"""Phase 4-1 대시보드 — 구역 파일을 고칩니다 (한 번만 실행).
 · 지표 칸 위계: 숫자 > 이름(.k) > 보조(.s). 지금은 이름이 연한 회색(text-3)이고 보조가 더 진해서 거꾸로 읽혔습니다
 · 카드 사이 16px, 태블릿 이상에서는 카드 안쪽 24px — '여백이 정보' (문서 2장)
 · 타임라인 상단 묶음 사이 12px
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

set_in_block("5.css", ".metric .k", "color", "var(--text-2)")
set_in_block("5.css", ".metric .k", "font-weight", "700")
set_in_block("5.css", ".metric .k", "margin-top", "var(--s4)")
set_in_block("5.css", ".metric .s", "color", "var(--text-3)")
set_in_block("5.css", ".tl-top", "gap", "var(--s12)")
set_in_block("3.css", ".card + .card", "margin-top", "var(--s16)")
set_in_block("3.css", ".fold + .fold", "margin-top", "var(--s16)")
s = load("11.css")
block = """
/* ---- Phase 4-1 대시보드: 태블릿 이상에서는 카드 안쪽을 24px 로 넓힙니다 ('여백이 정보'). 폰은 16px 그대로 ---- */
@media (min-width:768px){
  .card-b{padding:var(--s24)}
  .metric{padding:var(--s24) var(--s24)}
  .fold-h{padding:var(--s16) var(--s24)}
  .fold-b{padding:0 var(--s24) var(--s24)}
  .dash{gap:var(--s16)}
}
"""
s = s.rstrip("\n") + "\n" + block
save("11.css", s); print("ok 11.css 대시보드 여백 블록 추가")
