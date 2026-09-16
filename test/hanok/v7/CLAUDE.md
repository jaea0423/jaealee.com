# v7 — 전수조사 · 구조 정리 작업 폴더

**여기가 작업 공간입니다. `../v6` 와 그 위는 전부 읽기 전용입니다.**
v6 는 8차(좌석·세션 개편) 끝 상태로 동결(2026-09-15). v7 는 그 복사본에서 시작해 **보안·오류 전수조사, 불필요한 코드 제거, 파일 나누기**를 합니다.

---

## 0. 무엇이 어디에 있나

| 경로 | 상태 |
|---|---|
| `../v6/` 와 그 위 | **읽기만** |
| `../assets/*.b64` `../v4/assets/*.b64` | **읽기만.** 빌드가 이미지·글꼴을 여기서 가져옵니다 |
| `v7/src/page.html` | HTML 뼈대. `__CSS__` `__JS__` 자리에 아래 조각이 들어갑니다 |
| `v7/src/css/NN-이름.css` | CSS 조각 — **이름 순서대로** 이어 붙습니다(순서가 곧 우선순위) |
| `v7/src/js/NN-이름.js` | JS 조각 — 이름 순서대로 이어 붙습니다. 전부 한 `<script>` 안이라 서로 전역으로 봅니다 |
| `v7/build.py` | 조각을 합쳐 HTML 하나로. `__SUPA_CFG__` 에 설정 파일을 끼웁니다 |
| `v7/work/patchlib.py` | 패치 스크립트 공용(`load/save/rep/where/js_check`) |
| `v7/work/index.v6.html` | 나누기 전 원본(참고용, 고치지 않음) |
| `v7/supabase/` `v7/backup/` | v6 그대로 |

```bash
cd v7
python build.py        # prod → dist/, index.html, screen/index.html
python build.py dev    # dev  → dev/index.html, dev/screen/index.html
```

배포 주소: **`jaealee.com/test/hanok/v7`** (개발용은 `…/v7/dev/`). 배포 형태는 여전히 **HTML 파일 하나**입니다.

---

## 1. 이 폴더의 목적 (순서대로)

1. **파일 나누기** — 끝. `src/index.html` 1만 줄 → `page.html` + css 14조각 + js 20조각. 빌드 결과는 v6 와 같음(빈 줄만 다름)
2. **보안 전수조사** — `work/전수조사.md` 에 항목·결과
3. **오류 전수조사** — 정적 검사(정의 안 된 함수·안 쓰는 함수·중복 정의) + 화면 시나리오
4. **불필요한 코드 제거** — 비활성(직원·근태·매출) 주석 코드, 안 쓰는 함수, 덮어쓰기 CSS 정리
5. 그 다음에 디자인

묶음 하나 끝날 때마다 빌드·확인·`work/PROGRESS.md` 한 줄·보고.

---

## 2. 코드 규칙 (v1~v6 와 동일)

상위 `../CLAUDE.md` 2장을 그대로 따릅니다.

- **구형 스마트TV 금지 문법** — `?.` `??` `.flat()` `.replaceAll()` `structuredClone`, CSS 는 `inset:` `backdrop-filter` `color-mix()` `:has()` `:is()` `@container`
- 배율은 `zoom`, `transform:scale` 금지
- **경고는 막지 않고 알리기만** (설계 원칙)
- 주석은 한국어로, '왜' 를 쓰기
- 흉내 표시(`.mockbar` `.sb-mock` `.lk-open`) 지우지 마세요
- 나타났다 사라지는 요소는 **자리를 미리 잡아 두고 보이기만** 바꾸기
- **예약 객체 모양을 바꾸지 않습니다.** 행 ↔ 객체 변환은 `rowToRes` / `resToRow` 두 함수에서만
- **날짜가 정해진 계산은 `store().settings` 말고 `settingsAt(date)`(좌석은 `roomsAt(date)`·`joinsAt(date)`, 코스는 `courseGroups(date)`)** — 예정 설정(`03b-scheduled.js`)이 그 날짜에 유효한 값을 돌려줍니다. id 로 좌석을 찾을 땐 `seatById`(예정 좌석까지 찾음)
- supabase-js · Realtime · Edge Function 안 씀. `fetch` 로 REST·Auth 직접 호출(`sb()` 헬퍼 하나)
- service_role 키는 어떤 파일에도 쓰지 않음(build.py 가 막음). PIN 은 화면 4자리, 서버 비밀번호 = PIN+"00"

### 손님 화면 관련

- `tv-mode-list` / `tv-mode-grid` — **`tv-grid` 는 안쪽 격자가 이미 쓰는 이름입니다**
- `adUrl()` — TV 는 `screen/` 주소로 엽니다. 영상은 base64 로 넣지 않음, `screen/ad.mp4`
- TV 는 로그인 없이 공개 뷰(`public_today` / `public_screen`)만 읽습니다. 전화·요청사항·메모는 뷰에 넣지 않습니다

### 조각을 고칠 때

- 어느 조각인지 모르면 `python -c "import work.patchlib as L; print(L.where('function 이름('))"`
- 조각 사이 순서를 바꾸지 마세요 — CSS 는 뒤가 이기고, JS 는 `const`/`let` 선언 순서에 걸립니다
- 새 조각을 만들 때는 번호를 사이에 끼웁니다(예 `07b-…`). 앞 번호를 다시 매기지 않습니다

---

## 3. 한 단계 끝날 때마다

1. `python build.py` (그리고 `python build.py dev`) — `구형 브라우저 문법 검사 통과`
2. 네 폭(430/820/1280/1920) + 손님 화면 확인. 스크린샷 `python work/shot.py`, 동작은 브라우저에서 JS 로(dev 사이트 `http://127.0.0.1:8767/v7/dev/`)
3. `work/PROGRESS.md` 에 한 줄
4. 멈추고 보고
