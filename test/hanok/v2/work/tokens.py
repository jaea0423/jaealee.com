"""Phase 1 — 토큰 계단 적용 도구. 구역 파일(work/zones/*.css)을 직접 고칩니다.

  python work/tokens.py inventory          지금 CSS 의 간격/글자/반경 px 값 분포 (손님용 화면 제외)
  python work/tokens.py exact              계단에 딱 맞는 값만 토큰으로 바꿈 (화면 변화 없음) — 1-A
  python work/tokens.py snap               계단에서 벗어난 값을 가장 가까운 계단으로 옮김 — 1-B (화면이 바뀜)

대상 구역: 2~9, 11, 11.extra (손님용 화면 10 은 --tvu 배수라 제외, 1 은 토큰 정의 자체)
"""
import os, re, sys, json, collections

WORK = os.path.dirname(os.path.abspath(__file__))
ZONES = [os.path.join(WORK, "zones", f) for f in ("2.css","3.css","4.css","5.css","6.css","7.css","8.css","9.css","11.css","11.extra.css")]

SPACE = {4:"--s4", 8:"--s8", 12:"--s12", 16:"--s16", 24:"--s24", 32:"--s32", 48:"--s48"}
FONT  = {11:"--fs-label", 13:"--fs-sub", 15:"--fs-body", 17:"--fs-title", 20:"--fs-head", 28:"--fs-num"}
RADIUS= {6:"--r-sm", 10:"--r-md", 16:"--r-lg"}
SPACE_PROPS  = re.compile(r"^(padding|margin|gap|row-gap|column-gap)(-(top|right|bottom|left))?$")
FONT_PROPS   = re.compile(r"^font-size$")
RADIUS_PROPS = re.compile(r"^border-radius$")

def split_decls(body):
    out=[]; depth=0; q=None; cur=""
    for c in body:
        if q:
            cur+=c
            if c==q: q=None
            continue
        if c in "'\"": q=c; cur+=c; continue
        if c=="(": depth+=1
        elif c==")": depth-=1
        if c==";" and depth==0: out.append(cur); cur=""
        else: cur+=c
    if cur: out.append(cur)
    return out

# ---- 1-B: 계단 밖 값을 어디로 옮길지 (재아 확인: 2026-09-05) ----
# 규칙: 두 계단의 정중앙이면 위로 (밝은 조명 태블릿에서 작아지는 쪽은 피함). 그 밖에는 가장 가까운 계단.
# 예외: 본문 아래 여백 60·80·90 (FAB·적용 바 자리), 알약 999, 음수, 1px 이하, clamp() 안의 값은 그대로.
SNAP_SPACE = {2:4, 3:4, 5:4, 6:8, 7:8, 9:8, 10:12, 11:12, 13:12, 14:16, 15:16, 18:16, 20:24, 22:24, 26:24, 28:32, 34:32}
SNAP_FONT  = {9:11, 9.5:11, 10:11, 10.5:11, 11.5:11, 12:13, 12.5:13, 13.5:13, 14:15, 14.5:15, 15.5:15, 16:17, 16.5:17,
              18:17, 18.5:20, 19:20, 21:20, 22:20, 23:20, 24:28, 26:28, 30:28, 32:28, 38:40, 40:40, 42:40}
SNAP_RADIUS= {2:6, 3:6, 4:6, 5:6, 7:6, 8:6, 9:10, 11:10, 12:10}
FONT[40] = "--fs-big"      # 큰 숫자(인원 타일·숫자 팝업) 전용 한 단
SNAP = {id(SPACE): SNAP_SPACE, id(FONT): SNAP_FONT, id(RADIUS): SNAP_RADIUS}

def rewrite_value(prop, value, table, snap):
    """값 안의 Npx 를 토큰으로. snap 이면 위 표대로 계단으로 옮김"""
    changed = []
    if "clamp(" in value: return value, changed
    def rep(m):
        n = float(m.group(1))
        if n <= 1: return m.group(0)
        if n in table:
            changed.append((n, n)); return f"var({table[n]})"
        if not snap: return m.group(0)
        near = SNAP[id(table)].get(n)
        if near is None: return m.group(0)
        changed.append((n, near)); return f"var({table[near]})"
    new = re.sub(r"(?<![\w.-])(\d*\.?\d+)px", rep, value)
    return new, changed

def process(mode, only=None):
    """only: 'space' | 'font' | 'radius' — 한 항목씩 적용할 때"""
    total = collections.Counter(); moves = collections.Counter()
    for path in ZONES:
        if not os.path.exists(path): continue
        css = open(path, encoding="utf-8").read()
        out = []; i = 0
        # 블록 단위로: 셀렉터{ ... } 의 몸통만 손댑니다 (주석 안은 건드리지 않음)
        while True:
            j = css.find("{", i)
            if j < 0: out.append(css[i:]); break
            # 주석 안의 { 는 건너뜀
            last_c = css.rfind("/*", i, j); last_e = css.rfind("*/", i, j)
            if last_c > last_e:
                k = css.find("*/", j); out.append(css[i:k+2]); i = k+2; continue
            head = css[i:j+1]
            # 앞 @media 블록의 닫는 } 가 머리에 딸려 오므로 떼어 냅니다 (안 떼면 '@' 로 안 시작해 첫 규칙을 건너뜀)
            head_sel = re.sub(r"/\*.*?\*/", "", head, flags=re.S).strip().lstrip("}").strip()
            if head_sel.startswith("@"):   # @media { … } 껍데기는 통과 (앞에 주석이 붙어 있어도)
                out.append(head); i = j+1; continue
            if re.match(r"^(\.tv|\.ts-|\.dsec|\.intro)", head_sel):   # 손님용 화면 규칙은 손대지 않음 (11구역 안의 것도)
                k = css.find("}", j); out.append(css[i:k+1]); i = k+1; continue
            k = css.find("}", j)
            body = css[j+1:k]
            new_parts = []
            for d in split_decls(body):
                if ":" not in d or d.strip().startswith("/*"): new_parts.append(d); continue
                p, v = d.split(":", 1); pn = p.strip().lower()
                table = SPACE if SPACE_PROPS.match(pn) else FONT if FONT_PROPS.match(pn) else RADIUS if RADIUS_PROPS.match(pn) else None
                if only and table is not {"space":SPACE, "font":FONT, "radius":RADIUS}[only]: table = None
                if table:
                    nv, ch = rewrite_value(pn, v, table, mode == "snap")
                    for a, b in ch:
                        total[pn.split("-")[0]] += 1
                        if a != b: moves[(pn.split("-")[0], a, b)] += 1
                    new_parts.append(p + ":" + nv)
                else:
                    new_parts.append(d)
            out.append(head + ";".join(new_parts) + "}")
            i = k+1
        new = "".join(out)
        if new != css:
            open(path, "w", encoding="utf-8").write(new)
            print(os.path.basename(path), "고침")
    print("토큰으로 바꾼 선언:", dict(total))
    if moves:
        print("계단으로 옮긴 값 (속성, 원래→계단: 개수):")
        for (p, a, b), n in sorted(moves.items()): print(f"  {p} {a:g}→{b:g}: {n}")

if __name__ == "__main__":
    process(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
