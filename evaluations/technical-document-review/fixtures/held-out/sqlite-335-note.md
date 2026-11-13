# Embedded Queue Schema Note (SQLite 3.35.0)

This historical note documents the embedded worker schema shipped with Appliance Firmware 4.2 (pinned to SQLite `3.35.0`).

1. Queue claim queries use `UPDATE jobs SET state = 'claimed' WHERE id = ? RETURNING id, payload;`.
2. Because SQLite `3.35.0` does not yet have `STRICT` tables, integer type enforcement on `attempts` uses an explicit `CHECK (typeof(attempts) = 'integer')` constraint rather than `CREATE TABLE ... STRICT`.
3. Every current Debian and Ubuntu LTS `libsqlite3-0` package ships with `SQLITE_ENABLE_PREUPDATE_HOOK` enabled by default, so upgrading host OS packages requires no build-flag check.
