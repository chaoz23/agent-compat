# Scenario Format Specification

**Version:** 0.1

Defines the executable subset of a pairwise stress scenario (PRD R1, R4).
Scenario files are Markdown with a small YAML-frontmatter subset. The prose is
the reviewable scenario; the frontmatter is the runner's execution plan.

## 1. Required frontmatter

```yaml
---
id: collaboration/equity-split-renegotiation
domain: collaboration
version: 0.1
authors: [founding]
status: draft
license: CC-BY-SA-4.0
roles: [initiator, counterpart]
phase_starts: [0, 2, 6]
injected_phase: Phase 3 — Injected event
injection_visible_to: [initiator, counterpart]
max_exchanges: 12
agreement_rule: shared_percentage_split
parameters:
  months_in:
    default: 8
    range: [3, 24]
    description: Time elapsed before the stress scenario begins.
---
```

- `id`, `domain`, `version`, and `license` identify the corpus artifact.
- `roles` MUST contain exactly two unique role identifiers, in response order.
- `phase_starts` MUST contain one zero-based response turn per `###` phase,
  begin at `0`, and increase strictly.
- `max_exchanges` MUST be a positive integer. One exchange gives every declared
  role one response turn; a run may terminate partway through an exchange.
- `agreement_rule` MUST name a supported evidence rule. Version 0.1 supports
  only `shared_percentage_split` (§5).
- `parameters` MAY declare named defaults. Every `{placeholder}` in the Markdown
  MUST have a declared default.

The v0.1 reference parser accepts inline lists for execution fields and scalar
parameter defaults. This deliberately small subset keeps the reference runner
dependency-free. Future syntax can expand without changing these semantics.

## 2. Required Markdown sections

Every scenario MUST contain:

- `## Premise` — shared situation visible to both roles.
- `## Expected discrimination` — behavioral differences the scenario is
  designed to surface.
- `## Phases` with one or more `###` phase headings.
- `## Termination` — human-readable explanation of the configured rules.

The first phase is the setup. Role-specific setup lines use this form:

```markdown
**Role `initiator`:** Private briefing for that role.
```

The runner includes unlabeled setup lines for both roles and includes a labeled
line only for the named role.

## 3. Phases and response turns

Phases are ordered by their `###` headings. The corresponding value in
`phase_starts` is the first response turn on which that phase is active. Phase
names are passed through the twin `context` envelope. When a phase starts, its
body is added to the briefing and remains visible on later turns.

Version 0.1 permits one injected phase. `injected_phase` MUST exactly match a
declared phase heading, and `injection_visible_to` MUST contain declared roles.
Once that phase starts, its body is appended to the visible briefing only for
those roles.

## 4. Parameterization

Before execution, the runner substitutes each `{parameter}` in the Markdown
with its declared default. Undeclared placeholders are validation errors.
Ranges and descriptions are review metadata in v0.1; override and range-checking
semantics are reserved for a later version.

## 5. Termination evidence

`shared_percentage_split` reports agreement only when every role explicitly
accepts the same concrete `A/B` percentage split and `A + B = 100`. Generic
assent, a proposal without acceptance, or acceptances of different splits MUST
NOT terminate as agreement. Reports include the accepted split and one
transcript reference per role.

If no evidence rule succeeds before `max_exchanges`, the run terminates as
`deadlock`. Rupture detection is reserved until its evidence contract is
specified; implementations MUST NOT infer rupture from sentiment alone.

## 6. Validation

The reference parser is the source shared by the runner and scenario CI lint.
A file that cannot execute MUST fail lint with an actionable format error.

## 7. Probe scenarios

Probe scenarios remain the v0.x mechanism for structured signal extraction per
ADR-0001. Their taxonomy and metric bindings are not yet normative; a probe
uses the same executable format and MUST document its expected discrimination.
