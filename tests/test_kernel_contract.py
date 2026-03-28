from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config import KernelConfig
from core.kernel import AntigravityKernel
from run_kernel_contract_checks import run_checks


class KernelContractIntegrationTests(unittest.TestCase):
    def test_kernel_contract_regression_path_passes(self) -> None:
        result = run_checks()

        self.assertTrue(result["success"])
        mission_41 = result["missions"]["mission_41"]
        mission_43 = result["missions"]["mission_43"]

        self.assertTrue(mission_41["blocked"])
        self.assertTrue(mission_43["low_sincerity_rejected"])
        self.assertTrue(mission_43["high_sincerity_requires_approval"])
        self.assertTrue(mission_43["high_sincerity_executed"])
        self.assertTrue(mission_43["mid_sincere_executes_in_sincere_env"])
        self.assertTrue(mission_43["mid_sincere_rejected_in_stagnant_env"])
        self.assertTrue(mission_43["invalid_token_rejected"])

    def test_kernel_rejects_forged_token_fail_closed(self) -> None:
        config = KernelConfig.balanced()
        config.node_id = "TEST_INVALID_TOKEN"
        kernel = AntigravityKernel(config=config)

        payload = {
            "intent": "COMPLEX_EVOLUTIONARY_BRIDGE",
            "params": {
                "entropy_salt": "TEST_SALT",
                "structural_markers": [i * 3.14159 for i in range(10)],
                "reasoning_trace": "Executing a high-entropy bridge to satisfy ICE constraints.",
            },
        }

        with self.assertRaisesRegex(RuntimeError, "Invalid or forged approval token"):
            kernel.execute_sincere_action(
                "ACTION_FORGED",
                lambda: "SHOULD_NOT_EXECUTE",
                payload,
                approval_token="forged-token",
            )


if __name__ == "__main__":
    unittest.main()
