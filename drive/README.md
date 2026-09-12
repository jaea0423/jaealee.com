# 자료실 선택 화면

## 수정 범위

- 현재 학기 과목: `ai`, `algorithm`, `english`, `privacy-crypto`, `privacy-law`, `secure-coding`.
- 각 과목의 `index.html`은 과목 메뉴와 수업·교수·시간 정보를 표시합니다.
- 각 과목의 `lecture/index.html`은 주차·차시를 선택하는 목록입니다.
- `english/team-project/index.html`은 자료 등록 전 안내입니다.
- 공통 디자인은 `navigation.css`, 등록 상태 확인은 `navigation.js`에서 관리합니다.

실제 `lecture/weekXX/`의 수업 HTML·PDF·기타 자료는 목록 정리 대상이 아닙니다. `archive/`는 본문이 들어 있는 index도 있으므로 일괄 변경하지 않습니다. `drive/index.html`의 홈 자료실 이동과 기존 상대경로를 유지합니다.

## 자료 등록

기존 주차·차시 경로에 파일을 올리면 목록에서 HEAD 요청으로 존재 여부를 확인합니다. 404는 준비 중으로 표시하고 이동을 막으며, 성공하면 링크를 활성화합니다. 통신 실패나 서버 오류는 파일 부재로 단정하지 않고 기존 상태를 보존합니다. JavaScript가 없는 환경에서는 원래 링크가 유지됩니다.

## 검증

- `node --check drive/navigation.js`
- 저장소 루트를 로컬 HTTP 서버로 열어 과목·주차 목록을 데스크톱과 모바일 너비에서 확인합니다.
- 수업 정보 펼치기, 상위 경로 이동, 실제 차시 열기, 미등록 항목의 이동 차단을 확인합니다.
- 실제 수업 파일과 `/test`에 변경이 없는지 확인하고, 이번 작업 파일만 커밋합니다.
- 공통 CSS·JS 변경 시 목록 HTML의 버전 문자열도 갱신합니다.
