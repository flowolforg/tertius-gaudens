#!/usr/bin/env python3
"""Per-context stance within disagreement edges — quantifies "engages to criticize?".

For each `disagreement = true` edge in the snapshot (check_corpusids_agreement,
which keeps the raw in-text contexts[]), classify EACH context as
CRITICAL / SUPPORTIVE / NEUTRAL toward the cited paper A, then report the share
of contexts that are actually critical. Tests whether a heavily-engaging citer
disputes A *throughout* (high critical share) or builds on A with criticism as
one facet (low critical share).

Read-only against the snapshot; needs ANTHROPIC_API_KEY for the classification.
Model default claude-opus-4-8; for the full ~13k-edge run use claude-haiku-4-5
via the Batch API (one request per edge, custom_id = citationid).

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  SAMPLE_LIMIT=40 MIN_CTX=8 python scripts/classify_contexts_snapshot.py
"""
import csv
import gzip
import json
import os
import sys
from collections import Counter

from anthropic import Anthropic

SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "snapshot")
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")
SAMPLE_LIMIT = int(os.environ.get("SAMPLE_LIMIT", "40"))
MIN_CTX = int(os.environ.get("MIN_CTX", "8"))

SYSTEM = (
    "You classify individual in-text citation contexts by how the citing text relates to "
    "the CITED paper A at that specific spot. Labels (exactly one per context): "
    "CRITICAL (disputes/criticizes A, names a weakness, contrasts unfavourably, outperforms A); "
    "SUPPORTIVE (agrees with/adopts/follows/builds on A, uses A as support); "
    "NEUTRAL (mere mention — notation, background, listing, methodology-following without judgement). "
    "Most contexts are NEUTRAL. Reply ONLY with JSON: "
    '{"labels":[{"i":<int>,"label":"CRITICAL|SUPPORTIVE|NEUTRAL"}]} in input order.'
)


def parse_pg_array(s: str) -> list[str]:
    if not s or s in ("{}", "NULL", None):
        return []
    body, out, i, n = s[1:-1], [], 0, len(s) - 2
    while i < n:
        if body[i] == '"':
            i += 1
            buf = []
            while i < n:
                c = body[i]
                if c == "\\":
                    buf.append(body[i + 1]); i += 2; continue
                if c == '"':
                    i += 1; break
                buf.append(c); i += 1
            out.append("".join(buf))
            if i < n and body[i] == ",":
                i += 1
        else:
            j = body.find(",", i)
            if j == -1:
                out.append(body[i:]); break
            out.append(body[i:j]); i = j + 1
    return out


def classify_edge(client: Anthropic, summary: str, contexts: list[str]) -> list[str]:
    numbered = "\n".join(f"[{i}] {c}" for i, c in enumerate(contexts))
    user = (f"Disagreement summary for context: {summary or 'N/A'}\n\n"
            f"Contexts (index in brackets):\n{numbered}")
    resp = client.messages.create(
        model=MODEL, max_tokens=2000, system=SYSTEM,
        messages=[{"role": "user", "content": user}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "")
    s, e = text.find("{"), text.rfind("}")
    data = json.loads(text[s:e + 1]) if s != -1 else {"labels": []}
    by_i = {d["i"]: d["label"] for d in data.get("labels", [])}
    return [by_i.get(i, "NEUTRAL") for i in range(len(contexts))]


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY not set")
    csv.field_size_limit(10_000_000)
    client = Anthropic()
    edges = []
    with gzip.open(os.path.join(SNAP, "check_corpusids_agreement.csv.gz"), "rt") as f:
        for row in csv.DictReader(f):
            if row["disagreement"] not in ("t", "true", "True", "1"):
                continue
            cc = row["contextcount"]
            if cc.isdigit() and int(cc) >= MIN_CTX:
                ctxs = parse_pg_array(row["contexts"])
                if len(ctxs) >= 6:
                    edges.append((row["citationid"], ctxs, row["summary_of_disagreement"]))
    edges.sort(key=lambda r: r[0])
    step = max(1, len(edges) // SAMPLE_LIMIT)
    sample = edges[::step][:SAMPLE_LIMIT]

    tot = Counter()
    per_edge = []
    for cid, ctxs, summ in sample:
        labels = classify_edge(client, summ, ctxs)
        c = Counter(labels)
        tot.update(labels)
        crit_share = c["CRITICAL"] / len(labels)
        per_edge.append({"citationid": cid, "n": len(labels), **c, "crit_share": round(crit_share, 3)})
        print(f"cid={cid} n={len(labels):>2} CRIT={c['CRITICAL']:>2} SUPP={c['SUPPORTIVE']:>2} "
              f"NEUT={c['NEUTRAL']:>2} crit_share={crit_share:.0%}")
    N = sum(tot.values())
    print(f"\n{len(sample)} edges, {N} contexts")
    for lab in ("CRITICAL", "SUPPORTIVE", "NEUTRAL"):
        print(f"  {lab:<11} {tot[lab]:>4} ({tot[lab]/N:.1%})")
    shares = [e["crit_share"] for e in per_edge]
    print(f"  mean per-edge critical share: {sum(shares)/len(shares):.1%}")
    json.dump({"per_edge": per_edge, "totals": dict(tot)},
              open("context_stance_result.json", "w"), indent=2)


if __name__ == "__main__":
    main()
