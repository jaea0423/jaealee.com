# -*- coding: utf-8 -*-
"""v4 스크린샷 도구 — 헤드리스 크롬 (Playwright 가 이 파이썬에 없어서 v3 의 shots.py 방식을 가볍게 다시 만든 것)

  from shot import run
  run("6a", [("dash_today", 1280, 800, "view.date=todayStr(); render();"), ...])
  → work/shots/6a/<이름>_<폭>.png

정적 서버(hanok/ 루트, 포트 8767)를 스스로 띄우고 끝나면 내립니다.
각 작업의 js 는 shot.html 이 앱 창 스코프에서 실행합니다. 공통 앞부분(PRELUDE)이 잠금·인트로를 건너뜁니다."""
import os, sys, subprocess, time, urllib.parse
from PIL import Image

WORK = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(WORK))            # hanok/ (사이트 루트. system/ 은 그 아래)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 8767
BASE = "http://127.0.0.1:%d" % PORT
PROFILE = os.path.join(WORK, ".chrome-profile")
SRC = "/system/dist/hanok-admin.html"

PRELUDE = "view.storeKey='hanok'; AUTHED=true; INTRO=null; try{clearIntro(true);}catch(e){} view.date=todayStr(); "

def run(label, jobs, src=SRC):
    out = os.path.join(WORK, "shots", label); os.makedirs(out, exist_ok=True)
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1", "--directory", PROJ],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)
    paths = []
    try:
        for job in jobs:
            name, w, h, js = job[:4]
            budget = job[4] if len(job) > 4 else 9000   # 가상 시간(ms). 인트로처럼 '몇 ms 시점' 을 찍을 때 작게 줍니다
            png = os.path.join(out, "%s_%d.png" % (name, w))
            ww = max(w, 500)
            url = "%s/system/work/shot.html?src=%s&w=%d&h=%d&js=%s" % (BASE, src, w, h, urllib.parse.quote(PRELUDE + js, safe=""))
            r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                                "--user-data-dir=" + PROFILE, "--window-size=%d,%d" % (ww, h),
                                "--timeout=%d" % max(budget, 3000), "--virtual-time-budget=%d" % budget, "--screenshot=" + png, url],
                               capture_output=True, timeout=120, text=True)
            if ww != w and os.path.exists(png):
                im = Image.open(png); im.crop((0, 0, w, h)).save(png)
            size = os.path.getsize(png) if os.path.exists(png) else 0
            print("shot", os.path.relpath(png, PROJ), size, "" if size > 8000 else "!! 빈 화면?")
            paths.append(png)
    finally:
        srv.terminate()
    return paths

if __name__ == "__main__":
    run("test", [("dash", 1280, 800, "render();")])
