---
id: why-terrio-comparison-with-alternatives
title: terrio と他の選択肢（GDAL、gdal クレート、GeoRust、GeoArrow、whitebox、OxiGeo）：どれを選ぶか
status: draft
terrio_version: 0.5.0
terrio_commit: 6779102281ad2835cbc23fba3138e01a138bc6f9
interface: rust
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-24
verified_on: 2026-10-24
verified_how: read-docs
as_of: 2026-10-21
sources:
  - terrio docs/why-terrio.md（main 6779102）
  - plays/2026-10-21-first-contact.md、plays/2026-10-21-untested-items.md（実測の裏づけ）
related: [terrio-scope-included-and-excluded, terrio-architecture-and-pure-rust-claim, terrio-possibilities-and-risks, hfu-dwg7-workflow-substitution-survey]
---

## 要点

作者自身の整理では、terrio は「**GDAL の結果を基準に、よく使うラスタ・ベクタ形式の入出力・変換・再投影を、純 Rust で**行う」もの。**GDAL の全部の置き換えではない**ことを、ページ自身が断っている。選び分けの目安は、「システムにライブラリを入れられない／WebAssembly で動かしたい／GDAL の `gdal_translate` や `ogr2ogr` を置き換えたい」なら terrio、それ以外（多くの形式、最速の処理、格子つきの測地変換）は GDAL。

## やり方（選び分け、read-docs）

| 選択肢 | 何か | 形式 | 純 Rust / WebAssembly | 再投影 |
|---|---|---|---|---|
| **GDAL** | C/C++ の基準ライブラリとコマンド | 200 超のドライバー | いいえ（ブラウザは Emscripten） | PROJ。完全 |
| **`gdal` クレート** | インストール済みの GDAL への Rust 結合 | その GDAL にあるもの | いいえ（libgdal とヘッダーが要る） | GDAL 経由 |
| **GeoRust のクレート群** | 形状型、アルゴリズム、形式ごとのクレート | 形式ごとに 1 つ | 多くは可 | `proj`（C の PROJ）か `proj4rs`（純 Rust、PROJ 文字列のみ） |
| **GeoArrow / `geoparquet`** | Arrow メモリ上の列指向の形状 | GeoParquet、Arrow IPC など | 可 | 役割外 |
| **whitebox_next_gen** | Whitebox の純 Rust の形式・投影クレート | 多くのラスタとベクタ | 可 | `wbprojection` |
| **OxiGeo**（旧 OxiGDAL） | 別の純 Rust の GDAL 代替 | 約 16（HDF5、GRIB を含む） | 可 | 独自 |
| **terrio** | GDAL を基準にした純 Rust の入出力 | よく使うラスタ・ベクタ・タイル、点群、STAC。残りは任意の GDAL | 可 | 6,354 の EPSG CRS に GDAL の操作 |

**terrio を選ぶ場面**: システムのライブラリなしでビルド・クロスコンパイル・単一バイナリにしたい Rust のプログラム／ブラウザ等での入出力（npm）／COG・PMTiles・COPC を HTTP・`s3://`・`gs://`・`az://` から少しずつ読む／`gdal_translate`、`gdalwarp`、`ogr2ogr` を置き換えたいスクリプトや CI／GDAL の wheel なしで NumPy 配列がほしい Python。

**別のものを使う場面**: File Geodatabase、MrSID、GRIB、HDF、データベースなど terrio にない形式（GDAL を直接、`gdal` クレート、または terrio の `gdal` feature）／今の最速の変換・warp（GDAL。terrio は速い処理も遅い処理もある。`terrio-benchmarks-vs-gdal`）／**格子つきの測地変換や鉛直測地系**（PROJ。ページは「NTv2 などの格子は**まだ適用しない**」と書く）／幾何アルゴリズム（バッファ、交差、簡略化は `geo`）／列指向の分析（GeoArrow、GeoParquet、DuckDB）。

## 確かめたこと（何をして、何が起きたか）

- ページの内容は、上の表と選び分けのとおり（読んだ）。**「格子はまだ適用しない」は、実際の動作とも、`docs/crs.md` とも合わない**（EGM96 は `TERRIO_NETWORK=ON` で適用された。`vertical-datum-grids-and-geoid-in-japan`）。
- 「システムに何も入れなくてよい」は、この環境で `pip install` 1 回で GDAL 相当の処理が動いたことと合う。「GDAL の `gdal_translate`/`ogr2ogr`/`gdalwarp` を置き換えたい」は、`hfu-dwg7-workflow-substitution-survey` で、置き換えやすいもの・難しいものに分けた。
- OxiGeo については、ページが「比較していない」と書く（terrio は形式を絞り、GDAL とファイルごとに突き合わせる方針）。
- 比較表の他のプロジェクトの記述（GeoRust、OxiGeo の形式数など）は、**確かめていない**。

## 気をつけること

- 選び分けは**作者の視点**。他のプロジェクトの側の見方は含まれない。
- 「GDAL の結果が基準」は、日本語パスや CP932 の Shapefile のように、**GDAL が当たり前にできることが、まだできていない**入口もある（`terrio-source-quirks`）。

## 0.5.0 での再確認（2026-10-24）

`docs/why-terrio.md` の変更は 5 行: 「GRIB は terrio にない」という記述が消えた（0.5.0 で GRIB1/2 を読める）。残る「向かない場合」は、File Geodatabase、MrSID、HDF4、データベースなど。read-docs。

## 出典

- https://terrio.opengeos.org/why-terrio/
