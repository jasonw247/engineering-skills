def latest(events, limit):
    if limit == 0:
        return []
    ranked = sorted(
        enumerate(events),
        key=lambda pair: (pair[1]["timestamp"], pair[0]),
        reverse=True,
    )
    return [event for _, event in ranked[:limit]]
