# scientific

Dependency-free scientific calculation library with a built-in CLI calculator.

## Modules

- **Elementary** — `power`, `nth_root`, `log`, `factorial`, `combinations`, `permutations`, `hypotenuse`
- **Trigonometry** — `sin_deg`, `cos_deg`, `tan_deg`, `asin_deg`, `acos_deg`, `atan_deg`, `atan2_deg`
- **Statistics** — `mean`, `median`, `variance`, `std_dev`, `mode`, `percentile`, `correlation`, `linear_regression`
- **Vectors** — `dot`, `magnitude`, `normalize`, `angle_between_deg`
- **Numerical methods** — `derivative`, `integrate`, `find_root`, `newton_root`, `solve_quadratic`
- **Unit conversions** — `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `celsius_to_kelvin`, `kelvin_to_celsius`, `fahrenheit_to_kelvin`, `kelvin_to_fahrenheit`
- **Physics** — `gravitational_force`, `photon_energy`, `ideal_gas_pressure`
- **Constants** — `SPEED_OF_LIGHT`, `PLANCK`, `GRAVITATIONAL`, `AVOGADRO`, `BOLTZMANN`, `ELEMENTARY_CHARGE`, `GAS_CONSTANT`

All functions live in `src/scientific.py`. There are no external dependencies.

## Usage

### As a library

```python
import sys
sys.path.insert(0, "src")
from scientific import mean, sin_deg, gravitational_force

mean([2.5, 3.1, 4.8])
sin_deg(30)
gravitational_force(5.972e24, 7.348e22, 3.844e8)
```

### As a CLI calculator

Run a function directly:

```bash
python src/scientific.py mean 2.5 3.1 4.8
python src/scientific.py sin_deg 30
```

Evaluate an expression:

```bash
python src/scientific.py eval "2 * sin_deg(30) + log(100, 10)"
```

Start the interactive REPL:

```bash
python src/scientific.py repl
```

Show all subcommands:

```bash
python src/scientific.py --help
```

### Expression syntax

The expression evaluator (`evaluate()`) supports:

- Arithmetic: `+ - * / % ^` (`**` is accepted as `^`)
- Parentheses and lists: `[1, 2, 3]`
- Any public function name from `src/scientific.py`
- Constants: `pi`, `e`, `tau`, `sqrt`, `exp`, `abs`
- Variable assignment: `x = 2.5` (REPL only, persists across lines)
- Function-as-expression: `derivative(x^2, 3)` binds `x` to the expression

## Tests

```bash
python3 -m unittest discover tests -v
```

Tests use the standard library `unittest` framework. See `tests/test_scientific.py`.

## Development

### Lint and format

```bash
pip install ruff
ruff check src/
ruff format --check src/
```

### Run the demo

```bash
python src/scientific.py
```

With no arguments the module prints a short demonstration of all subsystems.

## Requirements

- Python 3.11+
- No third-party packages
