---
id: cog-remote-window-overview-and-warp
title: リモート COG の窓読み・overview・縮小の使い分け
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
as_of: 2026-10-18
sources:
  - plays/2026-10-21-first-contact.md（3.1）
  - terrio docs/remote-data.md、docs/gdal.md
  - Earth Search STAC（sentinel-2-l2a、アイテム S2C_54SUE_20261018_0_L2A）
related: [cloud-native-read-behavior-matrix, jgd2011-plane-rectangular-transform]
freshness: high
finding:
  - translate-outsize-downloads-whole-cog
  - overview-index-is-zero-based-from-first-reduction
---

## 要点

リモート COG から小さな部分を取るなら、`convert --srcwin`（ピクセルの窓）か `warp --te`（出力範囲）か `convert --overview N`（縮小版）を使う。**`translate --outsize` で縮小すると、全体（この例で約 208 MiB）を取る。**

## やり方

```sh
U=https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/54/S/UE/2026/10/S2C_54SUE_20261018_0_L2A/B04.tif
terrio info $U                                       # 約 78 KiB
terrio convert $U win.tif --srcwin 5000 5000 512 512  # 約 6.4 MiB
terrio convert $U ov.tif --overview 2                 # 1373x1373、約 2.6 MiB
terrio warp $U out.tif --t-srs EPSG:6677 --te -10000 -40000 0 -30000 --te-srs EPSG:6677 --tr 10 10 -r bilinear   # 約 6.1 MiB
# 避ける: terrio translate $U small.tif --outsize 512 512   # 約 208 MiB
```

アイテムは Earth Search の STAC 検索（`POST /v1/search`、bbox 139.6,35.6,139.9,35.8、雲量 20% 未満）で見つけた。

## 確かめたこと（何をして、何が起きたか）

- B04: 10980×10980、UInt16、EPSG:32654、ファイル 216,253,355 バイト。`Accept-Ranges: bytes`。overview は 5490, 2745, 1373, 687。
- `--overview 4` は失敗（`no overview 4: the raster has 4 overview(s)`）。0〜3 が有効で、**`--overview 0` は 5490×5490（全解像度ではない）**。全解像度は `--overview` では取れない。
- `--srcwin 5000 5000 256 256` と `... 1024 1024` は、どちらも約 6.4 MiB。窓が 5120 のタイル境界をまたぐため（タイル 1024、圧縮後 約 1.6 MiB）。
- `warp` の出力: `Origin (-10000, -30000)`、`WGS 84 extent: (139.7228, 35.6394)–(139.8333, 35.7296)`。東端の経度 139.8333 は、第IX系の原点（東経 139°50′）と合う。
- `translate --outsize 512 512` は `-r average` でも約 208 MiB。

## 気をつけること

- `--overview` は 0 始まりで、全解像度は含まない。
- 窓読みの転送量はタイル数で決まる。窓を小さくしても減らないことがある。タイル境界に合わせると減る（未確認）。
- この COG は 2026-10-18 の撮影。Sentinel-2 のアイテムは新しいものが出続けるので、同じ URL を後で使うなら STAC で探し直す。
- `convert --help` には「overview N (0 is the largest)」とあり、実測と合う。一方 `docs/cli.md` と `docs/remote-data.md` は番号の意味を書いていない。

## 出典

- plays/2026-10-21-first-contact.md
- https://terrio.opengeos.org/remote-data/ 、https://terrio.opengeos.org/gdal/
- https://earth-search.aws.element84.com/v1
