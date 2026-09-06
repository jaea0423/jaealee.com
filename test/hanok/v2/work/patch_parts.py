"""Phase 3-2 입력·카드·태그 통일 + 실선 줄이기 — 구역 파일을 고칩니다 (한 번만 실행).
 · 입력창(input/select) 최소 높이 44px, 반경 --r-sm 로 버튼과 같은 모서리
 · 카드·시트·타일류 반경 --r-md(10px), 시트·확인창·완료 상자는 --r-lg(16px)
 · 태그(.tag)와 알약(.pill)은 같은 크기·굵기·반경 — 뜻(색)만 다르게
 · 접기 카드 몸통·소제목·범례·분 조절·구역 묶음의 구분선을 여백으로 대체 (선 대신 여백으로 위계)
"""
import os, re
Z = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zones")

def load(fn): return open(os.path.join(Z, fn), encoding="utf-8").read()
def save(fn, s): open(os.path.join(Z, fn), "w", encoding="utf-8").write(s)

def set_in_block(fn, sel, prop, value):
    """fn 안의 '<sel>{' 블록에서 prop 값을 바꾸거나(없으면 덧붙임)"""
    s = load(fn); i = s.index(sel + "{"); j = s.index("}", i); body = s[i + len(sel) + 1:j]
    pat = re.compile(r"(^|;\s*)" + re.escape(prop) + r"\s*:[^;]*")
    if pat.search(body): body = pat.sub(lambda m: m.group(1) + f"{prop}:{value}", body, count=1)
    else: body = body.rstrip().rstrip(";") + f"; {prop}:{value}"
    save(fn, s[:i + len(sel) + 1] + body + s[j:]); print("ok", fn, sel, prop, "=", value)

def drop_in_block(fn, sel, prop):
    s = load(fn); i = s.index(sel + "{"); j = s.index("}", i); body = s[i + len(sel) + 1:j]
    body2 = re.sub(r"(^|;)\s*" + re.escape(prop) + r"\s*:[^;]*;?", lambda m: ";" if m.group(1) == ";" else "", body, count=1)
    body2 = re.sub(r";\s*;", ";", body2).strip("; ")
    save(fn, s[:i + len(sel) + 1] + body2 + s[j:]); print("ok", fn, sel, "-", prop)

# ---- 입력창 ----
set_in_block("2.css", "input, select, textarea", "border-radius", "var(--r-sm)")
s = load("2.css")
s = s.replace("input:focus, select:focus{", "/* 입력창도 손가락으로 누르므로 44px 이상 (textarea 는 여러 줄이라 제외) */\ninput, select{min-height:44px}\ninput:focus, select:focus{", 1)
save("2.css", s); print("ok 2.css input min-height")
set_in_block("3.css", ".f.big input", "border-radius", "var(--r-sm)")

# ---- 카드·타일: --r-md / 시트·확인창: --r-lg ----
for fn, sel in [("3.css", ".card"), ("5.css", ".hours-line"), ("6.css", ".calbox"), ("6.css", ".wz-cal"), ("6.css", ".wz-time"),
                ("6.css", ".wz-review"), ("6.css", ".mark-info"), ("6.css", ".seat-note"), ("6.css", ".sms-box"), ("6.css", ".smsprev"),
                ("6.css", ".chg-box"), ("6.css", ".blk-hits"), ("6.css", ".urlbox"), ("6.css", ".course-sum"), ("6.css", ".infant"),
                ("7.css", ".zone"), ("7.css", ".disprow"), ("7.css", ".dayrow"), ("7.css", ".zmap"), ("7.css", ".applybar"), ("7.css", ".logbox"),
                ("6.css", ".cday"), ("6.css", ".ptile"), ("6.css", ".scell"), ("6.css", ".srccell"), ("6.css", ".citem"), ("6.css", ".hcell")]:
    set_in_block(fn, sel, "border-radius", "var(--r-md)")
set_in_block("6.css", ".sheet", "border-radius", "var(--r-lg) var(--r-lg) 0 0")
set_in_block("6.css", ".modal", "border-radius", "var(--r-lg)")
set_in_block("6.css", ".done-box", "border-radius", "var(--r-lg)")
s = load("11.css"); s = s.replace("  .sheet{border-radius:var(--r-sm)}", "  .sheet{border-radius:var(--r-lg)}", 1); save("11.css", s); print("ok 11.css .sheet @768 → --r-lg")

# ---- 태그 · 알약: 같은 크기·굵기·반경 ----
for sel in (".tag", ".pill"):
    set_in_block("3.css", sel, "font-size", "var(--fs-sub)")
    set_in_block("3.css", sel, "font-weight", "600")
    set_in_block("3.css", sel, "padding", "var(--s4) var(--s8)")
    set_in_block("3.css", sel, "border-radius", "var(--r-sm)")
set_in_block("3.css", ".chg-tag", "font-size", "var(--fs-sub)")
set_in_block("3.css", ".chg-tag", "font-weight", "700")
set_in_block("3.css", ".chg-tag", "border-radius", "var(--r-sm)")

# ---- 실선 → 여백 ----
drop_in_block("3.css", ".fold-b", "border-top");      set_in_block("3.css", ".fold-b", "padding-top", "0")
drop_in_block("3.css", ".subhead", "border-bottom");  drop_in_block("3.css", ".subhead", "padding-bottom")
drop_in_block("5.css", ".tl-legends", "border-top");  set_in_block("5.css", ".tl-legends", "padding-top", "var(--s4)")
drop_in_block("6.css", ".mwrap", "border-top")
drop_in_block("7.css", ".z-join", "border-top")
drop_in_block("7.css", ".zm-legend", "border-top")
print("done")
