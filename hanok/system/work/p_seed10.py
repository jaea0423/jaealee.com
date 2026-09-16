# -*- coding: utf-8 -*-
"""seed_dev.py 를 10차(홈페이지 연동·홈페이지 관리·예정 설정·사용 중지) 기준으로 넓힙니다. 한 번만 적용."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "seed_dev.py")
s = io.open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)

rep('''"""dev DB 에 더미 예약을 넣습니다 (2026-08-01 ~ 2026-10-31). 실서비스(prod)에는 절대 쓰지 않습니다.''',
    '''"""dev DB 에 더미 예약을 넣습니다 (2026-08-01 ~ 2026-11-30). 실서비스(prod)에는 절대 쓰지 않습니다.
   10차(2026-09-16): 홈페이지 예약(requests, source 기타·홈페이지 예약) · 사용 중지(하루/기간/시각) · 임시 휴무·임시 운영시간 · 예정 설정(여포 룸) ·
   겹침 강한 경고 · 사용 중지 좌석에 잡힌 예약 · 어제는 확정으로 남김(자동 처리 확인) · 문자 흉내 기록 · 같은 번호 두 건.
   먼저 SQL Editor 에서 표를 비우고(work/seed_dev.py 위 안내 SQL) 돌립니다. 설정(stores.settings)의 blocks·overrides·scheduled 도 이 값으로 덮습니다.''')

# 어제는 일부 '확정' 으로 남겨 자동 처리(방문/노쇼 판단)를 볼 수 있게
rep('''        if is_past: status = random.choices(["방문", "노쇼", "취소"], [86, 5, 9])[0]''',
    '''        yesterday = (datetime.datetime.strptime(today, "%Y-%m-%d") - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if date == yesterday: status = random.choices(["확정", "방문", "취소"], [40, 52, 8])[0]   # 어제 확정 = 아직 방문 처리 안 한 것
        elif is_past: status = random.choices(["방문", "노쇼", "취소"], [86, 5, 9])[0]''')
# 변경 이력 항목에 이전→이후 값(앱 형식 {n,a,b})
rep('''        changes.append({"on": when, "at": when + "T04:00:00.000Z", "kind": "변경", "items": [{"n": random.choice(["인원", "시각", "좌석"])}]})''',
    '''        n = random.choice(["인원", "시간", "좌석"])
        item = {"n": n, "a": "4명", "b": "%d명" % ppl} if n == "인원" else ({"n": n, "a": "오후 6:00", "b": hm(t)} if n == "시간" else {"n": n, "a": "미배정", "b": "룸"})
        changes.append({"on": when, "at": when + "T04:00:00.000Z", "kind": "변경", "items": [item]})''')
# 경로: 미래 예약의 일부는 홈페이지 예약(기타 · 홈페이지 예약) — requests 표와 짝
rep('''    src = random.choices(st["sources"], ([55, 30, 10, 5] + [2] * 10)[:len(st["sources"])])[0]''',
    '''    src = random.choices(st["sources"], ([55, 30, 10, 5] + [2] * 10)[:len(st["sources"])])[0]
    web = (not is_past) and random.random() < 0.10
    if web: src = "기타"''')
rep('''        "source": src, "sourceDetail": random.choice(SRC_DETAIL) if src == "기타" else "",''',
    '''        "source": src, "sourceDetail": "홈페이지 예약" if web else (random.choice(SRC_DETAIL) if src == "기타" else ""),''')
# 문자 흉내 기록: 확정 문자 한 통(미래 확정의 절반), 재안내(어제·오늘)
rep('''    if is_past and status == "방문" and random.random() < 0.5: rec["auto"] = True
    return rec''',
    '''    if is_past and status == "방문" and random.random() < 0.5: rec["auto"] = True
    if ph and status in ("확정", "방문") and random.random() < 0.5:
        rec["sms"].append({"kind": "확정", "at": created, "to": ph, "offset": None, "resent": False, "mock": True,
                           "text": "[한옥반점] %s님, %s %s %d명 예약이 확정되었습니다. 문의 031-724-1004" % (name, date, hm(t), ppl)})
        if date <= today and random.random() < 0.7:
            rec["sms"].append({"kind": "재안내", "at": date + "T00:00:00.000Z", "to": ph, "offset": 1, "resent": False, "mock": True,
                               "text": "[한옥반점] %s님, 내일 %s %d명 예약 안내드립니다. 변경은 031-724-1004" % (name, hm(t), ppl)})
    if web: rec["_web"] = True
    return rec''')
# 날짜 범위
rep('''    d = datetime.date(2026, 8, 1); end = datetime.date(2026, 10, 31)''',
    '''    d = datetime.date(2026, 8, 1); end = datetime.date(2026, 11, 30)''')
rep('''    if d > datetime.date(2026, 10, 12): weights = [25, 45, 25, 5, 0]   # 먼 미래는 드문드문''',
    '''    if d > datetime.date(2026, 10, 12): weights = [25, 45, 25, 5, 0]   # 먼 미래는 드문드문
    if d > datetime.date(2026, 11, 5): weights = [55, 35, 10, 0, 0]''')
# to_row: 홈페이지 예약 표시는 data 에 안 남김
rep('''def to_row(rec):
    rec.pop("_none", None)''',
    '''def to_row(rec):
    rec.pop("_none", None); rec.pop("_web", None)''')

# main: 의도한 케이스 + requests + 설정
rep('''    for i in range(0, len(rows), 200):
        call("/rest/v1/reservations", "POST", rows[i:i+200], token=tok, prefer="return=minimal")
        print("넣음", i + len(rows[i:i+200]), "/", len(rows))
    print("완료: %d 건. 2026-08-01 ~ 2026-10-31 · 날짜 프로필 %s" % (len(rows), profs))''',
    '''    T = datetime.date.today()
    def D(n): return (T + datetime.timedelta(days=n)).strftime("%Y-%m-%d")
    def dow_of(ds): return (datetime.datetime.strptime(ds, "%Y-%m-%d").weekday() + 1) % 7
    def add(rec): rows.append(to_row(rec)); return rows[-1]
    r_by_name = {r["name"]: r for r in ROOMS}
    # ----- 일부러 만든 케이스 (내일~) -----
    # 1) 같은 룸에 1시간 안 두 건 확정(강한 겹침 경고) — 내일 18:00 · 18:30 조조
    for t in (18*60, 18*60+30):
        add(base_rec(D(1), dow_of(D(1)), t, 4, today, roomId=r_by_name["조조"]["id"], status="확정", menuType="코스", courses=make_courses(dow_of(D(1)), t, 4, "ok"), memo="같은 방 30분 차이 — 사장님이 알고 받음"))
    # 2) 사용 중지 좌석(주유, 내일 하루)에 잡힌 예약
    add(base_rec(D(1), dow_of(D(1)), 12*60, 5, today, roomId=r_by_name["주유"]["id"], status="확정", menuType="코스", courses=make_courses(dow_of(D(1)), 12*60, 5, "ok"), memo="주유 수리 전에 받은 예약 — 다른 방으로 옮겨야 함"))
    # 3) 전화 없음 + 단체 12명 룸 합침(동탁) + 알러지
    big = base_rec(D(2), dow_of(D(2)), 18*60, 12, today, roomId=r_by_name["동탁"]["id"], status="확정", menuType="코스", courses=make_courses(dow_of(D(2)), 18*60, 12, "ok"), request="단체 계산서 · 상석 준비"); big["phone"] = ""; big["allergy"] = "갑각류 알러지 2명"; add(big)
    # 4) 노쇼 이력 번호로 미래 확정 (REPEAT 첫 사람을 노쇼로 만들고 미래 예약)
    nsn, nsp = REPEAT[0]
    add(base_rec(D(-5), dow_of(D(-5)), 19*60, 3, today, seatPref="table:" + FLOORS[0], status="노쇼"))
    ns2 = base_rec(D(-12), dow_of(D(-12)), 12*60, 2, today, seatPref="table:" + FLOORS[0], status="노쇼"); ns2["name"] = nsn; ns2["phone"] = nsp; add(ns2)
    ns3 = base_rec(D(3), dow_of(D(3)), 19*60, 4, today, seatPref="room-any", status="확정", menuType="확인 필요"); ns3["name"] = nsn; ns3["phone"] = nsp; ns3["memo"] = "노쇼 이력 — 전날 확인 전화"; add(ns3)
    # 5) 지난 날짜에 아직 확정(방문 처리 안 됨) — 그저께
    add(base_rec(D(-2), dow_of(D(-2)), 13*60, 2, today, seatPref="table:" + FLOORS[1], status="확정", memo="방문 처리 빠뜨림"))
    # 6) 예정 설정(여포 룸, D+7 부터)이 생기기 전 날짜에 여포를 잡은 예약은 없음. 대신 D+8 에 여포 지정 예약(예정 좌석)
    yeopo_id = "r_yeopo"
    add(base_rec(D(8), dow_of(D(8)), 18*60, 6, today, roomId=yeopo_id, status="확정", menuType="코스", courses=make_courses(dow_of(D(8)), 18*60, 6, "ok"), memo="여포 룸(예정 설정) 첫 손님"))
    # 7) 임시 휴무일(D+9)에 잡힌 예약 — 경고
    add(base_rec(D(9), dow_of(D(9)), 12*60, 4, today, seatPref="table:" + FLOORS[0], status="확정", memo="휴무일인데 받아 둠 — 확인"))
    # 8) 정원 초과 룸(조조 8명), 최소 미달 룸(동탁 4명) — 모레
    add(base_rec(D(2), dow_of(D(2)), 12*60, 8, today, roomId=r_by_name["조조"]["id"], status="확정", menuType="코스", courses=make_courses(dow_of(D(2)), 12*60, 8, "ok")))
    add(base_rec(D(2), dow_of(D(2)), 12*60+30, 4, today, roomId=r_by_name["동탁"]["id"], status="확정", menuType="코스", courses=make_courses(dow_of(D(2)), 12*60+30, 4, "ok")))
    # 9) 어린이만(성인 없음) + 의자 초과 — 내일 점심 테이블
    kid = base_rec(D(1), dow_of(D(1)), 12*60+30, 3, today, seatPref="table:" + FLOORS[0], status="확정", infants=3); kid["chairs"] = 4; add(kid)
    # 10) 라스트오더 뒤 · 브레이크 안 — 내일
    add(base_rec(D(1), dow_of(D(1)), 20*60+50, 2, today, seatPref="table:" + FLOORS[0], status="확정", memo="라스트오더 지나서 받음"))
    add(base_rec(D(1), dow_of(D(1)), 16*60, 4, today, seatPref="table:" + FLOORS[1], status="확정", memo="브레이크 중 — 단골"))
    # 11) 지난 3주 안에 취소→노쇼 판단 케이스: 당일 취소
    cc = base_rec(D(-3), dow_of(D(-3)), 18*60, 4, today, roomId=r_by_name["관우"]["id"], status="취소"); cc["changes"][-1]["on"] = D(-3); add(cc)
    # ----- 같은 날 같은 번호 두 건 (중복 확인 케이스) — 내일 -----
    tomorrow = D(1)
    dup = [r for r in rows if r["date"] == tomorrow and r["status"] == "확정" and r["phone"]][:1]
    if dup:
        c = json.loads(json.dumps(dup[0])); c["id"] = "res_" + str(uuid.uuid4()); c["time"] = "19:30"; c["data"]["memo"] = "같은 번호로 두 번 예약 — 같은 팀인지 확인"; c["data"]["sourceDetail"] = ""; rows.append(c)
    for i in range(0, len(rows), 200):
        call("/rest/v1/reservations", "POST", rows[i:i+200], token=tok, prefer="return=minimal")
        print("넣음", i + len(rows[i:i+200]), "/", len(rows))
    print("예약 완료: %d 건. 2026-08-01 ~ 2026-11-30 · 날짜 프로필 %s" % (len(rows), profs))

    # ----- 홈페이지 예약(requests): 확정된 것은 예약과 짝, 대기 5·거절 1·만료 1 -----
    reqs = []
    def req(rid, rec_row, status="대기", **kw):
        d = rec_row
        x = {"id": rid, "store": "hanok", "date": d["date"], "time": d["time"], "adults": max(2, d["people"] - d["data"].get("infants", 0)), "kids": d["data"].get("infants", 0),
             "people": d["people"], "seat": "room" if (d["room_id"] and d["room_id"].startswith("r")) or (d["data"].get("seatPref") == "room-any") else "table",
             "course": "later" if d["data"].get("menuType") in ("코스", "확인 필요") else "none", "course_label": "미정" if d["data"].get("menuType") in ("코스", "확인 필요") else "",
             "name": d["name"], "phone": d["phone"] or "01000000000", "request": d["data"].get("request", ""), "status": status, "reason": "", "res_id": None,
             "created_at": d["created_at"], "expires_at": (datetime.datetime.strptime(d["created_at"][:19], "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")}
        x.update(kw); reqs.append(x); return x
    web_rows = [r for r in rows if r["data"].get("sourceDetail") == "홈페이지 예약"]
    for r in web_rows: req("rq_" + r["id"][4:12], r, "확정", res_id=r["id"])
    now = datetime.datetime.utcnow()
    def pending(rid, date, time, adults, kids, seat, course, label, name, phone, request, hours_left=20):
        reqs.append({"id": rid, "store": "hanok", "date": date, "time": time, "adults": adults, "kids": kids, "people": adults + kids, "seat": seat, "course": course, "course_label": label,
                     "name": name, "phone": phone, "request": request, "status": "대기", "reason": "", "res_id": None,
                     "created_at": (now - datetime.timedelta(hours=24 - hours_left)).strftime("%Y-%m-%dT%H:%M:%SZ"), "expires_at": (now + datetime.timedelta(hours=hours_left)).strftime("%Y-%m-%dT%H:%M:%SZ")})
    pending("rq_p1", D(2), "12:00", 6, 1, "room", "set:요리사 추천세트", "요리사 추천세트", "박보검", "01055551111", "아이 의자 하나 부탁드립니다", 21)
    pending("rq_p2", D(3), "18:30", 2, 0, "table", "none", "", "장원영", "01055552222", "", 15)
    pending("rq_p3", D(1), "18:00", 5, 0, "room", "later", "미정", "손흥민", "01055553333", "룸이면 어디든 괜찮아요", 9)          # 내일 18:00 룸 — 조조 겹침 날이라 자리 없음 경고 가능
    pending("rq_p4", D(2), "18:00", 4, 0, "table", "course:촉 코스", "촉 코스", nsn, "".join(ch for ch in nsp if ch.isdigit()), "", 6)   # 노쇼 이력 번호 + 같은 날 예약 있는 번호
    pending("rq_p5", D(1), "12:30", 2, 0, "table", "none", "", "카리나", "01055555555", "", 0.7)                              # 40분 남음
    reqs.append({"id": "rq_rej1", "store": "hanok", "date": D(4), "time": "19:00", "adults": 3, "kids": 0, "people": 3, "seat": "room", "course": "later", "course_label": "미정",
                 "name": "유재석", "phone": "01055556666", "request": "", "status": "거절", "reason": "룸은 성인 5명부터 받고 있습니다", "res_id": None,
                 "created_at": (now - datetime.timedelta(hours=30)).strftime("%Y-%m-%dT%H:%M:%SZ"), "expires_at": (now - datetime.timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")})
    reqs.append({"id": "rq_exp1", "store": "hanok", "date": D(5), "time": "12:00", "adults": 2, "kids": 0, "people": 2, "seat": "table", "course": "none", "course_label": "",
                 "name": "아이유", "phone": "01055557777", "request": "", "status": "만료", "reason": "24시간 안에 처리되지 않음", "res_id": None,
                 "created_at": (now - datetime.timedelta(hours=40)).strftime("%Y-%m-%dT%H:%M:%SZ"), "expires_at": (now - datetime.timedelta(hours=16)).strftime("%Y-%m-%dT%H:%M:%SZ")})
    for i in range(0, len(reqs), 200):
        call("/rest/v1/requests", "POST", reqs[i:i+200], token=tok, prefer="return=minimal")
    print("홈페이지 예약: %d 건 (대기 5 · 거절 1 · 만료 1 · 확정 %d)" % (len(reqs), len(web_rows)))

    # ----- 설정: 사용 중지 · 임시 휴무/운영시간 · 예정 설정(여포) -----
    def blk(room_name, frm, to, note, fromTime="", toTime="", openEnded=False):
        r = r_by_name[room_name]; r.setdefault("blocks", []); r["blocks"] = [b for b in r["blocks"] if not b.get("demo")]
        r["blocks"].append({"id": "blk_demo_" + room_name + "_" + frm, "from": frm, "to": to, "fromTime": fromTime, "toTime": toTime, "openEnded": openEnded, "note": note, "demo": True})
    for r in st["rooms"]: r["blocks"] = [b for b in r.get("blocks", []) if not b.get("demo")]
    blk("주유", D(1), D(1), "에어컨 수리")                       # 하루
    blk("초선", D(4), D(6), "장판 교체")                          # 기간
    blk("유비", D(2), D(2), "행사 준비", "11:00", "15:00")         # 하루 중 일부(시각)
    tables = [x for x in st["rooms"] if x["type"] == "table"]
    if tables:
        t0 = tables[-1]; t0["blocks"] = [b for b in t0.get("blocks", []) if not b.get("demo")]
        t0["blocks"].append({"id": "blk_demo_t_" + D(3), "from": D(3), "to": None, "fromTime": "", "toTime": "", "openEnded": True, "note": "의자 고장 — 해제할 때까지", "demo": True})
    st["overrides"] = [o for o in st.get("overrides", []) if not o.get("demo")] + [
        {"date": D(9), "closed": True, "note": "직원 워크숍", "demo": True},
        {"date": D(12), "closed": False, "open": "12:00", "close": "21:00", "bs": "", "be": "", "lo": "19:40", "note": "행사로 늦게 엶", "demo": True},
    ]
    # 예정 설정: D+7 부터 지하에 '여포' 파셜룸(4~8) 추가
    rooms_after = json.loads(json.dumps(st["rooms"]))
    if not any(r["id"] == yeopo_id for r in rooms_after):
        rooms_after.append({"id": yeopo_id, "name": "여포", "type": "room", "minCapacity": 4, "capacity": 8, "floor": "지하", "blocks": []})
    st["scheduled"] = [x for x in st.get("scheduled", []) if not x.get("demo")] + [
        {"id": "sc_demo_seats", "from": D(7), "to": None, "group": "seats", "values": {"rooms": rooms_after, "joins": st.get("joins", [])}, "note": "지하 여포 파셜룸 추가", "createdAt": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "by": "staff", "demo": True}]
    call("/rest/v1/stores?key=eq.hanok", "PATCH", {"settings": st}, token=tok, prefer="return=minimal")
    print("설정: 사용 중지 4(하루·기간·시각·무기한) · 임시 휴무 1 · 임시 운영시간 1 · 예정 설정 1(여포, %s 부터)" % D(7))''')
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
