-- ============================================================
-- 대경빌 주차 - 확인용 임시 데이터 (초안 검토용)
-- 실행할 때마다 무작위 차량번호로 29건을 새로 넣습니다.
--   등록 중 13 / 등록 예정 3 / 만료 10 / 삭제됨 3
--
-- ※ 실제 데이터가 이미 들어 있다면 섞이므로 주의하세요.
-- ※ 다 보고 나서 지우는 방법은 이 파일 맨 아래에 있습니다.
-- ============================================================

-- 0) 안전장치: 종료일(end_date)을 비워 둘 수 있어야 합니다.
--    setup.sql 을 아직 다시 실행하지 않았다면 여기서 함께 풀어 줍니다.
alter table public.vehicles alter column end_date drop not null;

-- 무작위 한국식 차량번호를 만드는 함수 (예: 123가 4567)
create or replace function public.rand_plate()
returns text language sql volatile as $$
  select lpad((floor(random() * 900) + 100)::int::text, 3, '0')
      || (array['가','나','다','라','마','거','너','더','러','머',
                '버','서','어','저','고','노','도','로','모','보',
                '소','오','조','구','누','두','루','무','부','수',
                '우','주','하','허','호'])[floor(random() * 35 + 1)]
      || ' '
      || lpad((floor(random() * 9000) + 1000)::int::text, 4, '0');
$$;

-- 무작위 차종
create or replace function public.rand_car()
returns text language sql volatile as $$
  select (array['흰색','검정','회색','은색','파랑','빨강'])[floor(random()*6+1)]
      || ' '
      || (array['아반떼','쏘나타','그랜저','K5','K3','모닝','레이','캐스퍼',
                '투싼','셀토스','코나','니로','스파크','트랙스','아이오닉'])[floor(random()*15+1)];
$$;

-- ---------- 등록 중 13대 ----------
-- 시작일은 과거, 종료일은 미래. 3대는 7일 안에 만료(임박 배너 확인용), 1대는 미정.
insert into public.vehicles (room, plate, start_date, end_date, car_type, memo, deleted)
select
  (100 * ((n - 1) / 3 + 1) + ((n - 1) % 3 + 1))::text || '호',
  public.rand_plate(),
  current_date - ((random() * 300 + 30)::int),
  case
    when n <= 3  then current_date + (n + 1)          -- 2~4일 뒤 만료 (임박)
    when n = 4   then null                            -- 미정
    else current_date + ((random() * 300 + 30)::int)
  end,
  public.rand_car(),
  case when n = 4 then '종료일 미정' else null end,
  false
from generate_series(1, 13) as n;

-- ---------- 등록 예정 3대 (월세 입주 전) ----------
insert into public.vehicles (room, plate, start_date, end_date, car_type, memo, deleted)
select
  (600 + n)::text || '호',
  public.rand_plate(),
  current_date + (n * 5 + 3),
  current_date + (n * 5 + 3) + 364,
  public.rand_car(),
  '입주 예정',
  false
from generate_series(1, 3) as n;

-- ---------- 만료 10대 ----------
insert into public.vehicles (room, plate, start_date, end_date, car_type, memo, deleted)
select
  (100 * ((n - 1) / 3 + 1) + ((n - 1) % 3 + 1))::text || '호',
  public.rand_plate(),
  current_date - ((random() * 700 + 400)::int),
  current_date - ((random() * 300 + 1)::int),
  public.rand_car(),
  null,
  false
from generate_series(1, 10) as n;

-- ---------- 삭제됨 3대 ----------
insert into public.vehicles (room, plate, start_date, end_date, car_type, memo, deleted)
select
  (200 + n)::text || '호',
  public.rand_plate(),
  current_date - 500,
  current_date - 200,
  public.rand_car(),
  (array['중복 등록', '이사 나감', '번호 잘못 입력'])[n],
  true
from generate_series(1, 3) as n;

-- 확인
select
  count(*) filter (where not deleted and start_date <= current_date
                     and (end_date is null or end_date >= current_date)) as "등록 중",
  count(*) filter (where not deleted and start_date > current_date)       as "등록 예정",
  count(*) filter (where not deleted and end_date < current_date)         as "만료",
  count(*) filter (where deleted)                                          as "삭제됨",
  count(*)                                                                 as "전체"
from public.vehicles;

-- ============================================================
-- 다 확인한 뒤 임시 데이터를 지우려면 아래 세 줄의 주석(--)을 지우고 실행하세요.
-- ※ vehicles 표를 통째로 비웁니다. 진짜 데이터가 있으면 절대 실행하지 마세요.
-- ============================================================
-- delete from public.vehicles;
-- drop function if exists public.rand_plate();
-- drop function if exists public.rand_car();
