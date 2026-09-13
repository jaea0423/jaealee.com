# -*- coding: utf-8 -*-
"""v5 7차 묶음 B — 읽기 (Supabase)
   · SUPA_CFG(빌드가 채움) · sb() 헬퍼 · 로그인(PIN 4자리 + "00") · 세션(메모리+sessionStorage, 만료 5분 전 갱신)
   · loadFromServer: stores → reservations(365일) → logs(300) → 지금 DATA 모양 → migrate → 캐시
   · rowToRes / resToRow (행 ↔ 객체, 여기서만)
   · 캐시(localStorage) · 오프라인 읽기 전용 띠 · 30초 재시도
   · 쓰기는 아직 막음(_readonly) — 누르면 이유를 알림
   · _ui(테마·배율) 는 기기별이라 localStorage. tvType 은 매장 설정(settings.tvType)으로 이동
   · 손님용 TV·매장 선택 화면은 로그인 없이 공개 뷰(public_screen / public_today)만 읽음"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ============================================================
# 0. 설정 자리표시자 + Supabase 층 (loadData 바로 앞)
# ============================================================
rep("""/* ---------- 저장/불러오기 (실제 버전에서는 이 두 함수만 Supabase 호출로 교체) ---------- */
/* 불러오기에 실패했을 때의 상태. 화면 맨 위에 띠로 뜹니다 */
var LOAD_ERROR = null;
async function loadData(){
  /* 저장소가 아예 없으면(개발 중 · 파일로 열었을 때) 예시 데이터로 돕니다.
     저장소가 있는데 실패했으면 **절대 예시 데이터를 만들지 않습니다.**
     예전엔 실패하면 무조건 예시 1,300건을 만들었는데, DB 를 붙인 뒤 인터넷이 잠깐 끊기면
     그 가짜가 진짜 DB 에 저장되는 사고가 납니다. 실패하면 빈 상태로 멈추고 알립니다. */
  if(!window.storage || typeof window.storage.get !== "function"){""",
"""/* ============================================================
   Supabase (7차) — supabase-js 없이 fetch 로 REST·Auth 를 직접 부릅니다
   ("외부 요청 0" 원칙 유지, 파일 크기 그대로, 구형 TV 도 fetch 는 됩니다)
   SUPA_CFG 는 build.py 가 supabase.{dev|prod}.json 으로 채웁니다. null 이면 지금처럼 브라우저 안에서만(예시 데이터).
   결정 사항은 work/7차_작업지시.md — 여기 주석은 '왜' 만 짧게.
   ============================================================ */
var SUPA_CFG = __SUPA_CFG__;
var SESSION = null;          /* {access_token, refresh_token, expires_at(초), who:"staff"|"admin"} — 메모리 + sessionStorage 에만 */
var OFFLINE = null;          /* 서버를 못 읽어 캐시로 보는 중: {at:마지막 갱신, pin:재접속용 PIN} */
var READONLY_WHY = "";       /* 읽기 전용인 이유 (안내문에 씀) */
var SYNC = { res:{}, settings:{}, snapshots:{}, lastUpd:{} };   /* 마지막 동기화 때의 모양 — 묶음 C 의 flush 가 '바뀐 것만' 고르는 기준 */
var CACHE_KEY = "hanok.cache.v1", UI_KEY = "hanok.ui.v1", SESSION_KEY = "hanok.session.v1", PINH_KEY = "hanok.pinh.v1";
function supaOn(){ return !!(SUPA_CFG && SUPA_CFG.url && SUPA_CFG.anonKey); }
/* PIN 은 화면에서 4자리, Supabase 비밀번호는 최소 6자리 → 뒤에 "00" 을 붙여 씁니다 (재아 결정. 계정 비밀번호도 그렇게 등록) */
function pinToPassword(pin){ return String(pin) + "00"; }

/* 호출 하나. 실패는 Error 로 던집니다 — e.network(연결 없음) / e.status(HTTP) 로 구분 */
async function sb(path, opt){
  opt = opt || {};
  var headers = { "apikey": SUPA_CFG.anonKey,
                  "Authorization": "Bearer " + ((opt.anon || !SESSION) ? SUPA_CFG.anonKey : SESSION.access_token),
                  "Content-Type": "application/json" };
  if(opt.prefer) headers["Prefer"] = opt.prefer;
  var res;
  try{
    res = await fetch(SUPA_CFG.url + path, { method: opt.method || "GET", headers: headers,
                                             body: opt.body != null ? JSON.stringify(opt.body) : undefined });
  }catch(e){ var ne = new Error("서버에 연결할 수 없습니다"); ne.network = true; throw ne; }
  var text = await res.text(), json = null;
  try{ json = text ? JSON.parse(text) : null; }catch(e){}
  if(!res.ok){
    var he = new Error((json && (json.msg || json.message || json.error_description || json.error)) || ("HTTP " + res.status));
    he.status = res.status; he.body = json; throw he;
  }
  return json;
}

/* ---------- 세션 ---------- */
function sessionSave(){ try{ sessionStorage.setItem(SESSION_KEY, JSON.stringify(SESSION)); }catch(e){} }
function sessionLoad(){ try{ var j = JSON.parse(sessionStorage.getItem(SESSION_KEY) || "null"); if(j && j.access_token) SESSION = j; }catch(e){} }
function sessionClear(){ SESSION = null; try{ sessionStorage.removeItem(SESSION_KEY); }catch(e){} }
function sessionSet(j, email){
  SESSION = { access_token:j.access_token, refresh_token:j.refresh_token,
              expires_at: Math.floor(Date.now()/1000) + (j.expires_in || 3600),
              who: email === SUPA_CFG.adminEmail ? "admin" : "staff" };
  sessionSave();
}
async function sbLogin(email, password){
  var j = await sb("/auth/v1/token?grant_type=password", { method:"POST", anon:true, body:{ email:email, password:password } });
  sessionSet(j, email);
}
async function sbRefresh(){
  if(!SESSION) return;
  var j = await sb("/auth/v1/token?grant_type=refresh_token", { method:"POST", anon:true, body:{ refresh_token:SESSION.refresh_token } });
  sessionSet(j, SESSION.who === "admin" ? SUPA_CFG.adminEmail : SUPA_CFG.staffEmail);
}
/* 만료 5분 전에 갱신. 1분 타이머에서 부릅니다. 갱신이 거부되면(토큰 폐기) 잠급니다 — 연결만 없는 경우는 그대로 둡니다 */
async function sessionTick(){
  if(!SESSION || !supaOn()) return;
  if(SESSION.expires_at - Date.now()/1000 > 300) return;
  try{ await sbRefresh(); }
  catch(e){ if(!e.network){ sessionClear(); AUTHED = false; view.storeKey = null; render(); } }
}

/* ---------- 행 ↔ 예약 객체 — 모양을 만지는 곳은 이 둘뿐 ---------- */
var RES_TOP = { id:1, date:1, time:1, status:1, name:1, phone:1, people:1, roomId:1, updatedAt:1, deletedAt:1 };
function rowToRes(row){
  var rec = Object.assign({}, row.data || {});
  rec.id = row.id; rec.date = row.date; rec.time = row.time; rec.status = row.status;
  rec.name = row.name || "";
  rec.phone = row.phone ? phoneFmt(String(row.phone)) : "";     /* 서버는 숫자만, 화면은 하이픈 */
  rec.people = row.people; rec.roomId = row.room_id || null;
  rec.updatedAt = row.updated_at;                                /* 서버 시각 문자열 그대로 (파싱 금지 — 마이크로초가 잘립니다) */
  if(row.deleted_at) rec.deletedAt = row.deleted_at;
  if(!rec.createdAt && row.created_at) rec.createdAt = row.created_at;
  return rec;
}
function resToRow(rec, storeKey){
  var data = {}, k;
  for(k in rec) if(!RES_TOP[k] && k.charAt(0) !== "_") data[k] = rec[k];
  return { id:rec.id, store:storeKey, date:rec.date, time:rec.time, status:rec.status,
           name:rec.name || "", phone:String(rec.phone || "").replace(/\\D/g, ""),
           people:pplOf(rec), room_id:rec.roomId || null, data:data, deleted_at:rec.deletedAt || null };
}

/* ---------- 읽기 ---------- */
/* 1년치만 읽습니다. 1년 넘은 노쇼 이력은 안 보이는 것을 감수(지시서 6장) */
async function loadFromServer(){
  var from = shiftDate(todayStr(), -365), trashFrom = shiftDate(todayStr(), -30);
  var rows = await sb("/rest/v1/stores?select=*");
  var d = { _logs: [] }, keys = Object.keys(DEFAULT_DATA), i, k, srow;
  for(i = 0; i < keys.length; i++){
    k = keys[i]; srow = rows.find(function(r){ return r.key === k; }) || {};
    d[k] = { name: srow.name || DEFAULT_DATA[k].name, settings: srow.settings || {}, snapshots: srow.snapshots || {},
             reservations: [], trash: [], _updatedAt: srow.updated_at || "" };
    if(!DEFAULT_DATA[k].enabled) continue;                       /* 안집: 화면만 있고 비활성 — 예약은 안 읽습니다 */
    var rr = await sb("/rest/v1/reservations?store=eq." + k + "&date=gte." + from + "&select=*&order=date,time");
    rr.forEach(function(row){
      var rec = rowToRes(row);
      if(row.deleted_at){ if(row.deleted_at.slice(0,10) >= trashFrom) d[k].trash.push(rec); }
      else d[k].reservations.push(rec);
    });
  }
  var logs = await sb("/rest/v1/logs?select=*&order=at.desc&limit=300");
  d._logs = logs.reverse().map(function(l){ return { ts:l.at, ip:l.who || "", store:l.store, action:l.action, detail:l.detail, ua:l.ua }; });
  return d;
}
/* 서버에서 받은 것을 DATA 로. _ui(테마·배율)는 기기별이라 localStorage 에서 */
function assembleData(d){
  var data = migrate(d);
  data._ui = uiLoad();
  data._readonly = true; READONLY_WHY = "stage";               /* 7차 B: 쓰기는 묶음 C 에서. 그때까지 읽기 전용 */
  syncMark(data);
  return data;
}
/* 마지막 동기화 모양을 기억 — 묶음 C 의 flush 가 이것과 비교해 바뀐 것만 보냅니다 */
function syncMark(data){
  SYNC = { res:{}, settings:{}, snapshots:{}, lastUpd:{} };
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var st = data[k]; if(!st) return;
    SYNC.settings[k] = JSON.stringify(st.settings); SYNC.snapshots[k] = JSON.stringify(st.snapshots || {});
    var max = "";
    (st.reservations || []).concat(st.trash || []).forEach(function(r){ SYNC.res[r.id] = JSON.stringify(r); if((r.updatedAt || "") > max) max = r.updatedAt; });
    SYNC.lastUpd[k] = max;
  });
}
/* 로그인 뒤(또는 세션 복구 뒤) 서버를 읽어 들어갑니다 */
async function enterStore(){
  var d = await loadFromServer();
  DATA = assembleData(d);
  AUTHED = true; OFFLINE = null; LOAD_ERROR = null;
  cacheSave();
}
/* 1분 갱신. 묶음 C 에서 델타(updated_at=gt.)로 바꿉니다 — 지금은 통째로 다시 읽음 */
async function reloadFromStore(){
  if(!supaOn()) return;
  if(view.display && !SESSION){ await loadPublic(); return; }
  if(!SESSION) return;
  if(OFFLINE){ await reconnect(); return; }
  var d = await loadFromServer();
  var ui = DATA._ui;
  DATA = assembleData(d); DATA._ui = ui;
  cacheSave();
}

/* ---------- 캐시 · 오프라인 ---------- */
function cacheSave(){
  try{
    var out = { at: new Date().toISOString(), data: {} };
    Object.keys(DEFAULT_DATA).forEach(function(k){
      var st = DATA[k]; if(!st) return;
      out.data[k] = { name:st.name, settings:st.settings, snapshots:st.snapshots, reservations:st.reservations, trash:st.trash };
    });
    localStorage.setItem(CACHE_KEY, JSON.stringify(out));
  }catch(e){ console.warn("캐시 저장 실패", e); }
}
function cacheLoad(){ try{ return JSON.parse(localStorage.getItem(CACHE_KEY) || "null"); }catch(e){ return null; } }
function uiLoad(){ try{ return JSON.parse(localStorage.getItem(UI_KEY) || "null") || { theme:"hanok" }; }catch(e){ return { theme:"hanok" }; } }
function uiSave(){ try{ if(DATA && DATA._ui) localStorage.setItem(UI_KEY, JSON.stringify(DATA._ui)); }catch(e){} }
/* 오프라인에서 PIN 을 맞춰 볼 수단 — 마지막으로 서버가 받아 준 PIN 의 해시(djb2). 4자리 PIN 은 원래 약하니 이 정도로 */
function strHash(str){ var h = 5381, i; for(i = 0; i < str.length; i++) h = ((h << 5) + h + str.charCodeAt(i)) | 0; return String(h); }
function pinHashSave(pin){ try{ localStorage.setItem(PINH_KEY, strHash(pin + "|" + SUPA_CFG.url)); }catch(e){} }
function pinHashOk(pin){ try{ return localStorage.getItem(PINH_KEY) === strHash(pin + "|" + SUPA_CFG.url); }catch(e){ return false; } }
/* 서버를 못 읽을 때 캐시로 들어갑니다(읽기 전용). 캐시가 없으면 false */
function enterOffline(pin){
  var c = cacheLoad();
  if(!c || !c.data) return false;
  var ui = DATA && DATA._ui;
  DATA = migrate(deepClone(c.data)); DATA._ui = ui || uiLoad(); DATA._logs = DATA._logs || [];
  DATA._readonly = true; READONLY_WHY = "offline";
  OFFLINE = { at: c.at, pin: pin || (OFFLINE && OFFLINE.pin) || "" };
  AUTHED = true; LOAD_ERROR = null;
  return true;
}
/* 다시 연결 — 띠의 버튼과 30초 타이머가 부릅니다 */
async function reconnect(){
  if(!OFFLINE || !supaOn()) return;
  try{
    if(!SESSION && OFFLINE.pin) await sbLogin(SUPA_CFG.staffEmail, pinToPassword(OFFLINE.pin));
    if(!SESSION) return;
    await enterStore();
    render();
  }catch(e){ console.warn("재연결 실패", e.message); }
}
setInterval(function(){ if(OFFLINE) reconnect(); }, 30000);

/* ---------- 로그인 없이 읽는 공개 뷰 — 매장 선택 화면의 '오늘 예약 N건' 과 손님용 TV ----------
   TV 가 실제로 읽는 설정만(rooms·displayRows·tvAd·tvType). 이름은 서버가 가려서 옵니다(mask_name) */
async function loadPublic(){
  if(!supaOn() || AUTHED) return;
  var today = todayStr();
  var st = await sb("/rest/v1/public_screen?select=*", { anon:true });
  var tr = await sb("/rest/v1/public_today?select=*", { anon:true });
  var d = {};
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var row = st.find(function(r){ return r.store === k; }) || {}, sset = {}, key;
    /* 뷰는 없는 키를 null 로 줍니다(settings->'rooms'). null 을 그대로 넘기면 migrate 의 기본값을 덮어 화면이 죽습니다 */
    for(key in (row.settings || {})) if(row.settings[key] != null) sset[key] = row.settings[key];
    d[k] = { name: row.name || DEFAULT_DATA[k].name, settings: sset, reservations: [] };
    tr.forEach(function(r){
      if(r.store !== k) return;
      d[k].reservations.push({ id: k + "-" + r.time + "-" + r.name, date: today, time: r.time, name: r.name, people: r.people, roomId: r.room_id, status: r.status, masked: true });
    });
  });
  var ui = DATA && DATA._ui;
  DATA = migrate(d); DATA._ui = ui || uiLoad(); DATA._readonly = true; READONLY_WHY = "public";
  try{ localStorage.setItem("hanok.screen.v1", JSON.stringify({ at:new Date().toISOString(), data:d })); }catch(e){}
}

/* 쓰기가 막혀 있으면 이유를 알리고 true. 막지 않는 것이 원칙이지만 이 경우는 진짜로 저장이 불가능합니다 */
function readonlyBlock(){
  if(!DATA || !DATA._readonly) return false;
  var why = READONLY_WHY === "offline" ? "서버와 연결이 끊겨 지금은 볼 수만 있습니다. 종이에 적어 두세요 — 연결되면 다시 시도하세요."
          : READONLY_WHY === "stage"  ? "저장 기능은 아직 서버에 연결하기 전입니다(7차 C 단계)."
          : "데이터를 불러오지 못한 상태라 저장이 막혀 있습니다. 새로고침해 보세요.";
  uiAlert("지금은 저장할 수 없습니다", why, "warn");
  return true;
}

/* ---------- 저장/불러오기 ---------- */
/* 불러오기에 실패했을 때의 상태. 화면 맨 위에 띠로 뜹니다 */
var LOAD_ERROR = null;
async function loadData(){
  if(supaOn()){
    /* 서버 모드: 로그인 전에는 빈 뼈대. 세션이 sessionStorage 에 살아 있으면(같은 탭 새로고침) 바로 읽어 들어갑니다 */
    DATA = migrate(deepClone(DEFAULT_DATA)); DATA._ui = uiLoad(); DATA._readonly = true; READONLY_WHY = "public";
    sessionLoad();
    if(SESSION){
      try{ await enterStore(); }
      catch(e){
        console.error("불러오기 실패", e);
        if(e.network){ if(!enterOffline()) LOAD_ERROR = e.message; }
        else { sessionClear(); LOAD_ERROR = e.message; }
      }
    }
    if(!AUTHED) loadPublic().then(function(){ render(); }).catch(function(e){ console.warn("공개 뷰 실패", e.message); });
  }else
  /* 저장소가 아예 없으면(개발 중 · 파일로 열었을 때) 예시 데이터로 돕니다.
     저장소가 있는데 실패했으면 **절대 예시 데이터를 만들지 않습니다.**
     예전엔 실패하면 무조건 예시 1,300건을 만들었는데, DB 를 붙인 뒤 인터넷이 잠깐 끊기면
     그 가짜가 진짜 DB 에 저장되는 사고가 납니다. 실패하면 빈 상태로 멈추고 알립니다. */
  if(!window.storage || typeof window.storage.get !== "function"){""")

# 세션 복구는 서버 모드에선 sessionStorage(SESSION) 가 맡습니다
rep("""  if(DATA._session && DATA._session.authed) AUTHED = true;
  document.getElementById("app").setAttribute("data-ok","1");""",
"""  if(!supaOn() && DATA._session && DATA._session.authed) AUTHED = true;
  document.getElementById("app").setAttribute("data-ok","1");""")

# saveData — 서버 모드에서는 묶음 C 까지 아무것도 안 보냄. _ui 는 항상 기기에 저장
rep("""async function saveData(){
  if(DATA && DATA._readonly) return;   /* 불러오기 실패 상태 — 덮어쓰지 않습니다 */
  try{ await window.storage.set(STORAGE_KEY, JSON.stringify(DATA)); }
  catch(e){ console.error("저장 실패", e); }
}""",
"""async function saveData(){
  uiSave();                            /* 테마·배율·tvType 폴백은 기기별 — 서버와 무관하게 늘 저장 */
  if(DATA && DATA._readonly) return;   /* 불러오기 실패 · 오프라인 · 7차 B 단계 — 덮어쓰지 않습니다 */
  if(supaOn()) return;                 /* 묶음 C 에서 flush(바뀐 것만 PATCH/POST)로 채웁니다 */
  try{ await window.storage.set(STORAGE_KEY, JSON.stringify(DATA)); }
  catch(e){ console.error("저장 실패", e); }
}""")

# migrate — tvType 을 _ui 에서 settings 로 (TV 가 공개 뷰로 읽으려면 매장 설정이어야 합니다)
rep("""function migrate(d){
  d._auth = d._auth || {...DEFAULT_AUTH};
  d._logs = d._logs || [];""",
"""function migrate(d){
  d._auth = d._auth || {...DEFAULT_AUTH};
  d._logs = d._logs || [];
  /* tvType(목록형/좌석표)은 기기 설정(_ui)에 있었는데 TV 가 공개 뷰로 읽으려면 매장 설정이어야 합니다 → settings.tvType (7차) */
  if(d._ui && d._ui.tvType && d.hanok && d.hanok.settings && !d.hanok.settings.tvType) d.hanok.settings.tvType = d._ui.tvType;""")

# ============================================================
# 1. 로그인 — PIN → staff 계정
# ============================================================
rep("""var PIN_ANY = true;
function pinCheck(){
  const real = PIN_BUF === ((DATA._auth && DATA._auth.pin) || DEFAULT_AUTH.pin);""",
"""var PIN_ANY = true;
var LOCK_BUSY = false;   /* 서버에 PIN 을 확인하는 중 — 잠금 화면에 '확인 중' 표시 */
async function pinCheck(){
  if(supaOn()) return pinCheckServer();
  const real = PIN_BUF === ((DATA._auth && DATA._auth.pin) || DEFAULT_AUTH.pin);""")
rep("""function lockNow(){
  logEvent("잠금", "");
  AUTHED=false; PIN_BUF=""; PIN_ERR=""; view.storeKey=null;
  DATA._session = {authed:false};
  saveData(); render();
}""",
"""/* 서버 모드 — PIN 4자리를 staff 계정 비밀번호(PIN+"00")로 로그인. 맞으면 서버를 읽어 들어갑니다.
   연결이 없으면: 마지막으로 서버가 받아 준 PIN 과 같을 때만 캐시로 들어갑니다(읽기 전용) */
async function pinCheckServer(){
  var pin = PIN_BUF;
  LOCK_BUSY = true; PIN_ERR = ""; render();
  try{
    await sbLogin(SUPA_CFG.staffEmail, pinToPassword(pin));
    pinHashSave(pin);
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
      PIN_ERR = "PIN 번호가 맞지 않습니다.";
    }else{
      PIN_ERR = "로그인 실패: " + e.message;
    }
    console.warn("로그인 실패", e.status, e.message);
  }
  LOCK_BUSY = false; render();
}
function lockNow(){
  logEvent("잠금", "");
  AUTHED=false; PIN_BUF=""; PIN_ERR=""; view.storeKey=null;
  DATA._session = {authed:false};
  sessionClear(); OFFLINE = null;
  saveData(); render();
}""")
rep("""function goHome(){
  logEvent("잠금", "매장 선택으로");
  AUTHED=false; PIN_BUF=""; PIN_ERR=""; view.storeKey=null; view.draft=null;
  if(DATA) DATA._session = {authed:false};
  saveData(); render();
}""",
"""function goHome(){
  logEvent("잠금", "매장 선택으로");
  AUTHED=false; PIN_BUF=""; PIN_ERR=""; view.storeKey=null; view.draft=null;
  if(DATA) DATA._session = {authed:false};
  sessionClear(); OFFLINE = null;
  saveData(); render();
  if(supaOn()) loadPublic().then(function(){ render(); }).catch(function(){});   /* 매장 선택의 '오늘 예약 N건' */
}""")
# 잠금 화면 — 확인 중 표시, 4자리 입력 중 잠금
rep("""        <div class="lk-err">${esc(PIN_ERR)}</div>""",
    """        <div class="lk-err ${LOCK_BUSY?'busy':''}">${LOCK_BUSY ? "서버 확인 중…" : esc(PIN_ERR)}</div>""")
rep("""function pinPush(n){
  if(PIN_BUF.length>=4) return;""",
"""function pinPush(n){
  if(PIN_BUF.length>=4 || LOCK_BUSY) return;""")
rep(""".lk-err{height:20px; font-size:var(--fs-sub); color:var(--rust); font-weight:600; margin-bottom:var(--s16)}""",
    """.lk-err{height:20px; font-size:var(--fs-sub); color:var(--rust); font-weight:600; margin-bottom:var(--s16)}
.lk-err.busy{color:var(--text-3)}   /* 서버 확인 중 — 오류가 아니라 회색 */""")

# ============================================================
# 2. 1분 타이머 — 세션 갱신 · 디스플레이 실패 카운트
# ============================================================
rep("""  if(SNAP_DAY && todayStr() !== SNAP_DAY) takeSnapshot();
  if(!AUTHED || view.display || WZ || view.form || MODAL) return;""",
"""  if(SNAP_DAY && todayStr() !== SNAP_DAY) takeSnapshot();
  sessionTick();   /* 토큰 만료 5분 전 갱신 */
  if(!AUTHED || view.display || WZ || view.form || MODAL) return;""")
rep("""async function refreshData(){
  try{
    if(typeof reloadFromStore === "function") await reloadFromStore();   /* Supabase 연동 뒤에 채워집니다 */
    LAST_REFRESH = Date.now();
  }catch(e){ console.error("갱신 실패", e); }
}""",
"""async function refreshData(){
  try{
    await reloadFromStore();
    LAST_REFRESH = Date.now();
  }catch(e){
    console.error("갱신 실패", e.message);
    if(view.display) throw e;                                  /* TV 는 3번 연속 실패를 세어 '연결 확인 중' 을 띄웁니다 */
    if(e.network && !OFFLINE && SESSION){ enterOffline(); render(); }   /* 보던 중 연결이 끊김 → 캐시 읽기 전용으로 */
  }
}""")

# ============================================================
# 3. 띠 — 오프라인 / 단계 / 불러오기 실패
# ============================================================
rep("""function renderLoadError(){
  if(!LOAD_ERROR) return "";""",
"""function renderLoadError(){
  if(view.display) return "";
  if(OFFLINE && AUTHED){
    var d = OFFLINE.at ? new Date(OFFLINE.at) : null;          /* 캐시 시각은 UTC 문자열 — 한국 시각으로 */
    var at = d && !isNaN(d) ? pad(d.getHours()) + ":" + pad(d.getMinutes()) : "-";
    return `<div class="crashbar offline">
      <b>오프라인</b><span>마지막 갱신 ${esc(at || "-")} · 지금은 볼 수만 있습니다. 30초마다 다시 연결해 봅니다.</span>
      <button onclick="reconnect()">다시 연결</button></div>`;
  }
  if(AUTHED && DATA && DATA._readonly && READONLY_WHY === "stage")
    return `<div class="crashbar stage"><b>읽기 전용</b><span>서버 연결 7차 B 단계 — 저장 기능은 C 에서 붙습니다.</span></div>`;
  if(!LOAD_ERROR) return "";""")
rep(""".crashbar button{margin-left:auto; background:#fff; color:#A63B26; border:none;
  border-radius:var(--r-sm); padding:var(--s8) var(--s16); font-weight:700; font-size:var(--fs-sub)}""",
""".crashbar button{margin-left:auto; background:#fff; color:#A63B26; border:none;
  border-radius:var(--r-sm); padding:var(--s8) var(--s16); font-weight:700; font-size:var(--fs-sub)}
/* 오프라인(캐시로 보는 중)은 갈색 — 빨강은 '고장' 이라 구분. 단계 띠(7차 B)는 호박색 */
.crashbar.offline{background:#5A4E40}
.crashbar.offline button{color:#5A4E40}
.crashbar.stage{background:#8A6512; padding:var(--s8) var(--s16)}""")

# ============================================================
# 4. 쓰기 진입점 — 읽기 전용이면 이유를 알림
# ============================================================
rep("""function openWizard(date){
  histPush();""", """function openWizard(date){
  if(readonlyBlock()) return;
  histPush();""")
rep("""function openRes(id){ histPush(); view.form={type:"res", id}; render(); }""",
    """function openRes(id){ if(readonlyBlock()) return; histPush(); view.form={type:"res", id}; render(); }""")
rep("""async function markRes(id, status){
  const s = store();""", """async function markRes(id, status){
  if(readonlyBlock()) return;
  const s = store();""")
rep("""async function delRes(id){
  const s=store();""", """async function delRes(id){
  if(readonlyBlock()) return;
  const s=store();""")
rep("""function applySettings(){
  if(!view.draft) return;""", """function applySettings(){
  if(!view.draft) return;
  if(readonlyBlock()) return;""")

# ============================================================
# 5. tvType → settings.tvType · 예시 데이터 버튼은 demo 일 때만
# ============================================================
rep("""function tvType(){
  var t = DATA && DATA._ui ? DATA._ui.tvType : null;
  return t === "grid" ? "grid" : "list";
}
function setTvType(t){
  if(!DATA._ui) DATA._ui = {};
  DATA._ui.tvType = (t === "grid" ? "grid" : "list");
  saveData(); render();
}""",
"""/* 목록형/좌석표 — 매장 설정(settings.tvType). TV 가 로그인 없이 공개 뷰로 읽는 값이라 기기 설정(_ui)이면 안 됩니다 (7차) */
function tvType(){
  var st = view.storeKey && DATA && DATA[view.storeKey] ? DATA[view.storeKey].settings : null;
  var t = st && st.tvType ? st.tvType : (DATA && DATA._ui ? DATA._ui.tvType : null);
  return t === "grid" ? "grid" : "list";
}
function setTvType(t){
  if(readonlyBlock()) return;
  t = (t === "grid" ? "grid" : "list");
  /* 설정 화면(임시본) 안의 버튼이라 임시본과 실제 설정에 같이 씁니다 — 아니면 '적용하기' 가 옛값으로 되돌립니다 */
  if(view.draft) view.draft.tvType = t;
  store().settings.tvType = t;
  saveData(); render();
}""")
rep("""      <button class="btn danger" onclick="clearDemo()">예시 데이터 지우기</button>
      <button class="btn" onclick="addDemo()">예시 데이터 넣기</button>""",
"""      ${(!supaOn() || SUPA_CFG.demo) ? `<button class="btn danger" onclick="clearDemo()">예시 데이터 지우기</button>
      <button class="btn" onclick="addDemo()">예시 데이터 넣기</button>` : ""}""")
rep("""async function addDemo(){
  if(!await uiConfirm2(""", """async function addDemo(){
  if(readonlyBlock()) return;
  if(!await uiConfirm2(""")

# 공개 뷰에서 온 이름은 이미 가려져 있습니다 — 다시 가리면 "조 * * * 결" 이 됩니다
rep("""function maskName(n){
  const s = String(n||"").trim();
  if(s.length<=1) return s;""",
"""function maskName(n){
  const s = String(n||"").trim();
  if(s.indexOf("*") >= 0) return s;   /* 서버(mask_name)가 이미 가린 이름 */
  if(s.length<=1) return s;""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_b 적용 완료")
