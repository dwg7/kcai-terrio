# hfu への質問（2026-11-04 時点。答えが出たら `DECISIONS.md` に追記し、ここから消す）

優先度順。**A は答えがないと先へ進めない／進めにくいもの**、B は進め方の確認、C は任意。

## A. 判断が要るもの

1. **`reviewed` にしてほしい踏み跡**。43 本すべて `draft`（AI は `reviewed` にできない）。先に見てほしい候補: `cloud-native-read-behavior-matrix`、`terrio-vs-gdal-spot-checks`、`vertical-datum-grids-and-geoid-in-japan`（訂正済み）、`jgd2011-plane-rectangular-transform`、`advice-for-dwg7`。**どれから、`reviewed_by` に誰の名前を入れるか。**
2. **kcai の `docs/distribution.md`（版つきの束）を、このリポジトリで実装するか。** するなら、束の形（zip / tar、含める範囲、版の付け方）の希望。しないなら、「関わり方 12」は今の GitHub 公開で足りるとみなしてよいか。

## B. 進め方の確認

## D. 定期実行の修正（要対応）

8. **新版確認の定期実行（毎日 7:23 JST）は、実行のたびに push が拒否されています**。そのセッションの許可リポジトリに `dwg7/kcai-terrio` が入っていないためです（作成時の警告どおり）。AI の側から直す手段がありません。**claude.ai の定期実行の設定で、`dwg7/kcai-terrio` をソースに追加してください**。直るまでは、私が起きたときに手元で確かめ直します。直すまで定期実行を止めますか（`enabled=false`）、そのままにしますか。

## E. 新しい情報（回答不要）

9. 上流への下書きは有効な 3 件（Zarr の日本語パス、COG の `TILING_SCHEME` と `--dstalpha`、CLI の FlatGeobuf の全量取得）。取り下げた 3 件（南極点、docs/rust.md、CP932）は、投稿前に別の人が直した。**投稿は急がなくてよいが、遅れると追い越される**ことは分かった。最初に出すなら Zarr の日本語パス（小さく、再現が確実で、まだ直っていない）。
