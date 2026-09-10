# scientific

Dependency-free Python module for scientific calculations: elementary functions, degree-based trigonometry, descriptive statistics, vector algebra, numerical methods, unit conversions, SI physics constants and formulas, and a safe expression evaluator with an interactive REPL and CLI.

## Requirements

- Python 3.11 or later
- No external dependencies (standard library only)

## Install

Clone the repository. No install step is needed:

```bash
git clone <repo-url>
```

## Usage

### As a library

```python
import sys
sys.path.insert(0, "src")
import scientific as sci

sci.sin_deg(30)            # 0.5
sci.mean([1, 2, 3, 4])    # 2.5
sci.dot([1, 2, 3], [4, 5, 6])  # 32.0
sci.newton_root(lambda x: x * x - 2, 1)  # ~1.414
```

### As a CLI calculator

```bash
# Run a specific function
python src/scientific.py mean 2.5 3.1 4.8

# Evaluate a free-form expression
python src/scientific.py eval "2 * sin_deg(30) + log(100, 10)"

# Start the interactive REPL
python src/scientific.py repl

# Show all subcommands
python src/scientific.py --help
```

### Run the built-in demo

```bash
python src/scientific.py
```

## Running tests

```bash
python3 -m unittest discover tests
```

## Module layout

All public functions live in `src/scientific.py`. The main groups:

| Group | Functions |
|---|---|
| Physical constants | `SPEED_OF_LIGHT`, `PLANCK`, `GRAVITATIONAL`, `AVOGADRO`, `BOLTZMANN`, `ELEMENTARY_CHARGE`, `GAS_CONSTANT` |
| Elementary | `power`, `nth_root`, `log`, `factorial`, `combinations`, `permutations`, `hypotenuse` |
| Trigonometry (degrees) | `sin_deg`, `cos_deg`, `tan_deg`, `asin_deg`, `acos_deg`, `atan_deg`, `atan2_deg` |
| Statistics | `mean`, `median`, `variance`, `std_dev`, `mode`, `percentile`, `correlation`, `linear_regression` |
| Vector algebra | `dot`, `magnitude`, `normalize`, `angle_between_deg` |
| Numerical methods | `derivative`, `integrate`, `find_root`, `newton_root`, `solve_quadratic` |
| Unit conversions | `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `celsius_to_kelvin`, `kelvin_to_celsius`, `fahrenheit_to_kelvin`, `kelvin_to_fahrenheit` |
| Physics | `gravitational_force`, `photon_energy`, `ideal_gas_pressure` |
| Expression evaluator | `evaluate` |
| Interactive REPL | `repl` |
| CLI entry point | `main` |

## Linting and formatting

CI enforces [ruff](https://docs.astral.sh/ruff/):

```bash
pip install ruff
ruff check src/
ruff format --check src/
```
