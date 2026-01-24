#!/usr/bin/env python3
"""
Example: Infinite Loop Fix

Demonstrates how EmoCore detects and halts an agent that is stuck in an
infinite loop of repeated actions without making progress.

This is the canonical "exploration theater" scenario.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from emocore.interface import observe
from emocore.agent import EmoCoreAgent
from emocore.observation import Observation


def simulate_infinite_loop():
    """
    Simulate an agent that keeps trying the same action forever.
    EmoCore should detect this and halt.
    """
    print("=" * 60)
    print("INFINITE LOOP FIX DEMO")
    print("=" * 60)
    print()
    print("Scenario: An agent keeps calling 'search_web' but gets no results.")
    print("Expected: EmoCore halts the agent before too many wasted steps.")
    print()
    print("-" * 60)
    
    agent = EmoCoreAgent()
    
    # The agent keeps trying the same thing
    obs = Observation(
        action="search_web",
        result="success",        # It "succeeds" but...
        env_state_delta=0.0,     # ...nothing in the world changes
        agent_state_delta=0.1,   # It thinks it's working
        elapsed_time=1.0
    )
    
    for step in range(100):
        result = observe(agent, obs)
        
        status = "HALTED" if result.halted else result.mode.name
        print(f"Step {step+1:3d} | Mode: {status:10s} | "
              f"Effort: {result.budget.effort:.2f} | "
              f"Frustration: {result.pressure_log['frustration']:+.2f}")
        
        if result.halted:
            print()
            print("-" * 60)
            print(f"[OK] HALTED at step {step+1}")
            print(f"   Reason: {result.reason}")
            print(f"   Failure Type: {result.failure.name}")
            print()
            print("EmoCore detected that the agent was making no real progress")
            print("and stopped it before wasting more resources.")
            return step + 1
    
    print("[FAIL] Agent did not halt (unexpected)")
    return 100


if __name__ == "__main__":
    steps = simulate_infinite_loop()
    print(f"\nTotal steps before halt: {steps}")
