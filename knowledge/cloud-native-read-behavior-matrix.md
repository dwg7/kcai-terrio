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
updated: 2026-10-21
interface: cli
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - plays/2026-10-21-first-contact.md（転送量の測定、3.1〜3.3）
  - terrio docs/remote-data.md、docs/gdal.md（v0.3.2 と main）
related: [cog-remote-window-overview-and-warp, pmtiles-remote-reading, terrio-scope-included-and-excluded, terrio-release-vs-main-drift]
freshness: high
finding:
  - geoparquet-remote-info-downloads-whole-file
  - translate-outsize-downloads-whole-cog
  - server-ignoring-range-makes-terrio-read-whole-file
---

## 要点

リモートの URL に対する terrio の読み方は、形式と操作で大きく違う。**「クラウドネイティブな形式だから範囲読み込み」とは限らない。** 転送量は、`/proc/net/dev` の受信バイトの差で測った概数（TLS とプロキシの上乗せを含む）。

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
| GeoParquet（Overture places、681 MB） | `info` | **約 656 MiB** | **全量ダウンロード**（一時ファイルへ。ドキュメントに記載） | played |
| STAC API の検索 | `curl` による POST 検索 | 小さい | terrio では**未試験** | — |
| STACIT / STAC アイテムの COG 資産 | — | — | **未試験**（ドキュメントは「COG のヘッダー、窓は必要なタイルだけ」） | read-docs |
| Zarr（v2 / v3、リモート） | — | — | **未試験**（ドキュメントは「メタデータ 1 回、窓はチャンクだけ」） | read-docs |
| JPEG 2000 | — | — | **未試験**（ドキュメントは「窓と解像度レベルで範囲読み込み」） | read-docs |
| FlatGeobuf / COPC / Shapefile / GeoJSON（リモート） | — | — | **未試験**（ドキュメントは「その他の形式は一時ディレクトリへ先に取得」。COPC はロードマップに「少しずつ」とある） | read-docs |

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
- **GeoParquet の `info` でも全量を取る**。巨大な Parquet のリモートに `info` を打たない（ディスクとメモリの割り当てに注意）。
- **配信側が Range を無視すると、全体を読み続ける**。terrio は 200 を受けても止めない。必ず `timeout` を付ける。
- 表は 2026-10-21 の 1 回の測定。配信側（キャッシュの有無）でも変わる。版が上がったら、また測る。

## 出典

- plays/2026-10-21-first-contact.md
- https://terrio.opengeos.org/ （remote-data、gdal）
