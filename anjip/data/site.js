/* 안집 사이트 — 내용 전부의 기본값 (한 곳). 한옥반점 사이트(../hanok/data/site.js)와 같은 방식입니다.
   글·사진·차림·영업시간·연락처가 이 한 객체에 들어 있고, 사이트는 이 값으로 그립니다.
   나중에 예약 시스템 '홈페이지 관리' 가 안집도 맡게 되면 서버 값(site_versions, store = anjip)이 이 위를 덮습니다(js/content.js).

   사진: img/ 의 파일명 또는 전체 주소. 글 안의 **굵게** 는 굵은 글씨, 줄바꿈은 그대로.
   ★ 확인 필요(재아 → 고모): 주소·전화·영업시간·콜키지 금액·좌석 수 — 아래 "확인" 표시가 붙은 값은 임시입니다. */
window.SITE_DEFAULT = {
  info: {
    name: "안집", tagline: "토속음식의 명가",
    addr: "경기 성남시 분당구 새마을로51번길 (확인)", addr2: "경기 성남시 분당구\n새마을로51번길 (확인)",   /* 확인: 한옥반점 맞은편 — 정확한 번지 */
    tel: "031-000-0000",   /* 확인 */
    parking: "발렛 포함 주차 1,000원", since: 1996,   /* 2019년에 "23년" 이라 홍보 → 1996년 개업 → 2026년 30년 */
    naverMap: "#", kakaoMap: "#",   /* 확인 */
    instagram: "",
    owner: "", bizno: "",   /* 확인 */
    services: ["예약 · 포장 · 단체 가능", "콜키지 가능 (유료)", "365일 연중무휴"],
    menuPdf: ""
  },

  /* 영업시간 — 확인 필요. 연중무휴는 확인됨 */
  hours: [
    { day: "매일", open: "11:30 – 22:00 (확인)" }
  ],
  hoursNote: ["365일 연중무휴", "브레이크·라스트오더 확인 중"],

  /* 방송 — 홈 띠와 이야기 장에 */
  tv: [
    { show: "SBS 생방송투데이", ep: "3308회", date: "2023년 6월 2일", what: "간장게장" },
    { show: "KBS 2TV 생생정보", ep: "1053회", date: "2020년 4월 23일", what: "간장게장" }
  ],

  notices: [],

  /* 홈에 크게 보이는 대표 셋 */
  signature: [
    { name: "간장게장 정식", sub: "연평도 암꽃게 · 직접 담근 간장", img: "gejang.jpg" },
    { name: "한우 안창살", sub: "숙성하지 않은 생고기 · 안집 시그니처", img: "beef.jpg" },
    { name: "당일 도축 육사시미", sub: "소량만 · 게장 정식과 함께", img: "gejang-close.jpg" }
  ],

  /* 공간 — 룸 없음. 1층·지하 홀 (좌석 수 확인) */
  halls: [
    { name: "1층", cap: "테이블 (확인)", img: "hansang.jpg" },
    { name: "지하", cap: "테이블 (확인) · 단체", img: "crab-hands-wide.jpg" }
  ],

  home: {
    heroSlides: ["gejang.jpg", "crab-hands.jpg", "hansang.jpg"],
    heroTitle: "삼십 년, 한자리의 간장게장",
    heroSub: "분당 · 연평도 꽃게와 한우 1++ · 365일 연중무휴",
    intro: {
      img: "crab-hands.jpg", imgAlt: "알이 꽉 찬 연평도 암꽃게",
      title: "삼십 년째\n같은 자리에서 담급니다",
      paras: [
        "안집은 1996년부터 분당 한자리를 지켜 온 한정식집입니다. 서른 해 동안 쌓은 경험으로, 가장 좋은 재료를 골라 정성껏 차립니다.",
        "간장과 된장을 직접 담가 씁니다. 조미료는 최소로 하고, 재료가 가진 맛으로 상을 채웁니다. 간장게장은 **연평도산 암꽃게**만을 일정한 크기로 골라 주문을 받은 뒤 담급니다.",
        "한우는 **1++ 등급**만 쓰고 숙성하지 않은 생고기로 냅니다. 고기 본연의 신선함과 육향이 살아 있습니다."
      ],
      more: "이야기 전체"
    },
    menuSec: { title: "차림", lead: "게장 정식은 인원수에 맞게. 소고기 구이와 게장을 함께 드셔도 좋습니다", img: "yangnyeom.jpg", imgAlt: "양념게장", more: "차림 전체" },
    tvSec: { title: "방송에 소개된 간장게장", lead: "전국 5대 게장으로 꼽힙니다" },
    spaceSec: { title: "공간", lead: "1층과 지하, 두 층의 홀. 가족 식사도 단체 모임도 편하게", more: "공간",
      tiles: [ { img: "hansang.jpg", alt: "4인 한상", wide: true }, { img: "gejang-close.jpg", alt: "간장게장" }, { img: "beef.jpg", alt: "한우 구이" }, { img: "yangnyeom.jpg", alt: "양념게장" } ] },
    infoSec: { visitMore: "오시는 길 전체", telNote: "예약·포장·단체 문의는 전화로 주세요" },
    band: { img: "hansang-full.jpg", title: "예약 · 포장", lines: ["전화로 예약과 포장을 받습니다.", "단체 모임도 미리 말씀해 주시면 자리를 준비해 두겠습니다."], button: "전화하기" }
  },

  about: {
    head: { img: "crab-hands.jpg", title: "이야기", sub: "1996년부터 분당 한자리에서. 직접 담근 간장과 연평도 꽃게, 그리고 한우." },
    story: {
      title: "간장게장은\n주문을 받은 뒤 담급니다", sub: "안집의 방식",
      paras: [
        "음식은 재료에서 맛이 정해집니다. 안집은 한 끼의 손님을 위해 일 년을 준비하는 마음으로 재료를 고릅니다. 간장게장에는 **일정한 크기로 고른 100% 연평도산 암꽃게**만 씁니다. 알과 살이 꽉 찬 밀물 암꽃게를 엄선해, 시중 제품처럼 미리 만들어 두지 않고 **주문을 받은 뒤** 담급니다.",
        "간장은 스무 해 넘게 이어 온 안집만의 방법으로 직접 담급니다. 방부제 없이, 무조미로. 그래서 짜지 않고 게살의 단맛이 살아 있습니다. 밥도둑이라는 말이 어디서 왔는지 한 숟갈이면 아실 겁니다.",
        "한우는 **1++ 등급만** 씁니다. 숙성시키지 않은 진짜 생고기를 손님상에 올립니다. 신선도와 육향이 뛰어난 대신 오래 구울수록 질겨질 수 있으니, 살짝만 익혀 드시길 권합니다. 부드러운 고기를 찾으시면 안집 시그니처 **안창살**을, 아이들과 함께라면 **생갈비살 주물럭**을 권합니다. 당일 도축한 한우 **육사시미**는 소량만 준비합니다.",
        "한옥반점과는 한 가족이 함께 운영합니다. 주차장을 같이 씁니다."
      ],
      pics: [ { img: "gejang-story.jpg", alt: "안집 간장게장" }, { img: "hansang-full.jpg", alt: "간장게장 정식 한상" } ]
    },
    tvTitle: "방송 출연"
  },

  menuPage: {
    head: { img: "gejang.jpg", title: "차림", sub: "게장 정식은 반드시 인원수에 맞게 주문해 주세요. 한우 구이와 게장 정식을 합쳐 인원수에 맞춰 주문하셔도 됩니다." },
    notes: [
      "게장 정식은 인원수에 맞게 주문해 주세요. 한우 구이와 게장 정식을 합쳐 인원수에 맞게 주문하셔도 됩니다.",
      "1인상은 준비되지 않습니다(1인 = 초등학생 기준). 소고기 구이를 드시는 경우 추가 메뉴로 게장을 더하실 수 있습니다.",
      "안집 게장은 연평도산 꽃게만을 사용합니다.",
      "가격은 바뀔 수 있습니다. 정확한 가격은 매장에서 확인해 주세요."
    ],
    origin: "원산지 — 등심·안창·치마살·주물럭(등심)·육사시미 한우(국내산) / 꽃게(국내산) / 쌀(국내산) / 한우 떡갈비(국내산) / 녹두전(돼지고기 국내산) / 두부(콩: 인도·미국·중국) / 파김치·갓김치·열무김치(국내산) / 알타리·배추김치(중국산·국내산) / 고춧가루(중국산)"
  },

  visit: {
    head: { img: "hansang.jpg", title: "오시는 길", sub: "분당 새마을로 골목, 한옥반점 맞은편입니다." },
    hoursTitle: "영업시간", mapCaption: "약도는 실제 축적과 다를 수 있습니다.",
    parkingTitle: "주차",
    parking: [
      "주차장은 맞은편 '한옥반점'과 함께 사용합니다.",
      "골목 초입이라 혼잡한 구간이므로 주차 관리요원의 안내에 따라 주세요.",
      "발렛 및 주차장 이용 요금은 한 대당 1,000원입니다."
    ],
    transitTitle: "대중교통",
    transit: ["버스 — 통로골 또는 서현중학교 정류장", "지하철 — 수인분당선 서현역"]
  },

  /* ---------- 차림 — 2026-09 메뉴판 사진에서 옮김. 가격 단위 원 ---------- */
  menu: [
    { id: "sets", title: "식사", sub: "게장 정식 — 연평도산 꽃게",
      items: [
        { name: "간장게장 특 정식", price: 44000, desc: "게장 정식 + 떡갈비 70g + 녹두전 70g · 2인 이상", badge: "특" },
        { name: "양념게장 특 정식", price: 44000, desc: "게장 정식 + 떡갈비 70g + 녹두전 70g · 2인 이상", badge: "특" },
        { name: "간장게장 정식", price: 35000, badge: "대표" },
        { name: "양념게장 정식", price: 35000 }
      ],
      note: "게장 정식에 당일 도축 육사시미를 곁들이시길 권합니다." },
    { id: "beef", title: "한우", sub: "숙성하지 않은 생고기 · 1++",
      items: [
        { name: "한우 생갈비살 주물럭", size: "150g", price: 35000, desc: "쫄깃하고 야들야들 · 아이들 식사와 술안주로", badge: "추천" },
        { name: "한우 생등심", size: "150g", price: 52000 },
        { name: "한우 치마살", size: "150g", price: 52000 },
        { name: "한우 안창살", size: "130g", price: 62000, desc: "안집 시그니처 · 부드러운 고기를 찾으시면", badge: "시그니처" },
        { name: "한우 당일도축 육사시미", size: "120g", price: 35000, desc: "소량만 준비합니다", badge: "강력추천" }
      ],
      note: "100g 기준 — 육사시미 29,166원 · 생등심·치마살 34,666원 · 갈비주물럭 23,333원 · 안창살 47,692원. 고기 추천을 원하시면 말씀해 주세요." },
    { id: "extra", title: "추가 요리",
      items: [
        { name: "한우 당일 도축 육사시미", size: "120g", price: 35000, badge: "강력추천" },
        { name: "꽃게 간장게장 한 마리", size: "연평도", price: 25000 },
        { name: "꽃게 양념게장 한 마리", size: "연평도", price: 25000 },
        { name: "한우 떡갈비", price: 20000 },
        { name: "도토리묵 무침", price: 15000 },
        { name: "녹두전", price: 20000 },
        { name: "된장찌개", price: 8000 },
        { name: "냉소면 / 잔치국수", price: 8000 },
        { name: "경상도식 소고기 무국 (얼큰)", price: 15000, badge: "NEW" }
      ] },
    { id: "after", title: "고기 식사류", sub: "구이 뒤 식사",
      items: [
        { name: "후식 된장찌개", price: 4000 },
        { name: "후식 냉소면 (열무)", price: 6000 },
        { name: "후식 잔치국수", price: 6000 },
        { name: "누룽지", price: 2000 },
        { name: "공기밥", price: 1000 }
      ] },
    { id: "drinks", title: "주류",
      items: [
        { name: "화요 41", price: 45000 },
        { name: "화요 25", price: 28000 },
        { name: "복분자", price: 18000 },
        { name: "15년 숙성 매취순", price: 15000 },
        { name: "막걸리", sizes: [["대 1,700ml", 15000], ["소 800ml", 8000]] },
        { name: "백세주", price: 12000 },
        { name: "산사춘", price: 12000 },
        { name: "소주", price: 5000 },
        { name: "맥주", price: 5000 },
        { name: "음료", price: 2000 }
      ] },
    { id: "wine", title: "와인 · 양주",
      items: [
        { name: "무초마스 레드", size: "MUCHO MAS RED 13.5% · 750ml · vivino 4.2", price: 60000 },
        { name: "까뮤 VSOP 꼬냑", size: "CAMUS VSOP COGNAC 40% · 700ml", price: 180000 }
      ] }
  ]
};

/* 전역 이름(INFO·HOURS·MENU …) — js/site.js 가 이 이름으로 읽습니다. 서버 값이 오면 js/content.js 가 같은 함수로 다시 채웁니다 */
window.applySiteGlobals = function(S){
  window.SITE = S;
  window.MENU = S.menu; window.HALLS = S.halls;
  window.HOURS = S.hours; window.HOURS_NOTE = S.hoursNote;
  window.SIGNATURE = S.signature; window.NOTICES = S.notices; window.INFO = S.info;
};
window.applySiteGlobals(window.SITE_DEFAULT);
