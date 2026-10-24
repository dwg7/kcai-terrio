---
id: terrio-architecture-and-pure-rust-claim
title: terrio の構成と「純 Rust」の中身（ドキュメントと SBOM を突き合わせる）
status: stale
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: rust
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - terrio docs/architecture.md、docs/why-terrio.md、docs/gdal.md、docs/index.md（main 6779102）
  - PyPI の terrio 0.3.2 の wheel に入っている SBOM（sboms/terrio-py.cyclonedx.json）
related: [terrio-source-quirks, terrio-license-and-third-party-notices, why-terrio-comparison-with-alternatives]
---

## 要点

**構成**: `crates/terrio`（本体: `dataset.rs` が開く・読む・書く・形式判定、`formats.rs` が GDAL の短い名前のドライバー表、`drivers/` が自前のドライバー、`geotiff.rs`/`cog.rs` が遅延読み、`tiles/`、`vfs.rs` が場所の解決、`http.rs`/`s3.rs` が範囲要求と AWS SigV4、`crs.rs`、`ops/`、`memory.rs`、`info.rs`）、`terrio-cli`、`python/`（PyO3）、`js/`（wasm-bindgen）、`scripts/`（試験データ、GDAL との比較、ベンチマーク）。**「純 Rust」は、完全には純ではない**: ドキュメントは「C の依存は Zstandard のコーデックだけ」と書くが、wheel の SBOM には、ほかにも C を含むクレートがある。

## やり方（読み方）

- データモデル: ラスタは `wbraster::Raster`（型つきのバッファ、バンドごと・行ごと、位置情報と CRS）に、ドライバーと nodata の宣言を足した `RasterDataset`。ベクタは `wbvector::Layer`（OGC のシンプルフィーチャ、Z と M、型つき属性とスキーマ）。GeoTIFF とタイルのアーカイブは遅延で開ける。
- 土台は whitebox_next_gen の 3 つのクレート（`wbraster`、`wbvector`、`wbprojection`）。GDAL と突き合わせて誤りが見つかった所は、自前のドライバーで置き換えた（GeoTIFF、JPEG 2000、Zarr、netCDF、HFA、GeoPackage（自前の SQLite の読み書き）、Esri 形式、FlatGeobuf、CSV、GeoJSON、GeoParquet、GML、GPX、KML、TopoJSON、MapInfo、OSM、Shapefile の書き出し）。上流の不具合は、置き換えた PR に書かれている。
- 並列: ネイティブは rayon（GeoTIFF のタイルの符号化、COG の overview、warp（出力行ごと）、rasterize（行の帯）、Zarr のチャンク、ベクタの地物）。**結果は入力順に結合し、単一スレッドと同じバイト列になる**と書く。WebAssembly は同じコードを逐次で走らせる。

## 確かめたこと（何をして、何が起きたか）

- ドキュメント間の記述（main）:
  - `docs/architecture.md`: 「C の依存は **Zstandard のコーデックだけ**（WebAssembly にもコンパイルされる）。JPEG 2000 は OpenJPEG の Rust 移植で、C のアロケータ呼び出しは terrio が提供」。
  - `docs/gdal.md`: GDAL バックエンドは「**terrio の唯一の C 依存**」（任意の feature）。
  - `docs/index.md`: 「C の依存なしで」。
- **wheel の SBOM（played）**: C やアセンブリを含む可能性のあるクレートの名前が並ぶ: `zstd`、`zstd-safe`、`zstd-sys`（Zstandard の C ライブラリの結合）、`cc`（C のビルド用）、**`ring`**（暗号。`rustls` が使う。C とアセンブリを含むことが知られている。**この環境では中身を確かめていない**）、`libc`、`brotli` と `lzma-rust2`、`ruzstd` は純 Rust。
- したがって、**「C の依存は Zstandard だけ」は、PyPI の 0.3.2 の wheel の SBOM とは合わない可能性がある**（`ring` の扱い次第。`ring` はリモート入出力の TLS 用で、WebAssembly 版には入らないはず。**未確認**）。ドキュメントの 3 つの記述（Zstandard だけ、GDAL バックエンドだけ、C なし）が、互いに少しずつ違う。
- ほかの観察は `terrio-source-quirks` にある（規模、unsafe、panic の素地）。

## 気をつけること

- 「純 Rust」「GDAL なし」は、**使う側にとっての実用上の意味**（システムに入れるものがない、WebAssembly でも動く、静的に配れる）では成り立つ。「依存に C が一切ない」という意味では、そのまま受け取らない。
- 結果が「単一スレッドと同じバイト列」という主張は、この遊びでは検証していない。
- 構成の記述は main のもの。0.3.2 のタグでは、機能の分け方（Cargo の feature）などが違う（`terrio-release-vs-main-drift`）。

## 出典

- https://terrio.opengeos.org/architecture/ 、https://terrio.opengeos.org/why-terrio/ 、https://terrio.opengeos.org/gdal/
- plays/2026-10-21-license-and-basics.md
