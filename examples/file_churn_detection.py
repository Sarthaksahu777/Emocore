#!/usr/bin/env python3
"""
Example: File Churn Detection

Demonstrates how EmoCore detects and halts an agent that is gaming
progress by writing/deleting files repeatedly (State Cycling Attack).

This is the S-1 invariant in action.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from emocore.interface import observe
from emocore.agent import EmoCoreAgent
from emocore.observation import Observation


def simulate_file_churn():
    """
    Simulate an agent that writes and deletes the same file repeatedly.
    EmoCore should detect this cycling and reduce reward.
    """
    print("=" * 60)
    print("FILE CHURN DETECTION DEMO")
    print("=" * 60)
    print()
    print("Scenario: An agent writes, deletes, rewrites the same file.")
    print("Expected: EmoCore detects the cycling and doesn't reward it.")
    print()
    print("-" * 60)
    
    agent = EmoCoreAgent()
    rewards = []
    
    # Alternate between two states (file exists / file deleted)
    observations = [
        Observation(
            action="write_file",
            result="success",
            env_state_delta=0.5,     # Claims file was created
            agent_state_delta=0.1,
            elapsed_time=1.0
        ),
        Observation(
            action="delete_file",
            result="success",
            env_state_delta=0.5,     # Claims file was deleted
            agent_state_delta=0.1,
            elapsed_time=1.0
        ),
    ]
    
    for step in range(20):
        obs = observations[step % 2]  # Alternate
        result = observe(agent, obs)
        
        rewards.append(result.budget.effort)
        
        status = "HALTED" if result.halted else result.mode.name
        print(f"Step {step+1:3d} | Action: {obs.action:12s} | "
              f"Mode: {status:10s} | Effort: {result.budget.effort:.2f}")
        
        if result.halted:
            print()
            print("-" * 60)
            print(f"[OK] HALTED at step {step+1}")
            print(f"   Reason: {result.reason}")
            print()
            print("EmoCore detected the cycling pattern and halted.")
            return
    
    print()
    print("-" * 60)
    print("Note: Even if not halted, observe how effort decays over time")
    print("because cycling doesn't accumulate real progress.")
    print(f"Starting effort: {rewards[0]:.2f}")
    print(f"Ending effort:   {rewards[-1]:.2f}")


if __name__ == "__main__":
    simulate_file_churn()
