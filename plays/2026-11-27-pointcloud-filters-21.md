# 2026-11-27 点群の他のフィルタ 21 種の PDAL との比較（terrio 0.10.0・PDAL 2.10.2）

- 入力: Autzen の COPC から `terrio convert URL sub.laz --bounds 636900 851600 637100 851800` で切り出した 21,434 点
- 方法: `scripts/compare_pointcloud_filters.py sub.laz`（terrio の `filter <名前>` と `pdal translate -f filters.<名前>`、PDAL は `--writers.las.extra_dims=all`。追加の次元は小文字・下線なしで照合し、点数と最小・最大・平均を 1e-6 以内で比べる）。12 秒

## 結果

21 種すべて一致: `lof`（4 次元）、`nndistance`（2）、`radialdensity`（2）、`reciprocity`（2）、`eigenvalues`（4）、`covariancefeatures`（5）、`normal`（5）、`approximatecoplanar`（2）、`estimaterank`（2）、`skewnessbalancing`、`iqr`（17,931 点）、`mad`（17,885 点）、`csf`、`elm`、`hag_delaunay`（2）、`head`・`tail`（各 1,000 点）、`sort`、`voxeldownsize`（11,525 点）、`voxelcenternearestneighbor`（11,468 点）、`sample`（6,100 点）。

比べられなかった: `zsmooth`（terrio・PDAL とも出力の次元に `Z` を使えない。新しい次元への書き出しが要る）。

## 発見

1. 点群フィルタは、前回の 7 種と合わせて 28 種が PDAL と一致。terrio の「PDAL と同じ答え」の主張が、点群でも裏づけられた。
2. 引数の名前が揃っていない（`sort --dimensions`、`zsmooth --dim`、`iqr --dimension`）。
3. 比較のスクリプトをリポジトリに足した（再利用できる）。
