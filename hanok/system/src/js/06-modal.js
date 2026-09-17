/* ============================================================
   공통 팝업 — 브라우저 기본 alert/confirm 대신 같은 테마로
   uiAlert / uiConfirm 은 Promise 를 돌려주므로 await 로 씁니다.
   ============================================================ */
let MODAL = null;
/* 알림이 떠 있는데 새 알림이 오면 이전 것은 '취소' 로 닫습니다 — 안 그러면 이전 Promise 가 영원히 대기해
   그것을 기다리던 저장·단계 이동이 조용히 멈추고, 확인을 눌러도 다음 알림이 계속 뜹니다(7차 점검 U2) */
function modalReplace(next){
  var prev = MODAL; MODAL = next; render();
  if(prev && prev.res) prev.res(false);
}
function uiAlert(title, msg, tone){
  return new Promise(res => { modalReplace({mode:"alert", title, msg, tone:tone||"warn", res}); });
}
function uiConfirm(title, msg, opt){
  opt = opt || {};
  return new Promise(res => {
    modalReplace({mode:"confirm", title, msg, tone:opt.tone||"warn",
                  ok:opt.ok||"계속", cancel:opt.cancel||"취소", res});
  });
}
function modalAnswer(v){
  const m = MODAL; MODAL = null; render();
  if(m) m.res(v);
}
/* 선택지 팝업 — [[라벨, 값], …]. 취소면 null */
function uiChoice(title, msg, choices){
  return new Promise(res => { modalReplace({mode:"choice", title, msg, tone:"warn", choices, cancel:"그만두기", res}); });
}
/* 한 줄 입력 팝업 — 관리자 비밀번호 등. 취소면 null */
function uiPrompt(title, msg, opt){
  opt = opt || {};
  return new Promise(res => { modalReplace({mode:"prompt", title, msg, tone:"ok", ok:opt.ok||"확인", cancel:"취소", password:!!opt.password, value:opt.value||"", res}); });
}
/* 여러 개 중 하나 고르기 — 고른 번호(0부터), 취소면 null */
function uiChoose(title, options, msg){
  return new Promise(res => { modalReplace({mode:"choice", title, msg:msg||"", tone:"ok", choices:options.map((o,i)=>[o,i]), cancel:"취소", res}); });
}
function modalPromptAnswer(){ const el = document.getElementById("md-input"); const m = MODAL; MODAL = null; render(); if(m) m.res(el ? el.value : ""); }
function renderModal(){
  if(!MODAL) return "";
  const m = MODAL;
  /* '---' 만 있는 줄은 가로선으로 그립니다.
     문자 미리보기에서 '어디부터 어디까지가 문자인지' 눈으로 끊어 주려고 만들었습니다.
     선은 화면에만 그려지고 실제 문자 내용에는 들어가지 않습니다. */
  const lines = m.html ? `<div class="md-l md-html">${m.html}</div>` : String(m.msg||"").split("\n").map(l=>
    l.trim()==="---" ? `<div class="md-rule"></div>`
    : l.trim()==="" ? `<div class="md-gap"></div>`
    : `<div class="md-l">${esc(l)}</div>`).join("");
  return `
    <div class="overlay modal-ov" onclick="modalAnswer(false)">
      <div class="modal ${m.tone}" onclick="event.stopPropagation()">
        <div class="md-h">${esc(m.title)}</div>
        <div class="md-b">${lines}${m.mode==="prompt"?`<input id="md-input" type="${m.password?"password":"text"}" value="${esc(m.value||"")}" autofocus style="margin-top:8px; width:100%" onkeydown="if(event.key==='Enter') modalPromptAnswer()">`:""}</div>
        <div class="md-f">
          ${m.mode==="confirm"||m.mode==="prompt"||m.mode==="choice"?`<button class="btn" onclick="modalAnswer(${m.mode==="confirm"?"false":"null"})">${esc(m.cancel)}</button>`:""}
          ${m.mode==="choice" ? (m.choices||[]).map(([lb,v],i)=>`<button class="btn ${m.tone==="warn"&&i===0?"danger-fill":"primary"}" onclick="modalAnswer(${JSON.stringify(v)})">${esc(lb)}</button>`).join("") :
          `<button class="btn ${m.tone==="warn"?"danger-fill":"primary"}" onclick="${m.mode==="prompt"?"modalPromptAnswer()":"modalAnswer(true)"}">
            ${m.mode==="confirm"||m.mode==="prompt"?esc(m.ok):"확인"}</button>`}
        </div>
      </div>
    </div>`;
}

/* ---------- 매장 선택 ---------- */
function renderSelect(){
  const order = ["anjip","hanok"];   // 왼쪽 안집, 오른쪽 한옥반점
  const panels = order.map(key => {
    const s = DATA[key];
    const cnt = s.reservations.filter(r => r.date===todayStr() && r.status==="확정").length;
    const locked = !s.enabled;
    return `
      <button class="panel ${locked?'soon':''}" data-store="${key}"
        ${locked?'aria-disabled="true"':''} onclick="${locked?"":`goStore('${key}')`}">
        <span class="bg"></span><span class="veil"></span>
        <span class="label">
          <span class="name">${esc(s.name)}</span>
          <span class="rule"></span>
          ${locked ? `<span class="badge">준비 중</span>`
                   : `<span class="meta">오늘 예약 ${cnt}건</span>`}
        </span>
      </button>`;
  }).join("");
  return `<div class="split">${panels}</div>`;
}
function goStore(key){
  view.storeKey=key; view.tab="dash"; view.date=todayStr(); view.calMonth=monthStr();
  if(AUTHED) logEvent("매장 진입", key);
  render();
}
/* 상단바 더보기(⋮) 열고 닫기. 바깥(투명 막)을 누르면 닫힙니다 */
function toggleMore(){ view.moreOpen = !view.moreOpen; render(); }
function closeMore(){ if(view.moreOpen){ view.moreOpen = false; render(); } }
/* 매장 이름 누르기 = 매장 선택으로 (로그아웃. PIN 이라 부담이 적습니다) */
async function setTab(t){
  /* 다른 기기가 설정을 바꿨는데 이 기기에 옛 임시본이 남아 있으면 '저장 안 한 변경' 으로 오탐하고, 적용하면 되돌립니다(점검 C3).
     고친 것이 없으면 들어올 때마다 새로 뜹니다 */
  if(t === "settings" && view.draft && !settingsDirty()) view.draft = null;
  /* 설정에서 나갈 때 저장 안 한 변경이 있으면 물어봅니다 */
  if(view.tab==="settings" && t!=="settings" && settingsDirty()){
    const ok = await uiConfirm("저장하지 않은 변경이 있습니다",
      "변경 내용을 버리고 나갈까요?", {ok:"버리고 나가기", cancel:"계속 편집"});
    if(!ok) return;
    view.draft = null;
  }
  /* 설정은 관리자 비밀번호로만 들어갑니다(재아). 한 번 통과하면 잠글 때까지 다시 묻지 않고,
     PIN 변경·관리자 비밀번호 변경·접속 기록·PIN 관리·초기화·기록 복사는 그 안에서 한 번 더 묻습니다 */
  if(t==="settings" && !view.adminOk){ if(!await adminGate("설정 열기")) return; view.adminOk = true; }
  /* 설정에서 나가면 관리자 확인도 풀립니다 — 다시 들어올 때 비밀번호를 또 묻게(재아). 홈페이지 관리도 설정 안에 있으니 같이 */
  if(view.tab==="settings" && t!=="settings") view.adminOk = false;
  if(t==="settings" && !view.draft) view.draft = deepClone(store().settings);
  Object.keys(view.open).forEach(function(x){ view.open[x] = false; });   /* 어디든 갔다 오면 폴드는 접힌 상태로(재아) — 설정·대시보드 모두 */
  view.tab=t; render(); window.scrollTo(0,0);
}
/* 설정 화면에서는 임시본을 씁니다 — '적용하기'를 눌러야 반영됩니다 */
function draft(){
  if(!view.draft) view.draft = deepClone(store().settings);
  return view.draft;
}
function settingsDirty(){
  return !!view.draft && JSON.stringify(view.draft) !== JSON.stringify(store().settings);
}
/* 시트(운영시간·임시일정·노쇼 제외)는 '적용하기' 없이 바로 저장합니다. 그 값을 임시본에도 같이 써 둬야
   나중에 '적용하기' 를 눌렀을 때 옛 임시본이 방금 저장한 것을 되돌리지 않습니다(점검 D1) */
function mirrorDraft(key){ if(view.draft) view.draft[key] = deepClone(store().settings[key]); }
/* 설정 두 개의 차이를 '키: 이전 → 이후' 로 — 관리자 → 설정 변경 내역 */
function settingsDiff(a, b){
  const out = [], keys = {}; Object.keys(a||{}).concat(Object.keys(b||{})).forEach(k=>{ keys[k]=1; });
  const NAME = {scheduled:null, rooms:"좌석", joins:"룸 합침", schedules:"운영시간", overrides:"임시 일정", holidays:"공휴일 추가", holidaysOff:"공휴일 제외", courseGroups:"코스 구성", sources:"예약경로", sms:"문자 안내", displayRows:"디스플레이 배치", tvType:"디스플레이 형식", groupSize:"단체 기준", noshowExcluded:"노쇼 경고 제외", uiZoom:"화면 크기", closeGapMin:"겹침 경고", noshowWarnCount:"노쇼 경고 기준", noshowCancelRule:"취소→노쇼 기준", tvAd:"광고 영상", holidayAsWeekend:"공휴일=주말", minCountAdultsOnly:"정원 기준", chairDefault:"유아의자 기본", loSoon:"임박 기준", breakMode:"브레이크 방식", _setlog:null};
  Object.keys(keys).forEach(k=>{
    if(NAME[k] === null) return;
    const x = JSON.stringify(a ? a[k] : undefined), y = JSON.stringify(b ? b[k] : undefined);
    if(x === y) return;
    const short = v => { if(v === undefined) return "없음"; const t = typeof v === "string" ? v : JSON.stringify(v); return t.length > 60 ? t.slice(0,57) + "…" : t; };
    const av = a ? a[k] : undefined, bv = b ? b[k] : undefined;
    /* 배열(좌석·경로·합침·코스 구성·임시 일정)은 JSON 을 그대로 적으면 못 읽습니다(검토 2026-09-17) — 개수와 늘고 준 이름만 */
    if(Array.isArray(av) || Array.isArray(bv)){
      const nm = x => x == null ? "" : (typeof x === "string" ? x : (x.name || x.title || x.date || x.id || ""));
      const A = (av || []).map(nm), B = (bv || []).map(nm);
      const added = B.filter(n => n && A.indexOf(n) < 0), removed = A.filter(n => n && B.indexOf(n) < 0);
      let s = `${A.length}개 → ${B.length}개`;
      if(added.length) s += ` · 추가 ${added.slice(0,4).join(", ")}${added.length > 4 ? " 외" : ""}`;
      if(removed.length) s += ` · 삭제 ${removed.slice(0,4).join(", ")}${removed.length > 4 ? " 외" : ""}`;
      if(!added.length && !removed.length) s += " · 내용 수정";
      out.push(`${NAME[k] || k}: ${s}`);
      return;
    }
    out.push(`${NAME[k] || k}: ${short(av)} → ${short(bv)}`);
  });
  return out;
}
async function applySettings(){
  if(!view.draft) return;
  if(readonlyBlock()) return;
  const before = store().settings, after = deepClone(view.draft);
  /* 좌석·규칙·코스가 바뀌었으면 "지금 바로 / 날짜부터" — 날짜면 예정으로 들어가고 그 묶음은 되돌아옵니다(03b) */
  if(!await askScheduleOnApply(before, after)) return;
  after.scheduled = before.scheduled;   /* 예정 목록은 임시본이 아니라 설정에서 직접 관리 */
  const diff = settingsDiff(before, after);
  after._setlog = (before._setlog || []).concat(diff.length ? [{at:new Date().toISOString(), who:SESSION ? SESSION.who : "-", items:diff}] : []).slice(-60);
  store().settings = after;
  view.draft = deepClone(after);   /* _setlog 가 붙어 임시본과 달라지지 않게 */
  logEvent("설정 변경", diff.length ? diff.join(" / ").slice(0, 300) : "적용(변경 없음)");
  absorbScheduled();
  takeSnapshot();   /* 룸·테이블 수가 바뀌었을 수 있으니 오늘 스냅샷을 새로 (내일부터 오늘을 이 수로 계산) */
  saveData(); render();
}
async function revertSettings(){
  if(!await uiConfirm("변경을 되돌릴까요?", "마지막으로 적용한 상태로 돌아갑니다.", {ok:"되돌리기"})) return;
  view.draft = deepClone(store().settings);
  render();
}

/* ---------- 매장 화면 껍데기 ---------- */
/* ---------- 새로고침 · 갱신 시각 · 자동 갱신 ----------
   지금은 저장소가 없어 '새로고침'이 화면을 다시 그리는 것뿐입니다.
   Supabase 가 붙으면 여기서 loadData() 를 다시 불러 서버 값을 가져옵니다.
   갱신 시각은 "N분 전" 으로 보여 줍니다 — 시각보다 '얼마나 오래됐나' 가 판단에 쓸모 있습니다. */
var LAST_REFRESH = Date.now();
async function refreshData(){
  try{
    var changed = await reloadFromStore();
    LAST_REFRESH = Date.now();
    /* 홈페이지 연동(11c): 새 접수 끌어오기 → 팝업, 남은 자리 올리기(45초 간격) */
    try{ if(SESSION && !view.display){ var fresh = await pullRequests(); if(fresh) changed = true; publishAvail(); } }catch(e){}
    return changed !== false;   /* 서버 모드는 바뀐 것이 있는지 돌려줍니다. 그 밖(undefined)은 '모름' = 다시 그림 */
  }catch(e){
    console.error("갱신 실패", e.message);
    if(view.display) throw e;                                  /* TV 는 3번 연속 실패를 세어 '연결 확인 중' 을 띄웁니다 */
    if(e.network && !OFFLINE && SESSION){ enterOffline(); render(); }   /* 보던 중 연결이 끊김 → 캐시 읽기 전용으로 */
  }
}
async function manualRefresh(){
  var b = document.querySelector(".b-refresh");
  if(b) b.classList.add("spin");
  await refreshData();
  render();
}
/* 대시보드는 10초마다 스스로 갱신합니다(재아 2026-09-17, 전에는 1분) — 서버에서 바뀐 행만 받아 오고, 실제로 바뀐 것이 있을 때만 다시 그립니다.
   마법사·시트·확인창이 떠 있으면 건너뜁니다(입력 중에 화면이 바뀌면 안 되니까). 탭이 뒤로 가 있으면(document.hidden) 쉽니다 — 폰 배터리.
   '새로고침' 버튼은 즉시 + 무조건 다시 그림. 자정 처리·토큰 갱신 같은 살림은 1분에 한 번만 */
var TICK_N = 0;
setInterval(function(){
  TICK_N++;
  if(TICK_N % 6 === 0){
  /* 자정을 넘겼으면 새 날짜의 좌석 수를 남깁니다 (밤새 켜 둔 태블릿·TV). 6차 전에는 자정 처리가 따로 없었습니다 */
  if(SNAP_DAY && todayStr() !== SNAP_DAY){ if(AUTHED) absorbScheduled(); takeSnapshot(); if(AUTHED && autoCloseDays()) saveData(); }   /* 어제 '확정' → '방문' 도 함께(점검 R7) */
  sessionTick();   /* 토큰 만료 5분 전 갱신 */
  if(SAVE_FAIL && !OFFLINE) flush();   /* 저장 못 한 것이 있으면 다시 */
  if(AUTHED && !view.display && typeof publishAvail === "function" && AVAIL_DIRTY) publishAvail();   /* 미뤄 둔 남은 자리 올리기 */
  }
  if(!AUTHED || view.display || WZ || view.form || MODAL || document.hidden || REFRESH_BUSY) return;
  REFRESH_BUSY = true;
  refreshData().then(function(changed){ REFRESH_BUSY = false; if(changed) render(); }, function(){ REFRESH_BUSY = false; });   /* 느린 회선에서 앞 갱신이 안 끝났으면 겹치지 않게(finally 는 구형 TV 에 없을 수 있어 then 둘로) */
}, 10000);
var REFRESH_BUSY = false;

/* 폰 여부 — CSS 의 @media (max-width:640px) 와 같은 기준. 폰에서는 상단바·대시보드를 다른 구성으로 그립니다(PC 는 그대로) */
function isMobile(){ return window.innerWidth <= 640; }
var MOBILE_WAS = null;
window.addEventListener("resize", function(){
  var m = isMobile();
  if(MOBILE_WAS !== null && m !== MOBILE_WAS && DATA) render();   /* 폰↔PC 경계를 넘을 때만 다시 그림 */
  MOBILE_WAS = m;
});
function renderStore(){
  const s = store();
  MOBILE_WAS = isMobile();
  const stt = shopState(s.settings);
  /* 8차-O(재아): 네이버 가져오기·빠른 입력은 팝업 시트가 아니라 화면 전체로 (view.form.page) */
  const pageForm = !!(view.form && view.form.page);
  const pageTitle = pageForm ? (view.form.type === "naver" ? "네이버 예약 가져오기" : view.form.type === "site" ? "홈페이지 관리" : "빠른 입력") : "";
  const body = pageForm ? `<div class="page-wrap">${renderSheet()}</div>` : (view.tab==="settings" ? renderSettings : renderDash)();

  return `
    <div class="shell">
      ${pageForm ? `<header class="topbar page ${notodayView()?'notoday':''}"><div class="topbar-in">
        <button class="storename" onclick="goHomeScreen()" title="홈으로"><span class="sn-brand">HANOK</span></button>
        <div class="bar-mid"><span class="bdate static">${pageTitle}</span></div>
        <div class="bar-right"><button class="tvbtn icon b-exit" onclick="closeSheet()" title="닫기" aria-label="닫기">✕</button></div>
      </div></header>` : `<header class="topbar ${notodayView()?'notoday':''} ${isMobile()?'mobile':''} ${view.tab==="settings"?'settings':''}"><div class="topbar-in">
        <!-- 매장 이름 = 예전 맨 왼쪽 버튼의 역할. 대시보드에서는 매장 선택으로, 설정에서는 대시보드로. 아이콘·화살표 없이 글자만(6차-K) -->
        <!-- 8차-P(재아): HANOK 은 홈(대시보드·오늘)으로, 이미 홈이면 새로고침. 매장 나가기·로그아웃은 더보기 -->
        <button class="storename" onclick="${view.tab==="settings" || view.form || WZ ? "goHomeScreen()" : (view.date===todayStr() ? "manualRefresh()" : "goToday()")}"
          title="${view.tab==="settings" ? "대시보드로" : (view.date===todayStr() ? "새로고침" : "오늘로")}"><span class="sn-brand">HANOK</span></button>
        ${isMobile() && view.tab!=="settings" ? `
        <!-- 폰: 리스트|그래프 스위치 — 본문에 두면 자리를 크게 먹어 로고 옆으로 (7차-M) -->
        <button class="mswitch" onclick="view.mView = view.mView==='graph' ? 'list' : 'graph'; render()" aria-label="목록/타임라인 전환">
          <span class="${view.mView==='graph'?'':'on'}">목록</span><span class="${view.mView==='graph'?'on':''}">타임라인</span>
        </button>` : ``}

        ${view.tab==="settings" || isMobile() ? `` : `
        <div class="bar-mid">
          <button class="bnav mo" onclick="moveMonthDate(-1)" title="이전 달">&laquo;</button>
          <button class="bnav" onclick="moveDate(-1)" title="어제">&lsaquo;</button>
          <button class="bdate" onclick="openCal()" title="달력 열기">${dateLabel(view.date)}</button>
          <button class="bnav" onclick="moveDate(1)" title="내일">&rsaquo;</button>
          <button class="bnav mo" onclick="moveMonthDate(1)" title="다음 달">&raquo;</button>
        </div>`}

        <div class="bar-right">
          ${view.tab==="settings" ? `
          <!-- 설정: 되돌리기·적용하기를 여기(나가기 왼쪽)에 (재아). 아래 안내 띠는 없앴습니다 -->
          <button class="tvbtn b-sched ${schedList().length?'has':''}" onclick="openScheduled()" title="예정된 설정">예정<i class="cnt">${schedList().length}</i></button>
          <button class="tvbtn b-revert" onclick="revertSettings()" ${settingsDirty()?"":"disabled"}>되돌리기</button>
          <button class="tvbtn amber b-apply" onclick="applySettings()" ${settingsDirty()?"":"disabled"}>적용하기</button>
          <button class="tvbtn icon b-exit" onclick="setTab('dash')" title="설정 나가기" aria-label="설정 나가기">${ICON.exit}</button>` : isMobile() ? `
          <!-- 폰: 아이콘만 한 줄. 날짜는 달력 아이콘으로(오늘이 아니면 상단바가 검정이라 티가 납니다), 등록은 오른쪽 아래 둥근 ＋ (7차-M)
               '오늘' 은 375px 에 안 들어가 더보기로 — 달력 아이콘의 점이 '오늘이 아님' 표시 -->
          <button class="tvbtn icon b-cal ${view.date===todayStr()?'':'dot'}" onclick="openCal()" title="날짜" aria-label="날짜 선택">${ICON.cal}</button>
          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}</button>
          <button class="tvbtn icon b-search" onclick="openSearch()" title="예약 검색" aria-label="예약 검색">${ICON.search}</button>
          <button class="tvbtn icon b-reqs ${reqPending().length?'has':''}" onclick="openRequests()" title="홈페이지 예약" aria-label="홈페이지 예약">${ICON.inbox}<i class="cnt">${reqPending().length}</i></button>` : `
          ${view.date===todayStr() ? "" : `<button class="tvbtn b-today" onclick="goToday()">오늘</button>`}
          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}</button>
          <button class="tvbtn b-search" onclick="openSearch()">예약 검색</button>
          <button class="tvbtn b-reqs ${reqPending().length?'has':''}" onclick="openRequests()">홈페이지 예약<i class="cnt">${reqPending().length}</i></button>
          <button class="tvbtn accent b-add" onclick="openWizard()">＋ 예약 등록</button>`}
          ${view.tab==="settings" ? "" : `
          <!-- 더보기(⋮): 자주 안 쓰는 것들을 여기로 모았습니다 — 예약률 추이 · 영업시간 · 설정 · 디스플레이 모드 -->
          <div class="more-wrap">
            <button class="tvbtn icon b-more ${view.moreOpen?'on':''}" onclick="toggleMore()" title="더보기" aria-label="더보기">${ICON.more}</button>
            ${view.moreOpen ? `
            <div class="more-menu">
              ${isMobile() && view.date!==todayStr() ? `<button onclick="closeMore(); goToday()">${ICON.cal}<span>오늘로</span></button>` : ``}
              <button onclick="closeMore(); openHours()">${ICON.clock}<span>영업시간</span></button>
              ${isMobile() ? `` : `<button onclick="closeMore(); openDisplay()">${ICON.tv}<span>디스플레이 모드</span></button>`}
              ${document.fullscreenEnabled ? `<button onclick="closeMore(); toggleFullscreen()">${document.fullscreenElement?ICON.shrink:ICON.expand}<span>${document.fullscreenElement?"전체화면 해제":"전체화면"}</span></button>` : ""}
              <button onclick="closeMore(); openZoomAdj()">${ICON.search}<span>화면 보정</span></button>
              <button onclick="closeMore(); openSlip()">${ICON.print}<span>비상 예약지</span></button>
              <button onclick="closeMore(); setTab('settings')">${ICON.set}<span>설정</span></button>
              <button onclick="closeMore(); lockNow()">${ICON.exit}<span>로그아웃</span></button>
              <button onclick="closeMore(); exitApp()">${ICON.shrink}<span>종료하기</span></button>
            </div>` : ""}
          </div>`}
        </div>
        ${view.moreOpen ? `<div class="more-veil" onclick="closeMore()"></div>` : ""}
      </div></header>`}
      <div class="layout">
        <main class="content">${body}</main>
      </div>
      ${view.form && !pageForm ? renderSheet() : ""}
      ${(!WZ && view.form && view.form.type==="res" && tmpRes && tmpRes.courseOpen) ? renderCourse() : ""}
      ${WZ ? renderWizard() : ""}
    </div>`;
}
