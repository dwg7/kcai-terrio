---
id: terrio-point-clouds
title: 点群（LAS/LAZ/COPC/EPT/PLY/E57）：範囲読み、フィルター、グリッド化、ドキュメントの例の再現
status: stale
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-24
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - terrio docs/point-clouds.md（main 6779102）
  - Autzen の COPC（https://s3.amazonaws.com/hobu-lidar/autzen-classified.copc.laz、81 MB）
  - plays/2026-10-21-untested-items.md、plays/2026-10-21-license-and-basics.md
related: [cloud-native-read-behavior-matrix, terrio-processing-commands-smoke-test, terrio-cli-command-reference, terrio-conformance-and-testing-against-gdal]
freshness: high
---

## 要点

点群は **LAS 1.0〜1.4（点形式 0〜10、波形つき）、LAZ、COPC、EPT、PLY、E57** を読み書きできる（純 Rust。LASzip は `laz` クレート、E57 は `e57` クレート）。**COPC は、クラウドから「必要な範囲と粗さ」だけを範囲読みする**。ドキュメントの Autzen の例を、そのまま打って**要求の数も点数も再現できた**。PDAL のフィルターを 20 種持ち、DEM 化（`grid`）もできる。

## やり方

```sh
C=https://s3.amazonaws.com/hobu-lidar/autzen-classified.copc.laz
terrio info $C                                                      # 2 要求、118 KiB
terrio convert $C sub.laz --bounds 637000 851000 637500 851500 --resolution 7.27   # 8 要求、3.5 MiB、18,901 点
terrio convert $C sub.laz --bounds … --max-level 2                  # レベルで絞る（--max-points でも）
terrio filter smrf tile.laz classified.laz                          # 地面分類
terrio grid tile.laz dsm.tif --tr 1 --stat max                      # DSM。DTM は --class 2 --stat idw
```

## 確かめたこと（何をして、何が起きたか）

**ドキュメントの例の再現（played）**

| ドキュメントの記述 | 実測（0.3.2） |
|---|---|
| `info`: 2 要求、120 kB（81 MB のうち） | 2 要求、**118 KiB** |
| `convert --bounds 637000 851000 637500 851500 --resolution 7.27`: 8 要求、3.7 MB、18,901 点（PDAL の `readers.copc` と同じ点） | 8 要求、**3,574 KiB**、**18,901 点**（点数が一致。PDAL とは比べていない） |

**そのほかの COPC（played）**: 700 ft 四方の `--bounds` が 21 要求・6.9 MiB（304,487 点）、`--max-level 2` を足すと 5 要求・1.6 MiB（11,880 点）、全域で `--max-level 1` が 3 要求・1.7 MiB（131,060 点）。

**フィルター（played、Autzen の 700 ft 四方の切り出し 44,465 点で）**

| コマンド | 結果 |
|---|---|
| `filter outlier --method statistical --mean-k 8 --multiplier 2 --remove` | 43,287 点 |
| `filter voxeldownsize --cell 10 --mode first` | 7,395 点 |
| `filter expression --expression "Z > 450"` | 19,030 点 |
| `filter crop --polygon "POLYGON((…))"` | 10,723 点 |
| `filter assign --value "Classification = 7 WHERE Z < 430"` | 44,465 点（値だけ変わる） |
| `filter splitter --length 350 "sp_#.laz"` | 9 ファイル |
| `filter merge v.laz e.laz` | 26,425 点（= 7,395 + 19,030） |
| `filter cluster` | 次元 `cluster_id` が付く |
| `filter normal` | 次元 `normal_z` などが付く（snake case。PDAL の名前を snake case にしたもの） |
| `convert … --class 2 --returns last,only`（`smrf` 後） | 36,297 点 |
| `filter smrf` → `hag_nn`、`grid`（min/max/mean/idw/count/stdev、`--bin`、`--method linear|nearest`） | 動いた（前の踏み跡）。結果の正しさは未検証 |

**形式の往復（played）**: LAZ から PLY、E57、EPT（`pcept/ept.json`）、COPC へ書き、読み戻した点数が 44,465 で一致。COPC は `LAS 1.4、点形式 7`。

**ドキュメントの内訳（read-docs）**
- 全次元を読む（余分なバイトも）。CRS は WKT レコードか GeoKeys（複合 CRS は水平と鉛直に分ける）。次元は laspy の名前（`x`、`y`、`z`、`intensity`、`return_number`、`classification`、`gps_time`、`red`…）、LAS にないものは PDAL の名前の snake case（`normal_x`、`origin_id`）。
- **EPT**: ローカルも、`https://` と `s3://` もその場で読む（bounds、resolution、max-level）。書き出しは COPC と同じ八分木（立方体、1 セル 1 点の 128³ の格子、ノードは最大 10 万点）。例: USGS 3DEP の Wisconsin（115 億点）から 347,376 点を 10 秒（PDAL と同じ点）。
- **メモリを超える大きさ**: `convert`、`info --stats`、`grid`、`filter range/expression` は、100 万点ずつ（`--chunk-points`）。3.05 GB の LAS（1.017 億点）で、`info --stats` 18.5 秒・66 MB、`convert` LAS→LAZ 139 秒・117 MB、LAZ→COPC 267 秒・251 MB、`grid` 25 秒・769 MB（PDAL の `writers.gdal` は 52 秒・6.3 GB）。COPC と EPT の書き出しは、一時ファイルを `TMPDIR` に置く。
- **フィルター 20 種**（PDAL の名前と既定）: `smrf`、`pmf`、`csf`（地面）、`elm`、`outlier`、`hag_nn`、`hag_delaunay`、`range`、`expression`、`assign`、`crop`、`decimation`、`merge`、`splitter`、`chipper`、`sample`、`voxeldownsize`、`voxelcenternearestneighbor`、`normal`、`cluster`。PDAL の癖も再現する、と書く。再投影は `convert --t-srs`。すべて `--a-srs` で CRS を付け直せる。
- 波形（点形式 4、5、9、10）は読み、LAS/LAZ へ保つ。PLY は ASCII が既定（`--ply-encoding binary_little_endian`）。E57 は全スキャンを姿勢つきで読む。

## 気をつけること

- **PDAL と同じ結果**という主張（laspy と 55 ファイルで全次元が同一、PDAL と比較など）は、ドキュメントの比較表のもの。この遊びでは、**点数の一致を 1 件確かめただけ**（18,901 点）。
- TIN のグリッド（`--method linear`）は、`gdal_grid` と **99.91% のセルが一致**で、完全一致ではない（ドキュメントが断っている）。
- `TMPDIR` に一時ファイルを置く書き出しがあるので、サイズに注意（`terrio-possibilities-and-risks`）。
- フィルターの結果の中身（分類の正しさ）は、見ていない。

## 0.4.2 での再確認（2026-10-24）

terrio **0.4.2** で、COPC（44,465 点）の `info` と `filter range`（`Classification[2:2],Z[450:460)` → 1313 点、`Z[500:)` → 6720 点）は、PDAL 2.10.2 と一致した値のまま。played（部分）。点群の他の機能は確かめ直していない。main は PDAL のフィルタを多数足した（#210、#205）。

## 出典

- https://terrio.opengeos.org/point-clouds/
- plays/2026-10-21-untested-items.md 、plays/2026-10-21-license-and-basics.md
