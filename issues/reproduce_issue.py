import os 
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core.agent import EmoCoreAgent

from core.profiles import PROFILES, ProfileType, Profile
from core.failures import FailureType

def debug_aggressive_vs_balanced():
    print("\n--- Debugging Aggressive vs Balanced ---")
    bal = EmoCoreAgent(profile=PROFILES[ProfileType.BALANCED])
    agg = EmoCoreAgent(profile=PROFILES[ProfileType.AGGRESSIVE])

    halted_bal = None
    halted_agg = None

    for i in range(10):
        if halted_bal is None:
            r = bal.step(0.0, 0.0, 0.0)
            if r.halted:
                halted_bal = i
                print(f"Balanced halted at step {i}")
                print(f"Reason: {r.reason}")
                print(f"Failure: {r.failure}")
                print(f"Budget: {r.budget}")
        
        if halted_agg is None:
            r = agg.step(0.0, 0.0, 0.0)
            if r.halted:
                halted_agg = i
                print(f"Aggressive halted at step {i}")
                print(f"Reason: {r.reason}")
                print(f"Failure: {r.failure}")
                print(f"Budget: {r.budget}")

def debug_overrisk():
    print("\n--- Debugging Overrisk ---")
    profile = Profile(
        name="test_overrisk",
        max_risk=0.3,
        max_exploration=1.0,
        exhaustion_threshold=0.0,
        stagnation_window=100,
        time_persistence_decay=0.5,
        time_exploration_decay=0.5,
        max_steps=10,
    )

    core = EmoCoreAgent(profile=profile)

    for i in range(10):
        out = core.step(
            reward=0.0,
            novelty=0.0,
            urgency=1.0 
        )
        print(f"Step {i}: Risk={out.budget.risk}, Effort={out.budget.effort}")
        if out.halted:
            print(f"Halted at step {i}")
            print(f"Reason: {out.reason}")
            print(f"Failure: {out.failure}")
            break

if __name__ == "__main__":
    debug_aggressive_vs_balanced()
    debug_overrisk()
