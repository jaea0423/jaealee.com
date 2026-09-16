# -*- coding: utf-8 -*-
"""층 이름 바꾸기(2026-09-16 '지하' → '저층'): stores.settings 의 rooms.floor(예정 설정 안 포함)와 reservations 의 seatPref 'table:지하'.
   python work/rename_floor.py  (HANOK_PIN 필요). 한 번만."""
import io, json, os, sys, urllib.parse, urllib.request, re
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(io.open(os.path.join(BASE, "supabase.dev.json"), encoding="utf-8"))
PIN = os.environ.get("HANOK_PIN"); assert PIN
def call(path, method="GET", body=None, token=None, prefer=None):
    h = {"apikey": cfg["anonKey"], "Authorization": "Bearer " + (token or cfg["anonKey"]), "Content-Type": "application/json"}
    if prefer: h["Prefer"] = prefer
    req = urllib.request.Request(cfg["url"] + path, data=json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None, headers=h, method=method)
    with urllib.request.urlopen(req) as r:
        t = r.read().decode("utf-8"); return json.loads(t) if t else None
tok = call("/auth/v1/token?grant_type=password", "POST", {"email": cfg["staffEmail"], "password": PIN + "00"})["access_token"]
OLD, NEW = "지하", "저층"
st = call("/rest/v1/stores?key=eq.hanok&select=settings", token=tok)[0]["settings"]
txt = json.dumps(st, ensure_ascii=False)
n = txt.count('"floor": "%s"' % OLD)
txt = txt.replace('"floor": "%s"' % OLD, '"floor": "%s"' % NEW)
call("/rest/v1/stores?key=eq.hanok", "PATCH", {"settings": json.loads(txt)}, token=tok, prefer="return=minimal")
print("settings floor 바꿈:", n)
q = urllib.parse.quote("table:" + OLD)
rows = call("/rest/v1/reservations?data->>seatPref=eq." + q + "&select=*", token=tok)
for r in rows: r["data"]["seatPref"] = "table:" + NEW
for i in range(0, len(rows), 200):
    call("/rest/v1/reservations?on_conflict=id", "POST", rows[i:i+200], token=tok, prefer="resolution=merge-duplicates,return=minimal")
print("reservations seatPref 바꿈:", len(rows))
