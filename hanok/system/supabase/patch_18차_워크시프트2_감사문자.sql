-- 18차 (2026-09-19) 워크시프트 2 + 감사 문자 (재아)
--  · staff.sched_hist: 정규 근무를 기간별로 [{from:"2026-01-01", days:[7], spans:[{start,end,break}]}] — 하루 두 타임도 spans 로
--  · staff.pay_hist : 시급/월급을 기간별로 [{from:"2026-09-01", pay:11000}] (기본 1일부터)
--  · staff.absent_deduct: 월급제 결근 일할 공제 여부
--  · attendance.spans: 다른 시간(△)이 하루 두 타임일 때 [{start,end,break}] (start/end 는 첫 타임을 그대로 둠)
--  · thanks_sms: 감사 문자 대기열 — 확인(방문)된 예약만, 보낼 시각에 보냄(문자 업체 연결 전엔 흉내)
alter table staff add column if not exists sched_hist jsonb not null default '[]';
alter table staff add column if not exists pay_hist jsonb not null default '[]';
alter table staff add column if not exists absent_deduct boolean not null default false;
alter table attendance add column if not exists spans jsonb not null default '[]';

create table if not exists thanks_sms (
  id          text primary key,
  store       text not null default 'hanok',
  res_id      text not null,
  phone       text not null,
  name        text not null default '',
  text        text not null,
  send_at     timestamptz not null,
  status      text not null default '대기' check (status in ('대기','보냄','취소','실패')),
  made_by     text not null default '',     -- 'ai' | 'template' | 'manual'
  by          text not null default '',
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (store, res_id)
);
drop trigger if exists t_thanks_upd on thanks_sms; create trigger t_thanks_upd before update on thanks_sms for each row execute function set_updated_at();
alter table thanks_sms enable row level security;
drop policy if exists staff_all on thanks_sms; create policy staff_all on thanks_sms for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
revoke all on thanks_sms from anon, authenticated;
grant select, insert, update on thanks_sms to authenticated;
