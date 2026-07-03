# Where Should The AI Scientist Land, and When?

*The title alludes to* The AI Scientist *[11]; the argument (§3.5) is that such a system should land not on the direction-opening role it reaches for, but on the verifiable roles — and knowing* when *is half the problem.*

### The evolution of neural scaling laws as a worked case, and a method for timing automated research

**Author:** Philipp von Hilgers
**Companion repository:** https://github.com/flowolforg/tertius-gaudens (all data, scripts, intermediate dumps — §10)
**Data vintage:** citation/discourse snapshot co-dated ~January 2025; case papers span 2020–2024.
*(Deutsche Fassung: [PAPER.de.md](PAPER.de.md))*

---

## 1. Introduction: a case and a question

Automated research systems are improving quickly, but the strategic question is less "can an AI do research?" than **"where in the life-cycle of an idea should it act?"** A field's literature is a sequence of moves — someone opens a direction, someone corrects it, someone audits the correction, someone supersedes it. These moves are not equally hard, equally risky, or equally automatable. Choosing the right one is the whole game.

We make the question concrete with a case whose arc is now visible in full: **neural scaling laws.** Four papers define it.

- **Kaplan et al. [1]** — *Scaling Laws for Neural Language Models* (2020).
- **Hoffmann et al. [3]** — *Training Compute-Optimal LLMs* (Chinchilla; 2022).
- **Besiroglu et al. [4]** — *Chinchilla Scaling: A Replication Attempt* (2024).
- **DeepSeek-AI [5]** — *DeepSeek LLM* (2024).

Retrospectively, **at which of these points could an AI scientist best have contributed?** We argue: at Besiroglu and DeepSeek — the *re-analysis* and the *re-optimization* — and not at Kaplan or Hoffmann, the *direction-opening* and the *new-experiment correction*. §2 summarizes what each paper actually contributed; §3 abstracts the four roles into a transferable concept and states the precise axis (verifiable vs. speculative novelty); §4 shows how the chain is mined from the raw literature with deterministic bibliometrics and one targeted use of AI; §5 defines the thresholds whose crossing is the *starting gun*; §6 analyzes role-by-role what is in reach and what is not; §7 sketches the resulting research landscape; §8 turns the framework on this paper itself.

The point of the case is not the case. It is that the same structure — opener, corrector, auditor, optimizer — recurs across fields, so a method that locates these roles in scaling-laws can be pointed at *live* fronts to time entry prospectively.

---

## 2. Four insights: what Kaplan, Hoffmann, Besiroglu, and DeepSeek actually established

| Paper (year) | Knowledge gain | Role | Mode |
|---|---|---|---|
| **Kaplan** [1] (2020) | Loss falls *predictably* with compute, parameters, and data as power laws — model performance becomes forecastable before training. | **A** — opens the direction | speculative |
| **Hoffmann / Chinchilla** [3] (2022) | Kaplan's allocation was suboptimal; for a fixed compute budget, parameters and training tokens should scale *roughly equally*. Established by training 400+ models. | **B-novel** — corrects the formula | speculative |
| **Besiroglu** [4] (2024) | Re-analyzed Chinchilla's *own published data* and found the reported parametric fit statistically inconsistent (implausibly tight intervals; not reproducible). No new training. | **B-audit** — audits the corrector | verifiable |
| **DeepSeek** [5] (2024) | Re-based the scale variable on *non-embedding FLOPs/token* (not parameter count), yielding cleaner, more transferable scaling fits and practical hyperparameter scaling. | **C** — re-optimizes the frame | verifiable |

Kaplan et al. (2020) [1] were the first to show systematically that language-model loss follows power laws across several orders of magnitude — in model size (non-embedding parameters), dataset size, and training compute. Two consequences followed: model performance becomes forecastable before training, and for a growing compute budget one should scale parameter count much faster than data (N_opt ∝ C^0.73) — very large models, trained on comparatively little data and stopped well before convergence. The paper opened the direction: performance as a computable function of investment.

Hoffmann et al. (2022) [3] re-measured the frontier — with over 400 trained models and three independent estimation approaches. The result: Kaplan's allocation was suboptimal; parameters and training tokens should scale roughly equally (N_opt ∝ C^0.5). The evidence was Chinchilla (70B parameters), which outperformed the four-times-larger Gopher at the same compute budget. The correction delivered "the right formula" — at the price of new large-scale experiments.

Besiroglu et al. (2024) [4] reconstructed the data points from Hoffmann's published figures and attempted to replicate its third estimation procedure (the parametric fit). The finding: the reported parameters are inconsistent with the other two approaches, fit the extracted data poorly, and the confidence intervals are implausibly narrow — intervals this narrow would require over 600,000 experiments, while likely fewer than 500 were run. Their own re-fit (α = 0.35, β = 0.37) reconciles approach 3 with approaches 1 and 2. No new training: an audit of published numbers on commodity hardware.

DeepSeek-AI (2024) [5] re-examined scaling laws in the course of training DeepSeek LLM: model scale is represented by non-embedding FLOPs per token instead of parameter counts, the allocation is re-fitted on that basis — with the finding that the optimum depends on data quality — and hyperparameters (batch size, learning rate) become scalable as formulas of the compute budget. The paper also records that earlier works (Kaplan, Hoffmann) reached differing conclusions — precisely the lack of consensus our discourse signal picks up.

Read top to bottom, the chain is a dialectic: a bold claim (A), a confirming correction that lands the "right formula" (B-novel), a sober audit that finds the correction itself flawed (B-audit), and a re-optimization that supersedes the whole setup from inside (C). Kaplan and Hoffmann reach *beyond* the settled record; Besiroglu and DeepSeek work *within* it. That difference is the paper's hinge.

---

## 3. The concept: the *tertius gaudens* triad and the verifiable/speculative axis

### 3.1 The de-risking dialectic

Borrowing Simmel's *tertius gaudens* [8] — the "rejoicing third" who profits from the configuration of two others — we read the chain as a structural opportunity (closely related to Burt's structural holes [9]). When a landmark **A** is *confirmed and corrected* by a strong **B**, the direction has been **de-risked**: it is now known to matter *and* it has a precise, well-posed form. A third actor **C** can then execute the radical optimization the formalized problem invites. Unlike Simmel's rivalry, this is dialectical — A is thesis, B the confirming-corrective antithesis, and the synthesis-shaped opening is the prize. The third takes no side; it harvests the **certainty** A and B jointly manufactured.

### 3.2 The real axis is verifiable vs. speculative novelty

The naïve framing asks "should the AI play A, B, or C?" — a question of role. The right axis is **not "how creative" but "how verifiable at the moment of the act."** The claim is *not* that the automatable moves are uncreative: DeepSeek's choice of a non-embedding-FLOPs measure was genuine and non-obvious. The claim is about epistemic structure:

- **An oracle exists for C and B-audit, not for A and B-novel.** Once B has landed the frame, the objective is formalized (compute = f(parameters, tokens), an explicit frontier) and the yardstick is fixed (loss curves). C's contribution is *checkable the moment it is tried*; Besiroglu's audit is checkable against Hoffmann's published numbers. Kaplan had to invent the yardstick — nothing to check against; Hoffmann's allocation resolved only years later. C and B-audit create on the *decidable* side of the line; A and B-novel wager on undecided terrain.
- **Search substitutes for insight only where an oracle exists.** This is the crux. C's creative choice — which re-parameterization to try — is not mechanically derivable, but it is **substitutable by breadth × verification**: enumerate the natural compute measures, let the loss curves decide. Where a human used insight to guess, a machine can try-and-check. A has no verifier at the time; there, search cannot replace insight.
- **Bounded vs. unbounded failure.** A wrong C merely fails to win (local, recoverable). A wrong A collapses its own premise; a wrong B-novel misleads the whole field. Verifiable novelty has bounded downside; speculative novelty does not.

As a spectrum:

```
   A    ────────   B-novel   ────────   C    ────────   B-audit
postulate          postulate a law    optimize        re-check
the frame          inside the frame   in the frame    the frame
no oracle          oracle only later  oracle now       oracle now
└──── speculative: insight required ──┘└── verifiable: search substitutes ──┘
```

**Honest boundary.** The argument rests on the space of useful re-parameterizations being *small and searchable enough* for the oracle to find the hit. For scaling *measures* (finitely many natural compute definitions) that is plausible; for a genuinely non-searchable architectural leap, C would slide toward A and the claim would weaken.

### 3.3 Collapsing the wait

This dissolves "why wait for C?" The wait was an **artifact of human division of labor** — Kaplan→…→DeepSeek took four years because four actors moved in sequence. But B-audit and C are the **same machine capability**: generate-and-verify against the existing record. An agent that audits a landmark can propose the optimized successor *in the same move*, collapsing the human gap into one. It need not wait for a third party to harvest the certainty it just manufactured. What stays off-limits is only the speculative pair, A and B-novel.

### 3.4 From case to method

Nothing above is specific to scaling laws. Any field that records *who disputes whom, and how substantively* exposes the same A→B→C structure. The remainder of the paper builds the extraction and timing method (§4–§5) and then asks which roles an automated agent can actually fill (§6).

### 3.5 Related work: autonomous idea generation

The closest prior system is *The AI Scientist* [11], the first autonomous pipeline to carry a machine-generated paper through blind peer review — a real engineering milestone. Its **idea generation**, however, is structurally different, and the contrast sharpens what we propose. There, a human code template seeds an iterative loop in which an LLM acts as a *mutation operator* growing an archive of ideas; each idea carries *self-assessed* interestingness/novelty/feasibility scores (1–10), and novelty is *enforced* by discarding proposals too **semantically similar** to existing work (via the Semantic Scholar API), under the prompt to be an "ambitious AI PhD student … contributing significantly to the field." Four differences follow:

- **Novelty as dissimilarity vs. standing as dispute.** The AI Scientist equates novelty with *semantic distance* from prior work. But distance is a weak proxy for value — much of the best work sits *close* to a landmark and disputes it precisely (Chinchilla is "near" Kaplan and matters *because* it contradicts it). We read an idea's standing not from similarity but from *who substantively disputes whom* — an external structural fact, not a self-report or a distance.
- **Same data source, opposite use.** Both lean on Semantic Scholar. The AI Scientist queries it for *dissimilarity* (avoid overlap); we use its *in-text citation contexts* for *engagement and dispute* — a rarer, sharper signal (§4.3) that separates a landmark's real critics from its ceremonial citers.
- **No timing.** Mutating a template proceeds in a temporal vacuum; there is no notion of *when* a direction is ripe. Our method is about timing — the velocity-based starting gun *t_B* (§5.5), the moment a direction is de-risked. An idea can be novel-and-feasible yet premature or already stale; a similarity check cannot tell.
- **Which role is even automatable.** Reaching for "significant, novel contributions" implicitly aims at the **A** role — opening a direction — which is *speculative* novelty with no oracle (§3.2), the least automatable act. We argue the reachable roles are the *verifiable* ones, **B-audit and C**, and that idea generation should be pointed there.

None of this diminishes the engineering; our claim is narrower and orthogonal — that *idea selection and timing*, read from the field's disagreement structure rather than from self-assessed novelty, is where an automated scientist gains traction. This is the sense in which the paper's title answers [11]: it names *where* such a system should land (the verifiable roles, §6) and *when* (the velocity-based starting gun, §5.5).

---

## 4. Extracting the chain from the literature pool

The chain is produced by a search-and-rank algorithm over the citation graph: **deterministic bibliometrics** (no model, fully reproducible) plus **one narrowly-scoped AI step** — the per-edge in-text stance — precomputed at ingest. Keeping AI confined to that single judgment is deliberate: everything else is auditable arithmetic. A reference implementation ships with the paper (§10).

### 4.1 Sources

- **arXiv (computer science).**[^arxiv] Categories `cs.CV, cs.LG, cs.CL, cs.AI, cs.NE, cs.RO` → **314,690 papers** (`title, abstract, year, publicationdate, citationcount`). Day-level `publicationdate` matters: in 49 of our 100 candidate triads, A and B share a *year*.
- **Semantic Scholar citation graph** [7]. **4,299,126 citation edges** — and, decisively, **in-text citation contexts**: `contextcount`, the number of distinct in-text locations where a citing paper invokes the cited one, plus the raw context strings for a 60,343-edge subset.

### 4.2 The selection algorithm

Two graph quantities drive the algorithm, and a bare citation count is neither:

- **`contextcount`** — how many distinct in-text locations a citing paper devotes to the cited one. Citing a paper once, in passing, is ceremonial; citing it *repeatedly* is sustained engagement.
- **stance** — whether those in-text mentions *dispute* the cited paper. This is the one AI-judged quantity (§4.7): a plain count cannot tell "[KMH20] is wrong about X" from "using the exponents of [KMH20]."

The algorithm has three stages:

1. **Obtain the landmark A — by monitoring, not querying.** The autonomous system does not search for a seed; it **monitors the whole corpus** and flags any paper that crosses the landmark bar — reception `≥ θ_A` (prospectively, citation *velocity* above the field; §5.5). A is *detected as it emerges*, not requested. (For a human wanting to inspect a *known* seed, semantic retrieval also works — embed the query and rank by `0.7·cosine(query, paper) + 0.3·min(1, citationcount/1000)` — but that is a convenience, not the algorithm's start.) Here the detected seed is Kaplan.
2. **Select the substantive critics.** Among the *thousands* of papers citing A, keep only those that both **engage A repeatedly** (`contextcount ≥ 3`) and **dispute it** (`disagreement = true`). Most citations satisfy neither, so this is a hard cut.
3. **Rank by reach.** Order the survivors by `citationcount`, with `contextcount` as tie-breaker: the focus signal has done its work in the gate (stage 2); the ranking asks only how widely the critic itself is received.

Run on Kaplan, stage 3 returns **Hoffmann at rank 1 and DeepSeek at rank 3** — not because anyone curated them, but because each references Kaplan *many times* (`contextcount` 10 and 7) *and* does so to *find a flaw* (`disagreement = true`). Out of ~3,000 papers citing Kaplan, the algorithm elevates the field's canonical corrector (Hoffmann, B-novel) and a later re-optimizer (DeepSeek, C); §4.4 checks this output against the encyclopedia's canon and marks where it holds and where it does not. The procedure is deterministic given the encoder and the stance labels; §4.3 shows the funnel numerically.

The chain, however, spans **two anchors**. Kaplan's critics yield Hoffmann *and* DeepSeek — both cite and dispute Kaplan. But the auditor **Besiroglu does not cite Kaplan at all** (no edge in the graph); it disputes *Hoffmann* (`contextcount = 10`). So Besiroglu cannot appear in Kaplan's list; it surfaces only when the same two scores are **re-applied with Hoffmann as the new seed**. The four-node chain is therefore a *traversal with re-anchoring* — Kaplan → {Hoffmann, DeepSeek}, then re-seed on Hoffmann → {Besiroglu} — not a single ranking (§4.5).

### 4.3 The scoring funnel: monitoring all papers, not querying for one

The autonomous system does not begin with a query. It **watches the whole corpus** and lets an A→B pair *emerge*: a paper that crosses the landmark bar (a *Kaplan-like* A), then a qualified paper that disputes it (a *Hoffmann-like* B). Semantic retrieval (§4.2) is only how a human inspects a *chosen* seed; the monitor's start is the full 314,690-paper pool. So framed, the chain is the output of a funnel over everything:

| Stage | Filter (score / gate) | Pool |
|---|---|---|
| start | monitor every paper | **314,690** |
| ① landmark-candidate detection | reception `≥ θ_A` (`citationcount ≥ 1000`; prospectively, velocity above the field, §5.5) | **326** landmark candidates — Kaplan among them |
| — | take one candidate, A = Kaplan → its citers | **3,031** papers cite Kaplan |
| ② discourse gate | edge *analyzed* **∧** `disagreement = true` **∧** `contextcount ≥ 3` | 3,031 → *322 analyzed (10.6 %)* → **28** qualified critics |
| ③ salience rank | `citationcount` (reach; `contextcount` as tie-breaker) | **Hoffmann #1**, Henighan #2, **DeepSeek #3** |

The system is never *told* to look at Kaplan: Kaplan surfaces itself by crossing ①, and Hoffmann surfaces by crossing ②–③. Two of the cuts do the real work, and both are bibliometric, not semantic:

- **The discourse gate ② is the hard filter — but for two entangled reasons, and one is a limitation, not a virtue.** The 3,031 → 28 collapse decomposes: only **322 (10.6 %)** of Kaplan's citers were ever *analyzed* by the discourse pass at all; of those, **36 (11.2 % of analyzed)** carry `disagreement = true`; `contextcount ≥ 3` leaves 32, and the in-corpus reception the ranking needs leaves **28**. So the ~100× cut is **coverage × rarity, not rarity alone** — roughly a 10× factor is simply that ~89 % of citers were never labeled (§4.5, §5.3). Read correctly, the base rate is disagreement per *analyzed* edge — **5.2 % globally, 11.2 % for Kaplan** — not per all edges, since ~84 % were never examined at all: uncommon-but-not-vanishing *where the field actually looks*. Two honest consequences follow: the gate is blind to any dispute that was never analyzed, and analysis is itself biased toward prominent papers (label rate climbs 5.6 % → 30.9 % with the cited paper's citation count, §5.3), so the method preferentially surfaces *prominent* disputes. Where disagreement *is* labeled, though, it is genuinely engaged — only **1.7 %** of disagreement edges are single-context versus **60.5 %** across all edges, and `cc ≥ 3` keeps 74.9 % of them; that part of the filter is clean.
- **The salience rank ③ orders what survives** by reach — `citationcount`, with `contextcount` as tie-breaker; focus has done its work in gate ②. Hoffmann tops it (1,571 citations) over Henighan (345); DeepSeek (181) takes rank 3, ahead of more focused but narrowly received critics such as *Unified Scaling Laws for Routed Language Models* (148).

So **Kaplan → Hoffmann → DeepSeek is A (①) → B (③#1) → C (③#3) of a deterministic cascade** — no theme-clustering, no LLM in the ranking, no query. The connection between the three papers, invisible in a 314,690-row table, is surfaced by monitoring plus three scores. (Henighan sits at #2 on a *different* theme; §5.2 returns to that.) A second, sharper reason than theme: Henighan is not an *external* critic at all — [1] and [2] share their core authors (Kaplan, Henighan), so the labeled disagreement is a self-refinement by A's own team. Simmel's triad requires distinct actors; the gate should add an author-disjointness filter (`authors(A) ∩ authors(B) = ∅`), deterministically checkable, which would sort Henighan out as a matter of course.

One caveat frames everything that follows: stage ① and the salience score ③ read *lifetime* citation counts, **frozen at the ~January 2025 snapshot**. So this cascade is **retrospective** — it reconstructs a finished episode from hindsight, when the papers are already famous. It shows the *shape* of the chain, not *when* the monitor would have fired. §5.5 swaps lifetime counts for citation **velocity** to ask the prospective question: how early could a live monitor have detected the same chain — the Kaplan-like A, then the Hoffmann-like B?

### 4.4 The filters recover the field's canonical spine

Does this scoring *manufacture* a connection or *find* a real one? The external check is Wikipedia's *Neural scaling law* article [10], which independently canonizes exactly **Kaplan [1] → Hoffmann/Chinchilla [3] → Besiroglu [4]** — discussing all three with their competing exponents (Kaplan `N_opt ∝ C^0.73`; Chinchilla `α=0.34, β=0.28, N_opt ∝ C^0.5`; Besiroglu's revised `α=0.35, β=0.37`). That is precisely the **A → B-novel → B-audit spine** of our chain, recovered by the filters with no tool in the loop. Strong evidence the scores track real relevance rather than inventing links — and it is what licenses applying the same scores *prospectively*.

**C is where the tool and the encyclopedia diverge — and the divergence is instructive.** DeepSeek is not in that article, but the disagreement is real in the data: `DeepSeek → Kaplan` is a *labeled* disagreement over **7 distinct in-text locations** (`contextcount = 7`) — a substantive engagement the algorithm did not invent. The gap is one of **lens, not fact**. Wikipedia organizes scaling laws by the *fit lineage* — the `L = A/N^α + B/D^β` parametric model and its exponents — a thread on which Kaplan, Chinchilla, and Besiroglu form a closed line and DeepSeek's contribution (the non-embedding-FLOPs *measure*) sits on a different axis. The algorithm organizes by *discourse* — who substantively disputes whom — and on that axis DeepSeek plainly belongs. So the encyclopedia's omission is not evidence that the link is spurious; it is a case of a discourse connection that a topic-lineage narrative does not track. That is closer to the tool's *point* than to its failure: surfacing real disputes the canonical framing overlooks. The honest residual is only that "belongs by discourse" and "canonized as a fit-lineage landmark" are different senses of belonging — we claim the first for C, and note the field has not (yet) granted the second.

*Honest scope.* This is one well-known case; that filter output coincides with the encyclopedia's spine is compelling here but is itself the hypothesis a broader, multi-field evaluation would have to test.

### 4.5 The labels in the data — and where the coverage gap bites

Underneath that ranking the sentiment labels are only partial. We verified the four-node chain edge-by-edge against the graph:

| Edge | in-text `contextcount` | sentiment label |
|---|---:|---|
| Kaplan → Hoffmann | 10 | **disagreement = true** |
| DeepSeek → Kaplan | 7 | **disagreement = true** |
| DeepSeek → Hoffmann | 7 | none (unlabeled) |
| **Besiroglu → Hoffmann** | **10** | **none (unlabeled)** |
| Besiroglu → Kaplan | — | **no edge** (re-anchoring required, §4.2) |

The *structural* chain is complete and its `contextcount` gate is deterministic — every edge that exists is present with its in-text weight, and the strong engagement (cc = 10) of the audit edge Besiroglu→Hoffmann is plainly visible. The last row is the reason the chain needs re-anchoring: with *no* Besiroglu→Kaplan edge, the auditor is invisible from the Kaplan seed and only appears once Hoffmann becomes the seed. But the discourse layer (an ingest-time LLM pass) annotated only ~16 % of edges (§5.3) and **never labeled the pivotal B-audit edge** despite its cc = 10. This is the method in microcosm: deterministic bibliometrics surface the skeleton, the ranking, and the gate; the targeted classifier must then be *run on the high-contextcount unlabeled edges* to complete the labels. "Unlabeled" means "not yet analyzed," not "no critique" — Besiroglu is emphatically a critique.

### 4.6 A Markov formulation of the reference chain (extension)

The greedy traversal of §4.2 — take the top disputer, then re-anchor — invites a cleaner formalization as a **Markov chain on the discourse graph**. Let states be papers, and let the transition probability from a paper *p* to a critic *q* be its normalized reach weight (`citationcount`) over *p*'s qualified disputers:

> P(*p* → *q*) = [contextcount(*q*→*p*) · citationcount(*q*)] ⁄ Σ over *p*'s qualified disputers, for *q* disputing *p* (`disagreement`, `cc ≥ 3`).

A random walk under P "steps to whoever most substantively disputes where it currently stands," and the implied reference chain is a **high-probability path** of this walk. Three things the greedy version handles by hand fall out natively:

- **Re-anchoring becomes automatic.** The walk crosses Kaplan → Hoffmann → Besiroglu with no hand-coded re-seed; the missing Besiroglu→Kaplan edge is simply a zero-probability transition, while the two-hop Kaplan → Hoffmann → Besiroglu carries mass.
- **Multi-step influence aggregates.** A paper reachable by several disagreement hops (DeepSeek disputes *both* Kaplan and Hoffmann) accumulates probability from every route rather than being pinned to one anchor.
- **The open frontier is a set of near-absorbing states.** Papers with no qualified disputers *yet* leak little probability onward — they are where the walk pools, i.e. the candidate-C / entry region a prospective system should watch.

We flag this as a modeling direction; the results here use the deterministic traversal, which suffices to exhibit the chain. A Markov treatment would matter most *prospectively* — ranking many partially-overlapping dispute paths across a whole field at once.

### 4.7 Models used

| Stage | Model | Purpose |
|---|---|---|
| Embedding / retrieval | `all-MiniLM-L6-v2` [6] (384-dim) | semantic similarity over the corpus |
| In-text stance at ingest | **`gpt-4o-mini`** (OpenAI), via the **Batch API**, JSON mode, temperature 0.1 | per-edge `agreement` / `disagreement` booleans + summaries |
| Theme clustering; per-context type | `claude-opus-4-8` | grouping critics by theme; CRITICAL/SUPPORTIVE/NEUTRAL per in-text context |

Note that the selective, prominence-biased coverage of §4.3/§5.3 is a property of *this ingest run* — which `(cited paper, citing quote)` pairs were placed into the Batch input — **not of `gpt-4o-mini` itself.** The 84 % of edges that carry no stance were simply never submitted to the batch, not judged neutral by the model. A more complete labeling is therefore purely a matter of re-running the same batch over the unlabeled high-`contextcount` edges (§4.5), at `gpt-4o-mini` batch pricing.

---

## 5. Signal thresholds: when they fire and why they are the starting gun

### 5.1 The gate

A critique edge B→A is admitted only if `disagreement = true`, reception `R(A) ≥ θ_A`, `R(B) ≥ θ_R`, and engagement `contextcount ≥ θ_C`. Thresholds are **absolute, not relative**, so "is this already a signal?" is comparable across the corpus and across time — the property that lets *early-but-solid* critiques fire. Calibrating on `papers.citationcount` gives percentiles **p90 = 36, p95 = 68, p99 = 223**; we set `θ_A = 1000`, `θ_R = 300` (both deep in the tail), `θ_C = 3` (retains 74.9 % of disagreement edges; fallback `θ_C = 2` retains 98.3 %).

Two further gates, from §5.4: a **type gate** (admit only `conceptual_correction` / `scope_limitation`, never `benchmark_superiority`) and a cheap **genre pre-filter** on A's title+abstract. Both are negative screens; neither replaces the disagreement signal.

### 5.2 Selecting B: which ranking surfaces Hoffmann?

Among A's qualified critics, which becomes B? The choice of ranking matters, and it is instructive that *two* deterministic rankings already work while a third, tempting one fails:

- **The reach ranking (`citationcount`, `contextcount` as tie-breaker)** — the stage-3 ranking (§4.3) — puts **Hoffmann first** (1,571) and DeepSeek third (181). The chain falls straight out; no clustering needed.
- **A naïve time selector** ("earliest qualified critic becomes B") *fails*: it returns Henighan et al. [2] (2020, aspect-ratio), because a landmark is attacked on several distinct themes and the globally-earliest critique is a narrow refinement on a *side* theme.

So theme-clustering is **not required to surface Hoffmann in this case** — the product ranking suffices. Its value is twofold and *prospective*: (i) it separates the *allocation* conversation (Hoffmann #1, DeepSeek #3) from Henighan's unrelated *aspect-ratio* critique sitting between them, so the chain is read as one theme rather than three; and (ii) it swaps lifetime `citationcount` for **velocity** (age-normalized reception), the signal a *live* system needs before lifetime counts exist:

| Date | Critic of Kaplan | velocity (/yr, ref 2025-01-01) | theme |
|---|---|---:|---|
| 2022-03-29 | **Hoffmann / Chinchilla** | **569** | compute/token allocation |
| 2024-01-05 | DeepSeek | 183 | compute/token allocation |
| 2020-10-28 | Henighan (earliest overall) | 83 | aspect-ratio |

The allocation theme is the most contested (~10 of Kaplan's 28 qualified critics) and the fastest, so under either product-of-reach (retrospective) or theme×velocity (prospective) Hoffmann leads — and only the pure time selector is fooled.

### 5.3 Disagreement is rare and selectively labeled

Disagreement is a *needle* — but the right denominator matters (§4.3). **For cost reasons, the ingest batch (§4.7) did not label the whole graph:** only the relationships of papers carrying at least a minimum citation footprint were submitted, so of 4.3 M edges just **15.8 % (680,392) were ever analyzed**; 35,389 of those carry `disagreement = true` — **5.2 % of *analyzed* edges** (11.2 % for Kaplan), the honest base rate. The unlabeled ~84 % default to no stance without ever having been examined. Because the batch was weighted toward well-cited papers, the label rate climbs with the cited paper's citation count (5.6 % under 10 cites → 30.9 % over 1000) and with engagement (`contextcount` 1 → 10+: 1.5 % → 42.1 %) — coverage is not random but *prominence-biased*. The operational consequence, recurring throughout: a *missing* label usually means "never analyzed," not "no critique" (cf. Besiroglu→Hoffmann, §4.5), and the method sees only the analyzed slice. We treat coverage as a **confidence discount**, and flag the prominence bias as a limitation (§9).

### 5.4 The type gate: conceptual correction, not benchmark superiority

Citation count — even velocity — conflates *conceptual* novelty (a contestable claim) with *artifact* novelty (a survey, benchmark, toolkit, or model release cited by adoption). And the disagreement signal does **not** auto-filter genres: artifact releases attract qualified disagreement at rates *equal to or above* conceptual landmarks —

| Paper | citations | disagreements (`cc ≥ 3`) | per 1k citations |
|---|---:|---:|---:|
| GPT-3 (conceptual+artifact) | 34,493 | 369 | 10.7 |
| Kaplan (conceptual) | 3,567 | 32 | 9.0 |
| LLaMA (artifact) | 9,681 | 109 | 11.3 |
| GPT-4 Technical Report (artifact) | 9,377 | 156 | 16.6 |

— because being the SOTA baseline invites contest. But the *type* differs: LLaMA's disagreements read "model X outperforms LLaMA on benchmark Y" (a ranking race); Kaplan's read "the power-law values are wrong" (a correction of the mechanism). The single `disagreement` boolean conflates them, so a **type label** — `{conceptual_correction, scope_limitation, benchmark_superiority}` — is load-bearing: only the first two open an A→B→C dialectic. (Crude title-regex genre filtering is too leaky — `"A Framework for …"` tags method papers — so genre screening needs a semantic classifier, not patterns; among 218 correctors, genre papers appear at 9.6 %, ≈ the 11.0 % baseline, i.e. *no* self-filtering on the issuing side either.)

### 5.5 From retrospective chain to earliest entry: the velocity reformulation

The chain of §4 is **retrospective**: its salience rank (`citationcount`, `contextcount` as tie-breaker) reads *lifetime* citation counts frozen at the January 2025 snapshot. Looking back from 2025, the papers are already canonical — the cascade shows the *shape* of a finished episode, not *when* to act. The operational question is the opposite: **what is the earliest moment an AI scientist should be sent into the field?**

Replace lifetime counts with citation **velocity** — citations per unit time — and the static gate becomes a *temporal* one:

- **Landmark-candidate condition on A (necessary, not sufficient).** A is a landmark *candidate* from the first moment its citation velocity exceeds the field's — a high percentile of its contemporaries. Being cited *faster than peers per unit time* is the necessary early sign; it does not yet guarantee a landmark (the paper may still fizzle). This makes the question precise: *from when* did Kaplan clear that bar? That timestamp **t_A** is when Kaplan first *looks* like a landmark — potentially years before its lifetime count makes the status obvious.
- **The same measure on B.** From when does Hoffmann's velocity clear the qualified-critic bar while its conceptual disagreement with Kaplan registers? Call it **t_B**.
- **Earliest entry ≈ t_B.** Not A's publication (t_A is a candidate signal only — the direction is still speculative), and not the 2025 hindsight view — but the first moment a velocity-qualified landmark has been met by a velocity-qualified, conceptually-disagreeing critic. That is when the direction is *de-risked in real time* (§3.1): the oracle now exists, and verifiable work — audit, optimization — becomes possible. This is the true **starting gun**; A's publication is not.

**What this requires, honestly.** Velocity as a *rate* needs time-resolved citation histories — citations within the first *k* years — whereas the January 2025 snapshot carries a single *lifetime* count per paper. The velocities in §5.2 (`citationcount / age`) are therefore a coarse proxy, and t_A, t_B cannot be pinned down from this dump alone. So the velocity reformulation is stated as the method's **live form**; backtesting *when* the gun would have fired needs longitudinal citation data (e.g. Semantic Scholar's per-year counts) and is future work. What the snapshot does establish is the retrospective chain plus one suggestive fact: even age-normalized, Hoffmann's velocity dominates all of Kaplan's critics (§5.2) — a hint that the prospective signal would indeed have fired early.

---

## 6. What is in reach of an AI scientist — and what is not

Two axes decide reachability: **does an oracle exist at the time?** and **does the move need resources the agent lacks?** Compute clusters are scarce and expensive; existing datasets and published results are cheap.

| Paper | Role | Oracle at the time? | Resource demand | In reach? |
|---|---|---|---|---|
| Kaplan | A | No — postulates the frame | moderate compute | **No** — needs taste, no verifier |
| Hoffmann | B-novel | No — resolves years later | **400+ models — a large cluster** | **No** — speculative *and* compute-bound |
| Besiroglu | B-audit | Yes — Hoffmann's own data | **a laptop** (re-analysis) | **Yes** — cheap, verifiable |
| DeepSeek | C | Yes — existing loss curves | moderate (search + verify) | **Yes\*** — verifiable; *caveat §3.2* |

- **Kaplan (A) is out of reach.** No oracle: the value of "loss is predictable from compute" could not be checked until the field built the apparatus to check it. This is the human-shaped act of *taste* — betting on an undecided question.
- **Hoffmann (B-novel) is doubly out of reach.** It is speculative (the allocation claim resolved only later — and was itself faulted, see below), *and* it demanded training 400+ models at scale — empirical compute the agent does not command. New-experiment correction is the most expensive and riskiest role.
- **Besiroglu (B-audit) is the best fit.** It re-analyzed Chinchilla's *published* data on commodity hardware and found a statistical flaw — pure interpolation over existing numbers, immediately checkable. Auditing landmark results at scale is exactly what a tireless, broad agent is good at, and the input (datasets, reported fits) is cheap.
- **DeepSeek (C) is in reach, with the §3.2 caveat.** Its contribution is verifiable against the existing yardstick, and its creative choice is reachable by search × verification *if* the measure space is searchable; for a non-searchable architectural leap, it slides toward A.

**Empirical support for "B-novel is risky."** Across 218 "correctors" (papers issuing a qualified disagreement at a landmark) vs. 1,818 similarly-cited non-correctors, correctors are themselves corrected **86.2 %** vs. 81.0 % of the time, and attract **~23 % more disagreement per citation**. Hoffmann is a case in point: it is the target of 7 qualified disagreements, and Besiroglu's audit is one of them. *The corrector gets corrected* — which is why the speculative correction is the role to avoid, and the audit the role to occupy.

---

## 7. Outlook: a landscape where AI takes C and B-audit

Suppose automated agents reliably occupy the two verifiable roles. Four dynamics follow.

1. **Audit becomes continuous and instantaneous.** Every landmark is re-derived against its own data as it appears. Errors like Chinchilla's fit surface in weeks, not the two years it took Besiroglu. The field spends less time building on wrong formulas; the *cost of being wrong in public* rises sharply.
2. **Optimization windows compress.** The tertius advantage — entering a de-risked frame before the obvious player — erodes when an agent harvests every window the instant B crosses the gate. Returns to a *single* C collapse toward the competitive frontier; the moat migrates from the idea to **speed and monitoring infrastructure**.
3. **The division of labor sharpens along the verifiable/speculative seam.** Machines own interpolation (audit + optimize); humans are pushed toward extrapolation — opening directions (A) and staking new experimental claims (B-novel), the roles that need taste and large compute. The bottleneck *inverts*: verifiable optimization becomes abundant and cheap, so the scarce, valuable input becomes **original direction-setting**.
4. **A self-correcting equilibrium.** If audit is free, speculative claims are pressure-tested at once — discouraging sloppy B-novel, rewarding solid A. If optimization is free and crowded, the prize drifts back to whoever opens the *next* direction. The economy of science re-prices human originality upward precisely because the verifiable work has been automated away.

The risk worth naming: an agent ecosystem that audits and optimizes brilliantly but cannot open directions would, at the limit, polish an ever-finer set of *existing* frames while the supply of new frames depends entirely on humans. Abundance of C is not a substitute for scarcity of A.

---

## 8. Coda: does *this* paper have landmark quality?

The framework turns on itself. This paper is an **A-type act**: it postulates a frame (the verifiable/speculative axis; the four-role reading of scientific progress) for which **no oracle exists today.** Its central claims are not checkable against the present record — they are a wager on undecided terrain. By its own thesis, that makes it *speculative novelty*, the one thing an automated scientist could not have produced and could not now certify.

So: is it a landmark? By the very structure it proposes, the paper **cannot answer.** It becomes one only if (a) it receives reception, and (b) at least one human takes the role of **B-novel** — confirming-and-correcting it with the new argument or evidence the paper itself lacks (after which a B-audit might re-check that correction, and a C operationalize the method). And — this is the honest, unavoidable point — **whether that happens cannot be predicted**, because there is no verifier for an A at the moment of the act. The paper manufactures no certainty about itself; only the field, later, can.

And the test is not even clean — which is where honesty must end. **Reception is confounded by brand.** Kaplan carried OpenAI, Chinchilla carried Google DeepMind, DeepSeek carried DeepSeek: each arrived with institutional recognition and the presumption of elite, highly-selected expertise that *pre-paves* citation independent of content. The signals this method trusts — citation count, velocity — therefore measure quality *entangled with* prestige, and the very landmarks it validates against were pre-selected in part by brand. This paper carries no such brand. So if it goes uncited, the cause is genuinely ambiguous: low quality, or merely the absence of the precondition every paper in the chain enjoyed. And the ambiguity is **asymmetric — the reasons a paper is *not* received are far more numerous than the reasons it is** (obscurity, wrong venue, no network, poor timing, no brand — and, yes, low quality), whereas strong reception concentrates on a few (real merit, amplified by prestige). Non-reception is thus weak evidence of anything; strong reception is the more informative event. The reflexive test the framework proposes is, by this token, biased against exactly the kind of unbranded A-act this paper is.

Which is the whole argument, reflexively: had an AI been able to write this, it would not be a landmark. That it required a speculative leap is exactly what places it beyond the agent's reach — and in the reader's, to corroborate or refute.

---

## 9. Limitations

1. **Selective, prominence-biased coverage (§4.3, §5.3).** Only 15.8 % of edges were ever analyzed, so an absent label usually means "never analyzed," not "no critique" (Besiroglu→Hoffmann, cc = 10, is the cautionary case). The batch was restricted for cost to papers with a minimum citation footprint (§5.3), with two effects: (i) the funnel's reduction is *coverage × rarity*, and the honest disagreement rate is 5.2 % of *analyzed* edges, not of all edges; (ii) analysis is biased toward prominent cited papers (label rate 5.6 % → 30.9 % with citation count), so the method preferentially surfaces *prominent* disputes and can miss substantive ones on less-cited work. Coverage is a confidence discount, not a guarantee.
2. **Live C-detection is a bet.** The method asserts the *absence* of a resolver; only time confirms it. The backtest validates the concept, not each prospective call.
3. **Lifetime vs. early-window citations (§5.5).** The extracted chain uses lifetime citation counts at the Jan-2025 snapshot, so it is retrospective; the prospective, velocity-based form that would time entry (t_A, t_B) needs first-`k`-year citation histories the snapshot lacks. Backtesting *when* the gun fires is future work.
4. **A single disagreement boolean (§5.4).** It separates neither confirming-corrector from total-rejecter nor conceptual-correction from benchmark-superiority. `scripts/classify_disagreement_contexts.py` prototypes the per-context remedy; a summary-level type dimension extends it.
5. **Genre confounders are not auto-filtered.** Citation/velocity signals admit surveys, benchmarks, toolkits, and model releases on both the A and B sides; the method depends on an added semantic genre pre-filter and the type gate, both untested at scale here.
6. **Searchability assumption (§3.2).** The "C is in reach" claim holds only where the optimization space is searchable enough for an oracle to find the hit.
7. **Reception is confounded by institutional brand (§8).** Citation count and velocity — the method's landmark signals — entangle intrinsic quality with the prestige of the authoring institution (OpenAI, DeepMind, DeepSeek in our chain), which pre-paves citation. The method cannot separate the two, so it will systematically over-rank branded work and under-detect equally-good unbranded work. Non-reception is a weak, many-caused signal and must not be read as low quality.

---

## 10. Data & code availability (reproducibility)

```
tertius-gaudens/
├── PAPER.md                     # this paper
├── README.md                    # setup, provenance, exact invocations
├── data/
│   ├── top100.json              # 100 ranked A→B triads (gate output)
│   └── kaplan_critics.json      # all 28 qualified critics of Kaplan + summaries
└── scripts/                     # read-only against the source graph
    ├── poc_research_ideas.py    # gate + selector (top100 / validate / calibrate)
    ├── diag_contextcount.py     # §4.3 / §5.3 rarity & context-count distributions
    ├── classify_disagreement_contexts.py  # §5.4 per-context CRITICAL/SUPPORTIVE/NEUTRAL
    └── show_disagreeing.py      # inspect the disagreeing set for any paper
```

Every quantitative claim is reproducible: §4.3/§5.3 from `diag_contextcount.py`; §5.1 calibration and §5.2 triads from `poc_research_ideas.py`; the velocity tables from `data/kaplan_critics.json`; the §4.5 chain edges and §6 corrector statistics from direct read-only queries (documented in `README.md`). The graph derives from public sources (arXiv metadata; Semantic Scholar citation graph with in-text contexts); the discourse layer was generated by the models in §4.7.

---

### References

[1] J. Kaplan, S. McCandlish, T. Henighan, et al., "Scaling Laws for Neural Language Models," arXiv:2001.08361 [cs.LG], 2020.

[2] T. Henighan, J. Kaplan, M. Katz, et al., "Scaling Laws for Autoregressive Generative Modeling," arXiv:2010.14701 [cs.LG], 2020.

[3] J. Hoffmann, S. Borgeaud, A. Mensch, et al., "Training Compute-Optimal Large Language Models," arXiv:2203.15556 [cs.CL], 2022.

[4] T. Besiroglu, E. Erdil, M. Barnett, and J. You, "Chinchilla Scaling: A Replication Attempt," arXiv:2404.10102 [cs.LG], 2024.

[5] DeepSeek-AI, "DeepSeek LLM: Scaling Open-Source Language Models with Longtermism," arXiv:2401.02954 [cs.CL], 2024.

[6] W. Wang, F. Wei, L. Dong, et al., "MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers," arXiv:2002.10957 [cs.CL], 2020.

[7] R. Kinney, C. Anastasiades, R. Authur, et al., "The Semantic Scholar Open Data Platform," arXiv:2301.10140 [cs.DL], 2023.

[8] G. Simmel, *Soziologie: Untersuchungen über die Formen der Vergesellschaftung.* Duncker & Humblot, 1908.

[9] R. S. Burt, *Structural Holes: The Social Structure of Competition.* Harvard University Press, 1992.

[10] "Neural scaling law," Wikipedia. https://en.wikipedia.org/wiki/Neural_scaling_law (accessed 2026).

[11] C. Lu et al., "Towards end-to-end automation of AI research" (The AI Scientist), *Nature*, vol. 651, no. 8107, pp. 914–919, 2026. doi:10.1038/s41586-026-10265-5.

[12] A. Karpathy, interview, *Lex Fridman Podcast* #333, "Tesla AI, Self-Driving, Optimus, Aliens, and AGI," 2022 (arXiv segment ≈ 2:36:37).

---

[^arxiv]: **Why AI-on-arXiv is a particularly apt arena.** Karpathy [12] frames arXiv less as a website than as a publication *model*: one uploads, and within minutes the community reads, tweets, and cites — bypassing the months-long journal loop, while an arXiv paper still carries a semi-official weight a blog post does not. Two features of that model make AI an unusually good fit for this method. **Verifiability** — machine-learning results are cheap to reproduce, so a claim uploaded today is tried by others tomorrow, who become its arbiter; community review is fast and empirical, and the field moves accordingly. That is exactly the *oracle* precondition (§3.2) that makes the verifiable roles — B-audit and C — automatable, and it holds far better in AI than in fields where reproduction is slow or costly. **Cumulativeness** — Karpathy's image of scientific papers as small, fast "blockchains," each building on and disputing its predecessors — is precisely the dense, current dispute record the method reads. (His aside that prestige venues slow the field — conference work is "three generations" old, and *Nature* releases details a year late — sits pointedly beside our own *Nature* reference [11] and the brand caveat of §8.)
