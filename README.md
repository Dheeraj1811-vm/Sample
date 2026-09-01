# scientific

A dependency-free Python module of scientific calculation helpers, usable both as a library and as a command-line calculator.

It covers elementary functions, trigonometry, statistics, vector algebra, numerical methods, unit conversions, and physical constants (plus the formulas built on them). It has no third-party dependencies and runs on the Python standard library (Python 3.11, per CI).

## Features

- **Elementary** — `power`, `nth_root`, `log`, `factorial`, `combinations`, `permutations`, `hypotenuse`
- **Trigonometry** (degrees) — `sin_deg`, `cos_deg`, `tan_deg`, `asin_deg`, `acos_deg`, `atan_deg`, `atan2_deg`
- **Statistics** — `mean`, `median`, `mode`, `variance`, `std_dev`, `percentile`, `correlation`, `linear_regression`
- **Vector algebra** — `dot`, `magnitude`, `normalize`, `angle_between_deg`
- **Numerical methods** — `derivative`, `integrate`, `find_root`, `newton_root`, `solve_quadratic`
- **Unit conversions** — Celsius / Fahrenheit / Kelvin in every direction
- **Physics** — `gravitational_force`, `photon_energy`, `ideal_gas_pressure`, built on the module's SI constants

## Command line

Run with no arguments for a short demo, or pass a subcommand:

```bash
python src/scientific.py                 # run the demo
python src/scientific.py --help          # list every subcommand
python src/scientific.py constants       # print the physical constants
python src/scientific.py mean 2.5 3.1 4.8
python src/scientific.py solve-quadratic 1 2 5
python src/scientific.py dot 1,2,3 4,5,6
python src/scientific.py photon-energy 500e-9 --json
```

- Subcommands mirror the function names with hyphens instead of underscores (e.g. `std-dev`, `solve-quadratic`).
- Single-sequence inputs are space separated; two-sequence commands take comma-separated groups (e.g. `dot 1,2,3 4,5,6`).
- `--json` prints the result as a JSON object on any subcommand.
- `variance` and `std-dev` are sample-based by default; pass `--population` for population statistics.
- Functions that require a callable — `derivative`, `integrate`, `find_root`, `newton_root` — are library-only: the CLI has no expression parser yet.

## Using it as a library

There is no install step (no package metadata is shipped); put `src/` on the path and import `scientific`:

```bash
PYTHONPATH=src python -c "import scientific; print(scientific.mean([1, 2, 3]))"
```

## Development

```bash
# run the test suite (standard-library unittest)
python -m unittest discover -s tests

# lint and format check (as CI runs them)
ruff check src/
ruff format --check src/
```

## CI

`.github/workflows/ci.yml` runs two jobs on push and pull request to `main`: **lint** (`ruff check src/` and `ruff format --check src/`) and **smoke** (imports the module).

## Project layout

```
src/scientific.py          # the module: library API + CLI
tests/test_scientific.py   # unittest test suite
.github/workflows/ci.yml   # CI: lint + smoke
```
