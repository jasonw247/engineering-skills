# Assessment of the concurrency claim

The claim in `example-semantics.md:3` is materially incorrect: the example creates 12 worker tasks while limiting concurrent execution inside the semaphore-protected section to two. The document needs a claim correction; the implementation was left unchanged.

## Scope and verification

Applied the supplied technical-document-review skill in **Assess** mode. Read the complete input and performed a focused review of its reasoning, measurement boundaries, and executable example. Verification used only the supplied local material and one execution of the exact Python code block, copied without changes into a temporary directory within the workspace. No external sources or services were consulted.

The fixture ran under Python 3.9.6, exited with status 0, and produced no stderr. Its stdout was:

```json
{"peak_active": 2, "created_tasks": 12, "results": 12}
```

The temporary directory was removed. The input's bytes were verified unchanged after execution; its SHA-256 was `efb2f78b017c86c5ae84401e75bd153171b0dc916eb4b6d494947f226f1243e1`.

## Findings

### 1. High priority: the semaphore does not bound task creation

**Location:** Claim at line 3; task creation and counting at lines 24–25; semaphore acquisition at line 17.

The list comprehension calls `asyncio.create_task(fetch(item))` once for each of the 12 inputs. The semaphore is acquired inside `fetch`, after its task has been created. Waiting for a semaphore permit therefore does not prevent task creation. The executed fixture directly contradicts “creates at most two worker tasks”: `created_tasks` is 12.

By inspection, replacing the input with N items would create N worker tasks through this comprehension, assuming successful creation. This is a code-based inference, not a measured input-size sweep. The metric counts the worker tasks in `tasks`; it is not a count of every task managed by the event loop.

**Reader impact:** Readers could mistake a limit on simultaneous guarded operations for a limit on task admission or resource use. The task list and gathered results retain one entry per input, so this example also does not establish constant memory use as input size grows. Memory was not measured.

**Correction:** State that task creation scales with the number of inputs and that the semaphore limits entry into the guarded section. If bounded task creation is an actual requirement, it needs a different admission or worker arrangement; implementing that change is outside this assessment.

### 2. Medium priority: define “active work” and limit the evidence claim

**Location:** “This proves … active work” at line 3; instrumentation at lines 17–21 and result reporting at line 27.

`active` measures overlapping occupancy of the semaphore-protected section, including time suspended at `asyncio.sleep(0)`. It does not measure simultaneous CPU execution, total live tasks, or work outside that section. The fixture contains no external operations.

**Reader impact:** The broad wording can be read as a guarantee about all work or deployment behavior. The observed peak of two establishes the fixture's measured peak for this run. Separately, the code supports a structural upper bound of two occupants of this guarded section while all such work uses this shared semaphore as shown. A maximum of two does not require every run or workload to reach two.

**Correction:** Name the guarded section as the measurement boundary. Do not extend this result to throughput, latency, memory bounds, real service concurrency, or behavior under failure and cancellation; those were not tested here.

## Suggested replacement for line 3

> This implementation creates one worker task per input: 12 tasks in this example. A shared semaphore with a limit of two allows at most two `fetch` calls to occupy the guarded section at once. In the locally executed fixture, the measured peak occupancy was two and all 12 results were returned. The semaphore does not bound task creation or establish bounded memory use.

This wording separates the executed fixture observations from the general behavior inferred from the code. No deployment-level validation was performed.
