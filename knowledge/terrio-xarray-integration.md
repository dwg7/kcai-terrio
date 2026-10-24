---
id: terrio-xarray-integration
title: xarray 連携（terrio.xarray）：リモート COG を遅延で開き、窓だけ取って再投影する
status: stale
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: python
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、Node 22、Chromium 1194）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - terrio docs/xarray.md（main 6779102）
  - USGS 3DEP の COG（https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/current/n40w106/USGS_1_n40w106.tif、51 MB）
  - plays/2026-10-21-license-and-basics.md
related: [terrio-python-api, terrio-rio-rasterio-compatible-api, cog-remote-window-overview-and-warp, terrio-formats-rasters-and-compression]
freshness: high
---

## 要点

`pip install "terrio[xarray]"`（terrio、xarray、dask）で、**rioxarray の API を GDAL なしで**使える。`terrio.xarray.open_rasterio`（または `xr.open_dataset(path, engine="terrio")`）が、ラスタを**遅延で** DataArray として開き、`.terrio` アクセサが rioxarray の `.rio` のメソッド（`clip_box`、`reproject`、`to_raster` など）を持つ。ドキュメントの例（リモートの標高 COG）を動かし、**最後まで通った**。リモートの COG は、窓に必要なタイルだけを範囲読みする。

## やり方

```python
import xarray as xr, terrio.xarray as txr
url = "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/current/n40w106/USGS_1_n40w106.tif"
dem = txr.open_rasterio(url, masked=True, chunks=True)           # ヘッダーだけ
b = dem.terrio.clip_box(-105.35, 39.85, -105.15, 40.0, crs="EPSG:4326")   # 窓のタイルだけ取る
utm = b.terrio.reproject(b.terrio.estimate_utm_crs(), resolution=30, resampling="bilinear")
utm.terrio.to_raster("boulder.tif", driver="COG", compress="DEFLATE")
utm.terrio.to_raster("boulder.zarr")                              # GeoZarr
utm.to_dataset(name="elevation").to_zarr("x.zarr")                # 座標系つきで保存（zarr パッケージが要る）
txr.register_rio_accessor()                                       # rioxarray 用のコードを `.rio` のまま動かす
```

## 確かめたこと（何をして、何が起きたか）

- `open_rasterio(url, masked=True, chunks=True)`: 3.4 秒、次元 `('band','y','x')`、形 (1, 3612, 3612)、float32。座標は `band x y spatial_ref`。`.terrio.crs` は `EPSG:4269`、解像度 0.000277…°。
- `clip_box(-105.35, 39.85, -105.15, 40.0, crs="EPSG:4326")` → (1, 541, 721)、`compute()` で標高 1606〜2835 m。`reproject(estimate_utm_crs(), resolution=30, resampling="bilinear")` → (1, 558, 572)、`EPSG:32613`。
- **ここまでの転送量: 要求 4 回、約 3.2 MiB**（ヘッダー、窓のタイル）。
- `to_raster` で COG（1.34 MB）と GeoZarr（`.zarr` のディレクトリ）が書け、GeoZarr を `txr.open_rasterio` で読み戻せた（EPSG:32613）。xarray の `to_zarr` でも座標系が保たれ、`decode_coords="all"` で読み戻すと `spatial_ref` の座標がある。
- `xr.open_dataset(url, engine="terrio")` は `band_data`（1, 3612, 3612）。`register_rio_accessor()` の後、`dem.rio.crs == dem.terrio.crs`。`merge_arrays`（2 枚のタイル）が (2, 200, 300)。
- **`xarray` の `to_zarr` は `zarr` パッケージが要る**が、`terrio[xarray]` の extras には入らない（`pip install zarr` を足した）。Zarr v3 の統合メタデータについての警告が出た。
- ドキュメントの主張（read-docs）: rioxarray 0.23 と 257 チェック（同一 216、WKT の文字だけ違う 20、許容内 21、差異 0）。再投影は丸めの違い（GDAL の格子の計算が terrio と 1e-15 の相対差）。HTTP で窓を読むと、必要なタイルだけ（0.4〜1.6 MB、GDAL の 15% 以内）、開くだけで 0.13 MB（GDAL は 0.02 MB）。dask の各読み手がファイルを開き直し、**ピクセルインターリーブの COG で同じタイルを読み手の数だけ取る**（4 バンドで 2.8 MB、GDAL は 0.64 MB）。`lock=True` で 1 回にできる（0.66 MB）。

## 気をつけること

- **サブデータセット（netCDF の変数、HDF5 のグループ）は未対応**（`NotImplementedError`）。GCP と RPC も読み書きしない。書くのは CF 規約だけ。回転した格子は書けない。`estimate_utm_crs` は WGS 84、NAD83、NAD27 の UTM のみ。複素数型は未対応。
- **HTTP の `.aux.xml` サイドカーは読まない**。GeoTIFF 以外のメタデータ（タグ、バンドの説明、ブロックの形）は GDAL と違うことがある。
- `to_raster` は、出力全体をメモリに持ってから書く（dask でもチャンクごとに計算して書き手のバッファへ）。
- `chunks=True` だと、この COG では**幅いっぱいのチャンク**（3612）になった。大きなファイルでは `chunks` を明示する。
- 日本の座標系（JGD2011 など）と日本語のバンド名・パスは、**この踏み跡では試していない**。

## 出典

- https://terrio.opengeos.org/xarray/
- plays/2026-10-21-license-and-basics.md
