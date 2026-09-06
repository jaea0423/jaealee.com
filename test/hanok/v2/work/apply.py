"""Phase 0 — CSS 구역 통합을 한 구역씩 적용합니다.

  python work/apply.py N        (v2 폴더에서)  → 구역 1..N 을 정리한 CSS 를 v2/src/index.html 에 써넣습니다

원리
- 원본은 work/src_before.html (통합 전 사본) 입니다. 항상 여기서 다시 계산하므로 N 을 늘려 가며 반복 실행할 수 있습니다.
- 구역 1..N 에 속한 셀렉터: 흩어진 정의를 하나로 합쳐 새 구역 블록으로 냅니다.
  · 선언은 원본 순서대로 이어 붙이되 같은 속성이 뒤에 또 나오면 앞 것을 지웁니다 (축약/개별 속성 순서 유지 → 결과 동일)
  · 한 번만 정의된 규칙은 원본 텍스트(주석 포함)를 그대로 옮깁니다
- 아직 안 한 구역: 원본 텍스트를 그대로 둡니다 ('아직 정리하지 않은 부분').
- 옮긴 셀렉터의 @media 규칙은 파일 끝 '반응형' 구역으로 모읍니다. 원본 순서를 그대로 지키고
  (조건별로 한 덩어리로 합치면 앞뒤가 바뀌어 화면이 바뀝니다), 원본에서 뒤쪽 규칙에
  항상 덮여 효력이 없던 선언은 지웁니다 (그대로 두면 끝으로 가면서 살아나 화면이 바뀝니다).
- @supports 폴백은 항상 맨 끝(12 구역)에 둡니다.
- 한 번도 쓰이지 않는 클래스(sections.json 의 dead)는 지웁니다.
"""
import json, sys, re, os, collections
from cssparse import parse, read_css, specificity

WORK = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(WORK)
N = int(sys.argv[1])

css, off = read_css(os.path.join(WORK, "src_before.html"))
allrules = parse(css, off)
# 짝 없는 } 바로 뒤의 규칙은 브라우저가 무효 처리해 왔으므로(효력 없음) 옮기지 않고 잔여 원본에서도 지웁니다
dropped = [r for r in allrules if r["kind"] == "rule" and r.get("dropped")]
for r in dropped: print(f"  (원본에서 효력 없던 규칙 제거 — {r['line']}행, 짝 없는 }} 뒤) {r['sel']}")
rules = [r for r in allrules if r["kind"] == "rule" and not r.get("dropped")]
strays = [r for r in allrules if r["kind"] == "stray_close"]
supports = [r for r in allrules if r["kind"] == "rule" and r["ctx"] and r["ctx"][0].startswith("@supports")]
SEC = json.load(open(os.path.join(WORK, "sections.json"), encoding="utf-8"))
DEAD = set(SEC["dead"]); SECTIONS = SEC["sections"]; MEDIA_ORDER = SEC.get("media_order", [])
HEADER = open(os.path.join(WORK, "header.css"), encoding="utf-8").read()

CTX_TEXT = {}
for i, r in enumerate(rules):
    r["i"] = i
    r["ctxkey"] = " && ".join(re.sub(r"\s+", "", c) for c in r["ctx"])
    r["spec"] = specificity(r["sel"])
    CTX_TEXT.setdefault(r["ctxkey"], r["ctx"])

# ---------------- 구역 배정 ----------------
def key_class(sel):
    s = re.sub(r"::?[\w-]+(\([^)]*\))?", "", sel)
    s = re.sub(r"\[[^\]]*\]", "", s)
    parts = re.split(r"\s*[>+~]\s*|\s+", s.strip())
    if parts[0].startswith("body.theme-hanok"): return "theme-hanok"
    m = re.findall(r"\.([\w-]+)", parts[0])
    return m[0] if m else parts[0]

def zone_of(sel):
    """(구역 번호 1.., 패턴 순번). dead 는 0."""
    if any(m in DEAD for m in re.findall(r"\.([\w-]+)", sel)): return (0, 0)
    kc = key_class(sel)
    for zi, (name, pats) in enumerate(SECTIONS, start=1):
        for pi, p in enumerate(pats):
            if re.fullmatch(p, kc) or re.fullmatch(p, sel): return (zi, pi)
    return (99, 0)

for r in rules:
    r["zone"], r["pi"] = zone_of(r["sel"])
    r["supports"] = bool(r["ctx"]) and r["ctx"][0].startswith("@supports")
    r["moved"] = (r["zone"] <= N) and not r["supports"]     # dead(0) 포함

unassigned = sorted({r["sel"] for r in rules if r["zone"] == 99})
if unassigned:
    print("구역 미배정 셀렉터:", unassigned); sys.exit(1)

# ---------------- 주석 ----------------
comments = []   # (start, end, text, depth)
pos = 0; depth = 0; scan = 0
while True:
    j = css.find("/*", pos)
    if j < 0: break
    depth += css.count("{", scan, j) - css.count("}", scan, j)
    depth = max(depth, 0)
    k = css.find("*/", j + 2)
    if k < 0: break
    comments.append((j, k + 2, css[j:k+2], depth)); scan = k + 2; pos = k + 2
used_comments = set()
def top_comments_before(start):
    out = []
    for cs, ce, t, d in comments:
        if d != 0 or (cs, ce) in used_comments or ce > start: continue
        gap = css[ce:start]
        if gap.count("\n") <= 2 and gap.strip() == "":
            used_comments.add((cs, ce)); out.append(t)
    return out
def inner_comments(start, end):
    out = []
    for cs, ce, t, d in comments:
        if start < cs < end and (cs, ce) not in used_comments:
            used_comments.add((cs, ce)); out.append(t)
    return out

# ---------------- 원본 블록 ----------------
blocks = collections.OrderedDict()
for r in rules:
    b = blocks.setdefault(r["start"], {"rules": [], "start": r["start"], "end": r["end"], "line": r["line"]})
    b["rules"].append(r)

defs = collections.defaultdict(list)          # (sel, ctx) → 정의 목록
for r in rules:
    defs[(r["sel"], r["ctxkey"])].append(r)

def merge_decls(ds):
    out = []
    for d in ds:
        for p, v, imp in d["decls"]:
            out = [x for x in out if x[0] != p]
            out.append((p, v, imp))
    return out
def fmt(decls):
    return "; ".join(f"{p}:{v}{' !important' if imp else ''}" for p, v, imp in decls)

# ---------------- 구역 블록 만들기 (기본 컨텍스트, 옮기는 것만) ----------------
zone_items = collections.defaultdict(list)    # zone → [((pi, line), text)]
emitted = set()
for start, b in blocks.items():
    live = [r for r in b["rules"] if r["moved"] and r["zone"] > 0 and not r["ctx"]]
    if not live: continue
    allmoved = all(r["moved"] for r in b["rules"])
    single = all(len(defs[(r["sel"], r["ctxkey"])]) == 1 for r in live)
    if single and allmoved and len(live) == len(b["rules"]):
        pre = top_comments_before(b["start"])
        text = css[b["start"]:b["end"]].strip()
        for cs, ce, t, d in comments:
            if b["start"] <= cs < b["end"]: used_comments.add((cs, ce))
        z = live[0]["zone"]
        zone_items[z].append(((live[0]["pi"], b["line"]), "\n".join(pre + [text])))
        continue
    for r in live:
        key = (r["sel"], r["ctxkey"])
        if key in emitted: continue
        ds = defs[key]
        if ds[0]["i"] != r["i"]: continue
        emitted.add(key)
        pre = []; inner = []
        for d in ds:
            bb = blocks[d["start"]]
            if all(x["moved"] for x in bb["rules"]):
                pre += top_comments_before(d["start"])
            inner += inner_comments(d["start"], d["end"])
        text = f"{r['sel']}{{{fmt(merge_decls(ds))}}}"
        zone_items[r["zone"]].append(((r["pi"], b["line"]), "\n".join(pre + [text] + inner)))

# ---------------- 옮기는 @media 규칙 ----------------
media_groups = collections.OrderedDict()      # ctxkey → [(sel, decls, i, line)]
# 같은 (셀렉터, 조건)이 여러 번 정의돼 있어도 한 곳으로 합치지 않고 각자 원래 자리에 둡니다.
# 합쳐서 마지막 자리로 옮기면 앞쪽 정의의 속성이 함께 끌려가, 그 사이에 있던 다른 셀렉터 규칙
# (예: .sheet @768 의 max-width 가 .sheet-wide 뒤로) 과 앞뒤가 바뀝니다.
# 대신 (1) 같은 셀렉터·조건의 뒤 정의가 덮는 속성, (2) 뒤쪽 기본 규칙이 항상 덮는 속성(효력 없음)만 지웁니다.
for (sel, ctx), ds in defs.items():
    if not ctx or ds[0]["supports"] or not ds[0]["moved"] or ds[0]["zone"] == 0: continue
    base = defs.get((sel, ""), [])
    for k, d in enumerate(ds):
        later_same = {p for later in ds[k+1:] for p, _, _ in later["decls"]}
        kept = []
        for p, v, imp in d["decls"]:
            if p in later_same and not imp: continue
            dead = any(any(pp == p for pp, _, _ in bd["decls"]) and bd["i"] > d["i"] and not imp for bd in base)
            if dead: print(f"  (효력 없던 미디어 선언 제거) {sel} @ {ctx} :: {p}:{v}")
            else: kept.append((p, v, imp))
        if kept:
            media_groups.setdefault(ctx, []).append((sel, kept, d["i"], d["line"]))


# ---------------- 잔여 원본 (아직 안 옮긴 부분) ----------------
edits = []   # (start, end, replacement)
for start, b in blocks.items():
    moved = [r for r in b["rules"] if r["moved"] or r["supports"]]
    if not moved: continue
    if len(moved) == len(b["rules"]):
        s = b["start"]
        # 바로 앞에 붙은(이미 구역으로 옮겨진) 주석도 함께 지웁니다
        for cs, ce, t, d in comments:
            if (cs, ce) in used_comments and ce <= s and css[ce:s].strip() == "" and css[ce:s].count("\n") <= 2:
                s = min(s, cs)
        edits.append((s, b["end"], ""))
    else:
        remain = [r["sel"] for r in b["rules"] if not (r["moved"] or r["supports"])]
        head_end = css.index("{", b["start"])
        edits.append((b["start"], head_end, ", ".join(remain)))
for st in strays:
    edits.append((st["pos"], st["pos"] + 1, ""))
for r in dropped:
    edits.append((r["start"], r["end"], ""))
# 구역으로 옮겨진 주석 중 아직 남아 있는 것 제거
for cs, ce, t, d in comments:
    if (cs, ce) in used_comments and not any(a <= cs and ce <= e for a, e, _ in edits):
        edits.append((cs, ce, ""))
residual = css
edits = sorted(set(edits), key=lambda x: -x[0])   # 같은 구간이 두 번 들어오면 한 번만 (두 번 지우면 엉뚱한 글자가 지워집니다)
for a, e, rep in edits:
    residual = residual[:a] + rep + residual[e:]
# 속이 빈 @media / @supports 껍데기 제거
for _ in range(3):
    # 속이 비었거나 주석만 남은 껍데기 제거
    residual = re.sub(r"@(media|supports)[^{}]*\{(?:\s|/\*.*?\*/)*\}", "", residual, flags=re.S)
residual = re.sub(r"\n{3,}", "\n\n", residual).strip("\n")

# ---------------- 출력 ----------------
out = [HEADER]
for zi, (name, pats) in enumerate(SECTIONS, start=1):
    if zi > N: break
    out.append(f"\n\n/* ============================================================\n   {name}\n   ============================================================ */")
    gen = "\n".join(text for key, text in sorted(zone_items.get(zi, []), key=lambda x: x[0]))
    # 손으로 다듬은 구역 파일이 있으면 그것을 씁니다 (work/zones/N.css).
    # 생성본은 work/zones/N.gen.css 에 남겨 두므로, 다듬은 파일과 생성본을 비교해 빠진 규칙이 없는지 볼 수 있습니다.
    os.makedirs(os.path.join(WORK, "zones"), exist_ok=True)
    open(os.path.join(WORK, "zones", f"{zi}.gen.css"), "w", encoding="utf-8").write(gen + "\n")
    hand = os.path.join(WORK, "zones", f"{zi}.css")
    if os.path.exists(hand):
        out.append(open(hand, encoding="utf-8").read().strip("\n"))
        print(f"  구역 {zi}: 손으로 다듬은 work/zones/{zi}.css 사용")
    else:
        out.append(gen)
if "{" in residual:
    out.append(f"\n\n/* ============================================================\n   ── 아직 정리하지 않은 부분 (원본 그대로) — 구역 {N+1} 부터 차례로 옮깁니다 ──\n   ============================================================ */")
    out.append(residual)
else:
    # 규칙이 하나도 안 남았으면(모든 구역을 옮긴 뒤) 옛 구역 머리 주석만 남으므로 통째로 뺍니다
    print("  잔여 원본: 규칙 없음 (옛 주석만 남아 생략)")
if media_groups:
    out.append("\n\n/* ============================================================\n"
               "   11. 반응형 — 정리한 구역의 @media 규칙\n"
               "   원본에서의 앞뒤 순서를 그대로 지키고, 붙어 있는 같은 조건끼리만 한 블록으로 묶었습니다.\n"
               "   (같은 조건을 한 덩어리로 합치면 다른 조건 블록과의 앞뒤가 바뀌어 화면이 바뀝니다 — 겹치는 조건은 뒤가 이깁니다)\n"
               "   ============================================================ */")
    flat = []   # (원본 위치, ctx, sel, decls)
    for ctx, lst in media_groups.items():
        for sel, decls, i, line in lst:
            flat.append((i, ctx, sel, decls))
    flat.sort()
    prev = None; media_lines = []
    for i, ctx, sel, decls in flat:
        if ctx != prev:
            if prev is not None: media_lines.append("}" * len(CTX_TEXT[prev]))
            head = " { ".join(re.sub(r"\s+", " ", p.strip()) for p in CTX_TEXT[ctx])
            media_lines.append("\n" + head + "{")
            prev = ctx
        media_lines.append(f"  {sel}{{{fmt(decls)}}}")
    if prev is not None: media_lines.append("}" * len(CTX_TEXT[prev]))
    gen11 = "\n".join(media_lines)
    open(os.path.join(WORK, "zones", "11.gen.css"), "w", encoding="utf-8").write(gen11 + "\n")
    hand11 = os.path.join(WORK, "zones", "11.css")
    if os.path.exists(hand11):
        out.append(open(hand11, encoding="utf-8").read().strip("\n"))
        print("  구역 11: 손으로 다듬은 work/zones/11.css 사용")
    else:
        out.append(gen11)
    # 손으로 덧붙이는 규칙 (work/zones/11.extra.css) — 기본 규칙을 앞 구역으로 올리면서 뒤에 있던 @media 규칙에
    # 지게 된 것을 되살릴 때 씁니다 (같은 규칙을 미디어 구역 뒤에 한 번 더 둠)
    extra = os.path.join(WORK, "zones", "11.extra.css")
    if os.path.exists(extra):
        out.append(open(extra, encoding="utf-8").read().strip("\n"))
if supports:
    out.append("\n\n/* ============================================================\n   12. 구형 브라우저 폴백 — 반드시 @supports 안에 둡니다\n   ============================================================ */")
    seen = set()
    for r in supports:
        b = blocks[r["start"]]
        # @supports 블록 전체 텍스트(머리부터 닫는 괄호까지)를 그대로 옮깁니다
        hs = css.rfind("@supports", 0, r["start"])
        if hs in seen: continue
        seen.add(hs)
        depth = 0; k = css.index("{", hs)
        while True:
            c = css[k]
            if c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: break
            k += 1
        pre = top_comments_before(hs)
        out.append("\n".join(pre + [css[hs:k+1]]))

new_css = "\n".join(out).strip("\n") + "\n"
src_path = os.path.join(V2, "src", "index.html")
html = open(src_path, encoding="utf-8").read()
a = html.index("<style>") + len("<style>"); b_ = html.index("</style>")
open(src_path, "w", encoding="utf-8", newline="\n").write(html[:a] + "\n" + new_css + html[b_:])
moved_n = sum(1 for r in rules if r["moved"] and r["zone"] > 0)
dead_n = sum(1 for r in rules if r["zone"] == 0)
print(f"구역 1..{N} 적용: 옮긴 규칙 {moved_n}개, 지운 죽은 규칙 {dead_n}개, 새 CSS {len(new_css.splitlines())}줄 → {src_path}")
