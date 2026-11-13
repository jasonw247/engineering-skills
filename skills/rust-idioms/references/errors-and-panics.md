# Errors and panics

## Choosing an error type

- **Libraries:** return concrete error types (an enum or struct, commonly derived with `thiserror`) so callers can match on the cases they handle. Type-erased errors (`Box<dyn Error>`, `anyhow::Error`) belong at application boundaries; callers of a library cannot reliably recover a concrete type from them.
- **Applications:** a single erased report type at the top level is the common convention. Canonical's guide goes further and asks for concrete types everywhere except prototypes. Follow the repository's existing choice, and use one application-level report type.
- When a dependency's error type would leak implementation details into a public API, wrap it in an opaque type (a public `struct InternalError(Inner)` with a private inner enum) rather than exposing the dependency's type.
- Design the crate's `Error` early. Writing its variants shows which context (path, identifier, input) must be carried to the point where the error is detected.

## Wrapping without duplication

An error that wraps another should either print the inner error in its own message or return it from `Error::source()`, not both. Chain-walking reporters (`anyhow`'s `{:#}`, logging integrations) print every `source()` after the outer message, so doing both prints the inner message twice.

`thiserror` treats a field named `source`, or marked `#[source]` or `#[from]`, as the source. So `#[error("cannot access {path}: {source}")]` with a `source` field duplicates it:

```rust
#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("cannot access {path}")]          // inner message reached via source()
    Access { path: PathBuf, source: io::Error },
}
```

Convert a foreign error into the crate's error at the call that produced it (`Url::parse(&s).map_err(|source| Error::BadUrl { var, source })?`), not after a chain of combinators where it is unclear which step failed. Converting early keeps the crate speaking one error language internally.

## Messages

- Concise and consistent in form; a common pattern is "cannot <verb> <object>".
- Start lowercase and omit trailing punctuation, since messages are often embedded after a colon in a chain. Keep the standard capitalization of acronyms and proper names.
- Write for the actual reader: precise detail for developers using a library, and guidance on what to do next for end users of an application.
- Add context once per layer, and check the full chain for repetition.

## Panics

- Panic only for states the program cannot recover from that no input can cause. A panic reachable from user input, a file, or the network is a bug: return an error.
- A panic is not a cleanup path: with `panic = "abort"`, destructors never run.
- Replace `unwrap` with `?` (using `ok_or`/`ok_or_else` to turn an `Option` into an error), with `if let`/`let … else`, or with a type that makes the invalid state unrepresentable. Where a panic is genuinely an invariant, use `expect("…")` stating the invariant. Some teams prefix internal-fault messages with `internal error:` so the fault is clearly not the user's.
- `unwrap` on a value that can only fail through a programmer mistake (a literal regex, a constant parse) is acceptable in a tiny scope.
- Tests may `unwrap`: a failure points at the line, whereas `?` in a test can lose the error's origin unless backtraces are captured.
- `lock().unwrap()` on a `Mutex` propagates a panic that already happened in another thread (poisoning); that is an accepted use.
