---
id: hfu-dwg7-workflow-substitution-survey
title: hfu と dwg7 の公開リポジトリの処理のうち、terrio で代替できそうなものと、できなさそうなもの
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、PyPI の wheel）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
interface: cli
verified_on: 2026-10-21
verified_how: read-source
as_of: 2026-10-21
sources:
  - plays/2026-10-21-japan-edge-cases-and-survey.md（5）
  - "公開リポジトリ 75 件の浅い複製（2026-10-21）。代表: hfu/kompressor、hfu/abidjan-martin、hfu/terrain2021、hfu/kitavolca、hfu/tha-adm、hfu/zip2seq、hfu/area-forecast、hfu/senrigan、dwg7/snow-hokkaido、dwg7/cafebabe、dwg7/plateau-mago-implicit"
related: [terrio-scope-included-and-excluded, shapefile-cp932-attributes-not-decoded, vertical-datum-grids-and-geoid-in-japan, cloud-native-read-behavior-matrix, terrio-possibilities-and-risks]
freshness: high
---

## 要点

hfu と dwg7 の公開リポジトリは、**タイル配信（PMTiles、Martin、MapLibre）と、それを作る前処理（ogr2ogr、tippecanoe、gdal_translate、gdalwarp）**が中心。前処理のうち、**ラスタの再投影・圧縮・窓切り出し・形式変換、ベクタの形式変換と属性の選択**は terrio で代替できる見込みがある。**タイルの生成（tippecanoe）、幾何の検査・修復（SQLite 方言の `ST_*`）、配信・表示、Shift_JIS の Shapefile、日本のジオイド**は、いまは代替できない。

**この塊は「読んで判断した」もので、置き換えの実測は一部だけ。** 実測した項目は「確かめ方」の列に `played` と書いた。

## 調べ方

- `list_repos` で見えた公開リポジトリから、地理空間に関係しそうな 75 件を `git clone --depth 1`。非公開のものは扱わない（このリポジトリが公開のため）。取得したコードは**実行していない**。
- キーワード（ogr2ogr、gdal_*、tippecanoe、pmtiles、rasterio など）で走査し、代表的なスクリプトを読んだ。数は「そのキーワードを含むリポジトリの数」で、文書への言及も含む。全部を読んだわけではない。
- 集計は `plays/2026-10-21-japan-edge-cases-and-survey.md` の 5。

## 代替できそうなもの

| 処理（リポジトリ） | いまの道具 | terrio での見通し | 確かめ方 |
|---|---|---|---|
| GeoTIFF の一括再圧縮と検証（hfu/kompressor） | `gdal_translate -co COMPRESS=ZSTD/DEFLATE/LZW/LERC_ZSTD`、`ZSTD_LEVEL`、`ZLEVEL`、predictor、`TILED`、`BIGTIFF`、検証に `gdalinfo` | `convert --compress`（ZSTD、DEFLATE、LZW ほか）と `--tile-size`、`--bigtiff`、検証は `info`。**圧縮レベル、predictor、LERC の指定はオプションに見当たらない** | read-docs（`--help`） |
| COG の作成（hfu/abidjan-martin） | `gdalwarp -t_srs EPSG:3857 -r bilinear -dstalpha -co TILED -co COMPRESS=LZW` → `gdal_translate -of COG -co TILING_SCHEME=GoogleMapsCompatible …` | `warp`（`--t-srs`、`-r`、`--tr`）は動いた。**`--dstalpha` に当たるオプションが `--help` にない**。COG の `TILING_SCHEME=GoogleMapsCompatible` などは**未確認**（4×4 の入力では判別できなかった） | warp は played、COG オプションは未確認 |
| 航空写真のラスタタイル（dwg7/cafebabe の pattern） | `gdalwarp` → MBTiles(WebP) → `gdaladdo` → `pmtiles convert` | `convert … out.pmtiles --co TILE_FORMAT=WEBP` で一段にできる**はず**（ドキュメント） | 未試験 |
| ベクタの形式変換と列の選択（hfu/tha-adm、zip2seq、area-forecast、kitavolca） | `ogr2ogr -f GeoJSONSeq /vsistdout/ in.shp -select …`、`/vsizip/` | `convert --select`、`-f GeoJSONSeq`、zip 内（`a.zip!x.shp` や `/vsizip/`）は可（ドキュメント）。**出力は `/vsistdout/` が使えず、`/dev/stdout` で代用**。UTF-8 の日本語は通る | stdout は played |
| rasterio による窓読み・ラスタ化（dwg7/snow-hokkaido） | `rasterio.open`、`windows.from_bounds`、`features.rasterize`、`transform.from_origin`、`sample`、`Resampling` | `terrio.rio`（rasterio 互換）に `windows` `features` `transform` `enums` があり、import はできた。**動作の同等性は未確認** | import だけ played |
| 座標の変換（pyproj が 3 リポジトリ。JGD2011 や平面直角座標系の言及は 16 リポジトリ） | pyproj、GDAL | `terrio crs`、`warp`、`--t-srs`。**水平方向は JGD2011 ↔ 平面直角で動いた**。旧日本測地系・JGD2000 の格子補正はなし | played（`jgd2011-plane-rectangular-transform`） |
| クラウドのデータの確認（PMTiles、COG の `info`） | `pmtiles show`、`gdalinfo /vsicurl/` | `terrio info URL`。Range が効く配信なら小さな転送で済む。Range を無視する配信では全体を読む（要 `timeout`） | played |

## 代替できなさそうなもの

| 処理（リポジトリ） | 理由 |
|---|---|
| ベクタタイルの生成（tippecanoe が 20 リポジトリ。`-zg`、`--drop-densest-as-needed`、`--extend-zooms-if-still-dropping`、`--no-tile-size-limit` など） | terrio は GeoJSON → ベクタ PMTiles を**書ける**（400 四角形で確認）が、書き方は GDAL の MVT ライタ相当。tippecanoe の「タイルのサイズに合わせて地物を間引く・ズームを延ばす」方針の代わりにはならない。大きなデータでの比較は未実施 |
| 幾何の検査・修復（hfu/terrain2021: `-dialect SQLite -sql "… ST_IsValid(Geometry)=0 …"`、unary union、面積によるズーム決定） | `--sql` は OGR SQL の部分集合で、`ST_*` を含む SQL は `SQL: expected FROM` で失敗。幾何アルゴリズムは範囲外と明言されている。`--skipfailures` もない |
| Shift_JIS の Shapefile（hfu/kitavolca の `SHAPE_ENCODING CP932`） | **黙って文字化けする**（`shapefile-cp932-attributes-not-decoded`） |
| 日本のジオイド補正（dwg7/plateau-mago-implicit。JGD2011 と GSIGEO2011 を扱う） | terrio では高さが変わらなかった（`vertical-datum-grids-and-geoid-in-japan`） |
| タイルの配信と表示（Martin が 45、MapLibre が 54、`pmtiles serve`） | terrio はサーバーでも描画でもない |
| 動的なタイル作成（rio-tiler: hfu/senrigan） | 同上 |
| 大きな GeoParquet の部分読みと分析（DuckDB が 5 リポジトリ） | terrio の GeoParquet は全量取得（656 MiB を実測）。分析は DuckDB / GeoParquet のほうが向く |
| `gdal` 統合 CLI（GDAL 3.11 以降）や、GDAL の長い尾の形式 | 範囲外。GDAL バックエンドは PyPI の wheel に入っていない |

## 気をつけること

- 「代替できる」は、**置き換えて同じ成果物が出る**ことまでは確かめていない。置き換えるなら、1 つのスクリプトずつ、GDAL の出力と差分を取る（この遊びの方針の外。別の作業として）。
- 日本語のファイル名・属性は、現状の 0.3.2 では **panic と文字化けの地雷**がある（`japanese-path-panic-in-zarr-parse-name`、`geojson-japanese-string-panic`、`shapefile-cp932-attributes-not-decoded`）。置き換えの前に避け方を決める。
- 調べたのは公開リポジトリだけで、一覧も途中で切れている。非公開の処理は含まない。

## 出典

- plays/2026-10-21-japan-edge-cases-and-survey.md
- 各リポジトリ（github.com/hfu/…、github.com/dwg7/…。2026-10-21 時点の `main` の浅い複製）
