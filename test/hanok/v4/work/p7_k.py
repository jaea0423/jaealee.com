# -*- coding: utf-8 -*-
"""v4 6차-K — 7차(Supabase) 전 정리 (2026-09-14 재아 결정)
   1 관리 화면에도 해시 주소 — #/hanok · #/hanok/settings · #/hanok/2026-09-20. 새로고침해도 그 자리.
     폴더로 나누지 않습니다(파일 하나 원칙·로그인 상태 전달·Supabase 연동 세 곳 문제). 디스플레이의 #/screen/hanok 은 그대로
   2 설정 화면: 점 3개 메뉴 → 나가기 아이콘 버튼 하나 (좌측 HANOK 과 같은 역할)
   3 HANOK 왼쪽 매장 아이콘·설정의 ← 삭제. 글자만
   4 '오늘로' 버튼 — 오늘이 아닐 때만, 새로고침과 예약 검색 사이, 예약 검색과 같은 알약"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ============================================================
# 1. 해시 주소
# ============================================================
rep("""  if(applyRoute()){
    document.addEventListener("keydown", escDisplay);
  }
  render();
  /* 뒤로 가기·주소 변경에도 반응 */
  window.addEventListener("hashchange", ()=>{ if(applyRoute()) render(); });
}""",
"""  if(applyRoute()){
    document.addEventListener("keydown", escDisplay);
  }else{
    applyAdminRoute();   /* #/hanok/settings 처럼 관리 화면 주소로 들어온 경우 */
  }
  render();
  /* 뒤로 가기·주소 변경에도 반응 */
  window.addEventListener("hashchange", ()=>{ if(applyRoute() || applyAdminRoute()) render(); });
}""")

rep("""/* 주소를 바꿔 둡니다 (파일로 열었을 때는 조용히 실패해도 괜찮습니다) */
function setRoute(toScreen){""",
"""/* ---------- 관리 화면 주소 (6차-K) ----------
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
  var hash = (location.hash || "").replace(/^#/, "").replace(/\\/+$/, "");
  var m = hash.match(/^\\/([a-z]+)(?:\\/(settings|\\d{4}-\\d{2}-\\d{2}))?$/i);
  if(!m || !DATA || !DATA[m[1].toLowerCase()] || !DATA[m[1].toLowerCase()].enabled) return false;
  var key = m[1].toLowerCase(), sub = m[2] || "";
  var tab = sub === "settings" ? "settings" : "dash";
  var date = /^\\d{4}-\\d{2}-\\d{2}$/.test(sub) ? sub : todayStr();
  if(view.storeKey === key && view.tab === tab && view.date === date && !view.display) return false;   /* 이미 그 자리 — hashchange 되풀이 방지 */
  view.storeKey = key; view.tab = tab; view.date = date; view.calMonth = date.slice(0,7);
  view.display = false; view.form = null; tmpRes = null;
  if(tab === "settings") view.draft = deepClone(DATA[key].settings);   /* 설정은 임시본 위에서 편집합니다(setTab 과 같게) */
  return true;
}
/* 주소를 바꿔 둡니다 (파일로 열었을 때는 조용히 실패해도 괜찮습니다) */
function setRoute(toScreen){""")

# 그릴 때마다 주소 맞춤 — renderApp 끝(afterRender 앞)
rep("""  app.innerHTML = (view.display ? renderDisplay()
                  : (view.storeKey ? renderStore() : renderSelect())) + renderModal() + renderLoadError();
  afterRender();   /* 화면을 그린 뒤 필요한 이벤트 연결 (분 조절 레일 등) */
}""",
"""  app.innerHTML = (view.display ? renderDisplay()
                  : (view.storeKey ? renderStore() : renderSelect())) + renderModal() + renderLoadError();
  syncHash();      /* 주소를 지금 화면에 맞춥니다 — 새로고침해도 그 자리로 */
  afterRender();   /* 화면을 그린 뒤 필요한 이벤트 연결 (분 조절 레일 등) */
}""")
# 잠금 화면에서도 주소는 목적지(예: #/hanok/settings)를 유지해야 PIN 뒤에 거기로 갑니다
rep("""  if(view.storeKey && !AUTHED){ app.innerHTML = renderLock() + renderModal(); afterRender(); return; }""",
    """  if(view.storeKey && !AUTHED){ app.innerHTML = renderLock() + renderModal(); syncHash(); afterRender(); return; }""")
# 매장 선택으로 나가면 주소도 비웁니다 (goHome → storeKey null → syncHash 가 "" 로)  ※ 별도 코드 불필요

# ============================================================
# 2·3·4. 상단바
# ============================================================
rep("""        <!-- 매장 이름 = 예전 맨 왼쪽 버튼의 역할. 대시보드에서는 매장 선택으로, 설정에서는 대시보드로 -->
        <button class="storename" onclick="${view.tab==="settings"?"setTab('dash')":"goHome()"}"
          title="${view.tab==="settings"?"대시보드로":"매장 선택"}">${view.tab==="settings"?'<span class="sn-ic">←</span>':ICON.store}<span class="sn-brand">HANOK</span></button>
""",
"""        <!-- 매장 이름 = 예전 맨 왼쪽 버튼의 역할. 대시보드에서는 매장 선택으로, 설정에서는 대시보드로. 아이콘·화살표 없이 글자만(6차-K) -->
        <button class="storename" onclick="${view.tab==="settings"?"setTab('dash')":"goHome()"}"
          title="${view.tab==="settings"?"대시보드로":"매장 선택"}"><span class="sn-brand">HANOK</span></button>
""")
rep("""        <div class="bar-right">
          ${view.tab==="settings" ? "" : `
          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}<span class="rf-at" id="rf-at">${refreshedAgo()}</span></button>
          <button class="tvbtn b-search" onclick="openSearch()">예약 검색</button>
          <button class="tvbtn accent b-add" onclick="openWizard('${view.date}')">＋ 예약 등록</button>`}
          <!-- 더보기(⋮): 자주 안 쓰는 것들을 여기로 모았습니다 — 예약률 추이 · 설정 · 디스플레이 모드 -->
          <div class="more-wrap">
            <button class="tvbtn icon b-more ${view.moreOpen?'on':''}" onclick="toggleMore()" title="더보기" aria-label="더보기">${ICON.more}</button>
            ${view.moreOpen ? `
            <div class="more-menu">
              ${view.tab==="settings" ? "" : `<button onclick="closeMore(); openRate()">${ICON.chart}<span>예약률 추이</span></button>`}
              <button onclick="closeMore(); setTab('${view.tab==="settings"?"dash":"settings"}')">${ICON.set}<span>${view.tab==="settings"?"설정 닫기":"설정"}</span></button>
              <button onclick="closeMore(); openDisplay()">${ICON.tv}<span>디스플레이 모드</span></button>
            </div>` : ""}
          </div>
        </div>""",
"""        <div class="bar-right">
          ${view.tab==="settings" ? `
          <!-- 설정에서는 점 3개 대신 나가기 하나 (좌측 HANOK 과 같은 역할). 디스플레이 모드는 대시보드 메뉴에 있습니다 (6차-K) -->
          <button class="tvbtn icon b-exit" onclick="setTab('dash')" title="설정 나가기" aria-label="설정 나가기">${ICON.exit}</button>` : `
          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}<span class="rf-at" id="rf-at">${refreshedAgo()}</span></button>
          ${view.date===todayStr() ? "" : `<button class="tvbtn b-today" onclick="goToday()">오늘로</button>`}
          <button class="tvbtn b-search" onclick="openSearch()">예약 검색</button>
          <button class="tvbtn accent b-add" onclick="openWizard('${view.date}')">＋ 예약 등록</button>
          <!-- 더보기(⋮): 자주 안 쓰는 것들을 여기로 모았습니다 — 예약률 추이 · 설정 · 디스플레이 모드 -->
          <div class="more-wrap">
            <button class="tvbtn icon b-more ${view.moreOpen?'on':''}" onclick="toggleMore()" title="더보기" aria-label="더보기">${ICON.more}</button>
            ${view.moreOpen ? `
            <div class="more-menu">
              <button onclick="closeMore(); openRate()">${ICON.chart}<span>예약률 추이</span></button>
              <button onclick="closeMore(); setTab('settings')">${ICON.set}<span>설정</span></button>
              <button onclick="closeMore(); openDisplay()">${ICON.tv}<span>디스플레이 모드</span></button>
            </div>` : ""}
          </div>`}
        </div>""")

# 나가기 아이콘 — ICON 에 추가 (more 옆)
rep("""  more:'<svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="1.6" fill="currentColor" stroke="none"/>""",
    """  exit:'<svg viewBox="0 0 24 24"><path d="M14 4h5a1 1 0 011 1v14a1 1 0 01-1 1h-5"/><path d="M10 17l5-5-5-5M15 12H3"/></svg>',
  more:'<svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="1.6" fill="currentColor" stroke="none"/>""")
# 매장 아이콘 정의는 더 쓰는 곳이 없어 지웁니다
import re
n0 = len(s)
s = re.sub(r"  store:'<svg viewBox=\"0 0 24 24\">.*?</svg>',\n", "", s, count=1)
assert len(s) < n0, "ICON.store 삭제 실패"

# 오늘로 — 6차-F 에서 지운 goToday 복구
rep("""/* '오늘이 아닌 날짜를 보는 중' — 상단바(.topbar.notoday)와 body.notoday 가 같은 조건을 써야 하므로 한 곳에.
   설정 탭은 날짜 개념이 없어 제외. 디스플레이·잠금·인트로는 renderApp 이 renderStore 전에 갈라져 나가므로 여기서도 빼 둡니다.
   ('오늘' 버튼과 goToday 는 6차-F 에서 삭제 — 오늘로 돌아올 때도 날짜를 눌러 달력에서 고릅니다) */""",
"""/* '오늘로' 버튼 — 오늘이 아닐 때만 상단바 오른쪽(새로고침과 예약 검색 사이)에. 6차-F 에서 뺐다가 6차-K 에서 되살림 */
function goToday(){ view.date = todayStr(); view.calMonth = monthStr(); render(); }
/* '오늘이 아닌 날짜를 보는 중' — 상단바(.topbar.notoday)와 body.notoday 가 같은 조건을 써야 하므로 한 곳에.
   설정 탭은 날짜 개념이 없어 제외. 디스플레이·잠금·인트로는 renderApp 이 renderStore 전에 갈라져 나가므로 여기서도 빼 둡니다 */""")

# CSS — 아이콘 자리 규칙 정리, 좁은 화면 순서에 오늘로 끼움
rep("""/* ---- 상단바: 맨 왼쪽 버튼을 없애고 매장 이름이 그 일을 합니다 ---- */
.storename{gap:var(--s8)}
.storename svg{width:18px; height:18px; stroke:currentColor; fill:none; stroke-width:1.7; flex:none; opacity:.8}
.storename .sn-ic{font-size:var(--fs-body); opacity:.8}
""",
"""/* ---- 상단바: 맨 왼쪽 버튼을 없애고 매장 이름이 그 일을 합니다 (6차-K 부터 아이콘 없이 HANOK 글자만) ---- */
""")
rep(""".storename svg{opacity:1}
""", "")
rep("""  .b-search{order:4; flex:0 1 auto}
  .b-add{order:5; flex:0 1 auto}""",
"""  .b-today{order:4; flex:0 1 auto}
  .b-search{order:5; flex:0 1 auto}
  .b-add{order:6; flex:0 1 auto}""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_k ok")
