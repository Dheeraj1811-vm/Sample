# Sample

A dependency-free scientific calculation utility module. `src/scientific.py` provides physical constants, elementary functions, trigonometry, descriptive statistics, numerical methods, and unit conversions, using only the Python standard library.

## Requirements

- Python 3.11 (the version used by CI)
- No third-party dependencies

## Usage

Run the built-in demonstration:

```bash
python src/scientific.py
```

Import functions from your own code by adding `src/` to `sys.path`:

```python
import sys
sys.path.insert(0, "src")
from scientific import integrate, sin_deg, solve_quadratic
```

The module is not packaged for installation; it is imported directly from the repository.

## CI

GitHub Actions (`.github/workflows/ci.yml`) runs on pushes and pull requests to `main`, with two jobs:

- **lint** — `ruff check src/` and `ruff format --check src/`
- **smoke** — imports `scientific` and prints `ok`
