# AGENTS.md

## Project Snapshot

- Single-module Python project: `src/scientific.py`
- No external dependencies; no packaging config (no `pyproject.toml`)
- Python 3.11+
- Acts as both a library and a CLI calculator

## Toolchain and Verification

```bash
# Tests
python3 -m unittest discover tests

# Lint (CI runs on src/ only)
ruff check src/

# Format check
ruff format --check src/

# Smoke import
python -c "import sys; sys.path.insert(0, 'src'); import scientific"
```

CI config: `.github/workflows/ci.yml` (ruff lint + format + smoke import, Python 3.11).

## Architecture / Context Map

| Path | Role |
|---|---|
| `src/scientific.py` | The entire library + CLI. All public symbols in `__all__`. |
| `tests/test_scientific.py` | Unit tests (`unittest`). Adds `src/` to `sys.path` at import time. |
| `.github/workflows/ci.yml` | CI: ruff lint, ruff format check, smoke import. |

### Non-obvious details

- The CLI is defined in `_COMMANDS` (a dict of `_Command` dataclasses) near the bottom of `src/scientific.py`.
- The expression evaluator uses a custom tokenizer/parser (`_tokenize`, `_Parser`) — no `eval()` call.
- `evaluate()` accepts a `variables` dict for assignment (`x = 3`) and cross-call state.
- `repl()` accepts a `lines` parameter for testable input; `None` means interactive.
- The test file does `sys.path.insert(0, ...)` manually; there is no install step.

## Boundaries

- **Never** add external dependencies without updating CI and the README.
- **Never** use `eval()`/`exec()` in the expression evaluator.
- All new public functions must be added to `__all__` in `src/scientific.py`.
- Lint and format with ruff before committing; CI checks `src/` only.

## Where to Look

- Public API: `__all__` at the top of `src/scientific.py`
- CLI subcommand definitions: `_COMMANDS` dict in `src/scientific.py`
- Expression grammar: `_Parser` class docstring in `src/scientific.py`
- Test patterns: `tests/test_scientific.py`
