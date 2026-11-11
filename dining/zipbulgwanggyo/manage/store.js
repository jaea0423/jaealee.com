/* 짚불태백 광교점 시안 — 예약·웨이팅·선결제 장부·포인트·기록 자료 한 곳 (window.ZB).
   손님 홈페이지의 예약 창(../js/reserve.js), 입구 웨이팅(../waiting/), 계산대(../points/), 매장 TV(../tv/), 매장 화면(app.js)이 이 파일 하나를 같이 씁니다.

   ★ 한옥반점과 다른 점: 자리를 '어느 테이블' 로 배정하지 않습니다. 테이블 '개수' 만 셉니다.
     · 예약 하나가 쓰는 테이블 수 = 인원 ÷ 한 테이블 좌석(올림)
     · 예약은 평균 이용 시간(점심 dwellLunch · 저녁 dwellDinner) 동안 그 개수를 차지합니다
     · 홈페이지로는 onlineTables 개까지만 받고, 나머지는 워크인·전화용으로 남깁니다

   ★ 11-11 개선: 확인표 답 = 설정값. 사장님 답이 오면 매장 화면 '설정' 에서 값만 바꾸면 되게 규칙을 모두 cfg 로 뺐습니다.
     기록(log): 예약·웨이팅·장부·포인트·설정이 바뀔 때마다 '언제·어느 기기·무엇' 을 한 줄씩 남깁니다(지우지 않음).

   시안이라 서버가 없습니다. 자료는 이 브라우저(localStorage)에만 있고, 날짜가 바뀌면 예시를 새로 만듭니다. */
(function(){
  const KEY = "zb-demo-v4";   /* v4(11-11): 기록·포인트 유효기간·설정 칸이 늘어 예시를 새로 만듦 */
  const pad = n => String(n).padStart(2, "0");
  const ymd = d => d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  const addDays = (s, n) => { const d = new Date(s + "T00:00:00"); d.setDate(d.getDate() + n); return ymd(d); };
  const mins = t => Number(t.slice(0, 2)) * 60 + Number(t.slice(3));
  const hhmm = m => pad(Math.floor(m / 60)) + ":" + pad(m % 60);
  const today = () => ymd(new Date());
  const dayStart = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d.getTime(); };
  const DAY = 86400000;

  /* 기본값 = 확인표에서 우리가 먼저 제안한 값(사장님 답이 오면 설정에서 바꿈) */
  const DEFAULT_CFG = {
    /* 예약 */
    tables: 20,            /* 매장 전체 테이블 수 */
    onlineTables: 12,      /* 그중 홈페이지 예약으로 받을 수 */
    seats: 4,              /* 한 테이블 좌석 */
    dwellLunch: 90,        /* 한 팀 평균 이용 시간(분) — 점심. 제한이 아니라 예약을 잡기 위한 평균 */
    dwellDinner: 120,      /* 저녁(술을 곁들여 더 김) */
    maxDays: 60,           /* 홈페이지 예약: 며칠 앞까지 */
    groupConfirm: 7,       /* 이 인원 이상 홈페이지 예약은 사장님 확인 후 확정, 그 아래는 바로 확정 */
    lateMin: 15,           /* 예약 손님이 늦을 때 자리를 잡아 두는 시간(분) */
    noshowLimit: 2,        /* 노쇼가 이 횟수가 되면 홈페이지 예약을 막고 전화로 안내 */
    slots: ["11:30","12:00","12:30","13:00","13:30","14:00","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30"],   /* ../js/reserve.js 의 시간표와 같게 */
    /* 웨이팅 */
    waitMin: 8,            /* 기록이 모자랄 때 쓰는 '한 팀이 빠지는 시간(분)' 기본값 — 기록이 쌓이면 실제 입장 간격으로 계산 */
    callWaitMin: 10,       /* 호출 후 이 시간이 지나면 '넘기기' 를 권함 */
    bigTeam: 7,            /* 이 인원 이상은 입구 기기에서 웨이팅을 받지 않고 직원·예약으로 안내 */
    lastOrder: "21:00",    /* 라스트오더 */
    waitCloseBefore: 30,   /* 라스트오더 몇 분 전에 웨이팅 접수를 닫을지 */
    /* 장부 */
    lowBalance: 100000,    /* 잔액이 이 아래로 내려가면 '충전 안내' */
    ledgerCredit: 0,       /* 마이너스 허용 한도(원). 0 = 마이너스 안 됨(그래도 막지 않고 경고만) */
    /* 포인트 */
    pointRate: 5,          /* 결제 금액의 몇 % 를 쌓을지 */
    pointMin: 5000,        /* 이만큼 모여야 쓸 수 있음 (1포인트 = 1원) */
    pointExpireDays: 365,  /* 유효기간(일). 쌓인 포인트는 가게의 부채라 기간을 둠 */
    pointNextDay: true,    /* 적립한 포인트는 다음 날부터 사용(그날 밤 마감에서 실수를 바로잡게) */
    pointAuth: "name"      /* 사용할 때 본인 확인: name 이름+번호 / code 휴대폰 인증번호 */
  };
  const ACTIVE = { req: 1, ok: 1, in: 1 };   /* 테이블을 차지하는 상태: 신청(확정 전에도 자리를 잡아 둠) · 확정 · 방문 */

  let db = null, device = "매장 화면";
  function load(){
    try{ db = JSON.parse(localStorage.getItem(KEY) || "null"); }catch(e){ db = null; }
    if(!db || db.seeded !== today()) db = seed((db && db.cfg) || null);   /* 하루 지난 예시는 날짜가 안 맞아 새로 */
    /* 설정 칸이 새로 생겨도 저장된 값은 두고 빠진 칸만 기본값으로 */
    const before = JSON.stringify(db.cfg);
    db.cfg = Object.assign({}, DEFAULT_CFG, db.cfg);
    if(!db.log) db.log = [];
    if(JSON.stringify(db.cfg) !== before) save();
    return db;
  }
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(db)); }catch(e){} }

  /* ---------- 기록 ----------
     kind: res 예약 · wait 웨이팅 · ledger 장부 · point 포인트 · cfg 설정. by = 어느 기기·화면에서. 지우지 않고 더하기만. */
  function log(kind, text, at, by){
    db.log.push({ id: "g" + (db.log.length + 1) + "_" + Date.now().toString(36), at: at || Date.now(), kind: kind, text: text, by: by || device });
    if(db.log.length > 800) db.log.splice(0, db.log.length - 800);
  }

  const dwellFor = t => mins(t) < 15 * 60 ? db.cfg.dwellLunch : db.cfg.dwellDinner;
  const tablesFor = (people, cfg) => Math.max(1, Math.ceil(people / (cfg || db.cfg).seats));
  /* 그 시각에 차 있는 테이블 수 */
  function usedAt(date, m, skipId, list){
    return (list || db.res).reduce((n, r) => {
      if(r.date !== date || !ACTIVE[r.status] || r.id === skipId) return n;
      const s = mins(r.time);
      return (s <= m && m < s + dwellFor(r.time)) ? n + tablesFor(r.people) : n;
    }, 0);
  }
  /* 그 시각에 시작하는 예약이 이용 시간 내내 들어갈 수 있나. online 이면 홈페이지 한도로 */
  function fits(date, time, people, online, skipId, list){
    const limit = online ? db.cfg.onlineTables : db.cfg.tables, need = tablesFor(people), s = mins(time);
    for(let m = s; m < s + dwellFor(time); m += 30){ if(usedAt(date, m, skipId, list) + need > limit) return false; }
    return true;
  }
  /* 그 시각에 시작하면 남는 테이블 수(이용 시간 중 가장 빡빡한 때 기준) */
  function leftAt(date, time, online){
    const limit = online ? db.cfg.onlineTables : db.cfg.tables, s = mins(time); let peak = 0;
    for(let m = s; m < s + dwellFor(time); m += 30) peak = Math.max(peak, usedAt(date, m));
    return limit - peak;
  }
  const digits = s => String(s || "").replace(/\D/g, "");
  /* 이 번호의 노쇼 횟수 — 홈페이지 예약 제한에 씀 */
  const noshowCount = phone => { const d = digits(phone); return d ? db.res.filter(r => r.status === "noshow" && digits(r.phone) === d).length : 0; };

  /* ---------- 예시 자료 ---------- */
  function seed(keepCfg){
    const cfg = Object.assign({}, DEFAULT_CFG, keepCfg || {});
    const out = { cfg: cfg, res: [], seeded: today(), log: [] };
    db = out;
    let x = 20261110;   /* 늘 같은 예시가 나오게 정해진 씨앗 */
    const rnd = () => { x = (x * 1103515245 + 12345) & 0x7fffffff; return x / 0x7fffffff; };
    const pick = a => a[Math.floor(rnd() * a.length)];
    const FAM = ["김","이","박","최","정","강","조","윤","장","임","한","오","서","신","권"];
    const GIV = ["민수","서연","지훈","하은","도윤","수빈","예준","지우","현우","유진","성민","은지","준호","다은","태현"];
    const MEMO = ["", "", "", "", "유아용 의자 1개", "생일 모임", "회사 회식", "창가 자리 희망", "조용한 자리 부탁드려요", "주차 2대"];
    const LUNCH = ["11:30","12:00","12:00","12:30","13:00"], DINNER = ["17:30","18:00","18:00","18:30","18:30","19:00","19:00","19:30","20:00"];
    const now = new Date(), nowM = now.getHours() * 60 + now.getMinutes(), td = today();
    let seq = 0;
    for(let i = -1; i <= 13; i++){
      const date = addDays(td, i), wd = new Date(date + "T00:00:00").getDay(), busy = wd === 5 || wd === 6 || wd === 0;
      const n = (busy ? 17 : 10) + Math.floor(rnd() * 4);   /* 저녁 피크에 한도 가까이 차는 모습이 보이게 넉넉히(안 들어가는 건 아래에서 버림) */
      for(let k = 0; k < n; k++){
        const time = rnd() < 0.28 ? pick(LUNCH) : pick(DINNER);
        const people = rnd() < 0.12 ? 8 + Math.floor(rnd() * 5) : 2 + Math.floor(rnd() * 5);
        if(!fits(date, time, people, false)) continue;   /* 예시도 수용량을 넘기지 않게 */
        const past = i < 0 || (i === 0 && mins(time) + 20 < nowM);
        const src = rnd() < 0.45 ? "홈페이지" : (rnd() < 0.8 ? "전화" : "방문");
        let status = past ? (rnd() < 0.08 ? "noshow" : "in") : "ok";
        if(!past && src === "홈페이지" && people >= cfg.groupConfirm && i <= 5) status = "req";   /* 단체 홈페이지 신청은 사장님 확인 대기 */
        if(!past && rnd() < 0.05) status = "cancel";
        out.res.push({ id: "ex_" + (++seq), date: date, time: time, people: people,
          name: pick(FAM) + pick(GIV), phone: "010-" + (2000 + Math.floor(rnd() * 8000)) + "-" + pad(Math.floor(rnd() * 100)) + pad(Math.floor(rnd() * 100)),
          memo: pick(MEMO), pre: "", status: status, src: src, at: Date.now() - Math.floor(rnd() * 5e8) });
      }
    }
    /* 방금 시간이 지났는데 아직 안 온 확정 예약 하나 — '늦음' 표시 예시 */
    const lateM = Math.floor((nowM - 8) / 30) * 30, lateT = hhmm(lateM);
    if(cfg.slots.indexOf(lateT) >= 0 && nowM - lateM >= 5) out.res.push({ id: "ex_late", date: td, time: lateT, people: 3, name: "한지민", phone: "010-6631-2048", memo: "", pre: "", status: "ok", src: "전화", at: Date.now() - 2 * DAY });
    /* 노쇼 제한 예시 — 같은 번호로 노쇼 두 번(이 번호로 홈페이지 예약을 하면 전화로 안내됨) */
    [-9, -23].forEach((d, k) => out.res.push({ id: "ex_ns" + k, date: addDays(td, d), time: "19:00", people: 4, name: "오현우", phone: "010-5172-0490", memo: "", pre: "", status: "noshow", src: "홈페이지", at: Date.now() - (30 - d) * DAY }));
    out.wait = seedWait();
    out.ledger = seedLedger();
    out.points = seedPoints(cfg);
    seedLog(out);
    save();
    return out;
  }

  /* ---------- 웨이팅 ----------
     예약과 달리 '오늘, 지금' 만 있습니다. 번호표 한 줄 = { no 대기번호, people, phone, at 접수, callAt 호출, doneAt 끝, status, first 예약 손님 우선 }.
     status: wait 대기 → call 호출 → in 입장 / gone 미방문 / cancel 취소. 입장 시각(doneAt)이 쌓여 예상 대기 계산에 쓰입니다. */
  const LIVE = { wait: 1, call: 1 };
  function seedWait(){
    const now = Date.now(), M = 60000, list = []; let no = 0;
    const mk = (ago, people, status, src, dur) => {
      const r = { id: "w_ex" + (++no), no: no, people: people, phone: "010-" + String(3100 + no * 617).slice(-4) + "-" + String(1000 + no * 137).slice(-4), src: src || "입구 접수", status: status, at: now - ago * M };
      if(status === "call") r.callAt = now - 3 * M;
      else if(!LIVE[status]) { r.callAt = r.at + (dur || 20) * M - 2 * M; r.doneAt = r.at + (dur || 20) * M; }
      list.push(r);
    };
    /* 입장 간격이 9분쯤 되게 — 예상 대기가 '최근 입장 기준' 으로 계산되는 모습 */
    mk(121, 2, "in", 0, 21); mk(110, 4, "in", 0, 19); mk(104, 3, "gone", 0, 22); mk(103, 6, "in", 0, 21); mk(96, 2, "in", 0, 23); mk(88, 4, "cancel", 0, 9);
    mk(86, 5, "in", "직접 등록", 22); mk(76, 2, "in", 0, 21); mk(66, 4, "in", 0, 20);
    mk(36, 4, "call"); mk(28, 2, "wait"); mk(21, 6, "wait"); mk(13, 3, "wait", "직접 등록"); mk(6, 4, "wait");
    return { on: true, seq: no, list: list };
  }
  const waitLive = () => db.wait.list.filter(x => LIVE[x.status]).sort((a, b) => (b.first ? 1 : 0) - (a.first ? 1 : 0) || a.no - b.no);
  /* 한 팀이 빠지는 시간 — 오늘 입장 기록의 간격(중앙값). 기록이 3개 안 되면 설정의 기본값 */
  function waitPace(){
    const ins = db.wait.list.filter(x => x.status === "in" && x.doneAt && x.doneAt > Date.now() - 3 * 3600000).map(x => x.doneAt).sort((a, b) => a - b);
    const gaps = []; for(let i = 1; i < ins.length; i++) gaps.push((ins[i] - ins[i - 1]) / 60000);
    if(gaps.length < 3) return { per: db.cfg.waitMin, basis: "기본값" };
    gaps.sort((a, b) => a - b);
    const med = gaps[Math.floor(gaps.length / 2)];
    return { per: Math.max(3, Math.min(30, Math.round(med))), basis: "최근 입장 " + ins.length + "팀 기준" };
  }
  /* 앞에 n팀일 때 예상 대기(분) 범위 */
  function waitRange(ahead){
    if(ahead <= 0) return null;
    const p = waitPace().per, mid = ahead * p;
    return { lo: Math.max(1, Math.round(mid * 0.8 / 5) * 5 || 5), hi: Math.max(5, Math.round(mid * 1.25 / 5) * 5) };
  }
  /* 접수 마감 시각(라스트오더 − n분)과 지금 마감인지 */
  function waitClose(){
    const m = mins(db.cfg.lastOrder) - db.cfg.waitCloseBefore, d = new Date(), now = d.getHours() * 60 + d.getMinutes();
    return { at: hhmm(m), closed: now >= m };
  }

  /* ---------- 선결제 장부 ----------
     장부 한 권 = acct { name, kind 회사/개인, contact 담당자, phone, memo }
     기록 한 줄 = tx { acct, type charge 충전 / use 사용, amount, memo, by 쓴 사람, at, void 취소 여부 }
     ★ 잔액은 기록을 더해 계산 — 잘못 넣은 줄은 지우지 않고 '취소' 로 남김.
     잔액보다 많이 써도 막지 않습니다. 마이너스 한도(ledgerCredit)를 넘으면 경고만. */
  function seedLedger(){
    const now = Date.now(), accts = [], tx = []; let n = 0;
    const A = (name, kind, contact, phone, memo) => { const a = { id: "a" + (accts.length + 1), name: name, kind: kind, contact: contact, phone: phone, memo: memo || "" }; accts.push(a); return a; };
    const T = (a, type, amount, daysAgo, memo, by, isVoid) => { const t = { id: "t" + (++n), acct: a.id, type: type, amount: amount, memo: memo || "", by: by || "", at: now - daysAgo * DAY - (n % 5) * 3600000 }; if(isVoid) t.void = true; tx.push(t); };
    let a = A("광교테크 총무팀", "회사", "박 과장", "010-4821-1201", "회식 때 차감. 영수증은 담당자 메일로");
    T(a, "charge", 1000000, 80, "계좌이체"); T(a, "use", 186000, 74, "팀 회식 8명", "박 과장"); T(a, "use", 243000, 51, "송년회 1차 11명", "박 과장");
    T(a, "use", 158000, 30, "6명", "김 대리"); T(a, "use", 64000, 9, "금액 잘못 입력", "", true); T(a, "use", 212000, 9, "부서 회식 9명", "박 과장");
    a = A("광교 미소치과", "회사", "김 원장", "010-9356-1302", "직원 점심 · 저녁");
    T(a, "charge", 500000, 60, "카드"); T(a, "use", 98000, 45, "점심 5명", "김 원장"); T(a, "use", 132000, 20, "저녁 4명", "실장"); T(a, "use", 76000, 3, "점심 특선 4명", "실장");
    a = A("한빛세무회계", "회사", "이 실장", "010-2287-1403", "");
    T(a, "charge", 300000, 40, "계좌이체"); T(a, "use", 87000, 33, "4명", "이 실장"); T(a, "use", 64000, 12, "3명", "이 실장"); T(a, "use", 95000, 2, "5명", "대표");
    a = A("김민수 님", "개인", "", "010-7140-1504", "단골 · 생갈비 미리 준비");
    T(a, "charge", 200000, 25, "현금"); T(a, "use", 46000, 18, "2명"); T(a, "use", 52000, 6, "가족 3명");
    a = A("한결화재 광교지점", "회사", "최 팀장", "010-5512-1605", "분기마다 충전");
    T(a, "charge", 1000000, 20, "계좌이체"); T(a, "use", 312000, 14, "지점 회식 14명", "최 팀장"); T(a, "use", 268000, 0.2, "지점 회식 12명", "최 팀장");
    a = A("이서연 님", "개인", "", "010-3368-1706", "");
    T(a, "charge", 100000, 50, "카드"); T(a, "use", 58000, 41, "3명"); T(a, "use", 49000, 22, "2명");
    a = A("광교중앙 상인회", "회사", "정 총무", "010-8823-1807", "월례회 셋째 주 화요일");
    T(a, "charge", 500000, 70, "계좌이체"); T(a, "use", 162000, 60, "월례회"); T(a, "use", 145000, 38, "월례회"); T(a, "use", 193000, 16, "월례회 + 추가 주문");
    a = A("정도윤 님", "개인", "", "010-6604-1908", "");
    T(a, "charge", 300000, 5, "카드");
    return { seq: n, accts: accts, tx: tx };
  }

  /* ---------- 포인트 ----------
     계산할 때 '결제 금액 + 손님 휴대폰 번호' 로 그 % 만큼 쌓입니다. 처음 보는 번호면 그 자리에서 회원(이름·별명을 받아 둠 — 쓸 때 확인용).
     회원 = member { phone, name }, 기록 = tx { mem, type earn 적립 / use 사용, pts, amount 결제 금액, at, src 들어온 방식, void }
     ★ 잔액은 기록으로 계산. 적립 한 건 = 덩어리(lot) 하나, 유효기간이 지나면 사라지고, 쓸 때는 오래된 덩어리부터 씀.
     ★ 적립한 날에는 못 쓰고 다음 날부터(pointNextDay) — 그날 밤 마감에서 실수를 바로잡을 수 있게. */
  function seedPoints(cfg){
    let x = 4242; const rnd = () => { x = (x * 1103515245 + 12345) & 0x7fffffff; return x / 0x7fffffff; };
    const now = Date.now(), rate = cfg.pointRate, members = [], tx = []; let n = 0;
    const NAMES = ["김민수", "박", "이하은", "최도윤", "정", "강예준", "윤서아", "임", "한지민", "오", "서준우", "신", "권하린", "조", "장민재", "황"];
    const E = (m, amount, at, src) => { tx.push({ id: "p" + (++n), mem: m.id, type: "earn", pts: Math.floor(amount * rate / 100), amount: amount, at: at, src: src || "계산대" }); };
    for(let i = 0; i < 16; i++){
      const m = { id: "m" + (i + 1), phone: "010-" + String(2400 + i * 389).slice(-4) + "-" + String(2101 + i * 173).slice(-4), name: NAMES[i] };
      members.push(m);
      const days = []; const v = 1 + Math.floor(rnd() * 6);
      for(let k = 0; k < v; k++) days.push(1 + Math.floor(rnd() * 420));   /* 1년 넘은 적립도 섞어 유효기간이 보이게 */
      days.sort((a, b) => b - a);
      let bal = 0;
      days.forEach(d => {
        const at = now - d * DAY - (12 + Math.floor(rnd() * 9)) * 3600000 + 6 * 3600000, amount = (40 + Math.floor(rnd() * 200)) * 1000;
        if(bal >= 5000 && d < 360 && rnd() < 0.35){ const use = Math.floor(bal / 1000) * 1000; tx.push({ id: "p" + (++n), mem: m.id, type: "use", pts: use, amount: amount, at: at - 60000 }); bal -= use; }
        E(m, amount, at, rnd() < 0.7 ? "계산대" : "직원 입력"); bal += Math.floor(amount * rate / 100);
      });
    }
    /* 오늘 적립 — 마감 정산 예시(같은 번호 두 번 · 큰 금액 하나가 걸러지게) */
    const t0 = dayStart(), h = hr => Math.min(now - 60000, t0 + hr * 3600000);
    E(members[2], 86000, h(12.4)); E(members[5], 64000, h(13.1), "직원 입력"); E(members[2], 52000, h(13.3)); E(members[8], 486000, h(14.0), "직원 입력");
    E(members[11], 118000, h(15.2));
    return { seq: n, members: members, tx: tx };
  }
  /* 포인트 상태 — 덩어리 계산. at 기준 시각(기본 지금) */
  function pstate(memId){
    const c = db.cfg, now = Date.now(), life = c.pointExpireDays * DAY, t0 = dayStart();
    const txs = db.points.tx.filter(t => t.mem === memId && !t.void).sort((a, b) => a.at - b.at);
    let lots = [], expired = 0;
    const drop = when => { lots = lots.filter(l => { if(l.at + life <= when){ expired += l.left; return false; } return true; }); };
    txs.forEach(t => {
      drop(t.at);
      if(t.type === "earn") lots.push({ at: t.at, left: t.pts });
      else { let need = t.pts; for(const l of lots){ const k = Math.min(l.left, need); l.left -= k; need -= k; if(!need) break; } lots = lots.filter(l => l.left > 0); }
    });
    drop(now);
    const total = lots.reduce((s, l) => s + l.left, 0);
    const today = c.pointNextDay ? lots.filter(l => l.at >= t0).reduce((s, l) => s + l.left, 0) : 0;
    const soon = lots.filter(l => l.at + life - now < 30 * DAY).reduce((s, l) => s + l.left, 0);
    const first = lots.length ? lots[0].at + life : 0;
    return { total: total, usable: total - today, today: today, soon: soon, expired: expired, nextExpire: first };
  }
  const pbal = id => pstate(id).total;
  const fmtPhone = s => { const d = digits(s); return d.length === 11 ? d.slice(0, 3) + "-" + d.slice(3, 7) + "-" + d.slice(7) : d; };
  const bal = id => db.ledger.tx.reduce((s, t) => t.acct !== id || t.void ? s : s + (t.type === "charge" ? t.amount : -t.amount), 0);
  const won = n => (n < 0 ? "−" : "") + Math.abs(n).toLocaleString("ko-KR") + "원";

  /* 오늘 기록 예시 — 예시 자료에서 오늘 일어난 일을 거꾸로 적어 둠 */
  function seedLog(out){
    const t0 = dayStart(), L = [], add = (at, kind, text, by) => { if(at >= t0) L.push({ id: "gs" + L.length, at: at, kind: kind, text: text, by: by }); };
    out.wait.list.forEach(w => {
      add(w.at, "wait", `웨이팅 ${w.no}번 ${w.people}명 접수`, w.src === "직접 등록" ? "매장 화면" : "입구 기기");
      if(w.callAt) add(w.callAt, "wait", `웨이팅 ${w.no}번 호출`, "매장 화면");
      if(w.doneAt) add(w.doneAt, "wait", `웨이팅 ${w.no}번 ${{ in: "입장", gone: "미방문", cancel: "취소" }[w.status]}`, "매장 화면");
    });
    out.points.tx.forEach(t => { const m = out.points.members.filter(x => x.id === t.mem)[0];
      add(t.at, "point", `${m.phone} ${t.type === "earn" ? "적립 +" + t.pts.toLocaleString("ko-KR") + " (결제 " + won(t.amount) + ")" : "사용 −" + t.pts.toLocaleString("ko-KR")}`, t.src === "직원 입력" ? "매장 화면" : "계산대"); });
    out.ledger.tx.forEach(t => { const a = out.ledger.accts.filter(x => x.id === t.acct)[0];
      add(t.at, "ledger", `${a.name} ${t.type === "charge" ? "충전" : "사용"} ${won(t.amount)}`, "매장 화면"); });
    out.res.filter(r => r.date === today() && (r.status === "in" || r.status === "noshow")).forEach(r => {
      add(t0 + (mins(r.time) + 5) * 60000, "res", `${r.time} ${r.name} ${r.people}명 ${r.status === "in" ? "방문" : "노쇼"}`, "매장 화면"); });
    out.log = L.filter(l => l.at <= Date.now()).sort((a, b) => a.at - b.at);
  }

  const RES_ST = { req: "새 신청", ok: "확정", in: "방문", noshow: "노쇼", cancel: "취소" };
  window.ZB = {
    get cfg(){ return db.cfg; },
    get res(){ return db.res; },
    get log(){ return db.log; },
    reload: load, save: save,
    setDevice(name){ device = name; },
    reset(){ db = seed(null); return db; },
    setCfg(patch){
      const changes = Object.keys(patch).filter(k => db.cfg[k] !== patch[k]).map(k => `${k} ${db.cfg[k]} → ${patch[k]}`);
      Object.assign(db.cfg, patch); db.cfg.onlineTables = Math.min(db.cfg.onlineTables, db.cfg.tables);
      if(changes.length) log("cfg", "설정 " + changes.join(", "));
      save();
    },
    add(r){ r.id = r.id || ("r_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6)); r.at = Date.now(); db.res.push(r);
      log("res", `${r.date.slice(5)} ${r.time} ${r.name} ${r.people}명 예약 ${r.status === "req" ? "신청" : "등록"} (${r.src})`); save(); return r; },
    update(id, patch){ const r = db.res.filter(x => x.id === id)[0]; if(r){ Object.assign(r, patch);
      if(patch.status) log("res", `${r.date.slice(5)} ${r.time} ${r.name} ${r.people}명 → ${RES_ST[patch.status]}`); save(); } return r; },
    byDate(date){ return db.res.filter(r => r.date === date).sort((a, b) => a.time < b.time ? -1 : a.time > b.time ? 1 : a.at - b.at); },
    tablesFor: tablesFor, usedAt: usedAt, fits: fits, leftAt: leftAt, dwellFor: dwellFor, noshowCount: noshowCount,
    /* 홈페이지 예약이 들어올 때 상태: 단체(groupConfirm 이상)는 사장님 확인, 그 아래는 바로 확정 */
    autoStatus(people){ return people >= db.cfg.groupConfirm ? "req" : "ok"; },
    /* 웨이팅 */
    get wait(){ return db.wait; },
    waitLive: waitLive, waitPace: waitPace, waitRange: waitRange, waitClose: waitClose,
    waitAhead(id){ return waitLive().findIndex(x => x.id === id); },   /* 내 앞에 몇 팀(0 이면 맨 앞, -1 이면 대기 중이 아님) */
    waitEta(ahead){ return ahead * waitPace().per; },
    waitAdd(people, phone, src, first){ const w = db.wait, r = { id: "w_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), no: ++w.seq, people: people, phone: phone || "", src: src, status: "wait", at: Date.now() };
      if(first) r.first = true; w.list.push(r); log("wait", `웨이팅 ${r.no}번 ${people}명 접수${first ? " (예약 손님 · 맨 앞)" : ""}`); save(); return r; },
    waitSet(id, status){ const r = db.wait.list.filter(x => x.id === id)[0]; if(!r) return null;
      r.status = status; if(status === "call") r.callAt = Date.now(); else if(status === "wait"){ delete r.callAt; delete r.doneAt; } else r.doneAt = Date.now();
      log("wait", `웨이팅 ${r.no}번 ${{ call: "호출", in: "입장", gone: "미방문", cancel: "취소", wait: "대기로 되돌림" }[status]}`); save(); return r; },
    waitOn(v){ db.wait.on = !!v; log("wait", v ? "웨이팅 접수 다시 받음" : "웨이팅 접수 멈춤"); save(); },
    /* 선결제 장부 */
    get ledger(){ return db.ledger; },
    bal: bal,
    acctTx(id){ return db.ledger.tx.filter(t => t.acct === id).sort((a, b) => a.at - b.at); },
    addAcct(p){ const a = Object.assign({ id: "a_" + Date.now().toString(36) }, p); db.ledger.accts.push(a); log("ledger", `새 장부 ${a.name}`); save(); return a; },
    addTx(acct, type, amount, memo, by){ const t = { id: "t_" + (++db.ledger.seq) + Date.now().toString(36), acct: acct, type: type, amount: amount, memo: memo || "", by: by || "", at: Date.now() }; db.ledger.tx.push(t);
      const a = db.ledger.accts.filter(x => x.id === acct)[0]; log("ledger", `${a ? a.name : ""} ${type === "charge" ? "충전" : "사용"} ${won(amount)}${memo ? " · " + memo : ""}`); save(); return t; },
    voidTx(id, on){ const t = db.ledger.tx.filter(x => x.id === id)[0]; if(t){ if(on === false) delete t.void; else t.void = true;
      const a = db.ledger.accts.filter(x => x.id === t.acct)[0]; log("ledger", `${a ? a.name : ""} ${t.type === "charge" ? "충전" : "사용"} ${won(t.amount)} ${t.void ? "취소" : "되살림"}`); save(); } return t; },
    /* 포인트 */
    get points(){ return db.points; },
    pbal: pbal, pstate: pstate, fmtPhone: fmtPhone,
    memTx(id){ return db.points.tx.filter(t => t.mem === id).sort((a, b) => a.at - b.at); },
    memberByPhone(p){ const f = fmtPhone(p); return db.points.members.filter(m => m.phone === f)[0] || null; },
    /* 오늘 이 회원이 이미 적립한 기록(중복 적립 경고용) */
    earnedToday(memId){ const t0 = dayStart(); return db.points.tx.filter(t => t.mem === memId && t.type === "earn" && !t.void && t.at >= t0); },
    /* 적립: 번호가 처음이면 회원을 만들고(이름·별명) 쌓음. src = 들어온 방식(계산대 / 직원 입력) */
    earn(phone, amount, name, src){
      let m = this.memberByPhone(phone), isNew = !m;
      if(!m){ m = { id: "m_" + Date.now().toString(36), phone: fmtPhone(phone), name: (name || "").trim() }; db.points.members.push(m); }
      else if(name && !m.name) m.name = name.trim();
      const t = { id: "p_" + (++db.points.seq) + Date.now().toString(36), mem: m.id, type: "earn", pts: Math.floor(amount * db.cfg.pointRate / 100), amount: amount, at: Date.now(), src: src || (device === "계산대" ? "계산대" : "직원 입력") };
      db.points.tx.push(t); log("point", `${m.phone} 적립 +${t.pts.toLocaleString("ko-KR")} (결제 ${won(amount)})${isNew ? " · 새 회원 " + (m.name || "") : ""}`); save(); return { m: m, t: t, isNew: isNew };
    },
    usePts(mem, pts, how){ const t = { id: "p_" + (++db.points.seq) + Date.now().toString(36), mem: mem, type: "use", pts: pts, amount: 0, at: Date.now(), how: how || "" }; db.points.tx.push(t);
      const m = db.points.members.filter(x => x.id === mem)[0]; log("point", `${m ? m.phone : ""} 사용 −${pts.toLocaleString("ko-KR")}${how ? " · 확인: " + how : ""}`); save(); return t; },
    voidPTx(id, on){ const t = db.points.tx.filter(x => x.id === id)[0]; if(t){ if(on === false) delete t.void; else t.void = true;
      const m = db.points.members.filter(x => x.id === t.mem)[0]; log("point", `${m ? m.phone : ""} ${t.type === "earn" ? "적립" : "사용"} ${t.pts.toLocaleString("ko-KR")} ${t.void ? "취소" : "되살림"}`); save(); } return t; },
    /* 계산대 화면에 띄운 결제 금액 — 직원이 금액을 보내면 손님이 계산대 태블릿(../points/)에서 번호를 눌러 적립. 한 번에 하나만 */
    get pending(){ return db.points.pending || null; },
    setPending(amount){ if(amount) db.points.pending = { amount: amount, at: Date.now() }; else delete db.points.pending; save(); },
    /* 마감 정산 — 오늘 입력한 포스 매출(비교용) */
    get closing(){ return db.closing && db.closing.date === today() ? db.closing : { date: today(), pos: 0 }; },
    setClosing(patch){ db.closing = Object.assign({}, this.closing, patch); if(patch.pos != null) log("point", `마감: 포스 매출 ${won(patch.pos)} 입력`); if(patch.done) log("point", "마감 확인 완료"); save(); },
    today: today, addDays: addDays, mins: mins, hhmm: hhmm, dayStart: dayStart, KEY: KEY
  };
  load();
})();
