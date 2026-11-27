# Draft issue for opengeos/terrio (not posted; hfu will review and post)

**Title:** terrio-js 0.9.0: `openUrl` of a large raster PMTiles panics (`capacity overflow`); 0.7.0 and 0.8.0 open it at once

Hello, and thank you for terrio. While re-running my small browser test page with terrio-js 0.9.0, one of my six examples stopped working. It worked in 0.7.0 and 0.8.0, so I write what I saw in case it is a regression.

## Versions

terrio-js 0.7.0, 0.8.0 and 0.9.0 from npm (installed one by one with `npm install terrio-js@X`), Node.js 22 on Linux x86_64. The same panic appears in Chromium 1194 with terrio-js 0.9.0 loaded from jsDelivr. The terrio 0.9.0 CLI (PyPI wheel) is not affected.

## Reproduction

`t.mjs` (Node 22; I use `NODE_USE_ENV_PROXY=1` only because my network needs a proxy):

```js
import fs from 'node:fs';
const T = await import('./node_modules/terrio-js/terrio.js');
await T.default({ module_or_path: fs.readFileSync('./node_modules/terrio-js/terrio_bg.wasm') });
console.log(T.version());
const d = await T.openUrl('https://r2-public.protomaps.com/protomaps-sample-datasets/terrarium_z9.pmtiles', {});
console.log(JSON.stringify(d.info()).slice(0, 200));
```

| terrio-js | result |
|---|---|
| 0.7.0, 0.8.0 | opens at once; `info()` gives `{"type":"raster","driver":"PMTiles","size":[131072,130644],"band_count":3,...}` |
| 0.9.0 | no result for about 88 s, then `capacity overflow` (a Rust panic from `alloc/raw_vec`); in the browser the panic is followed by `unreachable` |

The file is a 30.5 GB raster PMTiles (Terrarium z9). A small vector PMTiles (`https://depot.optgeo.org/ksj_n03_hkd.pmtiles`) still opens in 0.9.0. The CLI, `terrio info <same url>`, takes 3.5 s and 12 requests with 0.9.0.

**Rechecked 2026-11-27 (0.10.0):** terrio-js 0.10.0 still panics with `capacity overflow` on the same URL. The `core` and `threads` builds in the npm package behave the same. In Node the panic ends the process (the error cannot be caught with `try/catch`), so run each URL in its own process. 0.8.0 still opens it in 4.1 s.

## What I do not know

I did not look for the cause. It may be related to the size of the archive or its directories in 32-bit WebAssembly, but this is only a guess. I also did not try the `memory64` build (it does not load in my Node 22).

Thank you for your work. I hope this is useful.
