"""v3 4차 — 디자인 개편 (apple.com/kr 기준, apple-design 규칙 준수).
   1) 팔레트: 따뜻한 회색 → 애플 중성 회색 (#F5F5F7 / #1D1D1F / #6E6E73). 하루 종일 켜 두는 화면이라 순백·먹색 대비를 한 단 낮춤
   2) 상단바: 먹색 띠 → 밝은 바탕 (apple.com 내비 rgba(250,250,252,.8) — blur 는 구형 TV 금지라 불투명도만 높임)
   3) 모서리: 버튼·칩은 알약(980px), 타일 12px, 카드·시트 18px
   4) 카드: 테두리·그림자 없이 흰 면 하나 (회색 바탕 위 흰 카드 — apple.com 의 회색/흰 교차 구성)
   5) 고른 타일은 살짝 떠 보이게 (그림자) — '선택됐다'가 색만이 아니라 깊이로도 읽히게
   6) 타이포: 큰 제목 -0.02em, 숫자 -0.03em, 라벨 +0.04em (크기별 자간 — apple-design §15)
   손님용 화면(.tv)은 팔레트 변수를 쓰지 않으므로 영향 없음 (확인함)"""
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

# ---------- 토큰: 모서리 계단 ----------
rep('''  --r-sm:6px;  --r-md:10px;  --r-lg:16px;
  --r:10px;''',
'''  --r-sm:8px;  --r-md:12px;  --r-lg:18px;   /* v3: 8/12/18 (apple.com 의 12/18/28 을 관리 화면 크기에 맞춰 한 단 줄임) */
  --r:12px;''')

# ---------- 팔레트 ----------
rep('''body.theme-hanok{
  --bg:#F3F2EF;            /* 바탕 — 따뜻한 회색 */
  --surface:#FFFFFF;       /* 카드는 흰색 — 바탕과 대비를 만들어 정보가 또렷해짐 */
  --surface-2:#F7F6F3;     /* 카드 안쪽 구역 */
  --border:#E4E2DD;
  --border-strong:#C9C6BF;
  --text:#1C1B19;          /* 먹 */
  --text-2:#5B5954;
  --text-3:#8A8781;
  --pine:#1C1B19;          /* 주요 동작 = 먹색 (이름은 청록 시절 것) */
  --pine-soft:#EDECE8;
  --amber:#8A6512;         /* 주의 */
  --amber-soft:#F8F1DE;
  --rust:#A63B26;          /* 경고 — 벽돌 */
  --rust-soft:#FAE9E4;
  --shadow:0 1px 0 rgba(23,22,20,.04);
  --topbar-bg:#1C1B19;     /* 상단바는 먹색 바탕 + 밝은 글자 */
  --topbar-fg:#F4F3F0;
  --topbar-line:#000;
  --topbar-btn-line:rgba(244,243,240,.26);
  --topbar-hover:rgba(244,243,240,.12);''',
'''body.theme-hanok{
  /* v3 디자인 개편 — apple.com/kr 의 중성 회색. 이전(따뜻한 회색 #F3F2EF/#1C1B19)은 work/patch_v3d.py 에 남아 있습니다 */
  --bg:#F5F5F7;            /* 바탕 — 애플 회색. 흰 카드가 이 위에 놓입니다 */
  --surface:#FFFFFF;       /* 카드 */
  --surface-2:#F5F5F7;     /* 카드 안쪽 구역 = 바탕색 (한 단계만 씁니다) */
  --border:#E5E5EA;        /* 실선 — 거의 안 보이는 굵기 */
  --border-strong:#D2D2D7;
  --text:#1D1D1F;
  --text-2:#6E6E73;        /* 흰 바탕 대비 4.9:1 */
  --text-3:#808085;        /* 라벨 전용 (본문에 쓰지 않음) */
  --pine:#1D1D1F;          /* 주요 동작 = 검정 (이름은 청록 시절 것) */
  --pine-soft:#EDEDF0;
  --amber:#8A6512;         /* 주의 */
  --amber-soft:#FBF3DF;
  --rust:#A63B26;          /* 경고 — 벽돌. 회색 팔레트에서 유일한 '색'이라 더 잘 띕니다 */
  --rust-soft:#FAE9E4;
  --shadow:none;
  --topbar-bg:rgba(250,250,252,.94);   /* 상단바 — 밝은 바탕 (apple.com 내비). 검은 띠는 하루 종일 보기에 무거웠습니다 */
  --topbar-fg:#1D1D1F;
  --topbar-line:rgba(0,0,0,.08);
  --topbar-btn-line:rgba(0,0,0,.16);
  --topbar-hover:rgba(0,0,0,.05);''')
rep('''body.theme-hanok .topbar{box-shadow:none; border-bottom:1px solid #000}''',
    '''body.theme-hanok .topbar{box-shadow:none; border-bottom:1px solid var(--topbar-line)}''')

# ---------- 상단바의 '예약 등록' — 밝은 바탕이 됐으니 검정 채움 ----------
rep('''.topbar .tvbtn.accent{border-color:transparent; opacity:1; background:#F4F2EE; color:#1B1A18; font-weight:700}
.topbar .tvbtn.accent:hover{background:#fff}''',
'''.topbar .tvbtn.accent{border-color:transparent; opacity:1; background:var(--text); color:#fff; font-weight:700}
.topbar .tvbtn.accent:hover{background:#2C2C2E}''')
rep('''.topbar .bdate:hover{border-color:rgba(243,234,218,.28)}''', '''.topbar .bdate:hover{border-color:var(--topbar-btn-line)}''')

BLOCK = r'''
/* ============================================================
   v3 디자인 개편 — apple.com/kr 을 기준으로 (2026-09-07)
   색은 9구역 팔레트에서, 모서리 계단은 1구역 토큰에서 바꿨고 여기에는 '구성' 규칙만 둡니다.
   원칙: 면은 회색 바탕 + 흰 카드 두 단계뿐, 선은 거의 안 보이게, 누르는 것은 알약, 고른 것은 살짝 떠 보이게.
   ============================================================ */
/* ---- 알약 — 누르는 것 전부. 타일(면이 넓은 것)은 12px 그대로 ---- */
.btn, .btn.sm, .btn.lg, .tvbtn, .topbar .tvbtn, .topbar .home, .bdate, .btoday, .wz-back,
.seg button, .filters button, .nonebtn, .nonebtn.sm, .mfine button, .pmore, .undecided, .wbtn,
.tag, .pill, .wz-sum span, .avail, .scell .avail{border-radius:980px}
.btn.lg{padding:var(--s16) var(--s32)}
.btn.primary{box-shadow:0 1px 2px rgba(0,0,0,.12)}
/* ---- 상단바: 44px 내비 느낌으로 얇게. 버튼은 36px 그대로(손가락) ---- */
.topbar-in{padding:var(--s8) var(--s24)}
.storename svg{opacity:1}
.more-menu{border:none; box-shadow:0 12px 40px rgba(0,0,0,.16); border-radius:var(--r-md); padding:var(--s8)}
/* ---- 카드: 테두리·그림자 없이 흰 면 하나 ---- */
.card{border:none; box-shadow:none; border-radius:var(--r-lg)}
.card + .card{margin-top:var(--s16)}
.fold-h:hover{background:transparent}
/* 지표 칸은 카드 없이 회색 바탕 위에 흰 칸 다섯 개 — apple.com 의 회색 바탕 + 흰 상자 구성 */
.metrics-card{background:transparent; border-radius:0}
.metrics{gap:var(--s8); background:transparent}
.metric{border-radius:var(--r-md); padding:var(--s12) var(--s16)}
button.metric:hover{background:#FAFAFC}
.metric .v{letter-spacing:-.03em}
.metric .k{letter-spacing:.04em}
/* ---- 타일: 선은 실선 한 겹, 고르면 검정 + 살짝 떠 보이게 ---- */
.srccell, .ptile, .scell, .hcell, .citem, button.bday, .pmore, .bigstep button, .mfine button, .mo-h .nav,
.wbtn, .dcell, .zm-t, .pkey, .pdot, .wz-back, .btn, .seg button, .filters button, .nonebtn, .ordbtns button,
.res-head .nav, .datenav .nav{border-color:var(--border)}
.scell.busy{border-style:solid; background:var(--surface-2); opacity:.75}
.hcell.gone{opacity:.4}
.srccell.on, .ptile.on, .scell.on, .hcell.on, .citem.on, button.bday.sel{box-shadow:0 6px 16px rgba(0,0,0,.16)}
.ptile .pn, .bigstep .v, .tl-kpi b, .hcell .hh{letter-spacing:-.03em}
.lbl, .wz-eyebrow, .subhead, .metric .k, .hcell .ap{letter-spacing:.04em}
/* ---- 마법사: 질문은 더 크게·더 조여서 (큰 글자는 자간을 음수로 — 크기별 자간) ---- */
.wz-q h2{letter-spacing:-.02em; line-height:1.3}
@media (min-width:768px){ .wz-q h2{font-size:32px; letter-spacing:-.025em} }
.wz-top, .wz-foot{border-color:var(--border)}
.wz-sum span{background:var(--surface-2); border-color:transparent; color:var(--text-2)}
.wz-dot .n{background:var(--border-strong); color:#fff}
.hours-line, .seat-note, .course-sum, .infant{background:var(--surface-2); border:none}
/* ---- 입력 ---- */
input, select, textarea{border-color:var(--border-strong); border-radius:var(--r-sm)}
.f.big input{border-radius:var(--r-md)}
/* ---- 시트·확인창: 크고 부드러운 그림자로 '떠 있는 재질'을 (blur 는 구형 TV 금지) ---- */
.sheet{box-shadow:0 24px 64px rgba(0,0,0,.22)}
.modal{box-shadow:0 24px 64px rgba(0,0,0,.24); border-radius:var(--r-lg)}
.calbox{border-radius:var(--r-lg); box-shadow:0 24px 64px rgba(0,0,0,.22)}
.overlay{background:rgba(0,0,0,.4)}
.done-box{border:none; box-shadow:0 12px 40px rgba(0,0,0,.08)}
/* ---- 타임라인: 블록은 애플 진회색, 지난 것은 밝은 회색 ---- */
.tl-track{background:#FAFAFC; border-color:var(--border)}
.blk, .lgsw.ok{background:#2C2C2E}
.blk.past{background:#C7C7CC}
.blk.past.tent{background:#D1D1D6}
'''
rep('''/* ============================================================
   12. 구형 브라우저 폴백''', BLOCK + '''
/* ============================================================
   12. 구형 브라우저 폴백''')

io.open(SRC, "w", encoding="utf-8", newline="\n").write(s)
print("4차 패치 완료:", n_ok, "곳")
