-- DineONE dev 더미 자료 (2026-11-12) — dineone-dev 전용. ★ 운영(dineone-prod)에는 절대 넣지 않습니다.
-- SQL Editor 에서 이 파일을 한 번 실행하면 dev_reseed() 함수가 생기고 바로 더미 가게를 만듭니다.
-- 그 뒤로는 언제든  select dev_reseed();  한 줄로 '오늘 기준' 더미를 새로 만듭니다(시안처럼 날짜가 지나면 다시).
--
-- · 가게: 짚불태백 광교점(slug zipbulgwanggyo) 하나. 설정은 시안 store.js 의 DEFAULT_CFG 와 같음
-- · 손님 번호는 모두 010-0000-xxxx (실제로 쓰지 않는 번호대) — 개발 DB 에 실제 손님 정보를 넣지 않는 원칙(구조 정리 5장)
-- · Authentication 에서 만든 '일반(비익명) 로그인 계정'은 모두 이 가게의 사장으로 묶음 (dev 에서만)
-- · 업무 기록(activity_log)은 더미를 만들며 생긴 줄을 지우고 깨끗하게 시작

create or replace function dev_reseed(p_slug text default 'zipbulgwanggyo') returns text
language plpgsql volatile security definer set search_path = public as $$
declare
  s        uuid;
  td       date;
  now_kst  timestamp := now() at time zone 'Asia/Seoul';
  now_m    int := extract(hour from now_kst)::int * 60 + extract(minute from now_kst)::int;
  fam      text[] := array['김','이','박','최','정','강','조','윤','장','임','한','오','서','신','권'];
  giv      text[] := array['민수','서연','지훈','하은','도윤','수빈','예준','지우','현우','유진','성민','은지','준호','다은','태현'];
  memo     text[] := array['','','','','유아용 의자 1개','생일 모임','회사 회식','창가 자리 희망','조용한 자리 부탁드려요','주차 2대'];
  lunch    text[] := array['11:30','12:00','12:00','12:30','13:00'];
  dinner   text[] := array['17:30','18:00','18:00','18:30','18:30','19:00','19:00','19:30','20:00'];
  i int; k int; n int; ppl int; past boolean; st text; src text; t text; d date; cid uuid; aid uuid; no int;
  seq int := 0;
  pm uuid[] := '{}';
begin
  if current_setting('request.jwt.claims', true) is not null and auth.uid() is not null then
    raise exception 'SQL Editor 에서만 실행합니다';
  end if;
  perform setseed(0.20261110);

  -- 가게 (없으면 만들고, 있으면 업무 자료를 비움 — dev 라서 지움)
  select id into s from stores where slug = p_slug;
  if s is null then
    insert into stores (slug, name, short_name, phone, address)
    values (p_slug, '짚불태백 광교점', '짚불태백', '0312320136', '경기 수원시 영통구 광교중앙로248번길 7, 1층')
    returning id into s;
  else
    delete from consents where store_id = s;      delete from point_tx where store_id = s;
    delete from reservations where store_id = s;  delete from waitlist where store_id = s;
    delete from wait_counters where store_id = s; delete from ledger_tx where store_id = s;
    delete from ledger_accounts where store_id = s; delete from customers where store_id = s;
    delete from day_closings where store_id = s;  delete from counter_pending where store_id = s;
    delete from store_tables where store_id = s;  delete from zones where store_id = s;
    delete from sms_messages where store_id = s;  delete from sms_credit_tx where store_id = s;
  end if;
  td := biz_date(s);

  insert into store_settings (store_id, cfg) values (s, '{
    "tables":20,"onlineTables":12,"seats":4,"dwellLunch":90,"dwellDinner":120,"maxDays":60,"groupConfirm":7,
    "lateMin":15,"noshowLimit":2,
    "slots":["11:30","12:00","12:30","13:00","13:30","14:00","17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30"],
    "waitMin":8,"callWaitMin":10,"bigTeam":7,"lastOrder":"21:00","waitCloseBefore":30,
    "lowBalance":100000,"ledgerCredit":0,
    "pointRate":5,"pointMin":5000,"pointExpireDays":365,"pointNextDay":true,"pointAuth":"name"}'::jsonb)
  on conflict (store_id) do update set cfg = excluded.cfg, updated_at = now();
  insert into store_features (store_id, feature, enabled)
    select s, f, true from unnest(array['reserve','wait','ledger','points','tv','sms']) f
  on conflict (store_id, feature) do update set enabled = true;

  -- 공간: 홀 하나, 테이블 20개(4인), 앞 12개가 온라인 예약용
  insert into zones (store_id, name) values (s, '홀');
  insert into store_tables (store_id, zone_id, name, seats, online, sort)
    select s, (select id from zones where store_id = s limit 1), g::text, 4, g <= 12, g from generate_series(1, 20) g;

  -- 사장: dev 에서 만든 일반 로그인 계정 모두
  insert into store_staff (store_id, user_id, role)
    select s, u.id, 'owner' from auth.users u
     where coalesce(u.is_anonymous, false) = false
       and not exists (select 1 from devices dv where dv.user_id = u.id)
  on conflict (store_id, user_id) do nothing;

  -- 예약: 어제 ~ 13일 뒤
  for i in -1 .. 13 loop
    d := td + i;
    n := case when extract(dow from d) in (5, 6, 0) then 13 else 8 end + floor(random() * 4)::int;
    for k in 1 .. n loop
      t   := case when random() < 0.28 then lunch[1 + floor(random() * 5)::int] else dinner[1 + floor(random() * 9)::int] end;
      ppl := case when random() < 0.12 then 8 + floor(random() * 5)::int else 2 + floor(random() * 5)::int end;
      past := i < 0 or (i = 0 and (split_part(t, ':', 1)::int * 60 + split_part(t, ':', 2)::int) + 20 < now_m);
      src := case when random() < 0.45 then 'web' when random() < 0.8 then 'phone' else 'walkin' end;
      st  := case when past then (case when random() < 0.08 then 'noshow' else 'seated' end) else 'ok' end;
      if not past and src = 'web' and ppl >= 7 and i <= 5 then st := 'req'; end if;
      if not past and random() < 0.05 then st := 'cancel'; end if;
      seq := seq + 1;
      insert into customers (store_id, phone, name)
        values (s, '0100000' || lpad((1000 + seq)::text, 4, '0'), fam[1 + floor(random() * 15)::int] || giv[1 + floor(random() * 15)::int])
        returning id into cid;
      insert into reservations (store_id, customer_id, visit_date, visit_time, people, status, src, memo, created_by, created_at)
        values (s, cid, d, t::time, ppl, st, src, nullif(memo[1 + floor(random() * 10)::int], ''), '더미', now() - (random() * interval '6 days'));
    end loop;
  end loop;
  -- 노쇼 두 번인 번호(홈페이지 예약 제한 예시)
  insert into customers (store_id, phone, name) values (s, '01000000490', '오현우') returning id into cid;
  insert into reservations (store_id, customer_id, visit_date, visit_time, people, status, src, created_by)
    values (s, cid, td - 9, '19:00', 4, 'noshow', 'web', '더미'), (s, cid, td - 23, '19:00', 4, 'noshow', 'web', '더미');

  -- 웨이팅: 오늘. 입장 간격 9분쯤 (예상 대기 계산 예시)
  no := 14;
  insert into waitlist (store_id, biz_date, no, people, phone, src, status, created_at, called_at, seated_at, ended_at)
  select s, td, x.wno, x.ppl, '0100000' || lpad((3000 + x.wno)::text, 4, '0'), x.wsrc, x.wst,
         now() - make_interval(mins => x.ago),
         case when x.wst = 'call' then now() - interval '3 minutes'
              when x.wst in ('in','gone','cancel') then now() - make_interval(mins => x.ago) + make_interval(mins => x.dur - 2) end,
         case when x.wst = 'in' then now() - make_interval(mins => x.ago) + make_interval(mins => x.dur) end,
         case when x.wst in ('in','gone','cancel') then now() - make_interval(mins => x.ago) + make_interval(mins => x.dur) end
    from (values (1,121,2,'in','entrance',21),(2,110,4,'in','entrance',19),(3,104,3,'gone','entrance',22),(4,103,6,'in','entrance',21),
                 (5,96,2,'in','entrance',23),(6,88,4,'cancel','entrance',9),(7,86,5,'in','staff',22),(8,76,2,'in','entrance',21),
                 (9,66,4,'in','entrance',20),(10,36,4,'call','entrance',0),(11,28,2,'wait','entrance',0),(12,21,6,'wait','entrance',0),
                 (13,13,3,'wait','staff',0),(14,6,4,'wait','entrance',0)) as x(wno, ago, ppl, wst, wsrc, dur);
  insert into wait_counters (store_id, biz_date, last_no) values (s, td, no)
    on conflict (store_id, biz_date) do update set last_no = excluded.last_no;

  -- 장부
  insert into ledger_accounts (store_id, name, kind, contact, phone, memo) values
    (s, '광교테크 총무팀', 'company', '박 과장', '01000004821', '회식 때 차감. 영수증은 담당자 메일로'),
    (s, '광교 미소치과', 'company', '김 원장', '01000009356', '직원 점심 · 저녁'),
    (s, '한빛세무회계', 'company', '이 실장', '01000002287', null),
    (s, '김민수 님', 'person', null, '01000007140', '단골 · 생갈비 미리 준비'),
    (s, '한결화재 광교지점', 'company', '최 팀장', '01000005512', '분기마다 충전');
  select id into aid from ledger_accounts where store_id = s and name = '광교테크 총무팀';
  insert into ledger_tx (store_id, account_id, type, amount, memo, by_name, created_by, created_at, voided_at) values
    (s, aid, 'charge', 1000000, '계좌이체', null, '더미', now() - interval '80 days', null),
    (s, aid, 'use', 186000, '팀 회식 8명', '박 과장', '더미', now() - interval '74 days', null),
    (s, aid, 'use', 243000, '송년회 1차 11명', '박 과장', '더미', now() - interval '51 days', null),
    (s, aid, 'use', 64000, '금액 잘못 입력', null, '더미', now() - interval '9 days', now() - interval '9 days'),
    (s, aid, 'use', 212000, '부서 회식 9명', '박 과장', '더미', now() - interval '9 days', null);
  select id into aid from ledger_accounts where store_id = s and name = '광교 미소치과';
  insert into ledger_tx (store_id, account_id, type, amount, memo, by_name, created_by, created_at) values
    (s, aid, 'charge', 500000, '카드', null, '더미', now() - interval '60 days'),
    (s, aid, 'use', 98000, '점심 5명', '김 원장', '더미', now() - interval '45 days'),
    (s, aid, 'use', 76000, '점심 특선 4명', '실장', '더미', now() - interval '3 days');
  select id into aid from ledger_accounts where store_id = s and name = '한빛세무회계';
  insert into ledger_tx (store_id, account_id, type, amount, memo, by_name, created_by, created_at) values
    (s, aid, 'charge', 300000, '계좌이체', null, '더미', now() - interval '40 days'),
    (s, aid, 'use', 87000, '4명', '이 실장', '더미', now() - interval '33 days'),
    (s, aid, 'use', 95000, '5명', '대표', '더미', now() - interval '2 days');
  select id into aid from ledger_accounts where store_id = s and name = '김민수 님';
  insert into ledger_tx (store_id, account_id, type, amount, memo, created_by, created_at) values
    (s, aid, 'charge', 200000, '현금', '더미', now() - interval '25 days'),
    (s, aid, 'use', 52000, '가족 3명', '더미', now() - interval '6 days');
  select id into aid from ledger_accounts where store_id = s and name = '한결화재 광교지점';
  insert into ledger_tx (store_id, account_id, type, amount, memo, by_name, created_by, created_at) values
    (s, aid, 'charge', 1000000, '계좌이체', null, '더미', now() - interval '20 days'),
    (s, aid, 'use', 268000, '지점 회식 12명', '최 팀장', '더미', now() - interval '5 hours');

  -- 포인트 회원 16명: 1년 넘은 적립도 섞어 유효기간이 보이게
  for k in 1 .. 16 loop
    insert into customers (store_id, phone, name, marketing)
      values (s, '0100000' || lpad((2100 + k)::text, 4, '0'),
              (array['김민수','박','이하은','최도윤','정','강예준','윤서아','임','한지민','오','서준우','신','권하린','조','장민재','황'])[k],
              random() < 0.4)
      returning id into cid;
    pm := pm || cid;
    insert into consents (store_id, customer_id, kind, version, agreed, via, at) values
      (s, cid, 'privacy', '2026-11-v1', true, '더미', now() - interval '420 days'),
      (s, cid, 'marketing', '2026-11-v1', (select marketing from customers where id = cid), '더미', now() - interval '420 days');
    for i in 1 .. (1 + floor(random() * 5)::int) loop
      insert into point_tx (store_id, customer_id, type, pts, pay_amount, src, created_by, created_at)
        select s, cid, 'earn', floor(a * 0.05)::int, a, case when random() < 0.7 then 'counter' else 'staff' end, '더미',
               now() - make_interval(days => 1 + floor(random() * 420)::int, hours => floor(random() * 9)::int)
          from (select (40 + floor(random() * 200)::int) * 1000 as a) z;
    end loop;
  end loop;
  -- 오늘 적립 — 마감 정산 예시(같은 번호 두 번 · 큰 금액)
  insert into point_tx (store_id, customer_id, type, pts, pay_amount, src, created_by, created_at) values
    (s, pm[3], 'earn', 4300, 86000, 'counter', '더미', least(now() - interval '1 minute', now() - interval '3 hours')),
    (s, pm[3], 'earn', 2600, 52000, 'counter', '더미', least(now() - interval '1 minute', now() - interval '2 hours')),
    (s, pm[9], 'earn', 24300, 486000, 'staff', '더미', least(now() - interval '1 minute', now() - interval '90 minutes'));
  update customers c set last_seen_at = coalesce((select max(created_at) from point_tx p where p.customer_id = c.id), c.created_at)
   where c.store_id = s;

  -- 더미를 만들며 생긴 업무 기록은 지우고 깨끗하게 시작
  delete from activity_log where store_id = s;
  return format('더미 완료: 예약 %s · 웨이팅 %s · 포인트 회원 16 · 장부 5 · 사장 계정 %s',
    (select count(*) from reservations where store_id = s), no,
    (select count(*) from store_staff where store_id = s and role = 'owner'));
end $$;

revoke execute on function dev_reseed(text) from public, anon, authenticated, service_role;

select dev_reseed();
