#!/usr/bin/env python3
"""P(criticism | contextcount): does deeper in-text engagement raise disagreement?

Runs against the frozen snapshot (data/snapshot/), no live DB. Joins citations
(contextcount) with discourse (agreement/disagreement) on citationid and reports,
per contextcount bucket, the disagreement/agreement rate over ALL edges and over
the ANALYZED subset (a proxy: any stance true or a disagreement summary present).

Usage:
  python scripts/disagreement_by_contextcount.py     # expects ../data/snapshot/*.csv.gz
"""
import csv
import gzip
import os
from collections import Counter

SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "snapshot")
ORDER = ["1", "2", "3", "4", "5", "6-10", "11-20", "21+"]


def _bool(s: str) -> bool:
    return s in ("t", "true", "True", "1")


def _bucket(c: int) -> str:
    if c <= 5:
        return str(c)
    if c <= 10:
        return "6-10"
    if c <= 20:
        return "11-20"
    return "21+"


def main() -> None:
    dis, agr, has_summary = {}, {}, {}
    with gzip.open(os.path.join(SNAP, "discourse.csv.gz"), "rt") as f:
        for row in csv.DictReader(f):
            cid = row["citationid"]
            dis[cid] = _bool(row["disagreement"])
            agr[cid] = _bool(row.get("agreement", ""))
            s = row.get("summary_of_disagreement", "")
            has_summary[cid] = s not in ("", "none", "None", "NULL", None)

    tot, ndis, nagr, ana, ana_dis = (Counter() for _ in range(5))
    with gzip.open(os.path.join(SNAP, "citations.csv.gz"), "rt") as f:
        for row in csv.DictReader(f):
            cc = row["contextcount"]
            if cc in ("", "NULL", None):
                continue
            b = _bucket(int(cc))
            cid = row["citationid"]
            d, a = dis.get(cid, False), agr.get(cid, False)
            tot[b] += 1
            ndis[b] += d
            nagr[b] += a
            if d or a or has_summary.get(cid, False):
                ana[b] += 1
                ana_dis[b] += d

    print(f"{'ctx':>6} {'N':>10} {'P(disag)':>9} {'P(agree)':>9} "
          f"{'analyzed':>10} {'P(disag|ana)':>13}")
    for b in ORDER:
        n = tot[b]
        if not n:
            continue
        pa = 100 * ana_dis[b] / ana[b] if ana[b] else 0.0
        print(f"{b:>6} {n:>10,} {100*ndis[b]/n:>8.2f}% {100*nagr[b]/n:>8.2f}% "
              f"{ana[b]:>10,} {pa:>12.2f}%")


if __name__ == "__main__":
    main()
