# Delivery

Created an installable `range_tools` library in `range-tools/`, supporting Python 3.9+ with no runtime dependencies. Its public `clip(value, lower, upper)` returns the appropriate bound outside an interval, returns the value within it, and raises `ValueError` for an inverted interval. Ordinary integer and finite float inputs are covered.

The small `src/` package uses `pyproject.toml` with the installed setuptools build backend. Metadata and package discovery use `setup.cfg`, which works with installed setuptools 58.0.4; this avoids requiring an offline-unavailable backend upgrade for newer metadata features. Ruff and mypy are configured as optional development tools. Behavioral tests use unittest. No service framework, runtime dependency, global installation, or dependency fetch was introduced.

## Commands and results

From `work/`:

```sh
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip wheel --no-index --no-deps --no-build-isolation --wheel-dir dist ./range-tools
.venv/bin/python -m pip install --no-index --no-deps dist/range_tools-0.1.0-py3-none-any.whl
```

All succeeded with Python 3.9.6, pip 21.2.4, setuptools 58.0.4, and wheel 0.37.0. The venv inherited installed build tooling but the library was installed only into the venv. The wheel was inspected using `zipfile.ZipFile`: it contains `range_tools/__init__.py`, `range_tools/py.typed`, and distribution metadata declaring Python >=3.9. All `Requires-Dist` entries apply only to the optional `dev` extra.

From `work/outside-checkout/`, which is outside the package checkout:

```sh
../.venv/bin/python -I -
../.venv/bin/python -I -m unittest discover -s ../range-tools/tests -v
```

The first command received an inline script importing `range_tools` and `clip`, asserting that `range_tools.__file__` is beneath `.venv`, and asserting `clip(12, 0, 10) == 10`. It resolved to `.venv/lib/python3.9/site-packages/range_tools/__init__.py`. Isolated mode excluded the working directory and `PYTHONPATH` from import resolution. All **5 tests passed** against the installed wheel: integer boundaries, finite-float boundaries, mixed integer/float inputs, equal bounds, and inverted bounds.

From `work/range-tools/`, attempted:

```sh
../.venv/bin/python -m ruff format --check .
../.venv/bin/python -m ruff check .
../.venv/bin/python -m mypy
```

These checks could not run because Ruff and mypy are not installed; Python reported `No module named ruff` and `No module named mypy`. They are configured, not claimed as passed. The offline constraint prevented fetching them. Other interpreter versions were not tested; no cross-version test matrix is claimed.

## Artifacts

- `range-tools/`: source package, packaging metadata, README, configured development checks, and `tests/test_clip.py`.
- `dist/range_tools-0.1.0-py3-none-any.whl`: built and installed distribution.
- `.venv/`: isolated verification environment.
- `outside-checkout/`: working directory used for external import and installed-package tests.
- `delivery.md`: this report.

Wheel SHA-256: `abb994fd2183fcacdf757185ca839337ecb637f5066fc3bd895b6b3647eaa94b`.
