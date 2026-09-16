# -*- coding: utf-8 -*-
"""v7 정리 1 — 정적 검사(audit_js) 결과대로: 중복 minToHM, 안 부르는 함수 20개, 주석으로 막아 둔 직원·근태·매출 코드 삭제.
   되살릴 일이 생기면 v6(work/index.v6.html)에 그대로 있습니다."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L

# 1) minToHM 중복 — 앞 것(24시간 넘김 처리 없음) 삭제
s = L.load("js/03-util.js")
first = "function minToHM(m){ return pad(Math.floor(m/60))+\":\"+pad(m%60); }\n"
assert s.count(first) == 1
s = s.replace(first, "")
L.save("js/03-util.js", s)

# 2) 안 부르는 함수
dead = {
  "js/14-settings.js": ["addRole", "delRole", "moveRoom", "setRoomField", "setSettingNum"],
  "js/08-changes.js": ["changeLines"],
  "js/11-res.js": ["dayBadge", "renderRes", "setDate", "weekStart"],
  "js/03-util.js": ["floorLeft", "stayMin", "won"],
  "js/06-modal.js": ["goHome"],
  "js/15-sheets.js": ["openSetLog"],
  "js/07-dash.js": ["ratePreview"],
  "js/04-render.js": ["setTheme", "toggleTheme"],
  "js/09-sms.js": ["smsSeat", "toggleClosed"],
}
for name, fns in dead.items():
    s = L.load(name)
    for fn in fns:
        s = L.remove_fn(s, fn)
    L.save(name, s)

# 3) 주석 코드 덩어리
def cut_between(name, start_marker, end_marker, keep_end=False):
    s = L.load(name)
    a = s.index(start_marker); b = s.index(end_marker, a)
    if not keep_end: b += len(end_marker)
    L.save(name, s[:a] + s[b:])

# 09-sms: 매출 그래프 주석 (toggleClosed 는 위에서 지웠으니 그 다음 주석 블록부터 파일 끝의 다음 배너 전까지)
s = L.load("js/09-sms.js")
a = s.index("// ===== 매출 기능 비활성화 (그래프)")
b = s.index("\n// }\n", a) + len("\n// }\n")
L.save("js/09-sms.js", s[:a] + s[b:])

# 12·13: 통째 삭제 (배너만 남기지 않고 파일 삭제)
os.remove(L.path("js/12-staff-off.js"))
os.remove(L.path("js/13-sales-off.js"))

# 15-sheets: 직원·근태·매출 입력 시트 주석 + openStaff/openAtt/openSale 주석 줄
s = L.load("js/15-sheets.js")
a = s.index("/* ---------- 직원 ---------- */\n// ===== 직원 기능 비활성화")
b = s.index("// }\n", s.index("// function delSale(date){", a)) + len("// }\n")
s = s[:a] + s[b:]
for line in ['// function openStaff(id){ view.form={type:"staff", id}; render(); }\n',
             '// function openAtt(id){ view.form={type:"att", id}; render(); }\n',
             '// function openSale(date){ view.form={type:"sale", id:date}; render(); }\n']:
    assert s.count(line) == 1, line
    s = s.replace(line, "")
L.save("js/15-sheets.js", s)

L.js_check()
print("clean1 적용")
