/* ---------- 손님 관리 (customers, 15차) ----------
   손님 = 전화번호(숫자만) 하나. 예약 기록(reservations)에서 그 번호로 모아 방문·노쇼·취소·마지막 방문을 셉니다.
   이름은 같은 번호로 가장 많이 적힌 이름(재아) — 관리 화면에서 고정 이름을 따로 적을 수 있음. 손님마다 메모.
   찾기는 뒷자리 4자리 우선(전화로 "뒷자리가 어떻게 되세요?" 하고 찾는 흐름), 그다음 번호 전체·이름.
   서버 표 customers(store, phone, name, memo) — 메모·고정 이름만. 예약 자체는 건드리지 않습니다. 화면형, 관리자 비밀번호 뒤. */
var GS = null;
var CUST = null;   /* {phone: {name, memo}} — 예약 상세에서 손님 메모를 보여 주려고 앱 켤 때 한 번 받아 둠 */

async function gsLoadMemos(){
  if(!supaOn() || !SESSION) return;
  try{
    var rows = await sb("/rest/v1/customers?store=eq." + (view.storeKey || "hanok") + "&select=phone,name,memo");
    CUST = {}; rows.forEach(function(r){ CUST[r.phone] = r; });
  }catch(e){ if(!CUST) CUST = {}; }
}
function custOf(phone){ var d = String(phone || "").replace(/\D/g, ""); return (CUST && CUST[d]) || null; }

async function openGuestsPage(){
  if(!supaOn()){ await uiAlert("서버 설정이 없는 빌드입니다", "손님 관리는 서버가 있어야 합니다.", "warn"); return; }
  if(!view.adminOk){ if(!await adminGate("손님 관리 열기")) return; view.adminOk = true; }
  view.form = {type:"guests", page:true};
  if(!GS) GS = { q:"", sort:"recent", open:null, loading:true };
  render(); await gsLoadMemos(); GS.loading = false; render();
}
/* 예약 전체를 번호별로 모음 — 화면 그릴 때마다 계산(2천 건에 수십 ms) */
function gsBuild(){
  var map = {}, today = todayStr();
  store().reservations.forEach(function(r){
    var d = String(r.phone || "").replace(/\D/g, ""); if(d.length < 8) return;
    var g = map[d]; if(!g) g = map[d] = { phone:d, names:{}, total:0, visit:0, noshow:0, cancel:0, upcoming:0, last:"", first:"", people:0, list:[] };
    g.total++; g.list.push(r);
    var n = (r.name || "").trim(); if(n) g.names[n] = (g.names[n] || 0) + 1;
    if(r.status === "방문") g.visit++; else if(r.status === "노쇼") g.noshow++; else if(r.status === "취소") g.cancel++;
    if(r.status === "확정" && r.date >= today) g.upcoming++;
    if(r.status === "방문" || (r.status === "확정" && r.date < today)){ if(!g.last || r.date > g.last) g.last = r.date; }
    if(!g.first || r.date < g.first) g.first = r.date;
    g.people += pplOf(r);
  });
  Object.keys(map).forEach(function(k){
    var g = map[k], c = CUST && CUST[k];
    var best = "", n = 0; Object.keys(g.names).forEach(function(x){ if(g.names[x] > n){ n = g.names[x]; best = x; } });
    g.name = (c && c.name) || best || "(이름 없음)"; g.memo = (c && c.memo) || ""; g.aka = Object.keys(g.names).filter(function(x){ return x !== g.name; });
    g.list.sort(function(a, b){ return (b.date + b.time).localeCompare(a.date + a.time); });
  });
  return map;
}
function gsList(){
  var map = gsBuild(), all = Object.keys(map).map(function(k){ return map[k]; });
  var q = (GS.q || "").trim(), qd = q.replace(/\D/g, "");
  if(q){
    all = all.filter(function(g){
      if(qd.length >= 2 && qd.length <= 4) return g.phone.slice(-4).indexOf(qd) >= 0 || g.phone.indexOf(qd) >= 0;
      if(qd.length > 4) return g.phone.indexOf(qd) >= 0;
      var lq = q.toLowerCase(); return g.name.toLowerCase().indexOf(lq) >= 0 || g.aka.some(function(x){ return x.toLowerCase().indexOf(lq) >= 0; }) || (g.memo || "").toLowerCase().indexOf(lq) >= 0;
    });
    /* 뒷자리가 딱 맞는 손님을 위로 */
    if(qd.length === 4) all.sort(function(a, b){ return (b.phone.slice(-4) === qd) - (a.phone.slice(-4) === qd); });
  }else{
    if(GS.sort === "recent") all.sort(function(a, b){ return (b.last || "").localeCompare(a.last || "") || b.total - a.total; });
    else if(GS.sort === "visits") all.sort(function(a, b){ return b.visit - a.visit || b.total - a.total; });
    else if(GS.sort === "noshow") all = all.filter(function(g){ return g.noshow; }).sort(function(a, b){ return b.noshow - a.noshow; });
    else if(GS.sort === "memo") all = all.filter(function(g){ return g.memo; }).sort(function(a, b){ return (b.last || "").localeCompare(a.last || ""); });
  }
  return all;
}
function gsPhoneHtml(d){ var f = phoneNorm(d); var i = f.lastIndexOf("-"); return i > 0 ? esc(f.slice(0, i + 1)) + '<b>' + esc(f.slice(i + 1)) + '</b>' : '<b>' + esc(f) + '</b>'; }
function gsSetQ(v){ GS.q = v; var box = document.getElementById("gs-list"); if(box) box.innerHTML = gsRows(); }
function gsRows(){
  var list = gsList().slice(0, 200);
  if(!list.length) return '<div class="empty">' + (GS.q ? "맞는 손님이 없습니다." : "예약 기록이 있는 손님이 여기 모입니다.") + '</div>';
  return list.map(function(g){
    return '<button class="rowitem tap" onclick="gsOpen(\'' + g.phone + '\')"><span class="grow"><span class="t">' + esc(g.name) + (g.memo ? ' <span class="tag blue sm">메모</span>' : '') + (g.noshow ? ' <span class="tag rust sm">노쇼 ' + g.noshow + '</span>' : '') + '</span>' +
      '<span class="s">' + gsPhoneHtml(g.phone) + ' · 방문 ' + g.visit + (g.upcoming ? ' · 예정 ' + g.upcoming : '') + (g.cancel ? ' · 취소 ' + g.cancel : '') + (g.last ? ' · 마지막 ' + dateLabel(g.last) : '') + '</span></span></button>';
  }).join("");
}
function gsOpen(phone){ GS.open = phone; GS.memoDraft = null; render(); }
function gsClose(){ GS.open = null; render(); }
async function gsSave(){
  var map = gsBuild(), g = map[GS.open]; if(!g) return;
  var nameEl = document.getElementById("gs-name"), memoEl = document.getElementById("gs-memo");
  var row = { store:view.storeKey || "hanok", phone:GS.open, name:(nameEl ? nameEl.value : "").trim(), memo:(memoEl ? memoEl.value : "").trim(), by:(SESSION && SESSION.who) || "" };
  try{
    await sb("/rest/v1/customers?on_conflict=store,phone", { method:"POST", body:row, prefer:"resolution=merge-duplicates,return=minimal" });
    CUST = CUST || {}; CUST[GS.open] = row; showToast("저장했습니다"); render();
  }catch(e){ await uiAlert("저장 실패", e.message || String(e), "warn"); }
}
function sheetGuests(){
  if(!GS || GS.loading) return '<p class="muted" style="padding:20px 0">불러오는 중…</p>';
  var seg = function(k, label){ return '<button class="' + (GS.sort === k ? "on" : "") + '" onclick="GS.sort=\'' + k + '\'; render()">' + label + '</button>'; };
  return '<div class="gs-top"><input id="gs-q" value="' + esc(GS.q || "") + '" placeholder="뒷자리 4자리 · 번호 · 이름 · 메모" oninput="gsSetQ(this.value)" autocomplete="off">' +
    '<div class="seg">' + seg("recent", "최근 방문") + seg("visits", "많이 온 순") + seg("noshow", "노쇼") + seg("memo", "메모 있음") + '</div></div>' +
    '<div class="card searchbox" id="gs-list">' + gsRows() + '</div>' +
    '<p class="f-note">전화번호 하나 = 손님 하나. 이름은 그 번호로 가장 많이 적힌 이름이고, 열어서 고정 이름·메모를 적을 수 있습니다. 예약을 고치면 여기도 바로 바뀝니다.</p>' +
    (GS.open ? gsDetailHtml() : "");
}
function gsDetailHtml(){
  var g = gsBuild()[GS.open]; if(!g) return "";
  var c = CUST && CUST[GS.open];
  var hist = g.list.slice(0, 40).map(function(r){
    return '<button class="rowitem tap" onclick="GS.open=null; openMark(\'' + r.id + '\')"><span class="time-col">' + esc(dateLabel(r.date).replace(/ \(.\)$/, "")) + '</span><span class="grow"><span class="t">' + esc(hm(r.time)) + ' · ' + pplText(r) + (r.status !== "확정" ? ' <span class="tag ' + (r.status === "노쇼" ? "rust" : r.status === "방문" ? "pine" : "") + ' sm">' + r.status + '</span>' : '') + '</span>' +
      '<span class="s">' + esc(resSeatLabel(r)) + (r.name !== g.name ? ' · ' + esc(r.name) : '') + (r.request ? ' · ' + esc(r.request) : '') + (r.allergy ? ' · 알러지 ' + esc(r.allergy) : '') + '</span></span></button>';
  }).join("");
  return '<div class="overlay" onclick="gsClose()"><div class="sheet sheet-tall" onclick="event.stopPropagation()">' +
    sheetHead(esc(g.name) + ' <small class="muted">' + gsPhoneHtml(g.phone) + '</small>') +
    '<div class="gs-stats"><span><b>' + g.visit + '</b>방문</span><span><b>' + g.upcoming + '</b>예정</span><span class="' + (g.noshow ? "rust" : "") + '"><b>' + g.noshow + '</b>노쇼</span><span><b>' + g.cancel + '</b>취소</span><span><b>' + (g.total ? Math.round(g.people / g.total) : 0) + '</b>평균 인원</span></div>' +
    (g.aka.length ? '<p class="f-note">이 번호로 적힌 다른 이름: ' + esc(g.aka.join(", ")) + '</p>' : '') +
    '<div class="grid2"><label class="f"><div class="lb">고정 이름 <span class="lbl-note">비우면 자동</span></div><input id="gs-name" type="text" value="' + esc(c ? c.name : "") + '" placeholder="' + esc(g.name) + '"></label>' +
    '<label class="f"><div class="lb">메모</div><input id="gs-memo" type="text" value="' + esc(g.memo || "") + '" placeholder="예: 창가 선호, 매운 것 못 드심, 단골"></label></div>' +
    '<div class="btn-row" style="margin:0 0 10px"><button class="btn sm primary" onclick="gsSave()">메모 저장</button></div>' +
    '<div class="subhead">예약 기록 ' + g.total + '건</div><div class="card searchbox">' + hist + '</div>' +
    '<div class="sheet-actions"><button class="btn primary" onclick="gsClose()">닫기</button></div></div></div>';
}
function gsEsc(){ if(GS && view.form && view.form.type === "guests" && GS.open){ GS.open = null; render(); return true; } return false; }
