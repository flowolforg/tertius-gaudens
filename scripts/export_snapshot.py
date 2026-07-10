#!/usr/bin/env python3
"""Export the frozen ~Jan-2025 snapshot for third-party reproduction.

Exports exactly the tables/columns the analysis scripts read (read-only) into
gzipped CSVs plus a manifest with row counts and checksums. Publish the
resulting data/snapshot/ files as a GitHub release asset or on Zenodo; anyone
can then restore them into a local Postgres with load_snapshot.py and run
every script in scripts/ unchanged.

Usage:
  export DATABASE_URL='postgresql://user:pass@host:port/db'   # source (SSL)
  python scripts/export_snapshot.py                # full export
  python scripts/export_snapshot.py --no-abstracts # smaller papers.csv.gz

Read-only: uses COPY (SELECT ...) TO STDOUT only.
"""
import argparse
import asyncio
import gzip
import hashlib
import json
import os
import sys
from datetime import date

import asyncpg

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "snapshot")

# Wunschspalten je Tabelle; exportiert wird der Schnitt mit den real
# existierenden Spalten (Introspektion via information_schema).
WANTED = {
    "papers": ["corpusid", "title", "year", "publicationdate", "citationcount",
               "arxiv", "abstract"],
    "citations": ["citationid", "citingcorpusid", "citedcorpusid", "contextcount"],
    "discourse": ["citationid", "disagreement", "agreement", "summary_of_disagreement"],
    "check_corpusids_agreement": ["citationid", "citingcorpusid", "citedcorpusid",
                                  "contextcount", "disagreement",
                                  "summary_of_disagreement", "contexts"],
}

COLS_SQL = """
SELECT column_name FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = $1
"""


async def resolve_columns(conn, with_abstracts: bool) -> dict[str, list[str]]:
    out = {}
    for table, wanted in WANTED.items():
        existing = {r["column_name"] for r in await conn.fetch(COLS_SQL, table)}
        if not existing:
            sys.exit(f"table {table} not found")
        cols = [c for c in wanted if c in existing]
        if not with_abstracts and "abstract" in cols:
            cols.remove("abstract")
        missing = [c for c in wanted if c not in existing]
        if missing:
            print(f"  note: {table} has no column(s) {missing} — skipped")
        out[table] = cols
    return out


def _dsn() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        sys.exit("DATABASE_URL not set")
    return url.replace("postgresql+asyncpg://", "postgresql://").split("?")[0]


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-abstracts", action="store_true",
                    help="omit papers.abstract (much smaller; only `validate` output loses text)")
    args = ap.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)
    conn = await asyncpg.connect(_dsn(), ssl="require", timeout=60)
    manifest = {"snapshot_date": "~2025-01", "exported": str(date.today()),
                "with_abstracts": not args.no_abstracts, "tables": {}}
    try:
        columns = await resolve_columns(conn, not args.no_abstracts)
        for name, cols in columns.items():
            query = f"SELECT {', '.join(cols)} FROM {name}"
            path = os.path.join(OUT_DIR, f"{name}.csv.gz")
            print(f"exporting {name} ({', '.join(cols)}) ...", flush=True)
            with gzip.open(path, "wb") as f:
                await conn.copy_from_query(query, output=f, format="csv", header=True)
            count = await conn.fetchval(f"SELECT count(*) FROM {name}")
            manifest["tables"][name] = {
                "rows": count,
                "file": os.path.basename(path),
                "sha256": _sha256(path),
                "size_bytes": os.path.getsize(path),
            }
            print(f"  {count:,} rows -> {path} ({os.path.getsize(path)/1e6:.1f} MB)")
    finally:
        await conn.close()

    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print("manifest.json written. Publish data/snapshot/* as a release asset.")


if __name__ == "__main__":
    asyncio.run(main())
