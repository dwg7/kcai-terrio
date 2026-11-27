#!/usr/bin/env python3
"""terrio と GDAL の画素を、小さな公開データで突き合わせる（kcai-terrio の確認用）。

使い方:
  PATH=<GDAL の bin>:<terrio の bin>:$PATH python3 scripts/compare_with_gdal.py [--workdir DIR]
terrio（CLI と Python）と gdaldem / gdal_translate / gdalwarp / gdal_calc.py / gdal_proximity.py /
gdal_sieve.py / gdal_rasterize が PATH にあること。入力は、公開の COG（Sentinel-2、USGS 3DEP）の窓を
terrio で取り出して作る。一時ファイルは --workdir（既定: 一時ディレクトリ）に作り、終わりに消す。
"""
import argparse, shutil, subprocess, sys, tempfile, os
import numpy as np
import terrio

S2 = "https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/54/S/UE/2026/10/S2C_54SUE_20261018_0_L2A/%s.tif"
DEM = "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/1/TIFF/current/n40w106/USGS_1_n40w106.tif"
COUNTRIES = "https://raw.githubusercontent.com/opengeos/data/main/world/countries.geojson"


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        print("  失敗:", cmd[:90], "|", (r.stderr or r.stdout)[-120:].strip().replace("\n", " "))
    return r.returncode == 0


def rd(f):
    return np.asarray(terrio.open_raster(f).read(1), dtype="float64")


def cmp(name, a, b, tol=0.0):
    if a.shape != b.shape:
        print(f"DIFF  {name}: 形が違う terrio {a.shape} gdal {b.shape}")
        return False
    both = np.isnan(a) & np.isnan(b)
    d = np.abs(a - b)
    d[both] = 0
    n = int((d > tol).sum())
    print(f"{'SAME ' if n == 0 else 'DIFF '} {name}: 差のある画素 {n}/{a.size}、最大差 {np.nanmax(d):.6g}")
    return n == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir")
    a = ap.parse_args()
    wd = a.workdir or tempfile.mkdtemp(prefix="cmp-")
    os.makedirs(wd, exist_ok=True)
    os.chdir(wd)
    print("terrio:", terrio.__version__, "|", subprocess.run("gdalinfo --version", shell=True, capture_output=True, text=True).stdout.strip())
    ok = sh(f"terrio translate {S2 % 'B04'} B04.tif --srcwin 5000 5000 512 512") and sh(f"terrio translate {S2 % 'B08'} B08.tif --srcwin 5000 5000 512 512") and sh(f"terrio translate {DEM} dsm.tif --srcwin 2000 1500 140 140")
    if not ok:
        print("入力の取得に失敗（通信を確認）")
        return 2
    res = []
    for m in ["hillshade", "slope", "aspect", "TRI", "TPI", "roughness"]:
        sh(f"terrio dem {m} dsm.tif t_{m}.tif"); sh(f"gdaldem {m.lower()} dsm.tif g_{m}.tif -q")
        res.append(cmp(f"dem {m}", rd(f"t_{m}.tif"), rd(f"g_{m}.tif"), 1e-4 if m in ("slope", "aspect") else 0))
    sh("terrio dem hillshade dsm.tif t_ms.tif --multidirectional"); sh("gdaldem hillshade -multidirectional dsm.tif g_ms.tif -q")
    res.append(cmp("dem hillshade multidirectional", rd("t_ms.tif"), rd("g_ms.tif")))
    sh("terrio translate B04.tif t_w.tif --srcwin 100 50 200 150"); sh("gdal_translate -q -srcwin 100 50 200 150 B04.tif g_w.tif")
    res.append(cmp("translate srcwin", rd("t_w.tif"), rd("g_w.tif")))
    sh("terrio translate B04.tif t_o.tif --outsize 100 100 -r bilinear"); sh("gdal_translate -q -outsize 100 100 -r bilinear B04.tif g_o.tif")
    res.append(cmp("translate outsize bilinear", rd("t_o.tif"), rd("g_o.tif")))
    for policy, flag, env in (("既定", "", ""), ("--grid-invariant false", "--grid-invariant false", "")):
        for r in ["near", "bilinear", "cubic", "average"]:
            sh(f"terrio warp B04.tif t_{r}.tif --t-srs EPSG:6677 --tr 10 10 -r {r} {flag}"); sh(f"gdalwarp -q -overwrite B04.tif g_{r}.tif -t_srs EPSG:6677 -tr 10 10 -r {r}")
            res.append(cmp(f"warp {r}（{policy}）", rd(f"t_{r}.tif"), rd(f"g_{r}.tif")))
    sh('terrio calc -A B08.tif -B B04.tif --calc "(A.astype(float)-B)/(A+B)" --type Float32 t_ndvi.tif')
    sh('gdal_calc.py -A B08.tif -B B04.tif --calc "(A.astype(float)-B)/(A+B)" --outfile g_ndvi.tif --type Float32 --quiet')
    res.append(cmp("calc NDVI", rd("t_ndvi.tif"), rd("g_ndvi.tif")))
    sh("terrio sieve B04.tif t_s.tif --st 20"); sh("gdal_sieve.py -q -st 20 B04.tif g_s.tif")
    res.append(cmp("sieve st=20", rd("t_s.tif"), rd("g_s.tif")))
    print(f"\n{sum(res)}/{len(res)} が一致（作業ディレクトリ: {wd}）")
    if not a.workdir:
        shutil.rmtree(wd, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
