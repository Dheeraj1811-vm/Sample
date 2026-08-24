# AGENTS.md

Guidance for coding agents working in this repository.

## Project Snapshot

- Single-module scientific calculator in pure Python: `src/scientific.py`.
- Standard library only (`math`, `collections`, `typing`). No third-party
  dependencies, no build system, no manifest (`pyproject.toml`), no CI
  workflows.

## Toolchain and Verification

- Run the test suite from the repo root:
  `python3 -m unittest discover tests`
- Run the module demo: `python3 src/scientific.py`
- `tests/test_scientific.py` prepends `src/` to `sys.path` and imports the
  module as `scientific` (not as a package) — preserve this import convention.

## Context Map

- `src/scientific.py` — public API is defined by `__all__`; sections:
  physical constants, elementary functions, trigonometry (degrees),
  statistics, numerical methods, unit conversions, `_demo()` under `__main__`.
- `tests/test_scientific.py` — `unittest` classes mirror the module sections
  (`TestElementary`, `TestTrigonometry`, `TestStatistics`,
  `TestNumericalMethods`, `TestConversions`, `TestConstants`).

## Boundaries

- Keep the module dependency-free (standard library only).
- Domain violations raise `ValueError` (e.g. `nth_root`, `log`, `mode`,
  `percentile`, `correlation`, `newton_root`) — follow this convention for
  new functions.
- Trigonometric functions take/return degrees (`*_deg` names), not radians.
- New public functions must be added to `__all__` and covered by tests.
