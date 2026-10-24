---
id: terrio-python-api
title: Python API（terrio）：ドキュメントの例 30 件を動かした結果
status: stale
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: python
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - terrio docs/python.md（main 6779102）
  - plays/2026-10-21-license-and-basics.md
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
related: [terrio-rio-rasterio-compatible-api, terrio-cli-command-reference, terrio-formats-vectors-streaming-and-tiles, terrio-install-platforms-and-release-history]
freshness: high
---

## 要点

Python の API は、**ラスタ（`open_raster`、遅延の窓・overview 読み）、ベクタ（`open_vector`、`write_vector`、ストリーム）、Arrow、各操作（`convert` `translate` `warp` `mosaic` `rasterize` `polygonize` `dem` `calc` `proximity` `sieve`）、座標変換（`transform_points`）、バイトからの読み書き**。コマンドのオプションがキーワード引数になる。ドキュメントの例を手元のデータで 30 件動かし、**29 件が通り、失敗の 1 件は、世界の国界を Web Mercator に変える例（南極の点）**だった。

## やり方

```python
import terrio
cog = terrio.open_raster("https://…/B04.tif", lazy=True)         # 窓だけ範囲読み
tile = cog.read(1, window=(5000, 5000, 256, 256)); thumb = cog.read(overview=2)
ds = terrio.open_vector("countries.gpkg"); layer = ds.layers[0]   # layer["name"] でも
terrio.write_vector(layer, "world.gpkg", append=True)             # 追記
for chunk in terrio.open_stream("countries.gpkg", "ne_110m_admin_0_countries", batch_size=50): ...
terrio.convert("ne.zip", "eu.gpkg", where="CONTINENT = 'Europe'", select=["NAME"])
terrio.transform_points([139.767125], [35.681236], "EPSG:6668", "EPSG:6677")
```

## 確かめたこと（何をして、何が起きたか）

- **通った 29 件**: `open_vector`（名前、CRS、種類、件数 177、範囲）、`layer["…"]`、`to_geojson`（177）、`to_wkb`、`columns`、`write_vector`（FlatGeobuf、GeoJSON の辞書）、`bbox` 読み（42 件）、`append`（177 → 354）、`open_stream`（合計 177）、`iter_features`（177）、`convert(where, select)`（39）、`info(stats=True)`、`translate(outsize=("25%","25%"))`（128²）、`warp(t_srs="EPSG:4326")`、`mosaic`（リスト入力）、`rasterize(attribute=…)`、`polygonize(connectedness=8)`（910。CLI の既定の 4 連結は 1,260）、`dem(hillshade, z=2, multidirectional=True)`、`calc`（NDVI の平均 0.344）、`proximity`、`sieve`、`transform_points`（`-5992.9196, -35363.2377`）、エポックつき、`set_grid_search_paths`、`open_bytes`/`to_bytes`、`Raster.from_array` から COG と GeoZarr v3 への書き出し、`GeoTiffWriter`（行ごと、マスクつき）、`read_mask`。
- **失敗 1 件**: `layer.to_crs("EPSG:3857")` が `CRSError … failed to reproject feature 159 … cannot transform (180, -90)`（南極。CLI と同じ原因）。
- **エラーの型（ドキュメントどおり）**: 存在しないファイルは `NotFoundError`（`FileNotFoundError` の子）、不正な CRS は `CRSError`（`ValueError` の子）、未知のキーワードは `TypeError`。**ただし panic は `PanicException`（`BaseException`）で、これらに入らない**（`japanese-path-panic-in-zarr-parse-name`）。
- 型スタブ（`py.typed`、`mypy --strict`、`stubtest` で検査）と、`terrio.TerrioError` の階層は、ドキュメントの記述（未検証）。

## 気をつけること

- **Arrow の相互運用（played、別の仮想環境に pyarrow 26.0、GeoPandas 1.2、Polars 2.0）**: `layer.to_arrow()` → `pa.table`（177 行、geometry 列に `ARROW:extension:name`）、`GeoDataFrame.from_arrow`（177 行、CRS EPSG:4326）、`polars.DataFrame(t)`（177×169）、`to_arrow(geometry_encoding="geoarrow")` の拡張名は `geoarrow.multipolygon`、`terrio.from_arrow(pa_table)`（177）、`write_vector(pa_table, …gpkg, layer_name=…)` がすべて通った。DuckDB と GDAL の Arrow ストリームは未確認。
- `polygonize` の連結性の既定は、CLI（4 連結）と Python（引数で指定）で、同じ入力でも結果が違って見える。指定を明示する。
- 日本語の相対パスや CP932 の Shapefile などの入口の問題は、Python でも同じ（`terrio-source-quirks`）。

## 出典

- https://terrio.opengeos.org/python/
- plays/2026-10-21-license-and-basics.md
