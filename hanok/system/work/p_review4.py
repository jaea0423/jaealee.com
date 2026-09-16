# -*- coding: utf-8 -*-
"""재아 요청(2026-09-16 밤): ① '지하' → '저층'(층 이름) ② 타임라인 좌우의 '자리 없음 N' 글자 제거(그래프 칸으로 충분) """
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ① 시스템 기본값·문서
s = load("js/01-data.js"); assert s.count('floor:"지하"') == 10; s = s.replace('floor:"지하"', 'floor:"저층"'); save("js/01-data.js", s)
s = load("js/03-util.js")
s = s.replace("그래서 예약은 '1층 테이블 / 지하 테이블' 까지만 받고", "그래서 예약은 '1층 테이블 / 저층 테이블' 까지만 받고")
s = s.replace("지하는 여포가 맨 앞이라", "저층은 여포가 맨 앞이라")
save("js/03-util.js", s)
s = load("js/08-changes.js"); s = s.replace("/* 지하 → 1층 처럼", "/* 저층 → 1층 처럼"); save("js/08-changes.js", s)
s = load("js/19-demo.js"); s = rep(s, 'const HALLS = ["1층 홀","지하 홀"];', 'const HALLS = ["1층 홀","저층 홀"];', 1); save("js/19-demo.js", s)
for f in ["매뉴얼.html", "비상예약지.html"]:
    p = os.path.join(BASE, f); t = io.open(p, encoding="utf-8").read(); n = t.count("지하")
    t = t.replace("지하 테이블", "저층 테이블").replace("지하 홀", "저층 홀").replace("지하:", "저층:").replace("지하)", "저층)").replace("지하 ", "저층 ")
    io.open(p, "w", encoding="utf-8").write(t); print(f, "지하", n, "→", t.count("지하"))
p = os.path.join(BASE, "work", "p_seed10.py"); t = io.open(p, encoding="utf-8").read(); io.open(p, "w", encoding="utf-8").write(t.replace('"floor": "지하"', '"floor": "저층"').replace("지하에", "저층에").replace("지하 여포", "저층 여포"))
p = os.path.join(BASE, "work", "seed_dev.py"); t = io.open(p, encoding="utf-8").read(); io.open(p, "w", encoding="utf-8").write(t.replace('"floor": "지하"', '"floor": "저층"').replace("지하에", "저층에").replace("지하 여포", "저층 여포"))

# ② 타임라인: 층 이름 칸·오른쪽 예약률 칸의 '자리 없음' 글자 제거 — 맨 위 빗금 칸 라벨만 남김
s = load("js/10-timeline.js")
s = rep(s, '''${over?`<span class="bk" title="같은 시간에 테이블 수보다 팀이 많습니다 — 맨 위 빗금 칸에 놓인 예약">자리 없음 ${over}팀</span>`:""}</div>''', '''</div>''', 1)
s = rep(s, '''${over?`<small class="over" title="같은 시간에 테이블 수보다 팀이 많습니다 — 자리 없는 팀(경고 예약)">자리 없음 ${over}</small>`:""}''', '', 1)
save("js/10-timeline.js", s)
print("ok")
