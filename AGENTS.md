# AGENTS.md

## Project Snapshot

- **Purpose**: Dependency-free scientific calculation library (single module).
- **Stack**: Python 3.11, stdlib only (`math`, `collections`, `typing`).
- **Layout**: Flat module in `src/scientific.py`; tests in `tests/test_scientific.py` using `unittest`.
- **No packaging**: No `pyproject.toml`, `setup.py`, or `requirements.txt`. Tests add `src/` to `sys.path` directly.

## Toolchain and Verification

| Task | Command |
|------|---------|
| Run unit tests | `python3 -m unittest discover tests -v` |
| Lint | `ruff check src/` |
| Format check | `ruff format --check src/` |
| Run demo | `python src/scientific.py` |

CI (`.github/workflows/ci.yml`) runs `ruff check src/`, `ruff format --check src/`, and an import smoke check. There is no unit-test job in CI.

## Architecture / Context Map

- `src/scientific.py` — single module, ~560 lines. Sections: constants → elementary → trig → statistics → vectors → numerical methods → unit conversions → physics → demo (`_demo()`).
- `tests/test_scientific.py` — `unittest.TestCase` classes mirroring each section. Tests inject `src/` into `sys.path` at the top.
- All public symbols are listed in `__all__`.

## Boundaries

- **Always**: Keep `src/scientific.py` stdlib-only. Raise `ValueError` for invalid inputs (matches existing pattern).
- **Never**: Add external dependencies or a packaging configuration without explicit instruction.
- **Never**: Modify `.github/workflows/ci.yml` unless asked.

## Where to Look

| What | Where |
|------|-------|
| Public API surface | `__all__` in `src/scientific.py` |
| Error-handling pattern | `ValueError` raises in `src/scientific.py` |
| Test conventions | `tests/test_scientific.py` |
| CI pipeline | `.github/workflows/ci.yml` |
