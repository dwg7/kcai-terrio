---
id: japanese-path-panic-in-zarr-parse-name
title: 日本語から始まる相対パスで terrio が panic する（Zarr 名の判定）
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、PyPI の wheel）
verified_on: 2026-10-21
verified_how: played
sources:
  - plays/2026-10-21-first-contact.md
  - crates/terrio/src/drivers/zarr.rs の parse_name（v0.3.2 の 1310 行付近）
  - drafts/upstream/2026-10-21-zarr-parse-name-panic-on-multibyte-path.md
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
related: [upstream-issue-feedback-loop, geojson-japanese-string-panic, terrio-source-quirks]
hazard: multibyte-path-slicing-panic
finding:
  - utf8-boundary-panic-in-zarr-parse-name
---

## 要点

**2026-10-21 更新: 最新の main（`6779102`）でも、まだ panic する（`zarr.rs:1310`）。** 同じ型の GeoJSON / CSV の panic は、#161 で直った（`upstream-issue-feedback-loop`）。この塊の下書きは、hfu の投稿を待っている。

**日本語のファイル名を相対パスで渡すと、terrio が panic する場合がある。** どの形式でも起こる（パスを最初に Zarr 名として調べるため）。5 バイト目が日本語の文字の途中に当たるとき: `日本地図.tif`、`標高.tif`、`データ/x.tif`。絶対パス（`/tmp/…/日本地図.tif`）は通る。日本で最も自然な使い方（日本語名のファイルを相対パスで）に当たるので、日本ローカルでは影響が大きい。

## やり方（再現）

```sh
terrio convert some.png ascii.tif
cp ascii.tif 日本地図.tif
terrio info 日本地図.tif          # panic
terrio info "$PWD/日本地図.tif"   # 通る
```

## 確かめたこと（何をして、何が起きたか）

| パス | 結果 |
|---|---|
| `ascii.tif`、`ab地図.tif`、`地.tif` | 通る |
| `日本地図.tif`、`地図.tif`、`標高.tif`、`データ/x.tif`、`a地図.tif` | **panic** |
| `$PWD/日本地図.tif`（絶対パス） | 通る |

- メッセージ: `end byte index 5 is not a char boundary; it is inside '本' (bytes 3..6 of string)`（`zarr.rs:1310:24`）。
- Python の `terrio.open_raster('日本地図.tif')` も `PanicException`（`BaseException` 系）。
- ソース: `parse_name` が `t.len() > 5 && t[..5].eq_ignore_ascii_case("ZARR:")` で文字列をバイト 5 で切る。規則は「バイト 5 が文字の途中にある」。3 バイト文字だけの名前は、ほぼ必ず該当する。
- `convert` の出力側のパスや、`mosaic` の入力など、他の入口は**未確認**。
- `png.rs` の `read_world_file`（`&ext[..1]`）にも似たコードがあるが、再現できなかった（未知の拡張子は先に拒否される）。

## 気をつけること

- **回避策**: 絶対パスで渡す（`"$PWD/日本地図.tif"`）、ファイル名を ASCII にする、先頭に ASCII を足して 5 バイト目を文字の境界にする（`ab地図.tif` は通る）。
- Python では `except Exception` が効かない。`BaseException` まで捕まえるか、パスを事前に ASCII 化する。
- 下書き（`drafts/upstream/`）は hfu が確認して投稿する。新しい版で直ったら、この塊を再確認して `stale` を外す。

## 出典

- plays/2026-10-21-first-contact.md
- https://github.com/opengeos/terrio （v0.3.2、crates/terrio/src/drivers/zarr.rs）
- drafts/upstream/2026-10-21-zarr-parse-name-panic-on-multibyte-path.md
