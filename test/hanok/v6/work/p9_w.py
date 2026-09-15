# -*- coding: utf-8 -*-
"""8차-W — 재아 목록 7차: 목록 필터(전체/예정/지난·방문/취소·노쇼), 화면 보정 ±40, 전체화면은 인트로에서, 시각 칸(지난 시간 글자 삭제·마지막 접수 분 칸·밖 시각 중복 제거·건수 삭제),
   7명 이상은 7부터, 좌석 단계는 룸|테이블 먼저 고르고 '아무곳' 카드 삭제(다음 = 미정), 룸 합침 전부 표시, 나눠 앉기 결과가 붙일 수 있는 짝이면 나눔 아님"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 목록 필터 ----------
s = R(s, """  const filters = ["전체",...STATUS].map(f=>{
    const n = f==="전체" ? s.reservations.filter(r=>r.date===date).length
                         : s.reservations.filter(r=>r.date===date && r.status===f).length;
    return `<button class="${view.filter===f?'on':''}" onclick="setFilter('${f}')">${f} ${n}</button>`;
  }).join("");
  if(view.filter!=="전체") day = day.filter(r=>r.status===view.filter);""",
"""  /* 8차-W(재아): 전체 / 예정(아직 안 온 확정) / 지난·방문(1시간 지난 확정 + 방문) / 취소·노쇼 */
  const nowM0 = toMin(nowHM()), isToday0 = date === todayStr();
  const isPastRes = r => r.date < todayStr() || (isToday0 && toMin(r.time) + 60 < nowM0);
  const GROUPS = { "전체": r=>true, "예정": r=>r.status==="확정" && !isPastRes(r), "지난·방문": r=>r.status==="방문" || (r.status==="확정" && isPastRes(r)), "취소·노쇼": r=>r.status==="취소" || r.status==="노쇼" };
  if(!GROUPS[view.filter]) view.filter = "전체";
  const filters = Object.keys(GROUPS).map(f=>{
    const n = s.reservations.filter(r=>r.date===date && GROUPS[f](r)).length;
    return `<button class="${view.filter===f?'on':''}" onclick="setFilter('${f}')">${f} ${n}</button>`;
  }).join("");
  if(view.filter!=="전체") day = day.filter(GROUPS[view.filter]);""")

# ---------- 화면 보정 ±40 ----------
s = R(s, """function setZoomAdj(d){ DATA._ui = DATA._ui || {}; DATA._ui.zoomAdj = Math.max(-20, Math.min(20, (DATA._ui.zoomAdj||0) + d)); uiSave(); applyTheme(); render(); }""",
         """function setZoomAdj(d){ DATA._ui = DATA._ui || {}; DATA._ui.zoomAdj = Math.max(-40, Math.min(40, (DATA._ui.zoomAdj||0) + d)); uiSave(); applyTheme(); render(); }""")
s = R(s, """  if(DATA && DATA._ui && typeof DATA._ui.zoom === "number" && typeof DATA._ui.zoomAdj !== "number"){ DATA._ui.zoomAdj = Math.max(-20, Math.min(20, DATA._ui.zoom - 100)); delete DATA._ui.zoom; uiSave(); }""",
         """  if(DATA && DATA._ui && typeof DATA._ui.zoom === "number" && typeof DATA._ui.zoomAdj !== "number"){ DATA._ui.zoomAdj = Math.max(-40, Math.min(40, DATA._ui.zoom - 100)); delete DATA._ui.zoom; uiSave(); }""")

# ---------- 전체화면: PIN 마지막 숫자가 아니라 인트로가 뜰 때(로그인 통과 뒤). 크롬은 손짓 뒤 몇 초 안이면 허락합니다 ----------
s = R(s, """  if(PIN_BUF.length===4) tryFullscreen();   /* 마지막 숫자를 누르는 손짓에 얹어야 브라우저가 허락합니다 */""", "")
s = R(s, """function startIntro(){
  INTRO = { n:0 };""", """function startIntro(){
  tryFullscreen();   /* 로그인 통과 → 인트로에서 전체화면(재아). PIN 을 누른 손짓 직후라 허락됩니다 */
  INTRO = { n:0 };""")

# ---------- 시각 칸 ----------
s = R(s, """        <span class="hn">${gone?"지난 시간":(people?`룸 ${freeRooms} · ${tTxt}`:(cnt?`${cnt}건`:"&nbsp;"))}</span>
      </button>`);
    }""", """        <span class="hn">${people?`룸 ${freeRooms} · ${tTxt}`:"&nbsp;"}</span>
      </button>`);
    }
    /* 접수 마감이 30분 단위가 아니면(예 19:50) 그 마지막 시각 칸을 하나 더 — 전화로 "몇 시까지 되나요" 에 바로 답하게(재아) */
    if(last % 30 !== 0){
      const hmL = minToHM(last), goneL = isPastDate || (isToday && last <= nowM);
      cells.push(`<button class="hcell big last ${curT===last?'on':''} ${goneL?'gone':''}" onclick="${ctx.pick}(${last})">
        <span class="hh">${hm(hmL).replace(/^(오전|오후) /,"")}</span><span class="ap">마지막</span><span class="hn">접수 마감 시각</span></button>`);
    }""")
# 밖 시각: 세션 칸에 있는 시각은 빼고, 건수 표시 삭제
s = R(s, """  const slotCells = slots.map(t=>{
    const h = Math.floor(t/60), m = t%60;
    const n = s.reservations.filter(r=>r.date===WZ.date && r.status==="확정" && Math.floor(toMin(r.time)/30)*30===t).length;""",
"""  /* 세션 칸에 이미 있는 시각은 여기서 뺍니다 — '접수 시간 밖' 은 나머지만 */
  const inSess = {}; sessionsFor(WZ.date).forEach(se=>{ for(let t = toMin(se.from); t <= toMin(se.lastBook); t += 30) inSess[t] = 1; });
  const slotCells = slots.filter(t=>!inSess[t] || (dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be))).map(t=>{
    const h = Math.floor(t/60), m = t%60;
    const n = 0;""")
s = R(s, """           :gone?`<span class="hn muted2">지난 시간</span>`
           :(n?`<span class="hn">${n}건</span>`:`<span class="hn">&nbsp;</span>`)}""", """           :`<span class="hn">&nbsp;</span>`}""")
# 마법사 wzPickSlot 가 분 단위 시각(19:50)을 받으면 그대로
s = R(s, """function wzPickSlot(t){ WZ.time = minToHM(t); render(); }""", """function wzPickSlot(t){ WZ.time = minToHM(t); render(); }   /* 마지막 접수 칸(19:50)처럼 30분 단위가 아닌 값도 그대로 — 분 레일이 자동으로 +20 위치 */""")

# ---------- 7명 이상은 7부터 ----------
s = R(s, """function wzCustom(){ WZ.customPeople=true; if(!WZ.people) WZ.people=7; render(); }""", """function wzCustom(){ WZ.customPeople=true; if(!WZ.people || WZ.people < 7) WZ.people=7; render(); }   /* 6명을 눌러 뒀어도 7부터(재아) */""")

# ---------- 좌석 단계: 룸|테이블 먼저, '아무곳' 카드 삭제, 다음 = 미정 ----------
s = R(s, """  if(!WZ.seatKind){
    /* 이미 고른 좌석이 있으면 그 종류, 없으면 인원으로 추정(룸 최소 4 이상이면 룸) */
    const cur = seatById(WZ.seat) || (st.joins||[]).find(j=>j.id===WZ.seat);
    WZ.seatKind = cur ? (isTable(cur) ? "table" : "room") : (isTablePref(WZ.seat) ? "table" : "room");
  }
  const kind = WZ.seatKind;""", """  if(!WZ.seatKind && WZ.seat){
    const cur = seatById(WZ.seat) || (st.joins||[]).find(j=>j.id===WZ.seat);
    WZ.seatKind = cur ? (isTable(cur) ? "table" : "room") : (isTablePref(WZ.seat) ? "table" : "room");
  }
  const kind = WZ.seatKind;   /* 8차-W(재아): 기본값 없음 — 룸/테이블을 먼저 고르면 그때 좌석이 보입니다 */""")
s = R(s, """  let body = "";
  if(kind === "room"){
    const rooms = st.rooms.filter(isRoom);
    const joins = (st.joins||[]).filter(j=>total >= j.min && total <= j.max);""", """  let body = "";
  if(kind === "room"){
    const rooms = st.rooms.filter(isRoom);
    const joins = (st.joins||[]);   /* 인원이 안 맞아도 다 보여 주고 '인원 부족/초과' 로 표시(재아: 합침이 안 보였음) */""")
s = R(s, """    body = `<div class="sgrid floors">
      <button class="scell ${WZ.seat==='table-any'?'on':''} ${anyBad?'warned busy':''}" onclick="wzSeat('table-any')">
        <span class="sn">층 상관없음</span><span class="sc">사장님 순서대로 자동</span>
        <span class="avail ${anyBad?'warn':'free'}">${!anyFit ? "시간을 먼저" : anyFit.state==="ok" ? "자리 있음" : anyFit.state==="split" ? "나눠 앉기" : "자리 없음"}</span></button>
      ${floors.map(fl=>{""", """    body = `<div class="sgrid floors">
      ${floors.map(fl=>{""")
s = R(s, """    ${kind==='room' ? `<div class="lbl" style="margin-top:18px">좌석 미정으로 접수</div>
    <div class="sgrid any">
      <button class="scell any ${WZ.seat==='room-any'?'on':''}" onclick="wzSeat('room-any')">
        <span class="sn">룸 중 아무곳</span><span class="sc">비어 있는 방에 잠정 배정</span></button>
    </div>` : `<p class="f-note" style="margin-top:12px">어느 테이블에 앉을지는 당일 현장에서 정합니다. 자리가 부족해도 접수는 됩니다(경고만).</p>`}`;""",
"""    ${!kind ? `<div class="empty">룸 예약인지 테이블 예약인지 먼저 고르세요.</div>` : kind==='room' ? `<p class="f-note" style="margin-top:12px">방을 안 고르고 <b>다음</b>을 누르면 '룸 미정' 으로 접수돼 빈 방에 잠정 배정됩니다.</p>` : `<p class="f-note" style="margin-top:12px">층을 안 고르고 <b>다음</b>을 누르면 층 상관없이 사장님 순서로 잡습니다. 어느 테이블인지는 당일 현장에서.</p>`}`;""")
# 룸|테이블 세그먼트 옆에 '자리 없음' 경고
s = R(s, """    <div class="seg seatkind">
      <button class="${kind==='room'?'on':''}" onclick="wzSeatKind('room')">룸 예약</button>
      <button class="${kind==='table'?'on':''}" onclick="wzSeatKind('table')">테이블 예약</button>
    </div>""", """    ${(()=>{ if(!WZ.time) return `<div class="seg seatkind"><button class="${kind==='room'?'on':''}" onclick="wzSeatKind('room')">룸 예약</button><button class="${kind==='table'?'on':''}" onclick="wzSeatKind('table')">테이블 예약</button></div>`;
      /* 고르는 순간부터 자리 여부를 — 종류 버튼에 '자리 없음' 을 붙입니다(재아). 룸: 이 인원이 앉을 빈 룸 하나라도, 테이블: 층 무관 */
      const roomOk = !!findSeat({date:WZ.date, time:WZ.time, people:total, kind:"room-any"});
      const tf = floorFit(null, WZ.date, WZ.time, total);
      return `<div class="seg seatkind">
        <button class="${kind==='room'?'on':''} ${roomOk?'':'warned'}" onclick="wzSeatKind('room')">룸 예약${roomOk?"":" · 빈 방 없음"}</button>
        <button class="${kind==='table'?'on':''} ${tf.state==='none'?'warned':''}" onclick="wzSeatKind('table')">테이블 예약${tf.state==='none'?" · 자리 없음":tf.state==='split'?" · 나눠 앉기":""}</button>
      </div>`; })()}""")
# 다음 = 미정: 3단계 통과 조건은 seatKind 만 있으면 됨, 넘어갈 때 seat 없으면 room-any/table-any 로
s = R(s, """  if(WZ.step===3) return !!WZ.seat;""", """  if(WZ.step===3) return !!(WZ.seat || WZ.seatKind);""")
s = R(s, """  if(n > WZ.step && !wzCanNext()) return; /* 통과 여부를 검사 */""", """  if(n > WZ.step && !wzCanNext()) return; /* 통과 여부를 검사 */
  /* 좌석 단계에서 종류만 고르고 넘어가면 '미정' 으로(재아) — 자리 없으면 확인창은 wzSeat 가 띄웁니다 */
  if(n === 4 && WZ.step === 3 && !WZ.seat && WZ.seatKind){ await wzSeat(WZ.seatKind === "room" ? "room-any" : "table-any"); if(!WZ.seat) return; if(WZ.step === 4) return; }""")
s = R(s, """function wzSeatKind(k){ WZ.seatKind = k; if(WZ.seat && !seatById(WZ.seat)) { /* 다른 갈래의 '미정'·층 은 지움 */ if(/-any$/.test(WZ.seat) || /^table:/.test(WZ.seat)) WZ.seat = null; } render(); }""",
         """function wzSeatKind(k){ WZ.seatKind = k; if(WZ.seat){ const cur = seatById(WZ.seat) || (store().settings.joins||[]).find(j=>j.id===WZ.seat); const isT = cur ? isTable(cur) : isTablePref(WZ.seat); if((k==="room") === !!isT) WZ.seat = null; } render(); }   /* 갈래를 바꾸면 다른 갈래의 선택은 지움 */""")
# wzSeat 의 미정 경로: wzAutoNext 대신 step 4 로 (이미 wzGo 안에서 부름)
s = R(s, """  WZ.tentative = f ? f.id : null; WZ.tentativeExtra = f ? f.extra : [];
  WZ.seat = v; wzAutoNext();
}""", """  WZ.tentative = f ? f.id : null; WZ.tentativeExtra = f ? f.extra : [];
  WZ.seat = v; WZ.step = 4; WZ.maxStep = Math.max(WZ.maxStep||0, 4); render();
}""")

# ---------- 나눠 앉기 결과가 서로 붙일 수 있는 짝이면 나눔 아님(안전장치) ----------
s = R(s, """      if(sum >= people && pick.length > 1) return {id:pick[0].id, extra:pick.slice(1).map(x=>x.id), split:true};""",
"""      if(sum >= people && pick.length > 1){
        /* 골라진 테이블들이 서로 이어져 있으면(한 줄) 나눠 앉는 게 아니라 붙이는 것 */
        const chained = pick.every((x,i)=>i===0 || pick.slice(0,i).some(c=>canJoinTables(c.id, x.id)));
        return {id:pick[0].id, extra:pick.slice(1).map(x=>x.id), split:!chained};
      }""")
L.js_check(s)
L.save(s)
print("p9_w ok")
