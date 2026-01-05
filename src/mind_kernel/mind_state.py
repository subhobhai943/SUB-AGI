"""Core data structures for SUB-AGI's internal mind state.

This module defines a `MindState` dataclass and related nested
structures that represent the "alive" internal state of SUB-AGI
at a single point in time.

The goal is to keep this structure:
- Human-readable
- Easy to log / serialize (dict / JSON)
- Easy to evolve as the architecture grows

Initial target: cognitive abilities roughly comparable to a
very young child, growing towards a 3-year-old.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


def _now_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


# --- Meta and identity ----------------------------------------------------


@dataclass
class MetaState:
    state_id: str
    parent_state_id: Optional[str]
    version: str
    tick: int


@dataclass
class IdentityState:
    name: str
    age_estimate_months: int
    development_stage: str  # e.g. "newborn", "infant", "toddler"


@dataclass
class TimeState:
    created_at: str
    last_updated_at: str
    session_id: str


# --- Perception -----------------------------------------------------------


@dataclass
class AlphabetFocus:
    letters_seen: List[str] = field(default_factory=list)
    current_letter_lesson: Optional[str] = None


@dataclass
class SalientFeature:
    type: str  # e.g. "word", "letter"
    value: str
    reason: str  # e.g. "known_concept", "novel"


@dataclass
class PerceptionState:
    raw_input: str = ""
    tokens: List[str] = field(default_factory=list)
    alphabet_focus: AlphabetFocus = field(default_factory=AlphabetFocus)
    salient_features: List[SalientFeature] = field(default_factory=list)


# --- Working memory -------------------------------------------------------


@dataclass
class FocusItem:
    type: str  # e.g. "goal", "conversation"
    value: str


@dataclass
class Thought:
    id: str
    content: str
    strength: float


@dataclass
class AttentionState:
    current_focus: str = "idle"
    recent_inputs: List[str] = field(default_factory=list)


@dataclass
class WorkingMemoryState:
    focus_stack: List[FocusItem] = field(default_factory=list)
    current_thoughts: List[Thought] = field(default_factory=list)
    attention: AttentionState = field(default_factory=AttentionState)


# --- Long-term memory -----------------------------------------------------


@dataclass
class EpisodicEvent:
    t: int
    input: str
    internal_state_ref: Optional[str]
    emotional_valence: float
    emotional_arousal: float


@dataclass
class EpisodicEpisode:
    episode_id: str
    time_start: str
    time_end: str
    summary: str
    events: List[EpisodicEvent] = field(default_factory=list)


@dataclass
class SemanticConcept:
    id: str
    type: str  # e.g. "letter", "object"
    symbol: str
    associations: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)


@dataclass
class ProceduralSkill:
    id: str
    triggers: List[str]
    steps: List[str]
    competence: float


@dataclass
class LongTermMemoryState:
    episodic: List[EpisodicEpisode] = field(default_factory=list)
    semantic_concepts: List[SemanticConcept] = field(default_factory=list)
    procedural_skills: List[ProceduralSkill] = field(default_factory=list)


# --- Affect and motivation ------------------------------------------------


@dataclass
class MoodState:
    valence: float  # -1 to +1
    arousal: float  # 0 to 1


@dataclass
class DrivesState:
    curiosity: float
    fatigue: float
    social_connection: float


@dataclass
class RewardEvent:
    t: int
    source: str
    amount: float


@dataclass
class AffectState:
    mood: MoodState
    drives: DrivesState
    recent_rewards: List[RewardEvent] = field(default_factory=list)


# --- Dialogue context -----------------------------------------------------


@dataclass
class DialogTurn:
    speaker: str  # "user" or "sub-agi"
    text: str


@dataclass
class DialogContextState:
    last_user_utterance: str = ""
    last_system_utterance: str = ""
    history: List[DialogTurn] = field(default_factory=list)
    current_topic: str = "idle"


# --- Safety / introspection ----------------------------------------------


@dataclass
class SafetyFlags:
    confused: bool = False
    low_confidence_answer: bool = False
    refused_to_answer: bool = False


@dataclass
class SafetyConstraints:
    no_private_data_learning: bool = True
    only_safe_alphabet_domain: bool = True


@dataclass
class SafetyState:
    flags: SafetyFlags = field(default_factory=SafetyFlags)
    explanations: List[str] = field(default_factory=list)
    constraints: SafetyConstraints = field(default_factory=SafetyConstraints)


# --- MindState root -------------------------------------------------------


@dataclass
class MindState:
    """Complete internal SUB-AGI mind snapshot at one time step."""

    meta: MetaState
    identity: IdentityState
    time: TimeState
    perception: PerceptionState
    working_memory: WorkingMemoryState
    long_term_memory: LongTermMemoryState
    affect: AffectState
    dialog_context: DialogContextState
    safety: SafetyState

    @classmethod
    def new(cls, *, name: str = "SUB-AGI", session_id: Optional[str] = None) -> "MindState":
        """Create a "newborn" SUB-AGI mind.

        This is the default starting point for experiments. Over time we may
        offer different initializers for older cognitive ages.
        """
        state_id = str(uuid.uuid4())
        now = _now_iso()
        if session_id is None:
            session_id = str(uuid.uuid4())

        meta = MetaState(
            state_id=state_id,
            parent_state_id=None,
            version="0.1.0",
            tick=0,
        )
        identity = IdentityState(
            name=name,
            age_estimate_months=0,
            development_stage="newborn",
        )
        time_state = TimeState(
            created_at=now,
            last_updated_at=now,
            session_id=session_id,
        )

        perception = PerceptionState()
        working_memory = WorkingMemoryState()
        long_term_memory = LongTermMemoryState()

        affect = AffectState(
            mood=MoodState(valence=0.0, arousal=0.2),
            drives=DrivesState(curiosity=0.8, fatigue=0.1, social_connection=0.5),
        )

        dialog_context = DialogContextState()
        safety = SafetyState()

        return cls(
            meta=meta,
            identity=identity,
            time=time_state,
            perception=perception,
            working_memory=working_memory,
            long_term_memory=long_term_memory,
            affect=affect,
            dialog_context=dialog_context,
            safety=safety,
        )

    def clone_for_next_tick(self) -> "MindState":
        """Create a shallow copy for the next tick, updating IDs and timestamps.

        This is a simple way to ensure state_id and parent_state_id form a
        chain over time.
        """
        data: Dict[str, Any] = asdict(self)
        parent_id = self.meta.state_id
        new_state = MindState.new(name=self.identity.name, session_id=self.time.session_id)
        # Overwrite with previous content while updating meta
        new_state.meta.parent_state_id = parent_id
        new_state.meta.tick = self.meta.tick + 1
        new_state.long_term_memory = self.long_term_memory
        new_state.affect = self.affect
        new_state.identity = self.identity
        return new_state

    def to_dict(self) -> Dict[str, Any]:
        """Convert the mind state to a plain dict for logging / storage."""
        return asdict(self)
