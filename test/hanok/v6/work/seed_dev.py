# -*- coding: utf-8 -*-
"""dev DB 에 더미 예약을 넣습니다 (2026-08-01 ~ 2026-10-31). 실서비스(prod)에는 절대 쓰지 않습니다.

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
USED = {}   # date → [(seat_id, start, end)] — 같은 자리에 겹치는 예약을 안 만들려고 (경고 시연용 2% 는 일부러 겹침)
def busy(date, sid, t, stay=150):
    return any(s == sid and a < t + stay and t < b for s, a, b in USED.get(date, []))
def mark(date, ids, t, stay=150):
    USED.setdefault(date, []).extend((sid, t, t + stay) for sid in ids)
def table_combo(date, t, ppl):
    """인원에 맞는 빈 테이블 하나 또는 같은 층 붙임 조합(대표 id, 나머지 id 목록)"""
    one = [x for x in TABLES if (x.get("capacity") or x.get("seats") or 4) >= ppl and (x.get("minCapacity") or 0) <= ppl and not busy(date, x["id"], t)]
    if one: return random.choice(one)["id"], []
    pool = [x for x in TABLES if x.get("joinWith") and not busy(date, x["id"], t)]
    random.shuffle(pool)
    for a in pool:
        combo, total = [a], a.get("seats") or 4
        for b in pool:
            if b is a or b["id"] not in a["joinWith"]: continue
            combo.append(b); total += b.get("seats") or 4
            if total >= ppl: return combo[0]["id"], [c["id"] for c in combo[1:]]
    return None, []
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

def hours(dow):
    d = st["schedules"][0]["days"][dow]
    return d

def tm(s): return int(s[:2]) * 60 + int(s[3:])
def slots(dow):
    """8차: 세션마다 시작~접수 마감 사이 30분 간격 (평일 점심 11:00~14:00, 저녁 17:00~19:30 식)"""
    h = hours(dow); out = []
    bs = tm(h["bs"]) if h.get("bs") else None
    be = tm(h["be"]) if h.get("be") else None
    for se in h.get("sessions", []):
        t = tm(se["from"]); last = tm(se["lastBook"])
        if bs and be and t < bs < last: t = max(t, be) if t >= bs else t   # 저녁 세션이 15:30 부터면 브레이크 뒤부터
        while t <= last:
            if not (bs and be and bs <= t < be): out.append(t)
            t += 30
    return out or [12 * 60]

def hm(m): return "%02d:%02d" % (m // 60, m % 60)

def make(date, dow, today):
    r = {}
    is_past = date < today
    ppl = random.choice([2, 2, 2, 3, 4, 4, 4, 5, 6, 6, 8, 10, 12])
    infants = random.choice([0, 0, 0, 0, 0, 1, 1, 2]) if ppl >= 3 else 0
    sl = slots(dow)
    t = random.choice(sl)
    # 점심/저녁 몰림
    if random.random() < 0.6: t = random.choice([m for m in sl if m in (11*60+30, 12*60, 12*60+30, 13*60, 18*60, 18*60+30, 19*60)] or sl)
    # 경고 케이스 몇 개: 라스트오더 이후 · 브레이크 안
    warn = random.random()
    if warn < 0.02: t = 20 * 60 + 50
    elif warn < 0.035 and hours(dow).get("bs"): t = 16 * 60
    name = pick_name()
    ph = phone()
    if random.random() < 0.18:
        name, ph = random.choice(REPEAT)
    if random.random() < 0.06: ph = ""
    # 좌석: 인원에 맞는 룸 / 홀 / 미배정
    fit = [x for x in ROOMS if x["capacity"] >= ppl and (x.get("minCapacity") or 2) <= max(1, ppl - infants) and not busy(date, x["id"], t)]
    seat_r = random.random()
    room_id = None; seat_pref = None; tent = None; extra = []
    if fit and seat_r < 0.55: room_id = random.choice(fit)["id"]
    elif seat_r < 0.62 and ppl >= 12:
        js = [j for j in JOINS if j["min"] <= ppl <= j["max"] and not any(busy(date, i, t) for i in j["ids"])]   # 룸 합침
        if js: j = random.choice(js); room_id, extra = j["ids"][0], j["ids"][1:]
    elif seat_r < 0.66: room_id, extra = table_combo(date, t, ppl)      # 특정 테이블을 잡은 경우(파셜룸 등) — 드물게
    elif seat_r < 0.88: seat_pref = "table:" + random.choice(FLOORS)      # 8차-H: 보통은 층까지만
    if room_id is None and seat_pref is None:
        seat_pref = random.choice(["room-any", "table:" + random.choice(FLOORS)]) if ppl >= 4 else "table:" + random.choice(FLOORS)
        # tentativeRoomId 는 앱이 로드 때 겹침을 보고 계산합니다(reflowFuture). 여기서 아무 방이나 넣으면 같은 방에 둘이 들어갑니다
    if random.random() < 0.02 and ROOMS: room_id = "r1"; extra = []   # 정원 초과·겹침 경고 시연 (4인 방에 큰 팀)
    if room_id: mark(date, [room_id] + extra, t)
    is_room = room_id is not None and room_id.startswith("r")
    # 식사
    menu = "해당 없음"; courses = {}; undecided = False
    if is_room:
        menu = random.choice(["코스", "코스", "코스", "코스 상당", "확인 필요", "해당 없음"])
        if menu == "코스":
            gid = "cg_dinner" if t >= 17 * 60 else ("cg_welunch" if dow in (0, 6) else "cg_wdlunch")
            g = CG[gid]; adults = max(1, ppl - infants)
            if random.random() < 0.12: undecided = True
            else:
                item = random.choice(g["items"]); courses["%s|%s" % (gid, item)] = adults if random.random() < 0.85 else max(1, adults - 1)
                if random.random() < 0.1:
                    item2 = random.choice([i for i in g["items"] if i != item]); courses["%s|%s" % (gid, item2)] = 1
    elif random.random() < 0.15:
        menu = "코스"; gid = "cg_dinner" if t >= 17 * 60 else ("cg_welunch" if dow in (0, 6) else "cg_wdlunch")
        courses["%s|%s" % (gid, random.choice(CG[gid]["items"]))] = max(1, ppl - infants)
    # 상태
    if is_past: status = random.choices(["방문", "노쇼", "취소"], [86, 5, 9])[0]
    else: status = random.choices(["확정", "취소"], [94, 6])[0]
    created = (datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=random.choice([0, 1, 2, 3, 5, 7, 10, 14, 21]), hours=random.randint(1, 12))).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    changes = [{"on": created[:10], "at": created, "kind": "등록", "items": []}]
    if status in ("취소", "노쇼"):
        at = (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(hours=random.randint(8, 20))).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        changes.append({"on": at[:10], "at": at, "kind": status, "items": []})
    elif random.random() < 0.15:
        at = created[:10] + "T13:00:00.000Z"
        changes.append({"on": at[:10], "at": at, "kind": "변경", "items": [{"n": random.choice(["인원", "시각", "좌석"])}]})
    src = random.choices(st["sources"], ([60, 28, 8, 4] + [2] * 10)[:len(st["sources"])])[0]
    rec = {
        "id": "res_" + str(uuid.uuid4()), "date": date, "time": hm(t), "name": name, "phone": ph,
        "people": ppl, "infants": infants, "chairs": infants if random.random() < 0.7 else 0,
        "roomId": room_id, "extraIds": extra, "seatPref": seat_pref if room_id is None else None, "tentativeRoomId": tent if room_id is None else None, "tentativeExtra": [],
        "source": src, "sourceDetail": random.choice(SRC_DETAIL) if src == "기타" else "",
        "createdAt": created, "menuType": menu, "courses": courses, "courseUndecided": undecided,
        "allergy": random.choice(ALLERGY) if random.random() < 0.12 else "", "allergyChecked": True,
        "request": random.choice(REQUEST) if random.random() < 0.22 else "",
        "memo": random.choice(MEMO) if random.random() < 0.15 else "",
        "status": status, "changes": changes, "sms": [], "demo": True,
    }
    if random.random() < 0.05 and ppl >= 3: rec["infants"] = ppl - 1; rec["chairs"] = 2   # 성인 1명 + 유아 다수 (경고 케이스)
    return rec

def to_row(rec):
    top = {"id", "date", "time", "status", "name", "phone", "people", "roomId", "updatedAt", "deletedAt"}
    data = {k: v for k, v in rec.items() if k not in top}
    return {"id": rec["id"], "store": "hanok", "date": rec["date"], "time": rec["time"], "status": rec["status"], "name": rec["name"],
            "phone": "".join(ch for ch in rec["phone"] if ch.isdigit()), "people": rec["people"], "room_id": rec["roomId"], "data": data,
            "created_at": rec["createdAt"]}

def main():
    clear()
    today = datetime.date(2026, 9, 14).strftime("%Y-%m-%d")
    d = datetime.date(2026, 8, 1); end = datetime.date(2026, 10, 31)
    rows = []
    while d <= end:
        ds = d.strftime("%Y-%m-%d"); dow = (d.weekday() + 1) % 7   # JS getDay: 일=0
        n = random.choice([4, 6, 7, 8, 9, 10, 11, 12]) + (4 if dow in (5, 6) else 0)
        if d > datetime.date(2026, 10, 10): n = max(1, n // 3)   # 먼 미래는 드문드문
        for _ in range(n): rows.append(to_row(make(ds, dow, today)))
        d += datetime.timedelta(days=1)
    # 같은 날 같은 번호 두 건 (중복 확인 케이스)
    dup = [r for r in rows if r["date"] == "2026-09-20"][:1]
    if dup:
        c = json.loads(json.dumps(dup[0])); c["id"] = "res_" + str(uuid.uuid4()); c["time"] = "19:30"; c["data"]["memo"] = "같은 번호로 두 번 예약 — 같은 팀인지 확인"; rows.append(c)
    for i in range(0, len(rows), 200):
        call("/rest/v1/reservations", "POST", rows[i:i+200], token=tok, prefer="return=minimal")
        print("넣음", i + len(rows[i:i+200]), "/", len(rows))
    print("완료:", len(rows), "건. 2026-08-01 ~ 2026-10-31")

if __name__ == "__main__":
    main()
