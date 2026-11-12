-- DineONE DB 변경 0002 (2026-11-12) — 매장 기기 등록, 계산대 금액 넘기기, 기기용 조회 함수
-- 0001 = dineone-db-draft.sql (dev 적용 완료). 이 파일은 그 위에 더하는 변경입니다. dev 에 한 번만 실행.
-- 실서비스 저장소가 생기면 supabase/migrations/0002_devices.sql 로 옮깁니다.

------------------------------------------------------------------------------
-- 1. 계산대 금액 넘기기 — 직원이 결제 금액을 보내면 계산대 태블릿에 뜨고, 손님이 번호를 눌러 적립
--    가게마다 한 줄(한 번에 하나). 적립되면 지워짐
------------------------------------------------------------------------------

create table counter_pending (
  store_id   uuid primary key references stores(id),
  amount     int not null check (amount > 0),
  created_by text,
  at         timestamptz not null default now()
);
alter table counter_pending enable row level security;
create policy pending_staff on counter_pending for all using (is_staff(store_id)) with check (is_staff(store_id));
grant select, insert, update, delete on counter_pending to authenticated;
grant all on counter_pending to service_role;

------------------------------------------------------------------------------
-- 2. 기기 등록 — 사장·매니저가 코드를 만들고, 기기(익명 로그인)가 코드를 넣으면 가게에 묶임
--    코드는 10자리(영문 대문자+숫자, 헷갈리는 0·O·1·I 빼고). 30분 안에 한 번만 쓸 수 있음
------------------------------------------------------------------------------

create function make_device_code(p_store uuid, p_kind text, p_label text) returns text
language plpgsql volatile security definer set search_path = public as $$
declare
  abc  text := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  code text := '';
  i    int;
begin
  if not is_staff(p_store, array['owner','manager']) then raise exception '사장·매니저만 기기 코드를 만들 수 있습니다'; end if;
  if p_kind not in ('counter','entrance','points','combo','tv') then raise exception '기기 종류를 확인해 주세요'; end if;
  for i in 1 .. 10 loop
    code := code || substr(abc, 1 + floor(random() * length(abc))::int, 1);
  end loop;
  insert into device_codes (code_hash, store_id, kind, label, expires_at, created_by)
  values (encode(sha256(convert_to(code, 'UTF8')), 'hex'), p_store, p_kind, coalesce(nullif(trim(p_label), ''), p_kind),
          now() + interval '30 minutes', auth.uid());
  return substr(code, 1, 5) || '-' || substr(code, 6, 5);
end $$;

create function register_device(p_code text) returns jsonb
language plpgsql volatile security definer set search_path = public as $$
declare
  h  text := encode(sha256(convert_to(upper(regexp_replace(p_code, '[^A-Za-z0-9]', '', 'g')), 'UTF8')), 'hex');
  dc record;
  st record;
begin
  if auth.uid() is null then raise exception '로그인이 필요합니다'; end if;
  if exists (select 1 from devices where user_id = auth.uid() and revoked_at is null) then
    raise exception '이미 등록된 기기입니다';
  end if;
  select * into dc from device_codes where code_hash = h for update;
  if dc is null or dc.used_at is not null or dc.expires_at < now() then
    raise exception '코드가 맞지 않거나 시간이 지났습니다. 매장 화면에서 새 코드를 받아 주세요';
  end if;
  update device_codes set used_at = now() where code_hash = h;
  insert into devices (store_id, user_id, kind, label, last_seen_at) values (dc.store_id, auth.uid(), dc.kind, dc.label, now());
  select name, slug into st from stores where id = dc.store_id;
  return jsonb_build_object('store', st.name, 'slug', st.slug, 'kind', dc.kind, 'label', dc.label);
end $$;

-- 기기가 켜질 때: 나는 어느 가게의 무슨 기기인가 + 가게 설정
create function kiosk_me() returns jsonb
language plpgsql volatile security definer set search_path = public as $$
declare d record;
begin
  select dv.*, s.name as store_name, s.slug into d
    from devices dv join stores s on s.id = dv.store_id
   where dv.user_id = auth.uid() and dv.revoked_at is null;
  if d is null then return null; end if;
  update devices set last_seen_at = now() where id = d.id;
  return jsonb_build_object('store', d.store_name, 'slug', d.slug, 'kind', d.kind, 'label', d.label,
    'cfg', (select cfg from store_settings where store_id = d.store_id),
    'features', (select coalesce(jsonb_object_agg(feature, enabled), '{}') from store_features where store_id = d.store_id));
end $$;

------------------------------------------------------------------------------
-- 3. 기기용 조회 — 손님 목록을 통째로 주지 않고 필요한 답만
------------------------------------------------------------------------------

-- 포인트 조회: 회원인지, 포인트 상태 (이름·번호는 돌려주지 않음)
create function kiosk_lookup(p_phone text) returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare
  s   uuid := device_store();
  cid uuid;
  st  record;
begin
  if s is null then raise exception '등록되지 않은 기기입니다'; end if;
  select id into cid from customers where store_id = s and phone = regexp_replace(p_phone, '[^0-9]', '', 'g');
  if cid is null then return jsonb_build_object('member', false); end if;
  select * into st from point_state(cid);
  return jsonb_build_object('member', true, 'total', st.total, 'usable', st.usable, 'today', st.today, 'soon', st.soon);
end $$;

-- 입구 화면: 접수 받는 중인지, 대기 팀 수, 최근 입장 시각(예상 대기 계산용 — 번호·전화 없음)
create function kiosk_wait_status() returns jsonb
language plpgsql stable security definer set search_path = public as $$
declare
  s uuid := device_store();
  d date;
begin
  if s is null then raise exception '등록되지 않은 기기입니다'; end if;
  d := biz_date(s);
  return jsonb_build_object(
    'on', coalesce((select enabled from store_features where store_id = s and feature = 'wait'), true),
    'waiting', (select count(*) from waitlist where store_id = s and biz_date = d and status = 'wait'),
    'calls', (select coalesce(jsonb_agg(no order by called_at), '[]') from waitlist where store_id = s and biz_date = d and status = 'call'),
    'seated', (select coalesce(jsonb_agg(extract(epoch from seated_at) * 1000 order by seated_at), '[]')
                 from waitlist where store_id = s and biz_date = d and status = 'in' and seated_at > now() - interval '3 hours'));
end $$;

-- 계산대 태블릿: 직원이 보낸 금액
create function kiosk_pending() returns int
language sql stable security definer set search_path = public as $$
  select amount from counter_pending where store_id = device_store()
$$;

-- 계산대 태블릿: 보낸 금액으로 적립하고 금액을 지움 (두 번 적립되지 않게 한 번에)
create function kiosk_earn_pending(p_phone text, p_name text default null,
                                   p_privacy boolean default false, p_marketing boolean default false)
returns table (pts int, is_new boolean, usable int, total int)
language plpgsql volatile security definer set search_path = public as $$
declare
  s uuid := device_store();
  amt int;
begin
  if s is null then raise exception '등록되지 않은 기기입니다'; end if;
  delete from counter_pending where store_id = s returning amount into amt;
  if amt is null then raise exception '계산대에서 보낸 금액이 없습니다'; end if;
  return query select * from kiosk_earn(p_phone, amt, p_name, p_privacy, p_marketing);
end $$;

-- 적립 안 함: 보낸 금액만 지움
create function kiosk_skip_pending() returns void
language sql volatile security definer set search_path = public as $$
  delete from counter_pending where store_id = device_store()
$$;

------------------------------------------------------------------------------
-- 4. 권한 — 기본으로 열리는 함수 실행 권한을 닫고 필요한 것만
------------------------------------------------------------------------------

revoke execute on function make_device_code(uuid, text, text), register_device(text), kiosk_me(), kiosk_lookup(text),
  kiosk_wait_status(), kiosk_pending(), kiosk_earn_pending(text, text, boolean, boolean), kiosk_skip_pending()
  from public, anon;
grant execute on function make_device_code(uuid, text, text), register_device(text), kiosk_me(), kiosk_lookup(text),
  kiosk_wait_status(), kiosk_pending(), kiosk_earn_pending(text, text, boolean, boolean), kiosk_skip_pending()
  to authenticated, service_role;
-- 기기 기록에 '기기 연결 신호'만 바뀐 건 남기지 않음(0001 log_change) — kiosk_me 가 last_seen_at 만 바꿈
