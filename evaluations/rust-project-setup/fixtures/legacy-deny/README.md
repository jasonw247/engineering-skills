# Synthetic fixture: legacy cargo-deny configuration

A single-crate library whose CI began failing after cargo-deny was upgraded. The error reported in CI was:

    error[unexpected-value]: expected '["all", "workspace", "transitive", "none"]'
      ┌─ deny.toml:4:16
      │
    4 │ unmaintained = "warn"

The project deliberately uses cargo-machete and `RUSTFLAGS=-Dwarnings`; neither is part of this request.
