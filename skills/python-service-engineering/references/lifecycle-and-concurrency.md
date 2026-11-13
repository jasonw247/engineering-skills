# Lifecycle and concurrency diagnostics

Read the rows matching the symptom under investigation.

| Symptom | Path to trace | Deterministic check |
| --- | --- | --- |
| Memory grows with input despite a semaphore | Source iterator, `create_task` fan-out, queue `maxsize`, ordered-result buffer, return-list contract | Hold workers at an `asyncio.Event` barrier and assert the source iterator and live task count stop advancing at the configured bound. |
| Concurrent requests stall each other | Synchronous SDK/disk calls in `async def`, GIL-bound CPU work, contended locks, exhausted connection pools | Block one slow operation on a fake barrier and verify a concurrent health/heartbeat coroutine completes immediately. |
| Work or sockets survive cancellation | Unowned `create_task`, swallowed `CancelledError`, orphan `to_thread` calls, unclosed async generators | Cancel a task suspended at a barrier; assert owned child tasks exit and streams/clients close once. |
| Partial startup leaks open clients | Lifespan setup order vs teardown coverage (`AsyncExitStack` vs manual `close()`) | Force resource #2's initializer to raise and assert resource #1 closes exactly once. |
| Duplicate writes after a timeout | Operation idempotency key, remote reconciliation, whole-workflow vs single-step retry | Simulate remote commit followed by a lost response; verify retry reconciles or deduplicates without a second side effect. |
| Client disconnect leaks upstream streams | Streaming response generator `aclose()`, request scope vs shared `AsyncClient` lifetime | Abort iteration partway through a response stream and verify the upstream stream closes while the shared client pool stays open. |

## Diagnostic notes

- **Deterministic concurrency tests:** Use `asyncio.Event`, `asyncio.Barrier`, fake transports, and peak in-flight counters instead of `asyncio.sleep` races. Use timeouts only as a fail-safe against hung tests.
- **`TaskGroup` failure semantics:** `asyncio.TaskGroup` cancels remaining children when any child raises an unhandled exception and wraps failures in `ExceptionGroup`. Keep that atomic cancellation when partial results are invalid; catch expected per-item exceptions inside the worker when siblings must finish independently.
- **Ordered-stream memory:** Returning results in input order requires holding completed items `(i + 1 .. i + W)` whenever item `i` is slow. Bound the total in-flight window `W` (queued + active + buffered out-of-order completions), not just active worker coroutines.
- **Blocking threads under cancellation:** Python cannot forcibly kill a running OS thread. Bound blocking operations with client/socket timeouts, pass a `threading.Event` where the callee polls for cancellation, and avoid claiming that task cancellation aborts an already-dispatched remote write.
- **Readiness vs liveness:** Keep downstream dependency failures out of liveness probes so transient outages stop traffic via readiness or admission policies (bounded wait, fast reject, or durable queue handoff) instead of triggering container restart loops.
