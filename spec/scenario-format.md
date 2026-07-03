# Scenario Format Specification

**Version:** pre-0.1 — OUTLINE ONLY. Structure firms up alongside [ADR-0001](../decisions/ADR-0001-twin-interface.md); probe-scenario requirements depend on its resolution.

Parameterized stress scenarios with phases, injected events, and termination conditions (PRD R1, R4).

## 1. File format and layout

<!-- Structured markdown + YAML frontmatter; one scenario per file; domain packs as directories. Non-programmer authorable (Persona C). -->

## 2. Metadata block

<!-- id, domain, version, authors, license (CC-BY-SA), expected-discrimination statement (R4 acceptance). -->

## 3. Parameterization

<!-- Named parameters with ranges/defaults; e.g. equity split %, severity of injected failure. -->

## 4. Phases and injected events

<!-- Ordered phases; mid-scenario event injection (the "asymmetric bad luck" mechanic); who receives what information. -->

## 5. Termination conditions

<!-- Turn limits, deadlock detection, resolution detection. -->

## 6. Probe scenarios

<!-- Reserved: standardized signal-extraction scenarios, pending ADR-0001. -->
