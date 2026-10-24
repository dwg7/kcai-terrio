# hfu への質問（2026-10-24 時点。答えが出たら `DECISIONS.md` に追記し、ここから消す）

優先度順。**A は答えがないと先へ進めない／進めにくいもの**、B は進め方の確認、C は任意。

## A. 判断が要るもの

1. **`reviewed` にしてほしい踏み跡**。43 本すべて `draft`（AI は `reviewed` にできない）。先に見てほしい候補: `cloud-native-read-behavior-matrix`、`terrio-vs-gdal-spot-checks`、`vertical-datum-grids-and-geoid-in-japan`（訂正済み）、`jgd2011-plane-rectangular-transform`、`advice-for-dwg7`。**どれから、`reviewed_by` に誰の名前を入れるか。**
2. **kcai の `docs/distribution.md`（版つきの束）を、このリポジトリで実装するか。** するなら、束の形（zip / tar、含める範囲、版の付け方）の希望。しないなら、「関わり方 12」は今の GitHub 公開で足りるとみなしてよいか。

## B. 進め方の確認

## D. 新しい情報（回答不要。投稿の順の参考）

8. 上流への下書きは有効な 6 件。**最初に出すなら、`2026-10-24-rust-docs-dependency-version-does-not-resolve.md`（docs/rust.md の依存の書き方。小さく、再現が確実）**が向く。そのあと Zarr の日本語パス、南極点の EPSG:3857、CP932 の順（`drafts/upstream/README.md`）。いずれも 0.5.0 で再現を確認済み。
