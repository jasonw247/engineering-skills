# range_tools

A Python 3.9+ library with no runtime dependencies.

```python
from range_tools import clip

clip(12, 0, 10)  # 10
clip(0.5, 0, 1)  # 0.5
```

`clip(value, lower, upper)` accepts ordinary integers and finite floats. It
returns the lower bound below the interval, the upper bound above it, and the
original value otherwise. An inverted interval raises `ValueError`.

Packaging uses the locally available setuptools backend. Metadata lives in
`setup.cfg` for compatibility with setuptools 58; `pyproject.toml` selects the
backend and configures development checks. The optional `dev` extra provides
Ruff for formatting/lint and mypy for static typing. Behavioral tests use the
standard library's unittest runner.

From this project directory, with the package installed:

```sh
python -m unittest discover -s tests -v
python -m ruff format --check .
python -m ruff check .
python -m mypy
```
