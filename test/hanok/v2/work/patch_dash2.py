"""Phase 6-1 대시보드 기준 화면 — 구역 파일을 고칩니다 (한 번만 실행).
 1) 강조 하나: 타임라인 상단은 '예약률 17%' 만 크게, 룸·홀은 보조 글로. 나머지 위계는 굵기 두 단(600·700)으로
 2) 세로 리듬: 버튼 줄높이 20px (12+20+12 = 44), 지표 숫자 줄높이 32px, 이름·보조 20px — 전부 4의 배수
 3) 굵기 800·900 → 700 (관리 화면), 상단바 아이콘 선 두께 1.7 로 통일
 4) 움직임 최소한: 시트 200ms 올라오기, 확인창 150ms 떠오르기, 접기 카드 몸통 150ms 나타나기.
    transform 은 translate 만 씁니다 (scale 은 배율 zoom 과 부딪힘). 움직임 줄이기 설정이면 전부 끕니다
 5) 빈 상태: 글자 한 줄이 아니라 옅은 바탕의 상자로
"""
import os, re
Z = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zones")
def load(fn): return open(os.path.join(Z, fn), encoding="utf-8").read()
def save(fn, s): open(os.path.join(Z, fn), "w", encoding="utf-8").write(s)
def set_in_block(fn, sel, prop, value):
    s = load(fn); i = s.index(sel + "{"); j = s.index("}", i); body = s[i + len(sel) + 1:j]
    pat = re.compile(r"(^|;\s*)" + re.escape(prop) + r"\s*:[^;]*")
    if pat.search(body): body = pat.sub(lambda m: m.group(1) + f"{prop}:{value}", body, count=1)
    else: body = body.rstrip().rstrip(";") + f"; {prop}:{value}"
    save(fn, s[:i + len(sel) + 1] + body + s[j:]); print("ok", fn, sel, prop, "=", value)

# 1) 타임라인 상단 위계
set_in_block("5.css", ".tl-kpi", "font-size", "var(--fs-sub)")
set_in_block("5.css", ".tl-kpi", "color", "var(--text-3)")
set_in_block("5.css", ".tl-kpi b", "font-size", "var(--fs-head)")
set_in_block("5.css", ".tl-kpi b", "line-height", "28px")
set_in_block("5.css", ".tl-kpi.sub b", "font-size", "var(--fs-body)")
set_in_block("5.css", ".tl-kpi.sub b", "font-weight", "600")
set_in_block("5.css", ".tl-kpi.sub b", "color", "var(--text-2)")
set_in_block("5.css", ".tl-kpis", "align-items", "baseline")

# 2) 세로 리듬
set_in_block("3.css", ".btn", "line-height", "20px")
set_in_block("5.css", ".metric .v", "line-height", "32px")
set_in_block("5.css", ".metric .k", "line-height", "20px")
set_in_block("5.css", ".metric .s", "line-height", "20px")
set_in_block("5.css", ".metric .s", "margin-top", "0")
set_in_block("3.css", ".fh-t", "line-height", "24px")

# 3) 굵기·아이콘
for fn in ("3.css", "4.css", "5.css", "6.css", "7.css", "8.css"):
    s = load(fn); n = len(re.findall(r"font-weight:(800|900)", s))
    s = re.sub(r"font-weight:(800|900)", "font-weight:700", s); save(fn, s); print("ok", fn, "굵기 800/900→700", n)
set_in_block("4.css", ".topbar .home svg", "stroke-width", "1.7")

# 4) 움직임 — 6구역(시트·확인창)과 3구역(접기 카드)에 덧붙임
s = load("6.css")
motion = """
/* ---------- 움직임 (Phase 6-1) — 딱 세 곳만 ----------
   시트는 아래에서 200ms 올라오고, 확인창은 150ms 떠오릅니다. '반응하는 도구' 느낌은 이 정도로 충분하고,
   전화 받으며 쓰는 화면이라 그 이상은 기다리게 만듭니다. transform 은 translate 만 (scale 은 배율 zoom 과 부딪혀 잘림) */
@keyframes sheet-in{from{transform:translateY(24px); opacity:0} to{transform:none; opacity:1}}
@keyframes modal-in{from{transform:translateY(8px); opacity:0} to{transform:none; opacity:1}}
@keyframes fade-in{from{opacity:0} to{opacity:1}}
.sheet, .calbox{animation:sheet-in .2s ease-out}
.modal{animation:modal-in .15s ease-out}
.overlay{animation:fade-in .15s ease-out}
"""
s = s.rstrip("\n") + "\n" + motion; save("6.css", s); print("ok 6.css 움직임")
set_in_block("3.css", ".fold-b", "animation", "fade-in .15s ease-out")

# 5) 빈 상태
set_in_block("3.css", ".empty", "background", "var(--surface-2)")
set_in_block("3.css", ".empty", "border-radius", "var(--r-md)")
set_in_block("3.css", ".empty", "padding", "var(--s32) var(--s16)")
set_in_block("3.css", ".empty", "font-size", "var(--fs-body)")
set_in_block("3.css", ".empty", "color", "var(--text-2)")

# 움직임 줄이기 설정 존중 — 11구역 끝에
s = load("11.css")
s = s.rstrip("\n") + """

/* 움직임 줄이기(접근성 설정)면 시트·확인창 애니메이션을 끕니다 */
@media (prefers-reduced-motion:reduce){
  .sheet, .calbox, .modal, .overlay, .fold-b{animation:none}
}
"""
save("11.css", s); print("ok 11.css reduced-motion")
print("done")
