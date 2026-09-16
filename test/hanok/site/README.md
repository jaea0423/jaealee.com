# 한옥반점 가게 사이트 (`test/hanok/site/`)

정적 파일 — 빌드 없음. 다섯 장: `index.html`(홈) · `about.html`(이야기·공간) · `menu.html`(차림) · `visit.html`(오시는 길) · `reserve.html`(예약 접수).
공통: `css/site.css` + `js/site.js`(상단·바닥·알림 팝업을 넣고 장별 내용을 그림) + `data/menu.js` + `img/` + `fonts/`.
관리 화면(v7)과 다른 물건: 구형 TV 제약 없음, 폰 우선, 현대 CSS.

- 메뉴·룸·영업시간·주소·알림(NOTICE)·대표 요리(SIGNATURE)는 `data/menu.js` 한 곳. 바꿀 때 여기만.
- **가격은 화면에 안 씀** — 메뉴판 PDF(`menu.pdf`, `INFO.menuPdf`)에서만. data 의 price 는 남겨 둠(나중에 쓸 수 있게).
- 알림 팝업은 `NOTICE` — `until` 지나면 자동으로 안 뜸, 세션에 한 번만.
- 사진은 `img/` — 지금은 관리 화면 배경 7장 + 전경 1장(임시). 룸 사진 6장·음식 사진은 재아가 채움.
- 예약 접수 폼은 **시안** — 아직 저장하지 않음. 붙일 때: Supabase RPC(anon insert + 횟수 제한) → 관리 화면 '손님 요청' 경로 → 사장 확정 → 문자.
- `?shot=1` 은 전체 페이지 스크린샷용(첫 화면 높이 고정).
