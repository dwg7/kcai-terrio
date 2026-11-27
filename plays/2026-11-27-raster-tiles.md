# 2026-11-27 `terrio tile` と `gdal2tiles` の比較（terrio 0.10.0・GDAL 3.13.3）

- 入力: Sentinel-2 L2A の B04（UTM 54N、10 m）の 1024×1024 の窓を、Byte（0〜3000 を 0〜255）にしたもの
- 実行: `terrio tile src8.tif t_tiles --min-zoom 10 --max-zoom 14 -r bilinear` と `gdal2tiles.py --xyz -z 10-14 -r bilinear --processes=2`。画素は PIL で比べた（タイルは L または LA のモード）

## 結果

| 項目 | 結果 |
|---|---|
| タイル集合 | 61 枚で同じ（z10:1、z11:2、z12:6、z13:16、z14:36） |
| 時間 | terrio 1.2 秒、gdal2tiles 1.05 秒（2 プロセス） |
| z14（最大）`-r near` | 差のある画素 0.3%（6,029/2,359,296）、ずれなし、アルファの有効範囲は同じ |
| z14 `-r bilinear` | 平均差 0.05 階調、最大 1 |
| z13 / z12 / z11 / z10（bilinear） | 平均差 2.5 / 4.2 / 4.5 / 4.2、8 階調超の画素 3.6〜13.8%、アルファの不一致 1,358 / 992 / 560 / 276 画素 |
| `--overview-resampling average`（tiles／source） | z10〜13 の平均差 4.2・4.5・4.2・2.5／4.2・4.6・4.4・2.9（ほぼ変わらず） |
| `--overview-resampling bilinear --overview-source source` | 1.6・1.7・1.8・4.5（z10〜12 は縮むが z13 が広がる） |
| `--overview-resampling near`（tiles） | 18.7・16.1・12.2・6.7（悪化） |

## 発見

1. タイル集合・ズーム・最大ズームの画素は、`gdal2tiles` とほぼ同じ。
2. 低ズームは、どの設定でも一致しない（縮小のやり方の違い。平均 2.5〜4.5 階調）。
3. 未確認: GTiff / WebP の出力、`--webviewer`、`--kml`、`--tiling-scheme raster`、見た目（目視）。
