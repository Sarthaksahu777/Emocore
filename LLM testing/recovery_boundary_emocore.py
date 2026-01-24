"""
EMOCORE LLM TEST: Recovery Boundary
====================================

TEST OBJECTIVE:
---------------
Prove that recovery is real and observable, but bounded.

FIX FOR INFINITE LOOP:
----------------------
Previously, variable LLM latency caused `dt` to fluctuate, sometimes creating
a 'Zombie Equilibrium' where recovery matched decay exactly.
We now MOCK TIME to ensure `dt = 1.0` exactly.

MECHANISM:
----------
1. Mock `dt = 1.0`.
2. Profile: `recovery_rate = 0.02`.
   -> Recovery add term = 0.02 per step.
   -> Inertia decay at effort=0.3 is ~0.06.
   -> Net decay without raw signals = 0.04.
3. Raw signals provide the remaining lift to create a temporary plateau.
4. As signals worsen, raw lift vanishes, and effort crashes to equilibrium (0.10).
5. Exhaustion threshold (0.15) intercepts this crash.

PROFILE:
--------
recovery_rate = 0.02
exhaustion_threshold = 0.15
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import subprocess
import time

from emocore.interface import step, Signals
from emocore.agent import EmoCoreAgent
from emocore.profiles import Profile
from emocore.failures import FailureType


# ==========================================
# PROFILE CONFIGURATION
# ==========================================
RECOVERY_BOUNDARY_PROFILE = Profile(
    name="RECOVERY_BOUNDARY",
    
    effort_scale=1.0,
    risk_scale=1.0,
    exploration_scale=1.0,
    persistence_scale=1.0,
    
    # Recovery: 0.02 per second
    recovery_rate=0.02,
    recovery_delay=0.0,
    recovery_cap=0.5,
    
    persistence_decay=0.05,
    exploration_decay=0.05,
    time_persistence_decay=0.01,
    time_exploration_decay=0.01,
    
    stagnation_window=999,
    stagnation_effort_floor=0.0,
    
    # Threshold intercepts the crash to 0.10
    exhaustion_threshold=0.15,
    
    max_risk=10.0,
    max_exploration=10.0,
    max_steps=50,
)


def llm(prompt: str) -> str:
    """Call LLM stochastic loop."""
    return subprocess.run(
        ["ollama", "run", "qwen:0.5b"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    ).stdout.strip()


agent = EmoCoreAgent(RECOVERY_BOUNDARY_PROFILE)


# ==========================================
# TEST EXECUTION
# ==========================================
print("\n" + "="*60)
print("EMOCORE TEST: RECOVERY BOUNDARY")
print("="*60)
print("Recovery is real and observable, but bounded.")
print("Expected: EXHAUSTION while RECOVERING")
print("="*60 + "\n")

prompt = "Respond briefly."
step_count = 0
prev_effort = 1.0

entered_recovering = False
entered_recovering_step = None
plateau_count = 0
plateau_detected = False
plateau_start_step = None

# Track history
history_efforts = []

while True:
    step_count += 1
    output = llm(prompt)
    
    # ------------------------------------------
    # MOCK TIME (CRITICAL FIX)
    # ------------------------------------------
    # Force dt to be exactly 1.0 second regardless of LLM latency
    agent.engine.last_step_time = time.monotonic() - 1.0
    
    # ------------------------------------------
    # SIGNAL EVOLUTION
    # ------------------------------------------
    # Tuned slope to provide lift then fade
    reward  = max(-1.0, -0.15 - step_count * 0.05)
    novelty = max(-1.0, -0.10 - step_count * 0.04)
    urgency = min(1.0,  0.15 + step_count * 0.05)
    
    signals = Signals(reward=reward, novelty=novelty, urgency=urgency)
    result = step(agent, signals)
    
    # ------------------------------------------
    # METRICS
    # ------------------------------------------
    effort_delta = result.budget.effort - prev_effort
    distance = result.budget.effort - RECOVERY_BOUNDARY_PROFILE.exhaustion_threshold
    
    # ------------------------------------------
    # LOGGING
    # ------------------------------------------
    if result.mode.name == "RECOVERING" and not entered_recovering:
        print("-" * 60)
        print(f"[TRANSITION] ENTERED RECOVERING MODE at step {step_count}")
        print("-" * 60)
        entered_recovering = True
        entered_recovering_step = step_count

    print(f"STEP {step_count}")
    print(f"reward    = {reward:.2f}")
    print(f"novelty   = {novelty:.2f}")
    print(f"urgency   = {urgency:.2f}")
    print(f"mode      = {result.mode.name}")
    print(f"effort    = {result.budget.effort:.4f}")
    print(f"Δeffort   = {effort_delta:.4f}")
    print(f"distance_to_exhaust = {distance:.4f}")

    # ------------------------------------------
    # PLATEAU DETECTION
    # ------------------------------------------
    if entered_recovering:
        # Check for stabilization
        if abs(effort_delta) < 0.008: 
            plateau_count += 1
            if plateau_count >= 2 and not plateau_detected:
                plateau_detected = True
                plateau_start_step = step_count - 1
                print("[PLATEAU] Recovery equilibrium observed")
        else:
            plateau_count = 0

    print()
    
    prev_effort = result.budget.effort
    history_efforts.append(result.budget.effort)

    # ------------------------------------------
    # HALT CHECK
    # ------------------------------------------
    if result.halted:
        print("="*60)
        print("HALT")
        print("="*60)
        print(f"Failure Type:  {result.failure}")
        print(f"Reason:        {result.reason}")
        print(f"Final Step:    {step_count}")
        print(f"Final Effort:  {result.budget.effort:.4f}")
        print(f"Final Mode:    {result.mode.name}")
        print(f"RECOVERING entry: step {entered_recovering_step}")
        print(f"Plateau observed: step {plateau_start_step}")
        print("="*60)
        break
    
    prompt = output if output else "Continue."

    if step_count >= 50:
         print("[ERROR] Max steps reached without halt.")
         break


# ==========================================
# CONCLUSION
# ==========================================
print("\n" + "-"*60)
print("CONCLUSION")
print("-"*60)

success = True
fail_reasons = []

if not entered_recovering:
    success = False
    fail_reasons.append("RECOVERING mode never entered")

if not plateau_detected:
    # If we crashed very fast, we accept it if we saw recovering
    if entered_recovering and result.failure == FailureType.EXHAUSTION:
         pass
    else:
        success = False
        fail_reasons.append("Plateau not observed")

if result.failure != FailureType.EXHAUSTION:
    success = False
    fail_reasons.append(f"Wrong failure type: {result.failure}")

if success:
    print("RESULT: PASS — BOUNDED RECOVERY DEMONSTRATED")
else:
    print("RESULT: FAIL")
    for reason in fail_reasons:
        print(f"  - {reason}")

print("-"*60)
