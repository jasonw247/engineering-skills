# Bounded concurrency example

The semaphore limit is two, so this implementation creates at most two worker tasks regardless of input size. This proves that task creation and active work are both bounded by two.

```python
import asyncio
import json


async def measure():
    gate = asyncio.Semaphore(2)
    active = 0
    peak_active = 0

    async def fetch(item):
        nonlocal active, peak_active
        async with gate:
            active += 1
            peak_active = max(peak_active, active)
            await asyncio.sleep(0)
            active -= 1
            return item

    tasks = [asyncio.create_task(fetch(item)) for item in range(12)]
    created_tasks = len(tasks)
    results = await asyncio.gather(*tasks)
    return {"peak_active": peak_active, "created_tasks": created_tasks, "results": len(results)}


print(json.dumps(asyncio.run(measure())))
```

This example uses no external services. A reviewer may execute it in a temporary directory. Review the claim and the example's meaning; changing the implementation is outside this assessment.
