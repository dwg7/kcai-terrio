# 2026-10-21 公式ノートブック（quickstart / xarray）を手元で動かす

- 日付: 2026-10-21（夜）
- terrio: 配布版 0.3.2（PyPI の wheel、Linux x86_64、Python 3.13）
- 環境: クラウドセッション。新しい仮想環境に `terrio[xarray]`、`matplotlib`、`dask`。matplotlib は Agg（描画は画面に出さない）
- 方法: リポジトリ `docs/notebooks/quickstart.ipynb`（28 セル）と `xarray.ipynb`（27 セル）のコードセルを、順に実行する小さな実行器で動かした（Colab ではない）。`%pip` のセルは飛ばした。`TERRIO_HTTP_LOG=YES` で通信を記録
- 入力は公開データ（USGS 3DEP の 1 度 DEM、opengeos/data の Landsat 7 と国界）

## 結果

| ノートブック | コードセル | 結果 |
|---|---|---|
| quickstart | 15 | **すべて成功**（版 0.3.2、遠隔 COG の窓・概観、hillshade / slope、warp、NDVI、国界の読み、GPKG への変換、FlatGeobuf / GeoParquet / Shapefile / KML の書き出しと再読込、rasterize、点の変換） |
| xarray | 13 | **12 成功、1 失敗**。失敗は `to_zarr`（`zarr` パッケージが無い）。`zarr` を入れると成功（`EPSG:32613 True`） |

- ノートブックの冒頭は `pip install "terrio[xarray]"` だけ。`terrio[xarray]` の依存は `xarray` と `dask[array]` で、**`zarr` を含まない**（`importlib.metadata.requires` で確認）。公式の Colab で `xr.open_zarr` / `to_zarr` のセルを動かすには、`zarr` を足す必要がありそう（Colab に標準で入っているかは未確認）。
- 遠隔 DEM（約 26 MB の COG ではなく、3612×3612 の Float32）の読みは、範囲読み込み（HTTP 206）。quickstart 全体で DEM から受け取ったのは約 8 MB（先頭 64 KiB + 640 KiB、窓切り出しの 3 本の約 2.4 MB）。一方 **Landsat 7 の GeoTIFF（4.9 MB）と国界の GeoJSON は全量取得**（形式が範囲読みに向かない小さなファイル）。
- 国界の GeoJSON は **179 地物**（Natural Earth の 177 とは別のデータ）。`layer.fields` は `{'id': 'Text', 'name': 'Text'}`。
- xarray の `merge_arrays`、`clip`、`reproject`、`estimate_utm_crs`、`rio` アクセサ互換（`register_rio_accessor`）が、公式の手順どおりに動いた。

## 発見

1. xarray ノートブックの `to_zarr` のセルは、`terrio[xarray]` だけでは `ImportError`（`zarr` が無い）。上流への報告の候補だが、Colab の環境で実際に起きるかは**未確認**なので、下書きにしていない。
2. 公式のノートブックは、そのまま動く（失敗は上の 1 件のみ）。ドキュメントの例が実際に動く、という確かめになった。

## 後始末

- 作業ディレクトリは `/tmp/work/nb`（仮想環境と出力）。終わりに消す。
