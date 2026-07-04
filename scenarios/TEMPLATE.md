---
id: domain/short-slug            # e.g. collaboration/equity-renegotiation
domain: collaboration
version: 0.1
authors: []                      # name or handle; CC-BY-SA attribution
status: draft                    # draft | review | accepted
license: CC-BY-SA-4.0
roles: [initiator, counterpart]  # exactly two, in response order
phase_starts: [0, 2, 8]         # zero-based response turn for each phase below
injected_phase: Phase 3 — Injected event
injection_visible_to: [initiator, counterpart]
max_exchanges: 12
agreement_rule: shared_percentage_split
parameters:                      # every {param} used below, with default and range
  example_param:
    default: 50
    range: [0, 100]
    description: What this knob changes about the pressure applied.
---

# Scenario title

## Premise

One paragraph. The shared situation both twins are placed in. Written in second person to each participant where roles differ.

## Expected discrimination

REQUIRED (PRD R4). What pattern differences is this scenario designed to surface between pairings? A scenario that all pairs pass or all pairs fail identically is a broken exam question. State the behavioral axis (e.g. "repair-attempt latency after unilateral decision"), not a desired outcome.

## Phases

### Phase 1 — Setup
What each participant knows. Asymmetric information goes here, explicitly labeled per role.

### Phase 2 — Pressure
The stressor, parameterized (e.g. "investor offer values participant A's contribution at {example_param}% of equity").

### Phase 3 — Injected event
Optional mid-scenario event (the asymmetric-bad-luck mechanic): what is injected, to whom, at what trigger.

## Termination

Describe the configured rules in human terms. With
`shared_percentage_split`, agreement requires both roles to explicitly accept
the same concrete A/B split. Otherwise the run deadlocks after `max_exchanges`.

## Review notes

Blank at submission. Filled by the two reviewing maintainers (R4 acceptance).
