def latest(events, limit):
    if limit == 0:
        return []
    by_timestamp = {event["timestamp"]: event for event in events}
    ranked = sorted(
        enumerate(by_timestamp.values()),
        key=lambda pair: (pair[1]["timestamp"], pair[0]),
        reverse=True,
    )
    return [event for _, event in ranked[:limit]]
