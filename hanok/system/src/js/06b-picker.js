/* ============================================================
   숫자·날짜·기간 입력 팝업 (09-24 재아: "기본 입력 말고 우리 팝업으로 — 시스템 전반")
   · uiNum(제목, 값, {min, max, unit})      → 숫자(문자열 아님) 또는 null(취소)
   · uiDate(제목, 'YYYY-MM-DD', {min, max, clear}) → 'YYYY-MM-DD' / ""(지움) / null(취소)
   · uiRange(제목, from, to, {openEnd, clear})     → {from, to} / null. openEnd 면 '끝 없음'(to:"") 가능
   · 앱 안의 <input type="date">·<input type="number"> 는 전부 누르면 위 팝업이 뜹니다(pkArm).
     칸 값을 바꾼 뒤 input·change 이벤트를 내 주므로 기존 onchange 가 그대로 돕니다 — 칸마다 고칠 필요 없음.
     기기 기본 달력·키보드는 기기마다 모양이 달라 사장님이 헷갈렸음. 키보드(숫자·Backspace·Enter)도 팝업에서 받습니다.
   구형 TV 금지 문법 주의 — 손님 TV 화면에는 이 칸들이 없지만 같은 파일로 빌드됩니다.
   ============================================================ */
var PK_WD = ["일","월","화","수","목","금","토"];
function pkYmd(d){ return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
function pkShort(ds){ if(!ds) return ""; var d = new Date(ds + "T00:00:00"); return (d.getMonth() + 1) + "/" + d.getDate() + "(" + PK_WD[d.getDay()] + ")"; }
/* 기간 글자 — '9/24(목) ~ 9/28(월)', 끝이 없으면 '9/24(목) 부터', 둘 다 없으면 빈 글 */
function pkRangeText(a, b){ if(!a && !b) return ""; if(a && !b) return pkShort(a) + " 부터"; if(!a) return pkShort(b) + " 까지"; return a === b ? pkShort(a) : pkShort(a) + " ~ " + pkShort(b); }

function uiNum(title, value, opt){
  opt = opt || {};
  return new Promise(function(res){ modalReplace({mode:"num", title:title, tone:"ok", buf:(value == null || value === "") ? "" : String(value), fresh:true, min:opt.min, max:opt.max, unit:opt.unit || "", err:"", res:res}); });
}
function uiDate(title, value, opt){
  opt = opt || {};
  var v = value || "", m = (v || todayStr()).slice(0, 7);
  return new Promise(function(res){ modalReplace({mode:"date", title:title, tone:"ok", a:v, month:m, min:opt.min || "", max:opt.max || "", clear:!!opt.clear, res:res}); });
}
function uiRange(title, from, to, opt){
  opt = opt || {};
  var m = (from || to || todayStr()).slice(0, 7);
  return new Promise(function(res){ modalReplace({mode:"range", title:title, tone:"ok", a:from || "", b:to || "", pickB:!!from, month:m, min:opt.min || "", openEnd:!!opt.openEnd, clear:!!opt.clear, res:res}); });
}

/* ---------- 숫자 ---------- */
function pkNumPush(k){
  var m = MODAL; if(!m || m.mode !== "num") return;
  if(m.fresh && /^[0-9]$/.test(String(k))){ m.buf = ""; }   /* 처음 누르는 숫자는 새로 쓰기(값 뒤에 붙지 않게) */
  m.fresh = false; m.err = "";
  if(k === "back") m.buf = m.buf.slice(0, -1);
  else if(k === "clear") m.buf = "";
  else if(m.buf.length < 7) m.buf = (m.buf === "0" ? "" : m.buf) + String(k);
  render();
}
function pkNumOk(){
  var m = MODAL; if(!m || m.mode !== "num") return;
  if(m.buf === ""){ m.err = "숫자를 넣어 주세요"; render(); return; }
  var n = parseInt(m.buf, 10);
  if((m.min != null && n < m.min) || (m.max != null && n > m.max)){ m.err = (m.min != null ? m.min : "") + " ~ " + (m.max != null ? m.max : "") + " 사이로 넣어 주세요"; render(); return; }
  MODAL = null; render(); m.res(n);
}
function pkFmtNum(s){ return s === "" ? "" : Number(s).toLocaleString("ko-KR"); }

/* ---------- 달력(날짜·기간 같이 씀) ---------- */
function pkMonth(n){ var m = MODAL; if(!m) return; var p = m.month.split("-").map(Number), d = new Date(p[0], p[1] - 1 + n, 1); m.month = d.getFullYear() + "-" + pad(d.getMonth() + 1); render(); }
function pkPick(ds){
  var m = MODAL; if(!m) return;
  if(m.mode === "date"){ MODAL = null; render(); m.res(ds); return; }
  /* 기간: 첫 번째 = 시작, 두 번째 = 끝(앞이면 서로 바꿈). 셋째부터는 새로 시작 */
  if(!m.pickB || !m.a){ m.a = ds; m.b = ""; m.pickB = true; }
  else { if(ds < m.a){ m.b = m.a; m.a = ds; } else m.b = ds; m.pickB = false; }
  render();
}
function pkRangeOk(noEnd){
  var m = MODAL; if(!m || m.mode !== "range" || !m.a) return;
  var b = noEnd ? "" : (m.b || m.a);   /* 끝을 안 골랐으면 하루짜리 */
  MODAL = null; render(); m.res({from:m.a, to:b});
}
function pkClear(){ var m = MODAL; if(!m) return; MODAL = null; render(); m.res(m.mode === "range" ? {from:"", to:""} : ""); }
function pkCalHtml(m){
  var p = m.month.split("-").map(Number), y = p[0], mo = p[1];
  var lead = new Date(y, mo - 1, 1).getDay(), last = new Date(y, mo, 0).getDate(), today = todayStr(), cells = "";
  for(var i = 0; i < lead; i++) cells += '<span></span>';
  for(var d = 1; d <= last; d++){
    var ds = y + "-" + pad(mo) + "-" + pad(d), dow = (lead + d - 1) % 7;
    var off = (m.min && ds < m.min) || (m.max && ds > m.max);
    var sel = m.mode === "date" ? ds === m.a : (ds === m.a || ds === m.b);
    var inR = m.mode === "range" && m.a && m.b && ds > m.a && ds < m.b;
    cells += '<button type="button" class="pk-d' + (dow === 0 ? ' sun' : dow === 6 ? ' sat' : '') + (ds === today ? ' today' : '') + (sel ? ' on' : '') + (inR ? ' in' : '') + '"' + (off ? ' disabled' : '') + ' onclick="pkPick(\'' + ds + '\')">' + d + '</button>';
  }
  return '<div class="pk-cal"><div class="pk-nav"><button type="button" onclick="pkMonth(-1)" aria-label="이전 달">‹</button><b>' + y + '년 ' + mo + '월</b><button type="button" onclick="pkMonth(1)" aria-label="다음 달">›</button></div>' +
    '<div class="pk-grid pk-head">' + PK_WD.map(function(w, i){ return '<span class="' + (i === 0 ? 'sun' : i === 6 ? 'sat' : '') + '">' + w + '</span>'; }).join("") + '</div>' +
    '<div class="pk-grid">' + cells + '</div></div>';
}

/* renderModal(06) 이 이 세 가지일 때 여기로 넘깁니다 */
function pkRender(m){
  var body = "", foot = '<button class="btn" onclick="modalAnswer(null)">취소</button>';
  if(m.mode === "num"){
    body = '<div class="pk-num"><span class="pk-v">' + (m.buf === "" ? '<i>&nbsp;</i>' : esc(pkFmtNum(m.buf))) + '</span>' + (m.unit ? '<small>' + esc(m.unit) + '</small>' : '') + '</div>' +
      '<div class="pk-err">' + esc(m.err || "") + '</div>' +
      '<div class="pkeys md">' + [1,2,3,4,5,6,7,8,9,"clear",0,"back"].map(function(k){ return k === "clear" ? '<button class="pkey sub" onclick="pkNumPush(\'clear\')" title="지우기">↻</button>' : k === "back" ? '<button class="pkey sub" onclick="pkNumPush(\'back\')" aria-label="한 글자 지우기">←</button>' : '<button class="pkey" onclick="pkNumPush(' + k + ')">' + k + '</button>'; }).join("") + '</div>';
    foot += '<button class="btn primary" onclick="pkNumOk()">확인</button>';
  }else if(m.mode === "date"){
    body = pkCalHtml(m);
    if(m.clear) foot = '<button class="btn ghost" onclick="pkClear()" style="margin-right:auto">지우기</button>' + foot;
  }else{
    body = '<div class="pk-rng"><span class="' + (!m.pickB ? 'cur' : '') + '"><small>시작</small>' + (m.a ? esc(pkShort(m.a)) : '—') + '</span><i>~</i><span class="' + (m.pickB ? 'cur' : '') + '"><small>끝</small>' + (m.b ? esc(pkShort(m.b)) : (m.a ? '같은 날' : '—')) + '</span></div>' + pkCalHtml(m);
    if(m.clear) foot = '<button class="btn ghost" onclick="pkClear()" style="margin-right:auto">지우기</button>' + foot;
    if(m.openEnd) foot += '<button class="btn" onclick="pkRangeOk(true)"' + (m.a ? '' : ' disabled') + '>끝 없이</button>';
    foot += '<button class="btn primary" onclick="pkRangeOk(false)"' + (m.a ? '' : ' disabled') + '>확인</button>';
  }
  return '<div class="overlay modal-ov" onclick="modalAnswer(null)"><div class="modal ok pk-modal pkm-' + m.mode + '" role="dialog" aria-modal="true" aria-labelledby="modal-title" onclick="event.stopPropagation()">' +
    '<div class="md-h" id="modal-title">' + esc(m.title) + '</div><div class="md-b">' + body + '</div><div class="md-f">' + foot + '</div></div></div>';
}

/* ---------- 앱 안의 기본 날짜·숫자 칸을 팝업으로 ----------
   readOnly 로 기기 달력·키보드를 막고, 누르거나(마우스·손가락) 포커스 뒤 Enter·Space·숫자를 치면 팝업. 값이 정해지면 input·change 를 내 줌 */
function pkArm(root){
  var list = (root || document).querySelectorAll('input[type="date"], input[type="number"]');
  for(var i = 0; i < list.length; i++){ var el = list[i]; if(el.dataset.pk) continue; el.dataset.pk = "1"; el.readOnly = true; el.setAttribute("inputmode", "none"); el.classList.add("pk-in"); }
}
function pkLabel(el){
  var lab = el.closest("label"), lb = lab && lab.querySelector(".lb, b");
  var t = (lb && lb.textContent) || el.getAttribute("aria-label") || el.title || el.placeholder || (el.type === "date" ? "날짜" : "숫자");
  return String(t).replace(/\s+/g, " ").trim().slice(0, 30);
}
/* 팝업을 닫으면 화면을 다시 그려서 처음 누른 칸(el)은 이미 화면에 없습니다. 새로 그려진 같은 칸(id, 없으면 순번)에 넣습니다 */
function pkKey(el){ if(el.id) return "#" + el.id; var l = document.querySelectorAll("input.pk-in"); for(var i = 0; i < l.length; i++) if(l[i] === el) return i; return -1; }
function pkLive(el, key){
  if(document.body.contains(el)) return el;
  if(typeof key === "string") return document.getElementById(key.slice(1)) || el;
  var l = document.querySelectorAll("input.pk-in"); return (key >= 0 && l[key] && l[key].type === el.type) ? l[key] : el;
}
function pkSet(el, v){
  el.value = v;
  el.dispatchEvent(new Event("input", {bubbles:true}));
  el.dispatchEvent(new Event("change", {bubbles:true}));
}
function pkOpenFor(el, firstKey){
  if(el.disabled) return;
  var key = pkKey(el);
  if(el.type === "date"){
    uiDate(pkLabel(el), el.value, {min:el.min, max:el.max, clear:!el.required}).then(function(v){ if(v != null) pkSet(pkLive(el, key), v); });
  }else{
    var mn = el.min !== "" ? Number(el.min) : null, mx = el.max !== "" ? Number(el.max) : null;
    uiNum(pkLabel(el), el.value, {min:mn, max:mx, unit:el.dataset.unit || ""}).then(function(v){ if(v != null) pkSet(pkLive(el, key), String(v)); });
    if(firstKey) setTimeout(function(){ pkNumPush(firstKey); }, 0);
  }
}
document.addEventListener("click", function(e){
  var el = e.target && e.target.closest && e.target.closest("input.pk-in");
  if(!el) return;
  e.preventDefault(); pkOpenFor(el);
}, true);
/* 아직 무장 안 된 칸(그리기 밖에서 생긴 것)에 손이 가면 그 자리에서 무장하고 팝업 */
document.addEventListener("focusin", function(e){
  var el = e.target;
  if(el && el.tagName === "INPUT" && (el.type === "date" || el.type === "number") && !el.dataset.pk){ pkArm(el.parentNode); }
}, true);
document.addEventListener("keydown", function(e){
  var m = MODAL;
  if(m && m.mode === "num"){
    if(/^[0-9]$/.test(e.key)){ e.preventDefault(); e.stopImmediatePropagation(); pkNumPush(e.key); }
    else if(e.key === "Backspace"){ e.preventDefault(); e.stopImmediatePropagation(); pkNumPush("back"); }
    else if(e.key === "Delete"){ e.preventDefault(); e.stopImmediatePropagation(); pkNumPush("clear"); }
    else if(e.key === "Enter"){ e.preventDefault(); e.stopImmediatePropagation(); pkNumOk(); }
    return;
  }
  if(m && m.mode === "range" && e.key === "Enter" && m.a){ e.preventDefault(); e.stopImmediatePropagation(); pkRangeOk(false); return; }
  if(m && (m.mode === "date" || m.mode === "range") && (e.key === "ArrowLeft" || e.key === "ArrowRight") && !e.altKey){ e.preventDefault(); e.stopImmediatePropagation(); pkMonth(e.key === "ArrowLeft" ? -1 : 1); return; }
  var el = e.target;
  if(!m && el && el.classList && el.classList.contains("pk-in")){
    if(e.key === "Enter" || e.key === " "){ e.preventDefault(); e.stopImmediatePropagation(); pkOpenFor(el); }
    else if(el.type === "number" && /^[0-9]$/.test(e.key)){ e.preventDefault(); e.stopImmediatePropagation(); pkOpenFor(el, e.key); }
  }
}, true);
