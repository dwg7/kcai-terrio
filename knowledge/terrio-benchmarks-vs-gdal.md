---
id: terrio-benchmarks-vs-gdal
title: GDAL との速度とメモリの比較（作者の計測）と、読むときの注意
status: draft
terrio_version: 0.3.2
terrio_commit: 6779102281ad2835cbc23fba3138e01a138bc6f9
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: read-docs
as_of: 2026-10-21
sources:
  - terrio docs/benchmarks.md（main 6779102）
related: [terrio-conformance-and-testing-against-gdal, terrio-architecture-and-pure-rust-claim, why-terrio-comparison-with-alternatives]
freshness: high
---

## 要点

作者の計測では、**小さなファイルで 1.2〜16 倍、1 GB 級で 1.0〜13.6 倍、terrio が速い**。メモリは、多くで terrio が少なく、**JPEG 2000 の GeoTIFF 化と OSM PBF の GeoPackage 化では terrio のほうが多い**。ページ自身が「**スナップショットとして読むこと**。terrio は若く、GDAL との一致を先にした」と断る。**この環境には GDAL がなく、この遊びでは計測を再現していない**。

## やり方（読み方）

- 計測の条件（作者）: Intel Xeon w7-3445、40 スレッド、Linux、GDAL 3.12.2、各コマンドを新しいプロセスで、ウォームアップ 1 回の後に 5 回の中央値（大きなファイルは 3 回）。**小さなファイルは terrio 0.0.1、大きなファイルは 0.2.0** の時点。`scripts/benchmark.py` で再実行できる（GDAL の CLI が `PATH` に要る。大きなデータは約 3.5 GB を取る）。

## 確かめたこと（何をして、何が起きたか）（read-docs）

| 作業 | terrio | GDAL | 倍率 |
|---|---|---|---|
| ラスタ `info`（USGS 3DEP の 3612²） | 14 ms | 43 ms | 3.1 倍 |
| GeoTIFF → COG（Deflate、同タイル） | 224 ms | 1.20 s | 5.3 倍 |
| Warp（UTM 13N、bilinear、同タイル） | 142 ms | 1.10 s | 7.7 倍 |
| モザイク → VRT（4 タイル） | 2 ms | 35 ms | 16.5 倍 |
| Shapefile → GeoPackage（7,342 点） | 39 ms | 82 ms | 2.1 倍 |
| GeoPackage → FlatGeobuf（米国の郡） | 49 ms | 61 ms | 1.2 倍 |
| 米国の郡のラスタ化（0.01°） | 158 ms | 314 ms | 2.0 倍 |
| リモート COG の `info`（S3） | 451 ms | 587 ms | 1.3 倍 |
| **大**: 14412² のモザイクの COG 化 | 1.54 s（784 MB） | 20.98 s（1.2 GB） | 13.6 倍 |
| **大**: 同モザイクの hillshade | 593 ms（371 MB） | 4.55 s（855 MB） | 7.7 倍 |
| **大**: 線 200 万 → GeoJSON | 3.48 s | 42.69 s | 12.3 倍 |
| **大**: Sentinel-2 の JP2 → GeoTIFF | 478 ms（**753 MB**） | 3.23 s（517 MB） | 6.8 倍（メモリは多い） |
| **大**: OSM PBF（Colorado）→ GeoPackage | 21.40 s（**986 MB**） | 45.21 s（455 MB） | 2.1 倍（メモリは多い） |

- 注: 「`info` が速い」のは、GeoTIFF のヘッダーだけを読むため。「モザイクの VRT が速い」のは、入力のヘッダーだけを読むため（GDAL は各入力を開く）。リモート COG の `info` は 64 KiB の範囲 1 回（この環境でも 1 要求・64 KiB を確認）。`info` の GPKG の範囲は、全地物の形状を復号して求める（GDAL は `gpkg_contents` の値）。
- 大きなベクタは、最大 65,536 地物、約 64 MB ずつ。大きなラスタは、窓で読み、行の帯で書く。JP2 の帯は全体を復号する。
- **この環境の観察（played）**: `terrio info` のリモート COG は 1 要求 64 KiB（0.6 秒）。5 GB の GeoParquet の `info` は、CLI では全量取得で、ベンチマークの「リモート」は COG だけ（`cloud-native-read-behavior-matrix`）。

## 気をつけること

- **並列で速い**: 作者の計測機は 40 スレッド。`nproc` が少ない環境（クラウドのセッションなど）では差が縮む、とページ自身が書く。
- 「速い」は、**同じ結果**を前提にした比較（出力は GDAL と同一、という主張。`terrio-conformance-and-testing-against-gdal`）。
- 小さなファイルの数値は **terrio 0.0.1 の時点**で、現行の 0.3.2 の速度とは限らない。**この遊びでは計測していない**（大きなファイルを取らない方針のため）。
- 日本語のパスで panic する等、**速さ以前の入口**の問題は、ここに現れない（`terrio-source-quirks`）。

## 出典

- https://terrio.opengeos.org/benchmarks/
