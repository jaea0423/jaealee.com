# 2025_강원대_시큐어코딩_1주차_1차시_vF (1)

<!-- p.1 -->

시큐어코딩

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[표지 일러스트: 노트북 화면의 차트·그래프 주위에서 사람들이 돋보기·서류를 들고 협업하는 아이소메트릭 그림]

---

<!-- p.2 -->

SW개발보안 이해
01 현대 애플리케이션 보안 과제
02 사고사례를 통한 시큐어코딩 이해

---

<!-- p.3 -->

학습 목표
현대 애플리케이션의 보안과제를 이해한다
현대 애플리케이션 보안과제를 해결하기 위한 방안을 이해한다.
사고사례를 통한 시큐어코딩을 이해한다.

---

<!-- p.4 -->

학습 내용
1. 현대 애플리케이션 보안 과제
2. 사고사례를 통한 시큐어코딩 이해

---

<!-- p.5 -->

SW개발보안 이해
01 현대 애플리케이션 보안 과제
02 사고사례를 통한 시큐어코딩 이해

---

<!-- p.6 -->

데이터 유출현황 및 침해발생 원인
출처: 개인정보보호위원회 제공
최근 3년간 개인정보 유출 사고

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.7 -->

데이터 유출현황 및 침해발생 원인
2020년 한국 기업데이터 유출현황과 데이터 침해 발생원인

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.8 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
현대 애플리케이션의 보안 과제 (출처: 라드웨어 애플리케이션 보호 위한 4가지 도전과제 기술백서)

| 봇관리 | API 보안 | 서비스 거부(DoS) | 지속적인 보안 |
| --- | --- | --- | --- |
| **인터넷 트래픽의 52%는 봇에 의한 통신** | **API로 연결된 다양한 환경** | **여전히 서비스 장애를 일으키는 효과적인 공격** | **DevOps 개발환경에서 민첩성을 위해 희생되는 보안** |
| • 그중 절반은 악성 봇<br>• 기업의 79%는 악성봇과 정상봇을 구분하지 못함<br>• 악성봇은 네트워크 트래픽 낭비, 도스/디도스 공격, 중요정보/개인정보 수집, 캡챠우회 지능적인 봇 공격수행, 크리덴셜 스터핑을 통한 개인정보 수집에 이용됨 | • IoT, 클라우드, 웹, 모바일 등 다양한 환경에서 애플리케이션이 사용되며, API로 연결<br>• API를 통해 서로의 리소스와 정보 공유<br>• API 취약점을 이용해 각종 인젝션, 파라미터 조작, 공격사이트로 리다이렉트, 봇 공격 등을 발생시킴 | • 애플리케이션 계층 DoS 공격은 매우 오래된 공격 방식이지만 서비스를 장애를 일으키는데 여전히 효과적<br>• HTTP/S 플러드, 슬로우로리스, LOIC, 버퍼오버플로, 브루트 포스 공격<br>• IoT봇넷에 의해 구동되는 애플리케이션 계층 공격은 선호되는 디도스 공격 벡터 | • 신속한 개발과 롤아웃 방법론은 애플리케이션을 지속적으로 수정하고 업데이트 하지만 보안을 고려하지 못하는 경우가 발생<br>• 개발완료된 서비스의 취약점을 개선하고 보안을 주입하는 것은 더 어려운 일<br>• AI기술을 활용한 리소스 매핑, 가능한 위협 분석, 실시간 보안 정책을 생성하고 최적화 |

---

<!-- p.9 -->

애플리케이션 보안 과제는 어떻게 해결해야 할까?
SW개발보안 프로세스
DevSecOps
보안내재화
Security By Design
Zero Trust

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[슬라이드 전체가 큰 컬러 글씨로 된 5개 키워드: SW개발보안 프로세스 / DevSecOps / 보안내재화 / Security By Design / Zero Trust]

---

<!-- p.10 -->

애플리케이션 보안(1)
SW개발보안 프로세스
DevSecOps
〮
애플리케이션 수명주기 따른 반복 지속적 보안 제어 필수

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[슬라이드 전체가 큰 컬러 글씨: SW개발보안 프로세스 / DevSecOps, 아래에 '애플리케이션 수명주기 따른 반복·지속적 보안 제어 필수']

---

<!-- p.11 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
SW개발보안 프로세스

SW개발과정에서 개발자의 실수, 논리적 오류 등으로 인해 발생될 수 있는 보안약점들을 최소화하여 안전한 SW를 개발하기 위해 소프트웨어 개발 각 단계별 적절한 보안활동 수행

| 요구사항분석 | 설계 | 구현 | 테스트 |
| --- | --- | --- | --- |
| • 요구사항 중 보안요구사항 식별 | • 보안요구사항과 위협에 대한 보안통제를 고려한 위협원 도출<br>• 외부 인터페이스 식별<br>• 보안통제 수립 | • 표준코딩 정의서 및 SW개발보안 가이드를 준수하여 개발<br>• 소스코드 보안약점 진단(도구 활용) | • 실행코드 보안취약점 진단 (동적분석: 스캐닝, 모의해킹 테스트 등) |

- ※ 현재는 SW 개발과정 중 **소스코드 구현단계를 중심으로** SW 개발보안 적용
- ※ **보안취약점(Vulnerability)**: 해킹 등 실제 보안사고에 이용되는 SW 보안약점
- ※ **보안약점(Weakness)**: 보안취약점의 근본 원인이 되는 SW 상의 허점, 결점, 오류 등

---

<!-- p.12 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
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

<!-- p.13 -->

DevSecOps AWS 아키텍쳐

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.14 -->

DevSecOps AWS 아키텍쳐

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[AWS 콘솔 캡처: CodePipeline 'devsecops-workshop-pipeline-pipeline']

왼쪽 메뉴: 개발자 도구 > CodePipeline — 소스(CodeCommit: 시작하기, 리포지토리, 승인 규칙 템플릿), 빌드(CodeBuild), 배포(CodeDeploy), 파이프라인(CodePipeline), 설정

| 스테이지 | 액션 | 결과 |
| --- | --- | --- |
| **Source** (성공) | SourceAction (AWS CodeCommit) | ✅ 성공 - 4시간 전 (b4511738) |
| **SCA-and-SAST-Analysis** (실패) | SCAnalysis (AWS CodeBuild) | ✅ 성공 - 4시간 전 |
| | SASTAnalysis (AWS CodeBuild) | ❌ 실패 - 4시간 전, 작업 실행 실패 |

→ SAST 검사에서 보안약점이 발견되어 파이프라인이 **다음 단계로 넘어가지 못하고 멈춘** 상태 (재시도 버튼)

---

<!-- p.15 -->

DevSecOps AWS 아키텍쳐

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[AWS 콘솔 캡처: 같은 파이프라인의 다음 스테이지]

| 스테이지 | 액션 | 결과 |
| --- | --- | --- |
| **Staging-Depoy-and-DAST-Analysis** (성공) | DeployStagingAction (AWS Elastic Beanstalk) | ✅ 성공 - 7일 전 |
| | ↓ DASTAnalysis (AWS CodeBuild) | ✅ 성공 - 7일 전 |

(스테이징 환경에 배포한 뒤 동적 분석(DAST)을 수행)

---

<!-- p.16 -->

DevSecOps AWS 아키텍쳐

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[AWS 콘솔 캡처: 마지막 스테이지]

| 스테이지 | 액션 | 결과 |
| --- | --- | --- |
| **Manual-Approval** (성공) | ApprovalRequired (수동 승인) | ✅ 승인됨 - 7일 전 |
| **Production-Depoy** (성공) | DeployProdAction (AWS Elastic Beanstalk) | ✅ 성공 - 7일 전 |

(사람이 수동으로 승인해야 운영 환경에 배포됨)

---

<!-- p.17 -->

애플리케이션 보안(2)
보안내재화
Security By Design
안전(Secure)하게 동작되는 제품을 만들기위해 제품의 설계단계에서부터 보안을 고려함으로써
알려진 취약점을 조기에 효과적으로 제거하는 것을 의미한다.

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[슬라이드 전체가 큰 글씨: 보안내재화 / Security By Design]

---

<!-- p.18 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
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

<!-- p.19 -->

Security By Design – Threat Modeling

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.20 -->

애플리케이션 보안(3)
제로 트러스트 원칙을 사용하여 개발
Zero Trust
제로트러스트는 ‘아무것도 신뢰할 수 없다는 가정하에, 사용자 및 다양한 정보를 바탕으로 최소한
의 권한과 세밀한 통제를 지속적으로 수행하는 보안 활동’
‘Never Trust, Always Verify’

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[도식: 제로 트러스트 4단계 순환 (점선 화살표로 처음으로 되돌아감)]

① **Never Trust, Always Verify** (사용자·기기 아이콘) → ② **Least Privilege and Default Deny** (열쇠) → ③ **Full Visibility and Inspection** (돋보기) → ④ **Centralized Management** (톱니바퀴) → 다시 ①

---

<!-- p.21 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[도식: BEYONDCORP — A NEW APPROACH TO ENTERPRISE SECURITY (구글)]

- 왼쪽: **Google Building**(Unprivileged Network, Managed Device)과 **Public Network**(Managed Device)
- 두 네트워크 모두 **Access Proxy**와 **Single Sign-On**을 거쳐야 접근 가능 (Unprivileged Network는 802.1X로 RADIUS 인증)
- **접근제어엔진** 영역: Access Proxy ↔ Access Control Engine ↔ Pipeline
- **기기인증** 영역: Device Inventory Database → Trust Inference → Certificate Issuer → Pipeline
- **사용자인증** 영역: Single Sign-On ↔ User/Group Database

(오른쪽 설명 3가지 컴포넌트는 본문 텍스트와 동일)

---

<!-- p.22 -->

SW개발보안 이해
01 현대 애플리케이션 보안 과제
02 사고사례를 통한 시큐어코딩 이해

---

<!-- p.23 -->

시큐어한 소프트웨어란?
Secure Software
결함 (Defects)
실수 (Mistake) 장애 (Failure)
결점 (Fault)
오류 (Error) 문제(Problem)
버그 (Bugs)

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[도식: Secure Software를 방해하는 세 가지 (점선으로 연결, 각각 빨간 ✖ 표시)]

| 단계 | 용어 |
| --- | --- |
| 원인 | 실수(Mistake), 오류(Error) |
| 코드에 남은 것 | 결함(Defects), 결점(Fault), 버그(Bugs) |
| 결과 | 장애(Failure), 문제(Problem) |

---

<!-- p.24 -->

개발자의 사소한 실수 -
시큐어코딩이 적용되지 않은 스마트 컨트랙트

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[기사 캡처] BLOCKCHAIN NEWS — **코인 무한복사 가능? SMT 사태로 시장 폭락…후오비선 출금 중단** (김동호 기자, 2018-04-25)
- SMT토큰 1경 개 이상 복사, 후오비서 이상거래 포착
- 이더리움 기반 토큰 전부 복사 가능은 사실무근…SMT 스마트컨트랙 문제

[거래소 공지 캡처] Huobi.pro 공지 사항 — "Hangco Pro의 모든 통화 인치 통화 서비스 중지에 대한 발표" (2018-04-25): SmartMesh(SMT) 프로젝트에서 비정상적인 거래를 발견해 모든 통화의 입출금을 일시 중지

---

<!-- p.25 -->

개발자의 사소한 실수 -
시큐어코딩이 적용되지 않은 스마트 컨트랙트
오버플로우
오버플로우란 숫자가 최대치 이상으로 증가하는 것을 말한다.
0 1 1 1 1 1 1 1
+ 0 0 0 0 0 0 0 1
0 0 0 0 0 0 0 0

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[그림: 8비트 덧셈으로 보는 오버플로우]

```
    0 1 1 1  1 1 1 1     (= 127, 8비트 부호 있는 정수의 최댓값)
  + 0 0 0 0  0 0 0 1     (= 1)
  ─────────────────
    0 0 0 0  0 0 0 0     (결과가 표현 범위를 넘어 0이 됨)
```
(맨 앞 칸(부호 비트)이 주황색으로 강조됨)

---

<!-- p.26 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[코드에서 주황 상자로 강조된 두 부분]
1. 함수 인자 `(address _from, address _to, uint256 _value, uint256 _feeSmt,` — 공격자가 `_value`와 `_feeSmt`에 매우 큰 값을 넣을 수 있음
2. `if(balances[_from] < _feeSmt + _value) revert();` — **`_feeSmt + _value`가 오버플로우**되면 합이 아주 작은 값이 되어 잔고 검사를 통과해 버림 → 토큰이 무한 생성됨 (SMT 사태의 원인)

---

<!-- p.27 -->

개발자의 사소한 실수 -
시큐어코딩이 적용되지 않은 스마트 컨트랙트
세이프매스(SafeMath)
이더리움 스마트컨트랙트 개발에 많이 사용되는 솔리디티(Solidity)에서는 오버플로우(overflow)와
언더플로우(underflow) 처리를 위해 SafeMath 라이브러리를 제공하고 있음.
라이브러리는 솔리디티에서 특수한 컨트랙트(Contract)

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.28 -->

소프트웨어 보안취약점 사례 – OSS( ) 취약점 공격
Open Source Software

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[기사 캡처 1] **"방치된 오픈소스 사용"** — log4j 교훈 잊었나? 2년 이상 방치된 오픈소스 88%가 사용 중 (출처: 보안뉴스)
- 88%의 조직에서 여전히 최신 오픈소스 업데이트에 미진한 것으로 나타나
- 오픈소스 라이선스 충돌 및 취약점 감소하는 추세
- 시놉시스, '2022 오픈소스 보안과 리스크 분석(OSSRA)' 보고서 발간 — 전 세계 17개 산업분야 2,400여 개 커머셜 코드 베이스 분석
- 2,097개 코드베이스 중 85%가 4년 이상 지난 오픈소스를 포함, 88%는 최신 버전이 아닌 구성 요소 사용, 이중 5%에 취약한 버전의 Log4j 포함
- "관리를 하지 않아 잊혀지고 나면 사용 위치를 파악하여 업데이트하는데 어려움을 겪게 된다. … 소프트웨어 공급망과 소프트웨어 BOM(원재료 명세서, Bill of Materials)이 중요한 이유가 여기에 있다"

[그래프 캡처 2] **"2023 OSSRA 보고서"** — 상용 소프트웨어의 코드베이스 중 76%는 오픈소스…그 중 48%는 고위험군의 보안 취약점 포함 (출처: 2023 OSSRA 보고서)
- 2018~2022년 추이 그래프 (확대 부분 수치): 오픈소스를 포함하는 코드베이스 비율 **96%**, 취약점이 최소 1개 이상 있는 코드베이스 비율 **84%**, 오픈소스인 코드베이스의 코드 비율 **76%**, 고위험 취약점을 포함하는 코드베이스 비율 **48%**

---

<!-- p.29 -->

소프트웨어 보안취약점 사례 – OSS( ) 취약점 공격
Open Source Software
전세계가 두려워했던 Log4j 취약점
- 2021년 11월 24일 Alibaba Cloud 보안팀에 의해 처음 발견
- Java 기반 로깅 도구인 Apache Log4j 라이브러리 원격 코드 실행 취약점
- 공격자가 로그 메시지를 제어할 수 있는 서버에서 로드된 임의의 코드 실행 가능
- Log4j 라이브러리를 사용하는 대부분의 앱이 취약한 것으로 알려짐
출처: 2023년 SW보안약점 진단원 보수 교육

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.30 -->

소프트웨어 보안취약점 사례 – 공급망 해킹
취약한 소프트웨어를 사용하는 기관, 기업등에 피해를 주기 쉬운 공급망 해킹 공격 유행
공격자들은 소프트웨어 개발-설계-구현-유통 단계별 허점 공략

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[도식 1: 위즈베라 해킹 (출처: Welivesecurity)]

1. Attacker → **Compromise** → Web server with VeraPort support (웹서버 해킹)
2. Target PC(WIZVERA VeraPort) → **Configuration request** → Compromised web server (설정 요청)
3. Compromised web server → **Malicious binary** → Target PC (악성 파일이 정상 보안 프로그램 배포 경로로 설치됨)

[도식 2: Solar Winds 해킹 (출처: Prevasio)]

① Attacker가 SolarWinds Company를 침투 → ② 18K Organizations(1만8천 곳 고객사)에 배포 → ③ **Malicious Update**(악성 업데이트)가 Corporation XYZ에 설치 → ④ SolarWinds Orion에 2nd Stage Backdoor(TearDrop) → ⑤ local.corp-xyz.com(Local Domain Name) 수집 → ⑥ Encrypt → Encrypted Domain Name(x8rmf702k.appsync-api.us-west-2.avsvmcloud.com) → ⑦ DNS Query(Passive DNS Sensor) → ⑧ Recursive DNS Server → ⑨ Authoritative DNS Server → ⑩ C2 Server(HTTP)로 연결 → ⑪ 통신 / ⑫ Historic Records를 통해 → ⑬ Decrypt → ⑭ Deduct → 'Corporation XYZ' (Domain Name Recovery: 감염된 기업을 식별)

---

<!-- p.31 -->

소프트웨어 보안 취약점 사례 – 공급망 보안
SBOM(Software Bill of Materials)
소프트웨어를 빌드하기 위해 사용된 여러 컴포넌트에 대한 내용과 공급망 관계를 형식에 맞춰 기록하는 것
소프트웨어 제품을 생산, 소비, 운영하는 자가 공급망에 대해 더 깊이 이해하고 알려진
혹은 새로운 취약점과 위협을 추적하여 알려진 취약점의 확산을 효과적으로 저지하기 위한 목적
소프트웨어개발주기에따른 정보 출처 한국인터넷진흥원

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.32 -->

요약 정리
현대 애플리케이션의 보안과제에서 API 보안과 지속적인 보안에 대해 학습함.
현대 애플리케이션 보안과제를 해결하기 위한 방안으로 SW개발보안, 보안 내재화,
제로트러스트 보안모델 적용을 학습함.
개발자의 사소한 실수로 발생할 수 있는 보안 사고를 예방하기 위해
시큐어코딩이 필수 보안 활동임을 학습함.

---

<!-- p.33 -->

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

<!-- p.34 -->

감사합니다.

---

<!-- p.35 -->

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

<!-- p.36 -->

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
