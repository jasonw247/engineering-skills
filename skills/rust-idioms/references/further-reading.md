# Further reading

A topic-sorted selection from Matthias Endler's *idiomatic-rust* list (CC0). These are pointers, not imported guidance: the linked material was not read or verified at extraction. Check an article's date against the crate's edition before following it. Some links in the list go to archived copies.

## Reference collections

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/): the rust-lang checklist for public library APIs (naming, common traits, conversions, future-proofing).
- [Clippy](https://github.com/rust-lang/rust-clippy): lint documentation; each lint page explains its idiom.
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/): distilled into this skill (see [sources](sources.md)); the original has fuller examples.
- [Canonical's Rust Best Practices](https://canonical.github.io/rust-best-practices/): one organization's house style. The skill links to it rather than restating it; [Canonical guide notes](canonical-notes.md) records its tooling corrections.
- [Elements of Rust](https://github.com/ferrous-systems/elements-of-rust): broader style and engineering conventions.

## Strings and arguments

- [When should I use String vs &str?](https://steveklabnik.com/writing/when-should-i-use-string-vs-str/) (Klabnik, 2024)
- [Taking string arguments in Rust](http://xion.io/post/code/rust-string-args.html) (2019)
- [Are out parameters idiomatic in Rust?](https://steveklabnik.com/writing/are-out-parameters-idiomatic-in-rust/) (2020)
- [Preferred way of passing `Path`-like types around?](https://www.reddit.com/r/rust/comments/cekeq9/preferred_way_of_passing_pathlike_types_around/) (forum, 2020)

## Errors and panics

- [Error Handling in Rust](https://burntsushi.net/rust-error-handling/) (BurntSushi, 2015)
- [Designing Error Types in Rust Libraries](https://d34dl0ck.me/rust-bites-designing-error-types-in-rust-libraries/index.html) (2025)
- [Context-preserving error handling](https://kazlauskas.me/entries/errors) (2020)
- [To panic or not to panic](https://www.ncameron.org/blog/to-panic-or-not-to-panic/) (2025)
- [Three Kinds Of Unwrap](https://zkrising.com/writing/three-unwraps/) (2024)

## Types and conversions

- [The Ultimate Guide to Rust Newtypes](https://www.howtocodeit.com/articles/ultimate-guide-rust-newtypes) (2024)
- [Rust Patterns: Enums Instead Of Booleans](https://blakesmith.me/2019/05/07/rust-patterns-enums-instead-of-booleans.html) (2019)
- [Pretty State Machine Patterns in Rust](https://hoverbear.org/2016/10/12/rust-state-machine-pattern/) (2016)
- [Convenient and idiomatic conversions in Rust](https://ricardomartins.cc/2016/08/03/convenient_and_idiomatic_conversions_in_rust) (2016)
- [Rust Number Conversion: Don't Follow the Book...](https://blog.notmet.net/2021/12/rust-number-conversion-dont-follow-the-book.../) (2021)
- [Idiomatic tree and graph like structures in Rust](https://rust-leipzig.github.io/architecture/2016/12/20/idiomatic-trees-in-rust/) (arenas, 2016)

## Iterators, Option, and Result

- [Iteration patterns for Result & Option](http://xion.io/post/code/rust-iter-patterns.html) (2017)
- [Rust Iterators Beyond the Basics](https://blog.jetbrains.com/rust/2024/03/12/rust-iterators-beyond-the-basics-part-i-building-blocks/) (2024)
- [Level Up your Rust pattern matching](https://blog.cuongle.dev/p/level-up-your-rust-pattern-matching) (2025)

## Simplicity and pitfalls

- [Be Simple](https://corrode.dev/blog/simple/) and the talk [The Four Horsemen of Bad Rust Code](https://github.com/corrode/four-horsemen-talk) (2024–25): over-engineering and premature optimization.
- [Pitfalls of Safe Rust](https://corrode.dev/blog/pitfalls-of-safe-rust/) and [Patterns for Defensive Programming in Rust](https://corrode.dev/blog/defensive-programming/) (2025)
- [Don't Worry About Lifetimes](https://corrode.dev/blog/lifetimes/) (2024)
- [Rust's Sneaky Deadlock With if let Blocks](https://brooksblog.bearblog.dev/rusts-sneaky-deadlock-with-if-let-blocks/) (2024). Edition 2024 shortened the lifetime of `if let` scrutinee temporaries, so check which edition the hazard applies to.
- [Cancelling async Rust](https://sunshowers.io/posts/cancelling-async-rust/) (cancel safety, 2025)

## Library APIs and documentation

- [Elegant Library APIs in Rust](https://deterministic.space/elegant-apis-in-rust.html) (2016)
- [Teaching libraries through good documentation](https://deterministic.space/teaching-libraries.html) (2016)
- [Guide on how to write documentation for a Rust crate](https://blog.guillaume-gomez.fr/articles/2020-03-12+Guide+on+how+to+write+documentation+for+a+Rust+crate) (2020)

The full list, with books, workshops, and talks, is at [corrode.dev/idiomatic-rust](https://corrode.dev/idiomatic-rust/).
