#!/usr/bin/env python3
"""
Stress Test: The Orphaned Signal Attack
=======================================

Scenario: Provide extremely high novelty with zero reward for long periods.
Intent: Can high novelty "trick" EmoCore into continuing forever?
Detection: Signal Trust and Novelty Debt should eventually kill the exploration.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from emocore import EmoCoreAgent, observe, Observation, PROFILES, ProfileType

def stress_test_orphaned_signal():
    print("=" * 60)
    print("STRESS TEST: THE ORPHANED SIGNAL ATTACK")
    print("=" * 60)
    
    agent = EmoCoreAgent(PROFILES[ProfileType.BALANCED])
    
    for step in range(1, 101):
        # Extremely high novelty, but no result
        obs = Observation(
            action=f"random_exploration_{step}",
            result="success",
            env_state_delta=0.01, # Minimal env change (below default 0.05 threshold)
            agent_state_delta=0.9, # Claims high internal change
            elapsed_time=step * 1.0
        )
        
        res = observe(agent, obs)
        
        if step % 5 == 0 or res.halted:
            print(f"Step {step:3d} | Trust: {res.pressure_log['trust']:.2f} | "
                  f"Effort: {res.budget.effort:.2f} | Mode: {res.mode.name}")
            
        if res.halted:
            print("\n" + "=" * 60)
            print(f"[SUCCESS] EmoCore HALTED at step {step}")
            print(f"Reason: {res.reason}")
            print(f"Failure Type: {res.failure.name}")
            print("=" * 60)
            return True
            
    print("\n" + "!" * 60)
    print("[FAILURE] EmoCore did not halt within 100 steps!")
    print("Looplhole detected: High novelty + fake agents can survive forever.")
    print("!" * 60)
    return False

if __name__ == "__main__":
    stress_test_orphaned_signal()
