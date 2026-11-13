//! Fixture library.

/// Returns the input doubled.
///
/// ```
/// assert_eq!(legacy_deny::double(2), 4);
/// ```
#[must_use]
pub fn double(x: u32) -> u32 {
    x * 2
}
