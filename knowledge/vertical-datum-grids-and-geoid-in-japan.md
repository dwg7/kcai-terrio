---
id: vertical-datum-grids-and-geoid-in-japan
title: 格子とジオイド：日本の高さの変換は「3 次元の CRS」から（GDAL と突き合わせて訂正した）
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、Node 22、GDAL 3.8.4 / PROJ 9.4 を apt で導入）
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - plays/2026-10-21-japan-edge-cases-and-survey.md（3。当初の誤った結論を含む）、plays/2026-10-21-gdal-comparison.md（訂正）
  - terrio docs/crs.md（格子の探し方、高さと鉛直測地系）、docs/why-terrio.md
  - https://cdn.proj.org/files.geojson （jp_gsi_gsigeo2011.tif、jp_gsi_jpgeo2024.tif）
  - GDAL 3.8.4 の gdaltransform、PROJ の projinfo
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
related: [jgd2011-plane-rectangular-transform, terrio-crs-forms-projections-grids-and-epochs, terrio-vs-gdal-spot-checks, terrio-conformance-and-testing-against-gdal, hfu-dwg7-workflow-substitution-survey]
hazard: 2d-crs-drops-height-semantics
freshness: high
finding:
  - japan-geoid-needs-3d-source-crs
  - terrio-prefers-jpgeo2024-gdal-3-8-uses-gsigeo2011
---

## 要点

**【訂正】** 当初「日本のジオイドが terrio で適用されない」と書いたが、**誤りだった**。`EPSG:6668`（JGD2011 の **2 次元**）を使ったのが原因で、GDAL/PROJ も同じく高さを変えない。**3 次元の `EPSG:6667` から `EPSG:6697`（標高つき）へ変換すれば、terrio は日本のジオイドを適用する**。terrio は新しいモデル **JPGEO2024** を優先し、GDAL 3.8.4（PROJ 9.4）は **GSIGEO2011** を使うので、同じ点で約 0.1 m 違う。**同じ格子（GSIGEO2011）を使わせると、terrio と GDAL は小数 11 桁まで一致した**。

## やり方

```sh
# 楕円体高 86.7 m（JGD2011 の 3 次元 = EPSG:6667）→ 標高（EPSG:6697）
echo "139.767125 35.681236 86.7" | TERRIO_NETWORK=ON terrio crs EPSG:6667 --to EPSG:6697   # → 49.9386（JPGEO2024）
echo "139.767125 35.681236 86.7" | PROJ_NETWORK=ON gdaltransform -s_srs EPSG:6667 -t_srs EPSG:6697   # → 50.0375（GSIGEO2011）
# 2 次元の EPSG:6668 では、どちらも高さは変わらない（86.7 → 86.7）
```

JS では `registerGrid('jp_gsi_gsigeo2011.tif', バイト)` で格子を渡してから、`transformPoints([139.767125],[35.681236],'EPSG:6667','EPSG:6697',[86.7])`。

## 確かめたこと（何をして、何が起きたか）

| 変換（点 139.767125, 35.681236、東京駅付近） | terrio | GDAL 3.8.4 / PROJ 9.4 |
|---|---|---|
| `EPSG:6668`（2D）→ `EPSG:6697`、高さ 86.7 | 86.7（不変） | 86.7（不変）。`projinfo` の操作は `+proj=noop` |
| `EPSG:6697` → `EPSG:6668`、高さ 50 | 50（不変） | 50（不変） |
| 明示の PROJ 文字列 `+geoidgrids=jp_gsi_gsigeo2011.tif`（両方向） | 不変 | **不変**（同じ） |
| **`EPSG:6667`（3D）→ `EPSG:6697`、高さ 86.7** | **49.9386**（CLI は `jp_gsi_jpgeo2024.tif` を自動取得）。ネットワークなしでも、キャッシュにあれば同じ | **50.0375**（GSIGEO2011） |
| 同上、逆（50.0375 → 3D） | 86.7989 | 86.7 |
| JS: `registerGrid` で GSIGEO2011 だけ登録 | **50.03747748404898** | 50.037477484049（**一致**） |
| JS: さらに JPGEO2024 を登録 | 49.93855654598838（新しいほうを優先） | — |
| 札幌（141.3545, 43.0621）、高さ 100 | 67.806 | 68.049 |
| 大阪（135.5023, 34.6937）、高さ 100 | 62.369 | 62.513 |
| **那覇（127.6809, 26.2124）、高さ 100** | 69.153 | **100（不変）** |

- EGM96（`EPSG:4979 → EPSG:4326+5773`、高さ 50）は、terrio の `TERRIO_NETWORK=ON` で 13.5559、GDAL でも 13.5558849…（**一致**）。
- **差の理由（推測を含む）**: terrio の EPSG の表は新しく、JGD2011 の鉛直変換に JPGEO2024 を持つ。Ubuntu の GDAL 3.8.4 / PROJ 9.4 は古く、GSIGEO2011 を使う。terrio の基準は GDAL 3.12 / PROJ 9.8.1 なので、**同じ版の GDAL 3.12 との比較は、この環境ではできていない**。那覇で GDAL が不変なのは、古い版の変換の適用範囲に沖縄が入っていないためかもしれない（未確認）。
- PROJ の CDN の `jp_` の格子は、`jp_gsi_gsigeo2011.tif`（428,043 バイト）と `jp_gsi_jpgeo2024.tif`（7,379,285 バイト）。日本の**水平方向**の格子（旧日本測地系、JGD2000→JGD2011）は CDN にない。
- `docs/why-terrio.md`（格子は適用しない）と `docs/crs.md`（適用する）の食い違いは、実測で後者が正しい。
- **conformance の `scripts/proj_grids.txt`（128 行）に日本の格子（`jp_`）は 0 件**。terrio の試験では、日本の格子は検証されていない（GDAL とは別に、上の突き合わせで 1 点ずつ確かめた）。

## 気をつけること

- **高さを変換するなら、入力の CRS は 3 次元（`EPSG:6667`、`EPSG:4979`）か複合 CRS にする**。2 次元の `EPSG:6668` に高さを渡すと、**エラーも警告もなく高さが変わらない**（GDAL も同じ）。dwg7/plateau-mago-implicit のような標高の補正では、この点が決定的。
- **どのジオイドモデルが使われるか**は、版による: terrio（新しい EPSG）は JPGEO2024、GDAL 3.8.4 は GSIGEO2011。成果物に使うなら、モデルを明示する（`registerGrid` や `TERRIO_GRID_DIR` に使う格子だけを置く）。
- 測量成果には使わない（GDAL との比較は、GDAL 3.8.4 の少数の点だけ）。
- **この踏み跡の以前の版は、誤った結論を書いていた**（「日本のジオイドは適用されない」）。下書き（`drafts/upstream/2026-10-21-jgd2011-geoid-heights-unchanged.md`）は、投稿前に GDAL で確かめて、**取り下げた**。

## 出典

- plays/2026-10-21-gdal-comparison.md
- https://terrio.opengeos.org/crs/ 、https://cdn.proj.org/
