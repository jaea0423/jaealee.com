-- ============================================================
-- 대경빌 주차 관리 시스템 - Supabase 최초 설정 SQL
-- Supabase 대시보드 > SQL Editor 에 통째로 붙여넣고 Run 하세요.
-- 한 번만 실행하면 됩니다.
-- ============================================================

-- 1) 차량 표(table) 만들기 -----------------------------------
create table if not exists public.vehicles (
  id          uuid primary key default gen_random_uuid(),
  room        text        not null,          -- 호실 (예: 201호)
  plate       text        not null,          -- 차량번호 (예: 123가 6456)
  start_date  date        not null,          -- 등록 시작일
  end_date    date        not null,          -- 등록 종료일
  car_type    text,                          -- 차량 종류 (선택)
  memo        text,                          -- 메모 (선택)
  deleted     boolean     not null default false,  -- 삭제함으로 옮겼는지
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- 목록을 자주 정렬/검색하므로 색인(index)을 하나 둡니다
create index if not exists vehicles_dates_idx
  on public.vehicles (deleted, start_date, end_date);

-- 2) RLS 켜기 ------------------------------------------------
-- RLS(Row Level Security, 행 수준 보안)를 켜면
-- "정책(policy)에서 허용한 것 외에는 전부 거부" 가 기본이 됩니다.
alter table public.vehicles enable row level security;

-- 3) 정책: 로그인한 관리자만 전체 읽기/쓰기 -------------------
drop policy if exists "admin_full_access" on public.vehicles;
create policy "admin_full_access"
  on public.vehicles
  for all
  to authenticated          -- 로그인한 사용자만
  using (true)
  with check (true);

-- anon(로그인 안 한 방문자)용 정책은 일부러 만들지 않습니다.
-- => 방문자는 이 표를 직접 읽을 수 없습니다. (호실/메모 보호)

-- 4) 방문자에게 보여줄 "차량번호만" 뷰(view) ------------------
-- 지금 등록 기간 안에 있고 삭제되지 않은 차량의 번호만 노출합니다.
create or replace view public.vehicles_public
with (security_invoker = off) as     -- 뷰 소유자 권한으로 실행 => RLS 우회
select plate
from public.vehicles
where deleted = false
  and current_date between start_date and end_date;

-- 방문자(anon)와 관리자(authenticated) 모두 이 뷰는 읽을 수 있게
grant select on public.vehicles_public to anon, authenticated;

-- 5) updated_at 자동 갱신 -------------------------------------
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists vehicles_touch on public.vehicles;
create trigger vehicles_touch
  before update on public.vehicles
  for each row execute function public.touch_updated_at();
