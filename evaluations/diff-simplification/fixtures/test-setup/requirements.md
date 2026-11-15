# Synthetic task: retry regression tests

The completed change adds `test_retry.py`; `original_test_retry.py` is the task
base. Simplify only the newly added test file. `retry.py`, `support.py`, the base,
and this request are read-only. All behavior is local and deterministic.

Preserve these independent scenarios, each with a diagnostic identifying it:
- immediate success, including empty payload;
- retry after 429, with a delay of one;
- retry after two 503 responses, with delays of one then two;
- exhaustion after three retryable responses;
- immediate rejection of a 400 response without a retry;
- cancellation during the retry delay, with the transport still closed;
- invalid attempt count, rejected before the transport is used or closed.

Check return values or exact errors, receive counts, delays, closure, and event
ordering as applicable. Each scenario starts with fresh fake state. A failure in
one scenario must not prevent the others from being exercised. Retain the
cancellation resource boundary and direct-call validation coverage even when
those tests need different assertions from the successful cases.

Run the tests with `python3 -B -m unittest -v test_retry` from this directory.
