# -*- coding: utf-8 -*-
"""v4 5차 — 손님용 화면(디스플레이)을 별도 주소 screen/ 로, 방치해도 되는(키오스크) 동작으로.
   · 1분마다 화면을 통째로 다시 그려서 광고 영상이 매분 처음부터 다시 시작하던 것 → 날개(예약 목록)만 갈아 끼움
   · 갱신 때 데이터를 다시 읽음(refreshData → 나중에 Supabase reloadFromStore)
   · 읽기가 3번 연속 실패하면 바닥글에 작게 '연결 확인 중' — 화면은 그대로(마지막 데이터)
   · 새벽 4시에 하루 한 번 통째로 새로 불러옴(오래 켜 둔 TV 브라우저의 메모리 누수 대비)
   · 주소: /v4/screen/ (폴더) — build.py 가 같은 파일을 screen/index.html 로도 만듭니다
   · 목록형 글자 다듬기(시각 명조, 이름 키움, 인원 금색)"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:70])
    s = s.replace(old, new)

# ---------- 1. 주소 처리: /screen/ 폴더·index.html 도 인식 ----------
rep("""  const path = (location.pathname || "").replace(/\\/+$/,"");
  const hash = (location.hash || "").replace(/^#/,"").replace(/\\/+$/,"");
  const raw = /screen/.test(hash) ? hash : path;""",
"""  /* v4 부터 손님용 화면은 screen/ 폴더의 index.html 입니다.
     .../screen  .../screen/  .../screen/index.html  .../screen/hanok  전부 같은 뜻으로 봅니다 */
  const path = (location.pathname || "").replace(/\\/index\\.html?$/i,"").replace(/\\/+$/,"");
  const hash = (location.hash || "").replace(/^#/,"").replace(/\\/+$/,"");
  const raw = /screen/.test(hash) ? hash : path;""")

# 앱 폴더(= screen 의 부모) 구하는 공용 함수. adUrl / screenUrl / setRoute 가 각자 정규식을 갖고 있던 것을 한 곳으로.
rep("""function adUrl(name){
  var v = (name || "").trim();
  if(!v) return "";
  /* 전체 주소나 경로를 직접 적었으면 그대로 씁니다 */
  if(v.indexOf("://") >= 0 || v.charAt(0) === "/") return v;
  try{
    var dir = location.pathname.replace(/\\/screen(\\/[a-z]+)?$/i, "").replace(/\\/[^\\/]*$/, "");
    return dir + "/" + v;
  }catch(e){ return v; }
}
function screenUrl(){
  try{
    const base = location.origin + location.pathname.replace(/\\/screen(\\/[a-z]+)?$/i,"").replace(/\\/+$/,"");
    if(location.protocol === "file:") return location.href.split("#")[0] + `#/screen/${view.storeKey}`;
    return `${base}/screen/${view.storeKey}`;
  }catch(e){ return `/screen/${view.storeKey}`; }
}""",
"""/* 앱이 놓인 폴더 경로(끝 슬래시 없음). /v4/, /v4/index.html, /v4/screen/, /v4/screen/index.html, /v4/screen/hanok 전부 → /v4 */
function appDir(){
  try{
    return location.pathname
      .replace(/\\/[^\\/]*\\.html?$/i, "")            /* index.html 떼기 */
      .replace(/\\/screen(\\/[a-z]*)?\\/?$/i, "")       /* screen 폴더(와 매장 이름) 떼기 */
      .replace(/\\/+$/, "");
  }catch(e){ return ""; }
}
/* 광고 영상은 screen/ 폴더에 둡니다 (손님용 화면과 한 묶음). 파일 이름만 적으면 그 폴더를 붙입니다 */
function adUrl(name){
  var v = (name || "").trim();
  if(!v) return "";
  /* 전체 주소나 경로를 직접 적었으면 그대로 씁니다 */
  if(v.indexOf("://") >= 0 || v.charAt(0) === "/") return v;
  return appDir() + "/screen/" + v;
}
function screenUrl(){
  try{
    if(location.protocol === "file:") return location.href.split("#")[0] + `#/screen/${view.storeKey}`;
    return location.origin + appDir() + "/screen/";
  }catch(e){ return "/screen/"; }
}""")

rep("""    const base = location.pathname.replace(/\\/screen(\\/[a-z]+)?$/i, "").replace(/\\/+$/,"");
    history.replaceState(null, "", toScreen ? `${base}/screen/${view.storeKey}` : (base || "/"));""",
"""    /* 관리 화면에서 디스플레이를 열 때는 주소만 바꿔 둡니다 (뒤로 가기·새로고침 대비).
       screen/ 은 실제 폴더라 그 안의 /hanok 은 서버에 없으므로 폴더 주소로만 갑니다 */
    const base = appDir();
    history.replaceState(null, "", toScreen ? `${base}/screen/` : (base || "/"));""")

# ---------- 2. 갱신: 통째로 다시 그리지 않고 날개만 ----------
rep("""  dispTimer = setInterval(()=>{
    if(!view.display) return;
    render();
    document.querySelectorAll(".tv-bg").forEach((el,i)=> el.classList.toggle("on", i+1===(view.bgIndex||1)));
  }, 60000);
}""",
"""  dispTimer = setInterval(displayTick, 60000);
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
function updateDisplayInPlace(){
  if(!view.display) return;
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
}""")

# ---------- 3. 목록형: 날개를 따로 만드는 함수로 분리 + 인원 금색 ----------
rep("""      <aside class="tvl-side">
        <div class="tvl-head">
          <div class="tvl-date">${dateTxt}</div>
          <h1>오늘의 예약</h1>
        </div>
        <ul class="tvl-rows">${rows || `<li class="tvl-none">오늘 예약이 없습니다</li>`}</ul>
        <div class="tvl-more"></div>
        <div class="tvl-foot">찾아주셔서 감사합니다</div>
      </aside>
    </div>`;
}""",
"""      <aside class="tvl-side">${tvSideHtml()}</aside>
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
      const seat = r.roomId ? seatLabel(r.roomId) : "";
      return `<div class="tvl-g">
        <span class="tvl-n">${esc(maskName(r.name))} 님</span>
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
        <ul class="tvl-rows">${rows || `<li class="tvl-none">오늘 예약이 없습니다</li>`}</ul>
        <div class="tvl-more"></div>
        <div class="tvl-foot">찾아주셔서 감사합니다${DISP_FAIL >= 3 ? '<span class="tvl-off">연결 확인 중</span>' : ""}</div>`;
}""")

# renderTvList 안에서 이제 안 쓰는 계산은 지웁니다 (rows·dateTxt 를 tvSideHtml 이 만듦)
a = s.index("function renderTvList(){"); b = s.index("  /* 광고 영상 경로는 설정에서 넣습니다", a)
head = """function renderTvList(){
  const s = store() || DATA.hanok;
  const st = s.settings;
"""
s = s[:a] + head + s[b:]

# ---------- 4. 목록형 글자 다듬기 ----------
rep(""".tvl-date{font-family:var(--serif-tv); font-size:calc(var(--tvu)*2);
  letter-spacing:.18em; color:#D6C4A2}""",
""".tvl-date{font-family:var(--serif-tv); font-size:calc(var(--tvu)*2);
  letter-spacing:.06em; color:#D6C4A2}""")
rep(""".tvl-t{font-size:calc(var(--tvu)*3.1); font-weight:800; color:#FFD98A;
  font-variant-numeric:tabular-nums; letter-spacing:.01em; line-height:1.15}""",
"""/* 시각은 명조 — 붉은 칠기·금박의 인트로, 날개 제목과 같은 목소리로. 숫자는 폭이 같아야 줄이 맞습니다 */
.tvl-t{font-family:var(--serif-tv); font-size:calc(var(--tvu)*3.4); font-weight:900; color:#FFD98A;
  font-variant-numeric:tabular-nums; letter-spacing:.02em; line-height:1.15}""")
rep(""".tvl-n{font-size:calc(var(--tvu)*2.3); font-weight:700; color:#FFFFFF;
  overflow:hidden; text-overflow:ellipsis; min-width:0}
.tvl-s{font-size:calc(var(--tvu)*1.9); font-weight:600; color:#C8B795; flex:none}""",
""".tvl-n{font-size:calc(var(--tvu)*2.5); font-weight:700; color:#FFFFFF; letter-spacing:-.005em;
  overflow:hidden; text-overflow:ellipsis; min-width:0}
/* 좌석은 차분하게, 인원은 금색으로 — 손님이 '내 방·내 인원'을 한눈에 찾습니다 */
.tvl-s{font-size:calc(var(--tvu)*2.1); font-weight:600; color:#C8B795; flex:none; display:inline-flex; align-items:baseline; gap:calc(var(--tvu)*1.1)}
.tvl-cnt{color:#FFD98A; font-weight:700; font-variant-numeric:tabular-nums; min-width:calc(var(--tvu)*4.2); text-align:right}
.tvl-cnt small{font-size:.78em; font-weight:600; color:#C8B795; margin-left:.12em}
.tvl-off{display:block; font-family:var(--font); font-size:.7em; letter-spacing:.04em; text-indent:0; color:#8C7B62; margin-top:calc(var(--tvu)*.6)}""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
