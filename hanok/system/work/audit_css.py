# -*- coding: utf-8 -*-
"""v7 CSS 정적 검사 — 규칙(selector{...})마다 클래스 토큰을 뽑아, JS·page.html 어디에도 안 나오는 클래스가 든 규칙을 찾습니다.
   그런 규칙은 어떤 요소에도 못 붙으니 죽은 규칙입니다. (동적 이름 s-확정 · k-warn 은 접두어로 따로 봅니다)
   그리고 같은 셀렉터가 몇 번 정의됐는지도 셉니다."""
import io, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L

js = "\n".join(L.load(n) for n in L.parts("js")) + L.load("page.html")
css_parts = L.parts("css")

def strip(s): return re.sub(r"/\*[\s\S]*?\*/", "", s)

def rules(css):
    """(selector, body) 목록 — @media 안은 펼쳐서, @font-face·@keyframes·@supports 는 건너뜀"""
    out = []
    depth = 0; i = 0; n = len(css); buf = ""
    stack = []
    while i < n:
        c = css[i]
        if c == "{":
            head = buf.strip(); buf = ""
            stack.append(head); i += 1
            if head.startswith("@") and not head.startswith("@media") and not head.startswith("@supports"):
                # 통째 건너뜀
                d = 1
                while i < n and d:
                    if css[i] == "{": d += 1
                    elif css[i] == "}": d -= 1
                    i += 1
                stack.pop()
            continue
        if c == "}":
            head = stack.pop() if stack else ""
            if head and not head.startswith("@"):
                out.append((head, buf.strip(), [h for h in stack if h.startswith("@")]))
            buf = ""; i += 1; continue
        buf += c; i += 1
    return out

used_words = set(re.findall(r"[A-Za-z_][\w-]*", js))
# 동적으로 붙는 클래스 접두어 (코드에서 "s-"+status 처럼 만드는 것)
DYN_PREFIX = ("s-", "k-", "f", "c", "tv-", "theme-")

dead = []; counts = collections.Counter(); all_rules = 0
for name in css_parts:
    css = strip(L.load(name))
    for sel, body, ctx in rules(css):
        all_rules += 1
        for single in sel.split(","):
            counts[(single.strip(), tuple(ctx))] += 1
        classes = set(re.findall(r"\.([A-Za-z_][\w-]*)", sel))
        missing = [c for c in classes if c not in used_words and not (c.startswith(DYN_PREFIX) and len(c) <= 12)]
        ids = set(re.findall(r"#([A-Za-z_][\w-]*)", sel))
        missing += ["#" + i for i in ids if i not in used_words]
        if missing:
            dead.append((name, sel[:90], ctx, missing))

print("규칙 %d개" % all_rules)
print("\n== 어디에도 안 쓰는 클래스가 든 규칙 (%d) ==" % len(dead))
for name, sel, ctx, missing in dead:
    print("  %-18s %-70s %s  ← %s" % (name, sel, ("@" if ctx else ""), ", ".join(missing)))

multi = [(k, v) for k, v in counts.items() if v >= 3]
multi.sort(key=lambda x: -x[1])
print("\n== 같은 셀렉터 3번 이상 (같은 @media 조건 기준) (%d) ==" % len(multi))
for (sel, ctx), v in multi[:60]:
    print("  %2d  %-60s %s" % (v, sel, " ".join(ctx)[:50]))
