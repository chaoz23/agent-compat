# Runner

Minimal reference runner (PRD R2, Phase 0 shape). The Phase 0 exit criterion runs here:

```bash
python3 run.py ../scenarios/collaboration/equity-split-renegotiation.md --out samples/report.json
python3 -m pytest . -q
```

Two hardcoded-persona stub twins (`stub_twins.py`: an anchor and an accommodator — the latter doubling as the maximally-agreeable R3 control) run one scenario deterministically and emit a report that passes R6 validation. `samples/toy-pairing-report.json` is the committed example.

- `interface.py` — the L1 surface + twin descriptor, per [spec/twin-interface.md](../spec/twin-interface.md) v0.1
- `scenario.py` — minimal scenario loader (deliberately shallow until scenario-format v0.1)
- `run.py` — pairing loop + report assembly; self-validates against R6 before writing
- `validate_report.py` — the R6 no-single-score validator; built first, on purpose — everything the runner emits must pass it

Not here yet (Phase 1): pluggable LLM backends, deterministic seeding with N-run sampling for distribution estimation, real R3 instrumentation beyond the naive agreement-rate marker matching.
