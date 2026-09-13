# v5 — Supabase 연동 작업 폴더

**여기가 작업 공간입니다. `../v4` 와 그 위는 전부 읽기 전용입니다.**
v4 는 6차(UI 정리·데이터 모양 확정)까지 끝난 상태로 그대로 둡니다. v5 는 그 복사본에서 시작합니다(2026-09-14).

---

## 0. 무엇이 어디에 있나

| 경로 | 상태 |
|---|---|
| `../src/` `../index.html` `../v2/` `../v3/` `../v4/` | **읽기만** |
| `../assets/*.b64` `../v4/assets/*.b64` | **읽기만.** 빌드가 이미지·글꼴을 여기서 가져옵니다 (복사하지 않음 — 갈라지지 않게) |
| `v5/src/index.html` | ★ 여기만 고칩니다 |
| `v5/build.py` | 빌드. `__SUPA_CFG__` 자리에 설정 파일을 끼웁니다 |
| `v5/supabase/schema.sql` | Supabase SQL Editor 에서 한 번 실행하는 스키마 |
| `v5/supabase/checklist.md` | 재아가 대시보드에서 직접 할 일 + 복구 절차 |
| `v5/supabase.dev.json` `v5/supabase.prod.json` | 접속 설정(재아가 채움). anon 키만. **service_role 은 어디에도 쓰지 않음** |
| `v5/backup/hanok-backup.yml` | 비공개 저장소 `hanok-backup` 으로 옮길 GitHub Actions 워크플로 |
| `v5/screen/ad.mp4` | 손님 화면 광고 영상(29MB) — 반드시 screen/ 안에 (adUrl 이 screen/ 을 붙임) |
| `v5/work/` | 지시서 · 패치 스크립트 · 스크린샷 · 진행 기록 |

```bash
cd v5
python build.py        # prod 설정 → v5/dist/, v5/index.html, v5/screen/index.html
python build.py dev    # dev 설정  → v5/dev/index.html, v5/dev/screen/index.html
```

배포 주소: **`jaealee.com/test/hanok/v5`** (개발용은 `…/v5/dev/`)

---

## 1. 이 폴더의 목적

**Supabase 를 붙이는 것.** 결정은 전부 `work/7차_작업지시.md` 에 있습니다 — 거기 적힌 것은 다시 묻지 않고, 안 적힌 것이 애매하면 멈추고 묻습니다.

순서(지시서 9장): A 파일만 → B 읽기 → C 쓰기 → D TV → E 계정 → F 백업. 묶음 하나 끝날 때마다 빌드·확인·`work/PROGRESS.md` 한 줄·보고.

---

## 2. 코드 규칙 (v1~v4 와 동일)

상위 `../CLAUDE.md` 2장을 그대로 따릅니다.

- **구형 스마트TV 금지 문법** — `?.` `??` `.flat()` `.replaceAll()` `structuredClone`, CSS 는 `inset:` `backdrop-filter` `color-mix()` `:has()`. `fetch`·`Promise`·`async/await` 는 이미 쓰고 있으니 됩니다
- 배율은 `zoom`, `transform:scale` 금지
- **경고는 막지 않고 알리기만** (설계 원칙). 예외는 읽기 전용(진짜로 저장이 불가능할 때)뿐 — 그때도 이유를 말합니다
- 주석은 한국어로, '왜' 를 쓰기
- 흉내 표시(`.mockbar` `.sb-mock` `.lk-open`) 지우지 마세요
- 나타났다 사라지는 요소는 **자리를 미리 잡아 두고 보이기만** 바꾸기
- **예약 객체 모양을 바꾸지 않습니다.** 행 ↔ 객체 변환은 `rowToRes` / `resToRow` 두 함수에서만
- supabase-js · Realtime · Edge Function 안 씀. `fetch` 로 REST·Auth 직접 호출(`sb()` 헬퍼 하나)
- 파일 크기 증가 200KB 이상 금지

### 손님 화면 관련

- `tv-mode-list` / `tv-mode-grid` — **`tv-grid` 는 안쪽 격자가 이미 쓰는 이름입니다**
- `adUrl()` — TV 는 `screen/` 주소로 엽니다. 상대 경로를 그대로 쓰면 영상이 안 나옵니다
- 영상은 **절대 base64 로 넣지 마세요.** 별도 파일 + H.264
- TV 는 로그인 없이 공개 뷰(`public_today` / `public_screen`)만 읽습니다. 전화·요청사항·메모는 뷰에 넣지 않습니다

### 관리 화면 주소 (6차-K)

`#/hanok` `#/hanok/settings` `#/hanok/YYYY-MM-DD` — 상태→주소는 `syncHash`(그릴 때마다), 주소→상태는 `applyAdminRoute`(로드·hashchange). 디스플레이는 `#/screen/hanok` 또는 `screen/` 폴더.

---

## 3. 한 단계 끝날 때마다

1. `python build.py` (그리고 필요하면 `python build.py dev`) — `구형 브라우저 문법 검사 통과`
2. 네 폭(430/820/1280/1920) + 손님 화면(1920) 확인. **추측하지 말고 직접 보세요.** 스크린샷은 `python work/shot.py` 방식(헤드리스 크롬), 동작은 브라우저에서 JS 로
3. `work/PROGRESS.md` 에 한 줄
4. 멈추고 보고
