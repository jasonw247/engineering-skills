# Synthetic task: batch timeouts

The completed change adds `build_timeouts(entries, audit)` to `loader.py`.
`original_loader.py` is the task base; the rest of `loader.py` belongs to another
contributor. Only the new function and its imports are task-owned.

For each `(name, raw)` entry, convert raw to text exactly once. Accept canonical
nonnegative integers followed by `ms` or `s`, without trimming whitespace,
leading zeroes, fractions, or signs. Return integer milliseconds as an ordered
list of `(name, milliseconds)`, preserving duplicate names. An invalid value
raises `durations.DurationError` with `invalid timeout: {text!r}`.

Append each successfully parsed entry to the supplied audit immediately, before
consuming the next entry. Stop at the first error; retain earlier audit entries
and never consume later entries. Propagate iterator, conversion, and audit errors
unchanged. Empty input returns an empty list without touching the audit.

Neighboring duration facilities have other supported direct callers. Preserve
all existing contracts. `durations.py`, `original_loader.py`, `test_loader.py`,
and this request are read-only. Do not change `describe_metadata`.

Run the supplied tests with `python3 -B -m unittest -v` from this directory.
