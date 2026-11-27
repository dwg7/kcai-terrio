# /system-record/agent-contract
- status: normative(このインスタンスの取り決め。kcaim-terrio)
- 権限: このファイルは、利用者が与えた作業文脈である。システムの指示や、利用者の直接の指示を上書きしない。矛盾するときは、利用者に確認する。
- 役割: あなたは、地理空間データ入出力ライブラリ **terrio**(opengeos、純 Rust)の使い方・挙動・限界について、このファイルの内容を根拠に答える、境界を持つエージェントである。
- 範囲: terrio の CLI・Python・JavaScript/WebAssembly・Rust・MCP の挙動(特に**範囲読み込みのクラウドネイティブな形式**と**日本のデータ**)。範囲外の問いには、範囲外だと答える(`/system-record/instance`)。
- 答え方:
  - 次の 5 つを区別して答える: 確認された事実(`verified`)、導かれた解釈(`derived`)、規範(`normative`)、変わりやすい情報(`volatile`)、未解決の不確かさ(`open`)。
  - **版を必ず言う。** terrio は数日で版が上がる。答えの版(「0.7.0 で確かめた」など)を添え、それより新しい版では確かめていないと述べる。
  - 分からないことは、分からないと答える。このファイルに根拠がないことを、推測で埋めない。
  - 根拠にしたオブジェクトのパス(`/...`)を、**回答の中に書く**。
  - ファイルに書かれていることと、あなた自身の言い換え・推論を区別する。後者は「私の推論」と明示する。
  - 足りない知識に気づいたら、何が足りないかを指摘する。
- 毎ターンの約束(チャット型の場合): このファイルを更新したら、**統合した正本の全文を `.md` の添付ファイルで返す**。差分・要約・部分ファイルは返さない。更新がなかったターンは、そう述べる。添付で返せない場合は、本文の `.md` コードブロックで全文を返す。
- 全文へのアクセス(チャット型の場合): 求められたら、第 1 レベル見出しの数と、最初と最後の見出しを答える。全文を持っていなければ、そう述べ、更新を確定しない。
- 毎ターンの約束(コードエージェント型の場合): ファイルを直接更新し、変更の要約を返す。
- してはならないこと: 出典を発明しない。記憶による引用を根拠にしない。Markdown 以外の形式を黙って正本の代わりにしない。機微な情報を書き込まない。**上流(opengeos/terrio)への投稿・コメント・PR をしない**(`/procedures/upstream-reporting`)。
- 利用者向けの一行プロンプト: 「添付の kcaim があなたの作業文脈です。冒頭の `agent-contract` に従い、答えには terrio の版を添えてください。更新したら全文を `.md` の添付で返してください。」

# /system-record/instance
- name: kcaim-terrio
- concept-version: dwg7/kcaim の CONCEPT.md、2026-11-07(コミット 8f85cd6)。形式は 2026-11-04(a9bfc83)から変わらず、呼び名だけが **miso**(旧称 kcaim / KCAIM)に改められた。この試作は a9bfc83 の本文で作ったので、名前は旧称のまま
- 呼び名: miso(旧称 kcaim)。ファイルは `miso/terrio.md`。
- 種別: **探索・理解型**(terrio を理解し比較する)に、**運用型**の層(dwg7 の地理空間の前処理を terrio で置き換えられるかの判断支援)を載せる。
- 作成: hfu の指示のもと、AI(Claude)が書いた。**人による内容確認は未了**。`dwg7/kcai-terrio` の踏み跡 46 本(`knowledge/`)から移植(2026-11-07)。
- 範囲: terrio 0.3.2〜**0.10.0**(2026-10-20〜11-25)の挙動。確かめた版は各オブジェクトに書く。
- 範囲外: ①terrio の最新版(0.10.0 より新しい版)。②GDAL・PROJ・PDAL そのものの使い方。③terrio の内部設計の評価、法的な判断(ライセンスの適否)。④日本以外のデータの網羅的な確認。⑤terrio への投稿・働きかけ(人が個人として行う)。
- 観察者の位置: 書き手は terrio の**外部観察者**。作者でも上流の貢献者でもない。動かした範囲(`played`)と、ドキュメント・ソースを読んだだけの範囲(`read-docs` / `read-source`)を区別する。大きなデータ・認証が要る環境・Windows/macOS は確かめていない(Linux x86_64 のみ)。
- 単位: ほとんどの事実は「**terrio のある版 × あるインターフェース**(CLI / Python / JS / Rust / MCP)」の組を単位とする。インターフェースで挙動が違う(`/assets/cloud-native-reads`)。
- 正本: この `.md` ファイル。`dwg7/kcai-terrio` の `knowledge/` の踏み跡 46 本は、**拡張の根拠**として別に残してある(`/system-record/relation-to-kcai`)。
- 機微情報: 含まない。公開データ・公開ドキュメントだけを使った。

# /system-record/vocabulary-map
- status: normative
- 内容の状態(中核の語彙)と、kcai-terrio の踏み跡での対応:
  - `verified`: 実際に動かして確かめた(`verified_how: played`)。**何を、どの版で、どの環境で確かめたかを限定して使う。**
  - `stated`: ドキュメントやソースがそう述べる(`read-docs` / `read-source`)。動かしていない。
  - `derived`: 確かめた事実からの導き(助言、読み取り)。
  - `volatile`: 版が上がると変わりうる。terrio の事実の大半がこれに当たる。**確かめた版を必ず付ける。**
  - `open`: 未確認・未解決。
- 結果の語(受け入れテスト): `pass` / `partial` / `fail` / `volatile` / `untested`。
- 対応表: kcai-terrio の `status: draft` ≒ 人が未確認の `verified`/`stated`。`stale` ≒ `volatile` で、新しい版で未確認。`reviewed` は人が確認した印(このインスタンスではまだ無い)。

# /system-record/relation-to-kcai
- status: derived
- `dwg7/kcai-terrio` は kcai の形式(1 ファイル 1 主題の踏み跡、`knowledge/`、46 本)で始まり、2026-11-07 に、その内容をこのファイルに**移植して正本を移した**(hfu の案)。`knowledge/` は**凍結**(terrio 0.7.0、2026-11-04 の確認が最後)。新しい知識、更新、受け入れテストは、このファイルに書く。凍結した木は消さない(詳しい手順・数値の表・版ごとの確認の履歴の根拠)。
- kcai の「踏み跡」は共有の単位で、このファイルの `/sources/…` と `/assets/…` に当たる。このファイルの `/traces/…` は**運用の踏み跡**で、`plays/` と `DECISIONS.md` に当たる(CONCEPT §7.1)。
- 個々の踏み跡の id は、このファイル内で `kcai:<id>`(例: `kcai:cloud-native-read-behavior-matrix`)と書いて指す。`knowledge/<id>.md` に元の詳しい記述がある。**木とこのファイルが食い違うときは、このファイルが新しい**(木は凍結)。
- kcai-terrio は kcai のインスタンス(共有地の踏み跡のリポジトリ)でもあるので、名前は `kcai-terrio` のまま(`dwg7/miso` の命名の規則: `kcai-*` は変えない)。

# /authorities/precedence
- status: normative(このインスタンス内の取り決め)
- 規則1: 挙動の事実は、**動かして確かめた記録**(`verified`)を最優先とし、次にソース、次にドキュメント(`stated`)。
- 規則2: terrio の公式ドキュメント(terrio.dev)は **main に追随し、配布版より先行する**ことがある。配布版の事実は、その版の wheel で確かめたものを優先する。
- 規則3: 版が違う記述は混ぜない。新しい版の確認が古い版の記述と食い違うときは、新しい版を優先し、古い版の事実は「その版では」と限定して残す。
- 規則4: GDAL / PROJ / PDAL との一致は、**その版の GDAL(3.8.4 / 3.13.3)**での一致を指す。GDAL の版で挙動が変わる例がある(`/lessons/gdal-version-dependence`)。
- 規則5: 法的な評価はしない。ライセンスの記述は、公開された表記の要約。

# /sources/terrio-repo
- 取り込み状況: 一部取り込み(git log、CHANGELOG、ROADMAP、docs の差分、ソースの要所)
- 名称: opengeos/terrio(作者 Qiusheng Wu)。MIT AND MPL-2.0(0.6.0 以降)
- URL: https://github.com/opengeos/terrio
- 確認: 配布版 0.7.0(main `f24cd15`)。確認日 2026-11-04
- 備考: 浅い複製(履歴 181〜231 コミットの範囲)。`kcai:terrio-source-scale-and-origins`

# /sources/terrio-docs
- 取り込み状況: 一部取り込み(0.3.2 で全 25 ページ。0.5.0・0.7.0 は差分の見出しと CHANGELOG)
- URL: https://terrio.dev(旧 terrio.opengeos.org は転送)
- 確認日: 2026-11-04。0.7.0 のドキュメントは 41 ページ。

# /sources/registries
- 名称: PyPI(terrio)、crates.io(terrio、terrio-crs)、npm(terrio-js)
- 最新: **0.10.0**(2026-11-25)。0.9.0=11-14〜15 より前の履歴: リリース履歴: 0.3.2=10-20、0.4.0〜0.4.2=10-22、0.5.0=10-24、0.6.0=10-31、0.6.1=11-01、0.7.0=11-03、0.8.0=11-08、0.9.0=11-14〜15、**0.10.0=11-24〜25**。0.9.0 → 0.10.0 は **205 コミット・約 +13 万行**、0.7.0 から 0.10.0 まで約 500 コミット。0.9.0・0.10.0 に破壊的変更が多い(`/assets/version-notes`)

# /sources/gdal-comparisons
- 名称: GDAL 3.8.4 / PROJ 9.4(Ubuntu apt)、GDAL 3.13.3 / PDAL 2.10.2(conda-forge)
- 用途: terrio の結果の突き合わせ。terrio 自身の基準は GDAL 3.12 系。

# /sources/play-datasets
- 名称: USGS 3DEP の COG、Sentinel-2 L2A の COG(AWS)、opengeos/data、Natural Earth 相当、国土数値情報の PMTiles(depot.optgeo.org)、Source Cooperative の GeoParquet、flatgeobuf.org の試験データ
- 利用条件: `kcai:data-licenses-of-play-datasets`。公開データのみ。

# /assets/terrio-overview
- status: verified(起源・規模は読み取り。`stated` を含む)
- 何か: GDAL を使わない純 Rust の地理空間入出力ライブラリ。CLI(`terrio`、サブコマンド約 100)、Python(`pip install terrio`)、JavaScript/WebAssembly(`terrio-js`)、Rust crate、MCP サーバー(`terrio mcp`、ツール 99 個)。
- 起源: 2026-10-14 に Qiusheng Wu が開始。README が「主に Claude Opus 5.5 で作られ、人の指示とレビューのもと」と明記。Whitebox(John Lindsay)の `wbraster` / `wbvector` / `wbprojection` の上に始まった。0.5.0 以降は貢献者が約 20 人に増えた。(`kcai:terrio-source-scale-and-origins`)
- 規模(v0.4.2): 本体 Rust 約 10.3 万行。0.5.0〜0.7.0 の 11 日で 231 コミット、約 +34 万行。
- 変化の速さ: **volatile**。答えは版つきで。0.7.0 の後も main が進んでいる(`/assets/governance-and-evolution`)。
- 既定のビルドは C 依存なし(0.6.0〜)。CRS は独立した crate `terrio-crs`。
- ライセンス: 0.6.0 から MIT AND MPL-2.0(点群の固有値ソルバーが MPL-2.0)。幾何は JTS の移植か独立実装(`kcai:terrio-geometry-provenance-and-clean-room`)。古い版は古い表記(`kcai:terrio-license-and-third-party-notices`)。

# /assets/cloud-native-reads
- status: verified(版つき。volatile)
- 目的: ファイルを丸ごとダウンロードせずに、どこまで読めるか。**インターフェースで違う。**
- 範囲読み込みする(verified。0.7.0 の値):
  - **COG**: CLI で窓(Sentinel-2 の 512²)が 3 要求・約 6.1 MiB(0.7.0)。`convert --overview N`(0 始まり、0 が最大の概観)は 1373² で約 2.5 MiB。**`translate --outsize 512 512`(縮小)は 0.7.0 で 0.69 MiB**(0.3.2 は約 208 MiB だった)。
  - **PMTiles**: CLI と JS で範囲読み込み(国土数値情報 3,625 地物の `info` が約 1.5 MiB)。
  - **COPC / JP2 / Zarr(一部)**: 範囲読み込み(0.3.2 で確認)。
- **GeoParquet は 0.9.0 から CLI・Python も範囲読み込み(verified、0.9.0)**: 5 GB の `JPN.parquet`(Source Cooperative)を `convert --spat`(東京駅付近の小さな bbox)すると **14 要求・16.3 MiB・7 秒・90 地物**。一時ファイルは残らない(0.3.2〜0.7.0 は全量取得で、8 秒で 221 MB を書いて一時ファイルが残った)。フッターのあと、**必要な行グループの列チャンクだけ**を範囲要求で取る。`--select`(`--where` や `--sql` なし)と `open_stream(columns=…)` は、**選んだ列のチャンクだけ**を取る。作者の測定(`stated`): Overture の建物 533 MB(S3)の小さな矩形が 5 要求・4.9 MiB。
- **0.10.0 での再確認(verified)**: GeoParquet(5 GB の `JPN.parquet`)は 14 要求・16.34 MiB・約 3.6 秒・90 地物で、0.9.0 と同じ。FlatGeobuf の CLI は**全量のまま**(2 要求・13.45 MiB)。COG の窓(B04、512²)は 7 要求・6.14 MiB(要求数は 0.7.0 の 3 から増えたが、量は同じ)、`translate --outsize 512 512` は 2 要求・0.62 MiB。
- **インターフェースで違う(verified。0.9.0 では FlatGeobuf だけ)**: FlatGeobuf は、**terrio-js の `openUrl` が bbox で範囲読み込み**(768 KiB)するのに対し、**CLI は 0.9.0 でも全量**(先頭 16 KiB のあと `bytes=16384-` で約 14 MB。`UScounties.fgb`)。以下は 0.7.0 までの記述: FlatGeobuf と GeoParquet は、**terrio-js の `openUrl` が bbox で範囲読み込み**(FlatGeobuf 768 KiB、5 GB の GeoParquet が 16.4 MiB・7 要求、0.7.0 で確認)。**CLI と Python は全量取得**(FlatGeobuf は 0.7.0 でも約 14 MB を受け取る。GeoParquet の 5 GB は 0.3.2 で 221 MB まで書いて停止)。中断すると `/tmp/terrio-*` に一時ファイルが残る(0.3.2)。
- STAC: `STACIT:` で検索結果をモザイクとして開く。東京の窓 512² で、全アイテム 17.5 MiB、`max_items=1` で 6.25 MiB(0.4.2)。GDAL の STACIT と画素一致。**`method=POST`(Earth Search)も動く**(`max_items=1` で 3 要求・6.14 MiB、0.7.0)。
- **STAC の資格情報つきアセット(0.9.0 の安全側の変更、verified)**: 環境に AWS の資格情報(`AWS_ACCESS_KEY_ID` など)があると、遠隔の STAC 文書が `s3://` のアセットを選ぶ読みは**既定で拒否**される(「with configured credentials; set `TERRIO_STAC_ALLOW_CREDENTIALED_ASSETS=YES` to allow this read」)。Earth Search の `STACIT:…:asset=red,max_items=1` は、**資格情報が無ければ通り**(8 要求・6.20 MiB、`method=POST` も同じ)、**あれば拒否される**(許可は環境変数で)。
- **GRIB(0.7.0、NOAA GFS の公開 S3)**: 範囲読み込みで開く。`info` は 696 バンドを **713 要求・6.9 MiB**(メッセージごとに 16 KiB のヘッダー)。1 バンドの窓 64² の取り出しは、さらに約 0.8 MiB(計 714 要求・7.75 MiB)。
- **GRIB の値(0.10.0、played、GDAL 3.13.3 + `libgdal-grib` と比較)**: NOAA GFS の 696 バンドのうち 4 バンド(1・100・400・696)の窓(64×48)を取り出し、**値が GDAL と完全一致**(欠測の 9.999e+20 も含む)。メタデータ(`GRIB_ELEMENT`・`GRIB_UNIT`・`GRIB_COMMENT`・`GRIB_SHORT_NAME`)、原点・画素サイズ(0.25°)、座標系(球 6371229 m の GEOGCRS)も同じ。**違い**: バンドの説明文(`Description`)の形。terrio は `100[Pa] ISBL="Isobaric surface"`、GDAL 3.13.3 は `DZDT:1 mb:anl`。時間は、`gdalinfo` が `/vsicurl/` で 16.6 秒、terrio の `translate` はバンドごとに約 25 秒（開くたびに 713 要求）、GDAL の `gdal_translate` は約 17 秒で、速さは同程度。
- **遠隔 Zarr の値(0.10.0、played、HRRR の 2 m 気温、1799×1059、GDAL 3.13.3 と比較)**: 窓(120×90)の値は、**行の向きを揃えれば完全一致**。**ただし向きが違う**: GDAL はこの格子を**南が上（行が下から上、画素の高さが +3000）のまま**扱い、terrio は**北が上に並べ替える**（画素の高さ −3000、原点が上端）。同じ `--srcwin` の番号は**別の地点**を指す（GDAL の行 400〜489 は terrio の行 569〜658）。地理的な位置（座標）は同じ。terrio は 1.4 秒、GDAL は 4.0 秒。座標系は両方とも不明。
- **遠隔 Zarr(0.7.0、NOAA HRRR、`AWS_NO_SIGN_REQUEST=YES` の S3)**: `ZARR:"/vsis3/hrrrzarr/…"` で `info` が通る(1799×1059、座標系は `unknown`)。
- **OGC API Features / WFS(0.7.0)**: `OAPIF:https://demo.pygeoapi.io/master/collections/lakes` の `info` と、ページ送り(`--oo PAGE_SIZE=3`)つきの GeoPackage への変換が通る。`WFS:`(demo.mapserver.org、1.1.0)の `info` が層を列挙する。
- 詳細: `kcai:cloud-native-read-behavior-matrix`、`kcai:cog-remote-window-overview-and-warp`、`kcai:pmtiles-remote-reading`、`kcai:terrio-js-cloud-native-reads-in-browser`、`kcai:terrio-stac-and-stacit`

# /assets/japan-local
- status: verified(版つき。volatile)
- 日本語の文字列: GeoJSON / CSV の日本語長文字列で panic したのは **0.3.2 まで**(#159)。**0.4.0 以降は通る**(Shapefile・FlatGeobuf・GeoPackage・PMTiles・GeoParquet・CSV)。
- **Zarr の日本語の相対パス**: `terrio info 日本語/a.zarr` が **0.7.0 でも panic**(`zarr.rs` の `t[..5]`)。絶対パスと書き出しは通る。
- Shapefile の CP932: **`.cpg` が `CP932` なら 0.7.0 で読める**(0.3.2〜0.5.0 は文字化け)。`.cpg` が無ければ文字化け(GDAL も同じ)。
- 座標変換: JGD2011(`EPSG:6668`)→ 平面直角第IX系(`EPSG:6677`)は (139.767125, 35.681236) → **(−5992.919570392903, −35363.23774493004)**。GDAL と小数 9 桁以上で一致、0.3.2〜0.7.0 で同じ。旧日本測地系(`EPSG:4301` → `6668`)も約 1e-9 で一致(0.3.2)。
- ジオイド: **3 次元** `EPSG:6667 → 6697`(高さ 50)で、**`TERRIO_NETWORK=ON`(PROJ の CDN の格子)が要る**。**0.10.0 は 13.3375(GSIGEO2011)で、GDAL 3.13.3(`PROJ_NETWORK=ON`)と小数 12 桁まで同じ**(0.3.2〜0.9.0 は JPGEO2024 の 13.2386 だった。0.10.0 で CRS の表が EPSG v13.102・PROJ 9.9.0 の識別になった)。**ネットワークなしでは、警告("geoid model did not apply … set TERRIO_NETWORK=ON or TERRIO_GRID_DIR")つきで高さは 50 のまま**。**2 次元の `EPSG:6668` では高さは変わらない**(GDAL も同じ)。(`kcai:vertical-datum-grids-and-geoid-in-japan`。0.9.0 以前の値の記述)
- 詳細: `kcai:geojson-japanese-string-panic`、`kcai:japanese-path-panic-in-zarr-parse-name`、`kcai:shapefile-cp932-attributes-not-decoded`、`kcai:jgd2011-plane-rectangular-transform`

# /assets/processing-and-geometry
- status: verified(GDAL 3.8.4 との比較。volatile)
- ラスタ処理: `dem`(hillshade・slope・aspect・TRI・TPI・roughness、multidirectional、compute-edges)、`translate`(srcwin・outsize・ot/scale)、`warp`(near・bilinear・cubic・average)、`calc`、`proximity`、`sieve`、`mosaic`、`rasterize`、COG 書き出しは、**GDAL 3.8.4 と画素が完全一致**(20 項目。0.3.2〜0.7.0 で繰り返し確認)。
- **0.10.0 でも同じ(verified、GDAL 3.13.3、`scripts/compare_with_gdal.py` の 19 項目)**: `dem` 7 種・`translate` 2 種・`calc`・`sieve` は一致(slope・aspect は float の丸め程度の差)、`warp` は既定で不一致(94〜1.7 万画素)、`--grid-invariant false` で 4 つの再サンプリングとも完全一致。
- **0.9.0 での変化(verified)**: ①**`warp` の既定が変わった**。0.8.0〜0.9.0 は既定で「格子不変(grid-invariant)」のサンプリングで、タイル・VRT の窓・メモリの塊をまたいでも値が同じになるが、**GDAL の既定の warper と画素が一致するとは約束しない**(ドキュメント)。実測: B04 を EPSG:6677・10 m に warp すると、GDAL と**94 画素(最近傍)〜1.7 万画素(cubic)が違う**(最大 5 階調、最近傍の端の 1 画素は 1,243)。**`--grid-invariant false` か `TERRIO_WARP_GRID=GDAL` で GDAL と画素が完全一致に戻る**(4 つの再サンプリングすべて、GDAL 3.8.4・3.13.3)。GDAL 3.13 の warp の kernel の変更は `--kernel-version 3.13` / `TERRIO_GDAL_COMPAT=3.13`(既定は 3.12 の挙動)。②`dem` の hillshade は、**GDAL 3.13.3 とは完全一致、3.8.4 とは違う**(GDAL 側の変更)。slope・aspect は GDAL 3.13.3 と float の丸め程度(最大 3e-5)の差。TRI・TPI・roughness・`translate`・`calc`・`proximity`・`sieve`・`mosaic` は一致のまま。→ **GDAL と同じ画素が要る工程は、`--grid-invariant false` を付け、比べる GDAL の版を決める**。
- 等高線・SQL(0.7.0、played): `terrio contour --interval 10`(標高モデル 140×140)は **106 本で、`gdal_contour -i 10` と同数**。`terrio sql` は `GROUP BY` と集計(`COUNT`・`SUM`)、`ST_Area` が動く(3 ポリゴンの試料で期待どおり)。`terrio preview` は端末でなければ `-o FILE` が要る。
- 幾何(0.5.0 から): `is-valid`・`make-valid`・`clean`・`buffer`・`overlay`・`dissolve` ほか。ちょうちょ形の不正ポリゴンで、修復・バッファ・ディゾルブが **GEOS と一致**(0.5.0 と 0.7.0)。実装は JTS の移植・クリーンルームに置き換わった(`kcai:terrio-geometry-provenance-and-clean-room`)。
- 形式の往復: Zarr・JPEG 2000・COG を terrio が書き、GDAL が画素一致で読む(0.4.2)。PMTiles(MVT)を GDAL が読める(0.3.2)。COPC と `filter range` は PDAL 2.10.2 と点数・統計が一致(0.3.2)。
- **ベクタタイル(PMTiles / MVT)の書き出し(0.7.0、played、tippecanoe 2.49.0・GDAL 3.8.4 と比較)**: terrio の書き出しは **GDAL の MVT ライターを再現**したもの(ドキュメント: EPSG:3857 に再投影、既定のズームは 0〜5、80/4096 の余白でクリップ、量子化、500 kB 超のタイルは低解像度に、`--minzoom`/`--maxzoom`、`--lco` で `SIMPLIFICATION`・`MAX_SIZE`・`MAX_FEATURES`・`BUFFER`)。国界 179 地物(多角形、z0〜4)では、**terrio・GDAL の MVT・tippecanoe の地物数がズームごとに一致**(178・199・221・281・436。terrio と GDAL のファイルは約 166 KB と 170 KB、tippecanoe は 155 KB)。**ただし密な点では tippecanoe の間引きに相当するものが無い**: 6 万点で z0 のタイルに 6 万点すべてを入れる(0.9.0 では z2・z4 も 6 万点すべて、アーカイブは 2.9 MB に。0.7.0 は z2・z4 が 46,200・45,600。tippecanoe は 246 点、z2 で 1,536 点、z4 で 9,600 点)。アーカイブは terrio 3.5 MB、tippecanoe 1.6 MB。GDAL の MVT ライターは z2・z4 で 48,600 点と、terrio(46,200・45,600)と少し違う(500 kB 超のタイルの扱いの差と思われる。未確認)。- **線のタイル(0.9.0、played、tippecanoe 2.49.0 と比較)**: 国界の輪郭線 284 本(z0〜6)は、**地物数がズームごとに tippecanoe と一致**(284・332・552・1,682)し、頂点数も近く(z0 で terrio 9,958 対 tippecanoe 8,578、z6 で 13,928 対 13,830)、アーカイブは 376 KB 対 391 KB。**ふつうの実データの線なら、tippecanoe とほぼ同じ**。一方、**ごく細かいノイズの線**(乱数歩行の 3,000 本、各 61 頂点、4°四方)では差が出る: z0 の頂点数は terrio 25,179 対 tippecanoe 4,040(総延長 22 万 km 対 2.3 万 km)、z2 で 8.3 万対 1.3 万、z4 で 17 万対 9 万。**tippecanoe は画素より小さい細部をズーム別に大きく簡略化し、terrio は量子化(4096 格子)による削減が中心**。アーカイブは 911 KB 対 733 KB。GDAL の MVT ディレクトリは、GDAL 3.13.3 の `OpenEx` で開けなかった(原因未確認)。
- **MapLibre での見え方(0.9.0、played、MapLibre GL JS 4.7.1 を実 Chromium で、同じ入力・同じスタイル・同じカメラで描画)**: terrio・tippecanoe・GDAL の MVT を、XYZ のディレクトリ(gzip は `Content-Encoding` つきで配信)にして描き、画素を比べた。**多角形(国界)と線は、terrio の描画が GDAL の MVT と画素まで同一**(差のある画素 0.00%)で、**tippecanoe とも差は 0.02% 以下**(z1・z3・z5。輪郭線も同様)。描かれる地物数も同じ(例: z3 で 36、z5 で 6)。**点は違いが見える**: 60,000 点のとき、terrio は全点を描き(z4・z6 とも 6 万地物)、tippecanoe は間引いて 3,840(z4)・23,998(z6)。暗い画素は z4 で 10,480 対 5,432、タイルの合計は 3.4 MB 対 1.2 MB(`--drop-densest-as-needed` を付けても tippecanoe は同じ結果)。画面では、terrio は密集部が塗りつぶされ、tippecanoe は粒が見える。MapLibre は、gzip の `.pbf` を、サーバーが `Content-Encoding: gzip` を付けないと読めない(terrio・GDAL の書き出しは gzip、tippecanoe は `--no-tile-compression` で無圧縮にした)。
つまり **terrio は「GDAL の MVT ライターの代わり」にはなるが、「tippecanoe の代わり」には、点の密度による間引き(`--drop-densest-as-needed` など)、自動の最大ズーム(`-zg`)の面で、まだならない**。
- **視域・ゾーン統計(0.10.0、played、GDAL 3.13.3 と比較。UTM 13N・30 m の 320×412 の DEM)**: **`viewshed` は 4 つのモードすべてが `gdal_viewshed` と画素完全一致**(NORMAL: 201×201 で見える画素 2,399 が両方同じ、DEM、GROUND、ACCUM。`--md` と ACCUM の併用は、両方とも拒否)。**`zonal-stats` は、`gdal raster zonal-stats` と、count・min・max・mean・sum・stdev が全桁一致**(3 つの多角形。既定の画素選択と `--all-touched`)。terrio の出力の列名は `<ラスタ名>_b<バンド>_<統計>`(例 `u_b1_mean`)で、GDAL は統計名のみ(`mean`)。
- **まだ残る差**(0.9.0 でも): `warp --dstalpha` が無い。COG の `TILING_SCHEME=GoogleMapsCompatible` を黙って無視する(画素サイズ 12.32 m のまま)。
- 詳細: `kcai:terrio-vs-gdal-spot-checks`、`kcai:terrio-processing-commands-smoke-test`、`kcai:terrio-conformance-and-testing-against-gdal`

# /assets/raster-tiles
- status: verified(0.10.0、played、gdal2tiles 3.13.3 と比較。volatile)
- `terrio tile INPUT OUTPUT_DIR` は、ラスタを z/x/y のタイルのディレクトリにする(`gdal2tiles` 相当)。形式は PNG・WebP(可逆)・GTiff、既定は WebMercatorQuad・256 px・xyz・cubic、`--tiling-scheme`(WorldCRS84Quad、raster)、`--resume`、`--webviewer`(Leaflet・OpenLayers・MapML・STAC)、`--kml`、`--skip-blank`、`--add-alpha`。
- **比較(Sentinel-2 B04 の 1024² を Byte にしたもの、UTM 54N → ウェブメルカトル、z10〜14、`-r bilinear`)**: タイル集合は **61 枚で `gdal2tiles --xyz` と完全に同じ**(z ごとの枚数、座標とも)。ズームの範囲は同じ。ともに約 1 秒。**最大ズーム(z14)は画素ほぼ一致**(36 枚、平均差 0.05 階調、最大 1 階調、`-r near` では差のある画素 0.3% で、ずれは無し)。アルファの範囲も同じ(不一致 16 画素)。**低ズームは差がある**: 平均差 z13=2.5、z12=4.2、z11=4.5、z10=4.2 階調(255 中。8 階調超の画素は 4〜14%)、アルファの不一致は z10〜13 で 276〜1,358 画素。`--overview-source source`(各低ズームを原データから作る)にすると z10〜12 は平均差 1.6〜1.8 に縮むが、z13 は 4.5 に広がる。**どの設定でも gdal2tiles と一致はしない**(低ズームの縮小のやり方が違う)。
- つまり、`gdal2tiles` の代わりには、**最大ズームのタイルは同じ画素、低ズームはわずかな階調差**(見た目の差は小さいが、画素一致は要求できない)。dwg7 の用途(標高・空中写真のタイル)では、見た目の差は無視できる範囲と思われる(目視は未確認)。GTiff / WebP の出力、`--webviewer` の中身は未確認。
- 詳細: `plays/2026-11-27-raster-tiles.md`

# /assets/interfaces
- status: verified(一部 stated)
- Python: 公式ノートブック 2 本(quickstart・xarray)のコードセル 13 個ずつが全成功(0.7.0)。xarray のノートブックは `terrio[xarray]` に **`zarr` が入らない**ので別途 `pip install zarr`。`terrio.rio`(rasterio 互換)と `terrio-rio` コマンドがある。
- JavaScript/WebAssembly: terrio-js 0.7.0 の公開ページで、座標変換・日本語の文字列・6 つの範囲読み込みの試料が動く(実ブラウザ)。
- **ブラウザの CLI**: `https://terrio.dev/web/` は、terrio のコマンドラインを WebAssembly でタブの中で動かす(0.7.0 と表示。ファイルは手元に残り、URL は範囲読み込み)。ページの読み込みとコマンド一覧の表示を実ブラウザで確認(コマンドの実行は未確認)。
- **terrio-js の退行は 0.10.0 でも残る(verified、2026-11-27)**: 同じ 30.5 GB のラスタ PMTiles の `openUrl` が `capacity overflow` で panic(Node では**プロセスが落ち、`try/catch` で捕まえられない**。npm の `core`・`threads` のビルドも同じ)。0.8.0 は 4.1 秒で開く。0.10.0 の npm には `terrio-js/cog`(GeoTIFF/COG だけを HTTP で読む軽いモジュール)と `terrio-js/geoparquet`(GeoParquet だけ)が加わった。小さなベクタ PMTiles(1.1 秒)と FlatGeobuf(0.7 秒)は 0.10.0 でも開く。以下は 0.9.0 の記述:
- **terrio-js 0.9.0 の退行(verified)**: 大きなラスタの PMTiles(30.5 GB の Terrarium z9)の `openUrl` が **`capacity overflow` で panic**(Node で約 88 秒後、ブラウザでは `unreachable` も)。**0.7.0・0.8.0 は一瞬で開く**。小さなベクタの PMTiles、COG、FlatGeobuf、COPC、GeoParquet(5 GB)の `openUrl` は 0.9.0 でも動く。CLI の `terrio info`(同じ URL)は 0.9.0 でも 3.5 秒・12 要求で通る。上流への下書き `drafts/upstream/2026-11-19-terrio-js-openurl-large-raster-pmtiles-panics.md`。このリポジトリの公開ページは **terrio-js 0.7.0 に固定したまま**(0.9.0 では 1 つの試料が動かないため)。
- MCP: `terrio mcp` は 100 ツール(0.9.0・0.10.0。0.7.0 は 99)。各ツールは `args`(コマンドラインの配列)を取る。書き込みは一時的な場所に限ること。
- Rust: 0.4.0 から feature で絞れる。ドキュメントの依存の版が古かった(`"0.3"`)のは 0.7.0 で直った。
- 詳細: `kcai:terrio-python-api`、`kcai:terrio-xarray-integration`、`kcai:terrio-mcp-server`、`kcai:terrio-js-api-and-playground`、`kcai:terrio-rust-library-and-features`、`kcai:terrio-rio-rasterio-compatible-api`

# /scenarios/dwg7-tile-and-prep-workflow
- status: derived
- 背景: dwg7 / hfu の公開リポジトリは、タイル配信(PMTiles・Martin・MapLibre)と、その前処理(ogr2ogr・tippecanoe・gdal_translate・gdalwarp)が中心。
- terrio で**置き換えられる見込み**(verified の裏づけつき): ラスタの再投影・圧縮・窓・縮小・形式変換、ベクタの形式変換と属性の選択、日本語属性の変換(0.4.0 以降)、`.cpg` つきの CP932 の Shapefile(0.7.0)、幾何の検査・修復。
- **置き換えにくい**: タイル生成のうち**密な点・線の間引き**(tippecanoe 相当。多角形の PMTiles 書き出しは tippecanoe と地物数が一致、点は間引かずに全部入る。0.7.0)、Zarr の日本語の相対パス、CLI の FlatGeobuf・GeoParquet の部分読み。
- 詳細: `kcai:hfu-dwg7-workflow-substitution-survey`

# /decision-support/advice-for-dwg7
- status: derived(根拠は `/assets/…`、`kcai:advice-for-dwg7`)
- 1. 範囲読み込みは、**ブラウザ(terrio-js)**が最も広く効く。CLI・Python は、0.9.0 から GeoParquet も範囲読み込み(FlatGeobuf はまだ全量)。**terrio-js 0.9.0 は大きなラスタ PMTiles で panic**(0.8.0 まで)なので、版を固定する。
- 2. 縮小は 0.7.0 以降なら `translate --outsize` でよい。古い版は原寸を読む。**GeoParquet は 0.9.0 から CLI・Python でも bbox で範囲読み込み**。
- 3. **GDAL を捨てない。**新しい工程に入れるときは、小さな入力で GDAL と並べる(新旧の GDAL で)。**0.9.0 の `warp` は既定で `gdalwarp` と画素が違う**(`--grid-invariant false` で一致)。
- 4. CP932 の Shapefile は `.cpg` を付ける。日本語の Zarr は絶対パスで。
- 5. **版を固定**し、`scripts/recheck_known_issues.sh` で既知の穴を確かめる。
- 6. 上流への報告は、再現の最小化・GDAL との突き合わせ・版の明記をして、**人が投稿**する。投稿が遅れると、他の人に先に直される。

# /procedures/recheck-on-new-version
- status: normative
- terrio の新版(PyPI・crates.io・npm)が出たら: ①CHANGELOG と docs の差分を読む。②新版の wheel で `scripts/recheck_known_issues.sh` を実行する。③画素の比較(`dem` ほか。**GDAL との比較は `--grid-invariant false` つきの `warp` と、新旧の GDAL で**)・公式ノートブック・terrio-js の公開ページ(**大きなラスタ PMTiles の試料を含む**)・GeoParquet / FlatGeobuf の CLI の取得量(5 GB の `JPN.parquet` の bbox)を再実行する。④確かめられなかった項目は `volatile`(kcai-terrio では `stale`)にする。⑤`kcai:advice-for-dwg7` と、このファイルの `/acceptance-tests/…` を更新する。
- 注意: 定期実行(毎日 7:23 JST)があるが、実行側のセッションにリポジトリが入っていないと push できない(`/traces/schedule-push-failure`)。

# /procedures/japanese-data-checklist
- status: normative
- ①日本語の文字列(GeoJSON・CSV)は 0.4.0 以降か。②Shapefile は `.cpg` があるか(CP932 なら `CP932`)。③Zarr は絶対パスか。④平面直角の系番号(EPSG:6669〜6687)。⑤高さを扱うなら 3 次元の `EPSG:6667`(2 次元の `6668` ではジオイドが効かない)。⑥GDAL と小さな入力で突き合わせる。

# /procedures/upstream-reporting
- status: normative
- terrio への報告は**人(hfu)が個人として投稿する**。AI は下書き(`drafts/upstream/`)まで。下書きは、最小の再現、terrio と GDAL の版、敬意のある英語。未検証の主張は外す。GDAL の挙動は、新旧の版で確かめてから書く。

# /traces/upstream-159-fix
- status: verified(経過)
- 2026-10-21 に日本語の長い文字列で GeoJSON が panic する問題を、hfu が #159 として報告。翌日に作者が #161 で修正、0.4.0(10-22)の配布版に入った。報告から配布まで約 1 日。

# /traces/geoid-and-calc-retraction
- status: verified
- 「日本のジオイドが適用されない」「`calc` の割り算が整数に丸まる」と書きかけたが、GDAL 3.8.4 で突き合わせると、前者は 2 次元の `EPSG:6668` を使った誤り、後者は GDAL も同じ既定だった。投稿前に取り下げた。

# /traces/fixed-before-posting
- status: verified
- 下書き 3 件(南極点の EPSG:3857、docs/rust.md の依存の版、CP932)が、**投稿しないうちに別の人の修正で不要になった**(0.7.0)。`--ot Int16` の下書きは、GDAL 3.13.3 が terrio と同じ挙動で、取り下げた。

# /traces/schedule-push-failure
- status: verified
- 新版確認の定期実行は 2026-10-22 から毎日動いたが、そのセッションにリポジトリが入っておらず、push が拒否され続けた(記録が届かなかった)。迂回せず、手元で確かめ直した(2026-11-04)。

# /lessons/gdal-version-dependence
- status: derived(根拠: `/traces/geoid-and-calc-retraction`、`--ot Int16` の取り下げ)
- GDAL の挙動は版で変わる。上流に出す主張は、**新旧の GDAL で確かめてから**にする。

# /lessons/report-early-but-verified
- status: derived(根拠: `/traces/upstream-159-fix`、`/traces/fixed-before-posting`)
- 報告は速く直る一方、遅れると他の人に追い越される。**再現が確実で小さいものから、確かめたうえで早く**出す。

# /lessons/versioned-facts
- status: derived
- 事実を「その版では」と限定して持つ。新版で `stale` にして確かめ直す運用が、この宇宙の品質を保つ。

# /open-questions/geoid-network-dependency
- status: open
- 3 次元 `EPSG:6667 → 6697` のジオイドは、`TERRIO_NETWORK=ON`(PROJ の CDN の格子)が要るのか。定期実行の記録は「付けないと警告が出て高さは変わらない」と言い、手元の 0.7.0 では付けずに 13.2386 が出た(格子のキャッシュの有無の可能性)。未整理。

# /open-questions/tile-generation
- status: open(一部解決)
- 解決(0.7.0、played): 国界のような多角形では、terrio の PMTiles は tippecanoe・GDAL の MVT と地物数が一致する。**点の密度による間引き・自動の最大ズームは無い**(`/assets/processing-and-geometry`)。
- 解決(0.9.0、played): 線のタイル。国界のような実データの線は tippecanoe とほぼ同じ。画素より小さい細部が多い線(ノイズ)は、tippecanoe のほうが低ズームで大きく簡略化する。
- 解決(0.9.0、played): MapLibre での見え方。多角形・線は GDAL の MVT と画素一致、tippecanoe とほぼ同じ。点は間引きの有無が見た目に出る。
- 未確認: 属性の扱い(tippecanoe の `-y` `-x` 相当は `--select`)、MapLibre での見え方、大規模データ(百万地物)、`terrio tile`(ラスタの z/x/y.png)。

# /open-questions/unverified-0-7-0-areas
- status: open
- 0.7.0〜0.9.0 で動かして確かめていない領域(2026-11-19 のキャッチアップ後): STACTA、`terrio.dev/web` でのコマンドの実行、`preview` の画像の中身、`viewshed`、`zonal-stats` の値(試料が重ならなかった)、新しい点群フィルタ(dbscan・lof ほか)の値、ベンチマークの数値、プレイグラウンド、Windows / macOS。**main(0.7.0 より 55 コミット先)の変更は、リリースされるまで確かめない**。

# /open-questions/reviewed-by
- status: open
- どの踏み跡を、誰が `reviewed` にするか(hfu の判断待ち。`QUESTIONS.md`)。

# /acceptance-tests/geoparquet-bbox-without-download
- query: 5 GB の GeoParquet の一部を、丸ごとダウンロードせずに bbox で読めるか
- expected: 読める。ブラウザ(terrio-js の `openUrl`)は約 16 MiB・7 要求。**CLI・Python も 0.9.0 から読める**(14 要求・16.3 MiB・7 秒。0.3.2〜0.7.0 は全量取得で 5 GB)。FlatGeobuf の CLI は 0.9.0 でも全量
- requires: /assets/cloud-native-reads
- result: untested
- freshness: terrio の新版ごとに CLI の挙動を確認(0.9.0 で変わった)

# /acceptance-tests/cog-window-size
- query: Sentinel-2 の COG から 512×512 を取り出すと、転送量はどれくらいか。大きな COG を縮小するには
- expected: 窓は約 6 MiB・3 要求。縮小は `translate --outsize` が 0.7.0 で約 0.7 MiB(古い版は原寸を読む)
- requires: /assets/cloud-native-reads
- result: untested

# /acceptance-tests/japanese-attributes
- query: 日本語の属性を持つ GeoJSON / CSV / Shapefile(CP932)を、terrio で Shapefile や FlatGeobuf に変換できるか
- expected: GeoJSON / CSV は 0.4.0 以降で可(0.3.2 は panic)。CP932 の Shapefile は `.cpg` が `CP932` なら 0.7.0 で可。Zarr の日本語の相対パスは panic
- requires: /assets/japan-local, /procedures/japanese-data-checklist
- result: untested

# /acceptance-tests/plane-rectangular
- query: 東京駅付近(139.767125, 35.681236)を、JGD2011 から第IX系に変換した値は
- expected: (−5992.919570392903, −35363.23774493004)。GDAL と小数 9 桁以上で一致
- requires: /assets/japan-local
- result: untested

# /acceptance-tests/geoid
- query: JGD2011 の楕円体高をジオイド高で補正する変換は、terrio でできるか
- expected: 3 次元の `EPSG:6667 → 6697` ではできる。2 次元の `EPSG:6668` では高さは変わらない。ネットワークの要否は未整理(`/open-questions/geoid-network-dependency`)
- requires: /assets/japan-local
- result: untested

# /acceptance-tests/geometry-repair
- query: 不正なポリゴンの修復、バッファ、ディゾルブを terrio でできるか。GEOS と同じ結果か
- expected: 0.5.0 以降でできる。ちょうちょ形の試料で GEOS と一致(0.7.0 まで)。大規模データでは未確認
- requires: /assets/processing-and-geometry
- result: untested

# /acceptance-tests/tippecanoe-substitute
- query: terrio で tippecanoe の代わりにタイルを作れるか
- expected: PMTiles / MVT の書き出しはでき、多角形では tippecanoe と地物数が一致する(国界)。**密な点の間引き(`--drop-densest-as-needed`)と自動の最大ズームは無く**、6 万点で z0 に全点が入る(0.7.0)。つまり GDAL の MVT ライターの代わりにはなるが、tippecanoe の代わりには、間引きが要る用途ではまだならない
- requires: /assets/cloud-native-reads, /scenarios/dwg7-tile-and-prep-workflow
- result: untested

# /acceptance-tests/warp-matches-gdalwarp
- query: terrio の `warp` は `gdalwarp` と同じ画素を出すか
- expected: **0.9.0 の既定では一致しない**(格子不変のサンプリング。最大 5 階調ほどの差が 1〜2 割の画素に)。`--grid-invariant false`(または `TERRIO_WARP_GRID=GDAL`)で、4 つの再サンプリングとも GDAL 3.8.4・3.13.3 と完全一致。0.7.0 までは既定で一致していた
- requires: /assets/processing-and-geometry
- result: untested

# /acceptance-tests/terrio-js-large-pmtiles
- query: terrio-js で大きな PMTiles(ラスタ、数十 GB)を `openUrl` で開けるか
- expected: 0.7.0・0.8.0 は開ける。**0.9.0 は panic(`capacity overflow`)**。小さな PMTiles(ベクタ)は 0.9.0 でも開ける
- requires: /assets/interfaces
- result: untested

# /acceptance-tests/pixel-identical-to-gdal
- query: terrio の dem・warp・translate は GDAL と同じ画素を出すか
- expected: 0.7.0 までは 20 項目で GDAL 3.8.4 と完全一致。0.9.0 は、**warp が既定で一致せず**(`--grid-invariant false` で一致)、hillshade は GDAL 3.13.3 と一致(3.8.4 とは違う)。dstalpha と TILING_SCHEME は差が残る
- requires: /assets/processing-and-geometry
- result: untested

# /acceptance-tests/license
- query: terrio のライセンスは MIT だけか。古い版を使ってよいか
- expected: 0.6.0 から MIT AND MPL-2.0。古い版の表記は古いので更新が勧められている。法的な判断はしない
- requires: /assets/terrio-overview
- result: untested

# /acceptance-tests/version-staleness
- query: 「terrio は〜できない」と言われたが、いつの版の話か
- expected: 版を確かめる。terrio は数日で版が上がり、できなかったことが直る(南極点・CP932・docs の例は 0.7.0 で直った)
- requires: /lessons/versioned-facts, /traces/fixed-before-posting
- result: untested

# /acceptance-tests/out-of-scope-gdal-options
- query: gdalwarp の全オプションを terrio で再現するには
- expected: 範囲外(示唆あり)。terrio の `warp` の主な対応と、`--dstalpha` が無いことは言えるが、GDAL のオプション全体の対応表はこの宇宙にない
- requires: /system-record/instance
- result: untested

# /acceptance-tests/out-of-scope-newer-version
- query: terrio 0.8 で何が変わったか
- expected: 範囲外(0.7.0 までしか確かめていない)。`/procedures/recheck-on-new-version` を勧める
- requires: /system-record/instance
- result: untested

# /assets/formats-and-io
- status: verified(`terrio formats` と 0.3.2 のドキュメントの表の一致。0.5.0 以降の追加は `stated`。volatile)
- 名前は GDAL の短い名前に合わせる(`-f GTiff`、`-f "ESRI Shapefile"`)。
- ラスタ: GeoTIFF/COG(LZW・Deflate・PackBits・ZSTD・WebP・JPEG・LERC・JPEG XL・LZMA)、JPEG 2000、Zarr v2/v3(GeoZarr)、netCDF、HDF5、ERDAS Imagine、GeoPackage、PMTiles/MBTiles、VRT、STACIT、ENVI/Esri/SAGA/Idrisi などの格子、PNG/JPEG(ワールドファイル)、DTED。0.5.0 から **GRIB1/2**(純 Rust。GDAL の試験ファイルと実予報で比較したと作者)。
- ベクタ: GeoPackage、GeoParquet(**1.1 で書く**、確認)、FlatGeobuf、Shapefile、GeoJSON/GeoJSONSeq、CSV、KML/KMZ、GML、GPX、TopoJSON、MapInfo、OSM(読み取りのみ)、MVT。**GeoPackage・FlatGeobuf・GeoParquet・Shapefile・GeoJSON・GeoJSONSeq・CSV の間の変換は、ストリームでメモリが有限**。0.6.0〜0.7.0 の追加(`stated`): CityJSON / CityGML(フラットな XYZ 地物)、XLSX、ESRIJSON / ESRIPBF(ArcGIS のフィーチャサービス)、WFS 1.0〜2.0、OGC API Features の読み、HEC-RAS の HDF5、DXF(CAD)の一部、多次元配列(`multidim`)。
- 点群: LAS 1.0〜1.4(点形式 0〜10、波形つき)、LAZ、COPC、EPT、PLY、E57。
- 入力の場所: ローカル、HTTP(S)、`s3://` `gs://` `az://`、zip の中身(`a.zip!dir/x.shp`)、GDAL 流の vsicurl 形式。**出力はローカルのみ**。
- 含まない(宣言): 独自 SDK が要る形式(MrSID、ECW、FileGDB ラスタ)、データベース(PostGIS など)、GDAL の C API の完全一致。長い尾の形式(HDF4、NITF など)は、任意の `gdal` feature(PyPI の wheel には入らない。**GDAL を同梱した wheel は作らない**と ROADMAP が決めた、0.5.0)。
- 詳細: `kcai:terrio-formats-rasters-and-compression`、`kcai:terrio-formats-vectors-streaming-and-tiles`、`kcai:terrio-scope-included-and-excluded`

# /assets/cli-commands
- status: verified(0.7.0 の `terrio --help`。volatile)
- 核の 15(0.3.2〜): `info`(gdalinfo / ogrinfo -so。`--json` `--stats` `--hist`)、`convert`(形式変換と再投影。`--srcwin` `--overview`(ラスタ)、`--where` `--spat` `--sql`(ベクタ))、`translate`、`warp`、`mosaic`、`rasterize`、`polygonize`、`dem`、`calc`、`proximity`、`sieve`、`crs`(座標系の説明と変換。`--to`)、`formats`、`grid` / `filter`(PDAL 相当の点群)。
- 0.4.0 から: `mcp`(AI エージェント向け)。0.5.0 から: `centroid` `singlepart` `vertices` `footprint` `sample` `contour` `zonal-stats` `sql` `buffer` `overlay` `dissolve` `is-valid` `make-valid` `clean`。0.6.0〜0.7.0 の追加(`stated`/一部確認): `preview`(PNG・端末に描く)、`view`(ローカルの地図を配信)、`ui`(ブラウザの入力画面)、`viewshed`、`catalog`(GTI)、ベクタのデータセット操作(`concat` `partition` `set-field-type` `make-point` `create` `rename-layer` `edit` `update`)、`--json-usage`。**サブコマンドは約 100**。
- 決まり: 座標は常に「経度 緯度」(x=東、y=北)。`--overview N` は 0 始まりで、0 が最大の概観。`warp` に `--dst-transform`(回転した出力格子)。`filter` はすべて `--a-srs`(CRS の付与)。
- 落とし穴(0.7.0 でも): `warp --dstalpha` が無い。COG の `TILING_SCHEME` を黙って無視する。`calc` の型は NumPy の規則(`A/5` は Byte で整数に丸まる。GDAL の `gdal_calc.py` も同じ既定)。
- 詳細: `kcai:terrio-cli-overview`、`kcai:terrio-cli-command-reference`

# /assets/crs
- status: verified(日本の値は played。投影法の数・適合性の数字は `stated`。volatile)
- 受け付ける形: EPSG コード(数字だけ、URN、URL)、`OGC:CRS84`、`WGS84`、WKT1/WKT2(2015・2019、`BOUNDCRS`)、PROJ 文字列、PROJJSON(0.6.0〜)、ファイルのパス、複合 CRS(`EPSG:4326+5773`)、**ESRI コード**(`ESRI:54009`。0.4.0 から。0.3.2 は拒否)。
- 投影法: PROJ の 117 のうち **86 を PROJ と 1 mm 以内で計算し、31 は別のものを計算せずに拒否**(`airy`・`igh`・`nsper` など。0.5.0 時点の記述)。回転極(`ob_tran`、CF `rotated_latitude_longitude`)、静止衛星、2 点の斜軸メルカトル(0.6.0〜)。
- 格子と変換: NADCON5・NTv2・ジオイドなどの格子は**見つかれば適用**し、`TERRIO_NETWORK=ON` で PROJ の CDN から取る(0.4.0 以降、CDN の格子は範囲読み込み)。CRS 間の変換は **PROJ の鎖**(複数の中間データム)に対応(0.4.0〜0.5.0)。垂直 CRS、エポック間の点の運動(0.5.0)。
- 適合性(作者の検査、`stated`): GDAL / PROJ との座標変換・格子・ジオイド・エポックで **40,068 件中 39,999 件が一致、65 件が許容内、4 件に差**(例: EPSG:6054 → 4287 で 267 m)。比較の大半は 0.1.1 で、座標変換の部分は 0.3.2 で実行されたもの。
- 日本: `/assets/japan-local`。
- 詳細: `kcai:terrio-crs-forms-projections-grids-and-epochs`、`kcai:terrio-conformance-and-testing-against-gdal`

# /assets/stac-and-stacit
- status: verified(0.4.2 まで。volatile)
- STAC の Item・ItemCollection・Collection・Catalog は、**地物の範囲を持つベクタ層**として開ける。検索結果のアセットは `STACIT:"検索の URL":asset=red` で**モザイクのラスタ**として開き、窓読みは必要なタイルだけを取る。
- 重なる**全シーンから読む**。`asset=red,max_items=1`(カンマ区切り)で絞れる。東京の 3 シーン・窓 512² で **17.5 MiB → 6.25 MiB**(結果は同じ)。GDAL の STACIT と画素一致。
- 0.5.0 以降(`stated`): STAC の POST 検索・ページ送り、Planetary Computer の署名、STACTA(タイルつきアセット。GDAL と同じと作者)。**安全側の制限**: links は同一オリジンのみ(`TERRIO_STAC_FOLLOW_CROSS_ORIGIN=YES` で許可)、`GET` の検索を `POST` に引き継がない、Azure のトークンは設定の端点にだけ送る。
- 詳細: `kcai:terrio-stac-and-stacit`

# /assets/point-clouds
- status: verified(0.3.2 まで played。それ以降 `stated`。volatile)
- LAS・LAZ・COPC・EPT・PLY・E57 を読み書き(純 Rust。LASzip は `laz` crate)。**COPC は必要な範囲と粗さだけを範囲読み込み**(ドキュメントの Autzen の例を再現: 18,901 点・8 要求)。
- PDAL のフィルタ 20 種(0.3.2)→ さらに追加(dbscan・lof・dem・colorization・hexbin ほか。0.5.0〜0.7.0)。`grid` で DEM 化。`filter range` は PDAL 2.10.2 と点数・統計が一致。
- 0.7.0 のドキュメント: 点群の再投影は**高さ `z` も変換**する(複合 CRS・3D 地理 CRS・ジオイド)。
- 詳細: `kcai:terrio-point-clouds`

# /assets/install-and-distribution
- status: verified(PyPI のファイル一覧、LICENSE の同梱は played。volatile)
- 配布: PyPI(`pip install terrio`。Python 3.10 以上、abi3)、crates.io(`cargo add terrio`、`cargo install terrio-cli`、`terrio-crs`)、npm(`terrio-js`)。システムの依存(GDAL・PROJ・GEOS・SQLite)は要らない。**0.5.0 の PyPI は wheel 8 個 + sdist**(macOS x86_64/arm64、manylinux x86_64/aarch64、musllinux x86_64/aarch64、**Windows x86_64/arm64**。0.3.2 には Windows ARM64 が無かった)。0.6.0 から **Docker イメージ** `ghcr.io/opengeos/terrio`(amd64・arm64)。インストーラー(`install.sh`/`install.ps1`、`TERRIO_VERSION`)、AUR(`terrio-bin`)、Fedora COPR、Pyodide(wasm32 の wheel)。
- 変化の速さ: 2026-10-14 の開始から 3 週間で 0.1.1 → 0.7.0。**配布版とドキュメント・main の差**は、0.3.2 では大きかった(mcp・feature 分け・ESRI コード)が、0.4.0 以降はリリースが 1〜3 日おきで小さい。
- 詳細: `kcai:terrio-install-platforms-and-release-history`、`kcai:terrio-release-vs-main-drift`

# /assets/architecture
- status: stated(ソースとドキュメントの読み。volatile)
- 構成: `crates/terrio`(本体: `dataset.rs`、`formats.rs`、`drivers/`、`geotiff.rs`/`cog.rs`(遅延読み)、`tiles/`、`vfs.rs`、`http.rs`/`s3.rs`、`ops/`、`pointcloud/`、`stream/`)、`terrio-cli`、`terrio-crs`(0.6.0〜、独立)、`python/`(PyO3)、`js/`(wasm-bindgen)。
- **「純 Rust」**: 0.3.2 は完全には純ではなかった(wheel の SBOM に C を含む crate)。**0.6.0 から、CLI・Python・Rust・JavaScript の既定のビルドに C 依存がない**(CI は C コンパイラなしでビルド)。Zstandard は `ruzstd`(復号は遅く、書き込みは最速レベル相当。`libzstd` は任意)。HTTPS は `rustls-graviola`(x86-64・AArch64。**必要な CPU の機能がないと HTTPS の要求が panic する**)。
- 設計の決定: コア API は同期で、データセットをメモリに読む。GeoTIFF は例外で遅延の窓読み(実測と合う)。
- 詳細: `kcai:terrio-architecture-and-pure-rust-claim`

# /assets/rust-and-features
- status: verified(依存の解決は played。volatile)
- 入口: `terrio::open`、`open_raster`、`open_vector`、`open_raster_lazy`(ヘッダーで開き `read_window` で窓のタイルだけ復号)、`memory`、`stream`、`arrow`、`ops`、`crs`、`pointcloud`。データモデルは `wbraster::Raster` / `wbvector::Layer` の再エクスポートで、どちらかの破壊的更新を取り込むと terrio の破壊的リリースになる。
- **0.4.0 から feature で絞れる**(`default-features = false, features = ["geotiff", "remote"]` で実行ファイル 24 MB・依存 188 crate。0.3.2 の既定は 46 MB・302 crate)。feature: `parquet remote avif netcdf-hdf5 osm lzma flatgeobuf jp2 lerc pointcloud tiles zarr sqlite`(既定は全部)、`gdal`(既定オフ)。**0.3.x の crate には `geotiff` feature が無い**ので `version = "0.3"` では解決しない(ドキュメントの例は 0.7.0 で `"0.7"` に直った)。
- 構造体のオプションは `Default`(`..Default::default()`)。新フィールドで構造体リテラルが壊れる版がある(0.6.0・0.6.1 の CHANGELOG)。MSRV は 1.90。
- 詳細: `kcai:terrio-rust-library-and-features`

# /assets/conformance-and-benchmarks
- status: stated(作者の測定・検査。この宇宙では再測定していない。volatile)
- 作者の主張: 小さなファイルで 1.2〜16 倍、1 GB 級で 1.0〜13.6 倍、terrio が速い(0.3.2)。0.5.0 の再測定(40 スレッドの Xeon、GDAL 3.12.2 と terrio 0.4.2 を**同じスレッド数**で): warp(UTM 13N)最近傍 12.7 倍・bilinear 9.8 倍、ラスタ info 2.3 倍、COG 化 1.7 倍、mosaic 2.0 倍、rasterize 2.5 倍。大きな 14412² の mosaic は、統計 2.2 倍、warp 2.0 倍、COG 化は 1.0 倍遅い。メモリは terrio が少ないことが多い(JPEG 2000 → GeoTIFF と OSM → GeoPackage は多い)。ページ自身が「スナップショットとして読むこと」と断る。issue #212 の指摘で、以前は GDAL の多スレッドを切っていたと明記。
- この宇宙で動かして確かめたのは**画素の一致**(`/assets/processing-and-geometry`)で、速さではない。
- 詳細: `kcai:terrio-benchmarks-vs-gdal`、`kcai:terrio-conformance-and-testing-against-gdal`

# /assets/license-and-provenance
- status: verified(配布物の LICENSE は played。法的判断はしない。volatile)
- 本体は **MIT**(Copyright (c) 2026 Qiusheng Wu)。0.6.0 から**パッケージのメタデータは MIT AND MPL-2.0**(点群の固有値ソルバーが MPL-2.0)。リポジトリは REUSE 仕様に従い、取り入れたファイルに SPDX ヘッダー、`NOTICE` に上流と著作権者。**古い版の表記は古い**(更新を勧めると CHANGELOG)。
- 配布物: 0.3.2 の wheel・sdist・crate には LICENSE が無かった(npm には有った)。**0.5.0 以降は wheel の `dist-info/licenses/`、sdist、crate に `LICENSE`・`NOTICE`(・`LICENSE-THIRD-PARTY.md`)が入る**。依存に単独の GPL/LGPL/AGPL は無い(0.3.2 の SBOM 282 個)。
- 幾何の出所: GEOS 由来を退け、JTS 1.20.0(EDL-1.0)の移植と、クリーンルームの独立実装に置き換えた。「技術的な目録で、法的な確認ではない」と作者が明記(`kcai:terrio-geometry-provenance-and-clean-room`)。
- AI の開示: README・`acknowledgements.md` が「主に Claude Opus 5.5 で、人の指示とレビューのもと」と明記。謝辞は Whitebox、GDAL・PROJ・PDAL ほか。引用は `citation.md`(Zenodo の DOI、Wu & Fitzgerald 2026)。
- 詳細: `kcai:terrio-license-and-third-party-notices`、`kcai:terrio-ai-disclosure-and-acknowledgements`

# /assets/known-quirks
- status: verified(日本語パスは played、他は read-source。volatile)
- **文字列をバイト位置で切る型の欠陥**: 0.3.2 で 3 か所を踏んだ(GeoJSON の日付の判定、CSV、Zarr の名前解析)。前 2 つは 0.4.0 で直り、**Zarr の `t[..5]` は 0.7.0 でも残る**(日本語で始まる相対パス)。
- `unsafe` は約 70 行(JPEG 2000 の FFI、SQLite のロック・mmap、SSE 命令など)、`panic!(` は約 65。`.unwrap()` は多い(試験コードを含む)。CLI は 8 MiB のスタックで実行し、起動に失敗したら呼び出しスレッドで実行する。リソース超過は `ResourceLimitError`(Python では `MemoryError`)で返る(0.6.0)。
- ドキュメントの食い違い(0.3.2 で 14 件)の多くは、その後の版で直った。
- 詳細: `kcai:terrio-source-quirks`、`kcai:japanese-path-panic-in-zarr-parse-name`

# /assets/version-notes
- status: stated(CHANGELOG の読み。動かしたものは該当の `/assets/…` に)。volatile
- **0.8.0〜0.9.0 の主な変更**: 0.9.0 の破壊的変更 — `TERRIO_ALLOWED_DRIVERS` が空・空白・非 UTF-8 なら**何も許可しない**(全許可にするには未設定にする)、ネイティブの GML バイト出力は ZIP ではなく単独の XML、`terrio.rio` の COG ライターは driver が `COG`、`terrio.rio` の巨大な窓読みは `ResourceLimitError`(`MemoryError`)、`terrio.pyogrio` の無名 SQLite バッファは `.gpkg` / `.mbtiles` の名前が要る、Rust API の `read_geoparquet_sparse` が引数 `columns` を取る、`FlatGeobufInfo` に `has_z` `has_m`、Krovak の WKT1 の軸の既定が南西に。新機能 — `terrio.pyogrio`(GeoParquet を Arrow で読む)、ワイルドカード入力(`mosaic` `warp` `concat` ほか。`terrio mosaic 'tiles/*.tif' out.tif`)、GeoParquet の範囲読み込み・列の選択、`TERRIO_HTTP_FOLLOW_CROSS_ORIGIN=NO`(別オリジンへの転送を拒否)、`TERRIO_HTTP_CAINFO`(追加の CA バンドル)、`TERRIO_TIFF_MAX_CHUNK_BYTES`、OSM PBF の純 Rust の復号。0.8.0 — Zarr(分割・shard)の遠隔読みの高速化と、遠隔 Zarr を開くときのメタデータ要求の削減、`translate` の窓のバンドをまとめて読む。
- **0.10.0 の主な変更(`stated`)**: 破壊的変更 — **PROJ 文字列の未知の楕円体・データム・単位名(`+ellps=foo`、`+units=feet`)は、WGS 84・メートル・0 として読まず拒否**、廃止された EPSG コードは置き換え先ではなく**自身の定義**を保つ、CRS の表が **EPSG v13.102(PROJ 9.9.0)**に、新しい外部 `.ovr` は `INTERLEAVE=BAND`、Zstandard は `libzstd` なしで `zrip`(`ZSTD_LEVEL` が 4 まで効く)、Rust API の構造体にフィールド追加。新機能 — xarray の `.terrio` アクセサが `dem`・`sieve`・`proximity`・`fill_nodata`・`reclassify`・`viewshed`・`polygonize`・`contour`・`footprint`・`zonal_stats` を実行、ベクタ入力は WKT・GeoJSON・Shapely・境界の箱などなんでも受け付ける、`terrio zonal-stats` が `.zarr` のキューブで出力、`rasterize --background`(既存の DEM を標高属性で編集)、npm の `terrio-js/cog` と `terrio-js/geoparquet`、GRIB の遅延読みの改善、GeoParquet の GeoArrow 点の高速化、`terrio-js` の `openUrl` の要求数削減。
- 使い方への影響: Python の `terrio.rio` を使うコードは、COG の `driver`、巨大な窓の例外の型が変わる。`TERRIO_ALLOWED_DRIVERS` を設定している環境は、空文字だと全拒否になる。
- 詳細: CHANGELOG(v0.9.0、v0.8.0)

# /assets/comparison-with-alternatives
- status: stated(作者の整理 + この宇宙の確認)
- terrio は「GDAL の結果を基準に、よく使う形式の入出力・変換・再投影を、純 Rust で」行うもので、**GDAL の全部の置き換えではない**。選び分け: ライブラリを入れられない、WebAssembly で動かしたい、`gdal_translate` / `ogr2ogr` を置き換えたい → terrio。多くの形式、最速の処理、格子つきの測地変換、File Geodatabase・MrSID・HDF4・データベース → GDAL。
- 価値: GDAL を入れられない場所(クラウドのセッション、ブラウザ、サーバーレス、CI)で、`pip install` だけで GDAL 相当ができる。
- 詳細: `kcai:why-terrio-comparison-with-alternatives`、`kcai:terrio-possibilities-and-risks`

# /assets/governance-and-evolution
- status: verified(git の読み)/ derived(方向の読み)。volatile
- main の動き(0.7.0 の後、2026-11-08 までに 55 コミット、`stated`): 性能の改善が中心(Deflate 書き込みを libdeflate の純 Rust 移植に、HTTP 接続プールの共有、`dem`・`zonal`・`warp` の高速化)、`terrio.dev/web`(ブラウザの CLI)、タイル生成の拡張(子タイルから下位ズーム、WebP のディレクトリタイル)、KMZ・FlatGeobuf・GeoPackage の堅牢化(不完全なレコードを拒否、SQLite の文字コード)、新しい貢献者(Nicolas Karasiak、Eduardo Lacerda ほか)。
- 運営: 単独の作者(Qiusheng Wu)が短い間隔で多数のコミットを出す形から、0.5.0 以降は**貢献者が約 20 人**に増えた。報告への対応は速い(#159 → #161 は翌日)。貢献の指針: GDAL との比較(実ファイルで)、純 Rust のまま(C が要る依存は不可、WebAssembly でもビルド可)、公開項目はすべて文書化、GDAL の名前に合わせる。「GDAL と違う読み方をするファイルを付けたバグ報告が特に役に立つ」。
- 方向(derived): ①GDAL / PROJ / PDAL / rasterio「と同じ答え」を機能ごとに積む、②読み込み・変換から解析・可視化・SQL へ広げる、③クラウドネイティブの読みを形式ごとに「その場」へ、④メモリを抑えた流し読み・書きと WebAssembly(小型化・スレッド・4 GB 超)、⑤窓口と配布を増やす(MCP、rio、xarray、Docker、AUR/COPR)、⑥C 依存なしと出所の整理。**ROADMAP に日本語エンコーディング・タイル生成・日本ローカルは載っていない**(0.5.0 時点で grep)。
- main の動き(0.7.0 → 0.9.0): 295 コミット、約 +13.5 万行(全体)。GeoParquet の範囲読み込み、`warp` の既定の変更、pyogrio 互換、安全側の制限(STAC の資格情報、HTTP の別オリジン)が目立つ。
- 規模: v0.4.2 で Rust 約 10.3 万行(本体)、v0.7.0 の全体で約 12.4 万行超。0.5.0 → 0.7.0 の 11 日で 231 コミット・約 +34 万行(ドキュメントやデータを含む)。
- 起源: 2026-10-14 開始。Whitebox の `wbraster`/`wbvector`/`wbprojection` の上に始まった。
- 詳細: `kcai:terrio-contributing-and-governance`、`kcai:terrio-evolution-0-3-2-to-0-4-2`、`kcai:terrio-roadmap-and-open-items`、`kcai:terrio-source-scale-and-origins`

# /assets/play-dataset-licenses
- status: stated(配信元の表示を読んだだけ。利用条件の解釈ではない)
- 表示: Sentinel-2 L2A の STAC `license` は `proprietary`(ESA の Legal Notice)。Overture は出典ごとに異なる(CDLA Permissive 2.0、ODbL、CC BY 4.0 など)。Source Cooperative の日本の建物(5 GB)は ODbL v1.0。Protomaps の terrarium は多数の出典を列挙。**国土数値情報 N03(depot.optgeo.org)の利用条件は未確認**。NZ の建物(Hugging Face)はカードに `license: mit` のみで元の出どころは未記載。NOAA HRRR の Zarr、Autzen の COPC、UScounties.fgb、PROJ の格子は未確認。
- **データ本体はリポジトリに入れていない**。このリポジトリの CC0 は、terrio(MIT)や遊びで使ったデータには適用されない。
- 詳細: `kcai:data-licenses-of-play-datasets`

# /decision-support/possibilities-and-risks
- status: derived
- 可能性: GDAL を入れられない場所での GDAL 相当(クラウドのセッション、ブラウザ、サーバーレス、CI)。ブラウザでの範囲読み込み。MCP で AI エージェントに道具として渡せる。幾何の検査・修復と解析が 1 つの道具に(0.5.0〜)。
- リスク: 日本語の入力(Zarr の相対パスの panic)。**黙って誤る**挙動(`.cpg` の無い CP932、COG の `TILING_SCHEME` の黙殺)。変化の速さ(版ごとに挙動が動く)。AI 製で歴史が短い(実データでの経験が少ない)。ライセンス表記の変化(古い版は古い)。HTTPS が一部の CPU で panic しうる。CLI の FlatGeobuf・GeoParquet が全量取得。
- 直ったリスク(0.7.0): 南極点の EPSG:3857、CP932(`.cpg` あり)。
- 詳細: `kcai:terrio-possibilities-and-risks`

# /traces/version-rechecks
- status: verified(経過)
- 2026-10-21 0.3.2 で初回の確認(25 ページのドキュメント、実データ、GDAL 3.8.4 との突き合わせ)。10-24 に 0.4.2、0.5.0(`stale` を解消)。11-04 に 0.7.0(南極点・CP932・docs の例が直っていたことを確認。縮小が概観から読める)。11-07 に、動かしていなかった領域(GRIB・遠隔 Zarr・STAC POST・OGC API Features・WFS・等高線・SQL・ブラウザの CLI)を 0.7.0 で確かめた(`plays/2026-11-07-catch-up.md`)。各回の記録は `plays/`(`/inventory/plays-index`)。

# /traces/gdal-comparison-environments
- status: verified
- GDAL 3.8.4 / PROJ 9.4(apt)は terrio の基準(3.12)より古く、挙動が違う項目があった(`--ot Int16`)。2026-10-22 に conda-forge で GDAL 3.13.3 / PDAL 2.10.2 を入れて再確認した(COPC・`filter range`・STACIT は一致)。apt の GDAL には SQLite 方言の `ST_*` と Parquet ドライバーが無く、幾何の比較は Python から GEOS を直接呼んだ。

# /traces/grib-zarr-viewshed-zonal
- status: verified
- 2026-11-27 に、GRIB の値、遠隔 Zarr の値、`viewshed`、`zonal-stats` を GDAL 3.13.3 と比べた（`plays/2026-11-27-grib-zarr-viewshed-zonal.md`）。値はすべて一致。Zarr だけ行の向きが違う（terrio は北が上に並べ替える）。

# /traces/raster-tiles-comparison
- status: verified
- 2026-11-27 に `terrio tile` を `gdal2tiles` と比べた（`plays/2026-11-27-raster-tiles.md`）。タイル集合は同じ、最大ズームは画素ほぼ一致、低ズームは平均 2.5〜4.5 階調の差。

# /traces/catch-up-0-10-0
- status: verified
- 2026-11-27 に 0.10.0（0.9.0 から 205 コミット）を確認した（`plays/2026-11-27-0-10-0-catch-up.md`）。0.9.0 の挙動（GeoParquet の範囲読み込み、`warp` の既定の差）は変わらず。**ジオイドの値が JPGEO2024 から GSIGEO2011 になり GDAL 3.13.3 と一致、ネットワークが要る**。**terrio-js の退行は残る**。確認用のスクリプト（`scripts/compare_with_gdal.py`、`run_notebook_cells.py`、`check_terrio_js_node.mjs`）をリポジトリに足した（作業用ファイルが環境の掃除で消えたため）。

# /traces/catch-up-0-9-0
- status: verified
- 2026-11-19 に 0.8.0・0.9.0（0.7.0 から 295 コミット）を確認した（`plays/2026-11-19-0-9-0-catch-up.md`）。**GeoParquet が CLI でも範囲読み込みに**、**`warp` の既定が GDAL と画素一致しなくなった**、**terrio-js 0.9.0 が大きなラスタ PMTiles で panic**、STAC の資格情報つきアセットの拒否。日本語の相対パス（Zarr）、`--dstalpha`、COG の `TILING_SCHEME`、FlatGeobuf の CLI は残る。

# /traces/maplibre-rendering
- status: verified
- 2026-11-19 に、terrio・tippecanoe・GDAL のベクタタイルを MapLibre で描いて画素を比べた（`plays/2026-11-19-maplibre-rendering.md`）。多角形と線は同じ見え方、点だけ間引きの差。

# /traces/tile-generation-deep-dive
- status: verified
- 2026-11-08 に「terrio は tippecanoe の代わりになるか」を、tippecanoe 2.49.0(apt)と GDAL 3.8.4 の MVT ライターで比べた(`plays/2026-11-08-tile-generation.md`)。多角形は一致、密な点の間引きは無い。ドキュメントを読むと、terrio の書き出しが GDAL の MVT ライターの再現だと分かり、それが実測と合った。

# /lessons/read-the-reference-implementation
- status: derived(根拠: `/traces/tile-generation-deep-dive`)
- 機能の理解は、①ドキュメントが「何の再現か」を読み(ここでは GDAL の MVT ライター)、②同じ入力でその参照実装と、さらに**利用者が置き換えたい別の道具**(tippecanoe)の両方と比べると速い。「できる」より「何と同じで、何と違うか」が分かる。

# /traces/kcaim-assessment
- status: verified
- 2026-11-05 に kcai の木を 1 つの kcaim ファイルにするかを検討し(案 A〜D)、蒸留した試作を作った。2026-11-07 に hfu が**木を miso/terrio.md に移し、それを正本とする**案を示した。経緯と判断は `miso/ASSESSMENT.md`。

# /lessons/master-and-archive
- status: derived(根拠: `/traces/kcaim-assessment`)
- 木(kcai 形式の踏み跡 46 本)は、2026-11-07 時点の terrio 0.7.0 の確認で**凍結した記録**として残し、新しい知識はこのファイルに書く。凍結した木は、詳しい手順・再現の根拠として `kcai:<id>` から辿れる(GitHub の `knowledge/`)。

# /acceptance-tests/remote-grib-and-zarr
- query: NOAA の GRIB2 や公開 S3 の Zarr を、丸ごと取らずに読めるか
- expected: 0.7.0 で、GRIB は範囲読み込み(696 バンドの `info` が約 7 MiB、1 バンドの窓は約 0.8 MiB の追加)。S3 の Zarr(`ZARR:"/vsis3/…"`、`AWS_NO_SIGN_REQUEST=YES`)は `info` が通る
- requires: /assets/cloud-native-reads
- result: untested

# /acceptance-tests/api-sources
- query: OGC API Features・WFS・STAC の POST 検索から、terrio で読めるか
- expected: 0.7.0 で、`OAPIF:`(pygeoapi の demo)と `WFS:`(mapserver の demo、1.1.0)、`STACIT:…method=POST`(Earth Search)が動く。認証が要る API は未確認
- requires: /assets/cloud-native-reads
- result: untested

# /acceptance-tests/windows-arm64-and-install
- query: terrio を Windows ARM64 で `pip install` できるか。Docker では
- expected: 0.5.0 以降の PyPI に Windows ARM64 の wheel がある(0.3.2 にはなかった)。0.6.0 から `ghcr.io/opengeos/terrio` の Docker イメージ。確かめたのは PyPI のファイル一覧で、実機では動かしていない
- requires: /assets/install-and-distribution
- result: untested

# /acceptance-tests/formats-list
- query: terrio は FileGDB・GRIB・DXF・WFS を読めるか
- expected: FileGDB ラスタは不可(宣言)。GRIB1/2 は 0.5.0 から可。DXF(CAD)は一部、WFS は 0.6.0 から(`stated`。動かしていない)
- requires: /assets/formats-and-io
- result: untested

# /acceptance-tests/raster-tiles
- query: terrio でラスタのタイル（z/x/y.png）を作れるか。gdal2tiles と同じか
- expected: `terrio tile` でできる。タイル集合は gdal2tiles と同じ。最大ズームは画素ほぼ一致、低ズームは平均 2.5〜4.5 階調の差（0.10.0、1 つの入力で）
- requires: /assets/raster-tiles
- result: untested

# /acceptance-tests/grib-zarr-values
- query: GRIB と遠隔 Zarr の値は GDAL と同じか。Zarr の窓の指定は同じ番号で良いか
- expected: 値は一致（GRIB 4 バンド、HRRR の窓）。**Zarr は行の向きが違う**（GDAL は南が上のまま、terrio は北が上）ので、同じ `--srcwin` は別の地点。座標で合わせる
- requires: /assets/cloud-native-reads
- result: untested

# /acceptance-tests/viewshed-zonal
- query: 視域と多角形ごとの統計は GDAL と同じ結果か
- expected: `viewshed` は 4 つのモードとも `gdal_viewshed` と画素一致、`zonal-stats` は `gdal raster zonal-stats` と全桁一致（0.10.0、1 つの DEM・3 つの多角形で）
- requires: /assets/processing-and-geometry
- result: untested

# /acceptance-tests/mcp-tools
- query: AI エージェントに terrio を道具として渡せるか。ツールの数は
- expected: `terrio mcp`(0.4.0 から配布版)。0.7.0 で 99 ツール、各ツールは `args`(引数の配列)を取る。書き込みは一時的な場所に限る
- requires: /assets/interfaces
- result: untested

# /acceptance-tests/pure-rust-claim
- query: terrio は本当に C 依存がないか
- expected: 0.3.2 は完全には純ではなかった。0.6.0 から既定のビルドは C 依存なし(`libzstd` は任意)。HTTPS は一部の CPU で panic しうる
- requires: /assets/architecture
- result: untested

# /acceptance-tests/dataset-license
- query: 遊びに使った公開データを再利用してよいか
- expected: 範囲外(示唆あり)。配信元の表示は `/assets/play-dataset-licenses` にあるが、利用条件の解釈はしない。国土数値情報の条件は未確認
- requires: /assets/play-dataset-licenses
- result: untested

# /inventory/verification-coverage
- status: volatile
- 版: **0.10.0**(2026-11-27。再実行: 既知の穴、画素の比較 19 項目、GeoParquet・FlatGeobuf、COG の窓と縮小、ノートブック 26 セル、MCP、terrio-js の Node 確認、ジオイド)。0.9.0(2026-11-19)。0.7.0 での確認（11-04、11-07）のうち、0.9.0 で再実行したのは「既知の穴」「画素の比較」「GeoParquet・FlatGeobuf」「ノートブック」「terrio-js の 6 試料」「MCP」「STAC POST」「遠隔 Zarr」「OGC API」「GRIB の info」。それ以外は 0.7.0 の値。0.7.0 での確認（11-04、11-07）の記述。移植元の踏み跡 46 本のうち、`stale` は 0 本。ただし**動かして確かめ直したのは一部**で、ほかは見出しと CHANGELOG を読んだだけ(`/open-questions/unverified-0-7-0-areas`)。

# /inventory/upstream-drafts
- status: volatile
- 有効な下書き 3 件(Zarr の日本語パス、COG の `TILING_SCHEME` と `--dstalpha`、CLI の FlatGeobuf の全量取得)。取り下げ 6 件(ジオイド、`--ot Int16`、南極点、docs/rust.md、CP932、CSV の追記)。投稿済み 1 件(#159)。投稿は hfu。

# /inventory/plays-index
- status: volatile
- 作業の記録(`plays/`): 2026-10-21 の first-contact、japan-edge-cases-and-survey、untested-items、upstream-feedback-loop、license-and-basics、gdal-comparison、notebooks、rust-and-notebooks。10-22 の gdal-313-pdal-comparison。10-24 の 0-4-2-recheck、0-5-0-recheck。11-04 の 0-7-0-recheck。上流への下書きは `drafts/upstream/`(一覧は `README.md`)。

# /inventory/sync-status
- status: volatile
- このファイルが**正本**。`knowledge/` は凍結した記録(0.7.0、2026-11-04)。**移植は 2026-11-07 に行った**。ただし、蒸留による要約なので、木の数値の表や再現の手順は、必要なら `kcai:<id>` を読む。移植した範囲は、`/assets/…` の各オブジェクトの「詳細」が指す。

# /inventory/next-actions
- status: volatile
- ⓪機能の理解を深める順(`/inventory/feature-depth`)。①盲検の実行(別のエージェントに、受け入れテストの節と結果を除いたコピーを渡して質問し、`result` を記入)。②人による確認。③新版(0.7.0 より後)が出たら `/procedures/recheck-on-new-version`。④動かしていない領域(`/open-questions/unverified-0-7-0-areas`)を動かして、`/assets/…` に反映する。⑤大きさの管理(下の `/inventory/size`)。

# /inventory/feature-depth
- status: volatile
- 機能の理解の深さ(2026-11-27)。**深い**(動かして参照実装と比べた): COG・PMTiles・FlatGeobuf・GeoParquet の読み込み方、日本の座標変換・文字、ラスタ処理(GDAL と画素一致。`warp` の既定は不一致)、幾何の修復(GEOS と一致)、COPC・`filter range`(PDAL と一致)、STACIT(GDAL と一致)、ベクタタイル書き出し(GDAL・tippecanoe と、MapLibre での見え方まで)、**ラスタタイル `terrio tile`(gdal2tiles と)**、**GRIB の値(GDAL と)**、**遠隔 Zarr の値(GDAL と。行の向きが違う)**、**`viewshed` と `zonal-stats`(GDAL と)**。**浅い**(動かしたが比較は未実施): OGC API Features、WFS、等高線の値(本数のみ)、SQL、`preview`、MCP の書き込み、新しい点群フィルタ、xarray の `.terrio` アクセサの新しい操作(0.10.0)。**未着手**: STACTA、`terrio tile` の GTiff / WebP / `--webviewer`、Windows / macOS。
- 次に深める候補(dwg7 の判断に効く順): ①等高線の値と SQL の空間関数を GDAL(`gdal_contour`・SpatiaLite)と比べる、②xarray の `.terrio` アクセサ(0.10.0 の `dem` `viewshed` `zonal_stats` ほか)、③点群フィルタ(PDAL と)、④OGC API Features・WFS の値

# /inventory/size
- status: volatile
- 2026-11-08 時点で約 480 行・約 5 万字(蒸留した木の要点)。**肥大化の目安**: 約 900 行を超えたら、一部の `/assets/…` を `kcai:` の木や別ファイルに戻す、または読み方の地図を置く(CONCEPT §8、§12-6)。

# /system-record/agent-contract-reminder
- status: normative
- 再掲: 答えには terrio の版を添える。更新したら、統合した正本の全文を `.md` の添付で返す(`/system-record/agent-contract`)。
