# 2025_강원대_시큐어코딩_5주차_2차시_vF

<!-- p.1 -->

OAuth2 인증 및 인가
01 OAuth2 이해
02 OAuth2 구현
03 OAuth2 보안 위협 및 해결 방법

---

<!-- p.2 -->

학습 목표
OAuth2 개념과 필요성을 이해하고 설명할 수 있다.
OAUth2 프로세스 및 구성요소를 이해하고, 구현할 수 있다.
OAuth2 보안 위협을 이해하고 이에 대한 해결 방안을 설명할 수 있다.

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 원문 표기 그대로 — 두 번째 목표의 "OAUth2"는 "OAuth2"의 대소문자 오타로 보임)

---

<!-- p.3 -->

학습 내용
1. OAuth2 개념
2. OAuth2 구현
3. OAuth2 보안 위협 및 해결방법

---

<!-- p.4 -->

OAuth2 인증 및 인가
01 OAuth2 이해
02 OAuth2 구현
03 OAuth2 보안 위협 및 해결 방법

---

<!-- p.5 -->

OAuth2 란?
정의
OAuth(Open Authorization)는 클라이언트 애플리케이션이 특정 리소스 소유자를 대신하여 서버 리소스에 액세서할 수 있는 권한
부여를 위한 개방형 표준.
사례)
사용자가 Google 계정을 이용해서 타사앱(B사의 애플리케이션)에 로그인하거나 데이터 공유
사용자가 GitHub 계정을 이용하여 CI/CD 툴(Jenkins)과 연동

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 원문 표기 그대로 — "액세서할"은 "액세스할"의 오타로 보임)

[이미지] 슬라이드 오른쪽 아래에 OAuth 2 로고(원형 배지 안에 큰 숫자 "2", 테두리에 "OAUTH" 글자)가 장식으로 들어 있음.

---

<!-- p.6 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## OAuth2 주요 구성요소

[도식] 네 구성요소와 그 사이 점선 화살표로 이루어진 관계도

| 구성요소 | 위치 | 설명 |
|---|---|---|
| **클라이언트 애플리케이션 (Client)** (APP 톱니바퀴 아이콘) | 왼쪽 위 | 리소스 소유자의 데이터를 요청하는 애플리케이션 (예: 모바일앱, 웹앱) |
| **리소스 서버 (Resource Server)** (노란색 서버 2대 아이콘) | 오른쪽 위 | 실제데이터를 가지고 있으며, 발급된 토큰을 검증하여 클라이언트의 요청을 허용하는 서버 |
| **리소스 소유자 (Resource Owner)** (사람 + 노트북·휴대폰 아이콘) | 왼쪽 아래 | 사용자(User) 또는 서비스, 리소스 (예: Google Drive, Github 등) |
| **권한서버 (Authorization Server)** (파란색 서버 아이콘) | 오른쪽 아래 | 인증을 수행하고 토큰을 발급하는 서버 (예: Google, Github, Facebook 등) |

화살표(점선) 흐름:
- 리소스 소유자 → 클라이언트 애플리케이션 : **서비스 액세스**
- 리소스 소유자 → 권한서버 : **액세스 권한**
- 권한서버 → 클라이언트 애플리케이션 : **인가코드/ 액세스 토큰 발급**
- 클라이언트 애플리케이션 → 리소스 서버 : **데이터 액세스**
- 리소스 서버 → 권한서버 : **대리인 인증권한 확인**

---

<!-- p.7 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## OAuth2 구성 요소

| 참여자 | 설명 | 역할 |
|---|---|---|
| 클라이언트 애플리케이션 (Client Application) | 리소스 소유자를 대신해 보호된 리소스에 접근하려는 애플리케이션 | 사용자 인증 및 권한 부여를 받아, Access Token을 획득하여 리소스 서버에 접근 |
| 리소스 소유자 (Resource Owner) | 리소스(데이터)를 소유한 사용자 | 자신의 리소스에 접근할 수 있도록 권한을 부여 |
| 권한 서버 (Authorization Server) | 사용자 인증과 권한 부여를 처리하고, Access Token을 발급하는 서버 | 클라이언트의 인증 요청을 검증하고, 적절한 Authorization Grant 또는 Access Token을 발급 |
| 리소스 서버 (Resource Server) | 보호된 리소스를 보유하고 있는 서버 | 클라이언트가 제출한 Access Token의 유효성을 확인한 후, 접근 요청에 따라 리소스를 제공 |

---

<!-- p.8 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## OAuth2 인증 흐름 : Authorization Code Grant

[도식] 네 참여자 사이를 번호 붙은 파란 화살표로 연결
- 왼쪽: 사용자 (Resource Owner)
- 가운데(APP 아이콘): 클라이언트 애플리케이션 (Client)
- 오른쪽 위: 리소스 서버 (Resource Server)
- 오른쪽 아래: 권한서버 (Authorization Server)

| 단계 | 방향 | 내용 |
|---|---|---|
| ① | 사용자 → 클라이언트 | 서비스 접근 |
| ② | 클라이언트 → 권한서버 | 인증 요청 페이지 redirect |
| ③ | 권한서버 → 사용자 | redirect된 페이지를 통해 로그인 요청 |
| ④ | 사용자 → 권한서버 | 로그인 정보 입력 |
| ⑤ | 권한서버 → 클라이언트 | Authorization Code 발급 |
| ⑥ | 클라이언트 → 권한서버 | Access Token 요청 |
| ⑦ | 권한서버 → 클라이언트 | Access Token 발급 |
| ⑧ | 클라이언트 → 리소스 서버 | Access Token으로 사용자 리소스 요청 |
| ⑨ | 리소스 서버 → 권한서버 | Access Token 검증 |
| ⑩ | 권한서버 → 리소스 서버 | Access Token 검증 OK |
| ⑪ | 리소스 서버 → 클라이언트 | 요청한 리소스 제공 |
| ⑫ | 클라이언트 → 사용자 | 보호된 서비스 이용 |

(②·⑥은 클라이언트→권한서버 방향 같은 화살표에, ⑤·⑦은 권한서버→클라이언트 방향 같은 화살표에 함께 표기됨. ⑤의 Authorization Code는 실제로는 다음 슬라이드처럼 사용자 브라우저의 redirect를 거쳐 클라이언트에 전달되며, 이 도식은 이를 단순화해 표현함)

---

<!-- p.9 -->

OAuth2 인증 흐름 : Authorization Code Grant

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[도식] Authorization Code Grant 시퀀스 다이어그램 (영문). 참여자(왼쪽→오른쪽): **User**, **UserAgent (Browser)**, **Web Server (Client App)**, **Authorization Server**, **Resource Server**

| # | 보내는 쪽 → 받는 쪽 | 메시지 |
|---|---|---|
| 1 | User → UserAgent (Browser) | Enter URL |
| 2 | UserAgent → Web Server (Client App) | Open URL |
| 3 | Web Server → Web Server (자기 자신) | Start OAuth Process |
| 4 | Web Server → UserAgent | Redirect to AuthZ Server |
| 5 | UserAgent → Authorization Server | Opens redirect URL |
| 6 | Authorization Server → UserAgent | Present Authorization UI |
| 7 | UserAgent → User | Present Authorization UI |
| 8 | User → UserAgent | Present credentials and authorise or deny |
| 9 | UserAgent → Authorization Server | Present submitted data from user |
| 10 | Authorization Server → Authorization Server (자기 자신) | Verify and create Authorization code |
| 11 | Authorization Server → UserAgent | Redirect to Web Server with Authorization Code |
| 12 | UserAgent → Web Server | Follow redirect to Web Server |
| 13 | Web Server → Authorization Server | Present Authorization Code |
| 14 | Authorization Server → Web Server | Return Access Token |
| 15 | Web Server → Resource Server | Call protected resource with Access Token |
| 16 | Resource Server → Web Server | Return protected resource |

(※ 원문 표기 그대로 — "authorise"는 영국식 철자)
(앞 슬라이드 ①~⑫와의 대응: 1~2 ≈ ①, 4~5 ≈ ②, 6~7 ≈ ③, 8~9 ≈ ④, 11~12 ≈ ⑤, 13 ≈ ⑥, 14 ≈ ⑦, 15 ≈ ⑧, 16 ≈ ⑪. 이 다이어그램에는 ⑨⑩ 토큰 검증 단계가 따로 그려져 있지 않음)

---

<!-- p.10 -->

OAuth2 의 장단점
OAuth2의 장점
〮 비밀번호 노출 위험 감소
사용자 비밀번호를 클라이언트에 전달하지 않고, 권한 서버에서만 관리하므로 보안성이 향상됨
〮 SSO (Single Sign-On) 지원
한 번의 로그인으로 여러 애플리케이션에 접근할 수 있어 사용자 편의성이 높아짐
〮 토큰 기반 인증
Access 토큰과 Refresh 토큰을 활용하여, 세션 관리 및 권한 검증을 효과적으로 수행,
유효기간을 짧게 운영하여 토큰 탈취 피해가 발생하더라도 피해를 최소화함
〮 다양한 클라이언트 지원
웹, 모바일, API 등 여러 클라이언트에 대해 유연하게 적용 가능하며, 확장성이 뛰어남
〮 외부 인증 연동 용이
소셜 로그인 및 다른 제3자 인증 시스템과 쉽게 통합

---

<!-- p.11 -->

OAuth2 의 장단점
OAuth2 단점
〮 구현 복잡성
다양한 인증 흐름(Authorization Code, Implicit, Client Credentials 등)과 토큰 관리가 복잡하여 잘못 구현될 경우
보안 취약점이 발생할 수 있음
〮 클라이언트 비밀 관리 문제
모바일이나 공개 클라이언트의 경우, 태생적으로 클라이언트에 보관하는 토큰 등을 완벽하게 보호하기 어려움
〮 표준 해석의 차이
OAuth2는 표준 자체가 다소 유연하게 되어 있어서, 연동 시스템 간 구현의 차이 발생할 수 있음
〮 추가 보안 고려 필요
PKCE, 토큰 취소(Revocation), 타임스탬프/Nonce 등 추가 보안 대책이 없으면 리플레이 공격, 토큰 탈취 등의 위험이 존재
〮 서버 간 신뢰 관계 구성 필요
인증 서버와 리소스 서버 간의 신뢰가 깨지지 않도록 보안 구성이 탄탄하지 않으면 전체 시스템 보안이 위험할 수 있음

---

<!-- p.12 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## OAuth 와 OAuth2 비교

| 구분 | OAuth | OAuth2 |
|---|---|---|
| 보안 방식 | · 서명 기반 인증: 각 요청마다 HMAC-SHA1 등으로 서명을 생성하여 전송<br>· 별도의 전송 보안 없이도 일정 수준의 보안 제공 | · 토큰 기반 인증: Access Token과 Refresh Token을 활용<br>· HTTPS/TLS를 기본 전제 보안 수단으로 사용하여 전송 보안을 확보 |
| 구현 복잡성 | · 서명 계산 및 검증 과정으로 인해 구현 난이도가 높음<br>· 클라이언트와 서버 모두에서 복잡한 암호화 로직 필요 | · 서명 계산 없이 토큰을 사용하기 때문에 구현이 간단함<br>· 다양한 인증 흐름(Authorization Code, Implicit, Client Credentials, Resource Owner Password Credentials 등) 지원 |
| 유연성 및 확장성 | · 표준이 다소 엄격하여 확장에 한계가 있음<br>· 일부 레거시 시스템에서 주로 사용 | · 현대 애플리케이션 환경(웹, 모바일, API 등)에 최적화된 유연한 설계<br>· 추가 보안 강화 (예: PKCE)를 통해 공개 클라이언트 보안 강화 가능 |

(※ 검증: Python hmac/hashlib로 HMAC-SHA1 출력 길이 확인 — 20바이트(160비트). OAuth 1.0의 서명 방식(HMAC-SHA1 등) 설명과 일치)

---

<!-- p.13 -->

OAuth2 인증 및 인가
01 OAuth2 이해
02 OAuth2 구현
03 OAuth2 보안 위협 및 해결 방법

---

<!-- p.14 -->

Google OAuth 클라이언트 생성
1. Google Cloud 가입 필요
https://cloud.google.com/apis?hl=ko

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[화면 캡처] 브라우저(Firefox)로 연 Google Cloud API 페이지
- 탭 제목: `Cloud API | Google Cloud`, 주소창: `https://cloud.google.com/apis?hl=ko`
- 상단 메뉴: Google Cloud 로고 | 개요 · 솔루션 · **제품**(선택됨, 밑줄) · 가격 책정 · 리소스 · 문의하기 | 검색 아이콘 · Docs · 지원 · 로그인 · [무료로 시작하기] 버튼
- 노란 배너: "Next '24를 놓치셨나요? 걱정하지 마세요. 이제 모든 세션을 주문형으로 이용할 수 있습니다. 지금 시청하세요. →"
- 본문 제목 **Google Cloud API**: "Google Cloud API를 사용하면 선호하는 언어를 사용하여 워크플로를 자동화할 수 있습니다. 널리 사용되는 프로그래밍 언어로 Cloud API를 REST 호출 또는 클라이언트 라이브러리와 함께 사용하세요." — 버튼 [Google Cloud 무료로 사용해 보기] [문서 보기]
- 오른쪽 상자 "다음으로 이동:" 클라우드 아키텍처 센터 / Cloud API 사용 / Google Cloud Marketplace
- 왼쪽 "필터링 기준 > 필터" 체크박스: AI 및 Machine Learning API, 컴퓨팅 API, 스토리지 및 데이터베이스 API, Networking API, 데이터 분석 API, 관리 도구 API
- 검색창("검색") 아래 **AI 및 Machine Learning API** 카드: Vertex AI API(최소한의 머신러닝 전문 지식과 수고로 고품질 커스텀 머신러닝 모델을 학습시킵니다.), 기반 모델 API(Vertex AI를 사용하여 특정 태스크에 맞게 조정하거나 맞춤설정할 수 있는 Gemini 모델을 비롯한 사전 학습된 멀티태스크 대규모 모델입니다.), Vision API(이미지 라벨 지정, 얼굴, 로고 및 랜드마크 인식, OCR, 선정적인 콘텐츠 인식 등을 앱에 통합합니다.), 그 아래 줄 Speech-to-Text API · Cloud Natural Language · Cloud Translation API(일부 잘림)
- 이 화면에서 오른쪽 위 '로그인'/'무료로 시작하기'로 Google Cloud 가입을 진행함

---

<!-- p.15 -->

Google OAuth 클라이언트 생성
2. 새 프로젝트 생성

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[화면 캡처 1 — 왼쪽] Google Cloud 콘솔 첫 화면 위에 뜬 **프로젝트 선택** 대화상자
- 탭 `환영합니다 – Google Cloud C...`, 주소창 `https://console.cloud.google.com/welcome?hl=ko&inv=1&invt=AbqlbA&organizationId=...`
- 상단 바: Google Cloud | [조직 없음] 프로젝트 선택기 | 검색창 "리소스, 문서, 제품 등 검색(/)" [검색]
- 대화상자: 제목 "프로젝트 선택", 검색칸 "프로젝트 및 폴더 검색", 탭 최근 · 별표표시됨 · **전체**(선택), 표 머리글 이름 | ID, 행 "조직 없음 | 0", 오른쪽 아래 [취소]
- **빨간 박스: 대화상자 오른쪽 위 [새 프로젝트] 버튼** → 클릭
- 뒤쪽 배경: "시작하기", "프로젝트를 만들...", [VM 만들기], "빠른 액세스" (API 및 서비스, Compute Engine, Cloud Storage, BigQuery) 등이 가려진 채로 보임

[화면 캡처 2 — 오른쪽] **새 프로젝트** 생성 양식
- 노란 경고: "projects 할당량이 12개 남았습니다. 할당량 증가를 요청하거나 프로젝트를 삭제하세요. 자세히 알아보기" / "Manage Quotas"
- **빨간 박스: 프로젝트 이름 \* = `OAuth2 Test`** (오른쪽 ? 도움말 아이콘)
- 그 아래 "프로젝트 ID: oauth2-test-452107. 나중에 변경할 수 없습니다. [수정]"
- 위치 \* : "조직 없음" [찾아보기] — "상위 조직 또는 폴더"
- **빨간 박스: [만들기] 버튼** (옆에 [취소])

(※ 검증: Python 정규식 `[a-z][a-z0-9-]{4,28}[a-z0-9]`로 프로젝트 ID `oauth2-test-452107` 확인 — 소문자로 시작·6~30자 규칙과 일치, 프로젝트 이름을 소문자·하이픈으로 바꾼 뒤 숫자 접미사가 붙은 형태)

---

<!-- p.16 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Google OAuth 클라이언트 생성

### 3. 서비스 동의 및 시작

**API 및 서비스 > OAuth 동의 화면 선택**

[화면 캡처 1 — 왼쪽] Google Cloud 콘솔(프로젝트 `OAuth2 Test` 선택됨)의 왼쪽 탐색 메뉴
- 메뉴 항목: Cloud 개요 > · 솔루션 > · (고정된 제품) · **API 및 서비스 >** · 결제 · IAM 및 관리자 · Marketplace · Compute Engine > · Kubernetes Engine >
- **빨간 박스 1: "API 및 서비스"** 항목 → 마우스를 올리면 하위 메뉴가 펼쳐짐
- 하위 메뉴: 사용 설정된 API 및 서비스 · 라이브러리 · 사용자 인증 정보 · **OAuth 동의 화면** · 페이지 사용 동의
- **빨간 박스 2: "OAuth 동의 화면"** 선택
- 뒤쪽 대시보드: 탭 대시보드 · 활동 · 추천, "프로젝트 정보 — 프로젝트 이름 OAuth2 Test", "→ 프로젝트 설정으로 이동", API 카드, "리소스" 카드 등(일부 가려짐)

**Google 인증 플랫폼에서 아직 구성하지 않았을 경우 '시작하기' 눌러 설정**

[화면 캡처 2 — 오른쪽] Google 인증 플랫폼 / 개요 화면
- 상단: Google Cloud | 프로젝트 `OAuth2 Test` | 검색창 "리소스, 문서, 제품 등 검색(/)" [검색]
- 경로: Google 인증 플랫폼 / 개요
- 왼쪽 메뉴: **개요**(선택됨) · 브랜딩 · 대상 · 클라이언트 · 데이터 액세스 · 인증 센터
- 본문 "OAuth 개요": (액자 속 점선 구름 그림) "**Google 인증 플랫폼이 아직 구성되지 않음** — 시작하여 애플리케이션의 ID를 구성하고 Google API 호출 및 Google 계정으로 로그인에 사용할 사용자 인증 정보를 관리하세요. 자세히 알아보기"
- **빨간 박스: [시작하기] 버튼** 클릭

---

<!-- p.17 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Google OAuth 클라이언트 생성

### 4. 프로젝트 구성

**앱 정보 > 앱 이름 : OAuth2 Test, 사용자 지원 이메일: 개인 메일 주소**

[화면 캡처 1 — 왼쪽] "프로젝트 구성" 마법사 1단계
- 탭 `프로젝트 구성 – Google 인증...`, 주소창 `https://console.cloud.google.com/auth/overview/create?hl=ko&inv=1&invt=AbqlbA&org...`
- 상단: Google Cloud | `OAuth2 Test` | 검색창에 "동의" 입력됨 [검색]
- 경로: Google 인증 플랫폼 / 개요 / 브랜딩 만들기
- 왼쪽 메뉴: 개요(선택) · 브랜딩 · 대상 · 클라이언트 · 데이터 액세스 · 인증 센터
- 단계: ❶ 앱 정보 → ❷ 대상 → ❸ 연락처 정보 → ❹ 완료, 맨 아래 [만들기] [취소]
- **빨간 박스: ❶ 앱 정보 영역**
  - 앱 이름 \* : `OAuth2 Test` — "동의를 요청하는 앱의 이름"
  - 사용자 지원 이메일 \* : `pineful@gmail.com` (드롭다운) — "사용자가 동의에 대해 문의하는 용도입니다. 자세히 알아보기"
  - [다음] 버튼

**대상 > 외부 선택**

[화면 캡처 2 — 오른쪽] 같은 마법사 2단계 (✔ 앱 정보 완료)
- ❷ 대상:
  - ○ 내부 ⓘ — "조직 내 사용자만 사용할 수 있습니다. 인증을 위해 앱을 제출할 필요는 없습니다. 사용자 유형 자세히 알아보기"
  - **빨간 박스: ◉ 외부 ⓘ (선택됨)** — "Google 계정이 있는 모든 테스트 사용자가 사용할 수 있습니다. 앱이 테스트 모드로 시작되고 테스트 사용자 목록에 추가된 사용자에게만 제공됩니다. 앱을 프로덕션에 푸시할 준비가 되면 앱을 인증해야 할 수도 있습니다. 사용자 유형 자세히 알아보기"
  - **빨간 박스: [다음] 버튼**
- 이어서 ❸ 연락처 정보, ❹ 완료

(캡처 속 메일 주소는 강사 본인 계정 예시이며, 실습 시에는 자신의 메일 주소 입력)

---

<!-- p.18 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Google OAuth 클라이언트 생성

### 4. 프로젝트 구성

**연락처 정보: 개인 메일 주소**

[화면 캡처 1 — 왼쪽] "프로젝트 구성" 마법사 3단계 (주소창 `https://console.cloud.google.com/auth/overview/create?hl=ko&inv=1&invt=AbqlbA&org...`, 경로 Google 인증 플랫폼 / 개요 / 브랜딩 만들기)
- ✔ 앱 정보, ✔ 대상 완료
- **빨간 박스: ❸ 연락처 정보 영역**
  - 이메일 주소 \* : `pineful@gmail.com` (칩 형태, ⊗ 삭제 표시) — "이 이메일 주소는 Google에서 프로젝트 변경사항에 대해 알림을 보내기 위한 용도입니다."
  - [다음] 버튼
- ❹ 완료, 하단 [만들기] [취소]

**'만들기' 버튼 선택**

[화면 캡처 2 — 오른쪽] 마법사 4단계
- ✔ 앱 정보, ✔ 대상, ✔ 연락처 정보
- ❹ 완료: ☑ "Google API 서비스: 사용자 데이터 정책에 동의합니다." (체크됨) → [계속]
- **빨간 박스: 하단 [만들기] 버튼** (옆에 취소)

---

<!-- p.19 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Google OAuth 클라이언트 생성

### 5. 클라이언트 만들기

**클라이언트 > + CREATE CLIENT 선택**

[화면 캡처 1 — 왼쪽] Google 인증 플랫폼 / 클라이언트 화면
- 탭 `클라이언트 – Google 인증 플랫...`, 주소창 `https://console.cloud.google.com/auth/clients?hl=ko&inv=1&invt=AbqlbA&organization...`
- 상단: Google Cloud | `OAuth2 Test` | 검색창 "사용자 인증 정보" [검색], 알림 배지 ②
- 왼쪽 메뉴: 개요 · 브랜딩 · 대상 · **클라이언트**(선택) · 데이터 액세스 · 인증 센터
- 툴바: 클라이언트 | **빨간 박스: [+ CREATE CLIENT]** | 🗑 삭제 | ↶ 삭제된 OAUTH 클라이언트 복원
- "OAuth 2.0 클라이언트 ID" 표 (이름 | 생성일 ↓ | 유형 | 클라이언트 ID | 작업): "표시할 OAuth 클라이언트가 없습니다."

**OAuth 클라이언트 ID 만들기**

[화면 캡처 2 — 가운데] 경로 Google 인증 플랫폼 / 클라이언트 / 클라이언트 만들기, 주소창 `https://console.cloud.google.com/auth/clients/create?hl=ko&inv=1&invt=AbqlbA&organ...`
- 제목 "← OAuth 클라이언트 ID 만들기"
- 안내: "클라이언트 ID는 Google OAuth 서버에서 단일 앱을 식별하는 데 사용됩니다. 앱이 여러 플랫폼에서 실행되는 경우 각각 자체 클라이언트 ID가 있어야 합니다. 자세한 내용은 OAuth 2.0 설정을 참조하세요. OAuth 클라이언트 유형을 자세히 알아보세요."
- 애플리케이션 유형 \* : **웹 애플리케이션** (드롭다운, 파란 테두리로 포커스)
- 이름 \* : `웹 클라이언트 1` — "OAuth 2.0 클라이언트의 이름입니다. 이 이름은 콘솔에서 클라이언트를 식별하는 용도로만 사용되며 최종 사용자에게 표시되지 않습니다."
- ⓘ "아래에 추가한 URI의 도메인이 승인된 도메인으로 OAuth 동의 화면에 자동으로 추가됩니다."
- 승인된 JavaScript 원본 ⓘ — "브라우저 요청에 사용" [+ URI 추가]
- 승인된 리디렉션 URI ⓘ (아래로 이어짐)

**애플리케이션 유형을 '웹 애플리케이션'으로 선택, 이름 디폴트 그대로**

**승인된 리디렉션 URI' 항목에 아래 URI 입력**
(※ 원문 표기 그대로 — 여는 작은따옴표 없이 닫는 따옴표만 있음)

[화면 캡처 3 — 오른쪽] 저장 후의 "← 웹 애플리케이션의 클라이언트 ID" 화면 (🗑 삭제 버튼)
- 탭 2개: `웹 애플리케이션의 클라이언트`, `G 로그인 - Google 계정`
- 주소창 `https://console.cloud.google.com/auth/clients/131457979987-4eg2qpr3kuodbf3eeorjsq3p46u8pv2v.ap...`
- 경로: Google 인증 플랫폼 / 클라이언트 / 클라이언트: `131457979987-4eg2qpr3kuodbf3eeorjsq3p46u8pv2v.apps.googleusercontent.com`
- 승인된 JavaScript 원본 ⓘ — "브라우저 요청에 사용" [+ URI 추가] (비어 있음)
- 승인된 리디렉션 URI ⓘ — "웹 서버의 요청에 사용"
- **빨간 박스: URI 1 \* = `http://localhost:8000/login/oauth2/code/google`**, 아래 [+ URI 추가]
- "참고: 설정이 적용되는 데 5분에서 몇 시간이 걸릴 수 있습니다." [저장] [취소]

```
http://localhost:8000/login/oauth2/code/google
```

(※ 검증: Python urlparse로 확인 — scheme=http, host=localhost, port=8000, path=/login/oauth2/code/google. Spring Security OAuth2 Client의 기본 리디렉션 URI 템플릿 `{baseUrl}/login/oauth2/code/{registrationId}`에 registrationId=`google`을 넣은 형태와 일치. 실습 서버를 8000 포트로 띄운다는 전제)
(※ 검증: Python 정규식으로 클라이언트 ID `131457979987-4eg2qpr3kuodbf3eeorjsq3p46u8pv2v.apps.googleusercontent.com` 확인 — `숫자-32자.apps.googleusercontent.com` 형식과 일치, 다음 슬라이드 목록의 `131457979987-4eg2...`와도 앞부분 일치)

---

<!-- p.20 -->

Google OAuth 클라이언트 생성
5. 클라이언트 만들기(계속)
OAuth 2.0 클라이언트 ID 생성 확인

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[화면 캡처] 생성 완료 후 Google 인증 플랫폼 / 클라이언트 목록
- 탭 `클라이언트 – Google 인증 플랫...`, 주소창 `https://console.cloud.google.com/auth/clients?highlightClient=131457979987-4eg2qpr3k...`
- 상단: Google Cloud | `OAuth2 Test` | 검색창 "사용자 인증 정보" [검색], 알림 배지 ②
- 왼쪽 메뉴: 개요 · 브랜딩 · 대상 · **클라이언트**(선택) · 데이터 액세스 · 인증 센터
- 툴바: 클라이언트 | + CREATE CLIENT | 🗑 삭제 | ↶ 삭제된 OAUTH 클라이언트 복원
- **OAuth 2.0 클라이언트 ID** 표

| 이름 | 생성일 ↓ | 유형 | 클라이언트 ID | 작업 |
|---|---|---|---|---|
| 웹 클라이언트 1 (링크) | 2025. 2. 26. | 웹 애플리케이션 | 131457979987-4eg2... (복사 아이콘) | ✏ 편집 · 🗑 삭제 · ⬇ 다운로드(JSON) |

- 화면 아래 토스트 메시지: "OAuth 클라이언트 생성됨" ✕

(※ 검증: Python으로 확인 — 주소창 highlightClient 값과 표의 클라이언트 ID 앞부분 `131457979987-4eg2`가 앞 슬라이드의 전체 ID와 일치)

---

<!-- p.21 -->

Google OAuth 클라이언트 생성
6. 데이터 액세스 설정
항목 추가 또는 삭제 화면으로 들어가서 2개 항목 선택 하고 [업데이트] 버튼 클릭

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[화면 캡처 1 — Google Cloud 콘솔 '데이터 액세스' 화면]**
- 브라우저 탭: `데이터 액세스 – Google 인증 …`, 주소창: `https://console.cloud.google.com/auth/scopes?hl=ko&inv=1&invt=AbqlbA&organization…`
- 상단 바: Google Cloud / 프로젝트 선택 `OAuth2 Test` / 검색창 `동의` / [검색]
- 경로: Google 인증 플랫폼 / 데이터 액세스
- 왼쪽 메뉴: 개요 · 브랜딩 · 대상 · 클라이언트 · **데이터 액세스**(빨간 박스) · 인증 센터
- 본문 '데이터 액세스': "범위는 사용자에게 앱 승인을 요청하는 권한을 나타내며 프로젝트에서 사용자의 Google 계정에 있는 특정 유형의 비공개 사용자 데이터에 액세스하도록 허용합니다. 자세히 알아보기"
- **[범위 추가 또는 삭제]** 버튼(빨간 박스)
- '민감하지 않은 범위' 표(열: API ↑ | 범위 | 사용자에게 표시되는 설명) — "표시할 행이 없습니다."
- '🔒 민감한 범위' — "민감한 범위는 비공개 사용자 데이터에 대한 액세스를 요청하는 범위입니다." 표(API ↑ | 범위 | 사용자에게 표시되는 설명) — "표시할 행이 없습니다."

**[화면 캡처 2 — '선택한 범위 업데이트' 패널]**
- 안내: "아래에는 사용 설정된 API의 범위만 나와 있습니다. 이 화면에 누락된 범위를 추가하려면 Google API 라이브러리에서 API를 찾아 사용 설정하거나 아래의 '붙여넣은 범위' 텍스트 상자를 사용하세요. 라이브러리에서 사용 설정한 새 API를 확인하려면 페이지를 새로고침하세요."
- 필터: 속성 이름 또는 값 입력

| 선택 | API | 범위 | 사용자에게 표시되는 설명 |
|---|---|---|---|
| ☑ (빨간 박스) | | `.../auth/userinfo.email` | 기본 Google 계정의 이메일 주소 확인 |
| ☑ (빨간 박스) | | `.../auth/userinfo.profile` | 개인정보(공개로 설정한 개인정보 포함) 보기 |
| ☐ | | `openid` | Google에서 내 개인 정보를 나와 연결 |
| ☐ | Analytics Hub API | `.../auth/bigquery` | View and manage your data in Google BigQuery and see the email address for your Google Account |
| ☐ | Analytics Hub API | `.../auth/cloud-platform` | Google Cloud 데이터 확인, 수정, 구성, 삭제 및 Google 계정의 이메일 주소 확인 |
| ☐ | BigQuery API | `.../auth/bigquery.readonly` | Google BigQuery에서 데이터를 봅니다. |
| ☐ | BigQuery API | `.../auth/cloud-platform.read-only` | Google Cloud 서비스 전체의 데이터 조회 및 Google 계정의 이메일 주소 확인 |
| ☐ | BigQuery API | `.../auth/devstorage.full_control` | Manage your data and permissions in Cloud Storage and see the email address for your Google Account |
| ☐ | BigQuery API | `.../auth/devstorage.read_only` | Google 클라우드 저장소에서 데이터 조회 |
| ☐ | BigQuery | `.../auth/devstorage…` | Cloud Storage의 데이터 관리 및 Google 계정의 이메일 주소 확… (이하 잘림) |

→ 선택하는 2개 항목 = `userinfo.email`, `userinfo.profile` (뒤 슬라이드 인가 요청 URL의 scope와 동일).

**[화면 캡처 3 — 패널 하단 '직접 범위 추가']**
- "추가할 범위가 위 표에 표시되지 않으면 여기에 입력할 수 있습니다. 각 범위를 새 줄에 입력하거나 쉼표로 구분해야 합니다. 'https://'로 시작하는 전체 범위 문자열을 입력하세요. 완료되면 '표에 추가'를 클릭하세요."
- 빈 입력 상자, [테이블에 추가] 버튼, 맨 아래 **[업데이트]** 버튼(빨간 박스)

---

<!-- p.22 -->

Google OAuth 클라이언트 생성
7. 대상 설정
대상 > 테스트 사용자 > + ADD USERS 에 본인 메일 주소 입력

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[화면 캡처 1 — '대상' 화면]**
- 브라우저 탭: `대상 – Google 인증 플랫폼 – C…`, 주소창: `https://console.cloud.google.com/auth/audience?hl=ko&inv=1&invt=AbqlbA&organizati…`
- 상단 바: Google Cloud / `OAuth2 Test` / 검색창 `동의`
- 경로: Google 인증 플랫폼 / 대상
- 왼쪽 메뉴: 개요 · 브랜딩 · **대상**(빨간 박스) · 클라이언트 · 데이터 액세스 · 인증 센터
- 'OAuth 사용자 한도 ?': "게시 상태가 '테스트 중'으로 설정된 동안에는 테스트 사용자만 앱에 액세스할 수 있습니다. 앱 인증 전에 허용되는 사용자 한도는 100명이며 앱의 전체 수명 주기에서 계산됩니다. 자세히 알아보기" / 진행 막대 "사용자 0명(테스트 0명, 기타 0명)/사용자 한도100명"
- '테스트 사용자' — **[+ ADD USERS]** 버튼(빨간 박스)
- 필터(속성 이름 또는 값 입력) / 표 열 '사용자 정보' — "표시할 행이 없습니다." / '∧ 간략히 보기'

**[화면 캡처 2 — '사용자 추가' 패널]**
- ⚠ "게시 상태가 '테스트 중'으로 설정된 동안에는 테스트 사용자만 앱에 액세스할 수 있습니다. 앱 인증 전에 허용되는 사용자 한도는 100명이며 앱의 전체 수명 주기에서 계산됩니다." LEARN MORE
- 입력란: `pineful@gmail.com` (빨간 박스), 글자 수 표시 `0 / 100`
- **[저장]** 버튼

---

<!-- p.23 -->

Google OAuth 클라이언트 생성
8. 설정 확인 및 테스트
사용자 인증 정보 > OAuth 2.0 클라이언트 ID > 생성한 웹 클라이언트 항목의 맨 끝 다운로드 아이콘 클릭
아래 URL에 클라이언트 ID를 넣어 구글 로그인 창이 뜨는지 확인
https://accounts.google.com/o/oauth2/auth?client_id=클라이언트ID&redirect_uri=http://localhost:8000/login/oauth2/code/google&response_type=code&scope=https://
www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/userinfo.profile

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[화면 캡처 1 — API 및 서비스 > 사용자 인증 정보, '웹 클라이언트 1' 팝업]**
- 브라우저 탭: `사용자 인증 정보 – API 및 서비…`, 주소창: `https://console.cloud.google.com/apis/credentials?hl=ko&inv=1&invt=AbqlbA&organizationId=0&pr…`
- 상단: Google Cloud / `OAuth2 Test` / 검색창 `사용자 인증 정보`
- 왼쪽 메뉴(API 및 서비스): 사용 설정된 API 및 서비스 · 라이브러리 · **사용자 인증 정보**(선택됨) · OAuth 동의 화면 · 페이지 사용 동의
- 상단 버튼: [+ 사용자 인증 정보 만들기] [삭제] [삭제된 사용자 인증 정보 복원]
- 배경 목록의 OAuth 2.0 클라이언트 ID 행 끝 아이콘: 연필(수정) · 휴지통(삭제) · **⬇ 다운로드**; 클라이언트 ID 열 `…57979987-4eg2...`
- 팝업 '웹 클라이언트 1' (클라이언트 ID·보안 비밀번호 부분 빨간 박스):

| 항목 | 값 |
|---|---|
| 클라이언트 ID | `131457979987-4eg2qpr3kuodbf3eeorjsq3p46u8pv2v.apps.googleusercontent.com` |
| 클라이언트 보안 비밀번호 | `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` |
| 생성일 | 2025년 2월 26일 PM 5시 5분 10초 GMT+9 |
| 상태 | ✅ 사용 설정됨 |

- [⬇ JSON 다운로드], [닫기]
- (※ 검증: Python으로 확인 — 클라이언트 ID는 `숫자12자리-영숫자32자.apps.googleusercontent.com`, 보안 비밀번호는 `GOCSPX-` + 28자 형식으로 Google OAuth 클라이언트 형식과 일치. 25쪽 application.properties에 보이는 일부 값 `GOCSPX-8MyKdI60-rfs…`, `…jsq3p46u8pv2v.apps.googleusercontent.com`와도 일치)

**[화면 캡처 2 — 위 URL 접속 결과: Google 로그인 '계정 선택' 화면]**
- 탭: `웹 애플리케이션의 클라이언트` / `로그인 - Google 계정`, 주소창: `https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?client_id=131457979987-4eg2qpr3…`
- 'G Google 계정으로 로그인' — **계정 선택**, "OAuth2 Test(으)로 이동"
- 계정 목록: 박민순 `mspark@openeg.co.kr` (로그아웃됨) / 박민순 `pineful@gmail.com` / 다른 계정 사용
- 하단: 한국어 ▾ · 도움말 · 개인정보처리방침 · 약관(일부를 파란 박스로 가림)

**[테스트 URL 파라미터 정리]** (※ 검증: Python `urllib.parse`로 분해 — 일치)
```
엔드포인트     : https://accounts.google.com/o/oauth2/auth
client_id      : 클라이언트ID
redirect_uri   : http://localhost:8000/login/oauth2/code/google
response_type  : code
scope          : https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile   ('+' = 공백 구분)
```
(※ 검증: URL의 redirect_uri 포트는 **8000**인데, 26쪽 Google 콘솔 '승인된 리디렉션 URI'와 25쪽 `oauth2.google.redirect-uri`는 **8080**으로 표기됨 — 원문 내부 불일치. Google은 등록된 URI와 정확히 일치해야 하므로 실제로는 둘 중 하나를 맞춰야 함. 서버 포트는 25쪽 `server.port=8000`, 29쪽 콘솔 `Tomcat started on port(s): 8000`)

---

<!-- p.24 -->

Authorization Code 발급
〮 Google OAuth API 등록 필요
〮 사용자가 구글 로그인을 마치고 나면 redirect_uri에 Authorization Code를 응답해 줌

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[도식 — Google OAuth 2.0 웹 서버 흐름 시퀀스 다이어그램]** (참여자: User / Your App / Google Servers)
```
Your App ──Request token──────────────────────▶ Google Servers
User     ──User login & consent───────────────▶ Google Servers     ┐ 빨간 박스
Your App ◀- - - - Authorization code - - - - - - Google Servers     ┘ (이번 단계)
Your App ──Exchange code for token────────────▶ Google Servers
Your App ◀- - - - Token response - - - - - - - - Google Servers
Your App ──Use token to call Google API───────▶ Google Servers
```
- 빨간 박스: 'User login & consent' → 'Authorization code' 구간 = 이 슬라이드에서 구현하는 Authorization Code 발급 단계.

---

<!-- p.25 -->

Authorization Code 발급
〮 구축되어 있는 LAB 환경에 소스 추가하여 OAuth2 연동 테스트 구현
〮 LAB 소스코드에서 src/main/resources/application.properties 파일에 클라이언트 ID,
클라이언트 Secret, 토큰, 리소스 URI 등 내용 추가
발급받은 클라이언트 ID값
발급받은 클라이언트 Secret 값
입력한 리디렉트 URI 값

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[코드 캡처 — `application.properties` (Eclipse/STS 편집기)]**
```properties
# Server
server.port=8000
#server.error.whitelabel.enabled=false
#server.error.include-exception=true
#server.error.include-stacktrace=always

spring.web.resources.static-locations=classpath:/static/

# thymeleaf
spring.thymeleaf.prefix=classpath:templates/
spring.thymeleaf.check-template-location=true
spring.thymeleaf.suffix=.html
spring.thymeleaf.mode=HTML5
spring.thymeleaf.cache=false

logging.config=classpath:log4j2.xml

# OAuth2 Test
oauth2.google.client-id=1314579…(라벨에 가려짐)…jsq3p46u8pv2v.apps.googleusercontent.com
oauth2.google.client-secret=GOCSPX-8MyKdI60-rfs…(라벨에 가려짐)
oauth2.google.redirect-uri=http://localhost:8080/login/oauth2/code/goo…(라벨에 가려짐)
oauth2.google.token-uri=https://oauth2.googleapis.com/token
oauth2.google.resource-uri=https://www.googleapis.com/oauth2/v2/userinfo
```
- 행 번호 1~23 (17행 빈 줄, 24행 이하 빈 줄). 18~23행(`# OAuth2 Test` 블록) 전체가 빨간 박스.
- 빨간 라벨 위치: "발급받은 클라이언트 ID값" → 19행 client-id, "발급받은 클라이언트 Secret 값" → 20행 client-secret, "입력한 리디렉트 URI 값" → 21행 redirect-uri.
- (※ 검증: 30쪽 코드의 `env.getProperty("oauth2." + registrationId + ".client-id")` 등에 registrationId=`google`을 넣으면 위 키 `oauth2.google.client-id/client-secret/redirect-uri/token-uri`와 정확히 일치 — Python으로 확인)
- (※ 검증: `server.port=8000`인데 `redirect-uri`는 `localhost:8080` — 23·29쪽 인가 요청 URL(`localhost:8000`)과 불일치. 토큰 교환 시 redirect_uri는 인가 요청 때 값과 같아야 하므로 원문 내부 모순)

---

<!-- p.26 -->

Authorization Code 발급
〮 컨트롤러
〮 기존 로그인 컨트롤러 소스코드인 LoginController.java 끝에 코드 추가
〮 kr.co.openeg.lab.loginController.LoginController.java
kr.co.openeg.lab.login.controller.LoginController.java

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[화면 캡처 — Google 콘솔 '승인된 리디렉션 URI' 입력란]**
- 제목 "승인된 리디렉션 URI ?", 설명 "웹 서버의 요청에 사용"
- `URI 1 *` 입력값: `http://localhost:8080/login/oauth2/code/google` (빨간 박스)
- (※ 검증: 포트 8080 — 23·29쪽 테스트 URL의 redirect_uri `http://localhost:8000/...` 및 `server.port=8000`과 불일치. 원문 표기 그대로)

**[코드 캡처 — LoginController.java 55~82행, 74~81행 파란 박스가 추가 코드]**
```java
            mav.addObject("userId", userId);
            mav.addObject("errCode", 1);    // not exist userId in database
            mav.setViewName("index");
            return mav;
        }else {
            session.setAttribute("userId", userId);
            session.setAttribute("userName", loginCheckResult.getUserName());
            mav.setViewName("redirect:/board/main");

            return mav;
        }
    }

    @RequestMapping("/logout")
    public String logout(HttpSession session){
        session.invalidate();
        return "redirect:login";
    }

    // ── 74~81행: 추가 코드(파란 박스) ──
    @RequestMapping("/login/oauth2/code/{registrationId}")
    public ModelAndView googleLogin(@RequestParam(required = false) String code, @PathVariable String registrationId) {
        service.socialLogin(code, registrationId);

        ModelAndView mav = new ModelAndView();
        mav.setViewName("redirect:/");
        return mav;
    }
}
```
- 코드 아래 캡션 상자: `kr.co.openeg.lab.login.controller.LoginController.java`
- (※ 원문 표기 그대로 — 본문 경로는 `kr.co.openeg.lab.loginController.LoginController.java`, 캡션은 `kr.co.openeg.lab.login.controller.LoginController.java`로 서로 다름. 실제 패키지는 캡션 쪽(`login.controller`)으로 보임)
- (※ 검증: 리디렉트 경로 `/login/oauth2/code/google`이 `/login/oauth2/code/{registrationId}`에 매칭되어 registrationId=`google` — Python 정규식으로 확인, 29쪽 콘솔 `registrationId = google`과 일치)

---

<!-- p.27 -->

Authorization Code 발급
〮 서비스
〮 기존 로그인 서비스 소스코드인 LoginService.java 끝에 코드 추가
〮 kr.co.openeg.lab.loginService.LoginService.java

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[코드 캡처 — LoginService.java 1~30행, 25~28행 파란 박스가 추가 코드]**
```java
package kr.co.openeg.lab.login.service;

import org.springframework.beans.factory.annotation.Autowired;[...]   // 4~9행 import 접힘

@Service
public class LoginService {

    @Autowired
    private LoginDao dao;

    public MemberModel checkUserId(String userId) {
        return dao.selectUserId(userId);
    }

    public MemberModel checkUserId(LoginSessionModel loginModel) {
        return dao.selectUserId(loginModel);
    }

    // ── 25~28행: 추가 코드(파란 박스) ──
    public void socialLogin(String code, String registrationId) {
        System.out.println("code = " + code);
        System.out.println("registrationId = " + registrationId);
    }

}
```
- (※ 원문 표기 그대로 — 본문 경로는 `kr.co.openeg.lab.loginService.LoginService.java`이지만 코드의 패키지 선언은 `kr.co.openeg.lab.login.service`)

---

<!-- p.28 -->

Authorization Code 발급
〮 로그인 필터
〮 로그인되어 있지 않아도 /login/oauth2 이하 URL 접근이 가능하도록 SessionInterceptor.java 소스코드 수정
〮 kr.co.openeg.lab.common.interceptor.SessionInterceptor.java

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[코드 캡처 — SessionInterceptor.java 21~49행, 35~40행 빨간 박스가 추가 코드]**
```java
        // pass through when access login.do, join.do

        if(request.getRequestURI().equals("/login")||
            request.getRequestURI().equals("/rest/login")||
            request.getRequestURI().equals("/vanilla/login")||
            request.getRequestURI().equals("/member/join")){
            if(userId != null){
                response.sendRedirect(request.getContextPath() + "/board/list");
                return true;
            } else {
                return true;
            }
        }

        // ── 36~40행: 추가 코드(빨간 박스) ──
        // bypass OAuth2 authentication URI
        if(request.getRequestURI().startsWith("/login/oauth2")) {
            System.out.println("oauth2 login bypass!");
            return true;
        }

        //
        // where other pages
        if(userId == null){
            response.sendRedirect(request.getContextPath() + "/login");
            HttpSession session=request.getSession();
            session.setAttribute("errCode", "4");
            return false;
        } else {
```
- (※ 검증: Python으로 확인 — `"/login/oauth2/code/google".startswith("/login/oauth2")` = True. 다만 `/login/oauth2evil`처럼 접두어만 같은 경로도 True가 되므로 `/login/oauth2/`로 끝 슬래시까지 비교하는 편이 더 엄격함)

---

<!-- p.29 -->

Authorization Code 발급
〮 앞서 시도해봤던 URL을 입력하여 구글 로그인 창이 나타나며, 계정을 선택하고 진행하면 STS 콘솔에 메시지가 제대로
출력되면 성공
https://accounts.google.com/o/oauth2/auth?client_id=클라이언트ID&redirect_uri=http://localhost:8000/login/oa
uth2/code/google&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email+https://www.google
apis.com/auth/userinfo.profile

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[테스트 URL — 한 줄로 이어 쓴 형태]**
```
https://accounts.google.com/o/oauth2/auth?client_id=클라이언트ID&redirect_uri=http://localhost:8000/login/oauth2/code/google&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/userinfo.profile
```
(슬라이드에서 '클라이언트ID'는 빨간 글씨 = 실제 값으로 바꿔 넣을 자리)

**[화면 캡처 1 — 계정 선택]** 탭 `클라이언트 – Google 인증 플랫…` / `로그인 - Google 계정`, 주소 `https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?client_id=131457979987-4eg2qpr3…`; 'Google 계정으로 로그인' — 계정 선택, "OAuth2 Test(으)로 이동", 계정 2개(이름·메일 파란 박스로 가림), 다른 계정 사용.

**[화면 캡처 2 — 동의 화면]** 주소 `https://accounts.google.com/signin/oauth/id?authuser=0&part=AJi8hAN8hZMzwEaAs7mCpMC2UHb…`; "OAuth2 Test 서비스로 로그인", 계정 `pineful@gmail.com ▾`; 안내 "계속하면 Google에서 내 이름, 이메일 주소, 언어 환경설정, 프로필 사진을 OAuth2 Test 서비스와 공유합니다. OAuth2 Test의 개인정보처리방침 및 서비스 약관을 참고하세요." "Google 계정에서 Google 계정으로 로그인을 관리할 수 있습니다." 버튼 [취소] [계속].

**[STS 콘솔 캡처]** (탭: Problems · Javadoc · Declaration · Search · Console · Call Hierarchy; `SecureCoding - SecureCodingLabTestApplication [Spring Boot App] C:\SecureCoding2025\sts4\sts-4.10.0.RELEASE\plugins\org.eclipse.justj.openjdk.hotspot.jre…`)
```
2025-02-27 10:37:40 WARN  TemplateMode:150 - [THYMELEAF][restartedMain] Template Mode 'HTML5' is …
2025-02-27 10:37:40 INFO  OptionalLiveReloadServer:58 - LiveReload server is running on port 3572…
2025-02-27 10:37:40 INFO  Http11NioProtocol:173 - Starting ProtocolHandler ["http-nio-8000"]
2025-02-27 10:37:40 INFO  TomcatWebServer:220 - Tomcat started on port(s): 8000 (http) with conte…
2025-02-27 10:37:40 INFO  SecureCodingLabTestApplication:61 - Started SecureCodingLabTestApplicat…
2025-02-27 10:37:40 INFO  ConditionEvaluationDeltaLoggingListener:63 - Condition evaluation unchan…
2025-02-27 15:13:13 INFO  [/]:173 - Initializing Spring DispatcherServlet 'dispatcherServlet'
2025-02-27 15:13:13 INFO  DispatcherServlet:525 - Initializing Servlet 'dispatcherServlet'
2025-02-27 15:13:13 INFO  DispatcherServlet:547 - Completed initialization in 40 ms
2025-02-27 15:13:13 WARN  SessionIdGeneratorBase:173 - Creation of SecureRandom instance for sess…
oauth2 login bypass!                                                          ← 빨간 박스
code = 4/0AQSTgQG2cqjbbarYc53Iz8enPwqy7IT9PjwyqFlg0Wx7wPJhp_GypUbCTsgFD3-3l3hNBw   ← 빨간 박스
registrationId = google                                                       ← 빨간 박스
```
- 'oauth2 login bypass!'는 28쪽 인터셉터, 'code = …'/'registrationId = …'는 27쪽 socialLogin()의 출력. (※ 검증: code가 Google 인가 코드 형식인 `4/0A…`로 시작 — 일치; `3l3hNBw`의 l/1 구분은 판독 확신 낮음)

---

<!-- p.30 -->

Access Token 발급
〮 발급받은 Authorization Code를 통해 Access Token 발급
〮 서비스 (코드 수정)
accessToken 발급 성공 콘솔 화면

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[코드 캡처 — LoginService.java 33~79행, 39~76행 빨간 박스가 수정 코드]**
```java
    }

    public MemberModel checkUserId(LoginSessionModel loginModel) {
        return dao.selectUserId(loginModel);
    }

    // ── 39~76행: 수정 코드(빨간 박스) ──
    private final Environment env;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final RestTemplate restTemplate = new RestTemplate();

    public LoginService(Environment env) {
        this.env = env;
    }
    public void socialLogin(String code, String registrationId) {
        String accessToken = getAccessToken(code, registrationId);
        System.out.println("accessToken = " + accessToken);
    }

    private String getAccessToken(String authorizationCode, String registrationId) {
        String clientId = env.getProperty("oauth2." + registrationId + ".client-id");
        String clientSecret = env.getProperty("oauth2." + registrationId + ".client-secret");
        String redirectUri = env.getProperty("oauth2." + registrationId + ".redirect-uri");
        String tokenUri = env.getProperty("oauth2." + registrationId + ".token-uri");

        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
        params.add("code", authorizationCode);
        params.add("client_id", clientId);
        params.add("client_secret", clientSecret);
        params.add("redirect_uri", redirectUri);
        params.add("grant_type", "authorization_code");

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

        HttpEntity entity = new HttpEntity(params, headers);

        ResponseEntity<String> response = restTemplate.exchange(tokenUri, HttpMethod.POST, entity, String.class);
        try {
            JsonNode accessTokenNode = objectMapper.readTree(response.getBody());
            return accessTokenNode.get("access_token").asText();
        } catch (IOException e) {
            throw new RuntimeException("Failed to parse access token response", e);
        }
    }

}
```
- 즉 토큰 엔드포인트 `https://oauth2.googleapis.com/token`에 `application/x-www-form-urlencoded` POST로 `code, client_id, client_secret, redirect_uri, grant_type=authorization_code` 전송 → 응답 JSON의 `access_token` 추출. (※ 검증: Python `urlencode`로 같은 본문 구성 확인 — 일치)

**[도식]** 24쪽과 같은 시퀀스 다이어그램(User / Your App / Google Servers). 이번에는 **'Exchange code for token' → 'Token response'** 구간이 빨간 박스.

**[콘솔 캡처 — accessToken 발급 성공]** (`… javaw.exe (2025. 2. 27. 오후 3:28:04)`)
```
2025-02-27 15:28:21 INFO  OptionalLiveReloadServer:58 - LiveReload server is running on port 35729
2025-02-27 15:28:21 INFO  Http11NioProtocol:173 - Starting ProtocolHandler ["http-nio-8000"]
2025-02-27 15:28:21 INFO  TomcatWebServer:220 - Tomcat started on port(s): 8000 (http) with context path ''
2025-02-27 15:28:21 INFO  SecureCodingLabTestApplication:61 - Started SecureCodingLabTestApplication in 3.253 seconds (JVM running for 15.57)
2025-02-27 15:28:51 INFO  [/]:173 - Initializing Spring DispatcherServlet 'dispatcherServlet'
2025-02-27 15:28:51 INFO  DispatcherServlet:525 - Initializing Servlet 'dispatcherServlet'
2025-02-27 15:28:51 INFO  DispatcherServlet:547 - Completed initialization in 1 ms
oauth2 login bypass!                                                          ← 빨간 박스
accessToken = ya29.a0AeXRPp4V7qUB7KdmiomBWLtBt7c4O0p3t9IhHl9pYJAN5nBrQZN-Ie9DXS_wLeipb7LOiuH78Um6oTb-5lWv5rD7os8j2cbedpVSNgRv2HdXaVq_BPyRh6_RFeWPEO8mhbHUEM…(오른쪽 잘림)   ← 빨간 박스
2025-02-27 15:28:56 WARN  FragmentProcessor:-1 - You don't need to put the layout:fragment/data-layout-fragment attribute into the <head> section - the dec…
```
- (※ 검증: Google access token의 `ya29.` 접두어 형식과 일치. 토큰 문자열의 O/0, l/1 구분은 판독 확신 낮음)
- (※ 참고: 실습 확인용으로 access token을 콘솔에 그대로 출력하는데, 35~36쪽의 'Access Token 유출' 관점에서는 운영 코드에서 토큰 로깅을 피해야 함)

---

<!-- p.31 -->

Resource Server에서 유저정보 받기
〮 발급받은 Authorization Code를 통해 Access Token 발급
〮 서비스 (코드 수정)
최종적으로 유저정보 수신 성공

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 원문 표기 그대로 — 첫 줄 "발급받은 Authorization Code를 통해 Access Token 발급"은 30쪽 문구를 그대로 쓴 것으로, 이 슬라이드의 실제 내용은 Access Token으로 Resource Server에서 유저 정보 조회)

**[코드 캡처 1 — LoginService.socialLogin() 46~57행 (수정)]**
```java
    public void socialLogin(String code, String registrationId) {
        String accessToken = getAccessToken(code, registrationId);
        JsonNode userResourceNode = getUserResource(accessToken, registrationId);
        System.out.println("userResourceNode = " + userResourceNode);

        String id = userResourceNode.get("id").asText();
        String email = userResourceNode.get("email").asText();
        String nickname = userResourceNode.get("name").asText();
        System.out.println("id = " + id);
        System.out.println("email = " + email);
        System.out.println("nickname = " + nickname);
    }
```

**[코드 캡처 2 — getUserResource() 86~94행 (추가)]**
```java
    private JsonNode getUserResource(String accessToken, String registrationId) {
        String resourceUri = env.getProperty("oauth2."+registrationId+".resource-uri");

        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + accessToken);
        HttpEntity entity = new HttpEntity(headers);
        return restTemplate.exchange(resourceUri, HttpMethod.GET, entity, JsonNode.class).getBody();
    }
}
```
- 즉 `GET https://www.googleapis.com/oauth2/v2/userinfo` + 헤더 `Authorization: Bearer <access token>`.

**[도식]** 24쪽과 같은 시퀀스 다이어그램. 이번에는 **'Use token to call Google API'** 구간이 빨간 박스.

**[콘솔 캡처 — 최종적으로 유저정보 수신 성공]** (`… javaw.exe (2025. 2. 27. 오후 3:41:21)`)
```
2025-02-27 15:41:26 INFO  SecureCodingLabTestApplication:61 - Started SecureCodingLabTestApplication in 2.813 seconds (JVM running for 4.132)
2025-02-27 15:41:40 INFO  [/]:173 - Initializing Spring DispatcherServlet 'dispatcherServlet'
2025-02-27 15:41:40 INFO  DispatcherServlet:525 - Initializing Servlet 'dispatcherServlet'
2025-02-27 15:41:40 INFO  DispatcherServlet:547 - Completed initialization in 1 ms
oauth2 login bypass!                                                                  ← 빨간 박스(이하 nickname 행까지)
userResourceNode = {"id":"117678585699554568936","email":"(가림)","verified_email":true,"name":"(가림)","given_name":"(가림)","family_name":"(가림)","pictu…(잘림)
id = 117678585699554568936
email = (파란 박스로 가림)
nickname = (파란 박스로 가림)
2025-02-27 15:41:42 WARN  FragmentProcessor:-1 - You don't need to put the layout:fragment/data-layout-fragment attribute into the <head> section - the dec…
```
- (※ 검증: Python으로 확인 — Google 사용자 id `117678585699554568936`은 21자리 숫자로 Google 계정 고유 ID 형식과 일치. userinfo v2 응답 필드 id/email/verified_email/name/given_name/family_name/picture가 코드의 `get("id")`, `get("email")`, `get("name")`과 대응)

---

<!-- p.32 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# 유저 정보를 토대로 계정 연동

- 원래 id 또는 email 정보를 토대로 사용자 DB와 연동 로직을 구현해야 함. 편의상 강제로 test 계정과 연동 처리.

**· 컨트롤러 (코드 수정)** — LoginController.java 75~86행
```java
    @RequestMapping("/login/oauth2/code/{registrationId}")
    public ModelAndView googleLogin(
            @RequestParam(required = false) String code,
            @PathVariable String registrationId,
            HttpServletRequest request,
            HttpServletResponse response) {
        service.socialLogin(code, registrationId, request, response);

        ModelAndView mav = new ModelAndView();
        mav.setViewName("redirect:/board/main");
        return mav;
    }
```

**· 서비스 (코드 수정)** — LoginService.java 51~77행
```java
    public void socialLogin(String code, String registrationId, HttpServletRequest request, HttpServletResponse response) {
        String accessToken = getAccessToken(code, registrationId);
        JsonNode userResourceNode = getUserResource(accessToken, registrationId);
        System.out.println("userResourceNode = " + userResourceNode);

        String id = userResourceNode.get("id").asText();
        String email = userResourceNode.get("email").asText();
        String nickname = userResourceNode.get("name").asText();
        System.out.println("id = " + id);
        System.out.println("email = " + email);
        System.out.println("nickname = " + nickname);

        // 강제로 test 계정과 연동.
        MemberModel member = checkUserId("test");
        if (member == null) {
            throw new RuntimeException("User not found in local DB: test");
        }

        HttpSession session = request.getSession(true);
        session.setAttribute("userId", member.getUserId());
        session.setAttribute("userName", nickname);          // 이름을 구글 계정에서 가져온다.

        // 5? 클라이언트가 세션을 사용할 수 있도록 `JSESSIONID` 쿠키 설정
        response.setHeader("Set-Cookie", "JSESSIONID=" + session.getId() + "; Path=/; HttpOnly; Secure");

        System.out.println("OAuth2 Login 성공 - JSESSIONID 발급 완료");
    }
```
(73행 주석 맨 앞 '5' 뒤 글자는 '回'처럼 보이는 깨진 문자 — 판독 확신 낮음)

- test 계정으로 연동되어 세션 ID 발급됨

**[콘솔 캡처]** (`… javaw.exe (2025. 2. 27. 오후 4:45:41)`)
```
2025-02-27 16:46:02 INFO  DispatcherServlet:547 - Completed initialization in 1 ms
oauth2 login bypass!
userResourceNode = {"id":"117678585699554568936","email":"(가림)","verified_email":true,"name":"(가림)","given_name":"(가림)","family_name":"(가림)","pictu…(잘림)
id = 117678585699554568936
email = (파란 박스로 가림)
nickname = (파란 박스로 가림)
2025-02-27 16:46:03 INFO  HikariDataSource:110 - HikariPool-1 - Starting...
2025-02-27 16:46:03 INFO  HikariDataSource:123 - HikariPool-1 - Start completed.
OAuth2 Login 성공 - JSESSIONID 발급 완료                ← 빨간 박스
2025-02-27 16:46:04 WARN  FragmentProcessor:-1 - You don't need to put the layout:fragment/data-layout-fragment attribute into the <head> section - the dec…
```
(※ 검증: Python `http.cookies`로 `JSESSIONID=<id>; Path=/; HttpOnly; Secure` 파싱 확인 — 유효한 쿠키 문법. 단 `Secure` 속성은 HTTPS에서만 전송되므로 `http://localhost:8000` 실습 환경에서는 브라우저가 이 쿠키를 저장/전송하지 않을 수 있음(localhost 예외를 두는 브라우저도 있음). 또 서블릿 컨테이너가 `getSession(true)` 시 자체 JSESSIONID 쿠키를 함께 내려 보낼 수 있음)

---

<!-- p.33 -->

OAuth2를 통한 로그인 성공 화면
〮 구글 로그인 성공하면, LAB 서비스의 test 계정으로 로그인 완료됨
〮 정보수정 화면에 들어가보면, 이름 항목에 구글계정 이름이 나타남

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[화면 캡처 1 — 로그인 후 메인]** 탭 `클라이언트 – Google 인증 플랫…` / `시큐어코딩랩 - 메인`, 주소 `localhost:8000/board/main`
- 헤더: (주)오픈이지 로고, "안전한 소프트웨어를 만들기 위한 노력"
- 메뉴: 메인 · 게시판 · 시큐어코딩 테스트 · DB 초기화 / 오른쪽 **[ test 님 ]** · 로그아웃 · 정보수정 → test 계정으로 로그인된 상태
- 본문: "소프트웨어 보안은 보안소프트웨어를 뜻하는 것이 아닙니다. / 소프트웨어 라이프 사이클 전반에 걸쳐 안전한 소프트웨어 개발의 여러 모범사례를 적용하는 것을 의미합니다. / 보안문제는 특정 보안기능의 문제보다는 안전한 시스템을 구성하는 표준의 문제 때문에 발생할 가능성이 더 높습니다. / 그래서 소프트웨어 보안은 전체 개발단계 라이프 사이클의 접근 방식 중 하나가 되어야 합니다." + 『해킹 방어를 위한 JAVA 시큐어코딩』 책 표지 이미지

**[화면 캡처 2 — 정보수정]** 탭 `시큐어코딩랩 - 회원정보 수정`, 주소 `localhost:8000/member/modify`
- '회원정보 수정' 폼: **아이디 `test`**, **이름 (구글 계정 이름 — 파란 박스로 가림)** (두 행 빨간 박스) / 비밀번호 / 새 비밀번호 / 새 비밀번호 확인 / [재작성] [확인]
- 하단: Copyright © (주)오픈이지 2021-2025
- → 32쪽 `session.setAttribute("userName", nickname)`으로 구글 계정 이름이 이름 항목에 표시됨

---

<!-- p.34 -->

OAuth2 인증 및 인가
01 OAuth2 이해
02 OAuth2 구현
03 OAuth2 보안 위협 및 해결 방법

---

<!-- p.35 -->

OAuth2 구현시 발생할 수 있는 취약점
〮 발생할 수 있는 취약점
〮 Redirect URI 검증 미흡
〮 State 파라미터 미사용
〮 PKCE 미적용
〮 주요 취약점 사례
〮 Authorization Code 탈취
- 중간자 공격(MITM)이나 오픈 리다이렉트 취약점을 이용해, 인증 코드가 탈취되어 부적절한 토큰 발급 위험
〮 Access Token 유출
- HTTPS 미적용, 불안전한 토큰 저장(예: 로컬 스토리지, 브라우저 캐시 등)으로 토큰 노출 가능
〮 토큰 재사용 및 리플레이 공격
- 만료되지 않은 토큰 또는 중복 요청 처리 미흡으로 인한 리플레이 공격, 부적절한 접근 권한 행사
〮 클라이언트 시크릿 관리 취약점
- 클라이언트 시크릿(Client Secret)이 공개 클라이언트에 노출될 경우, 악의적 사용자가 토큰 발급 시도 가능

---

<!-- p.36 -->

Access Token 유출 방지 전략
〮 안전한 전송 및 저장
〮 HTTPS/TLS 적용
〮 보안 쿠키 사용
〮 토큰 관리 정책 강화
〮 짧은 유효기간
〮 Refresh Token 도입
〮 토큰 취소 및 재발급
〮 애플리케이션 보안 강화
〮 XSS 방어: 입력값 검증, 인코딩 및 CSP(Content Security Policy) 적용
〮 PKCE 사용: 공개 클라이언트의 경우, PKCE 도입으로 Authorization Code 탈취 방지

---

<!-- p.37 -->

요약 정리
OAuth2는 웹 및 애플리케이션 인증 및 권한 부여를 위한 개방형 표준 규격이다.
Access Token 유출을 방지하기 위해 HTTPS 적용, 보안 쿠키 사용, 토큰 만료 시간 설정 등의
조치를 취해야 한다.
OAuth2에서 발생할 수 있는 주요 취약점으로는 Redirect URI 검증 미흡, State 파라미터 미사용,
PKCE 미적용 등이 있다.

---

<!-- p.38 -->

참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [홍릉과학출판사] 소프트웨어 개발 보안 실무 - 시큐어 코딩 원리와 실제
- [secu BOOK] 웹 해킹과 시큐어코딩 탐지/수정 실습가이드
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴,
암호화까지 안전한 소프트웨어의 모든 것
- [위키북스] 웹 애플리케이션 보안 완벽 가이드 - 체계적으로 배우는 안전한 웹 애플리케이션 제작 기법
- [한빛미디어] 웹 애플리케이션 보안 - 정찰, 공격, 방어 세 단계로 배우는 웹 애플리케이션 보안의 모든 것
- [한빛미디어] 웹 해킹 & 보안 완벽 가이드 - 웹 애플리케이션 보안 취약점을 겨냥한 공격과 방어

---

<!-- p.39 -->

감사합니다.

---

<!-- p.40 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# 퀴즈

1. 다음 중 OAuth2에 대한 설명으로 맞지 않는 것은?
   - 1) 인증과 인가를 분리한 프로토콜
   - 2) 제3자 애플리케이션이 사용자의 자원에 접근하도록 허용
   - 3) 토큰 기반 인증 사용
   - 4) 비밀번호를 통해 접근 권한을 위임

2. OAuth2의 구성 요소에 대한 설명 중 잘못된 것은?
   - 1) Resource Owner - 리소스 서비스 업체
   - 2) Resource Server - 보호된 리소스를 보유하고 있는 서버
   - 3) Authorization Server - 사용자 인증과 권한 부여처리, 액세스 토큰 발급
   - 4) Client Application - 보호된 리소스에 접근하려는 애플리케이션

3. Access Token 재발급을 위한 장기 인증 수단으로, 사용자 재로그인 없이 새로운 Access Token을 발급하기 위해 사용하는 Token의 이름은 무엇인가요? (영문 소문자만)
   - (                )

---

<!-- p.41 -->

퀴즈 정답
1. 다음 중 OAuth2에 대한 설명으로 맞지 않는 것은?
4) 비밀번호를 통해 접근 권한을 위임
OAuth2는 기존 OAuth 1.0의 비밀번호 유출시 취약해질 수 있는 보안을 강화하기 위해 토큰 기반 인증을 사용합니다.
2. OAuth2의 구성 요소에 대한 설명 중 잘못된 것은?
1) Resource Owner - 리소스 서비스 업체
리소스에 대한 소유 또는 접근 권한을 가지고 있는 것은 사용자입니다.
3. Access Token 재발급을 위한 장기 인증 수단으로, 사용자 재로그인 없이 새로운 Access Token을 발급
하기 위해 사용하는 Token의 이름은 무엇인가요? (영문 소문자만)
( refresh )

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(정답 표시: 1번 '4) 비밀번호를 통해 접근 권한을 위임', 2번 '1) Resource Owner - 리소스 서비스 업체', 3번 'refresh'가 빨간 글씨로 강조됨. 각 정답 아래 검은 글씨는 해설)
