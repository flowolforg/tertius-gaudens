# Reproducing without access to our server: the frozen snapshot

The analysis scripts run read-only against a PostgreSQL mirror of the
citation/discourse graph. That mirror is private infrastructure — so the
frozen **~January 2025 snapshot** the paper is based on is published as a
set of gzipped CSVs (a GitHub release asset). Restoring it locally makes
**every quantitative claim in the paper checkable on a laptop**, in the
spirit of §6: audit is cheap.

## 1. What the snapshot contains

Exactly the tables/columns the scripts in `scripts/` read:

| Table | Rows | Used by |
|---|---|---|
| `papers` | 314,690 | all scripts (§5.1 calibration, cohorts, titles) |
| `citations` | 4,299,126 | funnel §4.3, chain edges, backtest §5.2 |
| `discourse` | ~680 k labeled edges | disagreement gate, §5.3 rarity |
| `check_corpusids_agreement` | 60,343 edges with raw in-text contexts | §5.4 classifier, audit of stance labels |

Produced by `scripts/export_snapshot.py` (run by the authors against the
source DB; `--no-abstracts` shrinks `papers.csv.gz` if needed).
`manifest.json` carries row counts and SHA-256 checksums for verification.

## 2. Restore locally (one-time, ~5 minutes)

```bash
# 1. download data/snapshot/* from the release and place under data/snapshot/
# 2. start a throwaway Postgres
docker run --name tertius-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
# 3. load + verify against manifest
pip install asyncpg
python scripts/load_snapshot.py --dsn postgresql://postgres:postgres@localhost:5432/postgres
```

## 3. Run the analysis scripts against the local copy

```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
export PGSSL=disable   # local server has no SSL
python scripts/poc_research_ideas.py calibrate   # -> {p90:36, p95:68, p99:223}
python scripts/poc_research_ideas.py top100
python scripts/diag_contextcount.py
python scripts/backtest_velocity.py
```

### Required one-line patch (SSL)

The scripts default to SSL because the source is a managed Postgres. To honor
`PGSSL=disable`, change the connect calls as follows (four places):

```python
# before
conn = await asyncpg.connect(_dsn(), ssl="require", timeout=60)
# after
_SSL = None if os.environ.get("PGSSL") == "disable" else "require"
conn = await asyncpg.connect(_dsn(), ssl=_SSL, timeout=60)
```

- `scripts/poc_research_ideas.py` → `_connect()`
- `scripts/diag_contextcount.py` → `main()` (add `import os`)
- `scripts/show_disagreeing.py` → `main()` (add `import os`)
- `scripts/backtest_velocity.py` → `main()`: replace the `ssl.create_default_context()`
  block with the same `_SSL` logic (`ssl=_SSL` instead of `ssl=ctx`)

## 4. Claim-by-claim map

| Paper claim | Command |
|---|---|
| §5.1 percentiles p90/p95/p99 = 36/68/223 | `poc_research_ideas.py calibrate` |
| §4.3 funnel (3,031 → 322 → 36 → 32 → 28), 5.2 % / 11.2 % base rates | `diag_contextcount.py` + `show_disagreeing.py "Scaling Laws for Neural Language Models"` |
| §4.2 ranking: Hoffmann #1, DeepSeek #3 (cc 10 / 7) | `show_disagreeing.py` |
| §5.2 backtest: t_A = 2020-Q3, t_B = 2022-Q2, window ~21–24 months | `backtest_velocity.py` |
| §5.4 per-context CRITICAL/SUPPORTIVE/NEUTRAL | `classify_disagreement_contexts.py` (needs `ANTHROPIC_API_KEY`) |
| Top-100 A→B triads | `poc_research_ideas.py top100` (also shipped: `data/top100.json`) |

## 5. Licensing

The snapshot is a derived work of arXiv metadata and the Semantic Scholar
Open Data Platform (ODC-BY 1.0). Any redistribution must retain the
attribution notice in `LICENSE`. The discourse labels (LLM-generated) are
provided under the repository's data terms.
