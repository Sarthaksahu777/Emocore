# EmoCore — Signal Specification (v0.x)

> **One-Line Contract:** EmoCore converts observable agent behavior into bounded, temporal control signals and deterministically halts execution when continued action is no longer justified.

---

## Purpose

Define how observable agent behavior is converted into bounded internal control signals used to justify continuation or termination of execution.

> **Critical Scope Lock:** EmoCore ingests declared behavioral evidence, not raw observations. If evidence is incomplete or incorrect, EmoCore degrades conservatively by halting earlier.

**EmoCore does not detect correctness or progress.**  
**It detects whether continued action remains justified.**

---

## Limitations & Behavioral Risks (IMPORTANT)

EmoCore is **pessimistic by design**. Users must expect the following behaviors:

1. **Hostility to Delayed Rewards**: EmoCore punishes long periods of zero environment change. If a task requires 50 steps of "thinking" before a single file write, EmoCore will likely halt unless the adapter provides intermediate `env_state_delta` increments.
2. **The "Mean" Governor**: EmoCore will amplify bad telemetry. If an adapter is noisy or under-reports progress, EmoCore will halt early.
3. **No Distinction between Failure and Inefficiency**: EmoCore treats a perfectly correct but slow agent the same as a broken agent — it halts both to preserve budget.
4. **Path Dependence**: Due to `Signal Trust` decay, two identical actions may result in different governance decisions if the agent's historical credibility differs.
5. **Reset is an Escape Hatch**: `agent.reset()` is a manual override. Automating resets in a loop defeats the entire governance system. EmoCore makes no safety guarantees under repeated automated resets.

---

## Design Principles (Non-Negotiable)

1. Signals are derived from **behavior**, not model internals
2. Signals are **temporal**, not point-in-time
3. **No single signal** can justify continuation
4. **Frustration** (loss of control) dominates all others
5. Signal extraction may be heuristic; **halting authority lives only in core**
6. **EmoCore is pessimistic under uncertainty** and defaults toward halting unless evidence accumulates

> [!CAUTION]
> Principle 6 is load-bearing. If you remove this, future contributors will "optimize" EmoCore into an unsafe system.

---

## Architectural Scope (Path B: Extraction + Governance)

EmoCore provides **end-to-end signal extraction and governance**, not just governance of user-provided signals.

### System Boundary

```
┌────────────────────────────────────────────────────────────┐
│                        EmoCore                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │             Extractor Layer                         │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐   │   │
│  │  │ Rule-Based  │ │  LLM Agent  │ │   Custom     │   │   │
│  │  │ (default)   │ │  (future)   │ │ (user hook)  │   │   │
│  │  └─────────────┘ └─────────────┘ └──────────────┘   │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Validation Layer                         │   │
│  │    Range checks, smoothness, oscillation detection  │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Governance Layer                         │   │
│  │    Appraisal → Budgets → Mode → Halt Decision       │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

### Observable Behavior Interface

Users pass **observations**, not signals. EmoCore extracts signals internally.

```python
@dataclass(frozen=True)
class Observation:
    action: str                  # What action was taken
    result: str                  # 'success' | 'failure' | 'timeout' | 'error'
    env_state_delta: float       # External environment change [0.0, 1.0]
    agent_state_delta: float     # Internal agent change [0.0, 1.0]
    elapsed_time: float          # Seconds since episode start
    tokens_used: int = 0         # For LLM agents (optional)
    error: str | None = None     # Error message if any
```

> [!WARNING]
> **state_delta split is critical.** Without separating `env_state_delta` from `agent_state_delta`, an LLM can rewrite its thoughts forever (internal change) while the world is completely static, and EmoCore thinks progress is happening.

**Composite state_delta for extraction:**
```python
state_delta = w_env * env_state_delta + w_agent * agent_state_delta

# Default weights:
w_env = 0.7    # External change dominates
w_agent = 0.3  # Internal change contributes but doesn't dominate
```

### State Cycling Detection (Anti-Churn)

Prevents agents from gaming `env_state_delta` by writing/deleting files repeatedly.

```python
# Track recent environment state hashes
state_hash = hash(env_state)

IF state_hash in recent_hashes[-N:]:
    env_state_delta = 0  # Not actually new state
```

| Invariant | Description |
|-----------|-------------|
| S-1 | IF state_hash repeats within N steps, env_state_delta MUST be set to 0 |

### API Comparison

| Old API (manual signals) | New API (observable behavior) |
|--------------------------|-------------------------------|
| `step(agent, Signals(...))` | `observe(agent, Observation(...))` |
| User computes signals | EmoCore extracts signals |
| Power users only | Plug-and-play |

> [!NOTE]
> Both APIs coexist. `step()` remains for power users who want manual control.

### Extraction Categories

| Agent Type | Extractor | Status |
|------------|-----------|--------|
| Generic | `RuleBasedExtractor` | ✅ Default |
| LLM Agent | `LLMAgentExtractor` | 🔜 Future |
| Tool Agent | `ToolAgentExtractor` | 🔜 Future |
| Custom | User subclasses `SignalExtractor` | ✅ Available |

### Layer Responsibilities

| Layer | Responsibility | Determinism |
|-------|----------------|-------------|
| **Extractor** | Convert observations → signals | Heuristic (may vary) |
| **Validator** | Enforce signal bounds and consistency | ✅ Deterministic |
| **Governance** | Compute budgets and halt decision | ✅ Deterministic |

> [!IMPORTANT]
> **Extraction may be heuristic. Validation and governance are deterministic.**
> EmoCore provides halt guarantees *given* signals that pass validation.

---

## Signal Set (Minimal & Complete)

EmoCore operates on exactly four signals:

| Signal | Range | Meaning |
|--------|-------|---------|
| **Reward** | `[-1.0, 1.0]` | Evidence that resistance or uncertainty decreased |
| **Novelty** | `[0.0, 1.0]` | Evidence of entering new state/action regions |
| **Urgency** | `[0.0, 1.0]` | Time/budget pressure tightening tolerances |
| **Difficulty** | `[0.0, 1.0]` | Evidence of loss of controllability (Frustration) |
| **Trust** | `[0.0, 1.0]` | Internal credibility of the evidence source (Temporal) |

> [!IMPORTANT]
> **Trust is a functional multiplier.** All signals (except Difficulty) are gated by `Trust`. If Trust is 0.5, a Reward of 1.0 becomes 0.5. Difficulty is never gated as it acts as a safety brake.
| **Trust** | `[0.0, 1.0]` | Internal credibility of the evidence source (Temporal) |

> [!IMPORTANT]
> **Trust is a functional multiplier.** All signals (except Difficulty) are gated by `Trust`. If Trust is 0.5, a Reward of 1.0 becomes 0.5. Difficulty is never gated as it acts as a safety brake.

> [!IMPORTANT]
> No other signals exist in v0.x.

---

## 1. Reward Signal

**Question answered:** *Did recent actions reduce resistance relative to recent history?*

### Inputs (examples)

- Explicit success / failure flags
- Tool error vs successful execution
- Goal-state delta (expected vs actual)
- Retry exhaustion / timeout

### Rules

- Reward is **directional**, not absolute
- Reward changes **slowly**
- Reward **decays** unless reinforced by state change

### Invariants

| Invariant | Description |
|-----------|-------------|
| R-1 | Reward MUST decay if state deltas remain below threshold for N consecutive steps |
| R-2 | Reward MUST NOT override high frustration |

> [!NOTE]
> **R-1 Rationale:** "Identical action" requires action space introspection EmoCore explicitly avoids. State-delta is observable and agent-agnostic.

### Progress Detection Thresholds

Explicit bounds for detecting near-zero progress:

```python
# Default thresholds (tunable per deployment)
STATE_DELTA_THRESHOLD = 0.05   # Below this is "no meaningful progress"
STAGNATION_STEPS = 5           # Consecutive steps below threshold → frustration spike
```

| state_delta | Steps below | Effect |
|-------------|-------------|--------|
| ≥ 0.05 | - | Normal processing |
| < 0.05 | 1-4 | Reward starts decaying |
| < 0.05 | ≥ 5 | Frustration spike + stagnation flag |

> [!WARNING]
> **Near-zero progress is as dangerous as no progress.** An agent making imperceptibly small changes can run forever without meaningful results. The threshold must be set above measurement noise.

### Extraction Logic

| Observation | Effect |
|-------------|--------|
| Success | `+reward` |
| Failure | `−reward` |
| State delta below threshold | Reward decays |

> [!NOTE]
> Reward ≠ correctness. Reward = change in expected value of continuing.

---

## 2. Novelty Signal

**Question answered:** *Is the agent visiting new regions of state or action space?*

### Inputs (examples)

- State hash / structural diff
- New tool or tool-category usage
- Action diversity over sliding window
- Memory or file-system deltas

### Rules

- Novelty **decays rapidly** with repetition
- Novelty contribution is **scaled by frustration** (quadratic suppression)
- Novelty alone **never justifies continuation**

### Effective Novelty Formula

```python
effective_novelty = novelty * (1.0 - frustration ** 2)
```

| Frustration | Novelty Strength |
|-------------|------------------|
| 0.3 | 91% |
| 0.6 | 64% |
| 0.8 | 36% |
| 0.95 | ~10% |

> [!TIP]
> **Quadratic scaling** provides smooth degradation with no cliff edges. High novelty at moderate frustration still contributes meaningfully (emergent grace window).

### Invariants

| Invariant | Description |
|-----------|-------------|
| N-1 | Novelty MUST → 0 under stagnation |
| N-2 | Novelty contribution MUST be scaled down by frustration² |
| N-3 | IF novelty > 0.8 AND frustration > 0.6 → grace window of `min(5, novelty × 10)` steps before full suppression |
| N-4 | Urgency CAPS grace windows (threat/time pressure beats curiosity) |
| N-5 | Novelty debt accumulates when novelty is high but reward doesn't improve |

### Grace Window Logic

```
IF frustration > threshold THEN
    effective_novelty = novelty × (1 - frustration)²
    
    IF urgency > 0.7 THEN
        grace_window = 0  # Urgency caps grace window
    ELSE
        grace_window = novelty > 0.8 → 5 steps of reduced suppression
    
    AFTER grace_window:
        IF state_delta < threshold → HALT (novelty was exploration theater)
        ELSE → novelty contribution restored partially
```

### Novelty Debt (Anti-Gaming Mechanism)

Prevents agents from oscillating between novel-looking but equivalent states.

```python
# Novelty debt accumulates when novelty is high but reward doesn't improve
novelty_debt += novelty * (1 if reward <= 0 else 0)

IF novelty_debt > limit THEN
    novelty → 0  # Forced suppression
```

| novelty_debt | Effect |
|--------------|--------|
| < 3.0 | Normal novelty contribution |
| 3.0 - 5.0 | Novelty scaled by 0.5 |
| > 5.0 | Novelty forced to 0 (exploration theater detected) |

### Novelty Debt Recovery

When the agent finally succeeds, debt gradually forgives:

```python
IF reward > 0.5:
    novelty_debt *= 0.8  # Gradual recovery on success
```

> [!NOTE]
> Without recovery, an agent that eventually succeeds would still be punished for past exploration. Asymmetric: decay is fast, recovery is slow.

> [!WARNING]
> Novelty = entropy delta, not usefulness. Novelty without resistance reduction is dangerous. The "Hail Mary" gets a chance, but it must produce results within the grace window.

---

## 3. Urgency Signal

**Question answered:** *How fast must justification be resolved?*

### Inputs (examples)

- Wall-clock elapsed time
- Remaining step / token / cost budget
- Deadline proximity

### Rules

- Urgency increases **monotonically within an episode**
- Episode reset → urgency resets
- Budget extension → urgency recalculates from new constraints
- Urgency tracks `max(time_pressure, budget_pressure)`, not their sum
- Urgency **tightens thresholds**; it **never relaxes** them

### Invariants

| Invariant | Description |
|-----------|-------------|
| U-1 | Urgency MUST NOT justify continuation |
| U-2 | High urgency + low reward ⇒ faster halt |
| U-3 | Urgency is monotonic WITHIN an episode only |

### Extraction Logic

| Observation | Effect |
|-------------|--------|
| Time passes | Urgency increases monotonically |
| Deadline approaches | Nonlinear ramp |
| Episode reset | Urgency resets to 0 |

> [!CAUTION]
> Urgency accelerates failure — it does not override safety.

---

## 4. Difficulty / Frustration Signal (Dominant)

**Question answered:** *Is the system losing controllability?*

### Inputs (examples)

- Failure streak length
- State unchanged for N steps
- Action oscillation (A↔B loops)
- Tool error accumulation

### Rules

- Frustration rises with **effort spent without resistance reduction**
- Frustration decays **slowly and asymmetrically**

### Dominance Invariant (Critical)

```
IF frustration > threshold THEN:
    novelty contribution scaled by (1 - frustration²)
    exploration → suppressed
    persistence → capped
    risk → capped

IF frustration > max ⇒ HALT
```

### Invariants

| Invariant | Description |
|-----------|-------------|
| D-1 | Frustration MUST dominate all other signals above threshold |
| D-2 | Frustration above max MUST trigger unconditional halt |

> [!IMPORTANT]
> Frustration is not emotion — it is control loss detection.

---

## Signal Validation Layer

EmoCore validates all signals before processing. Validation is **deterministic**.

### Validation Constraints

| Constraint | Rule |
|------------|------|
| **Range bounds** | All signals must be within declared ranges |
| **Smoothness** | No signal may change by >0.5 in a single step |
| **Non-oscillation** | **Reward (Trust-adjusted)** cannot flip direction >3× in 10 steps |

### V-3: Oscillation Detection Details

Oscillation detection happens **Post-Extraction (after Trust is applied) but Pre-Validation Clamping**. It specifically monitors the `Reward` sign. Rapid flipping indicates an unstable adapter or a "shining" state estimation. EmoCore treats this as a loss of controllability.

### Strictness Modes

| Mode | Behavior |
|------|----------|
| `strict=False` (default) | Clamp out-of-range values, log warning, continue |
| `strict=True` | Raise `ValidationError` on constraint violation |

> [!NOTE]
> Default `strict=False` provides graceful degradation for production. Use `strict=True` in tests to catch bugs early.

### Determinism Contract

| Layer | Determinism |
|-------|-------------|
| Signal Extraction | ❌ May be heuristic (user-provided) |
| Signal Validation | ✅ Deterministic (bounds, smoothness) |
| Governance Core | ✅ Deterministic (given valid signals) |
| Halt Decision | ✅ Deterministic (given governance state) |

> **EmoCore provides deterministic halt guarantees *given* signals that satisfy validation constraints.**

---

## Signal Trust (Credibility Decay)

Signals are not blindly trusted. Trust decays when signals fail to produce downstream justification.

### Signal Trust Scalar

```python
signal_trust ∈ [0.0, 1.0]  # Global credibility

# Trust decays when:
# - Novelty is high but reward doesn't improve
# - Reward oscillates without trend
# - state_delta is inconsistent

# Trust gates all signals:
effective_signal = signal * signal_trust
```

### Trust Rules

| Condition | Trust Effect |
|-----------|-------------|
| Novelty high, reward flat | Trust decays by 0.1/step |
| Reward oscillates >3× in 10 steps | Trust decays by 0.2 |
| state_delta inconsistent with result | Trust decays by 0.15 |
| Consistent positive trends | Trust recovers by 0.05/step |

> [!IMPORTANT]
> **Signal trust provides immunity to fake signals.** This is not learning — it is confidence decay. This is how human frustration works and how control systems reduce gain under noise.

---

## Temporal Logic (Core Insight)

Signals are **evidence accumulators**, not labels.

### Continuation is justified only if:

- Difficulty is **decreasing**, OR
- Novelty is **decreasing** while reward **stabilizes**, OR
- System transitions from exploratory → **focused behavior**

### Termination is justified if:

- Effort rises while state deltas remain flat
- Novelty remains high but difficulty does not decrease  
- Urgency rises while reward remains non-positive
- Frustration crosses dominance threshold

---

## Extraction Architecture Patterns

All patterns are valid; EmoCore stays agnostic to implementation.

| Pattern | When to Use |
|---------|-------------|
| **Event-driven** | Clean agent with event hooks |
| **Middleware / interceptor** | Minimal agent changes |
| **Wrapper / observer** | Zero agent modification |
| **Log parsing** | Existing systems, post-hoc |

> [!NOTE]
> Extraction may be heuristic. Authority stays in core.

### Design Decision

| Approach | Verdict |
|----------|---------|
| Pure heuristics | ✅ Preferred (interpretable, deterministic) |
| ML-based extraction | ❌ Optional, later, never authoritative |
| Hybrid | ⚠️ Only if signals stay bounded & explainable |

**Rationale:** EmoCore's job is termination guarantees, not prediction accuracy.

---

## Explicit Non-Goals

This spec explicitly does **NOT**:

- Infer intent
- Detect correctness
- Optimize reward
- Learn signal mappings
- Choose actions

**It only governs whether action may continue.**

---

## Sanity Check

> If someone asks: *"How does EmoCore know it's making progress?"*
>
> The only correct answer is:
>
> **"It doesn't. It only knows when continuing can no longer be justified."**

If this answer ever becomes incorrect, the system is broken.

---

## Summary

> EmoCore extracts **reward**, **novelty**, **urgency**, and **difficulty** from observable agent behavior using rule-based, temporal feature extraction. These signals do not infer correctness or intent; they accumulate evidence for or against continued execution. **Frustration** (loss of controllability) dominates all other signals, ensuring bounded execution and deterministic halting under long-horizon stress.

---

## Appendix: Design Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Reward invariant R-1 | State-delta based decay | Action-agnostic, observable |
| Novelty suppression | Quadratic scaling `(1 - frustration²)` | Smooth, no cliff edges |
| Urgency reset | Implicit on episode reset | Semantic clarity, simpler API |
| Validation strictness | `strict=False` default | Graceful degradation in production |
| **Explicit pessimism** | Principle 6: default toward halting | Prevents "optimization" into unsafe system |
| **state_delta split** | Separate env vs agent internal change | Prevents LLMs from faking progress via thought rewrites |
| **Novelty debt** | Accumulates when novelty high but reward flat | Detects and halts exploration theater |
| **Novelty debt recovery** | 0.8× decay on reward > 0.5 | Don't punish success for past exploration |
| **Signal trust** | Global credibility scalar, decays on inconsistency | Immunity to fake/adversarial signals |
| **Urgency caps grace windows** | Threat beats curiosity | Biology + control theory aligned |
| **State cycling detection (S-1)** | Hash repeat → env_state_delta = 0 | Closes file-churn exploit |
| **Default weights** | w_env=0.7, w_agent=0.3 | External change matters more |
| **Progress thresholds** | Configurable via extractor (Default: 0.05 / 5 steps) | Addresses "hidden unit problem" for different adapters |
| **Trust promotion** | trust promoted to first-class Signal | Increases transparency, eliminates "hidden" path dependence |
| **Oscillation Anchor** | detection pinned to Trust-adjusted Reward | Eliminates spec ambiguity for consistent implementations |

---

## Appendix: Model-Specific Extraction Guide

The Observation interface is **minimally model-agnostic**. Here's how to extract signals for different agent types.

### LLM Agents (Claude, GPT, Gemini)

| Field | How to Extract |
|-------|----------------|
| `action` | Tool/function call name, or `"generate"` for pure text |
| `result` | `"success"` if tool executed, `"failure"` on exception, `"error"` on refusal |
| `env_state_delta` | `new_information_tokens / context_window_size` — how much new external info was added |
| `agent_state_delta` | Token diversity: `len(set(tokens)) / len(tokens)` — proxy for reasoning change |
| `elapsed_time` | Wall clock since conversation start |
| `tokens_used` | Native from API response |
| `error` | Error message from tool or API |

**LLM-specific interpretation:**
```python
# For pure chat (no tools):
env_state_delta = 0.0  # No external state change
agent_state_delta = response_length_change / max_length  # Internal "thinking" change

# For tool-using LLM:
env_state_delta = tool_output_changed(before, after)
agent_state_delta = reasoning_changed(prev_chain_of_thought, current)
```

> [!WARNING]
> **LLM without tools:** If the agent never calls tools, `env_state_delta` will always be 0. This triggers stagnation detection quickly — which is correct behavior (pure text generation without external action is not progress).

---

### Tool Agents (ReAct, Function Calling)

| Field | How to Extract |
|-------|----------------|
| `action` | Tool name: `"read_file"`, `"web_search"`, `"execute_code"` |
| `result` | Tool return code: `"success"`, `"failure"`, `"timeout"` |
| `env_state_delta` | `hash(env_state_after) != hash(env_state_before)` → 1.0, else 0.0 |
| `agent_state_delta` | Scratchpad/memory change ratio |
| `elapsed_time` | Wall clock since task start |
| `tokens_used` | Sum of all LLM calls if applicable |
| `error` | Tool error message |

**Tool-specific interpretation:**
```python
# File operations
env_state_delta = file_system_changed(before, after)

# Database operations
env_state_delta = db_rows_affected > 0

# Web operations
env_state_delta = new_urls_fetched > 0

# Code execution
env_state_delta = stdout_changed or files_modified
```

---

### Game AI / RL Agents

| Field | How to Extract |
|-------|----------------|
| `action` | Action ID or name |
| `result` | `"success"` if game state valid, `"failure"` on invalid move |
| `env_state_delta` | `game_state_hash_delta / max_delta` |
| `agent_state_delta` | Policy entropy change or Q-value shift |
| `elapsed_time` | Episode time or step count / max_steps |
| `tokens_used` | N/A (set to 0) |
| `error` | Game error message |

---

### Robotics / Embodied Agents

| Field | How to Extract |
|-------|----------------|
| `action` | Motor command or action primitive |
| `result` | Sensor confirmation of action execution |
| `env_state_delta` | Sensor readings diff (camera, lidar, etc.) |
| `agent_state_delta` | Internal planner state change |
| `elapsed_time` | Wall clock |
| `tokens_used` | N/A (set to 0) |
| `error` | Hardware error or safety violation |

---

### Custom Agents (User-Defined)

Subclass `SignalExtractor` and implement:

```python
from emocore.extractors import SignalExtractor, Observation, Signals

class MyCustomExtractor(SignalExtractor):
    def extract(self, observation: Observation) -> Signals:
        # Your domain-specific extraction logic
        reward = self._compute_reward(observation)
        novelty = self._compute_novelty(observation)
        urgency = self._compute_urgency(observation)
        difficulty = self._compute_difficulty(observation)
        
        return Signals(
            reward=reward,
            novelty=novelty,
            urgency=urgency,
            difficulty=difficulty
        )
    
    def reset(self):
        # Clear any stateful tracking between episodes
        self.history = []
```

---

### Extraction Compatibility Matrix

| Agent Type | env_state_delta | agent_state_delta | Practical? |
|------------|-----------------|-------------------|------------|
| LLM + Tools | ✅ Easy | ⚠️ Heuristic | ✅ Yes |
| LLM Pure Chat | ❌ Always 0 | ⚠️ Heuristic | ⚠️ Limited |
| Tool Agent | ✅ Easy | ✅ Scratchpad | ✅ Yes |
| Game AI | ✅ Game state | ✅ Policy state | ✅ Yes |
| Robotics | ✅ Sensors | ✅ Planner | ✅ Yes |
| Custom | Depends | Depends | ✅ User controls |

> [!NOTE]
> **Pure chat LLMs** (no tools) will trigger faster halts because `env_state_delta = 0`. This is intentional — text generation without external action is not observable progress.


