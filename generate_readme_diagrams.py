#!/usr/bin/env python3
"""
Generate diagrams for README visualization
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'primary': '#2E86AB',
    'success': '#06A77D',
    'warning': '#F77F00',
    'danger': '#D62828',
    'neutral': '#6C757D'
}

def create_architecture_diagram():
    """Create the EmoCore architecture flow diagram"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'EmoCore Architecture', 
            ha='center', fontsize=16, fontweight='bold')
    
    # Environment box
    env_box = FancyBboxPatch((3, 7.5), 4, 1, 
                             boxstyle="round,pad=0.1", 
                             edgecolor=colors['neutral'], 
                             facecolor='lightgray', linewidth=2)
    ax.add_patch(env_box)
    ax.text(5, 8, 'Environment\n(Task, Rewards, Urgency)', 
            ha='center', va='center', fontsize=10)
    
    # Agent/LLM box
    agent_box = FancyBboxPatch((3, 5.5), 4, 1.2, 
                               boxstyle="round,pad=0.1", 
                               edgecolor=colors['primary'], 
                               facecolor='lightblue', linewidth=2)
    ax.add_patch(agent_box)
    ax.text(5, 6.1, 'Agent / LLM / Planner\n(Chooses Actions)', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # EmoCore box (highlighted)
    emo_box = FancyBboxPatch((2.5, 3.5), 5, 1.2, 
                             boxstyle="round,pad=0.1", 
                             edgecolor=colors['danger'], 
                             facecolor='#FFE5E5', linewidth=3)
    ax.add_patch(emo_box)
    ax.text(5, 4.3, '⚡ EmoCore Runtime Governor', 
            ha='center', va='center', fontsize=11, fontweight='bold', 
            color=colors['danger'])
    ax.text(5, 3.8, 'Tracks Stress • Enforces Budgets • Decides HALT/GO', 
            ha='center', va='center', fontsize=8, style='italic')
    
    # Execution box
    exec_box = FancyBboxPatch((3, 1.8), 4, 1, 
                              boxstyle="round,pad=0.1", 
                              edgecolor=colors['success'], 
                              facecolor='lightgreen', linewidth=2)
    ax.add_patch(exec_box)
    ax.text(5, 2.3, 'Action Execution\n(Tools, APIs, Motors)', 
            ha='center', va='center', fontsize=10)
    
    # Arrows
    arrow1 = FancyArrowPatch((5, 7.5), (5, 6.7), 
                            arrowstyle='->', lw=2, color='black')
    ax.add_patch(arrow1)
    
    arrow2 = FancyArrowPatch((5, 5.5), (5, 4.7), 
                            arrowstyle='->', lw=2, color='black')
    ax.add_patch(arrow2)
    
    arrow3 = FancyArrowPatch((5, 3.5), (5, 2.8), 
                            arrowstyle='->', lw=3, color=colors['success'])
    ax.add_patch(arrow3)
    ax.text(5.5, 3.1, 'GO', fontsize=9, fontweight='bold', color=colors['success'])
    
    # HALT indicator
    ax.plot([7.5, 7.5], [3.5, 2.8], 'r--', lw=2)
    ax.text(8.2, 3.1, 'HALT', fontsize=9, fontweight='bold', color=colors['danger'])
    ax.scatter(7.5, 3.1, s=100, c=colors['danger'], marker='X', zorder=5)
    
    # Key insight box
    insight_box = FancyBboxPatch((0.5, 0.2), 9, 1, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor=colors['warning'], 
                                 facecolor='#FFF3CD', linewidth=2)
    ax.add_patch(insight_box)
    ax.text(5, 0.7, '💡 Execution is no longer "run unless killed"', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(5, 0.4, 'Execution becomes permissioned — every action must be approved by EmoCore', 
            ha='center', va='center', fontsize=8, style='italic')
    
    plt.tight_layout()
    plt.savefig('docs/architecture_diagram.png', dpi=300, bbox_inches='tight', 
                facecolor='white')
    print("[OK] Created architecture_diagram.png")
    plt.close()

def create_pressure_budget_diagram():
    """Create pressure vs budget dynamics visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    steps = np.arange(0, 20)
    
    # Subplot 1: Pressure (Unbounded)
    frustration = steps * 0.3 + np.random.randn(20) * 0.1
    confidence = 1 - steps * 0.1 - np.random.randn(20) * 0.05
    
    ax1.plot(steps, frustration, 'o-', color=colors['danger'], 
             linewidth=2, markersize=6, label='Frustration')
    ax1.plot(steps, confidence, 's-', color=colors['primary'], 
             linewidth=2, markersize=6, label='Confidence')
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    ax1.set_xlabel('Steps', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Pressure Magnitude', fontsize=12, fontweight='bold')
    ax1.set_title('Pressure (Unbounded)\nAccumulates Without Limit', 
                  fontsize=13, fontweight='bold', color=colors['danger'])
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-1, 7)
    
    # Add annotation
    ax1.annotate('Stress increases\nforever ↑', 
                xy=(18, 5.5), fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['danger'], alpha=0.2))
    
    # Subplot 2: Budgets (Bounded)
    effort = np.maximum(0, 1 - steps * 0.08)
    persistence = np.maximum(0, 1 - steps * 0.06)
    
    ax2.plot(steps, effort, 'o-', color=colors['success'], 
             linewidth=2, markersize=6, label='Effort')
    ax2.plot(steps, persistence, 's-', color=colors['warning'], 
             linewidth=2, markersize=6, label='Persistence')
    ax2.axhline(y=0, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax2.axhline(y=1, color='black', linestyle='--', alpha=0.3)
    ax2.fill_between(steps, 0, 1, alpha=0.1, color='green', label='Valid Range')
    ax2.set_xlabel('Steps', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Budget Capacity', fontsize=12, fontweight='bold')
    ax2.set_title('Budgets (Bounded in [0,1])\nPermission Collapses', 
                  fontsize=13, fontweight='bold', color=colors['success'])
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.2, 1.3)
    
    # Add HALT marker
    halt_step = 13
    ax2.axvline(x=halt_step, color='red', linestyle='--', linewidth=2)
    ax2.text(halt_step + 0.5, 0.5, 'TERMINAL\nHALT', 
            fontsize=11, fontweight='bold', color='red',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('docs/pressure_budget_dynamics.png', dpi=300, bbox_inches='tight', 
                facecolor='white')
    print("[OK] Created pressure_budget_dynamics.png")
    plt.close()

def create_failure_progression_diagram():
    """Create failure mode progression timeline"""
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Title
    ax.text(7, 3.5, 'Failure Mode Progression', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Timeline
    ax.plot([1, 13], [2, 2], 'k-', linewidth=2)
    
    # States
    states = [
        (2, 'IDLE', colors['success'], 'Normal\nOperation'),
        (7, 'RECOVERING', colors['warning'], 'Budget\nRegeneration'),
        (12, 'HALTED', colors['danger'], 'Terminal\nFailure')
    ]
    
    for x, label, color, desc in states:
        circle = plt.Circle((x, 2), 0.3, color=color, zorder=3)
        ax.add_patch(circle)
        ax.text(x, 2, label[0], ha='center', va='center', 
                fontsize=12, fontweight='bold', color='white', zorder=4)
        ax.text(x, 1.2, label, ha='center', va='top', 
                fontsize=10, fontweight='bold', color=color)
        ax.text(x, 0.8, desc, ha='center', va='top', 
                fontsize=8, style='italic')
    
    # Arrows
    ax.annotate('', xy=(6.5, 2), xytext=(2.5, 2),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    ax.text(4.5, 2.5, 'Pressure\nincreases', ha='center', fontsize=8)
    
    ax.annotate('', xy=(11.5, 2), xytext=(7.5, 2),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    ax.text(9.5, 2.5, 'Exhaustion\nthreshold', ha='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('docs/failure_progression.png', dpi=300, bbox_inches='tight', 
                facecolor='white')
    print("[OK] Created failure_progression.png")
    plt.close()

if __name__ == "__main__":
    print("Generating README diagrams...")
    create_architecture_diagram()
    create_pressure_budget_diagram()
    create_failure_progression_diagram()
    print("\n[OK] All diagrams created in docs/")
