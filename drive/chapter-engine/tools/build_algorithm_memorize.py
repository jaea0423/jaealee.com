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

def munit(label, html): return f'<div class="unit"><div class="mlab">{label}</div>{html}</div>'
nb = lambda: '&nbsp;'
MATRIX = f"""<table class="mx"><colgroup><col style="width:17%"><col style="width:23%"><col style="width:25%"><col style="width:15%"><col style="width:20%"></colgroup>
<thead><tr><th>예제</th><th>전략</th><th>결과</th><th>시간</th><th>증명 열쇠</th></tr></thead><tbody>
<tr><td class="k">거스름돈</td><td class="big">큰 단위부터</td><td>368원 → <b>13개</b><small>반례 {{1, 5, 7}}, 10원: 4 vs 2</small></td><td>—</td><td>단위가 <b>약수 관계</b>일 때만 최적</td></tr>
<tr><td class="k">일의 개수</td><td class="big">짧은 일부터</td><td>[2, 1, 4, 6, 3], 9 → <b>3개</b></td><td>—</td><td>부등식 3개 충돌</td></tr>
<tr><td class="k">강의실 배정</td><td class="big">빨리 끝나는 것부터</td><td><b>L = [0, 3, 7, 10]</b></td><td><b>{nlogn}</b></td><td>바꿔치기 → {a(5)} 남음</td></tr>
<tr><td class="k">Huffman</td><td class="big">최소 빈도 2개 합침</td><td>300 → <b>230비트</b><small>16 → 25 → 32 → 57 → 100</small></td><td><b>{nlogn}</b><small>extract_min · insert O(log {n})</small></td><td>보조 1 · 2 + 귀납</td></tr>
</tbody></table>"""
KEYS = f"""<div class="keys">
<div class="kl">귀류법 틀</div><div class="kf">가정 "그리디 해는 <b>최적이 아니다</b>" → … → <span class="x">모순</span> → 최적</div>
<div class="kl">일의 개수</div><div class="kf">{X} + {a(4)} &gt; {T} &nbsp;·&nbsp; {Y} + {b(4)} ≤ {T} &nbsp;·&nbsp; {X} ≤ {Y}, {a(4)} ≤ {b(4)} &nbsp;⇒&nbsp; {X} + {a(4)} ≤ {T} <span class="x">모순</span><small>최적 아님 → 4개(k + 1 개)만 잡으면 충분</small></div>
<div class="kl">강의실 배정</div><div class="kf">{a(1)}→0, {a(2)}→3, {a(3)}→7, {a(4)}→10 &nbsp;⇒&nbsp; {a(5)} 남음 &nbsp;⇒&nbsp; for 문이 놓칠 리 없음 <span class="x">모순</span><small>{sb("A", 1)} ⊂ {sb("G", 1)} (a₁ 과 안 겹치면 0번과도 안 겹침)</small></div>
<div class="kl">허프만 보조 1</div><div class="kf">({f_("x")} − {f_("a")})({d_("T", "x")} − {d_("T", "a")}) ≥ 0 &nbsp;⇒&nbsp; 최소 빈도 {v("x")}, {v("y")} 가 <b>가장 깊은 형제</b>인 최적 트리 존재</div>
<div class="kl">허프만 보조 2</div><div class="kf">cost({v("B")}) − cost({v("B")}′) = {f_("u")} + {f_("v")}</div>
<div class="kl">허프만 귀납</div><div class="kf">{n} = 2 자명 → {n} &lt; {v("k")} 가정 → {n} = {v("k")}: cost({T}″ − {{x, y}}) &lt; cost({T}′) <span class="x">모순</span><small>{T}′ 은 귀납 가정으로 최적</small></div>
</div>"""
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
GREEDY = [
 munit('한눈에 — 전략 · 결과 · 시간', MATRIX),
 munit('증명 열쇠 — 서술형에 그대로 쓸 식', KEYS),
 f'<div class="unit mgrid"><div><div class="mlab">빈칸 나올 줄 (형광 부분)</div>{CODE}</div><div><div class="mlab">판서 정정 — 고친 값</div>{FIX}</div></div>',
]

build_memorize(OUT, title='알고리즘 기말 암기노트', subject='알고리즘 기말', h1='알고리즘 암기노트', h1_en='기말',
               ranges=[('그리디 Greedy', '9-2 ~ 10-2', '2 ~ 15', GREEDY)], pdf='final.pdf')
print('ok', OUT)
