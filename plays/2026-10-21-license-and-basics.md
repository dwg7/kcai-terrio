# 2026-10-21 ライセンスなどの基礎的事項の確認と、ドキュメント全 25 ページの消化

- 日付: 2026-10-21（夜。`upstream-feedback-loop` の続き）
- terrio: 配布版 **0.3.2**（PyPI の wheel）。ソースとドキュメントは main `6779102281ad2835cbc23fba3138e01a138bc6f9`（2026-10-21 16:39 EDT、#164）。main は `/tmp/terrio-target/release/terrio` にビルド済み（差分ビルド 3 分 16 秒）。terrio-js は 0.3.2
- 環境: Claude Code クラウドセッション、Linux x86_64、4 コア、RAM 15 GB。Python 3.13.16（pyarrow 26.0、GeoPandas 1.2、Polars 2.0、xarray、dask、zarr は `/tmp/pyenv` の別の仮想環境）、Node 22.22、Chromium 1194（Playwright）
- 転送量は terrio 自身のログ（`TERRIO_HTTP_LOG=YES`）か JS の `stats()`。一時ファイルは `/tmp/work`（リポジトリ外）

## 1. ライセンスと基礎的事項

| 確認 | 方法 | 結果 |
|---|---|---|
| 本体の宣言 | リポジトリの `LICENSE`、`Cargo.toml`、`python/pyproject.toml`、PyPI の METADATA、npm の `package.json`、crates.io の全版 | すべて **MIT**（Copyright (c) 2026 Qiusheng Wu） |
| 0.3.2 の wheel の LICENSE | 入れて `dist-info` を `ls` | **`licenses/` なし**。`sboms/terrio-py.cyclonedx.json` はある |
| 0.3.2 の sdist | PyPI から取得、`tar tzf`（259 ファイル） | **LICENSE なし**（README だけ） |
| 0.3.2 の crate | crates.io の `download`、`tar tzf` | **LICENSE なし**（`Cargo.toml` の `license = "MIT"`） |
| 0.3.2 の npm | jsDelivr | **LICENSE あり**（`package.json` の `files` にない） |
| main の #164 | `git show`、`NOTICE`、`LICENSE-THIRD-PARTY.md` | PROJ（MIT 系）、CSF（Apache-2.0）、EPSG（IOGP の条件）、Esri（Apache-2.0）、rasterio（BSD-3）、rioxarray（Apache-2.0）、Arrow、IJG の告知を追加。配布物に同梱予定（未リリース） |
| 依存 | wheel の SBOM（CycloneDX 1.5）を集計 | **282 コンポーネント**（255 種）。`MIT OR Apache-2.0` 156、MIT 45、Apache-2.0 14 など。GPL/LGPL/AGPL だけのものはなし。注意: `self_cell`（`Apache-2.0 OR GPL-2.0-only`）、`smartstring`（`MPL-2.0+`）、WTFPL ×4、`webpki-roots`（`CDLA-Permissive-2.0`） |
| README の開示 | PyPI 0.3.2 の METADATA を検索 | "Disclaimer" と "Claude Opus" が **0 件**（開示は #142、0.3.2 の後） |
| 版の履歴 | PyPI / npm / crates.io の API | PyPI: 0.1.1（10-15）、0.2.0（10-15）、0.3.1（10-17）、0.3.2（10-20）。**PyPI に 0.3.0 はない**。**0.3.2 の wheel は 8 つ（Windows ARM64 なし）** |
| データのライセンス | STAC のコレクション、Source Cooperative の製品ページ、Overture の帰属ページ、stars の `/catalog`、HF のカード | `data-licenses-of-play-datasets` |

## 2. ドキュメント全 25 ページの消化

- 読んだページ: Home、Why terrio?、Installation、Getting Started、Playground、Notebooks、Command Line、AI Agents (MCP)、Formats、Point Clouds、Remote Data、Coordinate Systems、Coming from GDAL、Coming from rasterio、Rust Library、Python、xarray、JavaScript、Testing Against GDAL、Conformance、Benchmarks、Architecture、Contributing、Acknowledgements、Roadmap（と `ROADMAP.md` 全体）
- **公開サイトとの一致**: 各ページの `<article>` の語と md の語を比較。サイトの語が md にある割合は 0.94〜1.00（Python と JavaScript が 0.94 で、差は記法）。main にだけある語（`ESRI:54009`、`cargo-about`、`Claude Opus`、`default-features`、`ARM64`）がサイトにあり、**サイトは main に追随**
- 対応表と、記述の食い違い 14 件: `knowledge/terrio-docs-coverage-map.md`

## 3. ドキュメントの例を動かした結果（0.3.2）

| 例 | 結果 |
|---|---|
| Getting Started: `info` の zip、`convert` で GPKG / FlatGeobuf / Parquet、`rasterize`、`polygonize`、`crs` | 通る。`europe.parquet` は 39 地物 |
| 同: **`convert countries.gpkg countries_3857.geojson --t-srs EPSG:3857`** | **失敗**: `failed to reproject feature 159 … cannot transform (180, -90)`（Antarctica）。0.3.2 と main で同じ。`--where "NAME <> 'Antarctica'"` で通る。PMTiles の書き出し（既定）も同じ原因で失敗 |
| USGS の標高 COG（51,486,544 バイト）: `translate --srcwin 1000 1000 512 512 --ot Int16` | 3 要求・3.2 MiB。**出力は Int16 なのに nodata=-999999（範囲外）** |
| 同: `warp`（UTM 13N、30 m、411×529）、`mosaic`（.vrt と .tif） | 通る |
| CLI: `polygonize` の既定の属性 | `DN`（文書どおり） |
| CLI: `calc` の型 | Byte の `A*60` は桁あふれ（4,5,6 → 240,44,104）。**`A/5` は `--type` なしで Byte（値 1）**、`--type Float32` で 0.8〜1.2 |
| CLI: `warp -r` の一覧、`formats --json`、`info --json` のキー | 文書と一致（49 行） |
| Formats の表と `terrio formats --json` の機械的な突き合わせ | 表の 46 行はすべてバイナリにあり、バイナリにだけ点群の E57、EPT、PLY。HFA の書き込みは文書の `✓*`（`gdal` feature）と整合 |
| GeoParquet の書き出し | `version 1.1.0`、`covering.bbox`、`geometry_bbox` 列を確認 |
| PMTiles のベクタの既定のズーム | 0〜5（`ZOOM_LEVEL=6` は `invalid zoom level 6: the archive has zoom levels 0 to 5`） |
| `--append` / `--overwrite`（GeoPackage） | 177 → 354 → 177 |
| STACIT: 窓（512²、東京、3 シーン）、`max_items=1` | 全シーン 17.5 MiB（11 要求）、**`max_items=1` で 6.2 MiB（4 要求）**、結果の平均は同じ（804）。オプションは `asset=red,max_items=1` のカンマ区切り |
| 点群（Autzen の COPC）: 文書の 2 つの例 | `info` 2 要求・118 KiB（文書 120 kB）、`--bounds … --resolution 7.27` が **8 要求・3,574 KiB・18,901 点**（文書 8 要求・3.7 MB・18,901 点） |
| 点群のフィルター 9 種、PLY / E57 / EPT / COPC の往復 | 44,465 点の切り出しで通る（`outlier --remove` 43,287、`voxeldownsize` 7,395、`expression` 19,030、`crop` 10,723、`merge` 26,425 など）。次元名は `cluster_id`、`normal_z` |
| 座標系: 書式 | 数字だけ、URN、URL、`OGC:CRS84`、`WGS84`、複合、PROJ 文字列が通る。`+proj=airy`、`+proj=igh` は拒否。**`ESRI:54009` は 0.3.2 で `cannot parse`、main で通る** |
| 座標系: NADCON5（`TERRIO_NETWORK=ON`） | 格子を全体（139,914 バイト）で取得。結果の差は約 1 m |
| 座標系: エポック | `echo "135 -25 0" \| terrio crs EPSG:7912 --to EPSG:7843 --s_coord_epoch 2010.0` → `135.0000030617912 -24.99999469886912 -0.0015…`（約 0.3 m）。引数で `x y z` は不可（標準入力） |
| `terrio.rio`: マスク、窓、エラー型、CRS | `read(1)` は ndarray、`masked=True` で MaskedArray。`RasterioIOError`、`CRSError`、`IndexError`。端数のある窓が読める |
| Python API のドキュメントの例 30 件 | **29 件が通る**。失敗は `to_crs("EPSG:3857")`（南極）。エラーの型の階層は文書どおり |
| Arrow（別の仮想環境） | pyarrow、GeoPandas（`from_arrow`、CRS 4326）、Polars（177×169）、GeoArrow ネイティブ（`geoarrow.multipolygon`）、`from_arrow`、`write_vector(pa_table)` が通る |
| xarray（`terrio[xarray]` + zarr） | リモート COG を遅延で開き、`clip_box`、`reproject`、`to_raster`（COG と GeoZarr）、`to_zarr`、`engine="terrio"`、`register_rio_accessor`、`merge_arrays` が通る。ここまで **4 要求・約 3.2 MiB** |
| terrio-js（Node）の API | 主要な操作が動く。`dem(b, {mode:…})`（誤った呼び方）は **WASM のトラップ**（`memory access out of bounds`）。EGM96 は `registerGrid` で適用、**日本のジオイドは `registerGrid` でも不変** |
| 公式プレイグラウンド（実 Chromium） | 0.3.2 固定。サンプルと座標変換は動く。**日本語の長い文字列の GeoJSON で `unreachable`** |

## 4. 発見（この回）

1. 0.3.2 の **wheel、sdist、crate に LICENSE ファイルがない**（npm にはある）。main の #164 で追加予定
2. wheel の SBOM は 282 コンポーネント。GPL 単独なし。`ring`、`zstd-sys` があり、「C の依存は Zstandard だけ」のドキュメントの記述と合わない可能性
3. **ドキュメントの食い違いと配布版との差 14 件**（`terrio-docs-coverage-map`）
4. **入門ページの EPSG:3857 の例が失敗する**（南極）。PMTiles の既定の書き出しも失敗
5. `translate --ot Int16` で nodata が範囲外のまま。`calc` の `/` が整数に丸まる
6. STACIT の窓は重なる全シーンから読む（`max_items` で絞れる）
7. 日本のジオイドは、JS で格子を直接登録しても不変（変換の選択側の可能性）。conformance の格子の一覧（128 行）に日本の格子（`jp_`）がない
8. 公式プレイグラウンドで日本語の長い文字列が落ちる（#161 の修正は 0.3.2 固定のため未反映）
9. ロードマップ（main）の完了印は、配布版より先行する。JS の範囲読みは、ロードマップと型定義だけにある

## 5. まだ試していないこと

- Notebooks（Colab）の実行、ベンチマークの再現（GDAL がない）、Rust のコードを書いての実行
- DuckDB と GDAL の Arrow ストリーム、`terrio-gdal`（GDAL バックエンド）、Pyodide の wheel
- インストーラ（`curl | sh`）、Windows と macOS
- LERC・LZMA・JPEG XL・JPEG の YCbCr の GeoTIFF、netCDF/HDF5 の実ファイル
