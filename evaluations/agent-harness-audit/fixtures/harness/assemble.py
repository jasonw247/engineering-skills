"""Builds the request sent to the model on each turn."""

import datetime
import platform

SYSTEM_TEMPLATE = """You are a coding agent.
# Environment
OS: {os}
Current time: {now}
Open tasks: {open_tasks}
"""


def build_request(history, tools, open_tasks, reminder):
    system = SYSTEM_TEMPLATE.format(
        os=platform.system(),
        now=datetime.datetime.now().isoformat(timespec="seconds"),
        open_tasks=len(open_tasks),
    )
    # Refresh the reminder in place so the model always sees the latest one.
    for message in history:
        if message.get("kind") == "reminder":
            message["content"] = reminder
    return {"system": system, "tools": tools, "messages": history}


def clear_old_results(history, keep_last=5):
    """Drop old tool results to save space."""
    results = [m for m in history if m["role"] == "tool_result"]
    stale = {id(m) for m in results[:-keep_last]}
    return [m for m in history if id(m) not in stale]
