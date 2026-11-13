//! Synthetic review fixture.

use std::cell::Cell;
use std::ffi::{CString, NulError, c_char};

/// Counts words that contain three consecutive vowels.
pub fn vowel_words(text: &str) -> usize {
    text.split_whitespace()
        .filter(|w| has_three_vowels(w))
        .count()
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
#[derive(Debug)]
pub enum State {
    Connecting { host: String, attempts: u8 },
    Connected { host: String },
}

/// Marks a connection as established once it has been attempted.
pub fn establish(state: &mut State) {
    if let State::Connecting { host, attempts } = state
        && *attempts > 0
    {
        *state = State::Connected {
            host: std::mem::take(host),
        };
    }
}

/// Tracks whether a batch is in progress.
#[derive(Debug, Default)]
pub struct Batch {
    active: Cell<bool>,
}

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

impl Batch {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn is_active(&self) -> bool {
        self.active.get()
    }

    /// Runs `f` with the batch marked active, clearing the flag on every exit path.
    pub fn run<T>(&self, f: impl FnOnce(&Self) -> T) -> T {
        let previous = self.active.replace(true);
        let _guard = ActiveGuard {
            active: &self.active,
            previous,
        };
        f(self)
    }
}

unsafe extern "C" {
    fn set_label(label: *const c_char);
}

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
