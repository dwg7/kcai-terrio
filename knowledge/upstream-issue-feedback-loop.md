---
id: upstream-issue-feedback-loop
title: 上流への報告から修正までの流れ：opengeos/terrio#159 の体験（AI が下書き、hfu が投稿、作者が当日修正）
status: stale
terrio_version: 0.3.2
terrio_commit: baf4768
interface: cli
environment: GitHub（opengeos/terrio、dwg7/kcai-terrio）と Claude Code クラウドセッション
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - https://github.com/opengeos/terrio/issues/159 （hfu の連絡では closed。このセッションからは本文を読めない）
  - opengeos/terrio のコミット baf4768「Don't panic on long multi-byte strings when sniffing dates (#161)」（2026-10-21 11:23 EDT = 15:23 UTC、Fixes #159）
  - drafts/upstream/2026-10-21-geojson-panic-on-multibyte-strings.md
  - plays/2026-10-21-japan-edge-cases-and-survey.md
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
related: [geojson-japanese-string-panic, japanese-path-panic-in-zarr-parse-name, terrio-release-vs-main-drift, terrio-source-quirks]
upstream_issue: opengeos/terrio#159
upstream_fix: baf4768
---

## 要点

kcai の「鍛える循環」を、**上流のオープンソースへの報告**で実際に回した最初の例。AI（Claude）が見つけて下書きを書き、**hfu が確認して整え、hfu が投稿**し、作者（Qiusheng Wu さん）が**下書きの更新から 43 分後に main で修正**した（hfu の連絡では issue は closed）。修正は main にあり、**配布版（PyPI の 0.3.2）にはまだ入っていない**。

## やり方（この流れで効いたこと）

1. **AI が、動かして見つける**（日本語の GeoJSON を `terrio info` したら panic）。
2. **最小の再現**（1 地物の GeoJSON を `printf` で作る 1 行）、**版と環境**、**原因の場所**（`geojson.rs:275` の `&s[..10]`）、**直し方の案**（バイト列で比べる、または `s.get(..10)`）を下書きに入れる。
3. 敬意をもって、やさしい英語で書く。批判ではなく「試した人の報告」にする。
4. **hfu が確認して整え（`5ba52ef`）、hfu が投稿**する。AI は投稿しない（`AGENTS.md`）。
5. 作者が修正し、issue を閉じる。**配布版に入るのを待って、踏み跡を確かめ直す**（`stale` の運用）。

## 確かめたこと（何をして、何が起きたか）

- 2026-10-21 14:40 UTC（23:40 JST）: hfu が下書きを更新（`5ba52ef`「Refine upstream issue draft for clarity and GDAL comparison」）。この後に hfu が #159 を投稿した（投稿の正確な時刻は、このセッションから issue を読めないため分からない）。
- 2026-10-21 15:23 UTC: 作者のコミット `baf4768`（#161、`Fixes #159`）。変更は `geojson.rs`、`csv.rs`、`datetime.rs`、`mapinfo.rs` の 4 ファイル。`is_datetime` を**バイト列で判定する形**（`is_date_bytes(&b[..10])`）に直した。これは下書きの「直し方の案」のとおり。
- **同じ型の箇所も、作者が一緒に直した**: CSV の読み取り（私は #159 へのコメント案として下書き済みだったが、投稿前に直っていた）と、`parse_date`、MIF の日付の読み取り。
- **回帰テストが付いた**: 下書きの再現例の `東京都千代田区` をそのまま使い、日付に似た名前（`2020-01-0千代田区一丁目`）も加えている。
- 修正は main のみ。PyPI の最新は 0.3.2、タグも v0.3.2 まで（2026-10-21 時点）。main を手元でビルドして確かめる（`plays/2026-10-21-upstream-feedback-loop.md`）。
- **同じ種類の別の箇所（`zarr.rs:1310` の `t[..5]`、日本語の相対パス）は、#161 の変更に含まれず、最新の main（`6779102`）でも残っている**。こちらは別の下書きで、投稿は未了。

## 気をつけること

- **早く直った理由の推測**（根拠は上のとおり）: 再現が 1 行で、原因の行と直し方が書かれていて、敬意があった。作者が短い期間に多くの修正（この日だけで 10 件以上のコミット）を出している。
- **同じ型の弱点は、まとめて探してから報告する**と、1 回で済む。今回は GeoJSON だけを先に報告し、CSV と別の入口（`zarr.rs`）は後から見つけた。作者のほうが先に CSV を直した。
- 下書きは hfu が整える前の私の版と、整えた版で、**未検証の主張**（「GDAL は同じ値を問題なく読む」）が入りうる。この環境には GDAL がなく、私は確かめられない。投稿する前に、確かめていない主張は外すか、確かめた旨を書く。
- この踏み跡の「作者の対応が早い」は、**1 件の体験**。一般化しない。
- kcai としての示唆（`DECISIONS.md` に記録）: 「AI が見つけて下書き → 人が確認して投稿 → 作者が直す → 配布版を待って確かめ直す」の循環が、小さく実際に回った。

## 出典

- https://github.com/opengeos/terrio/issues/159
- https://github.com/opengeos/terrio/commit/baf4768 （#161）
- drafts/upstream/2026-10-21-geojson-panic-on-multibyte-strings.md
