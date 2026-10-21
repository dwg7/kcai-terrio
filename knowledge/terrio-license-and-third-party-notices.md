---
id: terrio-license-and-third-party-notices
title: terrio のライセンス：MIT、同梱される依存と第三者の告知、0.3.2 の配布物に LICENSE がない件
status: draft
terrio_version: 0.3.2
terrio_commit: 6779102281ad2835cbc23fba3138e01a138bc6f9
interface: rust
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - opengeos/terrio の LICENSE、NOTICE、LICENSE-THIRD-PARTY.md、README の License、Cargo.toml、python/pyproject.toml（main 6779102、#164）
  - PyPI の terrio 0.3.2（wheel の METADATA と sboms/terrio-py.cyclonedx.json、sdist）、crates.io の terrio 0.3.2、npm の terrio-js 0.3.2（jsDelivr）
  - plays/2026-10-21-license-and-basics.md
related: [terrio-ai-disclosure-and-acknowledgements, data-licenses-of-play-datasets, terrio-install-platforms-and-release-history, terrio-release-vs-main-drift]
freshness: high
---

## 要点

**terrio は MIT ライセンス（Copyright (c) 2026 Qiusheng Wu）。** 本体の 4 つの宣言（リポジトリの `LICENSE`、`Cargo.toml`、PyPI の `License-Expression`、npm の `license`）はすべて MIT で一致している。依存（wheel の SBOM で 282 個）に、単独の GPL / LGPL / AGPL はない。**ただし 0.3.2 の wheel、sdist、crate には LICENSE ファイルが入っていない**（npm の `terrio-js` には入っている）。main の #164 で、`NOTICE` と `LICENSE-THIRD-PARTY.md` が追加され、配布物に同梱される予定で、**未リリース**。これは技術的な読みで、**法的助言ではない**。

## やり方（確かめ方）

```sh
# 宣言の確認
pip show terrio                          # License-Expression: MIT（METADATA）
ls <site-packages>/terrio-0.3.2.dist-info   # licenses/ がない（0.3.2）
# 依存のライセンス（wheel に入っている SBOM。CycloneDX 1.5）
python3 -c "import json;d=json.load(open('…/dist-info/sboms/terrio-py.cyclonedx.json'));print(len(d['components']))"
```

## 確かめたこと（何をして、何が起きたか）

**本体のライセンスの宣言（4 か所一致）**

- リポジトリ `LICENSE`: "MIT License / Copyright (c) 2026 Qiusheng Wu"。`Cargo.toml`（ワークスペース）と `python/pyproject.toml` が `license = "MIT"`。crates.io の 0.1.1〜0.3.2 は全版 MIT。PyPI の `License-Expression: MIT`。npm の `package.json` が `"license": "MIT"`。

**0.3.2 の配布物の LICENSE ファイル（played）**

| 配布物 | LICENSE | 確かめ方 |
|---|---|---|
| PyPI の wheel（`cp310-abi3-manylinux_2_17_x86_64`） | **なし**（`dist-info` に `licenses/` がない） | 入れて `ls` |
| PyPI の sdist（`terrio-0.3.2.tar.gz`、259 ファイル） | **なし**（README だけ） | 取得して `tar tzf` |
| crates.io の `terrio-0.3.2` | **なし**（`Cargo.toml` と `Cargo.toml.orig` だけ。マニフェストに `license = "MIT"`） | `download` して `tar tzf` |
| npm の `terrio-js@0.3.2` | **あり**（`package.json` の `files` に書かれていないが、LICENSE が配られている） | jsDelivr で取得 |

- #164（main、2026-10-21）のコミットメッセージにも「published wheels carried no license file」とある。#164 は、`LICENSE`、`NOTICE`、`LICENSE-THIRD-PARTY.md` を wheel、sdist、npm、CLI のアーカイブに、`LICENSE` と `NOTICE` を crate に同梱する。**PyPI はまだ 0.3.2 で、この変更は未リリース**。

**第三者の告知（main の `NOTICE`、read-docs）**

- **PROJ**（MIT 系）: `crates/terrio/src/crs/` の投影と格子の補間は PROJ からの移植。
- **CSF**（Apache-2.0、北京師範大学）: 地面分類の `csf.rs` は PDAL が同梱するコードの移植（変更あり）。
- **EPSG Geodetic Parameter Dataset**（IOGP の著作権）: `epsg.tsv.zst` と `datums.tsv.zst` は、IOGP の利用条件に従い、帰属表示つきで再配布。「EPSG そのものではなく、IOGP の推奨を受けているわけでもない」とある。
- **Esri の projection engine data**（Apache-2.0）: `esri.tsv.zst` など。
- ほか: rasterio（BSD-3-Clause、Mapbox）、rioxarray（Apache-2.0）、Apache Arrow の NOTICE、IJG の表記（`jpeg-encoder`）。`LICENSE-THIRD-PARTY.md` は `cargo-about` で生成し、リリースの試走で最新か検査する。

**依存のライセンス（wheel の SBOM、played）**: `sboms/terrio-py.cyclonedx.json`（CycloneDX 1.5）に **282 コンポーネント**（名前は 255 種。同じクレートの 2 版を含む）。

| ライセンス表記（SPDX） | 数 | 例 |
|---|---|---|
| `MIT OR Apache-2.0` | 156 | hdf5-reader、netcdf-reader など |
| `MIT` | 45 | terrio 自身の 3 つ（terrio、terrio-cli、terrio-py）を含む |
| `Apache-2.0` | 14 | arrow-buffer、arrow-ipc など |
| `Apache-2.0 OR MIT` | 11 | autocfg など |
| `BSD-3-Clause` | 8 | snap、subtle など |
| `Unlicense OR MIT` | 4 | aho-corasick、memchr、byteorder |
| `BSD-2-Clause` | 4 | flatgeobuf、numpy、openjp2、rusty_av1d |
| `WTFPL` | 4 | osmpbfreader（2 版）、par-map、pub-iterator-type |
| `ISC` | 3 | delaunator、rustls-webpki、untrusted |
| その他の組み合わせ | 33 | Zlib、0BSD、CC0-1.0（2）、`Apache-2.0 AND ISC`（ring）、`(MIT OR Apache-2.0) AND IJG`（jpeg-encoder）など |

注意が要る表記（SBOM のまま）:

- `self_cell`: `Apache-2.0 OR GPL-2.0-only`（選択式。Apache-2.0 を選べる）
- `smartstring`: `MPL-2.0+`（弱いコピーレフト。ファイル単位）
- `webpki-roots`: `CDLA-Permissive-2.0`
- WTFPL の 4 つ（FSF は自由と認めるが、OSI の承認はない）
- **GPL / LGPL / AGPL だけのものは、この SBOM にはない**（上の表と、GPL・MPL の文字列検索で確認）

## 気をつけること

- **配布物を再配布する人は、0.3.2 の wheel / sdist / crate に LICENSE がない**ことを知っておく。MIT は「著作権表示と許諾表示を、コピーに含める」ことを条件とする。リポジトリの `LICENSE` を別に添えるのが無難（法的な判断は専門家に）。
- SBOM は **Python の wheel のもの**。npm の WebAssembly 版（HTTP のクライアントなどが違う）、CLI のアーカイブ、Pyodide の wheel の依存は**確かめていない**。
- `LICENSE-THIRD-PARTY.md`（main）の中身は、集計していない（SBOM の集計だけ）。
- **このリポジトリ（kcai-terrio）は CC0 で、terrio のコードやデータを複製していない**。ドキュメントは要約して出典を示す（短い引用にとどめる）。ドキュメント単独のライセンス表示は、見つからなかった（リポジトリ全体が MIT の下）。
- 新しい版が出たら、LICENSE の同梱、SBOM の中身（特にコピーレフト）を確かめ直す。

## 出典

- https://github.com/opengeos/terrio/blob/main/LICENSE 、/NOTICE 、/LICENSE-THIRD-PARTY.md
- https://pypi.org/project/terrio/0.3.2/ 、https://crates.io/crates/terrio/0.3.2 、https://www.npmjs.com/package/terrio-js
- plays/2026-10-21-license-and-basics.md
