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
