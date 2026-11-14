"""Synthetic deterministic transport and clock; public fixture support."""

from retry import Cancelled


class Transport:
    def __init__(self, responses, events):
        self.responses = iter(responses)
        self.events = events
        self.calls = 0
        self.closed = False

    def receive(self):
        self.calls += 1
        self.events.append("receive")
        return next(self.responses)

    def close(self):
        self.closed = True
        self.events.append("close")


class Clock:
    def __init__(self, events, cancel=False):
        self.events = events
        self.cancel = cancel
        self.delays = []

    def sleep(self, delay):
        self.delays.append(delay)
        self.events.append(f"sleep:{delay}")
        if self.cancel:
            raise Cancelled("operator cancelled")
