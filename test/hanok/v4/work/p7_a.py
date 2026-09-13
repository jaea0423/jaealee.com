# -*- coding: utf-8 -*-
"""v4 6차 묶음 A — 색·글자 (지시서 1, 3, 4, 5, 11, 12)
   1  타임라인 '오늘 바뀐 것' 블록: 파란 바탕 + 흰 글자, 원래 상태색은 2px 테두리로. '잠정' 꼬리표 삭제
   3  흐림(dim) 기준을 isBlockPast() 하나로: 방문 처리 즉시 / 미처리는 시작+60분. 홀·룸·디스플레이 공용
   4  오늘이 아닌 날짜: 상단바·페이지 바탕 검정, 날짜 옆 '지난 날짜'/'D-n', '오늘' 버튼은 오늘이 아닐 때만
   5  영업시간 줄을 같은 폭 세 칸으로 (대시보드·마법사 공용 hoursLineHtml)
   11 HANOK 로고 산세리프
   12 디스플레이 목록형의 매장 이름 글자 삭제
   한 번에 여러 곳을 바꾸는 치환은 개수를 assert 합니다."""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ============================================================
# 1. .blk.changed — 파란 바탕
# ============================================================
rep(""".blk .tt{font-style:normal; background:rgba(255,255,255,.28); border-radius:var(--r-sm); padding:1px var(--s4); font-size:var(--fs-label)}
""", "")

rep("""/* 변동 예약(당일 변경) — 왼쪽 파란 띠만으로는 눈에 안 들어와 글씨까지 하늘색으로.
   어두운 블록 위라서 옅은 파랑은 회색으로 보입니다. 채도를 확실히 올립니다.
   띠에 글자가 물리지 않도록 왼쪽 여백도 띠 두께만큼 밉니다. */
.blk.changed{box-shadow:inset 4px 0 0 #4FA8F0; padding-left:var(--s12); color:#6EC2FF}
.blk.changed b{color:#9FD8FF}
.blk.changed .tt{background:rgba(110,194,255,.25)}
""",
"""/* 오늘 등록·변경·취소·노쇼가 일어난 예약(changeTag 가 있는 것) — 바탕을 통째로 파랑으로.
   6차 전의 '왼쪽 4px 띠 + 하늘색 글자'는 회색 잠정 블록 위에서 거의 안 보였습니다.
   원래 상태색(확정 먹색 / 잠정 회색 / 경고 벽돌)은 2px 테두리로 옮겨 상태를 잃지 않게 합니다.
   3px 는 블록 높이 19px 에서 글자 자리를 잡아먹어 2px 고정. 내일이 되면 changeTag 가 비어 저절로 풀립니다.
   '잠정' 꼬리표(.tt)는 블록 색으로 구분되므로 지웠습니다(툴팁의 ' · 잠정'은 남김).
   ※ button.blk.tent / .warned / .warned.past 가 (0,3,1) 까지 올라가 있어 여기도 button 을 붙여 같은 높이로 씁니다 */
button.blk.changed{background:var(--blue); color:#fff; border:2px solid var(--text); padding-left:var(--s4)}
button.blk.changed.tent{border:2px solid #8E8A80}
button.blk.changed.warned, button.blk.changed.tent.warned{border:2px solid var(--rust)}
.blk.changed b{color:#fff}
/* 지난 것은 다른 past 블록처럼 흐리게 — 색은 그대로 두고 투명도로만 (테두리 색도 같이 흐려져 '지난 것'이 한눈에) */
button.blk.changed.past, button.blk.changed.warned.past{background:var(--blue); opacity:.5}
""")

rep("""${blockLabel(it.r)}${tent?' <i class="tt">잠정</i>':''}</button>`;""",
    """${blockLabel(it.r)}</button>`;""", 2)

# ============================================================
# 3. 흐림 기준 — isBlockPast 하나로
# ============================================================
rep("""function nowHM(){ const d=new Date(); return pad(d.getHours())+":"+pad(d.getMinutes()); }
""",
"""function nowHM(){ const d=new Date(); return pad(d.getHours())+":"+pad(d.getMinutes()); }
/* 타임라인 블록(홀·룸)과 손님 화면 줄을 '흐리게' 할지 — 세 곳이 같은 규칙을 씁니다.
   · 방문 처리한 예약은 바로 흐리게(끝난 일).
   · 처리 안 한 예약은 시작 +60분이 지나면 흐리게.
   → 흐려졌는데 '방문'이 안 찍힌 블록 = 노쇼 확인이 필요한 건, 이라는 뜻이 됩니다.
   6차 전에는 종료 시각(시작+체류시간)이 지나야 흐려져서, 한창 식사 중인 손님과 안 온 손님이 같은 색이었습니다. */
function isBlockPast(r, s0, date, nowM){
  const t = todayStr();
  if(date < t) return true;
  if(date > t) return false;
  return r.status === "방문" || s0 + 60 < nowM;
}
""")

rep("""      const past = date<todayStr() || (date===todayStr() && it.e0 < nowM);
""", """      const past = isBlockPast(it.r, it.s0, date, nowM);
""", 2)

rep("""      /* 예약 시각에서 1시간이 지나면 흐리게. 자리를 접어야 할 때 이런 건이 먼저 밀립니다 */
      const past = (toMin(r.time) + 60 <= toMin(now)) || r.status==="방문";
""",
"""      /* 흐림 기준은 타임라인 블록과 같은 함수(isBlockPast). 자리를 접어야 할 때 이런 건이 먼저 밀립니다 */
      const past = isBlockPast(r, toMin(r.time), today, toMin(now));
""")

# ============================================================
# 4. 오늘이 아닐 때 — 검정 상단바 + 검정 바탕
# ============================================================
rep("""/* 오늘이 아닌 날짜를 보고 있으면 상단바 색이 바뀝니다.
   어제·내일을 보다가 그대로 예약을 받는 실수가 있어서, 눈에 확실히 띄어야 합니다.
   과거는 회갈색, 미래는 호박색 — 방향까지 색으로 구분합니다. */
.topbar.notoday{border-bottom-width:2px}
.topbar.notoday.past{--topbar-bg:#EEE9E0; --topbar-line:#B9AE9C}
.topbar.notoday.future{--topbar-bg:#FBF1DC; --topbar-line:#D9BF87}
.topbar.notoday .bdate{font-weight:800; color:#6A4E18}
.topbar.notoday.past .bdate{color:#5A4E40}
.topbar.notoday .btoday{background:var(--text); color:#fff; border-color:var(--text)}
""",
"""/* 오늘이 아닌 날짜를 보고 있으면 상단바와 페이지 바탕이 검정이 됩니다.
   어제·내일을 보다가 그대로 예약을 받는 실수가 있어서, 눈에 확실히 띄어야 합니다.
   6차 전에는 지난 날짜 회갈색 / 다음 날짜 노랑이었는데 차이가 약하고 노랑은 경고로 읽혀서,
   방향 구분은 색 대신 날짜 옆 작은 글자(.nt-tag — '지난 날짜' / 'D-3')로 옮겼습니다.
   body.notoday 는 renderApp 이 같은 조건(notodayView)으로 붙입니다 — 설정 탭·디스플레이·잠금에서는 안 붙음 */
.topbar.notoday{--topbar-bg:var(--text); --topbar-fg:#fff; --topbar-line:var(--text);
  --topbar-btn-line:rgba(255,255,255,.55); --topbar-hover:rgba(255,255,255,.12)}
.topbar.notoday .bdate{font-weight:800; color:#fff}
.topbar.notoday .nt-tag{font-size:var(--fs-label); font-weight:600; color:rgba(255,255,255,.7); margin-left:var(--s8); letter-spacing:0}
.topbar.notoday .rf-at{color:rgba(255,255,255,.7)}
/* 검정 바 위에서 검정 '예약 등록' 버튼은 사라지므로 흰 바탕·검정 글자로 뒤집습니다 */
.topbar.notoday .tvbtn.accent{background:#fff; color:var(--text)}
.topbar.notoday .tvbtn.accent:hover{background:#E5E5EA}
/* '오늘' 버튼 — 오늘로 돌아오는 유일한 한 번 탭 경로라 없애지 않습니다. 오늘이 아닐 때만 그리고 흰 테두리 */
.topbar.notoday .btoday{border-color:#fff; color:#fff; opacity:1}
/* 페이지 바탕도 검정. 카드·타임라인·목록은 흰 상자 그대로라 대비가 세지므로 그림자는 없앱니다.
   시트·마법사·달력·확인창은 var(--bg) 를 직접 깔고 있어 그대로 밝습니다 (뒤로 검정이 비치는 건 정상) */
body.notoday{background:var(--text)}
body.notoday .card{box-shadow:none}
""")

rep("""/* '오늘' 버튼 — 오늘이면 .hold 로 자리만 지킵니다 (날짜가 가운데에서 흔들리지 않게 왼쪽에 같은 폭의 빈 칸) */
""",
"""/* '오늘' 버튼 — 오늘이 아닐 때만 그립니다(6차). 날짜가 가운데에서 흔들리지 않게 그때만 왼쪽에 같은 폭의 빈 칸(::before)을 둡니다.
   오늘이면 버튼도 빈 칸도 없으니 양쪽이 비어 역시 가운데입니다 */
""")
rep(""".bar-mid::before{content:""; width:52px; flex:none; margin-right:var(--s8)}
@media (max-width:900px){ .bar-mid::before{display:none} }
""",
""".topbar.notoday .bar-mid::before{content:""; width:52px; flex:none; margin-right:var(--s8)}
@media (max-width:900px){ .topbar.notoday .bar-mid::before{display:none} }
""")

rep("""      <header class="topbar ${view.tab!=="settings" && view.date!==todayStr() ? (view.date<todayStr()?'notoday past':'notoday future') : ''}"><div class="topbar-in">""",
    """      <header class="topbar ${notodayView()?'notoday':''}"><div class="topbar-in">""")
rep("""          <button class="bdate" onclick="openCal()" title="달력 열기">${dateLabel(view.date)}</button>""",
    """          <button class="bdate" onclick="openCal()" title="달력 열기">${dateLabel(view.date)}${notodayTag()}</button>""")
rep("""          <button class="btoday ${view.date===todayStr()?'hold':''}" onclick="goToday()" ${view.date===todayStr()?'tabindex="-1"':''}>오늘</button>""",
    """          ${view.date===todayStr() ? '' : '<button class="btoday" onclick="goToday()">오늘</button>'}""")

rep("""function goToday(){ view.date = todayStr(); render(); }
""",
"""function goToday(){ view.date = todayStr(); render(); }
/* '오늘이 아닌 날짜를 보는 중' — 상단바(.topbar.notoday)와 body.notoday 가 같은 조건을 써야 하므로 한 곳에.
   설정 탭은 날짜 개념이 없어 제외. 디스플레이·잠금·인트로는 renderApp 이 renderStore 전에 갈라져 나가므로 여기서도 빼 둡니다 */
function notodayView(){
  return !!view.storeKey && AUTHED && !view.display && !INTRO && view.tab!=="settings" && view.date!==todayStr();
}
/* 날짜 옆 작은 글자 — 지난 날짜면 '지난 날짜', 다음 날짜면 며칠 뒤인지(D-3). 색으로 방향을 나누던 것을 글자로 */
function notodayTag(){
  if(view.date===todayStr()) return "";
  if(view.date<todayStr()) return ' <span class="nt-tag">지난 날짜</span>';
  const n = Math.round((new Date(view.date+"T00:00:00") - new Date(todayStr()+"T00:00:00"))/86400000);
  return ' <span class="nt-tag">D-'+n+'</span>';
}
""")

rep("""  saveScroll();
  applyTheme();
""",
"""  saveScroll();
  applyTheme();
  /* 오늘이 아닌 날짜면 페이지 바탕도 검정 (applyTheme 이 className 을 통째로 다시 쓰므로 그 뒤에) */
  document.body.classList.toggle("notoday", notodayView());
""")

# ============================================================
# 5. 영업시간 줄 — 같은 폭 세 칸
# ============================================================
rep("""function dateLabel(s){
  const d=new Date(s+"T00:00:00");
  return (d.getMonth()+1)+"월 "+d.getDate()+"일 ("+["일","월","화","수","목","금","토"][d.getDay()]+")";
}
""",
"""function dateLabel(s){
  const d=new Date(s+"T00:00:00");
  return (d.getMonth()+1)+"월 "+d.getDate()+"일 ("+["일","월","화","수","목","금","토"][d.getDay()]+")";
}
/* 영업시간 줄 — 대시보드(타임라인 위)와 마법사 날짜 화면이 같은 것을 씁니다.
   한 문장('영업시간 … · 브레이크 … · 라스트오더 …')은 요일마다 길이가 달라 눈이 매번 다른 자리를 찾아야 했습니다.
   같은 폭 세 칸으로 나누면 값이 항상 같은 자리에 옵니다. 없는 항목도 칸을 비우지 않고 '없음' / '—' 로 채웁니다 */
function hoursLineHtml(dh){
  if(dh.closed) return `<div class="hours-line closed"><span class="hl-c"><i>휴무</i>${dh.note?esc(dh.note):""}</span></div>`;
  return `<div class="hours-line">
    <span class="hl-c"><i>영업시간</i>${esc(dh.open)} ~ ${esc(dh.close)}</span>
    <span class="hl-c"><i>브레이크</i>${dh.bs?`${esc(dh.bs)} ~ ${esc(dh.be)}`:"없음"}</span>
    <span class="hl-c"><i>라스트오더</i>${dh.lo?esc(dh.lo):"—"}</span>
  </div>`;
}
""")

rep(""".tl-hours{font-size:var(--fs-sub); color:var(--text-2); font-weight:600}
.hours-line{font-size:var(--fs-sub); color:var(--text-2); background:var(--surface-2);
  border:none; border-radius:var(--r-md); padding:var(--s8) var(--s12); margin-bottom:var(--s12)}
""",
"""/* 영업시간 세 칸 (hoursLineHtml). 라벨은 옅게, 값은 본문색.
   칸 사이 세로선은 --border 가 surface-2 위에서 거의 안 보여 --border-strong 을 씁니다 */
.hours-line{font-size:var(--fs-sub); color:var(--text); background:var(--surface-2);
  border:none; border-radius:var(--r-md); padding:var(--s8) var(--s12); margin-bottom:var(--s12);
  display:grid; grid-template-columns:repeat(3,1fr)}
.hours-line .hl-c{min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; padding:0 var(--s12); font-weight:600}
.hours-line .hl-c:first-child{padding-left:0}
.hours-line .hl-c + .hl-c{border-left:1px solid var(--border-strong)}
.hours-line .hl-c i{font-style:normal; color:var(--text-3); font-weight:600; margin-right:var(--s8)}
.hours-line.closed{grid-template-columns:1fr}
.tl-top .hours-line{margin-bottom:0}   /* .tl-top 은 gap 으로 간격을 잡으므로 여기서는 아래 여백 없이 */
""")

rep("""      <span class="tl-hours">${dh.closed
        ? `휴무 · ${esc(dh.note||"")}`
        : `영업시간 ${esc(dh.open)} ~ ${esc(dh.close)}${dh.bs?` · 브레이크 ${esc(dh.bs)} ~ ${esc(dh.be)}`:""}${dh.lo?` · 라스트오더 ${esc(dh.lo)}`:""}`}</span>
""", """      ${hoursLineHtml(dh)}
""")

rep("""      <div class="hours-line">${dh.closed?"휴무":`영업 ${esc(dh.open)} ~ ${esc(dh.close)}${dh.bs?` · 브레이크 ${esc(dh.bs)} ~ ${esc(dh.be)}`:""}${dh.lo?` · 라스트오더 ${esc(dh.lo)}`:""}`}</div>
""", """      ${hoursLineHtml(dh)}
""")

# 폰: 세 칸이 좁아 값이 잘리므로 한 줄에 '|' 로 이어 씁니다 (767px 이하 블록의 .tl-hours 자리)
rep("""  .tl-hours{font-size:var(--fs-label)}
""",
"""  /* 영업시간 줄 — 폰에서는 세 칸이 좁아 값이 잘리므로 한 줄에 '|' 구분선으로 이어 씁니다 */
  .hours-line{display:flex}
  .hours-line .hl-c{flex:none; padding:0 var(--s8)}
  .hours-line .hl-c i{margin-right:var(--s4)}
""")

# ============================================================
# 11. HANOK 로고 — 산세리프
# ============================================================
rep("""/* 상단바 왼쪽 — 로고타입. 한글 매장명 대신 HANOK */
.sn-brand{font-family:var(--serif); font-weight:800; letter-spacing:.14em; font-size:15px}
""",
"""/* 상단바 왼쪽 — 로고타입. 한글 매장명 대신 HANOK. 명조는 상단바에서 무거워 보여 산세리프(Pretendard)로 (6차).
   상단바가 검정일 때(.topbar.notoday)는 --topbar-fg 를 물려받아 흰색 */
.sn-brand{font-family:var(--sans); font-weight:700; letter-spacing:.18em; font-size:15px}
""")

# ============================================================
# 12. 디스플레이 목록형 — 매장 이름 글자 삭제
# ============================================================
rep(""".tvl-mark{position:absolute; left:0; right:0; bottom:calc(var(--tvu)*5); text-align:center}
.tvl-mark span{font-family:var(--serif-tv); font-size:calc(var(--tvu)*4.2);
  letter-spacing:.22em; text-indent:.22em; color:rgba(246,238,221,.92);
  text-shadow:0 2px 18px rgba(0,0,0,.8)}
""", "")
rep("""        <div class="tvl-mark"><span>${esc(s.name)}</span></div>
""", "")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_a 적용 완료")
