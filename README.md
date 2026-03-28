# MTP Weaver

`mtp-weaver` is a focused research repository for governance, auditability, and structured runtime control. It is intentionally separate from the main cognitive stack so that kernel, audit, and mission-oriented runtime mechanisms can evolve with a clearer systems boundary and a more explicit architectural purpose.

## Scope

- Primary: kernel-facing runtime control, audit flow, mission checks, and governance-oriented execution paths.
- Includes: `core/`, `missions/`, `tests/`, and the contract-checking runtime around them.
- Excludes: general cognitive research, incubating experiments, and long-form operational manuals.

## Non-goals

- Absorbing broad cognitive modeling work that belongs in `cognitive-lab`.
- Becoming a catch-all repository for unrelated technical artifacts.
- Replacing `project-manuals` as the home for reusable process documentation.

## Inputs

- Kernel contracts and runtime assumptions that need explicit audit boundaries.
- Mission flows that must prove fail-closed behavior.
- Governance-oriented experiments that are too specialized for the mainline cognitive repository.

## Outputs

- Runnable kernel-to-core validation paths.
- Audit and mission control surfaces with explicit failure behavior.
- A repository boundary that makes governance runtime work easier to reason about and review.

## Validation

- `python run_kernel_contract_checks.py`
- `python -m unittest discover -s tests -p "test_*.py" -v`

## Promotion Path

- Inbound: governance and audit runtime work that needs a dedicated systems boundary.
- Outbound: reusable procedures should be documented in `project-manuals`, not hidden here.
- Repository role: auxiliary research and audit repository with targeted maintenance.
