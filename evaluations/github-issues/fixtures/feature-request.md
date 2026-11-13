# Request: organization-wide audit log export

Admins need to export the audit log for their whole organization, not one
project at a time. Today `GET /projects/{id}/audit` returns one project's
events as JSON, and the web UI shows a per-project table.

Wanted:
- A new `audit_events.org_id` column (currently events only carry project_id),
  backfilled for roughly 40 million existing rows.
- `GET /orgs/{id}/audit/export?from=&to=&format=csv|jsonl`, streaming, admin only.
- An "Export" button on the organization settings page with date range and
  format pickers, and a download progress state.
- An async job for exports larger than 1 million events, emailing a signed
  link that expires after 24 hours.
- Docs for the API and the admin guide.

Rough estimate from the team: about 1,500 changed lines including tests
(migration and backfill ~300, API ~400, async job ~350, UI ~350, docs ~100).
