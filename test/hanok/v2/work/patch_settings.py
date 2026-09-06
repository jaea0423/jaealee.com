"""Phase 4-3 설정 — 구역 파일을 고칩니다 (한 번만 실행).
 · 좌석 순서 ▲▼ 버튼(.ordbtns button)에 CSS 가 아예 없어 브라우저 기본 버튼(28px 짜리)으로 나오고 있었습니다 → 44px 버튼으로
 · 좌석·정원 설정 줄(.tset) 위아래 여백 8→12px
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

set_in_block("7.css", ".tset", "padding", "var(--s12) 0")
s = load("7.css")
block = """
/* ---------- 좌석 배정 순서 줄의 ▲▼ 버튼 (설정 → 좌석) ----------
   Phase 4-3 전까지 이 버튼에는 CSS 가 없어 브라우저 기본 버튼(28px)으로 나왔습니다. 손가락으로 누르므로 44px. */
.ordbtns{display:inline-flex; gap:var(--s4); flex:none}
.ordbtns button{min-width:44px; min-height:44px; border:1px solid var(--border-strong); background:var(--surface);
  border-radius:var(--r-sm); font-size:var(--fs-sub); color:var(--text-2); cursor:pointer; -webkit-tap-highlight-color:transparent}
.ordbtns button:active{filter:brightness(.9)}
.ordbtns button:disabled{opacity:.3; cursor:default}
.ordnum{width:24px; text-align:center; font-weight:700; color:var(--text-3); flex:none}
"""
s = s.replace("/* ---------- 좌석·정원 설정 줄 (.tset)", block.strip("\n") + "\n\n/* ---------- 좌석·정원 설정 줄 (.tset)", 1)
save("7.css", s); print("ok 7.css ordbtns 추가")
