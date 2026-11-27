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
# 그림: viewBox 폭 300 = 카드 안쪽 폭(약 79mm) → 1 단위 ≈ 1px, 글자는 11.3px(8.5pt) · 12.7px(9.5pt) 두 가지만
F85, F95 = 11.3, 12.7
def svg_coins():
    cs = [100, 100, 100, 50, 10] + [1] * 8; x = 2; o = ['<svg viewBox="0 0 300 34"><title>368원 = 100 × 3 + 50 + 10 + 1 × 8</title>']
    for c_ in cs:
        r = {100: 14, 50: 12, 10: 11, 1: 8}[c_]
        fs = F85 if c_ > 1 else 10
        o.append(f'<circle cx="{x + r}" cy="17" r="{r}" fill="#E7F5EC" stroke="#15803D" stroke-width="1.4"/><text x="{x + r}" y="{17 + fs * .36}" font-size="{fs}" font-weight="800" text-anchor="middle" fill="#15803D">{c_}</text>')
        x += 2 * r + 3
    o.append('</svg>'); return ''.join(o)
def svg_jobs():
    U = 26; X0 = 4; o = ['<svg viewBox="0 0 300 50"><title>1 + 2 + 3 = 6, +4 = 10 &gt; 9</title>']; x = X0
    for t in (1, 2, 3):
        o.append(f'<rect x="{x}" y="10" width="{t * U}" height="22" fill="#FDEEE6" stroke="#C2410C" stroke-width="1.4"/><text x="{x + t * U / 2}" y="{21 + F95 * .36}" font-size="{F95}" font-weight="800" text-anchor="middle" fill="#C2410C">{t}</text>'); x += t * U
    o.append(f'<rect x="{x}" y="10" width="{4 * U}" height="22" fill="#fff" stroke="#888" stroke-width="1.2" stroke-dasharray="4 3"/><text x="{x + 2 * U}" y="{21 + F85 * .36}" font-size="{F85}" font-weight="700" text-anchor="middle" fill="#666">+4 = 10</text>')
    tx = X0 + 9 * U
    o.append(f'<line x1="{tx}" y1="4" x2="{tx}" y2="38" stroke="#111" stroke-width="2.2"/><text x="{tx}" y="48" font-size="{F85}" font-weight="800" text-anchor="middle">T = 9</text></svg>')
    return ''.join(o)
def svg_iv():
    U = 20.5; X0 = 7; o = ['<svg viewBox="0 0 300 70"><title>0, 3, 7, 10 선택</title>']
    sel = (0, 3, 7, 10); lay = [[], [], []]
    for i, (s_, f_2) in enumerate(zip(S, F)):
        if i in sel: continue
        for row in lay:
            if all(f2 <= s_ or f_2 <= s2 for s2, f2 in row): row.append((s_, f_2)); break
    for li, row in enumerate(lay):
        for s_, f_2 in row: o.append(f'<rect x="{X0 + s_ * U}" y="{2 + li * 9}" width="{(f_2 - s_) * U}" height="7" fill="#EEF0F4" stroke="#B5BAC4" stroke-width=".8"/>')
    for i in sel:
        o.append(f'<rect x="{X0 + S[i] * U}" y="31" width="{(F[i] - S[i]) * U}" height="17" fill="#1D4ED8"/><text x="{X0 + (S[i] + F[i]) / 2 * U}" y="{39.5 + F85 * .36}" font-size="{F85}" font-weight="800" text-anchor="middle" fill="#fff">{i}</text>')
    o.append(f'<line x1="{X0}" y1="52" x2="{X0 + 14 * U}" y2="52" stroke="#111" stroke-width="1.2"/>')
    for t in (0, 4, 7, 11, 14): o.append(f'<text x="{X0 + t * U}" y="66" font-size="{F85}" text-anchor="middle" fill="#333">{t}</text>')
    o.append('</svg>'); return ''.join(o)
def svg_tree():
    N = {'r': (110, 10, 0), 'a': (40, 40, 1), 'n57': (180, 40, 0), 'n25': (130, 72, 0), 'n32': (232, 72, 0),
         'c': (100, 104, 1), 'b': (160, 104, 1), 'n16': (208, 104, 0), 'd': (268, 104, 1), 'f': (176, 136, 1), 'e': (240, 136, 1)}
    E = [('r', 'a', 0), ('r', 'n57', 1), ('n57', 'n25', 0), ('n57', 'n32', 1), ('n25', 'c', 0), ('n25', 'b', 1), ('n32', 'n16', 0), ('n32', 'd', 1), ('n16', 'f', 0), ('n16', 'e', 1)]
    o = ['<svg viewBox="0 0 300 150"><title>허프만 트리</title>']
    for p_, c_, bit in E:
        (x1, y1), (x2, y2) = N[p_][:2], N[c_][:2]
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#7E22CE" stroke-width="1.3"/><text x="{(x1 + x2) / 2 + (-8 if bit == 0 else 8)}" y="{(y1 + y2) / 2 + 3}" font-size="{F85}" font-weight="800" text-anchor="middle" fill="#7E22CE">{bit}</text>')
    for k_, (x, y, leaf) in N.items():
        if leaf:
            lab = f'{k_} = {HCODE[k_]}'
            o.append(f'<rect x="{x - 27}" y="{y - 10}" width="54" height="20" rx="4" fill="#F3E9FB" stroke="#7E22CE" stroke-width="1.3"/><text x="{x}" y="{y + F85 * .36}" font-size="{F85}" font-weight="800" text-anchor="middle">{lab}</text>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#7E22CE" stroke-width="1.3"/>')
    o.append('</svg>'); return ''.join(o)

def chain(*items):
    out = []
    for i, it in enumerate(items):
        cls = 'bx x' if it.startswith('!') else 'bx'
        out.append(f'<span class="{cls}">{it.lstrip("!")}</span>')
        if i < len(items) - 1: out.append('<span class="ar">→</span>')
    return '<div class="chain">' + ''.join(out) + '</div>'
def card(color, name, time, strat, fig, res, ch, extra=''):
    badge = f'<span>{time}</span>' if time and time != '—' else ''
    return (f'<div class="card {color}"><div class="hd">{name}{badge}</div><div class="in">'
            f'<div class="st">{strat}</div>{fig}<div class="res">{res}</div>{ch}{extra}</div></div>')

CARDS = '<div class="unit cards">' + ''.join([
  card('c-green', '거스름돈', '—', '큰 단위부터', svg_coins(), '368원 → 13개',
       chain('작은 단위 = 큰 단위의 <b>약수</b>', '그때만 최적'),
       chain('!반례 {1, 5, 7} · 10원', '!그리디 4개 vs 최적 2개')),
  card('c-orange', '일의 개수', '—', '짧은 일부터', svg_jobs(), '[2, 1, 4, 6, 3], T = 9 → 3개',
       chain(f'{X} + {a(4)} &gt; {T} <small>멈춤</small>', f'{Y} + {b(4)} ≤ {T} <small>가정</small>', f'{X} ≤ {Y}, {a(4)} ≤ {b(4)} <small>가장 짧음</small>') + chain(f'!{X} + {a(4)} ≤ {T} ⇒ 모순')),
  card('c-blue', '강의실 배정', f'O({n} log {n})', '빨리 끝나는 것부터', svg_iv(), 'L = [0, 3, 7, 10] → 4개',
       chain(f'{a(1)} → 0', f'{sb("A", 1)} ⊂ {sb("G", 1)}', f'{a(2)}→3 … {a(4)}→10') + chain(f'!{a(5)} 남음', '!for 문이 놓칠 리 없음 ⇒ 모순'),
       '<div class="cd">L = <mark>[0]</mark>, k = <mark>0</mark>\nfor i in range(<mark>1</mark>, n):\n    if <mark>F[k] &lt;= S[i]</mark>:\n        L.append(i), <mark>k = i</mark></div><span class="tag">판서 정정: <b>A₁ ⊂ G₁</b> (방향 주의)</span>'),
  card('c-purple', 'Huffman 코딩', f'O({n} log {n})', '최소 빈도 2개 합침', svg_tree(), '300 → 230비트 <small>16 → 25 → 32 → 57 → 100</small>',
       chain(f'extract_min · insert O(log {n}) × {n} 번 = O({n} log {n})'),
       '<div class="cd">while <mark>len(T) &gt; 1</mark>:\n    x = <mark>extract_min</mark>(T); y = extract_min(T)\n    z = Node(left = x, right = y)\n    <mark>f(z) = f(x) + f(y)</mark>; <mark>insert</mark>(T, z)</div><span class="tag">판서 정정: <b>f = 1100</b> · <b>d 빈도 16</b></span>'),
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


fx, fy = f_('x'), f_('y')
def K(t): return f'<em class="key">{t}</em>'
def pick(no, q, rows, code=''):
    """rows = [(이름, 답, 작은 보충)] — 답의 핵심만 K() 로 빨갛게"""
    body = ''.join(f'<div class="l">{l}</div><div class="a">{a_}{f"<small>{sm}</small>" if sm else ""}</div>' for l, a_, sm in rows)
    cd = f'<div class="cd">{code}</div>' if code else ''
    return f'<div class="unit pick"><div class="no">{no:02d}</div><div><div class="q">{q}</div>{cd}<div class="rows">{body}</div></div></div>'
TOP = '<div class="unit"><p class="pnote"><span class="key">빨간 글씨</span> = 외울 답 (빨간 셀로판지로 가리면 빈칸 문제)</p></div>'
PICKS = [
 pick(1, 'Huffman 코딩이 항상 최적임을 증명', [
   ('보조 1', f'최소 빈도 {v("x")}, {v("y")} 가 {K("가장 깊은 형제")}인 최적 트리 존재', f'{v("x")} ↔ 가장 깊은 {v("a")} 교환: ({f_("x")} − {f_("a")})({d_("T","x")} − {d_("T","a")}) ≥ 0'),
   ('교환 결과', f'{T}′ 도 {K("최적")} (비용이 늘지 않으므로)', ''),
   ('보조 2', K(f'cost({v("B")}) − cost({v("B")}′) = {f_("u")} + {f_("v")}'), f'형제 {v("u")}, {v("v")} → 부모 {v("w")}'),
   ('부모 깊이', K(f'{d_("B′","w")} = {d_("B","u")} − 1'), ''),
   ('귀납', f'{n} = 2 {K("자명")} → {n} &lt; {v("k")} {K("가정")} → {n} = {v("k")} 증명', ''),
   ('n = k', f'cost({T}′) = cost({T}) − {fx} − {fy}', f'{T}′ = {T} 의 {v("x")}, {v("y")} 를 합친 트리'),
   ('모순', K(f'cost({T}″ − {{x, y}}) &lt; cost({T}′)'), f'{T}′ 은 귀납 가정으로 최적인데 더 작은 트리가 있음'),
 ]),
 pick(2, '허프만 트리 · 코드 · 전체 비트 수', [
   ('합치기', f'{K("빈도가 가장 작은 두 개")}를 합침, 새 빈도 = {K("합")}', ''),
   ('코드', f'왼쪽 {K("0")}, 오른쪽 {K("1")}, 루트 → 리프 경로', ''),
   ('비트 수', K('Σ 빈도 × 깊이'), '고정 길이 = 문자 수를 표현하는 비트 × 총 빈도'),
   ('예시', f'a43 b13 c12 {K("d16")} e9 f7 → f {K("1100")} · e 1101 · c 100 · b 101 · d 111 · a 0 → {K("230")} (고정 300)', '합치는 순서 16 → 25 → 32 → 57 → 100'),
 ]),
 pick(3, '허프만 의사코드 빈칸 · 수행시간', [
   ('힙 연산', K(f'O(log {n})'), 'extract_min, insert (min heap 높이)'),
   ('전체', K(nlogn), f'{n} 번 반복'),
 ], code=f"""while {K('len(T) &gt; 1')}:
    x = {K('extract_min')}(T);  y = extract_min(T)
    z = Node(left = x, right = y)
    {K('f(z) = f(x) + f(y)')};  {K('insert')}(T, z)"""),
 pick(4, '강의실 배정 — 결과 구하기', [
   ('정렬', K('끝나는 시간 F 오름차순'), ''),
   ('선택', f'{K("F[k] ≤ S[i]")} 이면 선택, k = i', ''),
   ('예시', K('L = [0, 3, 7, 10]'), '4개'),
 ]),
 pick(5, '강의실 배정 — 최적성 증명', [
   ('가정', f'그리디 해는 {K("최적이 아니다")} → {a(1)} ~ {a(5)}', ''),
   ('바꿔치기', f'{K(f"{a(1)} → 0")}, {K(f"{sb("A",1)} ⊂ {sb("G",1)}")} → {a(2)}→3 … {a(4)}→10', '0번이 가장 먼저 끝남'),
   ('모순', f'{a(5)} 를 {K("for 문이 놓칠 리 없음")}', ''),
 ]),
 pick(6, '강의실 배정 — 빈칸 · 수행시간', [
   ('전체', K(nlogn), f'정렬 {nlogn} + for 문 O({n})'),
 ], code=f"""L = {K('[0]')}, k = {K('0')}
for i in range({K('1')}, n):
    if {K('F[k] &lt;= S[i]')}:
        L.append(i), {K('k = i')}"""),
 pick(7, '짧은 일부터 — 최적성 증명', [
   ('멈춤', K(f'{X} + {a(4)} &gt; {T}'), ''),
   ('가정', K(f'{Y} + {b(4)} ≤ {T}'), f'4개 {b(1)} ~ {b(4)} 가능'),
   ('가장 짧음', K(f'{X} ≤ {Y}, {a(4)} ≤ {b(4)}'), ''),
   ('모순', f'{X} + {a(4)} ≤ {T}', ''),
 ]),
 pick(8, '큰 동전부터 — 항상 최적?', [
   ('조건', f'단위가 {K("약수 관계")}일 때만', ''),
   ('반례', f'{K("1, 5, 7원")} · 10원 → {K("4개 vs 2개")}', '7 + 1 + 1 + 1 / 5 + 5'),
 ]),
 pick(9, 'prefix-free code', [
   ('정의', f'어떤 코드도 다른 코드의 {K("앞부분이 아님")}', ''),
   ('이진 트리', f'문자는 {K("리프에만")} → 자동 만족', ''),
   ('반례', '0, 00 → 00 = aa? c?', ''),
 ]),
]
GREEDY = PICKS


# ── 백트래킹 (11-1 ~ 13-1) ──
BT = [
 pick(1, '0/1 Knapsack — 한계함수 (가지를 볼까?)', [
   ('MP', f'지금까지 찾은 답 중 {K("최대 가치")}', ''),
   ('왼쪽 X[i] = 1', K('p(v) + P[i] + frac(i+1, K − s(v) − S[i])'), '남은 용량 K − s(v) − S[i]'),
   ('오른쪽 X[i] = 0', K('p(v) + frac(i+1, K − s(v))'), 'P[i] 를 더하지 않음'),
   ('안 감', f'상한 {K("≤ MP")}', '같아도 거름'),
   ('거르기 3', f'① {K("넘침")} ② 안 넣는 가지 ③ {K("fractional 상한 ≤ MP")} (가장 중요)', ''),
 ]),
 pick(2, '0/1 Knapsack 예시 추적 — P = [15, 16, 6], S = [3, 4, 2], K = 5', [
   ('[ ] → 1', f'15 + frac(1, 2) = 15 + {K("8")} = {K("23")}', '아이템 1 을 2/4 만큼'),
   ('[1] → 1', f'{K("4 > 남은 2")} → 넘침', ''),
   ('[1] → 0', f'15 + 6 = {K("21")} → [1, 0]', 's(v) 는 3 그대로'),
   ('[1,0] → 1', f'답, {K("MP = 21")}', ''),
   ('[1,0] → 0', f'15 + 0 = {K("15")} ≤ 21', ''),
   ('[ ] → 0', f'16 + 3 = {K("19")} ≤ 21', '19 는 상한 (답 아님)'),
   ('결과', K('[1, 0, 1], 21'), ''),
 ]),
 pick(3, 'knapsack 코드 빈칸', [
   ('끝', f'{K("i >= n or size == 0")} → update_best', ''),
   ('주의', f'안 넣는 가지는 {K("if S[i] <= size 밖")}', '안쪽이면 답 21 → 6'),
 ], code=f"""if {K('S[i] &lt;= size')}:
    B = frac_knapsack({K('i + 1')}, {K('size - S[i]')})
    if {K('profit + P[i] + B')} &gt; MP:
        X[i] = 1; knapsack(i+1, size-S[i], profit+P[i]); X[i] = 0
B = frac_knapsack(i + 1, {K('size')})
if {K('profit + B')} &gt; MP:
    X[i] = 0; knapsack(i+1, size, profit)"""),
 pick(4, 'fractional vs 0/1 Knapsack', [
   ('관계', K('fractional 최적 ≥ 0/1 최적'), '쪼개서 빈칸 없이 채움 → 상한으로 씀'),
   ('fractional', f'{K("가성비 P/S")} 순 그리디 → K = 16 예: {K("115")}', '2 + 5 + 9 (3번을 9/10)'),
   ('0/1', f'가성비 순 80 은 최적 아님 → {K("90")} (2 + 10), {K("백트래킹")}', ''),
 ]),
 pick(5, 'N-Queens — is_safe · 답', [
   ('X[k]', f'k 행 퀸의 {K("열")}', ''),
   ('같은 열', K('X[i] == c'), ''),
   ('대각선', K('|X[i] − c| == |i − k|'), '밑변 = 높이'),
   ('4-Queens', f'{K("[1, 3, 0, 2]")}, [2, 0, 3, 1]', '첫 해 = 앞의 것'),
 ]),
 pick(6, 'Subset Sum — 재귀 · DP · O(nS)', [
   ('끝', f'S == 0 → {K("True")}, S &lt; 0 or 원소 없음 → {K("False")}', ''),
   ('재귀', f'{K("넣음 (S − z)")} or 안 넣음 (S)', '경우 2<sup>n</sup>'),
   ('DP', K('DP[i][S] = DP[i−1][S−A[i]] or DP[i−1][S]'), ''),
   ('시간', f'{K("O(nS)")} — 입력의 {K("값")} S 가 들어가 바람직하지 않음', ''),
 ]),
 pick(7, 'Subset Sum — 답 구하기 · 가지치기', [
   ('sol', f'성공하면 {K("return [z] + result")}, 실패면 안 넣고', '불가능 None'),
   ('sol2', f'X[k] = 1 → k+1, X[k] = 0 → k+1, {K("k == n")} 에서 합 확인', '답 모두 출력'),
   ('가지치기', f'오름차순 + {K("current_sum + A[k] ≤ S")}', '호출 255 → 93'),
 ]),
 pick(8, '미로 find_way', [
   ('순서', f'{K("↓ 먼저")}, 안 되면 →', ''),
   ('구조', f'if 도착 · if safe · else 가 {K("같은 높이")}', '11-1 판서 정정'),
   ('4 × 4', f'(0,0) (1,0) {K("(1,1)")} (2,1) (3,1) (3,2) (3,3)', '0111 / 0010 / 1011 / 0000'),
 ]),
 pick(9, '일반형 · 한계함수 · SST', [
   ('일반형', f'for 후보 c: if {K("B(X[0], …, X[k−1], c)")} → X[k] = c, Backtrack(k+1)', ''),
   ('B', f'{K("한계함수")} — 조건 충돌 검사, 문제마다 다름', '잘 설계하면 효율 ↑'),
   ('SST', f'{K("State-Space Tree")} — 노드 = 상태', ''),
 ]),
]


build_memorize(OUT, title='알고리즘 기말 암기노트', subject='알고리즘 기말', h1='알고리즘 암기노트', h1_en='기말',
               ranges=[('그리디 Greedy', '9-2 ~ 10-2', '2 ~ 15', GREEDY), ('백트래킹 Backtracking', '11-1 ~ 13-1', '2 ~ 17', BT)], pdf='final.pdf')
print('ok', OUT)
