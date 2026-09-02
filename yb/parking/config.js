/* ============================================================
   대경빌 주차 관리 시스템 - 설정 파일
   ============================================================ */

const CONFIG = {
  // 1) Supabase 프로젝트 URL
  SUPABASE_URL: "https://zfbuiwjbastohyztoexg.supabase.co",

  // 2) Supabase anon public key
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpmYnVpd2piYXN0b2h5enRvZXhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgyODc4MjYsImV4cCI6MjEwMzg2MzgyNn0.Sv6RdGuchVEjrHzvjsuJle6RYJ-ixdhD9qu5Th0i3QA",

  // 3) 관리자 계정 이메일 (Supabase Authentication 에 만들어 둔 계정)
  ADMIN_EMAIL: "iamyongbum@naver.com",

  // 4) 건물 이름 (화면 제목에 쓰입니다)
  BUILDING: "대경빌",

  // 5) 이동주차 요청 연락처. 비워 두면 첫 화면에 안 나옵니다.
  //    예: "010-1234-5678"
  CONTACT: "",
};

/* ---------- 공용 함수 ---------- */

function configReady() {
  return CONFIG.SUPABASE_URL !== "" && CONFIG.SUPABASE_ANON_KEY !== "";
}

function makeClient() {
  return window.supabase.createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);
}

// Date -> "YYYY-MM-DD"
function fmt(d) {
  const p = (n) => String(n).padStart(2, "0");
  return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
}

function todayStr() { return fmt(new Date()); }

// "2026-09-02T05:11:22Z" -> "2026-09-02 14:11"
function fmtDateTime(iso) {
  if (!iso) { return "-"; }
  const d = new Date(iso);
  if (isNaN(d)) { return "-"; }
  const p = (n) => String(n).padStart(2, "0");
  return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate())
       + " " + p(d.getHours()) + ":" + p(d.getMinutes());
}

/* ---------- 기간 계산 ----------
   "날짜 기준" 규칙입니다. n개월짜리 기간의 종료일은
   "n개월 뒤 같은 날의 하루 전" 입니다.
     10월 1일 시작 + 1개월 -> 10월 31일
     9월  4일 시작 + 1개월 -> 10월 3일
   시작일이 1일이면 그 달의 마지막 날이 종료일이 되고,
   대상 월에 그 날짜가 없으면(2월 30일 등) 그 달 말일로 맞춥니다.
     1월 31일 시작 + 1개월 -> 2월 28일
------------------------------------------------------------- */
function addMonths(startStr, months) {
  const [y, m, day] = startStr.split("-").map(Number);

  // 목표 연/월 구하기 (0=1월)
  let tm = (m - 1) + months;
  const ty = y + Math.floor(tm / 12);
  tm = ((tm % 12) + 12) % 12;

  const target = day - 1;               // "하루 전"

  if (target === 0) {
    // 1일 시작 -> 목표 월의 '직전 달' 마지막 날
    const d = new Date(ty, tm, 1);
    d.setDate(0);                       // 0일 = 전달 마지막 날
    return fmt(d);
  }

  const lastDay = new Date(ty, tm + 1, 0).getDate();   // 목표 월의 말일
  return fmt(new Date(ty, tm, Math.min(target, lastDay)));
}

// n일짜리 기간의 종료일 (3주 = 21일 -> 시작일 + 20일)
function addDays(startStr, days) {
  const [y, m, day] = startStr.split("-").map(Number);
  const d = new Date(y, m - 1, day);
  d.setDate(d.getDate() + days - 1);
  return fmt(d);
}

/* ---------- 호실 ---------- */
// "401" -> "401호" (이미 '호'로 끝나면 그대로)
function normRoom(s) {
  const t = (s || "").trim();
  if (t === "") { return ""; }
  return /호$/.test(t) ? t : t + "호";
}

/* ---------- 차량번호 ---------- */
// 공백을 모두 없애고 마지막 한글 뒤에만 한 칸을 넣습니다.
// "12가2132" -> "12가 2132",  "서울12가3456" -> "서울12가 3456"
function formatPlate(s) {
  const t = (s || "").replace(/\s+/g, "");
  const m = t.match(/^(.*[가-힣])(.+)$/);
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

const STATUS_LABEL = {
  active:   "등록 중",
  upcoming: "등록 예정",
  expired:  "만료",
  deleted:  "삭제됨",
};

function periodText(v) {
  return v.start_date + " ~ " + (v.end_date ? v.end_date : "미정");
}

/* ---------- 정렬 ---------- */
// 호실을 숫자로 비교합니다. "101호" < "201호" < "1001호"
function roomKey(r) {
  const m = String(r || "").match(/\d+/);
  return m ? parseInt(m[0], 10) : 999999;
}

function byRoom(a, b) {
  return roomKey(a.room) - roomKey(b.room)
      || String(a.room).localeCompare(String(b.room), "ko")
      || String(a.plate).localeCompare(String(b.plate), "ko");
}

// 종료일까지 남은 날 (미정이면 null)
function daysLeft(v, today) {
  if (!v.end_date) { return null; }
  const a = new Date(today), b = new Date(v.end_date);
  return Math.round((b - a) / 86400000);
}

/* ---------- 연장 ----------
   만료된 차량을 연장할 때, 이미 지나간 날짜에 붙이면 여전히 만료 상태가 됩니다.
   그래서 "기존 종료일 다음 날" 과 "오늘" 중 늦은 쪽을 시작점으로 잡습니다.
--------------------------------------------------------------- */
function extendFrom(v, today) {
  if (!v.end_date) { return today; }
  const a = v.end_date.split("-").map(Number);
  const d = new Date(a[0], a[1] - 1, a[2]);
  d.setDate(d.getDate() + 1);
  const next = fmt(d);
  return next > today ? next : today;
}

// 임박 기준: 종료일까지 7일 이하로 남은 '등록 중' 차량
const SOON_DAYS = 7;
function isSoon(v, today) {
  if (statusOf(v, today) !== "active") { return false; }
  const left = daysLeft(v, today);
  return left !== null && left <= SOON_DAYS;
}
