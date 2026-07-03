#!/usr/bin/env python3
"""Read-only: zeigt die Disagreeing-Trefferliste fuer ein Paper (Titel-Suche),
exakt mit der aktuellen Logik aus get_disagreeing_papers (reines Produkt + Gate>=3).

Run:
  cd /Users/pvh/flowolf/flowolfFullstack
  app/venv/bin/python app/poc/show_disagreeing.py "Scaling Laws for Neural Language Models"
"""
import sys
import asyncio
import asyncpg


def _dsn() -> str:
    for line in open(".env"):
        if line.strip().startswith("DATABASE_URL"):
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            return v.replace("postgresql+asyncpg://", "postgresql://").split("?")[0]
    raise SystemExit("DATABASE_URL nicht in .env")


FIND_SQL = """
SELECT corpusid, title, year, citationcount, arxiv
FROM papers WHERE title ILIKE $1
ORDER BY citationcount DESC NULLS LAST LIMIT 10;
"""

# Exakt wie get_disagreeing_papers (citation_service.py), $1 = corpusid des Landmark A
DIS_SQL = """
SELECT DISTINCT
    c.citingcorpusid,
    citing_p.title as citing_title,
    citing_p.year as citing_year,
    citing_p.citationcount as citing_citationcount,
    c.contextcount,
    COALESCE(c.contextcount, 0) * COALESCE(citing_p.citationcount, 0) as citation_impact_score,
    d.summary_of_disagreement
FROM papers p
JOIN citations c ON p.corpusid = c.citedcorpusid
JOIN discourse d ON c.citationid = d.citationid
JOIN papers citing_p ON citing_p.corpusid = c.citingcorpusid
WHERE p.corpusid = $1
AND d.disagreement = true
AND COALESCE(c.contextcount, 0) >= 3
ORDER BY citation_impact_score DESC
LIMIT 50;
"""


async def main(title_substr: str) -> None:
    conn = await asyncpg.connect(_dsn(), ssl="require", timeout=60)
    try:
        matches = await conn.fetch(FIND_SQL, f"%{title_substr}%")
        if not matches:
            print(f"Kein Paper mit Titel ~ '{title_substr}' gefunden.")
            return
        print("Titel-Treffer (corpusid | year | citations | title):")
        for m in matches:
            print(f"  {m['corpusid']} | {m['year']} | {m['citationcount']} | {m['title'][:70]}")
        a = matches[0]
        print(f"\n>>> Verwende A = {a['corpusid']} ({a['title'][:60]}), arxiv={a['arxiv']}\n")

        rows = await conn.fetch(DIS_SQL, a["corpusid"])
        print(f"Disagreeing-Liste ({len(rows)} Treffer, Sortierung wie im UI):\n")
        for i, r in enumerate(rows, 1):
            print(f"#{i:2}  score={r['citation_impact_score']:>10}  "
                  f"ctx={r['contextcount']:>2}  cit={r['citing_citationcount']:>6}  "
                  f"({r['citing_year']})  {(r['citing_title'] or '')[:60]}")
        if not rows:
            print("  (keine disagreeing-Paper mit contextcount>=3)")
    finally:
        await conn.close()


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "Scaling Laws for Neural Language Models"
    asyncio.run(main(q))
