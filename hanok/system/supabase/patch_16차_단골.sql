-- 16차 (2026-09-18) 단골 등급 — 방문 2회 이상 VIP, 5회 이상 VVIP, 노쇼 한 번에 방문 5회를 뺌 (재아).
-- 앱(03c-tier.js)과 같은 규칙을 서버에도 두어 손님 TV(전화번호가 없는 공개 뷰)가 tier 열로 받습니다. 숫자를 바꾸면 양쪽 다.
-- security definer: 뷰 안에서 불리지만 함수는 부르는 쪽(anon) 권한으로 돌아 reservations 를 못 읽음 → 소유자 권한으로
create or replace function hanok_tier(p text) returns text language sql stable security definer set search_path = public as $$
  select case when p is null or p = '' then ''
              when s >= 5 then 'VVIP' when s >= 2 then 'VIP' else '' end
  from (select coalesce(count(*) filter (where status = '방문'), 0) - 5 * coalesce(count(*) filter (where status = '노쇼'), 0) as s
        from reservations where deleted_at is null and phone = p) x
$$;
create or replace view public_today as
  select store, time, mask_name(name) as name, people, room_id, status, data->>'seatPref' as seat_pref, hanok_tier(phone) as tier
  from reservations
  where deleted_at is null and status in ('확정','방문')
    and date = to_char(now() at time zone 'Asia/Seoul', 'YYYY-MM-DD');
grant select on public_today to anon, authenticated;
