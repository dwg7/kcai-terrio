---
id: terrio-release-vs-main-drift
title: リリース版（PyPI の 0.3.2）と main のずれ：ドキュメントは先行する
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
  - "PyPI: terrio（版 0.1.1, 0.2.0, 0.3.1, 0.3.2）"
  - "opengeos/terrio のタグ v0.3.2（a08e7d8、2026-10-19、Release 0.3.2 #106）と main（cf6bd5d、2026-10-21）"
  - plays/2026-10-21-first-contact.md
  - plays/2026-10-21-untested-items.md（main のビルドと再確認）
related: [terrio-cli-overview, terrio-scope-included-and-excluded]
freshness: high
---

## 要点

**ドキュメント（terrio.opengeos.org、リポジトリの main）は、PyPI の最新版（0.3.2）より先に進んでいる。** main の `Cargo.toml` も `version = "0.3.2"` のままで、版の数字だけでは見分けられない。例: `terrio mcp` は main にあるが、0.3.2 のリリースにはない。

## やり方

```sh
pip install --upgrade terrio && terrio --version          # 配布版
git ls-remote --tags https://github.com/opengeos/terrio   # タグ
terrio --help | grep -c mcp                               # 機能の有無は実際に確かめる
```

読んだソースやドキュメントは、**タグ（例: v0.3.2 = `a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6`）に合わせて**読む。`terrio_commit` には、タグのコミットを書く。

## 確かめたこと（何をして、何が起きたか）

- `pip install --upgrade terrio` → 0.3.2。PyPI には 0.1.1、0.2.0、0.3.1、0.3.2 がある。
- `terrio mcp --help` → `error: unrecognized subcommand 'mcp'`。`terrio --help` にも出ない。
- main（cf6bd5d）の `crates/terrio-cli/src/lib.rs` には `Command::Mcp` があり、タグ v0.3.2（a08e7d8）には `Mcp` がない（grep で 0 件）。
- 一方、`geojson.rs` の panic の箇所は、タグと main で同じ。wheel の panic の行番号（275）は、どちらのソースとも合う。
- **main を実際にビルドして比べた**（`cargo build --release -p terrio-cli`、6 分 33 秒）。`terrio --version` は main も `terrio 0.3.2` と出す。`terrio mcp` は動く（`terrio-mcp-server`）。一方、**日本語の panic（GeoJSON、CSV、相対パス）、CP932 の文字化け、FlatGeobuf の全量取得は、main でも同じ**（日本のジオイドは、3 次元の CRS なら適用される。当初の誤りを訂正した）だった（`plays/2026-10-21-untested-items.md` の 6）。
- main は 2026-10-21 だけで 10 件前後のコミット（座標系、netCDF、Cargo features など）。**リリースの間隔より、main の進みが速い**。

## 更新（2026-10-21 夜）

- main は `6779102`（#164）まで進んだ。PyPI は 0.3.2 のまま。**修正が main に入って、配布版にはまだ出ない**例が出た: GeoJSON / CSV の日本語 panic は #161（`baf4768`）で直ったが、`pip install terrio` で入る 0.3.2 には入っていない（`upstream-issue-feedback-loop`）。

## 気をつけること

- `pip install` した版で、ドキュメントの例が動くとは限らない。動かないときは、タグのドキュメントと照らす。
- 最新のソースから `cargo install` / `maturin` で入れる手もあるが、このセッションでは未試験（Rust の環境の有無も未確認）。
- 「最新に追随する」方針は、PyPI の最新版に追随することを指す（`DECISIONS.md`）。main に追随するかは別の判断。

## 出典

- https://pypi.org/project/terrio/
- https://github.com/opengeos/terrio/tags 、https://terrio.opengeos.org/
- plays/2026-10-21-first-contact.md
