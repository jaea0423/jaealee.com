"""Phase 2 — 팔레트 안을 실제 화면에 입혀 스크린샷으로 비교합니다.

  python work/palette.py build          work/palettes/*.css 를 지금 빌드(dist)에 덧붙인 work/pal_<안>.html 생성
  python work/palette.py shoot          안마다 스크린샷 (대시보드·마법사·설정·예약상세 4폭) → work/shots/pal_<안>/
  python work/palette.py compose        같은 화면을 [현재 | A | B | C] 로 나란히 → work/shots/palette_<화면>.png

서버(python work/serve.py 8766)가 떠 있어야 합니다. 팔레트 CSS 는 <style> 맨 끝에 붙으므로 모든 규칙을 덮습니다.
"""
import os, sys, subprocess, glob
from PIL import Image, ImageDraw

WORK = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(WORK)
DIST = os.path.join(V2, "dist", "hanok-admin.html")
NAMES = ["A", "B", "C"]
SCREENS = ["dash_1280", "dash_430", "wizard_820", "settings_1280", "detail_430"]

def build():
    html = open(DIST, encoding="utf-8").read()
    for n in NAMES:
        css = open(os.path.join(WORK, "palettes", n + ".css"), encoding="utf-8").read()
        out = html.replace("</style>", "\n" + css + "\n</style>", 1)
        p = os.path.join(WORK, f"pal_{n}.html")
        open(p, "w", encoding="utf-8").write(out); print("built", p)

def shoot():
    env = dict(os.environ, SHOT_STATES="dash,wizard,settings,detail")
    for n in NAMES:
        subprocess.run([sys.executable, os.path.join(WORK, "shots.py"), "shoot", f"pal_{n}", f"v2/work/pal_{n}.html"], env=env, check=True)

def compose():
    for scr in SCREENS:
        imgs = [Image.open(os.path.join(WORK, "shots", "p1b", scr + ".png")).convert("RGB")]
        labels = ["현재"]
        for n in NAMES:
            imgs.append(Image.open(os.path.join(WORK, "shots", f"pal_{n}", scr + ".png")).convert("RGB")); labels.append(n)
        gap = 20; top = 44
        cols = 2 if imgs[0].width >= 800 else 4          # 넓은 화면은 2×2, 폰 화면은 한 줄에 4개
        cw, ch = imgs[0].width, imgs[0].height + top
        rows = (len(imgs) + cols - 1) // cols
        w = cw * cols + gap * (cols - 1); h = ch * rows + gap * (rows - 1)
        out = Image.new("RGB", (w, h), (235, 235, 235)); d = ImageDraw.Draw(out)
        for k, (i, lab) in enumerate(zip(imgs, labels)):
            x = (k % cols) * (cw + gap); y = (k // cols) * (ch + gap)
            d.rectangle([x, y, x + i.width, y + top - 6], fill=(40, 40, 40))
            d.text((x + 12, y + 12), lab, fill=(255, 255, 255))
            out.paste(i, (x, y + top))
        maxw = 2400
        if w > maxw: out = out.resize((maxw, int(h * maxw / w)), Image.LANCZOS)
        p = os.path.join(WORK, "shots", f"palette_{scr}.png"); out.save(p); print(p, out.size)

if __name__ == "__main__":
    {"build": build, "shoot": shoot, "compose": compose}[sys.argv[1]]()
