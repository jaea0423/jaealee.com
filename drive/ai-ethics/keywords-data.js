// 인공지능시대의 윤리 - 통합 키워드 데이터
// 족보: 2024학년도 겨울학기 (2025학년도 여름학기는 다르게 출제됨)
// 총 키워드 수: 218개

const PAST_EXAM = {
  "출처": "2024학년도 겨울학기 족보 (2025학년도 여름학기는 다르게 출제 예정)",
  "객관식": [
    {
      "id": "bopo-mc-01",
      "주차": 3,
      "주제": "편향성",
      "질문": "편향과 편견의 차이를 바르게 설명한 것은?",
      "보기": [
        "편향은 행동보다는 심리적인 고정 관념을 의미한다.",
        "편향은 특정 행동 성향을 자동으로 야기할 수 있다.",
        "편견은 개개인 자신의 국한된 경험과는 무관하게 생겨난다.",
        "편견은 행동 메커니즘 자체가 치우친 상태를 말한다."
      ],
      "정답": "편향은 특정 행동 성향을 자동으로 야기할 수 있다.",
      "해설": "편견(Prejudice)은 심리적 고정관념·태도, 편향(Bias)은 행동 메커니즘·시스템 차원의 치우침. 편향이 직접적인 행동 성향을 자동 유발할 수 있음."
    },
    {
      "id": "bopo-mc-02",
      "주차": 1,
      "주제": "상황윤리(Situation Ethics)/플레처",
      "질문": "플레처의 6개의 기초 원칙에 해당하지 않는 것은?",
      "보기": [
        "사랑의 결정은 상황보다는 관례와 규칙에 따라야 한다.",
        "오직 사랑만이 본래적으로 선하다.",
        "기독교에서 행동을 결정하게 하는 규범은 사랑이다.",
        "목적만이 수단을 정당화한다.",
        "사랑과 정의는 동일한 것이다."
      ],
      "정답": "사랑의 결정은 상황보다는 관례와 규칙에 따라야 한다.",
      "해설": "플레처(Fletcher) 상황윤리는 '규칙이 아닌 상황에 따라 사랑이 결정한다'고 봄. 따라서 '관례·규칙'을 따른다는 것은 정반대 진술."
    },
    {
      "id": "bopo-mc-03",
      "주차": 1,
      "주제": "칸트 윤리(Kantian Ethics)",
      "질문": "칸트의 세 원칙인 보편성, 인격성, 자율성과 그 설명이 잘못 서술된 것은?",
      "보기": [
        "인격성: 너 자신과 다른 사람의 인격을 언제나 목적으로 대우하고, 단순한 수단으로 대우하지 말라.",
        "보편성: 네 의지의 격률이 언제나 보편적 입법의 원리로서 타당할 수 있게끔 행위 하라.",
        "자율성: 모든 존재자는 그 준칙에 의해 항상 보편적 목적의 왕국의 입법적 성원인 것 같이 행위하라."
      ],
      "정답": "자율성: 모든 존재자는 그 준칙에 의해 항상 보편적 목적의 왕국의 입법적 성원인 것 같이 행위하라.",
      "해설": "이 진술은 사실상 '보편성/목적의 왕국'에 가까운 설명. 자율성(Autonomy)은 '의지가 스스로 보편적 법칙을 부여한다'는 의미."
    },
    {
      "id": "bopo-mc-04",
      "주차": 6,
      "주제": "트롤리 딜레마(Trolley Problem)/말레 실험",
      "질문": "버트람 말레(Bertram Malle)는 트롤리 딜레마 실험 연구에서 선로 전환기를 당기는 역할행위자를 '인간', '휴머노이드 로봇', '자동기계 로봇'이라는 세 종류로 설정하였다. 실험에서 선로 전환기를 당기지 않을 경우, 세 종류의 행위자 중에서 가장 도덕적으로 큰 비난을 받은 행위자는?",
      "보기": [
        "자동기계 로봇",
        "인간",
        "휴머노이드 로봇"
      ],
      "정답": "휴머노이드 로봇",
      "해설": "휴머노이드 로봇은 인간형 외관 때문에 인간 수준의 도덕적 판단을 기대받음. 따라서 부작위(전환기 안 당김)에 대해 가장 큰 비난."
    },
    {
      "id": "bopo-mc-05",
      "주차": 9,
      "주제": "데카르트/동물기계론",
      "질문": "동물을 기계의 일종으로 간주한 서양 근대 사상가는?",
      "보기": [
        "르네 데카르트",
        "프란시스 베이컨",
        "토마스 홉스"
      ],
      "정답": "르네 데카르트",
      "해설": "데카르트(Descartes)는 '동물=자동기계(Automata)'로 보았음. 인간만이 영혼·이성을 가진다고 주장."
    },
    {
      "id": "bopo-mc-06",
      "주차": 4,
      "주제": "AI로봇 윤리 프로세스",
      "질문": "AI로봇의 윤리적 프로세스에 관한 설명으로 잘못된 것은?",
      "보기": [
        "로봇의 윤리적 행동은 인지적인 추론과 정서적인 동기가 결합된 결과이다.",
        "로봇의 윤리적 행동은 진리보존적 추론의 결과에 불과하다.",
        "로봇의 행동 결과에 유틸리티만 할당한다면, 인간의 직관과 어긋나는 결과가 도출될 수 있다."
      ],
      "정답": "로봇의 윤리적 행동은 진리보존적 추론의 결과에 불과하다.",
      "해설": "윤리적 행동은 단순 논리적 추론(진리보존)만이 아닌 정서·직관도 포함한 복합적 과정."
    },
    {
      "id": "bopo-mc-07",
      "주차": 3,
      "주제": "설명가능 인공지능(XAI, Explainable AI)",
      "질문": "설명가능 인공지능(Explainable AI)의 효과에 관한 설명으로 적절하지 않은 것은?",
      "보기": [
        "주어진 알고리즘을 예측할 수 있다.",
        "인공지능 모형에 대해 이해 가능해진다.",
        "인간 간의 이해를 증진할 수 있다.",
        "인간 개입 시점을 계획할 수 있다."
      ],
      "정답": "주어진 알고리즘을 예측할 수 있다.",
      "해설": "XAI는 결과·판단의 '이유'를 설명할 수 있게 함. 알고리즘 자체의 출력 예측이 목적이 아님."
    },
    {
      "id": "bopo-mc-08",
      "주차": 3,
      "주제": "AI 발명자 인정 (책무성)",
      "질문": "인공지능이 발명자로 인정받기 위해 고려해야 할 두 가지 사항에 관한 질문을 고르면? (정답 두 개)",
      "보기": [
        "인공지능이 법인격을 가질 수 있는가?",
        "인공지능의 발명품이 고부가가치의 제품인가?",
        "인공지능은 인간과 같은 지능을 갖고 있는가?",
        "인공지능의 창작이 발명이 될 수 있는가?"
      ],
      "정답": [
        "인공지능이 법인격을 가질 수 있는가?",
        "인공지능의 창작이 발명이 될 수 있는가?"
      ],
      "해설": "(1) 법인격(Legal Personhood) 가능성 (2) AI의 창작이 '발명' 범주에 들어가는가, 이 두 가지가 핵심 쟁점."
    },
    {
      "id": "bopo-mc-09",
      "주차": 9,
      "주제": "로봇 회복/로봇 강화(인간향상)",
      "질문": "로봇 회복과 로봇 강화에 관한 설명으로 적절하지 않은 것은?",
      "보기": [
        "로봇 회복이 로봇 강화로 전환되는 경우가 언제인지 불명확하다.",
        "로봇강화는 신체적 인지적 능력을 확장되고 개선된 기계적 전자적 능력으로 교체하는 것을 일컫는다.",
        "로봇회복이란 사라진 신체적 인지적 능력을 같은 기능의 기계적 전자적 능력으로 교체하는 것을 일컫는다.",
        "로봇 기관에서 어떤 기능은 회복하고 어떤 기능은 강화시킬 수 없다."
      ],
      "정답": "로봇 기관에서 어떤 기능은 회복하고 어떤 기능은 강화시킬 수 없다.",
      "해설": "회복(Restoration)과 강화(Enhancement)는 분리되지 않고 동시 가능. 회복이 어느 시점에 강화로 넘어가는지의 경계가 모호함이 쟁점."
    },
    {
      "id": "bopo-mc-10",
      "주차": 3,
      "주제": "책무성(Accountability)과 투명성(Transparency)",
      "질문": "AI윤리에서 책무성과 투명성의 관계에 대한 설명으로 옳지 않은 것은?",
      "보기": [
        "투명성이 높아지면 책무성과 책임 부여가 오히려 어려워진다.",
        "투명성과 책무성은 '관련성'만 있을 뿐 '인과 관계'는 아니다.",
        "투명성이 높아진다고 자동적으로 책무성이 확보되는 것은 아니다.",
        "학습과정의 문제보다는 데이터의 내용이 편향될 수 있으므로 알고리즘 공개를 하여도 어느 부분이 잘못인지 잘 설명되지 않을 수 있다."
      ],
      "정답": "투명성이 높아지면 책무성과 책임 부여가 오히려 어려워진다.",
      "해설": "투명성이 높아진다고 책무성 부여가 어려워지는 것은 아님. 다만 '자동적으로' 확보되지도 않을 뿐. 인과가 아닌 관련성."
    },
    {
      "id": "bopo-mc-11",
      "주차": 10,
      "주제": "자율무기시스템(LAWS)/군사로봇",
      "질문": "다음 중 '군사적 목적을 위한 AI'(자율무기시스템) 사용에 대한 입장이 나머지 것들과 다른 하나는?",
      "보기": [
        "로봇은 복수심과 감정으로 잔혹 행위를 하지 않는다.",
        "군사용 인공지능 기술이 국가 간 군비경쟁을 확장시킨다.",
        "자율무기시스템으로 인적 비용을 줄이면서 전쟁을 부추길 수 있다.",
        "자율무기시스템이 모든 전투원에게 같은 위험을 초래하지 않는다는 점에서 불공정하다."
      ],
      "정답": "로봇은 복수심과 감정으로 잔혹 행위를 하지 않는다.",
      "해설": "정답만 '찬성(긍정)' 입장. 나머지 3개는 모두 '반대(부정)' 입장."
    }
  ],
  "단답형": [
    {
      "id": "bopo-sa-01",
      "주차": 1,
      "주제": "칸트 자율(Autonomy)",
      "질문": "( ? ) 윤리학에서의 자율: 인간이 자기 삶에서 무엇을 할 것인지, 어떤 도덕 규칙에 따라 살아갈 것인지를 결정할 수 있는 능력",
      "정답": "칸트",
      "해설": "칸트(Kant) 윤리학의 핵심 개념. 의지의 자기 입법 능력."
    },
    {
      "id": "bopo-sa-02",
      "주차": 2,
      "주제": "비지도 학습(Unsupervised Learning)",
      "질문": "기계 학습 중 주어진 입력에 대응하는 행동을 취하는 시스템에 대해 적용, 지도학습과 달리 주어진 입력에 대한 출력이 주어지지 않는 학습 유형은?",
      "정답": "비지도 학습",
      "해설": "Unsupervised Learning. 라벨(정답) 없이 패턴을 스스로 발견. 클러스터링·차원축소 등."
    },
    {
      "id": "bopo-sa-03",
      "주차": 10,
      "주제": "휴머노이드(Humanoid)",
      "질문": "다음의 공통으로 밑줄 친 이 로봇을 일컫는 용어를 쓰시오. (얼굴 표정·음성·피부를 똑같이 복사한 로봇, 의료케어 활용 시 인격체로 간주됨)",
      "정답": "휴머노이드",
      "해설": "Humanoid Robot. 인간 외형을 모사한 로봇. 소피아(Sophia) 등."
    },
    {
      "id": "bopo-sa-04",
      "주차": 5,
      "주제": "케임브리지 애널리티카/개인정보 유출",
      "질문": "AI기술의 윤리적 위험의 종류 중에서 '케임브리지 애널리티카 정보 유출 사건'은 어떤 위험의 대표적인 사례인가? ( ? ) 위험",
      "정답": "개인정보 유출",
      "해설": "Cambridge Analytica 사건은 페이스북 사용자 8천만 명 데이터를 정치 광고에 무단 활용한 사건. 대표적 개인정보 유출(Privacy Breach) 사례."
    },
    {
      "id": "bopo-sa-05",
      "주차": 3,
      "주제": "책무성(Accountability)",
      "질문": "인공지능이 단순한 자동 시스템을 넘어 자율 시스템이 되면서 ( ? )의 측면이 더 중요해진다. ( ? )이란 특정 이해 당사자가 자신의 행위와 관련한 책임과 의무를 식별하고 설명하거나 행위의 정당성에 대한 물음에 답하는 것이다.",
      "정답": "책무성",
      "해설": "책무성(Accountability)은 책임(Responsibility)을 넘어 '설명·정당화'까지 포함하는 개념."
    },
    {
      "id": "bopo-sa-06",
      "주차": 3,
      "주제": "설명 가능한 인공지능(XAI)",
      "질문": "( ? ) 인공지능은 판단에 대한 이유를 사람이 이해할 수 있는 방식으로 제시하는 인공지능을 일컫는다. 특정한 판단에 대해 알고리즘의 설계자조차도 그 이유를 설명할 수 없는 '블랙박스' 인공지능과 대비되는 개념이다.",
      "정답": "설명 가능한",
      "해설": "Explainable AI (XAI). 블랙박스(Black Box) AI의 대안."
    },
    {
      "id": "bopo-sa-07",
      "주차": 2,
      "주제": "비전 시스템(Vision System)",
      "질문": "AI시스템의 유형 중에서 '카메라의 이미지 데이터를 지식 표현으로 변환하는 AI의 하위 분야를 가리키는 시스템은?",
      "정답": "비전 시스템",
      "해설": "Computer Vision. 이미지·영상 → 의미 정보로 변환. 객체 인식·얼굴 인식 등."
    },
    {
      "id": "bopo-sa-08",
      "주차": 9,
      "주제": "로봇의 의사결정 단계 (감지→계획→행동)",
      "질문": "인공지능 에이전트는 온라인 또는 시뮬레이션 된 세계에서 작동하는 소프트웨어인 반면에, 로봇은 구체화된 몸을 가지고 실제 세계에서 존재하고 작동한다. 그리고 ( ? ) → 계획 → 행동을 통해 의사결정을 내린다.",
      "정답": "감지",
      "해설": "Sense → Plan → Act (SPA 패러다임). 로봇의 고전적 의사결정 사이클."
    },
    {
      "id": "bopo-sa-09",
      "주차": 4,
      "주제": "감정(Emotion)/안토니오 다마지오",
      "질문": "신경과학자 안토니오 다마지오의 주장에서 공통으로 들어갈 용어. (단세포 생물은 화학 분자에 의존해서 환경 감지·반응 ... ( ? )은 신체 내 무엇이 잘못되었는지 알아내는 방법, 복잡한 네트워크)",
      "정답": "감정",
      "해설": "안토니오 다마지오(Antonio Damasio)는 감정(Emotion)을 신체적·생물학적 신호로 봄. 이성과 감정의 통합 강조."
    }
  ]
};

const KEYWORDS = [
  {
    "keyword": "공리주의",
    "english": "Utilitarianism",
    "category": "윤리이론",
    "file": "01주차/01주차_학습서.html",
    "anchor": "utilitarianism",
    "summary": "결과·효용 중심 윤리. '최대 다수의 최대 행복'. 벤담·밀이 대표.",
    "fromBopo": false
  },
  {
    "keyword": "벤담",
    "english": "Jeremy Bentham",
    "category": "인물",
    "file": "01주차/01주차_학습서.html",
    "anchor": "bentham",
    "summary": "양적 공리주의 창시자. 쾌락 계산법(Hedonic Calculus) 7척도 제시. 판옵티콘(Panopticon)도 그가 제안.",
    "fromBopo": false
  },
  {
    "keyword": "쾌락 계산법",
    "english": "Hedonic Calculus",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "hedonic-calculus",
    "summary": "7가지 척도: 강도·지속성·확실성·근접성·다산성·순수성·범위. 창의성은 포함 안 됨(함정).",
    "fromBopo": false
  },
  {
    "keyword": "손다이크 실험",
    "english": "Thorndike Experiment",
    "category": "사례",
    "file": "01주차/01주차_학습서.html",
    "anchor": "thorndike",
    "summary": "고통의 가격 설문. 캔자스 농장 30만, 지렁이 10만. 샌델이 이를 인용해 공리주의 비판.",
    "fromBopo": false
  },
  {
    "keyword": "마이클 샌델",
    "english": "Michael Sandel",
    "category": "인물",
    "file": "01주차/01주차_학습서.html",
    "anchor": "thorndike",
    "summary": "하버드 정의론 강의로 유명. '모든 것을 가격으로 계산하면 인간의 존엄이 사라진다'고 비판.",
    "fromBopo": false
  },
  {
    "keyword": "밀",
    "english": "John Stuart Mill",
    "category": "인물",
    "file": "01주차/01주차_학습서.html",
    "anchor": "mill",
    "summary": "질적 공리주의. '배부른 돼지보다 배고픈 인간이, 만족한 바보보다 불만족한 소크라테스가 낫다.'",
    "fromBopo": false
  },
  {
    "keyword": "칸트",
    "english": "Immanuel Kant",
    "category": "인물",
    "file": "01주차/01주차_학습서.html",
    "anchor": "kant",
    "summary": "의무론(동기윤리)의 대표 철학자. 정언명령과 3원칙(보편성·인격성·자율성). 자율=의지의 자기 입법.",
    "fromBopo": true
  },
  {
    "keyword": "의무론",
    "english": "Deontology",
    "category": "윤리이론",
    "file": "01주차/01주차_학습서.html",
    "anchor": "kant",
    "summary": "행위의 가치는 결과가 아니라 동기(Motive)에 있다는 윤리이론. 칸트가 대표.",
    "fromBopo": false
  },
  {
    "keyword": "정언명령",
    "english": "Categorical Imperative",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "categorical-imperative",
    "summary": "조건 없는 도덕 명령. '내가 인간이라면 반드시 그렇게 해야 한다.'",
    "fromBopo": false
  },
  {
    "keyword": "보편성",
    "english": "Universality",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "universality",
    "summary": "칸트 3원칙 중 하나. '네 의지의 격률이 보편적 입법의 원리로서 타당할 수 있게끔 행위 하라.'",
    "fromBopo": true
  },
  {
    "keyword": "인격성",
    "english": "Humanity",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "humanity",
    "summary": "칸트 3원칙 중 하나. 인간을 단순한 수단이 아니라 목적 그 자체로 대하라.",
    "fromBopo": true
  },
  {
    "keyword": "자율성",
    "english": "Autonomy",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "autonomy",
    "summary": "칸트 3원칙. 의지의 자기 입법 능력. 인간이 자기 삶의 도덕 규칙을 결정할 수 있는 능력.",
    "fromBopo": true
  },
  {
    "keyword": "코페르니쿠스적 전환",
    "english": "Copernican Revolution",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "kant",
    "summary": "칸트의 인식 전환. 인식 능력 안의 선험적 형식이 경험을 구성한다는 입장.",
    "fromBopo": false
  },
  {
    "keyword": "플레처",
    "english": "Joseph Fletcher",
    "category": "인물",
    "file": "01주차/01주차_학습서.html",
    "anchor": "fletcher",
    "summary": "상황윤리(Situation Ethics) 창시자. 율법주의·무율법주의 중간의 제3의 길. 사랑이 유일한 절대 기준.",
    "fromBopo": true
  },
  {
    "keyword": "상황윤리",
    "english": "Situation Ethics",
    "category": "윤리이론",
    "file": "01주차/01주차_학습서.html",
    "anchor": "situation-ethics",
    "summary": "플레처가 제시. 사랑(Agape)이 유일한 절대 기준. 6원칙으로 구성.",
    "fromBopo": true
  },
  {
    "keyword": "사랑",
    "english": "Agape",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "fletcher",
    "summary": "상황윤리의 유일한 기준. 감정이 아니라 의지의 행위.",
    "fromBopo": false
  },
  {
    "keyword": "플레처 6원칙",
    "english": "Fletcher's Six Principles",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "fletcher-6",
    "summary": "(1) 사랑만이 본래적 선 (2) 사랑이 궁극 규범 (3) 사랑=정의 (4) 사랑은 의지의 행위 (5) 목적이 수단 정당화 (6) 상황에 따라 결정.",
    "fromBopo": true
  },
  {
    "keyword": "율법주의",
    "english": "Legalism",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "situation-ethics",
    "summary": "규칙만 남은 윤리. 플레처가 비판한 한 극단.",
    "fromBopo": false
  },
  {
    "keyword": "무율법주의",
    "english": "Antinomianism",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "situation-ethics",
    "summary": "기준이 사라진 윤리. 플레처가 비판한 다른 극단.",
    "fromBopo": false
  },
  {
    "keyword": "판옵티콘",
    "english": "Panopticon",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "bentham",
    "summary": "벤담이 제안한 원형 감시 시설. '관찰당할 수 있다면 스스로 도덕적으로 행동한다.' 감시 도시 사례에서 등장.",
    "fromBopo": false
  },
  {
    "keyword": "절차적 사랑",
    "english": "Procedural Love",
    "category": "개념",
    "file": "01주차/01주차_학습서.html",
    "anchor": "fletcher",
    "summary": "AI 윤리에 적용된 상황윤리. 예외를 허용하되 이유를 남기고 다중 검증·사후평가로 갱신.",
    "fromBopo": false
  },
  {
    "keyword": "트롤리 딜레마",
    "english": "Trolley Problem",
    "category": "사례",
    "file": "01주차/01주차_학습서.html",
    "anchor": "utilitarianism",
    "summary": "자율주행차 충돌 선택의 윤리적 딜레마. 1주차에서 공리주의 사례로, 6주차에서 본격 다룸.",
    "fromBopo": true
  },
  {
    "keyword": "존 메카시",
    "english": "John McCarthy",
    "category": "인물",
    "file": "02주차/02주차_학습서.html",
    "anchor": "mccarthy",
    "summary": "1956년 다트머스 회의에서 'AI'라는 용어를 처음 공식 사용. '모든 지적 행위는 원칙적으로 기계에 의해 모방될 수 있다.'",
    "fromBopo": false
  },
  {
    "keyword": "다트머스 회의",
    "english": "Dartmouth Conference",
    "category": "역사",
    "file": "02주차/02주차_학습서.html",
    "anchor": "mccarthy",
    "summary": "1956년 AI라는 개념이 공식 출범한 학술 회의.",
    "fromBopo": false
  },
  {
    "keyword": "러셀 노빅",
    "english": "Russell & Norvig",
    "category": "인물",
    "file": "02주차/02주차_학습서.html",
    "anchor": "russell-norvig",
    "summary": "AI를 '목표지향적 행동을 수행하는 시스템'으로 정의. 지능적 에이전트 개념.",
    "fromBopo": false
  },
  {
    "keyword": "지능적 에이전트",
    "english": "Intelligent Agent",
    "category": "개념",
    "file": "02주차/02주차_학습서.html",
    "anchor": "russell-norvig",
    "summary": "환경을 인식하고 목표를 향해 합리적으로 행동하는 시스템.",
    "fromBopo": false
  },
  {
    "keyword": "마이신",
    "english": "MYCIN",
    "category": "사례",
    "file": "02주차/02주차_학습서.html",
    "anchor": "mycin",
    "summary": "1970년대 스탠퍼드의 규칙기반 의료진단 시스템. 450개 규칙. AI의 겨울로 이어진 사례.",
    "fromBopo": false
  },
  {
    "keyword": "AI의 겨울",
    "english": "AI Winter",
    "category": "역사",
    "file": "02주차/02주차_학습서.html",
    "anchor": "stages",
    "summary": "규칙기반 AI의 한계로 인한 첫 번째 침체기.",
    "fromBopo": false
  },
  {
    "keyword": "알파고",
    "english": "AlphaGo",
    "category": "사례",
    "file": "02주차/02주차_학습서.html",
    "anchor": "alphago",
    "summary": "2016년 등장한 학습기반 AI의 상징. 자가 대국으로 전략 발전 (강화학습).",
    "fromBopo": false
  },
  {
    "keyword": "약인공지능",
    "english": "ANI (Artificial Narrow Intelligence)",
    "category": "유형",
    "file": "02주차/02주차_학습서.html",
    "anchor": "ani",
    "summary": "한 가지 작업만 잘하는 좁은 지능. 현재 거의 모든 AI(ChatGPT 포함)가 여기 속함.",
    "fromBopo": false
  },
  {
    "keyword": "강인공지능",
    "english": "AGI (Artificial General Intelligence)",
    "category": "유형",
    "file": "02주차/02주차_학습서.html",
    "anchor": "ani",
    "summary": "인간처럼 다양한 문제를 스스로 해결하는 범용 지능. 아직 미구현.",
    "fromBopo": false
  },
  {
    "keyword": "초인공지능",
    "english": "ASI (Artificial Super Intelligence)",
    "category": "유형",
    "file": "02주차/02주차_학습서.html",
    "anchor": "ani",
    "summary": "인간을 능가하는 가설적 지능. 닉 보스트롬이 위험성 경고.",
    "fromBopo": false
  },
  {
    "keyword": "닉 보스트롬",
    "english": "Nick Bostrom",
    "category": "인물",
    "file": "02주차/02주차_학습서.html",
    "anchor": "bostrom",
    "summary": "초인공지능(ASI)의 위험을 경고. 'AI가 목표를 설정하는 순간 인간은 그 목표의 일부가 된다.' 기능 4단계 분류.",
    "fromBopo": false
  },
  {
    "keyword": "지도학습",
    "english": "Supervised Learning",
    "category": "기술",
    "file": "02주차/02주차_학습서.html",
    "anchor": "unsupervised",
    "summary": "정답(라벨)이 있는 데이터로 학습하는 머신러닝 방법.",
    "fromBopo": false
  },
  {
    "keyword": "비지도학습",
    "english": "Unsupervised Learning",
    "category": "기술",
    "file": "02주차/02주차_학습서.html",
    "anchor": "unsupervised",
    "summary": "주어진 입력에 대한 출력(정답)이 주어지지 않는 학습 유형. 클러스터링·차원축소. ★ 족보 단답형 출제.",
    "fromBopo": true
  },
  {
    "keyword": "강화학습",
    "english": "Reinforcement Learning",
    "category": "기술",
    "file": "02주차/02주차_학습서.html",
    "anchor": "unsupervised",
    "summary": "행동의 보상·벌점으로 학습. 알파고 자가 대국 사용.",
    "fromBopo": false
  },
  {
    "keyword": "비전 시스템",
    "english": "Vision System / Computer Vision",
    "category": "기술",
    "file": "02주차/02주차_학습서.html",
    "anchor": "vision",
    "summary": "카메라의 이미지 데이터를 지식 표현으로 변환하는 AI 하위 분야. ★ 족보 단답형 출제.",
    "fromBopo": true
  },
  {
    "keyword": "딥블루",
    "english": "Deep Blue",
    "category": "사례",
    "file": "02주차/02주차_학습서.html",
    "anchor": "bostrom",
    "summary": "체스 챔피언을 이긴 단순 반응형 AI. 기억 없이 매번 새로 계산.",
    "fromBopo": false
  },
  {
    "keyword": "단순 반응형",
    "english": "Reactive AI",
    "category": "유형",
    "file": "02주차/02주차_학습서.html",
    "anchor": "bostrom",
    "summary": "보스트롬 4단계 ①. 기억 없이 즉각 반응. 딥블루.",
    "fromBopo": false
  },
  {
    "keyword": "기억형",
    "english": "Limited Memory",
    "category": "유형",
    "file": "02주차/02주차_학습서.html",
    "anchor": "bostrom",
    "summary": "보스트롬 4단계 ②. 과거 데이터 저장·활용. 자율주행·추천.",
    "fromBopo": false
  },
  {
    "keyword": "이론형",
    "english": "Theory of Mind",
    "category": "유형",
    "file": "02주차/02주차_학습서.html",
    "anchor": "bostrom",
    "summary": "보스트롬 4단계 ③. 감정·의도 이해 시도. 미완성.",
    "fromBopo": false
  },
  {
    "keyword": "자기인식형",
    "english": "Self-Aware AI",
    "category": "유형",
    "file": "02주차/02주차_학습서.html",
    "anchor": "bostrom",
    "summary": "보스트롬 4단계 ④. 가설적 단계.",
    "fromBopo": false
  },
  {
    "keyword": "AI 한계",
    "english": "Limits of AI",
    "category": "개념",
    "file": "02주차/02주차_학습서.html",
    "anchor": "limits",
    "summary": "인식적·도덕적·감정적(존재론적) 세 한계.",
    "fromBopo": false
  },
  {
    "keyword": "규칙기반 AI",
    "english": "Symbolic AI",
    "category": "유형",
    "file": "02주차/02주차_학습서.html",
    "anchor": "stages",
    "summary": "사람이 모든 규칙을 입력하는 1단계 AI. 'If A then B' 구조.",
    "fromBopo": false
  },
  {
    "keyword": "생성 기반 AI",
    "english": "Generative AI",
    "category": "유형",
    "file": "02주차/02주차_학습서.html",
    "anchor": "stages",
    "summary": "학습한 지식으로 새로운 문장·이미지·음악 창조. ChatGPT, Midjourney.",
    "fromBopo": false
  },
  {
    "keyword": "편향",
    "english": "Bias",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "prejudice",
    "summary": "시스템이 자동으로 한쪽으로 기울어지는 구조적 성향. 특정 행동 성향을 자동으로 야기. ★ 족보 출제.",
    "fromBopo": true
  },
  {
    "keyword": "편견",
    "english": "Prejudice",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "prejudice",
    "summary": "인간의 심리적 고정관념. 개인 경험에서 비롯됨. 편향(Bias)과 구분.",
    "fromBopo": true
  },
  {
    "keyword": "알고리즘 편향",
    "english": "Algorithmic Bias",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "algo-bias",
    "summary": "데이터 선택·수집·분류·활용 또는 알고리즘 구성에서 공평하지 않은 기준이 개입되는 현상.",
    "fromBopo": false
  },
  {
    "keyword": "COMPAS",
    "english": "COMPAS",
    "category": "사례",
    "file": "03주차/03주차_학습서.html",
    "anchor": "compas",
    "summary": "플로리다 재범 예측 프로그램. 인종 변수 없이도 흑인 고위험 분류 확률 2배. 대리 변수(Proxy) 사례.",
    "fromBopo": false
  },
  {
    "keyword": "EVAAS",
    "english": "EVAAS",
    "category": "사례",
    "file": "03주차/03주차_학습서.html",
    "anchor": "compas",
    "summary": "교사 평가 시스템. 블랙박스로 점수 이유 불명. AI 점수만으로 교사 해임 사례.",
    "fromBopo": false
  },
  {
    "keyword": "애플카드",
    "english": "Apple Card",
    "category": "사례",
    "file": "03주차/03주차_학습서.html",
    "anchor": "compas",
    "summary": "2019년. 동일 신용·소득 부부 중 여성이 남성의 1/10 한도. 골드만삭스 발행. 결정 과정 설명 불가.",
    "fromBopo": false
  },
  {
    "keyword": "GDPR",
    "english": "General Data Protection Regulation",
    "category": "법률",
    "file": "03주차/03주차_학습서.html",
    "anchor": "bias",
    "summary": "2018년 EU 일반 데이터 보호 규정. AI 결정 근거 요구권 + 데이터 삭제권. AI 윤리를 제도화한 첫 사례.",
    "fromBopo": false
  },
  {
    "keyword": "투명성",
    "english": "Transparency",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "trans-acc",
    "summary": "AI 판단 과정이 외부에서 이해 가능한 정도. 책무성의 출발점이지만 자동 보장은 아님.",
    "fromBopo": true
  },
  {
    "keyword": "블랙박스",
    "english": "Black Box",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "blackbox",
    "summary": "입력·출력은 보이지만 판단 과정이 가려진 AI. 딥러닝의 본질적 한계.",
    "fromBopo": false
  },
  {
    "keyword": "XAI",
    "english": "Explainable AI",
    "category": "기술",
    "file": "03주차/03주차_학습서.html",
    "anchor": "xai",
    "summary": "설명 가능한 인공지능. 판단 이유를 사람이 이해할 수 있게 제시. 2017년 DARPA 공식 제안. 블랙박스의 반대. ★ 족보 출제.",
    "fromBopo": true
  },
  {
    "keyword": "설명 가능한 인공지능",
    "english": "Explainable AI (XAI)",
    "category": "기술",
    "file": "03주차/03주차_학습서.html",
    "anchor": "xai",
    "summary": "AI의 판단 이유를 사람이 이해할 수 있는 방식으로 제시. 블랙박스의 반대 개념. ★ 족보 단답 출제.",
    "fromBopo": true
  },
  {
    "keyword": "DARPA",
    "english": "DARPA",
    "category": "기관",
    "file": "03주차/03주차_학습서.html",
    "anchor": "xai",
    "summary": "미국 국방고등연구계획국. 2017년 XAI 공식 제안.",
    "fromBopo": false
  },
  {
    "keyword": "Optimizing Mind",
    "english": "Optimizing Mind",
    "category": "사례",
    "file": "03주차/03주차_학습서.html",
    "anchor": "xai",
    "summary": "AI 신경과학 스타트업. AI 신경망을 인간 뇌 구조와 대응시켜 결정 경로 시각화.",
    "fromBopo": false
  },
  {
    "keyword": "책임",
    "english": "Responsibility",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "responsibility",
    "summary": "법적·제도적 귀속(누가 잘못했는가). 사후적 개념.",
    "fromBopo": false
  },
  {
    "keyword": "책무성",
    "english": "Accountability",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "accountability",
    "summary": "행위·결정의 설명·정당화 의무. 사전적 개념. AI 자율 시스템에서 더 중요해짐. ★ 족보 단답 출제.",
    "fromBopo": true
  },
  {
    "keyword": "분산된 책임",
    "english": "Distributed Responsibility",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "responsibility",
    "summary": "자율 시스템에서 설계자·제작자·데이터 제공자·운영자에 책임이 흩어지는 현상.",
    "fromBopo": false
  },
  {
    "keyword": "지능형 재산",
    "english": "Intelligent Property",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "responsibility",
    "summary": "보조형 AI(자율주행 레벨 2~3)의 법적 지위. 인간 책임 유지. IEEE 권고.",
    "fromBopo": false
  },
  {
    "keyword": "DEKA Arm",
    "english": "DEKA Arm",
    "category": "사례",
    "file": "03주차/03주차_학습서.html",
    "anchor": "responsibility",
    "summary": "딘 카멘의 데카 연구소 인공지능 의수. 인간 신경-AI 결합. 물건/신체 법적 쟁점.",
    "fromBopo": false
  },
  {
    "keyword": "법인격",
    "english": "Legal Personhood",
    "category": "법률",
    "file": "03주차/03주차_학습서.html",
    "anchor": "inventor",
    "summary": "AI 발명자 인정의 핵심 쟁점 1. AI에게 법인격 부여 가능성. ★ 족보 출제.",
    "fromBopo": true
  },
  {
    "keyword": "AI 발명자",
    "english": "AI Inventor",
    "category": "법률",
    "file": "03주차/03주차_학습서.html",
    "anchor": "inventor",
    "summary": "AI가 발명자로 인정받기 위한 두 쟁점: (1) 법인격 (2) 창작이 발명인가. ★ 족보 객관식 출제.",
    "fromBopo": true
  },
  {
    "keyword": "책무성 6조건",
    "english": "Six Conditions for Accountability",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "accountability",
    "summary": "사용 목적·데이터 소스·알고리즘 구조·프로세스 그래프·사용자 인터페이스·출력 단계.",
    "fromBopo": false
  },
  {
    "keyword": "대리 변수",
    "english": "Proxy Variable",
    "category": "개념",
    "file": "03주차/03주차_학습서.html",
    "anchor": "compas",
    "summary": "민감 변수(인종 등) 대신 그와 강하게 연관된 변수(거주지 등)가 작동해 결과를 편향시키는 현상.",
    "fromBopo": false
  },
  {
    "keyword": "자율성",
    "english": "Autonomy",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "autonomy",
    "summary": "스스로 규칙을 만들고 그에 따라 행동하는 능력. 자기통제·자기결정·책임.",
    "fromBopo": false
  },
  {
    "keyword": "자기통제",
    "english": "Self-control",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "autonomy",
    "summary": "외부 압력에 휘둘리지 않고 행동을 조절.",
    "fromBopo": false
  },
  {
    "keyword": "자기결정",
    "english": "Self-determination",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "autonomy",
    "summary": "내가 목적을 정함.",
    "fromBopo": false
  },
  {
    "keyword": "자기 입법",
    "english": "Self-legislation",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "kant-auto",
    "summary": "칸트의 자율성. 스스로 법칙을 세우는 능력. 목적의 왕국으로 이어짐.",
    "fromBopo": false
  },
  {
    "keyword": "목적의 왕국",
    "english": "Kingdom of Ends",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "kant-auto",
    "summary": "칸트가 그린 자율적 존재들의 공동체. 서로를 목적으로 대우.",
    "fromBopo": false
  },
  {
    "keyword": "허락된 자율성",
    "english": "Permitted Autonomy",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "ai-auto-levels",
    "summary": "AI의 자율성은 진정한 자율이 아니라 인간이 부여한 목적의 그림자.",
    "fromBopo": false
  },
  {
    "keyword": "조건부 자율성",
    "english": "Conditional Autonomy",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "ai-auto-levels",
    "summary": "AI 자율성 레벨 3. 현재 대부분의 AI(자율주행·추천·의료 AI).",
    "fromBopo": false
  },
  {
    "keyword": "아시모프",
    "english": "Isaac Asimov",
    "category": "인물",
    "file": "04주차/04주차_학습서.html",
    "anchor": "asimov",
    "summary": "로봇 3원칙을 제시한 과학소설 작가. 안전→복종→자기보호.",
    "fromBopo": false
  },
  {
    "keyword": "로봇 3원칙",
    "english": "Three Laws of Robotics",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "asimov",
    "summary": "(1) 인간에 해 끼치지 않음 (2) 명령 복종 (3) 자기 보호. 현실에서 충돌.",
    "fromBopo": false
  },
  {
    "keyword": "진리보존적 추론",
    "english": "Truth-preserving Reasoning",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "robot-ethics",
    "summary": "AI 로봇 윤리에서 단순 논리만으로는 부족. 정서·직관 결합 필요. ★ 족보 함정 키워드.",
    "fromBopo": true
  },
  {
    "keyword": "LAWS",
    "english": "Lethal Autonomous Weapons Systems",
    "category": "기술",
    "file": "04주차/04주차_학습서.html",
    "anchor": "laws",
    "summary": "치명적 자율 무기 시스템. AI가 스스로 표적 결정. UN 금지 논의. 10주차에서 본격 다룸.",
    "fromBopo": false
  },
  {
    "keyword": "Human in the Loop",
    "english": "Human in the Loop",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "laws",
    "summary": "인간이 AI 판단 과정에 개입할 수 있는 구조. 고위험 영역에서 필수.",
    "fromBopo": false
  },
  {
    "keyword": "하이브리드 자율성",
    "english": "Hybrid Autonomy",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "laws",
    "summary": "AI가 판단을 보조하고 인간이 감독·결정하는 구조.",
    "fromBopo": false
  },
  {
    "keyword": "자동화된 차별",
    "english": "Automated Discrimination",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "laws",
    "summary": "금융 AI 등에서 발생. AI는 차별하지 않지만 데이터가 차별해왔음.",
    "fromBopo": false
  },
  {
    "keyword": "전자인격",
    "english": "Electronic Person",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "electronic-person",
    "summary": "EU 발 책임 귀속 논의. '전자인간'이 아닌 '법적 인격'. AI에게 도덕적 인격 부여가 아닌 법적 책임 단위 설정.",
    "fromBopo": false
  },
  {
    "keyword": "법적 인격",
    "english": "Legal Personhood",
    "category": "법률",
    "file": "04주차/04주차_학습서.html",
    "anchor": "moral-legal",
    "summary": "법적 권리·책임 주체 자격. 인간이 아닌 법인(Corporation)도 가짐. ★ 3주차 AI 발명자와 연결.",
    "fromBopo": true
  },
  {
    "keyword": "도덕적 인격",
    "english": "Moral Personhood",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "moral-legal",
    "summary": "도덕적 고려 대상 자격. 고통·감정·복지 기준.",
    "fromBopo": false
  },
  {
    "keyword": "도덕적 객체",
    "english": "Moral Object",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "moral-legal",
    "summary": "도덕적 고려 대상이지만 책임은 묻지 않는 존재 (어린아이·동물).",
    "fromBopo": false
  },
  {
    "keyword": "도덕적 주체",
    "english": "Moral Subject",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "moral-legal",
    "summary": "옳고 그름을 구분하고 책임지는 존재. 성인 인간.",
    "fromBopo": false
  },
  {
    "keyword": "데카르트",
    "english": "René Descartes",
    "category": "인물",
    "file": "04주차/04주차_학습서.html",
    "anchor": "descartes",
    "summary": "동물을 자동기계(Automata)로 봄. 인간만이 영혼·이성. ★ 족보 출제 (9주차 객관식).",
    "fromBopo": true
  },
  {
    "keyword": "동물기계론",
    "english": "Animal Machine Theory",
    "category": "개념",
    "file": "04주차/04주차_학습서.html",
    "anchor": "descartes",
    "summary": "데카르트의 입장. 동물의 고통 반응은 기계적 반사.",
    "fromBopo": true
  },
  {
    "keyword": "오랑우탄 판결",
    "english": "Orangutan Ruling",
    "category": "사례",
    "file": "04주차/04주차_학습서.html",
    "anchor": "orangutan",
    "summary": "2014년 아르헨티나. 오랑우탄을 비인간 인격으로 인정.",
    "fromBopo": false
  },
  {
    "keyword": "존 로크",
    "english": "John Locke",
    "category": "인물",
    "file": "04주차/04주차_학습서.html",
    "anchor": "moral-legal",
    "summary": "「인간 지성론」. 인격을 사고능력·자기인식·책임능력으로 정의 (생물학적 인간과 분리).",
    "fromBopo": false
  },
  {
    "keyword": "법인",
    "english": "Corporation / Legal Person",
    "category": "법률",
    "file": "04주차/04주차_학습서.html",
    "anchor": "moral-legal",
    "summary": "인간이 아닌 조직에 법적 인격을 부여한 사례. 전자인격 논의의 비교 대상.",
    "fromBopo": false
  },
  {
    "keyword": "안토니오 다마지오",
    "english": "Antonio Damasio",
    "category": "인물",
    "file": "04주차/04주차_학습서.html",
    "anchor": "moral-legal",
    "summary": "신경과학자. 감정(Emotion)을 단세포 생물의 환경 감지 반응으로 봄. 감정은 신체적·생물학적 신호의 복잡한 네트워크. ★ 족보 단답 출제.",
    "fromBopo": true
  },
  {
    "keyword": "다마지오",
    "english": "Damasio",
    "category": "인물",
    "file": "04주차/04주차_학습서.html",
    "anchor": "moral-legal",
    "summary": "신경과학자 안토니오 다마지오. 족보 단답: 단세포 생물은 화학분자에 의존해 환경 감지·반응. ( ? )은 신체 내 잘못된 점을 알아내는 방법, 복잡한 네트워크 → 답: 감정.",
    "fromBopo": true
  },
  {
    "keyword": "윤리적 위험",
    "english": "Ethical Risk",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "risk",
    "summary": "법적으로 합법이어도 사회적 비난·평판 붕괴 부르는 위험.",
    "fromBopo": false
  },
  {
    "keyword": "케임브리지 애널리티카",
    "english": "Cambridge Analytica",
    "category": "사례",
    "file": "05주차/05주차_학습서.html",
    "anchor": "cambridge",
    "summary": "페이스북 사용자 8천만 명 데이터 무단 활용. 개인정보 유출 위험의 대표. ★ 족보 단답 출제.",
    "fromBopo": true
  },
  {
    "keyword": "개인정보 유출",
    "english": "Privacy Breach",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "cambridge",
    "summary": "케임브리지 애널리티카가 대표 사례. ★ 족보 단답 답.",
    "fromBopo": true
  },
  {
    "keyword": "라나플라자",
    "english": "Rana Plaza",
    "category": "사례",
    "file": "05주차/05주차_학습서.html",
    "anchor": "risk",
    "summary": "2013년 방글라데시 의류 공장 붕괴. 공급망 윤리 부상.",
    "fromBopo": false
  },
  {
    "keyword": "코발트 광산",
    "english": "Cobalt Mining",
    "category": "사례",
    "file": "05주차/05주차_학습서.html",
    "anchor": "risk",
    "summary": "아동노동 문제. 비난은 광산이 아닌 애플·삼성·테슬라로.",
    "fromBopo": false
  },
  {
    "keyword": "셸 사례",
    "english": "Shell Malampaya / Brent Spar",
    "category": "사례",
    "file": "05주차/05주차_학습서.html",
    "anchor": "shell",
    "summary": "셸의 3억$ 우회 송유관. 윤리=보험 사례. 브렌트 스파르 사건 학습.",
    "fromBopo": false
  },
  {
    "keyword": "덕덕고",
    "english": "DuckDuckGo",
    "category": "사례",
    "file": "05주차/05주차_학습서.html",
    "anchor": "duckduckgo",
    "summary": "프라이버시 보호를 마케팅 전략으로 만든 검색 엔진.",
    "fromBopo": false
  },
  {
    "keyword": "필립 코틀러",
    "english": "Philip Kotler",
    "category": "인물",
    "file": "05주차/05주차_학습서.html",
    "anchor": "kotler",
    "summary": "마케팅 정의: 고객 가치 창출 + 관계 구축 + 상응 보상.",
    "fromBopo": false
  },
  {
    "keyword": "대리광고",
    "english": "Surrogate Advertising",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "ads6",
    "summary": "술·담배 광고 금지 우회. 같은 로고로 다른 상품 광고.",
    "fromBopo": false
  },
  {
    "keyword": "타겟",
    "english": "Target",
    "category": "사례",
    "file": "05주차/05주차_학습서.html",
    "anchor": "target",
    "summary": "AI가 10대 딸 임신을 가족보다 먼저 알아낸 미국 유통기업 사례.",
    "fromBopo": false
  },
  {
    "keyword": "필터 버블",
    "english": "Filter Bubble",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "target",
    "summary": "추천 알고리즘이 비슷한 취향만 반복 노출하는 현상.",
    "fromBopo": false
  },
  {
    "keyword": "분배 정의",
    "english": "Distributive Justice",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "justice",
    "summary": "누가 얼마나 가져야 하는가의 사회 규칙.",
    "fromBopo": false
  },
  {
    "keyword": "호메로스",
    "english": "Homer",
    "category": "인물",
    "file": "05주차/05주차_학습서.html",
    "anchor": "justice",
    "summary": "'각자에게 각자의 몫' — 분배 정의의 직관.",
    "fromBopo": false
  },
  {
    "keyword": "아리스토텔레스",
    "english": "Aristotle",
    "category": "인물",
    "file": "05주차/05주차_학습서.html",
    "anchor": "aristotle",
    "summary": "비례적 평등(Proportional Equality). 기여·능력에 비례한 분배.",
    "fromBopo": false
  },
  {
    "keyword": "비례적 평등",
    "english": "Proportional Equality",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "aristotle",
    "summary": "아리스토텔레스. 동등한 사람에게 동등한 몫.",
    "fromBopo": false
  },
  {
    "keyword": "롤즈",
    "english": "John Rawls",
    "category": "인물",
    "file": "05주차/05주차_학습서.html",
    "anchor": "rawls",
    "summary": "정의론. 무지의 베일 + 2원칙(평등한 자유 + 기회균등·차등).",
    "fromBopo": false
  },
  {
    "keyword": "무지의 베일",
    "english": "Veil of Ignorance",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "rawls",
    "summary": "롤즈의 사유 실험. 자신의 정체성을 모른 채 사회 규칙을 정하면 공정한 원칙 선택.",
    "fromBopo": false
  },
  {
    "keyword": "원초적 상황",
    "english": "Original Position",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "rawls",
    "summary": "롤즈가 제안한 가상 출발점.",
    "fromBopo": false
  },
  {
    "keyword": "차등의 원칙",
    "english": "Difference Principle",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "rawls",
    "summary": "롤즈 제2원칙. 불평등은 최소 수혜자에게 최대 이득이 돌아갈 때만 정당.",
    "fromBopo": false
  },
  {
    "keyword": "최소 수혜자",
    "english": "Least Advantaged",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "rawls",
    "summary": "롤즈가 우선권을 주는 사회적 약자 집단.",
    "fromBopo": false
  },
  {
    "keyword": "기회 균등",
    "english": "Fair Equality of Opportunity",
    "category": "개념",
    "file": "05주차/05주차_학습서.html",
    "anchor": "rawls",
    "summary": "롤즈 제2원칙 (a). 직업·지위는 모두에게 열림.",
    "fromBopo": false
  },
  {
    "keyword": "로봇세",
    "english": "Robot Tax",
    "category": "정책",
    "file": "05주차/05주차_학습서.html",
    "anchor": "robot-tax",
    "summary": "AI·로봇 자동화 기업에 과세해 실직자·취약계층 지원. 잘못 설계 시 격차 확대 우려.",
    "fromBopo": false
  },
  {
    "keyword": "데이터 배당",
    "english": "Data Dividend",
    "category": "정책",
    "file": "05주차/05주차_학습서.html",
    "anchor": "robot-tax",
    "summary": "데이터 제공자에 대한 재분배 정책.",
    "fromBopo": false
  },
  {
    "keyword": "SAE 자율주행 6단계",
    "english": "SAE J3016 Levels 0-5",
    "category": "기술",
    "file": "06주차/06주차_학습서.html",
    "anchor": "sae",
    "summary": "0=자동화없음, 1=한가지보조, 2=다기능보조(책임인간), 3=조건부자율, 4=고도자율, 5=완전자율.",
    "fromBopo": false
  },
  {
    "keyword": "자율주행 4단계",
    "english": "Sensor-Perception-Decision-Control",
    "category": "기술",
    "file": "06주차/06주차_학습서.html",
    "anchor": "sensors",
    "summary": "센서→인지→판단→제어. 자율주행차의 기본 작동 구조.",
    "fromBopo": false
  },
  {
    "keyword": "트롤리 딜레마",
    "english": "Trolley Problem",
    "category": "사례",
    "file": "06주차/06주차_학습서.html",
    "anchor": "trolley",
    "summary": "필리파 풋(1967)의 사고 실험. 자율주행 시대에 실제 알고리즘 문제로 부상.",
    "fromBopo": true
  },
  {
    "keyword": "필리파 풋",
    "english": "Philippa Foot",
    "category": "인물",
    "file": "06주차/06주차_학습서.html",
    "anchor": "trolley",
    "summary": "1967년 트롤리 딜레마 원형 제시한 영국 철학자.",
    "fromBopo": false
  },
  {
    "keyword": "버트람 말레",
    "english": "Bertram Malle",
    "category": "인물",
    "file": "06주차/06주차_학습서.html",
    "anchor": "malle",
    "summary": "트롤리 딜레마 실험. 인간/휴머노이드/자동기계 로봇 비교. 휴머노이드가 부작위에 가장 큰 비난. ★ 족보 객관식.",
    "fromBopo": true
  },
  {
    "keyword": "말레 실험",
    "english": "Malle Experiment",
    "category": "사례",
    "file": "06주차/06주차_학습서.html",
    "anchor": "malle",
    "summary": "선로 전환기를 당기지 않을 때 휴머노이드 로봇이 가장 큰 비난을 받음. ★ 족보 객관식.",
    "fromBopo": true
  },
  {
    "keyword": "휴머노이드 로봇",
    "english": "Humanoid Robot",
    "category": "유형",
    "file": "06주차/06주차_학습서.html",
    "anchor": "malle",
    "summary": "인간형 외관 로봇. 말레 실험에서 도덕적 책임 기대가 가장 큼. ★ 족보 객관식·단답 모두 출제(10주차에도).",
    "fromBopo": true
  },
  {
    "keyword": "모럴 머신",
    "english": "Moral Machine",
    "category": "사례",
    "file": "06주차/06주차_학습서.html",
    "anchor": "moral-machine",
    "summary": "MIT 미디어랩. 2014~2018, 233개국 230만 명. 2018 네이처. 문화권별 윤리 차이.",
    "fromBopo": false
  },
  {
    "keyword": "죄수의 딜레마",
    "english": "Prisoner's Dilemma",
    "category": "개념",
    "file": "06주차/06주차_학습서.html",
    "anchor": "prisoner",
    "summary": "각자 합리성 → 집단 비합리성. 게임이론 고전.",
    "fromBopo": false
  },
  {
    "keyword": "존 내쉬",
    "english": "John Nash",
    "category": "인물",
    "file": "06주차/06주차_학습서.html",
    "anchor": "nash",
    "summary": "내쉬 균형 정립. 영화 「뷰티풀 마인드」.",
    "fromBopo": false
  },
  {
    "keyword": "내쉬 균형",
    "english": "Nash Equilibrium",
    "category": "개념",
    "file": "06주차/06주차_학습서.html",
    "anchor": "nash",
    "summary": "어느 한쪽도 혼자 전략을 바꿔 더 나은 결과를 얻지 못하는 상태.",
    "fromBopo": false
  },
  {
    "keyword": "공리주의 프로그램",
    "english": "Utilitarian Algorithm",
    "category": "기술",
    "file": "06주차/06주차_학습서.html",
    "anchor": "two-algos",
    "summary": "자율주행 알고리즘. 다수 보행자 살리기 위해 탑승자 희생 감수.",
    "fromBopo": false
  },
  {
    "keyword": "운전자 중심 프로그램",
    "english": "Driver-Protection Algorithm",
    "category": "기술",
    "file": "06주차/06주차_학습서.html",
    "anchor": "two-algos",
    "summary": "탑승자 무조건 보호. 이론적 위험 회피.",
    "fromBopo": false
  },
  {
    "keyword": "독일 자율주행 윤리지침",
    "english": "German Ethics Guidelines for Automated Driving",
    "category": "법률",
    "file": "06주차/06주차_학습서.html",
    "anchor": "sae",
    "summary": "2017 독일 발표. 20개 지침. 글로벌 표준.",
    "fromBopo": false
  },
  {
    "keyword": "EDR",
    "english": "Event Data Recorder",
    "category": "기술",
    "file": "06주차/06주차_학습서.html",
    "anchor": "sae",
    "summary": "자율주행 블랙박스. 책임 규명에 필수.",
    "fromBopo": false
  },
  {
    "keyword": "한국 AI 윤리 3원칙",
    "english": "Korea AI Ethics Principles",
    "category": "법률",
    "file": "06주차/06주차_학습서.html",
    "anchor": "korea3",
    "summary": "2020 발표. 인간 존엄성 + 사회 공공성 + 기술의 합목적성.",
    "fromBopo": false
  },
  {
    "keyword": "GM Cruise",
    "english": "GM Cruise",
    "category": "사례",
    "file": "06주차/06주차_학습서.html",
    "anchor": "sae",
    "summary": "2023 샌프란시스코 보행자 끌고 간 사고. 운행 허가 중단.",
    "fromBopo": false
  },
  {
    "keyword": "우버 자율주행 사고",
    "english": "Uber Self-driving Accident",
    "category": "사례",
    "file": "06주차/06주차_학습서.html",
    "anchor": "sae",
    "summary": "2018. 보행자 사망. 비상제동 비활성화 + 안전요원 미주시.",
    "fromBopo": false
  },
  {
    "keyword": "GAN",
    "english": "Generative Adversarial Network",
    "category": "기술",
    "file": "07주차/07주차_학습서.html",
    "anchor": "gan",
    "summary": "생성망 + 판별망의 경쟁 학습. 딥페이크의 기술 기반.",
    "fromBopo": false
  },
  {
    "keyword": "딥페이크",
    "english": "Deepfake",
    "category": "기술",
    "file": "07주차/07주차_학습서.html",
    "anchor": "deepfake",
    "summary": "AI 합성 영상. 인터넷 사용자 닉네임에서 유래. 라벨링·탐지 AI로 대응.",
    "fromBopo": false
  },
  {
    "keyword": "튜링 테스트",
    "english": "Turing Test",
    "category": "개념",
    "file": "07주차/07주차_학습서.html",
    "anchor": "turing",
    "summary": "1950 앨런 튜링. 심판이 사람/기계 구별 못하면 통과. 영화 「이미테이션 게임」.",
    "fromBopo": false
  },
  {
    "keyword": "앨런 튜링",
    "english": "Alan Turing",
    "category": "인물",
    "file": "07주차/07주차_학습서.html",
    "anchor": "turing",
    "summary": "튜링 테스트 제안. 컴퓨터 과학의 창시자.",
    "fromBopo": false
  },
  {
    "keyword": "유진",
    "english": "Eugene Goostman",
    "category": "사례",
    "file": "07주차/07주차_학습서.html",
    "anchor": "turing",
    "summary": "2014 레딩대 튜링 테스트 통과 챗봇. 13살 우크라이나 소년 캐릭터.",
    "fromBopo": false
  },
  {
    "keyword": "중국어방",
    "english": "Chinese Room",
    "category": "개념",
    "file": "07주차/07주차_학습서.html",
    "anchor": "chinese-room",
    "summary": "존 설의 논증. '기호 조작 ≠ 의미 이해'. 튜링 테스트 비판.",
    "fromBopo": false
  },
  {
    "keyword": "존 설",
    "english": "John Searle",
    "category": "인물",
    "file": "07주차/07주차_학습서.html",
    "anchor": "chinese-room",
    "summary": "중국어방 논증 제시 철학자.",
    "fromBopo": false
  },
  {
    "keyword": "레이 커즈와일",
    "english": "Ray Kurzweil",
    "category": "인물",
    "file": "07주차/07주차_학습서.html",
    "anchor": "chinese-room",
    "summary": "미래학자. 중국어방 반박. '시스템 수준의 이해' 주장.",
    "fromBopo": false
  },
  {
    "keyword": "메커니컬 터크",
    "english": "Mechanical Turk",
    "category": "사례",
    "file": "07주차/07주차_학습서.html",
    "anchor": "chinese-room",
    "summary": "아마존 디지털 인력 시장. 봇의 가짜 노동 문제.",
    "fromBopo": false
  },
  {
    "keyword": "AI 신뢰성",
    "english": "AI Reliability",
    "category": "개념",
    "file": "07주차/07주차_학습서.html",
    "anchor": "reliability",
    "summary": "4요소: 정확성·안정성·예측가능성·경고성. 도덕성은 포함 아님.",
    "fromBopo": false
  },
  {
    "keyword": "AI 공정성",
    "english": "AI Fairness",
    "category": "개념",
    "file": "07주차/07주차_학습서.html",
    "anchor": "fairness",
    "summary": "특정 개인·집단에 체계적 불이익 없는 상태. 기준 자체가 충돌 가능.",
    "fromBopo": false
  },
  {
    "keyword": "자동화 편향",
    "english": "Automation Bias",
    "category": "개념",
    "file": "07주차/07주차_학습서.html",
    "anchor": "auto-bias",
    "summary": "AI 판단을 과도 신뢰하는 인간 심리. 의료·판결·채용에서 위험.",
    "fromBopo": false
  },
  {
    "keyword": "EU AI Act",
    "english": "EU AI Act",
    "category": "법률",
    "file": "07주차/07주차_학습서.html",
    "anchor": "eu-act",
    "summary": "AI를 위험도 4단계 분류. 고위험에 데이터 편향검사·설명 가능성·감독·구제 의무.",
    "fromBopo": false
  },
  {
    "keyword": "데이터 드리프트",
    "english": "Data Drift",
    "category": "개념",
    "file": "07주차/07주차_학습서.html",
    "anchor": "eu-act",
    "summary": "시간 경과로 AI 판단 기준이 자연 왜곡. 정기 점검·재학습 필요.",
    "fromBopo": false
  },
  {
    "keyword": "인간중심 AI",
    "english": "Human-Centered AI (HCAI)",
    "category": "개념",
    "file": "07주차/07주차_학습서.html",
    "anchor": "hcai",
    "summary": "AI의 성능보다 인간 가치·권리·안전을 설계 중심에 둠.",
    "fromBopo": false
  },
  {
    "keyword": "신뢰성 4요소",
    "english": "Four Reliability Factors",
    "category": "개념",
    "file": "07주차/07주차_학습서.html",
    "anchor": "reliability",
    "summary": "정확성·안정성·예측가능성·경고성.",
    "fromBopo": false
  },
  {
    "keyword": "로봇 회복",
    "english": "Robot Restoration",
    "category": "개념",
    "file": "09주차/09주차_학습서.html",
    "anchor": "enhancement",
    "summary": "사라진 능력을 '같은 기능'의 기계로 교체. ★ 족보 객관식.",
    "fromBopo": true
  },
  {
    "keyword": "로봇 강화",
    "english": "Robot Enhancement",
    "category": "개념",
    "file": "09주차/09주차_학습서.html",
    "anchor": "enhancement",
    "summary": "능력을 '확장·개선'된 기계로 교체. ★ 족보 객관식.",
    "fromBopo": true
  },
  {
    "keyword": "회복 vs 강화",
    "english": "Restoration vs Enhancement",
    "category": "개념",
    "file": "09주차/09주차_학습서.html",
    "anchor": "enhancement",
    "summary": "경계 모호함이 쟁점. '어떤 기능은 회복하고 어떤 기능은 강화할 수 없다'는 잘못된 진술. ★ 족보 출제.",
    "fromBopo": true
  },
  {
    "keyword": "데카르트",
    "english": "René Descartes",
    "category": "인물",
    "file": "09주차/09주차_학습서.html",
    "anchor": "descartes",
    "summary": "동물을 자동기계(Automata)로 봄. ★★★ 족보 객관식 출제 (4·9주차 모두 다룸).",
    "fromBopo": true
  },
  {
    "keyword": "동물기계론",
    "english": "Animal Machine Theory",
    "category": "개념",
    "file": "09주차/09주차_학습서.html",
    "anchor": "descartes",
    "summary": "데카르트의 입장. 동물의 고통 반응은 기계적 반사. ★ 족보 출제.",
    "fromBopo": true
  },
  {
    "keyword": "감지",
    "english": "Sense",
    "category": "개념",
    "file": "09주차/09주차_학습서.html",
    "anchor": "spa",
    "summary": "로봇 의사결정 사이클의 첫 단계: 감지→계획→행동. ★ 족보 단답.",
    "fromBopo": true
  },
  {
    "keyword": "SPA",
    "english": "Sense-Plan-Act",
    "category": "기술",
    "file": "09주차/09주차_학습서.html",
    "anchor": "spa",
    "summary": "로봇의 고전 의사결정 패러다임. 감지→계획→행동. ★ 족보 출제.",
    "fromBopo": true
  },
  {
    "keyword": "Sense-Think-Act",
    "english": "Sense-Think-Act",
    "category": "기술",
    "file": "09주차/09주차_학습서.html",
    "anchor": "spa",
    "summary": "로봇의 기능적 정의. 감지+판단+행동. 강의 표현. SPA와 동의어.",
    "fromBopo": false
  },
  {
    "keyword": "휴 허",
    "english": "Hugh Herr",
    "category": "인물",
    "file": "09주차/09주차_학습서.html",
    "anchor": "hugh-herr",
    "summary": "MIT 미디어랩. 10대 사고로 두 다리 잃음 → 세계 최고 생체 로봇 의족 개발.",
    "fromBopo": false
  },
  {
    "keyword": "외골격 로봇",
    "english": "Exoskeleton",
    "category": "기술",
    "file": "09주차/09주차_학습서.html",
    "anchor": "enhancement",
    "summary": "장애인 재활→회복, 군인 근력 증폭→강화. 같은 기술이 맥락에 따라 다름.",
    "fromBopo": false
  },
  {
    "keyword": "BCI",
    "english": "Brain-Computer Interface",
    "category": "기술",
    "file": "09주차/09주차_학습서.html",
    "anchor": "bci",
    "summary": "뇌-컴퓨터 인터페이스. '생각하면 기계가 움직임'. 인간 능력 재정의.",
    "fromBopo": false
  },
  {
    "keyword": "모다피닐",
    "english": "Modafinil",
    "category": "기술",
    "file": "09주차/09주차_학습서.html",
    "anchor": "bci",
    "summary": "미공군 공식 사용 각성 약물.",
    "fromBopo": false
  },
  {
    "keyword": "리탈린",
    "english": "Ritalin",
    "category": "기술",
    "file": "09주차/09주차_학습서.html",
    "anchor": "bci",
    "summary": "미국 대학생들의 '공부약'. 학업 도핑 논란.",
    "fromBopo": false
  },
  {
    "keyword": "애더럴",
    "english": "Adderall",
    "category": "기술",
    "file": "09주차/09주차_학습서.html",
    "anchor": "bci",
    "summary": "주의력 강화제. 시험기 인지 강화 약물.",
    "fromBopo": false
  },
  {
    "keyword": "TMS",
    "english": "Transcranial Magnetic Stimulation",
    "category": "기술",
    "file": "09주차/09주차_학습서.html",
    "anchor": "bci",
    "summary": "경두개 자기자극. 우울증 치료→기억력·학습 향상.",
    "fromBopo": false
  },
  {
    "keyword": "로봇 정의",
    "english": "Definition of Robot",
    "category": "개념",
    "file": "09주차/09주차_학습서.html",
    "anchor": "robot-def",
    "summary": "Sense + Think + Act 세 기능을 모두 갖춘 존재. 형태 무관.",
    "fromBopo": false
  },
  {
    "keyword": "유니메이트",
    "english": "Unimate",
    "category": "사례",
    "file": "09주차/09주차_학습서.html",
    "anchor": "unimate",
    "summary": "1960s 세계 최초 산업용 로봇. 자동차 공장 용접·프레스.",
    "fromBopo": false
  },
  {
    "keyword": "휴머노이드",
    "english": "Humanoid",
    "category": "유형",
    "file": "09주차/09주차_학습서.html",
    "anchor": "robot-def",
    "summary": "인간형 외관 로봇. ★ 6주차 말레 실험, 10주차 소셜로봇 단답에서도 출제.",
    "fromBopo": true
  },
  {
    "keyword": "엘리시움",
    "english": "Elysium",
    "category": "사례",
    "file": "09주차/09주차_학습서.html",
    "anchor": "enhancement",
    "summary": "영화. 강화 가진 자/못 가진 자의 두 계급 사회 경고.",
    "fromBopo": false
  },
  {
    "keyword": "베이맥스",
    "english": "Baymax",
    "category": "사례",
    "file": "09주차/09주차_학습서.html",
    "anchor": "robot-def",
    "summary": "빅 히어로 6의 돌봄·치유 로봇. 동아시아적 로봇 인식.",
    "fromBopo": false
  },
  {
    "keyword": "소셜 로봇",
    "english": "Social Robot",
    "category": "유형",
    "file": "10주차/10주차_학습서.html",
    "anchor": "social",
    "summary": "인간과 사회적 상호작용을 하는 지능형 자율 로봇. 관계 파트너.",
    "fromBopo": false
  },
  {
    "keyword": "페퍼",
    "english": "Pepper",
    "category": "사례",
    "file": "10주차/10주차_학습서.html",
    "anchor": "social",
    "summary": "일본 소프트뱅크 휴머노이드. 카페·매장 안내.",
    "fromBopo": false
  },
  {
    "keyword": "효돌",
    "english": "Hyodol",
    "category": "사례",
    "file": "10주차/10주차_학습서.html",
    "anchor": "social",
    "summary": "한국 시니어 케어 로봇. 약·식사·말벗.",
    "fromBopo": false
  },
  {
    "keyword": "파로",
    "english": "Paro",
    "category": "사례",
    "file": "10주차/10주차_학습서.html",
    "anchor": "social",
    "summary": "일본 아기 바다표범 로봇. FDA 승인. 치매·자폐 환자 케어.",
    "fromBopo": false
  },
  {
    "keyword": "휴머노이드",
    "english": "Humanoid",
    "category": "유형",
    "file": "10주차/10주차_학습서.html",
    "anchor": "humanoid",
    "summary": "실제 인물의 얼굴·음성·피부를 똑같이 복사한 로봇. 의료케어 시 환자가 인격체로 간주. ★★★ 족보 단답.",
    "fromBopo": true
  },
  {
    "keyword": "ELIZA 효과",
    "english": "ELIZA Effect",
    "category": "개념",
    "file": "10주차/10주차_학습서.html",
    "anchor": "eliza",
    "summary": "단순한 프로그램에게도 실제보다 더 많은 지능·감정을 부여하는 심리 현상.",
    "fromBopo": false
  },
  {
    "keyword": "공감",
    "english": "Empathy",
    "category": "개념",
    "file": "10주차/10주차_학습서.html",
    "anchor": "empathy",
    "summary": "인간 = 자신의 경험·감정 통한 정서 반응. 로봇 = 패턴 분류·응답 출력 (시뮬레이션).",
    "fromBopo": false
  },
  {
    "keyword": "다빈치 시스템",
    "english": "da Vinci System",
    "category": "사례",
    "file": "10주차/10주차_학습서.html",
    "anchor": "davinci",
    "summary": "2001 FDA 승인. 정밀 절개·회복기간 단축. 로봇 수술 대중화.",
    "fromBopo": false
  },
  {
    "keyword": "Mako",
    "english": "Mako",
    "category": "사례",
    "file": "10주차/10주차_학습서.html",
    "anchor": "davinci",
    "summary": "정형외과 인공관절 수술 로봇. 범위 넘으면 자동 정지.",
    "fromBopo": false
  },
  {
    "keyword": "의료 로봇",
    "english": "Medical Robot",
    "category": "유형",
    "file": "10주차/10주차_학습서.html",
    "anchor": "surgery",
    "summary": "수술 로봇을 포함한 의료 전반 로봇. 재활·간호·물류.",
    "fromBopo": false
  },
  {
    "keyword": "수술 로봇",
    "english": "Surgical Robot",
    "category": "유형",
    "file": "10주차/10주차_학습서.html",
    "anchor": "surgery",
    "summary": "절개·절삭·봉합 등 직접 수술 행위 수행. 4유형(보조·협력·반자동·나노).",
    "fromBopo": false
  },
  {
    "keyword": "LAWS",
    "english": "Lethal Autonomous Weapons Systems",
    "category": "기술",
    "file": "10주차/10주차_학습서.html",
    "anchor": "laws",
    "summary": "치명적 자율 무기 시스템. 인간 개입 없이 표적 선택+공격까지. ★ 족보 객관식 (자율무기 입장).",
    "fromBopo": true
  },
  {
    "keyword": "자율무기",
    "english": "Autonomous Weapons",
    "category": "기술",
    "file": "10주차/10주차_학습서.html",
    "anchor": "stance",
    "summary": "★ 족보: '감정 없는 로봇이 잔혹 행위 안 함'만 찬성 입장. 나머지는 반대.",
    "fromBopo": true
  },
  {
    "keyword": "패트리어트",
    "english": "Patriot",
    "category": "사례",
    "file": "10주차/10주차_학습서.html",
    "anchor": "laws",
    "summary": "공중위협 자동 요격 미사일 시스템. 부분 자율 무기 사례.",
    "fromBopo": false
  },
  {
    "keyword": "이지스",
    "english": "Aegis",
    "category": "사례",
    "file": "10주차/10주차_학습서.html",
    "anchor": "laws",
    "summary": "해상 자율 방어 시스템.",
    "fromBopo": false
  },
  {
    "keyword": "팔랑스",
    "english": "Phalanx",
    "category": "사례",
    "file": "10주차/10주차_학습서.html",
    "anchor": "laws",
    "summary": "근접 방공 자동 시스템.",
    "fromBopo": false
  },
  {
    "keyword": "정당한 전쟁론",
    "english": "Just War Theory",
    "category": "개념",
    "file": "10주차/10주차_학습서.html",
    "anchor": "just-war",
    "summary": "전쟁의 도덕적 허용 조건. 정당한 명분·최후의 수단·합법적 권위·올바른 의도·성공 가능성·비례성·목적의 제한.",
    "fromBopo": false
  },
  {
    "keyword": "국제인도법",
    "english": "IHL (International Humanitarian Law)",
    "category": "법률",
    "file": "10주차/10주차_학습서.html",
    "anchor": "just-war",
    "summary": "2원칙: 차별성(Distinction) + 비례성(Proportionality).",
    "fromBopo": false
  },
  {
    "keyword": "차별성 원칙",
    "english": "Principle of Distinction",
    "category": "법률",
    "file": "10주차/10주차_학습서.html",
    "anchor": "just-war",
    "summary": "전투원 vs 비전투원 구분, 민간인 보호.",
    "fromBopo": false
  },
  {
    "keyword": "비례성 원칙",
    "english": "Principle of Proportionality",
    "category": "법률",
    "file": "10주차/10주차_학습서.html",
    "anchor": "just-war",
    "summary": "군사 목표 ↔ 민간 피해 균형.",
    "fromBopo": false
  },
  {
    "keyword": "의미 있는 인간 통제",
    "english": "Meaningful Human Control",
    "category": "개념",
    "file": "10주차/10주차_학습서.html",
    "anchor": "just-war",
    "summary": "최종 살상 결정은 반드시 인간이. 인간 존엄성 원칙.",
    "fromBopo": false
  },
  {
    "keyword": "유발 하라리",
    "english": "Yuval Noah Harari",
    "category": "인물",
    "file": "11주차/11주차_학습서.html",
    "anchor": "harari",
    "summary": "「호모 데우스」 저자. 알고리즘·데이터이즘 개념 제시.",
    "fromBopo": false
  },
  {
    "keyword": "호모 데우스",
    "english": "Homo Deus",
    "category": "사례",
    "file": "11주차/11주차_학습서.html",
    "anchor": "harari",
    "summary": "유발 하라리의 미래학 저서. 데이터이즘·알고리즘 시대 경고.",
    "fromBopo": false
  },
  {
    "keyword": "데이터이즘",
    "english": "Dataism",
    "category": "개념",
    "file": "11주차/11주차_학습서.html",
    "anchor": "dataism",
    "summary": "데이터를 신처럼 여기는 세계관. 도덕·전통보다 데이터 최적화가 기준.",
    "fromBopo": false
  },
  {
    "keyword": "알고리즘",
    "english": "Algorithm (Harari)",
    "category": "개념",
    "file": "11주차/11주차_학습서.html",
    "anchor": "harari",
    "summary": "하라리의 정의: 입력→규칙→출력의 절차적 체계. 인간 의사결정도 알고리즘화 위험.",
    "fromBopo": false
  },
  {
    "keyword": "2050 미래사회보고서",
    "english": "2050 Future Society Report",
    "category": "사례",
    "file": "11주차/11주차_학습서.html",
    "anchor": "2050",
    "summary": "서울대 유기훈 교수팀. 4계급 피라미드(초양극화).",
    "fromBopo": false
  },
  {
    "keyword": "프레카리아트",
    "english": "Precariat",
    "category": "개념",
    "file": "11주차/11주차_학습서.html",
    "anchor": "precariat",
    "summary": "2050 보고서의 99.997%. 불안정 노동에 내몰린 시민 다수.",
    "fromBopo": false
  },
  {
    "keyword": "플랫폼 소유주",
    "english": "Platform Owner",
    "category": "개념",
    "file": "11주차/11주차_학습서.html",
    "anchor": "2050",
    "summary": "2050 보고서 최상위 0.001%. 데이터 흐름 통제 = 권력.",
    "fromBopo": false
  },
  {
    "keyword": "존 헨리",
    "english": "John Henry",
    "category": "사례",
    "file": "11주차/11주차_학습서.html",
    "anchor": "john-henry",
    "summary": "흑인 노예 출신 철도 노동자. 굴착기와 대결 후 사망. 산업혁명 상징.",
    "fromBopo": false
  },
  {
    "keyword": "러다이트 운동",
    "english": "Luddite Movement",
    "category": "사례",
    "file": "11주차/11주차_학습서.html",
    "anchor": "john-henry",
    "summary": "19세기 노동자 기계 파괴 저항 운동.",
    "fromBopo": false
  },
  {
    "keyword": "딥블루",
    "english": "Deep Blue",
    "category": "사례",
    "file": "11주차/11주차_학습서.html",
    "anchor": "deep-blue",
    "summary": "1997 IBM 슈퍼컴퓨터. 체스 챔피언 카스파로프 패배. 화이트칼라 위협 시작.",
    "fromBopo": false
  },
  {
    "keyword": "4차 산업혁명",
    "english": "Fourth Industrial Revolution",
    "category": "개념",
    "file": "11주차/11주차_학습서.html",
    "anchor": "4ir",
    "summary": "AI + IoT + 빅데이터 + 메타버스 + 초연결.",
    "fromBopo": false
  },
  {
    "keyword": "자동화 위험군",
    "english": "Automation Risk",
    "category": "개념",
    "file": "11주차/11주차_학습서.html",
    "anchor": "automation",
    "summary": "반복·규칙·정형화된 작업이 자동화 위험. 직업이 아닌 작업 단위로 분석.",
    "fromBopo": false
  },
  {
    "keyword": "작업 단위",
    "english": "Task-based Analysis",
    "category": "개념",
    "file": "11주차/11주차_학습서.html",
    "anchor": "automation",
    "summary": "OECD 방식. 직업이 아닌 세부 업무로 자동화 가능성 분석 (5주차와 연결).",
    "fromBopo": false
  },
  {
    "keyword": "인공지성",
    "english": "Artificial Intellect",
    "category": "개념",
    "file": "11주차/11주차_학습서.html",
    "anchor": "2050",
    "summary": "2050 보고서. 인간보다 효율적인 노동력으로 자리 잡은 AI 로봇.",
    "fromBopo": false
  },
  {
    "keyword": "AI 감시",
    "english": "AI Surveillance",
    "category": "개념",
    "file": "12주차/12주차_학습서.html",
    "anchor": "ai-surveillance",
    "summary": "3가지 변화: 규모·속도·정밀도. 인구 전체 분석·예측 시대.",
    "fromBopo": false
  },
  {
    "keyword": "사회신용 시스템",
    "english": "Social Credit System",
    "category": "사례",
    "file": "12주차/12주차_학습서.html",
    "anchor": "china",
    "summary": "중국 정부의 전국 규모 점수 감시 체계. 2018년 1,700만 건 탑승금지.",
    "fromBopo": false
  },
  {
    "keyword": "HART",
    "english": "Homeland Advanced Recognition Technology",
    "category": "사례",
    "file": "12주차/12주차_학습서.html",
    "anchor": "hart",
    "summary": "미국 국토안보부 AI 감시. 얼굴·음성·지문·홍채·SNS·관계망 통합. 미래 행동 예측.",
    "fromBopo": false
  },
  {
    "keyword": "감시 자본주의",
    "english": "Surveillance Capitalism",
    "category": "개념",
    "file": "12주차/12주차_학습서.html",
    "anchor": "zuboff",
    "summary": "쇼샤나 주보프. 인간 행동 예측·조작이 핵심 비즈니스 모델인 자본주의.",
    "fromBopo": false
  },
  {
    "keyword": "쇼샤나 주보프",
    "english": "Shoshana Zuboff",
    "category": "인물",
    "file": "12주차/12주차_학습서.html",
    "anchor": "zuboff",
    "summary": "하버드대 교수. 감시 자본주의 개념 명명.",
    "fromBopo": false
  },
  {
    "keyword": "캠브리지 애널리티카 (12주차)",
    "english": "Cambridge Analytica",
    "category": "사례",
    "file": "12주차/12주차_학습서.html",
    "anchor": "cambridge",
    "summary": "2016 미국 대선. 페이스북 8,700만 명 데이터로 정치 메시지 맞춤 전달. 5주차 족보(개인정보 유출)와 연결.",
    "fromBopo": false
  },
  {
    "keyword": "사회적 조종",
    "english": "Social Manipulation",
    "category": "개념",
    "file": "12주차/12주차_학습서.html",
    "anchor": "manipulation",
    "summary": "알고리즘이 선택·감정·행동을 조용히 유도. '스스로 선택했다고 믿게 만들기'.",
    "fromBopo": false
  },
  {
    "keyword": "조종 3요소",
    "english": "Three Elements of Manipulation",
    "category": "개념",
    "file": "12주차/12주차_학습서.html",
    "anchor": "three-elements",
    "summary": "예측(Prediction) + 개입(Intervention) + 반복(Repetition).",
    "fromBopo": false
  },
  {
    "keyword": "감정 감염 실험",
    "english": "Emotional Contagion Experiment",
    "category": "사례",
    "file": "12주차/12주차_학습서.html",
    "anchor": "facebook",
    "summary": "2014 페이스북. 70만 명 무동의 실험. 'AI는 감정을 설계할 수 있다.'",
    "fromBopo": false
  },
  {
    "keyword": "가용성 휴리스틱",
    "english": "Availability Heuristic",
    "category": "개념",
    "file": "12주차/12주차_학습서.html",
    "anchor": "three-elements",
    "summary": "반복 노출된 자극을 내 생각이라 착각하는 인지 편향.",
    "fromBopo": false
  },
  {
    "keyword": "소셜 딜레마",
    "english": "The Social Dilemma",
    "category": "사례",
    "file": "12주차/12주차_학습서.html",
    "anchor": "tiktok",
    "summary": "전직 기술자들의 폭로 다큐. '광고가 아닌 주의(Attention)를 판매.'",
    "fromBopo": false
  },
  {
    "keyword": "틱톡 알고리즘",
    "english": "TikTok Algorithm",
    "category": "사례",
    "file": "12주차/12주차_학습서.html",
    "anchor": "tiktok",
    "summary": "시청 시간·스크롤·표정·근육 움직임 분석. '좋아요보다 눈동자 움직임 신뢰.'",
    "fromBopo": false
  },
  {
    "keyword": "플랫폼 3목표",
    "english": "Three Platform Goals",
    "category": "개념",
    "file": "12주차/12주차_학습서.html",
    "anchor": "three-goals",
    "summary": "참여(Engagement) + 성장(Growth) + 광고(Advertising).",
    "fromBopo": false
  }
];
