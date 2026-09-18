-- ============================================================
-- 한옥반점 예약 시스템 — Supabase 스키마 (v4 7차)
--
-- Supabase 대시보드 → SQL Editor 에 이 파일을 통째로 붙여 넣고 한 번 실행합니다.
-- 두 번 실행해도 됩니다 (create ... if not exists / or replace / on conflict).
-- hanok-dev 와 hanok(실서비스) 두 프로젝트에 각각 한 번씩.
--
-- 왜 이런 모양인가 (work/7차_작업지시.md 1장):
--   · 예약은 행(row) 단위 — JSON 한 덩어리로 두면 기기 두 대가 서로 덮어써 예약이 사라집니다.
--   · 설정은 jsonb 한 덩어리 — 사장 한 사람이 가끔 고치는 것이라 쪼갤 이유가 없습니다.
--   · 칼럼으로 뽑는 것은 조회·정렬·뷰·색인에 필요한 것만. 나머지는 전부 data jsonb.
--     화면 코드가 보는 예약 객체는 지금과 100% 같고, 행 ↔ 객체 변환은 rowToRes / resToRow 두 함수에서만 합니다.
-- ============================================================

-- ---------- 1. 테이블 ----------

create table if not exists stores (
  key        text primary key,                 -- 'hanok' | 'anjip'
  name       text not null,
  settings   jsonb not null default '{}',      -- 지금의 s.settings 통째 (좌석·영업시간·코스·문자·displayRows·tvAd·tvType…)
  snapshots  jsonb not null default '{}',      -- 6차의 s.snapshots (날짜별 좌석 수 — 지난 날짜 예약률 계산용)
  updated_at timestamptz not null default now()
);

create table if not exists reservations (
  id         text primary key,                 -- 클라이언트 newId("res") 가 만든 'res_<UUID v4>' 그대로 (기기 두 대가 동시에 만들어도 안 겹침). 접두어가 있어 uuid 형이 아니라 text
  store      text not null references stores(key),
  date       text not null,                    -- 'YYYY-MM-DD' 문자열. date 형으로 두면 시차(UTC↔KST)로 하루가 밀립니다
  time       text not null,                    -- 'HH:MM'
  status     text not null,                    -- 확정 / 방문 / 노쇼 / 취소 (지금 값 그대로, 한글)
  name       text not null default '',
  phone      text not null default '',         -- 숫자만 (하이픈 제거해서 저장. 화면은 phoneFmt 로 다시 붙임) — 같은 번호 검색용
  people     int  not null default 0,          -- pplOf(r) 결과(유아 포함 총원). 성인/유아 세부는 data 에
  room_id    text,                             -- r.roomId (확정 배정만. 잠정 배정 tentativeRoomId 는 data 에)
  data       jsonb not null default '{}',      -- 나머지 전부: infants, chairs, courses, menuType, source, memo, request, allergy, changes, sms, tentativeRoomId, seatPref, createdAt …
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),  -- 서버가 찍습니다 (아래 트리거). 충돌 검사의 기준값
  deleted_at timestamptz                       -- soft delete. null 이면 살아 있음. 별도 trash 테이블 없음
);
create index if not exists reservations_store_date  on reservations(store, date);
create index if not exists reservations_store_phone on reservations(store, phone);
create index if not exists reservations_updated     on reservations(store, updated_at);   -- 1분 델타 갱신(updated_at=gt.…)용

create table if not exists logs (
  id     bigserial primary key,
  store  text not null,
  at     timestamptz not null default now(),
  action text not null,
  detail text not null default '',
  who    text not null default '',             -- 'staff' | 'admin' | 'screen'
  ua     text not null default ''
);
create index if not exists logs_store_at on logs(store, at desc);

-- updated_at 은 서버가 찍습니다. 태블릿·TV 의 시계는 믿지 않습니다 (틀린 시계 하나가 충돌 검사를 전부 망칩니다)
create or replace function set_updated_at() returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end $$;

drop trigger if exists t_res_upd   on reservations;
drop trigger if exists t_store_upd on stores;
create trigger t_res_upd   before update on reservations for each row execute function set_updated_at();
create trigger t_store_upd before update on stores       for each row execute function set_updated_at();

-- ---------- 2. 권한 (RLS) ----------
-- 로그인한 계정(staff / admin)은 전부 가능, 로그인 안 한 anon 은 테이블 직접 접근 불가.
-- 두 계정이 같은 권한을 갖는 것은 의도된 것 — 관리자 구분은 화면(SESSION.who)에서만 합니다.

alter table stores       enable row level security;
alter table reservations enable row level security;
alter table logs         enable row level security;

drop policy if exists staff_all on stores;
drop policy if exists staff_all on reservations;
drop policy if exists staff_all on logs;
create policy staff_all on stores       for all to authenticated using (true) with check (true);
create policy staff_all on reservations for all to authenticated using (true) with check (true);
create policy staff_all on logs         for all to authenticated using (true) with check (true);

revoke all on stores, reservations, logs from anon;

-- ---------- 3. 손님용 TV — 로그인 없이 보는 두 뷰 ----------
-- 이름은 서버에서 가립니다 (JS maskName 과 같은 모양: "조 * 결", "김 *", 4자 "남궁민수" → "남 * * 수").
-- 전화·요청사항·메모·문자는 뷰에 절대 넣지 않습니다.

-- 한 글자 이름도 가리고, 별은 하나로(별 개수로 이름 길이가 드러나지 않게)
-- 12차: 앱(maskName)과 같은 모양 — 띄어쓰기 빼고 첫·끝 글자만, 글자 수만큼 별 (남궁민수 → 남 * * 수, Tom Cruise → T * * * * * * * e)
create or replace function mask_name(n text) returns text language sql immutable as $$
  with s as (select regexp_replace(trim(coalesce(n, '')), '\s+', '', 'g') as v)
  select case when length(v) <= 1 then '*'
              when length(v) = 2 then left(v, 1) || ' *'
              else left(v, 1) || ' ' || array_to_string(array_fill('*'::text, array[length(v) - 2]), ' ') || ' ' || right(v, 1) end
  from s
$$;

-- 오늘(한국 시각) 확정·방문 예약만. 날짜 비교가 문자열이라 시차 문제가 없습니다
-- 16차: hanok_tier — 단골 등급(방문 2회 VIP · 5회 VVIP · 노쇼 −5). 앱 03c-tier.js 와 같은 숫자
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

-- TV 코드(renderTvList / renderTvGrid / tvSideHtml / displayRows)가 실제로 읽는 설정 키만:
--   rooms(좌석 이름·종류·정원), displayRows(좌석표 3행 배치), tvAd(광고 영상 파일명), tvType(목록형/좌석표), tvIdleFull(예약 없으면 광고만)
--   ※ tvType 은 지금 DATA._ui.tvType 에 있습니다 — 7차 묶음 B 에서 settings.tvType 으로 옮깁니다(보고 참고)
create or replace view public_screen as
  select key as store, name,
         jsonb_build_object('rooms',       settings->'rooms',
                            'displayRows', settings->'displayRows',
                            'tvAd',        settings->'tvAd',
                            'tvType',      settings->'tvType',
                            'tvIdleFull',  settings->'tvIdleFull') as settings
  from stores;

grant select on public_today, public_screen to anon;
grant select on public_today, public_screen to authenticated;

-- ---------- 4. 매장 두 행 ----------
-- settings 는 {} 로 둡니다 — 앱의 migrate() 가 기본값(DEFAULT_DATA.settings)을 채워 첫 저장 때 올라옵니다.
insert into stores (key, name) values
  ('hanok', '한옥반점'),
  ('anjip', '안집')
on conflict (key) do nothing;

-- ---------- 4-1. 이미 uuid 로 만든 프로젝트(7차 A 판) 는 이 한 줄로 바꿉니다 (빈 테이블일 때) ----------
-- alter table reservations alter column id type text;

-- ---------- 5. 확인 ----------
-- 아래 두 줄을 터미널에서 (ANON·URL 은 Project Settings → API):
--   curl -s -H "apikey: ANON" "URL/rest/v1/reservations"   → 401 또는 []  (anon 은 테이블 못 봄)
--   curl -s -H "apikey: ANON" "URL/rest/v1/public_today"   → [] 또는 오늘 행 (이름은 가려져 있어야 함)
