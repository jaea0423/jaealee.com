"""v3 1차 — CSS 패치. 11구역(반응형) 끝, 12구역(@supports) 바로 앞에 v3 블록을 덧붙입니다.
   맨 뒤에 두는 이유: 같은 우선순위면 뒤가 이기므로 앞의 기본값·미디어 규칙을 확실히 덮습니다."""
import os, sys, io
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "index.html")
s = io.open(SRC, encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    c = s.count(old)
    if c != count:
        print("!! 치환 실패 (%d번 발견):\n%s" % (c, old[:160])); sys.exit(1)
    s = s.replace(old, new)

# 1024 이상에서 달력을 grid 로 두던 규칙 — 아래 v3 블록에서 flex 열로 바꾸므로 지웁니다 (grid 가 남으면 flex:1 이 안 먹음)
rep('''@media (min-width:1024px){
  .wz-cal{display:grid; grid-template-columns:1fr; gap:0}
  .bday{min-height:76px}''',
'''@media (min-width:1024px){
  .bday{min-height:76px}''')

BLOCK = r'''
/* ============================================================
   v3 1차 — 재아 요청 반영 (2026-09-07)
   원칙: "누르는 선택에 따라 화면 높이가 바뀌지 않게". 나타났다 사라지는 요소는 자리를 미리 잡아 두고(.ghost / 슬롯)
   보이기만 바꿉니다. visibility:hidden 은 display:none 과 달리 자리를 그대로 차지합니다.
   ============================================================ */
/* 자리만 지키고 보이지 않는 요소 — 경로 입력창 · 직접 입력 스테퍼 · 코스 요약 줄 */
.ghost{visibility:hidden; pointer-events:none}
.src-detail{margin-top:18px}
/* 경고 자리: 항상 두 줄(40px)만큼 비워 둡니다. 경고가 생겨도 아래 본문이 밀리지 않습니다.
   세 줄 이상 걸리는 경우(지난 날짜 + 라스트오더 + 마감)는 드물어 그때만 조금 밀립니다 */
.wz-warn{min-height:40px; line-height:20px; margin-top:var(--s8)}
/* 노쇼 안내 자리 (전화번호 아래) */
.ns-slot{min-height:40px; margin-top:var(--s8)}
.ns-slot .ns-hint{margin-top:0}
/* 분 조절: 시각을 고르기 전에는 흐리게, 손잡이·채움만 숨김 (레일 높이는 그대로) */
.mwrap.idle{opacity:.5; pointer-events:none}
.mwrap.idle .mknob, .mwrap.idle .mfill{visibility:hidden}
.mwrap.idle .mhead .mnow{color:var(--text-3); font-size:var(--fs-sub); font-weight:600}
/* 달력이 시간 칸과 키를 맞춥니다 — 900px 이상에서 좌우로 놓일 때 날짜 칸이 남는 높이를 나눠 가집니다 */
.wz-cal{display:flex; flex-direction:column}
.wz-cal .bgrid:last-child{flex:1; grid-auto-rows:1fr}
@media (min-width:900px){
  .wz-step1{align-items:stretch}
}
/* 시각 글자까지 벽돌색 — 경고 걸리는 시각은 칸 아래 작은 글씨만으로는 멀리서 안 보입니다 */
.hcell .ap.rust, .hcell .hh.rust{color:var(--rust)}
.hcell.on .ap.rust, .hcell.on .hh.rust{color:#fff}
/* 같은 팝업을 고쳐 그린 것이면 등장 움직임 생략 — 코스를 누를 때마다 시트가 다시 열리는 것처럼 보이던 문제 */
body.same-pop .sheet, body.same-pop .calbox, body.same-pop .modal, body.same-pop .overlay{animation:none}

/* ---- 상단바: 맨 왼쪽 버튼을 없애고 매장 이름이 그 일을 합니다 ---- */
.storename{gap:var(--s8)}
.storename svg{width:18px; height:18px; stroke:currentColor; fill:none; stroke-width:1.7; flex:none; opacity:.8}
.storename .sn-ic{font-size:var(--fs-body); opacity:.8}
/* 날짜 화살표는 마우스가 그 줄에 갔을 때만 — 손가락 기기(hover 없음)에서는 늘 보입니다. 안 보이면 못 누르니까 */
@media (hover:hover) and (pointer:fine){
  .bnav{opacity:0; transition:opacity .15s}
  .bar-mid:hover .bnav, .bnav:focus-visible{opacity:.7}
  .bar-mid:hover .bnav.mo{opacity:.55}
  .bar-mid:hover .bnav:hover{opacity:1}
}
/* 더보기(⋮) 메뉴 — 예약률 추이 · 설정 · 디스플레이 모드 */
.more-wrap{position:relative; flex:none}
.more-menu{position:absolute; right:0; top:calc(100% + 6px); z-index:40; min-width:190px; padding:var(--s4);
  background:var(--surface); border:1px solid var(--border); border-radius:var(--r-md);
  box-shadow:0 8px 24px rgba(20,20,18,.18); display:flex; flex-direction:column; animation:modal-in .15s ease-out}
.more-menu button{display:flex; align-items:center; gap:var(--s12); width:100%; min-height:44px; border:none; background:none;
  text-align:left; padding:var(--s8) var(--s12); font-size:var(--fs-body); font-weight:600; color:var(--text); border-radius:var(--r-sm); white-space:nowrap}
.more-menu button:hover{background:var(--surface-2)}
.more-menu button:active{filter:brightness(.9)}
.more-menu svg{width:19px; height:19px; stroke:currentColor; fill:none; stroke-width:1.7; flex:none; color:var(--text-2)}
/* 메뉴 바깥을 누르면 닫히게 하는 투명 막. 상단바(z30) 안에 있으므로 본문 전체를 덮습니다 */
.more-veil{position:fixed; top:0; left:0; right:0; bottom:0; z-index:29}
@media (max-width:900px){ .more-wrap{order:6} }

/* ---- 대시보드 지표줄: 타임라인 아래로 내리고 칸을 낮춥니다 (전엔 너무 두꺼운 네모) ---- */
.metric{padding:var(--s8) var(--s12)}
.metric .v{font-size:var(--fs-head); line-height:24px; letter-spacing:-.02em}
.metric .u{font-size:var(--fs-sub)}
.metric .k{margin-top:0; font-size:var(--fs-label); line-height:18px}
.metric .s{font-size:var(--fs-label); line-height:18px}
'''
rep('''.panel.soon:hover .bg{transform:scale(1.03)}


/* ============================================================
   12. 구형 브라우저 폴백''',
'''.panel.soon:hover .bg{transform:scale(1.03)}
''' + BLOCK + '''

/* ============================================================
   12. 구형 브라우저 폴백''')

io.open(SRC, "w", encoding="utf-8", newline="\n").write(s)
print("CSS 패치 완료")
