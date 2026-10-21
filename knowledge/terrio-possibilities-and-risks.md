---
id: terrio-possibilities-and-risks
title: terrio が開く可能性と、使うときのリスク
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
as_of: 2026-10-21
sources:
  - plays/2026-10-21-first-contact.md
  - plays/2026-10-21-japan-edge-cases-and-survey.md
  - terrio docs（remote-data、crs、gdal、why-terrio、javascript、mcp）
related: [terrio-source-quirks, hfu-dwg7-workflow-substitution-survey, cloud-native-read-behavior-matrix, terrio-release-vs-main-drift, shapefile-cp932-attributes-not-decoded, vertical-datum-grids-and-geoid-in-japan]
freshness: high
---

## 要点

terrio の価値は「**GDAL を入れられない場所で、GDAL 相当のことが `pip install` だけでできる**」こと。クラウドのセッション、ブラウザ、サーバーレス、CI で効く。一方で、**0.3.2 は日本語の入力でまだ荒く、黙って誤る振る舞いがいくつかある。** 「可能性」は試せたもの・ドキュメントにあるものを分け、「リスク」は実測したものを先に書く。

## 開く可能性

| 可能性 | 根拠 | 確かめ方 |
|---|---|---|
| GDAL なしの環境（このクラウドセッション）で、COG の窓切り出し・再投影・PMTiles の窓読み・形式変換ができる | 6 MiB 前後で 10 km 四方を JGD2011 の平面直角座標系に出した | played |
| 配信しているデータの**健全性検査**（`info` と `TERRIO_HTTP_LOG=YES`）。Range が効くか、サイズ、メタデータを見る | depot.optgeo.org の大きなファイルが Range を無視していると、この道具で気づけた | played |
| PMTiles / COG を、配信用の形から解析用の形（GeoTIFF、GeoJSON、GPKG）に**直接**落とす | ksj_n03_hkd.pmtiles → 札幌周辺の GeoJSON（278 KiB） | played |
| **ブラウザ（WebAssembly）で**読む。データは利用者のブラウザが取りに行く（このセッションの通信制限に縛られない） | npm の `terrio-js`。depot.optgeo.org は CORS が `*`（stars.optgeo.org は未確認） | read-docs（未試験） |
| **AI エージェント**との相性: `--help` が詳しく、GDAL の語彙に沿い、MCP サーバー（`terrio mcp`、main のみ） | 配布版には `mcp` がない | read-docs |
| rasterio 互換 API（`terrio.rio`）で、既存の Python コードの import 差し替え | `windows` `features` `transform` `enums` の import は通った | import だけ played |
| STAC + COG のクラウド処理（STACIT のモザイク） | ドキュメントに例 | read-docs（未試験） |
| 公的データのうち、**UTF-8 の GeoJSON・GPKG・PMTiles と、COG** | 日本語の属性が通った（短い文字列で） | played |

## リスク

**実測したもの（黙って誤る・止まる）**

1. **日本語の相対パスで panic**（`日本地図.tif`）。ほぼ全形式（`japanese-path-panic-in-zarr-parse-name`）
2. **日本語の長い文字列を含む GeoJSON と CSV で panic**（`geojson-japanese-string-panic`）
3. **CP932 の Shapefile が黙って文字化け**（`shapefile-cp932-attributes-not-decoded`）
4. **日本のジオイドが適用されず、高さが黙って変わらない**（`vertical-datum-grids-and-geoid-in-japan`）
5. **縮小（`translate --outsize`、`warp`）で COG をほぼ全量取得**（208 MiB）、**GeoParquet の `info` で 656 MiB を取得**（`cloud-native-read-behavior-matrix`）
6. **配信が Range を無視すると、terrio は全体を読み続ける**（`timeout` が必須。`TERRIO_HTTP_TIMEOUT` の既定は無し）
7. **ドキュメントが配布版より先行**し、記述同士も食い違う（`terrio-release-vs-main-drift`）

**読んで分かる・推測を含むもの**

- **若さ**: 2026-10-14 開始で 0.3.2。最初の 1 週間で 0.1.1 から 0.3.2。挙動や API が頻繁に変わる前提で、版を固定して使う。
- **単独の作者への依存**: `Cargo.toml` の作者は 1 名。土台の `whitebox_next_gen` も別の個人プロジェクト（`docs/why-terrio.md`）。継続性は未知。
- **GDAL との一致は主張**: 2 万件超の比較表がある（`docs/conformance.md`）が、この遊びでは検証していない。**測量成果には使わない。**
- **メモリ**: 非 GeoTIFF の入力は全量をメモリに読む（`docs/gdal.md`）。大きなデータは OOM の恐れ。
- **認証情報**: S3 は `AWS_*` 環境変数や `~/.aws` があると**署名付き**で要求する。公開データだけを使う方針では、環境にその変数がないことを確かめる（公開バケットは `AWS_NO_SIGN_REQUEST=YES`）。
- **ネットワーク**: `TERRIO_NETWORK=ON` で実行時に `cdn.proj.org` へ出て、格子を `~/.cache/terrio/grids` に置く。許可リストの環境では追加が要る。
- **依存**: 335 パッケージ（純 Rust）。監査していない。
- **出力はローカルのみ**。リモートへの書き込みはできない。
- **データのライセンスは別**: terrio（MIT）の許諾はデータに及ばない。

## 気をつけること

- 「可能性」の多くは**未試験**（ブラウザ、MCP、STAC、rasterio 互換の実動作）。次の遊びで `played` にする。
- リスクの 1〜6 は、新しい版で直るかもしれない。直ったら、対応する塊を `stale` から確かめ直して更新する。
- issue の下書き（`drafts/upstream/`）は 4 件。投稿は hfu が確認して行う。

## 出典

- plays/2026-10-21-first-contact.md 、plays/2026-10-21-japan-edge-cases-and-survey.md
- https://terrio.opengeos.org/
