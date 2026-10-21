# WEEK06 — 6주차 ORM·MyBatis / SQL 인젝션 / Command 인젝션 (시큐어코딩 중간고사 주차 묶음)

> 이 파일 하나에 6주차의 교안 퀴즈(1-QUESTIONS, 신뢰도 A) · 정리(4-NOTES, C~D) · 교안 원문(2-SLIDES, A) · 강의 발화(3-TRANSCRIPT, B)가 모두 있다.
> 위치 표기 규칙은 전체 파일과 같다: `[2-SLIDES] N주차 M차시 p.X` = 교안, `[N주차 M차시 mm:ss]` = 발화, `[1-QUESTIONS] N주차 M차시 퀴즈 K` = 퀴즈.
> 맨 앞의 찾아보기(0-INDEX)는 1~7주차 전체 지도다. 다른 주차 개념이면 그 주차 파일(weekNN.md)을 봐야 한다.

---

# 0-INDEX — 찾아보기 (먼저 여기를 본다)

> 개념 → 어느 파일/주차에 있는지. 표에서 위치를 확인한 뒤 해당 파일을 검색하면 빠름.
> 파일 신뢰도: 1-QUESTIONS(A·퀴즈) · 2-SLIDES(A·교안) · 3-TRANSCRIPT(B·발화) · 4-NOTES(C~D·AI정리)

주차 요약: 1주차 보안약점과 시큐어코딩 개요 / 2주차 SW개발보안 방법론·위협 모델링 / 3주차 Spring Boot 개발 환경·실습 / 4주차 정규식과 입력값 검증·XSS 필터 / 5주차 인증과 인가 · OAuth2 · JWT / 6주차 ORM·MyBatis / SQL 인젝션 / Command 인젝션 / 7주차 프론트엔드 데이터 처리 / XSS / CSRF

| 개념 | 검색 표기 | 교안(2-SLIDES) 주차-차시 | 발화(3-TRANSCRIPT) 주차 |
|---|---|---|---|
| 보안약점 | 보안약점, Weakness, CWE, 취약점 | 1-1, 1-2, 1-3, 2-1, 2-2, 2-3, 3-1, 3-2, 3-3, 4-1, 4-2, 4-3, 5-1, 5-2, 5-3, 6-1, 6-2, 6-3, 7-1, 7-2, 7-3 | 1, 2, 3, 4, 5, 6, 7 |
| SQL 인젝션 | SQL Injection, SQL 인젝션, SQL 삽입, 에스큐엘 인젝션 | 1-1, 1-2, 1-3, 2-1, 4-1, 4-3, 6-1, 6-2, 6-3, 7-2 | 1, 2, 4, 6, 7 |
| PreparedStatement | PreparedStatement, 프리페어드 스테이트먼트, 파라미터 바인딩, 바인딩 | 6-1, 6-2, 7-1, 7-2 | 3, 5, 6, 7 |
| XSS | XSS, Cross-Site Scripting, 크로스사이트 스크립팅, 크로스 사이트 스크립팅 | 1-1, 1-3, 2-1, 2-3, 3-1, 4-1, 4-3, 5-1, 5-2, 5-3, 7-1, 7-2, 7-3 | 1, 2, 3, 4, 5, 6, 7 |
| Reflected XSS | Reflected XSS, 반사형 XSS, 리플렉티드 | 7-2 | 7 |
| Stored XSS | Stored XSS, 저장형 XSS, 스토어드 | 7-2, 7-3 | 7 |
| DOM XSS | DOM XSS, DOM 기반 XSS, 돔 기반, document.write | 7-1, 7-2 | 7 |
| CSRF | CSRF, Cross-Site Request Forgery, 크로스사이트 요청 위조, 크로스 사이트 요청 위조 | 1-2, 1-3, 5-1, 7-2, 7-3 | 1, 5, 7 |
| Command 인젝션 | Command Injection, 커맨드 인젝션, 명령어 삽입, 명령 삽입 | 1-2, 1-3, 4-1, 6-3, 7-1 | 1, 4, 6 |
| CSP | CSP, Content Security Policy, 콘텐츠 보안 정책, 컨텐츠 시큐리티 폴리시 | 1-2, 1-3, 5-2, 7-1, 7-2 | 1, 5, 7 |
| SameSite | SameSite, 세임사이트, Strict, Lax | 1-3, 5-1, 5-3, 7-1, 7-2, 7-3 | 1, 3, 5, 7 |
| HTML 인코딩 | HTML Encoding, HTML 인코딩, 이스케이프, Escape | 1-1, 2-3, 3-3, 5-1, 5-2, 5-3, 6-1, 6-2, 6-3, 7-1, 7-2 | 1, 2, 3, 4, 5, 6, 7 |
| 화이트리스트 | 화이트리스트, Whitelist, 최소 허용, 허용 목록 | 1-3, 6-2, 6-3, 7-1, 7-3 | 1, 6, 7 |
| ORM | ORM, Object-Relational Mapping, 객체 관계 매핑, JPA | 1-1, 1-3, 2-2, 2-3, 3-1, 3-2, 3-3, 4-3, 5-2, 6-1, 6-2, 6-3, 7-2, 7-3 | 1, 2, 3, 4, 5, 6 |
| MyBatis | MyBatis, 마이바티스, Mapper, 매퍼 | 5-2, 6-1, 6-2 | 4, 5, 6 |
| Dirty Checking | Dirty Checking, 더티 체킹, 변경 감지 | 6-1 | 6 |
| Mass Assignment | Mass Assignment, 대량 할당, DTO, isAdmin | 1-3, 3-3, 6-1 | 1, 3, 6 |
| 인증 | Authentication, 인증, 로그인 | 1-1, 1-2, 1-3, 2-1, 2-2, 2-3, 3-1, 3-2, 4-3, 5-1, 5-2, 5-3, 6-2, 7-1, 7-2, 7-3 | 1, 2, 3, 4, 5, 6, 7 |
| 인가 | Authorization, 인가, 권한, RBAC | 1-1, 1-2, 1-3, 2-2, 2-3, 3-1, 4-3, 5-1, 5-2, 5-3, 6-1, 6-2, 6-3, 7-1, 7-2, 7-3 | 1, 2, 3, 4, 5, 6, 7 |
| 세션 | Session, 세션, JSESSIONID, 세션 쿠키 | 1-1, 1-2, 1-3, 2-1, 2-2, 2-3, 3-1, 4-1, 4-2, 4-3, 5-1, 5-2, 5-3, 6-1, 6-2, 6-3, 7-1, 7-2, 7-3 | 1, 2, 3, 4, 5, 6, 7 |
| 토큰 | Token, 토큰, Bearer, 베어러 | 1-1, 1-3, 2-3, 5-1, 5-2, 5-3, 7-1, 7-2, 7-3 | 1, 2, 3, 5, 7 |
| OAuth2 | OAuth2, OAuth 2.0, 오아스, 권한 위임 | 1-3, 2-3, 3-1, 5-2, 5-3, 6-1, 6-2, 7-2, 7-3 | 1, 2, 3, 5, 6, 7 |
| JWT | JWT, JSON Web Token, 제이더블유티, Claims | 1-3, 5-1, 5-2, 5-3 | 1, 5 |
| Refresh Token | Refresh Token, 리프레시 토큰, 토큰 회전, Rotation | 5-2, 5-3 | 5 |
| MFA | MFA, Multi-Factor, 다중 인증, 다중 매체 인증 | 1-1, 1-3, 2-2, 5-1 | 1, 2, 5 |
| HSTS | HSTS, HTTP Strict-Transport-Security, 스트릭트 트랜스포트 | 5-1 | 5 |
| IDOR | IDOR, Insecure Direct Object References, 직접 객체 참조, 수평 권한 | 1-1, 1-3, 2-2, 2-3, 5-1, 6-2, 7-1 | 1, 2, 5 |
| 정규식 | Regex, 정규식, Regular Expression, Pattern | 4-1, 4-2, 4-3, 5-2, 6-3, 7-1, 7-2, 7-3 | 4, 6, 7 |
| ReDoS | ReDoS, 레도스, 백트래킹, Backtracking | 4-2 | 4 |
| Filter | Filter, 필터, Interceptor, 인터셉터 | 1-3, 2-2, 2-3, 3-2, 4-1, 4-2, 4-3, 5-1, 5-2, 6-1, 6-2, 6-3, 7-1, 7-2, 7-3 | 1, 2, 3, 4, 5, 6, 7 |
| 위협 모델링 | Threat Modeling, 위협 모델링, STRIDE, 스트라이드 | 1-1, 1-2, 1-3, 2-1, 2-2, 2-3, 3-1, 3-2, 4-2, 4-3, 5-1, 5-2, 5-3, 6-1, 6-2, 6-3, 7-1, 7-2, 7-3 | 1, 2, 3, 4, 5 |
| SSR/CSR | SSR, CSR, Server-Side Rendering, Client-Side Rendering | 1-1, 1-3, 4-3, 5-1, 7-1, 7-2, 7-3 | 1, 4, 5, 7 |
| 로컬 저장소 | localStorage, sessionStorage, 로컬 저장소, 로컬 스토리지 | 5-1, 5-2, 5-3, 7-1 | 5, 7 |
| CORS | CORS, 코어스, Cross-Origin, 교차 출처 | 4-3, 7-1 | 4, 7 |
| SQLMap | SQLMap, 에스큐엘맵 | 6-2 | - |
| ZAP | ZAP, OWASP ZAP, Active Scan, Burp | 1-1, 3-1, 5-1, 6-2, 6-3, 7-1 | 1, 3, 4, 5, 6 |
| 코드 리뷰 | 코드 리뷰, Code Review, SAST, DAST | 1-1, 1-3, 2-1, 2-2, 6-2, 6-3, 7-1 | 1, 2, 6, 7 |

## [0-INDEX] 교안 쪽 제목 목록 (626쪽 전체) — 문제의 핵심어를 여기서 먼저 찾는다
> 같은 제목이 이어지면 쪽 범위로 묶음. 제목에 없어도 본문에 있을 수 있으니, 여기 없으면 2-SLIDES 본문을 핵심어로 다시 검색한다.

### [0-INDEX] 1주차 1차시 교안 제목 — 보안약점과 시큐어코딩 개요
p.1 시큐어코딩
p.2 SW개발보안 이해
p.3 학습 목표
p.4 학습 내용
p.5 SW개발보안 이해
p.6~7 데이터 유출현황 및 침해발생 원인
p.8 현대 애플리케이션의 보안 과제 (출처: 라드웨어 애플리케이션 보호 위한
p.9 애플리케이션 보안 과제는 어떻게 해결해야 할까?
p.10 애플리케이션 보안(1)
p.11 SW개발보안 프로세스
p.12 DevOps환경에서의 DevSecOps (그림출처: 가트너)
p.13~16 DevSecOps AWS 아키텍쳐
p.17 애플리케이션 보안(2)
p.18~19 Security By Design – Threat Modeling
p.20 애플리케이션 보안(3)
p.21 제로 트러스트 보안 모델
p.22 SW개발보안 이해
p.23 시큐어한 소프트웨어란?
p.24~27 개발자의 사소한 실수 -
p.28~29 소프트웨어 보안취약점 사례 – OSS( ) 취약점 공격
p.30 소프트웨어 보안취약점 사례 – 공급망 해킹
p.31 소프트웨어 보안 취약점 사례 – 공급망 보안
p.32 요약 정리
p.33 참고 문헌
p.34 감사합니다.
p.35 퀴즈
p.36 퀴즈 정답

### [0-INDEX] 1주차 2차시 교안 제목 — 보안약점과 시큐어코딩 개요
p.1 시큐어코딩
p.2 SW개발보안 국내기준
p.3 학습 목표
p.4 학습 내용
p.5 SW개발보안 국내기준
p.6~9 행정안전부 SW개발보안 가이드
p.10 행정안전부 개발보안 가이드
p.11 국내 SW개발보안 제도(과학기술정보통신부)
p.12 SW개발보안 국내기준
p.13 클라우드서비스(SaaS) 보안 인증
p.14 클라우드 보안인증 통제항목 [SaaS 표준등급]
p.15 SaaS CSAP 기술적 보호조치 (★ ISMS 인증시 점검대체 가능 항
p.16 SaaS CSAP 기술적 보호조치
p.17 요약 정리
p.18 참고 문헌
p.19 감사합니다.
p.20 퀴즈
p.21 퀴즈 정답

### [0-INDEX] 1주차 3차시 교안 제목 — 보안약점과 시큐어코딩 개요
p.1 시큐어코딩
p.2 SW개발보안 국외기준
p.3 학습 목표
p.4 학습 내용
p.5 SW개발보안 국외기준
p.6~8 국외 개발보안 현황
p.9 SW개발보안 국외기준
p.10~11 OWASP TOP 10
p.12~21 OWASP TOP 10 2021
p.22 OWASP API Security Risk TOP 10
p.23~28 OWASP API Security Risk TOP 10 2023
p.29 OWASP API Security Risk TOP 10
p.30~32 OWASP API Security Risk TOP 10 2023
p.33 OWASP Mobile Risk TOP 10
p.34 SW개발보안 국외기준
p.35 CVE 취약점 DB활용(http://cve.mitre.org)
p.36 CVE 작동 방식
p.37 CVE 예제
p.38 CVE 와 소프트웨어 개발보안
p.39 SW개발보안 국외기준
p.40 CWE 취약점 DB활용(http://cwe.mitre.org)
p.41 CWE와 CVE의 차이점
p.42 CWE TOP 25
p.43 CWE TOP 25 선정 목적 및 활용 방안
p.44~45 2023 CWE TOP 25 (https://cwe.mitre.org/t
p.46 요약 정리
p.47 참고 문헌
p.48 감사합니다.
p.49 퀴즈
p.50 퀴즈 정답

### [0-INDEX] 2주차 1차시 교안 제목 — SW개발보안 방법론·위협 모델링
p.1 시큐어코딩
p.2 SW개발보안 방법론
p.3 학습 목표
p.4 학습 내용
p.5~7 SW개발보안 방법론
p.8 SW개발보안 적용 시 비용 효과
p.9 SW개발보안 방법론 적용의 중요성
p.10 SW개발보안 방법론
p.11~18 소프트웨어 개발보안 적용 우수사례 MS-SDL
p.19 요약 정리
p.20 참고 문헌
p.21 감사합니다.
p.22 퀴즈
p.23 퀴즈 정답

### [0-INDEX] 2주차 2차시 교안 제목 — SW개발보안 방법론·위협 모델링
p.1 시큐어코딩
p.2 위협모델링 개요
p.3 학습 목표
p.4 학습 내용
p.5 위협모델링 개요
p.6 위협모델링(Threat Modeling) 이란?
p.7 위협모델링(Threat Modeling)의 핵심 목표
p.8 위협모델링(Threat Modeling)이 중요한 이유
p.9 위협모델링(Threat Modeling) 참가자 및 역할 (1)
p.10 위협모델링(Threat Modeling) 참가자 및 역할 (2)
p.11 위협모델링(Threat Modeling) 흐름
p.12 위협모델링(Threat Modeling) 프레임워크
p.13 위협모델링 프레임워크 - STRIDE
p.14 위협모델링 프레임워크 – DREAD
p.15 위협모델링 프레임워크 – DREAD 세부 점수 기준 예시
p.16 위협모델링 프레임워크 – DREAD 총점 기준에 따른 위협 수준
p.17 위협모델링 프레임워크 – DREAD 평가 예시
p.18 위협모델링 개요
p.19 위협모델링 프레임워크 프로세스
p.20 위협모델링 프로세스 – 시스템 정의(Define the System)
p.21 위협모델링 프로세스 – 위협 식별(Identify Threats) [Id
p.22 위협모델링 프로세스 – 완화 계획 수립(Mitigate Threats)
p.23 위협모델링 프로세스 – 검토 및 개선(Validate & Review)
p.24 MS-SDL 위협모델링 프로세스 요약
p.25 요약 정리
p.26 참고 문헌
p.27 감사합니다.
p.28 퀴즈
p.29 퀴즈 정답

### [0-INDEX] 2주차 3차시 교안 제목 — SW개발보안 방법론·위협 모델링
p.1 위협모델링 실무 적용
p.2 학습 목표
p.3 학습 내용
p.4 위협모델링 실무 적용
p.5 위협모델링 도구 선정 기준
p.6 위협모델링 도구들
p.7 위협모델링 도구들 – 도구 선정 가이드
p.8 MTMT(Microsoft Threats Modeling Tool)
p.9 위협모델링 실무 적용
p.10 위협모델링 실무 적용 실습
p.11 1단계: 시스템 이해 및 범위 정의
p.12 1단계: 시스템 이해 및 범위 정의 - DFD 그리기
p.13 2단계: STRIDE 위협 도출 — 게시글 작성 기능에 대한 STRIDE
p.14 3단계: DREAD 위험도 평가 — 게시글 작성 기능에서 도출된 위협들에
p.15 4단계: 위협 완화 및 대응 전략 수립 — 도출된 위협 내용들을 완화할
p.16 5단계: 보안 검증 및 지속적인 개선
p.17 [개별 실습] 댓글 작성 기능 위협모델링 분석 준비
p.18 요약 정리
p.19 참고 문헌
p.20 감사합니다.
p.21 퀴즈
p.22 퀴즈 정답

### [0-INDEX] 3주차 1차시 교안 제목 — Spring Boot 개발 환경·실습
p.1 실습환경 구축-1
p.2 학습 목표
p.3 학습 내용
p.4 실습환경 구축-1
p.5 실습환경 아키텍처 이해
p.6 실습환경 구축 – 웹 서비스 서버 설정 (1/8)
p.7 실습환경 구축 – 웹 서비스 서버 설정 (2/8)
p.8 실습환경 구축 – 웹 서비스 서버 설정 (3/8)
p.9 실습환경 구축 – 웹 서비스 서버 설정 (4/8)
p.10 실습환경 구축 – 웹 서비스 서버 설정 (5/8)
p.11 실습환경 구축 – 웹 서비스 서버 설정 (6/8)
p.12 실습환경 구축 – 웹 서비스 서버 설정 (7/8)
p.13 실습환경 구축 – 웹 서비스 서버 설정 (8/8)
p.14 실습환경 구축 – 프록시 설정(1/4)
p.15 실습환경 구축 – 프록시 설정(2/4)
p.16 실습환경 구축 – 프록시 설정(3/4)
p.17 실습환경 구축 – 프록시 설정(4/4)
p.18 실습환경 구축 – 파이어폭스 브라우저 설정(1/3)
p.19 실습환경 구축 – 파이어폭스 브라우저 설정(2/3)
p.20 실습환경 구축 – 파이어폭스 브라우저 설정(3/3)
p.21 실습환경 구축 – BurpSuite 프록시 서버 동작
p.22 실습환경 구축-1
p.23 웹 구조
p.24 웹 서비스 흐름
p.25 HTTP 구조
p.26 HTTP 구조 — HTTP 흐름 이해
p.27 BurpSuite을 활용한 HTTP 구조 보기
p.28 HTTP Request 메시지 구조
p.29 HTTP Request Method
p.30 HTTP Response 메시지 구조
p.31~33 HTTP Response Status Code
p.34 실습환경 구축-1
p.35 데이터 인코딩 개요
p.36 03 데이터 인코딩
p.37 URL 인코딩
p.38 URL 인코딩이 필요한 문자 목록
p.39~42 BurpSuite를 통해 BASE64 디코딩
p.43~44 BurpSuite를 통해 URL인코딩/디코딩
p.45 요약 정리
p.46 참고 문헌
p.47 감사합니다.
p.48 퀴즈
p.49 퀴즈 정답

### [0-INDEX] 3주차 2차시 교안 제목 — Spring Boot 개발 환경·실습
p.1 실습환경 구축-2
p.2 학습 목표
p.3 학습 내용
p.4 실습환경 구축-2
p.5~7 프레임워크(Framework)와 플랫폼(Platform) 개념 및 차이
p.8 Spring Boot 프레임워크란?
p.9 Spring Boot vs. Spring Framework
p.10~17 Spring Boot 기본 사용법
p.18 시연 영상
p.19 요약 정리
p.20 참고 문헌
p.21 감사합니다.
p.22 퀴즈
p.23 퀴즈 정답

### [0-INDEX] 3주차 3차시 교안 제목 — Spring Boot 개발 환경·실습
p.1 실습환경 구축-3
p.2 학습 목표
p.3 학습 내용
p.4 실습환경 구축-3
p.5~6 Spring Boot을 이용한 간단한 게시판 만들기 — Step 1. 설
p.7~15 Spring Boot을 이용한 간단한 게시판 만들기
p.16 시연 영상
p.17 요약 정리
p.18 참고 문헌
p.19 감사합니다.
p.20 퀴즈
p.21 퀴즈 정답

### [0-INDEX] 4주차 1차시 교안 제목 — 정규식과 입력값 검증·XSS 필터
p.1 정규식 기본문법
p.2 학습 목표
p.3 학습 내용
p.4 정규식 기본 문법
p.5~6 정규식이란?
p.7 정규식 활용 사례
p.8 정규식 문자 다루기 — 문자 다루기
p.9 정규식 문자 다루기 — 기본 문자 클래스 (Character Class)
p.10 정규식 기본 문법
p.11 반복 다루기 — 반복 메타문자
p.12 반복 다루기 — 실무 활용 예시
p.13 정규식 기본 문법
p.14 문자열 다루기
p.15 문자열 다루기 — 자주 사용되는 정규식
p.16 정규식 시각적 이해
p.17 요약 정리
p.18 참고 문헌
p.19 감사합니다.
p.20 퀴즈
p.21 퀴즈 정답

### [0-INDEX] 4주차 2차시 교안 제목 — 정규식과 입력값 검증·XSS 필터
p.1 정규식 활용한 데이터 검증
p.2 학습 목표
p.3 학습 내용
p.4 정규식 활용한 데이터 검증
p.5 grep 명령어에서 정규식 사용
p.6 grep 명령어에서 정규식 사용 — grep 명령어에서 자주 사용하는 옵
p.7 grep 명령어에서 정규식 사용
p.8 sed 명령어에서 정규식 사용
p.9 sed 명령어에서 정규식 사용 — sed 명령어에서 자주 사용하는 명령어
p.10 sed 명령어에서 정규식 사용
p.11 awk 명령어에서 정규식 사용
p.12 awk 명령어에서 정규식 사용 — awk의 주요 변수
p.13 awk 명령어에서 정규식 사용
p.14 정규식 활용한 데이터 검증
p.15~19 자바 프로그램에서 정규식 사용
p.20~24 정규식 사용 시 문제점
p.25 요약 정리
p.26 참고 문헌
p.27 감사합니다.
p.28 퀴즈
p.29 퀴즈 정답

### [0-INDEX] 4주차 3차시 교안 제목 — 정규식과 입력값 검증·XSS 필터
p.1 정규식을 활용한 입력값 필터링
p.2 학습 목표
p.3 학습 내용
p.4 정규식을 활용한 입력값 필터링
p.5 필터(Filter)란?
p.6 Spring Boot Filter 구조
p.7~9 Spring Boot 에서 필터 구현 방법
p.10 Spring Security 와 기본 필터
p.11~13 입력값 필터 만들기
p.14 입력값 필터 만들기 — 정규식을 이용한 입력값 필터링 정책
p.15~16 LAB1 - 소스코드의 XSS 취약점 확인
p.17~20 LAB2 - 소스코드에 XSS 필터 반영
p.21 LAB3 - 소스코드에서 XSS 필터 동작 확인
p.22 시연 영상
p.23 요약 정리
p.24 참고 문헌
p.25 감사합니다.
p.26 퀴즈
p.27 퀴즈 정답

### [0-INDEX] 5주차 1차시 교안 제목 — 인증과 인가 · OAuth2 · JWT
p.1 인증과 인가 기초
p.2 학습 목표
p.3 학습 내용
p.4 인증과 인가 기초
p.5 인증과 인가의 차이
p.6 인증 방식 이해
p.7 인증 방식 이해 – 지식기반 인증
p.8 인증 방식 이해 – 소유기반 인증
p.9 인증 방식 이해 – 생체기반 인증
p.10 보안강화를 위한 최신 인증 기술
p.11 인증과 인가 기초
p.12 일반적인 웹 애플리케이션의 인증/인가 프로세스
p.13 세션 기반 인증
p.14~15 LAB 세션 처리 확인
p.16 토큰 기반 인증
p.17~18 JWT 로그인 세션 처리 확인
p.19 인증과 인가 기초
p.20 주요 인증 보안 위협
p.21 주요 인증 보안 위협 대응 방안
p.22 주요 인가 보안 위협
p.23 주요 인가 보안 위협 대응 방안
p.24 요약 정리
p.25 참고 문헌
p.26 감사합니다.
p.27 퀴즈
p.28 퀴즈 정답

### [0-INDEX] 5주차 2차시 교안 제목 — 인증과 인가 · OAuth2 · JWT
p.1 OAuth2 인증 및 인가
p.2 학습 목표
p.3 학습 내용
p.4 OAuth2 인증 및 인가
p.5 OAuth2 란?
p.6 OAuth2 주요 구성요소
p.7 OAuth2 구성 요소
p.8~9 OAuth2 인증 흐름 : Authorization Code Grant
p.10~11 OAuth2 의 장단점
p.12 OAuth 와 OAuth2 비교
p.13 OAuth2 인증 및 인가
p.14~23 Google OAuth 클라이언트 생성
p.24~29 Authorization Code 발급
p.30 Access Token 발급
p.31 Resource Server에서 유저정보 받기
p.32 유저 정보를 토대로 계정 연동
p.33 OAuth2를 통한 로그인 성공 화면
p.34 OAuth2 인증 및 인가
p.35 OAuth2 구현시 발생할 수 있는 취약점
p.36 Access Token 유출 방지 전략
p.37 요약 정리
p.38 참고 문헌
p.39 감사합니다.
p.40 퀴즈
p.41 퀴즈 정답

### [0-INDEX] 5주차 3차시 교안 제목 — 인증과 인가 · OAuth2 · JWT
p.1 JWT 인증 및 인가
p.2 학습 목표
p.3 학습 내용
p.4 JWT 인증 및 인가
p.5 JWT(JSON Web Token) 이란?
p.6 JWT의 구성 및 동작 방식
p.7 JWT의 장점
p.8 JWT의 단점
p.9~11 JWT 기반 인증 흐름
p.12 JWT 인증 및 인가
p.13 JWT 구현 실습
p.14 프로젝트 환경 설정
p.15 JWT 컨트롤러 소스코드 (1/4)
p.16 JWT 컨트롤러 소스코드 (2/4)
p.17 JWT 컨트롤러 소스코드 (3/4)
p.18 JWT 컨트롤러 소스코드 (4/4)
p.19 구현된 JWT 기능 테스트 (1/3)
p.20 구현된 JWT 기능 테스트 (2/3)
p.21 구현된 JWT 기능 테스트 (3/3)
p.22 JWT 인증 및 인가
p.23~24 JWT 보안 및 취약점 대응 – 서명과 키 관리
p.25 JWT 보안 및 취약점 대응 – 유효기간 관리
p.26 JWT 보안 및 취약점 대응 – JWT 탈취
p.27 요약 정리
p.28 참고 문헌
p.29 감사합니다.
p.30 퀴즈
p.31 퀴즈 정답

### [0-INDEX] 6주차 1차시 교안 제목 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
p.1 ORM 프레임워크 이해와 활용
p.2 학습 목표
p.3 학습 내용
p.4 ORM 프레임워크 이해와 활용
p.5 ORM(Object-Relational Mapping) 의 정의와 필요성
p.6 전통적인 SQL 쿼리 vs ORM 방식 비교 – 정의와 특징
p.7 전통적인 SQL 쿼리 vs ORM 방식 비교 – 장점과 단점
p.8 전통적인 SQL 쿼리 vs ORM 방식 비교
p.9~11 ORM이 제공하는 주요 기능
p.12 ORM 프레임워크 이해와 활용
p.13 MyBatis 프레임워크 - 개요
p.14 MyBatis 프레임워크 – 주요 기능
p.15 MyBatis 프레임워크 – 설정 및 구성
p.16 MyBatis 프레임워크 사용 예시 (1/3)
p.17 MyBatis 프레임워크 사용 예시 (2/3)
p.18 MyBatis 프레임워크 사용 예시 (3/3)
p.19 MyBatis 프레임워크 – 장단점 및 사례
p.20 ORM 프레임워크 이해와 활용
p.21 ORM 프레임워크와 보안 개요
p.22 SQL 인젝션 및 동적 쿼리 취약점
p.23 캐싱 및 지연 로딩 관련 보안 이슈
p.24 매핑, 설정 및 권한 관리 취약점
p.25 요약 정리
p.26 참고 문헌
p.27 감사합니다.
p.28 퀴즈
p.29 퀴즈 정답

### [0-INDEX] 6주차 2차시 교안 제목 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
p.1 SQL 인젝션 진단 및 대응
p.2 학습 목표
p.3 학습 내용
p.4 SQL 인젝션 취약점 진단 및 대응
p.5~6 SQL 인젝션 개요
p.7~9 SQL 인젝션 취약점 발생 원인
p.10 SQL 인젝션 취약점 공격 방식
p.11 Error-based SQL 인젝션 (오류 기반 SQL 인젝션)
p.12~13 Union-based SQL 인젝션 (유니온 기반 SQL 인젝션)
p.14 Blind SQL 인젝션 (블라인드 SQL 인젝션)
p.15 SQL 인젝션 공격 보안 사고 사례
p.16 SQL 인젝션 취약점 진단 및 대응
p.17~18 SQL인젝션 취약점 진단 방법 – 코드리뷰
p.19 SQL인젝션 취약점 진단 방법 – 자동화된 진단 도구 활용
p.20~26 SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
p.27 SQL인젝션 취약점 대응 방법 – 입력 값 검증
p.28~29 SQL인젝션 취약점 대응 방법 – 보안 로그 기록 및 모니터링
p.30 요약 정리
p.31 참고 문헌
p.32 감사합니다.
p.33 퀴즈
p.34 퀴즈 정답

### [0-INDEX] 6주차 3차시 교안 제목 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
p.1 Command 인젝션 취약점 진단 및 대응
p.2 학습 목표
p.3 학습 내용
p.4 Command 인젝션 취약점 진단 및 대응
p.5~6 Command 인젝션이란?
p.7 운영체제별 명령어 실행 방식 이해 - Windows
p.8 운영체제별 명령어 실행 방식 이해 - Linux
p.9 Command 인젝션 취약점 진단 및 대응
p.10~12 Command 인젝션 취약점 진단 - 수동진단
p.13~14 Command 인젝션 취약점 진단 – 자동화도구 활용
p.15~17 Command 인젝션 대응 – 시큐어코딩 적용
p.18 Command 인젝션 대응 – 시스템 보호 전략
p.19 요약 정리
p.20 참고 문헌
p.21 감사합니다.
p.22 퀴즈
p.23 퀴즈 정답

### [0-INDEX] 7주차 1차시 교안 제목 — 프론트엔드 데이터 처리 / XSS / CSRF
p.1 프론트엔드 데이터 처리
p.2 학습 목표
p.3 학습 내용
p.4 프론트엔드 데이터 처리
p.5 클라이언트/서버 구조
p.6 프론트엔드의 역할
p.7~10 프론트엔드에서 입력 데이터 처리 방식
p.11 프론트엔드 데이터 처리
p.12~13 DOM 기반 보안 문제
p.14 JavaScript 실행 환경에서의 보안 문제
p.15~16 로컬 저장소의 보안 문제
p.17~18 보안에 취약한 API 호출 방식
p.19 프론트엔드 데이터 처리
p.20~22 사용자 입력 값 검증 및 필터링
p.23~24 CSP(Content Security Policy) 적용
p.25 요약 정리
p.26 참고 문헌
p.27 감사합니다.
p.28 퀴즈
p.29 퀴즈 정답

### [0-INDEX] 7주차 2차시 교안 제목 — 프론트엔드 데이터 처리 / XSS / CSRF
p.1 XSS 취약점 진단 및 대응
p.2 📌
p.3 📍
p.4 XSS 취약점 진단 및 대응
p.5 XSS(크로스 사이트 스크립팅) 이란?
p.6 XSS 취약점 공격 흐름
p.7 XSS 취약점 유형
p.8 XSS 취약점 공격 피해
p.9 XSS 취약점 진단 및 대응
p.10~12 XSS 공격 유형 및 기법 – Reflected XSS
p.13~15 XSS 공격 유형 및 기법 – Stored XSS
p.16~18 XSS 공격 유형 및 기법 – DOM 기반 XSS
p.19 사고 사례
p.20 XSS 취약점 진단 및 대응
p.21~22 입출력 값 검증 및 필터링
p.23~25 HTML 엔티티 이스케이프 처리
p.26 Spring Web MVC에서 입출력 필터링
p.27~28 CSP(Content-Security-Policy) 적용
p.29 요약 정리
p.30 참고 문헌
p.31 감사합니다.
p.32 퀴즈
p.33 퀴즈 정답

### [0-INDEX] 7주차 3차시 교안 제목 — 프론트엔드 데이터 처리 / XSS / CSRF
p.1 CSRF 취약점 진단 및 대응
p.2 학습 목표
p.3 학습 내용
p.4 CSRF 취약점 진단 및 대응
p.5 CSRF(크로스 사이트 요청 위조)란?
p.6 CSRF 취약점 발생 원인
p.7~8 CSRF 취약점 공격 흐름
p.9 CSRF와 XSS의 차이점
p.10 CSRF 공격 사고 사례
p.11 CSRF 취약점 진단 및 대응
p.12~14 CSRF 공격 기법
p.15~16 CSRF 공격이 가능한 취약한 웹 사이트
p.17 CSRF 취약점 진단 및 대응
p.18~19 CSRF 토큰 적용 및 활용
p.20~21 SameSite Cookie 정책 설정
p.22 Origin/Referer 검증 및 세션 관리 보안 강화
p.23 요약 정리
p.24 참고 문헌
p.25 감사합니다.
p.26 퀴즈
p.27 퀴즈 정답

## [0-INDEX] 교안 퀴즈 문항 목록 (63문제) — 시험 문제와 겹치는지 먼저 본다
- [1-QUESTIONS] 1주차 1차시 퀴즈 1 — 다음 중 SW개발보안 프로세스에 해당하지 않는 것은? → 정답 4) 배포
- [1-QUESTIONS] 1주차 1차시 퀴즈 2 — 제품의 설계단계에서부터 보안을 고려하여 알려진 취약점을 조기에 효과적으로 제거하는 것을 의미하는 것은? → 정답 2) 보안내재화
- [1-QUESTIONS] 1주차 1차시 퀴즈 3 — 다음 중 '오버플로우'에 대한 설명이 맞는 것은? → 정답 2) 연산 결과가 허용할 수 있는 범위를 벗어남
- [1-QUESTIONS] 1주차 2차시 퀴즈 1 — 다음 중 행정안전부 SW개발보안 가이드와 관련 없는 내용은? → 정답 3) 테스트 단계부터 SW개발 보안을 적용하기 위한 기준
- [1-QUESTIONS] 1주차 2차시 퀴즈 2 — 다음 중 클라우드 서비스 보안 인증과 관련하여, 소프트웨어 보안과 관련된 통제 항목이 아닌 것은? → 정답 4) 개발 조직의 신원 관리 및 통제
- [1-QUESTIONS] 1주차 2차시 퀴즈 3 — 다음 중 클라우드 서비스 보안 인증을 나타내는 용어는? → 정답 1) CSAP
- [1-QUESTIONS] 1주차 3차시 퀴즈 1 — 다음 중 '취약한 접근 통제' 취약점에 대한 설명이 맞는 것은? → 정답 1) 인증된 사용자가 접근이 제한된 데이터나 기능에 접근 가능
- [1-QUESTIONS] 1주차 3차시 퀴즈 2 — 다음 중 '인젝션 공격'에 대한 설명으로 틀린 것은? → 정답 3) 커맨드 인젝션 방어를 위해 Prepared Statement를 사용
- [1-QUESTIONS] 1주차 3차시 퀴즈 3 — 다음 중 CVE와 CWE에 대해서 잘못 이야기한 것은? → 정답 3) CWE Top 25는 보안 취약점 중 가장 위험한 25가지를 선정한
- [1-QUESTIONS] 2주차 1차시 퀴즈 1 — 다음 중 SW개발보안 방법론의 주요 개념이 아닌 것은? → 정답 3) SBOM 다중화
- [1-QUESTIONS] 2주차 1차시 퀴즈 2 — 다음 중 SW 결함 수정비용이 가장 많이 필요한 경우는? → 정답 2) 설계과정 발생한 결함이 제품 출시 단계에서 발견된 경우
- [1-QUESTIONS] 2주차 1차시 퀴즈 3 — 다음 중 MS-SDL 보안개발 방법론에 대한 설명 중 틀린 것은? → 정답 2) 요구사항 정의 단계에 위협 모델링을 수행한다.
- [1-QUESTIONS] 2주차 2차시 퀴즈 1 — 다음 중 위협모델링의 핵심 목표가 아닌 것은? → 정답 4) SW 구조 이해
- [1-QUESTIONS] 2주차 2차시 퀴즈 2 — 다음 중 위협모델링 프로세스 단계에 대한 내용이 틀린 것은? → 정답 1) 시스템 정의
- [1-QUESTIONS] 2주차 2차시 퀴즈 3 — 다음 중 STRIDE 프레임워크에서 정의한 주요 위협요소에 대한 설명으로 올바른 것은? → 정답 3) 서비스 거부
- [1-QUESTIONS] 2주차 3차시 퀴즈 1 — 다음 중 위협모델링 도구 선정 기준으로 가장 적합하지 않은 것은? → 정답 4) CWE/CVE 연계 분석 여부
- [1-QUESTIONS] 2주차 3차시 퀴즈 2 — 다음 중 데이터 흐름 다이어그램(DFD)의 주요 구성요소가 아닌 것은? → 정답 4) Module
- [1-QUESTIONS] 2주차 3차시 퀴즈 3 — 다음 중 데이터 흐름 다이어그램(DFD)를 작성하는 단계는? → 정답 1) 시스템 이해 및 범위 정의
- [1-QUESTIONS] 3주차 1차시 퀴즈 1 — 다음 중 웹 애플리케이션 서버 로직의 3대 계층에 속하지 않는 것은? → 정답 2) 네트워크 계층
- [1-QUESTIONS] 3주차 1차시 퀴즈 2 — 다음 중 HTTP에 대한 설명으로 옳은 것은? → 정답 1) 무상태 방식
- [1-QUESTIONS] 3주차 1차시 퀴즈 3 — 다음 중 BASE64 인코딩에 대한 내용으로 틀린 것은? → 정답 4) 데이터를 8비트 단위로 분할하며, 총 64개의 문자 집합으로 표현
- [1-QUESTIONS] 3주차 2차시 퀴즈 1 — 다음 중 프레임워크와 플랫폼에 대한 설명 중 옳은 것은? → 정답 3) 프레임워크는 특정한 개발방식(패턴)을 강제한다.
- [1-QUESTIONS] 3주차 2차시 퀴즈 2 — 다음 중 프레임워크별 지원 언어에 대한 설명이 잘못된 것은? → 정답 4) Ruby on Rails
- [1-QUESTIONS] 3주차 2차시 퀴즈 3 — 다음 중 Spring Framework와 비교하여 Spring Boot의 장점이 아닌 것은? → 정답 2) WAR 패키징
- [1-QUESTIONS] 3주차 3차시 퀴즈 1 — 다음 중, Spring Boot 개발 방법론에서 계층별 설명이 잘못된 것은? → 정답 4) Service
- [1-QUESTIONS] 3주차 3차시 퀴즈 2 — 게시판 만들기 실습에서 사용한 테스트용 In-Memory DB의 이름은? (2글자) ( ) → 정답 ( H2 )
- [1-QUESTIONS] 3주차 3차시 퀴즈 3 — 다음 중, 게시판 만들기 실습 내용에 대한 설명 중 잘못된 것은? → 정답 1) PUT /posts
- [1-QUESTIONS] 4주차 1차시 퀴즈 1 — 정규식에서 `^` (Caret) 기호의 의미로 알맞은 것은? → 정답 2) 문자열의 시작을 의미
- [1-QUESTIONS] 4주차 1차시 퀴즈 2 — 다음 중 정규식 `a?b`가 매칭할 수 있는 문자열은 무엇일까요? (2개) → 정답 1) b, 2) ab
- [1-QUESTIONS] 4주차 1차시 퀴즈 3 — 정규식을 사용할 때, 특정 문자가 한 번 이상 반복될 경우 사용할 수 있는 기호는 무엇일까요?　(　　) → 정답 ( + ) — `+`는 앞에 나온 문자가 한 번 이상 반복될 경우 매칭할
- [1-QUESTIONS] 4주차 2차시 퀴즈 1 — 다음 리눅스 명령어 중 정규식을 활용할 수 없는 것은? → 정답 3) ps
- [1-QUESTIONS] 4주차 2차시 퀴즈 2 — 자바 프로그램에서 정규식을 받아들여 패턴을 정의하는데 사용하는 클래스명은?　(　　) → 정답 ( Pattern )
- [1-QUESTIONS] 4주차 2차시 퀴즈 3 — 다음 중 정규식 사용시 발생 가능한 문제점이 아닌것은? → 정답 1) DDoS 보안 문제
- [1-QUESTIONS] 4주차 3차시 퀴즈 1 — 클라이언트의 HTTP 요청과 응답을 가로채어 특정 작업을 수행하는 서블릿 기반 컴포넌트는 무엇인가? → 정답 3) Filter
- [1-QUESTIONS] 4주차 3차시 퀴즈 2 — String 클래스에서 정규식으로 지정한 문자열을 다른 문자열로 바꾸기 위해 사용하는 메서드 이름은? (영문 10글자, . 제외)　(　　) → 정답 ( replaceAll )
- [1-QUESTIONS] 4주차 3차시 퀴즈 3 — 다음 중 XSS 입력값 필터에서 처리해야 하는 내용이 아닌 것은? → 정답 4) 압축파일 안에 들어있는 스크립트 파일 제거
- [1-QUESTIONS] 5주차 1차시 퀴즈 1 — 다음 중 인증과 인가에 대한 설명 중 잘못된 것은? → 정답 1) 인증은 사용자에게 리소스 접근 가능한 권한을 부여하는 것
- [1-QUESTIONS] 5주차 1차시 퀴즈 2 — 사용자의 역할에 따라 접근 권한을 부여하는 방식을 나타내는 용어는? (영문 4글자) ( ) → 정답 ( RBAC )
- [1-QUESTIONS] 5주차 1차시 퀴즈 3 — 다음중 인가 보안 위협에 대한 대응 방안은? → 정답 1) 최소권한원칙
- [1-QUESTIONS] 5주차 2차시 퀴즈 1 — 다음 중 OAuth2에 대한 설명으로 맞지 않는 것은? → 정답 4) 비밀번호를 통해 접근 권한을 위임
- [1-QUESTIONS] 5주차 2차시 퀴즈 2 — OAuth2의 구성 요소에 대한 설명 중 잘못된 것은? → 정답 1) Resource Owner
- [1-QUESTIONS] 5주차 2차시 퀴즈 3 — Access Token 재발급을 위한 장기 인증 수단으로, 사용자 재로그인 없이 새로운 Access Token을 발급하기 위해 사용하는 Token의 이름은 무… → 정답 ( refresh )
- [1-QUESTIONS] 5주차 3차시 퀴즈 1 — JWT의 주요 특징에 해당하지 않는 것은? → 정답 4) 헤더-페이로드-트레일러 로 구성
- [1-QUESTIONS] 5주차 3차시 퀴즈 2 — JWT의 단점 중 틀린 것은? → 정답 1) 만료 시간 전 강제 무효화를 위한 관리자 페이지 필요
- [1-QUESTIONS] 5주차 3차시 퀴즈 3 — JWT 페이로드에 포함시키는 사용자 식별자, 역할, 권한 등의 정보를 일컫는 단어는? ( ) → 정답 ( 클레임 또는 claim )
- [1-QUESTIONS] 6주차 1차시 퀴즈 1 — 다음 중 ORM(Object-Relational Mapping)의 주요 장점이 아닌 것은? → 정답 3) 모든 SQL 최적화를 자동으로 수행하여 성능 문제 없음
- [1-QUESTIONS] 6주차 1차시 퀴즈 2 — MyBatis 프레임워크의 특징으로 적절한 것은? → 정답 2) SQL을 직접 작성하면서도 매핑 작업을 줄여 생산성을 높임
- [1-QUESTIONS] 6주차 1차시 퀴즈 3 — ORM을 잘못 사용할 경우 발생할 수 있는 대표적인 보안 취약점 중 하나로, SQL 쿼리를 문자열 결합 방식으로 생성할 때 발생할 수 있는 공격 기법은 무엇인… → 정답 ( SQL Injection 또는 SQL 인젝션 )
- [1-QUESTIONS] 6주차 2차시 퀴즈 1 — 다음 중 SQL 인젝션을 예방하기 위한 방법으로 옳지 않은 것은 무엇일까요? → 정답 3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.
- [1-QUESTIONS] 6주차 2차시 퀴즈 2 — 다음 중 SQL 인젝션 공격으로 인해 발생할 수 있는 피해가 아닌 것은 무엇일까요? → 정답 4) 네트워크 장비가 물리적으로 파손된다.
- [1-QUESTIONS] 6주차 2차시 퀴즈 3 — SQL 인젝션 방어를 위해 Java에서 동적 SQL 대신 권장되는 JDBC API 클래스 이름은? ( ) → 정답 ( PreparedStatement )
- [1-QUESTIONS] 6주차 3차시 퀴즈 1 — 다음 중 Windows 환경에서 Command 인젝션 위험을 줄이기 위한 방법으로 가장 옳은 것은 ? → 정답 3) 명령 인자를 배열로 분리하고, 권한이 제한된 계정으로 실행한다.
- [1-QUESTIONS] 6주차 3차시 퀴즈 2 — 다음 중 Command 인젝션 공격 예시로 볼 수 있는 것은 ? → 정답 3) ls; rm -rf /
- [1-QUESTIONS] 6주차 3차시 퀴즈 3 — Linux 환경에서 명령어를 연속 실행하기 위해 자주 사용되는 쉘 연산자 기호를 정확히 쓰세요. ( ) → 정답 ( ; )
- [1-QUESTIONS] 7주차 1차시 퀴즈 1 — 다음 중 로컬 저장소(LocalStorage)에 민감 정보를 저장했을 때 발생할 수 있는 문제가 아닌 것은 ? → 정답 3) 도메인이 다르면 로컬 저장소를 공유할 수 있다.
- [1-QUESTIONS] 7주차 1차시 퀴즈 2 — SSR(Server-Side Rendering)과 CSR(Client-Side Rendering)에 대한 설명으로 옳은 것은 ? → 정답 3) SSR은 서버에서 HTML을 완성해 응답하고, CSR은 클라이언트가
- [1-QUESTIONS] 7주차 1차시 퀴즈 3 — 프론트엔드에서 외부 스크립트나 스타일의 로딩 출처를 제한해 XSS 같은 공격을 완화하기 위해 사용하는 보안 정책은 ? (영문 3글자) ( ) → 정답 ( CSP )
- [1-QUESTIONS] 7주차 2차시 퀴즈 1 — 다음 중 XSS 방어 기법에 해당하지 않는 것은 ? → 정답 4) CSRF 토큰을 사용해 사용자 요청이 정당한지 검증
- [1-QUESTIONS] 7주차 2차시 퀴즈 2 — 다음 중 XSS를 유발할 수 있는 취약한 코드 예시로 옳은 것은 ? → 정답 1) out.println("You searched for: " + re
- [1-QUESTIONS] 7주차 2차시 퀴즈 3 — XSS의 종류 중 서버를 거치지 않고, 클라이언트 자바스크립트 로직에서 발생하는 공격 방식은? (영어 대문자 3글자) ( ) → 정답 ( DOM )
- [1-QUESTIONS] 7주차 3차시 퀴즈 1 — 다음 중 CSRF 공격이 성공하기 위해 반드시 필요한 조건은 ? → 정답 1) 중요 웹사이트에 로그인되어 쿠키를 보유하고 있어야 한다.
- [1-QUESTIONS] 7주차 3차시 퀴즈 2 — 다음 중 CSRF 방어 기법에 해당하지 않는 것은 ? → 정답 4) 암호화된 비밀번호로 로그인 처리
- [1-QUESTIONS] 7주차 3차시 퀴즈 3 — CSRF 공격을 완화하기 위해 쿠키에 설정하는 속성 중, 외부 도메인에서 요청이 발생했을 때 쿠키가 자동 전송되지 않도록 제한하기 위해 사용하는 속성은 ? ( ) → 정답 ( SameSite )

---

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

---

# [4-NOTES] 6주차 관련 정리 (신뢰도 C~D) — 교안·발화가 다른 지점. 시험 답은 교안 우선.

## [4-NOTES] 6주차 1차시 · ORM과 SQL 인젝션 — 과장 (C)
키워드: ORM, SQL 인젝션, Native Query, 문자열 결합
- [6주차 1차시 07:08]: "ORM 방식은 원천적으로 SQL 인젝션이 존재할 수 없다"고 함.
- 바로잡음: 과장. [6주차 1차시 31:14]와 [2-SLIDES] 6주차 1차시 p.22는 **문자열 결합으로 동적 쿼리를 만들거나 Native Query를 쓰면 다시 취약**하다고 명시. 시험에서 "ORM이면 SQL 인젝션 불가능"은 틀린 보기.

## [4-NOTES] 6주차 1차시 · MyBatis where 태그 동작 — 오류 (C)
키워드: MyBatis, where 태그, if 태그, AND
- [6주차 1차시 29:00]: "각 요소가 늘어나면 그 사이에 자동으로 AND(end) 키워드가 삽입된다"고 함.
- 바로잡음: AND는 개발자가 직접 씀. `<where>` 태그의 역할은 조건이 하나라도 있으면 WHERE를 붙이고 **맨 앞의 AND/OR를 제거**하는 것. [2-SLIDES] 6주차 1차시 p.18 설명·동작과 일치하는 쪽이 맞음.

## [4-NOTES] 6주차 3차시 · $IFS 공백 우회 예시 — 부정확 (C)
키워드: Command Injection, IFS, 환경변수, 공백 우회
- [6주차 3차시 13:43] 및 손글씨: 입력값에 IFS 환경변수를 공백 없이 붙이면 "값 공백 ls"로 치환된다고 설명.
- 바로잡음: 영문자가 바로 뒤에 붙으면 셸이 전체를 하나의 변수 이름으로 읽어 동작하지 않음. 의도대로 되려면 중괄호로 변수명을 감싸야 함. ([2-SLIDES] 6주차 3차시 p.12 검증 메모와 같은 취지)

## [4-NOTES] 6주차 1차시 · User 엔티티 id 타입 불일치 — 교안 내부 모순 (C)
키워드: ORM, 엔티티, 매핑, Long, GeneratedValue
- [2-SLIDES] 6주차 1차시 p.5: User 엔티티 id는 Long + 자동 증가(IDENTITY)인데, 오른쪽 예시 테이블의 id 값은 문자열(guest/admin/operator). [2-SLIDES] 6주차 1차시 p.17 MyBatis 예시는 id를 int로 받음. 개념 설명용 축약으로 이해.

## [4-NOTES] 공통 · 자동 전사 한계 (C)
키워드: 녹취, 자동 전사, 불명확, 음성 인식
- 3-TRANSCRIPT는 자동 전사라 영문 용어·숫자·포트·메서드명에 오인식이 있을 수 있음([불명확]·[표현 차이] 표시). 숫자·코드·정확한 용어는 2-SLIDES(교안)를 우선.
- 6·7주차 녹취는 화면 기록이 없어 교수님 펜 강조 위치를 알 수 없음. 7주차는 1차시 앞부분(시험 안내)과 3차시 중간에 무음 구간이 있어 누락 가능.

## [4-NOTES] 시험 안내 (B, 발화 근거)
키워드: 중간고사, 시험, LMS, 온라인, 범위
- [7주차 1차시 00:00] 발화: 8주차에 중간고사, LMS 온라인 실시간, 공지사항 확인 요망. 범위는 "오늘까지 수업 내용"(1~7주차).
- 시험 규정(사용자 확인): 2026-10-22(목) 19:00~20:00, 온라인 LMS 퀴즈, AI·오픈북 가능, 범위 1~7주차. 날짜·시간은 LMS 공지로 최종 확인.

---

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

---

# [3-TRANSCRIPT] 6주차 1차시 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · MyBatis/마이바티스/Mapper/매퍼/#{}/${}/동적 SQL · Dirty Checking/더티 체킹/변경 감지 · Mass Assignment/대량 할당/DTO/isAdmin · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state

[6주차 1차시 00:00] 네, 안녕하세요.
[6주차 1차시 00:05] 시큐어 코딩 6주차 1차시 강의 시작하도록 하겠습니다.
[6주차 1차시 00:11] 이번에 학습할 내용은 ORM 프레임워크라는 것에 대한 이해와 활용이 되겠습니다.
[6주차 1차시 00:22] 이번 시간 학습 목표는 다음과 같습니다.
[6주차 1차시 00:26] ORM 프레임워크의 개념과 동작 방식을 먼저 알아보고요.
[6주차 1차시 00:31] ORM을 사용하면서 발생할 수 있는 보안 취약점과 보안 위협을 살펴보고
[6주차 1차시 00:36] 여기에서 발생할 수 있는 인젝션 공격을 방어하는 보안 대책도 알아보도록 하겠습니다.
[6주차 1차시 00:46] 우리가 배워볼 내용으로는 ORM 프레임워크가 어떤 것인지 그리고 장단점은 무엇인지 알아보고
[6주차 1차시 00:55] 널리 사용하고 있는 마이바티스 프레임워크는 어떻게 다른지, 어떤 경우에 취약점이 발생하게 되는지 알아보도록 하겠습니다.
[6주차 1차시 01:10] 먼저 첫 번째로 ORM 개념과 기본 원리 살펴보도록 하겠습니다.
[6주차 1차시 01:21] ORM의 정의와 필요성인데요.
[6주차 1차시 01:26] ORM은 객체 지향 언어의 객체와 관계형 데이트베이스의 테이블 간 데이터를 자동으로 연결해주는 기술입니다.
[6주차 1차시 01:40] 자바의 유저 클래스를 데이터베이스의 유저 수 테이블에 맵핑하기만 하면 되니까
[6주차 1차시 01:45] 복잡한 SQL 없이 객체만 다루면 되기 때문에 코드를 간결하게 유지할 수 있습니다.
[6주차 1차시 01:52] 이 프레임워크의 필요성으로
[6주차 1차시 01:54] 첫 번째는 불일치 문제 해결입니다.
[6주차 1차시 01:59] 객체 모델과 데이터베이스 스키마 간 구조나 네이밍이 다르면
[6주차 1차시 02:03] 수동 맵핑으로 오류가 발생하기 쉬운데요.
[6주차 1차시 02:08] ORM은 어노테이션만 적절하게 달아주면
[6주차 1차시 02:11] 자동으로 필드와 칼럼을 연결해 주기 때문에
[6주차 1차시 02:15] 맵핑 오류를 완전 차단합니다.
[6주차 1차시 02:18] 두 번째는 개발 생산성 향상입니다.
[6주차 1차시 02:23] 직접 SQL문을 작성하고 파라미터를 바인딩하던 반복 작업이 사라지다 보니 개발자는 비즈니스 로직에만 집중할 수 있습니다.
[6주차 1차시 02:32] 이 과정에서 코드가 간결해지고 가독성이 높아져 유지보수 단계에서도 효율이 크게 개선됩니다.
[6주차 1차시 02:41] 세 번째는 유지보수성과 보안 강화인데요.
[6주차 1차시 02:46] 데이터베이스 접근 과정이 추상화되기 때문에 SQL 인젝션 같은 취약점을 최소화하고
[6주차 1차시 02:54] 트랜잭션 처리나 커넥션 관리도 일관된 API를 통해 안전하게 수행됩니다.
[6주차 1차시 03:03] 그래서 화면 왼쪽 예제는 이 엔티티 어노테이션을 붙인 유저 클래스가 있고
[6주차 1차시 03:09] 오른쪽 그림은 유저 테이블 구조가 나와 있습니다.
[6주차 1차시 03:16] 이처럼 ORM을 도입하면 코드와 테이블 간 맵핑이 단순해지고
[6주차 1차시 03:21] 객체 모델과 스키마 간 불일치 해소, 생산성 향상, 마지막으로 보안 강화를 동시에 달성할 수 있습니다.
[6주차 1차시 03:31] 또한 하이버네이트와 같은 JPA 구현체를 쓴다면
[6주차 1차시 03:37] 연관관계 맵핑이나 데이터 패치 전략을 세밀하게 제어할 수 있어서
[6주차 1차시 03:43] 대용량 데이터 처리 시에도 성능과 보안을 균형있게 유지할 수 있습니다.
[6주차 1차시 03:50] 마지막으로 ORM 도입 후에는 실제 실행 SQL을 로깅하고 단위 통합 테스트를 통해 맵핑 정책과 보안 설정을 반드시 검증해야 합니다.
[6주차 1차시 04:03] 이 과정을 통해서 안정적이고 안전한 데이터 액세스 구조를 완성할 수 있습니다.
[6주차 1차시 04:17] 이번에는 전통적인 SQL 쿼리와 OMR 방식을 정리를 해보겠습니다.
[6주차 1차시 04:25] 먼저 왼쪽, 전통적인 SQL 쿼리입니다.
[6주차 1차시 04:29] 전통 SQL은 개발자가 SQL문을 직접 작성하여 데이터베이스와 상호작용하는 방식을 말하는데요.
[6주차 1차시 04:39] 쿼리의 구조를 설계하고 조인이나 서브 쿼리 같은 복잡한 조회문을 세밀하게 제어를 할 수 있습니다.
[6주차 1차시 04:48] 또 데이터베이스 관리 시스템 고유의 최적화 기능을 직접 활용할 수 있기 때문에
[6주차 1차시 04:55] 저희가 매우 세밀한 성능 튜닝이 필요한 경우에 유리합니다.
[6주차 1차시 05:02] 하지만 단점도 분명한데요.
[6주차 1차시 05:06] 커넥션 관리, 파라미터 바인딩, 결과 맵핑 같은 반복 작업을 매번 수작업으로 처리해야 하고 프로젝트 규모가 커질수록 SQL 문자열이 흩어져 관리가 어려워집니다.
[6주차 1차시 05:20] 특히 보안 취약점인 SQL 인젝션을 방어하려면 모든 쿼리의 파라미터 바인딩을 꼼꼼히 적용해야 하는데요.
[6주차 1차시 05:30] 하지만 오른쪽 ORM 방식은 객체지향 언어의 객체와 관계형 데이터베이스의 테이블을 자동으로 맵핑합니다.
[6주차 1차시 05:41] 하여 개발자는 메서드 호출이나 객체 조작만으로 데이터베이스 작업을 수행할 수 있기 때문에 코드 가독성과 유지 보수성이 크게 향상됩니다.
[6주차 1차시 05:55] 또 데이터베이스 종속 코드가 최소화되므로
[6주차 1차시 05:58] DBMS 교체가 용이하고
[6주차 1차시 06:01] JPA나 하이버네이트 같은 부연체를 통해
[6주차 1차시 06:06] 데이터 패치 전략과 캐시를 일관되게 관리할 수 있습니다.
[6주차 1차시 06:11] 하지만 ORM도 사용에 유의하지 않으면
[6주차 1차시 06:16] 추상화 계층이 성능 방목을 일으키거나
[6주차 1차시 06:19] 복잡한 대량 조회 시 BOU를 초래할 수 있게 됩니다.
[6주차 1차시 06:25] 따라서 핵심 조회 로직은 전통 SK를 혼용하고
[6주차 1차시 06:29] 나머지 일반 CRUD는 ORM으로 처리하는 하이브리드 전략을 권장하고 있습니다.
[6주차 1차시 06:45] 이러한 ORM 방식을 사용하면 객체의 지향적인 면이 강화되므로 개발 속도가 향상되는 것은 어쩌면 당연한 일입니다.
[6주차 1차시 06:57] ORM 방식으로 연동시킬 수만 있다면 데이터베이스가 다른 제품으로 바뀌더라도 소스코드 변경 없이 그대로 사용할 수 있을 정도이니까요.
[6주차 1차시 07:08] 그리고 앞서 언급했듯이 쿼리문을 일일이 텍스트 문장으로 만들어 사용하는 방식이 아니기 때문에
[6주차 1차시 07:15] 원천적으로 SQL 인젝션과 같은 취약점이 존재할 수가 없습니다.
[6주차 1차시 07:20] 표에서 볼 수 있듯이 ORM의 장점은 전통적인 SQL 쿼리의 단점 부분과 비교해 본다면 더욱 잘 드러나는데요.
[6주차 1차시 07:31] 전통적인 방식에서는 쿼리를 조합하는 로직이 반드시 있어야 하며 여러 요건을 만족시키려고 하다보면 복잡하게 꼬일 수가 있어서 스파게티처럼 코드가 나가게 되는데
[6주차 1차시 07:45] 이런 코드를 나중에 유지 보수를 하려면 정말 조심스럽기도 하고 위험하기 때문에 생산성도 떨어지게 됩니다.
[6주차 1차시 07:54] 만약 또
[6주차 1차시 07:55] 데이터베이스가 다른 것으로
[6주차 1차시 07:58] 바뀌어야 한다면
[6주차 1차시 07:59] 쿼리문의 문법 사용 방법이 함께 바뀔 수 있기 때문에
[6주차 1차시 08:03] 이와 관련된 소스 코드도 모두 재검토 및 재개발할 수밖에 없습니다.
[6주차 1차시 08:09] 그리고 쿼리문을 조작하는 과정에 사용자 입력 값을 합치는 과정을 다뤄야 함으로
[6주차 1차시 08:15] SQL 인젝션 위험성을 항상 안고 있을 수밖에 없게 되죠.
[6주차 1차시 08:20] 반면에 ORM 방식의 단점이라면 복잡한 조인이나 객체 간 연관관계를 통한 대량의 데이터를 취급할 때
[6주차 1차시 08:29] 최적화가 어려워서 성능이 급격히 떨어질 수 있다는 점입니다.
[6주차 1차시 08:36] 데이터베이스를 설계할 때는 ORM의 동작 방식을 감안하는 것이 중요하다는 점을 꼭 기억하시길 바랍니다.
[6주차 1차시 08:44] 이와 대응되는 그래도 전통적인 SQL 쿼리의 장점을 보자면 데이터베이스의 기능을 100% 있는 그대로 활용하여 최적화할 수 있다는 점입니다.
[6주차 1차시 09:04] 그럼 이번에는 관점을 조금 바꿔서 전통적인 SQL 쿼리 방식과 ORM 중에서 각각 어떤 경우에 사용하는 것이 더 적합한지 살펴보도록 하겠습니다.
[6주차 1차시 09:16] 먼저 전통적인 SQL 쿼리 방식이 적합한 경우인데요.
[6주차 1차시 09:21] 첫째, 절대적으로 성능 튜닝이 중요한 경우입니다.
[6주차 1차시 09:25] 실행 계획을 직접 분석하여 인덱스 힌트 파티셔닝 전략을 적용해야 할 때 수동 퀄이 작성이 가능하기 때문에 빈틈없는 최적화를 수행할 수 있습니다.
[6주차 1차시 09:37] 예를 들어 로그 테이블에서 일별 트래픽 추이를 실시간 집계할 때는 윈도우 함수와 저장 표시절을 활용하여 메모리 사용량과 인풋아웃 비용을 정교하게 제어할 수 있죠.
[6주차 1차시 09:52] 또 둘째, 복잡한 다중조인이나 서브퍼리가 필요한 리포팅 로직입니다.
[6주차 1차시 09:59] 엔터프라이즈급 리포트 생성 시 여러 테이블을 중첩 조회해야 할 때
[6주차 1차시 10:03] 명령형 접근방식이 더 직관적이고
[6주차 1차시 10:06] DBMS 고유 특성을 활용하기에는 유리합니다.
[6주차 1차시 10:11] 셋째로는 특정 DBMS 독립기능을 적극 활용해야 할 경우입니다.
[6주차 1차시 10:16] 예를 들어 오라클의 플래시백 퀄이나 마이크로소프트 SQL 서버의 컬럼 스토어 인덱스 같은 고급 기능은 전통 SQL에만 완전하게 지원이 됩니다.
[6주차 1차시 10:28] 다음은 ORM 방식이 적합한 경우인데요.
[6주차 1차시 10:32] 첫째, CRUD 중심의 애플리케이션 개발이나 빠른 프로토타이핑이 필요할 때입니다.
[6주차 1차시 10:39] 객체 모델과 데이터베이스 맵핑을 자동화하여 기본 생성 조회 수정 삭제, 즉 CRUD 로직을 즉시 구현할 수 있어서 개발 생산성이 크게 향상됩니다.
[6주차 1차시 10:55] 둘째, 유지 보수성과 확장성이 중요한 대규모 서비스에서 DBMS 교체나 마이크로 서비스 전환을 염두에 둘 때에도 ORM이 효과적입니다.
[6주차 1차시 11:07] JPA 구현체나 하이버네이트를 사용하면 패치 전략과 2차 캐시를 공유하고 테스트 환경에서는 인메모리 데이터베이스로 손쉽게 전환할 수 있어서 테스트 커버리지가 대폭 늘어납니다.
[6주차 1차시 11:26] 지금부터는 ORM이 제공하는 핵심 기능 3가지에 대해 자세히 설명해 보도록 하겠습니다.
[6주차 1차시 11:32] 첫째는 객체 테이블 맵핑 기능입니다.
[6주차 1차시 11:36] 개발자는 별도의 SQL 작성 없이 Java 클래스와 데이터베이스 테이블, 그리고 클래스 필드와 테이블 컬럼 간 맵핑만 설정하면 됩니다.
[6주차 1차시 11:48] 예를 들어 유저 클래스의 ID, Name, Email 필드를 DB의 Users 테이블의 ID, Name, Email 컬럼에 자동으로 연결을 해줄 수 있습니다.
[6주차 1차시 11:59] 이 덕분에 JDBC 코드나 Query String을 일일이 관리할 필요가 없어서 개발 초기 생산성이 크게 올라갑니다.
[6주차 1차시 12:08] 또 보안 관점에서는 파라미터 마인딩이 자동 적용되어 SQL 인젝션 위험이 자연스럽게 감소합니다.
[6주차 1차시 12:15] 둘째, 관계 맵핑 기능입니다.
[6주차 1차시 12:19] 1대1, 1대4, 다대다 관계를 어노테이션 또는 XML 설정으로 정의하면 내부적으로 조인 로직이 자동 생성됩니다.
[6주차 1차시 12:29] 예컨대 주문 객체 오더와 주문 내역의 아이템 객체 오더 아이템 간 1대 N 관계를 1대 M, M대 N 어노테이션으로 선언하면 주문 데이터를 조회할 때 관련 아이템을 한 번에 로드하거나 지연 로딩을 적용하여 성능을 최적화할 수 있습니다.
[6주차 1차시 12:49] 그리고 이 과정 역시 SQL 도입문을 직접 다루지 않아도 되므로 코드 가독성과 보안 검증이 수월해집니다.
[6주차 1차시 12:59] 셋째, 자동 스키마 생성 및 업데이트 기능입니다.
[6주차 1차시 13:03] 도메인 모델을 변경하면 DB 스키마를 자동으로 생성해주거나 업그레이드 스크립트를 생성을 해줍니다.
[6주차 1차시 13:10] 새로운 엔티티나 칼럼이 추가될 때마다 수동 마이크레이션 부담이 크게 줄어들고 스키마 버전 관리를 위한 별도 툴을 연동하는 것도 간편해집니다.
[6주차 1차시 13:22] 다음은 CRUD 작업 지원입니다.
[6주차 1차시 13:26] Create, Read, Update, Delete 이 동작은 모두 객체 조작과 메소드 호출만으로 처리가 됩니다.
[6주차 1차시 13:34] 더 중요한 것은 Dirty Checking Mechanism이라는 것인데요.
[6주차 1차시 13:37] 트랜잭션 중간에 엔티티 객체의 상태가 변경되면
[6주차 1차시 13:41] 커밋 시점까지 변경된 부분만 자동으로 추출하여
[6주차 1차시 13:45] 업데이트 쿼리를 통해 동기화해 줍니다.
[6주차 1차시 13:50] 이 과정 덕분에 불필요한 업데이트가 발생하지 않으며
[6주차 1차시 13:54] 보안 로직을 엔티티 단위로 집중 적용할 수도 있습니다.
[6주차 1차시 14:03] 이처럼 ORM은 맵핑 관계의 정의, 자동 스키마 생성부터 CRUD 및 더티 치킹에 이르기까지 데이터 액세스 전반을 추상화하여 생산성과 보안, 유지 보수성을 모두를 크게 향상시켜 줄 수 있습니다.
[6주차 1차시 14:25] 이번에는 ORM이 제공하는 고급 퀄리 기능 및 레이지 로딩과 캐싱 메커니즘을 자세히 살펴보도록 하겠습니다.
[6주차 1차시 14:37] 우선 고급 퀄리 기능입니다.
[6주차 1차시 14:40] ORM은 SQL 대신 객체 지향적인 퀄리 언어를 제공하는데요.
[6주차 1차시 14:46] 대표적으로 하이버네이트에서 지원하는 HQL과 JPA에 기반해서 지원하는 JPQL이 있는데요.
[6주차 1차시 14:54] 이 언어들은 테이블이 아니라 엔티티 객체와 필드를 대상으로 쿼리를 작성하도록 추상화된 방식입니다.
[6주차 1차시 15:04] 객체 모델에 맞춰 코드를 짤 수 있는 언어라서 가독성이 높고 유지 보수도 훨씬 수월해집니다.
[6주차 1차시 15:12] 다음은 Criteria API 기능입니다.
[6주차 1차시 15:15] 이것은 자바코드 안에서 동적으로 쿼리를 구성할 수 있는 프로그래밍 방식 인터페이스인데요.
[6주차 1차시 15:21] 메소드 체인 방식으로 조건과 정렬, 그루핑을 표현할 수 있기 때문에 조건이 복잡하게 바뀌더라도 문자열을 연결하는 오류 없이 쿼리를 만들 수 있습니다.
[6주차 1차시 15:34] 그리고 필요에 따라 네이티브 쿼리를 직접 실행할 수 있는 기능도 제공합니다.
[6주차 1차시 15:40] 이렇게 제공되는 기능들은 복잡한 성능 튜닝이나 DBMS 고유 기능을 활용해야 할 때 매우 유용합니다.
[6주차 1차시 15:49] 추상화 계층을 유지하면서도 특정 쿼리만 직접 작성해 실행할 수 있기 때문에 성능과 유연성을 모두 잡을 수 있습니다.
[6주차 1차시 15:58] 다음은 레이지 로딩, 즉 지연 로딩과 캐싱 기능입니다.
[6주차 1차시 16:04] 지연 로딩은 실제 객체가 사용되려는 그 시점에 관련 데이터를 DB로부터 불러오기 때문에 초기 로딩 부담을 최소화합니다.
[6주차 1차시 16:13] 예컨대 어떤 주문 엔티티를 조회할 때는 주문 기본 정보만 로드하고, 주문 항목 목록은 실제 참조할 때 비로소 가져오도록 설정할 수 있습니다.
[6주차 1차시 16:27] 그리고 1차 캐시와 2차 캐시를 통해 반복 조회 시 성능을 최적화합니다.
[6주차 1차시 16:32] 1차 캐시는 같은 세션 내에서 엔티티를 중복 조회하지 않도록 캐시를 하고,
[6주차 1차시 16:42] 2차 캐시는 애플리케이션 전역에 공유 가능한 캐시 레이어를 제공하여 데이터베이스 부하가 크게 줄어듭니다.
[6주차 1차시 16:54] ORM이 제공하는 주요 기능 중 트랜잭션 관리 기능과 부가 기능들을 차근차근 살펴보도록 하겠습니다.
[6주차 1차시 17:02] 우선 트랜잭션 관리부터 보면, ORM을 사용하면 서비스 메소드 위에 트랜잭션을 어노테이션만 붙이면 메소드가 시작될 때 자동으로 트랜잭션이 열리고 정상적으로 끝나면 커밋, 중간에 오류가 나면 자동으로 롤백이 이루어집니다.
[6주차 1차시 17:22] 덕분에 개발자는 일일이 커밋과 롤백 코드를 작성하지 않아도 되고, 트랜잭션 누락이 발생해서 데이터 일관성이 깨질 수 있는 위험을 크게 줄일 수 있습니다.
[6주차 1차시 17:35] 다음은 동시성 제어 기능입니다. 두 가지 대표 방식을 지원하는데요. 하나는 낙관적 락입니다.
[6주차 1차시 17:42] 이 방식은 내가 마지막으로 본 데이터 그대로인가를
[6주차 1차시 17:48] 마지막 순간에만 확인해보고 다른 사용자가 먼저 바꿨다는 게 발견되면
[6주차 1차시 17:53] 예외를 던져 재시도를 유도합니다.
[6주차 1차시 17:57] 충돌 빈도가 낮을 때 유리한 방식이고요.
[6주차 1차시 18:03] 다른 하나는 이제 비관적 락인데요.
[6주차 1차시 18:07] 데이터베이스가 먼저 해당 레코드에 자물쇠를 채우듯 잠금을 걸어 다른 사용자의 접근을 막습니다.
[6주차 1차시 18:14] 충돌 가능성을 완전히 차단해야 할 때 사용하면 좋지만
[6주차 1차시 18:18] 과도한 잠금으로 인한 대기는 성능 저하를 가져올 수 있겠죠 당연히.
[6주차 1차시 18:25] 이 밖에도 ORM은 엔티티 간 관계 맵핑과 데이터 패치 전략을 통해 데이터 로딩 방식을 정교하게 제어합니다.
[6주차 1차시 18:34] 일대다 관계를 레이지 로딩, 즉 지연 로딩으로 설정해서 필요할 때만 데이터를 불러오거나
[6주차 1차시 18:41] 반대로 로딩으로 한 번에 모두 가져오게끔 하여 추가 커리 호출을 줄일 수도 있습니다.
[6주차 1차시 18:51] 이 두 가지 방식을 상황에 맞춰서 조합을 하면 메모리와 네트워크 자원을 효과적으로 관리할 수 있습니다.
[6주차 1차시 19:04] 마지막으로 OMR은 확장 기능도 풍부하게 제공하는데요.
[6주차 1차시 19:08] XML 설정, 어누테이션, 플러그인 방식 등을 통해
[6주차 1차시 19:12] 엔티티 저장 전 후에 자동으로 보안 검사나 로그 기록을 삽입할 수가 있고
[6주차 1차시 19:18] 사용자 정의 타입 맵핑을 적용하여 암호화된 컬럼도 손쉽게 다룰 수 있습니다.
[6주차 1차시 19:25] 이 모든 기능이 모여 ORM은 단순한 맵핑 도구를 넘어
[6주차 1차시 19:29] 개발 생산성과 시스템 안전성을 동시에 높여주는 핵심 프레임워크로 사용되고 있습니다.
[6주차 1차시 19:38] 다음으로는 MyBatis라는 프레임워크에 대해 알아보도록 하겠습니다.
[6주차 1차시 19:49] 우리가 지금까지는 ORM 프레임워크를 살펴보면서 얼마나 많은 부분이 자동화되고 편리해지는지를 확인을 했는데요.
[6주차 1차시 19:58] 하지만 한편으로는 내 손으로 직접 SQL을 다루고 싶다
[6주차 1차시 20:04] 또는 복잡한 조인이나 DBMS 고유 기능을 세밀하게 제어해야 한다는 요구도 여전히 존재합니다
[6주차 1차시 20:12] 이 지점에서 등장하는 것이 바로 MyBatis입니다
[6주차 1차시 20:16] 마이바티스는 Java Persistence Framework라기보다는 SQL 맵핑 도구라고 부르는 편이 더 잘 어울리는데요.
[6주차 1차시 20:29] 개발자가 직접 작성한 SQL 문을 XML 맵퍼 파일이나 어노테이션에 적용하고 그 결과를 Java 객체에 깔끔하고 효율적으로 바인딩해주는 역할을 맡기 때문입니다.
[6주차 1차시 20:50] 마이바티스의 핵심 가치는 수동으로 작성한 SQL과 자동 맵핑이라는 두 축 위에 있는데요.
[6주차 1차시 20:59] JDBC 코드를 반복해서 작성하는 상황을 생각해 본다면
[6주차 1차시 21:03] 커넥션 열고 Prepared Statement 만든 뒤
[6주차 1차시 21:07] Parameter Binding 하고 결과를 일일이 객체에 담아서
[6주차 1차시 21:13] Finally에서 닿는 과정의 연속인데
[6주차 1차시 21:18] MyBatis를 도입을 하면 이런 Boiler Plate 코드가 대부분 사라집니다.
[6주차 1차시 21:25] 대신 이제 여러분이 작성한 SQL이 매퍼 파일 안에 남고
[6주차 1차시 21:29] 자바코드에서는 간단히 한 줄 호출로 결과를 받아올 수 있습니다.
[6주차 1차시 21:35] 또한 마이바티스는 복잡한 쿼리를 처리할 때도 불리함이 없습니다.
[6주차 1차시 21:41] 저장 프로시저를 호출하거나 윈도우 함수, 공통 테이블 표현식인 CTE 등을 자유롭게 섞을 수가 있고
[6주차 1차시 21:51] 필요하다면 DBMS 특허 문법까지 그대로 옮길 수 있습니다.
[6주차 1차시 21:57] 반면 JPA는 이런 보급지 기능을 모두 지원하지 못할 때가 많죠.
[6주차 1차시 22:02] 그래서 대규모 데이터 분석, 복잡한 리포트, 성능 튜닝이 중요한 영역에서 마이바티스를 많이 사용하고 있습니다.
[6주차 1차시 22:14] 마이바티스에는 보통 크게 4가지 핵심 기능이 있습니다.
[6주차 1차시 22:19] 먼저 SQL 맵핑 및 실행입니다.
[6주차 1차시 22:22] 개발자는 맵퍼 MXL 파일이나
[6주차 1차시 22:25] 어노테이션의 SQL을 선언적으로 정의를 합니다.
[6주차 1차시 22:32] 이때 내부적으로는 파라미터 바인딩과 결과 맵핑이 자동으로 이루어집니다.
[6주차 1차시 22:38] 두 번째로 동적 SQL 지원이 있습니다.
[6주차 1차시 22:40] if 태그나 for each 반복문 태그를 이용해서
[6주차 1차시 22:48] 분기와 반복이 섞인 복잡한 쿼리를 깔끔하게 작성을 할 수가 있습니다.
[6주차 1차시 22:56] 자버코드 안에서 문자열을 잔뜩 이어붙이는 대신
[6주차 1차시 22:59] XML 태그 안에 로직을 선언하기 때문에
[6주차 1차시 23:02] 가독성과 재사용성이 크게 향상됩니다.
[6주차 1차시 23:06] 세 번째 기능은 타입 핸들러입니다.
[6주차 1차시 23:09] 데이터베이스의 컬럼 타입과 자바 커스텀 클래스를 변환하는 로직을 한 곳에 모아둘 수 있는데요.
[6주차 1차시 23:16] 예를 들면 JSON 문자를 자바 객체로 혹은 로컬 데이트 타임을 SQL 타임 스탬프로 변환하는 코드를 직접 작성해 주입할 수 있습니다.
[6주차 1차시 23:28] 마지막으로 플러그인을 활용하면 커리 실행 전후에 로직을 끼워 넣을 수 있습니다.
[6주차 1차시 23:34] 페이징을 자동으로 처리하거나 모든 SQL을 로깅하거나 특정 파라미터를 암호화, 복구화하는 등의 확장 지점을 만들어줍니다.
[6주차 1차시 23:44] 이렇게 네 가지 기능이 결합되어 MyBatis는 직접 작성한 SQL을 그대로 쓰면서도 반복 코드를 없애고 유지 보수성을 확보하는 독자적인 위치를 차지하게 되었습니다.
[6주차 1차시 24:02] 이번에는 실제 프로젝트의 마이바티스를 세팅할 때 거치는 세 가지 핵심 단계를 차례대로 보도록 하겠습니다.
[6주차 1차시 24:10] 첫 번째는 전역 설정 파일 mybatis.config.xml입니다.
[6주차 1차시 24:17] 이 파일에서는 데이터 소스 정보, 트랜잭션 매니저, 캐시 정책, 플러그인 등록, 별칭 설정 등을 한 번에 정의합니다.
[6주차 1차시 24:29] 특히 여러 환경, 즉 개발, 테스트, 운영 환경에 따라 다른 데이터 소스를 쓰거나
[6주차 1차시 24:36] JDBC 트랜잭션 대신 스프링 관리 트랜잭션을 적용할 때 이 설정 파일 하나로 제어할 수 있다는 점이 큰 장점입니다.
[6주차 1차시 24:45] 두 번째 단계는 매퍼 인터페이스와 매퍼 XML 혹은 어노테이션 매팅을 만드는 작업입니다.
[6주차 1차시 24:54] 보통 각 도메인별로 유저매퍼.xml 같은 파일을 만들고 SQL 문장과 파라미터 타입 결과 매팅 정보를 정의합니다.
[6주차 1차시 25:04] 자바 코드와 매팅 파일을 네임 스페이스로 연결해주면 서비스 레이어에서는 매팅되어 있는 쿼리를 쉽게 실행할 수 있습니다.
[6주차 1차시 25:13] 어노테이션 방식을 택하면 XML 없이 셀렉트 인서트 어노테이션을 인터페이스 메소드 위에 붙여서 관리할 수도 있습니다.
[6주차 1차시 25:24] 세 번째 단계는 SQL 세션 팩토리 및 세션 관리입니다.
[6주차 1차시 25:29] SQL 세션 팩토리 빌더로 글로벌 설정을 업로드해서 SQL 세션 팩토리를 설정하고 Try with Resource 구문으로 SQL 세션을 열고 닫는 방식입니다.
[6주차 1차시 25:43] 스프링 부트 환경에서는 관련 빈을 연동하고
[6주차 1차시 25:46] 트랜잭션 어노테이션으로 트랜잭션 범위를 선언만 하면
[6주차 1차시 25:51] 마이바티스가 스프링의 트랜잭션 경계에 맞춰
[6주차 1차시 25:54] 자동으로 세션을 열고 commit, rollback을 해줍니다.
[6주차 1차시 25:58] 좀 더 자세히 살펴보면
[6주차 1차시 26:04] 마이바티스 설정 파일은 이런 형태로 되어 있습니다.
[6주차 1차시 26:08] 그래서 XML 형식 안에 여러 세트의 설정 내용을
[6주차 1차시 26:12] environment라는 태그를 통해 구분을 하고 있고
[6주차 1차시 26:16] 여기에서는 Development라는 개발환경에 설정 내용이 들어있는 것을 확인할 수 있습니다.
[6주차 1차시 26:26] 이 부분입니다.
[6주차 1차시 26:30] 그 안에 데이터 소스 태그로 묶인 곳에는 맵핑되어 실제 연결하기 위한 JDBC 셋업 정보가 보이는데,
[6주차 1차시 26:45] 이를 통해 소스 코드가 만들어지게 됩니다.
[6주차 1차시 26:49] 그리고 맵핑 내용을 정의한 외부 파일명도 명시가 이렇게 명시되어 있습니다.
[6주차 1차시 27:01] 어떤 방식으로 맵핑하는지도 한번 보도록 하겠습니다.
[6주차 1차시 27:08] 첫 번째 XML 기반 맵핑은 앞서 설정 파일에서 지정한 외부 맵퍼 XML 파일에
[6주차 1차시 27:15] 쿼리문을 넣어놓는 방식입니다.
[6주차 1차시 27:18] 위쪽 그림과 같이 각 쿼리에 아이디를 부여하고
[6주차 1차시 27:23] 이런 식으로 아이디를 부여하고
[6주차 1차시 27:27] 여기까지
[6주차 1차시 27:34] id를 부여하고 결과값을 어느 객체에 되돌려주는지도 지정하여
[6주차 1차시 27:46] 자바 프로그램과의 인터페이스를 규정하고 있습니다.
[6주차 1차시 27:52] 인서트, 업데이트, 딜리트 등의 쿼리별로
[6주차 1차시 27:55] XML의 엔시티가 정의되어 있는 것을 볼 수 있습니다.
[6주차 1차시 28:01] 그 다음 두 번째로 어노테이션 기반의 맵핑 같은 경우에는
[6주차 1차시 28:05] 맵핑 내용이 Java 소스 코드에 포함되는 경우입니다.
[6주차 1차시 28:11] 이 경우는 인터페이스에 정의한 각 메서드들마다
[6주차 1차시 28:16] 쿼리를 어노테이션을 통해 간단하게 맵핑을 할 수가 있는데
[6주차 1차시 28:19] 그래서 셀렉트, 어노테이션, 인서트, 업데이트, 딜리트 다 이런 식으로 맵핑을 할 수가 있는데
[6주차 1차시 28:29] 간단한 만큼 다양한 상황에 대처하기란 좀 어렵습니다.
[6주차 1차시 28:36] 그래서 간단하고 작은 프로젝트에 적합한 방식이다 라고 보시면 되겠습니다.
[6주차 1차시 28:44] 다음은 매퍼 파일에서 사용할 수 있는 동적 SQL 사용 예시입니다.
[6주차 1차시 28:50] SQL 조건 지정 부분을 동적으로 변화하고 싶을 때 사용하는 where 태그는 다양한 조합의 쿼리문을 사용할 수 있도록 해줍니다.
[6주차 1차시 29:00] if 태그를 통해 특정 조건이 만족될 때만 해당 조건을 덧붙일 수 있고 각 요소들이 늘어나면 그 사이에는 자동으로 end 키워드가 삽입됩니다.
[6주차 1차시 29:15] 그럼 MyBatis의 장단점을 한번 정리해 보도록 하겠습니다.
[6주차 1차시 29:21] MyBatis는 ORM과 달리 SQL을 직접 작성해 주기 때문에
[6주차 1차시 29:25] 복잡한 커리 사용이나 성능을 최적화하기에 유리합니다.
[6주차 1차시 29:31] 어노테이션을 잘 활용한다면 ORM보다 간단하게 설정할 수도 있으며
[6주차 1차시 29:36] DB 작업 과정에 어떻게든 개발자가 개입할 수 있도록 하였다는 점이 큰 장점입니다.
[6주차 1차시 29:43] 반면에 단점을 보자면 오히려 직접 SQL을 작성할 수 있다 보니
[6주차 1차시 29:48] 비슷한 쿼리들이 많이 만들어질 수 있다는 점입니다.
[6주차 1차시 29:53] 이런 상태에서 그 쿼리에 관련되는 변경사항이 발생한다면
[6주차 1차시 29:57] 이를 일일이 찾아 확인해가며 맞춰져야 하는 문제가 발생할 수 있습니다.
[6주차 1차시 30:05] 마이바티스는 ORM만큼 자동으로 객체 관계가 맵핑되지는 않으며
[6주차 1차시 30:10] 기능들을 문제없이 제대로 다루려면
[6주차 1차시 30:13] 이에 대해 철저히 학습해 두는 것이 필요합니다.
[6주차 1차시 30:20] 그러면 다음 주제로 넘어가서 MyBatis를 포함한 ORM 프레임워크를 사용할 때 어떤 보안 이슈가 발생할 수 있는지 알아보도록 하겠습니다.
[6주차 1차시 30:35] 앞서 학습했던 것과 같이 ORM 프레임워크는 객체와 관계형 데이터베이스를 자동으로 랩핑하여 개발 생산성을 높여주는 장점이 있습니다.
[6주차 1차시 30:45] 그리고 직접 SQL 문장을 작성하지 않기 때문에 기본적인 DB 공격을 방어할 수 있다고도 얘기했습니다.
[6주차 1차시 30:54] 하지만 설정을 잘못하거나 사용 방식이 잘못된 경우 치약점이 발생할 수도 있습니다.
[6주차 1차시 31:03] SQL 인젝션으로 대표되는 데이터베이스에 대한 공격은 ORM이 자동으로 SQL을 생성해주는 방식을 사용할 때 근본적으로 방어됩니다.
[6주차 1차시 31:14] 하지만 예외적인 방법을 사용해서 스트링 형태의 커리문을 조합해서 사용한다면 시약점이 결국 다시 만들어지게 되는데요.
[6주차 1차시 31:26] 특히 사용자가 입력한 내용을 커리에 직접 반영하는 경우 시약점이 발생하기 때문에 꼭 별도로 입력 내용을 검증하도록 개발하거나 ORM 동적 SQL 태그 및 파라미터 바인딩을 적용해야 합니다.
[6주차 1차시 31:44] 앞서 ORM에서 성능을 향상시키기 위해 지연 로딩과 캐싱 방식을 사용한다고 했었는데요.
[6주차 1차시 31:52] 그런데 이로 인한 취약점이 또 발생할 수가 있습니다.
[6주차 1차시 31:57] 메모리에서 처리하는 캐시는 그래도 괜찮은 편이지만,
[6주차 1차시 32:00] 파일 형태로 캐시하는 경우라면 해당 파일을 찾아내어 유출시킬 경우
[6주차 1차시 32:06] 민감한 내용이 그대로 노출될 수 있습니다.
[6주차 1차시 32:10] 심지어 이 캐시 파일을 마음대로 변조할 수 있다면
[6주차 1차시 32:13] 서비스 결과물과 데이터베이스까지 영향을 미칠 수 있는데요.
[6주차 1차시 32:18] 사용하고 있는 ORM 버전이 캐시의 무결성을 검사하면서 동작한다면 문제가 없겠지만, 그렇지 않다면 캐시 변조 공격에 취약한 상태이므로 캐시 파일이 저장되는 영역을 철저하게 보안 관리해야 합니다.
[6주차 1차시 32:38] 맵핑을 잘못 설정하게 되면 외부에 민감한 정보가 유출될 수 있고, 복잡한 맵핑을 잘못 설정하게 되면 계속 꼬리를 물어가는 루트가 발생하여 서비스가 멈추거나 과도한 부하가 발생할 수 있습니다.
[6주차 1차시 32:55] 자동으로 처리되는 것이 편리하다는 장점도 있지만 어떤 것들이 맵핑되어 전달되는지 관심을 갖지 않게 되므로 중요한 정보가 외부로 노출되고 있는 경우에도 전혀 모르는 상황이 발생할 수도 있습니다.
[6주차 1차시 33:12] 이 중 대량 할당 취약점 부분의 경우는 특히 주의해야 할 부분인데요.
[6주차 1차시 33:17] 예를 들어 설명해 보도록 하겠습니다.
[6주차 1차시 33:21] 사용자가 자신의 계정 정보를 수정하는 기능을 구현한다고 할 때
[6주차 1차시 33:24] 수많은 정보들의 각 항목마다 검증하도록 처리하는 것은 개발하기 번거로울 수 있습니다.
[6주차 1차시 33:32] 그래서 변경할 것들을 클라이언트에서 JSON으로 넣어 보내면
[6주차 1차시 33:37] 서버가 이 값을 도착 맵핑되어 있는 객체에 넣어서 자동으로 반영되게 구현할 수도 있을 겁니다.
[6주차 1차시 33:46] 이 경우 검증되어 있는 클라이언트만 생각해보면 일단 보이는 문제가 없습니다.
[6주차 1차시 33:53] 하지만 만약 그 객체 필드 중 isAdmin이라는 관리자 여부를 판단하는 필드가 만약에 존재를 하고
[6주차 1차시 34:00] 이것이 외부에 알려지게 된다면 어떻게 될까요?
[6주차 1차시 34:05] 개인정보를 수정하기 위한 API 호출을 흉내내거나
[6주차 1차시 34:09] Buffs 같은 노구로 중간에 끼어들어서
[6주차 1차시 34:12] JSON 내용의 isAdmin 값을 true로 지정하도록 하여 보낸다면
[6주차 1차시 34:17] 자신의 계정에 관리자 권한을 부여할 수도 있을 겁니다.
[6주차 1차시 34:22] 이를 방지하는 방법은 따로 있는 것이 아니고요.
[6주차 1차시 34:27] 민간 필드가 노출되거나 수정 가능하지 않도록 명시적으로 제외시키거나
[6주차 1차시 34:31] 읽기 전용으로 설정하는 것 등의 방법이 필요합니다.
[6주차 1차시 34:37] 그리고 외부로부터 입력 값은 반드시 검증하는 것이 항상 기본이며
[6주차 1차시 34:42] 맵핑된 객체를 통신 용도로 재사용하지 말고
[6주차 1차시 34:46] 반드시 별도의 통신용 객체, 즉 데인터 트랜스퍼 오브젝트를 활용하여
[6주차 1차시 34:57] 아무 필드에나 마음대로 접근하는 것을 막아야 합니다.
[6주차 1차시 35:05] 이번 차시 내용 요약해 보도록 하겠습니다.
[6주차 1차시 35:12] ORM은 객체와 관계형 데이터베이스 간의 맵핑을 자동화하여 개발 생산성을 높인다.
[6주차 1차시 35:19] 그래서 SQL문을 직접 작성하지 않아도 CRUD, 기본 동작 및 복잡한 쿼리를 수행할 수 있다.
[6주차 1차시 35:28] SQL 인젝션 방어 기능이 있지만 설정을 잘못하게 되면 보안 취약점이 발생할 수도 있기 때문에
[6주차 1차시 35:35] 보안 취약점이 발생할 수도 있다.
[6주차 1차시 35:42] 그리고 마이바티스는 SQL을 직접 작성할 수도 있는 ORM 프레임워크이므로 복잡한 쿼리 최적화에 유리한 면이 있다.
[6주차 1차시 35:57] 이러한 ORM 프레임워크를 사용할 때에는 반드시 보안과 성능 최적화를 고려하여 설계하는 것이 시큐어 코딩 관점에서 필수적이다.
[6주차 1차시 36:09] 이렇게 이번 차시에 배워봤고요.
[6주차 1차시 36:14] 참고문안이고, 이번 차시 수업 여기까지 하도록 하겠습니다.
[6주차 1차시 36:19] 감사합니다.

# [3-TRANSCRIPT] 6주차 2차시 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · 화이트리스트/Whitelist/최소 허용/허용 목록 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · MyBatis/마이바티스/Mapper/매퍼/#{}/${}/동적 SQL · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

[6주차 2차시 00:00] 안녕하세요. 6주차 2차시 강의 시작하도록 하겠습니다.
[6주차 2차시 00:09] 이번 차시에서 학습할 내용은 SQL 인젝션 진단 및 대응입니다.
[6주차 2차시 00:17] 이번 차시의 학습 목표입니다.
[6주차 2차시 00:22] SQL 인젝션 공격의 개념과 원리가 무엇인지 알아보고 여러가지 공격 기법들을 직접 학습해 보겠습니다.
[6주차 2차시 00:32] 또한 이를 방어하기 위한 대응 방법까지 함께 살펴보도록 하겠습니다.
[6주차 2차시 00:40] 이에 따른 학습 내용은 앞서 말씀드린 학습 목표와 동일합니다.
[6주차 2차시 00:47] 본격적으로 SQL 인젝션의 개념과 발생 원리부터 함께 알아보도록 하겠습니다.
[6주차 2차시 00:57] SQL 인젝션이 뭔지 보면 왜 모든 데이터베이스 기반 애플리케이션이 이 공격에 노출될 수밖에 없는지 한번 살펴보도록 하겠습니다.
[6주차 2차시 01:10] SQL 인젝션이라는 용어는 이미 잘 알고 있는 분들도 계실텐데요.
[6주차 2차시 01:18] 먼저 인젝션이라는 단어 자체가 어떤 것을 주입한다는 뜻을 가지고 있죠.
[6주차 2차시 01:25] 즉 SQL 인젝션이란 애플리케이션이 데이터베이스로 보내는 정상적인 쿼리문 안에
[6주차 2차시 01:32] 악의적인 SQL 코드를 끼워 넣어 개발자가 의도하지 않은 명령을 실행하도록 만드는 공격 기법입니다.
[6주차 2차시 01:41] 대부분의 RDBMS는 관계형 데이터베이스는
[6주차 2차시 01:48] 클라이언트로부터 문자열 형태의 SQL 쿼리문을 받아 파싱한 후에 실행을 하는데
[6주차 2차시 01:55] 만약에 특정 웹 애플리케이션에서 SQL 문자열을 만들 때
[6주차 2차시 02:01] 사용자 입력값도 함께 조합하여 사용한다는 것을
[6주차 2차시 02:05] 해커가 알게 되었다면
[6주차 2차시 02:06] 해당 입력값에 악의적인 SQL 퀄리를 주입시켜 매우 악의적인 동작을 하도록 변조시켜 버릴 수가 있습니다.
[6주차 2차시 02:16] 현재 거의 모든 데이터베이스에서 SQL 쿼리 형태를 지원하고 있으므로 데이터베이스를 사용하는 웹뿐 아니라 모바일, 데스크톱 애플리케이션까지 광범위하게 인젝션 위험에 노출되어 있다고 말할 수 있을 겁니다.
[6주차 2차시 02:32] 그리고 이러한 공격 기법의 특성상 사용자 입력을 기반으로 운영되는 포털이나 쇼핑몰 같은 서비스에서 많은 피해 사례가 발생하고 있는데요.
[6주차 2차시 02:45] 공격자가 성공적으로 커리를 조작하면 단순히 데이터 조회를 넘어서 다음과 같은 심각한 피해가 발생할 수 있습니다.
[6주차 2차시 02:54] 금융거래 내역이나 의료기록 등에 민감한 고객 개인 정보가 외부로 흘러나갑니다.
[6주차 2차시 03:01] 그리고 인서트, 업데이트, 딜리트 같은 데이터 조작어를 삽입해서 데이터베이스 내용을 마음대로 조작하거나 삭제할 수 있습니다.
[6주차 2차시 03:11] 심지어 DBA 권한으로 시스템 테이블에 접근해 운영체제 명령어나 외부 프로그램을 호출하는 프로세저를 실행할 수도 있죠.
[6주차 2차시 03:21] 아울러 무한 루프나 대량 쿼리를 주입해서 데이터베이스 자원을 고갈시키는 도스 공격도 가능합니다.
[6주차 2차시 03:31] 실제로 국내외 대형 포털 쇼핑몰 금융관에서 SQL 인젝션 취약점을 통해 수십만 건의 개인정보가 유출되거나 핵심 서비스가 마비된 사례가 다수 보고되고 있습니다.
[6주차 2차시 03:47] 정리하자면 SQL 인젝션은 사용자 입력을 통해
[6주차 2차시 03:52] 애플리케이션이 생성하는 쿼리 구조 자체를 변조하는 공격으로
[6주차 2차시 03:56] 그 결과 불법 데이터 접근 및 시스템 명령 실행까지 가능하게 만드는 매우 위험한 취약점입니다.
[6주차 2차시 04:07] SQL인젝션 공격의 흐름을 그림으로 한번 살펴보도록 하겠습니다.
[6주차 2차시 04:14] 여기에서 로그인 창을 뚫고 들어가는 상황을 보여주고 있는 그림인데요.
[6주차 2차시 04:20] 이 서비스의 로그인 과정은 입력한 사용자 아이디와 암호를 데이터베이스로 조회해서 결과가 성공이라면 해당 아이디로 로그인을 시켜주고 조회를 실패하면 로그인을 거부하는 방식으로 구현되어 있었습니다.
[6주차 2차시 04:38] 이 경우 공격자는 입력창에 일부러 따옴표와 마이너스 마이너스 즉 주성문을 표기하는 기호 등을 섞어서 악의적인 쿼리문을 입력을 하는데요.
[6주차 2차시 04:51] 원래 웹 애플리케이션은 입력한 값 뒤에 앞뒤로 따옴표를 붙여주면서 쿼리문을 조합을 합니다.
[6주차 2차시 05:01] 그런데 사용자 입력 값에 따옴표가 들어있다면 문장 해석이 전혀 다르게 바뀌어 버리죠.
[6주차 2차시 05:08] 애플리케이션이 자동으로 붙여주는 앞 따옴표와
[6주차 2차시 05:11] 공격자가 입력상에 넣은 따옴표가 뒷 따옴표로 해석이 되면서
[6주차 2차시 05:16] 이후 입력값은 순수한 SQL 문장으로 해석되는 상황이 되는 겁니다.
[6주차 2차시 05:22] 그렇다면 여기에 5월 1은 1와 같은 내용을 붙여준다면 어떻게 될까요?
[6주차 2차시 05:30] 1은 1 이것은 뭘 얘기하는 거냐면
[6주차 2차시 05:37] 이런 식으로 or, 1은 1 이런 거를 붙여 준다는 거죠
[6주차 2차시 05:44] 그래서 1이랑 1이랑 같냐 이것은 당연히 참이고
[6주차 2차시 05:48] or라는 논리 연산자는 또는 이잖아요
[6주차 2차시 05:52] 그래서 어느 쪽이 참이기만 하면
[6주차 2차시 05:55] 결과가 참으로 나오기 때문에
[6주차 2차시 05:57] 퀄리 앞부분에서 아이디랑 비밀번호가 일치하지 않더라도
[6주차 2차시 06:02] 최종 결과가 성공으로 되고
[6주차 2차시 06:04] 결국 아이디와 암호가 확인되었다고
[6주차 2차시 06:07] 잘못 이해한 애플리케이션은 공격자에게 로그인 권한을 내어주게 될 겁니다.
[6주차 2차시 06:14] 마이너스 마이너스를 뒤에 붙여주는 이유는
[6주차 2차시 06:16] 사용자 입력 뒷부분에 붙는 쿼리문들을 모두 무시하기 위해서입니다.
[6주차 2차시 06:25] SQL 인젝션이 그럼 왜 발생하는지 그 근본 원인을 자세히 한번 살펴보겠습니다.
[6주차 2차시 06:32] SQL 인젝션 공격의 출발점은 악의적인 쿼리문을 주입하는 첫 단계입니다.
[6주차 2차시 06:38] 가장 큰 이유는 동적 쿼리를 만들 때 사용자 입력을 검증 없이 그대로 조합하기 때문입니다.
[6주차 2차시 06:45] 사용자 입력에 따라 바뀔 수 있는 동적 커리를 사용해 구현했다면, 사용자가 입력한 내용이 커리 문장에 영향을 미치지 않는지 반드시 검증을 해야 하죠.
[6주차 2차시 06:58] 웹, 웹이랑 URL 파라미터, API 요청 바디 등 모든 웹 입력에는 작은 따옴표, 세미콜론, 대시 같은 특수 문자가 포함될 수가 있는데,
[6주차 2차시 07:11] 이를 필터링하거나 escape하지 않으면 원래 의도한 SQL 구조가 깨지고 맙니다.
[6주차 2차시 07:18] 나와있는 예시 쿼리문처럼 유저 인풋자리에 admin.or.71을 넣어주면
[6주차 2차시 07:26] 조건문을 항상 참으로 만들어서 비밀번호 검증 단계 자체를 오해해버리죠.
[6주차 2차시 07:36] 공격자는 이러한 취약점을 발견하면 간단한 문자열 3인만으로 데이터베이스의 민감 정보는 물론 시스템 전체에게도 명령을 내릴 수가 있습니다.
[6주차 2차시 07:49] SQL 인젝션은 모든 종류의 관계형 데이터베이스에서 RDB에서 동일한 방식으로 동작하기 때문에
[6주차 2차시 07:57] 어느 환경에서든 외부 입력 검증 로직이 빠져 있다면 언제든 공격에 노출될 위험이 있습니다.
[6주차 2차시 08:10] 따라서 동적 커리를 사용할 때는 반드시 입력 값의 길이와 형식을 체크하고
[6주차 2차시 08:17] 작은 다운표나 세미콜론을 허용하지 않도록 필터링하거나
[6주차 2차시 08:21] 더 좋은 방법으로는 Prepared Statement로
[6주차 2차시 08:25] 사용자 입력 값을 쿼리와 애초에 완전히 분리해주는 것이 필요합니다.
[6주차 2차시 08:32] 이렇게만 해도 SQL 인젝션의 90% 이상은 방어를 할 수가 있습니다.
[6주차 2차시 08:43] 이번에는 에러 메시지가 얼마나 위험한 정보 노출 통로가 될 수 있는지 살펴보겠습니다.
[6주차 2차시 08:54] 공격자는 인젝션을 통해 쿼리문을 변조하여 의도적으로 에러를 만들어 보기도 하는데요.
[6주차 2차시 09:01] 보통 애플리케이션은 예외가 발생하면 내부에서 어떤 일이 일어났는지 로그로 남기거나
[6주차 2차시 09:07] 클라이언트에게 간단한 오류 화면을 보여주는데
[6주차 2차시 09:10] 그런데 만약 이 과정에서 데이터베이스 내부 구조를 알려주는 메시지가 그대로 노출된다면
[6주차 2차시 09:18] 공격자는 이 오류 메시지를 마치 단서처럼 활용해서 추가 취약점을 찾을 수 있습니다.
[6주차 2차시 09:26] 예시에 나와 있는 것처럼 사용자 입력값 유저 인풋에 db 언더바 네임 함수 호출 내용을 주입하면
[6주차 2차시 09:33] SQL 서버는 데이터베이스 이름을 포함한 오류를 되돌려줄 수가 있습니다.
[6주차 2차시 09:38] 이 한 번의 시도로 데이터베이스 이름을 알아냈다면 공격자는 그 다음에는 테이블 목록 조회 퀄이나 버전에 따른 알려진 취약점 탐색으로 이어갈 수가 있습니다.
[6주차 2차시 09:51] 이럴 때 에러 메시지는 시스템 내부 구조를 해커에게 고스란히 노출하는 열린 창문과 같은 셈이 되는데요.
[6주차 2차시 10:00] 따라서 운영 환경에서는 에러 메시지를 외부에 절대 노출하지 말고 단순히 서버 내부 오류가 발생했습니다.
[6주차 2차시 10:09] 같은 일반화된 문구만 제공을 해야 합니다.
[6주차 2차시 10:11] 물론 내부에선 반드시 상세 정보를 안전한 로그만 남겨두어 감사나 디버깅 목적으로 활용하면서도 공격에 악용되지 않도록 해야 합니다.
[6주차 2차시 10:26] 그리고 과도한 DB 권한으로 인해 SQL 인젝션 취약점이 단순한 데이터 유출을 넘어 더 큰 재난으로 확대될 수 있다는 것을 한번 얘기해 보겠습니다.
[6주차 2차시 10:39] 애플리케이션이 데이터베이스와 통신할 때 사용하는 계정이 셀렉트 권한만 있다면 최악의 경우라도 데이터 읽기 수준에서 피해가 끝나겠지만
[6주차 2차시 10:49] 만약 이 계정에 insert, update, delete는 물론 drop이나 alter, 심지어 저장 프로시저 실행 권한까지 부여되어 있다면 이야기가 달라집니다.
[6주차 2차시 11:04] 공격자는 SQL 인젝션을 통한 쿼리 삽입만으로 테이블을 통째로 삭제하거나 변경할 수 있고 저장 프로시저를 악용해 운영체제 명령어를 실행하는 것까지 가능해집니다.
[6주차 2차시 11:18] 이 과정에서 단순 정보 노출이 아니라 시스템 자체를 파괴하거나 악성 코드를 설치해 추가 공격의 교두보를 마련할 수도 있는 거죠.
[6주차 2차시 11:28] 따라서 최소 권한 원칙을 적용해 애플리케이션 전용 계정에는 오직 필요한 CRUD 권한만 부여하고 그 외의 권한은 모두 제거해야 합니다.
[6주차 2차시 11:45] 읽기 전용 기능에서 반드시 셀렉트 전용 계정을 쓰기 기능에는 인서트, 업데이트, 딜리트만 허용된 계정을 사용을 하고
[6주차 2차시 11:55] 테이블 생성 및 변경이 가능한 DDL 명령이나 권한을 부여하는 DCL 명령에 대한 권한은 절대 주지 않아야 합니다.
[6주차 2차시 12:06] 또한 저장 프로세저 권한은 별도의 안전한 계정으로 분리하고, 운영 중에는 위험한 확장 프로세저들을 아예 비활성화해 두는 것이 좋습니다.
[6주차 2차시 12:16] 이렇게 개정별 권한을 세분화 및 정리하면 설령 SQL 인젝션이 성공하더라도 피해 범위를 데이터 조회로 국한시켜 더 큰 재앙을 막을 수 있습니다.
[6주차 2차시 12:34] 그럼 SQL 인젝션 공격에서 사용하는 커리 조작 방법에 대해 자세히 알아보도록 하겠습니다.
[6주차 2차시 12:46] 관련 코드를 보면 웹페이지 HTML에서 입력된 ID와 패스워드 값이 애플리케이션의 서버로 도달하면서
[6주차 2차시 12:56] 여기서 보면 id와 패스워드, 아무런 검증 없이 SQL이라는 변수의 문자열 조합에 곧장 사용하는 것을 볼 수 있습니다.
[6주차 2차시 13:16] 보시면 이 SQL 변수에 이 아이디랑 패스워드를 그냥 문자열처럼 더해서 지금 만들어서 대입하고 있죠.
[6주차 2차시 13:31] 아래 입력 예시들을 한번 살펴보면
[6주차 2차시 13:34] 갭 방식 호출로 어떻게 아이디 값과 패스워드 값을 넣으면 로그인 검사를 무력화시키는지 알 수 있습니다.
[6주차 2차시 13:43] ID와 패스워드를 비교하는 로직 사이에는 원래 A&D 논리 연산자가 있는데
[6주차 2차시 13:48] 그 앞뒤를 무조건 True 값이 나오도록 Or를 사용한 커리문을 주입하면
[6주차 2차시 13:54] 전체 해석이 무조건 true가 나오도록 고정시킬 수가 있습니다.
[6주차 2차시 14:01] 그 방식은 방금 설명한 것은
[6주차 2차시 14:06] 이거를 아이디랑 패스워드에 적절하게 넣으면 이렇게 할 수 있고
[6주차 2차시 14:15] 그것보다도 더 간단한 방법이 그 아래 있는데요.
[6주차 2차시 14:19] 마이너스 마이너스는 오라클 같은 데이터베이스에서 EU 내용을 주성문으로 취급하는 것이라서
[6주차 2차시 14:27] 이렇게 입력을 하는 순간 그 뒤 쿼리문이 모두 무력화됩니다.
[6주차 2차시 14:36] 그래서 관리자 계정 중 어드민이 있다면 트루가 되고
[6주차 2차시 14:39] 그 뒤 모든 내용들이 주석 처리되어 트루감만 남기 때문에 어드민 계정으로 로그인이 됩니다.
[6주차 2차시 14:49] 데이터베이스가 만약 MySQL 방식이라면 샵 기호를 주석 기호로 바꾸어 사용하면 같은 효과를 거두게 됩니다.
[6주차 2차시 15:02] 그 다음 오류 기반 SQL 인젝션은 애초에 쿼리 오류를 유도해 그 오류 메시지에 담긴 정보를 통해 데이터베이스 구조를 파악하는 공격 기법입니다.
[6주차 2차시 15:14] 이 방식을 이용하면 테이블명이나 컬럼명, 심지어 데이터베이스 엔진 버전까지 에러 메시지에서 확인을 할 수가 있죠.
[6주차 2차시 15:23] 첫 번째로 사용자 입력 값에 따옴표 한 개만 전달하면 퀄이 문법이 깨지며 예상치 못한 따옴표 오류가 발생을 합니다.
[6주차 2차시 15:32] 만약 애플리케이션이 이 오류를 별도 검증 없이 화면에 그대로 출력한다면 공격자는 이를 통해 SQL 인젝션이 가능함을 바로 파악할 수가 있습니다.
[6주차 2차시 15:45] 두 번째는 having71 구문을 추가해 그룹핑 오류를 일으키는 방법입니다.
[6주차 2차시 15:52] having절은 groupby와 함께 사용해야 하기 때문에 groupby가 필요하다는 오류 메시지가 발생하고
[6주차 2차시 15:58] 여기에서 테이블에
[6주차 2차시 16:00] 필드 정보를 유출할 수 있습니다.
[6주차 2차시 16:03] 세번째 기법은
[6주차 2차시 16:04] 데이터베이스
[6주차 2차시 16:06] 이름을 강제로 숫자와
[6주차 2차시 16:08] 비교하는 것입니다.
[6주차 2차시 16:14] 여기서 영문 기반의
[6주차 2차시 16:16] 데이터베이스 이름이 숫자와 비교될 수
[6주차 2차시 16:18] 없어서 변환불가 오류가 발생하며 이 메시지에서 데이터베이스 이름이 드러나는 경우가 있습니다.
[6주차 2차시 16:26] 마지막 예시구문을 사용하면 SQL 서버의 엔진 종류와 빌드 정보를 오류 메시지로 얻어낼 수 있습니다.
[6주차 2차시 16:44] 이 정보가 있으면 알려진 취약점에 대한 공격도 손쉽게 설계할 수 있죠.
[6주차 2차시 16:52] 이처럼 오류 기반 SQL 인젝션은 의도적으로 다양한 오류를 유발해서 그 속에 숨겨진 데이터베이스 내부 정보를 빠르게 수집하여 더 정교한 공격으로 이어지는 발판을 마련합니다.
[6주차 2차시 17:11] 이번에는 유니온 기반 SQL 인젝션에 대해 알아보겠습니다.
[6주차 2차시 17:16] 이 공격은 단순한 인증 검사를 우회하는 수준을 넘어서 DB 내부 정보 유출을 목적으로 하고 있습니다.
[6주차 2차시 17:24] 유니온은 이쪽 조건의 결과값과 다른 쪽의 결과값을 합집합으로 결합하여 결과를 만드는 기능인데
[6주차 2차시 17:34] 이를 악용하면 본격적으로 데이터베이스의 구조를 추적하고 값을 유출할 수 있습니다.
[6주차 2차시 17:41] 첫 번째 예시의 경우
[6주차 2차시 17:43] 어드민 따옴표 유니온 셀렉트 123456
[6주차 2차시 17:48] 유니온 뒷부분 셀렉트 부문은 테이블을 지정하지 않고
[6주차 2차시 17:53] 그냥 숫자로 1, 2, 3 등의 값을 결과값으로 보여주는 역할을 하기 때문에
[6주차 2차시 17:58] 해당 웹페이지에서 이 숫자들이 나타나는 곳이 있다면
[6주차 2차시 18:03] 바로 이곳을 정보를 유출하는 창고로 사용할 수 있다는 뜻이 됩니다.
[6주차 2차시 18:09] 그 다음부터는 해당 컬럼 위치에 얻어내고 싶은 내용을 넣으면 되는 것이죠.
[6주차 2차시 18:15] 그걸 활용한 것이 바로 두 번째 예시입니다.
[6주차 2차시 18:19] 첫 번째 예시를 입력해 봤더니 결과 화면에 어디인가 1이 보였다는 겁니다.
[6주차 2차시 18:25] 그래서 첫 번째와 동일한 유니온 셀렉트 구문에 버전을 얻는 함수를 넣어보면 결과 화면 그 위에 버전이 표시가 될 겁니다.
[6주차 2차시 18:37] 이 앞서 봤던 거에서 1자리에 버전을 넣는 거죠.
[6주차 2차시 18:42] 그럼 그 다음으로는 확대 공격을 하는 것이 세 번째 예시인데요.
[6주차 2차시 18:49] 이번에는 MySQL 데이터베이스 정보가 들어있는
[6주차 2차시 18:53] 인포메이션 스키마에 스키마 테이블을 유니온시켜서
[6주차 2차시 18:58] 존재하는 DB 목록을 알아낼 수 있습니다.
[6주차 2차시 19:03] 그럼 그 중에 타겟을 삼고 싶은 DB 이름을 찾아볼 수 있을 겁니다.
[6주차 2차시 19:09] 그런데 목록을 보니 특별한 다른 DB는 없는 것 같고 기본적으로 연결되어 있는 DB 내용을 찾아보겠다고 판단했으면 네 번째 구문을 통해서 더 깊게 들어가 볼 수 있습니다.
[6주차 2차시 19:26] 현재 DB 이름은 데이터베이스라는 함수 호출로 얻을 수 있으니까 웨어절에서 활용을 했고요.
[6주차 2차시 19:33] 이 공격은 스키마 테이블 목록에서 현재 DB에 해당하는 테이블 이름들을 모두 가져와
[6주차 2차시 19:40] 그룹 CONCAT 함수를 통해 하나의 문자열로 합쳐서 볼 수 있게 해줍니다.
[6주차 2차시 19:46] 테이블 목록이 콤마로 구분되어 화면에 한 번에 나타나게 될 것입니다.
[6주차 2차시 19:52] 그럼 그 다음에는 그 테이블들 중 하나를 선택해 볼 수 있을 텐데
[6주차 2차시 19:57] 여기에서는 다섯 번째 예시에서 보드 멤버 테이블을 선택을 했습니다.
[6주차 2차시 20:03] 이 사진이라는 뜻이죠
[6주차 2차시 20:08] 비슷한 방식으로 컬럼 이름, 목록을 얻어냅니다.
[6주차 2차시 20:11] 이렇게 하면 테이블명과 컬럼명까지 알아냈으니까 직접 그 테이블로부터 값을 가져와 보기만 하면 됩니다.
[6주차 2차시 20:20] 마지막 예시에서 원하는 컬럼들을 지정하여 내용을 유출할 수 있습니다.
[6주차 2차시 20:31] 공격자들이 데이터베이스 내부 구조를 활용해서 공격하려면
[6주차 2차시 20:37] 이런 데이터베이스 시스템 테이블의 도조와 의미를 이해하고 있어야 합니다.
[6주차 2차시 20:44] 데이터베이스가 동작하는 동안 사용하는 스테이블이므로
[6주차 2차시 20:47] 접근하지 못하도록 막는 것도 사실 어렵습니다.
[6주차 2차시 20:52] 실제로 상당히 많은 애플리케이션들이 이런 시스템 테이블의 내용도 활용하여 동작하기 때문에 더더욱 그렇습니다.
[6주차 2차시 21:00] 그런 영향이 전혀 없는 환경이라면 일반 사용자 계정은 내용을 조회하지 못하도록 권한 조정을 해두는 것이 바람직합니다.
[6주차 2차시 21:13] Blind SQL Injection은 오류 메시지 없이도 쿼리 결과의 유무나 응답 시간을 관찰해 데이터베이스 내부 정보를 하나씩 꺼내오는 기법입니다.
[6주차 2차시 21:27] 예시에서는 SQL 서버의 username 함수를 사용해 사용자 이름을 알아내는 과정을 보여주는데요.
[6주차 2차시 21:44] 먼저 아이디가 데이터인 계정이 존재한다는 것을 오류 기반 인젝션으로 확인했다고 가정합니다.
[6주차 2차시 21:51] 화면의 값이 직접 노출되지 않은 상태에서 첫 번째 예시처럼 주입해 첫 글자가 A일 때와 아닐 때의 페이지 응답 차이를 보고 판단하는 것입니다.
[6주차 2차시 22:03] 첫 글자가 참이면 정상 페이지로 뜨고 거짓이나 에러면 실패 페이지로 넘어가죠. 이 방식을 반복해 두 번째 글자 세 번째 글자를 순서대로 확인하면서
[6주차 2차시 22:15] 전체 이름을 유추하게 되는데 컨텐츠 기반 공격이라고 부릅니다.
[6주차 2차시 22:22] 반면 타임 기반 공격은 Wait for Delay 구문을 주입해서 응답 지연 시간 여부를 보면서 같은 원리로 정보를 수집합니다.
[6주차 2차시 22:36] 자동화 툴을 활용하면 이 과정을 반복적으로 수행하여 한 글자씩 빠르게 꺼내올 수 있으므로 방어하기가 더 어렵습니다.
[6주차 2차시 22:45] 그럼 실제 보안사고 사례를 한번 보도록 하겠습니다.
[6주차 2차시 22:53] 여기 어때는 워드이노베이션이라는 회사가 운영하는 매우 유명한 숙박중개 사이트죠.
[6주차 2차시 22:59] 당시 약 5천 명 정도의 회원들에게 협박성 음란문자가 발송되어 이 원인을 조사하는 과정에서 개인정보 유출 사실이 확인되었습니다.
[6주차 2차시 23:12] 약 97만 명의 회원 정보가 유출되었는데 그 시작점이 SQL 인젝션입니다.
[6주차 2차시 23:18] 데이터베이스 안에 저장되어 있던 관리자 세션 아이디 값을 확득하고
[6주차 2차시 23:22] 이를 악용해 서비스 관리자 웹페이지를 우회 접속한 뒤 정보를 빼낸 것입니다.
[6주차 2차시 23:30] 당시 웹 애플리케이션은 입력과 검증 로직이 없었던 것으로 파악됩니다.
[6주차 2차시 23:36] 한국직업능력 교육원은 2024년 8월 SQL 인젝션으로 추정되는 공격을 통해 회원정보 약 160만 건이 유출되었다고 합니다.
[6주차 2차시 23:51] 사례에서 보듯이 SQL 인젝션 공격은 끊임없이 보안사고의 원인으로 지목되고 있는 공격입니다.
[6주차 2차시 24:02] 그럼 이제부터 어떻게 SQL 인젝션 취약점을 찾아내고 대응해야 하는지 알아보도록 하겠습니다.
[6주차 2차시 24:14] SQL 인젝션의 취약점을 진단하는 가장 기본적인 방법은 소스 코드를 검사해보는 겁니다.
[6주차 2차시 24:22] 코드 리뷰라는 용어의 개념부터 잡아볼텐데요.
[6주차 2차시 24:25] 코드 리뷰라는 것은 개발자가 작성한 소스 코드를 체계적으로 검토해서 버그와 보안 취약점을 찾아내는 과정을 말합니다.
[6주차 2차시 24:36] 특히 SQL 인젝션 취약점은 개발 단계부터 동쪽 허리문을 조합할 때 사용자 입력값을 제대로 검증하지 않아 발생하는 경우가 가장 많습니다.
[6주차 2차시 24:48] 데이터베이스 접근 권한이 최소화되어 있었다면 심각한 피해를 막을 수 있었겠지만 그렇더라도 에러를 유발시켜 시스템 정보들을 획득하여 다른 공격 단서로 활용될 수 있기 때문에
[6주차 2차시 25:01] 근본적으로는 입력감 검증 및 정제가 매우 중요하다고 말할 수 있습니다.
[6주차 2차시 25:07] 그리고 코드리뷰가 중요한 이유는 자동화된 검사 도구만으로는 놓칠 수 있는 세부 로직과 예외 처리를 사람이 직접 살펴볼 수 있기 때문입니다.
[6주차 2차시 25:20] 이러한 코드리뷰 문화가 정착이 된다면 다양한 취약점에 대응할 수 있도록 개발자 간 노하우가 공유되어 전체적인 보안 수준을 올릴 수 있습니다.
[6주차 2차시 25:31] 코드를 리뷰할 때에는 우선 동적 SQL을 사용하는 부분을 점검해야 합니다.
[6주차 2차시 25:41] 예시 코드의 findUserByUserName 이라는 함수를 보면
[6주차 2차시 25:46] 인수로 받은 유저네임 함수를 살펴보면
[6주차 2차시 25:54] 인수로 받은 유저네임을 별다른 검증 없이 커리 문자를 조합할 때 곧바로 사용을 하고 있는데요.
[6주차 2차시 26:01] 이것은 SQL 인젝션 공격에 노출된 전형적인 코드 패턴입니다.
[6주차 2차시 26:09] 화이트리스트 기반으로 입력값을 검증해서 문자열, 길이, 특수문자나 인코딩 등의 입력 패턴에 적절히 대처하는 코드가 존재하는지
[6주차 2차시 26:19] 뭐 Prepared Statement와 같은 바인딩 방식으로 개발을 해서
[6주차 2차시 26:25] 그런 바인딩 방식으로 해서 입력 값이 커리문에 영향을 주지 못하도록
[6주차 2차시 26:33] 대응하였는지 확인해 봐야 합니다.
[6주차 2차시 26:40] 아무리 그래도 코드 리뷰라는 것 자체가
[6주차 2차시 26:43] 사람이 하는 작업이기 때문에 실수가 발생할 수 있습니다.
[6주차 2차시 26:49] 실수로 찾지 못한 취약점, 로직이 복잡하여 발견하지 못한 취약점들을 찾아내거나 대규모 프로젝트 복잡한 형태의 코드를 다루고 있다면 반드시 자동화 진단 도구를 도입해야 합니다.
[6주차 2차시 27:04] 우선 정적 분석 도구라는 것은 소스코드를 스캔해서 잠재된 취약점을 탐지하는 것으로
[6주차 2차시 27:11] 소나, 큐브, 체크막, 맑스, 포티파이 등의 제품이 알려져 있는데
[6주차 2차시 27:21] SQL 인젝션, 크로스 사이트 스크립트, 하드 코딩된 비밀번호 등의 취약점들은 이 과정에서 대부분 찾아낼 수 있습니다.
[6주차 2차시 27:32] 반면 동적 분석 도구는요. 실제로 웹 애플리케이션이 동작하는 상태에서 공격 시나리오를 시도합니다.
[6주차 2차시 27:41] OWASP, JAP, Buffs, 그리고 이런 제품들이 알려져 있는데요.
[6주차 2차시 27:50] 스킬 인젝션, 크로스 사이트 스크립트, 페이로드 공격 과정을 자동으로 시도하여
[6주차 2차시 27:55] 웹 애플리케이션의 대응 상황을 확인해 볼 수 있습니다.
[6주차 2차시 28:06] 이러한 자동화 도구들을 CICD 파이프라인에 통합하면
[6주차 2차시 28:13] 빌드 단계에서 코드 품질과 보안 수준을 지속적으로 모니터링할 수 있습니다.
[6주차 2차시 28:20] 운영단계에 들어가기 전에 이슈를 미리 발견하여 수정할 수 있으므로 비용과 위험을 크게 줄일 수 있습니다.
[6주차 2차시 28:30] 그럼 SQL 인젝션 취약점을 어떻게 대응하면 좋을지 알아보겠습니다.
[6주차 2차시 28:40] 여기 제시되어 있는 취약한 코드를 보면 첫 줄 GET 파라미터를 통해 사용자 입력 값을 ID 변수로 받는데
[6주차 2차시 28:51] 두 번째 줄처럼 터리문 조합에 그대로 사용하게 되면 SQL 인젝션 공격에 노출됩니다.
[6주차 2차시 29:01] 원래 의도는 웨어절 다음 ID 값이 입력받은 문자열과 일치하는 데이터만 가져오라는 것이지만
[6주차 2차시 29:08] 사용자가 1, OR, 1은 1, 이런 식으로 주입을 하게 되면
[6주차 2차시 29:16] 아이디값이 1이거나 또는 1이랑 1이라는 숫자가 같으면과 같이 해석되는 바람에
[6주차 2차시 29:24] 조건부가 아니라 항상 참의되어 버려 모든 데이터를 가져오는 문장으로 바뀌게 되는 것입니다.
[6주차 2차시 29:31] 이를 방지하려면 파라미터 바인딩 방식을 적용해야 합니다.
[6주차 2차시 29:38] 파라미터 바인딩 방식은 prepared statement와 placeholder라고 부르는 물음표 기호를 사용해서 실제 파라미터를 쿼리문과 분리합니다.
[6주차 2차시 29:55] 물음표가 들어간 부분은 나중에 setString과 같은 함수를 써서 값을 별도로 바인딩하죠.
[6주차 2차시 30:02] 이 경우 파라미터에 바인딩되는 내용은 쿼리문장으로 섞어 해석하지 않기 때문에 원천적으로 사용자 입력에 따른 취약점을 제거할 수 있습니다.
[6주차 2차시 30:14] 또한 이런 방식 특성상 쿼리문을 미리 설정해 놓고 바인딩하는 값만 바꿔가며 반복 사용할 수 있게 되니까
[6주차 2차시 30:21] 비슷한 쿼리들을 반복적으로 파싱하고 실행 플랜을 수행하지 않아도 되어 성능이 매우 좋아집니다.
[6주차 2차시 30:34] 이번 페이지에서는 JDBC API 방식의 취약한 코드를
[6주차 2차시 30:39] 앞서 배운 파라미터 바이딩 방법을 통해 안전한 코드로 변환하는 것을 볼 수 있습니다.
[6주차 2차시 30:47] 물음표로 표시된 파라미터가 바이딩될 위치가 두 개 존재하는데
[6주차 2차시 30:52] 이런 식으로 지금 입력 값이 들어가서 쿼리문이 만들어지는 것을
[6주차 2차시 31:02] 이렇게 물음표로 둬서
[6주차 2차시 31:06] 바인딩될 위치가 두 개 존재하는 거죠.
[6주차 2차시 31:10] 맨 앞에서부터 첫 번째 위치, 두 번째 위치를 번호로 지정을 하면서
[6주차 2차시 31:15] 이렇게 setString을 가지고
[6주차 2차시 31:18] 첫 번째 위치, 그리고 두 번째 위치, 번호로 지정을 하면서 파인딩을 하고 있습니다.
[6주차 2차시 31:28] 물론 비밀번호 검증 로직에는 해시나 솔트를 사용하는 등
[6주차 2차시 31:31] 다른 보안 기법도 함께 적용되어야 하지만
[6주차 2차시 31:35] 적어도 SQL 인젝션 관점으로만 볼 때에는 안전한 대응 방법을 잘 적용했다고 볼 수 있습니다.
[6주차 2차시 31:45] 다음은 ORM 프레임워크인 Hibernate를 사용할 때도
[6주차 2차시 31:50] 문자열 조합으로 동쪽 커리를 만들면 SQL 인젝션 위험이 생깁니다.
[6주차 2차시 31:57] 이 부분에서 지금 SQL 인젝션 위험이 있는 거죠.
[6주차 2차시 32:04] 반드시 그래서 파라미터 바인딩 방식을 사용하여 SQL 인젝션 위험을 피해야 합니다.
[6주차 2차시 32:10] 여기에서는 물음표 기호 뒤에
[6주차 2차시 32:18] 이 부분입니다.
[6주차 2차시 32:22] 파라미터 간 겹치지 않는 숫자를 지정하여
[6주차 2차시 32:25] 세스트링에서 위치를 명확히 지정할 수 있도록 합니다.
[6주차 2차시 32:29] 최근 ORM 프레임워크에서는 이런 식으로 정확하게 위치 번호를 써서 지정하는 방식만 허용하는 추세입니다.
[6주차 2차시 32:41] 그 다음에 MyBatis 같은 경우에도 맵업 파일에서 SQL 구문을 작성할 때
[6주차 2차시 32:48] 파라미터 기법을 사용해야 합니다.
[6주차 2차시 32:52] 여기에서 주목해야 하는 것은
[6주차 2차시 32:53] 네임 값을
[6주차 2차시 32:55] 이렇게
[6주차 2차시 32:57] 달러 기호와 중괄호로 묶은 단순 시환 방식과
[6주차 2차시 33:02] 아래에 보면
[6주차 2차시 33:05] 샵 기호와 중괄호로 묶은 파라미터 바인딩 방식의 차이입니다.
[6주차 2차시 33:13] 단순 시환 방식을 사용하면 문자열을 조합하는 것과 동일하기 때문에
[6주차 2차시 33:18] SQL 인젝션 공격에 취약합니다.
[6주차 2차시 33:21] 반드시 샵 기호를 사용하여 파라미터 바인딩을 사용해야 하겠습니다.
[6주차 2차시 33:27] 어노테이션을 통해 맵핑을 지정할 때에도 마찬가지이므로 꼭 기억해 두시기를 바랍니다.
[6주차 2차시 33:36] 이번에는 Java Persistence API 방식, 즉 JPA 방식을 보여주고 있습니다.
[6주차 2차시 33:47] 앞에서 보았던 방식과 유사한 방법으로 대응을 하면 되는데요.
[6주차 2차시 33:55] 이렇게 위치 기반 바인딩 방식으로
[6주차 2차시 34:01] 플레이스 홀더 1번 위치에 전화번호를 대입하여
[6주차 2차시 34:05] 쿼리를 완성하도록 하고 있습니다.
[6주차 2차시 34:12] 그래서 파라미터 바인딩이 무적의 방법이냐
[6주차 2차시 34:17] 그렇진 않고, 파라미터 바인딩을 사용하더라도 입력값 자체를 필터링하거나 인코딩 작업을 병행하는 것이 좋은데요.
[6주차 2차시 34:27] 웹 애플리케이션에서 왼쪽, 오른쪽, 꺽쇠 기호 등 HTML 태그 문자가 들어오면 크로스 사이트 스크립팅 취약점이 발생할 수 있고,
[6주차 2차시 34:38] 세미콜론이나 따옴표, 마이너스 마이너스와 같은 SQL 특수 문자가 들어오는 것을 그대로 놔두면
[6주차 2차시 34:45] 항우 코드 유지 보수 과정에서 취약한 코드가 생길 경우 SQL 인젝션 취약점이 다시 발생할 수 있습니다.
[6주차 2차시 34:55] 사용자 입력이 어디에 사용되는지에 따라 인코딩 전략을 달리해야 하는데요.
[6주차 2차시 35:00] 예를 들어 왼쪽 꺽쇠와 오른쪽 꺽쇠 기호 같은 경우 html 바디에 표현해야 한다면 html 인코딩을 통해 and lt, and gt.
[6주차 2차시 35:18] 이게 수학에서는 크다 작다 그런 거 잖아요
[6주차 2차시 35:30] 그래서 less than, greater than 이런 거에 줄임말인데
[6주차 2차시 35:38] 이런 식으로 변환을 해서 사용을 하고
[6주차 2차시 35:41] url에 포함이 된다면 url 인코딩 방식에 따라
[6주차 2차시 35:44] ASCII 코드 표현인 %30, %32 이런 것으로 변환을 해서 사용을 해야 합니다.
[6주차 2차시 36:01] 그러면 이번에는 SQL 맵을 통해
[6주차 2차시 36:05] 가동으로 검증하는 방법에 대해 알아보겠습니다.
[6주차 2차시 36:10] SQL 맵은 SQL 인젝션을 자동으로 탐지할 수 있는
[6주차 2차시 36:13] 강력한 오픈 소스 도구인데요.
[6주차 2차시 36:15] 이 페이지에 나와 있는 검증 테스트 예시처럼
[6주차 2차시 36:19] SQL맵의 URL을 지정하여 여러 공격 페이로드를 주입해봅니다.
[6주차 2차시 36:25] 여기에서 이제 리스크라는 파라미터와 레벨 파라미터는
[6주차 2차시 36:29] 공격의 강도와 테스트 범위를 조정하는 것이고
[6주차 2차시 36:36] 배치 파라미터를 주면 스텝별로 질문하는 것을 생략하게 되어
[6주차 2차시 36:42] 테스트를 자동으로 수행하도록 합니다.
[6주차 2차시 36:45] 만약 SQL 맵이 인젝션 취약점을 발견하면 해당 위치와 유효했던 공격 페이로드를 알려줍니다.
[6주차 2차시 36:55] 실제 운영 서버에서 이런 도구를 돌릴 때에는 DB 부담이나 로그를 많이 발생시킬 수 있어서 테스트 환경을 구축하거나 제한된 범위에서만 진행하는 것이 좋겠습니다.
[6주차 2차시 37:11] SQL 인젝션을 비롯한 보안 공격을 조기 탐지하고 사고에 대응하기 위해서는 로그 기록과 모니터링 체계를 수립하는 것이 매우 중요합니다.
[6주차 2차시 37:27] 웹 애플리케이션 레벨에 따라 요청 파라미터로 로깅하고
[6주차 2차시 37:32] DB레벨에서는 이 부분입니다.
[6주차 2차시 37:36] 웹 애플리케이션에서는 이런 거, 데이터베이스에서는 에러 로그를 남겨두어야
[6주차 2차시 37:42] SQL 인젝션 공격 시도의 징후를 감지할 수 있습니다.
[6주차 2차시 37:48] 이 로그를 보안 모니터링 툴과 연동시켜 특정 키워드나 에러 패턴을 감지하면
[6주차 2차시 37:54] 실시간 알림을 받게 할 수도 있습니다.
[6주차 2차시 38:01] 로그를 기록할 때 너무 많은 정보를 남기면
[6주차 2차시 38:04] 성능에 영향을 줄 수 있고 개인정보가 또 유출될 가능성이 있습니다.
[6주차 2차시 38:09] 하지만 그렇다고 너무 적게 남겨버리면
[6주차 2차시 38:12] 공격 징후를 파악하기 어렵겠죠.
[6주차 2차시 38:16] SQL 인젝션을 탐지하려면 웹 요청 파라미터
[6주차 2차시 38:19] DB 에러 메시지, 아이페이지 주소, 그 다음에 세션 아이디 등의 사용자 식별 정보,
[6주차 2차시 38:27] 요청 시간, HTTP 메서드 등을 로깅하는 것이 유용한 편입니다.
[6주차 2차시 38:34] 이 내용을 심 솔루션, 스플렁크 등으로 보내서 대시보드 형태로 공급 패턴을 보여주거나
[6주차 2차시 38:41] 실시간 알림을 설정할 수 있습니다.
[6주차 2차시 38:49] 그렇게 해서 이번 차시 내용 요약 정리해 보겠습니다.
[6주차 2차시 38:53] SQL 인젝션은 사용자의 입력 값을 제대로 검증하지 않고 사용하여 DB 쿼리가 조작될 수 있는 취약점입니다.
[6주차 2차시 39:01] 또 에러 기반, 유니온 기반, 블라인드 방식 등의 공격에 대해서 알아보았으며
[6주차 2차시 39:08] 그래서 가급적 Prepared Statement로 대표되는 파라미터 바인딩 방식을 사용하여 방어를 해야 한다.
[6주차 2차시 39:16] 그리고 입력과 검증 및 필터링을 포함한 시큐어 코딩이 지속적으로 이루어지고 있는지 자동화 진단 도구를 활용하여 지속적으로 감시해야 합니다.
[6주차 2차시 39:30] 참고 문원이고요.
[6주차 2차시 39:33] 이번 차시 수업 여기까지 하도록 하겠습니다.
[6주차 2차시 39:37] 감사합니다.
[6주차 2차시 39:40] 수고하세요.

# [3-TRANSCRIPT] 6주차 3차시 — ORM·MyBatis / SQL 인젝션 / Command 인젝션
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · ZAP/OWASP ZAP/Active Scan/Burp/버프스위트/버프 스위트 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

[6주차 3차시 00:00] 안녕하세요. 6주차 3차시 강의 시작하도록 하겠습니다.
[6주차 3차시 00:11] 이번 차시에서는 커맨드 인젝션 취약점에 대해 알아보고 대응 전략까지 살펴보겠습니다.
[6주차 3차시 00:24] 학습목표는 다음과 같습니다. 커맨드 인젝션 취약점의 개념과 발생원리를 알아보고, 어떻게 실제 공격기법으로 만들어지는지, 또 어떻게 진단하는지 배워보겠습니다.
[6주차 3차시 00:41] 아울러 방어기법까지 이어서 설명하도록 하겠습니다.
[6주차 3차시 00:50] 이에 따른 학습 내용은 보시는 바와 같습니다. 넘어가겠습니다.
[6주차 3차시 00:59] 그럼 첫 번째로 커맨드 인젝션의 개념과 발생 원리입니다.
[6주차 3차시 01:11] 우선 계열을 보면 적절한 검증 절차를 거치지 않은 사용자 입력 값이 명령어의 일부 또는 전부로 구성되어 실행되는 경우
[6주차 3차시 01:23] 의도하지 않은 시스템 명령어가 실행되어 부적절하게 권한이 변경되거나 시스템 동작에 악영향을 미친다고 되어 있습니다.
[6주차 3차시 01:33] 다시 풀어서 설명드리면 Command Injection이란 웹 애플리케이션이나 서버 프로그램에서 사용자의 입력값을 제대로 검증하지 않는 바람에 사용자가 서버 운영체제의 명령어를 호출할 수 있게 되는 보안 취약점입니다.
[6주차 3차시 01:52] 예를 들어 웹 애플리케이션이 제공하는 서비스에서 사용자가 업로드한 파일을 백신 프로그램에 전달하여 검사하는 기능을 제공하고 있다고 할 때
[6주차 3차시 02:03] 사용자가 검사할 파일명만 입력하는 것이 아니라 악의적인 명령어를 덧붙여 보내면 이 명령어가 서버에서 무방비로 실행되어 버리는 상황인 것입니다.
[6주차 3차시 02:15] 커맨드 인젝션은 입력값 검증 부실과 시스템 명령어 직접 호출 가능이라는 두 가지 조건이 맞물릴 때 발생하는데요.
[6주차 3차시 02:26] 사용자가 매우 창의적으로 악의적인 내용을 입력할 수 있다는 생각을 하지 않고
[6주차 3차시 02:32] 개발자가 전혀 대비하지 않은 점 그리고 시스템 자원을 다룰 때 코드를 통해 완벽하게 통제를 해야 하는데
[6주차 3차시 02:42] 매우 다양한 상황을 대처하기 어렵다면서 사용자 입력 값을 그대로 활용하여 제어권을 맡겨버리는 것이 겹쳐져서 발생합니다.
[6주차 3차시 02:58] 다음은 그림을 보면서 치약점 공격의 흐름을 간단히 따라가 보겠습니다.
[6주차 3차시 03:06] 먼저 좌측의 공격자는 대상 웹 서비스에서 사용자 입력을 받은 페이지들을 조사하다가 시스템 명령어를 호출해 처리하는 것으로 보이는 페이지를 발견합니다.
[6주차 3차시 03:20] 만약 공격자가 다른 방식으로 관리자 계정을 탈취해 관리자 페이지에 우회 로그인까지 했다면 내부 직원의 편의를 위해 간단하게 만들어둔 매우 취약한 페이지들이 있을 가능성도 있습니다.
[6주차 3차시 03:38] 이제 그 중 하나의 페이지에 파일명을 입력하는 기능이 있다고 가정해보겠습니다.
[6주차 3차시 03:44] 1번 단계에서 공격자는 파일명을 입력하며 뒤에 end ping 127.0.0.1 이런 명령어를 덧붙여서 전송을 합니다.
[6주차 3차시 04:00] 프론트엔드에서 명령어 입력을 막았다 하더라도
[6주차 3차시 04:03] 버프스윗 같은 툴을 이용해 요청을 중간에서 조작할 수 있습니다.
[6주차 3차시 04:10] 그 다음 2번에서 웹서버가 이를 검증하지 않고 OS 명령어에 주입하면
[6주차 3차시 04:16] Command Prompt나 Shell에서 처리할 때 추가로 넣은 핑 명령어가 같이 실행되게 됩니다.
[6주차 3차시 04:25] 원래는 타입 명령어로 파일 내용을 출력하려던 기능이었지만
[6주차 3차시 04:29] 여기에 덧붙여진 명령어도 그대로 실행이 되는 것입니다.
[6주차 3차시 04:35] 3번에서는 서버가 명령어 실행 결과를 출력 채널로 보내면서
[6주차 3차시 04:40] 파일 내용뿐 아니라 PING 명령어의 결과까지 같이 사용자에게 전달됩니다.
[6주차 3차시 04:49] 이렇게 공격자가 임의로 서버 내부 명령어를 실행시킬 수 있다는 것이 확인되면
[6주차 3차시 04:55] 이번엔 실제 피해를 일으키는 명령어를 시도할 수 있습니다.
[6주차 3차시 05:01] 예를 들어 rm-rf 같은 명령어로 서버 파일 시스템 전체를 삭제하거나
[6주차 3차시 05:08] wget 명령어를 통해 외부에서 악성 파일을 내려받아 실행하는 것도 가능합니다.
[6주차 3차시 05:18] 이런 공격이 실제로 실행되면 매우 큰 피해가 발생할 수 있지만
[6주차 3차시 05:22] 그 원인을 정확하게 추적하기는 어려운데요.
[6주차 3차시 05:27] 결국 커맨드 인젝션은 개발자가 시켜 코딩을 소홀히 했을 때 발생하는 매우 치명적인 보안 취약점입니다.
[6주차 3차시 05:38] 이번에는 윈도우 환경에서 명령어가 실행되는 방식과
[6주차 3차시 05:47] Command Injection 관계에 대해 알아보도록 하겠습니다.
[6주차 3차시 05:52] 윈도우에서는 일반적으로 Command Prompt로 알려진
[6주차 3차시 05:56] CMD나 PowerShell을 통해 명령어를 처리를 합니다.
[6주차 3차시 06:01] 예를 들어 애플리케이션이 명령어를 실행할 경우
[6주차 3차시 06:04] CMD를 호출하면서
[6주차 3차시 06:06] 슬래시 C 옵션 뒤에 실제 실행할 명령어를
[6주차 3차시 06:12] 인수로 전달하게 됩니다.
[6주차 3차시 06:15] 이때 몇 가지 특수 기호를 활용을 하면
[6주차 3차시 06:17] 한 줄에 여러 개의 명령어를 실행할 수 있습니다.
[6주차 3차시 06:22] 예를 들어 앞 페이지에서 봤듯이
[6주차 3차시 06:25] 명령어와 명령어 사이에 end를 입력했다면
[6주차 3차시 06:29] 두 명령어를 무조건 순차적으로 실행하라는 의미가 됩니다.
[6주차 3차시 06:36] 또한 세로 줄로 표시되는 파이프 기호
[6주차 3차시 06:39] 이렇게 생긴 거 아시죠?
[6주차 3차시 06:50] 그래서 앞쪽 명령어의 출력을 뒤쪽 명령어에 입력해서
[6주차 3차시 06:56] 입력으로 전달하는 걸로 두 명령어가 함께 실행되는 효과를 냅니다.
[6주차 3차시 07:04] 오른쪽 꺽쇠는 출력 결과를 특정 파일로 저장하는 리디렉션 기능을 수행하는데, 이를 악용하면 실행 결과를 숨기거나 다른 파일의 내용을 덮어 쓸 수도 있습니다.
[6주차 3차시 07:19] 파워쉘 역시 커맨드 프롬프트와 본질적으로 다르지 않으며, 특히 관리자 권한으로 실행되면 레지스트리 변경이나 네트워크 설정 조작 같은 고위험 작업도 가능해집니다.
[6주차 3차시 07:40] 그 다음으로는 유닉스 또는 리눅스 환경에서
[6주차 3차시 07:45] 환경은 일반적으로 기본으로 포함된 빈 디렉토리 안에
[6주차 3차시 07:53] shell이나 배시 shell 프로그램을 사용하며
[6주차 3차시 07:57] ampersand나 파이프 같은 메타 문자를 통해
[6주차 3차시 08:01] 여러 명령어를 연결할 수 있습니다.
[6주차 3차시 08:05] 쉘의 특징 중 하나는 인수와 같은 와일드카드를 사용하면
[6주차 3차시 08:11] 해당 조건에 맞는 파일명 리스트를 자동으로 생성해 인수로 전달한다는 점입니다.
[6주차 3차시 08:20] 이 기능을 활용하면 현재 작업 디렉토리에 어떤 파일이 있는지 쉽게 알아낼 수 있습니다.
[6주차 3차시 08:28] 또 하나 주의해야 할 특수문자가 백틱입니다.
[6주차 3차시 08:32] 작은 따옴표처럼 생겼지만 반대 방향으로 기울어진
[6주차 3차시 08:36] 앞에서 얘기한 것은 와일드카드에서 별점 txt 이런 것들을 허용한다는 거고
[6주차 3차시 08:50] 여기서 말하는 백틱은 이렇게 생긴 탭 위에 있는 물결이랑 같이 쓰이는 기호 있잖아요.
[6주차 3차시 08:58] 그걸 백틱이라고 하는데 이 기호로 명령어를 감싸면
[6주차 3차시 09:03] 해당 명령어를 실행한 결과값이 그 자리에 대체가 됩니다.
[6주차 3차시 09:09] 비슷하게 달러기호와 괄호로 명령어를 묶는 서브셀 방식도 존재하고
[6주차 3차시 09:17] 이런 식으로 하고 이 안에다가 또 다른 명령어를 쓰는 거죠.
[6주차 3차시 09:25] 마찬가지로 실행 결과를 삽입하는 데 사용됩니다.
[6주차 3차시 09:29] 이러한 기능들을 악용하면 의도하지 않은 명령어를 따로 실행시킬 수 있게 되는 거죠.
[6주차 3차시 09:37] 이처럼 운영체제마다 명령어 처리 방식은 다를 수 있지만 커맨드 인젝션 지약점이 발생하는 원리는 동일합니다.
[6주차 3차시 09:50] 다음으로 커맨드 인젝션 지약점을 어떻게 진단하고 대응할지 알아보도록 하겠습니다.
[6주차 3차시 10:04] 진단을 진행할 때는 테스트 케이스를 구체적으로 설계한 후 수행해야 합니다.
[6주차 3차시 10:09] 예를 들어 파일 업로드 기능이 있는지, 검색 파라미터가 운영체제 명령와 연동되는지,
[6주차 3차시 10:17] 이미지 변환 툴이나 압축 해제 툴 같은 외부 프로그램을 호출하는지 등
[6주차 3차시 10:22] 애플리케이션 구조를 충분히 이해한 뒤에 테스트 방법을 정해야 합니다.
[6주차 3차시 10:31] 이후에는 테스트 입력 값에 특수문자나 제어문자를 삽입해
[6주차 3차시 10:35] 명령어 실행 흐름이 달라지는지를 관찰합니다.
[6주차 3차시 10:41] 로그 파일이나 서버 콘솔에 평소 보이지 않던 파싱 에러 메시지가 나타난다면
[6주차 3차시 10:47] 인젝션 시도의 징후일 수 있습니다.
[6주차 3차시 10:52] 하지만 이런 징후가 없다고 해서 또 반드시 안전한 것은 아닌데요.
[6주차 3차시 10:58] 에러 없이 권한을 획득한 뒤 조용히 작업이 이루어질 수도 있기 때문이죠.
[6주차 3차시 11:04] 따라서 수동 진단을 할 땐 서버에서 실제로 명령어가 실행되었는지
[6주차 3차시 11:12] 파일이 생성되었는지 네트워크 트래픽이 발생했는지 등을 종합적으로 확인해야 합니다.
[6주차 3차시 11:22] 수동진단은 자동화 도구로는 탐지하기 어려운 세부 로직까지
[6주차 3차시 11:26] 직접 살펴볼 수 있다는 장점이 있지만
[6주차 3차시 11:30] 많은 시간과 경험이 당연히 필요하겠죠.
[6주차 3차시 11:34] 그래서 실제 프로젝트에서는 수동진단과 자동화 도구를 병행해서
[6주차 3차시 11:39] 시약점을 보다 효과적으로 찾아 냅니다.
[6주차 3차시 11:50] 앞서 공격 패턴의 중심이 되는 몇몇 기호들에 대해 이야기했었는데요.
[6주차 3차시 11:57] 수동 진단을 할 때는 이런 기호들을 실제로 입력해 보며
[6주차 3차시 12:00] 동작 여부를 확인해야 합니다.
[6주차 3차시 12:05] 우선 명령어를 연결할 때 사용하는 연결자 기호가 허용되는지부터 점검을 하는 것으로 시작을 합니다.
[6주차 3차시 12:14] 그래서 end 하나를 사용하면 앞뒤 명령어를 무조건 모두 실행하라는 의미가 되고
[6주차 3차시 12:20] end를 두 개를 쓰면 이렇게 하나를 쓰면 모두 무조건
[6주차 3차시 12:28] end를 두 개를 쓰면 앞 명령어가 성공했을 때만 뒤명령어를 실행하게 됩니다.
[6주차 3차시 12:36] 공격자는 애플리케이션이 end 하나만 차단하고 있다는 걸 알게 되면
[6주차 3차시 12:41] 일부러 항상 성공하는 명령어랑 함께 and 두 개를 조합해서 필터링을 우회할 수가 있습니다.
[6주차 3차시 12:53] 타입드 키워도 유사한데요.
[6주차 3차시 12:55] 하나를 사용하면 앞 명령어의 출력을 다음 명령어의 입력으로 넘기면서
[6주차 3차시 13:00] 두 명령어 모두 실행하는 구조가 되고
[6주차 3차시 13:04] 두 개를 사용하면 앞 명령어가 실패했을 때만 뒤 명령어를 실행하라는 의미로 바뀝니다.
[6주차 3차시 13:11] 이어서 환경변수 변조와 서브명령 실행기법의 진단입니다.
[6주차 3차시 13:19] 우선 환경변수 변조 테스트인데요.
[6주차 3차시 13:25] 공격자는 달러 패스나 달러 IFS 등을 악용하여 명령어 실행 경로를 바꾸거나 검증을 우회할 수 있습니다.
[6주차 3차시 13:38] 예를 들어 $IFS는 공백 기호가 들어있기 때문에
[6주차 3차시 13:43] 테스트 달러 IFS LS 이것은 결국에 테스트 한 칸, 아이고
[6주차 3차시 13:58] 테스트 한 칸 띄고 LS명령으로 변환되어 실행될 수 있습니다.
[6주차 3차시 14:03] 공백이 걸러내도록 구현된 경우는 많지만
[6주차 3차시 14:09] 환경 변수를 활용하면 일단 공백이 없기 때문에
[6주차 3차시 14:13] 막아놓은 검사 로직을 통과할 수도 있습니다.
[6주차 3차시 14:17] 또 달러 패스 내용을 조작해서 명령어가 실행될 때 공격자가 악성 코드를 심어놓은 디렉토리로부터 우선 탐색하도록 변조할 수도 있을 겁니다.
[6주차 3차시 14:29] 다음은 서브 명령 실행이 가능한지 테스트를 하는데요.
[6주차 3차시 14:36] 백틱 또는 달러 그리고 괄호 부문을 사용하여 명령어 내부에 또 다른 명령어를 삽입해보는 것입니다.
[6주차 3차시 14:47] 에코 달러 괄호 속에 LS 이런 식으로 쓰면 LS 명령어가 실행된 후 그 결과가 에코 명령어로 전달되면서 출력됩니다.
[6주차 3차시 15:03] 이런 식으로 중첩 실행이 가능하기 때문에 예상치 못한 명령이 서버에서 동작할 수 있게 되는 것입니다.
[6주차 3차시 15:12] 수동진단 시에는 이런 고급 기법들도 시도를 해봐야 합니다.
[6주차 3차시 15:17] 앞서 언급한 것처럼 수동 진단만으로는 모든 취약점을 찾기엔 시간도 많이 늘고 중요한 취약점을 놓칠 위험도 있습니다.
[6주차 3차시 15:29] 따라서 반드시 자동화 도구를 함께 사용하는 것을 권장하는데요.
[6주차 3차시 15:36] 대표적인 오픈소스 웹 취약점 스캐너로는 OWASP에서 제공하는 JAP이 있습니다.
[6주차 3차시 15:45] 얘는 이제 Z-Attack Proxy의 약자이고
[6주차 3차시 15:50] 이 JEP은 브라우저 프록시처럼 작동하면서 HTTP 트래픽을 가로채고 분석할 수 있는 도구입니다.
[6주차 3차시 15:59] 진단 환경은 버프 스위트를 설정할 때와 매우 유사합니다.
[6주차 3차시 16:04] 브라우저의 프록시 설정을 JEP이 실행 중인 서버 주소와 기본 포트인 8080으로 지정하면 이후 브라우저에서 발생하는 모든 요청과 응답이 JEP을 통해 분석되고 기록됩니다.
[6주차 3차시 16:20] 이 상태에서 잽이 제공하는 자동 스캔 기능을 활용하면 다양한 공격 시나리오를 자동으로 수행하며 취약점을 진단할 수 있습니다.
[6주차 3차시 16:35] 잽의 액티브 스캔 기능을 사용하면 미리 정의된 다양한 공격 패턴을 자동으로 시도해 취약점을 진단할 수 있습니다.
[6주차 3차시 16:47] 테스트할 URL을 선택한 후 액티브 스캔을 실행하면
[6주차 3차시 16:53] 곧바로 점검이 시작되며 웹 애플리케이션의 입력 시점마다 공격 시도가 이루어집니다.
[6주차 3차시 17:01] 이 점검 항목에는 커맨드 인젝션 여부도 포함되어 있는데요.
[6주차 3차시 17:07] 스캔 기본 설정의 고급 옵션 부분을 열어보면
[6주차 3차시 17:11] 정책 목록에 좀 작게 보이지만
[6주차 3차시 17:18] OS 리모트 코멘드 인젝션 페이로드라는 항목이 포함되어 있는 것을 볼 수 있습니다.
[6주차 3차시 17:28] 그리고 점검 도중 문제가 탐지되면
[6주차 3차시 17:32] 화면 하단의 경고창을 통해 취약점의 위치와 유형이 실시간으로 표현이 됩니다.
[6주차 3차시 17:41] 그러면 이 커맨드 인젝션을 어떻게 대응하면 좋을지
[6주차 3차시 17:50] 시큐어 코딩 관점에서 살펴보도록 하겠습니다
[6주차 3차시 17:54] 위쪽에 보이는 예시는 취약한 코드의 일부인데요
[6주차 3차시 17:59] 가장 아랫줄을 보면 GetRuntime 메소드를 사용하여
[6주차 3차시 18:07] 명령어 문자열을 윈도우 커맨드 프롬프트에 전달해 실행하려는 구조입니다.
[6주차 3차시 18:16] 그런데 이 명령어 문자열에 결합된 버전 변수는 코드 상단에서 get 파라미터를 통해 사용자로부터 입력받은 값이죠.
[6주차 3차시 18:35] 이게 이제 사용자로부터 입력받은 값, 즉 외부 입력 값을 별다른 검증 없이 지금 명령어에 바로 결합해버리고 있는 셈이 되겠습니다.
[6주차 3차시 18:48] 이 값에 어떤 내용이 들어올지는 전혀 예측할 수 없기 때문에 이러한 방식은 매우 위험합니다.
[6주차 3차시 18:56] 그래서 아래쪽에 있는 안전한 코드로 수정을 할 수가 있는데요.
[6주차 3차시 19:02] 이 안전한 코드에는 먼저 버전 파라미터에 대해 정규 표현식을 사용해 입력 값을 검증을 합니다.
[6주차 3차시 19:17] 여기에서는 숫자가 한 개 이상 포함된 값만 허용하는 정규식을 적용을 했고
[6주차 3차시 19:23] 만약 숫자가 아니거나 값이 비어있다면 부적합한 값으로 처리되도록 분리합니다.
[6주차 3차시 19:33] 사실 이렇게 좁은 범위의 정규식만으로도 커맨드 인젝션 방어가 어느 정도 가능하긴 하지만
[6주차 3차시 19:41] EXEC 함수를 사용할 때는
[6주차 3차시 19:44] 명령어와 인수를 배열 형태로 분리하여
[6주차 3차시 19:47] 전달하는 방식을 반드시 습관화해야 합니다.
[6주차 3차시 19:53] 실제로 개발 현장에서는
[6주차 3차시 19:55] 기존에 작성한 코드를 복사하거나
[6주차 3차시 19:57] 부분제 사용하는 일이 많기 때문에
[6주차 3차시 20:00] 처음부터 시켜코딩 원칙에 맞게 구성해두는 것이 매우 중요합니다.
[6주차 3차시 20:08] 이처럼 명령와 각 인수를 분리하여 배열로 전달하면
[6주차 3차시 20:12] 특수기호를 이용한 우회 실행이 차단되어서
[6주차 3차시 20:18] 이 방식만으로도 커맨드 인젝션의 위험을 상당 부분 예방할 수 있습니다.
[6주차 3차시 20:29] 그리고 사실 커맨드 인젝션을 예방하려면
[6주차 3차시 20:32] OS명령어를 직접 실행하는 함수 자체를 사용하는 것보다
[6주차 3차시 20:37] 직접 OS 명령어를 사용하지 않고 안전하게 프로세스를 실행하는 API를 사용하는 것이 바람직합니다.
[6주차 3차시 20:46] 왜냐하면 이 안에서 막대한 권한을 가진 명령어를 사용하고 있다면 그 명령어를 해커가 악용할 가능성이 있기 때문에 안전한 API를 사용하는 것이 더 바람직한 거죠.
[6주차 3차시 21:05] 예를 들어 자바에서는 프로세스 빌더를 사용하는 방식이 권장되며 이 방식은 명령과 인자를 부분에 실행할 수 있도록 설계되어 있기 때문에 일부러 CMD나 쉘을 다시 실행시키지 않는 한 상당히 안전한 방식이라고 볼 수 있습니다.
[6주차 3차시 21:26] C나 C++ 언어에서는 명령어와 인수를 분리해 실행할 수 있는 EXECVP 함수를 사용하는 것이 좋습니다.
[6주차 3차시 21:40] 그리고 입력 값을 검증할 때는 허용된 값만 통과시키는 화이트 리스트 방식으로 입력 제한 규칙이 철저히 지켜지고 있는지를 반드시 확인해야 합니다.
[6주차 3차시 21:56] 특히 특수기호와 같은 메타 문자는 꼭 필요한 경우가 아니라면 모두 제거하고
[6주차 3차시 22:01] 정말 필요하다면 글자 그대로 전달되도록 escape 처리를 적용해야 합니다.
[6주차 3차시 22:10] 무엇보다 중요한 점은 입력값 검증은 반드시 서버 측에서 수행해야 한다는 것입니다.
[6주차 3차시 22:17] 클라이언트 측의 자바스크립트만으로 검증하면 공격자가 이를 손쉽게 우회할 수 있기 때문입니다.
[6주차 3차시 22:27] 마지막으로 의심스러운 요청이 들어왔을 때 신속하게 탐지할 수 있도록 커맨드 인젝션 공격 관점에 맞는 로깅 및 모니터링 체계를 마련해 두는 것도 매우 중요합니다.
[6주차 3차시 22:43] 커맨드 인젝션을 대응하는 로직을 구현할 때에는 입력값 검증 과정에서 오류가 발생하거나 실행 오류가 발생하더라도 외부로 민감한 정보가 노출되지 않도록 처리해야 합니다.
[6주차 3차시 23:11] 오류 메시지는 내부에만 상세히 기록하도록 하고, 사용자에게는 오류 발생 여부만 간단히 알리는 수준으로 제한해야 합니다.
[6주차 3차시 23:26] 또한 소스 코드 리뷰를 정기적으로 수행하면서 OS 명령어를 호출하는 코드가 존재하는지 해당 부분의 입력과 검증이 제대로 적용되었는지 확인해야 합니다.
[6주차 3차시 23:41] 이와 함께 CICD 파이프라인의 정적 분석 도구를 연동하여
[6주차 3차시 23:46] 코드 변경이 이루어질 때마다 자동으로 보안 검사를 수행할 수 있도록 해야 합니다.
[6주차 3차시 23:53] Command Injection은 입력 조합이 매우 다양하고 복잡하기 때문에
[6주차 3차시 23:56] 테스트 시 다양한 공격 시나리오를 반복적으로 검증해야 합니다.
[6주차 3차시 24:03] 이를 위해 악의적인 입력 사례를 정리한 테스트 시트를 미리 준비해두고
[6주차 3차시 24:08] 단위 테스트 및 통합 테스트 단계에서 주기적으로 검증하는 것이 효과적입니다.
[6주차 3차시 24:17] 하지만 아무리 점검과 대비를 철저히 했더라도 실수나 유지보수 과정에서 새로운 취약점이 발생할 수 있는데요.
[6주차 3차시 24:27] 그렇기 때문에 설령 커맨드 인젝션이 발생하더라도 피해를 최소화하고 시스템을 보호할 수 있는 대비책이 필요합니다.
[6주차 3차시 24:37] 첫 번째로 최소 권한 원칙을 적용하는 것입니다.
[6주차 3차시 24:41] 애플리케이션에서 외부 명령어를 실행하더라도 실행 권한을 제한해 두면 피해 범위를 줄일 수 있습니다.
[6주차 3차시 24:51] 두 번째는 샌드박싱이나 컨테이너와 기술을 활용하는 방법입니다.
[6주차 3차시 24:56] 애플리케이션이 격리된 환경에서 동작하도록 구성하면 공격이 발생하더라도 시스템 전체로 확산되는 것을 막을 수 있습니다.
[6주차 3차시 25:06] 세 번째는 로깅과 모니터링 체계의 구축입니다.
[6주차 3차시 25:10] 이상 행동이 감지되었을 때 즉시 알림을 받고 대응할 수 있도록 감시 체계를 운영하는 것이 중요합니다.
[6주차 3차시 25:21] 이는 커맨드 인젝션 뿐만 아니라 다양한 취약점 대응에 있어 항상 강조되는 핵심 대응 전략입니다.
[6주차 3차시 25:33] 이번 차시 내용 요약해 보겠습니다.
[6주차 3차시 25:36] 이번 차시에서는 커맨드 인젝션의 개념과 진단 대응 방안에 대해 학습을 했습니다.
[6주차 3차시 25:45] 커맨드 인젝션은 검증되지 않은 입력 값에 대한 값의 메타문자를 포함시켜
[6주차 3차시 25:50] 악의적인 OS 명령어를 실행함으로써 시스템을 장악할 수 있는 치명적인 취약점입니다.
[6주차 3차시 25:59] 이 취약점을 진단하기 위해서는 수동 진단과 자동화 도구를 병행하여 보다 효과적으로 탐지해야 합니다.
[6주차 3차시 26:08] 대응 방안으로는 입력값 검증, 안전한 API 사요, 최소 권한의 원칙 적용, 샌드박싱 및 격리 실행,
[6주차 3차시 26:16] 로깅과 모니터링 체계 구축 등이 있으며
[6주차 3차시 26:19] 이와 함께 정기적인 코드 리뷰와
[6주차 3차시 26:23] CICD 파이프라인 내의 정적 분석 도구 연동을 통해
[6주차 3차시 26:27] 사전 예방 체계를 갖추는 것이 중요합니다.
[6주차 3차시 26:34] 참고 문헌이고요.
[6주차 3차시 26:38] 이번 주차 강의 여기까지 하도록 하겠습니다.
[6주차 3차시 26:44] 감사합니다.
[6주차 3차시 26:49] 감사합니다.

