/* 짚불태백 인계점 시안 — 예약·웨이팅 자료 한 곳 (window.ZB).
   손님 홈페이지의 예약 창(../js/reserve.js), 손님용 웨이팅 접수 화면(../waiting/), 매장 화면(app.js)이 이 파일 하나를 같이 씁니다.

   ★ 한옥반점과 다른 점: 자리를 '어느 테이블' 로 배정하지 않습니다. 테이블 '개수' 만 셉니다.
     · 예약 하나가 쓰는 테이블 수 = 인원 ÷ 한 테이블 좌석(올림)
     · 예약은 식사 시간(dwellMin) 동안 그 개수를 차지합니다
     · 홈페이지로는 onlineTables 개까지만 받고, 나머지는 워크인·전화용으로 남깁니다
     어느 자리에 앉힐지는 그날 매장이 정합니다 — 룸·합석·조건 같은 규칙이 통째로 필요 없어집니다.

   시안이라 서버가 없습니다. 자료는 이 브라우저(localStorage)에만 있고, 날짜가 바뀌면 예시를 새로 만듭니다. */
(function(){
  const KEY = "zb-demo-v1";
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
    waitMin: 8           /* 웨이팅: 앞 팀 하나가 빠지는 데 걸리는 시간(분, 예시) — 예상 대기 = 앞 팀 수 × 이 값 */
  };
  const ACTIVE = { req: 1, ok: 1, in: 1 };   /* 테이블을 차지하는 상태: 신청(확정 전에도 자리를 잡아 둠) · 확정 · 방문 */

  let db = null;
  function load(){
    try{ db = JSON.parse(localStorage.getItem(KEY) || "null"); }catch(e){ db = null; }
    if(!db || db.seeded !== today()) db = seed((db && db.cfg) || null);   /* 하루 지난 예시는 날짜가 안 맞아 새로 */
    /* 웨이팅이 생기기 전에 저장된 자료에는 웨이팅 칸이 없음 — 예약은 그대로 두고 빠진 것만 채움 */
    if(!db.wait || db.cfg.waitMin == null){ db.cfg = Object.assign({}, DEFAULT_CFG, db.cfg); if(!db.wait) db.wait = seedWait(); save(); }
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
          name: pick(FAM) + pick(GIV), phone: "010-0000-" + pad(Math.floor(rnd() * 100)) + pad(Math.floor(rnd() * 100)),
          memo: pick(MEMO), pre: people <= 6 ? pick(PRE) : "", status: status, src: src, at: Date.now() - Math.floor(rnd() * 5e8) });
      }
    }
    out.wait = seedWait();
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
      const r = { id: "w_ex" + (++no), no: no, people: people, phone: "010-0000-" + String(1000 + no * 137).slice(-4), src: src || "매장 접수", status: status, at: now - ago * M };
      if(status === "call") r.callAt = now - 2 * M;
      else if(!LIVE[status]) r.doneAt = r.at + 22 * M;
      list.push(r);
    };
    mk(95, 2, "in"); mk(88, 4, "in"); mk(80, 3, "gone"); mk(71, 6, "in"); mk(63, 2, "in"); mk(55, 4, "cancel"); mk(47, 5, "in", "직접 등록");
    mk(33, 4, "call"); mk(26, 2, "wait"); mk(19, 6, "wait"); mk(12, 3, "wait", "직접 등록"); mk(5, 4, "wait");
    return { on: true, seq: no, list: list };
  }
  const waitLive = () => db.wait.list.filter(x => LIVE[x.status]).sort((a, b) => a.no - b.no);

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
    today: today, addDays: addDays, mins: mins, hhmm: hhmm, KEY: KEY
  };
  load();
})();
