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
