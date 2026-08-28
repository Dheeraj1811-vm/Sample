# AGENTS.md

## Project Snapshot

- Single-module Python project: `src/scientific.py` — dependency-free scientific helpers (constants, elementary functions, trig, statistics, numerical methods, unit conversions).
- Standard library only (`math`, `typing`). No packaging metadata, no `__init__.py` in `src/`.
- `python src/scientific.py` runs a built-in demo (`_demo()`).

## Toolchain and Verification

CI (`.github/workflows/ci.yml`, Python 3.11) is the source of truth for verification. Local equivalents:

| Check | Command |
|---|---|
| Lint | `ruff check src/` |
| Format | `ruff format --check src/` |
| Smoke | `python -c "import sys; sys.path.insert(0, 'src'); import scientific; print('ok')"` |

- Install ruff locally with `python -m pip install --upgrade pip ruff` (as CI does).
- No ruff config file exists; ruff default settings apply.
- No test suite exists; do not claim tests pass.

## Context Map

- `src/scientific.py` — the only code file. Public API is defined by `__all__`.
- `.github/workflows/ci.yml` — two jobs: `lint` (ruff check + format check) and `smoke` (module import). Triggers on push/PR to `main`.
- `src/` is not a package: import it via `sys.path` manipulation, not `pip install` or relative imports.

## Boundaries

- Never: add third-party dependencies; the module must stay standard-library only.
- Never: run `pip install` of this repo or add packaging metadata without an explicit request.
- Keep new code ruff-clean under default settings (`ruff check` + `ruff format`), or CI's `lint` job fails.

## Where to Look

- Module behavior and docstrings: `src/scientific.py`
- CI expectations: `.github/workflows/ci.yml`
