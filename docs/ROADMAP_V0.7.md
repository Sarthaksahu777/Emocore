# EmoCore v0.7 Roadmap: "Plug-and-Play Governance"

## 🎯 Primary Goal
> **EmoCore can be dropped into a real agent loop without hand-wiring every signal.**

The focus of v0.7 is **accessibility and integration**. We are moving from a "governance primitive" that requires manual signal injection to a "governance layer" that automatically infers signals from agent behavior and environmental context.

---

## 🏗️ 1. Signal Extraction Layer (Automated Heuristics)
The Extraction Layer is an external wrapper that transforms raw agent telemetry into canonical EmoCore signals.

*   **Reward Extraction**:
    *   [x] Detect task success/failure via explicit flags.
    *   [x] Detect retries (identical actions or repeated tool calls).
    *   *Mapping:* Success → `+reward`; Failure/Retry → `-reward`.
*   **Novelty Extraction**:
    *   [x] State change detection (hash/snapshot diffs).
    *   [x] Tool usage divergence (new vs. repeated tools).
    *   *Mapping:* New state/tool → `+novelty`.
*   **Urgency Extraction**:
    *   [x] Wall-clock elapsed time integration.
    *   [x] Token/Step budget depletion tracking.
    *   *Mapping:* Proximity to limit → `+urgency`.
*   **Difficulty Inference (NEW)**:
    *   [x] Stagnation streak detection (no state change over $N$ steps).
    *   [x] Tool error accumulation counter.
    *   *Mapping:* High friction → `+difficulty` (requires core extension).

---

## �️ 2. Core Extensions (Minimal Support)
To enable the "Plug-and-Play" vision, minor non-breaking changes are required in the core:

*   **`Signals` Interface**: ✅ `Signals` extended with `difficulty` field.
*   **`AppraisalEngine`**: ✅ `compute()` accepts `difficulty` from public interface.
*   **`EmoEngine`**: 
    *   ✅ Implemented `reset(reason: str)` method for manual clearing of HALTED states.
    *   ✅ Exposed `pressure_log` in `EngineResult` for the Trace Logger.

---

## 🔌 3. Integration Surface (Adapters)
*   **LLM Loop Adapter**: A drop-in wrapper for standard LLM retry/generation loops that handles state and signals automatically.
*   **Tool-Calling Agent Adapter**: A wrapper that captures tool execution results, failures, and retries to map them directly to EmoCore signals.
*   **Examples Gallery (`/examples`)**:
    *   [x] **The Infinite Loop Fix**: Deterministic halt of a repeating LLM agent.
    *   [x] **The Retry Storm**: Halting an agent that keeps hitting the same tool error.
    *   [x] **Visualizer**: Multi-step task trace with budget/pressure graphs.

---

## ✅ v0.7 Exit Criteria
v0.7 is considered **Complete** when:
*   ✅ EmoCore runs in a production-style agent loop with **zero manual signal wiring**.
*   ✅ Signals are derived automatically via the Extraction Layer.
*   ✅ Invariants (Terminality, Freezing) remain untouched.
*   ✅ A manual `reset()` is the only way to recover from a `HALTED` state.

---

## � Non-Negotiable Rules
*   ❌ **No weakening of halting guarantees**: Halting must remain deterministic and final.
*   ❌ **No learning**: The governance matrices ($W, V$) remain fixed.
*   ❌ **No policy influence**: We bound capacity; we do not select actions.

---

> **North Star:** EmoCore exists to enforce bounded execution, not better decisions.

---
*Last Updated: Dec 15, 2025*
