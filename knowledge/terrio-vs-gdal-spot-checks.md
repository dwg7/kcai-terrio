---
id: terrio-vs-gdal-spot-checks
title: GDAL 3.8.4 との突き合わせ（約 30 項目）：一致したこと、食い違い、訂正したこと
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、GDAL 3.8.4 / PROJ 9.4 を apt で導入、Python 3.13.16）
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - plays/2026-10-21-gdal-comparison.md
  - terrio docs/testing.md、docs/conformance.md（作者の突き合わせ）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
related: [terrio-conformance-and-testing-against-gdal, vertical-datum-grids-and-geoid-in-japan, terrio-formats-vectors-streaming-and-tiles, shapefile-cp932-attributes-not-decoded, terrio-processing-commands-smoke-test, terrio-source-quirks]
freshness: high
finding:
  - antarctica-to-webmercator-fails-in-terrio-but-not-gdal
  - int16-nodata-out-of-range-not-clamped
  - cog-tiling-scheme-and-dstalpha-missing
---

## 要点

小さな実データで、terrio 0.3.2 と **GDAL 3.8.4**（terrio の基準 3.12 より古い）を突き合わせた。**画素・座標は、約 30 項目で GDAL と完全（または小数 9〜11 桁まで）一致**した（`dem` 8 種、`translate` 3、`warp` 4 つの再サンプリング、`calc`、`proximity`、`sieve`、`polygonize`、`mosaic`、`rasterize`、COG、ベクタ変換 5 形式、日本の座標系、旧日本測地系、NADCON5、エポック、EGM96）。**作者の「GDAL と同じ」という主張は、この範囲では裏づけられた。** 食い違いは、**南極の点での Web Mercator 変換（terrio は失敗、GDAL は成功）、`--ot Int16` の nodata（GDAL は丸めて警告）、CP932 の Shapefile、COG の `TILING_SCHEME`、`--dstalpha`** の 5 つ。**以前の 2 つの「発見」は誤りで、訂正した**（日本のジオイド、`calc` の型）。

## やり方

```sh
sudo apt-get install -y gdal-bin python3-gdal proj-bin       # GDAL 3.8.4、PROJ 9.4（Ubuntu noble）
gdaldem hillshade dsm.tif g_hs.tif ; terrio dem hillshade dsm.tif t_hs.tif    # 画素を numpy で比べる
echo "180 -90" | gdaltransform -s_srs EPSG:4326 -t_srs EPSG:3857
ogr2ogr -f GeoJSON out.geojson countries.gpkg -t_srs EPSG:3857
```

（`terrio.open_raster(f).read(1)` で両方の出力を読み、`numpy` で差を取った。`gdal_calc.py` などは `python3.12 /usr/bin/…`。）

## 確かめたこと（何をして、何が起きたか）

**一致したもの（played）**

| 領域 | 項目と結果 |
|---|---|
| 地形 | `dem` hillshade、slope、aspect、TRI、TPI、roughness、`--multidirectional`、`--compute-edges`: 140×140 で**画素差 0** |
| 切り出し・縮小 | `translate --srcwin`、`--outsize … -r bilinear`、`--ot Byte --scale`: **差 0** |
| 再投影 | `warp`（EPSG:32654 → 6677、10 m、near / bilinear / cubic / average）: 大きさ・範囲・画素が**一致** |
| ラスタ代数 | `calc` NDVI（Float32）、`A*60`（Byte の桁あふれ）、`proximity`、`sieve`: **一致**。`polygonize` の地物数 1,260 が一致 |
| モザイク・焼き込み | `mosaic`（.tif は `gdal_merge.py`、.vrt は GDAL が描画）、`rasterize`（`-a`、`--at`）: **一致** |
| COG | terrio の COG を GDAL が読め、画素は GDAL の COG と一致 |
| ベクタ | 国界 177 を FlatGeobuf、GeoJSON、Shapefile、GML、KML に変換 → GDAL が 177 地物で読む |
| 座標 | JGD2011 → 平面直角（6669、6672、6677、6679、6685、6687）と逆変換: 小数 9 桁以上で一致。旧日本測地系 4301 → 6668 は 1e-9 で一致、4612 → 6668 は両方恒等。NADCON5、エポック、EGM96 も一致 |
| 日本のジオイド | 同じ格子（GSIGEO2011）を使えば、**小数 11 桁まで一致**。terrio は新しい JPGEO2024 を優先（0.1 m 差）。2 次元の `EPSG:6668` では、**GDAL も高さを変えない** |

**食い違い（played）**

1. **南極（`(180, -90)`）の Web Mercator 変換**: terrio は `failed to reproject feature 159 … cannot transform (180, -90)` で止まり、GDAL の `ogr2ogr` は 177 地物を出力する（`gdaltransform` は `20037508.34 -242528680.94`）。入門ページの例と PMTiles の既定の書き出しが影響を受ける。
2. **`translate -ot Int16`（Float32、nodata −999999）**: terrio は nodata を −999999 のまま、GDAL は `-32768` に丸めて警告する。
3. **CP932 の Shapefile**: GDAL は `.cpg`（CP932 / SHIFT_JIS）か `SHAPE_ENCODING=CP932` で正しく読む。terrio は読めない。
4. **COG の `TILING_SCHEME=GoogleMapsCompatible`**: GDAL は 9.5546 m・1024×1024 に整列、terrio は黙って無視。
5. **`warp -dstalpha`**: GDAL にあり、terrio にない。
6. **日本語の長い文字列の GeoJSON**: GDAL は読める（#159 の本文のとおり。0.3.2 の terrio は panic、main は修正済み）。

**訂正したもの**: 「日本のジオイドが適用されない」は誤り（`vertical-datum-grids-and-geoid-in-japan`）。「`calc` の `/` が整数に丸まるのは問題」も、GDAL の `gdal_calc.py` と同じ既定だった。

## 追加の突き合わせ（Zarr・JP2・日本語属性）

- terrio 0.3.2 が書いた **Zarr、JPEG 2000、COG** を GDAL 3.8.4 が読むと、画素・地理変換・座標系が完全一致した（`plays/2026-10-21-gdal-comparison.md` §5、played）。
- 日本語属性は、main のビルドで書いた Shapefile（`.cpg`=UTF-8）、FlatGeobuf、GeoPackage、PMTiles を GDAL が正しく読む。0.3.2 は #159 の panic で書けない（played）。
- GeoParquet は GDAL 側のドライバーが無く、突き合わせできなかった。

## PMTiles（MVT）

terrio 0.3.2 が書いた PMTiles（国界 179 地物、z0〜5）を GDAL 3.8.4 が読めた。幾何はすべて有効、属性は `mvt_id` / `id` / `name`、小さな島は低ズームで落ちる。`terrio info` の地物片の数（806）は GDAL の最大ズームの数（839）と一致せず、原因は未確認（`plays/2026-10-21-gdal-comparison.md` §6、played）。STACIT と COPC は GDAL / PDAL との突き合わせが未了。

## 気をつけること

- **GDAL は 3.8.4 で、terrio の基準（3.12）ではない**。EPSG の版、ドライバーの有無（Parquet、PDAL なし）の違いがある。ずれがあっても、3.12 で同じとは限らない。
- 突き合わせたのは**小さなデータ**。作者の 4 万件の比較（`terrio-conformance-and-testing-against-gdal`）の代わりにはならない。
- 上流に伝えるなら、**確かめた GDAL の版を明記する**。食い違い 1〜5 は、下書きにした（投稿は hfu が確認して行う）。
- 結果は、速度ではなく**値の一致**。

## 出典

- plays/2026-10-21-gdal-comparison.md
- https://gdal.org/ 、https://proj.org/
