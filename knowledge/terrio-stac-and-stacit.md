---
id: terrio-stac-and-stacit
title: STAC と STACIT：検索結果のモザイク、max_items で転送量を減らす
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - terrio docs/formats.md の STAC の節、docs/remote-data.md の STAC の節（main 6779102）
  - Earth Search（sentinel-2-l2a、東京の検索）
  - plays/2026-10-21-untested-items.md、plays/2026-10-21-license-and-basics.md
related: [cloud-native-read-behavior-matrix, terrio-formats-rasters-and-compression, data-licenses-of-play-datasets]
freshness: high
---

## 要点

STAC の Item、ItemCollection（STAC API の検索結果）、Collection、Catalog は、**地物の範囲を持つベクタ層**として開ける。検索結果の資産（アセット）は `STACIT:"検索の URL":asset=red` で**モザイクのラスタ**として開け、窓読みでは必要なタイルだけを取る。**重なる全シーンから読むが、`max_items=N` で絞れる**。東京の 3 シーンの重なりで、窓（512²）の転送量が **17.5 MiB から 6.2 MiB** に減った（結果の平均は同じ）。

## やり方

```sh
Q="https://earth-search.aws.element84.com/v1/search?collections=sentinel-2-l2a&bbox=139.7,35.6,139.8,35.7&datetime=2026-10-10T00:00:00Z/2026-10-21T00:00:00Z&limit=4"
terrio info "$Q"                                      # 地物の範囲の層（3 件）
terrio info "STACIT:\"$Q\":asset=red"                  # 10980² のモザイク
terrio convert "STACIT:\"$Q\":asset=red,max_items=1" r.tif --srcwin 5000 5000 512 512   # 1 シーンだけ（約 6.2 MiB）
terrio info 'STAC:"https://…/items/S2B_…":red'          # 1 つのアイテムの資産
```

- オプションは **`asset=red,max_items=1` のようにカンマ区切り**（`:` や空白区切りは `rc=1` で失敗した）。ドキュメントによると、`collection=`、`crs=` の絞り込みと、terrio 独自の `resolution=highest|lowest|average`、`max_items=N` がある。

## 確かめたこと（何をして、何が起きたか）

- 検索（`bbox=139.7,35.6,139.8,35.7`、2026-10-10〜21）は 3 件: 2026-10-18（雲量 0.7%）、10-13（63.7%）、10-10（7.3%）。API が返す順は新しい順。
- `terrio info "$Q"` は `Driver: GeoJSON`、層 `search`、3 地物。受信 62 KiB（要求 2 回）。`STACIT:…:asset=red` の `info` は `Driver: STACIT`、10980×10980、EPSG:32654、受信 188 KiB（要求 5 回）。
- 窓の `convert`: 全シーンで **要求 11 回、17,918 KiB**（約 17.5 MiB）。`max_items=1` で **要求 4 回、6,398 KiB**（約 6.2 MiB）。**どちらも窓の平均が 804** で同じ。ドキュメントは「アイテムは日付の昇順に重ねる」と書くので、最新のシーンが上に来て、古い 2 シーンの分の転送（約 11 MiB）は、この窓では無駄だった。
- アセットの資産は `STAC:"item":asset`（または `item.json!asset`）で開ける。href は項目の場所から解決される（read-docs）。検索は `next` のリンクを辿り、**最大 1000 件**（read-docs）。

## 気をつけること

- **窓の転送量は、重なるシーンの数に比例する**。雲の多い日付も含めて読む。`max_items` は**新しい順に並べた先頭ではなく、「ドキュメントの重ね順」に従う**ので、どのシーンが残るかは、結果で確かめる（この例では、新しい 2026-10-18 が上に出た）。
- STAC API の POST ページング、STACTA（タイルつきアセット）、署名つき URL（Planetary Computer）は未対応（ロードマップの未完了）。
- STAC のデータのライセンスは、コレクションごとに違う（`data-licenses-of-play-datasets`: Sentinel-2 は `proprietary` と表示）。

## 出典

- https://terrio.opengeos.org/formats/ 、https://terrio.opengeos.org/remote-data/
- https://earth-search.aws.element84.com/v1
- plays/2026-10-21-untested-items.md
