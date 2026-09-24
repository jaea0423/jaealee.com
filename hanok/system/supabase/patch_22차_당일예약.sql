-- ============================================================
-- 22차 — 홈페이지 '당일 예약' 스위치 (2026-09-24). 두 번 실행해도 됩니다. dev 먼저, prod 는 실서비스 때.
-- 지금까지 서버는 '내일부터' 만 받았습니다(date > 오늘). 관리 화면에서 당일 예약을 켜면 예약 창이 오늘도 고르게 되므로
-- 서버는 오늘부터 받게 넓힙니다. 켜고 끄는 건 홈페이지 설정(SITE.online.sameDay)이 합니다 — 끈 동안은 예약 창이 오늘을 안 보여 줌.
-- 나머지는 11차 정책과 한 글자도 다르지 않습니다.
-- ============================================================
drop policy if exists anon_insert on requests;
create policy anon_insert on requests for insert to anon with check (
  store = 'hanok' and status = '대기' and res_id is null and reason = ''
  and date ~ '^\d{4}-\d{2}-\d{2}$' and time ~ '^\d{2}:\d{2}$'
  and date >= to_char(now() at time zone 'Asia/Seoul', 'YYYY-MM-DD')
  and date <= to_char((now() at time zone 'Asia/Seoul') + interval '31 days', 'YYYY-MM-DD')
  and adults between 2 and 12 and kids between 0 and 12 and people = adults + kids and people <= 12
  and seat in ('room','table') and (seat <> 'room' or adults >= 5)
  and length(name) between 1 and 30 and phone ~ '^01\d{8,9}$' and length(request) <= 300 and length(allergy) <= 100
);
