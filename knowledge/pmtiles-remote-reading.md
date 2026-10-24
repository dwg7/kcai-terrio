---
id: pmtiles-remote-reading
title: PMTiles をリモートで読む（ラスタ・ベクタ、日本語属性、Range を無視する配信）
status: draft
terrio_version: 0.5.0
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、PyPI の wheel）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-24
interface: cli
verified_on: 2026-10-24
verified_how: played
as_of: 2026-10-21
sources:
  - plays/2026-10-21-first-contact.md（3.2）
  - terrio docs/remote-data.md（PMTiles の節）
  - https://depot.optgeo.org/ （Caddy のファイル一覧、host-inventory.json）
related: [cloud-native-read-behavior-matrix, geojson-japanese-string-panic]
freshness: high
finding:
  - server-ignoring-range-makes-terrio-read-whole-file
---

## 要点

PMTiles は、**Range が効く配信なら**、30 GB 級でも `info` が約 0.8 MiB、窓が約 1.3 MiB で済む。ラスタは zoom レベルが overview になり、ベクタは `--oo ZOOM_LEVEL=N` と `--spat` で必要なタイルだけ読む。日本語の属性は正しく通る。**配信側が Range を無視すると、terrio は全体を読み続ける。**

## やり方

```sh
# ラスタ（Protomaps のサンプル、30.5 GB）
terrio info https://r2-public.protomaps.com/protomaps-sample-datasets/terrarium_z9.pmtiles
terrio convert URL win.tif --srcwin 30000 45000 512 512
# ベクタ（国土数値情報 行政区域 北海道 N03、depot.optgeo.org、2.2 MB）
terrio convert --oo ZOOM_LEVEL=8 --spat 141.2 42.9 141.5 43.15 --spat-srs EPSG:4326 \
  https://depot.optgeo.org/ksj_n03_hkd.pmtiles sapporo.geojson
```

## 確かめたこと（何をして、何が起きたか）

- Protomaps terrarium_z9（30,543,645,671 バイト）: `info` → 131072×130644、3 バンド、EPSG:3857、overview 9 段、約 0.84 MiB。`--srcwin` の窓 → 約 1.3 MiB。
- ksj_n03_hkd.pmtiles: 層 `ksj_n03_shichoson`、MultiPolygon 3625 地物、属性 `code, county_or_city, municipality, pref, subprefecture`。札幌周辺の抽出は 22 地物、約 278 KiB。`municipality: 札幌市北区`、`subprefecture: 石狩振興局` など**文字化けなし**。`info` の CRS は EPSG:3857 と表示（タイルの座標系）。出力 GeoJSON の `crs` も EPSG:3857 で、経緯度ではない。
- **depot.optgeo.org の Range**: `ksj_n03_hkd`（2.2 MB）、`jma_1saibun_hkd`（0.56 MB）、`vlcm`（8 MB）、`bvmap-koicha-tokyo`（5.7 MB）は `Range: bytes=0-99` に 206。`kitaphoto`（783 MB）と `mapterhorn-japan-bridge`（275 GB）は **200 で全体を返す**（`content-length` は全体、`cf-cache-status: BYPASS`）。HEAD は `accept-ranges: bytes` を返すのに、GET の Range が効かない。
- そのため `mapterhorn-japan-bridge.pmtiles` の `info` は、120 秒で 1.2 GiB を受信しても終わらなかった（terrio の要求は `bytes=0-65535` で、応答は 200 → 全体を流し続けた）。PMTiles の header を手で読むと、root ディレクトリ 1,996 バイト、leaf ディレクトリ約 5.9 MB、データ約 274.8 GB、タイル 6731 万、zoom 0〜16。
- 同じ環境から、Protomaps の 30 GB には Range が効いた。環境のプロキシのせいではない。

## 気をつけること

- 大きな PMTiles を読む前に、**Range が効くかを `curl -r 0-99 -D -` で確かめる**（206 か 200 か）。
- 出力 GeoJSON が EPSG:3857 のままになる。経緯度が要るなら `--t-srs EPSG:4326`（このセッションでは未試験）。
- ベクタ PMTiles は、zoom ごとに地物が異なる（簡略化や間引きがある）。`ZOOM_LEVEL` を指定しないときの挙動は未確認。
- 抽出した GeoJSON に日本語の長い文字列が入ると、そのあと terrio で読めなくなる（`geojson-japanese-string-panic`）。今回の札幌周辺では、属性の長さが短く、たまたま通った。

## 0.5.0 での再確認（2026-10-24）

0.4.2 の CLI で `terrio info https://depot.optgeo.org/ksj_n03_hkd.pmtiles` は 12 要求・1.48 MiB で 3,625 地物。terrio-js 0.5.0 の PMTiles（ラスタ 12 要求・832 KiB、ベクタ 1 要求・64 KiB）も同じ。played。PMTiles は範囲読み込みのまま。

## 出典

- plays/2026-10-21-first-contact.md
- https://terrio.opengeos.org/remote-data/
- https://depot.optgeo.org/ 、https://stars.optgeo.org/catalog
