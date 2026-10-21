# kcai-terrio

[terrio](https://github.com/opengeos/terrio)（GDAL を使わない Pure Rust の地理空間データ入出力ライブラリ）で、**クラウドネイティブなデータをクラウドネイティブに触って遊びきり**、その遊びから得た知識を [kcai](https://github.com/dwg7/kcai)（Knowledge Co-created with AI（AI と共創した知識））の方式で Markdown の踏み跡として残すリポジトリです。kcai の最初期のインスタンスの一つで、「変化の速い分野で、版と確認日を記録する仕組みが役に立つか」を試す場でもあります。

管理責任者: hfu（外部への発信、承認、マージの権限）。準拠する kcai: `dwg7/kcai` コミット 66d3840（2026-10-21）。

## 中身

- [`knowledge/`](knowledge/README.md): 踏み跡（題名、状態、確かめた版の一覧つき）
- [`plays/`](plays/): 遊びの記録（日時、terrio の版、環境、コマンド、結果、発見）
- [`drafts/upstream/`](drafts/upstream/): terrio への issue の下書き（投稿は hfu が確認して行う）
- [`docs/index.html`](docs/index.html): ブラウザ（WebAssembly）で遊ぶページ（terrio-js を CDN から版を固定して読む。GitHub Pages で公開予定）
- [`DECISIONS.md`](DECISIONS.md): 決めたことと理由、kcai との食い違い
- [`AGENTS.md`](AGENTS.md): AI 向け案内の本体（`CLAUDE.md` は入口だけ）

## 方針（要約）

- 常に最新の terrio（`pip install --upgrade terrio`）を使い、**遊ぶたびに版を記録**する。版が上がったら、影響しそうな踏み跡を `stale` にして確かめ直す。
- ファイルを丸ごとダウンロードしない。範囲読み込み（HTTP Range）でどこまで扱えるかを試すことが、遊びの中心。
- 動かして確かめたこと（`played`）と、読んだだけのこと（`read-docs` / `read-source`）を区別する。
- 日本ローカル（JGD2011、平面直角座標系、日本語属性）を意識的に試す。
- 公開データだけを使い、認証情報は扱わない。大きなデータは入れない。

## 謝辞

terrio は Qiusheng Wu さん（[opengeos](https://github.com/opengeos)）の作品です（MIT ライセンス）。2026 年 10 月に始まったばかりのプロジェクトが、短い期間に大きく育っていることに敬意を表します。ドキュメントは https://terrio.opengeos.org にあります。

kcai の考え方は [dwg7/kcai](https://github.com/dwg7/kcai) にあります。

## ライセンス

このリポジトリの文書とコードは **CC0 1.0** です。**terrio 自体（MIT）や、遊びで使ったデータのライセンスには適用されません。** 各データの利用条件は、それぞれの提供元に従ってください（国土地理院、国土数値情報、Sentinel-2、Overture Maps、Protomaps などは、それぞれ条件が異なります）。

---

## English summary

kcai-terrio plays with [terrio](https://github.com/opengeos/terrio) — a pure-Rust, GDAL-free geospatial I/O library by Qiusheng Wu (opengeos) — on cloud-native data (COG, PMTiles, GeoParquet, STAC) and records what was learned as small Markdown traces, following [kcai](https://github.com/dwg7/kcai). Every trace records the terrio version, environment, date, and whether it was actually run (`played`) or only read. Findings that look like bugs become issue drafts in `drafts/upstream/`, which the maintainer (hfu) reviews before posting. CC0 1.0; it does not apply to terrio (MIT) or the datasets used.
