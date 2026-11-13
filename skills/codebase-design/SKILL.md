---
name: codebase-design
description: Design and evaluate module interfaces, ownership boundaries, and test seams using deep-module principles. Use when designing a new module boundary, refactoring shallow pass-through layers, deciding where a dependency seam belongs, or comparing alternative APIs; not for routine local edits or domain-glossary definitions.
---

# Codebase design

Evaluate and shape modules by comparing the functionality they deliver against the interface cost they impose on callers (John Ousterhout, *A Philosophy of Software Design*). Preserve the repository's established domain vocabulary and boundaries; apply this skill where an interface, ownership, or testability choice is actually being made.

## Core concepts

- **Module:** any unit with an interface and an implementation, from a single function or class up to a package or service.
- **Interface:** everything a caller must know to use the module safely: signatures, preconditions, call ordering, error modes, side effects, configuration knobs, and performance behavior. Type signatures are only the visible part of this cost.
- **Depth:** functionality delivered relative to interface cost. A deep module hides substantial rules, state, or coordination behind a small contract (such as Unix file descriptors or a retry-aware HTTP client). A shallow module makes callers learn almost as much detail as the module implements.
- **Seam** *(Michael Feathers)*: a boundary where behavior can be swapped (such as a test double or alternate transport) without editing callers. Keep internal test seams private rather than enlarging the public API.
- **Adapter:** a concrete implementation behind a seam (such as a Postgres store versus an in-memory fake).
- **Leverage and locality:** deep modules give callers leverage (more capability per rule learned) and give maintainers locality (invariants and bug fixes stay inside one module instead of touching every caller).

## Evaluate or shape a boundary

1. Inspect real call sites, error paths, and existing helpers before adding new types or layers.
2. Run the deletion test: ask what happens if this module disappears and callers inline its work. If total complexity drops, the layer was pass-through ceremony and can be collapsed; if tricky state, edge cases, or security/resource invariants scatter across callers, the boundary earns its keep even with one implementation.
3. Pull shared caller obligations inward so ordinary calls succeed without setup rituals or post-filtering, and define errors out of existence where domain rules allow (for example, idempotent `delete_if_present` when missing keys are normal).
4. Add an injected dependency or port only when multiple implementations exist, when a security, resource, or process boundary requires isolation, or when deterministic tests must control external I/O, clocks, or randomness. Compare two contrasting interface shapes with [design it twice](DESIGN-IT-TWICE.md) when a boundary is hard to reverse, and read [deepening](DEEPENING.md) when consolidating fragmented wrappers.

## Common shallow-module mistakes

- Cramming distinct operations into one `run(mode, options)` mega-method cuts method count while raising interface cost through mode-dependent preconditions and tangled return types, without reducing the behavioral cases tests must cover. Deepen modules by generalizing rules and removing special cases, not by hiding unrelated operations behind flags.
- Forwarding layers (`Controller -> Service -> Manager -> Repository`) that pass identical arguments 1-to-1 force readers across four files to trace one operation while hiding nothing. Collapse layers that enforce no invariant or policy of their own.
- Splitting one cohesive task by execution order (`Reader`, `Validator`, `Writer`) forces all three pieces to share knowledge of intermediate shapes and ordering rules. Group code around the invariant or data representation it owns instead of chronological steps.
- Duplicating knowledge of a wire format, SQL layout, cache key format, or retry rule across two modules creates silent breakage whenever one side changes; give each representation rule one authoritative owner.
- Exposing internal buffer sizes, retry knobs, and strategy flags on public constructors makes callers understand implementation internals; choose sensible defaults inside the module and expose only settings callers genuinely need to vary.
- Extracting a shared helper from two modules whose code looks similar by coincidence couples independent domain policies behind boolean flags; ten clear lines in each module beat a flag-ridden shared helper.
- Exporting private helpers or internal fields solely for unit tests locks tests to internal structure; test through the module's behavioral contract or keep invariant tests inside module-private scope.
