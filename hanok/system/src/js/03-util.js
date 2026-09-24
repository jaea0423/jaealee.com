/* ============================================================
   유틸
   ============================================================ */
function pad(n){ return String(n).padStart(2,"0"); }
/* 예약·설정 항목의 고유 번호.
   예전엔 "res_"+Date.now() 였는데, 기기 두 대가 같은 밀리초에 저장하면 같은 번호가 나옵니다.
   DB 의 기본 키가 될 값이라 겹치면 한쪽이 덮어써집니다.
   crypto.randomUUID 는 구형 TV 에 없어서 직접 만듭니다 (RFC 4122 v4 모양). */
/* 예약 번호(09-20 재아): 손님과 통화하거나 문자에 적을 때 부르는 6자리. 예약 id 에서 늘 같은 값이 나옵니다(저장 안 함).
   지운 예약이라도 id 가 다르니 번호가 겹치지 않습니다(같은 id 는 없음). 글자는 헷갈리는 0·O·1·I 를 뺀 32자 */
function resCode(r){
  /* 숫자 8자리(재아 09-20). 앞 prefix(res_/rq_)는 빼고 셈 — 홈페이지 접수 번호(rq_…)와 그걸 받은 예약(res_…)이 같은 번호가 되게(사이트 js/reserve.js 에 같은 함수) */
  var s = String(r && r.id || "").replace(/^(res|rq)_/, ""), h = 2166136261;
  for(var i = 0; i < s.length; i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  h = (h ^ (h >>> 13)) >>> 0; h = Math.imul(h, 2654435761) >>> 0;
  return String(h % 100000000).padStart(8, "0");
}
function newId(prefix){
  var h = "0123456789abcdef", out = "", i, r;
  for(i = 0; i < 36; i++){
    if(i === 8 || i === 13 || i === 18 || i === 23){ out += "-"; continue; }
    if(i === 14){ out += "4"; continue; }
    r = Math.floor(Math.random() * 16);
    if(i === 19) r = (r & 3) | 8;
    out += h.charAt(r);
  }
  return (prefix ? prefix + "_" : "") + out;
}
/* 예약이 바뀔 때마다 찍는 시각. 두 기기가 같은 예약을 고쳤는지 나중에 이걸로 압니다 */
function touch(rec){ if(rec) rec.updatedAt = new Date().toISOString(); return rec; }
function todayStr(d = new Date()){ return d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate()); }
function monthStr(d = new Date()){ return d.getFullYear()+"-"+pad(d.getMonth()+1); }
function shiftDate(s, days){ const d=new Date(s+"T00:00:00"); d.setDate(d.getDate()+days); return todayStr(d); }
function dateLabel(s){
  const d=new Date(s+"T00:00:00");
  return (d.getMonth()+1)+"월 "+d.getDate()+"일 ("+["일","월","화","수","목","금","토"][d.getDay()]+")";
}
/* 영업시간 줄 — 대시보드(타임라인 위)와 마법사 날짜 화면이 같은 것을 씁니다.
   한 문장('영업시간 … · 브레이크 … · 라스트오더 …')은 요일마다 길이가 달라 눈이 매번 다른 자리를 찾아야 했습니다.
   같은 폭 세 칸으로 나누면 값이 항상 같은 자리에 옵니다. 없는 항목도 칸을 비우지 않고 '없음' / '—' 로 채웁니다 */
function hoursLineHtml(dh){
  if(dh.closed) return `<div class="hours-line closed"><span class="hl-c"><i>휴무</i>${dh.note?esc(dh.note):""}</span></div>`;
  return `<div class="hours-line">
    <span class="hl-c"><i>영업시간</i>${esc(dh.open)} ~ ${esc(dh.close)}</span>
    <span class="hl-c"><i>브레이크</i>${dh.bs?`${esc(dh.bs)} ~ ${esc(dh.be)}`:"없음"}</span>
    <span class="hl-c"><i>라스트오더</i>${dh.lo?esc(dh.lo):"—"}</span>
  </div>`;
}
function nowHM(){ const d=new Date(); return pad(d.getHours())+":"+pad(d.getMinutes()); }
/* 예약 한 줄 요약 — '9/20(금) 18:00 · 홍길동 · 4명 · 관우 룸'. 확인창·토스트처럼 좁은 곳에 씁니다 */
function resLine(r){
  const d = new Date(r.date + "T00:00:00");
  const seat = seatText(r);
  return (d.getMonth()+1) + "/" + d.getDate() + "(" + ["일","월","화","수","목","금","토"][d.getDay()] + ") "
       + r.time + " · " + r.name + " · " + pplOf(r) + "명 · " + seat;
}
/* 타임라인 블록(홀·룸)과 손님 화면 줄을 '흐리게' 할지 — 세 곳이 같은 규칙을 씁니다.
   · 방문 처리한 예약은 바로 흐리게(끝난 일).
   · 처리 안 한 예약은 시작 +60분이 지나면 흐리게.
   → 흐려졌는데 '방문'이 안 찍힌 블록 = 노쇼 확인이 필요한 건, 이라는 뜻이 됩니다.
   6차 전에는 종료 시각(시작+체류시간)이 지나야 흐려져서, 한창 식사 중인 손님과 안 온 손님이 같은 색이었습니다. */
function isBlockPast(r, s0, date, nowM){
  const t = todayStr();
  if(date < t) return true;
  if(date > t) return false;
  return r.status === "방문" || s0 + 60 < nowM;
}
/* 입력값을 화면에 넣기 전 반드시 통과 — 스크립트 주입(XSS) 방지 */
function esc(s){
  return String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;")
    .replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");
}
/* onclick="fn('여기')" 안에 넣는 값. esc 만 하면 HTML 파서가 &#39; 를 ' 로 되돌려 JS 문자열이 끊깁니다 —
   JS 쪽 이스케이프(\')를 먼저 하고 HTML 이스케이프를 겹칩니다 */
function jsq(s){ return esc(String(s == null ? "" : s).replace(/\\/g,"\\\\").replace(/'/g,"\\'").replace(/\r?\n/g," ")); }
/* 구형 스마트TV 브라우저에는 structuredClone 이 없어 직접 복사합니다 */
function deepClone(o){ return JSON.parse(JSON.stringify(o)); }
function store(){ return DATA[view.storeKey]; }

/* ---------- 지난 예약 자동 정리 ----------
   손님이 왔다는 것을 기본으로 두고, 직원은 예외(노쇼·취소)만 누릅니다. */
/* ---------- 좌석 수 스냅샷 ----------
   s.snapshots = { "2026-09-12": { rooms: 8, hallTables: 11 }, ... }
   dayStat 이 '현재 설정'의 룸·홀 테이블 수로 모든 날짜를 계산해서, 룸을 하나 없애면 지난달 예약률이 전부 올랐습니다.
   지난 날짜는 그날의 좌석 수로 계산해야 하므로 하루 한 줄씩 남깁니다.
   · 앱을 켤 때(loadData)·날짜가 바뀔 때(1분 갱신 타이머)·설정을 적용할 때 부릅니다.
   · 오늘 것은 아직 바뀔 수 있으니 매번 덮어쓰고, 빠진 지난 날짜(앱을 안 켠 날)는 오늘 설정으로 채웁니다.
   · 1년 넘은 것은 지웁니다. 하루 1~2줄이라 용량 걱정 없음. Supabase 로 갈 때 같은 JSON 에 실려 갑니다(별도 테이블 없음) */
var SNAP_DAY = null;
function takeSnapshot(){
  if(!DATA) return;
  var today = todayStr();
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var st = DATA[k] && DATA[k].settings;
    if(!st) return;
    var snaps = DATA[k].snapshots = DATA[k].snapshots || {};
    var all = st.rooms || [];
    var roomN = all.filter(function(r){ return r.type === "room"; }).length;
    var hallN = all.filter(function(r){ return isTable(r); }).length;   /* 테이블 수 (이름은 옛 것 그대로 — 스냅샷 호환) */
    var keys = Object.keys(snaps).sort();
    /* 빠진 지난 날짜 — 마지막 스냅샷 다음 날부터(하나도 없으면 30일 전부터) 어제까지 */
    var d = keys.length ? shiftDate(keys[keys.length - 1], 1) : shiftDate(today, -30), guard = 0;
    while(d < today && guard++ < 400){ if(!snaps[d]) snaps[d] = { rooms: roomN, hallTables: hallN }; d = shiftDate(d, 1); }
    snaps[today] = { rooms: roomN, hallTables: hallN };
    var limit = shiftDate(today, -366);
    for(var i = 0; i < keys.length; i++) if(keys[i] < limit) delete snaps[keys[i]];
  });
  SNAP_DAY = today;
  saveData();
}
function autoCloseDays(){
  if(!DATA || clockBad()) return 0;   /* 시계가 틀린 기기가 미래 예약을 '방문' 으로 올리지 않게 */
  const today = todayStr();
  let n = 0;
  Object.keys(DEFAULT_DATA).forEach(k=>{
    (DATA[k].reservations||[]).forEach(r=>{
      if(r.date < today && r.status==="확정"){ r.status="방문"; r.auto=true; n++; }
    });
  });
  if(n) saveData();
  return n;
}
function autoClosedList(date){
  const s = store();
  return s.reservations.filter(r=>r.date===date && r.auto && r.status==="방문")
    .sort((a,b)=>a.time.localeCompare(b.time));
}

/* ---------- 접속 기록 ----------
   퇴사자 분쟁 등 사후 확인용. 사람이 읽기 좋게 꾸미지 않고 그대로 쌓습니다. */
function logEvent(action, detail){
  if(!DATA || !DATA._logs) return;
  DATA._logs.push({
    ts: new Date().toISOString(),
    ip: SESSION && SESSION.who ? SESSION.who : CLIENT_IP,
    store: view.storeKey || "-",
    action,
    detail: detail || "",
    ua: (navigator.userAgent||"").slice(0,120)
  });
  if(DATA._logs.length > LOG_MAX) DATA._logs = DATA._logs.slice(-LOG_MAX);
  /* 서버에도 한 줄. 실패해도 무시 — 로그 때문에 화면이 죽으면 안 됩니다.
     who(계정) 는 보내지 않습니다 — 서버가 토큰의 이메일로 채웁니다(supabase/patch_8차.sql, 위조 방지) */
  if(supaOn() && SESSION && !OFFLINE){
    sb("/rest/v1/logs", { method:"POST", body:{ store:view.storeKey || "-", action:action, detail:detail || "", ua:(navigator.userAgent||"").slice(0,120) }, prefer:"return=minimal" })
      .catch(function(e){ console.warn("로그 저장 실패", e.message); });
  }
  saveData();
}

/* 총 인원 — 어린이를 포함한 값. 옛 기록(성인+어린이 분리)도 함께 처리 */
/* 총 인원. 옛 데이터는 people 없이 adults+infants 로 저장돼 있어 그때만 더해 씁니다.
   (예전에는 자기 자신을 다시 부르게 돼 있어 people 이 없으면 무한 재귀로 멈췄습니다) */
function pplOf(r){ return r.people != null ? r.people : ((r.adults||0) + (r.infants||0)); }
/* 인원 표기 — "6명 (어린이 1명 포함)" */
function pplText(r){
  const n = pplOf(r), i = r.infants||0;
  return i ? `${n}명(어린이${i})` : `${n}명`;
}

/* ---------- 좌석 판정 (체류시간 기준) ---------- */
function toMin(t){ const [h,m]=t.split(":").map(Number); return h*60+m; }
/* 그 시각의 체류 시간(분) — 점심과 저녁을 다르게 잡습니다 */
/* ---------- 운영시간 ----------
   요일별 기본값 + 적용 시작일 + 그날만의 예외(임시 휴무·단축 영업) */
function scheduleFor(date){
  const st = store().settings;
  const list = (st.schedules||[]).filter(s=>s.from<=date).sort((a,b)=>a.from.localeCompare(b.from));
  return list.length ? list[list.length-1] : null;
}
/* 내장 공휴일표 — 인터넷 없이도 돌아야 하고(외부 요청 0), 공공 API 는 키 갱신·장애 위험이 있어 표로 둡니다.
   대체공휴일 포함. 임시공휴일·선거일은 미리 알 수 없으니 사장님이 설정에서 추가합니다(2026-06-03 지방선거는 넣음).
   ★ 매년 11월에 다음 해가 이 표에 없으면 설정·확인 필요에 안내가 뜹니다 — 그때 한 줄 추가하거나 설정에서 직접 등록 ★ */
var KR_HOLIDAYS = {
  2026: ["2026-01-01","2026-02-16","2026-02-17","2026-02-18","2026-03-01","2026-03-02","2026-05-05","2026-05-24","2026-05-25","2026-06-03","2026-06-06",
         "2026-08-15","2026-08-17","2026-09-24","2026-09-25","2026-09-26","2026-09-28","2026-10-03","2026-10-05","2026-10-09","2026-12-25"],
  2027: ["2027-01-01","2027-02-06","2027-02-07","2027-02-08","2027-02-09","2027-03-01","2027-05-05","2027-05-13","2027-06-06","2027-06-07",
         "2027-08-15","2027-08-16","2027-09-14","2027-09-15","2027-09-16","2027-10-03","2027-10-04","2027-10-09","2027-10-11","2027-12-25","2027-12-27"]
};
function isHoliday(date){
  const st = store().settings;
  if(st.holidayMode === false) return false;
  if((st.holidaysOff||[]).indexOf(date) >= 0) return false;
  if((st.holidays||[]).indexOf(date) >= 0) return true;
  const y = KR_HOLIDAYS[Number(date.slice(0,4))];
  return !!y && y.indexOf(date) >= 0;
}
/* 공휴일 표시 켜기/끄기 — 사장 추가(holidays)·제외(holidaysOff) 목록으로. 워크시프트 날짜 머리·휴무 등록에서 부름. 바로 저장(설정 '적용하기' 없이) */
function setHolidayFlag(date, on){
  const st = store().settings; st.holidays = st.holidays || []; st.holidaysOff = st.holidaysOff || [];
  const builtin = !!(KR_HOLIDAYS[Number(date.slice(0,4))] || []).includes(date);
  st.holidays = st.holidays.filter(d => d !== date); st.holidaysOff = st.holidaysOff.filter(d => d !== date);
  if(on && !builtin) st.holidays.push(date);
  if(!on && builtin) st.holidaysOff.push(date);
  mirrorDraft("holidays"); mirrorDraft("holidaysOff");
  logEvent("설정 변경", `공휴일 ${on ? "지정" : "해제"} ${date}`); saveData();
}
/* 그 해의 공휴일 목록(내장 + 사장 추가 − 제외) */
function holidaysOfYear(y, settings){
  const st = settings || store().settings, out = {};   /* 설정 화면은 임시본을 넘깁니다 */
  (KR_HOLIDAYS[y]||[]).forEach(d=>{ out[d] = "내장"; });
  (st.holidays||[]).forEach(d=>{ if(d.slice(0,4)===String(y)) out[d] = "추가"; });
  (st.holidaysOff||[]).forEach(d=>{ delete out[d]; });
  return Object.keys(out).sort().map(d=>({date:d, src:out[d]}));
}
/* 다음 해 공휴일이 준비돼 있는지 — 11월부터 없으면 알립니다 */
function holidayTableGap(){
  const d = new Date(), y = d.getFullYear(), next = y + 1;
  if(d.getMonth() < 10) return null;
  if(KR_HOLIDAYS[next] || (store().settings.holidays||[]).some(x=>x.slice(0,4)===String(next))) return null;
  return next;
}
function hoursFor(date){
  const st = store().settings;
  const sch = scheduleFor(date);
  const dow = new Date(date+"T00:00:00").getDay();
  /* 공휴일이면 공휴일 운영시간을 먼저 봅니다 */
  const dayDef = (isHoliday(date) && sch && sch.holiday) ? sch.holiday
               : (sch && sch.days && sch.days[dow]);
  const base = dayDef ? {...dayDef}
    : {open:st.open||"11:00", close:st.close||"22:00", lo:st.lastOrder||"20:40", bs:"", be:""};
  base.closed = false; base.note = "";
  const ov = (st.overrides||[]).find(o=>o.date===date);
  if(ov){
    if(ov.closed) return {...base, closed:true, note:ov.note||"임시 휴무"};
    ["open","close","lo","bs","be"].forEach(k=>{ if(ov[k]!==undefined) base[k]=ov[k]; });
    base.note = ov.note||"임시 운영시간";
    base.custom = true;
  }
  return base;
}
/* 타임라인 가로축 — 어느 날이든 같은 폭으로 보이도록 가장 넓은 영업시간을 씁니다 */
function axisRange(){
  const st = store().settings;
  let o = 24*60, c = 0;
  (st.schedules||[]).forEach(s=>(s.days||[]).forEach(d=>{
    o = Math.min(o, toMin(d.open)); c = Math.max(c, toMin(d.close));
  }));
  (st.overrides||[]).forEach(v=>{
    if(v.open) o = Math.min(o, toMin(v.open));
    if(v.close) c = Math.max(c, toMin(v.close));
  });
  if(o>=c){ o = toMin(st.open||"11:00"); c = toMin(st.close||"22:00"); }
  return {o, c};
}
/* 그 시각이 브레이크타임인지 */
function inBreak(date, time){
  const h = hoursFor(date);
  if(!h.bs || !h.be || !time) return false;
  const t = toMin(time);
  return t >= toMin(h.bs) && t < toMin(h.be);
}
/* ---------- 세션 (8차-X) ----------
   하루 운영시간(day)에는 sess{edge, lunch{lastBook,room,table}, dinner{...}} 만 저장하고, 실제 세션 목록은 여기서 만듭니다.
   · 브레이크가 있으면 경계 = 브레이크 시작, 저녁 시작 = 브레이크 끝 (설정에서 잠김 — 임시 영업시간이 브레이크를 바꾸면 경계도 따라감)
   · 브레이크가 없으면 경계 = sess.edge. 경계 시각 자체는 저녁 (15:30 예약 = 저녁 규칙)
   · 브레이크도 경계도 없으면 하루가 한 세션 — 저녁 쪽 접수 마감·점유를 씁니다 (재아 질문: 그런 날이 실제로 있는지) */
function sessFromDay(day){
  if(day.sess) return day.sess;
  /* 옛 저장본(자유 세션 목록) — 첫 세션을 점심, 둘째를 저녁으로 */
  var ss = day.sessions || [], a = ss[0], b = ss[1] || ss[0];
  var stay = function(se, k){ return !se ? "end" : k === "table" && se.stayTable != null ? se.stayTable : (se.stay != null ? se.stay : "end"); };
  if(!a) return { edge:"15:30", lunch:{lastBook:"14:00", room:"end", table:"end"}, dinner:{lastBook:"19:30", room:"end", table:"end"} };
  return { edge: a.until || (ss[1] && ss[1].from) || "15:30",
           lunch:{ lastBook:a.lastBook || "14:00", room:stay(a,"room"), table:stay(a,"table") },
           dinner:{ lastBook:b.lastBook || "19:30", room:stay(b,"room"), table:stay(b,"table") } };
}
/* 저장본을 새 모양으로 고정합니다(설정 편집·마이그레이션) */
function ensureSess(day){ if(!day.sess) day.sess = sessFromDay(day); delete day.sessions; return day.sess; }
function sessionsOfDay(dh){
  var x = sessFromDay(dh);
  var edge = dh.bs ? dh.bs : (x.edge || "");
  var mk = function(name, from, seg, until){ return { name:name, from:from, lastBook:seg.lastBook, stay:seg.room, stayTable:seg.table != null ? seg.table : seg.room, until:until }; };
  if(!edge) return [ mk("종일", dh.open, x.dinner, dh.close) ];
  return [ mk("점심", dh.open, x.lunch, edge), mk("저녁", dh.be || edge, x.dinner, dh.close) ];
}
function sessionsFor(date){
  const dh = hoursFor(date);
  if(dh.closed) return [];
  return sessionsOfDay(dh);
}
/* 세션 점유 글자 — 룸/테이블이 같으면 하나로, 다르면 둘 다 */
function stayLabel(se){
  var f = function(v){ return v === "end" ? "끝까지" : (v || 110) + "분"; };
  var t = se.stayTable != null ? se.stayTable : se.stay;
  return t === se.stay ? (se.stay === "end" ? "세션 끝까지 한 팀" : f(se.stay)) : "룸 " + f(se.stay) + " · 테이블 " + f(t);
}
/* 그 시각이 속한 세션. 첫 세션 전이면 첫 세션 */
function sessionAt(date, time){
  const ss = sessionsFor(date); if(!ss.length || !time) return null;
  const t = toMin(time); let cur = ss[0];
  for(let i=0;i<ss.length;i++) if(toMin(ss[i].from) <= t) cur = ss[i];
  return cur;
}
/* 세션의 끝 시각(분) — until 이 있으면 그것, 없으면 다음 세션 시작, 그것도 없으면 마감 */
function sessionEnd(date, sess){
  const ss = sessionsFor(date), dh = hoursFor(date);
  if(sess.until) return toMin(sess.until);
  const i = ss.indexOf(sess);
  if(i >= 0 && i+1 < ss.length) return toMin(ss[i+1].from);
  return toMin(dh.close);
}
/* 그 시각에 앉은 팀이 자리를 쓰는 시간(분).
   stay:"end" = 세션 끝까지(평일 점심은 브레이크까지, 저녁은 영업 종료까지 — 한 자리에 한 팀). 숫자면 그 분만큼.
   8차-X: 룸/테이블 점유를 따로 둡니다(재아) — seatId 가 테이블(또는 테이블 희망 'table:1층')이면 stayTable */
function stayMinAt(date, time, seatId){
  if(!time) return 150;
  const sess = sessionAt(date, time);
  if(!sess){ const st = store().settings; return Math.round((st.stayHours||3)*60); }
  const x = seatId ? seatById(seatId) : null;
  const isT = !!seatId && (isTablePref(seatId) || (x && isTable(x)));
  const stv = isT && sess.stayTable != null ? sess.stayTable : sess.stay;
  if(stv === "end") return Math.max(30, sessionEnd(date, sess) - toMin(time));
  return Math.max(30, Number(stv) || 150);
}
/* 예약 한 건의 체류 시간 — 배정된(또는 잠정) 좌석, 없으면 희망 종류(테이블 예약이면 테이블 점유) */
function stayOf(r){ return stayMinAt(r.date, r.time, effSeat(r) || r.seatPref); }
/* ---------- 홀 테이블 ----------
   홀마다 2인석·4인석·6인석 등을 섞어 둘 수 있고, 붙일 수 있는지도 따로 정합니다. */

/* 남은 테이블로 이 인원을 앉힐 수 있는지
   - 같은 존 안에서만 붙일 수 있고, 존마다 정한 최대 개수를 넘지 못합니다.
   - 남는 자리가 가장 적은 조합을 고릅니다. */
/* 예약 한 건이 쓰는 테이블 수 (표시용) */
/* ---------- 좌석 헬퍼 (8차) ----------
   룸: minCapacity(최적=최소) ~ capacity(최대). 테이블: seats(기본) ~ capacity(있으면, 여포 5) / 최소는 minCapacity(여포 4) 아니면 없음 */
function isRoom(x){ return !!x && x.type === "room"; }
function isTable(x){ return !!x && (x.type === "table" || x.type === "hall"); }
/* id 로 좌석 찾기 — 지금 좌석에 없으면 예정 좌석에서도 찾습니다(예정 날짜의 예약이 그 좌석을 가리킬 수 있음) */
function seatById(id){ const st = store().settings; return (st.rooms||[]).find(x=>x.id===id) || allSeatsEver().find(x=>x.id===id) || null; }
/* 주말·공휴일이면 true (공휴일을 주말로 볼지는 설정) */
function isWeekendDay(date){ if(!date) return false; const dow = new Date(date+"T00:00:00").getDay(); return dow===0 || dow===6 || (store().settings.holidayAsWeekend!==false && isHoliday(date)); }
/* 룸 최소 인원 — 날짜를 주면 주말·공휴일은 minWeekend(있으면). 테이블은 minCapacity 없으면 0 */
function roomMin(r, date){
  if(!r) return 0;
  if(isRoom(r) && date && isWeekendDay(date) && r.minWeekend != null) return r.minWeekend;
  if(r.minCapacity != null) return r.minCapacity;
  return isTable(r) ? 0 : Math.max(2,(r.capacity||2)-2);
}
/* 룸 최적 인원(안내용) — 없으면 주말 최소 */
function roomOpt(r){ if(!r || !isRoom(r)) return 0; return r.optCapacity != null ? r.optCapacity : (r.minWeekend != null ? r.minWeekend : roomMin(r)); }
function seatMax(r){ if(!r) return 0; return isTable(r) ? (r.capacity || r.seats || 4) : (r.capacity || 4); }
/* 예약이 쓰는 좌석 전부(대표 + 합친 것). 확정이면 roomId 계열, 아니면 잠정 계열 */
function seatsOf(r){
  if(r.roomId) return [r.roomId].concat(r.extraIds || []);
  if(r.tentativeRoomId) return [r.tentativeRoomId].concat(r.tentativeExtra || []);
  return [];
}
function usesSeat(r, id){ return seatsOf(r).indexOf(id) >= 0; }
/* 좌석 묶음의 최대 인원 — 룸 합침 그룹이면 그룹 max, 테이블 여러 개면 seats 합 */
function seatsMax(ids){
  const st = store().settings;
  const j = (st.joins||[]).find(g=>sameIds(g.ids, ids));
  if(j) return j.max;
  return ids.reduce((a,id)=>a+seatMax(seatById(id)), 0);
}
function seatsMin(ids, date){
  const st = store().settings;
  const j = (st.joins||[]).find(g=>sameIds(g.ids, ids));
  if(j) return j.min;
  if(ids.length === 1) return roomMin(seatById(ids[0]), date);
  return 0;
}
function sameIds(a, b){ if(!a || !b || a.length !== b.length) return false; const x = a.slice().sort(), y = b.slice().sort(); return x.every((v,i)=>v===y[i]); }
/* 합침 그룹 찾기 */
function joinOf(ids){ return allJoinsEver().find(g=>sameIds(g.ids, ids)) || null; }
/* ---------- 테이블은 층 단위 (8차-H) ----------
   홀은 그날 남는 자리에 앉히는 곳이라 테이블을 미리 정해도 현장에서 지켜지지 않습니다.
   그래서 예약은 '1층 테이블 / 저층 테이블' 까지만 받고, 시스템은 층의 자리 수(테이블 인원 합)와
   같은 시간에 겹치는 손님 수로 '자리 부족' 만 알립니다. 특정 테이블 배정은 수정 시트에서만(파셜룸 등). */
function isTablePref(p){ return p === "table-any" || p === "hall-any" || /^table:/.test(p || ""); }
function prefFloor(p){ return /^table:/.test(p || "") ? p.slice(6) : null; }
function floorTables(fl, date){ return (date ? roomsAt(date) : (store().settings.rooms || [])).filter(t => isTable(t) && (fl == null || (t.floor || "") === (fl || ""))); }   /* fl == null → 전체. date 를 주면 그 날짜의 좌석 */
/* 예약이 쓰는 테이블 층. 룸이면 undefined, 층 미정 테이블이면 null */
function resFloor(r){
  if(r.roomId){ const x = seatById(r.roomId); return x && isTable(x) ? (x.floor || "") : undefined; }
  if(isTablePref(r.seatPref)){
    const pf = prefFloor(r.seatPref);
    if(pf != null) return pf;
    /* 층 상관없음(table-any)이라도 잠정 배정된 테이블이 있으면 그 층 — '층 미정' 줄은 정말 자리를 못 찾았을 때만(재아 09-17) */
    const t = r.tentativeRoomId ? seatById(r.tentativeRoomId) : null;
    return t && isTable(t) ? (t.floor || "") : null;
  }
  return undefined;
}
function floorSeats(fl, date, time){
  return floorTables(fl).filter(t => !(date && time && blockedAt(t, date, time))).reduce((a, t) => a + (t.seats || 4), 0);
}
function floorLabel(fl){ return `${fl || ""} 테이블`.trim(); }
/* 그 시각에 그 층에서 한 자리(붙임 포함)로 앉힐 수 있는 최대 인원 — 마법사 안내용. 20명부터 내려가며 찾습니다 */
/* fl == null 은 '층 상관없음' — findSeat 에 floor 를 안 넘겨 전체 테이블(사장님 순서)로 */
function floorMaxParty(fl, date, time, excludeId){
  for(let p = 21; p >= 1; p--) if(findSeat({date, time, people:p, kind:"table-any", floor:fl, excludeId, noSplit:true})) return p;
  return 0;
}
/* 테이블 예약(층)의 숨은 배정 결과 — {state:"ok"|"split"|"none", f} */
function floorFit(fl, date, time, people, excludeId){
  const f = findSeat({date, time, people, kind:"table-any", floor:fl, excludeId});
  return { state: !f ? "none" : (f.split ? "split" : "ok"), f };
}
/* 두 테이블을 붙일 수 있는지(양쪽 다 허용) */
function canJoinTables(a, b){
  const A = seatById(a), B = seatById(b);
  return isTable(A) && isTable(B) && A.floor === B.floor && (A.joinWith||[]).indexOf(b) >= 0 && (B.joinWith||[]).indexOf(a) >= 0;
}
/* 수리·고장 등으로 잠시 쓰지 않는 좌석 */
/* ---------- 좌석 사용 중지 (기간제) ----------
   room.blocks = [{id, from, to, fromTime, toTime, openEnded, note}]
     from~to      : 날짜 범위. openEnded 면 to 는 무시하고 '해제할 때까지'
     fromTime~toTime : 비우면 그 날 하루 종일.
                       기간이 여러 날이면 첫날은 fromTime 부터, 마지막 날은 toTime 까지,
                       가운데 날들은 하루 종일 잠급니다.
   막지는 않고 경고만 합니다(설계 5.2) — 판단은 사장님 몫입니다. */
function roomBlocks(r){ return (r && r.blocks) ? r.blocks : []; }

/* 그 좌석이 그 날짜에 잠기는 구간들을 '분' 단위로 돌려줍니다. 없으면 빈 배열 */
function blockSpans(room, date){
  const out = [];
  const list = roomBlocks(room);
  for(let i=0;i<list.length;i++){
    const b = list[i];
    if(!b.from || date < b.from) continue;
    if(!b.openEnded && b.to && date > b.to) continue;
    const last = b.openEnded ? null : (b.to || b.from);
    /* 첫날·마지막날만 시각을 적용하고, 사이에 낀 날은 하루 종일 */
    const s = (date === b.from && b.fromTime) ? toMin(b.fromTime) : 0;
    const e = (last && date === last && b.toTime) ? toMin(b.toTime) : 24*60;
    if(e <= s) continue;
    out.push({s, e, note:b.note||"", id:b.id, allDay:(s===0 && e===24*60), blk:b});
  }
  return out;
}
/* 그 날짜에 걸리는 사용 중지 항목(원본 block)들 — 라벨에 '기간' 을 적으려고. blockSpans 는 그 날의 분 구간만 주기 때문 */
function blocksOn(room, date){
  return roomBlocks(room).filter(function(b){ if(!b.from || date < b.from) return false; if(!b.openEnded && b.to && date > b.to) return false; return true; });
}
/* "9/17" · "9/17 ~ 9/19" · "9/17 부터" — 하루면 날짜 하나, 여러 날이면 시작 ~ 끝(재아) */
function blockPeriod(b){
  const md = function(d){ return d ? (+d.slice(5,7)) + "/" + (+d.slice(8,10)) : ""; };
  if(!b || !b.from) return "";
  if(b.openEnded) return md(b.from) + " 부터";
  if(!b.to || b.to === b.from) return md(b.from);
  return md(b.from) + " ~ " + md(b.to);
}
/* "사용 중지 (사유 / 기간)" — 사유가 없으면 기간만 */
function blockLabelText(b){
  const p = blockPeriod(b);
  return "사용 중지 (" + (b.note ? b.note + " / " : "") + p + ")";
}
/* 그 날짜(·시각)에 사용 중지인지. time 을 주면 그 시각만, 안 주면 그 날 하루 중 일부라도 */
function blockedAt(room, date, time){
  const spans = blockSpans(room, date);
  if(!spans.length) return null;
  if(!time) return spans[0];
  const t = toMin(time);
  for(let i=0;i<spans.length;i++) if(t >= spans[i].s && t < spans[i].e) return spans[i];
  return null;
}
/* "하루 종일" 또는 "11:00 ~ 16:00" 처럼 사람이 읽는 구간 표기 */
function spanLabel(sp){
  if(!sp) return "";
  if(sp.allDay) return "하루 종일";
  return hm(minToHM(sp.s)) + " ~ " + hm(minToHM(sp.e));
}
function minToHM(m){ return pad(Math.floor(m/60)%24) + ":" + pad(m%60); }
/* 그 날 하루가 통째로 잠겼는지 (타임라인 줄 전체를 흐리게 할지 판단) */
function blockedAllDay(room, date){
  const spans = blockSpans(room, date);
  for(let i=0;i<spans.length;i++) if(spans[i].allDay) return true;
  return false;
}
/* 예약 한 건이 사용 중지 구간에 걸리는지 — 체류 시간까지 봅니다 */
function resBlocked(r){
  if(!r.roomId) return null;
  const ids = [r.roomId].concat(r.extraIds||[]);
  const s = toMin(r.time), e = s + stayOf(r);
  for(let k=0;k<ids.length;k++){
    const room = seatById(ids[k]); if(!room) continue;
    const spans = blockSpans(room, r.date);
    for(let i=0;i<spans.length;i++) if(s < spans[i].e && spans[i].s < e) return spans[i];
  }
  return null;
}
/* 최소 인원 판정에 쓸 인원 — 설정에 따라 성인만 셉니다 */
function adultCount(people, infants){
  return store().settings.minCountAdultsOnly === false
    ? (people||0) : Math.max(0,(people||0)-(infants||0));
}
/* 마지막으로 예약을 받을 수 있는 시각 */
/* 유아용 의자 기본값을 어린이 수로 채울지(true) 0개로 둘지(false). 설정에서 바꿉니다 */
function chairDefaultInfants(){ return store().settings.chairDefault === "infants"; }   /* 기본 0개(재아). 설정에서 '어린이 수와 같게' 를 고르면 따라감 */
/* 자리 기준을 성인만으로 볼지, 어린이를 포함해 볼지 */
function seatCountsInfants(){ return store().settings.minCountAdultsOnly === false; }

/* 마지막으로 예약(입장)을 받을 수 있는 시각 — 그 시각이 속한 세션의 lastBook. 라스트오더(주방 마감)와는 다릅니다 */
function lastBookMin(date, time){
  const st = store().settings;
  const d = date || view.date || todayStr();
  const sess = sessionAt(d, time || "19:00");
  if(sess && sess.lastBook) return toMin(sess.lastBook);
  const h = hoursFor(d);
  return h.lo ? toMin(h.lo) : toMin(h.close) - (st.lastBookingBuffer != null ? st.lastBookingBuffer : 60);
}
/* 확정 배정이 없으면 잠정 배정을 좌석으로 간주 */
function effSeat(r){ return r.roomId || r.tentativeRoomId || null; }

/* 룸을 그 시각에 쓸 수 있는지 판정
   blocked: 앞뒤 1시간 안에 확정 예약 → 배정 불가
   warn   : 체류시간 안에 확정 예약, 또는 잠정 배정이 걸려 있음 → 사장 판단
   free   : 여유 있음                                                     */
/* 이 예약이 지금 좌석을 잡고 있는가 —
   '확정'은 앞으로 올 손님, '방문'은 지금 앉아 있는 손님. 둘 다 자리를 씁니다.
   '취소'와 '노쇼'는 자리를 비웁니다.

   ※ 예전에는 이 판단이 파일 안에서 다섯 갈래로 갈려 있었습니다.
      룸은 '확정'만 봐서 손님이 도착해 '방문'을 누르는 순간 빈 방이 되었고(이중 예약),
      홀은 '취소'만 빼서 노쇼 처리해도 테이블이 안 풀렸습니다.
      같은 버튼이 좌석 종류에 따라 정반대로 동작했습니다.
      새 판정을 넣을 때는 반드시 이 함수를 쓰세요. */
function holdsSeat(r){ return r.status==="확정" || r.status==="방문"; }

/* 좌석(룸이든 테이블이든 하나)을 그 시각에 쓸 수 있는지 — 합쳐 쓰는 예약도 그 좌석을 점유합니다 */
function roomStatus(date, time, roomId, excludeId, hitsOnly){
  const s = store();
  if(!time || !roomId) return {state:"free", hits:[], tentative:[], movable:[]};
  const t = toMin(time);
  const all = s.reservations.filter(r =>
    r.date===date && holdsSeat(r) && r.id!==excludeId && usesSeat(r, roomId));
  let state="free"; const near=[], tent=[], movable=[];
  for(const r of all){
    const rt = toMin(r.time), gap = Math.abs(rt-t);
    /* 겹침 = 먼저 앉는 팀의 점유가 끝나기 전에 다음 팀이 시작하면.
       예전엔 두 점유 시간 중 긴 쪽으로 대칭 비교해서, 저녁(끝까지 = 4시간) 예약이 낮 3시 예약과 겹친다고 나왔습니다 */
    const overlap = rt <= t ? rt + stayMinAt(date, r.time, roomId) > t : t + stayMinAt(date, time, roomId) > rt;
    if(!overlap) continue;
    if(r.roomId){
      if(gap < (store().settings.closeGapMin != null ? store().settings.closeGapMin : 60)){ state="blocked"; }   /* 설정: '이 시간 안에 겹치면 강한 경고' */
      else if(state!=="blocked"){ state="warn"; }
      near.push(r);
    }else{
      /* hitsOnly: 확정 예약만 볼 때는 잠정 예약이 비켜줄 수 있는지 따지지 않습니다 —
         그 판단(canRelocate→findSeat→roomStatus)이 다시 여기로 들어와 잠정끼리 서로를 기다리며 끝없이 돌았습니다 */
      if(hitsOnly){ tent.push(r); }
      else if(canRelocate(r, roomId)){ movable.push(r); }
      else{
        if(state==="free") state="warn";
        tent.push(r);
      }
    }
  }
  near.sort((a,b)=>a.time.localeCompare(b.time));
  return {state, hits:near, tentative:tent, movable};
}
/* 좌석 미정 예약을 지금 자리 말고 다른 곳으로 옮길 수 있는지 — 확정 예약만 따집니다(잠정끼리는 비켜줄 수 있음) */
function canRelocate(r, excludeRoomId){
  return !!findSeat({date:r.date, time:r.time, people:pplOf(r), kind:r.seatPref||"any", excludeId:r.id, excludeSeat:excludeRoomId, confirmedOnly:true});
}
/* 좌석 미정 예약들의 잠정 배정을 다시 계산 — 예약이 추가·변경될 때 호출 */
function reflowTentatives(date){
  const s = store();
  const targets = s.reservations.filter(r=>r.date===date && holdsSeat(r) && !r.roomId);
  targets.forEach(r=>{ r.tentativeRoomId = null; r.tentativeExtra = []; r.tentativeSplit = false; });
  /* 취소·노쇼는 자리를 안 잡으니 옛 잠정도 지웁니다 — 남겨 두면 상세에 '추천 좌석' 이 그대로 보였습니다(11월 시나리오 점검) */
  s.reservations.forEach(r=>{ if(r.date===date && !holdsSeat(r) && !r.roomId && r.tentativeRoomId){ r.tentativeRoomId = null; r.tentativeExtra = []; r.tentativeSplit = false; } });
  /* 테이블 예약(층)도 계산은 테이블 단위로 합니다 — 화면에는 층까지만 보이고, 겹침·붙임·나눠 앉기 판단에 씁니다 */
  targets.sort((a,b)=>a.time.localeCompare(b.time)).forEach(r=>{
    const fl = prefFloor(r.seatPref);
    const f = findSeat({date:r.date, time:r.time, people:pplOf(r), kind:isTablePref(r.seatPref) ? "table-any" : (r.seatPref||"any"), floor:fl, excludeId:r.id, strict:true});
    r.tentativeRoomId = f ? f.id : null; r.tentativeExtra = f && f.extra.length ? f.extra : []; r.tentativeSplit = !!(f && f.split);
  });
}
/* 홀의 그 시간대 테이블 사용 현황 (잠정 배정 포함)
   실제 테이블 목록을 놓고 먼저 온 팀부터 앉혀 봅니다. */
/* 이 인원이 홀에 들어갈 수 있는지 */
/* 이 인원이 쓰게 될 테이블 (표시용) */

/* 좌석 미정 예약에 붙일 '잠정 배정' 좌석을 고름
   - 룸: 인원이 맞는 가장 작은 빈 방
   - 홀: 남은 테이블이 충분한 홀
   자리가 없으면 null (예약은 받되 안내가 필요한 상황)                    */
/* ---------- 잠정 배정 (8차) ----------
   규칙(누님): 인원이 맞는 좌석 중 → 사장님이 정한 순서(설정 목록 순). 룸/테이블은 손님이 고른 쪽만.
   테이블: 한 테이블에 들어가면 그것(2명은 4인석 우선 — 중식당 관행), 안 들어가면 붙일 수 있는 테이블끼리 붙여서(개수 적은 조합 → 남는 자리 적은 조합).
   룸 합침(중문 탈거)은 자동으로 하지 않습니다 — 사람이 고를 때만.
   confirmedOnly: 확정 예약만 보고 판단(잠정 예약을 옮길 수 있는지 볼 때) */
function findSeat(o){
  const st = store().settings, date = o.date, time = o.time, people = o.people || 0;
  const kind = o.kind === "hall-any" ? "table-any" : (o.kind || "any");
  const wantRoom = kind === "room-any" || kind === "any", wantTable = kind === "table-any" || kind === "any";
  const free = id => {
    if(o.excludeSeat === id) return false;
    const rs = roomStatus(date, time, id, o.excludeId, !!o.confirmedOnly);
    if(o.confirmedOnly) return rs.hits.length === 0;
    return rs.state === "free" && !rs.tentative.length && !rs.movable.length;   /* 아무것도 없는 자리 */
  };
  /* 잠정만 있는 자리(그 팀이 다른 데로 갈 수 있을 때)도 후보로 — 단 잠정 재계산(strict)에서는 안 씁니다.
     재계산은 시간순으로 한 팀씩 자리를 잡는데, 앞 팀의 잠정을 '비켜줄 수 있다' 며 같은 자리를 또 주면 두 잠정이 한 자리에 겹쳐 보였습니다 */
  const freeLoose = id => !o.strict && o.excludeSeat !== id && roomStatus(date, time, id, o.excludeId).state === "free";
  const seats = roomsAt(date).filter(x=>!blockedAt(x, date, time));
  if(wantRoom){
    const rooms = seats.filter(x=>isRoom(x) && people >= roomMin(x, date) && people <= seatMax(x));
    for(const r of rooms) if(free(r.id)) return {id:r.id, extra:[]};
    if(!o.confirmedOnly) for(const r of rooms) if(freeLoose(r.id)) return {id:r.id, extra:[]};
  }
  if(wantTable){
    /* 층을 정한 테이블 예약("table:1층")은 그 층 안에서만. 층 미정(옛 table-any)은 전체 */
    const inFloor = x => o.floor == null || (x.floor||"") === (o.floor||"");
    const tables = seats.filter(x=>isTable(x) && inFloor(x) && people >= roomMin(x) && people <= seatMax(x));
    /* 2명은 4인석을 먼저 (2인석은 좁아 손님이 싫어함). 그 밖에는 사장님이 정한 순서(설정의 테이블 순서) —
       저층은 여포가 맨 앞이라 4~5명은 여포부터(재아: 우선순위 높음). 순서가 같을 리 없으니 남는 자리는 마지막 기준 */
    const order = x => roomsAt(date).indexOf(x);
    /* 짝(pair)이 있는 테이블(하후상-1·2)은 평소 붙여 8인석으로 두므로, 한 테이블만 쓰는 팀에게는 맨 뒤 — 다른 4인석이 다 찼을 때만 나눠 씁니다(누님 09-20) */
    const score = x => ((people <= 2 && (x.seats||4) >= 4) ? 0 : 1000) + (x.pair ? 500 : 0) + order(x);
    const sorted = tables.slice().sort((x,y)=>score(x)-score(y) || (seatMax(x)-seatMax(y)));
    for(const t of sorted) if(free(t.id)) return {id:t.id, extra:[]};
    if(!o.confirmedOnly) for(const t of sorted) if(freeLoose(t.id)) return {id:t.id, extra:[]};
    /* 붙이기 — 비어 있는 테이블 중 서로 붙일 수 있는 조합 */
    const pool = seats.filter(x=>isTable(x) && inFloor(x) && (x.joinWith||[]).length && ((o.confirmedOnly || o.strict) ? free(x.id) : freeLoose(x.id)));
    let best = null;
    const tryCombo = (combo, sum) => {
      if(sum >= people){
        const waste = sum - people;
        const paired = combo.length === 2 && combo[0].pair === combo[1].id;   /* 평소 붙여 둔 짝(하후상-1·2)은 같은 조건이면 먼저 */
        if(!best || combo.length < best.combo.length || (combo.length === best.combo.length && (waste < best.waste || (waste === best.waste && paired && !best.paired)))) best = {combo:combo.slice(), waste, paired};
        return;
      }
      if(combo.length >= 5) return;
      const last = combo[combo.length-1];
      pool.forEach(x=>{
        if(combo.indexOf(x) >= 0) return;
        if(pool.indexOf(x) < pool.indexOf(last)) return;            /* 순서 고정으로 중복 조합 방지 */
        if(!combo.some(c=>canJoinTables(c.id, x.id))) return;   /* 하나라도 이어져 있으면(한 줄로 붙는 자리) — 전부 서로 붙을 필요는 없음 */
        combo.push(x); tryCombo(combo, sum + (x.seats||4)); combo.pop();
      });
    };
    pool.forEach(x=>tryCombo([x], x.seats||4));
    if(best) return {id:best.combo[0].id, extra:best.combo.slice(1).map(x=>x.id)};
    /* 나눠 앉기(재아 결정) — 붙일 조합이 없으면 빈 테이블 여러 개에 나눠 앉는 것으로 잡습니다. 붙임 여부는 안 봅니다.
       큰 테이블부터 채워 개수를 최소로. 결과에 split 을 붙여 화면에서는 경고로만 알립니다(막지 않음) */
    if(!o.noSplit){
      const freeT = seats.filter(x=>isTable(x) && inFloor(x) && !(roomMin(x) > people && false) && ((o.confirmedOnly || o.strict) ? free(x.id) : freeLoose(x.id)))
        .sort((x,y)=>(y.seats||4)-(x.seats||4));
      let sum = 0; const pick = [];
      for(const t of freeT){ if(sum >= people) break; pick.push(t); sum += (t.seats||4); }
      if(sum >= people && pick.length > 1){
        /* 골라진 테이블들이 서로 이어져 있으면(한 줄) 나눠 앉는 게 아니라 붙이는 것 */
        const chained = pick.every((x,i)=>i===0 || pick.slice(0,i).some(c=>canJoinTables(c.id, x.id)));
        return {id:pick[0].id, extra:pick.slice(1).map(x=>x.id), split:!chained};
      }
    }
  }
  return null;
}
function suggestSeatFull(date, time, people, kind, excludeId){
  return findSeat({date:date, time:time, people:people, kind:kind, excludeId:excludeId});
}
/* 대표 좌석 id 만 (옛 호출부용) */
function suggestSeat(date, time, people, kind, excludeId){
  const f = suggestSeatFull(date, time, people, kind, excludeId);
  return f ? f.id : null;
}

/* 영업 상태를 현재 시각으로 계산 */
function shopState(st){
  if(st.tempClosed) return {cls:"closed", txt:"임시 휴무"};
  const today = todayStr();
  const h = hoursFor(today);
  if(h.closed) return {cls:"closed", txt:esc(h.note||"휴무")};
  const n = nowHM();
  if(n < h.open)   return {cls:"prep",   txt:"영업 준비 중"};
  if(n >= h.close) return {cls:"closed", txt:"영업 종료"};
  if(h.bs && h.be && n>=h.bs && n<h.be) return {cls:"prep", txt:"브레이크타임"};
  if(h.lo && n >= h.lo) return {cls:"open", txt:"영업 중 · 라스트오더 지남"};
  return {cls:"open", txt:"영업 중"};
}

/* 아이콘 (선으로만 그린 최소한의 아이콘) */
const ICON = {
  spark:'<svg viewBox="0 0 24 24"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8zM5 15l.6 1.6L7 17l-1.4.6L5 19l-.6-1.4L3 17l1.4-.4z"/></svg>',
  sms:'<svg viewBox="0 0 24 24"><path d="M4 5h16v11H8l-4 4z"/><path d="M8 9h8M8 12h5"/></svg>',
  key:'<svg viewBox="0 0 24 24"><circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3M15 12v2"/></svg>',
  back:'<svg viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
  person:'<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.6"/><path d="M4.5 20.5c0-4.1 3.4-6.6 7.5-6.6s7.5 2.5 7.5 6.6"/></svg>',
  users:'<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><circle cx="17" cy="9" r="2.4"/><path d="M2.5 20c0-3.3 2.9-5.5 6.5-5.5s6.5 2.2 6.5 5.5M16 14.5c3 0 5.5 1.8 5.5 4.5"/></svg>',
  print:'<svg viewBox="0 0 24 24"><path d="M7 8V4h10v4M7 16H5a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2M7 13h10v7H7z"/></svg>',
  site:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/></svg>',
  expand:'<svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>',
  shrink:'<svg viewBox="0 0 24 24"><path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5"/></svg>',
  dash:'<svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="8" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="11" width="7" height="10" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/></svg>',
  res:'<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
  staff:'<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><path d="M17 11.5a2.7 2.7 0 100-5.4M18 19.5c0-2.3-.8-3.9-2.2-4.9"/></svg>',
  sales:'<svg viewBox="0 0 24 24"><path d="M4 19V9M10 19V5M16 19v-6M22 19H2"/></svg>',
  set:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 00.3 1.8l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.6 1.6 0 00-2.7 1.1V21a2 2 0 11-4 0v-.1A1.6 1.6 0 006.5 19.4l-.1.1a2 2 0 11-2.8-2.8l.1-.1A1.6 1.6 0 003 15a2 2 0 010-4 1.6 1.6 0 001.1-2.7l-.1-.1a2 2 0 112.8-2.8l.1.1A1.6 1.6 0 009 4.6V4a2 2 0 014 0v.1A1.6 1.6 0 0017.5 4.6l.1-.1a2 2 0 112.8 2.8l-.1.1A1.6 1.6 0 0021 11a2 2 0 010 4z"/></svg>',
  plus:'<svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>',
  chart:'<svg viewBox="0 0 24 24"><path d="M4 19V5M4 19h16"/><rect x="7.5" y="12" width="3" height="7" rx="1"/><rect x="13" y="8" width="3" height="11" rx="1"/><path d="M6 10l4-4 4 3 5-5"/></svg>',
  tv:'<svg viewBox="0 0 24 24"><rect x="2.5" y="4.5" width="19" height="13" rx="2"/><path d="M8 21h8M12 17.5V21"/></svg>',
  refresh:'<svg viewBox="0 0 24 24"><path d="M20 12a8 8 0 1 1-2.34-5.66"/><path d="M20 4v5h-5"/></svg>',
  exit:'<svg viewBox="0 0 24 24"><path d="M14 4h5a1 1 0 011 1v14a1 1 0 01-1 1h-5"/><path d="M10 17l5-5-5-5M15 12H3"/></svg>',
  power:'<svg viewBox="0 0 24 24"><path d="M12 3v9"/><path d="M6.6 6.6a7.5 7.5 0 1 0 10.8 0"/></svg>',
  sun:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>',   /* 타임라인 점심만(09-20) */
  moon:'<svg viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>',   /* 저녁만 */   /* 종료하기 — 전원 단추 모양(예전엔 축소 아이콘이라 뜻이 안 맞았음, 재아 09-20) */
  search:'<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/></svg>',
  inbox:'<svg viewBox="0 0 24 24"><path d="M4 13l2-8h12l2 8v6H4z"/><path d="M4 13h5l1.5 2h3L15 13h5"/></svg>',
  clock:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>',
  more:'<svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="1.6" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none"/><circle cx="12" cy="19" r="1.6" fill="currentColor" stroke="none"/></svg>',
  cal:'<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M3 10h18M8 3v4M16 3v4"/><circle cx="8.5" cy="14.5" r="1.2" fill="currentColor" stroke="none"/><circle cx="12" cy="14.5" r="1.2" fill="currentColor" stroke="none"/><circle cx="15.5" cy="14.5" r="1.2" fill="currentColor" stroke="none"/></svg>'
};
// 탭 없이 한 화면으로 운영합니다. 설정은 상단 톱니바퀴 버튼으로 엽니다.
// 매출·직원 기능은 비활성화되어 있습니다 (아래 주석 블록 참고).
