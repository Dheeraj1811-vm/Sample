# AGENTS.md

## Project Snapshot

- Single-module Python library: `src/scientific.py`
- Dependency-free; standard library only
- Python 3.11+
- No packaging manifest (`pyproject.toml`, `setup.py`, etc.)

## Toolchain

| Task | Command |
|---|---|
| Run demo | `python src/scientific.py` |
| Run tests | `python3 -m unittest discover tests` |
| Lint | `ruff check src/` |
| Format check | `ruff format --check src/` |
| Format | `ruff format src/` |

## Architecture

- **`src/scientific.py`** — the entire library; one flat module, no sub-packages. Import via `sys.path.insert(0, "src")` or add `src/` to `PYTHONPATH`.
- **`tests/test_scientific.py`** — `unittest` suite; mirrors the module's section layout (elementary, trig, statistics, vectors, numerical, conversions, constants, physics).
- **`.github/workflows/ci.yml`** — runs `ruff check` + `ruff format --check` on `src/` and a smoke import on `main`.

## Boundaries

- Always: add new functions to `__all__` in `src/scientific.py`.
- Always: add corresponding test coverage in `tests/test_scientific.py` matching the existing section pattern.
- Always: use `math.fsum` for summation loops to avoid floating-point accumulation drift.
- Never: introduce external dependencies.
- Never: split the module into a package without an explicit decision; the single-file layout is intentional.
