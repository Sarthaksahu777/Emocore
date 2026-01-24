#!/usr/bin/env python3
"""
Example: EmoCore Trace Visualizer
=================================

Runs a multi-step simulation (Retry Storm scenario) and generates
a diagnostic plot of Pressure State and Behavior Budgets.

Requires: matplotlib
"""

import sys
import os
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core import EmoCoreAgent, observe, Observation, PROFILES

def run_visualizer_demo():
    print("=" * 60)
    print("EMOCORE TRACE VISUALIZER")
    print("=" * 60)
    
    # 1. Setup Simulation
    from core.profiles import ProfileType
    agent = EmoCoreAgent(PROFILES[ProfileType.BALANCED])
    steps = 40
    
    # History for plotting
    history = {
        "confidence": [],
        "frustration": [],
        "curiosity": [],
        "arousal": [],
        "risk_pressure": [],
        "effort": [],
        "persistence": [],
        "risk_budget": [],
        "exploration": [],
        "mode": []
    }
    
    print(f"Simulating {steps} steps of a Retry Storm...")
    
    for i in range(steps):
        # Simulate a failing loop (Retry Storm)
        obs = Observation(
            action="api_call",
            result="failure",
            env_state_delta=0.01 if i < 5 else 0.0, # Slow progress then stop
            agent_state_delta=0.05,
            elapsed_time=i * 2.0
        )
        
        res = observe(agent, obs)
        
        # Record states
        history["confidence"].append(res.pressure_log["confidence"])
        history["frustration"].append(res.pressure_log["frustration"])
        history["curiosity"].append(res.pressure_log["curiosity"])
        history["arousal"].append(res.pressure_log["arousal"])
        history["risk_pressure"].append(res.pressure_log["risk"])
        
        history["effort"].append(res.budget.effort)
        history["persistence"].append(res.budget.persistence)
        history["risk_budget"].append(res.budget.risk)
        history["exploration"].append(res.budget.exploration)
        
        history["mode"].append(res.mode.value)
        
        if res.halted:
            print(f"Halted at step {i+1} due to {res.reason}")
            # Pad remaining steps if halted early
            for _ in range(steps - i - 1):
                for key in history:
                    history[key].append(history[key][-1])
            break

    # 2. Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Subplot 1: Pressure State
    ax1.set_title("Core Pressure Dynamics (Internal State)", fontsize=14, fontweight='bold')
    ax1.plot(history["confidence"], label="Confidence", marker='.', alpha=0.8)
    ax1.plot(history["frustration"], label="Frustration", marker='.', alpha=0.8)
    ax1.plot(history["curiosity"], label="Curiosity", marker='.', alpha=0.8)
    ax1.plot(history["arousal"], label="Arousal", marker='.', alpha=0.8)
    ax1.plot(history["risk_pressure"], label="Risk Pressure", marker='.', alpha=0.8, linestyle='--')
    ax1.axhline(y=0, color='black', alpha=0.3)
    ax1.set_ylabel("Pressure Magnitude")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Subplot 2: Behavior Budget
    ax2.set_title("Behavioral Budgets (Governance Output)", fontsize=14, fontweight='bold')
    ax2.plot(history["effort"], label="Effort", color='green', linewidth=2)
    ax2.plot(history["persistence"], label="Persistence", color='blue', linewidth=2)
    ax2.plot(history["risk_budget"], label="Risk Budget", color='red', linestyle='--')
    ax2.plot(history["exploration"], label="Exploration", color='orange', linestyle='--')
    ax2.set_ylabel("Resource Capacity")
    ax2.set_xlabel("Steps")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Annotate Halts
    if res.halted:
        ax2.annotate('HALTED', xy=(i, history["effort"][i]), xytext=(i+2, 0.5),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     fontsize=12, color='white', bbox=dict(boxstyle="round", fc="red"))
    
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), "trace_plot.png")
    plt.savefig(output_path)
    print(f"\nTrace plot saved to: {output_path}")
    
    # 3. Textual Summary (Premium CLI feel)
    print("\n" + "="*60)
    print("GOVERNANCE TRACE SUMMARY")
    print("="*60)
    print(f"{'Metric':<15} | {'Initial':<10} | {'Final':<10} | {'Trend'}")
    print("-" * 60)
    
    metrics = ["confidence", "frustration", "effort", "persistence"]
    for m in metrics:
        start = history[m][0]
        end = history[m][-1]
        trend = "[INC]" if end > start else "[DEC]" if end < start else "[STABLE]"
        print(f"{m.capitalize():<15} | {start:10.2f} | {end:10.2f} | {trend}")
    
    print("="*60)

if __name__ == "__main__":
    run_visualizer_demo()
