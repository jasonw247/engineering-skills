# ADR format

Use the repository's existing decision-record directory, template, and numbering scheme first. Fall back to `docs/adr/0001-slug.md` (incrementing the highest existing four-digit prefix) only when no convention exists and creating an ADR was approved.

## Minimal template

```markdown
# {Short imperative or declarative decision title}

{2-4 sentences: the constraint or problem, the option chosen, and the decisive trade-off.}
```

A single tight paragraph is enough when it records the constraint, decision, and reason clearly.

## Optional sections (include only when they carry load)

- **Status:** `proposed | accepted | superseded by ADR-NNNN` (include when superseding an older ADR, and update the older ADR's status line too so readers do not follow stale decisions).
- **Rejected alternatives:** include when a plausible option (for example, GraphQL vs REST, ORM vs raw SQL, sync RPC vs event bus) was rejected for non-obvious reasons someone would otherwise re-propose in six months.
- **Consequences & operational obligations:** include when the decision creates an ongoing constraint (for example, *"callers must supply an idempotency key; cross-context reads go by `CustomerId` only"*).

## Decisions worth an ADR

- **Data ownership and consistency boundaries:** event-sourced write model vs state table; which service owns `Customer` truth; eventual consistency windows.
- **Cross-service or public contracts:** sync HTTP vs async events; versioning and compatibility guarantees.
- **Lock-in infrastructure:** primary datastore, queue/broker, auth model, or regulatory hosting constraints invisible in source code.
- **Deliberate departures from house defaults:** hand-written SQL in an ORM codebase due to a measured query constraint, or vendoring a dependency to satisfy an offline build rule.
