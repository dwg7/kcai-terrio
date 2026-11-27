# 2026-11-27 点群フィルタの PDAL との比較（terrio 0.10.0・PDAL 2.10.2）

- 入力: Autzen の COPC（`hobu-lidar`）から `terrio convert URL sub2.laz --bounds 636800 851500 637500 852200` で切り出した 304,487 点（`--resolution 5` なら 44,465 点）。PDAL は `pdal translate … -f filters.<名前>`、統計は `pdal info --stats`

| フィルタ | terrio と PDAL |
|---|---|
| `crop`（`--crop-bounds "([636900,637300],[851600,852000])"`） | 99,192 点、X・Y・Z の最小・最大・平均が同じ |
| `decimation --step 10` | 30,449 点、同じ |
| `smrf`（既定） | Classification の最小 0・最大 19・平均 1.9259 が同じ |
| `pmf`（既定） | 平均 1.72111 が同じ |
| `outlier`（statistical、mean_k 8、multiplier 3） | Classification の最大 65・平均 1.50007 が同じ |
| `hag_nn`（smrf のあと） | min −130.67、max 135.56、平均 1.909036 対 1.909034（float の精度の差） |
| `dbscan`（min 6、eps 2.0） | クラスター ID の最小 −1・最大 3811・平均 931.5883 が同じ |

## 発見

1. 7 つのフィルタは PDAL と一致。
2. `filter crop --bounds …` は、エラーなしで 0 点を返す（`--bounds` は入力を読むときの絞り込み）。箱は `--crop-bounds`。
3. 追加の次元の名前が違う（terrio `height_above_ground`・`cluster_id`、PDAL `HeightAboveGround`・`ClusterID`）。terrio が書いた LAS を PDAL で処理する工程は、名前を合わせる。

## 追記: xarray の `.terrio` アクセサ（0.10.0）

`txr.open_rasterio('u.tif', masked=True).squeeze().terrio` で、`dem('hillshade')` は CLI と gdaldem に完全一致。`viewshed(466429, 4375612, oz=2, md=3000)` は CLI と完全一致（見える画素 2,498）。`zonal_stats('z.geojson', stats=[…])` は CLI と値が同じ（列名の形が違う）。`stats` に文字列を渡すとエラー（リストで渡す）。
