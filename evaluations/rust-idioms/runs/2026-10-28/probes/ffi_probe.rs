use std::alloc::{GlobalAlloc, Layout, System};
use std::ffi::{CStr, c_char};
use std::sync::Mutex;

// Poisoning allocator: on dealloc, overwrite the block with '#' and a final NUL,
// and leak it, so reading a freed CString shows "###..." instead of the label.
struct Poison;
unsafe impl GlobalAlloc for Poison {
    unsafe fn alloc(&self, l: Layout) -> *mut u8 {
        unsafe { System.alloc(l) }
    }
    unsafe fn dealloc(&self, p: *mut u8, l: Layout) {
        unsafe {
            std::ptr::write_bytes(p, b'#', l.size());
            if l.size() > 0 {
                *p.add(l.size() - 1) = 0;
            }
        }
    }
}
#[global_allocator]
static A: Poison = Poison;

static SEEN: Mutex<Vec<u8>> = Mutex::new(Vec::new());

// Stand-in for the C library: copies the string during the call.
#[unsafe(no_mangle)]
pub extern "C" fn set_label(p: *const c_char) {
    let bytes = unsafe { CStr::from_ptr(p) }.to_bytes().to_vec();
    *SEEN.lock().unwrap() = bytes;
}

#[test]
fn c_receives_the_label() {
    idiom_review::label("hello");
    let seen = String::from_utf8_lossy(&SEEN.lock().unwrap()).into_owned();
    assert_eq!(seen, "hello", "C side read freed memory: {seen:?}");
}

#[test]
fn interior_nul_is_an_input_error_not_a_panic() {
    let r = std::panic::catch_unwind(|| idiom_review::label("a\0b"));
    assert!(r.is_ok(), "label() panicked on input containing a NUL byte");
}
