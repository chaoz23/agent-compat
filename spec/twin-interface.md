# Twin Interface Specification

**Version:** 0.1 (per [ADR-0001](../decisions/ADR-0001-twin-interface.md) — accepted 2026-07-02)

Defines what a twin must *expose* to be simulatable — a conformant query surface, not the twin's internals (PRD R1, Non-Goal 2). The words MUST/SHOULD/MAY are RFC-2119.

## 1. Scope and conformance

There is exactly one conformance level, **L1**. A twin is conformant if it implements the response surface (§2) and declares provenance metadata (§4) in its descriptor (§5). Reports annotate `conformance: "L1"`.

There is no structured elicitation requirement. Structured signal (values, stances, shift-under-pressure) is extracted through **probe scenarios** — standardized scenarios engineered to surface it through in-character interaction — defined in [scenario-format.md](scenario-format.md). Rationale and the reopening condition are in ADR-0001.

## 2. The response surface

```
respond(context, message) -> message
```

- `message` (in and out) is a plain string: the counterpart's utterance in, the twin's in-character reply out.
- `context` is an envelope object the runner constructs fresh on every call:

| Field | Type | Meaning |
|---|---|---|
| `scenario_id` | string | Scenario being run (e.g. `collaboration/equity-split-renegotiation`) |
| `role` | string | Which scenario role this twin plays |
| `briefing` | string | Everything this role knows: premise, role-specific setup, and any injected events *visible to this role*, rendered as text |
| `phase` | string | Current phase name |
| `turn` | int | 0-based turn index within the run |
| `history` | list of `{speaker, text}` | The full visible conversation so far, oldest first |
| `params` | object | Resolved scenario parameter values |

- **Statelessness:** a twin MUST NOT rely on hidden state carried across `respond` calls within or across runs; everything it needs is in `context`. This is what makes deterministic seeding (R2) and sealed running (R7) possible. A twin MAY be internally stateful in how it *models its human* (that's its whole job); it MUST NOT be stateful about *this simulation*.
- A twin SHOULD stay in character; the runner treats every returned string as an in-character utterance, evidence-quotable in reports.

## 3. Elicitation annex (reserved, inactive)

Reserved for a possible future `elicit(...)` surface. Per ADR-0001, this annex is **inactive in v0.x** and is only activated if a required metric demonstrably cannot be built on probe scenarios. If activated:

- Elicitation outputs MUST be hard-tagged **T0-equivalent provenance** regardless of the twin's declared tier — a directly-asked answer is a stated self-model, whatever produced it.
- Reports MUST NOT mix elicited and behavioral signal without tier annotation (extends R5's no-silent-tier-mixing to the interface).

Implementations MUST NOT ship `elicit` surfaces claiming agent-compat conformance while this annex is inactive.

## 4. Provenance metadata (R5)

Every twin declares its evidence basis in its descriptor:

- **T0** — self-report / questionnaire-derived.
- **T1** — conversational-corpus-derived.
- **T2** — behaviorally verified.

Runners MUST propagate tiers into reports unmodified; report renderers widen uncertainty for lower tiers. Tier freshness/drift is an open PRD question and MAY appear as an optional `provenance.as_of` date.

## 5. Twin descriptor

The unit a runner accepts. JSON object:

```json
{
  "twin_id": "string, stable identifier",
  "display_name": "string",
  "provenance": {"tier": "T0 | T1 | T2", "as_of": "optional ISO date"},
  "interface_version": "0.1",
  "backend": "free-form string: stub | ollama/<model> | api/<endpoint-class>"
}
```

The descriptor carries no twin internals — no persona text, no corpus, no weights. How a runner *reaches* the twin behind a descriptor (in-process object, HTTP endpoint, sealed-runner attestation) is a runner concern, out of scope for this document.

## 6. Errors and refusals

A twin MAY refuse to respond (returning a refusal is still an in-character response; raising an error is not). Runner-level errors (timeouts, malformed returns) MUST surface in the report's per-scenario record — a run with hidden failures is worse than a failed run.
