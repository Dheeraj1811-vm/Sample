# AGENTS.md

## Project Snapshot

Dependency-free Python scientific calculation library. Single source module (`src/scientific.py`) with a built-in expression evaluator, CLI, and REPL. No package install step; import via `sys.path`.

## Toolchain and Verification

```bash
# Run tests (stdlib unittest, no pytest)
python3 -m unittest discover tests -v

# Lint
ruff check src/

# Format check
ruff format --check src/

# Smoke test (used by CI)
python -c "import sys; sys.path.insert(0, 'src'); import scientific; print('ok')"
```

CI config: `.github/workflows/ci.yml` — runs ruff lint + format check and a smoke import on Python 3.11.

## Architecture / Context Map

| Path | Purpose |
|------|---------|
| `src/scientific.py` | Entire library: math functions, expression evaluator, CLI (`main()`), REPL (`repl()`) |
| `tests/test_scientific.py` | All tests (stdlib `unittest`, 11 classes, 131 methods) |
| `.github/workflows/ci.yml` | CI: ruff lint, ruff format check, smoke import |

Key internal symbols (all in `src/scientific.py`):

- `__all__` — public API; every name here is reachable from the CLI
- `_NAMESPACE` — shared name table for the expression evaluator
- `_DEFERRED_FIRST_ARGUMENT` — functions whose first arg is a lambda expression (`derivative`, `integrate`, `find_root`, `newton_root`)
- `_COMMANDS` — CLI subcommand registry
- `main(argv)` — CLI entry point; `repl(lines)` — REPL entry point; `evaluate(expr, variables)` — expression evaluator

## Boundaries

- **Never** introduce a third-party dependency. The module must remain importable with only the standard library.
- **Never** use `eval()` or `exec()` for expression evaluation. The parser (`_Parser`) is the only code path.
- Public API changes: update `__all__`, the CLI (`_COMMANDS`), and the `_NAMESPACE`-exposing tests in `tests/test_scientific.py` (`test_every_public_function_is_reachable_from_the_cli`).
- Tests must remain stdlib `unittest` (no pytest). New tests go in `tests/test_scientific.py`.

## Where to Look

- `src/scientific.py` — all logic, read top-to-bottom: constants → math → stats → vectors → numerical → conversions → physics → demo → evaluator → CLI → REPL
- `tests/test_scientific.py` — class per subsystem; `TestCLI` and `TestRepl` test the I/O layer
- `.github/workflows/ci.yml` — exact CI commands
