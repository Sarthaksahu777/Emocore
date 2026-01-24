# LLM Testing

This directory contains specialized evaluation scripts designed to stress-test EmoCore's governance over Large Language Model (LLM) agent loops.

## Contents

- `llm_loop_emocore.py`: Demonstrates EmoCore's ability to halt a yapping or stagnant LLM loop.
- `llm_loop_raw.py`: The baseline (non-governed) version of the same loop.
- `post_halt_integrity_emocore.py`: Verifies that EmoCore invariants hold after a halt (Budget stays at 0).
- `recovery_boundary_emocore.py`: Tests the mathematical limits of the `RECOVERING` mode.
- `urgency_flood_emocore.py`: Tests how rapidly increasing urgency accelerates halting.
- `profile_divergence_emocore.py`: Compares how different EmoCore profiles (CONSERVATIVE vs AGGRESSIVE) respond to the same stimuli.

## Usage

Run these scripts from the project root:
```bash
python "LLM testing/llm_loop_emocore.py"
```
