# 踏み跡の一覧

`status` は kcai の `draft | reviewed | stable | deprecated` に、このリポジトリ独自の `stale`（新しい版でまだ確かめ直していない）を足したもの。AI は `reviewed` 以上にしない。形式は `AGENTS.md`。

| 踏み跡 | 状態 | 確かめた版 | 確かめた日 | 確かめ方 |
|---|---|---|---|---|
| [advice-for-dwg7](advice-for-dwg7.md): dwg7 に対する助言（作業が進むごとに更新する生きた踏み跡） | draft | 0.5.0 | 2026-10-21 | played |
| [cloud-native-read-behavior-matrix](cloud-native-read-behavior-matrix.md): クラウドネイティブな形式の読み込み方：どこまで範囲読み込みか（一覧） | draft | 0.3.2 | 2026-10-21 | played |
| [cog-remote-window-overview-and-warp](cog-remote-window-overview-and-warp.md): リモート COG の窓読み・overview・縮小の使い分け | draft | 0.4.2 | 2026-10-24 | played |
| [data-licenses-of-play-datasets](data-licenses-of-play-datasets.md): 遊びで使ったデータのライセンス表記（配信元が書いていること） | draft | 0.5.0 | 2026-10-24 | read-docs |
| [geojson-japanese-string-panic](geojson-japanese-string-panic.md): 日本語の長い文字列を含む GeoJSON と CSV で terrio が panic する（0.3.2） | draft | 0.5.0 | 2026-10-24 | played |
| [hfu-dwg7-workflow-substitution-survey](hfu-dwg7-workflow-substitution-survey.md): hfu と dwg7 の公開リポジトリの処理のうち、terrio で代替できそうなものと、できなさそうなもの | draft | 0.5.0 | 2026-10-24 | read-source |
| [japanese-path-panic-in-zarr-parse-name](japanese-path-panic-in-zarr-parse-name.md): 日本語から始まる相対パスで terrio が panic する（Zarr 名の判定） | draft | 0.5.0 | 2026-10-24 | played |
| [jgd2011-plane-rectangular-transform](jgd2011-plane-rectangular-transform.md): JGD2011 と平面直角座標系（EPSG:6669〜6687）の変換と、測地系のずれ | draft | 0.5.0 | 2026-10-24 | played |
| [pmtiles-remote-reading](pmtiles-remote-reading.md): PMTiles をリモートで読む（ラスタ・ベクタ、日本語属性、Range を無視する配信） | draft | 0.5.0 | 2026-10-24 | played |
| [shapefile-cp932-attributes-not-decoded](shapefile-cp932-attributes-not-decoded.md): CP932（Shift_JIS）の Shapefile 属性が、黙って文字化けする | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-ai-disclosure-and-acknowledgements](terrio-ai-disclosure-and-acknowledgements.md): terrio の AI 開示と謝辞：誰の仕事の上にあるか | draft | 0.5.0 | 2026-10-24 | read-docs |
| [terrio-architecture-and-pure-rust-claim](terrio-architecture-and-pure-rust-claim.md): terrio の構成と「純 Rust」の中身（ドキュメントと SBOM を突き合わせる） | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-benchmarks-vs-gdal](terrio-benchmarks-vs-gdal.md): GDAL との速度とメモリの比較（作者の計測）と、読むときの注意 | draft | 0.5.0 | 2026-10-24 | read-docs |
| [terrio-cli-command-reference](terrio-cli-command-reference.md): コマンドごとの主なオプションと決まり（cli.md の要約と、確かめた点） | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-cli-overview](terrio-cli-overview.md): terrio コマンドラインの概要（GDAL のどのコマンドに当たるか） | draft | 0.5.0 | 2026-10-24 | read-docs |
| [terrio-conformance-and-testing-against-gdal](terrio-conformance-and-testing-against-gdal.md): GDAL との突き合わせ試験と適合性レポート：何を、いつ、どの版で比べたか | draft | 0.5.0 | 2026-10-24 | read-docs |
| [terrio-contributing-and-governance](terrio-contributing-and-governance.md): terrio への貢献の作法と、プロジェクトの運営の様子 | draft | 0.5.0 | 2026-10-24 | read-docs |
| [terrio-crs-forms-projections-grids-and-epochs](terrio-crs-forms-projections-grids-and-epochs.md): 座標系：受け付ける書式、計算できる投影、格子の探し方、高さとエポック | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-docs-coverage-map](terrio-docs-coverage-map.md): terrio ドキュメント全 25 ページの対応表：どの踏み跡に消化したか、公開サイトとの一致、記述の食い違い | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-evolution-0-3-2-to-0-4-2](terrio-evolution-0-3-2-to-0-4-2.md): terrio の進化の方向（0.3.2 から 0.4.2、そして main） | draft | 0.4.2 | 2026-10-24 | read-source |
| [terrio-formats-rasters-and-compression](terrio-formats-rasters-and-compression.md): 対応形式（ラスタ）と圧縮：表をバイナリの terrio formats と突き合わせた | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-formats-vectors-streaming-and-tiles](terrio-formats-vectors-streaming-and-tiles.md): 対応形式（ベクタ・タイル・Arrow）：ストリーム変換、GeoParquet 1.1、タイルの書き出し、南極で落ちる例 | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-install-platforms-and-release-history](terrio-install-platforms-and-release-history.md): terrio の入れ方、対応環境、版の履歴（PyPI・npm・crates.io） | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-js-api-and-playground](terrio-js-api-and-playground.md): terrio-js の API と、公式プレイグラウンド：Node とブラウザで動かして確かめた | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-js-cloud-native-reads-in-browser](terrio-js-cloud-native-reads-in-browser.md): ブラウザ（WebAssembly）で terrio を使う：openUrl の範囲読み込みと、このリポジトリのページ | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-license-and-third-party-notices](terrio-license-and-third-party-notices.md): terrio のライセンス：MIT、同梱される依存と第三者の告知、0.3.2 の配布物に LICENSE がない件 | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-mcp-server](terrio-mcp-server.md): terrio の MCP サーバー（terrio mcp）：配布版にはなく、main にある | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-overview-and-getting-started](terrio-overview-and-getting-started.md): terrio の概観と入門の手順（トップページ、Getting Started、Notebooks を実際に動かす） | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-point-clouds](terrio-point-clouds.md): 点群（LAS/LAZ/COPC/EPT/PLY/E57）：範囲読み、フィルター、グリッド化、ドキュメントの例の再現 | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-possibilities-and-risks](terrio-possibilities-and-risks.md): terrio が開く可能性と、使うときのリスク | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-processing-commands-smoke-test](terrio-processing-commands-smoke-test.md): 処理系コマンドの動作確認（calc、dem、grid、filter、sieve、proximity、polygonize、rasterize、mosaic、COG） | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-python-api](terrio-python-api.md): Python API（terrio）：ドキュメントの例 30 件を動かした結果 | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-release-vs-main-drift](terrio-release-vs-main-drift.md): リリース版（PyPI の 0.3.2）と main のずれ：ドキュメントは先行する | draft | 0.5.0 | 2026-10-21 | played |
| [terrio-rio-rasterio-compatible-api](terrio-rio-rasterio-compatible-api.md): rasterio 互換 API（terrio.rio）：実際の利用コードの呼び出しが通るか | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-roadmap-and-open-items](terrio-roadmap-and-open-items.md): terrio のロードマップ：完了とされたこと、未完了の 21 項目、設計の決定 | draft | 0.5.0 | 2026-10-24 | read-docs |
| [terrio-rust-library-and-features](terrio-rust-library-and-features.md): Rust ライブラリ：入口、Cargo の feature、API の安定性方針（配布版との差に注意） | draft | 0.5.0 | 2026-10-24 | read-docs |
| [terrio-scope-included-and-excluded](terrio-scope-included-and-excluded.md): terrio が含む機能と含まない機能 | draft | 0.5.0 | 2026-10-24 | read-docs |
| [terrio-source-quirks](terrio-source-quirks.md): terrio のソースコードの癖（規模、作り、同じ型の弱点） | draft | 0.5.0 | 2026-10-24 | read-source |
| [terrio-source-scale-and-origins](terrio-source-scale-and-origins.md): terrio のソースコードの規模と起源（誰が、いつ、何の上に作ったか） | draft | 0.4.2 | 2026-10-23 | read-source |
| [terrio-stac-and-stacit](terrio-stac-and-stacit.md): STAC と STACIT：検索結果のモザイク、max_items で転送量を減らす | draft | 0.4.2 | 2026-10-24 | played |
| [terrio-vs-gdal-spot-checks](terrio-vs-gdal-spot-checks.md): GDAL 3.8.4 との突き合わせ（約 30 項目）：一致したこと、食い違い、訂正したこと | draft | 0.5.0 | 2026-10-24 | played |
| [terrio-xarray-integration](terrio-xarray-integration.md): xarray 連携（terrio.xarray）：リモート COG を遅延で開き、窓だけ取って再投影する | draft | 0.5.0 | 2026-10-24 | played |
| [upstream-issue-feedback-loop](upstream-issue-feedback-loop.md): 上流への報告から修正までの流れ：opengeos/terrio#159 の体験（AI が下書き、hfu が投稿、作者が当日修正） | draft | 0.5.0 | 2026-10-24 | played |
| [vertical-datum-grids-and-geoid-in-japan](vertical-datum-grids-and-geoid-in-japan.md): 格子とジオイド：日本の高さの変換は「3 次元の CRS」から（GDAL と突き合わせて訂正した） | draft | 0.5.0 | 2026-10-24 | played |
| [why-terrio-comparison-with-alternatives](why-terrio-comparison-with-alternatives.md): terrio と他の選択肢（GDAL、gdal クレート、GeoRust、GeoArrow、whitebox、OxiGeo）：どれを選ぶか | draft | 0.5.0 | 2026-10-24 | read-docs |

`played` は実際に動かした。`read-docs` / `read-source` は読んだだけ。

## 読む順序の目安

1. 入口（ドキュメントの全体）: `terrio-docs-coverage-map`（全ページ → 踏み跡の対応表と、食い違い 14 件）、`terrio-overview-and-getting-started`、`terrio-cli-overview`、`terrio-scope-included-and-excluded`、`why-terrio-comparison-with-alternatives`
2. 版と配布: `terrio-release-vs-main-drift`、`terrio-evolution-0-3-2-to-0-4-2`（進化の方向）、`terrio-install-platforms-and-release-history`、`terrio-license-and-third-party-notices`、`terrio-roadmap-and-open-items`
3. クラウドネイティブ: `cloud-native-read-behavior-matrix`（一覧表。入口別の比較つき）、`cog-remote-window-overview-and-warp`、`pmtiles-remote-reading`、`terrio-stac-and-stacit`、`terrio-point-clouds`、`terrio-js-cloud-native-reads-in-browser`
4. 使い方: `terrio-cli-command-reference`、`terrio-processing-commands-smoke-test`、`terrio-python-api`、`terrio-rio-rasterio-compatible-api`、`terrio-xarray-integration`、`terrio-rust-library-and-features`、`terrio-js-api-and-playground`、`terrio-mcp-server`、`terrio-formats-rasters-and-compression`、`terrio-formats-vectors-streaming-and-tiles`
5. 日本ローカル: `jgd2011-plane-rectangular-transform`、`terrio-crs-forms-projections-grids-and-epochs`、`vertical-datum-grids-and-geoid-in-japan`、`shapefile-cp932-attributes-not-decoded`、`japanese-path-panic-in-zarr-parse-name`、`geojson-japanese-string-panic`
6. 品質と評価: `terrio-conformance-and-testing-against-gdal`、`terrio-vs-gdal-spot-checks`、`terrio-benchmarks-vs-gdal`、`terrio-architecture-and-pure-rust-claim`、`terrio-source-quirks`、`terrio-source-scale-and-origins`、`terrio-possibilities-and-risks`、`hfu-dwg7-workflow-substitution-survey`
7. 運営と上流: `terrio-contributing-and-governance`、`upstream-issue-feedback-loop`、`terrio-ai-disclosure-and-acknowledgements`、`data-licenses-of-play-datasets`
8. 助言（生きた踏み跡。作業ごとに更新）: `advice-for-dwg7`
