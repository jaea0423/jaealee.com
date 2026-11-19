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
FREQ = dict(a=43, b=13, c=12, d=16, e=9, f=7); CODE = dict(a='0', b='101', c='100', d='111', e='1101', f='1100')
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
def munit(label, html, pri=''):
    p = f'<span class="pri">{pri}</span>' if pri else ''
    return f'<div class="unit"><div class="mlab">{p}{label}</div>{html}</div>'
def keys(rows):
    return '<div class="keys">' + ''.join(f'<div class="kl">{l}</div><div class="kf">{f}</div>' for l, f in rows) + '</div>'
def mtable(head, rows, widths):
    cg = ''.join(f'<col style="width:{w}">' for w in widths)
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td class="{"k" if i == 0 else ""}">{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<table class="mx"><colgroup>{cg}</colgroup><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
X_ = 'x'
fx, fy, fa, fu, fv = f_('x'), f_('y'), f_('a'), f_('u'), f_('v')
HUFF_PROOF = keys([
  ('목표', f'허프만 트리 {T} 는 <b>최적 decode tree</b> (cost 최소인 트리 중 하나)'),
  ('보조 1', f'최소 빈도 {v("x")}, {v("y")} 를 <b>가장 깊은 형제</b>로 갖는 최적 트리가 존재<small>귀류: 가장 깊은 {v("a")} 와 {v("x")} 교환 → cost({T}) − cost({T}′) = ({fx} − {fa})({d_("T", "x")} − {d_("T", "a")}) ≥ 0 → 비용 안 늘어남</small>'),
  ('보조 2', f'가장 깊은 형제 {v("u")}, {v("v")} 를 부모 {v("w")} 로 합치면 cost({v("B")}) − cost({v("B")}′) = <b>{fu} + {fv}</b><small>{d_("B", "v")} = {d_("B", "u")}, {d_("B′", "w")} = {d_("B", "u")} − 1, {f_("w")} = {fu} + {fv}</small>'),
  ('귀납', f'① {n} = 2 자명 &nbsp;② {n} &lt; {v("k")} 이면 최적 (가정) &nbsp;③ {n} = {v("k")} 증명'),
  ('③ 준비', f'{T}′ = {T} 의 {v("x")}, {v("y")} 를 {v("z")} 로 합친 트리 ({v("k")} − 1 개) → <b>cost({T}′) = cost({T}) − {fx} − {fy}</b> (보조 2)'),
  ('③ 귀류', f'{T} 최적 아님 → cost({T}″) &lt; cost({T}), 보조 1 로 {T}″ 의 가장 깊은 형제 = {v("x")}, {v("y")}<br>cost({T}″ − {{x, y}}) = cost({T}″) − {fx} − {fy} <b>&lt; cost({T}′)</b> ↔ {T}′ 은 ② 로 최적 <span class="x">모순</span>'),
])
TRACE = mtable(['문제 유형', '외울 절차', '예시로 확인'], [
  ['허프만 트리 · 코드', f'<b>최소 빈도 2개 합침</b> 반복 ({n} − 1 번) → 왼쪽 0, 오른쪽 1 → 리프까지 경로 = 코드', 'f7 e9 → 16, c12 b13 → 25, 16 d16 → 32, 57, 100'],
  ['비트 수 계산', f'cost = <b>Σ 빈도 × 깊이</b> / 고정 길이 = 문자 종류를 표현할 비트 × 총 빈도', '230비트 vs 3 × 100 = 300비트'],
  ['강의실 추적', '<b>F 오름차순</b> → 0번 선택 → <b>F[k] ≤ S[i]</b> 이면 선택, k = i', 'L = [0, 3, 7, 10] (4개)'],
  ['일의 개수', '<b>짧은 것부터</b> 누적 합이 T 를 넘기 직전까지', '[2, 1, 4, 6, 3], 9 → 1 + 2 + 3 → 3개'],
  ['거스름돈', '<b>큰 단위부터</b> / 반례: 작은 단위가 큰 단위의 약수가 아니게', '{1, 5, 7}, 10원 → 4개 vs 2개'],
], ['20%', '48%', '32%'])
TIME = mtable(['대상', '시간', '이유 (쓰라고 하면)'], [
  ['강의실 배정', f'<b>{nlogn}</b>', f'정렬 {nlogn} 이 지배, for 문은 O({n})'],
  ['extract_min · insert', f'<b>O(log {n})</b>', 'min heap 높이 = log n (heapify_down / up)'],
  ['Huffman 전체', f'<b>{nlogn}</b>', f'while 약 {n} 번 × O(log {n})'],
], ['26%', '22%', '52%'])
OTHER_PROOF = keys([
  ('첫 줄 (공통)', '가정: "그리디 전략으로 구한 해는 <b>최적이 아니다</b>" → 하나 더 많은 해가 있다'),
  ('강의실', f'{a(1)}→0 (0번이 가장 먼저 끝남) · {sb("A", 1)} ⊂ {sb("G", 1)} · {a(2)}→3 … {a(4)}→10 ⇒ {a(5)} 남음 ⇒ for 문이 다 훑으므로 놓칠 수 없음 <span class="x">모순</span>'),
  ('일의 개수', f'{X} + {a(4)} &gt; {T} (멈춤) · {Y} + {b(4)} ≤ {T} (가정) · {X} ≤ {Y}, {a(4)} ≤ {b(4)} (가장 짧음) ⇒ {X} + {a(4)} ≤ {T} <span class="x">모순</span>'),
])
CONCEPT = mtable(['물으면', '답'], [
  ['prefix-free 판정', '어떤 코드가 다른 코드의 <b>앞부분</b>이면 아님 (예: 0, 00 → 00 = aa? c?)'],
  ['이진 트리 → prefix-free 인 이유', '문자는 <b>리프에만</b> → 경로 중간에 다른 문자 없음'],
  ['강의실 1 · 2번 전략이 틀린 이유', '짧은 것부터: a 가 b, c 를 막음 / 빨리 시작: a 가 b, c, d 를 막음'],
  ['최적 허프만 트리는 하나?', '<b>아니다</b> (비용 같아도 모양 여러 개)'],
], ['38%', '62%'])
GREEDY = [
 munit('Huffman 최적성 증명 — 기말 확정, 순서와 이유까지', HUFF_PROOF, '★★★'),
 munit('동작 추적 · 계산 — 주어진 값으로 결과 구하기', TRACE, '★★★'),
 munit('시간복잡도', TIME, '★★'),
 munit('강의실 · 일의 개수 증명 — 귀류법 열쇠', OTHER_PROOF, '★★'),
 f'<div class="unit mgrid"><div><div class="mlab"><span class="pri">★★</span>빈칸 나올 줄 (형광 부분)</div>{CODE}</div><div><div class="mlab"><span class="pri">★</span>판서 정정 — 고친 값</div>{FIX}</div></div>',
 munit('개념 판정 — 짧게 묻는 것', CONCEPT, '★'),
]

build_memorize(OUT, title='알고리즘 기말 암기노트', subject='알고리즘 기말', h1='알고리즘 암기노트', h1_en='기말',
               ranges=[('그리디 Greedy', '9-2 ~ 10-2', '2 ~ 15', GREEDY)], pdf='final.pdf')
print('ok', OUT)
