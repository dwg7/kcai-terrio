#!/usr/bin/env python3
"""kcaim ファイルの最小の検査（dwg7/kcaim CONCEPT §5.3）。標準ライブラリのみ。

使い方: python3 scripts/check_kcaim.py kcaim/terrio.md
エラー（終了コード 1）: UTF-8 でない、空、第 1 レベル見出しが `# /...` でない、重複。
警告: 内部パス参照が解決しない、`result:` の語が宣言外、status の語が語彙外。
"""
import re
import sys
from pathlib import Path

RESULTS = {"pass", "partial", "fail", "volatile", "untested"}
STATES = {"verified", "derived", "normative", "open", "volatile", "stated", "recalled", "secondary"}


def main(path):
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"エラー: {path}: {e}")
        return 1
    if not text.strip():
        print(f"エラー: {path}: 空")
        return 1
    errs, warns = [], []
    heads = re.findall(r"^# (.*)$", text, re.M)
    seen = {}
    for h in heads:
        if not h.startswith("/"):
            errs.append(f"第 1 レベル見出しが `# /...` でない: {h}")
        elif h in seen:
            errs.append(f"第 1 レベル見出しが重複: {h}")
        seen[h] = True
    # コードブロック内の `# ` は数えない簡易検査は省略（このファイルは使っていない）
    paths = set(heads)
    for m in re.finditer(r"`(/[a-z0-9][a-z0-9\-/]*)`", text):
        p = m.group(1)
        if p not in paths and not any(h.startswith(p + "/") for h in paths) and p.count("/") >= 1:
            warns.append(f"内部パス参照が見つからない: {p}")
    for m in re.finditer(r"^- result: (\S+)", text, re.M):
        if m.group(1) not in RESULTS:
            warns.append(f"結果の語が宣言外: {m.group(1)}")
    for m in re.finditer(r"^- status: ([a-z]+)", text, re.M):
        if m.group(1) not in STATES:
            warns.append(f"状態の語が語彙外: {m.group(1)}")
    for e in errs:
        print("エラー:", e)
    for w in sorted(set(warns)):
        print("警告:", w)
    print(f"{path}: 第 1 レベル見出し {len(heads)} 個、エラー {len(errs)}、警告 {len(set(warns))}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "kcaim/terrio.md"))
