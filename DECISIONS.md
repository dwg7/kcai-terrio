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
