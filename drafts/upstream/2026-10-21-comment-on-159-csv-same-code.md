# OBSOLETE — do not post: the CSV reader was fixed together with #159 in #161 (baf4768)

(Kept as a record. Original draft below.)

Additional information: the CSV reader has the same code, and it panics in the same way.

- `crates/terrio/src/drivers/vector/csv.rs:587` has `is_date(&s[..10])` after a byte-length check, like `geojson.rs`.
- Reproduction (terrio 0.3.2, tag `v0.3.2`):

```sh
printf 'x,y,name\n139.7,35.7,東京都千代田区\n' > t.csv
terrio info t.csv        # panicked at crates/terrio/src/drivers/vector/csv.rs:587:22
```

- `札幌市北区` (15 bytes) works; `東京都千代田区` (21 bytes) panics. `terrio convert` and Python `terrio.open_vector` fail the same way.

So a fix may be needed in both places (or in a shared `is_datetime` helper). A related case, with a different code path, is reported separately: relative paths such as `日本地図.tif` panic in `zarr.rs` (`parse_name`).
