# -*- coding: utf-8 -*-
"""v6 8차-F(2) — 점검 결함 수정 묶음 2
   S5 서버 행 검증(rowToRes) + onclick 안의 이름 값은 jsq() 로 · S6 fetchIP 삭제 · D4/R7 시계 어긋남 검사 + 자정 autoClose
   R2 단계 점 건너뛰기 막기 · R3 재확정 시 '오늘 취소' 태그 해제 · T3 TV 에서 좌석표 전환은 기기 안에서만
   U3 화면 전환 때 겹침 요소 초기화 · U4 sheetHead esc · U5 showCrash esc · C3 설정 진입 시 새 임시본 · C4 최소>최대 보정"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- S5: 서버 행 검증 ----------
s = L.replace_fn(s, "rowToRes", r"""function rowToRes(row){
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
  if(rec.seatPref != null && ["any","room-any","table-any","hall-any"].indexOf(rec.seatPref) < 0) rec.seatPref = null;
  rec.updatedAt = row.updated_at;                                /* 서버 시각 문자열 그대로 (파싱 금지 — 마이크로초가 잘립니다) */
  if(row.deleted_at) rec.deletedAt = row.deleted_at;
  if(!rec.createdAt && row.created_at) rec.createdAt = row.created_at;
  return rec;
}""")
# rowToRes 가 null 을 줄 수 있으니 호출부에서 거릅니다
import re
for m in re.findall(r"[^\n]*rowToRes\([^\n]*", s):
    pass
s = R(s, """  var trec = rowToRes(t);
  var st = DATA[k];""", """  var trec = rowToRes(t);
  if(!trec){ await pushNew(rec, k); return; }   /* 서버 행이 깨져 있으면 내 것으로 덮습니다 */
  var st = DATA[k];""")

# ---------- S5: onclick 안에 들어가는 '이름' 값(설정에서 온 경로명·코스 키) ----------
s = R(s, """function esc(s){
  return String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;")
    .replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");
}""",
"""function esc(s){
  return String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;")
    .replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");
}
/* onclick="fn('여기')" 안에 넣는 값. esc 만 하면 HTML 파서가 &#39; 를 ' 로 되돌려 JS 문자열이 끊깁니다 —
   JS 쪽 이스케이프(\\')를 먼저 하고 HTML 이스케이프를 겹칩니다 */
function jsq(s){ return esc(String(s == null ? "" : s).replace(/\\\\/g,"\\\\\\\\").replace(/'/g,"\\\\'").replace(/\\r?\\n/g," ")); }""")
s = R(s, """onclick="delSource('${esc(x)}')" """, """onclick="delSource('${jsq(x)}')" """)
s = R(s, """onclick="pickSource('${esc(x)}')">${esc(x)}</button>""", """onclick="pickSource('${jsq(x)}')">${esc(x)}</button>""")
s = R(s, """onclick="wzSource('${v}')">""", """onclick="wzSource('${jsq(v)}')">""")
s = R(s, """onclick="bumpCourse('${key}')">""", """onclick="bumpCourse('${jsq(key)}')">""")
s = R(s, """onclick="dropCourse('${key}')" """, """onclick="dropCourse('${jsq(key)}')" """)

# ---------- S6: 외부 IP 조회 삭제 (외부 요청 0 원칙. 서버 로그에는 who 만) ----------
s = L.remove_fn(s, "fetchIP")
s = R(s, """  fetchIP();
  autoCloseDays();""", """  autoCloseDays();""")

# ---------- D4/R7: 서버 시각과 기기 시계 비교, 자정 넘김 autoClose ----------
s = R(s, """  var text = await res.text(), json = null;""",
"""  /* 기기 시계 검사(점검 D4) — RTC 가 죽은 태블릿은 날짜가 몇 년씩 틀립니다. 서버 응답의 Date 헤더와 비교해 둡니다 */
  try{ var sd = res.headers && res.headers.get("date"); if(sd){ var sms = Date.parse(sd); if(!isNaN(sms)) CLOCK_SKEW = sms - Date.now(); } }catch(e){}
  var text = await res.text(), json = null;""")
s = R(s, """var FLUSHING = false, FLUSH_AGAIN = false, SAVE_FAIL = null;""",
"""var FLUSHING = false, FLUSH_AGAIN = false, SAVE_FAIL = null;
var CLOCK_SKEW = 0;   /* 서버 시각 − 기기 시각(ms). 하루 이상 어긋나면 자동 방문 처리·스냅샷을 건너뜁니다 */
function clockBad(){ return Math.abs(CLOCK_SKEW) > 12 * 3600 * 1000; }""")
s = R(s, """function autoCloseDays(){
  if(!DATA) return 0;""", """function autoCloseDays(){
  if(!DATA || clockBad()) return 0;   /* 시계가 틀린 기기가 미래 예약을 '방문' 으로 올리지 않게 */""")
s = R(s, """  if(SNAP_DAY && todayStr() !== SNAP_DAY) takeSnapshot();
  sessionTick();""", """  if(SNAP_DAY && todayStr() !== SNAP_DAY){ takeSnapshot(); if(AUTHED && autoCloseDays()) saveData(); }   /* 어제 '확정' → '방문' 도 함께(점검 R7) */
  sessionTick();""")
s = R(s, """  if(!LOAD_ERROR) return "";
  return `<div class="crashbar loaderr">""", """  if(AUTHED && clockBad()){
    return `<div class="crashbar offline"><b>이 기기의 시계가 틀립니다</b><span>서버와 ${Math.round(Math.abs(CLOCK_SKEW)/3600000)}시간 이상 차이 — 날짜·시각 설정을 확인하세요. 자동 방문 처리는 멈춰 둡니다.</span></div>`;
  }
  if(!LOAD_ERROR) return "";
  return `<div class="crashbar loaderr">""")

# ---------- R2: 단계 점으로 건너뛰기 막기 — 한 단계씩 검사하며 전진, 점은 가 본 단계까지만 ----------
s = R(s, """async function wzGo(n){
  wzSyncInputs();                       /* 먼저 입력값을 상태로 옮긴 뒤 */
  if(n > WZ.step && !wzCanNext()) return; /* 통과 여부를 검사 */""",
"""async function wzGo(n){
  wzSyncInputs();                       /* 먼저 입력값을 상태로 옮긴 뒤 */
  /* 두 단계 이상 앞으로 뛰면(단계 점) 한 단계씩 검사하며 갑니다 — 좌석·메뉴·알러지 확인을 건너뛰고 등록되던 것(점검 R2) */
  if(n > WZ.step + 1){
    while(WZ.step < n){ const was = WZ.step; await wzGo(was + 1); if(WZ.step !== was + 1) return; }
    return;
  }
  if(n > WZ.step && !wzCanNext()) return; /* 통과 여부를 검사 */""")
s = R(s, """  WZ.step = Math.max(0, Math.min(LAST_STEP, n));
  render();
  /* 단계를 옮길 때만 맨 위로 */""", """  WZ.step = Math.max(0, Math.min(LAST_STEP, n));
  WZ.maxStep = Math.max(WZ.maxStep || 0, WZ.step);
  render();
  /* 단계를 옮길 때만 맨 위로 */""")
s = R(s, """    `<button class="wz-dot ${i===WZ.step?'on':''} ${i<WZ.step?'past':''}" onclick="wzGo(${i})">""",
"""    `<button class="wz-dot ${i===WZ.step?'on':''} ${i<WZ.step?'past':''}" onclick="wzGo(${i})" ${i > (WZ.maxStep||0) + 1 ? "disabled" : ""}>""")

# ---------- R3: 취소 → 확정 되돌림 ----------
s = R(s, """    const n = touch({...r, status});
    if(status==="취소" || status==="노쇼") addChange(n, status, []);
    return n;""",
"""    const n = touch({...r, status});
    if(status==="취소" || status==="노쇼") addChange(n, status, []);
    else if(status==="확정" && (r.status==="취소" || r.status==="노쇼")) addChange(n, "변경", [{n:"상태", a:r.status, b:"확정"}]);   /* 되돌림도 남겨야 '오늘 취소' 태그가 풀립니다(점검 R3) */
    return n;""", 2)
s = R(s, """  /* 취소·노쇼가 가장 중요합니다 — 자리를 비워야 하는 건이라 */
  var kind = kinds["취소"] ? "취소" : kinds["노쇼"] ? "노쇼"
           : kinds["등록"] ? "신규" : "변경";""",
"""  /* 취소·노쇼가 가장 중요합니다 — 자리를 비워야 하는 건이라. 단, 그 뒤에 다시 확정으로 되돌렸으면(상태 변경) 취소가 아닙니다 */
  var lastStatus = null;
  for(i=0;i<cs.length;i++){
    if(cs[i].kind==="취소" || cs[i].kind==="노쇼") lastStatus = cs[i].kind;
    else if(cs[i].kind==="변경" && (cs[i].items||[]).some(function(x){ return x.n==="상태"; })) lastStatus = null;
  }
  var kind = lastStatus ? lastStatus : kinds["등록"] ? "신규" : "변경";""")

# ---------- T3: TV(읽기 전용)에서 좌석표 전환은 이 기기 안에서만 ----------
s = R(s, """function tvType(){
  var st = view.storeKey && DATA && DATA[view.storeKey] ? DATA[view.storeKey].settings : null;""",
"""function tvType(){
  if(view.tvTypeLocal) return view.tvTypeLocal;   /* TV 에서 리모컨으로 바꾼 것 — 저장은 못 하니 이 화면에서만 */
  var st = view.storeKey && DATA && DATA[view.storeKey] ? DATA[view.storeKey].settings : null;""")
s = R(s, """function swapTvType(){
  setTvType(tvType() === "grid" ? "list" : "grid");""",
"""function swapTvType(){
  var next = tvType() === "grid" ? "list" : "grid";
  if(DATA && DATA._readonly){ view.tvTypeLocal = next; render(); }   /* 공개 TV 는 저장이 안 되므로 막지 않고 화면만 바꿉니다(점검 T3) */
  else setTvType(next);""")

# ---------- U3: 화면 전환 때 겹침 요소 초기화 ----------
s = R(s, """async function lockNow(){
  if(!await flushBeforeLeave()) return;""",
"""/* 마법사·달력·더보기·확인창을 한 번에 접습니다. 세션 만료·주소 이동으로 화면이 바뀔 때 옛 마법사가 남거나
   body 의 overflow:hidden 이 남아 스크롤이 안 되던 것(점검 U3) */
function resetOverlays(){
  WZ = null; tmpRes = null; view.form = null; view.calOpen = false; view.moreOpen = false; view.pickSeat = null;
  if(typeof MODAL !== "undefined" && MODAL && MODAL.res){ try{ MODAL.res(false); }catch(e){} }
  MODAL = null;
  try{ document.body.style.overflow = ""; }catch(e){}
}
async function lockNow(){
  if(!await flushBeforeLeave()) return;
  resetOverlays();""")
s = R(s, """async function goHome(){
  if(!await flushBeforeLeave()) return;""", """async function goHome(){
  if(!await flushBeforeLeave()) return;
  resetOverlays();""")
s = R(s, """    if(!e.network && e.status && e.status < 500 && e.status !== 429){ sessionClear(); AUTHED = false; view.storeKey = null; render(); }""",
"""    if(!e.network && e.status && e.status < 500 && e.status !== 429){ sessionClear(); AUTHED = false; view.storeKey = null; resetOverlays(); render(); }""")

# ---------- U4/U5: esc ----------
s = R(s, """    ${sheetHead(`${esc(room.name)} 사용 중지`)}""", """    ${sheetHead(`${esc(room.name)} 사용 중지`)}""")   # 이미 esc — 확인용
s = R(s, """      '<i>' + String(e && e.message ? e.message : e).slice(0,120) + '</i>';""",
         """      '<i>' + esc(String(e && e.message ? e.message : e).slice(0,120)) + '</i>';""")

# ---------- C3: 설정 화면에 들어올 때 안 고친 임시본은 새로 ----------
s = R(s, """async function setTab(t){""", """async function setTab(t){
  /* 다른 기기가 설정을 바꿨는데 이 기기에 옛 임시본이 남아 있으면 '저장 안 한 변경' 으로 오탐하고, 적용하면 되돌립니다(점검 C3).
     고친 것이 없으면 들어올 때마다 새로 뜹니다 */
  if(t === "settings" && view.draft && !settingsDirty()) view.draft = null;""")

# ---------- C4: 룸 최소 > 최대 보정 ----------
s = R(s, """  if(f.ctx && f.ctx.room){
    st.rooms = st.rooms.map(r=>r.id===f.ctx.room?Object.assign({}, r, {[f.key]:v, tuned:true}):r);""",
"""  if(f.ctx && f.ctx.room){
    st.rooms = st.rooms.map(r=>{
      if(r.id!==f.ctx.room) return r;
      const n = Object.assign({}, r, {[f.key]:v, tuned:true});
      /* 최소가 최대보다 크면 그 좌석은 어떤 인원에도 안 맞아 배정 후보에서 영영 빠집니다(점검 C4) — 맞춰 줍니다 */
      if(f.key==="minCapacity" && n.capacity != null && v > seatMax(n)) n.capacity = v;
      if(f.key==="capacity" && n.minCapacity != null && n.minCapacity > v) n.minCapacity = v;
      return n;
    });""")

L.js_check(s)
L.save(s)
print("p9_f ok")
