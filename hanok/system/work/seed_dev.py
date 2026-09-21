# -*- coding: utf-8 -*-
"""dev DB 에 더미 예약을 넣습니다 (2026-08-01 ~ 2026-11-30). 실서비스(prod)에는 절대 쓰지 않습니다.
   10차(2026-09-16): 홈페이지 예약(requests, source 기타·홈페이지 예약) · 사용 중지(하루/기간/시각) · 임시 휴무·임시 운영시간 · 예정 설정(마초 룸) ·
   겹침 강한 경고 · 사용 중지 좌석에 잡힌 예약 · 어제는 확정으로 남김(자동 처리 확인) · 문자 흉내 기록 · 같은 번호 두 건.
   먼저 SQL Editor 에서 표를 비우고(work/seed_dev.py 위 안내 SQL) 돌립니다. 설정(stores.settings)의 blocks·overrides·scheduled 도 이 값으로 덮습니다.
   8차 좌석 모형(룸 8·합침·층 테이블·특정 테이블·나눠 앉기) 기준. 날짜마다 없음/한산/보통/붐빔/포화 프로필을 섞습니다.

  python work/seed_dev.py            넣기 (이미 demo 행이 있으면 먼저 지우고 다시)
  python work/seed_dev.py clear      demo 행만 지우기 (data.demo = true 인 행 — 앱의 '예시 데이터 지우기' 와 같은 기준)

행 모양은 앱의 resToRow 와 같게 만듭니다 (phone 숫자만, people 총원, 나머지 data). data.demo = true 로 표시.
이름은 만화·영화·애니메이션 인물(12차, 재아 09-21 — 연예인 실명 대신) + 가끔 영어 표기 + 작품 속 단체명. 요청·메모·경고 케이스를 섞고, 알러지는 요청사항에 씁니다(칸 없음)."""
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
# 12차(2026-09-21, 재아): 연예인 대신 만화·영화·애니메이션 인물. 화면에서 실명처럼 보이지 않게
KO = ["둘리","도우너","또치","마이콜","희동이","고길동","박영희","신짱구","신짱아","신형만","봉미선","김철수","한유리","맹구","이훈이","나미리",
      "도라에몽","노진구","신이슬","만퉁퉁","왕비실","도라미","아가츠마 젠이츠","카마도 탄지로","카마도 네즈코","하시비라 이노스케","렌고쿠 쿄주로","토미오카 기유",
      "코쵸우 시노부","고죠 사토루","이타도리 유지","후시구로 메구미","쿠기사키 노바라","나나미 켄토","게토 스구루","젠인 마키","토도 아오이",
      "토니 스타크","스티브 로저스","피터 파커","브루스 배너","나타샤 로마노프","토르 오딘슨","완다 막시모프","스티븐 스트레인지","닉 퓨리","티찰라",
      "몽키 D. 루피","롤로노아 조로","나미","상디","우솝","토니토니 쵸파","니코 로빈","우즈마키 나루토","우치하 사스케","하루노 사쿠라","하타케 카카시",
      "손오공","베지터","부르마","크리링","피콜로","에드워드 엘릭","알폰스 엘릭","로이 머스탱","엘사","안나","우디","버즈","미키 마우스","도날드 덕",
      "해리 포터","헤르미온느 그레인저","론 위즐리","덤블도어","프로도 배긴스","간달프","아라곤","레골라스","루크 스카이워커","한 솔로","레아 오르가나","요다",
      "뽀로로","크롱","에디","포비","패티","남도일","유미란","괴도 키드","한지우","이슬","웅이","호빵맨","세균맨","토토로","치히로","하울","소피","키키",
      "기영이","기철이","하니","홍두깨","브루스 웨인","클라크 켄트","다이애나","셜록 홈즈","존 왓슨","잭 스패로우","포레스트 검프","인디아나 존스",
      "마리오","루이지","피치 공주","링크","젤다","김전일","에렌 예거","미카사 아커만","아르민","리바이","고죠 유타","킬루아","곤 프릭스","히소카",
      "몬타나 존스","코난 에도가와","최강창민","아톰","우라라","루피","라이언","어피치","무지","콘","펭수","치이카와","하치와레","우사기"]
FOREIGN = ["Tony Stark","Peter Parker","Bruce Wayne","Hermione Granger","Luke Skywalker","Jack Sparrow","Ellen Ripley","Sarah Connor","John Wick",
           "Forrest Gump","Indiana Jones","James Bond","Sherlock Holmes","Elsa","Woody","Buzz Lightyear","Gojo Satoru","Monkey D. Luffy","Naruto",
           "Son Goku","Doraemon","Totoro","Shrek","Fiona","Homer Simpson","Marge Simpson","SpongeBob","Patrick Star","Groot","Rocket"]
COMPANY = ["스타크 인더스트리 총무팀","쉴드 본부 1팀","호그와트 그리핀도르 동문회","도쿄주술고전 교직원","귀살대 주(柱) 모임","떡잎마을 방범대",
           "해바라기반 학부모회","밀짚모자 해적단","나뭇잎 마을 7반","웨인 엔터프라이즈 인사팀","캡슐 코퍼레이션","고길동 가족","지브리 작화팀",
           "뽀롱뽀롱 숲속마을","몬스터 주식회사 총무과","우주비행사 협회(버즈)","카멜롯 원탁 기사단","셜록 베이커가 221B","엘프 왕국 사절단","크립톤 동문회"]
LONGNAME = ["김수한무거북이와두루미삼천갑자동방삭","몽키 D. 루피 일행 (해적단 전원)","티라노사우르스 렉스 호이"]

# 12차: 알러지 칸을 없앰 — 요청사항에 같이 적음(유아 의자와 같은 방식). 손님이 말한 것 = 요청사항, 직원끼리 보는 것 = 메모
REQUEST = ["송별회 — 조용한 방이면 좋겠어요","상견례 — 조용한 방으로","생일 케이크 반입, 초 준비 부탁","창가 자리","휠체어 손님 1분 — 입구 가까운 자리",
           "회식 — 술 많이 나갑니다","돌잔치 뒤풀이","어르신 생신 — 등받이 있는 의자","촬영 있음 (조용히 부탁드려요)","프로포즈 예정 — 디저트 때 케이크 부탁",
           "단체 계산서 · 카드 나눠 결제","코스 30분 늦게 시작 (늦게 오는 분 있음)","유아용 의자 1개","유아용 의자 2개","갑각류 알러지 1명",
           "땅콩 알러지 (아이)","밀가루 알러지 — 글루텐 주의","조개류 못 드심","견과류 알러지 2명 — 소스 확인","계란 알러지 1명","우유 알러지 (유아)",
           "고수 빼 주세요","매운 거 못 드시는 분 2명","임산부 있음 — 날것 빼고","채식하시는 분 1명 — 고기 빼고 가능한지","5시 반까지는 나가야 해요",
           "주차 발렛 부탁드려요","생일 — 양초 하나만","오래 앉아 있을 예정 — 후식 천천히","룸이면 어디든 괜찮아요","아이 셋 — 시끄러울 수 있어요",
           "탕수육 소스 따로","짜장면 곱빼기 2개 미리","고량주 반입 가능한지","회사 법인카드 — 영수증 필요","반려견 동반 가능한지 (안 되면 괜찮아요)"]
MEMO = ["사장님 지인","단골 — 상석 준비","지난번 노쇼 이력 있음, 전날 확인 전화","비서가 대신 예약함","현금 결제 예정","방송국 — 카메라 들어옴",
        "네이버 리뷰 이벤트 손님","술 취하면 시끄러움 주의","아이 둘, 유아의자 확인","지난번 짜장 소스 짜다고 하심","옆 테이블과 떨어뜨려 주기",
        "전화 안 받음 — 문자로 확인","사장님이 직접 받음","동창회 총무 — 계산은 총무가","이름 확인 필요 (전화로는 '두리' 라 함)","예약금 없음",
        "룸 원했지만 없어서 테이블로 안내함","고량주 반입 문의 — 콜키지 안내함","늘 늦게 옴 (20분쯤)","전에 룸 바꿔 달라 한 적 있음",
        "주차 자리 미리 빼 두기","손님이 사진 찍어 가도 되냐 함 — OK","단골 — 늘 유비 룸 원함","어린이 메뉴 문의함 — 없다고 안내"]
SRC_DETAIL = ["지인 소개","인스타 DM","워크인 재방문","블로그 보고","카카오 채널"]
def pick_request():
    """요청사항 — 하나, 가끔 둘(알러지 + 유아 의자 같은 조합)"""
    a = random.choice(REQUEST)
    if random.random() < 0.25:
        b = random.choice(REQUEST)
        if b != a: return a + ", " + b
    return a

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
def sessions(dow):
    """앱의 sessionsOfDay 와 같은 규칙 — 8차-X 부터 sess{edge, lunch, dinner} 로 저장됩니다(옛 sessions[] 도 받음)"""
    h = hours(dow)
    if "sessions" in h and "sess" not in h: return h["sessions"]
    x = h.get("sess") or {"edge":"15:30","lunch":{"lastBook":"14:00","room":"end","table":"end"},"dinner":{"lastBook":"19:30","room":"end","table":"end"}}
    edge = h.get("bs") or x.get("edge") or ""
    def mk(name, frm, seg, until): return {"name":name, "from":frm, "lastBook":seg["lastBook"], "stay":seg["room"], "stayTable":seg.get("table", seg["room"]), "until":until}
    if not edge: return [mk("종일", h["open"], x["dinner"], h["close"])]
    return [mk("점심", h["open"], x["lunch"], edge), mk("저녁", h.get("be") or edge, x["dinner"], h["close"])]
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
        yesterday = (datetime.datetime.strptime(today, "%Y-%m-%d") - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        if date == yesterday: status = random.choices(["확정", "방문", "취소"], [40, 52, 8])[0]   # 어제 확정 = 아직 방문 처리 안 한 것
        elif is_past: status = random.choices(["방문", "노쇼", "취소"], [86, 5, 9])[0]
        elif date == today: status = random.choices(["확정", "방문", "취소"], [70, 22, 8])[0]
        else: status = random.choices(["확정", "취소"], [94, 6])[0]
    created_days = random.choice([0, 0, 1, 2, 3, 5, 7, 10, 14, 21, 30])
    created_dt = datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=created_days, hours=random.randint(1, 12))
    created_dt = min(created_dt, datetime.datetime.utcnow() - datetime.timedelta(hours=1))   # 접수 시각이 미래가 되지 않게(requests 폭주 방지 트리거가 '최근 10분' 을 셈)
    created = created_dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    changes = [{"on": created[:10], "at": created, "kind": "등록", "items": []}]
    if status in ("취소", "노쇼"):
        when = date if random.random() < 0.6 else (datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=random.randint(1, 3))).strftime("%Y-%m-%d")
        changes.append({"on": when, "at": when + "T%02d:00:00.000Z" % random.randint(1, 12), "kind": status, "items": []})
    elif random.random() < 0.15:
        when = max(created[:10], (datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=random.choice([0, 0, 1]))).strftime("%Y-%m-%d"))
        n = random.choice(["인원", "시간", "좌석"])
        item = {"n": n, "a": "4명", "b": "%d명" % ppl} if n == "인원" else ({"n": n, "a": "오후 6:00", "b": hm(t)} if n == "시간" else {"n": n, "a": "미배정", "b": "룸"})
        changes.append({"on": when, "at": when + "T04:00:00.000Z", "kind": "변경", "items": [item]})
    src = random.choices(st["sources"], ([55, 30, 10, 5] + [2] * 10)[:len(st["sources"])])[0]
    web = (not is_past) and random.random() < 0.10
    if web: src = "기타"
    rec = {
        "id": "res_" + str(uuid.uuid4()), "date": date, "time": hm(t), "name": name, "phone": ph,
        "people": ppl, "infants": infants, "chairs": (infants if random.random() < 0.7 else max(0, infants - 1)) if infants else 0,
        "roomId": kw.get("roomId"), "extraIds": kw.get("extraIds", []),
        "seatPref": kw.get("seatPref") if not kw.get("roomId") else None,
        "tentativeRoomId": None, "tentativeExtra": [], "tentativeSplit": False,
        "source": src, "sourceDetail": "홈페이지 예약" if web else (random.choice(SRC_DETAIL) if src == "기타" else ""),
        "createdAt": created, "menuType": kw.get("menuType", "해당 없음"), "courses": kw.get("courses", {}), "courseUndecided": kw.get("courseUndecided", False),
        "allergy": "", "allergyChecked": True,   # 12차: 알러지 칸 없음 — 요청사항에
        "request": kw.get("request", pick_request() if random.random() < 0.38 else ""),
        "memo": kw.get("memo", random.choice(MEMO) if random.random() < 0.28 else ""),
        "status": status, "changes": changes, "sms": [], "demo": True,
    }
    if is_past and status == "방문" and random.random() < 0.5: rec["auto"] = True
    if ph and status in ("확정", "방문") and random.random() < 0.5:
        rec["sms"].append({"kind": "확정", "at": created, "to": ph, "offset": None, "resent": False, "mock": True,
                           "text": "[한옥반점] %s님, %s %s %d명 예약이 확정되었습니다. 문의 031-724-1004" % (name, date, hm(t), ppl)})
        if date <= today and random.random() < 0.7:
            rec["sms"].append({"kind": "재안내", "at": date + "T00:00:00.000Z", "to": ph, "offset": 1, "resent": False, "mock": True,
                               "text": "[한옥반점] %s님, 내일 %s %d명 예약 안내드립니다. 변경은 031-724-1004" % (name, hm(t), ppl)})
    if web: rec["_web"] = True
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
    # 11차(2026-09-19, 재아 "너무 과하고 오예약이 많다"): 현실적으로 — 평일은 한산~보통, 주말 보통~붐빔, 포화는 드물게
    if dow in (0, 6):  weights = [4, 22, 46, 24, 4]
    elif dow == 1:     weights = [18, 50, 27, 5, 0]      # 월요일 한산
    else:              weights = [12, 44, 36, 8, 0]
    if d > datetime.date(2026, 10, 12): weights = [35, 45, 18, 2, 0]   # 먼 미래는 드문드문
    if d > datetime.date(2026, 11, 5): weights = [65, 30, 5, 0, 0]
    return random.choices(["none", "quiet", "normal", "busy", "full"], weights)[0]

def gen_day(date, dow, today, prof):
    rows = []
    if prof == "none": return rows
    frac = {"quiet": 0.18, "normal": 0.38, "busy": 0.62, "full": 0.85}[prof]
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
                if r < 0.006: ppl = hi + random.randint(1, 2)                 # 정원 초과 경고(드물게)
                elif r < 0.012: ppl = max(1, lo - random.randint(1, 2))      # 최소 인원 미달 경고(드물게)
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
                    if random.random() < 0.01 and not any(r.get("_none") for r in rows): kw = {"seatPref": "table:" + fl, "_none": True}; ids = []   # 자리 없음 경고 케이스(아주 드물게)
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
    if random.random() < 0.012 and h.get("lo"):
        rows.append(base_rec(date, dow, tm(h["lo"]) + 10, 2, today, seatPref="table:" + FLOORS[0], memo="라스트오더 지나서 받음 — 사장님 확인"))
    if random.random() < 0.008 and h.get("bs"):
        rows.append(base_rec(date, dow, tm(h["bs"]) + 30, 4, today, seatPref="table:" + FLOORS[-1], memo="브레이크타임 중 — 단골"))
    # ----- 유아만 / 유아의자 초과 -----
    if False:   # 11차: 유아의자 기능을 뺐으니(09-17) 어린이만 온 팀 케이스는 안 넣음
        rec = base_rec(date, dow, random.choice(sorted(POPULAR)), 3, today, seatPref="table:" + FLOORS[0], infants=3); rec["chairs"] = 4; rows.append(rec)
    return rows

def to_row(rec):
    rec.pop("_none", None); rec.pop("_web", None)
    top = {"id", "date", "time", "status", "name", "phone", "people", "roomId", "updatedAt", "deletedAt"}
    data = {k: v for k, v in rec.items() if k not in top}
    return {"id": rec["id"], "store": "hanok", "date": rec["date"], "time": rec["time"], "status": rec["status"], "name": rec["name"],
            "phone": "".join(ch for ch in rec["phone"] if ch.isdigit()), "people": rec["people"], "room_id": rec["roomId"], "data": data,
            "created_at": rec["createdAt"]}

def main():
    clear()
    today = datetime.date.today().strftime("%Y-%m-%d")
    d = datetime.date(2026, 8, 1); end = datetime.date(2026, 11, 30)
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
    T = datetime.date.today()
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
    # 3) 전화 없음 + 단체 12명 룸 합침(동탁) + 알러지(요청사항에)
    big = base_rec(D(2), dow_of(D(2)), 18*60, 12, today, roomId=r_by_name["동탁"]["id"], status="확정", menuType="코스", courses=make_courses(dow_of(D(2)), 18*60, 12, "ok"), request="단체 계산서 · 상석 준비, 갑각류 알러지 2명"); big["phone"] = ""; big["name"] = "스타크 인더스트리 총무팀"; add(big)
    # 4) 노쇼 이력 번호로 미래 확정 (REPEAT 첫 사람을 노쇼로 만들고 미래 예약)
    nsn, nsp = REPEAT[0]
    add(base_rec(D(-5), dow_of(D(-5)), 19*60, 3, today, seatPref="table:" + FLOORS[0], status="노쇼"))
    ns2 = base_rec(D(-12), dow_of(D(-12)), 12*60, 2, today, seatPref="table:" + FLOORS[0], status="노쇼"); ns2["name"] = nsn; ns2["phone"] = nsp; add(ns2)
    ns3 = base_rec(D(3), dow_of(D(3)), 19*60, 4, today, seatPref="room-any", status="확정", menuType="확인 필요"); ns3["name"] = nsn; ns3["phone"] = nsp; ns3["memo"] = "노쇼 이력 — 전날 확인 전화"; add(ns3)
    # 5) 지난 날짜에 아직 확정(방문 처리 안 됨) — 그저께
    add(base_rec(D(-2), dow_of(D(-2)), 13*60, 2, today, seatPref="table:" + FLOORS[1], status="확정", memo="방문 처리 빠뜨림"))
    # 6) 예정 설정(마초 룸, D+7 부터)이 생기기 전 날짜에 마초를 잡은 예약은 없음. 대신 D+8 에 마초 지정 예약(예정 좌석)
    yeopo_id = "r_yeopo"
    add(base_rec(D(8), dow_of(D(8)), 18*60, 6, today, roomId=yeopo_id, status="확정", menuType="코스", courses=make_courses(dow_of(D(8)), 18*60, 6, "ok"), memo="마초 룸(예정 설정) 첫 손님"))
    # 7~10) 휴무일 예약·정원 초과/미달·어린이만·라스트오더/브레이크 케이스는 11차에서 뺐음(현실적으로, 재아). 무작위로 아주 드물게만 섞임
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

    seed_reqs_and_settings(rows, today, T, D, r_by_name, yeopo_id, nsn, nsp)

# ----- 손님 메모(customers) — 단골 몇 명에게 사장님이 적어 둔 메모. 감사 문자 AI 가 '손님 메모' 로 참고함 -----
CUST_MEMO = ["사장님 대학 후배 — 늘 유비 룸","탕수육 소스 부먹 싫어하심","3월 생신 — 지난해 미역국 챙겨 드림","아이가 땅콩 알러지 — 주방에 꼭",
             "회사 접대 자주 — 영수증 회사명으로","조용한 자리 원하심, 창가","고량주 좋아하심 — 재고 확인"]
def seed_customers():
    rows = []
    for (name, ph), memo in zip(REPEAT[:len(CUST_MEMO)], CUST_MEMO):
        digits = "".join(ch for ch in ph if ch.isdigit())
        if digits: rows.append({"store": "hanok", "phone": digits, "name": "", "memo": memo, "by": "admin"})
    if rows: call("/rest/v1/customers?on_conflict=store,phone", "POST", rows, token=tok, prefer="resolution=merge-duplicates,return=minimal")
    print("손님 메모: %d 명" % len(rows))

def seed_reqs_and_settings(rows, today, T, D, r_by_name, yeopo_id, nsn, nsp):
    now = datetime.datetime.utcnow()
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
    seen_ph = set()
    for r in web_rows:
        if r["phone"] in seen_ph: continue   # 폭주 방지 트리거(같은 번호 하루 3건)에 걸리지 않게 번호당 하나
        seen_ph.add(r["phone"]); req("rq_" + r["id"][4:12], r, "확정", res_id=r["id"])
    def pending(rid, date, time, adults, kids, seat, course, label, name, phone, request, hours_left=20):
        reqs.append({"id": rid, "store": "hanok", "date": date, "time": time, "adults": adults, "kids": kids, "people": adults + kids, "seat": seat, "course": course, "course_label": label,
                     "name": name, "phone": phone, "request": request, "status": "대기", "reason": "", "res_id": None,
                     "created_at": (now - datetime.timedelta(hours=24 - hours_left)).strftime("%Y-%m-%dT%H:%M:%SZ"), "expires_at": (now + datetime.timedelta(hours=hours_left)).strftime("%Y-%m-%dT%H:%M:%SZ")})
    pending("rq_p1", D(2), "12:00", 6, 1, "room", "set:요리사 추천세트", "요리사 추천세트", "신형만", "01055551111", "아이 의자 하나 부탁드립니다. 아이가 땅콩 알러지 있어요", 21)   # 12차: 알러지는 요청사항에
    pending("rq_p2", D(3), "18:30", 2, 0, "table", "none", "", "헤르미온느 그레인저", "01055552222", "", 15)
    pending("rq_p3", D(1), "18:00", 5, 0, "room", "later", "미정", "토니 스타크", "01055553333", "룸이면 어디든 괜찮아요", 9)          # 내일 18:00 룸 — 조조 겹침 날이라 자리 없음 경고 가능
    # rq_p4(노쇼 이력 번호)·rq_p5(40분 남음)는 11차에서 뺐음 — 대기 3건이면 충분
    reqs.append({"id": "rq_rej1", "store": "hanok", "date": D(4), "time": "19:00", "adults": 3, "kids": 0, "people": 3, "seat": "room", "course": "later", "course_label": "미정",
                 "name": "고길동", "phone": "01055556666", "request": "", "status": "거절", "reason": "룸은 성인 5명부터 받고 있습니다", "res_id": None,
                 "created_at": (now - datetime.timedelta(hours=30)).strftime("%Y-%m-%dT%H:%M:%SZ"), "expires_at": (now - datetime.timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")})
    reqs.append({"id": "rq_exp1", "store": "hanok", "date": D(5), "time": "12:00", "adults": 2, "kids": 0, "people": 2, "seat": "table", "course": "none", "course_label": "",
                 "name": "도라에몽", "phone": "01055557777", "request": "", "status": "만료", "reason": "24시간 안에 처리되지 않음", "res_id": None,
                 "created_at": (now - datetime.timedelta(hours=40)).strftime("%Y-%m-%dT%H:%M:%SZ"), "expires_at": (now - datetime.timedelta(hours=16)).strftime("%Y-%m-%dT%H:%M:%SZ")})
    for x in reqs: x.setdefault("allergy", "")   # 한 번에 넣을 때 키가 전부 같아야 함(PGRST102)
    for i in range(0, len(reqs), 200):
        call("/rest/v1/requests?on_conflict=id", "POST", reqs[i:i+200], token=tok, prefer="resolution=merge-duplicates,return=minimal")   # 같은 id 는 덮어씀(다시 돌릴 때)
    print("홈페이지 예약: %d 건 (대기 3 · 거절 1 · 만료 1 · 확정 %d)" % (len(reqs), len(web_rows)))
    seed_customers()

    # ----- 설정: 사용 중지 · 임시 휴무/운영시간 · 예정 설정(마초) -----
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
    # 예정 설정: D+7 부터 저층에 '마초' 룸(4~8) 추가 — 이름은 기존 테이블 '여포' 와 겹치지 않게
    rooms_after = json.loads(json.dumps(st["rooms"]))
    if not any(r["id"] == yeopo_id for r in rooms_after):
        rooms_after.append({"id": yeopo_id, "name": "마초", "type": "room", "floor": "저층", "minCapacity": 4, "minWeekend": 4, "optCapacity": 6, "capacity": 8, "blocks": []})
    st["scheduled"] = [x for x in st.get("scheduled", []) if not x.get("demo")] + [
        {"id": "sc_demo_seats", "from": D(7), "to": None, "group": "seats", "values": {"rooms": rooms_after, "joins": st.get("joins", [])}, "note": "저층 마초 룸 추가", "createdAt": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "by": "staff", "demo": True}]
    call("/rest/v1/stores?key=eq.hanok", "PATCH", {"settings": st}, token=tok, prefer="return=minimal")
    print("설정: 사용 중지 4(하루·기간·시각·무기한) · 임시 휴무 1 · 임시 운영시간 1 · 예정 설정 1(마초, %s 부터)" % D(7))

if __name__ == "__main__":
    if "reqs" in sys.argv[1:]:
        # 예약은 그대로 두고 홈페이지 예약·설정만 다시
        T = datetime.date.today(); today = T.strftime("%Y-%m-%d")
        def D(n): return (T + datetime.timedelta(days=n)).strftime("%Y-%m-%d")
        import urllib.parse
        rows = call("/rest/v1/reservations?data->>sourceDetail=eq." + urllib.parse.quote("홈페이지 예약") + "&deleted_at=is.null&select=*", token=tok)
        r_by_name = {r["name"]: r for r in ROOMS}
        nsn, nsp = REPEAT[0]
        seed_reqs_and_settings(rows, today, T, D, r_by_name, "r_yeopo", nsn, nsp)
    else:
        main()
