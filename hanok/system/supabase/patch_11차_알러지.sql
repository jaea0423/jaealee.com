-- ============================================================
-- 11차 — 홈페이지 예약 접수에 알레르기 칸 (2026-09-17). 두 번 실행해도 됩니다. dev 먼저, prod 는 실서비스 때.
-- 요청사항에 섞어 적으면 시스템의 '알러지 없음' 확인과 연동이 안 되므로 칸을 따로 둡니다(재아).
-- ============================================================
alter table requests add column if not exists allergy text not null default '';
-- anon_insert 정책에 길이 제한 추가(100자). 정책은 통째로 다시 만듭니다 — 9차 것과 같고 allergy 줄만 더함
drop policy if exists anon_insert on requests;
create policy anon_insert on requests for insert to anon with check (
  store = 'hanok' and status = '대기' and res_id is null and reason = ''
  and date ~ '^\d{4}-\d{2}-\d{2}$' and time ~ '^\d{2}:\d{2}$'
  and date >  to_char(now() at time zone 'Asia/Seoul', 'YYYY-MM-DD')
  and date <= to_char((now() at time zone 'Asia/Seoul') + interval '31 days', 'YYYY-MM-DD')
  and adults between 2 and 12 and kids between 0 and 12 and people = adults + kids and people <= 12
  and seat in ('room','table') and (seat <> 'room' or adults >= 5)
  and length(name) between 1 and 30 and phone ~ '^01\d{8,9}$' and length(request) <= 300 and length(allergy) <= 100
);
