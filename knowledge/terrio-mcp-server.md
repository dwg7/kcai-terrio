---
id: terrio-mcp-server
title: terrio の MCP サーバー（terrio mcp）：配布版にはなく、main にある
status: stale
terrio_version: 0.3.2
terrio_commit: cf6bd5dbcb6021f99ffde6c7f2c0f4f3f311ed2b
interface: mcp
environment: Claude Code クラウドセッション（Linux x86_64、Python 3.13.16）
authors:
  - hfu の指示のもと、AI（Claude）が実施・記述。AI 支援あり
reviewed_by: []
updated: 2026-10-21
verified_on: 2026-10-21
verified_how: played
sources:
  - plays/2026-10-21-untested-items.md（5、6）
  - terrio docs/mcp.md（main）
  - crates/terrio-cli/src/mcp.rs（main）
related: [terrio-release-vs-main-drift, terrio-cli-overview, japanese-path-panic-in-zarr-parse-name, terrio-possibilities-and-risks]
freshness: high
---

## 要点

`terrio mcp` は、terrio のコマンドを AI エージェントに渡す MCP サーバー（標準入出力）。**PyPI の 0.3.2 には入っておらず、main（`cf6bd5d`）にある**。main を `cargo build --release -p terrio-cli` でビルドし（6 分 33 秒）、JSON-RPC を直接話して動作を確かめた。ツールは 15 個で、引数は「コマンドライン引数の文字列配列」。**各呼び出しは別プロセスで動くので、panic しても、サーバーは落ちずに `isError` を返す。**

## やり方

```sh
# main をビルド（Rust が要る）
git clone --depth 1 https://github.com/opengeos/terrio && cd terrio
cargo build --release -p terrio-cli          # target/release/terrio
# Claude Code に登録（ドキュメントの手順。このセッションでは試していない）
claude mcp add terrio -- terrio mcp
```

JSON-RPC の例（`initialize` → `notifications/initialized` → `tools/list` → `tools/call`）:

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"info","arguments":{"args":["B04.tif"]}}}
```

## 確かめたこと（何をして、何が起きたか）

- `initialize`: `serverInfo` が `terrio` / `0.3.2`、`protocolVersion 2025-03-26`、`capabilities.tools`。
- `tools/list`: `info` `convert` `formats` `crs` `rasterize` `polygonize` `translate` `warp` `mosaic` `dem` `calc` `proximity` `sieve` `grid` `filter`（`mcp` と `help` は除く）。入力スキーマは `{"args": string[]}`。**説明は各コマンドの `--help` 全文**なので、AI は全オプションを見られる。
- `tools/call` `info`（ローカルの GeoTIFF）: 成功。`crs`（`EPSG:6668 → EPSG:6677`、東京駅）: `-5992.919570392903 -35363.23774493004`。`formats`: 50 行。
- 存在しないファイル: `isError: true` と `terrio: 'nonexist.tif' does not exist`、`(terrio info failed with exit code 1)`。
- 日本語の相対パス（`日本地図.tif`）: `isError: true` で panic のメッセージとバックトレースが返る。**サーバーは生きている**。絶対パスなら成功。

## 気をつけること

- **配布版では使えない**。main のビルドか、次のリリースを待つ。
- MCP 経由でも、日本語の相対パスの panic は起きる（絶対パスで渡すよう、AI に指示する）。
- ツールは**書き込みもできる**（`convert` など）。出力先をこのリポジトリの一時的な場所に限る（`AGENTS.md` の方針）。認証情報は渡さない。
- バックトレースが長く、AI の文脈を食う（41 行ほど）。
- Claude Code への実登録と、AI が自律的に使う場面は**未試験**。

## 出典

- https://terrio.opengeos.org/mcp/ （main）
- plays/2026-10-21-untested-items.md
