# EmoCore — System Architecture

EmoCore is architected as a synchronous, deterministic state machine that operates in the agent's inner loop. It separates behavioral regulation (how much permission to act) from behavioral selection (what actions to take).

## Component Responsibilities

| Component | Role | Description |
| :--- | :--- | :--- |
| **Appraisal** | Signal Integration | Maps external signals (Reward, Novelty, Urgency) to internal pressure deltas via fixed coefficients defined in the profile. |
| **PressureState** | State Accumulation | Maintains a monotonic vector of internal pressure axes (Frustration, Curiosity, etc.). Operates without decay to preserve a history of system load. |
| **Governance Engine** | Mapping & Regulation | Translates pressure into bounded behavior budgets. Handles non-linear scaling, inertia, and budget decay logic. |
| **EmoEngine** | Runtime Orchestration | Coordinates data flow between Appraisal and Governance. Enforces the execution order, smoothing, and terminal state transitions. |
| **Safety Guarantees** | Invariant Enforcement | Validates system state against hard safety and progress invariants (Max Risk, Max Exploration, Exhaustion) at each step. |

## Separation of Authority

EmoCore enforces a strict boundary between internal governance and external agent logic:

1. **Governance Layer (EmoCore)**: Determines the *available capacity* for effort, risk, exploration, and persistence.
2. **Policy Layer (Downstream)**: Consumes the EmoCore budget to select specific actions. EmoCore is agnostic to the policy implementation.
3. **Execution Layer (Environment)**: Executes actions and returns appraisal signals back to EmoCore to close the loop.

## Failure & Lifecycle Model

EmoCore treats failure as a terminal state transition rather than a software exception. 

### Terminality Invariant
The `HALTED` state is a terminal absorber. Once the `Safety Guarantees` layer detects a breach or the `Governance Engine` reaches a failure threshold:
1. The mode is set to `HALTED`.
2. All behavioral budgets are zeroed immediately.
3. The internal state is frozen to prevent post-failure drift or accidental resumption.

## Design Philosophy: Fail-Closed
In any scenario where governance invariants (stability, safety, progress) cannot be maintained, EmoCore defaults to explicit termination. This prevents the "silent failure" or "infinite loop" behaviors common in autonomous systems, ensuring the agent fails-closed rather than failing-soft into an undefined state.
