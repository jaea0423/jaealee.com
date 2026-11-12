-- DineONE DB 검사 (dineone-dev 전용)
-- Supabase 대시보드 → SQL Editor 에 이 파일 전체를 붙여 넣고 Run.
-- 맨 아래에 '검사 이름 · 통과 여부 · 결과' 표가 나옵니다. 모두 ok = true 여야 합니다.
-- 검사용 가게·사람·기기를 잠깐 만들었다가 끝에서 모두 지웁니다(실제 자료는 건드리지 않음).
-- ★ 운영(dineone-prod)에서는 돌리지 않습니다.

create temp table _r (n serial, name text, ok boolean, result text);
grant all on _r to authenticated, anon;
grant usage on sequence _r_n_seq to authenticated, anon;

-- 검사용 자료 (아이디는 dddd… 로 시작해 실제 자료와 겹치지 않음)
insert into auth.users (id, email, aud, role) values
  ('dddddddd-0000-0000-0000-000000000001', 'check-owner@example.invalid', 'authenticated', 'authenticated'),
  ('dddddddd-0000-0000-0000-000000000002', 'check-other@example.invalid', 'authenticated', 'authenticated'),
  ('dddddddd-0000-0000-0000-000000000003', 'check-device@example.invalid', 'authenticated', 'authenticated');
insert into stores (id, slug, name, short_name, phone) values
  ('dddddddd-1111-0000-0000-000000000001', 'zz-check-a', '검사가게A', '검사A', '0310000000'),
  ('dddddddd-1111-0000-0000-000000000002', 'zz-check-b', '검사가게B', '검사B', '0310000001');
insert into store_settings (store_id, cfg) values
  ('dddddddd-1111-0000-0000-000000000001', '{"pointRate":5,"pointMin":5000,"pointExpireDays":365,"pointNextDay":true}');
insert into store_staff (store_id, user_id, role) values
  ('dddddddd-1111-0000-0000-000000000001', 'dddddddd-0000-0000-0000-000000000001', 'owner'),
  ('dddddddd-1111-0000-0000-000000000002', 'dddddddd-0000-0000-0000-000000000002', 'owner');
insert into profiles (user_id, name) values ('dddddddd-0000-0000-0000-000000000001', '검사사장');
insert into devices (store_id, user_id, kind, label) values
  ('dddddddd-1111-0000-0000-000000000001', 'dddddddd-0000-0000-0000-000000000003', 'combo', '검사 태블릿');

-- 0. 예약어 가게 이름
do $$ begin
  begin insert into stores (slug, name, short_name) values ('admin', 'x', 'x');
        insert into _r (name, ok, result) values ('가게 영문 이름 admin 막힘', false, '들어감');
  exception when others then insert into _r (name, ok, result) values ('가게 영문 이름 admin 막힘', true, sqlerrm); end;
end $$;

-- 1. 매장 기기로 일하기
do $$ declare v text; e text; begin
  perform set_config('request.jwt.claims', '{"sub":"dddddddd-0000-0000-0000-000000000003","role":"authenticated"}', false);
  execute 'set role authenticated';
  begin perform kiosk_earn('010-9999-0000', 50000, '동의안함'); e := null; exception when others then e := sqlerrm; end;
  insert into _r (name, ok, result) values ('새 회원 동의 없이 적립 막힘', e is not null, coalesce(e, '가입됨'));
  select to_jsonb(k)::text into v from kiosk_earn('010-1234-1201', 86000, '김민수', true, true) k;
  insert into _r (name, ok, result) values ('기기 적립 86,000원 → 4,300', v like '%"pts": 4300%', v);
  begin perform kiosk_earn('01012341201', 3000); e := null; exception when others then e := sqlerrm; end;
  insert into _r (name, ok, result) values ('최소 금액 미만 막힘', e is not null, coalesce(e, '적립됨'));
  select to_jsonb(k)::text into v from kiosk_wait_join(4, '010-5555-0001') k;
  insert into _r (name, ok, result) values ('웨이팅 1번', v like '%"no": 1%', v);
  select to_jsonb(k)::text into v from kiosk_wait_join(2, '010-5555-0002') k;
  insert into _r (name, ok, result) values ('웨이팅 2번(앞 1팀)', v like '%"ahead": 1%', v);
  select count(*)::text into v from customers;
  insert into _r (name, ok, result) values ('기기는 손님 표를 직접 못 읽음', v = '0', v || '명');
  execute 'reset role';
end $$;

-- 2. 사장·다른 가게 사장
do $$ declare v text; e text; begin
  perform set_config('request.jwt.claims', '{"sub":"dddddddd-0000-0000-0000-000000000001","role":"authenticated"}', false);
  execute 'set role authenticated';
  select count(*)::text into v from customers;
  insert into _r (name, ok, result) values ('사장은 자기 가게 손님 1명', v = '1', v || '명');
  insert into reservations (store_id, customer_id, visit_date, visit_time, people, status, src)
    select store_id, id, biz_date(store_id), ((now() at time zone 'Asia/Seoul') + interval '1 hour')::time, 4, 'ok', 'phone' from customers;
  update waitlist set status = 'call', called_at = now() where no = 1;
  begin update activity_log set actor_label = 'x'; e := null; exception when others then e := sqlerrm; end;
  insert into _r (name, ok, result) values ('업무 기록 고치기 막힘', e is not null, coalesce(e, '고쳐짐'));
  begin delete from point_tx; e := null; exception when others then e := sqlerrm; end;
  insert into _r (name, ok, result) values ('포인트 기록 지우기 막힘', e is not null, coalesce(e, '지워짐'));
  begin update consents set agreed = true; e := null; exception when others then e := sqlerrm; end;
  insert into _r (name, ok, result) values ('동의 기록 고치기 막힘', e is not null, coalesce(e, '고쳐짐'));
  begin perform purge_personal_data(); e := null; exception when others then e := sqlerrm; end;
  insert into _r (name, ok, result) values ('사장도 지우기 함수 못 부름', e is not null, coalesce(e, '불림'));
  select (usable::text || '/' || total::text) into v from point_state((select id from customers limit 1));
  insert into _r (name, ok, result) values ('오늘 적립은 내일부터(쓸 수 있는/전체)', v = '0/4300', v);
  select (usable::text || '/' || total::text) into v from point_state((select id from customers limit 1), now() + interval '2 days');
  insert into _r (name, ok, result) values ('이틀 뒤 쓸 수 있음', v = '4300/4300', v);
  select (expired::text) into v from point_state((select id from customers limit 1), now() + interval '400 days');
  insert into _r (name, ok, result) values ('400일 뒤 소멸', v = '4300', v);
  select count(*)::text into v from activity_log where actor_label = '검사 태블릿' and after::text like '%010****1201%';
  insert into _r (name, ok, result) values ('업무 기록에 기기 이름·가린 번호', v::int > 0, v || '줄');
  execute 'reset role';

  perform set_config('request.jwt.claims', '{"sub":"dddddddd-0000-0000-0000-000000000002","role":"authenticated"}', false);
  execute 'set role authenticated';
  select count(*)::text into v from customers;
  insert into _r (name, ok, result) values ('다른 가게 사장은 손님 0명', v = '0', v || '명');
  select count(*)::text into v from activity_log where store_id = 'dddddddd-1111-0000-0000-000000000001';
  insert into _r (name, ok, result) values ('다른 가게 업무 기록 안 보임', v = '0', v || '줄');
  execute 'reset role';
end $$;

-- 3. 매장 TV
do $$ declare v text; begin
  perform set_config('request.jwt.claims', '{"sub":"dddddddd-0000-0000-0000-000000000003","role":"authenticated"}', false);
  execute 'set role authenticated';
  select tv_board()::text into v;
  insert into _r (name, ok, result) values ('TV: 호출 1번, 이름 가림', v like '%"calls": [1]%' and v like '%김*수%' and v not like '%1201%', v);
  execute 'reset role';
end $$;

-- 4. 손님 브라우저(anon)
do $$ declare e text; begin
  perform set_config('request.jwt.claims', '{"role":"anon"}', false);
  execute 'set role anon';
  begin perform count(*) from customers; e := null; exception when others then e := sqlerrm; end;
  insert into _r (name, ok, result) values ('손님 브라우저는 표에 권한 없음', e is not null, coalesce(e, '읽힘'));
  begin perform tv_board(); e := null; exception when others then e := sqlerrm; end;
  insert into _r (name, ok, result) values ('손님 브라우저는 기기 함수 못 부름', e is not null, coalesce(e, '불림'));
  begin perform purge_personal_data(); e := null; exception when others then e := sqlerrm; end;
  insert into _r (name, ok, result) values ('손님 브라우저는 지우기 함수 못 부름', e is not null, coalesce(e, '불림'));
  execute 'reset role';
end $$;

-- 5. 보관 기간 지우기 (서버 권한으로)
do $$ declare v text; begin
  insert into sms_messages (store_id, kind, to_phone, body, bytes, msg_type, credits, created_at)
    values ('dddddddd-1111-0000-0000-000000000001', 'point_earn', '01012341201', '본문', 60, 'sms', 1, now() - interval '7 months');
  perform purge_personal_data(now() + interval '1 day');
  select count(*)::text into v from waitlist where store_id = 'dddddddd-1111-0000-0000-000000000001' and phone is not null;
  insert into _r (name, ok, result) values ('하루 뒤 웨이팅 번호 지워짐', v = '0', v || '건 남음');
  select to_phone into v from sms_messages where store_id = 'dddddddd-1111-0000-0000-000000000001';
  insert into _r (name, ok, result) values ('6개월 지난 문자 번호 가림', v = '010****1201', v);
  perform purge_personal_data(now() + interval '3 years 1 day');
  select coalesce(phone, '(비움)') into v from customers where store_id = 'dddddddd-1111-0000-0000-000000000001';
  insert into _r (name, ok, result) values ('3년 뒤 손님 번호 비움', v = '(비움)', v);
  select count(*)::text into v from point_tx where store_id = 'dddddddd-1111-0000-0000-000000000001';
  insert into _r (name, ok, result) values ('포인트 내역은 남음', v = '1', v || '건');
end $$;

-- 6. RLS 가 꺼진 표가 없는지
insert into _r (name, ok, result)
  select 'RLS 꺼진 표 없음', count(*) = 0, coalesce(string_agg(c.relname, ', '), '없음')
  from pg_class c join pg_namespace n on n.oid = c.relnamespace
  where n.nspname = 'public' and c.relkind = 'r' and not c.relrowsecurity;

-- 검사용 자료 지우기
delete from sms_messages   where store_id::text like 'dddddddd%';
delete from consents       where store_id::text like 'dddddddd%';
delete from point_tx       where store_id::text like 'dddddddd%';
delete from reservations   where store_id::text like 'dddddddd%';
delete from waitlist       where store_id::text like 'dddddddd%';
delete from wait_counters  where store_id::text like 'dddddddd%';
delete from customers      where store_id::text like 'dddddddd%';
delete from devices        where store_id::text like 'dddddddd%';
delete from store_staff    where store_id::text like 'dddddddd%';
delete from store_settings where store_id::text like 'dddddddd%';
delete from profiles       where user_id::text like 'dddddddd%';
delete from activity_log   where store_id::text like 'dddddddd%' or actor_id::text like 'dddddddd%';
delete from stores         where id::text like 'dddddddd%';
delete from auth.users     where id::text like 'dddddddd%';

select n as "번호", name as "검사", ok as "통과", result as "결과" from _r order by n;
