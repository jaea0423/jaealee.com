/* ============================================================
   렌더링
   ============================================================ */
function applyTheme(){
  const t = (DATA && DATA._ui && DATA._ui.theme) || "hanok";
  document.body.className = t==="hanok" ? "theme-hanok" : "";
  /* 화면 배율. 브라우저 확대와 같은 방식이라 레이아웃이 그대로 커집니다.
     transform:scale 은 자리를 그대로 차지해 화면이 잘리므로 쓰지 않습니다. */
  document.documentElement.style.setProperty("--ui-zoom", (uiZoom()/100));
}
/* 기본 110%. 100%는 태블릿·모니터 모두 조금 작고, 125%는 브라우저 확대와 겹치면 너무 커집니다.
   기기마다 다르므로 설정 → 화면 크기에서 바꿉니다. */
const ZOOM_STEPS = [90, 95, 100, 105, 110, 120, 135];
/* 화면 크기 = 매장 공유값(설정 → 적용하기) + 이 기기 보정(즉시). PC 는 110 이 맞고 아이패드는 100 이 맞는 식이라 보정을 둡니다 */
function uiZoom(){
  if(DATA && DATA._ui && typeof DATA._ui.zoom === "number" && typeof DATA._ui.zoomAdj !== "number"){ DATA._ui.zoomAdj = Math.max(-40, Math.min(40, DATA._ui.zoom - 100)); delete DATA._ui.zoom; uiSave(); }   /* 8차-T: 옛 기기값을 보정으로 */
  const shared = view.storeKey && DATA && DATA[view.storeKey] && DATA[view.storeKey].settings ? DATA[view.storeKey].settings.uiZoom : null;
  const base = ZOOM_STEPS.indexOf(shared) >= 0 ? shared : 100;
  const adj = DATA && DATA._ui && typeof DATA._ui.zoomAdj === "number" ? DATA._ui.zoomAdj : 0;
  return Math.max(70, Math.min(160, base + adj));
}
function setZoomAdj(d){ DATA._ui = DATA._ui || {}; DATA._ui.zoomAdj = Math.max(-40, Math.min(40, (DATA._ui.zoomAdj||0) + d)); uiSave(); applyTheme(); render(); }
function setPolicy(k,v){ const st=draft(); st[k]=v; render(); }
/* 문자 설정 — 다른 설정과 같이 '적용하기'를 눌러야 반영됩니다 */
function setSms(k, v){
  const st = draft();
  st.sms = { ...SMS_DEFAULT, ...(st.sms||{}) };
  st.sms[k] = v;
  /* 당일로 바꾸면 오전까지만 고를 수 있으므로, 오후에 맞춰져 있던 시각을 당깁니다 */
  if(k === "remindOffset"){
    const hs = remindHours(v);
    if(hs.indexOf(st.sms.remindHour) < 0) st.sms.remindHour = hs[hs.length-1];
  }
  /* 전화번호는 글자를 칠 때마다 화면을 새로 그리면 커서가 튑니다 */
  if(k === "storePhone") return;
  render();
}
function setZoom(z){ draft().uiZoom = z; render(); }   /* 매장 공유값 — '적용하기' 를 눌러야 반영(재아) */
/* 화면 그리기는 innerHTML 을 통째로 바꾸는 방식이라, 도중에 예외가 나면
   대입 자체가 일어나지 않아 화면이 직전 상태로 굳습니다.
   그러면 이후 모든 클릭이 같은 예외로 죽는데 사용자 눈에는
   "버튼을 눌러도 아무 일도 안 남" 으로만 보입니다.
   그래서 여기서 잡아 새로고침 안내를 띄웁니다. */
function render(){
  try{ renderApp(); }
  catch(e){ showCrash(e); }
}
function showCrash(e){
  try{
    console.error("화면 오류", e);
    var old = document.getElementById("crashbar");
    if(old) old.parentNode.removeChild(old);
    var d = document.createElement("div");
    d.id = "crashbar";
    d.className = "crashbar";
    d.innerHTML = '<b>화면을 그리는 중 문제가 생겼습니다.</b>' +
      '<span>방금 한 조작은 저장되지 않았을 수 있습니다.</span>' +
      '<button onclick="location.reload()">새로고침</button>' +
      '<i>' + esc(String(e && e.message ? e.message : e).slice(0,120)) + '</i>';
    document.body.appendChild(d);
  }catch(_){ /* 안내조차 실패하면 조용히 넘어갑니다 */ }
}
/* 화면을 다시 그리면 innerHTML 이 통째로 바뀌므로 스크롤 위치가 0으로 돌아갑니다.
   마법사에서 분 단위를 조절할 때마다 화면이 맨 위로 튀던 원인이 이것이었습니다.
   그리기 직전에 위치를 적어 두고 그린 뒤에 되돌려 놓습니다.
   ※ 단계를 옮길 때는 맨 위로 가야 하므로 wzGo() 가 그린 다음 0으로 덮어씁니다. */
var KEEP_SCROLL = [".wz-mid", ".sheet", ".calbox"];
var scrollMemo = null;
/* '같은 화면을 다시 그린 것'인지 판별하는 열쇠.
   다른 단계·다른 팝업으로 넘어갔다면 위치를 물려받으면 안 됩니다
   (새로 연 팝업이 엉뚱하게 중간부터 보이는 일을 막습니다). */
function viewKey(){
  return (WZ ? "wz" + WZ.step : "-") + "|" +
         (view.form ? view.form.type + (view.form.id || "") : "-") + "|" +
         (view.calOpen ? "cal" : "-") + "|" + view.tab;
}
function saveScroll(){
  scrollMemo = { key: viewKey(), pos: [] };
  for(var i=0;i<KEEP_SCROLL.length;i++){
    var el = document.querySelector(KEEP_SCROLL[i]);
    if(el && el.scrollTop > 0) scrollMemo.pos.push([KEEP_SCROLL[i], el.scrollTop]);
  }
}
function restoreScroll(){
  if(!scrollMemo) return;
  var memo = scrollMemo; scrollMemo = null;
  if(memo.key !== viewKey()) return;      /* 화면이 바뀌었으면 맨 위에서 시작 */
  for(var i=0;i<memo.pos.length;i++){
    var el = document.querySelector(memo.pos[i][0]);
    if(el) el.scrollTop = memo.pos[i][1];
  }
}
var lastPopKey = "";
/* 어떤 팝업이 떠 있는지 열쇠. 직전 그리기와 같으면 '같은 팝업을 고쳐 그린 것' 이므로 등장 움직임을 생략합니다 */
/* 시트 키와 확인창 키를 따로 봅니다 — 예전엔 하나로 묶어서, 시트 안에서 확인창이 떴다 닫히면 시트가 두 번 '두둥실' 했습니다(재아) */
function popKey(){
  const t = WZ ? WZ : tmpRes;
  return viewKey() + "|" + (t && t.courseOpen ? "course" : "-");
}
function modalKey(){ return MODAL ? "modal" : "-"; }
var lastModalKey = "";
function renderLoadError(){
  if(view.display) return "";
  if(OFFLINE && AUTHED){
    var d = OFFLINE.at ? new Date(OFFLINE.at) : null;          /* 캐시 시각은 UTC 문자열 — 한국 시각으로 */
    var at = d && !isNaN(d) ? pad(d.getHours()) + ":" + pad(d.getMinutes()) : "-";
    return `<div class="crashbar offline">
      <b>오프라인</b><span>마지막 갱신 ${esc(at || "-")} · 지금은 볼 수만 있습니다. 30초마다 다시 연결해 봅니다.</span>
      <button onclick="reconnect()">다시 연결</button></div>`;
  }
  if(AUTHED && clockBad()){
    return `<div class="crashbar offline"><b>이 기기의 시계가 틀립니다</b><span>서버와 ${Math.round(Math.abs(CLOCK_SKEW)/3600000)}시간 이상 차이 — 날짜·시각 설정을 확인하세요. 자동 방문 처리는 멈춰 둡니다.</span></div>`;
  }
  if(!LOAD_ERROR) return "";
  return `<div class="crashbar loaderr">
    <b>예약 데이터를 불러오지 못했습니다.</b>
    <span>지금 보이는 화면은 비어 있는 상태이며, 저장이 막혀 있습니다. 인터넷을 확인하고 다시 시도하세요.</span>
    <button onclick="location.reload()">다시 불러오기</button>
    <i>${esc(LOAD_ERROR)}</i>
  </div>`;
}
function renderApp(){
  saveScroll();
  /* 다시 그리기 전에 타이핑 중인 값을 상태로 옮깁니다. 마법사 6단계에서 요청사항을 치다가 유아의자 ± 를 누르면 입력이 사라졌고,
     1분 갱신·폰 회전에도 같은 일이 났습니다(점검 R1). 입력칸이 없는 화면에서는 아무 일도 안 합니다 */
  try{ if(WZ) wzSyncInputs(); if(!WZ && tmpRes && view.form && view.form.type === "res") syncRes(); }catch(e){}
  applyTheme();
  /* 오늘이 아닌 날짜면 페이지 바탕도 검정 (applyTheme 이 className 을 통째로 다시 쓰므로 그 뒤에) */
  document.body.classList.toggle("notoday", notodayView());
  const pk = popKey(), mk = modalKey();
  document.body.classList.toggle("same-pop", pk === lastPopKey);
  document.body.classList.toggle("same-modal", mk === lastModalKey);
  lastPopKey = pk; lastModalKey = mk;
  /* 팝업이 떠 있으면 뒤 화면이 스크롤되지 않게 */
  document.body.style.overflow =
    (MODAL || (view.form && !view.form.page && !view.display) || view.calOpen || WZ) ? "hidden" : "";
  const app = document.getElementById("app");
  if(!DATA){ app.innerHTML="<p class='empty'>불러오는 중…</p>"; return; }
  /* 디스플레이 모드는 주소로 바로 열 수 있습니다 (TV 전용 화면) */
  if(view.display && view.storeKey){ app.innerHTML = renderDisplay() + renderModal(); afterRender(); return; }
  /* 매장을 고른 뒤에 PIN 을 입력합니다 */
  if(view.storeKey && !AUTHED){ app.innerHTML = renderLock() + renderModal(); syncHash(); afterRender(); return; }
  if(INTRO){ app.innerHTML = renderIntro(); return; }
  app.innerHTML = (view.display ? renderDisplay()
                  : (view.storeKey ? renderStore() : renderSelect())) + renderModal() + renderLoadError();
  syncHash();      /* 주소를 지금 화면에 맞춥니다 — 새로고침해도 그 자리로 */
  /* 라벨 충돌로 타임라인 행이 늘어날 수 있으므로 먼저 행 높이를 확정한 뒤 현재 시각선 높이를 맞춥니다. */
  if(typeof tlPlaceLabels === "function") tlPlaceLabels();
  afterRender();   /* 화면을 그린 뒤 필요한 이벤트 연결 (분 조절 레일 등) */
  if(typeof aiWaveStart === "function") aiWaveStart();   /* 감사 문자 AI 물결(14g) — 캔버스가 있을 때만 돎 */   /* 타임라인 라벨(사용 중지·자리 없음) 자리 — 실제 픽셀로 겹침을 보고 정함 */
}

/* ---------- 들어갈 때 인사 ----------
   PIN 을 맞히고 바로 화면이 튀어나오면 눌린 건지 아닌지 알기 어렵습니다.
   짧게(2초 안쪽) 인사를 띄워 '들어가는 중'이라는 감각을 줍니다.
   중식당이라 중국어(歡迎光臨)에서 한국어(어서오세요)로 글자가 하나씩 바뀌고,
   바탕은 붉은 칠기 → 어두운 나무색 → 한지·창살 세 단계로 따라갑니다.
   아무 데나 누르면 바로 건너뜁니다 — 바쁠 때 1초도 아깝습니다.
   ※ 글자가 바뀔 때마다 render() 로 화면을 다시 그리면 CSS 전환이 전혀 재생되지 않습니다
     (요소가 새로 만들어지니까). 처음 한 번만 그리고 그 뒤로는 클래스만 바꿉니다. */
var INTRO = null, introTimers = [];
var INTRO_FROM = "歡迎光臨";       /* 歡迎光臨 */
var INTRO_TO   = "어서오세요";  /* 어서오세요 */
function startIntro(){
  tryFullscreen();   /* 로그인 통과 → 인트로에서 전체화면(재아). PIN 을 누른 손짓 직후라 허락됩니다 */
  INTRO = { n:0 };
  clearIntro(true);
  render();                                   /* 한 번만 그립니다 */
  /* 글자 5개가 200ms 간격(1초) — 135ms 는 거의 동시라 단계가 안 느껴졌고, 260ms 는 붉은 첫 장면이 길었습니다(6차-F).
     첫 글자는 360ms, 마지막 글자 뒤 600ms 에 끝. 총 약 1.8초, 아무 데나 누르면 건너뜀 */
  var steps = INTRO_TO.length, t0 = 70, gap = 88;   /* 재아: 1.7배 빠르게 — 글자 88ms 간격, 총 0.8초쯤 */
  for(var i=1;i<=steps;i++){
    introTimers.push(setTimeout((function(k){ return function(){ introStep(k); }; })(i), t0 + i*gap));
  }
  introTimers.push(setTimeout(endIntro, t0 + steps*gap + 265));
}
/* 글자 진행 p(0~1)에 따른 바탕 두 겹의 불투명도 — 나무색은 앞 절반에서, 한지(와 창호)는 뒤 절반에서 올라옵니다 */
function introBg(n){
  var p = Math.min(1, n / Math.max(1, INTRO_TO.length - 1));
  return { mid: Math.min(1, p*2).toFixed(2), ko: Math.max(0, (p-.5)*2).toFixed(2) };
}
function clearIntro(keepState){
  for(var i=0;i<introTimers.length;i++) clearTimeout(introTimers[i]);
  introTimers = [];
  if(!keepState) INTRO = null;
}
function endIntro(){ tryFullscreen(); clearIntro(); INTRO = null; render(); }   /* 인트로를 눌러 건너뛸 때도 전체화면 시도(손짓이 있으니) */
/* k 번째 글자까지 바꿉니다. 화면을 다시 그리지 않고 클래스만 붙입니다 */
function introStep(k){
  if(!INTRO) return;
  INTRO.n = k;
  var root = document.querySelector(".intro");
  if(!root) return;
  root.className = "intro turning";
  var cn = root.querySelectorAll(".intro-word.cn .ic"), ko = root.querySelectorAll(".intro-word.ko .ic"), i;
  for(i=0;i<cn.length;i++) cn[i].className = "ic" + (i < k ? " off" : "");
  for(i=0;i<ko.length;i++) ko[i].className = "ic" + (i < k ? " on"  : "");
  /* 첫 글자가 바뀌는 순간 바탕도 함께 움직이기 시작하도록 조금 앞서 갑니다 (k=1 에 나무색 절반, k=2 에 나무색 완성, k=3~4 에 한지) */
  var bg = introBg(k), mid = root.querySelector(".intro-mid"), kos = root.querySelectorAll(".intro-ko, .intro-sash");
  if(mid) mid.style.opacity = bg.mid;
  for(i=0;i<kos.length;i++) kos[i].style.opacity = bg.ko;
}
/* 다른 이유로 render() 가 도중에 불려도 진행 중인 단계(INTRO.n)를 그대로 그립니다 */
function renderIntro(){
  var i, cn = "", ko = "", n = INTRO.n || 0;
  for(i=0;i<INTRO_FROM.length;i++) cn += '<span class="ic' + (i < n ? ' off' : '') + '">' + INTRO_FROM.charAt(i) + '</span>';
  for(i=0;i<INTRO_TO.length;i++)   ko += '<span class="ic' + (i < n ? ' on'  : '') + '">' + INTRO_TO.charAt(i) + '</span>';
  var bg = introBg(n);
  var pm = n ? ' style="opacity:' + bg.mid + '"' : '', pk = n ? ' style="opacity:' + bg.ko + '"' : '';
  return '<div class="intro' + (n ? ' turning' : '') + '" onclick="endIntro()">' +
           '<div class="intro-bg intro-cn"></div>' +
           '<div class="intro-bg intro-mid"' + pm + '></div>' +
           '<div class="intro-bg intro-ko"' + pk + '></div>' +
           '<div class="intro-sash l"' + pk + '></div><div class="intro-sash r"' + pk + '></div>' +
           '<div class="intro-w">' +
             '<div class="intro-word cn">' + cn + '</div>' +
             '<div class="intro-word ko">' + ko + '</div>' +
           '</div>' +
         '</div>';
}
