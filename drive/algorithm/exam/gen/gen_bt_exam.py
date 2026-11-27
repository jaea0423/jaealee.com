# 백트래킹 문제지 6개 — bt-0 (기초 OX) / bt-1a·1b·1c (기본 1·2·3회) / bt-2 (응용) / bt-3 (심화)
# 계산 값은 bt_common 으로 구하고 assert 로 확인
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bt_common import *
W = '2026년 11월 27일 작성'
SRC = {
 'bt': ['11-1', 's1', '백트래킹'], 'maze': ['11-1', 's2', '미로 탈출'], 'feat': ['11-1', 's3', '백트래킹의 특징'], 'maze5': ['11-1', 's4', '5 × 5 미로'],
 'fw': ['11-1', 's6', 'find_way'], 'nq': ['11-1', 's7', 'N-Queens'], 'safe': ['11-1', 's8', 'is_safe'], 'ss': ['11-1', 's9', 'Subset Sum'],
 'ss1': ['11-1', 's10', 'subsetsum1'], 'sstree': ['11-1', 's11', '재귀 탐색 트리'], 'fwfix': ['12-1', 's1', 'find_way 들여쓰기'],
 'ss2': ['12-1', 's2', 'subsetsum2'], 'dp': ['12-1', 's3', 'DP · O(nS)'], 'ons': ['12-1', 's4', 'O(nS) 의 문제'], 'sol': ['12-1', 's5', 'subsetsum_sol'],
 'sol2': ['12-1', 's6', 'subsetsum_sol2'], 'prune': ['12-1', 's7', '가지치기'], 'gen': ['12-1', 's8', '일반형 · 한계함수'], 'sst': ['12-1', 's9', 'SST'],
 'kn': ['12-2', 's1', 'Knapsack'], 'two': ['12-2', 's2', 'fractional · 0/1'], 'fr': ['12-2', 's3', 'fractional 풀이'], 'g01': ['12-2', 's4', '0/1 가성비 순'],
 'kbt': ['12-2', 's5', '0/1 은 백트래킹'], 'k3': ['12-2', 's6', '아이템 3개 예시'], 'v': ['12-2', 's7', '노드 v'], 'bound': ['12-2', 's8', '한계함수 MP'],
 'B': ['13-1', 's1', 'B 와 변수'], 'frk': ['13-1', 's2', 'frac_knapsack'], 'kcode': ['13-1', 's3', 'knapsack'], 'upd': ['13-1', 's4', 'update_best'], 'board': ['13-1', 's5', '판서 트리'],
}
def src(*k): return [SRC[x] for x in k]
def P_(slug, title, level, scope, exam): page(slug, title, level, scope, exam, written=W)

# ═════════ 공통 값 ═════════
G4 = ['0111', '0010', '1011', '0000']; T4, P4 = maze_sst(G4); assert P4 == [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]
Q4, Q4s = queens_sst(4); assert Q4s == [1, 3, 0, 2] and count(Q4, 'x') == 18
A3 = [8, 6, 7]; SS3 = ss_sst(A3, 15)
A7 = [8, 6, 7, 5, 3, 10, 9]; assert sorted(map(sorted, subsets(A7, 15))) == [[3, 5, 7], [5, 10], [6, 9], [7, 8]]
K3 = ([15, 16, 6], [3, 4, 2], 5); r3 = knap_bt(*K3); assert r3[0] == 21 and r3[1] == [1, 0, 1]
assert frac(*K3[:2], 0, 16) == 0 or True
assert frac([40, 30, 50, 10], [2, 5, 10, 5], 0, 16) == 115 and knap_opt([40, 30, 50, 10], [2, 5, 10, 5], 16) == 90
pth = lambda p: ' → '.join(f'({x},{y})' for x, y in p)
FW_CODE = '''
def find_way(x, y):
    if x == n - 1 and y == n - 1:
        return true
    if M[x][y] == safe:
        try_down = find_way(x + 1, y)
        if try_down == true:
            return true
        try_east = find_way(x, y + 1)
        return try_east
    else:
        return false'''

# ════════════════ bt-0 기초 OX ════════════════
B0 = [
OX('백트래킹 개념', 15, '백트래킹 알고리즘에 대한 설명이다.', [
 ('진행하다 막히면 가장 최근의 선택으로 되돌아가 다른 선택을 해 본다.', True, '진행 → 막힘 → back-track.'),
 ('해가 하나 이상 존재하면 백트래킹은 반드시 해를 찾는다.', True, '가능한 방식을 다 해 보기 때문.'),
 ('백트래킹은 항상 다항 시간 안에 끝난다.', False, '모든 경우 (예: 2<sup>n</sup>) 를 볼 수 있어 오래 걸린다.'),
 ('백트래킹은 그리디 · 분할 정복 · DP 로 풀기 어려울 때 쓰는 최후의 보루이다.', True, '비효율적이라서 (교수님).'),
 ('한 번 고른 선택을 되돌리지 않는다는 점에서 그리디와 같다.', False, '되돌리는 것이 백트래킹의 핵심. 그리디는 되돌리지 않음.'),
 ('재귀 탐색 트리의 각 노드를 상태 (state) 라 하고, 이 트리를 상태 공간 트리 (SST) 라 한다.', True, 'State-Space Tree.'),
 ('한계함수 B 를 잘 설계하면 탐색할 필요 없는 가지를 빼서 효율을 높일 수 있다.', True, '쓸데없는 가지를 제외.'),
], src('bt', 'feat', 'gen', 'sst')),
OX('미로 탈출', 15, '남쪽 (↓), 동쪽 (→) 만 갈 수 있고 남쪽을 먼저 시도하는 미로 문제와 find_way(x, y) 에 대한 설명이다.', [
 ('find_way 의 첫 호출은 find_way(0, 0) 이다.', True, '시작 = 왼쪽 위.'),
 ('M[x][y] 에서 x 는 열, y 는 행이다.', False, 'x = 행, y = 열 (수업 정의).'),
 ('남쪽 시도가 실패하면 동쪽을 시도하는 것이 백트랙이다.', True, '돌아와서 안 해 본 선택.'),
 ('"도착이면 true", "흰 칸이면 탐색", "아니면 false" 세 블록은 같은 들여쓰기 높이여야 한다.', True, '12-1 판서 정정.'),
 ('수업 4 × 4 미로 (0111 / 0010 / 1011 / 0000) 에서 찾은 길은 (1, 1) 을 지난다.', True, pth(P4) + '.'),
 ('수업 코드는 미로 밖으로 나가는 경우를 따로 검사한다.', False, '검사가 없다 — 실제로는 x ≥ n or y ≥ n 검사가 필요 (보충).'),
 ('5 × 5 수업 미로에서 (4, 0) 은 들어갔다가 되돌아온 칸이다.', True, '아래로 끝까지 갔다가 막혀 백트랙.'),
], src('maze', 'maze5', 'fw', 'fwfix')),
OX('N-Queens', 15, 'N × N 체스판에 퀸 N 개를 놓는 문제와 X[k] = k 행 퀸의 열 인덱스 표기에 대한 설명이다.', [
 ('퀸끼리는 같은 행, 같은 열, 같은 대각선에 있으면 안 된다.', True, '문제 조건.'),
 ('행마다 퀸을 하나씩 놓으므로 is_safe 는 같은 행을 검사하지 않는다.', True, 'X[k] 로 행이 이미 다름.'),
 ('4-Queens 의 답은 [1, 3, 0, 2] 하나뿐이다.', False, '[2, 0, 3, 1] 까지 2개.'),
 ('|X[i] − c| == |i − k| 이면 두 퀸은 같은 대각선에 있다.', True, '밑변 = 높이.'),
 ('대각선 검사에서 절댓값을 쓰는 이유는 퀸이 왼쪽 위에 있을 수도 있어서이다.', True, '부호가 반대.'),
 ('0 열부터 놓아 보는 순서로 탐색하면 4-Queens 에서 처음 찾는 해는 [2, 0, 3, 1] 이다.', False, '[1, 3, 0, 2] 가 먼저 (X[0] = 1 이 2 보다 앞).'),
 ('nqueens(k) 의 for 문이 끝나면 위 행으로 되돌아간다.', True, '더 놓을 곳이 없음 = 백트랙.'),
], src('nq', 'safe')),
OX('Subset Sum', 20, '집합 A 의 부분집합 중 합이 S 인 것을 찾는 문제 (모든 원소는 양의 정수) 에 대한 설명이다.', [
 ('원소가 n 개면 확인할 부분집합은 2<sup>n</sup> 개이다.', True, '원소마다 넣음 / 안 넣음.'),
 ('subsetsum1 은 S == 0 이면 True 를 반환한다.', True, '딱 맞게 떨어짐.'),
 ('subsetsum1 에서 원소 z 를 넣으면 재귀 호출의 S 는 S + z 가 된다.', False, 'S − z (남은 목표가 줄어듦).'),
 ('연속된 구간의 합을 구하는 부분합 최대 문제와 달리 순서 · 연속이 상관없다.', True, '수업 비교.'),
 ('DP[i][S] = DP[i−1][S−A[i]] or DP[i−1][S] 로 채우면 수행시간은 O(nS) 이다.', True, '표 n × (S + 1), 칸마다 or.'),
 ('O(nS) 는 입력의 크기만으로 정해지는 바람직한 수행시간이다.', False, 'S 라는 입력의 <b>값</b>이 들어가 바람직하지 않음.'),
 ('A 를 오름차순 정렬하고 current_sum + A[k] ≤ S 일 때만 넣으면 탐색이 줄어든다.', True, '수업 예 255 → 93 호출.'),
 ('subsetsum_sol 은 가능한 답을 모두 반환한다.', False, '하나만 반환. 모두 출력은 subsetsum_sol2.'),
], src('ss', 'ss1', 'dp', 'ons', 'sol', 'sol2', 'prune')),
OX('일반형 · 한계함수', 15, 'Backtrack(k) 일반형과 한계함수 B 에 대한 설명이다.', [
 ('Backtrack(k) 는 X[k] 를 정하는 함수이다.', True, '첫 호출 Backtrack(0).'),
 ('B 는 지금까지 정한 X[0] ~ X[k−1] 과 후보 c 가 조건과 충돌하는지 검사한다.', True, 'bounding function.'),
 ('B 는 모든 문제에서 같다.', False, '문제마다 다름 (N-Queens = is_safe, subset sum = 합 ≤ S …).'),
 ('후보 c 는 항상 0 또는 1 이다.', False, 'N-Queens 는 0 ~ N − 1.'),
 ('k ≥ n 이면 해인지 확인하고 해면 출력한다.', True, 'output solution.'),
 ('B 가 True 일 때만 X[k] = c 로 두고 Backtrack(k + 1) 을 호출한다.', True, '충돌 없을 때만 진행.'),
], src('gen', 'sst')),
OX('Knapsack', 20, '용량 K 인 배낭 문제 (fractional · 0/1) 와 0/1 백트래킹에 대한 설명이다.', [
 ('무게 합 ≤ K 를 지키면서 가치 합을 최대로 하는 문제이다.', True, '조건 1 · 2.'),
 ('fractional 은 아이템을 쪼개 일부만 넣을 수 있다.', True, '0/1 은 넣거나 안 넣거나.'),
 ('같은 입력에서 0/1 최적 가치가 fractional 최적 가치보다 클 수 있다.', False, '항상 fractional ≥ 0/1.'),
 ('fractional 은 가성비 P/S 가 큰 순서로 넣는 그리디로 풀린다.', True, 'K = 16 예: 115.'),
 ('0/1 도 가성비 순서로 넣으면 항상 최적이다.', False, '80 &lt; 90 반례.'),
 ('왼쪽 가지 (X[i] = 1) 의 상한은 p(v) + P[i] + fractional(i + 1, K − s(v) − S[i]) 이다.', True, '넣은 뒤 남은 공간을 fractional 로.'),
 ('오른쪽 가지 (X[i] = 0) 의 상한에도 P[i] 를 더한다.', False, '안 넣으므로 p(v) + fractional(i + 1, K − s(v)).'),
 ('상한이 MP 와 같으면 그 가지를 방문한다.', False, '상한 ≤ MP 면 방문 안 함 (코드는 &gt; MP 일 때만 방문).'),
 ('fractional 로 구한 상한 19 는 그 가지에서 실제로 만들 수 있는 0/1 가치이다.', False, '쪼갠 값이라 실제로는 만들 수 없을 수 있음 (상한일 뿐).'),
], src('kn', 'two', 'fr', 'g01', 'bound')),
]
P_('bt-0', 'F. 백트래킹 — 기초 OX', '기초', '11주차 1차시 ~ 13주차 1차시 — 백트래킹 · 미로 · N-Queens · Subset Sum · 일반형 · Knapsack', B0)

# ════════════════ bt-1a 기본 1회 — 수업 값 · 수업 기호 ════════════════
fwq = FW_CODE.replace('find_way(x + 1, y)', '(가)').replace('try_east = find_way(x, y + 1)', 'try_east = (나)').replace('    else:\n        return false', '    else:\n        (다)')
B1A = [
dict(type='essay', lv='중', unit='미로 SST', pts=12,
 q=f'<p>4 × 4 미로 (회색 = 벽) 에서 (0, 0) 에서 (3, 3) 까지 간다. 남쪽 (↓) 을 왼쪽 가지로 먼저, 동쪽 (→) 을 오른쪽 가지로 나중에 탐색하고, 첫 해에서 멈춘다.</p>{maze_html(G4)}<p>(1) 상태 공간 트리를 그리시오 (갈 수 없는 노드는 X, 도착은 O).<br>(2) 찾은 경로를 쓰시오.</p>',
 model=tree_svg(T4, '미로 SST') + f'(2) {pth(P4)}', rubric=[['트리 구조 · 순서', 5], ['X 노드 3개 ((2,0), (4,1), (4,2))', 4], ['경로', 3]], src=src('sst', 'maze')),
dict(type='table', lv='하', unit='find_way', pts=8, q='<p>find_way 의 빈칸을 채우시오.</p>' + pre(fwq), head=['빈칸', '답'],
 rows=[['(가)', Bk('find_way(x + 1, y)', 'find_way(x+1, y)', 'find_way(x+1,y)')], ['(나)', Bk('find_way(x, y + 1)', 'find_way(x, y+1)', 'find_way(x,y+1)')], ['(다)', Bk('return false', 'return False')]],
 exp='남쪽 = 행 + 1 → (x + 1, y) 먼저, 실패하면 동쪽 = 열 + 1. 벽이면 false.', src=src('fw')),
dict(type='short', lv='하', unit='N-Queens', pts=6, q='<p>4-Queens 를 0행부터, 각 행에서 0열부터 놓아 보는 백트래킹으로 풀 때 처음 찾는 해 X 를 쓰시오. (X[k] = k 행 퀸의 열)</p>',
 show='[1, 3, 0, 2]', alt=['1,3,0,2', '1 3 0 2'], exp='X[0] = 0 아래는 모두 실패 → X[0] = 1 → [1, 3, 0, 2]. 다른 해 [2, 0, 3, 1] 은 그 뒤.', src=src('nq')),
dict(type='table', lv='하', unit='is_safe', pts=9, q='<p>is_safe(k, c) 의 빈칸을 채우시오.</p>' + pre('''
def is_safe(k, c):
    for i in range(k):
        if (가):            # 같은 열
            return False
        if (나):            # 같은 대각선
            return False
    return (다)'''), head=['빈칸', '답'],
 rows=[['(가)', Bk('X[i] == c', 'X[i]==c')], ['(나)', Bk('abs(X[i] - c) == abs(i - k)', 'abs(X[i]-c)==abs(i-k)', '|X[i]-c| == |i-k|')], ['(다)', Bk('True')]],
 exp='밑변 |X[i] − c| = 높이 |i − k| 이면 대각선. 위쪽 퀸 모두와 안 겹치면 True.', src=src('safe')),
dict(type='table', lv='하', unit='subsetsum1', pts=9, q='<p>subsetsum1 의 빈칸을 채우시오.</p>' + pre('''
def subsetsum1(A, S):
    if (가):
        return True
    if (나):
        return False
    z = A[0]
    B = A[1:]
    return subsetsum1(B, (다)) or subsetsum1(B, S)'''), head=['빈칸', '답'],
 rows=[['(가)', Bk('S == 0', 'S==0')], ['(나)', Bk('S < 0 or len(A) == 0', 'S<0 or len(A)==0')], ['(다)', Bk('S - z', 'S-z')]],
 exp='딱 맞으면 True, 넘쳤거나 원소가 없으면 False. 넣으면 남은 목표 S − z.', src=src('ss1')),
dict(type='essay', lv='중', unit='Subset Sum 트리', pts=10, q='<p>A = [8, 6, 7], S = 15 에서 subsetsum1 의 재귀 탐색 트리를 그리시오. 노드에는 남은 S, 왼쪽 가지는 원소를 넣음 (○), 오른쪽은 안 넣음 (✕), 첫 True 에서 멈춘다.</p>',
 model=tree_svg(SS3, 'subset sum 트리', bw=70), rubric=[['넣음 먼저 순서', 3], ['S = −6, S = 1 (원소 없음) 에서 실패', 4], ['S = 0 에서 멈춤', 3]], src=src('sstree')),
dict(type='short', lv='하', unit='Subset Sum', pts=6, q='<p>A = {8, 6, 7, 5, 3, 10, 9}, S = 15 일 때 합이 15 인 부분집합의 개수를 쓰시오.</p>', show='4', alt=['4개'],
 exp='{8, 7}, {7, 5, 3}, {5, 10}, {6, 9}.', src=src('ss')),
dict(type='table', lv='중', unit='DP · O(nS)', pts=8, q='<p>subsetsum2 를 DP 로 바꾼다. 빈칸을 채우시오.</p><p>DP[i][S] = DP[i − 1][ (가) ] or DP[i − 1][ (나) ]</p>', head=['빈칸', '답'],
 rows=[['(가)', Bk('S - A[i]', 'S-A[i]')], ['(나)', Bk('S')], ['테이블 크기', Bk('n × (S + 1)', 'n*(S+1)', 'n(S+1)')], ['수행시간', Bk('O(nS)')], ['문제점 (한 단어)', Bk('값', '입력의 값')]],
 exp='수행시간에 입력의 크기가 아니라 값 S 가 들어가 S 가 크면 비정상적으로 커짐.', src=src('dp', 'ons')),
dict(type='table', lv='하', unit='fractional', pts=8, q='<p>K = 16, 무게 S = [2, 5, 10, 5], 가치 P = [40, 30, 50, 10] 을 fractional 로 푼다.</p>', head=['항목', '답'],
 rows=[['가성비 P/S', Bk('20, 6, 5, 2', '20,6,5,2')], ['3번째 아이템을 넣는 무게', Bk('9')], ['최대 가치', Bk('115')], ['0/1 최적 가치', Bk('90')]],
 exp='2 + 5 통째로 (70), 남은 9 → 3번째 9/10 → 45 → 115. 0/1 은 2 + 10 → 90 (가성비 순 80 은 최적 아님).', src=src('fr', 'g01')),
dict(type='table', lv='중', unit='0/1 추적', pts=12, q='<p>P = [15, 16, 6], S = [3, 4, 2], K = 5. 각 가지로 가기 전에 상한을 계산해 MP 와 비교한다 (상한 ≤ MP 면 안 감). 빈칸을 채우시오.</p>',
 head=['가지', '상한 (또는 이유)', '감 / 안 감'],
 rows=[['[ ] → X[0] = 1', Bk('23'), Bk('감')], ['[1] → X[1] = 1', Bk('넘침', '무게 초과', '4 > 2'), Bk('안 감')], ['[1] → X[1] = 0', Bk('21'), Bk('감')],
       ['[1, 0] → X[2] = 1', Bk('21'), Bk('감')], ['[1, 0] → X[2] = 0', Bk('15'), Bk('안 감')], ['[ ] → X[0] = 0', Bk('19'), Bk('안 감')], ['결과 X, MP', Bk('[1, 0, 1], 21', '[1,0,1], 21'), '']],
 exp='23 = 15 + frac(1, 2) = 15 + 8. 21 = 15 + frac(2, 2). [1, 0, 1] 에서 MP = 21. 15 = 15 + frac(3, 2) = 15 + 0. 19 = frac(1, 5) = 16 + 3.', src=src('k3', 'board')),
dict(type='table', lv='중', unit='knapsack 코드', pts=12, q='<p>knapsack(i, size, profit) 의 빈칸을 채우시오.</p>' + pre('''
def knapsack(i, size, profit):
    if (가):
        update_best(profit)
        return
    if S[i] <= size:
        B = frac_knapsack((나), (다))
        if (라) > MP:
            X[i] = 1
            knapsack(i + 1, size - S[i], profit + P[i])
            X[i] = 0
    B = frac_knapsack(i + 1, (마))
    if profit + B > MP:
        X[i] = 0
        knapsack(i + 1, size, profit)'''), head=['빈칸', '답'],
 rows=[['(가)', Bk('i >= n or size == 0', 'i>=n or size==0')], ['(나)', Bk('i + 1', 'i+1')], ['(다)', Bk('size - S[i]', 'size-S[i]')], ['(라)', Bk('profit + P[i] + B', 'profit+P[i]+B')], ['(마)', Bk('size')]],
 exp='다 정했거나 꽉 차면 MP 갱신. 넣는 가지 상한 = profit + P[i] + frac(i + 1, size − S[i]), 안 넣는 가지 = profit + frac(i + 1, size).', src=src('kcode')),
]
P_('bt-1a', 'F. 백트래킹 — 기본 1회', '기본', '<b>백트래킹 · 기본 1회</b> (11주차 1차시 ~ 13주차 1차시)<br>수업 예시 값 · 수업 기호 그대로 — 트리 그리기 · 코드 빈칸 · 추적', B1A)

# ════════════════ bt-1b 기본 2회 — 새 값 · 수업 기호 ════════════════
G4b = ['0011', '0100', '0001', '1100']; T4b, P4b = maze_sst(G4b); assert P4b == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (3, 3)]
Q5, Q5s = queens_sst(5); assert Q5s == [0, 2, 4, 1, 3]
A4b, S4b = [2, 4, 5, 9], 11; assert sol_first(A4b, S4b) == [2, 4, 5] and sol2_all(A4b, S4b) == [[1, 1, 1, 0], [1, 0, 0, 1]]
SS4b = ss_sst(A4b, S4b)
DPA, DPS = [2, 4, 5], 7
DPT = [[False] * (DPS + 1) for _ in DPA]
for i, a in enumerate(DPA):
    for s in range(DPS + 1):
        DPT[i][s] = s == 0 or (i == 0 and s == a) or (i > 0 and (DPT[i - 1][s] or (s >= a and DPT[i - 1][s - a])))
assert [s for s in range(8) if DPT[2][s]] == [0, 2, 4, 5, 6, 7]
KB = ([40, 30, 18, 10], [2, 3, 3, 5], 7); rB = knap_bt(*KB); assert rB[0] == 70 and rB[1] == [1, 1, 0, 0] and knap_opt(*KB) == 70
assert frac(*KB[:2], 1, 5) == 30 + 18 * Fr(2, 3) or True
SAFE3 = [c for c in range(4) if all(x != c and abs(x - c) != abs(i - 3) for i, x in enumerate([1, 3, 0]))]; assert SAFE3 == [2]
SAFE2 = [c for c in range(5) if all(x != c and abs(x - c) != abs(i - 2) for i, x in enumerate([0, 2]))]; assert SAFE2 == [4]
fr_b = lambda i, s: F_(frac(*KB[:2], i, s))
B1B = [
dict(type='essay', lv='중', unit='미로 SST', pts=12, q=f'<p>새 4 × 4 미로 (회색 = 벽) 에서 수업 규칙 (↓ 먼저, → 나중, 첫 해에서 멈춤) 으로 상태 공간 트리를 그리고 경로를 쓰시오.</p>{maze_html(G4b)}',
 model=tree_svg(T4b, '미로 SST') + pth(P4b), rubric=[['트리 · 순서', 5], [f'X 노드 {count(T4b, "x")}개', 4], ['경로', 3]], src=src('sst', 'maze')),
dict(type='table', lv='하', unit='is_safe', pts=10, q='<p>4-Queens 에서 X = [1, 3, 0] 까지 정했다. 3행의 각 열 c 에 대해 is_safe(3, c) 의 결과와 이유를 쓰시오.</p>', head=['c', '결과', '이유'],
 rows=[['0', Bk('False'), Bk('같은 열')], ['1', Bk('False'), Bk('같은 열')], ['2', Bk('True'), Bk('충돌 없음')], ['3', Bk('False'), Bk('같은 열')]],
 exp='X[2] = 0 → c = 0 같은 열, X[0] = 1 → c = 1 같은 열, X[1] = 3 → c = 3 같은 열. c = 2: |1−2|=1≠3, |3−2|=1≠2, |0−2|=2≠1 → True → [1, 3, 0, 2].', src=src('safe')),
dict(type='short', lv='중', unit='N-Queens', pts=6, q='<p>5-Queens 를 수업 순서 (0행부터, 0열부터) 로 풀 때 처음 찾는 해 X 를 쓰시오.</p>', show='[0, 2, 4, 1, 3]', alt=['0,2,4,1,3', '0 2 4 1 3'],
 exp='X[0] = 0 → X[1] = 0, 1 은 충돌, 2 가능 → X[2] = 4 만 가능 → X[3] = 1 → X[4] = 3. 되돌아갈 필요 없이 바로 찾음.', src=src('nq')),
dict(type='essay', lv='중', unit='Subset Sum 트리', pts=10, q=f'<p>A = {xs(A4b)}, S = {S4b}. subsetsum1 의 탐색 트리를 그리시오 (노드 = 남은 S, 왼쪽 = 넣음, 첫 True 에서 멈춤).</p>',
 model=tree_svg(SS4b, 'subset sum 트리', bw=66), rubric=[['넣음 먼저', 3], ['실패 노드 처리', 3], ['S = 0 도착 경로 2 → 4 → 5', 4]], src=src('sstree')),
dict(type='table', lv='중', unit='sol · sol2', pts=12, q=f'<p>A = {xs(A4b)}, S = {S4b} 일 때 결과를 쓰시오.</p>', head=['함수', '결과'],
 rows=[['subsetsum_sol(A, S) 가 반환하는 부분집합', Bk('[2, 4, 5]', '2,4,5', '{2,4,5}')], ['subsetsum_sol2(0) 이 처음 출력하는 X', Bk('[1, 1, 1, 0]', '1,1,1,0')], ['두 번째로 출력하는 X', Bk('[1, 0, 0, 1]', '1,0,0,1')]],
 exp='sol 은 넣는 쪽을 먼저 시도해 처음 성공한 것을 반환 → 2, 4, 5. sol2 는 X[k] = 1 을 먼저 → [1, 1, 1, 0] ({2, 4, 5}) → [1, 0, 0, 1] ({2, 9}).', src=src('sol', 'sol2')),
dict(type='table', lv='중', unit='DP', pts=10, q=f'<p>A = {xs(DPA)}, S = 7. DP[i][s] (A[0] ~ A[i] 로 합 s 를 만들 수 있으면 T) 의 마지막 행 (i = 2) 에서 T 인 s 를 모두 쓰고, DP[2][7] 이 T 인 근거가 되는 칸을 쓰시오.</p>', head=['항목', '답'],
 rows=[['DP[2][s] = T 인 s', Bk('0, 2, 4, 5, 6, 7', '0,2,4,5,6,7')], ['DP[2][7] 의 근거', Bk('DP[1][2]', 'DP[1][7-5]')]],
 exp='DP[2][7] = DP[1][7 − 5] or DP[1][7] = DP[1][2] (T, {2}) → T ({2, 5}).', src=src('dp')),
dict(type='table', lv='중', unit='0/1 추적', pts=14, q=f'<p>가치 P = {xs(KB[0])}, 무게 S = {xs(KB[1])}, K = {KB[2]} (가성비 순). 수업 코드 (가지로 가기 전 상한 검사, MP 는 잎 · 꽉 참에서 갱신) 로 풀 때 빈칸을 채우시오.</p>',
 head=['가지', '상한 (또는 이유)', '결과'],
 rows=[['[ ] → X[0] = 1', Bk(F_(40 + frac(*KB[:2], 1, 5))), Bk('감')], ['[1] → X[1] = 1', Bk(F_(70 + frac(*KB[:2], 2, 2))), Bk('감')], ['[1, 1] → X[2] = 1', Bk('넘침', '무게 초과', '3 > 2'), Bk('안 감')], ['[1, 1] → X[2] = 0', Bk(F_(70 + frac(*KB[:2], 3, 2))), Bk('감')],
       ['[1, 1, 0] → X[3] = 1', Bk('넘침', '무게 초과'), Bk('안 감')], ['[1, 1, 0] → X[3] = 0', Bk('70'), Bk('감 (MP = 70)', '감')], ['[1] → X[1] = 0', Bk(F_(40 + frac(*KB[:2], 2, 5))), Bk('안 감')], ['[ ] → X[0] = 0', Bk(F_(frac(*KB[:2], 1, 7))), Bk('안 감')],
       ['결과', Bk('[1, 1, 0, 0], 70', '[1,1,0,0], 70'), '']],
 exp=f'[ ] 왼쪽 = 40 + frac(1, 5) = 40 + 30 + 18 × 2/3 = 82. [1] 왼쪽 = 70 + frac(2, 2) = 70 + 12 = 82. [1, 0] = 40 + frac(2, 5) = 40 + 18 + 10 × 2/5 = 62 ≤ 70. [0] = frac(1, 7) = 30 + 18 + 1/5 × 10 = 50 ≤ 70.', src=src('bound', 'kcode')),
dict(type='table', lv='하', unit='frac_knapsack', pts=8, q=f'<p>위 문제의 아이템으로 frac_knapsack 값을 구하시오.</p>', head=['호출', 'B'],
 rows=[['frac_knapsack(1, 5)', Bk(fr_b(1, 5))], ['frac_knapsack(2, 2)', Bk(fr_b(2, 2))], ['frac_knapsack(2, 5)', Bk(fr_b(2, 5))], ['frac_knapsack(3, 0)', Bk('0')]],
 exp='아이템 i 부터 가성비 순으로 남은 용량을 채움. (1, 5): 3 (30) + 3 중 2 (12) = 42. (2, 2): 18 × 2/3 = 12. (2, 5): 18 + 10 × 2/5 = 22.', src=src('frk')),
dict(type='table', lv='하', unit='Knapsack', pts=8, q='<p>빈칸을 채우시오.</p>', head=['문장', '답'],
 rows=[['fractional 최적 가치 ( ) 0/1 최적 가치', Bk('≥', '>=')], ['MP 의 뜻', Bk('지금까지 찾은 최대 가치', '지금까지 찾은 답 중 최대 가치')], ['상한이 MP ( ) 이면 그 가지를 방문하지 않는다', Bk('이하', '≤', '<=')], ['update_best 에서 X 를 저장할 때 쓰는 함수', Bk('X.copy()', 'copy')]],
 exp='쪼개면 빈칸 없이 채울 수 있어 fractional 이 같거나 크다 → 상한으로 쓴다.', src=src('two', 'bound', 'upd')),
dict(type='short', lv='하', unit='Knapsack', pts=10, q='<p>K = 16, S = [2, 5, 10, 5], P = [40, 30, 50, 10] 에서 0/1 을 가성비 순으로 넣었을 때의 가치와 최적 가치를 "a, b" 로 쓰시오.</p>', show='80, 90', alt=['80,90'],
 exp='가성비 순: 2, 5, (10 넘침), 5 → 80. 최적: 2 + 10 → 90.', src=src('g01')),
]
P_('bt-1b', 'F. 백트래킹 — 기본 2회', '기본', '<b>백트래킹 · 기본 2회</b> (11주차 1차시 ~ 13주차 1차시)<br>수업과 같은 유형을 새 값으로 — 새 미로 · 5-Queens · sol / sol2 결과 · DP 칸 · 새 배낭 추적', B1B)

# ════════════════ bt-1c 기본 3회 — 새 값 + 기호 바꿈 ════════════════
G5c = ['00100', '01010', '00010', '10011', '11000']; T5c, P5c = maze_sst(G5c)
assert P5c and P5c[-1] == (4, 4)
KC = ([24, 30, 18, 8], [2, 5, 3, 4], 8); rC = knap_bt(*KC); assert rC[0] == 54 and rC[1] == [1, 1, 0, 0] and knap_opt(*KC) == 54
B1C = [
dict(type='table', lv='중', unit='find_way', pts=10, q='<p>격자 G (0 = 길, 1 = 벽), 행 r, 열 c 로 바꿔 쓴 미로 함수이다. 빈칸을 채우시오. (남 → 동 순서)</p>' + pre('''
def go(r, c):
    if r == n - 1 and c == n - 1:
        return true
    if (가):
        if go((나)):
            return true
        return go((다))
    else:
        return false'''), head=['빈칸', '답'],
 rows=[['(가)', Bk('G[r][c] == 0', 'G[r][c]==0')], ['(나)', Bk('r + 1, c', 'r+1, c', 'r+1,c')], ['(다)', Bk('r, c + 1', 'r, c+1', 'r,c+1')], ['수업 코드의 M[x][y] == safe 에 해당', Bk('(가)')]],
 exp='행 = r (수업 x), 열 = c (수업 y). 남쪽 = 행 + 1.', src=src('fw')),
dict(type='essay', lv='상', unit='미로 SST', pts=14, q=f'<p>5 × 5 미로 (회색 = 벽) 에서 수업 규칙 (↓ 먼저, → 나중, 첫 해에서 멈춤) 으로 상태 공간 트리를 그리고 경로를 쓰시오.</p>{maze_html(G5c)}',
 model=tree_svg(T5c, '5×5 SST', bw=62, DX=66) + pth(P5c), rubric=[['트리 · 순서', 6], [f'X 노드 {count(T5c, "x")}개', 4], ['경로', 4]], src=src('sst', 'maze5')),
dict(type='table', lv='중', unit='N-Queens', pts=12, q='<p>퀸 위치를 Q[r] (r 행 퀸의 열), 함수를 place(r) · ok(r, col) 로 바꿨다. 빈칸을 채우시오.</p>' + pre('''
def place(r):
    if r == N:
        print(Q)
        return
    for col in range(N):
        if ok(r, col):
            (가)
            (나)

def ok(r, col):
    for j in range(r):
        if Q[j] == col or (다):
            return False
    return True'''), head=['빈칸', '답'],
 rows=[['(가)', Bk('Q[r] = col', 'Q[r]=col')], ['(나)', Bk('place(r + 1)', 'place(r+1)')], ['(다)', Bk('abs(Q[j] - col) == abs(j - r)', 'abs(Q[j]-col)==abs(j-r)')]],
 exp='수업의 X, k, c, i, nqueens, is_safe 가 Q, r, col, j, place, ok 로 바뀐 것.', src=src('nq', 'safe')),
dict(type='table', lv='중', unit='Subset Sum', pts=12, q='<p>목표 합 T, 배열 arr, 인덱스 idx 로 바꾼 subsetsum2 이다. 빈칸을 채우시오.</p>' + pre('''
def check(arr, idx, T):
    if T == 0:
        return True
    elif (가):
        return False
    else:
        return check(arr, (나), (다)) or check(arr, idx - 1, T)
# 첫 호출: check(arr, (라), T)'''), head=['빈칸', '답'],
 rows=[['(가)', Bk('T < 0 or idx == -1', 'T<0 or idx==-1')], ['(나)', Bk('idx - 1', 'idx-1')], ['(다)', Bk('T - arr[idx]', 'T-arr[idx]')], ['(라)', Bk('len(arr) - 1', 'len(arr)-1')]],
 exp='수업의 A, i, S 가 arr, idx, T.', src=src('ss2')),
dict(type='essay', lv='중', unit='가지치기', pts=10, q='<p>합이 T 인 부분집합을 모두 출력하는 함수 show(k, cur) (cur = 지금까지 넣은 합) 를 쓰시오. 배열 arr 은 오름차순, 선택은 Y[k] (1 = 넣음). 넣어서 T 를 넘으면 넣는 가지는 가지 않는다.</p>',
 model=pre('''
def show(k, cur):
    if k == n:
        if cur == T:
            print(Y)
        return
    if cur + arr[k] <= T:      # 가지치기
        Y[k] = 1
        show(k + 1, cur + arr[k])
    Y[k] = 0
    show(k + 1, cur)'''), rubric=[['k == n 에서 합 확인 · 출력 · return', 3], ['cur + arr[k] ≤ T 조건', 3], ['넣음 / 안 넣음 두 재귀와 Y 복원', 4]], src=src('sol2', 'prune')),
dict(type='table', lv='중', unit='Knapsack 코드', pts=14, q='<p>용량 W, 무게 w[ ], 가치 c[ ], 남은 용량 room, 지금 가치 val, 최대 best 로 바꾼 코드이다. 빈칸을 채우시오.</p>' + pre('''
def bag(i, room, val):
    if i >= n or room == 0:
        save(val)
        return
    if (가):
        U = frac(i + 1, (나))
        if (다) > best:
            Y[i] = 1
            bag(i + 1, room - w[i], val + c[i])
            Y[i] = 0
    U = frac(i + 1, room)
    if (라) > best:
        Y[i] = 0
        bag(i + 1, room, val)'''), head=['빈칸', '답'],
 rows=[['(가)', Bk('w[i] <= room', 'w[i]<=room')], ['(나)', Bk('room - w[i]', 'room-w[i]')], ['(다)', Bk('val + c[i] + U', 'val+c[i]+U')], ['(라)', Bk('val + U', 'val+U')]],
 exp='수업의 S, P, K, size, profit, MP, B 가 w, c, W, room, val, best, U.', src=src('kcode')),
dict(type='table', lv='상', unit='0/1 추적', pts=16, q=f'<p>가치 c = {xs(KC[0])}, 무게 w = {xs(KC[1])}, W = {KC[2]}. 위 bag 코드 (best 는 잎 · 꽉 참에서만 갱신) 로 풀 때 빈칸을 채우시오.</p>',
 head=['가지', '상한 (또는 이유)', '결과'],
 rows=[['[ ] → Y[0] = 1', Bk(F_(24 + frac(*KC[:2], 1, 6))), Bk('감')], ['[1] → Y[1] = 1', Bk(F_(54 + frac(*KC[:2], 2, 1))), Bk('감')], ['[1, 1] → Y[2] = 1', Bk('넘침', '무게 초과'), Bk('안 감')], ['[1, 1] → Y[2] = 0', Bk(F_(54 + frac(*KC[:2], 3, 1))), Bk('감')],
       ['[1, 1, 0] → Y[3] = 1', Bk('넘침', '무게 초과'), Bk('안 감')], ['[1, 1, 0] → Y[3] = 0', Bk('54'), Bk('감', '감 (best = 54)')], ['[1] → Y[1] = 0', Bk(F_(24 + frac(*KC[:2], 2, 6))), Bk('안 감')], ['[ ] → Y[0] = 0', Bk(F_(frac(*KC[:2], 1, 8))), Bk('안 감')],
       ['결과', Bk('[1, 1, 0, 0], 54', '[1,1,0,0], 54'), '']],
 exp='가성비 12, 6, 6, 2. [ ] 왼쪽 = 24 + frac(1, 6) = 24 + 30 + 1 × 6 = 60. [1] 왼쪽 = 54 + frac(2, 1) = 54 + 6 = 60. [1, 0] = 24 + 18 + 3 × 2 = 48 ≤ 54. [0] = 30 + 18 = 48 ≤ 54.', src=src('k3', 'bound')),
dict(type='essay', lv='중', unit='Knapsack', pts=12, q='<p>fractional 최적 가치 ≥ 0/1 최적 가치 인 이유를 쓰고, 이 사실이 bag 함수의 어느 부분에 쓰이는지 쓰시오.</p>',
 model='0/1 의 해는 아이템을 쪼개지 않은 fractional 해이기도 하다 → fractional 은 더 많은 선택지 중 최대를 고르므로 0/1 보다 작을 수 없다 (남는 공간을 쪼갠 조각으로 채움). 그래서 남은 아이템을 남은 용량에 fractional 로 채운 값 (frac) 은 그 가지에서 0/1 로 얻을 수 있는 가치의 <b>상한</b>이 되고, bag 의 val + c[i] + U &gt; best, val + U &gt; best 검사에서 상한 ≤ best 인 가지를 방문하지 않는 데 쓰인다.',
 rubric=[['0/1 해 ⊂ fractional 해 (또는 빈칸을 채움) 이유', 5], ['frac 이 상한이 됨', 4], ['상한 ≤ best 인 가지를 거르는 두 if', 3]], src=src('two', 'bound')),
]
P_('bt-1c', 'F. 백트래킹 — 기본 3회', '기본', '<b>백트래킹 · 기본 3회</b> (11주차 1차시 ~ 13주차 1차시)<br>새 값 + <b>기호를 바꾼</b> 코드 — 역할로 읽기 · 5 × 5 SST · 가지치기 코드 작성 · 새 배낭 추적', B1C)

# ════════════════ bt-2 응용 ════════════════
TE, PE = maze_sst(G4, order=((0, 1, '→'), (1, 0, '↓'))); assert PE == P4
A6 = [4, 6, 3, 5, 2, 1]; S6 = 9
c_un, c_pr = calls(sorted(A6), S6, False), calls(sorted(A6), S6, True)
assert (c_un, c_pr) == (127, calls(sorted(A6), S6, True))
K4 = ([40, 30, 50, 10], [2, 5, 10, 5], 16); r4 = knap_bt(*K4); assert r4[0] == 90 and len(r4[3]) == 8
rBn = knap_bt(*KB, mp_mode='node'); assert len(rB[3]) == 5 and len(rBn[3]) == 4
# 정렬 안 된 입력
KU = ([18, 40, 10, 30], [3, 2, 5, 3], 7); assert frac(KU[0], KU[1], 0, 7) == 82 and knap_opt(*KU) == 70
order = sorted(range(4), key=lambda j: -Fr(KU[0][j], KU[1][j])); assert order == [1, 3, 0, 2]
B2 = [
dict(type='essay', lv='중', unit='탐색 순서', pts=10, q=f'<p>수업 4 × 4 미로에서 탐색 순서만 바꿔 <b>동쪽 (→) 을 먼저</b> (왼쪽 가지), 남쪽을 나중에 탐색한다. 트리를 그리고 경로를 쓰시오. 수업 순서와 비교해 경로가 같은지 쓰시오.</p>{maze_html(G4)}',
 model=tree_svg(TE, '→ 먼저') + f'{pth(PE)} — 이 미로는 길이 하나라 경로는 같지만, X 노드 수와 트리 모양이 다르다 (→ 먼저 {count(TE, "x")}개, ↓ 먼저 3개).', rubric=[['→ 먼저 순서로 트리', 5], ['경로', 3], ['비교', 2]], src=src('sst')),
dict(type='line', lv='중', unit='knapsack 버그', pts=10, q='<p>knapsack 코드를 옮기다 어떤 줄부터 끝까지를 한 칸 더 들여썼다. P = [15, 16, 6], S = [3, 4, 2], K = 5 에서 답이 21 이 아니라 6 이 나왔다. 잘못 들여쓰기 시작한 줄을 고르시오.</p>',
 code='''
def knapsack(i, size, profit):
    if i >= n or size == 0:
        update_best(profit); return
    if S[i] <= size:
        B = frac_knapsack(i + 1, size - S[i])
        if profit + P[i] + B > MP:
            X[i] = 1; knapsack(i + 1, size - S[i], profit + P[i]); X[i] = 0
        B = frac_knapsack(i + 1, size)
        if profit + B > MP:
            X[i] = 0; knapsack(i + 1, size, profit)''', answer=[8],
 exp='8 ~ 10번 줄 (안 넣는 가지) 이 if S[i] &lt;= size 안에 들어가 있다. [1] 에서 아이템 1 (무게 4) 이 남은 용량 2 에 안 들어가면 안 넣는 가지 [1, 0] 까지 사라져 [1, 0, 1] (21) 을 못 찾고, 결국 [0, 0, 1] (6) 이 답이 된다 (코드로 확인). 13-1 필기의 들여쓰기 문제와 같다 — 안 넣는 가지는 if 밖.', src=src('kcode')),
dict(type='table', lv='중', unit='가지치기 효과', pts=10, q=f'<p>A = {xs(A6)}, S = {S6}. 오름차순 정렬 후 subsetsum_sol2 (합을 인자로 넘기는 형태) 를 실행한다. 재귀 호출 횟수를 쓰시오.</p>', head=['방법', '호출 횟수'],
 rows=[['가지치기 없음', Bk(str(c_un))], ['current_sum + A[k] ≤ S 일 때만 넣음', Bk(str(c_pr))]],
 exp=f'가지치기 없으면 2<sup>7</sup> − 1 = {c_un} (깊이 0 ~ 6 의 모든 노드). 정렬되어 있어 한 번 넘으면 뒤 원소도 넘으므로 넣는 가지가 많이 잘린다 → {c_pr}.', src=src('prune')),
dict(type='essay', lv='상', unit='가지치기 조건', pts=10, q='<p>Subset Sum 가지치기 current_sum + A[k] ≤ S 는 모든 원소가 양수이고 오름차순일 때 정확하다. (1) 원소에 음수가 있으면 왜 틀릴 수 있는지 예를 들어 쓰시오. (2) 정렬하지 않으면 무엇을 잃는지 쓰시오.</p>',
 model='(1) A = [5, 3, −2], S = 6: 5 + 3 = 8 &gt; 6 이라 3 을 넣는 가지를 자르면 {5, 3, −2} = 6 을 놓친다 — 음수가 있으면 넘었다가 다시 줄어들 수 있다.<br>(2) 넣는 가지 하나만 자르는 것은 정렬 없이도 맞지만, 오름차순이면 A[k] 가 넘칠 때 그 뒤 원소도 모두 넘친다는 것을 알 수 있어 <b>뒤를 볼 필요가 없다</b>는 판단 (수업: 7 부터는 탐색할 필요 없음) 을 할 수 있다.',
 rubric=[['음수 반례와 이유', 5], ['정렬의 역할 (뒤 원소도 넘침)', 5]], src=src('prune', 'ss1')),
dict(type='table', lv='중', unit='MP 갱신 시점', pts=10, q=f'<p>P = {xs(KB[0])}, S = {xs(KB[1])}, K = 7. MP 를 ① 잎 · 꽉 참에서만 갱신 (update_best 코드) 할 때와 ② 방문하는 모든 노드에서 지금 가치로 갱신 (13-1 판서) 할 때를 비교하시오.</p>', head=['항목', '① 코드', '② 판서'],
 rows=[['[1, 1] 을 방문한 직후 MP', Bk('0'), Bk('70')], ['[1, 1, 0] → X[3] = 0 가지 (상한 70)', Bk('감'), Bk('안 감')], ['방문한 노드 수 (루트 포함)', Bk(str(len(rB[3]))), Bk(str(len(rBn[3])))], ['최종 MP', Bk('70'), Bk('70')]],
 exp='② 는 [1, 1] 에서 이미 MP = 70 이 되어 상한 70 ≤ 70 인 가지를 거른다 (best 는 [1, 1] 에서 나머지 0 으로 저장). 결과는 같고 방문 수만 다르다.', src=src('board', 'upd')),
dict(type='table', lv='중', unit='정렬 안 된 입력', pts=10, q=f'<p>가치 P = {xs(KU[0])}, 무게 S = {xs(KU[1])}, K = 7 이 가성비 순이 아니다. 수업처럼 먼저 정렬하고 푼다.</p>', head=['항목', '답'],
 rows=[['가성비 순으로 정렬한 아이템 번호 (0부터)', Bk('1, 3, 0, 2', '1,3,0,2')], ['fractional 최대 가치', Bk(F_(frac(KU[0], KU[1], 0, 7)))], ['0/1 최적 가치', Bk(str(knap_opt(*KU)))], ['0/1 최적에서 넣는 아이템 번호', Bk('1, 3', '1,3')]],
 exp=f'가성비 6, 20, 2, 10 → 1 (20), 3 (10), 0 (6), 2 (2). fractional: 2 + 3 통째로 (70), 남은 2 → 아이템 0 의 2/3 → 12 → {F_(frac(KU[0], KU[1], 0, 7))}. 0/1: 아이템 1, 3 (무게 5, 가치 70) 이 최대 {knap_opt(*KU)} — 아이템 0 을 더하면 무게 8 &gt; 7.', src=src('k3', 'fr')),
dict(type='table', lv='하', unit='한계함수 설계', pts=10, q='<p>각 문제에서 한계함수 B 가 검사하는 것을 쓰시오.</p>', head=['문제', 'B'],
 rows=[['미로', Bk('벽 · 미로 밖', '벽이거나 밖')], ['N-Queens', Bk('같은 열 · 대각선', 'is_safe')], ['Subset Sum (정렬)', Bk('합 + A[k] ≤ S', 'current_sum + A[k] <= S')], ['0/1 Knapsack', Bk('무게 ≤ K, 상한 > MP', '넘침, 상한 ≤ MP')]],
 exp='B 는 문제마다 다르고, 잘 설계할수록 거르는 가지가 많아진다.', src=src('gen')),
dict(type='mc', lv='중', unit='O(nS)', pts=10, q='<p>Subset Sum 의 DP 수행시간 O(nS) 에 대한 설명으로 옳은 것은?</p>',
 choices=['n 이 같으면 S 가 커져도 수행시간은 같다.', 'S 가 20억이면 표의 칸이 n × 20억 개 가까이 필요하다.', 'S 는 입력의 개수이므로 O(n<sup>2</sup>) 과 같다.', 'O(nS) 는 항상 2<sup>n</sup> 보다 빠르다.'], answer=[2],
 exp='표는 n × (S + 1). S 는 입력의 <b>값</b>이라 크면 표도 커진다 → 바람직하지 않다고 하신 이유. S 가 매우 크면 2<sup>n</sup> 보다 느릴 수도 있다.', src=src('dp', 'ons')),
dict(type='table', lv='중', unit='SST 크기', pts=10, q='<p>빈칸을 채우시오.</p>', head=['항목', '답'],
 rows=[['원소 5개 subset sum 의 잎 (끝까지 정한 상태) 수', Bk('32')], ['그때 전체 노드 수', Bk('63')], ['4-Queens SST 에서 첫 해까지 X 표시 노드 수 (수업 규칙)', Bk(str(count(Q4, 'x')))], ['4-Queens 의 해의 개수', Bk('2')]],
 exp=f'잎 2<sup>5</sup>, 노드 2<sup>6</sup> − 1. 4-Queens 첫 해 [1, 3, 0, 2] 까지 X {count(Q4, "x")}개 (과제 4).', src=src('sst', 'nq')),
dict(type='table', lv='중', unit='0/1 4개 예시', pts=10, q='<p>K = 16, S = [2, 5, 10, 5], P = [40, 30, 50, 10] 을 수업 코드로 풀 때 거르는 가지와 이유를 채우시오.</p>', head=['거르는 가지', '이유 (상한 값 또는 넘침)'],
 rows=[['[1, 1, 1]', Bk('넘침', '무게 17 > 16')], ['[1, 1, 0, 0]', Bk('70')], ['[1, 0, 1, 1]', Bk('넘침')], ['[1, 0, 0]', Bk('50')], ['[0]', Bk('82')]],
 exp='MP = 70 ([1, 1, 0, 1]) 다음 90 ([1, 0, 1, 0]) 으로 갱신. [1, 1, 0, 0] = 70 + 0 ≤ 70, [1, 0, 0] = 40 + frac(3, 14) = 40 + 10 = 50 ≤ 90, [0] = frac(1, 16) = 30 + 50 + 1 × 2 = 82 ≤ 90.', src=src('bound', 'kcode')),
]
assert r4[4] == [((1, 1, 1), 'over', None), ((1, 1, 0, 0), 'bound', 70), ((1, 0, 1, 1), 'over', None), ((1, 0, 0), 'bound', 50), ((0,), 'bound', 82)]
P_('bt-2', 'F. 백트래킹 — 응용', '응용', '<b>백트래킹 · 응용</b> (11주차 1차시 ~ 13주차 1차시)<br>탐색 순서 바꾸기 · 버그 찾기 · 가지치기 효과 · MP 갱신 시점 · 정렬 안 된 입력 · O(nS)', B2)

# ════════════════ bt-3 심화 ════════════════
B3 = [
dict(type='essay', lv='상', unit='한계함수 정당성', pts=15, q='<p>0/1 Knapsack 백트래킹에서 "상한 ≤ MP 인 가지는 방문하지 않아도 최적 해를 놓치지 않는다" 를 귀류법으로 설명하시오.</p>',
 model='<b>가정</b>: 상한 U ≤ MP 인 가지 아래에 MP 보다 가치가 큰 0/1 해 x 가 있다 (놓쳤다).<br>그 가지에서 x 의 가치 = p(v) (+ P[i]) + (나머지 아이템으로 얻은 0/1 가치). 나머지 아이템의 0/1 가치 ≤ 같은 아이템 · 같은 남은 용량의 fractional 최적 가치 (0/1 해는 쪼개지 않은 fractional 해) → x 의 가치 ≤ U.<br><b>모순</b>: MP &lt; x 의 가치 ≤ U ≤ MP.<br><b>결론</b>: 그런 해는 없다 → 걸러도 최적을 놓치지 않는다.',
 rubric=[['가정', 3], ['0/1 ≤ fractional 로 x ≤ U', 6], ['MP < x ≤ U ≤ MP 모순', 4], ['결론', 2]], src=src('two', 'bound')),
dict(type='essay', lv='상', unit='0/1 추적', pts=15, q='<p>K = 16, S = [2, 5, 10, 5], P = [40, 30, 50, 10] 을 수업 코드로 풀 때 상태 공간 트리를 그리고, 방문하는 노드마다 p(v), s(v), 거르는 가지마다 상한 (또는 넘침) 을 쓰시오. 최종 MP 와 X 를 쓰시오.</p>',
 model='방문: [ ] (0, 0) → [1] (40, 2) → [1, 1] (70, 7) → [1, 1, 1] 넘침 ✕ → [1, 1, 0] (70, 7) → [1, 1, 0, 1] (80, 12) 잎 → MP = 80 → [1, 1, 0, 0] 상한 70 ✕ → [1, 0] (40, 2) → [1, 0, 1] (90, 12) → [1, 0, 1, 1] 넘침 ✕ → [1, 0, 1, 0] 잎 → <b>MP = 90</b> → [1, 0, 0] 상한 50 ✕ → [0] 상한 82 ✕.<br>결과 <b>MP = 90, X = [1, 0, 1, 0]</b>. (방문 노드 8개)',
 rubric=[['방문 순서 · 트리', 5], ['MP 80 → 90 갱신', 4], ['거른 가지 5개와 이유', 4], ['결과', 2]], src=src('bound', 'kcode', 'board')),
dict(type='essay', lv='상', unit='그리디 vs 백트래킹', pts=10, q='<p>fractional knapsack 은 그리디로, 0/1 knapsack 은 백트래킹으로 푸는 이유를 각각 쓰시오. 0/1 에 가성비 그리디가 실패하는 예를 수업 값이 아닌 새 값으로 하나 만드시오.</p>',
 model='fractional: 쪼갤 수 있어 가성비가 높은 것부터 채우면 남는 공간도 다음 좋은 아이템 조각으로 채워져 최적 (그리디). 0/1: 쪼갤 수 없어 가성비 좋은 것을 먼저 넣으면 남는 공간이 낭비될 수 있음 → 모든 조합을 봐야 하므로 백트래킹 (+ 상한으로 가지치기).<br>예: K = 4, 무게 [3, 2, 2], 가치 [9, 5, 5] (가성비 3, 2.5, 2.5) → 그리디 9 (3 을 넣으면 2 가 안 들어감), 최적 2 + 2 → 10.',
 rubric=[['fractional 그리디 이유', 3], ['0/1 백트래킹 이유', 3], ['실제로 실패하는 새 예', 4]], src=src('fr', 'g01', 'kbt')),
dict(type='essay', lv='상', unit='N-Queens 트리', pts=15, q='<p>4-Queens 를 수업 규칙 (각 노드에서 0, 1, 2, 3 열 순서, 충돌하면 X, 첫 해에서 종료) 으로 풀 때 상태 공간 트리를 그리시오. (과제 4 와 같은 문제)</p>',
 model='<b>루트 [ ] 의 X[0] = 0 가지</b>' + '<pre style="font-size:12px;line-height:1.45">' + esc(chr(10).join(tree_text(Q4[3][0]))) + '</pre>' + '<b>X[0] = 1 가지</b>' + tree_svg(Q4[3][1], '[1] 아래', bw=64, DX=66, DY=62) + f'가지의 숫자 = 그 행에 놓은 열. 첫 해 [1, 3, 0, 2], X 노드 {count(Q4, "x")}개. X[0] = 2, 3 은 탐색하지 않음.',
 rubric=[['[0] 아래 전부 실패 처리', 5], ['[1] → [1, 3] → [1, 3, 0] → [1, 3, 0, 2]', 5], ['X 표시 · 탐색 안 한 가지 처리', 5]], src=src('nq', 'sst')),
dict(type='essay', lv='상', unit='일반형 적용', pts=10, q='<p>Backtrack(k) 일반형으로 0/1 Knapsack 을 다시 쓸 때, 후보 c 와 한계함수 B(X[0], …, X[k−1], c) 를 각각 정의하시오.</p>',
 model='후보 c ∈ {1, 0} (1 먼저). B: c = 1 이면 s + S[k] ≤ K 이고 p + P[k] + frac(k + 1, K − s − S[k]) &gt; MP, c = 0 이면 p + frac(k + 1, K − s) &gt; MP (p, s = X[0] ~ X[k−1] 로 넣은 가치 · 무게 합). k ≥ n 에서 MP 와 비교해 갱신 (output solution).',
 rubric=[['후보 c', 2], ['c = 1 의 B (넘침 + 상한)', 4], ['c = 0 의 B', 3], ['k ≥ n 처리', 1]], src=src('gen', 'bound')),
dict(type='essay', lv='상', unit='Subset Sum 비교', pts=10, q='<p>subsetsum1, subsetsum_sol, subsetsum_sol2 의 반환 · 출력과 쓰임을 비교하고, subsetsum1 을 DP 로 바꿀 수 있게 만든 subsetsum2 의 차이를 쓰시오.</p>',
 model='subsetsum1: 있는지만 True / False. sol: 답 하나 (리스트, 없으면 None). sol2: X 로 모든 답 출력. subsetsum2 는 배열을 잘라 넘기는 대신 인덱스 i 하나를 줄여 넘겨 상태가 (i, S) 두 숫자가 됨 → DP[i][S] 표로 저장 가능 → O(nS).',
 rubric=[['세 함수 비교', 6], ['subsetsum2 → (i, S) → DP', 4]], src=src('ss1', 'ss2', 'sol', 'sol2', 'dp')),
dict(type='essay', lv='상', unit='MP 초기값', pts=10, q='<p>knapsack(0, K, 0) 을 부르기 전에 MP = 0 으로 둔다. MP 를 처음부터 큰 값 (예: 1000) 으로 잘못 두면 어떤 일이 생기는지, 반대로 MP 를 "가성비 그리디로 구한 0/1 가치" 로 시작하면 어떤 장점이 있는지 쓰시오.</p>',
 model='1000 이면 모든 상한이 1000 이하라서 루트의 두 가지 모두 거름 → 아무 해도 찾지 못함 (best_X 없음). MP 는 실제로 가능한 해의 가치여야 한다. 그리디 0/1 가치 (예: K = 16 에서 80) 는 실제로 가능한 해이므로 MP 의 시작값으로 써도 최적을 놓치지 않고, 처음부터 더 많은 가지를 거를 수 있다 (보충).',
 rubric=[['큰 값이면 전부 거름', 4], ['MP 는 가능한 해의 가치여야 함', 3], ['그리디 값 시작의 장점', 3]], src=src('bound', 'upd')),
dict(type='essay', lv='상', unit='find_way 범위', pts=15, q='<p>수업 find_way 는 미로 밖 검사가 없다. (1) 수업 4 × 4 미로에서 실제로 미로 밖 인덱스로 호출되는 순간을 쓰시오. (2) 고친 코드를 쓰시오. (3) 동쪽 먼저로 바꾸려면 어떤 줄을 어떻게 바꾸는지 쓰시오.</p>',
 model='(1) (3, 1) 에서 남쪽 find_way(4, 1) — M[4][1] 은 범위 밖. (2) 맨 앞에 <code>if x &gt;= n or y &gt;= n: return false</code>. (3) <code>try_down = find_way(x + 1, y)</code> 와 <code>try_east = find_way(x, y + 1)</code> 의 순서를 바꿈 (먼저 find_way(x, y + 1) 을 시도하고 실패하면 find_way(x + 1, y)).',
 rubric=[['(1) (4, 1) 호출', 5], ['(2) 범위 검사', 5], ['(3) 두 호출 순서 교환', 5]], src=src('fw', 'fwfix')),
]
P_('bt-3', 'F. 백트래킹 — 심화', '심화', '<b>백트래킹 · 심화</b> (11주차 1차시 ~ 13주차 1차시)<br>한계함수가 맞는 이유 (귀류법) · 4개 배낭 전체 추적 · 4-Queens SST · 일반형 적용 · 함수 비교', B3)
