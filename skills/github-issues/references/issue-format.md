# Issue format

Use the repository's issue templates or forms when it has them. These templates are the fallback. Leave out sections that would be empty.

## Titles

| Weak | Better | Why |
| --- | --- | --- |
| `Sync improvements` | `Cap sync retries with a per-client budget` | States the outcome |
| `[Bug] export broken` | `CSV export drops rows after the first 10,000` | Describes the observed failure; the type or label marks it as a bug |
| `Phase 2` | `Backfill plan_id for existing accounts` | Stands alone without the parent |

## Single issue

```markdown
## Context
Why this matters now: current behavior, who it affects, and links to evidence
(incident, discussion, related PR).

## Outcome
What is true when this is done, from a user's or maintainer's point of view.

## Acceptance criteria
- [ ] An observable condition that can be checked on its own
- [ ] The tests or checks that demonstrate it

## Out of scope
- Related work deliberately excluded, with its issue if one exists

## Notes
Starting points in the code, constraints, open questions.
Size: about N changed lines (estimate).

Blocked by #N
Related #M
```

## Bug

Add these to the single-issue template:

```markdown
## Steps to reproduce
1. ...

## Expected
## Actual
## Environment
Version, platform, configuration that matters.
```

## Parent

```markdown
## Outcome
The overall result the children deliver together.

## Plan
The sub-issues are linked below in delivery order. One sentence on why they
are in this order (for example: expand the schema before switching readers).

## Done when
- [ ] All sub-issues are closed
- [ ] An end-to-end check that no single child can show on its own

## Out of scope
- ...
```

A parent describes the whole and does not repeat its children's acceptance criteria. Native sub-issue links show which children are open. Add a checklist of children only if the repository does not use sub-issues.

## Child

```markdown
Part of #PARENT

## Outcome
What this change delivers, and the state the system is left in if later
children never land.

## Acceptance criteria
- [ ] ...

## Notes
Size: about N changed lines (estimate).

Blocked by #N
```

A child must make sense to someone who has not read its siblings. Restate the context it needs instead of saying "see parent".
