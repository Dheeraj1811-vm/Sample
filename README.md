# Scientific Calculator

A dependency-free Python module of scientific helper functions: elementary
math, degree-based trigonometry, statistics, numerical methods, unit
conversions, and SI physical constants (CODATA 2018).

## Requirements

- Python 3 (standard library only — no third-party packages, no install step)

## Usage

```python
import sys
sys.path.insert(0, "src")

import scientific as sci

sci.nth_root(-8, 3)          # -2.0 (real-valued odd roots)
sci.sin_deg(30)              # 0.5
sci.std_dev([1.0, 2.0, 3.0]) # sample standard deviation
sci.find_root(lambda x: x * x - 2, 0, 2)  # bisection
```

Or run the built-in demonstration:

```bash
python3 src/scientific.py
```

## Tests

Run from the project root:

```bash
python3 -m unittest discover tests
```

## Project layout

| Path | Description |
| --- | --- |
| `src/scientific.py` | The module: constants, functions, and the `__main__` demo |
| `tests/test_scientific.py` | `unittest` test suite (elementary, trig, statistics, numerical methods, conversions, constants) |
