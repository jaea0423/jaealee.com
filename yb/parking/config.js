/* ============================================================
   대경빌 주차 관리 시스템 - 설정 파일

   ※ 이 파일은 일부러 '옛날 문법(ES5)'으로 작성되어 있습니다.
      스마트TV 내장 브라우저처럼 오래된 환경에서도 돌아가야 하기 때문입니다.
      const / let / 화살표함수(=>) / padStart 등을 쓰면
      그런 브라우저에서 스크립트 전체가 멈춰 버립니다.
   ============================================================ */

var CONFIG = {
  // 1) Supabase 프로젝트 URL
  SUPABASE_URL: "https://zfbuiwjbastohyztoexg.supabase.co",

  // 2) Supabase anon public key
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpmYnVpd2piYXN0b2h5enRvZXhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgyODc4MjYsImV4cCI6MjEwMzg2MzgyNn0.Sv6RdGuchVEjrHzvjsuJle6RYJ-ixdhD9qu5Th0i3QA",

  // 3) 관리자 계정 이메일 (Supabase Authentication 에 만들어 둔 계정)
  ADMIN_EMAIL: "iamyongbum@naver.com",

  // 4) 건물 이름 (화면 제목에 쓰입니다)
  BUILDING: "대경빌",

  // 5) 이동주차 요청 연락처. 비워 두면 첫 화면에 안 나옵니다.
  CONTACT: "",

  // 6) 주차면 수. 등록 차량이 이보다 적으면 빈 칸으로 채웁니다.
  SLOTS: 20,          // PC / 태블릿
  SLOTS_MOBILE: 16    // 휴대폰
};

/* ---------- 공용 함수 ---------- */

function configReady() {
  return CONFIG.SUPABASE_URL !== "" && CONFIG.SUPABASE_ANON_KEY !== "";
}

// 관리자 화면에서만 씁니다 (supabase-js 라이브러리가 필요합니다)
function makeClient() {
  return window.supabase.createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);
}

/* ------------------------------------------------------------
   첫 화면(게시용)에서 쓰는 차량번호 읽기.
   라이브러리 없이 XMLHttpRequest 로 직접 가져옵니다.
   읽기 한 번뿐이라 라이브러리가 필요 없고,
   오래된 브라우저에서도 돌아갑니다.

   onOk(배열)      성공. [{plate:"12가 3456"}, ...]
   onFail(문구)    실패. 사람이 읽을 수 있는 이유가 들어옵니다.
------------------------------------------------------------- */
function loadPlates(onOk, onFail) {
  if (!configReady()) {
    onFail("설정이 비어 있습니다 (config.js)");
    return;
  }

  var url = CONFIG.SUPABASE_URL + "/rest/v1/vehicles_public?select=plate";
  var xhr = new XMLHttpRequest();

  try {
    xhr.open("GET", url, true);
  } catch (e) {
    onFail("주소를 열 수 없습니다");
    return;
  }

  xhr.setRequestHeader("apikey", CONFIG.SUPABASE_ANON_KEY);
  xhr.setRequestHeader("Authorization", "Bearer " + CONFIG.SUPABASE_ANON_KEY);
  xhr.setRequestHeader("Accept", "application/json");
  xhr.timeout = 15000;

  xhr.onreadystatechange = function () {
    if (xhr.readyState !== 4) { return; }

    if (xhr.status === 0) {
      onFail("서버에 연결하지 못했습니다 (인터넷 또는 보안 연결 문제)");
      return;
    }
    if (xhr.status !== 200) {
      onFail("서버 응답 오류 " + xhr.status);
      return;
    }

    var data;
    try {
      data = JSON.parse(xhr.responseText);
    } catch (e2) {
      onFail("응답을 해석하지 못했습니다");
      return;
    }
    if (!data || typeof data.length !== "number") {
      onFail("예상과 다른 응답입니다");
      return;
    }
    onOk(data);
  };

  xhr.ontimeout = function () { onFail("서버 응답이 너무 느립니다"); };

  try {
    xhr.send();
  } catch (e3) {
    onFail("요청을 보내지 못했습니다");
  }
}

/* ------------------------------------------------------------
   설정값 하나 읽기 (app_settings 표). 라이브러리 없이 동작합니다.
   로그인 전에도 읽을 수 있는 공개 설정만 들어 있습니다.
     cb(값)   성공. 값이 없으면 null
     cb(null) 실패해도 null (게시 화면이 멈추면 안 되므로 조용히 넘어갑니다)
------------------------------------------------------------- */
function readSetting(key, cb) {
  if (!configReady()) { cb(null); return; }

  var url = CONFIG.SUPABASE_URL
          + "/rest/v1/app_settings?select=value&key=eq."
          + encodeURIComponent(key);
  var xhr = new XMLHttpRequest();

  try { xhr.open("GET", url, true); } catch (e) { cb(null); return; }

  xhr.setRequestHeader("apikey", CONFIG.SUPABASE_ANON_KEY);
  xhr.setRequestHeader("Authorization", "Bearer " + CONFIG.SUPABASE_ANON_KEY);
  xhr.setRequestHeader("Accept", "application/json");
  xhr.timeout = 10000;

  xhr.onreadystatechange = function () {
    if (xhr.readyState !== 4) { return; }
    if (xhr.status !== 200) { cb(null); return; }
    var d;
    try { d = JSON.parse(xhr.responseText); } catch (e2) { cb(null); return; }
    cb(d && d.length ? d[0].value : null);
  };
  xhr.ontimeout = function () { cb(null); };

  try { xhr.send(); } catch (e3) { cb(null); }
}

/* ------------------------------------------------------------
   게시 화면 원격 새로고침.

   관리자 화면에서 "새로고침 신호"를 누르면 app_settings 의
   reload_token 값이 바뀝니다. 게시 화면들은 1분마다 이 값을 보고,
   자기가 처음 봤던 값과 달라지면 스스로 페이지를 다시 엽니다.

   주소 뒤에 ?v=... 를 붙여 여는 이유는, 그래야 브라우저가
   캐시에 둔 옛날 코드가 아니라 새 코드를 받아오기 때문입니다.
------------------------------------------------------------- */
function watchReload() {
  var seen = null;

  function check() {
    readSetting("reload_token", function (val) {
      if (val === null) { return; }          // 못 읽었으면 그냥 넘어갑니다
      if (seen === null) { seen = val; return; }   // 처음 본 값을 기준으로 삼습니다
      if (val !== seen) {
        location.replace(location.pathname + "?v=" + encodeURIComponent(val));
      }
    });
  }

  check();
  setInterval(check, 60000);   // 1분마다
}

/* ---------- 날짜 ---------- */

function pad2(n) {
  n = String(n);
  return n.length < 2 ? "0" + n : n;
}

// Date -> "YYYY-MM-DD"
function fmt(d) {
  return d.getFullYear() + "-" + pad2(d.getMonth() + 1) + "-" + pad2(d.getDate());
}

function todayStr() { return fmt(new Date()); }

// "2026-09-02T05:11:22Z" -> "2026-09-02 14:11"
function fmtDateTime(iso) {
  if (!iso) { return "-"; }
  var d = new Date(iso);
  if (isNaN(d.getTime())) { return "-"; }
  return d.getFullYear() + "-" + pad2(d.getMonth() + 1) + "-" + pad2(d.getDate())
       + " " + pad2(d.getHours()) + ":" + pad2(d.getMinutes());
}

/* ---------- 기간 계산 ----------
   n개월짜리 기간의 종료일은 "n개월 뒤 같은 날의 하루 전" 입니다.
     10월 1일 시작 + 1개월 -> 10월 31일
     9월  4일 시작 + 1개월 -> 10월 3일
   대상 월에 그 날짜가 없으면(2월 30일 등) 그 달 말일로 맞춥니다.
     1월 31일 시작 + 1개월 -> 2월 28일
------------------------------------------------------------- */
function addMonths(startStr, months) {
  var a = startStr.split("-");
  var y = Number(a[0]), m = Number(a[1]), day = Number(a[2]);

  var tm = (m - 1) + months;
  var ty = y + Math.floor(tm / 12);
  tm = ((tm % 12) + 12) % 12;

  var target = day - 1;               // "하루 전"

  if (target === 0) {
    // 1일 시작 -> 목표 월의 '직전 달' 마지막 날
    var d = new Date(ty, tm, 1);
    d.setDate(0);
    return fmt(d);
  }

  var lastDay = new Date(ty, tm + 1, 0).getDate();   // 목표 월의 말일
  return fmt(new Date(ty, tm, Math.min(target, lastDay)));
}

// n일짜리 기간의 종료일 (3주 = 21일 -> 시작일 + 20일)
function addDays(startStr, days) {
  var a = startStr.split("-");
  var d = new Date(Number(a[0]), Number(a[1]) - 1, Number(a[2]));
  d.setDate(d.getDate() + days - 1);
  return fmt(d);
}

/* ---------- 호실 ---------- */
// "401" -> "401호" (이미 '호'로 끝나면 그대로)
function normRoom(s) {
  var t = (s || "");
  t = t.replace(/^\s+|\s+$/g, "");
  if (t === "") { return ""; }
  return /호$/.test(t) ? t : t + "호";
}

/* ---------- 차량번호 ---------- */
// 공백을 모두 없애고 마지막 한글 뒤에만 한 칸을 넣습니다.
// "12가2132" -> "12가 2132",  "서울12가3456" -> "서울12가 3456"
function formatPlate(s) {
  var t = (s || "").replace(/\s+/g, "");
  var m = t.match(/^(.*[가-힣])(.+)$/);
  return m ? m[1] + " " + m[2] : t;
}

/* ---------- 상태 ---------- */
// end_date 가 비어 있으면(미정) 만료되지 않습니다.
function statusOf(v, today) {
  if (v.deleted) { return "deleted"; }
  if (today < v.start_date) { return "upcoming"; }
  if (v.end_date && today > v.end_date) { return "expired"; }
  return "active";
}

var STATUS_LABEL = {
  active:   "등록 중",
  upcoming: "등록 예정",
  expired:  "만료",
  deleted:  "삭제됨"
};

function periodText(v) {
  return v.start_date + " ~ " + (v.end_date ? v.end_date : "미정");
}

/* ---------- 정렬 ---------- */
// 호실을 숫자로 비교합니다. "101호" < "201호" < "1001호"
function roomKey(r) {
  var m = String(r || "").match(/\d+/);
  return m ? parseInt(m[0], 10) : 999999;
}

function byRoom(a, b) {
  return roomKey(a.room) - roomKey(b.room)
      || String(a.room).localeCompare(String(b.room))
      || String(a.plate).localeCompare(String(b.plate));
}

// 종료일까지 남은 날 (미정이면 null)
function daysLeft(v, today) {
  if (!v.end_date) { return null; }
  var a = new Date(today), b = new Date(v.end_date);
  return Math.round((b.getTime() - a.getTime()) / 86400000);
}

/* ---------- 연장 ----------
   만료된 차량을 연장할 때 이미 지나간 날짜에 붙이면 여전히 만료 상태가 됩니다.
   그래서 "기존 종료일 다음 날" 과 "오늘" 중 늦은 쪽을 시작점으로 잡습니다.
--------------------------------------------------------------- */
function extendFrom(v, today) {
  if (!v.end_date) { return today; }
  var a = v.end_date.split("-");
  var d = new Date(Number(a[0]), Number(a[1]) - 1, Number(a[2]));
  d.setDate(d.getDate() + 1);
  var next = fmt(d);
  return next > today ? next : today;
}

// 임박 기준: 종료일까지 7일 이하로 남은 '등록 중' 차량
var SOON_DAYS = 7;
function isSoon(v, today) {
  if (statusOf(v, today) !== "active") { return false; }
  var left = daysLeft(v, today);
  return left !== null && left <= SOON_DAYS;
}
