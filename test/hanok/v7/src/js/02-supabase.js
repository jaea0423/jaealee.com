/* ============================================================
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
/* 캐시·세션 키에 프로젝트 주소를 붙입니다 — dev 와 실서비스가 같은 origin(jaealee.com)이라 안 붙이면 prod 오프라인 때 dev 더미가 보였습니다(점검 D11) */
var PROJ_TAG = (function(){ try{ return supaOn() ? "." + SUPA_CFG.url.replace(/^https?:\/\//, "").split(".")[0] : ""; }catch(e){ return ""; } })();
var CACHE_KEY = "hanok.cache.v1" + PROJ_TAG, UI_KEY = "hanok.ui.v1", SESSION_KEY = "hanok.session.v1" + PROJ_TAG, PINH_KEY = "hanok.pinh.v1" + PROJ_TAG;
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
  if(opt.range){ headers["Range-Unit"] = "items"; headers["Range"] = opt.range; }
  var res, ctl = (typeof AbortController === "function") ? new AbortController() : null;
  var timer = ctl ? setTimeout(function(){ ctl.abort(); }, 15000) : null;   /* 응답이 영영 안 오면(half-open) 15초 뒤 끊습니다 */
  try{
    res = await fetch(SUPA_CFG.url + path, { method: opt.method || "GET", headers: headers,
                                             body: opt.body != null ? JSON.stringify(opt.body) : undefined,
                                             signal: ctl ? ctl.signal : undefined });
  }catch(e){ var ne = new Error("서버에 연결할 수 없습니다"); ne.network = true; throw ne; }
  finally{ if(timer) clearTimeout(timer); }
  /* 기기 시계 검사(점검 D4) — RTC 가 죽은 태블릿은 날짜가 몇 년씩 틀립니다. 서버 응답의 Date 헤더와 비교해 둡니다 */
  try{ var sd = res.headers && res.headers.get("date"); if(sd){ var sms = Date.parse(sd); if(!isNaN(sms)) CLOCK_SKEW = sms - Date.now(); } }catch(e){}
  var text = await res.text(), json = null;
  try{ json = text ? JSON.parse(text) : null; }catch(e){}
  if(!res.ok){
    var he = new Error((json && (json.msg || json.message || json.error_description || json.error)) || ("HTTP " + res.status));
    he.status = res.status; he.body = json; throw he;
  }
  return json;
}

/* 1,000행 넘는 목록을 Range 헤더로 끝까지 이어 받습니다 (PostgREST 페이지 한도) */
async function sbAll(path){
  var out = [], start = 0, STEP = 1000;
  while(true){
    var page = await sb(path, { range: start + "-" + (start + STEP - 1) });
    out = out.concat(page || []);
    if(!page || page.length < STEP) break;
    start += STEP;
  }
  return out;
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
  catch(e){
    /* 토큰이 정말 거부된 경우(400/401/403)만 잠급니다. 서버 장애(5xx)·과다 요청(429)·연결 없음은 다음 분에 다시 시도 —
       잠그면 재로그인 때 못 보낸 변경이 사라집니다(점검 D7) */
    if(!e.network && e.status && e.status < 500 && e.status !== 429){ sessionClear(); AUTHED = false; view.storeKey = null; resetOverlays(); render(); }
  }
}

/* ---------- 행 ↔ 예약 객체 — 모양을 만지는 곳은 이 둘뿐 ---------- */
var RES_TOP = { id:1, date:1, time:1, status:1, name:1, phone:1, people:1, roomId:1, updatedAt:1, deletedAt:1 };
function rowToRes(row){
  /* 서버 행은 다른 기기(또는 토큰을 가진 누군가)가 쓴 것이라 모양을 믿지 않습니다. id·날짜·시각·좌석 id 는 onclick 문자열 안으로 들어가므로
     형식이 어긋나면 그 행을 버립니다(null) — 점검 S5 에서 id 에 JS 를 넣어 실행되는 것을 재현했습니다 */
  var ID = /^[A-Za-z0-9_-]{1,64}$/, DATE = /^\d{4}-\d{2}-\d{2}$/, TIME = /^\d{2}:\d{2}$/;
  if(!row || !ID.test(String(row.id)) || !DATE.test(String(row.date)) || !TIME.test(String(row.time))) return null;
  var rec = Object.assign({}, row.data || {});
  rec.id = row.id; rec.date = row.date; rec.time = row.time; rec.status = STATUS.indexOf(row.status) >= 0 ? row.status : "확정";
  rec.name = String(row.name || "");
  rec.phone = row.phone ? phoneFmt(String(row.phone)) : "";     /* 서버는 숫자만, 화면은 하이픈 */
  rec.people = Math.max(0, parseInt(row.people) || 0); rec.roomId = ID.test(String(row.room_id || "")) ? row.room_id : null;
  var okId = function(x){ return typeof x === "string" && ID.test(x); };
  rec.extraIds = Array.isArray(rec.extraIds) ? rec.extraIds.filter(okId) : [];
  rec.tentativeRoomId = okId(rec.tentativeRoomId) ? rec.tentativeRoomId : null;
  rec.tentativeExtra = Array.isArray(rec.tentativeExtra) ? rec.tentativeExtra.filter(okId) : [];
  if(rec.seatPref != null && ["any","room-any","table-any","hall-any"].indexOf(rec.seatPref) < 0 && !/^table:[\w가-힣 -]{0,20}$/.test(String(rec.seatPref))) rec.seatPref = null;
  rec.updatedAt = row.updated_at;                                /* 서버 시각 문자열 그대로 (파싱 금지 — 마이크로초가 잘립니다) */
  if(row.deleted_at) rec.deletedAt = row.deleted_at;
  if(!rec.createdAt && row.created_at) rec.createdAt = row.created_at;
  return rec;
}
function resToRow(rec, storeKey){
  var data = {}, k;
  for(k in rec) if(!RES_TOP[k] && k.charAt(0) !== "_") data[k] = rec[k];
  return { id:rec.id, store:storeKey, date:rec.date, time:rec.time, status:rec.status,
           name:rec.name || "", phone:String(rec.phone || "").replace(/\D/g, ""),
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
             reservations: [], trash: [], _updatedAt: srow.updated_at || "",
             _rawSettings: JSON.stringify(srow.settings || {}) };   /* 서버에 있던 그대로 — migrate 가 기본값을 채운 것과 다르면 첫 flush 가 올립니다 */
    if(!DEFAULT_DATA[k].enabled) continue;                       /* 안집: 화면만 있고 비활성 — 예약은 안 읽습니다 */
    /* PostgREST 는 한 번에 최대 1,000행만 줍니다. 1년치 예약 + 휴지통이 그보다 많으면 뒤가 잘려 최근 예약이 안 보였습니다 —
       Range 헤더로 이어 받고, 오래된 휴지통 행(30일 지난 soft delete)은 서버에서 거릅니다 */
    var rr = await sbAll("/rest/v1/reservations?store=eq." + k + "&date=gte." + from + "&or=(deleted_at.is.null,deleted_at.gte." + trashFrom + ")&select=*&order=date,time,id");
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
  data._readonly = false; READONLY_WHY = "";
  syncMark(data);
  return data;
}
/* 마지막 동기화 모양을 기억 — 묶음 C 의 flush 가 이것과 비교해 바뀐 것만 보냅니다 */
function syncMark(data){
  SYNC = { res:{}, settings:{}, snapshots:{}, lastUpd:{}, storeUpd:{} };
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var st = data[k]; if(!st) return;
    /* 설정은 '서버에 있던 원본' 을 기준으로 — 서버가 {} 이면 migrate 가 채운 기본값 전체가 첫 flush 때 올라갑니다 */
    SYNC.settings[k] = st._rawSettings != null ? st._rawSettings : JSON.stringify(st.settings); SYNC.snapshots[k] = JSON.stringify(st.snapshots || {});
    SYNC.storeUpd[k] = st._updatedAt || "";
    delete st._rawSettings;
    var max = "";
    (st.reservations || []).concat(st.trash || []).forEach(function(r){
      /* 불러오며 모양을 고친 예약은 서버 것과 다르므로 '동기화 전' 으로 — 다음 flush 가 올립니다(시각은 남겨 조건부 PATCH 가 되게) */
      SYNC.res[r.id] = MIGRATED_RES[r.id] ? JSON.stringify(Object.assign({}, r, {_legacy:1})) : JSON.stringify(r);
      if((r.updatedAt || "") > max) max = r.updatedAt;
    });
    MIGRATED_RES = {};
    SYNC.lastUpd[k] = max;
  });
}
/* 로그인 뒤(또는 세션 복구 뒤) 서버를 읽어 들어갑니다 */
async function enterStore(){
  var d = await loadFromServer();
  DATA = assembleData(d);
  AUTHED = true; OFFLINE = null; LOAD_ERROR = null;
  cacheSave();
  autoCloseDays();   /* 지난 날짜의 '확정' → '방문' (이 기기가 처음 켠 것이면 여기서 올라갑니다) */
  takeSnapshot();
  reflowFuture();    /* 잠정 배정은 겹침을 봐야 하므로 다른 곳에서 들어온 예약까지 포함해 다시 계산 */
  saveData();        /* 불러오며 모양을 고친 예약(옛 홀 배정 등)이 있으면 여기서 올라갑니다. 없으면 flush 가 보낼 것이 없어 조용합니다 */
}
/* 오늘 이후 날짜의 잠정 배정(룸 미정 예약의 tentativeRoomId)을 다시 계산합니다.
   잠정 배정은 그 날 다른 예약과의 겹침으로 정해지는 값이라, 다른 기기·시드·복구로 들어온 예약이 있으면 틀어집니다.
   바뀐 것은 saveData → flush 로 올라가고, 두 기기가 같은 답을 내면 충돌로 치지 않습니다(pushChanged 의 같은 내용 처리) */
function reflowFuture(){
  /* 세션 복구 때는 아직 view.storeKey 가 없을 수 있어(주소 적용 전) 매장을 직접 돌며 잠시 storeKey 를 바꿉니다 — reflowTentatives 가 store() 를 쓰므로 */
  var prev = view.storeKey, today = todayStr(), changed = false;
  Object.keys(DEFAULT_DATA).forEach(function(k){
    if(!DEFAULT_DATA[k].enabled || !DATA || !DATA[k]) return;
    view.storeKey = k;
    var s = DATA[k], dates = {};
    s.reservations.forEach(function(r){ if(r.date >= today && !r.roomId && holdsSeat(r)) dates[r.date] = 1; });
    Object.keys(dates).forEach(function(d){
      var before = s.reservations.filter(function(r){ return r.date === d && !r.roomId; }).map(function(r){ return r.id + ":" + (r.tentativeRoomId || ""); }).join(",");
      reflowTentatives(d);
      var after = s.reservations.filter(function(r){ return r.date === d && !r.roomId; }).map(function(r){ return r.id + ":" + (r.tentativeRoomId || ""); }).join(",");
      if(before !== after) changed = true;
    });
  });
  view.storeKey = prev;
  /* 저장하지 않습니다. 잠정 배정은 겹침으로 정해지는 '계산값' 이라 각 기기가 같은 규칙으로 같은 답을 내고,
     저장하면 두 기기가 서로를 '먼저 수정한 기기' 로 보아 아무것도 안 했는데 충돌 알림이 떴습니다(7차 점검).
     이 기기에서 실제로 예약을 고칠 때(saveRes/wzSubmit 의 reflowTentatives) 함께 올라갑니다 */
  if(changed) syncMarkTentatives();
}
/* 재계산으로 바뀐 잠정 배정을 '이미 동기화된 것' 으로 표시해 flush 가 보내지 않게 합니다 */
function syncMarkTentatives(){
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var st = DATA[k]; if(!st) return;
    (st.reservations || []).forEach(function(r){
      if(r.roomId || !SYNC.res[r.id]) return;
      try{ var was = JSON.parse(SYNC.res[r.id]); if(was.tentativeRoomId !== r.tentativeRoomId || JSON.stringify(was.tentativeExtra||[]) !== JSON.stringify(r.tentativeExtra||[]) || !!was.tentativeSplit !== !!r.tentativeSplit){ was.tentativeRoomId = r.tentativeRoomId; was.tentativeExtra = r.tentativeExtra || []; was.tentativeSplit = !!r.tentativeSplit; SYNC.res[r.id] = JSON.stringify(Object.assign({}, r, {updatedAt: was.updatedAt})); r.updatedAt = was.updatedAt; } }catch(e){}
    });
  });
}
/* 1분 갱신 — 전체가 아니라 바뀐 행만 (updated_at=gt.마지막으로 본 최대값).
   이 기기에서 고쳐 놓고 아직 못 보낸(dirty) 예약은 덮지 않습니다 — 다음 flush 의 조건부 PATCH 가 0행이 되어 충돌 절차로 갑니다 */
async function reloadFromStore(){
  if(!supaOn()) return;
  if(view.display && !SESSION){ await loadPublic(); return; }
  if(!SESSION) return;
  if(OFFLINE){ await reconnect(); return; }
  var keys = Object.keys(DEFAULT_DATA), i, k, changed = false;
  var stores = await sb("/rest/v1/stores?select=key,name,settings,snapshots,updated_at");
  for(i = 0; i < keys.length; i++){
    k = keys[i]; if(!DEFAULT_DATA[k].enabled || !DATA[k]) continue;
    var st = DATA[k];
    /* 설정·스냅샷 — 다른 기기가 바꿨고 이 기기는 안 건드렸으면 받아들임 */
    var srow = stores.find(function(r){ return r.key === k; });
    if(srow && srow.updated_at !== SYNC.storeUpd[k]){
      if(JSON.stringify(st.settings) === SYNC.settings[k]){ var mg = {}; mg[k] = { settings: srow.settings || {} }; st.settings = migrate(mg)[k].settings; SYNC.settings[k] = JSON.stringify(st.settings); changed = true; }
      if(JSON.stringify(st.snapshots || {}) === SYNC.snapshots[k]){ st.snapshots = srow.snapshots || {}; SYNC.snapshots[k] = JSON.stringify(st.snapshots); }
      SYNC.storeUpd[k] = srow.updated_at;
      if(view.draft && view.tab === "settings" && !settingsDirty()) view.draft = deepClone(st.settings);
    }
    /* 예약 델타 */
    var since = SYNC.lastUpd[k] || "";
    var q = "/rest/v1/reservations?store=eq." + k + "&select=*&order=updated_at" + (since ? "&updated_at=gt." + encodeURIComponent(since) : "");
    var rows = await sb(q);
    rows.forEach(function(row){
      var rec = rowToRes(row), id = row.id;
      var li = st.reservations.findIndex(function(r){ return r.id === id; }), ti = st.trash.findIndex(function(r){ return r.id === id; });
      var local = li >= 0 ? st.reservations[li] : (ti >= 0 ? st.trash[ti] : null);
      if(row.updated_at > (SYNC.lastUpd[k] || "")) SYNC.lastUpd[k] = row.updated_at;
      if(local && SYNC.res[id] && JSON.stringify(local) !== SYNC.res[id]) return;   /* 이 기기에서 고친 것 — 덮지 않음 */
      if(li >= 0) st.reservations.splice(li, 1);
      if(ti >= 0) st.trash.splice(ti, 1);
      if(row.deleted_at) st.trash.push(rec); else st.reservations.push(rec);
      SYNC.res[id] = JSON.stringify(rec);
      changed = true;
    });
    if(changed) st.reservations.sort(function(a, b){ return (a.date + a.time).localeCompare(b.date + b.time); });
  }
  if(changed){ cacheSave(); reflowFuture(); }
  return changed;
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
/* 전체화면 — 기본 켬(설정 → 화면 크기에서 끌 수 있음). 안드로이드 크롬·PC 에서만 됨. 아이폰·아이패드는 '홈 화면에 추가' 로 */
function tryFullscreen(){
  try{
    var ui = DATA && DATA._ui; if(ui && ui.fullscreen === false) return;
    var el = document.documentElement;
    if(document.fullscreenElement || !el.requestFullscreen) return;
    el.requestFullscreen().catch(function(){});
  }catch(e){}
}
/* 비상 예약지를 새 탭에 — 새 탭이 열리면 전체화면이 풀리므로, 전체화면이었다면 돌아와서 다시 켤 버튼을 띄웁니다(재아).
   전체화면은 손짓이 있어야 켜져서 팝업 버튼을 누르는 순간에 요청합니다 */
async function openSlip(){
  var wasFs = !!document.fullscreenElement;
  window.open((location.pathname.indexOf('/dev/') >= 0 ? '../' : '') + '비상예약지.html', '_blank', 'noopener');
  if(!wasFs) return;
  if(await uiConfirm("비상 예약지를 새 탭에 열었습니다", "새 탭이 열리면서 전체화면이 풀립니다.\n인쇄하고 돌아오면 아래 버튼으로 다시 켜세요.", {ok:"다시 전체화면", cancel:"그냥 두기", tone:"ok"})) tryFullscreenForce();
}
function toggleFullscreen(){
  try{
    if(document.fullscreenElement){ if(document.exitFullscreen) document.exitFullscreen().catch(function(){}); }
    else if(document.documentElement.requestFullscreen) document.documentElement.requestFullscreen().catch(function(){});
  }catch(e){}
  setTimeout(render, 300);
}
function setFullscreenAuto(on){ if(DATA && DATA._ui){ DATA._ui.fullscreen = !!on; uiSave(); } if(!on && document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(function(){}); if(on) tryFullscreen(); render(); }
function uiSave(){ try{ if(DATA && DATA._ui) localStorage.setItem(UI_KEY, JSON.stringify(DATA._ui)); }catch(e){} }
/* 오프라인에서 PIN 을 맞춰 볼 수단 — 마지막으로 서버가 받아 준 PIN 의 해시(djb2). 4자리 PIN 은 원래 약하니 이 정도로 */
function strHash(str){ var h = 5381, i; for(i = 0; i < str.length; i++) h = ((h << 5) + h + str.charCodeAt(i)) | 0; return String(h); }
function pinHashSave(pin){ try{ localStorage.setItem(PINH_KEY, strHash(pin + "|" + SUPA_CFG.url)); }catch(e){} }
function pinHashOk(pin){ try{ return localStorage.getItem(PINH_KEY) === strHash(pin + "|" + SUPA_CFG.url); }catch(e){ return false; } }
/* 서버를 못 읽을 때 캐시로 들어갑니다(읽기 전용). 캐시가 없으면 false */
/* 아직 서버에 못 보낸 변경이 있는지 — 오프라인 전환·잠금 전에 봅니다 */
function hasDirty(){
  if(!DATA || !SYNC || !SYNC.res) return false;
  var k, dirty = false;
  for(k in DEFAULT_DATA){
    var st = DATA[k]; if(!st || !DEFAULT_DATA[k].enabled) continue;
    if(JSON.stringify(st.settings) !== SYNC.settings[k]) dirty = true;
    (st.reservations || []).concat(st.trash || []).forEach(function(r){ if(JSON.stringify(r) !== SYNC.res[r.id]) dirty = true; });
  }
  return dirty;
}
function enterOffline(pin){
  var c = cacheLoad();
  if(!c || !c.data) return false;
  if(AUTHED && hasDirty()){
    /* 보던 중 끊겼는데 못 보낸 변경이 있으면 지금 DATA 를 그대로 둡니다(캐시로 바꾸면 그 변경이 사라짐 — 점검 D3).
       읽기 전용으로만 잠그고, 다시 연결되면 reconnect 가 flush 부터 합니다 */
    DATA._readonly = true; READONLY_WHY = "offline";
    OFFLINE = { at: c.at, pin: pin || (OFFLINE && OFFLINE.pin) || "", keep: true };
    return true;
  }
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
    if(OFFLINE.keep){
      /* 못 보낸 변경을 들고 있던 경우 — 먼저 보내고 나서 서버 것을 다시 읽습니다 */
      var was = OFFLINE; OFFLINE = null; DATA._readonly = false; READONLY_WHY = "";
      try{ await flush(); }catch(e){}
      if(SAVE_FAIL){ OFFLINE = was; DATA._readonly = true; READONLY_WHY = "offline"; return; }
    }
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
      d[k].reservations.push({ id: k + "-" + r.time + "-" + r.name, date: today, time: r.time, name: r.name, people: r.people, roomId: r.room_id, seatPref: r.seat_pref || null, status: r.status, masked: true });
    });
  });
  if(AUTHED) return;   /* 기다리는 사이 PIN 으로 들어왔으면 공개 데이터로 덮지 않습니다(점검 D5) */
  var ui = DATA && DATA._ui;
  DATA = migrate(d); DATA._ui = ui || uiLoad(); DATA._readonly = true; READONLY_WHY = "public";
  try{ localStorage.setItem(SCREEN_KEY, JSON.stringify({ at:new Date().toISOString(), data:d })); }catch(e){}
}
var SCREEN_KEY = "hanok.screen.v1";
/* 켤 때 서버를 못 읽으면 마지막으로 성공한 화면(캐시)으로 시작합니다 — TV 는 방치용이라 빈 화면보다 어제 목록이 낫습니다.
   1분 갱신이 이어서 시도하고, 성공하면 자연히 새 데이터로 바뀝니다. 캐시도 없으면 그대로 던집니다(빈 화면 + 띠) */
async function loadPublicOrCache(){
  try{ await loadPublic(); }
  catch(e){
    var c = null; try{ c = JSON.parse(localStorage.getItem(SCREEN_KEY) || "null"); }catch(e2){}
    if(!c || !c.data) throw e;
    if(!c.at || todayStr(new Date(c.at)) !== todayStr()){ Object.keys(c.data).forEach(function(k){ c.data[k].reservations = []; }); }   /* 날짜가 지난 캐시 — 좌석 설정만 쓰고 예약은 비움 */
    var ui = DATA && DATA._ui;
    DATA = migrate(deepClone(c.data)); DATA._ui = ui || uiLoad(); DATA._readonly = true; READONLY_WHY = "public";
    DISP_FAIL = Math.max(DISP_FAIL, 1);
    console.warn("공개 뷰 실패 — 캐시(" + c.at + ")로 시작", e.message);
  }
}

/* 쓰기가 막혀 있으면 이유를 알리고 true. 막지 않는 것이 원칙이지만 이 경우는 진짜로 저장이 불가능합니다 */
function readonlyBlock(){
  if(!DATA || !DATA._readonly) return false;
  var why = READONLY_WHY === "offline" ? "서버와 연결이 끊겨 지금은 볼 수만 있습니다. 종이에 적어 두세요 — 연결되면 다시 시도하세요."
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
      try{
        /* 밤새 켜 둔 태블릿을 새로고침하면 토큰이 만료돼 "JWT expired" 로 멈췄습니다 — 만료(임박)면 먼저 갱신(점검 D9) */
        if(SESSION.expires_at - Date.now()/1000 < 300){ try{ await sbRefresh(); }catch(e){ if(!e.network) throw e; } }
        await enterStore();
      }
      catch(e){
        console.error("불러오기 실패", e);
        if(e.network){ if(!enterOffline()) LOAD_ERROR = e.message; }
        else { sessionClear(); LOAD_ERROR = e.message; }
      }
    }
    if(!AUTHED) loadPublicOrCache().then(function(){ render(); }).catch(function(e){ console.warn("공개 뷰 실패", e.message); });
  }else
  /* 저장소가 아예 없으면(개발 중 · 파일로 열었을 때) 예시 데이터로 돕니다.
     저장소가 있는데 실패했으면 **절대 예시 데이터를 만들지 않습니다.**
     예전엔 실패하면 무조건 예시 1,300건을 만들었는데, DB 를 붙인 뒤 인터넷이 잠깐 끊기면
     그 가짜가 진짜 DB 에 저장되는 사고가 납니다. 실패하면 빈 상태로 멈추고 알립니다. */
  if(!window.storage || typeof window.storage.get !== "function"){
    DATA = seedDemo(deepClone(DEFAULT_DATA));
  }else{
    try{
      const r = await window.storage.get(STORAGE_KEY);
      DATA = r ? migrate(JSON.parse(r.value)) : migrate(deepClone(DEFAULT_DATA));
    }catch(e){
      console.error("불러오기 실패", e);
      LOAD_ERROR = String(e && e.message ? e.message : e);
      DATA = migrate(deepClone(DEFAULT_DATA));
      DATA._readonly = true;      /* 저장을 막습니다 — 빈 상태를 덮어쓰면 안 됩니다 */
    }
  }
  if(!DATA._ui) DATA._ui = {theme:"hanok"};
  if(!DATA._logs) DATA._logs = [];
  /* 새로고침해도 잠기지 않도록 인증 상태를 저장해 둡니다.
     자동 로그아웃은 없고, '지금 잠그기'를 눌러야 풀립니다. */
  if(!supaOn() && DATA._session && DATA._session.authed) AUTHED = true;
  document.getElementById("app").setAttribute("data-ok","1");
  autoCloseDays();
  takeSnapshot();
  /* 재안내 시각이 지난 예약을 '보냄'으로 바꿉니다.
     실제 서비스라면 서버가 시간 맞춰 보낼 일이지만, 지금은 화면이 켜져 있을 때만 돕니다.
     그래서 1분마다 한 번 더 확인합니다 — 저녁 5시에 화면을 켜 두면 그때 처리됩니다. */
  smsTick();
  setInterval(function(){ if(smsTick()) render(); }, 60000);
  if(applyRoute()){
    document.addEventListener("keydown", escDisplay);
  }else{
    applyAdminRoute();   /* #/hanok/settings 처럼 관리 화면 주소로 들어온 경우 */
  }
  render();
  /* 뒤로 가기·주소 변경에도 반응 */
  window.addEventListener("hashchange", ()=>{ if(applyRoute() || applyAdminRoute()) render(); });
}
/* ---------- 8차 좌석 마이그레이션 ----------
   옛 '홀'(type:hall, zones) 은 테이블 개별 목록으로 바꿉니다. 홀에 배정돼 있던 예약은 테이블을 특정할 수 없으니
   미배정(seatPref "table-any") 으로 두고 잠정 배정을 다시 계산합니다. 실서비스에는 옛 데이터가 없어 dev 더미에만 해당 */
var MIGRATED_RES = {};   /* 이번 불러오기에서 모양을 고친 예약 id — syncMark 가 '아직 안 올라간 것' 으로 표시해 서버에도 반영되게 */
function migrateSeats(d){
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var st = d[k] && d[k].settings; if(!st) return;
    var def = DEFAULT_DATA[k].settings;
    var rooms = st.rooms || [];
    var halls = rooms.filter(function(x){ return x.type === "hall"; });
    var hallIds = halls.map(function(x){ return x.id; });
    if(halls.length){
      st.rooms = rooms.filter(function(x){ return x.type !== "hall"; }).concat(deepClone((def.rooms||[]).filter(function(x){ return x.type === "table"; })));
    }
    /* 예약 쪽은 설정과 따로 봅니다 — 설정이 먼저 새 모양으로 저장된 뒤에도 옛 홀 배정(h1 등)이 남은 예약이 서버에 있을 수 있습니다 */
    var known = {}; (st.rooms||[]).forEach(function(x){ known[x.id] = 1; });
    var legacy = function(id){ return id && !known[id] && (hallIds.indexOf(id) >= 0 || /^h\d+$/.test(id)); };
    (d[k].reservations||[]).concat(d[k].trash||[]).forEach(function(r){
      var before = JSON.stringify(r);
      if(legacy(r.roomId)){ r.roomId = null; r.seatPref = "table-any"; r.legacyHall = true; }
      if(legacy(r.tentativeRoomId)){ r.tentativeRoomId = null; r.tentativeExtra = []; }
      if(r.seatPref === "hall-any") r.seatPref = "table-any";
      if(JSON.stringify(r) !== before) MIGRATED_RES[r.id] = 1;
    });
    /* 룸 정원이 옛 기본값(조조 4 등)이면 누님 답으로 교체 — 이름이 같은 룸만 */
    (st.rooms||[]).forEach(function(x){
      if(x.type !== "room") return;
      var dr = (def.rooms||[]).find(function(y){ return y.type === "room" && y.name === x.name; });
      if(dr && !x.tuned){ x.minCapacity = dr.minCapacity; x.minWeekend = dr.minWeekend; x.optCapacity = dr.optCapacity; x.capacity = dr.capacity; x.floor = dr.floor; }   /* 8차-L: 평일/주말 최소·최적도 기본표에서 */
    });
    /* 8차-L: 룸 최소를 평일/주말로 나눔. 옛 저장본은 '최소=최적' 하나뿐이라 임의로 나눕니다(누님 질문 목록) */
    (st.rooms || []).forEach(function(r){
      if(!isRoom(r) || r.optCapacity != null) return;
      var opt = r.minCapacity != null ? r.minCapacity : Math.max(2, (r.capacity||2) - 2);
      r.optCapacity = opt; r.minWeekend = opt; r.minCapacity = Math.max(2, opt - 2);
    });
    if(!st.joins) st.joins = deepClone(def.joins || []);
    st.joins.forEach(function(j){ if(j.split == null && /원탁|나뉨/.test(j.note || "")) j.split = true; });
    if(!st.holidaysOff) st.holidaysOff = [];
    /* 1년 넘게 지난 임시 일정·추가/제외 공휴일·사용 중지는 정리 — 무한히 쌓여 설정 JSON 이 커지는 것을 막습니다(점검 C5) */
    var cut = shiftDate(todayStr(), -366);
    if(st.overrides) st.overrides = st.overrides.filter(function(o){ return !o.date || o.date >= cut; });
    st.holidays = (st.holidays || []).filter(function(d){ return d >= cut; });
    st.holidaysOff = st.holidaysOff.filter(function(d){ return d >= cut; });
    (st.rooms || []).forEach(function(r){ if(r.blocks) r.blocks = r.blocks.filter(function(b){ return !b.to || b.to >= cut; }); });
    /* 옛 기본 경로 3개 → 새 기본 4개 (사장님이 손댄 목록이면 그대로) */
    if(JSON.stringify(st.sources) === JSON.stringify(["전화 예약","네이버 예약","기타"]) || JSON.stringify(st.sources) === JSON.stringify(["네이버 예약","전화 예약","방문","기타"])) st.sources = def.sources.slice();   /* 순서: 전화·네이버·방문·기타(재아) */
    /* 운영시간에 세션이 없으면 요일별 기본 세션을 붙입니다 */
    (st.schedules||[]).forEach(function(sch){
      /* 세션이 없는 옛 운영시간표는 8차 기본표(누님 확인본: 일 라스트오더 19:40, 공휴일=일요일, 토요일 브레이크 없음)로 통째 바꿉니다.
         아직 실서비스 전이라 사장님이 직접 고친 시간표는 없습니다 */
      (sch.days||[]).forEach(function(day, i){ if(!day.sess && !day.sessions && def.schedules[0].days[i]) sch.days[i] = deepClone(def.schedules[0].days[i]); });
      if(!sch.holiday || (!sch.holiday.sess && !sch.holiday.sessions)) sch.holiday = deepClone(def.schedules[0].holiday);
      /* 8차-X: 자유 세션 목록(sessions[]) → 점심 경계 + 점심/저녁(sess{}) */
      (sch.days||[]).concat([sch.holiday]).forEach(function(day){ if(day) ensureSess(day); });
    });
  });
}
/* 저장된 옛 데이터에 새 항목이 없을 때 채워 넣기 */
function migrate(d){
  delete d._auth;   /* 7차: PIN 은 서버(Supabase 계정)에만. 옛 저장본에 평문으로 남아 있던 것을 지웁니다 */
  d._logs = d._logs || [];
  migrateSeats(d);   /* 8차: 홀(zones) → 테이블 개별, 세션, 경로, 합침 */
  /* tvType(목록형/좌석표)은 기기 설정(_ui)에 있었는데 TV 가 공개 뷰로 읽으려면 매장 설정이어야 합니다 → settings.tvType (7차) */
  if(d._ui && d._ui.tvType && d.hanok && d.hanok.settings && !d.hanok.settings.tvType) d.hanok.settings.tvType = d._ui.tvType;
  for(const k of Object.keys(DEFAULT_DATA)){
    d[k] = { ...deepClone(DEFAULT_DATA[k]), ...(d[k]||{}) };
    d[k].settings = { ...DEFAULT_DATA[k].settings, ...(d[k].settings||{}) };
    for(const arr of ["reservations","staff","attendance","sales","trash"]) d[k][arr] = d[k][arr] || [];
    d[k].snapshots = d[k].snapshots || {};   /* 날짜별 좌석 수 (takeSnapshot 참고) */
    /* 옛 기록에 deletedAt 이 붙은 채 reservations 에 남아 있으면 trash 로 옮깁니다 */
    d[k].trash = d[k].trash.concat(d[k].reservations.filter(r=>r.deletedAt));
    d[k].reservations = d[k].reservations.filter(r=>!r.deletedAt);
    /* 옛 기록 정리: 인원을 유아 포함 총원으로, 상태 이름 변경 */
    d[k].reservations = d[k].reservations.map(r=>({
      ...r,
      people: r.people != null ? r.people : pplOf(r),
      chairs: r.chairs != null ? r.chairs : (r.infants||0),
      status: (r.status==="완료"||r.status==="식사완료") ? "방문" : r.status,
      sms: r.sms || [],       /* 보낸 문자 기록 (흉내) */
      /* 경로 이름을 풀네임으로 통일 ("전화" → "전화 예약") */
      source: r.source==="전화" ? "전화 예약" : (r.source==="네이버예약" ? "네이버 예약" : r.source)
    }));
    /* 코스 묶음에 고정 id 를 붙이고, 예약의 코스 키를 '순서 번호|이름' → 'id|이름' 으로 옮깁니다.
       순서 번호는 설정에서 행을 바꾸는 순간 과거 예약이 전부 틀어지는 구조였습니다.
       ※ 옛 키의 번호는 '그 시점의 순서' 이므로, 지금 순서 기준으로 한 번만 옮깁니다. */
    (function(){
      var gs = d[k].settings.courseGroups || [];
      var i, defaults = ["cg_dinner","cg_wdlunch","cg_welunch"];
      for(i = 0; i < gs.length; i++) if(!gs[i].id) gs[i].id = defaults[i] || newId("cg");
      var fix = function(courses){
        if(!courses) return courses;
        var out = {}, key, seg, g;
        for(key in courses){
          seg = key.split("|");
          if(/^\d+$/.test(seg[0])){ g = gs[+seg[0]]; out[(g ? g.id : seg[0]) + "|" + seg[1]] = courses[key]; }
          else out[key] = courses[key];
        }
        return out;
      };
      d[k].reservations.forEach(function(r){ r.courses = fix(r.courses); });
      (d[k].trash || []).forEach(function(r){ r.courses = fix(r.courses); });
    })();
    /* 문자 설정이 없던 기록에도 기본값을 채웁니다 */
    d[k].settings.sms = { ...SMS_DEFAULT, ...(d[k].settings.sms||{}) };
    d[k].settings.sources = (d[k].settings.sources||[]).map(function(x){
      return x==="전화" ? "전화 예약" : (x==="네이버예약" ? "네이버 예약" : x);
    });
    /* 옛 '사용 중지'(켜짐/꺼짐 하나)를 기간제로 옮깁니다.
       끝나는 날을 모르는 상태였으므로 '해제할 때까지'로 봅니다. */
    d[k].settings.rooms = (d[k].settings.rooms||[]).map(function(r){
      var out = {...r};
      if(!out.blocks) out.blocks = [];
      if(out.blocked){
        out.blocks = out.blocks.concat([{
          id:"blk_"+out.id, from:todayStr(), to:"", fromTime:"", toTime:"",
          openEnded:true, note:out.blockNote||""
        }]);
      }
      delete out.blocked; delete out.blockNote;
      return out;
    });
  }
  return d;
}
async function saveData(){
  uiSave();                            /* 테마·배율·tvType 폴백은 기기별 — 서버와 무관하게 늘 저장 */
  if(DATA && DATA._readonly) return;   /* 불러오기 실패 · 오프라인 — 덮어쓰지 않습니다 */
  if(supaOn()) return flush();         /* 서버 모드: 바뀐 것만 보냅니다 */
  try{ await window.storage.set(STORAGE_KEY, JSON.stringify(DATA)); }
  catch(e){ console.error("저장 실패", e); }
}
/* ---------- flush — 바뀐 것만 서버로 ----------
   saveData() 를 부르는 곳이 40여 곳이라 호출부는 그대로 두고, 여기서 마지막 동기화(SYNC)와 지금 JSON 을 비교합니다.
   예약 수백 건 stringify 는 밀리초 단위. 실패하면 dirty 는 메모리에 남아 '다시 시도' 로 다시 보냅니다(오프라인 쓰기 큐는 안 만듦 — 결정) */
var FLUSHING = false, FLUSH_AGAIN = false, SAVE_FAIL = null;
var CLOCK_SKEW = 0;   /* 서버 시각 − 기기 시각(ms). 하루 이상 어긋나면 자동 방문 처리·스냅샷을 건너뜁니다 */
function clockBad(){ return Math.abs(CLOCK_SKEW) > 12 * 3600 * 1000; }
async function flush(){
  if(!SESSION || OFFLINE) return;
  if(FLUSHING){ FLUSH_AGAIN = true; return; }
  FLUSHING = true;
  try{
    var keys = Object.keys(DEFAULT_DATA), i, k;
    for(i = 0; i < keys.length; i++){
      k = keys[i]; var st = DATA[k]; if(!st || !DEFAULT_DATA[k].enabled) continue;
      /* 설정·스냅샷 — 사장 한 사람이 가끔 고치므로 조건 없이 (마지막 저장이 이김) */
      var sj = JSON.stringify(st.settings), pj = JSON.stringify(st.snapshots || {});
      if(sj !== SYNC.settings[k] || pj !== SYNC.snapshots[k]){
        var body = {}; if(sj !== SYNC.settings[k]) body.settings = st.settings; if(pj !== SYNC.snapshots[k]) body.snapshots = st.snapshots || {};
        var srows = await sb("/rest/v1/stores?key=eq." + k, { method:"PATCH", body:body, prefer:"return=representation" });
        SYNC.settings[k] = sj; SYNC.snapshots[k] = pj; if(srows && srows[0]) SYNC.storeUpd[k] = srows[0].updated_at;
      }
      /* 예약 — 살아 있는 것 + 휴지통(soft delete 는 deleted_at PATCH) */
      var all = (st.reservations || []).concat(st.trash || []), j;
      var firstErr = null;
      for(j = 0; j < all.length; j++){
        var rec = all[j], cur = JSON.stringify(rec);
        if(cur === SYNC.res[rec.id]) continue;
        /* 한 건이 실패해도 나머지는 보냅니다. 연결 자체가 없으면(network) 바로 멈춥니다 — 나머지도 다 실패할 테니 */
        try{
          if(!SYNC.res[rec.id]) await pushNew(rec, k);
          else await pushChanged(rec, k, cur);
        }catch(e){ if(e.network) throw e; if(!firstErr) firstErr = e; console.error("저장 실패", rec.id, e.message); }
      }
      if(firstErr) throw firstErr;
    }
    if(SAVE_FAIL){ SAVE_FAIL = null; saveFailBand(); }
    cacheSave();
  }catch(e){
    console.error("저장 실패", e.message);
    SAVE_FAIL = { msg: e.message, at: Date.now() }; saveFailBand();
  }
  FLUSHING = false;
  if(FLUSH_AGAIN){ FLUSH_AGAIN = false; return flush(); }
}
/* 보낸 뒤 처리. sent = 보낼 때의 JSON — 요청이 오가는 사이에 객체가 또 바뀌었을 수 있습니다
   (등록 직후 reflowTentatives 가 잠정 배정을 바꾸는 것이 실제 사례). 그러면 '보낸 것' 만 동기화된 것으로 적고 한 번 더 보냅니다 */
function markSynced(rec, row, sent){
  if(row && row.updated_at) rec.updatedAt = row.updated_at;   /* 서버 시각 문자열 그대로 */
  var synced = JSON.parse(sent); synced.updatedAt = rec.updatedAt;
  SYNC.res[rec.id] = JSON.stringify(synced);
  if(JSON.stringify(rec) !== SYNC.res[rec.id]) FLUSH_AGAIN = true;
  var k; for(k in DEFAULT_DATA) if(DATA[k] && ((DATA[k].reservations||[]).indexOf(rec) >= 0 || (DATA[k].trash||[]).indexOf(rec) >= 0)){
    if(row && row.updated_at > (SYNC.lastUpd[k] || "")) SYNC.lastUpd[k] = row.updated_at;
  }
}
async function pushNew(rec, k){
  var sent = JSON.stringify(rec);
  try{
    var rows = await sb("/rest/v1/reservations", { method:"POST", body:resToRow(rec, k), prefer:"return=representation" });
    markSynced(rec, rows && rows[0], sent);
  }catch(e){
    /* 409 = 서버에는 이미 들어갔는데 응답이 유실된 경우(통신 끊김). 다시 POST 하면 영원히 409 라 PATCH 로 갈아탑니다(점검 D2) */
    if(e.status !== 409) throw e;
    SYNC.res[rec.id] = JSON.stringify(Object.assign({}, rec, {_lost:1}));   /* '본 적 있음' 으로 — 조건(updated_at) 없이 PATCH */
    await pushChanged(rec, k, sent);
  }
}
/* 조건부 PATCH — 내가 마지막으로 본 updated_at 과 같을 때만. 0행이면 누가 먼저 고친 것 → 충돌 절차 */
async function pushChanged(rec, k, cur){
  var seen = "";
  try{ seen = JSON.parse(SYNC.res[rec.id]).updatedAt || ""; }catch(e){}
  var row = resToRow(rec, k); delete row.id; delete row.store;
  var q = "/rest/v1/reservations?id=eq." + rec.id + (seen ? "&updated_at=eq." + encodeURIComponent(seen) : "");
  var rows = await sb(q, { method:"PATCH", body:row, prefer:"return=representation" });
  if(rows && rows.length){ markSynced(rec, rows[0], cur); return; }
  /* 충돌 */
  var theirs = await sb("/rest/v1/reservations?id=eq." + rec.id + "&select=*");
  var t = theirs && theirs[0];
  if(!t){ await pushNew(rec, k); return; }   /* 서버에 아예 없음(백업 복구 등) — 새로 넣습니다 */
  var trec = rowToRes(t);
  if(!trec){ await pushNew(rec, k); return; }   /* 서버 행이 깨져 있으면 내 것으로 덮습니다 */
  var st = DATA[k];
  /* 내용이 같으면(시각만 다름) 묻지 않고 상대 것을 받습니다.
     두 기기가 같은 결론에 도달하는 경우가 실제로 잦습니다 — 아침에 둘 다 켜서 autoCloseDays 가 같은 예약을 '방문' 으로 바꾸거나,
     각자 저장한 뒤 reflowTentatives 가 같은 잠정 배정을 계산하거나. 이걸 매번 물으면 확인창이 수십 개 뜹니다 */
  var mineNoTs = Object.assign({}, rec), theirsNoTs = Object.assign({}, trec); delete mineNoTs.updatedAt; delete theirsNoTs.updatedAt;
  if(canon(mineNoTs) === canon(theirsNoTs)){   /* 키 순서가 달라도(내 객체 vs 서버에서 온 객체) 같은 내용이면 같게 */
    rec.updatedAt = trec.updatedAt; SYNC.res[rec.id] = JSON.stringify(rec);
    if(t.updated_at > (SYNC.lastUpd[k] || "")) SYNC.lastUpd[k] = t.updated_at;
    return;
  }
  /* 선택지를 주지 않습니다(재아 결정) — 서버 내용으로 화면을 바꾸고 다시 하라고 알립니다. 다시 하면 그때는 충돌이 아닙니다 */
  var title = t.deleted_at ? "다른 기기에서 이미 삭제된 예약입니다" : "작성 도중 다른 기기에서 수정된 내용입니다";
  var li = st.reservations.indexOf(rec), ti = st.trash.indexOf(rec);
  if(li >= 0) st.reservations.splice(li, 1); if(ti >= 0) st.trash.splice(ti, 1);
  if(t.deleted_at) st.trash.push(trec); else st.reservations.push(trec);
  st.reservations.sort(function(a, b){ return (a.date + a.time).localeCompare(b.date + b.time); });
  SYNC.res[rec.id] = JSON.stringify(trec); if(t.updated_at > (SYNC.lastUpd[k] || "")) SYNC.lastUpd[k] = t.updated_at;
  render();
  await uiAlert(title, conflictSummary(rec, trec) + "\n\n내 변경은 저장되지 않았고 화면을 최신 내용으로 바꿨습니다. 다시 수정해 주세요.", "warn");
}
/* 키 순서에 상관없는 JSON — 같은 내용인지 비교할 때 */
function canon(o){
  if(o === null || typeof o !== "object") return JSON.stringify(o);
  if(Array.isArray(o)) return "[" + o.map(canon).join(",") + "]";
  return "{" + Object.keys(o).filter(function(k){ return o[k] !== undefined; }).sort()
                 .map(function(k){ return JSON.stringify(k) + ":" + canon(o[k]); }).join(",") + "}";
}
/* 상대 버전 요약 — 시각·인원·좌석·상태 중 다른 것만 '18:00 → 18:30' 식으로 */
function conflictSummary(mine, theirs){
  var out = [], f = [["date","날짜"],["time","시각"],["people","인원"],["roomId","좌석"],["status","상태"],["name","이름"],["phone","전화"],["memo","메모"],["request","요청"],["allergy","알러지"],["menuType","식사"]], i;
  for(i = 0; i < f.length; i++){
    var key = f[i][0], a = mine[key], b = theirs[key];
    if(key === "roomId"){ a = a ? seatLabel(a) : "미배정"; b = b ? seatLabel(b) : "미배정"; }
    if(String(a == null ? "" : a) !== String(b == null ? "" : b)) out.push(f[i][1] + ": " + (a == null ? "-" : a) + " → " + (b == null ? "-" : b));
  }
  if(theirs.deletedAt) out.push("상대 기기에서 삭제됨");
  return out.length ? "내가 입력한 것 → 지금 저장된 것:\n" + out.join("\n") : "다른 기기가 나중에 저장했습니다.";
}
/* 저장 실패 띠 — body 에 직접 붙입니다(입력 중 시트를 다시 그리지 않으려고). 다시 시도는 flush */
function saveFailBand(){
  var el = document.getElementById("savefail");
  if(!SAVE_FAIL){ if(el) el.parentNode.removeChild(el); return; }
  if(!el){ el = document.createElement("div"); el.id = "savefail"; el.className = "crashbar savefail"; document.body.appendChild(el); }
  el.innerHTML = '<b>저장 안 됨</b><span>' + esc(SAVE_FAIL.msg) + ' · 지금 화면의 변경은 저장되지 않았습니다. <b>탭을 닫으면 사라집니다.</b></span>' +
                 '<button onclick="flush()">다시 시도</button>';
}
