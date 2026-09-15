# -*- coding: utf-8 -*-
"""8차-P — 재아 목록 1차: 전체화면 스크롤(zoom×100vh), 애니메이션 전부 끄기, 상단바(HANOK=홈/새로고침, 나가기·로그아웃은 더보기),
   설정 상단바에 되돌리기/적용하기, 안내 문구 삭제, 화면 크기 기본 100% + 매장 공유, 타임라인 '예약률' 글자 삭제·22 잘림,
   예약 목록 지난/방문/취소 구분, 로그 한국 시각·전체 복사 관리자 비번, 경로 기본 셋 삭제 불가, 설정 줄 배치(제목 왼쪽·조작 오른쪽),
   마법사/화면형 상단바 높이 통일 + 화면형은 X 만"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 전체화면에서 스크롤: zoom 이 100vh 도 1.1배 해서 화면보다 커졌습니다 ----------
s = R(s, """.shell{min-height:100vh; zoom:var(--ui-zoom, 1.1)}""", """.shell{min-height:calc(100vh / var(--ui-zoom, 1)); zoom:var(--ui-zoom, 1)}   /* zoom 이 min-height 도 곱하므로 나눠 둡니다 — 안 그러면 내용이 짧아도 스크롤이 생깁니다(전체화면에서 티남) */""")
s = R(s, """  return ZOOM_STEPS.indexOf(z) >= 0 ? z : 110;
}""", """  return ZOOM_STEPS.indexOf(z) >= 0 ? z : 100;   /* 기본 100%(재아) */
}""")
# 화면 크기: 매장 설정(공유) 우선, 없으면 기기값
s = R(s, """function uiZoom(){
  const z = DATA && DATA._ui ? DATA._ui.zoom : null;""", """function uiZoom(){
  const shared = view.storeKey && DATA && DATA[view.storeKey] && DATA[view.storeKey].settings ? DATA[view.storeKey].settings.uiZoom : null;   /* 매장 설정에 공유(재아) */
  const z = shared != null ? shared : (DATA && DATA._ui ? DATA._ui.zoom : null);""")
s = R(s, """function setZoom(z){
  DATA._ui = DATA._ui || {};
  DATA._ui.zoom = z;""", """function setZoom(z){
  DATA._ui = DATA._ui || {};
  DATA._ui.zoom = z;
  if(view.storeKey && store()){ store().settings.uiZoom = z; mirrorDraft("uiZoom"); }   /* 모든 기기에 같이 */""")

# ---------- 애니메이션 전부 끄기 ----------
s = R(s, """.sheet, .calbox{animation:sheet-in .2s ease-out}
.modal{animation:modal-in .15s ease-out}
.overlay{animation:fade-in .15s ease-out}""", """/* 8차-P(재아): 등장 애니메이션은 전부 끕니다 — 매일 쓰는 도구는 '짠' 하고 뜨는 게 낫습니다 */
.sheet, .calbox, .modal, .overlay{animation:none}""")
s = R(s, """.fold-b.just{animation:fade-in .15s ease-out}   /* 방금 연 폴드만 — 매 render 마다 재생되면 '새로고침' 느낌이 납니다(8차-K) */""", """.fold-b.just{animation:none}""")

# ---------- 상단바: HANOK = 홈/새로고침, 나가기·로그아웃은 더보기 ----------
s = R(s, """        <button class="storename" onclick="${view.tab==="settings"?"setTab('dash')":"goHome()"}"
          title="${view.tab==="settings"?"대시보드로":"매장 선택"}"><span class="sn-brand">HANOK</span></button>""",
"""        <!-- 8차-P(재아): HANOK 은 홈(대시보드·오늘)으로, 이미 홈이면 새로고침. 매장 나가기·로그아웃은 더보기 -->
        <button class="storename" onclick="${view.tab==="settings" || view.form || WZ ? "goHomeScreen()" : (view.date===todayStr() ? "manualRefresh()" : "goToday()")}"
          title="${view.tab==="settings" ? "대시보드로" : (view.date===todayStr() ? "새로고침" : "오늘로")}"><span class="sn-brand">HANOK</span></button>""")
s = R(s, """          <!-- 설정에서는 점 3개 대신 나가기 하나 (좌측 HANOK 과 같은 역할). 디스플레이 모드는 대시보드 메뉴에 있습니다 (6차-K) -->
          <button class="tvbtn icon b-exit" onclick="setTab('dash')" title="설정 나가기" aria-label="설정 나가기">${ICON.exit}</button>` : isMobile() ? `""",
"""          <!-- 설정: 되돌리기·적용하기를 여기(나가기 왼쪽)에 (재아). 아래 안내 띠는 없앴습니다 -->
          <button class="tvbtn b-revert" onclick="revertSettings()" ${settingsDirty()?"":"disabled"}>되돌리기</button>
          <button class="tvbtn accent b-apply" onclick="applySettings()" ${settingsDirty()?"":"disabled"}>적용하기</button>
          <button class="tvbtn icon b-exit" onclick="setTab('dash')" title="설정 나가기" aria-label="설정 나가기">${ICON.exit}</button>` : isMobile() ? `""")
s = R(s, """              <button onclick="closeMore(); openDisplay()">${ICON.tv}<span>디스플레이 모드</span></button>
            </div>` : ""}""", """              <button onclick="closeMore(); openDisplay()">${ICON.tv}<span>디스플레이 모드</span></button>
              <button onclick="closeMore(); goHome()">${ICON.exit}<span>매장 나가기</span></button>
              <button onclick="closeMore(); lockNow()">${ICON.exit}<span>로그아웃 (잠금)</span></button>
            </div>` : ""}""")
s = R(s, """    <div class="applybar ${dirty?'on':''}">
      <span class="ab-t">${dirty?"저장하지 않은 변경이 있습니다":"모든 변경이 적용되었습니다"}</span>
      <button class="btn" onclick="revertSettings()" ${dirty?"":"disabled"}>되돌리기</button>
      <button class="btn primary" onclick="applySettings()" ${dirty?"":"disabled"}>적용하기</button>
    </div>`;""", """    ${dirty ? `<div class="applybar on"><span class="ab-t">저장하지 않은 변경이 있습니다 — 위 '적용하기'</span></div>` : ""}`;""")
s = R(s, """      <button class="btn danger" onclick="lockNow()">로그아웃</button>""", """""")
# 홈 화면으로(마법사·시트·설정 닫고 대시보드)
s = R(s, """function goToday(){""", """function goHomeScreen(){ WZ = null; tmpRes = null; view.form = null; view.calOpen = false; if(view.tab === "settings") return setTab("dash"); render(); }
function goToday(){""")

# ---------- 타임라인: '예약률' 글자 삭제, 22 잘림 ----------
s = R(s, """        <span class="tl-kpi">예약률 <b>${st2.rate}%</b></span>""", """        <span class="tl-kpi"><b>${st2.rate}%</b></span>""")
s = R(s, """          <div class="tl-rate"><span class="rt">예약률</span></div>""", """          <div class="tl-rate"></div>""")
s = R(s, """    ticks.push(`<span class="tk" style="left:${pos(m)}%"><i></i><b>${Math.floor(m/60)}</b></span>`);""",
         """    ticks.push(`<span class="tk ${m>=c?'end':''}" style="left:${pos(m)}%"><i></i><b>${Math.floor(m/60)}</b></span>`);   /* 맨 끝 눈금은 글자를 왼쪽으로 붙여 잘리지 않게 */""")
s = R(s, """.offline-card{padding:var(--s24); text-align:center}""", """.tk.end b{transform:translateX(-100%); margin-left:-2px}
.offline-card{padding:var(--s24); text-align:center}""")

# ---------- 로그: 한국 시각 표기, 전체 복사는 관리자 비밀번호 ----------
s = R(s, """    const t = l.ts.replace("T"," ").slice(0,19);""", """    const dd = new Date(l.ts), t = isNaN(dd) ? String(l.ts).slice(0,19) : `${dd.getFullYear()}-${pad(dd.getMonth()+1)}-${pad(dd.getDate())} ${pad(dd.getHours())}:${pad(dd.getMinutes())}:${pad(dd.getSeconds())}`;   /* 저장은 UTC, 표시는 이 기기(한국) 시각 */""")
s = R(s, """async function copyLogs(){
  const txt = (DATA._logs||[]).map(l=>`${l.ts}\\t${l.ip}\\t${l.store}\\t${l.action}\\t${l.detail}\\t${l.ua}`).join("\\n");""",
"""async function copyLogs(){
  if(!await adminGate("접속 기록 전체 복사")) return;   /* 전화번호·이름이 들어 있어 관리자 비밀번호(재아) */
  const txt = (DATA._logs||[]).map(l=>{ const d = new Date(l.ts); const t = isNaN(d) ? l.ts : `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`; return `${t}\\t${l.ip}\\t${l.store}\\t${l.action}\\t${l.detail}\\t${l.ua}`; }).join("\\n");""")
# 관리자 비밀번호 확인 공통창 (+ 입력 팝업 uiPrompt)
s = R(s, """function renderModal(){
  if(!MODAL) return "";""", """/* 한 줄 입력 팝업 — 관리자 비밀번호 등. 취소면 null */
function uiPrompt(title, msg, opt){
  opt = opt || {};
  return new Promise(res => { modalReplace({mode:"prompt", title, msg, tone:"ok", ok:opt.ok||"확인", cancel:"취소", password:!!opt.password, res}); });
}
function modalPromptAnswer(){ const el = document.getElementById("md-input"); const m = MODAL; MODAL = null; render(); if(m) m.res(el ? el.value : ""); }
function renderModal(){
  if(!MODAL) return "";""")
s = R(s, """        <div class="md-b">${lines}</div>
        <div class="md-f">
          ${m.mode==="confirm"?`<button class="btn" onclick="modalAnswer(false)">${esc(m.cancel)}</button>`:""}
          <button class="btn ${m.tone==="warn"?"danger-fill":"primary"}" onclick="modalAnswer(true)">
            ${m.mode==="confirm"?esc(m.ok):"확인"}</button>
        </div>""", """        <div class="md-b">${lines}${m.mode==="prompt"?`<input id="md-input" type="${m.password?"password":"text"}" autofocus style="margin-top:8px; width:100%" onkeydown="if(event.key==='Enter') modalPromptAnswer()">`:""}</div>
        <div class="md-f">
          ${m.mode==="confirm"||m.mode==="prompt"?`<button class="btn" onclick="modalAnswer(${m.mode==="prompt"?"null":"false"})">${esc(m.cancel)}</button>`:""}
          <button class="btn ${m.tone==="warn"?"danger-fill":"primary"}" onclick="${m.mode==="prompt"?"modalPromptAnswer()":"modalAnswer(true)"}">
            ${m.mode==="confirm"||m.mode==="prompt"?esc(m.ok):"확인"}</button>
        </div>""")
s = R(s, """function sheetLogs(){""", """/* 관리자 비밀번호 한 번 묻기 — 서버가 없는 빌드는 그냥 통과 */
async function adminGate(what){
  if(!supaOn()) return true;
  const pw = await uiPrompt(what, "관리자 비밀번호를 입력하세요", {password:true, ok:"확인"});
  if(pw == null) return false;
  try{ await authToken(SUPA_CFG.adminEmail, pw); logEvent("관리자 확인", what); return true; }
  catch(e){ await uiAlert("관리자 비밀번호가 다릅니다", "", "warn"); return false; }
}
function sheetLogs(){""")

# ---------- 경로: 기본 셋(전화·네이버·방문)은 못 지움 ----------
s = R(s, """        ${x!=="기타"?`<button onclick="delSource('${jsq(x)}')" """, """        ${["전화 예약","네이버 예약","방문","기타"].indexOf(x)<0?`<button onclick="delSource('${jsq(x)}')" """)

# ---------- 마법사 상단바 높이 = 일반 상단바, 화면형은 X 만 ----------
s = R(s, """.wz-top{background:var(--surface); border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:var(--s12); padding:var(--s12) var(--s16); flex-wrap:wrap}""",
""".wz-top{background:var(--surface); border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:var(--s12); padding:var(--s8) var(--s24); min-height:64px; flex-wrap:wrap}   /* 일반 상단바와 같은 높이(재아) */""")
s = R(s, """  const pageForm = !!(view.form && view.form.page);""", """  const pageForm = !!(view.form && view.form.page);
  const pageTitle = pageForm ? (view.form.type === "naver" ? "네이버 예약 가져오기" : "빠른 입력") : "";""")
s = R(s, """      <header class="topbar ${notodayView()?'notoday':''} ${isMobile()?'mobile':''} ${view.tab==="settings"?'settings':''}"><div class="topbar-in">""",
"""      ${pageForm ? `<header class="topbar page ${notodayView()?'notoday':''}"><div class="topbar-in">
        <button class="storename" onclick="goHomeScreen()" title="홈으로"><span class="sn-brand">HANOK</span></button>
        <div class="bar-mid"><span class="bdate static">${pageTitle}</span></div>
        <div class="bar-right"><button class="tvbtn icon b-exit" onclick="closeSheet()" title="닫기" aria-label="닫기">✕</button></div>
      </div></header>` : `<header class="topbar ${notodayView()?'notoday':''} ${isMobile()?'mobile':''} ${view.tab==="settings"?'settings':''}"><div class="topbar-in">""")
s = R(s, """        ${view.moreOpen ? `<div class="more-veil" onclick="closeMore()"></div>` : ""}
      </div></header>""", """        ${view.moreOpen ? `<div class="more-veil" onclick="closeMore()"></div>` : ""}
      </div></header>`}""")
s = R(s, """.tk.end b{transform:translateX(-100%); margin-left:-2px}""", """.tk.end b{transform:translateX(-100%); margin-left:-2px}
.topbar.page .bdate.static{cursor:default; background:none; border:none}
.topbar-in{min-height:64px}
.tvbtn.b-revert:disabled, .tvbtn.b-apply:disabled{opacity:.4}""")

# ---------- 예약 목록: 지난 / 방문 / 취소 구분 ----------
s = R(s, """.rrow.s-취소{opacity:.4}
.rrow.s-방문{opacity:.4}
.rrow.s-노쇼{opacity:.55}""", """/* 8차-P(재아): 흐림만으로는 안 보여서 — 방문은 초록 체크 + 회색 바탕, 취소는 회색 + 가운데 줄, 노쇼는 벽돌색 표시 + 가운데 줄 */
.rrow.s-방문, .rrow.s-취소, .rrow.s-노쇼{background:var(--surface-2); color:var(--text-3)}
.rrow.s-방문 .rr-t:before{content:"✓ "; color:var(--pine); font-weight:700}
.rrow.s-방문 .rr-n{color:var(--text-2)}
.rrow.s-취소 .rr-n, .rrow.s-취소 .rr-t{text-decoration:line-through}
.rrow.s-노쇼 .rr-n{text-decoration:line-through} .rrow.s-노쇼 .rr-t{color:var(--rust)}
.mrow.s-방문, .mrow.s-취소, .mrow.s-노쇼{background:var(--surface-2); color:var(--text-3)}
.mrow.s-취소 .mr-n, .mrow.s-노쇼 .mr-n{text-decoration:line-through}""")

# ---------- 설정 줄 배치: 제목 왼쪽 · 조작 오른쪽, 안내는 아래 ----------
s = R(s, """.tk.end b{transform:translateX(-100%); margin-left:-2px}""", """.tk.end b{transform:translateX(-100%); margin-left:-2px}
/* 8차-P(재아): 설정 한 줄이 한 행을 다 먹지 않게 — 제목은 왼쪽, 버튼·토글은 오른쪽, 설명은 아래 한 줄 */
.fold-b label.f, .fold-b .f{display:grid; grid-template-columns:1fr auto; column-gap:var(--s16); align-items:center; margin-bottom:var(--s8)}
.fold-b .f > .lb{margin:0}
.fold-b .f > .f-note{grid-column:1 / -1; margin-top:2px}
.fold-b .f > .togglebtn, .fold-b .f > .numbtn{width:auto; min-width:0; justify-self:end}
.fold-b .f > input[type=time], .fold-b .f > input[type=text], .fold-b .f > input:not([type]){justify-self:end; width:auto; min-width:140px}
.fold-b .f > .seg{justify-self:end}
.fold-b .f.stack{display:block}   /* 세로로 둬야 하는 것(긴 입력)은 이 클래스 */
@media (max-width:640px){ .fold-b label.f, .fold-b .f{grid-template-columns:1fr} .fold-b .f > *{justify-self:start} }""")
L.js_check(s)
L.save(s)
print("p9_p ok")
