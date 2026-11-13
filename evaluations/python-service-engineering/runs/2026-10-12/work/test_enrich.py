import asyncio
import unittest

from enrich import enrich_all


class FetchFailure(Exception):
    pass


class SourceFailure(Exception):
    pass


class EnrichTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.initial_tasks = asyncio.all_tasks()

    async def asyncTearDown(self):
        remaining = asyncio.all_tasks() - self.initial_tasks
        remaining.discard(asyncio.current_task())
        self.assertFalse(remaining, f"Tasks leaked: {remaining}")

    async def test_empty_input(self):
        closed = False

        async def source():
            nonlocal closed
            try:
                for item in ():
                    yield item
            finally:
                closed = True

        async def fetch(item):
            self.fail("Empty input must not call fetch")

        self.assertEqual(await enrich_all(source(), fetch), [])
        self.assertTrue(closed)

    async def test_results_preserve_order_when_completion_does_not(self):
        release_first = asyncio.Event()
        later_finished = asyncio.Event()
        completion_order = []

        async def source():
            for item in range(12):
                yield item

        async def fetch(item):
            if item == 0:
                await release_first.wait()
            completion_order.append(item)
            if item == 11:
                later_finished.set()
            return item * 3

        task = asyncio.create_task(enrich_all(source(), fetch, limit=3))
        await asyncio.wait_for(later_finished.wait(), 2)
        self.assertNotIn(0, completion_order)
        release_first.set()
        self.assertEqual(await asyncio.wait_for(task, 2), [i * 3 for i in range(12)])
        self.assertEqual(completion_order[-1], 0)

    async def test_large_stream_has_backpressure_and_bounded_live_tasks(self):
        count = 20_000
        limit = 4
        consumed = active = peak_active = peak_tasks = 0
        all_started = asyncio.Event()
        release = asyncio.Event()
        baseline = asyncio.all_tasks()

        async def source():
            nonlocal consumed
            for item in range(count):
                consumed += 1
                yield item

        async def fetch(item):
            nonlocal active, peak_active, peak_tasks
            active += 1
            peak_active = max(peak_active, active)
            peak_tasks = max(peak_tasks, len(asyncio.all_tasks() - baseline))
            if active == limit:
                all_started.set()
            try:
                await release.wait()
                await asyncio.sleep(0)
                return item
            finally:
                active -= 1

        task = asyncio.create_task(enrich_all(source(), fetch, limit))
        async with asyncio.timeout(3):
            await all_started.wait()
        await asyncio.sleep(0)
        self.assertLessEqual(consumed, 2 * limit + 1)
        self.assertEqual(active, limit)
        self.assertLessEqual(len(asyncio.all_tasks() - baseline), limit + 2)
        release.set()
        async with asyncio.timeout(15):
            result = await task
        self.assertEqual(result, list(range(count)))
        self.assertLessEqual(peak_active, limit)
        self.assertLessEqual(peak_tasks, limit + 2)
        self.assertEqual(active, 0)
        print(f"large stream: items={count}, peak fetches={peak_active}, "
              f"peak owned tasks including caller={peak_tasks}")

    async def test_fetch_failure_stops_blocked_source_and_sibling(self):
        source_waiting = asyncio.Event()
        sibling_started = asyncio.Event()
        source_closed = asyncio.Event()
        sibling_closed = asyncio.Event()
        never = asyncio.Event()
        error = FetchFailure("downstream failed")

        async def source():
            try:
                yield 0
                yield 1
                source_waiting.set()
                await never.wait()
            finally:
                await asyncio.sleep(0)
                source_closed.set()

        async def fetch(item):
            if item == 0:
                await source_waiting.wait()
                await sibling_started.wait()
                raise error
            try:
                sibling_started.set()
                await never.wait()
            finally:
                await asyncio.sleep(0)
                sibling_closed.set()

        async with asyncio.timeout(3):
            with self.assertRaises(FetchFailure) as caught:
                await enrich_all(source(), fetch, limit=2)
        self.assertIs(caught.exception, error)
        self.assertTrue(source_closed.is_set())
        self.assertTrue(sibling_closed.is_set())

    async def test_source_failure_stops_active_fetches(self):
        all_started = asyncio.Event()
        never = asyncio.Event()
        started = closed = 0
        error = SourceFailure("stream failed")

        async def source():
            yield 0
            yield 1
            await all_started.wait()
            raise error

        async def fetch(item):
            nonlocal started, closed
            started += 1
            if started == 2:
                all_started.set()
            try:
                await never.wait()
            finally:
                await asyncio.sleep(0)
                closed += 1

        async with asyncio.timeout(3):
            with self.assertRaises(SourceFailure) as caught:
                await enrich_all(source(), fetch, limit=2)
        self.assertIs(caught.exception, error)
        self.assertEqual(closed, 2)

    async def test_repeated_caller_cancellation_waits_for_cleanup(self):
        all_started = asyncio.Event()
        cleanup_started = asyncio.Event()
        source_closed = asyncio.Event()
        allow_cleanup = asyncio.Event()
        never = asyncio.Event()
        started = cleaning = closed = 0

        async def source():
            try:
                for item in range(100):
                    yield item
            finally:
                await asyncio.sleep(0)
                source_closed.set()

        async def fetch(item):
            nonlocal started, cleaning, closed
            started += 1
            if started == 2:
                all_started.set()
            try:
                await never.wait()
            finally:
                cleaning += 1
                if cleaning == 2:
                    cleanup_started.set()
                await allow_cleanup.wait()
                closed += 1

        task = asyncio.create_task(enrich_all(source(), fetch, limit=2))
        async with asyncio.timeout(3):
            await all_started.wait()
            task.cancel()
            await cleanup_started.wait()
            await source_closed.wait()
            self.assertFalse(task.done())
            task.cancel()
            await asyncio.sleep(0)
            self.assertFalse(task.done())
            self.assertEqual(closed, 0)
            allow_cleanup.set()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertEqual(closed, 2)

    async def test_child_cancellation_stops_other_work(self):
        sibling_started = asyncio.Event()
        sibling_closed = asyncio.Event()
        never = asyncio.Event()

        async def source():
            yield 0
            yield 1

        async def fetch(item):
            if item == 0:
                await sibling_started.wait()
                raise asyncio.CancelledError
            try:
                sibling_started.set()
                await never.wait()
            finally:
                await asyncio.sleep(0)
                sibling_closed.set()

        async with asyncio.timeout(3):
            with self.assertRaises(asyncio.CancelledError):
                await enrich_all(source(), fetch, limit=2)
        self.assertTrue(sibling_closed.is_set())

    async def test_limit_one(self):
        active = 0

        async def source():
            for item in [3, 1, 2]:
                yield item

        async def fetch(item):
            nonlocal active
            active += 1
            self.assertEqual(active, 1)
            await asyncio.sleep(0)
            active -= 1
            return item

        self.assertEqual(await enrich_all(source(), fetch, limit=1), [3, 1, 2])

    async def test_invalid_limits_do_not_consume_input(self):
        async def source():
            self.fail("Invalid limits must fail before consuming input")
            yield 0

        async def fetch(item):
            self.fail("Invalid limits must fail before fetching")

        for limit, exception in [(0, ValueError), (-1, ValueError), (1.5, TypeError)]:
            with self.subTest(limit=limit):
                stream = source()
                try:
                    with self.assertRaises(exception):
                        await enrich_all(stream, fetch, limit)
                finally:
                    await stream.aclose()


if __name__ == "__main__":
    unittest.main()
