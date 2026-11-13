# Ownership and API idioms

| Situation | Idiom | Limit |
| --- | --- | --- |
| Choosing a parameter type | Borrow the view (`&str`, `&[T]`, `&Path`) when the function only reads; take ownership when it stores or consumes the value. Use `impl Trait` for a single-use generic parameter. | Callers cannot name an `impl Trait` parameter's type with a turbofish; a public function whose callers may need to name it keeps a named generic for that parameter. |
| An owning type with a natural borrowed view | Implement `Deref` to the view, so methods live on the view and both forms get them, as `Vec`/`[T]` and `String`/`str` do. | Only for that owner/view relation. `Deref` used for inheritance surprises readers and carries no trait implementations. |
| Constructing values | A `new` associated function; `Default` too when an empty value is meaningful. Use a builder for many optional settings ([design patterns](design-patterns.md)). | One `Default` per type, and only a meaningful one. |
| A public struct callers fill in (configuration, request data) | Public fields plus `Default`, so callers write `Config { retries: 3, ..Default::default() }`. Constructors or a builder for types with invariants. | `#[non_exhaustive]` forbids struct literals in other crates, `..Default::default()` included; pair it with setters or a builder. |
| Moving a field out of `&mut self` or a matched enum | `mem::take`, `mem::replace`, or `Option::take`, then rebuild the value. | `take` needs `Default`; `replace` works otherwise. |
| A borrow-checker conflict | Restructure first: move out with the row above, pass only the fields a function needs, or split the struct so fields borrow independently. | A clone is fine when deliberate: the copy is meant to diverge, the code is cold, or the restructuring costs more clarity than it saves. `Rc`/`Arc` clones share; they do not copy. |
| A manual `PartialEq`, `Ord`, `Hash`, `Debug`, or serialization impl | Destructure `self` exhaustively (`let Self { a, b, cache: _ } = self;`), so a newly added field forces a decision. | Most valuable for internal types that change often. |
| Data from a remote API or file format | Deserialize into wire types local to the adapter function or module, then convert into domain types. | When the wire shape and the domain coincide and both are under your control, one type serves. |
| A fallible function that consumes its argument | Return the argument inside the error, so callers can retry or fall back without cloning (`String::from_utf8` → `FromUtf8Error::into_bytes`). | Costs a richer error type; worth it when retry or fallback is realistic. |
| Code that must run on every exit path, including `?` and panics | A guard type with `Drop`, held in a named binding (`let _guard = …`) until the scope ends. A guard over shared state restores the previous value (`let previous = cell.replace(true);`) rather than writing a fixed one, so nested and reentrant use stays correct. | Guard code stays panic-free; see the destructor trap in the skill. |
| A branch picks one of several types and the code after it is not hot | Bind `&mut dyn Trait` from the branches: `let r: &mut dyn Read = if … { &mut stdin() } else { &mut File::open(p)? };`. | Rust ≥ 1.79 (temporary lifetime extension). Generics stay the default on hot paths. |
| A `move` closure needing a clone of one variable and a borrow of another | Rebind them in a block that returns the closure, keeping the original names. | One extra indentation level. |
| Leaving room to extend a public type | A major-version bump. `#[non_exhaustive]` for types mirroring something that changes independently of the crate (protocol codes, platform errors). | `#[non_exhaustive]` restricts only other crates, and it forces downstream wildcard arms that rarely have a sensible action. A hidden private field works within the crate; default Clippy flags it (`manual_non_exhaustive`), so `#[expect]` it with a reason. |
| Doc examples needing heavy setup | Hide setup lines with `#`; add a `#[doc(hidden)]` constructor when setup is long. | An example wrapped in an uncalled `fn` compiles but runs no assertions; reserve it for cases that would otherwise need `no_run`. |

## Names and doc comments

- Name by role in context (`haystack`, `needle`), with one name per concept, one word order across the API, and no type names inside variable names. Public names are the hardest to change; spend the most care there.
- Pattern bindings keep the field's name (`State::Evaluating { workload, .. }`).
- When a signature has several lifetimes, name them after the borrowed data (`'cursor`, `'tree`), and reuse a name wherever the same data appears.
- A doc comment's first sentence says when to use the item, and refers to parameters by name.
