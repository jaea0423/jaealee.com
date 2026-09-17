-- ============================================================
-- 9차 — 홈페이지 예약 연동 (site/ ↔ v7)
-- Supabase 대시보드 → SQL Editor 에 붙여 넣고 실행. 두 번 실행해도 됩니다.
-- hanok-dev 먼저, 실서비스는 prod 에서 다시.
--
-- 구조 (왜 이렇게 했나):
--   · 홈페이지는 로그인이 없으니 anon 키로 접근합니다. anon 이 할 수 있는 건 딱 둘 —
--     ① public_avail 읽기(남은 자리)  ② requests 에 한 줄 넣기(접수). 예약 표·설정·전화번호는 절대 못 봅니다.
--   · 남은 자리 계산은 SQL 로 다시 짜지 않습니다. v7(직원 태블릿)이 이미 계산하는 값을 public_avail 에 올려 두고
--     홈페이지는 그걸 읽기만 합니다. 태블릿이 꺼져 있으면 마지막 값이 남습니다 — 접수는 어차피 직원 확인 뒤 확정이라 괜찮습니다.
--   · requests 는 v7 의 '홈페이지 예약' 창이 읽어 승인(→ reservations 에 등록)·거절합니다. 24시간 지나면 만료.
-- ============================================================

-- ---------- 1. 남은 자리 (v7 → 홈페이지) ----------
create table if not exists public_avail (
  store      text not null references stores(key),
  date       text not null,                 -- 'YYYY-MM-DD'
  data       jsonb not null default '{}',   -- {"11:00":{"rooms":[[5,7],[2,6]],"tableMax":6}, ...}  rooms = 빈 룸의 [최소,최대] 인원, tableMax = 테이블에 앉힐 수 있는 최대 인원
  updated_at timestamptz not null default now(),
  primary key (store, date)
);
alter table public_avail enable row level security;
drop policy if exists staff_all on public_avail;
drop policy if exists anon_read on public_avail;
create policy staff_all on public_avail for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
create policy anon_read on public_avail for select to anon using (true);
revoke all on public_avail from anon;   -- Supabase 기본값이 새 표에 anon 전권을 주므로 먼저 걷어냄(RLS 가 막긴 하지만 schema.sql 79행과 같은 원칙)
grant select on public_avail to anon;
grant all on public_avail to authenticated;
drop trigger if exists t_avail_upd on public_avail;
create trigger t_avail_upd before update on public_avail for each row execute function set_updated_at();

-- ---------- 2. 홈페이지 예약 접수 (홈페이지 → v7) ----------
create table if not exists requests (
  id           text primary key,            -- 홈페이지가 만든 'rq_<난수>'
  store        text not null references stores(key),
  date         text not null,
  time         text not null,
  adults       int  not null default 0,
  kids         int  not null default 0,
  people       int  not null default 0,
  seat         text not null default 'table',   -- 'room' | 'table'
  course       text not null default 'none',    -- 'course:촉 코스' | 'set:B 세트' | 'later' | 'none'
  course_label text not null default '',
  name         text not null default '',
  phone        text not null default '',        -- 숫자만
  request      text not null default '',
  status       text not null default '대기',    -- 대기 / 확정 / 거절 / 만료
  reason       text not null default '',
  res_id       text,                            -- 확정되면 reservations.id
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now(),
  expires_at   timestamptz not null default (now() + interval '24 hours')
);
create index if not exists requests_store_status on requests(store, status, created_at);
alter table requests enable row level security;
drop policy if exists staff_all   on requests;
drop policy if exists anon_insert on requests;
create policy staff_all on requests for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
-- anon 은 넣기만. 값의 모양도 여기서 한 번 더 조입니다(홈페이지 코드가 걸러도 서버가 최종)
create policy anon_insert on requests for insert to anon with check (
  store = 'hanok' and status = '대기' and res_id is null and reason = ''
  and date ~ '^\d{4}-\d{2}-\d{2}$' and time ~ '^\d{2}:\d{2}$'
  and date >  to_char(now() at time zone 'Asia/Seoul', 'YYYY-MM-DD')                       -- 당일은 전화
  and date <= to_char((now() at time zone 'Asia/Seoul') + interval '31 days', 'YYYY-MM-DD')
  and adults between 2 and 12 and kids between 0 and 12 and people = adults + kids and people <= 12
  and seat in ('room','table') and (seat <> 'room' or adults >= 5)
  and length(name) between 1 and 30 and phone ~ '^01\d{8,9}$' and length(request) <= 300
);
revoke all on requests from anon;
grant insert on requests to anon;   -- 읽기·고치기·지우기는 없음. 접수 한 줄 넣기만
grant all on requests to authenticated;
revoke delete on requests, public_avail from authenticated;   -- 지우지 않습니다(S4 와 같은 원칙)
drop trigger if exists t_req_upd on requests;
create trigger t_req_upd before update on requests for each row execute function set_updated_at();

-- 접수 폭주 막기: 같은 번호는 하루 3건(13차에서 5건으로), 전체는 10분에 20건. 넘으면 거부(홈페이지는 "잠시 뒤 다시" 안내)
create or replace function requests_rate_limit() returns trigger language plpgsql security definer as $$
begin
  if (select count(*) from requests where phone = new.phone and created_at > now() - interval '1 day') >= 3 then
    raise exception 'RATE_PHONE' using errcode = 'P0001';
  end if;
  if (select count(*) from requests where created_at > now() - interval '10 minutes') >= 20 then
    raise exception 'RATE_ALL' using errcode = 'P0001';
  end if;
  return new;
end $$;
drop trigger if exists t_req_rate on requests;
create trigger t_req_rate before insert on requests for each row execute function requests_rate_limit();

-- ---------- 3. 확인 ----------
-- select * from public_avail limit 3;
-- select id, status, date, time, people, seat, expires_at from requests order by created_at desc limit 5;
