/* ============================================================
   데이터 정의
   ============================================================ */
const STORAGE_KEY = "hanok-admin-v2";

/* 문자 기본값.
   ※ DEFAULT_DATA 가 이 값을 펼쳐 쓰므로 **반드시 DEFAULT_DATA 보다 위에** 있어야 합니다.
      아래에 두면 var 호이스팅 때문에 값이 undefined 인 채로 펼쳐져 sms:{} 가 되고,
      저장된 기록이 없는 첫 실행에서 재안내 시각이 비어 버립니다(migrate 를 안 타므로). */
var SMS_DEFAULT = {
  on:true,
  skipNaver:true,         /* 네이버 예약은 네이버가 문자를 보내므로 우리는 안 보냄(재아) */
  storePhone:"031-724-1004",   /* 발신번호 — 매장 번호. 실제 발송을 붙일 때 통신사에 등록 */
  remindOffset:0,         /* 재안내를 며칠 전에 — 2 | 1 | 0(당일) */
  remindHour:9,           /* 그날 몇 시에 */
  parkingNote:"※ 주차 안내\n주차장 이용 가능합니다. 주차비 1,000원이며 발렛은 무료입니다.",
  /* 문안(8차-X, 재아): 설정에서 고칠 수 있습니다. {매장} {이름} {일시} {인원} {주차} {오늘내일} 자리에 값이 들어갑니다 */
  tplNew:"[ 예약 완료 안내 ]\n\n안녕하세요, {매장}입니다.\n예약확인 문자 드립니다.\n\n{이름} 님\n{일시}\n{인원}\n\n예약해주셔서 감사합니다.",
  tplRemind:"[ 예약 방문 안내 ]\n\n{오늘내일} 예약 방문 안내드립니다.\n\n{이름} 님\n{일시}\n{인원}\n\n{주차}\n\n시간 변경이 필요하시면 미리 연락 주시기 바랍니다.\n\n감사합니다."
};
const DEFAULT_DATA = {
  hanok: {
    name:"한옥반점", sub:"중식 코스 요리", enabled:true,
    settings:{
      open:"11:00", close:"22:00", lastOrder:"20:40", tempClosed:false,
      /* 요일별 운영시간 — 적용 시작일을 두고 여러 벌을 보관합니다.
         나중에 시간이 바뀌어도 과거 기록의 계산이 틀어지지 않습니다. */
      schedules:[{
        from:"2000-01-01",
        /* 세션(8차-X): 하루를 '점심 경계'(edge) 하나로 점심/저녁으로 나눕니다. 브레이크가 있는 날은 경계 = 브레이크 시작(자동, 잠김).
           점심·저녁마다 접수 마감(lastBook)과 점유(room/table: "end" = 세션 끝까지 한 팀, 숫자 = 분). 경계가 비면 하루가 한 세션(저녁 규칙).
           토·일·공휴일 점심은 1시간 50분(브레이크 없음, 15:30 경계). 경계 시각(15:30) 자체는 저녁으로 칩니다. 실제 세션 목록은 sessionsOfDay() 가 만듭니다 */
        days:[
          {open:"11:00", close:"20:30", lo:"19:40", bs:"",      be:"",
           sess:{edge:"15:30", lunch:{lastBook:"15:30", room:110, table:110}, dinner:{lastBook:"18:30", room:"end", table:"end"}}},   /* 일 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sess:{edge:"15:30", lunch:{lastBook:"14:00", room:"end", table:"end"}, dinner:{lastBook:"19:30", room:"end", table:"end"}}},   /* 월 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sess:{edge:"15:30", lunch:{lastBook:"14:00", room:"end", table:"end"}, dinner:{lastBook:"19:30", room:"end", table:"end"}}},   /* 화 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sess:{edge:"15:30", lunch:{lastBook:"14:00", room:"end", table:"end"}, dinner:{lastBook:"19:30", room:"end", table:"end"}}},   /* 수 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sess:{edge:"15:30", lunch:{lastBook:"14:00", room:"end", table:"end"}, dinner:{lastBook:"19:30", room:"end", table:"end"}}},   /* 목 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"15:30", be:"17:00",
           sess:{edge:"15:30", lunch:{lastBook:"14:00", room:"end", table:"end"}, dinner:{lastBook:"19:30", room:"end", table:"end"}}},   /* 금 */
          {open:"11:00", close:"22:00", lo:"20:40", bs:"",      be:"",
           sess:{edge:"15:30", lunch:{lastBook:"15:30", room:110, table:110}, dinner:{lastBook:"19:30", room:"end", table:"end"}}}    /* 토 */
        ],
        /* 공휴일은 일요일과 같습니다 (설정에서 변경) */
        holiday:{open:"11:00", close:"20:30", lo:"19:40", bs:"", be:"",
           sess:{edge:"15:30", lunch:{lastBook:"15:30", room:110, table:110}, dinner:{lastBook:"18:30", room:"end", table:"end"}}}
      }],
      overrides:[],        /* 임시 휴무·단축 영업 등 특정 날짜만 다른 경우 */
      /* 손님용 목록 화면 왼쪽에 트는 광고 영상.
         v3 폴더에 ad.mp4 를 올려 두기만 하면 바로 나옵니다.
         파일이 없으면 매장 사진으로 되돌아가므로 기본값으로 둬도 안전합니다. */
      tvAd:"ad.mp4",
      /* 문자 안내 — 지금은 흉내만 냅니다 (실제로 나가지 않습니다). 기본값은 SMS_DEFAULT 참고 */
      sms:{ ...SMS_DEFAULT },
      breakMode:"leave",       /* leave = 매장을 비움, order = 음식 주문만 중단 */
      breakEntryBuffer:60,     /* 주문만 중단일 때, 브레이크 몇 분 전까지 받을지 */
      stayHours:3,          /* 룸 저녁 체류 시간 */
      lunchStayHours:2.5,   /* 룸 점심 체류 시간 */
      hallStayHours:2.5,    /* 홀 저녁 체류 시간 — 테이블 단위라 룸보다 짧게 */
      hallLunchStayHours:2, /* 홀 점심 체류 시간 */
      lunchUntil:"16:00",   /* 이 시각 전 예약은 점심으로 계산 */
      lastBookingBuffer:60, /* 영업 종료 몇 분 전까지 예약을 받을지 */
      minCountAdultsOnly:true,  /* 룸 최소 인원을 성인 기준으로 볼지 */
      groupSize:8,              /* 이 인원부터 단체로 봅니다 */
      displayRows:null,         /* 디스플레이 모드 좌석 배치 (null이면 자동) */
      holidayMode:true,         /* 공휴일 별도 운영시간 사용 */
      holidays:[],              /* 사장이 직접 등록하는 공휴일(내장표에 없는 임시공휴일·선거일 등). holidaysOff 는 내장표에서 뺄 날짜 */
      holidaysOff:[],
      holidayAsWeekend:true,    /* 코스 시간대에서 공휴일을 주말로 봄 */
      courseGroups:[
        { id:"cg_dinner",  label:"저녁 (종일)", items:["오","촉","한","위"],    when:["종일"] },
        { id:"cg_wdlunch", label:"평일 점심",   items:["요리사","동한","서한"], when:["평일점심"] },
        { id:"cg_welunch", label:"주말 점심",   items:["요리사","B","A"],       when:["주말점심"] }
      ],
      /* ---------- 좌석 (8차, 누님 답) ----------
         룸: minCapacity = 최적(=최소) 인원, capacity = 최대. 배열 순서 = 사장님 배정 우선순위(설정에서 ▲▼).
         테이블: 개별 이름. seats = 기본 인원, capacity 가 있으면 그것이 최대(여포 4~5). joinWith = 붙일 수 있는 테이블.
                 '홀' 이라는 묶음은 없습니다 — 층(floor)으로만 묶어 보여 줍니다. 가게에서 '테이블 예약 / 룸 예약' 이라고 부릅니다 */
      rooms:[
        {id:"r1",name:"조조",type:"room",floor:"1층",minCapacity:2,minWeekend:4,optCapacity:4,capacity:6},
        {id:"r2",name:"유비",type:"room",floor:"1층",minCapacity:6,minWeekend:8,optCapacity:8,capacity:9},
        {id:"r3",name:"장비",type:"room",floor:"1층",minCapacity:4,minWeekend:6,optCapacity:6,capacity:7},
        {id:"r4",name:"관우",type:"room",floor:"1층",minCapacity:4,minWeekend:6,optCapacity:6,capacity:7},
        {id:"r5",name:"공명",type:"room",floor:"지하",minCapacity:4,minWeekend:6,optCapacity:6,capacity:7},
        {id:"r6",name:"주유",type:"room",floor:"지하",minCapacity:4,minWeekend:6,optCapacity:6,capacity:7},
        {id:"r7",name:"초선",type:"room",floor:"지하",minCapacity:4,minWeekend:6,optCapacity:6,capacity:7},
        {id:"r8",name:"동탁",type:"room",floor:"지하",minCapacity:10,minWeekend:12,optCapacity:12,capacity:14},
        {id:"t21", name:"21",  type:"table",floor:"1층",seats:4,joinWith:[]},
        {id:"t22", name:"22",  type:"table",floor:"1층",seats:4,joinWith:[]},
        {id:"t23a",name:"23-4",type:"table",floor:"1층",seats:4,joinWith:["t23b"]},
        {id:"t23b",name:"23-2",type:"table",floor:"1층",seats:2,joinWith:["t23a"]},
        {id:"t24", name:"24",  type:"table",floor:"1층",seats:2,joinWith:[]},
        {id:"t25", name:"25",  type:"table",floor:"1층",seats:2,joinWith:[]},
        {id:"tyb", name:"여포",    type:"table",floor:"지하",seats:4,capacity:5,minCapacity:4,joinWith:[],note:"파셜룸"},
        {id:"thd", name:"하후돈",  type:"table",floor:"지하",seats:4,joinWith:["ths1","ths2","thy","the"]},
        {id:"ths1",name:"하후상-1",type:"table",floor:"지하",seats:4,joinWith:["thd","ths2","thy","the"]},
        {id:"ths2",name:"하후상-2",type:"table",floor:"지하",seats:4,joinWith:["thd","ths1","thy","the"]},
        {id:"thy", name:"하후연",  type:"table",floor:"지하",seats:2,joinWith:["thd","ths1","ths2","the"]},
        {id:"the", name:"하후은",  type:"table",floor:"지하",seats:2,joinWith:["thd","ths1","ths2","thy"]}
      ],
      /* 룸 합침(중문 탈거). 자동(잠정) 배정에는 쓰지 않고 사람이 고를 때만. 원탁은 공간만 합쳐지고 테이블은 나뉘어 손님 확인이 필요 */
      joins:[
        {id:"j1",ids:["r3","r4"],     min:12,max:14,note:"중문 탈거"},
        {id:"j2",ids:["r5","r6"],     min:12,max:14,split:true,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"},
        {id:"j3",ids:["r6","r7"],     min:12,max:14,split:true,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"},
        {id:"j4",ids:["r5","r6","r7"],min:18,max:21,split:true,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"}
      ],
      sources:["전화 예약","네이버 예약","방문","기타"],
      roles:["점장","매니저","주방장","주방","서빙","발렛"]
    },
    reservations:[], staff:[], attendance:[], sales:[]
  },
  anjip:{
    name:"안집", sub:"한정식 · 소고기 · 간장게장", enabled:false,
    settings:{open:"11:30",close:"22:00",lastOrder:"21:30",tempClosed:false,rooms:[],sources:["전화","네이버예약","기타"],roles:["점장","홀","주방"]},
    reservations:[], staff:[], attendance:[], sales:[]
  }
};

const STATUS = ["확정","방문","취소","노쇼"];

let DATA = null;
/* 인증 기본값 — 설정에서 변경 가능 (변경 시 관리자 비밀번호 필요) */
const LOG_MAX = 3000;      /* 로그는 최근 3000건까지 보관 */
let CLIENT_IP = "";  /* 접속 IP 는 더 이상 조회하지 않습니다(외부 요청 0 원칙 — 점검 S6). 서버 로그에는 계정(who)만 남습니다 */
let view = { storeKey:null, tab:"dash", date:todayStr(), filter:"예정", form:null, salesMonth:monthStr(), payMonth:monthStr(), calMonth:monthStr(), calOpen:false, display:false, open:{list:false, rate:false} };
