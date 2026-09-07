"""두 스크린샷 묶음을 나란히 붙여 한 장으로 — 눈으로 전후를 비교할 때.
  python work/compare.py <라벨A> <라벨B> <파일이름(확장자 없이)> [최대폭]
  → work/shots/_cmp_<파일이름>.png (왼쪽 A, 오른쪽 B)"""
import os, sys
from PIL import Image
WORK = os.path.dirname(os.path.abspath(__file__))
a, b, name = sys.argv[1:4]
maxw = int(sys.argv[4]) if len(sys.argv) > 4 else 1400
ia = Image.open(os.path.join(WORK, "shots", a, name + ".png")).convert("RGB")
ib = Image.open(os.path.join(WORK, "shots", b, name + ".png")).convert("RGB")
gap = 16
w = ia.width + ib.width + gap; h = max(ia.height, ib.height)
out = Image.new("RGB", (w, h), (200, 60, 60))
out.paste(ia, (0, 0)); out.paste(ib, (ia.width + gap, 0))
if w > maxw:
    out = out.resize((maxw, int(h * maxw / w)), Image.LANCZOS)
p = os.path.join(WORK, "shots", f"_cmp_{name}.png"); out.save(p); print(p, out.size)
