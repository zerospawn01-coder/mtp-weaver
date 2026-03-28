from __future__ import annotations

from typing import Any, Dict


def contextual_reversibility_index(payload: Dict[str, Any]) -> float:
    if not payload:
        return 0.0
    unique_keys = len(set(payload.keys()))
    return min(1.0, unique_keys / 10.0)

