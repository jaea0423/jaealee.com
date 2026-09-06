"""헤드리스 크롬으로 화면 4개 × 폭 4개 스크린샷을 찍고, 통합 전후를 픽셀 단위로 비교합니다.

  python work/shots.py shoot <라벨> <앱 URL 경로>      예: python work/shots.py shoot before /v2/work/before.html
  python work/shots.py diff  <라벨A> <라벨B>            예: python work/shots.py diff before zone2
  python work/shots.py combos <이름> <앱 URL 경로>      → work/snaps/<이름>.json (요소 클래스 조합)

서버(python work/serve.py 8766)가 떠 있어야 합니다. 결과: work/shots/<라벨>/<상태>_<폭>.png, diff 는 work/shots/diff_A_B/
"""
import os, sys, subprocess, time
from PIL import Image, ImageChops

WORK = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "http://localhost:8766"
PROFILE = os.path.join(WORK, ".chrome-profile")   # 사용자 크롬 프로필과 섞이지 않게 별도 프로필
WIDTHS = [(430, 932), (820, 1180), (1280, 800), (1920, 1080)]
STATES = ["dash", "wizard", "settings", "detail", "select", "lock", "display"]   # display: 손님용 TV 화면 (좁은 폭에서는 '화면이 작습니다' 안내, 세로 820 은 축소 미리보기)

def norm(src):
    # Git Bash 가 "/v2/..." 인자를 "C:/Program Files/Git/v2/..." 로 바꿔 버리므로 앞의 / 없이 받아서 여기서 붙입니다
    src = src.replace("\\", "/")
    if "Git/" in src: src = src[src.index("Git/") + 3:]
    return "/" + src.lstrip("/")

def shoot(label, src):
    src = norm(src)
    out = os.path.join(WORK, "shots", label); os.makedirs(out, exist_ok=True)
    # 실제 기기 높이 한 벌 + 대시보드·설정은 긴 화면(높이 2600)으로 한 벌 더 — 아래쪽 카드까지 보려고
    states = os.environ.get("SHOT_STATES", "").split(",") if os.environ.get("SHOT_STATES") else STATES   # 일부 화면만 찍을 때
    jobs = [(w, h, st) for w, h in WIDTHS for st in states] + \
           ([(w, 2600, st + "-tall") for w, _ in WIDTHS for st in ("dash", "settings")] if states is STATES else [])
    if os.environ.get("ONE"): jobs = jobs[2:3]
    for w, h, st in jobs:
        if True:
            png = os.path.join(out, f"{st}_{w}.png")
            # 헤드리스 크롬은 창 폭 최소 500px — 그보다 좁은 폭은 iframe 크기로 만들고 스크린샷을 잘라 냅니다
            ww = max(w, 500)
            url = f"{BASE}/v2/work/shot.html?src={src}&state={st.replace('-tall', '')}&w={w}&h={h}"
            r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                            f"--user-data-dir={PROFILE}", f"--window-size={ww},{h}", "--timeout=8000", "--virtual-time-budget=8000",
                            f"--screenshot={png}", url], capture_output=True, timeout=120, text=True)
            if ww != w and os.path.exists(png):
                im = Image.open(png); im.crop((0, 0, w, h)).save(png)
            size = os.path.getsize(png) if os.path.exists(png) else 0
            if os.environ.get("ONE"): print(r.args, r.returncode, repr(r.stderr[-300:]))
            print("shot", os.path.basename(png), size, "" if size > 12000 else "!! 빈 화면? " + r.stderr.strip().splitlines()[-1:][0] if r.stderr.strip() else "")

def diff(a, b):
    da, db = os.path.join(WORK, "shots", a), os.path.join(WORK, "shots", b)
    out = os.path.join(WORK, "shots", f"diff_{a}_{b}"); os.makedirs(out, exist_ok=True)
    for old in os.listdir(out): os.remove(os.path.join(out, old))   # 지난 비교 결과가 남아 헷갈리지 않게
    worst = []
    for name in sorted(os.listdir(da)):
        if not name.endswith(".png"): continue
        pa, pb = os.path.join(da, name), os.path.join(db, name)
        if not os.path.exists(pb): print(name, "B 없음"); continue
        ia, ib = Image.open(pa).convert("RGB"), Image.open(pb).convert("RGB")
        if ia.size != ib.size: print(name, "크기 다름", ia.size, ib.size); worst.append((name, -1)); continue
        d = ImageChops.difference(ia, ib)
        bbox = d.getbbox()
        n = sum(1 for px in d.getdata() if px != (0, 0, 0)) if bbox else 0
        print(f"{name:22s} 다른 픽셀 {n:8d}  {'' if not bbox else str(bbox)}")
        if n:
            # 다른 곳을 빨갛게 표시한 그림
            mask = d.convert("L").point(lambda v: 255 if v else 0)
            red = Image.new("RGB", ia.size, (255, 0, 0))
            vis = Image.composite(red, ia, mask)
            vis.save(os.path.join(out, name))
        worst.append((name, n))
    tot = sum(n for _, n in worst)
    print("합계 다른 픽셀:", tot, "(0 이면 통과)")
    return tot

def combos(name, src):
    src = norm(src)
    url = f"{BASE}/v2/work/shot.html?src={src}&mode=combos&name={name}"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--window-size=1280,800",
                    "--timeout=25000", "--virtual-time-budget=25000", "--screenshot=" + os.path.join(WORK, "shots", "_combos.png"), url],
                   capture_output=True, timeout=180)
    p = os.path.join(WORK, "snaps", name + ".json")
    print("combos:", p, os.path.getsize(p) if os.path.exists(p) else "FAIL")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "shoot": shoot(sys.argv[2], sys.argv[3])
    elif cmd == "diff": sys.exit(1 if diff(sys.argv[2], sys.argv[3]) else 0)
    elif cmd == "combos": combos(sys.argv[2], sys.argv[3])
