---
id: terrio-formats-vectors-streaming-and-tiles
title: 対応形式（ベクタ・タイル・Arrow）：ストリーム変換、GeoParquet 1.1、タイルの書き出し、南極で落ちる例
status: draft
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
  - terrio docs/formats.md の Vectors、Tile archives、Arrow and GeoArrow の節（main 6779102）
  - docs/getting-started.md の例
  - plays/2026-10-21-license-and-basics.md
related: [terrio-formats-rasters-and-compression, pmtiles-remote-reading, hfu-dwg7-workflow-substitution-survey, geojson-japanese-string-panic, terrio-overview-and-getting-started]
freshness: high
finding:
  - reprojecting-antarctica-to-webmercator-fails
---

## 要点

ベクタは **GeoPackage、GeoParquet、FlatGeobuf、Shapefile、GeoJSON/GeoJSONSeq、CSV、KML/KMZ、GML、GPX、TopoJSON、MapInfo、OSM（読み取りのみ）、PMTiles/MBTiles/MVT のベクタタイル**。層とフィールドの作りは GDAL に合わせる。**GeoPackage、FlatGeobuf、GeoParquet、Shapefile、GeoJSON、GeoJSONSeq、CSV の間の変換は、ストリームで、メモリが有限**。GeoParquet は **1.1 で書く**ことを確かめた。**一方、世界の国界を Web Mercator に変換する文書の例が、南極の点で失敗する**（GeoJSON でも PMTiles でも、0.3.2 でも main でも）。

## やり方

```sh
terrio convert countries.gpkg europe.parquet --where "CONTINENT = 'Europe'" --select NAME,POP_EST   # GeoParquet 1.1
terrio convert countries.gpkg ap.gpkg --append        # 追記（フィールドは名前で対応）
terrio convert countries.gpkg ap.gpkg --overwrite     # 層を置き換える
terrio convert countries.gpkg c.pmtiles --where "NAME <> 'Antarctica'"   # ベクタタイル（既定でズーム 0〜5）
terrio convert --oo ZOOM_LEVEL=5 c.pmtiles z5.geojson
```

## 確かめたこと（何をして、何が起きたか）

- **GeoParquet の書き出し（played）**: ファイルの中に `"version":"1.1.0"`、`primary_column: geometry`、`encoding: WKB`、`geometry_types`、**`covering.bbox` と `geometry_bbox` 列**。ドキュメントの「GeoParquet 1.1、CRS は PROJJSON（EPSG:4326 は省略）、`geometry_bbox` の covering 列、統計つきの 65536 行の行グループ」と合う（行グループの大きさは未確認）。読み取りの bbox は、covering の bbox で行グループと行を飛ばす（ローカルで。リモートの CLI は全量取得）。
- **GeoPackage（played）**: `--append` で 177 → 354 地物、`--overwrite` で 177 に戻る。R-tree による空間フィルター、b-tree の追記、ロールバックジャーナル、WAL・auto-vacuum・トリガーつきは全体を書き直す、などの作りがドキュメントにある（読んだだけ）。
- **ストリーム変換（read-docs）**: GeoPackage、FlatGeobuf、GeoParquet、Shapefile、GeoJSON、GeoJSONSeq、CSV は一度に一部の地物を読む。GeoJSON と CSV の入力は、型の推定のため 2 回読む。FlatGeobuf の出力は、地物を出力の隣の一時ファイルに溜めて、空間インデックスの順に書く。
- **タイルの書き出し（played）**: GeoJSON から PMTiles（400 の四角形、`--minzoom 4 --maxzoom 10`）が書け、戻して 400 地物。**既定のズームは 0〜5**（`ZOOM_LEVEL=5` は読め、`6` は `invalid zoom level 6: the archive has zoom levels 0 to 5`）。GDAL の MVT ライタ相当: EPSG:3857 に投影、バッファ 80（4096 のうち）、タイルが 500 kB を超えると低解像度で符号化して大きな地物に絞る。無効なポリゴンは GEOS の `MakeValid`（linework 法）相当で直す（read-docs）。`--lco` は `MINZOOM`、`MAXZOOM`、`EXTENT`、`BUFFER`、`SIMPLIFICATION`、`MAX_SIZE`、`MAX_FEATURES` など。ラスタのタイルは `--co TILE_FORMAT=PNG|JPEG|WEBP`、`QUALITY`、`ZOOM_LEVEL_STRATEGY` など。
- **南極の点（played）**: Natural Earth の 110m の国界（177 地物）で、
  - `convert countries.gpkg countries_3857.geojson --t-srs EPSG:3857`（**入門ページの例そのもの**）
  - `convert countries.gpkg c.pmtiles`（既定のタイル書き出し）
  - は、どちらも `failed to reproject feature 159 … cannot transform (180, -90)`（地物 159 は Antarctica、最南の緯度が −90）で止まる。**0.3.2 と最新の main（6779102）で同じ**。`--where "NAME <> 'Antarctica'"` を付けると、GeoJSON も PMTiles（804 地物、ズーム 0〜5）も通る。**GDAL（ogr2ogr）の挙動は、この環境にないので未確認**。ドキュメントは「Natural Earth の国界（スーダンが無効）を、ズーム 0〜6 で GDAL と比べた」と書くので、比較には別の前処理があるのかもしれない（未確認）。
- **自然に出た例**: 上の回避策の GeoJSON（ベンガル語などの名前を含む）を、0.3.2 の `terrio info` で開くと、#159 と同じ panic（`geojson.rs:275`）が出た。main では直っている（`upstream-issue-feedback-loop`）。

## 気をつけること

- 世界規模のデータを Web Mercator にするとき、**極（±90°）の点**に注意する。入門の例が、そのまま失敗する。
- GeoJSONSeq は WGS 84、外環が反時計回りで書く。TopoJSON は `crs` メンバーつきで書く。CSV の CRS は隣の `.prj` から。Shapefile の属性は UTF-8 の `.cpg` 付きで書く（CP932 は読めない: `shapefile-cp932-attributes-not-decoded`）。
- MBTiles/PMTiles のラスタは、**低いズームも書く**（`gdal_translate -of MBTiles` と違い、`gdaladdo` を足した形）。
- GDAL との比較（PMTiles のベクタタイルを tippecanoe が書いたものも含む）の記述は、**ドキュメントの主張で、未検証**。

## 出典

- https://terrio.opengeos.org/formats/ 、https://terrio.opengeos.org/getting-started/
- plays/2026-10-21-license-and-basics.md
