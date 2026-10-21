# 2026-10-21 未試験項目の消化（STACIT、Zarr、FlatGeobuf、COPC、JP2、処理系、Python、rasterio 互換、WebAssembly、MCP）

- 日付: 2026-10-21（`japan-edge-cases-and-survey` の続き）
- terrio: **0.3.2（PyPI の wheel）**。加えて **main（`cf6bd5dbcb6021f99ffde6c7f2c0f4f3f311ed2b`）を `cargo build --release -p terrio-cli` でビルド**（6 分 33 秒、`/tmp/terrio-target/release/terrio`、リポジトリ外）。main の `--version` も `terrio 0.3.2` と出す
- terrio-js: **0.3.2**（jsDelivr、wasm 20,035,236 バイト）。Node 22.22、Chromium 1194（Playwright）
- 環境: Claude Code クラウドセッション、Linux x86_64、RAM 16 GB、Python 3.13.16
- 転送量の測り方: 途中から（STACIT は測り直した）、terrio 自身のログ（`TERRIO_HTTP_LOG=YES` の要求数と `received N bytes` の合計）に切り替えた（背景のビルドの通信が `/proc/net/dev` に混ざるため）。JS 版は `RemoteDataset.stats()`
- 一時ファイルは `/tmp/work`、`/tmp/survey`、`/tmp/terrio-*`（すべてリポジトリ外）

## 1. リモートの読み込み（CLI 0.3.2）

| 対象 | 操作 | 要求数 | 受信 | 判定 |
|---|---|---|---|---|
| STACIT（Earth Search、東京、`red`） | `info "STACIT:\"URL\""` | 2 | 62 KiB | 目録（地物 3 件）を GeoJSON 層として返す（`Driver: GeoJSON`） |
| 同上 | `info "STACIT:\"URL\":asset=red"` | 5 | 188 KiB | 10980² のモザイク。`Driver: STACIT` |
| 同上 | `convert … --srcwin 5000 5000 512 512` | 11 | **約 17.5 MiB** | 重なる 3 シーン（雲量 0.7 / 64 / 7%）それぞれから約 6 MiB を取る |
| Zarr（NOAA HRRR、S3、`AWS_NO_SIGN_REQUEST=YES`） | `info` | 3 | 888 KiB | 1799×1059、**CRS は unknown**。応答は 200（オブジェクト単位） |
| 同上 | `convert --srcwin 800 500 256 256` | 9 | 978 KiB | 範囲読み込み（チャンク単位） |
| FlatGeobuf（flatgeobuf.org、14.1 MB） | `info` | 2 | 13.8 MiB | **全量** |
| 同上 | `convert --spat -109 37 -102 41` | 1 | 13.8 MiB | **全量**（82 地物） |
| COPC（Autzen、81 MB） | `info` | 2 | 118 KiB | 範囲読み込み |
| 同上 | `convert --bounds 636800 851500 637500 852200` → LAZ | 21 | 6.9 MiB | 304,487 点、出力 2.1 MB |
| 同上 | 上に `--max-level 2` | 5 | 1.6 MiB | 11,880 点、出力 139 KB |
| 同上 | 全域を `--max-level 1` | 3 | 1.7 MiB | 131,060 点 |
| JPEG 2000（Sentinel-2 B04、GCS、26 MB） | `info` | 1 | 16 KiB | 範囲読み込み |
| 同上 | `convert --srcwin 2000 6000 1024 1024` | 36 | 3.3 MiB | 範囲読み込み（ドキュメントの 3.4 MB と合う） |
| 同上 | `convert --overview 3`（687²） | 64 | **約 24.8 MiB** | **ほぼ全体**（COG の overview 2 は 2.6 MiB） |
| GeoParquet（Source Cooperative、日本の建物、**5,056,052,769 バイト**） | `info`（8 秒で打ち切り） | 2 | — | 最初が `bytes=0-65535` の 206、次が **`(whole file)` の 200**。8 秒で **221 MB** を一時ファイルに書いた。**終了後も `/tmp/terrio-XXXX/JPN.parquet` が残った**（手で消した） |

メモ: `terrio grid` は `--tr` が必須（`--resolution` は別のもの）。`terrio convert … --bounds` は 4 つの値（`xmin ymin xmax ymax`）。

## 2. 処理系コマンド（0.3.2、ローカルの小さな実データ）

入力: Sentinel-2 の B04/B08（512²、リモート COG から窓で取得）、SCL（256²）、Autzen の COPC の切り出し（4.4 万点）。

| コマンド | 結果 |
|---|---|
| `calc -A B08.tif -B B04.tif --calc "(A.astype(float)-B)/(A+B)" --type Float32 --NoDataValue -9999` | NDVI。min −0.549、max 0.999、平均 0.344、有効 262,144 |
| 同上で `astype` なし、`--type` なし（`(A-B)/(A+B)`） | 出力は **UInt16、nodata=65535**（NumPy の型規則。符号なしの引き算は桁あふれする型） |
| `polygonize scl.tif` → GPKG | 1,260 ポリゴン |
| `sieve scl.tif --st 20` → `polygonize` | 85 ポリゴン |
| `proximity scl.tif --values 6 --distunits GEO` | 最大 2,276.9（m）。Float |
| `grid pc.laz --tr 5 --stat mean` | 140×140、Float64、nodata −9999、標高 416〜589（ft）。CRS は EPSG:2992 |
| `dem hillshade` / `slope -s 1` / `TRI` / `color-relief ramp.txt` | 1 バンド（1〜255）、傾斜 0.01〜82.9、TRI 1 バンド、色別は 3 バンド Byte |
| `filter smrf pc.laz gr.laz` → `filter hag_nn` | 点数は変わらず、分類・高さの次元が付く（中身の検証はしていない） |
| `rasterize poly.geojson --burn 1 --tr 0.001 0.001 --a-srs EPSG:6668` | 36×26、有効 910 画素。`-a v` で属性 7 を焼ける |
| `mosaic a.tif b.tif m.vrt` / `m.tif` | 512×512（VRT と GeoTIFF の両方） |
| `convert -f COG --compress DEFLATE --tile-size 256` | overview 2 段 |
| `convert -f COG --co TILING_SCHEME=GoogleMapsCompatible` | **エラーなしで無視**（画素サイズ 12.32 m のまま、overview 1 段） |
| `warp --dstalpha` | `unexpected argument '--dstalpha'`（未対応） |
| `rasterize` の入力 GeoJSON に `東京都港区芝公園周辺` | **panic**（GeoJSON の日本語の長い文字列。#159 と同じ） |

## 3. Python（0.3.2）

- `terrio.open_raster(URL, lazy=True)`: 開くのに 0.74 秒。`read(1, window=(5000,5000,256,256))` が 1.0 秒。`read(1, window=(0,0,687,687), overview=3)` も可。要求は合計 5 回、約 6.8 MiB（窓 6.3 MiB + 小さな overview）
- `terrio.rio`（rasterio 互換）は `import terrio.rio` が必要（`import terrio` では出ない）。**dwg7/snow-hokkaido が使う呼び出しの再現 12 件が全部通った**: 2 バンド書き込み（`compress`、`blocksize`、`tiled`）と `set_band_description`・`update_tags`、読み戻し（`tags()` `descriptions` `crs` `shape`）、`driver='COG'` の書き込み、`read(boundless=True, fill_value=0)`、`from_bounds` + `out_shape` + `Resampling` + `window_transform` + `windows.bounds`、`rasterio.Env(...)` 越しのリモート COG 窓読み、`rasterize(all_touched=False)`、`sample`、`'r+'` での `update_tags`、`warp.transform_bounds`、`warp.calculate_default_transform`
- 気づき: `Window` の値が `np.float64`（rasterio は Python の float）。`COG` で書いたファイルの `info` は `Driver: GTiff`（GDAL と同じ扱い）

## 4. WebAssembly（terrio-js 0.3.2、Node と実 Chromium）

- **`openUrl` が、COG、PMTiles、COPC、FlatGeobuf、GeoParquet を範囲読み**する（CLI と違い、FlatGeobuf と GeoParquet も）。0.3.2 の `docs/javascript.md` には出ていないが、型定義（`terrio.d.ts`）にある。

| 対象 | 操作 | 要求 | 受信 |
|---|---|---|---|
| Sentinel-2 COG | `info` / 256² 窓 | 1 / 3 | 64 KiB / 6.2 MiB |
| PMTiles ラスタ 30.5 GB | `info` | 12 | 832 KiB |
| PMTiles ベクタ（depot、2.2 MB） | `info` | 1 | 64 KiB |
| FlatGeobuf 14 MB | `info` | 1 | 64 KiB |
| 同上 | `read({bbox: コロラド})`（82 地物） | 4 | **768 KiB**（CLI は 13.8 MiB） |
| COPC 81 MB | `info` | 2 | 118 KiB |
| GeoParquet **5 GB** | `info` | 3 | 14.5 MiB（フッターが大きい） |
| 同上 | `read({bbox: 東京駅の約 1 km 四方})`（119 棟） | 7 | **16.4 MiB**、約 10 秒 |

- **実 Chromium（Playwright）**: `docs/index.html`（terrio-js を jsDelivr から固定版で読み込む）で、上の 6 種がすべて成功した（CORS に問題なし）。ブラウザでも要求数と受信量は Node と同じ（COG 窓 6.2 MiB、PMTiles 832 KiB、FlatGeobuf 768 KiB、COPC 118 KiB、GeoParquet 16.4 MiB）
- `transformPoints([139.767125],[35.681236],"EPSG:6668","EPSG:6677")` → `-5992.9196, -35363.2377`（CLI と同じ）
- **日本語の長い文字列の panic は WebAssembly でも再現**: GeoJSON `東京都千代田区` と CSV で `RuntimeError: unreachable`（コンソールに `panicked at crates/terrio/src/drivers/vector/geojson.rs:275:22` / `csv.rs:587:22`）。`札幌市北区` は通る。**トラップ後も、同じモジュールで他の呼び出しは動いた**
- CDN の取得物: `terrio_bg.wasm` は 20 MB（ドキュメントの「初回は約 4 MB」は転送時の圧縮後の値と思われる。未確認）

## 5. MCP（main のビルド、`terrio mcp`）

標準入出力の JSON-RPC を直接話した（`initialize` → `tools/list` → `tools/call`）。

- `serverInfo`: `terrio` / 版 `0.3.2`、`protocolVersion 2025-03-26`
- ツール 15 個（`info` `convert` `formats` `crs` `rasterize` `polygonize` `translate` `warp` `mosaic` `dem` `calc` `proximity` `sieve` `grid` `filter`）。引数は `{"args": ["…"]}`（コマンドライン引数の文字列配列）。**ツールの説明は各コマンドの `--help` 全文**
- `info`（ローカル）と `crs`（`-5992.919570392903 -35363.23774493004`）は成功。存在しないファイルは `isError: true` とメッセージ
- **日本語の相対パスで panic した場合も、`isError: true` で返り、サーバーは落ちない**（各呼び出しが別プロセスのため）。絶対パスは通る
- Claude Code への登録（`claude mcp add terrio -- terrio mcp`）は、このセッションのツールを増やすので**試していない**

## 6. main（cf6bd5d）での再確認

| 項目 | main の結果 |
|---|---|
| `terrio mcp` | ある（0.3.2 の wheel にはない） |
| GeoJSON / CSV の日本語 panic | **直っていない**（`geojson.rs:275`、`csv.rs:587`） |
| 日本語の相対パス | **直っていない**（`zarr.rs:1310`） |
| CP932 の Shapefile | **直っていない**（`.cpg` あり・なしとも文字化け） |
| 日本のジオイド（`TERRIO_NETWORK=ON`） | **変わらない**（高さ不変） |
| `warp --dstalpha` | ない |
| リモート FlatGeobuf の `--spat` | 全量（13.8 MiB、要求 1 回） |

## 7. 発見（このセッションの追加分）

1. **WebAssembly 版は FlatGeobuf と GeoParquet を範囲読みするが、CLI / Python は全量取得する**（入口によって「クラウドネイティブ度」が違う）
2. **`terrio` は中断されると、ダウンロード中の一時ファイルを残す**（8 秒で 221 MB）
3. COPC は CLI でも範囲読みが効き、`--bounds` / `--max-level` で転送量を落とせる
4. JPEG 2000 は窓なら範囲読みだが、overview は全体を読む
5. COG の `TILING_SCHEME` は黙って無視される。`warp --dstalpha` はない
6. `terrio.rio` は、実際の利用コードの呼び出し 12 件がすべて通った
7. `terrio mcp` は main にあり、プロトコルどおり動く。配布版にはない
8. 日本語の panic は、main でも、WebAssembly でも、MCP 経由でも同じ

## 8. Hugging Face の GeoParquet と、一時ファイルの場所

- 対象: `huggingface.co/datasets/severo/geoparquet/resolve/main/nz-building-outlines.parquet`（430,146,888 バイト）。URL は **302 で署名付きの CDN（`us.aws.cdn.hf.co`、xet）へ転送**され、転送先は `accept-ranges: bytes`、`access-control-allow-origin: *`
- CLI 0.3.2: リダイレクトを追って（4 秒で打ち切り）ダウンロードを始めた。**`TMPDIR=/tmp/work/tmpx` を指定すると、一時ディレクトリ `terrio-XXXXXX` がそこにできた**（`TMPDIR` は効く。ソースは `tempfile::Builder` で `vfs.rs:311`）。打ち切り後に残ったので手で消した
- terrio-js `openUrl`: `info` は 2 要求・約 97 KiB で、**行グループが 1 つ（330 万行、430 MB、bbox の統計なし）**。`read({bbox:[174.76,-36.86,174.78,-36.84]})` は 0 件で、**約 394 MiB（ファイルのほぼ全体）を読んだ**（3 要求、約 10.7 秒）。行グループが 1 つで統計がないと、範囲読みの利点がない。0 件の理由は未確認（bbox の座標系が違う可能性。`info` に CRS が出ない）
- Source Cooperative の日本の建物（5 GB）は、行グループが約 5,000 行ずつ（フッター約 15 MB）で、bbox 読みが効いた。**範囲読みの効き方は、ファイルの行グループの作りで決まる**

## 9. まだ試していないこと

- Source Cooperative の COG
- main の CLI で `mcp` を Claude Code に登録しての実使用
- STACIT の `--outsize` などでの縮小、Zarr の `CRS unknown` の原因
- 大きなベクタ PMTiles の書き出し（tippecanoe との比較）
