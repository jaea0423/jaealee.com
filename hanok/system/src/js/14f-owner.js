/* ---------- 사장님 메뉴 (18차, 재아) ----------
   더보기(⋮) → 사장님. 관리자 비밀번호 한 번 통과하면 그 안의 것들은 다시 안 묻습니다(설정과 같은 view.adminOk).
   여기 모은 것: 디스플레이 모드 · 비상 예약지 · 워크시프트 · 손님 관리(노쇼 관리 포함) · 문자(기록·직접 보내기·감사 문자) · PIN 관리 · 홈페이지 관리.
   화면형(view.form={type:"owner", page:true}) — 큰 단추 격자. 폰에서는 두 줄. */
async function openOwnerPage(){
  if(!view.adminOk){ if(!await adminGate("사장님 메뉴 열기")) return; view.adminOk = true; }
  view.form = {type:"owner", page:true}; render();
}
function sheetOwner(){
  var item = function(fn, icon, title, sub){ return '<button class="own-it" onclick="' + fn + '">' + icon + '<b>' + title + '</b><small>' + sub + '</small></button>'; };
  var pend = typeof reqPending === "function" ? reqPending().length : 0;
  return '<div class="own-grid">' +
    item("openSiteAdmin()", ICON.site, "홈페이지 관리", "글·사진·팝업·소식·예약 접수" + (pend ? " · 대기 " + pend + "건" : "")) +
    item("openStaffPage()", ICON.staff, "워크시프트", "직원 근무표 · 급여") +
    item("openGuestsPage()", ICON.users, "손님 관리", "단골·메모 · 노쇼 관리") +
    item("openThanksPage()", ICON.spark, "감사 문자", "다녀간 손님께 AI 문자 · 예약 발송") +
    item("openSmsLog()", ICON.inbox, "문자 기록", "나간 문자 전부") +
    item("openSmsFree()", ICON.sms, "문자 직접 보내기", "번호 넣고 바로") +
    (isMobile() ? "" : item("openDisplay()", ICON.tv, "디스플레이 모드", "손님용 TV 화면")) +
    item("openSlip()", ICON.print, "비상 예약지", "시스템이 안 될 때 종이") +
    item("openPinManage()", ICON.key, "PIN 관리", "직원 PIN · 관리자 비밀번호") +
    item("setTab('settings')", ICON.set, "설정", "운영시간 · 좌석 · 코스 · 문자 안내") +
    '</div><p class="f-note">사장님만 쓰는 것들을 모았습니다. 직원 화면에서는 안 보이게 하는 작업(권한)은 나중에.</p>';
}
