# -*- coding: utf-8 -*-
"""8차-X — 재아 목록 8차(앞부분): 세션 구조 재설계(점심 경계 하나 + 점심/저녁 접수 마감·점유 룸/테이블, 브레이크면 경계 잠김),
   운영시간 편집(월요일부터·요일 접힘·라스트오더 직접 입력 + '마감 N분 전' 참고), 요약 순서 월금/화토/수일/목공휴,
   설정 검은 버튼 지양, 설정 설명문 → ⓘ 팝업, 보낸 문자 접기, 안내 문자 문안 편집, 관리자 '문자 보내기'(흉내)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ============================================================
# 1. 기본 운영시간표 — sessions[] → sess{}
# ============================================================
s = R(s, """        /* 세션(8차): 접수 가능 시각(from~lastBook)과 점유(stay). stay:"end" 는 until(세션 끝)까지 한 팀만 — 평일 점심은 브레이크까지, 저녁은 영업 종료까지.
           토·일·공휴일 점심은 1시간 50분(브레이크 없음, 15:30 경계). 15:30 이후 접수분은 저녁 세션 규칙 */""",
"""        /* 세션(8차-X): 하루를 '점심 경계'(edge) 하나로 점심/저녁으로 나눕니다. 브레이크가 있는 날은 경계 = 브레이크 시작(자동, 잠김).
           점심·저녁마다 접수 마감(lastBook)과 점유(room/table: "end" = 세션 끝까지 한 팀, 숫자 = 분). 경계가 비면 하루가 한 세션(저녁 규칙).
           토·일·공휴일 점심은 1시간 50분(브레이크 없음, 15:30 경계). 경계 시각(15:30) 자체는 저녁으로 칩니다. 실제 세션 목록은 sessionsOfDay() 가 만듭니다 */""")
WE_SUN = """sessions:[{name:"점심",from:"11:00",lastBook:"15:30",stay:110,   until:"15:30"},{name:"저녁",from:"15:30",lastBook:"18:30",stay:"end",until:"20:30"}]"""
WE_SAT = """sessions:[{name:"점심",from:"11:00",lastBook:"15:30",stay:110,   until:"15:30"},{name:"저녁",from:"15:30",lastBook:"19:30",stay:"end",until:"22:00"}]"""
WD     = """sessions:[{name:"점심",from:"11:00",lastBook:"14:00",stay:"end", until:"15:30"},{name:"저녁",from:"17:00",lastBook:"19:30",stay:"end",until:"22:00"}]"""
s = R(s, WE_SUN, """sess:{edge:"15:30", lunch:{lastBook:"15:30", room:110, table:110}, dinner:{lastBook:"18:30", room:"end", table:"end"}}""", 2)
s = R(s, WE_SAT, """sess:{edge:"15:30", lunch:{lastBook:"15:30", room:110, table:110}, dinner:{lastBook:"19:30", room:"end", table:"end"}}""", 1)
s = R(s, WD,     """sess:{edge:"15:30", lunch:{lastBook:"14:00", room:"end", table:"end"}, dinner:{lastBook:"19:30", room:"end", table:"end"}}""", 5)

# 마이그레이션: 세션이 없는 옛 표 → 기본표, 있으면 sess 로 변환
s = R(s, """      (sch.days||[]).forEach(function(day, i){ if(!day.sessions && def.schedules[0].days[i]) sch.days[i] = deepClone(def.schedules[0].days[i]); });
      if(!sch.holiday || !sch.holiday.sessions) sch.holiday = deepClone(def.schedules[0].holiday);""",
"""      (sch.days||[]).forEach(function(day, i){ if(!day.sess && !day.sessions && def.schedules[0].days[i]) sch.days[i] = deepClone(def.schedules[0].days[i]); });
      if(!sch.holiday || (!sch.holiday.sess && !sch.holiday.sessions)) sch.holiday = deepClone(def.schedules[0].holiday);
      /* 8차-X: 자유 세션 목록(sessions[]) → 점심 경계 + 점심/저녁(sess{}) */
      (sch.days||[]).concat([sch.holiday]).forEach(function(day){ if(day) ensureSess(day); });""")

# ============================================================
# 2. 세션 헬퍼 — sessionsFor 는 sessionsOfDay(hoursFor) 로
# ============================================================
s = R(s, """/* ---------- 세션 (8차) ----------
   그 날의 세션 목록. 운영시간(요일/공휴일/임시)에 sessions 가 있으면 그것, 없으면 옛 필드(lunchUntil·stayHours)로 만든 두 세션 */
function sessionsFor(date){
  const st = store().settings, dh = hoursFor(date);
  if(dh.closed) return [];
  if(dh.sessions && dh.sessions.length) return dh.sessions;
  /* 옛 저장본 — 점심/저녁 두 세션으로 흉내 */
  const lu = st.lunchUntil || "16:00";
  return [{name:"점심", from:dh.open, lastBook:lu, stay:Math.round((st.lunchStayHours||2.5)*60), until:dh.bs||lu},
          {name:"저녁", from:dh.be||lu, lastBook:dh.lo||dh.close, stay:Math.round((st.stayHours||3)*60), until:dh.close}];
}""",
"""/* ---------- 세션 (8차-X) ----------
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
}""")

s = R(s, """/* 그 시각에 앉은 팀이 자리를 쓰는 시간(분).
   stay:"end" = 세션 끝까지(평일 점심은 브레이크까지, 저녁은 영업 종료까지 — 한 자리에 한 팀). 숫자면 그 분만큼.
   좌석 종류(룸/테이블)로는 이제 나누지 않습니다 — 누님 답에 그런 구분이 없었습니다 */
function stayMinAt(date, time, seatId){
  if(!time) return 150;
  const sess = sessionAt(date, time);
  if(!sess){ const st = store().settings; return Math.round((st.stayHours||3)*60); }
  if(sess.stay === "end") return Math.max(30, sessionEnd(date, sess) - toMin(time));
  return Math.max(30, Number(sess.stay) || 150);
}
/* 예약 한 건의 체류 시간 — 배정된(또는 잠정) 좌석 종류에 따라 달라집니다 */
function stayOf(r){ return stayMinAt(r.date, r.time, effSeat(r)); }""",
"""/* 그 시각에 앉은 팀이 자리를 쓰는 시간(분).
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
function stayOf(r){ return stayMinAt(r.date, r.time, effSeat(r) || r.seatPref); }""")
# 층 부하 계산의 새 팀 점유도 테이블 기준
s = R(s, """    const overlap = rt <= t ? rt + stayOf(r) > t : t + stayMinAt(date, time) > rt;
    if(overlap) sum += pplOf(r);""",
"""    const overlap = rt <= t ? rt + stayOf(r) > t : t + stayMinAt(date, time, "table-any") > rt;
    if(overlap) sum += pplOf(r);""")

# 시각 칸: 경계 시각은 저녁에만(점심·저녁에 같은 칸이 두 번 나오던 것), 세션 머리에 룸/테이블 점유
s = R(s, """    for(let t = from; t <= last; t += 30){
      if(dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be)) continue;
      const hmS = minToHM(t);
      const gone = isPastDate || (isToday && t+30 <= nowM);
      const freeRooms""",
"""    /* 다음 세션이 있으면 그 시작(경계) 시각은 다음 세션 칸에만 — 15:30 이 점심·저녁에 둘 다 나와 같이 켜지던 것(재아) */
    const cut = ss.indexOf(se) + 1 < ss.length ? toMin(se.until) : null;
    for(let t = from; t <= last; t += 30){
      if(cut != null && t >= cut) break;
      if(dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be)) continue;
      const hmS = minToHM(t);
      const gone = isPastDate || (isToday && t+30 <= nowM);
      const freeRooms""")
s = R(s, """    if(last % 30 !== 0){
      const hmL = minToHM(last), goneL = isPastDate || (isToday && last <= nowM);""",
"""    if(last % 30 !== 0 && !(cut != null && last >= cut)){
      const hmL = minToHM(last), goneL = isPastDate || (isToday && last <= nowM);""")
s = R(s, """    return `<div class="sess-h2"><b>${esc(se.name)}</b><span class="lbl-note">${se.from}부터 · 접수 ${se.lastBook}까지${se.stay==="end"?" · 세션 끝까지 한 팀":` · ${se.stay}분`}</span></div><div class="hgrid sess">${cells.join("")}</div>`;""",
"""    return `<div class="sess-h2"><b>${esc(se.name)}</b><span class="lbl-note">${se.from}부터 · 접수 ${se.lastBook}까지 · ${stayLabel(se)}</span></div><div class="hgrid sess">${cells.join("")}</div>`;""")
# 좌석 단계의 점유 안내 — 고른 갈래(룸/테이블)에 맞게
s = R(s, """  const stayTxt = WZ.time ? (sess && sess.stay==="end" ? `${sess.name} 세션 끝(${hm(minToHM(sessionEnd(WZ.date, sess)))})까지 한 팀` : `${hmDur(stayMinAt(WZ.date, WZ.time))} 머무는 기준`) : "";""",
"""  const stv = sess ? (kind === "table" && sess.stayTable != null ? sess.stayTable : sess.stay) : null;
  const stayTxt = WZ.time ? (sess && stv==="end" ? `${sess.name} 세션 끝(${hm(minToHM(sessionEnd(WZ.date, sess)))})까지 한 팀` : `${hmDur(stayMinAt(WZ.date, WZ.time, kind === "table" ? "table-any" : null))} 머무는 기준`) : "";""")

# ============================================================
# 3. 운영시간 요약(설정) — 월금/화토/수일/목공휴, 세션 요약, 검은 버튼 지양
# ============================================================
s = R(s, """function sessSummary(d){
  const ss = d.sessions || []; if(!ss.length) return "";
  return `<span class="sch-s">${ss.map(se=>`${esc(se.name)} 접수 ~${esc(se.lastBook)}${se.stay==="end"?"":` · ${se.stay}분`}`).join(" · ")}</span>`;
}""",
"""function sessSummary(d){
  const ss = sessionsOfDay(d); if(!ss.length) return "";
  const f = v => v === "end" ? "끝까지" : `${v||110}분`;
  return `<span class="sch-s">${ss.map(se=>`${esc(se.name)} 접수 ~${esc(se.lastBook)} (룸 ${f(se.stay)} · 테이블 ${f(se.stayTable)})`).join(" · ")}</span>`;
}""")
s = R(s, """          ${(sc.days||[]).map((d,i)=>`<span class="sch-d"><b>${DOWN[i]}</b>""",
"""          ${[1,2,3,4,5,6,0].map(i=>({d:(sc.days||[])[i], i})).filter(x=>x.d).map(({d,i})=>`<span class="sch-d"><b>${DOWN[i]}</b>""")
s = R(s, """      <button class="btn primary" onclick="openSchedule(null)">운영시간 수정</button>""",
         """      <button class="btn" onclick="openSchedule(null)">운영시간 수정</button>""")
for old in ["""<button class="btn primary" onclick="addHoliday()">공휴일 추가</button>""",
            """<button class="btn primary" onclick="addRoom('room')">룸 추가</button>""",
            """<button class="btn primary" onclick="addRoom('table')">테이블 추가</button>""",
            """<button class="btn primary" onclick="addJoin()">합침 추가</button>""",
            """<button class="btn primary" onclick="addCourseRow()">＋ 행 추가</button>""",
            """<button class="btn primary" onclick="addSource()">추가</button>"""]:
    s = R(s, old, old.replace("btn primary", "btn"))
# 요약 격자: 두 열일 때 세로로 채워 월금/화토/수일/목공휴
s = R(s, """@media (min-width:700px){
  .sch-days{grid-template-columns:1fr 1fr}
}""",
"""@media (min-width:700px){
  /* 8차-X(재아): 월·금 / 화·토 / 수·일 / 목·공휴 — 한 열에 네 칸씩 세로로 채웁니다(8칸 고정) */
  .sch-days{grid-template-columns:1fr 1fr; grid-auto-flow:column; grid-template-rows:repeat(4,auto)}
}""")

# ============================================================
# 4. 운영시간 편집 시트 — 월요일부터 · 접힘 · 라스트오더 참고 · 점심 경계
# ============================================================
old_rows = s[s.index("/* 세션 표 한 줄 — 이름 · 시작 · 접수 마감 · 점유(끝까지 / 분) · 끝 */"):s.index("function dayOf(i){")]
new_rows = r'''/* 운영시간 편집(8차-X, 재아) — 월요일부터, 요일 카드는 접혀 있고 눌러서 폅니다.
   세션은 '점심 경계' 하나 + 점심/저녁 접수 마감·점유(룸/테이블 따로). 브레이크가 있으면 경계는 브레이크 시작으로 잠깁니다.
   라스트오더는 직접 입력하고 옆에 '마감 N분 전' 을 참고로만 보여 줍니다(자동 버튼 삭제) */
function stayBox(i, seg, k, label){
  const v = dayOf(i).sess[seg][k];
  return `<div class="sf"><span>${label}</span><span class="sess-stay"><label class="chk"><input type="checkbox" ${v==="end"?"checked":""} onchange="setSessV(${i},'${seg}','${k}',this.checked?'end':110)"><span>끝까지</span></label>
    <input type="number" min="30" step="10" value="${v==="end"?"":(v||110)}" ${v==="end"?"disabled":""} onchange="setSessV(${i},'${seg}','${k}',parseInt(this.value)||110)"><small>분</small></span></div>`;
}
function segBox(i, seg, title, note){
  return `<div class="sess-r two">
    <div class="sf full"><b>${title}</b><span class="lbl-note">${esc(note)}</span></div>
    <div class="sf"><span>접수 마감</span><input type="time" value="${dayOf(i).sess[seg].lastBook||""}" onchange="setSessV(${i},'${seg}','lastBook',this.value)"></div>
    ${stayBox(i, seg, "room", "점유 · 룸")}
    ${stayBox(i, seg, "table", "점유 · 테이블")}
  </div>`;
}
function setSessV(i, seg, k, v){ dayOf(i).sess[seg][k] = v; render(); }
function setEdge(i, v){ dayOf(i).sess.edge = v; render(); }
function toggleEdge(i){ const x = dayOf(i).sess; x.edge = x.edge === "" ? "15:30" : ""; render(); }
function toggleSchedDay(key){ const d = view.schedDraft; d.open = d.open || {}; d.open[key] = !d.open[key]; render(); }
function sheetSchedule(){
  const d = view.schedDraft;
  d.open = d.open || {};
  const dayBlock = (x, i, label, cls) => {
    ensureSess(x);
    const key = String(i), isOpen = !!d.open[key];
    const edge = x.bs ? x.bs : (x.sess.edge || "");
    const loRef = x.lo ? `마감 ${hmDur(Math.max(0, toMin(x.close) - toMin(x.lo)))} 전` : "";
    const sum = `${esc(x.open)} ~ ${esc(x.close)}${x.bs?` · 브레이크 ${esc(x.bs)} ~ ${esc(x.be)}`:""}${x.lo?` · 라스트오더 ${esc(x.lo)}`:""}`;
    return `<div class="dayrow ${cls||''} ${isOpen?'on':''}">
      <button class="dr-h" onclick="toggleSchedDay('${key}')"><b>${label}</b><span class="dr-sum">${sum}</span><span class="fh-i">${isOpen?"▲":"▼"}</span></button>
      ${isOpen ? `<div class="dr-in">
        <label><span>영업</span>
          <input type="time" value="${x.open}" onchange="setDay(${i},'open',this.value)">
          <em>~</em>
          <input type="time" value="${x.close}" onchange="setDay(${i},'close',this.value)"></label>
        <label><span>브레이크</span>
          <input type="time" value="${x.bs||""}" ${x.bs?"":"disabled"} onchange="setDay(${i},'bs',this.value)">
          <em>~</em>
          <input type="time" value="${x.be||""}" ${x.bs?"":"disabled"} onchange="setDay(${i},'be',this.value)"></label>
        <label class="chk"><input type="checkbox" ${x.bs?"":"checked"} onchange="toggleBreakDay(${i})">
          <span>브레이크타임 없음</span></label>
        <label><span>라스트오더</span>
          <input type="time" value="${x.lo||""}" ${x.lo?"":"disabled"} onchange="setDay(${i},'lo',this.value)">
          <em class="lo-ref">${loRef}</em></label>
        <label class="chk"><input type="checkbox" ${x.lo?"":"checked"} onchange="toggleLoDay(${i})">
          <span>라스트오더 없음</span></label>
        <label><span>점심 경계</span>
          <input type="time" value="${edge}" ${(x.bs || x.sess.edge === "")?"disabled":""} onchange="setEdge(${i},this.value)">
          <em class="lo-ref">${x.bs ? "브레이크 시작과 같음 (자동)" : edge ? "이 시각부터 저녁" : "하루가 한 세션"}</em></label>
        ${x.bs ? "" : `<label class="chk"><input type="checkbox" ${x.sess.edge===""?"checked":""} onchange="toggleEdge(${i})">
          <span>점심 경계 없음 (하루 한 세션)</span></label>`}
        <div class="sess">
          ${edge ? segBox(i,"lunch","점심", `${x.open} ~ ${edge}`) + segBox(i,"dinner","저녁", `${x.be||edge} ~ ${x.close}`) : segBox(i,"dinner","종일", `${x.open} ~ ${x.close}`)}
        </div>
      </div>` : ""}
    </div>`;
  };
  const rows = [1,2,3,4,5,6,0].map(i=>dayBlock(d.days[i], i, DOW[i], i===0?'sun':i===6?'sat':'')).join("")
             + dayBlock(d.holiday, 7, "공휴일", "sun");
  return `
    ${sheetHead(d.isNew?"운영시간 수정":"운영시간 편집")}
    <p class="f-note" style="margin:-6px 0 12px"><b>점심 경계</b>부터 저녁입니다(브레이크가 있으면 브레이크 시작). <b>접수 마감</b>은 마지막으로 입장을 받는 시각,
      <b>점유 '끝까지'</b>는 그 세션 끝까지 한 자리에 한 팀. 라스트오더는 주방 마감이라 별개입니다.</p>
    <label class="f"><div class="lb">적용 시작일</div>
      <input type="date" value="${d.from}" onchange="setSchedFrom(this.value)">
      <div class="f-note">이 날짜부터 새 시간이 적용됩니다. 그 전 날짜는 이전 설정을 그대로 씁니다.</div>
    </label>
    ${rows}
    <div class="sheet-actions">
      ${!d.isNew && d.from!=="2000-01-01" ? `<button class="btn danger" onclick="delSchedule('${d.from}')">삭제</button>`:""}
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="saveSchedule()">저장</button>
    </div>`;
}
'''
s = s.replace(old_rows, new_rows)
s = R(s, """function autoLO(i){
  const d = dayOf(i);
  d.lo = minToHM(Math.max(0, toMin(d.close) - 80));
  render();
}
""", "")
# 저장할 때 새 모양으로 고정(옛 sessions 제거)
s = R(s, """  st.schedules.push({from:d.from, days:deepClone(d.days), holiday:deepClone(d.holiday)});""",
"""  d.days.forEach(ensureSess); ensureSess(d.holiday);
  st.schedules.push({from:d.from, days:deepClone(d.days), holiday:deepClone(d.holiday)});""")
# CSS — 접히는 요일 머리, 세션 두 칸 표, 라스트오더 참고 글자
s = R(s, """.dr-h{display:flex; align-items:center; gap:var(--s12); margin-bottom:var(--s8)}""",
""".dr-h{display:flex; align-items:center; gap:var(--s12); margin-bottom:0; width:100%; background:none; border:0; padding:0; text-align:left; font:inherit; color:inherit; cursor:pointer}
.dayrow.on .dr-h{margin-bottom:var(--s8)}
.dr-sum{margin-left:auto; font-size:var(--fs-label); color:var(--text-3); text-align:right}
.dr-h .fh-i{flex:none}
.lo-ref{font-style:normal; font-size:var(--fs-label); color:var(--text-3)}""")
s = R(s, """.dr-in .sess-r .sess-stay input[type=number]{width:64px; flex:0 0 auto}""",
""".dr-in .sess-r .sess-stay input[type=number]{width:64px; flex:0 0 auto}
/* 8차-X 세션 표: 점심/저녁 한 덩어리 = 제목 줄 + 접수 마감 · 점유(룸) · 점유(테이블) */
.sess-r.two{grid-template-columns:1fr 1fr 1fr}
.sess-r.two > .sf{grid-column:auto; grid-row:auto}
.sess-r.two > .sf.full{grid-column:1 / -1; flex-direction:row; align-items:baseline; gap:var(--s8)}
.sess-r.two > .sf.full b{font-size:var(--fs-body)}""")

# ============================================================
# 5. 설정 설명문 → ⓘ 팝업
# ============================================================
s = R(s, """/* 설정 화면의 접이식 구역 */
function sec(key, title, extra, inner){""",
"""/* 설정 설명문 → ⓘ 버튼(8차-X, 재아): 항목마다 붙던 설명(.f-note)을 떼어 오른쪽 ⓘ 로 옮기고, 누르면 팝업으로 보여 줍니다.
   · <label class="f"> 안의 설명 → 그 항목 제목(.lb) 오른쪽
   · 홀로 있는 <p class="f-note"> → 바로 앞의 소제목(.subhead)·버튼 줄(.btn-row)·라벨(.lbl) 끝, 없으면 작은 ⓘ 줄
   설명 안의 버튼(linkbtn)·굵은 글씨는 그대로 팝업에 들어갑니다 */
var INFO_NOTES = [];
function infoBtn(html){ INFO_NOTES.push(html); return `<button class="ibtn" type="button" onclick="event.stopPropagation(); showInfo(${INFO_NOTES.length-1})" aria-label="설명">i</button>`; }
function showInfo(i){ const h = INFO_NOTES[i]; if(h == null) return; modalReplace({mode:"alert", title:"설명", html:h, tone:"ok", res:function(){}}); }
function infoize(html){
  html = html.replace(/<label class="f"([^>]*)>([\\s\\S]*?)<\\/label>/g, function(m, attrs, body){
    var notes = [];
    body = body.replace(/<div class="f-note"[^>]*>([\\s\\S]*?)<\\/div>/g, function(_, n){ notes.push(n); return ""; });
    if(!notes.length) return m;
    body = body.replace(/(<div class="lb">)([\\s\\S]*?)(<\\/div>)/, function(_, a, t, b){ return a + t + infoBtn(notes.join("<br><br>")) + b; });
    return '<label class="f"' + attrs + '>' + body + '</label>';
  });
  html = html.replace(/<\\/p>\\s*<p class="f-note"[^>]*>/g, "<br><br>");   /* 붙어 있는 설명 둘은 한 팝업으로 */
  var out = "", re = /<p class="f-note"[^>]*>([\\s\\S]*?)<\\/p>/g, last = 0, m;
  while((m = re.exec(html))){
    var seg = html.slice(last, m.index), btn = infoBtn(m[1]);
    var a = Math.max(seg.lastIndexOf('<div class="subhead"'), seg.lastIndexOf('<div class="btn-row"'), seg.lastIndexOf('<div class="lbl"'));
    var e = a >= 0 ? seg.indexOf("</div>", a) : -1;
    seg = e >= 0 ? seg.slice(0, e) + btn + seg.slice(e) : seg + '<div class="f-info">' + btn + '</div>';
    out += seg; last = re.lastIndex;
  }
  return out + html.slice(last);
}
/* 설정 화면의 접이식 구역 */
function sec(key, title, extra, inner){""")
s = R(s, """      ${open?`<div class="fold-b ${view.foldJust==="s_"+key?'just':''}">${inner}</div>`:""}
    </section>`;
}""",
"""      ${open?`<div class="fold-b ${view.foldJust==="s_"+key?'just':''}">${infoize(inner)}</div>`:""}
    </section>`;
}""")
s = R(s, """function renderSettings(){
  const st = draft();               /* 임시본 — '적용하기'를 눌러야 반영됩니다 */""",
"""function renderSettings(){
  INFO_NOTES = [];                  /* ⓘ 설명은 그릴 때마다 새로 모읍니다 */
  const st = draft();               /* 임시본 — '적용하기'를 눌러야 반영됩니다 */""")
# 팝업이 HTML 설명을 그릴 수 있게
s = R(s, """  const lines = String(m.msg||"").split("\\n").map(l=>""",
"""  const lines = m.html ? `<div class="md-l md-html">${m.html}</div>` : String(m.msg||"").split("\\n").map(l=>""")
s = R(s, """    : `<div class="md-l">${esc(l)}</div>`).join("");
  return `
    <div class="overlay modal-ov" onclick="modalAnswer(false)">""",
"""    : `<div class="md-l">${esc(l)}</div>`).join("");
  return `
    <div class="overlay modal-ov" onclick="modalAnswer(false)">""")
s = R(s, """.linkbtn{background:none; border:none; color:var(--pine); font-weight:700; padding:0; text-decoration:underline}""",
""".linkbtn{background:none; border:none; color:var(--pine); font-weight:700; padding:0; text-decoration:underline}
/* 설정 ⓘ — 설명은 팝업에. 제목 옆에 작게, 누르기엔 충분히(터치 영역은 여백으로) */
.ibtn{display:inline-flex; align-items:center; justify-content:center; width:18px; height:18px; border-radius:50%; border:1px solid var(--text-3); color:var(--text-3);
  background:none; font:italic 700 11px Georgia,serif; margin-left:6px; padding:0; vertical-align:middle; cursor:pointer; flex:none; box-shadow:0 0 0 6px transparent}
.ibtn:hover{color:var(--text); border-color:var(--text)}
.f-info{display:flex; justify-content:flex-end; margin:-4px 0 var(--s8)}
.md-html{white-space:normal; line-height:1.55}
.md-html b{font-weight:700}""")

# ============================================================
# 6. 문자 — 보낸 문자 접기, 문안 편집, 관리자 '문자 보내기'(흉내)
# ============================================================
s = R(s, """  parkingNote:"※ 주차 안내\\n주차장 이용 가능합니다. 주차비 1,000원이며 발렛은 무료입니다."
};""",
"""  parkingNote:"※ 주차 안내\\n주차장 이용 가능합니다. 주차비 1,000원이며 발렛은 무료입니다.",
  /* 문안(8차-X, 재아): 설정에서 고칠 수 있습니다. {매장} {이름} {일시} {인원} {주차} {오늘내일} 자리에 값이 들어갑니다 */
  tplNew:"[ 예약 완료 안내 ]\\n\\n안녕하세요, {매장}입니다.\\n예약확인 문자 드립니다.\\n\\n{이름} 님\\n{일시}\\n{인원}\\n\\n예약해주셔서 감사합니다.",
  tplRemind:"[ 예약 방문 안내 ]\\n\\n{오늘내일} 예약 방문 안내드립니다.\\n\\n{이름} 님\\n{일시}\\n{인원}\\n\\n{주차}\\n\\n시간 변경이 필요하시면 미리 연락 주시기 바랍니다.\\n\\n감사합니다."
};""")
s = L.replace_fn(s, "smsText", r'''function smsText(r, kind, offset, st){
  var c = smsCfg(st), s = st || store();
  var map = { "매장": s.name || "", "이름": r.name || "", "일시": smsWhen(r), "인원": smsPpl(r),
              "주차": (c.parkingNote || "").trim(),
              /* '오늘 / 내일 / 모레' 는 설정값이 아니라 보내는 날과 예약일의 실제 차이로 정합니다 */
              "오늘내일": kind === "접수" ? "" : (smsGapWord(r) || "") };
  var tpl = kind === "접수" ? (c.tplNew || SMS_DEFAULT.tplNew) : (c.tplRemind || SMS_DEFAULT.tplRemind);
  return smsFill(tpl, map);
}
/* 문안의 {자리} 를 채우고, 빈 값 때문에 생긴 앞 공백·겹친 빈 줄을 정리합니다 */
function smsFill(tpl, map){
  var out = String(tpl || "").replace(/\{(매장|이름|일시|인원|주차|오늘내일)\}/g, function(_, k){ return map[k] != null ? map[k] : ""; });
  out = out.replace(/^[ \t]+/mg, "").replace(/\n{3,}/g, "\n\n");
  return out.trim();
}''')
s = L.replace_fn(s, "sheetSmsLog", r'''function sheetSmsLog(){
  const all = smsLog();
  view.smsOpen = view.smsOpen || {};
  /* 8차-X(재아): 전부 접어 두고 누르면 그 문자만 폅니다. 예약은 편 안에서 엽니다 */
  const rows = all.slice(0,200).map(({r,m})=>{
    const d = new Date(m.at);
    const t = isNaN(d) ? "" : `${d.getMonth()+1}/${d.getDate()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
    const key = (r.id || "free") + "|" + m.at, on = !!view.smsOpen[key];
    return `<div class="smsrow ${on?'on':''}">
      <button class="sr-top" onclick="toggleSmsRow('${key}')">
        <span class="sr-t">${esc(t)}</span>
        <span class="sr-k ${m.kind==="접수"?'new':m.kind==="직접"?'free':'rem'}">${esc(m.kind)}${m.resent?" · 재발송":""}</span>
        <span class="sr-n">${esc(r.name)} 님</span>
        <span class="sr-p">${esc(m.to||"번호 없음")}</span>
        <span class="fh-i">${on?"▲":"▼"}</span>
      </button>
      ${on ? `<div class="smsmsg">${esc(m.text)}</div>${r.id ? `<div class="btn-row" style="margin:0 0 8px"><button class="btn sm" onclick="openMark('${r.id}')">예약 열기</button></div>` : ""}` : ""}
    </div>`;
  }).join("");
  return `
    ${sheetHead("보낸 문자")}
    <div class="mockbar">실제로 나간 문자가 아닙니다. 화면 확인용 기록입니다.</div>
    <div class="smsbox">${rows || `<div class="empty">아직 보낸 문자가 없습니다.</div>`}</div>
    <p class="f-note">전체 ${all.length}건 중 ${Math.min(all.length,200)}건 표시. 누르면 내용이 펼쳐집니다.</p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
function toggleSmsRow(key){ view.smsOpen = view.smsOpen || {}; view.smsOpen[key] = !view.smsOpen[key]; render(); }
/* ---------- 관리자 → 문자 보내기(흉내) — 예약과 무관한 임의 문자(재아) ----------
   기록은 매장 설정(smsFreeLog, 최근 50건)에 남겨 다른 기기에서도 '보낸 문자' 에 보입니다 */
function openSmsFree(){ view.form = {type:"smsfree"}; view.smsFree = {to:"", name:"", text:""}; render(); }
function sheetSmsFree(){
  const f = view.smsFree || {to:"", name:"", text:""};
  return `
    ${sheetHead("문자 보내기")}
    <div class="mockbar">지금은 <b>흉내만</b> 냅니다. 실제로 문자가 나가지 않습니다.</div>
    <label class="f"><div class="lb">받는 번호</div><input id="sf-to" type="tel" value="${esc(f.to)}" placeholder="010-0000-0000"></label>
    <label class="f"><div class="lb">받는 분 (선택)</div><input id="sf-name" value="${esc(f.name)}" placeholder="홍길동"></label>
    <label class="f"><div class="lb">내용</div><textarea id="sf-text" rows="7" placeholder="보낼 내용">${esc(f.text)}</textarea></label>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="sendSmsFree()">보내기 (흉내)</button>
    </div>`;
}
async function sendSmsFree(){
  const g = id => { const el = document.getElementById(id); return el ? el.value.trim() : ""; };
  const to = g("sf-to"), name = g("sf-name"), text = g("sf-text");
  view.smsFree = {to, name, text};
  if(!to) return uiAlert("받는 번호를 입력하세요", "", "warn");
  if(!text) return uiAlert("내용을 입력하세요", "", "warn");
  if(!await uiConfirm(`${name ? name + " 님 " : ""}${to} 으로 보낼까요?`, text, {ok:"보내기", tone:"ok"})) return;
  if(readonlyBlock()) return;
  const st = store().settings;
  st.smsFreeLog = [{ at:new Date().toISOString(), to, name, text }].concat(st.smsFreeLog || []).slice(0, 50);
  mirrorDraft("smsFreeLog");
  logEvent("문자 보내기(흉내)", `${to} ${name} ${text.slice(0, 40)}`);
  view.form = null; view.smsFree = null; saveData(); render();
  uiAlert("문자를 보낸 것으로 기록했습니다", "실제 발송은 업체 연동 뒤에 붙습니다.", "ok");
}''')
s = L.replace_fn(s, "smsLog", r'''function smsLog(){
  var s = store(), out = [], i, j;
  for(i = 0; i < s.reservations.length; i++){
    var r = s.reservations[i], log = r.sms || [];
    for(j = 0; j < log.length; j++) out.push({ r:r, m:log[j] });
  }
  /* 관리자가 직접 보낸 문자(예약 없음) */
  var free = (s.settings && s.settings.smsFreeLog) || [];
  for(i = 0; i < free.length; i++) out.push({ r:{ id:null, name:free[i].name || "직접 입력" }, m:{ at:free[i].at, kind:"직접", to:free[i].to, text:free[i].text } });
  out.sort(function(a, b){ return a.m.at < b.m.at ? 1 : a.m.at > b.m.at ? -1 : 0; });
  return out;
}''')
# 시트 등록
s = R(s, """function openSmsLog(){ view.form={type:"smslog"}; render(); }""",
"""function openSmsLog(){ view.form={type:"smslog"}; view.smsOpen = {}; render(); }""")
# 시트 등록
s = R(s, "smslog:sheetSmsLog, rate:sheetRate,", "smslog:sheetSmsLog, smsfree:sheetSmsFree, rate:sheetRate,")
# 관리자 폴드 버튼
s = R(s, """      <button class="btn" onclick="openRate()">예약률 추이</button>
      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>""",
"""      <button class="btn" onclick="openRate()">예약률 추이</button>
      <button class="btn" onclick="openSmsFree()">문자 보내기</button>
      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>""")
# 문안 편집 UI — 미리보기 앞에
s = R(s, """    <div class="subhead">이렇게 나갑니다</div>
    <div class="smsprev">
      <div class="sp-h">접수 문자 <span>예약을 받은 즉시</span></div>""",
"""    <div class="subhead">문안 <span>{매장} {이름} {일시} {인원} {주차} {오늘내일} 자리에 값이 들어갑니다</span></div>
    <label class="f"><div class="lb">접수 문자</div>
      <textarea id="sms-tpl-new" rows="8" onchange="setSms('tplNew',this.value)">${esc(sm.tplNew||SMS_DEFAULT.tplNew)}</textarea>
      <div class="btn-row" style="margin-top:6px"><button class="btn sm" onclick="setSms('tplNew',SMS_DEFAULT.tplNew)">기본 문안으로</button></div></label>
    <label class="f"><div class="lb">재안내 문자</div>
      <textarea id="sms-tpl-rem" rows="10" onchange="setSms('tplRemind',this.value)">${esc(sm.tplRemind||SMS_DEFAULT.tplRemind)}</textarea>
      <div class="btn-row" style="margin-top:6px"><button class="btn sm" onclick="setSms('tplRemind',SMS_DEFAULT.tplRemind)">기본 문안으로</button></div></label>
    <p class="f-note">{주차}는 위 주차 안내가 비어 있으면 그 줄이 통째로 빠집니다. {오늘내일}은 보내는 날 기준으로 “오늘 / 내일 / 모레” 가 들어갑니다.</p>

    <div class="subhead">이렇게 나갑니다</div>
    <div class="smsprev">
      <div class="sp-h">접수 문자 <span>예약을 받은 즉시</span></div>""")
# CSS — 접힌 문자 줄
s = R(s, """.sr-top{display:flex; align-items:center; gap:var(--s8); flex-wrap:wrap; margin-bottom:var(--s4)}""",
""".sr-top{display:flex; align-items:center; gap:var(--s8); flex-wrap:wrap; margin-bottom:0; width:100%; background:none; border:0; padding:0; text-align:left; font:inherit; color:inherit; cursor:pointer}
.smsrow.on .sr-top{margin-bottom:var(--s4)}
.sr-top .fh-i{margin-left:auto}
.sr-k.free{background:var(--surface-2); color:var(--text-2)}""")

L.js_check(s)
L.save(s)
print("p9_x 적용")
