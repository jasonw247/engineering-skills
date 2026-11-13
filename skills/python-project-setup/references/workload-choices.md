# Workload choices

## Native runtimes, accelerators, and workspaces

Share one environment and lockfile only when components resolve cleanly together across every target OS and architecture. Training stacks (CUDA/ROCm wheels, `torch`, custom C++ ops) and lean serving APIs often carry conflicting transitive pins (`numpy`, `protobuf`, `typing-extensions`) or gigabyte wheels unneeded in production containers.

- Test resolution (`uv lock`, `poetry lock`) on the declared platform markers before promising a single shared workspace lock. Note that `uv` workspaces share a single `uv.lock` across all workspace members; components with incompatible native pins need separate top-level projects and lockfiles.
- Scope custom package indexes (such as PyTorch CUDA wheel indexes) explicitly to the packages that come from them (`[tool.uv.sources]` with `explicit = true` on the index, or manager equivalent). Adding an unscoped `--extra-index-url` lets an external index shadow public PyPI package names and pull unintended builds.
- Record supported OS, CPU/GPU architecture, and Python version bounds in `pyproject.toml` markers rather than prose alone.

## Configuration and package layout

- **Libraries:** expose a small documented API in `__init__.py` (or explicit submodules), avoid reading environment variables or opening files at import time, and check wheel + sdist contents when publishing.
- **CLIs:** wire commands through `[project.scripts]` (`name = "pkg.cli:main"`) instead of committed `bin/` wrapper scripts, and test `--help` and non-zero exit behavior on the installed entry point.
- **Services:** parse and validate environment configuration once at startup rather than reading `os.environ` deep inside request handlers. Keep plain dataclasses for internal domain values when external parsing is already handled at the boundary.
- **Notebooks and research:** extract reusable transforms and data schemas into an importable local package under `src/` so notebooks call tested functions instead of copying cells. Apply strict lint/type rules to `src/` while relaxing notebook-incompatible rules on `*.ipynb` if notebooks are checked in.

## Scaling checks to the deliverable

- **Interpreter matrix:** run CI across the lowest and highest supported minor Python versions for libraries; pin a single deployment minor version for services and internal apps.
- **Property-based testing (`hypothesis`):** add for parsers, serializers, numeric bounds, and stateful transitions where edge cases hide between hand-picked examples.

Keep `requires-python` unchanged on existing repositories unless raising the minimum version is explicitly authorized.
