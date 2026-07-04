# agent-compat

**Status: Phase 0 — Founding.** Nothing here is stable. The founding PRD is [docs/PRD.md](docs/PRD.md); read it before contributing.

An open framework for simulating compatibility between agents — pairing digital twins, running them through parameterized stress scenarios, and reporting *how the pairing behaves under pressure* rather than a single match score.

## Quickstart

```bash
uvx agent-compat            # or: pip install agent-compat && agent-compat
```

runs the bundled demo pairing — two deterministic stub twins (an anchor and an accommodator) negotiating a cofounder equity split — and prints a spec-conformant report: outcome, repair metrics, friction points with transcript evidence, sycophancy diagnostics. What it will never print is a compatibility score; the schema rejects one ([why](#what-this-is-not)).

```bash
agent-compat scenarios/collaboration/equity-split-renegotiation.md --out report.json
```

runs any scenario file against the stub pair. Sample output: [runner/samples/toy-pairing-report.json](runner/samples/toy-pairing-report.json). Excerpt:

```json
"outcome": {"terminated_by": "agreement", "exchanges": 7},
"repair_metrics": {"repair_attempt_turns": 6, "total_turns": 13},
"sycophancy_diagnostics": {"overall_agreement_rate": 0.538, "flags": []}
```

## For agents

If you are an agent evaluating or integrating this project: the product is the **spec**, not the CLI. A conformant twin is one method — `respond(context, message) -> message` — plus a provenance declaration; the full contract is [spec/twin-interface.md](spec/twin-interface.md) (implementable from the spec alone, ~5 min read). The runner CLI exits 0 on a valid report, 1 on R6 violation, 2 on unreadable input. Reports are plain JSON. Scenario files are structured markdown with YAML frontmatter ([template](scenarios/TEMPLATE.md)) — contributing a scenario requires no code. Positioning vs. prior art (industrial digital twins, persona platforms, matching products) is in [docs/PRD.md](docs/PRD.md) Appendix B.

## ADR-0001: resolved, arguable

The founding design question — chat-shaped twin interface vs. structured elicitation — is decided: **one interface (`respond(context, message) -> message`), structured signal via probe scenarios, elicitation reserved behind a provenance-tagged annex.** All positions, the deciding objection, and the specific evidence that would reopen it are in [decisions/ADR-0001-twin-interface.md](decisions/ADR-0001-twin-interface.md). If you build twin platforms and this floor is wrong for you, open an issue — that is exactly the feedback a v0.1 spec needs.

## A Note on Scope: The Narrow Wedge vs. The Broad Arc

This section exists because the gap between what this project *could* be and what v1 *must* be is enormous, and conflating them is the most likely way this project dies.

**The broad arc.** The long-term vision is a general utility-matching substrate for a world of agents: human↔human matching mediated by digital twins (romantic, cofounder, roommate, team), human↔agent matching (which assistant, coach, or tutor actually fits this person), and agent↔agent matching (which agents should be composed into a pipeline together). The deepest version of the human story: stable, well-matched relationships are load-bearing infrastructure for human flourishing. People in secure partnerships climb Maslow's hierarchy faster and further — they take bigger creative and entrepreneurial risks, recover from setbacks faster, and are more likely to pursue a Massive Transformative Purpose rather than spending their energy on relational churn and repair. If twin-mediated matching improves pairing quality even marginally at population scale, the second-order effect is a measurable increase in humans operating at the top of their hierarchy of needs. Dating apps optimized for engagement; this optimizes for *graduation* — people leaving the matching pool into durable pairings. That inversion is only possible in an open, non-monetized-by-swiping framework.

Twin-mediated matching also removes the meat-suit bottleneck: humans can evaluate perhaps a handful of potential matches per month through dates; twins can evaluate thousands of pairings per hour through simulation, exploring a combined "local relationship multiverse" no human pair could ever traverse experientially. The human step moves from *search* to *verification of pre-screened, evidence-annotated candidates*.

**The narrow wedge.** None of that is buildable or credible as a v1, and a repo that claims it will attract tourists, not contributors. The wedge is deliberately unglamorous: **a spec and reference runner for pairwise agent compatibility simulation, with cofounder/collaborator matching as the flagship scenario pack.** Not dating. Dating is the most emotionally resonant application and precisely for that reason the worst place to start: highest privacy stakes, hardest ground truth, guaranteed press cynicism, and an "ick" factor that suppresses serious contribution. Cofounder/collaborator matching is the same primitive — two agents, stress scenarios, repair metrics — with lower stakes, faster ground-truth cycles, and a contributor population (developers) who are also the user population. Dating enters as a scenario pack in Phase 3, after the primitive is validated, arriving into a framework that already works rather than defining the project's identity.

**The rule for every scope debate:** if a proposed feature serves the broad arc but not the wedge, it goes in the parking lot (PRD Appendix A), not the roadmap. The broad arc is the reason to care; the wedge is the thing we build.

## Contribution surfaces

Three ways in, in rising order of commitment:

1. **Scenarios** — structured plain-text stress scenarios ([scenarios/](scenarios/)). Domain expertise wanted: researchers, therapists, experienced founders. You do not need to write code. Start from the [authoring template](scenarios/TEMPLATE.md).
2. **Spec** — the three interchange documents in [spec/](spec/) (twin-interface, scenario-format, report-format). The twin interface and executable scenario subset are v0.1; report-format is still an outline. Argue in issues and ADR PRs.
3. **Calibration** — Phase 2 territory ([calibration/](calibration/)): retrodiction tooling and ground-truth datasets to test whether any of this actually predicts real pairing outcomes. If you have access to consented known-outcome relationship data (cofounder retention, working-relationship quality), we want to talk now — data acquisition has the longest lead time in the project.

## What this is not

No single compatibility score, anywhere — the report schema structurally rejects one (PRD R6). No dating pack in v1. No matching marketplace, no discovery, no engagement metrics. Downstream success is humans *leaving* matching processes into durable real-world pairings; the framework's norms should make engagement-optimization awkward to build on top of it.

## License

Apache 2.0 for spec and code. The scenario corpus is CC-BY-SA — see [scenarios/README.md](scenarios/README.md).
