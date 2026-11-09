# 2026_2_인공지능_9주차_Perceptron

<!-- p.1 -->

[인공지능]
Perceptron & Artificial Neural Networks
Eunsong Kang
eskang@kangwon.ac.kr
2026. 11. 2.

---

<!-- p.2 -->

Artificial Intelligence vs. Machine Learning vs. Deep Learning
1/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림] AI ⊃ ML ⊃ DL 포함 관계 (동심원 다이어그램)**

가장 큰 원(진한 남색) 안에 중간 원(파랑), 그 안에 가장 작은 원(하늘색)이 겹쳐 있는 구조로, 딥러닝 ⊂ 머신러닝 ⊂ 인공지능의 포함 관계를 보여줌.

- **ARTIFICIAL INTELLIGENCE** (바깥 원): A program that can sense, reason, act, and adapt
- **MACHINE LEARNING** (중간 원): Algorithms whose performance improve as they are exposed to more data over time
- **DEEP LEARNING** (가장 안쪽 원): Subset of machine learning in which multilayered neural networks learn from vast amounts of data

---

<!-- p.3 -->

Machine Learning vs. Deep Learning
https://www.telliant.com/consider-adding-deep-learning-to-your-next-software-project/
2/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림] 머신러닝과 딥러닝의 처리 파이프라인 비교 (자동차 인식 예시)**

위·아래 두 줄의 흐름도이며, 각 단계는 파란 화살표(→)로 연결됨.

1. **MACHINE LEARNING** (위쪽 줄)
   - INPUT (자동차 그림) → FEATURE EXTRACTION (사람이 모니터의 뇌 그림·막대그래프를 보며 직접 특징을 뽑는 모습) → CLASSIFICATION (트리 구조 노드 그림, 분류기) → OUTPUT (원 안에 `CAR` / 점선 / `NOT CAR`)
   - 즉, 특징 추출은 사람이, 분류는 모델이 별도 단계로 수행.
2. **DEEP LEARNING** (아래쪽 줄)
   - INPUT (자동차 그림) → FEATURE EXTRACTION + CLASSIFICATION (노드 3개씩 7열로 이루어진 완전연결 신경망 그림) → OUTPUT (원 안에 `CAR`(체크박스 목록 아이콘) / 점선 / `NOT CAR`)
   - 즉, 특징 추출과 분류를 하나의 신경망이 함께(end-to-end) 학습.

출처 링크(그림 하단): https://www.telliant.com/consider-adding-deep-learning-to-your-next-software-project/

---

<!-- p.4 -->

The machine learning model learns from features selected or designed by humans.
Edges Gradient orientations
3/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림] 사람이 설계한 특징(hand-crafted features)의 예 — 고양이 이미지**

- 왼쪽 그림 **Edges**: 검은 배경에 고양이 얼굴·수염·털의 윤곽선(에지)만 흰 선으로 검출된 에지 맵.
- 오른쪽 그림 **Gradient orientations**: 연한 배경 위에 격자(약 16×16)로 배치된 짧은 보라색 선분들 — 각 위치(셀)의 그래디언트 방향을 선분의 기울기로 나타낸 것(HOG류 특징의 방향 표시).
- 의미: 전통적 머신러닝에서는 이런 에지·그래디언트 방향 같은 특징을 사람이 선택·설계해 모델에 입력함.

---

<!-- p.5 -->

Timeline of Deep Learning
Adapted from Favio V´azquez
4/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림] 딥러닝 발전 연표 (가로 타임라인)**

회색 가로 막대(시간축) 위에 색깔 점이 찍혀 있고, 각 점에서 위 또는 아래로 선이 뻗어 사건 라벨과 연결됨(오른쪽 끝은 점점 흐려짐). 연도순 정리(원문 표기 그대로):

| 연도 | 사건 (그림 속 표기) | 인물 | 위치 |
|---|---|---|---|
| 1940 | Dark Era Until 1940 | — | 위 |
| 1943 | Neural Nets | McCulloch & Pitt | 아래 |
| 1950 | Computing Machinery and Intelligence | Alan Turing | 위 |
| 1958 | Perception | Rosenblatt | 아래 |
| 1960 | ADALINE | Widrow & Hoff | 위 |
| 1969 | XOR problem | Minsky & Papert | 아래 |
| 1974 | Backpropagation | Werbos (and more) | 위 |
| 1980 | Neocogition | Fukushima | 위 |
| 1980 | Self Organizing Map | KOhonen | 아래 |
| 1982 | Hopfield Network | John Hopfield | 아래 |
| 1985 | Boltzman Machine | Hinton & Sejnowski | 위 |
| 1986 | Restricted Boltzman Machine | Smolensky | 위 |
| 1986 | Multilayer Perception | Rumelhart, Hinton & Williams | 아래 |
| 1986 | RNNs | Jordan | 아래 |
| 1990 | LeNet | Lecun | 위 |
| 1997 | LSTMs | Hochreiter & Schmidhuber | 위 |
| 1997 | Bidirectional RNN | Schuster & Paliwal | 아래 |
| 2006 | Deep Boltzman Machine | Salakhutdinov & Hinton | 위 |
| 2006 | Deep Belief Networks- pretraing | Hinton | 아래 |
| 2012 | AlexNet | Hinton | 아래 |
| 2014 | GANs | Goodfellow | 위 |
| 2017 | Capsule Networks | Sabour, Frosst & Hinton | 아래 |

- 그림에서 "Backpropaga / tion"은 줄바꿈되어 표기됨.
- (※ 원문 표기 그대로 — 1958 "Perception", 1986 "Multilayer Perception"은 Perceptron의 오기. "Boltzman"은 Boltzmann, "Neocogition"은 Neocognitron, "pretraing"은 pretraining, "KOhonen"은 Kohonen, "McCulloch & Pitt"는 McCulloch & Pitts의 오기로 보임)
- 출처 표기: Adapted from Favio Vázquez

---

<!-- p.6 -->

Timeline of Large Language Models
Le, N. L., & Abel, M. H. (2025). How Well Do LLMs Predict Prerequisite Skills? Zero-Shot Comparison to Expert-Defined Concepts. 5/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림] 대형 언어 모델(LLM) 발표 연표 (회사별 가로 타임라인)**

가로축(시간): Feb 2023, May 2023, Aug 2023, Nov 2023, Feb 2024, May 2024, Aug 2024, Nov 2024, Feb 2025, May 2025, Aug 2025 (세로 점선 눈금). 세로축: 회사별 행(색깔 라벨 상자). 각 행의 선 위 점이 모델 발표 시점이며, 같은 시기 동시 발표 모델은 네모 상자로 묶여 있음. 왼쪽→오른쪽(시간순) 모델 목록:

- **xAI** (초록): Grok 1 → Grok 1.5 → Grok 2 → Grok 3 → Grok 4
- **Baidu** (청록): Ernie 3.5 → Ernie 4 → Ernie 4 Turbo → [Ernie 4.5 / Ernie X1] → [Ernie 4.5 Turbo / Ernie X1 Turbo] → Ernie 5
- **Google** (노랑): Gemini 1.0 Pro & Nano → Gemini 1.0 Ultra → Gemini 1.5 Pro → Gemini 1.5 Flash → Gemini 2.0 Flash → Gemini 2.0 Pro → Gemini 2.5 Flash → [Gemini 2.5 Pro / Gemini 2.5 Flash Lite] (마지막은 갈라지는 두 가지)
- **DeepSeek** (빨강): DeepSeek V2 → DeepSeek LLM V1 → DeepSeek Coder V1 → DeepSeek Coder V2 → DeepSeek V2.5 → DeepSeek R1 → DeepSeek V3 → DeepSeek R2
- **Microsoft** (자주): Phi-1 → Phi-2 → Phi-3 → Phi-3.5 → Phi-4
- **Mistral** (보라): Mistral 7B → [Mistral Medium / Mistral 8x7B] → Mistral Large → Mistral 8x22B → Mistral Large 2 → Mistral Small 3 → Mistral Small 3.1 → Mistral Medium 3
- **Meta** (파랑): Llama → Llama 2 → Llama 3 → Llama 3.1 → Llama 3.2 → Llama 3.3 → Llama 4
- **Alibaba** (주황): Qwen 7B → Qwen 14B → [Qwen 72B / Qwen 1.8B] → Qwen 1.5 → Qwen 2 → Qwen 2.5 → [Qwen 2.5 turbo / Qwen 2.5 max] → Qwen 3
- **OpenAI** (파랑): GPT-4 → GPT-4 Turbo → GPT-4o → GPT-4o mini → o1-preview → o1 → [o1-pro / o3 / o3-mini] → GPT-4.5 → [GPT-4.1 / o4-mini] → o3-pro
- **Anthropic** (적갈색): Claude → Claude 2 → Claude Instant 1.2 → Claude 2.1 → [Claude Opus 3 / Claude Sonnet 3 / Claude Haiku 3] → Claude Sonnet 3.5 → Claude Haiku 3.5 → Claude Sonnet 3.7 → [Claude Sonnet 4 / Claude Opus 4]

대략적 위치: Llama·Claude·GPT-4가 Feb~Mar 2023 부근으로 가장 이르고, Grok 4·Ernie 5·Gemini 2.5 Pro/Flash Lite·o3-pro·Claude Sonnet 4/Opus 4가 May~Aug 2025 부근으로 가장 늦음. (개별 점의 정확한 월은 그림 눈금으로만 추정 가능 — 판독 확신 낮음)

- (※ 원문 표기 그대로 — 그림에서 DeepSeek V2가 DeepSeek LLM V1보다 앞(2023년 초)에, DeepSeek V3가 R1 뒤에 배치되어 있고, 마지막에 DeepSeek R2가 표시되어 있음)
- 출처 표기: Le, N. L., & Abel, M. H. (2025). How Well Do LLMs Predict Prerequisite Skills? Zero-Shot Comparison to Expert-Defined Concepts.

---

<!-- p.7 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# Biological Neurons

**[그림] 생물학적 뉴런의 구조** (왼쪽)

노란색 뉴런 두 개가 연결된 모습. 라벨:
- **Dendrite**: 세포체 주변의 가지 돌기(신호 수신)
- **Nucleus**: 세포체 중앙의 주황색 핵
- **Axon**: 세포체에서 뻗어 나온 긴 축삭(신호 전달)
- **Myelin sheath**: 축삭을 마디마디 감싸고 있는 초록색 수초
- **Synapse**: 한 뉴런의 축삭 말단과 다른 뉴런의 가지돌기가 만나는 부분(파란색으로 강조)
- **Glial cells**: 주변의 분홍·보라색 별 모양 세포(신경교세포)

(오른쪽 본문)

- Neuron ($10^{11}$): a special biological cell that processes information
  - Nucleus contains information about hereditary traits
  - Dendrites (receiver) receives signals (impulses) from other neurons
  - Axon (transmitter) transmits signals generated by its cell body
- Synapses ($10^{14}$): terminals of the strands
  - an elementary structure and functional unit between two neurons
  - neurons have connections to around $10^4$ other neurons
  - via certain chemicals (neurotransmitters)

---

<!-- p.8 -->

Why (Artificial) Neural Networks?
Many desirable characteristics of a brain, not present in modern computers
▶ Massive parallelism
▶ Distributed representation and computation
▶ Distributed information across multiple synaptic connections
▶ Learning ability
▶ Generalization ability
▶ Adaptivity
▶ Inherent contextual information processing
▶ Fault tolerance
▶ Low energy consumption
7/25

---

<!-- p.9 -->

Perceptron
Originated from attempts to mimic the human brain, which is responsible for intelligent
behavior.
Developed by Frank Rosenblatt in 1957.
8/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림] Rosenblatt의 퍼셉트론 원 논문 첫 페이지 일부(스캔 이미지)**

> *Psychological Review*
> Vol. 65, No. 6, 1958
>
> **THE PERCEPTRON: A PROBABILISTIC MODEL FOR INFORMATION STORAGE AND ORGANIZATION IN THE BRAIN**¹
>
> F. ROSENBLATT
>
> *Cornell Aeronautical Laboratory*
>
> (왼쪽 단) If we are eventually to understand the capability of higher organisms for perceptual recognition, generalization, recall, and thinking, we must first have answers to three fundamental questions:
>
> (오른쪽 단) and the stored pattern. According to this hypothesis, if one understood the code or "wiring diagram" of the nervous system, one should, in principle, be able to discover exactly what an organism remembers by reconstruct- … (이하 잘림)

- 참고: 본문은 "Developed ... in 1957"이고 논문 게재는 1958년(Psychological Review)임.

---

<!-- p.10 -->

”If we are eventually to understand the capability of higher organisms for perceptual
recognition, generalization, recall, and thinking, we must first have answers to three
fundamental question.”(우리가 궁극적으로 지각적 인식, 일반화, 기억 그리고 사고를 할 수
있는 고등 유기체의 능력을 이해하기 위해서는 먼저 세 가지 근본적인 질문에 대해 답할 수
있어야 한다.)
1. How is information about the physical world sensed, or detected, by the biological system?
(생물 시스템은 실제 물리적 세계에 대한 정보를 어떻게 감지할까?)
2. In what form is information stored, or remembered? (어떤 형태로 저장되거나 기억될까?)
3. How does information contained in storage, or in memory, influence recognition and behavior?
(스토리지 또는 메모리에 저장된 정보가 인식과 동작에 어떻게 영향을 미칠까?)
9/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
- (※ 원문 표기 그대로 — 인용문 끝이 "three fundamental question."으로 되어 있으나 원 논문(p.9 스캔)은 "three fundamental questions:"임. 또한 여는 따옴표가 닫는 따옴표(”) 모양으로 표기됨)

---

<!-- p.11 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# Perceptron

**[그림] 2입력 퍼셉트론 구조** (왼쪽)

원(노드) `x1`, `x2`에서 각각 화살표가 출력 노드 `y`로 향하며, 화살표 위에 가중치 `w1`, `w2`가 적혀 있음 (x1 —w1→ y, x2 —w2→ y).

- $x_1, x_2$: input
- $y$; output
- $w_1, w_2$: **weight**

(오른쪽 본문)

- Serves as the foundation of deep learning.
- Receives multiple input signals and produces a single output signal.
- Unlike biological neurons, it takes binary values (0 = no signal, 1 = signal activated).

$$
y = \begin{cases} 0 & (w_1x_1 + w_2x_2 \le \theta) \\ 1 & (w_1x_1 + w_2x_2 > \theta) \end{cases}
$$

  - A neuron outputs 1 only when the total input signal exceeds the threshold $\theta$.

---

<!-- p.12 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# Basic Logic Gates

- A perceptron can implement logic gates.

**AND gate**

| $x_1$ | $x_2$ | $y$ |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 1 | 1 |

$(w_1, w_2, \theta) = (0.5, 0.5, 0.7)$

**NAND gate**

| $x_1$ | $x_2$ | $y$ |
|---|---|---|
| 0 | 0 | 1 |
| 1 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 1 | 0 |

$(w_1, w_2, \theta) = (-0.5, -0.5, -0.7)$

**OR gate**

| $x_1$ | $x_2$ | $y$ |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 1 | 1 |

$(w_1, w_2, \theta) = (0.5, 0.5, 0.2)$

→ The structure of perceptrons is identical, but their parameters (weights and thresholds) differ.

- 가중합 $w_1x_1+w_2x_2$ 확인: AND·OR은 입력 (0,0),(1,0),(0,1),(1,1)에 대해 0, 0.5, 0.5, 1.0 → AND는 $\theta=0.7$보다 큰 것이 1.0뿐이라 (1,1)만 1, OR은 $\theta=0.2$보다 큰 0.5·0.5·1.0이 1. NAND는 0, −0.5, −0.5, −1.0 → $\theta=-0.7$보다 큰 0, −0.5, −0.5가 1이고 −1.0만 0. (※ 검증: Python으로 재계산 — 일치)

---

<!-- p.13 -->

12/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림] AND / OR / XOR 게이트의 입력 공간 그래프 (선형 분리 가능성)**

범례(상단): 보라색 네모 ■ = **1 output**, 빨간 원 ● = **0 output**

세 개의 2차원 그래프가 나란히 있으며, 각각 가로축 $x_1$ (눈금 0, 1), 세로축 $x_2$ (눈금 0, 1), 네 입력점 (0,0), (1,0), (0,1), (1,1)을 표시함.

| 입력 $(x_1,x_2)$ | AND Gate | OR Gate | XOR Gate |
|---|---|---|---|
| (0,0) | ● 0 | ● 0 | ● 0 |
| (1,0) | ● 0 | ■ 1 | ■ 1 |
| (0,1) | ● 0 | ■ 1 | ■ 1 |
| (1,1) | ■ 1 | ■ 1 | ● 0 |

- AND, OR은 직선 하나로 ■과 ●을 나눌 수 있지만, XOR은 ■이 대각선 (1,0)·(0,1)에, ●이 (0,0)·(1,1)에 있어 직선 하나로 분리할 수 없음을 보여줌(단층 퍼셉트론의 한계).
- (※ 검증: Python으로 재계산 — 일치. 단층 퍼셉트론(sklearn Perceptron)은 AND·OR 정확도 1.0, XOR 정확도 0.5에 그치며, $w_1,w_2,\theta\in[-2,2]$ 격자 탐색에서도 XOR을 만족하는 직선이 없음)

---

<!-- p.14 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# Weights and Bias

- If we replace $\theta$ with $-b$, the equation can be rewritten as follows:

$$
y = \begin{cases} 0 & (\, b + w_1x_1 + w_2x_2 \le 0 \,) \\ 1 & (\, b + w_1x_1 + w_2x_2 > 0 \,) \end{cases}
$$

→ $w_1, w_2$ are parameters that <u>control the influence (importance) of each input</u> on the output, while the bias ($b$) is a parameter that determines <u>how easily the neuron is activated.</u>

- (밑줄은 원문 강조) 예: AND 게이트 $(w_1,w_2,\theta)=(0.5,0.5,0.7)$는 $b=-0.7$, OR 게이트는 $b=-0.2$로 바꿔 써도 같은 출력. (※ 검증: Python으로 재계산 — 일치)

---

<!-- p.15 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Limitation of Perceptron

- The perceptron we have seen so far cannot implement the XOR gate.

[그림: XOR 입력점의 좌표평면 2개 (가로축 x1, 세로축 x2, 눈금 0과 1). 기호: ○ = 출력 0, △ = 출력 1]
- 왼쪽 그래프: (0,0)에 ○, (1,0)에 △, (0,1)에 △, (1,1)에 ○ — XOR 출력 분포만 표시.
- 오른쪽 그래프: 같은 네 점 위에 왼쪽 위에서 오른쪽 아래로 내려가는 파란 직선 하나를 그어 둠(대략 x2축을 1보다 조금 위(≈1.2), x1축을 ≈1.5 부근에서 지남). 이 직선 위쪽에는 (1,1)의 ○만, 아래쪽에는 (0,0)의 ○와 (1,0)·(0,1)의 △가 함께 놓임 → 직선 하나로는 ○와 △를 나눌 수 없음을 보여 줌.
  (※ 검증: Python으로 재계산 — 일치. 계단함수 단층 퍼셉트론 $w_1,w_2,b\in[-2,2]$ 격자 탐색에서 XOR을 맞히는 직선 없음, sklearn `Perceptron` 정확도 0.5)

XOR gate

| $x_1$ | $x_2$ | $y$ |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 1 | 0 |

→ If the constraint of linearity is removed, the data can be separated.
(※ 참고: 이 페이지 그림에는 곡선(비선형) 경계는 그려져 있지 않고, 실패하는 직선 경계만 있음)

---

<!-- p.16 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Multi-layer Perceptron

- The XOR gate can be constructed by combining AND, NAND, and OR gates.

XOR gate

| $x_1$ | $x_2$ | $s_1$ | $s_2$ | y |
|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 1 | 0 |

[그림 1: 논리 회로도] 입력선 x1, x2가 각각 갈라져 두 게이트에 모두 들어감. 위쪽 게이트는 OR → 출력 s2, 아래쪽 게이트는 NAND(출력단에 작은 원) → 출력 s1. s2와 s1이 오른쪽 AND 게이트로 들어가 최종 출력 Out이 됨. 즉 $s_1=\mathrm{NAND}(x_1,x_2)$, $s_2=\mathrm{OR}(x_1,x_2)$, $y=\mathrm{AND}(s_1,s_2)$.

[그림 2: 퍼셉트론(노드) 표현] 왼쪽 층 노드 x1, x2 → 가운데 층 노드 s1, s2 → 오른쪽 노드 y. 화살표: x1→s1, x1→s2, x2→s1, x2→s2 (교차), s1→y, s2→y. 입력층–은닉층(s1, s2)–출력층(y)으로 쌓은 2층 퍼셉트론이 XOR을 구현함을 보여 줌.

(※ 검증: Python으로 재계산 — 일치. NAND $(w_1,w_2,b)=(-0.5,-0.5,0.7)$, OR $(0.5,0.5,-0.2)$, AND $(0.5,0.5,-0.7)$ 계단함수 퍼셉트론으로 표의 $s_1, s_2, y$ 네 행 모두 재현, $y=x_1 \oplus x_2$. sklearn `MLPClassifier`(은닉 4, tanh)도 XOR 정확도 1.0)

---

<!-- p.17 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Perceptron to Artificial Neural Networks

[그림: 신경망 구조도] 왼쪽 빨간 원 3개(라벨 "Input") → 가운데 파란 원 4개(라벨 "Hidden") → 오른쪽 초록 원 2개(라벨 "Output"). 입력 3개 각각에서 은닉 4개 모두로, 은닉 4개 각각에서 출력 2개 모두로 화살표가 이어진 완전연결(fully connected) 구조.

- How are signals transmitted in a neural network?

$$y = h(b + w_1x_1 + w_2x_2 + \ldots)$$

$$h(x) = \begin{cases} 0 & (x \le 0) \\ 1 & (x > 0) \end{cases}$$

The total sum of input signals is transformed through a function $h(x)$, and the transformed value represents the output $y$.
(※ 검증: Python으로 재계산 — 일치. $h(-1)=0,\ h(0)=0,\ h(1)=1$)

---

<!-- p.18 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Activation Function

[그림: 활성화 함수가 포함된 뉴런 도식] 회색으로 칠한 노드 "1"(편향 입력)이 가중치 b로, 노드 x1이 가중치 w1로, 노드 x2가 가중치 w2로 하나의 큰 원 안의 작은 노드 a로 들어감. 큰 원 안에서 a → (h()) → y로 화살표가 이어짐. 즉 가중합 a를 활성화 함수 h()에 통과시켜 출력 y를 만드는 과정을 뉴런 하나 안에 명시적으로 그린 것.

- The activation function determines whether the total sum of input signals triggers activation.

$$a = b + w_1x_1 + w_2x_2$$

$$y = h(a)$$

---

<!-- p.19 -->

Types of Activation Functions
https://studymachinelearning.com/activation-functions-in-neural-network/
18/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[그림: 활성화 함수 3종 비교표 — 1행 이름, 2행 수식, 3행 그래프]

| | Sigmoid | Tanh | RELU |
|---|---|---|---|
| 수식 | $g(z) = \dfrac{1}{1+e^{-z}}$ | $g(z) = \dfrac{e^{z}-e^{-z}}{e^{z}+e^{-z}}$ | $g(z) = \max(0, z)$ |
| 그래프 | 파란 S자 곡선. 가로축 눈금 −4, 0, 4, 세로축 눈금 $\frac{1}{2}$, 1. $z=0$에서 $\frac{1}{2}$를 지나고, 왼쪽으로 갈수록 0, 오른쪽으로 갈수록 1에 가까워짐 | 청록색 S자 곡선. 가로축 눈금 −4, 0, 4, 세로축 눈금 −1, 1. 원점(0,0)을 지나고 −1과 1 사이 값 | 노란 꺾은선. 가로축 눈금 0, 1, 세로축 눈금 1. $z<0$에서 0(수평), $z\ge 0$에서 기울기 1인 직선 |

출처(그림 아래 링크): https://studymachinelearning.com/activation-functions-in-neural-network/
(※ 검증: Python으로 재계산 — 일치. sigmoid(−4, 0, 4) = 0.018, 0.5, 0.982; tanh(−4, 0, 4) = −0.9993, 0, 0.9993(수식과 np.tanh 동일); ReLU(−1, 0, 1) = 0, 0, 1)

---

<!-- p.20 -->

3-layer Perceptron
The input layer consists of 2 nodes, the first hidden layer has 3 nodes, the second hidden layer
has 2 nodes, and the output layer consists of 2 nodes.
19/25

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[그림: 3층 퍼셉트론 구조도] 왼쪽부터 입력층 노드 $x_1, x_2$ (2개) → 1번째 은닉층 빈 노드 3개 → 2번째 은닉층 빈 노드 2개 → 출력층 노드 $y_1, y_2$ (2개). 인접한 층의 모든 노드 쌍이 화살표로 연결된 완전연결 구조(2×3, 3×2, 2×2 연결). 가중치를 가진 층이 3개이므로 "3-layer"라고 부름.

---

<!-- p.21 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 3-layer Perceptron: Input Layer to First Hidden Layer

[그림: 3층 퍼셉트론에서 입력층 → 1번째 은닉층 신호 전달] 회색 편향 노드 "1", 입력 노드 $x_1$, $x_2$에서 1번째 은닉층 노드 $a^{(1)}_1, a^{(1)}_2, a^{(1)}_3$로 화살표가 이어짐(이후 은닉층 2개 노드 → $y_1$, $y_2$는 흐리게 표시). $a^{(1)}_1$로 들어가는 세 화살표만 굵게 강조되고 라벨이 붙음: 1 → $a^{(1)}_1$ 은 $b^{(1)}_1$, $x_1$ → $a^{(1)}_1$ 은 $w^{(1)}_{11}$, $x_2$ → $a^{(1)}_1$ 은 $w^{(1)}_{12}$.

$$a^{(1)}_1 = w^{(1)}_{11}x_1 + w^{(1)}_{12}x_2 + b^{(1)}_1$$
$$a^{(1)}_2 = w^{(1)}_{21}x_1 + w^{(1)}_{22}x_2 + b^{(1)}_2$$
$$a^{(1)}_3 = w^{(1)}_{31}x_1 + w^{(1)}_{32}x_2 + b^{(1)}_3$$

$$\mathbf{a}^{(1)} = \mathbf{x}\mathbf{W}^{(1)} + \mathbf{b}^{(1)}$$

$$\mathbf{X} = (x_1, x_2),$$
$$\mathbf{a}^{(1)} = (a^{(1)}_1, a^{(1)}_2, a^{(1)}_3), \quad \mathbf{b}^{(1)} = (b^{(1)}_1, b^{(1)}_2, b^{(1)}_3),$$

$$\mathbf{W}^{(1)} = \begin{pmatrix} w^{(1)}_{11} & w^{(1)}_{21} & w^{(1)}_{31} \\ w^{(1)}_{12} & w^{(1)}_{22} & w^{(1)}_{32} \end{pmatrix}$$

(※ 원문 표기 그대로 — 행렬식에서는 소문자 굵은 $\mathbf{x}$, 정의에서는 대문자 $\mathbf{X}$를 사용)
(※ 가중치 첨자 $w_{ji}$: 앞 첨자 j = 다음 층 노드 번호, 뒤 첨자 i = 앞 층 노드 번호. 따라서 $\mathbf{W}^{(1)}$은 2×3 행렬)
(※ 검증: Python으로 재계산 — 일치. 임의 값에서 $\mathbf{x}\mathbf{W}^{(1)}+\mathbf{b}^{(1)}$ 결과가 위 세 원소별 식과 같음)

---

<!-- p.22 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 3-layer Perceptron: Activation Function

[그림: 1번째 은닉층 활성화] 1번째 은닉층의 각 노드가 큰 원으로 묶이고, 원 안에서 $a^{(1)}_j$ → (h()) → $z^{(1)}_j$ ($j=1,2,3$)로 변환됨. 위쪽 경로(편향 1 → $a^{(1)}_1$ 의 $b^{(1)}_1$, $x_1$ → $a^{(1)}_1$ 의 $w^{(1)}_{11}$, $x_2$ → $a^{(1)}_1$ 의 $w^{(1)}_{12}$, 그리고 $a^{(1)}_1 \to z^{(1)}_1$)가 굵게 강조됨. 다음 층들에도 회색 편향 노드 "1"이 각각 추가되어 2번째 은닉층(노드 2개)과 출력 $y_1$, $y_2$로 연결됨.

$$\mathbf{z}^{(1)} = h(\mathbf{a}^{(1)})$$

$$h : \mathbb{R}^n \to \mathbb{R}^n$$

$$h(\mathbf{x}) = (h(x_1), h(x_2), \ldots, h(x_j), \ldots, h(x_n))$$
where $\quad \mathbf{x} = (x_1, x_2, \ldots, x_n) \in \mathbb{R}^n$

$$h(x_j) = \frac{1}{1 + e^{-x_j}}$$

(※ 은닉층 활성화 함수로 시그모이드를 원소별로 적용)

---

<!-- p.23 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 3-layer Perceptron: First Hidden Layer to Second Hidden Layer

[그림: 1번째 은닉층 → 2번째 은닉층 신호 전달] 1번째 은닉층 출력 $z^{(1)}_1, z^{(1)}_2, z^{(1)}_3$와 편향 노드 "1"에서 2번째 은닉층 노드 $a^{(2)}_1$로 가는 화살표가 굵게 강조됨: 1 → $a^{(2)}_1$ 은 $b^{(2)}_1$, $z^{(1)}_1$ → 는 $w^{(2)}_{11}$, $z^{(1)}_2$ → 는 $w^{(2)}_{12}$, $z^{(1)}_3$ → 는 $w^{(2)}_{13}$. 2번째 은닉층 각 노드 안에서 $a^{(2)}_1 \to$ (h()) $\to z^{(2)}_1$, $a^{(2)}_2 \to$ (h()) $\to z^{(2)}_2$. 입력층(1, $x_1$, $x_2$)과 출력층($y_1$, $y_2$, 편향 1)은 흐리게 표시.

$$\mathbf{a}^{(2)} = \mathbf{z}^{(1)}\mathbf{W}^{(2)} + \mathbf{b}^{(2)}$$

$$\mathbf{z}^{(1)} = (z^{(1)}_1, z^{(1)}_2, z^{(1)}_3), \quad \mathbf{W}^{(2)} = \begin{pmatrix} w^{(2)}_{11} & w^{(2)}_{21} \\ w^{(2)}_{12} & w^{(2)}_{22} \\ w^{(2)}_{13} & w^{(2)}_{23} \end{pmatrix},$$

$$\mathbf{b}^{(2)} = (b^{(2)}_1, b^{(2)}_2), \quad \mathbf{a}^{(2)} = (a^{(2)}_1, a^{(2)}_2)$$

(※ $\mathbf{W}^{(2)}$는 3×2 행렬 → (1×3)(3×2) = 1×2, 차원 일치)

---

<!-- p.24 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 3-layer Perceptron: Second Hidden Layer to Output Layer

[그림: 2번째 은닉층 → 출력층 신호 전달] 편향 노드 "1"과 2번째 은닉층 출력 $z^{(2)}_1$, $z^{(2)}_2$에서 출력 노드 $a^{(3)}_1$로 가는 화살표가 굵게 강조됨: 1 → 는 $b^{(3)}_1$, $z^{(2)}_1$ → 는 $w^{(3)}_{11}$, $z^{(2)}_2$ → 는 $w^{(3)}_{12}$. 출력 노드 안에서 $a^{(3)}_1 \to$ (σ()) $\to y_1$, $a^{(3)}_2 \to$ (σ()) $\to y_2$. 앞쪽 층은 흐리게 표시. 출력층 활성화 함수는 h가 아닌 σ로 표기.

- For regression,
  - Identity function
$$\sigma(x) = x$$
- For classification,
  - Softmax function
$$\sigma : \mathbb{R}^n \to \mathbb{R}^n$$
$$\sigma(\mathbf{x}) = (\sigma(x_1), \sigma(x_2), \ldots, \sigma(x_j), \ldots, \sigma(x_n))$$
$$\sigma(x_j) = \frac{e^{x_j}}{\sum_{i=1}^{n} e^{x_i}}$$

---

<!-- p.25 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Softmax Function

$$\text{Output layer: } \begin{bmatrix} 1.3 \\ 5.1 \\ 2.2 \\ 0.7 \\ 1.1 \end{bmatrix} \xrightarrow{\ \text{Softmax activation } \sigma(x_j)=\frac{e^{x_j}}{\sum_{i=1}^{n} e^{x_i}}\ } \text{Probabilities: } \begin{bmatrix} 0.02 \\ 0.90 \\ 0.05 \\ 0.01 \\ 0.02 \end{bmatrix}$$

(출력층 값 5개를 소프트맥스에 통과시키면 합이 1인 확률 벡터가 되고, 가장 큰 입력 5.1이 가장 큰 확률 0.90을 가짐)
(※ 검증: Python으로 재계산 — 일치. softmax = (0.0202, 0.9025, 0.0497, 0.0111, 0.0165), 소수 둘째 자리 반올림 시 (0.02, 0.90, 0.05, 0.01, 0.02), 합 1)

---

<!-- p.26 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Batch Processing

- We estimated the output for a single sample at a time.
  - Each multiplication is dimensionally consistent (matrix dimensions match).

$$\mathbf{x}\ (2) \quad \mathbf{W_1}\ (2 \times 3) \quad \mathbf{W_2}\ (3 \times 2) \quad \mathbf{W_3}\ (2 \times 2) \quad \to \mathbf{Y}\ (2)$$

- If we process 100 images simultaneously, the output will have a shape of $100 \times 2$.

$$\mathbf{X}\ (100 \times 2) \quad \mathbf{W_1}\ (2 \times 3) \quad \mathbf{W_2}\ (3 \times 2) \quad \mathbf{W_3}\ (2 \times 2) \quad \to \mathbf{Y}\ (100 \times 2)$$

→ This way of processing multiple data samples at once is called **batch processing**.
(※ 검증: Python으로 재계산 — 일치. numpy로 시그모이드–시그모이드–소프트맥스 순전파 시 단일 입력 (2,) → (3,) → (2,) → (2,), 배치 입력 (100, 2) → 출력 (100, 2))

---

<!-- p.27 -->

Thank You!
(Q & A)

---

<!-- p.28 -->

References
사이토 고키 (2025), 밑바닥부터 시작하는 딥러닝 1(리마스터판), 한빛미디어
