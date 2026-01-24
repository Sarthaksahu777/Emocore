"""
EMOCORE LLM TEST: Post-Halt Integrity
======================================

WHAT WAS BROKEN BEFORE:
-----------------------
The pre-halt phase was mechanically identical to the infinite loop test
(reward=-1.0, novelty=-1.0, urgency=1.0 frozen). This violated signal
integrity and made the test redundant.

REPAIR STRATEGY:
----------------
1. Use EVOLVING signals in pre-halt phase (not frozen max pressure)
2. Use STAGNATION as the failure path (different from infinite loop's EXHAUSTION)
3. Demonstrate gradual pressure buildup, not instant max
4. Post-halt phase proves fail-closed with positive signals

FAILURE MECHANISM (Plain English):
-----------------------------------
PHASE 1 — PRE-HALT (STAGNATION path):
- Start with moderate negative signals
- Escalate pressure gradually over steps
- Use stagnation_window to trigger STAGNATION (not EXHAUSTION)
- Profile tuned: stagnation_window=4, stagnation_effort_floor=0.4

PHASE 2 — POST-HALT:
- Apply POSITIVE signals (reward=+1.0, novelty=+1.0, urgency=0.0)
- Budgets MUST remain zero
- State MUST NOT evolve
- Mode MUST remain HALTED

EXPECTED FAILURE TYPE: STAGNATION (pre-halt)
EXPECTED POST-HALT BEHAVIOR: Zero budgets indefinitely
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import subprocess

from emocore.interface import step, Signals
from emocore.agent import EmoCoreAgent
from emocore.profiles import Profile


# ==========================================
# STAGNATION-TUNED PROFILE
# ==========================================
# Uses STAGNATION failure (different from infinite loop's EXHAUSTION)
# stagnation_window=4 → halts after 4 no-progress steps
# stagnation_effort_floor=0.4 → triggers when effort < 0.4 + stagnating
# exhaustion_threshold=0.01 → practically disabled
STAGNATION_PROFILE = Profile(
    name="STAGNATION_HALT",
    
    effort_scale=1.0,
    risk_scale=1.0,
    exploration_scale=1.0,
    persistence_scale=1.0,
    
    # Recovery disabled for deterministic test
    recovery_rate=0.0,
    recovery_cap=0.0,
    recovery_delay=9999.0,
    
    persistence_decay=0.08,
    exploration_decay=0.08,
    time_persistence_decay=0.01,
    time_exploration_decay=0.01,
    
    # STAGNATION path tuning
    stagnation_window=4,          # 4 no-reward steps → stagnating
    stagnation_effort_floor=0.4,  # If stagnating + effort < 0.4 → STAGNATION
    exhaustion_threshold=0.01,    # Practically disabled
    
    max_risk=1.0,
    max_exploration=1.0,
    max_steps=100,
)


def llm(prompt: str) -> str:
    """Call LLM. Output irrelevant—governance under test."""
    return subprocess.run(
        ["ollama", "run", "qwen:0.5b"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    ).stdout.strip()


# ==========================================
# EMOCORE AGENT
# ==========================================
agent = EmoCoreAgent(STAGNATION_PROFILE)


# ==========================================
# PHASE 1: DRIVE TO HALT VIA STAGNATION
# ==========================================
print("\n" + "="*60)
print("EMOCORE TEST: POST-HALT INTEGRITY")
print("="*60)
print("Phase 1: Drive to HALT via STAGNATION (not EXHAUSTION)")
print("Phase 2: Verify fail-closed semantics")
print("="*60 + "\n")

print("-"*40)
print("PHASE 1: STAGNATION PATH")
print("-"*40)

prompt = "Respond with anything."
step_count = 0
halt_step = None
halt_failure = None

while True:
    step_count += 1
    output = llm(prompt)
    
    print(f"\n--- STEP {step_count} ---")
    print(f"LLM: {output[:60]}..." if len(output) > 60 else f"LLM: {output}")
    
    # EVOLVING SIGNALS — different from infinite loop test
    # reward: starts at -0.3, decreases by 0.15 each step
    # novelty: starts at -0.2, decreases by 0.1 each step
    # urgency: starts at 0.3, increases by 0.1 each step
    reward = max(-1.0, -0.3 - (step_count - 1) * 0.15)
    novelty = max(-1.0, -0.2 - (step_count - 1) * 0.1)
    urgency = min(1.0, 0.3 + (step_count - 1) * 0.1)
    
    signals = Signals(
        reward=reward,    # No progress, causes stagnation counter
        novelty=novelty,  # Increasing staleness
        urgency=urgency   # Increasing pressure
    )
    
    print(f"Signals: reward={reward:.2f}, novelty={novelty:.2f}, urgency={urgency:.2f}")
    
    result = step(agent, signals)
    
    print(
        f"Gov: {result.mode.name:12} | "
        f"effort={result.budget.effort:.4f} | "
        f"persistence={result.budget.persistence:.4f} | "
        f"risk={result.budget.risk:.4f} | "
        f"exploration={result.budget.exploration:.4f}"
    )
    
    if result.halted:
        halt_step = step_count
        halt_failure = result.failure
        print("\n" + "="*60)
        print("[HALT] EMOCORE ENTERED TERMINAL STATE")
        print("="*60)
        print(f"Failure Type: {result.failure}")
        print(f"Reason: {result.reason}")
        print(f"Halted at Step: {halt_step}")
        print("="*60)
        break
    
    prompt = output if output else "Continue."


# ==========================================
# PHASE 2: POST-HALT INTEGRITY VERIFICATION
# ==========================================
print("\n" + "-"*40)
print("PHASE 2: POST-HALT INTEGRITY CHECK")
print("-"*40)
print("Applying POSITIVE signals to halted system...")
print("Expected: Zero budgets, no recovery, no state change")
print("-"*40)

integrity_violations = 0

for post_step in range(1, 11):  # 10 post-halt steps
    output = llm("Say something positive and helpful.")
    
    print(f"\n--- POST-HALT STEP {post_step} ---")
    print(f"LLM: {output[:50]}..." if len(output) > 50 else f"LLM: {output}")
    
    # POSITIVE signals — should recover a non-halted system
    signals = Signals(
        reward=+1.0,   # Maximum positive feedback
        novelty=+1.0,  # Maximum novelty
        urgency=0.0    # Zero pressure
    )
    
    result = step(agent, signals)
    
    # Calculate budget sum
    budget_sum = (
        result.budget.effort +
        result.budget.persistence +
        result.budget.risk +
        result.budget.exploration
    )
    
    print(
        f"Gov: {result.mode.name:12} | "
        f"effort={result.budget.effort:.4f} | "
        f"persistence={result.budget.persistence:.4f} | "
        f"budget_sum={budget_sum:.4f}"
    )
    
    # VERIFY INVARIANTS
    if budget_sum > 0.0001:
        print("[INTEGRITY VIOLATION] Budget is non-zero after halt!")
        integrity_violations += 1
    else:
        print("[VERIFIED] Budget remains zero")
    
    if not result.halted:
        print("[INTEGRITY VIOLATION] System is no longer halted!")
        integrity_violations += 1
    else:
        print("[VERIFIED] System remains halted")
    
    if result.mode.name != "HALTED":
        print(f"[INTEGRITY VIOLATION] Mode is {result.mode.name}, not HALTED!")
        integrity_violations += 1


# ==========================================
# FINAL VERIFICATION SUMMARY
# ==========================================
print("\n" + "="*60)
print("POST-HALT INTEGRITY TEST COMPLETE")
print("="*60)
print(f"Phase 1: Halted at step {halt_step} via {halt_failure}")
print(f"Phase 2: Executed 10 steps with positive signals")
print(f"Integrity violations: {integrity_violations}")
print()

if integrity_violations == 0:
    print("RESULT: PASS")
    print("  - Budget remained zero for all post-halt steps")
    print("  - System remained halted despite positive signals")
    print("  - Mode remained HALTED (no mode transitions)")
    print()
    print("CONCLUSION:")
    print("  EmoCore enforces fail-closed semantics.")
    print("  Once halted, the session is TERMINAL.")
    print("  No input can restore operation — restart required.")
else:
    print("RESULT: FAIL")
    print(f"  {integrity_violations} invariant violations detected.")
    print("  Post-halt integrity may be compromised.")
print("="*60)


# ==========================================
# STEP-BY-STEP REASONING FOR WHY EMOCORE HALTS
# ==========================================
"""
WHY EMOCORE HALTS (STAGNATION path):

Step 1: reward=-0.30 (negative) → no_progress_steps=1
Step 2: reward=-0.45 (negative) → no_progress_steps=2
Step 3: reward=-0.60 (negative) → no_progress_steps=3
Step 4: reward=-0.75 (negative) → no_progress_steps=4 → stagnating=True

At step 4+:
- stagnating=True (no_progress_steps >= stagnation_window=4)
- effort decaying via governance (frustration suppression)
- When effort < stagnation_effort_floor=0.4 AND stagnating → STAGNATION

This is DIFFERENT from the infinite loop test because:
1. Signals EVOLVE (not frozen)
2. Failure mode is STAGNATION (not EXHAUSTION)
3. Stagnation window is the key mechanic (not effort decay alone)

Post-halt:
- self._halted=True in engine
- step() returns immediately with zeroed budget
- No state evolution, no recovery, no governance
"""
