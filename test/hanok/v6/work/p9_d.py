# -*- coding: utf-8 -*-
"""v6 8차-D — 설정 UI
   · 좌석: 룸 목록(순서·최소=최적·최대·층·사용중지) / 테이블 목록(층별, 기본 인원·최대·붙일 수 있는 테이블·순서) / 룸 합침 그룹(추가·삭제)
   · 운영시간 편집: 요일마다 세션 표(이름·시작·접수 마감·점유 끝까지|분·끝) + 공휴일 행. 저장이 임시본(draft)에도 반영(점검 D1)
   · 공휴일: 연도별 목록(내장/추가/제외 표시), 추가, 제외, 다음 해 표 없을 때 안내
   · 옛 체류 시간 4칸·점심 경계·마지막 예약 버퍼 삭제(세션이 대신함). 옛 홀 구역 편집기(sheetTables 등) 삭제"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()

# ---------- 좌석 폴드 ----------
a = s.index("  /* ---------- 좌석 ---------- */\n  const seatBody = `")
b = s.index("  /* ---------- 코스 ---------- */\n  const courseBody = `")
s = s[:a] + r"""  /* ---------- 좌석 (8차) ---------- */
  const rooms = st.rooms.filter(isRoom), tables = st.rooms.filter(isTable);
  const floorsT = []; tables.forEach(t=>{ if(floorsT.indexOf(t.floor||"")<0) floorsT.push(t.floor||""); });
  const ord = (list, r) => { const i = list.indexOf(r); return `<span class="ordbtns">
        <button ${i===0?"disabled":""} onclick="moveSeat('${r.id}',-1)" title="위로">▲</button>
        <button ${i===list.length-1?"disabled":""} onclick="moveSeat('${r.id}',1)" title="아래로">▼</button></span><span class="ordnum">${i+1}</span>`; };
  const roomRowHtml = r => `
      <div class="rowitem">
        ${ord(rooms, r)}
        <span class="grow"><span class="t">${esc(r.name)}</span>
          <span class="s">최적 ${roomMin(r)}명 · 최대 ${r.capacity}명${r.floor?` · ${esc(r.floor)}`:""}${blockSummary(r)}</span></span>
        <button class="numbtn sm" onclick="openNum('minCapacity','${esc(r.name)} 최적(최소) 인원',1,30,{room:'${r.id}'})">최적 ${roomMin(r)}</button>
        <button class="numbtn sm" onclick="openNum('capacity','${esc(r.name)} 최대 인원',1,40,{room:'${r.id}'})">최대 ${r.capacity}</button>
        <label class="tbl-in">층
          <input value="${esc(r.floor||"")}" placeholder="1층" style="width:60px" onchange="setRoomText('${r.id}','floor',this.value)"></label>
        <button class="btn sm ${roomBlocks(r).length?'danger':''}" onclick="openBlocks('${r.id}')">${roomBlocks(r).length?`사용 중지 ${roomBlocks(r).length}건`:"사용 중지"}</button>
        <button class="btn sm danger" onclick="delRoom('${r.id}')">삭제</button>
      </div>`;
  const tableRowHtml = (list, t) => `
      <div class="rowitem tblrow">
        ${ord(list, t)}
        <span class="grow"><span class="t">${esc(t.name)}${t.note?` <small class="muted">${esc(t.note)}</small>`:""}</span>
          <span class="s">${t.seats||4}인석${t.capacity&&t.capacity!==t.seats?` · 최대 ${t.capacity}`:""}${roomMin(t)?` · 최소 ${roomMin(t)}`:""}${blockSummary(t)}</span>
          <span class="s">붙이기: ${(t.joinWith||[]).length ? (t.joinWith||[]).map(id=>{ const x = seatById(id); return x ? esc(x.name) : ""; }).filter(Boolean).join(", ") : "없음"}</span></span>
        <button class="numbtn sm" onclick="openNum('seats','${esc(t.name)} 기본 인원',1,20,{room:'${t.id}'})">${t.seats||4}인석</button>
        <button class="btn sm" onclick="openTableEdit('${t.id}')">상세</button>
        <button class="btn sm ${roomBlocks(t).length?'danger':''}" onclick="openBlocks('${t.id}')">${roomBlocks(t).length?`중지 ${roomBlocks(t).length}`:"사용 중지"}</button>
        <button class="btn sm danger" onclick="delRoom('${t.id}')">삭제</button>
      </div>`;
  const joinRowHtml = j => `
      <div class="rowitem">
        <span class="grow"><span class="t">${esc(seatLabel(j.id))}</span>
          <span class="s">${j.min}~${j.max}명${j.note?` · ${esc(j.note)}`:""}</span></span>
        <button class="numbtn sm" onclick="openNum('min','${esc(seatLabel(j.id))} 최소',1,60,{join:'${j.id}'})">최소 ${j.min}</button>
        <button class="numbtn sm" onclick="openNum('max','${esc(seatLabel(j.id))} 최대',1,80,{join:'${j.id}'})">최대 ${j.max}</button>
        <button class="btn sm danger" onclick="delJoin('${j.id}')">삭제</button>
      </div>`;
  const seatBody = `
    <p class="f-note" style="margin:0 0 12px">
      <b>배정 순서</b>는 좌석을 정하지 않은 손님에게 자리를 미리 잡아 둘 때 씁니다.
      인원이 맞는 좌석 중 <b>위에서부터</b> 고릅니다(▲▼로 순서를 바꾸세요). 룸과 테이블은 손님이 고른 쪽만 봅니다.</p>
    <div class="subhead">룸 <span>최적 인원 = 최소 인원. 그보다 적으면 경고가 뜹니다</span></div>
    ${rooms.map(roomRowHtml).join("")}
    <div class="btn-row" style="margin-top:8px">
      <input id="nr-name" placeholder="룸 이름" style="flex:2 1 120px">
      <input id="nr-min" type="number" min="1" value="6" title="최적(최소) 인원" style="flex:1 1 62px">
      <input id="nr-cap" type="number" min="1" value="7" title="최대 인원" style="flex:1 1 62px">
      <input id="nr-floor" placeholder="층" style="flex:1 1 60px">
      <button class="btn primary" onclick="addRoom('room')">룸 추가</button>
    </div>

    <div class="subhead" style="margin-top:20px">테이블 <span>이름 있는 테이블 하나가 좌석 하나. 붙일 수 있는 테이블은 '상세'에서</span></div>
    ${floorsT.map(fl=>{ const list = tables.filter(t=>(t.floor||"")===fl); return `<div class="lbl" style="margin:10px 0 4px">${esc(fl||"층 없음")}</div>${list.map(t=>tableRowHtml(list, t)).join("")}`; }).join("")}
    <div class="btn-row" style="margin-top:8px">
      <input id="nt-name" placeholder="테이블 이름 (예: 26)" style="flex:2 1 120px">
      <input id="nt-seats" type="number" min="1" value="4" title="기본 인원" style="flex:1 1 62px">
      <input id="nt-floor" placeholder="층" value="${esc(floorsT[0]||"1층")}" style="flex:1 1 60px">
      <button class="btn primary" onclick="addRoom('table')">테이블 추가</button>
    </div>

    <div class="subhead" style="margin-top:20px">룸 합침 <span>중문을 떼어 두세 방을 한 팀이 쓰는 경우. 자동 배정에는 안 쓰고, 예약 받을 때 사람이 고릅니다</span></div>
    ${(st.joins||[]).map(joinRowHtml).join("") || `<div class="empty">합침 그룹이 없습니다.</div>`}
    <div class="btn-row" style="margin-top:8px; flex-wrap:wrap">
      ${rooms.map(r=>`<label class="chk" style="margin:0"><input type="checkbox" class="nj-room" value="${r.id}"><span>${esc(r.name)}</span></label>`).join("")}
    </div>
    <div class="btn-row" style="margin-top:6px">
      <input id="nj-min" type="number" min="1" value="12" title="최소" style="flex:1 1 62px">
      <input id="nj-max" type="number" min="1" value="14" title="최대" style="flex:1 1 62px">
      <input id="nj-note" placeholder="메모 (예: 원탁 — 손님 확인)" style="flex:3 1 160px">
      <button class="btn primary" onclick="addJoin()">합침 추가</button>
    </div>`;

""" + s[b:]

# ---------- 좌석 편집 함수들 ----------
s = L.replace_fn(s, "moveRoom", """/* 같은 종류(룸끼리·같은 층 테이블끼리) 안에서만 순서를 바꿉니다 — 배열은 룸·테이블이 섞여 있어 절대 index 로 바꾸면 종류를 넘어감 */
function moveSeat(id, d){
  const st = draft(), arr = st.rooms;
  const r = arr.find(x=>x.id===id); if(!r) return;
  const same = arr.filter(x=>x.type===r.type && (isRoom(r) || (x.floor||"")===(r.floor||"")));
  const k = same.indexOf(r), j = k + d;
  if(j < 0 || j >= same.length) return;
  const other = same[j];
  const i1 = arr.indexOf(r), i2 = arr.indexOf(other);
  arr[i1] = other; arr[i2] = r;
  render();
}
function moveRoom(i,d){ const st = draft(); if(st.rooms[i]) moveSeat(st.rooms[i].id, d); }""")
s = L.replace_fn(s, "addRoom", """async function addRoom(type){
  const st = draft();
  if(type === "table"){
    const name = (document.getElementById("nt-name").value||"").trim();
    if(!name) return uiAlert("테이블 이름을 입력하세요","","warn");
    const seats = Math.max(1, parseInt(document.getElementById("nt-seats").value)||4);
    st.rooms.push({id:"t_"+newId("t").slice(2,10), name, type:"table", floor:(document.getElementById("nt-floor").value||"").trim(), seats, joinWith:[]});
  }else{
    const name = (document.getElementById("nr-name").value||"").trim();
    if(!name) return uiAlert("룸 이름을 입력하세요","","warn");
    const cap = Math.max(1, parseInt(document.getElementById("nr-cap").value)||6);
    const min = Math.max(1, parseInt(document.getElementById("nr-min").value)||cap);
    st.rooms.push({id:"r_"+newId("r").slice(2,10), name, type:"room", floor:(document.getElementById("nr-floor").value||"").trim(), capacity:cap, minCapacity:Math.min(min,cap), tuned:true});
  }
  render();
}
/* 테이블 상세 — 최대 인원·최소·붙일 수 있는 테이블·메모 */
function openTableEdit(id){ view.form={type:"tedit", id}; render(); }
function sheetTableEdit(){
  const st = draft(), t = st.rooms.find(x=>x.id===view.form.id);
  if(!t) return `${sheetHead("테이블")}<div class="empty">없음</div>`;
  const others = st.rooms.filter(x=>isTable(x) && x.id!==t.id && (x.floor||"")===(t.floor||""));
  return `
    ${sheetHead(`${esc(t.name)} 테이블`)}
    <div class="grid2">
      <label class="f"><div class="lb">기본 인원</div><button class="numbtn" onclick="openNum('seats','기본 인원',1,20,{room:'${t.id}'})">${t.seats||4}<small>명</small></button></label>
      <label class="f"><div class="lb">최대 인원 <span class="lbl-note">비우면 기본과 같음</span></div><button class="numbtn" onclick="openNum('capacity','최대 인원',1,20,{room:'${t.id}'})">${t.capacity||t.seats||4}<small>명</small></button></label>
      <label class="f"><div class="lb">최소 인원 <span class="lbl-note">0 = 제한 없음</span></div><button class="numbtn" onclick="openNum('minCapacity','최소 인원',0,20,{room:'${t.id}'})">${t.minCapacity||0}<small>명</small></button></label>
      <label class="f"><div class="lb">층</div><input value="${esc(t.floor||"")}" onchange="setRoomText('${t.id}','floor',this.value)"></label>
    </div>
    <label class="f"><div class="lb">메모 <span class="lbl-note">예: 파셜룸</span></div><input value="${esc(t.note||"")}" onchange="setRoomText('${t.id}','note',this.value)"></label>
    <div class="lbl" style="margin-top:12px">붙일 수 있는 테이블 <span class="lbl-note">같은 층만. 서로 체크해야 붙습니다</span></div>
    <div class="btn-row" style="flex-wrap:wrap">
      ${others.map(o=>`<button class="wbtn ${(t.joinWith||[]).indexOf(o.id)>=0?'on':''}" onclick="toggleJoinWith('${t.id}','${o.id}')">${esc(o.name)}</button>`).join("") || `<span class="muted">같은 층에 다른 테이블이 없습니다</span>`}
    </div>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
function toggleJoinWith(id, other){
  const st = draft(), t = st.rooms.find(x=>x.id===id), o = st.rooms.find(x=>x.id===other);
  if(!t || !o) return;
  const on = (t.joinWith||[]).indexOf(other) >= 0;
  t.joinWith = on ? (t.joinWith||[]).filter(x=>x!==other) : (t.joinWith||[]).concat([other]);
  o.joinWith = on ? (o.joinWith||[]).filter(x=>x!==id) : ((o.joinWith||[]).indexOf(id)>=0 ? o.joinWith : (o.joinWith||[]).concat([id]));   /* 양쪽 다 */
  render();
}
async function addJoin(){
  const st = draft();
  const ids = Array.prototype.map.call(document.querySelectorAll(".nj-room:checked"), el=>el.value);
  if(ids.length < 2) return uiAlert("합칠 룸을 두 개 이상 고르세요","","warn");
  if((st.joins||[]).some(j=>sameIds(j.ids, ids))) return uiAlert("이미 있는 합침입니다","","warn");
  const min = Math.max(1, parseInt(document.getElementById("nj-min").value)||1), max = Math.max(min, parseInt(document.getElementById("nj-max").value)||min);
  st.joins = (st.joins||[]).concat([{id:"j_"+newId("j").slice(2,10), ids, min, max, note:(document.getElementById("nj-note").value||"").trim()}]);
  render();
}
async function delJoin(id){
  const st = draft(); const j = (st.joins||[]).find(x=>x.id===id);
  if(!await uiConfirm("합침을 삭제할까요?", j ? seatLabel(j.id) : "", {ok:"삭제"})) return;
  st.joins = (st.joins||[]).filter(x=>x.id!==id); render();
}""")
s = L.rep(s, """  if(!await uiConfirm("이 좌석을 삭제할까요?", `${r?r.name:""} — 기존 예약은 ‘미배정’으로 표시됩니다.`, {ok:"삭제"})) return;
  st.rooms = st.rooms.filter(x=>x.id!==id);
  render();""",
"""  if(!await uiConfirm("이 좌석을 삭제할까요?", `${r?r.name:""} — 기존 예약은 ‘미배정’으로 표시됩니다.`, {ok:"삭제"})) return;
  st.rooms = st.rooms.filter(x=>x.id!==id);
  st.rooms.forEach(x=>{ if(x.joinWith) x.joinWith = x.joinWith.filter(y=>y!==id); });
  st.joins = (st.joins||[]).filter(j=>j.ids.indexOf(id) < 0);
  render();""")
# 시트 등록 + 옛 홀 편집기 삭제
s = L.rep(s, "noshow:sheetNoshow, pin:sheetPin, apw:sheetAdminPw, hours:sheetHours, logs:sheetLogs,",
             "noshow:sheetNoshow, pin:sheetPin, apw:sheetAdminPw, hours:sheetHours, tedit:sheetTableEdit, logs:sheetLogs,")
s = L.rep(s, "tables:sheetTables, ", "")
s = L.rep(s, """function openTables(id){ view.form={type:"tables", id}; render(); }\n""", "")
for fn in ["sheetTables","zoneCombos","zoneMap","zonesOf","setZone","addZone","delZone","addZSet","delZSet"]:
    s = L.remove_fn(s, fn)
# numValue/numSave — 홀 구역 분기 삭제, 합침 그룹 분기 추가
s = L.rep(s, """  if(f.ctx && f.ctx.room){
    const r = st.rooms.find(x=>x.id===f.ctx.room);
    return r ? (f.key==="minCapacity" ? roomMin(r) : (r[f.key]||f.min)) : f.min;
  }
  if(f.ctx && f.ctx.tset != null){
    const hall = st.rooms.find(x=>x.id===f.ctx.hall);
    const zone = (hall.zones||[])[f.ctx.zone];
    if(f.key==="maxJoin") return zone.maxJoin||1;
    const s = zone.sets[f.ctx.tset];
    return s ? s[f.key] : f.min;""",
"""  if(f.ctx && f.ctx.room){
    const r = st.rooms.find(x=>x.id===f.ctx.room);
    return r ? (f.key==="minCapacity" ? roomMin(r) : (r[f.key] != null ? r[f.key] : (f.key==="capacity" ? seatMax(r) : f.min))) : f.min;
  }
  if(f.ctx && f.ctx.join){
    const j = (st.joins||[]).find(x=>x.id===f.ctx.join);
    return j ? j[f.key] : f.min;""")
s = L.rep(s, """  if(f.ctx && f.ctx.room){
    st.rooms = st.rooms.map(r=>r.id===f.ctx.room?{...r,[f.key]:v}:r);
  }else if(f.ctx && f.ctx.hall != null){
    const hall = st.rooms.find(x=>x.id===f.ctx.hall);
    const zone = hall.zones[f.ctx.zone];
    if(f.key==="maxJoin") zone.maxJoin = v;
    else zone.sets[f.ctx.tset][f.key] = v;
  }else{""",
"""  if(f.ctx && f.ctx.room){
    st.rooms = st.rooms.map(r=>r.id===f.ctx.room?Object.assign({}, r, {[f.key]:v, tuned:true}):r);
  }else if(f.ctx && f.ctx.join){
    st.joins = (st.joins||[]).map(j=>j.id===f.ctx.join?Object.assign({}, j, {[f.key]:v}):j);
  }else{""")

# ---------- 예약 규칙 폴드: 옛 체류 4칸·점심 경계·마감 버퍼 삭제 ----------
s = L.rep(s, """    <div class="subhead">체류 시간 <span>예약 한 건이 자리를 잡아 두는 시간</span></div>
    <div class="grid2">
      <label class="f"><div class="lb">룸 · 점심</div>
        <button class="numbtn" onclick="openNum('lunchStayHours','룸 점심 체류',1,6,{step:0.5})">${st.lunchStayHours||2.5}<small>시간</small></button></label>
      <label class="f"><div class="lb">룸 · 저녁</div>
        <button class="numbtn" onclick="openNum('stayHours','룸 저녁 체류',1,6,{step:0.5})">${st.stayHours||3}<small>시간</small></button></label>
      <label class="f"><div class="lb">홀 · 점심</div>
        <button class="numbtn" onclick="openNum('hallLunchStayHours','홀 점심 체류',1,6,{step:0.5})">${st.hallLunchStayHours||2}<small>시간</small></button></label>
      <label class="f"><div class="lb">홀 · 저녁</div>
        <button class="numbtn" onclick="openNum('hallStayHours','홀 저녁 체류',1,6,{step:0.5})">${st.hallStayHours||2.5}<small>시간</small></button></label>
    </div>
    <label class="f"><div class="lb">점심·저녁 경계</div>
      <input type="time" value="${st.lunchUntil||"16:00"}" onchange="setSetting('lunchUntil',this.value)">
      <div class="f-note">이 시각 이전 예약은 점심 체류 시간으로 계산됩니다.</div></label>
""",
"""    <p class="f-note" style="margin:0 0 12px"><b>점유 시간·접수 마감</b>은 운영시간의 <b>세션</b>(점심/저녁)에서 요일마다 정합니다 (운영시간 → 수정).</p>
""")
s = L.rep(s, """    <div class="subhead">마감·브레이크</div>
    <label class="f"><div class="lb">마지막 예약 (종료 전)</div>
      <button class="numbtn" onclick="openNum('lastBookingBuffer','영업 종료 몇 분 전까지 받나요?',0,180,{step:10})">${st.lastBookingBuffer != null ? st.lastBookingBuffer : 60}<small>분 전</small></button>
      <div class="f-note">라스트오더가 정해진 요일은 그 시각을 우선합니다.</div></label>
""", """    <div class="subhead">브레이크</div>
""")

# ---------- 운영시간 편집: 세션 표 + 공휴일 행 + draft 반영 ----------
s = L.rep(s, """  view.schedDraft = {
    from: from || todayStr(),
    isNew: !from,
    days: deepClone(base ? base.days : DEFAULT_DATA.hanok.settings.schedules[0].days)
  };""",
"""  view.schedDraft = {
    from: from || todayStr(), origFrom: from || null,
    isNew: !from,
    days: deepClone(base ? base.days : DEFAULT_DATA.hanok.settings.schedules[0].days),
    holiday: deepClone(base && base.holiday ? base.holiday : DEFAULT_DATA.hanok.settings.schedules[0].holiday)
  };""")
s = L.rep(s, """function sheetSchedule(){
  const d = view.schedDraft;
  const rows = d.days.map((x,i)=>`
    <div class="dayrow ${i===0?'sun':i===6?'sat':''}">
      <div class="dr-h"><b>${DOW[i]}</b></div>""",
"""/* 세션 표 한 줄 — 이름 · 시작 · 접수 마감 · 점유(끝까지 / 분) · 끝 */
function sessRows(x, key){
  const ss = x.sessions || [];
  return `<div class="sess">
    <div class="sess-h"><span>세션</span><span>시작</span><span>접수 마감</span><span>점유</span><span>끝</span><span></span></div>
    ${ss.map((se,si)=>`<div class="sess-r">
      <input value="${esc(se.name||"")}" onchange="setSess('${key}',${si},'name',this.value)">
      <input type="time" value="${se.from||""}" onchange="setSess('${key}',${si},'from',this.value)">
      <input type="time" value="${se.lastBook||""}" onchange="setSess('${key}',${si},'lastBook',this.value)">
      <span class="sess-stay"><label class="chk"><input type="checkbox" ${se.stay==="end"?"checked":""} onchange="setSess('${key}',${si},'stay',this.checked?'end':110)"><span>끝까지</span></label>
        ${se.stay==="end"?"":`<input type="number" min="30" step="10" value="${se.stay||110}" style="width:64px" onchange="setSess('${key}',${si},'stay',parseInt(this.value)||110)"><small>분</small>`}</span>
      <input type="time" value="${se.until||""}" onchange="setSess('${key}',${si},'until',this.value)">
      <button class="btn sm danger" onclick="delSess('${key}',${si})">×</button>
    </div>`).join("")}
    <button class="btn sm" onclick="addSess('${key}')">＋ 세션</button>
  </div>`;
}
function sessTarget(key){ const d = view.schedDraft; return key==="h" ? d.holiday : d.days[Number(key)]; }
function setSess(key, si, k, v){ const t = sessTarget(key); if(!t.sessions) t.sessions = []; t.sessions[si][k] = v; render(); }
function addSess(key){ const t = sessTarget(key); if(!t.sessions) t.sessions = []; t.sessions.push({name:"세션", from:t.open||"11:00", lastBook:t.close||"20:00", stay:"end", until:t.close||"22:00"}); render(); }
function delSess(key, si){ const t = sessTarget(key); (t.sessions||[]).splice(si,1); render(); }
function sheetSchedule(){
  const d = view.schedDraft;
  const dayBlock = (x, i, key, label, cls) => `
    <div class="dayrow ${cls||''}">
      <div class="dr-h"><b>${label}</b></div>""")
s = L.rep(s, """        <label class="chk"><input type="checkbox" ${x.lo?"":"checked"} onchange="toggleLoDay(${i})">
          <span>라스트오더 없음</span></label>
      </div>
    </div>`).join("");
  return `
    ${sheetHead(d.isNew?"운영시간 수정":"운영시간 편집")}""",
"""        <label class="chk"><input type="checkbox" ${x.lo?"":"checked"} onchange="toggleLoDay(${i})">
          <span>라스트오더 없음</span></label>
        ${sessRows(x, key)}
      </div>
    </div>`;
  const rows = d.days.map((x,i)=>dayBlock(x, i, String(i), DOW[i], i===0?'sun':i===6?'sat':'')).join("")
             + dayBlock(d.holiday, 7, "h", "공휴일", "sun");
  return `
    ${sheetHead(d.isNew?"운영시간 수정":"운영시간 편집")}
    <p class="f-note" style="margin:-6px 0 12px">세션 = 손님을 받는 시간대. <b>접수 마감</b>은 마지막으로 입장을 받는 시각(식사 시간 보장), <b>점유 '끝까지'</b>는 그 세션 끝까지 한 자리에 한 팀만.
      라스트오더는 주방 마감이라 별개입니다.</p>""")
# setDay/toggle* 는 index 7(공휴일)도 다루게
s = L.rep(s, """function setDay(i,k,v){ view.schedDraft.days[i][k]=v; render(); }
function toggleBreakDay(i){
  const d = view.schedDraft.days[i];""",
"""function dayOf(i){ return i===7 ? view.schedDraft.holiday : view.schedDraft.days[i]; }
function setDay(i,k,v){ dayOf(i)[k]=v; render(); }
function toggleBreakDay(i){
  const d = dayOf(i);""")
s = L.rep(s, """function toggleLoDay(i){
  const d = view.schedDraft.days[i];""", """function toggleLoDay(i){
  const d = dayOf(i);""")
s = L.rep(s, """  const d = view.schedDraft.days[i];
  d.lo = minToHM""", """  const d = dayOf(i);
  d.lo = minToHM""")
s = L.rep(s, """  st.schedules = (st.schedules||[]).filter(s=>s.from!==d.from);
  st.schedules.push({from:d.from, days:deepClone(d.days)});
  st.schedules.sort((a,b)=>a.from.localeCompare(b.from));
  logEvent("설정 변경", `운영시간 ${d.from}부터`);
  view.form=null; view.schedDraft=null; saveData(); render();""",
"""  st.schedules = (st.schedules||[]).filter(s=>s.from!==d.from && s.from!==d.origFrom);   /* 시작일을 바꿨으면 옛 항목도 정리 */
  st.schedules.push({from:d.from, days:deepClone(d.days), holiday:deepClone(d.holiday)});
  st.schedules.sort((a,b)=>a.from.localeCompare(b.from));
  if(view.draft) view.draft.schedules = deepClone(st.schedules);   /* 임시본에도 — 안 그러면 '적용하기'가 방금 저장한 것을 되돌립니다(점검 D1) */
  logEvent("설정 변경", `운영시간 ${d.from}부터`);
  view.form=null; view.schedDraft=null; saveData(); render();""")
s = L.rep(s, """  st.schedules = st.schedules.filter(s=>s.from!==from);
  logEvent("설정 변경", `운영시간 삭제 ${from}`);""",
"""  st.schedules = st.schedules.filter(s=>s.from!==from);
  if(view.draft) view.draft.schedules = deepClone(st.schedules);
  logEvent("설정 변경", `운영시간 삭제 ${from}`);""")
# 세션 표 CSS
s = L.rep(s, """.dr-in input:disabled{background:var(--surface-2); color:var(--text-3)}""",
""".dr-in input:disabled{background:var(--surface-2); color:var(--text-3)}
/* 세션 표 (8차) — 요일 칸 안, 한 줄에 이름·시작·접수 마감·점유·끝 */
.sess{margin-top:var(--s8); border-top:1px dashed var(--border); padding-top:var(--s8)}
.sess-h, .sess-r{display:grid; grid-template-columns:72px 96px 96px 1fr 96px 34px; gap:var(--s4); align-items:center; margin-bottom:var(--s4)}
.sess-h span{font-size:var(--fs-label); color:var(--text-3); font-weight:600}
.sess-r input{width:100%; min-width:0; padding:var(--s4) var(--s8); font-size:var(--fs-sub)}
.sess-stay{display:flex; align-items:center; gap:var(--s4); min-width:0}
.sess-stay .chk{margin:0; white-space:nowrap}
@media (max-width:640px){ .sess-h{display:none} .sess-r{grid-template-columns:1fr 1fr; } .sess-r button{grid-column:2; justify-self:end} }""")

# ---------- 공휴일 UI ----------
s = L.rep(s, """      <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:4px">
        ${(st.holidays||[]).slice().sort().map(h=>`
          <span class="tag" style="padding:6px 10px">${h.slice(5).replace("-","/")}
            <button onclick="delHoliday('${h}')" style="background:none;border:none;color:var(--rust);padding:0 0 0 5px">×</button>
          </span>`).join("") || `<span class="muted" style="font-size:13px">등록된 공휴일이 없습니다.</span>`}
      </div>
      <div class="btn-row" style="margin-top:10px">
        <input id="hol-date" type="date" style="flex:1 1 160px">
        <button class="btn primary" onclick="addHoliday()">공휴일 추가</button>
      </div>
      <p class="f-note">공휴일은 자동으로 알 수 없어 직접 등록합니다.</p>`:""}`;""",
"""      ${(()=>{ const y = view.holYear || new Date().getFullYear(); const gap = holidayTableGap(); return `
      <div class="btn-row" style="margin-top:8px; align-items:center">
        <button class="btn sm" onclick="view.holYear=${y-1}; render()">◀</button><b>${y}년</b><button class="btn sm" onclick="view.holYear=${y+1}; render()">▶</button>
        <span class="muted" style="font-size:12px">${KR_HOLIDAYS[y]?"내장표 있음":"내장표 없음 — 직접 등록"}</span>
      </div>
      ${gap?`<div class="alert amber" style="margin:8px 0"><span class="ic">!</span><div><div class="a-t">${gap}년 공휴일이 등록되지 않았습니다</div><div class="a-s">내장표는 2026~2027년까지입니다. 아래에서 ${gap}년 공휴일을 직접 추가하세요(대체공휴일 포함). 안 하면 그날 평일 운영시간으로 계산됩니다.</div></div></div>`:""}
      <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px">
        ${holidaysOfYear(y).map(h=>`
          <span class="tag ${h.src==="추가"?"blue":""}" style="padding:6px 10px" title="${h.src}">${h.date.slice(5).replace("-","/")}
            <button onclick="delHoliday('${h.date}')" style="background:none;border:none;color:var(--rust);padding:0 0 0 5px" title="${h.src==="내장"?"이 날은 공휴일 아님으로":"삭제"}">×</button>
          </span>`).join("") || `<span class="muted" style="font-size:13px">${y}년 공휴일이 없습니다.</span>`}
        ${(st.holidaysOff||[]).filter(d=>d.slice(0,4)===String(y)).map(d=>`<span class="tag" style="padding:6px 10px; opacity:.55; text-decoration:line-through" title="제외됨">${d.slice(5).replace("-","/")}
            <button onclick="restoreHoliday('${d}')" style="background:none;border:none;color:var(--pine);padding:0 0 0 5px" title="다시 공휴일로">↺</button></span>`).join("")}
      </div>
      <div class="btn-row" style="margin-top:10px">
        <input id="hol-date" type="date" style="flex:1 1 160px">
        <button class="btn primary" onclick="addHoliday()">공휴일 추가</button>
      </div>
      <p class="f-note">2026~2027년 공휴일(대체공휴일 포함)은 들어 있습니다. 임시공휴일·선거일은 미리 알 수 없으니 정해지면 추가하세요. × 는 그날을 공휴일에서 뺍니다.</p>`; })()}`:""}`;""")
s = L.rep(s, """function delHoliday(d){
  const st = draft();
  st.holidays = (st.holidays||[]).filter(x=>x!==d);
  render();
}""",
"""function delHoliday(d){
  const st = draft();
  if((st.holidays||[]).indexOf(d) >= 0) st.holidays = st.holidays.filter(x=>x!==d);
  else st.holidaysOff = (st.holidaysOff||[]).concat([d]);   /* 내장표의 날짜는 지울 수 없으니 '제외' 목록에 */
  render();
}
function restoreHoliday(d){ const st = draft(); st.holidaysOff = (st.holidaysOff||[]).filter(x=>x!==d); render(); }""")
s = L.rep(s, """function addHoliday(){
  const v = document.getElementById("hol-date").value;
  if(!v) return;
  const st = draft();
  st.holidays = [...new Set([...(st.holidays||[]), v])];
  render();
}""",
"""function addHoliday(){
  const v = document.getElementById("hol-date").value;
  if(!v) return;
  const st = draft();
  st.holidaysOff = (st.holidaysOff||[]).filter(x=>x!==v);
  st.holidays = [...new Set([...(st.holidays||[]), v])];
  view.holYear = Number(v.slice(0,4));
  render();
}""")

L.js_check(s)
L.save(s)
print("p9_d ok")
