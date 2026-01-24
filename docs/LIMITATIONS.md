# EmoCore — Systemic Limitations and Constraints

EmoCore is a regulation primitive, not an intelligence layer. It operates within a defined scope and does not address the following classes of problems:

## 1. Signal Integrity
EmoCore takes upstream signals (Reward, Novelty, Urgency) as ground truth. It does not validate for adversarial corruption, noise, or bias. If input signals are invalid, the resulting governance will be sub-optimal or incorrect.

## 2. Objective/Goal Alignment
EmoCore regulates the *execution* of behavior relative to its internal state. It cannot correct an agent that is efficiently optimizing the wrong objective.

## 3. Cognitive Abstraction
EmoCore does not possess reasoning capabilities. It cannot synthesize new strategies, rethink problems, or invent abstractions. It only determines if the current behavioral strategy should continue, slow down, or stop.

## 4. Normative and Moral Reasoning
EmoCore is a mechanistic regulator. It does not encode moral values, ethics, or alignment beyond the boundaries defined in its behavior profile.

## 5. Deployment Scope
The current version (v0.5) is designed for single-agent governance. It does not include primitives for multi-agent coordination or distributed governance.

## Philosophical Rationale
These limitations are intentional design boundaries. By focusing exclusively on **agency regulation**, EmoCore remains a predictable, auditable, and easily integrated infrastructure component. It makes systems safer and easier to debug without increasing the complexity of their intelligence layer.
