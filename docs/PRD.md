# agent-compat — Product Requirements Document

**Version:** 0.1 (Founding Draft)
**Status:** Open for comment — this document doubles as the project's core description
**License intent:** Apache 2.0 (spec + code), CC-BY-SA (scenario corpus)

---

## One-Line Description

An open framework for simulating compatibility between agents — pairing digital twins, running them through parameterized stress scenarios, and reporting *how the pairing behaves under pressure* rather than a single match score.

---

## A Note on Scope: The Narrow Wedge vs. The Broad Arc

This section exists because the gap between what this project *could* be and what v1 *must* be is enormous, and conflating them is the most likely way this project dies.

**The broad arc.** The long-term vision is a general utility-matching substrate for a world of agents: human↔human matching mediated by digital twins (romantic, cofounder, roommate, team), human↔agent matching (which assistant, coach, or tutor actually fits this person), and agent↔agent matching (which agents should be composed into a pipeline together). The deepest version of the human story: stable, well-matched relationships are load-bearing infrastructure for human flourishing. People in secure partnerships climb Maslow's hierarchy faster and further — they take bigger creative and entrepreneurial risks, recover from setbacks faster, and are more likely to pursue what Salim Ismail calls a Massive Transformative Purpose rather than spending their energy on relational churn and repair. If twin-mediated matching improves pairing quality even marginally at population scale, the second-order effect is a measurable increase in humans operating at the top of their hierarchy of needs. Dating apps optimized for engagement; this optimizes for *graduation* — people leaving the matching pool into durable pairings. That inversion is only possible in an open, non-monetized-by-swiping framework.

Additionally, twin-mediated matching removes the meat-suit bottleneck: humans can evaluate perhaps a handful of potential matches per month through dates; twins can evaluate thousands of pairings per hour through simulation, exploring a combined "local relationship multiverse" no human pair could ever traverse experientially. The human step moves from *search* to *verification of pre-screened, evidence-annotated candidates*.

**The narrow wedge.** None of that is buildable or credible as a v1, and a repo that claims it will attract tourists, not contributors. The wedge is deliberately unglamorous: **a spec and reference runner for pairwise agent compatibility simulation, with cofounder/collaborator matching as the flagship scenario pack.** Not dating. Dating is the most emotionally resonant application and precisely for that reason the worst place to start: highest privacy stakes, hardest ground truth, guaranteed press cynicism, and an "ick" factor that suppresses serious contribution. Cofounder/collaborator matching is the same primitive — two agents, stress scenarios, repair metrics — with lower stakes, faster ground-truth cycles (startups fail or don't within observable windows; YC has published extensively on cofounder conflict as a top startup killer), and a contributor population (developers) who are also the user population. Dating enters as a scenario pack in Phase 3, after the primitive is validated, arriving into a framework that already works rather than defining the project's identity.

**The rule for every scope debate:** if a proposed feature serves the broad arc but not the wedge, it goes in the parking lot (Appendix A), not the roadmap. The broad arc is the reason to care; the wedge is the thing we build.

---

## Problem Statement

Every existing matching system — dating platforms, cofounder matchers, team-assembly tools — matches on *stated* preferences (profiles, questionnaires) or *revealed* preferences (swipe/click behavior). Both are thin proxies. Decades of relationship research (Gottman et al.) and startup post-mortems (cofounder conflict as a leading cause of failure) converge on the same finding: compatibility is determined not by shared interests but by *behavior under stress* — conflict style, repair attempts, response to asymmetric bad luck. No existing system can observe this before the relationship exists.

Simultaneously, personal digital twins (Second-Me, Enchanted-Twin, character-persona systems) are proliferating, but there is no open standard for making two twins *interact diagnostically* — no shared scenario format, no interaction protocol, no scoring methodology, no calibration discipline. Anyone wanting twin-mediated compatibility today must build the entire stack bespoke, and the results are unfalsifiable.

The cost of not solving this: matching remains a proprietary, engagement-optimized, low-signal industry; the emerging twin ecosystem fragments into incompatible silos; and the highest-leverage application of personal AI — helping humans form better human bonds — is ceded by default to closed platforms with misaligned incentives.

---

## Goals

1. **Publish a spec others adopt.** Within 12 months, at least 2 external projects (twin platforms, matching products, research groups) consume or emit the agent-compat interchange formats. This is the OpenTimelineIO test: the spec, not the app, is the product.
2. **Prove the primitive beats the baseline.** Demonstrate, via the calibration harness, that stress-scenario simulation predicts real pairing outcomes (cofounder retention at 12 months, self-reported working-relationship quality at 90 days) better than questionnaire similarity scoring. Target: measurable, published lift over cosine-similarity-of-profiles baseline.
3. **Build a community-owned scenario corpus.** 100+ reviewed scenarios across at least 3 domains within the first year, with ≥30% authored by contributors outside the founding group — including non-programmers (researchers, therapists, experienced founders).
4. **Establish honest reporting as the norm.** Zero single-number compatibility scores anywhere in the framework. Every report ships distributions, friction points, and provenance-based confidence bounds. Success looks like downstream products inheriting this norm because the report format makes dishonesty harder than honesty.
5. **Keep the twin data sovereign.** Ship a reference "sealed runner" mode where two parties can run a compatibility simulation without either receiving the other's raw twin. Adoption of this mode by at least one privacy-focused twin platform validates the architecture.

---

## Non-Goals (v1)

1. **Building a dating app or any end-user product.** We build the engine and spec; products are downstream. Rationale: product ambitions fragment contributor focus and invite monetization conflicts before the primitive is proven.
2. **Building twin-creation tooling.** Twin construction (data ingestion, persona distillation, memory) is a crowded, well-funded space. We define what a twin must *expose* to be simulatable (the schema, forthcoming) and stay interoperable with existing twin builders. Rationale: don't compete with your suppliers.
3. **Romantic/dating scenario packs in v1.** Deferred to Phase 3 by design, not oversight. Rationale: see Scope Note above — the wedge must be validated in a lower-stakes domain first.
4. **Real-time human-in-the-loop simulation.** v1 is batch: submit two twins + scenario deck, receive a report. Interactive/streaming modes are P2. Rationale: batch is sufficient to prove predictive validity and 10x simpler.
5. **Any claim of clinical or psychological authority.** The framework produces *conversation material and evidence-annotated hypotheses*, never verdicts, diagnoses, or advice. Rationale: epistemic honesty is the moat; overclaiming destroys it and invites regulatory pain.
6. **Matching marketplaces or discovery.** Who gets simulated with whom is out of scope. We are the compatibility function, not the candidate generator. Rationale: discovery is where incentive corruption enters (pay-to-rank); keeping it out keeps the core neutral.

---

## Target Users & User Stories

**Persona A — Twin-platform developer** (builds Second-Me-style personal agents)
- As a twin-platform developer, I want a standard interface my twins can implement so that my users' twins can participate in compatibility simulations run by any conformant runner.
- As a twin-platform developer, I want a sealed-runner mode so that I can offer compatibility features without my users' twin data leaving trusted infrastructure.

**Persona B — Matching-product builder** (cofounder matcher, team-assembly tool, eventually dating)
- As a matching-product builder, I want to submit two twin descriptors and a scenario pack ID and receive a structured report so that I can build match-evaluation features without inventing simulation methodology.
- As a matching-product builder, I want provenance tiers surfaced in every report so that I can communicate confidence honestly to my users.

**Persona C — Scenario author** (researcher, therapist, experienced founder — may not code)
- As a scenario author, I want to contribute a stress scenario in a structured plain-text format so that my domain expertise improves simulation quality without me writing Python.
- As a scenario author, I want to see aggregate (anonymized) statistics on how my scenario discriminates between pairings so that I can refine it like a test author refines an exam question.

**Persona D — Researcher**
- As a computational social science researcher, I want a calibration harness with retrodiction support so that I can test whether simulated compatibility predicts real outcomes and publish falsifiable results.
- As a researcher, I want model-agnostic runners so that I can compare simulation validity across LLM backends and control for model-specific sycophancy.

**Persona E — End human (indirect, via Personas A/B)**
- As a person seeking a cofounder, I want to see *where* my twin and a candidate's twin deadlocked — with transcript evidence — so that I can have that exact conversation with the real human before committing.
- As a person, I want to run simulations against a hypothetical "improved me" twin so that I can see which of my own patterns most limit my pairings (the self-improvement loop — this story is what eventually generalizes to improving existing relationships, not just forming new ones).

---

## Requirements

### P0 — Must-Have (framework is not viable without these)

**R1. Interchange spec, v0.1** — Three documents: twin-interface (what a twin must expose: not the twin's internals, but a conformant *query surface* — respond-in-character, value-elicitation, provenance metadata), scenario-format (parameterized stress scenarios with phases, injected events, and termination conditions), report-format (structured output: per-scenario trajectories, friction points, repair metrics, distributions, provenance-weighted confidence).
- *Acceptance:* Two independently written twin stubs + the reference runner + one scenario produce a spec-conformant report. A third party can implement a conformant twin from the spec alone without reading runner source.

**R2. Reference runner (batch, model-agnostic)** — Executes a scenario deck against a twin pair. Pluggable LLM backend (local via Ollama-class, API via configurable endpoints). Deterministic seeding for reproducibility; N-run sampling for distribution estimation.
- *Acceptance:* Given two twins and a 10-scenario deck, produces a report with per-scenario outcome distributions over N≥50 runs; identical seeds reproduce identical trajectories on identical backends.

**R3. Anti-sycophancy instrumentation** — First-class metrics detecting artificial harmony: agreement-rate anomaly detection, position-shift tracking, "suspicious convergence" flags. Reports must display sycophancy diagnostics with the same prominence as compatibility findings.
- *Acceptance:* Runner correctly flags a control pairing of two maximally-agreeable stub twins as low-information; a validation suite of adversarial twin pairs produces expected diagnostic ranges.

**R4. Founding scenario pack: `collaboration/` (12–20 scenarios)** — Cofounder/collaborator stress scenarios: equity disagreement, vision divergence, unequal workload discovery, public failure attribution, acquisition-offer split, burnout asymmetry, credit disputes.
- *Acceptance:* Each scenario has parameterization, expected-discrimination documentation (what pattern differences it is designed to surface), and passes review by ≥2 maintainers.

**R5. Provenance tiers in schema and reports** — Every twin declares its evidence basis: T0 self-report/questionnaire, T1 conversational-corpus-derived, T2 behaviorally verified. Reports must render wider uncertainty for lower tiers and refuse silent tier-mixing.
- *Acceptance:* A T0×T0 pairing report visibly displays low-confidence framing; tier metadata survives round-trip through the full pipeline.

**R6. No-single-score report discipline** — The report format has *no field* for an overall compatibility number. Structural enforcement, not guideline.
- *Acceptance:* Schema validation rejects any report containing a top-level scalar compatibility score.

### P1 — Nice-to-Have (fast follows)

**R7. Sealed runner mode** — Both parties submit twins to an isolated runner; each receives only the report, never the counterpart twin. Reference implementation may start with process isolation + attestation stub, with a documented path to TEE (the Enchanted-Twin/Nitro-enclave pattern shows ecosystem precedent).
**R8. Calibration harness v1** — Retrodiction tooling: given twin pairs of *known-outcome* real relationships (consented research data or synthetic gold sets), measure predictive lift vs. profile-similarity baseline.
**R9. Scenario contribution pipeline** — Non-programmer-friendly authoring template (structured markdown), CI validation, and a scenario-quality dashboard (discrimination statistics per scenario).
**R10. Held-out scenario mechanism** — Support for private/rotating scenario subsets to resist Goodharting once twins are tuned against public scenarios.
**R11. `hiring-team/` and `roommate/` scenario packs** — Second and third domains to prove the primitive generalizes.

### P2 — Future Considerations (design for, don't build)

**R12. Romantic-relationship scenario pack** — The Phase 3 flagship. Requires: calibration methodology proven in lower-stakes domains, ethics review process established, partnership with relationship-research groups for scenario grounding.
**R13. Multi-agent (>2) compatibility** — Team assembly is N-way; keep the pair as the primitive but don't architecturally preclude N-way sessions.
**R14. Relationship-improvement mode** — Running an *existing* pair's twins to locate improvable friction (the "improve less compatible relationships" arc). Enormous human value, but requires the highest twin fidelity and the most careful framing.
**R15. Human↔agent matching** — Same machinery, one party is a product agent (tutor, coach, assistant). Likely the largest commercial adoption path; the spec should never assume both parties are human-derived.
**R16. Interactive/streaming simulation** — Human observes or intervenes mid-simulation.

---

## Success Metrics

**Leading (first 90 days post-publication)**
- Repo engagement: 20+ non-founder issues/PRs; 5+ substantive spec-discussion threads.
- First external conformant twin implementation (someone else's twin runs in our runner).
- 10+ community-contributed scenarios passing review.
- Reference runner completes a 50-run × 15-scenario pairing on a consumer GPU / mid-tier API budget (<$5 per full pairing at current token prices) — cost-per-pairing is the adoption gate for downstream products.

**Lagging (6–18 months)**
- Spec adoption: ≥2 external projects emitting/consuming agent-compat formats (Goal 1).
- Published calibration result: simulation-based prediction shows statistically significant lift over profile-similarity baseline on ≥1 real-outcome dataset (Goal 2).
- Corpus: 100+ scenarios, ≥30% external, ≥3 domains (Goal 3).
- One privacy-focused platform ships sealed-runner mode (Goal 5).
- Citation or use in ≥1 peer-reviewed study.

**Anti-metrics (things we refuse to optimize)**
- Simulations run per user (engagement). Twin-pool size. Anything resembling time-in-app. The graduation principle: downstream success is humans *leaving* matching processes into durable real-world pairings, and the framework's norms should make engagement-optimization awkward to build on top of it.

---

## Open Questions

**Blocking (resolve before v0.1 spec freeze)**
- *Spec/engineering:* Does the twin interface mandate a chat-completion-shaped API, or a richer structured elicitation surface (direct value/preference queries alongside in-character responses)? Richer = better metrics, higher implementation burden for twin platforms.
- *Engineering:* Sycophancy mitigation — is post-hoc detection (R3) sufficient for v1, or do we need runner-level countermeasures (adversarial system framing, position-anchoring) from day one?
- *Governance:* Scenario corpus licensing — CC-BY-SA proposed, but does share-alike deter commercial scenario contributions we want?

**Non-blocking (resolve during Phase 1–2)**
- *Research:* What is the minimum viable ground-truth dataset for calibration, and what consent framework does it require? (Candidate: consented retrospective cofounder pairs with known 12-month outcomes.)
- *Ethics/legal:* At what point does a compatibility report constitute a "consequential decision" under emerging AI regulation (EU AI Act risk tiers), and what does that imply for the report format's mandatory disclaimers?
- *Research:* How do we detect *twin drift* — a twin that no longer matches its human — and should staleness be a provenance dimension (T-tiers × freshness)?
- *Community:* Maintainer structure and decision rights once external contributors exceed founders — BDFL-with-spec-committee vs. early foundation-style governance?

---

## Timeline & Phasing

**Phase 0 — Founding (weeks 0–4):** This PRD published as the repo's core document. Spec drafts (twin-interface, scenario-format, report-format) opened as PRs for comment. Twin stubs + minimal runner skeleton. *Exit criterion:* one full toy pairing runs end-to-end.

**Phase 1 — Wedge (months 1–4):** P0 complete. `collaboration/` pack shipped. Anti-sycophancy suite validated. First external feedback cycle on spec. *Exit criterion:* R1–R6 acceptance criteria pass; ≥1 external person has implemented a conformant twin.

**Phase 2 — Credibility (months 4–9):** Calibration harness + first retrodiction study. Sealed runner reference. Second/third scenario domains. Scenario contribution pipeline with quality dashboard. *Exit criterion:* published baseline-lift result (even a negative one — a rigorous null result still establishes the framework as the venue for this question).

**Phase 3 — The resonant application (months 9+):** Romantic scenario pack development opens, gated on: Phase 2 calibration methodology proven, ethics review process in place, at least one research partnership for scenario grounding. Relationship-improvement mode (R14) enters design.

No hard external deadlines. The dependency to watch: calibration (Phase 2) depends on ground-truth data acquisition, which has the longest lead time — begin dataset conversations in Phase 1.

---

## Appendix A — Parking Lot (broad-arc ideas explicitly deferred)

Recorded so they stop relitigating scope: twin marketplaces and discovery; matchmaker-agent orchestration (agents that *propose* pairings); population-scale matching-graph analytics; longitudinal twin↔twin "check-in" simulations for existing couples; cross-cultural scenario localization; economic/negotiation compatibility for agent-to-agent commerce; integration with prediction markets on pairing outcomes (fun, deeply problematic, parked); "improved-self" counterfactual twin tooling beyond the basic user story in Persona E.

## Appendix B — Positioning vs. Prior Art

Industrial digital-twin frameworks (OpenTwins, OFacT) simulate physical systems, not persons; personal-twin projects (Second-Me, Enchanted-Twin) build and host twins but define no twin-to-twin diagnostic protocol; LLM-simulation research (multi-agent parametrization, SimBench-style benchmarks) validates that LLM-agent simulation methodology is publishable science but targets engineering systems. Dating incumbents (Match Group, Bumble) have publicly signaled AI-concierge directions but will build closed, engagement-optimized versions. agent-compat occupies the open middle layer none of them owns: the interchange spec and honest-reporting methodology for agent compatibility simulation. The closest analogy is OpenTimelineIO's position in editorial pipelines — unowned interchange between competing platforms is precisely what open source is structurally best at.

## Appendix C — Why This Matters (the human potential, kept out of the requirements on purpose)

The requirements above are deliberately dry. The reason to do the work is not. Relational stability is upstream of nearly everything humans care about: health outcomes, risk tolerance, creative output, longevity. The Harvard Study of Adult Development's core finding — relationship quality as the dominant predictor of flourishing — has never had an engineering response, only an app-industry response optimized for the opposite outcome. If twins can compress years of trial-and-error relational search into hours of honest simulation, and surface the three conversations a pair most needs to have before committing, the framework's downstream effect is measured in redirected human-years: time not spent in avoidable relational churn, available instead for whatever each person's larger purpose is. That is the broad arc. The wedge is a JSON schema, a scenario format, and a runner that refuses to flatter. Build the wedge.
