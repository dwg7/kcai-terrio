---
id: terrio-roadmap-and-open-items
title: terrio のロードマップ：完了とされたこと、未完了の 21 項目、設計の決定
status: draft
terrio_version: 0.3.2
terrio_commit: 6779102281ad2835cbc23fba3138e01a138bc6f9
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、Node 22、Chromium 1194）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: read-docs
as_of: 2026-10-21
sources:
  - opengeos/terrio の ROADMAP.md（main 6779102。公開サイトの Roadmap ページは同じ内容を取り込む）
related: [terrio-scope-included-and-excluded, terrio-release-vs-main-drift, vertical-datum-grids-and-geoid-in-japan, terrio-js-api-and-playground, terrio-possibilities-and-risks]
freshness: high
---

## 要点

ロードマップ（`ROADMAP.md`）は、**完了 49 項目、未完了 21 項目**（チェックボックスの数）。「1.0: Stable」の項目はすべて完了とされているが、**版は 0.3.2 のまま**で、ドキュメントは「1.0 までは API が変わりうる」と書く。**設計の決定**として「コア API は同期で、データセットをメモリに読む。リモートのファイルは先にダウンロードする。GeoTIFF は例外で、遅延で窓読みする」と明記している（実測の振る舞いと合う）。

## やり方（読み方）

- 原則（冒頭）: 既定は純 Rust（既定の feature は `wasm32-unknown-unknown` でビルドできる、C が要るものは任意の feature）、エコシステムの再利用（`wbraster` `wbvector` `wbprojection` と `tiff`）、形式間で 1 つのデータモデル、クラウドのデータはその場で読む（範囲要求、遅延タイル・チャンク、全量ダウンロードなし）、正しさは GDAL で測る。**非目標**: GDAL の C API やオプション名の一対一の一致、独自 SDK が要る形式（MrSID、ECW、FileGDB ラスタ）、コアでのデータベースドライバー（PostGIS、Oracle、SQL Server）。
- 項目は節に分かれる: 0.1 基礎、0.2 コア形式、0.3 処理、0.4 形式の追加、0.5 結合と GDAL バックエンド、1.0 安定、点群、Python と WebAssembly の結合、後で。

## 確かめたこと（何をして、何が起きたか）

**未完了の 21 項目（read-docs）**

| 領域 | 未完了 |
|---|---|
| Zarr | リモートのグループの一覧（統合メタデータなし）、3 次元超の配列、グループの書き出し（netCDF） |
| STAC | POST のページング、STACTA（タイル付きアセット）、署名付き URL（Planetary Computer） |
| 点群 | PDAL のその他のフィルター（`dbscan` `covariancefeatures` `lof` `dem` `colorization` `overlay` など）、EPT のその場更新 |
| Python / rasterio 互換 | RPC 変換器、`.msk` サイドカー、`rio` コマンドライン |
| Python / xarray | サブデータセット、GCP、RPC |
| Python / GDAL | `terrio-gdal` の GDAL 同梱 wheel、または conda-forge のパッケージ |
| WebAssembly | 自前の FlatGeobuf 読み取り（形式ライブラリの読み取りが 32 ビット WASM で大きなファイルでオーバーフローする）、WASM スレッド、ダウンロードの縮小（形式の分割・オンデマンド）、4 GB 超（memory64） |
| 座標系 | PROJ の複数の中間測地系の連鎖、鉛直 ↔ 鉛直の変換（VERTCON、オフセット）、**エポック間の座標の移動**、**リモートの格子を範囲要求で読む**（いまは全体） |

**この遊びの発見との対応**
- 「リモートの格子を範囲要求で読む」は未完了 → NADCON5 の格子を **全体**（139,914 バイトの 1 要求）で取った実測と合う。
- 「自前の FlatGeobuf 読み取り」は未完了で、WASM の FlatGeobuf は 14 MB で動いたが、**大きなファイルでオーバーフローする可能性**がある（未検証）。
- 「鉛直 ↔ 鉛直」と「複数の中間測地系」が未完了。日本の高さの変換は、3 次元の CRS から変換すれば動く（`vertical-datum-grids-and-geoid-in-japan`。当初の「適用されない」は誤りで訂正した）。ロードマップに日本の格子の項目はない。
- **ロードマップは「完了」を、配布版より先に書く**: 「Windows ARM64 と Pyodide の wheel」は完了（Pyodide の wheel は GitHub のリリースに付く）だが、**PyPI の 0.3.2 に Windows ARM64 の wheel はない**（`terrio-install-platforms-and-release-history`）。「WebAssembly でリモートを範囲読み（COG、PMTiles、COPC、FlatGeobuf は bbox、GeoParquet は行グループ）」は完了で、**`docs/javascript.md` には書かれていない**が、実測で確かめた（`terrio-js-cloud-native-reads-in-browser`）。
- 公開の節: 「crates.io と npm に 0.1.0 と 0.1.1、PyPI に 0.1.1」（0.1.0 は PyPI にない。`terrio-install-platforms-and-release-history` と合う）。

## 気をつけること

- ロードマップは**意図の宣言**。完了印があっても、配布版にあるとは限らない（`terrio-release-vs-main-drift`）。
- 日本の格子・日本語の入力に関する項目はない。上流への提案にするなら、hfu が判断して投稿する（`drafts/upstream/`）。
- 最終更新のコミットは 2026-10-20（`fb53ff6`）。版が上がったら、完了・未完了の移動を確かめる。

## 出典

- https://github.com/opengeos/terrio/blob/main/ROADMAP.md 、https://terrio.opengeos.org/roadmap/
