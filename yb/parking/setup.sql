-- ============================================================
-- 대경빌 주차 관리 시스템 - Supabase 설정 SQL
-- SQL Editor 에 통째로 붙여넣고 Run 하세요.
-- 여러 번 실행해도 안전합니다.
-- ============================================================

-- 1) 차량 표 --------------------------------------------------
create table if not exists public.vehicles (
  id          uuid primary key default gen_random_uuid(),
  room        text        not null,          -- 호실 (예: 201호)
  plate       text        not null,          -- 차량번호 (예: 12가 2132)
  start_date  date        not null,          -- 등록 시작일
  end_date    date,                          -- 등록 종료일 (비우면 '미정')
  car_type    text,                          -- 차량 종류 (선택)
  memo        text,                          -- 메모 (선택)
  deleted     boolean     not null default false,
  created_at  timestamptz not null default now(),   -- 등록일 (자동)
  updated_at  timestamptz not null default now()    -- 마지막 수정일 (자동)
);

-- 이미 만들어 둔 표라면 종료일을 비워 둘 수 있게 바꿉니다
alter table public.vehicles alter column end_date drop not null;

create index if not exists vehicles_dates_idx
  on public.vehicles (deleted, start_date, end_date);

-- 2) RLS(Row Level Security, 행 수준 보안) --------------------
alter table public.vehicles enable row level security;

drop policy if exists "admin_full_access" on public.vehicles;
create policy "admin_full_access"
  on public.vehicles for all to authenticated
  using (true) with check (true);
-- anon(로그인 안 한 방문자)용 정책은 없음 => 표에 직접 접근 불가

-- 3) 방문자용 뷰: 차량번호만 -----------------------------------
create or replace view public.vehicles_public
with (security_invoker = off) as
select plate
from public.vehicles
where deleted = false
  and start_date <= current_date
  and (end_date is null or end_date >= current_date);

grant select on public.vehicles_public to anon, authenticated;

-- 4) updated_at 자동 갱신 --------------------------------------
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

-- 5) 앱 설정 표 (로그인 방식: pin / password) -------------------
-- 로그인 화면이 "지금 어떤 방식인지" 알아야 하는데,
-- 그건 로그인 '전'에 필요한 정보라 방문자도 읽을 수 있어야 합니다.
-- (방식 이름만 들어 있어 노출되어도 무해합니다)
create table if not exists public.app_settings (
  key        text primary key,
  value      text not null,
  updated_at timestamptz not null default now()
);

alter table public.app_settings enable row level security;

drop policy if exists "settings_read" on public.app_settings;
create policy "settings_read"
  on public.app_settings for select to anon, authenticated using (true);

drop policy if exists "settings_write" on public.app_settings;
create policy "settings_write"
  on public.app_settings for all to authenticated
  using (true) with check (true);

insert into public.app_settings (key, value)
values ('auth_mode', 'pin')
on conflict (key) do nothing;

drop trigger if exists settings_touch on public.app_settings;
create trigger settings_touch
  before update on public.app_settings
  for each row execute function public.touch_updated_at();

-- 6) 기존 데이터 형식 정리 (선택) -------------------------------
update public.vehicles
   set room = room || '호'
 where room !~ '호$';

update public.vehicles
   set plate = regexp_replace(replace(plate, ' ', ''), '^(.*[가-힣])(.+)$', '\1 \2')
 where plate <> regexp_replace(replace(plate, ' ', ''), '^(.*[가-힣])(.+)$', '\1 \2');

-- ============================================================
-- 7) 변경 기록(로그) 표
-- 누가 언제 무엇을 바꿨는지 남깁니다. 관리자만 읽고 쓸 수 있습니다.
-- ============================================================
create table if not exists public.logs (
  id      bigserial primary key,
  at      timestamptz not null default now(),
  action  text not null,      -- 등록 / 수정 / 연장 / 삭제 / 복구 / 영구삭제
  room    text,
  plate   text,
  detail  text
);

alter table public.logs enable row level security;

drop policy if exists "logs_admin" on public.logs;
create policy "logs_admin"
  on public.logs for all to authenticated
  using (true) with check (true);

create index if not exists logs_at_idx on public.logs (at desc);
