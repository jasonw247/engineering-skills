# Delivery

Repaired `enrich.py` without changing `enrich_all(items, fetch, limit=4)` or its ordered list result. A producer feeds a queue of capacity `limit`; a fixed set of `limit` workers calls `fetch`. Indexed list slots preserve input order even when later inputs finish first.

The bounds are separate: at most `limit` active fetches, `limit` queued items, one producer-held item awaiting admission, and `limit + 1` owned tasks. The output list grows with the number of inputs, as allowed by the API. Non-integer limits raise `TypeError`; zero and negative limits raise `ValueError` before input consumption.

On source failure, fetch failure, child cancellation, or caller cancellation, remaining owned work is cancelled and awaited before propagation. Shielded cleanup prevents repeated caller cancellation from interrupting asynchronous child cleanup. Ordinary failures remain their original exceptions rather than being wrapped in an exception group. The producer closes the consumed async iterator on exit when it provides `aclose`; `fetch` owns its external resources.

## Validation

Ran from `work/`:

```sh
~/.local/share/uv/python/cpython-3.12.11-macos-aarch64-none/bin/python3.12 -B -m unittest -v test_enrich
```

All **9 stdlib-only behavior tests passed** on Python 3.12.11. Cases cover empty input, out-of-order completion with ordered output, a 20,000-item stream, blocked-source cleanup on fetch failure, active-worker cleanup on source failure, repeated caller cancellation while cleanup is blocked, child cancellation, serial operation, and invalid limits. Each test checks for remaining tasks.

The large-stream test held workers at a barrier to verify that consumption stopped within `2 * limit + 1` items before releasing work. With limit 4, observed peaks were **4 active fetches** and **6 live tasks including the calling task** across 20,000 inputs. The bounded queue accounts for queued work; the source-consumption assertion checks backpressure rather than relying on throughput alone.

Artifacts: `enrich.py`, `test_enrich.py`, and this report. No framework or dependency was added or fetched. Validation used fake asynchronous operations, not live services. Cleanup assumes the source and fetch operations cooperate with cancellation; cancelling a task cannot guarantee that an independently running remote action has stopped. No deadline or retry policy was invented for this API.
