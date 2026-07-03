# Twin Interface Specification

**Version:** pre-0.1 — OUTLINE ONLY. Blocked on [ADR-0001](../decisions/ADR-0001-twin-interface.md); do not implement against this document yet.

Defines what a twin must *expose* to be simulatable — a conformant query surface, not the twin's internals (PRD R1, Non-Goal 2).

## 1. Scope and conformance

<!-- Conformance levels (if any) per ADR-0001 resolution. What "conformant twin" means; what a runner may assume. -->

## 2. The response surface

<!-- respond(context, message) -> message. Context envelope: scenario phase, injected events, conversation history. Statelessness/state expectations. -->

## 3. Structured elicitation surface

<!-- Existence and shape depend entirely on ADR-0001. Placeholder for elicit_value / elicit_stance or removal note. -->

## 4. Provenance metadata (R5)

<!-- Mandatory declaration: T0 self-report | T1 conversational-corpus-derived | T2 behaviorally verified. Freshness/drift fields (open question, non-blocking). -->

## 5. Identity, versioning, and descriptors

<!-- Twin descriptor format: how a runner addresses a twin without receiving its internals. Sealed-runner (R7) implications noted, not specified. -->

## 6. Error handling and refusals

<!-- What a twin may refuse; how refusals are reported rather than hidden. -->
