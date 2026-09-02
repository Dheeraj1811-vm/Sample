# Sample

## What it is

A dependency-free collection of scientific helpers — elementary functions, trigonometry, statistics, vector algebra, numerical methods, unit conversions, physical constants, and physics formulas — that also runs as a command-line calculator.

## Requirements

- Python 3.11 (standard library only; no third-party dependencies)
- No packaging manifest — there is nothing to `pip install`. Run the script directly.

## Usage

### Command-line

```
python src/scientific.py <subcommand> [args]
```

Subcommand names use hyphens (e.g. `std-dev`, `sin-deg`, `nth-root`, `solve-quadratic`). A `--json` flag is available on most subcommands. Running with no arguments prints a short demonstration.

Examples:

```bash
# Show help
python src/scientific.py --help

# Arithmetic mean
python src/scientific.py mean 2.5 3.1 4.8

# Standard deviation (population)
python src/scientific.py std-dev 2 4 4 4 5 5 7 9 --population

# Logarithm (base 2)
python src/scientific.py log 1024 --base 2

# Dot product of two vectors
python src/scientific.py dot 1,2,3 4,5,6

# Photon energy from wavelength (JSON output)
python src/scientific.py photon-energy 500e-9 --json

# Evaluate a free-form expression (safe parser; Python eval() is never called)
python src/scientific.py eval "2 * sin_deg(30) + log(100, 10)"

# Interactive calculator
python src/scientific.py repl
```

### As a library

```python
import sys
sys.path.insert(0, "src")
import scientific as sci

sci.mean([2.5, 3.1, 4.8])
sci.sin_deg(30)
sci.dot([1, 2, 3], [4, 5, 6])
sci.photon_energy(500e-9)
```

## Project layout

| Path | Description |
|------|-------------|
| `src/scientific.py` | The module (library + CLI) |
| `tests/test_scientific.py` | Unit tests (stdlib `unittest`) |
| `.github/workflows/ci.yml` | CI (ruff lint + format check + import smoke test) |

## Testing

From the project root:

```bash
python3 -m unittest discover tests
```

## Development (lint & format)

Enforced by CI on push/PR to `main`:

```bash
ruff check src/
ruff format --check src/
```
