#!/usr/bin/env python3
"""Flowolf PoC: Forschungsideen-Finder — Top-100 + Validierung. Read-only.

Identifiziert Triaden A -> B (B kritisiert ein bahnbrechendes A) und liefert je
Landmark A den ZEITLICH FRUEHESTEN qualifizierten Kritiker B (Selektor = Zeit),
gefiltert ueber absolute Schwellen (Gate). Themen-Extraktion + Validierung am
Referenzfall Kaplan -> Hoffmann -> {Besiroglu, DeepSeek} passieren danach in der
Claude-Session auf Basis der Ausgabe.

Usage:
  export DATABASE_URL=postgresql://user:pass@host:port/db
  python poc_research_ideas.py top100             # -> top100.json
  python poc_research_ideas.py validate A B BYEAR # Folger-Kandidaten fuer (A,B,B-Jahr)
  python poc_research_ideas.py calibrate          # Perzentile zur Schwellen-Kontrolle

Benoetigt: asyncpg (bereits in requirements.txt).
"""
import os
import sys
import json
import asyncio

import asyncpg

# Konservative absolute Schwellen (Gate) — via `calibrate` pruefen/anpassen.
THETA_A = 1000       # R(A): A = Landmark (Lebenszeit-Zitate)
THETA_R = 300        # R(B): qualifizierter Kritiker
THETA_C = 3          # C(B->A): echte Auseinandersetzung statt Vorbei-Zitat.
                     # "Dreimal zitiert man nicht im Vorbeigehen." Behaelt 74,9% der
                     # disagreeing-Kanten (cc>=3); Ruckfalloption 2, falls zu wenig Treffer.
                     # Deckt sich mit dem Gate in get_disagreeing_papers.
THETA_FOLLOW = 200   # Mindest-Rezeption der Folger-Kandidaten (Validierung)


def _dsn() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        sys.exit("DATABASE_URL not set")
    # asyncpg versteht weder das SQLAlchemy-Schema noch Query-Optionen.
    return url.replace("postgresql+asyncpg://", "postgresql://").split("?")[0]


async def _connect() -> asyncpg.Connection:
    # DigitalOcean Managed Postgres verlangt i.d.R. SSL.
    return await asyncpg.connect(_dsn(), ssl="require")


TOP100_SQL = """
WITH qualified AS (
  SELECT a.corpusid AS a_corpusid, a.title AS a_title, a.year AS a_year,
         a.citationcount AS a_citations,
         b.corpusid AS b_corpusid, b.title AS b_title, b.year AS b_year,
         b.publicationdate AS b_date, b.citationcount AS b_citations,
         COALESCE(c.contextcount, 0) AS critique_strength,
         d.summary_of_disagreement,
         (a.citationcount::numeric * GREATEST(COALESCE(c.contextcount, 0), 1) * b.citationcount)
           AS rank_score
  FROM papers a
  JOIN citations c ON c.citedcorpusid = a.corpusid
  JOIN discourse d ON d.citationid = c.citationid
  JOIN papers b ON b.corpusid = c.citingcorpusid
  WHERE d.disagreement = true
    AND a.citationcount >= $1 AND b.citationcount >= $2
    AND COALESCE(c.contextcount, 0) >= $3 AND b.corpusid <> a.corpusid
),
earliest_per_a AS (  -- Selektor = Zeit: fruehester qualifizierter Kritiker pro A
  -- publicationdate (echte Tagesaufloesung) loest auch Intra-Jahr-Reihenfolge;
  -- Fallback auf b_year, falls publicationdate fehlt.
  SELECT DISTINCT ON (a_corpusid) * FROM qualified
  ORDER BY a_corpusid, b_date ASC NULLS LAST, b_year ASC NULLS LAST, b_citations DESC
)
SELECT * FROM earliest_per_a ORDER BY rank_score DESC LIMIT 100;
"""

VALIDATE_SQL = """
SELECT DISTINCT f.corpusid, f.title, f.year, f.publicationdate, f.citationcount,
       CASE WHEN cf.citedcorpusid = $2 THEN 'cites_B' ELSE 'cites_A' END AS relation,
       df.disagreement, df.summary_of_disagreement, f.abstract
FROM citations cf
JOIN papers f ON f.corpusid = cf.citingcorpusid
LEFT JOIN discourse df ON df.citationid = cf.citationid
WHERE cf.citedcorpusid IN ($1, $2) AND f.corpusid NOT IN ($1, $2)
  AND f.year >= $3 AND f.citationcount >= $4
ORDER BY f.citationcount DESC LIMIT 50;
"""

CALIBRATE_SQL = """
SELECT percentile_disc(0.90) WITHIN GROUP (ORDER BY citationcount) AS p90,
       percentile_disc(0.95) WITHIN GROUP (ORDER BY citationcount) AS p95,
       percentile_disc(0.99) WITHIN GROUP (ORDER BY citationcount) AS p99
FROM papers;
"""


async def top100() -> None:
    conn = await _connect()
    try:
        rows = await conn.fetch(TOP100_SQL, THETA_A, THETA_R, THETA_C)
        data = [dict(r) for r in rows]
        with open("top100.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"{len(data)} Triaden -> top100.json")
    finally:
        await conn.close()


async def validate(a: str, b: str, byear: str) -> None:
    conn = await _connect()
    try:
        rows = await conn.fetch(VALIDATE_SQL, int(a), int(b), int(byear), THETA_FOLLOW)
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False, indent=2, default=str))
    finally:
        await conn.close()


async def calibrate() -> None:
    conn = await _connect()
    try:
        print(dict(await conn.fetchrow(CALIBRATE_SQL)))
    finally:
        await conn.close()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "top100"
    if cmd == "top100":
        asyncio.run(top100())
    elif cmd == "validate":
        if len(sys.argv) < 5:
            sys.exit("usage: validate A_corpusid B_corpusid B_year")
        asyncio.run(validate(*sys.argv[2:5]))
    elif cmd == "calibrate":
        asyncio.run(calibrate())
    else:
        sys.exit(f"unknown command: {cmd}")
