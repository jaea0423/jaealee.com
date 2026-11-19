# 그리디 문제지 6개 생성 — greedy-0 (기초 OX) / greedy-1a·1b·1c (기본 1·2·3회) / greedy-2 (응용) / greedy-3 (심화)
# 모든 계산 값은 gx_core 로 구해서 넣고 assert 로 확인한다.
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gx_core import *

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
def Bk(a, *alt): return {'a': a, 'alt': list(alt)} if alt else {'a': a}
def sub(x, i): return f'{x}<sub>{i}</sub>'
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def pre(s): return '<pre>' + esc(s.strip('\n')) + '</pre>'
def ctab(head, rows):  # 문제 안에 넣는 작은 표 (주어진 값)
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in rows)
    return f'<table class="given" style="border-collapse:collapse;margin:6px 0;font-size:inherit"><tr>{h}</tr>{b}</table>'.replace('<th>', '<th style="border:1px solid #999;padding:2px 7px">').replace('<td>', '<td style="border:1px solid #999;padding:2px 7px;text-align:center">')

# 출처
SRC = {
 'greedy': ['09-2', 's2', '그리디 방법'], 'coin': ['09-2', 's3', '거스름돈'], 'coinwhy': ['09-2', 's4', '항상 최적인 이유'],
 'coinbad': ['09-2', 's5', '1원 · 5원 · 7원'], 'order': ['09-2', 's6', '그리디로 푸는 순서'], 'job': ['09-2', 's7', '일의 개수'],
 'contra': ['09-2', 's8', '귀류법'], 'jobpf': ['09-2', 's9', '일의 개수 증명'],
 'room': ['10-1', 's1', '강의실 배정'], 'room4': ['10-1', 's3', '최적 답 4개'], 'cand': ['10-1', 's4', '전략 후보 4가지'],
 'roomalg': ['10-1', 's5', '4번 전략 알고리즘'], 'roomex': ['10-1', 's6', '예시에 적용'], 'roompf': ['10-1', 's7', '강의실 증명'],
 'fixed': ['10-1', 's8', '고정 길이 코드'], 'var': ['10-1', 's9', '가변 길이 코드'], 'pfree': ['10-1', 's10', 'prefix-free'],
 'btree': ['10-1', 's11', '이진 트리'], 'cost': ['10-1', 's12', 'cost(T)'], 'hstr': ['10-1', 's13', '두 개씩 묶기'],
 'hdraw': ['10-1', 's14', '트리 그리기'], 'hcode': ['10-2', 's3', '허프만 의사코드'], 'heap': ['10-2', 's4', 'extract_min · insert'],
 'htime': ['10-2', 's5', '수행시간'], 'hgoal': ['10-2', 's6', '증명하려는 것'], 'lem1': ['10-2', 's7', '보조 명제 1'],
 'ind': ['10-2', 's8', '귀납법의 틀'], 'lem2': ['10-2', 's9', '보조 명제 2'], 'step3': ['10-2', 's10', '귀납 3단계'],
}
def src(*k): return [SRC[x] for x in k]

def huff_tab(freq, merges):
    return [[str(i + 1), Bk(f'{name(x)}, {name(y)}', f'{name(x)},{name(y)}', f'{name(y)}, {name(x)}'), Bk(str(s))] for i, (x, y, s) in enumerate(merges)]
def merges_txt(merges):
    return ' → '.join(f'{name(x)} + {name(y)} = {s}' for x, y, s in merges)
def code_rows(freq, code):
    return [[ch, str(freq[ch]), Bk(code[ch]), Bk(str(len(code[ch])))] for ch in sorted(freq)]
RULE = '묶을 때 <b>먼저 꺼낸(더 작은) 노드를 왼쪽(0)</b>, 나중에 꺼낸 노드를 오른쪽(1)에 둔다. 빈도가 같으면 <b>새로 만든 노드를 먼저</b> 꺼낸다.'

def page(slug, title, level, scope, exam, written='2026년 11월 19일 작성'):
    assert sum(q['pts'] for q in exam) == 100, (slug, sum(q['pts'] for q in exam))
    for q in exam:
        if 'rubric' in q: assert sum(r[1] for r in q['rubric']) == q['pts'], (slug, q['q'][:40])
        if q['type'] == 'table': assert all(len(r) == len(q['head']) for r in q['rows']), (slug, q['q'][:40])
    meta = dict(org='Kangwon National University CSE', subject='알고리즘', title=title, written=written,
                slug=f'algorithm-{slug}', lectureBase='../lecture', level=level, mcMax=1, scope=scope)
    body = ',\n\n'.join(json.dumps(q, ensure_ascii=False) for q in exam)
    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>알고리즘 {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&family=Nanum+Gothic:wght@400;700;800&family=Nanum+Gothic+Coding&family=Nanum+Pen+Script&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../exam-engine/exam.css">
<style>:root{{ --subject:#4F46E5; }}  /* 과목 색 — 이 한 줄만 과목마다 다르다 */</style>
<script src="../../exam-engine/exam.js"></script>
</head>
<body>
<div id="engineMissing" style="max-width:560px;margin:60px auto;padding:18px 20px;border:1.5px solid #141414;background:#fff;font:14px/1.7 sans-serif">
시험지 엔진을 불러오지 못했습니다.<br>이 파일은 <b>drive/exam-engine/exam.css · exam.js</b> 와 함께 있어야 열립니다.
(<code>drive/algorithm/exam/{slug}.html</code> 위치에서 열어 주세요.)</div>
<script>
/* ════════ 시험지 정보 ════════ */
const META = {json.dumps(meta, ensure_ascii=False, indent=2)};

/* ════════ 문항 ════════
   type  : mc 객관식 · ox O/X · short 단답 · table 표 빈칸 · line 코드 줄 고르기 · essay 서술
   생성  : exam/gen/gen_greedy_exam.py — 계산 값은 gx_core.py 에서 assert 로 검증
   채점  : 엔진은 채점하지 않음. 문항마다 「정답 · 해설」을 펼쳐 스스로 확인 — rubric 은 [기준, 점수] (부분 점수) */
const EXAM = [
{body}
];
</script>
</body>
</html>
'''
    open(f'{OUT}/{slug}.html', 'w').write(html)
    print('ok', slug, len(exam), '문항')

# ════════════════ 공통 값 (수업) ════════════════
LS = [1, 3, 0, 5, 3, 5, 6, 8, 8, 2, 12]; LF = list(range(4, 15))
LL, LTR = assign(LS, LF); assert LL == [0, 3, 7, 10] and best_count(LS, LF) == 4
HF = dict(a=43, b=13, c=12, d=16, e=9, f=7); HT, HM = huffman(HF); HC = codes(HT)
assert HC == dict(a='0', b='101', c='100', d='111', e='1101', f='1100') and cost(HF, HC) == 230
JA, JT = [2, 1, 4, 6, 3], 9; assert jobs(JA, JT) == [1, 2, 3]
ROOM_CODE = '''
1. F 값의 오름차순으로 정렬
2. L = [0], k = 0
3. for i in range(1, n):
       if F[k] <= S[i]:
           L.append(i), k = i
4. return L'''
HUFF_CODE = '''
def Huffman(T):
    while len(T) > 1:
        x = extract_min(T)
        y = extract_min(T)
        z = Node(left = x, right = y)
        f(z) = f(x) + f(y)
        insert(T, z)
    return T'''
def room_given(S, F, Sn='S', Fn='F', idx='i'):
    return ctab([idx] + [str(i) for i in range(len(S))], [[Sn] + [str(x) for x in S], [Fn] + [str(x) for x in F]])
def trace_exp(tr, S, F, Sn='S', Fn='F', i='i'):
    out = [f'시작: 0번 (끝 {F[0]})']
    for (t, st, k, fk, ok) in tr:
        if ok: out.append(f'{i} = {t}: {Sn}[{t}] = {st} ≥ {fk} → {t}번 배정 (끝 {F[t]})')
    return ' → '.join(out)
def trace_rows(tr, sel='배정'):
    return [[str(i), str(s), Bk(str(fk)), Bk('O' if ok else 'X', 'o' if ok else 'x')] for (i, s, k, fk, ok) in tr]

# ════════════════ greedy-0 기초 OX ════════════════
def OX(unit, pts, q, items, s):
    KOR = 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊ'
    return dict(type='ox', lv='기초', unit=unit, pts=pts, q=f'<p>{q} 각 문장이 맞으면 O, 틀리면 X 를 고르시오.</p>', items=[[a, b] for a, b, _ in items],
                exp='<br>'.join(f'<b>{KOR[i]} ({"O" if b else "X"})</b> {e}' for i, (_, b, e) in enumerate(items)), src=s)

G0 = [
OX('그리디 개념', 15, '그리디 방법과 귀류법에 대한 설명이다.', [
 ('그리디 방법은 현재 상태에서 가장 좋은 선택을 반복해서 답을 구성한다.', True, '"현재 상태에서 가장 좋은(탐욕스러운) 선택"을 반복한다.'),
 ('그리디 방법은 앞의 선택이 나빴다는 것을 알면 되돌아가서 다시 고른다.', False, '그리디는 선택을 되돌리지 않는다. 그래서 최적이라는 증명이 따로 필요하다.'),
 ('그리디 전략으로 구한 답은 항상 최적 해이다.', False, '1원 · 5원 · 7원 거스름돈처럼 틀리는 경우가 있다. 항상 최적임을 증명해야 그 방법이 최적이라고 말할 수 있다.'),
 ('작은 문제의 답을 테이블에 저장해 두고 다시 쓰는 것은 분할 정복의 특징이다.', False, '동적 계획법(DP)의 특징. 분할 정복은 저장하지 않고 다시 호출한다.'),
 ('귀류법은 결론을 부정해서 모순이 생김을 보이고, 그래서 결론이 참임을 보이는 방법이다.', True, '결론 부정(가정) → 전개 → 모순 → 가정이 틀림 → 결론 참.'),
 ('그리디 전략의 최적성을 귀류법으로 증명할 때, 가정은 "그리디 전략으로 구한 해는 최적 해가 아니다"이다.', True, '"P 이면 Q" 에서 Q(최적이다)만 부정한다.'),
 ('그리디 증명에서는 "이 전략으로 답을 구했다"는 부분도 함께 부정해서 가정한다.', False, '전략(P)은 그대로 두고 결론(Q)만 부정한다. 전략까지 부정하면 다른 명제가 된다.'),
], src('greedy', 'order', 'contra')),
OX('거스름돈', 15, '동전 1원 · 10원 · 50원 · 100원으로 거스름돈을 줄 때 동전 개수를 최소로 하는 문제이다.', [
 ('전략은 가장 큰 단위의 동전부터 거슬러 주는 것이다.', True, '남은 금액에 대해 큰 단위부터.'),
 ('368원을 이 전략으로 거슬러 주면 동전은 모두 13개이다.', True, '100원 3 + 50원 1 + 10원 1 + 1원 8 = 13.'),
 ('368원을 거슬러 줄 때 50원 동전은 2개 쓴다.', False, '100원 3개 뒤 남은 68원에서 50원은 1개.'),
 ('이 동전에서 전략이 최적인 이유는 작은 단위들이 큰 단위의 약수이기 때문이다.', True, '1, 10, 50 은 100 의 약수, 1, 10 은 50 의 약수 → 큰 동전 1개를 작은 동전 1개보다 적게 만들 수 없다.'),
 ('동전이 1원 · 5원 · 7원일 때 10원을 이 전략으로 거슬러 주면 2개이다.', False, '7 + 1 + 1 + 1 → 4개.'),
 ('동전이 1원 · 5원 · 7원일 때 10원의 최적 답은 5원 2개이다.', True, '2개.'),
 ('동전 단위가 어떻게 주어지든 큰 단위부터 고르면 최적이다.', False, '1 · 5 · 7 처럼 작은 단위가 큰 단위의 약수가 아니면 틀릴 수 있다.'),
], src('coin', 'coinwhy', 'coinbad')),
OX('일의 개수', 15, f'일 5개의 소요시간 A = [2, 1, 4, 6, 3], 하루에 일하는 시간 T = 9 일 때 할 수 있는 일의 개수를 최대로 하는 문제이다.', [
 ('전략은 소요시간이 적은 일부터 하는 것이다.', True, '개수를 최대로 해야 하므로 짧은 것부터.'),
 ('최적 답은 3개이다.', True, '1 + 2 + 3 = 6, 여기에 4 를 더하면 10 &gt; 9.'),
 ('이 문제는 하루 9시간을 최대한 꽉 채우는 일의 조합을 찾는 문제이다.', False, '시간이 아니라 일의 <b>개수</b>가 중요하다. 1 + 3 + 4 = 8 도 3개.'),
 (f'귀류법에서 최적 해를 {sub("b",1)} ~ {sub("b",4)} 4개로 잡는 것은, 5개 이상이어도 그중 4개를 떼어 내면 여전히 T 안에 들어가기 때문이다.', True, '4개로 모순을 보이면 그 이상도 모두 불가능하다.'),
 (f'증명에서 X = {sub("a",1)} + {sub("a",2)} + {sub("a",3)}, Y = {sub("b",1)} + {sub("b",2)} + {sub("b",3)} 일 때 X ≤ Y 이다.', True, f'{sub("a",1)}, {sub("a",2)}, {sub("a",3)} 은 가장 짧은 3개.'),
 (f'증명에서 {sub("a",4)} ≥ {sub("b",4)} 이다.', False, f'{sub("a",4)} 는 4번째로 작은 값이라 {sub("a",4)} ≤ {sub("b",4)}.'),
 (f'모순은 X + {sub("a",4)} ≤ T 와 X + {sub("a",4)} &gt; T 가 함께 성립하는 것이다.', True, f'⑤ X + {sub("a",4)} ≤ Y + {sub("b",4)} ≤ T 와 ① X + {sub("a",4)} &gt; T.'),
], src('job', 'jobpf')),
OX('강의실 배정', 20, '시작 시간 S, 끝 시간 F 가 주어진 강의를 한 강의실에 되도록 많이 배정하는 문제이다.', [
 ('목표는 배정하는 강의의 개수를 최대로 하는 것이다.', True, '어떤 강의인지보다 개수.'),
 ('빨리 시작하는 강의부터 배정하는 전략은 최적이다.', False, '긴 강의 a 가 가장 먼저 시작하면 b, c, d 3개를 놓친다 (반례).'),
 ('소요시간이 짧은 강의부터 배정하는 전략에는 반례가 있다.', True, '짧은 a 가 b, c 둘과 겹치면 1개만 고르게 된다.'),
 ('빨리 끝나는 강의부터 배정하는 전략이 최적이다.', True, '남은 시간을 가장 많이 남긴다. 귀류법으로 증명.'),
 ('알고리즘의 첫 단계는 S 값의 오름차순 정렬이다.', False, '<b>F</b> 값의 오름차순 정렬.'),
 ('for 문에서 F[k] ≤ S[i] 이면 i 번 강의를 배정하고 k = i 로 바꾼다.', True, 'k = 가장 최근에 배정한 강의.'),
 ('전체 수행시간은 for 문 하나뿐이므로 O(n) 이다.', False, '정렬 O(n log n) + for 문 O(n) → O(n log n).'),
 ('수업 예시(강의 11개)의 최적 답은 4개이고, 0, 3, 7, 10 말고도 4개를 고르는 다른 조합이 있다.', True, '1, 3, 7, 10 등.'),
], src('room', 'cand', 'roomalg', 'room4')),
OX('Huffman 코드', 20, '문자를 비트로 나타내는 코드와 Huffman 코딩에 대한 설명이다.', [
 ('ASCII 처럼 모든 문자를 같은 비트 수로 나타내는 코드는 고정 길이 코드이다.', True, '한 문자 8비트.'),
 ('문자가 6개이면 고정 길이로 한 문자에 3비트가 필요하다.', True, '2<sup>3</sup> = 8 ≥ 6.'),
 ('가변 길이 코드는 많이 나오는 문자에 많은 비트를 준다.', False, '많이 나오는 문자에 <b>적은</b> 비트.'),
 ('문자 4개에 0, 1, 00, 01 을 배정하면 prefix-free 가 아니다.', True, '0 이 00, 01 의 앞부분.'),
 ('decode tree 에서는 중간 노드에도 문자를 둘 수 있다.', False, '리프 노드만 문자.'),
 ('리프 노드에만 문자를 두면 prefix-free 가 자동으로 만족된다.', True, '한 리프로 가는 길은 다른 리프로 가는 길의 앞부분이 될 수 없다.'),
 ('cost(T) = Σ f(x) · d<sub>T</sub>(x) 에서 d<sub>T</sub>(x) 는 x 의 빈도수이다.', False, 'd<sub>T</sub>(x) 는 트리 T 에서 x 의 <b>깊이</b> (= 비트 수). 빈도수는 f(x).'),
 ('Huffman 전략은 빈도수가 가장 큰 두 개를 먼저 묶는다.', False, '가장 <b>적은</b> 두 개.'),
 ('cost 가 최소인 트리는 하나뿐이다.', False, '가지를 어디로 뻗느냐에 따라 여러 개일 수 있다 (cost 는 같다).'),
], src('fixed', 'var', 'pfree', 'btree', 'cost', 'hdraw')),
OX('Huffman 증명', 15, 'Huffman 의사코드의 수행시간과 최적성 증명에 대한 설명이다.', [
 ('extract_min 은 min heap 의 루트를 꺼내고 마지막 노드를 루트로 옮겨 heapify_down 한다.', True, '루트 = 가장 작은 노드.'),
 ('extract_min 과 insert 는 각각 O(log n) 이다.', True, '트리 높이 h = O(log n).'),
 ('문자가 n 개이면 while 문은 n − 1 번 반복되고 전체 수행시간은 O(n log n) 이다.', True, '묶을 때마다 노드가 1개 준다.'),
 ('보조 명제 1: 빈도수가 가장 작은 두 문자를 가장 깊은 곳에 형제로 갖는 최적 트리가 항상 존재한다.', True, '교환으로 증명.'),
 ('보조 명제 1 의 증명에서 x 와 a 를 바꾼 트리 T′ 은 비용이 늘어나므로 최적이 아니다.', False, 'cost(T) − cost(T′) ≥ 0 → 비용이 늘지 않으므로 T′ 도 최적.'),
 ('보조 명제 2: 가장 깊은 형제 u, v 를 부모 w 로 합치면 비용이 f(u) + f(v) 만큼 줄어든다.', True, 'cost(B) − cost(B′) = f(u) + f(v).'),
 ('본 증명은 문자 개수 n 에 대한 귀납법이고, 3단계(n = k) 안에서 귀류법을 쓴다.', True, '귀납법 안에 귀류법.'),
 ('귀납 가정은 "n = k − 1 일 때만 허프만 트리가 최적"이다.', False, '"n &lt; k 인 모든 경우" 최적이라고 가정한다.'),
], src('heap', 'htime', 'lem1', 'lem2', 'ind')),
]
page('greedy-0', 'E. 그리디 — 기초 OX', '기초', '9주차 2차시, 10주차 1·2차시 — 그리디 개념 · 귀류법 · 거스름돈 · 일의 개수 · 강의실 배정 · Huffman 코딩과 증명', G0)

# ════════════════ greedy-1a 기본 1회 — 수업 값 · 수업 기호 그대로 ════════════════
cg = coin_greedy([1, 10, 50, 100], 368)
G1A = [
dict(type='table', lv='하', unit='거스름돈', pts=8,
 q='<p>동전 1원, 10원, 50원, 100원으로 <b>368원</b>을 거슬러 준다. 가장 큰 단위 동전부터 거슬러 주는 그리디 전략을 쓸 때 표를 채우시오.</p>',
 head=['동전', '개수', '남은 금액'],
 rows=[['100원', Bk('3'), Bk('68')], ['50원', Bk('1'), Bk('18')], ['10원', Bk('1'), Bk('8')], ['1원', Bk('8'), Bk('0')], ['합계', Bk('13'), '']],
 exp='368 → 100원 3개 (68) → 50원 1개 (18) → 10원 1개 (8) → 1원 8개 (0). 모두 13개.', src=src('coin')),
dict(type='table', lv='하', unit='거스름돈', pts=6,
 q='<p>동전이 1원, 5원, 7원이고 거스름돈이 10원이다. 큰 단위부터 고르는 그리디 전략의 답과 최적 답의 동전 개수를 쓰시오.</p>',
 head=['방법', '동전', '개수'], rows=[['그리디', Bk('7원 1개 + 1원 3개', '7+1+1+1'), Bk('4')], ['최적', Bk('5원 2개', '5+5'), Bk('2')]],
 exp='그리디는 7원을 먼저 골라 남은 3원을 1원 3개로 → 4개. 5원 2개면 2개. 1원, 5원이 7원의 약수가 아니라서 틀린다.', src=src('coinbad')),
dict(type='short', lv='하', unit='일의 개수', pts=6,
 q='<p>일 5개의 소요시간이 A = [2, 1, 4, 6, 3] 이고 하루에 일하는 시간이 T = 9 이다. 소요시간이 적은 일부터 하는 그리디 전략으로 할 수 있는 일의 최대 개수를 쓰시오.</p>',
 show='3', alt=['3개'], exp='정렬 1, 2, 3, 4, 6 → 1 + 2 + 3 = 6, 여기에 4 를 더하면 10 &gt; 9 → 3개.', src=src('job')),
dict(type='table', lv='중', unit='강의실 배정', pts=12,
 q=f'<p>강의 11개가 F 오름차순으로 정렬되어 있다.</p>{room_given(LS, LF)}<p>수업 알고리즘으로 배정할 때, i = 1 부터 각 단계에서 비교하는 F[k] 값과 배정 여부(O/X)를 채우고 마지막 줄에 L 을 쓰시오.</p>',
 head=['i', 'S[i]', 'F[k]', '배정'], rows=trace_rows(LTR) + [['L', '', Bk('[0, 3, 7, 10]', '0,3,7,10', '0 3 7 10'), '']],
 exp='k = 0 (F = 4) 에서 시작. S[3] = 5 ≥ 4 → 3번 배정 (k = 3, F = 7). S[7] = 8 ≥ 7 → 7번 (F = 11). S[10] = 12 ≥ 11 → 10번. L = [0, 3, 7, 10], 4개.',
 src=src('roomex')),
dict(type='table', lv='하', unit='강의실 배정', pts=9,
 q='<p>빨리 끝나는 강의부터 배정하는 알고리즘이다. 빈칸 (가) ~ (다) 를 채우시오.</p>' + pre('''
1. (가) 값의 오름차순으로 정렬
2. L = [0], k = 0
3. for i in range(1, n):
       if (나):
           L.append(i), (다)
4. return L'''), head=['빈칸', '답'], rows=[['(가)', Bk('F')], ['(나)', Bk('F[k] <= S[i]', 'F[k]<=S[i]', 'S[i] >= F[k]')], ['(다)', Bk('k = i', 'k=i')]],
 exp='끝나는 시간 F 로 정렬. 가장 최근에 배정한 강의 k 가 끝난 뒤에(같아도 됨) 시작하면 배정하고 k 를 i 로 바꾼다.', src=src('roomalg')),
dict(type='essay', lv='하', unit='강의실 배정', pts=6,
 q='<p>5번 알고리즘의 1번 단계와 3번 단계의 시간복잡도를 각각 쓰고, 전체 시간복잡도를 쓰시오.</p>',
 model='1번 정렬 <b>O(n log n)</b>, 3번 for 문 <b>O(n)</b> → 전체 <b>O(n log n)</b> (큰 쪽).',
 rubric=[['정렬 O(n log n)', 2], ['for 문 O(n)', 2], ['전체 O(n log n)', 2]], src=src('roomalg')),
dict(type='table', lv='하', unit='Huffman', pts=10,
 q='<p>문자 a ~ f 의 빈도수가 a 43, b 13, c 12, d 16, e 9, f 7 이다. 빈도수가 가장 적은 두 개씩 묶는 순서를 채우시오. 묶은 노드는 두 빈도의 합으로 나타낸다.</p>',
 head=['단계', '묶는 두 개', '대표 빈도'], rows=huff_tab(HF, HM),
 exp=merges_txt(HM) + '. 묶은 노드(16)와 d(16)처럼 빈도가 같으면 둘 중 무엇을 먼저 묶어도 cost 는 같다.', src=src('hstr')),
dict(type='essay', lv='중', unit='Huffman', pts=12,
 q=f'<p>7번의 묶는 순서로 허프만 트리를 그리고, 각 문자의 코드를 쓰시오. {RULE}</p>',
 model=tree_svg(HT) + 'a = 0, b = 101, c = 100, d = 111, e = 1101, f = 1100',
 rubric=[['리프 6개가 모두 문자이고 묶은 순서대로 연결됨', 4], ['왼쪽 0 · 오른쪽 1 규칙대로 그림', 2], ['코드 6개 (하나 틀릴 때마다 −1, 최소 0)', 6]], src=src('hdraw', 'btree')),
dict(type='table', lv='하', unit='Huffman', pts=6,
 q='<p>8번의 코드로 문자 100개(빈도 합 100)를 나타낼 때 전체 비트 수와, 같은 문자들을 고정 길이 코드로 나타낼 때의 전체 비트 수를 쓰시오.</p>',
 head=['코드', '전체 비트 수'], rows=[['허프만 (가변 길이)', Bk('230')], ['고정 길이', Bk('300')]],
 exp='43 × 1 + (13 + 12 + 16) × 3 + (9 + 7) × 4 = 43 + 123 + 64 = 230. 고정 길이는 문자 6개 → 3비트 → 100 × 3 = 300.', src=src('var', 'cost')),
dict(type='table', lv='하', unit='Huffman', pts=9,
 q='<p>Huffman 의사코드의 빈칸 (가) ~ (라) 를 채우시오. f() 는 빈도수이다.</p>' + pre('''
def Huffman(T):
    while (가):
        x = extract_min(T)
        y = (나)
        z = Node(left = x, right = y)
        f(z) = (다)
        (라)
    return T'''), head=['빈칸', '답'],
 rows=[['(가)', Bk('len(T) > 1', 'len(T)>1')], ['(나)', Bk('extract_min(T)')], ['(다)', Bk('f(x) + f(y)', 'f(x)+f(y)')], ['(라)', Bk('insert(T, z)', 'insert(T,z)')]],
 exp='노드가 하나 남을 때까지 가장 작은 두 개 x, y 를 꺼내 부모 z 로 묶고, z 의 빈도를 두 빈도의 합으로 정한 뒤 다시 넣는다.', src=src('hcode')),
dict(type='table', lv='중', unit='일의 개수 증명', pts=8,
 q=f'<p>3번 문제의 그리디 해 {sub("a",1)}, {sub("a",2)}, {sub("a",3)} (그다음 짧은 일 {sub("a",4)}) 가 최적임을 귀류법으로 증명한다. X = {sub("a",1)} + {sub("a",2)} + {sub("a",3)}, Y = {sub("b",1)} + {sub("b",2)} + {sub("b",3)} 이다. 빈칸을 채우시오.</p>',
 head=['단계', '식 · 내용'],
 rows=[['가정', Bk(f'최적 해 b1 ~ b4 가 있다 (3개보다 많다)', 'b1~b4', '4개')], ['①', Bk('X + a4 > T', 'X+a4>T')], ['②', Bk('Y + b4 <= T', 'Y+b4<=T', 'Y + b4 ≤ T')],
       ['③', Bk('X <= Y', 'X ≤ Y')], ['④', Bk('a4 <= b4', 'a4 ≤ b4')], ['모순', Bk('X + a4 <= Y + b4 <= T 와 ① 이 충돌', 'X + a4 ≤ T')]],
 exp=f'① 그리디가 4번째를 못 넣음. ② {sub("b",1)} ~ {sub("b",4)} 는 가능한 해. ③ {sub("a",1)} ~ {sub("a",3)} 은 가장 짧은 3개. ④ {sub("a",4)} 는 4번째로 작은 값. ③ + ④ → X + {sub("a",4)} ≤ Y + {sub("b",4)} ≤ T 인데 ① 은 X + {sub("a",4)} &gt; T → 모순 → 가정이 틀림.',
 src=src('jobpf')),
dict(type='table', lv='중', unit='Huffman 증명', pts=8,
 q='<p>Huffman 코딩이 최적임을 보이는 증명의 뼈대이다. 빈칸을 채우시오.</p>',
 head=['항목', '빈칸', '답'],
 rows=[['보조 명제 1', '빈도수가 가장 (가) 두 문자를 가장 깊은 곳에 형제로 갖는 최적 트리가 존재한다', Bk('작은')],
       ['보조 명제 2', '가장 깊은 형제 u, v 를 부모 w 로 합치면 cost(B) − cost(B′) = (나)', Bk('f(u) + f(v)', 'f(u)+f(v)')],
       ['본 증명 바닥 조건', 'n = (다) 이면 허프만 트리는 최적', Bk('2')],
       ['본 증명 3단계', 'n = k 일 때 허프만 트리가 최적임을 (라) 으로 증명', Bk('귀류법')]],
 exp='문자 개수 n 에 대한 귀납법. 바닥 조건 n = 2 는 자명, 귀납 가정 n &lt; k, 3단계에서 "T 가 최적이 아니다"라고 가정해 모순을 보인다. 보조 명제 1 · 2 는 3단계 안에서 쓴다.', src=src('lem1', 'lem2', 'ind')),
]
page('greedy-1a', 'E. 그리디 — 기본 1회', '기본', '<b>그리디 · 기본 1회</b> (9주차 2차시 ~ 10주차 2차시)<br>수업 예시 값과 수업 기호 그대로 — 결과값 · 코드 빈칸 · 시간복잡도 · 트리 그리기 · 증명 뼈대', G1A)

# ════════════════ greedy-1b 기본 2회 — 새 값 · 수업 기호 ════════════════
cg2 = coin_greedy([1, 10, 50, 100], 437); assert cg2 == [(100, 4), (50, 0), (10, 3), (1, 7)]
assert coin_greedy([1, 4, 6], 8) == [(6, 1), (4, 0), (1, 2)] and coin_opt([1, 4, 6], 8) == 2
J2 = [3, 5, 1, 4, 2, 6]; assert jobs(J2, 10) == [1, 2, 3, 4]
S2 = [1, 2, 4, 1, 5, 8, 9, 11, 13]; F2 = [3, 5, 6, 7, 9, 10, 11, 14, 16]; L2, TR2 = assign(S2, F2); assert L2 == [0, 2, 5, 7] and best_count(S2, F2) == 4
HF2 = dict(a=15, b=8, c=25, d=5, e=30, f=7, g=10); HT2, HM2 = huffman(HF2); HC2 = codes(HT2); C2 = cost(HF2, HC2); assert C2 == 257
DEC = HC['f'] + HC['a'] + HC['c'] + HC['e'] + HC['d']  # 1100 0 100 1101 111
G1B = [
dict(type='table', lv='하', unit='거스름돈', pts=7,
 q='<p>동전 1원, 10원, 50원, 100원으로 <b>437원</b>을 큰 단위부터 거슬러 준다. 표를 채우시오.</p>',
 head=['동전', '개수'], rows=[['100원', Bk('4')], ['50원', Bk('0')], ['10원', Bk('3')], ['1원', Bk('7')], ['합계', Bk('14')]],
 exp='437 → 100원 4개 (37) → 50원은 37 &lt; 50 이라 0개 → 10원 3개 (7) → 1원 7개. 0개인 단위도 건너뛰지 않고 확인한다.', src=src('coin')),
dict(type='essay', lv='중', unit='거스름돈', pts=8,
 q='<p>동전이 1원, 4원, 6원이고 거스름돈이 8원이다.</p><p>(1) 큰 단위부터 고르는 그리디 전략의 답과 최적 답을 쓰시오.<br>(2) 1원 · 10원 · 50원 · 100원과 달리 이 동전에서 그리디가 틀리는 이유를 수업의 근거로 쓰시오.</p>',
 model='(1) 그리디: 6원 1개 + 1원 2개 = <b>3개</b>, 최적: 4원 2개 = <b>2개</b><br>(2) 1, 10, 50, 100 은 작은 단위가 큰 단위의 <b>약수</b>라서 큰 동전 1개를 작은 동전들로 1개보다 적게 만들 수 없다. 4 는 6 의 약수가 아니므로 이 근거가 성립하지 않는다.',
 rubric=[['그리디 3개 (6 + 1 + 1)', 2], ['최적 2개 (4 + 4)', 2], ['4 가 6 의 약수가 아니라는 이유', 4]], src=src('coinwhy', 'coinbad')),
dict(type='short', lv='하', unit='일의 개수', pts=6,
 q='<p>일 6개의 소요시간이 A = [3, 5, 1, 4, 2, 6] 이고 하루에 일하는 시간이 T = 10 이다. 소요시간이 적은 일부터 하는 전략으로 할 수 있는 일의 최대 개수를 쓰시오.</p>',
 show='4', alt=['4개'], exp='정렬 1, 2, 3, 4, 5, 6 → 1 + 2 + 3 + 4 = 10 ≤ 10 (같아도 가능) → 다음 5 를 더하면 15 &gt; 10 → 4개.', src=src('job')),
dict(type='table', lv='중', unit='강의실 배정', pts=12,
 q=f'<p>강의 9개가 F 오름차순으로 정렬되어 있다.</p>{room_given(S2, F2)}<p>빨리 끝나는 강의부터 배정할 때 i = 1 부터 표를 채우고, 마지막 줄에 L 을 쓰시오.</p>',
 head=['i', 'S[i]', 'F[k]', '배정'], rows=trace_rows(TR2) + [['L', '', Bk('[0, 2, 5, 7]', '0,2,5,7', '0 2 5 7'), '']],
 exp='0번(F = 3) → S[2] = 4 ≥ 3 → 2번(F = 6) → S[5] = 8 ≥ 6 → 5번(F = 10) → S[7] = 11 ≥ 10 → 7번(F = 14) → S[8] = 13 &lt; 14. L = [0, 2, 5, 7], 4개 (전수 조사로도 최대 4개).',
 src=src('roomex')),
dict(type='table', lv='중', unit='강의실 증명', pts=10,
 q=f'<p>4번에서 구한 해 (0, 2, 5, 7) 이 최적임을 수업 방식의 귀류법으로 증명한다. 빈칸을 채우시오.</p>',
 head=['단계', '내용', '답'],
 rows=[['가정', '(0, 2, 5, 7) 은 최적 해가 아니다 → 최적 해는 최소 (가) 개', Bk('5')],
       [f'{sub("a",1)} → 0', f'0번은 전체 중 가장 (나) 강의 → {sub("a",1)} 을 0 으로 바꿀 수 있다', Bk('빨리 끝나는', '먼저 끝나는')],
       ['집합', f'{sub("G",1)} = 0번과 겹치지 않는 강의, {sub("A",1)} = {sub("a",1)} 과 겹치지 않는 강의 → 포함 관계 (다)', Bk('A1 ⊂ G1', 'A₁ ⊂ G₁', 'A1⊂G1')],
       [f'{sub("a",2)} → 2', f'2번 = (라) 중 가장 빨리 끝나는 강의 → {sub("a",2)} 를 2 로 바꿀 수 있다', Bk('G1', 'G₁')],
       ['모순', f'(0, 2, 5, 7, {sub("a",5)}) 에서 7번보다 뒤에 시작하는 {sub("a",5)} 가 있다면 for 문이 (마)', Bk(f'a5 를 골랐어야 한다', 'a5를 골랐어야 함')]],
 exp=f'{sub("a",1)} 보다 앞에서 끝나는 강의는 없으므로 {sub("a",1)} 과 겹치지 않는 강의는 0번과도 겹치지 않는다 → {sub("A",1)} ⊂ {sub("G",1)}. 이 바꿔치기를 이어 가면 (0, 2, 5, 7, {sub("a",5)}). for 문은 모든 인덱스를 훑으므로 {sub("a",5)} 를 안 골랐을 수 없다 → 모순.',
 src=src('roompf')),
dict(type='table', lv='하', unit='Huffman', pts=10,
 q=f'<p>문자 a ~ g 의 빈도수가 a 15, b 8, c 25, d 5, e 30, f 7, g 10 이다. 빈도수가 가장 적은 두 개씩 묶는 순서를 채우시오.</p>',
 head=['단계', '묶는 두 개', '대표 빈도'], rows=huff_tab(HF2, HM2), exp=merges_txt(HM2) + '. 문자 7개 → 6번 묶는다 (n − 1 번).', src=src('hstr')),
dict(type='essay', lv='중', unit='Huffman', pts=12,
 q=f'<p>6번의 순서로 허프만 트리를 그리고 각 문자의 코드를 쓰시오. {RULE}</p>',
 model=tree_svg(HT2) + ', '.join(f'{c} = {HC2[c]}' for c in sorted(HC2)),
 rubric=[['묶은 순서대로 트리 구성', 4], ['왼쪽 0 · 오른쪽 1 규칙', 2], ['코드 7개 (하나 틀릴 때마다 −1, 최소 0)', 6]], src=src('hdraw')),
dict(type='table', lv='중', unit='Huffman', pts=7,
 q='<p>7번 트리로 문자 100개(빈도 합 100)를 나타낼 때 전체 비트 수와, 고정 길이 코드의 전체 비트 수를 쓰시오.</p>',
 head=['코드', '전체 비트 수'], rows=[['허프만', Bk(str(C2))], ['고정 길이', Bk('300')]],
 exp=' + '.join(f'{HF2[c]}×{len(HC2[c])}' for c in sorted(HF2)) + f' = {C2}. 문자 7개 → 2<sup>3</sup> = 8 ≥ 7 이라 고정 길이 3비트 → 300.', src=src('cost', 'fixed')),
dict(type='short', lv='중', unit='prefix-free', pts=6,
 q=f'<p>수업의 코드 a = 0, b = 101, c = 100, d = 111, e = 1101, f = 1100 으로 만든 비트열 <b>{DEC}</b> 을 문자열로 바꾸시오.</p>',
 show='faced', alt=['f a c e d'], exp='앞에서부터 트리를 따라 리프에 닿을 때마다 끊는다: 1100 (f) / 0 (a) / 100 (c) / 1101 (e) / 111 (d). prefix-free 라서 끊는 위치가 하나로 정해진다.', src=src('pfree', 'btree')),
dict(type='table', lv='하', unit='Huffman 시간', pts=8,
 q='<p>Huffman 의사코드에서 T 를 min heap 으로 생각한다. 문자가 n 개일 때 표를 채우시오.</p>',
 head=['항목', '답'], rows=[['extract_min 한 번', Bk('O(log n)')], ['insert 한 번', Bk('O(log n)')], ['while 반복 횟수', Bk('n − 1', 'n-1')], ['전체', Bk('O(n log n)')]],
 exp='heap 높이 h = O(log n). 한 번 묶을 때마다 노드가 1개 줄어 n − 1 번 반복 (Big-O 로는 n 번) → O(n log n).', src=src('heap', 'htime')),
dict(type='table', lv='상', unit='보조 명제 2', pts=14,
 q='<p>보조 명제 2: decode tree B 에서 가장 깊은 형제 u, v 를 부모 w 하나로 합친 트리를 B′ 이라 하면 cost(B) − cost(B′) = f(u) + f(v) 이다. 증명의 빈칸을 채우시오.</p>'
   + '<p>cost(B) − cost(B′) = f(u)·d<sub>B</sub>(u) + f(v)·d<sub>B</sub>(v) − f(w)·d<sub>B′</sub>(w)</p>',
 head=['빈칸', '내용', '답'],
 rows=[['(가)', 'u, v 는 형제이므로 d<sub>B</sub>(v) =', Bk('dB(u)', 'd_B(u)')],
       ['(나)', 'w 는 u 의 부모 자리이므로 d<sub>B′</sub>(w) =', Bk('dB(u) − 1', 'dB(u)-1', 'd_B(u)-1')],
       ['(다)', 'f(w) =', Bk('f(u) + f(v)', 'f(u)+f(v)')],
       ['(라)', '대입해 정리한 결과', Bk('f(u) + f(v)', 'f(u)+f(v)')],
       ['(마)', '나머지 리프의 비용이 식에 없는 이유', Bk('u, v 외에는 깊이가 같아서 빠진다', '나머지는 같아서 빠짐')]],
 exp='= f(u)d<sub>B</sub>(u) + f(v)d<sub>B</sub>(u) − (f(u) + f(v))(d<sub>B</sub>(u) − 1) = f(u) + f(v). 수업 판서의 d<sub>B′</sub>(u) − 1 은 d<sub>B</sub>(u) − 1 로 고친 것.',
 src=src('lem2')),
]
page('greedy-1b', 'E. 그리디 — 기본 2회', '기본', '<b>그리디 · 기본 2회</b> (9주차 2차시 ~ 10주차 2차시)<br>수업과 같은 문제를 새 값으로 — 거스름돈 반례 · 등호 경계 · 강의실 증명 빈칸 · 디코딩 · 보조 명제 2', G1B)

# ════════════════ greedy-1c 기본 3회 — 새 값 + 기호 바꿈 ════════════════
cg3 = coin_greedy([1, 5, 25, 100], 289); assert cg3 == [(100, 2), (25, 3), (5, 2), (1, 4)]
D3, H3 = [4, 2, 7, 1, 5, 3], 14; assert jobs(D3, H3) == [1, 2, 3, 4]
B3 = [1, 0, 3, 2, 6, 5, 9, 8, 11, 12]; E3 = [3, 4, 5, 7, 8, 10, 11, 12, 14, 15]; R3, TR3 = assign(B3, E3); assert R3 == [0, 2, 4, 6, 8] and best_count(B3, E3) == 5
HF3 = dict(A=22, B=4, C=13, D=9, E=35, F=6, G=11); HT3, HM3 = huffman(HF3); HC3 = codes(HT3); C3 = cost(HF3, HC3); assert C3 == 253
G1C = [
dict(type='table', lv='하', unit='거스름돈', pts=6,
 q='<p>동전 단위가 1, 5, 25, 100 이고 거스름돈이 <b>289</b> 이다. 큰 단위부터 거슬러 줄 때 표를 채우고, 이 동전에서 그리디가 최적인 이유를 한 단어로 쓰시오.</p>',
 head=['항목', '답'], rows=[['100', Bk('2')], ['25', Bk('3')], ['5', Bk('2')], ['1', Bk('4')], ['합계', Bk('11')], ['이유', Bk('약수', '작은 단위가 큰 단위의 약수')]],
 exp='289 → 100 × 2 (89) → 25 × 3 (14) → 5 × 2 (4) → 1 × 4. 1 | 5 | 25 | 100 처럼 작은 단위가 모두 큰 단위의 약수.', src=src('coin', 'coinwhy')),
dict(type='essay', lv='중', unit='일의 개수', pts=12,
 q=f'<p>소요시간 리스트 D = [4, 2, 7, 1, 5, 3], 하루 시간 H = 14 이다.</p><p>(1) 짧은 일부터 하는 전략의 답(개수)을 쓰시오.<br>(2) 그리디가 고른 일을 {sub("p",1)} ≤ {sub("p",2)} ≤ … , 그다음 일을 {sub("p",5)}, 가정한 최적 해를 {sub("q",1)} ≤ … ≤ {sub("q",5)} 라 하고, P = {sub("p",1)} + ⋯ + {sub("p",4)}, R = {sub("q",1)} + ⋯ + {sub("q",4)} 로 둘 때 귀류법 증명을 쓰시오.</p>',
 model=f'(1) 1 + 2 + 3 + 4 = 10 ≤ 14, + 5 = 15 &gt; 14 → <b>4개</b><br>(2) <b>가정</b>: 그리디 해(4개)는 최적이 아니다 → 5개 이상인 최적 해가 있고 그중 5개를 {sub("q",1)} ~ {sub("q",5)} 라 하자.<br>① P + {sub("p",5)} &gt; H (그리디가 5번째를 넣지 못함)<br>② R + {sub("q",5)} ≤ H (최적 해이므로)<br>③ P ≤ R ({sub("p",1)} ~ {sub("p",4)} 는 가장 짧은 4개)<br>④ {sub("p",5)} ≤ {sub("q",5)} ({sub("p",5)} 는 5번째로 짧은 일)<br>⑤ ③ + ④ → P + {sub("p",5)} ≤ R + {sub("q",5)} ≤ H<br><b>모순</b>: ⑤ 와 ① 이 충돌 → 가정이 틀림 → 그리디 해가 최적.',
 rubric=[['(1) 4개', 2], ['가정 (최적 해가 5개 이상)', 2], ['① ②', 2], ['③ ④ 와 각각의 이유', 4], ['⑤ 와 모순 · 결론', 2]], src=src('job', 'jobpf')),
dict(type='table', lv='중', unit='강의실 배정', pts=12,
 q=f'<p>강의 10개의 시작 시간 B, 끝 시간 E 가 E 오름차순으로 정렬되어 있다.</p>{room_given(B3, E3, "B", "E", "t")}<p>아래 알고리즘으로 배정할 때 t = 1 부터 표를 채우고 마지막 줄에 R 을 쓰시오.</p>' + pre('''
R = [0], j = 0
for t in range(1, n):
    if E[j] <= B[t]:
        R.append(t)
        j = t
return R'''),
 head=['t', 'B[t]', 'E[j]', '배정'], rows=trace_rows(TR3) + [['R', '', Bk('[0, 2, 4, 6, 8]', '0,2,4,6,8', '0 2 4 6 8'), '']],
 exp='수업의 S, F, k, L 이 B, E, j, R 로 바뀐 것뿐. ' + trace_exp(TR3, B3, E3, 'B', 'E', 't') + '. t = 2 처럼 E[j] = B[t] 로 같아도 배정한다. R = [0, 2, 4, 6, 8], 5개.',
 src=src('roomex')),
dict(type='table', lv='하', unit='강의실 배정', pts=6,
 q='<p>3번 알고리즘에서 바뀐 이름이 수업 코드의 무엇에 해당하는지 쓰시오.</p>',
 head=['3번 코드', '수업 코드'], rows=[['B', Bk('S')], ['E', Bk('F')], ['j', Bk('k')], ['R', Bk('L')]],
 exp='B(egin) = 시작 S, E(nd) = 끝 F, j = 가장 최근 배정한 강의 k, R = 고른 강의 리스트 L. 시험에서 이름이 바뀌어도 "역할"로 읽으면 같은 코드다.', src=src('roomalg')),
dict(type='table', lv='하', unit='Huffman', pts=10,
 q='<p>문자 A ~ G 의 빈도수 w() 가 A 22, B 4, C 13, D 9, E 35, F 6, G 11 이다. 빈도수가 가장 적은 두 개씩 묶는 순서를 채우시오.</p>',
 head=['단계', '묶는 두 개', '대표 빈도'], rows=huff_tab(HF3, HM3), exp=merges_txt(HM3), src=src('hstr')),
dict(type='essay', lv='중', unit='Huffman', pts=12,
 q=f'<p>5번의 순서로 허프만 트리를 그리고 각 문자의 코드와 전체 비트 수를 쓰시오. {RULE}</p>',
 model=tree_svg(HT3) + ', '.join(f'{c} = {HC3[c]}' for c in sorted(HC3)) + f'<br>전체 = ' + ' + '.join(f'{HF3[c]}×{len(HC3[c])}' for c in sorted(HF3)) + f' = <b>{C3}</b>',
 rubric=[['묶은 순서대로 트리 구성', 4], ['코드 7개 (하나 틀릴 때마다 −1, 최소 0)', 5], [f'전체 비트 수 {C3}', 3]], src=src('hdraw', 'cost')),
dict(type='table', lv='중', unit='Huffman', pts=8,
 q='<p>노드를 Q, 빈도를 w() 로 바꿔 쓴 Huffman 의사코드이다. 빈칸을 채우시오.</p>' + pre('''
def Huffman(Q):
    while len(Q) > 1:
        p = extract_min(Q)
        q = extract_min(Q)
        r = Node(left = p, right = q)
        w(r) = (가)
        (나)
    return Q'''),
 head=['빈칸', '답'], rows=[['(가)', Bk('w(p) + w(q)', 'w(p)+w(q)')], ['(나)', Bk('insert(Q, r)', 'insert(Q,r)')], ['문자 n 개일 때 while 반복 횟수', Bk('n − 1', 'n-1')], ['전체 시간복잡도', Bk('O(n log n)')]],
 exp='수업의 T, x, y, z, f 가 Q, p, q, r, w 로 바뀐 것. 새 노드 r 의 빈도는 두 자식 빈도의 합이고, r 을 다시 heap 에 넣는다.', src=src('hcode', 'htime')),
dict(type='essay', lv='상', unit='보조 명제 1', pts=14,
 q='<p>보조 명제 1 을 증명하시오. 빈도가 가장 작은 두 문자를 m, n 이라 하고, 최적 트리 H 에서 가장 깊은 곳의 형제를 s, t 라 하자. (수업의 x, y, a, b, T 가 각각 m, n, s, t, H 로 바뀌었다.)</p><p>명제: m, n 을 가장 깊은 곳에 형제로 갖는 최적 트리가 항상 존재한다.</p>',
 model='<b>가정</b>: 그런 최적 트리는 하나도 없다 → 최적 트리 H 의 가장 깊은 형제 s, t 는 m, n 이 아니다.<br><b>교환</b>: H 에서 m 과 s 의 자리를 바꾼 트리 H′. 달라진 것은 m, s 뿐.<br>cost(H) − cost(H′) = w(m)d<sub>H</sub>(m) + w(s)d<sub>H</sub>(s) − w(m)d<sub>H</sub>(s) − w(s)d<sub>H</sub>(m) = <b>(w(m) − w(s))(d<sub>H</sub>(m) − d<sub>H</sub>(s))</b><br>w(m) − w(s) ≤ 0 (m 의 빈도가 가장 작음), d<sub>H</sub>(m) − d<sub>H</sub>(s) ≤ 0 (s 가 가장 깊음) → 곱 ≥ 0 → cost(H) ≥ cost(H′) → <b>H′ 도 최적</b>.<br>같은 방법으로 n 과 t 를 바꾼 H″ 도 최적.<br><b>모순</b>: H″ 은 m, n 을 가장 깊은 형제로 갖는 최적 트리 ↔ 가정 → 명제가 참.',
 rubric=[['가정 (명제의 부정)', 2], ['교환 트리 H′ 과 cost 차이 식', 4], ['(w(m) − w(s))(d(m) − d(s)) 로 묶음', 3], ['두 인수의 부호와 이유 → H′ 도 최적', 3], ['n ↔ t 교환 후 모순 · 결론', 2]], src=src('lem1')),
dict(type='table', lv='중', unit='전략 후보', pts=10,
 q='<p>강의실 배정에서 다른 그리디 전략의 결과를 비교한다. 강의는 (시작, 끝) 으로 주어진다.</p><p>입력 ①: p (0, 10), q (1, 3), r (4, 6), s (7, 9)<br>입력 ②: p (4, 6), q (0, 5), r (5, 10)</p><p>각 전략으로 고른 강의 개수와 최적 개수를 채우시오. (끝 시간 = 다음 시작 시간이면 겹치지 않는다.)</p>',
 head=['입력', '전략', '전략의 개수', '최적 개수'],
 rows=[['①', '빨리 시작하는 강의부터', Bk('1'), Bk('3')], ['②', '소요시간이 짧은 강의부터', Bk('1'), Bk('2')], ['①', '빨리 끝나는 강의부터', Bk('3'), Bk('3')], ['②', '빨리 끝나는 강의부터', Bk('2'), Bk('2')]],
 exp='① 가장 먼저 시작하는 p 를 고르면 q, r, s 가 모두 겹쳐 1개, 최적은 q, r, s 3개. ② 가장 짧은 p (길이 2) 를 고르면 q, r 과 모두 겹쳐 1개, 최적은 q, r 2개. 빨리 끝나는 강의부터는 두 입력 모두 최적 — 수업에서 1, 2번 전략을 버린 이유가 이 반례들이다.',
 src=src('cand')),
dict(type='table', lv='상', unit='귀납 3단계', pts=10,
 q='<p>Huffman 증명의 귀납 3단계 (n = k) 이다. 허프만 트리 H 에서 빈도가 가장 작은 두 문자 m, n 을 부모 z 로 합친 트리를 H′ = H − {m, n} 이라 한다. 빈칸을 채우시오.</p>',
 head=['단계', '내용', '답'],
 rows=[['보조 명제 2', 'cost(H′) = (가)', Bk('cost(H) − w(m) − w(n)', 'cost(H)-w(m)-w(n)')],
       ['가정', 'H 는 최적이 아니다 → cost(K) (나) cost(H) 인 최적 트리 K 가 있다', Bk('<')],
       ['고르기', 'K 로 m, n 이 가장 깊은 곳에 형제로 있는 것을 고를 수 있다 — 근거 (다)', Bk('보조 명제 1')],
       ['합치기', 'cost(K − {m, n}) = cost(K) − w(m) − w(n) (라) cost(H′)', Bk('<')],
       ['모순', 'H′ 은 문자 k − 1 개의 허프만 트리 → (마) 에 의해 최적인데, 더 작은 트리가 있다', Bk('귀납 가정')]],
 exp='수업의 T, T″, x, y, f 가 H, K, m, n, w 로 바뀐 것. cost(K) &lt; cost(H) 이므로 cost(K − {m, n}) &lt; cost(H) − w(m) − w(n) = cost(H′). 문자 k − 1 개의 최적 트리 H′ 보다 비용이 작은 트리가 있다 → 모순 → H 는 최적.',
 src=src('step3', 'ind')),
]
page('greedy-1c', 'E. 그리디 — 기본 3회', '기본', '<b>그리디 · 기본 3회</b> (9주차 2차시 ~ 10주차 2차시)<br>새 값 + <b>기호를 바꾼</b> 문제 — 이름이 달라도 역할로 읽기 · 일의 개수 증명 서술 · 보조 명제 1 서술', G1C)

# ════════════════ greedy-2 응용 ════════════════
LEC = dict(A=(3, 8), B=(1, 4), C=(9, 12), D=(5, 7), E=(0, 6), F=(8, 11), G=(4, 5), H=(11, 14))
ORD = sorted(LEC, key=lambda k: (LEC[k][1], k)); SS = [LEC[k][0] for k in ORD]; FF = [LEC[k][1] for k in ORD]
LU, _ = assign(SS, FF); PICK = [ORD[i] for i in LU]; assert PICK == ['B', 'G', 'D', 'F', 'H'] and best_count(SS, FF) == 5
JA2 = [4, 2, 7, 3, 5, 1, 6]; JC = {T: len(jobs(JA2, T)) for T in (9, 10, 15, 30)}; assert JC == {9: 3, 10: 4, 15: 5, 30: 7}
assert (sum(k for _, k in coin_greedy([1, 5, 12], 15)), coin_opt([1, 5, 12], 15)) == (4, 3)
assert all(sum(k for _, k in coin_greedy([1, 5, 12], m)) == coin_opt([1, 5, 12], m) for m in range(1, 15))
assert (sum(k for _, k in coin_greedy([1, 6, 10], 12)), coin_opt([1, 6, 10], 12)) == (3, 2)
TB = dict(a='00', b='01', c='100', d='101', e='110', f='111'); assert prefix_free(TB) and cost(HF, TB) == 244
HP = [7, 9, 12, 13, 16, 43]; h = HP[:]; e1 = extract_min(h); H1 = h[:]; e2 = extract_min(h); H2 = h[:]; insert(h, e1 + e2); H3 = h[:]
assert (e1, H1, e2, H2, H3) == (7, [9, 13, 12, 43, 16], 9, [12, 13, 16, 43], [12, 13, 16, 43, 16])
TF = dict(a=5, b=5, c=10, d=10)
TA, _ = huffman(TF, True); TBB, _ = huffman(TF, False); CA, CB = codes(TA), codes(TBB); assert cost(TF, CA) == cost(TF, CB) == 60
T0 = dict(a='1100', b='1101', c='111', d='10', e='01', f='00'); assert prefix_free(T0) and cost(HF, T0) == 324
T1 = dict(T0); T1['f'], T1['a'] = T0['a'], T0['f']; assert cost(HF, T1) == 252
T2 = dict(T1); T2['e'], T2['b'] = T1['b'], T1['e']; assert cost(HF, T2) == 244
def lst(a): return '[' + ', '.join(map(str, a)) + ']'
def hs(a): return Bk(lst(a), ','.join(map(str, a)), ' '.join(map(str, a)))
G2 = [
dict(type='table', lv='중', unit='강의실 배정', pts=12,
 q='<p>강의 8개가 (시작, 끝) 으로 주어졌다. 정렬되어 있지 <b>않다</b>.</p><p>A (3, 8), B (1, 4), C (9, 12), D (5, 7), E (0, 6), F (8, 11), G (4, 5), H (11, 14)</p><p>빨리 끝나는 강의부터 배정하는 수업 알고리즘을 적용한다. 정렬한 순서, 고른 강의, 개수를 쓰시오.</p>',
 head=['항목', '답'], rows=[['끝 시간 순으로 정렬한 순서', Bk(', '.join(ORD), ','.join(ORD), ' '.join(ORD))], ['고른 강의 (고른 순서)', Bk(', '.join(PICK), ','.join(PICK), ' '.join(PICK))], ['개수', Bk('5')]],
 exp=f'끝 시간: B 4, G 5, E 6, D 7, A 8, F 11, C 12, H 14 (F 11 이 C 12 보다 먼저). B(끝 4) → G(시작 4 ≥ 4) → E(0 &lt; 5) ✕ → D(5 ≥ 5) → A(3 &lt; 7) ✕ → F(8 ≥ 7) → C(9 &lt; 11) ✕ → H(11 ≥ 11). 정렬을 먼저 하지 않고 이름 순서로 훑으면 틀린다.',
 src=src('roomalg', 'roomex')),
dict(type='line', lv='중', unit='강의실 배정', pts=8,
 q='<p>강의실 배정 코드를 옮겨 적다 <b>한 줄</b>을 잘못 적었다. 수업 예시(강의 11개)에 돌리자 [0, 3, 5, 6, 7, 8, 10] 이 나와 서로 겹치는 강의가 들어갔다. 잘못 적은 줄을 고르시오. (F 는 오름차순 정렬되어 있다.)</p>',
 code='''
L = [0]
k = 0
for i in range(1, n):
    if F[k] <= S[i]:
        L.append(i)
        k = k + 1
return L''', answer=[6],
 exp='k 는 "가장 최근에 배정한 강의의 번호"여야 하므로 k = i. k = k + 1 이면 3번을 배정한 뒤 k 가 1 이 되어 F[1] = 5 와 비교하고, S[5] = 5 ≥ 5 라서 3번(5 ~ 7)과 겹치는 5번(5 ~ 9)을 넣는다.', src=src('roomalg')),
dict(type='table', lv='하', unit='일의 개수', pts=8,
 q='<p>일 7개의 소요시간 A = [4, 2, 7, 3, 5, 1, 6] 이다. 하루 시간 T 에 따라 짧은 일부터 하는 전략으로 할 수 있는 일의 개수를 채우시오.</p>',
 head=['T', '개수'], rows=[[str(t), Bk(str(c))] for t, c in JC.items()],
 exp='정렬 1, 2, 3, 4, 5, 6, 7 의 누적 합 1, 3, 6, 10, 15, 21, 28. T 이하인 누적 합의 개수가 답 — T = 9 → 6 까지 3개, T = 10 → 10 (같음) 까지 4개, T = 15 → 5개, T = 30 → 28 ≤ 30 이라 7개 전부.', src=src('job')),
dict(type='table', lv='중', unit='거스름돈', pts=6,
 q='<p>동전 단위가 1, 5, 12 이다. 큰 단위부터 고르는 전략이 처음으로 틀리는 (가장 작은) 금액과, 그 금액에서 두 방법의 동전 개수를 쓰시오.</p>',
 head=['항목', '답'], rows=[['금액', Bk('15')], ['그리디 개수', Bk('4')], ['최적 개수', Bk('3')]],
 exp='14 이하는 모두 그리디 = 최적 (12 + 1 + 1 처럼). 15 에서 그리디는 12 + 1 + 1 + 1 = 4개, 최적은 5 + 5 + 5 = 3개. 5 가 12 의 약수가 아니어서 생긴다.', src=src('coinbad')),
dict(type='essay', lv='중', unit='거스름돈', pts=8,
 q='<p>동전 단위가 1, 6, 10 이다. 큰 단위부터 고르는 전략이 최적이 아닌 금액을 하나 찾아 두 방법의 동전을 쓰고, 수업의 근거로 이유를 쓰시오.</p>',
 model='예: <b>12</b> — 그리디 10 + 1 + 1 = 3개, 최적 6 + 6 = 2개.<br>이유: 6 이 10 의 <b>약수가 아니다</b>. 수업에서 큰 단위부터가 최적인 근거는 "작은 단위가 큰 단위의 약수"였으므로, 그 조건이 깨지면 큰 동전을 먼저 고르는 것이 손해가 될 수 있다.',
 rubric=[['그리디가 틀리는 금액 (12, 18 등 실제로 틀리는 것)', 3], ['두 방법의 동전과 개수', 2], ['6 이 10 의 약수가 아니라는 이유', 3]], src=src('coinwhy', 'coinbad')),
dict(type='mc', lv='하', unit='prefix-free', pts=6,
 q='<p>문자 a, b, c, d 에 대한 코드 중 <b>prefix-free 가 아닌</b> 것은?</p>',
 choices=['a = 0, b = 10, c = 110, d = 111', 'a = 00, b = 01, c = 10, d = 11', 'a = 1, b = 01, c = 001, d = 000', 'a = 0, b = 01, c = 110, d = 111'], answer=[4],
 exp='④ a = 0 이 b = 01 의 앞부분 → 비트열 01 을 "b" 로 읽을지 "a 다음 1…" 로 읽을지 정할 수 없다. ① ② ③ 은 모두 리프에만 문자를 둔 이진 트리로 그릴 수 있다.', src=src('pfree', 'btree')),
dict(type='table', lv='중', unit='cost', pts=8,
 q='<p>수업의 빈도 a 43, b 13, c 12, d 16, e 9, f 7 에 대해 다른 코드 a = 00, b = 01, c = 100, d = 101, e = 110, f = 111 을 만들었다. 빈칸을 채우시오.</p>',
 head=['항목', '답'], rows=[['prefix-free 인가 (O/X)', Bk('O', 'o')], ['전체 비트 수', Bk('244')], ['허프만 코드(230)와 비교해 최적인가 (O/X)', Bk('X', 'x')]],
 exp='(43 + 13) × 2 + (12 + 16 + 9 + 7) × 3 = 112 + 132 = 244. prefix-free 이지만 230 보다 크므로 최적이 아니다 — prefix-free 는 조건일 뿐, 최소 비용은 허프만이 보장한다.', src=src('cost', 'pfree')),
dict(type='table', lv='상', unit='min heap', pts=10,
 q=f'<p>Huffman 의 T 를 배열로 저장한 min heap 으로 본다. 처음 T = {lst(HP)} 이다. 수업 방식(extract_min: 루트를 꺼내고 마지막 노드를 루트로 옮겨 heapify_down / insert: 마지막 자리에 두고 heapify_up)으로 첫 번째 묶기를 할 때 각 단계 뒤의 배열을 쓰시오.</p>',
 head=['단계', '꺼낸 값', '배열'], rows=[['x = extract_min(T)', Bk(str(e1)), hs(H1)], ['y = extract_min(T)', Bk(str(e2)), hs(H2)], ['insert(T, z)', '—', hs(H3)]],
 exp='① 7 을 꺼내고 43 을 루트로 → 자식 9, 12 중 작은 9 와 교환 → 43 의 자식 13, 16 중 13 과 교환 → [9, 13, 12, 43, 16]. ② 9 를 꺼내고 16 을 루트로 → 자식 13, 12 중 12 와 교환 → [12, 13, 16, 43]. ③ z = 16 을 끝에 → 부모 13 보다 크므로 그대로 → [12, 13, 16, 43, 16]. 각 연산은 높이만큼 = O(log n).',
 src=src('heap')),
dict(type='table', lv='상', unit='Huffman', pts=10,
 q='<p>빈도가 a 5, b 5, c 10, d 10 이다. 빈도가 같을 때 꺼내는 순서에 따라 트리가 달라진다. 두 규칙으로 각각 허프만 트리를 만들 때 코드 길이와 전체 비트 수를 채우시오. (먼저 꺼낸 노드가 왼쪽 0)</p><p>규칙 ㉠: 빈도가 같으면 새로 만든 노드를 먼저 꺼낸다.<br>규칙 ㉡: 빈도가 같으면 원래 있던 문자를 먼저 꺼낸다.</p>',
 head=['문자', '㉠ 코드 길이', '㉡ 코드 길이'],
 rows=[[c, Bk(str(len(CA[c]))), Bk(str(len(CB[c])))] for c in 'abcd'] + [['전체 비트 수', Bk(str(cost(TF, CA))), Bk(str(cost(TF, CB)))]],
 exp='㉠ a + b = 10 → (새 노드 10) + c = 20 → d + 20 = 30: 길이 a 3, b 3, c 2, d 1. ㉡ a + b = 10 → c + d = 20 → 10 + 20 = 30: 모두 2. 두 트리의 모양은 다르지만 cost = 60 으로 같다 → 최적 트리는 하나가 아닐 수 있다.',
 src=src('hdraw', 'cost')),
dict(type='table', lv='상', unit='보조 명제 1', pts=8,
 q='<p>보조 명제 1 의 교환 식 cost(T) − cost(T′) = (f(x) − f(a))(d<sub>T</sub>(x) − d<sub>T</sub>(a)) 을 숫자로 확인한다. 수업의 빈도(a 43, b 13, c 12, d 16, e 9, f 7)에 트리 T 의 코드가 a = 1100, b = 1101, c = 111, d = 10, e = 01, f = 00 이다. 빈도가 가장 작은 f 를 가장 깊은 문자 a 와 바꾼 트리가 T′, 그다음 e 를 b 와 바꾼 트리가 T″ 이다.</p>',
 head=['항목', '답'], rows=[['cost(T)', Bk('324')], ['(f(f) − f(a))(d(f) − d(a))', Bk('72')], ['cost(T′)', Bk('252')], ['cost(T″)', Bk('244')]],
 exp='cost(T) = 43·4 + 13·4 + 12·3 + 16·2 + 9·2 + 7·2 = 324. (7 − 43)(2 − 4) = 72 ≥ 0 → cost(T′) = 324 − 72 = 252. e ↔ b: (9 − 13)(2 − 4) = 8 → 244. 두 인수가 모두 0 이하라서 차이는 항상 0 이상 → 바꿔도 비용이 늘지 않는다.',
 src=src('lem1')),
dict(type='table', lv='중', unit='보조 명제 2', pts=8,
 q='<p>수업의 허프만 트리 B (a = 0, b = 101, c = 100, d = 111, e = 1101, f = 1100, cost 230) 에서 가장 깊은 형제 e(9), f(7) 를 부모 w 하나로 합친 트리가 B′ 이다. 빈칸을 채우시오.</p>',
 head=['항목', '답'], rows=[['f(w)', Bk('16')], ['B′ 에서 w 의 깊이', Bk('3')], ['cost(B′) (직접 계산)', Bk('214')], ['cost(B) − cost(B′)', Bk('16')]],
 exp='cost(B′) = 43·1 + 13·3 + 12·3 + 16·3 + 16·3 = 214. 차이 230 − 214 = 16 = f(e) + f(f) → 보조 명제 2 와 같다.', src=src('lem2')),
dict(type='table', lv='중', unit='Huffman 시간', pts=8,
 q='<p>문자 20개로 Huffman 의사코드를 실행한다. 빈칸을 채우시오.</p>',
 head=['항목', '답'], rows=[['while 반복 횟수', Bk('19')], ['extract_min 호출 횟수', Bk('38')], ['insert 호출 횟수', Bk('19')], ['완성된 트리의 노드 개수 (리프 포함)', Bk('39')]],
 exp='한 번 반복할 때 노드 2개를 꺼내고 1개를 넣어 1개씩 준다 → 20 → 1 이 되려면 19번. extract_min 은 반복마다 2번 = 38, insert 1번 = 19. 리프 20 + 새로 만든 중간 노드 19 = 39.', src=src('hcode', 'htime')),
]
page('greedy-2', 'E. 그리디 — 응용', '응용', '<b>그리디 · 응용</b> (9주차 2차시 ~ 10주차 2차시)<br>정렬 안 된 입력 · 잘못된 코드 찾기 · 반례 찾기 · 동점 트리 · min heap 추적 · 보조 명제 숫자 확인', G2)

# ════════════════ greedy-3 심화 ════════════════
late = [1, 3, 7, 10]
G3 = [
dict(type='essay', lv='상', unit='강의실 증명', pts=14,
 q=f'<p>강의의 시작 시간 B, 끝 시간 E 가 E 오름차순으로 정렬되어 있다. 빨리 끝나는 강의부터 배정하는 알고리즘이 고른 강의를 {sub("r",1)}, {sub("r",2)}, …, {sub("r","m")} (m 개) 라 할 때, 이것이 최적임을 귀류법으로 증명하시오. (수업은 (0, 3, 7, 10) 이었지만 여기서는 일반적인 m 개로 쓴다.)</p>',
 model=f'<b>가정</b>: 그리디 해는 최적이 아니다 → 최적 해는 m + 1 개 이상 → 그중 끝 시간 순으로 {sub("o",1)}, …, {sub("o","m+1")} (서로 겹치지 않음).<br><b>바꾸기</b>: {sub("r",1)} 은 전체 중 가장 빨리 끝나므로 E[{sub("r",1)}] ≤ E[{sub("o",1)}] → {sub("o",1)} 을 {sub("r",1)} 로 바꿔도 겹치지 않는다.<br><b>포함</b>: {sub("G",1)} = {sub("r",1)} 과 겹치지 않는 강의, {sub("A",1)} = {sub("o",1)} 과 겹치지 않는 강의 → {sub("o",1)} 보다 앞에서 끝나는 강의가 없으므로 {sub("A",1)} ⊂ {sub("G",1)}.<br>{sub("r",2)} 는 {sub("G",1)} 중 가장 빨리 끝나는 강의 → {sub("A",1)} 에 있는 {sub("o",2)} 보다 늦게 끝나지 않음 → {sub("o",2)} 를 {sub("r",2)} 로 바꾼다. 이렇게 연쇄적으로 ({sub("r",1)}, …, {sub("r","m")}, {sub("o","m+1")}).<br><b>모순</b>: {sub("o","m+1")} 은 {sub("r","m")} 이 끝난 뒤 시작하는 강의인데, for 문은 모든 인덱스를 훑으므로 그리디가 {sub("o","m+1")} (또는 그런 강의)를 고르지 않았을 수 없다 ↔ 그리디 해는 m 개에서 끝남.<br><b>결론</b>: 가정이 틀렸다 → 그리디 해가 최적.',
 rubric=[['가정: 최적 해가 m + 1 개 이상', 2], [f'{sub("o",1)} → {sub("r",1)} 바꾸기와 이유 (가장 빨리 끝남)', 3], [f'{sub("A",1)} ⊂ {sub("G",1)} 와 이유', 3], ['연쇄적으로 바꿔 (r₁ … r<sub>m</sub>, o<sub>m+1</sub>)', 2], ['for 문이 o<sub>m+1</sub> 을 골랐어야 한다는 모순 · 결론', 4]], src=src('roompf')),
dict(type='essay', lv='상', unit='일의 개수 증명', pts=12,
 q=f'<p>일 n 개의 소요시간과 하루 시간 H 가 주어진다. 짧은 일부터 하는 전략이 m 개를 골랐다 ({sub("u",1)} ≤ ⋯ ≤ {sub("u","m")}, 그다음 짧은 일 {sub("u","m+1")}). 이 전략이 최적임을 귀류법으로 증명하시오. 기호는 직접 정해도 된다.</p>',
 model=f'<b>가정</b>: 그리디 해는 최적이 아니다 → m + 1 개 이상 할 수 있는 해가 있다 → 그중 짧은 순서로 m + 1 개 {sub("v",1)} ≤ ⋯ ≤ {sub("v","m+1")}.<br>U = {sub("u",1)} + ⋯ + {sub("u","m")}, V = {sub("v",1)} + ⋯ + {sub("v","m")}<br>① U + {sub("u","m+1")} &gt; H (그리디가 m + 1 번째를 못 넣음)<br>② V + {sub("v","m+1")} ≤ H (가능한 해)<br>③ U ≤ V ({sub("u",1)} ~ {sub("u","m")} 은 가장 짧은 m 개)<br>④ {sub("u","m+1")} ≤ {sub("v","m+1")} ({sub("u","m+1")} 은 m + 1 번째로 짧은 일)<br>⑤ U + {sub("u","m+1")} ≤ V + {sub("v","m+1")} ≤ H ↔ ① → <b>모순</b> → 그리디 해가 최적.<br>(m + 2 개 이상이어도 그중 m + 1 개만 떼어 내면 여전히 H 안에 들어가므로 m + 1 개로 충분하다.)',
 rubric=[['가정과 m + 1 개로 충분한 이유', 3], ['① ②', 3], ['③ ④ 와 이유', 4], ['⑤ 모순 · 결론', 2]], src=src('jobpf')),
dict(type='essay', lv='상', unit='보조 명제 1', pts=15,
 q='<p>Huffman 증명의 보조 명제 1 을 수업 기호(x, y, a, b, T, f, d<sub>T</sub>)로 서술하고 증명하시오.</p>',
 model='<b>명제</b>: 빈도수가 가장 작은 두 문자 x, y 를 가장 깊은 곳에 형제로 갖는 최적 decode tree 가 항상 존재한다.<br><b>가정</b>: 그런 최적 트리는 하나도 없다 → 최적 트리 T 에서 가장 깊은 형제 a, b 는 x, y 가 아니다.<br><b>교환</b>: x 와 a 를 바꾼 트리 T′. 나머지 리프는 그대로이므로 x, a 만 비교.<br>cost(T) − cost(T′) = f(x)d<sub>T</sub>(x) + f(a)d<sub>T</sub>(a) − f(x)d<sub>T′</sub>(x) − f(a)d<sub>T′</sub>(a), d<sub>T′</sub>(x) = d<sub>T</sub>(a), d<sub>T′</sub>(a) = d<sub>T</sub>(x)<br>= (f(x) − f(a))(d<sub>T</sub>(x) − d<sub>T</sub>(a)) ≥ 0 (f(x) ≤ f(a): x 의 빈도가 가장 작음, d<sub>T</sub>(x) ≤ d<sub>T</sub>(a): a 가 가장 깊음)<br>→ cost(T′) ≤ cost(T) → <b>T′ 도 최적</b>. 같은 방법으로 y ↔ b → T″ 도 최적.<br><b>모순</b>: T″ 은 x, y 를 가장 깊은 형제로 갖는 최적 트리 ↔ 가정 → 명제 참.',
 rubric=[['명제를 정확히 씀', 2], ['가정 (명제의 부정)', 2], ['cost 차이 식과 깊이 교환 관계', 4], ['(f(x) − f(a))(d(x) − d(a)) ≥ 0 과 두 부호의 이유', 4], ['T′ 최적 → T″ → 모순 · 결론', 3]], src=src('lem1')),
dict(type='essay', lv='상', unit='귀납 3단계', pts=15,
 q='<p>보조 명제 1, 2 와 귀납 가정(n &lt; k 일 때 허프만 트리는 최적)을 써서, n = k 일 때 허프만 트리 T 가 최적임을 증명하시오.</p>',
 model='T 에서 처음 묶은 (빈도가 가장 작은) x, y 를 부모 z 로 합친 트리 T′ = T − {x, y} (문자 k − 1 개). 보조 명제 2 → cost(T′) = cost(T) − f(x) − f(y).<br><b>가정</b>: T 는 최적이 아니다 → cost(T″) &lt; cost(T) 인 최적 트리 T″ 이 있다.<br><b>고르기</b>: 보조 명제 1 → T″ 으로 x, y 가 가장 깊은 곳에 형제로 있는 최적 트리를 고를 수 있다.<br><b>합치기</b>: 보조 명제 2 → cost(T″ − {x, y}) = cost(T″) − f(x) − f(y) &lt; cost(T) − f(x) − f(y) = cost(T′).<br><b>귀납 가정</b>: T′ 은 문자 k − 1 개를 허프만 알고리즘으로 만든 트리 → 최적.<br><b>모순</b>: 최적인 T′ 보다 비용이 <b>작은</b> 트리 T″ − {x, y} 가 있다 → 가정이 틀림 → T 는 최적.',
 rubric=[['T′ 정의와 cost(T′) = cost(T) − f(x) − f(y) (보조 명제 2)', 3], ['가정 cost(T″) &lt; cost(T)', 2], ['보조 명제 1 로 x, y 가 가장 깊은 형제인 T″ 선택', 3], ['cost(T″ − {x, y}) &lt; cost(T′) 유도', 3], ['귀납 가정으로 T′ 최적 → 모순 · 결론', 4]], src=src('step3', 'ind', 'lem1', 'lem2')),
dict(type='essay', lv='상', unit='전략 변형', pts=8,
 q='<p>강의실 배정에서 "<b>가장 늦게 시작하는 강의부터</b>, 이미 고른 강의와 겹치지 않으면 고르는" 전략은 최적인가? 수업 예시(강의 11개)에 적용한 결과와 함께 이유를 쓰시오.</p>',
 model=f'<b>최적이다.</b> 수업 예시에 적용하면 12 ~ 14 (10번) → 8 ~ 11 (7번) → 5 ~ 7 (3번) → 3 ~ 5 (1번) → {lst(late)}, <b>4개</b> (최적 4개와 같다).<br>이유: 시간축을 뒤집으면(시작 ↔ 끝) "늦게 시작하는 것부터"는 "빨리 끝나는 것부터"와 똑같은 전략이 된다. 겹침 관계는 뒤집어도 그대로이므로, 빨리 끝나는 강의부터의 귀류법 증명이 그대로 성립한다.',
 rubric=[['최적이라고 판단', 2], ['예시 결과 4개 (예: 1, 3, 7, 10)', 3], ['시간을 뒤집으면 빨리 끝나는 전략과 같다는 이유', 3]], src=src('cand', 'roompf')),
dict(type='essay', lv='상', unit='전략 변형', pts=8,
 q='<p>"<b>다른 강의와 가장 적게 겹치는 강의부터</b>" 고르는 전략 (고를 때마다 남은 강의끼리 다시 센다) 을 다음 강의들에 적용한다. (끝 = 다음 시작이면 겹치지 않는다.)</p><p>a (0, 3), b (4, 7), c (8, 11), d (12, 15), e (6, 9), p · q · r 은 모두 (2, 5), s · t · u 는 모두 (10, 13)</p><p>(1) 처음 각 강의가 겹치는 개수를 세어 이 전략이 처음 고르는 강의를 쓰시오.<br>(2) 이 전략의 결과 개수와 최적 개수를 비교하고 결론을 쓰시오.</p>',
 model='(1) e 는 b, c 하고만 겹쳐 <b>2개</b>로 가장 적다 (a, d 는 3개, 나머지는 4개) → <b>e</b> 를 먼저 고른다.<br>(2) e 를 고르면 b, c 가 빠진다. 남은 왼쪽 묶음 a, p, q, r 은 서로 모두 겹치고 오른쪽 묶음 d, s, t, u 도 그렇다 → 어느 것을 골라도 묶음마다 1개씩, 모두 <b>3개</b> (예: e, a, d). 최적은 a, b, c, d <b>4개</b> → 이 전략은 최적이 아니다 (반례).',
 rubric=[['e 가 겹침 2개로 가장 적음', 3], ['전략 결과 3개', 2], ['최적 4개 (a, b, c, d) → 최적이 아님', 3]], src=src('cand')),
dict(type='essay', lv='상', unit='거스름돈', pts=8,
 q='<p>미국 동전 1, 5, 10, 25 (센트) 는 10 이 25 의 약수가 아니다. 친구가 "수업에서 약수 관계가 깨지면 그리디가 틀린다고 했으니, 이 동전에서는 큰 단위부터 거슬러 주는 전략이 틀리는 금액이 반드시 있다"고 말했다. 이 말이 맞는지 판단하고 이유를 쓰시오. (1 ~ 999 센트를 모두 확인하면 그리디와 최적이 항상 같다.)</p>',
 model='<b>틀린 말이다.</b> 수업의 근거 "작은 단위가 큰 단위의 약수이면 큰 것부터가 최적"은 <b>충분 조건</b>이지 필요 조건이 아니다. 약수 관계가 깨지면 그리디가 틀릴 <b>수도</b> 있다는 뜻일 뿐 (1 · 5 · 7, 1 · 6 · 10 처럼), 반드시 틀린다는 뜻이 아니다. 1, 5, 10, 25 는 약수 관계가 아니어도 모든 금액에서 그리디가 최적이다 → 약수 관계가 아닐 때는 따로 증명하거나 반례를 찾아야 한다.',
 rubric=[['틀렸다고 판단', 2], ['약수 조건은 충분 조건일 뿐 (깨져도 틀린다는 보장 없음)', 4], ['"틀릴 수도 있다"와 "반드시 틀린다"의 구분 또는 반례 예시', 2]], src=src('coinwhy', 'coinbad')),
dict(type='essay', lv='상', unit='전략 변형', pts=8,
 q='<p>일의 개수 문제의 목표를 바꿔 "<b>하루 시간 T 를 넘지 않으면서 일한 시간의 합을 최대로</b>" 하려고 한다. 짧은 일부터 하는 전략을 그대로 쓴다.</p><p>(1) 이 전략이 틀리는 예를 하나 들어 두 답을 비교하시오.<br>(2) 수업의 귀류법 증명(① ~ ⑤) 중 어느 부분이 새 목표에서는 성립하지 않는지 쓰시오.</p>',
 model='(1) 예: A = [2, 3, 4], T = 7 → 짧은 것부터 2 + 3 = 5 (4 를 더하면 9 &gt; 7), 최적은 3 + 4 = <b>7</b>.<br>(2) 수업의 가정은 "최적 해가 <b>더 많은 개수</b>를 한다"였고 ③ X ≤ Y, ④ a<sub>4</sub> ≤ b<sub>4</sub> 는 개수를 비교할 때 쓰는 식이다. 새 목표에서 최적 해는 개수가 같거나 더 적고 시간 합만 크다 → b<sub>4</sub> 가 존재한다는 가정 자체가 성립하지 않아, 모순을 만들 수 없다. 짧은 것부터는 개수를 늘리는 전략이지 합을 키우는 전략이 아니다.',
 rubric=[['틀리는 예와 두 답 (실제로 틀리는 예)', 4], ['가정(더 많은 개수)이나 ③ · ④ 가 새 목표와 맞지 않는다는 설명', 4]], src=src('job', 'jobpf')),
dict(type='essay', lv='상', unit='보조 명제 2', pts=7,
 q='<p>수업 예시에서 묶을 때 생긴 대표 빈도는 16, 25, 32, 57, 100 이고 그 합은 230 = cost(T) 이다. 허프만 트리의 cost 가 항상 "묶을 때 생긴 대표 빈도의 합"과 같은 이유를 보조 명제 2 로 설명하시오.</p>',
 model='보조 명제 2: 가장 깊은 형제 u, v 를 부모 w 로 합치면 cost 가 정확히 f(u) + f(v) = f(w) 만큼 줄어든다. 허프만은 처음 묶은 두 개가 가장 깊은 형제가 되므로, 트리를 <b>묶은 순서의 반대로 하나씩 합치면</b> 매번 그 대표 빈도만큼 cost 가 줄고, 마지막에 루트 하나만 남으면 cost 는 0 이다. → cost(T) = 대표 빈도들의 합. (확인: 16 + 25 + 32 + 57 + 100 = 230)',
 rubric=[['합칠 때마다 cost 가 f(w) (= 대표 빈도) 만큼 줄어듦', 3], ['반복하면 루트만 남아 cost 0 → 합과 같다', 3], ['230 확인', 1]], src=src('lem2', 'hstr')),
dict(type='essay', lv='상', unit='강의실 배정', pts=5,
 q='<p>강의실 배정 코드의 조건 <b>F[k] &lt;= S[i]</b> 를 <b>F[k] &lt; S[i]</b> 로 바꾸었다. 수업 예시(강의 11개)에서는 결과가 같다. 결과가 달라지는 입력(강의 2 ~ 3개)을 만들고, 어느 쪽이 문제의 뜻에 맞는지 쓰시오.</p>',
 model='예: (0, 3), (3, 5) — &lt;= 이면 두 강의 모두 배정 (2개), &lt; 이면 3 &lt; 3 이 거짓이라 1개.<br>한 강의가 끝나는 시각에 다음 강의가 시작하는 것은 겹치지 않으므로 <b>&lt;=</b> 가 맞다 (수업 코드).',
 rubric=[['끝 = 시작인 강의가 있는 입력과 두 결과', 3], ['&lt;= 가 맞다는 이유', 2]], src=src('roomalg')),
]
page('greedy-3', 'E. 그리디 — 심화', '심화', '<b>그리디 · 심화</b> (9주차 2차시 ~ 10주차 2차시)<br>증명 전체 서술 (강의실 · 일의 개수 · Huffman 보조 명제 1 · 귀납 3단계) · 다른 전략의 최적 판정 · 반례', G3)
