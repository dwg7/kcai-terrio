---
id: terrio-overview-and-getting-started
title: terrio の概観と入門の手順（トップページ、Getting Started、Notebooks を実際に動かす）
status: stale
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - terrio docs/index.md、docs/getting-started.md、docs/notebooks.md（main 6779102）
  - plays/2026-10-21-license-and-basics.md（入門の手順の実行）
related: [terrio-cli-overview, terrio-scope-included-and-excluded, terrio-architecture-and-pure-rust-claim, cog-remote-window-overview-and-warp, terrio-install-platforms-and-release-history]
freshness: high
---

## 要点

トップページの自己紹介は「**C の依存なしで、ほとんどのワークフローが使う形式を読み、書き、変換し、再投影する。Rust が動く所ならどこでも（WebAssembly を含む）ビルドでき、実データで GDAL とファイルごとに突き合わせて試験する**」。入門ページ（Getting Started）の手順を、公開データで実際に動かした。**ほぼ動いたが、文書どおりに打つと失敗する例が 1 つあり、標高タイルの例は全量取得になる書き方が含まれる。**

## やり方

```sh
terrio info https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip   # zip の中の Shapefile を見つけて読む
terrio convert ne.zip countries.gpkg ; terrio convert countries.gpkg countries.fgb
terrio convert countries.gpkg europe.parquet --where "CONTINENT = 'Europe'" --select NAME,POP_EST
terrio rasterize countries.gpkg population.tif -a POP_EST --tr 0.1 0.1 --ot Float64
terrio polygonize population.tif pop_poly.gpkg --field v
terrio crs EPSG:4326 --to EPSG:32613 -105.5 39.5
# 標高タイル（COG、51 MB）は窓で
U=https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/current/n40w106/USGS_1_n40w106.tif
terrio translate $U subset.tif --srcwin 1000 1000 512 512 --ot Int16
terrio warp subset.tif dem_utm.tif --t-srs EPSG:32613 --tr 30 30 -r bilinear
```

Notebooks ページは、Colab で開ける 2 本（quickstart、xarray）の説明。**ノートブックは実行していない**。

## 確かめたこと（何をして、何が起きたか）

- トップページの機能の一覧は、ラスタ、ベクタ（ストリーム変換）、点群（リモート COPC / EPT の範囲読み）、クラウドのデータ、GDAL 流の操作（`warp` は 14 のリサンプリング）、座標系、3 つの口（Rust、Python、npm）。**状況は「初期開発。1.0 まで API が変わりうる」**。
- `info`（Natural Earth の zip、215 KB）: 要求 1 回、受信 210 KiB。`ESRI Shapefile`、177 地物、EPSG:4326。
- `convert`: zip → GPKG（553 KB）→ FlatGeobuf（482 KB）が通る。`--where "CONTINENT = 'Europe'" --select NAME,POP_EST` で Parquet に 39 地物（34 KB）。
- **文書の例 `convert countries.gpkg countries_3857.geojson --t-srs EPSG:3857` が失敗**: `failed to reproject feature 159 of layer 'ne_110m_admin_0_countries': cannot transform (180, -90)`（南極の点。Web Mercator は緯度 −90 を表せない）。**GDAL の ogr2ogr がどう振る舞うかは、この環境にないので未確認**。`--skipfailures` はない。
- `rasterize -a POP_EST --tr 0.1 0.1 --ot Float64`: 3601×1737、有効 2,149,757 画素、最大 1,397,715,000（中国の人口）。`polygonize --field v` で 306 ポリゴン。`crs EPSG:4326 --to EPSG:32613 -105.5 39.5` は `457010.38774697867 4372383.823613901`。
- USGS の標高 COG（51,486,544 バイト、3612²、Float32、EPSG:4269、overview 3 段）: `info` は 64 KiB。**`translate --srcwin 1000 1000 512 512 --ot Int16` は 3 要求・3.2 MiB の範囲読み**。出力は **`Int16` なのに `nodata=-999999`**（Int16 の範囲外。エラーも警告もなし。GDAL がどうするかは未確認）。`warp`（411×529、30 m、UTM 13N）と `mosaic`（.vrt と .tif、512×512）は動いた。
- 文書は標高タイルの全体を `terrio convert USGS_1_n40w106.tif dem.tif -f COG --compress DEFLATE` で変換する例を載せる。**窓なしの `convert` は 51 MB を全部読む**（実行していない。`cloud-native-read-behavior-matrix`）。

## 気をつけること

- 入門の例を、そのまま打ち込んで全部通る、とは限らない（EPSG:3857 の例）。
- `nodata` が出力の型で表せない値のままになる点は、後続の処理（`calc`、`dem`）で気づきにくい。出力の `info` で確かめる。
- トップページの「GDAL とファイルごとに突き合わせて試験」は**主張**で、この遊びでは検証していない（`terrio-conformance-and-testing-against-gdal`）。

## 出典

- https://terrio.opengeos.org/ 、https://terrio.opengeos.org/getting-started/ 、https://terrio.opengeos.org/notebooks/
- plays/2026-10-21-license-and-basics.md
