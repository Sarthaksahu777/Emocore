# EmoCore — Core Definition

EmoCore is a **runtime governance layer** designed to regulate autonomous agent agency by mapping accumulated internal pressure to bounded behavioral budgets. It enforces deterministic behavioral limits and explicit failure semantics, operating as a distinct primitive from decision-making logic.

## Core Decoupling
EmoCore operates independently of:
- **Agent Intelligence**: No reliance on reasoning, memory, or world modeling.
- **Policy**: No dependency on specific action-selection algorithms (e.g., LLMs, RL, Planners).
- **Environment Model**: No internal representation of external state.

> [!IMPORTANT]
> EmoCore governs **when** to act (permission, intensity, risk), not **what** to do (action selection).

## Key Properties
- **Model-Agnostic**: Compatible with any intelligence layer that consumes real-valued budgets.
- **Non-Learning**: Zero weight updates or gradient-based optimization; behavior is defined by static configuration profiles.
- **Fail-Closed**: Any violation of safety or progress invariants results in an immediate, terminal transition to the `HALTED` state.
- **Auditability**: All behavioral constraints are bounded, typed, and verifiable through synchronous state inspection.

## Canonical Role Mapping
| System Component | Responsibility |
| :--- | :--- |
| **Intelligence Layer** | Goal decomposition, action selection, and planning. |
| **EmoCore (Governance)** | Behavioral boundaries, effort regulation, and risk enforcement. |

## Operational Logic
1. **Pressure Integration**: Internal axes (Frustration, Curiosity, Arousal, Risk) accumulate monotonically from appraisal signals.
2. **Deterministic Governance**: A fixed mapping translates unbounded pressure state into a vector of bounded budgets.
3. **Behavioral Budgets**: Real-valued constraints $\in [0, 1]$ (Effort, Risk, Exploration, Persistence) that modulate agent execution.
4. **Pre-failure Recovery**: Controlled capacity restoration (Mode.RECOVERING) occurs only before a terminal threshold is reached.
5. **Terminal Failure**: Once a failure threshold is crossed (e.g., EXHAUSTION, OVERRISK), the system enters a non-recoverable `HALTED` mode.

## Specification Context
As a **first-class runtime governor**, EmoCore prevents runaway behaviors and ensures agents operate within defined technical safety and progress envelopes, making autonomous systems predictable and reliable.

---
*Last Updated: Jan 25, 2026*
