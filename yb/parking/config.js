/* ============================================================
   대경빌 주차 관리 시스템 - 설정 파일
   여기 세 줄만 채우면 됩니다. (README.md 참고)
   ============================================================ */

const CONFIG = {
  // 1) Supabase 프로젝트 URL  (예: "https://abcdefgh.supabase.co")
  SUPABASE_URL: "https://zfbuiwjbastohyztoexg.supabase.co",

  // 2) Supabase anon public key (eyJ... 로 시작하는 긴 문자열)
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpmYnVpd2piYXN0b2h5enRvZXhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODgyODc4MjYsImV4cCI6MjEwMzg2MzgyNn0.Sv6RdGuchVEjrHzvjsuJle6RYJ-ixdhD9qu5Th0i3QA",

  // 3) 관리자 계정 이메일 (Supabase Authentication 에 만들어 둔 계정)
  //    화면에서 입력하는 PIN/비밀번호가 이 계정의 비밀번호가 됩니다.
  ADMIN_EMAIL: "jaea0423@gmail.com",
};

/* ---------- 아래는 두 페이지가 함께 쓰는 공용 함수들 ---------- */

// 설정이 비어 있는지 확인
function configReady() {
  return CONFIG.SUPABASE_URL !== "" && CONFIG.SUPABASE_ANON_KEY !== "";
}

// Supabase 클라이언트 만들기 (supabase-js CDN 이 먼저 로드되어 있어야 함)
function makeClient() {
  return window.supabase.createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);
}

// 오늘 날짜를 "YYYY-MM-DD" 로. (UTC 가 아니라 한국 시간 기준으로 뽑습니다)
function todayStr() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, "0");
  return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
}

// Date 객체 -> "YYYY-MM-DD"
function fmt(d) {
  const p = (n) => String(n).padStart(2, "0");
  return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
}

// 시작일에서 n개월 뒤 "하루 전"을 종료일로 계산
// 예: 2026-09-02 에서 1개월 -> 2026-10-01
function addMonths(startStr, months) {
  const [y, m, day] = startStr.split("-").map(Number);
  const d = new Date(y, m - 1 + months, day);  // n개월 뒤 같은 날
  d.setDate(d.getDate() - 1);                  // 하루 빼기
  return fmt(d);
}

// 차량 한 건의 상태를 날짜로 판정
// deleted(삭제됨) > upcoming(등록 예정) > expired(만료) > active(등록 중)
function statusOf(v, today) {
  if (v.deleted) return "deleted";
  if (today < v.start_date) return "upcoming";
  if (today > v.end_date) return "expired";
  return "active";
}

const STATUS_LABEL = {
  active:   "등록 중",
  upcoming: "등록 예정",
  expired:  "만료",
  deleted:  "삭제됨",
};
