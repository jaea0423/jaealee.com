-- ============================================================
-- 10차 — 홈페이지 관리 (예약 시스템 '더보기 → 관리자 → 홈페이지 관리' 에서 사이트 글·사진·팝업을 고침)
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
-- 대시보드 Storage 에서 만들어도 되지만 SQL 로도 됩니다. public = 누구나 읽기(주소만 알면). 50MB 제한, 그림·PDF 만.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('site', 'site', true, 52428800, array['image/jpeg','image/png','image/webp','application/pdf'])
on conflict (id) do update set public = true, file_size_limit = 52428800, allowed_mime_types = array['image/jpeg','image/png','image/webp','application/pdf'];
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
