# cnn-img — figure crops from cnn-slides.pdf

Source: `../cnn-slides.pdf` (42 PDF pages). File prefix `pNN` = slide footer number `NN/39` = PDF page − 1.
All figures in this deck are embedded rasters. Each was extracted with `pdfimages`, its soft mask (transparency) composited onto white, then trimmed to content with a small white margin. Captions under the figures (e.g. "Example of convolution operation") and source URLs are vector text on the slide and are NOT included.

No figures on footer pages 04 (text list), 10, 17 (text/equations), 33, 36 (text), 40–41 (end slides). Page 00 (title) and the KNU logo are skipped.

| file | footer page | 내용 | redraw | notes |
|---|---|---|---|---|
| p01-image-classification.png | 1 | 고양이·골든리트리버 사진 + 분류 결과 패널(Cat ✓, Dog ✓) | no | 사진 |
| p02-detection-segmentation.png | 2 | 같은 사진의 객체 탐지(바운딩 박스) vs 분할(픽셀 단위 색칠) 비교 | no | 사진 위 오버레이 |
| p03-image-captioning.png | 3 | 이미지 캡셔닝 흐름: 사진 → Model(CNN Encoder / Language Decoder) → Caption 문장 | no | 사진 포함(상자·화살표 부분만은 재작도 가능) |
| p03-text-to-image.png | 3 | 텍스트→이미지 생성 흐름: Text 상자 → Image Generation Model → 생성 사진 | no | 사진 포함(상자·화살표 부분만은 재작도 가능) |
| p05-recognition-challenges.png | 5 | 이미지 인식의 어려움 7가지를 보여 주는 고양이 사진 7장(윗줄 3, 아랫줄 4) | no | 사진 모음, 슬라이드에 라벨 없음 |
| p06-grayscale-pixels.png | 6 | 흑백 사진 일부 영역 확대 → 0~255 픽셀값 19×16 배열, 라벨 Height (H) × Width (W) | no | 사진 포함. 숫자 배열은 AI_week12_CNN.md p.7에 전사됨 |
| p07-rgb-channels.png | 7 | 컬러 사진과 R·G·B 3채널로 분리해 겹친 그림, 라벨 RGB Channel, H × W × 3 | no | 사진 |
| p08-fc-network.png | 8 | 완전연결 신경망 블록도: 입력 "2" → (Affine→ReLU)×4 → Affine → Softmax | yes | 단순 블록 체인, 흰 상자 |
| p09-cnn-network.png | 9 | CNN 블록도: "2" → Conv→ReLU→Pooling ×2 → Conv→ReLU → Affine→ReLU → Affine→Softmax (Conv·Pooling 회색) | yes | 단순 블록 체인 |
| p11-conv-example.png | 11 | 합성곱 연산 예: 입력 4×4 ⊛ 필터 3×3 → 출력 2×2 | yes | Input `[[1,2,3,0],[0,1,2,3],[3,0,1,2],[2,3,0,1]]`; Filter `[[2,0,1],[0,1,2],[1,0,2]]`; Output `[[15,16],[6,15]]`. 라벨 "Input data", "Filter (Kernel)" |
| p12-conv-steps-1-2.png | 12 | 합성곱 계산 1~2단계(윈도우 회색, 채워지는 출력 칸 회색) | yes | 입력·필터는 p11과 동일. 1단계: 창 1~3행·1~3열 → 출력 (1,1)=15. 2단계: 창 1~3행·2~4열 → 출력 15 16 |
| p13-conv-steps-3-4.png | 13 | 합성곱 계산 3~4단계 | yes | 3단계: 창 2~4행·1~3열 → (2,1)=6. 4단계: 창 2~4행·2~4열 → (2,2)=15. 최종 `[[15,16],[6,15]]` |
| p14-conv-bias.png | 14 | 합성곱 + 편향: 입력 ⊛ 필터 → 2×2 + Bias 3 → 출력 | yes | 입력·필터 p11과 동일; 합성곱 `[[15,16],[6,15]]`; Bias `3`; Output `[[18,19],[9,18]]`. 라벨 Input data / Filter (Kernel) / Bias / Output data |
| p15-padding.png | 15 | 패딩 1(점선 빈 칸 테두리) 입력 ⊛ 필터 → 4×4 출력 | yes | 입력 4×4(p11과 동일) + 폭 1 점선 패딩(빈 칸=0); Filter p11과 동일; Output `[[7,12,10,2],[4,15,16,10],[10,6,15,6],[8,10,4,3]]`. 형상 라벨 (4, 4), (3, 3), (4, 4); "Input data (padding: 1)" |
| p16-stride-2.png | 16 | 스트라이드 2 합성곱 2단계(위: 첫 창, 아래: 오른쪽 2칸 이동, "Stride: 2" 곡선 화살표) | yes | Input 7×7 `[[1,2,3,0,1,2,3],[0,1,2,3,0,1,2],[3,0,1,2,3,0,1],[2,3,0,1,2,3,0],[1,2,3,0,1,2,3],[0,1,2,3,0,1,2],[3,0,1,2,3,0,1]]`; Filter `[[2,0,1],[0,1,2],[1,0,2]]`; 출력 3×3 격자에 위: (1,1)=15, 아래: 15 17 (나머지 빈 칸). 회색 창: 위 1~3행·1~3열, 아래 1~3행·3~5열 |
| p18-conv-3d.png | 18 | 3채널 입력(4×4×3) ⊛ 3채널 필터(3×3×3) → 출력 2×2(1채널) | yes | 앞 채널 입력 p11과 동일, 앞 채널 필터 p11과 동일. 가운데 입력: 첫 행 `3 0 6 5`, 오른쪽 열 `5,3,0,1`(부분); 뒤 입력: 첫 행 `4 2 1 2`, 오른쪽 열 `2,4,2,5`. 가운데 필터: 첫 행 `0 1 3`, 오른쪽 열 `3,2,0`; 뒤 필터: 첫 행 `4 0 2`, 오른쪽 열 `2,0,2`. Output `[[63,55],[18,51]]`. 나머지 값은 원본에서도 가려져 있으므로 보이는 값만 그리면 됨 |
| p19-conv-3d-steps-1-2.png | 19 | 3차원 합성곱 1단계(위)·2단계(아래) — 세 채널 공통 창 회색 | yes | p18과 같은 값. 1단계: 창 1~3행·1~3열 → 출력 63 _ / _ _. 2단계: 창 1~3행·2~4열 → 63 55 / _ _ |
| p19-conv-3d-steps-3-4.png | 19 | 3차원 합성곱 3단계(위)·4단계(아래) | yes | 3단계: 창 2~4행·1~3열 → 63 55 / 18 _. 4단계: 창 2~4행·2~4열 → 63 55 / 18 51 |
| p20-blocks-single-filter.png | 20 | 블록으로 본 3차원 합성곱: (C,H,W) ⊛ (C,FH,FW) → (1,OH,OW) | yes | 회색 직육면체 3개 + 치수 라벨 C/H/W, C/FH/FW, OH/OW; 아래 줄 형상과 Input data / Filter (Kernel) / Output data |
| p21-blocks-fn-filters.png | 21 | 필터 FN개: (C,H,W) ⊛ (FN,C,FH,FW) → (FN,OH,OW) | yes | 필터 블록 세로 나열(점선 생략) + "FN개" 라벨, 출력은 FN장 겹친 판 |
| p22-blocks-bias.png | 22 | 편향 포함 처리 흐름: (C,H,W) ⊛ (FN,C,FH,FW) → (FN,OH,OW) + (FN,1,1) → (FN,OH,OW) | yes | Bias 블록은 FN×1×1 막대. 라벨 Input data / Filter (Kernel) / Bias / Output data |
| p23-max-pooling-steps.png | 23 | 2×2 최대 풀링(stride 2) 4단계 — 창 회색, 최댓값 굵은 테두리 | yes | Input `[[1,2,1,0],[0,1,2,3],[3,0,1,2],[2,4,0,1]]`. 단계별 최댓값 2(1행2열), 3(2행4열), 4(4행2열), 2(3행4열). 출력 `[[2,3],[4,2]]` (단계마다 채워진 칸만 표시) |
| p24-pooling-channels.png | 24 | 풀링은 채널 수 유지: 3채널 4×4 → 3채널 2×2 | yes | 앞 입력 p23과 동일 → 앞 출력 `[[2,3],[4,2]]`. 가운데 입력 첫 행 `3 0 6 5`, 오른쪽 열 `5,3,0,1` → 출력 첫 행 `3 6`, 오른쪽 아래 `2`. 뒤 입력 첫 행 `4 2 1 2`, 오른쪽 열 `2,4,2,5` → 출력 첫 행 `4 4`, 오른쪽 아래 `5`. 슬라이드 캡션 "The number of channels remains unchanged."는 미포함 |
| p24-pooling-robustness.png | 24 | 입력이 한 칸 밀려도 3×3 최대 풀링(stride 3) 결과가 같음 | yes | 왼쪽 6×6 `[[1,2,0,7,1,0],[0,9,2,3,2,3],[3,0,1,2,1,2],[2,4,0,1,0,1],[6,0,1,2,1,2],[2,4,0,1,8,1]]` → `[[9,7],[6,8]]`. 오른쪽(1열 오른쪽 이동) `[[1,1,2,0,7,1],[3,0,9,2,3,2],[2,3,0,1,2,1],[3,2,4,0,1,0],[2,6,0,1,2,1],[1,2,4,0,1,8]]` → `[[9,7],[6,8]]`. 왼쪽 위 3×3 창 회색, 최댓값 9·7·6·8 굵은 테두리. 슬라이드 캡션은 미포함 |
| p25-first-layer-weights.png | 25 | 1층 합성곱 필터 30개의 학습 전(잡음) / 학습 후(에지·블롭) 시각화 | no | 가중치 시각화 이미지 |
| p26-feature-hierarchy.png | 26 | 층 깊이별 특징 시각화: low / mid / high-level features (각 5×6 격자) | no | 특징 시각화 이미지(출처 tvirdi.github.io) |
| p27-human-visual-system.png | 27 | 뇌 시각 경로(눈→LGN→V1→V2→V4→IT), 수용 영역 크기, 특징 계층(edges and lines→shapes→objects→faces) | no | 뇌 일러스트. 오른쪽 두 패널(Receptive fields size, Features)만은 재작도 가능 |
| p28-ilsvrc-top5-error.png | 28 | ILSVRC 우승 모델 Top-5 error 막대그래프 | yes | 2010 NEC America 28.2, 2011 Xerox 25.8, 2012 AlexNet 16.4, 2013 Clarifi 11.7, 2014 VGG 7.3, 2014 GoogLeNet 6.7, 2015 ResNet 3.5; y축 0–30 (5 간격) |
| p29-lenet-architecture.png | 29 | LeNet-5 구조도(GfG): INPUT 32×32 → C1 6@28×28 → S2 6@14×14 → C3 16@10×10 → S4 16@5×5 → C5 120 → F6 84 → OUTPUT 10 | yes | 연산 라벨 Convolutions / Subsampling / Full Connection / Gaussian Connections. 원본은 연회색 배경, GfG 로고 포함 |
| p30-lenet-table.png | 30 | LeNet 층 구성 표(검은 배경 이미지 표) | yes | 표 값은 AI_week12_CNN.md p.31에 전사됨("Avergae" 오타 원문 그대로). HTML 표로 대체 가능 |
| p31-alexnet-architecture.png | 31 | AlexNet 2-GPU 구조도(224×224×3, 11×11 stride 4 → 55×55×48 ×2 → … → Dense 2048 ×2 → 1000) | yes | 라벨 많음. 값은 AI_week12_CNN.md p.32 참조. 원본 입력 224(표는 227) |
| p32-alexnet-table.png | 32 | AlexNet 층 구성 표 | yes | 값은 AI_week12_CNN.md p.33에 전사. HTML 표로 대체 가능 |
| p34-vggnet16.png | 34 | VGG16 3D 블록 구조도(conv1~conv5, pool, fc6~fc8, 범례 3색) | yes | 크기 라벨 224×224×64, 112×112×128, 56×56×256, 28×28×512, 14×14×512, 7×7×512, 1×1×4096, 1×1×1000. 왼쪽 입력 흑백 사진은 원본에서도 잘려 있음(사진 대신 빈 판으로 표현) |
| p35-vggnet-table.png | 35 | VGGNet 층 구성 표 | yes | 값은 AI_week12_CNN.md p.36에 전사(Layer 5 "2 X Convolution" 원문 그대로). HTML 표로 대체 가능 |
| p37-resnet-architectures.png | 37 | VGG-19 / 34-layer plain / 34-layer residual 비교(원 그림을 90° 회전, 오른쪽→왼쪽 흐름) | yes | 원본 해상도가 낮고 글자가 회전·매우 작음 — 사이트용으로는 재작도 권장. 층 구성은 AI_week12_CNN.md p.38에 전사 |
| p38-depth-degradation.png | 38 | CIFAR-10 plain 20층 vs 56층의 training/test error 곡선 2개 | no | 곡선 원데이터 미상(눈대중 근삿값만 있음) |
| p39-residual-block.png | 39 | 잔차 블록: x → weight layer → relu → weight layer → ⊕(x identity) → relu, 라벨 F(x), F(x)+x | yes | 단순 블록도. 원본은 아주 연한 회색 배경, 왼쪽 아래 캡션 "A residual block"(이미지 내부 텍스트) 포함 |

Counts: 37 PNG files — redraw yes 26, no 11.
