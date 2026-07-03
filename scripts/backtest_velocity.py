"""
backtest_velocity.py — Proxy-2-Backtest der Velocity-Reformulierung (§5.2).

Rekonstruiert Zitations-Trajektorien aus dem eingefrorenen Snapshot: Ein
Zitationsereignis wird auf das Publikationsdatum des zitierenden Papers
datiert (nur Zitierer innerhalb des arXiv-CS-Korpus sind datierbar; für
Kaplan sind das 2.311 von 3.567 Lebenszeit-Zitationen, ~65 %).

Methode:
  1. Kohorte = alle Korpus-Paper aus dem Publikationsquartal des Zielpapers.
  2. Je Kohorten-Paper: Zitationen pro Kalenderquartal (fehlende Quartale = 0).
  3. Baseline = p95/p99 der Quartalsraten über die Kohorte, je Quartal.
  4. Crossing = erstes Quartal, in dem das Zielpaper das Band überschreitet
     und im Folgequartal darüber bleibt (2-Quartale-Regel gegen Rauschen).
     t_A: Kaplan > p99 (Landmark-Kandidat). t_B: Hoffmann > p95, zusätzlich
     bedingt auf die Existenz der stance-gelabelten Disput-Kante (ab
     Hoffmanns Publikation, 2022-03-29).

Read-only gegen den Quell-Graphen. DATABASE_URL setzen (SSL erforderlich).
Ausgabe: data/backtest_velocity.csv und Konsolen-Zusammenfassung.
"""
import asyncio, asyncpg, csv, datetime as dt, math, os, ssl, sys

KAPLAN, HOFFMANN = 210861095, 247778764
TARGETS = [
    ("Kaplan",   KAPLAN,   dt.date(2020, 1, 1), dt.date(2020, 4, 1)),
    ("Hoffmann", HOFFMANN, dt.date(2022, 1, 1), dt.date(2022, 4, 1)),
]
LAST_QUARTER = (2024, 10)  # letztes volles Quartal vor dem ~Jan-2025-Snapshot
SUSTAIN = 2                # Quartale in Folge über dem Band

def _dsn() -> str:
    dsn = os.environ.get("DATABASE_URL", "")
    if not dsn:
        sys.exit("DATABASE_URL setzen (postgresql://…)")
    return dsn.replace("postgresql+asyncpg://", "postgresql://")

def quarters(start: dt.date, last=LAST_QUARTER):
    y, m = start.year, 1 + 3 * ((start.month - 1) // 3)
    out = []
    while (y, m) <= last:
        out.append(f"{y:04d}-{m:02d}")
        m += 3
        if m > 10:
            m, y = 1, y + 1
    return out

async def cohort_curves(conn, a: dt.date, b: dt.date):
    """Quartalsraten aller Paper mit Publikationsdatum in [a, b)."""
    n = await conn.fetchval(
        "select count(*) from papers where publicationdate>=$1 and publicationdate<$2", a, b)
    rows = await conn.fetch("""
        select ci.citedcorpusid cid,
               to_char(date_trunc('quarter', p.publicationdate), 'YYYY-MM') q,
               count(*) n
        from citations ci
        join papers a on a.corpusid = ci.citedcorpusid
             and a.publicationdate >= $1 and a.publicationdate < $2
        join papers p on p.corpusid = ci.citingcorpusid
             and p.publicationdate is not null
        group by 1, 2""", a, b)
    curves = {}
    for r in rows:
        curves.setdefault(r["cid"], {})[r["q"]] = r["n"]
    return n, curves

def percentile(sorted_vals, n_total, p):
    """p-Perzentil über n_total Werte, fehlende als 0 vorangestellt."""
    k = min(n_total - 1, math.ceil(p * n_total) - 1)
    zeros = n_total - len(sorted_vals)
    return 0 if k < zeros else sorted_vals[k - zeros]

def first_crossing(qs, target, bands, band_idx):
    run = 0
    for q in qs:
        run = run + 1 if target.get(q, 0) > bands[q][band_idx] else 0
        if run == SUSTAIN:
            return q
    return None

async def main():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    conn = await asyncpg.connect(_dsn(), ssl=ctx, timeout=30)
    out_rows = []
    for name, cid, a, b in TARGETS:
        n, curves = await cohort_curves(conn, a, b)
        qs = quarters(a)
        bands = {}
        for q in qs:
            vals = sorted(c.get(q, 0) for c in curves.values())
            bands[q] = (percentile(vals, n, 0.95), percentile(vals, n, 0.99))
        tgt = curves.get(cid, {})
        c95 = first_crossing(qs, tgt, bands, 0)
        c99 = first_crossing(qs, tgt, bands, 1)
        print(f"{name}: Kohorte N={n}; erstes anhaltendes Crossing "
              f">p95: {c95}, >p99: {c99}")
        for q in qs:
            out_rows.append([name, q, tgt.get(q, 0), bands[q][0], bands[q][1]])
    await conn.close()
    path = os.path.join(os.path.dirname(__file__), "..", "data", "backtest_velocity.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["paper", "quarter", "citations_in_quarter", "cohort_p95", "cohort_p99"])
        w.writerows(out_rows)
    print("geschrieben:", os.path.normpath(path))

if __name__ == "__main__":
    asyncio.run(main())
