from __future__ import annotations

import random
from typing import List, Optional, Tuple

from .trajectory import Trajectory


class GenePool:
    def __init__(self, sincere_min: float, sincere_max: float, sincere_target: float) -> None:
        self.sincere_min = sincere_min
        self.sincere_max = sincere_max
        self.sincere_target = sincere_target
        self._pool: List[Tuple[Trajectory, float]] = []

    @property
    def size(self) -> int:
        return len(self._pool)

    def preserve(self, trajectory: Trajectory) -> bool:
        if not trajectory.history:
            return False
        score = sum(entry.ehi for entry in trajectory.history) / len(trajectory.history)
        if not (self.sincere_min <= score <= self.sincere_max):
            return False
        self._pool.append((trajectory, score))
        self._pool.sort(key=lambda item: abs(item[1] - self.sincere_target))
        self._pool = self._pool[:50]
        return True

    def preserve_foreign(self, trajectory: Trajectory, fitness_override: float | None = None) -> bool:
        score = fitness_override if fitness_override is not None else 0.5
        self._pool.append((trajectory, score))
        self._pool.sort(key=lambda item: abs(item[1] - self.sincere_target))
        self._pool = self._pool[:50]
        return True

    def select_parents(self) -> Optional[Tuple[Trajectory, Trajectory]]:
        if len(self._pool) < 2:
            return None
        parents = random.sample(self._pool[: min(len(self._pool), 10)], 2)
        return parents[0][0], parents[1][0]


class CrossoverEngine:
    def splice(self, parent_a: Trajectory, parent_b: Trajectory) -> Trajectory:
        child = Trajectory(agent_id=f"{parent_a.agent_id}+{parent_b.agent_id}")
        midpoint_a = max(1, len(parent_a.history) // 2)
        midpoint_b = max(1, len(parent_b.history) // 2)
        for entry in parent_a.history[:midpoint_a]:
            child.commit(entry.ehi, entry.payload)
        for entry in parent_b.history[-midpoint_b:]:
            child.commit(entry.ehi, entry.payload)
        return child


class HyperMutator:
    def __init__(self, chaos_rate: float = 0.25) -> None:
        self.chaos_rate = chaos_rate
        self.r = chaos_rate

    def inject_chaos(self, trajectory: Trajectory) -> Trajectory:
        mutated = Trajectory(agent_id=f"{trajectory.agent_id}_mut")
        for entry in trajectory.history:
            payload = dict(entry.payload)
            payload["chaos"] = round(random.random() * self.r, 4)
            mutated.commit(entry.ehi, payload)
        return mutated

