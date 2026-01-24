# BENCHMARKS/demo_failure_reply.py
"""
Demo: EmoCore Failure-Reply Pattern
Showcases how EmoCore detects stagnation and provides a structured failure 
that can be used to generate a helpful "reply" to the user/operator.
"""
import sys
import os
import time

# Ensure we can import emocore
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from emocore.engine import EmoEngine
from emocore.profiles import BALANCED
from emocore.failures import FailureType

def run_stagnation_demo():
    print("="*60)
    print("EMOCORE DEMO: STAGNATION DETECTION & FAILURE-REPLY")
    print("="*60)
    print("Scenario: An agent is stuck in a loop trying to solve a task but")
    print("making no progress. The budget is decaying, and the window is closing.")
    print("-" * 60)

    # Use BALANCED profile with a short stagnation window for the demo
    # We'll override the window to 5 steps to make the demo fast
    custom_profile = BALANCED.__class__(
        **{**BALANCED.__dict__, 'stagnation_window': 5, 'stagnation_effort_floor': 0.4}
    )
    
    engine = EmoEngine(profile=custom_profile)

    # Simulation loop
    print(f"{'Step':<5} | {'Mode':<10} | {'Effort':<8} | {'Persist':<8} | {'Frustr.':<8} | {'Reason'}")
    print("-" * 65)
    
    for step in range(1, 15):
        # Simulation: zero reward, low novelty, but some urgency
        # This causes Frustration and Arousal to climb, which suppresses effort.
        result = engine.step(reward=0.0, novelty=0.05, urgency=0.3)
        
        print(f"{step:02}    | {result.mode.name:<10} | {result.budget.effort:.2f}     | {result.budget.persistence:.2f}     | {result.state.frustration:.2f}     | {result.reason}")

        if result.halted:
            print("-" * 65)
            print(f"!!! GOVERNANCE HALT: {result.failure.name} !!!")
            
            # THE ADVANCED FAILURE-REPLY PATTERN
            # We use the internal state metadata to make the reply "non-cheap"
            reply = generate_sophisticated_reply(result)
            print("\nAGENT GOVERNANCE REPORT:")
            print(f"\"{reply}\"")
            print("-" * 65)
            break
        
        time.sleep(0.1)

def generate_sophisticated_reply(result) -> str:
    """
    Translates governance state into a technical status report.
    """
    failure = result.failure
    state = result.state
    
    if failure == FailureType.STAGNATION:
        return (f"Task execution halted due to sustained Stagnation (Velocity=0 for {result.reason} steps). "
                f"Internal Frustration metric reached {state.frustration:.2f}, causing behavioral effort "
                f"to fall below the safety floor. Strategic reassessment is required.")
    elif failure == FailureType.EXHAUSTION:
        return (f"Persistence budget depleted ({result.budget.effort:.2f}). "
                f"The agent has entered an unrecoverable state after sustained pressure. "
                "Cool-down or human intervention required.")
    else:
        return f"Autonomous governance halt triggered: {failure.name}. Reason: {result.reason}."

if __name__ == "__main__":
    run_stagnation_demo()
