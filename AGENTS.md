# AGENTS.md

## Purpose
Guidance for coding agents working in this repository.

## Project Snapshot
- **What**: Dependency-free Python scientific utilities module
- **Stack**: Python 3.9+ standard library only (`math`, `typing`)
- **Entry point**: `src/scientific.py` (also runnable as `python src/scientific.py` for a demo)

## Toolchain and Verification
| Action | Command |
|---|---|
| Run tests | `python3 -m unittest discover tests` |
| Run demo | `python src/scientific.py` |

No external dependencies, linters, formatters, or type checkers are configured.

## Architecture
- `src/scientific.py` — single module, all public symbols in `__all__` (28 symbols)
- `tests/test_scientific.py` — unittest suite with `unittest.TestCase` classes
- Public API categories: constants (7), elementary (7), trig (3), statistics (4), numerical (4), conversions (3)

## Boundaries
- **Always**: Use `ValueError` for input validation (follow existing pattern in `src/scientific.py`)
- **Never**: Add external dependencies — project is intentionally stdlib-only
- **Never**: Modify `.gitignore` without understanding the build environment

## Where to Look
- `src/scientific.py` — main source, self-documented with docstrings and type hints
- `tests/test_scientific.py` — test coverage reference; shows expected behavior and edge cases
