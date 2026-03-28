from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from missions.mission_41_stress_test import adversarial_stress_test
from missions.mission_43_closure import action_closure_test


def main() -> int:
    print("[VERIFY] Running kernel contract checks")
    adversarial_stress_test()
    action_closure_test()
    print("[VERIFY] Kernel contract checks complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

