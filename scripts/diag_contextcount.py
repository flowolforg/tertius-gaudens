#!/usr/bin/env python3
"""Read-only Diagnose: Hat die discourse-Analyse (disagreeing/agreeing edges)
einen contextcount-Cutoff? Vergleicht die contextcount-Verteilung von
disagreeing- / agreeing- / allen discourse-Kanten gegen alle Zitationen.

Run:
  cd /Users/pvh/flowolf/flowolfFullstack
  app/venv/bin/python app/poc/diag_contextcount.py
"""
import asyncio
import asyncpg


def _dsn() -> str:
    dsn = None
    for line in open(".env"):
        if line.strip().startswith("DATABASE_URL"):
            dsn = line.split("=", 1)[1].strip().strip('"').strip("'")
            break
    if not dsn:
        raise SystemExit("DATABASE_URL nicht in .env gefunden")
    return dsn.replace("postgresql+asyncpg://", "postgresql://").split("?")[0]


Q_DIS = """
SELECT MIN(c.contextcount) min_cc, MAX(c.contextcount) max_cc,
       COUNT(*) FILTER (WHERE c.contextcount IS NULL) cc_null,
       COUNT(*) FILTER (WHERE c.contextcount = 1) eq1,
       COUNT(*) FILTER (WHERE c.contextcount = 2) eq2,
       COUNT(*) FILTER (WHERE c.contextcount = 3) eq3,
       COUNT(*) FILTER (WHERE c.contextcount >= 4) ge4,
       COUNT(*) total
FROM citations c JOIN discourse d ON d.citationid = c.citationid
WHERE d.disagreement = true;
"""
Q_AGR = Q_DIS.replace("d.disagreement = true", "d.agreement = true")
Q_ALLDISC = """
SELECT MIN(c.contextcount) min_cc,
       COUNT(*) FILTER (WHERE c.contextcount = 1) eq1,
       COUNT(*) total
FROM citations c JOIN discourse d ON d.citationid = c.citationid;
"""
Q_ALLCIT = """
SELECT MIN(contextcount) min_cc,
       COUNT(*) FILTER (WHERE contextcount = 1) eq1,
       COUNT(*) FILTER (WHERE contextcount IS NULL) cc_null,
       COUNT(*) total
FROM citations;
"""


async def main() -> None:
    conn = await asyncpg.connect(_dsn(), ssl="require", timeout=60)
    try:
        for name, q in [
            ("DISAGREEING edges", Q_DIS),
            ("AGREEING edges", Q_AGR),
            ("ALL discourse edges", Q_ALLDISC),
            ("ALL citations", Q_ALLCIT),
        ]:
            row = await conn.fetchrow(q)
            print(f"\n== {name} ==")
            for k, v in dict(row).items():
                print(f"   {k:10} = {v}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
