# Source provenance

Written locally on 2026-10-12; revised on 2026-11-12 for concrete packaging defaults and build traps. Packaging, dependency separation, isolated install validation, and explicit construction follow the PyPA specifications listed below. `uv`, `ruff`, and `src/` layout are new-project defaults when no project toolchain exists; existing repository tooling stays authoritative. Deliberately excluded: service dependencies, a fixed Python 3.14 target, fixed type strictness, coverage thresholds, and mandatory property-testing tools.

## Limits

Check installed tool versions (`python3 -V`, `uv -V`, `pip -V`, and the configured build backend) in the target environment before relying on version-sensitive flags or metadata keys. Behavioral acceptance fixtures and results live outside the deployable skill.

## Related documentation

- **Layout and import isolation:** [PyPA Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/), [PyPA `src` layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/), [setuptools package discovery](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html), and [pytest import modes and `sys.path`](https://docs.pytest.org/en/stable/explanation/pythonpath.html).
- **Build and metadata standards:** [PEP 517](https://peps.python.org/pep-0517/) and [PEP 518](https://peps.python.org/pep-0518/) (`[build-system]`), [PEP 561](https://peps.python.org/pep-0561/) (`py.typed`), [PEP 621](https://peps.python.org/pep-0621/) (`[project]`), [PEP 639](https://peps.python.org/pep-0639/) (SPDX `license` expressions and deprecation of `License ::` classifiers in `setuptools>=77`, `hatchling>=1.27`, and `uv_build`), and [PEP 735](https://peps.python.org/pep-0735/) (`[dependency-groups]`).
- **New-project tool defaults:** [`uv` projects](https://docs.astral.sh/uv/concepts/projects/) and [`ruff` configuration](https://docs.astral.sh/ruff/configuration/).
