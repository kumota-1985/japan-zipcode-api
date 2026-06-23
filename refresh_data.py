#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日本郵便の郵便番号データ(utf_ken_all)を取得・正規化し、data/zipcodes.json(UTF-8) に保存。
出典: 日本郵便 郵便番号データ(無料・再配布自由)。
UTF版(2023年6月〜)は「1レコード1行・UTF-8・全角カナ」なので素直にパースできる。"""
import csv
import io
import json
import os
import re
import urllib.request
import zipfile

URL = "https://www.post.japanpost.jp/service/search/zipcode/download/utf/zip/utf_ken_all.zip"
HERE = os.path.dirname(os.path.abspath(__file__))
_PAREN = re.compile(r"[（(].*$")     # 町域の補足括弧(以降)を除去


def _clean(s):
    return _PAREN.sub("", s).strip()


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=120).read()
    zf = zipfile.ZipFile(io.BytesIO(raw))
    name = [n for n in zf.namelist() if n.upper().endswith(".CSV")][0]
    rows = list(csv.reader(io.StringIO(zf.read(name).decode("utf-8"))))

    data = {}
    for r in rows:
        if len(r) < 9 or len(r[2].strip()) != 7:
            continue
        town, town_kana = r[8].strip(), r[5]
        if town == "以下に掲載がない場合":
            town, town_kana = "", ""
        entry = {
            "prefecture": r[6].strip(), "city": r[7].strip(), "town": _clean(town),
            "prefecture_kana": r[3].strip(), "city_kana": r[4].strip(), "town_kana": _clean(town_kana),
        }
        bucket = data.setdefault(r[2].strip(), [])
        if entry not in bucket:
            bucket.append(entry)

    os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
    path = os.path.join(HERE, "data", "zipcodes.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"wrote {len(data)} zip codes -> {path}  ({os.path.getsize(path)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
