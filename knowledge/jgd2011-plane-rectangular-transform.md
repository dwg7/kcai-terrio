---
id: jgd2011-plane-rectangular-transform
title: JGD2011 と平面直角座標系（EPSG:6669〜6687）の変換と、測地系のずれ
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
  - plays/2026-10-21-first-contact.md（3.4）
  - terrio docs/crs.md、docs/why-terrio.md（格子の適用についての記述が食い違う）
  - plays/2026-10-21-japan-edge-cases-and-survey.md（3）
related: [cog-remote-window-overview-and-warp, terrio-scope-included-and-excluded, vertical-datum-grids-and-geoid-in-japan]
hazard: datum-shift-grids-not-applied
---

## 要点

`terrio crs` は、JGD2011（EPSG:6668）、平面直角座標系（6669〜6687）、JGD2000（4612）、旧日本測地系（4301）を扱え、東京駅の座標を第IX系（6677）に変換すると x=−5992.92、y=−35363.24（東西、南北）になる。**座標は「経度 緯度」の順。** 一方、JGD2000→JGD2011 の変換は値が変わらず、**日本の水平方向の格子は PROJ の CDN にもない**。**旧日本測地系（4301）→ JGD2011 の値は、GDAL 3.8.4 と小数 9 桁まで一致、JGD2000 → JGD2011 は GDAL も恒等**（`terrio-vs-gdal-spot-checks`）。高さ（ジオイド）の扱いは別の塊（`vertical-datum-grids-and-geoid-in-japan`。3 次元の CRS から変換する）。

## やり方

```sh
terrio crs EPSG:6677                                         # 名前
terrio crs EPSG:6668 --to EPSG:6677 139.767125 35.681236      # 経度 緯度 → 東西 南北
terrio crs EPSG:6677 --to EPSG:6668 -4000 -4000               # → 139.78898532 35.96393874
terrio warp URL out.tif --t-srs EPSG:6677 --te -10000 -40000 0 -30000 --te-srs EPSG:6677 --tr 10 10
```

## 確かめたこと（何をして、何が起きたか）

- `terrio crs EPSG:6668 / 6669 / 6676 / 6677 / 6685 / 4612` が名前を返した（6668 は JGD2011、6677 は "JGD2011 / Japan Plane Rectangular CS IX"、6685 は XVII）。
- 東京駅（経度 139.767125、緯度 35.681236）: 6668→6677 は `-5992.919570392903 -35363.23774493004`。4326→6677 は同じ値。
- 6677→6668 の逆変換: `-4000 -4000` → `139.78898532165454 35.96393874058313`。第IX系の原点（東経 139°50′、北緯 36°）の南西に当たる値として整合する。
- **緯度・経度の順**（`35.681236 139.767125`）は失敗: `cannot transform (35.681236, 139.767125)`。EPSG:6668 の軸順は緯度・経度だが、`terrio crs` は gdaltransform 流の「x y」（経度 緯度）。
- 4612（JGD2000）→ 6668: `139.767125 35.681236` のまま、**変化なし**。4301（旧日本測地系）→ 6668: `139.76389102 35.68447488`（経度で約 −0.0032°、緯度で約 +0.0033°）。旧日本測地系のずれ（数百 m 級）と、向きと大きさは矛盾しない。
- リモート COG から 10 km 四方を 6677 に `warp` できた（`cog-remote-window-overview-and-warp`）。
- 平面直角座標系の**軸の意味**: 測量の X（北）、Y（東）ではなく、`terrio` の出力は 東西、南北 の順（x=東、y=北）。この例では、x=−5992.9 は原点の西、y=−35363.2 は原点の南。

## 気をつけること

- **JGD2000→JGD2011 の地殻変動の補正（PatchJGD など）は入っていない**。実測で 4612→6668 は恒等で、ネットワーク ON（PROJ の CDN から格子を取る設定）でも同じ。CDN に日本の水平方向の格子（`jp_` で始まるもの）はジオイド 2 つだけ。ドキュメントは `why-terrio.md`（格子は適用しない）と `crs.md`（適用する）で食い違う。東日本大震災後の地殻変動が大きい地域では、座標の差が実用上問題になりうる（大きさは未確認）。測量成果には使わない。
- 4301（旧日本測地系）→6668 の変換が、何の方法（パラメータ変換か）かは未確認。
- 座標の順序と、測量の X/Y の流儀の違いに注意する。
- 6669〜6687 のうち、実際に変換したのは 6677（第IX系）だけ。他の系は名前の確認のみ。

## 出典

- plays/2026-10-21-first-contact.md
- https://terrio.opengeos.org/crs/ 、https://terrio.opengeos.org/why-terrio/
