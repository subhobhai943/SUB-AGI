"""Simple 2D grid-world environment for SUB-AGI.

Phase 1 goal: provide a minimal sensorimotor space where SUB-AGI can
"see" and "act" before being taught symbolic labels like letters.

Design principles (inspired by developmental robotics and symbol
grounding research):
- Discrete time steps.
- Discrete 2D grid.
- One agent (SUB-AGI) with a position and orientation.
- A small number of objects with simple shapes or IDs.
- Local observations (what is around the agent), not full omniscient view.

This environment does *not* depend on any ML framework. It is pure
Python, intentionally simple and fully inspectable.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple
import random


Coord = Tuple[int, int]


@dataclass
class GridObject:
    """An object in the grid world.

    Attributes
    ----------
    id: str
        A unique identifier, e.g. "obj-1".
    kind: str
        A high-level type label, e.g. "block", "target".
    position: Coord
        (row, col) location in the grid.
    """

    id: str
    kind: str
    position: Coord


@dataclass
class AgentState:
    position: Coord
    # For now, orientation is unused, but we keep it for future use.
    orientation: str = "up"  # one of {"up", "down", "left", "right"}


@dataclass
class GridWorldConfig:
    rows: int = 5
    cols: int = 5
    num_objects: int = 2


@dataclass
class Observation:
    """What the agent can "see" at a time step.

    For simplicity, we expose:
    - its own position
    - a list of visible objects with their relative positions
    - the raw grid if needed (can be disabled later for partial observability)
    """

    agent_position: Coord
    visible_objects: List[Dict]
    grid: List[List[str]]


class GridWorld:
    """A minimal grid world.

    The grid is represented as a 2D list of strings:
    - "." for empty cells
    - "A" for the agent
    - "O" for generic objects (for now)
    """

    def __init__(self, config: GridWorldConfig | None = None) -> None:
        self.config = config or GridWorldConfig()
        self.agent = AgentState(position=(0, 0))
        self.objects: List[GridObject] = []
        self._grid: List[List[str]] = []
        self.reset()

    # ------------------------------------------------------------------
    # Core environment API
    # ------------------------------------------------------------------

    def reset(self) -> Observation:
        """Reset the environment to a new random configuration."""
        r, c = self.config.rows, self.config.cols
        self._grid = [["." for _ in range(c)] for _ in range(r)]

        # Place agent in a random empty cell
        self.agent.position = (random.randrange(r), random.randrange(c))

        # Place objects
        self.objects = []
        occupied = {self.agent.position}
        for i in range(self.config.num_objects):
            pos = self._sample_empty_cell(occupied)
            occupied.add(pos)
            obj = GridObject(id=f"obj-{i+1}", kind="block", position=pos)
            self.objects.append(obj)

        self._render_to_grid()
        return self.observe()

    def step(self, action: str) -> Tuple[Observation, float, bool, Dict]:
        """Apply an action and return (obs, reward, done, info).

        Allowed actions: "up", "down", "left", "right", "stay".
        For Phase 1, there is no terminal condition (done is always False).
        Reward is 0 by default; experiments can define their own reward
        shaping later.
        """
        if action not in {"up", "down", "left", "right", "stay"}:
            raise ValueError(f"Invalid action: {action}")

        if action != "stay":
            self._move_agent(action)

        self._render_to_grid()
        obs = self.observe()
        reward = 0.0
        done = False
        info: Dict = {}
        return obs, reward, done, info

    def observe(self) -> Observation:
        """Return the agent's current observation of the world."""
        visible_objects: List[Dict] = []
        ar, ac = self.agent.position
        for obj in self.objects:
            orow, ocol = obj.position
            visible_objects.append(
                {
                    "id": obj.id,
                    "kind": obj.kind,
                    "abs_position": obj.position,
                    "rel_position": (orow - ar, ocol - ac),
                }
            )

        return Observation(
            agent_position=self.agent.position,
            visible_objects=visible_objects,
            grid=[row.copy() for row in self._grid],
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sample_empty_cell(self, occupied: set[Coord]) -> Coord:
        r, c = self.config.rows, self.config.cols
        while True:
            pos = (random.randrange(r), random.randrange(c))
            if pos not in occupied:
                return pos

    def _move_agent(self, direction: str) -> None:
        r, c = self.agent.position
        if direction == "up":
            r -= 1
        elif direction == "down":
            r += 1
        elif direction == "left":
            c -= 1
        elif direction == "right":
            c += 1

        r = max(0, min(self.config.rows - 1, r))
        c = max(0, min(self.config.cols - 1, c))
        self.agent.position = (r, c)
        self.agent.orientation = direction

    def _render_to_grid(self) -> None:
        r, c = self.config.rows, self.config.cols
        self._grid = [["." for _ in range(c)] for _ in range(r)]

        # Place objects
        for obj in self.objects:
            orow, ocol = obj.position
            self._grid[orow][ocol] = "O"

        # Place agent (overwrites object if same cell for now)
        ar, ac = self.agent.position
        self._grid[ar][ac] = "A"

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def grid_as_str(self) -> str:
        """Return a human-readable string representation of the grid."""
        return "\n".join(" ".join(row) for row in self._grid)

    def to_dict(self) -> Dict:
        """Return a dict snapshot of the environment state."""
        return {
            "config": asdict(self.config),
            "agent": asdict(self.agent),
            "objects": [asdict(o) for o in self.objects],
            "grid": [row.copy() for row in self._grid],
        }
