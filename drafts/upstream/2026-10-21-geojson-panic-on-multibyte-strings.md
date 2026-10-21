# Draft issue for opengeos/terrio (not posted; hfu will review and post)

**Title:** GeoJSON reader panics on long multibyte strings during datetime detection

Hello, and thank you for terrio. It is wonderful to see a pure-Rust GDAL-style tool grow so quickly.
While trying it on Japanese data, I found a small bug and wanted to report it in case it is useful.

## Version

- terrio 0.3.2 (`pip install terrio`, Linux x86_64, Python 3.13)
- Source checked at `cf6bd5dbcb6021f99ffde6c7f2c0f4f3f311ed2b` (main, 2026-10-21)

## What happens

A GeoJSON feature with a string property that contains 7 or more Japanese characters (19+ bytes in UTF-8) can make terrio panic while inferring field types.
`terrio info`, `terrio convert`, and Python `terrio.open_vector` all fail the same way.

```text
thread '<unnamed>' panicked at crates/terrio/src/drivers/vector/geojson.rs:275:22:
end byte index 10 is not a char boundary; it is inside '千' (bytes 9..12 of string)
```

This appears to be a bug in the GeoJSON reader, not in the input itself. GDAL reads the same kind of value without error, while terrio panics while checking whether a string looks like a date or datetime.

## Minimal reproduction

```sh
printf '{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[139.7,35.7]},"properties":{"name":"東京都千代田区"}}]}' > t.geojson
terrio info t.geojson
```

- `"札幌市北区"` (15 bytes) works.
- `"東京都千代田区"` (21 bytes) panics.
- `"abcdefghij"` works.

In Python the error is `pyo3_runtime.PanicException`, which derives from `BaseException`, so `except Exception:` does not catch it.

## Likely cause

In `is_datetime` (`crates/terrio/src/drivers/vector/geojson.rs`), the code checks `b.len() >= 19` on the UTF-8 byte length and then slices `&s[..10]`.
When byte 10 falls inside a multi-byte character, the slice is not a valid `&str` boundary and Rust panics.

This is especially easy to trigger with Japanese text, where many characters are three bytes in UTF-8.

A possible fix is to avoid slicing the `&str` at a byte position without checking boundaries, for example by testing the byte slice directly or by using `s.get(..10)` and treating `None` as “not a date”.

## Why it matters

This is easy to hit with real-world Japanese datasets, especially place names and addresses. In my case, I hit it while converting a vector tile archive (National Land Numerical Information, administrative areas) to GeoJSON and then reading the result.

The issue is also user-visible in multiple interfaces: CLI, Python API, and file conversion. A robust library should not panic on valid UTF-8 string values just because they are long and non-ASCII.

Thank you for your work. I hope this is helpful.
