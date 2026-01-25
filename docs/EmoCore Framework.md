EMOCORE

EmoCore: A Runtime Governance Layer for Regulated Agency
A Control-Theoretic Framework for Persistent Autonomous Systems

Abstract
Autonomous agents operating over long horizons face a fundamental challenge: regulating effort, risk, exploration, and persistence under uncertainty. Existing agent architectures primarily optimize decision policies but lack internal mechanisms for runtime self-regulation, leading to brittle behavior, runaway exploration, or unsafe persistence.
We introduce EmoCore, a model-agnostic governance layer that separates internal pressure accumulation from behavioral control, enforcing bounded action budgets through time- and attempt-based decay, failure classification, and hard safety guarantees. EmoCore does not select actions; instead, it regulates how much an agent is allowed to act.
We formalize the framework, describe its components, and argue that internal regulation is a necessary prerequisite for reliable long-horizon autonomy.

1. Introduction

1.1 Motivation
Autonomous agents increasingly operate without constant human oversight:
LLM-based agents
Robotics systems
Long-running decision loops
Self-improving software

However, most systems assume:
infinite retries
static risk thresholds
external supervision

This assumption fails in long-horizon, open-ended environments.


1.2 Failure Modes of Current Agents
Common observed failures:
infinite loops
over-exploration
unsafe escalation
brittle stopping conditions
silent collapse instead of explicit failure

These failures arise not from poor decision-making, but from the absence of internal governance.


1.3 Key Insight
> Intelligence optimizes actions.
Governance regulates the right to act.
Current systems conflate the two.


2. Conceptual Framework


2.1 Separation of Concerns
We distinguish four layers:
1. Signals – environmental feedback (reward, novelty, urgency)
2. Pressure State – accumulated internal variables
3. Governance – bounded behavioral budgets
4. Action Policy – task-specific decision logic
EmoCore operates strictly at layers 2–3.


2.2 Pressure vs Control
Concept	Description
Pressure	Accumulated internal signals (unbounded)
Control	Enforced behavioral limits (bounded)
Pressure can exceed safe limits.
Control must not.


2.3 Universal Control Axes
We define four control variables:
Effort – resource expenditure
Risk – tolerance for dangerous actions
Exploration – novelty tolerance
Persistence – retry endurance
These axes are substrate-independent and appear in biological, organizational, and artificial agents.


3. EmoCore Architecture


3.1 Appraisal Layer
Maps signals to pressure deltas:
\Delta S_t = f(\text{reward}, \text{novelty}, \text{urgency})
This layer:
interprets signals
does not make decisions
accumulates internal state


3.2 Pressure State Integration
Pressure evolves over time:
S_{t+1} = S_t + \Delta S_t
Pressure is not bounded and may become pathological.


3.3 Governance Layer
Governance computes bounded behavioral budgets:
B_t = g(S_t, B_{t-1}, \theta)
Where:
is the behavior budget
are profile constants
Governance enforces:
scaling
saturation
decay


3.4 Decay Mechanisms
Two decay processes are enforced:
Step-based decay – diminishing returns per attempt
Time-based decay – entropy and fatigue
Without decay, persistent agents inevitably diverge.


4. Failure Taxonomy


4.1 Explicit Failure Types
EmoCore treats failure as a first-class outcome:
EXHAUSTION – effort depleted
OVERRISK – risk tolerance exceeded
STAGNATION – no progress over window
SAFETY – hard boundary violation
EXTERNAL – time or step limit reached

Each failure has:
distinct cause
distinct recovery implications


4.2 Failure Ordering
Failure checks are ordered by severity:
1. Safety
2. Overrisk
3. Exhaustion
4. Stagnation
5. External
This ordering prevents silent unsafe behavior.


5. Guarantees and Invariants


5.1 Hard Guarantees
EmoCore enforces non-negotiable invariants:
budgets ∈ [0, 1]
halted ⇒ zero budget
control variables never increase post-halt
Guarantees override governance and policy logic.


5.2 Why Guarantees Matter
Without guarantees:
safety becomes advisory
failures propagate silently
post-halt actions still occur
Guarantees make the system fail-closed.


6. Profiles and Temperament


6.1 Profiles as Strategy Constants
Profiles define:
decay rates
scaling factors
failure sensitivity

They do not contain logic.


6.2 Comparative Profiles
We demonstrate:
Conservative agents halt earlier
Aggressive agents persist longer
Balanced agents trade off both
All share identical architecture.


7. Relation to Prior Work


7.1 Comparison Domains
EmoCore relates to:
control theory (bounded control)
affective neuroscience (homeostasis)
AI safety (runtime constraints)
organizational governance

However, unlike:
reward shaping
emotion modeling
rule-based safety

EmoCore is continuous, internal, and runtime-enforced.


7.2 What EmoCore Is Not
Not an emotion simulator
Not a policy optimizer
Not a reward function
Not a training-time constraint


8. Implications for AGI and Safety


8.1 Long-Horizon Autonomy
Any agent operating indefinitely must solve:
when to stop
when to reduce risk
when to recover

EmoCore provides this layer independent of intelligence.


8.2 Safety Without Supervision
EmoCore enables:
internal braking
explicit failure
graceful shutdown
recoverable operation


9. Limitations and Implemented Work


No learning of profiles (yet)
No multi-agent coupling
No normative ethics layer
No policy-level reasoning

These are extensions, not prerequisites.


10. Conclusion
We argue that internal governance is a missing primitive in autonomous agent design. EmoCore introduces a formal, modular framework for regulating agent behavior over time without interfering with task-level intelligence.
As autonomy scales, governance must move from external oversight to internal regulation.
> The hard problem is not making agents smarter —
it is making them know when to stop.

---
*Last Updated: Jan 25, 2026*
