# -*- coding: utf-8 -*-
"""8차-AA — 재아: 인트로 조금 더 빠르게, 비상예약지 버튼 밑줄 제거, 설정 항목 제목↔조작부 점선 안내선 + 조작부 축소,
   마법사 이전/다음을 입력부 폭에 맞춤, 경로 카드가 폭을 안 넘게"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 인트로 속도 ----------
s = R(s, """  var steps = INTRO_TO.length, t0 = 160, gap = 200;""", """  var steps = INTRO_TO.length, t0 = 120, gap = 150;   /* 8차-AA(재아): 조금 더 빠르게 — 글자 150ms 간격, 총 1.3초쯤 */""")
s = R(s, """  introTimers.push(setTimeout(endIntro, t0 + steps*gap + 600));""", """  introTimers.push(setTimeout(endIntro, t0 + steps*gap + 450));""")
s = R(s, """  transition:opacity .01s steps(1,end), transform .6s steps(3,end)}""", """  transition:opacity .01s steps(1,end), transform .45s steps(3,end)}""")
s = R(s, """background:#241E1A; transition:width .6s steps(3,end) .2s}""", """background:#241E1A; transition:width .45s steps(3,end) .15s}""")
s = R(s, """animation:intro-scan 1.2s steps(6,end) .2s 1 forwards}""", """animation:intro-scan .9s steps(6,end) .15s 1 forwards}""")

# ---------- 비상예약지: 링크 버튼 밑줄 없이 (새 탭은 이미 target=_blank) ----------
s = R(s, """.btn{border:1px solid var(--border-strong); background:var(--surface); color:var(--text); font-size:var(--fs-body); font-weight:600; padding:var(--s12) var(""",
         """a.btn{text-decoration:none; display:inline-flex; align-items:center}   /* 링크로 만든 버튼(비상 예약지 인쇄)도 버튼처럼 */
.btn{border:1px solid var(--border-strong); background:var(--surface); color:var(--text); font-size:var(--fs-body); font-weight:600; padding:var(--s12) var(""")

# ---------- 설정: 제목 → 조작부 점선 안내선, 조작부 크기 줄임 ----------
s = R(s, """.fold-b .f > .lb{margin:0}""",
""".fold-b .f > .lb{margin:0; display:flex; align-items:center; min-width:0}
/* 제목과 조작부가 멀어 눈이 헤맵니다 — 사이를 점선으로 이어 줍니다(8차-AA 재아) */
.fold-b .f > .lb:after{content:""; flex:1; min-width:16px; margin:0 var(--s12); border-bottom:1px dotted var(--border-strong); transform:translateY(1px)}
/* 조작부는 제목 글씨(fs-sub)에 맞춰 작게 — 설정은 '읽는 화면' 이라 큰 버튼이 어울리지 않습니다 */
.fold-b .togglebtn, .fold-b .numbtn{font-size:var(--fs-sub); padding:var(--s8) var(--s12); min-height:0}
.fold-b .numbtn{font-size:var(--fs-body)}
.fold-b .seg button{font-size:var(--fs-sub); padding:var(--s4) var(--s12); min-height:0}
.fold-b .f > input[type=time], .fold-b .f > input[type=text], .fold-b .f > input:not([type]){padding:var(--s8) var(--s12); font-size:var(--fs-sub)}
.fold-b .btn:not(.lg){font-size:var(--fs-sub); padding:var(--s8) var(--s12); min-height:0}""")

# ---------- 마법사 이전/다음: 입력부(.wz-body) 폭까지만 ----------
s = R(s, """.wz-q{text-align:center; padding:var(--s8) var(--s16) var(--s4); display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:var(--s12)}""",
         """.wz-q{text-align:center; padding:var(--s8) var(--s16) var(--s4); display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:var(--s12); max-width:940px; width:100%; margin:0 auto}   /* 폭은 .wz-body 와 같게 — 이전/다음이 입력부 끝선에 옵니다(재아) */""")
s = R(s, """  .wz-body{padding:var(--s16) var(--s24) var(--s24)}
  .wz-foot{""", """  .wz-body{padding:var(--s16) var(--s24) var(--s24)}
  .wz-q{padding-left:var(--s24); padding-right:var(--s24)}
  .wz-foot{""")
s = R(s, """  .wz-body{max-width:1120px}
  .bday{min-height:58px}""", """  .wz-body{max-width:1120px}
  .wz-q{max-width:1120px}
  .bday{min-height:58px}""")

# ---------- 경로 카드: 폭을 넘지 않게 ----------
s = R(s, """.srcgrid{display:grid; grid-template-columns:1fr 1fr; gap:var(--s12)}""",
         """.srcgrid{display:grid; grid-template-columns:1fr 1fr; gap:var(--s12); width:100%; min-width:0}
.srcgrid > .srccell{min-width:0; width:100%; box-sizing:border-box}   /* 글자가 길어도 칸이 폭을 밀어내지 않게 */
.srccell .s-l{overflow:hidden; text-overflow:ellipsis; white-space:nowrap}""")

L.js_check(s)
L.save(s)
print("p9_aa 적용")
