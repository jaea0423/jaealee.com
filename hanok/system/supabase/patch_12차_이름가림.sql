-- 12차 (2026-09-17) 손님 TV 이름 가림을 앱(maskName)과 같은 모양으로.
--  · 예전: 세 글자 넘어도 '김 * 아' 처럼 별 하나 → 글자 수를 알 수 없고, 외국 이름은 'T * e' 로 이상함
--  · 지금: 띄어쓰기는 빼고 첫 글자·끝 글자만 남기고 글자 수만큼 별 (재아) — 남궁민수 → 남 * * 수, Tom Cruise → T * * * * * * * e
-- public_today / public_screen 뷰는 이 함수를 그대로 부르므로 함수만 바꾸면 됩니다. dev·prod 모두 SQL Editor 에서 한 번.
create or replace function mask_name(n text) returns text language sql immutable as $$
  with s as (select regexp_replace(trim(coalesce(n, '')), '\s+', '', 'g') as v)
  select case when length(v) <= 1 then '*'
              when length(v) = 2 then left(v, 1) || ' *'
              else left(v, 1) || ' ' || array_to_string(array_fill('*'::text, array[length(v) - 2]), ' ') || ' ' || right(v, 1) end
  from s
$$;
