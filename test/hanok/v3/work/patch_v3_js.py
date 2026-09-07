"""v3 1차 — 자바스크립트(동작) 패치. src/index.html 을 직접 고칩니다.
   각 치환은 정확히 한 번만 맞아야 하며, 아니면 멈춥니다 (엉뚱한 곳을 고치지 않게)."""
import os, sys, io
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "index.html")
s = io.open(SRC, encoding="utf-8").read()
n_ok = 0
def rep(old, new, count=1):
    global s, n_ok
    c = s.count(old)
    if c != count:
        print("!! 치환 실패 (%d번 발견, %d번 기대):\n%s" % (c, count, old[:160])); sys.exit(1)
    s = s.replace(old, new); n_ok += 1

# ---------- 0단계 경로: 전화·네이버는 누르면 바로 다음 단계, 기타만 입력창 ----------
rep('''function wzSource(v){
  const el = document.getElementById("wz-src-detail");
  if(el) WZ.sourceDetail = el.value;
  WZ.source = v; render();
}''',
'''function wzSource(v){
  const el = document.getElementById("wz-src-detail");
  if(el) WZ.sourceDetail = el.value;
  WZ.source = v;
  /* 전화·네이버는 더 물을 것이 없으니 '다음'을 누르게 하지 않고 바로 넘어갑니다 (이전으로 돌아올 수 있습니다).
     기타는 경로를 적어야 하므로 이 화면에 머뭅니다 */
  if(v !== "기타"){ wzGo(1); return; }
  render();
}''')
# 기타 입력창 자리는 항상 잡아 둡니다 — 기타를 누를 때 타일들이 위로 튀지 않게
rep('''    ${WZ.source==="기타"?`
      <label class="f big" style="margin-top:18px"><div class="lb">어떤 경로인가요?</div>
        <input id="wz-src-detail" value="${esc(WZ.sourceDetail)}" placeholder="예: 지인 소개, 대면 예약" autofocus>
        <div class="f-note">예약 내역에만 참고용으로 표시됩니다.</div>
      </label>`:""}`;''',
'''    <label class="f big src-detail ${WZ.source==="기타"?"":"ghost"}"><div class="lb">어떤 경로인가요?</div>
        <input id="wz-src-detail" value="${esc(WZ.sourceDetail)}" placeholder="예: 지인 소개, 대면 예약" ${WZ.source==="기타"?"autofocus":"tabindex=\\"-1\\""}>
        <div class="f-note">예약 내역에만 참고용으로 표시됩니다.</div>
      </label>`;''')

# ---------- '다음 (확인 필요)' → '다음' (버튼이 빨개지고 경고문이 뜨므로 충분) ----------
rep('''        ${last?"예약 등록하기":(warn?"다음 (확인 필요)":"다음")}''',
    '''        ${last?"예약 등록하기":"다음"}''')
# 경고 자리는 항상 두 줄만큼 잡아 둡니다 — 경고가 생길 때 본문이 아래로 밀리지 않게
rep('''        <div class="wz-warn" id="wz-warn" style="display:${warn?"":"none"}">${
        String(warn||"").split("\\n").map(l=>`<div>${esc(l)}</div>`).join("")}</div></div>''',
'''        <div class="wz-warn" id="wz-warn">${
        String(warn||"").split("\\n").map(l=>`<div>${esc(l)}</div>`).join("")}</div></div>''')
rep('''  const bar = document.getElementById("wz-warn");
  if(bar){ bar.textContent = warn; bar.style.display = warn ? "" : "none"; }''',
'''  const bar = document.getElementById("wz-warn");
  if(bar){ bar.innerHTML = String(warn||"").split("\\n").map(l=>`<div>${esc(l)}</div>`).join(""); }''')

# ---------- 경고 문구 (짧게 + 남은 시간) ----------
rep('''  if(t > lo) out.push(`라스트오더(${loTxt}) 이후 시각입니다`);
  else {
    /* 임박 기준 분은 설정에서 바꿉니다 (설정 → 운영 판단 기준) */
    const soon = stx.loSoon != null ? stx.loSoon : 120;
    if(lo - t <= soon) out.push(`라스트오더(${loTxt}) 임박 — ${lo - t}분 전 입장입니다`);
  }
  if(dh.bs && t < toMin(dh.bs)){
    if((stx.breakMode||"leave")==="leave"){
      if(end > toMin(dh.bs)) out.push("식사 중 브레이크타임이 시작됩니다");
    }else{
      const buf = stx.breakEntryBuffer != null ? stx.breakEntryBuffer : 60;
      if(t > toMin(dh.bs) - buf) out.push(`브레이크 ${buf}분 전 이후 입장입니다`);
    }
  }
  if(end > toMin(dh.close)) out.push(`식사 시간이 마감(${hm(dh.close)}) 이후까지 이어집니다`);
  return out;
}''',
'''  /* 문구는 짧게, 대신 '남은 시간'을 함께 — 직원이 손님께 "주문 가능 시간이 40분입니다" 라고 바로 말할 수 있게.
     정확한 시각(라스트오더 몇 시)은 위 hours-line 에 이미 있으므로 여기서는 되풀이하지 않습니다 */
  if(t > lo) out.push("라스트오더 이후입니다.");
  else {
    /* 임박 기준 분은 설정에서 바꿉니다 (설정 → 운영 판단 기준) */
    const soon = stx.loSoon != null ? stx.loSoon : 120;
    if(lo - t <= soon) out.push(`라스트오더 임박 - 주문시간 ${hmDur(lo - t)}`);
  }
  if(dh.bs && t < toMin(dh.bs)){
    if((stx.breakMode||"leave")==="leave"){
      if(end > toMin(dh.bs)) out.push(`식사 중 브레이크가 시작됩니다 - 식사시간 ${hmDur(toMin(dh.bs) - t)}`);
    }else{
      const buf = stx.breakEntryBuffer != null ? stx.breakEntryBuffer : 60;
      if(t > toMin(dh.bs) - buf) out.push(`브레이크 ${buf}분 전 이후 입장입니다`);
    }
  }
  if(end > toMin(dh.close)) out.push(`마감 임박 - 식사시간 ${hmDur(toMin(dh.close) - t)}`);
  return out;
}
/* 분 → "1시간 05분" 꼴. 한 시간이 안 돼도 "0시간 40분" 으로 자리를 맞춥니다 (문구 길이가 흔들리지 않게) */
function hmDur(m){
  m = Math.max(0, m);
  return `${Math.floor(m/60)}시간 ${pad(m%60)}분`;
}''')
rep('''  if(inBreak(date, time)) return [`브레이크타임(${hm(dh.bs)} ~ ${hm(dh.be)})입니다`];''',
    '''  if(inBreak(date, time)) return ["브레이크입니다"];''')
# 확인 팝업 대상: '라스트오더 임박'만 빼고 전부 (마감 임박은 예전 '마감 넘김'과 같은 뜻이므로 팝업이 뜹니다)
rep('''  return timeWarns(date, time).filter(function(x){ return x.indexOf("임박") < 0; }).join("\\n");''',
    '''  return timeWarns(date, time).filter(function(x){ return x.indexOf("라스트오더 임박") < 0; }).join("\\n");''')
rep('''  if(msg.indexOf("브레이크타임(") >= 0) return "브레이크";
  if(msg.indexOf("이후 시각") >= 0) return "라스트오더 지남";
  if(msg.indexOf("마감") >= 0) return "마감 넘김";
  if(msg.indexOf("라스트오더") >= 0) return "라스트오더 임박";
  if(msg.indexOf("브레이크") >= 0) return "브레이크 임박";''',
'''  if(msg.indexOf("브레이크입니다") >= 0) return "브레이크";
  if(msg.indexOf("라스트오더 이후") >= 0) return "라스트오더 지남";
  if(msg.indexOf("마감") >= 0) return "마감 넘김";
  if(msg.indexOf("라스트오더") >= 0) return "라스트오더 임박";
  if(msg.indexOf("브레이크") >= 0) return "브레이크 임박";''')

# ---------- 1단계: 경고 시각은 오전/오후·시 글자까지 벽돌색, 분 조절은 항상 표시 ----------
rep('''    return `<button class="hcell ${curH===h?'on':''} ${bad?'late warned':''} ${gone?'gone':''}" onclick="wzPickHour(${h})">
      <span class="ap">${h<12?"오전":"오후"}</span>
      <span class="hh">${h%12===0?12:h%12}시</span>''',
'''    /* 경고가 걸리는 시각은 작은 표시만이 아니라 시각 글자까지 벽돌색 — 눈이 먼저 가야 하는 칸입니다 */
    const red = (bad || brk) ? " rust" : "";
    return `<button class="hcell ${curH===h?'on':''} ${bad?'late warned':''} ${gone?'gone':''}" onclick="wzPickHour(${h})">
      <span class="ap${red}">${h<12?"오전":"오후"}</span>
      <span class="hh${red}">${h%12===0?12:h%12}시</span>''')
rep('''  const minuteRail = curH===null ? "" : `
    <div class="mwrap">
      <div class="mhead"><span class="lbl">분 단위 조절</span><span class="mnow">${hm(WZ.time)}</span></div>''',
'''  /* 분 조절은 시각을 고르기 전에도 자리를 지킵니다(.idle) — 시각을 누르는 순간 레일이 생기며 화면이 내려앉지 않게 */
  const minuteRail = `
    <div class="mwrap ${curH===null?'idle':''}">
      <div class="mhead"><span class="lbl">분 단위 조절</span><span class="mnow">${curH===null?"시각을 먼저 선택하세요":hm(WZ.time)}</span></div>''')

# ---------- 2단계: 직접 입력 스테퍼 자리 항상 확보 ----------
rep('''    ${WZ.customPeople?`
      <div class="bigstep">
        <button onclick="wzAdj('people',-1)">−</button>
        <div class="v"><span>${WZ.people||7}</span><small>명</small></div>
        <button onclick="wzAdj('people',1)">＋</button>
      </div>`:""}''',
'''      <div class="bigstep ${WZ.customPeople?'':'ghost'}">
        <button onclick="wzAdj('people',-1)" ${WZ.customPeople?'':'tabindex="-1"'}>−</button>
        <div class="v"><span>${WZ.people||7}</span><small>명</small></div>
        <button onclick="wzAdj('people',1)" ${WZ.customPeople?'':'tabindex="-1"'}>＋</button>
      </div>''')

# ---------- 3단계: 미정 좌석 이름 짧게, '상관없음' 삭제 ----------
rep('''      <button class="scell any ${WZ.seat==='hall-any'?'on':''}" onclick="wzSeat('hall-any')"><span class="sn">홀 중 상관없음</span></button>
      <button class="scell any ${WZ.seat==='room-any'?'on':''}" onclick="wzSeat('room-any')"><span class="sn">룸 중 상관없음</span></button>
      <button class="scell any ${WZ.seat==='any'?'on':''}" onclick="wzSeat('any')"><span class="sn">상관없음</span></button>''',
'''      <button class="scell any ${WZ.seat==='hall-any'?'on':''}" onclick="wzSeat('hall-any')"><span class="sn">홀</span></button>
      <button class="scell any ${WZ.seat==='room-any'?'on':''}" onclick="wzSeat('room-any')"><span class="sn">룸</span></button>''')

# ---------- 4단계: 코스 요약 줄 자리 항상 확보, 위쪽 중복 경고(menu-warn) 제거 ----------
rep('''  return `
    ${roomWarn?`<div class="menu-warn">${esc(roomWarn)}</div>`:""}
    <div class="srcgrid menu4 ${opts.length===2?'menu2':''}">''',
'''  /* 룸 경고 문구는 위 질문 아래 경고 자리(wz-warn)에 이미 뜨므로 여기서는 타일 색만 바꿉니다 */
  return `
    <div class="srcgrid menu4 ${opts.length===2?'menu2':''}">''')
rep('''    ${WZ.menuType==="코스"?`
      <div class="course-sum">
        ${WZ.courseUndecided ? "코스 미정 — 방문 전 확정" : (n?`선택: ${esc(courseSummary(WZ.courses))}`:"코스 구성을 선택하세요")}
        <button class="btn sm" style="margin-left:auto" onclick="openCourse()">${n||WZ.courseUndecided?"수정":"선택"}</button>
      </div>`:""}
    ${WZ.courseOpen?renderCourse():""}`;''',
'''      <div class="course-sum ${WZ.menuType==="코스"?'':'ghost'}">
        ${WZ.courseUndecided ? "코스 미정 — 방문 전 확정" : (n?`선택: ${esc(courseSummary(WZ.courses))}`:"코스 구성을 선택하세요")}
        <button class="btn sm" style="margin-left:auto" onclick="openCourse()" ${WZ.menuType==="코스"?'':'tabindex="-1"'}>${n||WZ.courseUndecided?"수정":"선택"}</button>
      </div>
    ${WZ.courseOpen?renderCourse():""}`;''')
# 코스 경고: 판매하지 않는 시간대의 코스, 두 종류 이상 섞임 (막지 않고 알립니다)
rep('''      if(WZ.menuType==="코스" && !WZ.courseUndecided && n>adults)
        out.push(`코스 ${n}인분이 성인 ${adults}명보다 많습니다`);
    }
  }''',
'''      if(WZ.menuType==="코스" && !WZ.courseUndecided && n>adults)
        out.push(`코스 ${n}인분이 성인 ${adults}명보다 많습니다`);
    }
    out.push.apply(out, courseWarns());
  }''')
rep('''function renderCourse(){
  const gs = courseGroups();
  const stx = store().settings;
  const W = cTgt();
  const lunch = W.time && toMin(W.time) < toMin(stx.lunchUntil||"16:00");
  const dow = W.date ? new Date(W.date+"T00:00:00").getDay() : 0;
  /* 공휴일을 주말로 볼지는 설정에서 정합니다 */
  const weekend = dow===0 || dow===6 || (stx.holidayAsWeekend!==false && isHoliday(W.date));
  const fits = (g)=>{
    const w = g.when||[];
    if(!w.length || w.includes("종일")) return true;
    const key = (weekend?"주말":"평일") + (lunch?"점심":"저녁");
    return w.includes(key);
  };''',
'''/* 이 예약의 날짜·시각에 그 코스 그룹을 파는지 */
function courseGroupFits(g){
  const stx = store().settings, W = cTgt();
  const lunch = W.time && toMin(W.time) < toMin(stx.lunchUntil||"16:00");
  const dow = W.date ? new Date(W.date+"T00:00:00").getDay() : 0;
  /* 공휴일을 주말로 볼지는 설정에서 정합니다 */
  const weekend = dow===0 || dow===6 || (stx.holidayAsWeekend!==false && isHoliday(W.date));
  const w = g.when||[];
  if(!w.length || w.includes("종일")) return true;
  const key = (weekend?"주말":"평일") + (lunch?"점심":"저녁");
  return w.includes(key);
}
/* 코스 구성에서 걸리는 것 — 코스 팝업 안과 '다음' 버튼 위 경고 자리 두 곳에 같이 씁니다.
   1) 그 시간대에 팔지 않는 코스가 들어감 (예: 저녁에 평일 점심 코스)
   2) 코스가 두 종류 이상 섞임 — 한 테이블은 코스를 통일하는 것이 가게 규칙입니다
   둘 다 막지 않습니다. 사장님이 예외를 둘 수 있으므로 빨갛게 알리기만 합니다 */
function courseWarns(){
  const W = cTgt(); if(!W || W.menuType!=="코스" || W.courseUndecided) return [];
  const gs = courseGroups(), out = [];
  const picked = Object.entries(W.courses||{}).filter(([k,v])=>v>0);
  const offNames = picked.filter(([k])=>{ const g = gs[+k.split("|")[0]]; return g && !courseGroupFits(g); })
    .map(([k])=>k.split("|")[1]);
  if(offNames.length) out.push(`이 시간에 팔지 않는 코스입니다 — ${offNames.join(", ")}`);
  if(picked.length >= 2) out.push(`코스가 ${picked.length}종류입니다 — 한 테이블은 코스를 통일합니다`);
  return out;
}
function renderCourse(){
  const gs = courseGroups();
  const W = cTgt();
  const fits = courseGroupFits;''')
rep('''            ${short?`<div class="ct-warn">성인 ${ad}명보다 ${ad-n}명 적습니다</div>`:""}
            ${over?`<div class="ct-warn">성인 ${ad}명보다 ${n-ad}명 많습니다</div>`:""}</div>`;''',
'''            ${short?`<div class="ct-warn">성인 ${ad}명보다 ${ad-n}명 적습니다</div>`:""}
            ${over?`<div class="ct-warn">성인 ${ad}명보다 ${n-ad}명 많습니다</div>`:""}
            ${courseWarns().map(w=>`<div class="ct-warn">${esc(w)}</div>`).join("")}</div>`;''')
# 코스 합계 칸이 경고 유무로 커졌다 작아지지 않게 .bad 판정에 코스 경고도 포함
rep('''          const short = n>0 && n<ad, over = n>ad;
          return `<div class="course-total ${short||over?'bad':''}">선택 합계 <b>${n}</b>명''',
'''          const short = n>0 && n<ad, over = n>ad;
          return `<div class="course-total ${short||over||courseWarns().length?'bad':''}">선택 합계 <b>${n}</b>명''')

# ---------- 5단계: 노쇼 안내 자리 확보 ----------
rep('''      ${noshowHint()}
    </div>
    `;
}''',
'''      <div class="ns-slot">${noshowHint()}</div>
    </div>
    `;
}''')

# ---------- 전화번호 하이픈 자동 정리 ----------
rep('''function fmtPhone(el){
  const raw = el.value;
  if(raw.indexOf("-") >= 0){ WZ.phone = raw; return; }
  const d = raw.replace(/\\D/g,"").slice(0,11);
  let out = d;
  if(d.indexOf("010") === 0){
    if(d.length>3 && d.length<8) out = d.slice(0,3)+"-"+d.slice(3);
    else if(d.length>=8) out = d.slice(0,3)+"-"+d.slice(3,d.length-4)+"-"+d.slice(d.length-4);
  }
  el.value = out; WZ.phone = out;
}''',
'''/* ※ 예전에는 "값에 - 가 하나라도 있으면 손대지 않음" 이었는데, 시스템이 넣은 - 도 그 조건에 걸려
      010-1234 까지 만든 뒤로는 다시 정리하지 않아 010-12345678 이 됐습니다.
      이제 '사용자가 - 를 직접 쳤는지'(phoneManual)만 보고, 아니면 숫자만으로 매번 다시 만듭니다 */
function fmtPhone(el, ev){
  const raw = el.value;
  if(ev && ev.inputType==="insertText" && ev.data==="-") WZ.phoneManual = true;
  if(!raw.replace(/\\D/g,"")) WZ.phoneManual = false;        /* 다 지우면 다시 자동으로 */
  if(WZ.phoneManual){ WZ.phone = raw; return; }
  const out = phoneFmt(raw.replace(/\\D/g,"").slice(0,11));
  if(el.value !== out) el.value = out;
  WZ.phone = out;
}
/* 숫자열 → 하이픈 넣은 번호. 휴대폰(01x) 3-4-4, 서울(02) 2-3-4 / 2-4-4, 지역번호(033 등) 3-3-4 / 3-4-4, 1588 류 4-4.
   입력 중(자릿수가 다 안 찼을 때)에도 앞부분 하이픈은 미리 넣어 줍니다 */
function phoneFmt(d){
  if(!d) return "";
  let a = 3;                                   /* 앞자리(지역·통신사) 길이 */
  if(d.indexOf("02") === 0) a = 2;
  else if(/^1[5-9]/.test(d)) a = 4;            /* 1588-0000 같은 대표번호 */
  if(d.length <= a) return d;
  const rest = d.slice(a);
  if(a === 4) return d.slice(0,4) + "-" + rest;
  /* 가운데 자리: 휴대폰은 4, 그 외는 전체 길이가 (a+8) 이면 4, 아니면 3 */
  const mobile = d.indexOf("01") === 0;
  const mid = mobile ? 4 : (d.length >= a+8 ? 4 : 3);
  if(rest.length <= mid) return d.slice(0,a) + "-" + rest;
  return d.slice(0,a) + "-" + rest.slice(0,mid) + "-" + rest.slice(mid);
}''')
rep('''    phoneEl.oninput = ()=>{ fmtPhone(phoneEl); wzRefreshNext(); };''',
    '''    phoneEl.oninput = (ev)=>{ fmtPhone(phoneEl, ev); wzRefreshNext(); };''')

# ---------- 같은 화면을 다시 그릴 때는 시트 등장 애니메이션을 끕니다 (코스를 누를 때마다 창이 다시 열리는 것처럼 보이던 것) ----------
rep('''function renderApp(){
  saveScroll();
  applyTheme();''',
'''var lastPopKey = "";
/* 어떤 팝업이 떠 있는지 열쇠. 직전 그리기와 같으면 '같은 팝업을 고쳐 그린 것' 이므로 등장 움직임을 생략합니다 */
function popKey(){
  const t = WZ ? WZ : tmpRes;
  return viewKey() + "|" + (t && t.courseOpen ? "course" : "-") + "|" + (MODAL ? "modal" : "-");
}
function renderApp(){
  saveScroll();
  applyTheme();
  const pk = popKey();
  document.body.classList.toggle("same-pop", pk === lastPopKey);
  lastPopKey = pk;''')

# ---------- 상단바: 맨 왼쪽 버튼 삭제 → 매장 이름이 그 역할, 오른쪽에 더보기(⋮) ----------
rep('''        <button class="home" onclick="${view.tab==="settings"?"setTab('dash')":"goHome()"}"
          aria-label="${view.tab==="settings"?"대시보드로":"매장 선택"}"
          title="${view.tab==="settings"?"대시보드로":"매장 선택"}">${view.tab==="settings"?"←":ICON.store}</button>
        <button class="storename" onclick="setTab('dash')" title="대시보드로 이동">${esc(s.name)}</button>''',
'''        <!-- 매장 이름 = 예전 맨 왼쪽 버튼의 역할. 대시보드에서는 매장 선택으로, 설정에서는 대시보드로 -->
        <button class="storename" onclick="${view.tab==="settings"?"setTab('dash')":"goHome()"}"
          title="${view.tab==="settings"?"대시보드로":"매장 선택"}">${view.tab==="settings"?'<span class="sn-ic">←</span>':ICON.store}${esc(s.name)}</button>''')
rep('''        <div class="bar-right">
          ${view.tab==="settings" ? "" : `
          <button class="tvbtn icon b-chart" onclick="openRate()" title="예약률 추이">${ICON.chart}</button>`}
          <button class="tvbtn icon b-set ${view.tab==="settings"?'on':''}"
            onclick="setTab('${view.tab==="settings"?"dash":"settings"}')" title="설정">${ICON.set}</button>
          <button class="tvbtn icon b-tv" onclick="openDisplay()" title="디스플레이 모드">${ICON.tv}</button>
          ${view.tab==="settings" ? "" : `
          <button class="tvbtn b-search" onclick="openSearch()">예약 검색</button>
          <button class="tvbtn accent b-add" onclick="openWizard('${view.date}')">＋ 예약 등록</button>`}
        </div>''',
'''        <div class="bar-right">
          ${view.tab==="settings" ? "" : `
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
        </div>
        ${view.moreOpen ? `<div class="more-veil" onclick="closeMore()"></div>` : ""}''')
rep('''/* 매장 아이콘 = 로그아웃 (PIN 이라 부담이 적습니다) */
function goHome(){''',
'''/* 상단바 더보기(⋮) 열고 닫기. 바깥(투명 막)을 누르면 닫힙니다 */
function toggleMore(){ view.moreOpen = !view.moreOpen; render(); }
function closeMore(){ if(view.moreOpen){ view.moreOpen = false; render(); } }
/* 매장 이름 누르기 = 매장 선택으로 (로그아웃. PIN 이라 부담이 적습니다) */
function goHome(){''')
rep('''  cal:'<svg viewBox="0 0 24 24">''',
    '''  more:'<svg viewBox="0 0 24 24"><circle cx="12" cy="5" r="1.6" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.6" fill="currentColor" stroke="none"/><circle cx="12" cy="19" r="1.6" fill="currentColor" stroke="none"/></svg>',
  cal:'<svg viewBox="0 0 24 24">''')

# ---------- 대시보드: 지표줄을 타임라인 아래로 (예약 목록 위), 칸은 낮게 ----------
rep('''  return `
    <section class="card">
      <div class="metrics">
        <div class="metric"><div class="v">${active.length}<span class="u">건</span></div>''',
'''  /* 순서: 타임라인(오늘 상황이 한눈에) → 지표줄 → 예약 목록. 지표는 눌러서 여는 목록의 입구 역할이라 목록 바로 위가 맞습니다 */
  const metrics = `
    <section class="card metrics-card">
      <div class="metrics">
        <div class="metric"><div class="v">${active.length}<span class="u">건</span></div>''')
rep('''          <div class="k">확인 필요</div><div class="s">${checkCnt?"눌러서 확인":"모두 확인됨"}</div></button>
      </div>
    </section>

    <div class="card"><div class="card-b">${renderTimeline(d)}</div></div>



    <div style="height:20px"></div>
    ${foldCard("list", "예약 목록", `${dayRes.length}건`, renderResList(d))}''',
'''          <div class="k">확인 필요</div><div class="s">${checkCnt?"눌러서 확인":"모두 확인됨"}</div></button>
      </div>
    </section>`;

  return `
    <div class="card"><div class="card-b">${renderTimeline(d)}</div></div>
    ${metrics}
    ${foldCard("list", "예약 목록", `${dayRes.length}건`, renderResList(d))}''')

io.open(SRC, "w", encoding="utf-8", newline="\n").write(s)
print("JS 패치 완료:", n_ok, "곳")
