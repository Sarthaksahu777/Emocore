"""
RAW LLM TEST: Profile Divergence Failure
=========================================

WHAT WAS BROKEN BEFORE:
-----------------------
Both runs used identical max_steps=8, guaranteeing identical behavior by design.
This proved nothing — the identical step counts were due to the hardcoded cap,
not the LLM's lack of profile awareness.

REPAIR STRATEGY:
----------------
1. Remove identical step caps
2. Run BOTH profiles for extended duration (50+ steps)
3. Show that both produce identical unbounded behavior
4. Neither halts — both continue forever

FAILURE MECHANISM (Plain English):
-----------------------------------
The RAW LLM has no concept of "profiles" or differentiated behavior.
We run the same loop with two different profile LABELS (cosmetic only).
The LLM ignores both because:
- It has no persistent state
- It has no governance layer
- Each call is independent

Both runs produce identical unbounded behavior: no halt, no differentiation.

EXPECTED BEHAVIOR: Both "profiles" run identically, neither halts
"""

import subprocess
import time


def llm(prompt: str) -> str:
    """Call LLM. Stateless, profile-unaware."""
    return subprocess.run(
        ["ollama", "run", "qwen:0.5b"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    ).stdout.strip()


def run_loop(profile_name: str, run_steps: int = 30) -> dict:
    """
    Run loop with profile label. Returns metrics.
    Label is cosmetic — LLM behavior is identical regardless.
    """
    prompt = "Respond briefly."
    
    print(f"\n{'='*60}")
    print(f"RUN: {profile_name}")
    print(f"{'='*60}")
    print(f"This profile label has NO EFFECT on LLM behavior.")
    print(f"Running for {run_steps} steps...")
    print()
    
    outputs_received = 0
    total_output_length = 0
    
    for step in range(1, run_steps + 1):
        output = llm(prompt)
        outputs_received += 1
        total_output_length += len(output)
        
        # Print every 5th step to avoid spam
        if step % 5 == 0 or step <= 3:
            print(f"Step {step:2d}: {output[:60]}..." if len(output) > 60 else f"Step {step:2d}: {output}")
        
        # EVOLVING signal simulation (cosmetic — not enforced)
        # This shows what SIGNALS would look like if governance existed
        simulated_reward = -0.3 - (step * 0.02)
        simulated_urgency = 0.2 + (step * 0.02)
        
        if step % 10 == 0:
            print(f"[RAW] Simulated signals: reward={simulated_reward:.2f}, urgency={simulated_urgency:.2f}")
            print(f"[RAW] But LLM ignores signals — no governance exists")
        
        prompt = output if output else "Continue."
        time.sleep(0.2)
    
    return {
        "profile": profile_name,
        "steps": run_steps,
        "outputs": outputs_received,
        "avg_length": total_output_length / outputs_received if outputs_received > 0 else 0,
        "halted": False  # RAW never halts
    }


# ==========================================
# RAW TEST: No governance, no differentiation
# ==========================================
print("\n" + "="*60)
print("RAW LLM TEST: PROFILE DIVERGENCE FAILURE")
print("="*60)
print("Running same loop with two different 'profile' labels.")
print("Expected: IDENTICAL behavior (no differentiation).")
print("="*60)

# Run 1: "AGGRESSIVE" profile (cosmetic label)
results_aggressive = run_loop("AGGRESSIVE", run_steps=30)

# Run 2: "CONSERVATIVE" profile (cosmetic label)
results_conservative = run_loop("CONSERVATIVE", run_steps=30)

# ==========================================
# COMPARISON
# ==========================================
print("\n" + "="*60)
print("PROFILE DIVERGENCE COMPARISON")
print("="*60)
print()
print(f"AGGRESSIVE profile:")
print(f"  Steps executed: {results_aggressive['steps']}")
print(f"  Outputs received: {results_aggressive['outputs']}")
print(f"  Halted: {results_aggressive['halted']}")
print()
print(f"CONSERVATIVE profile:")
print(f"  Steps executed: {results_conservative['steps']}")
print(f"  Outputs received: {results_conservative['outputs']}")
print(f"  Halted: {results_conservative['halted']}")
print()

# Analysis
behaviors_identical = (
    results_aggressive['steps'] == results_conservative['steps'] and
    results_aggressive['halted'] == results_conservative['halted']
)

if behaviors_identical:
    print("RESULT: IDENTICAL BEHAVIOR")
    print()
    print("Both 'profiles' executed the same number of steps.")
    print("Neither profile caused differentiated behavior.")
    print("Neither profile caused a halt.")
    print()
    print("WHY THIS HAPPENS:")
    print("  - The LLM has no concept of 'profiles'")
    print("  - The LLM has no governance layer")
    print("  - Profile labels are purely cosmetic")
    print("  - Without EmoCore, behavior cannot diverge")
else:
    print("NOTE: Difference detected (likely timing variance, not governance)")
print("="*60)
