---
id: cloud-native-read-behavior-matrix
title: クラウドネイティブな形式の読み込み方：どこまで範囲読み込みか（一覧）
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、PyPI の wheel）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-24
interface: cli
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - plays/2026-10-21-first-contact.md（転送量の測定、3.1〜3.3）
  - plays/2026-10-21-untested-items.md（STACIT、Zarr、JP2、COPC、FlatGeobuf、GeoParquet 5 GB、WebAssembly）
  - terrio docs/remote-data.md、docs/gdal.md（v0.3.2 と main）
related: [cog-remote-window-overview-and-warp, pmtiles-remote-reading, terrio-scope-included-and-excluded, terrio-release-vs-main-drift, terrio-js-cloud-native-reads-in-browser]
freshness: high
finding:
  - geoparquet-remote-info-downloads-whole-file
  - translate-outsize-downloads-whole-cog
  - server-ignoring-range-makes-terrio-read-whole-file
  - wasm-reads-flatgeobuf-and-geoparquet-by-range-cli-does-not
  - interrupted-download-leaves-temp-file
---

## 要点

リモートの URL に対する terrio の読み方は、形式と操作で大きく違う。**「クラウドネイティブな形式だから範囲読み込み」とは限らない。** 転送量は、`/proc/net/dev` の受信バイトの差（TLS とプロキシの上乗せを含む概数）か、terrio 自身のログ（`TERRIO_HTTP_LOG=YES` の `received N bytes` の合計）、JS 版は `stats()` で測った。

| 形式 | 操作 | 実測の転送量（ファイル全体） | 判定 | 確かめ方 |
|---|---|---|---|---|
| COG（Sentinel-2 B04、10980², 216 MB） | `info` | 約 78 KiB | **範囲読み込み**（ヘッダーだけ） | played |
| 同上 | `convert --srcwin`（256² / 1024²） | 約 6.4 MiB | **範囲読み込み**（タイル単位。窓の大きさによらず、またぐタイル数で決まる） | played |
| 同上 | `warp`（10 km 四方を EPSG:6677 へ） | 約 6.1 MiB | **範囲読み込み** | played |
| 同上 | `convert --overview 2` | 約 2.6 MiB | **範囲読み込み**（overview 層） | played |
| 同上 | `translate --outsize 512 512`（縮小） | **約 208 MiB** | **ほぼ全量**（overview を使わない。ドキュメントに明記） | played + read-docs |
| PMTiles ラスタ（30.5 GB） | `info` | 約 0.84 MiB | **範囲読み込み**（ヘッダー、ルートディレクトリ、メタデータ） | played |
| 同上 | `convert --srcwin`（512²） | 約 1.3 MiB | **範囲読み込み** | played |
| PMTiles ベクタ（2.2 MB） | `info` | 約 1.5 MiB | ほぼ全体（小さいファイルなので判別できない） | played |
| 同上 | `convert --spat` + `ZOOM_LEVEL=8` | 約 278 KiB | **範囲読み込み**（空間フィルター付き） | played |
| PMTiles（275 GB）、Range を無視する配信 | `info` | **120 秒で 1.2 GiB、未完了** | 配信が 200 で全体を返し、terrio は読み続ける | played |
| GeoParquet（Overture places、681 MB） | `info` | **約 656 MiB** | **全量ダウンロード**（一時ファイルへ。ドキュメントに記載。正常終了時は削除される） | played |
| STACIT（検索結果のモザイク、東京、3 シーン） | `info "STACIT:\"URL\":asset=red"` | 約 188 KiB | **範囲読み込み**（目録とヘッダーだけ） | played |
| 同上 | `convert --srcwin`（512²） | **約 17.5 MiB** | 範囲読み込みだが、**重なる全シーン（3 つ）から読む**（雲の多い日付も） | played |
| Zarr（NOAA HRRR、S3） | `info` / 窓 256² | 888 KiB / 978 KiB | **範囲読み込み**（メタデータとチャンク。オブジェクト単位の GET） | played |
| JPEG 2000（Sentinel-2、26 MB） | `info` / 窓 1024² | 16 KiB / 3.3 MiB | **範囲読み込み** | played |
| 同上 | `convert --overview 3`（687²） | **約 24.8 MiB** | **ほぼ全体**（overview でも全タイルのヘッダーをたどる） | played |
| COPC（Autzen、81 MB） | `info` | 118 KiB | **範囲読み込み** | played |
| 同上 | `convert --bounds`（700 ft 四方）/ 同＋`--max-level 2` | 6.9 MiB / 1.6 MiB | **範囲読み込み**（八分木のノード単位。レベルで転送量を落とせる） | played |
| FlatGeobuf（14.1 MB） | `info` / `convert --spat` | 13.8 MiB（どちらも） | **全量**（空間インデックスは使われない） | played |
| GeoParquet（Source Cooperative、日本の建物 **5.06 GB**） | `info`（8 秒で打ち切り） | 8 秒で 221 MB を一時ファイルへ | **全量ダウンロード**（最初に Range 0-65535、すぐ全体の GET）。**中断すると一時ファイルが残る** | played |
| GeoParquet（Hugging Face、430 MB、302 で CDN へ） | `info`（4 秒で打ち切り） | 4 秒で一時ファイルを書き始めた | **全量ダウンロード**（リダイレクトは追う。一時ファイルは `TMPDIR` の下にできる） | played |
| Shapefile / GeoJSON（リモート） | — | — | **未試験**（ドキュメントは「一時ディレクトリへ先に取得」） | read-docs |

## 入口によって違う：WebAssembly 版は、より範囲読みする

同じ URL を、WebAssembly 版（terrio-js の `openUrl`）で開くと、CLI / Python と結果が変わる（実 Chromium と Node で測定）。

| 対象 | CLI / Python（0.3.2） | WebAssembly（terrio-js 0.3.2） |
|---|---|---|
| FlatGeobuf 14 MB、bbox（82 地物） | 全量 13.8 MiB | **768 KiB**（要求 4 回。空間インデックスを使う） |
| GeoParquet 5 GB、bbox（東京駅の約 1 km 四方、119 棟） | 全量ダウンロード（打ち切りまでに 221 MB） | **16.4 MiB**、要求 7 回、約 10 秒（行グループの統計で飛ばす） |
| GeoParquet 5 GB の `info` | 全量 | 14.5 MiB（フッターが大きい） |
| COG の窓 256² | 6.3 MiB | 6.2 MiB（同じ） |
| PMTiles 30 GB の `info` | 0.84 MiB | 832 KiB（同じ） |
| COPC の `info` | 118 KiB | 118 KiB（同じ） |

- WebAssembly 版の範囲読みは、**ファイルの作りに左右される**: Hugging Face の GeoParquet（430 MB）は行グループが 1 つで統計がなく、bbox 読みでも約 394 MiB（ほぼ全体）を読んだ。Source Cooperative の日本の建物（約 5,000 行ずつの行グループ）は 16 MiB で済んだ。
- ブラウザでは、相手が `Range` を許可しているだけで通った（試した 6 つの配信先すべて）。詳細は `terrio-js-cloud-native-reads-in-browser`。
- 「FlatGeobuf / GeoParquet のクラウド読み」が必要なら、今は **JS 版のほうが進んでいる**。CLI に入るかは不明（main の CLI も、FlatGeobuf は全量だった）。

## やり方

1. 先に `curl -sI URL` で `Accept-Ranges` と `Content-Length` を見る。
2. `TERRIO_HTTP_LOG=YES` で要求を見る（`GET ... (bytes=0-65535) -> 206` のように出る）。
3. 大きなファイルには `timeout 60 terrio ...` を付け、`TERRIO_HTTP_TIMEOUT` も設定する。
4. 転送量は `/proc/net/dev` の受信バイトの差などで測る。

## 確かめたこと（何をして、何が起きたか）

上の表のとおり。測定の手順とコマンドは `plays/2026-10-21-first-contact.md`。

- 要求ブロックは既定 64 KiB（`TERRIO_HTTP_BLOCK_SIZE`）。キャッシュは 64 MiB。隣り合う範囲は 1 回の要求にまとめる（ドキュメント）。
- COG の窓読みは、窓の大きさよりタイルの大きさに支配される。この COG のタイルは約 1.6 MiB（圧縮後）で、窓がタイル境界をまたいだため 4 タイル（約 6.4 MiB）を取った。

## 気をつけること

- **縮小の読み方**: `translate --outsize` と `warp` の縮小は、全解像度を読む（`docs/gdal.md`）。リモートでは `convert --overview N`（N は 0 始まりで、0 は最初の縮小版）を使う。
- **GeoParquet の `info` でも全量を取る**。巨大な Parquet のリモートに `info` を打たない（ディスクとメモリの割り当てに注意）。**中断すると、一時ファイル（`/tmp/terrio-XXXX/`）が残る**（5 GB のファイルで 8 秒後に 221 MB が残った）。
- **配信側が Range を無視すると、全体を読み続ける**。terrio は 200 を受けても止めない。必ず `timeout` を付ける。
- 表は 2026-10-21 の 1 回の測定。配信側（キャッシュの有無）でも変わる。版が上がったら、また測る。

## 0.4.2 での再確認（2026-10-24）

0.4.2 の wheel で再確認できた行だけ: **COG の窓・概観は範囲読み込み**（B04: 6.19 / 2.56 MiB）。**PMTiles（`depot.optgeo.org/ksj_n03_hkd.pmtiles`）は範囲読み込み**（`info` が 12 要求・1.48 MiB、3,625 地物）。**FlatGeobuf（`flatgeobuf.org/test/data/UScounties.fgb`）は CLI で全量取得のまま**（`(whole file)` 14,100,008 バイト、`--spat` で 3 地物）。ドキュメントの `remote-data.md` も「その他の形式は一時ファイルに取得」のまま。**他の行（GeoParquet、COPC、JP2、Zarr、STAC、JS 版）は 0.4.2 では確かめ直していない**（表は 0.3.2 の値）。main は Zarr の遠隔グループの一覧（#199）、CDN の格子の範囲読み込み（#202）、STAC の POST と Planetary Computer（#197）を足している。

## 出典

- plays/2026-10-21-first-contact.md
- https://terrio.opengeos.org/ （remote-data、gdal）
