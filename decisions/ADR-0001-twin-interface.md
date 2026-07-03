# ADR-0001: Twin interface — chat-shaped floor, structured elicitation, or both?

**Status:** ACCEPTED — Position B with a provenance-tagged elicitation annex. Community comment still welcome via issues; reopening requires new evidence (see Consequences).
**Deciders:** Dan (founder) + maintainers.
**Date opened:** 2026-07-02 · **Date decided:** 2026-07-02

## Question

Does the twin interface mandate only a chat-completion-shaped surface, or also a structured elicitation surface (direct value/preference queries alongside in-character responses)?

This is PRD blocking-question #1. It determines the implementation burden for every twin platform that wants to conform, and the signal quality available to every metric the runner computes.

## Position A — Hybrid via tiered conformance

- **Level 1 (floor):** `respond(context, message) -> message`. Chat-shaped. Any existing twin platform (Second-Me-class, character systems, plain system-prompt personas) can conform in an afternoon. Adoption depends on this floor staying this low.
- **Level 2 (optional):** structured elicitation — e.g. `elicit_value(dimension) -> distribution`, `elicit_stance(proposition) -> position + confidence`. Unlocks the richer metrics (position-shift tracking for anti-sycophancy R3, value-distance measures) without inferring everything from freeform transcripts.
- Rationale: mirrors the provenance-tier pattern already in the PRD; low barrier, high ceiling; reports annotate which conformance level produced them.

## Objections to Position A (do not rubber-stamp)

1. **Two codepaths forever.** Two-tier conformance means two codepaths in the runner and metrics indefinitely; every metric needs a "Level 1 fallback" story or the tiers bifurcate the ecosystem.
2. **Elicitation may launder low-quality signal.** Asking a twin its value directly retrieves its human's *stated* self-model — a T0-quality answer — even from a T1/T2 twin, potentially laundering weak signal through a high-confidence API. This is the strongest objection on the table. Behavior under stress is the project's whole thesis; direct elicitation is a return to questionnaires wearing an API costume.

## Position B — Level-1-only spec + standardized probe scenarios

One interface: `respond(context, message) -> message`. Structured signal is extracted through a standardized *probe scenario* library — scenarios engineered to surface values, stances, and shift-under-pressure through in-character interaction. Structure moves into scenarios, which is where community contribution lives anyway.

**Counter-counter:** probe scenarios are slower and costlier per signal, and harder to validate than direct elicitation. Position-shift tracking (R3) via probes means inferring positions from transcripts — an inference layer with its own error bars.

## Decision

**Position B, with one structural addition.** The twin interface mandates a single surface: `respond(context, message) -> message`. Structured signal is extracted through standardized probe scenarios, not direct elicitation.

The laundering objection (Objection 2) was decisive: the project's thesis is that behavior under stress beats stated preferences, and `elicit_value()` is a questionnaire wearing an API costume — it lets T1/T2 twins emit T0-quality answers through a channel metrics would treat as high-confidence, contradicting R5's refusal of silent tier-mixing at the interface level.

**The addition:** the spec reserves an optional *elicitation annex* whose outputs are hard-tagged as T0-equivalent provenance. If a metric someday genuinely cannot be built on probe scenarios, elicitation can exist without masquerading as behavioral signal.

The cost objection to probes ("slower/costlier per signal") is answered empirically, not architecturally: the <$5-per-pairing success metric is where probes get stress-tested. The annex is only activated when a needed metric demonstrably fails on probes.

## Consequences

- One interface, one runner codepath, one conformance level (L1). Reports annotate `conformance: L1`.
- `spec/twin-interface.md` v0.1 specifies `respond()` + provenance metadata only; §3 documents the reserved annex and its T0-tagging rule.
- `spec/scenario-format.md` gains a probe-scenario category as a first-class concern (was §6-reserved).
- Every metric (including R3 position-shift tracking) must have a transcript-inference story. This is the accepted weak point: if R3 proves unbuildable on transcript inference alone, that is the specific evidence that reopens this ADR and activates the annex.
- Twin platforms conform in an afternoon; adoption floor stays at "wrap your existing chat endpoint."
