-- 13차 (2026-09-17) 홈페이지 접수 제한: 같은 번호 하루 3건 → 5건 (재아). 전체 10분 20건은 그대로.
-- dev·prod 모두 SQL Editor 에서 한 번. 홈페이지 문구(js/reserve.js "이미 5건")와 숫자를 맞춰 둡니다.
create or replace function requests_rate_limit() returns trigger language plpgsql security definer as $$
begin
  if (select count(*) from requests where phone = new.phone and created_at > now() - interval '1 day') >= 5 then
    raise exception 'RATE_PHONE' using errcode = 'P0001';
  end if;
  if (select count(*) from requests where created_at > now() - interval '10 minutes') >= 20 then
    raise exception 'RATE_ALL' using errcode = 'P0001';
  end if;
  return new;
end $$;
