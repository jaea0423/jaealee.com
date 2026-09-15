/* ============================================================
   대시보드
   ============================================================ */
/* 오프라인이면 예약 목록·타임라인을 아예 감춥니다(재아 결정).
   캐시는 마지막으로 서버를 읽은 시점의 것이라, 그 사이 다른 기기에서 받은 예약이 없어 보입니다.
   비어 보이는 자리를 믿고 예약을 받으면 이중 예약이 나므로, '볼 수만 있음' 대신 '볼 수 없음' 으로 둡니다 */
function renderOfflineCard(){
  var d = OFFLINE.at ? new Date(OFFLINE.at) : null;
  var at = d && !isNaN(d) ? `${d.getMonth()+1}/${d.getDate()} ${pad(d.getHours())}:${pad(d.getMinutes())}` : "-";
  return `
    <section class="card offline-card">
      <div class="oc-t">서버에 연결되지 않아 예약을 보여 드리지 않습니다</div>
      <div class="oc-s">마지막으로 서버를 읽은 시각은 <b>${esc(at)}</b> 입니다. 그 뒤 다른 기기에서 받은 예약이 빠져 있어,
        빈자리로 보이는 곳이 실제로는 찼을 수 있습니다. 인터넷이 돌아오면 자동으로 다시 불러옵니다(30초마다 시도).</div>
      <div class="btn-row"><button class="btn primary" onclick="reconnect()">다시 연결</button></div>
    </section>`;
}
function renderDash(){
  const s = store(), st = s.settings, d = view.date;
  if(OFFLINE && AUTHED) return renderOfflineCard() + (view.calOpen ? renderCal() : "");
  const dayRes = s.reservations.filter(r=>r.date===d);
  const active = dayRes.filter(r=>r.status==="확정");
  const people = active.reduce((a,r)=>a+pplOf(r),0);
  const unassigned = active.filter(r=>isUnassigned(r) || (r.roomId && !seatById(r.roomId))).length;   /* 좌석이 삭제된 예약도(점검 C5) */
  const usedSeats = new Set(active.map(r=>effSeat(r)).filter(Boolean)).size;
  const stat = dayStat(d);

  /* 예약이 쓰는 좌석 수 — 룸 1개 = 1, 테이블 1개 = 1, 합치면 그만큼 */
  const seatUse = active.reduce((a,r)=>a + seatsOf(r).length, 0);
  const warnCnt = dayRes.filter(r=>holdsSeat(r) && resWarn(r).length).length;   /* 타임라인 위 '경고 N건' 과 같은 기준(확정+방문) */
  const checkCnt = checkItems(d).length;

  /* 순서: 타임라인(오늘 상황이 한눈에) → 지표줄 → 예약 목록. 지표는 눌러서 여는 목록의 입구 역할이라 목록 바로 위가 맞습니다 */
  const metrics = `
    <section class="card metrics-card">
      <div class="metrics">
        <!-- 셋째 줄(부연·'눌러서 열기')은 7차-M 에서 뺐습니다 — 두 줄이면 충분하고 카드가 낮아집니다 -->
        <div class="metric"><div class="v">${active.length}<span class="u">건</span></div>
          <div class="k">확정 예약</div></div>
        <div class="metric"><div class="v">${stat.rate}<span class="u">%</span></div>
          <div class="k">예약률</div></div>
        <button class="metric tapm ${unassigned?'warn':''}" onclick="openUnassigned()">
          <div class="v">${unassigned}<span class="u">건</span></div>
          <div class="k">룸 미배정</div></button>
        <button class="metric tapm ${warnCnt?'warn':''}" onclick="openPick('warn')">
          <div class="v">${warnCnt}<span class="u">건</span></div>
          <div class="k">경고 예약</div></button>
        <button class="metric tapm ${checkCnt?'amber':''}" onclick="openCheck()">
          <div class="v">${checkCnt}<span class="u">건</span></div>
          <div class="k">확인</div></button>
      </div>
    </section>`;

  if(isMobile()) return renderDashMobile(d, {active, unassigned, warnCnt, checkCnt, stat});
  return `
    <div class="card"><div class="card-b">${renderTimeline(d)}</div></div>
    ${foldCard("list", "예약 목록", `${dayRes.length}건`, renderResList(d))}
    ${view.calOpen ? renderCal() : ""}`;
}
/* ---------- 폰 대시보드 (7차-M) ----------
   폰에서 사장님이 보고 싶은 건 '지금부터 뭐가 오나' 라서 시간순 리스트가 기본이고, 그래프는 상단 스위치로.
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
  const graph = view.mView === "graph";   /* 리스트|그래프 스위치는 상단바(HANOK 옆)에 있습니다 */
  const toggle = "";
  const body = graph
    ? `<section class="card mgraph"><div class="card-b">${renderTimeline(d, true)}</div></section>`
    : `<section class="card"><div class="card-b">${renderAgenda(d)}</div></section>`;
  return `${kpi}${toggle}${body}
    <button class="fab" onclick="openWizard()" aria-label="예약 등록">${ICON.plus}</button>
    ${view.calOpen ? renderCal() : ""}`;
}
/* 리스트 — 두 줄 행. 1줄 시각·이름·상태, 2줄 인원·좌석·전화·꼬리표. 한 줄 전체가 탭 영역 */
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
  const seat = seatText(r);
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
function openZoomAdj(){ view.form={type:"zoomadj"}; render(); }
function sheetZoomAdj(){
  const adj = (DATA._ui && DATA._ui.zoomAdj) || 0, base = ZOOM_STEPS.indexOf(store().settings.uiZoom) >= 0 ? store().settings.uiZoom : 100;
  return `${sheetHead("화면 보정")}
    <p class="f-note" style="margin-top:-6px">이 기기에서만 크기를 조금 키우거나 줄입니다. 모든 기기 공통 크기는 설정 → 화면 크기.</p>
    <div class="zoomadj"><button class="btn" onclick="setZoomAdj(-5)">− 5</button><div class="za-v"><b>${uiZoom()}%</b><small>공통 ${base}% ${adj>=0?"+":""}${adj}</small></div><button class="btn" onclick="setZoomAdj(5)">＋ 5</button></div>
    <div class="btn-row" style="justify-content:center; margin-top:10px"><button class="btn sm ghost" onclick="setZoomAdj(-(${adj}))">보정 없음(0)</button></div>`;
}
function sheetHours(){
  const dh = hoursFor(view.date);
  const row = (k, v) => `<div class="hs-row"><span>${k}</span><b>${v}</b></div>`;
  return `
    ${sheetHead("영업시간")}
    <div class="hs-date">${dateLabel(view.date)}${dh.custom||dh.closed?` · ${esc(dh.note||"")}`:""}</div>
    ${dh.closed ? `<div class="hs-row"><b>휴무</b></div>` : row("영업시간", `${esc(dh.open)} ~ ${esc(dh.close)}`) + row("브레이크", dh.bs ? `${esc(dh.bs)} ~ ${esc(dh.be)}` : "없음") + row("라스트오더", dh.lo ? esc(dh.lo) : "—")}
`;
}

/* 접었다 펴는 카드 */
function foldCard(key, title, extra, inner){
  return `
    <section class="card fold ${view.open[key]?'on':''}">
      <button class="fold-h" onclick="toggleFold('${key}')">
        <span class="fh-t">${title}</span>
        <span class="fh-x">${extra||""}</span>
        <span class="fh-i">${view.open[key]?"▲":"▼"}</span>
      </button>
      ${view.open[key]?`<div class="fold-b ${view.foldJust===key?'just':''}">${inner}</div>`:""}
    </section>`;
}
/* 설정 섹션은 한 번에 하나만 펼칩니다.
   여러 개가 열려 있으면 어디를 보고 있었는지 잃습니다 — 다른 걸 누르면 이전 것은 접힙니다. */
function toggleFold(k){
  var was = !!view.open[k];
  if(k.indexOf("s_") === 0){
    Object.keys(view.open).forEach(function(x){ if(x.indexOf("s_") === 0) view.open[x] = false; });
  }
  view.open[k] = !was;
  view.foldJust = was ? null : k;   /* 이번 render 에만 열림 애니메이션 */
  render();
}

/* 미리보기 — 값과 눈금 없이 막대와 선만 */

/* ---------- 예약률 추이 ----------
   막대는 아래가 룸, 위가 홀입니다. 둘을 더한 높이가 그날 전체 예약률입니다.
   꺾은선은 전체 예약률의 흐름입니다. */
function rateChart(endDate, days){
  const list = [];
  for(let i=days-1;i>=0;i--){
    const d = shiftDate(endDate, -i);
    const st = dayStat(d);
    list.push({date:d, rate:st.rate, room:st.roomShare, hall:st.hallShare,
               roomRate:st.roomRate, hallRate:st.hallRate, count:st.count});
  }
  const W=720, H=250, L=36, R=10, T=14, B=34;
  const iw=W-L-R, ih=H-T-B, bw=iw/list.length;
  const y = v => T + ih - (v/100)*ih;
  const cx = i => L + i*bw + bw/2;

  const grid = [0,20,40,60,80,100].map(v=>`
    <line class="gl" x1="${L}" y1="${y(v)}" x2="${W-R}" y2="${y(v)}"/>
    <line class="gl tick" x1="${L-5}" y1="${y(v)}" x2="${L}" y2="${y(v)}"/>
    <text class="tx ax" x="${L-8}" y="${y(v)+3.5}" text-anchor="end">${v}%</text>`).join("");

  const bars = list.map((x,i)=>{
    const c = cx(i), w = Math.max(2, bw*0.56);
    const hr = (x.room/100)*ih, hh = (x.hall/100)*ih;
    return `
      <rect class="rb-room" x="${c-w/2}" y="${T+ih-hr}" width="${w}" height="${Math.max(0,hr)}" rx="1.5">
        <title>${x.date} 룸 ${Math.round(x.room)}%p (룸만 보면 ${x.roomRate}%)</title></rect>
      <rect class="rb-hall" x="${c-w/2}" y="${T+ih-hr-hh}" width="${w}" height="${Math.max(0,hh)}" rx="1.5">
        <title>${x.date} 테이블 ${Math.round(x.hall)}%p (테이블만 보면 ${x.hallRate}%)</title></rect>`;
  }).join("");

  const pts = list.map((x,i)=>`${cx(i)},${y(x.rate)}`).join(" ");
  const dots = list.map((x,i)=>`<circle class="line-total-d" cx="${cx(i)}" cy="${y(x.rate)}" r="2.4"/>`).join("");

  const labels = list.map((x,i)=>{
    const dt = new Date(x.date+"T00:00:00");
    const dow = ["일","월","화","수","목","금","토"][dt.getDay()];
    const on = x.date===view.date;
    return `<text class="tx ${on?'on':''}" x="${cx(i)}" y="${H-16}" text-anchor="middle">${dt.getDate()}</text>
            <text class="tx sm ${on?'on':''}" x="${cx(i)}" y="${H-4}" text-anchor="middle">${dow}</text>`;
  }).join("");

  const avg = Math.round(list.reduce((a,x)=>a+x.rate,0)/list.length);
  const peak = list.reduce((a,x)=>x.rate>a.rate?x:a, list[0]);
  const low  = list.reduce((a,x)=>x.rate<a.rate?x:a, list[0]);
  const st0 = dayStat(endDate);

  return `
    <div class="legend">
      <span><i class="sw rb-room"></i>룸 ${st0.roomSeats}개</span>
      <span><i class="sw rb-hall"></i>홀 ${st0.hallSeats}테이블</span>
      <span><i class="sw ln total"></i>전체 예약률</span>
    </div>
    <svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="예약률 추이">
      ${grid}${bars}
      <polyline class="line-total" points="${pts}"/>${dots}
      ${labels}
    </svg>
    <div class="chart-sum">
      <span>평균 <b>${avg}%</b></span>
      <span>최고 <b>${peak.rate}%</b> (${dateLabel(peak.date)})</span>
      <span>최저 <b>${low.rate}%</b> (${dateLabel(low.date)})</span>
      <span class="muted">노쇼·취소는 빠진 값입니다</span>
    </div>`;
}

/* ---------- 예약 목록 (한 줄) ---------- */
function renderResList(date){
  const s = store();
  let day = s.reservations.filter(r=>r.date===date).sort((a,b)=>a.time.localeCompare(b.time));
  /* 8차-W(재아): 전체 / 예정(아직 안 온 확정) / 지난·방문(1시간 지난 확정 + 방문) / 취소·노쇼 */
  const nowM0 = toMin(nowHM()), isToday0 = date === todayStr();
  const isPastRes = r => r.date < todayStr() || (isToday0 && toMin(r.time) + 60 < nowM0);
  /* '예정' 에는 아직 시각이 안 지난 '방문' 도 흐리게 넣습니다 — 잘못 누른 방문 처리를 눈치채게(8차-Z 재아) */
  const GROUPS = { "전체": r=>true, "예정": r=>(r.status==="확정" || r.status==="방문") && !isPastRes(r), "지난·방문": r=>r.status==="방문" || (r.status==="확정" && isPastRes(r)), "취소·노쇼": r=>r.status==="취소" || r.status==="노쇼" };
  if(!GROUPS[view.filter]) view.filter = "예정";
  /* 기본은 '예정'. 지난 날짜에서는 예정이 늘 비므로 그때만 '전체' 로 보여 줍니다(버튼도 전체가 켜짐) */
  const eff = (view.filter === "예정" && date < todayStr()) ? "전체" : view.filter;
  const filters = Object.keys(GROUPS).map(f=>{
    const n = s.reservations.filter(r=>r.date===date && GROUPS[f](r)).length;
    return `<button class="${eff===f?'on':''}" onclick="setFilter('${f}')">${f} ${n}</button>`;
  }).join("");
  if(eff!=="전체") day = day.filter(GROUPS[eff]);
  /* 8차-V(재아): 오늘 목록에는 '지금' 선을 넣어 위(지난)·아래(앞으로) 가 갈리게 */
  const nowM = toMin(nowHM()), isToday = date === todayStr();
  let marked = false;
  const rows = day.length ? day.map(r=>{
    let m = "";
    if(isToday && !marked && toMin(r.time) > nowM){ marked = true; m = `<div class="now-sep"><span>지금 ${hm(nowHM())}</span></div>`; }
    return m + resRow(r);
  }).join("") + (isToday && !marked ? `<div class="now-sep"><span>지금 ${hm(nowHM())} · 오늘 남은 예약 없음</span></div>` : "")
    : `<div class="empty">해당 조건의 예약이 없습니다.</div>`;
  return `<div class="filters">${filters}</div><div class="rlist">${rows}</div>`;
}
function resRow(r){
  const room = store().settings.rooms.find(x=>x.id===r.roomId);
  const seat = room ? resSeatLabel(r)
             : seatText(r);
  /* 시간이 지났는데 아직 처리하지 않은 예약 */
  const late = r.status==="확정" && r.date<=todayStr() &&
    (r.date<todayStr() || toMin(r.time)+60 < toMin(nowHM()));
  const pills = [
    r.assignedLater ? `<span class="pill" title="접수 때는 좌석 미정이었습니다">배정 완료</span>` : "",
    r.menuType==="코스" ? (r.courseUndecided
      ? `<span class="pill amber">코스 미정</span>`
      : `<span class="pill pine" title="${esc(courseSummary(r.courses))}">코스</span>`) :
    r.menuType==="코스 상당" ? `<span class="pill pine">코스상당</span>` :
    r.menuType==="확인 필요" ? `<span class="pill amber">메뉴확인</span>` : "",
    r.allergy ? `<span class="pill rust" title="${esc(r.allergy)}">알러지</span>` : "",
    r.chairs ? `<span class="pill pine">유아의자 ${r.chairs}</span>` : "",
    r.request ? `<span class="pill" title="${esc(r.request)}">요청</span>` : "",
    r.memo ? `<span class="pill blue" title="${esc(r.memo)}">메모</span>` : ""
  ].join("");
  /* 꼬리표 묶음 — 상태(취소/방문/노쇼)와 오늘 변동 표시까지 한 칸에. 비어 있으면 칸 자체를 안 그립니다(폰에서 빈 줄 방지) */
  const rest = pills
    + (r.status!=="확정"?`<span class="rr-st tag ${r.status==="노쇼"?"rust":""}">${r.status}</span>`:"")
    + (()=>{ const c=changeTag(r); return c?`<span class="chg-tag ${c.kind==="취소"||c.kind==="노쇼"?"off":""}">${esc(c.label)}</span>`:""; })();
  return `
    <button class="rrow s-${r.status} ${late?'late':''} ${resWarn(r).length?'k-warn':''} ${changeTag(r)?'k-chg':''} ${!r.roomId && !isTablePref(r.seatPref)?'k-tent':''}" onclick="openMark('${r.id}')">
      <span class="rr-bang">${late?"!":""}</span>
      <span class="rr-t">${esc(r.time)}</span>
      <span class="rr-n">${esc(r.name)}</span>
      <span class="rr-p">${pplOf(r)}명${r.infants?`(유아${r.infants})`:""}</span>
      <span class="rr-seat ${room||r.tentativeRoomId?'':'none'}">${esc(seat)}</span>
      <span class="rr-ph">${esc(r.phone||"-")}</span>
      ${rest?`<span class="rr-rest">${rest}</span>`:""}
    </button>`;
}
