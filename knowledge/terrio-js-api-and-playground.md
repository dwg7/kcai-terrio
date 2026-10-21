---
id: terrio-js-api-and-playground
title: terrio-js の API と、公式プレイグラウンド：Node とブラウザで動かして確かめた
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: wasm
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16、Node 22、Chromium 1194）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - terrio docs/javascript.md、docs/playground.md、docs/javascripts/playground.js（main 6779102）
  - terrio-js@0.3.2 の terrio.d.ts、https://terrio.opengeos.org/playground/
  - plays/2026-10-21-license-and-basics.md
related: [terrio-js-cloud-native-reads-in-browser, geojson-japanese-string-panic, vertical-datum-grids-and-geoid-in-japan, terrio-formats-rasters-and-compression]
freshness: high
---

## 要点

`terrio-js`（npm、WebAssembly）は、**バイト列から開き、バイト列へ書く**。関数は `open`、`openUrl`（範囲読み）、`openZarr`、`openPoints`/`readPoints`、`fromGeoJSON`、`fromArrowIPC`、`rasterFromArray`、`pointsFromArrays`、`transformPoints`、`describeCrs`、`registerGrid`、`drivers`、`version`、操作（`warp` `translate` `mosaic` `rasterize` `polygonize` `dem` `calc` `proximity` `sieve`）。**正しい呼び出しなら、確かめた操作はすべて動いた**。公式のプレイグラウンドも動くが、**日本語の長い文字列の GeoJSON では `unreachable`（panic）になる**。

## やり方

```js
import init, * as T from "https://cdn.jsdelivr.net/npm/terrio-js@0.3.2/terrio.js";
await init();                                                  // Node では init({ module_or_path: fs.readFileSync(wasmPath) })
const ds = T.open(bytes, "a.geojson");                         // ファイル名が形式を決める
ds.info(); ds.toGeoJSON(); ds.toBytes("a.fgb", { tSrs: "EPSG:3857", where: "lanes > 2" });
const r = T.rasterFromArray(new Float32Array(64*64), 64, 64, new Float64Array([0,1,0,64,0,-1]), "EPSG:32654", -9999);
T.dem(r, "hillshade", {}); T.calc("A*2", { A: r }, {}); T.warp(r, { tSrs: "EPSG:4326" });
T.transformPoints([139.767125], [35.681236], "EPSG:6668", "EPSG:6677");   // → -5992.9196, -35363.2377
T.registerGrid("us_nga_egm96_15.tif", gridBytes);                          // 格子をバイトで渡す（ファイルシステムがない）
```

## 確かめたこと（何をして、何が起きたか）

**Node（played、15 件中 14 件、残りは呼び出し方の誤り）**: `open`（GeoJSON のバイト）、`toGeoJSON`、`toBytes`（FlatGeobuf に `tSrs` と `where`、GeoPackage、KML）、`toArrowIPC`（GeoArrow）、`fromGeoJSON`、`describeCrs("EPSG:6677")`（"JGD2011 / Japan Plane Rectangular CS IX"）、`transformPoints`（JGD2011 → 第IX系が CLI と同じ値）、`drivers()`（49）、`version()`（0.3.2）。`rasterFromArray`（引数は `data, width, height, transform, crs, nodata`）から COG のバイト（1,795 バイト、64×64、float32、EPSG:32654）を作り、`open` で読み戻せた。`warp`（EPSG:4326）、`dem`（`hillshade` は uint8、`slope` は float32）、`calc`（`A*2`）、`translate`（`srcwin`）、`proximity`、`sieve`、`mosaic`、`polygonize` も動いた。
- **呼び出し方を誤ると、型エラーではなく WASM のトラップ**になる: `T.dem(b, {mode:'hillshade'})`（文字列の位置にオブジェクト）が `RuntimeError: memory access out of bounds`。`rasterFromArray` を別の引数順で呼ぶと `TypeError`。
- **EGM96**（`registerGrid` に `cdn.proj.org` の `us_nga_egm96_15.tif` を渡す）: `transformPoints([-100],[40],'EPSG:4979','EPSG:4326+5773',[100])` が高さ 125.05（適用される）。
- **日本のジオイド**: `registerGrid` に `jp_gsi_gsigeo2011.tif` を渡し、**3 次元の `EPSG:6667` → `EPSG:6697`、高さ 86.7 で 50.03747748404898**（GDAL 3.8.4 と一致）。JPGEO2024 も登録すると 49.9386（新しいほうを優先）。**2 次元の `EPSG:6668` では 86.7 のまま**（GDAL も同じ。当初、これを「適用されない」と誤解した。`vertical-datum-grids-and-geoid-in-japan`）。
- **公式のプレイグラウンド（実 Chromium、https://terrio.opengeos.org/playground/）**: 版は 0.3.2 を固定（`playground.js` の `VERSION`）。起動 "terrio 0.3.2 is ready"。サンプルの国界の GeoJSON が開き（`countries`、MultiPolygon、179 地物）、出力形式は GeoJSON、FlatGeobuf、GPKG、KML、KMZ、GML、GPX、TopoJSON。座標変換の欄で JGD2011 → 第IX系が `-5992.919570392903, -35363.23774493004`。**日本語の長い文字列（`東京都千代田区`）の GeoJSON を渡すと `Could not open jp_long.geojson: unreachable`**（コンソールに `geojson.rs:275` の panic）。修正（#161）は main にあり、**プレイグラウンドは 0.3.2 固定なので、次のリリースまで直らない**。
- **`docs/javascript.md` に `openUrl` の説明がない**（型定義とロードマップにはある）。`docs/javascript.md` の例は `registerGrid` と `transformPoints` を含む。

## 気をつけること

- ブラウザ・Node で使う前に、**引数の型と順**を `terrio.d.ts` で確かめる（誤ると原因の分かりにくいトラップ）。
- WASM のバイナリは 20 MB（配信は圧縮される）。ロードマップの未完了: 自前の FlatGeobuf 読み取り、スレッド、サイズの縮小、4 GB 超（`terrio-roadmap-and-open-items`）。
- プレイグラウンドはデータを送信しない（ブラウザの中だけ）。

## 出典

- https://terrio.opengeos.org/javascript/ 、https://terrio.opengeos.org/playground/
- https://cdn.jsdelivr.net/npm/terrio-js@0.3.2/terrio.d.ts
- plays/2026-10-21-license-and-basics.md
