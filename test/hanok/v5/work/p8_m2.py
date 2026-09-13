# -*- coding: utf-8 -*-
"""7차-M 보강 — '안건표' → '리스트'. 리스트|그래프 토글을 본문에서 빼서 상단바 HANOK 옆 작은 스위치(.mswitch)로 (폰만)"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

rep("""  const graph = view.mView === "graph";
  const toggle = `<div class="mview seg">
    <button class="${graph?'':'on'}" onclick="view.mView='list'; render()">안건표</button>
    <button class="${graph?'on':''}" onclick="view.mView='graph'; render()">그래프</button>
  </div>`;
  const body = graph""",
"""  const graph = view.mView === "graph";   /* 리스트|그래프 스위치는 상단바(HANOK 옆)에 있습니다 */
  const toggle = "";
  const body = graph""")
rep("""/* 안건표 — 두 줄 행. 1줄 시각·이름·상태, 2줄 인원·좌석·전화·꼬리표. 한 줄 전체가 탭 영역 */""",
    """/* 리스트 — 두 줄 행. 1줄 시각·이름·상태, 2줄 인원·좌석·전화·꼬리표. 한 줄 전체가 탭 영역 */""")
rep("""   폰에서 사장님이 보고 싶은 건 '지금부터 뭐가 오나' 라서 시간순 안건표가 기본이고, 그래프는 토글로.""",
    """   폰에서 사장님이 보고 싶은 건 '지금부터 뭐가 오나' 라서 시간순 리스트가 기본이고, 그래프는 상단 스위치로.""")
# 상단바: HANOK 바로 옆 스위치 (대시보드 탭, 폰)
rep("""          title="${view.tab==="settings"?"대시보드로":"매장 선택"}"><span class="sn-brand">HANOK</span></button>
""",
"""          title="${view.tab==="settings"?"대시보드로":"매장 선택"}"><span class="sn-brand">HANOK</span></button>
        ${isMobile() && view.tab!=="settings" ? `
        <!-- 폰: 리스트|그래프 스위치 — 본문에 두면 자리를 크게 먹어 로고 옆으로 (7차-M) -->
        <button class="mswitch" onclick="view.mView = view.mView==='graph' ? 'list' : 'graph'; render()" aria-label="리스트/그래프 전환">
          <span class="${view.mView==='graph'?'':'on'}">리스트</span><span class="${view.mView==='graph'?'on':''}">그래프</span>
        </button>` : ``}
""")
rep("""  /* 안건표 | 그래프 토글 */
  .mview{margin-bottom:var(--s12)}
  .mview button{flex:1}""",
"""  /* 리스트 | 그래프 스위치 — 로고 옆, 알약 두 칸. 켜진 쪽이 먹색 */
  .mswitch{display:inline-flex; align-items:center; flex:none; height:30px; padding:2px; margin-left:var(--s8); border-radius:999px; border:1px solid var(--topbar-btn-line); background:transparent; font:inherit}
  .mswitch span{display:inline-flex; align-items:center; height:24px; padding:0 var(--s8); border-radius:999px; font-size:var(--fs-label); font-weight:700; color:var(--topbar-fg); opacity:.6}
  .mswitch span.on{background:var(--text); color:#fff; opacity:1}
  body.notoday .mswitch span.on{background:#fff; color:var(--text)}""")
rep("""  /* 검정 모드: 안건표|그래프 토글이 검정 바탕에 묻히지 않게 */
  body.notoday .mview button{color:#fff; border-color:rgba(255,255,255,.45); background:transparent}
  body.notoday .mview button.on{background:#fff; color:var(--text); border-color:#fff}""", "")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_m2 ok")

# ---- 375px 에서 ⋮ 가 잘림: 상단 요소를 압축하고, 오늘이 아닐 때의 '오늘' 은 폰에서 더보기로(달력 아이콘에 점 표시) ----
s = io.open(P, encoding="utf-8").read()
rep("""          <!-- 폰: 아이콘만 한 줄. 날짜는 달력 아이콘으로(오늘이 아니면 상단바가 검정이라 티가 납니다), 등록은 오른쪽 아래 둥근 ＋ (7차-M) -->
          ${view.date===todayStr() ? "" : `<button class="tvbtn b-today" onclick="goToday()">오늘</button>`}
          <button class="tvbtn icon b-cal" onclick="openCal()" title="날짜" aria-label="날짜 선택">${ICON.cal}</button>""",
"""          <!-- 폰: 아이콘만 한 줄. 날짜는 달력 아이콘으로(오늘이 아니면 상단바가 검정이라 티가 납니다), 등록은 오른쪽 아래 둥근 ＋ (7차-M)
               '오늘' 은 375px 에 안 들어가 더보기로 — 달력 아이콘의 점이 '오늘이 아님' 표시 -->
          <button class="tvbtn icon b-cal ${view.date===todayStr()?'':'dot'}" onclick="openCal()" title="날짜" aria-label="날짜 선택">${ICON.cal}</button>""")
rep("""              <button onclick="closeMore(); openRate()">${ICON.chart}<span>예약률 추이</span></button>
              <button onclick="closeMore(); openHours()">${ICON.clock}<span>영업시간</span></button>""",
"""              ${isMobile() && view.date!==todayStr() ? `<button onclick="closeMore(); goToday()">${ICON.cal}<span>오늘로</span></button>` : ``}
              <button onclick="closeMore(); openRate()">${ICON.chart}<span>예약률 추이</span></button>
              <button onclick="closeMore(); openHours()">${ICON.clock}<span>영업시간</span></button>""")
rep("""  .topbar.mobile .topbar-in{flex-wrap:nowrap; padding:var(--s8) var(--s12); gap:var(--s4)}
  .topbar.mobile .storename{order:0; flex:none; justify-content:flex-start; text-align:left; height:36px; padding:0 var(--s4)}
  .topbar.mobile .bar-right{order:0; flex:1 1 auto; justify-content:flex-end; gap:var(--s4); flex-wrap:nowrap}
  .topbar.mobile .tvbtn.icon{width:38px; height:38px; padding:0; justify-content:center}
  .topbar.mobile .tvbtn.icon svg{width:19px; height:19px}
  .topbar.mobile .b-today{order:0; height:38px; padding:0 var(--s12)}""",
"""  .topbar.mobile .topbar-in{flex-wrap:nowrap; padding:var(--s8) var(--s12); gap:2px}
  .topbar.mobile .storename{order:0; flex:none; justify-content:flex-start; text-align:left; height:36px; padding:0 2px}
  .topbar.mobile .sn-brand{font-size:14px; letter-spacing:.12em}
  .topbar.mobile .bar-right{order:0; flex:1 1 auto; justify-content:flex-end; gap:3px; flex-wrap:nowrap; min-width:0}
  .topbar.mobile .tvbtn.icon{width:36px; height:36px; padding:0; justify-content:center; flex:none}
  .topbar.mobile .tvbtn.icon svg{width:18px; height:18px}
  .topbar.mobile .more-wrap{flex:none}
  /* 오늘이 아닐 때 달력 아이콘 오른쪽 위 점 */
  .topbar.mobile .b-cal{position:relative}
  .topbar.mobile .b-cal.dot::after{content:""; position:absolute; top:5px; right:5px; width:7px; height:7px; border-radius:50%; background:#fff}""")
rep("""  .mswitch{display:inline-flex; align-items:center; flex:none; height:30px; padding:2px; margin-left:var(--s8); border-radius:999px; border:1px solid var(--topbar-btn-line); background:transparent; font:inherit}
  .mswitch span{display:inline-flex; align-items:center; height:24px; padding:0 var(--s8); border-radius:999px; font-size:var(--fs-label); font-weight:700; color:var(--topbar-fg); opacity:.6}""",
"""  .mswitch{display:inline-flex; align-items:center; flex:none; height:28px; padding:2px; margin-left:var(--s4); border-radius:999px; border:1px solid var(--topbar-btn-line); background:transparent; font:inherit}
  .mswitch span{display:inline-flex; align-items:center; height:22px; padding:0 7px; border-radius:999px; font-size:var(--fs-label); font-weight:700; color:var(--topbar-fg); opacity:.6; letter-spacing:-.02em}""")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_m2 보강 ok")
