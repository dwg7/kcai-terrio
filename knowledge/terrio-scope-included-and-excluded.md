---
id: terrio-scope-included-and-excluded
title: terrio が含む機能と含まない機能
status: draft
terrio_version: 0.5.0
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、PyPI の wheel）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-24
interface: cli
verified_on: 2026-10-24
verified_how: read-docs
sources:
  - terrio docs/why-terrio.md、docs/gdal.md、docs/formats.md、docs/remote-data.md（v0.3.2 と main cf6bd5d）
  - terrio ROADMAP.md（main cf6bd5d）
  - "`terrio formats` の出力（plays/2026-10-21-first-contact.md）"
related: [terrio-cli-overview, cloud-native-read-behavior-matrix, terrio-release-vs-main-drift, vertical-datum-grids-and-geoid-in-japan, shapefile-cp932-attributes-not-decoded]
---

## 要点

terrio は「GDAL の全部の置き換え」ではなく、**よく使う形式の入出力・変換・再投影・ラスタ処理・点群を、C ライブラリなしで**行う道具。範囲外は、はっきり宣言されている。

**含む（読んだ範囲）**

- 形式（`terrio formats` で確認）: ラスタ（GeoTIFF/COG、各種 ASCII/バイナリ格子、JPEG2000、PNG/JPEG+ワールドファイル、Zarr、netCDF、HDF5(読)、VRT、MBTiles、PMTiles、GeoPackage タイル、STACIT(読)）、ベクタ（GeoJSON、GeoJSONSeq、TopoJSON、GeoPackage、GeoParquet、FlatGeobuf、Shapefile、KML/KMZ、GML、GPX、MapInfo、OSM(読)、CSV、MBTiles/PMTiles/MVT）、点群（LAS、LAZ、COPC、EPT(読)、PLY、E57）。
- 処理: warp、translate、mosaic、rasterize、polygonize、dem、calc、proximity、sieve、点群の grid / filter。
- 座標系: EPSG の座標系（6,354 件とされる）と、GDAL が選ぶのと同じ変換操作。
- 入力の場所: ローカル、HTTP(S)、S3、GCS、Azure、zip、GDAL の `/vsi*/`。
- 呼び出し口: CLI、Python（NumPy、Arrow、rasterio 互換 `terrio.rio`）、Rust、JavaScript/WebAssembly、MCP（main のみ）。

**含まない / 非目標（宣言されたもの）**

- 独自 SDK が要る形式（MrSID、ECW、FileGDB ラスタ）、データベースドライバー（PostGIS など）。
- GDAL の C API やオプション名の完全一致。
- 回転した geotransform、GCP だけの位置合わせ。
- **測地系のずれの格子（NTv2 など）の適用**: `docs/why-terrio.md` は "does not apply NTv2 or other shift grids yet" と書くが、`docs/crs.md` は PROJ の格子を探して適用すると書き、実測でも EGM96 は適用された（`TERRIO_NETWORK=ON`）。日本のジオイドも、3 次元の CRS（`EPSG:6667`）から変換すれば適用される（2 次元の `EPSG:6668` では、GDAL も高さを変えない。`vertical-datum-grids-and-geoid-in-japan`）。
- 幾何学アルゴリズム（バッファ、交差、簡略化）。`geo` クレートなどを使う。
- **出力のリモート書き込み**（出力はローカルのみ）。
- 既定のビルドは純 Rust。長い尾の形式（HDF4、GRIB、NITF、DXF、FileGDB の書き込みなど）は、任意の GDAL バックエンド（`gdal` feature）経由。**PyPI の wheel には入っていない**。

**中間（できるが条件つき）**

- 大きなベクタや GeoParquet の「その場読み」: 設計方針には「クラウドのデータはその場で読む」とあるが、実際は形式による（`cloud-native-read-behavior-matrix`）。
- ほとんどの非 GeoTIFF 入力は、メモリに全部読む。

## やり方

範囲を確かめたいときは、(1) `terrio formats`、(2) `docs/formats.md`、(3) `docs/gdal.md` の「Differences to know」、(4) `ROADMAP.md` の未完了項目（`[ ]`）、の順に見る。

## 確かめたこと（何をして、何が起きたか）

- `terrio formats` の一覧は、実際に出力を見て確認した（**played**）。
- 上の「含む」「含まない」の記述は、ドキュメントとロードマップを**読んだ**もので、個別に動かして確かめたものではない（`verified_how: read-docs`）。動かして確かめたことは `cloud-native-read-behavior-matrix` などの踏み跡に分けた。
- ロードマップの未完了項目（例: Zarr のリモートグループ一覧、STAC の POST ページング、署名付き URL）は、main の時点のもの。

## 気をつけること

- 「GDAL と同じ結果」を目標にしているが、それは**主張**。この遊びでは GDAL との突き合わせをしていない。
- ロードマップは変わる。版が上がったら読み直す（`stale` の印をつける）。
- 「含む」の中にも未試験が多い（`terrio-cli-overview` の「確かめたこと」）。

## 0.5.0 での再確認（2026-10-24）

0.5.0 の範囲の変化: **含む**ようになった — 幾何の検査・修復・バッファ・オーバーレイ・ディゾルブ・クリーン、等高線、ゾーン統計、読み取り専用の SQL、GRIB1/2、STACTA、Planetary Computer の署名、PDAL の追加フィルタ、`terrio-rio`、MCP。**含まない**まま — タイル生成（tippecanoe 相当）、HDF4 / NITF / DXF などの長い尾の形式、GDAL 同梱の wheel（方針として作らない）。日本語エンコーディング（CP932）は**未対応**。read-docs / played。

## 出典

- https://terrio.opengeos.org/ （why-terrio、gdal、formats、remote-data）
- https://github.com/opengeos/terrio/blob/main/ROADMAP.md
