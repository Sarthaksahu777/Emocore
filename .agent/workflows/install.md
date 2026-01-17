---
description: Official installation and configuration guide for the EmoCore Runtime Governance Layer.
---

# 📦 EmoCore Installation Manual

This manual provides authoritative instructions for installing, configuring, and verifying the EmoCore governance framework.

## 📋 Prerequisites

Before proceeding, ensure your environment meets the following requirements:
*   **Python:** 3.10 or higher
*   **Operating System:** Linux, macOS, or Windows
*   **Package Manager:** `pip` (standard with Python)

---

## 🛠️ Installation Procedures

### 1. Standard Installation
For general use in agentic applications.
```bash
pip install .
```

### 2. Developer Installation (Recommended)
Recommended for contributors or users needing real-time updates without re-installing.
```bash
pip install -e .
```

### 3. Full Development Suite
Includes testing frameworks (Pytest) and coverage tools.
```bash
pip install -e ".[dev]"
```

---

## ✅ Verification

To confirm the installation is valid and the core logic is operational, run the following "turbo" check:

// turbo
```bash
python -c "from core import EmoCoreAgent; agent = EmoCoreAgent(); print(f'EmoCore v{agent.__version__} Ready.')"
```

---

## 🚀 Quick Start

Initialize EmoCore in your agent's loop with these 5 lines:

```python
from core import EmoCoreAgent, step, Signals

# Initialize with default BALANCED profile
agent = EmoCoreAgent()

# Inject signals and receive governance decisions
result = step(agent, Signals(reward=0.8, urgency=0.2))

print(f"Status: {result.mode.name} | Budget Remaining: {result.budget.effort:.2f}")
```

---

## 🧪 Testing & Validation

### Run Unit Tests
// turbo
```bash
python -m pytest tests/ -v
```

### Execute Performance Benchmarks
```bash
python BENCHMARKS/demo.py
python BENCHMARKS/urgency_flood.py
```

---

> [!IMPORTANT]
> **Production Note:** EmoCore is a deterministic governance layer. If the system enters `HALTED` mode, it is an indication of a hard constraint violation. Always ensure your agent logic handles `result.halted` conditions to prevent unsafe execution.
