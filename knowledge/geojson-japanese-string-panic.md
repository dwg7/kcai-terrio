---
id: geojson-japanese-string-panic
title: 日本語の長い文字列を含む GeoJSON と CSV で terrio が panic する（0.3.2）
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
sources:
  - plays/2026-10-21-first-contact.md（3.5、4）
  - crates/terrio/src/drivers/vector/geojson.rs（v0.3.2 の 270〜277 行付近）
  - drafts/upstream/2026-10-21-geojson-panic-on-multibyte-strings.md
upstream_issue: opengeos/terrio#159
upstream_fix: baf4768
related: [upstream-issue-feedback-loop, pmtiles-remote-reading, japanese-path-panic-in-zarr-parse-name, terrio-source-quirks]
hazard: multibyte-string-slicing-panic
finding:
  - utf8-boundary-panic-in-is-datetime
---

## 要点

**2026-10-21 更新: GeoJSON と CSV の panic は、作者が main で修正した（opengeos/terrio#159、コミット `baf4768`、#161）。配布版（PyPI の 0.3.2）には未リリース。** 最新の main（`6779102`）で、`東京都千代田区` の GeoJSON と CSV が通ることを確かめた。以下は 0.3.2 での記述。経緯は `upstream-issue-feedback-loop`。

`terrio` 0.3.2 で、**日本語の文字列値が 7 文字以上（UTF-8 で 19 バイト以上）の GeoJSON**を開くと、panic する。`info`、`convert`、Python の `terrio.open_vector` のどれでも。日本の自治体名、住所、施設名では、普通に起こる。

## やり方（再現）

```sh
printf '{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[139.7,35.7]},"properties":{"name":"東京都千代田区"}}]}' > t.geojson
terrio info t.geojson     # panic
```

## 確かめたこと（何をして、何が起きたか）

- `"東京都千代田区"`（21 バイト）、`"札幌市北区役所庁舎"`: panic。`"札幌市"`（9 バイト）、`"札幌市北区"`（15 バイト）、`"abcdefghij"`: 通る。
- メッセージ: `end byte index 10 is not a char boundary; it is inside '千' (bytes 9..12 of string)`（`geojson.rs:275:22`）。
- Python は `pyo3_runtime.PanicException`。クラスの継承は `BaseException` で、`except Exception` では捕まらない。
- ソース（v0.3.2 と main cf6bd5d で同じ）: `is_datetime` が `b.len() >= 19` を確かめたあと `is_date(&s[..10])` で `&str` をバイト 10 で切る。日本語の 3 バイト文字では、バイト 10 が文字の途中になる。
- **CSV でも同じ**: `csv.rs:587` に同じ `is_date(&s[..10])` がある。`x,y,name` / `139.7,35.7,東京都千代田区` の CSV を `terrio info`、`convert`、Python の `open_vector` で開くと panic（`札幌市北区` は通る）。
- 修正案（下書きに記載）: バイト列のまま比較するか、`s.get(..10)` を使う。
- hfu が issue を投稿した（opengeos/terrio#159。内容は `drafts/upstream/2026-10-21-geojson-panic-on-multibyte-strings.md`）。作者が #161 で修正し、CSV（と MIF の日付）も一緒に直った。CSV のコメント案（`drafts/upstream/2026-10-21-comment-on-159-csv-same-code.md`）は不要になった。
- 注意: 投稿された本文は「GDAL は同じ値を問題なく読む」と書くが、**この環境には GDAL がなく、私は確かめていない**。

## 気をつけること

- 回避策: 当面は、日本語の長い文字列を含む GeoJSON を terrio で読まない。GeoPackage、FlatGeobuf、GeoParquet、PMTiles など別の形式を使う（**他の形式で同じ種類の問題が起きないかは未確認**）。
- 同じ型のバグ（バイト位置での文字列の切り出し）は、`zarr.rs`（パス名）と `csv.rs`（CSV）でも確認した（`japanese-path-panic-in-zarr-parse-name`、`terrio-source-quirks`）。
- 新しい版で直ったら、この塊は `stale` から再確認する。

## 出典

- plays/2026-10-21-first-contact.md
- https://github.com/opengeos/terrio （v0.3.2、crates/terrio/src/drivers/vector/geojson.rs）
- drafts/upstream/2026-10-21-geojson-panic-on-multibyte-strings.md
