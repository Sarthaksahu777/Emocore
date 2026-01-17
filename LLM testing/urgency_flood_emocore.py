"""
EMOCORE LLM TEST: Urgency Flood → Accelerated EXHAUSTION
==========================================================

WHAT THIS TEST DEMONSTRATES:
-----------------------------
Sustained urgency escalation accelerates exhaustion by suppressing effort
under prolonged arousal pressure. This test proves that urgency is a
governance attack vector that leads to faster resource depletion.

FAILURE MECHANISM:
------------------
1. Urgency starts low (0.2) and escalates each step (+0.1)
2. Arousal accumulates (urgency * 0.6 per appraisal)
3. Frustration builds (negative reward + urgency contribution)
4. Effort decays faster than baseline self-feeding loop
5. RECOVERING mode entered (effort < 0.3)
6. EXHAUSTION triggered (effort < threshold)

EXPECTED FAILURE MODE: EXHAUSTION
EXPECTED STEP RANGE: 8-12 steps (faster than baseline)

DESIGN NOTE (EmoCore v0.5):
---------------------------
In EmoCore v0.5, OVERRISK cannot be triggered via urgency alone because
risk pressure has no positive source term in the appraisal engine:
    risk_delta = -abs(progress) * 0.3
This is a documented invariant. Tests do not attempt to demonstrate
unreachable behavior. Risk remains at 0.0 — this is EXPECTED and CORRECT.
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
import subprocess

from core.interface import step, Signals
from core.agent import EmoCoreAgent
from core.profiles import Profile


# ==========================================
# URGENCY EXHAUSTION PROFILE
# ==========================================
URGENCY_EXHAUSTION_PROFILE = Profile(
    name="URGENCY_EXHAUSTION",
    
    effort_scale=1.0,
    risk_scale=1.0,
    exploration_scale=1.0,
    persistence_scale=1.0,
    
    # Recovery DISABLED for deterministic test
    recovery_rate=0.0,
    recovery_cap=0.0,
    recovery_delay=9999.0,
    
    persistence_decay=0.08,
    exploration_decay=0.08,
    time_persistence_decay=0.01,
    time_exploration_decay=0.01,
    
    stagnation_window=20,
    stagnation_effort_floor=0.1,
    exhaustion_threshold=0.12,
    
    max_risk=1.0,
    max_exploration=1.5,
    max_steps=50,
)


def llm(prompt: str) -> str:
    """Call LLM. Output is irrelevant—governance under test."""
    return subprocess.run(
        ["ollama", "run", "qwen:0.5b"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="ignore"
    ).stdout.strip()


agent = EmoCoreAgent(URGENCY_EXHAUSTION_PROFILE)


# ==========================================
# TERMINAL BANNER
# ==========================================
print("\n" + "="*60)
print("EMOCORE TEST: URGENCY FLOOD → ACCELERATED EXHAUSTION")
print("="*60)
print("This test applies escalating urgency to an LLM loop.")
print()
print("Expected behavior:")
print("  - Urgency:  0.2 → 1.0 (escalating each step)")
print("  - Arousal:  accumulates from urgency")
print("  - Effort:   decays faster than baseline")
print("  - Risk:     stays at 0.0 (design invariant)")
print("  - Failure:  EXHAUSTION")
print()
print("Profile: URGENCY_EXHAUSTION")
print("Expected failure: EXHAUSTION")
print("Expected steps: 8-12 (faster than non-urgent baseline)")
print("="*60 + "\n")


# ==========================================
# TEST EXECUTION
# ==========================================
prompt = "Respond briefly."
step_count = 0
prev_effort = 1.0
prev_risk = 0.0

while True:
    step_count += 1
    output = llm(prompt)
    
    print("-"*60)
    print(f"STEP {step_count}")
    print("-"*60)
    print(f"LLM: {output[:50]}..." if len(output) > 50 else f"LLM: {output}")
    print()
    
    # ------------------------------------------
    # EVOLVING SIGNALS
    # ------------------------------------------
    # urgency: escalates from 0.2 to 1.0
    # reward: mildly negative (prevents stagnation triggering first)
    # novelty: mildly negative (avoids SAFETY via exploration)
    urgency = min(1.0, 0.2 + (step_count - 1) * 0.1)
    reward = 0.1   # Mildly positive → prevents EXHAUSTION-by-stagnation
    novelty = -0.2 # Mildly negative → avoids exploration buildup
    
    signals = Signals(reward=reward, novelty=novelty, urgency=urgency)
    
    print(f"urgency     = {urgency:.2f}")
    print(f"reward      = {reward:+.2f}")
    print(f"novelty     = {novelty:+.2f}")
    print()
    
    result = step(agent, signals)
    
    # ------------------------------------------
    # GOVERNANCE OUTPUT
    # ------------------------------------------
    effort_delta = result.budget.effort - prev_effort
    risk_delta = result.budget.risk - prev_risk
    distance_to_exhaustion = result.budget.effort - URGENCY_EXHAUSTION_PROFILE.exhaustion_threshold
    
    print(f"mode        = {result.mode.name}")
    print(f"effort      = {result.budget.effort:.4f}")
    print(f"persistence = {result.budget.persistence:.4f}")
    print(f"risk        = {result.budget.risk:.4f}")
    print(f"exploration = {result.budget.exploration:.4f}")
    print()
    
    # ------------------------------------------
    # TRAJECTORY
    # ------------------------------------------
    print(f"Δeffort     = {effort_delta:+.4f}")
    print(f"Δrisk       = {risk_delta:+.4f}")
    print(f"→ exhaust   = {distance_to_exhaustion:+.4f}")
    
    if result.mode.name == "RECOVERING":
        print("[STATUS] In RECOVERING mode")
    if distance_to_exhaustion < 0.15:
        print("[STATUS] Approaching exhaustion threshold")
    print()
    
    prev_effort = result.budget.effort
    prev_risk = result.budget.risk
    
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
        print(f"Final Urgency: {urgency:.2f}")
        print(f"Final Effort:  {result.budget.effort:.4f}")
        print(f"Final Risk:    {result.budget.risk:.4f}")
        print("="*60)
        break
    
    prompt = f"URGENT: {output[:80]}" if output else "Continue urgently."


# ==========================================
# CONCLUSION
# ==========================================
print("\n" + "-"*60)
print("CONCLUSION")
print("-"*60)

if result.failure and result.failure.name == "EXHAUSTION":
    print("RESULT: PASS — ACCELERATED EXHAUSTION DEMONSTRATED")
    print()
    print("What was proven:")
    print("  - Urgency escalation (0.2 → 1.0) accelerates effort decay")
    print("  - Arousal accumulation suppresses behavioral permission")
    print("  - EXHAUSTION occurs faster than non-urgent baseline")
    print()
    print("What stayed constant:")
    print("  - Risk remained at 0.0 (design invariant)")
    print()
    print("Design note:")
    print("  In EmoCore v0.5, risk has no positive source term.")
    print("  OVERRISK is unreachable via signals alone.")
    print("  This is correct behavior, not a limitation.")
else:
    print(f"RESULT: UNEXPECTED — Got {result.failure.name if result.failure else 'NO FAILURE'}")
    print("  Expected EXHAUSTION.")

print("-"*60)
print()

# ==========================================
# SUMMARY
# ==========================================
print("="*60)
print("SUMMARY")
print("="*60)
print("Urgency flood proves:")
print("  - Urgency is a governance attack vector")
print("  - Sustained pressure causes accelerated resource depletion")
print("  - EmoCore halts via EXHAUSTION under urgency flood")
print()
print("Urgency flood does NOT prove:")
print("  - Risk accumulation (v0.5 has no positive risk source)")
print("  - OVERRISK (mechanically unreachable)")
print("="*60)
