# training-img — figure crops from training-slides.pdf

Source: `training-slides.pdf` (41 PDF pages, footer "n/38" = PDF page − 1). Every figure in the deck is an embedded raster, so each crop is the original embedded image (native resolution, soft mask composited onto white), trimmed with a small white margin. Page numbers below are footer numbers.

| file | footer page | 내용 | redraw |
|---|---|---|---|
| p04-gd-quiver.png | 4 | f(x,y)=x²/20+y²의 음의 기울기 벡터장(quiver), x∈[−10,10], y∈[−5,5] | yes — −∇f=(−x/10, −2y)를 격자에서 계산 |
| p04-sgd-path.png | 4 | SGD 갱신 경로(시작점 (−7,2), 30회)와 등고선 — y 방향 지그재그 | yes — η=0.95로 재현됨 |
| p06-momentum-path.png | 6 | Momentum 갱신 경로와 등고선 — 공이 구르듯 S자로 진동하며 수렴 | yes — η=0.1, α=0.9로 재현됨 |
| p08-adagrad-path.png | 8 | AdaGrad 갱신 경로와 등고선 — y 진동이 빠르게 줄고 x축을 따라 직진 | yes — η=1.5로 재현됨 |
| p10-adam-path.png | 10 | Adam 갱신 경로와 등고선 — 부드러운 곡선으로 최소점 근처 도달 | yes — η=0.3, β₁=0.9, β₂=0.999로 재현됨 |
| p11-optimizer-family-tree.png | 11 | 옵티마이저 계보도(GD→SGD→Adaptive/Momentum→Adam 계열, PyTorch·DeepSpeed 함수명) | yes — 상자·화살표 다이어그램 |
| p12-pytorch-optim-docs.png | 12 | PyTorch 공식 문서 torch.optim 'Algorithms' 페이지 스크린샷(다크 테마) | no — 웹 화면 스크린샷 |
| p16-sigmoid-hist-std1.png | 16 | 가중치 표준편차 1일 때 시그모이드 5개 층 활성화 히스토그램 — 0과 1에 몰린 U자형 | yes — 1000×100 입력, 5층 시뮬레이션(시드에 따라 막대 높이만 미세 차이) |
| p17-sigmoid-hist-std001.png | 17 | 가중치 표준편차 0.01일 때 시그모이드 활성화 히스토그램 — 0.5 부근에 집중 | yes — 같은 시뮬레이션, std=0.01 |
| p19-sigmoid-hist-xavier.png | 19 | Xavier 초기값(std=1/√n)일 때 시그모이드 활성화 히스토그램 — 넓게 퍼진 종 모양 | yes — 같은 시뮬레이션, std=0.1 |
| p21-relu-hist-init-compare.png | 21 | ReLU에서 초기값(std=0.01 / Xavier / He)별 5개 층 활성화 히스토그램(3행×5열, 행 캡션 포함 — 원문 오타 "Xaiver" 그대로) | yes — ReLU 5층 시뮬레이션으로 재현 확인됨 |
| p21-relu-loss-init-compare.png | 21 | 초기값별 MNIST 학습 손실 곡선(std=0.01 / Xavier / He, 2000 iterations) | no — 실제 MNIST 학습 실험 곡선(미니배치 무작위성으로 정확히 재현 불가) |
| p23-internal-covariate-shift.png | 23 | 내부 공변량 변화 — FC→ReLU 블록마다 입력 분포의 위치·폭이 달라지는 도식 | yes — 상자·화살표·분포 곡선의 단순 도식 |
| p24-batchnorm-network.png | 24 | Affine→Batch Norm→ReLU 구조의 배치 정규화 신경망 도식(입력 MNIST 숫자 '2') | yes — 블록 다이어그램(입력 숫자 이미지만 텍스트/아이콘으로 대체) |
| p27-batchnorm-train-accuracy.png | 27 | 배치 정규화 유무에 따른 훈련 정확도 비교(20 epochs) | no — 실제 학습 실험 곡선 |
| p30-overfitting-accuracy.png | 30 | 과적합 신경망의 훈련/시험 정확도(200 epochs) — 훈련 1.0 vs 시험 약 0.73 | no — 실제 학습 실험 곡선 |
| p32-weight-decay-accuracy.png | 32 | 가중치 감소 적용 시 훈련/시험 정확도(200 epochs) — 격차 축소 | no — 실제 학습 실험 곡선 |
| p33-dropout-network.png | 33 | 일반 신경망 vs 드롭아웃 신경망(5-5-5-1) 비교 도식 — 좌우 두 패널 합본 | yes — 노드·연결 다이어그램(삭제 뉴런 위치는 MD 기술대로) |
| p33-dropout-network-general.png | 33 | 위 도식의 왼쪽 패널: 완전연결 일반 신경망 | yes — 노드·연결 다이어그램 |
| p33-dropout-network-dropout.png | 33 | 위 도식의 오른쪽 패널: 일부 뉴런(⊗)을 지운 드롭아웃 신경망 | yes — 노드·연결 다이어그램 |
| p34-dropout-accuracy-compare.png | 34 | 드롭아웃 없음(왼쪽) vs 적용(오른쪽, ratio 0.15) 훈련/시험 정확도 — 좌우 두 그래프 합본 | no — 실제 학습 실험 곡선 |
| p34-dropout-accuracy-without.png | 34 | 위 그림 왼쪽: 드롭아웃 없음 — 훈련 1.0 vs 시험 약 0.77 | no — 실제 학습 실험 곡선 |
| p34-dropout-accuracy-with.png | 34 | 위 그림 오른쪽: 드롭아웃 적용 — 훈련 약 0.87, 시험 약 0.68로 격차 축소 | no — 실제 학습 실험 곡선 |
| p38-optuna-website.png | 38 | Optuna 공식 웹사이트 화면(배너 + 'Towards Optuna v5' 카드 3개) | no — 웹 화면 스크린샷 |

Notes
- p16/p17/p19 are small in the source (579×156 px embedded at 144 ppi); the crops keep native resolution, so a redrawn SVG would look much sharper.
- p33 and p34 are provided both as the original two-panel image and as separate left/right files.
- The p21 histogram image extends past the bottom of the slide in the PDF; the crop is the full embedded image, so the "He Initialization" row and caption are complete.
