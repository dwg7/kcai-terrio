---
id: terrio-formats-rasters-and-compression
title: 対応形式（ラスタ）と圧縮：表をバイナリの terrio formats と突き合わせた
status: stale
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-24
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - terrio docs/formats.md の Rasters、In WebAssembly の節（main 6779102）
  - "`terrio formats --json`（0.3.2 の wheel、49 行）"
  - plays/2026-10-21-license-and-basics.md
related: [terrio-formats-vectors-streaming-and-tiles, terrio-stac-and-stacit, terrio-scope-included-and-excluded, cloud-native-read-behavior-matrix]
---

## 要点

ラスタは **GeoTIFF/COG、JPEG 2000、Zarr v2/v3（GeoZarr）、netCDF、HDF5、ERDAS Imagine、GeoPackage、PMTiles/MBTiles、VRT、STACIT、ENVI/Esri/SAGA/Idrisi などの格子形式、PNG/JPEG（ワールドファイルつき）、DTED** など。名前は GDAL の短い名前に合わせる（`-f GTiff`、`-f "ESRI Shapefile"`）。**ドキュメントの表と、0.3.2 のバイナリの `terrio formats --json` は一致した**（機械的に比較）。

## やり方

```sh
terrio formats                 # 名前、種類、読み書き、拡張子
terrio formats --json          # 配列。{name, long_name, kind, extensions, read, write}
terrio convert dem.tif dem.zarr --co FORMAT=ZARR_V3 --co GEOREFERENCING_CONVENTION=SPATIAL_PROJ --co OVERVIEW_LEVELS=AUTO
terrio convert in.tif out.nc --co FORMAT=NC4 --co COMPRESS=DEFLATE        # netCDF-4
```

## 確かめたこと（何をして、何が起きたか）

**ドキュメントの表とバイナリの突き合わせ（played）**: 表の 46 行（ラスタ 25、ベクタ 17、点群 3）は、バイナリの 49 行にすべて含まれる。バイナリにだけあるのは点群の **E57、EPT、PLY**（表には LAS、LAZ、COPC だけで、ほかは `point-clouds.md` にある）。`HFA`（ERDAS Imagine）の書き込みは、表で `✓*`（`gdal` feature で書く）、バイナリで書き込みなし（`r-`）で、整合する。読み書きの印は、ほかに食い違いなし。

**GeoTIFF の圧縮（read-docs）**: なし、LZW、Deflate（古い符号も）、PackBits、JPEG、WebP、Zstandard、LZMA、LERC（単体、Deflate や Zstandard との組み合わせ、可逆・不可逆、NaN マスク）、JPEG XL。水平・浮動小数点の予測子、タイル・ストリップ、chunky・planar。**LERC、JPEG XL、LZMA は読み取りのみ**。JPEG は libjpeg と同じ整数 IDCT、色空間の変換で復号し、「画素は GDAL と同じ」と書く。9〜15 ビット、17〜31 ビットの詰めた符号なしは UInt16/UInt32 として読む（Sentinel-2 の 15 ビットなど）。

**JPEG 2000（read-docs + 一部 played）**: OpenJPEG の Rust 移植で、GeoJP2 / GMLJP2 の位置情報。窓と解像度レベルで範囲読み。ドキュメントは「10980² のバンドで 1024² の窓が 0.05 秒（全体の復号は 0.5 秒）」と書く。**実測では、窓は 3.3 MiB の範囲読み、overview 3 は約 24.8 MiB（ほぼ全体）**（`cloud-native-read-behavior-matrix`）。

**netCDF / HDF5**: 変数は `NETCDF:"file.nc":variable` / `/group/variable`、HDF5 は `HDF5:"file.h5"://group/dataset`。複数の変数は最初のものを開き、残りを subdataset として一覧する（`gdalinfo` と同じ）。**最後の次元が `bands` の 3 次元変数**（EMIT など）、緯度経度の配列（GEOLOCATION）、HDF-EOS5 のグリッドとスワス、COSMO-SkyMed、ODIM などの製品固有の位置情報を GDAL のとおりに読む、と書く。netCDF の書き出しの `--co`: `FORMAT`（NC、NC2、NC5、NC4、NC4C）、`COMPRESS`、`ZLEVEL`、`CHUNKING`、`GROUP`。netCDF-4 は HDF5 を terrio が自分で書く（C ライブラリなし）。複素数は 2 バンドで持ち、`terrio info` が複素型を報告する。**どれも実データでは試していない**（read-docs）。

**GeoPackage ラスタ**: Byte は PNG（`--compress JPEG` で JPEG）、1 バンドの Int16/UInt16/Float32 はグリッドカバレッジで書く。**Zarr**: GDAL と xarray の流儀、GeoZarr の `spatial:`、`proj:`、`multiscales`（下位レベルが overview）、コーデック（none、zlib、gzip、Zstandard、LZ4、Blosc）、v3 のシャーディング、`float16` は Float32 で読む。書き出しの `--co`: `FORMAT`、`GEOREFERENCING_CONVENTION`（`GDAL` / `SPATIAL_PROJ` / `CF`）、`OVERVIEW_LEVELS`、`OVERVIEW_RESAMPLING`。リモートの Zarr は範囲読み（`HRRR` で確認済み）。

**WebAssembly の節（read-docs。terrio-js で一部確認）**: バイトから読む。JPEG 2000 と、上のすべての圧縮の GeoTIFF を読める。複数ファイルの形式（Shapefile、MapInfo）は zip で渡す。GeoPackage、PMTiles、MBTiles は読み書きできる。**`openUrl` による範囲読みの形式は、ドキュメントではなく型定義に書かれている**（`terrio-js-cloud-native-reads-in-browser`）。

## 気をつけること

- 「画素は GDAL と同じ」は、ドキュメントの主張で、この遊びでは検証していない。「JPEG XL（不可逆）は libjxl と、一部の画素で 1 違うことがある」とドキュメント自身が断っている。
- **書き出しは、すべての形式でできるわけではない**: HDF5、OSM、EPT、STACIT は読み取りのみ。タイルのアーカイブは **1〜4 の Byte バンド**だけ（他の型は `translate --ot Byte --scale` で先に変える）。
- 読み取りは、ほとんどの非 GeoTIFF でメモリに全部読む（`docs/gdal.md`）。
- 試したのは、GeoTIFF/COG、JPEG 2000、Zarr（HRRR）、PMTiles、GeoPackage（書き出しと追記）、VRT、ASCII など一部。

## 0.4.2 での再確認（2026-10-24）

terrio **0.4.2** で、Sentinel-2 B04 を Zarr・JPEG 2000・COG に変換し、GDAL 3.8.4 で読むと、**画素が完全一致**（played、部分）。他の形式・圧縮は確かめ直していない。

## 出典

- https://terrio.opengeos.org/formats/
- `terrio formats --json`（0.3.2）、plays/2026-10-21-license-and-basics.md
