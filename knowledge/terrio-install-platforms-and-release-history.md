---
id: terrio-install-platforms-and-release-history
title: terrio の入れ方、対応環境、版の履歴（PyPI・npm・crates.io）
status: stale
terrio_version: 0.3.2
terrio_commit: 6779102281ad2835cbc23fba3138e01a138bc6f9
interface: cli
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
as_of: 2026-10-21
sources:
  - terrio docs/installation.md（main 6779102）
  - PyPI の JSON（https://pypi.org/pypi/terrio/json）、npm のレジストリ（terrio-js）、crates.io の API
  - plays/2026-10-21-license-and-basics.md
related: [terrio-license-and-third-party-notices, terrio-release-vs-main-drift, terrio-cli-overview, terrio-mcp-server]
freshness: high
---

## 要点

terrio は、**PyPI（`pip install terrio`）、crates.io（`cargo add terrio` / `cargo install terrio-cli`）、npm（`terrio-js`）** の 3 つで配られ、システムの依存（GDAL、PROJ、GEOS、SQLite）は要らない。Python は 3.10 以上（abi3 の wheel）。**ドキュメントの対応環境の記述は、PyPI の 0.3.2 より先行している**（Windows ARM64 の wheel など）。**2026-10-14 から 6 日で 0.1.1 → 0.3.2** と、変化がとても速い。

## やり方

```sh
pip install --upgrade terrio       # このリポジトリの基本（PyPI の配布物）
terrio --version                   # 0.3.2
# 公式のインストーラ（curl | sh）、cargo binstall terrio-cli、cargo install terrio-cli もある（このリポジトリでは使わない）
```

- ドキュメントの方法: インストーラ（`install.sh` / `install.ps1`、SHA-256 の検査つき、`TERRIO_VERSION`、`TERRIO_INSTALL_DIR`）、`pip` / `uv tool` / `pipx`、`cargo binstall`、`cargo install`（Rust 1.90 以上）。
- WebAssembly: npm の `terrio-js`、または Pyodide の wheel（GitHub のリリースに添付、0.2.0 から。Pyodide 0.29、Python 3.13。**未確認**）。
- GDAL バックエンドは **PyPI の wheel に含まれない**（ソースから `--features gdal` でビルド）。

## 確かめたこと（何をして、何が起きたか）

**PyPI（played / JSON を読んだ）**: `requires_python >=3.10`、`License-Expression: MIT`。依存は `numpy>=1.21` と `affine>=2.3`（追加: `geopandas`、`plot`（matplotlib）、`test`、`xarray`（xarray と dask）の extras）。wheel は `cp310-abi3` で、**インストールした wheel は 18.3 MB**。

| 版 | PyPI の公開（UTC） | PyPI のファイル |
|---|---|---|
| 0.1.1 | 2026-10-15 00:16 | 7（sdist + macOS Intel / arm64、manylinux x86_64 / aarch64、musllinux x86_64、Windows x64） |
| 0.2.0 | 2026-10-15 13:52 | 9（musllinux aarch64 が増える） |
| 0.3.1 | 2026-10-17 15:52 | 9 |
| 0.3.2 | 2026-10-20 03:22 | 9（sdist + 8 つの wheel） |

- **PyPI に 0.3.0 と 0.1.0 はない**。npm には 0.0.0-stage（10-14 23:09）、0.1.0（10-14 23:10）、0.1.1（10-15 00:12）、0.2.0（10-15 13:41）、0.3.0（10-17 14:44）、0.3.1（10-17 15:47）、0.3.2（10-20 03:22）。crates.io は最初の公開が 10-14 23:04 で、0.1.1、0.2.0、0.3.0、0.3.1、0.3.2 がある（全部 MIT）。**3 つの配布先で、版の集合が違う**。
- **0.3.2 の wheel は 8 つ**: macOS（Intel、arm64）、manylinux（x86_64、aarch64）、musllinux（x86_64、aarch64）、Windows x64。**Windows ARM64 の wheel は、PyPI の 0.3.2 にない**（`installation.md` は「Windows（x64 と ARM64）」と書く）。ドキュメントが配布版より先行している例。
- **インストーラ**（`curl | sh`）は、検査のため読んでいない。「Linux x86_64 / aarch64（静的）、macOS Intel / Apple silicon、Windows x64 / ARM64 の単体バイナリ」と書かれている（read-docs）。
- 要件: ビルド済みのバイナリや wheel はシステムの依存なし。ソースからのビルドは Rust 1.90 以上（`docs/contributing.md` の MSRV 方針と一致）。

## 気をつけること

- **版の数字だけでは、同じものか分からない**: PyPI と crates.io と npm で、同じ版番号でも公開されている集合が違う。main の `Cargo.toml` も 0.3.2 のまま進む（`terrio-release-vs-main-drift`）。
- Pyodide の wheel は、リモート URL を読めない（WebAssembly に HTTP クライアントがないため。`pyodide.http` で先に取る）。terrio-js の `openUrl` とは別の話。
- 6 日で 5 版の頻度なので、**版を固定して使い、遊ぶたびに版を記録する**（`AGENTS.md`）。
- このセッションでは、PyPI の wheel だけを使った。CLI のバイナリ、cargo、npm の CLI 以外の経路は、main のビルドと terrio-js 以外は試していない。

## 出典

- https://terrio.opengeos.org/installation/
- https://pypi.org/project/terrio/ 、https://www.npmjs.com/package/terrio-js 、https://crates.io/crates/terrio
- plays/2026-10-21-license-and-basics.md
