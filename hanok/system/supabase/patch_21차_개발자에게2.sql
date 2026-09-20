-- 21차 (2026-09-20) 개발자에게 손질 (재아)
--  · 상태는 '접수' → '답변 완료' 두 가지만 (재아가 답변을 적으면 '답변 완료'). 옛 값(확인·처리 중·끝)도 그대로 둠
--  · 사장님은 글을 지울 수 있음(삭제하기) — delete 권한
--  · 급함 알림(텔레그램)에 화면 사진 주소도 같이 (텔레그램이 링크 미리보기를 보여 줌)
alter table dev_requests drop constraint if exists dev_requests_status_check;
alter table dev_requests add constraint dev_requests_status_check check (status in ('접수','확인','처리 중','끝','답변 완료'));
grant delete on dev_requests to authenticated;

create or replace function hanok_notify_dev_request() returns trigger
language plpgsql security definer set search_path = public, vault, net as $$
declare tok text; chat text; body text; imgs text;
begin
  if not new.urgent then return new; end if;
  select decrypted_secret into tok  from vault.decrypted_secrets where name = 'telegram_bot_token' limit 1;
  select decrypted_secret into chat from vault.decrypted_secrets where name = 'telegram_chat_id'   limit 1;
  if tok is null or chat is null then return new; end if;
  select string_agg(value #>> '{}', E'\n') into imgs from jsonb_array_elements(coalesce(new.images, '[]'::jsonb));
  body := '🔴 ' || case new.store when 'hanok' then '한옥반점' when 'anjip' then '안집' else new.store end || ' · 급함' || E'\n' || new.title
        || E'\n' || left(coalesce(new.body, ''), 300)
        || case when imgs is not null and imgs <> '' then E'\n📷 ' || imgs else '' end
        || E'\n' || '— ' || case when new."by" = 'admin' then '사장님' else '직원' end || ' · ' || to_char(new.created_at at time zone 'Asia/Seoul', 'MM/DD HH24:MI');
  perform net.http_post(
    url := 'https://api.telegram.org/bot' || tok || '/sendMessage',
    headers := '{"Content-Type":"application/json"}'::jsonb,
    body := jsonb_build_object('chat_id', chat, 'text', body));
  return new;
end $$;

-- 재아가 답하는 법: Table Editor → dev_requests → 그 줄의 reply 에 답을 적고 status 를 '답변 완료' 로, replied_at 은 now().
-- 또는 SQL:  update dev_requests set reply = '…', status = '답변 완료', replied_at = now() where id = 'dq_…';
