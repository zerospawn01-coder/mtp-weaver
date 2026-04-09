import json
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


class CiGateTests(unittest.TestCase):
    def run_gate(self, gate: str) -> dict[str, object]:
        completed = subprocess.run(
            [sys.executable, "tools/ci_gate.py", gate],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, msg=completed.stdout + completed.stderr)
        return json.loads(completed.stdout)

    def test_validate_kernel_contract_gate_passes(self) -> None:
        payload = self.run_gate("validate-kernel-contract")
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["gate"], "validate-kernel-contract")

    def test_validate_mission_regression_gate_passes(self) -> None:
        payload = self.run_gate("validate-mission-regression")
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["gate"], "validate-mission-regression")

    def test_validate_governance_gate_passes(self) -> None:
        payload = self.run_gate("validate-governance")
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["gate"], "validate-governance")

    def test_internal_gate_errors_are_normalized(self) -> None:
        import tools.ci_gate as ci_gate

        original_gate = ci_gate.GATES["validate-governance"]

        def boom() -> int:
            raise RuntimeError("boom")

        ci_gate.GATES["validate-governance"] = boom
        try:
            stdout = StringIO()
            with redirect_stdout(stdout):
                code = ci_gate.main(["tools/ci_gate.py", "validate-governance"])
        finally:
            ci_gate.GATES["validate-governance"] = original_gate

        self.assertEqual(code, 1)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["status"], "FAIL")
        self.assertEqual(payload["gate"], "validate-governance")
        self.assertEqual(payload["violations"][0]["type"], "INTERNAL_CI_ERROR")


if __name__ == "__main__":
    unittest.main()
