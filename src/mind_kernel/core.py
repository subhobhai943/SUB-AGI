"""Core mind kernel loop for SUB-AGI.

Phase 2 Update:
- Implements the 'Curiosity Loop': Predict -> Act -> Observe -> Surprise -> Learn.
- Adds 'auto_act()' to allow SUB-AGI to choose its own actions in GridWorld.
"""

from __future__ import annotations
from typing import Tuple, Optional, Any
import random

from .mind_state import (
    MindState, Thought, FocusItem, EpisodicEpisode, EpisodicEvent,
    VisualObject, SemanticConcept, Prediction
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

        # 1. Update Perception
        self._update_perception(next_state, user_input, observation)

        # 2. Calculate Surprise & Update Affect (Curiosity Loop)
        self._process_prediction_error(next_state)

        # 3. Working Memory & Thoughts
        thought_content = f"Input: '{user_input}'."
        if observation:
            vis_count = len(next_state.perception.visual_objects)
            thought_content += f" Visuals: {vis_count}."
        
        # Add internal monologue about boredom/surprise
        if next_state.affect.drives.surprise_last_tick > 0.5:
            thought_content += " Whoa! Something changed!"
        elif next_state.affect.drives.boredom > 0.7:
            thought_content += " I am bored. I need to explore."

        thought = Thought(
            id=f"thought-{next_state.meta.tick}",
            content=thought_content,
            strength=0.7,
        )
        next_state.working_memory.current_thoughts.append(thought)
        
        # 4. Episodic Memory
        self._update_episodic_memory(next_state, user_input)

        # 5. Reply / Reaction
        reply = self._generate_reply(next_state, user_input)
        
        self._state = next_state
        return reply, self._state

    def choose_action(self, observation: Any) -> str:
        """Decide next physical action based on boredom and curiosity.
        
        This is the 'Autonomous' part of Phase 2.
        """
        # If very bored, move randomly to find something new
        if self._state.affect.drives.boredom > 0.5:
            # Simple heuristic: try to move to unvisited area or just random
            return random.choice(["up", "down", "left", "right"])
        
        # If curious (saw an object), maybe stay to look at it?
        # For now, let's keep exploring if we just saw it.
        # But if we are NOT bored, we might 'stay' to focus.
        if len(self._state.perception.visual_objects) > 0:
            return "stay" # Look at the interesting thing
            
        # Default exploration
        return random.choice(["up", "down", "left", "right"])

    def predict_next(self, action: str) -> None:
        """Form a prediction about the next state before acting."""
        # Simple prediction model: 
        # "If I move, I expect to see the same number of objects unless I find new ones"
        current_vis_count = len(self._state.perception.visual_objects)
        
        pred = Prediction(
            action_taken=action,
            expected_visual_count=current_vis_count, # Naive prediction
            confidence=0.5
        )
        self._state.working_memory.active_prediction = pred

    # --- Internal Helpers ---

    def _update_perception(self, state: MindState, user_input: str, observation: Any):
        state.perception.raw_input = user_input
        state.perception.tokens = user_input.strip().split()

        if observation and hasattr(observation, 'visible_objects'):
            state.perception.visual_objects = []
            for obj in observation.visible_objects:
                state.perception.visual_objects.append(
                    VisualObject(
                        id=obj['id'],
                        kind=obj['kind'],
                        rel_position=obj['rel_position'],
                        shape_pattern=obj.get('shape')
                    )
                )
            # Update spatial memory (visited locations)
            # Assuming observation has 'agent_position'
            pos = getattr(observation, 'agent_position', None)
            if pos and pos not in state.long_term_memory.spatial.visited_cells:
                state.long_term_memory.spatial.visited_cells.append(pos)

    def _process_prediction_error(self, state: MindState):
        """Compare active prediction with reality to compute surprise."""
        prediction = self._state.working_memory.active_prediction # Use PREVIOUS state's prediction
        surprise = 0.0
        
        if prediction:
            actual_count = len(state.perception.visual_objects)
            # Surprise is diff between expected and actual
            diff = abs(prediction.expected_visual_count - actual_count)
            if diff > 0:
                surprise = 1.0 # High surprise if object count changes!
            else:
                surprise = 0.0 # Boring, exactly as expected
        
        state.affect.drives.surprise_last_tick = surprise
        
        # Update Boredom
        if surprise > 0.1:
            # Novelty found! Reset boredom.
            state.affect.drives.boredom = 0.0
            # Boost mood (intrinsic reward)
            state.affect.mood.valence = min(1.0, state.affect.mood.valence + 0.2)
            state.affect.mood.arousal = min(1.0, state.affect.mood.arousal + 0.3)
        else:
            # Nothing new... getting bored.
            state.affect.drives.boredom = min(1.0, state.affect.drives.boredom + 0.1)
            state.affect.mood.arousal = max(0.0, state.affect.mood.arousal - 0.05)

    def _update_episodic_memory(self, state: MindState, user_input: str):
        if not state.long_term_memory.episodic:
            state.long_term_memory.episodic.append(
                EpisodicEpisode("ep-1", state.time.created_at, state.time.created_at, "Start")
            )
        state.long_term_memory.episodic[0].events.append(
            EpisodicEvent(state.meta.tick, user_input, state.meta.state_id, 0.1, 0.3)
        )

    def _generate_reply(self, state: MindState, user_input: str) -> str:
        # Check for specific queries or just report state
        text = user_input.lower().strip()
        
        if "status" in text:
            b = state.affect.drives.boredom
            s = state.affect.drives.surprise_last_tick
            return f"Boredom: {b:.2f}, Surprise: {s:.2f}, Visuals: {len(state.perception.visual_objects)}"
            
        # Symbol Grounding logic from Phase 1
        if text.startswith("this is ") and len(text.split()) == 3:
            label = text.split()[-1].upper()
            visible = state.perception.visual_objects
            objects_with_shape = [o for o in visible if o.shape_pattern]
            if len(objects_with_shape) == 1:
                obj = objects_with_shape[0]
                concept = SemanticConcept(f"concept-{label}", "letter_shape", label, shape_pattern=obj.shape_pattern)
                state.long_term_memory.semantic_concepts.append(concept)
                return f"Learned: This shape is '{label}'."

        if state.affect.drives.surprise_last_tick > 0.8:
            return "Wow! I found something new!"
            
        if state.affect.drives.boredom > 0.8:
            return "I am bored. I am going to move around."
            
        return f"Thinking... (Boredom: {state.affect.drives.boredom:.1f})"
