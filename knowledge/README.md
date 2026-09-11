# 지식 더하기 콘텐츠

화면: `/home/#knowledge`. 날짜 공유: `/home/#knowledge/YYYY-MM-DD`. 개별 코너: 날짜 뒤에 `/basic`, `/deep`, `/sentence`.

## 발행 파일

- `data/YYYY-MM-DD.json`: 호 날짜(date), 실제 작성 완료 시각(generatedAt), articles 3개.
- `index.json`: 공개한 날짜와 글의 제목·분야·핵심 개념·학습 내용. 보관함과 과거 주제 검토에 사용합니다.
- 새 콘텐츠와 목록을 함께 커밋합니다. 아직 검증하지 않은 초안은 목록에 추가하지 않습니다.
- 화면은 한국 날짜를 기준으로 미래 발행분을 목록에서 제외하며, 기본 화면에는 가장 최근의 발행분을 보여줍니다.

## 기사 형식

각 글: `kind`(basic/deep/sentence), `label`, `category`, `readingTime`, `title`, `concepts`, `learning`, `blocks`, `sources`.

기초·심화에는 `summary`와 선택적인 `takeaway`를 사용합니다. 문장에는 `quote`, `quoteOriginal`, `author`, `attribution`을 기록합니다. sources 항목은 `title`, `url`이며 https 원문을 연결합니다.

blocks:

- paragraph / heading: `text`
- table: `caption`, `headers`, `rows`
- fraction: `numerator`, `denominator`, `result`, `label`(접근성 설명). 화면에서 MathML 분수로 표시합니다.

모든 값은 일반 텍스트로 저장합니다. 본문에 HTML이나 Markdown을 넣지 않습니다. 다른 수식 구조가 필요하면 렌더러의 구조화된 수식 지원을 확장하고 검증해야 합니다.

## 편집·검증

발행 전 전체 index와 유사한 과거 글 본문을 읽고 핵심 질문·개념 중복을 확인합니다. 전날 분야를 피하고 최근 7개 발행일의 분포를 검토합니다. 단순 문자열 검사만으로 의미 중복 검증을 대체하지 않습니다.

현재 목록은 과거 비교에 필요한 기록 구조이며, AI 주제 선정·의미 중복 판정·예약 발행 기능 자체는 아직 연결하지 않았습니다.

첫 발행분은 2026-09-11입니다. 윤년 계산과 심슨의 역설 가상 자료를 직접 검산했습니다. 인용문은 MIT의 Elizabeth Carter 영어 번역 1절을 바탕으로 직접 한국어로 번역했습니다. Royal Museums Greenwich 자료 중 오래된 ‘다음 윤년’ 안내는 사용하지 않고 지속적으로 성립하는 달력 규칙만 참고했습니다.

## 보충 발행 기록

2026-09-01~10호는 2026-09-11에 보충 작성했습니다. 각 파일에 backfilled, publicationNote와 실제 generatedAt을 기록했습니다. 호 날짜를 과거 실제 작성 시각으로 간주하지 않습니다. 기존 11호 원고는 보존했습니다. 총 11호·33편이며 인접한 날의 기초·심화 분야가 반복되지 않도록 배치했습니다.
