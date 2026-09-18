# -*- coding: utf-8 -*-
"""Supabase 세 테이블을 JSON 으로 받습니다 (hanok-backup 워크플로가 실행). 표준 라이브러리만 씀.
   환경변수: SUPABASE_URL, SUPABASE_SERVICE_KEY. 인자: 출력 폴더(기본 data)
   PostgREST 는 한 번에 최대 1,000행이라 Range 헤더로 이어 받습니다. 예약은 전체(삭제 포함), 로그는 최근 30일."""
import json, os, sys, datetime, urllib.request

URL = os.environ["SUPABASE_URL"].rstrip("/"); KEY = os.environ["SUPABASE_SERVICE_KEY"]
OUT = sys.argv[1] if len(sys.argv) > 1 else "data"
STEP = int(os.environ.get("BACKUP_PAGE", "1000"))
assert 1 <= STEP <= 1000, "PostgREST 는 한 번에 최대 1,000행 — BACKUP_PAGE 가 그보다 크면 조용히 불완전한 백업이 됩니다"

def fetch_all(path):
    rows, start = [], 0
    while True:
        req = urllib.request.Request(URL + "/rest/v1/" + path, headers={
            "apikey": KEY, "Authorization": "Bearer " + KEY, "Range-Unit": "items", "Range": "%d-%d" % (start, start + STEP - 1)})
        with urllib.request.urlopen(req) as r:
            page = json.loads(r.read().decode("utf-8"))
        rows.extend(page)
        if len(page) < STEP: break
        start += STEP
    return rows

def save(name, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1, sort_keys=True)   # 줄 단위 diff 가 되게 정렬·들여쓰기
    print("%s: %d 행" % (name, len(rows)))

since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
save("stores.json",       fetch_all("stores?select=*&order=key"))
save("reservations.json", fetch_all("reservations?select=*&order=date,time,id"))
save("logs-30d.json",     fetch_all("logs?select=*&order=at,id&at=gte." + since)   # 같은 시각이 여러 줄이면 페이지 경계에서 빠지거나 겹치므로 id 로 순서를 고정)
# 9·10차에서 생긴 표들 — 홈페이지 예약 접수, 홈페이지 내용(초안·적용 판). public_avail 은 시스템이 매번 다시 올리니 안 받음
save("requests.json",      fetch_all("requests?select=*&order=created_at,id"))
save("site_draft.json",    fetch_all("site_draft?select=*&order=store"))
save("site_versions.json", fetch_all("site_versions?select=*&order=id"))
save("site_posts.json",    fetch_all("site_posts?select=*&order=created_at,id"))
# 15차 직원 근태·손님 메모
save("staff.json",         fetch_all("staff?select=*&order=sort,name"))
save("attendance.json",    fetch_all("attendance?select=*&order=date,staff_id"))
save("customers.json",     fetch_all("customers?select=*&order=phone"))
save("hr_settings.json",   fetch_all("hr_settings?select=*"))
save("thanks_sms.json",    fetch_all("thanks_sms?select=*&order=send_at,id"))   # 14차 소식 글(첨부 파일 자체는 Storage — 백업 안 됨)
with open(os.path.join(OUT, "backup-at.txt"), "w") as f: f.write(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")
