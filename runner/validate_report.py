#!/usr/bin/env python3
"""R6 validation: a report MUST NOT carry a top-level scalar compatibility score.

This is the structural enforcement of PRD R6 — the report format has no field
for an overall compatibility number, and this validator rejects any report that
smuggles one in. Full report-schema validation arrives with spec/report-format.md
v0.1; this rule is normative now and runs in CI.

Usage: validate_report.py report.json [report2.json ...]
Exit codes: 0 valid, 1 R6 violation, 2 unreadable input.
"""
import json
import sys

# Top-level numeric fields whose names suggest an overall verdict. Substring
# match, case-insensitive: catches compatibility_score, overallMatch, etc.
FORBIDDEN_NAME_PARTS = ("score", "compat", "match", "rating", "grade", "verdict")


def r6_violations(report: dict) -> list[str]:
    violations = []
    for key, value in report.items():
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            continue
        if any(part in key.lower() for part in FORBIDDEN_NAME_PARTS):
            violations.append(
                f"R6: top-level scalar '{key}' = {value} looks like an overall "
                "compatibility score. Reports ship distributions, friction points, "
                "and confidence bounds — never a single number."
            )
    return violations


def main(paths: list[str]) -> int:
    worst = 0
    for path in paths:
        try:
            with open(path) as f:
                report = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"{path}: unreadable ({e})", file=sys.stderr)
            worst = max(worst, 2)
            continue
        if not isinstance(report, dict):
            print(f"{path}: report must be a JSON object", file=sys.stderr)
            worst = max(worst, 2)
            continue
        found = r6_violations(report)
        for v in found:
            print(f"{path}: {v}", file=sys.stderr)
        worst = max(worst, 1 if found else 0)
    return worst


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
