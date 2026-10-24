---
id: terrio-ai-disclosure-and-acknowledgements
title: terrio の AI 開示と謝辞：誰の仕事の上にあるか
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
  - terrio docs/acknowledgements.md、README の Disclaimer（main 6779102。#142）
  - PyPI の 0.3.2 の METADATA（README）の検索結果
related: [terrio-license-and-third-party-notices, terrio-source-quirks, upstream-issue-feedback-loop]
---

## 要点

terrio は、**「Claude Opus 5.5（Anthropic の AI モデル）を主に使い、人の指示と確認のもとで作った」と README とドキュメントで開示している**（"primarily built with … working under human direction and review"）。結果は GDAL、PROJ、PDAL と突き合わせて試験しているが、「自分の用途で確かめて、おかしければ報告を」とも書く。謝辞は、土台にした作品と、移植元、データの出どころを具体的に挙げる。kcai の原則 4・5（出どころと、確かめた度合いを残す）と同じ方向の作法。

## やり方（読み方）

- 開示は `README.md` の "Disclaimer" と、`docs/acknowledgements.md` の最初の注意書き。
- 謝辞の各項目は、**ライセンスの出どころの一覧**として読める（`terrio-license-and-third-party-notices`）。

## 確かめたこと（何をして、何が起きたか）

- **開示は #142（2026-10-20 21:53 EDT = 10-21 01:53 UTC）で追加され、0.3.2（2026-10-20 03:22 UTC）の後**。PyPI の 0.3.2 の README（METADATA）で "Disclaimer" と "Claude Opus" を検索したが、**0 件**（played）。公開サイトと main の README にはある。
- **謝辞の内訳**（main の `docs/acknowledgements.md`）:
  - Whitebox: John Lindsay の `whitebox_next_gen`（`wbraster`、`wbvector`、`wbprojection`）の上に始まった。
  - GDAL、PROJ、PDAL: 比較の基準。投影は PROJ（MIT）から移植、楕円体上の gnomonic は `geographiclib-rs`（MIT）、地面分類の CSF は PDAL 同梱コードの移植（Apache-2.0）。EPSG の表は GDAL と PROJ から `scripts/gen_epsg_table.py` で生成。
  - EPSG（IOGP の利用条件）と Esri の投影データ（Apache-2.0）。
  - Python の API は rasterio（BSD-3-Clause、Mapbox）、xarray、rioxarray（Apache-2.0）の形を借りた。
  - 純 Rust のコーデックとフォーマットのクレート（tiff、png、openjp2、jxl-oxide、lerc、flatgeobuf、Arrow/Parquet、netcdf-reader、osmpbfreader、laz、e57 ほか）の表と、道具（clap、rayon、ureq、PyO3、wasm-bindgen）。JPEG 書き出しは IJG の仕事に基づく。
- 末尾に「漏れがあれば issue を」とある。

## 気をつけること

- 「AI が主に作った」という開示は、**品質の保証でも否定でもない**。実測では、日本語の入力で同じ型の panic が 3 か所あり（`terrio-source-quirks`）、一方で報告から数十分で直った（`upstream-issue-feedback-loop`）。
- この開示は**公開サイトと main のもの**。**使っている配布版（0.3.2）の README には含まれない**。
- このリポジトリ（kcai-terrio）の AI 開示は、踏み跡の `authors` に書いている（AI 支援あり）。

## 0.5.0 での再確認（2026-10-24）

`docs/acknowledgements.md`（103 行）が追加された。README の免責と同じ文面（Claude Opus 5.5、人の指示とレビュー）に加え、**Whitebox（John Lindsay の `wbraster` / `wbvector` / `wbprojection`）の上に始まった**こと、GDAL・PROJ・PDAL を基準にしていること、依存先への謝辞が書かれている。これは `terrio-source-scale-and-origins` で crates.io から読んだ起源と整合する。read-docs。

## 出典

- https://terrio.opengeos.org/acknowledgements/
- https://github.com/opengeos/terrio （README の Disclaimer、#142）
