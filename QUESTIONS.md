# hfu への質問（2026-10-22 時点。答えが出たら `DECISIONS.md` に追記し、ここから消す）

優先度順。**A は答えがないと先へ進めない／進めにくいもの**、B は進め方の確認、C は任意。

## A. 判断が要るもの

1. **`reviewed` にしてほしい踏み跡**。43 本すべて `draft`（AI は `reviewed` にできない）。先に見てほしい候補: `cloud-native-read-behavior-matrix`、`terrio-vs-gdal-spot-checks`、`vertical-datum-grids-and-geoid-in-japan`（訂正済み）、`jgd2011-plane-rectangular-transform`、`advice-for-dwg7`。**どれから、`reviewed_by` に誰の名前を入れるか。**
2. **kcai の `docs/distribution.md`（版つきの束）を、このリポジトリで実装するか。** するなら、束の形（zip / tar、含める範囲、版の付け方）の希望。しないなら、「関わり方 12」は今の GitHub 公開で足りるとみなしてよいか。

## B. 進め方の確認

3. **`scripts/` を kcai の新版に差し替えるか。** 今は文言だけ同じ規則で置換した（動作は同じ）。kcai の新版との差があれば、そちらを正とする。
4. **`templates/instance/` の差分の取り込み**: 私が読んで、差分をこのリポジトリに入れてよいか（`README`・`AGENTS`・`DECISIONS` の骨組みのみ。このリポジトリ固有の内容は残す）。
5. **STACIT と COPC の突き合わせ**: PDAL が環境にない。`pip` / `conda-forge` から PDAL や新しい GDAL（3.12）を入れる通信が許されるか不明。**入れてよいか。届かない場合は、保留のままにしてよいか。**（通信先の制限はすり抜けない方針のため、許可の一覧を hfu に伝える）
6. **新版の監視**: terrio は変化が速い（0.3.2 が最新、main は先行）。**新版が出たら `stale` の確かめ直しをする定期実行（スケジュール）を設定してよいか。** 頻度の希望（毎日 / 週 1）。

## C. 任意

7. **SNS 原稿の更新**: 用語を「踏み跡」にしたこと、GDAL との突き合わせで取り下げが出たこと、関わり方 13（宣伝をしない）との整合を、Facebook / LinkedIn の原稿に反映するか。
8. **公開ページ**（`docs/index.html`）に、踏み跡の一覧や助言へのリンクを足すか。今は terrio-js の試験ページのみ。
9. **大伴真吾さんへの言及**は、ご本人の了承を得てから、という扱いのままでよいか。
