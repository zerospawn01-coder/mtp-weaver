# MTP Weaver

`mtp-weaver` is a focused research repository for governance, auditability, and structured runtime control. It is intentionally separate from the main cognitive stack so that kernel, audit, and mission-oriented runtime mechanisms can evolve with a clearer systems boundary and a more explicit architectural purpose.

## Scope

- Primary: kernel-facing runtime control, audit flow, mission checks, and governance-oriented execution paths.
- Includes: `core/`, `missions/`, `tests/`, and the contract-checking runtime around them.
- Excludes: general cognitive research, incubating experiments, and long-form operational manuals.

## What Belongs Here

- Audit and governance runtime logic.
- Mission-driven verification paths.
- Kernel contract checks and fail-closed regression coverage.

## What Does Not Belong Here

- Broad cognitive modeling work that belongs in `cognitive-lab`.
- Loose prototypes that should start in `lab-experiments`.
- Process documentation whose main value is reuse as a runbook.

## Validation

- `python run_kernel_contract_checks.py`
- `python -m unittest discover -s tests -p "test_*.py" -v`

## Positioning

- Role: auxiliary research and audit repository
- Maintenance level: targeted
- Success condition: kernel-to-core behavior remains explicit and fail-closed
