# EmoCore Benchmarks

Standardized performance and reliability benchmarks for the EmoCore governance engine.

## Contents

- `overhead/`: Measures the latency impact of adding EmoCore to an agent's `step()` loop.
- `reliability/`: Measures the false-positive and false-negative rates for halting under ambiguous signals.
- `scalability/`: Tests engine performance with long-horizon episodes (10,000+ steps).
- `base_benchmarks.py`: Comparison of IDLE vs RECOVERING performance.

## Execution

Benchmarks contribute to the CI/CD pipeline. To run local benchmarks:
```bash
pytest BENCHMARKS/
```
