# jaealee.com

개인 홈페이지와 자료실, 날짜별 콘텐츠, 개별 웹 프로젝트를 함께 관리하는 저장소입니다.
웹 폴더 이름은 공개 주소와 연결되므로, 용도가 비슷하다는 이유만으로 이동하지 않습니다.

## 폴더 안내

| 구분 | 위치 | 용도 |
|---|---|---|
| 첫 화면 | `index.html`, `jaea.jpeg`, `CNAME` | 루트 소개 화면·이미지·도메인 |
| 통합 홈 | `home/` | 홈·자료실·뉴스·지식·기회·프로젝트 화면과 공통 렌더링 |
| 학습 자료 | `drive/` | 과목별 강의 자료. `archive/`도 기존 주소를 유지하는 보관 자료 |
| 날짜별 콘텐츠 | `news/`, `knowledge/`, `opportunities/` | 원고 JSON·목록·과거 뉴스 HTML |
| 개별 사이트 | `projects/`, `boyeoii/`, `hogu/`, `sister/`, `yb/` | 각 경로로 접근하는 프로젝트와 개인 페이지 |
| 공유 중인 테스트 | `test/` | 외부에 전달한 주소 포함. 전체 경로와 파일 보존 |
| 운영 | `automation/`, `bot/`, `supabase/` | 콘텐츠 발행·텔레그램 봇·DB 설정 자료 |
| 프로젝트 문서 | `docs/projects/` | 페이지 실행과 분리된 기획·설명 문서 |
| 비활성 보관함 | `_disabled/` | 사용 중단이 확인된 파일을 원형으로 보존. [관리 방법](_disabled/README.md) |

## 관리 기준

- 화면 수정은 `home/` 중심으로 진행하고 날짜별 원고·목록은 콘텐츠 자동화 작업과 충돌하지 않게 관리합니다.
- 화면 발행일은 `home/edition-day.js`의 한국시간 07시 경계를 사용합니다.
- `/test`는 외부 공유 중입니다. 이번 정리에서 내부 작업물·이미지·하위 버전까지 모두 보존했습니다. 별도 명시 요청 없이 이동·이름 변경·삭제하지 않습니다.
- 링크가 검색되지 않는 것만으로 파일이 불필요하다고 판단하지 않습니다. 외부에 전달한 주소일 수 있습니다.
- 과거 뉴스 HTML은 홈의 구형 보관본 표시에서 사용하므로 유지합니다.
- 신규 기획 문서는 `docs/projects/`에, 사용 중단이 확인된 항목은 `_disabled/`에 둡니다. 상세 이력과 원래 위치는 보관함 안내에 기록합니다.
- `automation/`·`bot/` 실행 경로와 공개 페이지의 상대경로는 유지합니다.

## 작업 지침

[AGENTS.md](AGENTS.md)를 먼저 확인합니다. 자동 발행은 [automation/README.md](automation/README.md)와 [automation/DAILY.md](automation/DAILY.md)를 따릅니다.

## 정리 기록 — 2026-09-12

- 루트의 `study-potato-overview.docx`를 `docs/projects/study-potato-overview.docx`로 이동했습니다. 문서 내용은 변경하지 않았습니다.
- 공개 페이지·자료·운영 폴더를 역할별로 설명하고, 기존 `_disabled/`를 비활성 보관함으로 명시했습니다.
