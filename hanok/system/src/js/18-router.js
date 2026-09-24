/* ============================================================
   주소로 화면 구분
     /            → 관리 화면 (PIN 필요)
     /screen      → 디스플레이 모드 (TV용, 바로 진입)
     /screen/hanok → 매장을 지정해서 진입
   서버 설정 없이도 되도록 #/screen 도 함께 지원합니다.
   ============================================================ */
function readRoute(){
  /* v4 부터 손님용 화면은 screen/ 폴더의 index.html 입니다.
     .../screen  .../screen/  .../screen/index.html  .../screen/hanok  전부 같은 뜻으로 봅니다 */
  const path = (location.pathname || "").replace(/\/index\.html?$/i,"").replace(/\/+$/,"");
  const hash = (location.hash || "").replace(/^#/,"").replace(/\/+$/,"");
  const raw = /screen/.test(hash) ? hash : path;
  const m = raw.match(/\/?screen(?:\/([a-z]+))?$/i);
  if(!m) return null;
  return {screen:true, store:(m[1]||"hanok").toLowerCase()};
}
function applyRoute(){
  const r = readRoute();
  if(r && DATA && DATA[r.store]){
    view.storeKey = r.store;
    view.display = true;
    view.fromRoute = true;      /* 주소로 바로 들어온 경우 */
    startDisplayTimers();
    return true;
  }
  return false;
}
/* ---------- 관리 화면 주소 (6차-K) ----------
   #/hanok  #/hanok/settings  #/hanok/2026-09-20  — 새로고침해도 보던 자리로 돌아옵니다.
   폴더로 나누지 않고 해시로만 나눕니다: 파일 하나 원칙이 지켜지고, 화면 사이 이동이 페이지 이동이 되지 않으며,
   로그인 상태를 페이지 사이에 넘길 필요가 없습니다.
   방향은 '상태 → 주소' 한쪽뿐입니다(syncHash, 그릴 때마다). 주소를 사람이 고치거나 새로 열 때만 '주소 → 상태'(applyAdminRoute).
   history 항목은 늘리지 않습니다(replaceState) — 뒤로가기는 마법사 보호(popstate)만 씁니다 */
function adminHash(){
  if(!view.storeKey || view.display) return "";
  var h = "/" + view.storeKey;
  if(view.tab === "settings") h += "/settings";
  else if(view.date && view.date !== todayStr()) h += "/" + view.date;   /* 오늘이면 날짜를 안 적어 내일 열어도 '오늘' */
  return h;
}
function syncHash(){
  var want = adminHash();
  var cur = (location.hash || "").replace(/^#/, "");
  if(want === cur) return;
  try{
    if(location.protocol === "file:"){ location.hash = want; return; }   /* file: 에서는 replaceState 가 막힐 수 있음 */
    /* history.state 를 그대로 넘겨야 마법사 보호용 {wz:1} 이 지워지지 않습니다 */
    history.replaceState(history.state, "", location.pathname + location.search + (want ? "#" + want : ""));
  }catch(e){}
}
function applyAdminRoute(){
  var hash = (location.hash || "").replace(/^#/, "").replace(/\/+$/, "");
  var m = hash.match(/^\/([a-z]+)(?:\/(settings|\d{4}-\d{2}-\d{2}))?$/i);
  if(!m || !DATA || !DATA[m[1].toLowerCase()] || !DATA[m[1].toLowerCase()].enabled) return false;
  var key = m[1].toLowerCase(), sub = m[2] || "";
  var tab = sub === "settings" ? "settings" : "dash";
  var date = /^\d{4}-\d{2}-\d{2}$/.test(sub) ? sub : todayStr();
  if(view.storeKey === key && view.tab === tab && view.date === date && !view.display) return false;   /* 이미 그 자리 — hashchange 되풀이 방지 */
  view.storeKey = key; view.tab = tab; view.date = date; view.calMonth = date.slice(0,7);
  view.display = false; view.form = null; tmpRes = null;
  if(tab === "settings") view.draft = deepClone(DATA[key].settings);   /* 설정은 임시본 위에서 편집합니다(setTab 과 같게) */
  return true;
}
/* 주소를 바꿔 둡니다 (파일로 열었을 때는 조용히 실패해도 괜찮습니다) */
function setRoute(toScreen){
  try{
    if(location.protocol === "file:"){
      location.hash = toScreen ? `/screen/${view.storeKey}` : "";
      return;
    }
    /* 관리 화면에서 디스플레이를 열 때는 주소만 바꿔 둡니다 (뒤로 가기·새로고침 대비).
       screen/ 은 실제 폴더라 그 안의 /hanok 은 서버에 없으므로 폴더 주소로만 갑니다 */
    const base = appDir();
    history.replaceState(null, "", toScreen ? `${base}/screen/` : (base || "/"));
  }catch(e){ /* 주소를 바꿀 수 없으면 그냥 둡니다 */ }
}
/* 배경 순환·자동 갱신 타이머 */
function startDisplayTimers(){
  view.bgIndex = view.bgIndex || 1;
  clearInterval(bgTimer); clearInterval(dispTimer);
  bgTimer = setInterval(()=>{
    if(!view.display) return;
    view.bgIndex = (view.bgIndex % 7) + 1;
    document.querySelectorAll(".tv-bg").forEach((el,i)=> el.classList.toggle("on", i+1===view.bgIndex));
  }, 12000);
  dispTimer = setInterval(displayTick, 60000);
  startDailyReload();
}
/* 1분마다: 데이터를 다시 읽고 목록만 갈아 끼웁니다.
   render() 로 통째로 그리면 <video> 가 새로 만들어져 광고가 매분 처음부터 다시 시작합니다. */
var DISP_FAIL = 0;
async function displayTick(){
  if(!view.display) return;
  try{ await refreshData(); DISP_FAIL = 0; }
  catch(e){ DISP_FAIL++; console.warn("디스플레이 갱신 실패", DISP_FAIL, e); }   /* 마지막 데이터로 계속 보여 줍니다 */
  updateDisplayInPlace();
}
var TV_IDLE_SHOWN = null;
function updateDisplayInPlace(){
  if(!view.display) return;
  /* 광고만 ↔ 목록 이 바뀌는 순간에만 통째로 다시 그립니다 (영상이 처음부터 다시 시작되는 건 이때뿐) */
  var idle = tvIdle();
  if(idle !== TV_IDLE_SHOWN){ render(); return; }
  if(idle) return;
  var side = document.querySelector(".tvl-side");
  if(tvType() !== "grid" && side){
    side.innerHTML = tvSideHtml();
    fitTvList();
  } else {
    render();   /* 좌석표형은 영상이 없어 통째로 그려도 됩니다 */
    document.querySelectorAll(".tv-bg").forEach((el,i)=> el.classList.toggle("on", i+1===(view.bgIndex||1)));
  }
}
/* 하루 한 번(새벽 4시) 페이지를 새로 불러옵니다.
   TV 브라우저를 몇 주씩 켜 두면 메모리가 새서 느려지거나 멈춥니다. 영업 전 시간에 한 번 털어 줍니다.
   주소로 바로 들어온(방치용) 화면에서만 합니다 — 관리 화면에서 잠깐 연 디스플레이는 건드리지 않습니다. */
var dailyTimer = null;
function startDailyReload(){
  clearInterval(dailyTimer);
  if(!view.fromRoute) return;
  var lastDay = new Date().getDate();
  dailyTimer = setInterval(function(){
    var d = new Date();
    if(d.getHours() === 4 && d.getDate() !== lastDay){ lastDay = d.getDate(); location.reload(); }
  }, 60000);
}
function openDisplay(){
  logEvent("디스플레이 모드", "");
  view.display = true;
  view.fromRoute = false;
  setRoute(true);
  render();
  startDisplayTimers();
  setTimeout(()=>{ pokeExit(4000); }, 120);
  document.addEventListener("keydown", escDisplay);
}
function closeDisplay(){
  const wasRoute = view.fromRoute;
  view.display = false; view.fromRoute = false;
  setRoute(false);
  /* 주소로 바로 들어온 경우에는 관리 화면 대신 잠금 화면으로 */
  if(wasRoute && !AUTHED){ view.storeKey = null; }
  clearInterval(dispTimer); clearInterval(bgTimer);
  document.removeEventListener("keydown", escDisplay);
  render();
}
function escDisplay(e){ if(e.key==="Escape") closeDisplay(); }
/* 종료 버튼을 잠깐 보여줍니다 (터치 기기에는 호버가 없으므로) */
let exitTimer = null;
function pokeExit(ms){
  /* 종료와 전환을 같이 띄웁니다 — TV 에는 마우스가 없어 화면을 눌러야 나옵니다 */
  const els = document.querySelectorAll(".tv-exit, .tv-swap");
  if(!els.length) return;
  for(var i=0;i<els.length;i++) els[i].classList.add("show");
  clearTimeout(exitTimer);
  exitTimer = setTimeout(function(){
    var e2 = document.querySelectorAll(".tv-exit, .tv-swap");
    for(var j=0;j<e2.length;j++) e2[j].classList.remove("show");
  }, ms||5000);
}

/* 이름 가운데 글자를 * 로 가림 — 손님 이름이 TV에 그대로 노출되지 않도록 */
/* 디스플레이 모드에 쓸 좌석 배치 — 3행, 각 행 최대 6칸 */
const DISP_MAX = 6;
function displayRows(){
  const st = store().settings;
  /* 테이블은 개별이 아니라 층별 한 칸("tables:1층")으로 — TV 는 룸 8칸 + 테이블 층 2칸이면 충분 */
  const ids = st.rooms.filter(isRoom).map(r=>r.id).concat(tableFloors().map(f=>"tables:"+f));
  const saved = st.displayRows;
  if(saved && saved.length===3){
    /* 없어진 좌석은 빼고, 새로 생긴 좌석은 빈 칸이 있는 행에 넣습니다 */
    const rows = saved.map(row=>row.filter(id=>ids.includes(id)));
    const placed = new Set([].concat.apply([], rows));
    ids.filter(id=>!placed.has(id)).forEach(id=>{
      const row = rows.find(r=>r.length<DISP_MAX) || rows[2];
      row.push(id);
    });
    return rows;
  }
  /* 기본: 1행 테이블(층별), 2·3행 룸을 반씩 */
  const halls = tableFloors().map(f=>"tables:"+f);
  const rooms = st.rooms.filter(isRoom).map(r=>r.id);
  const half = Math.ceil(rooms.length/2);
  return [halls, rooms.slice(0,half), rooms.slice(half)];
}
function tableFloors(){
  const out = []; (store().settings.rooms||[]).filter(isTable).forEach(t=>{ if(out.indexOf(t.floor||"")<0) out.push(t.floor||""); }); return out;
}
/* 디스플레이 칸 하나의 정보 — 룸이면 그 룸, "tables:층" 이면 그 층 테이블 묶음 */
function dispCell(id){
  if(/^tables:/.test(id)){ const fl = id.slice(7); return {id, name:`${fl||""} 테이블`.trim(), floor:"", floorKey:fl, type:"tables", ids:store().settings.rooms.filter(t=>isTable(t) && (t.floor||"")===fl).map(t=>t.id)}; }
  const r = seatById(id); return r ? Object.assign({ids:[r.id]}, r) : null;
}
/* ---------- 디스플레이 모드 글자 크기 자동 맞춤 ----------
   TV는 3~5m 떨어져서 봅니다. 예약이 적은 날에도 글자가 작으면 그냥 안 보입니다.
   그래서 "잘리지 않는 한 가장 크게" 를 화면 전체에 한 값으로 적용합니다.
   칸마다 크기를 따로 정하면 옆 칸과 어긋나 지저분해 보이므로 한 값만 씁니다.
   구형 TV 브라우저를 고려해 CSS max()·clamp() 대신 변수 하나만 바꿉니다. */
/* vh 단위, 큰 것부터. 첫 값이 상한, 마지막이 하한입니다.
   **글자가 크거나 작다는 말이 나오면 첫 값만 바꾸면 됩니다.**
   하한보다 더 줄이면 TV에서 못 읽으므로, 그래도 안 들어가면 목록을 접습니다. */
var TV_SIZES = [3.6, 3.3, 3.0, 2.8, 2.6, 2.4, 2.2];   /* 09-20: 좌석표를 층 기둥으로 바꾸며 칸이 커져 상한을 3.6 으로 */   /* 8차-J: 칸이 비어 있으면 글자를 키웁니다 — 안 넘치는 가장 큰 값을 고릅니다 */
/* 목록형 — 날개에 들어가는 줄 수는 TV 높이에 따라 달라집니다.
   넘치는 줄은 숨기고 '외 N건' 으로 알립니다.
   글자를 줄이지 않는 이유: 입구 TV 는 멀리서 봅니다. 작아지면 있으나 마나입니다. */
function fitTvList(){
  var box = document.querySelector(".tvl-rows");
  var more = document.querySelector(".tvl-more");
  if(!box || !more) return;
  var items = box.querySelectorAll(".tvl-r");
  /* 접을 때 세는 단위는 '묶음' 이 아니라 '예약 건수' 입니다 */
  var cnt = function(el){ return el.querySelectorAll(".tvl-g").length || 1; };
  var i;
  for(i=0;i<items.length;i++) items[i].style.display = "";
  more.textContent = "";
  if(!items.length) return;
  /* 뒤에서부터 하나씩 숨기며 넘치지 않을 때까지 */
  var hiddenGroups = 0, hiddenRes = 0;
  while(box.scrollHeight > box.clientHeight + 1 && hiddenGroups < items.length){
    hiddenGroups++;
    var el = items[items.length - hiddenGroups];
    el.style.display = "none";
    hiddenRes += cnt(el);
  }
  if(hiddenRes) more.textContent = "외 " + hiddenRes + "건";
}
function fitDisplay(){
  fitTvList();
  var grid = document.querySelector(".tv-grid");
  if(!grid || !grid.querySelectorAll(".dsec").length) return;
  /* 글자 크기는 고정입니다. 칸 크기도 CSS 에서 고정입니다.
     넘치는 만큼만 목록을 접습니다 — 칸마다 몇 줄까지 보일지를 줄여 나갑니다. */
  /* 큰 글자부터 시도해서 안 넘치는 첫 크기로. 다 넘치면 가장 작은 크기에서 줄을 접습니다 */
  /* 09-20: 칸마다 따로 접습니다. 큰 글자부터 시도해서, 모든 칸이 '최소 2줄' 을 보이며 들어가는 첫 크기를 고르고,
     그래도 넘치는 칸만 1줄까지 더 접습니다. (예전엔 한 칸이 넘치면 모든 칸을 같이 접어 여유 있는 칸에도 '외 N건' 이 붙었음) */
  var si;
  for(si = 0; si < TV_SIZES.length; si++){
    setGridSize(grid, TV_SIZES[si]);
    if(capEach(grid, 2)) break;
  }
  capEach(grid, 1);
}
/* 칸마다 넘치지 않을 때까지 줄을 접음(최소 minKeep 줄). 전부 들어가면 true */
function capEach(grid, minKeep){
  var uls = grid.querySelectorAll(".dsec ul"), ok = true, u;
  for(u = 0; u < uls.length; u++){
    var ul = uls[u], cap = 12;
    capList(ul, cap);
    while(cap > minKeep && ul.scrollHeight > ul.clientHeight + 1){ cap--; capList(ul, cap); }
    if(ul.scrollHeight > ul.clientHeight + 1) ok = false;
  }
  return ok;
}
/* 칸 안의 목록이 칸 높이를 넘는지 */
function overflowing(grid){
  var uls = grid.querySelectorAll(".dsec ul"), i;
  for(i=0;i<uls.length;i++) if(uls[i].scrollHeight > uls[i].clientHeight + 1) return true;
  return false;
}
/* 크기 단위는 vh 가 아니라 --tvu 입니다. 세로 휴대폰 미리보기처럼
   판 전체를 축소하는 화면에서는 --tvu 가 px 로 바뀌기 때문입니다. */
function setGridSize(grid, s){
  grid.style.setProperty("--tv-li", "calc(var(--tvu, 1vh) * " + s + ")");
  grid.style.setProperty("--tv-h3", "calc(var(--tvu, 1vh) * " + (s * 0.95).toFixed(3) + ")");
}
/* 칸마다 최대 cap 줄까지만 남기고 접습니다.
   지난 예약부터 접는 이유: 손님이 이 화면에서 알고 싶은 건 '앞으로 언제 자리가 차는지'라
   이미 지나간 시각은 자리를 차지할 값어치가 가장 낮습니다. */
function capLists(grid, cap){
  var uls = grid.querySelectorAll(".dsec ul");
  for(var u=0; u<uls.length; u++) capList(uls[u], cap);
}
function capList(ul, cap){
  {
    var items = [], k;
    var all = ul.querySelectorAll("li");
    for(k=0; k<all.length; k++) if(all[k].className.indexOf("more") < 0) items.push(all[k]);
    var keep = ul.className.indexOf("two-col") >= 0 ? cap * 2 : cap;   /* 홀은 2열 */
    for(k=0; k<items.length; k++) items[k].style.display = "";
    var hide = items.length - keep;
    if(hide <= 0){ setMore(ul, 0); reflowTwoCol(ul); return; }
    var done = 0;
    for(k=0; k<items.length && done<hide; k++)                 /* 먼저 지난 예약 */
      if(items[k].className.indexOf("past") >= 0){ items[k].style.display = "none"; done++; }
    for(k=items.length-1; k>=0 && done<hide; k--)              /* 그래도 넘치면 늦은 시각부터 */
      if(items[k].style.display !== "none"){ items[k].style.display = "none"; done++; }
    setMore(ul, done);
    reflowTwoCol(ul);
  }
}
function setMore(ul, n){
  var more = ul.querySelector("li.more");
  if(!n){ if(more) more.parentNode.removeChild(more); return; }
  if(!more){ more = document.createElement("li"); more.className = "more"; ul.appendChild(more); }
  more.textContent = "외 " + n + "건";
}
/* 홀은 2열 그리드라 줄 수를 남은 항목 수에 맞춰 다시 잡아야 높이가 실제로 줄어듭니다.
   (줄 수를 그대로 두면 뒤에서 지워도 열만 비고 높이는 그대로입니다) */
function reflowTwoCol(ul){
  if(ul.className.indexOf("two-col") < 0) return;
  var items = ul.children, vis = 0, more = null;
  for(var i=0; i<items.length; i++){
    if(items[i].className.indexOf("more") >= 0){ more = items[i]; continue; }   /* '외 N건' 은 줄 수에 안 넣고 맨 아래 한 줄에 가로로 */
    if(items[i].style.display !== "none") vis++;
  }
  var rows = Math.max(1, Math.ceil(vis/2));
  ul.style.gridTemplateRows = "repeat(" + rows + ",auto)" + (more ? " auto" : "");
  if(more){ more.style.gridColumn = "1 / -1"; more.style.gridRow = String(rows + 1); }
}

/* 가운데 글자를 가립니다. 이재아 → 이 * 아
   ○ 를 붙여 쓰면(이○아) TV에서 글자가 뭉쳐 보여 별표와 띄어쓰기로 바꿨습니다.
   글자 수는 그대로 지킵니다 — 네 글자면 '남 * * 수'. 외국 이름도 같은 규칙(재아 2026-09-17): 띄어쓰기는 빼고
   첫 글자와 끝 글자만 남김 — Tom Cruise → T * * * * * * * e. 서버(mask_name, patch_12차)도 같은 모양 */
function maskName(n){
  return String(n||"").trim();   /* 09-20(재아): TV 는 매장 안에 두니 이름을 가리지 않음. 서버 쪽도 patch_20차(mask_name 을 그대로 돌려줌). 아래는 옛 가림 규칙 — 되돌릴 때 */
  const s = String(n||"").trim().replace(/\s+/g, "");
  if(s.indexOf("*") >= 0) return String(n||"").trim();   /* 서버(mask_name)가 이미 가린 이름 */
  if(s.length<=1) return s;
  if(s.length===2) return s[0] + " *";
  var mid = "*";
  for(var i=1; i<s.length-2; i++) mid += " *";
  return s[0] + " " + mid + " " + s[s.length-1];
}

/* 손님용 화면은 두 가지입니다.
     list — 왼쪽 영상 + 오른쪽 시각순 예약 (기본). 입구 TV 기준
     grid — 좌석별 격자 (예전 방식, 보조)
   입구에서 손님은 지나가면서 3~5초 봅니다. 좌석별 격자는 '직원의 사고방식'이라
   손님은 자기 예약을 찾기 어렵습니다. 그래서 시각순을 기본으로 두었습니다. */
/* 목록형/좌석표 — 매장 설정(settings.tvType). TV 가 로그인 없이 공개 뷰로 읽는 값이라 기기 설정(_ui)이면 안 됩니다 (7차) */
function tvType(){
  if(view.tvTypeLocal) return view.tvTypeLocal;   /* TV 에서 리모컨으로 바꾼 것 — 저장은 못 하니 이 화면에서만 */
  var st = view.storeKey && DATA && DATA[view.storeKey] ? DATA[view.storeKey].settings : null;
  var t = st && st.tvType ? st.tvType : (DATA && DATA._ui ? DATA._ui.tvType : null);
  return t === "list" ? "list" : "grid";   /* 09-20(재아): 좌석표가 기본. 목록은 설정에서 고른 경우만 */
}
function setTvType(t){
  if(readonlyBlock()) return;
  t = (t === "grid" ? "grid" : "list");
  /* 설정 화면(임시본) 안의 버튼이라 임시본과 실제 설정에 같이 씁니다 — 아니면 '적용하기' 가 옛값으로 되돌립니다 */
  if(view.draft) view.draft.tvType = t;
  store().settings.tvType = t;
  saveData(); render();
}
/* TV 에는 마우스가 없을 수 있습니다. 전환 버튼은 보조이고,
   평소 쓸 방식은 설정에서 정해 둡니다. 고른 값은 새로고침해도 남습니다. */
function swapTvType(){
  var next = tvType() === "grid" ? "list" : "grid";
  if(DATA && DATA._readonly){ view.tvTypeLocal = next; render(); }   /* 공개 TV 는 저장이 안 되므로 막지 않고 화면만 바꿉니다(점검 T3) */
  else setTvType(next);
  setTimeout(function(){ pokeExit(4000); }, 60);
}

/* 광고 영상이 뜨기 전 빙글이 — 파일이 커서(29MB) 첫 프레임까지 몇 초 걸립니다. 재생이 시작되면(playing) 지웁니다.
   오류로 영상이 빠지면 사진이 드러나므로 그때도 지우고, 혹시 이벤트가 안 오면 15초 뒤에 지웁니다 */
function tvVideoReady(v){
  var box = v && v.parentNode, sp = box && box.querySelector(".tv-loading");
  if(sp && sp.parentNode) sp.parentNode.removeChild(sp);
}
setInterval(function(){
  document.querySelectorAll(".tv-loading").forEach(function(sp){
    var t = Number(sp.getAttribute("data-t") || 0) + 1; sp.setAttribute("data-t", t);
    if(t >= 15 && sp.parentNode) sp.parentNode.removeChild(sp);
  });
}, 1000);
/* 오늘 남은 예약이 없고 설정(tvIdleFull, 기본 켬)이 켜져 있으면 목록/좌석표 대신 광고만 전체 화면 */
function tvIdle(){
  var s = store() || DATA.hanok; if(!s) return false;
  if(s.settings.tvIdleFull === false) return false;
  var today = todayStr(), now = toMin(nowHM());
  return !s.reservations.some(function(r){ return r.date === today && (r.status === "확정" || r.status === "방문") && toMin(r.time) + 30 >= now; });
}
function renderTvIdle(){
  var st = (store() || DATA.hanok).settings, ad = (st.tvAd || "").trim();
  return `
    <div class="tvl tvl-idle">
      <div class="tvl-ad">
        <div class="tvl-bgs" aria-hidden="true">
          ${[1,2,3,4,5,6,7].map(i => `<div class="tv-bg b${i} ${i===(view.bgIndex||1)?'on':''}"></div>`).join("")}
        </div>
        ${ad ? `<video src="${esc(adUrl(ad))}" autoplay muted loop playsinline
                  onplaying="tvVideoReady(this)" onerror="tvVideoReady(this); this.parentNode.removeChild(this)"></video>
        <div class="tv-loading" aria-hidden="true"><i></i></div>` : ""}
      </div>
    </div>`;
}
function renderDisplay(){
  var idle = tvIdle(); TV_IDLE_SHOWN = idle;   /* 지금 그린 상태를 기억 — 1분 갱신이 이것과 비교해 바뀔 때만 통째로 다시 그립니다 */
  var inner = idle ? renderTvIdle() : (tvType() === "grid" ? renderTvGrid() : renderTvList());
  return `
  <div class="tv tv-mode-${idle ? "list" : tvType()} ${idle ? "tv-idle" : ""}">
    <div class="tv-stage">${inner}</div>
    <div class="tv-hot" aria-hidden="true" onmouseenter="pokeExit(6000)"></div>   <!-- 마우스가 버튼으로 옮겨가는 사이 사라지지 않게 6초 유지 -->
    <div class="tv-tap" aria-hidden="true" onclick="pokeExit(5000)" ontouchstart="pokeExit(5000)"></div>
    <button class="tv-swap" onclick="swapTvType()">${tvType()==="grid" ? "목록으로" : "좌석표로"}</button>
    <button class="tv-exit" onclick="closeDisplay()" title="Esc 로도 나갈 수 있습니다">디스플레이 종료</button>
    <div class="tv-small">
      <div class="ts-box">
        ${ICON.tv}
        <div class="ts-t">지원하지 않는 화면 크기입니다</div>
        <div class="ts-s">디스플레이 모드는 TV·모니터처럼<br>넓은 화면에서만 표시됩니다.</div>
        <button class="btn primary" onclick="closeDisplay()">돌아가기</button>
      </div>
    </div>
  </div>`;
}

/* ---------- 목록형 (기본) ----------
   왼쪽: 광고 영상. 아직 영상이 없으면 매장 사진을 천천히 넘깁니다.
   오른쪽: 오늘 예약을 시각 순으로. 좌석 이름을 줄마다 같이 답니다. */
function renderTvList(){
  const s = store() || DATA.hanok;
  const st = s.settings;
  /* 광고 영상 경로는 설정에서 넣습니다 (같은 폴더의 ad.mp4 등).
     base64 로 넣으면 안 됩니다 — 수십 MB가 되어 구형 TV 브라우저가 죽습니다. */
  const ad = (st.tvAd || "").trim();

  return `
    <div class="tvl">
      <div class="tvl-ad">
        <!-- 사진은 항상 깔아 둡니다. 영상이 있으면 그 위를 덮고,
             영상 파일이 없거나 형식이 안 맞으면(onerror) 영상만 치워 사진이 드러납니다.
             → ad.mp4 를 아직 안 올렸어도 화면이 검게 비지 않습니다. -->
        <div class="tvl-bgs" aria-hidden="true">
          ${[1,2,3,4,5,6,7].map(i => `<div class="tv-bg b${i} ${i===(view.bgIndex||1)?'on':''}"></div>`).join("")}
        </div>
        <div class="tvl-veil"></div>
        ${ad ? `<video src="${esc(adUrl(ad))}" autoplay muted loop playsinline
                  onplaying="tvVideoReady(this)" onerror="tvVideoReady(this); this.parentNode.removeChild(this)"></video>
        <div class="tv-loading" aria-hidden="true"><i></i></div>` : ""}
      </div>
      <aside class="tvl-side">${tvSideHtml()}</aside>
    </div>`;
}
/* 오른쪽 날개 속. 1분마다 이것만 갈아 끼웁니다 (영상은 그대로) */
function tvSideHtml(){
  const s = store() || DATA.hanok;
  const today = todayStr(), now = toMin(nowHM());
  /* 30분 넘게 지난 예약은 뺍니다 — 손님은 지나간 시각에 관심이 없습니다.
     저녁이 될수록 목록이 짧아져 여유가 생깁니다. */
  const live = s.reservations
    .filter(r => r.date === today && (r.status === "확정" || r.status === "방문") && toMin(r.time) + 30 >= now)
    .sort((a, b) => a.time.localeCompare(b.time));
  /* 같은 시각을 여러 번 쓰지 않고 묶습니다.
     한 줄에 한 건씩 시각을 반복하면 17:30 이 네 번 나와 자리만 먹고, 정작 손님이 찾는 이름은 적게 들어갑니다.
     시각으로 먼저 찾고 그 밑에서 이름을 찾는 것이 읽는 순서와도 맞습니다. */
  const groups = [];
  live.forEach(function(r){
    const g = groups.length ? groups[groups.length - 1] : null;
    if(g && g.time === r.time) g.items.push(r);
    else groups.push({ time:r.time, items:[r] });
  });
  const rows = groups.map(function(g){
    const items = g.items.map(function(r){
      const seat = r.roomId ? resSeatLabel(r) : "";
      return `<div class="tvl-g">
        <span class="tvl-n">${esc(maskName(r.name))} 님${r.tier ? tierTagOf(r.tier) : ""}</span>
        <span class="tvl-s">${seat ? `<span class="tvl-seat">${esc(seat)}</span>` : ""}<span class="tvl-cnt">${pplOf(r)}<small>명</small></span></span>
      </div>`;
    }).join("");
    return `<li class="tvl-r"><div class="tvl-t">${esc(g.time)}</div>${items}</li>`;
  }).join("");
  const d = new Date();
  const dateTxt = `${d.getMonth() + 1}월 ${d.getDate()}일 ${["일","월","화","수","목","금","토"][d.getDay()]}요일`;
  return `
        <div class="tvl-head">
          <div class="tvl-date">${dateTxt}</div>
          <h1>오늘의 예약</h1>
        </div>
        <ul class="tvl-rows">${rows}</ul>
        <div class="tvl-more"></div>
        <div class="tvl-foot">찾아주셔서 감사합니다${DISP_FAIL >= 3 ? '<span class="tvl-off">연결 확인 중</span>' : ""}</div>`;
}

/* ---------- 좌석표형 (기본, 09-20 재개편) ----------
   재아: 손님·직원 피드백이 "목록보다 좌석표가 낫다" → 좌석표를 기본으로 하고 판을 다시 짰습니다.
   · 층 단위로 두 기둥(1층 | 저층). 손님은 "어느 층으로 가면 되는지" 를 먼저 찾습니다. 설정의 3줄 배치(displayRows)는 더 안 씁니다.
   · 기둥 안: 룸 카드 2×2 + 아래에 그 층 테이블 카드(넓게). 룸 이름은 명조 크게, 정원은 작게.
   · 카드 안: 지난 손님은 빼고(30분), '다음 손님' 한 줄만 크게 — 나머지는 작은 줄. 비어 있으면 '예약 없음' 을 조용히.
   · TV(40~43인치, 3~5m)는 대비가 중요 — 유리판 카드 위에 흰 글자, 금색은 다음 손님 표시에만.
   fitDisplay/capLists 는 그대로 씁니다(.tv-grid · .dsec ul · li.past · li.more · two-col). */
function renderTvGrid(){
  const s = store() || DATA.hanok;
  const today = todayStr();
  const nowM = toMin(nowHM());
  /* 룸은 배정된 것만, 테이블은 층 희망(seatPref)까지 — 당일에는 룸 미배정이 없도록 운영한다는 전제 */
  const list = s.reservations.filter(r=>r.date===today && (r.status==="확정"||r.status==="방문") && (r.roomId || isTablePref(r.seatPref)));
  const rooms = roomsAt(today).filter(isRoom);
  const floors = [];
  rooms.forEach(r => { const f = r.floor || ""; if(floors.indexOf(f) < 0) floors.push(f); });
  tableFloors().forEach(f => { if(floors.indexOf(f) < 0) floors.push(f); });

  const card = (title, cap, rows, hall) => {
    let nextMarked = false;
    const items = rows.map(r => {
      const past = isBlockPast(r, toMin(r.time), today, nowM);
      return `<li class="${past?'past':''}">
        <span class="t">${esc(r.time)}</span>
        <span class="n">${esc(maskName(r.name))} 님${r.tier ? tierTagOf(r.tier) : ""}${pplOf(r) >= (s.settings.groupSize || 8) ? '<span class="tier grp">단체</span>' : ""}</span>
        <span class="p">${pplOf(r)}<small>명</small></span>
      </li>`;
    }).join("");
    return `<section class="dsec ${hall?'hall':''} ${rows.length?'':'empty'}">
      <h3><span class="nm">${esc(title)}</span>${cap ? `<span class="cap">${esc(cap)}</span>` : ""}</h3>
      <ul class="${hall?"two-col":""}"${hall ? ` style="grid-template-rows:repeat(${Math.max(1,Math.ceil(rows.length/2))},auto)"` : ""}>${items}</ul>
    </section>`;
  };
  /* 09-20(재아): 층 기둥 없이 룸 8칸을 한 격자로, 그 아래 '1층 테이블'·'저층 테이블' 두 칸. 시계·'예약 없음'·다음 손님 강조는 뺌 */
  const roomCards = rooms.map(room => {
    const rows = list.filter(r => r.roomId === room.id).sort((a,b)=>a.time.localeCompare(b.time));
    return card(room.name, "", rows, false);
  }).join("");
  const hallCards = tableFloors().map(fl => {
    const trows = list.filter(r => !r.roomId && resFloor(r) !== undefined && (resFloor(r)||"") === fl).sort((a,b)=>a.time.localeCompare(b.time));
    return card(`${fl} 테이블`, "", trows, true);
  }).join("");
  const cols = [`<div class="tv-cells tv-rooms" style="grid-template-columns:repeat(${Math.min(4, Math.max(1, rooms.length))},1fr)">${roomCards}</div><div class="tv-halls" style="grid-template-columns:repeat(${Math.max(1, tableFloors().length)},1fr)">${hallCards}</div>`];

  const d = new Date();
  const dateTxt = `${d.getMonth()+1}월 ${d.getDate()}일 ${["일","월","화","수","목","금","토"][d.getDay()]}요일`;
  const clock = `${pad(d.getHours())}:${pad(d.getMinutes())}`;
  return `
      <div class="tv-bgs" aria-hidden="true">
        ${[1,2,3,4,5,6,7].map(i=>`<div class="tv-bg b${i} ${i===(view.bgIndex||1)?'on':''}"></div>`).join("")}
      </div>
      <div class="tv-inner">
        <header class="tv-h">
          <div class="tv-date">${dateTxt}</div>
          <h1>오늘의 예약 안내</h1>
          <div class="tv-line"></div>
        </header>
        <div class="tv-grid tv-one">${cols.join("")}</div>
        <footer class="tv-f">찾아주셔서 감사합니다${DISP_FAIL >= 3 ? '<span class="tvl-off">연결 확인 중</span>' : ""}</footer>
      </div>`;
}

/* 화면이 처음 그려질 때 예정 설정을 흡수합니다(불러온 직후) */
setTimeout(function(){ try{ if(AUTHED && DATA && view.storeKey){ absorbScheduled(); if(typeof pullRequests === "function"){ pullRequests().then(function(n){ if(n) render(); }); publishAvail(true); } if(typeof gsLoadMemos === "function") gsLoadMemos(); } }catch(e){} }, 1500);

/* 시트·마법사 어디서든: Enter = 그 창의 확인·등록 단추(data-enter 가 있으면 그것, 없으면 .btn.primary 하나뿐일 때만),
   Esc = 닫기. 여러 줄 입력(textarea) 안에서 Enter 는 줄바꿈이라 건드리지 않습니다. '이전' 은 일부러 안 묶습니다(재아) */
document.addEventListener("keydown", function(e){
  const t = e.target;
  if(e.key === "Escape"){
    /* 확인창(MODAL): Esc = 취소. 마법사: Esc = 닫기(입력이 있으면 확인창). 시트·더보기: 닫기 (재아 09-17: 이 셋만 묶고 나머지는 안 묶음) */
    if(MODAL){ e.preventDefault(); if(MODAL.mode === "alert") modalAnswer(true); else modalAnswer(MODAL.mode === "confirm" ? false : null); return; }
    if(WZ && !WZ.done){ e.preventDefault(); closeWizard(); return; }
    if((typeof hrEsc === "function" && hrEsc()) || (typeof gsEsc === "function" && gsEsc())){ e.preventDefault(); return; }   /* 워크시프트·손님 화면 안의 작은 창부터 */
    if(typeof thEsc === "function" && thEsc()){ e.preventDefault(); return; }
    if(typeof cdEsc === "function" && cdEsc()){ e.preventDefault(); return; }   /* 퇴근하기 안의 워크시프트·감사 문자 팝업 */
    if(view.form && view.form.type === "site" && SA && (SA.postZoom != null || SA.postPreview)){ e.preventDefault(); SA.postZoom = null; SA.postPreview = null; render(); return; }
    if(view.form){ e.preventDefault(); closeSheet(); }
    else if(view.moreOpen){ closeMore(); }
    return;
  }
  /* 대시보드 단축키(09-20 재아): / = 예약 검색, + 또는 = = 예약 등록. 입력칸에 커서가 있거나 창이 떠 있으면 안 됨 */
  if(!MODAL && !WZ && !view.form && view.tab === "dash" && AUTHED && !view.display && !(t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable))){
    if(e.key === "/"){ e.preventDefault(); openSearch(); return; }
    if(e.key === "+" || e.key === "="){ e.preventDefault(); openWizard(); return; }
  }
  /* 숫자 비밀번호 팝업: 키보드 숫자·Backspace 도 받음 */
  if(MODAL && MODAL.mode === "pin"){ if(/^[0-9]$/.test(e.key)){ e.preventDefault(); pinModalPush(e.key); } else if(e.key === "Backspace"){ e.preventDefault(); pinModalPush("back"); } return; }
  if(e.key !== "Enter" || e.ctrlKey || e.altKey || e.isComposing) return;
  if(t && (t.tagName === "TEXTAREA" || t.tagName === "BUTTON" || t.tagName === "A" || t.isContentEditable)) return;
  if(MODAL){
    /* 확인창: Enter = 확인. 고르기(choice)는 답이 여럿이라 안 묶음. 입력창(prompt)은 자기 Enter 가 있음 */
    if(MODAL.mode === "alert" || MODAL.mode === "confirm"){ e.preventDefault(); modalAnswer(true); }
    return;
  }
  if(WZ && !WZ.done){
    /* 마법사: Enter = 다음/예약 등록(막혀 있으면 아무 일도 없음) */
    const nb = document.getElementById("wz-next");
    if(nb && !nb.disabled){ e.preventDefault(); nb.click(); }
    return;
  }
  const sheet = document.querySelector(".sheet");
  if(!sheet) return;
  let btn = sheet.querySelector("[data-enter]:not(:disabled)");
  if(!btn){ const ps = sheet.querySelectorAll(".sheet-actions .btn.primary:not(:disabled)"); if(ps.length === 1) btn = ps[0]; }
  if(btn){ e.preventDefault(); btn.click(); }
});
