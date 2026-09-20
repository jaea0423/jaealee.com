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

-- ---------- 급함 알림 → 텔레그램 (재아 09-20) ----------
-- 봇 토큰·채팅 ID 는 저장소·대화·HTML 어디에도 적지 않고 Supabase Vault 에만 둡니다.
-- 준비(대시보드에서 한 번):
--   1) Database → Extensions 에서 pg_net 켜기
--   2) Project Settings → Vault → New secret 두 개
--        이름 telegram_bot_token   값 123456:ABC-…   (BotFather 가 준 토큰)
--        이름 telegram_chat_id     값 987654321      (재아 채팅 ID — @userinfobot 에게 아무 말이나 보내면 알려 줌)
--   3) 아래를 SQL Editor 에서 실행
--   4) 봇에게 먼저 /start 한 번 보내 두기 (봇은 먼저 말을 건 사람에게만 보낼 수 있음)
create extension if not exists pg_net;
create or replace function hanok_notify_dev_request() returns trigger
language plpgsql security definer set search_path = public, vault, net as $$
declare tok text; chat text; body text;
begin
  if not new.urgent then return new; end if;   -- 보통은 알림 없음(재아가 모아서 봄)
  select decrypted_secret into tok  from vault.decrypted_secrets where name = 'telegram_bot_token' limit 1;
  select decrypted_secret into chat from vault.decrypted_secrets where name = 'telegram_chat_id'   limit 1;
  if tok is null or chat is null then return new; end if;   -- 아직 안 넣었으면 조용히 통과(글은 저장됨)
  body := '🔴 ' || case new.store when 'hanok' then '한옥반점' when 'anjip' then '안집' else new.store end || ' · 급함' || E'\n' || new.title   -- 봇 하나로 여러 가게(재아 09-20): 첫 줄에서 가게를 가름
        || E'\n' || left(coalesce(new.body, ''), 300)
        || E'\n' || '— ' || case when new.by = 'admin' then '사장님' else '직원' end || ' · ' || to_char(new.created_at at time zone 'Asia/Seoul', 'MM/DD HH24:MI');
  perform net.http_post(
    url := 'https://api.telegram.org/bot' || tok || '/sendMessage',
    headers := '{"Content-Type":"application/json"}'::jsonb,
    body := jsonb_build_object('chat_id', chat, 'text', body));
  return new;
end $$;
drop trigger if exists t_devreq_notify on dev_requests;
create trigger t_devreq_notify after insert on dev_requests for each row execute function hanok_notify_dev_request();
-- 시험: insert into dev_requests (id, title, body, urgent, by) values ('dq_test', '알림 시험', '이게 오면 됩니다', true, 'admin');  → 폰 확인 뒤 delete from dev_requests where id='dq_test';
