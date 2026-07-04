"""Scenario-format v0.1 loader and validator.

The executable metadata intentionally uses a small, flat YAML subset so the
reference runner stays dependency-free while scenario files remain authorable
without code. Markdown carries the human-facing content; frontmatter carries
the execution plan.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path


SUPPORTED_AGREEMENT_RULES = {"shared_percentage_split"}


class ScenarioFormatError(ValueError):
    """A scenario cannot be executed according to scenario-format v0.1."""


@dataclass(frozen=True)
class Phase:
    name: str
    body: str
    start_turn: int
    injected: bool = False
    visible_to: tuple[str, ...] = ()


@dataclass
class Scenario:
    scenario_id: str
    roles: tuple[str, ...]
    params: dict
    premise: str
    expected_discrimination: str
    phases: list[Phase] = field(default_factory=list)
    turn_limit: int = 12  # maximum pair exchanges
    agreement_rule: str = "shared_percentage_split"

    def phase_for_turn(self, turn: int) -> Phase:
        """Return the active phase for a zero-based response turn."""
        active = self.phases[0]
        for phase in self.phases:
            if phase.start_turn > turn:
                break
            active = phase
        return active

    def briefing_for(self, role: str, turn: int = 0) -> str:
        """Build the role-visible briefing at a particular response turn."""
        if role not in self.roles:
            raise ScenarioFormatError(f"unknown role '{role}'")

        def visible_body(phase: Phase) -> str:
            role_lines = [
                line for line in phase.body.splitlines()
                if not line.startswith("**Role") or f"`{role}`" in line
            ]
            return "\n".join(role_lines)

        parts = [self.premise, visible_body(self.phases[0])]
        for phase in self.phases[1:]:
            if phase.start_turn > turn:
                break
            if phase.injected and role not in phase.visible_to:
                continue
            label = "INJECTED EVENT" if phase.injected else f"PHASE: {phase.name}"
            parts.append(f"[{label}] {visible_body(phase)}")
        return "\n\n".join(part for part in parts if part)


def _frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        raise ScenarioFormatError("missing YAML frontmatter")
    pieces = text.split("---", 2)
    if len(pieces) != 3:
        raise ScenarioFormatError("unterminated YAML frontmatter")
    return pieces[1], pieces[2]


def _scalar(fm: str, key: str, *, required: bool = True) -> str | None:
    match = re.search(rf"^{re.escape(key)}:[ \t]*(.*?)[ \t]*$", fm, re.M)
    if not match or not match.group(1):
        if required:
            raise ScenarioFormatError(f"frontmatter missing '{key}'")
        return None
    value = re.split(r"\s+#", match.group(1).strip(), maxsplit=1)[0]
    return value.strip().strip("\"'")


def _inline_list(fm: str, key: str, *, required: bool = True) -> list[str]:
    raw = _scalar(fm, key, required=required)
    if raw is None:
        return []
    if not (raw.startswith("[") and raw.endswith("]")):
        raise ScenarioFormatError(f"'{key}' must be an inline list")
    values = [item.strip().strip("\"'") for item in raw[1:-1].split(",")]
    return [value for value in values if value]


def _positive_int(fm: str, key: str) -> int:
    raw = _scalar(fm, key)
    try:
        value = int(raw)
    except (TypeError, ValueError) as exc:
        raise ScenarioFormatError(f"'{key}' must be an integer") from exc
    if value <= 0:
        raise ScenarioFormatError(f"'{key}' must be greater than zero")
    return value


def _param_defaults(fm: str) -> dict:
    params = {}
    match = re.search(
        r"^parameters:[ \t]*(?:#[^\n]*)?$\n(.*?)(?=^[^ \n][^\n]*:|\Z)",
        fm,
        re.M | re.S,
    )
    if not match:
        return params
    current = None
    for line in match.group(1).splitlines():
        key = re.match(r"^  ([A-Za-z_][\w-]*):\s*$", line)
        if key:
            current = key.group(1)
            continue
        default = re.match(r"^    default:\s*(\S+)", line)
        if default and current:
            value = default.group(1).strip("\"'")
            params[current] = int(value) if value.lstrip("-").isdigit() else value
    return params


def _section(body: str, name: str) -> str:
    match = re.search(
        rf"^## {re.escape(name)}\s*$\n+(.*?)(?=^## |\Z)", body, re.M | re.S
    )
    if not match:
        raise ScenarioFormatError(f"missing required section '## {name}'")
    return match.group(1).strip()


def load_text(text: str) -> Scenario:
    """Parse and validate a scenario from text."""
    fm, body = _frontmatter(text)
    for key in ("id", "domain", "version", "license"):
        _scalar(fm, key)

    scenario_id = _scalar(fm, "id")
    roles = tuple(_inline_list(fm, "roles"))
    if len(roles) != 2 or len(set(roles)) != 2:
        raise ScenarioFormatError("'roles' must declare exactly two unique roles")

    starts_raw = _inline_list(fm, "phase_starts")
    try:
        phase_starts = [int(value) for value in starts_raw]
    except ValueError as exc:
        raise ScenarioFormatError("'phase_starts' values must be integers") from exc
    if not phase_starts or phase_starts[0] != 0:
        raise ScenarioFormatError("'phase_starts' must begin at turn 0")
    if any(a >= b for a, b in zip(phase_starts, phase_starts[1:])):
        raise ScenarioFormatError("'phase_starts' must be strictly increasing")

    phases_body = _section(body, "Phases")
    phase_parts = re.findall(
        r"^### (.+?)\s*$\n(.*?)(?=^### |\Z)", phases_body, re.M | re.S
    )
    if not phase_parts:
        raise ScenarioFormatError("'## Phases' must contain at least one '###' phase")
    if len(phase_parts) != len(phase_starts):
        raise ScenarioFormatError(
            "'phase_starts' must contain one start turn for each phase"
        )

    injected_name = _scalar(fm, "injected_phase", required=False)
    visible_to = tuple(_inline_list(fm, "injection_visible_to", required=False))
    phase_names = [name.strip() for name, _ in phase_parts]
    role_labels = set(re.findall(r"^\*\*Role `([^`]+)`:\*\*", phases_body, re.M))
    unknown_role_labels = role_labels - set(roles)
    if unknown_role_labels:
        raise ScenarioFormatError(
            "phase briefing contains unknown role(s): "
            + ", ".join(sorted(unknown_role_labels))
        )
    if injected_name and injected_name not in phase_names:
        raise ScenarioFormatError("'injected_phase' must name a declared phase")
    if injected_name and not visible_to:
        raise ScenarioFormatError("injected phases require 'injection_visible_to'")
    unknown_visible_roles = set(visible_to) - set(roles)
    if unknown_visible_roles:
        raise ScenarioFormatError(
            "'injection_visible_to' contains unknown role(s): "
            + ", ".join(sorted(unknown_visible_roles))
        )

    agreement_rule = _scalar(fm, "agreement_rule")
    if agreement_rule not in SUPPORTED_AGREEMENT_RULES:
        raise ScenarioFormatError(
            f"unsupported agreement rule '{agreement_rule}'; expected one of "
            + ", ".join(sorted(SUPPORTED_AGREEMENT_RULES))
        )

    params = _param_defaults(fm)
    placeholders = set(re.findall(r"\{([A-Za-z_][\w-]*)\}", body))
    undeclared = placeholders - set(params)
    if undeclared:
        raise ScenarioFormatError(
            "undeclared parameter placeholder(s): " + ", ".join(sorted(undeclared))
        )
    body = re.sub(
        r"\{([A-Za-z_][\w-]*)\}", lambda m: str(params[m.group(1)]), body
    )
    _section(body, "Termination")

    phases = [
        Phase(
            name=name.strip(),
            body=phase_body.strip(),
            start_turn=start,
            injected=name.strip() == injected_name,
            visible_to=visible_to if name.strip() == injected_name else (),
        )
        for (name, phase_body), start in zip(phase_parts, phase_starts)
    ]
    return Scenario(
        scenario_id=scenario_id,
        roles=roles,
        params=params,
        premise=_section(body, "Premise"),
        expected_discrimination=_section(body, "Expected discrimination"),
        phases=phases,
        turn_limit=_positive_int(fm, "max_exchanges"),
        agreement_rule=agreement_rule,
    )


def load(path: str | Path) -> Scenario:
    """Parse and validate a scenario file."""
    return load_text(Path(path).read_text())
