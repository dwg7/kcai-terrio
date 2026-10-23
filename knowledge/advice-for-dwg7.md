---
id: advice-for-dwg7
title: dwg7 に対する助言（作業が進むごとに更新する生きた踏み跡）
status: draft
terrio_version: 0.3.2
terrio_commit: 6779102
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64）。terrio 配布版 0.3.2 と main 6779102。比較に GDAL 3.8.4 / PROJ 9.4
verified_on: 2026-10-21
verified_how: played
sources:
  - knowledge/hfu-dwg7-workflow-substitution-survey.md
  - knowledge/terrio-vs-gdal-spot-checks.md
  - knowledge/cloud-native-read-behavior-matrix.md
  - plays/2026-10-21-gdal-comparison.md
  - drafts/upstream/README.md
authors:
  - AI（Claude）が書いた助言。hfu / dwg7 の指示のもと。AI 支援あり。助言は、証拠となる踏み跡への参照つきで、判断は dwg7 が行う
reviewed_by: []
updated: 2026-10-21
related: [terrio-source-scale-and-origins, terrio-rust-library-and-features, terrio-xarray-integration, hfu-dwg7-workflow-substitution-survey, terrio-possibilities-and-risks, terrio-vs-gdal-spot-checks, cloud-native-read-behavior-matrix, terrio-release-vs-main-drift, upstream-issue-feedback-loop]
freshness: high
---

## 要点

**この踏み跡は生きている。** 作業が進むごとに「更新履歴」に 1 行足し、助言を見直す（`AGENTS.md` の規則）。助言は証拠つきで、確かめた度合いを付ける。判断は dwg7 が行う。

いまの結論（2026-10-21）: terrio は、dwg7 の**前処理の一部（ラスタの再投影・圧縮・窓切り出し・形式変換、ベクタの形式変換）を置き換えられる見込み**がある。ただし **「入れ替える」より「並べて使い、GDAL と突き合わせる」** のが安全。日本語まわり（文字化け、panic）に落とし穴があり、主要な panic は上流で直りつつある。

## やり方（優先順位つきの助言）

| # | 助言 | 根拠（確かめた度合い） |
|---|---|---|
| 1 | **ブラウザ（terrio-js）で範囲読みを使う**のが、いちばん効く。COG / PMTiles / COPC / FlatGeobuf / GeoParquet を `openUrl` で部分取得できる（GeoParquet 5 GB → 16.4 MiB）。CLI / Python の FlatGeobuf・GeoParquet は**全量取得**なので、同じ感覚で使わない | `terrio-js-cloud-native-reads-in-browser`、`cloud-native-read-behavior-matrix`（played） |
| 2 | **COG / PMTiles の範囲読みは CLI でも有効**。大きな COG の窓切り出し・概観は丸ごとダウンロード不要。ただし downsample 系（translate / warp）は原寸を読む。`--overview N` で概観を使う | `cog-remote-window-overview-and-warp`、`pmtiles-remote-reading`（played） |
| 3 | **GDAL を捨てない**。画素・座標は約 30 項目で GDAL 3.8.4 と一致したが、差もある（南極点の EPSG:3857 変換の失敗、COG `TILING_SCHEME` の黙殺、`--dstalpha` なし、CP932）。COPC・`filter range`・STACIT は PDAL 2.10.2 / GDAL 3.13.3 と一致した。GDAL の版で挙動が変わる例もある（`-ot Int16` の nodata）ので、比べるなら新しい GDAL でも。新しい工程に入れるときは、小さな入力で GDAL と並べる | `terrio-vs-gdal-spot-checks`（played、GDAL 3.8.4 は terrio の基準より古い） |
| 4 | **Shift_JIS（CP932）の Shapefile は、いまは terrio に任せない**。属性が黙って文字化けする。UTF-8 に変換してから使うか、GDAL で読む | `shapefile-cp932-attributes-not-decoded`（played） |
| 5 | **日本語の入力に注意**。0.3.2 の GeoJSON / CSV の日本語長文字列 panic は main で修正済み（#159 → #161、未リリース）。**Zarr の日本語の相対パス**の panic は main にも残る。配布版を使うなら、これを避ける | `geojson-japanese-string-panic`、`japanese-path-panic-in-zarr-parse-name`（played） |
| 6 | **日本の座標変換は使える**。JGD2011 ↔ 平面直角（6669〜6687）は GDAL と小数 9 桁以上で一致。ジオイドは **3 次元の `EPSG:6667` → `6697`** で適用される（2 次元の 6668 では高さ不変。GDAL も同じ） | `jgd2011-plane-rectangular-transform`、`vertical-datum-grids-and-geoid-in-japan`（played） |
| 7 | **タイル生成（tippecanoe）、SQL による幾何の検査・修復、配信は置き換えない**。terrio の範囲外（PMTiles の書き出しは可能だが、tippecanoe の代わりではない）。world 全体を EPSG:3857 に変換する工程は、南極の問題に注意 | `terrio-scope-included-and-excluded`、`hfu-dwg7-workflow-substitution-survey` |
| 8 | **版を固定して使う**。配布版（0.3.2）と main は差があり、ドキュメントも main に追随する。pip / npm の版を決め、踏み跡は版つきで読む。新しい版が出たら `stale` の確かめ直し | `terrio-release-vs-main-drift`、`terrio-install-platforms-and-release-history` |
| 9 | **上流への報告は、再現の最小化・GDAL との突き合わせ・版の明記**をして、未検証の主張を外す。#159 は報告から修正まで早かった。取り下げた下書き（ジオイド）は、投稿前の確認の価値を示す | `upstream-issue-feedback-loop`、`drafts/upstream/README.md` |
| 10 | **Rust から使うなら、版に注意**。0.3.2 の crate は feature で絞れない（46 MB・302 クレート）。絞れるのは main（`geotiff` + `remote` で 24 MB・188 クレート）。ドキュメントの絞り込みの例は main 向け。API 自体（座標変換、遅延読み、COG 書き出し）は書いたとおりに動いた | `terrio-rust-library-and-features`（played） |
| 11 | **公式ノートブックはそのまま動く**（27 セル中、失敗は `zarr` の欠落 1 件）。xarray の例は `pip install zarr` を足す。学習の入口に勧められる | `plays/2026-10-21-notebooks.md`（played） |
| 12 | **MCP（`terrio mcp`）は main の機能**で、配布版にない。書き込みは一時的な場所に限る | `terrio-mcp-server`（played、main） |

## dwg7 が立てるとよい「ケースに則した問い」

kcai の `docs/human-role.md` に従い、この踏み跡の助言は、**dwg7 の現場のケースに当てはめて問い直す**と価値が出る。AI は構造と出典への問いは自分で立てられるが、ケースへの問いは現場を知る人が立てる。例:

1. 自分が実際に回している前処理（例: 平面直角系の GeoTIFF を COG にして PMTiles 配信する工程）を、**同じ入力で terrio と GDAL に通して**、結果が現場で許せる差か。（助言 3 の確かめを、自分の入力で）
2. 自分の Shapefile / CSV / GeoJSON の**日本語の属性とパス**は、0.3.2 で panic や文字化けしないか。（助言 4、5）
3. 世界全体や極域を含むデータを EPSG:3857 にしていないか。含むなら南極の問題に当たる。
4. 範囲読み込みしたいデータは**ブラウザ（terrio-js）で足りるか**、CLI で全量取得になるか。（助言 1）
5. 確かめた結果は、`reviewed_by` に記録する（AI は `reviewed` にしない）。

## 確かめたこと（何をして、何が起きたか）

- 下の「更新履歴」を参照。助言ごとの証拠は、表の踏み跡にある。
- この踏み跡自体は**助言**であり、個々の事実の確かめは各踏み跡で行う。助言の根拠が `read-docs` / `read-source` の場合は、表で明示する（現時点で 1〜12 の根拠の主要部は `played`）。

## 気をつけること

- 助言は**今日時点**。terrio は変化が速く、版が上がれば変わる。`updated` と更新履歴を見る。
- GDAL との比較は 3.8.4 で、terrio の基準（3.12）より古い。差が GDAL 側の改善で消えている可能性がある。
- 規模は小さな入力による**抜き取り**。大規模データ、性能、長期運用は確かめていない。
- AI の助言は `reviewed` にしない。dwg7 / hfu が確認して `reviewed_by` に記録する。

## 更新履歴

- 2026-10-21 夜: 初版。ドキュメント全面消化、GDAL との突き合わせ（ジオイドの訂正を含む）までを反映。
- 2026-10-21 夜（2）: 新しい版の確認（PyPI・crates.io・npm とも 0.3.2 のまま。`stale` にする踏み跡なし）。公式ノートブックを実行（助言 11）。Rust のコードを書いて実行（助言 10、feature の食い違いを確認）。GDAL 3.8.4 の確認を済ませた下書き 2 件を追加（南極点の EPSG:3857、`--ot Int16` の nodata）。

- 2026-10-21 深夜: 用語を「塊」から「踏み跡」に改めた（kcai に追随）。kcai の `docs/human-role.md` を読み、「ケースに則した問い」の節を足した。
- 2026-10-21 深夜（2）: Zarr・JP2・COG が GDAL と画素一致、日本語属性は main の書き出しを GDAL が正しく読むことを確認（助言 3 と 5 の裏づけ）。
- 2026-10-21 深夜（3）: PMTiles を GDAL が読めることを確認（幾何は有効）。タイル生成の代替の可否（助言 7）は、PMTiles の書き出しが使える水準という補強。tippecanoe 相当の機能（属性の間引き、ズーム別の単純化の制御）は未確認のまま。
- 2026-10-22: GDAL 3.13.3 / PDAL 2.10.2（conda-forge）で突き合わせ。COPC・`filter range`・STACIT は一致（助言 3 を補強）。`-ot Int16` の下書きは、新しい GDAL が terrio と同じなので取り下げ（GDAL の版依存）。scripts を kcai の新版に差し替え、`SOURCES.md` を追加した。
- 2026-10-23: **terrio 0.4.0〜0.4.2 が 2026-10-22 に出ていた**（PyPI・crates.io で確認）。この遊びの踏み跡は 0.3.2 で確かめたもので、新版での確かめ直しは**未了**（定期実行または次の作業で行う）。助言の表は 0.3.2 の事実で、0.4.x では変わりうる。ソースの規模と起源を分析した（`terrio-source-scale-and-origins`）。

## 出典

- 各踏み跡（上の表）、`plays/2026-10-21-*.md`、`DECISIONS.md`
