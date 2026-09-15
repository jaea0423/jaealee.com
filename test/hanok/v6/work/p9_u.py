# -*- coding: utf-8 -*-
"""8차-U — 재아 목록 5차: 더보기 순서·아이콘·예약률 추이는 관리자로, 설정 문구·적용 버튼 색·구분선 문구 삭제, 목록 행 자체 색,
   상단 칩(확정·경고·오늘 변경·요청·메모 | 확인 필요) + 지표 카드 삭제, 영업시간·검색 시트 닫기 버튼 삭제,
   달력 칸(일자/막대/N건(P%)·휴무 빗금), 시각 선택 개편(세션별 접수 가능 시각만·빈 룸/테이블 표시·나머지는 접기),
   확인 필요에 '더 나은 자리 가능', 예약지 세로 넘침"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 더보기 ----------
s = R(s, """              ${isMobile() && view.date!==todayStr() ? `<button onclick="closeMore(); goToday()">${ICON.cal}<span>오늘로</span></button>` : ``}
              <button onclick="closeMore(); openRate()">${ICON.chart}<span>예약률 추이</span></button>
              <button onclick="closeMore(); openHours()">${ICON.clock}<span>영업시간</span></button>
              <button onclick="closeMore(); setTab('settings')">${ICON.set}<span>설정</span></button>
              <button onclick="closeMore(); openDisplay()">${ICON.tv}<span>디스플레이 모드</span></button>
              ${document.fullscreenEnabled ? `<button onclick="closeMore(); toggleFullscreen()">${ICON.tv}<span>${document.fullscreenElement?"전체화면 해제":"전체화면"}</span></button>` : ""}
              <button onclick="closeMore(); lockNow()">${ICON.exit}<span>로그아웃</span></button>""",
"""              ${isMobile() && view.date!==todayStr() ? `<button onclick="closeMore(); goToday()">${ICON.cal}<span>오늘로</span></button>` : ``}
              <button onclick="closeMore(); openHours()">${ICON.clock}<span>영업시간</span></button>
              <button onclick="closeMore(); openDisplay()">${ICON.tv}<span>디스플레이 모드</span></button>
              ${document.fullscreenEnabled ? `<button onclick="closeMore(); toggleFullscreen()">${document.fullscreenElement?ICON.shrink:ICON.expand}<span>${document.fullscreenElement?"전체화면 해제":"전체화면"}</span></button>` : ""}
              <button onclick="closeMore(); setTab('settings')">${ICON.set}<span>설정</span></button>
              <button onclick="closeMore(); lockNow()">${ICON.exit}<span>로그아웃</span></button>""")
s = R(s, """const ICON = {""", """const ICON = {
  expand:'<svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>',
  shrink:'<svg viewBox="0 0 24 24"><path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5"/></svg>',""")
s = R(s, """      <button class="btn" onclick="openLogs()">로그</button>
      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>""", """      <button class="btn" onclick="openLogs()">로그</button>
      <button class="btn" onclick="openRate()">예약률 추이</button>
      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>""")

# ---------- 설정 문구·버튼 ----------
s = R(s, """    <div class="set-divider"><span>아래는 적용하기 없이 바로 반영됩니다</span></div>""", """    <div class="set-divider"></div>""")
s = R(s, """    ${dirty ? `<div class="applybar on"><span class="ab-t">저장하지 않은 변경이 있습니다 — 위 '적용하기'</span></div>` : ""}`;""",
         """    ${dirty ? `<div class="applybar on"><span class="ab-t">저장하지 않은 변경이 있습니다</span></div>` : ""}`;""")
s = R(s, """          <button class="tvbtn accent b-apply" onclick="applySettings()" ${settingsDirty()?"":"disabled"}>적용하기</button>""",
         """          <button class="tvbtn amber b-apply" onclick="applySettings()" ${settingsDirty()?"":"disabled"}>적용하기</button>""")
s = R(s, """.tk.end b{}""", """.tk.end b{}
.tvbtn.amber{background:#F3E2B3; color:#5A4A1E; border-color:#E2C97F} .tvbtn.amber:not(:disabled):hover{background:#EED89A}
.topbar.notoday .tvbtn.amber{background:#F3E2B3; color:#5A4A1E}""")

# ---------- 목록: 왼쪽 띠 대신 행 자체 색 ----------
s = R(s, """.rrow{position:relative; padding-left:calc(var(--s8) + 6px)}
.rrow:before{content:""; position:absolute; left:0; top:4px; bottom:4px; width:5px; border-radius:3px; background:#3A3833}
.rrow.k-warn:before{background:var(--rust)}
.rrow.k-chg:before{background:linear-gradient(180deg, #3D8BD9 0 50%, #3A3833 50%)}
.rrow.k-warn.k-chg:before{background:linear-gradient(180deg, #3D8BD9 0 50%, var(--rust) 50%)}
.rrow.k-tent:before{background-image:repeating-linear-gradient(-45deg, rgba(255,255,255,.5) 0 3px, transparent 3px 6px)}
.rrow.s-방문:before, .rrow.s-취소:before, .rrow.s-노쇼:before{opacity:.35}""",
"""/* 행 자체를 타임라인 블록처럼: 경고=옅은 벽돌 바탕, 오늘 변동=앞 절반 옅은 파랑, 룸 미정=빗금. 지난·방문·취소는 흐림 */
.rrow.k-warn{background:var(--rust-soft)}
.rrow.k-chg{background-image:linear-gradient(90deg, #DCEBF9 0, #DCEBF9 42%, rgba(220,235,249,0) 52%)}
.rrow.k-warn.k-chg{background-color:var(--rust-soft)}
.rrow.k-tent{background-image:repeating-linear-gradient(-45deg, rgba(58,56,51,.07) 0 4px, transparent 4px 10px)}
.rrow.k-tent.k-chg{background-image:linear-gradient(90deg, #DCEBF9 0, #DCEBF9 42%, rgba(220,235,249,0) 52%), repeating-linear-gradient(-45deg, rgba(58,56,51,.07) 0 4px, transparent 4px 10px)}
.rrow.s-방문, .rrow.s-노쇼{opacity:.6}""")

# ---------- 상단 칩: 확정·경고·오늘 변경·요청·메모 | 확인 필요. 아래 지표 카드 삭제 ----------
s = R(s, """          const cnt = {
            미정: tentCount,
            경고: live.filter(x=>resWarn(x).length).length,
            변경: day.filter(x=>changeTag(x)).length,
            요청: live.filter(x=>(x.request||"").trim()).length,
            메모: live.filter(x=>(x.memo||"").trim()).length,
            노쇼: day.filter(x=>x.status==="노쇼").length,
            취소: day.filter(x=>x.status==="취소").length
          };
          /* 파랑 = 우리끼리 남긴 표시(변경·메모), 벽돌색 = 손이 가야 할 것 */
          const cls = {미정:"amber", 경고:"rust", 변경:"blue", 요청:"", 메모:"blue", 노쇼:"rust", 취소:""};
          const nm  = {미정:"좌석 미정", 요청:"요청사항"};
          return Object.keys(cnt).filter(k=>cnt[k])
            .map(k=>`<span class="tag ${cls[k]}">${nm[k]||k} ${cnt[k]}건</span>`).join("");""",
"""          /* 8차-U(재아): 확정·경고·오늘 변경·요청·메모만, 누르면 목록. 확인 필요는 맨 오른쪽. 아래 지표 카드는 없앴습니다 */
          const cnt = {
            확정: live.filter(x=>x.status==="확정").length,
            경고: live.filter(x=>resWarn(x).length).length,
            변경: day.filter(x=>changeTag(x)).length,
            요청: live.filter(x=>(x.request||"").trim()).length,
            메모: live.filter(x=>(x.memo||"").trim()).length
          };
          const cls = {확정:"", 경고:"rust", 변경:"blue", 요청:"", 메모:"blue"};
          const nm  = {변경:"오늘 변경", 요청:"요청사항"};
          const act = {확정:"openPick('confirmed')", 경고:"openPick('warn')", 변경:"openPick('changed')", 요청:"openPick('request')", 메모:"openPick('memo')"};
          const chk = checkItems(date).length;
          return Object.keys(cnt).filter(k=>cnt[k])
            .map(k=>`<button class="tag tapchip ${cls[k]}" onclick="${act[k]}">${nm[k]||k} ${cnt[k]}건</button>`).join("")
            + `<button class="tag tapchip ${chk?'amber':''} right" onclick="openCheck()">확인 필요 ${chk}건</button>`;""")
s = R(s, """    warn:{title:"경고 예약", pick:r=>resWarn(r).length>0, note:"사장 판단으로 접수된 예약입니다. 문제가 없는지 확인하세요."},""",
"""    warn:{title:"경고 예약", pick:r=>resWarn(r).length>0, note:"사장 판단으로 접수된 예약입니다. 문제가 없는지 확인하세요."},
    confirmed:{title:"확정 예약", pick:r=>true, note:""},
    request:{title:"요청사항 있는 예약", pick:r=>!!(r.request||"").trim(), note:"요청이 가능한지, 주방·홀에 전달됐는지 확인하세요."},
    memo:{title:"메모 있는 예약", pick:r=>!!(r.memo||"").trim(), note:""},""")
s = R(s, """  if(isMobile()) return renderDashMobile(d, {active, unassigned, warnCnt, checkCnt, stat});
  return `
    <div class="card"><div class="card-b">${renderTimeline(d)}</div></div>
    ${metrics}""", """  if(isMobile()) return renderDashMobile(d, {active, unassigned, warnCnt, checkCnt, stat});
  return `
    <div class="card"><div class="card-b">${renderTimeline(d)}</div></div>""")
s = R(s, """.tk.end b{}""", """.tk.end b{}
.tag.tapchip{cursor:pointer; font:inherit; font-size:var(--fs-sub); font-weight:600} .tag.tapchip.right{margin-left:auto}
.tl-kpis{display:flex; align-items:center; flex-wrap:wrap; gap:var(--s8)}""")

# ---------- 영업시간·검색 시트 닫기 버튼 삭제 ----------
s = R(s, """    <div class="card searchbox">${rows}</div>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;""", """    <div class="card searchbox">${rows}</div>`;""")
import re
m = re.search(r"function sheetHours\(\)\{.*?\n\}", s, re.S)
assert m, "sheetHours"
body = m.group(0)
body2 = body.replace("""    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>""", "")
assert body2 != body, "hours close btn"
s = s.replace(body, body2)

# ---------- 달력 칸: 일자 / 막대 / N건 (P%) · 휴무 빗금 ----------
s = R(s, """    cells += `<button class="${cls}" onclick="pickCalDate('${ds}',true)">
      <span class="dn">${d}</span>
      ${st.count?`<span class="cn">${st.count}건</span>
        <span class="cbar"><i style="width:${st.rate}%"></i></span>
        <span class="cr">${st.rate}%</span>`:`<span class="cn none">-</span>`}
    </button>`;""", """    const closedDay = hoursFor(ds).closed;
    cells += `<button class="${cls} ${closedDay?'closed':''}" onclick="pickCalDate('${ds}',true)">
      <span class="dn">${d}</span>
      ${closedDay?`<span class="cn none">휴무</span>`:`<span class="cbar"><i style="width:${st.rate}%"></i></span>
        <span class="cn">${st.count}건 <small>(${st.rate}%)</small></span>`}
    </button>`;""")
s = R(s, """.tk.end b{}""", """.tk.end b{}
.cday.closed{background-image:repeating-linear-gradient(-45deg, rgba(58,56,51,.08) 0 4px, transparent 4px 10px)}
.cday .cn small{font-weight:500; color:var(--text-3)}""")

# ---------- 시각 선택 개편: 세션별 접수 가능 시각만 크게, 빈 룸/테이블 표시. 나머지는 접힘 ----------
s = R(s, """      <div class="lbl" style="margin-bottom:8px">${WZ.date?dateLabel(WZ.date):"날짜를 먼저 고르세요"} · 시각</div>
      <div class="hgrid">${slotCells}</div>""", """      <div class="lbl" style="margin-bottom:8px">${WZ.date?dateLabel(WZ.date):"날짜를 먼저 고르세요"} · 시각</div>
      ${sessionGrid()}
      <details class="hmore" ${WZ.showAllSlots?"open":""} ontoggle="WZ.showAllSlots=this.open"><summary>접수 시간 밖 시각 보기 <span class="lbl-note">영업 전·브레이크·접수 마감 뒤 — 경고가 붙습니다</span></summary>
      <div class="hgrid">${slotCells}</div></details>""")
s = R(s, """function wzStepDate(){""", """/* 8차-U(재아): 시각 선택 — 그날 세션(점심/저녁)마다 '접수 가능한 시각' 만 큼직하게. 칸에는 이 인원이 앉을 빈 룸 수·테이블 가능 여부.
   영업 밖·브레이크·접수 마감 뒤 시각은 아래 '접수 시간 밖' 에 접어 둡니다(경고 붙여서 받을 수는 있음) */
function sessionGrid(){
  const s = store(), st = s.settings, dh = hoursFor(WZ.date);
  if(dh.closed) return `<div class="empty">휴무일입니다. 아래 '접수 시간 밖' 에서 그래도 받을 수 있습니다.</div>`;
  const ss = sessionsFor(WZ.date); if(!ss.length) return "";
  const isToday = WZ.date===todayStr(), isPastDate = WZ.date < todayStr(), nowM = toMin(nowHM());
  const curT = WZ.time ? toMin(WZ.time) : null, curSlot = curT===null ? null : Math.floor(curT/30)*30;
  const people = WZ.people || 0;
  const rooms = st.rooms.filter(isRoom);
  return ss.map(se=>{
    const from = toMin(se.from), last = toMin(se.lastBook);
    const cells = [];
    for(let t = from; t <= last; t += 30){
      if(dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be)) continue;
      const hmS = minToHM(t);
      const gone = isPastDate || (isToday && t+30 <= nowM);
      const freeRooms = rooms.filter(x=>!blockedAt(x, WZ.date, hmS) && (!people || (people >= roomMin(x, WZ.date) && people <= seatMax(x))) && roomStatus(WZ.date, hmS, x.id).state === "free").length;
      const tf = people ? floorFit(null, WZ.date, hmS, people) : null;
      const tTxt = !people ? "" : tf.state==="ok" ? "테이블 가능" : tf.state==="split" ? "테이블 나눠" : "테이블 없음";
      const cnt = s.reservations.filter(r=>r.date===WZ.date && holdsSeat(r) && Math.floor(toMin(r.time)/30)*30===t).length;
      const bad = (people && freeRooms===0 && (!tf || tf.state==="none"));
      cells.push(`<button class="hcell big ${curSlot===t?'on':''} ${gone?'gone':''} ${bad?'busy':''}" onclick="wzPickSlot(${t})">
        <span class="hh">${hm(hmS).replace(/^(오전|오후) /,"")}</span><span class="ap">${t<720?"오전":"오후"}</span>
        <span class="hn">${gone?"지난 시간":(people?`룸 ${freeRooms} · ${tTxt}`:(cnt?`${cnt}건`:"&nbsp;"))}</span>
      </button>`);
    }
    return `<div class="sess-h2"><b>${esc(se.name)}</b><span class="lbl-note">${se.from}부터 · 접수 ${se.lastBook}까지${se.stay==="end"?" · 세션 끝까지 한 팀":` · ${se.stay}분`}</span></div><div class="hgrid sess">${cells.join("")}</div>`;
  }).join("");
}
function wzStepDate(){""")
s = R(s, """.tk.end b{}""", """.tk.end b{}
.sess-h2{display:flex; align-items:baseline; gap:var(--s8); margin:var(--s12) 0 var(--s8); font-size:var(--fs-body)}
.hgrid.sess{grid-template-columns:repeat(auto-fill,minmax(96px,1fr)); margin-bottom:var(--s8)}
.hcell.big{height:auto; min-height:76px; padding:var(--s8) var(--s4)}
.hcell.big .hh{font-size:var(--fs-title); font-weight:700} .hcell.big .ap{order:-1; font-size:var(--fs-label); color:var(--text-3)}
.hcell.big .hn{font-size:var(--fs-label); color:var(--text-2); margin-top:2px; white-space:nowrap}
.hcell.big.busy .hn{color:var(--rust)} .hcell.big.on .hn{color:inherit}
.hmore{margin-top:var(--s8)} .hmore summary{cursor:pointer; font-size:var(--fs-sub); color:var(--text-2); padding:var(--s8) 0; list-style:none}
.hmore summary::-webkit-details-marker{display:none} .hmore summary:before{content:"▸ "} .hmore[open] summary:before{content:"▾ "}""")

# ---------- 확인 필요: 더 나은 자리 가능 ----------
s = R(s, """  if(ns.length) items.push(["rust", `노쇼 이력 손님 ${ns.length}건`,""", """  /* 8차-U(재아): 취소 등으로 자리가 나서, 나눠 앉거나 자리 없던 예약을 한 자리로 옮길 수 있게 된 것 */
  const better = live.filter(r=>{
    if(!isTablePref(r.seatPref)) return false;
    if(!(r.tentativeSplit || !r.tentativeRoomId)) return false;
    const f = floorFit(prefFloor(r.seatPref), r.date, r.time, pplOf(r), r.id);
    return f.state === "ok";
  });
  if(better.length) items.push(["pine", `자리 개선 가능 ${better.length}건`, "나눠 앉거나 자리 없던 테이블 예약에 한 자리가 났습니다. 새로고침하면 다시 배정됩니다.", "openPick('better')"]);
  if(ns.length) items.push(["rust", `노쇼 이력 손님 ${ns.length}건`,""")
s = R(s, """    confirmed:{title:"확정 예약", pick:r=>true, note:""},""", """    confirmed:{title:"확정 예약", pick:r=>true, note:""},
    better:{title:"자리 개선 가능", pick:r=>isTablePref(r.seatPref) && (r.tentativeSplit || !r.tentativeRoomId) && floorFit(prefFloor(r.seatPref), r.date, r.time, pplOf(r), r.id).state==="ok", note:"취소 등으로 자리가 났습니다. 다시 계산되면 한 자리로 배정됩니다."},""")
L.js_check(s)
L.save(s)
print("p9_u ok")
