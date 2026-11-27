#!/usr/bin/env python3
"""terrio の点群フィルタを PDAL と、同じ入力・同じ引数で突き合わせる（kcai-terrio の確認用）。

使い方: PATH=<pdal の bin>:<terrio の bin>:$PATH python3 scripts/compare_pointcloud_filters.py input.laz [--workdir DIR]
出力の追加の次元（PDAL の CamelCase と terrio の snake_case は、小文字・下線なしで照合）と、点数・Classification の
最小・最大・平均を比べる。入力は、terrio で COPC から切り出す（例: terrio convert URL sub.laz --bounds ... --resolution 5）。
"""
import argparse, json, os, re, subprocess, sys, tempfile

STD = {"x", "y", "z", "intensity", "returnnumber", "numberofreturns", "scandirectionflag", "edgeofflightline",
       "classification", "synthetic", "keypoint", "withheld", "overlap", "scananglerank", "scanangle", "userdata", "pointsourceid",
       "gpstime", "red", "green", "blue", "scanchannel", "nir"}

# (名前, terrio の引数, PDAL の引数)
CASES = [
    ("lof", "filter lof", "-f filters.lof --filters.lof.minpts=10"),
    ("nndistance", "filter nndistance", "-f filters.nndistance"),
    ("radialdensity", "filter radialdensity", "-f filters.radialdensity"),
    ("reciprocity", "filter reciprocity", "-f filters.reciprocity"),
    ("eigenvalues", "filter eigenvalues", "-f filters.eigenvalues"),
    ("covariancefeatures", "filter covariancefeatures", "-f filters.covariancefeatures"),
    ("normal", "filter normal", "-f filters.normal"),
    ("approximatecoplanar", "filter approximatecoplanar", "-f filters.approximatecoplanar"),
    ("estimaterank", "filter estimaterank", "-f filters.estimaterank"),
    ("skewnessbalancing", "filter skewnessbalancing", "-f filters.skewnessbalancing"),
    ("iqr", "filter iqr --dimension Z", "-f filters.iqr --filters.iqr.dimension=Z"),
    ("mad", "filter mad --dimension Z", "-f filters.mad --filters.mad.dimension=Z"),
    ("csf", "filter csf", "-f filters.csf"),
    ("elm", "filter elm", "-f filters.elm"),
    ("hag_delaunay", "filter hag_delaunay", "-f filters.hag_delaunay"),
    ("zsmooth", "filter zsmooth --dim Z", "-f filters.zsmooth --filters.zsmooth.dim=Z"),
    ("head", "filter head --count 1000", "-f filters.head --filters.head.count=1000"),
    ("tail", "filter tail --count 1000", "-f filters.tail --filters.tail.count=1000"),
    ("sort", "filter sort --dimensions Z", "-f filters.sort --filters.sort.dimension=Z"),
    ("voxeldownsize", "filter voxeldownsize --cell 2", "-f filters.voxeldownsize --filters.voxeldownsize.cell=2"),
    ("voxelcenternearestneighbor", "filter voxelcenternearestneighbor --cell 2", "-f filters.voxelcenternearestneighbor --filters.voxelcenternearestneighbor.cell=2"),
    ("sample", "filter sample --radius 2", "-f filters.sample --filters.sample.radius=2"),
]


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode == 0, (r.stderr or r.stdout)[-160:].strip().replace("\n", " ")


def norm(n): return re.sub(r"[^a-z0-9]", "", n.lower())


def stats(path):
    r = subprocess.run(f"pdal info --stats {path}", shell=True, capture_output=True, text=True)
    try:
        s = json.loads(r.stdout)["stats"]["statistic"]
    except Exception:
        return None
    return {norm(d["name"]): d for d in s}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("input"); ap.add_argument("--workdir")
    a = ap.parse_args()
    wd = a.workdir or tempfile.mkdtemp(prefix="pcf-"); os.makedirs(wd, exist_ok=True)
    inp = os.path.abspath(a.input)
    same = tot = 0
    for name, t_args, p_args in CASES:
        t_out, p_out = f"{wd}/t_{name}.laz", f"{wd}/p_{name}.laz"
        ok_t, et = sh(f"terrio {t_args} {inp} {t_out}")
        ok_p, ep = sh(f"pdal translate {inp} {p_out} {p_args} --writers.las.extra_dims=all")
        if not (ok_t and ok_p):
            print(f"SKIP  {name}: terrio {'OK' if ok_t else '失敗: '+et[:70]} / pdal {'OK' if ok_p else '失敗: '+ep[:70]}")
            continue
        st, sp = stats(t_out), stats(p_out)
        if not st or not sp:
            print(f"SKIP  {name}: 統計を取れない"); continue
        nt, npd = int(next(iter(st.values()))["count"]), int(next(iter(sp.values()))["count"])
        dims = sorted(d for d in (set(st) & set(sp)) if d not in STD or d == "classification")
        diffs = []
        for d in dims:
            for k in ("minimum", "maximum", "average"):
                x, y = st[d][k], sp[d][k]
                if abs(x - y) > 1e-6 * max(1.0, abs(y)):
                    diffs.append(f"{d}.{k} {x:.6g}≠{y:.6g}")
        only_t = sorted(set(st) - set(sp) - STD); only_p = sorted(set(sp) - set(st) - STD)
        tot += 1; good = (nt == npd and not diffs); same += good
        print(f"{'SAME ' if good else 'DIFF '} {name}: 点数 terrio {nt} / pdal {npd}、比べた次元 {len(dims)}"
              + (f"、差: {'; '.join(diffs[:3])}" if diffs else "") + (f"、terrio のみの次元 {only_t}" if only_t else "") + (f"、PDAL のみの次元 {only_p}" if only_p else ""))
    print(f"\n{same}/{tot} が一致（作業ディレクトリ: {wd}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
