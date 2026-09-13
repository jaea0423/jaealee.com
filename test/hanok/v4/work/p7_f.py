# -*- coding: utf-8 -*-
"""v4 6차-F — 재아 검토 뒤 손질 (2026-09-14)
   A 타임라인 범례에 '오늘 변동'(파랑) 추가
   B 변동 블록 테두리 2px → 4px (2px 는 티가 안 남). 잠정은 점선 — 잠정+경고가 같이 오면 '점선 벽돌' 로 둘 다 보이게
   C 코스 선택 − 버튼 부활 (처음 누르면 성인 수만큼 채워져 그보다 적게 고를 길이 없었음)
   D PIN 글자 — 원을 대신해 큰 글자(40px), 글꼴을 과할 만큼 다르게
   E 오늘 버튼·'지난 날짜'/'D-n' 표시 삭제 (날짜를 눌러 달력에서 고름)
   F 인트로 더 짧게 — 붉은 첫 장면이 길었음. t0 380→160, gap 260→200, 끝 +700→+600 (총 2.4s → 1.8s)"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---------- A. 범례 ----------
rep(""".lgsw.warn{background:var(--rust)}
""",
""".lgsw.warn{background:var(--rust)}
/* 오늘 변동 — 블록과 같은 파랑 + 검정 테두리 (타임라인 .blk.changed 참고) */
.lgsw.chg{background:var(--blue); border:3px solid #2C2C2E; width:18px; height:14px}
""")
rep("""        <span class="tl-legend"><i class="lgsw warn"></i>경고</span>
      </div>""",
"""        <span class="tl-legend"><i class="lgsw warn"></i>경고</span>
        <span class="tl-legend"><i class="lgsw chg"></i>오늘 변동</span>
      </div>""")

# ---------- B. 변동 블록 테두리 4px, 잠정은 점선 ----------
rep("""   원래 상태색(확정 먹색 / 잠정 회색 / 경고 벽돌)은 2px 테두리로 옮겨 상태를 잃지 않게 합니다.
   3px 는 블록 높이 19px 에서 글자 자리를 잡아먹어 2px 고정. 내일이 되면 changeTag 가 비어 저절로 풀립니다.""",
"""   원래 상태색(확정 먹색 / 잠정 회색 / 경고 벽돌)은 4px 테두리로 옮겨 상태를 잃지 않게 합니다.
   처음 2px 로 했더니 티가 안 나 4px 로(재아 검토). 블록 높이 19px 에서 안쪽 11px 가 남아 11px 글자가 딱 들어갑니다.
   잠정은 점선 — 그래서 잠정+경고(룸 미정인데 코스 인원 부족 등)가 같이 오면 '점선 벽돌' 로 둘 다 읽힙니다.
   내일이 되면 changeTag 가 비어 저절로 풀립니다.""")
rep("""button.blk.changed{background:var(--blue); color:#fff; border:2px solid var(--text); padding-left:var(--s4)}
button.blk.changed.tent{border:2px solid #8E8A80}
button.blk.changed.warned, button.blk.changed.tent.warned{border:2px solid var(--rust)}""",
"""button.blk.changed{background:var(--blue); color:#fff; border:4px solid var(--text); padding-left:var(--s4)}
button.blk.changed.tent{border:4px dashed #8E8A80}
button.blk.changed.warned{border:4px solid var(--rust)}
button.blk.changed.tent.warned{border:4px dashed var(--rust)}""")

# ---------- C. 코스 − 버튼 ----------
rep("""            ${esc(name)}${c?`<i class="cnum">${c}</i>`:""}</button></span>`;""",
    """            ${esc(name)}${c?`<i class="cnum">${c}</i>`:""}</button>${c?`<button class="cminus" onclick="dropCourse('${key}')" aria-label="하나 줄이기">−</button>`:""}</span>`;""")

# ---------- D. PIN 글자 ----------
rep(""".pdots{display:flex; justify-content:center; margin:var(--s24) 0 var(--s8); gap:var(--s16)}
.pdot{width:34px; height:34px; border:1.5px solid var(--border-strong); background:transparent; display:grid; place-items:center; font-size:var(--fs-head); font-weight:700; color:transparent; transition:color .2s ease; box-shadow:none; border-radius:50%}
/* 채워지면 원은 그대로(빈 테두리) 두고 글자만 나타납니다. 6차 1차 때 '먹색 원 + 흰 글자' 로 바꿨다가 되돌림 —
   원래 규칙은 테두리도 지웠는데, 글자만 떠 있으면 자리 수가 안 보여 테두리는 남깁니다 */
.pdot.on{color:var(--text)}
/* 글자마다 다른 글꼴 — 내장 글꼴만 씁니다(Nanum Myeongjo 는 외부 글꼴이라 지움).
   f3 은 명조 합성 이탤릭(기울임 파일이 없어 브라우저가 기울입니다) */
.pdot.f1{font-family:'Noto Serif KR',serif; font-weight:900}
.pdot.f2{font-family:'Pretendard',sans-serif; font-weight:700}
.pdot.f3{font-family:'Noto Serif KR',serif; font-weight:900; font-style:italic}
.pdot.f4{font-family:'Pretendard',sans-serif; font-weight:400}
""",
""".pdots{display:flex; justify-content:center; align-items:center; margin:var(--s24) 0 var(--s8); gap:var(--s12); height:56px}
.pdot{width:48px; height:48px; border:1.5px solid var(--border-strong); background:transparent; display:grid; place-items:center; font-size:40px; line-height:1; color:transparent; transition:color .2s ease; box-shadow:none; border-radius:50%}
/* 채워지면 원이 사라지고 그 자리에 큰 글자가 들어옵니다 (원 안의 작은 글자는 심심하다는 평 — 6차-F).
   글자마다 글꼴을 과할 만큼 다르게 — 내장 글꼴 두 벌(Pretendard·Noto Serif KR)만으로 기울임·외곽선·회전으로 변화를 줍니다 */
.pdot.on{border-color:transparent; color:var(--text)}
.pdot.f1{font-family:'Noto Serif KR',serif; font-weight:900}                                                  /* 한 — 굵은 명조 */
.pdot.f2{font-family:'Pretendard',sans-serif; font-weight:700; font-style:italic; letter-spacing:-.05em}      /* 옥 — 기울인 굵은 고딕(합성 이탤릭) */
.pdot.f3{font-family:'Noto Serif KR',serif; font-weight:900}                                                  /* 반 — 속이 빈 외곽선 명조 */
.pdot.f3.on, body.theme-hanok .pdot.f3.on{color:transparent; -webkit-text-stroke:1.6px var(--text)}
.pdot.f4{font-family:'Pretendard',sans-serif; font-weight:400; transform:rotate(-10deg)}                      /* 점 — 가는 고딕을 살짝 기울여 (회전은 배율과 무관) */
""")

# ---------- E. 오늘 버튼 · 방향 표시 삭제 ----------
rep("""   6차 전에는 지난 날짜 회갈색 / 다음 날짜 노랑이었는데 차이가 약하고 노랑은 경고로 읽혀서,
   방향 구분은 색 대신 날짜 옆 작은 글자(.nt-tag — '지난 날짜' / 'D-3')로 옮겼습니다.
""",
"""   6차 전에는 지난 날짜 회갈색 / 다음 날짜 노랑이었는데 차이가 약하고 노랑은 경고로 읽혀 검정 하나로.
   방향 표시('지난 날짜'/'D-3')와 '오늘' 버튼은 6차-F 에서 뺐습니다 — 날짜를 눌러 달력에서 고릅니다.
""")
rep(""".topbar.notoday .nt-tag{font-size:var(--fs-label); font-weight:600; color:rgba(255,255,255,.7); margin-left:var(--s8); letter-spacing:0}
""", "")
rep("""/* '오늘' 버튼 — 오늘로 돌아오는 유일한 한 번 탭 경로라 없애지 않습니다. 오늘이 아닐 때만 그리고 흰 테두리 */
.topbar.notoday .btoday{border-color:#fff; color:#fff; opacity:1}
""", "")
rep("""/* '오늘' 버튼 — 오늘이 아닐 때만 그립니다(6차). 날짜가 가운데에서 흔들리지 않게 그때만 왼쪽에 같은 폭의 빈 칸(::before)을 둡니다.
   오늘이면 버튼도 빈 칸도 없으니 양쪽이 비어 역시 가운데입니다 */
.btoday{border:1px solid var(--topbar-btn-line); background:transparent; color:var(--topbar-fg); border-radius:var(--r-sm);
  height:34px; min-height:34px; padding:0 var(--s12); font-size:var(--fs-sub); font-weight:700; opacity:.85; flex:none; margin-left:var(--s8)}
.btoday:hover{background:var(--topbar-hover); opacity:1}
.topbar.notoday .bar-mid::before{content:""; width:52px; flex:none; margin-right:var(--s8)}
@media (max-width:900px){ .topbar.notoday .bar-mid::before{display:none} }
""", "")
rep(""".btn, .btn.sm, .btn.lg, .tvbtn, .topbar .tvbtn, .topbar .home, .bdate, .btoday, .wz-back,""",
    """.btn, .btn.sm, .btn.lg, .tvbtn, .topbar .tvbtn, .topbar .home, .bdate, .wz-back,""")
rep("""          <button class="bdate" onclick="openCal()" title="달력 열기">${dateLabel(view.date)}${notodayTag()}</button>""",
    """          <button class="bdate" onclick="openCal()" title="달력 열기">${dateLabel(view.date)}</button>""")
rep("""          <button class="bnav mo" onclick="moveMonthDate(1)" title="다음 달">&raquo;</button>
          ${view.date===todayStr() ? '' : '<button class="btoday" onclick="goToday()">오늘</button>'}
        </div>`}""",
"""          <button class="bnav mo" onclick="moveMonthDate(1)" title="다음 달">&raquo;</button>
        </div>`}""")
rep("""function goToday(){ view.date = todayStr(); render(); }
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
""",
"""/* '오늘이 아닌 날짜를 보는 중' — 상단바(.topbar.notoday)와 body.notoday 가 같은 조건을 써야 하므로 한 곳에.
   설정 탭은 날짜 개념이 없어 제외. 디스플레이·잠금·인트로는 renderApp 이 renderStore 전에 갈라져 나가므로 여기서도 빼 둡니다.
   ('오늘' 버튼과 goToday 는 6차-F 에서 삭제 — 오늘로 돌아올 때도 날짜를 눌러 달력에서 고릅니다) */
function notodayView(){
  return !!view.storeKey && AUTHED && !view.display && !INTRO && view.tab!=="settings" && view.date!==todayStr();
}
""")

# ---------- F. 인트로 더 짧게 ----------
rep("""  /* 글자 5개가 260ms 간격(1.3초) — 6차 전(135ms)에는 거의 동시에 바뀌어 단계가 안 느껴졌습니다.
     마지막 글자 뒤 700ms 에 끝. 총 약 2.4초, 아무 데나 누르면 건너뜀 */
  var steps = INTRO_TO.length, t0 = 380, gap = 260;
  for(var i=1;i<=steps;i++){
    introTimers.push(setTimeout((function(k){ return function(){ introStep(k); }; })(i), t0 + i*gap));
  }
  introTimers.push(setTimeout(endIntro, t0 + steps*gap + 700));""",
"""  /* 글자 5개가 200ms 간격(1초) — 135ms 는 거의 동시라 단계가 안 느껴졌고, 260ms 는 붉은 첫 장면이 길었습니다(6차-F).
     첫 글자는 360ms, 마지막 글자 뒤 600ms 에 끝. 총 약 1.8초, 아무 데나 누르면 건너뜀 */
  var steps = INTRO_TO.length, t0 = 160, gap = 200;
  for(var i=1;i<=steps;i++){
    introTimers.push(setTimeout((function(k){ return function(){ introStep(k); }; })(i), t0 + i*gap));
  }
  introTimers.push(setTimeout(endIntro, t0 + steps*gap + 600));""")
rep("""/* 바탕 전환은 글자 간격(260ms)보다 조금 길게 — 1.1s 는 마지막 글자 뒤 700ms 에 끝나는 인트로보다 늦게 끝났습니다 */
.intro-bg{position:absolute; top:0; right:0; bottom:0; left:0; transition:opacity .7s ease}""",
"""/* 바탕 전환은 글자 간격(200ms)보다 조금 길게 — 너무 길면 마지막 글자 뒤 600ms 에 끝나는 인트로보다 늦게 끝납니다 */
.intro-bg{position:absolute; top:0; right:0; bottom:0; left:0; transition:opacity .55s ease}""")
rep(""".intro .ic{display:inline-block; transition:opacity .7s ease, filter .7s ease, transform .7s ease, color .8s ease}   /* 글자 간격 260ms 에 맞춰 .55 → .7 */""",
    """.intro .ic{display:inline-block; transition:opacity .55s ease, filter .55s ease, transform .55s ease, color .6s ease}   /* 글자 간격 200ms 에 맞춰 */""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_f 적용 완료")
