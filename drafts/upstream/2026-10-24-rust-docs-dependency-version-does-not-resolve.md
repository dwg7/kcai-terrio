# Draft issue for opengeos/terrio (not posted; hfu will review and post)

**Title:** docs/rust.md: `terrio = { version = "0.3", default-features = false, features = ["geotiff"] }` does not resolve (the `geotiff` feature starts in 0.4)

Hello, and thank you for terrio. A small documentation thing I found while trying the Rust page.

## Version

Checked 2026-10-24 with cargo 1.97 against crates.io (terrio 0.5.0 is the latest). The same line is in `docs/rust.md` at v0.5.0 and on main (`8598e4a`).

## Reproduction

```toml
# Cargo.toml (an empty `fn main() {}` crate)
[dependencies]
terrio = { version = "0.3", default-features = false, features = ["geotiff"] }
```

```sh
cargo generate-lockfile
# error: failed to select a version for `terrio` ...
#   package `rr` depends on `terrio` with feature `geotiff` but `terrio` does not have that feature.
#   available features: default, gdal
```

`version = "0.3"` can only pick 0.3.x, and those releases have only the features `default` and `gdal`. With `version = "0.4"` the same dependency resolves (to 0.4.2 at that time):

```toml
terrio = { version = "0.4", default-features = false, features = ["geotiff"] }
```

## Suggestion

Update the example in `docs/rust.md` to the current minor version (or `"0.5"`). It might also help to say that the features exist from 0.4.0.

Thank you for your work. I hope this is useful.
