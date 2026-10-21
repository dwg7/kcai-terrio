# 2026-10-21 GDAL との突き合わせ（GDAL 3.8.4 / PROJ 9.4 を apt で導入）

- 日付: 2026-10-21（夜）
- terrio: 配布版 0.3.2（wheel）。一部 main（`6779102`）のビルド。terrio-js 0.3.2
- GDAL: Ubuntu noble の `gdal-bin` / `python3-gdal` / `proj-bin`（GDAL **3.8.4**、released 2024/02/08、PROJ 9.4）。**terrio の基準（GDAL 3.12、PROJ 9.8.1）より古い**。Python の結合は `python3.12` で動き、CLI（`gdalinfo`、`ogr2ogr`、`gdal_translate`、`gdalwarp`、`gdaldem`、`gdaltransform`、`cs2cs`、`projinfo`、`gdal_calc.py`、`gdal_proximity.py`、`gdal_sieve.py`、`gdal_polygonize.py`、`gdal_merge.py`、`gdal_rasterize`）が使える
- 目的: これまで**未確認だった**「GDAL の挙動」を確かめ、下書きの「未検証の主張」を外す（hfu の方針）。AGENTS.md の方針（GDAL との突き合わせは遊びの目的ではない）の範囲では、必要な確認に限った
- 入力は小さなデータ（Sentinel-2 の 512²、SCL の 256²、点群から作った DSM 140×140、Natural Earth の国界 177 地物）。一時ファイルは `/tmp/work`

## 1. 画素・数値の突き合わせ（terrio 0.3.2 と GDAL 3.8.4）

| 比べたもの | 結果 |
|---|---|
| `dem` hillshade / slope / aspect / TRI / TPI / roughness、`--multidirectional`、`--compute-edges`（DSM 140×140） | **8 項目すべて画素が完全一致**（差 0） |
| `translate`: `--srcwin`、`--outsize 100 100 -r bilinear`、`--ot Byte --scale 0 3000 0 255` | **3 項目すべて一致** |
| `warp`（EPSG:32654 → EPSG:6677、10 m）: near、bilinear、cubic、average | **4 項目すべて、出力の大きさ・範囲・画素が一致**（518×518） |
| `calc`: NDVI（Float32）、`A*60`（Byte の桁あふれ） | **一致** |
| `proximity --values 6 --distunits GEO`、`sieve --st 20` | **一致** |
| `polygonize`（SCL） | 地物数 1,260 で一致 |
| `mosaic`（.tif と `gdal_merge.py`、.vrt を GDAL が描画したもの） | **一致** |
| `rasterize`（`-a v`、`--at`） | 大きさ（36×46）・範囲・画素が**一致** |
| `convert -f COG --compress DEFLATE --tile-size 256` | GDAL がそのまま読み、画素は GDAL の COG と一致 |
| `convert`（国界 177 → FlatGeobuf、GeoJSON、Shapefile、GML、KML） | GDAL が読んで **177 地物**（ogr2ogr の出力と同数） |
| 座標変換: JGD2011 → 第IX系（6677）、逆変換、6669 / 6672 / 6679 / 6685 / 6687 | **小数 9 桁以上で一致**（例 `-5992.919570392903` と `-5992.9195703929`） |
| 旧日本測地系 `EPSG:4301 → 6668` | `139.76389102546048 35.68447487973283` と GDAL の `139.76389102546 35.6844748806271`（**約 1e-9 で一致**）。`4612 → 6668` は両方恒等 |
| NADCON5 `EPSG:4267 → 4269`（`-100 40`、ネットワークあり） | terrio `-100.0004055982497 40.00000580229538`、GDAL `-100.00040559825 40.0000058022954`（**一致**） |
| エポック（`EPSG:7912 → 7843`、2010.0） | `135.0000030617912 -24.99999469886912 -0.0015074610710144` と GDAL（**一致**） |
| EGM96（`EPSG:4979 → 4326+5773`、高さ 50） | terrio 13.5559、GDAL 13.5558849…（**一致**） |

## 2. 食い違い（GDAL の挙動を確かめた結果）

| 項目 | terrio 0.3.2 | GDAL 3.8.4 |
|---|---|---|
| **世界の国界を EPSG:3857 へ**（`ogr2ogr -t_srs EPSG:3857` と `terrio convert --t-srs`） | **失敗**: `failed to reproject feature 159 … cannot transform (180, -90)` | **成功**（177 地物）。`gdaltransform` は `(180,-90)` を `20037508.34 -242528680.94` に変換（`cs2cs` は `Invalid latitude` → inf）。入門ページの例と PMTiles の既定の書き出しが、これで失敗する |
| `translate -ot Int16`（Float32 の標高、nodata −999999） | 出力は `Int16`、**nodata=-999999 のまま**（範囲外。警告なし） | **`Warning 1: for band 1, nodata value has been clamped to -32768`** で `-32768` |
| Shapefile の属性が CP932（`札幌市`） | `.cpg` が CP932 / SHIFT_JIS でも、`SHAPE_ENCODING=CP932` でも**文字化け** | `.cpg=CP932` / `SHIFT_JIS` または `SHAPE_ENCODING=CP932` で `札幌市`。`.cpg=UTF-8` と `.cpg` なしは文字化け |
| COG の `TILING_SCHEME=GoogleMapsCompatible` | 黙って無視（画素サイズ 12.32 m のまま） | 画素サイズ 9.5546 m、1024×1024 に整列 |
| `warp --dstalpha` | `unexpected argument` | `gdalwarp -dstalpha` で 2 バンド（アルファつき） |
| 日本語の長い文字列を含む GeoJSON（`東京都千代田区`） | 0.3.2 で panic（#159。main で修正） | 問題なく読む（地物 1）。**#159 の本文の「GDAL は問題なく読む」は、事実だった** |
| 3 次元 `EPSG:6667 → 6697`（日本のジオイド） | JPGEO2024（高さ 86.7 → 49.9386） | GSIGEO2011（86.7 → 50.0375）。**同じ格子なら小数 11 桁まで一致**。那覇では GDAL は不変、terrio は 69.15 |
| 2 次元 `EPSG:6668 → 6697`（高さ 86.7） | 86.7（不変） | 86.7（不変。`projinfo` は `+proj=noop`） |
| `gdal_calc.py` / `terrio calc` の `A/5`（`--type` なし） | Byte（値 1） | **同じ（Byte）**。`A*60` の桁あふれも同じ |

## 3. 訂正

- **「日本のジオイドが適用されない」は誤り**（2 次元の `EPSG:6668` を使ったため）。GDAL も同じ。3 次元の `EPSG:6667` からなら terrio は適用する。`drafts/upstream/2026-10-21-jgd2011-geoid-heights-unchanged.md` は、**投稿前に確かめて、取り下げた**
- 「`calc` の `/` が整数に丸まる」は、GDAL と同じ既定で、terrio の不具合ではない

## 4. 確かめられなかったこと

- GDAL 3.12（terrio の基準）での結果。3.8.4 との差（EPSG の版、PMTiles / STACIT ドライバー、Parquet は非対応）がありうる
- PMTiles / MVT の書き出し、STACIT、Zarr、JPEG 2000、COPC、点群の GDAL / PDAL との比較（GDAL 3.8.4 に Parquet ドライバーなし。PDAL なし）
- 大きなデータでの速度（ベンチマーク）

## 5. 追加の突き合わせ（形式の相互運用、同じ夜の続き）

- 入力: Sentinel-2 B04（512²、UInt16、EPSG:32654）。terrio 0.3.2 で `convert` した **Zarr、JPEG 2000、COG** を GDAL 3.8.4（Zarr、JP2OpenJPEG、GTiff ドライバー）で読むと、**画素が完全一致、地理変換と座標系も一致**（無損失）。
- 日本語の属性（`札幌市`、`東京都千代田区`）を持つ GeoJSON を、**main のビルド**で Shapefile（`.cpg`=UTF-8）、FlatGeobuf、GeoPackage、PMTiles に書くと、GDAL（`ogrinfo`）が**正しい日本語で読む**。0.3.2 では同じ入力が #159 の panic（`千` の途中で切る）で、どの形式にも書けない（main で直る）。
- GeoParquet は、この GDAL（apt）に Parquet ドライバーが無く、読めなかった（terrio の問題ではない）。
