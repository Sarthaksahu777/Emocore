# EmoCore — Non-Goals

To maintain high predictability and narrow scope, EmoCore explicitly avoids the following roles:

1. **Planning & Decision-Making**: EmoCore never decides *what* action to take or in what sequence.
2. **Policy Optimization**: EmoCore does not learn or improve the agent's action-selection policy.
3. **Reward Shaping**: EmoCore does not modify external rewards or generate intrinsic motivation signals.
4. **Action Control**: EmoCore regulates *permission to act* (the budget), not the low-level execution (e.g., control loops, motor primitives).
5. **Ethics Engine**: EmoCore is a mechanistic regulator, not a normative framework for value alignment.

---

## What EmoCore IS
EmoCore is a **runtime behavioral governance layer** focused on:
- Accumulating internal pressure from performance and stress signals.
- Translating pressure into bounded, deterministic behavioral budgets.
- Enforcing hard failure conditions when safety or progress envelopes are breached.
- Providing a stable, fail-closed foundation for autonomous systems.

---
*Last Updated: Dec 15, 2025*
