# 백트래킹 개념노트 — A4 인쇄판 (README 규칙, build_greedy.py 와 같은 형식)
# 범위: 11주차 1차시 ~ 13주차 1차시 전반 (미로 · N-Queens · Subset Sum · 일반형 · SST · Knapsack)
import html as H, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapgen import *
from itertools import combinations, product
from fractions import Fraction as Fr
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'algorithm/lecture/chapter/backtracking.html')

# ═════════ 검증 ═════════
G4 = ['0111', '0010', '1011', '0000']
G5 = ['01010', '00001', '01001', '01100', '00110']
def find_way(G):
    n = len(G); log = []
    def fw(x, y, path):
        if x >= n or y >= n: log.append(('out', x, y)); return None
        if G[x][y] == '1': log.append(('wall', x, y)); return None
        if (x, y) == (n - 1, n - 1): return path + [(x, y)]
        log.append(('ok', x, y))
        r = fw(x + 1, y, path + [(x, y)])
        return r if r else fw(x, y + 1, path + [(x, y)])
    return fw(0, 0, []), log
P4, L4 = find_way(G4); P5, L5 = find_way(G5)
assert P4 == [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]
assert P5 == [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]
DEAD5 = {(x, y) for k, x, y in L5 if k == 'ok'} - set(P5); assert DEAD5 == {(2, 0), (3, 0), (4, 0), (4, 1)}
def queens(n):
    sols = []; X = [0] * n
    def ok(k, c): return all(X[i] != c and abs(X[i] - c) != abs(i - k) for i in range(k))
    def go(k):
        if k == n: sols.append(X[:]); return
        for c in range(n):
            if ok(k, c): X[k] = c; go(k + 1)
    go(0); return sols
assert queens(4) == [[1, 3, 0, 2], [2, 0, 3, 1]]
A7 = [8, 6, 7, 5, 3, 10, 9]; S15 = 15
SUBS = sorted(sorted(c) for r in range(1, 8) for c in combinations(A7, r) if sum(c) == S15)
assert SUBS == [[3, 5, 7], [5, 10], [6, 9], [7, 8]]
DP_A = [8, 6, 7]
DP = [[False] * 16 for _ in DP_A]
for i, a in enumerate(DP_A):
    for s in range(16):
        prev = (lambda t: (t == 0) if i == 0 else (DP[i - 1][t] if t >= 0 else False))
        DP[i][s] = s == 0 or (i == 0 and s == a) or (i > 0 and (DP[i - 1][s] or (s - a >= 0 and DP[i - 1][s - a])))
assert DP[2][15] and [s for s in range(16) if DP[2][s]] == [0, 6, 7, 8, 13, 14, 15]
AS = sorted(A7); cnt = [0, 0]
def s2(k, cs, pr):
    cnt[pr] += 1
    if k == 7: return
    if (not pr) or cs + AS[k] <= S15: s2(k + 1, cs + AS[k], pr)
    s2(k + 1, cs, pr)
s2(0, 0, 0); s2(0, 0, 1); assert cnt == [255, 93]
# Knapsack
K4, S4, P4k = 16, [2, 5, 10, 5], [40, 30, 50, 10]
best4 = max((sum(P4k[i] for i in c), c) for r in range(5) for c in combinations(range(4), r) if sum(S4[i] for i in c) <= K4)
assert best4 == (90, (0, 2))
P3, S3, K3 = [15, 16, 6], [3, 4, 2], 5
def frac(i, size, P=P3, S=S3):
    B = Fr(0)
    for j in sorted(range(i, len(P)), key=lambda j: -Fr(P[j], S[j])):
        if size == 0: break
        if S[j] <= size: B += P[j]; size -= S[j]
        else: B += Fr(P[j]) * size / S[j]; size = 0
    return B
assert frac(0, 16, P4k, S4) == 115 and frac(1, 2) == 8 and frac(2, 2) == 6 and frac(3, 0) == 0 and frac(3, 2) == 0 and frac(1, 5) == 19

# ═════════ 그림 ═════════
def fig_maze(G, path, dead=(), W=330, title='', mark_x=()):
    n = len(G); C = (W - 40) / n; o = [f'<svg viewBox="0 0 {W} {W - 10}" role="img"><title>{title}</title>']
    for x in range(n):
        for y in range(n):
            X0, Y0 = 20 + y * C, 10 + x * C
            fill = '#000' if G[x][y] == '1' else (YEL if (x, y) in path else ('#F7D9D1' if (x, y) in dead else '#fff'))
            o.append(f'<rect x="{X0}" y="{Y0}" width="{C}" height="{C}" fill="{fill}" stroke="#000" stroke-width="1.4"/>')
            if (x, y) in dead: o.append(f'<text x="{X0 + C / 2}" y="{Y0 + C / 2 + 6}" font-size="18" font-weight="800" text-anchor="middle" fill="{RED}">✕</text>')
    pts = ' '.join(f'{20 + y * C + C / 2},{10 + x * C + C / 2}' for x, y in path)
    o.append(f'<polyline points="{pts}" fill="none" stroke="#000" stroke-width="2.4"/>')
    o.append(f'<text x="{20 + C / 2}" y="{10 + C / 2 - C * .22}" font-size="12.5" font-weight="800" text-anchor="middle">시작</text>')
    o.append(f'<text x="{20 + (n - .5) * C}" y="{10 + (n - .5) * C - C * .22}" font-size="12.5" font-weight="800" text-anchor="middle">도착</text>')
    o.append('</svg>'); return ''.join(o)

def fig_board(X, W=300, title=''):
    n = len(X); C = (W - 40) / n; o = [f'<svg viewBox="0 0 {W} {W - 10}" role="img"><title>{title}</title>']
    for r in range(n):
        for c in range(n):
            o.append(f'<rect x="{30 + c * C}" y="{10 + r * C}" width="{C}" height="{C}" fill="{YEL if X[r] == c else "#fff"}" stroke="#000" stroke-width="1.4"/>')
            if X[r] == c: o.append(f'<text x="{30 + c * C + C / 2}" y="{10 + r * C + C / 2 + 8}" font-size="22" font-weight="800" text-anchor="middle">Q</text>')
        o.append(f'<text x="18" y="{10 + r * C + C / 2 + 5}" font-size="13" font-weight="700" text-anchor="middle">{r}</text>')
    o.append('</svg>'); return ''.join(o)

def fig_diag():
    W, C = 680, 46; o = [f'<svg viewBox="0 0 {W} 300" role="img"><title>대각선 판정</title>']
    x0, y0 = 40, 30
    for r in range(5):
        for c in range(5):
            o.append(f'<rect x="{x0 + c * C}" y="{y0 + r * C}" width="{C}" height="{C}" fill="#fff" stroke="#000" stroke-width="1"/>')
    qi, qk = (1, 4), (4, 1)
    for (r, c), lab in ((qi, 'i 행, X[i]'), (qk, 'k 행, c')):
        o.append(f'<rect x="{x0 + c * C}" y="{y0 + r * C}" width="{C}" height="{C}" fill="{YEL}" stroke="#000" stroke-width="1.6"/><text x="{x0 + c * C + C / 2}" y="{y0 + r * C + C / 2 + 7}" font-size="19" font-weight="800" text-anchor="middle">Q</text>')
    cx = lambda c: x0 + c * C + C / 2; cy = lambda r: y0 + r * C + C / 2
    o.append(f'<line x1="{cx(4)}" y1="{cy(1)}" x2="{cx(1)}" y2="{cy(4)}" stroke="{RED}" stroke-width="2.4"/>')
    o.append(f'<line x1="{cx(1)}" y1="{cy(4)}" x2="{cx(4)}" y2="{cy(4)}" stroke="#000" stroke-width="2" stroke-dasharray="6 4"/><line x1="{cx(4)}" y1="{cy(4)}" x2="{cx(4)}" y2="{cy(1)}" stroke="#000" stroke-width="2" stroke-dasharray="6 4"/>')
    tx = x0 + 5 * C + 40
    for j, s in enumerate(['위쪽 퀸: i 행, X[i] 열', '새 퀸: k 행, c 열', '밑변 = |c − X[i]|  (열 차이)', '높이 = |k − i|  (행 차이)', '밑변 = 높이  →  같은 대각선 (빨강)', '왼쪽 위 · 오른쪽 위 모두 → 절댓값']):
        o.append(f'<text x="{tx}" y="{y0 + 30 + j * 34}" font-size="15" font-weight="{800 if j == 4 else 600}" fill="{RED if j == 4 else "#000"}">{s}</text>')
    o.append('</svg>'); return ''.join(o)

def fig_bt(root, W=680, DX=None, DY=78, title='', bw=84, bh=30):
    """root = [라벨, 가지 라벨, 상태 ok|x|ans|todo, 자식]"""
    pos = {}; cnt = [0]
    def lay(nd, d):
        if not nd[3]: x = cnt[0]; cnt[0] += 1
        else: xs = [lay(c, d + 1) for c in nd[3]]; x = (xs[0] + xs[-1]) / 2
        pos[id(nd)] = (x, d); return x
    lay(root, 0); depth = max(d for _, d in pos.values())
    DX = DX or (W - 20) / cnt[0]; Hh = (depth + 1) * DY + 10
    X_ = lambda nd: 10 + pos[id(nd)][0] * DX + DX / 2; Y_ = lambda nd: 8 + pos[id(nd)][1] * DY
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img"><title>{title}</title>']
    def edges(nd):
        for c in nd[3]:
            dash = ' stroke-dasharray="6 4"' if c[2] == 'todo' else ''
            o.append(f'<line x1="{X_(nd)}" y1="{Y_(nd) + bh}" x2="{X_(c)}" y2="{Y_(c)}" stroke="#000" stroke-width="1.4"{dash}/>')
            mx, my = .35 * X_(nd) + .65 * X_(c), .35 * (Y_(nd) + bh) + .65 * Y_(c)
            right = X_(c) >= X_(nd)
            o.append(f'<text x="{mx + (7 if right else -7)}" y="{my}" font-size="12.5" font-weight="700" text-anchor="{"start" if right else "end"}">{c[1]}</text>')
            edges(c)
    edges(root)
    def nodes(nd):
        x, y = X_(nd), Y_(nd); st = nd[2]
        fill = YEL if st == 'ans' else ('#F7D9D1' if st == 'x' else '#fff'); stroke = RED if st == 'x' else '#000'
        dash = ' stroke-dasharray="6 4"' if st == 'todo' else ''
        o.append(f'<rect x="{x - bw / 2}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{dash}/>')
        o.append(f'<text x="{x}" y="{y + bh / 2 + 5}" font-size="13" font-weight="800" text-anchor="middle" fill="{RED if st == "x" else "#000"}">{nd[0]}{" ✕" if st == "x" else ""}</text>')
        for c in nd[3]: nodes(c)
    nodes(root); o.append('</svg>'); return ''.join(o)

def maze_sst(G):
    n = len(G); found = [False]
    def go(x, y, lab):
        nd = [f'({x},{y})', lab, 'ok', []]
        if x >= n or y >= n or G[x][y] == '1': nd[2] = 'x'; return nd
        if (x, y) == (n - 1, n - 1): nd[2] = 'ans'; found[0] = True; return nd
        for dx, dy, l in ((1, 0, '↓'), (0, 1, '→')):
            if found[0]: break
            nd[3].append(go(x + dx, y + dy, l))
        return nd
    return go(0, 0, '')
SST4 = maze_sst(G4)
def ss_tree():
    """subsetsum1 (A = [8, 6, 7], S = 15) — 교수님 설명 순서, 첫 True 에서 멈춤"""
    def nd(lab, e, st='ok', ch=()): return [lab, e, st, list(ch)]
    return nd('S = 15', '', 'ok', [
        nd('S = 7', '8 ○', 'ok', [nd('S = 1', '6 ○', 'ok', [nd('S = −6', '7 ○', 'x'), nd('S = 1', '7 ✕', 'x')]),
                                  nd('S = 7', '6 ✕', 'ok', [nd('S = 0', '7 ○', 'ans')])]),
        nd('S = 15', '8 ✕', 'todo')])
FIG_SS = fig_bt(ss_tree(), DY=74, title='subsetsum1 재귀 탐색 트리')
FIG_SST4 = fig_bt(SST4, DY=70, bw=70, title='4 × 4 미로의 SST')

def fig_bag(fills, note, W=330, U=11.5, K=16, S=S4, P=P4k):
    BW = 120; x0 = 50; y0 = 14; H0 = K * U
    o = [f'<svg viewBox="0 0 {W} {H0 + 50}" role="img"><title>{note}</title>']
    for t in range(0, K + 1, 4 if K > 8 else 1):
        y = y0 + H0 - t * U
        o.append(f'<line x1="{x0 - 5}" y1="{y}" x2="{x0}" y2="{y}" stroke="#000"/><text x="{x0 - 9}" y="{y + 4}" font-size="12" font-weight="600" text-anchor="end">{t}</text>')
    y = y0 + H0
    for i, w, kind in fills:
        y -= w * U; val = Fr(P[i]) * w / S[i]
        fill = YEL if kind == 'r' else '#fff'; dash = ' stroke-dasharray="5 3"' if kind == 'g' else ''
        o.append(f'<rect x="{x0 + 4}" y="{y}" width="{BW - 8}" height="{w * U}" fill="{fill}" stroke="#000" stroke-width="1.4"{dash}/>')
        lab = f'{i + 1}번 {w}{"" if w == S[i] else "/" + str(S[i])} · {val}' if K > 8 else f'{i}번 {w}{"" if w == S[i] else "/" + str(S[i])} · {val}'
        o.append(f'<text x="{x0 + BW / 2}" y="{y + w * U / 2 + 5}" font-size="12.5" font-weight="800" text-anchor="middle">{lab}</text>')
    if y > y0 + 1: o.append(f'<text x="{x0 + BW / 2}" y="{(y0 + y) / 2 + 5}" font-size="13" font-weight="800" text-anchor="middle" fill="{RED}">빈 {round((y - y0) / U)}</text>')
    o.append(f'<path d="M{x0} {y0 - 6} V{y0 + H0 + 3} H{x0 + BW} V{y0 - 6}" fill="none" stroke="#000" stroke-width="2.4"/>')
    o.append(f'<text x="{x0 + BW + 14}" y="{y0 + 24}" font-size="13" font-weight="800">K = {K}</text>')
    o.append(f'<text x="{W / 2}" y="{H0 + 44}" font-size="13" font-weight="700" text-anchor="middle">{note}</text>')
    o.append('</svg>'); return ''.join(o)
FIG_FR = fig_bag([(0, 2, 'r'), (1, 5, 'r'), (2, 9, 'r')], 'fractional: 40 + 30 + 45 = 115')
FIG_80 = fig_bag([(0, 2, 'r'), (1, 5, 'r'), (3, 5, 'r')], '0/1 가성비 순: 80')
FIG_90 = fig_bag([(0, 2, 'r'), (2, 10, 'r')], '0/1 최적: 40 + 50 = 90')

def fig_ksst():
    W, Hh = 680, 400
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img"><title>0/1 knapsack 상태 공간 트리</title>']
    N = {'r': (340, 14, '[ ]', 'p 0 · s 0'), 'a': (190, 124, '[1]', 'p 15 · s 3'), 'b': (290, 234, '[1, 0]', 'p 15 · s 3'), 'c': (200, 344, '[1, 0, 1]', 'p 21 · s 5')}
    Xn = {'x1': (80, 234, '[1, 1]', '무게 7 > 5'), 'x2': (420, 344, '[1, 0, 0]', '상한 15 ≤ 21'), 'x3': (540, 124, '[0]', '상한 19 ≤ 21')}
    def ln(a, b, lab, cut=False, right=False):
        x1, y1 = a[0], a[1] + 44; x2, y2 = b[0], b[1]
        o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RED if cut else "#000"}" stroke-width="1.6"{" stroke-dasharray=\"6 4\"" if cut else ""}/>')
        o.append(f'<text x="{(x1 + x2) / 2 + (9 if right else -9)}" y="{(y1 + y2) / 2}" font-size="12.5" font-weight="700" text-anchor="{"start" if right else "end"}">{lab}</text>')
    ln(N['r'], N['a'], 'X[0] = 1 · 상한 23'); ln(N['r'], Xn['x3'], 'X[0] = 0 · 상한 19', True, True)
    ln(N['a'], Xn['x1'], 'X[1] = 1', True); ln(N['a'], N['b'], 'X[1] = 0 · 상한 21', False, True)
    ln(N['b'], N['c'], 'X[2] = 1 · 상한 21'); ln(N['b'], Xn['x2'], 'X[2] = 0 · 상한 15', True, True)
    for k, (x, y, a, b) in N.items():
        o.append(f'<rect x="{x - 60}" y="{y}" width="120" height="44" rx="7" fill="{YEL if k == "c" else "#fff"}" stroke="#000" stroke-width="1.6"/>')
        o.append(f'<text x="{x}" y="{y + 18}" font-size="13.5" font-weight="800" text-anchor="middle">{a}</text><text x="{x}" y="{y + 36}" font-size="12.5" font-weight="600" text-anchor="middle">{b}</text>')
    for k, (x, y, a, b) in Xn.items():
        o.append(f'<rect x="{x - 60}" y="{y}" width="120" height="44" rx="7" fill="#F7D9D1" stroke="{RED}" stroke-width="1.5" stroke-dasharray="6 4"/>')
        o.append(f'<text x="{x}" y="{y + 18}" font-size="13.5" font-weight="800" text-anchor="middle" fill="{RED}">{a} ✕</text><text x="{x}" y="{y + 36}" font-size="12.5" font-weight="600" text-anchor="middle">{b}</text>')
    o.append('</svg>'); return ''.join(o)
FIG_KSST = fig_ksst()

def fig_vtri():
    W, Hh = 680, 300
    o = [f'<svg viewBox="0 0 {W} {Hh}" role="img"><title>노드 v</title>', '<polygon points="230,10 30,270 430,270" fill="#fff" stroke="#000" stroke-width="1.5"/>']
    pts = [(230, 18), (205, 55), (240, 92), (212, 129), (238, 166)]
    o.append('<polyline points="' + ' '.join(f'{x},{y}' for x, y in pts) + '" fill="none" stroke="#000" stroke-width="2.4"/>')
    for x, y in pts[:-1]: o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#000" stroke-width="1.4"/>')
    vx, vy = pts[-1]; o.append(f'<circle cx="{vx}" cy="{vy}" r="12" fill="{YEL}" stroke="#000" stroke-width="1.6"/><text x="{vx}" y="{vy + 5}" font-size="14" font-weight="800" text-anchor="middle">v</text>')
    for cx, lab, an in ((190, 'X[i] = 1', 'end'), (290, 'X[i] = 0', 'start')):
        o.append(f'<line x1="{vx}" y1="{vy + 12}" x2="{cx}" y2="210" stroke="#000" stroke-width="1.8"/><circle cx="{cx}" cy="210" r="6" fill="#fff" stroke="#000" stroke-width="1.4"/>')
        o.append(f'<polygon points="{cx},216 {cx - 34},270 {cx + 34},270" fill="#fff" stroke="#000" stroke-width="1.3"/>')
        o.append(f'<text x="{(vx + cx) / 2 + (-10 if an == "end" else 10)}" y="194" font-size="13" font-weight="800" text-anchor="{an}">{lab}</text>')
    tx = 460
    for j, s in enumerate(['루트 → v : X[0] ~ X[i − 1] 결정 완료', 'v 의 두 가지 : X[i] 결정', '작은 삼각형 : X[i + 1] ~ X[n − 1]', 'p(v) = v 까지 넣은 가치 합', 's(v) = v 까지 넣은 무게 합']):
        o.append(f'<text x="{tx}" y="{40 + j * 40}" font-size="14" font-weight="{800 if j < 3 else 600}">{s}</text>')
    o.append('</svg>'); return ''.join(o)
FIG_V = fig_vtri()

x_ = lambda i: f'X[{i}]'
CH = []

# 1 ──────────────────────────────
CH.append(('1', '백트래킹 방법', '11주차 1차시', [
 unit('', f'''<dl class="def"><dt>백트래킹</dt><dd>말 그대로 거슬러 올라가는 방법: {hl('진행 → 막힌다 → 되돌아간다 (back-track)')} 를 반복</dd>
 <dt>backtrack</dt><dd>되돌아가다, 거슬러 올라가다</dd></dl>
 <p>지금까지 분할 정복법, 동적 계획법, 그리디 전략을 배웠고, 이번 단원은 백트래킹 알고리즘. 굉장히 직관적이고 쉬운 알고리즘이다.</p>'''),
 unit('특징', f'''<ul class="dot"><li>사실 백트래킹은 {hl('가능한 방식을 다 해 보는 것')} — 막히면 되돌아가서 다시 시작</li>
 <li>오래 걸릴 수 있다</li>
 <li>시작 → 도착 경로가 1개 이상 존재한다면 {hl('무조건 답을 찾을 수 있다')}</li>
 <li>그리디, 분할 정복법, DP 로 답이 없을 때 {hl('최후의 보루')}로 쓰는 알고리즘 (비효율적이기 때문){fn('보충', '이 내용은 12주차 1차시 일반형 설명 때 나왔다.')}</li></ul>'''),
]))

# 2 ──────────────────────────────
CH.append(('2', '미로 탈출', '11주차 1차시, 예시 1', [
 unit('', f'''<dl class="def"><dt>문제</dt><dd>미로의 왼쪽 위 (시작) 에서 오른쪽 아래 (도착) 까지 갈 수 있는 길 찾기</dd>
 <dt>규칙</dt><dd>가능한 방향은 남쪽 (↓), 동쪽 (→) — {hl('이 순서대로')} 탐방, 막히면 백트랙</dd></dl>'''),
 unit('4 × 4 미로', f'''<div class="figrow"><figure>{fig_maze(G4, P4, title='4×4')}<figcaption>검정 = 벽, 노랑 = 찾은 길</figcaption></figure>
 <div>{table(['^순서', '동작'], [['1', '남 → (1, 0)'], ['2', '남 → (2, 0) 벽 → 최근 선택으로 돌아와 동 → (1, 1)'], ['3', '남 → (2, 1), 남 → (3, 1)'], ['4', '남 → 막힘 (미로 밖) → 백트랙, 동 → (3, 2)'], ['5', '남 → 막힘 → 백트랙, 동 → (3, 3) 도착']], ['18%', '82%'])}</div></div>'''),
 unit('5 × 5 미로', f'''<div class="figrow"><figure>{fig_maze(G5, P5, dead=DEAD5, title='5×5')}<figcaption>빨강 ✕ = 들어갔다가 백트랙한 칸</figcaption></figure>
 <div><ul class="dot"><li>아래로 4번 → (4, 0) 에서 아래 막힘, 동 (4, 1) → 아래 막힘, 동 (4, 2) 벽 → 돌아감</li>
 <li>(3, 0), (2, 0) 은 이미 아래를 해 봤고 동쪽이 벽 → 계속 돌아감</li>
 <li>(1, 0) 에서 동 → (1, 1) → 아래 벽, 동 (1, 2) → 아래 (2, 2) → 아래 벽, 동 (2, 3) → 아래 (3, 3) → 아래 벽, 동 (3, 4) → 아래 (4, 4) {hl('도착')}</li></ul></div></div>'''),
 unit('의사코드 — M[x][y] 와 find_way(x, y)', f'''<p>미로판을 {v('M')}, 행을 {v('x')}, 열을 {v('y')} 라 하면 한 칸은 {v('M')}[{v('x')}][{v('y')}] ({v('x')}, {v('y')} = 0 ~ 4). 흰 칸 (갈 수 있는 칸) 은 {hl('safe')}. 막힌 칸을 unsafe 라 할 수도 있지만 코드에서 필요 없어서 따로 정의하지 않는다.</p>{code('pseudocode', 'find_way(x, y) — 길이 있으면 true, 첫 호출 find_way(0, 0)', """
def find_way(x, y):
    if x == n - 1 and y == n - 1:     # 도착 지점
        return true
    if M[x][y] == safe:               # 현재 위치가 흰 칸
        try_down = find_way(x + 1, y)    # 1순위: 남쪽
        if try_down == true:
            return true
        try_east = find_way(x, y + 1)    # 남쪽이 막혔으면 동쪽
        return try_east
    else:                             # 현재 위치가 벽
        return false""")}
 <ul class="dot"><li>세 개의 {hl('if · if · else 는 같은 높이')}{fn('판서 정정', '처음 판서는 두 번째 if 와 else 가 첫 if 안쪽에 들여써져 있었다 → 그러면 도착이 아닐 때 아무것도 안 함. 12주차 1차시에 교수님이 같은 높이로 고치셨다.')} — 도착이면 true, 아니면 흰 칸인지 보고, 벽이면 false</li>
 <li>남쪽이 실패해서 돌아오면 동쪽을 시도 = 백트랙{fn('판서 정정', 'fine_way → find_way (오타).')}{fn('보충', '미로 밖 (x ≥ n 또는 y ≥ n) 검사가 없어서 실제로 돌리면 범위 밖 인덱스가 된다. 함수 맨 앞에 if x >= n or y >= n: return false 를 두면 된다.')}</li></ul>'''),
]))

# 3 ──────────────────────────────
CH.append(('3', 'N-Queens', '11주차 1차시, 예시 2', [
 unit('', f'''<dl class="def"><dt>문제</dt><dd>{v('N')} × {v('N')} 체스판에 퀸 {v('N')} 개를 놓되 {hl('서로 같은 행, 열, 대각선에 있으면 안 됨')}</dd>
 <dt>답의 표기</dt><dd>{v('X')}[{v('k')}] = {v('k')} 행에 놓인 퀸의 열 인덱스</dd></dl>'''),
 unit('4-Queens 의 답 2가지', f'''<div class="figrow"><figure>{fig_board([1, 3, 0, 2], title='답 1')}<figcaption>{v('X')} = [1, 3, 0, 2]</figcaption></figure><figure>{fig_board([2, 0, 3, 1], title='답 2')}<figcaption>{v('X')} = [2, 0, 3, 1]</figcaption></figure></div>
 <p>{v('X')}[0] 부터 채운다: {v('X')}[0] = 0 (0행 0열) 가능 → {v('X')}[1] 은 0 안 됨, 1 안 됨, 2 가능 → … 이런 식으로 채워 나가고 막히면 백트랙.</p>'''),
 unit('대각선 판정', f'''<figure>{fig_diag()}</figure>
 <p>위쪽 {v('i')} 행의 퀸 ({v('X')}[{v('i')}] 열) 과 새로 놓을 {v('k')} 행 {v('c')} 열을 이어 만든 직각삼각형의 {hl('밑변 |c − X[i]| 과 높이 |k − i| 가 같으면 같은 대각선')}. 왼쪽 위에 있으면 부호가 반대라서 절댓값으로 비교.</p>'''),
 unit('의사코드 — nqueens(k) · is_safe(k, c)', f'''{code('pseudocode', 'nqueens(k) — X[k] 를 정함, 첫 호출 nqueens(0)', """
def nqueens(k):
    if k == N:                  # 0 ~ N-1 행을 모두 채움
        print(X)
        return
    for c in range(N):          # k 행의 0 ~ N-1 열을 차례로
        if is_safe(k, c):
            X[k] = c
            nqueens(k + 1)

def is_safe(k, c):              # X[0] ~ X[k-1] 은 이미 정해짐
    for i in range(k):
        if X[i] == c:           # 같은 열 (같은 행은 이미 걸러져 있음)
            return False
        if abs(X[i] - c) == abs(i - k):   # 같은 대각선
            return False
    return True""")}
 <ul class="dot"><li>행마다 퀸을 하나씩 놓으므로 같은 행은 처음부터 생기지 않는다</li>
 <li>for 가 끝나면 이 행에는 더 놓을 곳이 없음 → 위 행으로 돌아감 = 백트랙{fn('판서 정정', '필기의 N-queens(k) / Nqueens(k+1) / pueudocode 등 이름 · 오타는 nqueens 로 통일. for 줄의 "$ c" 는 콜론.')}</li></ul>'''),
]))

# 4 ──────────────────────────────
dp_rows = [[f'{i} ({DP_A[i]})'] + ['T' if DP[i][s] else '' for s in range(16)] for i in range(3)]
CH.append(('4', 'Subset Sum (부분집합의 합)', '11주차 1차시 ~ 12주차 1차시, 예시 3', [
 unit('', f'''<dl class="def"><dt>문제</dt><dd>집합 {v('A')} 의 부분집합 중 {hl('원소의 합이 S 가 되는 부분집합')}이 존재하는지 (혹은 그 부분집합이 무엇인지)</dd>
 <dt>예시</dt><dd>{v('A')} = {{8, 6, 7, 5, 3, 10, 9}}, {v('S')} = 15 → 답 4개: {{8, 7}}, {{7, 5, 3}}, {{5, 10}}, {{6, 9}}{fn('판서 정정', '필기의 A 는 {8, 6, 7, 5, 4, 10, 9} 였으나, 답 {7, 5, 3} 이 나오려면 4 가 아니라 3 이다 (12주차 1차시 판서로 확인).')}</dd></dl>
 <ul class="dot"><li>예전에 한 부분합 최대 (연속된 구간) 와 다름 — 순서 상관없고 연속되지 않아도 됨 → 백트래킹으로 풀 수 있음</li>
 <li>원소마다 넣는다 / 안 넣는다 2가지 → 부분집합의 개수 {hl('2<sup>|A|</sup>')}개를 하나씩 체크</li></ul>'''),
 unit('subsetsum1 — 있으면 True', f'''{code('pseudocode', 'subsetsum1(A, S) — 모든 원소는 양의 정수', """
def subsetsum1(A, S):
    if S == 0:                    # 딱 맞게 떨어짐
        return True
    if S < 0 or len(A) == 0:      # 넘쳤거나 더 가져올 원소가 없음
        return False
    z = A[0]                      # 0번째 원소를 넣을지 말지
    B = A[1:]
    with_z = subsetsum1(B, S - z)     # 포함: S 가 z 만큼 줄어듦
    without_z = subsetsum1(B, S)      # 제외: S 는 그대로
    return with_z or without_z        # 하나만 True 여도 True""")}
 <p>필기의 with, without 은 파이썬 예약어 (with) 와 겹쳐 이름을 바꿨다.{fn('보충', 'with 는 파이썬 키워드라 실제 코드에서는 변수 이름으로 쓸 수 없다. 의사코드로는 의미가 같다.')}</p>'''),
 unit('재귀 탐색 트리 — A = [8, 6, 7], S = 15', f'''<figure>{FIG_SS}<figcaption>노드 = 남은 목표 S, 가지 ○ = 원소를 넣음, ✕ = 안 넣음. 노랑 = 답, 점선 = 보류 (탐색 안 함)</figcaption></figure>
 <ul class="dot"><li>8 ○ → S = 7 → 6 ○ → S = 1 → 7 ○ 이면 S = −6 (가망 없음) → 백트랙 → 7 ✕ 이면 S = 1 인데 원소가 없음 → 백트랙</li>
 <li>S = 7 로 돌아가 6 ✕ → S = 7 → 7 ○ → {hl('S = 0 → True')}, 더 백트래킹할 필요 없음{fn('보충', '교수님 설명대로 첫 True 에서 멈췄다. 위 코드는 with 와 without 을 둘 다 계산한 뒤 or 하므로 실제로는 나머지도 돈다. return subsetsum1(B, S − z) or subsetsum1(B, S) 로 쓰면 첫 True 에서 멈춘다.')}</li>
 <li>루트의 8 ✕ 쪽 (S = 15) 은 선택한 쪽을 타고 가다 백트래킹할 것이므로 보류</li></ul>'''),
 unit('subsetsum2 — 남은 원소를 인덱스 i 로', f'''{code('pseudocode', 'subsetsum2(A, i, S) — {A[0], …, A[i]} 중 합이 S 인 부분집합이 있는가', """
def subsetsum2(A, i, S):
    if S == 0:
        return True
    elif S < 0 or i == -1:
        return False
    else:                                # A[i] 를 넣을지 말지
        with_i = subsetsum2(A, i - 1, S - A[i])
        without_i = subsetsum2(A, i - 1, S)
        return with_i or without_i
# 호출: subsetsum2(A, len(A) - 1, S)""")}
 <p>subsetsum1 과 하는 일은 같고, 배열을 잘라 넘기는 대신 {hl('인덱스 i 하나만 줄여')} 넘긴다 → 인자가 (i, S) 두 숫자라서 점화식 · DP 테이블로 옮길 수 있다.{fn('보충', '필기의 질문 "저번 코드랑 뭐가 다른지" 에 대한 답.')}</p>'''),
 unit('점화식 → DP 테이블 · O(nS) 와 그 문제', f'''<div class="eq">DP[{v('i')}][{v('S')}] = DP[{v('i')} − 1][{v('S')} − A[{v('i')}]] or DP[{v('i')} − 1][{v('S')}]</div>
 <p>DP[{v('i')}][{v('S')}] = A[0] ~ A[{v('i')}] 로 합 {v('S')} 를 만들 수 있으면 True. 원하는 값은 마지막 칸 DP[{v('n')} − 1][{v('S')}].</p>
 {table(['i (A[i])'] + [f'^{s}' for s in range(16)], dp_rows, ['12%'] + ['5.5%'] * 16)}
 <p>A = [8, 6, 7], S = 15: 빈칸 = False. DP[2][15] = T. 표의 크기 = 행 {v('n')} × 열 ({v('S')} + 1), 칸마다 or 한 번 (기본 연산) → {hl(f'O({v("n")}{v("S")})')}</p><p><b>문제점</b> — 예: {v('A')} = [1억, 5억, 1.5억, …, 7억] (10개), {v('S')} = 20억 → O({v('n')}{v('S')}) = O(10 × 20억). 수행시간에 입력의 {hl('크기가 아니라 값')} ({v('S')}) 이 들어가면 비정상적으로 크게 유추될 수 있다 → 바람직하지 않음.{fn('보충', '이런 수행시간을 의사 다항 시간 (pseudo-polynomial time) 이라고 한다. S 를 나타내는 비트 수 log S 로 보면 S 는 그 지수이다.')}</p>'''),
 unit('subsetsum_sol — 답 하나를 반환', f'''{code('pseudocode', 'subsetsum_sol(A, S) — 답 부분집합 하나, 없으면 None', """
def subsetsum_sol(A, S):
    if S == 0:
        return []                    # 다 맞췄음
    if S < 0 or len(A) == 0:
        return None                  # 불가능
    z = A[0]
    B = A[1:]
    result = subsetsum_sol(B, S - z)     # z 를 넣고 시도
    if result is not None:
        return [z] + result              # 성공 → z 를 앞에 붙임
    return subsetsum_sol(B, S)           # 실패 → z 를 빼고 시도""")}
 <p>z = 이번에 넣을지 정할 원소, B = 나머지 원소 (재귀에 넘기려고 나눈 것).{fn('판서 정정', '필기의 result [Z] + result 는 return [z] + result (return 과 + 빠짐). 대문자 Z 는 원소 하나라 소문자 z 로.')}</p>'''),
 unit('subsetsum_sol2 — 답을 모두 출력', f'''<p>{v('X')} = 원소마다 넣으면 1, 안 넣으면 0. 예: [1, 0, 1, 0, 0, 0, 0] = {{8, 7}}, [0, 0, 0, 1, 0, 1, 0] = {{5, 10}}.</p>
 {code('pseudocode', 'subsetsum_sol2(k) — X[k] 결정, 첫 호출 subsetsum_sol2(0)', """
def subsetsum_sol2(k):
    if k == n:                       # X 를 다 정함
        current_sum = 0
        for i in range(n):
            if X[i] == 1:
                current_sum += A[i]
        if current_sum == S:
            print(X)
        return
    X[k] = 1                         # A[k] 넣고
    subsetsum_sol2(k + 1)
    X[k] = 0                         # A[k] 빼고
    subsetsum_sol2(k + 1)""")}
 <p>{v('k')} == {v('n')} 이면 넣기로 한 원소의 합을 구해 S 와 같을 때 출력하고 돌아간다.{fn('판서 정정', '필기의 if i in range(n) 은 for, print X 는 print(X), k == n 일 때 return 이 빠져 있었다 (없으면 X[n] 을 건드림).')}</p>'''),
 unit('더 효율적으로 — 정렬 + 가지치기', f'''<p>{v('A')} 를 {hl('오름차순 정렬')}: [3, 5, 6, 7, 8, 9, 10]. 3 ○ 5 ✕ 6 ○ 에서 7 을 넣으면 15 를 넘음 → 오름차순이므로 그 뒤도 볼 필요 없음.</p>
 {code('pseudocode', '넣는 부분 교체', """
    if current_sum + A[k] <= S:      # 넣어도 S 를 넘지 않을 때만
        X[k] = 1
        subsetsum_sol2(k + 1)""")}
 <p>호출은 subsetsum_sol2(0). 재귀 호출 수 {hl('255 → 93')} (보충, 코드로 확인).{fn('보충', '교체한 줄의 current_sum 은 원래 코드에서 k == n 일 때만 계산된다. 실제로는 지금까지의 합을 인자로 넘겨야 한다: def subsetsum_sol2(k, current_sum) … subsetsum_sol2(k + 1, current_sum + A[k]).')}</p>'''),
]))

# 5 ──────────────────────────────
CH.append(('5', '백트래킹 일반형 · 한계함수 · 상태 공간 트리', '12주차 1차시', [
 unit('일반형', f'''<p>해 {x_(0)}, {x_(1)}, …, {x_(v('n') + ' − 1')} 를 차례로 다 해 보는 것.</p>
 {code('pseudocode', 'Backtrack(k) — X[k] 결정, 첫 호출 Backtrack(0)', """
def Backtrack(k):
    if k >= n:
        output solution              # 해인지 확인하고 해면 출력
        return
    for each possible candidate c for X[k]:     # 후보를 하나씩
        if B(X[0], X[1], ..., X[k-1], c) == True:
            X[k] = c
            Backtrack(k + 1)""")}
 <p>후보 c 는 subset sum 이면 0 / 1, N-Queens 면 0 ~ N − 1 처럼 문제마다 다르다.{fn('판서 정정', 'condidate → candidate.')}</p>'''),
 unit('한계함수 B (bounding function)', f'''<dl class="def"><dt>B</dt><dd>지금까지 정한 {x_(0)} ~ {x_(v('k') + ' − 1')} 에 후보 c 를 더했을 때 {hl('조건과 충돌하는지')} 체크하는 함수 — 문제마다 다름</dd></dl>
 {table(['문제', 'B 가 검사하는 것'], [['N-Queens', '같은 열 · 대각선에 있는지 (is_safe)'], ['Subset Sum', '지금까지 합 + A[k] ≤ S 인지'], ['미로', '벽 · 미로 밖인지'], ['0/1 Knapsack', '무게 ≤ K 인지, 상한 &gt; MP 인지 (7장)']], ['30%', '70%'])}
 <p>백트래킹은 모든 가지 수를 고려해서 비효율적이지만, {hl('B 를 잘 설계해 쓸데없는 것을 제외')}하면 시간을 크게 줄여 쓸 만한 알고리즘이 된다.{fn('확인 필요', 'N-Queens 의 B 를 판서에서 정확히 어떻게 적으셨는지 필기에 없다 ("못 들음").')}</p>'''),
 unit('상태 공간 트리 (State-Space Tree, SST)', f'''<p>재귀 탐색 트리의 각 노드 (예: S = 15) 를 {hl('상태 (state)')} 라 하고, 이 트리를 {hl('SST')} 라 부른다.{fn('주의', '용어를 외우라는 것이 아니라 지식으로 알려 주신 것 (교수님).')}</p>
 <p>4 × 4 미로 (0 = 빈칸, 1 = 벽): 0111 / 0010 / 1011 / 0000. 왼쪽 가지 ↓, 오른쪽 가지 →. (2, 0) 처럼 갈 수 없는 가지를 판단하는 것이 한계함수.</p>
 <figure>{FIG_SST4}<figcaption>빨강 ✕ = 벽 · 미로 밖, 노랑 = 도착. 첫 해에서 멈춤</figcaption></figure>'''),
]))

# 6 ──────────────────────────────
CH.append(('6', 'Knapsack 문제', '12주차 2차시', [
 unit('', f'''<dl class="def"><dt>문제</dt><dd>용량 {v('K')} 인 배낭 (knapsack) 에 {hl('무게 합이 K 를 넘지 않게')} 아이템을 골라 담아 {hl('가치 합을 최대')}로</dd>
 <dt>예시</dt><dd>{v('K')} = 16, 무게 {v('S')} = [2, 5, 10, 5], 가치 {v('P')} = [40, 30, 50, 10]</dd></dl>
 {table(['조건', '내용'], [['1 (제약)', '선택한 아이템의 무게 합 ≤ K'], ['2 (목표)', '선택한 아이템의 가치 합 최대']], ['25%', '75%'])}{fn('판서 정정', '필기의 K-=16 → K = 16.')}'''),
 unit('두 종류', f'''{table(['', 'fractional knapsack', '0/1 knapsack'], [['뜻', '아이템을 쪼개 담을 수 있음 (일부만 넣어도 됨)', '넣거나 (1) 안 넣거나 (0), 쪼갤 수 없음'], ['예', '무게 2 · 가치 40 → 무게 1 · 가치 20 두 조각', '통째로만'], ['풀이', '가성비 그리디', '백트래킹']], ['16%', '42%', '42%'])}
 <div class="eq">fractional 최적 해의 가치 ≥ 0/1 최적 해의 가치 (항상)</div>
 <p>쪼개서 빈칸 없이 꽉꽉 채울 수 있기 때문. {hl('이 사실이 0/1 을 푸는 알고리즘에서 상한으로 쓰인다')} (7장).</p>'''),
 unit('fractional — 가성비 그리디', f'''<div class="figrow"><figure>{FIG_FR}</figure><div>
 <p>가성비 {v('P')} / {v('S')} = 20, 6, 5, 2 (이미 가성비 순으로 나열). 가성비 좋은 것부터 최대로 넣음 = 그리디.</p>
 <ul class="dot"><li>1번 (2), 2번 (5) 통째로</li><li>3번은 다 못 넣고 9 만큼 → 9 × 5 = 45</li><li>가치 {hl('115')}</li></ul>
 <p>그리디 단원이 아니라서 최적성 증명은 생략 (그리디 증명은 귀류법).</p></div></div>'''),
 unit('0/1 — 가성비 순서로는 최적이 아님', f'''<div class="figrow"><figure>{FIG_80}</figure><figure>{FIG_90}</figure></div>
 <p>가성비 순서로 넣으면 2 (40), 5 (30), 10 은 넘침, 5 (10) → 빈칸 4, 가치 80. 하지만 2 (40) 다음 바로 10 (50) 을 넣으면 {hl('90')} 이 더 크다 → 0/1 은 {hl('백트래킹')}으로 모든 가짓수를 보며 푼다.</p>'''),
]))

# 7 ──────────────────────────────
CH.append(('7', '0/1 Knapsack 백트래킹', '12주차 2차시 ~ 13주차 1차시', [
 unit('상태 공간 트리와 노드 v · p(v) · s(v)', f'''<p>예시 {v('P')} = [15, 16, 6], {v('S')} = [3, 4, 2], {v('K')} = 5, 가성비 5, 4, 3 (정렬되어 있지 않으면 먼저 정렬). 답의 형태 {v('X')} = [_, _, _] → 2<sup>3</sup> = 8가지. 아이템 4개면 2<sup>4</sup> = 16가지를 봐야 하는 것이 백트래킹의 단점.</p>
 <p>{v('X')} = [] 에서 시작, 왼쪽 가지 {x_(0)} = 1 (넣음), 오른쪽 가지 {x_(0)} = 0 (안 넣음). [1] 의 자식은 [1, 1], [1, 0] …</p><figure>{FIG_V}</figure>
 <p>v 에서 {x_(v('i'))} 를 정하고, v 의 두 자식 아래에서 {x_(v('i') + ' + 1')} ~ {x_(v('n') + ' − 1')} 를 정한다.{fn('보충', 'v 를 루트로 하는 서브트리 전체로 보면 X[i] 도 정하므로 i ~ n − 1.')}</p>'''),
 unit('한계함수 — MP 와 두 가지의 상한', f'''<dl class="def"><dt>MP</dt><dd>maximum current profit — {hl('지금까지 찾은 답 중 가장 큰 가치')}</dd>
 <dt>상한</dt><dd>그 가지에서 얻을 수 있는 가치의 최댓값 = 남은 용량을 {hl('fractional 로 채운 값')} (0/1 ≤ fractional 이므로)</dd></dl>
 {table(['', '왼쪽 X[i] = 1', '오른쪽 X[i] = 0'], [['남은 용량', 'K − s(v) − S[i]', 'K − s(v)'], ['상한', 'p(v) + P[i] + fractional(i + 1, K − s(v) − S[i])', 'p(v) + fractional(i + 1, K − s(v))'], ['방문 안 함', '상한 ≤ MP', '상한 ≤ MP']], ['18%', '41%', '41%'])}
 <p>거르는 3가지: ① 이미 넘쳐서 들어갈 수 없는 가지 ② 넣어도 되는데 굳이 안 넣는 가지 (상한 ≤ MP) ③ {hl('fractional 상한 ≤ MP')} — ③ 이 가장 중요.{fn('보충', '② 와 ③ 은 같은 식 (오른쪽 상한 ≤ MP). ② 는 남은 아이템이 없어 fractional 부분이 0 인 경우.')}</p>'''),
 unit('예시 탐색 (판서)', f'''<figure>{FIG_KSST}<figcaption>빨간 점선 = 거른 가지, 노랑 = 답</figcaption></figure>
 {table(['^단계', '가지', '계산', '판단'], [
   ['1', '[ ] → X[0] = 1', '0 + 15 + frac(1, 2) = 15 + 8 = 23', '23 &gt; MP 0 → [1] (p 15, s 3)'],
   ['2', '[1] → X[1] = 1', '무게 4 &gt; 남은 2', '① 넘침'],
   ['3', '[1] → X[1] = 0', '15 + frac(2, 2) = 15 + 6 = 21', '21 &gt; MP → [1, 0] (p 15, s 3 그대로)'],
   ['4', '[1, 0] → X[2] = 1', '15 + 6 + frac(3, 0) = 21', '&gt; MP → [1, 0, 1] → ' + hl('MP = 21')],
   ['5', '[1, 0] → X[2] = 0', '15 + frac(3, 2) = 15 + 0 = 15', '15 ≤ 21 → ②'],
   ['6', '[ ] → X[0] = 0', '0 + frac(1, 5) = 16 + 3 = 19', '19 ≤ 21 → ③']], ['9%', '22%', '37%', '32%'])}
 <ul class="dot"><li>frac(a, b): a = 다음에 볼 아이템 (i + 1), b = 남은 용량. frac(1, 2) 는 아이템 1 (4, 16) 을 2 만큼 → 16 × {frac(2, 4)} = 8, frac(1, 5) 는 16 + 아이템 2 반 (6 × {frac(1, 2)} = 3) = 19</li>
 <li>[1, 0] 의 s(v) 가 3 인 이유: fractional 은 상한을 본 것이지 실제로 넣은 것이 아님</li>
 <li>19 는 찾은 답이 아니라 상한 — 쪼갠 값이라 0/1 로는 만들 수 없음</li>
 <li>결과 {hl('MP = 21, X = [1, 0, 1]')}{fn('확인 필요', '판서는 [1] 에서 MP 를 15 (지금 가치) 로 갱신했고, 아래 update_best 코드는 잎 · 꽉 찼을 때만 갱신한다 (그 경우 [1] 에서 MP = 0). 이 예에서는 판단과 결과가 같다.')}</li></ul>'''),
 unit('코드 — frac_knapsack', f'''<p>B = 남은 아이템으로 더 얻을 수 있는 가치의 상한 (fractional). 변수: S[i] 크기, P[i] 가치, K 배낭 크기, n 아이템 수, size 남은 용량.</p>{code('python', 'frac_knapsack(i, size) — B = 아이템 i ~ n-1 을 size 에 fractional 로', """
def frac_knapsack(i, size):
    B = 0
    items = sorted(range(i, n), key=lambda j: P[j] / S[j], reverse=True)   # 가성비 내림차순
    for j in items:
        if size == 0:
            break
        if S[j] <= size:              # 통째로
            B += P[j]
            size -= S[j]
        else:                         # 넘침 → 남은 만큼 잘라서
            B += P[j] * (size / S[j])
            size = 0
    return B""")}'''),
 unit('코드 — knapsack · update_best', f'''{code('python', 'knapsack(i, size, profit) — X[i] 결정 (size = K − s(v), profit = p(v))', """
def knapsack(i, size, profit):
    if i >= n or size == 0:           # 다 정했거나 꽉 참
        update_best(profit)
        return
    if S[i] <= size:                  # X[i] = 1 (들어갈 때만)
        B = frac_knapsack(i + 1, size - S[i])
        if profit + P[i] + B > MP:
            X[i] = 1
            knapsack(i + 1, size - S[i], profit + P[i])
            X[i] = 0
    B = frac_knapsack(i + 1, size)    # X[i] = 0 (if 밖)
    if profit + B > MP:
        X[i] = 0
        knapsack(i + 1, size, profit)

def update_best(profit):              # MP 갱신
    if profit > MP:
        MP = profit
        best_X = X                    # 실제로는 X.copy()

knapsack(0, K, 0)                     # 실행 → print(MP), print(best_X)""")}
 <p>{hl('X[i] = 0 부분은 if 밖')} — 넘쳐서 못 넣어도 안 넣는 가지는 항상 검사한다.{fn('판서 정정', '필기에서 X[i] = 0 부분이 if S[i] <= size 안쪽에 들여써져 있었다 → 그러면 넘칠 때 안 넣는 가지까지 사라져 이 예시 답이 21 이 아니라 6 이 된다 (코드로 확인). if 밖이어야 한다. 그 밖에 Trure → True, uupdate_best · proffit → update_best · profit.')}{fn('보충', 'best_X = X 는 같은 리스트를 가리켜 나중에 바뀐다 → X.copy() (교수님: 의사코드라 신경 쓰지 않아도 됨). 실제 파이썬에서는 global MP, best_X 와 시작 전 X = [0] * n, MP = 0 이 필요.')}</p>'''),
]))

build(OUT, title='백트래킹 개념노트', run='알고리즘 - 개념노트 - 백트래킹 Backtracking',
      kick='알고리즘 · 윤지현 교수님 · 11주차 1차시 ~ 13주차 1차시', h1='백트래킹', h1_en='Backtracking',
      chapters=CH, pdf='backtracking.pdf')
print('ok', OUT, len(FN), 'notes')
