# Assessment of the concurrency claim

The claim in `example-semantics.md:3` is materially incorrect: the example creates 12 worker tasks, while the semaphore limits concurrent execution inside the guarded block to two. The fixture supports bounded active work within that block, but contradicts the claimed bound on task creation.

## Scope and verification

This assessment covers the complete supplied document, static inspection of its code, and one execution of its unchanged Python code block. Review followed the supplied technical-document-review skill and its technical-evidence guidance. No external sources or services were used. The source document and embedded implementation were left unchanged; this is an assessment, not an implementation revision.

The code block was extracted verbatim into a temporary directory within the workspace and run with Python 3.9.6. It exited with status 0, produced no stderr, and printed:

```json
{"peak_active": 2, "created_tasks": 12, "results": 12}
```

The temporary fixture was removed. A byte comparison confirmed that the source remained unchanged after execution.

## Material finding: the semaphore does not bound task creation

**Location:** the claim at line 3; task creation and measurement at lines 24–27; semaphore acquisition and active-work measurement at lines 17–21.

The list comprehension calls `asyncio.create_task(fetch(item))` once for every item in `range(12)`. It contains no suspension point and finishes creating all 12 tasks before `measure()` awaits `gather`. The semaphore is acquired inside each task, so it controls entry to the guarded block after task creation. Waiting tasks still exist.

The executed fixture reported 12 explicitly created worker tasks, a peak of two workers inside the guarded block, and 12 returned results. `created_tasks` counts the tasks in the list; it is not a count of every task managed by the event loop. `peak_active` measures overlapping guarded sections, including their `sleep(0)` suspension, rather than simultaneous CPU execution.

**Reader impact:** the current wording could lead readers to assume that a semaphore also limits task allocation or provides bounded admission for arbitrarily large inputs. In this pattern, replacing the 12-item range with a larger finite input still creates one worker task per item. The task list and collected results also grow with input size; this fixture does not measure memory usage.

**Proposed correction to the prose, preserving the implementation:**

> This example creates one worker task for each of its 12 inputs. The semaphore limits concurrent work inside the guarded block to two. In the executed fixture, the reported peak active count was two, 12 worker tasks were created, and 12 results were returned. Task creation is not bounded by the semaphore.

If a fixed bound on created tasks is a requirement, that calls for a separate implementation change, such as a fixed worker pool with bounded admission. No such change was made or evaluated here.

## What the evidence establishes

The execution observations apply to this local, successful 12-item fixture. Static inspection explains why the same guarded block admits at most two workers when they share this semaphore, and why the task-creation loop scales with the number of inputs. These are distinct forms of support; one execution alone does not prove behavior for all inputs or deployments.

The example performs no network requests and uses `asyncio.sleep(0)` as its suspended work. It establishes no production throughput, latency, memory ceiling, behavior under failures or cancellation, or global limit across separate semaphore instances, processes, or replicas. Any deployment claim would need evidence for the actual operation and coordination scope. Those properties remain untested here.
