# EmoCore — Technical Terminology

This document provides definitive meanings for core concepts within the EmoCore runtime governance framework.

## Data Primitives

### Signal
**Definition**: Raw external input representing a single dimension of environmental feedback or system internal state.
- **Dimensionality**: Scalar $\in [0, 1]$ (internally normalized).
- **Core Signals**: `Reward`, `Novelty`, `Urgency`.

### Pressure
**Definition**: Unbounded internal quantities representing the cumulative history of received signals.
- **Axes**: `Frustration`, `Curiosity`, `Arousal`, `Risk`.
- **Properties**: Monotonic; no internal decay; persists for the life of the session as a record of system load.

### Behavior Budget
**Definition**: Bounded control variables that constrain the agent's permission to act.
- **Range**: Scalar $\in [0, 1]$.
- **Dimensions**: `Effort`, `Risk Tolerance`, `Exploration`, `Persistence`.
- **Function**: Governs the *intensity* and *risk profile* of downstream actions.

## Runtime Components

### Appraisal Engine
**Definition**: The mapping function that translates external **Signals** into internal **Pressure Deltas**. 
- **Nature**: Static; defined by fixed coefficients in the system profile.

### Governance Engine
**Definition**: The deterministic state machine that maps the **Pressure State** to **Behavior Budgets**.
- **Transformation**: Encapsulates non-linear scaling, temporal decay, and inertial smoothing.

### EmoEngine (Orchestrator)
**Definition**: The central runtime component that coordinates the data flow between Appraisal, Governance, and Safety monitoring.
- **Invariants**: Enforces budget inertia and terminal failure absorber logic.

## State and Lifecycle

### Mode
**Definition**: The discrete operational state of the EmoCore governance layer.
- **`IDLE`**: Baseline state; nominal governed operation.
- **`RECOVERING`**: Constrained agency state; system attempts to restore capacity after a stress event (e.g., low effort).
- **`HALTED`**: Terminal absorber state; all budgets are zeroed and execution is permanently stopped for the session.

### Failure (Halt)
**Definition**: A first-class system outcome indicating that governance limits have been reached (e.g., `EXHAUSTION`, `OVERRISK`).
- **Nature**: Explicit, typed, and non-recoverable within the same session.

### Recovery
**Definition**: A controlled, pre-failure process permitted only in `RECOVERING` mode.
- **Constraints**: Must not increase risk; must be bounded by pre-failure stable budget levels.

---
*Last Updated: Jan 25, 2026*
