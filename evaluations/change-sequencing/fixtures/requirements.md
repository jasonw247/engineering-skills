# Synthetic change: per-workspace billing plans

Synthetic input for acceptance trials of `change-sequencing`.

Today every account has one `plan` column on the `accounts` table, read by the billing service, the admin UI, and a nightly invoicing job. Product wants plans per workspace instead of per account.

Requested in one pull request (about 3,400 changed lines):

- Rename `AccountPlan` to `Plan` throughout the codebase (about 1,900 lines, mechanical).
- Add a `workspace_plans` table and backfill it from `accounts.plan` for 2.1 million workspaces.
- Change the billing service and invoicing job to read the workspace plan.
- Add a workspace plan selector to the admin UI behind the `workspace_plans` flag.
- Remove `accounts.plan` and the code that reads it.
- Reformat the billing package with the new formatter configuration.

Constraints: deployments run the database migration before the application; the invoicing job runs nightly at 02:00 UTC and must never bill a workspace twice; the team uses stacked pull requests.
