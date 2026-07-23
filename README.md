# Scientific Calculation Utilities

A **dependency-free** Python module providing common scientific helpers: elementary functions, trigonometry, statistics, numerical methods, unit conversions, and physical constants.

## Requirements

- **Python 3.9+** (uses `from __future__ import annotations` and native tuple type hints)
- **No external dependencies** — standard library (`math`, `typing`) only

## Module Overview

| Category | Symbols |
|---|---|
| **Constants** (7) | `SPEED_OF_LIGHT`, `PLANCK`, `GRAVITATIONAL`, `AVOGADRO`, `BOLTZMANN`, `ELEMENTARY_CHARGE`, `GAS_CONSTANT` |
| **Elementary** (7) | `power`, `nth_root`, `log`, `factorial`, `combinations`, `permutations`, `hypotenuse` |
| **Trigonometry** (3) | `sin_deg`, `cos_deg`, `tan_deg` |
| **Statistics** (4) | `mean`, `median`, `variance`, `std_dev` |
| **Numerical Methods** (4) | `derivative`, `integrate`, `find_root`, `solve_quadratic` |
| **Unit Conversions** (3) | `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `celsius_to_kelvin` |

## Quick Start

Run the built-in demo:

```bash
python src/scientific.py
```

Import functions in your own code:

```python
from src.scientific import mean, derivative, celsius_to_fahrenheit, PLANCK
```

## Testing

```bash
python3 -m unittest discover tests
```

## Project Structure

```
src/scientific.py       # Main module (all public symbols in __all__)
tests/test_scientific.py # Unit tests (unittest)
```
