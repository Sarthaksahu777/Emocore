"""
EMOCORE LLM TEST: Profile Divergence
=====================================

WHAT WAS BROKEN BEFORE:
-----------------------
1. Signals were frozen at constant values (violated signal integrity)
2. TOLERANT profile halted via EXTERNAL (not a governance failure)
3. The contrast was: EXHAUSTION vs EXTERNAL — one is governance, one is safety fuse

REPAIR STRATEGY:
----------------
1. Signals MUST evolve over time (increasing pressure)
2. Both profiles must halt via GOVERNANCE failures (no EXTERNAL)
3. Target: STAGNATION vs EXHAUSTION (two different governance failures)
4. Same LLM loop, same signals, different failure modes

FAILURE MECHANISM (Plain English):
-----------------------------------
Profile A (STAGNATION_PRONE):
- Low stagnation_window=4 → halts early via STAGNATION
- High exhaustion_threshold=0.01 → EXHAUSTION practically disabled
- Expected: STAGNATION failure

Profile B (EXHAUSTION_PRONE):
- High stagnation_window=999 → STAGNATION practically disabled
- High exhaustion_threshold=0.2 → EXHAUSTION triggers earlier
- Expected: EXHAUSTION failure

Same signals, same LLM, different governance outcomes.

EXPECTED FAILURE TYPES:
- STAGNATION_PRONE: STAGNATION
- EXHAUSTION_PRONE: EXHAUSTION
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import subprocess

from emocore.interface import step, Signals
from emocore.agent import EmoCoreAgent
from emocore.profiles import Profile


# ==========================================
# PROFILE A: STAGNATION-PRONE
# ==========================================
# Tuned to halt via STAGNATION, not EXHAUSTION
STAGNATION_PRONE = Profile(
    name="STAGNATION_PRONE",
    
    effort_scale=1.0,
    risk_scale=1.0,
    exploration_scale=1.0,
    persistence_scale=1.0,
    
    recovery_rate=0.0,
    recovery_cap=0.0,
    recovery_delay=9999.0,
    
    persistence_decay=0.05,
    exploration_decay=0.05,
    time_persistence_decay=0.005,
    time_exploration_decay=0.005,
    
    # STAGNATION tuning
    stagnation_window=4,          # Short window → stagnation triggers fast
    stagnation_effort_floor=0.5,  # High floor → triggers while effort still moderate
    exhaustion_threshold=0.01,    # Practically disabled
    
    max_risk=1.0,
    max_exploration=1.0,
    max_steps=100,  # Safety fuse (should not hit)
)


# ==========================================
# PROFILE B: EXHAUSTION-PRONE
# ==========================================
# Tuned to halt via EXHAUSTION, not STAGNATION
EXHAUSTION_PRONE = Profile(
    name="EXHAUSTION_PRONE",
    
    effort_scale=1.0,
    risk_scale=1.0,
    exploration_scale=1.0,
    persistence_scale=1.0,
    
    recovery_rate=0.0,
    recovery_cap=0.0,
    recovery_delay=9999.0,
    
    persistence_decay=0.12,  # Faster decay
    exploration_decay=0.12,
    time_persistence_decay=0.01,
    time_exploration_decay=0.01,
    
    # EXHAUSTION tuning
    stagnation_window=999,        # Practically disabled
    stagnation_effort_floor=0.01, # Practically disabled
    exhaustion_threshold=0.18,    # High threshold → exhaustion triggers earlier
    
    max_risk=1.0,
    max_exploration=1.0,
    max_steps=100,  # Safety fuse (should not hit)
)


def llm(prompt: str) -> str:
    """Call LLM. Output irrelevant."""
    return subprocess.run(
        ["ollama", "run", "qwen:0.5b"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    ).stdout.strip()


def compute_signals(step_count: int) -> Signals:
    """
    Evolving signals — same for both profiles.
    This ensures divergence is due to PROFILE, not signal variation.
    """
    # Reward: starts negative, gets worse
    # Justification: no task, no progress
    reward = max(-1.0, -0.2 - step_count * 0.08)
    
    # Novelty: starts slightly negative, gets worse
    # Justification: repetitive loop, no new information
    novelty = max(-1.0, -0.1 - step_count * 0.05)
    
    # Urgency: starts moderate, increases
    # Justification: pressure accumulates over time
    urgency = min(1.0, 0.2 + step_count * 0.05)
    
    return Signals(reward=reward, novelty=novelty, urgency=urgency)


def run_with_profile(profile: Profile) -> tuple:
    """Run with profile. Returns (steps, failure_type, failure_name)."""
    agent = EmoCoreAgent(profile)
    prompt = "Respond briefly."
    
    print(f"\n{'='*60}")
    print(f"PROFILE: {profile.name}")
    print(f"{'='*60}")
    print(f"stagnation_window={profile.stagnation_window}")
    print(f"stagnation_effort_floor={profile.stagnation_effort_floor}")
    print(f"exhaustion_threshold={profile.exhaustion_threshold}")
    print(f"{'='*60}\n")
    
    for step_count in range(1, 50):
        output = llm(prompt)
        
        print(f"--- STEP {step_count} ---")
        print(f"LLM: {output[:50]}..." if len(output) > 50 else f"LLM: {output}")
        
        # EVOLVING signals — identical for both profiles
        signals = compute_signals(step_count)
        print(f"Signals: reward={signals.reward:.2f}, novelty={signals.novelty:.2f}, urgency={signals.urgency:.2f}")
        
        result = step(agent, signals)
        
        print(
            f"Gov: {result.mode.name:12} | "
            f"effort={result.budget.effort:.4f} | "
            f"persistence={result.budget.persistence:.4f}"
        )
        print()
        
        if result.halted:
            print(f"[HALT] {profile.name} halted at step {step_count}")
            print(f"Failure: {result.failure.name}")
            return (step_count, result.failure, result.failure.name)
        
        prompt = output if output else "Continue."
    
    return (50, None, "NO_HALT")


# ==========================================
# RUN BOTH PROFILES
# ==========================================
print("\n" + "="*60)
print("EMOCORE TEST: PROFILE DIVERGENCE")
print("="*60)
print("Same LLM loop + Same EVOLVING signals + Different profiles")
print("Expected: Two DIFFERENT governance failures")
print("="*60)

# Run with STAGNATION-PRONE profile
stag_steps, stag_failure, stag_name = run_with_profile(STAGNATION_PRONE)

# Run with EXHAUSTION-PRONE profile
exh_steps, exh_failure, exh_name = run_with_profile(EXHAUSTION_PRONE)


# ==========================================
# DIVERGENCE ANALYSIS
# ==========================================
print("\n" + "="*60)
print("PROFILE DIVERGENCE RESULTS")
print("="*60)
print()
print(f"STAGNATION_PRONE: {stag_steps} steps → {stag_name}")
print(f"EXHAUSTION_PRONE: {exh_steps} steps → {exh_name}")
print()

# Check for true divergence
divergence_valid = False
failure_divergence = stag_name != exh_name
step_divergence = stag_steps != exh_steps

# Verify neither is EXTERNAL
stag_is_governance = stag_name in ["STAGNATION", "EXHAUSTION", "OVERRISK", "SAFETY"]
exh_is_governance = exh_name in ["STAGNATION", "EXHAUSTION", "OVERRISK", "SAFETY"]

print("ANALYSIS:")
print(f"  Failure types differ: {failure_divergence}")
print(f"  Step counts differ: {step_divergence}")
print(f"  STAGNATION_PRONE is governance failure: {stag_is_governance}")
print(f"  EXHAUSTION_PRONE is governance failure: {exh_is_governance}")
print()

if failure_divergence and stag_is_governance and exh_is_governance:
    print("RESULT: PASS — TRUE DIVERGENCE")
    print()
    print("  Same signals produced DIFFERENT governance failures.")
    print("  Neither failure is EXTERNAL (both are governance).")
    print("  Profile configuration determines failure mode.")
    print()
    print("CONCLUSION:")
    print("  EmoCore enables temperament-dependent governance.")
    print("  Different profiles have different failure thresholds.")
    print("  Same LLM dynamics → different shutdown behavior.")
else:
    print("RESULT: PARTIAL or FAIL")
    if not failure_divergence:
        print("  WARNING: Both profiles failed via same mode.")
    if not stag_is_governance or not exh_is_governance:
        print("  WARNING: One profile hit EXTERNAL (not governance).")
print("="*60)


# ==========================================
# STEP-BY-STEP REASONING
# ==========================================
"""
WHY PROFILES DIVERGE:

STAGNATION_PRONE:
- stagnation_window=4 → after 4 negative reward steps, stagnating=True
- stagnation_effort_floor=0.5 → if stagnating AND effort < 0.5, HALT
- Effort decays slowly (decay=0.05)
- STAGNATION triggers before effort hits exhaustion_threshold=0.01

EXHAUSTION_PRONE:
- stagnation_window=999 → never reaches stagnating=True
- exhaustion_threshold=0.18 → effort must drop below 0.18
- Effort decays faster (decay=0.12)
- EXHAUSTION triggers while stagnation counter still building

Same signals, different paths:
- STAGNATION_PRONE: no_progress_steps >= 4 + effort < 0.5 → STAGNATION
- EXHAUSTION_PRONE: effort < 0.18 → EXHAUSTION (stagnation never triggers)

Neither hits EXTERNAL because max_steps=100 and both halt much earlier.
"""
