/* 짚불태백 광교점 — 제안용 시안. 내용 전부의 기본값 (한 곳).
   한옥반점 사이트(hanokbanjeom.com)와 같은 구조: 글·사진·팝업·차림·영업시간·연락처가 이 한 객체에 들어 있고, 사이트는 이 값으로 그립니다.
   시안이라 서버(js/config.js)가 없습니다 — 예약 창은 영업시간 규칙으로 흉내만 냅니다(js/reserve.js).

   ★ 주소·전화·영업시간·주차·좌석·사업자 정보·약도(img/map.svg)는 그럴듯한 더미입니다(11-10 사용자 요청: 화면에 '예시' 표시 없이).
     실제 광교점 정보가 아닙니다 — 받으면 여기만 고치면 됩니다.
   브랜드 소개·메뉴 이름은 본사 사이트(zipfiretaebaek.com, 2026-11-10 수집)에서 옮겼고, 가격은 본사 사이트에 없어 넣지 않았습니다.
   사진은 본사 사이트의 것 — 매장 사진은 광교점이 아니라 다른 지점입니다. */
window.SITE_DEFAULT = {
  info: {
    name: "짚불태백 광교점", brand: "짚불태백", branch: "광교점", branchEn: "GWANGGYO",
    addr: "경기 수원시 영통구 광교중앙로248번길 7, 1층", addr2: "경기 수원시 영통구\n광교중앙로248번길 7, 1층",
    tel: "031-232-0136", parking: "건물 뒤 전용 주차 12대 · 2시간 무료", since: 2025,
    naverMap: "https://map.naver.com/p/search/%EC%A7%9A%EB%B6%88%ED%83%9C%EB%B0%B1", kakaoMap: "https://map.kakao.com/?q=%EC%A7%9A%EB%B6%88%ED%83%9C%EB%B0%B1", instagram: "",   /* 지도는 상호 검색 주소(더미) — 광교점 지도 주소를 받으면 바꿈 */
    owner: "이태성", bizno: "124-58-03671",
    naverBooking: "",
    services: ["단체 회식 예약", "유아용 의자", "콜키지 가능", "포장 가능"],
    menuPdf: ""   /* 메뉴판 PDF — 받으면 파일명 */
  },

  /* 영업시간 — 더미. js/reserve.js 의 흉내 시간표(점심 11:30–14:00 · 저녁 17:00–20:30)와 같게 */
  hours: [
    { day: "매일", open: "11:30 – 22:00" }
  ],
  hoursNote: ["브레이크 15:00 – 17:00", "라스트오더 21:00", "연중무휴 · 설·추석 당일 휴무"],
  closed: [],

  /* 홈페이지 예약 접수 규칙 — 한옥반점의 '룸' 자리를 여기서는 '단체석' 으로 씁니다(seat 값은 그대로 room / table) */
  online: {
    enabled: true,
    offTitle: "지금은 온라인 예약을 받지 않습니다",
    offMsg: "예약은 전화로 부탁드립니다. 영업시간 중 언제든 받습니다.",
    maxDays: 30,
    minAdults: 2,
    maxPeople: 20,
    roomMinAdults: 8,            /* 단체석 최소 인원(성인) — 예시 */
    roomMinAdultsWeekend: 8,
    limitMin: 5,
    sameDay: true,               /* 고깃집은 당일 예약이 많아 켬 */
    sameDayLeadH: 2,
    roomCond: [],
    drinks: ["소주", "맥주", "와인(콜키지)", "음주 안 함"]
  },
  holidays: ["2026-12-25",
             "2027-01-01","2027-02-06","2027-02-07","2027-02-08","2027-02-09","2027-03-01","2027-05-01","2027-05-03","2027-05-05","2027-05-13","2027-06-06","2027-07-17","2027-07-19","2027-08-15","2027-08-16","2027-09-14","2027-09-15","2027-09-16","2027-10-03","2027-10-04","2027-10-09","2027-10-11","2027-12-25","2027-12-27"],

  /* 팝업창 — 본사 사이트 팝업(2025 한국 소비자 만족도 평가 1위)을 글로 옮김 */
  notices: [
    { id: "award-2025", from: "", until: "", x: 40, y: 110, w: 380,
      title: "2025 한국 소비자 만족도 평가 1위",
      lines: [
        "짚불태백이 KOREA BRAND ONE WINNER AWARDS 고깃집 프랜차이즈 부문에서 한국 소비자 만족도 평가 1위에 선정되었습니다.",
        "보내주신 큰 사랑에 감사드립니다. 광교점에서도 같은 맛으로 모시겠습니다."
      ],
      button: "예약하기" }
  ],

  signature: [],

  /* 공간 — 사진은 본사 사이트의 다른 지점 매장입니다(광교점 사진을 받으면 바꿈). 좌석 수는 예시 */
  rooms: [
    { name: "홀", cap: "4인 테이블", img: "in-1.webp" },
    { name: "부스석", cap: "4 ~ 6인", img: "in-2.webp" },
    { name: "중앙 홀", cap: "테이블을 붙여 단체석으로", img: "in-3.webp" },
    { name: "창가석", cap: "4인", img: "in-4.webp" },
    { name: "테라스 쪽 자리", cap: "4 ~ 6인", img: "in-5.webp" },
    { name: "긴 부스석", cap: "8인 이상 단체", img: "in-6.webp" },
    { name: "안쪽 자리", cap: "조용한 식사", img: "in-7.webp" },
    { name: "가족석", cap: "4 ~ 6인", img: "in-8.webp" },
    { name: "저녁의 홀", cap: "", img: "in-9.webp" }
  ],
  halls: [
    { name: "외관", cap: "", img: "hero-exterior.webp" },
    { name: "창가 자리", cap: "", img: "in-10.webp" },
    { name: "넓은 홀", cap: "", img: "in-11.webp" }
  ],

  /* ---------- 장별 글·사진 ---------- */
  home: {
    heroSlides: ["hero-exterior.webp", "hero-hall.webp", "hall-green.webp"]   /* 짚불 굽는 사진은 로고가 박혀 있고 작아서 첫 화면엔 안 씀 */,
    heroTitle: "짚불로 초벌한 우대갈비",
    heroSub: "짚불태백 광교점",
    intro: {
      img: "straw-plate.webp", imgAlt: "볏짚 위에 올린 짚불구이 한 접시",
      title: "볏짚으로 굽던\n그 시절의 향",
      paras: [
        "땔감이 귀하던 시절, 추수를 마친 마을에서는 볏짚에 불을 붙여 고기를 구웠습니다. 짚불태백은 그 향을 기억합니다.",
        "순간 화력 1000도의 짚불이 육즙을 잡고, 고기에 짚 향을 입힙니다. 태백 광산부들의 노고를 씻어 주던 갈비 한 점을 그대로 재현했습니다.",
        "소갈비 가운데 가장 맛있다는 6~8번대 꽃갈비살을 볏짚과 숯으로 초벌해 상에 올립니다."
      ],
      more: "이야기 전체"
    },
    menuSec: { title: "차림", lead: "숯으로 초벌한 뒤 볏짚으로 훈연해 짚불 향을 끝까지 살렸습니다", img: "grill-table.webp", imgAlt: "불판 위의 우대갈비", more: "차림 전체" },
    spaceSec: { title: "공간", lead: "나무결과 따뜻한 조명. 가족 외식도, 회식도 편안한 자리", more: "공간 전체",
      tiles: [ { img: "hero-hall.webp", alt: "매장 홀", wide: true }, { img: "in-2.webp", alt: "부스석" }, { img: "in-5.webp", alt: "테라스 쪽 자리" }, { img: "in-8.webp", alt: "가족석" } ] },
    infoSec: { visitMore: "오시는 길 전체", telNote: "예약과 문의는 영업시간 중 언제든 연락 주세요" },
    band: { img: "in-3.webp", title: "예약", lines: ["원하시는 날짜와 인원을 선택해 예약해 주세요.", "生우대갈비는 한정 수량이라 예약하실 때 미리 말씀해 주세요."], button: "예약하기" }
  },

  about: {
    head: { img: "hero-exterior.webp", title: "이야기", sub: "醫食同源 — 입으로 먹는 음식은 몸에 약이 된다." },
    greeting: {
      title: "의식동원\n醫食同源", by: "짚불태백",
      paras: [
        "**'입으로 먹는 음식은 몸에 약이 된다.'** 짚불태백이 음식을 대하는 마음입니다.",
        "일상의 노곤함을 풀어 주고 행복을 느끼게 하는 음식은 무엇일까. 그 순간만큼은 대접받는 느낌을 드릴 수 있는 음식은 무엇일까. 이 물음에서 시작해 많은 시행착오와 연구를 거쳤습니다.",
        "답은 오래된 방식에 있었습니다. 땔감이 귀하던 시절, 추수를 마친 마을에서 볏짚으로 고기를 구워 먹던 그 향입니다.",
        "짚불태백은 그 향을 오늘의 상 위에 올립니다. 편하게 드시고 가시면 그것으로 충분합니다."
      ],
      sign: "짚불태백 광교점 드림"
    },
    chef: {
      img: "grill-fire.webp", who: "차별화된 조리 방식", name: "짚불 초벌 구이",
      quote: "\"순간 화력 1000도.\n육즙은 가두고 짚 향은 입힙니다.\"",
      para: "숯으로 먼저 초벌한 뒤 볏짚으로 훈연합니다. 센 불이 겉을 빠르게 익혀 육즙을 잡고, 볏짚이 타며 내는 향이 고기에 뱁니다. 자리에서는 드시기 좋게 마저 구워 드립니다."
    },
    story: {
      title: "짚불태백은\n다릅니다", sub: "",
      paras: [
        "**꽃갈비살.** 소갈비 가운데 가장 맛있다는 6~8번대 꽃갈비살만 씁니다. 갈비뼈 모양을 그대로 살려 정형한 것이 우대갈비입니다. 본사가 제조부터 납품까지 직접 맡습니다.",
        "**태백 김치.** 한국인의 밥상에서 가장 중요한 반찬은 김치입니다. 태백 고랭지 배추로 담가 감칠맛이 깊고 시원합니다. 짚불구이와 가장 잘 어울리는 조합입니다.",
        "**비수기 없는 차림.** 저녁에는 짚불구이, 점심에는 정식과 해장국. 가족 외식부터 회식까지 부담 없이 찾으실 수 있습니다.",
        "SBS '생방송 투데이' 와 '임원희의 미식전파사' 에 우대갈비 맛집으로 소개되었고, 2025 한국 소비자 만족도 평가 고깃집 프랜차이즈 부문 1위에 선정되었습니다."
      ],
      pics: [ { img: "grill-table.webp", alt: "불판 위의 우대갈비와 꽃갈비살" }, { img: "kimchi.webp", alt: "태백 김치" } ]
    }
  },

  space: {
    head: { img: "in-1.webp", title: "공간", sub: "나무결과 따뜻한 조명이 있는 자리입니다. 테이블을 붙이면 단체 모임도 한자리에서 하실 수 있습니다. 사진은 짚불태백 다른 지점의 모습입니다." },
    roomsTitle: "매장", hallsTitle: "외관 · 홀"
  },

  menuPage: {
    head: { img: "straw-plate.webp", title: "차림", sub: "태백 짚불구이는 숯으로 초벌한 뒤 볏짚으로 훈연해 짚불 향을 극대화했습니다." },
    pdfLabel: "메뉴판 PDF",
    chefBand: { who: "차별화된 조리 방식 · 짚불 초벌 구이", quote: "\"순간 화력 1000도, 육즙은 가두고 향은 입힙니다.\"", img: "" },
    courses: { title: "코스", sub: "" },
    lunch: { title: "점심 특선", sub: "평일 오전 11:30 – 오후 3:00" },
    dishes: { title: "짚불구이 · 생고기" }, dumplings: { title: "" }, drinks: { title: "주류" }
  },

  visit: {
    head: { img: "exterior-2.webp", title: "오시는 길", sub: "광교중앙역 4번 출구에서 걸어서 6분, 광교호수공원 가는 길에 있습니다." },
    hoursTitle: "영업시간", mapCaption: "광교중앙역 4번 출구 → 광교중앙로 → 광교중앙로248번길",
    parkingTitle: "주차",
    parking: ["건물 뒤 전용 주차장 12대 — 식사하시면 2시간 무료입니다.", "자리가 없으면 광교중앙 공영주차장(걸어서 3분)을 이용해 주세요."],
    transitTitle: "대중교통",
    transit: ["지하철 — 신분당선 광교중앙역 4번 출구, 걸어서 6분", "버스 — 광교중앙역 정류장 하차, 걸어서 4분"]
  },

  /* 차림 — 본사 사이트의 메뉴 12종. 가격은 본사 사이트에 없어 비워 둠(화면에도 안 씀).
     img 는 차림 장의 사진 카드에, pre:true 는 예약 창에서 미리 주문받는 메뉴 */
  menu: {
    courses: { title: "", items: [] },
    lunch: [
      { title: "점심 특선", sub: "",
        items: [
          { name: "짚불고기 정식", img: "m-bulgogi-set.webp" },
          { name: "짚불냉면 정식", img: "m-naengmyeon-set.webp" },
          { name: "갈비 해장국", img: "m-haejang.webp" },
          { name: "한우 육회 비빔밥", img: "m-bibimbap.webp" }
        ] }
    ],
    dishes: [
      { group: "짚불초벌구이", items: [
        { name: "生우대 갈비", badge: "한정", tag: "한정 수량 · 예약 권장", img: "m-udae-raw.webp", pre: true },
        { name: "우대 갈비", badge: "BEST", tag: "6~8번대 꽃갈비살", img: "m-udae.webp", pre: true },
        { name: "짚불 안창살", img: "m-anchang.webp", pre: true }
      ] },
      { group: "한돈짚불구이", items: [
        { name: "짚불 통 삼겹살", img: "m-samgyeop.webp", pre: true },
        { name: "짚불 마블 목살", img: "m-moksal.webp", pre: true },
        { name: "짚불 통 항정살", img: "m-hangjeong.webp", pre: true }
      ] },
      { group: "프리미엄 생고기", items: [
        { name: "한우 육사시미", img: "m-yuksashimi.webp" },
        { name: "한우 육회", img: "m-yukhoe.webp" }
      ] }
    ],
    dumplings: { items: [] },
    drinks: []
  }
};

/* 예전 이름의 전역(MENU·ROOMS·HOURS·NOTICES·INFO …) — site.js·reserve.js 가 이 이름으로 읽습니다 */
window.applySiteGlobals = function(S){
  window.SITE = S;
  window.MENU = S.menu; window.ROOMS = S.rooms; window.HALLS = S.halls;
  window.HOURS = S.hours;
  window.HOURS_NOTE = S.hoursNote || [];
  window.CLOSED = S.closed; window.HOLIDAYS = S.holidays;
  window.SIGNATURE = S.signature; window.NOTICES = S.notices; window.INFO = S.info;
};
window.applySiteGlobals(window.SITE_DEFAULT);
