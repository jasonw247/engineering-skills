---
name: python-service-engineering
description: Implement or diagnose Python service resource lifetimes, asynchronous execution, concurrency, backpressure, cancellation, and validation boundaries. Use when those service behaviors are in scope; not for ordinary pure-Python edits or project packaging setup.
---

# Python service engineering

Start from the requested behavior or reported failure. Inspect the Python version, web or worker framework, ownership model, and existing tests before changing structure. Preserve public signatures and schemas unless asked to change them, and keep assessments read-only unless fixes are requested.

## Ownership and execution model

Trace the path from request or job admission through validation, domain work, external calls, and output. Identify what opens and closes every client, connection pool, model runtime, stream, and background task, separating per-request lifetimes from application or durable-job lifetimes.

Create shared clients and pools in the framework lifespan or a `contextlib.AsyncExitStack` so that if a second resource fails during startup, the first still closes cleanly. Keep per-request identity and database sessions out of module-level mutable state, and avoid opening network clients at import time.

Match execution to the workload: `await` native async I/O, run unavoidable blocking I/O through a bounded thread pool (`asyncio.to_thread` or a bounded executor), and isolate heavy CPU work in separate processes or native code that releases the GIL. Declaring a function `async def` does not make synchronous drivers cooperative.

## Backpressure, cancellation, and retries

Bound active calls, pending queue depth, and buffered outputs separately. Acquiring an `asyncio.Semaphore` inside spawned tasks caps active calls while still letting `create_task` or `gather` materialize unbounded tasks and arguments in memory; apply backpressure at admission with a bounded `asyncio.Queue(maxsize=...)` and fixed workers, or acquire capacity before advancing the upstream producer. Account for whether output itself streams incrementally or must be collected in memory for the caller.

Tie child tasks to an owner (`asyncio.TaskGroup` on Python 3.11+ or an explicitly tracked set) and stop owned work on error or client disconnect unless handing off to a separately owned durable job. Set deadlines at external boundaries, separate transient transport failures from permanent errors, and reconcile or deduplicate uncertain write outcomes before retrying so timeouts do not duplicate mutations.

Consult [lifecycle and concurrency diagnostics](references/lifecycle-and-concurrency.md) for memory growth, stalls, leaked streams, partial startup, or retry investigations.

## Boundary validation

Validate HTTP payloads, queue messages, tool arguments, and untrusted persisted records at the boundary with the project's runtime schema library (such as Pydantic, `msgspec`, or `cattrs`). Inside trusted domain code, use ordinary dataclasses, classes, or functions without re-parsing transport models or adding `Protocol` and factory layers for a single implementation.

## Asyncio and service pitfalls

- The event loop holds only weak references to tasks returned by `asyncio.create_task()`; unreferenced fire-and-forget tasks can be garbage-collected mid-`await`. Use `asyncio.TaskGroup` or hold strong references in a `set` with `task.add_done_callback(tasks.discard)`.
- `asyncio.CancelledError` inherits from `BaseException` rather than `Exception`. Catching `BaseException` or `CancelledError` without re-raising after cleanup breaks `asyncio.timeout()`, `TaskGroup`, and server shutdown.
- Cancelling `await asyncio.to_thread(...)` returns control to the caller immediately while the underlying OS thread and any dispatched remote write keep running until completion or socket timeout.
- Preserving input order across concurrent workers buffers fast completions behind a single slow early item; bound the total in-flight window rather than active workers alone.
- `TypedDict`, `dataclass`, `Annotated`, and `typing.cast` are erased or unchecked at runtime and do not validate untrusted inputs.

## Verification

Test the paths affected by the change (such as admission backpressure with workers held at an `asyncio.Event` barrier, partial-startup unwind, cancellation cleanup, malformed input, or retry deduplication) using deterministic barriers, fakes, and resource counters rather than `sleep` delays. Report the checks run and any unverified operational limits.

See [sources](references/sources.md) for provenance, scope notes, and standard-library references.
