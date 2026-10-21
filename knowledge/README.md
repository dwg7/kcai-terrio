# 知識の塊の一覧

`status` は kcai の `draft | reviewed | stable | deprecated` に、このリポジトリ独自の `stale`（新しい版でまだ確かめ直していない）を足したもの。AI は `reviewed` 以上にしない。形式は `AGENTS.md`。

| 塊 | 状態 | 確かめた版 | 確かめた日 | 確かめ方 |
|---|---|---|---|---|
| [クラウドネイティブな形式の読み込み方：どこまで範囲読み込みか（一覧）](cloud-native-read-behavior-matrix.md) | draft | 0.3.2 | 2026-10-21 | played |
| [リモート COG の窓読み・overview・縮小の使い分け](cog-remote-window-overview-and-warp.md) | draft | 0.3.2 | 2026-10-21 | played |
| [日本語の長い文字列を含む GeoJSON と CSV で terrio が panic する（0.3.2）](geojson-japanese-string-panic.md) | draft | 0.3.2 | 2026-10-21 | played |
| [hfu と dwg7 の公開リポジトリの処理のうち、terrio で代替できそうなものと、できなさそうなもの](hfu-dwg7-workflow-substitution-survey.md) | draft | 0.3.2 | 2026-10-21 | read-source |
| [日本語から始まる相対パスで terrio が panic する（Zarr 名の判定）](japanese-path-panic-in-zarr-parse-name.md) | draft | 0.3.2 | 2026-10-21 | played |
| [JGD2011 と平面直角座標系（EPSG:6669〜6687）の変換と、測地系のずれ](jgd2011-plane-rectangular-transform.md) | draft | 0.3.2 | 2026-10-21 | played |
| [PMTiles をリモートで読む（ラスタ・ベクタ、日本語属性、Range を無視する配信）](pmtiles-remote-reading.md) | draft | 0.3.2 | 2026-10-21 | played |
| [CP932（Shift_JIS）の Shapefile 属性が、黙って文字化けする](shapefile-cp932-attributes-not-decoded.md) | draft | 0.3.2 | 2026-10-21 | played |
| [terrio コマンドラインの概要（GDAL のどのコマンドに当たるか）](terrio-cli-overview.md) | draft | 0.3.2 | 2026-10-21 | read-docs |
| [terrio が開く可能性と、使うときのリスク](terrio-possibilities-and-risks.md) | draft | 0.3.2 | 2026-10-21 | played |
| [リリース版（PyPI の 0.3.2）と main のずれ：ドキュメントは先行する](terrio-release-vs-main-drift.md) | draft | 0.3.2 | 2026-10-21 | played |
| [terrio が含む機能と含まない機能](terrio-scope-included-and-excluded.md) | draft | 0.3.2 | 2026-10-21 | read-docs |
| [terrio のソースコードの癖（規模、作り、同じ型の弱点）](terrio-source-quirks.md) | draft | 0.3.2 | 2026-10-21 | read-source |
| [格子とジオイド：EGM96 は適用されるが、日本のジオイドは適用されなかった](vertical-datum-grids-and-geoid-in-japan.md) | draft | 0.3.2 | 2026-10-21 | played |

`played` は実際に動かした。`read-docs` / `read-source` は読んだだけ。

## 読む順序の目安

1. 全体像: `terrio-cli-overview`、`terrio-scope-included-and-excluded`、`terrio-release-vs-main-drift`
2. クラウドネイティブ: `cloud-native-read-behavior-matrix`（一覧表）、`cog-remote-window-overview-and-warp`、`pmtiles-remote-reading`
3. 日本ローカル: `jgd2011-plane-rectangular-transform`、`vertical-datum-grids-and-geoid-in-japan`、`shapefile-cp932-attributes-not-decoded`、`japanese-path-panic-in-zarr-parse-name`、`geojson-japanese-string-panic`
4. 評価: `terrio-source-quirks`、`terrio-possibilities-and-risks`、`hfu-dwg7-workflow-substitution-survey`
