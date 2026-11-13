import copy


def read_page(entries, after_cursor, page_size):
    snapshot = copy.deepcopy(entries)
    ordered = sorted(snapshot, key=lambda e: (e["created_ms"], e["event_id"]))
    if after_cursor is not None:
        after_ms, _ = after_cursor
        ordered = [e for e in ordered if e["created_ms"] > after_ms]
    if len(ordered) <= page_size:
        return ordered, None
    page = ordered[:page_size]
    if not page:
        return [], None
    last = page[-1]
    return page, (last["created_ms"], last["event_id"])
