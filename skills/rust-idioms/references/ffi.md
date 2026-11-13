# FFI idioms

Keep the `unsafe` surface small, make every pointer's lifetime and ownership explicit, and keep the Rust-side API idiomatic, translating at the boundary.

## Edition 2024 syntax

Under Edition 2024, `extern` blocks are written `unsafe extern "C" { … }`, exported symbols use `#[unsafe(no_mangle)]`, and unsafe operations inside an `unsafe fn` need their own `unsafe { … }` block (`unsafe_op_in_unsafe_fn` warns). Older examples, including much published guidance, use the pre-2024 forms and do not compile unchanged. Match the crate's edition.

## Panics

A panic that reaches an `extern "C"` function aborts the process; it cannot unwind into C, and a `catch_unwind` outside the boundary cannot intercept it. When the C API needs an error code instead of an abort, wrap the body in `std::panic::catch_unwind` inside the exported function and map the panic to an error code.

## Errors

- **Flat enums:** give each variant an explicit discriminant and convert it to the integer error code (`impl From<Error> for c_int`).
- **Enums carrying data:** return an integer code, and expose the detail through a separate description function.
- **Error structs:** mirror the struct as a `#[repr(C)]` type and convert with `From`, keeping the Rust type free of C-layout constraints.

Any string or buffer allocated for the caller needs a documented owner and a matching free function exported from the same library. Memory goes back to the allocator that produced it.

## Receiving strings from C

Borrow rather than copy, and convert in one small `unsafe` block:

```rust
use std::ffi::{CStr, c_char};

/// # Safety
/// `msg` must be non-null, point to a NUL-terminated string, and stay
/// unmodified for the duration of the call.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn mylib_log(msg: *const c_char) {
    // SAFETY: guaranteed by the caller, per the contract above.
    let msg = unsafe { CStr::from_ptr(msg) };
    let Ok(msg) = msg.to_str() else { return /* report invalid UTF-8 */ };
    crate::log(msg);
}
```

Document the caller's obligations in a `# Safety` section. Check for null explicitly if the API allows it. Hand-copying with `strlen`, `copy_nonoverlapping`, and `set_len` invites off-by-one errors around the NUL terminator, which can read uninitialized memory.

## Passing strings to C

- Bind the `CString` to a named variable that lives as long as C uses the pointer. A temporary inside the call expression (`f(CString::new(s)?.as_ptr())`) lives until the end of that statement. That is enough if C only reads during the call, and dangling if C keeps the pointer. `let p = CString::new(s)?.as_ptr();` dangles immediately; rustc warns about it (`dangling_pointers_from_temporaries`).
- Propagate `NulError` from `CString::new` rather than unwrapping it; interior NUL bytes are input errors.
- When C writes into a buffer, pass a `Vec<u8>` (modifying a `CString`'s contents through its pointer is undefined behavior). Read the result back up to the first NUL:

```rust
let mut buf = vec![0u8; 1024];
// SAFETY: geterr writes at most buf.len() bytes, including a NUL terminator.
unsafe { geterr(buf.as_mut_ptr().cast(), buf.len() as c_int) };
let msg = CStr::from_bytes_until_nul(&buf)?.to_str()?.to_owned();
```

- Keep ownership on the Rust side unless the C API requires a transfer. If it does, pair `CString::into_raw` with a Rust-exported function that calls `CString::from_raw` to free it.

## Shaping an exported API

- **Object-based design.** Stateful library types are opaque handles: Rust owns them, the caller manages them only through `create`/`destroy` functions, and the caller never sees their layout. Data exchanged with the caller uses transparent `#[repr(C)]` types that the caller owns. All behavior is functions taking the handle.
- **Group lifetimes into the parent handle.** Fold borrowing state, such as an iterator, into the parent handle. A separately exported borrowing handle can be used by C after its parent is destroyed, or while the parent is mutated, which is undefined behavior. The folded form is `first_key(db)` and `next_key(db)` on a wrapper holding the collection and a cursor. It costs expressiveness, such as one iteration at a time per object.
- **Wrapper types.** When several related Rust types must cross the boundary, consolidate them into one wrapper struct whose methods contain no `unsafe`. Re-creating a borrow on each call (for example, a stored index and `nth()`) is safer than storing a lifetime-erased borrow, which almost always ends in undefined behavior once another call takes `&mut` to the parent.
- Each function's documentation states which pointers it accepts (only those returned by this library, not after destroy) and who frees every returned allocation.
