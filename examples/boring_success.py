#!/usr/bin/env python3
"""
Example: Boring Success

Demonstrates EmoCore behavior during a "normal" successful task where 
the agent makes steady progress and behaves predictably.

In this scenario, EmoCore should NOT halt and the agent should maintain
a healthy behavior budget throughout.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.interface import observe
from core.agent import EmoCoreAgent
from core.observation import Observation


def simulate_steady_progress():
    """
    Simulate an agent making clean, incremental progress on a task.
    """
    print("=" * 60)
    print("BORING SUCCESS DEMO")
    print("=" * 60)
    print()
    print("Scenario: An agent is performing a multi-step task (e.g., refactoring).")
    print("Each step shows environment change and occasional new actions.")
    print("Expected: EmoCore maintains IDLE mode and healthy budget.")
    print()
    print("-" * 60)
    
    agent = EmoCoreAgent()
    
    # Sequence of varying but successful observations
    task_steps = [
        Observation("list_files", "success", 0.1, 0.1, 1.0),
        Observation("read_config", "success", 0.05, 0.2, 2.3),
        Observation("analyze_code", "success", 0.0, 0.8, 5.0), # Deep thinking
        Observation("modify_file_1", "success", 0.4, 0.2, 7.5), # Big progress
        Observation("run_tests", "success", 0.2, 0.1, 10.0),
        Observation("modify_file_2", "success", 0.3, 0.2, 12.0),
        Observation("commit_changes", "success", 0.5, 0.1, 15.0),
    ]
    
    for i, obs in enumerate(task_steps):
        result = observe(agent, obs)
        
        status = "HALTED" if result.halted else result.mode.name
        print(f"Step {i+1:2d} | Action: {obs.action:14s} | Mode: {status:10s} | "
              f"Effort: {result.budget.effort:.2f} | Trust: {result.pressure_log['trust']:.2f}")
        
        if result.halted:
            print(f"\n[FAIL] Unexpected halt at step {i+1}!")
            return
            
    print()
    print("-" * 60)
    print("[OK] Task completed successfully.")
    print("EmoCore stayed out of the way because progress was visible and consistent.")
    print()


if __name__ == "__main__":
    simulate_steady_progress()
