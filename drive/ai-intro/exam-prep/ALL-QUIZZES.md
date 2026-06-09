# 연습문제 통합 (1~14주차)


# ========= 01주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 1주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">

  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>1주차 문제집</h1>
    <div class="subtitle">인공지능이 인문학</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">각 문항 옆 [정답 보기] 버튼으로 개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <!-- ============ 객관식 ============ -->
  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">Cambridge 사전이 정의한 지능(Intelligence)의 4요소가 <strong>아닌</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> Learn (배움)</li>
      <li><span class="opt-num">②</span> Understand (이해)</li>
      <li><span class="opt-num">③</span> Memorize (암기)</li>
      <li><span class="opt-num">④</span> Make judgments based on reason (합리적 판단)</li>
      <li><span class="opt-num">⑤</span> Have opinions based on reason (자신의 의견)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>③ Memorize (암기)</strong><br>
      <span class="alabel">해설</span>
      Cambridge 사전 정의는 <span class="keyw">"The ability to learn, understand, and make judgments or have opinions that are based on reason."</span>
      따라서 <span class="keyw">Learn / Understand / Make judgments / Have opinions</span>의 4가지가 핵심이며, 마지막 두 가지는 <span class="keyw">based on reason(합리적 추론에 기반)</span>이라는 단서가 붙는다. 단순 암기는 지능의 정의에 포함되지 않는다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">"AI가 인간을 멸종시킬지 모른다"라는 문장에서 사용된 <strong>인공지능</strong>의 의미로 가장 적절한 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 학문 분야로서의 인공지능</li>
      <li><span class="opt-num">②</span> 기술로서의 인공지능</li>
      <li><span class="opt-num">③</span> 시스템(결과물)으로서의 인공지능</li>
      <li><span class="opt-num">④</span> 알고리즘으로서의 인공지능</li>
      <li><span class="opt-num">⑤</span> 데이터로서의 인공지능</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>③ 시스템(결과물)으로서의 인공지능</strong><br>
      <span class="alabel">해설</span>
      인공지능은 맥락에 따라 <span class="keyw">① 학문 / ② 기술 / ③ 시스템</span> 세 가지 의미로 쓰인다.
      "인간을 멸종시킬지 모른다"고 할 때 인공지능은 학문도 기술도 아닌, 그 기술이 적용된 <span class="keyw">결과물(시스템)</span>이 자율적으로 행동할 가능성을 의미한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">"세상의 딱딱함과 부드러움" 비교에서 <strong>잘못 짝지어진</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 딱딱함 — How many / 부드러움 — How much</li>
      <li><span class="opt-num">②</span> 딱딱함 — 이산적(Discrete) / 부드러움 — 연속적(Continuous)</li>
      <li><span class="opt-num">③</span> 딱딱함 — 산술 / 부드러움 — 기하학</li>
      <li><span class="opt-num">④</span> 딱딱함 — 우뇌 / 부드러움 — 좌뇌</li>
      <li><span class="opt-num">⑤</span> 딱딱함 — 디지털 / 부드러움 — 아날로그</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>④ 딱딱함 — 우뇌 / 부드러움 — 좌뇌</strong> (잘못된 짝)<br>
      <span class="alabel">해설</span>
      좌뇌 ↔ 우뇌가 반대로 되어 있다. 올바른 매핑은 <span class="keyw">딱딱함 = 좌뇌 (논리·수)</span>, <span class="keyw">부드러움 = 우뇌 (공간·이미지)</span>이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">톰 미첼(Tom Mitchell)의 학습 정의에서 <strong>E·T·P</strong>의 의미로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> E = Evaluation, T = Time, P = Process</li>
      <li><span class="opt-num">②</span> E = Experience, T = Task, P = Performance</li>
      <li><span class="opt-num">③</span> E = Event, T = Train, P = Predict</li>
      <li><span class="opt-num">④</span> E = Error, T = Target, P = Probability</li>
      <li><span class="opt-num">⑤</span> E = Expert, T = Theory, P = Program</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>② E = Experience, T = Task, P = Performance</strong><br>
      <span class="alabel">해설</span>
      "어떤 작업 <span class="keyw">T(Task)</span>에 대해 성능 측정 <span class="keyw">P(Performance)</span>가 경험 <span class="keyw">E(Experience)</span>에 의해 개선되면 그 프로그램은 학습한 것이다." 가장 빈출되는 정의이므로 정확히 외울 것.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">허먼(Herrmann)의 두뇌우성 모델에서 <strong>D 영역(우상)</strong>의 특징으로 가장 적절한 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 논리·계산·분석</li>
      <li><span class="opt-num">②</span> 계획·조직·통제·규칙</li>
      <li><span class="opt-num">③</span> 음악·감정·관계</li>
      <li><span class="opt-num">④</span> 시각·창의·도전·리스크</li>
      <li><span class="opt-num">⑤</span> 본능적 반응</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>④ 시각·창의·도전·리스크</strong><br>
      <span class="alabel">해설</span>
      허먼 4영역(반시계 방향): <span class="keyw">A(좌상)=논리</span>, <span class="keyw">B(좌하)=계획</span>, <span class="keyw">C(우하)=감정/관계</span>, <span class="keyw">D(우상)=시각/창의</span>. ①은 A, ②는 B, ③은 C에 해당한다.
    </div>
  </div>

  <!-- ============ 주관식 ============ -->
  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">인공지능을 한마디로 정의하면 무엇인가? (한국어로)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>"만든 지능"</strong> (사람이 만든 지능)<br>
      <span class="alabel">해설</span>
      "인공"(Artificial) = 사람이 만든 것 + "지능"(Intelligence) = 배우고 판단하는 능력. 둘을 합치면 <span class="keyw">"만든 지능"</span>.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">"Artificial(인공)"의 사전적 정의 두 가지 핵심 요소를 한국어로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>사람이 만든 것</strong> (Made by people)<br>
      ② <strong>자연에 있는 것을 모방한 것</strong> (Copy of something natural)<br>
      <span class="alabel">해설</span>
      두 번째 조건이 핵심이다. 자연을 모방했기 때문에 <span class="keyw">자연에 있는 인간의 지능을 모방한 것</span>이 인공지능이며, 이것이 "AI = 인문학"의 출발점이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">지능 컴퓨터 시스템이 가져야 할 4가지 능력을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>언어 이해</strong>(Understanding language)<br>
      ② <strong>그림(상황) 인식</strong>(Recognize picture)<br>
      ③ <strong>문제 해결</strong>(Solve problems)<br>
      ④ <strong>학습</strong>(Learn)<br>
      <span class="alabel">해설</span>
      강의 2차시 퀴즈에 그대로 등장한 빈출 항목.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">"내 전공은 인공지능이다 / 감마Go라는 인공지능 프로그램 / 인공지능이 여기 두는 게 좋다고 한다." 각 문장에서 인공지능의 의미를 순서대로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>학문 분야</strong> (Study)<br>
      ② <strong>기술</strong> (Computer technology)<br>
      ③ <strong>시스템</strong> (결과물 — 그 기술이 적용된 프로그램 자체)<br>
      <span class="alabel">해설</span>
      한 문장 안에 같은 단어가 세 번 나오면서 매번 다른 의미로 쓰이는 빈출 예시.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">톰 미첼의 학습 정의에서 E·T·P가 각각 무엇의 약자인지 영어로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>E = Experience / T = Task / P = Performance</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">세상의 "딱딱함(Hard)"에 해당하는 키워드 5가지 이상을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답 (택 5)</span>
      <strong>How many</strong>, <strong>수(Number)</strong>, <strong>디지털(Digital)</strong>, <strong>이산적(Discrete)</strong>, <strong>분리</strong>, <strong>산술(Arithmetic)</strong>, <strong>여러 개(독립)</strong>, <strong>좌뇌</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">사람의 뇌를 진화 순서에 따라 안쪽부터 3층으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>파충류의 뇌</strong> (Reptilian Brain) — 본능<br>
      ② <strong>포유류의 뇌 / 변연계</strong> (Limbic System) — 감정의 뇌<br>
      ③ <strong>사람의 뇌 / 신피질</strong> (Neocortex) — 이성의 뇌
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">허먼의 두뇌우성 모델 4영역(A·B·C·D) 위치와 핵심 키워드를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>A (좌상)</strong> — 논리·계산·분석 (분석적)<br>
      <strong>B (좌하)</strong> — 계획·조직·통제·규칙 (관리적)<br>
      <strong>C (우하)</strong> — 음악·감정·관계·사람 (대인적)<br>
      <strong>D (우상)</strong> — 시각·창의·도전·리스크 (상상적)<br>
      <span class="alabel">해설</span>
      <span class="keyw">반시계 방향</span>(좌상→좌하→우하→우상)으로 A·B·C·D.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">강의에서 "지능에서 가장 강조되는 능력"으로 꼽은 것은 무엇인가?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>학습 (Learn) — 배우는 능력</strong><br>
      <span class="alabel">해설</span>
      강아지 용호가 돌의 적당한 크기를 학습한 사례, 톰 미첼의 학습 정의 등 강의 전체가 학습 능력을 핵심으로 강조한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">강태원 교수가 정의한 "사람이 배운다는 것"의 의미를 한 단어로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>"달라지는 것"</strong><br>
      <span class="alabel">해설</span>
      "내가 4년 다닌 후에도 입학 때와 지적으로 달라지지 않으면 배운 게 없는 것이다." — 톰 미첼의 컴퓨터 학습 정의(경험으로 성능이 달라짐)와 같은 본질을 가리킨다.
    </div>
  </div>

  <!-- ============ 서술형 ============ -->
  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">"인공지능"이 학문 / 기술 / 시스템 세 가지 의미로 쓰이는 점을, 직접 만든 한 문장 예시(인공지능이 3번 등장)를 들어 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      예시 문장: "<em>나는 대학에서 <strong>인공지능</strong>을 전공하면서 최근 추천 알고리즘에 <strong>인공지능</strong> 기술을 적용한 프로그램을 만들었는데, 그 <strong>인공지능</strong>이 내가 좋아할 법한 영화를 정확히 골라 추천했다.</em>"<br><br>
      <strong>분석</strong> — 첫 번째는 ① <span class="keyw">학문 분야</span>(전공), 두 번째는 ② <span class="keyw">기술</span>(프로그램에 적용된 컴퓨터 기술), 세 번째는 ③ <span class="keyw">시스템</span>(그 기술이 만든 결과물 — 추천 프로그램 자체)을 의미한다. 이렇게 같은 단어가 맥락에 따라 다른 의미를 갖는다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">톰 미첼(Tom Mitchell)의 학습 정의를 영어 원문으로 쓰고, 한국어로 풀어 쓴 뒤, 게임 프로그램을 예로 E·T·P를 각각 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>영어 원문</strong>: <em>"A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks in T, as measured by P, improves with experience E."</em><br><br>
      <strong>한국어 풀이</strong>: 어떤 작업 <span class="keyw">T</span>의 성능을 측정 기준 <span class="keyw">P</span>로 평가할 때, 경험 <span class="keyw">E</span>가 쌓일수록 P가 개선되면 그 프로그램은 학습 능력을 가진 것이다.<br><br>
      <strong>게임 프로그램의 예</strong>:
      <ul>
        <li><strong>E (경험)</strong> = 사용자와의 게임 기록·대국 결과</li>
        <li><strong>T (작업)</strong> = 게임에서 승리하기</li>
        <li><strong>P (성능)</strong> = 승률 또는 점수</li>
      </ul>
      처음 샀을 때보다 일주일 사용 후 게임 프로그램의 승률이 높아졌고, 그 변화가 사전에 코딩된 if-else가 아니라 사용자와의 상호작용으로 발생했다면, 이 프로그램은 학습 능력을 가진 것이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">"세상의 딱딱함과 부드러움"이라는 비유를 사용해, 사람의 뇌가 좌·우뇌로 기능을 나누어 진화한 이유를 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      자연 세계는 <span class="keyw">셀 수 있는 것(딱딱함, 이산적, How many)</span>과 <span class="keyw">셀 수 없는 것(부드러움, 연속적, How much)</span>이 공존한다. 두 속성은 성격이 매우 달라서 하나의 처리 방식으로 모두 다루는 것은 비효율적이다. 따라서 "딱딱한 것은 너가, 부드러운 것은 내가"처럼 <span class="keyw">기능을 나누어 처리</span>하는 것이 가장 효율적이다.<br><br>
      이러한 진화의 결과 사람의 뇌는 <span class="keyw">좌뇌(딱딱함 — 논리·수)</span>와 <span class="keyw">우뇌(부드러움 — 공간·이미지)</span>로 기능이 분화되었으며, 이렇게 함으로써 자연에서 살아남는 데 더 효율적인 처리(에너지 절약, 생산성 증가)를 할 수 있게 되었다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">강태원 교수가 "인공지능이 인문학(Humanities)이다"라고 주장하는 두 가지 이유를, 과거와 오늘날의 인공지능 정의 변화와 함께 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>이유 ①</strong>: 인공(Artificial)이라는 단어 자체가 <span class="keyw">자연에 있는 것을 모방하여 사람이 만드는 것</span>이라는 뜻이다. 따라서 인공지능은 자연에 있는 <span class="keyw">인간의 지능을 모방</span>하는 학문이며, 인간을 모르고는 인간 같은 것을 만들 수 없다. 그래서 인간(인문학적) 이해가 필수다.<br><br>
      <strong>이유 ②</strong>: 시대별 정의가 바뀌었다.
      <ul>
        <li><strong>과거</strong>: "사람이 더 잘하던 일을 컴퓨터도 잘할 수 있게 하는 분야" — 좌뇌 영역(논리·계산)이 주된 대상이었다.</li>
        <li><strong>오늘</strong>: 생성 AI(Generative AI)가 등장하면서 음악·그림·감정 같은 <span class="keyw">우뇌 영역(인간만의 영역)</span>까지 컴퓨터가 다루게 되었다. 이런 시대에는 사람의 감정·관계·예술에 대한 이해, 곧 <span class="keyw">인문학적 통찰</span>이 더욱 중요해진다.</li>
      </ul>
      따라서 인공지능 연구에는 공학적 지식뿐 아니라 인문학적 지식이 필수적이며, 이런 의미에서 "인공지능이 인문학"이다. 노벨상 수상자 힌튼(Geoffrey Hinton)이 AI를 우려하는 이유도 같은 맥락 — 인간을 잘 이해해야 안전한 AI를 만들 수 있기 때문이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">허먼(Herrmann)의 두뇌우성 모델 4영역을 두 축(좌·우 / 위·아래)을 기준으로 설명하고, 각 영역의 키워드를 제시하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      허먼 모델은 두 개의 축으로 뇌를 4영역으로 나눈다.
      <ul>
        <li><strong>좌·우 축</strong>: 좌뇌 = <span class="keyw">딱딱함</span>(논리·수), 우뇌 = <span class="keyw">부드러움</span>(공간·이미지)</li>
        <li><strong>위·아래 축</strong>: 위 = <span class="keyw">신피질(이성)</span>, 아래 = <span class="keyw">변연계(감정)</span></li>
      </ul>
      <strong>4영역</strong>(반시계 방향):
      <ul>
        <li><strong>A (좌상, 딱딱함+이성)</strong> — 논리·계산·분석·기술 (분석적, Analytical)</li>
        <li><strong>B (좌하, 딱딱함+감정)</strong> — 계획·조직·통제·규칙·절차 (관리적, Sequential)</li>
        <li><strong>C (우하, 부드러움+감정)</strong> — 음악·감정·관계·사람 (대인적, Interpersonal)</li>
        <li><strong>D (우상, 부드러움+이성)</strong> — 시각·창의·도전·리스크 (상상적, Imaginative)</li>
      </ul>
      또한 한 영역만 발달한 것보다 <span class="keyw">4영역의 균형 발달</span>이 중요하며, 한쪽 영역이 손상되어도 다른 영역이 그 기능을 나누어 맡는 <span class="keyw">뇌의 가소성(Plasticity)</span>이 있어 영역 분리는 고정·불변이 아니다.
    </div>
  </div>

  <div class="nav-links">
    <a href="01주차_교과서.html">📚 교과서</a>
    <a href="01주차_학습서.html">📖 학습서</a>
  </div>

</div>

<script>
  function toggleAns(btn) {
    const box = btn.nextElementSibling;
    box.classList.toggle('show');
    btn.textContent = box.classList.contains('show') ? '정답 가리기' : '정답 보기';
  }
  function showAll() {
    document.querySelectorAll('.answer-box').forEach(b => b.classList.add('show'));
    document.querySelectorAll('.toggle-btn').forEach(b => b.textContent = '정답 가리기');
  }
  function hideAll() {
    document.querySelectorAll('.answer-box').forEach(b => b.classList.remove('show'));
    document.querySelectorAll('.toggle-btn').forEach(b => b.textContent = '정답 보기');
  }
</script>
</body>
</html>


# ========= 02주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 2주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>2주차 문제집</h1>
    <div class="subtitle">내 이상형은 기계</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">튜링 테스트(Turing Test)에 대한 설명으로 <strong>옳지 않은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 1950년 앨런 튜링이 논문에서 제안한 평가 기준이다.</li>
      <li><span class="opt-num">②</span> 이미테이션 게임(Imitation Game)이라고도 불린다.</li>
      <li><span class="opt-num">③</span> 판정관이 누가 사람이고 누가 기계인지 구분하지 못하면 그 기계는 지능이 있다고 본다.</li>
      <li><span class="opt-num">④</span> 튜링 테스트가 제안된 시점은 "Artificial Intelligence" 용어 탄생 이후이다.</li>
      <li><span class="opt-num">⑤</span> 영화 "엑스 마키나(Ex Machina)"는 사실상 튜링 테스트를 영화화한 작품이다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ 튜링 테스트가 제안된 시점은 "AI" 용어 탄생 이후이다.</strong> (틀림)<br>
      <span class="alabel">해설</span>
      튜링 테스트는 <span class="keyw">1950년</span>에 제안되었고, "Artificial Intelligence" 용어는 <span class="keyw">1956년 다트머스 회의</span>에서 탄생했다. 따라서 튜링 테스트가 <strong>먼저</strong>이며 당시에는 "Thinking Machine(생각하는 기계)"이라는 용어를 썼다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">중국어 방(Chinese Room) 사고실험을 제안한 사람과 연도는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 앨런 튜링(Alan Turing), 1950</li>
      <li><span class="opt-num">②</span> 존 메카시(John McCarthy), 1956</li>
      <li><span class="opt-num">③</span> 존 썰(John Searle), 1980</li>
      <li><span class="opt-num">④</span> 제프리 힌튼(Geoffrey Hinton), 2010</li>
      <li><span class="opt-num">⑤</span> 데미스 하사비스(Demis Hassabis), 2016</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 존 썰(John Searle), 1980</strong><br>
      <span class="alabel">해설</span>
      미국의 철학자 <span class="keyw">존 썰</span>이 <span class="keyw">1980년</span>에 발표한 사고실험. 튜링 테스트(1950) 후 30여 년 만의 대표적 반론이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">"인공지능(Artificial Intelligence)"이라는 용어가 공식 등장한 사건은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 1943년 맥컬럭과 피츠의 신경망 모델 발표</li>
      <li><span class="opt-num">②</span> 1950년 튜링 테스트 논문 발표</li>
      <li><span class="opt-num">③</span> 1956년 다트머스 회의(Dartmouth Conference)</li>
      <li><span class="opt-num">④</span> 1980년 존 썰의 중국어 방 발표</li>
      <li><span class="opt-num">⑤</span> 2016년 알파고와 이세돌의 대국</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 1956년 다트머스 회의</strong><br>
      <span class="alabel">해설</span>
      메카시(McCarthy)·민스키(Minsky)·새뮤얼(Samuel) 등이 모인 한 달짜리 컨퍼런스에서 <span class="keyw">"이 분야를 Artificial Intelligence로 부르자"</span>고 합의한 것이 AI 용어의 공식 출발점이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">알파고(AlphaGo)의 기술적 정체에 대한 설명으로 <strong>가장 옳은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 순수한 딥러닝 시스템이다.</li>
      <li><span class="opt-num">②</span> MCTS(몬테카를로 트리 탐색)를 골격으로 하고, CNN과 강화학습을 결합한 시스템이다.</li>
      <li><span class="opt-num">③</span> 전문가 시스템(Expert System)의 일종이다.</li>
      <li><span class="opt-num">④</span> 단순히 바둑 기보를 데이터베이스에서 검색하는 시스템이다.</li>
      <li><span class="opt-num">⑤</span> 기호주의 AI의 대표적 성공 사례이다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② MCTS + CNN + 강화학습의 조합</strong><br>
      <span class="alabel">해설</span>
      알파고는 흔히 딥러닝으로 알려져 있지만 실은 <span class="keyw">탐색 시스템(MCTS, Monte Carlo Tree Search)</span>을 핵심으로 하고, 거기에 <span class="keyw">CNN(합성곱 신경망)</span>과 <span class="keyw">강화학습(Reinforcement Learning)</span>을 결합한 것이다. 다음 주(3주차)의 탐색 주제와 직접 연결.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">기호주의(Symbolism)와 연결주의(Connectionism)의 짝으로 <strong>옳지 않은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 기호주의 — 논리(Logic)와 기호(Symbol) 처리</li>
      <li><span class="opt-num">②</span> 연결주의 — 신경망(Neural Network)</li>
      <li><span class="opt-num">③</span> 기호주의 — 메카시·민스키·새뮤얼이 대표</li>
      <li><span class="opt-num">④</span> 연결주의 — 힌튼·르쿤·벤지오가 대표</li>
      <li><span class="opt-num">⑤</span> 기호주의 — Keras 패키지의 이론적 기반</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>⑤ 기호주의 — Keras 패키지의 이론적 기반</strong> (틀림)<br>
      <span class="alabel">해설</span>
      <span class="keyw">Keras</span>는 <span class="keyw">딥러닝</span> 패키지로 <strong>연결주의</strong>의 도구이다. 기호주의 계열의 대표 패키지는 <span class="keyw">scikit-learn</span>(좁은 의미의 머신러닝).
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">튜링 테스트의 다른 이름 두 가지를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>이미테이션 게임(Imitation Game)</strong>, <strong>모방 게임</strong><br>
      <span class="alabel">해설</span> 셋(튜링 테스트 / 이미테이션 게임 / 모방 게임)은 모두 같은 말이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">중국어 방 사고실험의 결론(존 썰의 주장)을 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      "<strong>튜링 테스트를 통과했다고 해도 그 기계가 진짜로 '이해'(=지능)를 가졌다고 볼 수는 없다.</strong>"<br>
      <span class="alabel">해설</span> 방 안의 사람·매뉴얼·카드 어느 것도 중국어를 모르듯이, 튜링 테스트를 통과한 시스템도 단지 매칭 규칙을 적용한 것뿐이라는 주장.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">중국어 방에 대한 재반론인 "시스템 응답(System Response)"의 핵심 주장을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      "방 안의 어떤 부품도 중국어를 모르지만, <strong>그것들을 합친 시스템 전체</strong>는 중국어를 이해한 것이다. 바깥 사람은 사람이 아니라 시스템과 대화한 것이다."<br>
      <span class="alabel">해설</span> 인간의 두뇌도 마찬가지로, 어느 한 부위가 아니라 전체 시스템이 언어를 이해하는 것이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">2016년 알파고에 패한 이세돌 9단이 한 명언을 쓰고, 그 발언이 어떤 사고실험과 같은 구조인지 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      명언: <strong>"내가 진 거지 인간이 진 게 아니다. 알파고는 바둑의 아름다움을 모른다."</strong><br>
      대응 사고실험: <strong>중국어 방(Chinese Room)</strong> — 잘 둔다고 해서 본질을 이해하는 것은 아니라는 같은 구조.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">"Artificial Intelligence" 용어가 등장한 연도와 사건명을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>1956년, 다트머스 회의(Dartmouth Conference)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">최초의 신경망 모델을 제안한 두 학자와 연도를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>맥컬럭(McCulloch)과 피츠(Pitts), 1943년</strong><br>
      <span class="alabel">해설</span> 딥러닝의 진짜 뿌리는 매우 오래되었다는 점이 강의의 강조 사항.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">기호주의와 연결주의 각각의 대표 패키지(소프트웨어 라이브러리)를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      기호주의 — <strong>scikit-learn</strong> (좁은 의미의 머신러닝)<br>
      연결주의 — <strong>Keras</strong> (딥러닝)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">2010년대 AI가 폭발적으로 발달한 두 가지 동력을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>하드웨어 발달</strong> (연산 속도 폭증, GPU 등)<br>
      ② <strong>데이터 폭발</strong> (인터넷·월드와이드 웹으로 대규모 데이터 확보)<br>
      <span class="alabel">해설</span> 알고리즘은 1940~1990년대에 이미 다 등장했고, 하드웨어와 데이터가 합쳐지면서 폭발했다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">인공지능을 수준별로 구분하는 약어 ANI / AGI / ASI의 의미를 각각 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>ANI</strong> = Artificial Narrow Intelligence (약 인공지능, 특정 분야만)<br>
      <strong>AGI</strong> = Artificial General Intelligence (일반 인공지능, 인간 수준 범용)<br>
      <strong>ASI</strong> = Artificial Super Intelligence (초 인공지능, 인간 초월)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">알파고를 구성하는 세 가지 핵심 기술을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>MCTS</strong> (Monte Carlo Tree Search, 몬테카를로 트리 탐색) — 골격<br>
      ② <strong>CNN</strong> (Convolutional Neural Network, 합성곱 신경망)<br>
      ③ <strong>강화학습</strong> (Reinforcement Learning)
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">튜링 테스트의 정의·구성 요소·판정 기준을 EBS "AI 소개팅" 사례에 적용하여 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>정의</strong>: 튜링 테스트는 1950년 앨런 튜링이 제안한 평가 기준으로, 칸막이를 사이에 두고 ① 사람과 ② 기계가 텔레타이프로 대화할 때 <span class="keyw">판정관(Interrogator)</span>이 둘을 구분하지 못하면 그 기계는 지능을 가진 것으로 인정한다는 것이다.<br><br>
      <strong>EBS 소개팅 사례 적용</strong>:
      <ul>
        <li><strong>판정관</strong> = 여성 출연자 (얼굴을 볼 수 없고 채팅으로만 대화)</li>
        <li><strong>참가자 A·B·D</strong> = 사람 (1·2·4번 남성 출연자)</li>
        <li><strong>참가자 C</strong> = 기계 (3번 — AI 챗봇)</li>
        <li><strong>대화 매체</strong> = 채팅 (튜링 테스트의 텔레타이프와 동일)</li>
        <li><strong>결과</strong> = AI가 4표로 1등 → 판정관들이 AI를 사람과 구분하지 못했을 뿐 아니라 <span class="keyw">이상형으로까지 선택</span>했다.</li>
      </ul>
      이는 <strong>튜링 테스트의 통과 사례</strong>로 볼 수 있으며, 동시에 그것이 진짜 "지능"인지에 대한 후속 논쟁(중국어 방)의 출발점이 된다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">중국어 방(Chinese Room) 사고실험을 설명하고, 이에 대한 시스템 응답(System Response)이 어떤 점을 지적하는지 비교하여 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>중국어 방 (1980, 존 썰)</strong>: 중국어를 전혀 모르는 서양인이 방 안에 ① 한자 카드 ② 영어로 된 매뉴얼을 가지고 있다. 바깥 중국인이 한자 질문을 문틈으로 넣으면, 안의 사람은 매뉴얼대로 한자 카드를 찾아 답을 내보낸다. 바깥 사람은 정상 대화를 했다고 느끼지만, 방 안 사람은 중국어를 전혀 모른다. 따라서 <span class="keyw">튜링 테스트를 통과한 기계도 진짜 "이해"를 가진 게 아니다</span>라는 것이 썰의 결론.<br><br>
      <strong>시스템 응답 (재반론)</strong>: 방 안의 사람·매뉴얼·카드 어느 한 부품도 중국어를 모르지만, <span class="keyw">그것들을 합친 시스템 전체</span>는 중국어를 이해한 것이다. 바깥의 중국인은 사람과 대화한 게 아니라 <span class="keyw">중국어 방이라는 시스템</span>과 대화한 것이며, 그 시스템은 완벽히 중국어로 대화를 했으므로 시스템 자체는 중국어를 이해한다고 보아야 한다. 인간의 뇌도 한 부위에 언어가 들어 있는 게 아니라 시스템 전체로 작용하는 것과 같다.<br><br>
      <strong>비교</strong>: 썰은 <span class="keyw">개별 부품의 무지</span>에 초점을 맞춰 "이해 없음"을 주장했지만, 시스템 응답은 <span class="keyw">시스템 전체의 행동</span>에 초점을 맞춰 "이해 있음"을 주장한다. 강의는 정답이 정해져 있지 않다고 결론 내린다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">기호주의(Symbolism)와 연결주의(Connectionism)의 차이점을 설명하고, 두 흐름이 통합적으로 사용되어야 하는 이유를 비유를 들어 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>기호주의(Symbolism)</strong>는 인간을 "기호 처리 장치"로 보고, <span class="keyw">논리(Logic)와 기호(Symbol)</span>를 사용하여 P→Q와 같은 명시적 규칙으로 지능을 구현하려는 접근이다. 메카시·민스키·새뮤얼이 대표 인물이며, scikit-learn 같은 좁은 의미의 머신러닝 패키지가 이 흐름의 도구를 모아 놓은 것이다. 1980년대까지 주류였다.<br><br>
      <strong>연결주의(Connectionism)</strong>는 뇌를 "신호의 연결망"으로 보고, <span class="keyw">신경망(Neural Network)</span>으로 입력→계산→출력의 흐름을 통해 지능을 구현하려는 접근이다. 1943년 맥컬럭과 피츠가 시작했고 힌튼·르쿤·벤지오가 현대의 대표 인물이다. Keras 같은 딥러닝 패키지가 이 흐름의 도구다. 2010년대 이후 폭발적으로 발달했다.<br><br>
      <strong>비유</strong>: 강의는 두 흐름을 <span class="keyw">"망치와 톱"</span>에 비유한다. 집을 지을 때 망치만으로 못을 박고 톱으로 자를 수는 있지만, 톱으로 못을 박을 수는 없고 망치로 나무를 자를 수도 없다. 마찬가지로 인공지능을 만들 때도 <span class="keyw">두 도구가 모두 필요</span>하다. 2010년대 이후 연결주의(딥러닝)가 크게 부각되었지만, 둘 중 하나가 옳고 그르다는 것이 아니라 상호보완적으로 사용해야 제대로 된 AI를 만들 수 있다는 것이 강의의 결론이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">알파고가 "딥러닝 시스템"으로만 알려져 있는 것이 왜 부정확한지 설명하시오. 알파고의 실제 구성 요소와 다음 모델(알파고 제로, 알파제로)과의 차이도 함께 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      알파고가 흔히 "딥러닝 시스템"으로 알려져 있지만, 사실 알파고의 핵심 골격은 <span class="keyw">탐색 시스템(Search System)</span>이다. 인공지능에서 가장 오래된 분야 중 하나인 탐색의 한 종류인 <span class="keyw">MCTS(Monte Carlo Tree Search, 몬테카를로 트리 탐색)</span>가 1993년에 제안되어 발전해 오던 것이며, 알파고는 그 위에 두 가지 기술을 결합한 것이다.<br><br>
      <strong>알파고의 실제 구성</strong>:
      <ul>
        <li>① <span class="keyw">MCTS</span> — 가능한 다음 수를 트리 형태로 탐색</li>
        <li>② <span class="keyw">CNN(Convolutional Neural Network, 합성곱 신경망, 1989)</span> — 바둑판 상태의 가치를 평가</li>
        <li>③ <span class="keyw">강화학습(Reinforcement Learning)</span> — 자가 대국으로 성능 향상</li>
      </ul>
      따라서 딥러닝(CNN)은 알파고를 구성하는 <strong>한 부품</strong>일 뿐, 알파고 = 딥러닝이라고 말하는 것은 부정확하다.<br><br>
      <strong>다음 모델 차이</strong>:
      <ul>
        <li><strong>AlphaGo</strong> (2016): 프로 기사 기보 학습 + 자가 대국. 이세돌에 4승1패.</li>
        <li><strong>AlphaGo Zero</strong>: "Zero"는 <span class="keyw">기보 학습이 0(없음)</span>이라는 뜻. 바둑 규칙만 알려주고 자가 학습으로만 도달. 알파고를 100:0으로 격파.</li>
        <li><strong>AlphaZero</strong>: "Go"가 빠짐 = <span class="keyw">바둑에 한정되지 않는 일반 게임 AI</span>. 체스·쇼기에도 적용.</li>
      </ul>
      이후 AlphaFold(단백질 구조, 2024 노벨 화학상)·AlphaCode(코드 생성)로 확장되었다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">인공지능에 대한 철학적 논쟁의 흐름을 ① 튜링 테스트 → ② 중국어 방 → ③ 시스템 응답의 순서로 정리하고, 각 단계에서 무엇이 핵심 쟁점인지 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>① 튜링 테스트(1950, Alan Turing)</strong> — 핵심 쟁점: <span class="keyw">"기계가 생각한다"는 것을 어떻게 평가할 것인가</span>. 튜링은 행동주의적 답을 제시했다 — 판정관이 사람과 기계를 구분하지 못한다면 그 기계는 지능이 있다고 보자는 것. 즉 외부 행동(대화)이 충분히 사람 같으면 지능을 인정한다는 입장이다.<br><br>
      <strong>② 중국어 방(1980, John Searle)</strong> — 핵심 쟁점: <span class="keyw">"외부 행동이 비슷하다고 정말 '이해'(=지능)를 가진 것인가"</span>. 썰은 사고실험을 통해 부정한다 — 방 안의 서양인이 매뉴얼대로 한자를 매칭해도 중국어를 이해하지 못하듯이, 튜링 테스트를 통과한 기계도 단지 규칙 대조만 하는 것일 뿐 진짜 이해가 아니라는 주장. 즉 외부 행동만으로 지능을 판단할 수 없다는 입장.<br><br>
      <strong>③ 시스템 응답</strong> — 핵심 쟁점: <span class="keyw">"이해의 주체가 부품인가, 시스템 전체인가"</span>. 시스템 응답은 썰의 비판이 잘못된 분석 단위를 골랐다고 본다 — 어느 한 부품도 중국어를 모를 수는 있지만, 시스템 전체는 완벽히 중국어로 대화를 했으니 시스템 자체는 중국어를 이해한 것으로 보아야 한다는 입장. 인간의 뇌도 어떤 한 부위가 언어를 담고 있는 것이 아니라 시스템으로 작동하는 것과 같다.<br><br>
      <strong>의의</strong>: 이 논쟁은 정답이 정해져 있지 않으며 오늘날까지 이어진다. 이세돌의 "알파고는 바둑의 아름다움을 모른다"는 발언은 이 흐름의 현대적 사례이며, AI가 ASI 단계로 발전할 수 있는 시점에서 이 논의는 인류의 생존과도 관련된 중요한 문제로 부각된다.
    </div>
  </div>

  <div class="nav-links">
    <a href="02주차_교과서.html">📚 교과서</a>
    <a href="02주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 03주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 3주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>3주차 문제집</h1>
    <div class="subtitle">바둑, 다음 수는 어딜까!</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">상태공간 탐색의 3요소가 <strong>아닌</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 초기상태(Initial State)</li>
      <li><span class="opt-num">②</span> 목적상태(Goal State)</li>
      <li><span class="opt-num">③</span> 연산자(Operator)</li>
      <li><span class="opt-num">④</span> 평가함수(Evaluation Function)</li>
      <li><span class="opt-num">⑤</span> 해당 사항 없음 (모두 3요소이다)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ 평가함수(Evaluation Function)</strong><br>
      <span class="alabel">해설</span> 상태공간 탐색의 3요소는 <span class="keyw">초기상태 / 목적상태 / 연산자</span>. 평가함수는 휴리스틱 탐색(A*)에서 사용하는 별도 개념이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">선교사와 식인종 문제에서 초기상태가 <code>(3, 3, 1)</code>로 표현되었다. 가운데 숫자(둘째 자리)는 무엇을 의미하는가?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 왼쪽 강변의 선교사 수</li>
      <li><span class="opt-num">②</span> 왼쪽 강변의 식인종 수</li>
      <li><span class="opt-num">③</span> 오른쪽 강변의 선교사 수</li>
      <li><span class="opt-num">④</span> 배의 위치</li>
      <li><span class="opt-num">⑤</span> 이동 횟수</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 왼쪽 강변의 식인종 수</strong><br>
      <span class="alabel">해설</span> 상태 표현은 <code>(왼쪽 선교사 수, 왼쪽 식인종 수, 배의 위치)</code>. 배 위치는 <span class="keyw">왼쪽=1, 오른쪽=-1</span>.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">너비우선 탐색(BFS)의 구현에 사용되는 자료구조는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 스택(Stack)</li>
      <li><span class="opt-num">②</span> 큐(Queue)</li>
      <li><span class="opt-num">③</span> 우선순위 큐(Priority Queue)</li>
      <li><span class="opt-num">④</span> 해시 테이블(Hash Table)</li>
      <li><span class="opt-num">⑤</span> 연결 리스트(Linked List)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 큐(Queue)</strong><br>
      <span class="alabel">해설</span> <span class="keyw">BFS = 큐(FIFO)</span>, <span class="keyw">DFS = 스택(LIFO) 또는 재귀</span>. 자료구조 수업에서 그래프 순회를 배웠다면 같은 개념.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">A* 알고리즘의 평가함수 <code>f(n) = g(n) + h(n)</code>에서 <strong>g(n)</strong>의 의미로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 시작 상태에서 현재 상태 n까지의 실제 비용</li>
      <li><span class="opt-num">②</span> 현재 상태 n에서 목적 상태까지의 추정 비용</li>
      <li><span class="opt-num">③</span> 현재 상태에서 가능한 자식 노드의 수</li>
      <li><span class="opt-num">④</span> 트리의 깊이(depth)</li>
      <li><span class="opt-num">⑤</span> 노드의 우선순위</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>① 시작 상태에서 현재 상태 n까지의 실제 비용</strong><br>
      <span class="alabel">해설</span> <span class="keyw">g(n)</span>은 "지나온 길의 실제 비용", <span class="keyw">h(n)</span>은 "앞으로 갈 길의 추정 비용(휴리스틱)"이다. ②는 h(n)의 의미.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">게임 트리에서 <strong>상대의 차례</strong>를 나타내는 노드 형태와 그 노드 값의 결정 방식으로 옳게 짝지어진 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> OR 노드 — 자식 중 1이 하나라도 있으면 1</li>
      <li><span class="opt-num">②</span> OR 노드 — 자식 중 0이 하나라도 있으면 0</li>
      <li><span class="opt-num">③</span> AND 노드 — 자식 중 1이 하나라도 있으면 1</li>
      <li><span class="opt-num">④</span> AND 노드 — 자식 중 0이 하나라도 있으면 0</li>
      <li><span class="opt-num">⑤</span> AND 노드 — 자식의 평균값</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ AND 노드 — 자식 중 0이 하나라도 있으면 0</strong><br>
      <span class="alabel">해설</span> 상대의 차례는 <span class="keyw">AND 노드</span>. 상대가 자기에게 유리한 0(상대 승)을 무조건 선택할 것이므로, 자식 중 0이 하나라도 있으면 그 노드는 0으로 본다.<br>
      나의 차례는 <span class="keyw">OR 노드</span>로, 자식 중 1이 하나라도 있으면 1.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">상태공간 탐색에서 "문제를 푼다"는 것의 의미를 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      "<strong>초기상태에서 목적상태에 도달하는 일련의 연산자(Operator)를 찾는 일</strong>" 또는 "매 순간 목적상태에 도달하기 위해 할 일을 찾는 것".
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">8-퍼즐 문제에서 ① 초기상태, ② 목적상태, ③ 연산자가 무엇인지 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>초기상태</strong>: 무작위로 섞인 1~8 숫자판(빈칸 1개 포함)<br>
      ② <strong>목적상태</strong>: 1~8이 시계방향으로 정렬된 상태(가운데 빈칸)<br>
      ③ <strong>연산자</strong>: 빈 칸으로 인접 숫자를 이동(상·하·좌·우)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">선교사와 식인종 문제의 두 가지 핵심 제약(규칙)을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>빈 배는 이동할 수 없다</strong> (배에 1~2명이 반드시 타야 함, 한 번에 최대 2명)<br>
      ② <strong>어느 강변에서든 식인종 수가 선교사 수보다 많으면 잡아먹힌다</strong> (단, 그 강변에 선교사가 0명이면 잡아먹히지 않음)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">맹목적 탐색(Blind Search)을 강의에서 어떤 비유로 부르는지, 그리고 두 가지 주요 알고리즘의 이름을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      비유: <strong>"눈 감고 문고리 잡기"</strong> (Blind, 블라인드)<br>
      두 알고리즘: <strong>BFS (Breadth-First Search, 너비우선 탐색)</strong>, <strong>DFS (Depth-First Search, 깊이우선 탐색)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">A* 알고리즘의 평가함수를 쓰고, 각 항이 의미하는 것을 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>f(n) = g(n) + h(n)</strong><br>
      <strong>g(n)</strong>: 시작 상태에서 현재 상태 n까지의 실제 비용 (지나온 길)<br>
      <strong>h(n)</strong>: 현재 상태 n에서 목적 상태까지의 추정 비용 — 휴리스틱 함수 (앞으로 갈 길)<br>
      A*는 항상 f(n)이 가장 작은 노드를 우선 확장한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">8-퍼즐에 A* 알고리즘을 적용할 때, 일반적으로 사용하는 휴리스틱 함수 h(n)은 무엇인지 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>현재 상태와 목표 상태에서 일치하지 않는 칸의 수</strong> (빈칸 제외, 1~8 숫자 기준).<br>
      많이 일치할수록 비용이 적게 든 것으로 본다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">게임 트리(Game Tree)란 무엇이며, 어떤 종류의 문제에 대한 탐색 트리인가?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>두 명이 교대로 두는 게임</strong>(바둑·체스·Tic-Tac-Toe 등)에 대한 탐색 트리. AND-OR 트리 형태로 표현된다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">Min-Max 전략에서 ① 나의 차례 ② 상대의 차례에 각각 어떻게 자식 노드를 선택하는지 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① 나의 차례 (OR 노드): 자식 중 가장 <strong>큰 값(Max)</strong>을 선택 — 나의 이익이 최대<br>
      ② 상대의 차례 (AND 노드): 자식 중 가장 <strong>작은 값(Min)</strong>을 선택 — 상대가 나의 이익이 최소(=상대 이익이 최대)인 것을 고른다고 가정
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">αβ 가지치기에서 α와 β는 각각 무엇을 의미하는지 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>α (alpha)</strong> = 선수(나)가 보장받을 수 있는 <strong>최소 이익</strong>. (Max 측의 하한)<br>
      <strong>β (beta)</strong> = 후수(상대)가 보장받을 수 있는 <strong>최대 이익</strong>. (Min 측의 상한)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">알파고(AlphaGo)는 흔히 딥러닝으로 알려져 있지만, 강의에서 강조한 알파고의 본질적 정체는 무엇인가?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      알파고는 본질적으로 <strong>탐색 시스템</strong>이며, 정확히는 <strong>몬테카를로 트리 탐색(Monte Carlo Tree Search, MCTS) + 합성곱 신경망(CNN, 딥러닝) + 강화학습</strong>의 결합이다. 딥러닝은 그 안의 한 부품일 뿐 알파고의 골격은 탐색이다.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">"문제를 푼다"는 행위를 상태공간 탐색의 관점에서 설명하고, 미로 찾기를 예로 들어 ① 초기상태 ② 목적상태 ③ 연산자를 구체적으로 제시하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      상태공간 탐색의 관점에서 <strong>"문제를 푼다"</strong>는 것은 <span class="keyw">초기상태 S에서 목적상태 G에 도달하는 일련의 연산자(Operator)를 찾는 일</span>이다. 모든 문제는 ① 시작 상황(초기상태), ② 도달하고자 하는 상황(목적상태), ③ 한 상태에서 다른 상태로 옮기는 행동(연산자)의 세 요소로 형식화될 수 있다.<br><br>
      <strong>미로 찾기 예시</strong>:
      <ul>
        <li><strong>초기상태 S</strong>: 미로 입구</li>
        <li><strong>목적상태 G</strong>: 미로 출구</li>
        <li><strong>연산자</strong>: 특정 위치로 이동(상·하·좌·우)</li>
      </ul>
      이렇게 형식화한 뒤 시작 위치에서 가능한 이동을 적용하면서 출구에 도달하는 경로를 찾는 것이 곧 문제 해결이다. 이 과정에서 자연스럽게 <span class="keyw">탐색 트리</span>가 만들어지며, 이를 어떻게 효과적으로 탐색하느냐가 인공지능 문제이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">너비우선 탐색(BFS)과 깊이우선 탐색(DFS)을 비교 설명하시오. 각 알고리즘이 사용하는 자료구조, 유리한 상황, 그리고 한계점을 포함하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>BFS(Breadth-First Search, 너비우선 탐색)</strong>는 같은 깊이의 모든 노드를 먼저 방문한 뒤 다음 깊이로 내려가는 방식으로, <span class="keyw">큐(Queue, FIFO)</span>를 사용한다. 답이 트리의 위쪽(루트에 가까운 곳)에 있을 때 유리하며 <span class="keyw">최단 경로를 보장</span>한다는 장점이 있다. 그러나 같은 깊이의 모든 노드를 메모리에 유지해야 하므로 <span class="keyw">메모리 사용량이 많다</span>.<br><br>
      <strong>DFS(Depth-First Search, 깊이우선 탐색)</strong>는 한 가지를 끝까지 따라간 뒤 막히면 되돌아와(backtrack) 다른 가지를 탐색하는 방식으로, <span class="keyw">스택(Stack, LIFO) 또는 재귀</span>로 구현한다. 답이 트리의 왼쪽 깊은 곳에 있을 때 유리하며 메모리 사용량이 적다. 그러나 <span class="keyw">최단 경로를 보장하지 않으며</span>, 답이 오른쪽 위에 있는 경우 매우 비효율적이 된다.<br><br>
      <strong>공통 한계</strong>: 둘 다 <strong>맹목적 탐색</strong>으로, 문제에 내포된 정보를 활용하지 못한다. 답의 위치를 모르는 일반 문제에서는 어느 것이 더 좋다고 단정할 수 없으며, 경우의 수가 많은 문제(틱택토·바둑)에서는 비효율적이어서 휴리스틱 탐색(A*) 등의 전략이 필요하다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">A* 알고리즘의 평가함수를 쓰고, 8-퍼즐에 적용할 때 g(n)과 h(n)을 어떻게 정의하는지 구체적으로 설명하시오. 또한 BFS·DFS와 비교한 A*의 장점도 함께 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>A* 평가함수</strong>: <code>f(n) = g(n) + h(n)</code><br>
      A*는 항상 f(n)이 가장 작은 노드를 우선 확장하며, <span class="keyw">좋은 h(n)을 정의하면 항상 최적해를 보장</span>하는 것이 이론적으로 증명되어 있다.<br><br>
      <strong>8-퍼즐 적용</strong>:
      <ul>
        <li><strong>g(n)</strong> = 지금까지 숫자 조각을 옮긴 횟수 (지나온 시도 횟수)</li>
        <li><strong>h(n)</strong> = 현재 상태와 목표 상태에서 <span class="keyw">일치하지 않는 칸의 수</span> (빈칸 제외, 1~8 숫자 기준). 일치할수록 비용이 적게 든 것으로 추정.</li>
      </ul>
      예를 들어 시작 상태에서 4개 칸이 일치하지 않으면 f = 0+4 = 4. 다음 단계의 3가지 후보 상태에 대해 f를 계산해 가장 작은 값(예: 6, 4, 6 → 4 선택)으로 진행한다.<br><br>
      <strong>BFS·DFS와의 비교</strong>: BFS는 모든 같은 깊이를 다 살펴봐야 하고, DFS는 한쪽으로 깊이 내려가다 답에서 멀어질 수 있다. 반면 A*는 <span class="keyw">문제에 내포된 정보(휴리스틱)</span>를 활용해 유망한 방향으로 탐색하므로 훨씬 효율적이다. 오늘날 거의 모든 길찾기(스타크래프트 부대 이동 등)에 A*가 사용되고 있다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">게임 트리에서 AND-OR 노드의 차이를 설명하고, Min-Max 전략으로 자식 노드를 선택하는 방법을 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      게임 트리는 두 명이 교대로 두는 게임의 탐색 트리로, <strong>AND-OR 트리</strong> 형태로 표현된다.<br><br>
      <strong>OR 노드 (나의 차례)</strong> — 내가 두는 차례에서는 자식 중 <span class="keyw">하나라도 이길 수 있는 상태(1)</span>가 있으면 그쪽으로 가면 된다. 따라서 OR 연산을 적용해 1·0·0 → <strong>1</strong>이 된다.<br><br>
      <strong>AND 노드 (상대의 차례)</strong> — 상대가 두는 차례에서는 상대가 자기에게 유리한 수(나의 이익이 최소가 되는 수)를 선택한다고 가정해야 한다. 자식 중 <span class="keyw">0이 하나라도 있으면 상대는 그쪽을 무조건 선택</span>하므로 AND 연산을 적용해 1·1·0 → <strong>0</strong>이 된다.<br><br>
      <strong>Min-Max 전략</strong>은 이 원리를 일반화한 것으로, 단순한 1/0이 아니라 점수(이익)로 확장된다.
      <ul>
        <li>① <strong>나의 차례 (OR 노드)</strong>: 자식 중 가장 큰 값(<span class="keyw">Max</span>)을 선택 — 나의 이익이 최대인 수</li>
        <li>② <strong>상대의 차례 (AND 노드)</strong>: 자식 중 가장 작은 값(<span class="keyw">Min</span>)을 선택 — 상대가 자기 유리한, 즉 나의 이익이 최소인 수를 고른다고 가정</li>
      </ul>
      이렇게 하면 상대가 어떤 수를 두든 <strong>나의 보장된 최소 이익</strong>이 정해지고, 그것을 최대화하는 안전한 수를 찾을 수 있다. Min-Max는 알파고 이전까지 게임 AI의 가장 중요한 탐색 전략이었으나, 바둑처럼 경우의 수가 너무 많은 문제에는 부족하여 딥러닝·강화학습이 결합된 MCTS가 등장하게 되었다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">αβ 가지치기(Alpha-Beta Pruning)의 원리를 설명하고, β 가지치기와 α 가지치기 각각의 발생 상황을 예를 들어 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>αβ 가지치기</strong>는 Min-Max 전략을 적용하면서 <span class="keyw">결과에 영향을 주지 않을 가지를 잘라내(Prune)</span> 탐색량을 줄이는 기법이다. 사과나무에서 열매가 열리지 않을 가지를 잘라내듯, 결과에 무의미한 부분을 미리 제거한다.<br><br>
      <strong>α (alpha)</strong>는 선수(나)가 보장받을 수 있는 <span class="keyw">최소 이익</span>(Max 측의 하한)이고, <strong>β (beta)</strong>는 후수(상대)가 보장받을 수 있는 <span class="keyw">최대 이익</span>(Min 측의 상한)이다.<br><br>
      <strong>β 가지치기 (예시)</strong>: 내가 첫째 가지를 따라가면 이익 7이 보장된 상태에서, 둘째 가지를 살피다 보니 상대 노드의 한 자식 값이 8이 나왔다고 하자. 상대는 자기 유리한 쪽(나의 이익이 작은 쪽)을 고르므로 이 가지의 결과는 <span class="keyw">최대 8 이하</span>로 제한되지만, 이미 다른 가지로 가면 7이 보장되므로 <span class="keyw">이 가지의 나머지 자식들을 더 살펴볼 필요가 없다</span>.<br><br>
      <strong>α 가지치기 (예시)</strong>: 내가 첫째 가지를 따라가면 이익 7이 보장된 상태에서, 둘째 가지를 살피다 한 자식 값이 5가 나왔다고 하자. 그 가지의 결과는 <span class="keyw">최소 5 이상</span>이지만, 이미 7이 보장되므로 내가 그 가지로 갈 이유가 없다. <span class="keyw">이 가지의 나머지를 더 살피지 않는다</span>.<br><br>
      이렇게 αβ 가지치기를 적용하면 결과에 영향을 주지 않으면서 <strong>탐색 양을 크게 줄일 수 있어</strong> 경우의 수가 많은 문제도 효율적으로 풀 수 있게 된다. 다만 바둑처럼 극단적으로 큰 문제는 αβ만으로 부족해 알파고에서는 MCTS·딥러닝·강화학습이 결합되어 돌파구를 찾았다.
    </div>
  </div>

  <div class="nav-links">
    <a href="03주차_교과서.html">📚 교과서</a>
    <a href="03주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 04주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 4주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>4주차 문제집</h1>
    <div class="subtitle">지식? 네가 뭘 알아!</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">데이터·정보·지식의 추상화 수준 정렬로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 지식 < 정보 < 데이터</li>
      <li><span class="opt-num">②</span> 데이터 < 정보 < 지식 < 이론 < 원리</li>
      <li><span class="opt-num">③</span> 원리 < 이론 < 지식 < 데이터</li>
      <li><span class="opt-num">④</span> 정보 < 데이터 < 지식 < 원리 < 이론</li>
      <li><span class="opt-num">⑤</span> 데이터 < 지식 < 정보 < 이론</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 데이터 < 정보 < 지식 < 이론 < 원리</strong><br>
      <span class="alabel">해설</span> 데이터(재료) → 정보(가공된 데이터) → 지식(체계적으로 조직된 정보) → 이론 → 원리.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">규칙 기반 전문가 시스템의 5대 구성 요소가 <strong>아닌</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 지식베이스(Knowledge Base)</li>
      <li><span class="opt-num">②</span> 데이터베이스(Database)</li>
      <li><span class="opt-num">③</span> 추론엔진(Inference Engine)</li>
      <li><span class="opt-num">④</span> 학습 알고리즘(Learning Algorithm)</li>
      <li><span class="opt-num">⑤</span> 설명 기능(Explanation Facility)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ 학습 알고리즘</strong><br>
      <span class="alabel">해설</span>
      5대 구성: <span class="keyw">지식베이스 / 데이터베이스 / 추론엔진 / 사용자 인터페이스 / 설명 기능</span>. 학습 알고리즘은 머신러닝·딥러닝 영역이며, 전문가 시스템은 사람이 만든 규칙을 사용한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">"바이올린 ─ISA→ 현악기 ─ISA→ 악기" 형태로 지식을 표현하는 방법은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 규칙(Rule)</li>
      <li><span class="opt-num">②</span> 의미망(Semantic Net)</li>
      <li><span class="opt-num">③</span> 신경망(Neural Network)</li>
      <li><span class="opt-num">④</span> 결정 트리(Decision Tree)</li>
      <li><span class="opt-num">⑤</span> 베이지안 네트워크</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 의미망(Semantic Net)</strong><br>
      <span class="alabel">해설</span>
      개념(노드)들이 ISA·HAS 같은 관계(간선)로 연결된 그래프 형태. 자료구조의 그래프와 동일한 구조.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">전문가 시스템의 강점이지만 딥러닝의 약점인 특성은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 빠른 처리 속도</li>
      <li><span class="opt-num">②</span> 대용량 데이터 처리</li>
      <li><span class="opt-num">③</span> 설명 가능성 (Explainability)</li>
      <li><span class="opt-num">④</span> 자동 학습</li>
      <li><span class="opt-num">⑤</span> 패턴 인식</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 설명 가능성</strong><br>
      <span class="alabel">해설</span>
      전문가 시스템은 논리적 추론 과정을 그대로 설명할 수 있으나, 딥러닝은 학습된 가중치들의 결합이라 사람이 해석하기 어렵다. 그래서 <span class="keyw">XAI(Explainable AI)</span> 연구가 활발.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">뉴런(Neuron)의 부위 중 <strong>출력</strong>을 내보내는 부분은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 수상돌기 (Dendrite)</li>
      <li><span class="opt-num">②</span> 축색돌기 (Axon)</li>
      <li><span class="opt-num">③</span> 시냅스 (Synapse)</li>
      <li><span class="opt-num">④</span> 핵 (Nucleus)</li>
      <li><span class="opt-num">⑤</span> 미토콘드리아 (Mitochondria)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 축색돌기 (Axon)</strong><br>
      <span class="alabel">해설</span>
      <span class="keyw">수상돌기(Dendrite)=입력</span>, <span class="keyw">축색돌기(Axon)=출력</span>, <span class="keyw">시냅스(Synapse)=접합부</span>. 핵은 AI 관점에서 별로 중요하지 않다.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">강의에서 정의한 "지식(Knowledge)"이란 무엇인지 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      "<strong>체계적으로 잘 조직된 정보의 덩어리로서 우리가 알고 있는 것</strong>".
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">지식 표현(Knowledge Representation)의 두 가지 대표 방법을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>의미망(Semantic Net)</strong> — 그래프 형태<br>
      ② <strong>규칙(Rule)</strong> — IF-THEN 형태
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">"지식 병목(Knowledge Bottleneck)"이란 무엇이며, 그 결과 등장한 것은 무엇인가?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>지식 병목</strong>: 인공지능이 처리해야 할 사람의 지식 양이 너무 방대해 한꺼번에 처리할 수 없는 한계.<br>
      <strong>등장</strong>: <strong>전문가 시스템(Expert System)</strong> — 전체 지식이 아닌 특정 분야만 잘 처리하는 시스템.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">규칙 기반 전문가 시스템의 5대 구성 요소를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>지식베이스(Knowledge Base)</strong><br>
      ② <strong>데이터베이스(Database)</strong><br>
      ③ <strong>추론엔진(Inference Engine)</strong><br>
      ④ <strong>사용자 인터페이스(User Interface)</strong><br>
      ⑤ <strong>설명 기능(Explanation Facility)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">전문가 시스템과 2주차에서 배운 인공지능 수준 분류(ANI/AGI/ASI) 중 어디에 해당하는지 쓰고, 모든 분야를 다 잘하는 범용 전문가 시스템은 무엇에 해당하는지도 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      전문가 시스템 = <strong>ANI(Artificial Narrow Intelligence, 약 인공지능)</strong>. 특정 분야만 잘하므로.<br>
      범용 전문가 시스템 = <strong>AGI(Artificial General Intelligence, 일반 인공지능)</strong>. 모든 분야 인간 수준.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">"규칙(Rule)"으로 지식을 표현하는 형식을 쓰고, 관계·추천·지시·전략 중 한 가지의 예를 들어 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      형식: <strong>IF P THEN Q</strong> (P이면 Q이다)<br>
      예시 (택 1): <em>관계</em>: IF 연료탱크가 비었다 THEN 차가 멈췄다 / <em>추천</em>: IF 가을 AND 흐림 AND 비예보 THEN 우산을 가져가라 / <em>지시</em>: IF 차 멈춤 AND 탱크 빔 THEN 연료를 공급해라
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">뉴런의 4대 구성 부위를 영어 명칭과 함께 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>몸통/핵 (Soma / Nucleus)</strong> — AI 관점에서는 별로 중요하지 않음<br>
      ② <strong>수상돌기 (Dendrite)</strong> — 입력을 받음<br>
      ③ <strong>축색돌기 (Axon)</strong> — 출력을 내보냄<br>
      ④ <strong>시냅스 (Synapse)</strong> — 다른 뉴런과의 접합부
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">시냅스에서 뉴런 간 신호 전달 과정을 3단계로 요약하여 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① 축색돌기에서 <strong>전기 신호</strong>가 시냅스 끝까지 이동<br>
      ② 시냅스가 끊어져 있어 <strong>신경전달물질(화학물질)</strong>이 분비됨<br>
      ③ 건너편 수상돌기의 <strong>수용체</strong>가 받아들여 다시 전기 신호로 변환
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">강의에서 강조한 "학습의 본질"이 시냅스의 어떤 변화로 나타나는지 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>"시냅스에서의 신호 강도 조절"</strong>(수용체 수의 변화 등). 같은 입력이 와도 시냅스 상태에 따라 다음 뉴런으로 전달되는 신호의 양이 달라지며, 이것이 곧 학습이다. 인공 신경망에서는 <strong>가중치(Weight)</strong>로 표현된다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">XAI(Explainable AI)가 등장한 배경을 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      딥러닝은 답은 잘 내놓지만 "왜 그런 결론을 냈는지"를 설명하지 못하는 약점이 있어, AI의 의사결정 과정을 사람이 이해할 수 있도록 만드는 <strong>설명 가능한 인공지능(XAI)</strong> 연구가 등장했다.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">데이터(Data)·정보(Information)·지식(Knowledge)의 차이를 설명하고, 인공지능에 "지식"이 등장하게 된 배경을 함께 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>데이터(Data)</strong>는 처리되지 않은 단순한 재료이며, 컴퓨터는 원래 EDPS(Electronic Data Processing System)로서 데이터를 처리하는 장치였다.<br><br>
      <strong>정보(Information)</strong>는 가공된 데이터로, 데이터에 의미가 부여된 것이다. 정보가 다시 다른 처리의 입력으로 쓰일 때는 그 상황에서 데이터 역할을 한다.<br><br>
      <strong>지식(Knowledge)</strong>은 정보보다 한 단계 더 추상화된 개념으로, "<span class="keyw">체계적으로 잘 조직된 정보의 덩어리로서 우리가 알고 있는 것</span>"이다. 즉 정보들이 잘 조직되어 형성된 것이다.<br><br>
      <strong>지식 등장 배경</strong>: 초기 기호주의 인공지능은 기호와 논리만으로 지능을 구현하려 했으나, 실제로는 잘 작동하지 않았다. 사람이 지능적으로 일을 처리하는 방식을 깊이 연구한 결과, 단순한 기호·데이터 수준이 아니라 <span class="keyw">체계적이고 조직된 무언가</span> — 즉 지식 — 를 처리해야 한다는 결론에 이르렀다. 이로부터 <span class="keyw">지식 표현(Knowledge Representation)</span> 연구와 전문가 시스템이 등장하게 되었다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">지식 표현의 두 대표 방법인 의미망(Semantic Net)과 규칙(Rule)을 비교 설명하고, 각각이 자료구조 또는 이산수학의 어떤 개념과 연결되는지도 함께 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>의미망(Semantic Net)</strong>은 지식을 <strong>그래프 형태</strong>로 나타낸다. 노드(Node)는 개념을, 간선(Edge)은 개념들 사이의 관계(ISA, HAS, DOES 등)를 표현한다. 예: "바이올린 ─ISA→ 현악기 ─ISA→ 악기 ─DOES→ 소리를 낸다". 이렇게 표현하면 "첼로가 악기인가?"라는 질문에 첼로 → 현악기 → 악기의 연결을 추적해 답할 수 있다.<br><br>
      <strong>규칙(Rule)</strong>은 지식을 <strong>"IF P THEN Q"</strong> 형식으로 표현한다. 관계, 추천, 지시, 전략, 경험적 전문지식까지 다양한 종류의 지식을 표현할 수 있다. 예: "IF 호흡곤란 AND 발열 AND 기침 THEN COVID 의심".<br><br>
      <strong>자료구조와의 연결</strong>: 의미망은 <span class="keyw">그래프(Graph)</span> 자료구조와 본질적으로 동일하다. 자료구조 수업에서 배우는 인접 행렬·인접 리스트 표현이 그대로 적용된다.<br><br>
      <strong>이산수학과의 연결</strong>: 규칙은 <span class="keyw">명제 논리(Propositional Logic)</span>의 함의(Implication, P→Q)와 같다. 이산수학에서 배우는 진리값·논리 연산·추론 규칙(Modus Ponens 등)이 규칙 기반 추론의 토대이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">"지식 병목(Knowledge Bottleneck)" 현상을 설명하고, 그 결과 등장한 전문가 시스템의 정의와 5대 구성 요소를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>지식 병목</strong>은 인공지능이 처리해야 할 사람의 지식 양이 너무 방대하여 당시 기술로는 모두 처리할 수 없었던 한계를 일컫는다. 병의 좁은 목으로 물이 잘 흘러나가지 못하는 것에 비유한 표현이다. 이로 인해 1980년대까지 진행되던 범용 인공지능 연구는 한계에 부딪혔다.<br><br>
      <strong>해결책</strong>: 모든 지식을 다루는 대신 <span class="keyw">특정 분야</span>의 전문가 수준 지식만 다루는 시스템을 만들자는 발상 → <strong>전문가 시스템(Expert System)</strong>의 등장. 이는 <strong>최초의 상업적으로 성공한 AI</strong>이며, 1980년대 AI 붐의 주역이었다. 2주차의 분류로 ANI(약 인공지능)에 해당한다.<br><br>
      전문가들이 자기 지식을 규칙으로 표현하는 데 능숙하다는 것이 발견되어 <strong>규칙 기반(Rule-Based) 전문가 시스템</strong>이 발전했다.<br><br>
      <strong>5대 구성 요소</strong>:
      <ul>
        <li>① <span class="keyw">지식베이스(Knowledge Base)</span> — IF-THEN 규칙 모음</li>
        <li>② <span class="keyw">데이터베이스(Database)</span> — 환자 증상 등 사실(Facts)</li>
        <li>③ <span class="keyw">추론엔진(Inference Engine)</span> — 사실과 규칙을 결합해 결론 도출</li>
        <li>④ <span class="keyw">사용자 인터페이스(User Interface)</span> — 질의·응답</li>
        <li>⑤ <span class="keyw">설명 기능(Explanation Facility)</span> — "왜 그 결론?" 답변</li>
      </ul>
      이 프레임워크에서 지식베이스만 바꿔 끼우면 의사 진료, 두뇌 우성 판별 등 다양한 분야 시스템을 만들 수 있다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">전문가 시스템의 "설명 기능(Explanation Facility)"이 갖는 의의를 서술하고, 이것이 딥러닝과 비교했을 때 갖는 장점과, 이를 보완하기 위한 연구 분야를 함께 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      전문가 시스템의 <strong>설명 기능</strong>은 시스템이 어떤 결론을 내렸을 때 "왜 그 결론에 이르렀는지"를 사용자에게 <span class="keyw">논리적으로 설명</span>해 줄 수 있는 능력이다. 예를 들어 의사 진료 전문가 시스템이 "COVID가 의심됩니다"라고 진단했을 때, 환자가 "왜인가?"라고 물으면 "당신이 호흡곤란·발열·기침을 모두 보고했고, 이는 R57 규칙의 모든 조건을 충족하기 때문"이라고 추론 과정을 그대로 설명할 수 있다.<br><br>
      <strong>딥러닝과의 비교</strong>: 딥러닝은 답은 척척 내놓지만 <span class="keyw">왜 그런 답인지 설명하지 못하는</span> 약점이 있다. 학습된 가중치들의 복잡한 결합으로부터 결론이 나오기 때문에 사람이 그 과정을 직관적으로 해석하기 어렵다. 이로 인해 의료·법률·금융처럼 의사결정의 근거가 중요한 분야에서 딥러닝의 사용이 제한된다.<br><br>
      <strong>보완 연구</strong>: <span class="keyw">XAI(Explainable AI, 설명 가능한 인공지능)</span> 분야가 활발히 연구되고 있다. 딥러닝 모델의 결정 과정을 시각화하거나 사람이 이해할 수 있는 형태로 설명하는 기법(예: LIME, SHAP, Grad-CAM 등)이 대표적이다. 이는 곧 전문가 시스템의 강점을 딥러닝에 통합하려는 시도이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">뉴런(Neuron)의 구조를 설명하고, 시냅스(Synapse)에서 신호가 전달되는 과정과 그것이 "학습"과 어떻게 연결되는지 서술하시오. 인공 신경망(딥러닝)과의 연결 관계도 함께 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>뉴런 구조</strong>: 뉴런은 ① 몸통(핵, Soma/Nucleus), ② <span class="keyw">수상돌기(Dendrite)</span> — 입력을 받는 부분, ③ <span class="keyw">축색돌기(Axon)</span> — 출력을 내보내는 마디 있는 긴 줄기, ④ <span class="keyw">시냅스(Synapse)</span> — 한 뉴런의 축색돌기 끝과 다른 뉴런의 수상돌기가 만나는 접합부, 로 구성된다. 사람의 뇌에는 약 100억~1000억 개의 뉴런이 그물처럼 연결되어 있다.<br><br>
      <strong>시냅스에서의 신호 전달</strong>: 뉴런 간 신호 전달은 <span class="keyw">전기화학적</span>이다.
      <ul>
        <li>① 축색돌기를 따라 <strong>전기 신호</strong>가 시냅스 끝까지 이동</li>
        <li>② 시냅스가 끊어져 있어 전기 신호가 직접 못 가므로 <strong>신경전달물질(화학물질)</strong>이 분비됨</li>
        <li>③ 건너편 수상돌기의 <strong>수용체(Receptor)</strong>가 화학물질을 받아들임</li>
        <li>④ 다시 <strong>전기 신호</strong>로 변환되어 다음 뉴런으로 전달</li>
      </ul>
      이 과정에서 <span class="keyw">신호의 양이 조절</span>될 수 있다. 수용체 수가 많아지면 더 많은 신호가 전달되고, 적으면 적게 전달된다.<br><br>
      <strong>학습과의 연결</strong>: 같은 신호가 와도 시냅스의 상태에 따라 다음 뉴런으로 전달되는 출력이 달라지며, 경험을 통해 시냅스가 강화되거나 약화된다. 강의는 이를 "<span class="keyw">시냅스에서의 신호 강도 조절 = 학습</span>"이라고 강조하며, 이것이 <strong>딥러닝의 거의 전부</strong>라고 한다.<br><br>
      <strong>인공 신경망과의 연결</strong>: 인공 신경망(Artificial Neural Network)은 이 원리를 수학적으로 모델링한 것이다. 뉴런 = 노드(Node), 시냅스의 신호 강도 = <span class="keyw">가중치(Weight)</span>로 표현된다. 학습은 곧 가중치를 조정하는 과정이며, 5~7주차에서 본격적으로 다룬다.
    </div>
  </div>

  <div class="nav-links">
    <a href="04주차_교과서.html">📚 교과서</a>
    <a href="04주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 05주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 5주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>5주차 문제집</h1>
    <div class="subtitle">뇌세포가 카톡을!</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">인공 뉴런(Artificial Neuron)의 특징으로 <strong>옳지 않은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 입력은 여러 개, 출력은 단 하나(n:1)이다.</li>
      <li><span class="opt-num">②</span> 가중치(Weight)는 생물학적 시냅스에 해당한다.</li>
      <li><span class="opt-num">③</span> 가중치 합은 Σ Wᵢ·Xᵢ로 계산한다.</li>
      <li><span class="opt-num">④</span> 활성함수를 거치지 않은 가중치 합 자체가 곧 출력이다.</li>
      <li><span class="opt-num">⑤</span> ChatGPT의 매개변수 수가 곧 가중치 수이다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④</strong> (가중치 합 자체는 보통 활성함수를 거쳐 출력으로 변환됨)<br>
      <span class="alabel">해설</span> 가중치 합을 그대로 보내는 경우도 있지만 <span class="keyw">일반적으로 활성함수(Step/Sigmoid/ReLU)를 거쳐서 출력</span>한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">시그모이드(Sigmoid) 활성함수의 식과 출력 범위로 <strong>옳은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> max(0, x), 출력 [0, ∞)</li>
      <li><span class="opt-num">②</span> 1/(1+e⁻ˣ), 출력 (0, 1)</li>
      <li><span class="opt-num">③</span> x ≥ 0이면 1, 아니면 0; 출력 {0, 1}</li>
      <li><span class="opt-num">④</span> tanh(x), 출력 (-1, 1)</li>
      <li><span class="opt-num">⑤</span> ax + b, 출력 (-∞, ∞)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 1/(1+e⁻ˣ), 출력 (0, 1)</strong><br>
      <span class="alabel">해설</span> ①은 ReLU, ③은 계단함수. 시그모이드는 S자 곡선으로 출력이 항상 0과 1 사이.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">다층 신경망의 <strong>입력층(Input Layer)</strong>에 대한 설명으로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 가중치를 가지고 있어 입력값에 곱셈을 수행한다.</li>
      <li><span class="opt-num">②</span> 활성함수로 시그모이드를 주로 사용한다.</li>
      <li><span class="opt-num">③</span> "헛개비" — 가중치 없이 값을 그대로 다음 층으로 뿌려준다.</li>
      <li><span class="opt-num">④</span> 학습 시 가장 많이 갱신되는 층이다.</li>
      <li><span class="opt-num">⑤</span> 출력층보다 뉴런 수가 항상 적다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 헛개비 — 가중치 없이 값을 그대로 다음 층으로 뿌려준다</strong><br>
      <span class="alabel">해설</span> 입력층은 가중치도 활성함수도 없으며 값을 바이패스(bypass)할 뿐. Keras 등에서도 입력층은 개수만 지정한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">다층 신경망의 두 가지 핵심 규칙으로 옳은 짝은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 역전파(Backpropagation) + 부분 연결(Partial Connection)</li>
      <li><span class="opt-num">②</span> 전진 전파(Feed Forward) + 완전 연결(Fully Connected)</li>
      <li><span class="opt-num">③</span> 순환 연결(Recurrent) + 합성곱(Convolution)</li>
      <li><span class="opt-num">④</span> 정규화(Normalization) + 드롭아웃(Dropout)</li>
      <li><span class="opt-num">⑤</span> 분기 연결(Branching) + 풀링(Pooling)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 전진 전파 + 완전 연결</strong><br>
      <span class="alabel">해설</span>
      <span class="keyw">Feed Forward</span>: 한 층 → 다음 층 방향. <span class="keyw">Fully Connected</span>: 한 뉴런 출력이 다음 층 모든 뉴런으로. 강의 부제 "이웃에만 공평하게".
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">다음 인공 뉴런의 출력은? (입력 X₁=1, X₂=1, 가중치 W₁=1, W₂=1, 바이어스 가중치 θ=1.5, 활성함수=Step)</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 0</li>
      <li><span class="opt-num">②</span> 0.5</li>
      <li><span class="opt-num">③</span> 1</li>
      <li><span class="opt-num">④</span> -1.5</li>
      <li><span class="opt-num">⑤</span> 1.5</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 1</strong><br>
      <span class="alabel">해설</span>
      가중치 합 = 1·1 + 1·1 − 1.5 = <span class="keyw">0.5</span>. 0.5 ≥ 0이므로 Step Function 출력은 <span class="keyw">1</span>.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">인공 뉴런의 5가지 구성 요소를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>입력 (X₁ ~ Xₙ)</strong> ② <strong>가중치 (W₁ ~ Wₙ)</strong> ③ <strong>가중치 합 (Σ Wᵢ·Xᵢ)</strong> ④ <strong>활성함수 (Activation Function)</strong> ⑤ <strong>출력 (y, 단 하나)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">생물학적 뉴런과 인공 뉴런의 매핑 관계를 4가지 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① 수상돌기(Dendrite) → 입력(X)<br>
      ② 축색돌기(Axon) → 출력(y)<br>
      ③ <strong>시냅스(Synapse) → 가중치(Weight)</strong> ★ 가장 중요<br>
      ④ 몸통/핵 → 활성함수(Activation)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">대표적인 활성함수 3가지의 이름과 식을 각각 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>계단함수(Step)</strong>: x ≥ 0이면 1, 아니면 0<br>
      ② <strong>시그모이드(Sigmoid)</strong>: 1 / (1 + e⁻ˣ)<br>
      ③ <strong>ReLU</strong>: max(0, x)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">바이어스(Bias) 입력이 무엇이며, 왜 필요한지 한두 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      외부 입력과 무관하게 <strong>항상 정해진 값(보통 -1)이 들어가는 추가 입력</strong>. 학습에 필수적이며, 모든 실용 신경망에 포함되어 있다. 활성함수의 임계값을 조절하는 효과를 준다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">ChatGPT 같은 모델이 "수천억 매개변수(Parameters)"를 가졌다고 할 때, 매개변수가 신경망에서 무엇을 의미하는지 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      매개변수 = <strong>가중치(Weight)와 바이어스 가중치의 수</strong>. 신경망 학습은 곧 매개변수를 조정하는 과정이며, 매개변수가 많을수록 더 복잡한 패턴을 학습할 수 있다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">다층 신경망의 3종류 층 이름을 입력 → 출력 순서로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>입력층(Input Layer) → 중간층/은닉층(Hidden Layer) → 출력층(Output Layer)</strong>. 중간층은 1개 이상이며 "은닉층"이라고도 한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">"전진 전파(Feed Forward)"와 "완전 연결(Fully Connected)"의 의미를 각각 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>전진 전파</strong>: 정보가 한 층에서 다음 층 방향으로만 전달된다.<br>
      <strong>완전 연결</strong>: 한 뉴런의 출력이 다음 층의 모든 뉴런에 빠짐없이 전달된다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">시그모이드 함수에서 e가 무엇인지 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>오일러 상수(Euler's number, e ≈ 2.71828…)</strong>. 원주율 π처럼 자연계에 자주 등장하는 무리수이며 자연상수라고도 한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">다음 인공 뉴런의 가중치 합을 구하시오. 입력 X₁=2, X₂=3, X₃=1; 가중치 W₁=0.5, W₂=0.2, W₃=-0.4; 바이어스 θ=0.1.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      가중치 합 = 2·0.5 + 3·0.2 + 1·(-0.4) - 0.1 = 1 + 0.6 - 0.4 - 0.1 = <strong>1.1</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">신경망 학습이 본질적으로 무엇을 조정하는 과정인지 한 단어로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>가중치(Weight)</strong> 또는 매개변수(Parameter). 학습 = 가중치 조정 = 시냅스의 신호 강도 조절(생물학적 비유).
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">생물학적 뉴런과 인공 뉴런을 비교하여 설명하시오. 인공 뉴런의 5가지 구성 요소(입력·가중치·가중치 합·활성함수·출력)와 그것들이 생물학적 뉴런의 어떤 부위에 대응되는지 함께 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>생물학적 뉴런</strong>은 사람의 뇌를 구성하는 신경세포로, 4부위 — 몸통/핵(Soma), 수상돌기(Dendrite, 입력), 축색돌기(Axon, 출력), 시냅스(Synapse, 접합부) — 로 구성된다. 한 뉴런의 출력 신호가 시냅스를 통해 다른 뉴런의 수상돌기로 전달되며, 이때 시냅스의 수용체 수에 따라 신호의 양이 조절된다.<br><br>
      <strong>인공 뉴런</strong>은 이를 단순화한 계산 모델로, 강의 표현으로 "<span class="keyw">뼈만 추리자</span>"라고 한다. 5가지 구성 요소:
      <ul>
        <li>① <strong>입력(X₁ ~ Xₙ)</strong> — 수상돌기에 대응. 여러 개</li>
        <li>② <strong>가중치(W₁ ~ Wₙ)</strong> — <span class="keyw">시냅스에 대응</span>. 입력 신호의 강도를 조절</li>
        <li>③ <strong>가중치 합(Σ Wᵢ·Xᵢ)</strong> — 뉴런이 받아들이는 총 입력</li>
        <li>④ <strong>활성함수</strong> — 가중치 합을 출력으로 변환 (Step/Sigmoid/ReLU)</li>
        <li>⑤ <strong>출력(y)</strong> — 축색돌기에 대응. <span class="keyw">단 하나(n:1)</span></li>
      </ul>
      가장 중요한 매핑은 <strong>시냅스 ↔ 가중치</strong>이며, 신경망 학습 = 가중치 조정 = 시냅스의 신호 강도 조절에 해당한다. ChatGPT의 "수천억 개 매개변수"라는 표현이 곧 이 가중치의 수를 의미한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">활성함수(Activation Function)가 무엇이며 왜 필요한지 설명하고, 대표적인 3가지 활성함수의 이름·식·출력 범위를 비교 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>활성함수</strong>는 인공 뉴런에서 가중치 합을 출력으로 변환하는 비선형 함수이다. 활성함수가 없다면 신경망은 단순한 선형 함수의 조합에 불과하여 복잡한 패턴을 학습할 수 없다. 또한 생물학적 뉴런에서 신호가 일정 임계값 이상일 때만 발화하는 것을 모델링한다.<br><br>
      <strong>대표 3가지</strong>:
      <ul>
        <li>① <span class="keyw">계단함수 (Step Function)</span>: x ≥ 0이면 1, 아니면 0. 출력 범위 {0, 1}. 가장 단순. 초기 신경망에 사용.</li>
        <li>② <span class="keyw">시그모이드 (Sigmoid)</span>: 1/(1+e⁻ˣ). 출력 범위 (0, 1). S자 곡선으로 연속적이며 미분 가능. 학습에 유리.</li>
        <li>③ <span class="keyw">ReLU (Rectified Linear Unit)</span>: max(0, x). 출력 범위 [0, ∞). 0 이하는 0, 양수는 그대로. 딥러닝 시대의 표준이며 계산이 빠르고 깊은 신경망에 적합.</li>
      </ul>
      e는 <strong>오일러 상수(≈2.71828)</strong>이며, 시그모이드는 입력이 아무리 커도 출력이 1을 넘지 않아 신호가 폭발하지 않게 해준다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">다층 신경망(Multi-Layer Neural Network)의 구조를 설명하고, "전진 전파(Feed Forward)"와 "완전 연결(Fully Connected)" 규칙이 무엇을 의미하는지 서술하시오. 또한 입력층이 왜 "헛개비"라고 불리는지 함께 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>다층 신경망</strong>은 인공 뉴런들을 <span class="keyw">층(layer) 단위로 줄을 맞춰</span> 연결한 구조이다. 실제 사람의 뇌는 자유분방하게 얽혀 있지만, 컴퓨터로 계산하기 위해 줄을 맞춰 두면 효율적이기 때문이다. 강의 부제 "줄을 잘 서야 들어가요!"가 이를 의미한다.<br><br>
      구조는 ① <strong>입력층(Input Layer)</strong>, ② <strong>중간층/은닉층(Hidden Layer, 1개 이상)</strong>, ③ <strong>출력층(Output Layer)</strong>으로 되어 있다.<br><br>
      <strong>전진 전파(Feed Forward)</strong>: 정보가 입력층 → 중간층 → 출력층 방향으로만 전달된다. 역방향이나 같은 층 내부 연결은 없다.<br><br>
      <strong>완전 연결(Fully Connected)</strong>: 한 층의 한 뉴런 출력이 <span class="keyw">다음 층의 모든 뉴런</span>으로 빠짐없이 전달된다. 강의 부제 "이웃에만 공평하게"가 이를 표현한다.<br><br>
      <strong>입력층 = "헛개비"인 이유</strong>: 입력층의 노드들은 <span class="keyw">가중치도 활성함수도 없으며</span>, 외부 입력값을 그대로 다음 층의 모든 뉴런으로 뿌려주는 역할만 한다. Keras 등 실제 딥러닝 프레임워크에서도 입력층은 단지 "입력 차원 수"를 지정할 뿐 별도 계산이 없다. 따라서 진정한 의미의 "뉴런"은 아니다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">다음 다층 신경망에 입력 (X₁=1, X₂=1)이 들어왔을 때 최종 출력 Y₅를 구하는 과정을 단계별로 서술하시오.<br>가중치: W₁₃=0.5, W₁₄=0.9, W₂₃=0.4, W₂₄=1.0, W₃₅=-1.2, W₄₅=1.0. 활성함수: 시그모이드 (1/(1+e⁻ˣ)). (소수점 첫째 자리에서 반올림하여 1자리 정수로 답)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>단계 1 — Y₃ 계산</strong>:
      <ul>
        <li>가중치 합 = X₁·W₁₃ + X₂·W₂₃ = 1·0.5 + 1·0.4 = <span class="keyw">0.9</span></li>
        <li>Y₃ = 1/(1 + e⁻⁰·⁹) ≈ <strong>0.71 ≈ 0.7</strong></li>
      </ul>
      <strong>단계 2 — Y₄ 계산</strong>:
      <ul>
        <li>가중치 합 = X₁·W₁₄ + X₂·W₂₄ = 1·0.9 + 1·1.0 = <span class="keyw">1.9</span></li>
        <li>Y₄ = 1/(1 + e⁻¹·⁹) ≈ <strong>0.87 ≈ 0.9</strong></li>
      </ul>
      <strong>단계 3 — Y₅ 계산 (최종 출력)</strong>:
      <ul>
        <li>가중치 합 = Y₃·W₃₅ + Y₄·W₄₅ = 0.7·(-1.2) + 0.9·1.0 = -0.84 + 0.9 = <span class="keyw">0.06</span></li>
        <li>Y₅ = 1/(1 + e⁻⁰·⁰⁶) ≈ <strong>0.515 ≈ 0.5</strong></li>
      </ul>
      따라서 최종 출력 <strong>Y₅ ≈ 0.5</strong>이다.<br><br>
      <strong>풀이 핵심</strong>: 입력층부터 출력층까지 <span class="keyw">층 단위로 차례차례</span> 가중치 합과 활성함수를 적용한다. 이것이 다층 신경망의 전진 전파(Feed Forward) 계산이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">"가중치(Weight)"가 신경망에서 갖는 의미를 4주차에서 배운 시냅스의 학습 원리와 연결하여 설명하고, 신경망 학습이 본질적으로 무엇을 하는 것인지 서술하시오. ChatGPT 같은 대규모 언어 모델과의 연결도 함께 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>가중치(Weight)</strong>는 인공 뉴런에서 각 입력에 곱해지는 값으로, 한 입력이 다음 뉴런에 얼마나 영향을 주는지를 결정한다. 이것은 <span class="keyw">생물학적 시냅스</span>의 역할을 모델링한 것이다.<br><br>
      <strong>4주차 시냅스 원리와의 연결</strong>: 시냅스에서는 한 뉴런의 출력이 다른 뉴런의 입력으로 전달될 때 전기 신호 → 화학 물질 → 전기 신호로 변환되며, 이 과정에서 신호의 양이 조절된다. <span class="keyw">수용체 수가 많아지면 더 많은 신호가 전달</span>되고, 적으면 적게 전달된다. 같은 입력이 와도 시냅스의 상태에 따라 출력이 달라진다 — 이것이 <strong>학습</strong>의 본질이다.<br><br>
      인공 뉴런에서는 이 시냅스의 신호 강도가 <strong>가중치 W</strong>로 표현된다. 따라서 <span class="keyw">신경망 학습 = 가중치 조정</span>이라는 등식이 성립한다. 적절한 가중치를 찾으면 신경망은 입력과 원하는 출력 사이의 관계를 표현하게 된다.<br><br>
      <strong>ChatGPT와의 연결</strong>: ChatGPT 같은 대규모 언어 모델은 <strong>"수천억 개 매개변수(Parameter)"</strong>를 가졌다고 알려져 있는데, 이 매개변수가 곧 가중치이다. 우리가 프롬프트를 입력하면 신경망 내부에서 이 수천억 개 가중치를 사용한 가중치 합과 활성함수 계산이 수없이 일어나며, 그 결과로 답변이 생성된다. 매개변수가 많을수록 더 복잡한 패턴(언어 이해·생성)을 학습할 수 있다. 학습은 방대한 텍스트 데이터를 보면서 이 가중치들을 조금씩 조정해 나가는 과정이며, 6주차부터 본격적으로 다룬다.
    </div>
  </div>

  <div class="nav-links">
    <a href="05주차_교과서.html">📚 교과서</a>
    <a href="05주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 06주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 6주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>6주차 문제집</h1>
    <div class="subtitle">배워서 남주자!</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">"신경망 학습"의 본질을 가장 정확히 표현한 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 활성함수의 종류를 바꾸는 것</li>
      <li><span class="opt-num">②</span> 가중치(Weight)를 수정하는 것</li>
      <li><span class="opt-num">③</span> 입력 데이터를 늘리는 것</li>
      <li><span class="opt-num">④</span> 신경망 층수를 늘리는 것</li>
      <li><span class="opt-num">⑤</span> 출력의 형태를 바꾸는 것</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 가중치를 수정하는 것</strong><br>
      <span class="alabel">해설</span> 신경망 학습 = <span class="keyw">가중치 수정</span>. 4주차 시냅스의 신호 강도 조절과 같은 의미. ChatGPT의 1750억 매개변수가 곧 가중치 수.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">경사하강법(Gradient Descent)의 가중치 수정 식 ΔW = −α·(∂E/∂W)에서 <strong>α</strong>가 의미하는 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 가중치 자체</li>
      <li><span class="opt-num">②</span> 입력값</li>
      <li><span class="opt-num">③</span> 학습률(Learning Rate)</li>
      <li><span class="opt-num">④</span> 활성함수</li>
      <li><span class="opt-num">⑤</span> 오차</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 학습률(Learning Rate)</strong><br>
      <span class="alabel">해설</span> α는 한 번에 얼마나 학습할지를 결정하는 작은 양수. 너무 작으면 수렴 느리고 너무 크면 발산.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">XOR 문제와 신경망 역사에 대한 설명으로 <strong>옳지 않은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 1969년 민스키와 페퍼트(Minsky & Papert)가 단층 신경망의 한계를 지적했다.</li>
      <li><span class="opt-num">②</span> XOR은 선형 분리 불가능한 대표 문제이다.</li>
      <li><span class="opt-num">③</span> XOR 문제는 중간층(은닉층)을 추가하면 해결할 수 있다.</li>
      <li><span class="opt-num">④</span> 1986년 역전파 알고리즘으로 다층 신경망 학습이 가능해졌다.</li>
      <li><span class="opt-num">⑤</span> XOR 문제는 1956년 다트머스 회의에서 해결되었다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>⑤ 1956년 다트머스 회의에서 해결되었다</strong> (틀림)<br>
      <span class="alabel">해설</span>
      다트머스 회의(1956)는 AI 용어 탄생 시점. XOR 문제 해결은 <span class="keyw">1986년 역전파 알고리즘</span>으로 이루어졌다. 그 사이 약 20년이 신경망 1차 겨울.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">역전파 알고리즘(Backpropagation)에 대한 설명으로 <strong>옳은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 입력층에서 출력층 방향으로 데이터를 전파하는 알고리즘이다.</li>
      <li><span class="opt-num">②</span> 출력층의 오차를 입력층 방향(거꾸로)으로 전파하면서 가중치를 수정한다.</li>
      <li><span class="opt-num">③</span> 가중치를 무작위로 변경하는 알고리즘이다.</li>
      <li><span class="opt-num">④</span> 1969년 Minsky가 처음 제안했다.</li>
      <li><span class="opt-num">⑤</span> 단층 신경망에만 적용 가능하다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 출력층의 오차를 입력층 방향(거꾸로)으로 전파하면서 가중치를 수정한다</strong><br>
      <span class="alabel">해설</span>
      역전파(<span class="keyw">Backpropagation</span>)는 1986년 Rumelhart 등이 정립. 미분의 <span class="keyw">연쇄 법칙(Chain Rule)</span>으로 출력층 오차 기울기를 거꾸로 전파.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">"학습 데이터에는 잘 맞지만 새 데이터에는 잘 안 맞는" 현상은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 과소적합(Underfitting)</li>
      <li><span class="opt-num">②</span> 과적합(Overfitting)</li>
      <li><span class="opt-num">③</span> 발산(Divergence)</li>
      <li><span class="opt-num">④</span> 수렴(Convergence)</li>
      <li><span class="opt-num">⑤</span> 정규화(Regularization)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 과적합(Overfitting)</strong><br>
      <span class="alabel">해설</span> 일반화 성능 저하의 핵심 원인. <span class="keyw">정규화(Regularization)</span>·조기 종료·데이터 증강 등으로 해결.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">"신경망 학습"의 본질을 한 단어로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span> <strong>가중치(Weight) 수정</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">손실 함수의 다른 이름 두 가지를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span> <strong>비용 함수(Cost Function)</strong>, <strong>오차 함수(Error Function)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">경사하강법의 가중치 수정 식과 각 항의 의미를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>ΔW = −α · (∂E/∂W)</strong><br>
      ΔW: 가중치 변화량 / α: 학습률(Learning Rate, 작은 양수) / ∂E/∂W: 오차 E를 가중치 W로 미분한 기울기
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">XOR 진리표를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0<br>
      <span class="alabel">해설</span> 두 입력이 같으면 0, 다르면 1. <span class="keyw">선형 분리 불가능</span>한 대표 문제.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">XOR 문제의 한계를 지적한 두 학자와 연도, 그리고 그 한계를 극복한 알고리즘과 연도를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      한계 지적: <strong>민스키와 페퍼트(Minsky & Papert), 1969년</strong><br>
      극복 알고리즘: <strong>역전파(Backpropagation), 1986년</strong> (Rumelhart, Hinton, Williams)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">역전파 알고리즘이 사용하는 미분의 핵심 법칙은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span> <strong>연쇄 법칙 (Chain Rule)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">하이퍼파라미터(Hyperparameter)를 4가지 이상 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답 (택 4)</span>
      ① <strong>학습률(Learning Rate)</strong><br>
      ② <strong>중간층 수(Hidden Layers)</strong><br>
      ③ <strong>각 층의 뉴런 수</strong><br>
      ④ <strong>활성함수 종류(Sigmoid/Tanh/ReLU)</strong><br>
      ⑤ <strong>정규화율(Regularization Rate)</strong><br>
      ⑥ <strong>에폭 수(Epoch)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">과적합과 과소적합의 차이를 한 줄씩 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>과소적합(Underfitting)</strong>: 모델이 너무 단순해 학습 데이터에도 잘 맞지 않는 상태<br>
      <strong>과적합(Overfitting)</strong>: 학습 데이터엔 잘 맞지만 새 데이터에 일반화가 안 되는 상태
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">경사하강법만으로는 다층 신경망 학습이 어려웠던 이유를 한 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>중간층(은닉층) 뉴런이 내보내야 할 "정답값"을 알 수 없어 그 가중치의 기울기를 직접 계산할 수 없었기 때문.</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">오차 함수에서 어떤 가중치 W의 기울기 ∂E/∂W = 5.0이라고 한다. 학습률 α=0.1이라면 가중치는 어떻게 수정되는가? (수치 답변)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ΔW = −α · (∂E/∂W) = −0.1 · 5.0 = <strong>−0.5</strong><br>
      → 가중치는 <strong>0.5만큼 감소</strong>한다.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">"신경망 학습 = 가중치 수정"이라는 명제를 4주차 시냅스 학습 원리·5주차 가중치 개념과 연결하여 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      4주차에서 배운 <strong>생물학적 학습</strong>은 시냅스에서 일어난다. 같은 신호가 와도 시냅스의 수용체 수가 많으면 더 강하게 전달되고 적으면 약하게 전달되는데, 이 수용체 수의 변화가 곧 학습이다.<br><br>
      5주차에서 배운 <strong>인공 뉴런</strong>은 이 시냅스의 신호 강도를 <span class="keyw">가중치(Weight)</span>로 수치화한다. 따라서 인공 신경망의 학습은 가중치를 수정하는 일이며, 이는 생물학적 시냅스의 조절과 정확히 같은 의미이다.<br><br>
      6주차의 핵심은 <strong>그 가중치를 어떻게 수정할 것인가</strong>이다. 오차 함수의 기울기를 따라 가중치를 줄여 나가는 <span class="keyw">경사하강법</span>이 기본 방법이며, 다층 신경망에서는 <span class="keyw">역전파(Backpropagation)</span>로 출력층 오차를 거꾸로 전파해 모든 층의 가중치를 한꺼번에 수정한다. 이 모든 과정의 본질은 결국 가중치를 적절한 값으로 변경하는 것이다.<br><br>
      ChatGPT의 <strong>1750억 매개변수</strong>라는 표현은 곧 1750억 개의 가중치를 의미하며, 이를 학습시키는 과정 = 1750억 개 수도꼭지를 적절히 조절하는 일이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">경사하강법(Gradient Descent)의 원리를 수학식과 함께 설명하고, 학습률(Learning Rate)이 학습에 미치는 영향을 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>경사하강법</strong>은 오차 함수의 기울기(미분값)를 이용하여 오차를 줄이는 방향으로 가중치를 수정하는 알고리즘이다. 산을 내려갈 때 가장 가파른 경사를 따라 내려가면 골짜기에 도달하는 것에 비유된다.<br><br>
      <strong>수학식</strong>:
      <div style="text-align:center; font-family:serif; font-size:18px; margin:14px 0;">ΔW = −α · (∂E/∂W)</div>
      <ul>
        <li>ΔW: 가중치 변화량</li>
        <li>α (alpha): <span class="keyw">학습률(Learning Rate)</span>, 작은 양수</li>
        <li>∂E/∂W: 오차 E를 가중치 W로 미분한 기울기</li>
      </ul>
      <strong>해석</strong>: 기울기가 양수이면 가중치를 감소시키고, 음수이면 증가시킨다. 음의 부호(−)가 있어 항상 기울기 반대 방향으로 가중치가 이동하므로, 매 반복마다 오차가 작아지는 방향으로 진행한다.<br><br>
      <strong>학습률의 영향</strong>:
      <ul>
        <li><span class="keyw">학습률이 너무 작으면</span> 한 번에 가중치가 조금만 변하므로 수렴이 느리고 학습 시간이 매우 길어진다. 또한 지역 최솟값(Local Minimum)에 갇힐 위험도 있다.</li>
        <li><span class="keyw">학습률이 너무 크면</span> 한 번에 너무 멀리 점프해서 최솟값을 지나치거나 발산할 수 있다. 오차가 줄지 않고 오히려 커지는 현상이 발생.</li>
      </ul>
      따라서 적절한 학습률 선택이 중요하며, 보통 0.001~0.1 사이의 값을 사용한다. 학습률은 사람이 설정하는 <span class="keyw">하이퍼파라미터(Hyperparameter)</span>의 대표 예이며, 강의 표현으로 "<em>겸손하게 조금씩 배워야 한다</em>".
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">XOR 문제의 의미와 신경망 1차 겨울, 그리고 1986년 역전파 알고리즘의 등장이 가지는 역사적 의미를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>XOR(Exclusive OR) 문제</strong>는 두 입력이 같으면 0, 다르면 1을 출력하는 단순한 논리 연산이다. 진리표는 (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0이며, 2차원 평면에 표시하면 <span class="keyw">하나의 직선으로 분리할 수 없는</span> 분포(선형 분리 불가능, Non-linearly Separable)이다.<br><br>
      <strong>1969년의 사건</strong>: 마빈 민스키(Marvin Minsky)와 시모어 페퍼트(Seymour Papert)가 저서 <em>Perceptrons</em>에서 <span class="keyw">단층 퍼셉트론(Single-Layer Perceptron)으로는 XOR 문제를 학습할 수 없다</span>고 수학적으로 증명했다. 이는 당시 활발했던 연결주의 연구에 큰 충격을 주었다.<br><br>
      <strong>신경망 1차 겨울(약 1969~1986)</strong>: 신경망 연구가 약 20년간 침체되었다. 연구비 지원이 끊기고, 인공지능 연구의 주류는 기호주의(전문가 시스템 등)로 옮겨갔다. 강의 2주차의 "AI 겨울" 중 첫 번째에 해당.<br><br>
      <strong>1986년 역전파 알고리즘</strong>: 데이비드 룸멜하트(David Rumelhart), 제프리 힌튼(Geoffrey Hinton), 로널드 윌리엄스(Ronald Williams)가 <span class="keyw">역전파(Backpropagation)</span> 알고리즘을 정립하여 다층 신경망의 학습이 가능해졌다. 출력층의 오차를 입력층 방향으로 거꾸로 전파하면서 모든 층의 가중치를 동시에 수정하는 기법이다.<br><br>
      <strong>역사적 의의</strong>:
      <ul>
        <li>① <span class="keyw">중간층(은닉층)을 가진 다층 신경망의 학습</span>이 가능해져 XOR 같은 비선형 문제도 풀 수 있게 됨</li>
        <li>② 신경망 연구의 부활. 이후 1989년 CNN, 1990년대 후반 LSTM, 2010년대 딥러닝 폭발의 토대가 됨</li>
        <li>③ 힌튼은 이 공헌으로 2024년 노벨 물리학상을 수상</li>
        <li>④ 오늘날의 모든 딥러닝 모델은 역전파를 사용하므로, 이 알고리즘은 <span class="keyw">현대 AI의 핵심 기술</span>이라 할 수 있음</li>
      </ul>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">역전파 알고리즘(Backpropagation)의 동작 원리를 단계별로 설명하고, 그 수학적 토대인 연쇄 법칙(Chain Rule)이 어떻게 사용되는지 서술하시오. 강의의 비유 "너 때문이닷!"이 어떤 의미인지도 함께 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>역전파(Backpropagation)</strong>는 다층 신경망의 모든 가중치를 동시에 학습시키기 위한 알고리즘이다.<br><br>
      <strong>동작 단계</strong>:
      <ul>
        <li>① <span class="keyw">전진 전파(Feed Forward)</span>: 입력층 → 중간층 → 출력층 방향으로 신호를 전파해 출력 a를 계산</li>
        <li>② <span class="keyw">출력층 오차 계산</span>: 원하는 출력 d와 실제 출력 a의 차이로 오차 E 계산</li>
        <li>③ <span class="keyw">기울기 역방향 전파</span>: 출력층 → 중간층 → 입력층 방향으로 ∂E/∂W를 차례차례 계산</li>
        <li>④ <span class="keyw">가중치 동시 수정</span>: 모든 층의 가중치를 ΔW = −α·(∂E/∂W) 식으로 한꺼번에 수정</li>
      </ul>
      <strong>연쇄 법칙(Chain Rule)의 사용</strong>: 신경망은 함수의 합성으로 볼 수 있으며 미분의 연쇄 법칙으로 기울기를 분해할 수 있다.
      <div style="text-align:center; font-family:serif; font-size:18px; margin:14px 0;">∂E/∂W₁ = (∂E/∂y) · (∂y/∂z) · (∂z/∂W₁)</div>
      출력층에서 시작해 차례로 거꾸로 곱해 나가면 입력층 가중치의 기울기까지 효율적으로 계산할 수 있다. 이것이 <span class="keyw">동적 계획법(Dynamic Programming)</span> 방식의 효율성을 가져다 준다.<br><br>
      <strong>"너 때문이닷!" 비유</strong>: 출력층 뉴런이 자기 오차를 보고 "이 오차는 너(중간층 뉴런)가 잘못된 신호를 보냈기 때문이다"라며 책임을 묻는 모습. 중간층 뉴런은 자기에게 들어온 책임들을 모아 "그러면 내 가중치를 이렇게 바꿔야지"라며 자기를 수정한다. 같은 식으로 입력층 방향으로 책임이 거꾸로 흘러간다 — 곧 오차의 책임 추적이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">하이퍼파라미터(Hyperparameter)가 무엇이며 매개변수(Parameter)와 어떻게 다른지 설명하시오. 또한 과적합(Overfitting)과 과소적합(Underfitting)의 의미와 해결 방법을 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>매개변수(Parameter)</strong>는 신경망의 가중치(Weight)와 바이어스 가중치를 의미한다. 학습 과정에서 자동으로 조정되는 값이다(예: ChatGPT의 1750억 매개변수).<br><br>
      <strong>하이퍼파라미터(Hyperparameter)</strong>는 가중치를 수정하기 <em>위한</em> 매개변수, 즉 <span class="keyw">학습 과정 자체를 제어하는 변수</span>이다. 사람이 직접 설정하며 정답이 정해져 있지 않다. 대표 예:
      <ul>
        <li>학습률(Learning Rate, α)</li>
        <li>중간층(은닉층) 수와 각 층의 뉴런 수 (신경망 구조)</li>
        <li>활성함수 종류 (Sigmoid/Tanh/ReLU)</li>
        <li>정규화율(Regularization Rate)</li>
        <li>에폭(Epoch) 수</li>
      </ul>
      <strong>차이</strong>: 매개변수는 학습되어 변하는 값, 하이퍼파라미터는 학습 시작 전에 사람이 정하는 값이다.<br><br>
      <strong>과소적합(Underfitting)</strong>: 모델이 너무 단순해 학습 데이터에도 잘 맞지 않는 상태. <em>원인</em>: 중간층/뉴런 부족, 학습 부족. <em>해결</em>: 신경망 구조를 키우고 학습 시간 늘리기.<br><br>
      <strong>과적합(Overfitting)</strong>: 모델이 너무 복잡하거나 학습이 과도해 <span class="keyw">학습 데이터에는 잘 맞지만 새 데이터에는 일반화가 안 되는</span> 상태. <em>원인</em>: 모델 복잡도 과도, 학습 데이터 부족, 너무 오래 학습. <em>해결</em>:
      <ul>
        <li><span class="keyw">정규화(Regularization)</span>: 손실 함수에 가중치 크기 페널티 추가</li>
        <li>드롭아웃(Dropout): 학습 시 일부 뉴런을 무작위로 비활성화</li>
        <li>조기 종료(Early Stopping): 검증 오차가 더 이상 줄지 않으면 학습 중단</li>
        <li>데이터 증강(Data Augmentation): 학습 데이터를 늘리거나 변형</li>
        <li>모델 단순화: 층/뉴런 수 줄이기</li>
      </ul>
      신경망 학습의 목표는 과소적합과 과적합 사이의 <strong>적절한 균형(Sweet Spot)</strong>을 찾는 것이며, 이를 위해 하이퍼파라미터 튜닝이 필수이다.
    </div>
  </div>

  <div class="nav-links">
    <a href="06주차_교과서.html">📚 교과서</a>
    <a href="06주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 07주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 7주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>7주차 문제집</h1>
    <div class="subtitle">인공지능이 노벨상을!</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">DNN(Deep Neural Network)의 정의로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 입력층이 4개 이상인 신경망</li>
      <li><span class="opt-num">②</span> 출력층이 4개 이상인 신경망</li>
      <li><span class="opt-num">③</span> 중간층(은닉층)이 4개 이상인 신경망</li>
      <li><span class="opt-num">④</span> 가중치가 1만 개 이상인 신경망</li>
      <li><span class="opt-num">⑤</span> 활성함수가 ReLU인 신경망</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 중간층(은닉층)이 4개 이상인 신경망</strong><br>
      <span class="alabel">해설</span> DNN = Deep Neural Network = <span class="keyw">심층 신경망</span>. 중간층(은닉층) 수가 깊은 신경망. 딥러닝은 DNN을 학습시키는 기술.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">"기울기 소실(Vanishing Gradient)" 문제를 가장 효과적으로 해결한 활성함수는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> Sigmoid</li>
      <li><span class="opt-num">②</span> Step Function</li>
      <li><span class="opt-num">③</span> ReLU</li>
      <li><span class="opt-num">④</span> Identity Function</li>
      <li><span class="opt-num">⑤</span> Tanh</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ ReLU</strong><br>
      <span class="alabel">해설</span> ReLU = max(0, x). 양수 영역 기울기 1로 일정 → 기울기 소실 완화. <span class="keyw">딥러닝 시대 표준 활성함수</span>. 기울기 소실의 주된 원인은 시그모이드의 포화.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">CNN(합성곱 신경망)의 핵심 연산이 <strong>아닌</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 합성곱 (Convolution)</li>
      <li><span class="opt-num">②</span> 풀링 (Pooling)</li>
      <li><span class="opt-num">③</span> 완전 연결층 (Fully Connected Layer)</li>
      <li><span class="opt-num">④</span> 되먹임 (Feedback)</li>
      <li><span class="opt-num">⑤</span> 필터/커널 (Filter/Kernel)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ 되먹임 (Feedback)</strong><br>
      <span class="alabel">해설</span> 되먹임은 <span class="keyw">RNN(순환 신경망)</span>의 특징. CNN은 피드포워드 구조이며 합성곱·풀링·완전연결층이 핵심.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">2024년 노벨상과 수상자의 짝으로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 물리학상 — 데미스 하사비스 / 화학상 — 제프리 힌튼</li>
      <li><span class="opt-num">②</span> 물리학상 — 제프리 힌튼·존 호필드 / 화학상 — 데미스 하사비스</li>
      <li><span class="opt-num">③</span> 물리학상 — 얀 르쿤 / 화학상 — 요슈아 벤지오</li>
      <li><span class="opt-num">④</span> 물리학상 — 데미스 하사비스 / 화학상 — 존 호필드</li>
      <li><span class="opt-num">⑤</span> 모두 노벨상 수상하지 않았다</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 물리학상 — 힌튼·호필드 / 화학상 — 하사비스</strong><br>
      <span class="alabel">해설</span> 물리학상: <span class="keyw">제프리 힌튼·존 호필드</span>(신경망 기여) / 화학상: <span class="keyw">데미스 하사비스</span>(알파폴드).
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">"드롭아웃(Dropout)"의 주된 목적은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 학습 속도 향상</li>
      <li><span class="opt-num">②</span> 과적합(Overfitting) 방지</li>
      <li><span class="opt-num">③</span> 기울기 소실 완화</li>
      <li><span class="opt-num">④</span> 출력 정규화</li>
      <li><span class="opt-num">⑤</span> 입력 데이터 증강</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 과적합 방지</strong><br>
      <span class="alabel">해설</span> 드롭아웃은 <span class="keyw">학습 중 뉴런을 무작위로 비활성화</span>해 신경망이 특정 경로에만 의존하지 않게 만들어 과적합을 방지한다. 힌튼 제안.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">"신경망 응용(Modeling)"이 무엇인지 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span> 입력에서 출력으로의 <strong>관계를 찾는 일</strong>(함수를 정의하는 작업).
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">기울기 소실(Vanishing Gradient) 문제가 무엇이며 왜 발생하는지 한두 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      역전파에서 출력층 오차가 입력층 방향으로 전파될 때 <strong>층이 깊을수록 기울기가 0에 가까워져 가중치 수정이 거의 일어나지 않는 현상</strong>. 주된 원인은 시그모이드 활성함수의 포화(큰 입력값에서 기울기가 매우 작아짐).
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">딥러닝의 핵심 기술 두 가지(활성함수와 정규화 기법)를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>ReLU</strong> — 기울기 소실 해결<br>
      ② <strong>드롭아웃(Dropout)</strong> — 과적합 방지
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">CNN의 4가지 핵심 연산을 순서대로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>합성곱(Convolution)</strong> — 필터로 특징 추출<br>
      ② <strong>풀링(Pooling)</strong> — 특징지도 크기 축소<br>
      (①②를 여러 번 반복)<br>
      ③ <strong>완전 연결층(Fully Connected Layer)</strong> — 마지막에 분류
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">RNN과 LSTM의 차이점을 한 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>RNN</strong>은 출력을 입력으로 되먹임하는 기본 순환 구조이며, <strong>LSTM</strong>은 RNN의 변형으로 <span class="keyw">장기 의존성(Long-term Dependency)</span> 학습 능력이 개선된 것이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">2024년 노벨 물리학상을 받은 두 명과 그들의 기여를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>제프리 힌튼(Geoffrey Hinton)</strong>: 역전파·CNN·드롭아웃·2010 ImageNet 혁신<br>
      ② <strong>존 호필드(John Hopfield)</strong>: 호필드 네트워크(연관 기억 모델, 1982)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">2024년 노벨 화학상을 받은 사람과 그가 만든 시스템 이름을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>데미스 하사비스(Demis Hassabis)</strong>, <strong>알파폴드(AlphaFold)</strong>. 단백질 3D 구조 예측 모델.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">GPT의 약자를 풀어 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>Generative Pre-trained Transformer</strong> — 생성적, 사전 학습된, 트랜스포머
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">GAN(생성적 적대 신경망)의 두 구성 요소를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>생성자(Generator)</strong> — 가짜 데이터 생성<br>
      ② <strong>판별자(Discriminator)</strong> — 진짜/가짜 구별<br>
      두 신경망이 서로 경쟁하며 학습 → 점점 현실적인 데이터 생성.<br>
      <span class="alabel" style="color:#c1376b;">⚠️ 주의</span>
      <strong>강의 범위 외 외부 지식.</strong> 강 교수 강의 스크립트에는 GAN·생성적 적대·판별자·생성자 키워드가 등장하지 않음. 시험 출제 가능성 낮음.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">이미지 캡셔닝(Image Captioning)에서 CNN과 RNN이 각각 어떤 역할을 하는지 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>CNN</strong>: 이미지에서 특징 추출 (이미지 이해)<br>
      <strong>RNN</strong>: 추출된 특징을 바탕으로 자연스러운 문장 생성 (순서 있는 단어 출력)
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">DNN과 딥러닝의 정의를 쓰고, 깊은 신경망을 학습하는 데 등장하는 가장 큰 문제(기울기 소실)와 그 해결책을 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>DNN(Deep Neural Network)</strong>은 중간층(은닉층)이 <span class="keyw">4개 이상</span>인 깊은 신경망을 의미한다. <strong>딥러닝(Deep Learning)</strong>은 DNN을 효과적으로 학습시키기 위한 기술과 기법들의 총칭이다.<br><br>
      <strong>기울기 소실(Vanishing Gradient) 문제</strong>: 6주차에서 배운 역전파(Backpropagation)에서 출력층의 오차가 입력층 방향으로 거꾸로 전파되는 과정에서, 층이 깊을수록 기울기가 0에 가까워져 깊은 층의 가중치가 거의 수정되지 않는 현상이다. 이는 <span class="keyw">시그모이드(Sigmoid) 활성함수</span>의 포화 영역에서 기울기가 매우 작아지기 때문에 발생한다. 강의 비유: 거리에서 멀리 있는 사람에게 외쳐도 들리지 않듯이, 깊은 층은 학습 신호를 받지 못한다.<br><br>
      <strong>해결책</strong>:
      <ul>
        <li>① <span class="keyw">ReLU(Rectified Linear Unit) 활성함수</span> 사용 — f(x) = max(0, x). 양수 영역에서 기울기가 1로 일정하므로 기울기 소실이 거의 일어나지 않음. 딥러닝 시대의 표준 활성함수가 됨.</li>
        <li>② <span class="keyw">드롭아웃(Dropout)</span> — 힌튼 제안. 학습 중 뉴런을 무작위로 비활성화해 과적합을 방지하고 일반화 성능을 향상.</li>
        <li>③ 좋은 가중치 초기화, 배치 정규화(Batch Normalization), 잔차 연결(Residual Connection) 등 다양한 기법.</li>
      </ul>
      이러한 기술의 발전으로 2010년대부터 깊은 신경망이 본격적으로 학습 가능해졌으며, 이것이 <strong>딥러닝 혁명</strong>의 출발점이 되었다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">CNN(합성곱 신경망)의 구조와 동작 원리를 설명하고, 왜 이미지 처리에 효과적인지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>CNN(Convolutional Neural Network)</strong>은 1989년 얀 르쿤(Yann LeCun)이 제안한, 영상(이미지) 처리에 특화된 신경망 구조이다.<br><br>
      <strong>동작 원리</strong>:
      <ul>
        <li>① <span class="keyw">합성곱(Convolution)</span> — 작은 행렬인 <span class="keyw">필터(Filter, Kernel, Mask)</span>를 이미지 위에서 슬라이딩하면서 곱하고 더해 <span class="keyw">특징지도(Feature Map)</span>를 만든다. 필터마다 다른 종류의 특징(수직선·수평선·대각선·곡선 등)을 추출.</li>
        <li>② <span class="keyw">풀링(Pooling)</span> — 특징지도를 일정 영역(보통 2×2)으로 나누어 그 영역의 <span class="keyw">최댓값(Max Pooling)</span> 또는 <span class="keyw">평균값(Average Pooling)</span>을 취해 크기를 줄인다. 이로써 계산량 감소와 위치 변화에 대한 강건성 확보.</li>
        <li>③ ①과 ②를 여러 번 반복 → <span class="keyw">저수준(선·곡선) → 중간수준(눈·코·입) → 고수준(얼굴 전체)</span>의 계층적 특징 추출.</li>
        <li>④ 마지막에 <span class="keyw">완전 연결층(Fully Connected Layer)</span>을 연결해 분류 결과 출력.</li>
      </ul>
      <strong>이미지 처리에 효과적인 이유</strong>:
      <ul>
        <li>① <strong>지역 특징(Local Feature) 학습</strong>: 합성곱은 작은 영역의 패턴을 찾아내어 자연스러운 이미지 처리 방식과 일치한다.</li>
        <li>② <strong>가중치 공유(Weight Sharing)</strong>: 한 필터를 이미지 전체에 동일하게 적용하므로 매개변수 수가 크게 감소해 학습이 효율적.</li>
        <li>③ <strong>위치 불변성(Translation Invariance)</strong>: 같은 객체가 이미지의 어디에 있어도 비슷하게 인식한다.</li>
        <li>④ <strong>계층적 추상화</strong>: 사람의 시각 시스템처럼 저수준에서 고수준으로 특징을 단계적으로 추상화한다.</li>
      </ul>
      이러한 특성 덕분에 CNN은 이미지 분류·객체 검출·자율주행·얼굴 인식·의료 영상 분석 등 영상 처리의 표준 기술이 되었다. 알파고에도 사용되었으며, 2024년 노벨 물리학상의 근거 중 하나이기도 하다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">RNN(순환 신경망)이 무엇이며, 일반 피드포워드 신경망과 어떻게 다른지 설명하시오. LSTM의 의의도 함께 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>RNN(Recurrent Neural Network, 순환 신경망)</strong>은 출력을 다시 자기 자신의 입력으로 <span class="keyw">되먹임(Feedback)</span>하는 신경망이다. 이 되먹임 구조 덕분에 이전 시점의 정보를 기억하면서 현재 시점의 처리에 활용할 수 있다.<br><br>
      <strong>피드포워드 신경망과의 차이</strong>:
      <ul>
        <li><strong>피드포워드(Feed-Forward)</strong>: 입력 → 출력 한 방향. 각 입력은 독립적으로 처리됨. 이미지 분류 같은 정적 데이터에 적합.</li>
        <li><strong>RNN(Recurrent)</strong>: 되먹임 있음. 시간/순서 정보 유지. <span class="keyw">시계열(Time Series)·자연어·음성</span> 같은 순서 데이터에 적합.</li>
      </ul>
      <strong>예시</strong>: "나는 학교에 ___" 라는 문장의 빈칸을 예측하려면 앞의 단어들을 기억해야 한다. RNN은 이런 순서 의존성을 학습할 수 있다.<br><br>
      <strong>RNN의 한계</strong>: 기본 RNN은 <span class="keyw">장기 의존성(Long-term Dependency)</span> 학습이 어렵다. 즉 멀리 떨어진 정보를 기억하기 어렵다. 이는 기울기 소실/폭주 문제 때문.<br><br>
      <strong>LSTM(Long Short-Term Memory)의 의의</strong>: 1997년 Hochreiter & Schmidhuber가 제안한 RNN의 변형. <span class="keyw">게이트(Gate) 메커니즘</span>(입력 게이트·망각 게이트·출력 게이트)을 도입해 어떤 정보를 기억하고 잊을지 학습한다. 이로써 매우 긴 문맥도 처리 가능.<br><br>
      LSTM은 2010년대까지 자연어 처리·음성 인식·기계 번역의 표준 모델이었으며, 이후 트랜스포머(Transformer)에 자리를 양보했지만 여전히 시계열 처리에서 중요한 위치를 차지한다. <strong>호필드 네트워크</strong>(1982)도 순환 신경망의 일종으로, 2024년 노벨 물리학상의 근거가 되었다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">생성 AI(Generative AI)의 대표 모델 GPT의 구조와 동작 원리를 설명하고, 이미지 생성에 강력한 GAN의 원리도 함께 서술하시오. <span style="color:#c1376b; font-size:13px;">(⚠️ GAN 부분은 강의 범위 외 외부 지식)</span></div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>GPT(Generative Pre-trained Transformer)</strong>는 OpenAI가 개발한 대규모 언어 모델이다. 이름이 의미하는 바:
      <ul>
        <li>Generative — 텍스트를 <em>생성</em>한다</li>
        <li>Pre-trained — 방대한 텍스트 데이터로 <em>사전 학습</em>되었다</li>
        <li>Transformer — <span class="keyw">트랜스포머(Transformer)</span> 구조 기반</li>
      </ul>
      <strong>구조</strong>: 2017년 Google이 제안한 트랜스포머는 <span class="keyw">어텐션(Attention)</span> 메커니즘을 핵심으로 한다. 어텐션은 입력 시퀀스의 각 부분에 "얼마나 집중할지"를 학습한다. 이로써 멀리 떨어진 단어들 사이의 관계도 효과적으로 처리할 수 있어, RNN의 한계를 극복했다.<br><br>
      <strong>동작 원리</strong>: GPT는 주어진 텍스트 프롬프트(prompt)를 받아 <span class="keyw">다음 단어를 순차적으로 예측·생성</span>한다. 예: "오늘 날씨가" → "맑다" → "그래서" → "산책하기" → "좋다" 같은 식. 매개변수가 1750억 개(GPT-3) 또는 그 이상으로 매우 거대.<br><br>
      <strong>GAN(Generative Adversarial Network, 생성적 적대 신경망)</strong>은 2014년 Ian Goodfellow가 제안한 생성 모델이다. 두 신경망이 경쟁하며 학습한다:
      <ul>
        <li>① <span class="keyw">생성자(Generator)</span>: 가짜 데이터(이미지 등)를 만들어 낸다</li>
        <li>② <span class="keyw">판별자(Discriminator)</span>: 진짜 데이터와 가짜를 구별하려 시도한다</li>
      </ul>
      두 신경망이 서로 속이고 잡으려 경쟁하면서 점점 더 현실적인 데이터를 생성하게 된다. 비유하자면 위조지폐범과 경찰의 대결 — 경찰이 똑똑해질수록 위조지폐범도 더 정교한 위조지폐를 만든다.<br><br>
      <strong>응용</strong>: GAN은 사진 생성·딥페이크·스타일 전송 등에 강력. GPT는 텍스트 대화·번역·요약·코드 생성 등에 활용. 둘은 결합되기도 한다 — 예: 이미지 캡셔닝(CNN+RNN/Transformer), 동화책 자동 생성(이미지 → CNN → GPT → TTS).<br><br>
      <strong>윤리적 우려</strong>: 딥페이크, 저작권 분쟁, 가짜 뉴스, 신원 위조, 일자리 대체 등이 사회적 문제로 대두. 일부 문학상은 AI 작품 구별이 어려워져 폐지되기도 했다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">2024년 노벨상에서 인공지능이 물리학상과 화학상을 동시에 수상한 의미를 서술하시오. 수상자 세 명의 이름과 각자의 기여를 정확히 명시하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      2024년 노벨상은 <strong>인공지능(특히 신경망 기반 딥러닝)이 기초 과학으로 인정받은 역사적 사건</strong>이다.<br><br>
      <strong>2024 노벨 물리학상</strong>:
      <ul>
        <li>① <span class="keyw">제프리 힌튼(Geoffrey Hinton)</span> — "딥러닝의 대부"라 불림. 1986년 <strong>역전파(Backpropagation)</strong> 알고리즘 정립 기여, 1989년 <strong>볼츠만 머신(Boltzmann Machine)</strong>, 2010년 ImageNet 영상 인식 혁신, <strong>드롭아웃(Dropout)</strong> 제안. 6~7주차의 거의 모든 핵심 기술의 중심에 있다. 캐나다 토론토 대학.</li>
        <li>② <span class="keyw">존 호필드(John Hopfield)</span> — 1982년 <strong>호필드 네트워크(Hopfield Network)</strong> 제안. 순환 신경망의 일종으로 연관 기억(Associative Memory)을 모델링했다. 물리학자 출신으로 통계물리학을 신경망에 도입.</li>
      </ul>
      <strong>2024 노벨 화학상</strong>:
      <ul>
        <li>③ <span class="keyw">데미스 하사비스(Demis Hassabis)</span> — Google DeepMind CEO. 2016년 <strong>알파고(AlphaGo)</strong>로 이세돌 9단 격파. 2018년 <strong>알파폴드(AlphaFold)</strong>로 단백질 3D 구조 예측 문제를 혁신적으로 해결. 단백질 구조 예측은 50년간 생명과학의 큰 난제였는데, 알파폴드가 거의 해결했다. 이는 신약 개발·질병 연구 등 화학·생명과학 분야에 막대한 영향.</li>
      </ul>
      <strong>의미</strong>:
      <ul>
        <li>① <strong>학문적 인정</strong>: 신경망·딥러닝이 단순한 공학 기술을 넘어 <span class="keyw">기초 과학</span>으로서의 가치를 인정받았다.</li>
        <li>② <strong>학제 융합</strong>: 인공지능이 물리학(통계 물리학과 신경망)·화학(단백질 구조)·생명과학·수학 등 모든 분야에 영향을 미친다는 것을 보여줌.</li>
        <li>③ <strong>역사적 전환점</strong>: 2주차에서 배운 1969 XOR 문제로 인한 신경망 1차 겨울, 1986 역전파로 부활, 2010 딥러닝 혁명, 2016 알파고, 2022 ChatGPT를 거쳐 마침내 노벨상까지 — AI 역사의 정점.</li>
        <li>④ <strong>책임의 무게</strong>: 힌튼은 노벨상 수상 후에도 AI의 위험성을 경고하고 있다. AI가 발전할수록 윤리·안전·통제 문제가 더욱 중요해진다.</li>
      </ul>
      이는 강의 1주차의 "<em>인공지능이 인문학</em>" 메시지와 직결된다 — AI가 강력해질수록 인간에 대한 이해와 책임이 더욱 중요해진다.
    </div>
  </div>

  <div class="nav-links">
    <a href="07주차_교과서.html">📚 교과서</a>
    <a href="07주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 08주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 8주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>8주차 문제집</h1>
    <div class="subtitle">엄마는 고등어를 좋아해!</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">확률(Probability)에 대한 설명 중 <strong>옳지 않은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 0과 1 사이의 값으로 표현된다.</li>
      <li><span class="opt-num">②</span> 0에 가까울수록 발생 가능성이 낮다.</li>
      <li><span class="opt-num">③</span> 1에 가까울수록 발생 가능성이 높다.</li>
      <li><span class="opt-num">④</span> 0과 1이 가장 불확실한 상태이다.</li>
      <li><span class="opt-num">⑤</span> 불확실한 정도를 측정하는 도구이다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ 0과 1이 가장 불확실한 상태이다</strong> (틀림)<br>
      <span class="alabel">해설</span> 0과 1은 각각 "불가능"과 "확실"로 가장 확실한 상태. <span class="keyw">0.5가 가장 불확실한 상태</span>.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">두 자녀가 있는 가정에서 "첫째가 딸일 때 둘 다 딸일 확률"은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 1/4</li>
      <li><span class="opt-num">②</span> 1/3</li>
      <li><span class="opt-num">③</span> 1/2</li>
      <li><span class="opt-num">④</span> 2/3</li>
      <li><span class="opt-num">⑤</span> 1</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 1/2</strong><br>
      <span class="alabel">해설</span> 첫째가 딸이라는 조건 하에 둘째도 딸일 확률 = 둘째가 딸일 확률 = 1/2. 조건부 확률.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">베이즈 정리에 등장하는 용어 중 "결과 X를 보기 전 원인 A의 초기 확률"을 의미하는 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 사후확률 (Posterior)</li>
      <li><span class="opt-num">②</span> 우도 (Likelihood)</li>
      <li><span class="opt-num">③</span> 사전확률 (Prior)</li>
      <li><span class="opt-num">④</span> 증거 (Evidence)</li>
      <li><span class="opt-num">⑤</span> 정규화 상수 (Normalizer)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 사전확률 (Prior)</strong><br>
      <span class="alabel">해설</span> Prior=사전, Likelihood=우도(원인이 있을 때 결과의 확률), Evidence=증거(결과의 전체 확률), Posterior=사후(결과 본 후 갱신된 원인 확률).
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">확률과 퍼지의 차이로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 확률 = 속하는 정도, 퍼지 = 발생 가능성</li>
      <li><span class="opt-num">②</span> 확률 = 발생 가능성, 퍼지 = 속하는 정도(경계 모호함)</li>
      <li><span class="opt-num">③</span> 둘 다 같은 의미</li>
      <li><span class="opt-num">④</span> 확률은 0~1, 퍼지는 0~10</li>
      <li><span class="opt-num">⑤</span> 확률은 컴퓨터, 퍼지는 사람만 다룬다</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 확률 = 발생 가능성, 퍼지 = 속하는 정도</strong><br>
      <span class="alabel">해설</span> 확률은 사건의 가능성, 퍼지는 경계의 모호함을 다룬다. 둘 다 0~1 범위지만 의미가 다르다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">퍼지 추론(Fuzzy Inference)의 4단계가 <strong>아닌</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 퍼지화 (Fuzzification)</li>
      <li><span class="opt-num">②</span> 규칙 적용 (Rule Application)</li>
      <li><span class="opt-num">③</span> 집계 (Aggregation)</li>
      <li><span class="opt-num">④</span> 비퍼지화 (Defuzzification)</li>
      <li><span class="opt-num">⑤</span> 역전파 (Backpropagation)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>⑤ 역전파</strong><br>
      <span class="alabel">해설</span> 퍼지 추론 4단계: <span class="keyw">퍼지화 → 규칙 적용 → 집계 → 비퍼지화(무게중심)</span>. 역전파는 6주차 신경망 학습 알고리즘.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">조건부 확률 P(A|X)를 일반 확률로 풀어 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span> <strong>P(A|X) = P(A ∩ X) / P(X)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">베이즈 규칙(Bayes' Rule)을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span> <strong>P(A|X) = P(X|A) · P(A) / P(X)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">베이즈 정리에서 4가지 용어(사전확률·우도·증거·사후확률)의 영어를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      사전확률 = <strong>Prior</strong> · 우도 = <strong>Likelihood</strong> · 증거 = <strong>Evidence</strong> · 사후확률 = <strong>Posterior</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">"엄마는 고등어를 좋아해" 사례에서 자주 가는 마트(M4, 40%)와 고등어를 사왔을 때 가장 가능성 높은 마트(M3, 32%)가 다른 이유를 한 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      M4는 자주 가지만 그 마트에서 고등어를 살 확률이 낮고(P(고등어|M4)=0.1), M3는 덜 가지만 그 마트의 고등어 구매 확률이 상대적으로 높아(P(고등어|M3)=0.2) <strong>우도(Likelihood)</strong>가 사후확률을 뒤집기 때문.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">암 진단에서 "검사 정확성 99%"가 의미하는 P(?|?)를 수식으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>P(양성 | 암) = 0.99</strong> — "암 환자에게 양성 판정이 나올 확률"이지, "양성 판정 후 실제 암일 확률"이 아니다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">베이즈 정리의 현대적 응용 분야를 3가지 이상 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>스팸 필터(Spam Filter)</strong><br>
      ② <strong>의료 진단</strong><br>
      ③ <strong>음성 인식</strong><br>
      ④ <strong>나이브 베이즈 분류기(Naive Bayes Classifier)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">퍼지(Fuzzy)의 사전적 의미와 그것이 다루는 것을 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      "Fuzzy"는 <strong>"흐릿한, 경계가 명확하지 않은"</strong>이라는 뜻. 인간 언어의 <strong>애매모호함(경계의 모호함)</strong>을 수학적으로 표현한 이론.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">멤버십 함수 μ_큼(175cm) = 0.8의 의미를 한 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      "175cm는 <strong>'크다'(Tall) 퍼지 집합에 80% 정도 속한다</strong>"는 의미.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">퍼지 추론의 4단계를 순서대로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>퍼지화 (Fuzzification)</strong> — 수치 값을 멤버십 함수값으로<br>
      ② <strong>규칙 적용 (Rule Application)</strong> — 퍼지 IF-THEN 규칙<br>
      ③ <strong>집계 (Aggregation)</strong> — 결과 결합<br>
      ④ <strong>비퍼지화 (Defuzzification)</strong> — 무게중심으로 수치 출력
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">P(A) = 0.4, P(B|A) = 0.5, P(B|¬A) = 0.1일 때 P(A|B)는? (소수점 둘째 자리까지)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      P(B) = P(B|A)·P(A) + P(B|¬A)·P(¬A) = 0.5·0.4 + 0.1·0.6 = 0.20 + 0.06 = <strong>0.26</strong><br>
      P(A|B) = P(B|A)·P(A) / P(B) = 0.5·0.4 / 0.26 ≈ <strong>0.77</strong>
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">"엄마는 고등어를 좋아해" 사례를 베이즈 정리로 풀어 보이시오. 다음 데이터를 사용하시오: P(M1)=0.1, P(M2)=0.2, P(M3)=0.3, P(M4)=0.4; P(고등어|M1)=0.5, P(고등어|M2)=0.2, P(고등어|M3)=0.2, P(고등어|M4)=0.1. 각 마트의 사후확률을 계산하고, 가장 가능성 높은 마트는?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>1단계: 분모 P(고등어) 계산</strong>
      <div style="text-align:center; font-family:serif; margin:10px 0;">
        P(고등어) = Σ P(고등어|Mᵢ)·P(Mᵢ)<br>
        = 0.5·0.1 + 0.2·0.2 + 0.2·0.3 + 0.1·0.4<br>
        = 0.05 + 0.04 + 0.06 + 0.04 = <strong>0.19</strong>
      </div>
      <strong>2단계: 각 마트 사후확률 계산</strong>
      <ul>
        <li>P(M1|고등어) = (0.5·0.1) / 0.19 = 0.05/0.19 ≈ <span class="keyw">0.26</span></li>
        <li>P(M2|고등어) = (0.2·0.2) / 0.19 = 0.04/0.19 ≈ <span class="keyw">0.21</span></li>
        <li>P(M3|고등어) = (0.2·0.3) / 0.19 = 0.06/0.19 ≈ <span class="keyw">0.32</span> ★</li>
        <li>P(M4|고등어) = (0.1·0.4) / 0.19 = 0.04/0.19 ≈ <span class="keyw">0.21</span></li>
      </ul>
      <strong>결론</strong>: 가장 가능성 높은 마트는 <strong>M3 (32%)</strong>이다.<br><br>
      <strong>해석</strong>: 엄마가 가장 자주 가는 마트는 M4(40%)지만, 고등어를 사왔다는 사실(증거)이 추가되면서 사후확률이 변한다. M3는 사전확률은 30%로 두 번째였지만, 그 마트의 고등어 구매 확률(우도)이 상대적으로 높아 사후확률에서 1위가 된다. 이는 베이즈 정리의 핵심 — <span class="keyw">증거가 사전확률을 뒤집을 수 있다</span> — 를 보여 준다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">조건부 확률과 베이즈 정리의 차이를 설명하고, 베이즈 정리가 왜 인공지능에서 중요한지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>조건부 확률</strong> P(A|X)는 "X가 주어졌을 때 A가 일어날 확률"을 정의한다 — P(A|X) = P(A∩X)/P(X). 어떤 조건 하에서의 단순한 확률 측정이다.<br><br>
      <strong>베이즈 정리</strong>는 그 위에 <span class="keyw">방향을 거꾸로 추론</span>하는 식이다:
      <div style="text-align:center; font-family:serif; margin:10px 0;">
        P(A|X) = P(X|A)·P(A) / P(X)
      </div>
      이미 P(X|A)와 P(A)를 알고 있을 때 P(A|X)를 구할 수 있다. 즉 <strong>"원인 → 결과"의 확률에서 "결과 → 원인"의 확률을 추론</strong>한다. 이를 <strong>역확률(Inverse Probability)</strong> 문제라 부른다.<br><br>
      <strong>인공지능에서의 중요성</strong>:
      <ul>
        <li>① <strong>관찰로부터 추론</strong>: AI는 보통 결과(증상·관측)를 보고 원인(질병·라벨)을 추정해야 하는데, 베이즈 정리가 이를 가능케 한다.</li>
        <li>② <strong>학습의 토대</strong>: 데이터가 누적될수록 우도가 정확해지며, 사후확률이 점점 정확해지는 것이 곧 학습이다.</li>
        <li>③ <strong>응용 다수</strong>: 스팸 필터(메일 단어로부터 스팸 여부 추정), 의료 진단(증상으로부터 질병 추정), 음성 인식(소리 파형으로부터 단어 추정), 나이브 베이즈 분류기.</li>
        <li>④ <strong>설명 가능</strong>: 4주차 전문가 시스템처럼 추론 근거(어떤 우도와 사전확률이 결합되어 결론이 나왔는지)를 명확히 설명할 수 있다 — 딥러닝의 블랙박스와 대조적.</li>
      </ul>
      이런 점에서 베이즈 정리는 <strong>"확률적 추론"의 표준 도구</strong>이며, 머신러닝과 통계학의 핵심을 이룬다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">암 진단에서 "검사 정확성 99%"가 환자가 정말 알고 싶은 것과 어떻게 다른지 설명하고, 베이즈 정리로 풀어 그 차이를 보이시오. (암 발병률 1% 가정)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      "<strong>검사 정확성 99%</strong>"의 정확한 의미는 <span class="keyw">P(양성 | 암) = 0.99</span> — 암 환자에게 양성 판정이 나올 확률이다. 이는 <em>의료 검사의 민감도(Sensitivity)</em>이다.<br><br>
      그러나 환자가 정말로 알고 싶은 것은 <strong>"양성 판정을 받았는데 실제로 암일 확률" = P(암 | 양성)</strong>이다. 이 둘은 전혀 다르다.<br><br>
      <strong>베이즈 정리 적용</strong> (암 발병률 1% 가정, 검사 정확성 99% = 거짓 양성률 1%):
      <ul>
        <li>P(암) = 0.01 (사전확률)</li>
        <li>P(¬암) = 0.99</li>
        <li>P(양성|암) = 0.99 (우도, 정확한 양성)</li>
        <li>P(양성|¬암) = 0.01 (거짓 양성)</li>
      </ul>
      P(양성) = P(양성|암)·P(암) + P(양성|¬암)·P(¬암) = 0.99·0.01 + 0.01·0.99 = 0.0099 + 0.0099 = <strong>0.0198</strong>.<br><br>
      <strong>P(암|양성) = P(양성|암)·P(암) / P(양성) = 0.0099 / 0.0198 = 0.5 = 50%</strong> (단순화한 경우).<br><br>
      더 보수적인 거짓 양성률을 적용하면 P(암|양성)은 <span class="keyw">1~10%</span> 정도로 매우 낮아질 수 있다. 이는 <strong>거짓 양성(False Positive)</strong>이 많아 발생하는 현상이다.<br><br>
      <strong>의의</strong>: 검사 정확성이 높아도 <strong>희귀한 질병의 경우 양성 판정만으로 단정 짓기 어렵다</strong>. 추가 검사가 필요한 이유. 강의 메시지: <em>"모든 답은 문제에 있다"</em> — P(양성|암)과 P(암|양성)의 차이를 정확히 인식해야 올바른 결정을 내릴 수 있다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">확률(Probability)과 퍼지(Fuzzy)의 차이를 설명하고, 퍼지 집합과 멤버십 함수의 의미를 예시와 함께 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>확률과 퍼지의 차이</strong>:
      <ul>
        <li><strong>확률(Probability)</strong>: <span class="keyw">사건 발생의 가능성</span>을 0~1로 측정. 예: "내일 비 올 확률 30%"는 비라는 사건이 일어날 가능성.</li>
        <li><strong>퍼지(Fuzzy)</strong>: <span class="keyw">개념의 경계 모호함</span>을 0~1로 측정. 예: "키가 큰 편이다"는 키 175cm가 "크다"라는 집합에 어느 정도 속하는지.</li>
      </ul>
      두 이론 모두 0과 1 사이의 값을 사용하지만 의미가 전혀 다르다. 확률은 "일어날 가능성", 퍼지는 "속하는 정도"를 나타낸다.<br><br>
      <strong>퍼지 집합(Fuzzy Set)</strong>은 일반 집합과 달리 원소의 소속 여부를 0과 1 사이의 실수로 표현한다.
      <table style="margin:10px 0;">
        <tr><th>키</th><th>일반 집합 ("170cm 이상이면 큼")</th><th>퍼지 집합 (μ_큼)</th></tr>
        <tr><td>165cm</td><td>0 (안 큼)</td><td>0.2</td></tr>
        <tr><td>170cm</td><td>1 (큼)</td><td>0.5</td></tr>
        <tr><td>175cm</td><td>1 (큼)</td><td>0.8</td></tr>
        <tr><td>185cm</td><td>1 (큼)</td><td>1.0</td></tr>
      </table>
      퍼지 집합은 자연스럽게 모호한 경계를 표현한다.<br><br>
      <strong>멤버십 함수(Membership Function)</strong>는 원소 x가 퍼지 집합 A에 속하는 정도를 나타내는 함수 μ_A(x)이며, 0 ≤ μ ≤ 1이다. 예: μ_큼(175cm) = 0.8은 "175cm는 '크다'에 80% 정도 속한다"를 의미한다.<br><br>
      <strong>응용</strong>: 1990년대부터 퍼지 세탁기·에어컨·자동초점 카메라·일본 센다이 지하철 자동 운행 등에 광범위하게 사용. 1주차의 "딱딱함 vs 부드러움"의 부드러움 영역에 해당하며, 강태원 교수 전공인 <span class="keyw">계산지능(CI) / 소프트 컴퓨팅(Soft Computing)</span>의 핵심 분야이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">퍼지 추론(Fuzzy Inference)의 4단계를 순서대로 설명하고, 냉난방기 제어를 예로 들어 어떻게 적용되는지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>퍼지 추론(Fuzzy Inference)</strong>은 퍼지 규칙들과 입력값으로부터 출력값을 도출하는 과정이다. 4단계로 구성된다:<br><br>
      <strong>① 퍼지화 (Fuzzification)</strong>: 입력된 구체적인 수치 값을 퍼지 집합의 멤버십 함수값으로 변환. 예: 온도 33℃ → μ_높다(33) = 0.8, μ_중간(33) = 0.2.<br><br>
      <strong>② 규칙 적용 (Rule Application)</strong>: 미리 정의된 퍼지 IF-THEN 규칙들을 적용. 각 규칙의 조건부 멤버십값을 계산해 결론부 멤버십을 도출. 예: <em>"IF 온도가 높고 AND 습도가 높으면 THEN 냉방을 강하게"</em>.<br><br>
      <strong>③ 집계 (Aggregation)</strong>: 여러 규칙이 동시에 발동될 때 그 결과들을 결합. 보통 최대값(Max) 또는 합집합 연산을 사용해 출력 멤버십 함수를 만든다.<br><br>
      <strong>④ 비퍼지화 (Defuzzification)</strong>: 집계된 퍼지 결과를 다시 구체적인 수치 값으로 변환. 일반적으로 <span class="keyw">무게중심(Center of Gravity, COG)</span> 방식 — 결과 멤버십 함수의 무게중심 위치를 출력값으로 사용.<br><br>
      <strong>냉난방기 제어 예시</strong>:
      <ul>
        <li><strong>입력</strong>: 온도 33℃, 습도 58%, 밀폐도 4</li>
        <li><strong>① 퍼지화</strong>: 온도 33 → μ_높다=0.8, μ_중간=0.2 / 습도 58 → μ_높다=0.6, μ_중간=0.4 / 밀폐도 4 → μ_보통=0.7</li>
        <li><strong>② 규칙 적용</strong>: 여러 규칙(예: "온도 높음 AND 습도 높음 → 냉방 강", "온도 중간 → 냉방 약" 등)에 따라 출력 결정</li>
        <li><strong>③ 집계</strong>: 각 규칙의 결과 결합. 출력 변수 "냉방 강도"의 종합 멤버십 함수 생성</li>
        <li><strong>④ 비퍼지화</strong>: 무게중심 계산으로 최종 출력값 도출. 예: 냉방 강도 = -2 (약하게 냉방)</li>
      </ul>
      <strong>의의</strong>: 사람의 자연언어 명령("좀 시원하게 해 줘")을 컴퓨터가 직접 처리할 수 있게 만든다. 1990년대 일본·한국 가전제품의 핵심 기술이었으며, 오늘날에도 차량 자동변속기·자동 노출 카메라·산업용 제어 시스템 등에 광범위하게 사용된다.
    </div>
  </div>

  <div class="nav-links">
    <a href="08주차_교과서.html">📚 교과서</a>
    <a href="08주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 09주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 9주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>9주차 문제집</h1>
    <div class="subtitle">모두 거짓말을 한다</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">인터넷과 웹에 대한 설명으로 <strong>옳지 않은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 인터넷은 TCP/IP 프로토콜 기반의 네트워크이다.</li>
      <li><span class="opt-num">②</span> 웹은 HTTP/HTTPS 프로토콜로 동작한다.</li>
      <li><span class="opt-num">③</span> 웹은 하이퍼텍스트(Hypertext)를 공유하는 시스템이다.</li>
      <li><span class="opt-num">④</span> 인터넷과 웹은 같은 의미이다.</li>
      <li><span class="opt-num">⑤</span> HTML은 웹페이지를 작성하는 언어이다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ 인터넷과 웹은 같은 의미이다</strong> (틀림)<br>
      <span class="alabel">해설</span> 인터넷이 더 큰 개념이며 웹은 인터넷 위에서 동작하는 한 서비스. 이메일·FTP 등도 인터넷에서 동작.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">빅데이터의 3V에 해당하지 <strong>않는</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> Volume (용량)</li>
      <li><span class="opt-num">②</span> Velocity (속도)</li>
      <li><span class="opt-num">③</span> Variety (다양성)</li>
      <li><span class="opt-num">④</span> Validity (타당성)</li>
      <li><span class="opt-num">⑤</span> 모두 3V에 해당</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ Validity (타당성)</strong><br>
      <span class="alabel">해설</span> 3V = <span class="keyw">Volume(용량) + Velocity(속도) + Variety(다양성)</span>. 추가로 4V(Veracity, 진실성)·5V(Value, 가치)가 있다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">데이터 마이닝(Data Mining)에 대한 강의의 비유로 가장 적절한 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 산을 찍어 그림 그리기</li>
      <li><span class="opt-num">②</span> 광산에 묻힌 금을 캐는 것</li>
      <li><span class="opt-num">③</span> <strong>흙을 금으로 만드는 것</strong> — 가치 없어 보이는 데이터에서 가치 창출</li>
      <li><span class="opt-num">④</span> 책을 인덱싱하는 것</li>
      <li><span class="opt-num">⑤</span> 신경망을 학습시키는 것</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 흙을 금으로 만드는 것</strong><br>
      <span class="alabel">해설</span> 머신러닝(②)은 묻힌 금 캐기, 데이터 마이닝(③)은 흙을 금으로 만드는 일. 강의에서 강조한 핵심 비유.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">"모두 거짓말을 한다(Everybody Lies)"의 핵심 메시지로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> SNS의 데이터는 가장 솔직하다.</li>
      <li><span class="opt-num">②</span> 모든 인공지능은 거짓말을 한다.</li>
      <li><span class="opt-num">③</span> 검색 키워드는 익명성 때문에 SNS보다 솔직한 데이터이다.</li>
      <li><span class="opt-num">④</span> 빅데이터는 신뢰할 수 없다.</li>
      <li><span class="opt-num">⑤</span> 통계 자체가 거짓이다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 검색 키워드는 익명성 때문에 SNS보다 솔직한 데이터이다</strong><br>
      <span class="alabel">해설</span> SNS에는 자기 이미지를 꾸며 올리지만, 구글 검색은 익명성 때문에 진짜 관심사가 드러난다. <span class="keyw">"솔직한 데이터"</span>가 빅데이터의 새로운 가치.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">상관관계와 인과관계에 대한 설명으로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 둘은 같은 의미이다.</li>
      <li><span class="opt-num">②</span> 상관관계는 항상 인과관계를 의미한다.</li>
      <li><span class="opt-num">③</span> 상관관계는 두 변수가 함께 변하는 통계적 관계이며, 인과관계는 한쪽이 다른 쪽의 원인인 관계로 둘은 다르다.</li>
      <li><span class="opt-num">④</span> 인과관계는 통계로만 결정된다.</li>
      <li><span class="opt-num">⑤</span> 빅데이터에서는 둘을 구분하지 않는다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 상관 ≠ 인과</strong><br>
      <span class="alabel">해설</span> 둘을 혼동하면 캐시 오닐의 책 제목 그대로 <span class="keyw">"대량살상 수학무기"</span>가 된다. AI 윤리의 핵심.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">인터넷과 웹의 차이를 한 줄씩 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>인터넷</strong>: TCP/IP 프로토콜 기반의 글로벌 네트워크 인프라.<br>
      <strong>웹(WWW)</strong>: 인터넷 위에서 HTTP/HTTPS 프로토콜로 하이퍼텍스트를 공유하는 정보 시스템.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">웹 브라우저로 검색할 때 검색 속도를 결정적으로 빠르게 하는 사전 처리 과정의 이름은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>인덱싱(Indexing)</strong>. 책의 "찾아보기"처럼 단어 위치를 미리 기록한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">페이지랭크(PageRank) 알고리즘을 만든 두 사람과 그들이 창업한 회사를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>래리 페이지(Larry Page)</strong>와 <strong>세르게이 브린(Sergey Brin)</strong>. 회사: <strong>Google</strong>. 1996년에 페이지랭크를 제안하고 1998년에 구글을 창립.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">빅데이터의 3V를 영어로 쓰고 각각의 의미를 한국어로 한 줄씩 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>Volume</strong> — 용량 (TB~PB)<br>
      ② <strong>Velocity</strong> — 속도 (실시간 처리 어려움)<br>
      ③ <strong>Variety</strong> — 다양성 (텍스트·이미지·영상·센서 등)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">데이터 마이닝과 머신러닝의 차이를 강의의 비유로 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>머신러닝</strong> = 광산에 이미 묻힌 금을 캐내는 일 (데이터에 존재하는 패턴 발견)<br>
      <strong>데이터 마이닝</strong> = <strong>흙을 금으로 만드는 일</strong> (쓸모없어 보이는 데이터에서 새 가치 창출)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">"모두 거짓말을 한다(Everybody Lies)"가 강조한 빅데이터의 4가지 새로운 특성을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>새로운 유형의 데이터</strong>(검색·SNS·IoT)<br>
      ② <strong>솔직한 데이터</strong>(익명성으로 인한 무의식적 행동)<br>
      ③ <strong>작은 집단까지 분석 가능</strong>(동·거리 단위)<br>
      ④ <strong>인과관계 검증 가능</strong>(실험적 데이터)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">상관관계(Correlation)와 인과관계(Causality)의 차이를 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>상관관계</strong>는 두 변수가 함께 변하는 통계적 관계이지만, <strong>인과관계</strong>는 한쪽이 다른 쪽의 직접적 <strong>원인</strong>인 관계이다. 상관관계가 있다고 인과관계가 있는 것은 아니다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">데이터 과학의 대표 기법 4가지를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>워드 클라우드(Word Cloud)</strong> — 단어 빈도 시각화<br>
      ② <strong>감성 분석(Sentiment Analysis)</strong> — 텍스트 감정 수치화<br>
      ③ <strong>Google NGram Viewer</strong> — 출판된 책의 단어 빈도 시대별 분석<br>
      ④ <strong>MDS(Multidimensional Scaling)</strong> — 다차원 데이터 2D/3D 시각화
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">웹 크롤러(Web Crawler)가 무엇이며 그 어원을 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>웹 크롤러</strong>는 인터넷의 그물(Web)을 <strong>거미처럼(Crawler) 돌아다니며</strong> 문서를 자동 수집하는 소프트웨어. 봇(Bot)이라고도 부른다. 검색 엔진의 인덱싱 작업의 첫 단계.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">SaaS(Software as a Service)가 무엇인지 한 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      소프트웨어를 패키지로 판매하지 않고 <strong>인터넷 기반 서비스로 제공</strong>하는 모델. 예: Gmail·Google Docs. 구글의 또 다른 혁신.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">인터넷·웹·웹 브라우저·검색엔진·웹 크롤러·인덱싱·페이지랭크의 관계를 정리해 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>인터넷(Internet)</strong>은 TCP/IP 프로토콜로 전 세계 컴퓨터를 연결한 글로벌 네트워크 인프라이다. <strong>월드와이드웹(WWW)</strong>은 그 인터넷 위에서 동작하는 정보 공유 시스템으로 HTTP/HTTPS 프로토콜과 HTML로 작성된 하이퍼텍스트를 주고받는다. 인터넷 ≠ 웹이며, 인터넷이 더 큰 개념이다.<br><br>
      <strong>웹 브라우저(Web Browser)</strong>는 사용자가 웹페이지를 보기 위한 소프트웨어(Chrome·Edge 등)이며, 사용자는 이를 통해 <span class="keyw">브라우징(Browsing)</span> — 강의 비유로 "소가 풀을 뜯듯" — 즉 웹을 탐색한다.<br><br>
      <strong>검색엔진(Search Engine)</strong>(Google 등)은 사용자가 원하는 정보를 빠르게 찾도록 도와준다. 이를 위해 검색엔진 뒤에는 두 가지 사전 작업이 있다:
      <ul>
        <li>① <strong>웹 크롤러(Web Crawler)</strong>가 거미처럼 웹의 그물을 돌아다니며 문서를 <span class="keyw">크롤링(Crawling)</span>해 수집한다.</li>
        <li>② 수집된 페이지에 <span class="keyw">인덱싱(Indexing)</span> — 책의 "찾아보기"처럼 어떤 단어가 어느 페이지의 어느 위치에 있는지 기록 — 을 적용해 검색 속도를 결정적으로 높인다.</li>
      </ul>
      마지막으로 검색 결과에 <strong>순위</strong>를 매겨야 하는데, 구글의 <strong>페이지랭크(PageRank)</strong> 알고리즘(1996, 래리 페이지·세르게이 브린)이 핵심이다. 단순히 단어 빈도뿐 아니라 <span class="keyw">"다른 신뢰할 만한 페이지가 이 페이지를 얼마나 가리키는가"</span>를 고려해 권위를 측정한다. 이 데이터 중심 사고가 구글의 성공 비결이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">빅데이터(Big Data)의 정의와 3V를 설명하고, 빅데이터가 단순히 "큰 데이터"가 아닌 이유를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>빅데이터(Big Data)</strong>는 기존의 데이터 처리 방법으로는 다룰 수 없을 만큼 <span class="keyw">크고·빠르고·다양한</span> 데이터 집합이다. 단순히 데이터의 크기가 크다는 의미가 아니다.<br><br>
      <strong>3V — 빅데이터의 핵심 특성</strong>:
      <ul>
        <li>① <strong>Volume(용량)</strong>: 테라바이트(TB)~페타바이트(PB) 규모. 기존 저장 시스템으로 감당하기 어렵다.</li>
        <li>② <strong>Velocity(속도)</strong>: SNS 게시물·IoT 센서 데이터·웹 로그 등이 실시간으로 처리할 수 없을 만큼 빠르게 쌓인다.</li>
        <li>③ <strong>Variety(다양성)</strong>: 정형 데이터(데이터베이스의 표)뿐 아니라 텍스트·이미지·음성·영상·소셜 미디어·센서 등 다양한 형식의 비정형·반정형 데이터가 혼재한다.</li>
      </ul>
      이 3V 중 어느 하나만 충족해도 빅데이터로 보지 않으며, <strong>세 조건을 모두 충족하는 경우</strong>를 빅데이터라 한다. 추가로 4V(Veracity, 진실성)·5V(Value, 가치)도 논의된다.<br><br>
      <strong>"단순히 큰 데이터가 아닌 이유"</strong>: 1TB짜리 영화 파일 하나는 매우 크지만 빅데이터가 아니다. 단일 형식이고 정적이며 기존 시스템으로도 충분히 처리 가능하기 때문이다. 반면 매초 수만 개씩 생성되는 수억 명의 SNS 게시물은 작은 메시지의 모음이지만 3V를 모두 충족하므로 빅데이터다. 즉 빅데이터의 본질은 <span class="keyw">기존 처리 방법으로는 다룰 수 없는 새로운 도전</span>이며, 이를 해결하기 위해 분산 처리(Hadoop·Spark)·NoSQL 데이터베이스·실시간 스트리밍 처리 같은 새로운 기술들이 등장했다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">데이터 마이닝(Data Mining)과 머신러닝(Machine Learning)의 차이를 강의의 비유와 함께 설명하고, 강태원 교수가 데이터 마이닝을 "국가 생존 경쟁"이라 부른 이유를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>강의의 광산 비유</strong>:
      <ul>
        <li><strong>머신러닝(Machine Learning)</strong>은 <span class="keyw">광산에 이미 묻힌 금을 캐내는 일</span>이다. 데이터 안에 이미 패턴이 존재하며, 그 패턴을 알고리즘으로 발견·추출하는 작업이다.</li>
        <li><strong>데이터 마이닝(Data Mining)</strong>은 <span class="keyw">"흙을 금으로 만드는 일"</span>이다. 즉 표면적으로 가치 없어 보이는 데이터(흙)에서 새로운 가치(금)를 창출해 내는 더 높은 수준의 작업이다. 단순히 패턴을 발견하는 것을 넘어 <em>어떤 데이터에서 어떤 가치를 만들 수 있을지 발상하고 검증</em>하는 창의적 과정.</li>
      </ul>
      <strong>"국가 생존 경쟁"인 이유</strong>: 모든 나라가 같은 데이터(예: 검색 로그·SNS·IoT 센서 데이터)에 접근할 수 있는 시대에, <span class="keyw">그 데이터에서 새로운 가치를 발굴해 내는 능력</span>이 곧 국가 경쟁력이 된다. 어떤 나라가 "쓰레기"라고 생각해 버린 데이터에서 다른 나라가 가치를 발견해 내면, 첫 번째 나라는 그 부가가치를 두 번째 나라로부터 비싸게 구매해야 한다. 데이터 마이닝 능력이 곧 산업·경제 패권으로 이어지는 시대인 것이다.<br><br>
      대표적 예: 구글이 검색 데이터에서 광고·트렌드 분석 등 막대한 가치를 만들어 내고, 이로 인해 전 세계가 그들의 서비스에 의존하게 된 현상. 이는 단순한 검색 알고리즘이 아니라 <span class="keyw">데이터를 가치로 변환하는 데이터 마이닝 능력</span>의 결과다. 따라서 학생들은 단순한 머신러닝 도구 사용을 넘어, "어떤 데이터에서 어떤 가치를 만들 수 있을지" 창의적으로 사고하는 데이터 마이닝 능력을 길러야 한다는 것이 강의의 메시지다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">"모두 거짓말을 한다(Everybody Lies)"가 강조한 빅데이터의 4가지 특성을 설명하고, "왜 검색 키워드 데이터가 SNS 데이터보다 솔직한가"를 익명성 관점에서 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      Seth Stephens-Davidowitz의 책 <em>"Everybody Lies"</em>(2017)가 강조한 빅데이터의 4가지 새로운 특성:<br><br>
      ① <strong>새로운 유형의 데이터</strong>: 과거에는 활용할 수 없던 데이터들 — 검색 로그·SNS·IoT 센서·앱 사용 기록 등. 인터넷·웹의 발전이 가져온 새로운 데이터 자원.<br><br>
      ② <strong>솔직한 데이터(Honest Data)</strong>: <span class="keyw">불특정 다수의 무의식적 행동</span>에서 나온 데이터이므로 의도적 거짓이 거의 포함되지 않는다.<br><br>
      ③ <strong>작은 집단까지 분석 가능</strong>: 과거에는 도·시 단위로만 통계 가능했으나 이제는 동·거리·개인 단위까지 세밀 분석 가능. 표본 조사가 아닌 <em>전수 조사</em>에 가까운 데이터 확보.<br><br>
      ④ <strong>인과관계 검증 가능</strong>: 단순한 통계적 상관관계를 넘어, A/B 테스트 같은 실험적 데이터로 인과관계를 직접 검증할 수 있는 기회가 늘어남.<br><br>
      <strong>왜 검색 키워드가 SNS보다 솔직한가</strong>:
      <ul>
        <li><strong>SNS의 거짓</strong>: 페이스북·인스타그램에서 사람들은 자기 이미지를 꾸민다. 행복한 사진, 멋진 여행지, 화려한 성취 — 진짜 모습이 아니라 <span class="keyw">남에게 보이고 싶은 모습</span>을 올린다. 이는 사회적 동기에 의한 의도적 편향이며, 이런 데이터로는 사람들의 진짜 관심·고민·욕망을 알 수 없다.</li>
        <li><strong>검색의 솔직</strong>: 반면 구글 검색은 <span class="keyw">익명성</span>이 보장되어 있다. "내가 무엇을 검색했는지" 다른 사람에게 보이지 않으므로 사람들은 자기 진짜 관심사·고민·질병·욕망을 그대로 입력한다. 예: 페이스북에는 "행복한 결혼생활" 사진을 올리면서도 검색창에는 "이혼 절차"를 입력하는 식이다. 이렇게 익명성이 사람을 솔직하게 만든다.</li>
      </ul>
      이 통찰의 의의는 빅데이터 시대에 <strong>"무엇을 보았는가(SNS)"가 아니라 "무엇을 했는가(검색·구매·클릭)"</strong>가 진실에 더 가깝다는 점이다. 그래서 데이터 마이닝과 데이터 사이언스에서 검색 로그·구매 기록 같은 행동 데이터(Behavioral Data)가 매우 가치 있는 자원으로 평가된다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">상관관계(Correlation)와 인과관계(Causality)를 혼동했을 때 발생할 수 있는 위험을 설명하고, AI 윤리와 어떻게 연결되는지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>정의 차이</strong>: 상관관계(Correlation)는 두 변수가 함께 변하는 통계적 관계를 의미한다. 인과관계(Causality)는 한쪽이 다른 쪽의 <span class="keyw">직접적 원인</span>인 관계를 의미한다. 상관관계가 있다고 해서 반드시 인과관계가 있는 것은 아니다.<br><br>
      <strong>혼동의 위험 — 구체적 사례</strong>:
      <ul>
        <li>① <strong>주가와 출산율의 우연적 상관</strong>: 두 지표가 우연히 함께 변할 때 "주가가 오르면 출산율이 오른다"고 결론짓는 것. 사실 둘은 무관하거나 다른 변수(경기·정책 등)의 영향일 수 있다.</li>
        <li>② <strong>AI 채용 시스템의 차별</strong>: 과거 데이터에서 "남성 지원자가 더 자주 채용됐다"는 상관관계를 학습한 AI가 "남성을 채용하는 게 옳다"는 인과관계로 잘못 해석. 사실은 과거의 차별이 데이터에 반영된 결과인데도 AI는 이를 객관적 진실로 받아들임.</li>
        <li>③ <strong>의료 진단</strong>: 어떤 증상과 질병의 상관이 있다고 해서 그 증상이 원인이라고 단정하면 잘못된 치료가 이루어질 수 있다(8주차 베이즈 정리의 거짓 양성 사례).</li>
      </ul>
      <strong>"대량살상 수학무기(Weapons of Math Destruction)"</strong>: 캐시 오닐(Cathy O'Neil)의 책 제목. 알고리즘이 상관관계를 인과관계로 착각해 만든 모델이 사회에 광범위한 피해를 주는 현상을 의미. 예: 신용 점수, 형사 양형 보조 시스템, 채용 시스템 등에서 인종·성별·소득에 따른 차별이 알고리즘에 코드화된 채 작동.<br><br>
      <strong>AI 윤리와의 연결</strong>:
      <ul>
        <li>① <strong>편향된 학습 데이터</strong>: 7주차 딥러닝의 한계인 블랙박스 문제와 결합되면, AI가 왜 그런 결정을 내렸는지 설명하지 못한 채 차별을 재생산할 수 있다.</li>
        <li>② <strong>사회적 영향</strong>: AI가 보편화될수록 작은 통계적 오류가 수백만 명의 삶에 영향을 미친다. 채용·대출·의료·교육·법률 — 모든 영역에서.</li>
        <li>③ <strong>책임의 소재</strong>: "알고리즘이 그렇게 결정했다"는 변명이 통하지 않게 하려면 인간이 상관과 인과를 정확히 구분하고 검증해야 한다.</li>
      </ul>
      <strong>1주차의 메시지와의 연결</strong>: "인공지능이 인문학"이라는 명제가 다시 중요해진다. 상관관계와 인과관계의 구분, 그것을 윤리적으로 적용하는 능력은 단순한 공학·통계 지식이 아니라 <span class="keyw">인간과 사회에 대한 깊은 이해</span>가 필요한 인문학적 능력이다. 따라서 AI 시대일수록 데이터 문해력(Data Literacy)과 비판적 사고가 모든 시민의 필수 역량이 된다.
    </div>
  </div>

  <div class="nav-links">
    <a href="09주차_교과서.html">📚 교과서</a>
    <a href="09주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 10주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 10주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>10주차 문제집</h1>
    <div class="subtitle">이 영화 보세요!</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">인공지능 / 머신러닝 / 신경망 / 딥러닝의 포함 관계로 옳은 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> AI ⊂ ML ⊂ NN ⊂ DL</li>
      <li><span class="opt-num">②</span> AI ⊃ ML ⊃ NN ⊃ DL</li>
      <li><span class="opt-num">③</span> DL ⊃ NN ⊃ ML ⊃ AI</li>
      <li><span class="opt-num">④</span> 네 개는 모두 같은 의미이다</li>
      <li><span class="opt-num">⑤</span> ML과 NN은 독립적이다</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② AI ⊃ ML ⊃ NN ⊃ DL</strong><br>
      <span class="alabel">해설</span>인공지능이 가장 큰 범위. 머신러닝은 AI의 한 분야, 신경망은 ML의 한 종류, 딥러닝은 깊은 신경망. 단 오늘날 딥러닝이 너무 커져서 일반인에게는 DL=AI로 통용되기도 함.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">"회귀(Regression)"의 정의로 가장 정확한 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 어디에 속하는지 가려내는 것</li>
      <li><span class="opt-num">②</span> 덩어리를 묶어내는 것</li>
      <li><span class="opt-num">③</span> 관계식을 알아내는 것</li>
      <li><span class="opt-num">④</span> 가중치를 수정하는 것</li>
      <li><span class="opt-num">⑤</span> 데이터를 가공하는 것</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 관계식을 알아내는 것</strong><br>
      <span class="alabel">해설</span>회귀 = <span class="keyw">관계식 찾기</span>(예: 공부 시간 ↔ 학점). ①은 분류, ②는 군집화, ④는 학습.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">k-Means 알고리즘에 대한 설명으로 <strong>옳지 않은</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 비지도학습 알고리즘이다.</li>
      <li><span class="opt-num">②</span> K개의 덩어리가 있다고 가정하고 묶는다.</li>
      <li><span class="opt-num">③</span> 무게중심(평균)을 반복적으로 갱신한다.</li>
      <li><span class="opt-num">④</span> K값(덩어리 개수)을 알고리즘이 자동으로 정한다.</li>
      <li><span class="opt-num">⑤</span> 변동이 없을 때까지 반복한다.</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ K값을 알고리즘이 자동 결정</strong> (틀림)<br>
      <span class="alabel">해설</span><span class="keyw">K값은 사람이 미리 정해야 한다</span> — 이게 k-Means의 큰 한계. 어떤 K가 적절한지 알기 어렵다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">스팸 메일 필터에서 정상 메일(스팸이 아닌 메일)을 부르는 머신러닝 용어는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 정메일(Normal Mail)</li>
      <li><span class="opt-num">②</span> 햄(Ham)</li>
      <li><span class="opt-num">③</span> 화이트(White Mail)</li>
      <li><span class="opt-num">④</span> 클린(Clean Mail)</li>
      <li><span class="opt-num">⑤</span> 베이즈(Bayes)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 햄(Ham)</strong><br>
      <span class="alabel">해설</span>스팸이 가공육이라면 햄은 가공되지 않은 자연 그대로의 고기라는 비유에서 유래.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">협업 필터링(Collaborative Filtering)에서 가장 핵심인 작업은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 데이터 크롤링</li>
      <li><span class="opt-num">②</span> 유사성(Similarity) 측정</li>
      <li><span class="opt-num">③</span> 가중치 학습</li>
      <li><span class="opt-num">④</span> 백프로퍼게이션</li>
      <li><span class="opt-num">⑤</span> 합성곱 연산</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 유사성 측정</strong><br>
      <span class="alabel">해설</span>강의 강조: "유사성 측정에서 시작해서 그것으로 끝난다". 유클리드 거리·상관계수 등 측정 방법.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">머신러닝의 3대 알고리즘 분류(회귀·분류·군집화) 각각의 한 줄 정의를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>회귀</strong> = 관계식을 알아내는 것<br>
      ② <strong>분류</strong> = 어디에 속하는지 가려내는 것<br>
      ③ <strong>군집화</strong> = 덩어리를 묶어내는 것
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">지도학습과 비지도학습의 차이를 한 줄로 쓰고, 각각의 대표 알고리즘을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>지도학습</strong>: 정답(라벨)이 있는 학습. 회귀·분류.<br>
      <strong>비지도학습</strong>: 정답이 없는 학습. 군집화.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">머신러닝의 두 진영(연결주의·기호주의)에서 사용하는 대표 도구(라이브러리)를 각각 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      연결주의: <strong>TensorFlow, Keras</strong> (딥러닝)<br>
      기호주의: <strong>Scikit-learn</strong> (분류·회귀·군집화·KNN 등)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">베이즈 정리 기반 스팸 필터의 공식을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>P(스팸|단어) = P(단어|스팸) × P(스팸) / P(단어)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">k-Means 알고리즘의 작동 순서 4단계를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① K개 중심점을 임의로 배치<br>
      ② 각 데이터를 가장 가까운 중심에 소속시킴<br>
      ③ 각 그룹의 무게중심(평균)으로 중심점 이동<br>
      ④ 변동이 없을 때까지 ②~③ 반복
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">k-Means 알고리즘의 가장 큰 한계는?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>K값(덩어리 개수)을 사람이 미리 정해야 한다.</strong> 어떤 K가 적절한지 알기 어려움.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">추천 시스템의 두 가지 관점을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>사용자 기반(User-based)</strong>: 취향이 비슷한 사람이 본 것을 추천<br>
      ② <strong>아이템 기반(Item-based)</strong>: 이 책을 산 사람이 본 영화 추천 식
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">협업 필터링에서 사용하는 유사성 측정 방법 4가지를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>유클리드 거리(Euclidean Distance)</strong><br>
      ② <strong>상관계수(Correlation Coefficient)</strong><br>
      ③ 코사인 거리(Cosine Distance)<br>
      ④ 맨해튼 거리(Manhattan Distance)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">협업 필터링의 추천 점수 계산식을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>추천 점수 = Σ(유사성 × 평점) / Σ유사성</strong><br>
      = Σ(Sᵢ × Mᵢ) / Σ Sᵢ. 가까운 사람들의 평점을 비율적으로 반영.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">군집화 후 만들어진 덩어리에 이름을 붙이는 작업을 무엇이라 부르는가? (강의 강조 표기법으로)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>레이블링(Labeling)</strong> — 교수님 강조: "라벨링이 아니라 레이블링".
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">분류(Classification)와 군집화(Clustering)의 차이를 설명하시오. (입사 면접 단골 질문)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>분류(Classification)</strong>는 데이터가 어느 클래스에 속하는지 결정하는 작업이며, <span class="keyw">정답(라벨)이 미리 주어진 지도학습</span>이다. 예: "이 메일은 스팸인가 햄인가?" / "이 학생은 몇 반인가?". 베이즈 정리, 결정 트리, KNN, SVM 등이 사용된다.<br><br>
      <strong>군집화(Clustering)</strong>는 비슷한 성질의 데이터를 한 묶음(Cluster)으로 모으는 작업이며, <span class="keyw">정답이 없는 비지도학습</span>이다. 예: "고객을 비슷한 유형끼리 묶기". k-Means, 계층적 알고리즘 등이 사용된다.<br><br>
      <strong>핵심 차이</strong>: 분류는 "어디에 속하느냐"를 정답이 있는 상태에서 가려내고, 군집화는 "비슷한 것끼리 묶기"를 정답 없이 수행한다. 강의 비유로, 갓 태어난 아기도 "얼음"이라는 단어 없이 흰 덩어리를 한 묶음으로 인식할 수 있는 게 군집화 — 분류보다 더 낮은 수준의 인지 작용이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">머신러닝과 데이터 마이닝(Data Mining)의 관계와 차이를 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      두 분야는 사용하는 방법(method)이 많이 겹치며 상당히 중복(overlap)된다. 그러나 초점이 다르다.<br><br>
      <strong>머신러닝(Machine Learning)</strong>은 <span class="keyw">예측(Prediction)</span>에 초점을 둔다. 학습 데이터로부터 모델을 만들어 새 데이터에 대한 결과를 예측하는 학문/과학적 방법이다.<br><br>
      <strong>데이터 마이닝(Data Mining)</strong>은 이전에 알지 못한 <span class="keyw">새로운 사실(Unknown Property)</span>을 발견하는 데 초점을 둔다. 9주차 강의에서 강조했듯 "쓸모없는 광석을 금으로 만드는 행위" — 가치 없어 보이는 데이터에서 새 가치를 창출.<br><br>
      <strong>구체적 예</strong>: 머신러닝은 "스팸 메일을 예측하는 모델 만들기", 데이터 마이닝은 "맥주를 사는 사람이 안주도 산다는 사실 발견" — 후자의 발견 후 마트는 일부러 맥주와 안주를 멀리 두어 동선을 늘릴 수 있다. 둘은 종종 함께 사용되며 현대 데이터 과학의 양대 축이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">선형 회귀(Linear Regression)를 전통적 방법(최소자승법)과 신경망 방법으로 비교하여 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>선형 회귀</strong>는 입력과 출력 사이의 직선 관계 <code>Y = mx + b</code>를 찾는 작업이다. m(기울기)와 b(절편)를 구해야 한다.<br><br>
      <strong>전통적 방법 — 최소자승법(Least Squares)</strong>: <span class="keyw">미적분</span>을 이용해 데이터와 직선 사이 오차 제곱의 합을 최소화하는 m, b를 공식적으로 계산한다. 통계학·수학의 정통 방법이며 결과가 명확하다.<br><br>
      <strong>신경망 방법</strong>: 데이터(입력 x, 출력 y의 쌍)만 주면 신경망이 <span class="keyw">오류역전파(Backpropagation)</span> 학습으로 가중치(m, b에 해당)를 자동으로 수정해가며 관계식을 찾아낸다. 6주차에서 배운 경사하강법이 이를 가능케 한다.<br><br>
      <strong>비교</strong>: 최소자승법은 빠르고 정확하지만 복잡한 비선형 관계는 다루기 어렵다. 신경망은 시간이 더 걸리지만 다층 신경망으로 매우 복잡한 비선형 관계도 학습 가능 — 그래서 오늘날 딥러닝이 강력하다. 두 방법은 같은 회귀 문제를 다른 패러다임으로 푸는 것이며, 단순한 선형 회귀라면 최소자승법이, 복잡한 데이터라면 신경망이 적합하다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">k-Means 알고리즘의 작동 원리를 단계별로 설명하고, 이 알고리즘의 한계를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>k-Means</strong>는 K개의 덩어리가 있다고 <span class="keyw">가정</span>하고 그 개수만큼 데이터를 묶는 군집화 알고리즘이다(k=덩어리 개수, means=평균).<br><br>
      <strong>작동 4단계</strong>:
      <ul>
        <li>① K개 중심점(Centroid)을 임의(랜덤)로 배치한다.</li>
        <li>② 각 데이터에서 K개 중심까지 거리를 측정하고, 가장 가까운 중심에 소속시킨다.</li>
        <li>③ 각 그룹의 무게중심(소속 데이터의 평균 좌표)으로 중심점을 이동한다.</li>
        <li>④ 중심점이 더 이상 움직이지 않을 때까지 ②~③을 반복한다.</li>
      </ul>
      <strong>장점</strong>: K값만 정해 주면 매우 수월하게 군집화 가능. 구현이 단순.<br><br>
      <strong>한계</strong>:
      <ul>
        <li><span class="keyw">K값을 사람이 미리 정해야 한다</span> — 어떤 K가 적절한지 알기 어렵다. 이게 가장 큰 한계.</li>
        <li>초기 중심점 위치(랜덤)에 따라 결과가 달라질 수 있다.</li>
        <li>구형(원형)이 아닌 복잡한 모양의 클러스터에는 약하다.</li>
        <li>거리 계산이 가능한 수치형 데이터에만 적용 가능.</li>
      </ul>
      <strong>대안</strong>: 계층적 알고리즘(Hierarchical)은 처음에 모든 데이터를 각자 한 덩어리로 시작해서 가까운 것끼리 묶어가며 K를 줄여나간다. 또는 엘보(Elbow) 방법으로 적절한 K값을 찾는 기법도 있다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">협업 필터링(Collaborative Filtering)의 원리를 설명하고, 추천 점수 계산식이 단순히 "가장 유사한 사람 1명의 평점을 그대로 추천"하는 것이 아닌 이유를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>협업 필터링</strong>은 추천 시스템의 대표 알고리즘으로, "<span class="keyw">너랑 취향이 비슷한 사람들이 좋아한 것을 너에게도 추천</span>"한다는 원리이다. 핵심은 <strong>유사성(Similarity) 측정</strong> — 강의 강조: "유사성 측정에서 시작해 그것으로 끝난다".<br><br>
      <strong>유사성 측정 방법</strong>:
      <ul>
        <li><strong>유클리드 거리(Euclidean Distance)</strong>: 두 사용자의 평점 벡터 사이의 직선 거리. 절대값이 중요할 때.</li>
        <li><strong>상관계수(Correlation, R)</strong>: 경향성/패턴이 중요할 때(한 명은 모든 영화를 후하게 주고 한 명은 박하게 주지만, 좋아하는 영화 순위는 같을 때).</li>
        <li>코사인 거리·맨해튼 거리 등.</li>
      </ul>
      <strong>추천 점수 계산식</strong>:
      <div style="text-align:center; font-family:serif; margin:10px 0;">추천 점수 = Σ(Sᵢ × Mᵢ) / Σ Sᵢ</div>
      Sᵢ = i번 사용자와의 유사성, Mᵢ = i번 사용자의 해당 영화 평점.<br><br>
      <strong>왜 가장 유사한 사람 1명만으로 추천하지 않는가?</strong>
      <ul>
        <li>한 사람만 보면 <span class="keyw">우연이나 특이한 취향</span>에 끌려갈 수 있다.</li>
        <li>가장 유사한 사람도 모든 영화를 다 본 게 아니다 — 해당 영화에 평점 없을 수도.</li>
        <li>여러 명의 평점을 유사성으로 <span class="keyw">가중 평균</span>하면 더 안정적이고 일반화된 추천이 나온다.</li>
        <li>이는 <strong>집단지능(Collective Intelligence)</strong> 원리 — 9주차 페이지랭크와 같은 맥락. 다수의 데이터에서 더 신뢰할 만한 결론.</li>
      </ul>
      넷플릭스·아마존이 막대한 매출을 올리는 비결이 바로 이 정교한 추천 시스템이며, 이는 단순히 알고리즘이 아니라 <strong>데이터 시대의 비즈니스 모델</strong>이다.
    </div>
  </div>

  <div class="nav-links">
    <a href="10주차_교과서.html">📚 교과서</a>
    <a href="10주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 11주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 11주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>11주차 문제집</h1>
    <div class="subtitle">개미의 길찾기</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">자연 컴퓨팅의 3대 범주에 해당하지 <strong>않는</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 자연에서 배우기 (Learning from Nature)</li>
      <li><span class="opt-num">②</span> 자연 합성하기 (Synthesizing Nature)</li>
      <li><span class="opt-num">③</span> 자연 사용하기 (Using Nature)</li>
      <li><span class="opt-num">④</span> 자연 파괴하기 (Destroying Nature)</li>
      <li><span class="opt-num">⑤</span> 해당 사항 없음</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ 자연 파괴하기</strong> (그런 범주는 없음)<br>
      <span class="alabel">해설</span>자연 컴퓨팅의 3대 범주 = <span class="keyw">자연에서 배우기 / 자연 합성하기 / 자연 사용하기</span>.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">개미가 길에 남기는 화학 물질의 이름과, 시간이 지나면서 발생하는 핵심 현상으로 옳은 짝은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 페로몬 (Pheromone) — 증발 (Evaporation)</li>
      <li><span class="opt-num">②</span> 호르몬 (Hormone) — 합성 (Synthesis)</li>
      <li><span class="opt-num">③</span> 페로몬 (Pheromone) — 확산 (Diffusion)</li>
      <li><span class="opt-num">④</span> 도파민 (Dopamine) — 증발 (Evaporation)</li>
      <li><span class="opt-num">⑤</span> 항원 (Antigen) — 항체 형성</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>① 페로몬 — 증발</strong><br>
      <span class="alabel">해설</span>페로몬은 시간이 지나면 <span class="keyw">증발</span>한다. 이게 ACO의 핵심 — 긴 길은 증발이 많아 약해지고, 짧은 길은 누적 강화된다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">개체가 환경을 바꿈으로써 다른 개체와 간접적으로 소통하는 현상을 무엇이라 하는가?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 자기 조직화 (Self-Organization)</li>
      <li><span class="opt-num">②</span> 스티그머지 (Stigmergy)</li>
      <li><span class="opt-num">③</span> 양자 중첩 (Superposition)</li>
      <li><span class="opt-num">④</span> 증발 (Evaporation)</li>
      <li><span class="opt-num">⑤</span> 휴리스틱 (Heuristic)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 스티그머지</strong><br>
      <span class="alabel">해설</span>개미가 페로몬으로 환경을 바꿔 다른 개미와 소통하는 것. 강의 비유: "내가 말하면 공기가 진동하여 환경이 달라지는 것과 같은 원리".
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">DNA 컴퓨팅의 진법과 디지털 컴퓨터의 진법으로 옳은 짝은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 디지털 = 4진법, DNA = 2진법</li>
      <li><span class="opt-num">②</span> 디지털 = 2진법, DNA = 4진법(A·G·C·T)</li>
      <li><span class="opt-num">③</span> 디지털 = 10진법, DNA = 4진법</li>
      <li><span class="opt-num">④</span> 둘 다 2진법</li>
      <li><span class="opt-num">⑤</span> DNA = 16진법</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 디지털 = 2진법, DNA = 4진법</strong><br>
      <span class="alabel">해설</span>DNA의 4진법 = <span class="keyw">A(아데닌), G(구아닌), C(시토신), T(티민)</span>. 1g에 약 10억 TB 저장 가능.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">3차시 부제 "누가 지시하는가!"의 답은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 우두머리 개미가 지시한다</li>
      <li><span class="opt-num">②</span> 페로몬이 지시한다</li>
      <li><span class="opt-num">③</span> 아무도 지시하지 않는다 — 자기 조직화</li>
      <li><span class="opt-num">④</span> 자연의 신이 지시한다</li>
      <li><span class="opt-num">⑤</span> 환경이 지시한다</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 아무도 지시하지 않는다 — 자기 조직화</strong><br>
      <span class="alabel">해설</span><span class="keyw">자기 조직화(Self-Organization)</span>가 자연의 핵심 특징. 페이지랭크·딥러닝 가중치·인간 뇌 모두 같은 원리.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">자연 컴퓨팅의 3대 범주를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>자연에서 배우기 (Learning from Nature)</strong><br>
      ② <strong>자연 합성하기 (Synthesizing Nature)</strong><br>
      ③ <strong>자연 사용하기 (Using Nature)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">자연에서 배우기에 속하는 컴퓨팅 갈래를 4가지 이상 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>뉴럴 컴퓨팅(Neural Computing)</strong> — 뇌·뉴런<br>
      ② <strong>진화 컴퓨팅(Evolutionary Computing)</strong> — 자연 선택<br>
      ③ <strong>군집 지능(Swarm Intelligence)</strong> — 개미·꿀벌<br>
      ④ <strong>면역 컴퓨팅</strong> — 항원·항체<br>
      ⑤ <strong>세포 자동자(Cellular Automata)</strong> — 13주차에서 자세히<br>
      <span class="alabel" style="color:#c1376b;">⚠️ 주의</span>
      PSO(입자 군집 최적화)는 강의 범위 외 외부 지식. 강의에서는 위 5가지만 다룸.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">자연 컴퓨팅의 핵심 철학인 "이웃 정보 활용"의 의미를 한 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>개체가 자신의 전체 환경을 파악할 필요 없이, 주변(이웃)의 지역 정보만으로 행동을 결정하는 것.</strong><br>
      개미가 페로몬으로, 보이드가 주변 새들만 보고 행동하는 것이 모두 이 원리. 자기 조직화(Self-Organization)의 핵심.<br>
      <span class="alabel" style="color:#c1376b;">⚠️ 변경 안내</span>
      원래 PSO 비교 문제였으나 PSO는 강의 범위 외라 자연 컴퓨팅 일반 철학 문제로 교체.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">L-시스템의 4가지 기호와 그 의미를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>F</strong> = 전진 + 흔적 남김 / <strong>f</strong> = 전진 (흔적 없음) / <strong>+</strong> = 좌회전 / <strong>−</strong> = 우회전
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">DNA의 4가지 염기를 영어 약자와 한국어로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>A</strong>(Adenine, 아데닌) / <strong>G</strong>(Guanine, 구아닌) / <strong>C</strong>(Cytosine, 시토신) / <strong>T</strong>(Thymine, 티민)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">양자 컴퓨팅의 기본 단위 이름과, 4개 단위로 동시에 표현할 수 있는 상태의 수를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      기본 단위: <strong>큐비트 (Qubit)</strong><br>
      4개 큐비트 = <strong>2⁴ = 16가지 상태 동시 표현</strong> (기존 컴퓨터는 16가지 중 1가지만)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">개미 군집 최적화(ACO)의 3대 초매개변수를 기호와 의미로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>α (alpha)</strong> = 페로몬 가중치<br>
      <strong>β (beta)</strong> = 거리/휴리스틱 가중치<br>
      <strong>ρ (rho)</strong> = 페로몬 증발 상수 (Evaporation Rate)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">"스티그머지(Stigmergy)"의 정의를 한 문장으로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      개체가 <strong>환경을 바꿈으로써</strong> 다른 개체와 간접적으로 소통하는 것 (개미의 페로몬이 대표).
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">자기 조직화(Self-Organization)의 정의를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>중앙 지시자 없이 저절로 질서가 형성</strong>되는 현상. 자연의 핵심 특징. ACO·페이지랭크·딥러닝·인간 뇌가 모두 이 원리.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">ACO가 특히 강력한 문제의 종류는 무엇이며, 그 이유는?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>동적 환경(Dynamic Environment)의 NP 문제 (예: TSP)</strong>에 강력. 길이 바뀌어도 페로몬을 재구성하며 적응한다. 전통 알고리즘은 처음부터 다시 계산해야 하지만 ACO는 적응적.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">자연 컴퓨팅의 3대 범주를 설명하고, 각 범주에 해당하는 대표 사례를 1개 이상씩 들어 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>자연 컴퓨팅(Natural Computing)</strong>은 자연 현상에서 영감을 얻거나, 자연을 합성·이용하는 컴퓨팅 기술 전체를 의미한다. 세 가지 범주로 나뉜다.<br><br>
      <strong>① 자연에서 배우기 (Learning from Nature)</strong>: 자연 현상에서 아이디어를 가져와 우리의 문제를 해결하는 기술을 만든다.
      <ul>
        <li>뉴럴 컴퓨팅(딥러닝): 뇌의 뉴런 작동 방식 모방</li>
        <li>진화 컴퓨팅(유전 알고리즘): 자연 선택·다윈 진화 모방</li>
        <li>군집 지능(ACO): 개미·꿀벌의 집단 행동 모방</li>
        <li>면역 컴퓨팅: 항원-항체 반응을 보안에 활용</li>
      </ul>
      <strong>② 자연 합성하기 (Synthesizing Nature)</strong>: 컴퓨터 기술로 자연/생명을 합성하여 더 잘 이해·활용한다.
      <ul>
        <li>L-시스템: 식물 성장을 모방한 프랙탈로 게임·영화의 숲을 생성</li>
        <li>칼 심스의 가상 생명체(1994): 신경망+GA로 학습</li>
      </ul>
      <strong>③ 자연 사용하기 (Using Nature)</strong>: 자연에 있는 물질·현상을 직접 컴퓨팅에 활용한다.
      <ul>
        <li>DNA 컴퓨팅: A·G·C·T의 4진법, 1g에 10억 TB</li>
        <li>양자 컴퓨팅: 양자 중첩으로 큐비트가 동시 다중 상태</li>
      </ul>
      이 분류는 <span class="keyw">"인공지능 역시 자연 지능의 합성"</span>이라는 큰 관점을 제공하며, 11~14주차의 모든 후속 주제를 묶는 지도 역할을 한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">개미 군집 최적화(ACO)의 작동 원리를 설명하고, "왜 ACO가 동적 환경에서 강력한가"를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>ACO 작동 원리</strong>:
      <ul>
        <li>① 개미가 길을 갈 때 <span class="keyw">페로몬(Pheromone)</span>을 남긴다.</li>
        <li>② 시간이 지나면 페로몬은 <span class="keyw">증발(Evaporation)</span>한다.</li>
        <li>③ <strong>짧은 길</strong>: 왕복 시간이 짧아 페로몬이 계속 누적·강화됨.</li>
        <li>④ <strong>긴 길</strong>: 왕복이 오래 걸려 페로몬이 많이 증발되어 약해짐.</li>
        <li>⑤ 후속 개미들은 페로몬이 강한 짧은 길로 몰림 → <strong>빈익빈 부익부 강화</strong>로 자연스럽게 최단 경로 수렴.</li>
      </ul>
      <strong>인공 ACO의 매개변수</strong>:
      <ul>
        <li>α(알파): 페로몬 가중치</li>
        <li>β(베타): 거리/휴리스틱 가중치 (자연 개미와 달리 인공 개미는 거리 정보 활용 가능)</li>
        <li>ρ(로우): 증발 상수</li>
      </ul>
      <strong>동적 환경에서 강력한 이유</strong>: TSP(외판원 문제) 같은 NP 문제에서, 전통적 알고리즘은 도로가 막히거나 새 도시가 추가되면 <span class="keyw">처음부터 다시 계산</span>해야 한다. 그러나 ACO는 <span class="keyw">페로몬을 재구성하며 적응</span>한다. 막힌 길의 페로몬은 증발해 사라지고, 새로 발견된 우회로에 페로몬이 쌓이면서 자연스럽게 새 경로로 수렴. 영상에서 실제로 둥지와 먹이 사이에 장벽을 설치하면 우회 경로를 찾고, 다시 열어주면 더 짧은 길로 복귀하는 모습이 보였다.<br><br>
      <strong>"말 안 듣는 개미"의 가치</strong>도 중요. 모두가 페로몬을 따라가지 않고 다른 길을 시도하는 비순응자(Exploration)가 있어야 환경 변화에 적응 가능. 이는 사회의 <span class="keyw">다양성</span>과 같은 가치를 시사한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">"스티그머지(Stigmergy)"가 무엇인지 설명하고, 왜 그것이 인간의 언어 소통과 원리적으로 같다고 강의에서 설명했는지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>스티그머지(Stigmergy)</strong>는 개체가 <span class="keyw">환경을 바꿈으로써</span> 다른 개체와 의도하지 않은 잠재적 소통이 일어나는 현상이다. 개체끼리 직접 신호를 주고받지 않아도 환경 변화를 통해 정보가 전달된다.<br><br>
      <strong>개미의 사례</strong>: 개미는 시력이 거의 없고 무선 통신도 안 한다. 그러나 페로몬을 길에 남김으로써 <span class="keyw">땅이라는 환경을 변화</span>시킨다. 다른 개미들은 이 환경 변화(페로몬 농도)를 코로 감지해 길 정보를 얻는다 — 직접 소통은 없지만 정보는 전달된다.<br><br>
      <strong>인간 언어와의 원리적 동일성</strong>: 강태원 교수는 "내가 말을 하면 공기가 진동하여 우리 사이의 환경이 달라진다. 개미가 페로몬을 남긴 거나 내가 공기를 흔든 거나 <span class="keyw">원리적으로 같다 — 단지 센서가 다를 뿐</span>"이라고 설명했다.
      <ul>
        <li>개미: <strong>엉덩이(분비) → 환경(땅에 페로몬) → 코(감지)</strong></li>
        <li>인간: <strong>입(발성) → 환경(공기 진동) → 귀(감지)</strong></li>
      </ul>
      두 경우 모두 매개체가 환경이며, 환경 변화를 통해 정보가 전달된다는 점에서 동일한 원리이다.<br><br>
      <strong>의의</strong>: 이런 환경 매개 소통은 <span class="keyw">자기 조직화(Self-Organization)</span>의 핵심 메커니즘이다. 중앙 지시자 없이도, 직접 소통 없이도, 환경을 통해 군집 전체가 일사불란하게 움직일 수 있다. 인터넷의 페이지랭크(9주차)도 마찬가지 — 사용자들이 직접 소통하지 않아도 클릭·링크라는 환경 변화를 통해 페이지의 권위가 자연 발생적으로 형성된다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">DNA 컴퓨팅과 양자 컴퓨팅의 원리를 각각 설명하고, 디지털 컴퓨터와 무엇이 근본적으로 다른지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>DNA 컴퓨팅(DNA Computing)</strong>은 DNA 분자를 직접 계산에 활용하는 컴퓨팅으로, 실험실에서 진행된다.
      <ul>
        <li>디지털: 2진법(0, 1) | DNA: <strong>4진법 — A(아데닌), G(구아닌), C(시토신), T(티민)</strong></li>
        <li>저장 용량: 1g의 DNA에 약 <strong>10억 테라바이트(TB)</strong> 저장 가능, 거의 영구 보존</li>
        <li>응용: NP 문제(경로 찾기)를 화학 반응으로 푸는 방식. 예: 4개 도시 경로를 DNA 염기 사슬로 표현하고 화학 용액에 담가 합성된 사슬을 추출</li>
      </ul>
      <strong>양자 컴퓨팅(Quantum Computing)</strong>은 양자역학의 원리(특히 양자 중첩)를 이용한다.
      <ul>
        <li><strong>양자 중첩(Superposition)</strong>: 슈뢰딩거의 고양이 사고실험 — 고양이는 이미 살았거나 죽은 게 아니라, <span class="keyw">상자를 여는 순간 결정</span>되며 그 전까지 두 상태에 동시 존재</li>
        <li><strong>큐비트(Qubit)</strong>: 양자 컴퓨팅의 기본 단위. 0과 1이 동시에 중첩 상태로 존재</li>
        <li>큐비트 4개 = 2⁴ = <span class="keyw">16가지 상태 동시 표현</span> (기존 컴퓨터는 16가지 중 1가지만)</li>
        <li>n개 큐비트 = 2ⁿ개 상태를 한꺼번에 처리 → 일부 알고리즘에서 지수적 가속</li>
      </ul>
      <strong>디지털 컴퓨터와의 근본적 차이</strong>:
      <ul>
        <li>디지털: <span class="keyw">한 번에 하나의 상태</span>만 처리. 빠르더라도 순차적.</li>
        <li>DNA: 화학 반응의 <span class="keyw">병렬성</span>을 이용 — 수십억 가닥이 동시에 반응. 거대한 자료 저장.</li>
        <li>양자: 중첩 상태로 <span class="keyw">동시에 다중 계산</span>. 측정 시 하나의 결과로 붕괴.</li>
      </ul>
      <strong>의의</strong>: 양자 컴퓨터가 일반화되면 알파고 같은 시스템도 패러다임이 바뀐다고 강의는 예고한다. 모든 경우를 동시에 계산할 수 있으니 NP 문제도 다른 방식으로 접근 가능해지며, 암호 체계도 무너질 수 있다 — 그래서 양자 내성 암호(Post-Quantum Cryptography) 연구가 활발하다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">자기 조직화(Self-Organization)의 개념을 설명하고, 이 원리가 ACO·페이지랭크(9주차)·딥러닝(7주차)에서 어떻게 공통적으로 나타나는지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>자기 조직화(Self-Organization)</strong>는 어떤 <span class="keyw">중앙 지시자(Central Controller)도 없이 시스템 전체가 저절로 질서를 만들어 내는 현상</span>이다. 자연이 가진 가장 신비로운 특징 중 하나이며, 강의 부제 "누가 지시하는가!"의 답은 <strong>"아무도 지시하지 않는다"</strong>이다.<br><br>
      <strong>ACO(개미 군집 최적화)에서의 자기 조직화</strong>:
      <ul>
        <li>우두머리 개미가 "짧은 길로 가라"고 지시하지 않는다.</li>
        <li>각 개미는 자기 앞 페로몬만 보고 행동한다.</li>
        <li>그러나 페로몬+증발 메커니즘으로 군집 전체가 <span class="keyw">자연스럽게 최단 경로에 수렴</span>한다.</li>
        <li>스티그머지(환경 매개 소통)가 이를 가능케 한다.</li>
      </ul>
      <strong>페이지랭크(9주차)에서의 자기 조직화</strong>:
      <ul>
        <li>구글이 "이 페이지가 더 중요하다"고 지시하지 않는다.</li>
        <li>각 웹사이트 운영자는 자기가 좋다고 생각하는 페이지에 링크를 단다.</li>
        <li>이런 무수한 링크가 모여 <span class="keyw">자연스럽게 페이지의 권위(랭크)가 형성</span>된다.</li>
        <li>사용자들의 클릭·링크라는 환경 변화가 정보를 만들어 낸다 — 스티그머지의 디지털 버전.</li>
      </ul>
      <strong>딥러닝(6~7주차)에서의 자기 조직화</strong>:
      <ul>
        <li>프로그래머가 "이 뉴런의 가중치는 0.7이어야 한다"고 지시하지 않는다.</li>
        <li>각 뉴런(수도꼭지)은 역전파를 통해 자기 가중치를 조정한다.</li>
        <li>수많은 뉴런의 자율적 조정이 합쳐져 <span class="keyw">전체 신경망이 학습한다</span>.</li>
        <li>ChatGPT의 1750억 매개변수가 모두 이런 자기 조직화의 결과.</li>
      </ul>
      <strong>인간의 뇌</strong>도 같은 원리이며, 강태원 교수의 전공인 <span class="keyw">계산 지능(Computational Intelligence)</span>의 핵심 패러다임이기도 하다.<br><br>
      <strong>철학적 의의</strong>: 자기 조직화는 "지능은 중앙에서 통제되어야 한다"는 옛 관념을 뒤집는다. 단순한 규칙을 따르는 다수가 모이면, 누구도 의도하지 않은 복잡하고 지능적인 행동이 출현(emergence)한다. 이는 13주차 라이프 게임, 14주차 인공생명으로 이어지는 핵심 주제이며, 강의 전반에 흐르는 "다양성과 개체의 자율성"이라는 가치와 직결된다.
    </div>
  </div>

  <div class="nav-links">
    <a href="11주차_교과서.html">📚 교과서</a>
    <a href="11주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 12주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 12주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>12주차 문제집</h1>
    <div class="subtitle">발가락이 닮았네</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">자연의 진화를 구성하는 두 축은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 학습 + 추론</li>
      <li><span class="opt-num">②</span> 선택(Selection) + 유전(Heredity)</li>
      <li><span class="opt-num">③</span> 교차 + 돌연변이</li>
      <li><span class="opt-num">④</span> 부모 + 자식</li>
      <li><span class="opt-num">⑤</span> 환경 + 적응</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 선택 + 유전</strong><br>
      <span class="alabel">해설</span>1차시 퀴즈 정답: A=<span class="keyw">선택</span>, B=<span class="keyw">유전</span>. 둘 다 있어야 진화. 교차·돌연변이는 GA의 유전 연산.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">유전 알고리즘(GA)에서 <strong>사람</strong>이 직접 해야 할 가장 중요한 두 가지 일은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 모집단 구성 + 선택</li>
      <li><span class="opt-num">②</span> 교차 + 돌연변이</li>
      <li><span class="opt-num">③</span> 인코딩 + 적합도 함수 정의</li>
      <li><span class="opt-num">④</span> 모집단 구성 + 교차</li>
      <li><span class="opt-num">⑤</span> 모든 단계를 사람이 한다</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 인코딩 + 적합도 함수 정의</strong><br>
      <span class="alabel">해설</span>나머지(모집단 구성·선택·교차·돌연변이)는 컴퓨터가 무작위로 처리. 사람의 몫은 <span class="keyw">문제를 어떻게 비트로 표현할지(인코딩)</span>와 <span class="keyw">무엇이 좋은 해인지(적합도)</span> 정의.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">교차(Crossover)와 돌연변이(Mutation)의 단위로 옳은 짝은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 교차 = 비트 단위, 돌연변이 = 개체 단위</li>
      <li><span class="opt-num">②</span> 교차 = 개체 단위, 돌연변이 = 비트(유전자) 단위</li>
      <li><span class="opt-num">③</span> 둘 다 비트 단위</li>
      <li><span class="opt-num">④</span> 둘 다 개체 단위</li>
      <li><span class="opt-num">⑤</span> 둘 다 모집단 단위</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 교차 = 개체 단위, 돌연변이 = 비트 단위</strong><br>
      <span class="alabel">해설</span>교차는 두 부모 개체를 자르고 섞음(교차율 ~70%). 돌연변이는 비트(유전자) 하나하나에 적용(1/100~1/1000).
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">배낭 문제에 적용되는 적합도 함수로 강의에서 제시한 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> Fitness = |용량 + 부피|</li>
      <li><span class="opt-num">②</span> Fitness = 용량 × 부피</li>
      <li><span class="opt-num">③</span> Fitness = 1 / |자루 용량 − 실제 담긴 부피|</li>
      <li><span class="opt-num">④</span> Fitness = 자루 개수</li>
      <li><span class="opt-num">⑤</span> Fitness = √용량</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 1 / |용량 − 부피|</strong><br>
      <span class="alabel">해설</span><span class="keyw">절댓값</span>으로 부족/초과 모두 페널티, <span class="keyw">역수</span>로 차이가 작을수록 적합도가 높아지게 함.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">상위 개체를 무조건 선택하고 하위는 버리는 GA 선택 방식의 이름은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 룰렛휠 (Roulette Wheel)</li>
      <li><span class="opt-num">②</span> 토너먼트 (Tournament)</li>
      <li><span class="opt-num">③</span> 엘리티시즘 (Elitism, 우월주의)</li>
      <li><span class="opt-num">④</span> 랭크 (Rank)</li>
      <li><span class="opt-num">⑤</span> 무작위 (Random)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 엘리티시즘</strong><br>
      <span class="alabel">해설</span>3차시 배낭 문제에서 사용. 룰렛휠보다 빠르게 수렴하지만 다양성 손실 위험이 있음.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">진화의 두 축을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① <strong>자연 선택 (Natural Selection)</strong> — 환경에 적합한 것이 살아남음<br>
      ② <strong>유전 (Heredity)</strong> — 형질이 자손에게 전해짐
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">단순 유전 알고리즘(Simple GA)의 5단계 절차를 순서대로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      ① 문제 정의 및 <strong>인코딩(Encoding)</strong><br>
      ② <strong>모집단(Population)</strong> 구성<br>
      ③ <strong>적합도(Fitness)</strong> 계산<br>
      ④ <strong>선택(Selection)</strong><br>
      ⑤ <strong>유전 연산(교차 + 돌연변이)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">유전형(Genotype)과 표현형(Phenotype)의 차이를 한 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>유전형</strong> = DNA 표현 (예: <code>1101</code> 같은 비트 코드)<br>
      <strong>표현형</strong> = 그 유전형이 발현된 실제 모습 (예: 김 O 라면)
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">적합도 함수(Fitness Function)의 다른 두 가지 이름을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>비용 함수(Cost Function)</strong>, <strong>평가 함수(Evaluation Function)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">룰렛휠 선택(Roulette Wheel Selection)을 컴퓨터로 어떻게 구현하는지 한 줄로 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>0~1 사이 균등분포 랜덤 넘버를 생성하여 적합도 누적 비율과 비교</strong>, 해당 구간의 개체를 선택.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">교차율(Crossover Rate)은 일반적으로 어느 정도이며, 돌연변이는 어느 정도 확률로 일어나는가?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      교차율: 통상 <strong>약 70%</strong><br>
      돌연변이: <strong>1/100, 1/1000 정도로 매우 드물게</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">배낭 문제(Knapsack)의 적합도 함수를 쓰시오. (수식)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>Fitness = 1 / |자루 용량 − 실제 담긴 부피|</strong><br>
      절댓값은 부족·초과 모두 페널티, 역수는 차이가 작을수록 좋은 해라는 의도.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">엘리티시즘(Elitism)의 정의와, 룰렛휠과 비교한 장단점을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>엘리티시즘</strong>: 적합도 상위 개체를 무조건 선택, 하위 개체는 버림.<br>
      <strong>장점</strong>: 빠른 수렴.<br>
      <strong>단점</strong>: 다양성 손실 — 지역 최적해에 갇힐 수 있음.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">GA의 효율성을 수학적으로 입증한 학자와 그 이론 이름을 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>존 홀랜드(John Holland)</strong>의 <strong>스키마 이론(Schema Theory)</strong>
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">『눈먼 시계공(The Blind Watchmaker)』과 『이기적 유전자(The Selfish Gene)』의 저자를 쓰시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span>
      <strong>리처드 도킨스 (Richard Dawkins)</strong>. 『눈먼 시계공』에서 누적적 선택(Cumulative Selection)의 위력을 설명.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody">자연의 진화가 "선택"과 "유전" 두 축의 결합인 이유를 설명하고, 왜 둘 중 하나라도 없으면 진화가 일어나지 않는지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>자연의 진화(Evolution)</strong>는 두 가지 메커니즘이 결합되어 일어나는 과정이다.<br><br>
      <strong>① 자연 선택(Natural Selection)</strong>: 인간의 의도가 아니라 자연이 "현재 환경에 적합한 것"을 살아남게 하고, 부적합한 것은 도태시킨다. 강의 비유로 "하늘이 내려앉으면" 똑바로 걷는 사람보다 굽어 다니는 사람이 생존에 유리해지듯, 환경이 곧 기준이다.<br><br>
      <strong>② 유전(Heredity)</strong>: 부모의 DNA에 담긴 형질이 자손에게 전해진다. "물려주니까 의미가 있는 것" — 부모의 좋은 형질이 다음 세대로 전달되어야 점진적 변화가 누적된다.<br><br>
      <strong>둘 중 하나라도 없으면 안 되는 이유</strong>:
      <ul>
        <li><strong>선택만 있고 유전이 없으면</strong>: 좋은 형질을 가진 개체가 죽고 나면 그것으로 끝. 다음 세대에 이어지지 않으므로 진화가 누적되지 않는다.</li>
        <li><strong>유전만 있고 선택이 없으면</strong>: 좋은 형질과 나쁜 형질이 모두 전해진다. 환경에 적합한 방향으로의 변화가 일어나지 않는다.</li>
      </ul>
      <strong>"진화에 방향성은 없다"</strong>는 점도 중요. 흔히 보는 "원숭이 → 인간" 그림은 잘못된 통념. 진화는 수직 상승이 아니라 <span class="keyw">수평적 분기</span>이다. 인간은 원숭이보다 "더 진화"한 것이 아니라 다른 길로 갈라진 종일 뿐이다.<br><br>
      이 자연 진화의 두 축을 컴퓨터로 모방한 것이 <span class="keyw">유전 알고리즘(GA)</span>이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">단순 유전 알고리즘(Simple GA)의 5단계 절차를 설명하고, 각 단계에서 사람과 컴퓨터가 각각 무엇을 하는지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>단순 GA의 5단계 절차</strong>:
      <ul>
        <li>① <strong>문제 정의 및 인코딩(Encoding)</strong> — <span class="keyw">사람</span>이 한다. 문제를 컴퓨터가 다룰 비트 수열로 표현. 예: 라면 만들기에서 MSG·계란·파·김 4가지를 4비트로 표현(<code>1101</code> = MSG O, 계란 O, 파 X, 김 O).</li>
        <li>② <strong>모집단(Population) 구성</strong> — <span class="keyw">컴퓨터</span>가 한다. 무작위로 여러 후보 해(라면 4~6개)를 생성.</li>
        <li>③ <strong>적합도(Fitness) 계산</strong> — <span class="keyw">컴퓨터</span>가 한다(단, 적합도 함수 자체는 사람이 정의). 각 개체가 얼마나 좋은 해인지 평가.</li>
        <li>④ <strong>선택(Selection)</strong> — <span class="keyw">컴퓨터</span>가 무작위로. 룰렛휠(적합도 비율 무작위) 또는 엘리티시즘(상위 무조건).</li>
        <li>⑤ <strong>유전 연산</strong> — <span class="keyw">컴퓨터</span>가 무작위로. 교차(개체 단위, ~70%) + 돌연변이(비트 단위, 1/100~1/1000).</li>
      </ul>
      ③~⑤를 종료 조건(만족할 만한 답 또는 일정 세대) 만족까지 반복.<br><br>
      <strong>사람과 컴퓨터의 역할 분담</strong>:
      <ul>
        <li><strong>사람의 몫</strong>: ① 인코딩 ② 적합도 함수 정의. 이 두 가지가 GA 성공의 핵심.</li>
        <li><strong>컴퓨터의 몫</strong>: 나머지 모든 단계의 무작위 처리.</li>
      </ul>
      강의 비유: "동양식 — 라면을 분석하지 말고 그냥 먹어봐서 맛있으면 좋은 것". 사람이 모든 걸 분석하기보다, 자연(= 컴퓨터의 무작위성)에 맡기는 것이 GA의 철학이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">유전 연산의 두 가지인 교차(Crossover)와 돌연변이(Mutation)를 비교 설명하고, 각각의 단위·확률·역할의 차이를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>교차(Crossover)</strong>:
      <ul>
        <li><strong>단위</strong>: <span class="keyw">개체 단위</span>. 두 부모 개체의 염색체를 자르고 섞어 자식을 만든다.</li>
        <li><strong>확률(교차율, Crossover Rate)</strong>: 통상 <span class="keyw">약 70%</span>.</li>
        <li><strong>역할</strong>: 부모의 좋은 형질을 결합하여 더 좋은 자식을 만들기. 자르는 위치도 무작위.</li>
        <li>강의 비유: "엄마는 왼쪽, 아빠는 오른쪽이 아니다 — 코는 엄마·콧구멍은 아빠 식으로 미세하게 섞이지 단순 절반이 아니다."</li>
      </ul>
      <strong>돌연변이(Mutation)</strong>:
      <ul>
        <li><strong>단위</strong>: <span class="keyw">비트(유전자) 단위</span>. 비트 값을 0↔1로 뒤집기.</li>
        <li><strong>확률</strong>: 매우 드물게, <span class="keyw">1/100~1/1000</span> 정도.</li>
        <li><strong>역할</strong>: 부모에 없던 새로운 유전자 만들기. 다양성 도입.</li>
      </ul>
      <strong>차이 정리</strong>:
      <ul>
        <li>교차는 <strong>개체</strong> 단위, 돌연변이는 <strong>비트</strong> 단위</li>
        <li>교차는 <strong>자주</strong>(~70%), 돌연변이는 <strong>드물게</strong>(1/100~1/1000)</li>
        <li>교차는 기존 유전자의 <strong>재조합</strong>, 돌연변이는 <strong>새 유전자 창조</strong></li>
      </ul>
      <strong>왜 돌연변이가 드물어야 하는가?</strong>
      <ul>
        <li>너무 자주 일으키면 애써 학습한 좋은 유전자가 무너진다.</li>
        <li>너무 안 하면 부모 풀에 없는 새 가능성을 탐색할 수 없다.</li>
        <li>그래서 매우 낮은 확률로 가끔만 일어나야 한다.</li>
      </ul>
      이 두 연산의 균형이 GA의 효율성을 결정하며, 둘 다 강의의 핵심 철학인 <span class="keyw">"무작위성과 다양성"</span>을 구현한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">배낭 문제(Knapsack Problem)에 유전 알고리즘을 적용하는 과정을 설명하고, 적합도 함수가 왜 <code>1 / |용량 − 부피|</code>의 형태인지 그 설계 의도를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>배낭 문제(Knapsack Problem)</strong>는 주어진 용량의 배낭(들)에 물건을 빈틈없이 채우는 NP 문제이다. 11주차의 TSP(외판원 문제)와 함께 대표적 NP 문제로, 물건 수가 늘면 경우의 수가 폭증한다.<br><br>
      <strong>예시 설정</strong>: 자루 3개(용량 16, 8, 4), 물건 7개(부피 1~7), 모집단 4, 선택 방식 = 엘리티시즘.<br><br>
      <strong>GA 적용 과정</strong>:
      <ul>
        <li><strong>① 인코딩</strong>: 각 물건이 어느 자루에 들어가는지를 비트로 표현(물건 중심 방식이 자루 중심보다 효율적).</li>
        <li><strong>② 모집단</strong>: 4가지 다른 배치 방식을 랜덤 생성.</li>
        <li><strong>③ 적합도 계산</strong>: 각 자루의 (용량 − 실제 담긴 부피)를 측정.</li>
        <li><strong>④ 엘리티시즘 선택</strong>: 적합도 상위 개체 무조건 선택.</li>
        <li><strong>⑤ 교차·돌연변이</strong>: 새 자식 생성.</li>
        <li>최적의 배치(자루 용량과 부피가 거의 일치)를 찾을 때까지 반복.</li>
      </ul>
      <strong>적합도 함수의 설계 의도</strong>:
      <div style="text-align:center; font-family:serif; margin:10px 0;">Fitness = 1 / |자루 용량 − 실제 담긴 부피|</div>
      <ul>
        <li><strong>절댓값(|…|)을 쓰는 이유</strong>: 자루에 물건이 <span class="keyw">부족하든 초과하든 모두 페널티</span>를 주기 위해. 용량 16에 부피 14를 담아도(차이 2), 용량 16에 부피 18을 담아도(차이 2) 똑같이 나쁜 해로 평가. 부호로 인한 오류 방지.</li>
        <li><strong>역수(1/…)를 쓰는 이유</strong>: 차이가 작을수록 좋은 해이므로 <span class="keyw">차이가 작을수록 Fitness 값이 커져야</span> 한다. 차이가 0이면 적합도가 무한대(이론상), 차이가 클수록 0에 가까워진다.</li>
      </ul>
      이 적합도 함수가 잘못 설계되면(예: 절댓값을 빼면, 또는 역수를 안 쓰면) 컴퓨터가 아무리 돌려도 좋은 답을 못 찾는다. <strong>적합도 함수 설계는 사람의 가장 중요한 몫</strong>임을 보여주는 좋은 예시이다.<br><br>
      <strong>교재 안내</strong>: 강의에서 "교재 3차시 배낭 문제 예시(부피 차이 합 부분)에 오타가 있다"고 안내했으니 수업 들으며 수정할 것.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">GA의 무작위성(Randomness)이 왜 강점이 되는지 설명하고, 11주차의 자연 컴퓨팅 철학("이웃 정보 활용", "자기 조직화")과 어떻게 연결되는지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범답안</span>
      <strong>GA의 무작위성(Randomness)</strong>은 알고리즘의 본질이며 다음 단계 모두에서 작동한다.
      <ul>
        <li><strong>모집단</strong>: 무작위로 초기 후보 해 생성</li>
        <li><strong>선택</strong>: 룰렛휠은 적합도 비율로 무작위 추출</li>
        <li><strong>교차</strong>: 자르는 위치도 무작위</li>
        <li><strong>돌연변이</strong>: 어떤 비트가 뒤집힐지 무작위</li>
      </ul>
      강의 표현: "<span class="keyw">유전 알고리즘은 랜덤이야 랜덤</span>".<br><br>
      <strong>무작위성이 강점이 되는 이유</strong>:
      <ul>
        <li>① <strong>다양성 보존</strong>: "지금 나쁘다고 앞으로도 나쁜 게 아니다". 적합도 낮은 개체도 살아남을 기회를 줘야 의외의 최강해가 나올 수 있다.</li>
        <li>② <strong>지역 최적해(Local Minimum) 회피</strong>: 분석적 방법(경사하강법 등)은 가장 가까운 골짜기에 갇힐 수 있지만, 무작위성은 그 너머를 탐색.</li>
        <li>③ <strong>분석 불필요</strong>: "라면이 왜 맛있는지" 분석할 필요 없이 그냥 먹어보고 좋은 것을 남기면 된다. 동양식 사고.</li>
      </ul>
      <strong>11주차 자연 컴퓨팅 철학과의 연결</strong>:
      <ul>
        <li>① <strong>"이웃 정보 활용"</strong>(PSO에서 강조): GA의 교차도 이웃(같은 모집단의 다른 개체)의 정보를 활용해 새 자식을 만든다. 두 부모의 형질을 섞는 것이 "이웃 정보 활용"의 한 형태.</li>
        <li>② <strong>"자기 조직화(Self-Organization)"</strong>: 누가 "이 라면이 가장 맛있어"라고 지시하지 않는다. 단지 적합도가 높은 개체가 더 자주 선택되고, 다음 세대로 전달되는 단순 규칙만으로 모집단 전체가 <span class="keyw">자연스럽게 좋은 해로 수렴</span>한다.</li>
        <li>③ <strong>"누가 지시하는가? 아무도 지시하지 않는다"</strong>: 11주차 ACO와 같은 자기 조직화 원리.</li>
      </ul>
      <strong>딥러닝과의 결합 가능성</strong>: 신경망 하나 전체를 DNA로 표현해 GA로 진화시키는 연구가 활발. "신경망 여러 개 만들어놓고 누가 더 잘 작동하나" 보는 식. 미래 양자 컴퓨터가 일반화되면 GA의 계산 부담이 해결되어 더욱 강력해질 것으로 예상된다.
    </div>
  </div>

  <div class="nav-links">
    <a href="12주차_교과서.html">📚 교과서</a>
    <a href="12주차_학습서.html">📖 학습서</a>
  </div>
</div>
<script>
  function toggleAns(btn){const box=btn.nextElementSibling;box.classList.toggle('show');btn.textContent=box.classList.contains('show')?'정답 가리기':'정답 보기';}
  function showAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.add('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 가리기');}
  function hideAll(){document.querySelectorAll('.answer-box').forEach(b=>b.classList.remove('show'));document.querySelectorAll('.toggle-btn').forEach(b=>b.textContent='정답 보기');}
</script>
</body>
</html>


# ========= 13주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 13주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>13주차 문제집</h1>
    <div class="subtitle">단순한 복잡함</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">혼돈(Chaos) 시스템의 특징이 <strong>아닌</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 초기치 민감성 (Butterfly Effect)</li>
      <li><span class="opt-num">②</span> 주기 배증 (Bifurcation)</li>
      <li><span class="opt-num">③</span> 자기유사성 (Self-similarity)</li>
      <li><span class="opt-num">④</span> 완전한 무질서 (Total Disorder)</li>
      <li><span class="opt-num">⑤</span> 예측 불가능한 변화</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ 완전한 무질서</strong><br>
      <span class="alabel">해설</span>혼돈은 <span class="keyw">무질서와 구별됨</span>. 혼돈은 예측 불가능하지만 그 안에서 새로운 패턴(생명)이 나옴. 무질서는 패턴 없이 그냥 랜덤. "Life at the Edge of Chaos".
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">1차원 세포 자동자(CA)에서 가능한 <strong>규칙의 총 개수</strong>는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 8개</li>
      <li><span class="opt-num">②</span> 16개</li>
      <li><span class="opt-num">③</span> 64개</li>
      <li><span class="opt-num">④</span> 128개</li>
      <li><span class="opt-num">⑤</span> 256개</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>⑤ 256개</strong><br>
      <span class="alabel">해설</span>이웃 패턴은 2³=8가지(000~111). 각 패턴마다 결과를 0 또는 1로 정할 수 있으므로 가능한 규칙 = <span class="keyw">2⁸ = 256개</span>.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">콘웨이의 라이프 게임에서 사용하는 이웃 정의(8개)는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 무어 이웃 (Moore Neighborhood)</li>
      <li><span class="opt-num">②</span> 폰 노이만 이웃 (von Neumann Neighborhood)</li>
      <li><span class="opt-num">③</span> 유클리드 이웃</li>
      <li><span class="opt-num">④</span> 만델브로 이웃</li>
      <li><span class="opt-num">⑤</span> 콘웨이 이웃</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>① 무어 이웃</strong><br>
      <span class="alabel">해설</span><span class="keyw">무어 이웃</span>은 상하좌우 + 대각선 4개 = 8개. <span class="keyw">폰 노이만 이웃</span>은 상하좌우만 = 4개. 콘웨이는 무어를 사용.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">콘웨이의 라이프 게임에서 살아있는 세포가 <strong>다음 단계에 살아남는</strong> 조건은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 이웃이 1명</li>
      <li><span class="opt-num">②</span> 이웃이 2명 또는 3명</li>
      <li><span class="opt-num">③</span> 이웃이 정확히 3명</li>
      <li><span class="opt-num">④</span> 이웃이 4명 이상</li>
      <li><span class="opt-num">⑤</span> 이웃이 8명 모두</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 이웃이 2명 또는 3명</strong><br>
      <span class="alabel">해설</span>규칙 1(살아있는 세포): 이웃 <span class="keyw">2 또는 3개 → 생존</span>. 1개 이하 → 쓸쓸해서 사망. 4개 이상 → 시끄러워서 사망. 정답 ③은 빈 세포의 탄생 조건.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">2차원 세포 자동자에서 공간의 양 끝을 이어붙여 만들어진 형태는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 구(Sphere)</li>
      <li><span class="opt-num">②</span> 원통(Cylinder)</li>
      <li><span class="opt-num">③</span> 토러스(Torus, 원환체)</li>
      <li><span class="opt-num">④</span> 뫼비우스의 띠</li>
      <li><span class="opt-num">⑤</span> 평면(Plane)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 토러스</strong><br>
      <span class="alabel">해설</span>2차원 평면의 좌우를 이어붙이면 원통, 그 원통의 위아래를 또 이어붙이면 <span class="keyw">토러스(도넛 모양)</span>가 됨. 1차원 CA는 좌우만 이어붙이므로 원통.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">로렌츠(Lorenz)가 발견한, 작은 차이가 큰 변화를 일으키는 현상을 무엇이라 하는가? (영어 명칭도 함께)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>나비효과 (Butterfly Effect) = 초기치 민감성 (Sensitivity to Initial Conditions)</strong><br>
      <span class="alabel">해설</span>로렌츠가 소수점 뒷자리를 잘라낸 입력값으로 완전히 다른 결과를 얻은 데서 유래. 로렌츠의 <span class="keyw">이상한 끌개(Strange Attractor)</span> 그림이 나비 모양.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">혼돈 시스템에서 주기가 1 → 2 → 4 → 8 → 16... 두 배씩 늘어나는 현상을 무엇이라 하는가?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>주기 배증 (Bifurcation)</strong><br>
      <span class="alabel">해설</span>Bi = 두 갈래. 식 xₙ₊₁ = A·xₙ·(1−xₙ)에서 A 값을 늘려가면 한 값 → 두 값 → 네 값 → ... 이렇게 갈라짐.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">일부를 확대해서 보면 전체와 닮은 모양이 나오는, 혼돈과 프랙털의 공통 특징은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>자기유사성 (Self-similarity)</strong><br>
      <span class="alabel">해설</span>코흐 곡선, 시에르핀스키 삼각형, 만델브로 집합, 주식 그래프, 산과 구름 — 모두 자기유사성을 보임. 자연이 작동하는 방식.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">"자연의 기하학"이라 불리는, 만델브로가 정립한 기하학의 이름은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>프랙털 기하학 (Fractal Geometry)</strong><br>
      <span class="alabel">해설</span>유클리드 기하학은 직선·원·삼각형 같은 인공물용. 프랙털 기하학은 나무·구름·파도·산 같은 자연 형태를 다룸. <span class="keyw">만델브로(Benoit Mandelbrot)</span>가 정립.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">삼각형 가운데를 계속 파내는 방식으로 만들어지며, 면적은 0이지만 점은 무한히 많은 프랙털의 이름은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>시에르핀스키 삼각형 (Sierpinski Triangle)</strong><br>
      <span class="alabel">해설</span>강의 비유: "아이스크림을 끝없이 파먹는 방법". 사각형 버전은 <span class="keyw">시에르핀스키 카펫</span>. 1차원 CA의 72번 규칙에서도 자연적으로 생성됨.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">"렌즈가 여러 개 달린 복사기"로 비유되는, 반슬리(Barnsley)가 정리한 프랙털 생성 시스템의 영문 약어는?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>IFS (Iterative Fractal System, 반복 프랙털 시스템)</strong><br>
      <span class="alabel">해설</span>강 교수 강의 표현 그대로. 학술적으로는 Iterated Function System으로도 표기되지만 강의에선 Iterative Fractal System으로 발화. 한 종이를 여러 렌즈로 축소·회전·복사 → 결과를 다시 입력으로 → 반복. 고사리(Fern), 나무, 구름 등 자연 형태가 생성됨. 게임·영화의 풍경 생성에 활용.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">1차원 세포 자동자에서 시작 상태가 한 점(아담 한 마리)일 때, <strong>시에르핀스키 삼각형</strong> 모양을 만들어내는 규칙의 번호는?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>72번 규칙</strong><br>
      <span class="alabel">해설</span>72 = 64 + 8. 8개 입력 패턴에 대한 결과 비트 중 64 자리와 8 자리에 1. 단순 if-else 규칙이지만 결과는 프랙털. <span class="keyw">단순한 규칙 → 복잡한 행태</span>의 대표 사례.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">스티븐 울프램(Stephen Wolfram)이 분류한 세포 자동자의 4가지 행태는?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>① 수렴, ② 주기적, ③ 혼돈(Chaotic), ④ 무질서</strong><br>
      <span class="alabel">해설</span>이 중 <span class="keyw">③ 혼돈 영역에 생명이 있다</span>. 너무 단순(수렴·주기적)하지도, 완전 무질서하지도 않은 곳. 울프램은 Mathematica 개발자이자 물리학자.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">콘웨이의 라이프 게임에서 <strong>빈 세포에 새 생명이 탄생</strong>하는 조건은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>이웃 8개 중 살아있는 게 정확히 3개일 때</strong><br>
      <span class="alabel">해설</span>"3명이 사는 동네면 살 만하다고 입주"라는 비유. 그 외(0, 1, 2, 4~8)는 계속 빈 채로 유지.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">콘웨이 라이프 게임에서 주기적으로 글라이더(Glider)를 발사하여 CPU의 클럭처럼 작동하는 패턴의 이름은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>글라이더 건 (Glider Gun)</strong><br>
      <span class="alabel">해설</span>모든 전자회로의 기본인 클럭(신호 발생기) 역할. 이를 활용하면 AND·OR·NOT 게이트도 만들 수 있고, 결국 <span class="keyw">튜링 머신(컴퓨터)</span>까지 라이프 게임 위에 구현 가능.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody"><strong>혼돈(Chaos)</strong>과 <strong>무질서(Disorder)</strong>의 차이를 설명하고, "생명이 혼돈의 언저리에 있다"는 말이 의미하는 바를 함께 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      혼돈은 <span class="keyw">예측 불가능한 변화를 내포하지만 그 안에 패턴과 자기유사성이 있는 상태</span>다. 반면 무질서는 패턴이 전혀 없는 완전한 랜덤이다. 혼돈은 어지러우면서도 새로운 것이 생겨날 수 있는 "긴장된 균형" 상태이고, 무질서에서는 아무것도 새로 나오지 않는다. 울프램의 4분류에서 ① 수렴과 ② 주기적은 너무 단순해 새로운 것이 나오지 않고, ④ 무질서는 너무 흩어져 의미 있는 구조가 만들어지지 않는다. <span class="keyw">③ 혼돈(Chaotic) 영역만이 생명이 자라날 수 있는 "균형의 가장자리"</span>다. 그래서 "생명은 혼돈의 언저리(Edge of Chaos)에 있다"고 말한다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody">강의 1차시의 부제 <strong>"나비와 꽃"</strong>이 의미하는 바를, 혼돈과 프랙털의 관계 측면에서 서술하시오. 주식 시장 예시를 함께 들어 설명할 것.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      "나비"는 <span class="keyw">혼돈(Chaos)</span>을 상징한다 — 버터플라이 이펙트, 즉 초기치 민감성. "꽃"은 <span class="keyw">프랙털(Fractal)</span>을 상징한다 — 자연이 만들어내는 자기유사적 형태. 두 개념은 분리된 것이 아니라 <span class="keyw">항상 같이 등장</span>한다. 혼돈 시스템이 만들어내는 그림 안에서 자기유사적 프랙털 구조가 나타나고, 프랙털을 보여주는 자연 현상은 대개 초기치 민감성을 동반한다.
      대표적 예가 주식 시장이다. 주식 그래프의 일부를 확대해보면 전체와 비슷한 모양이 나타난다(<span class="keyw">프랙털성</span>). 그리고 사람들의 기대·소문이라는 자기 참조성과 초기 작은 사건이 큰 변동으로 이어지는 <span class="keyw">혼돈성</span>을 함께 가진다. 그래서 주식은 예측 불가능하다. 한 시스템 안에 나비(혼돈)와 꽃(프랙털)이 동시에 존재하는 것이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">1차원 세포 자동자에서 "32번 규칙"이라는 표현이 어떻게 만들어지는지, <strong>인코딩 방식</strong>을 단계별로 설명하시오. 가능한 규칙의 총 수가 256개인 이유도 함께 밝힐 것.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      1차원 CA에서 한 칸의 다음 상태는 자기 자신 + 양 옆 이웃(총 3칸)의 상태로 결정된다. 3칸 각각이 0/1이므로 가능한 입력 패턴은 <span class="keyw">2³ = 8가지</span>: 000, 001, 010, 011, 100, 101, 110, 111. 각 패턴마다 결과를 0 또는 1로 정해야 하므로 가능한 규칙은 <span class="keyw">2⁸ = 256개</span>다.
      "32번 규칙"이란 8개의 결과 비트를 일렬로 늘어놓은 다음 그것을 <span class="keyw">2진수로 보고 10진수로 변환한 값</span>이다. 자리값 1, 2, 4, 8, 16, 32, 64, 128 중에서 32 자리에만 1이 있으면 32번 규칙이 된다. 마치 유전 알고리즘에서 DNA(비트 수열)를 인코딩하는 것처럼, <span class="keyw">8비트가 규칙의 DNA 역할</span>을 한다. 72번 규칙이라면 64 + 8 자리에 1이 있다는 뜻이다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody"><strong>콘웨이의 라이프 게임(Game of Life)</strong>의 두 가지 규칙을 정확히 기술하고, 단순한 규칙에서 어떻게 <strong>튜링 머신(Turing Machine, 컴퓨터)</strong>까지 만들 수 있는지 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      <strong>두 규칙:</strong><br>
      <span class="keyw">규칙 1 (살아있는 세포)</span>: 무어 이웃(상하좌우 + 대각선) 8개 중 살아있는 게 2개 또는 3개면 다음 단계에도 살아남는다. 그 외(1개 이하 또는 4개 이상)는 사망.<br>
      <span class="keyw">규칙 2 (빈 세포)</span>: 8개 이웃 중 살아있는 게 정확히 3개면 새 생명이 탄생한다. 그 외는 계속 빈 채.<br><br>
      이 규칙만으로 매우 다양한 패턴이 생겨난다. <span class="keyw">글라이더(Glider)</span>는 4단계 주기로 모양이 바뀌며 대각선 이동하는 패턴이고, <span class="keyw">글라이더 건(Glider Gun)</span>은 주기적으로 글라이더를 발사하는 신호 생성기 역할을 한다. CPU의 클럭과 같다.
      이 글라이더들이 충돌하고 결합하는 패턴을 잘 배치하면 AND, OR, NOT 같은 논리 게이트를 만들 수 있다. 논리 게이트로는 모든 계산이 가능하다(튜링 완전성). 따라서 콘웨이의 라이프 게임만으로도 <span class="keyw">이론적으로 어떤 컴퓨터, 심지어 휴대폰까지 구현 가능</span>하다. 이것이 13주차의 핵심 메시지: 단순한 규칙 → 무한한 복잡함의 창발.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">13주차의 핵심 메시지인 <strong>"단순한 규칙 → 복잡한 행태의 창발(Emergence)"</strong>이 의미하는 바를 설명하고, 1차원 CA·콘웨이 라이프 게임·조개껍질 무늬·개미 알고리즘 등 여러 사례에서 공통적으로 발견되는 원리를 정리하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      <span class="keyw">창발(Emergence)</span>이란 구성요소의 단순한 상호작용에서 예측하지 못한 새로운 성질이나 행태가 갑자기 나타나는 현상이다. 13주차에서 본 모든 사례에는 공통된 세 가지 원리가 있다.<br><br>
      <strong>① 단순한 규칙</strong>: 1차원 CA는 8개 입력에 대한 0/1 출력. 콘웨이 라이프 게임은 단 2개 규칙. 조개껍질은 옆 칸 색만 보고 다음 색 결정. 개미는 페로몬 냄새만 맡음. 어디에도 복잡한 알고리즘은 없다.<br>
      <strong>② 이웃 정보만 사용</strong>: 전체를 볼 필요가 없다. 자신과 주변의 가까운 칸·개체만 본다. 멀리 있는 정보는 무시. 이것이 자연이 작동하는 효율적 방식이다.<br>
      <strong>③ 복잡한 행태 창발</strong>: 결과는 누가 시킨 것처럼 정교한 패턴 — 시에르핀스키 삼각형, 글라이더 건, 조개껍질의 아름다운 무늬, 개미 떼의 최단 경로 — 이 갑자기 튀어나온다.<br><br>
      이는 인공지능을 만들 때 시스템 내부가 복잡해야 할 필요가 없다는 강력한 증거다. <span class="keyw">"복잡해 보이는 것의 내부는 단순할 수 있다"</span>는 메시지가 13주차 전체를 관통한다. 14주차의 보이드(Boid) 알고리즘은 이 철학의 "끝판왕"이 될 것이다.
    </div>
  </div>

  <div class="nav-links">
    <a href="13주차_학습서.html">학습서로</a>
    <a href="13주차_교과서.html">교과서로</a>
    <a href="../index.html">메인으로</a>
  </div>
</div>
<script>
function toggleAns(btn) { var box = btn.nextElementSibling; box.classList.toggle('show'); btn.textContent = box.classList.contains('show') ? '정답 숨기기' : '정답 보기'; }
function showAll() { document.querySelectorAll('.answer-box').forEach(b => b.classList.add('show')); document.querySelectorAll('.toggle-btn').forEach(b => b.textContent = '정답 숨기기'); }
function hideAll() { document.querySelectorAll('.answer-box').forEach(b => b.classList.remove('show')); document.querySelectorAll('.toggle-btn').forEach(b => b.textContent = '정답 보기'); }
</script>
</body>
</html>


# ========= 14주차 =========

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>모두의 인공지능 - 14주차 문제집</title>
<link rel="stylesheet" href="../theme.css?v=20260605n">


</head>
<body>
<!-- HOME_BTN_START -->
<a class="home-btn" href="../index.html"><span class="arrow">←</span> 메인</a>
<!-- HOME_BTN_END -->

<div class="bg-shapes">
  <div class="shape s1"></div>
  <div class="shape s2"></div>
  <div class="shape s3"></div>
  <div class="shape s4"></div>
</div>

<div class="page">
  <div class="cover">
    <div class="series">모두의 인공지능 · 강태원 교수</div>
    <h1>14주차 문제집</h1>
    <div class="subtitle">이제는 인공생명 · 마지막 강의</div>
    <div class="doctype">문 제 집</div>
    <div class="meta">객관식 5 · 주관식 10 · 서술형 5</div>
  </div>

  <div class="controls">
    <span class="lab">정답 보기</span>
    <button onclick="showAll()">전체 보기</button>
    <button onclick="hideAll()">전체 가리기</button>
    <span class="hint">개별 토글 가능 · 인쇄 시 자동 표시</span>
  </div>

  <h2 class="chapter"><span class="badge">객관식</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 1</span><span class="qtype">객관식</span></div>
    <div class="qbody">보이드(Boid) 알고리즘의 3가지 규칙이 <strong>아닌</strong> 것은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 분리 (Separation)</li>
      <li><span class="opt-num">②</span> 정렬 (Alignment)</li>
      <li><span class="opt-num">③</span> 응집 (Cohesion)</li>
      <li><span class="opt-num">④</span> 회피 (Avoidance)</li>
      <li><span class="opt-num">⑤</span> 답 없음 (모두 보이드 규칙이다)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>④ 회피 (Avoidance)</strong><br>
      <span class="alabel">해설</span>보이드의 3 규칙은 <span class="keyw">분리·정렬·응집</span>뿐. 회피는 보이드 외 다른 알고리즘에서 사용. 분리 규칙 안에 회피 개념이 포함되어 있음.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 2</span><span class="qtype">객관식</span></div>
    <div class="qbody">새 떼를 영어로 표현하는 단어는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> School</li>
      <li><span class="opt-num">②</span> Flock</li>
      <li><span class="opt-num">③</span> Herd</li>
      <li><span class="opt-num">④</span> Pack</li>
      <li><span class="opt-num">⑤</span> Swarm</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② Flock</strong><br>
      <span class="alabel">해설</span>① School = 물고기 떼, ② <span class="keyw">Flock = 새 떼</span>, ③ Herd = 동물 무리(소·영양 등). Pack은 늑대 무리, Swarm은 벌 떼/곤충 떼.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 3</span><span class="qtype">객관식</span></div>
    <div class="qbody">크리스 랭턴(Chris Langton)이 정립한 학문 분야는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 인공지능 (Artificial Intelligence)</li>
      <li><span class="opt-num">②</span> 인공생명 (Artificial Life)</li>
      <li><span class="opt-num">③</span> 유전 알고리즘 (Genetic Algorithm)</li>
      <li><span class="opt-num">④</span> 신경망 (Neural Network)</li>
      <li><span class="opt-num">⑤</span> 떼 지능 (Swarm Intelligence)</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>② 인공생명 (Artificial Life)</strong><br>
      <span class="alabel">해설</span><span class="keyw">크리스 랭턴</span>이 1986년 인공생명을 학문 분야로 정립. 그의 명언: <span class="keyw">"Life as we know it" → "Life as it could be"</span>. 또한 랭턴의 개미(Langton's Ant)도 그의 작품.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 4</span><span class="qtype">객관식</span></div>
    <div class="qbody">강 교수가 강조한, AI가 "모두의 것"이 된 진짜 이유는?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> AI가 중요해졌기 때문에</li>
      <li><span class="opt-num">②</span> 국가 정책 때문에</li>
      <li><span class="opt-num">③</span> 중요할 뿐만 아니라 <strong>쉬워졌기</strong> 때문에</li>
      <li><span class="opt-num">④</span> 컴퓨터가 빨라졌기 때문에</li>
      <li><span class="opt-num">⑤</span> 일자리가 없어지기 때문에</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>③ 중요할 뿐만 아니라 쉬워졌기 때문에</strong><br>
      <span class="alabel">해설</span>중요해도 어려우면 모두 못 함(예: 양자역학). AI는 <span class="keyw">중요한데다 쉬워졌기 때문에</span> 모두가 해야 함. 안 하면 나만 뒤처짐.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 5</span><span class="qtype">객관식</span></div>
    <div class="qbody">랭턴의 개미(Langton's Ant) 규칙 중 <strong>흑색 셀에 도착했을 때</strong>의 행동은?</div>
    <ul class="options">
      <li><span class="opt-num">①</span> 왼쪽으로 90° 회전 후 이동</li>
      <li><span class="opt-num">②</span> 오른쪽으로 90° 회전 후 이동</li>
      <li><span class="opt-num">③</span> 180° 회전 (뒤로 돌아감)</li>
      <li><span class="opt-num">④</span> 그 자리에 정지</li>
      <li><span class="opt-num">⑤</span> 무작위 방향으로 이동</li>
    </ul>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>① 왼쪽으로 90° 회전 후 이동</strong><br>
      <span class="alabel">해설</span>흑색 → 왼쪽, <span class="keyw">백색 → 오른쪽</span>. 그리고 떠난 자리의 색은 반전. 이 규칙으로 시작하면 어떤 초기 상태에서도 결국 <span class="keyw">하이웨이(Highway)</span>가 생성됨.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">주관식</span>10문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 6</span><span class="qtype">주관식</span></div>
    <div class="qbody">1986년에 보이드(Boid) 알고리즘을 발표한 학자의 이름은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>크레이그 레이놀즈 (Craig Reynolds)</strong><br>
      <span class="alabel">해설</span>어린 시절부터 "어떻게 새 떼가 충돌 없이 이동할까"가 궁금했던 학자. 1986년 보이드 알고리즘 논문 발표. 이후 영화·게임의 군집 표현에 표준이 됨.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 7</span><span class="qtype">주관식</span></div>
    <div class="qbody">보이드 규칙 중 <strong>"동료들과 부딪치지 않는 방향으로 이동"</strong>하는 규칙의 이름은? (한국어와 영어 모두)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>분리 (Separation)</strong><br>
      <span class="alabel">해설</span>주변 동료들이 가는 방향의 <span class="keyw">반대 방향</span>으로 이동. 벡터 합의 반대로 계산. 분리만 강하면 떼가 흩어지므로 응집(Cohesion)과 균형이 필요.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 8</span><span class="qtype">주관식</span></div>
    <div class="qbody">보이드 규칙 중 <strong>"동료들과 떨어지지 않게 중심 쪽으로 이동"</strong>하는 규칙의 이름은? (한국어와 영어 모두)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>응집 (Cohesion)</strong><br>
      <span class="alabel">해설</span>주변 동료들의 <span class="keyw">위치의 중심점</span>을 구해 그쪽으로 이동. 분리(Separation)와 정반대 성질의 힘. 둘이 균형을 이뤄야 떼가 유지됨.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 9</span><span class="qtype">주관식</span></div>
    <div class="qbody">횡단보도 가운데에 박혀 있는 말뚝의 진짜 목적은 무엇이며, 그 원리를 무슨 알고리즘으로 시뮬레이션할 수 있는가?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>목적: 보행자가 더 빠르게 지나갈 수 있도록 / 알고리즘: 보이드(Boid)</strong><br>
      <span class="alabel">해설</span>흔히 "보행자 보호"라고 생각하지만 진짜 목적은 <span class="keyw">사람 흐름을 빠르게</span>. 말뚝이 있으면 갈 길이 정리돼 충돌이 줄고 통과 속도가 빨라짐. 보이드 시뮬레이션으로 검증됨.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 10</span><span class="qtype">주관식</span></div>
    <div class="qbody">랭턴의 개미가 만들어내는, 어떤 초기 상태에서도 결국 생성되는 직선 패턴의 이름은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>하이웨이 (Highway, 고속도로)</strong><br>
      <span class="alabel">해설</span>처음엔 무작위로 움직이다가 어느 순간 직선 형태의 하이웨이가 형성됨. <span class="keyw">"항상 생긴다"는 증명도, "안 생기는 초기 상태" 반례도</span> 아직 아무도 찾지 못한 수학 미해결 문제.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 11</span><span class="qtype">주관식</span></div>
    <div class="qbody">지구상의 모든 생명체가 공통적으로 기반하고 있는 화학 결합은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>탄소 결합 (Carbon-based)</strong><br>
      <span class="alabel">해설</span>지구의 모든 생명은 탄소 결합 단백질로 구성. 그러나 이게 생명의 유일한 형태인지는 아직 모름. 랭턴의 <span class="keyw">"Life as it could be"</span> 메시지가 여기 적용됨.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 12</span><span class="qtype">주관식</span></div>
    <div class="qbody">인공생명(ALife)은 <strong>마른 인공생명</strong>과 <strong>젖은 인공생명</strong>으로 나뉜다. 각각의 영어 표현과 예시는?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>마른 인공생명: Dry ALife (로봇·기계) / 젖은 인공생명: Wet ALife (합성 생물·사이보그)</strong><br>
      <span class="alabel">해설</span>강 인공지능 vs 약 인공지능과 비슷한 분류 방식. <span class="keyw">Dry = 기계적</span>, <span class="keyw">Wet = 생물학적</span>. 영화 〈블레이드 러너〉의 레플리컨트는 젖은 인공생명에 해당.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 13</span><span class="qtype">주관식</span></div>
    <div class="qbody">크리스 랭턴의 명언 <strong>"Life as we know it" → "( ? )"</strong>의 빈칸에 들어갈 표현은?</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>"Life as it could be"</strong><br>
      <span class="alabel">해설</span>"우리가 아는 것으로서의 생명" → <span class="keyw">"가능한 것으로서의 생명"</span>. 생명관 확장의 핵심 명언. 우리가 아는 탄소 기반 생명만이 전부가 아닐 수 있다는 주장.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 14</span><span class="qtype">주관식</span></div>
    <div class="qbody">생명의 큰 특징 중, "스스로 질서를 만들어내는 능력"을 무엇이라 하는가? (영어 포함)</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>자기 조직화 (Self-organization)</strong><br>
      <span class="alabel">해설</span>무생물은 열역학 제2법칙에 따라 무질서해짐. 생명은 그 반대 방향으로 스스로 질서를 만듦. 뇌의 시냅스 연결, 유전 알고리즘의 진화, 개미 떼의 길 찾기 모두 자기 조직화 사례.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 15</span><span class="qtype">주관식</span></div>
    <div class="qbody">Keras에서 학습을 시작하는 메서드 이름 <code>model.fit()</code>의 <strong>"fit"</strong>이 의미하는 바를 강의 비유에 따라 설명하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">정답</span><strong>옷을 몸에 맞춰보듯, 데이터에 모델을 맞춰가는 과정</strong><br>
      <span class="alabel">해설</span>Fit = "맞춰본다". 옷 살 때 피팅 룸에서 몸에 맞춰보는 것처럼, 모델의 <span class="keyw">가중치들을 데이터에 맞춰가는 학습</span>. 처음엔 안 맞다가 반복할수록 정확해짐.
    </div>
  </div>

  <h2 class="chapter"><span class="badge">서술형</span>5문항</h2>

  <div class="question">
    <div class="qhead"><span class="qno">문제 16</span><span class="qtype">서술형</span></div>
    <div class="qbody"><strong>보이드(Boid) 알고리즘의 3가지 규칙</strong>을 각각 설명하고, 이 알고리즘이 "단순한 규칙 → 복잡한 행태"의 끝판왕이라 불리는 이유를 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      <span class="keyw">① 분리(Separation)</span>: 주변 동료들의 방향 벡터를 더한 다음 그 반대 방향으로 이동 → 충돌 회피.<br>
      <span class="keyw">② 정렬(Alignment)</span>: 주변 동료들이 가는 방향의 평균에 맞춰 이동 → 줄 맞춤.<br>
      <span class="keyw">③ 응집(Cohesion)</span>: 주변 동료들의 위치의 중심점 방향으로 이동 → 떼 유지.<br><br>
      각 새는 매 순간 이 세 벡터를 계산하고 합산해 다음 이동 방향을 결정한다. 핵심은 <span class="keyw">전체를 지시하는 누군가가 없다는 것</span>. 모든 새가 같은 규칙을 적용하고, 각자 자기 주변(눈치 볼 수 있는 반경) 안의 동료만 본다. 멀리 있는 정보는 무시.<br><br>
      그럼에도 결과는 마치 누가 지휘하는 것처럼 자연스러운 군집 이동이다. 영화·게임의 새 떼, 물고기 떼, 군대 장면이 모두 이 알고리즘으로 만들어진다. 13주차의 세포 자동자보다 더 직관적으로 "단순한 규칙 + 이웃 정보만 → 전역적 복잡 행태"를 보여주기 때문에 <span class="keyw">"단순한 복잡함의 끝판왕"</span>이라 불린다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 17</span><span class="qtype">서술형</span></div>
    <div class="qbody"><strong>인공지능(AI)</strong>과 <strong>인공생명(ALife)</strong>의 관계를 설명하고, 두 분야를 분류하는 방식을 비교하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      인공생명(Artificial Life, ALife)은 <span class="keyw">인공지능을 포함하는 더 큰 학문 분야</span>다. 신경망·딥러닝, 유전 알고리즘, 면역 알고리즘, 떼 지능, 혼돈·프랙털, 세포 자동자 등 우리가 지금까지 배운 모든 분야가 인공생명에 속한다. 인공지능은 "지능"이라는 생명의 한 특징을 다루는 것이고, 인공생명은 그보다 넓은 "생명 전체"의 모방을 다룬다.<br><br>
      <strong>분류 방식 비교:</strong><br>
      인공지능은 <span class="keyw">강 인공지능(Strong AI, 인간 수준) vs 약 인공지능(Weak AI, 특정 작업)</span>으로 나뉜다.<br>
      인공생명은 <span class="keyw">마른 인공생명(Dry ALife, 기계·로봇) vs 젖은 인공생명(Wet ALife, 합성 생물·사이보그)</span>으로 나뉜다.<br><br>
      Dry는 기계적·소프트웨어적 구현(로봇, 시뮬레이션), Wet은 생물학적·화학적 합성(영화 〈블레이드 러너〉의 레플리컨트 같은 사이보그)을 의미한다. 크리스 랭턴이 1986년에 인공생명을 학문 분야로 정립했고, <span class="keyw">"Life as we know it" → "Life as it could be"</span>라는 명언으로 생명관 확장을 주장했다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 18</span><span class="qtype">서술형</span></div>
    <div class="qbody">"생명의 정의"가 명확하지 않은 이유를 설명하고, 강의에서 제시된 <strong>생명의 9가지 특징</strong> 중 5가지 이상을 들어 서술하시오. 또한 <strong>바이러스가 생명인지 아닌지</strong>의 모호함을 함께 논하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      "이런 것이 생명이다"라는 한 마디 정의가 학문적으로 합의되어 있지 않다. 그래서 학자들은 정의 대신 <span class="keyw">특징의 집합</span>으로 생명에 접근한다. 강의에서 제시된 특징:<br>
      ① <span class="keyw">성장(Growth)</span> — 자라남, ② <span class="keyw">자기 재생산(Reproduction)</span> — 새끼를 낳음, ③ <span class="keyw">신진대사(Metabolism)</span> — 물질·에너지 변환, ④ 환경과 상호작용, ⑤ 종속적 구성요소(돌과 다름), ⑥ 자기 회복력(상처 치유), ⑦ <span class="keyw">자기 조직화(Self-organization)</span> — 스스로 질서 생성, ⑧ 진화, ⑨ 정보의 저장소(DNA).<br><br>
      <strong>바이러스의 모호함</strong>: 바이러스는 DNA를 가지고 있어 ② 자기 재생산은 한다(숙주의 몸에서 폭증). 그러나 ③ 신진대사 기관(간·소화기관 등)이 없다 — 그냥 DNA 덩어리. 그래서 어떤 기준에서 보면 생명이고, 어떤 기준에서는 생명이 아니다. 영화 〈어벤져스〉의 타노스가 "랜덤하게 생명체의 절반을 없앴다"고 할 때, 바이러스는 포함되는가? 풀과 나무는? — 답하기 어렵다. 이런 모호함이 바로 <span class="keyw">"생명의 정의"가 학문적으로 어렵다</span>는 증거이며, 랭턴이 "Life as it could be"라며 생명관을 더 넓게 가져야 한다고 주장한 배경이기도 하다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 19</span><span class="qtype">서술형</span></div>
    <div class="qbody">강의에서 "AI가 모두의 것이 된 이유"를 <strong>레고 블록 비유</strong>를 사용해 설명하고, 그로 인해 <strong>새롭게 중요해진 인간의 능력</strong>이 무엇인지 서술하시오.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      옛날 AI는 <span class="keyw">기본 레고 블록만 받고 머리·팔·다리까지 처음부터 만들어야 했다</span>. 영상 처리, 알고리즘 구현, 학습 데이터 수집, 모델 코딩까지 모든 단계가 어려웠다. 그래서 컴퓨터 사이언스 전공자 중에서도 일부 전문가만 할 수 있었다.<br><br>
      오늘날의 AI는 <span class="keyw">완성된 부품(라이브러리·모델·API)들이 다 있고, 그냥 끼워 맞추면 된다</span>. Keras 같은 프레임워크에서는 <code>model.add(Conv2D(...))</code>, <code>model.add(Dense(...))</code> 같은 한 줄짜리 코드로 딥러닝 모델을 구성한다. CIFAR-10 이미지 분류 같은 작업도 몇 줄이면 완성된다. 학습 데이터도 이미 정리된 것들이 인터넷에 잔뜩 있어서 그냥 다운로드만 하면 된다.<br><br>
      이렇게 기술 자체가 쉬워졌기 때문에, 이제는 <span class="keyw">"무엇을 만들지" 생각해내는 능력 = 창의력</span>이 가장 중요해졌다. GPT에게 시키면 되고, 로봇에게 시키면 되는 시대. 시킬 거리를 만들어내는 사람이 경쟁력을 갖는다. 그래서 모든 분야의 사람이 AI를 알아야 하고, 그 분야의 문제를 AI로 해결할 아이디어를 내야 한다. 이것이 강 교수가 말한 <span class="keyw">"모두의 인공지능"</span>의 의미다.
    </div>
  </div>

  <div class="question">
    <div class="qhead"><span class="qno">문제 20</span><span class="qtype">서술형</span></div>
    <div class="qbody">강의 마지막에 제시된 <strong>닭·풀·소 짝짓기 실험</strong>이 의미하는 바를 설명하고, AI 시대를 살아가는 데 있어 <strong>좌뇌·우뇌 균형</strong>이 왜 중요한지 서술하시오. 이를 1주차의 "인공지능 인문학"과 연결지어 논할 것.</div>
    <div class="answer-area"></div>
    <button class="toggle-btn" onclick="toggleAns(this)">정답 보기</button>
    <div class="answer-box">
      <span class="alabel">모범 답안</span>
      <strong>닭·풀·소 짝짓기 실험</strong>(《생각의 지도》): 동양 사람들은 <span class="keyw">소-풀</span>로 묶는 경향(관계 중심: 소가 풀을 먹는다 → 우뇌). 서양 사람들은 <span class="keyw">닭-소</span>로 묶는 경향(분류 중심: 둘 다 동물 → 좌뇌). 정답이 있는 게 아니라 사고 방식의 차이다.<br><br>
      그러나 AI 시대에는 둘 다 필요하다. AI는 인간 지능을 모방하는 것이고, 인간은 좌뇌적 분류·분석과 우뇌적 관계·창의를 모두 한다. AI를 제대로 실현하고 활용하려면 <span class="keyw">두 가지 능력을 모두 갖춰야 한다</span>. 한 손, 한 다리로는 제대로 일할 수 없다.<br><br>
      이는 강의 <strong>1주차 "인공지능 인문학"</strong>의 메시지와 정확히 일치한다. 1주차에서 강조한 것은 "인문학이 중요하니 이공계는 손 떼라"가 아니라, <span class="keyw">"이공계도 인문학을, 문과도 AI를 해야 한다"</span>는 것이었다. 14주차 마지막에 다시 한 번 같은 메시지로 회귀한다 — 산업화 시대에는 분업이 효율적이었지만 AI 시대에는 두 영역을 넘나드는 창의력이 필요하다. 더 이상 문과·이과 구분은 무의미하다.<br><br>
      이것이 강의 전체의 마지막 결론: <span class="keyw">"좌뇌(분류·분석)와 우뇌(관계·창의)를 고르게 사용하지 않으면 살아남을 수 없다"</span>.
    </div>
  </div>

  <div class="nav-links">
    <a href="14주차_학습서.html">학습서로</a>
    <a href="14주차_교과서.html">교과서로</a>
    <a href="../index.html">메인으로</a>
  </div>
</div>
<script>
function toggleAns(btn) { var box = btn.nextElementSibling; box.classList.toggle('show'); btn.textContent = box.classList.contains('show') ? '정답 숨기기' : '정답 보기'; }
function showAll() { document.querySelectorAll('.answer-box').forEach(b => b.classList.add('show')); document.querySelectorAll('.toggle-btn').forEach(b => b.textContent = '정답 숨기기'); }
function hideAll() { document.querySelectorAll('.answer-box').forEach(b => b.classList.remove('show')); document.querySelectorAll('.toggle-btn').forEach(b => b.textContent = '정답 보기'); }
</script>
</body>
</html>
