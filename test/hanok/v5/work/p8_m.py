# -*- coding: utf-8 -*-
"""v5 7차-M — 모바일(640px 이하) UI 개편. PC 는 그대로(픽셀 비교로 확인).
   · 상단 한 줄: HANOK | [오늘] 📅 ↻ 🔍 ⋮ — 날짜 층 없음(날짜는 달력에서), 상단 ＋ 없음 → 오른쪽 아래 둥근 ＋(.fab)
   · 대시보드: 지표 한 줄 칩(.mkpi) → 안건표(기본, 두 줄 행 .mrow) | 그래프(압축: 홀은 쓰는 층만, 층 26px, 가로 스크롤 후 현재 시각 근처로)
     예약 목록 카드는 안건표에 합침, 영업시간 카드 숨김 → 더보기 '영업시간' 시트(PC 에도 항목 추가, PC 카드는 유지)
   · 검정 모드 그래프 깨짐 근본 수정: .tl-scroll 이 카드 밖으로 14px 삐져나가던 음수 margin 삭제, 이름 열의 -26px 그림자 트릭 삭제
   · 예시 데이터 넣기/지우기 버튼·함수 삭제(전부)"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ============================================================
# 0. 검정 모드 그래프 — 근본 수정
# ============================================================
rep(""".tl-scroll{overflow-x:auto; overflow-y:hidden; -webkit-overflow-scrolling:touch; margin:0 -14px; padding:0 var(--s16); position:relative}""",
    """/* 예전엔 margin:0 -14px 로 카드 여백까지 그래프를 끌어냈는데(-14 가 카드 여백 12~16px 과 안 맞아 카드 밖으로 2px 삐져나감),
   바탕이 검정이면 줄 사이 틈으로 검정이 비쳐 깨져 보였습니다. 카드 안에서만 스크롤합니다 (7차-M) */
.tl-scroll{overflow-x:auto; overflow-y:hidden; -webkit-overflow-scrolling:touch; margin:0; padding:0; position:relative}""")
rep("""   2) .tl-scroll 이 좌우로 14px 삐져나와 있어 이름 칸 왼쪽에 14px 틈이 남고 그리로 그래프가 보였습니다.
      → 모바일에서는 .tl-scroll 의 왼쪽 padding 을 없애고(11구역), 남는 틈은 box-shadow 로 왼쪽을 한 번 더 칠합니다.
        (가상요소 대신 box-shadow 를 쓰는 이유: 위치 계산 없이 요소 배경색 그대로 왼쪽으로 복사돼서 어긋날 일이 없습니다)
   box-shadow 세 겹 = 왼쪽 여백 칠하기 / 그래프와 나누는 세로선 / 스크롤됐음을 알리는 옅은 그림자 */""",
"""   2) (7차-M 에서 정리) .tl-scroll 이 카드 밖으로 삐져나가던 음수 margin 을 없애 이름 칸이 스크롤 상자 왼쪽 끝에 딱 붙습니다.
      왼쪽을 덧칠하던 -26px 그림자도 필요 없어졌습니다.
   box-shadow 두 겹 = 그래프와 나누는 세로선 / 스크롤됐음을 알리는 옅은 그림자 */""")
rep("""  box-shadow:-26px 0 0 var(--surface), 1px 0 0 var(--border), 8px 0 8px -6px rgba(23,22,20,.16);
}""",
"""  box-shadow:1px 0 0 var(--border), 8px 0 8px -6px rgba(23,22,20,.16);
}""")
rep(""".tl-row.axis .tl-name{font-size:var(--fs-label); color:var(--text-3); font-weight:600; background:var(--surface); box-shadow:-26px 0 0 var(--surface)}""",
    """.tl-row.axis .tl-name{font-size:var(--fs-label); color:var(--text-3); font-weight:600; background:var(--surface); box-shadow:none}""")
rep("""/* 모바일: 이름 열을 카드 왼쪽 끝에 붙입니다 (.tl-scroll 의 왼쪽 padding 을 없앰 — 5구역 .tl-name 주석 2) */
@media (max-width:899px){
  .tl-scroll{padding-left:0}
}
""", "")
rep("""@media (min-width:900px){
  .tl-scroll{margin:0; padding:0; overflow:visible}
  .tl{min-width:0}
}""",
"""@media (min-width:900px){
  .tl-scroll{overflow:visible}
  .tl{min-width:0}
}""")

# ============================================================
# 1. 모바일 판정 · 아이콘
# ============================================================
rep("""  more:'<svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="1.6" fill="currentColor" stroke="none"/>""",
    """  search:'<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/></svg>',
  clock:'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>',
  more:'<svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="1.6" fill="currentColor" stroke="none"/>""")
rep("""function renderStore(){
  const s = store();""",
"""/* 폰 여부 — CSS 의 @media (max-width:640px) 와 같은 기준. 폰에서는 상단바·대시보드를 다른 구성으로 그립니다(PC 는 그대로) */
function isMobile(){ return window.innerWidth <= 640; }
var MOBILE_WAS = null;
window.addEventListener("resize", function(){
  var m = isMobile();
  if(MOBILE_WAS !== null && m !== MOBILE_WAS && DATA) render();   /* 폰↔PC 경계를 넘을 때만 다시 그림 */
  MOBILE_WAS = m;
});
function renderStore(){
  const s = store();
  MOBILE_WAS = isMobile();""")

# ============================================================
# 2. 상단바 — 폰 한 줄
# ============================================================
rep("""      <header class="topbar ${notodayView()?'notoday':''}"><div class="topbar-in">""",
    """      <header class="topbar ${notodayView()?'notoday':''} ${isMobile()?'mobile':''}"><div class="topbar-in">""")
rep("""        ${view.tab==="settings" ? `` : `
        <div class="bar-mid">""",
"""        ${view.tab==="settings" || isMobile() ? `` : `
        <div class="bar-mid">""")
rep("""          <button class="tvbtn icon b-exit" onclick="setTab('dash')" title="설정 나가기" aria-label="설정 나가기">${ICON.exit}</button>` : `
          ${view.date===todayStr() ? "" : `<button class="tvbtn b-today" onclick="goToday()">오늘</button>`}
          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}</button>
          <button class="tvbtn b-search" onclick="openSearch()">예약 검색</button>
          <button class="tvbtn accent b-add" onclick="openWizard('${view.date}')">＋ 예약 등록</button>""",
"""          <button class="tvbtn icon b-exit" onclick="setTab('dash')" title="설정 나가기" aria-label="설정 나가기">${ICON.exit}</button>` : isMobile() ? `
          <!-- 폰: 아이콘만 한 줄. 날짜는 달력 아이콘으로(오늘이 아니면 상단바가 검정이라 티가 납니다), 등록은 오른쪽 아래 둥근 ＋ (7차-M) -->
          ${view.date===todayStr() ? "" : `<button class="tvbtn b-today" onclick="goToday()">오늘</button>`}
          <button class="tvbtn icon b-cal" onclick="openCal()" title="날짜" aria-label="날짜 선택">${ICON.cal}</button>
          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}</button>
          <button class="tvbtn icon b-search" onclick="openSearch()" title="예약 검색" aria-label="예약 검색">${ICON.search}</button>` : `
          ${view.date===todayStr() ? "" : `<button class="tvbtn b-today" onclick="goToday()">오늘</button>`}
          <button class="tvbtn icon b-refresh" onclick="manualRefresh()" title="새로고침" aria-label="새로고침">${ICON.refresh}</button>
          <button class="tvbtn b-search" onclick="openSearch()">예약 검색</button>
          <button class="tvbtn accent b-add" onclick="openWizard('${view.date}')">＋ 예약 등록</button>""")
# 더보기 묶음은 폰·PC 공통 — 닫는 백틱 구조를 맞춥니다: 위에서 PC 분기가 `...` 로 끝나고 more-wrap 이 따라오던 것을 두 분기 뒤 공통으로
rep("""          <button class="tvbtn accent b-add" onclick="openWizard('${view.date}')">＋ 예약 등록</button>
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
        </div>""",
"""          <button class="tvbtn accent b-add" onclick="openWizard('${view.date}')">＋ 예약 등록</button>`}
          ${view.tab==="settings" ? "" : `
          <!-- 더보기(⋮): 자주 안 쓰는 것들을 여기로 모았습니다 — 예약률 추이 · 영업시간 · 설정 · 디스플레이 모드 -->
          <div class="more-wrap">
            <button class="tvbtn icon b-more ${view.moreOpen?'on':''}" onclick="toggleMore()" title="더보기" aria-label="더보기">${ICON.more}</button>
            ${view.moreOpen ? `
            <div class="more-menu">
              <button onclick="closeMore(); openRate()">${ICON.chart}<span>예약률 추이</span></button>
              <button onclick="closeMore(); openHours()">${ICON.clock}<span>영업시간</span></button>
              <button onclick="closeMore(); setTab('settings')">${ICON.set}<span>설정</span></button>
              <button onclick="closeMore(); openDisplay()">${ICON.tv}<span>디스플레이 모드</span></button>
            </div>` : ""}
          </div>`}
        </div>""")

# ============================================================
# 3. 대시보드 — 폰 판
# ============================================================
rep("""  return `
    <div class="card"><div class="card-b">${renderTimeline(d)}</div></div>
    <section class="card hours-card">${hoursLineHtml(hoursFor(d))}</section>
    ${metrics}
    ${foldCard("list", "예약 목록", `${dayRes.length}건`, renderResList(d))}
    ${view.calOpen ? renderCal() : ""}`;
}""",
"""  if(isMobile()) return renderDashMobile(d, {active, unassigned, warnCnt, checkCnt, stat});
  return `
    <div class="card"><div class="card-b">${renderTimeline(d)}</div></div>
    <section class="card hours-card">${hoursLineHtml(hoursFor(d))}</section>
    ${metrics}
    ${foldCard("list", "예약 목록", `${dayRes.length}건`, renderResList(d))}
    ${view.calOpen ? renderCal() : ""}`;
}
/* ---------- 폰 대시보드 (7차-M) ----------
   폰에서 사장님이 보고 싶은 건 '지금부터 뭐가 오나' 라서 시간순 안건표가 기본이고, 그래프는 토글로.
   지표 다섯 칸과 그래프 위 지표줄은 내용이 겹쳐 한 줄 칩으로 합쳤습니다. 영업시간은 더보기 → 영업시간. */
function renderDashMobile(d, m){
  const chip = (n, label, cls, fn) => `<button class="mk ${n?cls:''} ${fn?'':'flat'}" ${fn?`onclick="${fn}"`:''}>${label} <b>${n}</b></button>`;
  const kpi = `<div class="mkpi">
    ${chip(m.active.length + "건", "확정", "", "")}
    ${chip(m.stat.rate + "%", "예약률", "", "")}
    ${chip(m.unassigned, "미배정", "warn", "openUnassigned()")}
    ${chip(m.warnCnt, "경고", "warn", "openPick('warn')")}
    ${chip(m.checkCnt, "확인", "amber", "openCheck()")}
  </div>`;
  const graph = view.mView === "graph";
  const toggle = `<div class="mview seg">
    <button class="${graph?'':'on'}" onclick="view.mView='list'; render()">안건표</button>
    <button class="${graph?'on':''}" onclick="view.mView='graph'; render()">그래프</button>
  </div>`;
  const body = graph
    ? `<section class="card mgraph"><div class="card-b">${renderTimeline(d, true)}</div></section>`
    : `<section class="card"><div class="card-b">${renderAgenda(d)}</div></section>`;
  return `${kpi}${toggle}${body}
    <button class="fab" onclick="openWizard('${d}')" aria-label="예약 등록">${ICON.plus}</button>
    ${view.calOpen ? renderCal() : ""}`;
}
/* 안건표 — 두 줄 행. 1줄 시각·이름·상태, 2줄 인원·좌석·전화·꼬리표. 한 줄 전체가 탭 영역 */
function renderAgenda(date){
  const s = store();
  let day = s.reservations.filter(r=>r.date===date).sort((a,b)=>a.time.localeCompare(b.time));
  const filters = ["전체",...STATUS].map(f=>{
    const n = f==="전체" ? day.length : day.filter(r=>r.status===f).length;
    return `<button class="${view.filter===f?'on':''}" onclick="setFilter('${f}')">${f} ${n}</button>`;
  }).join("");
  if(view.filter!=="전체") day = day.filter(r=>r.status===view.filter);
  const rows = day.length ? day.map(resRowMobile).join("") : `<div class="empty">해당 조건의 예약이 없습니다.</div>`;
  return `<div class="filters">${filters}</div><div class="mlist">${rows}</div>`;
}
function resRowMobile(r){
  const room = store().settings.rooms.find(x=>x.id===r.roomId);
  const seat = room ? seatLabel(r.roomId) : (r.tentativeRoomId ? `${seatLabel(r.tentativeRoomId)} 잠정` : "미배정");
  const late = r.status==="확정" && r.date<=todayStr() && (r.date<todayStr() || toMin(r.time)+60 < toMin(nowHM()));
  const warn = holdsSeat(r) && resWarn(r).length;
  const chg = changeTag(r);
  const pills = [
    r.menuType==="코스" ? (r.courseUndecided ? "코스 미정" : "코스") : r.menuType==="코스 상당" ? "코스상당" : r.menuType==="확인 필요" ? "메뉴확인" : "",
    r.allergy ? "알러지" : "", r.chairs ? `유아의자 ${r.chairs}` : "", r.request ? "요청" : "", r.memo ? "메모" : ""
  ].filter(Boolean).join(" · ");
  return `
    <button class="mrow s-${r.status} ${late?'late':''}" onclick="openMark('${r.id}')">
      <div class="mr-1">
        <span class="mr-t">${esc(r.time)}</span>
        <span class="mr-n">${esc(r.name)}</span>
        ${late?`<span class="mr-bang">!</span>`:""}
        ${r.status!=="확정"?`<span class="tag ${r.status==="노쇼"?"rust":""}">${r.status}</span>`:""}
        ${warn?`<span class="tag rust">경고</span>`:""}
        ${chg?`<span class="chg-tag ${chg.kind==="취소"||chg.kind==="노쇼"?"off":""}">${esc(chg.label)}</span>`:""}
      </div>
      <div class="mr-2">
        <span>${pplOf(r)}명${r.infants?`(유아${r.infants})`:""}</span>
        <span class="${room||r.tentativeRoomId?'':'none'}">${esc(seat)}</span>
        ${r.phone?`<span>${esc(r.phone)}</span>`:""}
        ${pills?`<span class="mr-p">${esc(pills)}</span>`:""}
      </div>
    </button>`;
}
/* 영업시간 시트 — 더보기에서. 폰은 카드가 없고 PC 는 카드가 있지만 항목은 양쪽에 둡니다 */
function openHours(){ view.form={type:"hours"}; render(); }
function sheetHours(){
  const dh = hoursFor(view.date);
  const row = (k, v) => `<div class="hs-row"><span>${k}</span><b>${v}</b></div>`;
  return `
    ${sheetHead("영업시간")}
    <div class="hs-date">${dateLabel(view.date)}${dh.custom||dh.closed?` · ${esc(dh.note||"")}`:""}</div>
    ${dh.closed ? `<div class="hs-row"><b>휴무</b></div>` : row("영업시간", `${esc(dh.open)} ~ ${esc(dh.close)}`) + row("브레이크", dh.bs ? `${esc(dh.bs)} ~ ${esc(dh.be)}` : "없음") + row("라스트오더", dh.lo ? esc(dh.lo) : "—")}
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}""")
rep("""noshow:sheetNoshow, pin:sheetPin, apw:sheetAdminPw, logs:sheetLogs,""",
    """noshow:sheetNoshow, pin:sheetPin, apw:sheetAdminPw, hours:sheetHours, logs:sheetLogs,""")

# 압축 그래프 — renderTimeline(date, compact)
rep("""function renderTimeline(date){""", """function renderTimeline(date, compact){""")
rep("""  const LANE = 21;   /* 층 하나의 높이(px) */""",
    """  const LANE = compact ? 26 : 21;   /* 층 하나의 높이(px). 폰 압축판은 손가락 크기로 조금 높게 */""")
rep("""    const placed = laneLayout(items, total);
    const blocks = placed.map(it=>{
      if(it.lane===null) return "";
      const w = ((it.e0-it.s0)/span)*100;""",
"""    const placed = laneLayout(items, total);
    /* 폰 압축판: 홀은 실제로 쓰는 층 + 1 만 그립니다 — 11층 빈 격자가 화면 절반을 먹었습니다 */
    const shown = compact ? Math.min(total, Math.max(2, placed.reduce((a,x)=>x.lane===null?a:Math.max(a, x.lane+x.need), 0) + 1)) : total;
    const blocks = placed.map(it=>{
      if(it.lane===null) return "";
      const w = ((it.e0-it.s0)/span)*100;""")
rep("""    return `<div class="tl-row hall ${blockedAllDay(hall,date)?'off-seat':''}" style="--lanes:${total}">
      <div class="tl-name"><b>${esc(hall.name)}</b><small>${total}테이블</small>${blockTag(hall)}</div>
      <div class="tl-track" style="height:${total*LANE}px">
        ${layers}
        ${Array.from({length:total},(_,i)=>`<span class="lane" style="bottom:${i*LANE}px; height:${LANE}px"></span>`).join("")}
        ${blockBands(hall)}${blocks}${nowLine}
      </div>
      <div class="tl-rate" style="height:${total*LANE}px">${total>1""",
"""    return `<div class="tl-row hall ${blockedAllDay(hall,date)?'off-seat':''}" style="--lanes:${shown}">
      <div class="tl-name"><b>${esc(hall.name)}</b><small>${total}테이블</small>${blockTag(hall)}</div>
      <div class="tl-track" style="height:${shown*LANE}px">
        ${layers}
        ${Array.from({length:shown},(_,i)=>`<span class="lane" style="bottom:${i*LANE}px; height:${LANE}px"></span>`).join("")}
        ${blockBands(hall)}${blocks}${nowLine}
      </div>
      <div class="tl-rate" style="height:${shown*LANE}px">${total>1""")
rep("""    <div class="tl-scroll" id="tl-scroll">
      <div class="tl">""",
"""    <div class="tl-scroll ${compact?'compact':''}" id="tl-scroll">
      <div class="tl">""")

# 폰 그래프: 그린 뒤 현재 시각 근처로 스크롤 (afterRender)
rep("""function afterRender(){""",
"""/* 폰 압축 그래프는 11시간을 가로로 늘려 스크롤합니다 — 그린 직후 현재 시각 1시간 전이 왼쪽에 오게 */
function scrollTlToNow(){
  var sc = document.querySelector(".tl-scroll.compact"); if(!sc) return;
  var track = sc.querySelector(".tl-track"); if(!track) return;
  var line = sc.querySelector(".nowline"); if(!line || /edge/.test(line.className)) return;
  var x = line.offsetLeft - track.clientWidth / 11;   /* 한 시간 폭만큼 앞에 */
  sc.scrollLeft = Math.max(0, track.offsetLeft + x - 88);
}
function afterRender(){
  scrollTlToNow();""")

# ============================================================
# 4. 예시 데이터 버튼·함수 삭제
# ============================================================
rep("""      <button class="btn" onclick="openLogs()">접속 기록</button>
      ${(!supaOn() || SUPA_CFG.demo) ? `<button class="btn danger" onclick="clearDemo()">예시 데이터 지우기</button>
      <button class="btn" onclick="addDemo()">예시 데이터 넣기</button>` : ""}
    </div>
    <p class="f-note">
      <b>접속 기록</b> — 누가 언제 무엇을 고쳤는지가 남습니다.
      예약이 왜 바뀌었는지 되짚을 때 보세요. 최근 ${LOG_MAX}건까지 보관합니다.<br>
      <b>예시 데이터</b> — 처음 실행 시 화면 확인용 예시 예약이 들어 있습니다.
      실제로 쓰기 전에 지우세요.</p>`;""",
"""      <button class="btn" onclick="openLogs()">접속 기록</button>
    </div>
    <p class="f-note">
      <b>접속 기록</b> — 누가 언제 무엇을 고쳤는지가 남습니다.
      예약이 왜 바뀌었는지 되짚을 때 보세요. 최근 ${LOG_MAX}건까지 보관합니다.</p>`;""")
a = s.index("/* 예시 데이터는 이제 사람이 눌러야만 들어갑니다 (자동 주입 없음) */")
b = s.index("\n\nloadData();")
s = s[:a] + "/* 예시 데이터 버튼(넣기·지우기)은 7차-M 에서 뺐습니다 — dev DB 는 work/seed_dev.py 로만 넣습니다 */" + s[b:]

# ============================================================
# 5. CSS — 폰 전용 (11구역 끝, 640px 이하)
# ============================================================
rep("""/* ============================================================
   12. 구형 브라우저 폴백 — 반드시 @supports 안에 둡니다""",
"""/* ---- 폰(640px 이하) 개편 (7차-M). PC 는 위 규칙 그대로 ---- */
/* 영업시간 시트 */
.hs-date{font-size:var(--fs-sub); color:var(--text-3); font-weight:600; margin:0 0 var(--s12)}
.hs-row{display:flex; justify-content:space-between; align-items:center; padding:var(--s12) 0; border-top:1px solid var(--border); font-size:var(--fs-body)}
.hs-row span{color:var(--text-2)} .hs-row b{font-weight:700}
@media (max-width:640px){
  /* 상단 한 줄 — 900px 규칙(3줄로 접기)을 되돌립니다 */
  .topbar.mobile .topbar-in{flex-wrap:nowrap; padding:var(--s8) var(--s12); gap:var(--s4)}
  .topbar.mobile .storename{order:0; flex:none; justify-content:flex-start; text-align:left; height:36px; padding:0 var(--s4)}
  .topbar.mobile .bar-right{order:0; flex:1 1 auto; justify-content:flex-end; gap:var(--s4); flex-wrap:nowrap}
  .topbar.mobile .tvbtn.icon{width:38px; height:38px; padding:0; justify-content:center}
  .topbar.mobile .tvbtn.icon svg{width:19px; height:19px}
  .topbar.mobile .b-today{order:0; height:38px; padding:0 var(--s12)}
  /* 지표 한 줄 칩 — 0 이 아닌 것만 색 */
  .mkpi{display:flex; gap:var(--s8); overflow-x:auto; -webkit-overflow-scrolling:touch; padding:0 0 var(--s4); margin-bottom:var(--s8)}
  .mk{flex:none; display:inline-flex; align-items:center; gap:var(--s4); height:34px; padding:0 var(--s12); border-radius:999px; border:1px solid var(--border-strong); background:var(--surface); color:var(--text-2); font:inherit; font-size:var(--fs-sub); font-weight:600; white-space:nowrap}
  .mk b{color:var(--text); font-weight:700}
  .mk.flat{pointer-events:none}
  .mk.warn{border-color:var(--rust); background:var(--rust-soft); color:var(--rust)} .mk.warn b{color:var(--rust)}
  .mk.amber{border-color:var(--amber); background:var(--amber-soft); color:var(--amber)} .mk.amber b{color:var(--amber)}
  body.notoday .mk{border-color:rgba(255,255,255,.35)}
  /* 안건표 | 그래프 토글 */
  .mview{margin-bottom:var(--s12)}
  .mview button{flex:1}
  /* 안건표 행 — 두 줄, 큼직하게 */
  .mlist{display:flex; flex-direction:column}
  .mrow{display:block; width:100%; text-align:left; background:none; border:none; border-top:1px solid var(--border); padding:var(--s12) var(--s4); font:inherit; color:inherit}
  .mrow:first-child{border-top:none}
  .mrow:active{background:var(--surface-2)}
  .mrow.s-취소, .mrow.s-방문{opacity:.45} .mrow.s-노쇼{opacity:.6}
  .mrow.late{background:var(--amber-soft)}
  .mr-1{display:flex; align-items:center; gap:var(--s8); min-width:0; flex-wrap:wrap}
  .mr-t{font-size:var(--fs-body); font-weight:700; color:var(--text); flex:none}
  .mr-n{font-size:var(--fs-title); font-weight:700; color:var(--text); min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:60%}
  .mr-bang{color:var(--rust); font-weight:800}
  .mr-2{display:flex; gap:var(--s8); flex-wrap:wrap; margin-top:var(--s4); font-size:var(--fs-sub); color:var(--text-2); font-weight:500}
  .mr-2 .none{color:var(--rust)}
  .mr-2 .mr-p{color:var(--text-3)}
  /* 압축 그래프 — 11시간을 카드보다 넓게 펴서 스크롤 (블록에 이름이 들어가게) */
  .tl-scroll.compact .tl{min-width:960px}
  .mgraph .tl-kpis{display:none}   /* 위 칩 줄과 겹치는 지표줄은 숨기고 범례는 남김 */
  /* 오른쪽 아래 둥근 등록 버튼 — 엄지 자리. 토스트(bottom 28px) 위로 */
  .fab{position:fixed; right:18px; bottom:22px; width:58px; height:58px; border-radius:50%; border:none; background:var(--text); color:#fff; font-size:30px; line-height:1; display:flex; align-items:center; justify-content:center; z-index:45; box-shadow:0 8px 24px rgba(0,0,0,.28); padding:0 0 3px}
  .fab svg{width:28px; height:28px; stroke:currentColor; fill:none; stroke-width:2.2}
  .fab:active{filter:brightness(1.2)}
  body.notoday .fab{background:#fff; color:var(--text)}
  /* 검정 모드: 안건표|그래프 토글이 검정 바탕에 묻히지 않게 */
  body.notoday .mview button{color:#fff; border-color:rgba(255,255,255,.45); background:transparent}
  body.notoday .mview button.on{background:#fff; color:var(--text); border-color:#fff}
  .toast{bottom:92px}
}

/* ============================================================
   12. 구형 브라우저 폴백 — 반드시 @supports 안에 둡니다""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_m 적용 완료")
