# 정리노트 — 백트래킹 (개념노트 backtracking.html 의 압축본)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapgen import *
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'algorithm/summary/backtracking.html')
X = v('X')

CH = []
CH.append(('1', '백트래킹 방법', '11-1', 2, [
 sunit('정의 · 특징', f'''<dl class="def"><dt>정의</dt><dd>{hl('진행 → 막힘 → 되돌아감')} (back-track) 을 반복, 가능한 방식을 다 해 봄</dd>
 <dt>장점</dt><dd>해가 있으면 {hl('무조건 찾음')}, 직관적</dd><dt>단점</dt><dd>오래 걸림 (경우 2<sup>n</sup> 등) → 다른 방법이 안 될 때 <b>최후의 보루</b></dd></dl>
 {table(['방법', '한 줄'], [['분할 정복', '나눠서 재귀'], ['DP', '작은 답 저장 후 재사용'], ['그리디', '지금 최선, 안 되돌림'], ['백트래킹', '다 해 보고 막히면 되돌림']], ['32%', '68%'])}''', 2),
]))
CH.append(('2', '미로 탈출', '11-1 · 12-1', 3, [
 sunit('규칙과 추적', f'''<dl class="def"><dt>규칙</dt><dd>↓ (남) 먼저, → (동) 나중, 막히면 <b>가장 최근 선택</b>으로 돌아감</dd></dl>
 {table(['미로', '찾은 길'], [['4 × 4<br>0111 / 0010 / 1011 / 0000', '(0,0) (1,0) (1,1) (2,1) (3,1) (3,2) (3,3)'], ['5 × 5', '(0,0) (1,0) (1,1) (1,2) (2,2) (2,3) (3,3) (3,4) (4,4) — (2,0) (3,0) (4,0) (4,1) 은 들어갔다 백트랙']], ['30%', '70%'])}''', 3),
 sunit('find_way(x, y)', f'''{code('pseudocode', 'find_way — 첫 호출 find_way(0, 0)', """
def find_way(x, y):
    if x == n-1 and y == n-1:  # 도착
        return true
    if M[x][y] == safe:        # 흰 칸
        if find_way(x+1, y):   # 남
            return true
        return find_way(x, y+1)  # 동
    else:
        return false""")}
 {trap(['세 블록 <b>if · if · else 는 같은 높이</b> (11-1 판서는 안쪽으로 들여씀 → 12-1 정정)', '미로 밖 검사 없음 — 실제 코드는 맨 앞에 x ≥ n or y ≥ n → false'])}
 {exam(['추적 순서 (남 → 동) 그대로 SST 그리기 — 과제 4', '빈칸: try_down 실패 후 <b>동쪽</b> 호출 줄'])}''', 4),
]))
CH.append(('3', 'N-Queens', '11-1', 5, [
 sunit('표기 · 답 · 대각선', f'''<dl class="def"><dt>{X}[k]</dt><dd>k 행 퀸의 <b>열</b> 인덱스 (행은 하나씩이라 같은 행 없음)</dd>
 <dt>4-Queens</dt><dd>[1, 3, 0, 2], [2, 0, 3, 1] — 2개</dd>
 <dt>대각선</dt><dd>{hl('|X[i] − c| == |i − k|')} (밑변 = 높이)</dd></dl>
 {code('pseudocode', 'nqueens(k) · is_safe(k, c)', """
def nqueens(k):
    if k == N: print(X); return
    for c in range(N):
        if is_safe(k, c):
            X[k] = c
            nqueens(k + 1)
def is_safe(k, c):
    for i in range(k):
        if X[i] == c:          # 같은 열
            return False
        if abs(X[i]-c) == abs(i-k):  # 대각선
            return False
    return True""")}
 {exam(['첫 해는 [1, 3, 0, 2] — 0열부터 놓아 보는 순서 (과제 4 트리)', 'is_safe 빈칸: 같은 열 · 대각선 두 조건'])}''', 5),
]))
CH.append(('4', 'Subset Sum', '11-1 · 12-1', 7, [
 sunit('문제 · subsetsum1 · 트리', f'''<dl class="def"><dt>문제</dt><dd>A 의 부분집합 중 합이 S. A = [8, 6, 7, 5, 3, 10, 9], S = 15 → {{8, 7}}, {{7, 5, 3}}, {{5, 10}}, {{6, 9}}</dd>
 <dt>경우</dt><dd>원소마다 넣음 / 안 넣음 → 2<sup>|A|</sup></dd></dl>
 {code('pseudocode', 'subsetsum1(A, S)', """
if S == 0: return True
if S < 0 or len(A) == 0: return False
z = A[0]; B = A[1:]
return subsetsum1(B, S-z) or subsetsum1(B, S)""")}
 <p>A = [8, 6, 7], S = 15 트리: 15 → (8 ○) 7 → (6 ○) 1 → −6 ✕, 1 ✕ → (6 ✕) 7 → (7 ○) <b>0 = True</b></p>
 {trap(['판서 A 의 4 → <b>3</b> (답 {7, 5, 3})', '노드 = <b>남은</b> 목표 S (넣으면 줄어듦)'])}''', 7),
 sunit('subsetsum2 · DP · O(nS)', f'''<div class="eq">DP[i][S] = DP[i−1][S−A[i]] or DP[i−1][S]</div>
 <ul class="dot"><li>subsetsum2(A, i, S): A[0] ~ A[i] 만 봄, i == −1 이면 False, 호출 subsetsum2(A, len(A)−1, S)</li>
 <li>표 n × (S + 1), 칸마다 or → {hl('O(nS)')}</li>
 <li>문제: S 처럼 입력의 <b>값</b>이 들어감 → 값이 크면 (20억) 비정상적으로 큼 → 바람직하지 않음</li></ul>''', 9),
 sunit('답 구하기 · 가지치기', f'''<ul class="dot"><li><b>sol</b>: 넣고 성공하면 <b>return [z] + result</b>, 실패면 안 넣고 시도, 불가능 None</li>
 <li><b>sol2(k)</b>: X[k] = 1 → (k+1), X[k] = 0 → (k+1), k == n 에서 합 == S 면 print(X) — 답 모두</li>
 <li><b>가지치기</b>: A 오름차순 + {hl('current_sum + A[k] ≤ S')} 일 때만 넣음 → 호출 255 → 93</li></ul>
 {trap(['sol 판서: return 과 + 빠짐', 'sol2 판서: if i in range → <b>for</b>, k == n 뒤 return', '교체 줄의 current_sum 은 인자로 넘겨야 함 (보충)'])}''', 9),
]))
CH.append(('5', '일반형 · 한계함수 · SST', '12-1', 11, [
 sunit('Backtrack(k)', f'''{code('pseudocode', 'Backtrack(k) — 첫 호출 Backtrack(0)', """
def Backtrack(k):
    if k >= n:
        output solution; return
    for each candidate c for X[k]:
        if B(X[0], ..., X[k-1], c) == True:
            X[k] = c
            Backtrack(k + 1)""")}
 <dl class="def"><dt>B</dt><dd>한계함수 (bounding function) — 지금까지 정한 것 + c 가 {hl('조건과 충돌하는지')}, 문제마다 다름</dd>
 <dt>SST</dt><dd>State-Space Tree — 노드 = 상태 (state)</dd></dl>
 {table(['문제', 'B'], [['N-Queens', 'is_safe (열 · 대각선)'], ['Subset Sum', '합 + A[k] ≤ S'], ['미로', '벽 · 미로 밖'], ['0/1 Knapsack', '무게 ≤ K, 상한 &gt; MP']], ['36%', '64%'])}
 {exam(['<b>B 를 잘 설계하면</b> 쓸데없는 가지를 빼서 효율 ↑ (교수님 강조)', 'SST 그리기: 왼쪽 가지 먼저, 막힌 노드 ✕, 첫 해 O (과제 4 규칙)'])}''', 11),
]))
CH.append(('6', 'Knapsack 문제', '12-2', 13, [
 sunit('정의 · 두 종류', f'''<dl class="def"><dt>문제</dt><dd>무게 합 ≤ K (조건 1) 이면서 {hl('가치 합 최대')} (조건 2)</dd>
 <dt>예시</dt><dd>K = 16, S = [2, 5, 10, 5], P = [40, 30, 50, 10]</dd></dl>
 {table(['', 'fractional', '0/1'], [['쪼개기', '가능', '불가 (1 / 0)'], ['풀이', '가성비 그리디', '백트래킹'], ['예시 답', '2 + 5 + 9 → <b>115</b>', '2 + 10 → <b>90</b>']], ['24%', '38%', '38%'])}
 <div class="eq">{hl('fractional 최적 ≥ 0/1 최적')} (항상)</div>
 {trap(['0/1 을 가성비 순으로: 2, 5, (10 넘침), 5 → <b>80</b> — 최적 아님', '판서 K-=16 → K = 16'])}
 {exam(['부등식을 기억 — 0/1 백트래킹의 <b>상한</b>으로 쓰임 (교수님)'])}''', 13),
]))
CH.append(('7', '0/1 Knapsack 백트래킹', '12-2 · 13-1', 15, [
 sunit('한계함수', f'''<dl class="def"><dt>p(v), s(v)</dt><dd>v 까지 넣은 가치 합, 무게 합 (v 에서 X[i] 결정)</dd><dt>MP</dt><dd>지금까지 찾은 답 중 최대 가치</dd></dl>
 {table(['', '상한', ''], [['X[i] = 1', 'p(v) + P[i] + frac(i+1, K − s(v) − S[i])', '≤ MP 면<br>안 감'], ['X[i] = 0', 'p(v) + frac(i+1, K − s(v))', '']], ['18%', '60%', '22%'])}
 <p>거르기: ① 넘침 ② 안 넣는 가지 (상한 ≤ MP) ③ {hl('fractional 상한 ≤ MP')} (가장 중요)</p>''', 15),
 sunit('예시 P = [15, 16, 6], S = [3, 4, 2], K = 5', f'''{table(['가지', '상한', '판단'], [['[ ] → X[0]=1', '15 + 8 = 23', '감'], ['[1] → X[1]=1', '4 &gt; 남은 2', '① ✕'], ['[1] → X[1]=0', '15 + 6 = 21', '감'], ['[1,0] → X[2]=1', '21', '답 MP = 21'], ['[1,0] → X[2]=0', '15 + 0 = 15', '② ✕'], ['[ ] → X[0]=0', '16 + 3 = 19', '③ ✕']], ['36%', '34%', '30%'])}
 <p>결과 {hl('MP = 21, X = [1, 0, 1]')}</p>
 {trap(['19 는 답이 아니라 <b>상한</b> (쪼갠 값)', '판서는 중간 노드에서도 MP 갱신 (15), 코드는 잎 · 꽉 참일 때만 — 이 예는 결과 같음', 'frac(a, b): a = 다음 아이템, b = 남은 용량'])}''', 16),
 sunit('코드 핵심', f'''{code('python', 'knapsack(i, size, profit)', """
if i >= n or size == 0:
    update_best(profit); return
if S[i] <= size:          # 넣는 가지
    B = frac_knapsack(i+1, size-S[i])
    if profit + P[i] + B > MP:
        X[i] = 1
        knapsack(i+1, size-S[i],
                 profit+P[i])
        X[i] = 0
B = frac_knapsack(i+1, size)  # if 밖
if profit + B > MP:
    X[i] = 0
    knapsack(i+1, size, profit)""")}
 {trap(['필기는 안 넣는 가지가 if 안쪽 → 답 21 이 <b>6</b> 으로 틀림', 'update_best: profit &gt; MP 면 MP, best_X (= X.copy()) 갱신. 실행 knapsack(0, K, 0)'])}
 {exam(['빈칸: 두 상한 식, size − S[i], i + 1', '변수 이름 바꿔 출제 대비: size = K − s(v), profit = p(v)'])}''', 17),
]))

build_summary(OUT, title='백트래킹 정리노트', unit='백트래킹 Backtracking', kick='', h1='백트래킹', h1_en='Backtracking', lead='', chapters=CH, pdf='backtracking.pdf')
print('ok', OUT)
