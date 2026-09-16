# -*- coding: utf-8 -*-
"""사이트 전체 페이지 스크린샷 — 헤드리스 크롬. 8767 서버가 떠 있어야 합니다(hanok/ 루트).
   python site/work/shot.py [폭] [높이]  → site/work/shots/<장>_<폭>.png"""
import os, sys, subprocess, time
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "shots"); os.makedirs(OUT, exist_ok=True)
w = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
h = int(sys.argv[2]) if len(sys.argv) > 2 else 5200
pages = sys.argv[3].split(",") if len(sys.argv) > 3 else ["index", "about", "space", "menu", "visit", "reserve"]
for p in pages:
    q = "?shot=notice&notice=1" if p == "notice" else "?shot=1"
    url = "http://127.0.0.1:8767/site/%s.html%s&v=%d" % ("index" if p == "notice" else p, q, time.time())
    png = os.path.join(OUT, "%s_%d.png" % (p, w))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    "--user-data-dir=" + os.path.join(HERE, ".chrome-profile"), "--window-size=%d,%d" % (w, h),
                    "--virtual-time-budget=6000", "--screenshot=" + png, url], capture_output=True, timeout=120)
    print(png)
# 예약 창 단계별 (?rv=N)
if "rv" in (sys.argv[4] if len(sys.argv) > 4 else ""):
    for n in (1,2,3,4,5,6,7):
        png = os.path.join(OUT, "rv%d_%d.png" % (n, w))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                        "--user-data-dir=" + os.path.join(HERE, ".chrome-profile"), "--window-size=%d,%d" % (w, 900),
                        "--virtual-time-budget=4000", "--screenshot=" + png, "http://127.0.0.1:8767/site/reserve.html?shot=1&rv=%d&v=%d" % (n, time.time())], capture_output=True, timeout=120)
        print(png)
