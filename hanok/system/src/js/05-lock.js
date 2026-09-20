/* ============================================================
   PIN 잠금 — 새로 열 때마다 입력합니다 (자동 로그인 없음)
   ============================================================ */
let AUTHED = false;
let PIN_BUF = "";
let PIN_ERR = "";

function renderLock(){
  const s = view.storeKey ? DATA[view.storeKey] : null;
  /* 자리를 채울 때마다 매장 이름 한 글자씩 나타납니다 */
  const marks = (s && s.name.length>=4) ? s.name.split("").slice(0,4) : ["한","옥","반","점"];
  const dots = [0,1,2,3].map(i=>
    `<span class="pdot f${i+1} ${i<PIN_BUF.length?'on':''}">${i<PIN_BUF.length?marks[i]:""}</span>`).join("");
  const keys = [1,2,3,4,5,6,7,8,9,"clear",0,"back"].map(k=>{
    if(k==="clear") return `<button class="pkey sub" onclick="pinClear()" title="다시 입력">↻</button>`;
    if(k==="back")  return `<button class="pkey sub" onclick="pinBack()">←</button>`;
    return `<button class="pkey" onclick="pinPush('${k}')">${k}</button>`;
  }).join("");
  return `
    <div class="lock">
      <div class="lockbox">
        <div class="lk-logo" role="img" aria-label="${esc(s?s.name:"")}"></div>   <!-- 09-20: 글자 대신 로고(사이트 로고의 먹색 판) -->
        <div class="pdots">${dots}</div>
        <div class="lk-err ${LOCK_BUSY?'busy':''}">${LOCK_BUSY ? "확인 중…" : (pinLockLeft() > 0 ? `${pinLockLeft()}초 뒤에 다시 입력할 수 있습니다` : esc(PIN_ERR))}</div>
        <div class="pkeys">${keys}</div>
        ${supaOn() ? "" : `<div class="lk-open"><b>서버 설정이 없는 빌드</b> — supabase.dev.json 또는 supabase.prod.json 을 넣고 다시 빌드하세요</div>`}
        <!-- '매장 다시 고르기' 는 뺌(09-20) — 매장이 하나 -->
      </div>
    </div>`;
}
function pinPush(n){
  if(!view.storeKey || view.display || AUTHED) return;   /* 잠금 화면일 때만. TV 리모컨 숫자키가 로그인 시도가 됐습니다(점검 U1) */
  if(PIN_BUF.length>=4 || LOCK_BUSY || pinLockLeft() > 0) return;
  PIN_BUF += n; PIN_ERR="";

  if(PIN_BUF.length===4) setTimeout(pinCheck, 120);
  render();
}
function pinBack(){ PIN_BUF = PIN_BUF.slice(0,-1); render(); }
function pinClear(){ PIN_BUF=""; PIN_ERR=""; render(); }
function backToStores(){ view.storeKey=null; PIN_BUF=""; PIN_ERR=""; render(); }
/* ============================================================
   PIN 확인
   서버 모드(SUPA_CFG 있음): PIN 4자리 + "00" 으로 staff 계정 로그인 — 진짜 검증. 틀림 5회 → 60초 잠금.
   서버 설정이 없는 빌드: 들어갈 수 없습니다(7차-H). build.py 가 prod 설정이 없으면 dev 설정을 쓰므로 사이트에 설정 없는 빌드가 올라갈 일은 없습니다.
   ============================================================ */
var PIN_FAILS = 0, PIN_LOCK_UNTIL = 0;   /* 틀린 횟수 · 잠금 해제 시각(ms) */
function pinLockLeft(){ return Math.max(0, Math.ceil((PIN_LOCK_UNTIL - Date.now()) / 1000)); }
var LOCK_BUSY = false;   /* 서버에 PIN 을 확인하는 중 — 잠금 화면에 '확인 중' 표시 */
async function pinCheck(){
  if(supaOn()) return pinCheckServer();
  /* 서버 설정이 없는 빌드 — PIN 을 확인할 곳이 없으므로 들어갈 수 없습니다 (재아 결정: 정해진 비밀번호로만).
     화면 확인용 스크린샷은 AUTHED 를 직접 켜서 찍습니다(work/shot.py) */
  PIN_BUF = ""; PIN_ERR = "서버 설정이 없는 빌드입니다. 들어갈 수 없습니다.";
  render();
}
/* 틀린 PIN 을 세고 5회면 60초 잠급니다. Supabase 에도 로그인 제한이 있지만 화면에서 먼저 막아 둡니다 */
function pinFailed(){
  PIN_FAILS++;
  if(PIN_FAILS >= 5){
    PIN_FAILS = 0; PIN_LOCK_UNTIL = Date.now() + 60000;
    logEvent("로그인 잠금", "PIN 5회 틀림 · 60초");
    var t = setInterval(function(){ if(pinLockLeft() <= 0){ clearInterval(t); PIN_ERR = ""; } render(); }, 1000);
  }
}
/* 서버 모드 — PIN 4자리를 staff 계정 비밀번호(PIN+"00")로 로그인. 맞으면 서버를 읽어 들어갑니다.
   연결이 없으면: 마지막으로 서버가 받아 준 PIN 과 같을 때만 캐시로 들어갑니다(읽기 전용) */
async function pinCheckServer(){
  var pin = PIN_BUF;
  LOCK_BUSY = true; PIN_ERR = ""; render();
  try{
    await sbLogin(SUPA_CFG.staffEmail, pinToPassword(pin));
    PIN_FAILS = 0; pinHashSave(pin);
    await enterStore();
    PIN_BUF = ""; PIN_ERR = "";
    logEvent("로그인 성공", "staff");
    LOCK_BUSY = false;
    startIntro();
    return;
  }catch(e){
    PIN_BUF = "";
    if(e.network){
      if(pinHashOk(pin) && enterOffline(pin)){ LOCK_BUSY = false; startIntro(); return; }
      PIN_ERR = "서버에 연결할 수 없습니다";
    }else if(e.status === 400){                      /* Supabase: 비밀번호 틀림 = 400 invalid_credentials. 401 은 API 키 문제라 따로 */
      PIN_ERR = "PIN 번호가 맞지 않습니다."; pinFailed();
    }else if(e.status === 429){
      PIN_ERR = "너무 여러 번 틀렸습니다. 잠시 뒤 다시 시도하세요.";
    }else{
      PIN_ERR = "로그인 실패: " + e.message;
    }
    console.warn("로그인 실패", e.status, e.message);
  }
  LOCK_BUSY = false; render();
}
/* 잠그기 전에 못 보낸 변경을 마저 보냅니다. 세션을 먼저 지우면 남은 PATCH 가 anon 으로 나가 401 이 났습니다(점검 D8) */
async function flushBeforeLeave(){
  if(!supaOn() || !SESSION) return true;
  if(FLUSHING || hasDirty()){ try{ await flush(); }catch(e){} }
  if(SAVE_FAIL || hasDirty()){
    return await uiConfirm("아직 서버에 저장되지 않은 변경이 있습니다", "지금 나가면 그 변경은 사라집니다. 그래도 나갈까요?", {ok:"버리고 나가기", cancel:"머무르기"});
  }
  return true;
}
/* 마법사·달력·더보기·확인창을 한 번에 접습니다. 세션 만료·주소 이동으로 화면이 바뀔 때 옛 마법사가 남거나
   body 의 overflow:hidden 이 남아 스크롤이 안 되던 것(점검 U3) */
function resetOverlays(){
  WZ = null; tmpRes = null; view.form = null; view.calOpen = false; view.moreOpen = false; view.pickSeat = null;
  if(typeof MODAL !== "undefined" && MODAL && MODAL.res){ try{ MODAL.res(false); }catch(e){} }
  MODAL = null;
  try{ document.body.style.overflow = ""; }catch(e){}
}
async function lockNow(){
  if(!await flushBeforeLeave()) return;
  resetOverlays();
  logEvent("잠금", "");
  AUTHED=false; PIN_BUF=""; PIN_ERR=""; view.storeKey=null; view.draft=null; view.adminOk=false;
  DATA._session = {authed:false};
  sessionClear(); OFFLINE = null;
  saveData(); render();
}
/* 더보기 → 종료하기: 로그아웃하고 창을 닫습니다(재아).
   브라우저는 스크립트가 연 창만 window.close() 로 닫아 줍니다 — 태블릿 홈 화면 앱(PWA)이나 직접 연 탭은 안 닫힐 수 있어,
   그럴 땐 '종료했습니다 · 창을 닫아 주세요' 화면을 보여 줍니다(다시 열면 처음부터) */
async function exitApp(){
  if(!await uiConfirm("종료할까요?", "로그아웃하고 이 창을 닫습니다.", {ok:"종료", cancel:"취소"})) return;
  if(!await flushBeforeLeave()) return;
  resetOverlays();
  logEvent("종료", "");
  AUTHED=false; PIN_BUF=""; PIN_ERR=""; view.storeKey=null; view.draft=null; view.adminOk=false;
  DATA._session = {authed:false};
  sessionClear(); OFFLINE = null;
  try{ saveData(); }catch(e){}
  try{ window.close(); }catch(e){}
  setTimeout(function(){
    document.body.innerHTML = '<div class="bye"><b>종료했습니다</b><span>이 창은 닫아도 됩니다.</span><button class="btn" onclick="location.reload()">다시 열기</button></div>';
  }, 300);
}
/* PC에서 키보드로도 입력 */
function pinKeydown(e){
  if(AUTHED) return;
  if(/^[0-9]$/.test(e.key)){ e.preventDefault(); pinPush(e.key); }
  else if(e.key==="Backspace"){ e.preventDefault(); pinBack(); }
  else if(e.key==="Escape"){ e.preventDefault(); pinClear(); }
}
document.addEventListener("keydown", pinKeydown);

/* 첫 줄을 제목으로, 나머지를 본문으로 나눠 띄웁니다 */
function splitMsg(m){
  const s = String(m||"").split("\n");
  const title = s[0].replace(/[?!.]$/,"") || "확인";
  return [title, s.slice(1).join("\n").trim()];
}
async function uiConfirm2(msg, opt){
  const [t,b] = splitMsg(msg);
  return uiConfirm(t, b || t, opt);
}
async function uiAlert2(msg){
  const [t,b] = splitMsg(msg);
  return uiAlert(t, b || "");
}
