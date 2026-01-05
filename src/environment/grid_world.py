"""Simple 2D grid-world environment for SUB-AGI.

Phase 1 goal: provide a minimal sensorimotor space where SUB-AGI can
"see" and "act" before being taught symbolic labels like letters.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple, Optional
import random


Coord = Tuple[int, int]


@dataclass
class GridObject:
    """An object in the grid world."""
    id: str
    kind: str
    position: Coord
    # 3x3 visual pattern (list of 3 strings of length 3)
    # e.g. [" . ", "A A", "A A"]
    shape: Optional[List[str]] = None


@dataclass
class AgentState:
    position: Coord
    orientation: str = "up"


@dataclass
class GridWorldConfig:
    rows: int = 5
    cols: int = 5
    num_objects: int = 2


@dataclass
class Observation:
    """What the agent can "see" at a time step."""
    agent_position: Coord
    visible_objects: List[Dict]
    grid: List[List[str]]


class GridWorld:
    """A minimal grid world."""

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

        # Place agent
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
        """Apply an action and return (obs, reward, done, info)."""
        if action not in {"up", "down", "left", "right", "stay"}:
            raise ValueError(f"Invalid action: {action}")

        if action != "stay":
            self._move_agent(action)

        self._render_to_grid()
        obs = self.observe()
        return obs, 0.0, False, {}

    def observe(self) -> Observation:
        """Return the agent's current observation of the world."""
        visible_objects: List[Dict] = []
        ar, ac = self.agent.position
        for obj in self.objects:
            orow, ocol = obj.position
            # Simple visibility: if in same grid, it's visible.
            # Real visual system would have FOV, but this is Phase 1.
            visible_objects.append(
                {
                    "id": obj.id,
                    "kind": obj.kind,
                    "abs_position": obj.position,
                    "rel_position": (orow - ar, ocol - ac),
                    "shape": obj.shape  # The agent sees the shape!
                }
            )

        return Observation(
            agent_position=self.agent.position,
            visible_objects=visible_objects,
            grid=[row.copy() for row in self._grid],
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def add_object(self, obj: GridObject):
        """Manually add an object (for experiments)."""
        self.objects.append(obj)
        self._render_to_grid()

    def _sample_empty_cell(self, occupied: set[Coord]) -> Coord:
        r, c = self.config.rows, self.config.cols
        while True:
            pos = (random.randrange(r), random.randrange(c))
            if pos not in occupied:
                return pos

    def _move_agent(self, direction: str) -> None:
        r, c = self.agent.position
        if direction == "up": r -= 1
        elif direction == "down": r += 1
        elif direction == "left": c -= 1
        elif direction == "right": c += 1

        r = max(0, min(self.config.rows - 1, r))
        c = max(0, min(self.config.cols - 1, c))
        self.agent.position = (r, c)
        self.agent.orientation = direction

    def _render_to_grid(self) -> None:
        r, c = self.config.rows, self.config.cols
        self._grid = [["." for _ in range(c)] for _ in range(r)]
        for obj in self.objects:
            orow, ocol = obj.position
            self._grid[orow][ocol] = "O"
        ar, ac = self.agent.position
        self._grid[ar][ac] = "A"

    def grid_as_str(self) -> str:
        return "\n".join(" ".join(row) for row in self._grid)

    def to_dict(self) -> Dict:
        return {
            "config": asdict(self.config),
            "agent": asdict(self.agent),
            "objects": [asdict(o) for o in self.objects],
        }

# --- Predefined Shapes for Phase 1 ---

SHAPE_A = [
    " . ",
    "A A",
    "A A"
] # Simplified A

SHAPE_B = [
    "BB ",
    "B B",
    "BB "
] # Simplified B
