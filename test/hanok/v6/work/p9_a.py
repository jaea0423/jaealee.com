# -*- coding: utf-8 -*-
"""v6 8차-A — 좌석·세션 데이터 모양 + 핵심 계산 (누님 답 기준, work/8차_준비.md)
   · 좌석 = 룸(8) + 테이블(12, 개별 이름). '홀' 개념 삭제 → 테이블은 룸처럼 하나의 좌석(type:"table", floor 로 묶음)
   · 합침: 룸 합침 그룹(joins, 중문 탈거) / 테이블 붙임(joinWith). 예약은 roomId(대표) + extraIds(나머지)
   · 세션: 요일별 sessions[{name, from, lastBook, stay(분|"end"), until}] — 점유·접수 마감 계산의 기준
   · 공휴일: 2026~2027 내장표 + 사장 추가/제외
   · 경로: 네이버 / 전화 / 방문 / 기타"""
import sys, os, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()

# ============================================================
# 1. DEFAULT_DATA — 좌석·합침·세션·경로
# ============================================================
a = s.index("      tableSeats:4,       /* 홀 테이블 1개당 기준 인원 */")
b = s.index('      sources:["전화 예약","네이버 예약","기타"],')
b_end = b + len('      sources:["전화 예약","네이버 예약","기타"],')
s = s[:a] + """      /* ---------- 좌석 (8차, 누님 답) ----------
         룸: minCapacity = 최적(=최소) 인원, capacity = 최대. 배열 순서 = 사장님 배정 우선순위(설정에서 ▲▼).
         테이블: 개별 이름. seats = 기본 인원, capacity 가 있으면 그것이 최대(여포 4~5). joinWith = 붙일 수 있는 테이블.
                 '홀' 이라는 묶음은 없습니다 — 층(floor)으로만 묶어 보여 줍니다. 가게에서 '테이블 예약 / 룸 예약' 이라고 부릅니다 */
      rooms:[
        {id:"r1",name:"조조",type:"room",floor:"1층",minCapacity:4,capacity:6},
        {id:"r2",name:"유비",type:"room",floor:"1층",minCapacity:8,capacity:9},
        {id:"r3",name:"장비",type:"room",floor:"1층",minCapacity:6,capacity:7},
        {id:"r4",name:"관우",type:"room",floor:"1층",minCapacity:6,capacity:7},
        {id:"r5",name:"공명",type:"room",floor:"지하",minCapacity:6,capacity:7},
        {id:"r6",name:"주유",type:"room",floor:"지하",minCapacity:6,capacity:7},
        {id:"r7",name:"초선",type:"room",floor:"지하",minCapacity:6,capacity:7},
        {id:"r8",name:"동탁",type:"room",floor:"지하",minCapacity:12,capacity:14},
        {id:"t21", name:"21",  type:"table",floor:"1층",seats:4,joinWith:[]},
        {id:"t22", name:"22",  type:"table",floor:"1층",seats:4,joinWith:[]},
        {id:"t23a",name:"23-4",type:"table",floor:"1층",seats:4,joinWith:["t23b"]},
        {id:"t23b",name:"23-2",type:"table",floor:"1층",seats:2,joinWith:["t23a"]},
        {id:"t24", name:"24",  type:"table",floor:"1층",seats:2,joinWith:[]},
        {id:"t25", name:"25",  type:"table",floor:"1층",seats:2,joinWith:[]},
        {id:"tyb", name:"여포",    type:"table",floor:"지하",seats:4,capacity:5,minCapacity:4,joinWith:[],note:"파셜룸"},
        {id:"thd", name:"하후돈",  type:"table",floor:"지하",seats:4,joinWith:["ths1","ths2","thy","the"]},
        {id:"ths1",name:"하후상-1",type:"table",floor:"지하",seats:4,joinWith:["thd","ths2","thy","the"]},
        {id:"ths2",name:"하후상-2",type:"table",floor:"지하",seats:4,joinWith:["thd","ths1","thy","the"]},
        {id:"thy", name:"하후연",  type:"table",floor:"지하",seats:2,joinWith:["thd","ths1","ths2","the"]},
        {id:"the", name:"하후은",  type:"table",floor:"지하",seats:2,joinWith:["thd","ths1","ths2","thy"]}
      ],
      /* 룸 합침(중문 탈거). 자동(잠정) 배정에는 쓰지 않고 사람이 고를 때만. 원탁은 공간만 합쳐지고 테이블은 나뉘어 손님 확인이 필요 */
      joins:[
        {id:"j1",ids:["r3","r4"],     min:12,max:14,note:"중문 탈거"},
        {id:"j2",ids:["r5","r6"],     min:12,max:14,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"},
        {id:"j3",ids:["r6","r7"],     min:12,max:14,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"},
        {id:"j4",ids:["r5","r6","r7"],min:18,max:21,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"}
      ],
      sources:["네이버 예약","전화 예약","방문","기타"],""" + s[b_end:]

# 세션 — 요일별 운영시간에 sessions 추가 (일·공휴일 / 월~금 / 토)
old_days = s[s.index("        days:[\n          {open:\"11:00\", close:\"20:30\", lo:\"19:10\""):s.index("        /* 공휴일은 토요일과 같게 시작합니다 (설정에서 변경) */")]
s = s.replace(old_days, """        /* 세션(8차): 접수 가능 시각(from~lastBook)과 점유(stay). stay:"end" 는 until(세션 끝)까지 한 팀만 — 평일 점심은 브레이크까지, 저녁은 영업 종료까지.
           토·일·공휴일 점심은 1시간 50분(브레이크 없음, 15:30 경계). 15:30 이후 접수분은 저녁 세션 규칙 */
        days:[
          {open:"11:00", close:"20:30", lo:"19:40", bs:"",      be:"",
           sessions:[{name:"점심",from:"11:00",lastBook:"15:30",stay:110,   until:"15:30"},{name:"저녁",from:"15:30",lastBook:"18:30",stay:"end",until:"20:30"}]},   /* 일 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sessions:[{name:"점심",from:"11:00",lastBook:"14:00",stay:"end", until:"15:30"},{name:"저녁",from:"17:00",lastBook:"19:30",stay:"end",until:"22:00"}]},   /* 월 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sessions:[{name:"점심",from:"11:00",lastBook:"14:00",stay:"end", until:"15:30"},{name:"저녁",from:"17:00",lastBook:"19:30",stay:"end",until:"22:00"}]},   /* 화 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sessions:[{name:"점심",from:"11:00",lastBook:"14:00",stay:"end", until:"15:30"},{name:"저녁",from:"17:00",lastBook:"19:30",stay:"end",until:"22:00"}]},   /* 수 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sessions:[{name:"점심",from:"11:00",lastBook:"14:00",stay:"end", until:"15:30"},{name:"저녁",from:"17:00",lastBook:"19:30",stay:"end",until:"22:00"}]},   /* 목 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sessions:[{name:"점심",from:"11:00",lastBook:"14:00",stay:"end", until:"15:30"},{name:"저녁",from:"17:00",lastBook:"19:30",stay:"end",until:"22:00"}]},   /* 금 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"",      be:"",
           sessions:[{name:"점심",from:"11:00",lastBook:"15:30",stay:110,   until:"15:30"},{name:"저녁",from:"15:30",lastBook:"19:30",stay:"end",until:"22:00"}]}    /* 토 */
        ],
""")
s = L.rep(s, """        /* 공휴일은 토요일과 같게 시작합니다 (설정에서 변경) */
        holiday:{open:"11:00", close:"22:00", lo:"20:40", bs:"", be:""}""",
"""        /* 공휴일은 일요일과 같습니다 (설정에서 변경) */
        holiday:{open:"11:00", close:"20:30", lo:"19:40", bs:"", be:"",
           sessions:[{name:"점심",from:"11:00",lastBook:"15:30",stay:110,   until:"15:30"},{name:"저녁",from:"15:30",lastBook:"18:30",stay:"end",until:"20:30"}]}""")
s = L.rep(s, """      holidays:[],              /* 사장이 직접 등록하는 공휴일 목록 */""",
"""      holidays:[],              /* 사장이 직접 등록하는 공휴일(내장표에 없는 임시공휴일·선거일 등). holidaysOff 는 내장표에서 뺄 날짜 */
      holidaysOff:[],""")

# ============================================================
# 2. 내장 공휴일표
# ============================================================
s = L.rep(s, """function isHoliday(date){
  const st = store().settings;
  return st.holidayMode !== false && (st.holidays||[]).includes(date);
}""",
"""/* 내장 공휴일표 — 인터넷 없이도 돌아야 하고(외부 요청 0), 공공 API 는 키 갱신·장애 위험이 있어 표로 둡니다.
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
/* 그 해의 공휴일 목록(내장 + 사장 추가 − 제외) */
function holidaysOfYear(y){
  const st = store().settings, out = {};
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
}""")

# ============================================================
# 3. 세션 · 체류 · 접수 마감
# ============================================================
s = L.replace_fn(s, "stayMinAt", """/* ---------- 세션 (8차) ----------
   그 날의 세션 목록. 운영시간(요일/공휴일/임시)에 sessions 가 있으면 그것, 없으면 옛 필드(lunchUntil·stayHours)로 만든 두 세션 */
function sessionsFor(date){
  const st = store().settings, dh = hoursFor(date);
  if(dh.closed) return [];
  if(dh.sessions && dh.sessions.length) return dh.sessions;
  /* 옛 저장본 — 점심/저녁 두 세션으로 흉내 */
  const lu = st.lunchUntil || "16:00";
  return [{name:"점심", from:dh.open, lastBook:lu, stay:Math.round((st.lunchStayHours||2.5)*60), until:dh.bs||lu},
          {name:"저녁", from:dh.be||lu, lastBook:dh.lo||dh.close, stay:Math.round((st.stayHours||3)*60), until:dh.close}];
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
   좌석 종류(룸/테이블)로는 이제 나누지 않습니다 — 누님 답에 그런 구분이 없었습니다 */
function stayMinAt(date, time, seatId){
  if(!time) return 150;
  const sess = sessionAt(date, time);
  if(!sess){ const st = store().settings; return Math.round((st.stayHours||3)*60); }
  if(sess.stay === "end") return Math.max(30, sessionEnd(date, sess) - toMin(time));
  return Math.max(30, Number(sess.stay) || 150);
}""")
s = L.replace_fn(s, "stayOf", """function stayOf(r){ return stayMinAt(r.date, r.time, effSeat(r)); }""")
s = L.replace_fn(s, "stayMin", """function stayMin(){ return stayMinAt(view.date || todayStr(), "19:00"); }""")
s = L.replace_fn(s, "lastBookMin", """/* 마지막으로 예약(입장)을 받을 수 있는 시각 — 그 시각이 속한 세션의 lastBook. 라스트오더(주방 마감)와는 다릅니다 */
function lastBookMin(date, time){
  const st = store().settings;
  const d = date || view.date || todayStr();
  const sess = sessionAt(d, time || "19:00");
  if(sess && sess.lastBook) return toMin(sess.lastBook);
  const h = hoursFor(d);
  return h.lo ? toMin(h.lo) : toMin(h.close) - (st.lastBookingBuffer != null ? st.lastBookingBuffer : 60);
}""")
# stayMinAt 호출부 — 날짜 인자 추가
s = L.rep(s, "if(gap >= stayMinAt(time, roomId)) continue;", "if(gap >= stayMinAt(date, time, roomId)) continue;")
s = L.rep(s, "const end = t + stayMinAt(time);", "const end = t + stayMinAt(date, time);")

# ============================================================
# 4. 좌석 헬퍼 (홀 함수 삭제)
# ============================================================
for fn in ["hallZones","hallTables","hallSeatTotal","pickTables","tablesFor"]:
    s = L.remove_fn(s, fn)
s = L.rep(s, """/* 룸 최소 인원 — 지정이 없으면 정원에서 2명 뺀 값 */
function roomMin(r){ return r.minCapacity != null ? r.minCapacity : Math.max(2,(r.capacity||2)-2); }""",
"""/* ---------- 좌석 헬퍼 (8차) ----------
   룸: minCapacity(최적=최소) ~ capacity(최대). 테이블: seats(기본) ~ capacity(있으면, 여포 5) / 최소는 minCapacity(여포 4) 아니면 없음 */
function isRoom(x){ return !!x && x.type === "room"; }
function isTable(x){ return !!x && (x.type === "table" || x.type === "hall"); }
function seatById(id){ const st = store().settings; return (st.rooms||[]).find(x=>x.id===id) || null; }
function roomMin(r){ if(!r) return 0; if(r.minCapacity != null) return r.minCapacity; return isTable(r) ? 0 : Math.max(2,(r.capacity||2)-2); }
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
function seatsMin(ids){
  const st = store().settings;
  const j = (st.joins||[]).find(g=>sameIds(g.ids, ids));
  if(j) return j.min;
  if(ids.length === 1) return roomMin(seatById(ids[0]));
  return 0;
}
function sameIds(a, b){ if(!a || !b || a.length !== b.length) return false; const x = a.slice().sort(), y = b.slice().sort(); return x.every((v,i)=>v===y[i]); }
/* 합침 그룹 찾기 */
function joinOf(ids){ return (store().settings.joins||[]).find(g=>sameIds(g.ids, ids)) || null; }
/* 두 테이블을 붙일 수 있는지(양쪽 다 허용) */
function canJoinTables(a, b){
  const A = seatById(a), B = seatById(b);
  return isTable(A) && isTable(B) && A.floor === B.floor && (A.joinWith||[]).indexOf(b) >= 0 && (B.joinWith||[]).indexOf(a) >= 0;
}""")

# ============================================================
# 5. 좌석 상태 · 이동 가능 · 잠정 배정 · 재계산
# ============================================================
s = L.replace_fn(s, "roomStatus", """/* 좌석(룸이든 테이블이든 하나)을 그 시각에 쓸 수 있는지 — 합쳐 쓰는 예약도 그 좌석을 점유합니다 */
function roomStatus(date, time, roomId, excludeId){
  const s = store();
  if(!time || !roomId) return {state:"free", hits:[], tentative:[], movable:[]};
  const t = toMin(time);
  const all = s.reservations.filter(r =>
    r.date===date && holdsSeat(r) && r.id!==excludeId && usesSeat(r, roomId));
  let state="free"; const near=[], tent=[], movable=[];
  for(const r of all){
    const gap = Math.abs(toMin(r.time)-t);
    /* 겹침 = 둘 중 어느 쪽 점유 시간 안에 상대 시작이 들어오면 */
    if(gap >= Math.max(stayMinAt(date, time, roomId), stayMinAt(date, r.time, roomId))) continue;
    if(r.roomId){
      if(gap < 60){ state="blocked"; }
      else if(state!=="blocked"){ state="warn"; }
      near.push(r);
    }else{
      if(canRelocate(r, roomId)){ movable.push(r); }
      else{
        if(state==="free") state="warn";
        tent.push(r);
      }
    }
  }
  near.sort((a,b)=>a.time.localeCompare(b.time));
  return {state, hits:near, tentative:tent, movable};
}""")
s = L.replace_fn(s, "canRelocate", """/* 좌석 미정 예약을 지금 자리 말고 다른 곳으로 옮길 수 있는지 — 확정 예약만 따집니다(잠정끼리는 비켜줄 수 있음) */
function canRelocate(r, excludeRoomId){
  return !!findSeat({date:r.date, time:r.time, people:pplOf(r), kind:r.seatPref||"any", excludeId:r.id, excludeSeat:excludeRoomId, confirmedOnly:true});
}""")
s = L.replace_fn(s, "reflowTentatives", """/* 좌석 미정 예약들의 잠정 배정을 다시 계산 — 예약이 추가·변경될 때 호출 */
function reflowTentatives(date){
  const s = store();
  const targets = s.reservations.filter(r=>r.date===date && holdsSeat(r) && !r.roomId);
  targets.forEach(r=>{ r.tentativeRoomId = null; r.tentativeExtra = []; });
  targets.sort((a,b)=>a.time.localeCompare(b.time)).forEach(r=>{
    const f = suggestSeatFull(r.date, r.time, pplOf(r), r.seatPref||"any", r.id);
    r.tentativeRoomId = f ? f.id : null; r.tentativeExtra = f && f.extra.length ? f.extra : [];
  });
}""")
for fn in ["hallStatus","hallFits","hallPlan"]:
    s = L.remove_fn(s, fn)
s = L.replace_fn(s, "suggestSeat", """/* ---------- 잠정 배정 (8차) ----------
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
    const rs = roomStatus(date, time, id, o.excludeId);
    if(o.confirmedOnly) return rs.hits.length === 0;
    return rs.state === "free" && !rs.tentative.length && !rs.movable.length;   /* 아무것도 없는 자리 */
  };
  const freeLoose = id => o.excludeSeat !== id && roomStatus(date, time, id, o.excludeId).state === "free";
  const seats = (st.rooms||[]).filter(x=>!blockedAt(x, date, time));
  if(wantRoom){
    const rooms = seats.filter(x=>isRoom(x) && people >= roomMin(x) && people <= seatMax(x));
    for(const r of rooms) if(free(r.id)) return {id:r.id, extra:[]};
    if(!o.confirmedOnly) for(const r of rooms) if(freeLoose(r.id)) return {id:r.id, extra:[]};
  }
  if(wantTable){
    const tables = seats.filter(x=>isTable(x) && people >= roomMin(x) && people <= seatMax(x));
    /* 2명은 4인석을 먼저 (2인석은 좁아 손님이 싫어함). 그 밖에는 남는 자리가 적은 순, 같으면 사장님 순서 */
    const score = x => (people <= 2 && (x.seats||4) >= 4) ? -1 : (seatMax(x) - people);
    const sorted = tables.slice().sort((x,y)=>score(x)-score(y));
    for(const t of sorted) if(free(t.id)) return {id:t.id, extra:[]};
    if(!o.confirmedOnly) for(const t of sorted) if(freeLoose(t.id)) return {id:t.id, extra:[]};
    /* 붙이기 — 비어 있는 테이블 중 서로 붙일 수 있는 조합 */
    const pool = seats.filter(x=>isTable(x) && (x.joinWith||[]).length && (o.confirmedOnly ? free(x.id) : freeLoose(x.id)));
    let best = null;
    const tryCombo = (combo, sum) => {
      if(sum >= people){
        const waste = sum - people;
        if(!best || combo.length < best.combo.length || (combo.length === best.combo.length && waste < best.waste)) best = {combo:combo.slice(), waste};
        return;
      }
      if(combo.length >= 5) return;
      const last = combo[combo.length-1];
      pool.forEach(x=>{
        if(combo.indexOf(x) >= 0) return;
        if(pool.indexOf(x) < pool.indexOf(last)) return;            /* 순서 고정으로 중복 조합 방지 */
        if(!combo.every(c=>canJoinTables(c.id, x.id))) return;
        combo.push(x); tryCombo(combo, sum + (x.seats||4)); combo.pop();
      });
    };
    pool.forEach(x=>tryCombo([x], x.seats||4));
    if(best) return {id:best.combo[0].id, extra:best.combo.slice(1).map(x=>x.id)};
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
}""")

# ============================================================
# 6. migrate — 옛 홀·옛 경로·세션·합침
# ============================================================
s = L.rep(s, """function migrate(d){
  delete d._auth;   /* 7차: PIN 은 서버(Supabase 계정)에만. 옛 저장본에 평문으로 남아 있던 것을 지웁니다 */
  d._logs = d._logs || [];""",
"""function migrate(d){
  delete d._auth;   /* 7차: PIN 은 서버(Supabase 계정)에만. 옛 저장본에 평문으로 남아 있던 것을 지웁니다 */
  d._logs = d._logs || [];
  migrateSeats(d);   /* 8차: 홀(zones) → 테이블 개별, 세션, 경로, 합침 */""")
s = L.rep(s, """/* 저장된 옛 데이터에 새 항목이 없을 때 채워 넣기 */
function migrate(d){""",
"""/* ---------- 8차 좌석 마이그레이션 ----------
   옛 '홀'(type:hall, zones) 은 테이블 개별 목록으로 바꿉니다. 홀에 배정돼 있던 예약은 테이블을 특정할 수 없으니
   미배정(seatPref "table-any") 으로 두고 잠정 배정을 다시 계산합니다. 실서비스에는 옛 데이터가 없어 dev 더미에만 해당 */
function migrateSeats(d){
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var st = d[k] && d[k].settings; if(!st) return;
    var def = DEFAULT_DATA[k].settings;
    var rooms = st.rooms || [];
    var halls = rooms.filter(function(x){ return x.type === "hall"; });
    if(halls.length){
      var hallIds = halls.map(function(x){ return x.id; });
      st.rooms = rooms.filter(function(x){ return x.type !== "hall"; }).concat(deepClone((def.rooms||[]).filter(function(x){ return x.type === "table"; })));
      (d[k].reservations||[]).concat(d[k].trash||[]).forEach(function(r){
        if(hallIds.indexOf(r.roomId) >= 0){ r.roomId = null; r.seatPref = "table-any"; r.legacyHall = true; }
        if(hallIds.indexOf(r.tentativeRoomId) >= 0){ r.tentativeRoomId = null; r.tentativeExtra = []; }
        if(r.seatPref === "hall-any") r.seatPref = "table-any";
      });
    }
    /* 룸 정원이 옛 기본값(조조 4 등)이면 누님 답으로 교체 — 이름이 같은 룸만 */
    (st.rooms||[]).forEach(function(x){
      if(x.type !== "room") return;
      var dr = (def.rooms||[]).find(function(y){ return y.type === "room" && y.name === x.name; });
      if(dr && !x.tuned){ x.minCapacity = dr.minCapacity; x.capacity = dr.capacity; x.floor = dr.floor; }
    });
    if(!st.joins) st.joins = deepClone(def.joins || []);
    if(!st.holidaysOff) st.holidaysOff = [];
    /* 옛 기본 경로 3개 → 새 기본 4개 (사장님이 손댄 목록이면 그대로) */
    if(JSON.stringify(st.sources) === JSON.stringify(["전화 예약","네이버 예약","기타"])) st.sources = def.sources.slice();
    /* 운영시간에 세션이 없으면 요일별 기본 세션을 붙입니다 */
    (st.schedules||[]).forEach(function(sch){
      (sch.days||[]).forEach(function(day, i){ if(!day.sessions && def.schedules[0].days[i]) day.sessions = deepClone(def.schedules[0].days[i].sessions); });
      if(sch.holiday && !sch.holiday.sessions) sch.holiday.sessions = deepClone(def.schedules[0].holiday.sessions);
    });
  });
}
/* 저장된 옛 데이터에 새 항목이 없을 때 채워 넣기 */
function migrate(d){""")

# ============================================================
# 7. takeSnapshot — 테이블 수
# ============================================================
s = L.rep(s, """    var hallN = all.filter(function(r){ return r.type === "hall"; })
                   .reduce(function(a, h){ return a + hallTables(h).length; }, 0);""",
"""    var hallN = all.filter(function(r){ return isTable(r); }).length;   /* 테이블 수 (이름은 옛 것 그대로 — 스냅샷 호환) */""")

L.js_check(s)
L.save(s)
print("p9_a ok")
