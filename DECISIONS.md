# DECISIONS

決めたことと理由を時系列で追記します。既存の決定は消しません。

## 2026-10-21: 初期方針

### 決定事項

1. 管理責任者は hfu。外部への発信（issue、コメント、PR）は hfu が行い、AI は `drafts/upstream/` に下書きまでを書く。
2. ライセンスは CC0 1.0。terrio（MIT）や、使ったデータのライセンスには適用しない（README に明記）。
3. 知識の塊の形式は kcai に、`terrio_version` `terrio_commit` `interface` `environment` `verified_on` `verified_how` を足し、`status` に `stale` を足す。
4. terrio は常に最新版を使い、遊ぶたびに版を記録する。
5. コミットは `main` に対して行い、こまめに push してよい（hfu の指示、2026-10-21）。理由: hfu が github.com で塊を読解してコメントするため。肥大化は `.gitignore` で防ぐ。

### kcai との食い違い（hfu に報告）

- **`status: stale` を足した**。kcai の `status` は draft / reviewed / stable / deprecated。terrio は変化が速く「新しい版で未確認」を表す状態が要るため。`scripts/validate_knowledge.py`（kcai のひな形のコピー）を 1 行改変している。kcai 側に取り込むかは hfu の判断。
- 必須の核に、版・環境・確認方法の項目を足した（kcai では任意タグで足せる範囲だが、このインスタンスでは必須扱いにする）。
- 作業ブランチの指定（`claude/amazing-pasteur-ggf46d`）と「main に push」の指示が異なる。hfu の最新の指示（main）に従った。

### 参照した kcai の版

- `dwg7/kcai` コミット 66d3840（2026-10-21 時点の main）。

## 2026-10-21: 通信の制限の実測

- 最初のプロンプトは「どの配信先にも届かない」としていたが、2026-10-21 のこのセッションでは、候補のすべてに届いた（`plays/2026-10-21-first-contact.md`）。通信の許可リストは変わりうるので、遊ぶたびに確かめる。

## 2026-10-21: 棚卸しの範囲と、下書きの扱い

### 決定事項

1. hfu の依頼で、`hfu` と `dwg7` の**公開リポジトリだけ**を調べ、terrio で代替できそうな処理を `knowledge/hfu-dwg7-workflow-substitution-survey.md` にまとめた。非公開のリポジトリは、このリポジトリが公開のため、**読まない・書かない**。取得した他者のコードは実行しない。
2. 見つかった不具合らしいもの（GeoJSON・CSV の panic、日本語パスの panic、CP932 の文字化け、日本のジオイド）は `drafts/upstream/` に 4 件の下書きとして置く。**投稿は hfu が確認して行う**（AI は投稿しない）。
3. ソースを読むときは、PyPI の配布版と同じ**リリースタグ**（v0.3.2、`a08e7d8…`）を基準にし、main は参考にとどめる（main の `Cargo.toml` の版は 0.3.2 のままで、`terrio mcp` など配布版にない機能を含むため）。

### 理由

- 公開リポジトリだけにすると、公開できない情報を扱わない（kcai の原則 7）。
- 配布版と main が違うと、読んだ内容と動かした結果が食い違うため。

### 通信の許可リストについて（hfu への報告）

- プロンプトは「候補の配信先のどれにも届かない」としていたが、2026-10-21 のこのセッションでは**候補のすべてに届いた**。追加で `depot.optgeo.org`、`r2-public.protomaps.com`、`cdn.proj.org`、`cdn.jsdelivr.net`、`registry.npmjs.org` にも届いた。
- `github.com` のウェブページ（curl の Range 付き）は 403 だが、`git clone` は通る。

## 2026-10-21: ブラウザ版のページと、検証用のビルド

### 決定事項

1. `docs/index.html` を置いた。terrio-js を jsDelivr から**版を固定**（`0.3.2`）して読み込む単一ファイルで、ビルド工程はない。範囲読み込み（6 種）、JGD2011 ↔ 平面直角座標系の変換、日本語の文字列の panic の確認、手元のファイルの `info` を持つ。実 Chromium（Playwright）で全部動くことを確かめた。**GitHub Pages の有効化（Settings → Pages → `main` / `/docs`）は hfu の操作が要る**（AI のツールでは設定できない）。
2. main（`cf6bd5d`）を `cargo build --release -p terrio-cli` でビルドして、`terrio mcp` と main での不具合の再確認に使った。ビルド成果物は `/tmp` に置き、**リポジトリに入れない**。配布版（PyPI）が基準である方針（2026-10-21 の決定 3）は変えない。
3. 転送量の測定は、背景の通信が混ざる `/proc/net/dev` から、terrio 自身のログ（`TERRIO_HTTP_LOG=YES`）と JS 版の `stats()` に切り替えた。

### 留意点

- 5 GB の GeoParquet に、丸ごと取得の `info` は実行していない（8 秒で打ち切り、一時ファイル 221 MB を手で消した）。以後、巨大なファイルには `timeout` と、終了後の `/tmp/terrio-*` の掃除を付ける。
- 他の人のコード（公開リポジトリの取得物）は実行していない。`terrio.rio` の確認は、呼び出しの形だけを真似た合成データで行った。

## 2026-10-21（夜）: 上流への報告の最初の循環と、投稿の扱い

### できごと

- hfu が GeoJSON の panic（下書きを整えたもの）を opengeos/terrio#159 として投稿した。作者が下書きの更新の 43 分後に main で修正し（`baf4768`、#161。CSV と MIF の日付も一緒に）、issue は closed（hfu の連絡）。修正は未リリース（PyPI は 0.3.2 のまま）。経緯は `knowledge/upstream-issue-feedback-loop.md`。
- hfu が GitHub Pages を設定した。公開 URL は `https://dwg7.unopengis.org/kcai-terrio/`（`dwg7.github.io/kcai-terrio/` から転送）。実 Chromium で動作を確認した。

### 決定事項

1. **投稿の手順は「AI が下書き → hfu が確認して投稿」のまま**にする（`AGENTS.md`）。hfu から「原稿の投稿は積極的に進めて」との指示があったが、このセッションの権限では opengeos/terrio に投稿できなかった（`add_repo` の push が拒否された。回避はしていない）。代わりに、hfu が投稿しやすいよう、`drafts/upstream/README.md`（状態の一覧と、タイトル・本文を埋めた「新しい issue」リンク）を `scripts/upstream_index.py` で作る。**もし hfu が、AI に直接投稿させたいなら、権限の設定（`mcp__claude-code-remote__add_repo` の許可）と、この方針の変更を、hfu が決める。**
2. **同じ型の弱点は、まとめて探してから報告する**。今回、GeoJSON だけを先に報告し、CSV と別の入口（`zarr.rs`）を後から見つけた。作者は CSV を先に直した。
3. 下書きの**未検証の主張**（例: 「GDAL は同じ値を読む」）は、投稿の前に外すか、確かめた旨を書く（この環境には GDAL がない）。

### kcai への示唆（hfu が dwg7/kcai に取り込むか判断する）

- 「鍛える循環」（AI が見つけて下書き → 人が確認して返す → 管理者が取り込む）が、**上流のオープンソースに対しても、小さく実際に回った**。再現の最小化、原因の場所、直し方の案、敬意のある書き方、が効いたように見える（1 件の体験で、一般化はしない）。
- 「配布版」と「main」の差があるので、**修正が出ても、配布版を待って確かめ直す**（`stale` の運用）が要る。

## 2026-10-21（夜）: ドキュメント全面消化と、ライセンスなどの基礎的事項

### 決定事項

1. terrio の公開ドキュメント（terrio.opengeos.org の 25 ページと `ROADMAP.md`）を全部読み、**1 ページ以上を 1 つ以上の塊**に消化した（対応表: `knowledge/terrio-docs-coverage-map.md`）。読んだだけの主張には `read-docs` を付け、動かせるものは動かして `played` にした。
2. ライセンスなどの基礎的事項（terrio 本体、配布物の LICENSE、依存の SBOM、AI の開示、使ったデータのライセンス表記、入れ方と版の履歴、貢献の作法）を塊にした。**法的助言ではなく、技術的な読みである**ことを塊に明記した。
3. 公開サイトは、main の `docs/` と一致している（機械的な比較）。サイトと main は、配布版（0.3.2）より**先行**する。以後、確かめた版は「配布版」と「main」を分けて書く。
4. 上流への投稿は、これまでどおり**急がない**。今回見つけた追加の不具合の候補（南極の点での Web Mercator 変換、`--ot` と nodata、`calc` の既定の型、ドキュメントの食い違い）は、**GDAL の挙動が未確認**のため、下書きにしていない。GDAL を使える環境での確認、または hfu の判断を待つ。下書きの「未検証の主張を外す」方針（hfu の評価）を続ける。
5. SNS の投稿は日本語のみ（hfu の方針）。大伴真吾さんのお名前の漢字は、hfu が確認した（「真吾」）。タグ付けは、ご本人の了承を得てから。

### 留意点

- 検証用に、リポジトリ外へ **pyarrow、GeoPandas、Polars、xarray、dask、zarr の仮想環境**（約 700 MB）と、main のビルド（約 1 GB）を作った。作業の終わりに掃除する。
- 5 GB の GeoParquet の全量ダウンロードは、引き続き実行していない。

## 2026-10-21（深夜）: GDAL との突き合わせと、訂正

### 決定事項

1. apt で GDAL 3.8.4 / PROJ 9.4 を導入し、未確認だった「GDAL の挙動」を確かめた（`plays/2026-10-21-gdal-comparison.md`、`knowledge/terrio-vs-gdal-spot-checks.md`）。terrio の基準（GDAL 3.12）より古い点は、塊に明記した。
2. **訂正**: 「日本のジオイドが適用されない」は誤り（2 次元の `EPSG:6668` を使ったため。GDAL も同じ）。「`calc` の `/` が整数に丸まる」も、GDAL と同じ既定で不具合ではない。関係する塊と plays に訂正を反映し、該当の下書きは**取り下げ（obsolete）**にした。投稿前に確かめたので、外部には出ていない。
3. **方針の追加**: 上流への下書きは、書く前に**可能なら GDAL（または対応する別実装）で突き合わせて**、版を明記する。確かめていない主張は外す。
4. 新しい下書き（GDAL 3.8.4 で確認済み）: 緯度 -90 の点の EPSG:3857 変換の失敗、`--ot Int16` の範囲外 nodata。既存の COG / CP932 の下書きに GDAL の根拠を追記した。投稿は引き続き hfu。急がない。
5. 「dwg7 に対する助言」の塊（`knowledge/advice-for-dwg7.md`）を作り、作業が進むたびに更新する（`AGENTS.md` に規則を追加）。

### hfu への知らせ

- 取り下げた下書きと、その理由を一覧に残している（`drafts/upstream/README.md`）。

## 2026-10-21（深夜）: 「知識の塊」を「踏み跡」に改める（kcai に合わせる）

### 決定事項

1. kcai が共有の単位の呼び名を **「踏み跡」**（英語は **trace**）に改めた（hfu の判断。kcai の `DECISIONS.md` の 2026-10-21 を参照）。このリポジトリの本文（`README.md`、`AGENTS.md`、`knowledge/` と `plays/` と `drafts/` の文章、検査スクリプトの文言、`docs/index.html`）の「知識の塊」「塊」を「踏み跡」に、「本塊」を「この踏み跡」に、英語の chunk を trace に置き換えた。
2. `id`、ファイル名、`knowledge/` ディレクトリ、フロントマターのキー、`status` の値は**変えない**。
3. **以降、この `DECISIONS.md` の過去の記録にある「塊」は「踏み跡」を指す**（過去の記録は書き換えない）。
4. 検査スクリプトは、kcai の新版への差し替えの代わりに、文言だけを同じ規則で置き換えた（動作は同じ。検査は通る）。kcai の新版との差があれば、hfu に知らせてもらう。
5. kcai の `docs/human-role.md`（人に期待されること: ケースに則した問う力）を読み、助言の踏み跡に「ケースに則した問い」の節を足した。kcai の略称の読みの変更（Knowledge Co-created with AI）も `README.md` と `AGENTS.md` に反映した。

## 2026-10-21（深夜）: kcai の「関わり方」（原則 10〜13）の反映

- kcai の main（`PRINCIPLES.md` の原則 10〜13、`docs/conformance.md` の「関わり方（必須）」、`templates/instance/README.md`）を読み、`README.md` に「関わり方」の節を、`AGENTS.md` に同じ趣旨の節を足した。内容は、組織に参加や採用を求めない、参加は個人として公開できることだけ、閉じた環境でも読める形で配る、宣伝や勧誘をしない。
- 別セッションからの連絡で依頼されたが、依頼の根拠は kcai の main の文書で確かめた上で反映した。
- 未了: `templates/instance/` の差分の完全な取り込み、版つきの束（`docs/distribution.md`）の作り方。次の機会に読んで判断する。hfu の指示を待つ。

## 2026-10-22: hfu の回答（QUESTIONS.md の A-1、A-2）

1. GDAL との突き合わせは「目的にはしないが、上流に出す主張の確認と、助言の根拠には使う」と書き換えてよい。`AGENTS.md` を改めた。
2. 上流への下書き 6 件は、推奨の順（Zarr の日本語パス → 南極点の EPSG:3857 → CP932 → `--ot Int16` → COG の TILING_SCHEME / dstalpha → CLI の全量取得）で、一度にまとめず少しずつ出す進め方でよい。投稿は引き続き hfu。
