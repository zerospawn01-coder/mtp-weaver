from __future__ import annotations

import json
from pathlib import Path

from .trajectory import Trajectory


class StructuralArchivist:
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir

    def harvest(self, trajectory: Trajectory) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        target = self.storage_dir / f"{trajectory.agent_id}.json"
        payload = [entry.payload for entry in trajectory.history]
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")

