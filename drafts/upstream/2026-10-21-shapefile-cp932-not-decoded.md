# Draft issue for opengeos/terrio (not posted; hfu will review and post)

**Title:** Shapefile attributes in CP932 (Shift_JIS) are read as Latin-1, silently — `.cpg` and `SHAPE_ENCODING` are not used for non-UTF-8 code pages

Hello, and thank you for terrio. I am trying it with Japanese public data, where many Shapefiles are encoded in CP932 (Shift_JIS), and I found a gap that I would like to share. It may be a feature request more than a bug.

## Version

terrio 0.3.2 (`pip install terrio`, Linux x86_64). Source checked at `v0.3.2` (`a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6`); the behavior is the same on main at `6779102` (2026-10-21).

## What happens

A Shapefile whose `.dbf` text is CP932 is read with mojibake, with no error or warning.

Reproduction (one point, `name` = 札幌市 stored as CP932 bytes `8E 44 96 79 8E 73`):

| condition | `name` read by terrio |
|---|---|
| no `.cpg` | `\x8eD\x96y\x8es` |
| `.cpg` = `CP932`, `SHIFT_JIS`, `Shift_JIS` or `932` | same |
| `SHAPE_ENCODING=CP932` in the environment | same |

GDAL 3.8.4 (Ubuntu apt) reads these correctly: with `.cpg` = `CP932` or `SHIFT_JIS`, or with `SHAPE_ENCODING=CP932`, the name is `札幌市`; with `.cpg` = `UTF-8` or no `.cpg` it is also garbled, as expected.

## What I found in the source

`crates/terrio/src/drivers/vector/shapefile.rs`: `dbf_layout` only checks whether the `.cpg` contains `UTF-8`, `UTF8` or `65001`, and `decode` is "UTF-8 if valid, else Latin-1". The module comment says text is decoded "as the `.cpg` file (or the DBF language driver) declares", so I think the intention was wider than the current code.

## Suggestion

If it fits the project, a small step would be to map common `.cpg` names (CP932 / Shift_JIS / EUC-JP / GBK / Big5 / CP1252 …) to a pure-Rust decoder such as `encoding_rs` (it also works in WebAssembly), and to honour `SHAPE_ENCODING` / the DBF language driver byte. If decoding is out of scope, a warning when the bytes are not valid UTF-8 and the `.cpg` names another code page would already help, because silent mojibake is hard to notice.

Thank you for your work and for considering this.
