# Japan Postal Code & Address API

郵便番号 ⇄ 住所 を1コールで返す小さなREST API。
データ = 日本郵便 郵便番号データ(utf_ken_all・無料・再配布自由)。120,000件超。

## エンドポイント
- `GET /v1/zip?code=1000001` — 郵便番号 → 住所(都道府県/市区町村/町域 + カナ)
- `GET /v1/search?q=梅田&prefecture=大阪府` — 住所テキスト → 郵便番号候補
- `GET /v1/prefectures` — 都道府県一覧(47)

## ローカル実行
```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8004   # http://127.0.0.1:8004/docs
```

## データ更新
```bash
python refresh_data.py   # 日本郵便 utf_ken_all を再取得し data/zipcodes.json を更新
```
`.github/workflows/refresh.yml` が毎月自動で再取得→commit。

## デプロイ / 出品
- `render.yaml`(Render)。バンドルデータ~23MBをメモリ保持(~150MB)→無料枠で動くが、OOM時は starter に。
- `openapi_rapidapi.json` を RapidAPI にインポート / `DOCS_TAB.md` を Docs に / `zipcode_logo.png`(〒) をロゴに。
