# Supabase — 재아가 직접 할 일

7차 지시서 8장. **hanok-dev 먼저**, 전부 끝나고 실서비스로 갈 때 `hanok` 프로젝트에 같은 순서로 한 번 더.
아래 순서대로 하고, 6번까지 끝나면 Claude Code 에 "다음" 이라고 하면 됩니다(묶음 B 시작).

## 1. 프로젝트 만들기

- supabase.com → New project → 이름 `hanok-dev`, Region **Northeast Asia (Seoul)**, 요금제 Free.
- Database password 는 대시보드 접속용이라 앱과 무관. 어디 적어 두기만.
- 나중에 실서비스용 `hanok` 을 하나 더 (무료 요금제로 2개까지).

## 2. 로그인 설정

Authentication → Providers → **Email**
- Confirm email: **끄기** (계정을 손으로 만들 것이라 확인 메일 불필요)
- Secure email change / **Secure password change: 끄기** — 켜져 있으면 PIN 변경 API(`PUT /auth/v1/user`)가 재인증을 요구해 401 이 납니다
- Minimum password length: **6** 그대로 (그래서 PIN 이 6자리)

Authentication → Settings (또는 Sign In / Up)
- **Allow new users to sign up: 끄기** — 가입은 막습니다. 계정은 아래 3번에서 손으로 둘만

## 3. 계정 두 개

Authentication → Users → **Add user** → Create new user
| 이메일 | 비밀번호 | 역할 |
|---|---|---|
| `staff@jaealee.com` | **6자리 PIN** (숫자만. 카운터에서 누를 것) | 평소 예약 접수·수정 |
| `admin@jaealee.com` | 관리자 비밀번호 (길게, 글자+숫자) | 설정 변경·PIN 변경 |

둘 다 **Auto Confirm User 체크**. 이메일은 실제로 받지 않아도 됩니다(로그인 아이디 역할만).

## 4. 스키마

SQL Editor → New query → `v5/supabase/schema.sql` 내용을 통째로 붙여 넣고 **Run**.
- 끝에 `stores` 에 `hanok`·`anjip` 두 행이 들어갑니다. settings 는 `{}` — 앱이 처음 저장할 때 기본값을 채웁니다
- 두 번 실행해도 됩니다
- Table Editor 에서 `stores` `reservations` `logs` 세 테이블과, 각 테이블의 자물쇠(RLS enabled)가 보이면 됨

## 5. 접속 설정 파일

Project Settings → **API**
- Project URL → `url`
- Project API keys → **`anon` `public`** → `anonKey`
- **`service_role` 은 복사하지 않습니다.** 이 키는 RLS 를 무시하는 전체 권한이라 파일에 들어가는 순간 누구나 DB 를 통째로 가져갈 수 있습니다. `build.py` 가 service_role 이 들어오면 빌드를 멈춥니다

`v5/supabase.dev.json.example` 을 복사해 `v5/supabase.dev.json` 으로 만들고 채웁니다:
```json
{ "url": "https://xxxx.supabase.co", "anonKey": "eyJ...", "staffEmail": "staff@jaealee.com", "adminEmail": "admin@jaealee.com", "demo": true }
```
anon 키와 URL 은 공개용이라 저장소에 올라가도 됩니다.

## 6. 확인 (묶음 B 가 끝난 뒤)

```bash
cd v5
python build.py dev
```
`v5/dev/index.html` 을 열어(사이트라면 `jaealee.com/test/hanok/v5/dev/`) PIN 6자리 입력 → 예약 하나 등록 → Supabase **Table Editor → reservations** 에 행이 생기는지 눈으로 확인.

터미널에서 권한 확인 (URL·ANON 은 5번 값):
```bash
curl -s -H "apikey: ANON" "URL/rest/v1/reservations"
```
→ `401` 이나 `[]` 이어야 합니다(로그인 안 한 anon 은 테이블을 못 봄).
```bash
curl -s -H "apikey: ANON" "URL/rest/v1/public_today"
```
→ `[]` 또는 오늘 예약 행. **이름이 `조 * 결` 처럼 가려져 있고 전화번호가 없어야** 합니다.

## 7. 무료 요금제 주의

- **7일간 요청이 없으면 프로젝트가 일시 정지**됩니다. TV 가 1분마다 읽으니 평소엔 괜찮지만, 휴무로 TV 를 일주일 끄면 대시보드 → Project → **Restore** 를 눌러야 합니다. 정지 중엔 앱이 "오프라인 · 마지막 갱신 …" 띠로 마지막 데이터를 보여 줍니다
- 용량: 예약 하루 20건 × 1년 ≈ 7,000행, 몇 MB. 무료 한도(500MB) 근처에도 안 갑니다

## 8. 실서비스로 갈 때

1. `hanok` 프로젝트에 1~5 반복 (`supabase.prod.json`)
   - 스키마 다음에 패치도 순서대로: `patch_8차.sql` → `patch_9차_홈페이지.sql`(홈페이지 예약: `public_avail`·`requests` 표, anon 은 읽기·접수만) → `patch_10차_홈페이지관리.sql`(홈페이지 관리: `site_draft`·`site_versions`·Storage `site` 버킷) → `patch_11차_알러지.sql`(requests.allergy) → `patch_12차_이름가림.sql`(TV 이름 가림을 앱과 같은 모양으로) → `patch_13차_접수제한.sql`(번호당 하루 5건) → `patch_14차_소식.sql`(site_posts 표 + 첨부 파일 종류) → `patch_15차_근태_손님.sql`(staff·attendance·customers) → `patch_16차_단골.sql`(hanok_tier + public_today.tier)
   - 홈페이지 쪽은 `site/js/config.js` 의 `url`·`anonKey` 를 prod 값으로 교체 (anon 키는 공개해도 됨)
2. `python build.py` (dev 없이) → `v5/index.html` `v5/screen/index.html`
3. 그 전까지 **prod 프로젝트에는 아무것도 쓰지 않습니다.** 예시 데이터 버튼은 prod 빌드에 없습니다

---

## 복구 절차 (백업 JSON → DB)

`hanok-backup` 저장소의 `data/reservations.json` 은 `reservations` 테이블을 그대로 받은 JSON 배열입니다.
되돌릴 때는 SQL Editor 에서 (JSON 을 `$$` 사이에 붙여 넣음):

```sql
insert into reservations
select * from jsonb_populate_recordset(null::reservations, $$ [ ...reservations.json 내용... ] $$::jsonb)
on conflict (id) do update set
  date = excluded.date, time = excluded.time, status = excluded.status, name = excluded.name,
  phone = excluded.phone, people = excluded.people, room_id = excluded.room_id, data = excluded.data,
  deleted_at = excluded.deleted_at;
```

`stores.json` 도 같은 식(`null::stores`, `on conflict (key)`). 수천 행이면 SQL Editor 가 버거우니 날짜 범위로 잘라서 넣습니다.
실제 복구 스크립트는 이번에 만들지 않습니다 — 필요해지면 그때.
