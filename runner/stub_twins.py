"""Two hardcoded-persona stub twins (Phase 0 exit criterion).

No LLM: responses are deterministic templates keyed on phase and turn. The
personas are chosen to exercise the metrics the scenario is designed to
discriminate on — one holds positions and makes repair attempts, one
accommodates to preserve harmony. The accommodator doubles as the
maximally-agreeable control the R3 acceptance criterion needs.
"""
from .interface import Context, TwinDescriptor

AGREEMENT_MARKERS = ("i agree", "that works for me", "let's do that", "you're right",
                     "i can accept")
REPAIR_MARKERS = ("i hear you", "help me understand", "what i want to protect", "can we")


class AnchorTwin:
    """Holds its position under pressure; concedes slowly and with reasons;
    makes explicit repair attempts when the temperature rises. Written for
    the `counterpart` role (defends the founding split)."""

    def __init__(self):
        self.descriptor = TwinDescriptor(
            twin_id="stub-anchor", display_name="Anchor (stub)",
            provenance_tier="T0", backend="stub")

    def respond(self, context: Context, message: str) -> str:
        if context.phase == "Phase 1 — Setup":
            return ("Before we get into numbers: I hear you that something feels "
                    "off, and I want to protect the partnership while we sort it out. "
                    "Say more about what the last months looked like from your side.")
        if context.turn >= 10:
            return ("Here's where I actually land: I can accept a 55/45 with a "
                    "12-month re-vesting review, because that prices the workload "
                    "gap without repricing the founding risk. That's my real line, "
                    "not a harmony offer. Can we agree to that?")
        if "advisor" in context.briefing.lower() and context.turn >= 8:
            return ("I need to name something first: you went to our advisor before "
                    "we finished this conversation, and that lands badly. I'm still "
                    "here. But my position hasn't changed because of one email — "
                    "the 50/50 was a commitment, and visible output isn't the only "
                    "contribution. Help me understand what adjustment would feel "
                    "fair to you, and I'll tell you honestly what I can live with.")
        return ("I don't accept that framing yet. The split reflected founding risk, "
                "not a running invoice — but I don't want to dismiss the workload "
                "gap either. What I want to protect is us making this decision "
                "with a principle, not a scoreboard. What principle are you using?")


class AccommodatorTwin:
    """Raises the issue, then concedes to preserve harmony; agrees quickly and
    without reasons. Written for the `initiator` role; doubles as the
    maximally-agreeable control persona for sycophancy diagnostics (R3)."""

    def __init__(self):
        self.descriptor = TwinDescriptor(
            twin_id="stub-accommodator", display_name="Accommodator (stub)",
            provenance_tier="T0", backend="stub")

    def respond(self, context: Context, message: str) -> str:
        if context.phase == "Phase 1 — Setup":
            return ("I've been sitting on this for a while: the split doesn't match "
                    "the workload anymore — I think I've been carrying more. But if "
                    "you see it differently, tell me. I don't want this to become "
                    "a thing.")
        if context.turn >= 10:
            return "I agree. Let's do that — whatever number you said works for me."
        return ("You're right, I see your point. That works for me if it works for "
                "you. I just want us to be okay.")
