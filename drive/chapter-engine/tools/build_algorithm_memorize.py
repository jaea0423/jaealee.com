# 암기노트 — 알고리즘 기말 (범위를 계속 추가, 범위마다 새 쪽)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapgen import *
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'algorithm/memorize/final.html')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# 검증 (개념노트와 같은 값)
S = [1, 3, 0, 5, 3, 5, 6, 8, 8, 2, 12]; F = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
L = [0]; k = 0
for i in range(1, len(S)):
    if F[k] <= S[i]: L.append(i); k = i
assert L == [0, 3, 7, 10]
FREQ = dict(a=43, b=13, c=12, d=16, e=9, f=7); HCODE = CODE = dict(a='0', b='101', c='100', d='111', e='1101', f='1100')
assert sum(FREQ[x] * len(CODE[x]) for x in FREQ) == 230
assert 100 * 3 + 50 + 10 + 8 == 368

X, Y, T = v('X'), v('Y'), v('T')
a = lambda i: sb('a', i); b = lambda i: sb('b', i)
def f_(x): return f'{v("f")}({v(x)})'
def d_(t, x): return f'{v("d")}<sub>{t}</sub>({v(x)})'
n = v('n'); nlogn = f'O({n} log {n})'
def c(s): return f'<code>{H.escape(s)}</code>'

CODE = """<div class="mcode"><span class="h">강의실 배정</span>L = <mark>[0]</mark>, k = <mark>0</mark>
for i in range(<mark>1</mark>, n):
    if <mark>F[k] &lt;= S[i]</mark>:
        L.append(i), <mark>k = i</mark><span class="h">Huffman</span>while <mark>len(T) &gt; 1</mark>:
    x = <mark>extract_min</mark>(T)
    y = extract_min(T)
    z = Node(left = x, right = y)
    <mark>f(z) = f(x) + f(y)</mark>
    <mark>insert</mark>(T, z)</div>"""
FIX = f"""<ul class="fix">
<li><span>f 의 코드</span> <b>1100<s>1110</s></b></li>
<li><span>d 깊이 · 빈도</span> <b>3, 16<s>15</s></b></li>
<li><span>보조 1 의 {T}′</span> <b>최적이다</b></li>
<li><span>{d_("B′", "w")}</span> <b>{d_("B", "u")} − 1</b></li>
<li><span>포함 방향</span> <b>{sb("A", 1)} ⊂ {sb("G", 1)}</b></li>
<li><span>{n} = {v("k")} 의 {v("x")}, {v("y")}</span> <b>최소 빈도 두 문자</b></li>
</ul>"""

# ── 작은 그림 ──
def svg_coins():
    cs = [100, 100, 100, 50, 10] + [1] * 8; x = 14; o = ['<svg viewBox="0 0 340 52"><title>368원 = 100 × 3 + 50 + 10 + 1 × 8</title>']
    for c_ in cs:
        r = {100: 15, 50: 13, 10: 11, 1: 8}[c_]
        o.append(f'<circle cx="{x + r}" cy="26" r="{r}" fill="#E7F5EC" stroke="#15803D" stroke-width="1.6"/><text x="{x + r}" y="{26 + 4}" font-size="{11 if r > 9 else 8}" font-weight="800" text-anchor="middle" fill="#15803D">{c_}</text>')
        x += 2 * r + 3
    o.append('</svg>'); return ''.join(o)
def svg_jobs():
    U = 30; X0 = 10; o = ['<svg viewBox="0 0 340 56"><title>1 + 2 + 3 = 6, +4 = 10 &gt; 9</title>']; x = X0
    for t in (1, 2, 3):
        o.append(f'<rect x="{x}" y="14" width="{t * U}" height="24" fill="#FDEEE6" stroke="#C2410C" stroke-width="1.6"/><text x="{x + t * U / 2}" y="31" font-size="13" font-weight="800" text-anchor="middle" fill="#C2410C">{t}</text>'); x += t * U
    o.append(f'<rect x="{x}" y="14" width="{4 * U}" height="24" fill="#fff" stroke="#999" stroke-width="1.4" stroke-dasharray="5 3"/><text x="{x + 2 * U}" y="31" font-size="12" font-weight="700" text-anchor="middle" fill="#777">+4 = 10</text>')
    tx = X0 + 9 * U
    o.append(f'<line x1="{tx}" y1="6" x2="{tx}" y2="48" stroke="#111" stroke-width="2.4"/><text x="{tx + 4}" y="52" font-size="11" font-weight="800">T = 9</text></svg>')
    return ''.join(o)
def svg_iv():
    U = 22; X0 = 10; o = ['<svg viewBox="0 0 340 74"><title>0, 3, 7, 10 선택</title>']
    sel = {0: 0, 3: 0, 7: 0, 10: 0}; rows = {}
    lay = [[], [], []]
    for i, (s_, f_2) in enumerate(zip(S, F)):
        if i in sel: continue
        for li, row in enumerate(lay):
            if all(f2 <= s_ or f_2 <= s2 for s2, f2 in row): row.append((s_, f_2)); break
    for li, row in enumerate(lay):
        for s_, f_2 in row: o.append(f'<rect x="{X0 + s_ * U}" y="{4 + li * 11}" width="{(f_2 - s_) * U}" height="8" fill="#EEF0F4" stroke="#B5BAC4" stroke-width=".8"/>')
    for i in sel:
        o.append(f'<rect x="{X0 + S[i] * U}" y="40" width="{(F[i] - S[i]) * U}" height="16" fill="#1D4ED8"/><text x="{X0 + (S[i] + F[i]) / 2 * U}" y="52" font-size="11" font-weight="800" text-anchor="middle" fill="#fff">{i}</text>')
    o.append(f'<line x1="{X0}" y1="60" x2="{X0 + 14 * U}" y2="60" stroke="#111" stroke-width="1.2"/>')
    for t in (0, 4, 7, 11, 14): o.append(f'<text x="{X0 + t * U}" y="72" font-size="10" text-anchor="middle" fill="#333">{t}</text>')
    o.append('</svg>'); return ''.join(o)
def svg_tree():
    N = {'r': (150, 12, '', 0), 'a': (70, 44, 'a', 1), 'n57': (230, 44, '', 0), 'n25': (180, 76, '', 0), 'n32': (280, 76, '', 0),
         'c': (155, 108, 'c', 1), 'b': (205, 108, 'b', 1), 'n16': (255, 108, '', 0), 'd': (305, 108, 'd', 1), 'f': (230, 138, 'f', 1), 'e': (280, 138, 'e', 1)}
    E = [('r', 'a', 0), ('r', 'n57', 1), ('n57', 'n25', 0), ('n57', 'n32', 1), ('n25', 'c', 0), ('n25', 'b', 1), ('n32', 'n16', 0), ('n32', 'd', 1), ('n16', 'f', 0), ('n16', 'e', 1)]
    o = ['<svg viewBox="0 0 340 154"><title>허프만 트리</title>']
    for p_, c_, bit in E:
        (x1, y1), (x2, y2) = N[p_][:2], N[c_][:2]
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#7E22CE" stroke-width="1.4"/><text x="{(x1 + x2) / 2 + (-7 if bit == 0 else 7)}" y="{(y1 + y2) / 2 + 3}" font-size="10" font-weight="800" text-anchor="middle" fill="#7E22CE">{bit}</text>')
    for k_, (x, y, lab, leaf) in N.items():
        if leaf:
            o.append(f'<rect x="{x - 26}" y="{y - 9}" width="52" height="18" rx="2" fill="#F3E9FB" stroke="#7E22CE" stroke-width="1.3"/><text x="{x}" y="{y + 4}" font-size="10.5" font-weight="800" text-anchor="middle">{lab}={HCODE[lab]}</text>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="{9 if lab else 5}" fill="#fff" stroke="#7E22CE" stroke-width="1.3"/>' + (f'<text x="{x}" y="{y + 3.5}" font-size="8.5" font-weight="800" text-anchor="middle">{lab}</text>' if lab else ''))
    o.append('</svg>'); return ''.join(o)

def chain(*items):
    out = []
    for i, it in enumerate(items):
        cls = 'bx x' if it.startswith('!') else 'bx'
        out.append(f'<span class="{cls}">{it.lstrip("!")}</span>')
        if i < len(items) - 1: out.append('<span class="ar">→</span>')
    return '<div class="chain">' + ''.join(out) + '</div>'
def card(color, name, time, strat, fig, res, ch, extra=''):
    return (f'<div class="card {color}"><div class="hd">{name}<span>{time}</span></div><div class="in">'
            f'<div class="st">{strat}</div>{fig}<div class="res">{res}</div>{ch}{extra}</div></div>')

CARDS = '<div class="unit cards">' + ''.join([
  card('c-green', '거스름돈', '—', '큰 단위부터', svg_coins(), '368원 → 13개',
       chain('작은 단위 = 큰 단위의 <b>약수</b>', '그때만 최적'),
       chain('!반례 {1, 5, 7} · 10원', '!그리디 4개 vs 최적 2개')),
  card('c-orange', '일의 개수', '—', '짧은 일부터', svg_jobs(), '[2, 1, 4, 6, 3], T = 9 → 3개',
       chain(f'{X} + {a(4)} &gt; {T}<br><small>멈춤</small>', f'{Y} + {b(4)} ≤ {T}<br><small>가정</small>', f'{X} ≤ {Y}<br>{a(4)} ≤ {b(4)}<br><small>가장 짧음</small>') + chain(f'!{X} + {a(4)} ≤ {T} ⇒ 모순')),
  card('c-blue', '강의실 배정', f'O({n} log {n})', '빨리 끝나는 것부터', svg_iv(), 'L = [0, 3, 7, 10] → 4개',
       chain(f'{a(1)} → 0', f'{sb("A", 1)} ⊂ {sb("G", 1)}', f'{a(2)}→3 … {a(4)}→10') + chain(f'!{a(5)} 남음', '!for 문이 놓칠 리 없음 ⇒ 모순'),
       '<div class="cd">L = <mark>[0]</mark>, k = <mark>0</mark>\nfor i in range(<mark>1</mark>, n):\n    if <mark>F[k] &lt;= S[i]</mark>:\n        L.append(i), <mark>k = i</mark></div><span class="tag">판서 정정 <b>A₁ ⊂ G₁</b> (방향 주의)</span>'),
  card('c-purple', 'Huffman 코딩', f'O({n} log {n})', '최소 빈도 2개 합침', svg_tree(), '300 → 230비트 <small>16 → 25 → 32 → 57 → 100</small>',
       chain(f'extract_min · insert O(log {n}) × {n} 번', f'O({n} log {n})'),
       '<div class="cd">while <mark>len(T) &gt; 1</mark>:\n    x = <mark>extract_min</mark>(T); y = extract_min(T)\n    z = Node(left = x, right = y)\n    <mark>f(z) = f(x) + f(y)</mark>; <mark>insert</mark>(T, z)</div><span class="tag">판서 정정 <b>f = 1100</b> · <b>d 빈도 16</b></span>'),
]) + '</div>'

def fstep(lb, fm, why='', cls=''):
    return f'<div class="st {cls}"><div class="lb">{lb}</div><div class="fm">{fm}</div><div class="why">{why}</div></div>'
DN = '<div class="dn">↓</div>'
FLOW = '<div class="unit c-purple"><div class="mlab"><span class="pri">★★★</span>Huffman 최적성 증명 — 기말 확정, 이 순서 그대로</div><div class="flow">' + DN.join([
  fstep('목표', f'허프만 트리 {T} = 최적', 'cost 최소인 decode tree 중 하나', 'hd2'),
  fstep('보조 1', f'최소 빈도 {v("x")}, {v("y")} 를<br><b>가장 깊은 형제</b>로 갖는 최적 트리 존재', f'귀류 · 가장 깊은 {v("a")} 와 {v("x")} 교환<br>({f_("x")} − {f_("a")})({d_("T", "x")} − {d_("T", "a")}) ≥ 0<br>→ {T}′ 도 최적 <b style="color:#C0341D">(판서 정정)</b>'),
  fstep('보조 2', f'cost({v("B")}) − cost({v("B")}′) = {f_("u")} + {f_("v")}', f'형제 {v("u")}, {v("v")} → 부모 {v("w")}<br>{d_("B′", "w")} = {d_("B", "u")} − 1 <b style="color:#C0341D">(판서 정정)</b>'),
  fstep('귀납', f'① {n} = 2 자명 &nbsp;② {n} &lt; {v("k")} 최적 &nbsp;③ {n} = {v("k")}', '② 는 증명할 필요 없는 가정'),
  fstep('③ 준비', f'cost({T}′) = cost({T}) − {f_("x")} − {f_("y")}', f'{T}′ = {T} 의 {v("x")}, {v("y")} 를 {v("z")} 로 (보조 2)'),
  fstep('③ 귀류', f'cost({T}″) &lt; cost({T}) 라 하면<br>cost({T}″ − {{x, y}}) &lt; cost({T}′)', f'보조 1 로 {T}″ 의 가장 깊은 형제 = 최소 빈도 {v("x")}, {v("y")}'),
  fstep('모순', f'{T}′ 은 ② 로 최적인데 더 작은 트리 존재 → {T} 최적', '', 'x'),
]) + '</div>' + f"""<div class="mini">
<div class="bx"><b class="t">귀류법 첫 줄 (모든 그리디 증명)</b>"그리디 전략으로 구한 해는 <b>최적이 아니다</b>" → 하나 더 많은 해가 있다</div>
<div class="bx"><b class="t">짧게 묻는 것</b>prefix-free = 어떤 코드도 다른 코드의 <b>앞부분이 아님</b><br>이진 트리면 자동: 문자는 <b>리프에만</b><br>최적 허프만 트리는 <b>여러 개</b> 가능</div>
</div></div>"""

GREEDY = [CARDS, FLOW]

build_memorize(OUT, title='알고리즘 기말 암기노트', subject='알고리즘 기말', h1='알고리즘 암기노트', h1_en='기말',
               ranges=[('그리디 Greedy', '9-2 ~ 10-2', '2 ~ 15', GREEDY)], pdf='final.pdf')
print('ok', OUT)
