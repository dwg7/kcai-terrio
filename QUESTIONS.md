# hfu への質問（2026-11-27 時点。答えが出たら `DECISIONS.md` に追記し、ここから消す）

優先度順。**A は答えがないと先へ進めない／進めにくいもの**、B は要対応、C は参考。

## A. 判断が要るもの

1. **`reviewed` にしてほしい踏み跡**（凍結した `knowledge/` の 46 本、または `miso/terrio.md` の特定のオブジェクト）。AI は `reviewed` にできない。先に見てほしい候補: `cloud-native-read-behavior-matrix`、`terrio-vs-gdal-spot-checks`、`vertical-datum-grids-and-geoid-in-japan`、`jgd2011-plane-rectangular-transform`、`miso/terrio.md` の `/decision-support/advice-for-dwg7`。どれから、`reviewed_by` に誰の名前を入れるか。
2. **版つきの束（`dwg7/miso` の `docs/distribution.md`）**: `miso/terrio.md` 自体が 1 ファイルの携帯版なので、「束」はこのファイルで足りるとみなしてよいか。足りないなら、束の形の希望。
3. **盲検の実行**: 別の AI（Copilot、Gemini など）に、`miso/terrio.md` から受け入れテストの節（`# /acceptance-tests/…` の見出し群）と結果を除いたコピーを渡し、冒頭の `agent-contract` の一行プロンプトで質問してもらえますか。質問は受け入れテスト 26 本。私は自分では盲検になれません。

## B. 要対応

4. **新版確認の定期実行（毎日 7:23 JST）は、リポジトリがそのセッションのソースに入っておらず、push が拒否されます**。AI の側から直せません。claude.ai の定期実行の設定で、`dwg7/kcai-terrio` をソースに追加してください（直るまでは、私が起きたときに手元で確かめ直します）。止めてもよいか。
5. **`dwg7/miso` の `MIGRATION.md` の移行表に `kcai-terrio` の行を足してください**（私は書けません）。内容: 名前は変えない（`kcai-*`）。`miso/terrio.md`（正本）、`scripts/check_miso.py`、凍結した `knowledge/`。
6. **上流への下書き（`drafts/upstream/README.md`）の投稿**は hfu。いま有効な 4 件のうち、**最優先は terrio-js 0.9.0・0.10.0 の退行**（30 GB のラスタ PMTiles の `openUrl` が panic。0.8.0 は開く。再現手順つき）。次に、Zarr の日本語の相対パスの panic、COG の `TILING_SCHEME` と `--dstalpha`、FlatGeobuf の CLI の全量取得（GeoParquet の部分は 0.9.0 で解決したので、FlatGeobuf だけに絞る）。投稿が遅れると別の人に先に直される（これまで 3 件が先に直った）。

## C. 参考（回答不要）

7. 移植（約 33 万字 → 約 8 万字の `miso/terrio.md`）で**落ちた事実が無いか**、気づいたら教えてください（凍結した `knowledge/` から足します）。
8. リモートのブランチの削除は済み（`main` のみ）。作業は `main` に一本化している。
