"""Read-only behavior and allocation comparisons for this review."""

import gc
import importlib.util
from pathlib import Path
import tracemalloc


def load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.latest


original = load("original")
proposed = load("proposed")
events = [
    {"id": "first", "timestamp": 5},
    {"id": "second", "timestamp": 5},
    {"id": "older", "timestamp": 4},
]
for limit in (0, 1, 2, 3):
    before = [event["id"] for event in original(events, limit)]
    after = [event["id"] for event in proposed(events, limit)]
    print(f"limit={limit}: original={before}, proposed={after}")

events = [{"timestamp": index} for index in range(200_000)]


def measure(function):
    gc.collect()
    tracemalloc.start()
    result = function(events, 10)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak


old_result, old_peak = measure(original)
new_result, new_peak = measure(proposed)
assert new_result == old_result
print(f"200,000 unique timestamps, limit=10: peak traced temporary bytes: original={old_peak}, proposed={new_peak}, ratio={new_peak / old_peak:.2f}")
