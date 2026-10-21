---
id: terrio-source-quirks
title: terrio のソースコードの癖（規模、作り、同じ型の弱点）
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、PyPI の wheel）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
interface: rust
verified_on: 2026-10-21
verified_how: read-source
sources:
  - opengeos/terrio のタグ v0.3.2（a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6）と main（cf6bd5d）
  - crates/terrio/src/drivers/{zarr,vector/geojson,vector/csv,vector/shapefile,png,hdf5,netcdf,dem}.rs、crates/terrio/Cargo.toml、.github/workflows/
  - plays/2026-10-21-japan-edge-cases-and-survey.md
related: [geojson-japanese-string-panic, japanese-path-panic-in-zarr-parse-name, shapefile-cp932-attributes-not-decoded, terrio-release-vs-main-drift, terrio-possibilities-and-risks]
freshness: high
finding:
  - same-string-slicing-bug-in-three-drivers
---

## 要点

terrio は、約 10 万行の Rust（4 つのクレート）が、**GDAL を基準に、実データで突き合わせる**ことを方針に書かれている。作りは丁寧だが、**「日本語（マルチバイト文字）を試す入口」が弱い**。同じ型の欠陥（文字列をバイト位置で切る）を、3 か所で実際に踏んだ。**読んだのはソースで、全体を監査したわけではない。**

## 確かめたこと（何をして、何が起きたか）

**規模と作り（read-source）**

- Rust edition 2024、MSRV 1.90、MIT、作者表記は Qiusheng Wu さん。ワークスペースは `crates/terrio`（本体）、`crates/terrio-cli`、`python`（PyO3）、`js`（WebAssembly）。`.rs` の合計は約 10.3 万行（インラインのテストを含む）。`#[test]` は 456、結合テストのファイルは 22。`Cargo.lock` は 335 パッケージ。
- 本体の `src` は、形式ごとのドライバー（`drivers/`）、座標系（`crs/`）、処理（`ops/`）、タイル（`tiles/`）、点群（`pointcloud/`）、ストリーム変換（`stream/`）、仮想ファイルシステム（`vfs.rs`、`http.rs`、`s3.rs`）に分かれる。並列化は `rayon`（WebAssembly では逐次）。
- 形式の符号化は、whitebox_next_gen の `wbraster` / `wbvector` / `wbprojection` を土台にし、誤りが見つかったものは自前のドライバーで置き換える方針（`docs/why-terrio.md`）。
- 機能は cargo の feature で切れる（main で追加。0.3.2 には入っていない）。
- ワークフローは 7 本（`ci`、`ci-platforms`、`claude-code-review`、`docs`、`release`、`release-build`、`release-dry-run`）。`ci.yml` のジョブに、GDAL バックエンドのビルド、MSRV、API ドキュメント、npm がある。`docs/conformance.md`（443 行）に、GDAL との 2 万件超の比較結果が載る。**この比較は主張で、この遊びでは検証していない。**
- `unsafe` は 71 行、9 ファイル。内訳: GDAL バックエンドの FFI（feature で任意）、JPEG 2000 の FFI（`jp2.rs`）、SQLite のロック（`libc::flock`）と mmap、`dem.rs` の x86 の SSE 命令（`_mm_rsqrt_ss`）。`.unwrap()` は全体で 786 回だが、テストを除くと少ない（最初の `#[cfg(test)]` より前で 186 回、うち 109 は `stream/tests.rs`）。

**同じ型の弱点：文字列をバイト位置で切る（played + read-source）**

| 場所 | コード | 結果 |
|---|---|---|
| `drivers/zarr.rs:1310`（`parse_name`） | `t[..5].eq_ignore_ascii_case("ZARR:")` | 日本語の相対パスで panic（**played**）。**全形式の入口** |
| `drivers/vector/geojson.rs:275`（`is_datetime`） | `is_date(&s[..10])` | 日本語の文字列 7 文字以上で panic（**played**） |
| `drivers/vector/csv.rs:587` | 同上 | CSV でも panic（**played**） |
| `drivers/png.rs:89`（`read_world_file`） | `&ext[..1]` | 再現できなかった（未知の拡張子は先に拒否される） |
| `drivers/hdf5.rs:37`、`netcdf.rs:22` | `s.get(..5).filter(...)` | **安全な書き方**。同じ作りの `zarr.rs` だけが違う |

- **更新（2026-10-21 夜）**: `geojson.rs` と `csv.rs` は、作者が #161 で直した（バイト列で判定。`parse_date` と MIF の日付も）。`zarr.rs:1310` は最新の main でも残っている。
- 安全な書き方が同じコードベースに既にある。Clippy の `string_slice`（バイト位置での文字列スライスを警告する）を有効にすれば、機械的に拾える（**提案。試していない**）。
- panic はエラーとして扱われず、CLI は Rust のバックトレース（41 行ほど）を標準エラーに出して終了コード 1、Python では `BaseException` 系の `PanicException`。

**ほかの癖（read-source / played）**

- **「宣言」と実装の食い違い**: `shapefile.rs` の先頭コメントは「`.cpg` が宣言するとおりにデコード」と書くが、実装は UTF-8 / Latin-1 の二択（`shapefile-cp932-attributes-not-decoded`）。`docs/why-terrio.md` は格子を適用しないと書き、`docs/crs.md` は適用すると書く。
- **黙って続ける**: 適用できる変換がないと高さは保たれる（ドキュメントに明記）。サーバーが Range を無視しても全体を読み続ける。DBF の文字コード不明は文字化けのまま。エラーより「それらしい結果」を返す傾向がある。
- **GDAL の癖を再現する**: 出力の座標は `x y`（経度 緯度）、オプション名は GDAL の kebab-case、`--overview` の番号など。GDAL に慣れた人には自然だが、GDAL のドキュメントは参照にならない部分もある。
- **配布版と main の乖離**: `main` の `Cargo.toml` が 0.3.2 のまま進む（`terrio-release-vs-main-drift`）。

## 気をつけること

- ここに挙げた弱点は、**日本語の入力で実際に踏んだもの**が中心。ほかの言語（韓国語、アラビア語など）でも同様だと推測できるが、試していない。
- 挙げた行番号は v0.3.2 のもの。main では動く可能性がある。新しい版が出たら再確認する。
- 「癖」は評価ではなく観察。テストの量や、GDAL と突き合わせる姿勢は、むしろ強み。

## 出典

- https://github.com/opengeos/terrio （v0.3.2）
- plays/2026-10-21-japan-edge-cases-and-survey.md
