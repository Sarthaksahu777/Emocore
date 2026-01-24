---
description: How to install and use EmoCore
---

# Install EmoCore

## Development Install (Editable)
```bash
pip install -e .
```

## Production Install
```bash
pip install .
```

## Install with Dev Dependencies
```bash
pip install -e ".[dev]"
```

---

# Run Tests

// turbo
```bash
python -m pytest tests/ -v
```

---

# Quick Start Example

```python
from emocore import EmoCoreAgent, step, Signals

# Create agent with default BALANCED profile
agent = EmoCoreAgent()

# Run governance loop
while True:
    result = step(agent, Signals(reward=0.5, urgency=0.1))
    print(f"Mode: {result.mode.name}, Effort: {result.budget.effort:.2f}")
    if result.halted:
        print(f"HALT: {result.failure.name}")
        break
```

---

# Run Benchmarks

```bash
python BENCHMARKS/demo.py
python BENCHMARKS/urgency_flood.py
python BENCHMARKS/infinite_loop.py
```

---

# Verify Installation

// turbo
```bash
python -c "from emocore import EmoCoreAgent, step, Signals; print('EmoCore installed successfully!')"
```
