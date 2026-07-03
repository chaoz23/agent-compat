# ADR-0001: Twin interface — chat-shaped floor, structured elicitation, or both?

**Status:** OPEN — this is the live founding debate. Nothing in `spec/twin-interface.md` freezes until this resolves.
**Deciders:** Dan (founder) + maintainers; community comment invited.
**Date opened:** 2026-07-02

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

*Pending. To be argued with Dan in-session; positions recorded above so the debate is inheritable. The spec draft in `spec/twin-interface.md` evolves in the same PRs as this ADR.*

## Consequences

*Recorded when decided.*
