#!/bin/sh
# 既知の発見（drafts/upstream/ と knowledge/）を、いまの terrio で確かめ直す。
# 使い方: scripts/recheck_known_issues.sh /path/to/terrio   （省略時は PATH の terrio）
# 一時ファイルは mktemp の下に作り、終わりに消す。GDAL（ogr2ogr）があれば CP932 の試料を作る。
T="${1:-terrio}"
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT; cd "$W" || exit 1
echo "terrio: $($T --version)"
cat > jp.geojson <<'J'
{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":"札幌市"},"geometry":{"type":"Point","coordinates":[141.35,43.06]}},{"type":"Feature","properties":{"name":"東京都千代田区"},"geometry":{"type":"Point","coordinates":[139.75,35.69]}}]}
J
r() { if [ "$1" = ok ]; then echo "OK    $2"; else echo "KNOWN $2"; fi; }
# 1. 日本語 GeoJSON の panic（#159）
if $T convert jp.geojson jp.shp >/dev/null 2>&1 && $T convert jp.geojson jp.fgb >/dev/null 2>&1; then r ok "日本語 GeoJSON → Shapefile / FlatGeobuf（#159）"; else r known "日本語 GeoJSON が通らない（#159）"; fi
# 2. Zarr の日本語の相対パス
mkdir -p 日本語 && python3 - <<'P' 2>/dev/null
import struct
P
printf '{"zarr_format":2}' > 日本語/.zgroup
if $T info 日本語/ >/dev/null 2>&1 || ! $T info 日本語/ 2>&1 | grep -q "char boundary"; then r ok "日本語の相対パスで panic しない"; else r known "日本語の相対パスで panic（zarr.rs の t[..5]）"; fi
# 3. 南極点 → EPSG:3857
echo '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[180,-90]}}]}' > pt.geojson
if $T convert pt.geojson o.geojson --t-srs EPSG:3857 >/dev/null 2>&1; then r ok "(180,-90) → EPSG:3857"; else r known "(180,-90) → EPSG:3857 が失敗"; fi
# 4. CP932 の Shapefile（ogr2ogr があるとき）
if command -v ogr2ogr >/dev/null 2>&1; then
  ogr2ogr -f "ESRI Shapefile" cp.shp jp.geojson -lco ENCODING=CP932 >/dev/null 2>&1
  $T convert cp.shp cp.geojson >/dev/null 2>&1
  if grep -q "札幌市" cp.geojson 2>/dev/null; then r ok "CP932 の属性を読む"; else r known "CP932 の属性が文字化け"; fi
else echo "SKIP  CP932（ogr2ogr がない）"; fi
# 5. 座標変換の値（JGD2011 → 第IX系）
v=$(echo "139.767125 35.681236 50" | $T crs EPSG:6668 --to EPSG:6677 2>/dev/null | tail -1)
echo "VALUE EPSG:6668→6677: $v   （期待: -5992.919570392903 -35363.23774493004 50）"
v=$(echo "139.767125 35.681236 50" | $T crs EPSG:6667 --to EPSG:6697 2>/dev/null | tail -1)
echo "VALUE EPSG:6667→6697: $v   （0.3.2〜0.4.2: 高さ 13.2386、ジオイドを適用）"
# 6. COG の窓と warp のオプション
$T warp --help 2>&1 | grep -q -- "--dstalpha" && r ok "warp --dstalpha がある" || r known "warp --dstalpha がない"
# 7. サブコマンド
echo "CMDS  $($T --help 2>&1 | sed -n '/Commands/,/Options/p' | awk 'NR>1 && NF{printf "%s ", $1}')"
