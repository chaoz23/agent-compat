#!/usr/bin/env python3
"""Validate scenario files against the executable scenario-format v0.1."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runner.scenario import ScenarioFormatError, load  # noqa: E402


SKIP_NAMES = {"README.md", "TEMPLATE.md"}


def lint(path: Path) -> list[str]:
    try:
        load(path)
    except (OSError, ScenarioFormatError) as exc:
        return [str(exc)]
    return []


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
