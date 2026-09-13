# -*- coding: utf-8 -*-
"""v5 7차-G — 재아 검토 (2026-09-14)
   1 충돌: 선택지 없이 '작성 도중 다른 기기에서 수정됨' 안내 + 화면을 서버 내용으로. 다시 하면 충돌 없음
   2 잠정 배정: 서버에서 읽은 뒤(첫 로드·델타) 오늘 이후 날짜를 다시 계산 — 시드처럼 밖에서 들어온 예약도 겹치지 않게
   3 TV: '오늘 예약이 없습니다' → 빈칸
   4 TV: 예약이 없으면 광고만 전체 화면(settings.tvIdleFull, 기본 켬). 목록/좌석표 무관. 설정에서 끔
   5 영업시간 세 칸 가운데 정렬
   6 상단 날짜를 페이지 기준 가운데(grid 1fr auto 1fr)
   7 날짜 선택 달력 항상 6줄(42칸)
   8 새로고침 버튼의 'N분 전' 삭제. 1분 자동 갱신은 바뀐 것이 있을 때만 다시 그림(입력 중엔 원래부터 안 그림)
   9 범례 '오늘 변동' → '변동'"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---------- 1. 충돌 = 실패 + 최신으로 ----------
a = s.index('  var title = t.deleted_at ? "다른 기기에서 이미 삭제된 예약입니다" : "다른 기기에서 먼저 수정됐습니다";')
b = s.index('/* 키 순서에 상관없는 JSON')
s = s[:a] + """  /* 선택지를 주지 않습니다(재아 결정) — 서버 내용으로 화면을 바꾸고 다시 하라고 알립니다. 다시 하면 그때는 충돌이 아닙니다 */
  var title = t.deleted_at ? "다른 기기에서 이미 삭제된 예약입니다" : "작성 도중 다른 기기에서 수정된 내용입니다";
  var li = st.reservations.indexOf(rec), ti = st.trash.indexOf(rec);
  if(li >= 0) st.reservations.splice(li, 1); if(ti >= 0) st.trash.splice(ti, 1);
  if(t.deleted_at) st.trash.push(trec); else st.reservations.push(trec);
  st.reservations.sort(function(a, b){ return (a.date + a.time).localeCompare(b.date + b.time); });
  SYNC.res[rec.id] = JSON.stringify(trec); if(t.updated_at > (SYNC.lastUpd[k] || "")) SYNC.lastUpd[k] = t.updated_at;
  render();
  await uiAlert(title, conflictSummary(rec, trec) + "\\n\\n내 변경은 저장되지 않았고 화면을 최신 내용으로 바꿨습니다. 다시 수정해 주세요.", "warn");
}
""" + s[b:]
rep("""  return out.length ? "상대 기기의 내용:\\n" + out.join("\\n") : "상대 기기의 내용은 화면과 같지만 나중에 저장됐습니다.";""",
    """  return out.length ? "내가 입력한 것 → 지금 저장된 것:\\n" + out.join("\\n") : "다른 기기가 나중에 저장했습니다.";""")

# ---------- 2. 잠정 배정 다시 계산 ----------
rep("""async function enterStore(){
  var d = await loadFromServer();
  DATA = assembleData(d);
  AUTHED = true; OFFLINE = null; LOAD_ERROR = null;
  cacheSave();
  autoCloseDays();   /* 지난 날짜의 '확정' → '방문' (이 기기가 처음 켠 것이면 여기서 올라갑니다) */
  takeSnapshot();
}""",
"""async function enterStore(){
  var d = await loadFromServer();
  DATA = assembleData(d);
  AUTHED = true; OFFLINE = null; LOAD_ERROR = null;
  cacheSave();
  autoCloseDays();   /* 지난 날짜의 '확정' → '방문' (이 기기가 처음 켠 것이면 여기서 올라갑니다) */
  takeSnapshot();
  reflowFuture();    /* 잠정 배정은 겹침을 봐야 하므로 다른 곳에서 들어온 예약까지 포함해 다시 계산 */
}
/* 오늘 이후 날짜의 잠정 배정(룸 미정 예약의 tentativeRoomId)을 다시 계산합니다.
   잠정 배정은 그 날 다른 예약과의 겹침으로 정해지는 값이라, 다른 기기·시드·복구로 들어온 예약이 있으면 틀어집니다.
   바뀐 것은 saveData → flush 로 올라가고, 두 기기가 같은 답을 내면 충돌로 치지 않습니다(pushChanged 의 같은 내용 처리) */
function reflowFuture(){
  /* 세션 복구 때는 아직 view.storeKey 가 없을 수 있어(주소 적용 전) 매장을 직접 돌며 잠시 storeKey 를 바꿉니다 — reflowTentatives 가 store() 를 쓰므로 */
  var prev = view.storeKey, today = todayStr(), changed = false;
  Object.keys(DEFAULT_DATA).forEach(function(k){
    if(!DEFAULT_DATA[k].enabled || !DATA || !DATA[k]) return;
    view.storeKey = k;
    var s = DATA[k], dates = {};
    s.reservations.forEach(function(r){ if(r.date >= today && !r.roomId && holdsSeat(r)) dates[r.date] = 1; });
    Object.keys(dates).forEach(function(d){
      var before = s.reservations.filter(function(r){ return r.date === d && !r.roomId; }).map(function(r){ return r.id + ":" + (r.tentativeRoomId || ""); }).join(",");
      reflowTentatives(d);
      var after = s.reservations.filter(function(r){ return r.date === d && !r.roomId; }).map(function(r){ return r.id + ":" + (r.tentativeRoomId || ""); }).join(",");
      if(before !== after) changed = true;
    });
  });
  view.storeKey = prev;
  if(changed) saveData();
}""")
rep("""  if(changed) cacheSave();
}""",
"""  if(changed){ cacheSave(); reflowFuture(); }
  return changed;
}""")

# ---------- 3·4. TV 빈칸 · 예약 없으면 광고만 ----------
rep("""        <ul class="tvl-rows">${rows || `<li class="tvl-none">오늘 예약이 없습니다</li>`}</ul>""",
    """        <ul class="tvl-rows">${rows}</ul>""")
rep("""    }).join("") : `<li class="none">예약 없음</li>`;""",
    """    }).join("") : ``;""")
rep("""function renderDisplay(){
  var inner = tvType() === "grid" ? renderTvGrid() : renderTvList();
  return `
  <div class="tv tv-mode-${tvType()}">""",
"""/* 오늘 남은 예약이 없고 설정(tvIdleFull, 기본 켬)이 켜져 있으면 목록/좌석표 대신 광고만 전체 화면 */
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
                  onerror="this.parentNode.removeChild(this)"></video>` : ""}
      </div>
    </div>`;
}
function renderDisplay(){
  var idle = tvIdle(); TV_IDLE_SHOWN = idle;   /* 지금 그린 상태를 기억 — 1분 갱신이 이것과 비교해 바뀔 때만 통째로 다시 그립니다 */
  var inner = idle ? renderTvIdle() : (tvType() === "grid" ? renderTvGrid() : renderTvList());
  return `
  <div class="tv tv-mode-${idle ? "list" : tvType()} ${idle ? "tv-idle" : ""}">""")
rep("""function updateDisplayInPlace(){
  if(!view.display) return;
  var side = document.querySelector(".tvl-side");
  if(tvType() !== "grid" && side){""",
"""var TV_IDLE_SHOWN = null;
function updateDisplayInPlace(){
  if(!view.display) return;
  /* 광고만 ↔ 목록 이 바뀌는 순간에만 통째로 다시 그립니다 (영상이 처음부터 다시 시작되는 건 이때뿐) */
  var idle = tvIdle();
  if(idle !== TV_IDLE_SHOWN){ render(); return; }
  if(idle) return;
  var side = document.querySelector(".tvl-side");
  if(tvType() !== "grid" && side){""")
rep(""".tvl-none{color:#9C8D76; font-size:calc(var(--tvu)*2.2); text-align:center;""",
    """/* 예약이 없을 때 광고만 — 날개 없이 영상이 화면 전체. 사진 위 어둡게 하는 막(veil)도 없음 */
.tvl-idle .tvl-ad{flex:1 1 100%}
.tv-idle .tv-swap{display:none}
.tvl-none{color:#9C8D76; font-size:calc(var(--tvu)*2.2); text-align:center;""")
rep("""    <div class="subhead">광고 영상 <span>목록 화면 왼쪽에 나옵니다</span></div>""",
"""    <div class="subhead">예약이 없을 때</div>
    <div class="seg">
      <button class="${st.tvIdleFull!==false?'on':''}" onclick="setPolicy('tvIdleFull', true)">광고만 전체 화면</button>
      <button class="${st.tvIdleFull===false?'on':''}" onclick="setPolicy('tvIdleFull', false)">빈 목록 그대로</button>
    </div>
    <p class="f-note">오늘 남은 예약이 하나도 없으면(30분 넘게 지난 것은 빼고) 목록·좌석표 대신 광고 영상만 화면 가득 틉니다. 예약이 생기면 다음 갱신(1분) 때 목록으로 돌아옵니다.</p>

    <div class="subhead">광고 영상 <span>목록 화면 왼쪽에 나옵니다</span></div>""")

# ---------- 5. 영업시간 가운데 ----------
rep(""".hours-line .hl-c{min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; padding:0 var(--s8); font-weight:600}
.hours-line .hl-c:first-child{padding-left:0}""",
""".hours-line .hl-c{min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; padding:0 var(--s8); font-weight:600; text-align:center}""")

# ---------- 6. 날짜 페이지 가운데 ----------
rep(""".topbar-in{display:flex; width:100%; max-width:1720px; margin:0 auto; padding:var(--s12) var(--s24); gap:var(--s8); align-items:center}""",
""".topbar-in{display:flex; width:100%; max-width:1720px; margin:0 auto; padding:var(--s12) var(--s24); gap:var(--s8); align-items:center}
/* 넓은 화면: 날짜를 '페이지' 기준 가운데에 — 양옆(로고 / 버튼 묶음)이 폭이 달라도 가운데 칸이 정중앙에 옵니다.
   좁은 화면(900px 이하)은 날짜가 둘째 줄로 내려가므로 flex 그대로 */
@media (min-width:901px){
  .topbar-in{display:grid; grid-template-columns:1fr auto 1fr; align-items:center}
  .topbar-in .storename{justify-self:start}
  .topbar-in .bar-right{justify-self:end}
  .topbar-in .more-veil{grid-column:1 / -1}
}""")

# ---------- 7. 날짜 선택 6줄 ----------
rep("""    </button>`;
  }
  return `
    <div class="overlay" onclick="closeCal()">""",
"""    </button>`;
  }
  /* 항상 6줄(42칸) — 5줄짜리 달과 6줄짜리 달을 오갈 때 높이가 바뀌어 손이 헛나갔습니다 */
  for(let i=lead+lastDay; i<42; i++) cells += `<span class="cday blank"></span>`;
  return `
    <div class="overlay" onclick="closeCal()">""")

# ---------- 8. 새로고침 'N분 전' 삭제 · 자동 갱신은 바뀐 것이 있을 때만 ----------
rep("""          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}<span class="rf-at" id="rf-at">${refreshedAgo()}</span></button>""",
    """          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}</button>""")
rep("""/* 대시보드는 1분마다 스스로 갱신합니다. 갱신 시각 글자만은 30초마다 따로 고쳐 씁니다(전체를 다시 그리지 않게) */
setInterval(function(){""",
"""/* 대시보드는 1분마다 스스로 갱신합니다 — 서버에서 바뀐 행만 받아 오고, 실제로 바뀐 것이 있을 때만 다시 그립니다.
   마법사·시트·확인창이 떠 있으면 건너뜁니다(입력 중에 화면이 바뀌면 안 되니까). '새로고침' 버튼은 즉시 + 무조건 다시 그림 */
setInterval(function(){""")
rep("""  if(!AUTHED || view.display || WZ || view.form || MODAL) return;
  refreshData().then(function(){ render(); });
}, 60000);
setInterval(function(){
  var el = document.getElementById("rf-at");
  if(el) el.textContent = refreshedAgo();
}, 30000);""",
"""  if(!AUTHED || view.display || WZ || view.form || MODAL) return;
  refreshData().then(function(changed){ if(changed) render(); });
}, 60000);""")
rep("""async function refreshData(){
  try{
    await reloadFromStore();
    LAST_REFRESH = Date.now();
  }catch(e){""",
"""async function refreshData(){
  try{
    var changed = await reloadFromStore();
    LAST_REFRESH = Date.now();
    return changed !== false;   /* 서버 모드는 바뀐 것이 있는지 돌려줍니다. 그 밖(undefined)은 '모름' = 다시 그림 */
  }catch(e){""")
rep(""".b-refresh{gap:6px !important}
.b-refresh .rf-at{font-size:11.5px; font-weight:600; color:var(--text-3); letter-spacing:0}
""", "")
rep(""".topbar.notoday .rf-at{color:rgba(255,255,255,.7)}
""", "")

# ---------- 9. 범례 ----------
rep("""        <span class="tl-legend"><i class="lgsw chg"></i>오늘 변동</span>""",
    """        <span class="tl-legend"><i class="lgsw chg"></i>변동</span>""")

# ---------- 보강: 새로고침 'N분 전' 함수 제거 · 잠정 배정은 아무것도 없는 방을 먼저 ----------
rep("""function refreshedAgo(){
  var sec = Math.max(0, Math.round((Date.now() - LAST_REFRESH) / 1000));
  if(sec < 60) return "방금";
  var m = Math.round(sec / 60);
  if(m < 60) return m + "분 전";
  return Math.floor(m / 60) + "시간 전";
}
""", "")
rep("""  for(const r of rooms){
    if(roomStatus(date,time,r.id,excludeId).state==="free") return r.id;
  }
  const halls = cand.filter(r=>r.type==="hall" && !blockedAt(r, date, time)).sort((a,b)=>hallSeatTotal(b)-hallSeatTotal(a));""",
"""  /* 1순위: 확정도 잠정도 아무것도 없는 방. 2순위: 잠정만 있고 그 잠정이 다른 데로 옮길 수 있는 방(옛 규칙).
     2순위만 있으면 잠정 두 건이 같은 방을 잡아 화면에 겹쳐 보였습니다 (7차-G) */
  for(const r of rooms){
    const rs = roomStatus(date,time,r.id,excludeId);
    if(rs.state==="free" && !rs.movable.length && !rs.tentative.length) return r.id;
  }
  for(const r of rooms){
    if(roomStatus(date,time,r.id,excludeId).state==="free") return r.id;
  }
  const halls = cand.filter(r=>r.type==="hall" && !blockedAt(r, date, time)).sort((a,b)=>hallSeatTotal(b)-hallSeatTotal(a));""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_g 적용 완료")

# 빈 칸도 같은 높이 — min-height:0 이면 42칸을 채워도 마지막 줄이 접혀 높이가 달라집니다
import io as _io
_s = _io.open(P, encoding="utf-8").read()
_s = _s.replace(".cday.blank{border:none; background:none; min-height:0}", ".cday.blank{border:none; background:none}   /* min-height 를 0 으로 두면 마지막 빈 줄이 접혀 5줄·6줄 높이가 달라집니다(7차-G) */")
_io.open(P, "w", encoding="utf-8", newline="\n").write(_s)
# 칸 높이도 고정 — 건수·막대가 있는 칸(≈72px)과 빈 칸(62px)이 섞이면 달마다 10px 씩 달라집니다
_s = _io.open(P, encoding="utf-8").read().replace(".cday{min-height:62px;", ".cday{min-height:74px;")
_io.open(P, "w", encoding="utf-8", newline="\n").write(_s)
