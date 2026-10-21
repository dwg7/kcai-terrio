---
id: terrio-rio-rasterio-compatible-api
title: rasterio 互換 API（terrio.rio）：実際の利用コードの呼び出しが通るか
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: python
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
sources:
  - plays/2026-10-21-untested-items.md（3）
  - terrio docs/rasterio.md
  - dwg7/snow-hokkaido の src/*.py（公開。呼び出しの形だけ参照し、実行はしていない）
related: [hfu-dwg7-workflow-substitution-survey, terrio-possibilities-and-risks]
freshness: high
---

## 要点

`import terrio.rio as rasterio` で、rasterio の呼び出しの多くがそのまま通る。**dwg7/snow-hokkaido が使う呼び出しの再現 12 件は、すべて通った**（合成データと、リモート COG への窓読み）。GDAL の wheel なしで、既存の rasterio コードを移せる見込みがある。ただし、**値の同等性（rasterio の結果と同じ数値か）は、ここでは確かめていない**。

## やり方

```python
import terrio.rio as rasterio                      # `import terrio` だけでは `terrio.rio` は出ない
from terrio.rio.windows import Window, from_bounds
from terrio.rio.transform import from_origin
from terrio.rio.features import rasterize
from terrio.rio.enums import Resampling

with rasterio.Env(GDAL_HTTP_MAX_RETRY="3"):
    with rasterio.open("https://…/B03.tif") as g:       # 遅延読み（Range）
        w = from_bounds(350000, 3945000, 352000, 3947000, g.transform)
        a = g.read(1, window=w, out_shape=(100, 100), resampling=Resampling.nearest)

with rasterio.open("out.tif", "w", driver="GTiff", width=300, height=200, count=2, dtype="uint8",
                   crs="EPSG:6668", transform=from_origin(139.0, 36.0, 0.001, 0.001),
                   compress="deflate", blocksize=512, tiled=True) as dst:
    dst.write(arr1, 1); dst.write(arr2, 2)
    dst.set_band_description(1, "class"); dst.update_tags(obs_start_utc="2026-10-01T00:00:00Z")
```

## 確かめたこと（何をして、何が起きたか）

通った呼び出し（12 件）:

1. 2 バンドの書き込み（`compress`、`blocksize`、`tiled`）と `set_band_description`・`update_tags`
2. 読み戻し（`shape`、`tags()`、`descriptions`、`crs`、`count`）
3. `driver="COG"` での書き込み
4. `read(boundless=True, fill_value=0)`（ラスタの外にはみ出す窓）
5. `from_bounds` + `out_shape` + `Resampling.nearest` + `window_transform` + `windows.bounds`
6. `rasterio.Env(...)` の中で、リモート COG の窓読み（Sentinel-2、約 6 MiB）
7. `rasterize(..., all_touched=False)`
8. `sample`
9. `'r+'` での `update_tags`
10. `warp.transform_bounds`
11. `warp.calculate_default_transform`
12. `shapes`（ベクタ化）

- `COG` で書いたファイルを `terrio.info` で見ると `Driver: GTiff`（GDAL と同じ扱い）。
- `Window` の値が `np.float64`（rasterio は Python の float）。
- 名前の確認: `windows` `features` `transform` `enums` `warp` `io` `mask` `merge` `env` `sample` がある（`vrt` は未確認）。

## 気をつけること

- **数値の同等性は未確認**（rasterio がこの環境にない）。置き換えるときは、1 スクリプトずつ、出力を比べる。
- `rasterio.open(...)` に GDAL 固有の `--config` 相当（`GDAL_DISABLE_READDIR_ON_OPEN` など）を渡しても、効いているかは分からない（`Env` は受け付けるだけかもしれない）。
- 日本語のパスで panic する（`japanese-path-panic-in-zarr-parse-name`）。`terrio.rio.open('日本地図.tif')` も同じ入口を通るはず（**未確認**）。
- GeoPandas / pyproj / rio-tiler など、rasterio の周りのライブラリは別。

## 出典

- plays/2026-10-21-untested-items.md
- https://terrio.opengeos.org/rasterio/
