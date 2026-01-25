#!/usr/bin/env python3
"""
Example: LLM Adapter Demo
=========================

This example demonstrates the Plug-and-Play governance using the
LLMLoopAdapter. It shows how EmoCore can be integrated into an 
existing LLM generation loop with minimal boilerplate.

Scenario:
---------
An LLM agent is trying to solve a task. It succeeds in some steps 
but hits a "stagnation" point where it repeats the same reasoning 
without affecting the environment. EmoCore detects this and halts.
"""

import sys
import os
import time
import random

# Add src to path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from emocore import EmoCoreAgent, LLMLoopAdapter

def simulate_llm_task():
    print("=" * 60)
    print("LLM ADAPTER DEMO: Automated Governance")
    print("=" * 60)
    
    # 1. Initialize EmoCore with CONSERVATIVE profile for faster feedback
    from emocore.profiles import PROFILES, ProfileType
    agent = EmoCoreAgent(PROFILES[ProfileType.CONSERVATIVE])
    
    # Custom extractor with tighter limits for the demo
    from emocore.extractor import RuleBasedExtractor
    extractor = RuleBasedExtractor(step_limit=15, stagnation_limit=2)
    
    adapter = LLMLoopAdapter(agent)
    
    print("Agent started. Goal: Modify a configuration file.")
    print("-" * 60)
    
    # 2. Simulated LLM Loop
    for step in range(1, 21):
        # --- Start of LLM Step ---
        adapter.start_step()
        
        # Simulate LLM reasoning and action
        print(f"\n[Step {step}] LLM is thinking...")
        time.sleep(0.5) # Thinking time
        
        if step < 4:
            # First few steps: making progress
            action = "identify_config_path"
            result = "success"
            env_delta = 0.2  # Found the file
            reasoning = "I have located the file at /etc/app.conf"
        elif step == 4:
            action = "modify_parameter"
            result = "success"
            env_delta = 0.6  # Actually changed the world!
            reasoning = "Successfully updated 'max_retries' to 5."
        else:
            # Stagnation starts here
            action = "verify_change"
            result = "success" # It "succeeds" at checking
            env_delta = 0.0    # But no new change in the world
            reasoning = "Verifying the change again... looks correct."
            
        print(f"Action: {action}")
        print(f"Outcome: {result} (Env Delta: {env_delta})")
        print(f"Reasoning: {reasoning}")
        
        # 3. Governance check via Adapter
        # Note: No manual Signals or Observation construction needed!
        res = adapter.end_step(
            action=action,
            result=result,
            env_delta=env_delta,
            agent_delta=0.0, # Absolutely no change in reasoning (looping)
            extractor=extractor
        )
        
        # --- End of LLM Step ---
        
        print(f"Gov Status: {res.mode.name} | Effort: {res.budget.effort:.2f}")
        
        if res.halted:
            print("\n" + "!" * 60)
            print("EMOCORE HALTED EXECUTION")
            print(f"Reason: {res.reason}")
            print(f"Failure Type: {res.failure.name}")
            print("!" * 60)
            print("\nEmoCore detected that after Step 4, no further progress")
            print("was being made despite the agent claiming success.")
            break
            
    print("\nDemo complete.")

if __name__ == "__main__":
    simulate_llm_task()
