---
id: terrio-cli-command-reference
title: コマンドごとの主なオプションと決まり（cli.md の要約と、確かめた点）
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
  - terrio docs/cli.md、docs/gdal.md（main 6779102）
  - "`terrio <command> --help`（0.3.2）"
  - plays/2026-10-21-license-and-basics.md
related: [terrio-cli-overview, terrio-processing-commands-smoke-test, terrio-formats-vectors-streaming-and-tiles, terrio-point-clouds]
---

## 要点

`terrio-cli-overview` の表の各コマンドについて、**オプションと決まり**を、ドキュメントの要約と、確かめた点で整理する。入力は、パス、URL、クラウドのオブジェクト、zip のメンバー。**出力はローカル**。

## やり方（コマンド別）

| コマンド | 主なオプション・決まり | 確かめたこと |
|---|---|---|
| `info` | `--json`、`--stats`、`--hist`、`-l 層`。リモートの GeoTIFF はヘッダーだけ。netCDF/HDF5/GeoPackage の subdataset を列挙 | `--json` のキーは `type driver size band_count geo_transform crs extent wgs84_extent bands metadata`。`--hist` は 256 バケットを出す |
| `convert` | 形式は拡張子か `-f`。`--t-srs`。ラスタ: `--compress` `--tile-size` `--bigtiff` `--srcwin` `--overview`。ベクタ: `--where`（OGR SQL）`--spat` `--select` `--limit` `--sql` `--nln` `--nlt` `--append` `--overwrite` `--oo` `--lco`。点群: `--bounds` `--max-level` `--resolution` `--class` `--returns` など。タイル: `--minzoom` `--maxzoom` | `--append` / `--overwrite` は GeoPackage で動いた。**`--ot` は `convert` にない**（`translate` にある） |
| `translate` | `--srcwin`、`--projwin`（+ `--projwin-srs`）、`-b`、`--ot`、`--scale`、`--exponent`、`--outsize`、`--tr`、`-r`、`--a-nodata`、`--a-srs`、`--a-ullr` | **`--outsize` の縮小は全解像度を読む**（リモート COG で約 208 MiB）。`--ot Int16` でも nodata が範囲外のまま |
| `warp` | `--t-srs` `--s-srs` `--tr` `--te`（+`--te-srs`）`--ts` `--tap` `-r`（near、bilinear、cubic、cubicspline、lanczos、average、rms、mode、min、max、med、q1、q3、sum）`--srcnodata` `--dstnodata` `--ot` `--cutline`（+`--crop-to-cutline`）`--et` `--order` `--tps`。複数入力はモザイク。GCP と回転した入力に対応 | `-r` の一覧は `--help` と一致。**`--dstalpha` はない** |
| `mosaic` | `--resolution highest|lowest|average|user` `--tr` `--te` `--separate` `--nodata` `-r` `--t-srs`。`.vrt` は GDAL の VRT（入力を参照）、他は画素を持つ | `.vrt` と `.tif` の両方が動いた |
| `rasterize` | `--burn` か `-a`、`--tr` か `--ts` か `--like`、`-l` `--sql` `--where` `--te` `--ot` `--init` `--at`（接した画素すべて）`--add` | `--burn` と `-a` で動いた（JGD2011 の 0.001° 格子） |
| `polygonize` | `-b`、`--field`（**既定 `DN`**）、`--nln`、`--8`、`--nomask`、`--mask`、`--append` `--overwrite`。穴あきポリゴン、外環は反時計回り | 既定の属性名 `DN` を確認 |
| `dem` | `hillshade` `slope` `aspect` `color-relief` `TRI` `TPI` `roughness`。`--alg Horn|ZevenbergenThorne`（TRI は Riley|Wilson）、`-z` `-s`（地理座標の DEM は 111120）`--az` `--alt` `--combined` `--multidirectional` `--igor` `-p` `--trigonometric` `--zero-for-flat` `--alpha`。`-s` なしの地理座標 DEM は中心緯度から尺度を決める（GDAL 3.11 以降と同じ）。カラーファイルは GDAL の形式か GMT の `.cpt` | `--multidirectional --alg ZevenbergenThorne`、`aspect --trigonometric` が動いた |
| `calc` | `-A`/`--A_band`（gdal_calc.py 流）か `--input NAME=PATH`。NumPy 構文（`where` `clip` `minimum` `maximum` `abs` `sqrt` `exp` `log` 三角関数 `A.astype(float32)`、定数 `pi` `e` `nan` `inf`）。**NumPy の型規則: 整数の演算は桁あふれ、`/` は float64、Python の数は配列の型に合わせる**。`--calc` を繰り返すと 1 つずつバンド。`--type` `--NoDataValue` `--hideNoData` `--extent` `--projwin` | **Byte の `A*60` が桁あふれ**（値 4,5,6 → 240,44,104）。**`A/5`（`--type` なし）は出力が Byte になり、値は 1 に丸まる**（`--type Float32` で 0.8〜1.2）。入力の nodata と等しい画素は出力が nodata。**GDAL 3.8.4 の `gdal_calc.py` も同じ**（`A*60` は桁あふれ、`A/5` は Byte）で、terrio の不具合ではなく、GDAL と同じ既定（`terrio-vs-gdal-spot-checks`） |
| `proximity` | `--values 1,2` `--distunits PIXEL|GEO` `--maxdist` `--srcband` `--nodata`（既定 65535）`--use-input-nodata` `--fixed-buf-val` `--ot`（既定 Float32） | `--values 6 --distunits GEO` が動いた |
| `sieve` | `--st`（既定 2）、`-4`/`-8`、`--nomask`、`--mask`。小さな領域は最大の隣に併合 | `--st 20` で 1,260 → 85 ポリゴン |
| `crs` | `crs CRS [--wkt]`、`crs SRC --to DST X Y …`、標準入力 `X Y [Z [T]]`、`--s_coord_epoch` `--t_coord_epoch`。変換できない点は `transformation failed.` | 座標は「経度 緯度」（`jgd2011-plane-rectangular-transform`）。高さは標準入力 |
| `formats` | `--json` | 49 行。表との一致（`terrio-formats-rasters-and-compression`） |
| `grid` | `--tr`（**必須**）`--stat min,max,mean,idw,count,stdev|all` `--dim z` `--radius` `--power` `--window-size` `--bin` `--te` `--class` `--returns` `--bounds` `--method` | DSM は `--stat max`、DTM は `--class 2 --stat idw`、密度は `--stat count --bin`（動いた） |
| `mcp` | `terrio mcp`（標準入出力の MCP サーバー） | main のみ（`terrio-mcp-server`） |

## 確かめたこと（何をして、何が起きたか）

- 上の表の「確かめたこと」の列のとおり。`polygonize` の既定の属性 `DN`、`warp -r` の一覧、`formats --json` の形、`--hist` などは、ドキュメントと実際が合った。
- `dem` は「`gdaldem` と画素ごとに同一」、`warp` は「`GDALSuggestedWarpOutput2` と同じ既定の出力格子」、`rasterize` は「GDAL のアルゴリズムで画素ごとに同一」と書く（**未検証**）。

## 気をつけること

- **型の既定**: `calc` は、入力の型で出力を決めるので、割り算や引き算は `astype` と `--type` を付ける。`translate` / `convert` の `--ot` の違い（`convert` にはない）。
- **GDAL とオプション名が違う所**: `grid` の `--tr`、`--stat`（PDAL 流）、`--dst-transform`（`warp` の独自拡張）など。
- 出力のリモート書き込みはできない。

## 出典

- https://terrio.opengeos.org/cli/ 、https://terrio.opengeos.org/gdal/
- plays/2026-10-21-license-and-basics.md
