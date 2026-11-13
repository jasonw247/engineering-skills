# Draft issues: organization-wide audit log export

Target repository: `example/audit-service`. Status: **draft only. Nothing has been created.** Filing waits for your approval (see "Filing plan" at the end).

## Why split

The team's estimate is about 1,500 changed lines across four subsystems (db, api, jobs, web), with a 40-million-row backfill whose rollout has to be reverted separately from the code. That is about three times the ~500-line point where a split is worth considering. It also breaks every other split signal: several behavior changes, a migration on its own rollout schedule, and acceptance criteria no single PR could meet. The work splits cleanly along expand → backfill → cut over, then one vertical slice per behavior. So: one parent issue and five child issues, each one PR.

## Sequence

| Order | Change (issue) | Purpose | Depends on | Checks | Rollback / notes |
| --- | --- | --- | --- | --- | --- |
| 1 | A. Add `org_id` to audit events and set it on every new event | Expand: new nullable column, all writers populate it | none | Migration up/down test; insert-path tests assert `org_id` is set | Revert code, then drop the column. Nothing reads it yet |
| 2 | B. Backfill `org_id` for existing audit events | Backfill ~40M rows, validate, build the export index | A deployed to **all** writers | Batch/resume tests; validation query reports 0 NULL `org_id` | Stop the job; rows already written stay correct. Drop the index if needed |
| 3 | C. Stream org audit log export as CSV or JSONL | Cut over: first reader of `org_id`; synchronous export for admins | B validated in production | Endpoint tests: authz, formats, range, streaming, size limit | Revert the PR; no data changes |
| 4 | D. Deliver large org audit exports by emailed link | Async job for exports over 1M events | C | Job, signed-URL expiry, email, and 202 response tests | Revert; the endpoint goes back to rejecting over-limit requests |
| 5 | E. Add audit log export to organization settings | UI plus admin guide | C, D | Component/e2e tests for both sync and queued paths | Revert the PR; the API stays usable |

Order rationale: the schema has to exist and be backfilled before anything reads it by organization. The UI comes last so it is built against the final API contract, including the async response.

There is no contract step. The old per-project endpoint and table stay. Nothing is removed.

## Migration plan

| Step | Deploy order | Signal it worked | Rollback | Must not happen until the next step lands |
| --- | --- | --- | --- | --- |
| A. Expand | Run the migration (nullable column, no default, so no table rewrite), then deploy writers that set `org_id` | New events have non-NULL `org_id`; NULL count stops growing | Revert writers, drop column | Start the backfill before every writer instance runs A's code (otherwise new NULL rows appear behind it) |
| B. Backfill | Run the batched job after A is fully rolled out; build the `(org_id, created_at)` index afterwards, without blocking writes | Progress reaches 100%; validation query returns 0 NULL rows and 0 rows where `org_id` ≠ the project's org | Stop the job (it is idempotent and resumable). Drop the index | Any code path that filters by `org_id` |
| C. Cut over | Deploy the export endpoint | Exports for a test org match the union of its per-project exports | Revert | none |

## Parts that were not split further

- **C (API, about 450 lines with docs)** is near the trigger. It stays whole because authorization, range validation, the two serializers, and streaming are one endpoint with one contract; a serializer without its endpoint would be an interface without a user. If the estimate grows a lot, the split point is CSV and JSONL: ship JSONL first, then add CSV.
- **API docs** go with the PR that changes the API (C, D) and the **admin guide** goes with the UI (E). A separate docs issue would drift from the behavior it describes.

## Labels used

All from `inputs/labels.json`: `type:feature`, `type:chore`, `area:db`, `area:api`, `area:jobs`, `area:web`. No issue types, templates, or milestones were available, so the bodies use the fallback format. Check for issue templates before filing.

---

## Parent: Let admins export their organization's full audit log

Labels: `type:feature`, `area:api`, `area:web`, `area:jobs`, `area:db`

```markdown
## Outcome
An organization admin can export every audit event for their organization over
a chosen date range, as CSV or JSONL, from the API or from the organization
settings page. Small exports download directly. Exports over 1 million events
arrive as an emailed link that expires after 24 hours.

Today only `GET /projects/{id}/audit` exists. It returns one project's events
as JSON, and the web UI shows a per-project table, so an org-wide export means
one request per project.

## Plan
The sub-issues are linked below in delivery order. Audit events only carry
`project_id`, so `org_id` has to be added and backfilled (~40M rows) before
anything can read by organization. The UI comes last so it is built against
the final API, including the async response.

## Done when
- [ ] All sub-issues are closed
- [ ] In a staging org with several projects, an admin uses the settings page to
      export a range under 1M events (direct download) and a range over 1M events
      (emailed link), and both files contain exactly the union of the per-project
      audit events for that range

## Out of scope
- Changing or removing `GET /projects/{id}/audit` or the per-project table
- Formats other than CSV and JSONL
- Scheduled or recurring exports
- Making `audit_events.org_id` NOT NULL (can follow once the backfill is validated)

Size: about 1,500 changed lines in total across the sub-issues (team estimate).
```

---

## A. Add `org_id` to audit events and set it on every new event

Labels: `type:chore`, `area:db`

```markdown
Part of #<PARENT>

## Context
Audit events carry only `project_id`, so the service cannot query events by
organization. The planned org-wide export needs `audit_events.org_id`. This is
the first, backward-compatible step: add the column and fill it for new events.
Existing rows (~40M) are backfilled in a separate issue.

## Outcome
`audit_events` has a nullable `org_id` column, and every code path that inserts
an audit event sets it from the event's project. If later work never lands,
the column is harmless: nothing reads it yet.

## Acceptance criteria
- [ ] A migration adds a nullable `org_id` column with no default (no table
      rewrite on a 40M-row table) and has a working down migration
- [ ] Every insert path for audit events sets `org_id` to the owning project's
      organization; tests cover each path
- [ ] A test fails if a new audit event is written with NULL `org_id`
- [ ] No existing query or API response changes

## Out of scope
- Backfilling existing rows, and any index on `org_id` (#<B>)
- Any reader of `org_id` (#<C>)
- A NOT NULL constraint

## Notes
Rollout: run the migration, then deploy the writers. Do not start the backfill
until every writer instance runs this code; otherwise rows written by old
instances will be left NULL.
Open question: if a project can move between organizations, which org should
historical events keep? This issue assumes the org at write time.
Size: about 120 changed lines (estimate).
```

---

## B. Backfill `org_id` for existing audit events

Labels: `type:chore`, `area:db`, `area:jobs`

```markdown
Part of #<PARENT>

## Context
`audit_events.org_id` exists and new events set it (#<A>), but roughly 40
million existing rows have NULL `org_id`. The org-wide export cannot read by
organization until these are filled and checked.

## Outcome
Every audit event has the correct `org_id`, confirmed by a validation query,
and an `(org_id, created_at)` index supports range queries by organization.
If later work never lands, the data is simply complete and unused.

## Acceptance criteria
- [ ] A backfill job updates rows in bounded batches (keyed by primary key) and
      does not hold long locks or block audit writes
- [ ] The job records progress and can be stopped and resumed without redoing
      or corrupting finished batches. Re-running it is a no-op
- [ ] Transient failures retry with backoff. A batch that keeps failing stops
      the job with a clear error instead of being skipped
- [ ] A validation query (committed with the job) reports the count of NULL
      `org_id` rows and the count of rows whose `org_id` does not match their
      project's organization. Both are 0 after a full run in staging
- [ ] After the backfill, an `(org_id, created_at)` index is built without
      blocking writes (for example `CREATE INDEX CONCURRENTLY` on PostgreSQL)
- [ ] A runbook note gives how to start, monitor, pause, and resume the job

## Out of scope
- Any reader of `org_id` (#<C>)
- A NOT NULL constraint (possible follow-up once validation passes in production)

## Notes
Prerequisite: #<A> deployed to all writers before the job starts.
Record the production run's duration and the validation result on this issue;
#<C> must not ship until validation shows 0 mismatches in production.
Size: about 180 changed lines (estimate).

Blocked by #<A>
```

---

## C. Stream org audit log export as CSV or JSONL

Labels: `type:feature`, `area:api`

```markdown
Part of #<PARENT>

## Context
Admins can only fetch audit events one project at a time via
`GET /projects/{id}/audit` (JSON). `audit_events.org_id` is now backfilled and
indexed (#<B>), so events can be read by organization.

## Outcome
An organization admin can call
`GET /orgs/{id}/audit/export?from=&to=&format=csv|jsonl` and receive a
streamed file of every audit event in that organization within the range.
Requests that would exceed 1,000,000 events are rejected with a clear error.
That limit stays the only behavior if the async issue never lands.

## Acceptance criteria
- [ ] Only admins of organization `{id}` can call it. Other users get 403, and
      unknown orgs get 404 without revealing whether the org exists
- [ ] `from` and `to` are required, validated, and documented (format, inclusive
      or exclusive bounds, time zone). Invalid ranges return 400
- [ ] `format=csv` and `format=jsonl` each return the same set of events with
      the correct `Content-Type` and a `Content-Disposition` filename. Other
      values return 400
- [ ] The response streams: memory use stays flat for a large export (a test
      or benchmark shows it does not buffer the whole result)
- [ ] CSV escapes commas, quotes, and newlines in field values (tested)
- [ ] Results are ordered by `created_at`, then id, so repeated exports match
- [ ] A range over 1,000,000 events returns an error status and a message
      telling the caller to narrow the range
- [ ] Integration test: for an org with several projects, the export equals the
      union of the per-project audit events for the same range
- [ ] API reference docs describe the endpoint, parameters, formats, limit, and
      errors

## Out of scope
- Async export for more than 1M events (#<D>)
- UI (#<E>)
- Changes to `GET /projects/{id}/audit`

## Notes
Do not merge until #<B>'s validation shows 0 NULL or mismatched rows in
production, or exports will silently miss events.
Counting events before streaming can use the `(org_id, created_at)` index.
If the estimate grows a lot, ship JSONL first and add CSV in a follow-up.
Size: about 450 changed lines including tests and API docs (estimate).

Blocked by #<B>
```

---

## D. Deliver large org audit exports by emailed link

Labels: `type:feature`, `area:jobs`, `area:api`

```markdown
Part of #<PARENT>

## Context
`GET /orgs/{id}/audit/export` streams exports up to 1,000,000 events and rejects
anything larger (#<C>). Admins of large organizations still need those exports.

## Outcome
For a request over 1,000,000 events, the endpoint queues a background export
and returns `202 Accepted`. When the file is ready, the requesting admin gets
an email with a signed download link that expires 24 hours after it is issued.

## Acceptance criteria
- [ ] Over-limit requests return 202 with a documented body (at least an export
      id and status) instead of the error from #<C>. Requests at or under the
      limit still stream as before
- [ ] The job writes the same content #<C> would produce for that org, range,
      and format (shared serializer; a test compares the two)
- [ ] The emailed link is signed, works for 24 hours, and returns an expiry
      error afterwards (tested with a controlled clock)
- [ ] The link only grants the one file. Altering the signature or path is
      rejected
- [ ] The job retries transient failures. On final failure the admin gets an
      email saying the export failed
- [ ] Export files are deleted once their link has expired
- [ ] API docs cover the 202 response, the email, and the 24-hour expiry

## Out of scope
- UI for queued exports (#<E>)
- Status polling or listing past exports
- Exports over the limit for non-admin users

## Notes
Open questions: where export files are stored, and whether expired files must
be deleted right away or after a retention window.
Size: about 380 changed lines including tests and docs (estimate).

Blocked by #<C>
```

---

## E. Add audit log export to organization settings

Labels: `type:feature`, `area:web`

```markdown
Part of #<PARENT>

## Context
The web UI only shows a per-project audit table. The API now supports
org-wide export: direct streaming (#<C>), with large exports queued and
emailed (#<D>).

## Outcome
Organization admins see an "Export audit log" control on the organization
settings page. They choose a date range and a format (CSV or JSONL), start the
export, and either get the file directly or are told it will arrive by email.

## Acceptance criteria
- [ ] The control is shown only to organization admins
- [ ] Date range and format pickers validate input before submitting
      (from ≤ to, both required)
- [ ] During a direct download the button shows a progress state and cannot be
      submitted twice. Success and failure are shown to the user
- [ ] A 202 response shows a message that the export will be emailed and the
      link will expire after 24 hours
- [ ] API errors (403, 400) show readable messages
- [ ] Tests cover the direct-download and queued paths and the non-admin case
- [ ] The admin guide documents how to export the audit log, the formats, and
      the large-export email behavior

## Out of scope
- Changes to the per-project audit table
- A list of past exports

## Notes
Progress for a streamed download may be indeterminate if the response has no
`Content-Length`. Showing an in-progress state is enough.
Size: about 400 changed lines including tests and the admin guide (estimate).

Blocked by #<D>
```

---

## Filing plan (after approval only)

1. Confirm the target is `example/audit-service` and not an upstream or fork.
2. Labels are taken from `inputs/labels.json`. Check issue templates, issue types, and milestones before filing.
3. A duplicate search was not run; I was told there are no open issues on this topic.
4. Create in blocker order: parent, A, B, C, D, E, replacing the `#<…>` placeholders with real numbers.
5. After all six exist, link A–E as sub-issues of the parent and add blocked-by links: B←A, C←B, D←C, E←D.

## Open questions for the team

- Project moves: if a project can change organization, should historical events keep the org they had at write time (the assumption here) or follow the project?
- Storage and retention for async export files (issue D).
- Is the 1,000,000-event threshold measured by counting before streaming (the assumption here), or should it be enforced some other way?
