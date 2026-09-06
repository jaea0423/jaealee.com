"""한 화면의 4폭(430/820/1280/1920) 스크린샷을 한 장에 — 반응형 점검용.
  python work/sheet.py <라벨> <상태>   → work/shots/_sheet_<상태>.png"""
import os, sys
from PIL import Image, ImageDraw
WORK = os.path.dirname(os.path.abspath(__file__))
label, state = sys.argv[1:3]
H = 900
imgs = []
for w in (430, 820, 1280, 1920):
    p = os.path.join(WORK, "shots", label, f"{state}_{w}.png")
    im = Image.open(p).convert("RGB")
    im = im.crop((0, 0, im.width, min(im.height, int(H * im.width / 1280) if w >= 1280 else im.height)))
    scale = H / im.height
    imgs.append((w, im.resize((int(im.width * scale), H), Image.LANCZOS)))
gap = 16; top = 28
W = sum(i.width for _, i in imgs) + gap * 3
out = Image.new("RGB", (W, H + top), (225, 225, 225)); d = ImageDraw.Draw(out)
x = 0
for w, i in imgs:
    d.text((x + 8, 6), f"{w}px", fill=(0, 0, 0)); out.paste(i, (x, top)); x += i.width + gap
if W > 2400: out = out.resize((2400, int((H + top) * 2400 / W)), Image.LANCZOS)
p = os.path.join(WORK, "shots", f"_sheet_{state}.png"); out.save(p); print(p, out.size)
