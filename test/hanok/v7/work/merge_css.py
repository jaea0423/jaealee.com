# -*- coding: utf-8 -*-
"""v7 정리 3 — 같은 셀렉터가 뒤에서 다시 정의(덮어쓰기)된 것을 **결과가 같을 때만** 앞 규칙에 합칩니다.

  합치는 조건(보수적): 앞 규칙 R1 과 뒤 규칙 R2 가 같은 셀렉터·같은 @media 조건이고,
  둘 사이에 있는 어떤 규칙도 R2 가 정하는 속성을 건드리지 않을 때.
  → 그러면 R2 의 값을 R1 에 옮겨 적고 R2 를 지워도 어떤 요소에도 결과가 달라지지 않습니다.
  (사이 규칙이 같은 속성을 쓰면 우선순위가 바뀔 수 있으니 그대로 둡니다)

  R2 바로 위 한 줄 주석은 R1 뒤에 옮겨 붙입니다('왜'가 사라지지 않게)."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L

def scan(css):
    """규칙 목록: dict(hs, bp, ep, sel, ctx(tuple), body) — 주석·문자열 건너뜀, @media/@supports 는 ctx 로. @font-face·@keyframes 안은 무시"""
    out = []; i = 0; n = len(css); sel_start = None; stack = []
    while i < n:
        c = css[i]
        if css.startswith("/*", i):
            j = css.index("*/", i) + 2
            if sel_start is not None and css[sel_start:i].strip() == "": sel_start = None
            i = j; continue
        if c in "\"'":
            j = i + 1
            while j < n and css[j] != c:
                if css[j] == "\\": j += 1
                j += 1
            i = j + 1; continue
        if c == "{":
            head = css[sel_start:i] if sel_start is not None else ""
            hs = (sel_start if sel_start is not None else i)
            hs += len(head) - len(head.lstrip())
            stack.append([hs, i, head.strip()])
            sel_start = None; i += 1; continue
        if c == "}":
            hs, bp, head = stack.pop()
            if head.startswith("@media") or head.startswith("@supports"):
                pass
            elif head.startswith("@"):
                pass   # font-face, keyframes
            else:
                ctx = tuple(h[2] for h in stack if h[2].startswith("@media") or h[2].startswith("@supports"))
                inside_at = any(h[2].startswith("@") and not (h[2].startswith("@media") or h[2].startswith("@supports")) for h in stack)
                if not inside_at:
                    out.append(dict(hs=hs, bp=bp, ep=i + 1, sel=head, ctx=ctx, body=css[bp + 1:i]))
            i += 1; sel_start = None; continue
        if sel_start is None and not c.isspace(): sel_start = i
        i += 1
    return out

def decls(body):
    """본문 → [(prop, value)] (주석 제거, 괄호 안 ; 무시)"""
    body = re.sub(r"/\*[\s\S]*?\*/", "", body)
    out = []; depth = 0; cur = ""
    for ch in body:
        if ch in "([": depth += 1
        elif ch in ")]": depth -= 1
        if ch == ";" and depth == 0:
            out.append(cur); cur = ""
        else: cur += ch
    if cur.strip(): out.append(cur)
    res = []
    for d in out:
        if ":" not in d: continue
        p, v = d.split(":", 1)
        res.append((p.strip().lower(), v.strip()))
    return res

def norm_sel(s): return re.sub(r"\s+", " ", s.strip())

FAMILY = ["border", "margin", "padding", "background", "grid-template", "grid-auto", "overflow", "transition", "animation", "text-decoration", "list-style", "outline", "columns", "gap"]
def related(p, q):
    """두 속성이 같은 요소에서 서로 덮어쓸 수 있는가 — 같은 이름, 축약형↔개별형(padding↔padding-top), font↔line-height, all"""
    if p == q or p == "all" or q == "all": return True
    if q.startswith(p + "-") or p.startswith(q + "-"): return True
    if {p, q} <= {"font", "line-height", "font-size", "font-weight", "font-family", "font-style"} and "font" in (p, q): return True
    for f in FAMILY:
        if p.startswith(f) and q.startswith(f): return True
    return False

# ---- 셀렉터 둘이 같은 요소에 붙을 수 있는지 — JS 의 class="..." 문자열에서 같이 나오는 클래스 조합으로 봅니다 ----
JS = "\n".join(L.load(n) for n in L.parts("js")) + L.load("page.html")
ATTRS = []
for m in re.finditer(r'class=(?:"([^"]*)"|\'([^\']*)\')', JS):
    v = m.group(1) if m.group(1) is not None else m.group(2)
    dyn = "${" in v
    toks = set(re.findall(r"[A-Za-z_][\w-]*", re.sub(r"\$\{[^}]*\}", " ", v)))
    ATTRS.append((toks, dyn))
def last_classes(sel):
    """셀렉터 마지막 복합 선택자의 클래스들. 요소만이거나 * 면 None(뭐든 될 수 있음)"""
    sel = re.sub(r"::?[a-zA-Z-]+(\([^)]*\))?", "", sel)      # 가상 요소/클래스 제거
    sel = re.sub(r"\[[^\]]*\]", "", sel)
    last = re.split(r"[\s>+~]+", sel.strip())[-1]
    cls = set(re.findall(r"\.([A-Za-z_][\w-]*)", last))
    return cls if cls else None
def compatible(s1, s2):
    a, b = last_classes(s1), last_classes(s2)
    if a is None or b is None: return True
    if a & b: return True
    for toks, dyn in ATTRS:
        ha, hb = bool(a & toks), bool(b & toks)
        if (ha and hb) or (dyn and (ha or hb)): return True
    return False

parts = L.parts("css")
texts = {n: L.load(n) for n in parts}
rules = []
for n in parts:
    for r in scan(texts[n]):
        r["part"] = n; r["sels"] = tuple(norm_sel(x) for x in r["sel"].split(","))
        r["props"] = decls(r["body"]); r["deleted"] = False; r["changed"] = False
        rules.append(r)

merged = 0
for idx, r2 in enumerate(rules):
    if r2["deleted"] or len(r2["sels"]) != 1: continue   # 여러 셀렉터가 묶인 규칙은 건드리지 않음
    props2 = dict(r2["props"])
    if not props2: continue
    # 가장 가까운 앞 규칙(같은 셀렉터 하나짜리·같은 ctx)
    r1 = None
    for k in range(idx - 1, -1, -1):
        c = rules[k]
        if c["deleted"]: continue
        if c["sels"] == r2["sels"] and c["ctx"] == r2["ctx"]:
            r1 = (k, c); break
    if not r1: continue
    k1, R1 = r1
    if "/*" in R1["body"] or "/*" in r2["body"]: continue   # 본문 안 주석('왜')이 있는 규칙은 다시 쓰지 않습니다
    # 사이 규칙이 R2 의 속성을 건드리는지
    touched = False
    for m in range(k1 + 1, idx):
        c = rules[m]
        if c["deleted"]: continue
        if not any(compatible(s, r2["sels"][0]) for s in c["sels"]): continue   # 같은 요소에 못 붙는 규칙은 상관없음
        for p, _ in c["props"]:
            if any(related(p, q) for q in props2): touched = True; break
        if touched: break
    if touched: continue
    # 합치기: R1 의 선언에서 같은 속성은 값 교체, 없는 것은 뒤에 추가
    new = []; seen = set()
    for p, v in R1["props"]:
        if p in props2: new.append((p, props2[p])); seen.add(p)
        else: new.append((p, v))
    for p, v in r2["props"]:
        if p not in seen and p not in dict(new): new.append((p, v))
    R1["props"] = new; R1["changed"] = True
    R1.setdefault("notes", []).append(r2)
    r2["deleted"] = True; merged += 1

# 되쓰기 — 조각마다 뒤에서 앞으로
for n in parts:
    css = texts[n]
    edits = []
    for r in rules:
        if r["part"] != n: continue
        if r["deleted"]:
            a = css.rfind("\n", 0, r["hs"]) + 1
            b = css.find("\n", r["ep"]); b = len(css) if b < 0 else b + 1
            line_only = css[a:r["hs"]].strip() == "" and css[r["ep"]:b].strip() == ""
            if line_only:
                pa = css.rfind("\n", 0, a - 1) + 1
                prev = css[pa:a]
                if re.match(r"^\s*/\*.*\*/\s*$", prev) and prev.count("/*") == 1: a = pa
                edits.append((a, b, ""))
            else:
                edits.append((r["hs"], r["ep"], ""))
        elif r["changed"]:
            multiline = "\n" in r["body"].strip()
            sep = "\n  " if multiline else " "
            body = ("; ".join("%s:%s" % (p, v) for p, v in r["props"]) if not multiline
                    else "\n  " + ";\n  ".join("%s:%s" % (p, v) for p, v in r["props"]) + "\n")
            # R2 들의 한 줄 주석을 뒤에 붙임
            notes = []
            for r2 in r.get("notes", []):
                t2 = texts[r2["part"]]
                a = t2.rfind("\n", 0, r2["hs"]) + 1
                pa = t2.rfind("\n", 0, a - 1) + 1
                prev = t2[pa:a].strip()
                if re.match(r"^/\*.*\*/$", prev) and prev.count("/*") == 1: notes.append(prev)
            tail = ("   " + " ".join(notes)) if notes else ""
            edits.append((r["bp"], r["ep"], "{" + body + "}" + tail))
    for a, b, rep in sorted(edits, key=lambda e: -e[0]):
        css = css[:a] + rep + css[b:]
    css = re.sub(r"(?m)^@(media|supports)[^{]*\{\s*\}\n?", "", css)
    css = re.sub(r"\n{3,}", "\n\n", css)
    L.save(n, css)
print("합친 규칙 %d" % merged)
