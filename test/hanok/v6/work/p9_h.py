# -*- coding: utf-8 -*-
"""v6 8차-H — 테이블은 층 단위로 접기 (재아 결정: 홀은 그날 남는 자리에 앉히므로 테이블을 미리 정하지 않는다)
   · 예약의 테이블 희망은 seatPref "table:<층>" (예 "table:1층"). 옛 "table-any" 는 층 미정 그대로
   · 테이블 예약은 잠정 배정을 하지 않고, 층의 자리 수(테이블 seats 합)와 겹치는 인원으로 '자리 부족' 만 경고
   · 마법사·수정 시트·좌석 배정: 테이블 쪽은 "1층 테이블 / 지하 테이블" 만. 특정 테이블은 수정 시트 '특정 테이블' 에서만
   · 타임라인: 테이블 12줄 → 층 1줄씩(겹치는 예약을 층으로 쌓음, 예약률은 인원/자리수)
   · TV: 테이블 예약은 층 이름만. 공개 뷰에 seat_pref 추가(SQL)
   · 설정 테이블 목록 문구: '자리 수를 세는 근거'"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 헬퍼 ----------
s = R(s, """function joinOf(ids){ return (store().settings.joins||[]).find(g=>sameIds(g.ids, ids)) || null; }""",
"""function joinOf(ids){ return (store().settings.joins||[]).find(g=>sameIds(g.ids, ids)) || null; }
/* ---------- 테이블은 층 단위 (8차-H) ----------
   홀은 그날 남는 자리에 앉히는 곳이라 테이블을 미리 정해도 현장에서 지켜지지 않습니다.
   그래서 예약은 '1층 테이블 / 지하 테이블' 까지만 받고, 시스템은 층의 자리 수(테이블 인원 합)와
   같은 시간에 겹치는 손님 수로 '자리 부족' 만 알립니다. 특정 테이블 배정은 수정 시트에서만(파셜룸 등). */
function isTablePref(p){ return p === "table-any" || p === "hall-any" || /^table:/.test(p || ""); }
function prefFloor(p){ return /^table:/.test(p || "") ? p.slice(6) : null; }
function floorTables(fl){ return (store().settings.rooms || []).filter(t => isTable(t) && (t.floor || "") === (fl || "")); }
/* 예약이 쓰는 테이블 층. 룸이면 undefined, 층 미정 테이블이면 null */
function resFloor(r){
  if(r.roomId){ const x = seatById(r.roomId); return x && isTable(x) ? (x.floor || "") : undefined; }
  if(isTablePref(r.seatPref)) return prefFloor(r.seatPref);
  return undefined;
}
function floorSeats(fl, date, time){
  return floorTables(fl).filter(t => !(date && time && blockedAt(t, date, time))).reduce((a, t) => a + (t.seats || 4), 0);
}
/* 그 시각에 그 층 테이블에 앉아 있는(겹치는) 손님 수 */
function floorLoad(date, time, fl, excludeId){
  const t = toMin(time); let sum = 0;
  store().reservations.forEach(r => {
    if(r.date !== date || !holdsSeat(r) || r.id === excludeId) return;
    const f = resFloor(r); if(f === undefined || (f || "") !== (fl || "")) return;
    const rt = toMin(r.time);
    const overlap = rt <= t ? rt + stayOf(r) > t : t + stayMinAt(date, time) > rt;
    if(overlap) sum += pplOf(r);
  });
  return sum;
}
function floorLeft(date, time, fl, excludeId){ return floorSeats(fl, date, time) - floorLoad(date, time, fl, excludeId); }
function floorLabel(fl){ return `${fl || ""} 테이블`.trim(); }""")

# ---------- 라벨 ----------
s = R(s, """  if(seat==="hall-any" || seat==="table-any") return "테이블 중 아무곳";
  if(seat==="room-any") return "룸 중 아무곳";""",
"""  if(seat==="hall-any" || seat==="table-any") return "테이블";
  if(/^table:/.test(seat||"")) return floorLabel(seat.slice(6));
  if(seat==="room-any") return "룸 중 아무곳";""")
s = R(s, """function resSeatLabel(r){ return r.roomId ? seatLabelIds([r.roomId].concat(r.extraIds||[])) : "미배정"; }""",
"""function resSeatLabel(r){
  if(r.roomId) return seatLabelIds([r.roomId].concat(r.extraIds||[]));
  if(isTablePref(r.seatPref)) return seatLabel(r.seatPref);   /* 테이블 예약은 층까지만 — 미배정이 아닙니다 */
  return "미배정";
}
/* 룸 미배정(잠정 포함) 여부 — 테이블 예약은 층이 자리이므로 미배정으로 세지 않습니다 */
function isUnassigned(r){ return !r.roomId && !isTablePref(r.seatPref); }""")

# ---------- 경고: 층 자리 부족 ----------
s = R(s, """  if((r.infants||0) >= pplOf(r) && pplOf(r)>0) out.push("성인 없음");
  if(seat && seat.type==="room"){""",
"""  if((r.infants||0) >= pplOf(r) && pplOf(r)>0) out.push("성인 없음");
  /* 테이블 예약(층 단위): 같은 시간대 손님 수가 그 층 자리 수를 넘으면 */
  if(!seat && isTablePref(r.seatPref) && r.status!=="취소" && prefFloor(r.seatPref) != null){
    if(floorLoad(r.date, r.time, prefFloor(r.seatPref), r.id) + pplOf(r) > floorSeats(prefFloor(r.seatPref), r.date, r.time)) out.push("테이블 자리 부족");
  }
  if(seat && seat.type==="room"){""")
s = R(s, """    "코스 인원 부족": `코스 인원이 성인 수보다 적습니다`
  };""", """    "코스 인원 부족": `코스 인원이 성인 수보다 적습니다`,
    "테이블 자리 부족": (function(){ const fl = prefFloor(rec.seatPref); return `${floorLabel(fl)} 자리가 부족합니다 — 그 시간에 ${floorLoad(rec.date, rec.time, fl, excludeId)}명 앉아 있고 자리는 ${floorSeats(fl, rec.date, rec.time)}석`; })()
  };""")

# ---------- 잠정 배정: 테이블 희망은 건너뜀, 미배정 집계 ----------
s = R(s, """  const targets = s.reservations.filter(r=>r.date===date && holdsSeat(r) && !r.roomId);
  targets.forEach(r=>{ r.tentativeRoomId = null; r.tentativeExtra = []; });""",
"""  const targets = s.reservations.filter(r=>r.date===date && holdsSeat(r) && !r.roomId);
  targets.forEach(r=>{ r.tentativeRoomId = null; r.tentativeExtra = []; });
  /* 테이블 예약은 층 단위라 잠정 배정이 없습니다 — 룸 희망만 */
  targets.splice(0, targets.length, ...targets.filter(r=>!isTablePref(r.seatPref)));""")
s = R(s, """    s.reservations.forEach(function(r){ if(r.date >= today && !r.roomId && holdsSeat(r)) dates[r.date] = 1; });""",
"""    s.reservations.forEach(function(r){ if(r.date >= today && !r.roomId && !isTablePref(r.seatPref) && holdsSeat(r)) dates[r.date] = 1; });""")
s = R(s, """  const unassigned = active.filter(r=>!r.roomId || !seatById(r.roomId)).length;   /* 좌석이 삭제된 예약도(점검 C5) */""",
"""  const unassigned = active.filter(r=>isUnassigned(r) || (r.roomId && !seatById(r.roomId))).length;   /* 좌석이 삭제된 예약도(점검 C5) */""")
s = R(s, """  const list = s.reservations.filter(r=>r.date===d && r.status==="확정" && (!r.roomId || !seatById(r.roomId)))""",
"""  const list = s.reservations.filter(r=>r.date===d && r.status==="확정" && (isUnassigned(r) || (r.roomId && !seatById(r.roomId))))""")
s = R(s, """          unassigned:list.filter(r=>!r.roomId).length};""", """          unassigned:list.filter(isUnassigned).length};""")
s = R(s, """  const tentCount = list.filter(r=>!r.roomId).length;""", """  const tentCount = list.filter(isUnassigned).length;""")
# 예약률 분자: 테이블은 인원 기준(자리 수 대비)
s = R(s, """  const noSeat = r => !seatsOf(r).length && !r.roomId;
  const roomUsed = list.reduce((a,r)=>a + (noSeat(r) ? (r.seatPref==="room-any" ? 1 : 0) : seatsOf(r).filter(isRoomSeat).length) * spanOf(r), 0);
  const hallUsed = list.reduce((a,r)=>a + (noSeat(r) ? (r.seatPref==="room-any" ? 0 : 1) : seatsOf(r).filter(id=>halls.some(x=>x.id===id)).length) * spanOf(r), 0);""",
"""  const noSeat = r => !seatsOf(r).length && !r.roomId;
  const roomUsed = list.reduce((a,r)=>a + (noSeat(r) ? (r.seatPref==="room-any" ? 1 : 0) : seatsOf(r).filter(isRoomSeat).length) * spanOf(r), 0);
  /* 테이블은 층 단위라 '좌석 수' 가 아니라 '손님 수 / 자리 수' 로 — 테이블 예약(층 희망·특정 테이블 모두) 인원 × 시간 */
  const hallUsed = list.reduce((a,r)=>a + (resFloor(r) !== undefined ? pplOf(r) * spanOf(r) : 0), 0);""")
s = R(s, """  const hallT = halls.length;""", """  const hallT = halls.reduce((a,t)=>a+(t.seats||4), 0);   /* 테이블 자리 수 합 (8차-H: 테이블 개수가 아니라 인원) */""")
s = R(s, """  const hallDen = Math.max(0, hallN*span - halls.reduce((a,h)=>a+blockedOf(h),0));""",
"""  const hallDen = Math.max(0, hallN*span - halls.reduce((a,h)=>a+blockedOf(h)*(h.seats||4),0));""")
s = R(s, """  const seatAll = roomN + hallN;        /* 룸 1개 = 좌석 1, 홀은 테이블 1개 = 좌석 1 */""",
"""  const seatAll = roomN + hallN;        /* 룸 1개 = 좌석 1, 테이블은 자리 수(인원) */""")

# ---------- 마법사: 테이블 쪽은 층 카드 ----------
s = R(s, """    WZ.seatKind = cur ? (isTable(cur) ? "table" : "room") : (WZ.seat==="table-any" ? "table" : "room");""",
"""    WZ.seatKind = cur ? (isTable(cur) ? "table" : "room") : (isTablePref(WZ.seat) ? "table" : "room");""")
s = R(s, """  }else{
    const floors = [];
    st.rooms.filter(isTable).forEach(t=>{ if(floors.indexOf(t.floor||"")<0) floors.push(t.floor||""); });
    body = floors.map(fl=>`<div class="lbl" style="margin-top:12px">${esc(fl||"테이블")}</div>
      <div class="sgrid tables">${st.rooms.filter(t=>isTable(t) && (t.floor||"")===fl).map(t=>cell([t.id], t)).join("")}</div>`).join("");
    if(WZ.seatExtra && WZ.seatExtra.length) body += `<p class="f-note">붙인 테이블: <b>${esc(seatLabelIds([WZ.seat].concat(WZ.seatExtra)))}</b></p>`;
  }""",
"""  }else{
    /* 테이블은 층만 고릅니다 — 어느 테이블에 앉을지는 그날 현장에서. 남은 자리는 같은 시간대 겹치는 손님 수로 */
    const floors = tableFloors();
    body = `<div class="sgrid floors">${floors.map(fl=>{
      const key = "table:" + fl, seats = floorSeats(fl, WZ.date, WZ.time), left = WZ.time ? floorLeft(WZ.date, WZ.time, fl) : seats;
      const short = WZ.time && left < total;
      return `<button class="scell ${WZ.seat===key?'on':''} ${short?'warned busy':''}" onclick="wzSeat('${key}')">
        <span class="sn">${esc(floorLabel(fl))}</span>
        <span class="sc">자리 ${seats}석</span>
        <span class="avail ${short?'warn':'free'}">${WZ.time ? (short ? `남은 자리 ${Math.max(0,left)}석 · 부족` : `남은 자리 ${left}석`) : "시간을 먼저"}</span>
      </button>`; }).join("")}</div>`;
  }""")
# 마법사 하단 '좌석 미정' 은 룸 쪽에서만
s = R(s, """    <div class="lbl" style="margin-top:18px">좌석 미정으로 접수</div>
    <div class="sgrid any">
      <button class="scell any ${WZ.seat===(kind==='room'?'room-any':'table-any')?'on':''}" onclick="wzSeat('${kind==='room'?'room-any':'table-any'}')">
        <span class="sn">${kind==='room'?'룸 중 아무곳':'테이블 중 아무곳'}</span><span class="sc">비어 있는 자리에 잠정 배정</span></button>
    </div>`;""",
"""    ${kind==='room' ? `<div class="lbl" style="margin-top:18px">좌석 미정으로 접수</div>
    <div class="sgrid any">
      <button class="scell any ${WZ.seat==='room-any'?'on':''}" onclick="wzSeat('room-any')">
        <span class="sn">룸 중 아무곳</span><span class="sc">비어 있는 방에 잠정 배정</span></button>
    </div>` : `<p class="f-note" style="margin-top:12px">어느 테이블에 앉을지는 당일 현장에서 정합니다. 자리가 부족해도 접수는 됩니다(경고만).</p>`}`;""")
s = R(s, """function wzSeatKind(k){ WZ.seatKind = k; if(WZ.seat && !seatById(WZ.seat)) { /* 다른 갈래의 '미정' 은 지움 */ if(/-any$/.test(WZ.seat)) WZ.seat = null; } render(); }""",
"""function wzSeatKind(k){ WZ.seatKind = k; if(WZ.seat && !seatById(WZ.seat)) { /* 다른 갈래의 '미정'·층 은 지움 */ if(/-any$/.test(WZ.seat) || /^table:/.test(WZ.seat)) WZ.seat = null; } render(); }""")
s = R(s, """  WZ.seatExtra = []; WZ.tentative = null; WZ.tentativeExtra = [];
  if(!["any","hall-any","table-any","room-any"].includes(v)){""",
"""  WZ.seatExtra = []; WZ.tentative = null; WZ.tentativeExtra = [];
  /* 테이블(층) — 자리 수만 보고, 부족해도 알리기만 */
  if(/^table:/.test(v)){
    const fl = v.slice(6), left = floorLeft(WZ.date, WZ.time, fl);
    if(left < people && !await uiConfirm(`${floorLabel(fl)} 자리가 부족합니다`,
      `그 시간대에 ${floorLoad(WZ.date, WZ.time, fl)}명이 앉아 있고 자리는 ${floorSeats(fl, WZ.date, WZ.time)}석입니다.\\n지금 ${people}명 — 남은 자리 ${Math.max(0,left)}석.\\n\\n회전이나 합석으로 감당 가능하면 접수하세요.`,
      {ok:"그래도 접수", cancel:"다시 고르기"})) return;
    WZ.seat = v; wzAutoNext();
    return;
  }
  if(!["any","hall-any","table-any","room-any"].includes(v)){""")
# 등록 시 seatPref 에 층 저장
import re
n = s.count('seatPref: fixed ? null : WZ.seat')
s = s.replace('seatPref: fixed ? null : WZ.seat', 'seatPref: fixed ? null : WZ.seat')   # 형태 확인용(변경 없음)

# ---------- 수정 시트: 좌석 select ----------
s = R(s, """    `<optgroup label="테이블">${st.rooms.filter(isTable).map(r=>opt(r.id, `${esc(r.floor||"")} ${esc(r.name)} · ${roomMin(r)?roomMin(r)+"~":""}${seatMax(r)}인`, !curJoin && f.roomId===r.id)).join("")}</optgroup>` +""",
"""    `<optgroup label="테이블 (층만)">${tableFloors().map(fl=>opt("table:"+fl, `${esc(floorLabel(fl))} · 자리 ${floorSeats(fl)}석`, !f.roomId && f.seatPref==="table:"+fl)).join("")}</optgroup>` +
    `<optgroup label="특정 테이블 (파셜룸 등 꼭 잡아야 할 때)">${st.rooms.filter(isTable).map(r=>opt(r.id, `${esc(r.floor||"")} ${esc(r.name)} · ${roomMin(r)?roomMin(r)+"~":""}${seatMax(r)}인`, !curJoin && f.roomId===r.id)).join("")}</optgroup>` +""")
s = R(s, """  if(j) tmpRes = Object.assign({}, tmpRes, {roomId:j.ids[0], extraIds:j.ids.slice(1)});
  else  tmpRes = Object.assign({}, tmpRes, {roomId:v, extraIds:[]});""",
"""  if(j) tmpRes = Object.assign({}, tmpRes, {roomId:j.ids[0], extraIds:j.ids.slice(1)});
  else if(/^table:/.test(v)) tmpRes = Object.assign({}, tmpRes, {roomId:null, extraIds:[], seatPref:v});   /* 층만 */
  else if(v === "") tmpRes = Object.assign({}, tmpRes, {roomId:null, extraIds:[], seatPref:"room-any"});
  else  tmpRes = Object.assign({}, tmpRes, {roomId:v, extraIds:[]});""")
s = R(s, """    seatPref: f.roomId ? null : (old ? old.seatPref : "table-any"),""",
"""    seatPref: f.roomId ? null : (f.seatPref || (old ? old.seatPref : "room-any")),""")

# ---------- 좌석 배정 시트(sheetMark): 테이블 예약은 층 그대로, 룸 미정만 후보 ----------
s = R(s, """  const seat = r.roomId ? resSeatLabel(r)
             : (r.tentativeRoomId ? `미배정 (${resTentLabel(r)} 잠정)` : "미배정");""",
"""  const seat = r.roomId ? resSeatLabel(r)
             : isTablePref(r.seatPref) ? resSeatLabel(r)
             : (r.tentativeRoomId ? `미배정 (${resTentLabel(r)} 잠정)` : "미배정");""")
s = R(s, """  let seatPick = "";
  if(!r.roomId){
    const kind = r.seatPref==="hall-any" ? "table-any" : (r.seatPref||"any");""",
"""  let seatPick = "";
  if(!r.roomId && isTablePref(r.seatPref)){
    /* 테이블 예약은 층이 곧 자리입니다. 특정 테이블을 꼭 잡아야 하면 '수정' 에서 */
    const fl = prefFloor(r.seatPref);
    seatPick = fl != null ? `<div class="lbl" style="margin:16px 0 8px">테이블 자리</div>
      <p class="f-note">${esc(floorLabel(fl))} · 그 시간대 ${floorLoad(r.date, r.time, fl, r.id) + pplOf(r)}명 / 자리 ${floorSeats(fl, r.date, r.time)}석. 어느 테이블에 앉을지는 당일 현장에서 정합니다. 특정 테이블(파셜룸 등)을 잡으려면 '수정' 에서 고르세요.</p>` : "";
  }else if(!r.roomId){
    const kind = r.seatPref==="hall-any" ? "table-any" : (r.seatPref||"any");""")

# ---------- 타임라인: 층 한 줄 ----------
s = R(s, """  const rooms = st.rooms.filter(isRoom), tables = st.rooms.filter(isTable);
  /* 테이블은 층별로 묶어 머리글 한 줄씩 */
  const floors = []; tables.forEach(t=>{ if(floors.indexOf(t.floor||"")<0) floors.push(t.floor||""); });
  const groupRow = (label) => `<div class="tl-row group"><div class="tl-name"><b>${esc(label)}</b></div><div class="tl-track"></div><div class="tl-rate"></div></div>`;
  const tableRows = floors.map(fl=>groupRow(`${fl||"테이블"} 테이블`) + tables.filter(t=>(t.floor||"")===fl).map(roomRow).join("")).join("");""",
"""  const rooms = st.rooms.filter(isRoom);
  const groupRow = (label) => `<div class="tl-row group"><div class="tl-name"><b>${esc(label)}</b></div><div class="tl-track"></div><div class="tl-rate"></div></div>`;
  /* 테이블은 층 한 줄 — 겹치는 예약을 층(lane)으로 쌓고, 예약률은 손님 수 / 자리 수 (8차-H) */
  const floorRow = (fl)=>{
    const items = list.filter(r=>resFloor(r) !== undefined && (resFloor(r)||"") === (fl||""))
      .sort((a,b)=>a.time.localeCompare(b.time))
      .map(r=>({ r, need:1, s0:toMin(r.time), e0:Math.min(c, toMin(r.time)+stayOf(r)) }));
    let lanes = 1;
    for(const a of items){ let k = 0; for(const b of items) if(a.s0 < b.e0 && b.s0 < a.e0) k++; if(k > lanes) lanes = k; }
    const FL_MAX = 6;
    if(lanes > FL_MAX) lanes = FL_MAX;
    const placed = laneLayout(items, lanes);
    const over = placed.filter(x=>x.lane===null).length;
    const seats = floorSeats(fl);
    const blocks = placed.map(it=>{
      const w = ((it.e0-it.s0)/span)*100, lane = it.lane===null?0:it.lane;
      const past = isBlockPast(it.r, it.s0, date, nowM);
      const bad = resWarn(it.r).length>0, chg = changeTag(it.r);
      const tn = it.r.roomId ? seatLabelIds(seatsOf(it.r)).replace(/ 테이블$/,"") : "";
      return `<button class="blk ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''}" onclick="openMark('${it.r.id}')"
        style="left:${pos(it.s0)}%; width:${w}%; bottom:${lane*LANE+1}px; height:${LANE-2}px"
        title="${esc(it.r.time)} ${esc(it.r.name)} ${pplText(it.r)}${tn?` · ${esc(tn)} 테이블 지정`:""}${chg?` · 오늘 ${esc(chg.label)}`:""}">
        ${chg?`<span class="chg-chip">${blockLabel(it.r)}</span>`:blockLabel(it.r)}${tn?` <small class="tn">${esc(tn)}</small>`:""}</button>`;
    }).join("");
    /* 예약률 = 손님·분 / 자리·분 (영업시간 안으로 자른 것) */
    const used = items.reduce((a,x)=>a+pplOf(x.r)*(x.e0-x.s0),0);
    const rate = seats ? Math.min(100, Math.round(used/(seats*span)*100)) : 0;
    const bands = floorTables(fl).map(blockBands).join("");
    return `<div class="tl-row tbl floor">
      <div class="tl-name"><b>${esc(floorLabel(fl))}</b><small>${seats}석</small></div>
      <div class="tl-track" style="height:${lanes*LANE}px">${layers}${bands}${blocks}${nowLine}</div>
      <div class="tl-rate" style="height:${lanes*LANE}px">${lanes>1
        ? `<span class="rb"><i></i><b>${rate}%</b><i></i></span>` : `<span class="rt">${rate}%</span>`}${over?`<small class="over">초과 ${over}</small>`:""}</div>
    </div>`;
  };
  const unknownFloor = list.some(r=>resFloor(r) === null);
  const tableRows = groupRow("테이블") + tableFloors().map(floorRow).join("") + (unknownFloor ? floorRow(null) : "");""")
# 층 미정(null) 행 이름
s = R(s, """      <div class="tl-name"><b>${esc(floorLabel(fl))}</b><small>${seats}석</small></div>""",
"""      <div class="tl-name"><b>${fl==null?"층 미정":esc(floorLabel(fl))}</b><small>${fl==null?"":seats+"석"}</small></div>""")
s = R(s, """    const seats = floorSeats(fl);
    const blocks = placed.map(it=>{""", """    const seats = fl==null ? 0 : floorSeats(fl);
    const blocks = placed.map(it=>{""")
s = R(s, """    const bands = floorTables(fl).map(blockBands).join("");""", """    const bands = fl==null ? "" : floorTables(fl).map(blockBands).join("");""")

# ---------- TV ----------
s = R(s, """  const list = s.reservations.filter(r=>r.date===today && (r.status==="확정"||r.status==="방문") && r.roomId);""",
"""  /* 룸은 배정된 것만, 테이블은 층 희망(seatPref)까지 — 당일에는 룸 미배정이 없도록 운영한다는 전제 */
  const list = s.reservations.filter(r=>r.date===today && (r.status==="확정"||r.status==="방문") && (r.roomId || isTablePref(r.seatPref)));""")
s = R(s, """    const rows = list.filter(r=>room.ids.indexOf(r.roomId)>=0).sort((a,b)=>a.time.localeCompare(b.time));""",
"""    const rows = list.filter(r=>isT ? (resFloor(r) !== undefined && (resFloor(r)||"") === (room.floorKey||"")) : room.ids.indexOf(r.roomId)>=0).sort((a,b)=>a.time.localeCompare(b.time));""")
s = R(s, """      const tn = isT ? seatsOf(r).map(id=>{ const x = seatById(id); return x ? x.name : ""; }).filter(Boolean).join("+") : "";""",
"""      const tn = "";   /* 손님에게 테이블 번호는 알리지 않습니다 — 층까지만(8차-H) */""")
s = R(s, """  if(/^tables:/.test(id)){ const fl = id.slice(7); return {id, name:`${fl||""} 테이블`.trim(), floor:"", type:"tables", ids:""",
"""  if(/^tables:/.test(id)){ const fl = id.slice(7); return {id, name:`${fl||""} 테이블`.trim(), floor:"", floorKey:fl, type:"tables", ids:""")
# 공개 뷰에서 seatPref 읽기
s = R(s, """      d[k].reservations.push({ id: k + "-" + r.time + "-" + r.name, date: today, time: r.time, name: r.name, people: r.people, roomId: r.room_id, status: r.status, masked""",
"""      d[k].reservations.push({ id: k + "-" + r.time + "-" + r.name, date: today, time: r.time, name: r.name, people: r.people, roomId: r.room_id, seatPref: r.seat_pref || null, status: r.status, masked""")

# ---------- 설정 문구 ----------
s = R(s, """    <div class="subhead" style="margin-top:20px">테이블 <span>이름 있는 테이블 하나가 좌석 하나. 붙일 수 있는 테이블은 '상세'에서</span></div>""",
"""    <div class="subhead" style="margin-top:20px">테이블 <span>예약은 층까지만 받습니다. 여기 목록은 층의 '자리 수' 를 세는 근거 — 테이블 인원을 더한 값이 그 층 자리 수</span></div>""")

# ---------- 시드 문자열은 seed_dev.py 에서 ----------
L.js_check(s)
L.save(s)
print("p9_h ok")
