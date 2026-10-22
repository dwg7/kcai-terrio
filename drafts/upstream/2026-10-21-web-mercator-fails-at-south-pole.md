# Draft issue for opengeos/terrio (not posted; hfu will review and post)

**Title:** Reprojecting to EPSG:3857 fails for features that touch latitude -90 (e.g. Antarctica in Natural Earth); GDAL succeeds

Hello, and thank you for terrio. While following the getting-started page with a world countries file, I hit an error that GDAL does not have. I am not sure what the intended behavior is, so I write what I saw.

## Version

terrio 0.3.2 (PyPI wheel, Linux x86_64). Same on main at `6779102` (2026-10-21). Compared with GDAL 3.8.4 / PROJ 9.4 (Ubuntu apt) and with GDAL 3.13.3 (conda-forge); both convert the same input without error.

## Minimal reproduction

`pt.geojson`: one point at the south pole corner of the longitude/latitude grid.

```json
{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[180,-90]}}]}
```

```sh
terrio convert pt.geojson out.geojson --t-srs EPSG:3857
# terrio: coordinate reference system: failed to reproject feature 0 of layer 'pt': coordinate reference system: cannot transform (180, -90)

ogr2ogr -f GeoJSON out.geojson pt.geojson -t_srs EPSG:3857
# succeeds: [ 20037508.342789243906736, -242528680.943742722272873 ]
```

A polygon with a vertex at (-10, -90) fails the same way in terrio and succeeds in ogr2ogr. In practice the whole Natural Earth countries layer (177 features, Antarctica is feature 159) fails to convert to EPSG:3857.

## Why it matters

- The default PMTiles write (EPSG:3857) of a world layer fails for the same reason.
- The getting-started example with a world countries file hits it (as far as I could tell by following it).

## Question

Would it be acceptable to follow GDAL here (the value at -90 is large but finite), or to clamp/skip such vertices with a warning, instead of failing the whole conversion? A workaround for users is `--where "NAME <> 'Antarctica'"`.

Thank you for your work. I hope this is useful.
