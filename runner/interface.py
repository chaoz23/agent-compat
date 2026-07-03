"""Twin interface, spec/twin-interface.md v0.1 — the L1 surface and descriptor."""
from dataclasses import dataclass, field
from typing import Protocol

INTERFACE_VERSION = "0.1"


@dataclass
class Context:
    """The envelope a runner constructs fresh on every respond() call (spec §2)."""
    scenario_id: str
    role: str
    briefing: str
    phase: str
    turn: int
    history: list[dict] = field(default_factory=list)  # {"speaker": str, "text": str}
    params: dict = field(default_factory=dict)


@dataclass
class TwinDescriptor:
    """Spec §5 — carries no twin internals."""
    twin_id: str
    display_name: str
    provenance_tier: str  # T0 | T1 | T2
    backend: str
    interface_version: str = INTERFACE_VERSION

    def to_report(self) -> dict:
        return {
            "twin_id": self.twin_id,
            "display_name": self.display_name,
            "provenance": {"tier": self.provenance_tier},
            "interface_version": self.interface_version,
            "backend": self.backend,
        }


class Twin(Protocol):
    """L1 conformance is this one method (spec §1-2)."""
    descriptor: TwinDescriptor

    def respond(self, context: Context, message: str) -> str: ...
