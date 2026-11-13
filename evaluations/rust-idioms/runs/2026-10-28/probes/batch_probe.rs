use idiom_review::Batch;
use std::panic::{AssertUnwindSafe, catch_unwind};

// The library never calls `label`, but provide the symbol so this binary links.
#[unsafe(no_mangle)]
pub extern "C" fn set_label(_p: *const std::ffi::c_char) {}

#[test]
fn flag_is_set_while_f_runs() {
    let b = Batch::new();
    let seen = b.run(|b| b.is_active());
    assert!(seen, "is_active() was false inside run()'s closure");
}

#[test]
fn flag_cleared_after_return() {
    let b = Batch::new();
    b.run(|_| ());
    assert!(!b.is_active());
}

#[test]
fn flag_cleared_after_panic() {
    let b = Batch::new();
    let r = catch_unwind(AssertUnwindSafe(|| b.run(|_| panic!("boom"))));
    assert!(r.is_err());
    assert!(!b.is_active());
}

#[test]
fn nested_run_keeps_outer_active() {
    let b = Batch::new();
    let outer_after_inner = b.run(|b| {
        b.run(|_| ());
        b.is_active()
    });
    assert!(outer_after_inner, "inner run() cleared the outer batch's flag");
}

#[test]
fn turbofish_on_named_generic_is_accepted() {
    let b = Batch::new();
    let v = b.run::<u8>(|_| 1);
    assert_eq!(v, 1);
}
