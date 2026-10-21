# 2026-10-21 上流への報告の結果と、最新の main での再確認

- 日付: 2026-10-21（夜。`untested-items` の続き）
- terrio: 配布版 **0.3.2**（PyPI の最新、変わらず）。**main を `6779102281ad2835cbc23fba3138e01a138bc6f9`（2026-10-21 16:39 EDT、#164）でビルド**（`cargo build --release -p terrio-cli`、差分ビルド 3 分 16 秒、`/tmp/terrio-target/`）
- 環境: Claude Code クラウドセッション、Linux x86_64
- きっかけ: hfu から「#159 を投稿した」「もう closed」「Pages の設定をした」との連絡

## 1. #159 の経過（わかる範囲）

| 時刻（UTC） | できごと |
|---|---|
| 14:40 | hfu が GeoJSON の panic の下書きを整える（`5ba52ef`）。この後に #159 を投稿（時刻は不明） |
| 15:23 | 作者のコミット `baf4768`（#161、`Fixes #159`）が main に入る |

- #161 の変更: `geojson.rs`、`csv.rs`、`datetime.rs`、`mapinfo.rs`。バイト列で日付を判定する形に変更。回帰テストは `東京都千代田区` と、日付に似た `2020-01-0千代田区一丁目`
- 配布版: PyPI は 0.3.2 のまま（版は 0.1.1、0.2.0、0.3.1、0.3.2）。タグも v0.3.2 まで。**修正は未リリース**
- このセッションから opengeos/terrio の issue は読めない（GitHub API が 403、`add_repo` の push 権限は拒否された）。issue の本文とコメントは、hfu の連絡と、コミットメッセージからの推測にとどまる

## 2. main（`6779102`）での再確認

| 項目 | 結果 |
|---|---|
| GeoJSON の `東京都千代田区`（`info`） | **直った**（`Features: 1`） |
| CSV の `東京都千代田区`（`info`） | **直った** |
| 日本語の相対パス（`日本地図.tif`、`標高.tif`） | **まだ panic**（`zarr.rs:1310:24`） |
| CP932 の Shapefile（`.cpg` = CP932） | まだ文字化け（`\x8eD\x96y\x8es`） |
| 日本のジオイド（`TERRIO_NETWORK=ON`、`EPSG:6697 → 6668`） | まだ高さ不変（50 → 50） |
| 旧日本測地系 `4301 → 6668` | 変わらず（`139.76389102546048 35.68447487973283`）。#163（変換の選び方）後も同じ |
| JGD2000 `4612 → 6668` | 変わらず（恒等） |
| COG の `TILING_SCHEME=GoogleMapsCompatible` | まだ黙って無視（画素サイズ 12.32 m のまま） |
| `warp --dstalpha` | まだない |
| リモート FlatGeobuf の `--spat` | まだ全量（`(whole file)` の GET） |
| `docs/why-terrio.md` の「NTv2 などの格子は適用しない」 | まだ残っている（`docs/crs.md` と食い違う） |

## 3. 公開ページ

- hfu が GitHub Pages を設定した。`https://dwg7.github.io/kcai-terrio/` は 301 で `https://dwg7.unopengis.org/kcai-terrio/` に転送される（カスタムドメイン）
- 実 Chromium で公開 URL を開き、JGD2011 → 第IX系の変換、COG の窓（6.2 MiB）、FlatGeobuf の bbox（768 KiB）、COPC の `info`（118 KiB）が成功。ページのエラーなし

## 4. 投稿の手段について

- hfu から「原稿の投稿は積極的に進めて」との指示があったが、このセッションの権限では opengeos/terrio への投稿ができない（`add_repo` の push が拒否された。回避はしない）
- そこで、hfu が投稿しやすいよう、`drafts/upstream/README.md` に状態の一覧と、投稿用のリンクを置いた
