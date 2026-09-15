# -*- coding: utf-8 -*-
"""8차-S — 재아 목록 4차: 타임라인 '나눠' 글자 삭제, 화면 크기(90/95 추가·적용하기로·기기 보정), 설정을 '적용 필요 / 바로 적용' 으로 나눔,
   일괄 등록 프롬프트가 사용자에게 되묻게, 관리자에 비상 예약지, PIN 관리(목록·관리자 비번 게이트), 로그 시트(이용 로그·설정 로그 탭)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 타임라인: 붙임 이름 뒤 '나눠' 글자 삭제(↔ 로 충분) ----------
s = R(s, """      const tn = it.r.roomId ? seatLabelIds(seatsOf(it.r)).replace(/ 테이블$/,"") : tableHint(it.r).replace(/^ \\(|\\)$/g,"");""",
         """      const tn = it.r.roomId ? seatLabelIds(seatsOf(it.r)).replace(/ 테이블$/,"") : tableHint(it.r).replace(/^ \\(|\\)$/g,"").replace(/ 나눠$/,"");""")

# ---------- 화면 크기: 90·95, 매장 공유값은 적용하기로, 기기 보정은 즉시 ----------
s = R(s, """const ZOOM_STEPS = [100, 105, 110, 120, 135];""", """const ZOOM_STEPS = [90, 95, 100, 105, 110, 120, 135];""")
s = R(s, """function uiZoom(){
  const shared = view.storeKey && DATA && DATA[view.storeKey] && DATA[view.storeKey].settings ? DATA[view.storeKey].settings.uiZoom : null;   /* 매장 설정에 공유(재아) */
  const z = shared != null ? shared : (DATA && DATA._ui ? DATA._ui.zoom : null);
  return ZOOM_STEPS.indexOf(z) >= 0 ? z : 100;   /* 기본 100%(재아) */
}""", """/* 화면 크기 = 매장 공유값(설정 → 적용하기) + 이 기기 보정(즉시). PC 는 110 이 맞고 아이패드는 100 이 맞는 식이라 보정을 둡니다 */
function uiZoom(){
  const shared = view.storeKey && DATA && DATA[view.storeKey] && DATA[view.storeKey].settings ? DATA[view.storeKey].settings.uiZoom : null;
  const base = ZOOM_STEPS.indexOf(shared) >= 0 ? shared : 100;
  const adj = DATA && DATA._ui && typeof DATA._ui.zoomAdj === "number" ? DATA._ui.zoomAdj : 0;
  return Math.max(70, Math.min(160, base + adj));
}
function setZoomAdj(d){ DATA._ui = DATA._ui || {}; DATA._ui.zoomAdj = Math.max(-20, Math.min(20, (DATA._ui.zoomAdj||0) + d)); uiSave(); applyTheme(); render(); }""")
s = R(s, """function setZoom(z){
  DATA._ui = DATA._ui || {};
  DATA._ui.zoom = z;
  if(view.storeKey && store()){ store().settings.uiZoom = z; mirrorDraft("uiZoom"); }   /* 모든 기기에 같이 */
  logEvent("설정 변경", `화면 크기 ${z}%`);
  saveData(); render();
}""", """function setZoom(z){ draft().uiZoom = z; render(); }   /* 매장 공유값 — '적용하기' 를 눌러야 반영(재아) */""")
s = R(s, """  const zoomBody = `
    <div class="seg zoomseg">${ZOOM_STEPS.map(function(z){
      return `<button class="${uiZoom()===z?'on':''}" onclick="setZoom(${z})">${z}%</button>`;
    }).join("")}</div>""", """  const zBase = ZOOM_STEPS.indexOf(st.uiZoom) >= 0 ? st.uiZoom : 100, zAdj = (DATA._ui && DATA._ui.zoomAdj) || 0;
  const zoomBody = `
    <div class="lbl">모든 기기 공통 <span class="lbl-note">적용하기를 눌러야 반영</span></div>
    <div class="seg zoomseg">${ZOOM_STEPS.map(function(z){
      return `<button class="${zBase===z?'on':''}" onclick="setZoom(${z})">${z}%</button>`;
    }).join("")}</div>
    <label class="f"><div class="lb">이 기기만 보정 <span class="lbl-note">바로 적용 · PC 는 +10, 아이패드는 0 처럼</span></div>
      <span class="seg"><button onclick="setZoomAdj(-5)">−5</button><button class="on" style="min-width:64px">${zAdj>0?"+":""}${zAdj}</button><button onclick="setZoomAdj(5)">+5</button></span>
      <div class="f-note">지금 이 기기 화면 크기: <b>${uiZoom()}%</b> (공통 ${zBase}% ${zAdj>=0?"+":""}${zAdj}). 전체화면에서 커 보이면 여기서 −5·−10.</div></label>""")

# ---------- 설정 순서: 적용하기가 필요한 것 / 바로 적용되는 것 ----------
s = R(s, """    ${sec("admin","관리자",`PIN · 비밀번호 · 기록`, adminBody)}
    ${sec("policy","운영 판단 기준",""", """    ${sec("policy","운영 판단 기준",""")
s = R(s, """    ${sec("zoom","화면 크기",`${uiZoom()}%`, zoomBody)}
    ${sec("etc","기타",`기록 ${(DATA._logs||[]).length}건`, etcBody)}""", """    ${sec("zoom","화면 크기",`${uiZoom()}%`, zoomBody)}
    <div class="set-divider"><span>아래는 적용하기 없이 바로 반영됩니다</span></div>
    ${sec("admin","관리자",`PIN · 로그 · 초기화`, adminBody)}
    ${sec("etc","기타",`노쇼 관리`, etcBody)}""")
s = R(s, """.tk.end b{}   /* 예약률 글자를 빼서 오른쪽에 자리가 생겼으니 다른 눈금과 같게 */""", """.tk.end b{}
.set-divider{display:flex; align-items:center; gap:var(--s12); margin:var(--s24) 0 var(--s8); color:var(--text-3); font-size:var(--fs-sub)}
.set-divider:before, .set-divider:after{content:""; flex:1; height:1px; background:var(--border-strong)}""")

# ---------- 일괄 등록 프롬프트: 먼저 사용자에게 되묻게 ----------
s = R(s, """  const txt = "아래 형식으로 한 줄에 하루씩 써 줘. 다른 말은 붙이지 말고 줄만.\\n형식: 날짜 | 메모 | 내용""",
         """  const txt = "우리 식당(한옥반점) 예약 시스템에 넣을 임시 휴무·영업시간 목록을 만들어 줘.\\n먼저 나에게 물어봐: ① 몇 년도 공휴일이 필요한지(대체공휴일 포함 여부) ② 휴무로 할 날과 임시 영업시간으로 할 날 ③ 임시 영업시간이면 영업·라스트오더·브레이크 시간. 답을 받은 뒤에 아래 형식으로 한 줄에 하루씩만 출력해(다른 말 없이).\\n형식: 날짜 | 메모 | 내용""")

# ---------- 관리자: 비상 예약지, PIN 관리, 로그 ----------
s = R(s, """    <div class="btn-row">
      <button class="btn" onclick="openPin()">PIN 번호 변경</button>
      ${supaOn() ? `<button class="btn" onclick="openAdminPw()">관리자 비밀번호 변경</button>` : ""}
      <button class="btn" onclick="openLogs()">접속 기록</button>
      <button class="btn" onclick="openSetLog()">설정 변경 내역</button>
      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>
    </div>
    <div class="subhead" style="margin-top:14px">PIN 목록</div>
    <div class="rowitem"><span class="grow"><span class="t">공용 <span class="tag pine">사용 중</span></span><span class="s">직원 모두가 쓰는 PIN. 접속 기록에는 '공용' 으로 남습니다.</span></span></div>
    <p class="f-note">직원마다 다른 PIN(이름별)은 나중에 여기서 추가·삭제하게 만들 수 있습니다. 그러면 기록에 직원 이름이 남습니다(누님 질문 15).</p>""",
"""    <div class="btn-row">
      <button class="btn" onclick="openPinManage()">PIN 번호 관리</button>
      ${supaOn() ? `<button class="btn" onclick="openAdminPw()">관리자 비밀번호 변경</button>` : ""}
      <button class="btn" onclick="openLogs()">로그</button>
      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>
      <a class="btn" href="${location.pathname.indexOf('/dev/')>=0?'../':''}비상예약지.html" target="_blank" rel="noopener">비상 예약지 인쇄</a>
    </div>
    <p class="f-note">비상 예약지: 시스템이 안 될 때 손으로 받는 종이(A4 한 장에 6장). 열리면 Ctrl+P 로 인쇄해 카운터에 두세요.</p>""")
# PIN 관리 시트
s = R(s, """function openPin(){ view.form={type:"pin"}; render(); }""", """function openPin(){ view.form={type:"pin"}; render(); }
async function openPinManage(){ if(!await adminGate("PIN 번호 관리")) return; view.form={type:"pinlist"}; render(); }
function sheetPinList(){
  return `
    ${sheetHead("PIN 번호 관리")}
    <div class="rowitem"><span class="grow"><span class="t">공용 <span class="tag pine">사용 중</span></span><span class="s">직원 모두가 쓰는 PIN · 로그에는 '공용(staff)' 으로 남습니다</span></span>
      <button class="btn sm" onclick="openPin()">번호 바꾸기</button></div>
    <div class="btn-row" style="margin-top:12px"><button class="btn" disabled title="직원별 PIN 은 서버 계정을 하나씩 만들어야 해서 다음 단계에서">＋ 직원 PIN 추가 (준비 중)</button></div>
    <p class="f-note">직원마다 다른 PIN 을 만들면 로그에 이름이 남고, 그만두면 그 PIN 만 지우면 됩니다. 서버 쪽 준비가 필요해 지금은 공용 하나입니다. 추가·삭제할 때도 관리자 비밀번호를 한 번 더 묻게 만듭니다.</p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}""")
s = R(s, """tedit:sheetTableEdit, naver:sheetNaver, setlog:sheetSetLog, logs:sheetLogs,""", """tedit:sheetTableEdit, naver:sheetNaver, setlog:sheetSetLog, pinlist:sheetPinList, logs:sheetLogs,""")
# 로그 시트: 탭(이용 로그 / 설정 로그)
s = R(s, """  return `
    ${sheetHead("접속 기록")}
    <div class="row" style="margin-bottom:10px">
      <input id="log-q" value="${esc(q)}" placeholder="검색 (동작·IP·날짜)" oninput="setLogQuery(this.value)" style="flex:1">
      <button class="btn" onclick="copyLogs()">전체 복사</button>
    </div>
    <div class="logbox">${rows || `<div class="empty">기록이 없습니다.</div>`}</div>
    <p class="f-note">전체 ${logs.length}건 중 ${Math.min(filtered.length,400)}건 표시.
      로그인·예약 등록·상태 변경·좌석 배정·설정 변경이 IP와 함께 쌓입니다.</p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;""",
"""  const tab = view.logTab || "use";
  const setlog = (store().settings._setlog || []).slice().reverse();
  const setRows = setlog.length ? setlog.map(e=>{ const d = new Date(e.at); const t = isNaN(d) ? e.at : `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
    return `<div class="logrow"><span class="lg-t">${esc(t)}</span><span class="lg-ip">${esc(e.who||"")}</span><span class="lg-d">${e.items.map(esc).join("<br>")}</span></div>`; }).join("") : `<div class="empty">아직 없습니다. '적용하기' 를 누를 때부터 쌓입니다.</div>`;
  return `
    ${sheetHead("로그")}
    <div class="seg" style="margin-bottom:10px"><button class="${tab==="use"?'on':''}" onclick="view.logTab='use'; render()">이용 로그</button><button class="${tab==="set"?'on':''}" onclick="view.logTab='set'; render()">설정 로그</button></div>
    ${tab==="use" ? `
    <div class="row" style="margin-bottom:10px">
      <input id="log-q" value="${esc(q)}" placeholder="검색 (동작·계정·날짜)" oninput="setLogQuery(this.value)" style="flex:1">
      <button class="btn" onclick="copyLogs()">전체 복사</button>
    </div>
    <div class="logbox">${rows || `<div class="empty">기록이 없습니다.</div>`}</div>
    <p class="f-note">전체 ${logs.length}건 중 ${Math.min(filtered.length,400)}건 표시. 로그인·예약 등록·상태 변경·좌석 배정·노쇼·설정 적용이 계정과 함께 쌓입니다.</p>` : `
    <div class="logbox">${setRows}</div>
    <p class="f-note">'적용하기' 마다 무엇이 어떻게 바뀌었는지. 최근 60번까지.</p>`}
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;""")
L.js_check(s)
L.save(s)
print("p9_s ok")
