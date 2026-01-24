#!/usr/bin/env python3
"""
Example: Retry Storm

Demonstrates how EmoCore detects and halts an agent that keeps retrying
a failing operation without making progress.

This catches API errors, network failures, and tool call loops.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.interface import observe
from core.agent import EmoCoreAgent
from core.observation import Observation


def simulate_retry_storm():
    """
    Simulate an agent that keeps retrying a failing API call.
    EmoCore should detect this and halt before excessive retries.
    """
    print("=" * 60)
    print("RETRY STORM DEMO")
    print("=" * 60)
    print()
    print("Scenario: An agent keeps calling an API that returns 500 errors.")
    print("Expected: EmoCore halts quickly due to frustration spike.")
    print()
    print("-" * 60)
    
    agent = EmoCoreAgent()
    
    for step in range(50):
        # Simulate a failing API call
        obs = Observation(
            action="call_external_api",
            result="failure",        # API keeps failing
            env_state_delta=0.0,     # No progress
            agent_state_delta=0.0,   # No internal change either
            elapsed_time=0.5,        # Quick retries
            error="HTTP 500: Internal Server Error"
        )
        
        result = observe(agent, obs)
        
        status = "HALTED" if result.halted else result.mode.name
        print(f"Step {step+1:3d} | Mode: {status:10s} | "
              f"Effort: {result.budget.effort:.2f} | "
              f"Difficulty: {result.pressure_log.get('frustration', 0):+.2f}")
        
        if result.halted:
            print()
            print("-" * 60)
            print(f"[OK] HALTED at step {step+1}")
            print(f"   Reason: {result.reason}")
            print(f"   Failure Type: {result.failure.name}")
            print()
            print("EmoCore detected the failure streak and stopped")
            print("before wasting more API calls.")
            return step + 1
    
    print("[FAIL] Agent did not halt (unexpected)")
    return 50


if __name__ == "__main__":
    steps = simulate_retry_storm()
    print(f"\nTotal retry attempts before halt: {steps}")
