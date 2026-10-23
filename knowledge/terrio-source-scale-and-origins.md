---
id: terrio-source-scale-and-origins
title: terrio のソースコードの規模と起源（誰が、いつ、何の上に作ったか）
status: draft
terrio_version: 0.4.2
terrio_commit: 17ca35a
interface: rust
environment: Claude Code クラウドセッション。opengeos/terrio の浅い複製（履歴 181 コミット）の v0.4.2 タグを数えた。crates.io の公開情報と、cargo のレジストリにある依存のソース
verified_on: 2026-10-23
verified_how: read-source
sources:
  - https://github.com/opengeos/terrio （v0.4.2、main 17ca35a。git log、Cargo.toml、Cargo.lock、README.md の Disclaimer、docs/acknowledgements.md）
  - https://crates.io/api/v1/crates/（wbraster、wbvector、wbprojection ほかの公開情報）
  - knowledge/terrio-ai-disclosure-and-acknowledgements.md
  - knowledge/terrio-source-quirks.md
authors:
  - hfu の指示のもと、AI（Claude）が数えて記述。AI 支援あり。行数は wc による単純な行数で、コメントと空行を含む
reviewed_by: []
updated: 2026-10-23
related: [terrio-ai-disclosure-and-acknowledgements, terrio-architecture-and-pure-rust-claim, terrio-source-quirks, terrio-possibilities-and-risks, terrio-release-vs-main-drift, terrio-contributing-and-governance]
freshness: high
---

## 要点

- **規模**: terrio 本体（`crates/terrio`）の Rust は約 **10.3 万行・177 ファイル**。CLI が約 3 千行、Python 結合が約 5 千行、JS 結合が約 2.6 千行。テスト（`tests/`）が約 8.4 千行、ドキュメントが約 3.6 千行・32 ページ。**依存を含めると、実質の規模はその 2〜3 倍以上**（Whitebox 系の 3 つの crate だけで約 15 万行。`Cargo.lock` は 336 crate）。
- **起源**: **2026-10-14 に Qiusheng Wu さん（opengeos）が始めた**。初日に 49 コミット、最初の機能 PR（#3）だけで約 5 千行。**ほぼ全部が Claude Opus 5.5 による AI 製**で、人が指示とレビューをする、と README の免責に明記されている。
- **土台**: ラスタ・ベクタ・座標系の核は、John Lindsay さん（Whitebox、`whitebox_next_gen`）の **`wbraster` / `wbvector` / `wbprojection`**（MIT OR Apache-2.0、2026-03-31 公開）。terrio は、これらの上に、ドライバー、操作、CLI、結合を足した「統合層」。点群・JPEG 2000・LERC・HDF5 などは、別の Rust crate を使う。
- **開発の速さ**: 9 日間で 181 コミット、v0.1.0 から v0.4.2 まで 9 回のタグ。**v0.4.0〜0.4.2 は 2026-10-22 に出た**（この遊びの踏み跡は 0.3.2 で確かめたもの）。

## 数えたもの

### 規模（v0.4.2、行数）

| 場所 | 行数 | 備考 |
|---|---|---|
| `crates/terrio/src/drivers` | 33,925 | 形式ごとのドライバー（最大） |
| `crates/terrio/src/ops` | 14,283 | warp / translate / dem / calc / vector 操作ほか |
| `crates/terrio/src/pointcloud` | 11,814 | LAS / LAZ / COPC / EPT / E57 / PLY、フィルタ |
| `crates/terrio/src/crs` + `crs.rs` | 11,619 | 座標系の変換、格子、エポック |
| `crates/terrio/src/tiles` | 6,225 | MBTiles / PMTiles / MVT |
| `crates/terrio/src/stream` | 3,074 | ストリーム変換 |
| `crates/terrio/src` その他 | 約 21,000 | `cog.rs`、`dataset.rs`、`stac.rs`、`http.rs`、`gdal_backend.rs` ほか |
| **terrio 本体の合計** | **102,816**（177 ファイル） | |
| `crates/terrio-cli` | 3,293（23 ファイル） | |
| `python/`（Rust の結合 + Python） | 5,080 | PyO3 |
| `js/`（WebAssembly 結合） | 2,632 | |
| `crates/terrio/tests` | 8,362 | 実データ試験、GDAL / PROJ との比較 |
| `docs/` | 3,643（32 ファイル） | |

- 試験: `#[test]` が 564 個、インライン試験のあるファイルが 102。`TODO` / `FIXME` は 3 個だけ。`unsafe` は 67 行（`.unwrap()` 935 は試験コードを含む数で、実装だけの数ではない）。
- データ: 座標系表 `crates/terrio/data/epsg.tsv.zst`（312 KB。GDAL 3.12.2 / PROJ 9.7.1 から**生成**したと、コミットメッセージにある）。試験用に `proj_strings.tsv`（894 KB）、`world_projections.tsv`（390 KB）。
- feature は 17 個（0.4.2 では `[features]` で絞れる。0.3.2 の crate では絞れなかった。`terrio-rust-library-and-features`）。

### 成長（結合を含む Rust 全体の行数）

| 日 | ファイル | 行数 |
|---|---|---|
| 2026-10-14（初日） | 141 | 約 61,000 |
| 10-15 | 171 | 約 87,500 |
| 10-17 | 191 | 約 103,000 |
| 10-20 | 200 | 約 106,600 |
| 10-22 | 214 | 約 113,800（結合を含む全体） |

初日の約 6 万行は、人が 1 日で書く量ではない。AI が書いた、という免責と整合する。以降の伸びは緩やかで、修正・比較・文書が増える。

### 起源（誰が書いたか）

| 項目 | 内容 |
|---|---|
| 作者 | Qiusheng Wu（opengeos の主宰。`geemap` などで知られる）。コミットの 167/181（別名 `giswqs` の 1 件を含めると 168）。残りは dependabot 10、Daniel Hofbauer 2（COG の概観の再サンプリングと平均の修正、速度向上。#165、#168）、William Mark Katzenmeyer 1（hdf5-reader の修正への追随。#98） |
| AI | README の免責: 「terrio は、主に **Claude Opus 5.5** で作られ、人の指示とレビューのもとにある。結果は GDAL / PROJ / PDAL と比べて試験しているが、自分の用途で確かめてほしい」。コミットメッセージにも "Address Claude review feedback" が 18 回。MCP サーバーも内蔵 |
| 作り方の特徴 | PR ごとに大きく（数千行）入り、「GDAL と一致する」ことを試験で担保する。座標系表は GDAL / PROJ から生成。CI で GDAL との比較を走らせる |
| 土台の crate | `wbraster`（約 5.5 万行）、`wbvector`（約 2.2 万行）、`wbprojection`（約 7.3 万行）。いずれも John Lindsay さん（`jblindsay`、Whitebox）が 2026-03-31 に公開。同じ人の `wbgeotiff`、`wbhdf` も 0.4 系の依存にある |
| 他の依存 | `geographiclib-rs`（georust、2020〜）、`openjp2`（OpenJPEG の Rust 移植、Neopallium）、`laz`（laz-rs、tmontaigu）、`e57`（cry-inc）、`flatgeobuf`（Børge Harrtell ら）、`lzma-rust2`、`rusty_av1d`（AV1 復号）、`lerc-reader` と `hdf5-reader` / `netcdf-reader`（i-norden、2026 年公開の新しい crate）ほか。`Cargo.lock` は 336 crate |

## 読み取れること

1. **「Pure Rust」の主張は、依存先の Rust 製ライブラリ群が成熟したからこそ成り立つ**。特に、Whitebox 系 3 crate と、`openjp2`・`laz`・`e57` のような既存の Rust 移植が土台。terrio の独自部分（10 万行）は、その上の統合と操作。
2. **AI 製で、規模が大きく、歴史が 9 日**。長く使われて磨かれた GDAL（数百万行規模と言われるが、ここでは数えていない）との差は、行数ではなく、実データでの経験の量にある。試験と GDAL 比較が品質の頼りで、この遊びで見つけた穴（日本語パス・文字化け・極点）は、まさに「人の現場データ」が足りなかった所に当たる。
3. **新しい crate への依存が多い**（`wb*`、`lerc-*`、`hdf5-reader` など、2026 年公開）。これらの更新が terrio の挙動を変えうる。版を固定して使い、`Cargo.lock` を見る。
4. **作者が速く直す**（#159 は報告の翌日以内に #161）。AI を前提にしたレビューと修正の速度が、品質を支えている可能性。ただし、単一の作者への依存でもある（貢献者は 3 人）。

## 気をつけること

- 行数は `wc -l` による**単純な行数**（コメント・空行・試験を含む）。品質や複雑さの指標ではない。
- 履歴は**浅い複製の 181 コミット**で、全部ではない可能性がある（始まりの 2026-10-14 までは届いている）。
- `Claude Opus 5.5` は README の記載であって、各コミットの AI 関与の割合は**確かめていない**。「ほぼ全部が AI 製」は初日の規模などからの推定。
- GDAL の規模は概数で、数えていない。
- 0.4.x は 2026-10-22 に出ており、この遊びの他の踏み跡（0.3.2 で確かめた）は、新版で確かめ直すまで `stale` 扱いとして読むこと。

## 出典

- https://github.com/opengeos/terrio （v0.4.2）の `git log`、`Cargo.toml`、`Cargo.lock`、`README.md`（Disclaimer）、`docs/acknowledgements.md`
- crates.io の各 crate の公開情報（2026-10-23 に取得）
