# hfu への質問（2026-11-07 時点。答えが出たら `DECISIONS.md` に追記し、ここから消す）

優先度順。**A は答えがないと先へ進めない／進めにくいもの**、B は進め方の確認、C は任意。

## A. 判断が要るもの

1. **`reviewed` にしてほしい踏み跡**。43 本すべて `draft`（AI は `reviewed` にできない）。先に見てほしい候補: `cloud-native-read-behavior-matrix`、`terrio-vs-gdal-spot-checks`、`vertical-datum-grids-and-geoid-in-japan`（訂正済み）、`jgd2011-plane-rectangular-transform`、`advice-for-dwg7`。**どれから、`reviewed_by` に誰の名前を入れるか。**
2. **kcai の `docs/distribution.md`（版つきの束）を、このリポジトリで実装するか。** するなら、束の形（zip / tar、含める範囲、版の付け方）の希望。しないなら、「関わり方 12」は今の GitHub 公開で足りるとみなしてよいか。

## B. 進め方の確認

## D. 定期実行の修正（要対応）

8. **新版確認の定期実行（毎日 7:23 JST）は、実行のたびに push が拒否されています**。そのセッションの許可リポジトリに `dwg7/kcai-terrio` が入っていないためです（作成時の警告どおり）。AI の側から直す手段がありません。**claude.ai の定期実行の設定で、`dwg7/kcai-terrio` をソースに追加してください**。直るまでは、私が起きたときに手元で確かめ直します。直すまで定期実行を止めますか（`enabled=false`）、そのままにしますか。

## D2. kcaim 化の判断（`kcaim/ASSESSMENT.md`）

10. **`kcaim/terrio.md` を、木と並ぶ「蒸留した携帯版」（案 C）として続けてよいか。** 木をやめて 1 ファイルだけにする案 D は、盲検の結果を見てから判断したい。
11. **盲検の実行**は、別のエージェントに、`/acceptance-tests/` と結果を除いたコピーを渡して質問する形になる。私は自分では盲検にならないので、**hfu が別の AI（Copilot、Gemini など）で試してくれますか。**試す手順（一行プロンプトと 14 の質問）は `kcaim/ASSESSMENT.md` §5。
12. 置き場: `kcaim/terrio.md` は、今は `dwg7/kcai-terrio` の中にある。`dwg7/kcaim` の `examples/` に置く方がよければ、hfu が移す（私は `dwg7/kcaim` に書けない）。

## D3. 名前の変更（kcaim → miso）への対応

13. `dwg7/kcaim` は、呼び名を **miso**（旧称 kcaim）に改める手順（`MIGRATION.md`、草稿）を進めている。移行表は「`kcai-*` のリポジトリは変えない」とし、**`kcai-terrio` の README には kcaim への言及がない**と記すが、この木には 11-05 から次がある: `kcaim/terrio.md`、`kcaim/ASSESSMENT.md`、`scripts/check_kcaim.py`、CI の検査の 1 段、`DECISIONS.md` と `QUESTIONS.md` の言及。**移行表に `kcai-terrio` の行を足す必要があるかもしれません**（私は `dwg7/kcaim` に書けません）。
14. 切り替え後に、`kcaim/` を **`miso/`** に、`check_kcaim.py` を `check_miso.py` に改めますか。**今は旧称のまま**にし、決まったら私が直します（移行期間は両方の名前を受理する方針に合わせ、`kcaim/terrio.md` から `miso/terrio.md` へ移すだけです）。

## E. 新しい情報（回答不要）

9. 上流への下書きは有効な 3 件（Zarr の日本語パス、COG の `TILING_SCHEME` と `--dstalpha`、CLI の FlatGeobuf の全量取得）。取り下げた 3 件（南極点、docs/rust.md、CP932）は、投稿前に別の人が直した。**投稿は急がなくてよいが、遅れると追い越される**ことは分かった。最初に出すなら Zarr の日本語パス（小さく、再現が確実で、まだ直っていない）。
