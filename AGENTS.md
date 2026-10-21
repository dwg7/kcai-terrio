# AGENTS

この文書は、`dwg7/kcai-terrio` で作業するすべての AI のための案内の本体です。特定の AI 製品に依存しない書き方にします。

## このリポジトリは何か

二つの目的を、一つのリポジトリで同時に果たします。

1. terrio で、クラウドネイティブなデータを、クラウドネイティブに触って遊びきる。
2. その遊びから得た知識を、kcai の方式で Markdown の塊として残す。

[dwg7/kcai](https://github.com/dwg7/kcai)（知識共創 AI）の最初期のインスタンスの一つで、コンセプトを小さく実地で試す場です。原則・形式は kcai に従います。食い違いを見つけたら `DECISIONS.md` に書き、管理責任者（hfu）に知らせます。

terrio は Qiusheng Wu さん（opengeos）による、GDAL を使わない Pure Rust の地理空間データ入出力ライブラリ（MIT）。CLI（`terrio`）、Python（`pip install terrio`）、JavaScript/WebAssembly（npm `terrio-js`）、Rust、MCP サーバー（`terrio mcp`）から使えます。2026-10-14 に始まったばかりで変化が速く、知識がすぐ古くなります。

- リポジトリ: https://github.com/opengeos/terrio
- ドキュメント: https://terrio.opengeos.org （`opengeos`。s のない opengeo.org は別ドメイン）

## 遊び方の方針

- **遊びきる**: GDAL との突き合わせは目的にしない。terrio を広く深く使う（各コマンド、Python API、WebAssembly 版、MCP）。
- **発見を記録する**: 思ったとおり動かない、ドキュメントと違う、驚いた、はすべて「発見」。発見がこのリポジトリのいちばんの成果。
- **最新に追随し、版を必ず記録する**: `pip install --upgrade terrio` で常に最新を使う。遊ぶたびに版（分かればコミット）を記録する。版が上がったら変更履歴を読み、影響しそうな塊を確かめ直す。確かめ直せていない塊は `status: stale` にする。
- **クラウドネイティブ**: 主な対象は範囲読み込み（HTTP Range）できる形式（COG、PMTiles、GeoParquet、FlatGeobuf、STAC）。**ファイルを丸ごとダウンロードしない**。どこまで範囲読み込みで扱えるかを試すことが遊びの中心。
- **日本ローカル**: JGD2011（EPSG:6668）、平面直角座標系（EPSG:6669〜6687）、日本の COG/PMTiles、日本語属性の文字化けを意識的に試す。

## 知識の塊

- `knowledge/` に 1 主題 1 ファイル。一覧は `knowledge/README.md`。
- 形式は kcai の形式に terrio 用の項目を足したもの:

```markdown
---
id: <英小文字とハイフン。一度付けたら変えない。ファイル名と一致>
title: <日本語の題名>
status: draft | reviewed | stable | stale | deprecated
terrio_version: <確かめたときの terrio の版>
terrio_commit: <分かれば>
interface: cli | python | wasm | mcp | rust
environment: <確かめた環境>
verified_on: <YYYY-MM-DD>
verified_how: played | read-source | read-docs
sources:
  - <ドキュメントやソースの該当箇所、plays/ の記録>
authors:
  - <書いた人。AI 支援の有無を必ず書く>
reviewed_by: []
updated: <YYYY-MM-DD>
related: []
---

## 要点
## やり方
## 確かめたこと（何をして、何が起きたか）
## 気をつけること
## 出典
```

- `stale` は「新しい版でまだ確かめ直していない」印。
- **確かめた度合いを正直に書く**。`played`（実際に動かした）と `read-source` / `read-docs`（読んだだけ）を区別する。
- AI は `reviewed` 以上にしない。人が確認して `reviewed_by` に記録する。
- 検査: `python3 scripts/validate_knowledge.py knowledge`（CI でも実行）。

## 遊びの記録と下書き

- `plays/YYYY-MM-DD-<題>.md`: 日時、terrio の版、環境、打ったコマンド、結果の要約、発見。大きな出力は要約する。
- `drafts/upstream/`: terrio への issue の下書き。再現手順と版を明記し、敬意をもって、やさしい英語で書く。**投稿は hfu が確認して hfu が行う。**
  `python3 scripts/upstream_index.py > drafts/upstream/README.md` で、状態の一覧と投稿用リンクを作る。同じ型の弱点は、まとめて探してから報告する。未検証の主張は、投稿前に外す。

## 生きた塊

- `knowledge/advice-for-dwg7.md`（dwg7 に対する助言）は、**作業が進むごとに更新する**。更新履歴に 1 行足し、助言の表を見直し、`updated` を直す。
- 上流への下書きは、書く前に、可能なら **GDAL（または対応する別実装）と突き合わせる**。版を明記し、確かめていない主張は外す。

## ブラウザ版

`docs/` に terrio-js を使う小さなページを置き、GitHub Pages で公開する。ビルド工程は持たず、CDN から版を固定して読み込む。何がブラウザで動き、何が動かないかも塊にする。

## 守ること

- 外部（opengeos/terrio など）への投稿・コメント・PR はしない。発信は hfu が行う。
- 認証情報を扱わない。公開データだけを使う。
- 大きなデータをリポジトリに入れない（`.gitignore` 参照）。ディスク割り当てに注意し、一時ファイルはこまめに消す。一時ファイルはリポジトリ外（スクラッチ）に置く。
- MCP で書き込むときは、出力先を一時的な場所に限る。
- terrio はこのリポジトリの遊びの範囲でだけ使う。
- 通信先の制限を、すり抜けない。届かない配信先は hfu に一覧で伝える。
- 判断が分かれることは推測で埋めず、hfu に質問する。決定は `DECISIONS.md` に追記する（消さない）。
- コミットは `main` に対して、こまめに行い、積極的に push してよい（hfu の指示。`DECISIONS.md`）。

## 参照先

- kcai: `PRINCIPLES.md`、`docs/knowledge-format.md`、`docs/asking.md`、`docs/unsaid.md`
- 道具: `python3 scripts/build_index.py --stats` ほか（kcai のコピー）
