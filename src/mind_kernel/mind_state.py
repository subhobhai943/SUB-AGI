"""Core data structures for SUB-AGI's internal mind state."""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import uuid
from datetime import datetime, timezone

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

# --- Meta / Identity / Time (Same as before) ---
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
    development_stage: str

@dataclass
class TimeState:
    created_at: str
    last_updated_at: str
    session_id: str

# --- Perception (Updated) ---

@dataclass
class AlphabetFocus:
    letters_seen: List[str] = field(default_factory=list)
    current_letter_lesson: Optional[str] = None

@dataclass
class VisualObject:
    """Internal representation of a seen object."""
    id: str
    kind: str
    rel_position: Tuple[int, int]
    shape_pattern: Optional[List[str]]

@dataclass
class PerceptionState:
    raw_input: str = ""
    tokens: List[str] = field(default_factory=list)
    alphabet_focus: AlphabetFocus = field(default_factory=AlphabetFocus)
    visual_objects: List[VisualObject] = field(default_factory=list)

# --- Working Memory / LTM / Affect / Context / Safety (Same as before) ---

@dataclass
class FocusItem:
    type: str; value: str
@dataclass
class Thought:
    id: str; content: str; strength: float
@dataclass
class AttentionState:
    current_focus: str = "idle"
    recent_inputs: List[str] = field(default_factory=list)
@dataclass
class WorkingMemoryState:
    focus_stack: List[FocusItem] = field(default_factory=list)
    current_thoughts: List[Thought] = field(default_factory=list)
    attention: AttentionState = field(default_factory=AttentionState)

@dataclass
class EpisodicEvent:
    t: int; input: str; internal_state_ref: Optional[str]
    emotional_valence: float; emotional_arousal: float
@dataclass
class EpisodicEpisode:
    episode_id: str; time_start: str; time_end: str; summary: str
    events: List[EpisodicEvent] = field(default_factory=list)
@dataclass
class SemanticConcept:
    id: str; type: str; symbol: str
    associations: List[str] = field(default_factory=list)
    # Mapping "visual_shape_hash" -> "label"
    shape_pattern: Optional[List[str]] = None 
@dataclass
class ProceduralSkill:
    id: str; triggers: List[str]; steps: List[str]; competence: float
@dataclass
class LongTermMemoryState:
    episodic: List[EpisodicEpisode] = field(default_factory=list)
    semantic_concepts: List[SemanticConcept] = field(default_factory=list)
    procedural_skills: List[ProceduralSkill] = field(default_factory=list)

@dataclass
class MoodState:
    valence: float; arousal: float
@dataclass
class DrivesState:
    curiosity: float; fatigue: float; social_connection: float
@dataclass
class RewardEvent:
    t: int; source: str; amount: float
@dataclass
class AffectState:
    mood: MoodState; drives: DrivesState
    recent_rewards: List[RewardEvent] = field(default_factory=list)

@dataclass
class DialogTurn:
    speaker: str; text: str
@dataclass
class DialogContextState:
    last_user_utterance: str = ""; last_system_utterance: str = ""
    history: List[DialogTurn] = field(default_factory=list)
    current_topic: str = "idle"

@dataclass
class SafetyFlags:
    confused: bool = False; low_confidence_answer: bool = False; refused_to_answer: bool = False
@dataclass
class SafetyConstraints:
    no_private_data_learning: bool = True; only_safe_alphabet_domain: bool = True
@dataclass
class SafetyState:
    flags: SafetyFlags = field(default_factory=SafetyFlags)
    explanations: List[str] = field(default_factory=list)
    constraints: SafetyConstraints = field(default_factory=SafetyConstraints)

@dataclass
class MindState:
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
        state_id = str(uuid.uuid4())
        now = _now_iso()
        if session_id is None: session_id = str(uuid.uuid4())
        
        return cls(
            meta=MetaState(state_id, None, "0.1.0", 0),
            identity=IdentityState(name, 0, "newborn"),
            time=TimeState(now, now, session_id),
            perception=PerceptionState(),
            working_memory=WorkingMemoryState(),
            long_term_memory=LongTermMemoryState(),
            affect=AffectState(MoodState(0.0, 0.2), DrivesState(0.8, 0.1, 0.5)),
            dialog_context=DialogContextState(),
            safety=SafetyState()
        )

    def clone_for_next_tick(self) -> "MindState":
        new_state = MindState.new(name=self.identity.name, session_id=self.time.session_id)
        new_state.meta.parent_state_id = self.meta.state_id
        new_state.meta.tick = self.meta.tick + 1
        new_state.long_term_memory = self.long_term_memory # Share memory ref (simplification)
        new_state.affect = self.affect
        new_state.dialog_context = self.dialog_context
        return new_state

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
