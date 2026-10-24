---
id: terrio-processing-commands-smoke-test
title: 処理系コマンドの動作確認（calc、dem、grid、filter、sieve、proximity、polygonize、rasterize、mosaic、COG）
status: draft
terrio_version: 0.5.0
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-24
verified_on: 2026-10-24
verified_how: played
sources:
  - plays/2026-10-21-untested-items.md（2）
  - terrio docs/cli.md、docs/gdal.md
related: [terrio-cli-overview, cog-remote-window-overview-and-warp, hfu-dwg7-workflow-substitution-survey]
---

## 要点

処理系のコマンド（`calc` `dem` `grid` `filter` `sieve` `proximity` `polygonize` `rasterize` `mosaic` と COG 書き出し）は、小さな実データで**動き、もっともらしい結果を返した**。**値を GDAL と比べてはいない**（この遊びの方針の外）。落とし穴は、(1) `calc` の型（NumPy の規則）、(2) `grid` の引数、(3) COG の `TILING_SCHEME` が黙って無視されること、(4) `warp` に `--dstalpha` がないこと。

## やり方

```sh
# NDVI（Sentinel-2 の B08 と B04）。astype(float) と --type を付ける
terrio calc -A B08.tif -B B04.tif --calc "(A.astype(float)-B)/(A+B)" --type Float32 --NoDataValue -9999 ndvi.tif
terrio sieve scl.tif scl_sieve.tif --st 20 && terrio polygonize scl_sieve.tif scl_poly.gpkg
terrio proximity scl.tif prox.tif --values 6 --distunits GEO
terrio grid pc.laz dsm.tif --tr 5 --stat mean            # --tr が必須（--resolution は別の意味）
terrio dem hillshade dsm.tif hs.tif; terrio dem slope dsm.tif sl.tif -s 1; terrio dem color-relief dsm.tif ramp.txt cr.tif
terrio filter smrf pc.laz gr.laz && terrio filter hag_nn gr.laz hag.laz
terrio rasterize poly.geojson rz.tif -a v --tr 0.001 0.001 --ot Byte
terrio mosaic a.tif b.tif m.vrt        # .vrt（仮想）か .tif（実体）
terrio convert in.tif out.tif -f COG --compress DEFLATE --tile-size 256
```

## 確かめたこと（何をして、何が起きたか）

入力は、Sentinel-2 の B04/B08（東京、512²）、SCL（256²）、Autzen の COPC の切り出し（4.4 万点）、四角形 1 つの GeoJSON。

- `calc`: NDVI は min −0.549、max 0.999、平均 0.344、有効画素 262,144。`astype` と `--type` を付けずに `(A-B)/(A+B)` とすると、**出力が UInt16、nodata 65535** になる（NumPy の型規則。符号なしの引き算は 0 未満が桁あふれする）。
- `polygonize`: SCL から 1,260 ポリゴン。`sieve --st 20` を通すと 85 ポリゴン。
- `proximity --values 6 --distunits GEO`: 最大 2,276.9（距離の単位は座標系の単位）。
- `grid`: 点群（EPSG:2992、ft）から 140×140（5 ft）。標高 416〜589。
- `dem`: hillshade は 1〜255、slope は 0.01〜82.9（度。`-s 1`）、TRI は 1 バンド、color-relief は 3 バンド Byte。
- `filter smrf` → `hag_nn`: 点数は変わらず、次元が付く（分類の中身は未検証）。
- `rasterize`: JGD2011（EPSG:6668）で 0.001° の格子に `--burn 1` または `-a v`（値 7）。36×26、有効 910 画素。**入力の GeoJSON に日本語の長い文字列があると panic する**（`geojson-japanese-string-panic`）。
- `mosaic`: 隣り合う 2 つの窓から 512×512（`.vrt` と `.tif`）。
- COG: `--compress DEFLATE --tile-size 256` で overview 2 段。**`--co TILING_SCHEME=GoogleMapsCompatible` はエラーなしで無視**（画素サイズが元のまま 12.32 m）。
- `warp --dstalpha`: `unexpected argument`（GDAL の `-dstalpha` に当たるものがない）。

## 気をつけること

- **値の正しさは未検証**。数値は「もっともらしい」まで。
- `calc` は NumPy の型規則なので、整数の演算は型に注意（`astype` と `--type`）。
- COG の `TILING_SCHEME` を使う処理（hfu/abidjan-martin）は、いまは置き換えられない。**黙って無視される**ので、出力の画素サイズを確かめる。
- `--help` の名前は GDAL と違うものがある（`grid` の `--tr`、`--stat`、`--method`）。

## 0.4.2 での再確認（2026-10-24）

terrio **0.4.2** で、GDAL 3.8.4（apt）と比べた。`dem` の hillshade・slope・aspect・TRI・TPI・roughness、`--multidirectional`、`--compute-edges`（DSM 140×140）、`translate` の `--srcwin`・`--outsize -r bilinear`・`--ot Byte --scale`、`warp`（EPSG:32654 → 6677、10 m。near・bilinear・cubic・average）、`calc`（NDVI、`A*60`）、`proximity`、`sieve`、`mosaic`（`gdal_merge.py`）は、**すべて画素が完全一致**（差 0）。`warp` の地理変換は GDAL と 2e-9 m 以内。played。`polygonize`・`rasterize`・`grid` と、他のコマンドの細かい引数は 0.4.2 では**確かめ直していない**。注意: GDAL 側の出力の一部（`gdal_calc.py`、`gdal_merge.py`）は、この回は生成に失敗し、先の回に作った出力と比べた。

## 0.5.0 での再確認（2026-10-24）

0.5.0 の wheel で、0.4.2 と同じ比較（`scripts` 外の比較スクリプト）を再実行: `dem` 6 種ほか、`translate`、`warp`、`calc`、`proximity`、`sieve`、`mosaic` の 20 項目が GDAL 3.8.4 と**すべて画素一致**。`rasterize`（2 種）、COG の画素、`mosaic` の VRT も一致。played。

## 出典

- plays/2026-10-21-untested-items.md
- https://terrio.opengeos.org/cli/
