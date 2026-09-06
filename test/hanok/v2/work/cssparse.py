"""CSS 파서 — src/index.html 의 <style> 블록(또는 .css 파일)을 규칙 목록으로 풀어냅니다.

출력: 규칙 하나마다 (순번, 시작줄, 컨텍스트(@media/@supports), 셀렉터, 선언들, 원본 위치)
목적: 셀렉터별로 몇 번 정의됐는지, 어느 컨텍스트에서, 최종값이 무엇인지 표를 만들기.
"""
import re, sys, json, collections

def read_css(path):
    s = open(path, encoding="utf-8").read()
    if "<style>" not in s:
        return s, 1
    a = s.index("<style>") + len("<style>")
    b = s.index("</style>")
    pre = s[:a]
    return s[a:b], pre.count("\n") + 1  # css text, line offset (1-based line of first css line)

def strip_comments(css):
    # 주석을 같은 길이의 공백으로 바꿔 줄 번호·위치를 유지
    out = []
    i = 0
    while i < len(css):
        j = css.find("/*", i)
        if j < 0:
            out.append(css[i:]); break
        out.append(css[i:j])
        k = css.find("*/", j + 2)
        if k < 0: k = len(css) - 2
        seg = css[j:k+2]
        out.append(re.sub(r"[^\n]", " ", seg))
        i = k + 2
    return "".join(out)

WS = " \t\r\n"

def parse(css, line_off):
    """중첩 @규칙을 재귀로 풀어냅니다. 반환: list of dict"""
    text = strip_comments(css)
    rules = []
    def line_of(pos):
        return text.count("\n", 0, pos) + line_off
    def parse_block(start, end, ctx):
        i = start
        dropped_next = False   # 짝 없는 } 뒤의 규칙 하나는 브라우저가 버립니다 ("} .tl-top" 이 셀렉터가 되어 무효)
        while i < end:
            m = re.compile(r"[{};]").search(text, i, end)
            if not m:
                break
            ch = m.group(0)
            head = text[i:m.start()].strip()
            if ch == ";":
                i = m.end(); continue
            if ch == "}":
                if head:
                    rules.append({"kind":"stray", "line":line_of(i), "text":head})
                rules.append({"kind":"stray_close", "line":line_of(m.start()), "pos":m.start()})
                dropped_next = True
                i = m.end(); continue
            depth = 1; j = m.end()
            while j < end and depth:
                c = text[j]
                if c == "{": depth += 1
                elif c == "}": depth -= 1
                j += 1
            body_start, body_end = m.end(), j - 1
            if head.startswith("@"):
                name = head.split("(")[0].split()[0]
                if name in ("@media", "@supports"):
                    parse_block(body_start, body_end, ctx + [head])
                else:
                    rules.append({"kind":"at", "line":line_of(i), "ctx":ctx, "sel":head,
                                  "body":text[body_start:body_end].strip()})
            else:
                decls = []
                for d in split_decls(text[body_start:body_end]):
                    d = d.strip()
                    if not d: continue
                    if ":" not in d:
                        decls.append((d, "", False)); continue
                    p, v = d.split(":", 1)
                    v = re.sub(r"\s+", " ", v.strip()); imp = False
                    if v.endswith("!important"):
                        imp = True; v = v[:-10].strip()
                    decls.append((p.strip().lower(), v, imp))
                hs = i
                while hs < m.start() and text[hs] in WS: hs += 1
                for sel in split_selectors(head):
                    rules.append({"kind":"rule", "line":line_of(hs), "ctx":ctx,
                                  "sel":sel, "group":head, "decls":decls,
                                  "start":hs, "end":j, "dropped":dropped_next})
                dropped_next = False
            i = j
    parse_block(0, len(text), [])
    return rules

def split_decls(body):
    """; 로 나누되 괄호·따옴표 안의 ; 는 무시 (url('data:...;base64,...') 때문)"""
    out=[]; depth=0; q=None; cur=""
    for c in body:
        if q:
            cur+=c
            if c==q: q=None
            continue
        if c in "'\"": q=c; cur+=c; continue
        if c=="(": depth+=1
        elif c==")": depth-=1
        if c==";" and depth==0:
            out.append(cur); cur=""
        else: cur+=c
    if cur.strip(): out.append(cur)
    return out

def split_selectors(head):
    # 괄호 안의 , 는 무시 (:not(a,b) 등)
    out=[]; depth=0; cur=""
    for c in head:
        if c in "([": depth+=1
        elif c in ")]": depth-=1
        if c=="," and depth==0:
            out.append(cur.strip()); cur=""
        else: cur+=c
    if cur.strip(): out.append(cur.strip())
    return [re.sub(r"\s+", " ", s) for s in out]

def specificity(sel):
    s = re.sub(r":not\(([^)]*)\)", r"\1", sel)  # :not 안쪽은 그대로 셈
    s = re.sub(r"::?[a-zA-Z-]+(\([^)]*\))?", lambda m: " PSEUDO_EL " if m.group(0).startswith("::") or m.group(0)[1:] in ("before","after","first-line","first-letter") else " PSEUDO ", s)
    ids = len(re.findall(r"#[\w-]+", s))
    cls = len(re.findall(r"\.[\w-]+", s)) + len(re.findall(r"\[[^\]]*\]", s)) + s.count(" PSEUDO ")
    s2 = re.sub(r"#[\w-]+|\.[\w-]+|\[[^\]]*\]| PSEUDO(_EL)? ", " ", s)
    tags = len(re.findall(r"(?<![\w-])[a-zA-Z][\w-]*", s2)) + s.count(" PSEUDO_EL ")
    return (ids, cls, tags)

if __name__ == "__main__":
    path = sys.argv[1]
    css, off = read_css(path)
    rules = parse(css, off)
    out = sys.argv[2] if len(sys.argv) > 2 else None
    if out:
        json.dump(rules, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    n_rules = sum(1 for r in rules if r["kind"]=="rule")
    strays = [r for r in rules if r["kind"].startswith("stray")]
    print("rules:", n_rules, "strays:", [(r["kind"], r["line"]) for r in strays])
    cnt = collections.Counter(r["sel"] for r in rules if r["kind"]=="rule")
    top = [(s,c) for s,c in cnt.most_common() if c>=3]
    print("selectors defined >=3 times:", len(top))
    for s,c in top[:30]:
        print(f"  {c:2d}  {s}")
    ctxs = collections.Counter(" && ".join(r["ctx"]) for r in rules if r["kind"]=="rule" and r["ctx"])
    print("media contexts:", len(ctxs))
    for k,v in ctxs.most_common():
        print(f"  {v:3d}  {k}")
