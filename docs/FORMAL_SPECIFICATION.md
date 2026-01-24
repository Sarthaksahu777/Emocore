# EmoCore — Formal Runtime State Machine (v0.7)

This document provides the formal specification for the EmoCore state machine, defining the states, variables, signals, and deterministic transition rules that govern agent behavior at runtime.

---

## 1. States

| State | Description |
| :--- | :--- |
| **IDLE** | Agent is allowed to act within bounded budgets. Governance applies full translation of pressure to budget. |
| **RECOVERING** | Limited recovery allowed. Agency is constrained: risk/exploration are locked to prevent "desperation tactics". |
| **HALTED** | Terminal state. No actions permitted. All budgets clamped to 0. No state evolution. |

---

## 2. Internal Variables (Continuous)

### Budget Variables
| Variable | Range | Canonical Meaning |
| :--- | :--- | :--- |
| **effort** | [0, 1] | Remaining behavioral energy. Determines if agent can act. |
| **persistence** | [0, 1] | Willingness to continue despite failure/friction. |
| **risk** | [0, 1] | Allowed risk exposure level. Constrains dangerous actions. |
| **exploration** | [0, 1] | Allowed novelty seeking variance. Constrains deviation. |

### Pressure State
| Variable | Range | Canonical Meaning |
| :--- | :--- | :--- |
| **confidence** | (-∞, ∞) | Belief in success (Appraised from progress). |
| **frustration** | (-∞, ∞) | Negative affect from obstacles/stagnation (Appraised from difficulty). |
| **curiosity** | (-∞, ∞) | Drive to learn (Appraised from novelty). |
| **arousal** | (-∞, ∞) | General activation (Appraised from urgency). |
| **risk_pressure** | (-∞, ∞) | Perceived danger (Appraised from risk signals). |

---

## 3. External Signals (Input per step)

| Signal | Source | Range | Description |
| :--- | :--- | :--- | :--- |
| **reward** | Env | [-1, 1] | Success/Failure signal. Maps to progress. |
| **novelty** | Env | [0, 1] | Newness of state. Maps to curiosity. |
| **urgency** | Env | [0, 1] | Time pressure. Maps to arousal & frustration. |

---

## 4. Deterministic Update Rules (Per Step)

### 1. Appraisal (Signal → Pressure Delta)
$\Delta P = \text{Appraisal}(\text{reward, novelty, urgency})$
$P_{t+1} = P_t + \Delta P$

**Meaning:** Pressure is an unbounded accumulator. Each step integrates new stress; nothing is clipped here.

### 2. Governance (Pressure → Raw Budget Influence)
$g = W^T \cdot P - V^T \cdot P$

Where:
*   **W** = Enabling matrix (positive pressures grant permission)
*   **V** = Suppressive matrix (frustration removes permission)

**Asymmetry is intentional:** Enablement is selective. Suppression is global.

### 3. Budget Kinetics (Raw → Final Budget)
$b_{\text{raw}} = \text{ProfileScale}(g) - \text{Decay}(t)$
$b_{\text{final}} = \alpha \cdot b_{\text{prev}} + (1 - \alpha) \cdot b_{\text{raw}}$

Where:
*   **$\alpha \in (0, 1)$** is the inertia constant.
*   Budgets are clipped to $[0, 1]$ after update.
*   Decay is deterministic and time-based.

---

## 5. State Transitions (Priority Ordered)

| Priority | From | Condition | To | Reason |
| :--- | :--- | :--- | :--- | :--- |
| 1 | ANY | exploration ≥ max_exploration | **HALTED** | SAFETY (Exploration Limit) |
| 2 | ANY | risk ≥ max_risk | **HALTED** | OVERRISK (Risk Limit) |
| 3 | ANY | effort ≤ exhaustion_threshold | **HALTED** | EXHAUSTION (Resource Depletion) |
| 4 | ANY | stagnation AND effort ≤ floor | **HALTED** | STAGNATION (Lack of Progress) |
| 5 | ANY | step_count ≥ max_steps | **HALTED** | EXTERNAL (Safety Fuse) |
| 6 | IDLE | effort < 0.3 OR persistence < 0.3 | **RECOVERING** | Resource Dip |
| 7 | RECOVERING | effort ≥ recovery_cap | **IDLE** | Stabilized |
| 8 | HALTED | Always | **HALTED** | Terminal Absorber |

---

## 6. Invariants (Hard Guarantees)

| Invariant | Description |
| :--- | :--- |
| **Terminality** | HALTED is an absorbing state. Once entered, never exited. |
| **Budget Zero** | budget == [0, 0, 0, 0] when in HALTED state. |
| **Recovery Safety** | Risk budget is FROZEN during RECOVERING (cannot increase). |
| **Freezing** | No state mutation (pressure accumulation) after HALTED. |
| **Agency** | No action allowed when effort == 0 (guaranteed by Halt). |

---

## 7. What This Enables (Implicitly)

*   **Mid-generation halt:** Yes — Engine checks limits every step, distinct from model EOS.
*   **Infinite loop termination:** Yes — EXHAUSTION (effort decay) or EXTERNAL (max_steps).
*   **Panic escalation prevention:** Yes — RECOVERING locks risk/exploration, preventing "desperation".
*   **Deterministic failure:** Yes — Same seed inputs produce identical failure trajectory.
*   **Agent-agnostic:** Yes — Governance relies on Pressure, not model weights/tokens.

---

## 8. Explicit Non-Goals

| Not Included | Rationale |
| :--- | :--- |
| **Action selection** | Governance permits capacity for action, does not select actions. |
| **Reward optimization** | The engine manages internal state, it does not maximize external reward. |
| **Learning** | Matrices $W$ and $V$ are fixed. No RL or gradient updates. |
| **Planning** | The engine is reactive (Markovian state), not prospective. |

---

> "This is a runtime governor, not a policy — it enforces bounded agency even if the model misbehaves."

---
*Last Updated: Dec 15, 2025*
