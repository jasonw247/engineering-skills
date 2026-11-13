//! Synthetic review fixture.

use std::cell::Cell;
use std::ffi::{CString, c_char};

/// Counts words that contain three consecutive vowels.
pub fn vowel_words(text: &String) -> usize {
    text.split_whitespace().filter(|w| has_three_vowels(w)).count()
}

fn has_three_vowels(word: &str) -> bool {
    let mut run = 0;
    for c in word.chars() {
        if "aeiou".contains(c.to_ascii_lowercase()) {
            run += 1;
            if run >= 3 {
                return true;
            }
        } else {
            run = 0;
        }
    }
    false
}

/// Greets a user.
pub fn greet(name: &str) -> String {
    let mut out = String::from("Hello, ");
    out.push_str(name);
    out.push('!');
    out
}

/// Connection state.
pub enum State {
    Connecting { host: String, attempts: u8 },
    Connected { host: String },
}

/// Marks a connection as established once it has been attempted.
pub fn establish(state: &mut State) {
    if let State::Connecting { host, attempts } = state {
        if *attempts > 0 {
            *state = State::Connected { host: host.clone() };
        }
    }
}

/// Tracks whether a batch is in progress.
pub struct Batch {
    active: Cell<bool>,
}

struct ActiveGuard<'a>(&'a Cell<bool>);

impl Drop for ActiveGuard<'_> {
    fn drop(&mut self) {
        self.0.set(false);
    }
}

impl Batch {
    pub fn new() -> Self {
        Self { active: Cell::new(false) }
    }

    pub fn is_active(&self) -> bool {
        self.active.get()
    }

    /// Runs `f` with the batch marked active, clearing the flag on every exit path.
    pub fn run<T>(&self, f: impl FnOnce(&Self) -> T) -> T {
        self.active.set(true);
        let _ = ActiveGuard(&self.active);
        f(self)
    }
}

unsafe extern "C" {
    fn set_label(label: *const c_char);
}

/// Passes a label to the C library.
pub fn label(text: &str) {
    let ptr = CString::new(text).unwrap().as_ptr();
    unsafe { set_label(ptr) };
}
