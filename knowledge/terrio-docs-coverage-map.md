---
id: terrio-docs-coverage-map
title: terrio ドキュメント全 25 ページの対応表：どの塊に消化したか、公開サイトとの一致、記述の食い違い
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
verified_how: played
as_of: 2026-10-21
sources:
  - https://terrio.opengeos.org/ の全ページ（sitemap の 25 ページ）と、リポジトリの docs/*.md と ROADMAP.md（main 6779102）
  - plays/2026-10-21-license-and-basics.md
related: [terrio-release-vs-main-drift, terrio-conformance-and-testing-against-gdal, terrio-roadmap-and-open-items, terrio-possibilities-and-risks]
freshness: high
---

## 要点

公開サイト（https://terrio.opengeos.org/）の 25 ページを、すべて読み、塊にした。**サイトは、リポジトリの main の `docs/` と実質的に同じ内容**（サイト側の語が md に含まれる割合は 94〜100%。差は記法とリンク）。**サイトとリポジトリの main は、配布版（0.3.2）より先に進んでいる**。確かめられる記述は動かして確かめ、**ドキュメントの中の食い違いと、配布版との差を 14 件**挙げた。

## やり方（読み方）

- 比較は、各ページの `<article>` の語（英数字の語）と、対応する md（`roadmap` は `ROADMAP.md` を取り込む）の語の集合の重なり。数値は md 側の語がサイトに載る割合（0.84〜0.99）と、サイトの語が md に載る割合（0.94〜1.00）。
- サイトの新しさは、main にだけある語を数点検索して確かめた: `crs/` に `ESRI:54009`、`acknowledgements/` に `cargo-about` と `Claude Opus`、`rust/` に `default-features`、`installation/` に `ARM64`。**すべてサイトにあった**（サイトは main に追随している）。

## 確かめたこと（何をして、何が起きたか）

**ページ → 塊**

| ページ | 消化した塊 |
|---|---|
| Home | `terrio-overview-and-getting-started`、`terrio-scope-included-and-excluded` |
| Why terrio? | `why-terrio-comparison-with-alternatives` |
| Installation | `terrio-install-platforms-and-release-history` |
| Getting Started | `terrio-overview-and-getting-started` |
| Playground | `terrio-js-api-and-playground` |
| Notebooks | `terrio-overview-and-getting-started`（**ノートブックは実行していない**） |
| Command Line | `terrio-cli-overview`、`terrio-cli-command-reference`、`terrio-processing-commands-smoke-test` |
| AI Agents (MCP) | `terrio-mcp-server` |
| Formats | `terrio-formats-rasters-and-compression`、`terrio-formats-vectors-streaming-and-tiles`、`terrio-stac-and-stacit` |
| Point Clouds | `terrio-point-clouds` |
| Remote Data | `cloud-native-read-behavior-matrix`、`cog-remote-window-overview-and-warp`、`pmtiles-remote-reading` |
| Coordinate Systems | `terrio-crs-forms-projections-grids-and-epochs`、`jgd2011-plane-rectangular-transform`、`vertical-datum-grids-and-geoid-in-japan` |
| Coming from GDAL | `terrio-cli-overview`、`terrio-scope-included-and-excluded` |
| Coming from rasterio | `terrio-rio-rasterio-compatible-api` |
| Rust Library | `terrio-rust-library-and-features` |
| Python | `terrio-python-api` |
| xarray | `terrio-xarray-integration` |
| JavaScript | `terrio-js-api-and-playground`、`terrio-js-cloud-native-reads-in-browser` |
| Testing Against GDAL | `terrio-conformance-and-testing-against-gdal` |
| Conformance | `terrio-conformance-and-testing-against-gdal` |
| Benchmarks | `terrio-benchmarks-vs-gdal` |
| Architecture | `terrio-architecture-and-pure-rust-claim` |
| Contributing | `terrio-contributing-and-governance` |
| Acknowledgements | `terrio-ai-disclosure-and-acknowledgements`、`terrio-license-and-third-party-notices` |
| Roadmap | `terrio-roadmap-and-open-items` |

**記述の食い違いと、配布版との差（14 件）**

1. `why-terrio.md`「NTv2 などの格子は**まだ適用しない**」 ⇔ `crs.md`「格子を探して適用する」。実測は後者（EGM96、NADCON5 が適用された）。
2. `architecture.md`「C の依存は Zstandard だけ」 ⇔ `gdal.md`「GDAL バックエンドが唯一の C 依存」 ⇔ wheel の SBOM に `zstd-sys`、`cc`、`ring` がある。
3. `rust.md` の冒頭「公開されたら docs.rs に」 ⇔ crates.io に公開済み（0.1.1〜0.3.2）で、`installation.md` は `cargo add terrio`。
4. `javascript.md` に `openUrl`（範囲読み）の説明がない ⇔ 型定義とロードマップにはある。
5. `rasterio.md`「LERC・LZMA・JPEG XL は復号しない」 ⇔ `formats.md`「読める」。
6. `installation.md`「Windows ARM64 の wheel」 ⇔ PyPI の 0.3.2 に **Windows x64 まで**（ARM64 はない）。
7. `getting-started.md` の `convert … --t-srs EPSG:3857` の例が、**南極の点で失敗**する（0.3.2、main）。
8. **配布版にない機能がサイトにある**: `terrio mcp`、ESRI コード（`ESRI:54009`）、Cargo の feature の分割、AI の開示、第三者告知（`NOTICE`）。
9. `conformance.md` の大半は **2026-10-14、terrio 0.1.1** の結果（座標変換の 2 つだけ 0.3.2）。
10. `benchmarks.md` は、小さなファイルが **0.0.1**、大きなファイルが **0.2.0** の時点。
11. `roadmap` の「1.0: Stable」が完了だが、版は 0.3.2、API は「1.0 まで変わりうる」。
12. `formats.md`「FlatGeobuf（空間インデックスつき）」の bbox は**ローカルの話**で、リモートの CLI は全量取得（JS は範囲読み）。
13. `getting-started.md` の標高タイルの `convert`（窓なし）は、全体を読む例。`translate --srcwin` なら範囲読み。
14. `xarray.md` の `to_zarr` の例は、`zarr` パッケージが要るが、`terrio[xarray]` の extras に入らない。

## 気をつけること

- **ドキュメントは main に追随して先に進む**。配布版（PyPI の 0.3.2）で試して動かないとき、まず `terrio-release-vs-main-drift` を見る。
- 上の 14 件のうち、上流に伝える価値があるものは、hfu が判断して投稿する（`drafts/upstream/`）。**投稿前に、確かめていない主張を外す**。
- ノートブック（Colab）は、実行していない。ブラウザの `playground` は動かした。

## 出典

- https://terrio.opengeos.org/ （sitemap の全ページ）
- plays/2026-10-21-license-and-basics.md
