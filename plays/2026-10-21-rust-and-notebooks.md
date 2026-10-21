# 2026-10-21 Rust のコードを書いて動かす

- terrio: crates.io 0.3.2、および main のソース（パス依存、0.3.2 と同じ版番号）。Rust 1.97、Linux x86_64
- 作ったもの: 座標変換（6668→6677、4326→3857 の (180,−90)）、遠隔 COG の遅延読み（概観 2 の 256×256）、COG の書き出しと読み戻しをする 30 行ほどのプログラム
- 結果と発見は `knowledge/terrio-rust-library-and-features.md` の「書いて動かした」。要点: API は書いたとおりに動いた／ドキュメントの `features = ["geotiff"]` は 0.3.2 では通らず main では通る／main で `geotiff` + `remote` に絞ると 24 MB・188 クレート（0.3.2 の既定は 46 MB・302 クレート）
- 公式ノートブックの実行は `plays/2026-10-21-notebooks.md`
- 新しい版の確認: PyPI・crates.io・npm とも 0.3.2 が最新。`stale` にする塊は無い
