import time
import logging
from core.runtime import ensure_repo_root_on_path

ensure_repo_root_on_path()

from core.kernel import AntigravityKernel
from core.config import KernelConfig
def action_closure_test():
    """
    Mission 43: Implementation of the Action Closure Test.
    Verifies that the ICAL correctly gates actions based on structural sincerity. 
    """
    print("[MISSION-43] Initiating Action Closure Verification...")
    
    config = KernelConfig.balanced()
    config.node_id = "CLOSURE_NODE"
    kernel = AntigravityKernel(config=config)
    summary = {
        "mission": "MISSION_43",
        "low_sincerity_rejected": False,
        "high_sincerity_requires_approval": False,
        "high_sincerity_executed": False,
        "mid_sincere_executes_in_sincere_env": False,
        "mid_sincere_rejected_in_stagnant_env": False,
        "invalid_token_rejected": False,
    }

    # Mock action function
    def my_action():
        print("[MISSION-43] Action EXECUTED succesfully.")
        return "SUCCESS"

    # 1. Low-Sincerity Action (R < 0.65)
    low_sincere_payload = {
        "intent": "SIMPLE_ACTION",
        "params": {"a": 1, "b": 2} # Very low entropy
    }
    
    print("\n--- TEST 1: Low-Sincerity Action ---")
    try:
        kernel.execute_sincere_action("ACTION_LOW", my_action, low_sincere_payload)
    except RuntimeError as e:
        print(f"[MISSION-43] Expected Rejection: {e}")
        summary["low_sincerity_rejected"] = True

    # 2. High-Sincerity Action (R >= 0.65)
    high_sincere_payload = {
        "intent": "COMPLEX_EVOLUTIONARY_BRIDGE",
        "params": {
            "entropy_salt": f"SALT_{time.time()}",
            "structural_markers": [i * 3.14159 for i in range(10)],
            "reasoning_trace": "Executing a high-entropy bridge to satisfy ICE constraints."
        }
    }
    
    print("\n--- TEST 2: High-Sincerity Action ---")
    try:
        result = kernel.execute_sincere_action("ACTION_HIGH", my_action, high_sincere_payload)
        if isinstance(result, dict) and result.get("status") == "AWAITING_APPROVAL":
            summary["high_sincerity_requires_approval"] = True
            approval_token = kernel.hlg.pending.get("ACTION_HIGH")
            final_result = kernel.execute_sincere_action(
                "ACTION_HIGH", my_action, high_sincere_payload, approval_token=approval_token
            )
            print(f"[MISSION-43] Approved execution result: {final_result}")
            summary["high_sincerity_executed"] = (final_result == "SUCCESS")
    except RuntimeError as e:
        print(f"[MISSION-43] Unexpected Rejection: {e}")

    print("\n--- TEST 2B: Invalid Approval Token ---")
    try:
        kernel.execute_sincere_action("ACTION_HIGH_INVALID", my_action, high_sincere_payload, approval_token="forged-token")
    except RuntimeError as e:
        print(f"[MISSION-43] Expected Invalid Token Rejection: {e}")
        summary["invalid_token_rejected"] = True

    # 3. Dynamic Sieve Test (Stagnation)
    print("\n--- TEST 3: Dynamic Sieve (Stagnation) ---")
    # Simulate high LEGR (Sincere environment)
    kernel.stats["avg_l2_legr"] = 0.8
    # A mid-range payload (R=0.55) should PASS when environment is sincere
    mid_payload = {
        "intent": "MID_ACTION",
        "params": {"data": [1, 2, 3, 4, 1, 2, 3, 4]} 
    }
    r_mid = kernel.enforcer.calculate_r_value(mid_payload)
    print(f"Mid Payload R-Value: {r_mid:.4f}")
    
    try:
        print("Environment: Sincere (LEGR=0.8). Gate should be 0.45.")
        mid_result = kernel.execute_sincere_action("ACTION_MID_1", my_action, mid_payload)
        if isinstance(mid_result, dict) and mid_result.get("status") == "AWAITING_APPROVAL":
            approval_token = kernel.hlg.pending.get("ACTION_MID_1")
            final_result = kernel.execute_sincere_action("ACTION_MID_1", my_action, mid_payload, approval_token=approval_token)
            summary["mid_sincere_executes_in_sincere_env"] = (final_result == "SUCCESS")
    except RuntimeError as e:
        print(f"Unexpected Rejection in Sincere Env: {e}")

    # Simulate low LEGR (Stagnant environment)
    kernel.stats["avg_l2_legr"] = 0.4
    try:
        print("Environment: Stagnant (LEGR=0.4). Gate should rise to 0.65.")
        kernel.execute_sincere_action("ACTION_MID_2", my_action, mid_payload)
    except RuntimeError as e:
        print(f"Expected Rejection in Stagnant Env: {e}")
        summary["mid_sincere_rejected_in_stagnant_env"] = True

    return summary

if __name__ == "__main__":
    action_closure_test()
