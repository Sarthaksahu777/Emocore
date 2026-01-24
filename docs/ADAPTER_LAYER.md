# EmoCore — Evidence Adapter Architecture

> **Philosophy:** EmoCore does not understand the world. It governs based on declared evidence.

---

## 1. The Core Resolution

**EmoCore does NOT perception or semantics.**
It only consumes **declared behavioral evidence** produced by the system using it.

You do not build an "outdoor compiler" or a "world model".
You define a small, strict evidence interface and enforce pessimistic governance on top of it.

## 2. Correct Architecture

```
WORLD / ENVIRONMENT
        ↓
AGENT / SYSTEM (LLM, robot, controller)
        ↓
[ EVIDENCE ADAPTER ] ← User Responsibility
        ↓
EMOCORE (Governance Only)
```

**EmoCore never sees raw environment data.**
**EmoCore never does perception.**

EmoCore only sees **normalized evidence**:
- `env_state_delta` (Did the world change?)
- `agent_state_delta` (Did the agent's internal state change?)
- `result` (Did the action succeed or fail?)
- `elapsed_time` (How long did it take?)

If the provided evidence is garbage? **EmoCore halts.**
This is a **safe failure mode** by design.

---

## 3. What is an Evidence Adapter?

An Evidence Adapter is a **lossy, shallow, replaceable layer**.
It converts system-specific signals into EmoCore's `Observation` struct.

It corresponds to patterns already present in robust systems:
- **Robotics:** State estimator / Observer
- **OS:** Device drivers
- **ML:** Feature extraction
- **Games:** Physics engine state

You do not replace these systems. You sit below them, consuming their output.

### The Contract

```python
# The Adapter's only job is to produce this:
@dataclass(frozen=True)
class Observation:
    action: str              # "move_arm", "web_search"
    result: str              # "success", "failure"
    env_state_delta: float   # 0.0 to 1.0
    agent_state_delta: float # 0.0 to 1.0
```

---

## 4. Why This Works (Theory)

Because EmoCore is **pessimistic** and **frustration-dominant**.

| Input Quality | EmoCore Reaction | Result |
|---------------|------------------|--------|
| **Noisy Adapter** | Signal trust decays | Conservative Halt |
| **Wrong Adapter** | Frustration spikes | Safe Halt |
| **Incomplete Adapter** | Evidence doesn't accumulate | Early Halt |

**EmoCore treats bad inputs as a reason to stop, not a reason to guess.**

---

## 5. Implementation Scope

**What EmoCore Provides:**
1. The `Observation` struct (the Evidence ABI)
2. One default `RuleBasedEvidenceAdapter` (for quick start)
3. Reference examples (LLM, Tool, etc.)

**What EmoCore Does NOT Provide:**
- Perception
- Computer Vision
- NLP / Text Parsing
- World Modeling

---

## Summary

> **EmoCore ingests declared behavioral evidence, not raw observations.**
> If evidence is incomplete or incorrect, EmoCore degrades conservatively by halting earlier.

This prevents scope explosion and ensures safety is preserved even with imperfect adapters.