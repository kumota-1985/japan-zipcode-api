#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Japan Postal Code & Address API  --  flip_zipcodeapi/app.py
================================================================================
郵便番号 ⇄ 住所 を1コールで。データ = 日本郵便の郵便番号データ(無料・再配布自由)。
フォーム自動入力・EC・配送系の定番ニーズ。

  - GET /v1/zip?code=1000001       郵便番号 → 住所(都道府県/市区町村/町域 + カナ)
  - GET /v1/search?q=梅田          住所テキスト → 候補(郵便番号つき)
  - GET /v1/prefectures            都道府県一覧

  pip install -r requirements.txt
  uvicorn app:app --reload --port 8004   → http://127.0.0.1:8004/docs
"""
import json
import os
import re
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.responses import HTMLResponse, PlainTextResponse

_HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_HERE, "data", "zipcodes.json"), encoding="utf-8") as _f:
    ZIPS = json.load(_f)                              # "1000001" -> [ {address}, ... ]
_FLAT = [(z, e) for z, lst in ZIPS.items() for e in lst]   # 逆引き用フラットリスト
PREFECTURES = sorted({e["prefecture"] for _z, e in _FLAT})

RAPIDAPI_SECRET = os.environ.get("RAPIDAPI_PROXY_SECRET")
PRO_KEYS = set(k.strip() for k in os.environ.get("ZIPCODE_KEYS", "").split(",") if k.strip())
ATTRIBUTION = "出典: 日本郵便 郵便番号データを加工。Source: Japan Post postal code data, processed."

app = FastAPI(
    title="Japan Postal Code & Address API",
    version="1.0.0",
    description="Look up a Japanese address from a 7-digit postal code, or search postal codes by "
                "address text. Prefecture / city / town with katakana readings. Japan Post data.",
)


def auth(x_api_key: Optional[str], rapid_secret: Optional[str]) -> None:
    if RAPIDAPI_SECRET:
        if rapid_secret == RAPIDAPI_SECRET:
            return
        if x_api_key and x_api_key in PRO_KEYS:
            return
        raise HTTPException(status_code=403, detail="Requests must go through the RapidAPI marketplace.")


def _norm_zip(code: str) -> str:
    z = re.sub(r"\D", "", code or "")
    if len(z) != 7:
        raise HTTPException(status_code=422, detail="code must be a 7-digit postal code (e.g. 1000001 or 100-0001)")
    return z


# --------------------------------------------------------------------------- #
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    return ('<h2>Japan Postal Code &amp; Address API</h2>'
            '<p>Japanese postal code &harr; address lookup.</p>'
            '<p>→ <a href="/docs">/docs</a>. <code>/v1/zip?code=1000001</code> '
            '<code>/v1/search?q=梅田</code></p>')


@app.get("/ping", include_in_schema=False)
def ping():
    return {"status": "ok"}


@app.get("/llms.txt", response_class=PlainTextResponse, include_in_schema=False)
def llms_txt():
    return """# Japan Postal Code & Address API
> Japanese postal code <-> address lookup (Japan Post data). 120k+ postal codes.

Base URL: https://japan-zipcode-api.onrender.com
Docs: https://japan-zipcode-api.onrender.com/docs
OpenAPI: https://japan-zipcode-api.onrender.com/openapi.json

## Endpoints
- GET /v1/zip?code=1000001 - postal code -> address (prefecture/city/town + katakana)
- GET /v1/search?q=梅田&prefecture=大阪府 - address text -> matching postal codes
- GET /v1/prefectures - list of the 47 prefectures
- Access: via the RapidAPI marketplace (subscribe for a key)
"""


@app.get("/v1/zip")
def zip_lookup(code: str = Query(..., description="7桁の郵便番号(ハイフン可)。例: 1000001 / 100-0001"),
              x_api_key: Optional[str] = Header(None),
              x_rapidapi_proxy_secret: Optional[str] = Header(None)):
    """郵便番号 → 住所。1つの郵便番号に複数住所が紐づく場合は全件返す。"""
    auth(x_api_key, x_rapidapi_proxy_secret)
    z = _norm_zip(code)
    found = ZIPS.get(z)
    if not found:
        raise HTTPException(status_code=404, detail=f"postal code not found: {z}")
    return {"zipcode": z, "count": len(found), "data": found, "attribution": ATTRIBUTION}


@app.get("/v1/search")
def search(q: Optional[str] = Query(None, description="住所テキスト(部分一致)。例: 梅田"),
           prefecture: Optional[str] = None, city: Optional[str] = None, town: Optional[str] = None,
           limit: int = Query(20, ge=1, le=100),
           x_api_key: Optional[str] = Header(None),
           x_rapidapi_proxy_secret: Optional[str] = Header(None)):
    """住所テキスト → 郵便番号。q(部分一致) と prefecture/city/town(部分一致)で絞り込む。"""
    auth(x_api_key, x_rapidapi_proxy_secret)
    if not any([q, prefecture, city, town]):
        raise HTTPException(status_code=422, detail="provide at least one of: q, prefecture, city, town")
    out = []
    for z, e in _FLAT:
        if prefecture and prefecture not in e["prefecture"]:
            continue
        if city and city not in e["city"]:
            continue
        if town and town not in e["town"]:
            continue
        if q and q not in (e["prefecture"] + e["city"] + e["town"]):
            continue
        out.append({"zipcode": z, **e})
        if len(out) >= limit:
            break
    return {"count": len(out), "limit": limit, "data": out, "attribution": ATTRIBUTION}


@app.get("/v1/prefectures")
def prefectures(x_api_key: Optional[str] = Header(None),
                x_rapidapi_proxy_secret: Optional[str] = Header(None)):
    """都道府県一覧(47)。"""
    auth(x_api_key, x_rapidapi_proxy_secret)
    return {"count": len(PREFECTURES), "data": PREFECTURES}
