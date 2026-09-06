"""Phase 4-2 예약·마법사 — 구역 파일을 고칩니다 (한 번만 실행).
 · 시트 제목은 큰 제목 단(--fs-head 20px) — 지금은 본문 제목(17px)과 같아 눈에 안 띔
 · 안내 상자(마법사 '현재 설정', 코스 요약, 예약 처리 상단 정보, 영업시간 줄)는 테두리 대신 옅은 바탕(surface-2) — 선 줄이기
 · 시트 안 입력 묶음(.f) 사이 12→16px, 시트 머리 아래 16→24px — 손가락으로 고를 때 붙어 보이지 않게
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

set_in_block("6.css", ".sheet-h h2", "font-size", "var(--fs-head)")
set_in_block("6.css", ".sheet-h", "margin-bottom", "var(--s24)")
set_in_block("3.css", ".f", "margin-bottom", "var(--s16)")
for fn, sel in (("6.css", ".seat-note"), ("6.css", ".course-sum"), ("6.css", ".mark-info"), ("5.css", ".hours-line")):
    set_in_block(fn, sel, "border", "none")
    set_in_block(fn, sel, "background", "var(--surface-2)")
set_in_block("6.css", ".md-h", "font-size", "var(--fs-head)")
print("done")
