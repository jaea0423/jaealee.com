# 1-QUESTIONS — 교안 퀴즈 (신뢰도 A)

> 각 차시 교안 끝의 퀴즈와 정답·해설. 교수님이 고른 문제라 시험 1순위 참고. 문제 하나 = 섹션 하나.
> 위치 표기: `[1-QUESTIONS] N주차 M차시 p.X · 퀴즈 K` (p.X = 문제 쪽). 각 섹션의 `출처:` 줄에 문제 쪽·정답 쪽 번호.


# [1-QUESTIONS] 1주차 1차시 — 보안약점과 시큐어코딩 개요
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · MFA/Multi-Factor/다중 인증/다중 매체 인증/OTP/FIDO2/WebAuthn · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [1-QUESTIONS] 1주차 1차시 p.35 · 퀴즈 1
문제: 다음 중 SW개발보안 프로세스에 해당하지 않는 것은?
1) 설계
2) 요구사항분석
3) 테스트
4) 배포
정답: 4) 배포
해설: SW개발보안 프로세스는 1) 요구사항분석 2)설계 3)구현 4)테스트 로 이루어져 있습니다.
출처: [2-SLIDES] 1주차 1차시 p.35 (문제) · p.36 (정답)

## [1-QUESTIONS] 1주차 1차시 p.35 · 퀴즈 2
문제: 제품의 설계단계에서부터 보안을 고려하여 알려진 취약점을 조기에 효과적으로 제거하는 것을 의미하는 것은?
1) DevSecOps
2) 보안내재화
3) 제로트러스트
4) 보안일체화
정답: 2) 보안내재화
해설: 영어 표현으로 Security By Design이라고 합니다.
출처: [2-SLIDES] 1주차 1차시 p.35 (문제) · p.36 (정답)

## [1-QUESTIONS] 1주차 1차시 p.35 · 퀴즈 3
문제: 다음 중 '오버플로우'에 대한 설명이 맞는 것은?
1) 연산 결과가 과하게 반올림됨
2) 연산 결과가 허용할 수 있는 범위를 벗어남
3) 연산 결과의 부호가 역전됨
4) 정수형과 실수형을 혼합하여 연산함
정답: 2) 연산 결과가 허용할 수 있는 범위를 벗어남
해설: 저장할 수 있는 값의 범위를 초과하는 연산이 이루어질 때, '오버플로우'가 발생했다고 합니다.
출처: [2-SLIDES] 1주차 1차시 p.35 (문제) · p.36 (정답)

# [1-QUESTIONS] 1주차 2차시 — 보안약점과 시큐어코딩 개요
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [1-QUESTIONS] 1주차 2차시 p.20 · 퀴즈 1
문제: 다음 중 행정안전부 SW개발보안 가이드와 관련 없는 내용은?
1) 행정, 공공기관 정보시스템 개발자 대상
2) SW보안약점 잔존여부 진단
3) 테스트 단계부터 SW개발 보안을 적용하기 위한 기준
4) 진단 범위는 설계 단계 산출물과 소스코드 전체
정답: 3) 테스트 단계부터 SW개발 보안을 적용하기 위한 기준
해설: SW개발보안 가이드는 SW개발 단계부터 보안을 적용하기 위한 기준을 제시하고 있습니다.
출처: [2-SLIDES] 1주차 2차시 p.20 (문제) · p.21 (정답)

## [1-QUESTIONS] 1주차 2차시 p.20 · 퀴즈 2
문제: 다음 중 클라우드 서비스 보안 인증과 관련하여, 소프트웨어 보안과 관련된 통제 항목이 아닌 것은?
1) 접근통제
2) 시스템 개발 및 운영 보안
3) 취약점 관리
4) 개발 조직의 신원 관리 및 통제
정답: 4) 개발 조직의 신원 관리 및 통제
해설: 개발 조직 관리는 소프트웨어 보안과 관련이 없습니다.
출처: [2-SLIDES] 1주차 2차시 p.20 (문제) · p.21 (정답)

## [1-QUESTIONS] 1주차 2차시 p.20 · 퀴즈 3
문제: 다음 중 클라우드 서비스 보안 인증을 나타내는 용어는?
1) CSAP
2) CCSP
3) SaaS
4) PaaS
정답: 1) CSAP
해설: CSAP는 Cloud Security Assurance Program의 약어입니다.
출처: [2-SLIDES] 1주차 2차시 p.20 (문제) · p.21 (정답)

# [1-QUESTIONS] 1주차 3차시 — 보안약점과 시큐어코딩 개요
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · SameSite/세임사이트/Strict/Lax/None · 화이트리스트/Whitelist/최소 허용/허용 목록 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Mass Assignment/대량 할당/DTO/isAdmin · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · MFA/Multi-Factor/다중 인증/다중 매체 인증/OTP/FIDO2/WebAuthn · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [1-QUESTIONS] 1주차 3차시 p.49 · 퀴즈 1
문제: 다음 중 '취약한 접근 통제' 취약점에 대한 설명이 맞는 것은?
1) 인증된 사용자가 접근이 제한된 데이터나 기능에 접근 가능
2) 손쉬운 암호 설정으로 인해 부루트포스 공격 가능
3) 없는 주소를 입력하였을 때 에러 메시지와 함께 서버 정보 노출
4) 틀린 암호를 무제한으로 시도 가능
정답: 1) 인증된 사용자가 접근이 제한된 데이터나 기능에 접근 가능
해설: 취약한 접근 통제 취약점은 적절한 인가 처리가 이루어지지 않아서 중요한 리소스 또는 기능이 권한 없는 사용자에게 노출될 수 있는 취 약점을 말합니다.
출처: [2-SLIDES] 1주차 3차시 p.49 (문제) · p.50 (정답)

## [1-QUESTIONS] 1주차 3차시 p.49 · 퀴즈 2
문제: 다음 중 '인젝션 공격'에 대한 설명으로 틀린 것은?
1) 악성 코드를 삽입하는 공격이다.
2) 사용자 입력값을 검증하고 필터링하면 방어할 수 있다.
3) 커맨드 인젝션 방어를 위해 Prepared Statement를 사용해야 한다.
4) 주로 사용자의 입력값을 그대로 파라미터로 사용할 때 발생한다.
정답: 3) 커맨드 인젝션 방어를 위해 Prepared Statement를 사용해야 한다.
해설: Prepared Statement 는 데이터베이스를 조작할 떄 쿼리를 만드는 방법이며, SQL 인젝션을 예방할 수 있습니다.
출처: [2-SLIDES] 1주차 3차시 p.49 (문제) · p.50 (정답)

## [1-QUESTIONS] 1주차 3차시 p.49 · 퀴즈 3
문제: 다음 중 CVE와 CWE에 대해서 잘못 이야기한 것은?
1) CVE는 소프트웨어와 하드웨어 보안 취약점을 공개한 시스템이다.
2) 보안 연구원, 기업, 기관이 발견한 취약점은 CNA에 보고된다.
3) CWE Top 25는 보안 취약점 중 가장 위험한 25가지를 선정한 목록이다.
4) 특정제품에서 발견된 취약점은 CVE 목록에서 찾을 수 있다.
정답: 3) CWE Top 25는 보안 취약점 중 가장 위험한 25가지를 선정한 목록이다.
해설: CWE는 보안 약점 목록을 말하며, 보안 취약점 목록은 CVE 입니다.
출처: [2-SLIDES] 1주차 3차시 p.49 (문제) · p.50 (정답)

# [1-QUESTIONS] 2주차 1차시 — SW개발보안 방법론·위협 모델링
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Authentication/인증/로그인 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [1-QUESTIONS] 2주차 1차시 p.22 · 퀴즈 1
문제: 다음 중 SW개발보안 방법론의 주요 개념이 아닌 것은?
1) 지속적인 보안 점검
2) 보안 내재화
3) SBOM 다중화
4) 취약점 최소화
정답: 3) SBOM 다중화
해설: SW개발보안 방법론의 주요 개념은 보안 내재화, 취약점 최소화, 지속적인 보안 점검입니다.
출처: [2-SLIDES] 2주차 1차시 p.22 (문제) · p.23 (정답)

## [1-QUESTIONS] 2주차 1차시 p.22 · 퀴즈 2
문제: 다음 중 SW 결함 수정비용이 가장 많이 필요한 경우는?
1) 코딩과정 발생한 결함이 통합 단계에서 발견된 경우
2) 설계과정 발생한 결함이 제품 출시 단계에서 발견된 경우
3) 설계과정 발생한 결함이 코딩 단계에서 발견된 경우
4) 통합과정 발생한 결함이 제품출시 단계에서 발견된 경우
정답: 2) 설계과정 발생한 결함이 제품 출시 단계에서 발견된 경우
해설: 개발의 최초 과정에서 발생한 결함이 최종 출시 단계까지 가서 알게 된다면 가장 많은 수정비용이 발생합니다. (위 표 기준 30배)
출처: [2-SLIDES] 2주차 1차시 p.22 (문제) · p.23 (정답)

## [1-QUESTIONS] 2주차 1차시 p.22 · 퀴즈 3
문제: 다음 중 MS-SDL 보안개발 방법론에 대한 설명 중 틀린 것은?
1) 보안 문제를 사전에 차단한다.
2) 요구사항 정의 단계에 위협 모델링을 수행한다.
3) 구현 단계에서 정적 분석을 수행한다.
4) 배포 단계에서 보안 가이드 문서를 제공한다.
정답: 2) 요구사항 정의 단계에 위협 모델링을 수행한다.
해설: 위협 모델링은 설계 단계에 수행하는 내용에 해당합니다.
출처: [2-SLIDES] 2주차 1차시 p.22 (문제) · p.23 (정답)

## [1-QUESTIONS] 2주차 1차시 p.22 · 비고

# [1-QUESTIONS] 2주차 2차시 — SW개발보안 방법론·위협 모델링
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · MFA/Multi-Factor/다중 인증/다중 매체 인증/OTP/FIDO2/WebAuthn · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [1-QUESTIONS] 2주차 2차시 p.28 · 퀴즈 1
문제: 다음 중 위협모델링의 핵심 목표가 아닌 것은?
1) 위험 평가
2) 보안 조치 적용
3) 시스템 이해
4) SW 구조 이해
정답: 4) SW 구조 이해
해설: 위협 모델링의 핵심 목표는 시스템 이해, 위협 식별, 위험 평가, 보안 조치 적용입니다.
출처: [2-SLIDES] 2주차 2차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 2주차 2차시 p.28 · 퀴즈 2
문제: 다음 중 위협모델링 프로세스 단계에 대한 내용이 틀린 것은?
1) 시스템 정의 - 구성원간 상호 협업 시스템을 명확히 정의
2) 위협 식별 - 발생할 수 있는 잠재적 위협을 식별
3) 완화 계획 수립 - 보안조치를 설계하고 구현
4) 검토 및 개선 - 결과를 검토하고 지속적으로 개선
정답: 1) 시스템 정의
해설: 구성원간 상호 협업 시스템을 명확히 정의 — 시스템 정의 단계에서는 위협 모델링을 수행하기 위해 보호할 대상을 명확히 정의하게 됩니다.
출처: [2-SLIDES] 2주차 2차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 2주차 2차시 p.28 · 퀴즈 3
문제: 다음 중 STRIDE 프레임워크에서 정의한 주요 위협요소에 대한 설명으로 올바른 것은?
1) 신원 위조 - 사용자가 악의적인 행동을 부인 가능
2) 권한 상승 - 기밀 데이터가 외부에 노출
3) 서비스 거부 - 시스템을 사용할 수 없도록 하는 공격
4) 정보 노출 - 데이터가 불법적으로 변경되거나 조작됨
정답: 3) 서비스 거부
해설: 시스템을 사용할 수 없도록 하는 공격 — 서비스 거부 보안 위협은 트래픽 제한, WAF 도입, DDoS 보호 서비스 적용 등으로 대응책을 마련할 수 있습니다.
출처: [2-SLIDES] 2주차 2차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 2주차 2차시 p.28 · 비고

# [1-QUESTIONS] 2주차 3차시 — SW개발보안 방법론·위협 모델링
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [1-QUESTIONS] 2주차 3차시 p.21 · 퀴즈 1
문제: 다음 중 위협모델링 도구 선정 기준으로 가장 적합하지 않은 것은?
1) 자동화 지원 여부
2) 보안 프레임워크 지원 여부
3) 무료/유료 여부
4) CWE/CVE 연계 분석 여부
정답: 4) CWE/CVE 연계 분석 여부
해설: 위협모델링 도구는 소프트웨어 약점 및 취약점 목록과 직접적인 연관을 가질 필요는 없습니다.
출처: [2-SLIDES] 2주차 3차시 p.21 (문제) · p.22 (정답)

## [1-QUESTIONS] 2주차 3차시 p.21 · 퀴즈 2
문제: 다음 중 데이터 흐름 다이어그램(DFD)의 주요 구성요소가 아닌 것은?
1) Process
2) Data Flow
3) External Interactor
4) Module
정답: 4) Module
해설: DFD의 주요 구성 요소는 External Interactor, Process, Data Store, Data Flow 입니다.
출처: [2-SLIDES] 2주차 3차시 p.21 (문제) · p.22 (정답)

## [1-QUESTIONS] 2주차 3차시 p.21 · 퀴즈 3
문제: 다음 중 데이터 흐름 다이어그램(DFD)를 작성하는 단계는?
1) 시스템 이해 및 범위 정의
2) 위협 식별
3) 위협 평가 및 대응 우선 순위 결정
4) 위협 완화 및 대응 전략 수립
정답: 1) 시스템 이해 및 범위 정의
해설: 데이터 흐름을 도식으로 그려보는 것은 전체 시스템의 주요 정보 흐름을 이해하기 위해 이루어집니다.
출처: [2-SLIDES] 2주차 3차시 p.21 (문제) · p.22 (정답)

# [1-QUESTIONS] 3주차 1차시 — Spring Boot 개발 환경·실습
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트

## [1-QUESTIONS] 3주차 1차시 p.48 · 퀴즈 1
문제: 다음 중 웹 애플리케이션 서버 로직의 3대 계층에 속하지 않는 것은?
1) 데이터 계층
2) 네트워크 계층
3) 비즈니스 계층
4) 프레젠테이션 계층
정답: 2) 네트워크 계층
해설: 웹 애플리케이션 서버 로직은 프레젠테이션 계층, 비즈니스 계층, 데이터 계층으로 구성되어 있습니다.
출처: [2-SLIDES] 3주차 1차시 p.48 (문제) · p.49 (정답)

## [1-QUESTIONS] 3주차 1차시 p.48 · 퀴즈 2
문제: 다음 중 HTTP에 대한 설명으로 옳은 것은?
1) 무상태 방식
2) UDP를 기본적으로 사용
3) Request Method로 GET, POST, PUT, REMOVE 등이 있음
4) Response Status Code로 2xx는 서버에 에러가 있다는 의미
정답: 1) 무상태 방식
해설: HTTP는 주로 TCP기반 무상태 방식으로 통신하며, GET, POST, PUT, DELETE 등의 Request Method를 사용합니다. Response Status Code가 2xx인 경우는 요청이 성공적으로 이루어졌다는 의미입니다.
출처: [2-SLIDES] 3주차 1차시 p.48 (문제) · p.49 (정답)

## [1-QUESTIONS] 3주차 1차시 p.48 · 퀴즈 3
문제: 다음 중 BASE64 인코딩에 대한 내용으로 틀린 것은?
1) 이메일, JSON, XML 등 텍스트 전송 환경에서 안전하게 사용
2) 부족한 비트는 0으로 패딩 처리되며, =로 표현
3) 데이터 손상 및 인코딩 문제를 방지함
4) 데이터를 8비트 단위로 분할하며, 총 64개의 문자 집합으로 표현
정답: 4) 데이터를 8비트 단위로 분할하며, 총 64개의 문자 집합으로 표현
해설: BASE64는 데이터를 6비트 단위로 분할합니다.
출처: [2-SLIDES] 3주차 1차시 p.48 (문제) · p.49 (정답)

## [1-QUESTIONS] 3주차 1차시 p.48 · 비고

# [1-QUESTIONS] 3주차 2차시 — Spring Boot 개발 환경·실습
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [1-QUESTIONS] 3주차 2차시 p.22 · 퀴즈 1
문제: 다음 중 프레임워크와 플랫폼에 대한 설명 중 옳은 것은?
1) 플랫폼은 재사용 가능한 코드 라이브러리이다.
2) Spring(Java)는 가장 대표적인 운영 플랫폼 중 하나이다.
3) 프레임워크는 특정한 개발방식(패턴)을 강제한다.
4) 프레임워크는 하드웨어와 소프트웨어의 조합을 포함한다.
정답: 3) 프레임워크는 특정한 개발방식(패턴)을 강제한다.
해설: 프레임워크는 강제하는 소프트웨어 개발 패턴과 관련된 코드 라이브러리 모음이며, 플랫폼은 애플리케이션이 실행될 수 있는 하드웨어 및 소프트웨어의 기반을 지칭하는 용어입니다.
출처: [2-SLIDES] 3주차 2차시 p.22 (문제) · p.23 (정답)

## [1-QUESTIONS] 3주차 2차시 p.22 · 퀴즈 2
문제: 다음 중 프레임워크별 지원 언어에 대한 설명이 잘못된 것은?
1) Django - Python
2) Spring - Java
3) React - Javascript
4) Ruby on Rails - C/C++
정답: 4) Ruby on Rails
해설: C/C++ Ruby on Rails는 Ruby 언어 기반으로 운영되는 웹 개발 프레임워크입니다.
출처: [2-SLIDES] 3주차 2차시 p.22 (문제) · p.23 (정답)

## [1-QUESTIONS] 3주차 2차시 p.22 · 퀴즈 3
문제: 다음 중 Spring Framework와 비교하여 Spring Boot의 장점이 아닌 것은?
1) Tomcat이 내장되어 있음
2) WAR 패키징
3) 자동 설정 지원
4) 간편하게 의존성 관리
정답: 2) WAR 패키징
해설: Spring Boot Framework는 JAR 패키징을 지원하여 독립적인 실행이 가능합니다.
출처: [2-SLIDES] 3주차 2차시 p.22 (문제) · p.23 (정답)

## [1-QUESTIONS] 3주차 2차시 p.22 · 비고

# [1-QUESTIONS] 3주차 3차시 — Spring Boot 개발 환경·실습
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Mass Assignment/대량 할당/DTO/isAdmin

## [1-QUESTIONS] 3주차 3차시 p.20 · 퀴즈 1
문제: 다음 중, Spring Boot 개발 방법론에서 계층별 설명이 잘못된 것은?
1) Controller - Request에 대한 처리 로직
2) DTO - 데이터 엔티티 모델링
3) Repository - 데이터베이스와 상호작용 담당
4) Service - 화면 UI 처리 로직
정답: 4) Service
해설: 화면 UI 처리 로직 서비스 계층은 비즈니스 로직을 처리하는 계층입니다.
출처: [2-SLIDES] 3주차 3차시 p.20 (문제) · p.21 (정답)

## [1-QUESTIONS] 3주차 3차시 p.20 · 퀴즈 2
문제: 게시판 만들기 실습에서 사용한 테스트용 In-Memory DB의 이름은? (2글자) ( )
정답: ( H2 )
출처: [2-SLIDES] 3주차 3차시 p.20 (문제) · p.21 (정답)

## [1-QUESTIONS] 3주차 3차시 p.20 · 퀴즈 3
문제: 다음 중, 게시판 만들기 실습 내용에 대한 설명 중 잘못된 것은?
1) PUT /posts - 게시글 생성
2) DELETE /posts/{id} - 게시글 삭제
3) GET /posts/{id} - 특정 게시물 조회
4) GET /posts - 게시글 목록 조회
정답: 1) PUT /posts
해설: 게시글 생성 게시글을 생성할 때에는 POST를 사용하며, PUT은 게시글을 수정할 때 사용합니다.
출처: [2-SLIDES] 3주차 3차시 p.20 (문제) · p.21 (정답)

# [1-QUESTIONS] 4주차 1차시 — 정규식과 입력값 검증·XSS 필터
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet

## [1-QUESTIONS] 4주차 1차시 p.20 · 퀴즈 1
문제: 정규식에서 `^` (Caret) 기호의 의미로 알맞은 것은?
1) 특정 단어를 강조하는 역할
2) 문자열의 시작을 의미
3) 숫자만 매칭하는 역할
4) 공백을 무시하는 역할
정답: 2) 문자열의 시작을 의미
해설: `^hello`라는 정규식은 "hello"로 시작하는 문자열을 찾습니다.
출처: [2-SLIDES] 4주차 1차시 p.20 (문제) · p.21 (정답)

## [1-QUESTIONS] 4주차 1차시 p.20 · 퀴즈 2
문제: 다음 중 정규식 `a?b`가 매칭할 수 있는 문자열은 무엇일까요? (2개)
1) b
2) ab
3) aabb
4) abc
정답: 1) b, 2) ab
해설: `?`는 앞의 문자가 0번 또는 1번 나올 수 있음을 의미합니다.
출처: [2-SLIDES] 4주차 1차시 p.20 (문제) · p.21 (정답)

## [1-QUESTIONS] 4주차 1차시 p.20 · 퀴즈 3
문제: 정규식을 사용할 때, 특정 문자가 한 번 이상 반복될 경우 사용할 수 있는 기호는 무엇일까요?　(　　)
정답: ( + ) — `+`는 앞에 나온 문자가 한 번 이상 반복될 경우 매칭할 때 사용합니다.
출처: [2-SLIDES] 4주차 1차시 p.20 (문제) · p.21 (정답)

## [1-QUESTIONS] 4주차 1차시 p.20 · 비고

# [1-QUESTIONS] 4주차 2차시 — 정규식과 입력값 검증·XSS 필터
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · ReDoS/레도스/백트래킹/Backtracking · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [1-QUESTIONS] 4주차 2차시 p.28 · 퀴즈 1
문제: 다음 리눅스 명령어 중 정규식을 활용할 수 없는 것은?
1) grep
2) sed
3) ps
4) awk
정답: 3) ps
해설: ps는 프로세스의 리스트를 보는 명령어이며, 자체적으로는 정규식을 지원하지 않습니다.
출처: [2-SLIDES] 4주차 2차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 4주차 2차시 p.28 · 퀴즈 2
문제: 자바 프로그램에서 정규식을 받아들여 패턴을 정의하는데 사용하는 클래스명은?　(　　)
정답: ( Pattern )
출처: [2-SLIDES] 4주차 2차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 4주차 2차시 p.28 · 퀴즈 3
문제: 다음 중 정규식 사용시 발생 가능한 문제점이 아닌것은?
1) DDoS 보안문제
2) 미매칭 문제
3) 성능 문제
4) 과도한 매칭
정답: 1) DDoS 보안 문제
해설: DDoS는 분산형 서비스 거부이며, 정규식으로 발생될 수 있는 보안 문제는 수많은 백트래킹으로 인한 성능저하를 일으키는 ReDoS 보안 문제임.
출처: [2-SLIDES] 4주차 2차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 4주차 2차시 p.28 · 비고
※ 정답 쪽의 3번 문제 문장("정규식 성능 저하의 원인이 아닌 것은?")이 퀴즈 쪽("정규식 사용시 발생 가능한 문제점이 아닌것은?")과 다르게 적혀 있습니다. 정답은 같습니다.

# [1-QUESTIONS] 4주차 3차시 — 정규식과 입력값 검증·XSS 필터
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · CORS/코어스/Cross-Origin/교차 출처

## [1-QUESTIONS] 4주차 3차시 p.26 · 퀴즈 1
문제: 클라이언트의 HTTP 요청과 응답을 가로채어 특정 작업을 수행하는 서블릿 기반 컴포넌트는 무엇인가?
1) Dispatcher
2) Handler
3) Filter
4) ViewResolver
정답: 3) Filter
해설: ※ 원본 정답 쪽에는 "2) Filter"로 인쇄되어 있지만, 문제의 보기에서 Filter는 3번입니다(2번은 Handler).
출처: [2-SLIDES] 4주차 3차시 p.26 (문제) · p.27 (정답)

## [1-QUESTIONS] 4주차 3차시 p.26 · 퀴즈 2
문제: String 클래스에서 정규식으로 지정한 문자열을 다른 문자열로 바꾸기 위해 사용하는 메서드 이름은? (영문 10글자, . 제외)　(　　)
정답: ( replaceAll )
출처: [2-SLIDES] 4주차 3차시 p.26 (문제) · p.27 (정답)

## [1-QUESTIONS] 4주차 3차시 p.26 · 퀴즈 3
문제: 다음 중 XSS 입력값 필터에서 처리해야 하는 내용이 아닌 것은?
1) <script> 태그와 그 사이 내용을 제거
2) javascript: 문자열 제거
3) onclick, onerror 등의 이벤트 핸들러 제거
4) 압축파일 안에 들어있는 스크립트 파일 제거
정답: 4) 압축파일 안에 들어있는 스크립트 파일 제거
해설: 압축파일을 다루는 작업은 필터에서 처리하기에 매우 많은 리소스를 사용하며, XSS 공격 방어와도 관련이 없습니다.
출처: [2-SLIDES] 4주차 3차시 p.26 (문제) · p.27 (정답)

## [1-QUESTIONS] 4주차 3차시 p.26 · 비고

# [1-QUESTIONS] 5주차 1차시 — 인증과 인가 · OAuth2 · JWT
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · SameSite/세임사이트/Strict/Lax/None · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · MFA/Multi-Factor/다중 인증/다중 매체 인증/OTP/FIDO2/WebAuthn · HSTS/HTTP Strict-Transport-Security/스트릭트 트랜스포트 · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트

## [1-QUESTIONS] 5주차 1차시 p.27 · 퀴즈 1
문제: 다음 중 인증과 인가에 대한 설명 중 잘못된 것은?
1) 인증은 사용자에게 리소스 접근 가능한 권한을 부여하는 것
2) 인가는 권한을 제한하는 것도 포함함
3) 인증은 이 사람이 누구인가를 확인하는 과정
4) 인가를 통해 사용자를 등급별로 구분할 수 있게 됨
정답: 1) 인증은 사용자에게 리소스 접근 가능한 권한을 부여하는 것
해설: 인증을 통해 누구인지 확인한 다음, 인가 과정을 통해 그 사용자에게 허용둰 권한을 부여합니다.
출처: [2-SLIDES] 5주차 1차시 p.27 (문제) · p.28 (정답)

## [1-QUESTIONS] 5주차 1차시 p.27 · 퀴즈 2
문제: 사용자의 역할에 따라 접근 권한을 부여하는 방식을 나타내는 용어는? (영문 4글자) ( )
정답: ( RBAC )
출처: [2-SLIDES] 5주차 1차시 p.27 (문제) · p.28 (정답)

## [1-QUESTIONS] 5주차 1차시 p.27 · 퀴즈 3
문제: 다음중 인가 보안 위협에 대한 대응 방안은?
1) 최소권한의 원칙
2) 강력한 비밀번호 정책
3) CAPCHA 적용
4) 다중인증
정답: 1) 최소권한원칙
해설: 모든 사용자는 필요한 최소한의 권한만 부여 [이미지 보충] 정답 '1) 인증은 사용자에게 리소스 접근 가능한 권한을 부여하는 것', 'RBAC', '1) 최소권한원칙'은 빨간 글씨로 강조됨.
출처: [2-SLIDES] 5주차 1차시 p.27 (문제) · p.28 (정답)

## [1-QUESTIONS] 5주차 1차시 p.27 · 비고
(※ 원문 표기 그대로 — 3번 보기 3) 'CAPCHA'는 'CAPTCHA'의 오타. 2번은 빈칸 '(          )'에 답을 쓰는 주관식)
(※ 원문 표기 그대로 — 추출 텍스트의 '허용둰 권한'은 '허용된 권한'의 오타로 보이며, 렌더링 이미지에서는 해당 글자가 보이지 않고 '허용    권한'처럼 빈칸으로 표시됨)

# [1-QUESTIONS] 5주차 2차시 — 인증과 인가 · OAuth2 · JWT
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · MyBatis/마이바티스/Mapper/매퍼/#{}/${}/동적 SQL · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · Refresh Token/리프레시 토큰/토큰 회전/Rotation · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin

## [1-QUESTIONS] 5주차 2차시 p.40 · 퀴즈 1
문제: 다음 중 OAuth2에 대한 설명으로 맞지 않는 것은?
1) 인증과 인가를 분리한 프로토콜
2) 제3자 애플리케이션이 사용자의 자원에 접근하도록 허용
3) 토큰 기반 인증 사용
4) 비밀번호를 통해 접근 권한을 위임
정답: 4) 비밀번호를 통해 접근 권한을 위임
해설: OAuth2는 기존 OAuth 1.0의 비밀번호 유출시 취약해질 수 있는 보안을 강화하기 위해 토큰 기반 인증을 사용합니다.
출처: [2-SLIDES] 5주차 2차시 p.40 (문제) · p.41 (정답)

## [1-QUESTIONS] 5주차 2차시 p.40 · 퀴즈 2
문제: OAuth2의 구성 요소에 대한 설명 중 잘못된 것은?
1) Resource Owner - 리소스 서비스 업체
2) Resource Server - 보호된 리소스를 보유하고 있는 서버
3) Authorization Server - 사용자 인증과 권한 부여처리, 액세스 토큰 발급
4) Client Application - 보호된 리소스에 접근하려는 애플리케이션
정답: 1) Resource Owner
해설: 리소스 서비스 업체 리소스에 대한 소유 또는 접근 권한을 가지고 있는 것은 사용자입니다.
출처: [2-SLIDES] 5주차 2차시 p.40 (문제) · p.41 (정답)

## [1-QUESTIONS] 5주차 2차시 p.40 · 퀴즈 3
문제: Access Token 재발급을 위한 장기 인증 수단으로, 사용자 재로그인 없이 새로운 Access Token을 발급하기 위해 사용하는 Token의 이름은 무엇인가요? (영문 소문자만) ( )
정답: ( refresh )
출처: [2-SLIDES] 5주차 2차시 p.40 (문제) · p.41 (정답)

## [1-QUESTIONS] 5주차 2차시 p.40 · 비고
(정답 표시: 1번 '4) 비밀번호를 통해 접근 권한을 위임', 2번 '1) Resource Owner - 리소스 서비스 업체', 3번 'refresh'가 빨간 글씨로 강조됨. 각 정답 아래 검은 글씨는 해설)

# [1-QUESTIONS] 5주차 3차시 — 인증과 인가 · OAuth2 · JWT
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · SameSite/세임사이트/Strict/Lax/None · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · Refresh Token/리프레시 토큰/토큰 회전/Rotation · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin

## [1-QUESTIONS] 5주차 3차시 p.30 · 퀴즈 1
문제: JWT의 주요 특징에 해당하지 않는 것은?
1) 위변조 확인을 위한 서명 포함
2) 경량
3) 사용자 정보, 만료시간 등의 정보 자체 포함
4) 헤더-페이로드-트레일러 로 구성
정답: 4) 헤더-페이로드-트레일러 로 구성
해설: JWT는 헤더-페이로드-서명 으로 구성되어 있는 토큰 형식입니다.
출처: [2-SLIDES] 5주차 3차시 p.30 (문제) · p.31 (정답)

## [1-QUESTIONS] 5주차 3차시 p.30 · 퀴즈 2
문제: JWT의 단점 중 틀린 것은?
1) 만료 시간 전 강제 무효화를 위한 관리자 페이지 필요
2) 토큰 탈취 위험
3) 정보 노출 문제
4) 과다한 크기로 전송 오버헤드 발생 가능성
정답: 1) 만료 시간 전 강제 무효화를 위한 관리자 페이지 필요
해설: JWT는 기본적으로, 만료 기간 전에 강제로 만료할 수 있는 방법이 없습니다.
출처: [2-SLIDES] 5주차 3차시 p.30 (문제) · p.31 (정답)

## [1-QUESTIONS] 5주차 3차시 p.30 · 퀴즈 3
문제: JWT 페이로드에 포함시키는 사용자 식별자, 역할, 권한 등의 정보를 일컫는 단어는? ( )
정답: ( 클레임 또는 claim )
출처: [2-SLIDES] 5주차 3차시 p.30 (문제) · p.31 (정답)

## [1-QUESTIONS] 5주차 3차시 p.30 · 비고

# [1-QUESTIONS] 6주차 1차시 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · MyBatis/마이바티스/Mapper/매퍼/#{}/${}/동적 SQL · Dirty Checking/더티 체킹/변경 감지 · Mass Assignment/대량 할당/DTO/isAdmin · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT

## [1-QUESTIONS] 6주차 1차시 p.28 · 퀴즈 1
문제: 다음 중 ORM(Object-Relational Mapping)의 주요 장점이 아닌 것은?
1) 객체와 RDB간의 매핑을 자동화하여 개발 생산성을 높일 수 있음
2) SQL을 직접 만들지 않아도 CRUD 및 복잡한 쿼리 수행이 가능
3) 모든 SQL 최적화를 자동으로 수행하여 성능 문제 없음
4) 데이터베이스 종속성을 줄이고 유지보수를 용이하게 함
정답: 3) 모든 SQL 최적화를 자동으로 수행하여 성능 문제 없음
해설: ORM은 자동 최적화 기능이 없으며, 복잡한 쿼리의 경우 성능 튜닝이 필요합니다.
출처: [2-SLIDES] 6주차 1차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 6주차 1차시 p.28 · 퀴즈 2
문제: MyBatis 프레임워크의 특징으로 적절한 것은?
1) SQL 작성하지 않고 객체 조작만으로 DB 작업을 수행
2) SQL을 직접 작성하면서도 매핑 작업을 줄여 생산성을 높임
3) 완전한 객체-관계 매핑으로 DB 구조를 자동으로 변경 가능
4) 기본적으로 동적 SQL을 지원하지 않음
정답: 2) SQL을 직접 작성하면서도 매핑 작업을 줄여 생산성을 높임
해설: MyBatis는 ORM과 달리 SQL을 직접 작성해야 하지만, 매핑을 도와주는 기능을 제공하여 반복 작업을 줄이고 생산성 을 높입니다.
출처: [2-SLIDES] 6주차 1차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 6주차 1차시 p.28 · 퀴즈 3
문제: ORM을 잘못 사용할 경우 발생할 수 있는 대표적인 보안 취약점 중 하나로, SQL 쿼리를 문자열 결합 방식으로 생성할 때 발생할 수 있는 공격 기법은 무엇인가? ( &nbsp; &nbsp; &nbsp; &nbsp; )
정답: ( SQL Injection 또는 SQL 인젝션 )
출처: [2-SLIDES] 6주차 1차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 6주차 1차시 p.28 · 비고
[정답 표시: 1번 "3) 모든 SQL 최적화를 자동으로 수행하여 성능 문제 없음", 2번 "2) SQL을 직접 작성하면서도 매핑 작업을 줄여 생산성을 높임", 3번 "SQL Injection", "SQL 인젝션"이 빨간 글씨로 강조됨 (해설 문장은 검은 글씨)]

# [1-QUESTIONS] 6주차 2차시 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · 화이트리스트/Whitelist/최소 허용/허용 목록 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · MyBatis/마이바티스/Mapper/매퍼/#{}/${}/동적 SQL · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SQLMap/에스큐엘맵 · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [1-QUESTIONS] 6주차 2차시 p.33 · 퀴즈 1
문제: 다음 중 SQL 인젝션을 예방하기 위한 방법으로 옳지 않은 것은 무엇일까요?
1) PreparedStatement(또는 파라미터 바인딩)를 사용한다.
2) 사용자 입력값을 길이·형식·특수문자 등에 대해 검증한다.
3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.
4) 데이터베이스 에러 메시지를 사용자에게 그대로 노출하지 않는다.
정답: 3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.
해설: 문자열 결합을 통해 쿼리를 직접 작성하면 인젝션 위험이 커집니다.
출처: [2-SLIDES] 6주차 2차시 p.33 (문제) · p.34 (정답)

## [1-QUESTIONS] 6주차 2차시 p.33 · 퀴즈 2
문제: 다음 중 SQL 인젝션 공격으로 인해 발생할 수 있는 피해가 아닌 것은 무엇일까요?
1) 데이터베이스에서 민감 정보가 유출된다.
2) 관리자 계정으로 인증을 우회할 수 있다.
3) 서버의 파일이 삭제되거나 변경될 수 있다.
4) 네트워크 장비가 물리적으로 파손된다.
정답: 4) 네트워크 장비가 물리적으로 파손된다.
해설: SQL 인젝션은 주로 DB 및 서버 내부 데이터 조작에 영향을 미치며, 물리적 장비 파손은 직접적인 영향 범위가 아닙니다.
출처: [2-SLIDES] 6주차 2차시 p.33 (문제) · p.34 (정답)

## [1-QUESTIONS] 6주차 2차시 p.33 · 퀴즈 3
문제: SQL 인젝션 방어를 위해 Java에서 동적 SQL 대신 권장되는 JDBC API 클래스 이름은? ( )
정답: ( PreparedStatement )
해설: 슬라이드 표시: 정답 줄('3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.', '4) 네트워크 장비가 물리적으로 파손된다.', 'PreparedStatement')은 빨간색, 해설은 검은색. 좌상단 'Quiz' 돋보기 아이콘.
출처: [2-SLIDES] 6주차 2차시 p.33 (문제) · p.34 (정답)

## [1-QUESTIONS] 6주차 2차시 p.33 · 비고
(좌상단 'Quiz' 돋보기 아이콘)

# [1-QUESTIONS] 6주차 3차시 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · 화이트리스트/Whitelist/최소 허용/허용 목록 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [1-QUESTIONS] 6주차 3차시 p.22 · 퀴즈 1
문제: 다음 중 Windows 환경에서 Command 인젝션 위험을 줄이기 위한 방법으로 가장 옳은 것은 ?
1) 문자열 결합으로 명령어를 만들고, 관리자 권한으로 실행한다.
2) 사용자 입력을 전혀 검증하지 않고 바로 cmd.exe /c에 전달한다.
3) 명령 인자를 배열로 분리하고, 권한이 제한된 계정으로 실행한다.
4) PowerShell 스크립트를 항상 시스템 권한으로만 실행한다.
정답: 3) 명령 인자를 배열로 분리하고, 권한이 제한된 계정으로 실행한다.
해설: 인자를 배열로 분리하고, 최소 권한 계정을 사용해야 인젝션 위험이 낮아집니다.
출처: [2-SLIDES] 6주차 3차시 p.22 (문제) · p.23 (정답)

## [1-QUESTIONS] 6주차 3차시 p.22 · 퀴즈 2
문제: 다음 중 Command 인젝션 공격 예시로 볼 수 있는 것은 ?
1) `ls –al`
2) `dir C:\Users`
3) `ls; rm -rf /`
4) `ping 127.0.0.1`
정답: 3) ls; rm -rf /
해설: 세미콜론 ;을 사용해 기존 명령 뒤에 rm -rf /를 추가로 실행하므로, 전형적인 인젝션 공격 시도입니다.
출처: [2-SLIDES] 6주차 3차시 p.22 (문제) · p.23 (정답)

## [1-QUESTIONS] 6주차 3차시 p.22 · 퀴즈 3
문제: Linux 환경에서 명령어를 연속 실행하기 위해 자주 사용되는 쉘 연산자 기호를 정확히 쓰세요. ( )
정답: ( ; )
출처: [2-SLIDES] 6주차 3차시 p.22 (문제) · p.23 (정답)

## [1-QUESTIONS] 6주차 3차시 p.22 · 비고
(※ 원문 표기 그대로 — 1)번 `ls –al` 의 하이픈이 일반 하이픈(-)이 아닌 en dash(–)로 입력되어 있음)

# [1-QUESTIONS] 7주차 1차시 — 프론트엔드 데이터 처리 / XSS / CSRF
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · DOM XSS/DOM 기반 XSS/돔 기반/document.write/innerHTML · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · SameSite/세임사이트/Strict/Lax/None · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · 화이트리스트/Whitelist/최소 허용/허용 목록 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin · CORS/코어스/Cross-Origin/교차 출처 · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

## [1-QUESTIONS] 7주차 1차시 p.28 · 퀴즈 1
문제: 다음 중 로컬 저장소(LocalStorage)에 민감 정보를 저장했을 때 발생할 수 있는 문제가 아닌 것은 ?
1) XSS 공격이 성공하면 로컬 저장소 내용이 유출될 수 있다.
2) 로컬 저장소는 기본적으로 평문으로 저장된다.
3) 도메인이 다르면 로컬 저장소를 공유할 수 있다.
4) 악성 스크립트가 로컬 저장소 내용을 임의로 변경할 수 있다.
정답: 3) 도메인이 다르면 로컬 저장소를 공유할 수 있다.
해설: Same-Origin Policy로 인해, 도메인이 다르면 로컬 저장소를 공유할 수 없습니다.
출처: [2-SLIDES] 7주차 1차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 7주차 1차시 p.28 · 퀴즈 2
문제: SSR(Server-Side Rendering)과 CSR(Client-Side Rendering)에 대한 설명으로 옳은 것은 ?
1) SSR은 브라우저가 기본 HTML만 받고, 모든 UI를 JavaScript로 구성한다.
2) CSR은 서버에서 데이터를 주입해 완성된 HTML을 전송한다.
3) SSR은 서버에서 HTML을 완성해 응답하고, CSR은 클라이언트가 JS로 화면을 동적으로 구성한다.
4) CSR은 검색 엔진 최적화(SEO)에 매우 유리하며, SSR은 초기 로딩이 느리다.
정답: 3) SSR은 서버에서 HTML을 완성해 응답하고, CSR은 클라이언트가 JS로 화면을 동적으로 구성한다.
해설: SSR은 서버가 완성된 HTML을, CSR은 브라우저가 JS로 동적 화면을 구성하는 방식입니다.
출처: [2-SLIDES] 7주차 1차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 7주차 1차시 p.28 · 퀴즈 3
문제: 프론트엔드에서 외부 스크립트나 스타일의 로딩 출처를 제한해 XSS 같은 공격을 완화하기 위해 사용하는 보안 정책은 ? (영문 3글자) ( )
정답: ( CSP )
출처: [2-SLIDES] 7주차 1차시 p.28 (문제) · p.29 (정답)

## [1-QUESTIONS] 7주차 1차시 p.28 · 비고
정답 보기(`3) 도메인이 다르면…`, `3) SSR은 서버에서…`)와 3번 정답 `CSP`는 슬라이드에서 빨간 글씨로 표시됨.
(※ 검증: 1번 해설의 '도메인'은 정확히는 출처(origin = 스킴+호스트+포트) 단위 — localStorage는 출처별로 분리되므로 같은 도메인이라도 http/https나 포트가 다르면 공유되지 않음. 정답 자체는 맞음)

# [1-QUESTIONS] 7주차 2차시 — 프론트엔드 데이터 처리 / XSS / CSRF
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Reflected XSS/반사형 XSS/리플렉티드 · Stored XSS/저장형 XSS/스토어드 · DOM XSS/DOM 기반 XSS/돔 기반/document.write/innerHTML · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · SameSite/세임사이트/Strict/Lax/None · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링

## [1-QUESTIONS] 7주차 2차시 p.32 · 퀴즈 1
문제: 다음 중 XSS 방어 기법에 해당하지 않는 것은 ?
1) HTML 엔티티 이스케이프로 <script>를 무해한 텍스트로 변환
2) CSP를 적용해 악성 스크립트 로드를 제한
3) 입력값 필터링으로 < > 같은 특수문자 차단
4) CSRF 토큰을 사용해 사용자 요청이 정당한지 검증
정답: 4) CSRF 토큰을 사용해 사용자 요청이 정당한지 검증
해설: CSRF 토큰은 주로 CSRF 공격 방어 기법이며, XSS 방어와는 직접 관련이 없습니다.
출처: [2-SLIDES] 7주차 2차시 p.32 (문제) · p.33 (정답)

## [1-QUESTIONS] 7주차 2차시 p.32 · 퀴즈 2
문제: 다음 중 XSS를 유발할 수 있는 취약한 코드 예시로 옳은 것은 ?
1) `out.println("You searched for: " + request.getParameter("q"));`
2) `response.setHeader("Content-Security-Policy", "default-src 'self'");`
3) `<input type="hidden" name="_csrf" value="...">`
4) `textContent = escapeHtml(userInput);`
정답: 1) out.println("You searched for: " + request.getParameter("q"));
해설: 사용자 입력값을 검증 없이 그대로 출력하면 XSS 공격이 발생할 수 있습니다.
출처: [2-SLIDES] 7주차 2차시 p.32 (문제) · p.33 (정답)

## [1-QUESTIONS] 7주차 2차시 p.32 · 퀴즈 3
문제: XSS의 종류 중 서버를 거치지 않고, 클라이언트 자바스크립트 로직에서 발생하는 공격 방식은? (영어 대문자 3글자) ( )
정답: ( DOM )
출처: [2-SLIDES] 7주차 2차시 p.32 (문제) · p.33 (정답)

## [1-QUESTIONS] 7주차 2차시 p.32 · 비고
(정답 표시: 1번의 "4) CSRF 토큰을 사용해 사용자 요청이 정당한지 검증", 2번의 "1) out.println(...)" 코드, 3번의 "DOM"이 빨간 글씨로 강조됨)

# [1-QUESTIONS] 7주차 3차시 — 프론트엔드 데이터 처리 / XSS / CSRF
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Stored XSS/저장형 XSS/스토어드 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · SameSite/세임사이트/Strict/Lax/None · 화이트리스트/Whitelist/최소 허용/허용 목록 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링

## [1-QUESTIONS] 7주차 3차시 p.26 · 퀴즈 1
문제: 다음 중 CSRF 공격이 성공하기 위해 반드시 필요한 조건은 ?
1) 중요 웹사이트에 로그인되어 쿠키를 보유하고 있어야 한다.
2) 서버가 Referer 검증을 엄격하게 적용해야 한다.
3) CSRF 토큰을 매 요청마다 발급해야 한다.
4) 브라우저가 SameSite=Strict로 쿠키를 설정해 둬야 한다.
정답: 1) 중요 웹사이트에 로그인되어 쿠키를 보유하고 있어야 한다.
해설: 공격이 성립하려면, 사용자가 로그인 중이라 브라우저가 쿠키를 전송해야 합니다.
출처: [2-SLIDES] 7주차 3차시 p.26 (문제) · p.27 (정답)

## [1-QUESTIONS] 7주차 3차시 p.26 · 퀴즈 2
문제: 다음 중 CSRF 방어 기법에 해당하지 않는 것은 ?
1) CSRF 토큰을 사용해 요청 시 고유 값 검증
2) SameSite 쿠키로 외부 도메인에서 쿠키 자동 전송 제한
3) Referer/Origin 검사로 출처가 올바른지 확인
4) 암호화된 비밀번호로 로그인 처리
정답: 4) 암호화된 비밀번호로 로그인 처리
해설: 비밀번호 암호화는 인증 과정 보안이지만, CSRF 방어 기법과는 직접 관련이 없습니다.
출처: [2-SLIDES] 7주차 3차시 p.26 (문제) · p.27 (정답)

## [1-QUESTIONS] 7주차 3차시 p.26 · 퀴즈 3
문제: CSRF 공격을 완화하기 위해 쿠키에 설정하는 속성 중, 외부 도메인에서 요청이 발생했을 때 쿠키가 자동 전송되지 않도록 제한하기 위해 사용하는 속성은 ? ( )
정답: ( SameSite )
출처: [2-SLIDES] 7주차 3차시 p.26 (문제) · p.27 (정답)

## [1-QUESTIONS] 7주차 3차시 p.26 · 비고
(정답 표시: 1번 "1) 중요 웹사이트에 로그인되어 쿠키를 보유하고 있어야 한다.", 2번 "4) 암호화된 비밀번호로 로그인 처리", 3번 괄호 안 "SameSite"가 빨간 글씨로 표시됨. ※ 검증: 26쪽 보기와 대조 — 1번의 2)·3)·4)는 모두 방어 측 조치라 공격 성립 조건이 아니고, 2번의 1)~3)은 18~22쪽에서 다룬 방어 기법(토큰·SameSite·Origin/Referer)이므로 정답 1 / 4 / SameSite — 일치)
