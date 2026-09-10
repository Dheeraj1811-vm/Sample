# AGENTS.md

Agent-facing guidance for working in this repository.

## Project snapshot

- **Module**: `src/scientific.py` — dependency-free Python scientific calculation library and CLI calculator.
- **Runtime**: Python 3.11+. Standard library only; no external runtime dependencies.
- **Public API**: all names in `__all__` in `src/scientific.py`.

## Toolchain and verification

| Task | Command |
|---|---|
| Lint | `ruff check src/` |
| Format check | `ruff format --check src/` |
| Run tests | `python3 -m unittest discover tests` |
| Run demo | `python src/scientific.py` |

CI config: `.github/workflows/ci.yml`.

## Testing conventions

- Framework: `unittest` (stdlib). No `pytest` or third-party test deps.
- Test file: `tests/test_scientific.py`.
- Tests import the module via `sys.path.insert(0, ...)` pointing at `src/` — no package install step.
- When adding a function, add a corresponding test case in `tests/test_scientific.py`.

## Code conventions

- Standard library imports only. Do not add third-party imports.
- All trigonometric functions use **degrees** (not radians) and are named `*_deg` to distinguish them from `math` equivalents.
- Functions raise `ValueError` for invalid input (wrong domain, wrong size, etc.) — no silent clamping.
- Use `math.fsum` for summations where numerical precision matters (see existing stat/linear regression code).

## File map

| Path | Purpose |
|---|---|
| `src/scientific.py` | All library code, expression evaluator, REPL, and CLI. Single file. |
| `tests/test_scientific.py` | Unit tests (unittest). |
| `.github/workflows/ci.yml` | CI: ruff lint + format check + import smoke test. |

## Boundaries

- Do not add external dependencies.
- Do not split `src/scientific.py` into a package without an explicit request; the module is intentionally a single file.
- Do not change the `*_deg` naming convention for trigonometric functions.
- New public functions must be added to `__all__` and get a test.

## Where to look next

- `src/scientific.py` — all code.
- `tests/test_scientific.py` — expected behavior for each function group.
- `.github/workflows/ci.yml` — what CI checks.
