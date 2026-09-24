-- ============================================================
-- 새 프로젝트 한 번에 세우기 (2026-09-24, 실서비스 prod 용)
-- schema.sql 다음에 8차~22차 패치를 번호 순서대로 이어 붙인 것입니다. 원본 파일은 그대로 두고 이것만 새로 만든 것.
-- 새 Supabase 프로젝트의 SQL Editor 에 통째로 붙여 넣고 Run. 각 조각이 '두 번 실행해도 되는' 형태라 다시 돌려도 됩니다.
-- 먼저 할 것: checklist.md 1~3(로그인 설정, staff·admin 계정). 텔레그램 알림(19차)은 Vault 비밀값 두 개를 넣어야 동작 — checklist 참고.
-- 개발용 예시 자료는 들어 있지 않습니다(매장 hanok·anjip 두 줄과 사진 저장소 'site' 만).
-- 순서: schema.sql → patch_8차.sql → patch_9차_홈페이지.sql → patch_10차_홈페이지관리.sql → patch_11차_알러지.sql → patch_12차_이름가림.sql → patch_13차_접수제한.sql → patch_14차_소식.sql → patch_15차_근태_손님.sql → patch_16차_단골.sql → patch_17차_워크시프트.sql → patch_18차_워크시프트2_감사문자.sql → patch_19차_개발자에게.sql → patch_20차_TV이름.sql → patch_21차_개발자에게2.sql → patch_22차_당일예약.sql
-- ============================================================


-- ################################################################
-- schema.sql
-- ################################################################
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


-- ################################################################
-- patch_8차.sql
-- ################################################################
-- ============================================================
-- 8차 보안 패치 (점검 S3·S4·S7). Supabase SQL Editor 에서 한 번 실행합니다.
-- schema.sql 을 처음부터 다시 돌릴 필요 없이 이 파일만 실행하면 됩니다.
-- ============================================================

-- S7. updated_at 을 INSERT 때도 서버가 찍습니다.
--     (UPDATE 만 걸려 있어, 기기가 updated_at='9999-…' 를 넣어 두면 다른 기기의 1분 델타가 영영 멈췄습니다)
drop trigger if exists t_res_upd   on reservations;
drop trigger if exists t_store_upd on stores;
create trigger t_res_upd   before insert or update on reservations for each row execute function set_updated_at();
create trigger t_store_upd before insert or update on stores       for each row execute function set_updated_at();

-- S3. RLS 가 이메일을 봅니다.
--     to authenticated using(true) 는 '로그인만 되면 누구나' 라서, 대시보드에서 사인업·익명 로그인·OAuth 중 하나만
--     켜지는 순간 전 세계에 열립니다. 우리 계정 두 개(staff·admin)만 통과시키고 익명 토큰은 거부합니다.
--     ★ 아래 두 이메일은 supabase.dev.json 과 같습니다. 실서비스 프로젝트에서는 supabase.prod.json 의 staffEmail / adminEmail 로 바꿔 실행하세요.
create or replace function hanok_is_staff() returns boolean language sql stable as $$
  select coalesce(auth.jwt()->>'email','') in ('staff@jaealee.com','admin@jaealee.com')
     and coalesce((auth.jwt()->>'is_anonymous')::boolean, false) = false
$$;

drop policy if exists staff_all on stores;
drop policy if exists staff_all on reservations;
drop policy if exists staff_all on logs;
create policy staff_all on stores       for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
create policy staff_all on reservations for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
create policy staff_all on logs         for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());

-- S4. 앱은 절대 행을 지우지 않습니다(휴지통 = deleted_at). 지우는 권한 자체를 뺍니다.
--     기록(logs)도 쓰기만 되고 고치거나 지울 수 없게 — 퇴사자 분쟁 때 믿을 수 있어야 합니다.
--     ※ seed_dev.py 의 clear() 는 DELETE 를 쓰므로 dev 프로젝트에서는 이 두 줄을 건너뛰거나, clear 뒤에 다시 실행하세요.
revoke delete on reservations, stores from authenticated;
revoke update, delete on logs from authenticated;

-- logs.who 는 서버가 채웁니다(클라이언트가 보내는 값은 무시) — 위조 방지
alter table logs alter column who set default (auth.jwt()->>'email');

-- 6장. 손님 화면 이름 가리기 — 한 글자 이름도 가리고, 별 개수로 이름 길이가 드러나지 않게 별은 하나로
create or replace function mask_name(n text) returns text language sql immutable as $$
  select case when length(trim(n)) <= 1 then '*'
              when length(trim(n)) = 2 then left(trim(n),1) || ' *'
              else left(trim(n),1) || ' * ' || right(trim(n),1) end
$$;

-- 8차-H. 손님 TV 가 테이블 예약을 층별로 보여 주려면 희망 층(seatPref)이 필요합니다. 전화·메모는 여전히 안 나갑니다.
create or replace view public_today as
  select store, time, mask_name(name) as name, people, room_id, status, data->>'seatPref' as seat_pref
  from reservations
  where deleted_at is null and status in ('확정','방문')
    and date = to_char(now() at time zone 'Asia/Seoul', 'YYYY-MM-DD');


-- ################################################################
-- patch_9차_홈페이지.sql
-- ################################################################
-- ============================================================
-- 9차 — 홈페이지 예약 연동 (site/ ↔ v7)
-- Supabase 대시보드 → SQL Editor 에 붙여 넣고 실행. 두 번 실행해도 됩니다.
-- hanok-dev 먼저, 실서비스는 prod 에서 다시.
--
-- 구조 (왜 이렇게 했나):
--   · 홈페이지는 로그인이 없으니 anon 키로 접근합니다. anon 이 할 수 있는 건 딱 둘 —
--     ① public_avail 읽기(남은 자리)  ② requests 에 한 줄 넣기(접수). 예약 표·설정·전화번호는 절대 못 봅니다.
--   · 남은 자리 계산은 SQL 로 다시 짜지 않습니다. v7(직원 태블릿)이 이미 계산하는 값을 public_avail 에 올려 두고
--     홈페이지는 그걸 읽기만 합니다. 태블릿이 꺼져 있으면 마지막 값이 남습니다 — 접수는 어차피 직원 확인 뒤 확정이라 괜찮습니다.
--   · requests 는 v7 의 '홈페이지 예약' 창이 읽어 승인(→ reservations 에 등록)·거절합니다. 24시간 지나면 만료.
-- ============================================================

-- ---------- 1. 남은 자리 (v7 → 홈페이지) ----------
create table if not exists public_avail (
  store      text not null references stores(key),
  date       text not null,                 -- 'YYYY-MM-DD'
  data       jsonb not null default '{}',   -- {"11:00":{"rooms":[[5,7],[2,6]],"tableMax":6}, ...}  rooms = 빈 룸의 [최소,최대] 인원, tableMax = 테이블에 앉힐 수 있는 최대 인원
  updated_at timestamptz not null default now(),
  primary key (store, date)
);
alter table public_avail enable row level security;
drop policy if exists staff_all on public_avail;
drop policy if exists anon_read on public_avail;
create policy staff_all on public_avail for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
create policy anon_read on public_avail for select to anon using (true);
revoke all on public_avail from anon;   -- Supabase 기본값이 새 표에 anon 전권을 주므로 먼저 걷어냄(RLS 가 막긴 하지만 schema.sql 79행과 같은 원칙)
grant select on public_avail to anon;
grant all on public_avail to authenticated;
drop trigger if exists t_avail_upd on public_avail;
create trigger t_avail_upd before update on public_avail for each row execute function set_updated_at();

-- ---------- 2. 홈페이지 예약 접수 (홈페이지 → v7) ----------
create table if not exists requests (
  id           text primary key,            -- 홈페이지가 만든 'rq_<난수>'
  store        text not null references stores(key),
  date         text not null,
  time         text not null,
  adults       int  not null default 0,
  kids         int  not null default 0,
  people       int  not null default 0,
  seat         text not null default 'table',   -- 'room' | 'table'
  course       text not null default 'none',    -- 'course:촉 코스' | 'set:B 세트' | 'later' | 'none'
  course_label text not null default '',
  name         text not null default '',
  phone        text not null default '',        -- 숫자만
  request      text not null default '',
  status       text not null default '대기',    -- 대기 / 확정 / 거절 / 만료
  reason       text not null default '',
  res_id       text,                            -- 확정되면 reservations.id
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now(),
  expires_at   timestamptz not null default (now() + interval '24 hours')
);
create index if not exists requests_store_status on requests(store, status, created_at);
alter table requests enable row level security;
drop policy if exists staff_all   on requests;
drop policy if exists anon_insert on requests;
create policy staff_all on requests for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
-- anon 은 넣기만. 값의 모양도 여기서 한 번 더 조입니다(홈페이지 코드가 걸러도 서버가 최종)
create policy anon_insert on requests for insert to anon with check (
  store = 'hanok' and status = '대기' and res_id is null and reason = ''
  and date ~ '^\d{4}-\d{2}-\d{2}$' and time ~ '^\d{2}:\d{2}$'
  and date >  to_char(now() at time zone 'Asia/Seoul', 'YYYY-MM-DD')                       -- 당일은 전화
  and date <= to_char((now() at time zone 'Asia/Seoul') + interval '31 days', 'YYYY-MM-DD')
  and adults between 2 and 12 and kids between 0 and 12 and people = adults + kids and people <= 12
  and seat in ('room','table') and (seat <> 'room' or adults >= 5)
  and length(name) between 1 and 30 and phone ~ '^01\d{8,9}$' and length(request) <= 300
);
revoke all on requests from anon;
grant insert on requests to anon;   -- 읽기·고치기·지우기는 없음. 접수 한 줄 넣기만
grant all on requests to authenticated;
revoke delete on requests, public_avail from authenticated;   -- 지우지 않습니다(S4 와 같은 원칙)
drop trigger if exists t_req_upd on requests;
create trigger t_req_upd before update on requests for each row execute function set_updated_at();

-- 접수 폭주 막기: 같은 번호는 하루 3건(13차에서 5건으로), 전체는 10분에 20건. 넘으면 거부(홈페이지는 "잠시 뒤 다시" 안내)
create or replace function requests_rate_limit() returns trigger language plpgsql security definer as $$
begin
  if (select count(*) from requests where phone = new.phone and created_at > now() - interval '1 day') >= 3 then
    raise exception 'RATE_PHONE' using errcode = 'P0001';
  end if;
  if (select count(*) from requests where created_at > now() - interval '10 minutes') >= 20 then
    raise exception 'RATE_ALL' using errcode = 'P0001';
  end if;
  return new;
end $$;
drop trigger if exists t_req_rate on requests;
create trigger t_req_rate before insert on requests for each row execute function requests_rate_limit();

-- ---------- 3. 확인 ----------
-- select * from public_avail limit 3;
-- select id, status, date, time, people, seat, expires_at from requests order by created_at desc limit 5;


-- ################################################################
-- patch_10차_홈페이지관리.sql
-- ################################################################
-- ============================================================
-- 10차 — 홈페이지 관리 (예약 시스템 '설정 → 홈페이지 → 홈페이지 관리 열기' 에서 사이트 글·사진·팝업·예약 접수를 고침. TV 광고 영상 파일도 같은 버킷)
-- Supabase 대시보드 → SQL Editor 에 붙여 넣고 실행. 두 번 실행해도 됩니다. hanok-dev 먼저, 실서비스는 prod 에서 다시.
--
-- 구조 (왜 이렇게 했나):
--   · 사이트(GitHub Pages)는 정적이라 파일을 고쳐 올릴 수 없습니다. 대신 사이트가 뜰 때 여기서 내용(JSON 하나)을 읽어
--     data/site.js 의 기본값 위에 덮습니다(hanok/js/content.js). 서버가 죽어도 기본값으로 뜹니다.
--   · site_draft   : 지금 고치는 중인 초안(매장당 한 줄). 사이트에 ?preview=1 을 붙이면 이걸 읽어 미리보기.
--   · site_versions: '적용' 할 때마다 한 판씩 쌓임. apply_at 이 미래면 예약 적용. 사이트는 apply_at ≤ 지금 인 최신 판을 씀.
--     되돌리기 = 옛 판을 새 판으로 다시 넣기(지우지 않음). 예약해 둔(미래) 판만 지울 수 있게 정책을 둡니다.
--   · anon 은 둘 다 읽기만(초안도 공개 — 손님이 볼 일은 없지만 비밀은 아님. 사진·PDF 파일은 어차피 공개 버킷).
--   · 사진·PDF 파일은 Storage 버킷 'site' — 아래 3장. 공개 읽기, 직원만 올리기·지우기.
-- ============================================================

-- ---------- 1. 초안 ----------
create table if not exists site_draft (
  store      text primary key references stores(key),
  data       jsonb not null default '{}',
  updated_at timestamptz not null default now(),
  by         text not null default ''
);
alter table site_draft enable row level security;
drop policy if exists staff_all on site_draft;
drop policy if exists anon_read on site_draft;
create policy staff_all on site_draft for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
create policy anon_read on site_draft for select to anon using (true);
revoke all on site_draft from anon;
grant select on site_draft to anon;
grant all on site_draft to authenticated;
drop trigger if exists t_site_draft_upd on site_draft;
create trigger t_site_draft_upd before update on site_draft for each row execute function set_updated_at();

-- ---------- 2. 적용한 판 ----------
create table if not exists site_versions (
  id         bigserial primary key,
  store      text not null references stores(key),
  data       jsonb not null,
  apply_at   timestamptz not null default now(),   -- 이 시각부터 사이트에 보임. 미래면 예약 적용
  note       text not null default '',             -- "추석 팝업", "가을 메뉴" 같은 메모
  created_at timestamptz not null default now(),
  by         text not null default ''
);
create index if not exists site_versions_store_apply on site_versions(store, apply_at desc);
alter table site_versions enable row level security;
drop policy if exists staff_rw      on site_versions;
drop policy if exists staff_del_future on site_versions;
drop policy if exists anon_read     on site_versions;
create policy staff_rw on site_versions for select to authenticated using (hanok_is_staff());
drop policy if exists staff_ins on site_versions;
create policy staff_ins on site_versions for insert to authenticated with check (hanok_is_staff());
-- 지우기는 아직 안 보인(미래) 판만 — 예약 적용 취소용. 이미 보인 판은 이력이라 남깁니다
create policy staff_del_future on site_versions for delete to authenticated using (hanok_is_staff() and apply_at > now());
create policy anon_read on site_versions for select to anon using (apply_at <= now());   -- 예약해 둔 판은 손님에게 미리 안 보임
revoke all on site_versions from anon;
grant select on site_versions to anon;
grant select, insert, delete on site_versions to authenticated;
grant usage, select on sequence site_versions_id_seq to authenticated;

-- ---------- 3. 파일 버킷 (사진·메뉴판 PDF) ----------
-- 대시보드 Storage 에서 만들어도 되지만 SQL 로도 됩니다. public = 누구나 읽기(주소만 알면). 50MB 제한, 그림·PDF·MP4(TV 광고 영상)만.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('site', 'site', true, 52428800, array['image/jpeg','image/png','image/webp','application/pdf','video/mp4'])
on conflict (id) do update set public = true, file_size_limit = 52428800, allowed_mime_types = array['image/jpeg','image/png','image/webp','application/pdf','video/mp4'];
drop policy if exists site_public_read on storage.objects;
drop policy if exists site_staff_write on storage.objects;
drop policy if exists site_staff_update on storage.objects;
drop policy if exists site_staff_delete on storage.objects;
create policy site_public_read  on storage.objects for select to anon, authenticated using (bucket_id = 'site');
create policy site_staff_write  on storage.objects for insert to authenticated with check (bucket_id = 'site' and hanok_is_staff());
create policy site_staff_update on storage.objects for update to authenticated using (bucket_id = 'site' and hanok_is_staff());
create policy site_staff_delete on storage.objects for delete to authenticated using (bucket_id = 'site' and hanok_is_staff());

-- ---------- 4. 확인 ----------
-- select store, updated_at from site_draft;
-- select id, apply_at, note, created_at from site_versions order by apply_at desc limit 5;


-- ################################################################
-- patch_11차_알러지.sql
-- ################################################################
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


-- ################################################################
-- patch_12차_이름가림.sql
-- ################################################################
-- 12차 (2026-09-17) 손님 TV 이름 가림을 앱(maskName)과 같은 모양으로.
--  · 예전: 세 글자 넘어도 '김 * 아' 처럼 별 하나 → 글자 수를 알 수 없고, 외국 이름은 'T * e' 로 이상함
--  · 지금: 띄어쓰기는 빼고 첫 글자·끝 글자만 남기고 글자 수만큼 별 (재아) — 남궁민수 → 남 * * 수, Tom Cruise → T * * * * * * * e
-- public_today / public_screen 뷰는 이 함수를 그대로 부르므로 함수만 바꾸면 됩니다. dev·prod 모두 SQL Editor 에서 한 번.
create or replace function mask_name(n text) returns text language sql immutable as $$
  with s as (select regexp_replace(trim(coalesce(n, '')), '\s+', '', 'g') as v)
  select case when length(v) <= 1 then '*'
              when length(v) = 2 then left(v, 1) || ' *'
              else left(v, 1) || ' ' || array_to_string(array_fill('*'::text, array[length(v) - 2]), ' ') || ' ' || right(v, 1) end
  from s
$$;


-- ################################################################
-- patch_13차_접수제한.sql
-- ################################################################
-- 13차 (2026-09-17) 홈페이지 접수 제한: 같은 번호 하루 3건 → 5건 (재아). 전체 10분 20건은 그대로.
-- dev·prod 모두 SQL Editor 에서 한 번. 홈페이지 문구(js/reserve.js "이미 5건")와 숫자를 맞춰 둡니다.
create or replace function requests_rate_limit() returns trigger language plpgsql security definer as $$
begin
  if (select count(*) from requests where phone = new.phone and created_at > now() - interval '1 day') >= 5 then
    raise exception 'RATE_PHONE' using errcode = 'P0001';
  end if;
  if (select count(*) from requests where created_at > now() - interval '10 minutes') >= 20 then
    raise exception 'RATE_ALL' using errcode = 'P0001';
  end if;
  return new;
end $$;


-- ################################################################
-- patch_14차_소식.sql
-- ################################################################
-- 14차 (2026-09-18) 홈페이지 '소식' — 사장님이 글을 쌓는 게시판. 사진·파일 첨부는 Storage 'site' 버킷(10차)에.
-- 초안·적용 판(site_draft/site_versions)과 별개로, 글은 저장하면 바로 홈페이지에 나옵니다('게시'). '초안' 은 관리 화면에만.
-- 지우기는 없음(S4 원칙) — status '삭제' 로 숨깁니다.
create table if not exists site_posts (
  id          text primary key,                       -- 앱이 만듦 (post_ + 랜덤)
  store       text not null default 'hanok',
  title       text not null,
  body        text not null default '',               -- 줄바꿈 그대로. **굵게** 가능(사이트 rich)
  date        date not null default current_date,     -- 글에 보이는 날짜(정렬 기준). 지난 날짜로 적어도 됨
  images      jsonb not null default '[]',            -- ["https://…/site/hanok/image/….jpg", …]
  files       jsonb not null default '[]',            -- [{"name":"가을 메뉴.pdf","url":"https://…"}, …]
  pinned      boolean not null default false,         -- 맨 위에 고정
  status      text not null default '게시' check (status in ('게시','초안','삭제')),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  by          text not null default ''
);
create index if not exists site_posts_list on site_posts (store, status, pinned desc, date desc);
drop trigger if exists t_posts_upd on site_posts;
create trigger t_posts_upd before update on site_posts for each row execute function set_updated_at();

alter table site_posts enable row level security;
drop policy if exists staff_rw on site_posts;
drop policy if exists anon_read on site_posts;
create policy staff_rw  on site_posts for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
create policy anon_read on site_posts for select to anon using (status = '게시');   -- 손님은 게시한 글만
-- Supabase 는 새 표에 anon·authenticated 전부 권한을 기본으로 주므로 명시적으로 걷어냅니다(RLS 가 막긴 하지만 이중으로)
revoke all on site_posts from anon, authenticated;
grant select on site_posts to anon;
grant select, insert, update on site_posts to authenticated;   -- delete 없음

-- 첨부 파일 종류를 넓힘: 사진·PDF·영상에 더해 한글·워드·엑셀·zip (글에 붙이는 파일)
update storage.buckets set allowed_mime_types = array[
  'image/jpeg','image/png','image/webp','image/gif','application/pdf','video/mp4',
  'application/x-hwp','application/haansofthwp','application/vnd.hancom.hwp','application/vnd.hancom.hwpx',
  'application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.ms-powerpoint','application/vnd.openxmlformats-officedocument.presentationml.presentation',
  'application/zip','text/plain','application/octet-stream']
where id = 'site';


-- ################################################################
-- patch_15차_근태_손님.sql
-- ################################################################
-- 15차 (2026-09-18) 직원 근태 + 손님 관리 (재아). 사장님이 직접 체크하는 표 — 화면은 관리자 비밀번호 뒤.
--  · staff: 직원(정규 근무 시간표·급여 방식). 퇴사는 active=false, 지우기 없음
--  · attendance: 날짜·직원마다 한 줄. 정규(○)/변형(시간 다름)/결근(×)/휴무(–), 배율(1.5배), 메모
--  · customers: 손님 메모 — 예약 자체는 reservations 에 있으니 여기엔 전화번호 열쇠 + 메모 + 이름 고정만
-- 서버 권한은 지금은 직원 로그인(hanok_is_staff)과 같음. '직원은 열람만' 은 나중 작업(권한 빼기)에서 admin 세션으로 나눕니다.
create table if not exists staff (
  id          text primary key,                    -- 앱이 만듦 (stf_…)
  store       text not null default 'hanok',
  name        text not null,
  role        text not null default '',            -- 홀·주방·매니저 같은 것(자유)
  phone       text not null default '',
  pay_type    text not null default 'hourly' check (pay_type in ('hourly','monthly')),
  pay         integer not null default 0,          -- 시급 또는 월급(원)
  sched       jsonb not null default '{}',         -- {"days":[false,true,…7], "start":"10:00", "end":"22:00", "break":60}
  start_date  date,
  end_date    date,
  memo        text not null default '',
  active      boolean not null default true,
  sort        integer not null default 0,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create table if not exists attendance (
  id          text primary key,                    -- att_<staff>_<date>
  store       text not null default 'hanok',
  staff_id    text not null references staff(id),
  date        date not null,
  status      text not null check (status in ('정규','변형','결근','휴무')),
  start       text not null default '',            -- 변형일 때 "HH:MM"
  "end"       text not null default '',
  break_min   integer not null default 0,
  rate        numeric(3,2) not null default 1,     -- 1 · 1.5 · 2
  memo        text not null default '',
  by          text not null default '',
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (store, staff_id, date)
);
create index if not exists attendance_month on attendance (store, date);
create table if not exists customers (
  store       text not null default 'hanok',
  phone       text not null,                       -- 숫자만 (01012345678)
  name        text not null default '',            -- 비우면 예약에서 가장 많이 쓴 이름
  memo        text not null default '',
  by          text not null default '',
  updated_at  timestamptz not null default now(),
  primary key (store, phone)
);
drop trigger if exists t_staff_upd on staff;      create trigger t_staff_upd before update on staff      for each row execute function set_updated_at();
drop trigger if exists t_att_upd   on attendance; create trigger t_att_upd   before update on attendance for each row execute function set_updated_at();
drop trigger if exists t_cust_upd  on customers;  create trigger t_cust_upd  before update on customers  for each row execute function set_updated_at();

alter table staff enable row level security;
alter table attendance enable row level security;
alter table customers enable row level security;
drop policy if exists staff_all on staff;      create policy staff_all on staff      for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
drop policy if exists staff_all on attendance; create policy staff_all on attendance for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
drop policy if exists staff_all on customers;  create policy staff_all on customers  for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
revoke all on staff, attendance, customers from anon, authenticated;
grant select, insert, update on staff, customers to authenticated;
grant select, insert, update, delete on attendance to authenticated;   -- 근태 칸은 '지우기' 가 자연스러움(잘못 찍은 것) — 사람·손님은 안 지움


-- ################################################################
-- patch_16차_단골.sql
-- ################################################################
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


-- ################################################################
-- patch_17차_워크시프트.sql
-- ################################################################
-- 17차 (2026-09-18) 워크시프트(직원 근태 → 급여까지). 15차 표에 덧붙임.
--  · staff.nick(별칭 — 화면에서 이름보다 먼저: '만두언니'), staff.tax(공제 방식: 4대보험 / 3.3% / 없음), staff.weekly_pay(주휴수당 자동 계산 여부)
--  · hr_settings: 사업장 설정 한 줄 — 5인 이상 여부(연장·야간 가산 적용), 4대보험 요율(매년 1월 확인), 야간 시간대
alter table staff add column if not exists nick text not null default '';
alter table staff add column if not exists tax text not null default '4대보험';
alter table staff add column if not exists weekly_pay boolean not null default true;
alter table staff drop constraint if exists staff_tax_check;
alter table staff add constraint staff_tax_check check (tax in ('4대보험','3.3%','없음'));

create table if not exists hr_settings (
  store       text primary key default 'hanok',
  data        jsonb not null default '{}',   -- {"over5":true, "rates":{"pension":4.5,"health":3.545,"care":12.95,"employ":0.9}, "night":["22:00","06:00"], "taxRate":3.3}
  updated_at  timestamptz not null default now()
);
drop trigger if exists t_hrs_upd on hr_settings; create trigger t_hrs_upd before update on hr_settings for each row execute function set_updated_at();
alter table hr_settings enable row level security;
drop policy if exists staff_all on hr_settings; create policy staff_all on hr_settings for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
revoke all on hr_settings from anon, authenticated;
grant select, insert, update on hr_settings to authenticated;


-- ################################################################
-- patch_18차_워크시프트2_감사문자.sql
-- ################################################################
-- 18차 (2026-09-19) 워크시프트 2 + 감사 문자 (재아)
--  · staff.sched_hist: 정규 근무를 기간별로 [{from:"2026-01-01", days:[7], spans:[{start,end,break}]}] — 하루 두 타임도 spans 로
--  · staff.pay_hist : 시급/월급을 기간별로 [{from:"2026-09-01", pay:11000}] (기본 1일부터)
--  · staff.absent_deduct: 월급제 결근 일할 공제 여부
--  · attendance.spans: 다른 시간(△)이 하루 두 타임일 때 [{start,end,break}] (start/end 는 첫 타임을 그대로 둠)
--  · thanks_sms: 감사 문자 대기열 — 확인(방문)된 예약만, 보낼 시각에 보냄(문자 업체 연결 전엔 흉내)
alter table staff add column if not exists sched_hist jsonb not null default '[]';
alter table staff add column if not exists pay_hist jsonb not null default '[]';
alter table staff add column if not exists absent_deduct boolean not null default false;
alter table attendance add column if not exists spans jsonb not null default '[]';

create table if not exists thanks_sms (
  id          text primary key,
  store       text not null default 'hanok',
  res_id      text not null,
  phone       text not null,
  name        text not null default '',
  text        text not null,
  send_at     timestamptz not null,
  status      text not null default '대기' check (status in ('대기','보냄','취소','실패')),
  made_by     text not null default '',     -- 'ai' | 'template' | 'manual'
  by          text not null default '',
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now(),
  unique (store, res_id)
);
drop trigger if exists t_thanks_upd on thanks_sms; create trigger t_thanks_upd before update on thanks_sms for each row execute function set_updated_at();
alter table thanks_sms enable row level security;
drop policy if exists staff_all on thanks_sms; create policy staff_all on thanks_sms for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
revoke all on thanks_sms from anon, authenticated;
grant select, insert, update on thanks_sms to authenticated;


-- ################################################################
-- patch_19차_개발자에게.sql
-- ################################################################
-- 19차 (2026-09-20) '개발자에게' (재아). 사장님·직원이 개선 요청·급한 조치를 글로 남기는 곳.
--  · 매번 전화·카톡으로 연락하는 게 서로 불편해서. 급함/보통 을 나누고, 급함만 재아에게 알림(아래 웹훅).
--  · 재아 답변(reply)·상태(status)는 재아가 적음 — 화면에서는 사장님이 상태를 '끝' 으로만 바꿀 수 있음.
create table if not exists dev_requests (
  id          text primary key,                    -- 앱이 만듦 (dq_…)
  store       text not null default 'hanok',
  title       text not null,
  body        text not null default '',
  urgent      boolean not null default false,      -- 급함(재아에게 알림) / 보통(모아서 봄)
  status      text not null default '접수' check (status in ('접수','확인','처리 중','끝')),
  images      jsonb not null default '[]',         -- 화면 사진 주소 목록(Storage site 버킷)
  by          text not null default '',            -- staff / admin
  reply       text not null default '',            -- 재아 답변
  replied_at  timestamptz,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create index if not exists dev_requests_list on dev_requests (store, created_at desc);
drop trigger if exists t_devreq_upd on dev_requests; create trigger t_devreq_upd before update on dev_requests for each row execute function set_updated_at();
alter table dev_requests enable row level security;
drop policy if exists staff_all on dev_requests; create policy staff_all on dev_requests for all to authenticated using (hanok_is_staff()) with check (hanok_is_staff());
revoke all on dev_requests from anon, authenticated;
grant select, insert, update on dev_requests to authenticated;

-- 급함 알림: Supabase 대시보드 → Database → Webhooks → 새 웹훅
--   표 dev_requests · INSERT · 조건 없음(웹훅은 조건을 못 걸어 받는 쪽에서 urgent 만 거름)
--   URL 은 텔레그램 봇(https://api.telegram.org/bot<토큰>/sendMessage) 앞에 둔 작은 중계(Cloudflare Worker 등) 또는 디스코드 웹훅.
--   메일 주소는 화면에 안 박음(재아 09-20: 매크로·스팸 우려).

-- ---------- 급함 알림 → 텔레그램 (재아 09-20) ----------
-- 봇 토큰·채팅 ID 는 저장소·대화·HTML 어디에도 적지 않고 Supabase Vault 에만 둡니다.
-- 준비(대시보드에서 한 번):
--   1) Database → Extensions 에서 pg_net 켜기
--   2) Project Settings → Vault → New secret 두 개
--        이름 telegram_bot_token   값 123456:ABC-…   (BotFather 가 준 토큰)
--        이름 telegram_chat_id     값 987654321      (재아 채팅 ID — @userinfobot 에게 아무 말이나 보내면 알려 줌)
--   3) 아래를 SQL Editor 에서 실행
--   4) 봇에게 먼저 /start 한 번 보내 두기 (봇은 먼저 말을 건 사람에게만 보낼 수 있음)
create extension if not exists pg_net;
create or replace function hanok_notify_dev_request() returns trigger
language plpgsql security definer set search_path = public, vault, net as $$
declare tok text; chat text; body text;
begin
  if not new.urgent then return new; end if;   -- 보통은 알림 없음(재아가 모아서 봄)
  select decrypted_secret into tok  from vault.decrypted_secrets where name = 'telegram_bot_token' limit 1;
  select decrypted_secret into chat from vault.decrypted_secrets where name = 'telegram_chat_id'   limit 1;
  if tok is null or chat is null then return new; end if;   -- 아직 안 넣었으면 조용히 통과(글은 저장됨)
  body := '🔴 ' || case new.store when 'hanok' then '한옥반점' when 'anjip' then '안집' else new.store end || ' · 급함' || E'\n' || new.title   -- 봇 하나로 여러 가게(재아 09-20): 첫 줄에서 가게를 가름
        || E'\n' || left(coalesce(new.body, ''), 300)
        || E'\n' || '— ' || case when new."by" = 'admin' then '사장님' else '직원' end || ' · ' || to_char(new.created_at at time zone 'Asia/Seoul', 'MM/DD HH24:MI');   -- "by" 는 예약어라 따옴표 필수(09-20 재아가 잡음)
  perform net.http_post(
    url := 'https://api.telegram.org/bot' || tok || '/sendMessage',
    headers := '{"Content-Type":"application/json"}'::jsonb,
    body := jsonb_build_object('chat_id', chat, 'text', body));
  return new;
end $$;
drop trigger if exists t_devreq_notify on dev_requests;
create trigger t_devreq_notify after insert on dev_requests for each row execute function hanok_notify_dev_request();
-- 시험: insert into dev_requests (id, title, body, urgent, by) values ('dq_test', '알림 시험', '이게 오면 됩니다', true, 'admin');  → 폰 확인 뒤 delete from dev_requests where id='dq_test';


-- ################################################################
-- patch_20차_TV이름.sql
-- ################################################################
-- 20차 (2026-09-20) 손님 TV 에 이름을 가리지 않고 그대로 (재아: TV 는 매장 안에 두니 가릴 이유가 없음).
-- public_today / public_screen 뷰가 mask_name() 을 부르므로, 함수를 '그대로 돌려주기' 로 바꾸면 뷰는 손댈 것 없음.
-- 다시 가리고 싶으면 patch_12차 의 함수 정의를 다시 실행하면 됩니다. dev·prod 모두 SQL Editor 에서 한 번.
create or replace function mask_name(n text) returns text language sql immutable as $$
  select trim(coalesce(n, ''))
$$;


-- ################################################################
-- patch_21차_개발자에게2.sql
-- ################################################################
-- 21차 (2026-09-20) 개발자에게 손질 (재아)
--  · 상태는 '접수' → '답변 완료' 두 가지만 (재아가 답변을 적으면 '답변 완료'). 옛 값(확인·처리 중·끝)도 그대로 둠
--  · 사장님은 글을 지울 수 있음(삭제하기) — delete 권한
--  · 급함 알림(텔레그램)에 화면 사진 주소도 같이 (텔레그램이 링크 미리보기를 보여 줌)
alter table dev_requests drop constraint if exists dev_requests_status_check;
alter table dev_requests add constraint dev_requests_status_check check (status in ('접수','확인','처리 중','끝','답변 완료'));
grant delete on dev_requests to authenticated;

create or replace function hanok_notify_dev_request() returns trigger
language plpgsql security definer set search_path = public, vault, net as $$
declare tok text; chat text; body text; imgs text;
begin
  if not new.urgent then return new; end if;
  select decrypted_secret into tok  from vault.decrypted_secrets where name = 'telegram_bot_token' limit 1;
  select decrypted_secret into chat from vault.decrypted_secrets where name = 'telegram_chat_id'   limit 1;
  if tok is null or chat is null then return new; end if;
  select string_agg(value #>> '{}', E'\n') into imgs from jsonb_array_elements(coalesce(new.images, '[]'::jsonb));
  body := '🔴 ' || case new.store when 'hanok' then '한옥반점' when 'anjip' then '안집' else new.store end || ' · 급함' || E'\n' || new.title
        || E'\n' || left(coalesce(new.body, ''), 300)
        || case when imgs is not null and imgs <> '' then E'\n📷 ' || imgs else '' end
        || E'\n' || '— ' || case when new."by" = 'admin' then '사장님' else '직원' end || ' · ' || to_char(new.created_at at time zone 'Asia/Seoul', 'MM/DD HH24:MI');
  perform net.http_post(
    url := 'https://api.telegram.org/bot' || tok || '/sendMessage',
    headers := '{"Content-Type":"application/json"}'::jsonb,
    body := jsonb_build_object('chat_id', chat, 'text', body));
  return new;
end $$;

-- 재아가 답하는 법: Table Editor → dev_requests → 그 줄의 reply 에 답을 적고 status 를 '답변 완료' 로, replied_at 은 now().
-- 또는 SQL:  update dev_requests set reply = '…', status = '답변 완료', replied_at = now() where id = 'dq_…';


-- ################################################################
-- patch_22차_당일예약.sql
-- ################################################################
-- ============================================================
-- 22차 — 홈페이지 '당일 예약' 스위치 (2026-09-24). 두 번 실행해도 됩니다. dev 먼저, prod 는 실서비스 때.
-- 지금까지 서버는 '내일부터' 만 받았습니다(date > 오늘). 관리 화면에서 당일 예약을 켜면 예약 창이 오늘도 고르게 되므로
-- 서버는 오늘부터 받게 넓힙니다. 켜고 끄는 건 홈페이지 설정(SITE.online.sameDay)이 합니다 — 끈 동안은 예약 창이 오늘을 안 보여 줌.
-- 09-24 추가: 홈페이지 '예약 가능 기간' 을 90일까지 늘릴 수 있게 31일 → 91일(기본은 여전히 30일). 그 밖은 11차 정책과 같습니다.
-- ============================================================
drop policy if exists anon_insert on requests;
create policy anon_insert on requests for insert to anon with check (
  store = 'hanok' and status = '대기' and res_id is null and reason = ''
  and date ~ '^\d{4}-\d{2}-\d{2}$' and time ~ '^\d{2}:\d{2}$'
  and date >= to_char(now() at time zone 'Asia/Seoul', 'YYYY-MM-DD')
  and date <= to_char((now() at time zone 'Asia/Seoul') + interval '91 days', 'YYYY-MM-DD')
  and adults between 2 and 12 and kids between 0 and 12 and people = adults + kids and people <= 12
  and seat in ('room','table') and (seat <> 'room' or adults >= 5)
  and length(name) between 1 and 30 and phone ~ '^01\d{8,9}$' and length(request) <= 300 and length(allergy) <= 100
);
