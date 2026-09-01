# AGENTS.md

Durable guidance for coding agents working in this repo. `README.md` covers usage; this file covers how to work safely here.

## Project snapshot

- Single-module, dependency-free Python scientific library + CLI. All code lives in `src/scientific.py` (module name `scientific`).
- Standard library only. There are no packaging files (`pyproject.toml`, `setup.py`, `requirements*.txt` are absent by design).
- Python 3.11 per `.github/workflows/ci.yml`.

## Layout

- `src/scientific.py` — the entire library and CLI. Public API is the `__all__` list.
- `tests/test_scientific.py` — `unittest` suite (not pytest). It inserts `src/` onto `sys.path` itself.
- `.github/workflows/ci.yml` — lint + smoke jobs (see Commands).

## Commands

- Tests: `python -m unittest discover -s tests`
- Lint: `ruff check src/` · Format check: `ruff format --check src/` · Apply format: `ruff format src/`
- Demo / CLI: `python src/scientific.py` · `python src/scientific.py --help`
- Import check (as CI does): `python -c "import sys; sys.path.insert(0, 'src'); import scientific"`

## How the CLI works

- `main(argv)` builds argparse subparsers in `_build_parser`.
- Most commands come from the `_COMMANDS` dict: `name -> _Command(call, help, arguments, options)`. To add a CLI command, add a `_COMMANDS` entry that wraps an existing function.
- `demo` and `constants` are hardwired in `_build_parser` (not in `_COMMANDS`). `constants` is derived from `__all__` (uppercase names) via `_CONSTANTS`.
- Callable-based functions (`derivative`, `integrate`, `find_root`, `newton_root`) are intentionally **library-only** — there is no expression parser. Do not wire them into the CLI without one.
- `--json` is a shared option; results are rendered by `_format_value` / `_jsonable`.

## Conventions

- Keep the module stdlib-only. Add any new public function to `__all__`.
- Public functions raise `ValueError` for invalid input (domain errors); the CLI converts `ValueError` / `OverflowError` / `ZeroDivisionError` into `exit 1` with a message on stderr.
- Add or extend `unittest` cases in `tests/test_scientific.py` alongside new features (the suite is organized into `TestCase` classes per area).

## Boundaries

- **Always**: keep `src/scientific.py` stdlib-only and register new public functions in `__all__`.
- **Ask first**: adding dependencies or packaging, or exposing callable-based functions on the CLI (needs an expression parser).

## Where to look next

- `src/scientific.py`: `__all__`, `_COMMANDS`, `_build_parser`, `main`, `_demo`.
- `tests/test_scientific.py`: `TestCase` classes `TestElementary` … `TestCLI`.
- `.github/workflows/ci.yml`: what CI enforces.
