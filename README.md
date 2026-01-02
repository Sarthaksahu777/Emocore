# EmoCore

EmoCore is a runtime governance layer that enforces hard behavioral bounds
in autonomous agents.

It does not improve reasoning.
It does not optimize performance.
It decides when execution must halt — even if the agent wants to continue.

## What EmoCore Proves

- Autonomous systems fail under sustained pressure
- Recovery exists but is bounded
- Some behaviors must be unreachable by design
- Halting is safer than escalation

## What EmoCore Does NOT Do

- It does not make agents safer
- It does not align agents
- It does not optimize emotions or behavior
- It does not prevent failure

## Canonical Tests

- Infinite loop → EXHAUSTION
- Urgency flood → ACCELERATED EXHAUSTION
- Recovery boundary → bounded insufficiency
- Post-halt integrity → fail-closed

Run tests in `LLM testing/`.

## Design Invariants

See `docs/INVARIANTS.md`.
