# Draft issue for opengeos/terrio (not posted; hfu will review and post)

**Title:** Panic when a dataset path has a multi-byte character across byte 5 (e.g. a relative path like `日本地図.tif`) — `zarr::parse_name` slices `&str` at byte 5

Hello, and thank you for terrio. While trying it with Japanese file names I found a panic that is easy to hit, so I would like to report it. (It is the same kind of problem as #159, which was fixed in #161 — thank you for the quick fix! — but in a different place: slicing a `&str` at a fixed byte index.)

## Version

- terrio 0.3.2 (`pip install terrio`, Linux x86_64, Python 3.13)

**Rechecked 2026-10-24 (0.5.0):** terrio 0.5.0 (PyPI wheel, 2026-10-24): `terrio info` of a relative path that starts with Japanese still panics; `t[..5]` is still in the source (v0.5.0).

**Rechecked 2026-10-24 (0.4.2):** terrio 0.4.2 (PyPI wheel): `terrio info 日本語/a.zarr` and `./日本語/a.zarr` still panic at `zarr.rs:1310` (line 1437 on main 17ca35a); absolute paths work.
- Source checked at tag `v0.3.2` (`a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6`). Re-checked on main at `6779102281ad2835cbc23fba3138e01a138bc6f9` (2026-10-21, after #161): still panics.

## What happens

Opening a **relative** path whose 5th byte falls inside a multi-byte character panics, for any format, because every path is first tried as a Zarr name.

```
thread '<unnamed>' panicked at crates/terrio/src/drivers/zarr.rs:1310:24:
end byte index 5 is not a char boundary; it is inside '本' (bytes 3..6 of string)
```

## Reproduction

```sh
terrio convert some.png ascii.tif        # any small GeoTIFF
cp ascii.tif 日本地図.tif
terrio info 日本地図.tif                  # panic
terrio info "$PWD/日本地図.tif"           # works (the first bytes are ASCII)
```

| path | result |
|---|---|
| `ascii.tif` | works |
| `日本地図.tif`, `地図.tif`, `標高.tif`, `データ/x.tif`, `a地図.tif` | panic |
| `ab地図.tif`, `地.tif`, `/tmp/…/日本地図.tif` | works |

The rule seems to be: panic when byte 5 is not on a character boundary (and the path is longer than 5 bytes).
Python `terrio.open_raster('日本地図.tif')` raises `pyo3_runtime.PanicException` (derived from `BaseException`, so `except Exception` does not catch it).

## Likely cause

`crates/terrio/src/drivers/zarr.rs`, `parse_name`:

```rust
if t.len() > 5 && t[..5].eq_ignore_ascii_case("ZARR:") {
```

`t[..5]` panics when byte 5 is inside a character. A possible fix is `t.as_bytes()[..5].eq_ignore_ascii_case(b"ZARR:")` or `t.get(..5).is_some_and(|p| p.eq_ignore_ascii_case("ZARR:"))`.

## Why it matters

In Japan, file and directory names in Japanese are common, and relative paths are the usual way to call a command line tool. Thank you for considering this.

## Related

- `png.rs` `read_world_file` also slices `&ext[..1]` on a lowercased extension; I could not trigger it (unknown extensions are rejected before), so this is only a note for a look.
