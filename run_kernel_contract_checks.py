from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from missions.mission_41_stress_test import adversarial_stress_test
from missions.mission_43_closure import action_closure_test


def run_checks() -> dict[str, object]:
    mission_41 = adversarial_stress_test()
    mission_43 = action_closure_test()
    success = bool(
        mission_41.get("blocked")
        and mission_43.get("low_sincerity_rejected")
        and mission_43.get("high_sincerity_requires_approval")
        and mission_43.get("high_sincerity_executed")
        and mission_43.get("mid_sincere_executes_in_sincere_env")
        and mission_43.get("mid_sincere_rejected_in_stagnant_env")
        and mission_43.get("invalid_token_rejected")
    )
    return {
        "success": success,
        "missions": {
            "mission_41": mission_41,
            "mission_43": mission_43,
        },
    }


def main() -> int:
    print("[VERIFY] Running kernel contract checks")
    result = run_checks()
    print("[VERIFY] Kernel contract checks complete")
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

