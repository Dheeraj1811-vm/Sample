# Sample — Scientific Calculation Utilities

A dependency-free Python library of common scientific helpers: elementary functions, trigonometry, statistics, vector algebra, numerical methods, unit conversions, and physics formulas.

## Requirements

- Python 3.11+
- No external dependencies (stdlib only)

## Usage

Add `src/` to your path and import the `scientific` module:

```python
import sys
sys.path.insert(0, "src")

from scientific import sin_deg, mean, integrate, celsius_to_fahrenheit

print(sin_deg(30))          # 0.5
print(mean([1, 2, 3]))      # 2.0
print(integrate(math.sin, 0, math.pi))  # ≈ 2.0
print(celsius_to_fahrenheit(100))       # 212.0
```

Or run the built-in demo:

```bash
python src/scientific.py
```

## Module Overview

| Section | Examples |
|---------|----------|
| Elementary functions | `power`, `nth_root`, `log`, `factorial`, `combinations`, `permutations`, `hypotenuse` |
| Trigonometry (degrees) | `sin_deg`, `cos_deg`, `tan_deg`, `asin_deg`, `acos_deg`, `atan_deg`, `atan2_deg` |
| Statistics | `mean`, `median`, `variance`, `std_dev`, `mode`, `percentile`, `correlation`, `linear_regression` |
| Vector algebra | `dot`, `magnitude`, `normalize`, `angle_between_deg` |
| Numerical methods | `derivative`, `integrate`, `find_root`, `newton_root`, `solve_quadratic` |
| Unit conversions | `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `celsius_to_kelvin`, `kelvin_to_celsius`, `fahrenheit_to_kelvin`, `kelvin_to_fahrenheit` |
| Physics (SI) | `gravitational_force`, `photon_energy`, `ideal_gas_pressure` |
| Constants (CODATA 2018) | `SPEED_OF_LIGHT`, `PLANCK`, `GRAVITATIONAL`, `AVOGADRO`, `BOLTZMANN`, `ELEMENTARY_CHARGE`, `GAS_CONSTANT` |

## Running Tests

```bash
python3 -m unittest discover tests -v
```

## Project Structure

```
├── src/
│   └── scientific.py        # Main module (all functions and constants)
├── tests/
│   └── test_scientific.py   # Unit tests (unittest)
├── .github/
│   └── workflows/
│       └── ci.yml           # CI pipeline (lint + smoke)
└── .gitignore
```
