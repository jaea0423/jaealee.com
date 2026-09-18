# -*- coding: utf-8 -*-
"""워크시프트 직원 기본 목록 넣기 (재아가 준 이름/별칭/역할, 2026-09-18). dev·prod 어디든 — 같은 별칭이 이미 있으면 건너뜁니다.
   python work/seed_staff.py            (HANOK_PIN 환경변수 필요, supabase.dev.json 기준 — prod 는 CFG 를 바꿔서)
급여·정규 근무는 넣지 않습니다(사장님이 화면에서). 시급 0 으로 들어가니 급여 화면에서 0원으로 보입니다."""
import io, json, os, sys, time, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(BASE, "supabase.dev.json")
cfg = json.load(io.open(CFG, encoding="utf-8"))
PIN = os.environ.get("HANOK_PIN")
if not PIN: raise SystemExit("HANOK_PIN 환경변수에 PIN 을 넣고 실행하세요")
def call(path, method="GET", body=None, token=None, prefer=None):
    h = {"apikey": cfg["anonKey"], "Authorization": "Bearer " + (token or cfg["anonKey"]), "Content-Type": "application/json"}
    if prefer: h["Prefer"] = prefer
    req = urllib.request.Request(cfg["url"] + path, data=json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None, headers=h, method=method)
    with urllib.request.urlopen(req) as r:
        t = r.read().decode("utf-8"); return json.loads(t) if t else None
tok = call("/auth/v1/token?grant_type=password", "POST", {"email": cfg["staffEmail"], "password": PIN + "00"})["access_token"]

# 이름 / 별칭 / 역할 — '홍길동' 은 아직 실명을 안 받은 자리(별칭으로 구분)
LIST = [("박수일", "주방장님", "주방"), ("홍길동", "부장님", "주방"), ("홍길동", "홍언니", "주방"), ("홍길동", "왕효엄 언니", "주방"),
        ("홍길동", "팀장님", "홀"), ("홍길동", "만두언니", "홀"), ("임현숙", "임현숙언니", "홀"), ("홍길동", "의범", "홀"), ("김명실", "김명실 언니", "홀")]
have = {r["nick"] for r in call("/rest/v1/staff?store=eq.hanok&select=nick", token=tok)}
rows = []
for i, (name, nick, role) in enumerate(LIST):
    if nick in have: print("있음:", nick); continue
    rows.append({"id": "stf_%s%02d" % (format(int(time.time()), "x"), i), "store": "hanok", "name": name, "nick": nick, "role": role, "pay_type": "hourly", "pay": 0,
                 "tax": "4대보험", "weekly_pay": True, "sched": {"days": [False, True, True, True, True, True, True], "start": "10:00", "end": "22:00", "break": 60},
                 "start_date": None, "active": True, "sort": i})
if rows:
    call("/rest/v1/staff", "POST", rows, token=tok, prefer="return=minimal")
print("넣음:", [r["nick"] for r in rows])
