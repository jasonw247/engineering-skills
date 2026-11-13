# Design patterns

Apply a pattern only for a current need. Rust's traits, closures, enums, and ownership make many classic patterns unnecessary, and an unneeded pattern adds interface without adding depth.

## Newtype

A single-field tuple struct (`struct Meters(f64);`, `struct Password(String);`) creates a distinct type rather than an alias.

- **Use for:** distinguishing units or identifiers, enforcing an invariant at construction, overriding behavior such as `Display` for a secret, restricting which operations are exposed, or hiding an implementation type so it can change compatibly.
- **Cost:** every method and trait you want to expose needs a pass-through, so a newtype without an invariant or a distinct meaning is boilerplate.
- `.0` access is normal inside a newtype's own `impl`. Elsewhere, prefer named fields or destructuring over numeric tuple indexing.

## Builder

Use a builder when a type would otherwise need many constructors or many optional settings, or when construction has side effects.

- Make it discoverable from the target type: `Foo::builder() -> FooBuilder`, finishing with `build()`. `build()` returns a `Result` when validation can fail.
- **By-value methods** (`fn bar(mut self, …) -> Self`) give simple chained construction and let `build(self)` move values without cloning.
- **`&mut self` methods** make conditional configuration easier (`if x { b.bar(..); }`), but `build(&self)` must then clone. A reusable `build(&self)` makes the builder closer to a factory, which can be the point (`std::process::Command`).
- Choose one receiver style per builder; follow the crate's precedent. Derive crates such as `derive_builder` remove the boilerplate if the project already uses them.

## Guards (RAII)

Tie a resource's release to a guard's `Drop`, and expose access to the resource only through the guard (`MutexGuard` style), so the borrow checker prevents use after release. `Deref` on the guard is ergonomic but optional; a `get` method works too. The limits of destructors apply (see the cleanup row in the skill).

## Typestate and marker generics

When callers know statically which variant or state they hold, split the API with a type parameter (`Request<Nfs>` vs `Request<Bootp>`, `Pin<Output>`): common methods go in `impl<P> …`, state-specific methods in `impl Request<Nfs>`. Callers lose the `Option` checks and runtime mismatch errors, and transitions that consume `self` (`fn connect(self) -> Conn<Connected>`) make invalid sequences fail to compile.

- **Cost:** more types in signatures and docs, and monomorphization increases binary size.
- If the split exists only because of partial initialization, use a builder. If only behavior differs and the API is the same, use a trait or a closure (strategy).
- Keep the marker trait in a private module when outside crates must not add states.

## Splitting a struct for independent borrows

When one field is borrowed mutably while a function needs read access to the rest, pass the fields the function needs, or group fields into smaller structs that can be borrowed separately. If the resulting pieces are not meaningful abstractions, prefer passing fields rather than inventing types.

## Custom traits for unwieldy bounds

When the same complex bound recurs, especially one involving `Fn` traits with specific outputs, define a named trait with a blanket impl (`impl<F: FnMut() -> Result<T, E>, T> Getter for F`). The bound becomes readable and can drop a type parameter. Cost: one more item to discover; document that a plain closure satisfies it.

## Strategy and command

A trait with an implementation per variant, or simply a closure parameter, replaces the strategy pattern. For queued or undoable operations (commands):

- `fn` pointers or generic closures when commands are small and stateless (static dispatch);
- `Box<dyn Fn…>` when commands capture state and are stored heterogeneously;
- a trait object (`Box<dyn Command>`) when each command carries several operations (`execute`, `rollback`) and its own data.

An enum is often simpler than all three when the set of commands is closed.

## Visitor and fold over trees

For heterogeneous trees such as ASTs, a `Visitor` trait with `visit_*` methods and free `walk_*` functions separates traversal from the operation, so several analyses share one traversal and override only the nodes they care about. A fold (`fold_*` methods returning new nodes) does the same while producing a transformed tree. Taking `Box` nodes reuses unchanged nodes but consumes the input; taking references keeps the input but clones; `Rc` nodes allow both at the cost of mutability. For homogeneous collections, iterators suffice.

## Containing unsafe

Put `unsafe` code in the smallest module that can uphold its invariants, expose a safe interface from it, and build ergonomic code on top. Only the inner module needs audit. `String` over `Vec<u8>` is the model: safe methods maintain UTF-8, and the `unsafe` constructors move the obligation to the caller. Keep each `unsafe` block small with a `// SAFETY:` comment stating the invariant relied on. "It is faster" justifies `unsafe` only with profiling that shows the safe version's cost matters.

## Crate granularity

Small, focused crates compile in parallel, encourage modular code, and can be reused. Within your own workspace, splitting by responsibility is usually worth it. For third-party crates, each dependency adds supply-chain exposure, version-duplication risk (two major versions' types do not interoperate), and maintenance uncertainty. Weigh a small dependency against writing the few lines yourself.
