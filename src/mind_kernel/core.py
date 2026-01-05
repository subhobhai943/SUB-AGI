"""Core mind kernel loop for SUB-AGI.

This module defines the MindKernel class that:
- Holds the current MindState
- Accepts user input as text
- Produces a text response

Initially this is intentionally simple and transparent. The goal is to
have a minimal, inspectable "alive" loop that can later grow in
complexity.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Tuple

from .mind_state import (
    MindState,
    Thought,
    FocusItem,
    EpisodicEpisode,
    EpisodicEvent,
)


class MindKernel:
    """Minimal SUB-AGI control loop.

    Usage pattern (pseudo-code):

        kernel = MindKernel()
        while True:
            user_text = input("You: ")
            reply, state = kernel.step(user_text)
            print("SUB-AGI:", reply)

    The kernel always returns the latest MindState, so callers can
    inspect or log the internal "mind" after each step.
    """

    def __init__(self) -> None:
        self._state: MindState = MindState.new()

    @property
    def state(self) -> MindState:
        return self._state

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def step(self, user_input: str) -> Tuple[str, MindState]:
        """Process one user input and return (reply_text, new_state).

        For now, the behavior is deliberately simple:
        - Update perception (raw_input, tokens)
        - Push a thought into working memory
        - Append an episodic memory event
        - Generate a basic, honest reply
        """
        # Prepare next state (tick+1) while preserving continuity
        next_state = self._state.clone_for_next_tick()

        # 1) Update perception
        tokens = user_input.strip().split()
        next_state.perception.raw_input = user_input
        next_state.perception.tokens = tokens

        # 2) Update working memory / attention
        next_state.working_memory.attention.recent_inputs.append(user_input)
        next_state.working_memory.attention.current_focus = "conversation"

        thought = Thought(
            id=f"thought-{next_state.meta.tick}",
            content=f"User said: '{user_input}'",
            strength=0.7,
        )
        next_state.working_memory.current_thoughts.append(thought)

        if user_input:
            next_state.working_memory.focus_stack.append(
                FocusItem(type="conversation", value="respond_to_user")
            )

        # 3) Minimal episodic memory update (one episode for now)
        if not next_state.long_term_memory.episodic:
            episode = EpisodicEpisode(
                episode_id="episode-1",
                time_start=next_state.time.created_at,
                time_end=next_state.time.created_at,
                summary="Initial interactions",
            )
            next_state.long_term_memory.episodic.append(episode)

        episode = next_state.long_term_memory.episodic[0]
        event = EpisodicEvent(
            t=next_state.meta.tick,
            input=user_input,
            internal_state_ref=next_state.meta.state_id,
            emotional_valence=0.1,
            emotional_arousal=0.3,
        )
        episode.events.append(event)
        episode.time_end = next_state.time.last_updated_at

        # 4) Dialogue context
        next_state.dialog_context.last_user_utterance = user_input
        next_state.dialog_context.history.append(
            replace(
                type(next_state.dialog_context.history[0]) if next_state.dialog_context.history else None,
            )
            if False
            else None
        )

        # Generate a naive but honest reply
        if not user_input.strip():
            reply = "I did not hear anything. Can you say something?"
            next_state.safety.flags.confused = True
        else:
            reply = self._generate_reply(next_state, user_input)
            next_state.dialog_context.last_system_utterance = reply
            next_state.dialog_context.history.append(
                type("DialogTurn", (), {"speaker": "sub-agi", "text": reply})()
            )

        # Update internal state
        self._state = next_state
        return reply, self._state

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _generate_reply(self, state: MindState, user_input: str) -> str:
        """Very simple reply strategy for the first prototype.

        Rules (temporary):
        - If the user mentions a single uppercase letter, treat it as
          an alphabet lesson.
        - Otherwise, acknowledge and echo.
        """
        tokens = user_input.strip().split()
        uppercase_letters = [t for t in tokens if len(t) == 1 and t.isalpha() and t.isupper()]

        if len(uppercase_letters) == 1:
            letter = uppercase_letters[0]
            if letter not in state.perception.alphabet_focus.letters_seen:
                state.perception.alphabet_focus.letters_seen.append(letter)
            state.perception.alphabet_focus.current_letter_lesson = letter
            return f"I see the letter '{letter}'. I am learning it."

        # Fallback generic reply
        return f"I am SUB-AGI and I heard you say: '{user_input}'."
