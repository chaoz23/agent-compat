#!/usr/bin/env python3
"""Scenario-format lint: structural checks on scenario files.

Deliberately shallow until spec/scenario-format.md v0.1 lands: checks YAML
frontmatter presence + required keys, and the required 'Expected
discrimination' section (PRD R4). TEMPLATE.md and READMEs are skipped.

Usage: lint_scenarios.py scenarios/
Exit codes: 0 clean, 1 lint errors.
"""
import sys
from pathlib import Path

REQUIRED_FRONTMATTER_KEYS = ("id:", "domain:", "version:", "license:")
REQUIRED_SECTIONS = ("## Expected discrimination", "## Premise", "## Termination")
SKIP_NAMES = {"README.md", "TEMPLATE.md"}


def lint(path: Path) -> list[str]:
    text = path.read_text()
    errors = []
    if not text.startswith("---"):
        errors.append("missing YAML frontmatter")
    else:
        frontmatter = text.split("---", 2)[1] if text.count("---") >= 2 else ""
        for key in REQUIRED_FRONTMATTER_KEYS:
            if key not in frontmatter:
                errors.append(f"frontmatter missing '{key}'")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing required section '{section}'")
    return errors


def main(root: str) -> int:
    failed = False
    files = [p for p in Path(root).rglob("*.md") if p.name not in SKIP_NAMES]
    for path in sorted(files):
        for err in lint(path):
            print(f"{path}: {err}", file=sys.stderr)
            failed = True
    print(f"linted {len(files)} scenario file(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "scenarios/"))
