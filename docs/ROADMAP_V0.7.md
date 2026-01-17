# EmoCore v0.7 Roadmap: "Plug-and-Play Governance"

## 🎯 Primary Goal
> **EmoCore can be dropped into a real agent loop without hand-wiring every signal.**

The focus of v0.7 is **accessibility and integration**. We are moving from a "governance primitive" that requires manual signal injection to a "governance layer" that automatically infers signals from agent behavior.

---

## 🚫 Non-Negotiable Rules (The "EmoCore Guardrails")
*   ❌ **No weakening of halting guarantees**: Halting must remain deterministic and final.
*   ❌ **No learning**: The governance matrices ($W, V$) remain fixed.
*   ❌ **No policy influence**: We bound capacity for action; we do not select actions.

---

## 🏗️ 1. Signal Extraction Layer (Automated Heuristics)
*   **Reward Extraction**:
    *   [ ] Detect task success/failure via explicit flags.
    *   [ ] Detect retries (identical actions or repeated tool calls).
    *   *Output:* Normalized reward $\in [-1.0, 1.0]$.
*   **Novelty Extraction**:
    *   [ ] State change detection (hash/snapshot diffs).
    *   [ ] Tool usage divergence (new vs. repeated tools).
    *   *Output:* Normalized novelty $\in [0.0, 1.0]$.
*   **Urgency Extraction**:
    *   [ ] Wall-clock elapsed time integration.
    *   [ ] Token/Step budget depletion tracking.
    *   *Output:* Normalized urgency $\in [0.0, 1.0]$.
*   **Difficulty Inference**:
    *   [ ] Stagnation streak detection (no state change over $N$ steps).
    *   [ ] Tool error accumulation counter.

---

## 🔌 2. Integration Surface (The Adapters)
*   **LLM Loop Adapter**: A drop-in wrapper for standard LLM retry/generation loops that handles state and signals automatically.
*   **Tool-Calling Agent Adapter**: A wrapper that captures tool execution results, failures, and retries to map them directly to EmoCore signals.
*   **Examples Gallery (`/examples`)**:
    *   [ ] Deterministic loop halting (The "Infinite Loop" fix).
    *   [ ] Tool failure cascade → Safe Halt.
    *   [ ] Multi-step task trace with budget visualizations.

---

## 🔄 3. Lifecycle & Observability
*   **Controlled Reset API**:
    *   [ ] `agent.reset(reason="...")` — Must be manual and explicit.
    *   [ ] No automatic recovery from `HALTED` state.
*   **Trace Logging**:
    *   [ ] Windowed pressure history.
    *   [ ] Budget decay timelines (Effort, Risk, etc.).
    *   [ ] Exportable JSON logs for auditability.

---

## ✅ v0.7 Exit Criteria
v0.7 is considered **Complete** when an engineer can say:
> *"I plugged EmoCore into my agent loop, and it stopped itself from looping indefinitely without me writing a single signal-mapping function."*

*   ✅ EmoCore runs in a production-style agent loop.
*   ✅ Signals are derived automatically from context.
*   ✅ Invariants (Terminality, Freezing) remain untouched.
*   ✅ Quick-start time is < 5 minutes.

---

## 🚧 Out of Scope (v0.8+)
*   ❌ Long-term horizon memory.
*   ❌ Multi-agent governance aggregation.
*   ❌ Async/Distributed hardening.
*   ❌ Adaptive/Dynamic profiles.

---

> **North Star:** EmoCore exists to enforce bounded execution, not better decisions.
