> **取り下げ（OBSOLETE）**: この下書きは**投稿しない**。2 次元の `EPSG:6668` を使ったための誤りで、3 次元の `EPSG:6667 → EPSG:6697` なら terrio は日本のジオイドを適用する。GDAL 3.8.4 でも 2 次元は高さ不変で、同じ格子なら小数 11 桁まで一致した（`plays/2026-10-21-gdal-comparison.md`、`knowledge/vertical-datum-grids-and-geoid-in-japan.md`）。経緯の記録として残す。

# Draft question for opengeos/terrio (not posted; hfu will review and post)

**Title:** Question: should `EPSG:6697 → EPSG:6668` apply the Japanese geoid (`jp_gsi_gsigeo2011.tif`)? Heights stay unchanged in 0.3.2

Hello, and thank you for terrio. I am not sure whether this is a bug or my usage, so I am writing it as a question with what I tried. (Also, `docs/why-terrio.md` says shift grids are not applied yet, while `docs/crs.md` describes grid support; the latter seems right.)

## Version

terrio 0.3.2 (PyPI wheel, Linux x86_64); same result on main at `6779102` (2026-10-21, after #163).

## What works

```sh
echo "139.767125 35.681236 50" | TERRIO_NETWORK=ON terrio crs EPSG:4979 --to "EPSG:4326+5773"
# 139.767125 35.681236 13.555884932782078   (downloads us_nga_egm96_15.tif; looks right)
```

## What I expected, and what I got

Tokyo Station area, JGD2011 orthometric height 50 m to ellipsoidal height. The geoid height there is about +37 m, so I expected about 87 m. The PROJ CDN has `jp_gsi_gsigeo2011.tif` and `jp_gsi_jpgeo2024.tif`.

```sh
echo "139.767125 35.681236 50" | TERRIO_NETWORK=ON terrio crs EPSG:6697 --to EPSG:6668
# 139.767125 35.681236 50      (height unchanged, no grid downloaded)
```

Also unchanged: `6668 → 6697`, `6668 → 6668+6695`, and PROJ strings with `+geoidgrids=jp_gsi_gsigeo2011.tif` / `jp_gsi_jpgeo2024.tif` (both directions). The grid file itself opens fine with `terrio info` (1201×1800, EPSG:6668).

## Questions

1. Is the Japanese vertical transformation expected to be selected from the EPSG data, or is it not covered yet?
2. For a `+geoidgrids=` PROJ string, which direction and CRS pair should I use?

One more observation: with terrio-js 0.3.2 in Node, registering the grid directly (`registerGrid("jp_gsi_gsigeo2011.tif", bytes)`) and transforming `EPSG:6668 → EPSG:6697` also leaves the height unchanged (86.7 → 86.7), while the same call with `us_nga_egm96_15.tif` for `EPSG:4979 → EPSG:4326+5773` works. So the grid lookup seems fine, and the issue may be in how the Japanese vertical transformation is selected.

I can test a build or a different invocation if that helps. Thank you!
