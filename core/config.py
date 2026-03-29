from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class KernelConfig:
    node_id: str
    mode: str
    sincere_min_legr: float
    sincere_max_legr: float
    sincere_target_legr: float
    chaos_rate: float
    archivist_enabled: bool
    harvest_dir: Path
    cycle_interval: float
    crossover_min_pool_size: int
    mutation_probability: float
    l1_template_length: int
    l1_value_min: float
    l1_value_max: float
    l2_chaos_rounds_min: int
    l2_chaos_rounds_max: int
    spr_similarity_threshold: float
    auto_persist: bool

    @classmethod
    def balanced(cls) -> "KernelConfig":
        repo_root = Path(__file__).resolve().parents[1]
        return cls(
            node_id="BALANCED_NODE",
            mode="BALANCED",
            sincere_min_legr=0.35,
            sincere_max_legr=0.95,
            sincere_target_legr=0.7,
            chaos_rate=0.25,
            archivist_enabled=False,
            harvest_dir=repo_root / "results" / "harvest",
            cycle_interval=0.05,
            crossover_min_pool_size=2,
            mutation_probability=0.5,
            l1_template_length=6,
            l1_value_min=0.1,
            l1_value_max=0.9,
            l2_chaos_rounds_min=1,
            l2_chaos_rounds_max=3,
            spr_similarity_threshold=0.85,
            auto_persist=False,
        )

    @classmethod
    def conservative(cls) -> "KernelConfig":
        config = cls.balanced()
        config.node_id = "CONSERVATIVE_NODE"
        config.mode = "CONSERVATIVE"
        config.chaos_rate = 0.15
        config.mutation_probability = 0.25
        config.spr_similarity_threshold = 0.75
        return config

