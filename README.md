# tertius-gaudens

**Mining scientific disagreement to time research entry.**

This repository accompanies the paper [*Where Should The AI Scientist Land, and When?*](PAPER.md) (Deutsch: [PAPER.de.md](PAPER.de.md)) — the title a deliberate counterpoint to *The AI Scientist* (Sakana AI, *Nature* 2026). It contains every script and intermediate data dump needed to reproduce the empirical claims, so that others can check the findings independently.

> **TL;DR** — Given a field’s whole literature, where is an automated "AI scientist" best brought into play? We answer through the four-paper evolution of neural scaling laws, mapping each to a role: **Kaplan = A** (opens the direction), **Hoffmann = B-novel** (corrects it with new experiments), **Besiroglu = B-audit** (re-analyzes the corrector’s data, finds its flaw), **DeepSeek = C** (re-optimizes the settled frame). The automatable roles are the **verifiable** ones — B-audit and C — not the **speculative** ones — A and B-novel — because search can substitute for insight only where an *oracle* exists. The chain is mined from the literature by deterministic bibliometrics plus one narrow use of AI: classifying each Semantic Scholar **in-text citation** as neutral / agreement / disagreement. Disagreement is a rare, high-fidelity signal (~5 % of *analyzed* edges) and functions as a hard gate.

---

## Why this is feasible: the data

| Layer | Source | Scale |
|---|---|---|
| Papers | arXiv CS (`cs.CV, cs.LG, cs.CL, cs.AI, cs.NE, cs.RO`) | **314,690** |
| Citation graph | Semantic Scholar (with **in-text citation contexts**) | **4,299,126 edges** |
| Discourse layer | per-edge agreement/disagreement + summaries (LLM-generated) | row-aligned, 4.3 M |
| Raw in-text contexts | Semantic Scholar context strings | **60,343 edges** |

**Disagreement is a rare, high-fidelity signal.** ~5 % of *analyzed* edges carry a disagreement label — a needle that functions as a hard gate. (Only 15.8 % of the graph was ever labeled, for cost; the batch was restricted to papers with a minimum citation footprint, so coverage is prominence-biased. See the paper, §4.3 / §5.3.)

**The chain falls out of three scores.** Among the ~3,000 papers citing Kaplan, ranking the substantive critics by `citationcount` (reach), with `contextcount` as tie-breaker — the focus signal does its work in the gate, the ranking measures reach puts **Hoffmann #1 and DeepSeek #3** (Henighan, a side-theme, sits at #2), surfaced deterministically. External check: Wikipedia’s *Neural scaling law* article independently canonizes Kaplan → Hoffmann → Besiroglu (the A → B-novel → B-audit spine); DeepSeek-as-C is the algorithm’s own forward candidate, not established canon. See the paper, §4.2–§4.4.

**Which roles can the AI take?** The two *verifiable* ones. The *speculative* corrector (B-novel) gets corrected: across 218 correctors (operationally: papers with `citationcount ≥ 300` issuing a disagreement with `contextcount ≥ 3` at a landmark with `citationcount ≥ 1000`; “corrected” = target of any labeled disagreement), issuing a correction is associated with **~23 % more disagreement-per-citation received** than for the 1,818 remaining papers with `citationcount ≥ 300`, and Hoffmann is corrected by 7 later papers (Besiroglu among them). B-audit (re-analyzing existing data, cheap, checkable) and C (optimizing within the settled frame, verifiable against existing loss curves) are in reach; A (no oracle) and B-novel (speculative *and* needs a 400+-model cluster) are not. See the paper, §6.

**Vintage / observation period:** the citation graph, discourse layer, and citation counts are co-dated **~January 2025**; case-study papers span **2020–2024**. Velocities use a `2025-01-01` reference date.

## Models used

- **`gpt-4o-mini`** (OpenAI), run via the **Batch API** (JSON mode, temp 0.1) — the per-edge in-text stance: `agreement` / `disagreement` booleans + summaries, generated at ingest.
- `claude-opus-4-8` — theme clustering, `confirming_correction` vs `rejection` framing, and per-in-text-context classification in this study.

---

## Reproduce

The scripts are **read-only** against a PostgreSQL mirror of the citation/discourse graph. Set `DATABASE_URL` (DigitalOcean-managed Postgres requires SSL).

```bash
export DATABASE_URL='postgresql://user:pass@host:port/db'
pip install asyncpg anthropic # anthropic only for the classifier

# §5.1 threshold calibration — citationcount percentiles
python scripts/poc_research_ideas.py calibrate # -> {p90:36, p95:68, p99:223}

# §5.2 ranked A→B triads (gate + earliest-critic selector)
# NOTE: top100 ranks A→B *triads* by a_citations × max(contextcount,1) × b_citations —
# a separate triad score, not the per-seed critic ranking (citationcount, contextcount as tie-breaker).
python scripts/poc_research_ideas.py top100 # -> top100.json (provided in data/)

# §4.3 / §5.3 disagreement rarity & context-count distributions
python scripts/diag_contextcount.py

# §5.2 velocity backtest (proxy 2): quarterly citation curves vs. same-age
# cohort percentiles; estimates t_A (Kaplan > p99, sustained) and t_B
# (Hoffmann > p95/p99, sustained). Result on this snapshot: t_A = 2020-Q3
# (~6 months after Kaplan), t_B = 2022-Q2 (the quarter after Hoffmann’s
# publication) — ~21 months before DeepSeek (2024-01) and ~24 months before
# Besiroglu (2024-04). Output: data/backtest_velocity.csv / .png
python scripts/backtest_velocity.py

# §5.4 per-context CRITICAL/SUPPORTIVE/NEUTRAL (needs ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-ant-...
SAMPLE_LIMIT=20 python scripts/classify_disagreement_contexts.py
```

Theme clustering and the velocity tables (§5.2) operate on `data/kaplan_critics.json`, which ships with this repo — no DB needed to inspect the case study.

## Provided data dumps

- [`data/top100.json`](data/top100.json) — 100 ranked A→B triads, each with the earliest qualified critic, `summary_of_disagreement`, critique strength, and rank score.
- [`data/kaplan_critics.json`](data/kaplan_critics.json) — all 28 qualified critics of Kaplan (2020) with publication dates, citation counts, in-text context counts, and disagreement summaries — the input to the theme-clustering case study.

## The selection algorithm

A search-and-rank cascade over the citation graph — deterministic bibliometrics plus one narrow AI step (per-edge in-text **stance**, precomputed at ingest):

```
monitor all 314,690 papers
│
▼
(1) DETECT landmark A     reception ≥ θ_A (prospectively: velocity above field)
│                         A emerges = Kaplan (not queried — detected)
▼
(2) SELECT substantive critics   among ~3,000 papers citing A, keep those that
                                 engage A repeatedly (contextcount ≥ 3)
                                 AND dispute it (disagreement = true) → 28
▼
(3) RANK by reach         citationcount (contextcount as tie-breaker)
│                         #1 = B (Hoffmann)   #3 = candidate C (DeepSeek)
▼
A → B → C   (recurse on B → auditor Besiroglu→Hoffmann);
            thresholds R(A),R(B) + theme/type screen layered on top
```

(A semantic search — `0.7·cosine(query,paper) + 0.3·min(1,cit/1000)` — is only a convenience for inspecting a *known* seed; the autonomous start is monitoring, not querying.)

The two quantities that do the work — `contextcount` (repeated in-text engagement) and stance (disagreement) — are exactly what pick Hoffmann and DeepSeek out of thousands: they cite Kaplan *many times* and do so to *find a flaw*.

The chain spans **two anchors**: Kaplan’s critics give Hoffmann + DeepSeek, but the auditor **Besiroglu does not cite Kaplan** — it disputes Hoffmann, so it surfaces only when the walk re-anchors on Hoffmann. The paper formalizes this traversal as a **Markov chain on the discourse graph** (§4.6), where re-anchoring is automatic and the open frontier is the set of near-absorbing states.

## Independent reproduction

Every quantitative claim in the paper has been reproduced once already — by an AI agent
(Claude, Anthropic) in an isolated sandbox **without access to the source database**, using
only the frozen snapshot and the unmodified scripts in this repository. The full protocol,
including the claim-by-claim result table, is in [`AUDIT.md`](AUDIT.md). To repeat the
reproduction yourself, see [`SNAPSHOT.md`](SNAPSHOT.md) (snapshot download, local Postgres
restore, script invocations).

## Related project

[flowolf.org](https://flowolf.org) — the reference application over the same corpus and
citation/discourse graph: semantic search across the 314,690-paper pool and inspection of
disagreement sets (the convenience interface mentioned in §4.2 of the paper).

## License & citation

Data derives from public sources (arXiv; Semantic Scholar Open Data). Please cite the accompanying paper and the underlying datasets. See [`PAPER.md`](PAPER.md) for references.
