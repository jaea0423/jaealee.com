# -*- coding: utf-8 -*-
"""v5 7차 묶음 E — 계정
   · PIN 변경을 서버로: (관리자 비밀번호로 admin 로그인 확인 → 현재 PIN 으로 staff 로그인 → 그 토큰으로 PUT /auth/v1/user). 새 PIN 확인 칸은 남김(오타로 잠기지 않게)
   · 관리자 비밀번호 변경 시트 (현재 → 새 → 확인, 6자 이상)
   · PIN 틀림 5회 → 60초 잠금 (화면에서 먼저)
   · PIN_ANY · DEFAULT_AUTH · DATA._auth 삭제 — 파일 안 평문 PIN 이 이걸로 끝. 서버 미연결(설정 없는 빌드)은 개발용이라 아무 PIN 이나 통과하고 그렇다고 표시
   · migrate 가 옛 _auth 를 지움"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---------- PIN_ANY · _auth 삭제 ----------
rep("""const DEFAULT_AUTH = { pin:"1234", admin:"admin1234" };
""", "")
rep("""  if(!DATA._auth) DATA._auth = {...DEFAULT_AUTH};
""", "")
rep("""function migrate(d){
  d._auth = d._auth || {...DEFAULT_AUTH};
  d._logs = d._logs || [];""",
"""function migrate(d){
  delete d._auth;   /* 7차: PIN 은 서버(Supabase 계정)에만. 옛 저장본에 평문으로 남아 있던 것을 지웁니다 */
  d._logs = d._logs || [];""")
rep("""  d._auth = {...DEFAULT_AUTH};

  return assignTentatives(d);""",
"""  return assignTentatives(d);""")

a = s.index("   제작 중 — 아무 번호나 통과시킵니다")
b = s.index("var LOCK_BUSY = false;")
# 주석 블록 시작(직전의 /* ====) 찾기
start = s.rfind("/* ====", 0, a)
s = s[:start] + """/* ============================================================
   PIN 확인
   서버 모드(SUPA_CFG 있음): PIN 4자리 + "00" 으로 staff 계정 로그인 — 진짜 검증. 틀림 5회 → 60초 잠금.
   서버 미연결(설정 파일 없는 빌드): 개발·확인용이라 아무 번호나 통과시키고, 잠금 화면에 그렇다고 표시합니다.
   ★ 실서비스는 반드시 supabase.prod.json 을 넣고 빌드합니다 — 그러면 이 통과 경로는 코드상 닿지 않습니다. ★
   ============================================================ */
var PIN_FAILS = 0, PIN_LOCK_UNTIL = 0;   /* 틀린 횟수 · 잠금 해제 시각(ms) */
function pinLockLeft(){ return Math.max(0, Math.ceil((PIN_LOCK_UNTIL - Date.now()) / 1000)); }
""" + s[b:]

rep("""async function pinCheck(){
  if(supaOn()) return pinCheckServer();
  const real = PIN_BUF === ((DATA._auth && DATA._auth.pin) || DEFAULT_AUTH.pin);
  const ok = real || PIN_ANY;
  logEvent(ok ? "로그인 성공" : "로그인 실패",
    ok ? (real ? "" : "제작 중 · PIN 확인 안 함") : `입력값 ${PIN_BUF}`);
  if(ok){
    AUTHED = true; PIN_BUF=""; PIN_ERR="";
    DATA._session = {authed:true, since:new Date().toISOString()};
    saveData();
    startIntro();
  }
  else { PIN_BUF=""; PIN_ERR="PIN 번호가 맞지 않습니다."; }
  render();
}""",
"""async function pinCheck(){
  if(supaOn()) return pinCheckServer();
  /* 서버 미연결 — 개발용. 아무 번호나 통과 */
  logEvent("로그인 성공", "서버 미연결 · PIN 확인 안 함");
  AUTHED = true; PIN_BUF=""; PIN_ERR="";
  DATA._session = {authed:true, since:new Date().toISOString()};
  saveData();
  startIntro();
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
}""")
rep("""  }catch(e){
    PIN_BUF = "";
    if(e.network){
      if(pinHashOk(pin) && enterOffline(pin)){ LOCK_BUSY = false; startIntro(); return; }
      PIN_ERR = "서버에 연결할 수 없습니다";
    }else if(e.status === 400){                      /* Supabase: 비밀번호 틀림 = 400 invalid_credentials. 401 은 API 키 문제라 따로 */
      PIN_ERR = "PIN 번호가 맞지 않습니다.";
    }else{""",
"""  }catch(e){
    PIN_BUF = "";
    if(e.network){
      if(pinHashOk(pin) && enterOffline(pin)){ LOCK_BUSY = false; startIntro(); return; }
      PIN_ERR = "서버에 연결할 수 없습니다";
    }else if(e.status === 400){                      /* Supabase: 비밀번호 틀림 = 400 invalid_credentials. 401 은 API 키 문제라 따로 */
      PIN_ERR = "PIN 번호가 맞지 않습니다."; pinFailed();
    }else if(e.status === 429){
      PIN_ERR = "너무 여러 번 틀렸습니다. 잠시 뒤 다시 시도하세요.";
    }else{""")
rep("""    await sbLogin(SUPA_CFG.staffEmail, pinToPassword(pin));
    pinHashSave(pin);""",
"""    await sbLogin(SUPA_CFG.staffEmail, pinToPassword(pin));
    PIN_FAILS = 0; pinHashSave(pin);""")
# 잠금 화면 — 잠긴 동안 입력 막고 남은 초 표시. 서버 미연결이면 안내
rep("""        <div class="lk-err ${LOCK_BUSY?'busy':''}">${LOCK_BUSY ? "서버 확인 중…" : esc(PIN_ERR)}</div>""",
    """        <div class="lk-err ${LOCK_BUSY?'busy':''}">${LOCK_BUSY ? "서버 확인 중…" : (pinLockLeft() > 0 ? `${pinLockLeft()}초 뒤에 다시 입력할 수 있습니다` : esc(PIN_ERR))}</div>""")
rep("""        <button class="lk-back" onclick="backToStores()">← 매장 다시 고르기</button>""",
    """        ${supaOn() ? "" : `<div class="lk-open"><b>서버 미연결 빌드</b> — 확인용이라 아무 번호나 통과합니다</div>`}
        <button class="lk-back" onclick="backToStores()">← 매장 다시 고르기</button>""")
rep("""function pinPush(n){
  if(PIN_BUF.length>=4 || LOCK_BUSY) return;""",
"""function pinPush(n){
  if(PIN_BUF.length>=4 || LOCK_BUSY || pinLockLeft() > 0) return;""")
rep("""/* PIN_ANY 가 켜져 있을 때만 뜹니다. 잠금이 풀려 있다는 사실이 눈에 보여야""",
    """/* 서버 미연결 빌드에서만 뜹니다. 잠금이 풀려 있다는 사실이 눈에 보여야""")

# ---------- PIN 변경 · 관리자 비밀번호 변경 시트 ----------
rep("""function sheetPin(){
  return `
    ${sheetHead("PIN 번호 변경")}
    <label class="f big"><div class="lb">관리자 비밀번호</div>
      <input id="pin-admin" type="password" placeholder="관리자 비밀번호" autocomplete="off">
    </label>
    <label class="f big"><div class="lb">새 PIN (숫자 4자리)</div>""",
"""function sheetPin(){
  if(!supaOn()) return `${sheetHead("PIN 번호 변경")}<p class="f-note">서버 미연결 빌드에서는 PIN 이 없습니다(아무 번호나 통과). 실서비스 빌드에서 바꿉니다.</p>
    <div class="sheet-actions"><button class="btn ghost" onclick="closeSheet()">닫기</button></div>`;
  return `
    ${sheetHead("PIN 번호 변경")}
    <label class="f big"><div class="lb">관리자 비밀번호</div>
      <input id="pin-admin" type="password" placeholder="관리자 비밀번호" autocomplete="off">
    </label>
    <label class="f big"><div class="lb">현재 PIN</div>
      <input id="pin-cur" type="password" inputmode="numeric" maxlength="4" placeholder="••••" autocomplete="off">
    </label>
    <label class="f big"><div class="lb">새 PIN (숫자 4자리)</div>""")
rep("""async function savePin(){
  const g = id => document.getElementById(id).value;
  if(g("pin-admin") !== ((DATA._auth && DATA._auth.admin) || DEFAULT_AUTH.admin)){
    logEvent("PIN 변경 실패", "관리자 비밀번호 불일치");
    await uiAlert2("관리자 비밀번호가 맞지 않습니다."); return;
  }
  const a = g("pin-new"), b = g("pin-new2");
  if(!/^\\d{4}$/.test(a)){ await uiAlert2("PIN은 숫자 4자리여야 합니다."); return; }
  if(a !== b){ await uiAlert2("새 PIN이 서로 다릅니다."); return; }
  DATA._auth.pin = a;
  logEvent("PIN 변경", "성공");
  DATA._session = {authed:true, since:new Date().toISOString()};
  view.form = null; saveData(); render();
  await uiAlert2("PIN이 변경되었습니다.");
}""",
"""/* PIN = staff 계정 비밀번호. admin 토큰으로는 남(staff)의 비밀번호를 못 바꾸므로:
   관리자 비밀번호로 admin 로그인(권한 확인) → 현재 PIN 으로 staff 로그인 → 그 토큰으로 PUT /auth/v1/user.
   지금 세션(SESSION)은 건드리지 않습니다 — 임시 토큰만 씁니다 */
async function authToken(email, password){
  var j = await sb("/auth/v1/token?grant_type=password", { method:"POST", anon:true, body:{ email:email, password:password } });
  return j.access_token;
}
async function setPassword(token, password){
  var res = await fetch(SUPA_CFG.url + "/auth/v1/user", { method:"PUT",
    headers:{ "apikey":SUPA_CFG.anonKey, "Authorization":"Bearer " + token, "Content-Type":"application/json" },
    body: JSON.stringify({ password:password }) });
  if(!res.ok){ var j = null; try{ j = await res.json(); }catch(e){} var err = new Error((j && (j.msg || j.message || j.error_description)) || ("HTTP " + res.status)); err.status = res.status; throw err; }
}
async function savePin(){
  const g = id => document.getElementById(id).value;
  const adminPw = g("pin-admin"), cur = g("pin-cur"), a = g("pin-new"), b = g("pin-new2");
  if(!/^\\d{4}$/.test(a)){ await uiAlert2("PIN은 숫자 4자리여야 합니다."); return; }
  if(a !== b){ await uiAlert2("새 PIN이 서로 다릅니다."); return; }
  if(!/^\\d{4}$/.test(cur)){ await uiAlert2("현재 PIN을 입력하세요."); return; }
  try{
    try{ await authToken(SUPA_CFG.adminEmail, adminPw); }
    catch(e){ if(e.status === 400){ logEvent("PIN 변경 실패", "관리자 비밀번호 불일치"); await uiAlert2("관리자 비밀번호가 맞지 않습니다."); return; } throw e; }
    var staffTok;
    try{ staffTok = await authToken(SUPA_CFG.staffEmail, pinToPassword(cur)); }
    catch(e){ if(e.status === 400){ logEvent("PIN 변경 실패", "현재 PIN 불일치"); await uiAlert2("현재 PIN이 맞지 않습니다."); return; } throw e; }
    await setPassword(staffTok, pinToPassword(a));
  }catch(e){
    await uiAlert("PIN을 바꾸지 못했습니다", e.network ? "서버에 연결할 수 없습니다." : e.message, "warn"); return;
  }
  pinHashSave(a);
  logEvent("PIN 변경", "성공");
  view.form = null; render();
  await uiAlert2("PIN이 변경되었습니다.\\n다른 기기는 다음 로그인부터 새 PIN 을 씁니다.");
}
/* 관리자 비밀번호 변경 — admin 본인 토큰으로 */
function sheetAdminPw(){
  return `
    ${sheetHead("관리자 비밀번호 변경")}
    <label class="f big"><div class="lb">현재 관리자 비밀번호</div>
      <input id="apw-cur" type="password" autocomplete="off">
    </label>
    <label class="f big"><div class="lb">새 비밀번호 (6자 이상)</div>
      <input id="apw-new" type="password" autocomplete="off">
    </label>
    <label class="f big"><div class="lb">새 비밀번호 확인</div>
      <input id="apw-new2" type="password" autocomplete="off">
    </label>
    <p class="f-note">관리자 비밀번호는 PIN 을 바꿀 때 씁니다. 잊으면 Supabase 대시보드에서만 되돌릴 수 있습니다.</p>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="saveAdminPw()">변경</button>
    </div>`;
}
async function saveAdminPw(){
  const g = id => document.getElementById(id).value;
  const cur = g("apw-cur"), a = g("apw-new"), b = g("apw-new2");
  if(a.length < 6){ await uiAlert2("새 비밀번호는 6자 이상이어야 합니다."); return; }
  if(a !== b){ await uiAlert2("새 비밀번호가 서로 다릅니다."); return; }
  try{
    var tok;
    try{ tok = await authToken(SUPA_CFG.adminEmail, cur); }
    catch(e){ if(e.status === 400){ logEvent("관리자 비밀번호 변경 실패", "현재 비밀번호 불일치"); await uiAlert2("현재 관리자 비밀번호가 맞지 않습니다."); return; } throw e; }
    await setPassword(tok, a);
  }catch(e){
    await uiAlert("비밀번호를 바꾸지 못했습니다", e.network ? "서버에 연결할 수 없습니다." : e.message, "warn"); return;
  }
  logEvent("관리자 비밀번호 변경", "성공");
  view.form = null; render();
  await uiAlert2("관리자 비밀번호가 변경되었습니다.");
}""")
rep("""function openPin(){ view.form={type:"pin"}; render(); }""",
    """function openPin(){ view.form={type:"pin"}; render(); }
function openAdminPw(){ view.form={type:"apw"}; render(); }""")
rep("""noshow:sheetNoshow, pin:sheetPin, logs:sheetLogs,""",
    """noshow:sheetNoshow, pin:sheetPin, apw:sheetAdminPw, logs:sheetLogs,""")
rep("""      <button class="btn" onclick="openPin()">PIN 번호 변경</button>
      <button class="btn danger" onclick="lockNow()">로그아웃</button>
    </div>
    <p class="f-note">PIN 변경에는 관리자 비밀번호가 필요합니다.</p>`;""",
"""      <button class="btn" onclick="openPin()">PIN 번호 변경</button>
      ${supaOn() ? `<button class="btn" onclick="openAdminPw()">관리자 비밀번호 변경</button>` : ""}
      <button class="btn danger" onclick="lockNow()">로그아웃</button>
    </div>
    <p class="f-note">PIN 변경에는 관리자 비밀번호가 필요합니다. PIN 은 직원과 공유하는 번호, 관리자 비밀번호는 사장님만 아는 것입니다.</p>`;""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_e 적용 완료")
