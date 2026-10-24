---
id: data-licenses-of-play-datasets
title: 遊びで使ったデータのライセンス表記（配信元が書いていること）
status: stale
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: read-docs
as_of: 2026-10-21
sources:
  - Earth Search の STAC コレクション sentinel-2-l2a（license と license リンク）
  - Source Cooperative の vida/google-microsoft-open-buildings のページ
  - Overture Maps の docs.overturemaps.org/attribution/
  - stars.optgeo.org の /catalog、PMTiles のメタデータ（`terrio info`）
  - Hugging Face の severo/geoparquet のデータカード
  - plays/2026-10-21-license-and-basics.md
related: [terrio-license-and-third-party-notices, pmtiles-remote-reading, cloud-native-read-behavior-matrix]
freshness: high
---

## 要点

kcai-terrio の README は、「CC0 は terrio（MIT）や、遊びで使ったデータのライセンスには適用されない」と書いている。この踏み跡は、**使ったデータが、配信元で何と表示されていたか**だけを記録する。**表示を読んだだけで、利用条件の解釈や、再利用の可否の判断ではない**。確かめていないものは「未確認」と書く。**データ本体はリポジトリに入れていない**（`.gitignore`、一時ファイルは都度削除）。

## やり方

配信元の、ライセンス表示の場所:

- STAC: コレクションの `license` と `rel: license` のリンク
- Source Cooperative: 製品ページの "Dataset Licenses"
- Overture: `docs.overturemaps.org/attribution/`
- PMTiles: `terrio info` のメタデータ（`attribution`）、Martin の `/catalog`
- Hugging Face: データカード（`cardData`）

## 確かめたこと（何をして、何が起きたか）

| データ（使った場面） | 配信元の表示 | 状態 |
|---|---|---|
| Sentinel-2 L2A の COG（Earth Search / sentinel-cogs。東京の窓、STACIT） | STAC の `license`: **`proprietary`**。リンク先は ESA の "Sentinel Data Legal Notice" | 表示を確認。条件の中身は読んでいない |
| Overture Maps の GeoParquet（places の `info`） | **テーマや出典ごとに異なる**。帰属表示のページに、CDLA Permissive 2.0、ODbL、CC BY 4.0 などの記載 | 表示を確認。places の個別の条件は確かめていない（`info` だけで、データは残していない） |
| 日本の建物（Source Cooperative の `vida/google-microsoft-open-buildings`、JPN.parquet、5 GB） | 製品ページの "Dataset Licenses" に **Open Database License (ODbL) v1.0** | 表示を確認 |
| Protomaps の terrarium_z9.pmtiles（30.5 GB） | PMTiles のメタデータの `attribution` に、多数の出典（ArcticDEM、豪州の Geoscience Australia、オーストリアの DGM、カナダの Open Government Licence、EU-DEM、ETOPO1、メキシコの INEGI など）が列挙 | 表示を確認。各出典の条件は別 |
| 国土数値情報 行政区域 N03（depot.optgeo.org の `ksj_n03_hkd.pmtiles`） | Martin のカタログは `description` のみ（"国土数値情報 行政区域（北海道）N03 2023"）で、`attribution` は空 | **利用条件は未確認** |
| シームレス空中写真（stars のカタログ。窓は取っていない） | "国土地理院 シームレス空中写真 (GSI seamlessphoto) CC BY 4.0" | カタログの表示のみ |
| 火山土地条件図（stars のカタログ。取っていない） | "測量法に基づく国土地理院長承認（使用）R 8JHs 207" | カタログの表示のみ |
| bvmap-koicha-tokyo（stars のカタログ。取っていない） | "国土地理院最適化ベクトルタイルを加工して作成"、"Not an official GSI product" | カタログの表示のみ |
| NZ の建物（Hugging Face の `severo/geoparquet`、`nz-building-outlines.parquet`、430 MB） | データカードは `license: mit` だけ。**元データの出どころは書かれていない** | カードの表示のみ。**出どころは未確認** |
| NOAA HRRR の Zarr（S3 の `hrrrzarr`） | — | **未確認** |
| Autzen の COPC（`hobu-lidar`）、UScounties.fgb（flatgeobuf.org のテストデータ） | — | **未確認** |
| PROJ の格子（`cdn.proj.org` の `us_nga_egm96_15.tif`、`jp_gsi_gsigeo2011.tif`） | — | **未確認**（格子ごとに異なる） |

## 気をつけること

- 「配信元が表示している」ことは、**そのデータを、自分の用途で使ってよい**ことを意味しない。日本の公的データ（国土数値情報、国土地理院）は、それぞれの利用規約・承認の表記ルールがある。使う前に、一次の規約を読む。
- 派生物（切り出した GeoJSON など）を**公開する場合**は、帰属表示と、ODbL のようなシェアアライクの条件に注意する。このリポジトリは、データの派生物を公開していない。
- ライセンス表示は変わりうる。**確認日は 2026-10-21**。
- Hugging Face のカードの `mit` は、データではなく、リポジトリの設定かもしれない。**元の出どころを確かめるまで、再利用しない**。

## 出典

- https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a
- https://source.coop/vida/google-microsoft-open-buildings 、https://docs.overturemaps.org/attribution/
- https://stars.optgeo.org/catalog 、https://huggingface.co/datasets/severo/geoparquet
- plays/2026-10-21-license-and-basics.md
