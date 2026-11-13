# Assessment of the bounded concurrency claim

The claim is **partly false**: the semaphore bounds concurrent execution inside its protected section to two, but it does not bound worker task creation to two. The example creates 12 worker tasks. For an input of size N, the same pattern creates N worker tasks, assuming creation succeeds.

## Executed fixture observations

I extracted the Python block from `example-semantics.md` without modifying its code and ran it once with Python 3.9.6 in a temporary directory inside the workspace. The process exited with status 0, produced no stderr, and printed:

```json
{"peak_active": 2, "created_tasks": 12, "results": 12}
```

These measurements have specific meanings:

- `created_tasks` is the length of the list populated by 12 calls to `asyncio.create_task`. It counts worker tasks created, not just tasks holding a semaphore permit. It excludes other tasks, such as the task running `measure()`.
- `peak_active` measures the maximum number of workers between the counter increment and decrement inside `async with gate`. The observed peak was two.
- `results` is the length of the list returned by `gather`, showing that this run collected 12 results. It is not a measure of concurrency.

The temporary directory was removed. The input, including its embedded implementation, remained byte-for-byte unchanged. Its SHA-256 before and after execution was `efb2f78b017c86c5ae84401e75bd153171b0dc916eb4b6d494947f226f1243e1`.

## Why the bounds differ

The list comprehension calls `asyncio.create_task(fetch(item))` for every item. There is no semaphore acquisition or suspension in that creation loop. The semaphore is acquired later, inside each worker coroutine. A worker waiting for a permit is already a created task.

The semaphore starts with two permits, and the context manager releases a permit on exit. In this implementation, at most two workers can occupy the protected section at once. The `await asyncio.sleep(0)` yields while each worker holds its permit, allowing the fixture to exercise overlapping occupancy. It performs no external operation.

Consequently, the worker task count and the retained task/result collections grow with input size. Limiting occupancy of the protected section does not establish a constant bound on task allocation or total memory use.

## Scope of the conclusion

The execution confirms the fixture's reported counts for one local run. The code structure independently explains why task creation scales with input size and why this semaphore limits its protected section to two occupants.

This does not prove that a deployment has at most two tasks or two operations globally. Each invocation of `measure()` creates its own semaphore; concurrent invocations would have independent limits. Work outside the protected section or work launched separately is not covered by this gate. The fixture also establishes no bounds on real service requests, connections, throughput, latency, or deployment memory use.

A supported replacement claim is: **“This example creates one worker task per input item and limits concurrent execution inside the semaphore-protected section to two; the 12-item fixture reports 12 created worker tasks and a peak occupancy of two.”** No implementation change is needed to state that narrower claim accurately.
