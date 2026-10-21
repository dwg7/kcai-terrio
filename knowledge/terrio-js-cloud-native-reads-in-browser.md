---
id: terrio-js-cloud-native-reads-in-browser
title: ブラウザ（WebAssembly）で terrio を使う：openUrl の範囲読み込みと、このリポジトリのページ
status: draft
terrio_version: 0.3.2
terrio_commit: a08e7d8b4b5a29304cbf6cf050b9ccc87ea516e6
interface: wasm
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - plays/2026-10-21-untested-items.md（4）
  - terrio-js@0.3.2 の terrio.d.ts（openUrl、RemoteDataset）、docs/javascript.md
  - docs/index.html（このリポジトリのページ）
related: [cloud-native-read-behavior-matrix, pmtiles-remote-reading, geojson-japanese-string-panic, terrio-possibilities-and-risks]
freshness: high
finding:
  - wasm-reads-flatgeobuf-and-geoparquet-by-range-cli-does-not
---

## 要点

**terrio-js の `openUrl(url, {})` は、COG・PMTiles・COPC・FlatGeobuf・GeoParquet を HTTP の Range で範囲読みする。** CLI / Python では全量取得だった FlatGeobuf と GeoParquet も、WebAssembly 版では必要な部分だけ読む（14 MB の FlatGeobuf を bbox で読んで 768 KiB、**5 GB の GeoParquet から東京駅周辺の 119 棟を 16.4 MiB**）。実 Chromium で、試した 6 つの配信先すべてが CORS を通った。データを取りに行くのは利用者のブラウザなので、このセッションの通信の制限に縛られない。

## やり方

```html
<script type="module">
import init, * as T from "https://cdn.jsdelivr.net/npm/terrio-js@0.3.2/terrio.js";
await init();                                   // wasm は 20 MB（配信時は圧縮される）
const d = await T.openUrl(url, {});             // ヘッダーだけ取る
d.info(); d.stats();                            // { requests, bytes }
await d.readBand(1, new Uint32Array([5000, 5000, 256, 256]));   // ラスタの窓
const r = await d.read({ bbox: [139.760, 35.676, 139.770, 35.686] }); r.toGeoJSON();  // ベクタ
</script>
```

動くページは `docs/index.html`（ビルドなし、版を固定）。GitHub Pages で公開するには、リポジトリの Settings → Pages → Branch を `main` / `/docs` に設定する（**hfu の操作が要る**）。公開後の URL は `https://dwg7.github.io/kcai-terrio/` のはず（未確認）。

## 確かめたこと（何をして、何が起きたか）

| 対象 | 操作 | 要求 | 受信 |
|---|---|---|---|
| Sentinel-2 COG（216 MB） | 256² の窓 | 3 | 6.2 MiB（Chromium の測定で 6,488,064 バイト） |
| PMTiles ラスタ（30.5 GB、Protomaps） | `info` | 12 | 832 KiB |
| PMTiles ベクタ（depot.optgeo.org、2.2 MB） | `info` | 1 | 64 KiB |
| FlatGeobuf（14 MB） | `read({bbox})`、82 地物 | 4 | 768 KiB |
| COPC（81 MB） | `info` | 2 | 118 KiB |
| GeoParquet（5 GB、日本の建物） | `read({bbox})`、119 棟 | 7 | 16.4 MiB、約 4.5 秒（Chromium）〜 10 秒（Node） |

- Node 22 と実 Chromium（Playwright、プロキシと CA は環境の設定）の両方で、同じ要求数と受信量だった。Chromium では、ページを `http://127.0.0.1` から配り、配信先はすべて別オリジン。
- `transformPoints` で JGD2011 → 第IX系は、CLI と同じ `-5992.9196, -35363.2377`。
- **日本語の長い文字列の panic も WebAssembly で再現**（`RuntimeError: unreachable`）。GeoJSON `東京都千代田区` と CSV。`札幌市北区` は通る。トラップのあとも、同じモジュールで他の呼び出しは動いた（`geojson-japanese-string-panic`）。
- `docs/javascript.md`（0.3.2）に `openUrl` の説明はなく、型定義にだけある。

## 気をつけること

- 試した配信先は、`Range` を許可していた。`Content-Range` を公開していない配信先（Sentinel の S3、depot、flatgeobuf.org）でも動いた（なぜかは未確認。`Content-Length` などで足りているのかもしれない）。**CORS が違う配信先では失敗しうる**。ページは失敗を画面に出す。
- 大きなベクタの bbox 読みは、行グループの統計で飛ばすため、**データの作り次第**: 5 GB の日本の建物（行グループ約 5,000 行）は 16 MiB で済んだが、Hugging Face の 430 MB の GeoParquet は**行グループが 1 つで統計がなく、bbox 読みでも約 394 MiB（ほぼ全体）を読んだ**（0 件だった理由は未確認。`info` に CRS が出ないので、bbox の座標系が合っていたかも分からない）。
- `cacheSize` の既定が 256 MB（メモリ）。大きな窓や点群は、ブラウザのメモリに注意。
- 版を上げたら、この踏み跡と `docs/index.html` の `PINNED` を確かめ直す。
- wasm の読み込みが約 20 MB（圧縮前）。モバイルでは重い。

## 出典

- https://www.npmjs.com/package/terrio-js 、https://cdn.jsdelivr.net/npm/terrio-js@0.3.2/terrio.d.ts
- plays/2026-10-21-untested-items.md
- docs/index.html
