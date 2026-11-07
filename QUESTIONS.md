# hfu への質問（2026-11-07 時点。答えが出たら `DECISIONS.md` に追記し、ここから消す）

優先度順。**A は答えがないと先へ進めない／進めにくいもの**、B は進め方の確認、C は任意。

## A. 判断が要るもの

1. **`reviewed` にしてほしい踏み跡**。43 本すべて `draft`（AI は `reviewed` にできない）。先に見てほしい候補: `cloud-native-read-behavior-matrix`、`terrio-vs-gdal-spot-checks`、`vertical-datum-grids-and-geoid-in-japan`（訂正済み）、`jgd2011-plane-rectangular-transform`、`advice-for-dwg7`。**どれから、`reviewed_by` に誰の名前を入れるか。**
2. **kcai の `docs/distribution.md`（版つきの束）を、このリポジトリで実装するか。** するなら、束の形（zip / tar、含める範囲、版の付け方）の希望。しないなら、「関わり方 12」は今の GitHub 公開で足りるとみなしてよいか。

## B. 進め方の確認

## D. 定期実行の修正（要対応）

8. **新版確認の定期実行（毎日 7:23 JST）は、実行のたびに push が拒否されています**。そのセッションの許可リポジトリに `dwg7/kcai-terrio` が入っていないためです（作成時の警告どおり）。AI の側から直す手段がありません。**claude.ai の定期実行の設定で、`dwg7/kcai-terrio` をソースに追加してください**。直るまでは、私が起きたときに手元で確かめ直します。直すまで定期実行を止めますか（`enabled=false`）、そのままにしますか。

## D2. miso/terrio.md が正本になった（2026-11-07）

10. **盲検の実行**: 別の AI（Copilot、Gemini など）に、`miso/terrio.md` から受け入れテストの節（`# /acceptance-tests/…` の見出し群）と結果を除いたコピーを渡し、一行プロンプト（冒頭の `agent-contract` にある）で質問してもらえますか。質問は `miso/terrio.md` の受け入れテスト 19 本。私は自分では盲検になれません。
11. 移植は蒸留（約 33 万字 → 約 5 万字）なので、**落ちた事実が無いか**の確認が要ります。気づいた落ちがあれば教えてください（凍結した `knowledge/` から足します）。
12. `dwg7/miso` の `MIGRATION.md` の移行表に `kcai-terrio` の行を足してください（私は書けません）。内容: `kcai-terrio` は名前を変えない（`kcai-*`）。`miso/terrio.md`（新）、`scripts/check_miso.py`（新）、凍結した `knowledge/`。

## E. 新しい情報（回答不要）

9. 上流への下書きは有効な 3 件（Zarr の日本語パス、COG の `TILING_SCHEME` と `--dstalpha`、CLI の FlatGeobuf の全量取得）。取り下げた 3 件（南極点、docs/rust.md、CP932）は、投稿前に別の人が直した。**投稿は急がなくてよいが、遅れると追い越される**ことは分かった。最初に出すなら Zarr の日本語パス（小さく、再現が確実で、まだ直っていない）。
