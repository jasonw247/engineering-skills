---
name: domain-modeling
description: Clarify ambiguous domain concepts, align codebase and product terminology, and maintain glossaries or Architecture Decision Records (ADRs). Use when resolving overloaded domain terms, stress-testing domain boundaries with edge cases, editing GLOSSARY.md, or recording consequential architectural trade-offs; not for simply reading an existing glossary while coding or refactoring internal module interfaces.
---

# Domain modeling

Sharpen the project's domain model when concepts are ambiguous, overloaded across modules, or undergoing a hard-to-reverse design decision.

## Locate conventions before writing

1. Search repository instructions and docs for existing glossary and decision-record paths (`GLOSSARY.md`, `GLOSSARY-MAP.md`, `docs/adr/`, `docs/decisions/`, RFC folders). Follow existing locations, numbering, and templates whenever present.
2. Respect write boundaries:
   - On a read-only question or review, report terminology conflicts and proposed definitions in your reply without creating or editing files.
   - When documentation edits are authorized and a glossary already exists, update it as terms settle using [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md).
   - When the repository has no glossary or ADR directory yet, confirm with the user before creating `GLOSSARY.md` or `docs/adr/`.

Fallback paths once new files are approved:
- Single bounded context: root `GLOSSARY.md` and `docs/adr/NNNN-slug.md`.
- Multiple bounded contexts: root `GLOSSARY-MAP.md` pointing to per-context glossaries (such as `src/billing/GLOSSARY.md`) and context-specific `docs/adr/` directories where needed.

## Clarify terms and boundaries

- Compare the user's terms against existing glossary entries, type and table names, and API fields, and surface conflicts with exact file locations (for example, pointing out where `cancelOrder` voids an entire order while a new request uses cancellation for a single line item).
- Define each glossary term from its business meaning and invariants rather than database column types, HTTP status codes, or generic plumbing names (`RetryPolicy`, `Timeout`, `DTO`, `Worker`), and list retired synonyms under `_Avoid_`.
- Test proposed entity boundaries against lifecycle edge cases: partial completion, duplicate or out-of-order events, ownership transfer, and expiration or deletion.

## Gate ADRs strictly

Propose or write an ADR ([format](ADR-FORMAT.md)) only when all three conditions hold:

1. **Costly to reverse:** changing direction later requires data migration, public contract changes, or cross-team rework.
2. **Non-obvious from code alone:** a maintainer reading the code later could reasonably wonder why a simpler-looking approach was skipped and undo a deliberate constraint.
3. **Genuine trade-off:** at least two viable options existed and one was chosen for concrete reasons.

Skip ADRs for routine library choices, local helper names, or easily reversed implementation details; code comments and commit messages cover those directly.
