from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AuditRecord:
    action_id: str
    outcome: str
    payload: Dict[str, Any]
    token: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class SOSPAuditLog:
    def __init__(self) -> None:
        self.records: List[AuditRecord] = []

    def log_action(
        self,
        action_id: str,
        outcome: str,
        payload: Dict[str, Any],
        token: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.records.append(
            AuditRecord(
                action_id=action_id,
                outcome=outcome,
                payload=dict(payload),
                token=token,
                metadata=dict(metadata or {}),
            )
        )

