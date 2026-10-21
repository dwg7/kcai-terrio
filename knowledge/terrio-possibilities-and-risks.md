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
  - plays/2026-10-21-untested-items.md
  - terrio docs（remote-data、crs、gdal、why-terrio、javascript、mcp）
related: [terrio-js-cloud-native-reads-in-browser, terrio-mcp-server, terrio-rio-rasterio-compatible-api, terrio-processing-commands-smoke-test, terrio-source-quirks, hfu-dwg7-workflow-substitution-survey, cloud-native-read-behavior-matrix, terrio-release-vs-main-drift, shapefile-cp932-attributes-not-decoded, vertical-datum-grids-and-geoid-in-japan]
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
| **ブラウザ（WebAssembly）で**範囲読みする。データは利用者のブラウザが取りに行く（このセッションの通信制限に縛られない）。**CLI が全量取る FlatGeobuf・GeoParquet も範囲読み**（5 GB の日本の建物から東京駅周辺 119 棟を 16.4 MiB） | 実 Chromium で 6 つの配信先が成功（`docs/index.html`、`terrio-js-cloud-native-reads-in-browser`） | played |
| **AI エージェント**との相性: ツールの説明が各コマンドの `--help` 全文で、GDAL の語彙に沿う。MCP サーバー（`terrio mcp`、main のみ）は、panic しても落ちずに `isError` を返す | JSON-RPC を直接話して確認（`terrio-mcp-server`）。配布版にはない | played（main のビルド） |
| rasterio 互換 API（`terrio.rio`）で、既存の Python コードの import 差し替え | 実際の利用コード（snow-hokkaido）の呼び出し 12 件が通った。値の同等性は未確認（`terrio-rio-rasterio-compatible-api`） | played |
| STAC + COG のクラウド処理（STACIT のモザイク）。東京の 3 シーンから 512² の窓が約 17.5 MiB | 重なる全シーンから読む（`cloud-native-read-behavior-matrix`） | played |
| COPC 点群をクラウドから必要な範囲・粗さだけ取る（`--bounds`、`--max-level`） | 700 ft 四方が 6.9 MiB、レベル 2 で 1.6 MiB | played |
| 公的データのうち、**UTF-8 の GeoJSON・GPKG・PMTiles と、COG** | 日本語の属性が通った（短い文字列で） | played |

## リスク

**実測したもの（黙って誤る・止まる）**

1. **日本語の相対パスで panic**（`日本地図.tif`）。ほぼ全形式（`japanese-path-panic-in-zarr-parse-name`）
2. **日本語の長い文字列を含む GeoJSON と CSV で panic**（`geojson-japanese-string-panic`）
3. **CP932 の Shapefile が黙って文字化け**（`shapefile-cp932-attributes-not-decoded`）
4. **日本のジオイドが適用されず、高さが黙って変わらない**（`vertical-datum-grids-and-geoid-in-japan`）
5. **縮小（`translate --outsize`、`warp`）で COG をほぼ全量取得**（208 MiB）、**GeoParquet の `info` で 656 MiB を取得**、**FlatGeobuf は `--spat` でも全量**、JPEG 2000 の overview もほぼ全体（`cloud-native-read-behavior-matrix`）
6. **配信が Range を無視すると、terrio は全体を読み続ける**（`timeout` が必須。`TERRIO_HTTP_TIMEOUT` の既定は無し）
7. **ドキュメントが配布版より先行**し、記述同士も食い違う（`terrio-release-vs-main-drift`）
8. **中断すると、ダウンロード中の一時ファイルが残る**（5 GB の GeoParquet を 8 秒で打ち切ると 221 MB が `/tmp/terrio-XXXX/` に残った）。ディスクの割り当てに注意し、`timeout` で止めたあとに掃除する
9. **COG の `TILING_SCHEME` が黙って無視される**。`warp --dstalpha` がない（`terrio-processing-commands-smoke-test`）
10. **入口によって結果が違う**（CLI / Python と WebAssembly で、FlatGeobuf と GeoParquet の読み方が違う）

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

- 「可能性」のうち、ブラウザ、MCP（main）、STACIT、rasterio 互換（呼び出しの通り方）は `played` にした。値の同等性、Claude Code への MCP 登録、Hugging Face は**未試験**。
- リスクの 1〜6 は、新しい版で直るかもしれない。直ったら、対応する塊を `stale` から確かめ直して更新する。
- issue の下書きは `drafts/upstream/`。GeoJSON の panic は hfu が #159 として投稿済み。残りの投稿は hfu が確認して行う。

## 出典

- plays/2026-10-21-first-contact.md 、plays/2026-10-21-japan-edge-cases-and-survey.md
- https://terrio.opengeos.org/
