---
id: terrio-evolution-0-3-2-to-0-4-2
title: terrio の進化の方向（0.3.2 から 0.4.2、そして main）
status: draft
terrio_version: 0.4.2
terrio_commit: 17ca35a
interface: cli
environment: Claude Code クラウドセッション。opengeos/terrio の git log（v0.3.2..v0.4.2 の 58 コミット、v0.4.2..main の 28 コミット）、ROADMAP.md の差分、0.4.2 の wheel で再確認した挙動
verified_on: 2026-10-24
verified_how: read-source
sources:
  - https://github.com/opengeos/terrio （git log v0.3.2..v0.4.2、v0.4.2..17ca35a、ROADMAP.md の v0.3.2 との差分）
  - plays/2026-10-24-0-4-2-recheck.md
  - knowledge/terrio-source-scale-and-origins.md
authors:
  - hfu の指示のもと、AI（Claude）が git log と差分から読み取って記述。AI 支援あり。方向の読みは推測を含む
reviewed_by: []
updated: 2026-10-24
related: [terrio-source-scale-and-origins, terrio-release-vs-main-drift, terrio-roadmap-and-open-items, terrio-possibilities-and-risks, hfu-dwg7-workflow-substitution-survey, advice-for-dwg7]
freshness: high
---

## 要点

0.3.2（2026-10-20）から 9 日足らずで、**0.4.0・0.4.1・0.4.2 が出て（2026-10-21〜22）、main はさらに 28 コミット進んだ**。0.3.2 から main までの差は、`crates/terrio/src` で **+1.9 万行**、全体で **+6.6 万行**。方向は 5 つに読める。

1. **GDAL / PROJ / PDAL / rasterio「と同じ答え」を、機能ごとに積み上げる**。ROADMAP の完了項目が「GDAL と同一」「PROJ の選び方」「GDAL の STACIT / STACTA と同じ」で書かれる。座標系は、PROJ の変換の鎖（#163、#170、#171、#222）、回転極・静止衛星・世界地図の図法（#148〜#150、#152）、垂直 CRS（#203）、エポック間の点の運動（#207）と、PROJ の細部を移植している。
2. **範囲を「読み込み・変換」から「解析」へ広げる**。等高線、ゾーン統計、独立した SQL、重心・分割・頂点抽出・有効域の外形・点のサンプリング（#228、#230）、PDAL の点群フィルタ（dbscan、lof、dem ほか。#210）。次の予定は buffer、overlay、dissolve、**幾何の検査・修復**（#211、#227）。
3. **クラウドネイティブの読みを、形式ごとに「その場」にしていく**。CDN の座標系格子の範囲読み込み（#202）、Zarr の遠隔グループの一覧と 4 次元以上（#198、#199）、STAC の POST・ページ送り・Planetary Computer の署名（#197）、STACTA（#218）。**ただし FlatGeobuf と GeoParquet の CLI は、0.4.2 でも全量取得のまま**（JS 版は範囲読み）。
4. **メモリを抑えた流し読み・書き**。COG・JP2→GeoTIFF・GeoPackage / FlatGeobuf・Shapefile を、帯や塊ごとに読み書き（#114、#176、#177、#191）、OSM をメモリマップに（#109、#190）、大きな解放をシステムに返す（#179）。**WebAssembly は小型化、スレッド、4 GB 超**（#220、#224、#229）。
5. **配り方と窓口を増やす**。MCP サーバー（#110）、`terrio.rio` の CLI（#204）、xarray・rioxarray 互換（#206）、AUR と Fedora COPR（#192）、sdist へのライセンス同梱（#172）、READMEとドキュメントの AI 開示・謝辞（#142）。

加えて、不具合の直しは速い（#159 → #161 は翌日）。

## 0.4.2 での再確認の結果（この遊びで見つけたもの）

| 項目 | 0.4.2 | 備考 |
|---|---|---|
| GeoJSON / CSV の日本語長文字列の panic（#159） | **直った** | 0.4.0 から。全書き出し形式で通った |
| Zarr の日本語の相対パスの panic | **残る** | `info 日本語/a.zarr`。main のソースにも残る |
| CP932 の Shapefile 属性 | 文字化けのまま | `.cpg` を指定しても変わらない |
| 南極点（180,−90）→ EPSG:3857 | 失敗のまま | |
| COG `TILING_SCHEME`、`warp --dstalpha` | 黙殺 / なしのまま | |
| COG の窓・概観、PMTiles | 範囲読み込み（6.19 / 2.56 MiB、PMTiles info 1.48 MiB） | 0.3.2 と同等 |
| FlatGeobuf の CLI | 全量取得のまま | |
| 日本の座標変換（6668→6677、6667→6697 のジオイド） | 同じ値 | |

## 読み取れること（推測を含む）

- **方向は「GDAL + PROJ + PDAL + rasterio + 一部の PostGIS / DuckDB 相当」を、一つの Pure Rust の道具に畳む**こと。幅は急速に広がるが、各機能の「現場データでの深さ」は、報告が入った所から直る（#159）。
- **日本ローカル（CP932、日本語パス、平面直角の運用）は、ROADMAP に出てこない**。ROADMAP に「Shift_JIS」「encoding」「tippecanoe」「タイル生成」「Japan」の語は無い（grep で確認）。これらは、上流に報告しないと、後回しになる可能性が高い。
- **dwg7 の代替表で「できなさそう」だった所のうち**、幾何の検査・修復（SQLite 方言の `ST_*`）は、#211 / #227 で**将来できるかもしれない**項目に上がった。タイル生成（tippecanoe）は触れられていない。
- **速さの代償**: 9 日で +6.6 万行。挙動が版ごとに動く。踏み跡は版ごとに `stale` にして確かめ直す運用が要る（この遊びの方針の通り）。

## 気をつけること

- 傾向は **git log と ROADMAP の差分から読んだ**もので、作者の意図は確かめていない。
- 再確認したのは**表の項目だけ**。他の踏み跡（34 本）は 0.3.2 のままで `stale`。
- main（17ca35a）の挙動は、ソースを読んだもので、すべては動かしていない。

## 出典

- https://github.com/opengeos/terrio の `git log`、`ROADMAP.md`（v0.3.2 と main の差分）
- `plays/2026-10-24-0-4-2-recheck.md`
