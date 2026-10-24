---
id: terrio-cli-overview
title: terrio コマンドラインの概要（GDAL のどのコマンドに当たるか）
status: stale
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、PyPI の wheel）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
interface: cli
verified_on: 2026-10-21
verified_how: read-docs
sources:
  - terrio docs/cli.md、docs/gdal.md（v0.3.2 と main cf6bd5d）
  - "`terrio --help` の出力（plays/2026-10-21-first-contact.md）"
related: [terrio-scope-included-and-excluded, terrio-release-vs-main-drift]
---

## 要点

`terrio` は、GDAL / OGR / PDAL の主なコマンドを、C ライブラリなしで再実装した単一のコマンド。`pip install terrio` で入る。入力は、ローカルパス、URL、`s3://` `gs://` `az://`、zip の中身（`a.zip!dir/x.shp`）、GDAL 流の `/vsicurl/` など。**出力はローカルのみ**。

| terrio | GDAL / PDAL での相当 | 用途 |
|---|---|---|
| `info` | gdalinfo, ogrinfo -so | 概要（`--json` `--stats` `--hist`） |
| `convert` | ogr2ogr、gdal_translate の形式変換 | 形式変換と再投影。`--srcwin` `--overview`（ラスタ）、`--where` `--spat` `--sql`（ベクタ） |
| `translate` | gdal_translate | 窓切り出し、型変換、リサイズ、値の変換 |
| `warp` | gdalwarp | 再投影・リサンプリング |
| `mosaic` | gdalbuildvrt, gdal_merge.py | モザイク（`.vrt` か実体） |
| `rasterize` / `polygonize` | gdal_rasterize / gdal_polygonize.py | ベクタ⇔ラスタ |
| `dem` | gdaldem | 陰影、傾斜、方位、色別標高、TRI、TPI、粗度 |
| `calc` | gdal_calc.py | NumPy 記法のバンド演算 |
| `proximity` / `sieve` | gdal_proximity.py / gdal_sieve.py | 距離、小領域の併合 |
| `crs` | gdalsrsinfo, gdaltransform | 座標系の説明と座標変換（`--to`） |
| `formats` | gdalinfo --formats | 対応形式の一覧 |
| `grid` / `filter` | PDAL の writers.gdal / filters | 点群のラスタ化、地面分類などのフィルタ |
| `mcp` | （なし） | AI エージェント向け MCP サーバー。**v0.3.2 のリリースには入っていない**（`terrio-release-vs-main-drift`、`terrio-mcp-server`） |

## やり方

```sh
pip install --upgrade terrio
terrio --version
terrio info URL            # 概要
terrio formats             # 形式
terrio <コマンド> --help   # 全オプション
```

## 確かめたこと（何をして、何が起きたか）

- `terrio --help` は 15 個のサブコマンド（`mcp` を除く）を出す。この一覧と上の表の対応は、`docs/gdal.md` の対応表と `--help` の説明文（"like gdal_translate" など）から作った（**読んで確認**。表の「相当」の厳密な同等性までは確かめていない）。
- 動かしたのは `info` `convert` `translate` `warp` `crs` `formats`（`plays/2026-10-21-first-contact.md`）と、`dem` `calc` `mosaic` `rasterize` `polygonize` `proximity` `sieve` `grid` `filter`（`terrio-processing-commands-smoke-test`）。`mcp` は main のビルドで確認した（`terrio-mcp-server`）。値の正しさは、どれも未検証。

## 気をつけること

- GDAL のオプション名は、ほぼ「ハイフン付きの kebab-case」に対応する（`-t_srs` → `--t-srs`、`-co COMPRESS=DEFLATE` → `--compress DEFLATE`）。同じ名前とは限らない（`docs/gdal.md` の対応表を見る）。
- `crs --to` の座標は `x y`（経度 緯度、東 北）の順。緯度・経度の順だと失敗する（`jgd2011-plane-rectangular-transform`）。
- ヘルプは長い。`--help` が一番新しい。

## 出典

- https://terrio.opengeos.org/ （docs/cli.md、docs/gdal.md）
- `terrio --help`（terrio 0.3.2）
