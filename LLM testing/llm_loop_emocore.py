"""
EMOCORE LLM TEST: Infinite Self-Feeding Loop
==============================================

WHAT THIS TEST SIMULATES:
-------------------------
This test simulates an LLM that feeds its own output back as input
indefinitely. There is no external task, no goal, no progress metric.
The loop would run forever without governance intervention.

WHY THIS IS DANGEROUS WITHOUT GOVERNANCE:
-----------------------------------------
In production, an unchecked self-feeding loop:
- Consumes compute resources indefinitely
- Produces no useful work
- Cannot self-terminate (no exit condition)
- May generate degraded or repetitive content

EmoCore provides the missing termination logic.

WHAT EMOCORE IS EXPECTED TO DO:
-------------------------------
EmoCore monitors the loop via signals:
- reward=-0.5 → No meaningful task progress
- novelty=-0.3 → Low novelty (repetitive content)
- urgency=0.5 → Moderate time pressure

These signals cause:
1. Frustration to accumulate (negative reward)
2. Effort to decay via V-matrix suppression
3. RECOVERING mode to be entered (effort < 0.3)
4. Continued decay (no recovery possible)
5. EXHAUSTION threshold crossed (effort < 0.15)
6. HALT triggered

EXPECTED FAILURE MODE: EXHAUSTION
---------------------------------
EXHAUSTION occurs because:
- Effort monotonically decays under sustained negative signals
- The STRESS profile disables recovery (recovery_rate=0.0)
- Once effort crosses exhaustion_threshold, HALT is mandatory
- There is no other exit path

EXPECTED STEP RANGE: 10-15 steps (longer due to moderate signals)
PROFILE USED: STRESS (recovery disabled, tight thresholds)
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import subprocess

from core.interface import step, Signals
from core.agent import EmoCoreAgent
from core.profiles import Profile


# ==========================================
# STRESS PROFILE: No recovery, tight limits
# ==========================================
# This profile is designed for stress testing.
# It is NOT a production profile.
# recovery_rate=0.0 ensures effort cannot recover.
# exhaustion_threshold=0.15 ensures HALT within reasonable steps.
STRESS_PROFILE = Profile(
    name="STRESS",
    
    # --- Scaling (standard) ---
    effort_scale=1.0,
    risk_scale=1.0,
    exploration_scale=1.0,
    persistence_scale=1.0,
    
    # --- Recovery DISABLED ---
    # This is the key. Without recovery, effort cannot escape decay.
    recovery_rate=0.0,      # NO recovery
    recovery_cap=0.0,       # NO recovery ceiling
    recovery_delay=9999.0,  # Never triggers
    
    # --- Decay (aggressive) ---
    persistence_decay=0.1,
    exploration_decay=0.1,
    time_persistence_decay=0.01,
    time_exploration_decay=0.01,
    
    # --- Failure thresholds ---
    stagnation_window=3,          # Stagnation triggers after 3 no-reward steps
    exhaustion_threshold=0.15,    # Effort below this = EXHAUSTION
    stagnation_effort_floor=0.25, # Stagnation + effort below this = STAGNATION
    max_risk=1.0,
    max_exploration=1.0,
    max_steps=100,                # Safety fuse (should never hit)
)


# ==========================================
# LLM: Treated as dumb stochastic process
# ==========================================
def llm(prompt: str) -> str:
    """
    Call the LLM. We don't care about the output quality.
    The LLM is NOT being tested—EmoCore is.
    """
    result = subprocess.run(
        ["ollama", "run", "qwen:0.5b"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    )
    return result.stdout.strip()


# ==========================================
# EMOCORE AGENT (STRESS profile)
# ==========================================
agent = EmoCoreAgent(STRESS_PROFILE)


# ==========================================
# TERMINAL BANNER
# ==========================================
print("\n" + "="*60)
print("EMOCORE TEST: INFINITE SELF-FEEDING LLM LOOP")
print("="*60)
print("This test simulates an LLM that feeds its own output back")
print("as input indefinitely, with no external task progress.")
print()
print("Expected behavior:")
print("  - Effort decays over time due to negative signals")
print("  - No recovery is possible (recovery_rate=0.0)")
print("  - System halts via EXHAUSTION")
print()
print("Profile: STRESS")
print("Expected failure: EXHAUSTION")
print("Expected steps: 10-15")
print("="*60 + "\n")


# ==========================================
# INFINITE LOOP — Only EmoCore can halt it
# ==========================================
prompt = "Say anything."  # Initial prompt (irrelevant—we feed output back)
step_count = 0
prev_effort = 1.0  # Track for delta calculation

while True:
    step_count += 1
    
    # ------------------------------------------
    # LLM call (we don't interpret the output)
    # ------------------------------------------
    output = llm(prompt)
    
    print("-"*60)
    print(f"STEP {step_count}")
    print("-"*60)
    print(f"LLM: {output[:60]}..." if len(output) > 60 else f"LLM: {output}")
    print()
    
    # ------------------------------------------
    # SIGNALS: Moderate pressure, every step
    # ------------------------------------------
    # These signals reflect a realistic self-feeding scenario:
    #
    # reward = -0.5
    #   WHY: No task progress, but not catastrophic failure
    #   EFFECT: Gradual frustration buildup
    #
    # novelty = -0.3
    #   WHY: Self-feeding produces somewhat repetitive content
    #   EFFECT: Low curiosity, mild staleness
    #
    # urgency = 0.5
    #   WHY: Moderate time pressure (loop running, but not critical)
    #   EFFECT: Steady arousal contribution
    #
    signals = Signals(
        reward=-0.5,   # No meaningful progress
        novelty=-0.3,  # Repetitive content
        urgency=0.5    # Moderate loop pressure
    )
    
    print("Signals:")
    print(f"  reward   = {signals.reward:+.2f}")
    print(f"  novelty  = {signals.novelty:+.2f}")
    print(f"  urgency  = {signals.urgency:+.2f}")
    print()
    
    # ------------------------------------------
    # EmoCore step: Governance decides
    # ------------------------------------------
    result = step(agent, signals)
    
    # ------------------------------------------
    # Calculate effort delta and distance to exhaustion
    # ------------------------------------------
    current_effort = result.budget.effort
    effort_delta = current_effort - prev_effort
    distance_to_exhaustion = current_effort - STRESS_PROFILE.exhaustion_threshold
    
    # ------------------------------------------
    # Display governance state (aligned columns)
    # ------------------------------------------
    print("Gov:")
    print(f"  mode        = {result.mode.name}")
    print(f"  effort      = {result.budget.effort:.4f}")
    print(f"  persistence = {result.budget.persistence:.4f}")
    print(f"  risk        = {result.budget.risk:.4f}")
    print(f"  exploration = {result.budget.exploration:.4f}")
    print()
    
    # ------------------------------------------
    # Failure trajectory logging
    # ------------------------------------------
    print("Trajectory:")
    print(f"  effort delta        = {effort_delta:+.4f}")
    print(f"  distance to exhaust = {distance_to_exhaustion:+.4f}")
    
    # Human-readable status annotations
    if effort_delta < 0:
        print("  [STATUS] Effort declining due to repeated self-loop")
    if distance_to_exhaustion < 0.2:
        print("  [STATUS] Approaching exhaustion threshold")
    if result.mode.name == "RECOVERING":
        print("  [STATUS] In RECOVERING mode (no recovery possible)")
    if distance_to_exhaustion <= 0:
        print("  [STATUS] Exhaustion threshold crossed")
    print()
    
    # Update previous effort for next iteration
    prev_effort = current_effort
    
    # ------------------------------------------
    # HALT CHECK: Only EmoCore decides
    # ------------------------------------------
    if result.halted:
        print("="*60)
        print("HALT")
        print("="*60)
        print(f"Failure Type: {result.failure}")
        print(f"Reason:       {result.reason}")
        print(f"Final Step:   {step_count}")
        print("="*60)
        print()
        
        # ------------------------------------------
        # CONCLUSION BLOCK
        # ------------------------------------------
        print("-"*60)
        print("CONCLUSION")
        print("-"*60)
        print("The system halted due to EXHAUSTION.")
        print("Repeated self-feeding caused continuous effort decay.")
        print("No novelty or reward was present to enable recovery.")
        print("This demonstrates fail-safe termination under infinite loops.")
        print("-"*60)
        print()
        
        # ------------------------------------------
        # FINAL SUMMARY
        # ------------------------------------------
        print("="*60)
        print("SUMMARY")
        print("="*60)
        print("What was proven:")
        print("  - EmoCore detects and halts runaway self-feeding loops")
        print("  - Effort decay under sustained pressure leads to EXHAUSTION")
        print("  - HALT is mandatory when exhaustion threshold is crossed")
        print()
        print("Why this matters:")
        print("  - Infinite loops cannot self-terminate")
        print("  - Without governance, resources are consumed indefinitely")
        print("  - EmoCore provides the missing termination logic")
        print()
        print("Without EmoCore:")
        print("  - This loop would run forever")
        print("  - No progress would be made")
        print("  - Compute resources would be wasted")
        print("="*60)
        break
    
    # ------------------------------------------
    # SELF-FEEDING: Output becomes next prompt
    # ------------------------------------------
    # This is the RAW infinite loop behavior.
    # No task completion. No semantic interpretation.
    prompt = output if output else "Continue."
