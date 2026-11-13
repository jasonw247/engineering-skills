# Audit log cursor contract

`read_page(entries, after_cursor, page_size)` returns `(items, next_cursor)` for audit records ordered by ascending `(created_ms, event_id)`.

- Multiple distinct audit records may share the same `created_ms` with different `event_id` strings; every record must appear once across sequential page reads.
- `after_cursor` is `None` on the first page or a `(created_ms, event_id)` tuple returned as `next_cursor` by the preceding page call.
- `page_size` is a positive integer (`>= 1`). When no records follow the returned page, `next_cursor` is `None`.
- `entries` may hold tens of thousands of dicts; common `page_size` is `50`. Do not modify inputs during review.
