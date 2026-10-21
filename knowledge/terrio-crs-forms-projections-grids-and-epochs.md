---
id: terrio-crs-forms-projections-grids-and-epochs
title: 座標系：受け付ける書式、計算できる投影、格子の探し方、高さとエポック
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
  - terrio docs/crs.md（main 6779102）
  - plays/2026-10-21-license-and-basics.md
related: [jgd2011-plane-rectangular-transform, vertical-datum-grids-and-geoid-in-japan, terrio-conformance-and-testing-against-gdal, terrio-release-vs-main-drift]
freshness: high
---

## 要点

座標系は、**EPSG コード（数字だけ、URN、URL を含む）、`OGC:CRS84`、`WGS84`、WKT1/WKT2、PROJ 文字列、ファイルのパス、複合 CRS（`EPSG:4326+5773`）**を受け付ける。**座標は常に GIS の順（x=東・経度、y=北・緯度）**。PROJ の 117 の投影のうち **86 を PROJ と同じに計算し、31 は別のものを計算せずに拒否する**。格子（NADCON5、NTv2、ジオイドなど）は、**見つかれば適用**し、`TERRIO_NETWORK=ON` で PROJ の CDN から取る。**ESRI コード（`ESRI:54009`）は main にあるが、配布版 0.3.2 では「cannot parse」になる。**

## やり方

```sh
terrio crs EPSG:32613                         # 名前
terrio crs EPSG:4326 --to EPSG:32613 -105.5 39.5            # 引数は x y の組
echo "135 -25 0" | terrio crs EPSG:7912 --to EPSG:7843 --s_coord_epoch 2010.0   # 高さとエポックは標準入力
TERRIO_NETWORK=ON TERRIO_GRID_CACHE=/tmp/grids terrio crs EPSG:4267 --to EPSG:4269 -100 40   # NADCON5 を自動取得
TERRIO_GRID_DIR=~/grids terrio crs EPSG:27700 --to EPSG:4258 434422 233624                   # 手元の格子（OSTN15）
```

格子の探す順: メモリに登録 → `TERRIO_GRID_DIR`、`PROJ_DATA`、`PROJ_LIB`、`~/.local/share/proj`、キャッシュ → ネットワーク（`TERRIO_NETWORK=ON` か `PROJ_NETWORK=ON`、CDN は `TERRIO_CDN_ENDPOINT`、キャッシュは `TERRIO_GRID_CACHE`、既定 `~/.cache/terrio/grids`）。**格子が必要な変換は、格子が見つかったときだけ使う**（なければ、GDAL が「格子なし」で挙げる変換）。

## 確かめたこと（何をして、何が起きたか）

**書式（played、0.3.2）**

| 入力 | 結果 |
|---|---|
| `EPSG:32613`、`32613`、`urn:ogc:def:crs:EPSG::32613`、`http://www.opengis.net/def/crs/EPSG/0/32613` | すべて EPSG:32613（WGS 84 / UTM zone 13N） |
| `OGC:CRS84`、`WGS84` | EPSG:4326 |
| `EPSG:5498`（複合）、`EPSG:4326+5773` | 通る（"NAD83 + NAVD88 height"、"WGS 84 + EGM96 height"） |
| `+proj=utm +zone=13 +datum=WGS84` | 通る |
| `+proj=airy`、`+proj=igh` | 拒否: `unsupported projection: PROJ +proj=airy is not supported by wbprojection`（ドキュメントの「拒否する 31」の例と合う） |
| `EPSG:9999999`、`foo` | `unknown EPSG code`、`cannot parse` |
| **`ESRI:54009`、`esri:102003`、`ESRI:54008`** | **0.3.2 では `cannot parse`**。**main（6779102）では通る**（`ESRI:54009` → World_Mollweide、`urn:ogc:def:crs:ESRI::102003` → USA_Contiguous_Albers_Equal_Area_Conic）。ドキュメントは main の記述 |

**格子（played）**: ドキュメントの例 `TERRIO_NETWORK=ON terrio crs EPSG:4267 --to EPSG:4269 -100 40` で、`https://cdn.proj.org/us_noaa_nadcon5_nad27_nad83_1986_conus.tif` を**全体で**取得（139,914 バイト、要求 1 回）し、結果が `-100.0004055982497 40.00000580229538`。ネットワークなし（格子なし）では `-100.00041558862637 39.999996883362` と、約 1 m の差（緯度で 9e-6°、経度で 1e-6°）。
**エポック（played）**: `echo "135 -25 0" | terrio crs EPSG:7912 --to EPSG:7843 --s_coord_epoch 2010.0` は `135.0000030617912 -24.99999469886912 -0.0015074610710144043`、エポックなしは `135 -24.999999999999996 0`（約 0.3 m の差）。**引数で `x y z` を渡すと `coordinates come in x y pairs` になる**（3 次元は標準入力）。

**高さと鉛直測地系（read-docs、一部 played）**: 高さを持つ CRS の間（`EPSG:4979`、複合 CRS）では、ジオイドモデル（EGM96、EGM2008、GEOID18、OSGM15 など）が高さを楕円体高と相互に変える。**適用できる格子がないと高さは保たれる**（PROJ の ballpark と同じ）。鉛直 CRS どうしは楕円体高を経由し、PROJ の直接の鉛直変換（VERTCON など）は使わない。**日本のジオイドは、3 次元の CRS（`EPSG:6667`）から `EPSG:6697` に変換すれば適用される**（2 次元の `EPSG:6668` では、GDAL も高さを変えない。`vertical-datum-grids-and-geoid-in-japan`）。

**動的測地系（read-docs）**: ITRF、WGS 84 の実現、ETRF などは、座標のエポックに依存する。動的 → 静的は元のエポック、静的 → 動的は先のエポック。15 パラメータのヘルマート変換と速度格子に対応。

**識別（read-docs）**: EPSG コードのない WKT（Shapefile の `.prj` など）は、測地系・変換・単位から EPSG コードを推定する（NYC の区の Shapefile は EPSG:2263、ESRI の `GCS_European_1950` は EPSG:4230、と GDAL と同じ）。**複数の候補は、名前、軸順、基本の測地系、最小のコードの順**に選ぶ。

**投影と回転極（read-docs）**: PROJ の 117 の投影のうち、86 を 1 mm 以内で PROJ と同じに計算（`crates/terrio/tests/proj_strings.rs`）。**既知の差**: Bessel 楕円体の Krovak（PROJ の逆変換が順変換の逆でない）。回転極のグリッド（CORDEX、COSMO-CLM）は PROJ 文字列、WKT2、CF の `rotated_latitude_longitude` で読む（`is_rotated_pole()`）。

**GDAL との近さ（read-docs）**: 同じ格子なら GDAL と**マイクロメートルまで**（250 ケース、5 万点、最大差 0.02 mm）。すべての EPSG CRS の基準点は 1 cm 以内。**CRS から CRS は、組の 97.5% で全点が 1 cm 以内、98.8% で 1 m 以内**（PROJ は複数の中間の測地系を連鎖させるが、terrio は 1 つだけ試す）。

## 気をつけること

- 軸順は**常に x（東）、y（北）**。EPSG:6668 の権威の軸順（緯度・経度）とは違う（`jgd2011-plane-rectangular-transform`）。
- **格子は、ネットワークをオンにするか、手元に置かないと使われない**。既定は格子なし（黙って精度が落ちる）。日本の水平格子は PROJ の CDN に存在しない。
- 「CRS から CRS」の 1 m 以内は 98.8%。**測量用途には使わない**。
- 格子は `TERRIO_GRID_CACHE` に置く。`TERRIO_NETWORK=ON` は実行時にネットワークへ出る。許可リストの環境では `cdn.proj.org` が要る。

## 出典

- https://terrio.opengeos.org/crs/
- plays/2026-10-21-license-and-basics.md
