# Runner

Reference batch runner (PRD R2) — not yet implemented; blocked on [ADR-0001](../decisions/ADR-0001-twin-interface.md) deciding the twin interface it drives.

What exists now: `validate_report.py`, the R6 no-single-score validator. It is deliberately first — the report discipline is the project's spine, and everything the runner eventually emits must pass it. Run tests with `python -m pytest runner/`.

Coming with ADR-0001 resolution: two hardcoded-persona stub twins, one toy scenario, and a minimal runner producing a spec-conformant report (Phase 0 exit criterion).
