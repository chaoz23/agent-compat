# Runner

Minimal reference runner (PRD R2, Phase 0 shape). The Phase 0 exit criterion runs here:

```bash
pip install -e . pytest        # from repo root; or just `uvx agent-compat` for the demo
agent-compat --out report.json # bundled demo scenario
agent-compat scenarios/collaboration/equity-split-renegotiation.md
python -m pytest runner/ -q
```

This directory is packaged as the `agent_compat` module (see `pyproject.toml`); the demo scenario in `data/` is drift-guarded against the corpus copy by a test.

Two hardcoded-persona stub twins (`stub_twins.py`: an anchor and an accommodator — the latter doubling as the maximally-agreeable R3 control) run one scenario deterministically and emit a report that passes R6 validation. `samples/toy-pairing-report.json` is the committed example.

- `interface.py` — the L1 surface + twin descriptor, per [spec/twin-interface.md](../spec/twin-interface.md) v0.1
- `scenario.py` — executable scenario-format v0.1 parser and validator, shared with CI
- `run.py` — data-driven pairing loop + evidence-based termination + report assembly;
  self-validates against R6 before writing
- `validate_report.py` — the R6 no-single-score validator; built first, on purpose — everything the runner emits must pass it

Not here yet (Phase 1): pluggable LLM backends, deterministic seeding with
N-run sampling for distribution estimation, rupture evidence, parameter
overrides, and real R3 instrumentation beyond naive agreement-rate markers.
