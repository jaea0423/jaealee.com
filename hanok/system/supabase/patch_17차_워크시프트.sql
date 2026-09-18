-- 17차 (2026-09-18) 워크시프트(직원 근태 → 급여까지). 15차 표에 덧붙임.
--  · staff.nick(별칭 — 화면에서 이름보다 먼저: '만두언니'), staff.tax(공제 방식: 4대보험 / 3.3% / 없음), staff.weekly_pay(주휴수당 자동 계산 여부)
--  · hr_settings: 사업장 설정 한 줄 — 5인 이상 여부(연장·야간 가산 적용), 4대보험 요율(매년 1월 확인), 야간 시간대
alter table staff add column if not exists nick text not null default '';
alter table staff add column if not exists tax text not null default '4대보험';
alter table staff add column if not exists weekly_pay boolean not null default true;
alter table staff drop constraint if exists staff_tax_check;
alter table staff add constraint staff_tax_check check (tax in ('4대보험','3.3%','없음'));

create table if not exists hr_settings (
  store       text primary key default 'hanok',
  data        jsonb not null default '{}',   -- {"over5":true, "rates":{"pension":4.5,"health":3.545,"care":12.95,"employ":0.9}, "night":["22:00","06:00"], "taxRate":3.3}
  updated_at  timestamptz not null default now()
);
drop trigger if exists t_hrs_upd on hr_settings; create trigger t_hrs_upd before update on hr_settings for each row execute function set_updated_at();
alter table hr_settings enable row level security;
drop policy if exists staff_all on hr_settings; create policy staff_all on hr_settings for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
revoke all on hr_settings from anon, authenticated;
grant select, insert, update on hr_settings to authenticated;
