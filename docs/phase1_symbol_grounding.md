# Phase 1: Symbol Grounding Environment

Phase 1 introduces a **2D grid-world environment** where SUB-AGI can act
and perceive before learning symbolic labels like letters.

## Motivation

Traditional AI learns symbols from static text, which leads to
"ungrounded" representations that do not connect to real experience
(symbol grounding problem). Developmental robotics and embodied
cognition research instead let agents build concepts from
sensorimotor interaction first, then attach words or symbols later
[Frontiers in Neurorobotics, 2012][1][Emergent Mind, 2025][2].

Our goal in Phase 1 is to give SUB-AGI a simple but rich enough world
where it can:
- Move.
- Encounter and distinguish objects.
- Form internal representations of space and objects.

Only after that will we attach labels (like "A", "B", "C") to patterns
in this experience.

## Environment: GridWorld

Implemented in `src/environment/grid_world.py`:

- Discrete 2D grid (default 5x5).
- One agent (SUB-AGI) with a position and orientation.
- A few objects (blocks) placed randomly.
- At each time step, SUB-AGI can act with one of:
  - `"up"`, `"down"`, `"left"`, `"right"`, `"stay"`.
- The agent receives an **observation** containing:
  - Its own position.
  - A list of visible objects with their absolute and relative positions.
  - The current grid as a 2D array of symbols (`"."`, `"A"`, `"O"`).

This environment is intentionally small, deterministic, and
fully inspectable. It does not depend on any deep learning
frameworks.

## How SUB-AGI Will Use This

In future steps, the `MindKernel` will:
- Hold a `GridWorld` instance.
- Decide an action each tick (possibly based on curiosity or goals).
- Receive an observation and integrate it into `MindState.perception`
  and `long_term_memory`.

Later, when a human teaches SUB-AGI that a certain configuration or
trajectory is called "A", that symbol will be grounded in the
agent's own experience inside this world.

---

[1]: https://www.frontiersin.org/articles/10.3389/fnbot.2012.00001/full
[2]: https://www.emergentmind.com/topics/symbol-grounding-problem
