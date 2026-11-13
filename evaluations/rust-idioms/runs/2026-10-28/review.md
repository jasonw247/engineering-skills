# Idiom review: `idiom-review` (`src/lib.rs`)

Four problems have real consequences. Two are correctness bugs: undefined behavior at the FFI call, and a guard that drops too early. Two are API problems: a panic on ordinary input, and a parameter type that turns away `&str` callers. One small gap is cheap to close (missing `Default`/`Debug`). Everything else in the file is style, and since the library is not performance-sensitive, I list it at the end without asking for changes.

Each finding below was checked with a probe on a copy in `scratch/`. A patched copy (`scratch/fixed/src/lib.rs`) passes every probe and is Clippy- and rustfmt-clean on Rust 1.92.0 (stable) and 1.99.1.

## Findings

### 1. High: `label` hands C a dangling pointer (undefined behavior)

`src/lib.rs:85-86`

```rust
let ptr = CString::new(text).unwrap().as_ptr();
unsafe { set_label(ptr) };
```

The `CString` is a temporary, so it is freed at the end of the `let` statement. `set_label` then reads freed memory. rustc already warns about this (`dangling_pointers_from_temporaries`), but the warning has been left in place.

**Evidence:** I wrote a test stand-in for `set_label` that copies the string, and used an allocator that overwrites freed blocks. With those, `label("hello")` delivered `"#####"` to the C side.

**Fix:** bind the `CString` to a named variable that outlives the call, and write down the assumption the `unsafe` block depends on (it has no `// SAFETY:` comment now). The combined fix is under finding 3.

**Open question about the C contract:** a local variable is only enough if `set_label` reads the string during the call. The name suggests it may keep the pointer. If it does, the Rust side has to keep the `CString` alive for as long as C uses it, for example by holding the current label in Rust-owned state and replacing it only after C has the new one. The other option is to hand ownership over with `CString::into_raw`, paired with a Rust-exported free function. Check the C library's documentation before choosing.

### 2. High: `Batch::run` drops its guard at once, so the batch is never active while `f` runs

`src/lib.rs:73-75`

```rust
self.active.set(true);
let _ = ActiveGuard(&self.active);
f(self)
```

`let _ = expr` does not bind anything, so the guard is dropped at the end of that statement. That resets the flag to `false` before `f` runs. As a result, `batch.run(|b| b.is_active())` returns `false`, which contradicts the doc comment ("Runs `f` with the batch marked active"). The flag does end up `false` after a return or a panic, but only because it was already cleared before `f` started. Neither rustc nor Clippy flags this with default lints. The allow-by-default rustc lint `let_underscore_drop` does catch it.

**Fix:** use a named binding (`let _guard = …`) so the guard lives until the end of the scope.

**A related problem the one-line fix leaves in place:** `f` receives `&Self`, so it can call `run` again. A guard that always writes `false` clears the flag when the inner `run` returns, while the outer one is still running. My nested-run probe still fails with only `let _guard`. Restoring the previous value fixes both problems:

```rust
/// Restores the flag to its value from before `run` began.
struct ActiveGuard<'a> {
    active: &'a Cell<bool>,
    previous: bool,
}

impl Drop for ActiveGuard<'_> {
    fn drop(&mut self) {
        self.active.set(self.previous);
    }
}

pub fn run<T>(&self, f: impl FnOnce(&Self) -> T) -> T {
    let previous = self.active.replace(true);
    let _guard = ActiveGuard { active: &self.active, previous };
    f(self)
}
```

A guard is the right tool here. The flag is in-memory state, not essential finalization, so it does not matter that destructors are skipped on abort.

### 3. Medium: `label` panics on input that contains a NUL byte

`src/lib.rs:85`

`CString::new(text).unwrap()` panics for any `&str` that contains `\0`, so the caller's own input can crash the process. In the probe, `label("a\0b")` panicked at `src/lib.rs:85:34`. An interior NUL is an input error and should come back as an error. Together with finding 1:

```rust
/// Passes `text` to the C library as its label.
///
/// # Errors
///
/// Returns the [`NulError`] from [`CString::new`] if `text` contains a NUL byte.
pub fn label(text: &str) -> Result<(), NulError> {
    let text = CString::new(text)?;
    // SAFETY: `text` is NUL-terminated and outlives the call; `set_label` reads
    // the string during the call and does not keep the pointer.
    unsafe { set_label(text.as_ptr()) };
    Ok(())
}
```

`NulError` is a concrete error type that reports the NUL's position and gives back the bytes (`into_vec`), so callers can recover. **API impact:** the signature changes. An existing `label(x);` statement still compiles, but it now gets an `unused_must_use` warning. Code that uses `label` as an `fn(&str)` value breaks. Treat this as a breaking change (0.2 to 0.3); with `publish = false`, that only affects callers inside this repository.

### 4. Medium: `vowel_words(&String)` rejects callers that hold a `&str`

`src/lib.rs:7`

The function only reads its input, but `&String` rejects string literals, slices of larger buffers, and `&str` parameters. A probe calling `vowel_words(slice)` with `slice: &str` failed with `E0308: expected &String, found &str`. Today those callers have to allocate a `String` just to make the call. Change the parameter to `text: &str`. This is source-compatible: `&String` arguments still coerce, and in the probe both kinds of call compiled and returned the same count. Clippy reports it (`ptr_arg`).

## Minor (small consequence, cheap to fix)

- **`Batch` has `new()` but no `Default`, and neither `Batch` nor `State` implements `Debug`.** Downstream types that contain them cannot `#[derive(Default)]` or `#[derive(Debug)]`, and callers cannot `{:?}` or `dbg!` a `State`. Clippy reports the first (`new_without_default`); the allow-by-default lint `missing_debug_implementations` reports the second. Fix: `#[derive(Debug, Default)]` on `Batch`, with `new` returning `Self::default()`, and `#[derive(Debug)]` on `State`.

## Considered and not flagged (style only here)

- **`establish` clones `host` to get around the borrow** (`src/lib.rs:44`). The old state is overwritten immediately, so the copy cannot drift from the original, and the cost is one allocation in code that is not hot. If someone touches the function anyway, the idiomatic form moves the string out with `host: std::mem::take(host)`. Clippy's `collapsible_if` on the same block is also style (its let-chain suggestion needs Rust 1.88+, which edition 2024 toolchains here have).
- **`greet` uses `String::from` + `push_str` + `push`.** `format!("Hello, {name}!")` reads better, but the behavior is the same.
- **`"aeiou".contains(c.to_ascii_lowercase())`** in `has_three_vowels` could be a `matches!`. This is purely style.
- **`run` takes `impl FnOnce(&Self) -> T`.** The `impl Trait` limit costs nothing here: callers can still turbofish `T` (`b.run::<u8>(|_| 1)` compiles), and nobody needs to name the closure type.
- **`State` is not `#[non_exhaustive]`.** That is fine. Adding a variant is a major-version change, which is the default way to evolve a type, and `State` does not mirror an external enum.
- **The file is not rustfmt-clean** (two over-long expressions). Running `cargo fmt` fixes it.

## Verification

Probes were run on a copy in `scratch/pkg`. `work/` and `skill/` were not modified (checked against `inputs.sha256`).

| Probe | Original | Patched (`scratch/fixed`) |
| --- | --- | --- |
| `run(\|b\| b.is_active())` is `true` | fails (`false`) | passes |
| flag is `false` after `run` returns / panics | passes | passes |
| nested `run` keeps the outer batch active | fails (also fails with only `let _guard`) | passes |
| `b.run::<u8>(…)` compiles | passes | passes |
| C side receives `"hello"` from `label("hello")` | fails (`"#####"`, freed memory) | passes |
| `label("a\0b")` returns an error, not a panic | fails (panic at `lib.rs:85:34`) | passes (`nul_position() == 1`) |
| `vowel_words(&str)` and `vowel_words(&String)` compile | `&str` call fails (E0308) | both pass |
| Clippy, default lints, `--lib` (1.92.0 and 1.99.1) | 3 Clippy warnings + 1 rustc warning | clean |
| Clippy with `let_underscore_drop`, `undocumented_unsafe_blocks`, `missing_debug_implementations` | 8 warnings | clean |
| `cargo fmt --check` | 2 diffs | clean |
