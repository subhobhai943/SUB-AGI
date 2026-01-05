"""Core mind kernel loop for SUB-AGI."""

from __future__ import annotations
from dataclasses import replace
from typing import Tuple, Optional, Any

from .mind_state import (
    MindState, Thought, FocusItem, EpisodicEpisode, EpisodicEvent,
    VisualObject, SemanticConcept
)

class MindKernel:
    """Minimal SUB-AGI control loop."""

    def __init__(self) -> None:
        self._state: MindState = MindState.new()

    @property
    def state(self) -> MindState:
        return self._state

    def step(self, user_input: str, observation: Optional[Any] = None) -> Tuple[str, MindState]:
        """Process input + observation -> reply + new_state."""
        next_state = self._state.clone_for_next_tick()

        # 1) Update perception (Text)
        next_state.perception.raw_input = user_input
        next_state.perception.tokens = user_input.strip().split()

        # 2) Update perception (Visual)
        # Assuming observation is a dict or object with 'visible_objects'
        if observation and hasattr(observation, 'visible_objects'):
            next_state.perception.visual_objects = []
            for obj in observation.visible_objects:
                # obj is dict from grid_world
                next_state.perception.visual_objects.append(
                    VisualObject(
                        id=obj['id'],
                        kind=obj['kind'],
                        rel_position=obj['rel_position'],
                        shape_pattern=obj.get('shape')
                    )
                )

        # 3) Working Memory Update
        thought = Thought(
            id=f"thought-{next_state.meta.tick}",
            content=f"Input: '{user_input}'. Visuals: {len(next_state.perception.visual_objects)} objects",
            strength=0.7,
        )
        next_state.working_memory.current_thoughts.append(thought)
        
        # 4) Episodic Memory (simplified)
        if not next_state.long_term_memory.episodic:
            next_state.long_term_memory.episodic.append(
                EpisodicEpisode("ep-1", next_state.time.created_at, next_state.time.created_at, "Start")
            )
        next_state.long_term_memory.episodic[0].events.append(
            EpisodicEvent(next_state.meta.tick, user_input, next_state.meta.state_id, 0.1, 0.3)
        )

        # 5) Reasoning & Reply Generation
        reply = self._generate_reply(next_state, user_input)
        
        self._state = next_state
        return reply, self._state

    def _generate_reply(self, state: MindState, user_input: str) -> str:
        """Heuristic-based reply logic for Phase 1."""
        text = user_input.lower().strip()
        
        # A) Symbol Grounding: User says "This is X" while looking at an object
        if text.startswith("this is ") and len(text.split()) == 3:
            label = text.split()[-1].upper() # Extract label "A"
            # Look at visual objects
            visible = state.perception.visual_objects
            
            # Heuristic: If exactly one salient object is visible, associate label with its shape
            objects_with_shape = [o for o in visible if o.shape_pattern]
            
            if len(objects_with_shape) == 1:
                obj = objects_with_shape[0]
                # Store in Semantic Memory
                concept = SemanticConcept(
                    id=f"concept-{label}",
                    type="letter_shape",
                    symbol=label,
                    shape_pattern=obj.shape_pattern
                )
                state.long_term_memory.semantic_concepts.append(concept)
                return f"I see the shape. I will remember that this is '{label}'."
            elif len(objects_with_shape) > 1:
                return "I see multiple shapes. Which one is it?"
            else:
                return "I don't see any shape to learn."

        # B) Recall: User asks "What is this?"
        if "what is this" in text:
            visible = state.perception.visual_objects
            objects_with_shape = [o for o in visible if o.shape_pattern]
            
            if len(objects_with_shape) == 1:
                target_shape = objects_with_shape[0].shape_pattern
                # Search Semantic Memory
                for concept in state.long_term_memory.semantic_concepts:
                    if concept.shape_pattern == target_shape:
                        return f"This looks like '{concept.symbol}'."
                return "I see a shape, but I don't know what it is yet."
            
        return f"I am listening. (Visual objects: {len(state.perception.visual_objects)})"
