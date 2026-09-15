# -*- coding: utf-8 -*-
"""v7 정리 2 — audit_css 가 찾은 '어디에도 안 쓰는 클래스가 든 셀렉터' 를 지웁니다.
   · 셀렉터 목록(a, b, c{...}) 중 일부만 죽었으면 그 셀렉터만 뺍니다
   · 전부 죽었으면 규칙째 지우고, 바로 위 줄이 그 규칙만을 위한 한 줄 주석이면 같이 지웁니다
   · 비게 된 @media 블록은 지웁니다
   KEEP 은 동적으로 붙거나(b1~b7) 자리만 남긴 것(tvx-legacy), 흉내 표시(sb-mock·lk-open)"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L

KEEP = set(["b1","b2","b3","b4","b5","b6","b7","tvx-legacy","sb-mock","lk-open","mockbar"])
DYN_PREFIX = ("s-", "k-", "f", "c", "tv-", "theme-")
js = "\n".join(L.load(n) for n in L.parts("js")) + L.load("page.html")
used = set(re.findall(r"[A-Za-z_][\w-]*", js)) | KEEP

def dead_selector(sel):
    classes = set(re.findall(r"\.([A-Za-z_][\w-]*)", sel))
    ids = set(re.findall(r"#([A-Za-z_][\w-]*)", sel))
    for c in classes:
        if c in used: continue
        if c.startswith(DYN_PREFIX) and len(c) <= 12: continue
        return True
    for i in ids:
        if i not in used: return True
    return False

def scan(css):
    """규칙 위치 목록: (sel_start, brace_pos, end_pos_after_close, selector_text, is_at) — 주석·문자열 건너뜀. @media 안도 평면으로"""
    out = []; i = 0; n = len(css); sel_start = None; depth_stack = []
    while i < n:
        c = css[i]
        if css.startswith("/*", i):
            j = css.index("*/", i) + 2
            if sel_start is None or css[sel_start:i].strip() == "": sel_start = None
            i = j; continue
        if c in "\"'":
            j = i + 1
            while j < n and css[j] != c:
                if css[j] == "\\": j += 1
                j += 1
            i = j + 1; continue
        if c == "{":
            head = css[sel_start:i] if sel_start is not None else ""
            hs = sel_start if sel_start is not None else i
            # 실제 셀렉터 시작: 앞 공백·개행 제외
            m = re.match(r"\s*", head); hs2 = hs + m.end()
            depth_stack.append((hs2, i, head.strip()))
            sel_start = None; i += 1; continue
        if c == "}":
            hs2, bp, head = depth_stack.pop()
            if not head.startswith("@"):
                out.append((hs2, bp, i + 1, head))
            i += 1; sel_start = None; continue
        if sel_start is None and not c.isspace(): sel_start = i
        i += 1
    return out

total_removed = 0; total_trim = 0
for name in L.parts("css"):
    css = L.load(name)
    rules = scan(css)
    edits = []   # (start, end, replacement)
    for hs, bp, ep, head in rules:
        sels = [x.strip() for x in head.split(",")]
        alive = [x for x in sels if not dead_selector(x)]
        if len(alive) == len(sels): continue
        if not alive:
            # 규칙째 삭제. 줄 시작~줄 끝까지 확장
            a = css.rfind("\n", 0, hs) + 1
            b = css.find("\n", ep); b = n if b < 0 else b + 1
            if css[a:hs].strip() != "" or css[ep:b].strip() != "":
                # 같은 줄에 다른 것이 있으면 규칙만
                edits.append((hs, ep, "")); total_removed += 1; continue
            # 바로 위 한 줄 주석
            pa = css.rfind("\n", 0, a - 1) + 1
            prev = css[pa:a]
            if re.match(r"^\s*/\*.*\*/\s*$", prev) and prev.count("/*") == 1:
                a = pa
            edits.append((a, b, "")); total_removed += 1
        else:
            edits.append((hs, bp, ", ".join(alive))); total_trim += 1
    n = len(css)
    for a, b, rep in sorted(edits, key=lambda e: -e[0]):
        css = css[:a] + rep + css[b:]
    # 빈 @media / @supports 블록
    css = re.sub(r"(?m)^@(media|supports)[^{]*\{\s*\}\n?", "", css)
    css = re.sub(r"\n{3,}", "\n\n", css)
    L.save(name, css)
print("규칙 삭제 %d · 셀렉터 일부 제거 %d" % (total_removed, total_trim))
