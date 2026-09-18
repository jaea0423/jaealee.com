-- 15차 (2026-09-18) 직원 근태 + 손님 관리 (재아). 사장님이 직접 체크하는 표 — 화면은 관리자 비밀번호 뒤.
--  · staff: 직원(정규 근무 시간표·급여 방식). 퇴사는 active=false, 지우기 없음
--  · attendance: 날짜·직원마다 한 줄. 정규(○)/변형(시간 다름)/결근(×)/휴무(–), 배율(1.5배), 메모
--  · customers: 손님 메모 — 예약 자체는 reservations 에 있으니 여기엔 전화번호 열쇠 + 메모 + 이름 고정만
-- 서버 권한은 지금은 직원 로그인(hanok_is_staff)과 같음. '직원은 열람만' 은 나중 작업(권한 빼기)에서 admin 세션으로 나눕니다.
create table if not exists staff (
  id          text primary key,                    -- 앱이 만듦 (stf_…)
  store       text not null default 'hanok',
  name        text not null,
  role        text not null default '',            -- 홀·주방·매니저 같은 것(자유)
  phone       text not null default '',
  pay_type    text not null default 'hourly' check (pay_type in ('hourly','monthly')),
  pay         integer not null default 0,          -- 시급 또는 월급(원)
  sched       jsonb not null default '{}',         -- {"days":[false,true,…7], "start":"10:00", "end":"22:00", "break":60}
  start_date  date,
  end_date    date,
  memo        text not null default '',
  active      boolean not null default true,
  sort        integer not null default 0,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create table if not exists attendance (
  id          text primary key,                    -- att_<staff>_<date>
  store       text not null default 'hanok',
  staff_id    text not null references staff(id),
  date        date not null,
  status      text not null check (status in ('정규','변형','결근','휴무')),
  start       text not null default '',            -- 변형일 때 "HH:MM"
  "end"       text not null default '',
  break_min   integer not null default 0,
  rate        numeric(3,2) not null default 1,     -- 1 · 1.5 · 2
  memo        text not null default '',
  by          text not null default '',
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (store, staff_id, date)
);
create index if not exists attendance_month on attendance (store, date);
create table if not exists customers (
  store       text not null default 'hanok',
  phone       text not null,                       -- 숫자만 (01012345678)
  name        text not null default '',            -- 비우면 예약에서 가장 많이 쓴 이름
  memo        text not null default '',
  by          text not null default '',
  updated_at  timestamptz not null default now(),
  primary key (store, phone)
);
drop trigger if exists t_staff_upd on staff;      create trigger t_staff_upd before update on staff      for each row execute function set_updated_at();
drop trigger if exists t_att_upd   on attendance; create trigger t_att_upd   before update on attendance for each row execute function set_updated_at();
drop trigger if exists t_cust_upd  on customers;  create trigger t_cust_upd  before update on customers  for each row execute function set_updated_at();

alter table staff enable row level security;
alter table attendance enable row level security;
alter table customers enable row level security;
drop policy if exists staff_all on staff;      create policy staff_all on staff      for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
drop policy if exists staff_all on attendance; create policy staff_all on attendance for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
drop policy if exists staff_all on customers;  create policy staff_all on customers  for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
revoke all on staff, attendance, customers from anon, authenticated;
grant select, insert, update on staff, customers to authenticated;
grant select, insert, update, delete on attendance to authenticated;   -- 근태 칸은 '지우기' 가 자연스러움(잘못 찍은 것) — 사람·손님은 안 지움
