# Docs タブに貼る内容(英語・Markdown)— Japan Postal Code & Address API

RapidAPIの **Docs**(About)タブに、下の `---` 内の英語Markdownをそのまま貼ってください。
ロゴは `zipcode_logo.png`(500x500)を General の Upload Logo に。

---

# Japan Postal Code & Address — Documentation

Look up a Japanese **address from a postal code**, or **search postal codes by address text**, in one call. Each result has prefecture / city / town plus **katakana readings** — perfect for checkout/address auto-fill, shipping and data cleaning. 120,000+ postal codes from **Japan Post**.

## Authentication
You don't manage any keys yourself. **Subscribe to a plan** (BASIC is free) and use the auto-generated snippets on the **Endpoints** tab — RapidAPI injects your `X-RapidAPI-Key` / `X-RapidAPI-Host` headers automatically.

---

## GET /v1/zip
Postal code → address. Accepts a 7-digit code with or without a hyphen.

| Param | Required | Example |
|---|---|---|
| `code` | **yes** | `1000001` or `100-0001` |

**Example:** `GET /v1/zip?code=1000001`
```json
{
  "zipcode": "1000001",
  "count": 1,
  "data": [
    { "prefecture": "東京都", "city": "千代田区", "town": "千代田",
      "prefecture_kana": "トウキョウト", "city_kana": "チヨダク", "town_kana": "チヨダ" }
  ]
}
```
A single postal code can map to multiple towns — all are returned in `data`.

## GET /v1/search
Address text → postal codes. Combine free-text `q` with `prefecture` / `city` / `town` filters (all partial-match).

| Param | Required | Example |
|---|---|---|
| `q` | one of these | `梅田` |
| `prefecture` / `city` / `town` | one of these | `大阪府` |
| `limit` | no | `20` (max 100) |

**Example:** `GET /v1/search?q=梅田&prefecture=大阪府`
```json
{ "count": 1, "limit": 20,
  "data": [ { "zipcode": "5300001", "prefecture": "大阪府", "city": "大阪市北区", "town": "梅田", "town_kana": "ウメダ" } ] }
```

## GET /v1/prefectures
List the 47 prefecture names. No parameters.

---

## Notes
- "以下に掲載がない場合" (no specific town) returns an empty `town`.
- Data covers **120,000+ postal codes** and is refreshed monthly from Japan Post.

## Data source & attribution
Postal code data is from **Japan Post** (日本郵便 郵便番号データ), provided free for use and redistribution. This is an independent service, not affiliated with Japan Post. Each response includes an `attribution` field — please display it.
