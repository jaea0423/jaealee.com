# -*- coding: utf-8 -*-
"""v4 6차 묶음 D (지시서 6) — 예약률 추이의 좌석 수 변동 대응: 날짜별 좌석 수 스냅샷 + 사용 중지 시간을 분모에서 뺌"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# 1. migrate — 없으면 {}
rep("""    for(const arr of ["reservations","staff","attendance","sales","trash"]) d[k][arr] = d[k][arr] || [];
""",
"""    for(const arr of ["reservations","staff","attendance","sales","trash"]) d[k][arr] = d[k][arr] || [];
    d[k].snapshots = d[k].snapshots || {};   /* 날짜별 좌석 수 (takeSnapshot 참고) */
""")

# 2. takeSnapshot — autoCloseDays 앞에
rep("""function autoCloseDays(){
  if(!DATA) return 0;""",
"""/* ---------- 좌석 수 스냅샷 ----------
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
    var hallN = all.filter(function(r){ return r.type === "hall"; })
                   .reduce(function(a, h){ return a + hallTables(h).length; }, 0);
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
  if(!DATA) return 0;""")

# 3. 부르는 곳 — loadData / 1분 타이머(자정 넘김) / 설정 적용
rep("""  fetchIP();
  autoCloseDays();
""",
"""  fetchIP();
  autoCloseDays();
  takeSnapshot();
""")
rep("""setInterval(function(){
  if(!AUTHED || view.display || WZ || view.form || MODAL) return;
  refreshData().then(function(){ render(); });
}, 60000);""",
"""setInterval(function(){
  /* 자정을 넘겼으면 새 날짜의 좌석 수를 남깁니다 (밤새 켜 둔 태블릿·TV). 6차 전에는 자정 처리가 따로 없었습니다 */
  if(SNAP_DAY && todayStr() !== SNAP_DAY) takeSnapshot();
  if(!AUTHED || view.display || WZ || view.form || MODAL) return;
  refreshData().then(function(){ render(); });
}, 60000);""")
rep("""  store().settings = deepClone(view.draft);
  logEvent("설정 변경", "적용");
  saveData(); render();
}""",
"""  store().settings = deepClone(view.draft);
  logEvent("설정 변경", "적용");
  takeSnapshot();   /* 룸·테이블 수가 바뀌었을 수 있으니 오늘 스냅샷을 새로 (내일부터 오늘을 이 수로 계산) */
  saveData(); render();
}""")

# 4. dayStat — 스냅샷 분모 + 사용 중지 시간 빼기
rep("""  const rooms = st.rooms.filter(r=>r.type==="room");
  const halls = st.rooms.filter(r=>r.type==="hall");
  const hallT = halls.reduce((a,h)=>a+hallTables(h).length,0);
  /* 예약이 차지하는 시간을 영업시간 안으로 잘라서 계산합니다.
     (마감 이후 시각의 예약이 음수가 되던 문제를 막습니다) */
  const spanOf = r => {
    const s0 = Math.max(o, toMin(r.time));
    const e0 = Math.min(c, toMin(r.time) + stayOf(r));
    return Math.max(0, e0 - s0);
  };
  const roomUsed = list.filter(r=>rooms.some(x=>x.id===effSeat(r)))
    .reduce((a,r)=>a+spanOf(r),0);
  const hallUsed = list.filter(r=>halls.some(x=>x.id===effSeat(r)))
    .reduce((a,r)=>a+tablesFor(pplOf(r))*spanOf(r),0);
  const clamp = v => Math.max(0, Math.min(100, Math.round(v)));
  const seatAll = rooms.length + hallT;        /* 룸 1개 = 좌석 1, 홀은 테이블 1개 = 좌석 1 */
  /* 룸만·홀만 놓고 본 비율 */
  const roomRate = rooms.length ? clamp(roomUsed/(rooms.length*span)*100) : 0;
  const hallRate = hallT ? clamp(hallUsed/(hallT*span)*100) : 0;
  /* 전체 예약률에서 각자가 차지하는 몫 — 둘을 더하면 전체가 됩니다 */
  const roomShare = seatAll ? roomUsed/(seatAll*span)*100 : 0;
  const hallShare = seatAll ? hallUsed/(seatAll*span)*100 : 0;
  const total = clamp(roomShare + hallShare);
  return {count:list.length, people, roomRate, hallRate, rate:total,
          roomShare:Math.max(0,roomShare), hallShare:Math.max(0,hallShare),
          seatAll, roomSeats:rooms.length, hallSeats:hallT,
          unassigned:list.filter(r=>!r.roomId).length};
}""",
"""  const rooms = st.rooms.filter(r=>r.type==="room");
  const halls = st.rooms.filter(r=>r.type==="hall");
  const hallT = halls.reduce((a,h)=>a+hallTables(h).length,0);
  /* 지난 날짜는 그날의 좌석 수(스냅샷)로, 오늘·앞날은 현재 설정으로 (takeSnapshot 주석 참고).
     스냅샷이 없는 지난 날짜(1년 넘은 것)는 현재 설정으로 계산합니다 */
  const snap = date < todayStr() ? (s.snapshots||{})[date] : null;
  const roomN = snap ? snap.rooms : rooms.length;
  const hallN = snap ? snap.hallTables : hallT;
  /* 예약이 차지하는 시간을 영업시간 안으로 잘라서 계산합니다.
     (마감 이후 시각의 예약이 음수가 되던 문제를 막습니다) */
  const spanOf = r => {
    const s0 = Math.max(o, toMin(r.time));
    const e0 = Math.min(c, toMin(r.time) + stayOf(r));
    return Math.max(0, e0 - s0);
  };
  /* 스냅샷으로 계산하는 지난 날짜에서, 지금은 없는 룸(삭제됨)에 앉았던 예약도 룸 사용으로 셉니다 —
     현재 룸 목록에만 맞추면 그 예약이 분자에서 빠져 예약률이 낮게 나옵니다. 홀은 지우는 일이 없어 홀 목록 기준 */
  const isRoomSeat = id => rooms.some(x=>x.id===id) || (!!snap && !!id && !halls.some(x=>x.id===id));
  const roomUsed = list.filter(r=>isRoomSeat(effSeat(r)))
    .reduce((a,r)=>a+spanOf(r),0);
  const hallUsed = list.filter(r=>halls.some(x=>x.id===effSeat(r)))
    .reduce((a,r)=>a+tablesFor(pplOf(r))*spanOf(r),0);
  /* 사용 중지(blocks)된 시간은 분모에서 뺍니다 — 룸을 잠가 둔 날 예약률이 억울하게 낮아지지 않게.
     분모가 '좌석 수 × 영업시간(분)' 이므로, 잠긴 좌석의 잠긴 시간(영업시간 안으로 자른 것)을 그만큼 뺍니다. 홀은 테이블 수만큼 */
  const blockedOf = seat => blockSpans(seat, date).reduce((a,sp)=>a+Math.max(0, Math.min(c, sp.e)-Math.max(o, sp.s)), 0);
  const roomDen = Math.max(0, roomN*span - rooms.reduce((a,r)=>a+blockedOf(r),0));
  const hallDen = Math.max(0, hallN*span - halls.reduce((a,h)=>a+hallTables(h).length*blockedOf(h),0));
  const clamp = v => Math.max(0, Math.min(100, Math.round(v)));
  const seatAll = roomN + hallN;        /* 룸 1개 = 좌석 1, 홀은 테이블 1개 = 좌석 1 */
  /* 룸만·홀만 놓고 본 비율 */
  const roomRate = roomDen ? clamp(roomUsed/roomDen*100) : 0;
  const hallRate = hallDen ? clamp(hallUsed/hallDen*100) : 0;
  /* 전체 예약률에서 각자가 차지하는 몫 — 둘을 더하면 전체가 됩니다 */
  const den = roomDen + hallDen;
  const roomShare = den ? roomUsed/den*100 : 0;
  const hallShare = den ? hallUsed/den*100 : 0;
  const total = clamp(roomShare + hallShare);
  return {count:list.length, people, roomRate, hallRate, rate:total,
          roomShare:Math.max(0,roomShare), hallShare:Math.max(0,hallShare),
          seatAll, roomSeats:roomN, hallSeats:hallN,
          unassigned:list.filter(r=>!r.roomId).length};
}""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_d 적용 완료")
