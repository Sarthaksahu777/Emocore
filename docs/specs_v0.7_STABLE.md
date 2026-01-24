# EmoCore v0.7 — Stable Release Specification

This document defines the technical requirements and behavioral guarantees for the EmoCore v0.7 runtime governance layer. 

## 1. Scope and Objective
EmoCore v0.7 establishes a stable foundation for **bounded agency**. It regulates agent behavioral intensity independent of task-specific logic. 

**Exclusions**: This version does not include learning, online optimization, or dynamic policy adjustment.

## 2. Core Guarantees (Hard Invariants)

The following invariants are enforced by the v0.7 runtime:

- **Bounded Budgets**: All behavioral budgets are strictly constrained.
  - $\text{effort, risk, exploration, persistence} \in [0, 1]$
- **Terminal Failure**: Any governance-triggered failure results in a transition to `Mode.HALTED`.
- **Session Stickiness**: Once `HALTED`, the system remains in that state for the remainder of the session; budgets are permanently zeroed.
- **Controlled Recovery**: Capacity restoration (RECOVERING) is only permitted pre-failure and is subject to:
  - **Risk Safety**: Risk budgets must not increase during a recovery phase.
  - **Monotonicity**: Recovery cannot exceed the last stable budget level.
- **Inertial Stability**: Budget updates are subject to temporal smoothing to prevent high-frequency oscillations.

## 3. Canonical Runtime Flow

Signals are processed in a synchronous, one-way pipeline:

```mermaid
graph TD
    S[External Signals] --> A[Appraisal Layer]
    A --> P[Pressure State (Unbounded)]
    P --> G[Governance Engine]
    G --> B[Behavior Budget (Bounded)]
    B --> M[Mode & Failure Logic]
    M --> H{HALT or CONTINUE}
```

## 4. Failure Taxonomy
Failure types are ordered and mutually exclusive. The first condition met triggers a terminal halt:

| Type | Description |
| :--- | :--- |
| **SAFETY** | Immediate halt triggered by external safety constraints. |
| **OVERRISK** | Cumulative risk pressure exceeds the profile threshold. |
| **EXHAUSTION** | Sustained high load without sufficient recovery. |
| **STAGNATION** | Persistent lack of progress (low novelty/reward). |
| **EXTERNAL** | Session-level termination (e.g., max_steps). |

## 5. Version Boundary
EmoCore v0.7 is considered functionally complete when:
1. All core invariants are verified through property-based testing.
2. The `HALTED` state is confirmed as a terminal absorber.
3. Behavior profiles demonstrate expected divergence in benchmark tests.
4. No additional mechanics are introduced that violate v0.7 stability.

---
*Last Updated: Dec 15, 2025*
