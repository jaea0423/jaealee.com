-- 19차 (2026-09-20) '개발자에게' (재아). 사장님·직원이 개선 요청·급한 조치를 글로 남기는 곳.
--  · 매번 전화·카톡으로 연락하는 게 서로 불편해서. 급함/보통 을 나누고, 급함만 재아에게 알림(아래 웹훅).
--  · 재아 답변(reply)·상태(status)는 재아가 적음 — 화면에서는 사장님이 상태를 '끝' 으로만 바꿀 수 있음.
create table if not exists dev_requests (
  id          text primary key,                    -- 앱이 만듦 (dq_…)
  store       text not null default 'hanok',
  title       text not null,
  body        text not null default '',
  urgent      boolean not null default false,      -- 급함(재아에게 알림) / 보통(모아서 봄)
  status      text not null default '접수' check (status in ('접수','확인','처리 중','끝')),
  images      jsonb not null default '[]',         -- 화면 사진 주소 목록(Storage site 버킷)
  by          text not null default '',            -- staff / admin
  reply       text not null default '',            -- 재아 답변
  replied_at  timestamptz,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create index if not exists dev_requests_list on dev_requests (store, created_at desc);
drop trigger if exists t_devreq_upd on dev_requests; create trigger t_devreq_upd before update on dev_requests for each row execute function set_updated_at();
alter table dev_requests enable row level security;
drop policy if exists staff_all on dev_requests; create policy staff_all on dev_requests for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
revoke all on dev_requests from anon, authenticated;
grant select, insert, update on dev_requests to authenticated;

-- 급함 알림: Supabase 대시보드 → Database → Webhooks → 새 웹훅
--   표 dev_requests · INSERT · 조건 없음(웹훅은 조건을 못 걸어 받는 쪽에서 urgent 만 거름)
--   URL 은 텔레그램 봇(https://api.telegram.org/bot<토큰>/sendMessage) 앞에 둔 작은 중계(Cloudflare Worker 등) 또는 디스코드 웹훅.
--   메일 주소는 화면에 안 박음(재아 09-20: 매크로·스팸 우려).
