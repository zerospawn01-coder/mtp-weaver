from __future__ import annotations

from .trajectory import Trajectory


class LEGREngine:
    def calculate(self, trajectory: Trajectory) -> float:
        if not trajectory.history:
            return 0.0
        return sum(entry.ehi for entry in trajectory.history) / len(trajectory.history)

