#!/usr/bin/env python3
"""公式ノートブック（docs/notebooks/*.ipynb）のコードセルを順に実行し、成功・失敗を数える。

使い方: python3 scripts/run_notebook_cells.py quickstart.ipynb [xarray.ipynb ...]
`%pip` のセルは飛ばす。描画は Agg。作業は一時ディレクトリで行う。xarray のノートブックには
zarr パッケージが要る（`terrio[xarray]` には入らない）。
"""
import ast, json, os, sys, tempfile, time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def run(path):
    nb = json.load(open(path))
    ns, ok, bad = {}, 0, 0
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code":
            continue
        src = "".join(c["source"])
        if src.lstrip().startswith("%pip"):
            continue
        t = time.time()
        try:
            tree = ast.parse(src)
            last = ast.Expression(tree.body.pop().value) if tree.body and isinstance(tree.body[-1], ast.Expr) else None
            exec(compile(tree, "c", "exec"), ns)
            if last:
                eval(compile(last, "c", "eval"), ns)
            ok += 1
        except BaseException as e:
            bad += 1
            print(f"  [{i}] 失敗 {time.time()-t:.1f}s {type(e).__name__}: {str(e)[:200]}")
        plt.close("all")
    print(f"{os.path.basename(path)}: 成功 {ok}、失敗 {bad}")
    return bad


if __name__ == "__main__":
    paths = [os.path.abspath(p) for p in sys.argv[1:]]
    os.chdir(tempfile.mkdtemp(prefix="nb-"))
    sys.exit(1 if sum(run(p) for p in paths) else 0)
