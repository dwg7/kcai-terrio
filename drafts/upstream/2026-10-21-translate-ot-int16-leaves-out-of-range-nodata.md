> **取り下げ（OBSOLETE）**: この下書きは**投稿しない**。GDAL 3.8.4 は nodata を -32768 に丸めて警告するが、**GDAL 3.13.3（新しい版）は terrio と同じく -999999 のまま残す**（警告なし）。terrio の挙動は、新しい GDAL と同じで、不具合とは言えない。GDAL の版による違いだった。（`plays/2026-10-22-gdal-313-pdal-comparison.md`）

# Draft issue for opengeos/terrio (not posted; hfu will review and post)

**Title:** `translate --ot Int16` keeps an out-of-range nodata value (-999999) without a warning; GDAL clamps it and warns

Hello, and thank you for terrio. A small thing I noticed when converting a Float32 elevation raster to Int16.

## Version

terrio 0.3.2 (PyPI wheel, Linux x86_64). Compared with GDAL 3.8.4 (Ubuntu apt). I did not check main for this one.

## Reproduction

A Float32 GeoTIFF (8x8) with nodata = -999999 and one nodata pixel.

```sh
terrio translate f.tif i.tif --ot Int16
terrio info i.tif
# Band 1: Int16, nodata=-999999     (outside the Int16 range, no message)

gdal_translate -ot Int16 f.tif g.tif
# Warning 1: for band 1, nodata value has been clamped to -32768, the original value being out of range.
# NoData Value=-32768
```

## Question

The nodata tag cannot match any Int16 pixel, so nodata pixels are probably no longer recognized after the conversion. Would a warning, a clamp like GDAL, or an error be preferred? I am not sure what the intended behavior is.

Thank you for your work. I hope this is useful.
