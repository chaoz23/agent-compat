from agent_compat.validate_report import r6_violations


def test_rejects_top_level_compatibility_score():
    assert r6_violations({"compatibility_score": 0.87})


def test_rejects_disguised_names():
    for key in ("overallMatch", "COMPAT_INDEX", "rating", "final_grade", "verdict_num"):
        assert r6_violations({key: 5}), key


def test_accepts_structured_report():
    report = {
        "spec_version": "0.1",
        "scenarios": [{"id": "collaboration/equity", "outcome_distribution": {"resolved": 0.6}}],
        "sycophancy_diagnostics": {"agreement_rate": 0.91},
        "provenance": {"twin_a": "T1", "twin_b": "T0"},
    }
    assert not r6_violations(report)


def test_nested_numbers_are_fine_only_top_level_is_policed():
    # Per-scenario/per-metric numbers are the point of the report; R6 bans
    # only the top-level overall verdict.
    assert not r6_violations({"metrics": {"repair_score": 0.4}})


def test_non_numeric_top_level_score_key_passes():
    assert not r6_violations({"score_methodology": "see spec"})


def test_bool_is_not_a_score():
    assert not r6_violations({"matched_schema": True})
