# Draft question for opengeos/terrio (not posted; hfu will review and post)

**Title:** Question: will the CLI/Python get the range-request FlatGeobuf and GeoParquet readers that terrio-js has? (and an interrupted download leaves its temp file)

Hello, and thank you for terrio. terrio-js is impressive: with `openUrl`, it reads a 5 GB GeoParquet by bbox with 7 requests (16.4 MiB), and a 14 MB FlatGeobuf by bbox with 768 KiB. I noticed that the CLI and Python behave differently for the same URLs, so I would like to ask about the plan.

## Versions

terrio 0.3.2 (PyPI wheel), terrio-js 0.3.2, and main at `6779102` (2026-10-21, built from source).

**Rechecked 2026-10-24:** terrio 0.4.2 (PyPI wheel): the CLI still downloads the whole FlatGeobuf (`UScounties.fgb`, 14,100,008 bytes) for a bbox query; I did not re-run the 5 GB GeoParquet.

## What I measured

| input | CLI / Python | terrio-js `openUrl` |
|---|---|---|
| FlatGeobuf (14 MB, `flatgeobuf.org/test/data/UScounties.fgb`), bbox | whole file, 13.8 MiB (`terrio convert --spat ...`, one `(whole file)` GET) | 4 requests, 768 KiB |
| GeoParquet (5 GB, Source Cooperative `…/country_iso=JPN/JPN.parquet`), small bbox | whole file download (221 MB written in 8 s before I stopped it) | 7 requests, 16.4 MiB |

This matches `docs/remote-data.md` ("other formats are downloaded first"), but `ROADMAP.md` lists "Read cloud data in place: range requests, lazy tiles and chunks, no full download" as a principle, so I wondered whether the CLI is expected to follow.

## A related note

When the CLI is interrupted during such a download (for example by `timeout`), the temporary file stays: `/tmp/terrio-XXXXXX/JPN.parquet` (221 MB after 8 seconds). Maybe the temporary directory could be removed on SIGTERM, or the location made configurable (I could not find a setting in the docs).

Thank you for considering this.
