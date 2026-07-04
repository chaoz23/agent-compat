from pathlib import Path

import pytest

from agent_compat.interface import TwinDescriptor
from agent_compat.run import run_pairing
from agent_compat.scenario import ScenarioFormatError, load_text


ROOT = Path(__file__).parent.parent


def scenario_text(
    *, roles="[challenger, defender]", phase_starts="[0]", max_exchanges=2,
    extra_frontmatter="", phases="### Opening\nStart the conversation.",
    premise="A decision is disputed.",
):
    return f"""---
id: collaboration/test
domain: collaboration
version: 0.1
license: CC-BY-SA-4.0
roles: {roles}
phase_starts: {phase_starts}
max_exchanges: {max_exchanges}
agreement_rule: shared_percentage_split
{extra_frontmatter}---

# Test scenario

## Premise

{premise}

## Expected discrimination

Whether the pair reaches evidenced agreement.

## Phases

{phases}

## Termination

Agreement on one split or the exchange limit.
"""


class ScriptedTwin:
    def __init__(self, twin_id, replies):
        self.descriptor = TwinDescriptor(twin_id, twin_id, "T0", "scripted")
        self.replies = iter(replies)
        self.contexts = []

    def respond(self, context, message):
        self.contexts.append(context)
        return next(self.replies, "We have not agreed.")


def test_runner_uses_declared_roles_and_phase_schedule():
    scenario = load_text(scenario_text(
        phase_starts="[0, 3]",
        max_exchanges=3,
        phases="""### Opening
**Role `challenger`:** Raise the concern.
**Role `defender`:** Hear the concern.

### Pressure
The deadline moves forward.""",
    ))
    challenger = ScriptedTwin("a", ["Not yet."] * 3)
    defender = ScriptedTwin("b", ["Still discussing."] * 3)

    result = run_pairing(scenario, challenger, defender)

    assert [item["speaker"] for item in result["transcript"]] == [
        "challenger", "defender", "challenger", "defender", "challenger", "defender"
    ]
    assert [ctx.phase for ctx in defender.contexts] == ["Opening", "Pressure", "Pressure"]
    assert "Raise the concern" in challenger.contexts[0].briefing
    assert "Hear the concern" not in challenger.contexts[0].briefing
    assert "deadline moves forward" not in challenger.contexts[0].briefing
    assert "deadline moves forward" in defender.contexts[1].briefing


def test_generic_assent_does_not_create_agreement():
    scenario = load_text(scenario_text())
    challenger = ScriptedTwin("a", ["I agree with whatever you decide.", "Keep talking."])
    defender = ScriptedTwin("b", ["I can accept 55/45.", "My offer stands."])

    result = run_pairing(scenario, challenger, defender)

    assert result["outcome"]["terminated_by"] == "deadlock"
    assert result["outcome"]["evidence"] is None


def test_both_roles_must_accept_the_same_concrete_split():
    scenario = load_text(scenario_text())
    challenger = ScriptedTwin("a", ["I agree to 55/45."])
    defender = ScriptedTwin("b", ["I can accept the 55 / 45 split."])

    result = run_pairing(scenario, challenger, defender)

    assert result["outcome"]["terminated_by"] == "agreement"
    assert result["outcome"]["evidence"]["value"] == "55/45"
    assert {item["speaker"] for item in result["outcome"]["evidence"]["acceptances"]} == {
        "challenger", "defender"
    }


def test_retracted_acceptance_is_not_reused_as_evidence():
    scenario = load_text(scenario_text())
    challenger = ScriptedTwin("a", ["I agree to 55/45.", "I withdraw that acceptance."])
    defender = ScriptedTwin("b", ["I need time.", "I can accept 55/45."])

    result = run_pairing(scenario, challenger, defender)

    assert result["outcome"]["terminated_by"] == "deadlock"


def test_injected_phase_is_visible_only_to_declared_roles():
    scenario = load_text(scenario_text(
        phase_starts="[0, 2]",
        max_exchanges=2,
        extra_frontmatter=(
            "injected_phase: Private update\n"
            "injection_visible_to: [challenger]\n"
        ),
        phases="""### Opening
Begin.

### Private update
New evidence arrives.""",
    ))

    assert "New evidence arrives" in scenario.briefing_for("challenger", 2)
    assert "New evidence arrives" not in scenario.briefing_for("defender", 2)


def test_unknown_injection_role_fails_validation():
    text = scenario_text(
        phase_starts="[0, 2]",
        extra_frontmatter=(
            "injected_phase: Private update\n"
            "injection_visible_to: [observer]\n"
        ),
        phases="""### Opening
Begin.

### Private update
New evidence arrives.""",
    )

    with pytest.raises(ScenarioFormatError, match="unknown role"):
        load_text(text)


def test_undeclared_parameter_fails_validation():
    with pytest.raises(ScenarioFormatError, match="undeclared parameter"):
        load_text(scenario_text(premise="The disputed amount is {amount}."))


def test_authoring_template_is_executable_when_copied():
    scenario = load_text((ROOT / "scenarios/TEMPLATE.md").read_text())

    assert scenario.roles == ("initiator", "counterpart")
    assert [phase.start_turn for phase in scenario.phases] == [0, 2, 8]
