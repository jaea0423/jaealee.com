# -*- coding: utf-8 -*-
"""work/review/*.png 를 두 장씩 옆으로 붙여 work/review/sheets/NN_제목.png 로 — Claude 가 한 번에 보기 좋게.
   python work/review_sheets.py           (820 + 390 전부)
   python work/review_sheets.py 390       (그 폭만)
폰 캡처는 세로가 길어 4장씩, 태블릿은 2장씩."""
import os, re, sys, glob
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "review")
OUT = os.path.join(SRC, "sheets")
want = sys.argv[1] if len(sys.argv) > 1 else None

def key(p):
    m = re.match(r"(\d+|S\d+)", os.path.basename(p)); k = m.group(1) if m else "999"
    return (0 if k[0] != "S" else 1, int(k.lstrip("S")), p)

os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, "*.png")): os.remove(f)
files = sorted(glob.glob(os.path.join(SRC, "*.png")), key=key)
if want: files = [f for f in files if f.endswith("_%s.png" % want)]
groups = {}
for f in files:
    w = int(re.search(r"_(\d+)\.png$", f).group(1)); groups.setdefault(w, []).append(f)
n = 0
for w, fs in sorted(groups.items()):
    per = 4 if w <= 430 else 2
    for i in range(0, len(fs), per):
        chunk = fs[i:i+per]; ims = [Image.open(f) for f in chunk]
        H = min(max(im.height for im in ims), 1400 if w > 430 else 1800)   # 너무 긴 건 위만
        W = sum(im.width for im in ims) + 12 * (len(ims) - 1)
        sheet = Image.new("RGB", (W, H), (200, 200, 200)); x = 0
        for im in ims:
            sheet.paste(im.crop((0, 0, im.width, min(im.height, H))), (x, 0)); x += im.width + 12
        title = "+".join(re.sub(r"_\d+\.png$", "", os.path.basename(f))[:18] for f in chunk)
        name = "%02d_%d_%s.png" % (n, w, title); n += 1
        sheet.save(os.path.join(OUT, name)); print(name, sheet.size)
print("장수:", n, "→", OUT)
