# -*- coding: utf-8 -*-
"""v6 8차-C — 화면: 타임라인(테이블 개별 줄·층 머리글·합침 블록), 예약률, TV 좌석표(층별 테이블 칸), 옛 좌석 현황판 정리, 시드 문자열"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()

# ---------- 타임라인: hallRow 삭제, roomRow 를 좌석 공용(seatRow)으로, 층 머리글 ----------
a = s.index("  /* ---------- 홀 ---------- */\n  const hallRow = (hall)=>{")
b = s.index("  /* ---------- 룸 ---------- */\n  const roomRow = (room)=>{")
s = s[:a] + s[b:]
s = L.rep(s, """  const roomRow = (room)=>{
    const items = list.filter(r=>effSeat(r)===room.id)
      .sort((a,b)=>a.time.localeCompare(b.time))
      .map(r=>({ r, need:1, s0:toMin(r.time), e0:Math.min(c, toMin(r.time)+stayOf(r)) }));""",
"""  /* 룸이든 테이블이든 좌석 하나 = 한 줄. 합쳐 쓰는 예약은 관련된 줄마다 블록이 그려지고 '+' 표시가 붙습니다 */
  const roomRow = (room)=>{
    const items = list.filter(r=>usesSeat(r, room.id))
      .sort((a,b)=>a.time.localeCompare(b.time))
      .map(r=>({ r, need:1, s0:toMin(r.time), e0:Math.min(c, toMin(r.time)+stayOf(r)), joined:seatsOf(r).length>1 }));""")
s = L.rep(s, """      return `<button class="blk ${tent?'tent':''} ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''}" onclick="openMark('${it.r.id}')"
        style="left:${pos(it.s0)}%; width:${w}%; bottom:${lane*LANE+1}px; height:${LANE-2}px"
        title="${esc(it.r.time)} ${esc(it.r.name)} ${pplText(it.r)}${tent?' · 잠정':''}${chg?` · 오늘 ${esc(chg.label)}`:""}${bad?` · 경고: ${esc(resWarn(it.r).join(", "))}`:""}">
        ${chg?`<span class="chg-chip">${blockLabel(it.r)}</span>`:blockLabel(it.r)}</button>`;
    }).join("");
    const used = items.reduce((a,x)=>a+(x.e0-x.s0),0);
    const rate = Math.min(100, Math.round(used/span*100));
    return `<div class="tl-row ${blockedAllDay(room,date)?'off-seat':''}">
      <div class="tl-name"><b>${esc(room.name)}</b><small>${roomMin(room)}~${room.capacity}인</small>${blockTag(room)}</div>""",
"""      return `<button class="blk ${tent?'tent':''} ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''} ${it.joined?'joined':''}" onclick="openMark('${it.r.id}')"
        style="left:${pos(it.s0)}%; width:${w}%; bottom:${lane*LANE+1}px; height:${LANE-2}px"
        title="${esc(it.r.time)} ${esc(it.r.name)} ${pplText(it.r)}${it.joined?` · ${esc(it.r.roomId?resSeatLabel(it.r):resTentLabel(it.r))} 합침`:""}${tent?' · 잠정':''}${chg?` · 오늘 ${esc(chg.label)}`:""}${bad?` · 경고: ${esc(resWarn(it.r).join(", "))}`:""}">
        ${it.joined?'<i class="jn">⊕</i>':''}${chg?`<span class="chg-chip">${blockLabel(it.r)}</span>`:blockLabel(it.r)}</button>`;
    }).join("");
    const used = items.reduce((a,x)=>a+(x.e0-x.s0),0);
    const rate = Math.min(100, Math.round(used/span*100));
    const sub = isTable(room) ? `${roomMin(room)?roomMin(room)+"~":""}${seatMax(room)}인` : `${roomMin(room)}~${room.capacity}인`;
    return `<div class="tl-row ${isTable(room)?'tbl':''} ${blockedAllDay(room,date)?'off-seat':''}">
      <div class="tl-name"><b>${esc(room.name)}</b><small>${sub}</small>${blockTag(room)}</div>""")
s = L.rep(s, """  const halls = st.rooms.filter(r=>r.type==="hall");
  const rooms = st.rooms.filter(r=>r.type==="room");

  /* 전체 가동률 */
  const st2 = dayStat(date);""",
"""  const rooms = st.rooms.filter(isRoom), tables = st.rooms.filter(isTable);
  /* 테이블은 층별로 묶어 머리글 한 줄씩 */
  const floors = []; tables.forEach(t=>{ if(floors.indexOf(t.floor||"")<0) floors.push(t.floor||""); });
  const groupRow = (label) => `<div class="tl-row group"><div class="tl-name"><b>${esc(label)}</b></div><div class="tl-track"></div><div class="tl-rate"></div></div>`;
  const tableRows = floors.map(fl=>groupRow(`${fl||"테이블"} 테이블`) + tables.filter(t=>(t.floor||"")===fl).map(roomRow).join("")).join("");

  /* 전체 가동률 */
  const st2 = dayStat(date);""")
s = L.rep(s, """        ${halls.map(hallRow).join("")}
        ${rooms.map(roomRow).join("")}
      </div>""",
"""        ${groupRow("룸")}
        ${rooms.map(roomRow).join("")}
        ${tableRows}
      </div>""")
s = L.rep(s, """        <span class="tl-kpi sub">홀 <b>${hallRate}%</b></span>""",
    """        <span class="tl-kpi sub">테이블 <b>${hallRate}%</b></span>""")
# CSS: 머리글 줄·합침 표시
s = L.rep(s, """/* 누를 수 있는 블록은 button 입니다 — 글자 크기·여백을 .blk 과 같게 다시 적어 button 기본 스타일을 지웁니다 */""",
"""/* 층 머리글 줄('룸', '1층 테이블') — 얇고 회색. 좌석 줄이 20개라 묶음이 없으면 눈이 길을 잃습니다 (8차) */
.tl-row.group{min-height:18px; margin-top:var(--s4)}
.tl-row.group .tl-name{font-size:var(--fs-label); color:var(--text-3); font-weight:700; letter-spacing:.04em; box-shadow:none; background:transparent}
.tl-row.group .tl-track, .tl-row.group .tl-rate{border:none; background:none; height:14px}
/* 합쳐 쓰는 예약 — 관련된 줄마다 같은 블록이 그려지고 ⊕ 표시 */
.blk.joined .jn{font-style:normal; font-size:11px; margin-right:2px; opacity:.9}
/* 누를 수 있는 블록은 button 입니다 — 글자 크기·여백을 .blk 과 같게 다시 적어 button 기본 스타일을 지웁니다 */""")

# ---------- 예약률 (dayStat) ----------
s = L.rep(s, """  const rooms = st.rooms.filter(r=>r.type==="room");
  const halls = st.rooms.filter(r=>r.type==="hall");
  const hallT = halls.reduce((a,h)=>a+hallTables(h).length,0);""",
"""  const rooms = st.rooms.filter(isRoom);
  const halls = st.rooms.filter(isTable);   /* 이름은 옛 것(hall) 그대로 — 스냅샷·호출부 호환. 뜻은 '테이블' */
  const hallT = halls.length;""")
s = L.rep(s, """  const isRoomSeat = id => rooms.some(x=>x.id===id) || (!!snap && !!id && !halls.some(x=>x.id===id));
  const roomUsed = list.filter(r=>isRoomSeat(effSeat(r)))
    .reduce((a,r)=>a+spanOf(r),0);
  const hallUsed = list.filter(r=>halls.some(x=>x.id===effSeat(r)))
    .reduce((a,r)=>a+tablesFor(pplOf(r))*spanOf(r),0);""",
"""  const isRoomSeat = id => rooms.some(x=>x.id===id) || (!!snap && !!id && !halls.some(x=>x.id===id));
  /* 좌석 하나 = 1 단위. 합쳐 쓰면 좌석 수만큼 */
  const roomUsed = list.reduce((a,r)=>a + seatsOf(r).filter(isRoomSeat).length * spanOf(r), 0);
  const hallUsed = list.reduce((a,r)=>a + seatsOf(r).filter(id=>halls.some(x=>x.id===id)).length * spanOf(r), 0);""")
s = L.rep(s, """  const hallDen = Math.max(0, hallN*span - halls.reduce((a,h)=>a+hallTables(h).length*blockedOf(h),0));""",
    """  const hallDen = Math.max(0, hallN*span - halls.reduce((a,h)=>a+blockedOf(h),0));""")

# ---------- 옛 좌석 현황판(renderSeatBoard, 호출 안 됨) — 홀 분기 제거 ----------
a = s.index("  const cell = (r)=>{\n    if(r.type===\"hall\"){")
b = s.index("    const rows = list.filter(x=>effSeat(x)===r.id).sort((a,b)=>a.time.localeCompare(b.time));\n    const tentOnly")
s = s[:a] + "  const cell = (r)=>{\n" + s[b:]
s = L.rep(s, """  const halls = st.rooms.filter(r=>r.type==="hall");
  const rooms = st.rooms.filter(r=>r.type==="room");
  return `
    <div class="sb-grid hall">${halls.map(cell).join("")}</div>
    <div class="sb-grid">${rooms.map(cell).join("")}</div>""",
"""  const halls = st.rooms.filter(isTable);
  const rooms = st.rooms.filter(isRoom);
  return `
    <div class="sb-grid hall">${halls.map(cell).join("")}</div>
    <div class="sb-grid">${rooms.map(cell).join("")}</div>""")

# ---------- TV 좌석표: 층별 테이블 칸 ("tables:1층") ----------
s = L.rep(s, """  const st = store().settings;
  const ids = st.rooms.map(r=>r.id);
  const saved = st.displayRows;""",
"""  const st = store().settings;
  /* 테이블은 개별이 아니라 층별 한 칸("tables:1층")으로 — TV 는 룸 8칸 + 테이블 층 2칸이면 충분 */
  const ids = st.rooms.filter(isRoom).map(r=>r.id).concat(tableFloors().map(f=>"tables:"+f));
  const saved = st.displayRows;""")
s = L.rep(s, """  /* 기본: 1행 홀, 2·3행 룸을 반씩 */
  const halls = st.rooms.filter(r=>r.type==="hall").map(r=>r.id);
  const rooms = st.rooms.filter(r=>r.type==="room").map(r=>r.id);
  const half = Math.ceil(rooms.length/2);
  return [halls, rooms.slice(0,half), rooms.slice(half)];
}""",
"""  /* 기본: 1행 테이블(층별), 2·3행 룸을 반씩 */
  const halls = tableFloors().map(f=>"tables:"+f);
  const rooms = st.rooms.filter(isRoom).map(r=>r.id);
  const half = Math.ceil(rooms.length/2);
  return [halls, rooms.slice(0,half), rooms.slice(half)];
}
function tableFloors(){
  const out = []; (store().settings.rooms||[]).filter(isTable).forEach(t=>{ if(out.indexOf(t.floor||"")<0) out.push(t.floor||""); }); return out;
}
/* 디스플레이 칸 하나의 정보 — 룸이면 그 룸, "tables:층" 이면 그 층 테이블 묶음 */
function dispCell(id){
  if(/^tables:/.test(id)){ const fl = id.slice(7); return {id, name:`${fl||""} 테이블`.trim(), floor:"", type:"tables", ids:store().settings.rooms.filter(t=>isTable(t) && (t.floor||"")===fl).map(t=>t.id)}; }
  const r = seatById(id); return r ? Object.assign({ids:[r.id]}, r) : null;
}""")
s = L.rep(s, """  const order = [].concat.apply([], rowIds).map(function(id){ return st.rooms.find(function(r){return r.id===id;}); }).filter(Boolean);
  const secN = [];   /* 칸마다 '한 열에 몇 줄이 들어가는지' — 행 높이를 나눌 때 씁니다 */
  const sec = order.map(room=>{
    const rows = list.filter(r=>r.roomId===room.id).sort((a,b)=>a.time.localeCompare(b.time));
    const items = rows.length ? rows.map(r=>{
      /* 흐림 기준은 타임라인 블록과 같은 함수(isBlockPast). 자리를 접어야 할 때 이런 건이 먼저 밀립니다 */
      const past = isBlockPast(r, toMin(r.time), today, toMin(now));
      return `<li class="${past?'past':''}">
        <span class="t">${esc(r.time)}</span>
        <span class="n">${esc(maskName(r.name))} 님</span>
        <span class="p">${pplOf(r)}명</span>
      </li>`;
    }).join("") : ``;
    /* 손님이 보는 화면이라 룸 정원만 안내하고 홀 테이블 수는 적지 않습니다 */
    const capTxt = room.type==="hall" ? "" : `${roomMin(room)}~${room.capacity}인`;
    /* 홀은 2열이라 필요한 줄 수가 절반입니다 (아래에서 grid-template-rows 를 그 수로 맞춥니다) */
    secN.push(room.type==="hall" ? Math.max(1, Math.ceil(rows.length/2)) : rows.length);
    return `<section class="dsec ${room.type==='hall'?'hall':''}">
      <h3><span class="fl">${esc(room.floor||"")}</span>
        <span class="nm">${esc(room.name)}</span>
        <span class="cap">${capTxt}</span></h3>
      <ul class="${room.type==="hall"?"two-col":""}"${room.type==="hall"
        /* 줄 수를 6으로 고정해 두면 예약이 적어도 빈 줄의 간격만큼 자리를 먹고,
           목록을 접어도 높이가 줄지 않습니다. 실제 필요한 줄 수로 맞춥니다. */
        ? ` style="grid-template-rows:repeat(${Math.max(1,Math.ceil(rows.length/2))},auto)"` : ""}>${items}</ul>
    </section>`;
  });""",
"""  const order = [].concat.apply([], rowIds).map(dispCell).filter(Boolean);
  const secN = [];   /* 칸마다 '한 열에 몇 줄이 들어가는지' — 행 높이를 나눌 때 씁니다 */
  const sec = order.map(room=>{
    const isT = room.type === "tables";
    /* 대표 좌석이 이 칸에 속하는 예약 (합친 예약은 한 번만) */
    const rows = list.filter(r=>room.ids.indexOf(r.roomId)>=0).sort((a,b)=>a.time.localeCompare(b.time));
    const items = rows.length ? rows.map(r=>{
      /* 흐림 기준은 타임라인 블록과 같은 함수(isBlockPast). 자리를 접어야 할 때 이런 건이 먼저 밀립니다 */
      const past = isBlockPast(r, toMin(r.time), today, toMin(now));
      const tn = isT ? seatsOf(r).map(id=>{ const x = seatById(id); return x ? x.name : ""; }).filter(Boolean).join("+") : "";
      return `<li class="${past?'past':''}">
        <span class="t">${esc(r.time)}</span>
        <span class="n">${esc(maskName(r.name))} 님${tn?` <small class="tn">${esc(tn)}</small>`:""}</span>
        <span class="p">${pplOf(r)}명</span>
      </li>`;
    }).join("") : ``;
    /* 손님이 보는 화면이라 룸 정원만 안내하고 테이블 수는 적지 않습니다 */
    const capTxt = isT ? "" : `${roomMin(room)}~${room.capacity}인`;
    /* 테이블 칸은 2열이라 필요한 줄 수가 절반입니다 (아래에서 grid-template-rows 를 그 수로 맞춥니다) */
    secN.push(isT ? Math.max(1, Math.ceil(rows.length/2)) : rows.length);
    return `<section class="dsec ${isT?'hall':''}">
      <h3><span class="fl">${esc(room.floor||"")}</span>
        <span class="nm">${esc(room.name)}</span>
        <span class="cap">${capTxt}</span></h3>
      <ul class="${isT?"two-col":""}"${isT
        ? ` style="grid-template-rows:repeat(${Math.max(1,Math.ceil(rows.length/2))},auto)"` : ""}>${items}</ul>
    </section>`;
  });""")
s = L.rep(s, """.dsec.hall{background:linear-gradient(180deg, rgba(30,25,15,.94), rgba(18,15,9,.95)); border-color:rgba(214,182,120,.52)}""",
""".dsec.hall{background:linear-gradient(180deg, rgba(30,25,15,.94), rgba(18,15,9,.95)); border-color:rgba(214,182,120,.52)}
.dsec li .tn{font-size:.72em; color:#C8B795; margin-left:.4em; font-weight:500}   /* 테이블 칸에서 테이블 이름 */""")

# ---------- 시드 문자열 ----------
s = L.rep(s, """        un.seatPref = u%2===0 ? "room-any" : "hall-any";""", """        un.seatPref = u%2===0 ? "room-any" : "table-any";""")

L.js_check(s)
L.save(s)
print("p9_c ok")
