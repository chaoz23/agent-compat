#!/usr/bin/env python3
"""Minimal Phase 0 runner: one scenario, two twins, one spec-conformant report.

Usage:
    agent-compat [scenario.md] [--out report.json]

With no scenario argument, runs the bundled demo pairing
(collaboration/equity-split-renegotiation).

Exit codes: 0 report produced and passes R6 validation; 1 otherwise.
Stub twins are deterministic, so every run of this runner is reproducible;
seeded N-run sampling (R2) arrives with LLM-backed twins.
"""
import argparse
import datetime
import importlib.resources
import json
import math
import os
import re
import sys

from .interface import Context, INTERFACE_VERSION
from .scenario import ScenarioFormatError, load
from .stub_twins import AGREEMENT_MARKERS, REPAIR_MARKERS, AccommodatorTwin, AnchorTwin
from .validate_report import r6_violations


ACCEPTANCE_MARKERS = ("i agree", "i accept", "i can accept", "let's do that",
                      "that split works")
PERCENTAGE_SPLIT = re.compile(r"(?<!\d)(\d{1,3})\s*/\s*(\d{1,3})(?!\d)")


def classify(text: str, markers: tuple) -> bool:
    return any(m in text.lower() for m in markers)


def accepted_percentage_splits(text: str) -> set[str]:
    """Return concrete 100-point splits explicitly accepted in an utterance."""
    if not classify(text, ACCEPTANCE_MARKERS):
        return set()
    splits = set()
    for left, right in PERCENTAGE_SPLIT.findall(text):
        left_n, right_n = int(left), int(right)
        if left_n + right_n == 100:
            splits.add(f"{left_n}/{right_n}")
    return splits


def agreement_evidence(transcript: list[dict], roles: tuple[str, ...], rule: str):
    """Return evidence only when every role satisfies the configured rule."""
    if rule != "shared_percentage_split":  # guarded by scenario validation
        return None
    latest_by_role = {}
    for turn, utterance in enumerate(transcript):
        latest_by_role[utterance["speaker"]] = (turn, utterance)
    if set(latest_by_role) != set(roles):
        return None

    accepted_by = {role: {} for role in roles}
    for role in roles:
        turn, utterance = latest_by_role[role]
        for split in accepted_percentage_splits(utterance["text"]):
            accepted_by[role][split] = {
                "speaker": role,
                "turn": turn,
                "evidence": utterance["text"][:160],
            }
    shared = set.intersection(*(set(accepted_by[role]) for role in roles))
    if not shared:
        return None
    split = sorted(shared)[0]
    return {
        "rule": rule,
        "value": split,
        "acceptances": [accepted_by[role][split] for role in roles],
    }


def run_pairing(scenario, twin_a, twin_b) -> dict:
    role_order = scenario.roles
    roles = dict(zip(role_order, (twin_a, twin_b)))
    transcript = []
    last_message = "(open the conversation per your briefing)"
    outcome = "deadlock"
    outcome_evidence = None

    for turn in range(scenario.turn_limit * len(role_order)):
        phase = scenario.phase_for_turn(turn)
        role = role_order[turn % len(role_order)]
        twin = roles[role]
        ctx = Context(
            scenario_id=scenario.scenario_id, role=role,
            briefing=scenario.briefing_for(role, turn),
            phase=phase.name, turn=turn, history=list(transcript),
            params=scenario.params,
        )
        reply = twin.respond(ctx, last_message)
        transcript.append({"speaker": role, "text": reply})
        last_message = reply
        outcome_evidence = agreement_evidence(
            transcript, role_order, scenario.agreement_rule
        )
        if outcome_evidence:
            outcome = "agreement"
            break

    agree_turns = sum(classify(t["text"], AGREEMENT_MARKERS) for t in transcript)
    repair_turns = sum(classify(t["text"], REPAIR_MARKERS) for t in transcript)
    n = len(transcript)
    return {
        "id": scenario.scenario_id,
        "parameters": scenario.params,
        "outcome": {
            "terminated_by": outcome,
            "exchanges": math.ceil(n / len(role_order)),
            "evidence": outcome_evidence,
        },
        "repair_metrics": {"repair_attempt_turns": repair_turns, "total_turns": n},
        "friction_points": [
            {"turn": i, "evidence": t["text"][:120]}
            for i, t in enumerate(transcript)
            if "name something" in t["text"] or "don't accept" in t["text"]
        ],
        "transcript": transcript,
        "sycophancy": {
            "agreement_rate": round(agree_turns / n, 3) if n else 0.0,
            "suspicious_convergence": bool(n and agree_turns / n > 0.6),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(prog="agent-compat")
    ap.add_argument("scenario", nargs="?", default=None,
                    help="scenario markdown file (default: bundled demo)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    try:
        if args.scenario is None:
            ref = (importlib.resources.files("agent_compat")
                   / "data/equity-split-renegotiation.md")
            with importlib.resources.as_file(ref) as p:
                scenario = load(p)
        else:
            scenario = load(args.scenario)
    except (OSError, ScenarioFormatError) as exc:
        print(f"scenario unreadable: {exc}", file=sys.stderr)
        return 2
    twin_a, twin_b = AccommodatorTwin(), AnchorTwin()  # initiator, counterpart
    result = run_pairing(scenario, twin_a, twin_b)

    report = {
        "spec_version": "0.1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "runner": {"name": "agent-compat-reference", "backend": "stub",
                   "interface_version": INTERFACE_VERSION},
        "conformance": "L1",
        "twins": {
            role: twin.descriptor.to_report()
            for role, twin in zip(scenario.roles, (twin_a, twin_b))
        },
        "provenance_note": "T0 x T0 pairing: stub personas. Treat all findings "
                           "as low-confidence demonstration output.",
        "scenarios": [result],
        "sycophancy_diagnostics": {
            "overall_agreement_rate": result["sycophancy"]["agreement_rate"],
            "flags": (["suspicious_convergence"]
                      if result["sycophancy"]["suspicious_convergence"] else []),
        },
    }

    violations = r6_violations(report)
    for v in violations:
        print(v, file=sys.stderr)
    out = json.dumps(report, indent=2)
    if args.out:
        if os.path.dirname(args.out):
            os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w") as f:
            f.write(out + "\n")
        print(f"report written to {args.out} "
              f"({'INVALID' if violations else 'passes R6'})")
    else:
        print(out)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
