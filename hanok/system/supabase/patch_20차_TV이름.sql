-- 20차 (2026-09-20) 손님 TV 에 이름을 가리지 않고 그대로 (재아: TV 는 매장 안에 두니 가릴 이유가 없음).
-- public_today / public_screen 뷰가 mask_name() 을 부르므로, 함수를 '그대로 돌려주기' 로 바꾸면 뷰는 손댈 것 없음.
-- 다시 가리고 싶으면 patch_12차 의 함수 정의를 다시 실행하면 됩니다. dev·prod 모두 SQL Editor 에서 한 번.
create or replace function mask_name(n text) returns text language sql immutable as $$
  select trim(coalesce(n, ''))
$$;
