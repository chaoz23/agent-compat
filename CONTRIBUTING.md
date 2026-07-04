# Contributing

Three surfaces, in rising order of commitment. Read [docs/PRD.md](docs/PRD.md) — especially the Narrow Wedge vs. Broad Arc section — before proposing scope.

## 1. Scenarios (no code required)

Copy [scenarios/TEMPLATE.md](scenarios/TEMPLATE.md), write a stress scenario for the `collaboration/` domain, open a PR. The one hard requirement is the **Expected discrimination** section: what pattern differences is your scenario designed to surface? Scenarios are licensed CC-BY-SA 4.0 (see [scenarios/README.md](scenarios/README.md)). CI lints structure; two maintainer reviews accept (PRD R4). Domain experts — founders, researchers, therapists — are the intended authors.

## 2. Spec

The three interchange documents in [spec/](spec/). twin-interface and the
executable scenario-format subset are v0.1; report-format remains an outline
hardening now. Design arguments happen in ADR PRs against
[decisions/](decisions/); read ADR-0001 for the house style (all positions
recorded, including losing ones, plus the evidence that would reopen).

## 3. Runner and metrics

Python, stdlib-only so far. `pip install -e . pytest && python -m pytest runner/`. Two invariants are non-negotiable: reports must pass `runner/validate_report.py` (no single compatibility score, R6), and every metric must work from transcripts alone — there is no elicitation API (ADR-0001).

## Ground truth (special case)

If you have access to consented known-outcome pairing data (cofounder retention, working-relationship quality), open an issue regardless of project phase — data acquisition is the project's longest lead-time item.
