def read_page(entries, after_cursor, page_size):
    ordered = sorted(entries, key=lambda e: (e["created_ms"], e["event_id"]))
    if after_cursor is not None:
        ordered = [e for e in ordered if (e["created_ms"], e["event_id"]) > after_cursor]
    page = ordered[:page_size]
    if len(ordered) <= page_size:
        return page, None
    last = page[-1]
    return page, (last["created_ms"], last["event_id"])
