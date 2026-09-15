# -*- coding: utf-8 -*-
"""v7 정적 검사 — js 조각 전부를 놓고
   1) 두 번 이상 정의된 함수(뒤 정의가 이김 — 앞 것은 죽은 코드이거나 버그)
   2) 정의만 있고 아무 데서도 안 부르는 함수
   3) 부르는데 정의가 없는 식별자(onclick 문자열 포함) — 브라우저 내장·DOM 은 제외
   4) 주석으로 막아 둔 코드 덩어리(// 로 시작하는 줄이 8줄 이상 이어짐)
   결과는 화면에 출력. 판단은 사람이."""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L

parts = L.parts("js")
texts = {n: L.load(n) for n in parts}
allj = "\n".join(texts[n] for n in parts)

# 주석·문자열을 대충 걷어낸 본문(참조 세기용) — 템플릿 문자열 안의 onclick 은 남겨야 하므로 문자열은 안 걷고 주석만 걷습니다
def strip_comments(s):
    s = re.sub(r"/\*[\s\S]*?\*/", "", s)
    s = re.sub(r"(?m)^\s*//.*$", "", s)
    return s
body = {n: strip_comments(texts[n]) for n in parts}
allb = "\n".join(body[n] for n in parts)

# 1) 정의
defs = {}
for n in parts:
    for m in re.finditer(r"(?m)^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(", body[n]):
        defs.setdefault(m.group(1), []).append(n)
    for m in re.finditer(r"(?m)^(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>", body[n]):
        defs.setdefault(m.group(1), []).append(n)
dups = {k: v for k, v in defs.items() if len(v) > 1}
print("== 두 번 이상 정의된 함수 (%d) ==" % len(dups))
for k, v in sorted(dups.items()): print("  %-24s %s" % (k, ", ".join(v)))

# 2) 참조 없는 함수
print("\n== 정의만 있고 안 부르는 함수 ==")
unused = []
for k in sorted(defs):
    n = len(re.findall(r"(?<![\w$.])" + re.escape(k) + r"(?![\w$])", allb))
    if n <= len(defs[k]):
        unused.append((k, defs[k]))
for k, v in unused: print("  %-24s %s" % (k, ", ".join(v)))
print("  (%d)" % len(unused))

# 3) 정의 없는 호출 — onclick 문자열 안 포함
KNOWN = set("""alert confirm prompt fetch setTimeout clearTimeout setInterval clearInterval requestAnimationFrame cancelAnimationFrame
Promise Math JSON Date Object Array String Number Boolean Error TypeError RegExp Map Set parseInt parseFloat isNaN isFinite encodeURIComponent decodeURIComponent
console document window navigator location history localStorage sessionStorage screen btoa atob AbortController Blob URL FormData Intl
if for while switch return function typeof new delete void catch try else do in of instanceof throw await async this super class extends static get set
escape unescape Symbol Reflect Proxy WeakMap Uint8Array TextEncoder TextDecoder structuredClone crypto performance matchMedia getComputedStyle
Image Audio Event CustomEvent KeyboardEvent MouseEvent Node Element HTMLElement DOMParser XMLHttpRequest WebSocket
""".split())
calls = set(re.findall(r"(?<![\w$.])([A-Za-z_$][\w$]*)\s*\(", allb))
undefined = sorted(c for c in calls if c not in defs and c not in KNOWN and not re.match(r"^[A-Z_]+$", c))
# 지역 함수(안쪽 const f = () =>, function 안의 function)는 defs 에 없으니 본문에 'function 이름' 또는 '이름 =' 가 있으면 제외
undefined = [c for c in undefined if not re.search(r"(?<![\w$.])(?:function\s+" + re.escape(c) + r"\s*\(|(?:const|let|var)\s+" + re.escape(c) + r"\s*=|\b" + re.escape(c) + r"\s*=\s*(?:function|\(|async|[A-Za-z_$][\w$]*\s*=>))", allb)]
print("\n== 정의 없이 부르는 이름 (%d) ==" % len(undefined))
for c in undefined:
    where = [n for n in parts if re.search(r"(?<![\w$.])" + re.escape(c) + r"\s*\(", body[n])]
    print("  %-24s %s" % (c, ", ".join(where)))

# 4) 주석 코드 덩어리
print("\n== 주석으로 막아 둔 코드 덩어리(8줄 이상) ==")
for n in parts:
    lines = texts[n].split("\n"); i = 0
    while i < len(lines):
        if re.match(r"^\s*//", lines[i]):
            j = i
            while j < len(lines) and re.match(r"^\s*//", lines[j]): j += 1
            if j - i >= 8: print("  %-22s %d~%d행 (%d줄) %s" % (n, i + 1, j, j - i, lines[i].strip()[:60]))
            i = j
        else: i += 1
