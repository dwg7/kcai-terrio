---
id: vertical-datum-grids-and-geoid-in-japan
title: 格子とジオイド：EGM96 は適用されるが、日本のジオイドは適用されなかった
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、PyPI の wheel）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
interface: cli
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - plays/2026-10-21-japan-edge-cases-and-survey.md（3）
  - terrio docs/crs.md（格子の探し方、高さと鉛直測地系）
  - terrio docs/why-terrio.md（「格子はまだ適用しない」の記述）
  - https://cdn.proj.org/files.geojson （jp_gsi_gsigeo2011.tif、jp_gsi_jpgeo2024.tif）
related: [jgd2011-plane-rectangular-transform, terrio-scope-included-and-excluded, hfu-dwg7-workflow-substitution-survey]
hazard: height-silently-unchanged
freshness: high
finding:
  - japan-geoid-grids-not-applied
  - docs-disagree-on-grid-support
---

## 要点

terrio は PROJ の格子を探して適用できる（`TERRIO_NETWORK=ON` で PROJ の CDN から自動取得）。EGM96 の高さ変換は実際に動いた。**しかし、日本のジオイド（GSIGEO2011、JPGEO2024）は、試した 6 通りの書き方のどれでも適用されず、高さがエラーなしで変わらなかった。** 日本の水平方向の格子（旧日本測地系や JGD2000 → JGD2011）は、そもそも PROJ の CDN にない。

## やり方

```sh
# 標準入力で x y z（経度 緯度 高さ）
echo "139.767125 35.681236 50" | TERRIO_NETWORK=ON terrio crs EPSG:4979 --to "EPSG:4326+5773"   # EGM96: 50 → 13.5559
# 日本のジオイド（適用されず 50 → 50）
echo "139.767125 35.681236 50" | TERRIO_NETWORK=ON terrio crs EPSG:6697 --to EPSG:6668
```

格子は `~/.cache/terrio/grids`（`TERRIO_GRID_CACHE`）に入る。探す場所の順: メモリに登録 → `TERRIO_GRID_DIR`、`PROJ_DATA`、`PROJ_LIB`、`~/.local/share/proj`、キャッシュ → ネットワーク（`TERRIO_NETWORK=ON`、CDN は `TERRIO_CDN_ENDPOINT`）。

## 確かめたこと（何をして、何が起きたか）

- ネットワーク OFF（既定）: EGM96 の変換で高さ 50 → 50（変わらない）。
- `TERRIO_NETWORK=ON`: `us_nga_egm96_15.tif`（約 2.6 MB）を取得して 50 → 13.5559。
- 日本のジオイド（`TERRIO_NETWORK=ON`）: `EPSG:6697 → 6668`、`6668 → 6697`、`6668 → 6668+6695`、`+geoidgrids=jp_gsi_gsigeo2011.tif` の PROJ 文字列（両方向）、`jp_gsi_jpgeo2024.tif` のどれも高さ不変で、格子の取得も起きなかった。
- **WebAssembly 版（terrio-js 0.3.2、Node）でも同じ**: `registerGrid('jp_gsi_gsigeo2011.tif', バイト)` で格子を直接登録して `EPSG:6668 → EPSG:6697`（高さ 86.7）を変換しても、高さは 86.7 のまま。同じ方法の EGM96（`us_nga_egm96_15.tif`）は 100 → 125.05 に変わる。**格子の探索ではなく、日本の変換の選択に原因がある可能性が高い**（未確定）。
- 格子ファイル自体は `terrio info` で読める（1201×1800、EPSG:6668、Float32、東経 119.99〜150.01、北緯 20.01〜50.01）。
- PROJ の CDN の `jp_` は `jp_gsi_gsigeo2011.tif`、`jp_gsi_jpgeo2024.tif`、README だけ。
- ドキュメントの食い違い: `why-terrio.md` は「格子はまだ適用しない」、`crs.md` は「格子を探して適用する」。後者が実態に近い。

## 気をつけること

- **高さが黙って変わらない**。ドキュメントにも「適用できる変換がなければ高さは保たれる」とある（PROJ の ballpark と同じ）。日本の標高と楕円体高の変換に terrio を使わない。
- 原因は**未確定**（terrio が日本の変換を EPSG の表から選ばないのか、PROJ 文字列の扱いか）。この塊は事実の記録で、原因の推測を含まない。
- 回避策の候補: 格子を `terrio` で開いて自分で内挿する（Python の `open_raster` と NumPy）。試していない。
- `TERRIO_NETWORK=ON` は実行時にネットワークへ出る。許可リストの環境では `cdn.proj.org` が必要（2026-10-21 は届いた）。

## 出典

- plays/2026-10-21-japan-edge-cases-and-survey.md
- https://terrio.opengeos.org/crs/ 、https://terrio.opengeos.org/why-terrio/
- https://cdn.proj.org/
