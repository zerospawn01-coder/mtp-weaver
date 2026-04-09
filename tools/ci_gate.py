"""Fail-closed CI gates for MTP Weaver."""

from __future__ import annotations

import json
import subprocess
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


class GateFailure(RuntimeError):
    """Raised when a CI gate must fail closed."""

    def __init__(
        self,
        gate: str,
        violation_type: str,
        reason: str,
        file: str | None = None,
        violation_id: str | None = None,
    ) -> None:
        super().__init__(reason)
        self.gate = gate
        self.violation_type = violation_type
        self.reason = reason
        self.file = file
        self.violation_id = violation_id or gate


def _emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _pass(gate: str, details: dict[str, Any] | None = None) -> int:
    payload = {"gate": gate, "status": "PASS"}
    if details:
        payload["details"] = details
    _emit(payload)
    return 0


def _fail(gate: str, error: GateFailure) -> int:
    _emit(
        {
            "gate": gate,
            "status": "FAIL",
            "violations": [
                {
                    "type": error.violation_type,
                    "id": error.violation_id,
                    "file": error.file or "",
                    "reason": error.reason,
                }
            ],
        }
    )
    return 1


def _run(command: list[str], gate: str, violation_id: str, file: str) -> str:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        reason = (completed.stdout + "\n" + completed.stderr).strip()
        raise GateFailure(
            gate=gate,
            violation_type="COMMAND_FAILURE",
            violation_id=violation_id,
            file=file,
            reason=reason or f"Command failed: {' '.join(command)}",
        )
    return completed.stdout


def run_validate_kernel_contract() -> int:
    gate = "validate-kernel-contract"
    output = _run(
        [sys.executable, "run_kernel_contract_checks.py"],
        gate=gate,
        violation_id="kernel-contract",
        file="run_kernel_contract_checks.py",
    )
    if "[VERIFY] Kernel contract checks complete" not in output:
        raise GateFailure(
            gate=gate,
            violation_type="KERNEL_CONTRACT_VIOLATION",
            violation_id="kernel-contract-output",
            file="run_kernel_contract_checks.py",
            reason="Kernel contract checks did not reach the expected completion marker.",
        )
    return _pass(gate, {"command": "python run_kernel_contract_checks.py"})


def run_validate_mission_regression() -> int:
    gate = "validate-mission-regression"
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from run_kernel_contract_checks import run_checks

    with redirect_stdout(StringIO()):
        result = run_checks()
    mission_41 = result["missions"]["mission_41"]
    mission_43 = result["missions"]["mission_43"]
    if not result["success"]:
        raise GateFailure(
            gate=gate,
            violation_type="MISSION_REGRESSION",
            violation_id="kernel-regression",
            file="run_kernel_contract_checks.py",
            reason="Kernel mission regression path returned success=false.",
        )
    return _pass(
        gate,
        {
            "mission_41_blocked": bool(mission_41.get("blocked")),
            "mission_43_checks": {
                "low_sincerity_rejected": bool(mission_43.get("low_sincerity_rejected")),
                "high_sincerity_requires_approval": bool(
                    mission_43.get("high_sincerity_requires_approval")
                ),
                "high_sincerity_executed": bool(mission_43.get("high_sincerity_executed")),
                "mid_sincere_executes_in_sincere_env": bool(
                    mission_43.get("mid_sincere_executes_in_sincere_env")
                ),
                "mid_sincere_rejected_in_stagnant_env": bool(
                    mission_43.get("mid_sincere_rejected_in_stagnant_env")
                ),
                "invalid_token_rejected": bool(mission_43.get("invalid_token_rejected")),
            },
        },
    )


def run_validate_governance() -> int:
    gate = "validate-governance"
    required_files = [
        "README.md",
        "KERNEL_CONTRACT.md",
        "run_kernel_contract_checks.py",
        "tests/test_kernel_contract.py",
        "core/kernel.py",
        "core/config.py",
        "missions/mission_41_stress_test.py",
        "missions/mission_43_closure.py",
    ]
    missing = [path for path in required_files if not (REPO_ROOT / path).is_file()]
    if missing:
        raise GateFailure(
            gate=gate,
            violation_type="GOVERNANCE_VIOLATION",
            violation_id="required-files",
            file="",
            reason="Missing required contract or regression files: " + ", ".join(missing),
        )
    return _pass(gate, {"required_files": required_files})


def run_unit_tests() -> int:
    gate = "unit-tests"
    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-p",
        "test_*.py",
        "-v",
    ]
    _run(command, gate=gate, violation_id="unittest", file="tests/")
    return _pass(gate, {"command": " ".join(command[1:])})


GATES = {
    "validate-kernel-contract": run_validate_kernel_contract,
    "validate-mission-regression": run_validate_mission_regression,
    "validate-governance": run_validate_governance,
    "unit-tests": run_unit_tests,
}


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in GATES:
        print("Usage: python tools/ci_gate.py <gate>", file=sys.stderr)
        print("Available gates:", ", ".join(sorted(GATES.keys())), file=sys.stderr)
        return 2
    gate = argv[1]
    try:
        return GATES[gate]()
    except GateFailure as error:
        return _fail(gate, error)
    except Exception as error:
        return _fail(
            gate,
            GateFailure(
                gate=gate,
                violation_type="INTERNAL_CI_ERROR",
                violation_id=gate,
                reason=str(error) or "Unexpected CI gate failure.",
            ),
        )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
