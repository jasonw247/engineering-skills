import asyncio


async def enrich_all(items, fetch, limit=4):
    """Return results in input order from an asynchronous input iterable.

    At most ``limit`` fetches and ``limit`` queued items are admitted, plus
    one item held by the producer awaiting admission. The returned list grows
    with the input. This call owns its workers and iteration; it closes the
    input iterator on exit if that iterator provides ``aclose``. ``fetch``
    remains responsible for its own external resources and must cooperate with
    cancellation. ``limit`` must be a positive integer.
    """
    if not isinstance(limit, int):
        raise TypeError("limit must be a positive integer")
    if limit < 1:
        raise ValueError("limit must be a positive integer")

    queue = asyncio.Queue(maxsize=limit)
    finished = object()
    results = []

    async def produce():
        iterator = aiter(items)
        try:
            async for item in iterator:
                index = len(results)
                results.append(None)
                await queue.put((index, item))
        finally:
            close = getattr(iterator, "aclose", None)
            if close is not None:
                await close()
        for _ in range(limit):
            await queue.put(finished)

    async def consume():
        while True:
            entry = await queue.get()
            if entry is finished:
                return
            index, item = entry
            results[index] = await fetch(item)

    tasks = [asyncio.create_task(produce())]
    tasks.extend(asyncio.create_task(consume()) for _ in range(limit))
    completion = asyncio.gather(*tasks)
    try:
        # Shield lets this owner cancel each child once, even if the caller
        # cancels repeatedly while a child is cleaning up asynchronously.
        await asyncio.shield(completion)
    finally:
        for task in tasks:
            if not task.done() and not task.cancelling():
                task.cancel()
        cleanup = asyncio.gather(*tasks, return_exceptions=True)
        cancelled_during_cleanup = False
        while not cleanup.done():
            try:
                await asyncio.shield(cleanup)
            except asyncio.CancelledError:
                cancelled_during_cleanup = True
        cleanup.result()
        # Retrieve a failure that may have arrived after caller cancellation.
        if not completion.cancelled():
            completion.exception()
        if cancelled_during_cleanup:
            raise asyncio.CancelledError
    return results
