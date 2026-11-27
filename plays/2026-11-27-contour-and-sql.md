# 2026-11-27 等高線と SQL の空間関数の GDAL との比較（terrio 0.10.0・GDAL 3.13.3）

## 等高線（USGS 3DEP の窓 300×300 を UTM 13N・30 m に warp した DEM）

| 設定 | terrio | `gdal_contour` |
|---|---|---|
| `-i 25 -a ELEV` | 184 本・32,753 頂点・761,126.84 m・36 レベル | 同じ（等高線ごとの長さの最大差 0） |
| 固定の高さ 2600・2800・3000 | 18 本・3,691 頂点・85,401.18 m | 同じ |
| `-i 25 --offset 10` | 188 本・32,945 頂点・763,922.99 m | 同じ |
| `--3d -i 50` | 90 本（3D の線） | 90 本（並びが違う。最初の線の標高は terrio 2400、GDAL 2900） |

## SQL（5 か国の多角形）

terrio の `sql` と、GDAL の `-dialect sqlite`（SpatiaLite）の同じ問い合わせ。

| 関数 | 差 |
|---|---|
| `ST_Area` | 13 桁以上一致（954.6355002133428 など） |
| `ST_Length`（線 5 本） | 完全一致 |
| `ST_Area(ST_Buffer(geometry, 0.5))` | 相対差 9.8e-10 |
| `ST_Area(ST_Transform(geometry, 3857))` | 相対差 5e-16 |
| `ST_Centroid` | 2e-13° |
| `ST_GeomFromText(...)` | **terrio は未対応**（`unsupported function`） |
| `ST_Intersects(geometry, 'POLYGON(...)')` | **terrio は 2 つの幾何を要求**（リテラルの WKT は不可） |

## 発見

1. 等高線は GDAL と完全一致。dwg7 が `gdal_contour` で作る等高線は、terrio で置き換えられる見込みが高い。
2. SQL の空間関数は、使える範囲では SpatiaLite と一致。リテラルの幾何で絞り込む問い合わせ（`ST_Intersects` と `ST_GeomFromText`）はまだ書けない。
3. オプション名: `contour` の属性名は `-a`/`--field`。
