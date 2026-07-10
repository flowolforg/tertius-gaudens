#!/usr/bin/env python3
"""Restore the frozen ~Jan-2025 snapshot into a local Postgres.

Together with the published data/snapshot/*.csv.gz files, this makes every
quantitative claim in the paper checkable on a laptop — no access to the
authors' server required.

Quick start:
  docker run --name tertius-pg -e POSTGRES_PASSWORD=postgres \
             -p 5432:5432 -d postgres:16
  pip install asyncpg
  python scripts/load_snapshot.py \
      --dsn postgresql://postgres:postgres@localhost:5432/postgres
  export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
  PGSSL=disable python scripts/poc_research_ideas.py calibrate

Verifies row counts against manifest.json after loading.
"""
import argparse
import asyncio
import csv
import gzip
import io
import json
import os
import sys

import asyncpg

SNAP_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "snapshot")

DDL = {
    "papers": """
        CREATE TABLE IF NOT EXISTS papers (
            corpusid        BIGINT PRIMARY KEY,
            title           TEXT,
            year            INT,
            publicationdate DATE,
            citationcount   INT,
            arxiv           TEXT,
            abstract        TEXT
        )""",
    "citations": """
        CREATE TABLE IF NOT EXISTS citations (
            citationid      BIGINT PRIMARY KEY,
            citingcorpusid  BIGINT,
            citedcorpusid   BIGINT,
            contextcount    INT
        )""",
    "discourse": """
        CREATE TABLE IF NOT EXISTS discourse (
            citationid              BIGINT,
            disagreement            BOOLEAN,
            agreement               BOOLEAN,
            summary_of_disagreement TEXT
        )""",
    "check_corpusids_agreement": """
        CREATE TABLE IF NOT EXISTS check_corpusids_agreement (
            citationid              BIGINT,
            citingcorpusid          BIGINT,
            citedcorpusid           BIGINT,
            contextcount            INT,
            disagreement            BOOLEAN,
            summary_of_disagreement TEXT,
            contexts                TEXT[]
        )""",
}

INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_cit_cited  ON citations (citedcorpusid)",
    "CREATE INDEX IF NOT EXISTS idx_cit_citing ON citations (citingcorpusid)",
    "CREATE INDEX IF NOT EXISTS idx_disc_cid   ON discourse (citationid)",
    "CREATE INDEX IF NOT EXISTS idx_pap_date   ON papers (publicationdate)",
    "CREATE INDEX IF NOT EXISTS idx_pap_cites  ON papers (citationcount)",
    "CREATE INDEX IF NOT EXISTS idx_chk_cid    ON check_corpusids_agreement (citationid)",
]


def _header(path: str) -> list[str]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        return next(csv.reader(f))


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default="postgresql://postgres:postgres@localhost:5432/postgres")
    ap.add_argument("--snapshot-dir", default=SNAP_DIR)
    args = ap.parse_args()

    manifest_path = os.path.join(args.snapshot_dir, "manifest.json")
    if not os.path.exists(manifest_path):
        sys.exit(f"manifest.json not found in {args.snapshot_dir} — "
                 "download the snapshot release asset first.")
    manifest = json.load(open(manifest_path))

    conn = await asyncpg.connect(args.dsn, ssl=None, timeout=60)
    try:
        for table, info in manifest["tables"].items():
            path = os.path.join(args.snapshot_dir, info["file"])
            cols = _header(path)
            await conn.execute(DDL[table])
            await conn.execute(f"TRUNCATE {table}")
            print(f"loading {table} ({info['rows']:,} rows) ...", flush=True)
            with gzip.open(path, "rb") as f:
                await conn.copy_to_table(table, source=f, columns=cols,
                                         format="csv", header=True)
            got = await conn.fetchval(f"SELECT count(*) FROM {table}")
            status = "OK" if got == info["rows"] else f"MISMATCH (expected {info['rows']:,})"
            print(f"  {got:,} rows loaded — {status}")
            if got != info["rows"]:
                sys.exit(1)
        print("creating indexes ...")
        for stmt in INDEXES:
            await conn.execute(stmt)
    finally:
        await conn.close()
    print("done. Set DATABASE_URL to this DSN and run the analysis scripts "
         "(PGSSL=disable for a local server).")


if __name__ == "__main__":
    asyncio.run(main())
