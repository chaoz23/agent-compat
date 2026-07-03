"""Minimal scenario loader: frontmatter + phase sections from structured markdown.

Deliberately shallow until spec/scenario-format.md v0.1 — parses exactly what
the Phase 0 runner needs: id, parameter defaults, role briefings, phases,
injected-event trigger, and turn limit.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Scenario:
    scenario_id: str
    params: dict
    premise: str
    phases: list[dict] = field(default_factory=list)  # {"name": str, "body": str}
    turn_limit: int = 12

    def briefing_for(self, role: str) -> str:
        """Premise + this role's setup lines from Phase 1."""
        setup = next((p["body"] for p in self.phases if "Setup" in p["name"]), "")
        role_lines = [
            line for line in setup.splitlines()
            if not line.startswith("**Role") or f"`{role}`" in line
        ]
        return self.premise + "\n\n" + "\n".join(role_lines)


def _frontmatter(text: str) -> tuple[str, str]:
    _, fm, body = text.split("---", 2)
    return fm, body


def _param_defaults(fm: str) -> dict:
    params = {}
    current = None
    for line in fm.splitlines():
        m = re.match(r"^  (\w+):\s*$", line)
        if m:
            current = m.group(1)
        m = re.match(r"^    default:\s*(\S+)", line)
        if m and current:
            v = m.group(1)
            params[current] = int(v) if v.lstrip("-").isdigit() else v
    return params


def load(path: str | Path) -> Scenario:
    fm, body = _frontmatter(Path(path).read_text())
    scenario_id = re.search(r"^id:\s*(\S+)", fm, re.M).group(1)
    params = _param_defaults(fm)

    body = re.sub(r"\{(\w+)\}", lambda m: str(params.get(m.group(1), m.group(0))), body)
    premise = re.search(r"## Premise\n+(.*?)\n+##", body, re.S).group(1).strip()
    phases = [
        {"name": name.strip(), "body": pbody.strip()}
        for name, pbody in re.findall(r"### (.+?)\n(.*?)(?=\n### |\n## |\Z)", body, re.S)
    ]
    m = re.search(r"turn limit \((\d+)", body)
    return Scenario(scenario_id, params, premise, phases,
                    turn_limit=int(m.group(1)) if m else 12)
