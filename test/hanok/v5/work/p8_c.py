# -*- coding: utf-8 -*-
"""v5 7차 묶음 C — 쓰기 (Supabase)
   · saveData = flush: 마지막 동기화(SYNC)와 지금 JSON 을 비교해 바뀐 것만 — 새 예약 POST, 바뀐 예약 PATCH(updated_at 조건), 설정·스냅샷 PATCH
   · 충돌(조건부 PATCH 가 0행): 서버 행을 다시 읽어 확인창 — '상대 내용으로 보기'(기본) / '내 변경으로 덮어쓰기'. 삭제된 행이면 문구 다름
   · logEvent → logs INSERT (실패 무시)
   · reloadFromStore = 델타(updated_at=gt.마지막) → 병합. 로컬에서 고친(dirty) 예약은 덮지 않음
   · 저장 실패 → 빨간 띠 '저장 안 됨 · 다시 시도' (탭을 닫으면 사라진다고 씀). 1분 타이머도 재시도
   · B 의 '읽기 전용 단계' 해제"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---------- 읽기 전용 단계 해제 ----------
rep("""  data._readonly = true; READONLY_WHY = "stage";               /* 7차 B: 쓰기는 묶음 C 에서. 그때까지 읽기 전용 */
  syncMark(data);""",
"""  data._readonly = false; READONLY_WHY = "";
  syncMark(data);""")
rep("""  if(AUTHED && DATA && DATA._readonly && READONLY_WHY === "stage")
    return `<div class="crashbar stage"><b>읽기 전용</b><span>서버 연결 7차 B 단계 — 저장 기능은 C 에서 붙습니다.</span></div>`;
""", "")
rep("""          : READONLY_WHY === "stage"  ? "저장 기능은 아직 서버에 연결하기 전입니다(7차 C 단계)."
""", "")
rep("""/* 오프라인(캐시로 보는 중)은 갈색 — 빨강은 '고장' 이라 구분. 단계 띠(7차 B)는 호박색 */
.crashbar.offline{background:#5A4E40}
.crashbar.offline button{color:#5A4E40}
.crashbar.stage{background:#8A6512; padding:var(--s8) var(--s16)}""",
"""/* 오프라인(캐시로 보는 중)은 갈색 — 빨강은 '고장·저장 안 됨' 이라 구분 */
.crashbar.offline{background:#5A4E40}
.crashbar.offline button{color:#5A4E40}
/* 저장 실패 띠 — #app 밖(body)에 두어 render() 와 무관하게 붙였다 뗍니다 (입력 중인 시트를 다시 그리지 않으려고) */
.crashbar.savefail{bottom:auto; top:0; box-shadow:0 2px 14px rgba(0,0,0,.3); z-index:9998}""")

# ---------- syncMark: stores 의 updated_at 도 기억 (다른 기기가 설정을 바꿨는지 델타에서 봄) ----------
rep("""  SYNC = { res:{}, settings:{}, snapshots:{}, lastUpd:{} };
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var st = data[k]; if(!st) return;
    SYNC.settings[k] = JSON.stringify(st.settings); SYNC.snapshots[k] = JSON.stringify(st.snapshots || {});""",
"""  SYNC = { res:{}, settings:{}, snapshots:{}, lastUpd:{}, storeUpd:{} };
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var st = data[k]; if(!st) return;
    SYNC.settings[k] = JSON.stringify(st.settings); SYNC.snapshots[k] = JSON.stringify(st.snapshots || {});
    SYNC.storeUpd[k] = st._updatedAt || "";""")

# ---------- enterStore 뒤에 지난 날짜 정리·스냅샷 (saveData → flush 로 올라감) ----------
rep("""async function enterStore(){
  var d = await loadFromServer();
  DATA = assembleData(d);
  AUTHED = true; OFFLINE = null; LOAD_ERROR = null;
  cacheSave();
}""",
"""async function enterStore(){
  var d = await loadFromServer();
  DATA = assembleData(d);
  AUTHED = true; OFFLINE = null; LOAD_ERROR = null;
  cacheSave();
  autoCloseDays();   /* 지난 날짜의 '확정' → '방문' (이 기기가 처음 켠 것이면 여기서 올라갑니다) */
  takeSnapshot();
}""")

# ---------- 델타 갱신 ----------
rep("""/* 1분 갱신. 묶음 C 에서 델타(updated_at=gt.)로 바꿉니다 — 지금은 통째로 다시 읽음 */
async function reloadFromStore(){
  if(!supaOn()) return;
  if(view.display && !SESSION){ await loadPublic(); return; }
  if(!SESSION) return;
  if(OFFLINE){ await reconnect(); return; }
  var d = await loadFromServer();
  var ui = DATA._ui;
  DATA = assembleData(d); DATA._ui = ui;
  cacheSave();
}""",
"""/* 1분 갱신 — 전체가 아니라 바뀐 행만 (updated_at=gt.마지막으로 본 최대값).
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
      if(JSON.stringify(st.settings) === SYNC.settings[k]){ st.settings = migrate({ hanok:{settings:srow.settings||{}} }).hanok.settings; SYNC.settings[k] = JSON.stringify(st.settings); changed = true; }
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
  if(changed) cacheSave();
}""")

# ---------- flush ----------
rep("""async function saveData(){
  uiSave();                            /* 테마·배율·tvType 폴백은 기기별 — 서버와 무관하게 늘 저장 */
  if(DATA && DATA._readonly) return;   /* 불러오기 실패 · 오프라인 · 7차 B 단계 — 덮어쓰지 않습니다 */
  if(supaOn()) return;                 /* 묶음 C 에서 flush(바뀐 것만 PATCH/POST)로 채웁니다 */
  try{ await window.storage.set(STORAGE_KEY, JSON.stringify(DATA)); }
  catch(e){ console.error("저장 실패", e); }
}""",
"""async function saveData(){
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
      for(j = 0; j < all.length; j++){
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
  var rows = await sb("/rest/v1/reservations", { method:"POST", body:resToRow(rec, k), prefer:"return=representation" });
  markSynced(rec, rows && rows[0], sent);
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
  var title = t.deleted_at ? "다른 기기에서 이미 삭제된 예약입니다" : "다른 기기에서 먼저 수정됐습니다";
  var takeTheirs = await uiConfirm(title, conflictSummary(rec, trec) + "\\n\\n상대 내용으로 보면 내 변경은 버려집니다.",
                                   { ok:"상대 내용으로 보기", cancel:"내 변경으로 덮어쓰기" });
  if(takeTheirs){
    var li = st.reservations.indexOf(rec), ti = st.trash.indexOf(rec);
    if(li >= 0) st.reservations.splice(li, 1); if(ti >= 0) st.trash.splice(ti, 1);
    if(t.deleted_at) st.trash.push(trec); else st.reservations.push(trec);
    st.reservations.sort(function(a, b){ return (a.date + a.time).localeCompare(b.date + b.time); });
    SYNC.res[rec.id] = JSON.stringify(trec); if(t.updated_at > (SYNC.lastUpd[k] || "")) SYNC.lastUpd[k] = t.updated_at;
    render();
  }else{
    var rows2 = await sb("/rest/v1/reservations?id=eq." + rec.id, { method:"PATCH", body:row, prefer:"return=representation" });
    markSynced(rec, rows2 && rows2[0], cur);
  }
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
  return out.length ? "상대 기기의 내용:\\n" + out.join("\\n") : "상대 기기의 내용은 화면과 같지만 나중에 저장됐습니다.";
}
/* 저장 실패 띠 — body 에 직접 붙입니다(입력 중 시트를 다시 그리지 않으려고). 다시 시도는 flush */
function saveFailBand(){
  var el = document.getElementById("savefail");
  if(!SAVE_FAIL){ if(el) el.parentNode.removeChild(el); return; }
  if(!el){ el = document.createElement("div"); el.id = "savefail"; el.className = "crashbar savefail"; document.body.appendChild(el); }
  el.innerHTML = '<b>저장 안 됨</b><span>' + esc(SAVE_FAIL.msg) + ' · 지금 화면의 변경은 저장되지 않았습니다. <b>탭을 닫으면 사라집니다.</b></span>' +
                 '<button onclick="flush()">다시 시도</button>';
}""")

# ---------- 로그 INSERT ----------
rep("""  if(DATA._logs.length > LOG_MAX) DATA._logs = DATA._logs.slice(-LOG_MAX);
  saveData();
}""",
"""  if(DATA._logs.length > LOG_MAX) DATA._logs = DATA._logs.slice(-LOG_MAX);
  /* 서버에도 한 줄. 실패해도 무시 — 로그 때문에 화면이 죽으면 안 됩니다 */
  if(supaOn() && SESSION && !OFFLINE){
    sb("/rest/v1/logs", { method:"POST", body:{ store:view.storeKey || "-", action:action, detail:detail || "", who:SESSION.who, ua:(navigator.userAgent||"").slice(0,120) }, prefer:"return=minimal" })
      .catch(function(e){ console.warn("로그 저장 실패", e.message); });
  }
  saveData();
}""")

# ---------- 1분 타이머: 저장 실패분 재시도 ----------
rep("""  sessionTick();   /* 토큰 만료 5분 전 갱신 */
  if(!AUTHED || view.display || WZ || view.form || MODAL) return;""",
"""  sessionTick();   /* 토큰 만료 5분 전 갱신 */
  if(SAVE_FAIL && !OFFLINE) flush();   /* 저장 못 한 것이 있으면 다시 */
  if(!AUTHED || view.display || WZ || view.form || MODAL) return;""")

# 로그인 성공 기록은 세션이 생긴 뒤라 서버에도 남습니다 — 순서 그대로

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_c 적용 완료")
