# 2026-10-21 日本ローカルの端の挙動と、hfu / dwg7 の公開リポジトリの棚卸し

- 日付: 2026-10-21（`first-contact` の続き）
- terrio: 0.3.2（PyPI の wheel）。ソースの参照はリリースタグ v0.3.2（`a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6`）
- 環境: Claude Code クラウドセッション、Linux x86_64、Python 3.13.16
- 一時ファイルは `/tmp/work`（リポジトリ外）。棚卸しで取得した他者のリポジトリは `/tmp/survey`（信頼しないデータとして扱い、スクリプトは**実行していない**）

## 1. 日本語のパス・文字列

| 試したこと | 結果 |
|---|---|
| `terrio info 日本地図.tif`（相対パス、実在の GeoTIFF） | **panic**（`zarr.rs:1310`、`t[..5]`） |
| 同上、`地図.tif` `標高.tif` `データ/x.tif` `a地図.tif` | panic |
| 同上、`ab地図.tif` `地.tif` `$PWD/日本地図.tif` | 通る |
| Python `terrio.open_raster('日本地図.tif')` | `PanicException`（`BaseException` 系） |
| panic 時の終了コード | 1（通常のエラーと同じ）。標準エラーに Rust のバックトレースが 41 行ほど出る |
| `t.`、`t.写真` という名前の PNG | panic せず `format not recognized` |
| `画像`（拡張子なし）という名前のファイル | panic（同じ `zarr.rs:1310`） |
| GeoJSON の `"東京都千代田区"` | panic（`geojson.rs:275`。first-contact 参照） |

## 2. Shapefile の文字コード（CP932 / Shift_JIS）

`ABCDEF` を属性に持つ Shapefile を terrio で書き、`.dbf` の中の `ABCDEF` を `札幌市` の CP932 のバイト列（6 バイト）に置き換えて作った。

| 条件 | 読んだ `name` |
|---|---|
| `.cpg` なし | `\x8eD\x96y\x8es`（Latin-1 として解釈。文字化け） |
| `.cpg` が `CP932` / `SHIFT_JIS` / `Shift_JIS` / `932` | 同じ（文字化け） |
| 環境変数 `SHAPE_ENCODING=CP932` | 同じ（無視される） |

エラーも警告も出ない。ソース（`drivers/vector/shapefile.rs` の `decode`）は「UTF-8、そうでなければ Latin-1」だけで、`.cpg` は UTF-8 かどうかの判定にしか使われない。

## 3. 高さと測地系の格子

- `terrio crs` は座標を `x y`（経度 緯度）の組で受ける。高さは**標準入力**から `x y z` で入れる（引数では `coordinates come in x y pairs` と言われる）。
- 既定（ネットワーク OFF）: `EPSG:4979 → EPSG:4326+5773`（EGM96）で高さが変わらない（50 → 50）。
- `TERRIO_NETWORK=ON`: 同じ変換で `50 → 13.5559`。**PROJ の CDN から `us_nga_egm96_15.tif`（約 2.6 MB）を自動取得**し（`~/.cache/terrio/grids`）、適用した。
- 日本のジオイド: PROJ の CDN には `jp_gsi_gsigeo2011.tif`（428,043 バイト）と `jp_gsi_jpgeo2024.tif`（7,379,285 バイト）がある（`jp_` で始まるのはこの 2 つと README だけ）。
  - `TERRIO_NETWORK=ON` で、`EPSG:6697 → EPSG:6668`、`EPSG:6668 → EPSG:6697`、`EPSG:6668 → EPSG:6668+6695`、`+geoidgrids=jp_gsi_gsigeo2011.tif` の PROJ 文字列（両方向）、`jp_gsi_jpgeo2024.tif` を試した。**どれも高さが変わらず**、格子も取得されなかった。
  - 格子そのものは `terrio info` で読める（1201×1800、EPSG:6668、Float32、範囲 東経 119.99〜150.01、北緯 20.01〜50.01）。
- 水平方向（旧日本測地系 EPSG:4301 → 6668、JGD2000 → JGD2011）は、ネットワーク ON でも結果が同じ（4612→6668 は恒等）。PROJ の CDN に日本の水平格子はない。
- ドキュメントの食い違い: `docs/why-terrio.md` は「NTv2 などの格子は**まだ適用しない**」と書き、`docs/crs.md` は「PROJ の格子（GeoTIFF、NTv2、GTX）を探して適用する」と書く。実測では後者が正しい（EGM96 は適用された）。

## 4. PMTiles の書き出しと入出力

- GeoJSON（20×20 = 400 の四角形、`区0`〜`区399`）→ `convert … g.pmtiles --minzoom 4 --maxzoom 10`: 39,554 バイト。`info` は MultiPolygon、400 地物、EPSG:3857。`--oo ZOOM_LEVEL=10` で GeoJSON に戻すと 400 地物、日本語の属性も保たれた。
- `convert … /vsistdout/` は `Is a directory (os error 21)` で失敗。`/dev/stdout` は動く（GeoJSONSeq）。
- `--sql "SELECT n FROM grid WHERE n < 3"` は通る。`ST_Area(geometry)` や `ST_IsValid(geometry)` を含む SQL は `SQL: expected FROM` で失敗（OGR SQL の部分集合。SQLite 方言の空間関数はない）。
- `--skipfailures` はない。

## 5. 棚卸し（hfu と dwg7 の公開リポジトリ）

- `list_repos` で見えた範囲（一覧は途中で切れており、全部ではない）から、公開リポジトリ 75 件を `git clone --depth 1` で取得。`dwg7/kcai-survey-training` など非公開のものは、このリポジトリが公開なので**扱わない**。
- 走査はキーワード（文書への言及も数える）。数は「そのキーワードを含むリポジトリの数」。

| キーワード | リポジトリ数 | キーワード | リポジトリ数 |
|---|---|---|---|
| maplibre | 54 | tippecanoe | 20 |
| pmtiles | 47 | gdal（全般） | 17 |
| martin | 45 | mbtiles | 17 |
| EPSG / PROJ | 31 | JGD2011 / 平面直角 | 16 |
| ogr2ogr | 12 | flatgeobuf | 9 |
| ogrinfo | 5 | rasterio | 4 |
| gdal_translate | 5 | gdalwarp | 3 |
| gdalinfo | 6 | duckdb | 5 |
| terrio | 0 | | |

詳しい分析は `knowledge/hfu-dwg7-workflow-substitution-survey.md`。

## 6. 発見（追加分）

1. **日本語から始まる相対パスで panic する**（`zarr.rs:1310`）。ほぼ全形式に影響
2. **CP932 の Shapefile 属性が黙って文字化けする**（`.cpg` も `SHAPE_ENCODING` も効かない）
3. **日本のジオイド（GSIGEO2011 / JPGEO2024）が適用されない**。EGM96 は適用される
4. ドキュメントの食い違い（格子の適用、`--overview` の意味、main と配布版）
5. `/vsistdout/` は出力先にできない（`/dev/stdout` は可）

## 7. まだ試していないこと

- `terrio mcp`（配布版にない）、WebAssembly 版（terrio-js）
- STACIT、Zarr、FlatGeobuf・COPC のリモート
- `COG` 書き出しの `TILING_SCHEME=GoogleMapsCompatible`（4×4 の入力では判別できなかった）、`warp` の `-dstalpha` 相当（`--help` に見当たらない）
- 出力 GeoJSON の EPSG:3857 を 4326 に直すこと、大きなベクタ PMTiles の書き出し（tippecanoe との比較）

## 8. 上流への報告の状況

- 2026-10-21: hfu が GeoJSON の panic を opengeos/terrio#159 として投稿した（本文は hfu が整えた版）。
- 未投稿の下書き: #159 への CSV のコメント案、日本語パスの panic、CP932 の Shapefile、日本のジオイド（質問）。
