# 그리디 문제지 — 계산·검증 도우미 (모든 정답 값은 여기서 계산하고 assert 로 확인)
import heapq, itertools, random
from itertools import combinations

# ── 강의실 배정 ──
def assign(S, F):
    """F 오름차순 정렬된 입력 — 수업 코드 그대로. 추적 기록과 L 을 돌려줌"""
    L = [0]; k = 0; tr = []
    for i in range(1, len(S)):
        ok = F[k] <= S[i]; tr.append((i, S[i], k, F[k], ok))
        if ok: L.append(i); k = i
    return L, tr

def best_count(S, F):
    """겹치지 않는 강의의 최대 개수 (전수 조사) — 그리디 답이 정말 최적인지 확인용"""
    n = len(S); best = 0
    for r in range(1, n + 1):
        for c in combinations(range(n), r):
            c = sorted(c, key=lambda i: F[i])
            if all(F[c[j]] <= S[c[j + 1]] for j in range(len(c) - 1)): best = r; break
    return best

# ── 거스름돈 ──
def coin_greedy(units, m):
    out = []
    for u in sorted(units, reverse=True):
        out.append((u, m // u)); m %= u
    return out

def coin_opt(units, m):
    INF = 10 ** 9; d = [0] + [INF] * m
    for x in range(1, m + 1):
        d[x] = min(d[x - u] + 1 for u in units if u <= x)
    return d[m]

# ── 일의 개수 ──
def jobs(A, T):
    s = 0; take = []
    for t in sorted(A):
        if s + t > T: break
        s += t; take.append(t)
    return take

# ── 허프만 ──
def huffman(freq, newer_first=True):
    """먼저 꺼낸 노드 = 왼쪽(0). 빈도가 같으면 newer_first=True 일 때 새로 만든 노드를 먼저 꺼냄 (수업 트리와 같음)"""
    h = []; merges = []
    for i, (ch, f) in enumerate(sorted(freq.items(), key=lambda kv: kv[1])):
        heapq.heappush(h, (f, 0 if newer_first else i, ('leaf', ch, f)))
    step = 0
    while len(h) > 1:
        x = heapq.heappop(h); y = heapq.heappop(h)
        f = x[0] + y[0]; step += 1
        node = ('node', f, x[2], y[2]); merges.append((x[2], y[2], f))
        heapq.heappush(h, (f, -step if newer_first else 1000 + step, node))
    return h[0][2], merges

def codes(t, p=''):
    if t[0] == 'leaf': return {t[1]: p or '0'}
    d = {}; d.update(codes(t[2], p + '0')); d.update(codes(t[3], p + '1')); return d

def cost(freq, code): return sum(freq[c] * len(code[c]) for c in freq)

def name(n): return n[1] if n[0] == 'leaf' else str(n[1])

def prefix_free(code):
    v = list(code.values()); return not any(a != b and b.startswith(a) for a in v for b in v)

# ── 트리 그림 (해설용 SVG) ──
def tree_svg(t, title='허프만 트리'):
    leaves = []; pos = {}
    def lay(n, d):
        if n[0] == 'leaf':
            x = len(leaves); leaves.append(n); pos[id(n)] = (x, d); return x
        a = lay(n[2], d + 1); b = lay(n[3], d + 1); x = (a + b) / 2; pos[id(n)] = (x, d); return x
    lay(t, 0)
    depth = max(p[1] for p in pos.values())
    GX, GY, PX, PY = 62, 58, 34, 22
    W = int(PX * 2 + GX * (len(leaves) - 1)); H = PY * 2 + GY * depth + 10
    X = lambda n: PX + pos[id(n)][0] * GX; Y = lambda n: PY + pos[id(n)][1] * GY
    o = [f'<svg viewBox="0 0 {W} {H}" style="width:100%;max-width:{min(W, 480)}px;height:auto;display:block;margin:8px 0" role="img"><title>{title}</title>']
    def draw(n):
        if n[0] == 'leaf': return
        for c, lab in ((n[2], '0'), (n[3], '1')):
            x1, y1, x2, y2 = X(n), Y(n), X(c), Y(c)
            o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#141414" stroke-width="1.4"/>')
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            o.append(f'<text x="{mx + (-11 if lab == "0" else 11)}" y="{my - 3}" font-size="16" font-weight="700" text-anchor="middle" fill="#141414">{lab}</text>')
            draw(c)
    draw(t)
    def box(n):
        x, y = X(n), Y(n)
        if n[0] == 'leaf':
            o.append(f'<rect x="{x - 29}" y="{y - 14}" width="58" height="28" fill="#fff" stroke="#141414" stroke-width="1.4"/>'
                     f'<text x="{x}" y="{y + 6}" font-size="17" text-anchor="middle" font-weight="700">{n[1]} {n[2]}</text>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="18" fill="#fff" stroke="#141414" stroke-width="1.4"/>'
                     f'<text x="{x}" y="{y + 5.5}" font-size="16" text-anchor="middle">{n[1]}</text>')
            box(n[2]); box(n[3])
    box(t); o.append('</svg>'); return ''.join(o)

# ── min heap (수업: extract_min = 루트 꺼내고 마지막을 루트로 → heapify_down / insert = 끝에 두고 heapify_up) ──
def extract_min(h):
    r = h[0]; h[0] = h[-1]; h.pop(); i = 0
    while True:
        l, rr, m = 2 * i + 1, 2 * i + 2, i
        if l < len(h) and h[l] < h[m]: m = l
        if rr < len(h) and h[rr] < h[m]: m = rr
        if m == i: break
        h[i], h[m] = h[m], h[i]; i = m
    return r

def insert(h, x):
    h.append(x); i = len(h) - 1
    while i > 0 and h[(i - 1) // 2] > h[i]:
        h[(i - 1) // 2], h[i] = h[i], h[(i - 1) // 2]; i = (i - 1) // 2
