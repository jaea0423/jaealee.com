-- DineONE DB 변경 0003 (2026-11-12) — 매장 화면(직원)이 실제 DB 로 일하기 위한 보강
-- 0001(draft) · 0002(devices) 다음. dev 에 한 번만 실행.

-- 1. '예약 손님 자리 없음 → 웨이팅 맨 앞' 에서 어느 예약의 웨이팅인지 잇기
alter table waitlist add column reservation_id uuid references reservations(id);

-- 2. 웨이팅 접수 켜기·끄기 같은 기능 스위치는 사장·매니저가 바꿈
create policy features_add on store_features for insert
  with check (is_staff(store_id, array['owner','manager']));
create policy features_edit on store_features for update
  using (is_staff(store_id, array['owner','manager'])) with check (is_staff(store_id, array['owner','manager']));
grant insert, update on store_features to authenticated;

-- 3. 직원이 웨이팅을 직접 등록 (번호는 DB 가 매김 — 입구 기기와 겹치지 않게)
create function staff_wait_add(p_store uuid, p_id uuid, p_people int, p_phone text,
                               p_priority boolean default false, p_reservation uuid default null)
returns int
language plpgsql volatile security definer set search_path = public as $$
declare
  v_no int;
  v_ahead int;
  ph text := nullif(regexp_replace(coalesce(p_phone, ''), '[^0-9]', '', 'g'), '');
begin
  if not is_staff(p_store) then raise exception '이 가게 직원만 웨이팅을 등록할 수 있습니다'; end if;
  select count(*) into v_ahead from waitlist where store_id = p_store and biz_date = biz_date(p_store) and status = 'wait';
  v_no := next_wait_no(p_store);
  insert into waitlist (id, store_id, biz_date, no, people, phone, src, priority, reservation_id, ahead_at_join)
  values (coalesce(p_id, gen_random_uuid()), p_store, biz_date(p_store), v_no, p_people, ph,
          case when p_reservation is not null then 'reservation' else 'staff' end, p_priority, p_reservation, v_ahead);
  return v_no;
end $$;
revoke execute on function staff_wait_add(uuid, uuid, int, text, boolean, uuid) from public, anon;
grant execute on function staff_wait_add(uuid, uuid, int, text, boolean, uuid) to authenticated, service_role;
