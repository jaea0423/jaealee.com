"""통합 전(원본)과 통합 후(새 파일)의 규칙 목록을 비교해, 순서가 의미를 갖는 쌍이 뒤집히지 않았는지 검사합니다.

검사 1 (같은/겹치는 컨텍스트 안의 순서):
  원본에서 A 가 B 보다 앞이고, 둘이 같은 우선순위·같은 속성(값 다름)·실제 DOM 에서 같은 요소에 걸릴 수 있으면
  새 파일에서도 A 의 마지막 정의가 B 의 마지막 정의보다 앞이어야 합니다.
  컨텍스트가 다르더라도 뷰포트 범위가 겹치면(예: max-width:900 과 max-width:767) 같이 검사합니다.
검사 2 (선언 보존):
  (셀렉터, 컨텍스트, 속성) 의 최종값이 원본과 새 파일에서 같아야 합니다. 빠지거나 바뀐 것을 보고합니다.
사용: python csscheck.py rules_before.json rules_after.json snaps/*.json
"""
import json, sys, re, collections
from cssparse import specificity

before = [r for r in json.load(open(sys.argv[1], encoding="utf-8")) if r["kind"] == "rule" and not r.get("dropped")]
after = [r for r in json.load(open(sys.argv[2], encoding="utf-8")) if r["kind"] == "rule" and not r.get("dropped")]
snap_files = [a for a in sys.argv[3:] if a.endswith(".json")]
PERMISSIVE = "--permissive" in sys.argv   # 스냅샷 없이: 태그만 맞으면 같은 요소에 걸릴 수 있다고 봄 (후보가 많이 나옴)

def norm_ctx(ctx):
    return " && ".join(re.sub(r"\s+", "", c) for c in ctx)

for rs in (before, after):
    for i, r in enumerate(rs):
        r["i"] = i; r["ctxkey"] = norm_ctx(r["ctx"]); r["spec"] = specificity(r["sel"])

combos = set()
for f in snap_files:
    d = json.load(open(f, encoding="utf-8"))
    # shots.py combos 형식: ["tag.cls.cls|조상클래스들|조상태그들", ...]
    for seg in d:
        if seg.startswith("ERR"): continue
        own, anc, anct = (seg.split("|") + ["", ""])[:3]
        parts = own.split(".")
        combos.add((parts[0], frozenset(p for p in parts[1:] if p),
                    frozenset(p for p in anc.split(".") if p), frozenset(p for p in anct.split(".") if p)))
print("DOM combos:", len(combos))

def compounds(sel):
    """셀렉터 → [(태그, 클래스집합), ...] 왼쪽부터. 가상 클래스/요소·속성은 무시"""
    s = re.sub(r"::?[\w-]+(\([^)]*\))?", "", sel)
    s = re.sub(r"\[[^\]]*\]", "", s)
    out = []
    for part in re.split(r"\s*[>+~]\s*|\s+", s.strip()):
        if not part: continue
        tag = re.match(r"^[a-zA-Z][\w-]*|\*", part)
        out.append((tag.group(0) if tag else "", frozenset(re.findall(r"\.([\w-]+)", part))))
    return out

def fits(sel_comps, combo):
    """이 셀렉터가 이 DOM 요소(조합)에 걸릴 수 있는가 — 맨 오른쪽은 요소 자신, 나머지는 조상에 있어야 함"""
    t, cs, anc, anct = combo
    last_tag, last_cls = sel_comps[-1]
    if last_tag and last_tag != "*" and last_tag != t: return False
    if not last_cls <= cs: return False
    for at, ac in sel_comps[:-1]:
        if at and at != "*" and at not in anct: return False
        if not ac <= anc: return False
    return True

_cm = {}
def comatch(a, b):
    k = (a, b)
    if k in _cm: return _cm[k]
    A, B = compounds(a), compounds(b)
    if PERMISSIVE:
        res = not (A[-1][0] and B[-1][0] and A[-1][0] != B[-1][0])
    else:
        res = any(fits(A, c) and fits(B, c) for c in combos)
    _cm[k] = res
    return res

# ---- 미디어 조건 겹침 (폭·높이 구간만 봅니다. 그 밖의 조건은 '겹칠 수 있음'으로) ----
def ranges(ctx):
    """ctx → list of (wmin,wmax,hmin,hmax) 대안(쉼표) 목록. @supports 는 None (별도 취급)"""
    if not ctx: return [(0, 1e9, 0, 1e9)]
    if "@supports" in ctx: return None
    out = []
    for part in ctx.split("&&"):
        part = part.strip()
        if not part.startswith("@media"): continue
        alts = part[len("@media"):].split(",")
        rr = []
        for alt in alts:
            wmin, wmax, hmin, hmax = 0, 1e9, 0, 1e9
            for m in re.finditer(r"\((min|max)-(width|height):\s*([\d.]+)px\)", alt):
                kind, dim, val = m.group(1), m.group(2), float(m.group(3))
                if dim == "width":
                    if kind == "min": wmin = max(wmin, val)
                    else: wmax = min(wmax, val)
                else:
                    if kind == "min": hmin = max(hmin, val)
                    else: hmax = min(hmax, val)
            rr.append((wmin, wmax, hmin, hmax))
        out.append(rr)
    # && 로 중첩된 경우 교집합
    res = out[0] if out else [(0, 1e9, 0, 1e9)]
    for rr in out[1:]:
        res = [(max(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), min(a[3], b[3])) for a in res for b in rr]
    return res

def overlap(c1, c2):
    r1, r2 = ranges(c1), ranges(c2)
    if r1 is None or r2 is None: return c1 == c2
    for a in r1:
        for b in r2:
            if max(a[0], b[0]) <= min(a[1], b[1]) and max(a[2], b[2]) <= min(a[3], b[3]):
                return True
    return False

# ---- 검사 2: 최종값 보존 ----
TOKENS = {"--s4":"4px","--s8":"8px","--s12":"12px","--s16":"16px","--s24":"24px","--s32":"32px","--s48":"48px",
          "--fs-label":"11px","--fs-sub":"13px","--fs-body":"15px","--fs-title":"17px","--fs-head":"20px","--fs-num":"28px","--fs-big":"40px",
          "--r-sm":"6px","--r-md":"10px","--r-lg":"16px"}
def resolve(v):
    """Phase 1 토큰(var(--s8) 등)을 px 로 되돌려 비교합니다 — 토큰으로 바꾼 것은 값이 같아야 함"""
    return re.sub(r"var\((--[\w-]+)\)", lambda m: TOKENS.get(m.group(1), m.group(0)), v)
def final_map(rs):
    fm = {}
    for r in rs:
        for p, v, imp in r["decls"]:
            fm[(r["sel"], r["ctxkey"], p)] = (re.sub(r"\s+", " ", resolve(v)), imp)
    return fm
fb, fa = final_map(before), final_map(after)
DEAD = set(json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "sections.json"), encoding="utf-8")).get("dead", []))
def is_dead(sel): return any(m in DEAD for m in re.findall(r"\.([\w-]+)", sel))
missing = [k for k in fb if k not in fa and not is_dead(k[0])]
changed = [k for k in fb if k in fa and fb[k] != fa[k]]
extra = [k for k in fa if k not in fb]
print(f"\n[검사 2] 최종값: 빠짐 {len(missing)} / 바뀜 {len(changed)} / 새로 생김 {len(extra)}")
for k in missing: print("  MISSING", k, fb[k])
for k in changed: print("  CHANGED", k, fb[k], "->", fa[k])
for k in extra: print("  EXTRA", k, fa[k])

# ---- 검사 1: 순서 ----
def last_pos(rs):
    lp = {}
    for r in rs:
        for p, v, imp in r["decls"]:
            lp[(r["sel"], r["ctxkey"], p)] = r["i"]
    return lp
lpb, lpa = last_pos(before), last_pos(after)

# 원본에서 순서가 의미 있는 쌍 (속성 단위)
pairs = []
by_prop = collections.defaultdict(list)
for r in before:
    for p, v, imp in r["decls"]:
        by_prop[p].append((r, v, imp))
for p, lst in by_prop.items():
    for x in range(len(lst)):
        a, va, ia = lst[x]
        for y in range(x + 1, len(lst)):
            b, vb, ib = lst[y]
            if a["sel"] == b["sel"] and a["ctxkey"] == b["ctxkey"]: continue   # 같은 셀렉터는 합쳐짐
            if a["spec"] != b["spec"] or ia != ib: continue
            if re.sub(r"\s+", " ", va) == re.sub(r"\s+", " ", vb): continue
            if not overlap(a["ctxkey"], b["ctxkey"]): continue
            if not comatch(a["sel"], b["sel"]): continue
            pairs.append((a, b, p))
print(f"\n[검사 1] 순서가 의미 있는 쌍: {len(pairs)}")
bad = 0
seen = set()
for a, b, p in pairs:
    ka = (a["sel"], a["ctxkey"], p); kb = (b["sel"], b["ctxkey"], p)
    if ka not in lpa or kb not in lpa: continue   # 빠진 건 검사 2 에서 보고
    # 원본: 이 속성에 대한 A 의 마지막 위치가 B 의 마지막 위치보다 앞인가?
    ob = lpb[ka] < lpb[kb]
    oa = lpa[ka] < lpa[kb]
    if ob != oa:
        key = (a["sel"], b["sel"], a["ctxkey"], b["ctxkey"], p)
        if key in seen: continue
        seen.add(key)
        bad += 1
        print(f"  ORDER FLIP  {p}: [{a['sel']}] @{a['ctxkey'] or 'base'} (line {a['line']})  vs  [{b['sel']}] @{b['ctxkey'] or 'base'} (line {b['line']})")
print("order flips:", bad)
