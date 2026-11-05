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
- concept-version: dwg7/kcaim の CONCEPT.md、2026-11-04(コミット a9bfc83)
- 種別: **探索・理解型**(terrio を理解し比較する)に、**運用型**の層(dwg7 の地理空間の前処理を terrio で置き換えられるかの判断支援)を載せる。
- 作成: hfu の指示のもと、AI(Claude)が書いた。**人による内容確認は未了**。`dwg7/kcai-terrio` の踏み跡 46 本(`knowledge/`)から蒸留した試作(2026-11-05)。
- 範囲: terrio 0.3.2〜0.7.0(2026-10-20〜11-03)の挙動。確かめた版は各オブジェクトに書く。
- 範囲外: ①terrio の最新版(0.7.0 より新しい版)。②GDAL・PROJ・PDAL そのものの使い方。③terrio の内部設計の評価、法的な判断(ライセンスの適否)。④日本以外のデータの網羅的な確認。⑤terrio への投稿・働きかけ(人が個人として行う)。
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
- `dwg7/kcai-terrio` は kcai の形式(1 ファイル 1 主題の踏み跡、`knowledge/`、47 本)で、日々更新される**作業の木**である。このファイルは、そこから**蒸留した携帯用の版**で、境界つきのエージェントが 1 ファイルで使えるようにする。
- kcai の「踏み跡」は共有の単位(確かめた経路)で、このファイルの `/sources/…` と `/assets/…` に当たる。このファイルの `/traces/…` は**運用の踏み跡**(作業で起きたこと)で、kcai-terrio の `plays/` と `DECISIONS.md` に当たる(`dwg7/kcaim` の CONCEPT §7.1)。
- 個々の踏み跡の id は、このファイル内で `kcai:<id>`(例: `kcai:cloud-native-read-behavior-matrix`)と書いて指す。`knowledge/<id>.md` を開くと、元の詳しい記述と確かめた手順がある。
- 木とこのファイルが食い違うときは、**木が新しい**(`/inventory/sync-status`)。

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
- 最新: 0.7.0(2026-11-03)。リリース履歴: 0.3.2=10-20、0.4.0〜0.4.2=10-22、0.5.0=10-24、0.6.0=10-31、0.6.1=11-01、0.7.0=11-03

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
- 変化の速さ: **volatile**。答えは版つきで。
- 既定のビルドは C 依存なし(0.6.0〜)。CRS は独立した crate `terrio-crs`。
- ライセンス: 0.6.0 から MIT AND MPL-2.0(点群の固有値ソルバーが MPL-2.0)。幾何は JTS の移植か独立実装(`kcai:terrio-geometry-provenance-and-clean-room`)。古い版は古い表記(`kcai:terrio-license-and-third-party-notices`)。

# /assets/cloud-native-reads
- status: verified(版つき。volatile)
- 目的: ファイルを丸ごとダウンロードせずに、どこまで読めるか。**インターフェースで違う。**
- 範囲読み込みする(verified):
  - **COG**: CLI で窓(Sentinel-2 の 512²)が 3 要求・約 6.1 MiB(0.7.0)。`convert --overview N`(0 始まり、0 が最大の概観)は 1373² で約 2.5 MiB。**`translate --outsize 512 512`(縮小)は 0.7.0 で 0.69 MiB**(0.3.2 は約 208 MiB だった)。
  - **PMTiles**: CLI と JS で範囲読み込み(国土数値情報 3,625 地物の `info` が約 1.5 MiB)。
  - **COPC / JP2 / Zarr(一部)**: 範囲読み込み(0.3.2 で確認)。
- **インターフェースで違う(verified)**: FlatGeobuf と GeoParquet は、**terrio-js の `openUrl` が bbox で範囲読み込み**(FlatGeobuf 768 KiB、5 GB の GeoParquet が 16.4 MiB・7 要求、0.7.0 で確認)。**CLI と Python は全量取得**(FlatGeobuf は 0.7.0 でも約 14 MB を受け取る。GeoParquet の 5 GB は 0.3.2 で 221 MB まで書いて停止)。中断すると `/tmp/terrio-*` に一時ファイルが残る(0.3.2)。
- STAC: `STACIT:` で検索結果をモザイクとして開く。東京の窓 512² で、全アイテム 17.5 MiB、`max_items=1` で 6.25 MiB(0.4.2)。GDAL の STACIT と画素一致。
- 詳細: `kcai:cloud-native-read-behavior-matrix`、`kcai:cog-remote-window-overview-and-warp`、`kcai:pmtiles-remote-reading`、`kcai:terrio-js-cloud-native-reads-in-browser`、`kcai:terrio-stac-and-stacit`

# /assets/japan-local
- status: verified(版つき。volatile)
- 日本語の文字列: GeoJSON / CSV の日本語長文字列で panic したのは **0.3.2 まで**(#159)。**0.4.0 以降は通る**(Shapefile・FlatGeobuf・GeoPackage・PMTiles・GeoParquet・CSV)。
- **Zarr の日本語の相対パス**: `terrio info 日本語/a.zarr` が **0.7.0 でも panic**(`zarr.rs` の `t[..5]`)。絶対パスと書き出しは通る。
- Shapefile の CP932: **`.cpg` が `CP932` なら 0.7.0 で読める**(0.3.2〜0.5.0 は文字化け)。`.cpg` が無ければ文字化け(GDAL も同じ)。
- 座標変換: JGD2011(`EPSG:6668`)→ 平面直角第IX系(`EPSG:6677`)は (139.767125, 35.681236) → **(−5992.919570392903, −35363.23774493004)**。GDAL と小数 9 桁以上で一致、0.3.2〜0.7.0 で同じ。旧日本測地系(`EPSG:4301` → `6668`)も約 1e-9 で一致(0.3.2)。
- ジオイド: **3 次元** `EPSG:6667 → 6697`(高さ 50)で 13.2386(JPGEO2024 を適用。GDAL 3.13.3 はネットワークありで GSIGEO2011 を使い 13.3375)。**2 次元の `EPSG:6668` では高さは変わらない**(GDAL も同じ)。(`kcai:vertical-datum-grids-and-geoid-in-japan`)
- 詳細: `kcai:geojson-japanese-string-panic`、`kcai:japanese-path-panic-in-zarr-parse-name`、`kcai:shapefile-cp932-attributes-not-decoded`、`kcai:jgd2011-plane-rectangular-transform`

# /assets/processing-and-geometry
- status: verified(GDAL 3.8.4 との比較。volatile)
- ラスタ処理: `dem`(hillshade・slope・aspect・TRI・TPI・roughness、multidirectional、compute-edges)、`translate`(srcwin・outsize・ot/scale)、`warp`(near・bilinear・cubic・average)、`calc`、`proximity`、`sieve`、`mosaic`、`rasterize`、COG 書き出しは、**GDAL 3.8.4 と画素が完全一致**(20 項目。0.3.2〜0.7.0 で繰り返し確認)。
- 幾何(0.5.0 から): `is-valid`・`make-valid`・`clean`・`buffer`・`overlay`・`dissolve` ほか。ちょうちょ形の不正ポリゴンで、修復・バッファ・ディゾルブが **GEOS と一致**(0.5.0 と 0.7.0)。実装は JTS の移植・クリーンルームに置き換わった(`kcai:terrio-geometry-provenance-and-clean-room`)。
- 形式の往復: Zarr・JPEG 2000・COG を terrio が書き、GDAL が画素一致で読む(0.4.2)。PMTiles(MVT)を GDAL が読める(0.3.2)。COPC と `filter range` は PDAL 2.10.2 と点数・統計が一致(0.3.2)。
- **まだ残る差**(0.7.0): `warp --dstalpha` が無い。COG の `TILING_SCHEME=GoogleMapsCompatible` を黙って無視する(画素サイズ 12.32 m のまま)。
- 詳細: `kcai:terrio-vs-gdal-spot-checks`、`kcai:terrio-processing-commands-smoke-test`、`kcai:terrio-conformance-and-testing-against-gdal`

# /assets/interfaces
- status: verified(一部 stated)
- Python: 公式ノートブック 2 本(quickstart・xarray)のコードセル 13 個ずつが全成功(0.7.0)。xarray のノートブックは `terrio[xarray]` に **`zarr` が入らない**ので別途 `pip install zarr`。`terrio.rio`(rasterio 互換)と `terrio-rio` コマンドがある。
- JavaScript/WebAssembly: terrio-js 0.7.0 の公開ページで、座標変換・日本語の文字列・6 つの範囲読み込みの試料が動く(実ブラウザ)。
- MCP: `terrio mcp` は 99 ツール(0.7.0)。各ツールは `args`(コマンドラインの配列)を取る。書き込みは一時的な場所に限ること。
- Rust: 0.4.0 から feature で絞れる。ドキュメントの依存の版が古かった(`"0.3"`)のは 0.7.0 で直った。
- 詳細: `kcai:terrio-python-api`、`kcai:terrio-xarray-integration`、`kcai:terrio-mcp-server`、`kcai:terrio-js-api-and-playground`、`kcai:terrio-rust-library-and-features`、`kcai:terrio-rio-rasterio-compatible-api`

# /scenarios/dwg7-tile-and-prep-workflow
- status: derived
- 背景: dwg7 / hfu の公開リポジトリは、タイル配信(PMTiles・Martin・MapLibre)と、その前処理(ogr2ogr・tippecanoe・gdal_translate・gdalwarp)が中心。
- terrio で**置き換えられる見込み**(verified の裏づけつき): ラスタの再投影・圧縮・窓・縮小・形式変換、ベクタの形式変換と属性の選択、日本語属性の変換(0.4.0 以降)、`.cpg` つきの CP932 の Shapefile(0.7.0)、幾何の検査・修復。
- **置き換えにくい**: タイル生成(tippecanoe 相当。PMTiles 書き出しは可能だが、属性の間引きやズーム別の単純化は未確認)、Zarr の日本語の相対パス、CLI の FlatGeobuf・GeoParquet の部分読み。
- 詳細: `kcai:hfu-dwg7-workflow-substitution-survey`

# /decision-support/advice-for-dwg7
- status: derived(根拠は `/assets/…`、`kcai:advice-for-dwg7`)
- 1. 範囲読み込みを使うなら、**ブラウザ(terrio-js)**が最も効く。CLI・Python の FlatGeobuf / GeoParquet は全量取得。
- 2. 縮小は 0.7.0 以降なら `translate --outsize` でよい。古い版は原寸を読む。
- 3. **GDAL を捨てない。**新しい工程に入れるときは、小さな入力で GDAL と並べる(新旧の GDAL で)。
- 4. CP932 の Shapefile は `.cpg` を付ける。日本語の Zarr は絶対パスで。
- 5. **版を固定**し、`scripts/recheck_known_issues.sh` で既知の穴を確かめる。
- 6. 上流への報告は、再現の最小化・GDAL との突き合わせ・版の明記をして、**人が投稿**する。投稿が遅れると、他の人に先に直される。

# /procedures/recheck-on-new-version
- status: normative
- terrio の新版(PyPI・crates.io・npm)が出たら: ①CHANGELOG と docs の差分を読む。②新版の wheel で `scripts/recheck_known_issues.sh` を実行する。③画素の比較(`dem` ほか)・公式ノートブック・terrio-js の公開ページを再実行する。④確かめられなかった項目は `volatile`(kcai-terrio では `stale`)にする。⑤`kcai:advice-for-dwg7` と、このファイルの `/acceptance-tests/…` を更新する。
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
- status: open
- terrio の PMTiles 書き出しは、tippecanoe の属性間引き・ズーム別単純化の代わりになるか。未確認。

# /open-questions/unverified-0-7-0-areas
- status: open
- 0.7.0 で動かして確かめていない領域: 遠隔 Zarr、STAC の POST と Planetary Computer、STACTA、GRIB、新しい点群フィルタ、WFS / OGC API Features、プレイグラウンド、ベンチマークの数値、Windows / macOS。

# /open-questions/reviewed-by
- status: open
- どの踏み跡を、誰が `reviewed` にするか(hfu の判断待ち。`QUESTIONS.md`)。

# /acceptance-tests/geoparquet-bbox-without-download
- query: 5 GB の GeoParquet の一部を、丸ごとダウンロードせずに bbox で読めるか
- expected: ブラウザ(terrio-js の `openUrl`)なら読める(約 16 MiB・7 要求)。CLI・Python は全量取得(版つきで)
- requires: /assets/cloud-native-reads
- result: untested
- freshness: terrio の新版ごとに CLI の挙動を確認

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
- expected: PMTiles の書き出しはできるが、tippecanoe の属性の間引きやズーム別の単純化の代わりになるかは未確認(`/open-questions/tile-generation`)
- requires: /assets/cloud-native-reads, /scenarios/dwg7-tile-and-prep-workflow
- result: untested

# /acceptance-tests/pixel-identical-to-gdal
- query: terrio の dem・warp・translate は GDAL と同じ画素を出すか
- expected: 20 項目で GDAL 3.8.4 と完全一致(warp の地理変換は 2e-9 m 以内)。dstalpha と TILING_SCHEME は差が残る
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

# /inventory/verification-coverage
- status: volatile
- 版: 0.7.0(2026-11-04)。踏み跡 46 本(`knowledge/`)のうち、`stale` は 0 本。ただし**動かして確かめ直したのは一部**で、ほかは見出しと CHANGELOG を読んだだけ(`/open-questions/unverified-0-7-0-areas`)。

# /inventory/upstream-drafts
- status: volatile
- 有効な下書き 3 件(Zarr の日本語パス、COG の `TILING_SCHEME` と `--dstalpha`、CLI の FlatGeobuf の全量取得)。取り下げ 6 件(ジオイド、`--ot Int16`、南極点、docs/rust.md、CP932、CSV の追記)。投稿済み 1 件(#159)。投稿は hfu。

# /inventory/sync-status
- status: volatile
- この試作は、`dwg7/kcai-terrio` の 2026-11-05 時点の木(`knowledge/`)から手で蒸留した。木が更新されたら、このファイルの版つきの事実を見直す必要がある(自動の生成は未実装。`kcaim/ASSESSMENT.md`)。

# /inventory/next-actions
- status: volatile
- ①盲検の実行(別のエージェントに、テストの節と結果を除いたコピーを渡して質問し、`result` を記入)。②人による `reviewed`。③木からの再生成の手順を決める。

# /system-record/agent-contract-reminder
- status: normative
- 再掲: 答えには terrio の版を添える。更新したら、統合した正本の全文を `.md` の添付で返す(`/system-record/agent-contract`)。
