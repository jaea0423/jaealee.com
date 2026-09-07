"""v3 2차 — "전화 받으면서 한 손으로 쓰는 도구" 방향으로 알아서 개선한 묶음.
   규칙: 경고가 없으면 고르는 순간 넘어가고, 경고가 있으면 멈춰서 빨갛게 보여 준다."""
import os, sys, io
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "index.html")
s = io.open(SRC, encoding="utf-8").read()
n_ok = 0
def rep(old, new, count=1):
    global s, n_ok
    c = s.count(old)
    if c != count:
        print("!! 치환 실패 (%d번 발견, %d번 기대):\n%s" % (c, count, old[:200])); sys.exit(1)
    s = s.replace(old, new); n_ok += 1

# ---------- 공통: 경고 없으면 바로 다음 단계 ----------
rep('''/* 다음으로 넘어갈 수 있는지 검사 */
function wzCanNext(){''',
'''/* 고르는 순간 다음 단계로 — 단, 경고가 걸리면 이 화면에 멈춰서 빨갛게 보여 줍니다.
   (넘어가 버리면 경고를 아무도 못 봅니다. 확인 팝업이 이미 뜬 것도 여기서 한 번 더 걸립니다) */
function wzAutoNext(){
  if(WZ.step < LAST_STEP && wzCanNext() && !wzWarnReason()) wzGo(WZ.step + 1);
  else render();
}
/* 다음으로 넘어갈 수 있는지 검사 */
function wzCanNext(){''')
rep('''  if(v !== "기타"){ wzGo(1); return; }
  render();
}''',
'''  if(v !== "기타"){ wzAutoNext(); return; }
  render();
}''')
# 좌석: 확인 팝업을 다 지나 왔으면 바로 다음
rep('''    WZ.tentative = sug;
  }
  WZ.seat = v; render();
}''',
'''    WZ.tentative = sug;
  }
  WZ.seat = v; wzAutoNext();
}''')
# 메뉴: 코스가 아니면 바로 다음 (룸에 '해당 없음' 같은 경고가 걸리면 멈춥니다)
rep('''function wzMenu(v){
  WZ.menuType = v;
  if(v==="코스"){ WZ.courseOpen = true; }
  else { WZ.courses = {}; WZ.courseOpen = false; }
  render();
}''',
'''function wzMenu(v){
  WZ.menuType = v;
  if(v==="코스"){ WZ.courseOpen = true; render(); return; }
  WZ.courses = {}; WZ.courseOpen = false;
  wzAutoNext();
}
/* 코스 팝업의 '완료' — 마법사에서는 코스 인원이 맞으면 바로 예약자 단계로 */
function doneCourse(){
  cSync(); const t=cTgt(); if(t) t.courseOpen = false;
  if(WZ) wzAutoNext(); else render();
}''')
rep('''          <button class="btn primary" onclick="closeCourse()">완료</button>''',
    '''          <button class="btn primary" onclick="doneCourse()">완료</button>''')

# ---------- 1단계: 휴무·지난 날짜 안내를 위쪽 경고 자리로 (시간 칸 위에 끼어들던 노란 띠 삭제) ----------
rep('''  if(WZ.step===1 && WZ.time){
    if(WZ.date < todayStr()) out.push("이미 지난 날짜입니다");
    out.push.apply(out, timeWarns(WZ.date, WZ.time));
  }''',
'''  if(WZ.step===1){
    const dh = hoursFor(WZ.date);
    if(WZ.date < todayStr()) out.push("이미 지난 날짜입니다");
    if(WZ.time) out.push.apply(out, timeWarns(WZ.date, WZ.time));
    else if(dh.closed) out.push(`휴무일입니다${dh.note?` (${dh.note})`:""}`);
  }''')
rep('''      ${dh.closed?`<div class="warnbar">${dateLabel(WZ.date)}은 휴무일입니다 (${esc(dh.note||"")}). 그래도 접수하려면 시간을 선택하세요.</div>`:""}
      ${isPastDate?`<div class="warnbar">이미 지난 날짜입니다 — ${dateLabel(WZ.date)}. 누락된 예약을 입력하는 경우가 아니라면 날짜를 다시 확인하세요.</div>`:""}
      <div class="hours-line">''',
'''      <div class="hours-line">''')

# ---------- 3단계: 안내문 짧게 ----------
rep('''        return `현재 설정 : <b>${hm(WZ.time)}</b>, 홀 좌석 체류 시간 ${f(hallM)}, 룸 좌석 체류 시간 ${f(roomM)}`;''',
    '''        return `<b>${hm(WZ.time)}</b> 입장 · 홀 ${f(hallM)} · 룸 ${f(roomM)} 머무는 기준`;''')

# ---------- 코스 팝업: 첫 탭에 성인 수만큼 채우고, 모서리 −로 줄입니다 ----------
rep('''function bumpCourse(key){
  cSync(); const t=cTgt(); if(!t) return;
  t.courses = {...t.courses, [key]:((t.courses||{})[key]||0)+1};
  render();
}''',
'''/* 한 테이블은 코스를 통일하는 것이 규칙이라, 처음 누르면 '아직 코스가 없는 성인 수'만큼 한 번에 채웁니다.
   (4명 테이블이면 탭 한 번에 4). 그 뒤로는 누를 때마다 1씩, 줄일 때는 모서리 − 로 */
function bumpCourse(key){
  cSync(); const t=cTgt(); if(!t) return;
  const cur = (t.courses||{})[key]||0;
  let add = 1;
  if(!cur){
    const adults = adultCount(t.people||0, t.infants||0);
    add = Math.max(1, adults - courseCount());
  }
  t.courses = {...t.courses, [key]:cur+add};
  t.courseUndecided = false;
  render();
}
function dropCourse(key){
  cSync(); const t=cTgt(); if(!t) return;
  const cur = (t.courses||{})[key]||0;
  const next = {...t.courses}; if(cur<=1) delete next[key]; else next[key] = cur-1;
  t.courses = next; render();
}''')
rep('''          return `<button class="citem ${c?'on':''} ${off&&c?'warned':''}" onclick="bumpCourse('${key}')">
            ${esc(name)}${c?`<i class="cnum">${c}</i>`:""}</button>`;''',
'''          return `<span class="citem-w"><button class="citem ${c?'on':''} ${off&&c?'warned':''}" onclick="bumpCourse('${key}')">
            ${esc(name)}${c?`<i class="cnum">${c}</i>`:""}</button>${c?`<button class="cminus" onclick="dropCourse('${key}')" aria-label="하나 줄이기">−</button>`:""}</span>`;''')

# ---------- 상단바: '오늘' 버튼 (오늘이 아닐 때만 보이고, 자리는 항상) ----------
rep('''          <button class="bnav" onclick="moveDate(1)" title="내일">&rsaquo;</button>
          <button class="bnav mo" onclick="moveMonthDate(1)" title="다음 달">&raquo;</button>
        </div>`}''',
'''          <button class="bnav" onclick="moveDate(1)" title="내일">&rsaquo;</button>
          <button class="bnav mo" onclick="moveMonthDate(1)" title="다음 달">&raquo;</button>
          <button class="btoday ${view.date===todayStr()?'ghost':''}" onclick="goToday()" ${view.date===todayStr()?'tabindex="-1"':''}>오늘</button>
        </div>`}''')
rep('''function moveDate(d){ view.date=shiftDate(view.date,d); render(); }''',
    '''function moveDate(d){ view.date=shiftDate(view.date,d); render(); }
/* 다른 날을 보다가 오늘로 한 번에 — 화살표를 여러 번 누르거나 달력을 열 필요가 없게 */
function goToday(){ view.date = todayStr(); render(); }''')

# ---------- CSS ----------
rep('''/* ---- 상단바: 맨 왼쪽 버튼을 없애고 매장 이름이 그 일을 합니다 ---- */''',
'''/* 코스 칸 + 모서리 − (처음 누르면 성인 수만큼 채워지므로 줄이는 길이 필요합니다) */
.citem-w{position:relative; display:block}
.citem-w .citem{width:100%}
.cminus{position:absolute; left:-6px; top:-8px; width:26px; height:26px; border-radius:50%; border:2px solid var(--bg);
  background:var(--text-2); color:#fff; font-size:var(--fs-body); line-height:1; display:grid; place-items:center; padding:0; z-index:1}
/* 합계 칸은 경고 한 줄만큼 자리를 미리 — 경고가 생길 때 시트가 커지지 않게 */
.course-total{min-height:64px}
/* '오늘' 버튼 — 오늘이면 .ghost 로 자리만 지킵니다 (날짜가 가운데에서 흔들리지 않게 왼쪽에 같은 폭의 빈 칸) */
.btoday{border:1px solid var(--topbar-btn-line); background:transparent; color:var(--topbar-fg); border-radius:var(--r-sm);
  height:34px; min-height:34px; padding:0 var(--s12); font-size:var(--fs-sub); font-weight:700; opacity:.85; flex:none; margin-left:var(--s8)}
.btoday:hover{background:var(--topbar-hover); opacity:1}
.bar-mid::before{content:""; width:52px; flex:none; margin-right:var(--s8)}
@media (max-width:900px){ .bar-mid::before{display:none} }

/* ---- 상단바: 맨 왼쪽 버튼을 없애고 매장 이름이 그 일을 합니다 ---- */''')

io.open(SRC, "w", encoding="utf-8", newline="\n").write(s)
print("2차 패치 완료:", n_ok, "곳")
