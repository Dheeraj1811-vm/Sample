# AGENTS.md

## Purpose

Operational guidance for coding agents working in this repository.

## Project Snapshot

- Dependency-free (stdlib-only) Python scientific-utilities module and CLI calculator.
- Single-module design: all code lives in `src/scientific.py`.
- Python 3.11 (enforced by CI; no local version pin in-repo).
- No packaging manifest (`pyproject.toml`, `setup.py`, `requirements*.txt` are absent).

## Toolchain and Verification

| Task | Command | Notes |
|---|---|---|
| Lint | `ruff check src/` | CI-only enforcement; no local ruff config |
| Format | `ruff format --check src/` | CI-only enforcement |
| Tests | `python3 -m unittest discover tests` | Run from project root; uses stdlib `unittest` |
| Smoke / import | `python -c "import sys; sys.path.insert(0, 'src'); import scientific; print('ok')"` | Same as CI smoke job |

CI workflow: `.github/workflows/ci.yml` (triggers on push/PR to `main`).

## Architecture or Context Map

- `src/scientific.py` — the entire module: constants, math, statistics, vectors, numerical methods, unit conversions, physics, and CLI entrypoint.
- `tests/test_scientific.py` — `unittest` test suite; inserts `src/` into `sys.path` before import.
- `.github/workflows/ci.yml` — lint + smoke jobs.
- No `__init__.py`; `src/` is added to `sys.path` by the test file and by the CLI script's own execution path.

### Public API groups (all in `src/scientific.py`)

| Group | Examples |
|---|---|
| Physical constants | `SPEED_OF_LIGHT`, `PLANCK`, `GRAVITATIONAL`, `AVOGADRO`, `BOLTZMANN`, `ELEMENTARY_CHARGE`, `GAS_CONSTANT` |
| Elementary | `power`, `nth_root`, `log`, `factorial`, `combinations`, `permutations`, `hypotenuse` |
| Trig (degrees) | `sin_deg`, `cos_deg`, `tan_deg`, `asin_deg`, `acos_deg`, `atan_deg`, `atan2_deg` |
| Statistics | `mean`, `median`, `variance`, `std_dev`, `mode`, `percentile`, `correlation`, `linear_regression` |
| Vectors | `dot`, `magnitude`, `normalize`, `angle_between_deg` |
| Numerical | `derivative`, `integrate`, `find_root`, `newton_root`, `solve_quadratic` |
| Unit conversions | `celsius_to_fahrenheit`, `fahrenheit_to_celsius`, `celsius_to_kelvin`, `kelvin_to_celsius`, `fahrenheit_to_kelvin`, `kelvin_to_fahrenheit` |
| Physics | `gravitational_force`, `photon_energy`, `ideal_gas_pressure` |
| CLI | `evaluate`, `repl`, `main` |

## CLI Notes

- Invocation: `python src/scientific.py <subcommand> [args]`
- Subcommand names are **hyphenated** (e.g. `nth-root`, `std-dev`, `solve-quadratic`); the underlying functions use underscores.
- Static subcommands: `demo`, `constants`, `eval`, `repl`.
- `--json` flag available on most subcommands (not on `demo`/`repl`).
- Exit codes: 0 = success, 1 = domain/runtime error, 2 = argparse usage error.
- `eval` uses a safe recursive-descent parser; Python `eval()` is **never** called.

## Boundaries

### Always

- Keep the module stdlib-only. Do not add third-party imports.
- Raise `ValueError` on invalid or domain-violating input (consistent with existing functions).
- Run `ruff check src/` and `ruff format --check src/` before committing.

### Never

- Import third-party packages.
- Use Python `eval()` or `exec()` in `src/scientific.py`.
- Add a packaging manifest, linter config file, or test runner config unless explicitly requested.

### Ask First

- Adding new physical constants or changing existing CODATA 2018 values.
- Changing CLI subcommand names or adding new subcommands.
- Modifying the `eval` subcommand's parser (safe-parsing is a core invariant).

## Where to Look

| Question | File |
|---|---|
| Module implementation | `src/scientific.py` |
| Test patterns and expected behavior | `tests/test_scientific.py` |
| CI steps and Python version | `.github/workflows/ci.yml` |
| What is git-ignored | `.gitignore` |
