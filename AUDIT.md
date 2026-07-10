# Independent reproduction audit

**Date:** 2026-07-10
**Auditor:** Claude (Anthropic), an AI agent operating in an isolated Linux sandbox (aarch64, Ubuntu 22) with **no access to the authors' source infrastructure**. The audit used only (a) the frozen snapshot files and (b) the unmodified analysis scripts from this repository.

## Input

`data/snapshot/` produced by `scripts/export_snapshot.py` against the source database (frozen ~January 2025 graph), 120 MB total. All four files verified against `manifest.json` by SHA-256 before use:

| File | Rows | SHA-256 verified |
|---|---:|---|
| papers.csv.gz | 314,690 | ✓ |
| citations.csv.gz | 4,299,126 | ✓ |
| discourse.csv.gz | 4,299,126 | ✓ |
| check_corpusids_agreement.csv.gz | 60,343 | ✓ |

## Environment

- PostgreSQL 16.4 (zonky embedded binaries, linux-arm64v8, run unprivileged via `initdb`/`pg_ctl`)
- Python 3.10, asyncpg
- Snapshot loaded with `scripts/load_snapshot.py` logic (COPY, explicit columns, row counts verified), indexes on `citations(citedcorpusid, citingcorpusid, citationid)`, `discourse(citationid)`, `papers(publicationdate, citationcount)`
- Scripts run unchanged except one connection-level substitution: `ssl="require"` → `ssl=None` (local server has no SSL)

## Commands and results

| Claim (paper) | Command | Result |
|---|---|---|
| §5.1 percentiles p90/p95/p99 = 36/68/223 | `poc_research_ideas.py calibrate` | `{'p90': 36, 'p95': 68, 'p99': 223}` — **exact** |
| Disagreement edges 35,389; 1.7 % single-context vs. 60.5 % overall; cc ≥ 3 retains 74.9 % | `diag_contextcount.py` | 35,389; 597/35,389 = 1.7 %; 2,601,772/4,299,126 = 60.5 %; 26,493/35,389 = 74.9 % — **exact** |
| §4.3 funnel: 326 landmark candidates; 3,031 Kaplan citers; 322 analyzed; 36 disagreement; 32 (cc ≥ 3); 28 in-corpus critics | direct read-only SQL | 326; 3,031; 322; 36; 32; 28 — **exact** |
| Base rates: 5.2 % of 680,392 analyzed edges (15.8 %); 11.2 % for Kaplan | direct read-only SQL | 680,392 analyzed; 5.2 %; 11.2 % — **exact** |
| §4.2 ranking: Hoffmann #1 (cc = 10, 1,571 citations), Henighan #2 (345), DeepSeek #3 by reach (cc = 7, 181) | `show_disagreeing.py "Scaling Laws for Neural Language Models"` | 28 hits; Hoffmann #1; Henighan 345; DeepSeek cc = 7, 181 — **exact** |
| Besiroglu: 14 lifetime citations; Besiroglu→Hoffmann cc = 10, unlabeled; Besiroglu→Kaplan: no edge | direct read-only SQL | 14; cc = 10, `disagreement = None`; no edge — **exact** |
| §5.2 backtest: cohorts 8,994 / 12,696; t_A = 2020-Q3 (Kaplan > p99 sustained); t_B = 2022-Q2 (Hoffmann) | `backtest_velocity.py` | N = 8,994, crossing 2020-07; N = 12,696, crossing 2022-04 — **exact** |
| §6: 218 correctors vs. 1,818 non-correctors; corrected 86.2 % vs. 81.0 %; +22.9 % disagreement per citation (pooled) | direct read-only SQL | 218; 1,818; 86.2 %; 81.0 %; +22.9 % — **exact** |
| Hoffmann target of 7 qualified disagreements | direct read-only SQL | 7 — **exact** |
| Top-100 A→B triads | `poc_research_ideas.py top100` | 100 triads generated — **matches** |

## Methodological note (fixed in the paper as of this audit)

The §6 corrector statistic reproduces only under the operational definition
*corrector = paper with citationcount ≥ 300 issuing a disagreement with
contextcount ≥ 3 at a landmark with citationcount ≥ 1000*, with *"corrected" =
target of at least one labeled disagreement of any context count*, and
*non-correctors = the remaining 1,818 papers with citationcount ≥ 300*. A naive
reading (no reception bar on the corrector) yields 7,162 candidates instead of
218. The paper's §6 wording has been amended to state the operational
definition explicitly.

## Verdict

Every quantitative claim checked reproduces exactly from the published
snapshot with the published scripts. In the paper's own terminology: this
audit is a **B-audit** — pure interpolation over existing numbers, performed
on commodity hardware by an agent without access to the source
infrastructure, completed before the paper's public announcement.
