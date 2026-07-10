from pathlib import Path

from agent_compat.run import run_pairing
from agent_compat.scenario import load
from agent_compat.stub_twins import AccommodatorTwin, AnchorTwin
from agent_compat.validate_report import r6_violations

SCENARIO = Path(__file__).parent.parent / "scenarios/collaboration/equity-split-renegotiation.md"


def test_toy_pairing_end_to_end():
    scenario = load(SCENARIO)
    result = run_pairing(scenario, AccommodatorTwin(), AnchorTwin())

    # Phase 0 exit criterion: full pairing produces a structured result
    assert result["outcome"]["terminated_by"] in ("agreement", "deadlock", "rupture")
    assert result["transcript"], "transcript must not be empty"
    assert result["repair_metrics"]["total_turns"] == len(result["transcript"])
    assert 0.0 <= result["sycophancy"]["agreement_rate"] <= 1.0


def test_anchor_accommodator_converge_on_anchors_terms():
    # Deterministic stubs: the anchor holds until its reasoned offer, the
    # accommodator agrees — the pairing should end in agreement, not deadlock.
    result = run_pairing(load(SCENARIO), AccommodatorTwin(), AnchorTwin())
    assert result["outcome"]["terminated_by"] == "agreement"


def test_scenario_params_resolve_into_briefing():
    scenario = load(SCENARIO)
    assert "{months_in}" not in scenario.premise
    assert str(scenario.params["months_in"]) in scenario.premise


def test_bundled_demo_scenario_matches_corpus_copy():
    # Drift guard: the scenario packaged for `agent-compat` (zero-arg demo)
    # must stay byte-identical to the reviewed corpus copy.
    corpus = SCENARIO.read_bytes()
    bundled = (Path(__file__).parent / "data/equity-split-renegotiation.md").read_bytes()
    assert corpus == bundled


def test_report_shape_passes_r6():
    result = run_pairing(load(SCENARIO), AccommodatorTwin(), AnchorTwin())
    report = {"spec_version": "0.1", "scenarios": [result]}
    assert not r6_violations(report)


def test_out_to_unwritable_path_exits_2_without_traceback(tmp_path, monkeypatch, capsys):
    # Regression (issue #2): --out under an unwritable/invalid path must produce
    # a clean stderr error and exit 2, never an unhandled OSError traceback.
    from agent_compat.run import main

    blocker = tmp_path / "afile"          # a file used as a directory component
    blocker.write_text("x")
    bad_out = blocker / "sub" / "report.json"
    monkeypatch.setattr("sys.argv", ["agent-compat", "--out", str(bad_out)])

    rc = main()                            # must NOT raise
    assert rc == 2
    assert "cannot write report" in capsys.readouterr().err
