from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class TrajectoryEntry:
    ehi: float
    payload: Dict[str, Any]


class Trajectory:
    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        self.history: List[TrajectoryEntry] = []

    @property
    def chain(self) -> List[Dict[str, Any]]:
        return [{"ehi": entry.ehi, "payload": entry.payload} for entry in self.history]

    def commit(self, ehi: float, payload: Dict[str, Any]) -> None:
        self.history.append(TrajectoryEntry(ehi=ehi, payload=dict(payload)))

