# 2026-10-21 first contact

- 日付: 2026-10-21
- terrio: 0.3.2（`pip install --upgrade terrio` で入った最新。PyPI 配布物）
- ソースの参照: opengeos/terrio の main（コミット `cf6bd5dbcb6021f99ffde6c7f2c0f4f3f311ed2b`、Cargo.toml の版も 0.3.2）。ドキュメントはこの `docs/` を読んだ
- 環境: Claude Code クラウドセッション、Linux 6.18 x86_64、Python 3.13.16、ディスク空き 約 30 GB
- 転送量の測り方: コマンド前後の `/proc/net/dev`（lo 以外）の受信バイトの差。HTTP の要求は `TERRIO_HTTP_LOG=YES` で見た。**転送量は概数**（TLS やプロキシの上乗せを含む）
- 一時ファイルはすべてリポジトリ外（`/tmp/work`）に置いた

## 1. インストールと概観

- `terrio --version` → `terrio 0.3.2`。依存として `affine 3.0.1` も入った
- `terrio --help`: 15 のサブコマンド（info, convert, formats, crs, rasterize, polygonize, translate, warp, mosaic, dem, calc, proximity, sieve, grid, filter）。**`mcp` は `--help` の一覧に出ない**（ドキュメントの cli.md には載っている。未確認: 0.3.2 に `terrio mcp` があるか）
- `terrio formats`: 約 50 行。ラスタ・ベクタ・点群。COG, PMTiles, MBTiles, GeoParquet, FlatGeobuf, Zarr, STACIT などを含む。HFA / HDF5 / OSM / EPT / STACIT は読み取りのみ
- Python: `import terrio` で `open_raster`, `open_vector`, `warp`, `translate`, `calc`, `dem` などの関数。`PanicException` は `BaseException` 系（下の発見 4）

## 2. 配信先に届くか

プロンプトでは「どれにも届かない」とあったが、**2026-10-21 のこのセッションでは、すべて届いた**。いずれも本物の応答（JSON / XML / HTML）を確認した。

| 配信先 | 結果 | 備考 |
|---|---|---|
| data.source.coop | 届いた（200, JSON） | Source Cooperative Data Proxy v2.5.1。データ本体は未試験 |
| sentinel-cogs.s3.us-west-2.amazonaws.com | 届いた | Range 可。COG を試した |
| earth-search.aws.element84.com/v1 | 届いた | STAC API。検索（POST）も可 |
| overturemaps-us-west-2.s3.amazonaws.com | 届いた | 一覧も取得可。GeoParquet を試した |
| stars.optgeo.org | 届いた | **Martin のタイル配信**（`/{source}/{z}/{x}/{y}`）で、`.pmtiles` の直リンクではない。`/catalog` に 44 のタイル源 |
| depot.optgeo.org | 届いた | Caddy のファイル一覧。**`.pmtiles` の実体**がある。CORS `*`。下の発見 5 |
| huggingface.co | 届いた（トップのみ） | データセットは未試験 |
| cdn.jsdelivr.net / registry.npmjs.org / unpkg.com | 届いた（unpkg は 302） | terrio-js を CDN から読める見込み |
| pypi.org, raw.githubusercontent.com, terrio.opengeos.org | 届いた | |
| github.com | git clone は可。curl の Range 付きページ取得は 403 | git のプロキシ経由なら読める |
| r2-public.protomaps.com | 届いた | terrio のドキュメントのサンプル（30 GB の PMTiles） |

## 3. 遊び

### 3.1 COG（Sentinel-2 L2A、東京周辺、54SUE、2026-10-18）

Earth Search で東京の範囲（bbox 139.6,35.6,139.9,35.8）を検索し、B04（10980×10980、UInt16、EPSG:32654、ファイル 216,253,355 バイト）を使った。

| コマンド | 受信 | 結果 |
|---|---|---|
| `terrio info URL` | 約 78 KiB | 0.6 秒。サイズ、CRS、overview（5490, 2745, 1373, 687）が分かる |
| `convert URL --srcwin 5000 5000 256 256` | 約 6.4 MiB | 要求 3 回 |
| `convert URL --srcwin 5000 5000 1024 1024` | 約 6.4 MiB | **窓が 256 でも 1024 でも同じ**（タイルの粒度。窓がタイル境界をまたぐ） |
| `translate URL --srcwin 5000 5000 512 512` | 約 6.4 MiB | 同上 |
| `convert URL --overview 2` | 約 2.6 MiB | 1373×1373 |
| `convert URL --overview 4` | 約 75 KiB | **失敗**: `no overview 4: the raster has 4 overview(s)`。**0 始まり**で 0〜3 |
| `convert URL --overview 0` | — | 5490×5490（**0 は全解像度ではなく最初の overview**） |
| `translate URL --outsize 512 512` | **約 208 MiB** | **ほぼ全量を取得**。overview を使わない（ドキュメントの gdal.md に明記: 縮小は全解像度を読む） |
| `translate URL --outsize 512 512 -r average` | 約 208 MiB | 同上 |
| `warp URL --t-srs EPSG:6677 --te -10000 -40000 0 -30000 --te-srs EPSG:6677 --tr 10 10 -r bilinear` | 約 6.1 MiB | JGD2011 / 第IX系の 10 km 四方。1000×1000 |

### 3.2 PMTiles

| 対象 | コマンド | 受信 | 結果 |
|---|---|---|---|
| protomaps terrarium_z9（30.5 GB、ラスタ） | `info` | 約 0.84 MiB | 131072×130644、3 バンド、overview 9 段 |
| 同上 | `convert --srcwin 30000 45000 512 512` | 約 1.3 MiB | 512×512 の GeoTIFF |
| depot.optgeo.org/ksj_n03_hkd.pmtiles（2.2 MB、ベクタ） | `info` | 約 1.5 MiB | MultiPolygon 3625、属性 6 つ。EPSG:3857 と表示 |
| 同上 | `convert --oo ZOOM_LEVEL=8 --spat 141.2 42.9 141.5 43.15 --spat-srs EPSG:4326 → sap.geojson` | 約 278 KiB | 22 地物。`札幌市北区` など**日本語の属性は正しい** |
| depot.optgeo.org/mapterhorn-japan-bridge.pmtiles（275 GB、標高） | `info` | **120 秒で 1.2 GiB、未完了** | 発見 5 |

### 3.3 GeoParquet（Overture places、part-00000、680,811,676 バイト）

- `terrio info URL` → **約 656 MiB を受信**してから結果（Features 5,120,674、Point、EPSG:4326）。範囲読み込みではなくファイル全体の取得。ドキュメント（remote-data.md）の「その他の形式は一時ディレクトリに先に取得」と合う。一時ファイルは終了後に残っていなかった

### 3.4 座標系（日本）

`terrio crs EPSG:xxxx` で、6668（JGD2011）、6669〜6685（平面直角 I〜XVII）、4612（JGD2000）などの名前が引ける。東京駅（経度 139.767125、緯度 35.681236）で変換した。

| 変換 | 入力 → 出力 |
|---|---|
| 6668 → 6677（第IX系） | `139.767125 35.681236` → `-5992.9196 -35363.2377`（東西 x、南北 y） |
| 4326 → 6677 | 同じ値（terrio は 6668 と 4326 を同じ扱いにしたように見える。差は cm〜dm のはずだが未確認） |
| 6677 → 6668 | `-4000 -4000` → `139.78898532 35.96393874` |
| 6668 → 6677、**緯度・経度の順** `35.681236 139.767125` | **失敗**: `cannot transform` |
| 4612（JGD2000）→ 6668 | **値が変わらない**（`139.767125 35.681236`） |
| 4301（Tokyo Datum）→ 6668 | `139.76389102 35.68447488`（約 0.0032° / 0.0033°、約 300〜400 m のずれ。向きと量は既知の旧測地系のずれと矛盾しない） |

### 3.5 日本語を含む GeoJSON

発見 1。

## 4. 発見（要約。詳細は踏み跡と下書き）

1. **日本語（7 文字以上）の文字列属性を含む GeoJSON を開くと panic する**（`geojson.rs:275`、`is_datetime` の `&s[..10]`）。`info`、`convert`、Python の `open_vector` のどれでも。`札幌市北区` は通り、`東京都千代田区` は落ちる。再現は最小（1 地物）
2. **GeoParquet の `info` が 656 MiB を全部取得する**。範囲読み込みを期待すると落とし穴
3. **`translate --outsize` / `warp` の縮小は、リモート COG をほぼ全量取得する**（208 MiB）。縮めたいときは `convert --overview N`（0 始まり、0 は最初の縮小版）
4. **Python の `PanicException` は `BaseException` 系**で、`except Exception` では捕まらない
5. **depot.optgeo.org は、大きいファイル（783 MB と 275 GB）で `Range` を無視して 200 で全体を返す**。小さいファイル（〜8 MB）は 206。terrio はそれを受けて全体を読み続けた（`TERRIO_HTTP_TIMEOUT` は既定でなし）。terrio の不具合ではなく配信側の挙動（`cf-cache-status: BYPASS`、Cloudflare 経由）。藤村さんへの報告事項
6. 通信の許可リストは、プロンプトの記述より広かった（すべて届いた）

## 5. まだ試していないこと（次回）

- `terrio mcp`（MCP サーバー）、WebAssembly 版（terrio-js）、Python API の遅延読み込み（`lazy=True`）
- STACIT（`STACIT:"search-url":asset=red`）、Zarr、FlatGeobuf・COPC のリモート
- `dem`, `calc`, `rasterize`, `polygonize`, `proximity`, `sieve`, `grid`, `filter`
- Source Cooperative のデータ本体、Hugging Face のデータセット
- 日本語のシェイプファイル（文字コード、`.cpg`）、Mapterhorn の日本標高の小さな窓（Range が効く経路が必要）
