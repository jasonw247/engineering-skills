"""Synthetic completed test addition with repetitive setup."""

import unittest

from retry import Cancelled, FetchError, fetch
from support import Clock, Transport


class RetryTests(unittest.TestCase):

    def test_immediate_success(self):
        events = []
        responses = [(200, "")]
        transport = Transport(responses, events)
        clock = Clock(events)
        self.assertFalse(transport.closed)
        self.assertEqual(transport.calls, 0)
        self.assertEqual(clock.delays, [])
        self.assertEqual(fetch(transport, clock), "")
        self.assertEqual(transport.calls, 1)
        self.assertEqual(clock.delays, [])
        self.assertTrue(transport.closed)
        self.assertEqual(events, ['receive', 'close'])

    def test_retry_429(self):
        events = []
        responses = [(429, "busy"), (200, "ok")]
        transport = Transport(responses, events)
        clock = Clock(events)
        self.assertFalse(transport.closed)
        self.assertEqual(transport.calls, 0)
        self.assertEqual(clock.delays, [])
        self.assertEqual(fetch(transport, clock), "ok")
        self.assertEqual(transport.calls, 2)
        self.assertEqual(clock.delays, [1])
        self.assertTrue(transport.closed)
        self.assertEqual(events, ['receive', 'sleep:1', 'receive', 'close'])

    def test_retry_503_twice(self):
        events = []
        responses = [(503, "busy"), (503, "busy"), (200, "ok")]
        transport = Transport(responses, events)
        clock = Clock(events)
        self.assertFalse(transport.closed)
        self.assertEqual(transport.calls, 0)
        self.assertEqual(clock.delays, [])
        self.assertEqual(fetch(transport, clock), "ok")
        self.assertEqual(transport.calls, 3)
        self.assertEqual(clock.delays, [1, 2])
        self.assertTrue(transport.closed)
        self.assertEqual(events, ['receive', 'sleep:1', 'receive', 'sleep:2', 'receive', 'close'])

    def test_exhaustion(self):
        events = []
        responses = [(503, "busy")] * 3
        transport = Transport(responses, events)
        clock = Clock(events)
        self.assertFalse(transport.closed)
        self.assertEqual(transport.calls, 0)
        self.assertEqual(clock.delays, [])
        with self.assertRaises(FetchError) as error:
            fetch(transport, clock)
        self.assertEqual(str(error.exception), "retry exhausted")
        self.assertEqual(transport.calls, 3)
        self.assertEqual(clock.delays, [1, 2])
        self.assertTrue(transport.closed)
        self.assertEqual(events, ['receive', 'sleep:1', 'receive', 'sleep:2', 'receive', 'close'])

    def test_reject_400(self):
        events = []
        responses = [(400, "bad"), (200, "wrong")]
        transport = Transport(responses, events)
        clock = Clock(events)
        self.assertFalse(transport.closed)
        self.assertEqual(transport.calls, 0)
        self.assertEqual(clock.delays, [])
        with self.assertRaises(FetchError) as error:
            fetch(transport, clock)
        self.assertEqual(str(error.exception), "status 400")
        self.assertEqual(transport.calls, 1)
        self.assertEqual(clock.delays, [])
        self.assertTrue(transport.closed)
        self.assertEqual(events, ['receive', 'close'])

    def test_cancel_closes_transport(self):
        events = []
        transport = Transport([(503, "busy"), (200, "wrong")], events)
        clock = Clock(events, cancel=True)
        with self.assertRaises(Cancelled) as error:
            fetch(transport, clock)
        self.assertEqual(str(error.exception), "operator cancelled")
        self.assertTrue(transport.closed, "cancelled retry must close the transport")
        self.assertEqual(transport.calls, 1)
        self.assertEqual(clock.delays, [1])
        self.assertEqual(events, ["receive", "sleep:1", "close"])

    def test_invalid_attempts(self):
        events = []
        transport = Transport([(200, "wrong")], events)
        clock = Clock(events)
        with self.assertRaises(ValueError) as error:
            fetch(transport, clock, attempts=0)
        self.assertEqual(str(error.exception), "attempts must be positive")
        self.assertEqual(transport.calls, 0)
        self.assertEqual(clock.delays, [])
        self.assertFalse(transport.closed)
        self.assertEqual(events, [])


if __name__ == "__main__":
    unittest.main()
