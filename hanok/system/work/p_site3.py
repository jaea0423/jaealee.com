# -*- coding: utf-8 -*-
"""홈페이지 관리 3단계 + 재아 요청(2026-09-16):
   ① 홈페이지 관리를 설정 안으로(더보기에서 빼고 설정에 '홈페이지' 묶음)
   ② 팝업 공지에 시작일(from) 추가
   ③ 적용 대화창을 진짜 날짜·시각 입력으로(글자 프롬프트 대신) — '일괄 언제부터'
   ④ 파일 올리기(사진·PDF·광고 영상): Storage 'site' 버킷. 광고 영상은 설정에서 '영상 올리기' 버튼으로 """
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep

# ---------- ① 설정 안으로 ----------
s = load("js/06-modal.js")
s = rep(s, '''              <button onclick="closeMore(); openSiteAdmin()">${ICON.site}<span>홈페이지 관리</span></button>
''', '', 1)
save("js/06-modal.js", s)

s = load("js/14-settings.js")
s = rep(s, '''    ${sec("hours","운영시간",`${hoursFor(todayStr()).open} ~ ${hoursFor(todayStr()).close}`, schedBody)}''',
'''    ${sec("site","홈페이지",`예약 접수 · 팝업 · 글 · 사진`, siteBody)}
    ${sec("hours","운영시간",`${hoursFor(todayStr()).open} ~ ${hoursFor(todayStr()).close}`, schedBody)}''', 1)
# siteBody 정의 — schedBody 정의 바로 앞에
s = rep(s, '''  /* ---------- 운영시간 ---------- */
  const schedBody = `''',
'''  /* ---------- 홈페이지 (손님이 보는 사이트) ---------- */
  const siteBody = `
    <p class="f-note" style="margin:0 0 12px">손님이 보는 홈페이지(jaealee.com/hanok)의 <b>예약 접수 켜고 끄기 · 팝업 공지 · 글 · 차림 · 사진 · 영업시간 표시</b>를 고칩니다.
      여기 설정과 달리 '적용' 을 누르는 즉시(또는 정한 시각부터) 홈페이지에 나갑니다. 미리보기로 먼저 확인할 수 있습니다.</p>
    <div class="btn-row"><button class="btn primary" onclick="openSiteAdmin()">홈페이지 관리 열기</button></div>`;

  /* ---------- 운영시간 ---------- */
  const schedBody = `''', 1)
# ④ 광고 영상: 파일 이름 입력 → 올리기 버튼
s = rep(s, '''    <input id="tv-ad" class="in-sm" value="${esc(st.tvAd||"")}" placeholder="ad.mp4"
      onchange="setPolicy('tvAd', this.value)">
    <p class="f-note">
      영상 파일을 <b>이 폴더에 같이 올려두고</b> 파일 이름만 적으면 됩니다 (예: <code>ad.mp4</code>).<br>
      · <b>H.264 (MP4)</b> 로 만드세요. 다른 형식은 구형 TV에서 안 나옵니다.<br>
      · 소리는 빼세요. 자동 재생이 막히고, 입구에서 소리가 나면 민폐입니다.<br>
      · 20~40초, 10MB 이하. 좌우가 잘리므로 <b>중요한 것은 가운데</b>에 두세요.<br>
      비워 두면 매장 사진이 천천히 넘어갑니다.</p>''',
'''    <div class="ub-row">
      <span class="grow" style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap">${st.tvAd ? `<a href="${esc(adUrl(st.tvAd))}" target="_blank" rel="noopener">${esc(st.tvAd.replace(/^.*\\//, ""))}</a>` : `<span class="muted">영상 없음 — 매장 사진이 넘어갑니다</span>`}</span>
      <button class="btn sm" onclick="saPickFile('video', function(url){ setPolicy('tvAd', url); })">영상 올리기</button>
      ${st.tvAd ? `<button class="btn sm ghost" onclick="setPolicy('tvAd', '')">비우기</button>` : ``}
    </div>
    <p class="f-note">
      태블릿·PC 에서 영상 파일을 고르면 서버에 올라가고 TV 가 그걸 틉니다(적용하기를 눌러야 바뀜).<br>
      · <b>H.264 (MP4)</b> 로 만드세요. 다른 형식은 구형 TV에서 안 나옵니다. 50MB 까지.<br>
      · 소리는 빼세요. 자동 재생이 막히고, 입구에서 소리가 나면 민폐입니다.<br>
      · 20~40초. 좌우가 잘리므로 <b>중요한 것은 가운데</b>에 두세요.</p>''', 1)
save("js/14-settings.js", s)

# ---------- ② ③ ④ 관리 화면 ----------
s = load("js/14b-site-admin.js")
# ② 팝업 시작일
s = rep(s, '''      var p = "notices." + i + ".", off = n.until && n.until < todayStr();
      return saBox((n.title || "(제목 없음)") + (off ? " · 마감 지남" : ""),
        '<div class="grid2">' + saF(p + "title", "제목") + saF(p + "until", "마감일", "YYYY-MM-DD · 이 날까지 뜸", {ph:"2026-09-27"}) + '</div>' +''',
'''      var p = "notices." + i + ".", off = n.until && n.until < todayStr(), soon = n.from && n.from > todayStr();
      return saBox((n.title || "(제목 없음)") + (off ? " · 마감 지남" : soon ? " · " + n.from + " 부터" : ""),
        saF(p + "title", "제목") +
        '<div class="grid2">' + saD(p + "from", "시작일", "비우면 바로") + saD(p + "until", "마감일", "비우면 계속. 이 날까지 뜸") + '</div>' +''', 1)
s = rep(s, '''onclick="saArrAdd(\\'notices\\', {id:\\'n\\' + Date.now().toString(36), until:\\'\\', x:40''',
           '''onclick="saArrAdd(\\'notices\\', {id:\\'n\\' + Date.now().toString(36), from:\\'\\', until:\\'\\', x:40''', 1)
# 날짜 입력 조각 + 파일 올리기 + 적용 대화창
s = rep(s, '''function saI(path, label, note){   /* 사진: 파일명/주소 + 작은 보기 (3단계에서 '올리기' 붙음) */
  var v = saGet(path); if(v == null) v = "";
  return '<div class="f sa-f sa-img"><div class="lb">' + esc(label) + '</div><div class="sa-imgrow"><div class="sa-thumb">' + (v ? '<img src="' + esc(saImg(v)) + '" alt="" onerror="this.parentNode.classList.add(\\'bad\\')">' : '') + '</div><input type="text" class="in-sm" value="' + esc(v) + '" placeholder="img/ 파일명 또는 https:// 주소" oninput="saSet(\\'' + path + '\\', this.value)" onchange="render()"></div>' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</div>';
}''',
'''function saD(path, label, note){   /* 날짜 — 기기 달력으로 */
  var v = saGet(path); if(v == null) v = "";
  return '<label class="f sa-f"><div class="lb">' + esc(label) + '</div><input type="date" class="in-sm" value="' + esc(v) + '" onchange="saSet(\\'' + path + '\\', this.value); render()">' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</label>';
}
function saI(path, label, note){   /* 사진: 작은 보기 + 파일명/주소 + 올리기 */
  var v = saGet(path); if(v == null) v = "";
  return '<div class="f sa-f sa-img"><div class="lb">' + esc(label) + '</div><div class="sa-imgrow"><div class="sa-thumb">' + (v ? '<img src="' + esc(saImg(v)) + '" alt="" onerror="this.parentNode.classList.add(\\'bad\\')">' : '') + '</div><input type="text" class="in-sm" value="' + esc(v) + '" placeholder="img/ 파일명 또는 https:// 주소" oninput="saSet(\\'' + path + '\\', this.value)" onchange="render()"><button class="btn sm" onclick="saPickFile(\\'image\\', function(u){ saSet(\\'' + path + '\\', u); render(); })">올리기</button></div>' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</div>';
}
function saFile(path, label, note){   /* PDF 같은 파일: 주소 + 올리기 */
  var v = saGet(path); if(v == null) v = "";
  return '<div class="f sa-f"><div class="lb">' + esc(label) + '</div><div class="sa-imgrow"><input type="text" class="in-sm" value="' + esc(v) + '" oninput="saSet(\\'' + path + '\\', this.value)"><button class="btn sm" onclick="saPickFile(\\'pdf\\', function(u){ saSet(\\'' + path + '\\', u); render(); })">올리기</button></div>' + (note ? '<div class="f-note">' + note + '</div>' : '') + '</div>';
}

/* ---------- 파일 올리기 (Storage 'site' 버킷, 공개 읽기·직원만 쓰기) ----------
   kind: image(축소해서 JPEG/PNG) · pdf · video(mp4 그대로). 올린 뒤 공개 주소를 cb 로 돌려줍니다.
   사진은 올리기 전에 긴 변 1600px 로 줄입니다 — 폰 사진 원본(4~8MB)을 그대로 두면 홈페이지가 느리고 무료 전송량(월 5GB)이 금방 찹니다 */
var SA_PICK = null;
function saPickFile(kind, cb){
  if(!supaOn() || !SESSION){ uiAlert("서버 연결이 필요합니다", "", "warn"); return; }
  var inp = document.getElementById("sa-file");
  if(!inp){ inp = document.createElement("input"); inp.type = "file"; inp.id = "sa-file"; inp.style.display = "none"; document.body.appendChild(inp); inp.addEventListener("change", saFileChosen); }
  inp.accept = kind === "image" ? "image/*" : kind === "pdf" ? "application/pdf" : "video/mp4,video/*";
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
    else if(p.kind === "video"){ if(!/mp4|quicktime|video\\//.test(type) && ext !== "mp4") throw new Error("MP4 영상만 올릴 수 있습니다"); if(ext !== "mp4") throw new Error("MP4(H.264) 로 바꿔서 올려 주세요 — 구형 TV 는 다른 형식을 못 틉니다"); type = "video/mp4"; }
    if(blob.size > 50 * 1024 * 1024) throw new Error("50MB 를 넘습니다 (" + Math.round(blob.size / 1048576) + "MB)");
    var safe = f.name.replace(/\\.[^.]+$/, "").replace(/[^0-9A-Za-z가-힣_-]+/g, "_").slice(0, 40) || "file";
    var path = (view.storeKey || "hanok") + "/" + p.kind + "/" + Date.now().toString(36) + "_" + safe + "." + ext;
    var res = await fetch(SUPA_CFG.url + "/storage/v1/object/site/" + path, { method:"POST", headers:{ "apikey":SUPA_CFG.anonKey, "Authorization":"Bearer " + SESSION.access_token, "Content-Type":type, "x-upsert":"true", "Cache-Control":"max-age=31536000" }, body:blob });
    if(!res.ok){ var t = ""; try{ t = (await res.json()).message || ""; }catch(x){} throw new Error("올리기 실패 " + res.status + (t ? " · " + t : "")); }
    var url = SUPA_CFG.url + "/storage/v1/object/public/site/" + path;
    logEvent("파일 올림", p.kind + " " + f.name + " → " + path);
    showToast("올렸습니다 · " + Math.round(blob.size / 1024) + "KB");
    p.cb(url);
  }catch(err){ await uiAlert("올리지 못했습니다", err.message || String(err), "warn"); }
}
/* 사진 줄이기: 긴 변 1600px, JPEG 0.85. PNG(투명 배경 — 주방장 사진 같은 것)는 PNG 로 둡니다 */
function saShrink(file){
  return new Promise(function(resolve, reject){
    var isPng = /png$/i.test(file.type) || /\\.png$/i.test(file.name);
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
}''', 1)
# ③ 적용 대화창: 프롬프트 셋 → 한 화면(지금/정한 시각 + 날짜·시각 + 메모)
s = rep(s, '''async function saApply(){
  if(!SA || !SA.draft) return;
  if(saDirty() && !await saSave(true)) return;
  var when = await uiChoose("홈페이지에 적용", ["지금 바로", "날짜·시각을 정해서 (예약)"], "적용하면 손님이 보는 홈페이지가 바뀝니다. 이전 판은 남아 있어 되돌릴 수 있습니다.");
  if(when == null) return;
  var at = new Date();
  if(when === 1){
    var d = await uiPrompt("적용 날짜", "YYYY-MM-DD", {value:shiftDate(todayStr(), 1), ok:"다음"}); if(d == null) return;
    d = d.trim(); if(!/^\\d{4}-\\d{2}-\\d{2}$/.test(d)){ await uiAlert("날짜 형식", "2026-09-24 처럼 적어 주세요.", "warn"); return; }
    var t = await uiPrompt("적용 시각", "HH:MM (24시간)", {value:"00:00", ok:"다음"}); if(t == null) return;
    t = t.trim(); if(!/^\\d{2}:\\d{2}$/.test(t)){ await uiAlert("시각 형식", "09:00 처럼 적어 주세요.", "warn"); return; }
    at = new Date(d + "T" + t + ":00");
    if(isNaN(at.getTime())){ await uiAlert("날짜·시각 오류", d + " " + t, "warn"); return; }
    if(at.getTime() < Date.now()){ await uiAlert("지난 시각입니다", "지금 바로 적용하려면 '지금 바로' 를 고르세요.", "warn"); return; }
  }
  var note = await uiPrompt("메모 (선택)", "예: 추석 팝업, 가을 메뉴", {value:"", ok:"적용"}); if(note == null) return;
  note = note.trim();
  try{''',
'''async function saApply(){
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
    '<div class="seg"><button class="' + (a.mode === "now" ? "on" : "") + '" onclick="saApplySet(\\'mode\\', \\'now\\')">지금 바로</button><button class="' + (a.mode === "at" ? "on" : "") + '" onclick="saApplySet(\\'mode\\', \\'at\\')">정한 시각부터</button></div>' +
    (a.mode === "at" ? '<div class="grid2" style="margin-top:12px"><label class="f"><div class="lb">날짜</div><input type="date" value="' + esc(a.date) + '" onchange="saApplySet(\\'date\\', this.value)"></label><label class="f"><div class="lb">시각</div><input type="time" value="' + esc(a.time) + '" onchange="saApplySet(\\'time\\', this.value)"></label></div>' +
      '<p class="f-note" style="margin:-4px 0 12px">그 시각까지는 지금 판이 그대로 보이고, 시각이 되면 이 판으로 바뀝니다. 팝업 하나만 나중에 띄우는 거면 팝업의 시작일로 하는 게 간단합니다.</p>' : '') +
    (fut.length ? '<div class="alert amber" style="margin:8px 0"><span class="ic">!</span><div><div class="a-t">예약해 둔 판이 ' + fut.length + '건 있습니다</div><div class="a-s">' + fut.map(function(v){ return saWhen(v.apply_at) + (v.note ? " · " + esc(v.note) : ""); }).join(", ") + ' — 그 시각이 되면 그 판이 이 판을 덮습니다. 필요 없으면 적용 기록에서 취소하세요.</div></div></div>' : '') +
    '<label class="f" style="margin-top:12px"><div class="lb">메모 (선택)</div><input type="text" class="in-sm" placeholder="예: 추석 팝업, 가을 메뉴" value="' + esc(a.note) + '" oninput="saApplySet(\\'note\\', this.value)"></label>' +
    '<div class="sheet-actions btn-row"><button class="btn ghost" onclick="saApplyClose()">취소</button><button class="btn primary" data-enter onclick="saApplyDo()" style="margin-left:auto">' + (a.mode === "at" ? "이 시각에 적용" : "지금 적용") + '</button></div>' +
    '</div></div>';
}
async function saApplyDo(){
  var a = view.saApply; if(!a) return;
  var at = new Date(), when = a.mode === "at" ? 1 : 0, d = a.date, t = a.time, note = (a.note || "").trim();
  if(when === 1){
    if(!/^\\d{4}-\\d{2}-\\d{2}$/.test(d || "") || !/^\\d{2}:\\d{2}$/.test(t || "")){ await uiAlert("날짜와 시각을 고르세요", "", "warn"); return; }
    at = new Date(d + "T" + t + ":00");
    if(isNaN(at.getTime())){ await uiAlert("날짜·시각 오류", d + " " + t, "warn"); return; }
    if(at.getTime() < Date.now()){ await uiAlert("지난 시각입니다", "지금 바로 적용하려면 '지금 바로' 를 고르세요.", "warn"); return; }
  }
  view.saApply = null;
  try{''', 1)
s = rep(s, '''    '<div class="sa-body">' + body + '</div>' +
    (view.saPreview ? saPreviewHtml() : "");''',
'''    '<div class="sa-body">' + body + '</div>' +
    (view.saPreview ? saPreviewHtml() : "") + (view.saApply ? saApplyHtml() : "");''', 1)
# 메뉴판 PDF: 올리기 버튼
s = rep(s, '''      saF("info.menuPdf", "메뉴판 PDF", "파일명(menu.pdf) 또는 올린 파일 주소")) +''',
           '''      saFile("info.menuPdf", "메뉴판 PDF", "파일명(menu.pdf) 또는 올린 파일 주소. '올리기' 로 새 PDF 를 올리면 주소가 채워집니다")) +''', 1)
# 사진 탭 안내 문구
s = rep(s, '''  return '<p class="f-note" style="margin:0 0 12px">지금은 <b>img/ 폴더의 파일명</b> 또는 <b>전체 주소</b>를 적습니다. 태블릿·폰에서 사진을 바로 올리는 것(3단계)은 다음 작업입니다.</p>' +''',
           '''  return '<p class="f-note" style="margin:0 0 12px"><b>올리기</b>로 태블릿·폰의 사진을 고르면 줄여서(긴 변 1600px) 서버에 올라가고 칸에 주소가 들어갑니다. 파일명(img/ 폴더)이나 주소를 직접 적어도 됩니다.</p>' +''', 1)
save("js/14b-site-admin.js", s)
print("ok")
