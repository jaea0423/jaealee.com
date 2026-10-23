# 2026_2_인공지능_8주차_Ensemble_Learning

<!-- p.1 -->

[인공지능]
Ensemble Learning
Eunsong Kang
eskang@kangwon.ac.kr
2026. 10. 22.

---

<!-- p.2 -->

Ensemble Learning
Ensemble learning is a method of combining multiple individual models to create an optimal
model with improved generalization.
Most popular ensemble methods
▶ Voting
▶ Bagging (i.e., random forests)
▶ Boosting (i.e., Adaboost, XGBoost)
▶ Stacking
1/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 원문 표기 그대로 — "Bagging (*i.e.*, random forests)", "Boosting (*i.e.*, Adaboost, XGBoost)"는 의미상 예시이므로 *e.g.*가 맞는 표현. 원문은 *i.e.*로 이탤릭 표기.)

---

<!-- p.3 -->

Voting Classifier
Suppose you have trained a few classifiers, each one achieving about 80% accuracy.
Training diverse classifiers
2/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림: Training diverse classifiers]**
- 아래쪽 평행사변형 판(학습 데이터): 2차원 좌표축 위에 파란색 채운 점(●)과 흰색 빈 점(○) 두 클래스의 샘플이 섞여 흩어져 있음.
- 이 학습 데이터에서 위쪽으로 화살표 4개가 뻗어 서로 다른 4개의 분류기(톱니바퀴 아이콘 상자)를 학습시킴. 상자 위 라벨(왼쪽→오른쪽):
  1. **Logistic Regression** (하늘색 상자)
  2. **SVM Classifier** (연보라색 상자)
  3. **Random Forest Classifier** (분홍색 상자)
  4. **Other...** (연노랑 상자)
- 오른쪽 굵은 글씨: **Diverse predictors** → 같은 데이터로 서로 다른 알고리즘의 분류기를 학습시킨다는 의미.

---

<!-- p.4 -->

Hard Voting Classifier
A simple way to create an even better classifier is to aggregate the predictions of each
classifier and predict the class that gets the most votes.
▶ Often achieves a higher accuracy than the best classifier in the ensemble.
Hard voting classifier predictions
3/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림: Hard voting classifier predictions]** (도식 안 원 출처 캡션: *Figure 7-2. Hard voting classifier predictions*)
- 맨 아래: **New instance**(X 표시된 회색 원) → 화살표 4개로 4개의 **Diverse predictors**(하늘색·연보라·분홍·연노랑 톱니바퀴 상자)에 입력.
- 각 예측기의 출력(**Predictions**, 원 안 숫자, 왼쪽→오른쪽): **1, 1, 2, 1** — 세 번째(분홍) 예측기만 클래스 **2**(파란색으로 채운 원), 나머지는 클래스 1(흰 원).
- 네 예측이 중괄호로 모여 위쪽으로 → **Ensemble's prediction (e.g., majority vote)** = **1** (1이 3표, 2가 1표이므로 다수결 결과 1).
(※ 검증: 표 집계 1:3표, 2:1표 → 다수결 1 — 일치)

---

<!-- p.5 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
- Even if each classifier is a weak learner, the ensemble can still be a strong learning, provided there is a sufficient number of weak learners and they are sufficiently diverse. (※ 원문 표기 그대로 — "strong learning"은 문맥상 "strong learner"의 오기)

**[그림 안 내용]**

Suppose that we have 5 independent classifiers for majority voting.

(그림: 분자 모형 모양 아이콘 5개가 가로로 나열 — classifier 1 (70%), classifier 2 (70%), classifier 3 (70%), classifier 4 (70%), classifier 5 (70%))

If the accuracy is 70% for each classifier, the accuracy of majority voting is:

$$(.7^5) + 5(.7^4)(.3) + 10(.7^3)(.3^2) = 0.8369$$

(설명: 5개 중 3개 이상 맞으면 다수결이 정답 → $\sum_{k=3}^{5}\binom{5}{k}0.7^k0.3^{5-k}$, 각 항은 5개 모두 정답 / 4개 정답($\binom{5}{4}=5$) / 3개 정답($\binom{5}{3}=10$).)
(※ 검증: Python으로 재계산 — $0.7^5+5\cdot0.7^4\cdot0.3+10\cdot0.7^3\cdot0.3^2 = 0.83692$, 이항분포 $P(X\ge3),\ X\sim B(5,0.7)$와 일치)

If there are 101 such classifiers, the majority voting accuracy is 0.99.

(※ 검증: Python으로 재계산 — $P(X\ge51),\ X\sim B(101,0.7) = 0.99998706\ldots$ 로, 슬라이드의 "0.99"는 실제 값(≈0.99999)을 낮게 반올림·절사한 표기. "0.99 이상"이라는 의미로는 맞음)

**Only true if all classifiers are perfectly independent, making uncorrelated errors, which is clearly not the case since they are trained on the same data** (진한 파란색 굵은 글씨 강조)

---

<!-- p.6 -->

Soft Voting Classifier
Soft Voting is a method in which the predicted class probabilities from each classifier are
averaged, and the class with the highest average probability is chosen as the final prediction.
In other words, it is a more refined approach than hard voting because it utilizes the
probability outputs of each classifier.
5/26

---

<!-- p.7 -->

Bagging and Pasting
Another approach is to use the same training algorithm for every predictor, but to train them
on different random subsets of the training set.
▶ Bagging (Bootstrapping): sampling with replacement
▶ Pasting: sampling without replacement
Pasting/bagging training set sampling and training
6/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림: Pasting/bagging training set sampling and training]**
- 맨 아래: **Training set** (평행사변형 판, 2차원 축 위 파란 ●와 흰 ○ 두 클래스 점들).
- Training set에서 화살표 4개 → **Random sampling (with replacement = bootstrap)** 으로 만든 4개의 부분 학습 집합(작은 평행사변형 판 4개). 각 판의 점 구성이 서로 조금씩 다름(무작위 추출, 복원추출이라 일부 점은 중복/누락).
- 각 부분 집합 위로 화살표 **Training** → 같은 종류(모두 하늘색 동일 톱니바퀴 아이콘)의 **Predictors (e.g., classifiers)** 4개를 학습.
- 즉 voting(p.3)과 달리 알고리즘은 동일하고 학습 데이터 부분집합만 다르다는 점을 보여줌.

---

<!-- p.8 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Why Bagging Lowers Variance?

- Generally, the net result is that the ensemble has a similar bias but a lower variance than a single predictor trained on the original training set.
- Assume that we measure a random variable $x \sim \mathcal{N}(\mu, \sigma^2)$. If we only have a single measurement $x_1$,
$$E[x_1] = \mu, \quad \text{and} \quad \mathrm{Var}(x_1) = \sigma^2$$
If we have measured $x$ $k$ times, and the value of $x$ is estimated as
$$\frac{x_1 + x_2 + \cdots + x_k}{K},$$
then
$$E\left[\frac{x_1 + x_2 + \cdots + x_k}{K}\right] = \mu;$$
$$\mathrm{Var}\left(\frac{x_1 + x_2 + \cdots + x_k}{K}\right) = \frac{K\sigma^2}{K^2} = \frac{\sigma^2}{K}$$

$\rightarrow$ Thus, bagging results in a model with smaller variance.

(※ 원문 표기 그대로 — 측정 횟수를 본문·분자 첨자에서는 소문자 $k$, 분모에서는 대문자 $K$로 혼용. 같은 값으로 읽어야 함)
(※ 검증: Python 시뮬레이션($\mu=3,\sigma=2,K=10$, 20만 회) — 평균 3.0018, 분산 0.3993 ≈ $\sigma^2/K=0.4$ 로 일치. 단, $\mathrm{Var}=K\sigma^2/K^2$는 $x_1,\dots,x_K$가 서로 **독립**일 때만 성립. 부트스트랩 표본으로 학습한 예측기들은 상관이 있으므로 실제 분산 감소폭은 $\sigma^2/K$보다 작음 — 상관계수 $\rho$이면 $\rho\sigma^2+\frac{1-\rho}{K}\sigma^2$)

---

<!-- p.9 -->

[Review] Bias and Variance
http://scott.fortmann-roe.com
8/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림: 편향-분산 과녁 비유 2×2 그림]** (출처 링크: http://scott.fortmann-roe.com)
- 열 제목: 왼쪽 **Low Variance**, 오른쪽 **High Variance** / 행 제목(세로 글씨): 위 **Low Bias**, 아래 **High Bias**.
- 각 칸은 과녁(바깥 흰 원 – 하늘색 고리 – 안쪽 흰 원 – 중앙 빨간 원(정답))과 남색 점들(모델 예측값)로 구성.
  - Low Bias + Low Variance (좌상): 점들이 중앙 빨간 원에 촘촘히 모여 있음 (이상적).
  - Low Bias + High Variance (우상): 점들이 중앙 주변(흰 원·하늘색 고리)에 넓게 흩어져 있지만 평균은 중앙.
  - High Bias + Low Variance (좌하): 점들이 촘촘히 모여 있으나 중앙에서 벗어난 위쪽(하늘색 고리 위 끝)에 몰려 있음.
  - High Bias + High Variance (우하): 점들이 중앙에서 벗어난 위쪽 바깥 영역에 넓게 흩어져 있음.
- 앞 슬라이드(배깅은 bias는 비슷하게 유지하고 variance를 낮춤)를 복습하는 그림.

---

<!-- p.10 -->

A single decision tree versus a bagging ensemble of 500 trees
9/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림: 두 개의 결정 경계 산점도 (moons형 2클래스 데이터)]**
- 공통: 가로축 $x_1$ (−1.5 ~ 2.5, 눈금 −1.5, −1.0, −0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5), 세로축 $x_2$ (−1.0 ~ 1.5, 눈금 −1.0, −0.5, 0.0, 0.5, 1.0, 1.5). 노란색 원(●) 클래스는 위쪽 초승달, 파란색 사각형(■) 클래스는 아래쪽 초승달 모양으로 분포하며 가운데에서 서로 겹침. 배경색 연노랑 = 노란 클래스로 예측된 영역, 연초록 = 파란 클래스로 예측된 영역, 진한 초록 선 = 결정 경계.
- 왼쪽 **Decision Tree** (단일 결정 트리): 경계가 축에 평행한 직선 조각들로만 이루어져 계단·사각형 모양. 대략 $x_1\approx-0.45$의 수직선, $x_2\approx0.4\sim0.5$ 부근의 수평선, $x_1\approx1.55$의 수직선 등과, 겹침 영역($x_1\approx0.0\sim1.3,\ x_2\approx-0.2\sim0.7$)에서 개별 점을 따라가는 작은 직사각형 섬들이 많음 → 학습 데이터에 과적합(높은 분산).
- 오른쪽 **Decision Trees with Bagging** (500개 트리 배깅): 경계가 $x_1\approx-0.5$에서 위로 올라가 $x_2\approx0.35$ 부근을 따라 가다가, $x_1\approx0.9\sim1.0$ 근처에서 $x_2\approx-0.05$까지 오목하게 내려간 뒤 $x_1\approx1.5$ 부근에서 다시 위로 올라가 상단까지 이어지는 하나의 비교적 매끄러운 곡선(잔 계단 모양). 작은 섬이 없어 일반화가 더 잘 됨.
(좌표값은 그림에서 눈으로 읽은 근사값 — 판독 확신 낮음)
- 결론: 배깅 앙상블은 단일 트리와 비슷한 편향을 가지면서 분산(경계의 불규칙성)이 훨씬 작음.

---

<!-- p.11 -->

Random Forest
A random forest is an ensemble of decision trees, generally trained via the bagging method
(or sometimes pasting).
The random forest algorithm introduces extra randomness when growing trees; instead of
searching for the very best feature when splitting a node, it searches for the best feature
among a random subset of features.
▶ This results in a greater tree diversity, which (once again) trades a higher bias for a lower
variance, generally yielding an overall better model.
Another great quality of random forests is that they make it easy to measure the relative
importance of each feature.
▶ Measures a feature’s importance by looking at how much the tree nodes that use that feature
reduce impurity on average (across all trees in the forest).
10/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(강조 표시: "**random forest**"는 굵게, "ensemble of decision trees"와 "it searches for the best feature among a random subset of features."에는 밑줄)

---

<!-- p.12 -->

11/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림: 랜덤 포레스트 예측 과정 도식]**
- 맨 위 **Test Sample Input** → 화살표로 **Tree 1**, **Tree 2**, **(. . .)**, **Tree 600** 각각에 입력.
- 각 트리는 깊이 2의 이진 트리(루트 1개, 중간 노드 2개, 리프 4개). 진한 회색 노드가 테스트 샘플이 지나가는 경로, 연회색은 지나가지 않는 노드:
  - Tree 1: 루트 → 오른쪽 자식 → 오른쪽(4번째) 리프
  - Tree 2: 루트 → 왼쪽 자식 → 왼쪽 자식의 오른쪽(2번째) 리프
  - Tree 600: 루트 → 오른쪽 자식 → 오른쪽 자식의 왼쪽(3번째) 리프
- 도달한 리프에서 굵은 화살표 → **Prediction 1**, **Prediction 2**, **(. . .)**, **Prediction 600**.
- 모든 예측이 **Average All Predictions** 상자로 모임 → 아래 **Random Forest Prediction**.
- (참고: '평균'은 회귀의 경우이며, 분류에서는 다수결 투표 또는 클래스 확률 평균을 사용)

---

<!-- p.13 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Random Forest Variable Importance

1. Compute the out of bag (OOB) error for the original dataset ($e_i$).
2. Compute the OOB error for the dataset in which the variable $x_i$ is permuted ($p_i$).
3. Compute the variable importance based on the mean and standard deviation of $(p_i - e_i)$ over all trees in the population.

\* Out-of-Bag (OOB) Samples: Training instances not selected during bootstrap sampling.

(참고: 부트스트랩에서 $n$개 중 특정 샘플이 한 번도 뽑히지 않을 확률은 $(1-1/n)^n \to e^{-1}\approx 0.368$ 이므로, 각 트리에서 약 36.8%가 OOB 샘플, 약 63.2%가 학습에 사용됨. ※ 검증: Python으로 재계산 — $n=1000$일 때 $0.3677$, $1-e^{-1}=0.6321$ 일치)
(※ 원문 표기 — 1단계 $e_i$에 변수 첨자 $i$가 붙어 있으나 원래 데이터의 OOB 오차는 변수와 무관; 다음 슬라이드에서는 $e^{(t)}$로 $i$ 없이 표기)

---

<!-- p.14 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
- A feature is important if randomizing it on OOB data consistently increases the prediction error.
- For tree $t$ and feature $i$:
$$e^{(t)} = \mathrm{OOBError}^{(t)}\ \text{(original)}, \qquad p_i^{(t)} = \mathrm{OOBError}^{(t)}\ \text{(after permuting feature } i\text{)},$$
$$d_i^{(t)} \;=\; p_i^{(t)} - e^{(t)}.$$
- With $T$ trees,
$$\bar{d}_i = \frac{1}{T}\sum_{t=1}^{T} d_i^{(t)}, \qquad s_i^2 = \frac{1}{T-1}\sum_{t=1}^{T}\left(d_i^{(t)} - \bar{d}_i\right)^2.$$

$$\text{Importance score:} \qquad v_i = \frac{\bar{d}_i}{s_i}.$$

(설명: $\bar d_i$는 트리별 오차 증가량의 평균, $s_i$는 표본표준편차(분모 $T-1$). $v_i$가 클수록 해당 변수를 섞었을 때 오차가 일관되게 커지므로 중요한 변수.)
(※ 검증: Python 예시 — $d=(0.05,0.07,0.04,0.06)$이면 $\bar d=0.055$, $s=0.01291$(ddof=1), $v=4.26$ 으로 공식대로 계산됨. 참고로 Breiman/R `randomForest`의 scaled importance는 표준오차 $s_i/\sqrt{T}$로 나누므로 이 슬라이드 정의와 $\sqrt{T}$배 차이)

---

<!-- p.15 -->

Boosting
Boosting refers to any ensemble methods that can combine several weak learners into a
strong learner.
The general idea of most boosting methods is to train predictors sequentially, each trying to
correct its predecessor.
AdaBoost, Gradient Boosting, XGBoost, etc..
14/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(강조 표시: "**Boosting**" 굵게, "sequentially"에 밑줄, "*AdaBoost*, *Gradient Boosting*, *XGBoost*, *etc.*"는 이탤릭. ※ 원문 표기 그대로 — "etc.."처럼 마침표 2개)

---

<!-- p.16 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## AdaBoost

- Pay more attention to training instances that were underfitted.
- New predictors increasingly focus on hard cases.
- Training process:
  1. Train a base classifier (e.g., Decision tree) on the training set.
  2. Increase the weights of misclassified <u>instances</u>.
  3. Train the next classifier on the updated weights.
  4. Repeat and combine all classifiers into an ensemble.

(그림 설명: 단계 번호는 원 안의 숫자 ①~④로 표시됨. 2번 항목의 "instances"에 밑줄 강조.)

---

<!-- p.17 -->

AdaBoost sequential training with instance weight updates
16/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(그림 설명: AdaBoost의 순차 학습 도식 — Géron 『Hands-On ML』 Figure 7-7과 같은 그림.)
- 아래 줄: 학습 데이터셋을 나타내는 평행사변형 4개(왼쪽→오른쪽), 각 안에 x·y축과 파란 점(인스턴스).
  - 1번째 데이터셋: 모든 점이 같은 진한 파란색(초기 가중치가 모두 같음, $w^{(i)}=1/m$).
  - 2~4번째 데이터셋: 직전 예측기가 잘 맞힌 점은 연한(흐린) 파란색, 틀린 점은 진한 파란색 → 진하기 = 인스턴스 가중치(틀린 샘플의 가중치가 커짐).
- 가운데 줄: 톱니바퀴 아이콘이 든 하늘색 상자 4개 = 예측기(학습 알고리즘). 각 데이터셋 → 위쪽 화살표 → 예측기.
- 위 줄: 예측기 1~3의 결과 그래프(평행사변형) 3개 — 파란 점들 위에 빨간 곡선(학습된 예측). 각 결과 그래프에서 오른쪽 아래로 향하는 대각선 화살표가 다음 단계의 (가중치가 갱신된) 데이터셋으로 이어짐.
- 4번째 예측기는 위쪽 결과 그래프 없이 끝남(계속 반복됨을 의미).
- 그림 캡션: "AdaBoost sequential training with instance weight updates".

---

<!-- p.18 -->

https://injo.tistory.com/31
17/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(그림 설명: 약한 학습기 2개를 결합해 강한 학습기를 만드는 AdaBoost 예시. 빨간 점·초록 점 두 클래스의 2차원 데이터.)
- 왼쪽 위 "Dataset": 빨간 점 8개, 초록 점 4개(오른쪽 아래 영역)가 모두 같은 크기(같은 가중치).
- 왼쪽 아래 "Weak learner #1": 오른쪽으로 기운 대각선 점선 경계 하나로 공간을 둘로 나눔 — 왼쪽 위(살구색) = 빨강 영역, 오른쪽 아래(연두색) = 초록 영역. 초록 영역 안에 들어간 빨간 점 1개가 원으로 표시됨(오분류).
- 꺾인 화살표 → 가운데 위 "Weighted dataset": 같은 데이터인데, 오분류됐던 그 빨간 점이 더 큰 점 + 원 표시로 강조됨(가중치 증가).
- 가운데 아래 "Weak learner #2": 거의 수평인 점선 경계 — 위쪽(살구색) = 빨강, 아래쪽(연두색) = 초록. 가중치가 커진 큰 빨간 점은 이제 빨강 영역에 들어가 올바르게 분류되지만, 왼쪽 아래의 다른 빨간 점 1개가 초록 영역에 남음.
- 오른쪽 굵은 화살표 → "Strong learner": 두 경계(대각선 점선 + 수평 점선)를 결합해 오른쪽 아래 부분만 초록(연두색), 나머지는 빨강(살구색) 영역으로 나눈 결과 — 12개 점이 모두 올바른 영역에 위치.
- 출처 링크: https://injo.tistory.com/31
(※ 검증: 그림처럼 12개 중 1개만 틀린 경우를 Python으로 계산 — 초기 $w=1/12$, $r_1=1/12\approx0.0833$, $\eta=1$일 때 $\alpha_1=\log 11\approx2.398$, 갱신·정규화 후 틀린 점 가중치 $0.5$, 나머지 각 $1/22\approx0.0455$(11배 차이) → 같은 예측기의 가중 오차율이 정확히 0.5가 됨. 그림의 "틀린 점이 커진다"는 설명과 일치)

---

<!-- p.19 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## AdaBoost: Weighted Error & Predictor Weight

- Each instance has an initial weight $w^{(i)} = \frac{1}{m}$, where $m$ is the number of training instances.
- A predictor is trained and its **weighted error rate** is calculated:

$$r_j = \frac{\sum_{i=1}^{m} w^{(i)}\, \mathbf{1}\big(\hat{y}_j^{(i)} \neq y^{(i)}\big)}{\sum_{i=1}^{m} w^{(i)}}$$

  where $\hat{y}_j^{(i)}$ is the prediction of the $j$-th predictor for the $i$-th instance.

- The predictor's weight $\alpha_j$ is then computed using:

$$\alpha_j = \eta \log\left(\frac{1 - r_j}{r_j}\right)$$

  - $\eta$: learning rate
  - If the predictor is accurate, $\alpha_j$ is high.
  - If it's worse than random guessing, $\alpha_j < 0$.

(※ 검증: Python으로 재계산 — $\eta=1$일 때 $r=0.1\to\alpha=2.197$, $r=0.3\to0.847$, $r=0.5\to0$, $r=0.6\to-0.405$, $r=0.9\to-2.197$. 정확할수록 $\alpha$가 크고 $r>0.5$이면 음수 — 일치. 단 "random guessing" 기준 $r=0.5$는 이진 분류 기준이며, 다중 클래스(SAMME)에서는 $\alpha_j=\eta\left[\log\frac{1-r_j}{r_j}+\log(K-1)\right]$로 $\log(K-1)$ 항이 추가됨 — 슬라이드 식은 $K=2$인 경우와 같음)
(※ 검증: 이 식(= SAMME, 이진)으로 직접 구현한 AdaBoost를 make_moons 데이터·깊이 1 결정 트리 5개로 돌려 sklearn `AdaBoostClassifier(algorithm="SAMME", learning_rate=0.5)`와 비교 — 예측기 가중치 [0.7582, 0.4300, 0.5076, 0.4484, 0.3584]와 예측 결과가 100% 일치)

---

<!-- p.20 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## AdaBoost: Weight Update & Final Prediction

- Instance weights are updated:

$$w^{(i)} \leftarrow \begin{cases} w^{(i)} & \text{if } \hat{y}_j^{(i)} = y^{(i)} \\ w^{(i)} \cdot \exp(\alpha_j) & \text{if } \hat{y}_j^{(i)} \neq y^{(i)} \end{cases}$$

  - Normalize all weights so that $\sum_{i=1}^{m} w^{(i)} = 1$
- Train a new predictor with updated weights.
- Repeat until desired number of predictors is reached or perfect predictor is found.
- Final Prediction: Weighted majority vote

$$\hat{y}(\mathbf{x}) = \underset{k}{\arg\max} \sum_{\substack{j=1 \\ \hat{y}_j(\mathbf{x}) = k}}^{N} \alpha_j$$

  where $N$ is the total number of predictors and $k$ is the index of class.

(※ 검증: Python으로 재계산 — 가중치 갱신 후 정규화하면 직전 예측기의 가중 오차율이 정확히 0.5가 되어 다음 예측기는 그 예측기가 틀린 샘플에 더 집중하게 됨(12개 중 1개 오분류 예: 0.0833 → 0.5). 가중 다수결 예: $\alpha=(1.2, 0.8, 0.6)$인 세 예측기가 각각 클래스 (0, 1, 1)을 예측하면 클래스 0 점수 1.2, 클래스 1 점수 1.4 → $\hat{y}=1$ (단순 다수결과 같지만, 첫 예측기 $\alpha$가 1.5보다 크면 결과가 0으로 바뀜) — 일치)

---

<!-- p.21 -->

Gradient Boosting
Gradient boosting is a popular boosting algorithm.
▶ Like AdaBoost, it builds an ensemble by sequentially adding predictors.
▶ Each new predictor corrects the errors of its predecessor.
Instead of adjusting instance weights, gradient boosting fits the new predictor to the residual
errors made by the previous one.
Gradient boosting can be used for different problems: regression, classification, and ranking.
20/26

---

<!-- p.22 -->

Gradient Boosting
21/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(그림 설명: 그래디언트 부스팅 과정 — Géron 『Hands-On ML』 Figure 7-9. 3행×2열 subplot, 가로축은 모두 $x_1$(−0.5~0.5, 눈금 −0.4, −0.2, 0.0, 0.2, 0.4).)
- 왼쪽 열 제목 "Residuals and tree predictions" / 오른쪽 열 제목 "Ensemble predictions".
- 1행 왼쪽: 세로축 $y$(0.0~0.8). 파란 점 = "Training set"(U자형(2차 곡선) 데이터), 초록 계단선 = $h_1(x_1)$(첫 번째 트리의 예측, 4단 계단: 약 0.66 → 0.49 → 0.12 → 0.53).
- 1행 오른쪽: 같은 Training set + 빨간 계단선 "$h(x_1) = h_1(x_1)$"(앙상블 = 첫 트리 그대로).
- 2행 왼쪽: 세로축 $y - h_1(x_1)$(−0.4~0.4). 검은 "+" = "Residuals"(1차 잔차), 초록 계단선 = $h_2(x_1)$(잔차에 맞춘 두 번째 트리: 약 0 → 0.16 → −0.09 → 0.04).
- 2행 오른쪽: 빨간 계단선 "$h(x_1) = h_1(x_1) + h_2(x_1)$" — 계단이 더 잘게 나뉘어 U자 곡선에 더 가까워짐.
- 3행 왼쪽: 세로축 $y - h_1(x_1) - h_2(x_1)$(−0.4~0.4). 검은 "+" = 2차 잔차, 초록 계단선 = $h_3(x_1)$(대부분 0 근처, 0.32 이후 약 −0.07, 0.47 이후 0.1~0.18로 상승).
- 3행 오른쪽: 빨간 계단선 "$h(x_1) = h_1(x_1) + h_2(x_1) + h_3(x_1)$" — 데이터에 가장 잘 맞음. 가로축 라벨 $x_1$.
- 그림 캡션: "Gradient Boosting". 핵심: 각 새 트리는 이전 앙상블의 잔차(residual)에 학습하고, 앙상블 예측은 트리 예측의 합.
(※ 검증: Géron 원본 코드(`np.random.seed(42)`, `X = np.random.rand(100,1) - 0.5`, `y = 3*X[:,0]**2 + 0.05*np.random.randn(100)`, `DecisionTreeRegressor(max_depth=2)` 3개를 잔차에 순차 학습)로 재현 — $h_1$ 분할점 −0.43, −0.36, 0.322 / 값 0.661, 0.488, 0.124, 0.529; $h_2$ 분할점 −0.36, −0.214, 0.196 / 값 0.0, 0.16, −0.09, 0.04; $h_3$ 분할점 0.322, 0.47, 0.478 / 값 0.007, −0.069, 0.11, 0.182. 그림의 계단 위치·높이와 일치. 또한 `GradientBoostingRegressor(max_depth=2, n_estimators=3, learning_rate=1.0)` 예측 = $h_1+h_2+h_3$ — 일치)

---

<!-- p.23 -->

Source from Github
22/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(그림 설명: 그래디언트 부스팅을 골프에 비유한 그림. 왼쪽에 골프 스윙하는 사람, 오른쪽에 깃발 "y"(목표값)가 꽂힌 홀.)
- 오른쪽 위 파란 포물선 = "MSE Loss Function". 곡선 위 주황 점 3개: $(y - F_0)^2$(높은 위치), $(y - F_1)^2$(더 낮음), $(y - F_2)^2$(최저점 근처, 깃발을 약간 지나친 오른쪽). 각 점에서 아래로 점선이 내려와 공의 위치를 표시. 깃발(y) 위치가 포물선의 최저점.
- 공의 이동(위로 볼록한 호): 첫 큰 샷 $f_0$, 이어서 $\Delta_1$, $\Delta_2$(깃발을 지나침), $\Delta_3$(뒤로 되돌아옴), $\Delta_4$(작은 호) — 매번 남은 거리(잔차)를 줄이는 보정 샷.
- 아래 가로 막대 5개 = 누적 예측: $F_0$(가장 짧음) < $F_1$ < $F_2$(y를 넘어섬); $F_3$(y보다 조금 짧게 되돌아옴), $F_4$(y와 거의 일치). 즉 $F_m = F_{m-1} + \Delta_m$, 각 $\Delta_m$은 MSE의 음의 기울기(= 잔차 $y-F_{m-1}$) 방향으로 이동.
- 캡션: "Source from Github"("Github"는 링크).
(※ 검증: $L=\tfrac12(y-F)^2$의 음의 기울기 $-\partial L/\partial F = y-F$가 잔차와 같음을 Python으로 확인 — 일치. 그래서 MSE에서 그래디언트 부스팅 = 잔차 학습)
(판독 확신 낮음: 원 그림에서 $\Delta_3$, $\Delta_4$의 호가 겹쳐 있어 어느 호가 어느 기호인지 정확히 구분하기 어려움 — 막대 길이상 $F_3$이 뒤로 되돌아오고 $F_4$가 y에 맞음)

---

<!-- p.24 -->

XGBoost
XGBoost (Extreme Gradient Boosting) is a gradient boosting algorithm that builds trees
sequentially to correct previous errors, using advanced optimization and regularization to
reduce overfitting and enhance performance.
Advantages of XGBoost
23/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(그림 설명: "Advantages of XGBoost" — 가운데 "XGBoost" 로고를 반원 모양으로 둘러싼 6개 조각(아이콘+설명).)
- 왼쪽 아래 (빨강, 모니터 아이콘): Parallelized tree building
- 왼쪽 (초록, 가지치기 가위 아이콘): Tree pruning using depth-first approach
- 왼쪽 위 (노랑, CPU 칩 아이콘): Cache awareness and out-of-core computing
- 오른쪽 위 (빨강, 판사봉 아이콘): Regularization for avoiding overfitting
- 오른쪽 (초록, 물음표 아이콘): Efficient handling of missing data
- 오른쪽 아래 (노랑, 체크 표시 아이콘): In-built cross-validation capability

---

<!-- p.25 -->

https://medium.com/data-science/https-medium-com-vishalmorde-xgboost-algorithm-long-she-may-rein-edd9f99be63d
24/26

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(그림 설명: 결정 트리에서 XGBoost까지의 발전 과정 — 회색 S자 화살표로 이어진 다이아몬드 원 아이콘 6개(왼쪽→오른쪽, 위아래 번갈아 배치, 오른쪽으로 갈수록 파란색이 진해짐). 각 단계 설명:)
1. **Decision Trees**: A graphical representation of possible solutions to a decision based on certain conditions
2. **Bagging**: Bootstrap aggregating or Bagging is a ensemble meta-algorithm combining predictions from multiple-decision trees through a majority voting mechanism
3. **Random Forest**: Bagging-based algorithm where only a subset of features are selected at random to build a forest or collection of decision trees
4. **Boosting**: Models are built sequentially by minimizing the errors from previous models while increasing (or boosting) influence of high-performing models
5. **Gradient Boosting**: Gradient Boosting employs gradient descent algorithm to minimize errors in sequential models
6. **XGBoost**(보라색 글씨로 강조): Optimized Gradient Boosting algorithm through parallel processing, tree-pruning, handling missing values and regularization to avoid overfitting/bias
(※ 원문 표기 그대로 — "a ensemble"(문법상 an ensemble), "multiple-decision trees")

---

<!-- p.26 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Stacking

- Instead of using trivial functions to aggregate the predictions of all predictors in an ensemble, why don't we train a model to perform this aggregation?

(그림 3개 — Géron 『Hands-On ML』 Figure 7-12, 7-13, 7-14)

**① Aggregating predictions using a blending predictor**
- 맨 아래 "New instance"(⊗ 기호)가 3개의 예측기(톱니바퀴 상자: 하늘색·보라색·분홍색)에 들어감 → "Predict".
- 세 예측기의 "Predictions": 3.1, 2.7, 2.9.
- 이 세 예측값이 위쪽 초록 상자 "Blending"(블렌더, 메타 학습기)에 입력 → 최종 예측 3.0.

**② Training the first layer**
- 맨 아래 "Training set"(파란 점 산점도)을 "Split" → "Subset 1", "Subset 2".
- Subset 1으로 첫 번째 층의 세 예측기(하늘색·보라색·분홍색 톱니바퀴 상자)를 "Train".

**③ Training the blender**
- 맨 아래 "Subset 2"(홀드아웃 세트)를 첫 층의 세 예측기에 넣어 "Predict".
- 각 예측기의 "Predictions"(빨간 곡선이 그려진 그래프 3개)를 모아 "Blending training set"(빨간 점 산점도 — 예측값들이 입력 특성, 실제 타깃이 정답)을 만듦.
- 이 세트로 맨 위 초록 상자 "Blender"를 "Train (to combine predictions)".

(※ 검증: ①의 수치 — 세 예측의 단순 평균은 (3.1+2.7+2.9)/3 = 2.9인데 블렌더 출력은 3.0 → 블렌더가 단순 평균이 아니라 학습된 결합 함수임을 보여주는 예시(Python으로 평균 계산 — 2.9))

---

<!-- p.27 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Comparison of Ensemble Methods

| Method | Strengths | Limitations |
|---|---|---|
| Voting | Combines different algorithms so models can complement each other; simple to implement and quick to try. | If base models differ greatly in quality, weak ones can drag down overall performance. |
| Bagging | Lowers variance of high-variance learners, helping prevent overfitting; supports parallel training efficiently. | Limited effect for high-bias learners; all models share the same inductive bias (same base algorithm). |
| Boosting | Sequentially focuses on errors to correct them; can capture complex patterns and achieve high accuracy. | Sensitive to noise/outliers with risk of overfitting; training time and tuning complexity can be high. |
| Stacking | Can achieve strong performance by leveraging complementary models; meta-learner can improve generalization. | Requires careful meta-model choice and data-splitting strategy; structure is complex and harder to implement. |

---

<!-- p.28 -->

Thank You!
(Q & A)

---

<!-- p.29 -->

References
James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). An Introduction to Statistical Learning: with Applications in R.
New York: Springer.
G´eron, A. (2019). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (2nd ed.). O’Reilly Media, Inc.
Advanced Methods for Data Analysis [Lecture Notes]. Retrieved from
http://www.stat.cmu.edu/ ryantibs/advmethods/notes/highdim.pdf

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 원문 표기 그대로 — 세 번째 참고문헌 URL이 "http://www.stat.cmu.edu/ ryantibs/advmethods/notes/highdim.pdf"로 공백이 들어가 있음. 실제 주소는 "http://www.stat.cmu.edu/~ryantibs/advmethods/notes/highdim.pdf"로 보이며, LaTeX에서 "~"가 줄바꿈 없는 공백으로 처리되어 사라진 것으로 추정)
