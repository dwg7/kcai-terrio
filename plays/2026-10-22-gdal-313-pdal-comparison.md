# 2026-10-22 GDAL 3.13.3 と PDAL 2.10.2 との突き合わせ

- 日付: 2026-10-22。terrio 配布版 0.3.2（一部は 2026-10-21 のビルドの結果を参照）
- 道具: micromamba で conda-forge から `libgdal-core>=3.12`、`gdal`、`pdal` を入れた（hfu の許可。通信は届いた）。**GDAL 3.13.3**（2026-08-13）、**PDAL 2.10.2**。terrio の基準（GDAL 3.12）より新しい。この GDAL のビルドには Parquet / PMTiles ドライバーが無い
- 一時ファイルは `/tmp/work`（終わりに消す）

## 結果

| 項目 | terrio 0.3.2 | GDAL 3.13.3 / PDAL 2.10.2 | 判定 |
|---|---|---|---|
| 南極点（180,−90）→ EPSG:3857 | 失敗 | `ogr2ogr` は成功（20037508.34, −242528680.94） | 差が残る（下書きを維持） |
| `translate -ot Int16`、nodata −999999 | −999999 のまま | **同じく −999999 のまま、警告なし**（3.8.4 だけ −32768 に丸めて警告） | **同じ。下書きを取り下げ** |
| COG `TILING_SCHEME=GoogleMapsCompatible` | 黙殺（12.32 m） | 9.5546 m に整列 | 差が残る |
| `warp --dstalpha` | 引数なし | `gdalwarp -dstalpha` で 2 バンド（アルファ） | 差が残る |
| CP932 の Shapefile 属性 | 文字化け（`.cpg=CP932` でも） | `札幌市` | 差が残る |
| 3 次元 `EPSG:6667 → 6697`、高さ 50 | 13.2386（JPGEO2024） | ネットワークなし: 不変 / `PROJ_NETWORK=ON`: 13.3375（GSIGEO2011） | 格子の違いは既知。適用はどちらも可 |
| **COPC**（terrio が書いた 44,465 点） | 点数・範囲・分類の統計 | PDAL: 同じ点数、範囲、`Classification` の最小・最大・平均が一致 | **一致** |
| `filter range`（`Classification[2:2],Z[450:460)`、`Z[500:)`、`ReturnNumber[2:3]`） | 1313 / 6720 / 379 点 | `filters.range` も 1313 / 6720 / 379 点。`Classification[2:2]` は 15,513 点で Z の平均も一致 | **一致** |
| **STACIT**（東京の検索結果、`asset=red`、窓 512²） | 10980×10980、EPSG:32654、原点・画素サイズ同じ | GDAL の STACIT ドライバー: 同じ大きさ。窓の画素は **完全一致**（`max_items=1` も一致） | **一致** |

## 発見

- **GDAL の版で挙動が違う**ことがある（`-ot Int16` の nodata）。上流へ出す主張は、**新しい GDAL でも確かめてから**にする。これで 1 件を投稿前に取り下げた（先の 2 件と合わせて 3 件）。
- 南極点、`TILING_SCHEME`、`--dstalpha`、CP932 は、新しい GDAL でも差が残る（下書きを維持）。
