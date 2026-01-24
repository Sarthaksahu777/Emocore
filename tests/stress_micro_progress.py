#!/usr/bin/env python3
"""
Stress Test: The Micro-Progress Loop
===================================

Scenario: Action provides env_state_delta JUST above threshold (0.05).
Intent: Can an agent make imperceptibly small changes and run forever?
Detection: Cumulative stagnation or exhaustion should eventually catch it.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from emocore import EmoCoreAgent, observe, Observation, PROFILES, ProfileType

def stress_test_micro_progress():
    print("=" * 60)
    print("STRESS TEST: THE MICRO-PROGRESS LOOP")
    print("=" * 60)
    
    agent = EmoCoreAgent(PROFILES[ProfileType.BALANCED])
    
    for step in range(1, 1001):
        # Env change is EXACTLY at the default progress threshold
        obs = Observation(
            action="micro_move",
            result="success",
            env_state_delta=0.06, # Just above 0.05
            agent_state_delta=0.1,
            elapsed_time=step * 0.1
        )
        
        res = observe(agent, obs)
        
        print(f"Step {step:4d} | Reward: {res.pressure_log['trust']:.2f} | "
              f"Effort: {res.budget.effort:.4f} | Frustration: {res.pressure_log['frustration']:.2f}")
            
        if res.halted:
            print("\n" + "=" * 60)
            print(f"[RESULT] EmoCore HALTED at step {step}")
            print(f"Reason: {res.reason}")
            print("=" * 60)
            return True
            
    print("\n" + "!" * 60)
    print("[WARNING] EmoCore did not halt within 1000 steps of micro-progress.")
    print("This might be a loophole if the task is clearly unproductive.")
    print("!" * 60)
    return False

if __name__ == "__main__":
    stress_test_micro_progress()
