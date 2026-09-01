# Scientific Calculation Utilities

A dependency-free Python library of common scientific helpers: elementary functions, trigonometry, statistics, vector algebra, numerical methods, unit conversions, and physical constants with the formulas that use them.

## Requirements

- Python 3.11+

No external dependencies.

## Usage

Add `src/` to your Python path and import:

```python
import sys; sys.path.insert(0, "src")
import scientific as sci

sci.mean([1, 2, 3])
sci.linear_regression([0, 1, 2], [1, 3, 5])
sci.photon_energy(500e-9)
```

Or run the built-in demo:

```bash
python src/scientific.py
```

## Module Sections

| Section | Key functions |
|---|---|
| Elementary | `power`, `nth_root`, `log`, `factorial`, `combinations`, `permutations`, `hypotenuse` |
| Trigonometry | `sin_deg`, `cos_deg`, `tan_deg`, `asin_deg`, `acos_deg`, `atan_deg`, `atan2_deg` |
| Statistics | `mean`, `median`, `variance`, `std_dev`, `mode`, `percentile`, `correlation`, `linear_regression` |
| Vector algebra | `dot`, `magnitude`, `normalize`, `angle_between_deg` |
| Numerical methods | `derivative`, `integrate`, `find_root`, `newton_root`, `solve_quadratic` |
| Unit conversions | `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `celsius_to_kelvin`, `kelvin_to_celsius`, `fahrenheit_to_kelvin`, `kelvin_to_fahrenheit` |
| Physics (SI) | `gravitational_force`, `photon_energy`, `ideal_gas_pressure` |

## Physical Constants

CODATA 2018 values (SI units): `SPEED_OF_LIGHT`, `PLANCK`, `GRAVITATIONAL`, `AVOGADRO`, `BOLTZMANN`, `ELEMENTARY_CHARGE`, `GAS_CONSTANT`.

## Running Tests

```bash
python3 -m unittest discover tests
```

## Linting

```bash
ruff check src/
ruff format --check src/
```
