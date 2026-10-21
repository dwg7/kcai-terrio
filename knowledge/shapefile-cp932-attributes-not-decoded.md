---
id: shapefile-cp932-attributes-not-decoded
title: CP932（Shift_JIS）の Shapefile 属性が、黙って文字化けする
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
  - plays/2026-10-21-japan-edge-cases-and-survey.md（2）
  - crates/terrio/src/drivers/vector/shapefile.rs の decode と dbf_layout（v0.3.2）
  - drafts/upstream/2026-10-21-shapefile-cp932-not-decoded.md
related: [japanese-path-panic-in-zarr-parse-name, hfu-dwg7-workflow-substitution-survey, terrio-source-quirks]
hazard: silent-mojibake-shapefile-cp932
finding:
  - dbf-text-is-utf8-or-latin1-only
---

## 要点

**terrio 0.3.2 は、Shapefile の属性（DBF）を「UTF-8、そうでなければ Latin-1」としか読めない。** 日本の公的データに多い CP932（Shift_JIS）の Shapefile は、エラーも警告もなく文字化けして読まれる。`.cpg` に `CP932` や `SHIFT_JIS` と書いても、環境変数 `SHAPE_ENCODING=CP932`（GDAL の流儀）を付けても変わらない。GDAL / ogr2ogr の `--config SHAPE_ENCODING CP932` で動いている処理は、そのままでは置き換えられない。

## やり方（再現）

```sh
# UTF-8 の Shapefile を作り、DBF の ABCDEF を CP932 のバイト列に置き換える
terrio convert a.geojson sj.shp          # name = "ABCDEF"
python3 -c "p='sj.dbf';b=open(p,'rb').read();open(p,'wb').write(b.replace(b'ABCDEF','札幌市'.encode('cp932')))"
rm sj.cpg
terrio convert sj.shp out.geojson        # name が文字化け
```

## 確かめたこと（何をして、何が起きたか）

- 結果の `name`: `\x8eD\x96y\x8es`（CP932 のバイトを 1 バイトずつ Latin-1 として並べたもの）。
- `.cpg` を `CP932`、`SHIFT_JIS`、`Shift_JIS`、`932` にしても同じ。`SHAPE_ENCODING=CP932` も同じ。
- ソース: `dbf_layout` は `.cpg` に `UTF-8`・`UTF8`・`65001` が含まれるかだけを見る。`decode` は「バイト列が正しい UTF-8 ならそのまま、`utf8` が真なら lossy な UTF-8、そうでなければ Latin-1」。エンコーディングのライブラリは使われていない。DBF の言語ドライバー ID のバイトも使われない。
- モジュール先頭のコメントは「`.cpg` が宣言するとおりにデコードする」と書くが、実装は UTF-8 / Latin-1 の二択（ドキュメントと実装の食い違い）。
- 書き出しは常に UTF-8 + `.cpg`。

## 気をつけること

- **黙って壊れる**のが危険。属性を使う処理（市町村名のコードの突き合わせなど）が、気づかず誤る。
- 回避策: terrio に渡す前に、別の道具（Python の `dbf` 読み取りなど）で UTF-8 に直す。または GDAL の `ogr2ogr` を使う。
- UTF-8 の Shapefile（`.cpg` が UTF-8）は問題なく、日本語も通る（`convert` の往復で確認済みの範囲）。
- フィールド名（DBF のヘッダー）も同じ関数でデコードされるので、日本語のフィールド名は影響を受けるはず（**未確認**）。

## 出典

- plays/2026-10-21-japan-edge-cases-and-survey.md
- https://github.com/opengeos/terrio （v0.3.2、crates/terrio/src/drivers/vector/shapefile.rs）
- drafts/upstream/2026-10-21-shapefile-cp932-not-decoded.md
