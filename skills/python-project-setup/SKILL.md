---
name: python-project-setup
description: Initialize, repair, or modernize Python packaging, dependency groups, lockfiles, and local/CI checks (`pyproject.toml`, `uv`, Poetry, Hatch, setuptools, Ruff, type checkers, pytest). Use when creating a Python package, fixing broken imports or wheel contents, or setting up project checks; not for routine Python code edits or unrequested tool migrations.
---

# Python project setup

Deliver an installable Python project whose package discovery, dependencies, and checks match its workload, verified from an isolated environment.

## Steps

1. **Inspect.** Identify the deliverable: published library, CLI, service, notebook/training repo, or workspace member. Read `pyproject.toml`, `setup.py`/`setup.cfg`, lockfiles (`uv.lock`, `poetry.lock`, `pdm.lock`, `requirements*.txt`), `.python-version`, CI workflows, and installed tool versions (`python3 -V`, `uv -V`, `pip -V`). Keep existing package managers, build backends, linters, type checkers, directory layout, and `requires-python` unless migrating them is the task.
2. **Configure.**
   - For new projects with no tool specified, use `pyproject.toml`, a `src/<package_name>/` layout with `__init__.py`, `uv` when installed (falling back to `python3 -m venv` and `pip` offline), `ruff` (`check` and `format`), one type checker (`mypy`, `pyright`, or `ty`), and `pytest`. Add a `[build-system]` table (`uv_build`, `hatchling`, or `setuptools>=77`) whenever the project builds a wheel, exposes `[project.scripts]`, or must be imported as a package.
   - Separate runtime dependencies (`[project.dependencies]`), user-facing extras (`[project.optional-dependencies]`), and developer tools (`[dependency-groups]` per PEP 735, such as `dev`). For libraries, use compatible lower bounds in `[project.dependencies]` and pin exact versions only in the lockfile. Regenerate lockfiles with the manager's resolver rather than editing them by hand.
   - For C/CUDA extensions, conflicting training vs serving pins, or multi-package workspaces, read [workload choices](references/workload-choices.md).
3. **Verify installation.** Install into an isolated environment (`--offline` / `--no-build-isolation` when network access is unavailable and build backends are local). For libraries and CLIs, build the wheel when build tools are present, inspect its archive entries (`python3 -m zipfile -l dist/*.whl`), and import the public module or invoke the CLI entry point from a directory outside the repository checkout so the working directory cannot mask missing package files.
4. **Run checks and report.** Run the configured formatter, linter, type checker, and behavioral tests. Report the changed files, exact commands and results, and any checks skipped because a tool or package index was unavailable.

## Packaging traps local runs miss

- `python -m pytest` and interactive `python` prepend `""` (the current working directory) to `sys.path`, even when `--import-mode=importlib` is set. In a flat layout, tests run from the repository root can import the local source folder while a broken wheel goes unnoticed. Use a `src/<package_name>/` layout and invoke the environment's `pytest` console script against the installed package, or verify imports after changing out of the checkout directory.
- `setuptools` flat-layout auto-discovery excludes common names such as `tests`, `docs`, `scripts`, and `benchmarks`, yet fails with `Multiple top-level packages discovered` (or ships unintended directories in the wheel) once folders like `notebooks/`, `migrations/`, `datasets/`, or `configs/` sit at the repository root. Use `src/<package_name>/` or set `[tool.setuptools.packages.find]` (`include = ["<package_name>*"]`).
- Downstream type checkers ignore a library's inline type annotations unless an empty `py.typed` marker ships inside the package directory (PEP 561). Data files (`.sql`, `.json`, templates) also drop out of wheels unless covered by the build backend's VCS or package-data rules; confirm with `python3 -m zipfile -l`.
- `setuptools>=77`, `hatchling>=1.27`, and `uv_build` support PEP 639 SPDX strings (`license = "MIT"`, `license-files = ["LICENSE*"]`) and warn or fail if SPDX `license` strings are mixed with legacy `License ::` trove classifiers or `{ text = "..." }` tables.
- Without an accurate `requires-python` in `[project]`, Ruff (`UP` rules) and type checkers allow newer syntax (`X | Y` below 3.10, `Self` below 3.11, `type` aliases below 3.12) that fails at import time on older supported interpreters.
- Listing `pytest`, `ruff`, or `mypy` under `[project.dependencies]` forces every downstream consumer to install them; keep development tools in `[dependency-groups]`.
- Skip unrequested scaffolding such as web frameworks, settings libraries, telemetry SDKs, `domain/`/`adapters/` folder trees, or coverage-percentage gates when a single package and plain functions meet the requirements.

See [sources](references/sources.md) for provenance, scope, and packaging specifications.
