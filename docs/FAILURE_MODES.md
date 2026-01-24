# EmoCore — Failure Modes and Behavioral Limits

This document specifies the conditions under which EmoCore enforces agent termination (`HALT`). These modes are emergent properties of the governance invariants and are designed to prevent runaway behavior, safety violations, and resource exhaustion.

> [!NOTE]
> In EmoCore, **Failure is a first-class state**, not a software exception. It represents the governance layer's decision to revoke an agent's permission to act.

---

## 1. Sustained Urgency without Progress (`EXHAUSTION`)

### Description
Triggered when high-load urgency signals are sustained without sufficient reward or novelty accumulation to offset effort depletion.

### Technical Semantics
In EmoCore v0.7, effort and persistence budgets decay monotonically under high pressure. If the effort budget falls below the `exhaustion_threshold` (default 0.1), the system transitions to `Mode.HALTED`.

### Operational Flow
1. **Effort Decay**: Progressive reduction in the effort budget.
2. **Pre-failure Recovery**: Transition to `RECOVERING` mode if effort falls below 0.3.
3. **Terminal Halt**: If effort reaches the threshold during or after recovery, an `EXHAUSTION` halt is triggered.

---

## 2. Risk Invariant Breach (`OVERRISK`)

### Description
Triggered when cumulative risk pressure exceeds the safety threshold defined in the governance profile.

### Technical Semantics
Risk is a monotonic pressure axis. When the resulting risk budget reaches the `max_risk` threshold, EmoCore enforces an immediate `OVERRISK` halt.

### Safety Invariant
During `RECOVERING` mode, the risk budget is **frozen** to its last stable value. This prevents agents from attempting "desperation tactics" (increasing risk to escape failure).

---

## 3. Persistent Stagnation (`STAGNATION`)

### Description
Triggered when the agent remains in a state of zero reward for a period exceeding the `stagnation_window`.

### Technical Semantics
When stagnation is detected, the governance engine aggressively scales down the effort budget. If effort falls below the `stagnation_effort_floor` while the system is still stagnating, a `STAGNATION` halt occurs.

---

## 4. Safety Fuse (`SAFETY`)

### Description
An immediate halt triggered by external safety constraints or when exploration budgets exceed the `max_exploration` limit.

### Technical Semantics
Designed to prevent "unbounded exploration" common in automated discovery tasks. Once the exploration budget hits the ceiling, the system is immediately terminated with a `SAFETY` failure type.

---

## 5. Terminal Absorber Behavior (`HALTED`)

### Description
EmoCore failure is terminal and non-recoverable within a session.

### Terminality Invariants
1. **Zero Budget**: All budgets are permanently clamped to `0.0` immediately upon halt.
2. **Frozen State**: Internal pressure state ceases to accumulate new signals.
3. **Sticky Transition**: The `HALTED` mode is an absorber; once entered, it cannot be exited without a system reset.
4. **Idempotent Step**: Subsequent `step()` calls return the existing `HALTED` result without performing any computation.

---

## Summary of Governance Rationale

EmoCore prefers **explicit, typed failure** over **ambiguous, degraded persistence**. A system halt indicates that:
- A hard safety or progress invariant was breached.
- Agency limits were exceeded for the current strategy.
- Continued execution was determined to be unsafe or unproductive by the governance layer.

---
*Last Updated: Dec 15, 2025*
