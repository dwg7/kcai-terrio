---
id: terrio-rust-library-and-features
title: Rust ライブラリ：入口、Cargo の feature、API の安定性方針（配布版との差に注意）
status: draft
terrio_version: 0.3.2
terrio_commit: 6779102281ad2835cbc23fba3138e01a138bc6f9
interface: rust
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、Node 22、Chromium 1194）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: read-docs
as_of: 2026-10-21
sources:
  - terrio docs/rust.md（main 6779102）
  - crates.io の terrio 0.3.2（Cargo.toml の license、features）、v0.3.2 タグの crates/terrio/Cargo.toml
related: [terrio-architecture-and-pure-rust-claim, terrio-release-vs-main-drift, terrio-contributing-and-governance, terrio-install-platforms-and-release-history]
freshness: high
---

## 要点

Rust の入口は `terrio::open`（形式を判定し、ラスタかベクタを返す）、`open_raster`、`open_vector`、`open_raster_lazy`（GeoTIFF/COG をヘッダーで開き、`read_window` で窓のタイルだけ復号）、`terrio::memory`（バイトから）、`terrio::stream`（メモリを超えるベクタ）、`terrio::arrow`、`terrio::ops`（コマンドの実体）、`terrio::crs`、`terrio::pointcloud`。**データモデルは `wbraster::Raster` と `wbvector::Layer` をそのまま再エクスポートしており、どちらかの破壊的な更新を terrio が取り込むと、terrio の破壊的リリースになる**。`1.0` に向けた API 方針を明文化している。**ドキュメントの Cargo feature の節は main のもので、0.3.2 のタグには入っていない**。

## やり方（読み方）

```rust
let ds = terrio::open("countries.gpkg")?;                       // Dataset::Raster か Dataset::Vector
let mut cog = terrio::open_raster_lazy("s3://bucket/image.tif")?;
let w = cog.read_window(terrio::Window::new(0, 0, 512, 512), &terrio::WindowOptions { bands: vec![1], overview: Some(0) })?;
terrio::stream::convert("buildings.gpkg", "buildings.fgb", &ConvertOptions::default())?;
```

- 書き出し: `write_raster_dataset(&ds, path, &RasterWriteOptions { driver: Some(RasterDriver::Cog), compression: Some("DEFLATE".into()), ..Default::default() })`、`write_vector(&layers, path, &VectorWriteOptions)`（GeoPackage は複数層）。既存の出力への追記・上書きは `ops::vector_filter::write_vector_with_mode`。
- 操作: `ops::warp::warp(&[&dem], &WarpOptions { dst_srs, resampling, ..Default::default() })`、`translate::translate` など。座標: `Transformer::new(&src, &dst)?.transform(x, y)`。

## 確かめたこと（何をして、何が起きたか）

- **API の安定性方針（read-docs）**: 
  - オプションの構造体はすべて `Default`（`..Default::default()` で作る）。新しいオプションは、旧来の動作を保つ既定値のフィールドとして足す（破壊的変更とは見なさない）。
  - 増える列挙（`Error`、`RasterDriver`、`VectorDriver`、`Kind`）は `#[non_exhaustive]`。
  - エラーは表示用のメッセージを持つ。`Error::Raster` と `Error::Vector` が形式ライブラリのエラーを包む。
  - MSRV は 1.90。
- **Cargo の feature（main）**: 既定ですべてのドライバーが有効。`default-features = false` で絞れる（例: COG の書き出しだけなら `features = ["geotiff"]`）。核（常に）: GeoTIFF/COG、生・ASCII のラスタ、PNG/JPEG、VRT、STAC、GeoJSON、TopoJSON、Shapefile、KML/KMZ、GML、GPX、CSV、MapInfo、CRS、操作、ストリーム。feature: `parquet`、`remote`（URL、`s3://` など、PROJ の CDN の格子。ネイティブのみ）、`netcdf-hdf5`、`sqlite`（GeoPackage）、`tiles`、`avif`、`zarr`、`jp2`、`flatgeobuf`、`osm`、`pointcloud`、`lerc`、`lzma`、`gdal`（既定オフ）。外したドライバーは、API には残り、開こうとすると "built without the `zarr` feature" で失敗する。**`geotiff` だけでも JPEG XL の復号器が入る**（`wbraster` が依存するため）。
- **0.3.2 のタグとの差（played / read-source）**: main の `terrio` クレートの `[features]` は上の一覧（`default` に多数）だが、**v0.3.2 のタグは `[features] default = []`**（feature 分けは #154 で main に入った）。**ドキュメントの例 `terrio = { version = "0.3", default-features = false, features = ["geotiff"] }` は、0.3.2 の crate ではそのまま通るか未確認**。
- **ドキュメントの食い違い**: ページの冒頭は「API リファレンスは、terrio が**公開されたら** docs.rs にある。それまでは `cargo doc`」と書く（古い記述）。一方、terrio は crates.io に**公開済み**（0.1.1〜0.3.2）。同じサイトの `installation.md` は `cargo add terrio` を案内する。冒頭の依存の書き方は `git = …` のまま。
- **WebAssembly**: ライブラリは `wasm32-unknown-unknown` でビルドでき、ネットワークと一時ファイルはネイティブのみ。JPEG 2000 には、グローバルアロケータ `terrio::NullSafeAllocator` と、リンクフラグ `-C link-arg=--allow-undefined` が要る（OpenJPEG の移植が null ポインタを解放するため）。
- この塊は**ドキュメントを読んだもの**。Rust のコードは、この遊びでは書いて動かしていない。

## 気をつけること

- 配布版（0.3.2）と main で、feature の構成が違う。**使う版のタグの `Cargo.toml` で確かめる**（`terrio-release-vs-main-drift`）。
- データモデルが外部クレートなので、`wbraster` / `wbvector` の版は terrio の再エクスポートに合わせる（直接依存しない）。
- 単独の作者の `wbraster` 系は別プロジェクト（`terrio-possibilities-and-risks`）。

## 出典

- https://terrio.opengeos.org/rust/ 、https://docs.rs/terrio
- https://crates.io/crates/terrio 、https://github.com/opengeos/terrio （v0.3.2 のタグ）
