/* ---------- 홈페이지 관리 (설정 → 홈페이지 → 열기. 설정이 관리자 비밀번호라 여기서 또 묻지 않음) ----------
   가게 사이트(../)의 글·사진·팝업·차림·영업시간·연락처와 '홈페이지 예약' 규칙을 여기서 고칩니다. 값은 설정(store().settings)이 아니라 서버 site_draft/site_versions 에 있습니다.

   흐름:  초안(site_draft) 고치기 → 미리보기(사이트 ?preview=1) → 적용(site_versions 에 한 판) — 지금 바로 / 날짜·시각을 정해서
   · 사이트는 apply_at ≤ 지금 인 최신 판을 읽습니다(hanok/js/content.js). 예약해 둔 판은 그 시각까지 손님에게 안 보입니다.
   · 초안은 서버에 한 줄(매장당). 다른 기기에서 이어서 고칠 수 있습니다. '초안 저장' 을 눌러야 서버에 갑니다.
   · 되돌리기 = 이전 판을 초안으로 가져와 다시 적용. 판은 지우지 않습니다(예약해 둔 미래 판만 취소 가능).
   · 기본값(SITE_DEFAULT)은 사이트의 data/site.js 를 그때그때 읽습니다 — 시스템 빌드에 사이트 글을 넣어 두면 둘이 갈라집니다.
   저장하는 건 '문서 전체' 입니다(기본값 + 고친 것). 그래서 관리 화면에 보이는 그대로가 사이트에 나갑니다.

   구형 TV 금지 문법 규칙(system/CLAUDE.md 2장)은 이 파일에도 그대로 — 한 파일로 합쳐지니까. */
var SA = null;   /* {draft, saved(서버에 있는 초안 JSON 문자열), live:{id,apply_at,note,data}, versions:[], defaults, loading, err, tab} */
var SA_ROOT = null;

/* 사이트 루트 — system/ 또는 system/dev/ 에서 한두 칸 위. 로컬(127.0.0.1:8767/system/dev/)도 같은 규칙 */
function saRoot(){
  if(SA_ROOT) return SA_ROOT;
  var p = location.pathname.replace(/system\/.*$/, "");
  if(p === location.pathname) p = location.pathname.replace(/[^\/]*$/, "") + "../";   /* system 이 없는 경로(파일로 열었을 때) */
  SA_ROOT = p; return p;
}
async function openSiteAdmin(){
  if(!supaOn()){ await uiAlert("서버 설정이 없는 빌드입니다", "홈페이지 관리는 서버가 있어야 합니다.", "warn"); return; }
  if(!view.adminOk){ if(!await adminGate("홈페이지 관리 열기")) return; view.adminOk = true; }
  view.form = {type:"site", page:true};
  /* 닫았다 다시 열면 고치던 초안은 그대로(서버에서 다시 읽지 않음). 저장돼 있으면 새로 읽어 다른 기기 변경을 반영 */
  if(SA && !SA.err && !SA.loading && saDirty()){ render(); return; }
  if(!SA || SA.err) SA = {loading:true, tab:"online"}; else SA.loading = true;
  render();
  await saLoad();
  render();
}
/* 서버에서 초안·적용판·판 목록·기본값을 한 번에 */
async function saLoad(){
  var key = view.storeKey || "hanok";
  try{
    var defaults = await saDefaults();
    var dr = await sb("/rest/v1/site_draft?store=eq." + key + "&select=data,updated_at,by");
    var vs = await sb("/rest/v1/site_versions?store=eq." + key + "&select=id,apply_at,note,created_at,by&order=apply_at.desc&limit=40");
    var lv = await sb("/rest/v1/site_versions?store=eq." + key + "&apply_at=lte." + encodeURIComponent(new Date().toISOString()) + "&select=id,data,apply_at,note&order=apply_at.desc&limit=1");
    var live = lv[0] || null;
    /* 초안이 없으면 지금 보이는 판(없으면 기본값)에서 시작 */
    var base = dr[0] && dr[0].data && Object.keys(dr[0].data).length ? dr[0].data : (live ? live.data : {});
    var draft = saMerge(defaults, base);
    SA = { draft: draft, saved: JSON.stringify(draft), savedAt: dr[0] ? dr[0].updated_at : null, savedBy: dr[0] ? dr[0].by : "",
           live: live, versions: vs, defaults: defaults, loading: false, err: null, tab: (SA && SA.tab) || "online" };
  }catch(e){ SA = { loading:false, err:e.message || String(e), tab:"online" }; }
}
/* 사이트의 data/site.js 를 글로 받아 window 흉내 안에서 실행 → SITE_DEFAULT. 전역을 더럽히지 않게 */
async function saDefaults(){
  var r = await fetch(saRoot() + "data/site.js?v=" + Date.now(), {cache:"no-store"});
  if(!r.ok) throw new Error("사이트 기본값(data/site.js)을 읽지 못했습니다 (" + r.status + ")");
  var src = await r.text(), w = {};
  new Function("window", src)(w);
  if(!w.SITE_DEFAULT) throw new Error("data/site.js 에 SITE_DEFAULT 가 없습니다");
  return w.SITE_DEFAULT;
}
/* content.js 의 merge 와 같은 규칙: 객체는 키별로, 배열·문자열·숫자는 통째로 */
function saMerge(base, over){
  if(!over || typeof over !== "object" || Array.isArray(over)) return over === undefined ? deepClone(base) : deepClone(over);
  var out = deepClone(base || {});
  Object.keys(over).forEach(function(k){ out[k] = (base && typeof base[k] === "object" && base[k] && !Array.isArray(base[k])) ? saMerge(base[k], over[k]) : deepClone(over[k]); });
  return out;
}
function saDirty(){ return !!(SA && SA.draft && JSON.stringify(SA.draft) !== SA.saved); }
/* 경로("notices.0.title")로 읽고 쓰기 — 숫자 키는 배열 칸 */
function saGet(path){ return path.split(".").reduce(function(o, k){ return o == null ? undefined : o[k]; }, SA.draft); }
function saSet(path, val){
  var ks = path.split("."), o = SA.draft;
  for(var i = 0; i < ks.length - 1; i++){ if(o[ks[i]] == null || typeof o[ks[i]] !== "object") o[ks[i]] = /^\d+$/.test(ks[i+1]) ? [] : {}; o = o[ks[i]]; }
  o[ks[ks.length-1]] = val;
  saHeader();
}
function saSetLines(path, text){ saSet(path, String(text).split("\n").map(function(x){ return x.replace(/\s+$/, ""); }).filter(function(x){ return x.length; })); }
function saSetNum(path, v, min, max){ var n = parseInt(v, 10); if(isNaN(n)) return; if(min != null) n = Math.max(min, n); if(max != null) n = Math.min(max, n); saSet(path, n); }
function saToggle(path){ saSet(path, !saGet(path)); render(); }
/* 글자만 바꾸는 동안은 전체를 다시 그리지 않고(입력 포커스가 날아감) 위 띠의 버튼 상태만 갱신 */
function saHeader(){
  var d = saDirty();
  var b = document.getElementById("sa-save"); if(b) b.disabled = !d;
  var s = document.getElementById("sa-state"); if(s) s.textContent = d ? "고친 내용이 있습니다 — 초안 저장을 누르세요" : saSavedText();
}
function saSavedText(){
  if(!SA.savedAt) return "저장한 초안 없음 (지금 보이는 판에서 시작)";
  return "초안 저장됨 · " + saWhen(SA.savedAt) + (SA.savedBy ? " · " + SA.savedBy : "");
}
function saWhen(iso){ var d = new Date(iso); return (d.getMonth()+1) + "/" + d.getDate() + " " + pad(d.getHours()) + ":" + pad(d.getMinutes()); }

/* ---------- 서버에 쓰기 ---------- */
async function saSave(quiet){
  if(!SA || !SA.draft) return false;
  try{
    var key = view.storeKey || "hanok";
    await sb("/rest/v1/site_draft?on_conflict=store", { method:"POST", body:{ store:key, data:SA.draft, by:(SESSION && SESSION.who) || "" }, prefer:"resolution=merge-duplicates,return=minimal" });
    SA.saved = JSON.stringify(SA.draft); SA.savedAt = new Date().toISOString(); SA.savedBy = (SESSION && SESSION.who) || "";
    if(!quiet) showToast("초안을 저장했습니다");
    saHeader(); return true;
  }catch(e){ await uiAlert("초안 저장 실패", e.message, "warn"); return false; }
}
/* 미리보기: 초안을 먼저 저장하고(사이트가 서버 초안을 읽으니까) 사이트를 덮개 안에 띄움 */
async function saPreview(page){
  if(saDirty() && !await saSave(true)) return;
  view.saPreview = page || view.saPreview || "index";
  render();
}
function saPreviewClose(){ view.saPreview = null; render(); }
function saPreviewUrl(page){ return saRoot() + (page || "index") + ".html?preview=1&v=" + Date.now(); }
/* 적용: 지금 바로 / 날짜·시각 정해서 */
async function saApply(){
  if(!SA || !SA.draft) return;
  if(saDirty() && !await saSave(true)) return;
  view.saApply = { mode:"now", date:shiftDate(todayStr(), 1), time:"00:00", note:"" };
  render();
}
function saApplyClose(){ view.saApply = null; render(); }
function saApplySet(k, v){ if(view.saApply){ view.saApply[k] = v; if(k === "mode") render(); } }
/* 적용 대화창 — 지금 바로 / 정한 시각부터(일괄). 팝업 하나만 나중에 띄우려면 팝업의 시작일을 쓰는 게 낫습니다(글 전체를 예약하는 것이 아니라) */
function saApplyHtml(){
  var a = view.saApply, fut = (SA.versions || []).filter(function(v){ return new Date(v.apply_at).getTime() > Date.now(); });
  return '<div class="overlay" onclick="saApplyClose()"><div class="sheet" onclick="event.stopPropagation()">' +
    '<div class="sheet-h"><h2>홈페이지에 적용</h2><button class="x" onclick="saApplyClose()" aria-label="닫기">×</button></div>' +
    '<p class="f-note" style="margin:-8px 0 12px">지금 초안 전체(글·팝업·차림·사진·예약 규칙)가 한 판으로 나갑니다. 이전 판은 남아 있어 되돌릴 수 있습니다.</p>' +
    '<div class="seg"><button class="' + (a.mode === "now" ? "on" : "") + '" onclick="saApplySet(\'mode\', \'now\')">지금 바로</button><button class="' + (a.mode === "at" ? "on" : "") + '" onclick="saApplySet(\'mode\', \'at\')">정한 시각부터</button></div>' +
    (a.mode === "at" ? '<div class="grid2" style="margin-top:12px"><label class="f"><div class="lb">날짜</div><input type="date" value="' + esc(a.date) + '" onchange="saApplySet(\'date\', this.value)"></label><label class="f"><div class="lb">시각</div><input type="time" value="' + esc(a.time) + '" onchange="saApplySet(\'time\', this.value)"></label></div>' +
      '<p class="f-note" style="margin:-4px 0 12px">그 시각까지는 지금 판이 그대로 보이고, 시각이 되면 이 판으로 바뀝니다. 팝업 하나만 나중에 띄우는 거면 팝업의 시작일로 하는 게 간단합니다.</p>' : '') +
    (fut.length ? '<div class="alert amber" style="margin:8px 0"><span class="ic">!</span><div><div class="a-t">예약해 둔 판이 ' + fut.length + '건 있습니다</div><div class="a-s">' + fut.map(function(v){ return saWhen(v.apply_at) + (v.note ? " · " + esc(v.note) : ""); }).join(", ") + ' — 그 시각이 되면 그 판이 이 판을 덮습니다. 필요 없으면 적용 기록에서 취소하세요.</div></div></div>' : '') +
    '<label class="f" style="margin-top:12px"><div class="lb">메모 (선택)</div><input type="text" class="in-sm" placeholder="예: 추석 팝업, 가을 메뉴" value="' + esc(a.note) + '" oninput="saApplySet(\'note\', this.value)"></label>' +
    '<div class="sheet-actions btn-row"><button class="btn ghost" onclick="saApplyClose()">취소</button><button class="btn primary" data-enter onclick="saApplyDo()" style="margin-left:auto">' + (a.mode === "at" ? "이 시각에 적용" : "지금 적용") + '</button></div>' +
    '</div></div>';
}
async function saApplyDo(){
  var a = view.saApply; if(!a) return;
  var at = new Date(), when = a.mode === "at" ? 1 : 0, d = a.date, t = a.time, note = (a.note || "").trim();
  if(when === 1){
    if(!/^\d{4}-\d{2}-\d{2}$/.test(d || "") || !/^\d{2}:\d{2}$/.test(t || "")){ await uiAlert("날짜와 시각을 고르세요", "", "warn"); return; }
    at = new Date(d + "T" + t + ":00");
    if(isNaN(at.getTime())){ await uiAlert("날짜·시각 오류", d + " " + t, "warn"); return; }
    if(at.getTime() < Date.now()){ await uiAlert("지난 시각입니다", "지금 바로 적용하려면 '지금 바로' 를 고르세요.", "warn"); return; }
  }
  view.saApply = null;
  try{
    var key = view.storeKey || "hanok";
    await sb("/rest/v1/site_versions", { method:"POST", body:{ store:key, data:SA.draft, apply_at:at.toISOString(), note:note, by:(SESSION && SESSION.who) || "" }, prefer:"return=minimal" });
    logEvent("홈페이지 적용", (when === 1 ? "예약 " + d + " " + t : "지금") + (note ? " · " + note : ""));
    showToast(when === 1 ? "예약해 두었습니다 · " + d + " " + t : "홈페이지에 적용했습니다");
    SA.loading = true; render(); await saLoad(); render();
  }catch(e){ await uiAlert("적용 실패", e.message, "warn"); }
}
/* 예약해 둔(미래) 판 취소 */
async function saCancelVersion(id){
  var v = (SA.versions || []).filter(function(x){ return x.id === id; })[0]; if(!v) return;
  if(!await uiConfirm("예약 적용을 취소할까요?", saWhen(v.apply_at) + (v.note ? " · " + v.note : ""), {ok:"취소하기", cancel:"두기"})) return;
  try{ await sb("/rest/v1/site_versions?id=eq." + id, {method:"DELETE", prefer:"return=minimal"}); logEvent("홈페이지 예약 적용 취소", String(id)); SA.loading = true; render(); await saLoad(); render(); }
  catch(e){ await uiAlert("취소 실패", e.message, "warn"); }
}
/* 이전 판을 초안으로 가져오기 (되돌리기는 그 뒤 '적용') */
async function saRestore(id){
  try{
    var rows = await sb("/rest/v1/site_versions?id=eq." + id + "&select=id,data,apply_at,note");
    if(!rows[0]) return;
    if(saDirty() && !await uiConfirm("고치던 초안을 버릴까요?", "이전 판을 가져오면 지금 초안은 사라집니다.", {ok:"버리고 가져오기", cancel:"그대로"})) return;
    SA.draft = saMerge(SA.defaults, rows[0].data); render();
    showToast("가져왔습니다 · 확인하고 '적용' 을 누르세요");
  }catch(e){ await uiAlert("가져오기 실패", e.message, "warn"); }
}
/* 초안을 지금 보이는 판으로 되돌림 */
async function saDiscard(){
  if(!await uiConfirm("고친 내용을 버릴까요?", "지금 홈페이지에 보이는 판으로 초안을 되돌립니다.", {ok:"버리기", cancel:"계속 편집"})) return;
  SA.draft = saMerge(SA.defaults, SA.live ? SA.live.data : {}); render(); saHeader();
}
function saTab(t){ SA.tab = t; render(); }
/* 배열 항목 추가·삭제·이동 */
function saArrAdd(path, item){ var a = saGet(path) || []; a.push(item); saSet(path, a); render(); }
async function saArrDel(path, i, what){ if(what && !await uiConfirm(what + " 삭제", "지울까요?", {ok:"삭제", cancel:"취소"})) return; var a = saGet(path) || []; a.splice(i, 1); saSet(path, a); render(); }
function saArrMove(path, i, d){ var a = saGet(path) || [], j = i + d; if(j < 0 || j >= a.length) return; var x = a[i]; a[i] = a[j]; a[j] = x; saSet(path, a); render(); }
/* 사진 주소: img/ 파일명 또는 전체 주소 → 보이는 주소 */
function saImg(x){ if(!x) return ""; return /^(https?:)?\/\//.test(x) || /^data:/.test(x) ? x : saRoot() + "img/" + x; }

/* ---------- 입력 조각 ---------- */
function saF(path, label, note, opt){   /* 한 줄 글 */
  opt = opt || {}; var v = saGet(path); if(v == null) v = "";
  return '<label class="f sa-f"><div class="lb">' + esc(label) + '</div><input type="text" class="in-sm" value="' + esc(v) + '" placeholder="' + esc(opt.ph || "") + '" oninput="saSet(\'' + path + '\', this.value)">' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</label>';
}
function saT(path, label, note, rows){   /* 여러 줄 글 (줄바꿈 그대로) */
  var v = saGet(path); if(v == null) v = "";
  return '<label class="f sa-f"><div class="lb">' + esc(label) + '</div><textarea class="in-sm" rows="' + (rows || 3) + '" oninput="saSet(\'' + path + '\', this.value)">' + esc(v) + '</textarea>' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</label>';
}
function saL(path, label, note, rows){   /* 줄마다 하나 → 배열 */
  var v = saGet(path); if(!Array.isArray(v)) v = [];
  return '<label class="f sa-f"><div class="lb">' + esc(label) + ' <span class="lbl-note">한 줄에 하나</span></div><textarea class="in-sm" rows="' + (rows || Math.max(3, v.length + 1)) + '" oninput="saSetLines(\'' + path + '\', this.value)">' + esc(v.join("\n")) + '</textarea>' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</label>';
}
function saN(path, label, min, max, unit, note){   /* 숫자 */
  var v = saGet(path); if(v == null) v = "";
  return '<label class="f sa-f sa-num"><div class="lb">' + esc(label) + '</div><div class="sa-numrow"><input type="number" class="in-sm" value="' + esc(v) + '" min="' + min + '" max="' + max + '" onchange="saSetNum(\'' + path + '\', this.value, ' + min + ', ' + max + '); this.value = saGet(\'' + path + '\')">' + (unit ? '<span>' + esc(unit) + '</span>' : '') + '</div>' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</label>';
}
function saD(path, label, note){   /* 날짜 — 기기 달력으로 */
  var v = saGet(path); if(v == null) v = "";
  return '<label class="f sa-f"><div class="lb">' + esc(label) + '</div><input type="date" class="in-sm" value="' + esc(v) + '" onchange="saSet(\'' + path + '\', this.value); render()">' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</label>';
}
function saI(path, label, note){   /* 사진: 작은 보기 + 파일명/주소 + 올리기 */
  var v = saGet(path); if(v == null) v = "";
  return '<div class="f sa-f sa-img"><div class="lb">' + esc(label) + '</div><div class="sa-imgrow"><div class="sa-thumb">' + (v ? '<img src="' + esc(saImg(v)) + '" alt="" onerror="this.parentNode.classList.add(\'bad\')">' : '') + '</div><input type="text" class="in-sm" value="' + esc(v) + '" placeholder="img/ 파일명 또는 https:// 주소" oninput="saSet(\'' + path + '\', this.value)" onchange="render()"><button class="btn sm" onclick="saPickFile(\'image\', function(u){ saSet(\'' + path + '\', u); render(); })">올리기</button></div>' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</div>';
}
function saFile(path, label, note){   /* PDF 같은 파일: 주소 + 올리기 */
  var v = saGet(path); if(v == null) v = "";
  return '<div class="f sa-f"><div class="lb">' + esc(label) + '</div><div class="sa-imgrow"><input type="text" class="in-sm" value="' + esc(v) + '" oninput="saSet(\'' + path + '\', this.value)"><button class="btn sm" onclick="saPickFile(\'pdf\', function(u){ saSet(\'' + path + '\', u); render(); })">올리기</button></div>' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</div>';
}

/* ---------- 파일 올리기 (Storage 'site' 버킷, 공개 읽기·직원만 쓰기) ----------
   kind: image(축소해서 JPEG/PNG) · pdf · video(mp4 그대로) · file(소식 첨부 — 종류 안 가림, 14차). 올린 뒤 공개 주소(와 원래 파일 이름)를 cb 로 돌려줍니다.
   사진은 올리기 전에 긴 변 1600px 로 줄입니다 — 폰 사진 원본(4~8MB)을 그대로 두면 홈페이지가 느리고 무료 전송량(월 5GB)이 금방 찹니다 */
var SA_PICK = null;
function saPickFile(kind, cb){
  if(!supaOn() || !SESSION){ uiAlert("서버 연결이 필요합니다", "", "warn"); return; }
  var inp = document.getElementById("sa-file");
  if(!inp){ inp = document.createElement("input"); inp.type = "file"; inp.id = "sa-file"; inp.style.display = "none"; document.body.appendChild(inp); inp.addEventListener("change", saFileChosen); }
  inp.accept = kind === "image" ? "image/*" : kind === "pdf" ? "application/pdf" : kind === "file" ? "" : "video/mp4,video/*";
  inp.value = ""; SA_PICK = {kind:kind, cb:cb}; inp.click();
}
async function saFileChosen(e){
  var f = e.target.files && e.target.files[0], p = SA_PICK; SA_PICK = null;
  if(!f || !p) return;
  try{
    showToast("올리는 중… " + f.name);
    var blob = f, ext = (f.name.split(".").pop() || "").toLowerCase(), type = f.type || "";
    if(p.kind === "image"){ var r = await saShrink(f); blob = r.blob; ext = r.ext; type = r.type; }
    else if(p.kind === "pdf"){ if(type !== "application/pdf" && ext !== "pdf") throw new Error("PDF 파일만 올릴 수 있습니다"); type = "application/pdf"; ext = "pdf"; }
    else if(p.kind === "video"){ if(!/mp4|quicktime|video\//.test(type) && ext !== "mp4") throw new Error("MP4 영상만 올릴 수 있습니다"); if(ext !== "mp4") throw new Error("MP4(H.264) 로 바꿔서 올려 주세요 — 구형 TV 는 다른 형식을 못 틉니다"); type = "video/mp4"; }
    else if(p.kind === "file"){ if(!type) type = "application/octet-stream"; if(!ext) ext = "bin"; }   /* 한글(hwp) 같은 건 브라우저가 종류를 모름 → 그냥 파일 */
    if(blob.size > 50 * 1024 * 1024) throw new Error("50MB 를 넘습니다 (" + Math.round(blob.size / 1048576) + "MB)");
    var safe = f.name.replace(/\.[^.]+$/, "").replace(/[^0-9A-Za-z_-]+/g, "_").replace(/^_+|_+$/g, "").slice(0, 40) || "file";   /* Storage 는 한글 키를 거부합니다("Invalid key") — 영문·숫자만 */
    var path = (view.storeKey || "hanok") + "/" + p.kind + "/" + Date.now().toString(36) + "_" + safe + "." + ext;
    var res = await fetch(SUPA_CFG.url + "/storage/v1/object/site/" + path, { method:"POST", headers:{ "apikey":SUPA_CFG.anonKey, "Authorization":"Bearer " + SESSION.access_token, "Content-Type":type, "x-upsert":"true", "Cache-Control":"max-age=31536000" }, body:blob });
    if(!res.ok){ var t = ""; try{ t = (await res.json()).message || ""; }catch(x){} throw new Error("올리기 실패 " + res.status + (t ? " · " + t : "")); }
    var url = SUPA_CFG.url + "/storage/v1/object/public/site/" + path;
    logEvent("파일 올림", p.kind + " " + f.name + " → " + path);
    showToast("올렸습니다 · " + Math.round(blob.size / 1024) + "KB");
    p.cb(url, f.name);
  }catch(err){ await uiAlert("올리지 못했습니다", err.message || String(err), "warn"); }
}
/* 사진 줄이기: 긴 변 1600px, JPEG 0.85. PNG(투명 배경 — 주방장 사진 같은 것)는 PNG 로 둡니다 */
function saShrink(file){
  return new Promise(function(resolve, reject){
    var isPng = /png$/i.test(file.type) || /\.png$/i.test(file.name);
    var img = new Image(), url = URL.createObjectURL(file);
    img.onload = function(){
      try{
        var MAX = 1600, w = img.naturalWidth, h = img.naturalHeight, k = Math.min(1, MAX / Math.max(w, h));
        var cw = Math.round(w * k), ch = Math.round(h * k);
        if(k >= 1 && file.size < 600 * 1024){ URL.revokeObjectURL(url); resolve({blob:file, ext:isPng ? "png" : (file.name.split(".").pop() || "jpg").toLowerCase(), type:file.type || (isPng ? "image/png" : "image/jpeg")}); return; }
        var c = document.createElement("canvas"); c.width = cw; c.height = ch;
        c.getContext("2d").drawImage(img, 0, 0, cw, ch);
        c.toBlob(function(b){ URL.revokeObjectURL(url); if(!b) reject(new Error("사진을 줄이지 못했습니다")); else resolve({blob:b, ext:isPng ? "png" : "jpg", type:isPng ? "image/png" : "image/jpeg"}); }, isPng ? "image/png" : "image/jpeg", 0.85);
      }catch(e){ reject(e); }
    };
    img.onerror = function(){ URL.revokeObjectURL(url); reject(new Error("사진 파일을 열 수 없습니다")); };
    img.src = url;
  });
}
function saBox(title, inner, extra){ return '<section class="card sa-box"><div class="sa-box-h"><b>' + esc(title) + '</b>' + (extra || "") + '</div>' + inner + '</section>'; }

/* ---------- 화면 ---------- */
function saHead(){ return (view.form && view.form.page) ? "" : sheetHead("홈페이지 관리"); }   /* 화면형은 상단바에 제목이 있어 겹치지 않게(검토 2026-09-17) */
function sheetSite(){
  if(!SA || SA.loading) return saHead() + '<p class="muted" style="padding:20px 0">불러오는 중…</p>';
  if(SA.err) return saHead() + '<div class="alert rust"><span class="ic">!</span><div><div class="a-t">불러오지 못했습니다</div><div class="a-s">' + esc(SA.err) + '</div></div></div><div class="btn-row" style="margin-top:12px"><button class="btn" onclick="openSiteAdmin()">다시 시도</button></div>';
  var TABS = [["online","홈페이지 예약"],["notices","팝업 공지"],["posts","소식"],["hours","영업시간·연락처"],["texts","글"],["menu","차림"],["images","사진"],["history","적용 기록"]];
  var future = (SA.versions || []).filter(function(v){ return new Date(v.apply_at).getTime() > Date.now(); });
  var body = ({online:saTabOnline, notices:saTabNotices, posts:saTabPosts, hours:saTabHours, texts:saTabTexts, menu:saTabMenu, images:saTabImages, history:saTabHistory}[SA.tab] || saTabOnline)();   /* posts 는 14c */
  return saHead() +
    '<div class="sa-top">' +
      '<div class="sa-status"><span id="sa-state">' + (saDirty() ? "고친 내용이 있습니다 — 초안 저장을 누르세요" : saSavedText()) + '</span>' +
        '<span class="muted">지금 홈페이지: ' + (SA.live ? saWhen(SA.live.apply_at) + " 판" + (SA.live.note ? ' · ' + esc(SA.live.note) : '') : "기본값(적용한 판 없음)") + (future.length ? ' · <b class="sa-fut">예약 ' + future.length + '건</b>' : '') + '</span></div>' +
      '<div class="btn-row sa-acts">' +
        '<button class="btn" id="sa-save" onclick="saSave()" ' + (saDirty() ? "" : "disabled") + '>초안 저장</button>' +
        '<button class="btn" onclick="saPreview()">미리보기</button>' +
        '<button class="btn primary" onclick="saApply()">적용…</button>' +
        '<button class="btn ghost" onclick="saDiscard()" title="초안을 지금 보이는 판으로">고친 것 버리기</button>' +
      '</div>' +
    '</div>' +
    '<div class="sa-tabs">' + TABS.map(function(t){ return '<button class="' + (SA.tab === t[0] ? "on" : "") + '" onclick="saTab(\'' + t[0] + '\')">' + t[1] + (t[0] === "history" && future.length ? '<i class="cnt">' + future.length + '</i>' : '') + '</button>'; }).join("") + '</div>' +
    '<div class="sa-body">' + body + '</div>' +
    (view.saPreview ? saPreviewHtml() : "") + (view.saApply ? saApplyHtml() : "");
}
function saPreviewHtml(){
  var PAGES = [["index","홈"],["about","이야기"],["space","공간"],["menu","차림"],["news","소식"],["visit","오시는 길"],["reserve","예약"]];
  return '<div class="sa-pv"><div class="sa-pv-h"><b>미리보기 — 초안</b>' +
    '<div class="sa-pv-pages">' + PAGES.map(function(p){ return '<button class="' + (view.saPreview === p[0] ? "on" : "") + '" onclick="saPreview(\'' + p[0] + '\')">' + p[1] + '</button>'; }).join("") + '</div>' +
    '<a class="btn sm" href="' + saPreviewUrl(view.saPreview) + '" target="_blank" rel="noopener">새 창</a><button class="btn sm ghost" onclick="saPreviewClose()">닫기</button></div>' +
    '<iframe src="' + saPreviewUrl(view.saPreview) + '" title="홈페이지 미리보기"></iframe></div>';
}

/* 1. 홈페이지 예약 */
function saTabOnline(){
  var on = saGet("online.enabled") !== false;
  var closed = saGet("closed") || [];
  return saBox("접수",
      '<button class="togglebtn ' + (on ? "on" : "sa-off") + '" onclick="saToggle(\'online.enabled\')">' + (on ? "홈페이지 예약을 받고 있습니다" : "홈페이지 예약 중단 — 전화 안내만") + '</button>' +
      '<p class="f-note">끄면 홈페이지 예약 창이 아래 안내만 보여줍니다. 이미 접수된 요청은 그대로 남습니다. 적용해야 반영됩니다.</p>' +
      saF("online.offTitle", "중단 안내 제목") + saT("online.offMsg", "중단 안내 문구", "", 2)) +
    saBox("규칙",
      '<div class="grid2">' +
      saN("online.maxDays", "며칠 앞까지 받나", 1, 30, "일", "최대 30일 — 시스템이 남은 자리를 30일치만 올립니다. 당일은 항상 전화(서버 규칙)") +
      saN("online.minAdults", "성인 몇 명부터", 2, 12, "명") +
      saN("online.maxPeople", "총 몇 명까지", 2, 12, "명", "넘으면 전화 안내") +
      saN("online.roomMinAdults", "룸은 성인 몇 명부터", 5, 12, "명") +
      saN("online.limitMin", "시간 고른 뒤 몇 분 안에", 3, 15, "분") +
      '</div><p class="f-note">서버가 성인 2~12명 · 룸 성인 5명 · 내일부터를 최종으로 확인합니다. 여기서는 그 안에서 좁히기만 됩니다. 더 넓히려면 재아에게(서버 정책).</p>') +
    saBox("홈페이지 예약 안 받는 날",
      '<div class="sa-chips">' + closed.slice().sort().map(function(d, i){ return '<span class="tag">' + esc(d) + '<button onclick="saArrDel(\'closed\', ' + closed.indexOf(d) + ')" title="빼기">×</button></span>'; }).join("") + (closed.length ? "" : '<span class="muted">없음</span>') + '</div>' +
      '<div class="btn-row" style="margin-top:8px"><input type="date" id="sa-closed-date" style="flex:1 1 160px"><button class="btn" onclick="(function(){ var el=document.getElementById(\'sa-closed-date\'); if(!el.value) return; var a=saGet(\'closed\')||[]; if(a.indexOf(el.value)<0) a.push(el.value); saSet(\'closed\', a); render(); })()">추가</button></div>' +
      '<p class="f-note">그날은 예약 창에 시각이 안 나옵니다(전화는 그대로). 영업 자체를 쉬는 날은 설정 → 운영시간 → 임시 영업·휴무.</p>') +
    saBox("특별 기간 차림 (명절 등)",
      (saGet("online.special") || []).map(function(sp, i){ var p = "online.special." + i; return '<div class="sa-box-in">' +
        '<div class="grid3"><label class="f"><div class="lb">이름</div><input type="text" class="in-sm" value="' + esc(sp.title || "") + '" placeholder="예: 추석 연휴 코스" oninput="saSet(\'' + p + '.title\', this.value)"></label>' +
        '<label class="f"><div class="lb">시작일</div><input type="date" class="in-sm" value="' + esc(sp.from || "") + '" onchange="saSet(\'' + p + '.from\', this.value)"></label><label class="f"><div class="lb">마감일</div><input type="date" class="in-sm" value="' + esc(sp.to || "") + '" onchange="saSet(\'' + p + '.to\', this.value)"></label></div>' +
        '<label class="f"><div class="lb">이 기간의 코스 <span class="lbl-note">한 줄에 하나 · "이름 | 한자" 가능 · 홈페이지 예약 창에는 이것만 나옴</span></div><textarea class="in-sm" rows="3" oninput="saSetLines(\'' + p + '.courses\', this.value)">' + esc((sp.courses || []).join("\n")) + '</textarea></label>' +
        '<label class="f"><div class="lb">안내 한 줄 <span class="lbl-note">예약 창 메뉴 단계에 보임</span></div><input type="text" class="in-sm" value="' + esc(sp.note || "") + '" oninput="saSet(\'' + p + '.note\', this.value)"></label>' +
        '<div class="btn-row"><button class="btn sm ghost" onclick="saArrDel(\'online.special\', ' + i + ', \'특별 기간\')">삭제</button></div></div>'; }).join("") +
      '<div class="btn-row"><button class="btn sm" onclick="saArrAdd(\'online.special\', {title:\'\', from:\'\', to:\'\', courses:[], note:\'\'})">＋ 특별 기간</button></div>' +
      '<p class="f-note">명절처럼 차림이 다른 기간. 그 기간 날짜를 고르면 홈페이지 예약 창의 메뉴 단계에 <b>여기 적은 코스만</b> 나오고(점심 세트·단품 없음) 안내 한 줄이 붙습니다. 시스템 쪽 코스 구성은 설정 → 코스·세트 구성에서 "날짜를 정해서(예정)" 로 같은 기간을 넣어 두세요.</p>') +
    saBox("예약 페이지 안내 문구",
      saF("reserve.head.sub", "위 소개 한 줄") +
      (saGet("reserve.notes") || []).map(function(n, i){ return '<div class="sa-row"><input type="text" class="in-sm sa-k" value="' + esc(n.b) + '" oninput="saSet(\'reserve.notes.' + i + '.b\', this.value)"><input type="text" class="in-sm" value="' + esc(n.s) + '" oninput="saSet(\'reserve.notes.' + i + '.s\', this.value)"><button class="btn sm ghost" onclick="saArrDel(\'reserve.notes\', ' + i + ')">×</button></div>'; }).join("") +
      '<div class="btn-row"><button class="btn sm" onclick="saArrAdd(\'reserve.notes\', {b:\'\', s:\'\'})">줄 추가</button></div>' +
      saF("reserve.go.lead", "'예약하기' 상자 안내") + saF("reserve.go.cap", "버튼 아래 작은 글"));
}
/* 2. 팝업 공지 */
function saTabNotices(){
  var list = saGet("notices") || [];
  return '<p class="f-note" style="margin:0 0 12px">홈페이지 첫 화면에 겹쳐 뜨는 알림창입니다. 마감일이 지나면 저절로 안 뜹니다. 손님이 닫으면 그 세션 동안, "오늘 하루 보지 않기" 면 그날 안 뜹니다.</p>' +
    list.map(function(n, i){
      var p = "notices." + i + ".", off = n.until && n.until < todayStr(), soon = n.from && n.from > todayStr();
      return saBox((n.title || "(제목 없음)") + (off ? " · 마감 지남" : soon ? " · " + n.from + " 부터" : ""),
        saF(p + "title", "제목") +
        '<div class="grid2">' + saD(p + "from", "시작일", "비우면 바로") + saD(p + "until", "마감일", "비우면 계속. 이 날까지 뜸") + '</div>' +
        saL(p + "lines", "내용", "문단마다 한 줄", 4) +
        '<div class="grid2">' + saF(p + "button", "버튼 글", "비우면 버튼 없음. 버튼은 예약 창을 엽니다") + saI(p + "img", "그림 팝업", "적으면 글 대신 그림 한 장") + '</div>' +
        '<div class="grid3">' + saN(p + "x", "왼쪽에서", 0, 1200, "px") + saN(p + "y", "위에서", 0, 800, "px") + saN(p + "w", "폭", 240, 640, "px") + '</div>',
        '<span class="sa-box-x"><button class="btn sm ghost" onclick="saArrMove(\'notices\', ' + i + ', -1)">↑</button><button class="btn sm ghost" onclick="saArrMove(\'notices\', ' + i + ', 1)">↓</button><button class="btn sm ghost" onclick="saArrDel(\'notices\', ' + i + ', \'팝업\')">삭제</button></span>');
    }).join("") +
    '<div class="btn-row"><button class="btn" onclick="saArrAdd(\'notices\', {id:\'n\' + Date.now().toString(36), from:\'\', until:\'\', x:40 + 30 * ' + list.length + ', y:110 + 30 * ' + list.length + ', w:380, title:\'\', lines:[], button:\'예약하기\'})">팝업 추가</button></div>';
}
/* 3. 영업시간·연락처 */
function saTabHours(){
  var hours = saGet("hours") || [];
  return saBox("영업시간 (홈페이지 표시용)",
      hours.map(function(h, i){ return '<div class="sa-row"><input type="text" class="in-sm sa-k" value="' + esc(h.day) + '" placeholder="월 – 토" oninput="saSet(\'hours.' + i + '.day\', this.value)"><input type="text" class="in-sm" value="' + esc(h.open) + '" placeholder="11:00 – 22:00" oninput="saSet(\'hours.' + i + '.open\', this.value)"><button class="btn sm ghost" onclick="saArrDel(\'hours\', ' + i + ')">×</button></div>'; }).join("") +
      '<div class="btn-row"><button class="btn sm" onclick="saArrAdd(\'hours\', {day:\'\', open:\'\'})">줄 추가</button></div>' +
      saL("hoursNote", "아래 작은 글", "브레이크·라스트오더 같은 것") +
      '<p class="f-note"><b>홈페이지에 보이는 글자</b>일 뿐, 예약 시스템 운영시간과 연결돼 있지 않습니다. 운영시간을 바꾸면(설정 → 운영시간) 여기 글도 직접 고쳐 주세요. 예약 창의 시각 칸은 시스템 운영시간을 따릅니다.</p>') +
    saBox("연락처·주소",
      '<div class="grid2">' + saF("info.tel", "전화") + saF("info.parking", "주차 한 줄") + '</div>' +
      saF("info.addr", "주소 (한 줄)") + saT("info.addr2", "주소 (두 줄 표시)", "홈·오시는 길에 두 줄로 나올 때", 2) +
      '<div class="grid2">' + saF("info.owner", "대표") + saF("info.bizno", "사업자등록번호") + '</div>' +
      saL("info.services", "이용 안내 알약", "홈 소개 아래·오시는 길에 한 줄로. 예: 콜키지 가능 · 병당 20,000원 / 단체 이용 가능 / 포장 가능 / 배달 가능", 4)) +
    saBox("링크",
      saF("info.naverMap", "네이버 지도") + saF("info.kakaoMap", "카카오맵") + saF("info.instagram", "인스타그램") + saF("info.blog", "블로그") +
      saFile("info.menuPdf", "메뉴판 PDF", "파일명(menu.pdf) 또는 올린 파일 주소. '올리기' 로 새 PDF 를 올리면 주소가 채워집니다")) +
    saBox("공휴일 (예약 창 시각 계산용)", saL("holidays", "공휴일", "YYYY-MM-DD 한 줄에 하나. 일요일 시간으로 봅니다", 6));
}
/* 4. 글 */
function saTabTexts(){
  return saBox("홈 (첫 화면)",
      saF("home.heroTitle", "큰 제목") + saF("home.heroSub", "제목 아래 한 줄") +
      saT("home.intro.title", "소개 제목", "줄바꿈 그대로", 2) + saL("home.intro.paras", "소개 글", "문단마다 한 줄. **굵게** 가능") +
      '<div class="grid2">' + saF("home.menuSec.lead", "차림 소개") + saF("home.spaceSec.lead", "공간 소개") + '</div>' +
      saF("home.infoSec.telNote", "연락 아래 한 줄") + saL("home.band.lines", "예약 띠 문구", "", 2)) +
    saBox("이야기",
      saF("about.head.sub", "위 소개 한 줄") +
      '<div class="grid2">' + saF("about.greeting.by", "인사말 — 누구") + saF("about.greeting.sign", "서명") + '</div>' +
      saL("about.greeting.paras", "인사말", "문단마다 한 줄. **굵게** 가능", 7) +
      '<div class="grid2">' + saF("about.chef.name", "주방장 이름") + saF("about.chef.who", "주방장 소개 한 줄") + '</div>' +
      saT("about.chef.quote", "주방장 한마디", "줄바꿈 그대로", 2) + saT("about.chef.para", "주방장 소개 글", "", 3) +
      saT("about.story.title", "집 이야기 제목", "", 2) + saF("about.story.sub", "제목 아래") + saL("about.story.paras", "집 이야기", "", 5)) +
    saBox("공간 · 차림 · 오시는 길",
      saF("space.head.sub", "공간 — 위 소개") +
      saF("menuPage.head.sub", "차림 — 위 소개") +
      '<div class="grid2">' + saF("menuPage.chefBand.who", "차림 — 주방장 띠") + saF("menuPage.chefBand.quote", "차림 — 주방장 한마디") + '</div>' +
      '<div class="grid2">' + saF("menuPage.courses.sub", "저녁 코스 아래 글") + saF("menuPage.lunch.sub", "점심 세트 아래 글") + '</div>' +
      saF("visit.head.sub", "오시는 길 — 위 소개") + saL("visit.parking", "주차 안내", "", 3) + saL("visit.transit", "대중교통", "", 2));
}
/* 5. 차림 */
function saTabMenu(){
  var C = saGet("menu.courses.items") || [], L = saGet("menu.lunch") || [], D = saGet("menu.dishes") || [], DM = saGet("menu.dumplings.items") || [], DR = saGet("menu.drinks") || [];
  var itemLines = function(items, withTag){ return items.map(function(x){ return x.name + (withTag && x.tag ? " | " + x.tag : ""); }); };
  return '<p class="f-note" style="margin:0 0 12px">가격은 홈페이지에 안 나옵니다(메뉴판 PDF 에서만). 요리·만두는 이름만 보이고, 주류는 이름 뒤에 <b>|</b> 를 두고 적으면 작은 설명이 붙습니다 — 예: <code>소주 | 참이슬 · 처음처럼</code></p>' +
    saBox("저녁 코스",
      C.map(function(c, i){ var p = "menu.courses.items." + i + "."; return '<div class="sa-sub"><div class="grid2">' + saF(p + "name", "이름") + saF(p + "cn", "한자") + '</div>' + saL(p + "dishes", "구성", "", 4) + '<div class="btn-row"><button class="btn sm ghost" onclick="saArrMove(\'menu.courses.items\', ' + i + ', -1)">↑</button><button class="btn sm ghost" onclick="saArrMove(\'menu.courses.items\', ' + i + ', 1)">↓</button><button class="btn sm ghost" onclick="saArrDel(\'menu.courses.items\', ' + i + ', \'코스\')">삭제</button></div></div>'; }).join("") +
      '<div class="btn-row"><button class="btn sm" onclick="saArrAdd(\'menu.courses.items\', {name:\'\', cn:\'\', dishes:[]})">코스 추가</button></div>') +
    saBox("점심 세트",
      L.map(function(g, gi){ var gp = "menu.lunch." + gi + "."; return '<div class="sa-sub"><div class="grid2">' + saF(gp + "title", "묶음 이름") + saF(gp + "sub", "옆에 작게", "예: 토·일·공휴일") + '</div>' +
        (g.items || []).map(function(x, i){ var p = gp + "items." + i + "."; return '<div class="sa-sub2">' + saF(p + "name", "세트 이름") + saL(p + "dishes", "구성", "", 3) + '<div class="btn-row"><button class="btn sm ghost" onclick="saArrDel(\'' + gp + 'items\', ' + i + ', \'세트\')">세트 삭제</button></div></div>'; }).join("") +
        '<div class="btn-row"><button class="btn sm" onclick="saArrAdd(\'' + gp + 'items\', {name:\'\', dishes:[]})">세트 추가</button><button class="btn sm ghost" onclick="saArrDel(\'menu.lunch\', ' + gi + ', \'묶음\')">묶음 삭제</button></div></div>'; }).join("") +
      '<div class="btn-row"><button class="btn sm" onclick="saArrAdd(\'menu.lunch\', {title:\'\', sub:\'\', items:[]})">묶음 추가</button></div>') +
    saBox("요리",
      D.map(function(g, gi){ var gp = "menu.dishes." + gi + "."; return '<div class="sa-sub">' + saF(gp + "group", "분류") + saMenuLines(gp + "items", "메뉴", itemLines(g.items || []), false) + '<div class="btn-row"><button class="btn sm ghost" onclick="saArrMove(\'menu.dishes\', ' + gi + ', -1)">↑</button><button class="btn sm ghost" onclick="saArrMove(\'menu.dishes\', ' + gi + ', 1)">↓</button><button class="btn sm ghost" onclick="saArrDel(\'menu.dishes\', ' + gi + ', \'분류\')">분류 삭제</button></div></div>'; }).join("") +
      '<div class="btn-row"><button class="btn sm" onclick="saArrAdd(\'menu.dishes\', {group:\'\', items:[]})">분류 추가</button></div>') +
    saBox("만두", saMenuLines("menu.dumplings.items", "메뉴", itemLines(DM), false)) +
    saBox("주류",
      DR.map(function(g, gi){ var gp = "menu.drinks." + gi + "."; return '<div class="sa-sub">' + saF(gp + "group", "분류") + saMenuLines(gp + "items", "메뉴", itemLines(g.items || [], true), true) + '<div class="btn-row"><button class="btn sm ghost" onclick="saArrDel(\'menu.drinks\', ' + gi + ', \'분류\')">분류 삭제</button></div></div>'; }).join("") +
      '<div class="btn-row"><button class="btn sm" onclick="saArrAdd(\'menu.drinks\', {group:\'\', items:[]})">분류 추가</button></div>');
}
/* "이름 | 설명" 줄들 ↔ [{name, tag}] . 가격·용량(price·sizes)은 화면에 안 쓰지만 있던 항목은 이름이 같으면 그대로 붙여 둡니다 */
function saMenuLines(path, label, lines, withTag){
  return '<label class="f sa-f"><div class="lb">' + esc(label) + ' <span class="lbl-note">한 줄에 하나' + (withTag ? ' · 이름 | 설명' : '') + '</span></div><textarea class="in-sm" rows="' + Math.max(3, lines.length + 1) + '" oninput="saSetMenuLines(\'' + path + '\', this.value, ' + (withTag ? 'true' : 'false') + ')">' + esc(lines.join("\n")) + '</textarea></label>';
}
/* 줄 → 항목. withTag(주류)면 "이름 | 설명" 을 tag 로. 아니면(요리·만두) 이름만 받고, 있던 tag·price 는 이름이 같으면 그대로 둠(화면엔 안 나와도 자료로 남김) */
function saSetMenuLines(path, text, withTag){
  var old = saGet(path) || [];
  var items = String(text).split("\n").map(function(l){ return l.trim(); }).filter(function(l){ return l.length; }).map(function(l){
    var sp = withTag ? l.split("|") : [l], name = sp[0].trim(), tag = withTag ? sp.slice(1).join("|").trim() : null;
    var prev = old.filter(function(x){ return x.name === name; })[0];
    var it = prev ? deepClone(prev) : {name:name};
    it.name = name; if(withTag){ if(tag) it.tag = tag; else delete it.tag; }
    return it;
  });
  saSet(path, items);
}
/* 6. 사진 */
function saTabImages(){
  var slides = saGet("home.heroSlides") || [], tiles = saGet("home.spaceSec.tiles") || [], pics = saGet("about.story.pics") || [], rooms = saGet("rooms") || [], halls = saGet("halls") || [];
  return '<p class="f-note" style="margin:0 0 12px"><b>올리기</b>로 태블릿·폰의 사진을 고르면 줄여서(긴 변 1600px) 서버에 올라가고 칸에 주소가 들어갑니다. 파일명(img/ 폴더)이나 주소를 직접 적어도 됩니다.</p>' +
    saBox("홈 첫 화면 (넘어가는 사진)",
      slides.map(function(x, i){ return '<div class="sa-row">' + saI("home.heroSlides." + i, (i+1) + "번") + '<span class="sa-rowbtns"><button class="btn sm ghost" onclick="saArrMove(\'home.heroSlides\', ' + i + ', -1)">↑</button><button class="btn sm ghost" onclick="saArrMove(\'home.heroSlides\', ' + i + ', 1)">↓</button><button class="btn sm ghost" onclick="saArrDel(\'home.heroSlides\', ' + i + ')">×</button></span></div>'; }).join("") +
      '<div class="btn-row"><button class="btn sm" onclick="saArrAdd(\'home.heroSlides\', \'\')">사진 추가</button></div>') +
    saBox("홈",
      '<div class="grid2">' + saI("home.intro.img", "소개 옆 사진") + saI("home.menuSec.img", "차림 옆 사진") + saI("home.band.img", "예약 띠 배경") + '</div>' +
      '<div class="subhead">공간 타일 (첫 장이 넓게)</div><div class="grid2">' + tiles.map(function(t, i){ return saI("home.spaceSec.tiles." + i + ".img", (i+1) + "번"); }).join("") + '</div>') +
    saBox("이야기",
      '<div class="grid2">' + saI("about.head.img", "위 큰 사진") + saI("about.chef.img", "주방장 사진", "배경 없는 PNG 가 어울립니다") + pics.map(function(p, i){ return saI("about.story.pics." + i + ".img", "집 이야기 사진 " + (i+1)); }).join("") + '</div>') +
    saBox("공간 · 차림 · 오시는 길 · 예약",
      '<div class="grid2">' + saI("space.head.img", "공간 위 사진") + saI("menuPage.head.img", "차림 위 사진") + saI("menuPage.chefBand.img", "차림 주방장 띠") + saI("visit.head.img", "오시는 길 위 사진") + saI("reserve.head.img", "예약 위 사진") + '</div>') +
    saBox("룸 · 테이블",
      '<div class="grid2">' + rooms.map(function(r, i){ return saI("rooms." + i + ".img", r.name + " 룸"); }).join("") + halls.map(function(h, i){ return saI("halls." + i + ".img", h.name); }).join("") + '</div>' +
      '<p class="f-note">룸 이름·인원은 예약 시스템 설정을 따르는 게 맞지만 지금은 홈페이지 글이 따로입니다. 이름이 바뀌면 여기서도 고쳐 주세요.</p>' +
      '<div class="grid2">' + rooms.map(function(r, i){ return saF("rooms." + i + ".cap", r.name + " 인원"); }).join("") + '</div>');
}
/* 7. 적용 기록 */
function saTabHistory(){
  var now = Date.now();
  var rows = (SA.versions || []).map(function(v){
    var fut = new Date(v.apply_at).getTime() > now, cur = SA.live && SA.live.id === v.id;
    return '<div class="sa-ver ' + (fut ? "fut" : "") + (cur ? " cur" : "") + '"><div><b>' + saWhen(v.apply_at) + '</b>' + (fut ? ' <span class="tag amber">예약</span>' : cur ? ' <span class="tag pine">지금 보임</span>' : '') + (v.note ? ' <span>' + esc(v.note) + '</span>' : '') + '<div class="muted">' + saWhen(v.created_at) + ' 등록' + (v.by ? ' · ' + esc(v.by) : '') + '</div></div>' +
      '<div class="btn-row">' + (fut ? '<button class="btn sm" onclick="saCancelVersion(' + v.id + ')">예약 취소</button>' : '') + (cur ? '' : '<button class="btn sm" onclick="saRestore(' + v.id + ')">이 판을 초안으로</button>') + '</div></div>';
  }).join("");
  return '<p class="f-note" style="margin:0 0 12px">적용할 때마다 한 판씩 남습니다. 이전 판으로 돌아가려면 "이 판을 초안으로" → 확인 → 적용.</p>' + (rows || '<p class="muted">아직 적용한 판이 없습니다. 홈페이지는 기본값으로 보입니다.</p>');
}
