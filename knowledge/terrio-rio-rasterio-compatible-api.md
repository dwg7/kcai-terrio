---
id: terrio-rio-rasterio-compatible-api
title: rasterio 互換 API（terrio.rio）：実際の利用コードの呼び出しが通るか
status: draft
terrio_version: 0.5.0
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: python
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-24
verified_on: 2026-10-24
verified_how: played
sources:
  - plays/2026-10-21-untested-items.md（3）
  - terrio docs/rasterio.md（main 6779102）
  - dwg7/snow-hokkaido の src/*.py（公開。呼び出しの形だけ参照し、実行はしていない）
related: [terrio-python-api, hfu-dwg7-workflow-substitution-survey, terrio-possibilities-and-risks, terrio-formats-rasters-and-compression]
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

## ドキュメントの内容と、追加で確かめたこと（2026-10-21 夜）

**対応範囲（read-docs）**: \`rio.open\`（\`r\` \`r+\` \`w\` \`w+\`、パス、URL、ファイルオブジェクト、\`MemoryFile\`）、データセットの属性とメソッド（\`read\` の \`window\` \`out_shape\` \`resampling\` \`masked\` \`boundless\` \`fill_value\`、\`write\`、\`sample\`、\`build_overviews\`、\`statistics\` など）、\`crs\`、\`transform\`、\`windows\`、\`features\`（\`rasterize\` \`shapes\` \`geometry_mask\` \`sieve\`）、\`warp\`（\`reproject\` \`calculate_default_transform\` \`transform_bounds\` \`transform_geom\`）、\`merge\`、\`mask\`、\`vrt.WarpedVRT\`、\`io\`（\`MemoryFile\` \`ZipMemoryFile\`）、\`control\`/\`rpc\`、\`shutil\`、\`stack\`、\`env\`/\`session\`（\`Env\` は GDAL のオプションと認証情報を terrio が読む環境変数に変え、**他は受け付けて無視**）、\`plot\`。

**仕組み（read-docs）**: GeoTIFF/COG と JPEG 2000 は、ローカルでもリモートでも窓ごとの遅延読み（overview は GDAL の選び方）。**ほかの形式（ASCII グリッド、ERDAS、ENVI、netCDF、Zarr）は、開くときに全部読む**。回転・南北反転の変換、GCP、RPC を読み書きできる。書き込みは、閉じるときにファイルへ（既定で 512 MB 超は一時ファイルに溜め、行ごとに書く。\`TERRIO_RIO_IN_MEMORY_LIMIT\`）。**GeoTIFF の nodata は 1 つだけ**（バンドごとに違う値を渡すと最後のバンドの値を書き、GDAL と同じ警告）。

**rasterio との一致（作者の比較、read-docs）**: 実ファイルとリモート COG で 160 チェック: **128 同一、17 許容内、15 既知の差**。既知の差は、バイリニア・キュービック・平均の縮小読み（nodata の近く）、\`-inf\` の nodata の boundless 読み、VRT の窓の読み、ESRI の \`.prj\` の EPSG 識別。**rasterio 1.5（GDAL 3.12）との突き合わせで、この遊びでは rasterio を使っていない**。

**対応していないもの（read-docs）**: 外部の \`.msk\` マスク、RPC 変換器、\`gauss\` の再サンプリング、PROJJSON/WKT2 の出力、**不可逆の GeoTIFF コーデックと YCbCr の JPEG（GDAL と違う復号）、LERC・LZMA・JPEG XL の復号**（※ドキュメント間で、\`formats.md\` は「LERC・LZMA・JPEG XL を読める」と書く。\`rasterio.md\` の記述と食い違う）、\`r+\` は全部書き直す、バンドの色テーブルはバンド 1 のみ、\`opener=\`、コマンドライン \`rio\`。

**追加で確かめた（played、0.3.2）**:
- \`read(1)\` は**通常の \`ndarray\`**、\`read(1, masked=True)\` で \`MaskedArray\`（B04 の nodata は 0.0）。\`dataset_mask()\` と \`read_masks()\` は uint8。
- 端数のある窓 \`Window(10.5, 10.25, 100.5, 50.75)\` が読め、形は (51, 101)。
- エラー: 存在しないファイルは \`terrio.rio.errors.RasterioIOError\`、不正な CRS は \`CRSError\`、範囲外のバンドは \`IndexError\`（rasterio と同じ型）。
- \`CRS.from_epsg(6677)\`: \`to_epsg()=6677\`、\`is_projected=True\`、\`linear_units='metre'\`。\`CRS.from_string('EPSG:6668').is_geographic=True\`。
- \`rasterio.Env(GDAL_HTTP_MAX_RETRY='3', FOO_BAR='x')\` が受け付けられる（未知のキーも）。

## 気をつけること

- **数値の同等性は未確認**（rasterio がこの環境にない）。置き換えるときは、1 スクリプトずつ、出力を比べる。
- `rasterio.open(...)` に GDAL 固有の `--config` 相当（`GDAL_DISABLE_READDIR_ON_OPEN` など）を渡しても、効いているかは分からない（`Env` は受け付けるだけかもしれない）。
- 日本語のパスで panic する（`japanese-path-panic-in-zarr-parse-name`）。`terrio.rio.open('日本地図.tif')` も同じ入口を通るはず（**未確認**）。
- GeoPandas / pyproj / rio-tiler など、rasterio の周りのライブラリは別。

## 0.5.0 での再確認（2026-10-24）

0.5.0 の wheel に `terrio.rio`（rasterio 互換のモジュール）と **`terrio-rio` コマンド**（`terrio-rio info B04.tif` が JSON を返す、played）。ドキュメントの `rasterio.md` は +91 行（RPC 変換、`.msk` の読み書き、rio の CLI）。公式ノートブック 2 本は rio アクセサ互換を含めて成功（played）。

## 出典

- plays/2026-10-21-untested-items.md
- https://terrio.opengeos.org/rasterio/
