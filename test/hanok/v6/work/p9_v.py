# -*- coding: utf-8 -*-
"""8차-V — 재아 목록 6차: 네이버 가져오기 열면 전체화면 잠시 해제·닫으면 복귀, 빠른 입력 날짜·시각을 우리 달력/세션 칸으로,
   화면형 시트는 머리 X 없음, 기기 보정은 더보기 '화면 보정' 로, 시트 최대 높이 zoom 보정, 목록 '지금' 구분선 + 지난 것 더 흐리게,
   이른 방문 처리 되묻기, 나뉨 기호 ⊕"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 네이버 가져오기: 전체화면 잠시 해제 ----------
s = R(s, """function openNaver(){ view.form = {type:"naver", page:true}; view.naver = {text:"", result:null}; render(); window.scrollTo(0,0); }   /* 열 때마다 비움(재아). 화면형 */""",
"""function openNaver(){
  /* 엑셀을 다녀와야 하므로 전체화면이면 잠시 풀고, 닫을 때 되돌립니다(재아) */
  view.fsWas = !!document.fullscreenElement;
  if(view.fsWas && document.exitFullscreen) document.exitFullscreen().catch(function(){});
  view.form = {type:"naver", page:true}; view.naver = {text:"", result:null}; render(); window.scrollTo(0,0);
}""")
s = R(s, """function closeSheet(){ var was = view.form && view.form.type === "res"; view.form=null; tmpRes=null; view.pickAll=false; view.pickSeat=null; render(); if(was) histPop(); }""",
"""function closeSheet(){
  var was = view.form && view.form.type === "res", wasNaver = view.form && view.form.type === "naver";
  view.form=null; tmpRes=null; view.pickAll=false; view.pickSeat=null; render(); if(was) histPop();
  if(wasNaver && view.fsWas){ view.fsWas = false; tryFullscreenForce(); }   /* 닫기 버튼 클릭이 손짓이라 여기서는 됩니다 */
}
function tryFullscreenForce(){ try{ var el = document.documentElement; if(!document.fullscreenElement && el.requestFullscreen) el.requestFullscreen().catch(function(){}); }catch(e){} }""")

# ---------- 화면형 시트: 머리에 X 없음 ----------
s = R(s, """function sheetHead(title){
  return `<div class="sheet-h"><h2>${title}</h2><button class="x" onclick="closeSheet()" aria-label="닫기">×</button></div>`;
}""", """function sheetHead(title){
  if(view.form && view.form.page) return `<div class="sheet-h"><h2>${title}</h2></div>`;   /* 화면형은 상단바에 X 가 있음 */
  return `<div class="sheet-h"><h2>${title}</h2><button class="x" onclick="closeSheet()" aria-label="닫기">×</button></div>`;
}""")

# ---------- 빠른 입력·수정: 날짜/시각을 우리 달력·세션 칸으로 ----------
s = R(s, """    <div class="grid2">
      <label class="f"><div class="lb">날짜</div><input id="f-date" type="date" value="${f.date}"></label>
      <label class="f"><div class="lb">시간</div><input id="f-time" type="time" value="${f.time}"></label>
    </div>""", """    <div class="grid2">
      <div class="f"><div class="lb">날짜</div><button class="numbtn ${f.pickDate?'on':''}" onclick="syncRes(); tmpRes.pickDate=!tmpRes.pickDate; tmpRes.pickTime=false; render()">${f.date?dateLabel(f.date):"날짜 고르기"}</button></div>
      <div class="f"><div class="lb">시간</div><button class="numbtn ${f.pickTime?'on':''}" onclick="syncRes(); tmpRes.pickTime=!tmpRes.pickTime; tmpRes.pickDate=false; render()">${f.time?hm(f.time):"시각 고르기"}</button></div>
    </div>
    <input id="f-date" type="hidden" value="${f.date||""}"><input id="f-time" type="hidden" value="${f.time||""}">
    ${f.pickDate ? `<div class="card" style="padding:8px; margin-bottom:12px">${miniCal(f.date, "resPickDate")}</div>` : ""}
    ${f.pickTime ? `<div class="card" style="padding:8px; margin-bottom:12px">${f.date ? timeGrid({date:f.date, people:f.people||0, time:f.time, pick:"resPickSlot"}) : `<div class="empty">날짜를 먼저 고르세요</div>`}
      ${store().settings.minuteSteps !== false && f.time ? `<div class="btn-row" style="margin-top:8px"><button class="btn sm" onclick="resNudge(-5)">− 5분</button><span class="lbl-note">${hm(f.time)}</span><button class="btn sm" onclick="resNudge(5)">＋ 5분</button></div>` : ""}</div>` : ""}""")
s = R(s, """function pickSource(x){ syncRes(); tmpRes = {...tmpRes, source:x}; render(); }""",
"""function pickSource(x){ syncRes(); tmpRes = {...tmpRes, source:x}; render(); }
function resPickDate(d){ syncRes(); tmpRes = Object.assign({}, tmpRes, {date:d, pickDate:false, calMonth:d.slice(0,7)}); render(); }
function resPickSlot(t){ syncRes(); tmpRes = Object.assign({}, tmpRes, {time:minToHM(t), pickTime:false}); render(); }
function resNudge(d){ syncRes(); if(!tmpRes.time) return; const m = Math.max(0, Math.min(23*60+55, toMin(tmpRes.time) + d)); tmpRes = Object.assign({}, tmpRes, {time:minToHM(m)}); render(); }
function resCalMove(d){ syncRes(); const [y,m] = (tmpRes.calMonth || tmpRes.date || todayStr()).slice(0,7).split("-").map(Number); const nd = new Date(y, m-1+d, 1); tmpRes = Object.assign({}, tmpRes, {calMonth:`${nd.getFullYear()}-${pad(nd.getMonth()+1)}`}); render(); }
/* 작은 달력 — 빠른 입력·수정 시트용. 마법사 달력과 같은 칸(일자·막대·건수) */
function miniCal(sel, pickFn){
  const s = store(), today = todayStr();
  const ym = (tmpRes && tmpRes.calMonth) || (sel || today).slice(0,7);
  const [y,m] = ym.split("-").map(Number);
  const first = new Date(y, m-1, 1), lastDay = new Date(y, m, 0).getDate(), lead = first.getDay();
  let cells = "";
  for(let i=0;i<lead;i++) cells += `<span class="bday"></span>`;
  for(let d=1; d<=lastDay; d++){
    const ds = `${y}-${pad(m)}-${pad(d)}`;
    const n = s.reservations.filter(r=>r.date===ds && r.status==="확정").length;
    const dow = new Date(ds+"T00:00:00").getDay();
    const rt = n ? dayStat(ds).rate : 0;
    cells += `<button class="bday btn-day ${sel===ds?'sel':''} ${ds===today?'today':''} ${ds<today?'past':''} ${dow===0?'sun':dow===6?'sat':''} ${hoursFor(ds).closed?'closed':''}" onclick="${pickFn}('${ds}')">
      <span class="d">${d}</span>${n?`<span class="b">${n}건</span><span class="obar"><i style="width:${rt}%" class="${rt>=70?'hi':rt>=40?'mid':''}"></i></span>`:""}</button>`;
  }
  return `<div class="cal-h"><button class="nav" onclick="resCalMove(-1)">‹</button><b>${y}년 ${m}월</b><button class="nav" onclick="resCalMove(1)">›</button></div>
    <div class="bcal"><span class="dow sun">일</span><span class="dow">월</span><span class="dow">화</span><span class="dow">수</span><span class="dow">목</span><span class="dow">금</span><span class="dow sat">토</span>${cells}</div>`;
}""")
# sessionGrid 를 일반화: ctx 로
s = R(s, """function sessionGrid(){
  const s = store(), st = s.settings, dh = hoursFor(WZ.date);
  if(dh.closed) return `<div class="empty">휴무일입니다. 아래 '접수 시간 밖' 에서 그래도 받을 수 있습니다.</div>`;
  const ss = sessionsFor(WZ.date); if(!ss.length) return "";
  const isToday = WZ.date===todayStr(), isPastDate = WZ.date < todayStr(), nowM = toMin(nowHM());
  const curT = WZ.time ? toMin(WZ.time) : null, curSlot = curT===null ? null : Math.floor(curT/30)*30;
  const people = WZ.people || 0;""", """function sessionGrid(){ return timeGrid({date:WZ.date, people:WZ.people||0, time:WZ.time, pick:"wzPickSlot"}); }
function timeGrid(ctx){
  const s = store(), st = s.settings, dh = hoursFor(ctx.date);
  if(dh.closed) return `<div class="empty">휴무일입니다. 아래 '접수 시간 밖' 에서 그래도 받을 수 있습니다.</div>`;
  const ss = sessionsFor(ctx.date); if(!ss.length) return "";
  const isToday = ctx.date===todayStr(), isPastDate = ctx.date < todayStr(), nowM = toMin(nowHM());
  const curT = ctx.time ? toMin(ctx.time) : null, curSlot = curT===null ? null : Math.floor(curT/30)*30;
  const people = ctx.people || 0;""")
s = s.replace("""      const freeRooms = rooms.filter(x=>!blockedAt(x, WZ.date, hmS) && (!people || (people >= roomMin(x, WZ.date) && people <= seatMax(x))) && roomStatus(WZ.date, hmS, x.id).state === "free").length;
      const tf = people ? floorFit(null, WZ.date, hmS, people) : null;""", """      const freeRooms = rooms.filter(x=>!blockedAt(x, ctx.date, hmS) && (!people || (people >= roomMin(x, ctx.date) && people <= seatMax(x))) && roomStatus(ctx.date, hmS, x.id).state === "free").length;
      const tf = people ? floorFit(null, ctx.date, hmS, people) : null;""")
s = s.replace("""      const cnt = s.reservations.filter(r=>r.date===WZ.date && holdsSeat(r) && Math.floor(toMin(r.time)/30)*30===t).length;
      const bad = (people && freeRooms===0 && (!tf || tf.state==="none"));
      cells.push(`<button class="hcell big ${curSlot===t?'on':''} ${gone?'gone':''} ${bad?'busy':''}" onclick="wzPickSlot(${t})">""", """      const cnt = s.reservations.filter(r=>r.date===ctx.date && holdsSeat(r) && Math.floor(toMin(r.time)/30)*30===t).length;
      const bad = (people && freeRooms===0 && (!tf || tf.state==="none"));
      cells.push(`<button class="hcell big ${curSlot===t?'on':''} ${gone?'gone':''} ${bad?'busy':''}" onclick="${ctx.pick}(${t})">""")
# syncRes 는 hidden input 을 읽으므로 그대로 동작. pickDate/pickTime/calMonth 는 저장 전 지움
s = R(s, """  delete rec.__id; delete rec.adults; delete rec.courseOpen;""", """  delete rec.__id; delete rec.adults; delete rec.courseOpen; delete rec.pickDate; delete rec.pickTime; delete rec.calMonth;""")

# ---------- 기기 보정 → 더보기 '화면 보정' ----------
s = R(s, """    <label class="f"><div class="lb">이 기기만 보정 <span class="lbl-note">바로 적용 · PC 는 +10, 아이패드는 0 처럼</span></div>
      <span class="seg"><button onclick="setZoomAdj(-5)">−5</button><button class="on" style="min-width:64px">${zAdj>0?"+":""}${zAdj}</button><button onclick="setZoomAdj(5)">+5</button></span>
      <div class="f-note">지금 이 기기 화면 크기: <b>${uiZoom()}%</b> (공통 ${zBase}% ${zAdj>=0?"+":""}${zAdj}). 전체화면에서 커 보이면 여기서 −5·−10.</div></label>""",
"""    <p class="f-note">기기마다 다르게 보이면 더보기 → <b>화면 보정</b>(이 기기만, 바로 반영). 지금 이 기기: <b>${uiZoom()}%</b> (공통 ${zBase}% ${zAdj>=0?"+":""}${zAdj}).</p>""")
s = R(s, """              <button onclick="closeMore(); setTab('settings')">${ICON.set}<span>설정</span></button>
              <button onclick="closeMore(); lockNow()">${ICON.exit}<span>로그아웃</span></button>""",
"""              <button onclick="closeMore(); openZoomAdj()">${ICON.search}<span>화면 보정</span></button>
              <button onclick="closeMore(); setTab('settings')">${ICON.set}<span>설정</span></button>
              <button onclick="closeMore(); lockNow()">${ICON.exit}<span>로그아웃</span></button>""")
s = R(s, """function openHours(){ view.form={type:"hours"}; render(); }""", """function openHours(){ view.form={type:"hours"}; render(); }
function openZoomAdj(){ view.form={type:"zoomadj"}; render(); }
function sheetZoomAdj(){
  const adj = (DATA._ui && DATA._ui.zoomAdj) || 0, base = ZOOM_STEPS.indexOf(store().settings.uiZoom) >= 0 ? store().settings.uiZoom : 100;
  return `${sheetHead("화면 보정")}
    <p class="f-note" style="margin-top:-6px">이 기기에서만 크기를 조금 키우거나 줄입니다. 모든 기기 공통 크기는 설정 → 화면 크기.</p>
    <div class="zoomadj"><button class="btn" onclick="setZoomAdj(-5)">− 5</button><div class="za-v"><b>${uiZoom()}%</b><small>공통 ${base}% ${adj>=0?"+":""}${adj}</small></div><button class="btn" onclick="setZoomAdj(5)">＋ 5</button></div>
    <div class="btn-row" style="justify-content:center; margin-top:10px"><button class="btn sm ghost" onclick="setZoomAdj(-(${adj}))">보정 없음(0)</button></div>`;
}""")
s = R(s, """tedit:sheetTableEdit, naver:sheetNaver, setlog:sheetSetLog, pinlist:sheetPinList, logs:sheetLogs,""", """tedit:sheetTableEdit, naver:sheetNaver, setlog:sheetSetLog, pinlist:sheetPinList, zoomadj:sheetZoomAdj, logs:sheetLogs,""")
s = R(s, """.tk.end b{}""", """.tk.end b{}
.zoomadj{display:flex; align-items:center; justify-content:center; gap:var(--s16)} .zoomadj .btn{min-width:72px}
.za-v{text-align:center; min-width:96px} .za-v b{display:block; font-size:var(--fs-num)} .za-v small{color:var(--text-3)}""")

# ---------- 시트 최대 높이: zoom 보정 ----------
s = R(s, """.sheet{width:100%; max-width:560px; max-height:90vh;""", """.sheet{width:100%; max-width:560px; max-height:calc(90vh / var(--ui-zoom, 1));""")

# ---------- 목록: '지금' 구분선, 지난 것 더 흐리게 ----------
s = R(s, """  const rows = day.length ? day.map(resRow).join("")""", """  /* 8차-V(재아): 오늘 목록에는 '지금' 선을 넣어 위(지난)·아래(앞으로) 가 갈리게 */
  const nowM = toMin(nowHM()), isToday = date === todayStr();
  let marked = false;
  const rows = day.length ? day.map(r=>{
    let m = "";
    if(isToday && !marked && toMin(r.time) > nowM){ marked = true; m = `<div class="now-sep"><span>지금 ${hm(nowHM())}</span></div>`; }
    return m + resRow(r);
  }).join("") + (isToday && !marked ? `<div class="now-sep"><span>지금 ${hm(nowHM())} · 오늘 남은 예약 없음</span></div>` : "")""")
s = R(s, """.rrow.late{opacity:.55}""", """.rrow.late{opacity:.45; filter:grayscale(1)}
.rrow.s-방문, .rrow.s-취소, .rrow.s-노쇼{filter:grayscale(1)}
.now-sep{display:flex; align-items:center; gap:var(--s8); color:var(--rust); font-size:var(--fs-label); font-weight:700; padding:2px var(--s8)}
.now-sep:before, .now-sep:after{content:""; flex:1; height:2px; background:var(--rust)}""")

# ---------- 이른 방문 처리 되묻기 ----------
s = R(s, """  if(rec) logEvent("상태 변경", `${rec.date} ${rec.time} ${rec.name} ${rec.status} → ${status}`);
  /* 취소·노쇼는 화이트보드에서 지워야 하는 건이라 반드시 남깁니다.
     '방문'은 자동 처리라 변동으로 세지 않습니다 (매일 전부 표시되면 의미가 없어집니다) */
  s.reservations = s.reservations.map(function(r){
    if(r.id!==id) return r;
    const n = touch({...r, status});
    if(status==="취소" || status==="노쇼") addChange(n, status, []);
    else if(status==="확정" && (r.status==="취소" || r.status==="노쇼")) addChange(n, "변경", [{n:"상태", a:r.status, b:"확정"}]);   /* 되돌림도 남겨야 '오늘 취소' 태그가 풀립니다(점검 R3) */
    return n;
  });
  if(rec) reflowTentatives(rec.date);
  if(status === "취소") view.form = null;   /* 방문·노쇼·되돌림은 시트를 그대로 둡니다(재아) */
  saveData(); render();
}""", """  /* 예약 시각까지 1시간 넘게 남았는데 방문을 누르면 되묻습니다(손이 미끄러진 경우가 많음). 그래도 누르면 그대로 방문 */
  if(status==="방문" && rec && rec.status!=="방문"){
    const left = (new Date(rec.date + "T" + rec.time + ":00") - new Date()) / 60000;
    if(left > 60 && !await uiConfirm("예약 시각이 아직 멀었습니다", `${rec.time} ${rec.name} 손님 · 예약까지 ${hmDur(Math.round(left))} 남음\\n지금 방문 처리할까요?`, {ok:"방문 처리", cancel:"아니요"})) return;
  }
  if(rec) logEvent("상태 변경", `${rec.date} ${rec.time} ${rec.name} ${rec.status} → ${status}`);
  /* 취소·노쇼는 화이트보드에서 지워야 하는 건이라 반드시 남깁니다.
     '방문'은 자동 처리라 변동으로 세지 않습니다 (매일 전부 표시되면 의미가 없어집니다) */
  s.reservations = s.reservations.map(function(r){
    if(r.id!==id) return r;
    const n = touch({...r, status});
    if(status==="취소" || status==="노쇼") addChange(n, status, []);
    else if(status==="확정" && (r.status==="취소" || r.status==="노쇼")) addChange(n, "변경", [{n:"상태", a:r.status, b:"확정"}]);   /* 되돌림도 남겨야 '오늘 취소' 태그가 풀립니다(점검 R3) */
    return n;
  });
  if(rec) reflowTentatives(rec.date);
  if(status === "취소") view.form = null;   /* 방문·노쇼·되돌림은 시트를 그대로 둡니다(재아) */
  saveData(); render();
}""")

# ---------- 나뉨 기호 ⊕ ----------
s = R(s, """        ${it.joined?`<i class="jn">${(joinOf(seatsOf(it.r))||{}).split?"⊟":"⊞"}</i>`:''}""", """        ${it.joined?`<i class="jn">${(joinOf(seatsOf(it.r))||{}).split?"⊕":"⊞"}</i>`:''}""")
s = R(s, """        <span class="tl-legend sym" title="룸 합침인데 공간이 나뉨(원탁) — 손님 확인">⊟ 나뉨</span>""", """        <span class="tl-legend sym" title="룸 합침인데 공간이 나뉨(원탁) — 손님 확인">⊕ 나뉨</span>""")
L.js_check(s)
L.save(s)
print("p9_v ok")
