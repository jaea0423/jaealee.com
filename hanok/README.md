# 한옥반점 가게 사이트 (`hanok/` — 주소 jaealee.com/hanok)

정적 파일 — 빌드 없음. 여섯 장: `index.html`(홈) · `about.html`(이야기) · `space.html`(공간) · `menu.html`(차림) · `visit.html`(오시는 길) · `reserve.html`(예약).
공통: `css/site.css` + `js/site.js`(상단·바닥·팝업을 넣고 장별 내용을 그림) + `js/reserve.js`(예약 창) + `img/` + `fonts/`.
관리 화면(system/)과 다른 물건: 구형 TV 제약 없음, 폰 우선, 현대 CSS.

## 내용은 어디서 오나 (2026-09-16 1단계)

- **`data/site.js`** — 글·사진·팝업·차림·영업시간·연락처 **전부의 기본값** 한 객체(`SITE_DEFAULT`). 서버가 없어도 이걸로 뜹니다.
- **`js/content.js`** — 서버 `site_versions`(적용한 판, `apply_at ≤ 지금` 인 최신) 값을 기본값 위에 덮어 `window.SITE` 로 둠. `?preview=1` 이면 `site_draft`(초안)를 읽고 위에 빨간 띠.
  마지막 값은 localStorage 에 두고 다음 방문 때 먼저 씀. 값이 정해질 때까지 `html.pending` 으로 본문을 잠깐 숨김(1.5초 넘으면 그냥 보임).
- **HTML 의 글은 대비용** — JS 가 꺼졌을 때·검색엔진용. 실제로는 `data-t`(글) `data-paras`(문단들) `data-img`(사진) `data-list`(목록) 표시가 붙은 자리를 `SITE` 값으로 다시 채웁니다.
  글 안의 `**굵게**` 는 굵은 글씨, 줄바꿈은 그대로 `<br>`. 사진은 `img/` 파일명 또는 전체 주소(관리 화면에서 올린 것).
- 예약 시스템 설정 → **홈페이지 → 홈페이지 관리 열기**(`system/src/js/14b-site-admin.js`)가 초안(`site_draft`)을 고치고 → 미리보기(`?preview=1`) → 적용(지금/예약)하면 `site_versions` 에 한 판 쌓입니다. 표는 `system/supabase/patch_10차_홈페이지관리.sql`.
- `online` 묶음(받기/중단·며칠 앞까지·성인 최소·최대 인원·룸 성인 최소·제한 시간)은 `js/reserve.js` 가 읽습니다. 서버 정책(성인 2~12·룸 성인 5·내일부터)이 상한이라 그 안에서 좁히기만 됩니다.
- 옛 전역 이름(`MENU` `ROOMS` `HOURS` `NOTICES` `INFO` …)은 `applySiteGlobals()` 가 `SITE` 에서 채워 줍니다 — `reserve.js` 가 그 이름으로 읽음.

## 기타

- **가격은 화면에 안 씀** — 메뉴판 PDF(`menu.pdf`, `info.menuPdf`)에서만. data 의 price 는 남겨 둠.
- 팝업(`notices`)은 `until` 지나면 자동으로 안 뜸, 닫으면 그 세션 동안(새로고침이면 다시), '오늘 하루' 는 그날.
- 예약 창은 `js/config.js`(window.SUPA) 가 있으면 진짜로 동작 — `public_avail` 읽기·`requests` 접수(서버 정책이 규칙·횟수 제한). 없으면 흉내. 문자·인증번호는 아직 흉내.
- `?shot=1` 은 전체 페이지 스크린샷용(`python work/shot.py`, 8767 서버 필요).
