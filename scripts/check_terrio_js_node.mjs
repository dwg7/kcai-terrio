// terrio-js を Node で動かし、遠隔の形式を openUrl で開けるかを確かめる（kcai-terrio の確認用）。
// 使い方: (cd 作業ディレクトリ && npm install terrio-js@<版>) && node scripts/check_terrio_js_node.mjs <作業ディレクトリ> [URL...]
// 通信にプロキシが要る環境では NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=<CA バンドル> を付ける。
import fs from 'node:fs';
import path from 'node:path';
const dir = path.resolve(process.argv[2] || '.');
const T = await import(path.join(dir, 'node_modules/terrio-js/terrio.js'));
await T.default({ module_or_path: fs.readFileSync(path.join(dir, 'node_modules/terrio-js/terrio_bg.wasm')) });
console.log('terrio-js', T.version());
const urls = process.argv.length > 3 ? process.argv.slice(3) : [
  'https://r2-public.protomaps.com/protomaps-sample-datasets/terrarium_z9.pmtiles', // 30.5 GB のラスタ PMTiles（0.9.0 で panic）
  'https://depot.optgeo.org/ksj_n03_hkd.pmtiles',                                     // 小さなベクタ PMTiles
  'https://flatgeobuf.org/test/data/UScounties.fgb',
];
for (const u of urls) {
  const t0 = Date.now();
  try {
    const d = await Promise.race([T.openUrl(u, {}), new Promise((_, r) => setTimeout(() => r(new Error('timeout 60 s')), 60000))]);
    let info = '';
    try { info = JSON.stringify(d.info()).slice(0, 90); } catch (e) { info = '(info なし)'; }
    console.log('OK  ', ((Date.now() - t0) / 1000).toFixed(1) + 's', u.split('/').pop(), info);
  } catch (e) {
    console.log('ERR ', ((Date.now() - t0) / 1000).toFixed(1) + 's', u.split('/').pop(), String(e).slice(0, 120));
  }
}
process.exit(0);
