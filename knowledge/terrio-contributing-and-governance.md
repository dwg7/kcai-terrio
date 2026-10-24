---
id: terrio-contributing-and-governance
title: terrio への貢献の作法と、プロジェクトの運営の様子
status: draft
terrio_version: 0.5.0
terrio_commit: 6779102281ad2835cbc23fba3138e01a138bc6f9
interface: rust
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-24
verified_on: 2026-10-24
verified_how: read-docs
as_of: 2026-10-21
sources:
  - terrio docs/contributing.md、docs/testing.md（main 6779102）
  - opengeos/terrio のリポジトリの構成（.github、ルートのファイル）、git の履歴
  - upstream-issue-feedback-loop の経験
related: [upstream-issue-feedback-loop, terrio-license-and-third-party-notices, terrio-source-quirks, terrio-install-platforms-and-release-history]
---

## 要点

**「GDAL と違う読み方をするファイルを付けたバグ報告が、特に役に立つ」**と、貢献ページが明言する。変更は、**GDAL との比較（実ファイルで）**、**純 Rust のまま（C のツールチェーンを要しない依存は不可、WebAssembly でもビルドできる）**、**公開項目はすべて文書化**、**GDAL の名前に合わせる**、の 4 つの指針に従う。最小の Rust は 1.90、引き上げには「公開から 6 か月未満の Rust にはしない」などの規則がある。運営は、**単独の作者が短い間隔で多数のコミットを出す**形で、報告への対応は速かった（1 件の体験）。

## やり方（貢献前の確認一覧、read-docs）

```sh
cargo fmt --all
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
TERRIO_TEST_DATA=../terrio-data cargo test --workspace      # 実データでの GDAL との比較
cargo build -p terrio --target wasm32-unknown-unknown       # WebAssembly でもビルドできること
RUSTDOCFLAGS="-D warnings" cargo doc -p terrio --no-deps    # 公開項目の文書化
cargo +1.90 check --workspace --all-targets                 # 最小の Rust
pre-commit run --all-files
```

GDAL バックエンドを変えるなら、GDAL を入れて `--features gdal` で clippy とテストを回す。ドキュメントは Zensical（`pip install zensical && zensical serve`）。

## 確かめたこと（何をして、何が起きたか）

- 貢献ページの 4 つの指針と、MSRV 方針（1.90。`msrv` の CI ジョブ、`Cargo.toml`、クレートのドキュメント、このページを一緒に変える。1.0 以降は minor リリースでだけ引き上げる）を読んだ。
- **リポジトリの構成（played: `ls`）**: ルートに `LICENSE`、`NOTICE`、`LICENSE-THIRD-PARTY.md`、`README.md`、`ROADMAP.md`、`Cargo.toml`、`clippy.toml`、`rustfmt.toml`、`.pre-commit-config.yaml`。`.github` には `dependabot.yml`、`scripts/`、ワークフロー 7 本。**`SECURITY.md`、`CODE_OF_CONDUCT.md`、`CHANGELOG`、`CONTRIBUTING.md`（ルート）は見当たらなかった**（変更履歴はコミットのタイトルとリリースのまとめ）。
- **運営の様子（git の履歴、直近）**: 2026-10-21 の 1 日だけで 10 件以上のコミット（座標系、netCDF、Cargo の feature、第三者告知など）。コミットのタイトルは「何を、どう直したか」を 1 文で書く形で、PR 番号（#106〜#164）が付く。
- **報告への対応**: #159（日本語の長い文字列の panic）は、hfu の下書き更新から 43 分後に、回帰テストつきで修正された（`upstream-issue-feedback-loop`）。**これは 1 件の体験で、一般化しない**。

## 気をつけること

- 「GDAL と比較せよ」という方針は、**報告の書き方**にも効く: ファイルと、GDAL の出力があると取り込まれやすいはず（推測。#159 は GDAL の出力なしでも直った）。
- 脆弱性の報告窓口（`SECURITY.md`）は見当たらない。**セキュリティに関わる報告は、公開の issue で出してよいか分からない**ので、必要になったら作者に確かめる。
- 単独の作者に依存する運営（`Cargo.toml` の authors は 1 名）。継続性は未知（`terrio-possibilities-and-risks`）。
- 貢献のルール（外部への PR）は、このリポジトリでは扱わない（`AGENTS.md`: 発信は hfu が行う）。

## 0.5.0 での再確認（2026-10-24）

`docs/contributing.md` は 0.3.2 から変更なし。貢献者はコミット上 Qiusheng Wu のほかに Daniel Hofbauer（COG の修正・速度。#165、#168）、William Katzenmeyer（#98）。issue #212（ベンチマークの GDAL の多スレッド）や #159（この遊びの報告）が数日で取り込まれ、**報告が反映される運営**が続いている。read-source。

## 出典

- https://terrio.opengeos.org/contributing/ 、https://terrio.opengeos.org/testing/
- https://github.com/opengeos/terrio （main 6779102 の構成と履歴）
