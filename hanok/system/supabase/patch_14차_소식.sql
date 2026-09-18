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
