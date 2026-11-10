/* 짚불태백 광교점 시안 — 예약·웨이팅·선결제 장부·포인트 자료 한 곳 (window.ZB).
   손님 홈페이지의 예약 창(../js/reserve.js), 손님용 웨이팅 접수 화면(../waiting/), 매장 화면(app.js)이 이 파일 하나를 같이 씁니다.

   ★ 한옥반점과 다른 점: 자리를 '어느 테이블' 로 배정하지 않습니다. 테이블 '개수' 만 셉니다.
     · 예약 하나가 쓰는 테이블 수 = 인원 ÷ 한 테이블 좌석(올림)
     · 예약은 식사 시간(dwellMin) 동안 그 개수를 차지합니다
     · 홈페이지로는 onlineTables 개까지만 받고, 나머지는 워크인·전화용으로 남깁니다
     어느 자리에 앉힐지는 그날 매장이 정합니다 — 룸·합석·조건 같은 규칙이 통째로 필요 없어집니다.

   시안이라 서버가 없습니다. 자료는 이 브라우저(localStorage)에만 있고, 날짜가 바뀌면 예시를 새로 만듭니다. */
(function(){
  const KEY = "zb-demo-v3";   /* v3(11-10): 지점이 광교점이 아니라 광교점 — 더미 이름을 바꿔서 옛 자료는 읽지 않고 새로 만듦 */
  const pad = n => String(n).padStart(2, "0");
  const ymd = d => d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  const addDays = (s, n) => { const d = new Date(s + "T00:00:00"); d.setDate(d.getDate() + n); return ymd(d); };
  const mins = t => Number(t.slice(0, 2)) * 60 + Number(t.slice(3));
  const hhmm = m => pad(Math.floor(m / 60)) + ":" + pad(m % 60);
  const today = () => ymd(new Date());

  const DEFAULT_CFG = {
    tables: 20,          /* 매장 전체 테이블 수 (예시) */
    onlineTables: 12,    /* 그중 홈페이지 예약으로 받을 수 (예시) */
    seats: 4,            /* 한 테이블 좌석 */
    dwellMin: 120,       /* 한 팀 식사 시간(분) — 이 동안 테이블을 차지 */
    slots: ["11:30","12:00","12:30","13:00","13:30","14:00","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30"],   /* ../js/reserve.js 의 시간표와 같게 */
    waitMin: 8,          /* 웨이팅: 앞 팀 하나가 빠지는 데 걸리는 시간(분, 예시) — 예상 대기 = 앞 팀 수 × 이 값 */
    lowBalance: 100000,  /* 선결제 장부: 잔액이 이 아래로 내려가면 '충전 안내' 표시 */
    pointRate: 5,        /* 포인트: 결제 금액의 몇 % 를 쌓아 줄지 (예시) */
    pointMin: 5000       /* 포인트: 이만큼 모여야 쓸 수 있음 (1P = 1원) */
  };
  const ACTIVE = { req: 1, ok: 1, in: 1 };   /* 테이블을 차지하는 상태: 신청(확정 전에도 자리를 잡아 둠) · 확정 · 방문 */

  let db = null;
  function load(){
    try{ db = JSON.parse(localStorage.getItem(KEY) || "null"); }catch(e){ db = null; }
    if(!db || db.seeded !== today()) db = seed((db && db.cfg) || null);   /* 하루 지난 예시는 날짜가 안 맞아 새로 */
    /* 웨이팅이 생기기 전에 저장된 자료에는 웨이팅 칸이 없음 — 예약은 그대로 두고 빠진 것만 채움 */
    if(!db.wait || !db.ledger || !db.points || db.cfg.waitMin == null || db.cfg.lowBalance == null || db.cfg.pointRate == null){
      db.cfg = Object.assign({}, DEFAULT_CFG, db.cfg); if(!db.wait) db.wait = seedWait(); if(!db.ledger) db.ledger = seedLedger(); if(!db.points) db.points = seedPoints(); save(); }
    return db;
  }
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(db)); }catch(e){} }

  const tablesFor = (people, cfg) => Math.max(1, Math.ceil(people / (cfg || db.cfg).seats));
  /* 그 시각에 차 있는 테이블 수 */
  function usedAt(date, m, skipId, list){
    const dw = db.cfg.dwellMin;
    return (list || db.res).reduce((n, r) => {
      if(r.date !== date || !ACTIVE[r.status] || r.id === skipId) return n;
      const s = mins(r.time);
      return (s <= m && m < s + dw) ? n + tablesFor(r.people) : n;
    }, 0);
  }
  /* 그 시각에 시작하는 예약이 식사 시간 내내 들어갈 수 있나. online 이면 홈페이지 한도로 */
  function fits(date, time, people, online, skipId, list){
    const limit = online ? db.cfg.onlineTables : db.cfg.tables, need = tablesFor(people), s = mins(time);
    for(let m = s; m < s + db.cfg.dwellMin; m += 30){ if(usedAt(date, m, skipId, list) + need > limit) return false; }
    return true;
  }
  /* 그 시각에 시작하면 남는 테이블 수(식사 시간 중 가장 빡빡한 때 기준) */
  function leftAt(date, time, online){
    const limit = online ? db.cfg.onlineTables : db.cfg.tables, s = mins(time); let peak = 0;
    for(let m = s; m < s + db.cfg.dwellMin; m += 30) peak = Math.max(peak, usedAt(date, m));
    return limit - peak;
  }

  /* ---------- 예시 자료 ---------- */
  function seed(keepCfg){
    const cfg = Object.assign({}, DEFAULT_CFG, keepCfg || {});
    const out = { cfg: cfg, res: [], seeded: today() };
    db = out;
    let x = 20261110;   /* 늘 같은 예시가 나오게 정해진 씨앗 */
    const rnd = () => { x = (x * 1103515245 + 12345) & 0x7fffffff; return x / 0x7fffffff; };
    const pick = a => a[Math.floor(rnd() * a.length)];
    const FAM = ["김","이","박","최","정","강","조","윤","장","임","한","오","서","신","권"];
    const GIV = ["민수","서연","지훈","하은","도윤","수빈","예준","지우","현우","유진","성민","은지","준호","다은","태현"];
    const MEMO = ["", "", "", "", "유아용 의자 1개", "생일 모임", "회사 회식", "창가 자리 희망", "조용한 자리 부탁드려요", "주차 2대"];
    const PRE = ["", "", "", "우대 갈비", "生우대 갈비", "짚불 통 삼겹살", "우대 갈비"];
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
        if(!past && src === "홈페이지" && i <= 3 && rnd() < 0.3) status = "req";   /* 아직 확인 안 한 홈페이지 신청 몇 건 */
        if(!past && rnd() < 0.05) status = "cancel";
        out.res.push({ id: "ex_" + (++seq), date: date, time: time, people: people,
          name: pick(FAM) + pick(GIV), phone: "010-" + (2000 + Math.floor(rnd() * 8000)) + "-" + pad(Math.floor(rnd() * 100)) + pad(Math.floor(rnd() * 100)),
          memo: pick(MEMO), pre: people <= 6 ? pick(PRE) : "", status: status, src: src, at: Date.now() - Math.floor(rnd() * 5e8) });
      }
    }
    out.wait = seedWait();
    out.ledger = seedLedger();
    out.points = seedPoints();
    save();
    return out;
  }

  /* ---------- 웨이팅 ----------
     예약과 달리 '오늘, 지금' 만 있습니다. 번호표 한 줄 = { no 대기번호, people, phone, at 접수 시각, status }.
     status: wait 대기 → call 호출(입장 안내를 보냄) → in 입장 / gone 미방문 / cancel 취소
     예시는 지금 시각에서 거꾸로 만들어, 언제 열어도 대기 중인 팀이 보입니다. */
  const LIVE = { wait: 1, call: 1 };
  function seedWait(){
    const now = Date.now(), M = 60000, list = []; let no = 0;
    const mk = (ago, people, status, src) => {
      const r = { id: "w_ex" + (++no), no: no, people: people, phone: "010-" + String(3100 + no * 617).slice(-4) + "-" + String(1000 + no * 137).slice(-4), src: src || "매장 접수", status: status, at: now - ago * M };
      if(status === "call") r.callAt = now - 2 * M;
      else if(!LIVE[status]) r.doneAt = r.at + 22 * M;
      list.push(r);
    };
    mk(95, 2, "in"); mk(88, 4, "in"); mk(80, 3, "gone"); mk(71, 6, "in"); mk(63, 2, "in"); mk(55, 4, "cancel"); mk(47, 5, "in", "직접 등록");
    mk(33, 4, "call"); mk(26, 2, "wait"); mk(19, 6, "wait"); mk(12, 3, "wait", "직접 등록"); mk(5, 4, "wait");
    return { on: true, seq: no, list: list };
  }
  const waitLive = () => db.wait.list.filter(x => LIVE[x.status]).sort((a, b) => a.no - b.no);

  /* ---------- 선결제 장부 ----------
     회사·단골이 돈을 미리 맡겨 두고, 올 때마다 먹은 만큼 빼는 장부입니다(종이 장부·엑셀을 대신).
     장부 한 권 = acct { name, kind 회사/개인, contact 담당자, phone, memo }
     기록 한 줄 = tx { acct, type charge 충전 / use 사용, amount, memo, by 쓴 사람, at, void 취소 여부 }
     ★ 잔액은 따로 저장하지 않고 기록을 더해 계산합니다 — 잘못 넣은 줄은 지우지 않고 '취소' 로 남겨, 나중에 따져도 흔적이 보이게.
     잔액보다 많이 써도 막지 않습니다(모자란 만큼 마이너스 = 다음 충전에서 정산). */
  function seedLedger(){
    const now = Date.now(), D = 86400000, accts = [], tx = []; let n = 0;
    const A = (name, kind, contact, phone, memo) => { const a = { id: "a" + (accts.length + 1), name: name, kind: kind, contact: contact, phone: phone, memo: memo || "" }; accts.push(a); return a; };
    const T = (a, type, amount, daysAgo, memo, by, isVoid) => { const t = { id: "t" + (++n), acct: a.id, type: type, amount: amount, memo: memo || "", by: by || "", at: now - daysAgo * D - (n % 5) * 3600000 }; if(isVoid) t.void = true; tx.push(t); };
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
    T(a, "charge", 1000000, 20, "계좌이체"); T(a, "use", 312000, 14, "지점 회식 14명", "최 팀장");
    a = A("이서연 님", "개인", "", "010-3368-1706", "");
    T(a, "charge", 100000, 50, "카드"); T(a, "use", 58000, 41, "3명"); T(a, "use", 49000, 22, "2명");
    a = A("광교중앙 상인회", "회사", "정 총무", "010-8823-1807", "월례회 셋째 주 화요일");
    T(a, "charge", 500000, 70, "계좌이체"); T(a, "use", 162000, 60, "월례회"); T(a, "use", 145000, 38, "월례회"); T(a, "use", 193000, 16, "월례회 + 추가 주문");
    a = A("정도윤 님", "개인", "", "010-6604-1908", "");
    T(a, "charge", 300000, 5, "카드");
    return { seq: n, accts: accts, tx: tx };
  }
  /* ---------- 포인트 ----------
     POS 연동 없이 시작할 수 있게: 계산할 때 직원이 '결제 금액 + 손님 휴대폰 번호' 를 넣으면 그 % 만큼 쌓입니다.
     처음 보는 번호면 그 자리에서 회원이 됩니다(따로 가입 단계 없음). 1P = 1원, 다음 계산에서 할인으로 씀.
     회원 = member { phone, name(선택) }, 기록 = tx { mem, type earn 적립 / use 사용, pts, amount 그때 결제 금액, at, void }
     장부와 같은 규칙: 잔액은 기록을 더해 계산하고, 잘못 넣은 줄은 지우지 않고 취소로 남깁니다. */
  function seedPoints(){
    let x = 4242; const rnd = () => { x = (x * 1103515245 + 12345) & 0x7fffffff; return x / 0x7fffffff; };
    const now = Date.now(), D = 86400000, rate = DEFAULT_CFG.pointRate, members = [], tx = []; let n = 0;
    const NAMES = ["김민수", "박지훈", "이하은", "최도윤", "정서연", "강예준"];
    for(let i = 0; i < 16; i++){
      const m = { id: "m" + (i + 1), phone: "010-" + String(2400 + i * 389).slice(-4) + "-" + String(2101 + i * 173).slice(-4), name: i % 3 === 0 ? NAMES[i / 3] : "" };
      members.push(m);
      const days = []; const v = 1 + Math.floor(rnd() * 6);
      for(let k = 0; k < v; k++) days.push(Math.floor(rnd() * 90));
      days.sort((a, b) => b - a);   /* 오래된 방문부터 */
      let bal = 0;
      days.forEach(d => {
        const at = now - d * D - (12 + Math.floor(rnd() * 9)) * 3600000 + 6 * 3600000, amount = (40 + Math.floor(rnd() * 200)) * 1000;
        if(bal >= 5000 && rnd() < 0.35){ const use = Math.floor(bal / 1000) * 1000; tx.push({ id: "p" + (++n), mem: m.id, type: "use", pts: use, amount: amount, at: at - 60000 }); bal -= use; }
        const pts = Math.floor(amount * rate / 100); tx.push({ id: "p" + (++n), mem: m.id, type: "earn", pts: pts, amount: amount, at: at }); bal += pts;
      });
    }
    return { seq: n, members: members, tx: tx };
  }
  const pbal = id => db.points.tx.reduce((s, t) => t.mem !== id || t.void ? s : s + (t.type === "earn" ? t.pts : -t.pts), 0);
  const fmtPhone = s => { const d = String(s || "").replace(/\D/g, ""); return d.length === 11 ? d.slice(0, 3) + "-" + d.slice(3, 7) + "-" + d.slice(7) : d; };

  const bal = id => db.ledger.tx.reduce((s, t) => t.acct !== id || t.void ? s : s + (t.type === "charge" ? t.amount : -t.amount), 0);

  window.ZB = {
    get cfg(){ return db.cfg; },
    get res(){ return db.res; },
    reload: load, save: save,
    reset(){ db = seed(null); return db; },
    setCfg(patch){ Object.assign(db.cfg, patch); db.cfg.onlineTables = Math.min(db.cfg.onlineTables, db.cfg.tables); save(); },
    add(r){ r.id = r.id || ("r_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6)); r.at = Date.now(); db.res.push(r); save(); return r; },
    update(id, patch){ const r = db.res.filter(x => x.id === id)[0]; if(r){ Object.assign(r, patch); save(); } return r; },
    byDate(date){ return db.res.filter(r => r.date === date).sort((a, b) => a.time < b.time ? -1 : a.time > b.time ? 1 : a.at - b.at); },
    tablesFor: tablesFor, usedAt: usedAt, fits: fits, leftAt: leftAt,
    /* 웨이팅 */
    get wait(){ return db.wait; },
    waitLive: waitLive,
    waitAhead(id){ return waitLive().findIndex(x => x.id === id); },   /* 내 앞에 몇 팀(0 이면 맨 앞, -1 이면 대기 중이 아님) */
    waitEta(ahead){ return ahead * db.cfg.waitMin; },
    waitAdd(people, phone, src){ const w = db.wait, r = { id: "w_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), no: ++w.seq, people: people, phone: phone || "", src: src, status: "wait", at: Date.now() }; w.list.push(r); save(); return r; },
    waitSet(id, status){ const r = db.wait.list.filter(x => x.id === id)[0]; if(!r) return null;
      r.status = status; if(status === "call") r.callAt = Date.now(); else if(status === "wait"){ delete r.callAt; delete r.doneAt; } else r.doneAt = Date.now();
      save(); return r; },
    waitOn(v){ db.wait.on = !!v; save(); },
    /* 선결제 장부 */
    get ledger(){ return db.ledger; },
    bal: bal,
    acctTx(id){ return db.ledger.tx.filter(t => t.acct === id).sort((a, b) => a.at - b.at); },   /* 오래된 것부터(잔액을 차례로 계산하려고) */
    addAcct(p){ const a = Object.assign({ id: "a_" + Date.now().toString(36) }, p); db.ledger.accts.push(a); save(); return a; },
    addTx(acct, type, amount, memo, by){ const t = { id: "t_" + (++db.ledger.seq) + Date.now().toString(36), acct: acct, type: type, amount: amount, memo: memo || "", by: by || "", at: Date.now() }; db.ledger.tx.push(t); save(); return t; },
    /* 포인트 */
    get points(){ return db.points; },
    pbal: pbal, fmtPhone: fmtPhone,
    memTx(id){ return db.points.tx.filter(t => t.mem === id).sort((a, b) => a.at - b.at); },
    memberByPhone(p){ const f = fmtPhone(p); return db.points.members.filter(m => m.phone === f)[0] || null; },
    /* 적립: 번호가 처음이면 회원을 만들고 쌓음 */
    earn(phone, amount, name){
      let m = this.memberByPhone(phone), isNew = !m;
      if(!m){ m = { id: "m_" + Date.now().toString(36), phone: fmtPhone(phone), name: name || "" }; db.points.members.push(m); }
      const t = { id: "p_" + (++db.points.seq) + Date.now().toString(36), mem: m.id, type: "earn", pts: Math.floor(amount * db.cfg.pointRate / 100), amount: amount, at: Date.now() };
      db.points.tx.push(t); save(); return { m: m, t: t, isNew: isNew };
    },
    usePts(mem, pts){ const t = { id: "p_" + (++db.points.seq) + Date.now().toString(36), mem: mem, type: "use", pts: pts, amount: 0, at: Date.now() }; db.points.tx.push(t); save(); return t; },
    /* 계산대 화면에 띄운 결제 금액 — 직원이 금액을 보내면 손님이 계산대 태블릿(../points/)에서 번호를 눌러 적립.
       한 번에 하나만(계산대는 하나). 적립이 끝나거나 직원이 거두면 비움. */
    get pending(){ return db.points.pending || null; },
    setPending(amount){ if(amount) db.points.pending = { amount: amount, at: Date.now() }; else delete db.points.pending; save(); },
    voidPTx(id, on){ const t = db.points.tx.filter(x => x.id === id)[0]; if(t){ if(on === false) delete t.void; else t.void = true; save(); } return t; },
    voidTx(id, on){ const t = db.ledger.tx.filter(x => x.id === id)[0]; if(t){ if(on === false) delete t.void; else t.void = true; save(); } return t; },
    today: today, addDays: addDays, mins: mins, hhmm: hhmm, KEY: KEY
  };
  load();
})();
