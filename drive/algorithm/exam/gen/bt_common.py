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

def OX(unit, pts, q, items, s):
    KOR = 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊ'
    return dict(type='ox', lv='기초', unit=unit, pts=pts, q=f'<p>{q} 각 문장이 맞으면 O, 틀리면 X 를 고르시오.</p>', items=[[a, b] for a, b, _ in items],
                exp='<br>'.join(f'<b>{KOR[i]} ({"O" if b else "X"})</b> {e}' for i, (_, b, e) in enumerate(items)), src=s)

# ═════════ 백트래킹 계산 도우미 ═════════
from itertools import combinations
from fractions import Fraction as Fr
YEL, RED = '#FFD84D', '#C0341D'
def maze_sst(G, order=((1, 0, '↓'), (0, 1, '→'))):
    """첫 해에서 멈춤. 노드 = [라벨, 가지, 상태, 자식]"""
    n = len(G); found = [False]; path = []
    def go(x, y, lab, trail):
        nd = [f'({x},{y})', lab, 'ok', []]
        if not (0 <= x < n and 0 <= y < n) or G[x][y] == '1': nd[2] = 'x'; return nd
        if (x, y) == (n - 1, n - 1): nd[2] = 'ans'; found[0] = True; path[:] = trail + [(x, y)]; return nd
        for dx, dy, l in order:
            if found[0]: break
            nd[3].append(go(x + dx, y + dy, l, trail + [(x, y)]))
        return nd
    return go(0, 0, '', []), path
def queens_sst(n):
    found = [None]
    def ok(X):
        k = len(X) - 1
        return all(X[i] != X[k] and abs(X[i] - X[k]) != k - i for i in range(k))
    def go(X, lab):
        nd = ['[' + ','.join(map(str, X)) + ']', lab, 'ok', []]
        if X and not ok(X): nd[2] = 'x'; return nd
        if len(X) == n: nd[2] = 'ans'; found[0] = X; return nd
        for c in range(n):
            if found[0]: break
            nd[3].append(go(X + [c], f'{c}'))
        return nd
    return go([], ''), found[0]
def count(nd, st): return (nd[2] == st) + sum(count(c, st) for c in nd[3])
def ss_sst(A, S):
    """subsetsum1 순서 (넣음 먼저), 첫 True 에서 멈춤, 노드 = 남은 S"""
    found = [False]
    def go(i, s, lab):
        nd = [f'S={s}', lab, 'ok', []]
        if s == 0: nd[2] = 'ans'; found[0] = True; return nd
        if s < 0 or i == len(A): nd[2] = 'x'; return nd
        for take in (1, 0):
            if found[0]: break
            nd[3].append(go(i + 1, s - A[i] if take else s, f'{A[i]}{"○" if take else "✕"}'))
        return nd
    return go(0, S, '')
def subsets(A, S): return [list(c) for r in range(1, len(A) + 1) for c in combinations(A, r) if sum(c) == S]
def sol_first(A, S):
    if S == 0: return []
    if S < 0 or not A: return None
    r = sol_first(A[1:], S - A[0])
    return [A[0]] + r if r is not None else sol_first(A[1:], S)
def sol2_all(A, S):
    out = []; n = len(A); X = [0] * n
    def go(k):
        if k == n:
            if sum(a for a, x in zip(A, X) if x) == S: out.append(X[:])
            return
        X[k] = 1; go(k + 1); X[k] = 0; go(k + 1)
    go(0); return out
def calls(A, S, prune):
    c = [0]; n = len(A)
    def go(k, cs):
        c[0] += 1
        if k == n: return
        if (not prune) or cs + A[k] <= S: go(k + 1, cs + A[k])
        go(k + 1, cs)
    go(0, 0); return c[0]
def frac(P, S, i, size):
    B = Fr(0)
    for j in sorted(range(i, len(P)), key=lambda j: -Fr(P[j], S[j])):
        if size == 0: break
        if S[j] <= size: B += P[j]; size -= S[j]
        else: B += Fr(P[j]) * size / S[j]; size = 0
    return B
def F_(x): return str(x) if Fr(x).denominator == 1 else f'{Fr(x).numerator}/{Fr(x).denominator}'
def knap_bt(P, S, K, mp_mode='leaf'):
    """교수님 코드 (자식 방문 전에 검사). mp_mode='leaf' 잎 · 꽉 참에서만, 'node' 방문하는 모든 노드에서 MP 갱신 (판서)"""
    n = len(P); st = {'MP': 0, 'best': None}; steps = []; visited = []; cut = []
    def kn(i, size, profit, X):
        visited.append(tuple(X))
        if mp_mode == 'node' and profit > st['MP']: st['MP'] = profit; st['best'] = X + [0] * (n - len(X))
        if i >= n or size == 0:
            if profit > st['MP']: st['MP'] = profit; st['best'] = X + [0] * (n - len(X))
            return
        if S[i] <= size:
            b = profit + P[i] + frac(P, S, i + 1, size - S[i])
            steps.append((tuple(X), 1, b, st['MP'], b > st['MP']))
            if b > st['MP']: kn(i + 1, size - S[i], profit + P[i], X + [1])
            else: cut.append((tuple(X + [1]), 'bound', b))
        else:
            steps.append((tuple(X), 1, None, st['MP'], False)); cut.append((tuple(X + [1]), 'over', None))
        b = profit + frac(P, S, i + 1, size)
        steps.append((tuple(X), 0, b, st['MP'], b > st['MP']))
        if b > st['MP']: kn(i + 1, size, profit, X + [0])
        else: cut.append((tuple(X + [0]), 'bound', b))
    kn(0, K, 0, []); return st['MP'], st['best'], steps, visited, cut
def knap_opt(P, S, K):
    return max(sum(P[i] for i in c) for r in range(len(P) + 1) for c in combinations(range(len(P)), r) if sum(S[i] for i in c) <= K)
def xs(X): return '[' + ', '.join(map(str, X)) + ']'

def tree_svg(root, title, bw=74, bh=30, DX=None, DY=70, W=None):
    pos = {}; cnt = [0]
    def lay(nd, d):
        if not nd[3]: x = cnt[0]; cnt[0] += 1
        else: xs_ = [lay(c, d + 1) for c in nd[3]]; x = (xs_[0] + xs_[-1]) / 2
        pos[id(nd)] = (x, d); return x
    lay(root, 0); depth = max(d for _, d in pos.values())
    DX = DX or max(bw + 10, 60); W = cnt[0] * DX + 20; Hh = (depth + 1) * DY + 10
    X_ = lambda nd: 10 + pos[id(nd)][0] * DX + DX / 2; Y_ = lambda nd: 8 + pos[id(nd)][1] * DY
    o = [f'<svg viewBox="0 0 {W} {Hh}" style="width:100%;max-width:{min(W, 900)}px;height:auto;display:block;margin:8px 0" role="img"><title>{title}</title>']
    def edges(nd):
        for c in nd[3]:
            o.append(f'<line x1="{X_(nd)}" y1="{Y_(nd) + bh}" x2="{X_(c)}" y2="{Y_(c)}" stroke="#141414" stroke-width="1.4"/>')
            mx, my = .3 * X_(nd) + .7 * X_(c), .3 * (Y_(nd) + bh) + .7 * Y_(c); r = X_(c) >= X_(nd)
            o.append(f'<text x="{mx + (6 if r else -6)}" y="{my}" font-size="13" font-weight="700" text-anchor="{"start" if r else "end"}">{c[1]}</text>')
            edges(c)
    edges(root)
    def nodes(nd):
        x, y = X_(nd), Y_(nd); s = nd[2]
        fill = YEL if s == 'ans' else ('#FBE3DC' if s == 'x' else '#fff'); stroke = RED if s == 'x' else '#141414'
        o.append(f'<rect x="{x - bw / 2}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        o.append(f'<text x="{x}" y="{y + bh / 2 + 5}" font-size="13.5" font-weight="800" text-anchor="middle" fill="{RED if s == "x" else "#141414"}">{nd[0]}{" X" if s == "x" else (" O" if s == "ans" else "")}</text>')
        for c in nd[3]: nodes(c)
    nodes(root); o.append('</svg>'); return ''.join(o)
def maze_html(G):
    n = len(G); C = 26
    cells = ''.join(f'<rect x="{2 + y * C}" y="{2 + x * C}" width="{C}" height="{C}" fill="{"#555" if G[x][y] == "1" else "#fff"}" stroke="#141414"/>' for x in range(n) for y in range(n))
    return f'<svg viewBox="0 0 {n * C + 4} {n * C + 4}" style="width:{n * 30}px;height:auto;display:block;margin:6px 0" role="img"><title>미로</title>{cells}</svg>'
def tree_text(nd, depth=0):
    """트리를 들여쓰기 목록으로 (좁은 칸에서도 읽히게)"""
    mark = ' X' if nd[2] == 'x' else (' O (정답)' if nd[2] == 'ans' else '')
    line = '    ' * depth + (f'─{nd[1]}→ ' if nd[1] else '') + nd[0] + mark
    return [line] + [l for c in nd[3] for l in tree_text(c, depth + 1)]
