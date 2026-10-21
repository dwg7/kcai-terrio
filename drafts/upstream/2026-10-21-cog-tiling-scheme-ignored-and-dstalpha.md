# Draft question/request for opengeos/terrio (not posted; hfu will review and post)

**Title:** COG creation option `TILING_SCHEME=GoogleMapsCompatible` is silently ignored (and `warp` has no `--dstalpha`)

Hello, and thank you for terrio. I am replacing a GDAL pipeline that makes web-map-friendly COGs, and I found two small gaps. I am not sure whether they are planned, so I write them as a question.

## Version

terrio 0.3.2 (PyPI wheel, Linux x86_64) and main at `6779102` (2026-10-21, built from source). Both behave the same.

## 1. `TILING_SCHEME` is ignored without a message

```sh
terrio warp --t-srs EPSG:3857 B04.tif w3857.tif -r bilinear
terrio convert w3857.tif cog.tif -f COG --co TILING_SCHEME=GoogleMapsCompatible
terrio info cog.tif    # Pixel size: (12.32192258630899, -12.32192258630899), 1 overview
```

GDAL's COG driver would reproject/align to the Web Mercator tile grid (pixel size from a zoom level, and `ZOOM_LEVEL_STRATEGY`, `ALIGNED_LEVELS`). terrio accepts the option and writes a normal COG with the source pixel size.
It would help to either support it or print a warning/error for unsupported COG creation options, because the result looks valid.

## 2. `warp` has no `--dstalpha`

```sh
terrio warp --t-srs EPSG:3857 B04.tif wa.tif --dstalpha
# error: unexpected argument '--dstalpha' found
```

`gdalwarp -dstalpha` is common when reprojecting to Web Mercator (the area outside the source becomes transparent).

Thank you for your work. I hope this is useful.
