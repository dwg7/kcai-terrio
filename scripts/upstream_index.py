#!/usr/bin/env python3
"""drafts/upstream/ の下書きから、状態の一覧と、GitHub の「新しい issue」リンクを作る。

使い方: python3 scripts/upstream_index.py > drafts/upstream/README.md
投稿は hfu が確認して行う（AGENTS.md）。リンクはタイトルと本文を埋めた新規 issue の画面を開くだけで、投稿はしない。
標準ライブラリのみ。
"""
import re
import sys
from pathlib import Path
from urllib.parse import quote

REPO = "opengeos/terrio"
D = Path(__file__).resolve().parent.parent / "drafts" / "upstream"
# ファイル名 -> (状態, 補足)。状態: posted / obsolete / ready
STATUS = {
    "2026-10-21-geojson-panic-on-multibyte-strings.md": ("posted", "hfu が #159 として投稿。作者が #161（baf4768）で修正。配布版は未リリース"),
    "2026-10-21-comment-on-159-csv-same-code.md": ("obsolete", "CSV も #161 で直ったので不要"),
    "2026-10-21-zarr-parse-name-panic-on-multibyte-path.md": ("ready", "日本語の相対パスで panic。最新 main（6779102）でも再現。**#159 と同じ型で、最優先**"),
    "2026-10-21-shapefile-cp932-not-decoded.md": ("ready", "CP932 の Shapefile が黙って文字化け。最新 main でも同じ。GDAL 3.8.4 と 3.13.3 は正しく読む（確認済み）"),
    "2026-10-21-jgd2011-geoid-heights-unchanged.md": ("obsolete", "取り下げ。2 次元の EPSG:6668 を使った誤り。3 次元の 6667 なら適用される（GDAL とも一致）"),
    "2026-10-21-web-mercator-fails-at-south-pole.md": ("ready", "緯度 -90 の点（南極）を EPSG:3857 に変換すると失敗。GDAL は成功。入門の例と PMTiles 既定の書き出しに影響。GDAL 3.8.4 と 3.13.3 で確認済み"),
    "2026-10-21-translate-ot-int16-leaves-out-of-range-nodata.md": ("obsolete", "取り下げ。GDAL 3.13.3 は terrio と同じく範囲外の nodata を残す（3.8.4 だけ丸める）"),
    "2026-10-21-cog-tiling-scheme-ignored-and-dstalpha.md": ("ready", "質問・要望（GDAL 3.8.4 と 3.13.3 で比較済み）。TILING_SCHEME が黙って無視される、--dstalpha がない"),
    "2026-10-21-cli-range-reads-for-flatgeobuf-and-geoparquet.md": ("ready", "質問。CLI の FlatGeobuf / GeoParquet は全量取得（JS 版は範囲読み）。中断時の一時ファイル"),
}
LIMIT = 7000  # GitHub の URL 長の実用的な上限の目安（超えたら貼り付けで投稿）


def split(text):
    m = re.search(r"^\*\*Title:\*\*\s*(.+)$", text, re.M)
    title = m.group(1).strip() if m else ""
    body = text[m.end():].lstrip("\n") if m else text
    return title, body.rstrip() + "\n"


def main():
    out = ["# 上流（opengeos/terrio）への報告の下書き", "",
           "投稿は **hfu が確認して行う**（`AGENTS.md`）。このファイルは `scripts/upstream_index.py` で作る。",
           "リンクは、タイトルと本文を埋めた「新しい issue」の画面を開く（開くだけで、投稿はされない）。URL が長すぎるものは、下書きの本文を貼り付ける。", "",
           "| 状態 | 下書き | タイトル | 補足 | 投稿用 |", "|---|---|---|---|---|"]
    for name, (st, note) in STATUS.items():
        p = D / name
        title, body = split(p.read_text(encoding="utf-8"))
        link = ""
        if st == "ready":
            url = f"https://github.com/{REPO}/issues/new?title={quote(title)}&body={quote(body)}"
            link = f"[新しい issue]({url})" if len(url) <= LIMIT else f"（長いので貼り付け: [空の issue](https://github.com/{REPO}/issues/new)）"
        out.append(f"| {st} | [{name}]({name}) | {title} | {note} | {link} |")
    out += ["", "状態: `posted` 投稿済み、`ready` 投稿待ち、`obsolete` 不要になった。",
            "投稿したら、`STATUS` の状態と補足（issue 番号）を直して、このファイルを作り直す。", ""]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
