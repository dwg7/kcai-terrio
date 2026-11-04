---
id: terrio-geometry-provenance-and-clean-room
title: terrio の幾何ルーチンの出所：GEOS 由来を退け、JTS の移植とクリーンルームで置き換えた経緯
status: draft
terrio_version: 0.7.0
terrio_commit: f24cd15
interface: rust
environment: Claude Code クラウドセッション。opengeos/terrio の v0.7.0 のソース（docs/jts-provenance.md、geos-retirement-audit.md、make-valid-*.md、CHANGELOG.md、NOTICE）を読んだ
verified_on: 2026-11-04
verified_how: read-docs
sources:
  - https://github.com/opengeos/terrio （v0.7.0: docs/jts-provenance.md、docs/geos-retirement-audit.md、docs/make-valid-clean-room-spec.md、docs/make-valid-implementation.md、CHANGELOG.md の 0.6.0「Licensing」「Geometry implementation provenance」）
  - knowledge/terrio-license-and-third-party-notices.md
  - knowledge/terrio-vs-gdal-spot-checks.md
authors:
  - hfu の指示のもと、AI（Claude）がドキュメントを読んで記述。AI 支援あり。法的助言ではなく、技術的な読み
reviewed_by: []
updated: 2026-11-04
related: [terrio-license-and-third-party-notices, terrio-source-scale-and-origins, terrio-possibilities-and-risks, terrio-vs-gdal-spot-checks, terrio-architecture-and-pure-rust-claim]
freshness: high
---

## 要点

0.5.0 で入った幾何の検査・修復・バッファ・オーバーレイは、**GEOS の挙動と一致**していた（この遊びで確かめた）。ところが 0.6.0 のあと、プロジェクトは**幾何ルーチンの「出所」を整理し直した**: GEOS 由来だった実装を退け、**JTS（Eclipse Distribution License 1.0）の移植**か、**独立して書き直した実装**に置き換えた。ライセンス表記も **MIT AND MPL-2.0** になった。

- **JTS 1.20.0 の移植**: 簡略化、凸包・凹包、Delaunay 三角分割、制約つき三角分割、タイルのクリップ範囲の計算ほか（`docs/jts-provenance.md`）。ポリゴンカバレッジの検証・簡略化・クリーニングは、JTS の後のコミット（1.20.0 + 226 コミット）から。EDL-1.0 の著作権表示を `NOTICE` に載せる。
- **「クリーンルーム」の実装**: タイルのポリゴン修復（旧 `tiles/valid.rs` の MakeValid）は、**振る舞いの仕様書**（`make-valid-clean-room-spec.md`、51 の参照観測つき）を別の研究役が確認し、**隔離された実装者**が仕様だけから書いて、保管者が出所の記録を分けて持つ、という手順で置き換えた（`make-valid-implementation.md`）。**実装の記録には、AI 提供者・サンドボックスの起動器・ログイン情報に依存しないテストにした**と書かれている。
- **監査**: `geos-retirement-audit.md` は、置き換えた経路の一覧と証拠を示す。GEOS の名前・版・実行呼び出しは残らず、テストに GEOS の導入は要らない。`+proj=geos`（静止衛星の投影法）は GEOS ライブラリとは無関係と注記している。「**技術的な目録であって、リポジトリ全体の法的な確認ではない**」と明記している。
- 点群の固有値ソルバー（`pointcloud/filters/selfadjoint.rs`）だけが MPL-2.0。

## 読み取れること

1. **品質の物差しは変わらない**（GDAL / GEOS と比べる）が、**実装の出所は別**にする、という二段構え。結果が一致すること（この遊びの確認）と、コードの由来がきれいなことは別の話で、後者に手間をかけている。
2. **AI が主に書くプロジェクトの、ライセンス上の用心**として読める。AI が既存のコードに似たものを書いてしまうリスクに、出所の記録・移植元の固定・隔離した再実装で対応している。kcai の「出典のない断定をしない」と通じる。
3. dwg7 にとっては、**0.5.0 で確かめた「GEOS と一致」は、実装が置き換わった後も成り立つか**を確かめ直す価値がある（0.7.0 で `make-valid` / `buffer` / `dissolve` を再実行して、一致を確認した。下の節）。
4. 利用側は、**古い版の `NOTICE` は古い**（CHANGELOG が「更新を勧める」と明記）ので、配布に含めるなら 0.6.0 以降の表記を使う。

## 確かめたこと（何をして、何が起きたか）

- v0.7.0 のドキュメントと CHANGELOG を読んだ（read-docs）。幾何の挙動は、0.7.0 の wheel で `make-valid` / `buffer` / `dissolve` を実行して GEOS と比べた（played。下の節）。

## 気をつけること

- 法的な評価はしていない。書かれていることの要約で、正しさ（クリーンルームが成立しているか）は確かめていない。
- 「隔離された実装者」が何であったか（人か AI か）は、読んだ範囲では断定できない。仕様書は「別の研究役」「新しいエージェントの完全な道具アクセスが承認された境界に従うこと」と書き、AI のエージェントを使ったことを示唆するが、**詳細は未確認**。

## 0.7.0 での再確認（2026-11-04）

0.7.0 の wheel で、`make-valid`・`buffer`・`dissolve` が GEOS（GDAL 3.8.4 の Python 結合）と一致することを確かめた（played）。実装が置き換わった後も、少なくともこの試料では挙動が保たれている。

## 出典

- https://github.com/opengeos/terrio （v0.7.0）の `docs/jts-provenance.md`、`docs/geos-retirement-audit.md`、`docs/make-valid-clean-room-spec.md`、`docs/make-valid-implementation.md`、`CHANGELOG.md`、`NOTICE`
