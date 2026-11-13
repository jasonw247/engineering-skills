# Source provenance

Written locally on 2026-10-12 and tightened on 2026-11-12.

## Scope notes

- FastAPI and Pydantic are treated as optional examples alongside other Python web and validation libraries.
- Separation of active concurrency, task creation, queued input, ordered-result buffering, and return-list accumulation reflects a 2026-10-12 local refinement.
- Standard-library `asyncio` semantics (`create_task` weak references, `CancelledError` inheriting from `BaseException` since Python 3.8, `TaskGroup` and `timeout` in Python 3.11+, `AsyncExitStack` unwind) were verified against Python 3.11–3.13 documentation on 2026-11-12. Check installed framework and SDK versions directly before relying on third-party dispatch details.

## Related documentation

- **Tasks, cancellation, and threads:** Python [`asyncio` Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html) and [`asyncio` Exceptions](https://docs.python.org/3/library/asyncio-exceptions.html).
- **Queues and resource lifetimes:** Python [`asyncio` Queues](https://docs.python.org/3/library/asyncio-queue.html), [`contextlib.AsyncExitStack`](https://docs.python.org/3/library/contextlib.html#contextlib.AsyncExitStack), and framework lifespan hooks such as [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
- **Runtime validation:** Python [`typing`](https://docs.python.org/3/library/typing.html) and [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) do not validate payloads at runtime; boundary validators include [Pydantic](https://docs.pydantic.dev/latest/), [msgspec](https://msgspec.dev/), and [cattrs](https://catt.rs/).
