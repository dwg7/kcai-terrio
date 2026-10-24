---
id: terrio-conformance-and-testing-against-gdal
title: GDAL との突き合わせ試験と適合性レポート：何を、いつ、どの版で比べたか
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
as_of: 2026-10-14
sources:
  - terrio docs/testing.md、docs/conformance.md、scripts/proj_grids.txt（main 6779102）
  - plays/2026-10-21-license-and-basics.md
related: [terrio-benchmarks-vs-gdal, terrio-point-clouds, vertical-datum-grids-and-geoid-in-japan, terrio-overview-and-getting-started, terrio-source-quirks]
freshness: high
---

## 要点

terrio は「GDAL を基準に、実データで突き合わせる」と明言し、**比較のスクリプトと、生成されるレポート（`docs/conformance.md`）を公開している**。レポートは **40,068 件（同一 39,861、許容内 177、差異あり 30）**。**ただし、ほとんどの比較は 2026-10-14 の terrio 0.1.1 で実行されたもの**（座標変換の 2 つの試験だけ 2026-10-21 の 0.3.2）。**この遊びでは、GDAL との突き合わせは行っていない**（環境に GDAL がなく、方針でも目的にしていない）ので、レポートの数字は**作者の主張として**読む。

## やり方（読み方）

- 試験データは `scripts/fetch_test_data.sh` が公開データから取る（Natural Earth、USGS 3DEP、NASA ECOSTRESS・OPERA、Landsat・SRTM・NLCD、米国の郡（FlatGeobuf）、NYC、Las Vegas、OSM（リヒテンシュタイン）、netCDF、JPSS・VIIRS、Sentinel-5P、Sentinel-2 の JPEG 2000、GDAL が各圧縮で書いた GeoTIFF など）。
- `scripts/conformance.py` が全スイートを回して Markdown のレポートを書く。個別の比較スクリプトは、`compare_with_gdal.py`、`compare_windows_with_gdal.py`、`compare_ops_with_gdal.py`、`compare_dem_calc_with_gdal.py`、`compare_tiles_with_gdal.py`、`compare_pointclouds.py`、`compare_rio_with_rasterio.py`、`compare_remote_zarr.py` など（領域ごと）。**PR ごとに CI で回る**（点群は PR では `autzen_trim.las` だけ、main へのプッシュで 400 万点の Madison も）。Rust のテストには GDAL の期待値が入っていて、GDAL なしで動く（比較スクリプトは GDAL の Python 結合が要る）。
- 比べる基準は GDAL 3.12.2、PROJ 9.7.1（座標は 9.8.1）、PDAL 2.9.3、laspy 2.7.0。

## 確かめたこと（何をして、何が起きたか）

**レポートの要約（read-docs）**

| スイート | 件数 | 同一 | 許容内 | 差異 |
|---|---:|---:|---:|---:|
| 概要と画素 | 64 | 64 | 0 | 0 |
| ベクタ変換（GDAL が読み戻す） | 23 | 23 | 0 | 0 |
| ラスタのドライバー | 487 | 487 | 0 | 0 |
| 窓・overview の読み | 186 | 186 | 0 | 0 |
| ラスタの操作（translate、warp、mosaic） | 49 | 42 | 7 | 0 |
| 地形・ラスタ代数 | 131 | 129 | 2 | 0 |
| ベクタ操作 | 51 | 51 | 0 | 0 |
| Arrow / GeoArrow | 180 | 171 | 9 | 0 |
| GeoPackage の更新・空間フィルター | 12 | 12 | 0 | 0 |
| 点群 | 615 | 609 | 6 | 0 |
| **座標変換**（6,354 の EPSG CRS、各 50 点） | 19,017 | 18,950 | 59 | **8** |
| **格子・ジオイド・エポック** | 19,253 | 19,137 | 94 | **22** |
| 合計 | 40,068 | 39,861 | 177 | 30 |

- 差異あり 30 件は、すべて**座標変換**（CRS から CRS が 8、格子つきが 22）。ラスタ・ベクタ・点群には差異ありはない。`warp` の「許容内」は、float32 の丸めの 1 段で、最大 7 画素（「入力の座標は PROJ ではなく terrio の投影計算から来る」ため）。`calc` の 2 件は NumPy の float32 の `sin`、`exp` などの丸め。
- **レポートの日付**: 「2026-10-14、terrio 0.1.1（9e7f7f5）」。座標変換の 2 つは「2026-10-21、terrio 0.3.2、PROJ 9.8.1」。**配布版 0.3.2 の他の領域は、この日付以降に再実行されたかは書かれていない**。
- **日本の座標系**: 「EPSG の各 CRS に 50 点」の試験に JGD2011（6668）や平面直角座標系（6669〜6687）は**含まれるはず**だが、レポートには日本の CRS の個別の行はない（`grep` で 0 件）。**格子の試験で使う `scripts/proj_grids.txt`（128 行）に、日本の格子（`jp_`）は 0 件**。日本の格子の検証は、terrio の試験にない。私たちの突き合わせでは、3 次元の CRS から変換すれば、同じ格子で GDAL と小数 11 桁まで一致した（`vertical-datum-grids-and-geoid-in-japan`）。

**ドキュメントの例を動かしたときの一致（played）**: 点群の COPC の例（要求の数と点数）が一致した（`terrio-point-clouds`）。FlatGeobuf の `--spat` は全量取得で、ドキュメントの「FlatGeobuf（空間インデックスつき）」は**ローカルの話**（`terrio-formats-vectors-streaming-and-tiles`）。

## 気をつけること

- 試験の範囲は**英語・米国・欧州のデータ中心**（Natural Earth、USGS、NYC、Las Vegas、リヒテンシュタインなど）。**日本語の文字列・パス、CP932 の Shapefile、日本の格子は、試験の範囲外のようだ**。実際に、日本語の panic が 3 か所、CP932 の文字化けが見つかった（ジオイドは、3 次元の CRS から変換すれば GDAL と一致）。この環境で GDAL 3.8.4 と突き合わせた約 30 項目の結果は `terrio-vs-gdal-spot-checks`。試験データの追加が、上流への貢献になりうる（下書き、投稿は hfu が確認）。
- 「同一」の判定は、数値の許容（例: 相対 1e-6、統計 1e-4）つき。「画素ごとに同一」は画素値の完全一致。
- レポートは**生成物**で、版ごとに書き換わる。`stale` の運用で追う。

## 0.5.0 での再確認（2026-10-24）

`docs/conformance.md`（2026-10-14 の 0.1.1 の結果に、2026-10-21 の 0.3.2 での座標変換の検査を足した版）: 座標変換 19,017 件（一致 19,002・許容内 13・差 2）、格子・ジオイド・エポック 19,253 件（一致 19,223・許容内 28・差 2）、**全体 40,068 件のうち 39,999 件が一致・65 件が許容内・4 件が差あり**。差ありの例: EPSG:6054 → 4287（267 m）、EPSG:29183 → 20823（208 m）。さらに 0.5.0 には、トポロジー（`compare_topology_with_gdal.py`）、GRIB、STACTA（99/99）、PROJ の鎖（`crs_chains.rs`）の検査が加わった。作者の検査で、この遊びでは再実行していない。read-docs。

## 出典

- https://terrio.opengeos.org/testing/ 、https://terrio.opengeos.org/conformance/
- plays/2026-10-21-license-and-basics.md
