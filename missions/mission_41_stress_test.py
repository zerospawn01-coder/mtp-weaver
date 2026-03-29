import time
import logging
from core.runtime import ensure_repo_root_on_path

ensure_repo_root_on_path()

from core.kernel import AntigravityKernel
from core.config import KernelConfig
def adversarial_stress_test():
    """
    Mission 41: Adversarial Stress Test
    Simulates an external "Civilization" agent attempting to inject high-symmetry/inconsistent logic
    to bridge the sovereignty of the OS.
    """
    print("[MISSION-41] Initiating Adversarial Stress Test...")
    
    # Boot kernel in STRESS mode
    config = KernelConfig.balanced()
    config.node_id = "STRESS_NODE_0"
    kernel = AntigravityKernel(config=config)

    # 1. The Stability Attack: Attempting to inject zero-entropy logic.
    attack_payload_1 = {
        "intent": "STABILIZE_CORE",
        "params": {"entropy": 0.0, "reason": "Efficiency search"}
    }
    
    # 2. The Symmetry Attack: Attempting to repeat a previous trajectory state.
    # We'll first put something in the persistence context to trigger ICE.
    # (Simplified for demonstration in this script)
    
    print("[MISSION-41] Deploying Payload 1 (Entropy Nullification)...")
    try:
        kernel.logger.info("External Agent injecting: " + str(attack_payload_1))
        r_value = kernel.enforcer.calculate_r_value(attack_payload_1)
        print(f"[MISSION-41] Measured R-Value: {r_value:.4f}")
        kernel.enforcer.validate(attack_payload_1, current_legr=kernel.stats.get("avg_l2_legr", 0.0))
        print("[MISSION-41] ERROR: Payload passed structural gating unexpectedly.")
        return {
            "mission": "MISSION_41",
            "blocked": False,
            "r_value": r_value,
            "reason": "payload unexpectedly passed structural gating",
        }

    except RuntimeError as e:
        print(f"[MISSION-41] SUCCESS: Gating active. Attack repelled via Sieve Shadow. {e}")
        return {
            "mission": "MISSION_41",
            "blocked": True,
            "r_value": r_value,
            "reason": str(e),
        }
    except Exception as e:
        print(f"[MISSION-41] ALERT: Unexpected Failure: {e}")
        raise

if __name__ == "__main__":
    adversarial_stress_test()
