# -*- coding: utf-8 -*-
"""홈페이지 관리 초안(site_draft) 정리 — 2026-09-20 부터 초안은 '기본값(data/site.js)과 다른 것만' 저장합니다(14b saDiff).
   그 전에 저장된 초안은 전체 복사본이라 옛 문구('저녁 코스 (종일)' 등)를 통째로 들고 있습니다.

   python work/site_draft_diff.py            초안이 기본값과 어디가 다른지 보여만 줌
   python work/site_draft_diff.py --slim     초안을 '다른 것만' 으로 다시 저장 (값은 그대로, 크기만 줄임)
   python work/site_draft_diff.py --reset    초안을 지움 → 다음에 홈페이지 관리를 열면 기본값(+적용판)에서 시작
   HANOK_PIN 환경변수 필요(직원 PIN). 기본값은 ../data/site.js 를 node 로 읽습니다."""
import io, json, os, sys, subprocess, urllib.request
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(io.open(os.path.join(BASE, "supabase.dev.json"), encoding="utf-8"))
PIN = os.environ.get("HANOK_PIN"); assert PIN, "HANOK_PIN 환경변수가 필요합니다"
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

def call(path, method="GET", body=None, token=None, prefer=None):
    h = {"apikey": cfg["anonKey"], "Authorization": "Bearer " + (token or cfg["anonKey"]), "Content-Type": "application/json"}
    if prefer: h["Prefer"] = prefer
    req = urllib.request.Request(cfg["url"] + path, data=json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None, headers=h, method=method)
    with urllib.request.urlopen(req) as r:
        t = r.read().decode("utf-8"); return json.loads(t) if t else None

def defaults():
    js = os.path.join(BASE, "..", "data", "site.js")
    out = subprocess.run(["node", "-e", "var window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.SITE_DEFAULT))", js], capture_output=True, text=True, encoding="utf-8")
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)

def diff(base, cur):   # 14b 의 saDiff 와 같은 규칙
    if not isinstance(cur, dict) or not isinstance(base, dict):
        return None if json.dumps(cur, sort_keys=True, ensure_ascii=False) == json.dumps(base, sort_keys=True, ensure_ascii=False) else cur
    out = {}
    for k, v in cur.items():
        d = diff(base.get(k), v)
        if d is not None: out[k] = d
    return out or None

def walk(d, pre=""):
    for k, v in d.items():
        if isinstance(v, dict): walk(v, pre + k + ".")
        else: print("  %s%s = %s" % (pre, k, json.dumps(v, ensure_ascii=False)[:120]))

tok = call("/auth/v1/token?grant_type=password", "POST", {"email": cfg["staffEmail"], "password": PIN + "00"})["access_token"]
rows = call("/rest/v1/site_draft?store=eq.hanok&select=data,updated_at,by", token=tok)
if not rows or not rows[0]["data"]:
    print("초안 없음"); sys.exit(0)
dr = rows[0]["data"]; base = defaults()
d = diff(base, dr) or {}
print("초안 저장:", rows[0]["updated_at"], rows[0]["by"], "· 키", len(json.dumps(dr)), "바이트 → 다른 것만", len(json.dumps(d)), "바이트")
print("기본값과 다른 칸:"); walk(d) if d else print("  (없음)")
if "--slim" in sys.argv:
    call("/rest/v1/site_draft?on_conflict=store", "POST", {"store": "hanok", "data": d, "by": "script"}, token=tok, prefer="resolution=merge-duplicates,return=minimal")
    print("→ 초안을 '다른 것만' 으로 다시 저장했습니다")
elif "--reset" in sys.argv:
    call("/rest/v1/site_draft?store=eq.hanok", "DELETE", token=tok, prefer="return=minimal")
    print("→ 초안을 지웠습니다. 다음에 홈페이지 관리를 열면 기본값에서 시작합니다")
