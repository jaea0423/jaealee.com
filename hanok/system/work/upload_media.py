# -*- coding: utf-8 -*-
"""메뉴판 PDF · 광고 영상을 Supabase Storage(site 버킷)에 올리고 주소를 연결합니다 (재아 09-20: 파일은 저장소가 아니라 서버에).
   python work/upload_media.py [menu.pdf 경로] [ad.mp4 경로] [--fresh]   (기본: 바탕화면의 menu.pdf, ad.mp4 · HANOK_PIN 환경변수 필요)
   --fresh: 옛 초안(09-20 전 전체 복사본)을 버리고 기본값에서 시작 — 초안에 옛 문구가 남아 있을 때

   하는 일
   1) Storage  site/hanok/pdf/<시각>_menu.pdf, site/hanok/video/<시각>_ad.mp4 로 올림(공개 주소)
   2) 시스템 설정 stores.settings.tvAd = 영상 주소  → TV 목록형·예약 없을 때 화면이 이 영상을 틉니다
   3) 홈페이지 초안·적용판 info.menuPdf = PDF 주소 → 사이트 차림 페이지의 '메뉴판 PDF' 링크
      초안은 '기본값과 다른 것만' 으로 다시 저장하고(site_draft_diff 와 같은 규칙), 같은 내용으로 적용판(site_versions, 지금)을 한 판 넣습니다.
   화면에서 하는 것과 같은 결과입니다(홈페이지 관리 → 올리기 → 적용 / 설정 → 디스플레이 → 영상 올리기 → 적용하기)."""
import io, json, os, sys, time, subprocess, urllib.request, datetime
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(io.open(os.path.join(BASE, "supabase.dev.json"), encoding="utf-8"))
PIN = os.environ.get("HANOK_PIN"); assert PIN, "HANOK_PIN 환경변수가 필요합니다"
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
DESK = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PDF = ARGS[0] if len(ARGS) > 0 else os.path.join(DESK, "menu.pdf")
MP4 = ARGS[1] if len(ARGS) > 1 else os.path.join(DESK, "ad.mp4")

def call(path, method="GET", body=None, token=None, prefer=None, raw=None, ctype=None):
    h = {"apikey": cfg["anonKey"], "Authorization": "Bearer " + (token or cfg["anonKey"])}
    if prefer: h["Prefer"] = prefer
    data = raw if raw is not None else (json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None)
    h["Content-Type"] = ctype or "application/json"
    if raw is not None: h["x-upsert"] = "true"
    req = urllib.request.Request(cfg["url"] + path, data=data, headers=h, method=method)
    with urllib.request.urlopen(req) as r:
        t = r.read().decode("utf-8"); return json.loads(t) if t else None

def upload(local, kind, name, ctype):
    assert os.path.exists(local), "파일 없음: " + local
    size = os.path.getsize(local); assert size <= 50 * 1024 * 1024, "50MB 를 넘습니다: " + local
    path = "hanok/%s/%s_%s" % (kind, format(int(time.time()), "x"), name)
    call("/storage/v1/object/site/" + path, "POST", raw=io.open(local, "rb").read(), token=tok, ctype=ctype)
    url = cfg["url"] + "/storage/v1/object/public/site/" + path
    print("올림 %s (%dKB) → %s" % (name, size // 1024, url)); return url

def defaults():
    js = os.path.join(BASE, "..", "data", "site.js")
    out = subprocess.run(["node", "-e", "var window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.SITE_DEFAULT))", js], capture_output=True, text=True, encoding="utf-8")
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)
def diff(base, cur):
    if not isinstance(cur, dict) or not isinstance(base, dict):
        return None if json.dumps(cur, sort_keys=True, ensure_ascii=False) == json.dumps(base, sort_keys=True, ensure_ascii=False) else cur
    out = {}
    for k, v in cur.items():
        d = diff(base.get(k), v)
        if d is not None: out[k] = d
    return out or None
def merge(base, over):
    if not isinstance(over, dict) or not isinstance(base, dict): return over
    out = dict(base)
    for k, v in over.items(): out[k] = merge(base.get(k), v) if isinstance(base.get(k), dict) else v
    return out

tok = call("/auth/v1/token?grant_type=password", "POST", {"email": cfg["staffEmail"], "password": PIN + "00"})["access_token"]
pdf_url = upload(PDF, "pdf", "menu.pdf", "application/pdf")
mp4_url = upload(MP4, "video", "ad.mp4", "video/mp4")

# 2) 시스템 설정 tvAd
st = call("/rest/v1/stores?key=eq.hanok&select=settings", token=tok)[0]["settings"]
st["tvAd"] = mp4_url
call("/rest/v1/stores?key=eq.hanok", "PATCH", {"settings": st}, token=tok, prefer="return=minimal")
print("설정 tvAd 연결")

# 3) 홈페이지 초안·적용판 info.menuPdf
base = defaults()
dr = call("/rest/v1/site_draft?store=eq.hanok&select=data", token=tok)
cur = merge(base, dr[0]["data"]) if dr and dr[0]["data"] and "--fresh" not in sys.argv else base   # --fresh: 옛 초안(전체 복사본)을 버리고 기본값에서
cur.setdefault("info", {})["menuPdf"] = pdf_url
d = diff(base, cur) or {}
call("/rest/v1/site_draft?on_conflict=store", "POST", {"store": "hanok", "data": d, "by": "script"}, token=tok, prefer="resolution=merge-duplicates,return=minimal")
call("/rest/v1/site_versions", "POST", {"store": "hanok", "data": d, "apply_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "note": "메뉴판 PDF 교체(script)", "by": "script"}, token=tok, prefer="return=minimal")
print("홈페이지 menuPdf 연결 · 적용판 생성. 기본값과 다른 칸:", json.dumps(d, ensure_ascii=False)[:300])
