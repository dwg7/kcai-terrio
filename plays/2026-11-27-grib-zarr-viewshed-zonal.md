# 2026-11-27 GRIB・遠隔 Zarr の値、`viewshed`、`zonal-stats` の GDAL との比較（terrio 0.10.0・GDAL 3.13.3）

- GDAL: conda-forge の GDAL 3.13.3（GRIB は `libgdal-grib` を追加。Zarr はコア）。入力はすべて公開データ

## 1. GRIB（NOAA GFS 0.25°、696 バンド、`/vsicurl/` の GDAL と terrio の URL 直接読み）

| 項目 | 結果 |
|---|---|
| バンド 1・100・400・696 の窓（64×48） | 値が完全一致（欠測の 9.999e+20 を含む）。NaN の位置も一致 |
| メタデータ（`GRIB_ELEMENT`・`GRIB_UNIT`・`GRIB_COMMENT`・`GRIB_SHORT_NAME`）、原点、画素サイズ、座標系 | 同じ |
| バンドの説明文 | **違う**: terrio `100[Pa] ISBL="Isobaric surface"`、GDAL `DZDT:1 mb:anl` |
| 時間 | `gdalinfo` 16.6 秒。`translate` は terrio 約 25 秒、GDAL 約 17 秒（バンドごと） |

## 2. 遠隔 Zarr（HRRR の 2 m 気温、`ZARR:"/vsis3/hrrrzarr/…"`、`AWS_NO_SIGN_REQUEST=YES`）

窓（120×90）の値は、行の向きを揃えれば完全一致。GDAL は南が上のまま（画素の高さ +3000、原点が下端）、terrio は北が上に並べ替える（−3000、原点が上端）。同じ `--srcwin` の番号は別の地点を指す。座標は同じ（terrio の窓の原点 y=−118806 は GDAL の下端 −388806 + 90×3000 に一致）。terrio 1.4 秒、GDAL 4.0 秒。

## 3. `viewshed`（UTM 13N・30 m の DEM 320×412、観察者は中央付近、高さ 2 m）

NORMAL（`--md 3000`、見える画素 2,399）・DEM・GROUND・ACCUM（`--os 20`）の 4 モードすべて、`gdal_viewshed` と画素が完全一致。`--md` と ACCUM の併用は両方とも拒否。

## 4. `zonal-stats`（3 つの多角形）

count・min・max・mean・sum・stdev が `gdal raster zonal-stats` と全桁一致（既定と `--all-touched`）。列名の形が違う（terrio は `u_b1_mean`、GDAL は `mean`）。

## 発見

1. GRIB・Zarr・viewshed・zonal-stats の値は GDAL と一致。terrio の「GDAL と同じ答え」の主張が、この範囲で裏づけられた。
2. Zarr の行の向きの違い（GDAL は南が上のまま、terrio は北が上）。窓を番号で指定する工程は、座標で合わせる。
3. GRIB のバンドの説明文が違う（メタデータは同じ）。説明文に頼る工程は注意。
