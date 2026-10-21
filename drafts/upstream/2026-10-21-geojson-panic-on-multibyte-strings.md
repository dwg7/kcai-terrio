# Draft issue for opengeos/terrio (not posted; hfu will review and post)

**Title:** Panic reading GeoJSON and CSV with long non-ASCII string values (`is_datetime` slices a `&str` at byte 10)

Hello, and thank you for terrio. It is wonderful to see a pure-Rust GDAL-style tool grow so fast.
While trying it on Japanese data, I found a small problem and I would like to report it in case it is useful.

## Version

- terrio 0.3.2 (`pip install terrio`, Linux x86_64, Python 3.13)
- Source checked at `cf6bd5dbcb6021f99ffde6c7f2c0f4f3f311ed2b` (main, 2026-10-21)

## What happens

A GeoJSON file that has a string property with 7 or more Japanese characters (19+ bytes in UTF-8) makes terrio panic.
`terrio info`, `terrio convert` and Python `terrio.open_vector` all fail the same way.

```
thread '<unnamed>' panicked at crates/terrio/src/drivers/vector/geojson.rs:275:22:
end byte index 10 is not a char boundary; it is inside '千' (bytes 9..12 of string)
```

## Minimal reproduction

```sh
printf '{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[139.7,35.7]},"properties":{"name":"東京都千代田区"}}]}' > t.geojson
terrio info t.geojson
```

- `"札幌市北区"` (15 bytes) works. `"東京都千代田区"` (21 bytes) panics. `"abcdefghij"` works.
- In Python the error is `pyo3_runtime.PanicException`, which derives from `BaseException`, so `except Exception:` does not catch it.

The CSV driver has the same code (`crates/terrio/src/drivers/vector/csv.rs:587`): a CSV `x,y,name` / `139.7,35.7,東京都千代田区` panics in the same way.

## Likely cause

In `is_datetime` (`crates/terrio/src/drivers/vector/geojson.rs`), `b.len() >= 19` is checked on bytes, and then `is_date(&s[..10])` slices the `&str` at byte 10.
When byte 10 is in the middle of a multi-byte character (always true for text made only of 3-byte CJK characters), the slice panics.

A possible fix is to test the bytes only, for example `is_date_bytes(&b[..10])`, or to use `s.get(..10)` and treat `None` as "not a date".

## Why it matters

Many Japanese datasets have long place names and addresses, so this is easy to hit.
I found it by converting a vector tile archive (National Land Numerical Information, administrative areas) to GeoJSON and then reading the result.

Thank you for your work. I hope this helps.
