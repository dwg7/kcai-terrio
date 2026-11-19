# 2026-11-19 MapLibre での見え方の比較（terrio 0.9.0・tippecanoe 2.49.0・GDAL 3.8.4 の MVT）

- 方法: 同じ入力（国界の多角形 179、その輪郭線 284、乱数の 6 万点）から、terrio（`convert -f MVT`）、tippecanoe（`-e --no-tile-compression`）、GDAL（`ogr2ogr -f MVT`）で XYZ のタイルのディレクトリを作る。MapLibre GL JS 4.7.1 を実 Chromium（SwiftShader）で動かし、800×600 で同じスタイル・カメラで描いて、画素を比べた。タイルの配信は小さなサーバー（gzip のタイルに `Content-Encoding: gzip` を付ける）
- タイル数: 多角形・線とも 3 者で同じ（559・512）。サイズも近い（多角形 264 KB・256 KB・259 KB）

## 結果

| 見え方 | terrio と GDAL の MVT | terrio と tippecanoe |
|---|---|---|
| 国界の多角形 z1・z3・z5 | 画素差 0.00%（同一） | 0.02%・0.01%・0.00% |
| 輪郭線 z3・z5 | 0.00% | 0.01%・0.00% |
| 6 万点 z4 | （比較せず） | 暗い画素 10,480 対 5,432（描く地物 60,000 対 3,840） |
| 6 万点 z6 | （比較せず） | 80,987 対 56,704（60,000 対 23,998） |
| 6 万点のタイル合計 | — | 3.4 MB 対 1.2 MB（`--drop-densest-as-needed` でも同じ） |

## 発見

1. 多角形と線は、terrio の描画が GDAL の MVT と画素まで同一で、tippecanoe ともほぼ同じ。**dwg7 の多角形・線の PMTiles の見た目は、tippecanoe と変わらない**。
2. 点は、terrio が全点を入れるので、密集部が塗りつぶされ、タイルも約 3 倍重い。間引きが要る点データ（建物の重心など）は、まだ tippecanoe に分がある。
3. MapLibre は gzip の `.pbf` に `Content-Encoding: gzip` を要求する。
