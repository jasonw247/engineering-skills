def latest(events, limit):
    return sorted(events, key=lambda event: event["timestamp"], reverse=True)[:limit]
