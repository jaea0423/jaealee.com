# WEEK05 — 5주차 인증과 인가 · OAuth2 · JWT (시큐어코딩 중간고사 주차 묶음)

> 이 파일 하나에 5주차의 교안 퀴즈(1-QUESTIONS, 신뢰도 A) · 정리(4-NOTES, C~D) · 교안 원문(2-SLIDES, A) · 강의 발화(3-TRANSCRIPT, B)가 모두 있다.
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

---

# [4-NOTES] 5주차 관련 정리 (신뢰도 C~D) — 교안·발화가 다른 지점. 시험 답은 교안 우선.

## [4-NOTES] 5주차 1차시 · JWT "암호화된 토큰" — 표현 오류 (C)
키워드: JWT, 암호화, 서명, Base64, 인코딩
- [2-SLIDES] 5주차 1차시 p.16 도식: "암호화된 토큰 전송". [5주차 1차시 08:19]는 "서명된 토큰"이라 함.
- 바로잡음: 일반 JWT는 Base64URL 인코딩 + 서명일 뿐 암호화 아님(누구나 내용 디코딩 가능). [2-SLIDES] 5주차 3차시 p.8·p.27도 "암호화되지 않는다"고 명시. 시험에서 "JWT는 암호화된다"는 틀린 보기.

## [4-NOTES] 5주차 3차시 · JWT 서명=암호화 / 공개키 검증 — 부정확 (C)
키워드: JWT, HS256, HMAC, 서명, 대칭키, 비대칭키
- 발화([3-TRANSCRIPT] 5주차 3차시): 서명을 "비밀키로 암호화", 검증을 "공개키로"라고 함.
- 바로잡음: 교안 실습의 HS256은 **대칭키(HMAC)** — 서명·검증에 같은 비밀키. 암호화가 아니라 키를 넣은 해시. 공개키 검증은 RS256·ES256 같은 비대칭 방식에만 해당. 교수님도 [5주차 3차시 25:30]에는 대칭키라고 정리함.

## [4-NOTES] 5주차 3차시 · /jwt/verify 응답 코드 (C)
키워드: JWT, verify, 401, 400, Bad Request
- [5주차 3차시 20:25]: 검증 실패 시 401 Unauthorized라고 함.
- 바로잡음: 실습 코드는 400 Bad Request. [2-SLIDES] 5주차 3차시 p.20·p.21과 [5주차 3차시 23:23]도 400. 또 /jwt/refresh는 역할(role)을 추출한다고 했으나 코드는 "user" 고정값을 넣음.

## [4-NOTES] 5주차 2차시 · 리소스 소유자 예시 — 교안 내부 불일치 (C)
키워드: OAuth2, Resource Owner, 리소스 소유자, 사용자
- [2-SLIDES] 5주차 2차시 p.6: 리소스 소유자 예로 "Google Drive, Github". [2-SLIDES] 5주차 2차시 p.7 표 · [1-QUESTIONS] 5주차 2차시 퀴즈 2 정답 · 발화는 모두 **사용자(User)**.
- 바로잡음: 리소스 소유자 = 사용자. Google Drive는 리소스 서버 쪽 예. 시험은 "사용자"로 답.

## [4-NOTES] 5주차 2차시 · 리디렉트 URI 포트 8000/8080 — 교안 내부 모순 (C)
키워드: OAuth2, redirect_uri, 포트, 8000, 8080
- 테스트 URL·server.port·콘솔 로그는 8000, [2-SLIDES] 5주차 2차시 p.25 설정파일 redirect-uri와 p.26 콘솔 캡처는 8080. 토큰 교환 시 redirect_uri는 인가 요청 때와 같아야 하므로 실제로는 8000으로 통일해야 함.

## [4-NOTES] 5주차 2차시 · PKCE "중간자 공격 방어" — 부정확 (C)
키워드: OAuth2, PKCE, 중간자 공격, 인가 코드 가로채기
- [5주차 2차시 13:09]는 PKCE를 "중간자 공격 방어"라 함.
- 바로잡음: PKCE가 막는 것은 **인가 코드 가로채기**. 통신 도청(MITM) 자체는 TLS가 막음. 교수님도 [5주차 2차시 27:59]에는 "인가 코드 탈취 방지"로 정확히 말함. [2-SLIDES] 5주차 2차시 p.36도 동일.

## [4-NOTES] 5주차 1차시 · 비밀번호 정책 — 교안/발화/최신표준 상이 (D)
키워드: 비밀번호 정책, 최소 길이, 주기적 변경, NIST, SP 800-63B
- [2-SLIDES] 5주차 1차시 p.21 "최소 8~12자", [5주차 1차시 20:15] "최소 12자 + 주기적 변경 요구".
- 보충(D): 최신 지침(NIST SP 800-63B-4, 2025)은 비밀번호 단독이면 최소 15자, **주기적 변경·문자조합 강요 금지**. 시험은 교안 표기로 답하되 실무 기준이 다름을 알아둘 것.

## [4-NOTES] 공통 · 자동 전사 한계 (C)
키워드: 녹취, 자동 전사, 불명확, 음성 인식
- 3-TRANSCRIPT는 자동 전사라 영문 용어·숫자·포트·메서드명에 오인식이 있을 수 있음([불명확]·[표현 차이] 표시). 숫자·코드·정확한 용어는 2-SLIDES(교안)를 우선.
- 6·7주차 녹취는 화면 기록이 없어 교수님 펜 강조 위치를 알 수 없음. 7주차는 1차시 앞부분(시험 안내)과 3차시 중간에 무음 구간이 있어 누락 가능.

## [4-NOTES] 시험 안내 (B, 발화 근거)
키워드: 중간고사, 시험, LMS, 온라인, 범위
- [7주차 1차시 00:00] 발화: 8주차에 중간고사, LMS 온라인 실시간, 공지사항 확인 요망. 범위는 "오늘까지 수업 내용"(1~7주차).
- 시험 규정(사용자 확인): 2026-10-22(목) 19:00~20:00, 온라인 LMS 퀴즈, AI·오픈북 가능, 범위 1~7주차. 날짜·시간은 LMS 공지로 최종 확인.

---

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

---

# [3-TRANSCRIPT] 5주차 1차시 — 인증과 인가 · OAuth2 · JWT
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · SameSite/세임사이트/Strict/Lax/None · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · MFA/Multi-Factor/다중 인증/다중 매체 인증/OTP/FIDO2/WebAuthn · HSTS/HTTP Strict-Transport-Security/스트릭트 트랜스포트 · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin

[5주차 1차시 00:04] 우선
[5주차 1차시 00:06] 업로드 기한을 맞추지 못해서 죄송하다는 말씀 드립니다.
[5주차 1차시 00:11] 앞으로 남은 수업에서는 그 기한을 잘 지켜서 동영상 업로드 할 수 있도록 하겠습니다.
[5주차 1차시 00:22] 이번 차시에서는 인증과 인가 기초 내용에 대해서 이야기해 보도록 하겠습니다.
[5주차 1차시 00:40] 학습 목표입니다.
[5주차 1차시 00:42] 우선 인증과 인가 개념을 분명히 이해하고, 차이점을 설명하고, 웹 애플리케이션 보안 과제 해결을 위한 인증과 인가 방식에는 어떤 것들이 있는지 알아보겠습니다.
[5주차 1차시 00:59] 또한 사고 사례를 통해 CQ 코딩 관점에서 취약점을 분석할 수 있도록 하겠습니다.
[5주차 1차시 01:07] 주요 학습 내용은 다음과 같습니다.
[5주차 1차시 01:11] 인증과 인가 개요를 통해 개념 차이를 정리하고 인증 인가 동작 과정을 직접 살펴보도록 하겠습니다.
[5주차 1차시 01:19] 또한 실습으로 세션 처리를 확인해 보며 보안 위험 및 해결 방법을 통해 실무에서 반드시 적용해야 할 대응책을 배워보도록 하겠습니다.
[5주차 1차시 01:38] 그럼 인증과 인가의 개요부터 시작하도록 하겠습니다.
[5주차 1차시 01:48] 우선 인증이라는 것은 사용자가 등록된 사용자인지 확인하는 과정입니다.
[5주차 1차시 01:54] 예를 들어 아이디, 패스워드를 입력해 로그인할 때 시스템은 입력된 아이디와 비밀번호가 저장된 회원정보와 일치하는지 검증을 하죠.
[5주차 1차시 02:06] 반면 인가는 인증된 사용자에 대해서 어떤 리소스에 어떤 권한을 허용할지 결정하는 절차입니다.
[5주차 1차시 02:16] 관리자는 모든 게시물을 삭제할 수 있지만 일반 사용자는 본인이 작성한 글만 수정할 수 있도록 권한을 제한하는 것이 바로 인가 과정입니다.
[5주차 1차시 02:30] 인증으로 내가 누구인지 확인하고 인가로 무엇을 할 수 있는지를 제어한다는 차이점이 있습니다.
[5주차 1차시 02:43] 인증은 내가 나인지 증명하는 방법입니다.
[5주차 1차시 02:48] 아이디와 비밀번호 입력은 사용이 편리하지만 유출되면 위험이 큰데요.
[5주차 1차시 02:53] 반면에 OTP나 스마트카드 같은 소유기반은 물리적 장치를 잃어버리면 불편하지만 공격에 대한 저항력은 강합니다.
[5주차 1차시 03:06] 그래서 지문, 홍채 같은 생체 기반은 도용이 어렵긴 하지만, 센서 오류가 발생하는 경우나 도입 비용 규모를 고려해야 합니다.
[5주차 1차시 03:22] 실무에서는 이들 방식을 적절히 조합하여서 보안을 강화하고 있습니다.
[5주차 1차시 03:35] 지식기반 인증은 사용자가 이미 알고 있는 정보를 통해 본인 여부를 확인하는 방식입니다.
[5주차 1차시 03:43] 대표적으로 아이디와 비밀번호를 입력하는 로그인 화면이 여기에 해당하는데요.
[5주차 1차시 03:50] 구현과 사용이 익숙해서 비밀번호만 기억하면 되기 때문에 편리하지만 비밀번호가 유출되거나 사회공학 기법에 당하면 바로 위험에 노출될 수 있습니다.
[5주차 1차시 04:02] 따라서 이 방식을 사용할 때는 다단계 인증을 결합해 보안을 강화하고 비밀번호 질문, 답변을 주기적으로 갱신하는 것이 좋습니다.
[5주차 1차시 04:19] 소유기반 인증은 사용자가 물리적으로 소유한 토큰이나 장치로 본인임을 증명하는 방식입니다.
[5주차 1차시 04:27] OTP 토큰이나 스마트카드처럼 실제 장치를 필요로 하기 때문에 단독으로는 도용이 어렵습니다.
[5주차 1차시 04:36] 또한 2차 인증으로도 자주 활용되는데요.
[5주차 1차시 04:40] 다만 분실, 도난 시 무력화될 수 있어서 관리 절차와 재발급 체계를 반드시 갖춰야 합니다.
[5주차 1차시 04:53] 생체 기반 인증은 지문, 홍채, 음성 등 고유한 신체 정보를 활용하는 방식인데요
[5주차 1차시 05:01] 앞서 이야기했듯이 복제나 도용이 매우 어렵고 기억할 필요는 없지만 정보 유출 시 치명적이고 센서 오류나 조명, 소음 같은 환경 변수에 대비해야 합니다
[5주차 1차시 05:24] 다음으로는 기존 인증 방식보다 업그레이드된 최신 인증 기술 3가지를 보도록 하겠습니다
[5주차 1차시 05:31] 첫번째는 패스워드리스 인증입니다
[5주차 1차시 05:34] 대표적 표준 규격으로는 FIDO2와 WebAuthN이 있는데요
[5주차 1차시 05:45] 공개키 기반 암호화를 활용을 하고 사용자는 디바이스에 등록된 지문이나 홍채 같은 생체 정보 또는 핀 번호 입력만으로 서버와 안전하게 인증을 수행해 비밀번호 유출 추측 위험을 근본적으로 제거하는 방식입니다.
[5주차 1차시 06:05] 두번째는 리스크 기반 인증 또는 적응형 인증입니다.
[5주차 1차시 06:12] 로그인 시 사용자의 위치, 디바이스 식별자, 네트워크 환경, 접속시간 등 다양한 컨텍스트 정보를 실시간 분석하여 이 요청이 정상인지를 판단합니다.
[5주차 1차시 06:26] 위험도가 높다고 판단되면 자동으로 일회용 암호인 OTP 또는 다중매체 인증 방식인 MFA로 추가 인증을 요구할 수 있습니다.
[5주차 1차시 06:37] 세 번째 인증 기술은 분산 신원 인증인 Decentralized Identity, 즉 DID입니다.
[5주차 1차시 06:47] 블록체인 같은 분산 원장 기술을 기반으로 중앙 집중식 데이터베이스 없이도 사용자가 검증 가능한 디지털 증명서 형태로 자기 신원 정보를 직접 발급, 검증할 수 있습니다.
[5주차 1차시 07:02] DID 방식을 좀 더 쉽게 설명하면 예를 들어 내 스마트폰에 디지털 지갑을 만들고 병원에서 성인이라는 증명서를 받습니다.
[5주차 1차시 07:14] 이후 쇼핑몰에서 술을 사려고 할 때 지갑에서 성인 증명서를 보여주는데 내 이름이나 생년월일 같은 정보를 보여주지 않아도 되죠.
[5주차 1차시 07:26] 개인정보 주권을 강화하며 상호 운용성을 확보할 수 있는 방식입니다.
[5주차 1차시 07:32] 이처럼 최신 인증 기술은 비밀번호 의존도를 낮추고, 상황에 맞춰 유연하면서도 강력한 보안을 제공하는 방향으로 진화하고 있습니다.
[5주차 1차시 07:50] 이번에는 인증과 인가의 동작 과정을 이야기해 보도록 하겠습니다.
[5주차 1차시 08:00] 웹 애플리케이션에서 인증과 인가 방식은 크게 세션 기반, 토큰 기반, 그리고 외부 인증으로 나눌 수 있습니다.
[5주차 1차시 08:09] 세션 기반은 서버 메모리나 데이터베이스의 세션 정보를 저장하고,
[5주차 1차시 08:15] 로그인 후 발급된 세션 큐키를 통해 사용자를 인증하는 방식이고,
[5주차 1차시 08:19] 토큰 기반은 JWT 같은 서명된 토큰을 발급해서 클라이언트가 로컬에 보관하고 이후 요청 시 Authorization Header에 나와 보내는 방식입니다.
[5주차 1차시 08:33] 또 외부 인증은 OAuth2나 SAML과 같은 프로토콜을 통해 구글, 페이스북 등 타사 인증 서비스를 활용하여 로그인하는 경우를 말합니다.
[5주차 1차시 08:50] 인가 방식 역시 세 가지로 정리를 할 수 있습니다.
[5주차 1차시 08:55] 역할 기반 접근 제어는 사용자에게 관리자, 일반 사용자와 같은 역할을 부여해 권한을 설정하는 개념이고
[5주차 1차시 09:09] 숙성 기반 접근 제어는 사용자 속성, 리소스 속성, 환경 속성 등을 조합해 더욱 세밀하게 접근을 통제하는 방식입니다.
[5주차 1차시 09:20] 그리고 최소 권한 원칙은 모든 사용자에게 꼭 필요한 최소한의 권한만을 부여하는 원칙으로 기본적으로 모든 동작을 금지하고 필요한 경우에만 최소한으로 열어주는 운영 방침이라고 이해하시면 됩니다.
[5주차 1차시 09:37] 이를 반영한 실제 인증 및 인간 흐름은 보는 바와 같이 세 단계로 흘러가게 되니 참고하시면 되겠습니다.
[5주차 1차시 09:52] 그러면 세션 기반 인증 과정을 한번 자세히 살펴보도록 하겠습니다.
[5주차 1차시 09:58] 사용자가 웹사이트에 접속하게 되면 세션 저장소가 할당되며 할당된 저장소를 식별하기 위해서 세션 아이디가 부여됩니다.
[5주차 1차시 10:09] 이렇게 발급된 세션 아이디는 응답 메시지 헤더의 set cookie 값을 통해 브라우저에 전달됩니다.
[5주차 1차시 10:16] 사용자는 인증을 요청하기 위해 아이디와 패스워드를 서버에 전달하게 되고, 서버는 사용자로부터 전달받은 아이디와 패스워드를 검증하여 정상적인 사용자이면 할당된 세션 저장소에 인증 정보를 저장합니다.
[5주차 1차시 10:38] 세션 저장소에는 하나의 서버를 운영하는 경우에는 메모리를 여러 대의 서버를 운영하는 경우에는 파일이나 데이터베이스를 사용하기도 합니다.
[5주차 1차시 10:49] 이후 사용자들의 요청을 수신하게 되면 서버는 세션 저장소에 저장되어 있는 사용자의 로그인 정보나 권한 정보를 사용하여 인가 정책을 적용하게 됩니다.
[5주차 1차시 11:00] 즉 서버는 요청마다 쿠키에 담긴 세션 아이디를 사용해서 사용자의 권한을 검증하기 때문에 쿠키에 대한 보안 조치가 필요합니다.
[5주차 1차시 11:14] 쿠키 값을 브라우저에서 액세스할 수 있게 제한하는 HTTP Only 속성을 True로 설정하거나 HTTPS 통신에서만 쿠키를 전송할 수 있도록 제한하는 Secure 속성을 True로 설정해야 하겠습니다.
[5주차 1차시 11:34] 그럼 이제 LAB 서비스에서 버프 수트를 활용해
[5주차 1차시 11:39] 세션 쿠키 발급과 전달 과정을 직접 확인하는 방법을 살펴보도록 하겠습니다
[5주차 1차시 11:45] 먼저 Proxy 탭에서 인터셉트를 끈 상태로 LAB 서비스에 접속합니다
[5주차 1차시 11:52] 그러면 HTTP 히스토리 화면에서 슬래시 즉 루트 URL에 대한 요청과 응답 내용이 남아 있습니다.
[5주차 1차시 12:01] 리퀘스트 메시지에는 쿠키 내용이 없었지만,
[5주차 1차시 12:06] 리스폰스 메시지의 새 쿠키 헤더에 새로운 세션 아이디 값이 들어있는 것을 볼 수 있습니다.
[5주차 1차시 12:14] 이렇게 새로운 세션 아이디가 쿠키 값으로 저장되어 사용이 됩니다.
[5주차 1차시 12:24] 이렇게 발급된 세션 아이디는 리퀘스트가 전송될 때마다 함께 전송이 됩니다.
[5주차 1차시 12:32] 자동으로 추가 요청이 들어간 슬래시 로그인 URL의 GET 항목을 선택한 후 하단 리퀘스트 탭을 보면 발급된 세션 아이디 극기가 포함되어 전송되는 것을 확인할 수 있습니다.
[5주차 1차시 12:50] 이번에는 토큰 기반 인증 과정을 살펴보도록 하겠습니다
[5주차 1차시 12:57] 사용자가 로그인 정보를 포스트로 전송하면
[5주차 1차시 13:01] 서버는 우선 유효성 검증을 하고
[5주차 1차시 13:04] 그 다음 사용된 JWT를 응답 내용의 JSON 형태로 담아 반환합니다
[5주차 1차시 13:12] 클라이언트는 이 토큰을 로컬 스토리지나 보안 쿠키에 저장하고 이후 모든 API 요청 시 authorization Header의 베어러 키워드와 함께 JWT를 보냅니다.
[5주차 1차시 13:26] 서버는 토큰의 서명을 확인한 후 페이로드에 담긴 클레임 정보를 통해 사용자의 신원과 권한을 검증합니다.
[5주차 1차시 13:35] 이러한 방식은 상태 비저장인 스테이트리스 구조로 마이크로서비스 환경에서 확장성이 뛰어나기 때문에 많이 활용되고 있습니다.
[5주차 1차시 13:54] 이번에는 HTTP 통신 내용을 보면서 JW 기반 로그인 방식을 알아보겠습니다.
[5주차 1차시 14:02] 성공적인 로그인 요청을 보내고 나면 리스폰스 바디에 발급된 액세스 토큰 필드를 확인할 수 있습니다.
[5주차 1차시 14:11] 이 JWT 형태의 토큰이 클라이언트 측 로컬 스토리지나 쿠키에 저장된 후 인증된 사용자만 사용할 수 있는 API를 호출할 때마다
[5주차 1차시 14:27] Authorization 헤더의 bearer 키워드와 함께 토큰이 담겨져 전송되는 것입니다.
[5주차 1차시 14:41] 이제 인증된 사용자만 접근할 수 있는 프로필 조회 화면으로 이동할 경우입니다.
[5주차 1차시 14:47] 클라이언트가 해당 URL로 GET 요청을 보낼 때
[5주차 1차시 14:51] Authorization 헤더에 베어러와 함께 토큰이 담겨져 있는 것이 보이죠.
[5주차 1차시 14:57] 서버는 이 토큰을 검증한 뒤 페이로드에 들어있던 유저 아이디, 유저네임, 이메일, 그리고 롤, 역할값이 담긴 제이선 응답을 반환을 하고 있습니다.
[5주차 1차시 15:19] 그럼 마지막으로 인증 및 인가와 관련된 보안 위협과 그 해결 방법을 알아보도록 하겠습니다
[5주차 1차시 15:33] 인증 단계에서 우리가 접할 수 있는 대표적인 보안 위협 6가지를 살펴보겠습니다
[5주차 1차시 15:39] 각 위협이 실제 서비스에서 어떤 위험을 초래하는지, 그리고 공격 방식의 핵심을 이해하는 것이 중요하겠습니다.
[5주차 1차시 15:50] 첫 번째로 크리덴셜 스터핑으로 알려져 있는 유명한 공격입니다.
[5주차 1차시 15:56] 이미 예전에 유출된 사용자 계정 정보를 다른 사이트에 대입해보는 공격인데요.
[5주차 1차시 16:03] 공격자는 자동화 스크립트를 이용하여 대량의 계정 비밀번호 조합을 로그인 폼에 넣어서 전송하고 성공 여부를 체크합니다.
[5주차 1차시 16:14] 이러한 방법을 통해 여러 사이트에서 동일한 비밀번호를 쓴 사용자의 계정을 손쉽게 탈취할 수 있습니다.
[5주차 1차시 16:23] 그리고 사전 대입 공격이라는 딕셔너리 어택이 있는데요.
[5주차 1차시 16:30] 이것은 자주 사용하는 단어, 문자열, 키워드, 목록을 이용해 비밀번호를 맞춰보는 기법입니다.
[5주차 1차시 16:39] 로그인을 여러 번 실패할 때 계정을 잠그는 정책이 없는 서비스라면
[5주차 1차시 16:43] 공격자는 비교적 짧은 시간 내에 쉬운 비밀번호들을 찾아낼 수 있습니다.
[5주차 1차시 16:51] 다음으로 피싱과 소셜 엔지니어링이 있습니다.
[5주차 1차시 16:56] 일반인들에게도 많이 알려진 공격인데요. 이메일, sms, 가짜 로그인 페이지 등을 통해 사용자를 속여 자격증명을 탈취하는 공격입니다.
[5주차 1차시 17:09] 기술적 방어만으로는 막 완전히 막기가 어려워서 사용자 교육과 행동 분석을 통한 이상행동 탐지 방법을 지속적으로 도입하는 추세입니다.
[5주차 1차시 17:19] 세 번째, 중간자 공격, man in the middle, 줄여서 MITM이라고 부릅니다.
[5주차 1차시 17:27] 이는 사용자가 로그인하는 과정에서 네트워크 트래픽을 가로채거나 변조하는 방식이며,
[5주차 1차시 17:35] 버프스트로 활용한 데이터 변조도 대표적인 사례 중 하나입니다.
[5주차 1차시 17:41] 통신 암호와 HTTPS가 제대로 적용되지 않았거나,
[5주차 1차시 17:49] 인증서 위조가 가능할 경우 발생합니다.
[5주차 1차시 17:52] 항상 TLS 암호를 최신 버전으로 구성하고
[5주차 1차시 17:56] 무조건 HTTPS로만 접속하도록
[5주차 1차시 18:00] HTTP 스트릭트 트랜스포트 시큐리티 즉 HSTS를 적용하여 위험을 최소화해야 합니다.
[5주차 1차시 18:11] 다음으로 세션 하이제킹은 공격자가 유효한 세션 쿠키나 토큰을 탈취해
[5주차 1차시 18:17] 인증된 사용자로 인식되도록 하는 공격입니다.
[5주차 1차시 18:23] 쿠키 탈취를 방지하려면
[5주차 1차시 18:29] Secure, HTTP Only, Same Site 설정을 설정해야 하며
[5주차 1차시 18:35] 토큰 기반 인증 시 짧은 만료 시간을 적용해야 합니다.
[5주차 1차시 18:42] 다섯 번째, 브루트 포스 어택이라고 부르는
[5주차 1차시 18:44] 무차별 대입 공격 방식은
[5주차 1차시 18:47] 말 그대로 가능한 모든 조합을 시도해보면서 비밀번호를 알아내는 방식입니다.
[5주차 1차시 18:54] 문자 종류와 길이에 따라 조합수가 급격히 늘어나지만
[5주차 1차시 18:58] 병렬화된 bot 네트워크를 활용한다면 여전히 실효성이 있습니다.
[5주차 1차시 19:04] 특히 패스워드 정책이 약하면 성공 확률이 높아지겠죠.
[5주차 1차시 19:13] 마지막으로 취약한 MFA 우회 공격이 있습니다
[5주차 1차시 19:17] OTP나 푸시 알림 같은 2차 인증 수단을 우회하는 기법이 존재하는데요
[5주차 1차시 19:23] 예를 들어 악성 코드를 통해 로컬 파일에서 OTP 시크릿 키를 추출하거나
[5주차 1차시 19:29] SMS 중간자 공격으로 인증 코드를 가로채기도 합니다
[5주차 1차시 19:34] 따라서 MFA를 도입할 때는 로컬 저장소 사용을 최소화하고 가능한 생체기반 2차 인증을 병행하는 것이 좋겠습니다.
[5주차 1차시 19:46] 이처럼 인증 단계에는 다양한 공격 벡터가 존재하며 단일 방어만으로는 완전한 보호가 어렵습니다.
[5주차 1차시 20:00] 이제 앞에서 살펴본 다양한 인증 보안 위협을 차단하기 위해 대응 방안을 하나씩 살펴보도록 하겠습니다.
[5주차 1차시 20:09] 우선 첫째로 강력한 비밀번호 정책을 수립해야 합니다.
[5주차 1차시 20:15] 최소 12자리 이상 대문자, 소문자, 숫자, 특수문자를 조합하도록 요구하고 사용자에게 주기적으로 변경하도록 요구하며
[5주차 1차시 20:28] 이전 비밀번호 재사용을 금지합니다
[5주차 1차시 20:32] 그리고 계정 잠금 및 로그인 시도 제한을 도입해서 브루트포스 공격과 딕셔너리 어택을 방어합니다
[5주차 1차시 20:42] 연속 로그인 실패가 일정 횟수를 넘으면 잠시 계정을 잠그거나 추가 인증을 요구합니다.
[5주차 1차시 20:51] 다음으로 다중매체 인증, 즉 멀티 팩터 어센티케이션을 필수적으로 적용해야 합니다.
[5주차 1차시 20:59] SMS, 이메일, OTP보다는 Authenticator App, FIDO2 또는 WebAuthn, 보안키, 생체 인증 등을 우선적으로 도입해서 MFA 우회 공격 위험을 최소화해야 합니다.
[5주차 1차시 21:20] 그리고 TLS 적용 및 HSTS를 철저히 구성해 중간자 공격을 막습니다.
[5주차 1차시 21:29] 모든 인증 엔드포인트를 HTTPS로만 노출하고, HTSTS 헤더를 통해 클라이언트가 무조건 암호화 채널을 사용하도록 강제해야 합니다.
[5주차 1차시 21:41] 다섯 번째로는 세션 토큰 보안 설정을 강화해야 합니다.
[5주차 1차시 21:45] 세션 쿠키에는 Secure, HTTP Only, Same Site Strict 속성을 설정하고
[5주차 1차시 21:53] JWT는 짧은 만료 시간을 설정하면서
[5주차 1차시 21:57] 리프레쉬 토큰 방식을 조합해 탈취할 수 있는 리스크를 줄입니다
[5주차 1차시 22:02] 그리고 이상징후 탐지 및 로그를 모니터링하는 것을 구현하는 것이 필요합니다
[5주차 1차시 22:12] 로그인 성공, 실패, MFA 우회 시도, 세션 생성, 삭제 등의 이벤트를 실시간으로 분석해서 일상적이지 않은 패턴이 감지되면 자동차단 또는 경고를 발송하도록 합니다.
[5주차 1차시 22:29] 마지막으로 자동화된 곳이 서비스에 접근하는 것을 제한할 수 있도록 캡처와 같은 솔루션을 적용하는 것이 좋습니다.
[5주차 1차시 22:38] 이렇게 다층 방어 원칙에 따라 종합적으로 대응한다면 현존하는 인증 단계의 위협을 대부분 효과적으로 차단할 수 있습니다.
[5주차 1차시 22:52] 앞서 인증과 관련된 보안 이야기를 했다면 지금부터는 인가와 관련된 내용을 다루도록 하겠습니다.
[5주차 1차시 23:02] 인가 단계에서 마주치게 되는 보안 위협으로는 다음과 같이 크게 7가지가 있습니다.
[5주차 1차시 23:08] 먼저 권한 상승 공격입니다.
[5주차 1차시 23:11] 의도치 않게 관리자 권한이 일반 사용자에게 부여되거나
[5주차 1차시 23:15] 클라이언트 쪽에서 권한 검사가 누락될 때 발생합니다.
[5주차 1차시 23:20] 다음으로는 수평적 권한 상승으로
[5주차 1차시 23:22] 같은 권한 등급 내에서 다른 사용자의 리소스를 조회하거나 수정하는 공격입니다.
[5주차 1차시 23:30] 예를 들어 URL 파라미터의 사용자 아이디를 바꿔서
[5주차 1차시 23:33] 다른 계정의 정보를 열람할 수 있는 형태가 예시가 되겠습니다.
[5주차 1차시 23:40] 세 번째로 수직적 권한 상승이 있는데요.
[5주차 1차시 23:44] 일반 사용자가 관리자 전용 기능을 호출해 시스템을 제어하는 방식입니다.
[5주차 1차시 23:51] 다음으로는 IDOR, 취약한 객체의 직접 참조,
[5주차 1차시 23:57] 인시큐어 다이렉트 오브젝트 레퍼런시스
[5주차 1차시 24:02] 라고 하는 위협이 있습니다.
[5주차 1차시 24:07] 내부 객체를 가리키는 식별자를 URL 같은 곳에 그대로 노출하여
[5주차 1차시 24:12] 그 의미만 이해하면 아무나 제약 없이 접근 가능하게 만들어 놓은 상황이고
[5주차 1차시 24:19] 다섯 번째로는 CSRF 즉 Cross-Site Request Forgery 공격은
[5주차 1차시 24:25] 사용자의 인증 세션을 악용해 의도치 않은 요청이 실행되는 상황을 말합니다.
[5주차 1차시 24:32] 여섯 번째, 불충분한 API 권한 검증이란
[5주차 1차시 24:35] 인증만 통과하면 모든 API를 사용할 수 있도록 개방해버리는
[5주차 1차시 24:40] 구조적 결함을 얘기를 합니다.
[5주차 1차시 24:44] 마지막으로 URL 기반 접근 통제 부족은
[5주차 1차시 24:47] 특정 엔드포인트가 숨겨지지 않아
[5주차 1차시 24:50] 경로만 알면 누구나 접속할 수 있는 문제입니다.
[5주차 1차시 24:53] 인가와 관련된 부분도 이렇게 다양한 공격 벡터를 모두 고려하여 설계를 강화해야 합니다.
[5주차 1차시 25:02] 이제 앞서 설명한 인가 단계의 보안 위협을 막기 위한 구체적 대책을 살펴보도록 하겠습니다.
[5주차 1차시 25:11] 첫 번째, 인가에서 중요한 건 최소 권한 원칙입니다.
[5주차 1차시 25:16] 한마디로 필요한 최소한의 권한만 부여하여 시스템을 보호하도록 하는 거죠.
[5주차 1차시 25:22] 두 번째는 역할 기반 접근 제어입니다. 최소 권한을 어떻게 할당해야 할지 고려할 때 관리자, 일반 사용자, 게스트 등과 같이 각 역할을 구분하고 그 역할에 맞춰 최소 권한을 할당하는 것이 좋습니다.
[5주차 1차시 25:39] 세번째는 IDOR 제한인데요,
[5주차 1차시 25:46] IDOR은 Insecure Direct Object Reference의 약자로 인증이나 권한 확인 없이 직접 객체에 접근할 수 있는 보안 문제인데요.
[5주차 1차시 25:57] 쉽게 말하면 URL에서 번호만 바꾸면 타인의 정보를 볼 수 있는 상황입니다.
[5주차 1차시 26:02] 예를 들어 API, slash orders, slash 1000 이런거에서 1000이 사용자 아이디인 경우에 이 url을 1001, 1002로 조작하여 전송을 했을 때 주문이 1002에 주문이 되지 않게 하려면 url 경로에 이런 아이디 정보를 노출시키지 않거나 만약 노출이 되었다고 하더라도 서버에서 요청 대상이 실제 소유자인지 반드시 비교하여 사고를 예방해야 합니다.
[5주차 1차시 26:32] 네번째, 정책 기반 접근 제어 방식을 적용하는 것입니다.
[5주차 1차시 26:38] 시간대, IP 주소와 같은 특정 조건에 따라서 접근 제어를 하는 방식입니다.
[5주차 1차시 26:45] 다섯번째는 서버 측 권한 검사입니다.
[5주차 1차시 26:48] 권한 검증은 반드시 서버에서 수행하도록 설계되고 구현되어야 합니다.
[5주차 1차시 26:55] 여섯번째는 크로스 사이트 요청 위조 방지입니다.
[5주차 1차시 26:59] 이를 방지하기 위해 CSRF 토큰을 적용하고 요청은 Same 사이트는 스트릭트, 쿠키 설정 등을 통해서 위조된 요청을 차단할 수 있도록 해야 합니다.
[5주차 1차시 27:11] 마지막으로 인증 보안 위협 대응 방안과 마찬가지로 중요 리소스 접근, 권한 변경 시도를 실시간으로 기록하기 위해서 보안 로깅 및 모니터링을 실시하고
[5주차 1차시 27:24] 이상징후가 감지되면 관리자에게 자동 알림을 보내거나 세션을 강제 만료시키는 체계를 갖춰야 합니다
[5주차 1차시 27:39] 이번 차시 내용 요약 정리해 보겠습니다
[5주차 1차시 27:42] 이번 차시에서는 인증이 사용자의 신원을 검증하는 과정이고
[5주차 1차시 27:51] 인가는 그 사용자가 어떤 리소스에 접근할 수 있는지를 결정하는 과정이라는 것을 배웠고요
[5주차 1차시 27:58] 그리고 세션 기반 인증에서는 서버가 세션을 관리하고, 토큰 기반 인증에서는 클라이언트가 토큰을 저장해서 요청 시 전송하는 구조를 비교해 보았습니다.
[5주차 1차시 28:11] 아울러 보안을 강화하기 위해 활용되고 있는 멀티팩터 어센티케이션, 비밀번호 없는 인증, 생체 인증 같은 최신 기법 등을 알아보았고,
[5주차 1차시 28:22] 크로스 사이트 스크립팅, CSRF, 세션 하이제킹, 토큰 재사용과 같은 공격을 막기 위해서는
[5주차 1차시 28:29] 항상 입력 값을 검증하고 푸키의 HTTP Only 시큐어 Same 사이트 속성을 설정해야 하며
[5주차 1차시 28:38] 토큰 서명을 검증하는 등의 대책이 필요함을 배웠습니다.
[5주차 1차시 28:43] 그리고 안전한 인증 시스템을 구축하기 위해 HTTPS, TLS 암호와 최소 권한의 원칙을 적용하면서
[5주차 1차시 28:50] 반드시 이상징후 모니터링을 병행해야 합니다.
[5주차 1차시 28:58] 참고 문안이고요.
[5주차 1차시 29:02] 이번 차시 수업은 여기까지 하도록 하겠습니다.
[5주차 1차시 29:06] 감사합니다.

# [3-TRANSCRIPT] 5주차 2차시 — 인증과 인가 · OAuth2 · JWT
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링

[5주차 2차시 00:04] 네,
[5주차 2차시 00:05] 5주차 2차시 강의 시작하도록 하겠습니다.
[5주차 2차시 00:10] 이번 차시에서는 OAuth2 인증 및 인가 방식에 대해 알아보도록 하겠습니다.
[5주차 2차시 00:22] 학습 목표입니다.
[5주차 2차시 00:26] OAuth2의 개념과 필요성을 이해해 보면서 프로세스 및 구성 요소를 알아보겠습니다.
[5주차 2차시 00:32] 아울러 실제 구현 과정을 체험해 보는 시간도 가져보려고 합니다.
[5주차 2차시 00:38] 그리고 이에 따른 보안 위협으로 어떤 것이 있는지 알아보고 해결 방안까지 학습해 보도록 하겠습니다.
[5주차 2차시 00:47] 이에 따른 학습 내용은 앞서 말씀드린 내용과 동일합니다.
[5주차 2차시 00:54] 그럼 우선 OAuth2가 라는 것이 무엇인지 알아보도록 하겠습니다.
[5주차 2차시 01:04] 웹 모바일 환경에서 널리 쓰이는 권한 위임 표준 OAuth2에 대해 이야기해 보도록 하겠습니다.
[5주차 2차시 01:13] 먼저 OAuth라는 개념부터 살펴볼게요.
[5주차 2차시 01:17] OAuth는 애플리케이션이 사용자의 비밀번호를 직접 다루지 않고도
[5주차 2차시 01:27] 사용자 대신 서버 자원에 안전하게 요청할 수 있도록 만든 권한 위임 방식의 규격입니다.
[5주차 2차시 01:35] 예를 들어 어떤 쇼핑몰에서 구글 계정으로 로그인 버튼을 눌렀을 때
[5주차 2차시 01:40] 쇼핑몰 사이트가 여러분의 구글 비밀번호를 알고 있지 않다는 점을 떠올려 보시면
[5주차 2차시 01:46] 구글 인증 서버가 여러분을 대신해 발급해준 액세스 토큰만 전달받아 이메일 주소나 프로필 정보를 가져오는 흐름이 바로 OAuth의 핵심입니다.
[5주차 2차시 02:01] 초기 보전인 OAuth 1은 요청마다 복잡한 서명 과정을 거쳐야 했습니다.
[5주차 2차시 02:07] 이 서명 절차 때문에 구현이 까다로웠고 모바일 앱이나 싱글 페이지 애플리케이션처럼 새로운 트렌드에 적용하기도 힘들었습니다.
[5주차 2차시 02:17] 그래서 2012년에 발표된 OAuth2에서는 서명 과정을 없애고 HTTPS 프로토콜만으로 토큰을 검증하는 베어로 방식을 도입을 했고 이 덕분에 토큰 기반 인증이 훨씬 가벼워졌고 여러 종류의 인증 흐름을 지원하면서 다양한 클라이언트
[5주차 2차시 02:39] 환경에 쉽게 적용할 수 있게 되었습니다.
[5주차 2차시 02:42] 다시 정리하자면 OAuth2는 복잡한 암호화나 서명 없이도
[5주차 2차시 02:50] HTTPS 연결만으로 액세스 토큰을 주고받아 권한을 위임할 수 있다는 점에서
[5주차 2차시 02:56] 더욱 가볍고 애플리케이션 환경에 구애받지 않는 유연성을 확보했으며
[5주차 2차시 03:02] 구현 난이도를 크게 낮춘 권한 위임 표준이라고 할 수 있습니다.
[5주차 2차시 03:07] 이제 OAuth2가 어떻게 탄생했고 어느 점이 개선되었는지 이해되셨을 거라 생각됩니다.
[5주차 2차시 03:20] 이번에는 OAuth2가 작성할 수 있도록 반드시 필요한 4가지 구성요소를 알아보겠습니다.
[5주차 2차시 03:28] 먼저 클라이언트 애플리케이션은 인증 서버의 사용자를 대신하여 권한을 요청하는 역할을 담당합니다.
[5주차 2차시 03:35] 우리가 쓰는 모바일 앱이나 웹 서비스가 바로 클라이언트입니다.
[5주차 2차시 03:41] 다음으로 리소스 소유자는 서버에 보관된 실제 데이터의 주인, 즉 우리가 로그인해서 접근하려는 이메일이나 사진 같은 정보를 가진 실제 사용자입니다.
[5주차 2차시 03:54] 이 사용자가 직접 비밀번호를 입력하면 그 값을 클라이언트에 전달하지 않고 대신 인증 서버의 본인임을 증명합니다.
[5주차 2차시 04:05] 그리고 권한 서버는 클라이언트가 요청한 권한이 적절한지 확인한 뒤 액세스 토큰을 발급하는 곳입니다.
[5주차 2차시 04:15] 구글 계정으로 로그인할 때 구글이 바로 이 권한 서버 역할을 수행하는 것입니다.
[5주차 2차시 04:21] 마지막으로 리소스 서버는 실제로 데이터를 보호하고 보관하고 있으며 유효한 액세스 토큰이 제시되었을 때만 요청된 리소스를 반환합니다.
[5주차 2차시 04:33] 예를 들어 여러분의 구글 드라이브 파일을 제공해주는 서버가 여기에 해당합니다.
[5주차 2차시 04:39] 이처럼 내 주체가 서로 역할을 분담하면서 클라이언트는 사용자 비밀번호를 직접 알 필요 없이 토큰만으로 안전하게 데이터에 접근할 수 있게 됩니다.
[5주차 2차시 04:57] 그럼 각 요소가 어떤 역할을 하는지 자세히 살펴보도록 하겠습니다.
[5주차 2차시 05:01] 먼저 클라이언트 애플리케이션입니다.
[5주차 2차시 05:05] 여러분이 사용하는 웹사이트나 모바일 앱이 바로 이 클라이언트라고 얘기했었는데요.
[5주차 2차시 05:12] 사용자가 로그인을 누르면 클라이언트는 권한 서버에 인증 요청을 보냅니다.
[5주차 2차시 05:18] 이때 클라이언트는 자신을 식별하기 위해서 클라이언트 아이디와 클라이언트 시크릿을 함께 전송합니다.
[5주차 2차시 05:26] 권한 서버가 이 정보를 확인하면 사용자가 동의한 범위에 따라 인가 코드가 클라이언트에 반환하게 됩니다.
[5주차 2차시 05:35] 이 코드를 받은 클라이언트는 다시 액세스 토큰을 요청하는 단계로 넘어갑니다.
[5주차 2차시 05:42] 다음으로 리소스 소유자의 차례입니다.
[5주차 2차시 05:45] 리소스 소유자는 보호된 리소스의 실제 주인인 사용자 자신을 뜻하는데요.
[5주차 2차시 05:50] 리소스 소유자는 클라이언트의 비밀번호를 직접 주지 않고 권한 서버가 제공하는 로그인 창에 안전하게 로그인 자격을 증명합니다.
[5주차 2차시 06:02] 이 과정을 통해 사용자의 민감 정보가 클라이언트에 노출되는 것을 방지합니다.
[5주차 2차시 06:09] 다음으로 권한 서버가 있습니다.
[5주차 2차시 06:11] 권한 서버는 클라이언트 애플리케이션이 보낸 인가코드와 시크릿을 검증하게 되며 적법하다고 판단되면 액세스 토큰과 선택적으로 리프레쉬 토큰을 발급을 합니다.
[5주차 2차시 06:26] 액세스 토큰은 유효기간이 짧아서 만료되면 다시 발급받아야 하고, 리프레쉬 토큰은 만료된 액세스 토큰을 새로 발급받을 때 사용됩니다.
[5주차 2차시 06:36] 마지막으로 리소스 서버는 실제로 데이터를 저장하고 있는 서버를 말하는데요.
[5주차 2차시 06:44] 클라이언트는 권한 서버가 발급한 액세스 토큰을 제대로 제시해야만 리소스 서버로부터 사용자 정보나 파일 같은 요청한 리소스를 제공받을 수 있습니다.
[5주차 2차시 06:59] 이때 리소스 서버는 토큰의 유효성뿐 아니라 적용 범위, 즉 스코프까지 확인하여 해당 토큰으로 이 API를 호출해도 되는가를 점검합니다.
[5주차 2차시 07:12] 이와 같이 4가지 요소가 순수대로 협력하여 클라이언트가 사용자의 민감 정보를 직접 다루지 않으면서도 안전하게 리소스에 접근할 수 있는 구조를 완성합니다.
[5주차 2차시 07:29] 이번에는 실제로 인증이 이루어지는 과정을 단순화시켜 그림을 통해 한번 살펴보도록 하겠습니다.
[5주차 2차시 07:36] 우선 1번, 사용자가 애플리케이션의 서비스 접속을 시도합니다.
[5주차 2차시 07:43] 즉시 애플리케이션은 2번, 2번을 따라 권한 서버에 인증 요청 페이지를 띄우도록
[5주차 2차시 07:53] 리디렉트를 시켜 사용자를 로그인 화면으로 보냅니다.
[5주차 2차시 07:57] 죄송합니다.
[5주차 2차시 08:00] 리디렉트된 로그인 페이지에서 사용자는 로그인 정보를 입력하고 권한동의 화면에서 허용을 클릭하면 4번을 따라가게 됩니다.
[5주차 2차시 08:11] 동의가 완료되면 권한 서버는 이제 5번을 따라서 Authorization Code, 즉 인가 코드를 발급하여 애플리케이션에 전달합니다.
[5주차 2차시 08:20] 애플리케이션은 6번 단계에서 받은 인가코드를 기반으로 리소스 서버 액세스토큰 요청을 권한 서버에 보냅니다.
[5주차 2차시 08:35] 이때 클라이언트 시크릿과 함께 인가코드를 전송하여 자신을 인증을 하고요.
[5주차 2차시 08:42] 권한 서버는 이를 검증한 뒤 7번 액세스토큰을 발급해 줍니다.
[5주차 2차시 08:47] 이제 애플리케이션은 발급받은 액세스 토큰으로 8번을 따라 리소스 서버에 필요한 사용자 리소스를 요청합니다.
[5주차 2차시 08:57] 리소스 서버는 9번을 통해 방금 발급받은 액세스 토큰이 맞는지 권한 서버와 크로스 체크를 수행을 하고
[5주차 2차시 09:05] 토큰이 유효하면 10번을 통해 OK 응답을 받습니다.
[5주차 2차시 09:09] 그럼 이제 리소스 서버는 11번에서 요청한 리소스를 제공해주기 때문에 애플리케이션은 받은 사용자 데이터를 가공하여 보호된 서비스 이용 화면을 렌더링하고 12번 사용자에게 보호된 서비스를 제공할 수 있게 됩니다.
[5주차 2차시 09:27] 이렇게 구성된 흐름 덕분에 사용자의 비밀번호는 오직 권한 서버가 제공하는 로그인 화면에서만 쓰이게 되며 애플리케이션은 인가코드와 토큰만을 안전하게 다루게 됩니다.
[5주차 2차시 09:45] 그럼 살펴본 과정을 시퀀스 다이어그램으로 다시 한번 따라가보도록 하겠습니다.
[5주차 2차시 09:52] 사용자가 유저 에이전트, 즉 웹 브라우저를 통해 클라이언트 애플리케이션을 해당하는 웹 서버 또는 클라이언트 애플리케이션 서버로 특정 URL을 접근하게 되면
[5주차 2차시 10:04] 인증 과정이 시작되면서 클라이언트가 권한 서버에 제공하는 로그인 페이지로 리다이렉션을 시킵니다.
[5주차 2차시 10:12] 권한 서버는 사용자가 자격증명을 제출하도록 로그인 UI를 표시하고 사용자가 인증 동의 절차를 마치면 인가 코드를 생성해 클라이언트에 전달합니다.
[5주차 2차시 10:28] 그러면 클라이언트는 이 인가코드를 다시 권한 서버에 제출하면서 액세스 토큰을 발급받습니다.
[5주차 2차시 10:35] 그리고 클라이언트가 받은 액세스 토큰으로 리소스 서버의 보호자원을 요청하고 리소스 서버는 토큰 유효성을 확인한 뒤 최종적으로 요청받는 리소스 데이터를 반환합니다.
[5주차 2차시 10:50] OAuth2 과정에서 중요한 점은 사용자 비밀번호가 권한 서버 밖으로 노출되지 않고 모든 민감 정보 교환은 보안 채널을 통해 이루어진다는 점입니다.
[5주차 2차시 11:07] 그럼 이번에는 한번 OAuth2의 장점과 단점을 한번 알아보겠습니다.
[5주차 2차시 11:13] 먼저 장점부터 나열되어 있는데요.
[5주차 2차시 11:17] OAuth2는 사용자 비밀번호를 애플리케이션에 직접 전달하지 않고 권한 서버에서만 관리되어 하도록 설계해서 비밀번호 노출 위험을 크게 줄여줍니다.
[5주차 2차시 11:29] 또한 한번 로그인하면 여러 애플리케이션에서 동일한 자격을 이용할 수 있는 SSO, 싱글 사인온 기능을 지원하기 때문에 사용자가 무척 편리합니다.
[5주차 2차시 11:42] 토큰 기반 인증 방식을 채택해서 액세스 토큰과 리프레쉬 토큰을 활용하기 때문에 세션 관리와 권한 검증이 효과적으로 이루어지는 장점이 돋보이다 보니
[5주차 2차시 11:52] 토큰의 유효기간을 짧게 운영하면 탈취 사고 발생 시 피해를 최소화할 수 있습니다.
[5주차 2차시 11:59] 그리고 다양한 클라이언트 유형, 웹이나 모바일, API 클라이언트를 유연하게 지원한다는 정도의 장점입니다.
[5주차 2차시 12:10] 이 덕분에 확장성이 뛰어나고 페이스북이나 구글 같은 외부 인증 시스템과 손쉽게 연동할 수 있다는 장점이 있습니다.
[5주차 2차시 12:24] 그럼 이 OAuth는 강력한 권한 위인 메커니즘이지만 그대로 쓰면 몇 가지 취약점, 단점이 있는데요
[5주차 2차시 12:32] 우선 표준 규격상 여러 그랜트 타입과 파라미터, 토큰 발급 및 검증 방식이 나열되어 있기 때문에
[5주차 2차시 12:41] 실제 서비스에서 잘못 구현하면 보안 허점이 생길 수 있습니다
[5주차 2차시 12:45] 특히 모바일 앱이나 싱글 페이지 애플리케이션처럼 클라이언트 시크릿을 안전하게 보관하기 힘든 환경에서는
[5주차 2차시 12:53] 액세스 토큰 탈취 위험이 크고 유효기간이 짧더라도 탈취된 토큰으로 악용될 수 있다는 점을 주의해야 합니다.
[5주차 2차시 13:04] 그리고 표준 해석 차이로 시스템 간 호환성 문제가 발생하기 쉬운데요.
[5주차 2차시 13:09] 따라서 OAuth2를 적용할 때는 기본 흐름 외에도 PKCE라는 중간자 공격을 방어하는 방식을 도입해서 인각 코드 교환을 보호하는 것이 좋고
[5주차 2차시 13:22] 토큰 취소 기능을 구현하여 필요할 때 이전에 발급된 토큰을 즉시 무효화할 수 있어야 하며
[5주차 2차시 13:30] 타임스탬프, 논스 같은 일회용 값을 사용하여 과거 값을 다시 사용하려는 공격을 방어해야 합니다.
[5주차 2차시 13:38] 결국 OAuth2는 기본 제공 기능만으로는 완전하지 않기 때문에 이런 보안 기법들을 함께 갖춰줘야만 실제 상용 운영 환경에서 안전하게 사용할 수 있습니다.
[5주차 2차시 13:55] 지금 보시는 화면은 OAuth와 OAuth2를 주요 3가지 관점, 즉 보안 방식, 구현 복잡성, 그리고 유연성 및 확장성 측면에서 비교한 표입니다
[5주차 2차시 14:10] 먼저 보안 방식을 보면, 구 버전 OAuth는 요청마다 HMAC SHA-1 같은 서명 기반 인증을 사용했습니다
[5주차 2차시 14:19] 클라이언트와 서버가 매번 별도의 서명을 계산하고 검증해야 했기 때문에 운영 부담이 컸고요.
[5주차 2차시 14:27] 반면 OAuth2는 별도의 서명 과정을 없애고,
[5주차 2차시 14:31] 액세스 토큰과 리프레쉬 토큰이라는 토큰만 주고받으면서,
[5주차 2차시 14:35] 전송 보안은 HTTPS 보안 통신 방식에 전적으로 의존하고 있습니다.
[5주차 2차시 14:41] 이를 통해 토큰이 유효한지만 확인하면 되고, 복잡한 암호로 로직이 불필요해졌습니다.
[5주차 2차시 14:49] 다음으로는 구현 복잡성을 보면 기존 OAuth는 서명 생성과 검증 로직 때문에 클라이언트와 서버 모두의 복잡한 암호 모듈이 필요했는데요.
[5주차 2차시 15:00] 그러나 OAuth2에서는 토큰을 발급받아 사용하도록 구조가 단순해져 개발자가 인증 코드를 직접 다루기보다 토큰만 처리하면 되기에 훨씬 구현 난이도가 낮아졌습니다.
[5주차 2차시 15:13] 마지막으로 유연성과 확장성을 살펴보면 두 버전 OAuth는 표준이 다소 엄격하고 확장 가능성이 제한적이었습니다
[5주차 2차시 15:23] 반면 OAuth2는 API, 웹, 모바일 환경을 모두 지원하도록 설계되었으며
[5주차 2차시 15:30] 특히 PKCE와 같은 추가 보안 기능을 쉽게 적용할 수 있습니다
[5주차 2차시 15:36] 따라서 다양한 클라이언트 환경에서도 유연하게 작동할 수 있으며
[5주차 2차시 15:41] 외부 인증 시스템과의 연동이 원활해졌습니다.
[5주차 2차시 15:45] 이 표를 보면 OAuth2가 왜 최신 애플리케이션 환경에서
[5주차 2차시 15:49] 폭넓게 채택되는지를 한눈에 볼 수가 있습니다.
[5주차 2차시 15:58] 그럼 실제 구글 OAuth와 연동하는 것을 실습을 한번 해보도록 하겠습니다.
[5주차 2차시 16:08] 지금부터는 우리 랩 서비스를 구글 OAuth에 연동하여 로그인되도록 수정해보려고 합니다
[5주차 2차시 16:14] 우선 GCP, 즉 구글 클라우드 플랫폼 계정을 하나 확보해야 하는데요
[5주차 2차시 16:19] 슬라이드에 나와있는 링크로 접속하여 가입 절차를 진행하면 됩니다
[5주차 2차시 16:29] 그 다음 구글 클라우드에서는 프로젝트 단위로 API를 관리하기 때문에
[5주차 2차시 16:34] OAuth 인증을 위해 새로운 프로젝트를 생성을 해야 합니다.
[5주차 2차시 16:39] 클라우드 콘솔에서 Set Project 버튼을 누르고 이름을 넣어 생성합니다.
[5주차 2차시 16:49] 그리고 OAuth 인증을 활성화하기 위해서 API 및 서비스 메뉴에서 OAuth 동의 화면을 선택을 합니다.
[5주차 2차시 16:58] 그러면 오른쪽처럼 아직 구성되지 않았을 때의 화면이 나타나 있을 텐데요.
[5주차 2차시 17:05] 시작하기를 눌러서 설정을 시작합니다.
[5주차 2차시 17:12] 그 다음 앱 정보 이름과 사용자 지원용 이메일 주소를 입력을 하는데요.
[5주차 2차시 17:19] 이때는 Gmail 계정을 사용하여야 합니다.
[5주차 2차시 17:22] 그리고 대상 항목에서는 외부를 선택합니다.
[5주차 2차시 17:29] 그리고 마지막으로 개인 이메일 주소를 입력하고 만들기를 눌러주시면 되겠습니다
[5주차 2차시 17:40] 이번에는 인증하러 들어오게 될 웹 클라이언트, 즉 랩 서비스와 관련된 정보를 생성하도록 하겠습니다
[5주차 2차시 17:47] Create Client를 선택을 해서 웹 애플리케이션 유형으로 등록을 하면 되는데요
[5주차 2차시 17:53] 중요한 것은 마지막 그림에 나와있는 승인된 URI 입력입니다.
[5주차 2차시 17:59] 여기에는 승인이 이루어진 후 오토라이제이션 코드를 전달받을 수 있는 링크를 적는데요.
[5주차 2차시 18:06] 관련 내용들은 기본적으로 GET 타입 파라미터로 전달되고, 뒤로 가면 랩 서비스에서 이를 받아들여 사용하도록 소스 코드 작업을 할 것입니다.
[5주차 2차시 18:21] 입력이 끝나면 클라이언트 아이디가 생성된 것을 확인할 수 있습니다
[5주차 2차시 18:31] 그 다음은 OAuth 인증 과정에서 구글 내부 데이터에 액세스할 수 있는 범위를 지정하게 됩니다
[5주차 2차시 18:38] 우리는 이메일, 프로필 정보 등만 활용할 예정이므로 그 부분을 체크하여 지정하도록 합니다
[5주차 2차시 18:51] 다음으로 동작 과정을 테스트하기 위해서 테스트 사용자 정보를 넣어보겠습니다
[5주차 2차시 18:56] 본인 이메일 주소를 넣어주시면 됩니다
[5주차 2차시 19:05] 그럼 원하는 대로 잘 동작하는지 확인해 보겠습니다
[5주차 2차시 19:09] 사용자 인증 정보에서 생성한 웹 클라이언트의 항목을 찾아
[5주차 2차시 19:13] 맨 끝에 있는 다운로드 아이콘을 클릭하면 클라이언트 아이디와 보안 비밀번호를 알 수 있습니다.
[5주차 2차시 19:22] 따로 잘 보관해 둡니다.
[5주차 2차시 19:24] 그리고 슬라이드 아래에 있는 주소를 웹브라우저에서 입력해 보면 되는데 빨간색 글씨 부분을 본인의 클라이언트 아이디 값으로 넣어주면 됩니다.
[5주차 2차시 19:35] 그럼 오른쪽과 같이 익숙한 구글 로그인 창을 볼 수가 있고 구글 계정 중 하나를 클릭을 할 수가 있습니다.
[5주차 2차시 19:43] 이후 랩 서비스에서 이어서 진행해 가지만
[5주차 2차시 19:47] 아직 그쪽 작업은 하지 않았기 때문에
[5주차 2차시 19:50] 현재는 여기까지만 확인할 수 있으면 되겠습니다
[5주차 2차시 19:58] 네 이렇게 구글 쪽 세팅은 완료가 되었고요
[5주차 2차시 20:02] 구글 로그인 창에서 계정을 선택하면
[5주차 2차시 20:08] 계정을 선택하면
[5주차 2차시 20:09] 랩 서비스 쪽으로 전달해주는 정보를 받아서 처리해 보도록 하겠습니다.
[5주차 2차시 20:19] 처리해야 되는 것에는 오토라이제이션 코드가 포함되어 있고요.
[5주차 2차시 20:28] 랩 서비스에서 오토라이제이션 코드를 받으려면
[5주차 2차시 20:32] 정말 구글에서 우리가 설정한 내용에 따라서
[5주차 2차시 20:36] 접속 요청이 들어오는지를 검증할 필요가 있습니다.
[5주차 2차시 20:42] application.properties 환경 파일에
[5주차 2차시 20:48] 발급받았던 클라이언트 아이디 값, 클라이언트 비밀번호, 즉 시크릿 값을 넣어줍니다.
[5주차 2차시 20:54] 아울러 토큰 URI와 그 다음에 토큰 URI 그리고 리소스 URI 그리고 리다이렉트 URI 또
[5주차 2차시 21:08] 이제 여기 나와 있는 것처럼 아까 발급받은 값과 조합해서 작성을 해주시면 되겠습니다.
[5주차 2차시 21:22] 이제 구글에서 로그인이 완료되면 리디렉트 해주는 링크를 받아들일 수 있도록 코드를 추가해 보겠습니다.
[5주차 2차시 21:31] 새로운 경로를 받아들일 수 있도록 로그인 컨트롤러 소스 코드에 붉은 박스로 표시한 부분을 추가합니다.
[5주차 2차시 21:39] Request Mapping Annotation 부분을 살펴보면 Registration ID 변수에는 Google이라는 키워드가 들어간다는 것을 알 수 있습니다.
[5주차 2차시 21:50] 이를 통해 다른 서비스로부터 수신되는 Redirection을 담당한 코드에서 처리할 수도 있습니다.
[5주차 2차시 21:57] 요청이 들어오면 Social Login이라는 서비스 쪽 메소드에서 처리가 이루어집니다.
[5주차 2차시 22:07] 서비스 쪽에 소셜 로그인 메소드도 추가해 보도록 하겠습니다.
[5주차 2차시 22:12] 일단은 정상적으로 수신되는지 확인해 보기 위해 콘솔 출력 코드만 넣었습니다.
[5주차 2차시 22:24] 우리가 만들고 있는 OAuth 관련 URL은 당연히 로그인을 하지 않았더라도 접근이 가능해야 할 것인데요.
[5주차 2차시 22:32] 그래서 이 경로에 대해서는 로그인 인증 검사를 하지 않고도 접근이 가능하도록 처리를 해야 하는데요.
[5주차 2차시 22:42] 로그인 필터 쪽에 작업을 하면 될 것 같습니다.
[5주차 2차시 22:46] 보이는 내용과 같이 해당 경로는 바이패스하도록 간단하게 코드를 추가하였습니다.
[5주차 2차시 22:52] 여기까지 코드 수정이 완료되었다면 서비스를 중단시키고 프로젝트 업데이트 후 다시 서비스를 시작해 봅니다. 준비가 되었다면 그렇게 해서 준비가 되었다면 아까 테스트를 해봤던 URL을 다시 입력해 봅니다.
[5주차 2차시 23:12] 구글 계정 중 하나를 선택하고 확인을 누르면 랩 서비스의 Eclipse 콘솔 창에
[5주차 2차시 23:22] authorization 코드와 구글이라는 키워드가 보일 겁니다.
[5주차 2차시 23:29] 이렇게 되었다면 일단 1차 단계까지는 성공한 것입니다.
[5주차 2차시 23:37] 그럼 이제 잘 수신되고 있는 authorization 코드를 가지고 다시 리소스를 받아올 수 있는 액세스 토큰을 받아보도록 하겠습니다.
[5주차 2차시 23:48] 왼쪽 붉은 박스 안에 나와 있는 것처럼 기존 소셜 로그인 메서드도 수정하고 getAccessToken 메서드도 추가하도록 하겠습니다.
[5주차 2차시 23:59] 환경 변수에 넣었던 내용도 가져와서
[5주차 2차시 24:01] authorization 코드와 함께 http 요청으로 보내
[5주차 2차시 24:05] access token을 받아오는 코드가 되겠습니다.
[5주차 2차시 24:09] 물론 이 과정에 이제 좀 섬세한 예외 처리 과정들이 있어야겠지만
[5주차 2차시 24:17] 지금은 큰 흐름을 이해하는 차원에서 생략되어 있으니
[5주차 2차시 24:22] 감안해 주시기 바랍니다.
[5주차 2차시 24:24] 이 내용을 랩 서비스에 반영해서
[5주차 2차시 24:26] 앞과 동일하게 테스트 URL을 입력을 해보면
[5주차 2차시 24:30] 액세스 코드가 콘솔에 뜨는 것을 볼 수 있을 겁니다.
[5주차 2차시 24:35] 여기까지 완성하면 2차 단계의 성공이라고 말할 수 있습니다.
[5주차 2차시 24:44] 마지막으로 구글 API를 사용할 수 있는 액세스 토큰이 확보되었으니
[5주차 2차시 24:50] 원하는 정보를 가져오면 됩니다.
[5주차 2차시 24:52] 코드를 다시 수정하여 GetUserResource라는 메소드를 추가합니다.
[5주차 2차시 24:59] 메소드 코드를 보면은 HTTP 헤더에 Bearer라는 키워드를 넣고
[5주차 2차시 25:04] 액세스 토큰을 넣는 부분이 확인이 되는데요.
[5주차 2차시 25:08] 그 응답법은 JSON 포맷으로 수신되므로
[5주차 2차시 25:11] ID, 이메일, 닉네임 등을 적절히 추출하여 콘솔에 출력하도록
[5주차 2차시 25:19] 그 부분은 잠시만 이렇게
[5주차 2차시 25:24] 이쪽
[5주차 2차시 25:24] 부분에
[5주차 2차시 25:25] 콘솔에 출력하도록 하고
[5주차 2차시 25:27] 다시 테스트를 해보면 화면 이런
[5주차 2차시 25:33] 식으로
[5주차 2차시 25:34] 정상적으로
[5주차 2차시 25:37] 잘 받아오는 것을 알 수 있습니다.
[5주차 2차시 25:41] 이렇게 이제 3차 단계까지 성공하였고요.
[5주차 2차시 25:49] 원래는 수신받은 정보를 서비스 사용자 정보와 맞춰보면서
[5주차 2차시 25:58] 어떤 계정과 맵핑할지 또는 신규 사용자를 생성해서 등록하는 과정을 거쳐야 합니다.
[5주차 2차시 26:06] 하지만 우리는 이미 존재하고 있는 테스트 계정으로 맵핑해서 로그인되는 것을 체험해 보려고 합니다.
[5주차 2차시 26:13] 이를 위해 화면에 나와 있는 것처럼 컨트롤러와 서비스 소스 코드를 수정을 해봅니다.
[5주차 2차시 26:23] 강제로 테스트 아이디로 연결되어
[5주차 2차시 26:27] 세션 아이디를 바인딩 시켜주면
[5주차 2차시 26:31] J세션 아이디를 바인딩 시켜주면
[5주차 2차시 26:34] 일반 로그인과 동일하게 서비스에서 인식됩니다.
[5주차 2차시 26:43] 그래서 테스트했던 URL을 구글 로그인 버튼으로 만들어서 클릭하게 된다면,
[5주차 2차시 26:49] 구글 계정을 선택한 후 서비스 메인 화면으로 로그인하여 들어갈 수 있습니다.
[5주차 2차시 26:56] 정보 수정 화면으로 이동해보면 이름으로 닉네임이 표시되어 있는 것을 확인할 수 있습니다.
[5주차 2차시 27:06] 물론 데이터베이스 연동 작업은 하지 않았기 때문에 지금 로그인 세션 상에서만 표시되는 것입니다.
[5주차 2차시 27:14] 이렇게 구글 OAuth2 연동 개발 과정을 간단하게 실습해봤는데요.
[5주차 2차시 27:25] 다음으로는 OAuth2의 보안 위협은 어떤 것이 있는지 알아보고 해결 방법도 알아보겠습니다.
[5주차 2차시 27:36] OAuth2는 세 가지의 대표적인 취약점을 가지고 있는데요
[5주차 2차시 27:41] Redirect URI 값은 꼭 제대로 검증하고 처리하지 않으면
[5주차 2차시 27:46] OAuth 인증 과정 중간에 공격자가 끼어들 수 있습니다
[5주차 2차시 27:50] 아울러 스테이트 파라미터라고 지칭하는 것은
[5주차 2차시 27:53] CSRF 방어에 사용하는 랜덤 토큰 같은 것을 말하는데요
[5주차 2차시 27:59] PKCE는 모바일 및 공용 클라이언트에서 오토라이제이션 코드 탈취를 막기 위한 보안 기법입니다.
[5주차 2차시 28:07] 이를 적용하지 않으면 공격자가 오토라이제이션 코드를 탈취하여 다른 클라이언트에서 액세스 토큰을 발급받을 위험이 있습니다.
[5주차 2차시 28:17] 아래의 사례들은 이러한 취약점들을 활용한 특정 공격 기법들입니다.
[5주차 2차시 28:22] 인증 과정에서 끼어들어 Authorization Code 또는 Access Token Client Secret을 탈취하거나
[5주차 2차시 28:30] 이미 사용이 끝났지만 재사용이 가능한 허점을 노린 공격 등이 있습니다.
[5주차 2차시 28:40] 그럼 리소스가 탈취되지 않도록 보호해야 하는 Access Token의 유출 방지 방법들을 알아보겠습니다.
[5주차 2차시 28:47] 우선 당연하게도 암호화된 통신을 사용해야 하고요.
[5주차 2차시 28:52] 쿠키를 쉽게 가져갈 수 있도록 관리하면 안 되겠습니다.
[5주차 2차시 28:56] 그리고 토큰이 어떤 방법으로든 유출될 수 있다고 가정한다면
[5주차 2차시 29:01] 유효기간을 짧게 설정하여 피해를 최소화하는 것이 바람직합니다.
[5주차 2차시 29:07] 또한 새로운 토큰으로 전환할 때에는 유출 확률이 낮은
[5주차 2차시 29:11] 별도의 리프레쉬 토큰을 사용하도록 합니다.
[5주차 2차시 29:15] 만약 유출이 확인되었다면 만료 시간과 무관하게
[5주차 2차시 29:19] 즉시 취소시키는 기능도 준비해두면 좋겠습니다.
[5주차 2차시 29:25] 애플리케이션에서는 크로스사이트 스크립팅 같은 취약점에 사용자가 노출되어
[5주차 2차시 29:30] 세션 정보들을 탈취당하지 않도록 해야 하며
[5주차 2차시 29:32] 앞서 계속 언급했듯이 PKC 메커니즘을 도입하여
[5주차 2차시 29:38] 오토라이제이션 코드 탈취를 방어하는 것을 권장하고 있습니다.
[5주차 2차시 29:44] 이번 차시 요약 정리해보도록 하겠습니다.
[5주차 2차시 29:49] OAuth2는 웹 애플리케이션 인증 및 권한 부여를 위한 개방형 표준 규격임을 우리가 살펴봤고요.
[5주차 2차시 29:58] 액세스 토큰 유출을 방지하기 위해서 HTTPS 적용, 보안 쿠키 사용, 토큰 만료 시간 설정 등의 조치를 취해야 한다.
[5주차 2차시 30:06] 그리고 OAuth2에서 발생할 수 있는 주요 취약점으로는 리디렉트 URI 검증 미흡, 스테이트 파라미터 미사용, PKC 미적용 등이 있다.
[5주차 2차시 30:20] 네,
[5주차 2차시 30:21] 참고문원이고요.
[5주차 2차시 30:26] 이번 차시 수업은 여기까지 하도록 하겠습니다.
[5주차 2차시 30:29] 감사합니다.

# [3-TRANSCRIPT] 5주차 3차시 — 인증과 인가 · OAuth2 · JWT
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · JWT/JSON Web Token/제이더블유티/Claims/클레임/HS256/RS256/Refresh Token/리프레시 토큰 · Refresh Token/리프레시 토큰/토큰 회전/Rotation · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin

[5주차 3차시 00:02] 5주차 3차시의
[5주차 3차시 00:04] 강의 시작하도록 하겠습니다.
[5주차 3차시 00:08] 이번 차시에서는 JWT 인증 및 인가에 대해 알아보도록 하겠습니다.
[5주차 3차시 00:18] 먼저 학습 목표입니다. JWT의 개념과 필요성을 알아보고, JWT 기반으로 인증 과정이 어떻게 흘러가는지도 이해해 보도록 하겠습니다.
[5주차 3차시 00:30] 그리고 JWT가
[5주차 3차시 00:31] 사용되는 과정에 어떤 보안 위협이 발생할 수 있는지, 어떻게
[5주차 3차시 00:36] 해결하면
[5주차 3차시 00:37] 되는지 학습하도록
[5주차 3차시 00:38] 하겠습니다.
[5주차 3차시 00:45] 이에 따른 학습 내용은 다음과 같습니다. JWT의 개념과 그 구현 방법, 보안 위협 및 해결 방법을 알아보도록 하겠습니다.
[5주차 3차시 01:00] 그럼 먼저 JWT가 어떤 것인지에 대해서부터 살펴보도록 하겠습니다.
[5주차 3차시 01:09] JWT는 JSON 웹 토큰의 약자로
[5주차 3차시 01:13] JSON 형식 데이터를 안전하게 주고받기 위해 만들어진 개방형 표준으로
[5주차 3차시 01:18] RFC 7519에 정의되어 있습니다.
[5주차 3차시 01:22] 주로
[5주차 3차시 01:23] 인증과
[5주차 3차시 01:23] 인가 목적으로 사용되며
[5주차 3차시 01:25] 클라이언트와 서버 사이에서 다양한 정보를 주고받을 때 사용합니다.
[5주차 3차시 01:30] 주요
[5주차 3차시 01:31] 특징 중 먼저 자체 포함이라는 특징은 사용자 정보나 만료 시간 등의 데이터를 모두 JWT 안에 담고 있기 때문에
[5주차 3차시 01:39] 서버 쪽에 별도 세션 저장소를 주지 않고도 인증과 인가가 가능하다는 것입니다.
[5주차 3차시 01:47] 예를 들어 사용자가 로그인하면 서버는 사용자 정보를 바탕으로 JWT를 생성해 클라이언트에 전달하고
[5주차 3차시 01:55] 이후 클라이언트가 API를 호출할 때마다 이 토큰을 보내면
[5주차 3차시 02:00] 서버는 토큰 자체만 판별하여 인증과 인가를 처리할 수 있습니다.
[5주차 3차시 02:07] 이 덕분에 서버가 여러 대로 분산되어 있더라도
[5주차 3차시 02:10] 확장성을 손쉽게 확보할 수 있는 것입니다.
[5주차 3차시 02:15] 다음으로는 경량이라는 장점이 있습니다.
[5주차 3차시 02:18] 다시 뒤에 보겠습니다만
[5주차 3차시 02:21] JWT는 헤더, 페이로드, 서명 세 부분을 마침표로 연결하는 형태입니다.
[5주차 3차시 02:30] 헤더와 페이로드는 베이스64 URL 인코딩 방식으로 인코딩이 되는데
[5주차 3차시 02:36] 사실 베이스64 인코딩 자체는 원본보다 크기를 약 33% 증가시키지만
[5주차 3차시 02:43] 일반적인 XML 통신 방식 치고는 구조가 단순하고
[5주차 3차시 02:48] 불필요한 공백이나 태그가 없기 때문에 비교적 작은 편입니다.
[5주차 3차시 02:53] 또한 HTTP 헤더나 URL 파라미터, 쿠키 등에 넣어 전송하기 편리하기 때문에
[5주차 3차시 03:00] 작다기보다는 전송 환경에 적합하도록 간결하게 구성되어 있다고 이해하시면 좋을 것 같습니다.
[5주차 3차시 03:12] 마지막으로는 서명 기능을 통해 토큰 위변조를 방지합니다.
[5주차 3차시 03:18] 헤더에는 어떤 알고리즘으로 서명했는지에 대한 정보가 들어있는데요.
[5주차 3차시 03:23] 여기에 알고리즘 명칭을 적습니다.
[5주차 3차시 03:30] 그리고 페이로드에는 사용자 식별자나 발급자, 발급 시각, 만료 시간 등의 정보가 들어가고
[5주차 3차시 03:38] 마지막으로 비밀키나 개인키를
[5주차 3차시 03:41] 사용해서
[5주차 3차시 03:41] 헤더와 페이로드를 디지털 서명을 생성하게 되는데요.
[5주차 3차시 03:46] 클라이언트가 이를 서버로 보내면 서버는 공개키로 서명을 검증해봐서 토큰 내용이 중간에 바뀌지는 않았는지 실제로 우리가 발급한
[5주차 3차시 03:58] 토큰이 맞는지를 확인할 수 있게 됩니다.
[5주차 3차시 04:01] 중요한 부분만 정리를 다시 한번 해보자면 JWT는 JSON 형식으로 구성되어 인증, 인가 처리에 필요한 데이터를 모두 포함하고 있습니다.
[5주차 3차시 04:13] 또한 베이스64 URL 인코딩 방식으로 되어 있어서 HTTP
[5주차 3차시 04:20] 헤더나 URL 파라미터, 쿠키 등에 넣어 전송할 수 있는 형태로 디지털 서명을 붙여 위변조를 막는 특징을 지닌 토큰이다.
[5주차 3차시 04:30] 이러한 구조 덕분에 요즘 마이크로 서비스나 분산 시스템, 서비스 리스 환경을 비롯해 다양한 서비스에서 인증, 인가용 토큰으로 널리 쓰이고 있습니다.
[5주차 3차시 04:47] 그럼 JWT의 세 가지 구성 요소와 동작 방식을 살펴보겠습니다
[5주차 3차시 04:52] 앞서 간단하게 언급만 했던 내용들인데요
[5주차 3차시 04:56] 먼저
[5주차 3차시 04:58] 헤더에는 이 토큰이 JWT라는 정보와 함께 어떤 알고리즘으로 서명했는지가 포함됩니다
[5주차 3차시 05:06] 예를 들어 HS256을 사용했다면 토큰은 JWT이며
[5주차 3차시 05:12] 서명
[5주차 3차시 05:13] 알고리즘은 뭐다라고 포함하는 메타데이터에 해당하는 것입니다.
[5주차 3차시 05:20] 다음으로 페이로드에는 인증 인가에 필요한 요구사항들 즉 클레임이 들어갑니다.
[5주차 3차시 05:28] 표준 규격상으로는 발급자, 주체, 사용자 아이디, 만료 시간 같은 항목이 있지만
[5주차 3차시 05:35] 필요에 따라 서비스 내 역할이나 권한 같은 커스텀 클레임을 추가할 수가 있습니다
[5주차 3차시 05:41] 서버는 페이로드를 보고 JWT의 사용자는 누구이고 언제까지 유효한지 등을 판단합니다
[5주차 3차시 05:50] 마지막으로
[5주차 3차시 05:52] 서명은 헤더와 페이로드를
[5주차 3차시 05:55] 헤더.페이로드 형식으로 연결한 뒤 비밀키 또는 개인키로 암호화해서 생성하는데요
[5주차 3차시 06:01] HMAC 샤256 방식으로 해시값을 만든 다음 이를 다시 인코딩하여 서명 부분을 완성합니다
[5주차 3차시 06:09] 이렇게 하면 서버는 토큰을
[5주차 3차시 06:12] 받을 때마다
[5주차 3차시 06:12] 붙어있는 서명을 검증해서
[5주차 3차시 06:14] 헤더와 페이로드가 중간에 변조되지 않았는지
[5주차 3차시 06:18] 만료 시간이 지났는지를 확인할 수 있습니다.
[5주차 3차시 06:22] 요약해보면 헤더는 이 토큰이 JWT이고
[5주차 3차시 06:27] HS 알고리즘으로 서명했다는 정보가 들어있고
[5주차 3차시 06:31] 페이로드는 누가 발급받았는지 언제 만료되는지 어떤 권한이 있는지 담고 있다.
[5주차 3차시 06:39] 그리고 마지막에 붙어있는 서명은
[5주차 3차시 06:41] 헤더와
[5주차 3차시 06:43] 페이로드를 합쳐 HMAC, SHA, 256 등으로 암호화가 되어 있으며 이를 활용해 위변조 여부를 검증하는 데 활용이 된다.
[5주차 3차시 06:52] 그리고 이 세 부분은 점으로 연결된 하나의 문자열로 구성되는데 클라이언트는 로그인 시 JWT를 발급받은 후 발급된 JWT를 요청할 때마다 서버에 보내고
[5주차 3차시 07:05] 서버는 JWT 내부의 세 부분을 검증해서 빠르고 안전하게 인증 인가 처리를 할 수 있게 됩니다.
[5주차 3차시 07:19] JWT를 사용하면
[5주차 3차시 07:20] 서버가 별도의 세션 정보를 보관하지 않아도 된다는 점에서 매우 편리한데요.
[5주차 3차시 07:26] 로그인 시점에서 사용자 정보와 만료 시간, 필요한 권한 등을 모두 토큰 안에 담아 만들기 때문에
[5주차 3차시 07:33] 이후 요청이 들어올 때마다 서버는 클라이언트가 전송한 토큰만 검증하면 됩니다.
[5주차 3차시 07:40] 즉 매번 데이터베이스에 접속하거나 외부 저장소를 조회하지 않고도
[5주차 3차시 07:46] 이 토큰이 진짜인지 만료되지는 않았는지를 빠르게 확인할 수 있어서
[5주차 3차시 07:51] 요청량이 많은 서비스에서도 안정적인 인증 처리가 가능하죠.
[5주차 3차시 07:56] 또한 JWT는 헤더에, 이 토큰은 JWT이고 HS256 방식으로 설명했다는 정보를 담고 있고
[5주차 3차시 08:07] 페이로드의 발급자, 주체, 만료 시간 같은 표준 클레임을 포함시키는데요
[5주차 3차시 08:12] 여기에 서비스 애플리케이션이 필요로 하는 역할이나 권한 같은 추가 정보를
[5주차 3차시 08:19] 커스텀 클레임 형태로 자유롭게 넣을 수 있습니다
[5주차 3차시 08:22] 이걸 활용하면 개발자는
[5주차 3차시 08:25] 요청이
[5주차 3차시 08:25] 들어올 때마다
[5주차 3차시 08:26] 매번 권한을 조회하는 로직을 구현하지 않아도 되고
[5주차 3차시 08:29] 페이로드만 확인하면 곧바로
[5주차 3차시 08:32] 해당
[5주차 3차시 08:33] 사용자가 어떤 권한을 가지고 있는지 판단할 수 있습니다.
[5주차 3차시 08:38] JWT는 RFC 7519라는
[5주차 3차시 08:40] 공식 규격이라서
[5주차 3차시 08:43] Spring Boot, Node.js, .NET 등 다양한 프로그래밍 언어와
[5주차 3차시 08:48] 플랫폼에서 별도의 커스터마이징 없이 그대로 사용할 수 있습니다.
[5주차 3차시 08:54] 그래서 마이크로 서비스나 서버리스 환경처럼 여러 시스템이 뒤섞여 연동하는 구조에서도 상호 호환성이 뛰어나기 때문에 인증 인가 토큰으로 널리 활용되고 있습니다.
[5주차 3차시 09:11] 이번에는 JWT를 사용할 때 주의할 점, 단점을 한번 빠르게 짚어보도록 하겠습니다.
[5주차 3차시 09:18] 먼저 페이로드에 담긴 데이터는 베이스64URL 인코딩으로 전달되나 누구나 쉽게 디코딩할 수 있어서 민감 정보를 포함해서는 안되겠습니다.
[5주차 3차시 09:31] 꼭 필요한 사용자 식별자와 권한 정보만 담아야 하고 탈취되지 않도록 HTTPS를 사용해야 합니다.
[5주차 3차시 09:40] 다음으로 한번 발급된 토큰은 만료 전까지 서버에서 즉시 무효화하기 어렵습니다.
[5주차 3차시 09:46] 로그아웃 시점에도 이미 발급된 토큰은 유효함으로
[5주차 3차시 09:50] 즉시 차단하려면 블랙리스트를 운영하거나 유효기간을 적절히 설정해야 합니다
[5주차 3차시 09:57] 하지만 또 유효기간을 너무 짧게 설정하면
[5주차 3차시 10:00] 사용자가 자주 재로그인해야 돼서 불편하고
[5주차 3차시 10:04] 너무 길게 설정하면 탈취된 토큰으로 오랫동안 공격받을 위험이 있겠죠
[5주차 3차시 10:10] 그리고 서버간 시간이 맞지 않으면 문제가 발생할 수 있으므로
[5주차 3차시 10:15] 모든 서버의 시계를 정확히 동기해야 되는 문제도 있습니다.
[5주차 3차시 10:21] 또한 JWT는
[5주차 3차시 10:22] 일반
[5주차 3차시 10:22] 세션 아이디보다 크기가 커서
[5주차 3차시 10:25] 매 요청 시 HTTP 헤더에 포함하면 네트워크 오버헤드가 늘어나는 단점이 있습니다.
[5주차 3차시 10:32] 특히 모바일 환경에서는 대역폭 부담이 커짐으로
[5주차 3차시 10:35] 페이로드를 가능한 한 간결하게 유지해야 합니다.
[5주차 3차시 10:43] 네, 그러면 이제 다음 그림을 보면 로그인 성공 후 서버는
[5주차 3차시 10:54] 로그인 성공 후 서버는 JWT 형식의 액세스 토큰과 리프레쉬 토큰을 생성을 합니다.
[5주차 3차시 11:01] 액세스 토큰에는 사용자 식별자와 권한 정보가 들어가서 서비스 이용 시 사용하게 되는데요.
[5주차 3차시 11:09] 리프레쉬 토큰은 액세스 토큰이 만료되었을 때 새로운 토큰을 발급받기 위해 사용합니다.
[5주차 3차시 11:16] 서버는 로그인 응답에 이 두 토큰을 담아 클라이언트로 보내고 클라이언트는 로컬 스토리지나 쿠키에 저장해두게 되는 것이죠.
[5주차 3차시 11:26] 이후 클라이언트는
[5주차 3차시 11:27] API를 호출할 때 요청 데이터에 베어러를 적고 액세스 토큰을 넣는 형식으로 Java 웹 토큰을 함께 전송하게 됩니다.
[5주차 3차시 11:36] 서버는 받을 때마다 서병을 검증해 토큰이 유효한지 확인한 다음
[5주차 3차시 11:42] 필요한 데이터를
[5주차 3차시 11:44] 제공합니다
[5주차 3차시 11:44] 만약 액세스 토큰이 만료되었다면
[5주차 3차시 11:47] 서버는 만료되었음을 알려주게 되고
[5주차 3차시 11:50] 클라이언트는 저장해둔 JWT 리프레쉬 토큰을 사용하여
[5주차 3차시 11:54] 새로운 액세스 토큰 발급을 요청합니다
[5주차 3차시 11:58] 이 모든 통신은 반드시 HTTPS로 보호되어야 하고
[5주차 3차시 12:03] 클라이언트는 액세스토큰의 만료기간을 참고해 자동갱신 로직을 구현해야 안전하게 운영할 수 있습니다.
[5주차 3차시 12:16] 그럼
[5주차 3차시 12:17] 다시
[5주차 3차시 12:18] 한번 서버가
[5주차 3차시 12:18] JWT를 활용해 사용자 권한을 어떻게 관리하는지 살펴보겠습니다.
[5주차 3차시 12:23] 우선 JWT 페이로드에는 사용자를 식별하기 위한 클레임과 함께
[5주차 3차시 12:29] 역할이나 권한 같은 정보가 담겨 있습니다.
[5주차 3차시 12:34] 클라이언트는 로그인 과정에서 발급받은 JWT를
[5주차 3차시 12:38] HTTP 헤더에 포함시켜 사용합니다.
[5주차 3차시 12:42] 그리고 서버는 요청을 받을 때마다 먼저
[5주차 3차시 12:46] JWT의 서명, 만료 시간, 그리고 발급자 정보를 검증하여
[5주차 3차시 12:52] 토큰의 무결성과 유효성을 확인합니다
[5주차 3차시 12:56] 검증에 문제가 없으면 페이로드 안에 클레임을 읽어
[5주차 3차시 13:00] 이 사용자가 누구이고 해당 API를 호출할 권한이 있는지를 즉시 판단을 합니다
[5주차 3차시 13:07] 예를 들어 역할값이 admin이라고 하면 관리자 전용 API를 허용하고
[5주차 3차시 13:14] 유저라면 일반 사용자 전용 리소스만 제공을 합니다
[5주차 3차시 13:18] 이 과정은 별도 세션 저장소 없이 JWT 정보만으로 이루어지기 때문에 무상태의 아키텍처를 유지할 수 있게 하며 특히 분산 시스템이나 마이크로 서비스 환경에서 효율적입니다.
[5주차 3차시 13:33] 마지막으로 짧은 만료 시간을 설정해 권한
[5주차 3차시 13:36] 변경이
[5주차 3차시 13:36] 이루어질 때에도 빠르게 반영되도록 하고 만료된 액세스 토큰은 리프레쉬 토큰을 통해 새로운 토큰을 발급받는 토큰 회전 전략을 사용합니다.
[5주차 3차시 13:48] 이를 통해 오래된 권한 정보를 가진 토큰이 계속 사용되는 것을 방지할 수 있습니다.
[5주차 3차시 14:00] 이번엔
[5주차 3차시 14:01] 앞서 이야기한 내용을 토대로 JWT 인증 설계 시 고려할 내용입니다.
[5주차 3차시 14:12] 첫째,
[5주차 3차시 14:13] 토큰이 발급된 후에 클레임이 고정되어 권한을 변경해도 즉시 반영되지 않습니다.
[5주차 3차시 14:20] 예컨대 관리자가
[5주차 3차시 14:21] 권한을
[5주차 3차시 14:22] 일반 사용자로 낮추더라도 기존에 발급된 토큰은 여전히 관리자 권한을 유지합니다.
[5주차 3차시 14:28] 이를 해결하려면 토큰 유효기간을 짧게 설정하거나 강제로 로그인으로 리프레시하거나
[5주차 3차시 14:37] 매 요청마다 중앙 인간 서버로 실시간 권한을 확인하겠습니다.
[5주차 3차시 14:48] 두 번째는 전송 저장 단계 보안입니다.
[5주차 3차시 14:53] 토큰은 반드시
[5주차 3차시 14:54] HTTPS로 전송해야 하고
[5주차 3차시 14:56] 클라이언트는 HTTP Only 또는 CQ 속성이 적용된 쿠키에 저장해서
[5주차 3차시 15:03] 크로스 사이트 스크립팅 공격을 방지를 해야 합니다.
[5주차 3차시 15:08] 또한 페이로드에는 최소한의 권한 정보만 담고
[5주차 3차시 15:12] 민감 데이터는 포함하지 않아야 하겠습니다.
[5주차 3차시 15:17] 이렇게 설계한다면 JWT의 장점을 살리면서 보안 위험을 줄일 수 있습니다.
[5주차 3차시 15:30] 그럼 실제 JWT 구현 과정을 실습을 통해 알아보도록 하겠습니다
[5주차 3차시 15:42] 실습 방법에 대해 요약해 보겠습니다
[5주차 3차시 15:47] 우선 앞서 스프링부트 프로젝트 생성 실습을 했었던
[5주차 3차시 15:52] 헬로우 스프링부트 프로젝트를 활용해 보려고 하는데요
[5주차 3차시 15:55] 이 프로젝트에 JWT 인증 기능의 코드들을 추가해 보면서
[5주차 3차시 16:00] 전체 흐름을 이해해 보려고 합니다
[5주차 3차시 16:04] 앞으로 이제 액세스 토큰과 리프레쉬 토큰을 생성하는 과정과
[5주차 3차시 16:09] 검증하는 과정, 리프레쉬 토큰을 활용한 재발급 과정까지
[5주차 3차시 16:13] 하나씩 실습해 보도록 하겠습니다.
[5주차 3차시 16:20] 그럼 먼저 화면에서처럼 form.pom.xml 파일에
[5주차 3차시 16:30] jjwt api, jjwt
[5주차 3차시 16:34] impl, jjwt jackson 의존성 디펜던시를 추가합니다.
[5주차 3차시 16:40] API에는
[5주차 3차시 16:42] JWT 생성 검증을 위한 기본 인터페이스를 제공하고
[5주차 3차시 16:47] INPL은 실제 서명 알고리즘을 구현하며
[5주차 3차시 16:51] Jackson은 토큰을 JSON 형태로 처리하는 기능을 담당합니다
[5주차 3차시 16:57] 이 세 가지 라이브러리를 포함시키면
[5주차 3차시 17:00] Spring Boot 프로젝트에서 쉽게 JWT를 생성하고 파싱할 수 있게 됩니다
[5주차 3차시 17:11] 이제 JWT 컨트롤러 소스 코드의
[5주차 3차시 17:15] 첫
[5주차 3차시 17:16] 부분을 살펴보겠습니다
[5주차 3차시 17:19] JWT 컨트롤러 클래스에서는 비밀키와
[5주차 3차시 17:23] 토큰 만료 시간 값을 상수로 선언해야 합니다
[5주차 3차시 17:27] 그리고 비밀키는 임의로 문자율을 정해서 설정할 수 있고
[5주차 3차시 17:31] 액세스 토큰 만료 시간을 10분, 리프레시 토큰 만료 시간을 30분으로 지정합니다.
[5주차 3차시 17:38] 실제 운영 환경에서는 리프레시 토큰 만료 시간을
[5주차 3차시 17:42] 일주일 정도로 길게 잡는 것이 보완적으로 좋습니다.
[5주차 3차시 17:46] 여기 나와 있는 코드에서는 테스트 목적으로 랜덤 키를 생성하여 사용하고 있으므로
[5주차 3차시 17:52] 서비스가 실행될 때마다 다른 값으로 지정될 것입니다.
[5주차 3차시 17:57] 이 비밀키는 토큰을 서명할 때 사용되며
[5주차 3차시 18:00] 절대로
[5주차 3차시 18:01] 외부에 노출하면 안됩니다.
[5주차 3차시 18:04] 만료 시간 상수는 각 토큰이 언제 만료하는지를 결정하는 기준이므로
[5주차 3차시 18:09] 서비스 요구사항에 맞춰서 적절히 설정해야 합니다.
[5주차 3차시 18:14] 이렇게 선언된 상수는 이후 토큰을 생성하거나 검증할 때 재사용됩니다.
[5주차 3차시 18:25] 첫 번째로 구현하는 slash.jwt slash.generate.endpoint는 로그인 정보를 받으면 사용자 인증 로직을 통해 유효성을 검사합니다
[5주차 3차시 18:36] 인증이 성공하면 JWTS 빌더로 액세스 토큰을 만드는데요
[5주차 3차시 18:42] Set Subject로는 사용자 아이디를, Claim Role로는 권한을 설정합니다
[5주차 3차시 18:49] 그 다음에 set expiration으로는 access token 만료 시간을 10분으로 지정한 뒤
[5주차 3차시 18:58] 그 다음에 sign with 파라미터로 시크릿 키를 받아서 서명하고 컴팩트로 토큰 문자열을 완성합니다.
[5주차 3차시 19:09] refresh token은 refresh token expiration에 따라 30분으로 동일하게 생성한 뒤
[5주차 3차시 19:16] 두 토큰을 제이슨 형태로 묶어 클라이언트에 반환하는데요.
[5주차 3차시 19:22] 토큰 타입으로 리프레쉬를 적어뒀습니다.
[5주차 3차시 19:30] 두 번째는 slashjwt slashverify endpoint입니다.
[5주차 3차시 19:37] 클라이언트가 보내온 액세스 토큰을 검사하는 역할을 합니다.
[5주차 3차시 19:46] 요청시 토큰 값을 파라미터로 받고 JWTS.passer를 호출하여 SetSignIn키로
[5주차 3차시 19:54] 서명을 검증한 후 PassClaim.jws를
[5주차 3차시 20:04] 사용해 페이로드를 파싱합니다.
[5주차 3차시 20:08] 서명 검사와 만료 시간 검증을 모두 통과하면 페이로드 안에 클레임에서 사용자 정보와 권한을 읽은 뒤 성공 응답을 반환합니다
[5주차 3차시 20:20] 만약 서명 검증에 실패하거나 토큰이 이미 만료된
[5주차 3차시 20:25] 경우라면 서버는 401 Unauthorized 상태 코드를 반환하며 접근을 거부합니다
[5주차 3차시 20:39] 슬래시 JWT 리프레쉬 엔드포인트는 클라이언트가 보낸 리프레쉬 토큰을 받아서 새로운 액세스 토큰을 발급합니다.
[5주차 3차시 20:49] 요청 파라미터로 전달된 리프레쉬 토큰을 JWTS.passer로 offset signing키로
[5주차 3차시 20:56] 검증
[5주차 3차시 20:56] 후 passclaim JWS로 또 페이로드를 파싱합니다.
[5주차 3차시 21:01] 서명과 만료 시간이 모두 유효하면 페이로드에서 사용자 정보와 역할을 추출을 해서 JWTS 빌더로 새로운 액세스토큰을 생성합니다.
[5주차 3차시 21:12] 이후 HS256 Sign With 호출 후 컴팩트로 이제 최종 문자열을 완성을 합니다.
[5주차 3차시 21:27] 생성된 액세스 토큰은 맵에 담아
[5주차 3차시 21:30] 제이슨
[5주차 3차시 21:30] 형태로 클라이언트에 반환하며
[5주차 3차시 21:32] 인증에 실패하면 마찬가지로 401 Unauthorized 코드를 응답합니다
[5주차 3차시 21:42] 구현된 JWT 기능이 제대로 동작하는지 액세스 토큰 발급 과정을 확인해 보겠습니다
[5주차 3차시 21:49] 일단 실제 운영 환경에서는 사용자 인증에 성공한 사용자에
[5주차 3차시 21:54] 대해서만
[5주차 3차시 21:54] 토큰이 발급되도록 구현해야 한다는 것은 알아두시고요.
[5주차 3차시 21:59] 웹 브라우저에서 localhost 8080 JWT Generate을 입력을 하면 토큰을 발급해 볼 수가 있습니다.
[5주차 3차시 22:10] 호출이 성공하면 서버는 JSON 형식으로 액세스 토큰, 리프레쉬 토큰을 반환을 해주는 걸 볼 수가 있습니다.
[5주차 3차시 22:16] 이때 파이어폭스 브라우저를 사용한다면 결과 화면 우측 상단의 원시값
[5주차 3차시 22:23] 보기 메뉴를
[5주차 3차시 22:24] 선택하여 토큰 전체 문자열을 확인하실 수 있습니다.
[5주차 3차시 22:33] 다음으로는 액세스 토큰 유효성 확인 과정을 테스트해 보겠습니다.
[5주차 3차시 22:37] 웹브라우저 주소 창에 localhost8080jwt-verify에
[5주차 3차시 22:44] 앞서
[5주차 3차시 22:46] 발급받은
[5주차 3차시 22:47] 액세스
[5주차 3차시 22:47] 토큰 값을 파라미터로 넣어
[5주차 3차시 22:49] 요청합니다.
[5주차 3차시 22:51] 요청이 들어오면 앞서 소스코드에서 작성했듯이 서버는 jwts 파서로 set-signing 키를 사용해 토큰 서명을 검증합니다.
[5주차 3차시 23:02] 서명
[5주차 3차시 23:04] 검사 이후에는 페이로드에 담긴 클레임을 통해 만료 여부를 확인하고요
[5주차 3차시 23:09] 두 검증이 모두 통과되면 서버는 페이로드 안에 사용자 정보, 역할 같은 클레임 정보를 제이슨 형식으로 반환합니다
[5주차 3차시 23:18] 하지만 서명 검증에 실패하거나 토큰이 이미 만료된 경우에는
[5주차 3차시 23:23] 서버가 HTTP 400번 배드 리퀘스트와 응답과 함께
[5주차 3차시 23:29] 에러 메시지를 반환을 하는 것을 확인할 수 있습니다.
[5주차 3차시 23:35] 이 기능으로 액세스 토큰이 유효한지
[5주차 3차시 23:43] 그리고 페이로드에 담긴 클레임 값이 올바른지 확인할 수 있습니다.
[5주차 3차시 23:53] 마지막으로 리프레쉬 토큰 회전 기능 테스트해 보겠습니다
[5주차 3차시 23:56] 웹브라우저 주소창에 로컬호스트 8080-JWT-Refresh 입력하면
[5주차 3차시 24:05] 리프레쉬 토큰 값을 파라미터로 넣고 요청을 합니다
[5주차 3차시 24:09] 이전 소스 코드 작성한 것처럼 서버는 JWTS 파서 사용해서 Set Sign-in 키로 토큰 서명 검증하고
[5주차 3차시 24:19] 만료 시간 해서 유효 여부 판단을 합니다.
[5주차 3차시 24:24] 그래서 이 리프레쉬 토큰이 유효하면 페이로드 안에 사용자 정보와
[5주차 3차시 24:29] 역할을 읽어서
[5주차 3차시 24:29] 새로운 액세스 토큰을 생성을 하고요.
[5주차 3차시 24:33] 필요하다면 리프레쉬 토큰도 같은 방식으로 재발급할 수 있겠죠.
[5주차 3차시 24:37] 새 액세스 토큰과 리프레쉬 토큰은 제이슨 형태로 반환이 됩니다.
[5주차 3차시 24:43] 이 역시 검증 실패 혹은 만료되었다면 400번 응답 함께 에러 메시지를 반환합니다.
[5주차 3차시 24:58] 그럼 마지막으로 JWT의 취약점과 이 취약점에 대응하는 방법 살펴보고 마치도록 하겠습니다.
[5주차 3차시 25:08] JWT는 서명은 헤더와 페이로드가 변두되지 않았음을 확인하여
[5주차 3차시 25:14] 토큰 무결성을 보장합니다
[5주차 3차시 25:16] 서명 알고리즘에는
[5주차 3차시 25:18] 대칭키 방식인 ACS256-384-512
[5주차 3차시 25:22] 비대칭키
[5주차 3차시 25:24] 방식인 RS256-384-512, ES256 등이 있습니다
[5주차 3차시 25:30] 대칭키 방식은 동일한 비밀키로 서명과 검증을 수행하고
[5주차 3차시 25:35] 비대칭키 방식은 개인키로 서명 후 공개키로 검증하는 방식입니다.
[5주차 3차시 25:41] 서명 생성 과정은 앞서 설명했듯이
[5주차 3차시 25:44] 헤더와 페이로드를 Base64 URL 인코딩하고
[5주차 3차시 25:48] 헤더점 페이로드 형태로 결합한 다음에
[5주차 3차시 25:52] 비밀키 또는 개인키 디지털로 이제 서명, 디지털 서명 생성하고
[5주차 3차시 26:05] JWT 키 관리에서 가장 먼저 고려해야 될 공격 방식은 알고리즘 혼동 공격입니다.
[5주차 3차시 26:14] 공격자가 토큰헤더의 알고리즘 값을 일부러 이미 값으로 바꿔서 서명
[5주차 3차시 26:20] 검증을
[5주차 3차시 26:20] 오해할 수 있으므로
[5주차 3차시 26:21] JWTS 파서 설정 시 반드시 HS256, RS256 등만 허용하도록 지정해야 합니다.
[5주차 3차시 26:31] 다음은 키 유출 위험입니다.
[5주차 3차시 26:34] 시크릿 키나 개인 키를 코드에 하드코딩하지 않고
[5주차 3차시 26:38] HSM이나 클라우드 키 관리 서비스에 안전하게 보관해야 합니다.
[5주차 3차시 26:44] 환경변수나 키 저장소를 사용할 경우에는 최소 권한으로
[5주차 3차시 26:48] 설정해
[5주차 3차시 26:49] 외부 노출을 방지해야 합니다.
[5주차 3차시 26:52] 마지막으로 키 회전 정책을 구현을 해야 하는데요.
[5주차 3차시 26:58] 신규 키를 도입할 때는 새로운 키와 이전 키를 동시에 허용하고
[5주차 3차시 27:02] 일정 기간이 지난 뒤에는 이전
[5주차 3차시 27:05] 키를 폐기해서
[5주차 3차시 27:06] 오래된 토큰이 더 이상 유효하지 않도록 해야 합니다.
[5주차 3차시 27:14] 이번에는 그래서 토큰의 유효기간이 보안에 어떤 영향을 미치는지 살펴보겠습니다.
[5주차 3차시 27:20] 우선 유효기간은 토큰이 발급된 시점으로부터 언제 만료될지를 결정하게 되는데요.
[5주차 3차시 27:27] 만료 시점이 지나면 해당 토큰은 즉시 무효화됩니다.
[5주차 3차시 27:32] 따라서 유효기간을 짧게 설정하면 토큰
[5주차 3차시 27:36] 탈취 사고가 발생하더라도 피해 범위를 줄일 수 있습니다.
[5주차 3차시 27:40] 반면에
[5주차 3차시 27:41] 너무 짧게 설정하면 사용자가 자주 재인증을 해야 해서 매우 불편할 수 있으니
[5주차 3차시 27:47] 어떤 서비스를 하는지 그 성격에 맞춰서 적절한 균형을 찾아야 하겠습니다.
[5주차 3차시 27:55] 그 균형이라고 하면 예를 들어서 금융 서비스처럼 민감도가 높은 경우에는 짧게 설정하고
[5주차 3차시 28:03] 일반 웹브라우저에서는 상대적으로 긴 유효기간을 설정하면 되겠습니다.
[5주차 3차시 28:08] 마지막으로 서버 간 시간 동기화가 맞지 않으면 만료 시점 검증에 오차가 발생할 수 있으므로
[5주차 3차시 28:16] 모든 서버의 시각을 정확히 동기화하는 것이 중요하겠습니다.
[5주차 3차시 28:24] 다음으로는
[5주차 3차시 28:25] JWT 탈취 방어 방법 살펴보겠습니다.
[5주차 3차시 28:29] 토큰 탈취는
[5주차 3차시 28:30] 주로
[5주차 3차시 28:30] 크로스 사이트 스크립팅 공격이나
[5주차 3차시 28:32] 불안전한 저장소 사용, 패키 스니핑 등에서 이 탈취가 발생을 하는데요.
[5주차 3차시 28:38] 예를 들어 클라이언트가 로컬 스토리지에 액세스 토큰을 보관한다면
[5주차 3차시 28:42] 실수로
[5주차 3차시 28:44] 크로스 사이트 스크립팅 취약점이 있는 웹페이지를 방문할 경우에
[5주차 3차시 28:48] 공격자가 자바스크립트로 해당 토큰을 바로 탈취를 할 수가 있겠죠.
[5주차 3차시 28:54] 이러한 위협으로부터 방어하려면 크로스 사이트 스크립팅 방어를 위해서
[5주차 3차시 28:58] CSP 즉 콘텐츠 보안 정책을 적용시켜 인라인 스크립트 실행을 제한하고
[5주차 3차시 29:05] HTTP Only, 시큐어 속성 등이 적용된 쿠키의 토큰을 저장하여
[5주차 3차시 29:11] 토큰 교환 과정은
[5주차 3차시 29:13] 모두
[5주차 3차시 29:14] HTTPS로 전송만 사용하도록 합니다.
[5주차 3차시 29:22] 마지막 차시 강의 내용 정리해 보도록 하겠습니다.
[5주차 3차시 29:26] JWT는 인증과 인가를 위해 널리 사용되는 유용하고 강력한 도구이지만
[5주차 3차시 29:32] 서명 검증, 뉴욕이간 관리, 키 보호 등을 확실하게 해야 한다.
[5주차 3차시 29:38] 아울러 JWT의 내용은 암호화되어 있지 않으므로
[5주차 3차시 29:42] 민감한 정보가 포함되지 않아야 하며
[5주차 3차시 29:47] 리프레쉬 토큰을 활용하여 인증이 유지되는 동안
[5주차 3차시 29:50] 토큰을 계속 바꿔주고 보관되어 있는 토큰이 탈취되지 않도록
[5주차 3차시 29:55] 탈취
[5주차 3차시 29:57] 방어
[5주차 3차시 29:57] 방법을 적용해서 관리해야 한다
[5주차 3차시 30:04] 참고 문헌이고요
[5주차 3차시 30:07] 5주차 강의 그리고 3차시 강의 여기까지 하도록 하겠습니다
[5주차 3차시 30:13] 감사합니다

