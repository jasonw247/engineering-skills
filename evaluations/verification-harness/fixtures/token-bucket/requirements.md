# Synthetic task: verification for a rate limiter

Coding agents edit `bucket.py` regularly. Twice this month an agent change
passed `test_bucket.py` and still broke refill: once tokens grew past
`capacity`, once a refill was lost when `take` was rejected. CI also reruns
`test_refill_after_wait` when it fails on a loaded runner.

Set up the checks agents should run before handing back a change to this
module. Keep the public `TokenBucket(capacity, refill_per_second)` constructor
and `take(count=1)` behavior unchanged for existing callers; an optional
argument that defaults to the current behavior is acceptable. Standard library
only; no network access.

Run the existing tests with `python3 -B -m unittest -v` from this directory.
