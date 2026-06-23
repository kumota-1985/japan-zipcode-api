#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Japan Postal Code & Address API のロゴ(500x500 PNG)を生成。
コンセプト: 日本の郵便記号〒(誰でも郵便番号だと分かる)を白抜きで。"""
import os
from PIL import Image, ImageDraw

W = 500
ORANGE = (234, 88, 12, 255)     # #EA580C 背景
WHITE = (255, 255, 255, 255)

img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# 角丸オレンジ背景
d.rounded_rectangle([0, 0, W - 1, W - 1], radius=112, fill=ORANGE)

# 〒 マーク(白): 上の横棒 / 下の横棒 / 中央から下の縦棒
d.rounded_rectangle([150, 150, 350, 178], radius=14, fill=WHITE)     # 上の横棒
d.rounded_rectangle([166, 224, 334, 252], radius=14, fill=WHITE)     # 下の横棒
d.rounded_rectangle([236, 238, 264, 372], radius=14, fill=WHITE)     # 中央の縦棒

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zipcode_logo.png")
img.save(out)
print("saved:", out, img.size)
