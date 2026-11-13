import asyncio


async def enrich_all(items, fetch, limit=4):
    """Return results in input order from an asynchronous input iterable."""
    semaphore = asyncio.Semaphore(limit)

    async def one(item):
        async with semaphore:
            return await fetch(item)

    tasks = [asyncio.create_task(one(item)) async for item in items]
    return await asyncio.gather(*tasks)
