from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


class HLG:
    def __init__(self) -> None:
        self.pending: Dict[str, str] = {}

    def request_approval(self, intent: str, action_id: str, payload: Dict[str, Any]) -> str:
        base = json.dumps({"intent": intent, "action_id": action_id, "payload": payload}, sort_keys=True)
        token = hashlib.sha256(base.encode("utf-8")).hexdigest()[:12]
        self.pending[action_id] = token
        return token

    def verify_token(self, token: str, action_id: str) -> bool:
        return self.pending.get(action_id) == token

