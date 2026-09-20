/* ============================================================
   예약
   ============================================================ */

/* 하루치 요약 — 달력 팝업과 예약 화면에서 함께 씁니다 */
function dayStat(date){
  const s = store(), st = s.settings;
  const h = hoursFor(date);
  const o = toMin(h.open), c = toMin(h.close), span = Math.max(60, c-o);
  /* 자리를 실제로 쓴 예약만 셉니다 (확정 + 방문).
     노쇼와 취소는 자리를 안 쓴 것이므로 예약률에서 빠집니다. */
  const list = s.reservations.filter(r=>r.date===date && holdsSeat(r));
  const people = list.reduce((a,r)=>a+pplOf(r),0);
  const rooms = roomsAt(date).filter(isRoom);            /* 앞날은 예정 좌석 수로 (예약률 분모) */
  const halls = roomsAt(date).filter(isTable);   /* 이름은 옛 것(hall) 그대로 — 스냅샷·호출부 호환. 뜻은 '테이블' */
  const hallT = halls.length;
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
  /* 좌석 하나 = 1 단위. 합쳐 쓰면 좌석 수만큼 */
  /* 자리를 아직 못 잡은 미정 예약(잠정도 없음)도 손님은 오므로 희망 쪽 좌석 1개로 셉니다 — 빠지면 예약률이 실제보다 낮게 보입니다(점검 R10) */
  const noSeat = r => !seatsOf(r).length && !r.roomId;
  const roomUsed = list.reduce((a,r)=>a + (noSeat(r) ? (r.seatPref==="room-any" ? 1 : 0) : seatsOf(r).filter(isRoomSeat).length) * spanOf(r), 0);
  const hallUsed = list.reduce((a,r)=>a + (noSeat(r) ? (r.seatPref==="room-any" ? 0 : 1) : seatsOf(r).filter(id=>halls.some(x=>x.id===id)).length) * spanOf(r), 0);
  /* 사용 중지(blocks)된 시간은 분모에서 뺍니다 — 룸을 잠가 둔 날 예약률이 억울하게 낮아지지 않게.
     분모가 '좌석 수 × 영업시간(분)' 이므로, 잠긴 좌석의 잠긴 시간(영업시간 안으로 자른 것)을 그만큼 뺍니다. 홀은 테이블 수만큼 */
  const blockedOf = seat => blockSpans(seat, date).reduce((a,sp)=>a+Math.max(0, Math.min(c, sp.e)-Math.max(o, sp.s)), 0);
  const roomDen = Math.max(0, roomN*span - rooms.reduce((a,r)=>a+blockedOf(r),0));
  const hallDen = Math.max(0, hallN*span - halls.reduce((a,h)=>a+blockedOf(h),0));
  const clamp = v => Math.max(0, Math.min(100, Math.round(v)));
  const seatAll = roomN + hallN;        /* 룸 1개 = 좌석 1, 테이블 1개 = 좌석 1 */
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
          unassigned:list.filter(isUnassigned).length};
}


/* ---------- 예약 화면 ---------- */

/* ---------- 달력 팝업 (월 단위) ---------- */
function openCal(){ view.calOpen = true; view.calMonth = view.date.slice(0,7); render(); }
function closeCal(){ view.calOpen = false; render(); }
function moveCalMonth(n){
  const [y,m] = view.calMonth.split("-").map(Number);
  const d = new Date(y, m-1+n, 1);
  view.calMonth = d.getFullYear()+"-"+pad(d.getMonth()+1);
  render();
}
function pickCalDate(d, close){
  view.date = d;
  if(close) view.calOpen = false;
  render();
}
function renderCal(){
  const [y,m] = view.calMonth.split("-").map(Number);
  const lead = new Date(y,m-1,1).getDay();
  const lastDay = new Date(y,m,0).getDate();
  const today = todayStr();

  let cells = "";
  for(let i=0;i<lead;i++) cells += `<span class="cday blank"></span>`;
  for(let d=1; d<=lastDay; d++){
    const ds = `${y}-${pad(m)}-${pad(d)}`;
    const st = dayStat(ds);
    const dow = new Date(ds+"T00:00:00").getDay();
    const cls = ["cday", ds===view.date?"sel":"", ds===today?"today":"",
                 dow===0?"sun":dow===6?"sat":""].join(" ");
    const closedDay = hoursFor(ds).closed;
    cells += `<button class="${cls} ${closedDay?'closed':''}" onclick="pickCalDate('${ds}',true)">
      <span class="dn">${d}</span>
      ${closedDay?`<span class="cn none">휴무</span>`:`<span class="cbar"><i style="width:${st.rate}%"></i></span>
        <span class="cn">${st.count}건 <small>(${st.rate}%)</small></span>`}
    </button>`;
  }
  /* 항상 6줄(42칸) — 5줄짜리 달과 6줄짜리 달을 오갈 때 높이가 바뀌어 손이 헛나갔습니다 */
  for(let i=lead+lastDay; i<42; i++) cells += `<span class="cday blank"></span>`;
  return `
    <div class="overlay" onclick="closeCal()">
      <div class="calbox" onclick="event.stopPropagation()">
        <div class="sheet-h">
          <h2>날짜 선택</h2>
          <button class="x" onclick="closeCal()" aria-label="닫기">×</button>
        </div>
        <div class="cal-nav">
          <button class="nav" onclick="moveCalMonth(-1)">◀</button>
          <div class="cal-m">${y}년 ${m}월</div>
          <button class="nav" onclick="moveCalMonth(1)">▶</button>
        </div>
        <div class="cgrid chead">${["일","월","화","수","목","금","토"].map((x,i)=>
          `<span class="chd ${i===0?'sun':i===6?'sat':''}">${x}</span>`).join("")}</div>
        <div class="cgrid">${cells}</div>
        <div class="sheet-actions">
          <button class="btn" onclick="pickCalDate('${todayStr()}',true)">오늘로</button>
          <button class="btn ghost" onclick="closeCal()">닫기</button>
        </div>
      </div>
    </div>`;
}
function setFilter(f){ view.filter=f; render(); }
function moveDate(d){ view.date=shiftDate(view.date,d); render(); }
/* 다른 날을 보다가 오늘로 한 번에 — 화살표를 여러 번 누르거나 달력을 열 필요가 없게 */
/* '오늘' 버튼 — 오늘이 아닐 때만 상단바 오른쪽(새로고침 왼쪽)에. 6차-F 에서 뺐다가 6차-K 에서 되살림, 7차-H 에서 자리·글자 조정 */
function goHomeScreen(){ WZ = null; tmpRes = null; view.form = null; view.calOpen = false; if(view.tab === "settings") return setTab("dash"); render(); }
function goToday(){ view.date = todayStr(); view.calMonth = monthStr(); render(); }
/* '오늘이 아닌 날짜를 보는 중' — 상단바(.topbar.notoday)와 body.notoday 가 같은 조건을 써야 하므로 한 곳에.
   설정 탭은 날짜 개념이 없어 제외. 디스플레이·잠금·인트로는 renderApp 이 renderStore 전에 갈라져 나가므로 여기서도 빼 둡니다 */
function notodayView(){
  /* 마법사가 열려 있으면 검정을 풀어 둡니다 — 다른 날짜를 보다가 등록을 눌러도 입력 화면은 평소 색(재아) */
  return !!view.storeKey && AUTHED && !view.display && !INTRO && !WZ && view.tab!=="settings" && view.date!==todayStr();
}
/* 오늘 기준 가까운 날짜에 이름표 */
function moveMonthDate(n){
  const [y,m,dd] = view.date.split("-").map(Number);
  const last = new Date(y, m-1+n+1, 0).getDate();
  const dt = new Date(y, m-1+n, Math.min(dd,last));
  view.date = todayStr(dt); view.calMonth = view.date.slice(0,7);
  render();
}
/* 취소하려는 시점이 설정한 기준 안이면(당일 등) '노쇼에 해당' 되묻기. 답: "노쇼" | "취소" | null(그만) */
async function askNoshowOnCancel(rec){
  const rule = store().settings.noshowCancelRule || "sameday";   /* 기본 '당일'(누님 09-20). 설정에서 바꿀 수 있음 */
  if(!rec || rec.status === "취소") return "취소";
  /* 노쇼 회피 막기(재아 09-20): 오늘 예약을 내일로 미뤄 두고 다시 취소하면 '당일 취소' 가 아니게 되는 것.
     변동 이력에 '원래 날짜 당일(또는 그 뒤)에 날짜를 미룬' 기록이 있으면 지금 취소해도 당일 취소로 봅니다 */
  const dodged = (rec.changes||[]).some(c => (c.items||[]).some(it => it.k === "date" && it.ra && it.rb && it.rb > it.ra && c.on >= it.ra));
  if(dodged){
    const first = (rec.changes||[]).map(c => (c.items||[]).filter(it => it.k === "date" && it.ra && it.rb && it.rb > it.ra && c.on >= it.ra).map(it => it.ra)[0]).filter(Boolean)[0];
    const r0 = await uiChoice("당일에 날짜를 미룬 뒤의 취소 — 노쇼에 해당합니다", `${rec.name} 손님 · 원래 ${dateLabel(first)} 예약을 그날 ${dateLabel(rec.date)} 로 미뤘다가 취소합니다.
어떻게 처리할까요?`, [["노쇼로 처리","노쇼"],["취소로 처리","취소"]]);
    return r0;
  }
  if(rule === "none") return "취소";
  const now = new Date(), t = new Date(rec.date + "T" + rec.time + ":00");
  const hoursLeft = (t - now) / 3600000;
  const hit = rule === "after" ? hoursLeft <= 0
            : rule === "sameday" ? rec.date === todayStr() || hoursLeft <= 0
            : rule === "day1" ? rec.date <= shiftDate(todayStr(), 1)
            : rule === "day2" ? rec.date <= shiftDate(todayStr(), 2)
            : rule === "hours" ? hoursLeft <= (store().settings.noshowCancelHours || 3)
            : false;
  if(!hit) return "취소";
  const label = {after:"예약 시각이 지난 뒤의 취소", sameday:"당일 취소", day1:"전날부터의 취소", day2:"이틀 전부터의 취소", hours:`${store().settings.noshowCancelHours||3}시간 안의 취소`}[rule];
  const r = await uiChoice(`${label}는 노쇼에 해당합니다`, `${rec.time} ${rec.name} 손님 · ${pplText(rec)}\n어떻게 처리할까요?`, [["노쇼로 처리","노쇼"],["취소로 처리","취소"]]);
  return r;
}
