-- ============================================================
--  jaealee.com  ·  Reading + Screen Archive  DB 스키마
--  Supabase 대시보드 → SQL Editor 에 통째로 붙여넣고 [Run]
--  (PostgreSQL 기준)
-- ============================================================

-- gen_random_uuid() 함수를 쓰기 위한 확장 (Supabase엔 보통 이미 있음)
create extension if not exists pgcrypto;

-- ------------------------------------------------------------
-- 1) 독서 기록 테이블  (R · Reading Archive)
-- ------------------------------------------------------------
create table if not exists public.reading_books (
  id            uuid primary key default gen_random_uuid(),
  -- 이 행을 만든 사용자. 기본값이 '현재 로그인한 사용자'라서 클라이언트가 안 보내도 채워짐
  user_id       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  registered_at timestamptz not null default now(),  -- 등록일(도장에 쓰던 값)
  title         text not null,                        -- 제목 (필수)
  author        text,                                 -- 저자
  publisher     text,                                 -- 출판사
  rating        numeric(2,1) default 0,               -- 별점 0.0 ~ 5.0 (0이면 미평가)
  start_date    date,                                 -- 읽기 시작
  end_date      date,                                 -- 다 읽음
  reason        text,                                 -- 고른 계기
  plot          text,                                 -- 줄거리
  review        text,                                 -- 독후감
  cover         text                                  -- 표지 이미지(base64 data URL)
);

-- ------------------------------------------------------------
-- 2) 영화/드라마 기록 테이블  (S · Screen Archive)
-- ------------------------------------------------------------
create table if not exists public.screen_items (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  registered_at timestamptz not null default now(),
  type          text not null default 'movie',        -- movie / drama / etc
  title         text not null,                        -- 제목 (필수)
  director      text,                                 -- 감독
  "cast"        text,                                 -- 출연 ("cast"는 SQL 예약어라 큰따옴표 필수)
  genre         text,                                 -- 장르
  year          text,                                 -- 제작연도 (자유 입력이라 text)
  country       text,                                 -- 국가
  runtime       text,                                 -- 러닝타임 / 화수 / 분량
  platform      text,                                 -- 관람 플랫폼
  rating        numeric(2,1) default 0,               -- 별점 0.0 ~ 5.0
  start_date    date,                                 -- 관람 시작
  end_date      date,                                 -- 관람 완료
  reason        text,                                 -- 관람 계기
  synopsis      text,                                 -- 시놉시스
  plot          text,                                 -- 줄거리
  review        text,                                 -- 감상평
  cover         text                                  -- 포스터 이미지(base64 data URL)
);

-- ------------------------------------------------------------
-- 3) Row Level Security (RLS) 켜기
--    → 로그인한 '본인'의 행만 읽고/쓰게 만드는 잠금장치
-- ------------------------------------------------------------
alter table public.reading_books enable row level security;
alter table public.screen_items  enable row level security;

-- 본인(auth.uid() = user_id) 행에 대해서만 select/insert/update/delete 허용
create policy "own rows - reading"
  on public.reading_books
  for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "own rows - screen"
  on public.screen_items
  for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- ------------------------------------------------------------
-- 4) 정렬·검색 속도용 인덱스 (선택이지만 넣어두면 좋음)
-- ------------------------------------------------------------
create index if not exists idx_reading_user_reg on public.reading_books (user_id, registered_at desc);
create index if not exists idx_screen_user_reg  on public.screen_items  (user_id, registered_at desc);

-- 끝. 실행 후 왼쪽 Table Editor 에서 두 테이블이 보이면 성공.
