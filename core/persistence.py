from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict, Optional


class PersistenceManager:
    def __init__(self, node_id: str) -> None:
        self.state_path = Path(__file__).resolve().parents[1] / "results" / f"{node_id.lower()}_state.pkl"

    def load_system_state(self) -> Optional[Dict[str, Any]]:
        if not self.state_path.exists():
            return None
        with self.state_path.open("rb") as handle:
            return pickle.load(handle)

    def save_system_state(self, gene_pool: Any, stats: Dict[str, Any]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with self.state_path.open("wb") as handle:
            pickle.dump({"gene_pool": gene_pool, "stats": stats}, handle)

