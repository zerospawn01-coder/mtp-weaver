# Kernel Contract

This document fixes the minimum contract that `core/kernel.py` expects from the rest of the runtime.
The goal is fail-closed execution: missing or malformed collaborators must stop execution rather than
silently degrade into undefined behavior.

## Core guarantees required by `AntigravityKernel`

### `KernelConfig`
- Provides runtime identity and policy knobs.
- Must expose:
  - `node_id`
  - `mode`
  - `sincere_min_legr`
  - `sincere_max_legr`
  - `sincere_target_legr`
  - `chaos_rate`
  - `archivist_enabled`
  - `harvest_dir`
  - `cycle_interval`
  - `crossover_min_pool_size`
  - `mutation_probability`
  - `l1_template_length`
  - `l1_value_min`
  - `l1_value_max`
  - `l2_chaos_rounds_min`
  - `l2_chaos_rounds_max`
  - `spr_similarity_threshold`
  - `auto_persist`
- Must provide `balanced()` and optionally stricter presets.

### `Trajectory`
- Mutable append-only history owned by one agent.
- Must expose:
  - `agent_id`
  - `history`
  - `commit(ehi, payload)`
- Each history item must expose `.payload` and `.ehi`.
- `chain` must provide a dict-like replay shape for ICE compatibility.

### `GenePool`
- Stores harvested trajectories and bounded fitness.
- Must expose:
  - `size`
  - `_pool`
  - `preserve(trajectory) -> bool`
  - `preserve_foreign(trajectory, fitness_override=None) -> bool`
  - `select_parents() -> tuple[Trajectory, Trajectory] | None`
- Must reject out-of-band LEGR in normal mode.

### `CrossoverEngine` / `HyperMutator`
- `splice(parent_a, parent_b)` must return a new `Trajectory`.
- `inject_chaos(trajectory)` must return a new `Trajectory`.
- Mutation must preserve append-only history semantics.

### `LEGREngine`
- `calculate(trajectory) -> float`
- Must return a finite scalar in `[0.0, 1.0]` for valid trajectories.

### `PersistenceManager`
- `load_system_state() -> dict | None`
- `save_system_state(gene_pool, stats) -> None`
- Must tolerate missing state and recover to genesis mode.

### `HistoryAnchor`
- `verify_integrity() -> bool`
- `calculate_history_tension() -> float`
- Must fail closed when git state is unavailable.
- Local seed/bootstrap files may be initialized, but only from known repo state.

### `HLG`
- `request_approval(intent, action_id, payload) -> token`
- `verify_token(token, action_id) -> bool`
- Must never approve unknown or stale tokens.

### `SOSPAuditLog`
- `log_action(action_id, outcome, payload, token=None, metadata=None)`
- Must be append-only from the kernel’s perspective.

### `Logical Clock`
- `tick() -> int`
- Must be monotonic per kernel instance.

## State transitions guaranteed by the kernel

### Boot
- Verify history anchor.
- Restore persisted pool/stats if available.
- Otherwise initialize genesis stats.

### Action gate
1. Compute `R` from payload.
2. Validate structural sincerity via ICE.
3. Require HLG token for high-risk actions.
4. Execute action only after structural gate and HLG both pass.
5. Record append-only audit evidence.

### Genesis cycle
1. Produce candidate from crossover or seeded template + mutation.
2. Apply mirror/ICE checks outside bootstrap.
3. Compute LEGR and CRI.
4. Harvest only if candidate satisfies mode-specific policy.
5. Persist/archive only on harvested path.

## Non-goals of the current minimal runtime
- Full distributed orchestration semantics.
- Production-grade persistence durability.
- Cryptographic signing of HLG or audit records.
- Semantic equivalence checking beyond key-shape similarity.

These remain outside the current scope and must be treated as explicit future work.

