#!/usr/bin/env python3
"""Prototyp: echter per-Fundstelle disagreement_contexts via Claude.

Liest read-only die in `check_corpusids_agreement.contexts[]` gespeicherten In-Text-
Fundstellen und klassifiziert jede Stelle einzeln (CRITICAL / SUPPORTIVE / NEUTRAL
gegenueber dem zitierten Paper A). `disagreement_contexts` = Anzahl CRITICAL — ein
sentiment-spezifischer Count statt des sentiment-blinden `contextcount`.

Quelle:   PostgreSQL (DATABASE_URL aus .env), Tabelle check_corpusids_agreement.
Modell:   claude-opus-4-8 (per ANTHROPIC_MODEL ueberschreibbar; fuer den vollen
          60k-Lauf eher claude-haiku-4-5 + die Batches-API, s.u.).
Auth:     ANTHROPIC_API_KEY aus der Umgebung.

Run:
  cd /Users/pvh/flowolf/flowolfFullstack
  export ANTHROPIC_API_KEY=sk-ant-...
  SAMPLE_LIMIT=20 app/venv/bin/python app/poc/classify_disagreement_contexts.py

Skalierung auf alle 60.343 Kanten: NICHT synchron in einem Lauf. Die Anthropic
Batches-API (50% Preis, asynchron) ist der richtige Weg — pro Kante ein Request,
custom_id = citationid; danach disagreement_contexts je Kante aggregieren.
"""
import os
import sys
import json
import asyncio

import asyncpg
from anthropic import Anthropic

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")
SAMPLE_LIMIT = int(os.environ.get("SAMPLE_LIMIT", "20"))  # Kostenschranke fuer den Prototyp

# Stabiler, ueber alle Kanten identischer Klassifikations-Leitfaden.
# cache_control => wird als Praefix gecached. Hinweis: Prompt-Caching greift erst
# ab dem Modell-Minimum (Opus 4.8: 4096, Sonnet 4.6: 2048 Tokens). Dieser Leitfaden
# ist kuerzer, cached also real erst, wenn man ihn mit mehr Few-Shots auffuettert
# oder ein Sonnet-Modell nutzt; der echte Kostenhebel fuer 60k ist die Batches-API.
GUIDE = """\
Du klassifizierst einzelne In-Text-Zitations-Fundstellen daraufhin, wie sich der
zitierende Text gegenueber dem ZITIERTEN Paper A an genau dieser Stelle verhaelt.

Labels (genau eines pro Fundstelle):
- CRITICAL   : widerspricht A, bezweifelt/kritisiert Methode oder Ergebnis von A,
               grenzt sich ab, oder benennt eine Schwaeche/Abweichung von A.
- SUPPORTIVE : stimmt A zu, bestaetigt/uebernimmt A, nutzt A als Stuetze.
- NEUTRAL    : reine Erwaehnung/Verweis ohne Wertung — Notation, Definition,
               Gleichung, Hintergrund, "siehe A", Zaehlung in einer Liste.

Wichtig: Die meisten Fundstellen sind NEUTRAL (Notation/Verweise). Vergib CRITICAL
nur bei tatsaechlicher inhaltlicher Kritik/Abgrenzung an dieser Stelle, nicht nur
weil das Paper insgesamt als "disagreement" markiert ist.

Beispiele (gegenueber Kaplan et al. "Scaling Laws", [KMH+20]):
- "We didn't find a good closed-form model for from-scratch results as was seen in
   [KMH+20]"  -> CRITICAL  (benennt eine Abweichung/Schwaeche)
- "using the power-law exponents from [KMH+20]"  -> NEUTRAL  (Notation/Uebernahme)
- "confirming that they remain generally applicable"  -> SUPPORTIVE  (Bestaetigung)

Antworte AUSSCHLIESSLICH mit einem JSON-Objekt, kein Fliesstext, keine Code-Fences:
{"classifications": [{"index": <int>, "label": "CRITICAL|SUPPORTIVE|NEUTRAL"}, ...]}
Ein Eintrag pro Fundstelle, in derselben Reihenfolge wie die nummerierten Fundstellen.
"""

SYSTEM = [{"type": "text", "text": GUIDE, "cache_control": {"type": "ephemeral"}}]

# Hinweis: Garantierte Schema-Validierung ginge ueber output_config.format
# (strukturierte Ausgabe) — erfordert aber ein neueres anthropic-SDK. Das im venv
# installierte 0.75.0 kennt den Parameter nicht, daher hier ein Prompt-Vertrag
# (Modell gibt striktes JSON aus, wir parsen robust). Bei SDK-Upgrade umstellbar.

FETCH_SQL = """
SELECT k.citationid, k.citingcorpusid, k.citedcorpusid, k.contextcount,
       a.title AS cited_title, b.title AS citing_title,
       k.summary_of_disagreement, k.contexts
FROM check_corpusids_agreement k
LEFT JOIN papers a ON a.corpusid = k.citedcorpusid
LEFT JOIN papers b ON b.corpusid = k.citingcorpusid
WHERE k.disagreement = true AND k.contexts IS NOT NULL
ORDER BY k.citedcorpusid, k.contextcount DESC   -- gleiche A benachbart (Cache-freundlich)
LIMIT $1;
"""


def _dsn() -> str:
    for line in open(".env"):
        if line.strip().startswith("DATABASE_URL"):
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            return v.replace("postgresql+asyncpg://", "postgresql://").split("?")[0]
    raise SystemExit("DATABASE_URL nicht in .env gefunden")


async def fetch_rows() -> list[dict]:
    conn = await asyncpg.connect(_dsn(), ssl="require", timeout=60)
    try:
        return [dict(r) for r in await conn.fetch(FETCH_SQL, SAMPLE_LIMIT)]
    finally:
        await conn.close()


def classify_edge(client: Anthropic, cited_title: str, summary: str, contexts: list[str]) -> list[str]:
    """Klassifiziert alle Fundstellen einer Kante in einem Request -> Liste der Labels."""
    numbered = "\n".join(f"[{i}] {c}" for i, c in enumerate(contexts))
    user_text = (
        f"ZITIERTES Paper A: {cited_title or 'N/A'}\n"
        f"Worum geht der Widerspruch (Zusammenfassung): {summary or 'N/A'}\n\n"
        f"Fundstellen (Index in eckigen Klammern):\n{numbered}\n\n"
        f"Klassifiziere jede Fundstelle einzeln."
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=SYSTEM,
        messages=[{"role": "user", "content": user_text}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "")
    # robust: JSON-Objekt aus evtl. umgebendem Text herausschneiden
    s, e = text.find("{"), text.rfind("}")
    data = json.loads(text[s:e + 1]) if s != -1 and e != -1 else {"classifications": []}
    # Labels in Eingabereihenfolge zurueckgeben (robust gegen Reihenfolge/Luecken).
    by_index = {c["index"]: c["label"] for c in data.get("classifications", [])}
    return [by_index.get(i, "NEUTRAL") for i in range(len(contexts))]


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY nicht gesetzt")
    rows = asyncio.run(fetch_rows())
    client = Anthropic()
    out = []
    print(f"Klassifiziere {len(rows)} Kanten (Modell {MODEL})\n")
    for r in rows:
        contexts = r["contexts"] or []
        labels = classify_edge(client, r["cited_title"], r["summary_of_disagreement"], contexts)
        crit = labels.count("CRITICAL")
        supp = labels.count("SUPPORTIVE")
        neut = labels.count("NEUTRAL")
        out.append({
            "citationid": r["citationid"],
            "citing_title": r["citing_title"],
            "cited_title": r["cited_title"],
            "contextcount": r["contextcount"],
            "disagreement_contexts": crit,
            "supportive_contexts": supp,
            "neutral_contexts": neut,
            "labels": labels,
        })
        print(f"ctx={r['contextcount']:>2}  CRITICAL={crit:>2} SUPP={supp:>2} NEUT={neut:>2}  "
              f"| {(r['citing_title'] or '')[:42]}  ->  {(r['cited_title'] or '')[:30]}")
    with open("disagreement_contexts.json", "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, default=str)
    n_ctx = sum(o["contextcount"] or 0 for o in out)
    n_crit = sum(o["disagreement_contexts"] for o in out)
    print(f"\nSumme: {n_ctx} Fundstellen -> {n_crit} CRITICAL "
          f"({100*n_crit/n_ctx:.0f}% sind echte Kritik). -> disagreement_contexts.json")


if __name__ == "__main__":
    main()
