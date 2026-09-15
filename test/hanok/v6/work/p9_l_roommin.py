# -*- coding: utf-8 -*-
"""8차-L: 룸 인원을 최소(평일) / 최소(주말·공휴일) / 최적 / 최대 로 분리.
   재아: 최소와 최적은 다르고, 평일과 주말 최소도 다르다. 값은 임의(질문 목록) — 최적=지금 값, 주말 최소=최적, 평일 최소=최적-2(2 이상)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

s = R(s, """function roomMin(r){ if(!r) return 0; if(r.minCapacity != null) return r.minCapacity; return isTable(r) ? 0 : Math.max(2,(r.capacity||2)-2); }""",
"""/* 주말·공휴일이면 true (공휴일을 주말로 볼지는 설정) */
function isWeekendDay(date){ if(!date) return false; const dow = new Date(date+"T00:00:00").getDay(); return dow===0 || dow===6 || (store().settings.holidayAsWeekend!==false && isHoliday(date)); }
/* 룸 최소 인원 — 날짜를 주면 주말·공휴일은 minWeekend(있으면). 테이블은 minCapacity 없으면 0 */
function roomMin(r, date){
  if(!r) return 0;
  if(isRoom(r) && date && isWeekendDay(date) && r.minWeekend != null) return r.minWeekend;
  if(r.minCapacity != null) return r.minCapacity;
  return isTable(r) ? 0 : Math.max(2,(r.capacity||2)-2);
}
/* 룸 최적 인원(안내용) — 없으면 주말 최소 */
function roomOpt(r){ if(!r || !isRoom(r)) return 0; return r.optCapacity != null ? r.optCapacity : (r.minWeekend != null ? r.minWeekend : roomMin(r)); }""")
s = R(s, """function seatsMin(ids){
  const st = store().settings;
  const j = (st.joins||[]).find(g=>sameIds(g.ids, ids));
  if(j) return j.min;
  if(ids.length === 1) return roomMin(seatById(ids[0]));
  return 0;
}""", """function seatsMin(ids, date){
  const st = store().settings;
  const j = (st.joins||[]).find(g=>sameIds(g.ids, ids));
  if(j) return j.min;
  if(ids.length === 1) return roomMin(seatById(ids[0]), date);
  return 0;
}""")
# 날짜를 아는 호출부에 date 전달
s = R(s, """    else if(adultCount(pplOf(r), r.infants) < seatsMin(ids)) out.push("최소 인원 미달");""",
         """    else if(adultCount(pplOf(r), r.infants) < seatsMin(ids, r.date)) out.push("최소 인원 미달");""")
s = R(s, """    else if(ad < seatsMin(ids)) out.push(`${label} 최소 인원 ${seatsMin(ids)}명에 못 미칩니다 (지금 ${ad}명)`);""",
         """    else if(ad < seatsMin(ids, rec.date)) out.push(`${label} 최소 인원 ${seatsMin(ids, rec.date)}명에 못 미칩니다 (지금 ${ad}명)`);""")
s = R(s, """  if(adultCount(ppl, r.infants||0) < seatsMin(ids) && !await uiConfirm2(`${label}은 최소 ${seatsMin(ids)}명부터입니다.""",
         """  if(adultCount(ppl, r.infants||0) < seatsMin(ids, r.date) && !await uiConfirm2(`${label}은 최소 ${seatsMin(ids, r.date)}명부터입니다.""")
s = R(s, """    const over = total > seatsMax(ids), under = adults < seatsMin(ids);""",
         """    const over = total > seatsMax(ids), under = adults < seatsMin(ids, WZ.date);""")
s = R(s, """      if(adults < seatsMin(ids)){""", """      if(adults < seatsMin(ids, WZ.date)){""")
s = R(s, """        if(!await uiConfirm(`${label} 최소 인원 미달`, `최소 ${seatsMin(ids)}명부터 받습니다.""",
         """        if(!await uiConfirm(`${label} 최소 인원 미달`, `최소 ${seatsMin(ids, WZ.date)}명부터 받습니다.""")
s = R(s, """      if(cnt < roomMin(room)) out.push(`최소 인원 미달 - ${seatLabel(room.id)} ${roomMin(room)}명부터`);""",
         """      if(cnt < roomMin(room, WZ.date)) out.push(`최소 인원 미달 - ${seatLabel(room.id)} ${roomMin(room, WZ.date)}명부터`);""")
s = R(s, """    const rooms = seats.filter(x=>isRoom(x) && people >= roomMin(x) && people <= seatMax(x));""",
         """    const rooms = seats.filter(x=>isRoom(x) && people >= roomMin(x, date) && people <= seatMax(x));""")
# 마법사 룸 셀 안내: 최소~최대 + 최적
s = R(s, """    const sub = isTable(x) ? `${roomMin(x)?roomMin(x)+"~":""}${seatMax(x)}인${x.note?` · ${esc(x.note)}`:""}` : `${seatsMin(ids)}~${seatsMax(ids)}인`;""",
         """    const sub = isTable(x) ? `${roomMin(x)?roomMin(x)+"~":""}${seatMax(x)}인${x.note?` · ${esc(x.note)}`:""}` : `${seatsMin(ids, WZ.date)}~${seatsMax(ids)}인${ids.length===1 && roomOpt(x) ? ` · 최적 ${roomOpt(x)}` : ""}`;""")
# 설정 룸 행: 평일 최소 / 주말 최소 / 최적 / 최대
s = R(s, """          <span class="s">최적 ${roomMin(r)}명 · 최대 ${r.capacity}명${r.floor?` · ${esc(r.floor)}`:""}${blockSummary(r)}</span></span>
        <button class="numbtn sm" onclick="openNum('minCapacity','${esc(r.name)} 최적(최소) 인원',1,30,{room:'${r.id}'})">최적 ${roomMin(r)}</button>
        <button class="numbtn sm" onclick="openNum('capacity','${esc(r.name)} 최대 인원',1,40,{room:'${r.id}'})">최대 ${r.capacity}</button>""",
"""          <span class="s">평일 ${roomMin(r)}명부터 · 주말 ${r.minWeekend != null ? r.minWeekend : roomMin(r)}명부터 · 최적 ${roomOpt(r)} · 최대 ${r.capacity}${r.floor?` · ${esc(r.floor)}`:""}${blockSummary(r)}</span></span>
        <button class="numbtn sm" onclick="openNum('minCapacity','${esc(r.name)} 평일 최소 인원',1,30,{room:'${r.id}'})">평일 ${roomMin(r)}</button>
        <button class="numbtn sm" onclick="openNum('minWeekend','${esc(r.name)} 주말·공휴일 최소 인원',1,30,{room:'${r.id}'})">주말 ${r.minWeekend != null ? r.minWeekend : roomMin(r)}</button>
        <button class="numbtn sm" onclick="openNum('optCapacity','${esc(r.name)} 최적 인원 (안내용)',1,30,{room:'${r.id}'})">최적 ${roomOpt(r)}</button>
        <button class="numbtn sm" onclick="openNum('capacity','${esc(r.name)} 최대 인원',1,40,{room:'${r.id}'})">최대 ${r.capacity}</button>""")
s = R(s, """    <div class="subhead">룸 <span>최적 인원 = 최소 인원. 그보다 적으면 경고가 뜹니다</span></div>""",
         """    <div class="subhead">룸 <span>최소(평일 / 주말·공휴일)보다 적으면 경고. 최적은 안내용(마법사에 표시)</span></div>""")
s = R(s, """    return r ? (f.key==="minCapacity" ? roomMin(r) : (r[f.key] != null ? r[f.key] : (f.key==="capacity" ? seatMax(r) : f.min))) : f.min;""",
         """    return r ? (f.key==="minCapacity" ? roomMin(r) : f.key==="minWeekend" ? (r.minWeekend != null ? r.minWeekend : roomMin(r)) : f.key==="optCapacity" ? roomOpt(r) : (r[f.key] != null ? r[f.key] : (f.key==="capacity" ? seatMax(r) : f.min))) : f.min;""")
# C4 보정에 주말 최소도
s = R(s, """      if(f.key==="minCapacity" && n.capacity != null && v > seatMax(n)) n.capacity = v;
      if(f.key==="capacity" && n.minCapacity != null && n.minCapacity > v) n.minCapacity = v;""",
"""      if((f.key==="minCapacity" || f.key==="minWeekend" || f.key==="optCapacity") && n.capacity != null && v > seatMax(n)) n.capacity = v;
      if(f.key==="capacity"){ if(n.minCapacity != null && n.minCapacity > v) n.minCapacity = v; if(n.minWeekend != null && n.minWeekend > v) n.minWeekend = v; if(n.optCapacity != null && n.optCapacity > v) n.optCapacity = v; }""")
# 기본 데이터·마이그레이션: 최적=지금 값, 주말 최소=최적, 평일 최소=최적-2(2 이상)
s = R(s, """    if(!st.joins) st.joins = deepClone(def.joins || []);
    st.joins.forEach(""", """    /* 8차-L: 룸 최소를 평일/주말로 나눔. 옛 저장본은 '최소=최적' 하나뿐이라 임의로 나눕니다(누님 질문 목록) */
    (st.rooms || []).forEach(function(r){
      if(!isRoom(r) || r.optCapacity != null) return;
      var opt = r.minCapacity != null ? r.minCapacity : Math.max(2, (r.capacity||2) - 2);
      r.optCapacity = opt; r.minWeekend = opt; r.minCapacity = Math.max(2, opt - 2);
    });
    if(!st.joins) st.joins = deepClone(def.joins || []);
    st.joins.forEach(""")
L.js_check(s)
L.save(s)
print("roommin ok")
