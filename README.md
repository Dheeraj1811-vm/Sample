# scientific

A dependency-free Python module of scientific helpers: elementary functions, trigonometry, statistics, vector algebra, numerical methods, unit conversions, physics formulas, and a built-in expression evaluator.

Works as both a library and a command-line calculator.

## Requirements

- Python 3.11+
- No external dependencies

## CLI Usage

```bash
# Run a subcommand
python src/scientific.py mean 2.5 3.1 4.8
python src/scientific.py dot 1,2,3 4,5,6
python src/scientific.py log 1024 --base 2
python src/scientific.py gravitational-force 5.972e24 7.348e22 3.844e8

# Evaluate a full expression
python src/scientific.py eval "2 * sin_deg(30) + log(100, 10)"
python src/scientific.py eval "integrate(sin_deg(x), 0, 180)"

# Interactive REPL
python src/scientific.py repl

# Print physical constants
python src/scientific.py constants

# Short demo
python src/scientific.py

# All commands accept --json for machine-readable output
python src/scientific.py mean 1 2 3 --json
```

Run `python src/scientific.py --help` for the full list of subcommands.

## Library Usage

```python
import sys
sys.path.insert(0, "src")
from scientific import mean, sin_deg, gravitational_force, evaluate

mean([1, 2, 3])           # 2.0
sin_deg(30)               # 0.499999...
gravitational_force(5.972e24, 7.348e22, 3.844e8)  # ~1.98e20 N

# Expression evaluator (safe, no eval())
evaluate("2 * sin_deg(30) + log(100, 10)")  # 3.0
```

## Module Overview

| Section | Functions |
|---|---|
| Constants | `SPEED_OF_LIGHT`, `PLANCK`, `GRAVITATIONAL`, `AVOGADRO`, `BOLTZMANN`, `ELEMENTARY_CHARGE`, `GAS_CONSTANT` |
| Elementary | `power`, `nth_root`, `log`, `factorial`, `combinations`, `permutations`, `hypotenuse` |
| Trigonometry | `sin_deg`, `cos_deg`, `tan_deg`, `asin_deg`, `acos_deg`, `atan_deg`, `atan2_deg` |
| Statistics | `mean`, `median`, `mode`, `percentile`, `variance`, `std_dev`, `correlation`, `linear_regression` |
| Vectors | `dot`, `magnitude`, `normalize`, `angle_between_deg` |
| Numerical Methods | `derivative`, `integrate`, `find_root`, `newton_root`, `solve_quadratic` |
| Unit Conversions | `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `celsius_to_kelvin`, `kelvin_to_celsius`, `fahrenheit_to_kelvin`, `kelvin_to_fahrenheit` |
| Physics | `gravitational_force`, `photon_energy`, `ideal_gas_pressure` |
| Evaluator / REPL | `evaluate`, `repl`, `main` |

## Tests

```bash
python3 -m unittest discover tests
```

