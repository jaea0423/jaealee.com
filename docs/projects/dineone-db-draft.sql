-- DineONE DB 설계 초안 v0 (2026-11-12)
-- ★ 아직 어디에도 적용하지 않은 초안입니다. 설명은 dineone-db.md 에 있습니다.
-- 실서비스 저장소(dineone)가 생기면 supabase/migrations/0001_init.sql 로 옮겨
-- dineone-dev 에 먼저 적용합니다. 운영(dineone-prod)에는 배포 승인과 함께만 들어갑니다(구조 정리 14장).
--
-- 지킬 것(구조 정리 5장)
--   · 모든 표에 store_id
--   · 칸은 더하기만 (지우기·이름 바꾸기 안 함)
--   · 돈·포인트·예약 기록은 지우지 않고 취소 표시(voided_at)
--   · 업무 기록(activity_log)은 트리거가 자동으로 남기고, 아무도 고치거나 지울 수 없음

------------------------------------------------------------------------------
-- 0. 가게 안의 '영업일' — 새벽 손님이 전날 영업으로 잡히게 (기본 05:00 경계)
------------------------------------------------------------------------------

create table stores (
  id          uuid primary key default gen_random_uuid(),
  slug        text not null unique check (slug ~ '^[a-z0-9][a-z0-9-]{1,30}$'),  -- 가게 영문 이름 (바꿀 수 있음)
  name        text not null,                                                -- 짚불태백 광교점
  short_name  text not null check (char_length(short_name) <= 8),           -- 문자 머리말 [짚불태백]
  phone       text,                                                         -- 가게 전화 (문자 끝에 붙임)
  address     text,
  status      text not null default 'pilot' check (status in ('pilot','active','paused','closed')),
  day_start   time not null default '05:00',
  created_at  timestamptz not null default now()
);

create table reserved_slugs (slug text primary key);
insert into reserved_slugs (slug) values
  ('www'),('partner'),('kiosk'),('admin'),('api'),('app'),('dev'),('test'),('mail'),('help'),('status');

create function check_slug() returns trigger language plpgsql as $$
begin
  if exists (select 1 from reserved_slugs where slug = new.slug) then
    raise exception '쓸 수 없는 가게 영문 이름입니다: %', new.slug;
  end if;
  return new;
end $$;
create trigger stores_slug before insert or update of slug on stores
  for each row execute function check_slug();

create function biz_date(p_store uuid, p_at timestamptz default now()) returns date
language sql stable as $$
  select ((p_at at time zone 'Asia/Seoul') - s.day_start)::date from stores s where s.id = p_store
$$;

-- 가게 주소: 서브도메인(짚불.dineone.co.kr)과 가게 자체 도메인
create table store_domains (
  host        text primary key check (host = lower(host)),
  store_id    uuid not null references stores(id),
  kind        text not null check (kind in ('sub','custom')),
  verified_at timestamptz,
  created_at  timestamptz not null default now()
);

-- 확인표 답 = 설정값. 시안의 DEFAULT_CFG 와 같은 이름을 씁니다(tables, dwellLunch, pointRate …)
create table store_settings (
  store_id    uuid primary key references stores(id),
  cfg         jsonb not null default '{}'::jsonb,
  updated_at  timestamptz not null default now()
);

-- 기능 켜고 끄기 (reserve, wait, remote_wait, ledger, points, tv, sms …)
create table store_features (
  store_id    uuid not null references stores(id),
  feature     text not null,
  enabled     boolean not null default false,
  primary key (store_id, feature)
);

------------------------------------------------------------------------------
-- 1. 사람과 권한 — 사람 × 가게 × 역할
------------------------------------------------------------------------------

create table profiles (
  user_id     uuid primary key references auth.users(id) on delete cascade,
  name        text,
  created_at  timestamptz not null default now()
);

create table store_staff (
  store_id    uuid not null references stores(id),
  user_id     uuid not null references auth.users(id),
  role        text not null check (role in ('owner','manager','staff')),
  created_at  timestamptz not null default now(),
  primary key (store_id, user_id)
);

-- 본사(와이비테크랩). readonly = 조사용 읽기 전용(구조 정리 14장)
create table platform_admins (
  user_id     uuid primary key references auth.users(id),
  role        text not null check (role in ('admin','readonly'))
);

------------------------------------------------------------------------------
-- 2. 매장 기기 — 직원 로그인 없이 '기기 등록 코드'로 가게에 묶음
--    기기마다 Supabase 익명 로그인 계정 하나(user_id). 등록 코드를 넣으면 이 표에 묶이고,
--    해제(revoked_at)하면 그 기기는 바로 아무것도 못 함.
------------------------------------------------------------------------------

create table devices (
  id            uuid primary key default gen_random_uuid(),
  store_id      uuid not null references stores(id),
  user_id       uuid unique references auth.users(id),
  kind          text not null check (kind in ('counter','entrance','points','combo','tv')),
  label         text not null,                 -- '카운터 아이패드', '입구 태블릿' (기록에 찍힘)
  wait_no_from  int,                           -- 끊겼을 때 이 기기가 쓸 웨이팅 번호 구간 (겹치지 않게)
  registered_at timestamptz not null default now(),
  last_seen_at  timestamptz,
  revoked_at    timestamptz
);

create table device_codes (
  code_hash   text primary key,                -- 코드 원문은 저장하지 않음
  store_id    uuid not null references stores(id),
  kind        text not null,
  label       text not null,
  expires_at  timestamptz not null,
  used_at     timestamptz,
  created_by  uuid references auth.users(id)
);

------------------------------------------------------------------------------
-- 3. 공간 — 가게 → 구역(홀·룸) → 테이블
------------------------------------------------------------------------------

create table zones (
  id        uuid primary key default gen_random_uuid(),
  store_id  uuid not null references stores(id),
  name      text not null,
  sort      int not null default 0
);

create table store_tables (
  id        uuid primary key default gen_random_uuid(),
  store_id  uuid not null references stores(id),
  zone_id   uuid references zones(id),
  name      text not null,                     -- 번호 또는 이름 (확인표 배치도)
  seats     int not null check (seats > 0),
  online    boolean not null default true,     -- 온라인 예약에 내놓는 테이블
  joins     uuid[] not null default '{}',      -- 붙일 수 있는 테이블
  sort      int not null default 0,
  active    boolean not null default true
);

------------------------------------------------------------------------------
-- 4. 손님 — 가게마다 따로 (가게끼리 손님을 공유하지 않음)
------------------------------------------------------------------------------

create table customers (
  id          uuid primary key default gen_random_uuid(),
  store_id    uuid not null references stores(id),
  phone       text not null check (phone ~ '^01[0-9]{8,9}$'),   -- 숫자만 01012345678
  name        text,                                             -- 성이나 별명도 됨
  memo        text,
  created_at  timestamptz not null default now(),
  unique (store_id, phone)
);

-- 개인정보·홍보 동의. 바뀔 때마다 한 줄 더함 (고치지 않음)
create table consents (
  id          bigint generated always as identity primary key,
  store_id    uuid not null references stores(id),
  customer_id uuid not null references customers(id),
  kind        text not null check (kind in ('privacy','marketing')),
  version     text not null,                   -- 동의 문구 버전 '2026-11-v1'
  agreed      boolean not null,
  via         text,                            -- 어느 화면·기기에서
  at          timestamptz not null default now()
);

------------------------------------------------------------------------------
-- 5. 예약
------------------------------------------------------------------------------

create table reservations (
  id          uuid primary key default gen_random_uuid(),
  store_id    uuid not null references stores(id),
  customer_id uuid not null references customers(id),
  visit_date  date not null,
  visit_time  time not null,
  people      int not null check (people between 1 and 200),
  zone_id     uuid references zones(id),
  table_ids   uuid[] not null default '{}',
  status      text not null default 'req'
              check (status in ('req','ok','seated','done','noshow','cancel')),
  src         text not null check (src in ('phone','web','walkin','staff','other')),
  memo        text,
  pre_order   text,
  created_by  text,                            -- 사람 이름 또는 기기 이름
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create index reservations_day on reservations (store_id, visit_date);
create index reservations_customer on reservations (store_id, customer_id);

------------------------------------------------------------------------------
-- 6. 웨이팅 — 입장 시각(seated_at)이 쌓여 예상 대기 시간을 계산 (구조 정리 11장)
------------------------------------------------------------------------------

create table waitlist (
  id                 uuid primary key default gen_random_uuid(),
  store_id           uuid not null references stores(id),
  biz_date           date not null,
  no                 int not null,
  people             int not null check (people between 1 and 200),
  customer_id        uuid references customers(id),
  phone              text check (phone ~ '^01[0-9]{8,9}$'),
  src                text not null check (src in ('entrance','remote','staff','reservation')),
  priority           boolean not null default false,   -- 예약 손님 자리 없음 → 맨 앞
  status             text not null default 'wait' check (status in ('wait','call','in','gone','cancel')),
  ahead_at_join      int,                              -- 접수 때 앞 팀 수
  free_tables_at_join int,                             -- 접수 때 빈 테이블 수
  created_at         timestamptz not null default now(),
  called_at          timestamptz,
  seated_at          timestamptz,
  ended_at           timestamptz,
  unique (store_id, biz_date, no)
);
create index waitlist_live on waitlist (store_id, biz_date, status);

create table wait_counters (
  store_id  uuid not null references stores(id),
  biz_date  date not null,
  last_no   int not null default 0,
  primary key (store_id, biz_date)
);

-- 오늘 다음 번호. 동시에 두 기기가 눌러도 겹치지 않음
create function next_wait_no(p_store uuid) returns int
language sql volatile security definer set search_path = public as $$
  insert into wait_counters (store_id, biz_date, last_no)
  values (p_store, biz_date(p_store), 1)
  on conflict (store_id, biz_date) do update set last_no = wait_counters.last_no + 1
  returning last_no
$$;

------------------------------------------------------------------------------
-- 7. 장부 (선결제) — 잔액보다 많이 써도 막지 않고 경고만 (credit_limit)
------------------------------------------------------------------------------

create table ledger_accounts (
  id           uuid primary key default gen_random_uuid(),
  store_id     uuid not null references stores(id),
  name         text not null,
  kind         text not null default 'company' check (kind in ('company','person')),
  contact      text,                            -- 담당자
  phone        text,
  memo         text,
  credit_limit int,                             -- 비우면 가게 설정 ledgerCredit 를 따름
  active       boolean not null default true,
  created_at   timestamptz not null default now()
);

create table ledger_tx (
  id          uuid primary key default gen_random_uuid(),
  store_id    uuid not null references stores(id),
  account_id  uuid not null references ledger_accounts(id),
  type        text not null check (type in ('charge','use')),
  amount      int not null check (amount > 0),
  memo        text,
  by_name     text,                             -- 쓴 사람 (말로 받은 이름)
  created_by  text,                             -- 화면·기기
  created_at  timestamptz not null default now(),
  voided_at   timestamptz,
  voided_by   text,
  void_reason text
);
create index ledger_tx_account on ledger_tx (store_id, account_id, created_at);

create view ledger_balances with (security_invoker = true) as
  select a.store_id, a.id as account_id, a.name,
         coalesce(sum(case when t.type = 'charge' then t.amount else -t.amount end)
                  filter (where t.voided_at is null), 0)::int as balance
  from ledger_accounts a left join ledger_tx t on t.account_id = a.id
  group by a.store_id, a.id, a.name;

------------------------------------------------------------------------------
-- 8. 포인트 — 적립은 '묶음'으로 보고 먼저 쌓인 것부터 씀(FIFO), 유효기간 지나면 소멸
------------------------------------------------------------------------------

create table point_tx (
  id          uuid primary key default gen_random_uuid(),
  store_id    uuid not null references stores(id),
  customer_id uuid not null references customers(id),
  type        text not null check (type in ('earn','use','adjust_add','adjust_sub')),
  pts         int not null check (pts > 0),
  pay_amount  int,                              -- 적립 기준 결제 금액
  src         text check (src in ('counter','staff','receipt','pos','system')),  -- 들어온 방식 (구조 정리 8장)
  verify      text check (verify in ('name','code','manual')),                  -- 사용 때 본인 확인 방식
  created_by  text,
  created_at  timestamptz not null default now(),
  voided_at   timestamptz,
  voided_by   text,
  void_reason text
);
create index point_tx_customer on point_tx (store_id, customer_id, created_at);

-- 시안 store.js 의 pstate() 와 같은 계산
create function point_state(p_customer uuid, p_now timestamptz default now())
returns table (total int, usable int, today int, soon int, expired int, next_expire timestamptz)
language plpgsql stable as $$
declare
  c        jsonb;
  life     interval;
  next_day boolean;
  t0       timestamptz;
  lot_at   timestamptz[] := '{}';
  lot_left int[] := '{}';
  r        record;
  need     int;
  k        int;
  i        int;
  v_store  uuid;
begin
  select cu.store_id into v_store from customers cu where cu.id = p_customer;
  select coalesce(ss.cfg, '{}'::jsonb) into c from store_settings ss where ss.store_id = v_store;
  c := coalesce(c, '{}'::jsonb);
  life     := make_interval(days => coalesce((c->>'pointExpireDays')::int, 365));
  next_day := coalesce((c->>'pointNextDay')::boolean, true);
  t0       := (biz_date(v_store, p_now)::timestamp + (select day_start from stores where id = v_store)) at time zone 'Asia/Seoul';
  expired  := 0;

  for r in select * from point_tx
           where customer_id = p_customer and voided_at is null and created_at <= p_now
           order by created_at loop
    -- 이 기록 시점까지 기한이 지난 묶음은 소멸
    for i in 1 .. coalesce(array_length(lot_at, 1), 0) loop
      if lot_left[i] > 0 and lot_at[i] + life <= r.created_at then
        expired := expired + lot_left[i]; lot_left[i] := 0;
      end if;
    end loop;
    if r.type in ('earn','adjust_add') then
      lot_at := lot_at || r.created_at; lot_left := lot_left || r.pts;
    else
      need := r.pts;
      for i in 1 .. coalesce(array_length(lot_at, 1), 0) loop
        exit when need = 0;
        k := least(lot_left[i], need); lot_left[i] := lot_left[i] - k; need := need - k;
      end loop;
    end if;
  end loop;

  total := 0; today := 0; soon := 0; next_expire := null;
  for i in 1 .. coalesce(array_length(lot_at, 1), 0) loop
    if lot_left[i] > 0 and lot_at[i] + life <= p_now then
      expired := expired + lot_left[i]; lot_left[i] := 0;
    end if;
    if lot_left[i] > 0 then
      total := total + lot_left[i];
      if next_day and lot_at[i] >= t0 then today := today + lot_left[i]; end if;
      if lot_at[i] + life - p_now < interval '30 days' then soon := soon + lot_left[i]; end if;
      if next_expire is null then next_expire := lot_at[i] + life; end if;
    end if;
  end loop;
  usable := total - today;
  return next;
end $$;

------------------------------------------------------------------------------
-- 9. 마감 — 그날 포스 매출과 나란히 비교
------------------------------------------------------------------------------

create table day_closings (
  store_id   uuid not null references stores(id),
  biz_date   date not null,
  pos_total  int,
  note       text,
  closed_at  timestamptz,
  closed_by  text,
  primary key (store_id, biz_date)
);

------------------------------------------------------------------------------
-- 10. 문자와 크레딧 — 단문 1, 장문 2 크레딧. 실제 발송은 서버(Edge Function)만
------------------------------------------------------------------------------

create table sms_messages (
  id           uuid primary key default gen_random_uuid(),
  store_id     uuid not null references stores(id),
  kind         text not null check (kind in
               ('res_confirm','res_change','res_remind','wait_join','wait_call','point_earn','ledger_use','promo','other')),
  to_phone     text not null check (to_phone ~ '^01[0-9]{8,9}$'),
  body         text not null,
  bytes        int not null,                    -- EUC-KR 기준. 90 이하 단문
  msg_type     text not null check (msg_type in ('sms','lms')),
  credits      int not null check (credits > 0),
  emergency    boolean not null default false,  -- 비상 크레딧으로 보낸 웨이팅 호출
  status       text not null default 'queued' check (status in ('queued','sent','failed')),
  provider     text,                            -- aligo / solapi
  provider_id  text,
  cost_won     numeric(8,2),                    -- 실제 원가 (청구·이익 계산용)
  error        text,
  created_at   timestamptz not null default now(),
  sent_at      timestamptz
);
create index sms_messages_store on sms_messages (store_id, created_at);

-- 크레딧 통장: 더하기(+)·빼기(−)를 한 줄씩. 잔액 = 합계
create table sms_credit_tx (
  id          bigint generated always as identity primary key,
  store_id    uuid not null references stores(id),
  type        text not null check (type in
              ('monthly','purchase','auto_charge','use','refund','emergency_use','emergency_settle','expire','adjust')),
  credits     int not null check (credits <> 0),
  bucket      text not null default 'monthly' check (bucket in ('monthly','purchased','emergency')),
  message_id  uuid references sms_messages(id),
  payment_id  uuid,
  memo        text,
  created_at  timestamptz not null default now()
);
create index sms_credit_tx_store on sms_credit_tx (store_id, created_at);

create view sms_wallets with (security_invoker = true) as
  select store_id,
         coalesce(sum(credits) filter (where bucket in ('monthly','purchased')), 0)::int as credits,
         coalesce(sum(credits) filter (where bucket = 'emergency'), 0)::int as emergency_used
  from sms_credit_tx group by store_id;

------------------------------------------------------------------------------
-- 11. 이용료와 결제 — 카드번호는 저장하지 않음. PG(토스페이먼츠 등)가 준 열쇠 이름만
------------------------------------------------------------------------------

create table subscriptions (
  store_id          uuid primary key references stores(id),
  plan              text not null default 'basic',
  monthly_price     int not null,               -- VAT 별도 (정가 59,000)
  partner_price     int,                        -- 파트너가 (39,000)
  partner_until     date,
  monthly_credits   int not null default 500,
  auto_charge       boolean not null default true,
  auto_charge_below int not null default 100,   -- 남은 크레딧이 이 아래면
  auto_charge_pack  int not null default 1000,  -- 이만큼 충전
  auto_charge_cap   int not null default 2,     -- 한 달 자동 충전 최대 횟수
  emergency_credits int not null default 30,    -- 웨이팅 호출 전용
  pg_billing_ref    text,                       -- PG 정기결제 열쇠의 이름(빌링키 자체는 비밀값 보관소)
  status            text not null default 'trial' check (status in ('trial','active','past_due','paused','ended')),
  started_at        date,
  updated_at        timestamptz not null default now()
);

create table payments (
  id          uuid primary key default gen_random_uuid(),
  store_id    uuid not null references stores(id),
  kind        text not null check (kind in ('subscription','credit_pack','auto_charge')),
  amount      int not null,                     -- 공급가
  vat         int not null,
  status      text not null default 'pending' check (status in ('pending','paid','failed','refunded')),
  pg_tx_ref   text,
  memo        text,
  created_at  timestamptz not null default now(),
  paid_at     timestamptz
);

------------------------------------------------------------------------------
-- 12. 업무 기록 — 트리거가 자동으로. 더하기만 됨
------------------------------------------------------------------------------

create table activity_log (
  id          bigint generated always as identity primary key,
  store_id    uuid,
  at          timestamptz not null default now(),
  actor_kind  text not null check (actor_kind in ('staff','device','admin','system')),
  actor_id    uuid,
  actor_label text,                             -- '카운터 아이패드', '홍길동(사장)'
  entity      text not null,                    -- 표 이름
  entity_id   text,
  action      text not null check (action in ('insert','update','delete')),
  before      jsonb,
  after       jsonb
);
create index activity_log_store on activity_log (store_id, at desc);

-- 기록 속 전화번호 가리기 01012341201 → 010****1201
create function mask_phones(j jsonb) returns jsonb language sql immutable as $$
  select case when j is null then null else
    regexp_replace(j::text, '"(01[0-9])([0-9]{3,4})([0-9]{4})"', '"\1****\3"', 'g')::jsonb end
$$;

create function log_change() returns trigger
language plpgsql security definer set search_path = public as $$
declare
  v_uid   uuid := auth.uid();
  v_kind  text := 'system';
  v_label text;
  v_store uuid;
  v_id    text;
begin
  -- 기기가 살아 있다는 신호(last_seen_at)만 바뀐 것은 기록하지 않음
  if tg_table_name = 'devices' and tg_op = 'UPDATE'
     and (to_jsonb(new) - 'last_seen_at') = (to_jsonb(old) - 'last_seen_at') then
    return new;
  end if;
  if v_uid is not null then
    select 'device', d.label into v_kind, v_label from devices d where d.user_id = v_uid;
    if v_kind = 'system' or v_kind is null then
      if exists (select 1 from platform_admins where user_id = v_uid) then v_kind := 'admin';
      else v_kind := 'staff'; end if;
      select coalesce(p.name, '') into v_label from profiles p where p.user_id = v_uid;
    end if;
  end if;
  if tg_op = 'DELETE' then
    v_store := old.store_id; v_id := to_jsonb(old)->>'id';
  else
    v_store := new.store_id; v_id := to_jsonb(new)->>'id';
  end if;
  insert into activity_log (store_id, actor_kind, actor_id, actor_label, entity, entity_id, action, before, after)
  values (v_store, v_kind, v_uid, v_label, tg_table_name, v_id, lower(tg_op),
          case when tg_op <> 'INSERT' then mask_phones(to_jsonb(old)) end,
          case when tg_op <> 'DELETE' then mask_phones(to_jsonb(new)) end);
  return coalesce(new, old);
end $$;

do $$
declare t text;
begin
  foreach t in array array['store_settings','store_features','store_staff','devices','zones','store_tables',
                           'customers','consents','reservations','waitlist','ledger_accounts','ledger_tx',
                           'point_tx','day_closings','subscriptions','payments'] loop
    execute format('create trigger %I_log after insert or update or delete on %I
                    for each row execute function log_change()', t, t);
  end loop;
end $$;

------------------------------------------------------------------------------
-- 13. 권한(RLS) — 가게 직원은 자기 가게만, 기기는 정해진 함수로만, 손님 화면은 서버를 거쳐서만
------------------------------------------------------------------------------

create function staff_role(p_store uuid) returns text
language sql stable security definer set search_path = public as $$
  select role from store_staff where store_id = p_store and user_id = auth.uid()
$$;

create function is_staff(p_store uuid, p_roles text[] default array['owner','manager','staff']) returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce(staff_role(p_store) = any (p_roles), false)
$$;

create function is_admin(p_write boolean default false) returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from platform_admins
                 where user_id = auth.uid() and (not p_write or role = 'admin'))
$$;

create function device_store() returns uuid
language sql stable security definer set search_path = public as $$
  select store_id from devices where user_id = auth.uid() and revoked_at is null
$$;

-- 모든 표에 RLS 켜기 (정책이 없으면 아무도 못 읽음)
do $$
declare t text;
begin
  foreach t in array array['stores','reserved_slugs','store_domains','store_settings','store_features','profiles',
                           'store_staff','platform_admins','devices','device_codes','zones','store_tables',
                           'customers','consents','reservations','waitlist','wait_counters','ledger_accounts',
                           'ledger_tx','point_tx','day_closings','sms_messages','sms_credit_tx',
                           'subscriptions','payments','activity_log'] loop
    execute format('alter table %I enable row level security', t);
  end loop;
end $$;

-- 업무 표: 직원은 읽기·쓰기·고치기(취소 표시 포함), 지우기 정책은 두지 않음 → 지울 수 없음
do $$
declare t text;
begin
  foreach t in array array['zones','store_tables','customers','consents','reservations','waitlist',
                           'ledger_accounts','ledger_tx','point_tx','day_closings'] loop
    execute format('create policy %I on %I for select using (is_staff(store_id) or is_admin())', t || '_read', t);
    execute format('create policy %I on %I for insert with check (is_staff(store_id))', t || '_add', t);
    execute format('create policy %I on %I for update using (is_staff(store_id)) with check (is_staff(store_id))', t || '_edit', t);
  end loop;
end $$;
-- 동의 기록은 고치지 않음 (새 줄로만)
drop policy consents_edit on consents;

create policy stores_read   on stores for select using (is_staff(id) or device_store() = id or is_admin());
create policy stores_edit   on stores for update using (is_staff(id, array['owner'])) with check (is_staff(id, array['owner']));
create policy domains_read  on store_domains for select using (is_staff(store_id) or is_admin());

create policy settings_read on store_settings for select using (is_staff(store_id) or device_store() = store_id or is_admin());
create policy settings_edit on store_settings for update
  using (is_staff(store_id, array['owner','manager'])) with check (is_staff(store_id, array['owner','manager']));
create policy features_read on store_features for select using (is_staff(store_id) or device_store() = store_id or is_admin());

create policy profiles_self on profiles for all using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy staff_read    on store_staff for select using (is_staff(store_id) or is_admin());
create policy staff_owner   on store_staff for insert with check (is_staff(store_id, array['owner']));
create policy devices_read  on devices for select using (is_staff(store_id) or user_id = auth.uid() or is_admin());
create policy devices_edit  on devices for update
  using (is_staff(store_id, array['owner','manager'])) with check (is_staff(store_id, array['owner','manager']));

-- 업무 기록·문자·이용료: 사장·매니저만 읽기. 쓰기는 트리거와 서버만
create policy log_read      on activity_log for select using (is_staff(store_id, array['owner','manager']) or is_admin());
create policy sms_read      on sms_messages for select using (is_staff(store_id, array['owner','manager']) or is_admin());
create policy credits_read  on sms_credit_tx for select using (is_staff(store_id, array['owner','manager']) or is_admin());
create policy subs_read     on subscriptions for select using (is_staff(store_id, array['owner']) or is_admin());
create policy pay_read      on payments for select using (is_staff(store_id, array['owner']) or is_admin());

-- 기록은 누구도 고치거나 지울 수 없음 (본사 포함). 서버 열쇠(service_role)도 권한을 뺌
revoke update, delete, truncate on activity_log from anon, authenticated, service_role;
revoke truncate on all tables in schema public from anon, authenticated;

------------------------------------------------------------------------------
-- 14. 매장 기기 전용 함수 — 기기는 표를 직접 읽지 않고 이 함수만 부름
--     (적립 태블릿이 손님 전화번호 목록 전체를 받아 갈 수 없게)
------------------------------------------------------------------------------

-- 입구·겸용 태블릿: 웨이팅 접수
create function kiosk_wait_join(p_people int, p_phone text) returns table (no int, ahead int)
language plpgsql volatile security definer set search_path = public as $$
declare
  s uuid := device_store();
  v_no int;
  v_ahead int;
  v_label text;
begin
  if s is null then raise exception '등록되지 않은 기기입니다'; end if;
  select label into v_label from devices where user_id = auth.uid();
  select count(*) into v_ahead from waitlist w
    where w.store_id = s and w.biz_date = biz_date(s) and w.status = 'wait';
  v_no := next_wait_no(s);
  insert into waitlist (store_id, biz_date, no, people, phone, src, ahead_at_join)
  values (s, biz_date(s), v_no, p_people, regexp_replace(p_phone, '[^0-9]', '', 'g'), 'entrance', v_ahead);
  update devices set last_seen_at = now() where user_id = auth.uid();
  no := v_no; ahead := v_ahead; return next;
end $$;

-- 계산대·겸용 태블릿: 적립 (처음이면 이름을 받아 회원 만들기)
create function kiosk_earn(p_phone text, p_amount int, p_name text default null)
returns table (pts int, is_new boolean, usable int, total int)
language plpgsql volatile security definer set search_path = public as $$
declare
  s     uuid := device_store();
  ph    text := regexp_replace(p_phone, '[^0-9]', '', 'g');
  c     jsonb;
  cid   uuid;
  v_pts int;
  st    record;
begin
  if s is null then raise exception '등록되지 않은 기기입니다'; end if;
  if p_amount is null or p_amount <= 0 then raise exception '결제 금액을 확인해 주세요'; end if;
  select coalesce(cfg, '{}'::jsonb) into c from store_settings where store_id = s;
  c := coalesce(c, '{}'::jsonb);
  if p_amount < coalesce((c->>'pointMin')::int, 0) then raise exception '적립 최소 금액보다 적습니다'; end if;
  select id into cid from customers where store_id = s and phone = ph;
  is_new := cid is null;
  if is_new then
    insert into customers (store_id, phone, name) values (s, ph, nullif(trim(p_name), '')) returning id into cid;
  end if;
  v_pts := floor(p_amount * coalesce((c->>'pointRate')::numeric, 5) / 100);
  insert into point_tx (store_id, customer_id, type, pts, pay_amount, src, created_by)
  values (s, cid, 'earn', v_pts, p_amount, 'counter', (select label from devices where user_id = auth.uid()));
  update devices set last_seen_at = now() where user_id = auth.uid();
  select * into st from point_state(cid);
  pts := v_pts; usable := st.usable; total := st.total; return next;
end $$;

-- 매장 TV: 부르는 번호·대기·곧 오는 예약 (이름 가리고 전화번호 없음)
create function tv_board() returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare
  s uuid := device_store();
  d date;
begin
  if s is null then raise exception '등록되지 않은 기기입니다'; end if;
  d := biz_date(s);
  return jsonb_build_object(
    'calls',   (select coalesce(jsonb_agg(no order by called_at), '[]') from waitlist
                where store_id = s and biz_date = d and status = 'call'),
    'waiting', (select count(*) from waitlist where store_id = s and biz_date = d and status = 'wait'),
    'soon',    (select coalesce(jsonb_agg(jsonb_build_object(
                  'time', to_char(r.visit_time, 'HH24:MI'),
                  'name', case when char_length(cu.name) <= 1 then cu.name
                               when char_length(cu.name) = 2 then left(cu.name, 1) || '*'
                               else left(cu.name, 1) || repeat('*', char_length(cu.name) - 2) || right(cu.name, 1) end,
                  'people', r.people) order by r.visit_time), '[]')
                from reservations r join customers cu on cu.id = r.customer_id
                where r.store_id = s and r.visit_date = d and r.status in ('req','ok')
                  and r.visit_time >= (now() at time zone 'Asia/Seoul')::time - interval '15 minutes')
  );
end $$;

-- 기기 함수는 로그인한(익명 포함) 기기만, 손님 화면(anon)은 못 부름
revoke execute on all functions in schema public from public, anon;
grant execute on function kiosk_wait_join(int, text), kiosk_earn(text, int, text), tv_board(),
                          point_state(uuid, timestamptz), biz_date(uuid, timestamptz),
                          is_staff(uuid, text[]), staff_role(uuid), is_admin(boolean), device_store()
  to authenticated;
-- 다음 번호 함수는 서버·기기 함수 안에서만 씀
revoke execute on function next_wait_no(uuid) from authenticated;
