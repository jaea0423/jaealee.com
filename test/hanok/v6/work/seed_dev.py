# -*- coding: utf-8 -*-
"""dev DB 에 더미 예약을 넣습니다 (2026-08-01 ~ 2026-10-31). 실서비스(prod)에는 절대 쓰지 않습니다.
   8차 좌석 모형(룸 8·합침·층 테이블·특정 테이블·나눠 앉기) 기준. 날짜마다 없음/한산/보통/붐빔/포화 프로필을 섞습니다.

  python work/seed_dev.py            넣기 (이미 demo 행이 있으면 먼저 지우고 다시)
  python work/seed_dev.py clear      demo 행만 지우기 (data.demo = true 인 행 — 앱의 '예시 데이터 지우기' 와 같은 기준)

행 모양은 앱의 resToRow 와 같게 만듭니다 (phone 숫자만, people 총원, 나머지 data). data.demo = true 로 표시.
이름은 재아 요청대로 한국 연예인 위주 + 가끔 외국인(영어/한글 표기) + 기업·단체명. 알러지·요청·메모·경고 케이스를 섞습니다."""
import io, json, os, sys, random, uuid, urllib.request, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(io.open(os.path.join(BASE, "supabase.dev.json"), encoding="utf-8"))
assert cfg.get("demo") is True, "demo:true 인 dev 설정에만 넣습니다"
PIN = os.environ.get("HANOK_PIN")
if not PIN: raise SystemExit("환경변수 HANOK_PIN 에 dev PIN 을 넣고 실행하세요 (예: PowerShell  $env:HANOK_PIN='####'; python work/seed_dev.py). 기본값은 두지 않습니다 — 점검 S1")

def call(path, method="GET", body=None, token=None, prefer=None):
    h = {"apikey": cfg["anonKey"], "Authorization": "Bearer " + (token or cfg["anonKey"]), "Content-Type": "application/json"}
    if prefer: h["Prefer"] = prefer
    req = urllib.request.Request(cfg["url"] + path, data=json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None, headers=h, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            t = r.read().decode("utf-8"); return json.loads(t) if t else None
    except urllib.error.HTTPError as e:
        raise SystemExit("%s %s → %s %s" % (method, path, e.code, e.read().decode("utf-8")[:300]))

tok = call("/auth/v1/token?grant_type=password", "POST", {"email": cfg["staffEmail"], "password": PIN + "00"})["access_token"]
st = call("/rest/v1/stores?key=eq.hanok&select=settings", token=tok)[0]["settings"]
ROOMS = [r for r in st["rooms"] if r["type"] == "room"]
TABLES = [r for r in st["rooms"] if r["type"] == "table"]
JOINS = st.get("joins", [])
FLOORS = []
for _t in TABLES:
    if (_t.get("floor") or "") not in FLOORS: FLOORS.append(_t.get("floor") or "")
CG = {g["id"]: g for g in st["courseGroups"]}

def clear():
    n = 0
    while True:
        rows = call("/rest/v1/reservations?data->>demo=eq.true&deleted_at=is.null&select=id&limit=500", token=tok)
        if not rows: break
        ids = ",".join('"%s"' % r["id"] for r in rows)
        # 하드 DELETE 권한은 뺐습니다(점검 S4). 아주 옛 날짜로 soft delete 하면 앱의 휴지통 창(최근 N일)에도 안 잡힙니다
        call("/rest/v1/reservations?id=in.(%s)" % ids, "PATCH", {"deleted_at": "2000-01-01T00:00:00Z"}, token=tok, prefer="return=minimal"); n += len(rows)
    print("demo 행 정리(soft delete):", n)

if "clear" in sys.argv[1:]:
    clear(); sys.exit(0)

random.seed(20260914)
# ---------- 이름 ----------
KO = ["유재석","아이유","손흥민","김연아","봉준호","박보검","송혜교","이정재","정우성","전지현","공유","김태희","조인성","하정우","마동석","김혜수",
      "배두나","이병헌","최민식","송강호","박서준","김고은","수지","이효리","강호동","신동엽","박나래","장도연","이서진","차은우","박은빈","김선호",
      "임영웅","성시경","백지영","이승기","윤아","태연","제니","지수","로제","뷔","지민","정국","RM","박지성","류현진","김민재","이강인","황희찬",
      "장원영","안유진","카리나","윈터","한소희","김유정","남주혁","박신혜","전도연","김윤석","황정민","라미란","염정아","김서형","장항준","김은희",
      "나영석","김태호","유희열","이적","윤종신","하동균","박효신","김범수","거미","에일리","백예린","이문세","조용필","나훈아","심수봉","송가인",
      "정동원","이찬원","장윤정","김호중","허경환","김준호","문세윤","이용진","이진호","양세형","양세찬","조세호","지석진","하하","김종국","송지효",
      "전소민","이광수","김종민","은지원","이수근","규현","민호","윤두준","기안84","이말년","주호민","침착맨","김풍","박명수","정준하","노홍철","정형돈","길"]
FOREIGN = ["Tom Cruise","톰 크루즈","Emma Watson","엠마 스톤","레오나르도 디카프리오","Brad Pitt","제이슨 모모아","Keanu Reeves","키아누 리브스",
           "Anne Hathaway","앤 해서웨이","Timothée Chalamet","티모시 샬라메","Ryan Gosling","라이언 고슬링","Taylor Swift","테일러 스위프트",
           "Sakurai Sho","기무라 타쿠야","Lisa","리사","Zendaya","젠데이아","Scarlett Johansson","Michael Jordan","마이클 조던"]
COMPANY = ["SK하이닉스 개발팀","삼성전자 인사팀","춘천시청 총무과","강원대 컴공 동문회","네이버 클라우드 3팀","한림대병원 내과","카카오모빌리티",
           "LG전자 H&A 사업부","현대자동차 남양연구소","춘천교대 92학번","강원도청 관광정책과","KBS 춘천방송총국","하나은행 춘천지점",
           "춘천마임축제 사무국","강원FC 프런트","넥슨 데이터팀","토스 결제팀","춘천고 3학년 8반 학부모회","봄내로타리클럽","한국은행 강원본부"]
LONGNAME = ["김수한무거북이와두루미삼천갑자동방삭","스티븐 스필버그 감독님 일행","크리스토퍼 놀란"]

ALLERGY = ["갑각류 알러지 1명","땅콩 알러지 (아이)","밀가루 알러지 — 글루텐 주의","조개류 못 드심","견과류 전부 알러지 2명","계란 알러지 1명","우유 알러지 (유아)"]
REQUEST = ["송별회","상견례 — 조용한 방으로","생일 케이크 반입","창가 자리","휠체어 손님 1분","회식 — 술 많이","돌잔치 뒤풀이","어르신 생신, 의자 등받이 있는 곳","촬영 있음 (조용히)","프로포즈 예정 — 케이크 타이밍 맞춰 주세요","단체 계산서 필요","코스 늦게 시작해 주세요 (30분 뒤 도착 손님 있음)"]
MEMO = ["사장님 지인","단골 — 상석 준비","지난번 노쇼 이력 있음, 확인 전화","매니저가 대신 예약함","현금 결제 예정","방송국 — 카메라 들어옴","VIP","네이버 리뷰 이벤트 손님","술 취하면 시끄러움 주의","아이 둘, 유아의자 확인"]
SRC_DETAIL = ["지인 소개","인스타 DM","워크인 재방문","블로그 보고","카카오 채널"]

def pick_name():
    r = random.random()
    if r < 0.80: return random.choice(KO)
    if r < 0.92: return random.choice(FOREIGN)
    if r < 0.99: return random.choice(COMPANY)
    return random.choice(LONGNAME)

def phone():
    return "010-%04d-%04d" % (random.randint(1000, 9999), random.randint(1000, 9999))

REPEAT = [(pick_name(), phone()) for _ in range(12)]   # 단골·노쇼 이력용 — 같은 번호가 여러 날 나옵니다


# ---------- 운영시간·세션 ----------
HOLIDAYS = set(["2026-08-15","2026-08-17","2026-09-24","2026-09-25","2026-09-26","2026-09-28","2026-10-03","2026-10-05","2026-10-09"])   # 앱의 KR_HOLIDAYS 2026 중 8~10월
def hours(dow):
    return st["schedules"][0]["days"][dow]
def tm(s): return int(s[:2]) * 60 + int(s[3:])
def hm(m): return "%02d:%02d" % (m // 60, m % 60)
def sessions(dow): return hours(dow).get("sessions", [])
def sess_at(dow, t):
    ss = sessions(dow); cur = ss[0] if ss else None
    for se in ss:
        if tm(se["from"]) <= t: cur = se
    return cur
def stay_of(dow, t):
    """앱의 stayMinAt 와 같은 규칙 — 세션 '끝까지' 면 세션 끝까지, 아니면 분"""
    se = sess_at(dow, t)
    if not se: return 150
    if se.get("stay") == "end": return max(30, tm(se["until"]) - t)
    return max(30, int(se.get("stay") or 110))
def slots_of(dow, se):
    """세션 시작~접수 마감, 30분 간격. 브레이크 안은 뺌"""
    h = hours(dow); bs = tm(h["bs"]) if h.get("bs") else None; be = tm(h["be"]) if h.get("be") else None
    t = tm(se["from"]); last = tm(se["lastBook"]); out = []
    while t <= last:
        if not (bs and be and bs <= t < be): out.append(t)
        t += 30
    return out
POPULAR = {11*60+30, 12*60, 12*60+30, 13*60, 18*60, 18*60+30, 19*60}

# ---------- 자리 점유 추적(같은 자리 겹침을 안 만들려고) ----------
USED = {}   # date → [(seat_id, start, end)]
def busy(date, sid, t, stay):
    return any(s == sid and a < t + stay and t < b for s, a, b in USED.get(date, []))
def mark(date, ids, t, stay):
    USED.setdefault(date, []).extend((sid, t, t + stay) for sid in ids)
def free_tables(date, fl, t, stay):
    return [x for x in TABLES if (x.get("floor") or "") == fl and not busy(date, x["id"], t, stay)]
def seats_of(x): return x.get("seats") or 4
def table_fit(date, fl, t, stay, ppl):
    """앱의 findSeat(테이블·층) 흉내 — 하나 / 붙임 조합 / 나눠 앉기 / 없으면 None. 순서는 설정 순서, 2명은 4인석 우선"""
    ft = free_tables(date, fl, t, stay)
    one = [x for x in ft if seats_of(x) >= ppl and (x.get("minCapacity") or 0) <= ppl and (x.get("capacity") or seats_of(x)) >= ppl]
    one.sort(key=lambda x: (0 if (ppl <= 2 and seats_of(x) >= 4) else 1, TABLES.index(x)))
    if one: return [one[0]["id"]], False
    pool = [x for x in ft if x.get("joinWith")]
    best = [None]
    def rec(combo, total):
        if total >= ppl:
            if best[0] is None or len(combo) < len(best[0]): best[0] = list(combo)
            return
        if len(combo) >= 5: return
        for x in pool:
            if x in combo or pool.index(x) < pool.index(combo[-1]): continue
            if not all(x["id"] in c.get("joinWith", []) for c in combo): continue
            combo.append(x); rec(combo, total + seats_of(x)); combo.pop()
    for x in pool: rec([x], seats_of(x))
    if best[0]: return [x["id"] for x in best[0]], False
    ft2 = sorted(ft, key=lambda x: -seats_of(x)); pick = []; s = 0   # 나눠 앉기: 붙임 무관, 큰 테이블부터
    for x in ft2:
        if s >= ppl: break
        pick.append(x); s += seats_of(x)
    if s >= ppl and len(pick) > 1: return [x["id"] for x in pick], True
    return None, False

# ---------- 코스 ----------
def course_gid(dow, t): return "cg_dinner" if t >= 17 * 60 else ("cg_welunch" if dow in (0, 6) else "cg_wdlunch")
def make_courses(dow, t, adults, mode):
    """mode: ok / short(인원 부족) / mixed(두 종류)"""
    gid = course_gid(dow, t); g = CG[gid]; c = {}
    item = random.choice(g["items"])
    if mode == "short": c["%s|%s" % (gid, item)] = max(1, adults - random.randint(1, 2))
    elif mode == "mixed":
        c["%s|%s" % (gid, item)] = max(1, adults - 1)
        c["%s|%s" % (gid, random.choice([i for i in g["items"] if i != item]))] = 1
    else: c["%s|%s" % (gid, item)] = adults
    return c

# ---------- 예약 한 건 ----------
def base_rec(date, dow, t, ppl, today, **kw):
    is_past = date < today
    name = pick_name(); ph = phone()
    if random.random() < 0.15: name, ph = random.choice(REPEAT)
    if random.random() < 0.05: ph = ""                     # 번호 없음 케이스
    infants = kw["infants"] if "infants" in kw else (random.choice([1, 1, 2]) if (ppl >= 3 and random.random() < 0.18) else 0)
    status = kw.get("status")
    if not status:
        if is_past: status = random.choices(["방문", "노쇼", "취소"], [86, 5, 9])[0]
        elif date == today: status = random.choices(["확정", "방문", "취소"], [70, 22, 8])[0]
        else: status = random.choices(["확정", "취소"], [94, 6])[0]
    created_days = random.choice([0, 0, 1, 2, 3, 5, 7, 10, 14, 21, 30])
    created = (datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=created_days, hours=random.randint(1, 12))).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    changes = [{"on": created[:10], "at": created, "kind": "등록", "items": []}]
    if status in ("취소", "노쇼"):
        when = date if random.random() < 0.6 else (datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=random.randint(1, 3))).strftime("%Y-%m-%d")
        changes.append({"on": when, "at": when + "T%02d:00:00.000Z" % random.randint(1, 12), "kind": status, "items": []})
    elif random.random() < 0.15:
        when = max(created[:10], (datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=random.choice([0, 0, 1]))).strftime("%Y-%m-%d"))
        changes.append({"on": when, "at": when + "T04:00:00.000Z", "kind": "변경", "items": [{"n": random.choice(["인원", "시각", "좌석"])}]})
    src = random.choices(st["sources"], ([55, 30, 10, 5] + [2] * 10)[:len(st["sources"])])[0]
    rec = {
        "id": "res_" + str(uuid.uuid4()), "date": date, "time": hm(t), "name": name, "phone": ph,
        "people": ppl, "infants": infants, "chairs": (infants if random.random() < 0.7 else max(0, infants - 1)) if infants else 0,
        "roomId": kw.get("roomId"), "extraIds": kw.get("extraIds", []),
        "seatPref": kw.get("seatPref") if not kw.get("roomId") else None,
        "tentativeRoomId": None, "tentativeExtra": [], "tentativeSplit": False,
        "source": src, "sourceDetail": random.choice(SRC_DETAIL) if src == "기타" else "",
        "createdAt": created, "menuType": kw.get("menuType", "해당 없음"), "courses": kw.get("courses", {}), "courseUndecided": kw.get("courseUndecided", False),
        "allergy": random.choice(ALLERGY) if random.random() < 0.12 else "", "allergyChecked": True,
        "request": kw.get("request", random.choice(REQUEST) if random.random() < 0.22 else ""),
        "memo": kw.get("memo", random.choice(MEMO) if random.random() < 0.15 else ""),
        "status": status, "changes": changes, "sms": [], "demo": True,
    }
    if is_past and status == "방문" and random.random() < 0.5: rec["auto"] = True
    return rec

def room_menu(dow, t, ppl, infants):
    """룸 예약의 식사 — 대부분 코스, 가끔 경고 케이스"""
    adults = max(1, ppl - infants); r = random.random()
    if r < 0.70: return {"menuType": "코스", "courses": make_courses(dow, t, adults, "ok")}
    if r < 0.78: return {"menuType": "코스", "courses": make_courses(dow, t, adults, "mixed")}
    if r < 0.84: return {"menuType": "코스", "courses": make_courses(dow, t, adults, "short")}   # 코스 인원 부족
    if r < 0.90: return {"menuType": "코스", "courses": {}, "courseUndecided": True}
    if r < 0.94: return {"menuType": "코스 상당", "courses": {}}
    if r < 0.97: return {"menuType": "확인 필요", "courses": {}}                                  # 코스 미확정
    return {"menuType": "해당 없음", "courses": {}}                                              # 룸·코스 아님

# ---------- 하루 ----------
def day_profile(d, dow):
    if dow in (0, 6):  weights = [3, 12, 35, 32, 18]     # 주말은 붐빔·포화가 많음
    elif dow == 1:     weights = [10, 35, 35, 15, 5]     # 월요일 한산
    else:              weights = [6, 22, 42, 22, 8]
    if d > datetime.date(2026, 10, 12): weights = [25, 45, 25, 5, 0]   # 먼 미래는 드문드문
    return random.choices(["none", "quiet", "normal", "busy", "full"], weights)[0]

def gen_day(date, dow, today, prof):
    rows = []
    if prof == "none": return rows
    frac = {"quiet": 0.25, "normal": 0.5, "busy": 0.75, "full": 0.95}[prof]
    for se in sessions(dow):
        sl = slots_of(dow, se)
        if not sl: continue
        f = frac * (1.0 if se["name"] == "저녁" else 0.85)
        # ----- 룸: 방마다 f 확률로 한 팀(주말 점심은 110분이라 두 팀까지) -----
        for room in ROOMS:
            teams = 1 if se.get("stay") == "end" else (2 if random.random() < f * 0.6 else 1)
            for k in range(teams):
                if random.random() > f: continue
                pool = [t for t in sl if not busy(date, room["id"], t, stay_of(dow, t))]
                if not pool: break
                t = random.choice([x for x in pool if x in POPULAR] or pool) if random.random() < 0.65 else random.choice(pool)
                lo, hi = (room.get("minCapacity") or 2), room["capacity"]
                ppl = random.randint(lo, hi)
                kw = {"roomId": room["id"]}
                if random.random() < 0.30: kw = {"seatPref": "room-any"}          # 룸 미정(잠정) — 실제로는 이런 접수가 많음(재아)
                r = random.random()
                if r < 0.03: ppl = hi + random.randint(1, 2)                  # 정원 초과 경고
                elif r < 0.06: ppl = max(1, lo - random.randint(1, 2))       # 최소 인원 미달 경고
                infants = random.choice([1, 2]) if (ppl >= 3 and random.random() < 0.2) else 0
                if ppl - infants < lo and r >= 0.06:                             # 유아를 빼도 최소 인원은 맞게 (일부러 만든 미달 케이스 제외)
                    if lo + infants <= hi: ppl = lo + infants
                    else: infants = 0
                kw.update(room_menu(dow, t, ppl, infants)); kw["infants"] = infants
                rec = base_rec(date, dow, t, ppl, today, **kw)
                if rec["status"] in ("확정", "방문") and rec["roomId"]: mark(date, [room["id"]], t, stay_of(dow, t))
                rows.append(rec)
        # ----- 룸 합침: 붐빌 때 가끔 -----
        if JOINS and random.random() < f * 0.35:
            j = random.choice(JOINS)
            for t in random.sample(sl, len(sl)):
                if all(not busy(date, i, t, stay_of(dow, t)) for i in j["ids"]):
                    ppl = random.randint(j["min"], j["max"]); infants = random.choice([0, 0, 1, 2])
                    kw = {"roomId": j["ids"][0], "extraIds": j["ids"][1:], "infants": infants, "request": random.choice(["단체 계산서 필요", "회식 — 술 많이", "송별회", "동문회 — 현수막 걸어도 되나요"])}
                    kw.update(room_menu(dow, t, ppl, infants))
                    rec = base_rec(date, dow, t, ppl, today, **kw)
                    if rec["status"] in ("확정", "방문"): mark(date, j["ids"], t, stay_of(dow, t))
                    rows.append(rec); break
        # ----- 테이블: 층마다 자리 수의 f 만큼 채움 -----
        for fl in FLOORS:
            cap = sum(seats_of(x) for x in TABLES if (x.get("floor") or "") == fl)
            target = int(cap * f * (1.6 if se.get("stay") != "end" else 1.0))   # 점심 110분은 회전이 있어 더 많이
            filled = 0; tries = 0
            while filled < target and tries < 40:
                tries += 1
                t = random.choice([x for x in sl if x in POPULAR] or sl) if random.random() < 0.6 else random.choice(sl)
                ppl = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 10, 12], [4, 32, 14, 28, 6, 9, 2, 2, 1, 1])[0]
                stay = stay_of(dow, t)
                ids, split = table_fit(date, fl, t, stay, ppl)
                if split and random.random() < 0.6: continue                    # 나눠 앉기는 가끔만
                if random.random() < 0.10 and ids:
                    kw = {"roomId": ids[0], "extraIds": ids[1:], "memo": "테이블 지정" if len(ids) == 1 else "붙여서 앉힘"}   # 특정 테이블 지정(파셜룸 등)
                elif not ids:
                    if random.random() < 0.04 and not any(r.get("_none") for r in rows): kw = {"seatPref": "table:" + fl, "_none": True}; ids = []   # 자리 없음 경고 케이스(하루 1건)
                    else: continue
                else: kw = {"seatPref": "table:" + fl}
                if random.random() < 0.12 and ppl >= 2: kw.update({"menuType": "코스", "courses": make_courses(dow, t, max(1, ppl), "ok")})
                none_case = kw.pop("_none", False)
                rec = base_rec(date, dow, t, ppl, today, **kw)
                if ids and not rec["roomId"]: rec["tentativeRoomId"] = ids[0]; rec["tentativeExtra"] = ids[1:]; rec["tentativeSplit"] = bool(split)
                if none_case: rec["_none"] = True
                if rec["status"] in ("확정", "방문") and ids: mark(date, ids, t, stay)
                rows.append(rec); filled += ppl
        # ----- 룸 미정(room-any) — 가끔 -----
        if random.random() < f * 0.1:
            t = random.choice(sl); ppl = random.choice([4, 5, 6, 6, 7, 8, 12, 2])
            rows.append(base_rec(date, dow, t, ppl, today, seatPref="room-any", request="방으로 부탁드려요 — 어느 방이든"))
    # ----- 시간 경고 케이스: 라스트오더 이후 / 브레이크 안 -----
    h = hours(dow)
    if random.random() < 0.06 and h.get("lo"):
        rows.append(base_rec(date, dow, tm(h["lo"]) + 10, 2, today, seatPref="table:" + FLOORS[0], memo="라스트오더 지나서 받음 — 사장님 확인"))
    if random.random() < 0.04 and h.get("bs"):
        rows.append(base_rec(date, dow, tm(h["bs"]) + 30, 4, today, seatPref="table:" + FLOORS[-1], memo="브레이크타임 중 — 단골"))
    # ----- 유아만 / 유아의자 초과 -----
    if random.random() < 0.04:
        rec = base_rec(date, dow, random.choice(sorted(POPULAR)), 3, today, seatPref="table:" + FLOORS[0], infants=3); rec["chairs"] = 4; rows.append(rec)
    return rows

def to_row(rec):
    rec.pop("_none", None)
    top = {"id", "date", "time", "status", "name", "phone", "people", "roomId", "updatedAt", "deletedAt"}
    data = {k: v for k, v in rec.items() if k not in top}
    return {"id": rec["id"], "store": "hanok", "date": rec["date"], "time": rec["time"], "status": rec["status"], "name": rec["name"],
            "phone": "".join(ch for ch in rec["phone"] if ch.isdigit()), "people": rec["people"], "room_id": rec["roomId"], "data": data,
            "created_at": rec["createdAt"]}

def main():
    clear()
    today = datetime.date.today().strftime("%Y-%m-%d")
    d = datetime.date(2026, 8, 1); end = datetime.date(2026, 10, 31)
    rows = []; profs = {}
    while d <= end:
        ds = d.strftime("%Y-%m-%d"); dow = (d.weekday() + 1) % 7   # JS getDay: 일=0
        if ds in HOLIDAYS: dow = 0                                  # 공휴일 = 일요일 운영시간(앱과 같음)
        prof = "busy" if ds == today else day_profile(d, dow)      # 오늘은 볼 것이 있게
        profs[prof] = profs.get(prof, 0) + 1
        for rec in gen_day(ds, dow, today, prof): rows.append(to_row(rec))
        d += datetime.timedelta(days=1)
    # 같은 날 같은 번호 두 건 (중복 확인 케이스) — 내일
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    dup = [r for r in rows if r["date"] == tomorrow and r["status"] == "확정" and r["phone"]][:1]
    if dup:
        c = json.loads(json.dumps(dup[0])); c["id"] = "res_" + str(uuid.uuid4()); c["time"] = "19:30"; c["data"]["memo"] = "같은 번호로 두 번 예약 — 같은 팀인지 확인"; rows.append(c)
    for i in range(0, len(rows), 200):
        call("/rest/v1/reservations", "POST", rows[i:i+200], token=tok, prefer="return=minimal")
        print("넣음", i + len(rows[i:i+200]), "/", len(rows))
    print("완료: %d 건. 2026-08-01 ~ 2026-10-31 · 날짜 프로필 %s" % (len(rows), profs))

if __name__ == "__main__":
    main()
