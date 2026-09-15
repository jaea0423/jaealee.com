# -*- coding: utf-8 -*-
"""v6 8차-F(1) — 점검 결함 수정 묶음 1: 사장님이 하루 안에 겪을 것
   D1 시트 저장이 임시본에도 반영 · D2 POST 409 → PATCH 경로 · D3 오프라인 전환 때 dirty 보존 · D5 늦은 공개 뷰 응답이 인증 DATA 덮음
   D6 fetch 15초 타임아웃 · D7 sessionTick 5xx/429 는 잠그지 않음 · D8 잠금 전 flush · D9 만료 세션은 갱신 후 진입
   R1 render 전에 마법사·시트 입력 동기화 · U1 TV 에서 숫자키 무시 · C1 oninput → onchange"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- D1: 시트가 live 에 직접 쓰는 것들 → 임시본에도 ----------
s = R(s, """function applySettings(){""", """/* 시트(운영시간·임시일정·노쇼 제외)는 '적용하기' 없이 바로 저장합니다. 그 값을 임시본에도 같이 써 둬야
   나중에 '적용하기' 를 눌렀을 때 옛 임시본이 방금 저장한 것을 되돌리지 않습니다(점검 D1) */
function mirrorDraft(key){ if(view.draft) view.draft[key] = deepClone(store().settings[key]); }
function applySettings(){""")
s = R(s, """  st.overrides = [...(st.overrides||[]).filter(o=>o.date!==d.date), rec];
  logEvent("설정 변경", `임시 일정 ${rec.date} ${rec.closed?"휴무":"시간변경"}`);""",
"""  st.overrides = [...(st.overrides||[]).filter(o=>o.date!==d.date), rec];
  mirrorDraft("overrides");
  logEvent("설정 변경", `임시 일정 ${rec.date} ${rec.closed?"휴무":"시간변경"}`);""")
s = R(s, """  st.overrides = st.overrides.filter(o=>o.date!==date);
  logEvent("설정 변경", `임시 일정 삭제 ${date}`);""",
"""  st.overrides = st.overrides.filter(o=>o.date!==date);
  mirrorDraft("overrides");
  logEvent("설정 변경", `임시 일정 삭제 ${date}`);""")
s = R(s, """  st.noshowExcluded = [...(st.noshowExcluded||[]), key];
  saveData(); render();
}
function restoreNoshow(){ store().settings.noshowExcluded = []; saveData(); render(); }""",
"""  st.noshowExcluded = [...(st.noshowExcluded||[]), key];
  mirrorDraft("noshowExcluded");
  saveData(); render();
}
function restoreNoshow(){ store().settings.noshowExcluded = []; mirrorDraft("noshowExcluded"); saveData(); render(); }""")
s = R(s, """  if(view.draft) view.draft.schedules = deepClone(st.schedules);   /* 임시본에도 — 안 그러면 '적용하기'가 방금 저장한 것을 되돌립니다(점검 D1) */""",
"""  mirrorDraft("schedules");   /* 안 그러면 '적용하기'가 방금 저장한 것을 되돌립니다(점검 D1) */""")
s = R(s, """  st.schedules = st.schedules.filter(s=>s.from!==from);
  if(view.draft) view.draft.schedules = deepClone(st.schedules);""",
"""  st.schedules = st.schedules.filter(s=>s.from!==from);
  mirrorDraft("schedules");""")

# ---------- D2: POST 가 409(이미 있음) 면 PATCH 경로로. 레코드별 try/catch 로 한 건 실패가 나머지를 막지 않게 ----------
s = L.replace_fn(s, "pushNew", """async function pushNew(rec, k){
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
}""")
s = R(s, """      for(j = 0; j < all.length; j++){
        var rec = all[j], cur = JSON.stringify(rec);
        if(cur === SYNC.res[rec.id]) continue;
        if(!SYNC.res[rec.id]) await pushNew(rec, k);
        else await pushChanged(rec, k, cur);
      }
    }
    if(SAVE_FAIL){ SAVE_FAIL = null; saveFailBand(); }
    cacheSave();
  }catch(e){
    console.error("저장 실패", e.message);
    SAVE_FAIL = { msg: e.message, at: Date.now() }; saveFailBand();
  }""",
"""      var firstErr = null;
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
  }""")

# ---------- D3: 오프라인 전환 때 아직 못 보낸 변경이 있으면 DATA 를 캐시로 바꾸지 않음 ----------
s = R(s, """function enterOffline(pin){
  var c = cacheLoad();
  if(!c || !c.data) return false;
  var ui = DATA && DATA._ui;
  DATA = migrate(deepClone(c.data)); DATA._ui = ui || uiLoad(); DATA._logs = DATA._logs || [];
  DATA._readonly = true; READONLY_WHY = "offline";
  OFFLINE = { at: c.at, pin: pin || (OFFLINE && OFFLINE.pin) || "" };""",
"""/* 아직 서버에 못 보낸 변경이 있는지 — 오프라인 전환·잠금 전에 봅니다 */
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
  OFFLINE = { at: c.at, pin: pin || (OFFLINE && OFFLINE.pin) || "" };""")
s = R(s, """    if(!SESSION && OFFLINE.pin) await sbLogin(SUPA_CFG.staffEmail, pinToPassword(OFFLINE.pin));
    if(!SESSION) return;
    await enterStore();
    render();""",
"""    if(!SESSION && OFFLINE.pin) await sbLogin(SUPA_CFG.staffEmail, pinToPassword(OFFLINE.pin));
    if(!SESSION) return;
    if(OFFLINE.keep){
      /* 못 보낸 변경을 들고 있던 경우 — 먼저 보내고 나서 서버 것을 다시 읽습니다 */
      var was = OFFLINE; OFFLINE = null; DATA._readonly = false; READONLY_WHY = "";
      try{ await flush(); }catch(e){}
      if(SAVE_FAIL){ OFFLINE = was; DATA._readonly = true; READONLY_WHY = "offline"; return; }
    }
    await enterStore();
    render();""")

# ---------- D5: 늦게 온 공개 뷰 응답이 로그인한 DATA 를 덮지 않게 ----------
s = R(s, """  var ui = DATA && DATA._ui;
  DATA = migrate(d); DATA._ui = ui || uiLoad(); DATA._readonly = true; READONLY_WHY = "public";
  try{ localStorage.setItem(SCREEN_KEY, JSON.stringify({ at:new Date().toISOString(), data:d })); }catch(e){}""",
"""  if(AUTHED) return;   /* 기다리는 사이 PIN 으로 들어왔으면 공개 데이터로 덮지 않습니다(점검 D5) */
  var ui = DATA && DATA._ui;
  DATA = migrate(d); DATA._ui = ui || uiLoad(); DATA._readonly = true; READONLY_WHY = "public";
  try{ localStorage.setItem(SCREEN_KEY, JSON.stringify({ at:new Date().toISOString(), data:d })); }catch(e){}""")

# ---------- D6: fetch 타임아웃 15초 (half-open 이면 FLUSHING 이 몇 분씩 잠겼음) ----------
s = R(s, """  var res;
  try{
    res = await fetch(SUPA_CFG.url + path, { method: opt.method || "GET", headers: headers,
                                             body: opt.body != null ? JSON.stringify(opt.body) : undefined });
  }catch(e){ var ne = new Error("서버에 연결할 수 없습니다"); ne.network = true; throw ne; }""",
"""  var res, ctl = (typeof AbortController === "function") ? new AbortController() : null;
  var timer = ctl ? setTimeout(function(){ ctl.abort(); }, 15000) : null;   /* 응답이 영영 안 오면(half-open) 15초 뒤 끊습니다 */
  try{
    res = await fetch(SUPA_CFG.url + path, { method: opt.method || "GET", headers: headers,
                                             body: opt.body != null ? JSON.stringify(opt.body) : undefined,
                                             signal: ctl ? ctl.signal : undefined });
  }catch(e){ var ne = new Error("서버에 연결할 수 없습니다"); ne.network = true; throw ne; }
  finally{ if(timer) clearTimeout(timer); }""")

# ---------- D7: 갱신 실패 중 400/401/403 만 잠금 (5xx·429 는 잠시 뒤 다시) ----------
s = R(s, """  try{ await sbRefresh(); }
  catch(e){ if(!e.network){ sessionClear(); AUTHED = false; view.storeKey = null; render(); } }
}""",
"""  try{ await sbRefresh(); }
  catch(e){
    /* 토큰이 정말 거부된 경우(400/401/403)만 잠급니다. 서버 장애(5xx)·과다 요청(429)·연결 없음은 다음 분에 다시 시도 —
       잠그면 재로그인 때 못 보낸 변경이 사라집니다(점검 D7) */
    if(!e.network && e.status && e.status < 500 && e.status !== 429){ sessionClear(); AUTHED = false; view.storeKey = null; render(); }
  }
}""")

# ---------- D8: 잠금·매장 나가기 전에 못 보낸 변경을 보내고, 안 되면 물어봄 ----------
s = R(s, """function lockNow(){
  logEvent("잠금", "");
  AUTHED=false; PIN_BUF=""; PIN_ERR=""; view.storeKey=null;
  DATA._session = {authed:false};
  sessionClear(); OFFLINE = null;
  saveData(); render();
}""",
"""/* 잠그기 전에 못 보낸 변경을 마저 보냅니다. 세션을 먼저 지우면 남은 PATCH 가 anon 으로 나가 401 이 났습니다(점검 D8) */
async function flushBeforeLeave(){
  if(!supaOn() || !SESSION) return true;
  if(FLUSHING || hasDirty()){ try{ await flush(); }catch(e){} }
  if(SAVE_FAIL || hasDirty()){
    return await uiConfirm("아직 서버에 저장되지 않은 변경이 있습니다", "지금 나가면 그 변경은 사라집니다. 그래도 나갈까요?", {ok:"버리고 나가기", cancel:"머무르기"});
  }
  return true;
}
async function lockNow(){
  if(!await flushBeforeLeave()) return;
  logEvent("잠금", "");
  AUTHED=false; PIN_BUF=""; PIN_ERR=""; view.storeKey=null; view.draft=null;
  DATA._session = {authed:false};
  sessionClear(); OFFLINE = null;
  saveData(); render();
}""")
s = R(s, """function goHome(){
  logEvent("잠금", "매장 선택으로");""",
"""async function goHome(){
  if(!await flushBeforeLeave()) return;
  logEvent("잠금", "매장 선택으로");""")

# ---------- D9: 새로고침 복구 때 만료된 세션이면 갱신 후 진입 ----------
s = R(s, """    sessionLoad();
    if(SESSION){
      try{ await enterStore(); }""",
"""    sessionLoad();
    if(SESSION){
      try{
        /* 밤새 켜 둔 태블릿을 새로고침하면 토큰이 만료돼 "JWT expired" 로 멈췄습니다 — 만료(임박)면 먼저 갱신(점검 D9) */
        if(SESSION.expires_at - Date.now()/1000 < 300){ try{ await sbRefresh(); }catch(e){ if(!e.network) throw e; } }
        await enterStore();
      }""")

# ---------- R1: render 전에 입력칸 값을 상태로 ----------
s = R(s, """function renderApp(){
  saveScroll();
  applyTheme();""",
"""function renderApp(){
  saveScroll();
  /* 다시 그리기 전에 타이핑 중인 값을 상태로 옮깁니다. 마법사 6단계에서 요청사항을 치다가 유아의자 ± 를 누르면 입력이 사라졌고,
     1분 갱신·폰 회전에도 같은 일이 났습니다(점검 R1). 입력칸이 없는 화면에서는 아무 일도 안 합니다 */
  try{ if(WZ) wzSyncInputs(); if(!WZ && tmpRes && view.form && view.form.type === "res") syncRes(); }catch(e){}
  applyTheme();""")

# ---------- U1: 공개 TV·매장 선택 화면에서 리모컨 숫자키가 PIN 으로 들어가지 않게 ----------
s = R(s, """function pinPush(n){
  if(PIN_BUF.length>=4 || LOCK_BUSY || pinLockLeft() > 0) return;""",
"""function pinPush(n){
  if(!view.storeKey || view.display || AUTHED) return;   /* 잠금 화면일 때만. TV 리모컨 숫자키가 로그인 시도가 됐습니다(점검 U1) */
  if(PIN_BUF.length>=4 || LOCK_BUSY || pinLockLeft() > 0) return;""")

# ---------- C1: 글자마다 render 하던 입력 → onchange ----------
s = R(s, """      oninput="setPolicy('tvAd', this.value)">""", """      onchange="setPolicy('tvAd', this.value)">""")
s = R(s, """      oninput="setSms('parkingNote',this.value)">${esc(sm.parkingNote||"")}</textarea>""",
         """      onchange="setSms('parkingNote',this.value)">${esc(sm.parkingNote||"")}</textarea>""")

L.js_check(s)
L.save(s)
print("p9_e ok")
