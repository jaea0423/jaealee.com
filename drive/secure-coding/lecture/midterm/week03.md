# WEEK03 — 3주차 Spring Boot 개발 환경·실습 (시큐어코딩 중간고사 주차 묶음)

> 이 파일 하나에 3주차의 교안 퀴즈(1-QUESTIONS, 신뢰도 A) · 정리(4-NOTES, C~D) · 교안 원문(2-SLIDES, A) · 강의 발화(3-TRANSCRIPT, B)가 모두 있다.
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

---

# [4-NOTES] 3주차 관련 정리 (신뢰도 C~D) — 교안·발화가 다른 지점. 시험 답은 교안 우선.

## [4-NOTES] 3주차 1차시 · Firefox 포트 — 발화/교안 차이 (C)
키워드: Spring Boot, 포트, 8081, 8082, Firefox
- [3주차 1차시 13:55]: 파이어폭스 프록시 포트를 "8082"라고 함. [2-SLIDES] 3주차 1차시 p.19·p.17: 8081(맞음). 실습 프록시 포트는 교안 기준 8081.

## [4-NOTES] 3주차 3차시 · 퀴즈 1 보기 정의 — 보기 2도 애매 (C)
키워드: Spring, DTO, Service, 계층, 퀴즈
- [1-QUESTIONS] 3주차 3차시 퀴즈 1("계층별 설명이 잘못된 것은?"): 교안 정답은 4) Service - 화면 UI 처리 로직.
- 보기 2) "DTO - 데이터 엔티티 모델링"도 엄밀히는 맞지 않음(DTO는 계층 간 데이터 전달 객체, 엔티티 모델링은 Entity/Domain). 시험은 교안 정답(4번)으로 답하고, "DTO = 엔티티 모델링"을 맞는 설명으로 고르는 보기는 피할 것.

## [4-NOTES] 공통 · 자동 전사 한계 (C)
키워드: 녹취, 자동 전사, 불명확, 음성 인식
- 3-TRANSCRIPT는 자동 전사라 영문 용어·숫자·포트·메서드명에 오인식이 있을 수 있음([불명확]·[표현 차이] 표시). 숫자·코드·정확한 용어는 2-SLIDES(교안)를 우선.
- 6·7주차 녹취는 화면 기록이 없어 교수님 펜 강조 위치를 알 수 없음. 7주차는 1차시 앞부분(시험 안내)과 3차시 중간에 무음 구간이 있어 누락 가능.

## [4-NOTES] 시험 안내 (B, 발화 근거)
키워드: 중간고사, 시험, LMS, 온라인, 범위
- [7주차 1차시 00:00] 발화: 8주차에 중간고사, LMS 온라인 실시간, 공지사항 확인 요망. 범위는 "오늘까지 수업 내용"(1~7주차).
- 시험 규정(사용자 확인): 2026-10-22(목) 19:00~20:00, 온라인 LMS 퀴즈, AI·오픈북 가능, 범위 1~7주차. 날짜·시간은 LMS 공지로 최종 확인.

---

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

---

# [3-TRANSCRIPT] 3주차 1차시 — Spring Boot 개발 환경·실습
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure

[3주차 1차시 00:02] 안녕하세요.
[3주차 1차시 00:04] 시큐어 코딩 3주차 강의 시작하도록 하겠습니다. 첫 번째 차시에서 설명드릴 내용은 시큐어 코딩 학습에 필요한 실습 환경 구축과 웹 환경에 대한 배경 지식 및 데이터 인코딩과 관련된 내용입니다.
[3주차 1차시 00:26] 우선 배포해드린 랩 프로젝트 구조에 대한 이해와
[3주차 1차시 00:31] 실습 환경을 셋업하고 이를 로컬에 구축해보도록 하겠습니다. 그리고 웹의 구조와 HTTP 통신 방식에 대해 자세히 알아보고, 베이스64 URL 인코딩 및 디코딩이란 무엇이고 어디에 활용하는지 알아보겠습니다.
[3주차 1차시 00:51] 이에 따른 학습 내용입니다. 랩 프로젝트를 활용하여 웹 서비스 구동을 주제로 학습을 진행하겠습니다. 웹 서버 애플리케이션 서버,
[3주차 1차시 01:02] 데이터베이스가 어떻게 연결되어 동작하는지 구조를 이해하고 실제로 HTTP 요청과 응답이 어떤 방식으로 이루어지는지 살펴보도록 하겠습니다.
[3주차 1차시 01:15] 또한 베이스64와 URL 인코딩 개념을 통해 웹 데이터 전달의 기초 원리를 익히고 이를 바탕으로 실습 환경에서 직접 서비스를 실행해 보겠습니다.
[3주차 1차시 01:30] 그럼 먼저 실습 환경을 구축하는 방법을
[3주차 1차시 01:34] 살펴보도록 하겠습니다.
[3주차 1차시 01:38] 지금부터 설명드리는 실습 환경은 별도 안내를 통해 배포해드리는 Secure Coding Lab 소스 코드 환경 기준입니다.
[3주차 1차시 01:48] 실습 환경의 전체의 흐름을 이해하는 것이 중요한데요. 지금 화면에는 웹 브라우저, Buffsuit Proxy Server, 그리고 스프링붓 기반의 Secure Coding 웹 애플리케이션과
[3주차 1차시 02:02] 데이터베이스 서버까지의 구조가 나와 있습니다. 사용자는 보통
[3주차 1차시 02:08] 웹 브라우저를 통해 1번 흐름과 같이 직접 웹 서비스에 접근하게 되지만 2번
[3주차 1차시 02:19] 흐름과 같이 버프스트라는 프록시 도구를 활용을 해서 모든 HTTP 요청과 응답을 중간에 가로칠 수가 있는데요.
[3주차 1차시 02:34] 이를 활용하면 별도 프로그램을 개발하지 않더라도 간편하게 통신 내용 조작을 통한 취약점 공격을 시도하거나 중요 정보를 얻을 수 있게 됩니다.
[3주차 1차시 02:48] 먼저 공개된 [불명확: cqcoding2025].zip 파일 압축 해제 하시고요.
[3주차 1차시 02:59] 압축은 반드시 C 드라이브 루트 경로에 풀어야 실습을
[3주차 1차시 03:05] 그대로 좀 따라 하실 수 있습니다. 그래서 정상적으로 이 압축이 풀리면 화면처럼 여러 폴더와 실행 파일들이 생성이 되는데요.
[3주차 1차시 03:18] 이 폴더들 안에 실습에 필요한 모든 환경과 코드가 포함되어 있습니다.
[3주차 1차시 03:26] 이번 단계에서는 JDK, [불명확: Waven,] MariaDB의 경로를 시스템 환경 변수에 등록을 하겠습니다
[3주차 1차시 03:35] 먼저 내 PC 아이콘에서 마우스 오른쪽 버튼을 눌러서 속성을 선택하시고 고급 시스템 설정으로 들어간 뒤 환경 변수를 설정합니다.
[3주차 1차시 03:49] 새로운 시스템 변수를 추가하면서 각자 Java Home, Maven Home, MySQL Home 이름으로 폴더 경로를 지정하시고
[3주차 1차시 03:59] 그 다음에는 패스 항목을 편집을 해서 이 변수들의 빈 폴더 경로를 제일 위쪽으로 추가해 줘야 합니다. 등록이 끝나면 CMD 명령 프롬프트 창을 열고 자바 띄어쓰기 하이픈 버전 MVN 버전, MySQL
[3주차 1차시 04:21] 버전 명령어를 실행을 해서 각각의 버전이 잘 출력이 되는지
[3주차 1차시 04:29] 로 이제 확인을 하시면 되겠습니다.
[3주차 1차시 04:37] 그 다음 웹서버와 프록시 서버는 각각 [불명확: 8081번] 포트를 사용하게 되는데요. 이미 시스템에서 다른 프로그램이 이 포트를 사용 중이라면 충돌이 발생하므로 먼저 포트를 확인을 해줘야 합니다.
[3주차 1차시 04:55] 명령 프롬프트에서 [불명확: netset] [불명확: .ano] 명령을 입력을 하면
[3주차 1차시 05:06] 현재 열려 있는 포트 리스트를 확인을 할 수가 있거든요. 그래서 만약 8000번이나 8081번 포트가 리스닝 상태로 보인다면 해당 포트를 전면 프로세스를 찾아서 종료를 해줘야 이 포트를 사용을 할 수가 있겠죠.
[3주차 1차시 05:22] 그래서 프로세스 ID, PID 값을 확인한 뒤에 작업 관리자를 띄워서 해당 프로세스를 찾아 종료시키면 되겠습니다.
[3주차 1차시 05:34] 이제
[3주차 1차시 05:35] 본격적으로 실습 환경을 한번 실행해 보겠습니다. 명령 프롬프트에서 CD 명령어를 통해 압축 파일을 풀었던 Secure Coding 2025 폴더로 이동한 후에 Start Underbar [불명확: LAP] 배치 파일을 실행을 합니다.
[3주차 1차시 05:56] 이 스크립트는 MariaDB와 Spring Tool Suite 4를 자동으로 실행을 시켜 주는데요.
[3주차 1차시 06:02] DB 서버가 정상적으로 실행이 되면 Ready for Connections라는 메시지가 표시가 되는데 이 창은 닫지 말고 최소화된 상태로 유지를 하셔야 합니다.
[3주차 1차시 06:15] Spring [불명확: Tool] Suite에서는 왼쪽에 Secure Coding이라는 프로젝트 폴더가 보이며 정상적으로 열렸다는 뜻입니다.
[3주차 1차시 06:30] 이제 프로젝트를 최신 설정으로 동기화를 해야 하는데요. 시큐어 코딩이라는 프로젝트 이름 위에서 마우스 오른쪽 버튼을 누르고 나오는 메이븐 항복을 찾은 후 그 안에서 업데이트 프로젝트를 클릭하면 창이 하나 열리는데 여기서 OK를 눌러주시면 되겠습니다.
[3주차 1차시 06:51] 이 과정을 통해 의전성 정보가 새로 반영이 되고 필요한 라이브러리들도 자동으로 설정이 됩니다.
[3주차 1차시 06:59] 화면 오른쪽 하단에 진행된 바가 사라지면 업데이트가 모두 완료가 된 것입니다.
[3주차 1차시 07:12] 이제 서버를 실행을 해야 하는데요. 프로젝트 이름을 마우스 오른쪽 버튼으로 클릭을 한 다음에 Run As라는 항목을 찾아서 Spring Boot App이라는 메뉴를 선택을 합니다.
[3주차 1차시 07:25] 그래서 Select Java application 창에서는 Secure Coding Lab Test application을
[3주차 1차시 07:36] 선택을 하고 OK 버튼을 누르면 [불명확: 이제] 서버가 실행이 됩니다. 그렇게 되면 이제 콘솔 창에 Tomcat Started on Pots 8000 이라는 메시지가 뜨면 성공적으로 서버가 구동된 것입니다.
[3주차 1차시 08:01] 간혹 콘솔창에서 출력되는 로그가 너무 많아서 성능 경고 메시지를 나타내는 경우가 있는데요 이럴 때는 콘솔 버퍼 크기를 늘려 주시면 됩니다 화면 상단 메뉴에서 윈도우즈를 누르고 프리퍼런 시스를 선택한 다음 왼쪽 메뉴에서 런 디버그 아래에 있는 콘솔을
[3주차 1차시 08:24] 찾아서 오른쪽에 나오는 콘솔 버퍼 사이즈를
[3주차 1차시 08:29] 100만 정도로 바꿔주시면 되고 그 다음에 어플라이 앤 클로즈를 누르면 설정이 저장이 됩니다.
[3주차 1차시 08:41] 이제 브라우저를 열고 정상적으로 웹 서비스가 실행되는지 확인해 보겠습니다. 크롬이나 파이어폭스 실행하신 다음에
[3주차 1차시 08:53] 주소창에 로컬 호스트 8000 입력하시면 로그인 화면이 나오는데요. 화면에 보이는 대로
[3주차 1차시 09:05] [불명확: 아이디에는] 테스트 암호는 [불명확: qqq111을] 입력하면 기본적으로 탑재되어 있는 사용자 계정으로 로그인할 수 있습니다.
[3주차 1차시 09:16] 로그인에 성공하면 초기 화면이 나타나게 되는데 이 화면까지 잘 나왔다면 서버 세팅이 정상적으로 완료된 것입니다.
[3주차 1차시 09:28] 이제 버프수트를 실행을 해서
[3주차 1차시 09:30] 중간에서 통신 내용을 가로챌 수 있도록
[3주차 1차시 09:38] 프록시 기능을 설정해보도록 하겠습니다.
[3주차 1차시 09:42] [불명확: 그래서] 랩 압축 파일을 풀어놓은 C드라이브의 Secure Coding 폴더 안에는 Download 폴더라는 폴더 하위에 Buffsuit Community 폴더에 Buffsuit Community.ex 파일이 있는데요.
[3주차 1차시 09:57] 이 파일을 실행하면 별도 설치 과정 없이 바로 실행됩니다. 처음 실행할 때는 Terms & Conditions 즉 사용자 약관 화면이 뜨는데
[3주차 1차시 10:09] 여기서 Accept 버튼을 클릭해서 동의하고 넘어갑니다.
[3주차 1차시 10:16] 다음으로 프로젝트를 어떻게 열지 선택하는 화면이 나타나는데요. 여기서는 저장이 필요 없는 실습 환경이기 때문에 임시 프로젝트를 여는 옵션인 Temporary Project로 진행을 하시면 되고요.
[3주차 1차시 10:32] Next 버튼을 누르고 설정 가져올 것인지 묻는 화면이 나오면
[3주차 1차시 10:37] 이미 선택되어 있는 Use Buff Default 그리고 Start Buff 버튼 눌러주시면 됩니다.
[3주차 1차시 10:46] 그럼 이제 메인 화면이 뜨는 것을 볼 수가 있고요. 본격적으로 Buff [불명확: Suite] Proxy 설정을 진행을 해보도록 하겠습니다.
[3주차 1차시 10:56] Buff Suite가 실행이 되면 기본적으로 127.0.0.1 localhost에 포트 8080으로 Proxy 서버가 활성화가 되어 있는데요.
[3주차 1차시 11:07] 하지만 이제 우리는 이 포트를 8081로 변경해서 사용할 예정이므로 해당 설정을 이제 좀 수정을 해줘야 합니다.
[3주차 1차시 11:16] 그래서 상단 메뉴에서 proxy 선택하고 하위 탭 options 클릭하면 proxy listener 목록이 보이는데요.
[3주차 1차시 11:25] 기본 값으로 등록된 항목을 선택하여 누르고 왼쪽에 edit 버튼 클릭하시면 포트 번호를 바꿀 수 있는 설정 창이 열리게 됩니다.
[3주차 1차시 11:38] 프록시 설정 창이 열리면 8080번 포트가 입력되어 있는 것을 8081로 변경을 해주고 그 아래 있는 bind to address 항목은
[3주차 1차시 11:54] loopback only 즉 localhost 전용으로 되어 있으면 되고요.
[3주차 1차시 12:01] 창의 오른쪽 아래 있는 OK 버튼을 눌러서 저장을 해주시면 됩니다.
[3주차 1차시 12:08] 많은 분들이 사용하는 크롬 웹 브라우저는 윈도우 환경의 프록시 설정을 따르도록 되어 있습니다.
[3주차 1차시 12:15] 하지만 윈도우 프록시 설정을 변경하게 되면 일반 인터넷 검색하는 것을 포함해서 실습과 무관한 인터넷 접속들이 전부 다 버프스트를 통해서 통신을 하려고 할 수 있기 때문에 실습 환경을 별도로 분리하기 위해서
[3주차 1차시 12:33] 웹브라우저를 추가로 설치하여 실습하는 것을 파이어폭스 웹브라우저를 추가로 설치해서 실습하는 것을 권장하고요 만약에 윈도우즈로
[3주차 1차시 12:45] 하셔도 프록시를 실습하는 동안만 켜놓고 아닌 경우에는 꺼놓던지 아니면 실습과 무관한 창들은 다 닫아주시고 진행하면 될 것 같습니다.
[3주차 1차시 13:04] 파이어폭스는 독자적으로 프록시 서버 설정하는 것이 가능하기 때문에 다른 인터넷 사용에 영향을 주지 않고 실습을 할 수가 있습니다.
[3주차 1차시 13:14] 설치되어 있지 않은 분들은 firefox.com 사이트에 접속하셔서
[3주차 1차시 13:22] 다운로드 받아서 설치하시면 되고요. 설치가 끝나고 나서 실행을 시키면 그림과 같이 설정 메뉴를 찾아 들어가서 맨 아래쪽에 있는 네트워크 설정 영역에서 설정 버튼을 클릭을 하면 프로시 서버를 수동으로 설정하는 창으로 진입을 할 수가 있고요.
[3주차 1차시 13:49] 프로시 서버 설정 창이 열리면 수동으로 프로시 설정을 입력한 뒤에
[3주차 1차시 13:55] HTTP 프록시에는 127.0.0.1 포트에는 8082를 입력을 하고 확인 버튼을 눌러주시면 설정이 됩니다.
[3주차 1차시 14:11] 그래서 버프스트가 리스닝 중인 포트를 정확하게 입력한 후 확인 버튼을 눌러 설정을 적용을 해야 합니다.
[3주차 1차시 14:20] 파이어폭스는 기본적으로 로컬호스트 주소에 대해서는 프록시 설정을 따르지 않도록 되어 있기 때문에
[3주차 1차시 14:28] 이를 수정하려면 주소창에 About Config를 입력을 해서 고급 설정 페이지에 들어간 후에 network.proxy.allow hijacking localhost 항목을 검색하고 해당 값을 true로 바꿔줘야 합니다.
[3주차 1차시 14:46] 여기까지
[3주차 1차시 14:46] 설정이 끝났으면 웹브라우저에서 localhost에
[3주차 1차시 14:52] 8000번 포트로 접속을 시도하면 버프스트 프록시 탭에 HTTP 요청이 잡히는 것을 확인할 수 있습니다.
[3주차 1차시 15:01] 이 요청은 인터셉트 기능이 켜져 있으면 전달받은 내용을 넘겨주지 않고 대기상태로 멈춰있게 되는데요.
[3주차 1차시 15:10] Intercept is on 버튼을 클릭을 해서 intercept를 off를 하면 요청을 멈춰 세우지 않고 그대로 서버에 전달을 하고 그 응답도 그대로 중개하여 브라우저에 정상적으로 화면이 표시가 됩니다.
[3주차 1차시 15:26] 이제 HTTP 트래픽을 실시간으로 분석할 수 있는 실습 환경이 완료된 것입니다.
[3주차 1차시 15:36] [불명확: 그럼] 지금부터는 웹과 [불명확: 그] 통신 방식인 HTTP 구조에 대해서 알아보도록 하겠습니다.
[3주차 1차시 15:44] 요즘에 웹 시스템은 단순히 세계층으로 설명하기엔 부족한데요. 오른쪽 그림은 그보다 훨씬 세분화된 아키텍처를 보여주고 있습니다.
[3주차 1차시 15:56] 예를 들어 프레젠테이션 레이어 안에서도 UI 컴포넌트와 UI 처리 로직이 따로 존재하고 비즈니스 레이어에는 비즈니스 워크플로우와 컴포넌트가 나뉘면서 외부 클라이언트와의 연동을 위한 서비스 인터페이스도 별도로 구성이 됩니다.
[3주차 1차시 16:14] 그리고 구조의 오른쪽에는 보안, 운영, 통신과 같이 전 계층에 걸쳐 영향을 미치는 크로스 커팅 컨선들도 정리가 되어 있습니다.
[3주차 1차시 16:27] 이처럼 현대 웹 애플리케이션은 다양한 기능과 역할을 나누어 관리하는 복잡하고 정교한 구조를 갖고 있다는 점을 이해하는 것이 중요합니다.
[3주차 1차시 16:40] 앞에서 웹 애플리케이션의 구조를 살펴봤다면
[3주차 1차시 16:44] 이제는 사용자가 웹 서비스를 이용을 할 때 실제로 어떤 흐름으로 동작하는지를 구체적으로 보도록 하겠습니다. 왼쪽에 있는 웹 브라우저에는 사용자가 요청을 보내는 출발점이 표시가 되어 있는데요.
[3주차 1차시 16:59] 사용자가 예를 들어 www.url.com에 접속을 한다고 가정을 하면
[3주차 1차시 17:06] 이 도메인 이름을 실제 IP 주소로 변환하기 위해서 먼저 DNS 서버에 요청을 보냅니다. DNS 서버는 요청을 받아서 해당 도메인에 해당되는 IP 주소를 응답으로 돌려주고요.
[3주차 1차시 17:22] 이 과정이 그림의 1번, 2번 단계입니다. 이제 브라우저는 받은 IP 주소를 이용해서 웹 서버에 접속을 하는데요.
[3주차 1차시 17:31] 3번 단계에서 이 웹 서버에 index.html
[3주차 1차시 17:36] 같은 정적 파일을 요청하게 되고 4번 단계에서는 해당 요청이 웹 애플리케이션 서버와 WAAS로 전달되어 비즈니스 로직을 처리를 하고 필요하다면 5번 단계에 데이터베이스에 접속을 해서 필요한 데이터를 가져오기도 합니다.
[3주차 1차시 17:52] 그 결과로 만들어진 HTML 응답이 6번과 같이 웹 서버로 전달이 되면 그대로 중계되어 7번 단계를 통해 브라우저로 전달이 됩니다.
[3주차 1차시 18:04] 여기서 중요한 점은 웹서버는 주로 정적자원 처리와 클라이언트 연결을 담당하고 WAAS는 웹 애플리케이션 로직 처리를 시행하고 DB에 접근하는 역할을 한다는 점입니다.
[3주차 1차시 18:19] 이렇게 기능적으로 분리된 구성을 통해서 웹 서비스의 성능과 확장성을 동시에 확보할 수 있게 됩니다.
[3주차 1차시 18:29] HTTP는 클라이언트와 서버가 요청과 응답을 주고받는
[3주차 1차시 18:37] 웹통신의 핵심 프로토콜인데요. HTML 문서뿐만 아니라 이미지, CSS, 자바스크립트와 같은 모든 웹 리소스도 HTTP 요청을 통해 전송됩니다.
[3주차 1차시 18:52] HTTP는 스테이틀리스 즉 무상태 구조로 동작하는데요. 서버는 각각의 요청을 독립적으로 처리하면서 이전 요청의 상태를 기억을 하지 않습니다.
[3주차 1차시 19:04] 그래서 인증 세션 같은 정보는
[3주차 1차시 19:07] 요청 메시지 안에 항상 명시적으로 담겨 있어야 하고요. HTTP는 TCP [불명확: IP] 위에서 동작하면서 위로는 HTML, CSS, JavaScript 같은 웹 기술과 연결이 되는데요.
[3주차 1차시 19:24] 이렇게 네트워크와 애플리케이션을 이어주는 중간계층 역할을 한다는 점이 중요합니다.
[3주차 1차시 19:33] 이 하나의
[3주차 1차시 19:33] HTTP 요청이 처리되기까지는
[3주차 1차시 19:37] TCP [불명확: IP] 연결 과정이 먼저 선행이 되는데요. 먼저 서버가 연결을 받을 준비를 하고 나면 브라우저가 TCP 3-way handshake을 통해서 연결을 설정을 합니다.
[3주차 1차시 19:50] 연결이 완료되면 서버는 클라이언트 전용 프로세스를 만들고 HTTP 요청을 처리를 할 준비를 합니다. 이후 브라우저는 요청을 전송하고 서버는 이를 받아서 응답 데이터를 생성하여 전송을 합니다.
[3주차 1차시 20:07] 응답은 다시 TCP를 통해 브라우저로 전달이 되고 연결 종료 과정을 거쳐 통신이 마무리됩니다.
[3주차 1차시 20:16] HTTP는 무상태이지만 그 아래에서는 TCP가 상태를 유지하면서 복잡한 연결 흐름을 관리하고 있다는 점이 핵심입니다.
[3주차 1차시 20:30] 버프스트의 HTTP 히스토리 기능을 이용하면 브라우저에서 오고 간 모든 요청과 응답을 시간순으로 확인할 수 있는데요.
[3주차 1차시 20:40] 화면에서는 요청 주소, 메서드, 응답 코드, MIME 타입 등이 한눈에 정리되어 있으며 항목을 선택을 하면 하단에서 리퀘스트 요청과 리스폰스 응답 메시지의 실제 내용을 확인할 수가 있습니다.
[3주차 1차시 20:57] 왼쪽 요청 메시지로 메서드와 헤더, 쿠키 정보 등이 포함이 되어 있고
[3주차 1차시 21:03] 오른쪽은 응답 메시지로 HTML이나 JSON 같은 파일이 서버 데이터가 표시가 됩니다.
[3주차 1차시 21:12] 퍼프스트를 활용을 하면 HTTP 구조와 데이터 흐름을 실시간으로 시각적으로 확인할 수 있기 때문에 앞서 배운 개념을 실제 네트워크 트래픽에서 직접 확인해 볼 수 있습니다.
[3주차 1차시 21:28] HTTP 요청은 크게 리퀘스트 라인이랑 헤더로 구성이 되는데요.
[3주차 1차시 21:33] 첫줄에는 요청방식의 메서드 그리고 방식의
[3주차 1차시 21:41] 메서드인 get이 메서드고요 요청경로 board-main 사용버전인 http 1.1 버전정보가 포함이 되고 이를 request-line이라고 합니다 그 아래에는 요청 헤더들이 이어지는데요 호스트는 요청할 서버 주소
[3주차 1차시 22:02] 그리고 유저 에이전트는 브라우저 종류를 나타냅니다. 이외에도 Accept, Referrer, Connection 등 다양한 헤드들이 포함이 되고 서버는 이 정보들을 참고해 적절한 응답을 생성합니다.
[3주차 1차시 22:21] 특히 중요한 내용이 쿠키 헤더인데요. HTTP가 원래 상태의 정보를 보관하지 않는 구조이기 때문에 서버는 쿠키를 통해 클라이언트의 세션 상태를 유지하게 됩니다.
[3주차 1차시 22:38] HTTP 메서드는 클라이언트가 서버에 어떤 방식으로 요청할지를 지정하는 방식인데요. 대표적으로 GET은 리소스를 조회를 할 때, POST는 데이터를 제출할 때 사용합니다.
[3주차 1차시 22:53] Get은 URL에 파라미터를 붙여서 전송하므로 보안에 취약할 수 있고, Post는 본문의 데이터를 담기 때문에 민감한 정보를 전송하는 데 더 적합합니다.
[3주차 1차시 23:05] 이외에 Put, Delete, Head, Options 같은 메소드들도 존재하지만, 실제 서비스에 필요한 메소드만 허용하고, 나머지는 웹방화벽, WAF 등에서 차단하는 것이 보안상 안전합니다.
[3주차 1차시 23:24] 이번에는 서버가 클라이언트 요청에 대해 보내는 HTTP 응답 메시지 구조를 살펴보도록 하겠습니다. 가장 윗줄인 HTTP 1.1 200 OK 상태줄 즉 스테이터스 라인인데요.
[3주차 1차시 23:39] 요청이 성공적으로 처리되었음을 나타냅니다. 그 아래에는 응답 헤더 즉 리스폰스 헤더가 이어지며 브라우저가 이 응답을 어떻게 해석하면 될지를 알려주는데요.
[3주차 1차시 23:53] 예를 들어 커넥션 타입, 응답이 HTML 문서이고 UTF [불명확: 파일] 인코딩을 사용한다는 것을 나타내며 캐시 컨트롤, 엑스파이어, 프레그마 등은 캐싱 여부들을 결정합니다.
[3주차 1차시 24:08] 또한 엑스 컨텐츠 타입 옵션스, 그리고 MIME 타입을 엄격하게 따르도록 하고 X, XSS 프로텍션
[3주차 1차시 24:24] 이것은 크로스 사이트 스크립팅 방어 기능 설정을 한다고 알 수 있습니다. 그리고 마지막으로는 응답 본문인 HTML 컨텐츠가 HTML 헤드 타이틀 순으로 맨 아랫부분에 있는 걸 보실 수가 있죠.
[3주차 1차시 24:47] 그래서 이 부분이 브라우저에 표시되는 실제 웹페이지를 설명하는 코드라고 보시면 되겠습니다.
[3주차 1차시 24:57] HTTP 응답 메시지 구조에 대한 이야기에서 가장 핵심적인 정보는 스테이터스 코드이고 상태 코드인데요.
[3주차 1차시 25:06] 이걸 좀 더 자세히 살펴보도록 하겠습니다. 상태 코드는 클라이언트 요청에 처리한 결과가 어떤 상태인지를 알려주는 세자리 숫자인데요.
[3주차 1차시 25:17] 이 숫자는 크게 100번대부터 500번대 값까지 총 5가지의 종류로 나뉘어집니다.
[3주차 1차시 25:25] 차례로 보면 100번 때는 정보 제공과 관련된 상태를 알려주는 코드고 200번 때는 성공적으로 처리되었다는 의미입니다.
[3주차 1차시 25:35] 그래서 200이
[3주차 1차시 25:36] OK의 의미로 많이 알려져 있죠. 그리고 300번 때는 요청한 자원이 다른 곳에 있다는 리디렉션의 의미입니다.
[3주차 1차시 25:45] 로그인한 다음 메인 페이지로 이동할 때 종종 사용이 됩니다. 400번 때는 클라이언트 요청에 문제가 있다는 의미입니다.
[3주차 1차시 25:55] 그래서 404 not found가 가장 대표적인 코드값입니다. 그리고 마지막으로 500번대 값은 서버에서 오류가 발생했다는 뜻입니다.
[3주차 1차시 26:07] 500 internal server
[3주차 1차시 26:08] error 많이 볼
[3주차 1차시 26:09] 수 있는 코드값이죠. 세부적으로 사용되는 코드의 각 의미들을 하단에 정리해 두었습니다.
[3주차 1차시 26:18] 100번대와 200번대 상태 코드에 대한 상세 내용이고요.
[3주차 1차시 26:23] 다음 페이지는 300번과 400번대 상태 코드에 대한 상세 내용들입니다.
[3주차 1차시 26:31] [불명확: 한번] 직접 읽어보시면 될 것 같습니다.
[3주차 1차시 26:40] 나머지 부분들도 정리된 내용을 직접 읽어보시면 좋을 것 같습니다.
[3주차 1차시 26:56] 그럼 이번에는 [불명확: 이제] 데이터 인코딩에 대해서 학습해보도록 하겠습니다.
[3주차 1차시 27:04] 데이터 인코딩은 정보를 특정 규칙에 따라서 다른 형식으로 변환하는 과정인데요. 인코딩이 필요한 경우는 세 가지 정도로 정리를 할 수가 있습니다.
[3주차 1차시 27:16] 첫 번째는 데이터 전송 과정에서의 안전성 확보인데요. 인코딩을 사용하면 네트워크나 시스템 간 데이터 전송 과정에서 데이터가 깨지지 않고 정확히 전달되도록 할 수가 있습니다.
[3주차 1차시 27:31] 둘째는 보안 강화입니다.
[3주차 1차시 27:34] 예를 들어 사용자의 입력값을 html 태그나 자바스크립트 코드로 처리하지 않고 안전하게 변환해서 주면 크로스 [불명확: 타이트] 스크립팅 같은 보안 문제를 막을 수가 있습니다.
[3주차 1차시 27:48] 세번째는 호환성 유지인데요. 서로 다른 시스템 간의 데이터를 주고 받을 때
[3주차 1차시 27:54] 상호 데이터 표기법 차이로 오류가 발생하는 걸 방지하기 위해서 공통된 인코딩 포맷을 사용하는 것이 이런때는 유리합니다 여기서 이제 중요한 건 인코딩이랑 암호화는 다르다는 것인데요
[3주차 1차시 28:10] 인코딩은 누구나 쉽게 디코딩할 수 있는 변환 방식이지만 암호화는 보안을 위해 키가 필요한 복호화를 하기 위해서는 키라는 비밀 정보가 필요하다는 점에서 인코딩과는 차이가 있습니다.
[3주차 1차시 28:27] 이제부터는 대표적인 두 가지 인코딩 방식인 베이스64 인코딩과 URL 인코딩을 한번 살펴보도록 하겠습니다.
[3주차 1차시 28:39] Base64 인코딩은 바이너리 데이터를 텍스트로 바꾸는 방법인데요. 이진 데이터를 6비트 단위로 쪼개서 A부터 [불명확: G,] 소문자 A부터 [불명확: G,] 그리고 숫자,
[3주차 1차시 28:53] 그리고 W란다 플러스와 슬래시까지 총 64개 문자로 변환해서 이름이 64로 붙어져 있는 거고 이때 6비트로 나누어 떨어지지 않는 경우에는
[3주차 1차시 29:08] [불명확: 는] 기호로 패딩 처리를 합니다. 이 방식이 사용되는 대표적인 예는 이메일, 제이슨, xml 같은 텍스트 기반 데이터 전송이고요.
[3주차 1차시 29:20] 예를 들어서 제이슨 안에 바이너리 파일을 삽입할 때 베이스64 인코딩을 해서 넣으면 안정적으로 전송을 할 수가 있습니다.
[3주차 1차시 29:31] 아래쪽에는 헬로월드라는 문자열을 베이스64로 인코딩한 결과입니다.
[3주차 1차시 29:37] [불명확: 이] 문자열이 오른쪽처럼 다양한 문자들로 바뀐 것을 확인을 할 수가 있습니다. Base64는 보안 목적이 아니라 전송 안전성과 호환성을 위한 인코딩이라는 점을 기억해 두시면 좋을 것 같습니다.
[3주차 1차시 29:55] 이번에는 URL 인코딩 알아보겠습니다.
[3주차 1차시 30:00] URL 인코딩은 웹 주소에 포함될 수 없는 특수문자들을 안전하게 표현하기 위해 사용이 되는 방식인데요.
[3주차 1차시 30:08] URL에는 공백이나 물음표, 엔드 기호, 샵 이런 특별한 의미를 가진 문자들이 있는데 이런 문자들을 그대로 URL에 포함시키면 해석에 문제가 발생을 하기 때문에 %기호와 ASCII 16 진수
[3주차 1차시 30:30] 값으로 변환해서 사용을 합니다. 예를 들어서 Hello, [불명확: Dear,] World 라는 문자열을
[3주차 1차시 30:40] 쿼리 파라미터로 전송을 하려면 공백을 %20으로 인코딩을 해서 Hello %20 World로 띄어쓰기 없이 바꿔야 전달이 됩니다.
[3주차 1차시 30:53] 그리고 한글, 일본어 같은 비아스키 문자들도 인코딩 대상입니다. 꺽쇠, 따옴표 같은 문자들은 크로스 사이트 스크립팅 같은 보안 문제를 유발할 수 있기 때문에 URL 인코딩을 통해 안전하게 전송을 해야 합니다.
[3주차 1차시 31:10] 슬라이드 아래쪽 예시처럼 스크립트 구문을 그대로 넣으면 위험하지만 인코딩을 통해 전달하면 안전하게 전달할 수 있습니다.
[3주차 1차시 31:22] 인코딩이 필요한 문자들을 표로 정리를 해보았는데요. 우선 앞에서 살펴봤던 [불명확: 0100,] %20으로 인코딩되고요.
[3주차 1차시 31:31] 퍼센트 20으로 인코딩 되고요. 제가 16진수니까 [불명확: 20이라고] 읽지 않고 [불명확: 20] 이런 식으로 읽도록 하겠습니다.
[3주차 1차시 31:41] 그리고 특별한 의미로 해석될 수 있는 예약 문자들, 예를 들어 물음표, [불명확: end,] 샵, 슬래시, 콜론 등은 각각의 ASCII 코드값을 사용하여 인코딩을 할 수가 있습니다.
[3주차 1차시 32:00] 스크립트 언어나 SQL문으로 악용될 수 있는 특수문자, 느낌표, 골뱅이, 이런 문자도 마찬가지이고요.
[3주차 1차시 32:10] 그리고 한글이나 일본어 같은 비-ASCII 문자들도
[3주차 1차시 32:14] 모두 인코딩을 통해 ASCII 코드로 변환하여 사용합니다. 반대로 인코딩이 필요 없는 안전한 문자들은 표준 ASCII 문자인 알파벳 대문자, 알파벳 소문자, 숫자, 그리고 일부 특수문자, 하이픈 언더바 점 물결과 같은 특수문자들입니다.
[3주차 1차시 32:40] 이제부터는 한번 실습을 해보도록 하겠습니다.
[3주차 1차시 32:44] 버프스트를 이용해서 베이스64로 인코딩된 문자열을 디코딩하는 방법을 한번 알아보도록 하겠습니다. 이미 시큐어 코딩 랩 설치 과정에서 버프스트를 프록시 서버로 설정을 해서 웹브라우저의 인터넷 통신 내용을 가로채서 볼 수가 있잖아요.
[3주차 1차시 33:07] 그래서 그 환경을 그대로 활용을 해보도록 하겠습니다.
[3주차 1차시 33:10] 주소창에 이 화면에 나와 있는 주소를 그대로 입력을 해주시고요. HTTP [불명확: BIN] 사이트에서 기본 인증을 요구하는 화면으로 넘어가는데 이때 버프스트에서 intercept is off로 되어 있다면 버튼을 다시 눌러서 온 상태로 즉 가로채기 상태로 전환을 해주셔야
[3주차 1차시 33:32] 되고요. 그리고 [불명확: 암호] 사용자 이름과 비밀번호를 입력하고 로그인을 한번 시도를 해봅시다.
[3주차 1차시 33:42] 버프스트 화면에서 HTTP 요청 내용을 보면 Authorization Header에 Base64 인코딩된 문자열이 포함되어 있는 것을 확인할 수 있습니다.
[3주차 1차시 33:56] 이 문자열은 사용자 이름과 비밀번호가 Base64로 인코딩되어 있다는 것을 나타내는데요. 이 인코딩된 문자열을 마우스로
[3주차 1차시 34:07] 더블클릭하거나 드래그해서 복사를 하면
[3주차 1차시 34:12] 우측 패널 인스펙터 창에 자동으로 디코딩된 값이 표시가 됩니다. [불명확: 그래서] 여러분이 입력한 로그인 정보가 복원되어 보이는 걸 확인하실 수 있을 겁니다.
[3주차 1차시 34:25] 일단 베이스64 원본 문자열에서 Ctrl-C를 눌러 복사를 해둡시다. 이번엔 버프스트
[3주차 1차시 34:34] 상단에 디코더 메뉴로 이동을
[3주차 1차시 34:37] 하면
[3주차 1차시 34:44] 입력창이 나오는데요.
[3주차 1차시 34:47] 여기에 아까 복사해둔 Base64 문자열을 붙여넣고 우측 옵션에서 Decode as Base64를 선택을 하면 하단에 디코딩된 문자열이 또 출력되는 것을 볼 수가 있습니다.
[3주차 1차시 35:04] 이러한 방식으로도 Base64 인코딩 데이터를 풀어서 확인할 수가 있고요.
[3주차 1차시 35:11] 이번에는 [불명확: Buffs트를] 통해서 URL 인코딩을 한번 실습을 해보도록 하겠습니다.
[3주차 1차시 35:20] 앞페이지에서 실습했었던 디코더 메뉴의 입력창에 사이트 주소를 붙여넣고 우측에 인코드에즈로 URL을 선택을 하면 아래쪽 파트의 %로 인코딩된 문자열을 볼 수가 있습니다.
[3주차 1차시 35:37] 방금
[3주차 1차시 35:42] URL 인코딩한 문자열을 입력창에 다시 복사해서 붙여넣고
[3주차 1차시 35:49] 옆에서 decode as로 URL을 선택을 하거나 인코딩 결과가 나와 있는 입력창 옆에서 decode as URL을 선택을 하면 그 아래쪽으로 원래 주소가 복원되어 나타나는 것을 확인할 수가 있습니다.
[3주차 1차시 36:09] 이번 차시의 내용은 여기까지인데요. 한번 정리를 해보면 우선 제공해드린 랩 실습 환경은 스프링 부트 기반으로 버프 수트를 프록시 서버로 설정을 해서 구축을 해봤고요.
[3주차 1차시 36:21] 웹서비스는 브라우저, 웹서버, 와스, DB 간의 통신 흐름으로 운영된다. 그리고 HTTP는 요청 메시지와 응답 메시지로 통신을 하며 상태 정보를 유지하지 않고 HTTP 요청 안에는 바디 외에 메서드, 경로, 쿠키, 파라미터 같은 헤더들이 있고 응답
[3주차 1차시 36:44] 안에는 바디 외에
[3주차 1차시 36:46] 상태 코드가 들어가 있어 서버의 처리 상태를 알 수가 있고, Base64와 URL 인코딩은 특수문자나 바이너리 데이터를 안전하게 전달하기 위해 사용된다.
[3주차 1차시 36:57] 이번 차시 내용은 이렇고,
[3주차 1차시 37:01] 참고 문헌은 다음과 같습니다.
[3주차 1차시 37:05] 1차시 이것으로 마치도록 하겠습니다. 감사합니다.

# [3-TRANSCRIPT] 3주차 2차시 — Spring Boot 개발 환경·실습
키워드: Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한

[3주차 2차시 00:04] 3주차 2차시 수업 진행 시작하도록 하겠습니다.
[3주차 2차시 00:14] 이번 차시는 실습 환경 구축 두 번째 시간이고요. 스프링부트 프레임워크를 활용한 웹 프로젝트 구축을 한번 해보도록 하겠습니다.
[3주차 2차시 00:27] 학습 목표입니다. 스프링부트 프레임워크의 개념과 역할을 이해하고 기본 사용법을 익혀보도록 하겠습니다.
[3주차 2차시 00:38] 이에 따른 학습 내용은
[3주차 2차시 00:40] 다음과 같습니다. 첫째, 프레임워크와 플랫폼의 개념을 정확히 이해하고 두 개념의 차이점을 구분할 수 있도록 합니다.
[3주차 2차시 00:50] 둘째, 간단한 웹 애플리케이션을 직접 작성하고 실행을 해보면서 웹 개발의 기본 구조와 흐름을 실습을 통해 익혀보도록 하겠습니다.
[3주차 2차시 01:04] 그럼 스프링부트 프레임워크에 대해 알아보도록 하겠습니다.
[3주차 2차시 01:10] 소프트웨어 개발을 하다보면
[3주차 2차시 01:17] 프레임워크와 플랫폼이라는 용어를 많이 접하게 될 텐데요. 처음 들으면 둘 다 개발에 도움을 주는 도구처럼 느껴집니다.
[3주차 2차시 01:26] 실제로는 이 두 가지는 목적과 역할이 좀 다른데요. 그럼 먼저 프레임워크가 무엇인지부터 한번 살펴보도록 하겠습니다.
[3주차 2차시 01:37] 프레임워크는 쉽게 말하면 개발을 빠르고 효율적으로 할 수 있도록 기본 틀과 규칙을 제공해주는 재사용 가능한 코드 라이브러리입니다.
[3주차 2차시 01:48] 예를 들어 아무것도 없는 상태에서 웹사이트를 처음부터 직접 만들면 어떨까요? 서버 설정, 데이터베이스 연결, 인증 로직, 화면 구성까지 모든 걸 다 직접 코딩을 해야 될 텐데 하지만 이때 프레임워크를 도입을 하면 기본적인 부분들이 이미 갖추어져 있기
[3주차 2차시 02:10] 때문에 개발자는 필요한 핵심 로직만 집중하여 개발을 할 수가 있습니다.
[3주차 2차시 02:17] 프레임워크는 단순한 라이브러리 모음이 아닌데요. 코드 아키텍처와 디자인 패턴 같은 개발 규칙을 함께 제공을 하는데요. MVC 패턴 같은 애플리케이션 구조를 강제로 따르게 합니다.
[3주차 2차시 02:32] 그 덕분에 개발자들은 일관성 있게 코드를 작성할 수 있게 되면서도 프로젝트 규모가 커지더라도 유지 보수가 쉬워집니다.
[3주차 2차시 02:42] 또 하나 중요한 점은 프레임워크가 자동화 기능을 제공하여
[3주차 2차시 02:46] 반복 작업을 줄여주고 생산성을 높여준다는 것입니다. 예를 들어 예전엔 데이터베이스 연결 설정을 매번 새로 구현을 했다면 이제는 프레임워크가 제공하는 설정 기능을 이용해서 간단한 코드만 만들면 이 연결이 끝이 나죠.
[3주차 2차시 03:05] 인증 로직, 오류 처리 같은 다른 영역에서도 마찬가지이고요. Java 언어에는 Spring 프레임워크, Python 언어에는 장고라는 프레임워크가 널리 쓰입니다.
[3주차 2차시 03:19] 그리고 자바스크립트 기반의 프론트엔드 개발에서는 리액트 같은 프레임워크가 인기를 끌고 있습니다.
[3주차 2차시 03:27] 이처럼 프레임워크는 단순한 도구를 넘어 개발 과정 전체를 더 빠르고 견고하게 만들어주는 역할을 하고 있습니다.
[3주차 2차시 03:39] 이번에는
[3주차 2차시 03:40] 플랫폼의 개념을 알아보도록 하겠습니다.
[3주차 2차시 03:44] 플랫폼은 프레임워크와 다르게 애플리케이션이 실행될 수 있는 환경 자체를 제공하는 것을 의미합니다. 즉 개발자가 만든 프로그램이 돌아갈 수 있는 운영체제, 서버 환경, 그리고 또는 클라우드 인프라와 같은 기반을 마련해주는 역할을 하죠.
[3주차 2차시 04:06] 그래서 플랫폼은 하드웨어일 수도 있고 소프트웨어일 수도 있으며 요즘은 이 둘을 아우르는 형태가 많습니다.
[3주차 2차시 04:15] 핵심은 개발자나 사용자가 서비스를 만들고 운영할 수 있도록 필요한 기반을 모두 제공해준다는 것입니다.
[3주차 2차시 04:24] 플랫폼의 가장 큰 특징은 크게 세 가지로 나눌 수 있는데요. 첫째, 애플리케이션이 실행될 수 있는 기반을 제공한다는 점입니다.
[3주차 2차시 04:35] 예를 들어 우리가 사용하는 윈도우나 맥, 리눅스 같은 운영체제는 애플리케이션이 동작할 수 있는 환경을 마련해줍니다.
[3주차 2차시 04:45] 이것이 [불명확: 이제] 바로 소프트웨어 플랫폼의 대표적인 사례이고요. 둘째, 개발자에게 API와 같은 서비스들을 제공해주는 것입니다.
[3주차 2차시 04:58] AWS, Azure 같은 클라우드 플랫폼을 생각을 해보면 이런 플랫폼은 단순히 서버만 제공하는 게 아니라 데이터 저장, 인증, 통신 같은 다양한 기능을 API 형태로 제공하죠.
[3주차 2차시 05:14] 덕분에 개발자는 일일이 인프라를 구축하지 않고도 서비스를 개발할 수 있습니다. 셋째, 하드웨어나 소프트웨어 기반으로 서비스 생태계를 형성한다는 특징이 있습니다.
[3주차 2차시 05:28] 대표적인 예가 바로 모바일 앱 생태계인데요. 안드로이드나 iOS는 각각 하나의 플랫폼으로서 수많은 앱이 그 위에서 개발되고 배포됩니다.
[3주차 2차시 05:40] 구체적으로 플랫폼 종류를 살펴보면 윈도우나 맥, 리눅스 등은 애플리케이션이 실행될 수 있는 전통적인 운영체제의 플랫폼이고 AWS나 Azure, GCP들은 클라우드 컴퓨팅 기반으로 다양한 인프라와 서비스를 제공하는 플랫폼입니다.
[3주차 2차시 06:01] 안드로이드나 iOS들은 모바일 앱 개발과 실행을 위한 플랫폼이고
[3주차 2차시 06:07] Unity, Unreal Engine은 게임 개발과 실행을 위한 전문 플랫폼이라고 생각하시면 되겠습니다.
[3주차 2차시 06:15] 그래서 플랫폼은 단순히 어떤 프로그램을 만들 때 쓰는 도구가 아니라 그 프로그램이 실제로 돌아가고 관리되고 성장할 수 있도록 지원하는 전체 환경을 의미합니다.
[3주차 2차시 06:33] 앞에서 프레임워크와 플랫폼의 개념을 따로 살펴봤는데요.
[3주차 2차시 06:38] 이번에는 직접 표로 비교하면서 차이를 정리해 보겠습니다. 프레임워크는 소프트웨어를 개발할 때 필요한 구조와 규칙을 제공, 그리고 개발자는 이틀을 기반으로 필요한 기능을 추가를 해가면서 개발을 진행을 하게 됩니다.
[3주차 2차시 06:57] 반면 플랫폼은 개발된 소프트웨어가 실행될 수 있는 환경을 제공해 줍니다.
[3주차 2차시 07:03] 운영체제, 서버, 클라우드, 인프라처럼 프로그램이 실제로 구동되는 기반을 제공하는 것입니다. 프레임워크가 어떻게 만들 것인가를 안내하는 도구라면 플랫폼은 어디서 구동할 것인가를 해결해주는 기반이라고 볼 수 있습니다.
[3주차 2차시 07:22] 또 하나 다른 점은 프레임워크는 주로 코드 구조나 개발 흐름을 관리하지만 플랫폼은 실행 환경 전반,
[3주차 2차시 07:31] 인프라까지 포함해 훨씬 넓은 범위를 다룬다는 것입니다. 프레임워크는 개발 지원 도구, 플랫폼은 실행 환경 제공이라는 점을 기억해두면 됩니다.
[3주차 2차시 07:47] 이제 본격적으로 스프링 부트 프레임워크를 살펴보도록 하겠습니다. 스프링 부트는 기존 스프링 프레임워크를 쉽게 사용할 수 있도록 만들어진 확장판인데요.
[3주차 2차시 08:06] Spring은 매우 유연하지만 설정할 것이 많아 초기 진입장벽이 높은 편이었는데 Spring Boot는 이런 복잡함을 없애고 개발자가 빠르게 프로젝트를 시작할 수 있도록 자동화 기능을 [불명확: 강화했습니다.] 대표적으로 자동 설정 Auto Configuration 기능이 있는데요.
[3주차 2차시 08:28] 애플리케이션이 필요로 하는 기본 설정을 자동으로 맞춰주기 때문에
[3주차 2차시 08:32] 개발자는 복잡한 XML 파일이나 환경 설정을 직접 작성할 필요가 거의 없습니다. 또 하나 중요한 특징은 [불명확: WAAS] 서버를 내장하고 있다는 점인데요.
[3주차 2차시 08:46] [불명확: 통깃] 같은 서버가 Spring Boot 안에 함께 들어있기 때문에 별도로 서버를 설치하지 않고도 애플리케이션을 바로 실행할 수 있습니다.
[3주차 2차시 08:55] 이외에도 다양한 스타트업 패키지가 준비되어 있어서 웹 데이터베이스, 웹 데이터베이스 보안 같은 기능을 쉽게 추가할 수 있습니다.
[3주차 2차시 09:07] 필요한 기능을 체크만 하면 알아서 관련 라이브러리들이 설정이 되고요.
[3주차 2차시 09:16] 스프링부터는 그래서 설정의 복잡함을 최소화하고 코딩에 바로 집중할 수 있도록 도와주는 프레임워크다.
[3주차 2차시 09:24] 따라서 개발 생산성이 크게 높아지게 되며 특히 빠르게 프로토타입을 만들 때 강력한 장점을 발휘하는 웹 프레임워크입니다.
[3주차 2차시 09:36] 그럼 기존 스프링 프레임워크와 스프링 부트를 표로 한번 비교를 해보도록 하겠습니다. 먼저 설정 방식 부분을 보면 스프링 프레임워크는 XML 파일이나 Java 설정 클래스 등을 통해서 세세한 구성을 직접 작성을 해야 했습니다.
[3주차 2차시 09:54] 개발자가 일일이 옵션을 지정하고 필요한 라이브러리들을 일일이 연결을 해야 했죠. 반면 스프링부트는 자동 설정 방식을 지원합니다.
[3주차 2차시 10:06] 자동으로 기본 설정을 적용해주고 추가로 필요한 부분만 개발자가 선택하면 됩니다. 스프링부트는 패키지 의존성 관리 쪽으로도 간편하고 서버도 내장되어 있습니다.
[3주차 2차시 10:20] 이런 여러 장점들 때문에 최근 개발되는 자바 기반 웹 서비스는
[3주차 2차시 10:25] 거의 비공식 표준처럼 스프링 부트 프레임워크를 사용하고 있다고 말할 수 있습니다.
[3주차 2차시 10:34] 스프링 부트 애플리케이션을 개발을 하려면 먼저 개발 환경을 구성을 해야 하는데요. 그 중 가장 기본적인 준비 단계가 바로 스프링 [불명확: 툴슛] 줄여서 STS 설치입니다.
[3주차 2차시 10:50] STS는 Eclipse를 기반으로 한 통합 개발 환경으로
[3주차 2차시 10:54] Spring Framework와 Spring Boot Project를 쉽게 만들고 관리를 할 수 있습니다. 우선 STS 공식 다운로드 사이트에 접속을 해서 자신의 OS에 맞는 설치 파일을 다운받아 설치를 진행하면 됩니다.
[3주차 2차시 11:13] 이제
[3주차 2차시 11:13] STS를 설치한 상태에서 Spring Boot Project를 직접 생성해보는 과정을 설명하도록 하겠습니다.
[3주차 2차시 11:23] STS를 실행한 뒤 새로운 프로젝트를 생성을 할 때 스프링 스타터 프로젝트를 선택을 합니다. 그러면 프로젝트 이름과 사용할 메이븐과 그래들 빌드 도구, 그리고 사용할 Java 버전, 패키징 방식 등을 선택할 수 있습니다.
[3주차 2차시 11:43] 프로젝트 메타데이터를 입력하는
[3주차 2차시 11:49] 메타데이터를 입력하는 단계에서는 그룹 아이디와 아티팩트 아이디 같은 정보를 입력을 해야 하는데요. 그룹 아이디는 보통 회사나 조직의 도메인을 반대 순서 형태로 입력한 뒤 프로젝트 명칭을 이용한 이름을 붙이고 아티팩트 아이디는 프로젝트 이름으로 입력을 합니다.
[3주차 2차시 12:21] 이 과정을 마치면 기본적인 프로젝트 구조가 자동으로 생성되고
[3주차 2차시 12:26] 필요한 의존성 라이브러리도 함께 다운로드 되어 준비가 완료됩니다.
[3주차 2차시 12:34] STS를 사용하면 복잡한 설정 없이 빠르게 Spring Boot 프로젝트를 시작할 수 있다는 점이 큰 장점입니다.
[3주차 2차시 12:44] Spring Boot 프로젝트를 만드는 방법으로 한 가지 더 있는데요. 바로 Spring Initializer라는 웹사이트를 사용하는 방법입니다.
[3주차 2차시 12:55] Spring Initializer는 웹브라우저에 start.spring.io를 입력하면 웹브라우저에서 바로 접속을 할 수 있는데요.
[3주차 2차시 13:07] 필요한 프로젝트 정보를 입력한 다음에 기본 구성이 완료된 프로젝트 파일을 다운로드할 수 있도록 도와줍니다. 웹페이지에 접속해보면 앞서 프로젝트 생성 시 입력했던 내용들과 유사하게 설정할 수 있도록 되어 있습니다.
[3주차 2차시 13:24] 특히 [불명확: 인셜라이저에서는] 웹, 데이터베이스, 시큐리티 등
[3주차 2차시 13:29] 다양한 스타터 라이브러리를 한 번에 선택해서 포함시킬 수 있기 때문에 초기 세팅이 훨씬 빠르고 간편합니다.
[3주차 2차시 13:39] 모든 항목을 입력하고 나서 generate 버튼을 누르면 프로젝트 파일들이 압축되어 다운로드 되므로 STS에서 불러와 바로 실행을 할 수가 있습니다.
[3주차 2차시 13:52] 이제
[3주차 2차시 13:53] 프로젝트가 준비가 되었으니 가장 기본이 되는 메인 애플리케이션 파일을 만들어 보도록 하겠습니다.
[3주차 2차시 14:02] [불명확: 이] Spring Boot 프로젝트를 생성을 하면 기본적으로 하나의 메인 클래스를 만들어야 하는데요. 여기에서는 Hello Spring Boot application으로 생성을 하는데 이 클래스는 프로젝트를 실행하는 시작 위치입니다.
[3주차 2차시 14:19] 클래스 안에는 메인 메소드가 들어있고 그 안에서 spring-application.run이라는 코드가 호출됩니다.
[3주차 2차시 14:28] 이 코드가 Spring Boot 애플리케이션을 동작시키게 하는 것이 핵심입니다. 여기서 주목할 점은 Spring Boot Application이라는 어노테이션이 클래스 위에 붙어 있다는 점입니다.
[3주차 2차시 14:43] 이 어노테이션으로는 Spring Boot 자동 설정, Spring Component Scan,
[3주차 2차시 14:49] Spring 설정 클래스로 인식하도록 하는 기능과 같이 여러 기능이 한꺼번에 포함되어 있는 특징을 갖고 있습니다.
[3주차 2차시 14:59] 메인 애플리케이션 클래스가 준비되었으니 다음으로 웹 요청을 처리할 수 있는 컨트롤러를 만들어 보는 과정입니다. 컨트롤러는 사용자의 요청을 받아서 그에 대한 응답을 생성하는 역할을 합니다.
[3주차 2차시 15:15] 스프링부트에서는 이를 처리할 곳을 지정하기 위해 해당 [불명확: 클래스의] 골뱅이
[3주차 2차시 15:22] REST 컨트롤러 [불명확: 언어테이션을] 붙여줍니다. 그리고 메소드에는 getMapping처럼 URL의 경로를 지정해서 지정한 경로로 요청이 들어왔을 때 이곳에서 처리하겠다고 정의를 합니다.
[3주차 2차시 15:42] 그 메서드 안에는 HelloSpringBoot
[3주차 2차시 15:46] 문자열을 반환해 두도록 작성해 두었습니다. 이렇게 하면 브라우저로 해당 서버에 접속을 했을 때 그 문자열이 바로 화면에 출력되게 됩니다.
[3주차 2차시 15:59] 컨트롤러 클래스는 어플리케이션 로직과 직접 연결되는 핵심 부분인데요. 특히 웹 서비스에서는 사용자의 요청 흐름을 가장 먼저 받는 출입구 역할을 하게 됩니다.
[3주차 2차시 16:14] 이제 이렇게 만들어진 애플리케이션을 실행해 보는 과정입니다.
[3주차 2차시 16:18] STS에서 프로젝트를 만든 후 메인 클래스 파일 즉 Hello Spring Boot Application 파일에서 마우스 [불명확: 클릭한] 후 Run as Spring Boot App 클릭하시면 됩니다.
[3주차 2차시 16:33] 앞서 이야기했듯이 Spring Boot는 내장 서버를 가지고 있기 때문에 별도로 Tomcat이나 다른 웹서버를 설치하지 않아도 됩니다.
[3주차 2차시 16:44] 애플리케이션이 실행되면서 콘솔창에 서버가 구동되어 있다는 로고가 출력되는 것을 볼 수 있게 되는데요.
[3주차 2차시 16:53] Started Hello Spring Boot Application이라는 메시지가 뜨면 애플리케이션이 정상적으로 실행이 된 것입니다.
[3주차 2차시 17:03] 이제 정상적으로 동작하는지 확인하는 방법을 한번 보겠습니다. 브라우저를 열고 주소창에 Localhost 8080 API Hello를
[3주차 2차시 17:13] 입력을 해보시면 됩니다.
[3주차 2차시 17:17] 우리가 작성한 Hello Controller에서 전송한 Hello Spring Boot라는 메시지가 화면에 나타났다면 애플리케이션이 정상적으로 시행되어 웹 요청을 처리하고 있다는 뜻입니다.
[3주차 2차시 17:32] 만약 이 메시지가 보이지 않거나 오류가 발생한다면 애플리케이션이 제대로 실행되지 않았거나 포트 번호, URL 경로 등을 잘못 입력한 것일 수 있으니까요.
[3주차 2차시 17:44] 잘 한번 확인해 보시길 바랍니다.
[3주차 2차시 17:47] 브라우저 외에도 포스트맨 같은 API 테스트 도구를 사용해서 확인할 수도 있습니다. 포스트맨은 설치한 후 [불명확: 실행해] 아까와 동일한 URL로 요청을 보내면 리스폰스 바디에 Hello Spring Boot라는 응답 결과가 표시가 됩니다.
[3주차 2차시 18:05] 그래서 이걸 활용하면 HTTP 요청과 응답의 상세한 내용을 함께 확인할 수 있기 때문에 API 개발이나 테스트를 진행할 때 훨씬 유용합니다.
[3주차 2차시 18:18] 마지막으로
[3주차 2차시 18:19] Spring Boot 애플리케이션을 종료하거나 다시 시작하는 방법입니다.
[3주차 2차시 18:28] 먼저 애플리케이션을 종료할 때에는 STS 컨솔 창에서 Ctrl-C를 누르거나 컨솔 또는 툴바에 있는 붉은 사각형 모양의 Stop 버튼을 클릭을 하면 쉽게 종료할 수 있습니다.
[3주차 2차시 18:43] 애플리케이션의 재시작 방법은 앞서 실행시켰던 방법과 동일하게 Run as Spring Boot 앱을 선택하시면 됩니다.
[3주차 2차시 18:54] 그럼 Spring Boot 프로젝트를 처음부터 생성을 한번 같이 해보도록 하겠습니다.
[3주차 2차시 19:02] 그럼 Spring Boot 프로젝트를 한번 생성해보도록 하겠습니다.
[3주차 2차시 19:09] 파일에서 New를 누르고 Spring
[3주차 2차시 19:12] [불명확: Startup]
[3주차 2차시 19:12] 프로젝트를 선택을 합니다.
[3주차 2차시 19:15] 이름을 HelloSpringBoot로 넣고,
[3주차 2차시 19:23] Type은, Maven, Java 버전은 17, Group, Artifact 등은 원하는 내용을 넣으시면 되는데 일단 기본 내용 그대로 두겠습니다.
[3주차 2차시 19:36] 패키지명은 대시가 없는 이름으로 넣겠습니다.
[3주차 2차시 19:44] 그리고 Next를 누르고 기본적으로 필요한
[3주차 2차시 19:46] Dependency를 선택을 해야 하는데요.
[3주차 2차시 19:49] Spring Web을 선택하고 Finish를 누르도록 하겠습니다.
[3주차 2차시 19:54] 그럼 이제 이렇게 Hello Spring Boot라는 프로젝트가 생성이 되었습니다. 아무것도 없는 빈 프로젝트이지만 한번 실행이 되는지 해보도록 하겠습니다.
[3주차 2차시 20:10] 프로젝트에서 오른쪽 [불명확: 마우스,] Run [불명확: As의]
[3주차 2차시 20:18] 스프링
[3주차 2차시 20:19] 부트 앱을 누르면 빌드 과정이 진행이
[3주차 2차시 20:22] 되고 콘솔에
[3주차 2차시 20:24] 스프링
[3주차 2차시 20:25] 부트가 실행되고
[3주차 2차시 20:26] 있는 로고를 볼 수가 있고요.
[3주차 2차시 20:29] 그리고 8080 포트에서 동작하고 있는 것도 확인을 할 수가 있습니다.
[3주차 2차시 20:39] 그럼 이제 헬로 컨트롤러 소스 코드를
[3주차 2차시 20:41] 넣어보도록 하겠습니다. 왼쪽에서 헬로
[3주차 2차시 20:45] 스프링 부트의 마우스 오른쪽 버튼하고
[3주차 2차시 20:49] 패키지를 추가하시고
[3주차 2차시 20:52] 컨트롤러 이름을
[3주차 2차시 20:54] 붙여주고 생성을 합니다.
[3주차 2차시 20:58] 만들어진 컨트롤러 패키지 밑으로 클래스를
[3주차 2차시 21:01] 추가하도록 하겠습니다.
[3주차 2차시 21:11] 클래스명은 HelloController로 해볼게요.
[3주차 2차시 21:19] 그러면 [불명확: 이제] 클래스에
[3주차 2차시 21:23] RESTController annotation을 추가를 해서 프레임워크가 인식하도록 합니다.
[3주차 2차시 21:33] 다음으로는 API라는 경로를 requestMapping으로 지정을
[3주차 2차시 21:38] 합니다.
[3주차 2차시 21:44] 이제 API 경로 밑으로 hello라는 경로가 들어왔을 때 처리하는 메소드를 만들어 보겠습니다.
[3주차 2차시 21:52] get 방식으로 받아들인다고 지정하기 위해서 getMapping annotation을 사용하고
[3주차 2차시 22:03] 메소드 이름은 sayHello, string으로 응답을 주려고 합니다.
[3주차 2차시 22:11] 그래서 보이는 시대로 [불명확: 좀] 작성하시고
[3주차 2차시 22:15] 메소드 안에는 특별한 처리 내용 없이 그냥 HelloStringBoot 문자열만 무조건 리턴하는 걸로 이제 메소드를 작성을 마치도록 하겠습니다 Ctrl S 눌러서 저장하시고
[3주차 2차시 22:30] 앞서 실행되어 있던 서버를 중단을
[3주차 2차시 22:33] 시킵니다 그리고 다시
[3주차 2차시 22:36] 프로젝트
[3주차 2차시 22:36] 실행을 하면
[3주차 2차시 22:40] 정상적으로 실행되었다면
[3주차 2차시 22:41] 웹브라우저에서 localhost 8080 api hello를 입력을
[3주차 2차시 22:48] 했을 때 화면에 Spring
[3주차 2차시 22:50] Boot 나오는
[3주차 2차시 22:52] 거 보실 수 있죠 여기까지가 가장 기본적인 웹 프로젝트 생성 과정이구요 한번 직접 따라해 보시길 바랍니다
[3주차 2차시 23:07] 그래서 Spring Boot 프레임워크를 활용을 하면 수많은 복잡한 과정들을 생략을 하고
[3주차 2차시 23:13] 곧바로 로직에 집중할 수 있다.
[3주차 2차시 23:19] 그럼
[3주차 2차시 23:20] 이번 차시 내용을 한번 요약 정리해 보도록 하겠습니다. 프레임워크는 소프트웨어 개발을 위한 구조와 규칙을 제공하는 코드 라이브러리다.
[3주차 2차시 23:31] 그리고 플랫폼은 애플리케이션이 실행될 수 있는 환경을 포괄적으로 칭하는 용어다.
[3주차 2차시 23:38] 스프링부트 프레임워크는 스프링 프레임워크를 기반으로 빠르게 자바의 맵 애플리케이션을 만들 수 있도록 지원을 하고 스프링 이니셜라이저를 사용하면 신규 프로젝트를 생성하고 개발할 수 있다.
[3주차 2차시 23:57] [불명확: 참고문안이고요.] 2차시
[3주차 2차시 24:00] 수업 여기까지 하도록 하겠습니다. 감사합니다.

# [3-TRANSCRIPT] 3주차 3차시 — Spring Boot 개발 환경·실습
키워드: PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Mass Assignment/대량 할당/DTO/isAdmin

[3주차 3차시 00:01] [불명확: 네,]
[3주차 3차시 00:03] 3차시 수업 시작하도록
[3주차 3차시 00:05] 하겠습니다. 이번 차시는 실습 환경 구축 3번째 시간으로 스프링부트 프레임워크를 활용한 웹 프로젝트 구축 2번째로 이어가 보도록 하겠습니다.
[3주차 3차시 00:23] 이번 차시의 목표입니다. 이번에는 보다 고도화된 스프링부트 프로젝트를 만들 예정입니다.
[3주차 3차시 00:31] 아주 간단한 게시판의 백엔드 프로그램을 만들어 보도록 하겠습니다. 이에 따른 학습 내용은
[3주차 3차시 00:39] 다음과 같습니다. 만들게 되는 게시판 코드의 구조를 이해하고 코드 입력과 빌드 실행 과정을 확실히 익혀 보도록 하겠습니다.
[3주차 3차시 00:53] 그럼 설계 과정부터 시작해서 순차적으로 게시판 기능을 완성해 보도록 하겠습니다.
[3주차 3차시 01:00] 개발하기에 앞서 어떤 기능이 필요한지를 정의해보고 이에 따라 데이터 모델을 설계해 나가도록 하겠습니다. 이번 실습에 프론트엔드 쪽 개발은 포함하지 않았습니다만 여러분들이 나중에 프론트엔드를 붙이고 기능을 고도화해 나가도 좋은 경험이 될 것 같습니다.
[3주차 3차시 01:23] 우선 게시판에서 기본적으로 제공되어야 하는 5가지 동작이 나와 있는데요.
[3주차 3차시 01:29] 각 동작들은 Create, Read, Update, Delete로 이어지는 CRUD 작업에 해당하는데요.
[3주차 3차시 01:38] 이 기능은 웹 애플리케이션의 기본이며, 이번에 구현하려고 하는 간단한 게시판의 핵심 구성 요소가 됩니다.
[3주차 3차시 01:48] 오른쪽 표는 각 기능들을 구현하기 위한 데이터 모델, 즉 엔티티 클래스의 구조를 설정해 본 것입니다. 총 4개의 필드로 구성이 되어 있는데요.
[3주차 3차시 01:59] 아이디는 각 게시글에 고유하게 식별하기 위한 값이며, 롱 타입으로 프라이머리 키입니다. 타이틀은 게시글의 제목, 컨텐츠는 본문 글 내용, 마지막으로 create [불명확: as은] 게시글이 작성된 시점을 저장하기 위한 필드인데, Java 8 이상에서 날짜와
[3주차 3차시 02:22] 시간을 다룰 때 주로 사용하는 로컬 데이트 타입으로 정의를 했습니다.
[3주차 3차시 02:29] 실제 코드로 작성될 클래스는 이 구조를 기반으로 해서 데이터베이스 테이블과 연결되는 핵심적인 객체가 됩니다.
[3주차 3차시 02:45] 그럼 게시판 기능을 어떻게 API로 구현할지 한번 살펴보도록 하겠습니다.
[3주차 3차시 02:54] 앞에서 살펴본 게시판의 주요 기능들을 각각 HTTP 메소드와 URL 경로, 그리고 요청과 응답 데이터 구조를 정해서 구체화합니다.
[3주차 3차시 03:05] 먼저 게시글 작성 기능입니다. HTTP 매서드는 포스트를 사용하고 URL 경로는 slash post입니다.
[3주차 3차시 03:16] 요청 시에는 게시글의 타이틀과 컨텐츠를 포함한 JSON 데이터를 만들어 전달하도록 하고, 응답으로는 생성된 게시글의 아이디, 타이틀, 컨텐츠, 크리에이트 [불명확: 앱] 같은 필드들이 포함된 JSON이 반환되도록 정의를 해봅니다.
[3주차 3차시 03:36] 다음은 모든 게시글 조회 기능, 즉 목록을 표시하기 위한 기능입니다. 이 기능은 동일한 경로에 대해 get 메소드를 사용합니다.
[3주차 3차시 03:48] 요청 데이터는 없고, 응답은 모든 게시글들의 배열 형태로 전달되며, 각 게시글마다 기본 필드들이 포함됩니다.
[3주차 3차시 03:59] 게시글 상세 조회 기능도 역시 get 메소드를 사용하지만, URL 경로는 postd의 id처럼,
[3주차 3차시 04:07] 게시글의 아이디를 포함한 경로를 사용합니다. 그리고 그 결과로는 해당 아이디에 해당하는 게시글의 정보를 단건으로 응답을 받습니다.
[3주차 3차시 04:21] 게시글 수정 기능은 put 메서드를 사용합니다. 경로 지정 방식은 앞과 동일하고 요청 데이터에는 수정할 타이틀과 컨텐츠를 포함합니다.
[3주차 3차시 04:33] 그에 대한 응답은 수정된 게시글의 전체 정보를 다시 받는 것입니다.
[3주차 3차시 04:39] 마지막으로 게시글 삭제 기능은 Delete Method입니다. 역시 같은 형태의 URL을 사용하며 단순히 성공 또는 실패 메시지만 반환하면 됩니다.
[3주차 3차시 04:52] 여기까지 아주 간단한 게시판 기능들을 RESTful API 형태로 설계를 해보았습니다. 이제 실제 코드로 한번 만들어 보도록 하겠습니다.
[3주차 3차시 05:04] 이제 게시판 기능을 구현하기 위해서 먼저 개발 환경을 한번 설정을 해보도록 하겠습니다. 스프링붓 프로젝트를 생성하고 설정하는 과정은 앞서 간단하게 실습을 해봤었죠.
[3주차 3차시 05:20] 이번에는 스프링 이니셜라이저와 STS에서 생성하는 방법 중 STS에서 만드는 방법으로 한번 해보도록 하겠습니다.
[3주차 3차시 05:30] 프로젝트 설정 방법은 기본적인 세팅을 그대로 사용하면서 필요한 라이브러리만 Dependency로 추가를 해주면 됩니다.
[3주차 3차시 05:40] REST API 형태의 웹 애플리케이션을 만들게 도와주는 Spring Web Library, 그리고 DB 연동 쪽을 도와주는 JPA를 일단 선택해야 합니다.
[3주차 3차시 05:53] 다음으로 실제 데이터를 저장하는 데이터베이스가 있어야 하는데요.
[3주차 3차시 05:57] 우리는 간단한 실습을 위해서 H2라는 메모리 기반 테스트 데이터베이스를 사용하겠습니다. 이 데이터베이스는 따로 스토리지에 저장하는 기능이 없기 때문에 실행할 때마다 내용이 비어있는 상태로 시작을 하게 됩니다.
[3주차 3차시 06:16] 실제 운영에 그래서 사용할 수는 없지만 별도로 데이터베이스를 구축하고 설정하지 않아도 되고
[3주차 3차시 06:23] 매번 간편하게 초기화 되니까 코드 개발 및 테스트용으로는 딱 알맞습니다. 그리고는 롬복을 사용하면 게터 세터를 일일이 코딩하지 않아도 되기 때문에 편리합니다.
[3주차 3차시 06:43] 이렇게 프로젝트를 생성하도록 할 텐데요. 뒤에 시연 영상으로도 실제 과정을 한번 보여드리도록 하겠습니다.
[3주차 3차시 06:52] 그러면
[3주차 3차시 06:54] 이제 본격적으로 코드를 입력하려고 하는데요
[3주차 3차시 07:00] 화면에 나와 있는 것처럼 프로젝트 구조를 구성하려고 합니다. 우리가 생성한 Spring Boot 프로젝트에 몇 가지 종류의 패키지를 추가하고 그 안에 필요한 클래스 파일들을 넣으려고 합니다.
[3주차 3차시 07:15] 일단은 컴, 이그젠플, 보드 순서대로 패키지 계층을 만들고 그 아래에는 크게 5개의 하위 페이지를 만들도록 하겠습니다.
[3주차 3차시 07:27] 먼저 컨트롤러는 사용자의 요청을 받아들이는 역할을 합니다. 예를 들어 게시글을 등록하거나 조회하는 요청이 우선 이곳으로 유입이 됩니다.
[3주차 3차시 07:39] 그리고 서비스는 비즈니스 로직을 수행하는 계층으로 게시글을 저장하거나 수정하는 등의 실제 게시판 처리 로직을 수행하며 컨트롤러와 레포지토리 사이의 중간다리 역할을 합니다.
[3주차 3차시 07:54] 레포지토리는 데이터베이스와 직접 통신하는 역할을 하는데요.
[3주차 3차시 07:59] Spring Data JPA를 사용하면 이 클래스가 JPA 레포지토리를 상속하도록 하는 것만으로 기본적인 CRUD 기능의 메소드들을 사용할 수 있게 되므로 정말 편리합니다.
[3주차 3차시 08:13] 다음으로 DTO는 Data Transfer Object의 약자인데요. Request로 유입되는 데이터와 Response로 내보낼 데이터를 담아두기 위한 클래스들을 넣습니다.
[3주차 3차시 08:26] 예를 들어 PostRequestDTO 같은 경우는 사용자가 작성한 게시글을 전달받을 때 이 클래스 형태로 담아 사용합니다.
[3주차 3차시 08:36] 마지막으로 Entity는 실제 테이블과 맵핑되는 클래스를 넣습니다. 여기서는 Post라는 클래스로 게시글 정보 구조를 표현하고 있습니다.
[3주차 3차시 08:47] 그리고 한 가지 더
[3주차 3차시 08:49] 왼쪽 그림에서 맨 아래 있는 MainApplication.java는 프로젝트를 실행하는 진입점, 즉 메인 클래스입니다.
[3주차 3차시 09:01] 이제 첫 번째로 보여드리는 코드는 Entity 클래스로 게시글 정보를 담을 객체입니다.
[3주차 3차시 09:11] 앞 실습에서 설명했던 내용이더라도 다시 한번 설명드리도록 하겠습니다.
[3주차 3차시 09:18] 이 클래스에서 골뱅이 엔티티는 이 클래스가 JPA에서 관리하는 엔티티 객체로 인식하라고 지정하는 것입니다.
[3주차 3차시 09:28] 이렇게 하면 이 클래스는 데이터베이스 테이블과 1대1로 맵핑이 됩니다. 테이블 이름은 클래스명과 동일하게 생성되므로 포스트라고 만들어집니다.
[3주차 3차시 09:42] 그럼 각 필드들을 한번 살펴볼까요?
[3주차 3차시 09:45] long 타입의 id는 게시글의 고유 인덱스 값입니다. 여기에 [불명확: at] 골뱅이 id를 붙이면 이 필드를 db의 primary key 즉 기본 키로 사용하면 된다는 뜻이며 [불명확: 그] 다음에 generated value로
[3주차 3차시 10:07] 지정한 것은 db에서 값을 자동 증가시키는 방식으로 생성하라는 뜻이 됩니다.
[3주차 3차시 10:14] 다음으로 문자열 타입의 타이틀과 컨텐츠가 [불명확: 있죠.] 스트링 타입으로 그리고 크리에이티드 앳의 경우는 게시글의 생성 날짜를 저장하는 필드입니다.
[3주차 3차시 10:26] 초기화 값으로 로컬 데이트 타임에 now를 호출하고 있으므로 객체가 생성될 때 현재 시각이 자동으로 들어가게 됩니다.
[3주차 3차시 10:38] 아직 설명하지 않은 어노테이션들이 많이 있는데요. 이 클래스에 붙어있는 getter, setter, no-arg constructor들은 모두 롬복 어노테이션입니다.
[3주차 3차시 10:52] 이걸 지정하면 개발자는 따로 getter, setter 메소드를 작성할 필요 없이 자동으로 생성되도록 할 수 있습니다. 그리고 no-argument constructor는
[3주차 3차시 11:15] NoArgument constructor는 인수가 없고 비어있는 constructor를 자동으로 만들어줍니다.
[3주차 3차시 11:24] 이제 Spring Data JPA는 이 객체를 이용하여 테이블을 생성하거나 데이터를 저장할 수 있도록 도와줍니다. 그럼 이 Entity를 기반으로 데이터에 접근할 수 있으므로 Repository를 만들어 보도록 하겠습니다.
[3주차 3차시 11:44] Repository 클래스는 이렇게 한번 만들어 보겠습니다.
[3주차 3차시 11:49] String Data JPA를 사용하게 되면 별도의 구현을 하지 않더라도 인터페이스 선언만으로 다양한 기능을 제공받게 됩니다.
[3주차 3차시 12:00] Post Repository 클래스는 JPA Repository를 상속하고 있는데요. Post Long은 엔티티로 사용하는 클래스 이름과 해당 클래스의 Primary Key의 Type입니다.
[3주차 3차시 12:12] 이 인터페이스를 상속하면 기본적인 CRUD 메소드들을 자동으로 제공하게 되는데 예를 들어보면 엔티티를 저장할 수 있는 save, 모든 게시글을 조회할 수 있는 find all, 아이디 값으로 특정 게시글을 조회할 수 있는 find by id, 지정한 게시글을 삭제하는 delete by id를 사용할
[3주차 3차시 12:35] 수 있게 됩니다. 레포지토리의 코드는 단 한 줄이지만 매우 많은 기능을 [불명확: 제공을] 하고 있습니다.
[3주차 3차시 12:46] 그 다음에 이 짧은 소스 코드는 클라이언트로부터 요청 데이터를 받기 위한 DTO 클래스인데요. Post Request DTO 클래스는 타이틀과 컨텐츠 두 개 필드를 가지고 있습니다.
[3주차 3차시 13:01] 게시글의 제목과 내용을 담고 있는 객체이며 사용자가 작성한 게시글 데이터가 이 DTO 클래스에 담겨져 서버로 전달됩니다.
[3주차 3차시 13:12] 여기에서도 골뱅이 게터 어노테이션이
[3주차 3차시 13:17] 붙어 있어서 이 타이틀과 컨텐츠의 getter 메서드가 자동으로 생성됩니다. 이 DTO 클래스는 제이슨 형태로 유입되는 리퀘스트 데이터와 바로 맵핑되어 컨트롤러에서 사용할 수 있습니다.
[3주차 3차시 13:38] 이번에는 서버가 클라이언트에게 응답을 보낼 때 사용하는 DTO, post-response-dto.java의 소스 코드입니다.
[3주차 3차시 13:50] 앞에서 만든 Post Request DTO가 사용자로부터 요청 데이터를 받을 때 사용되었다면, 이 Post Response DTO는 반대로 서버가 클라이언트에게 응답을 보낼 때 사용을 합니다.
[3주차 3차시 14:04] 이 클래스는 게시글의 제목, 본문, 생성일자 이렇게 세 가지 필드를 가지고 있으며, 프론트엔드 쪽이나 테스트 툴, 포스트맨 같은 것을 통해 수신된 응답 데이터를 확인할 수 있게 됩니다.
[3주차 3차시 14:20] 조금 눈여겨볼 부분이라면 컨스트럭터 즉 생성자에서 포스트 엔티티를 직접 받아 각 필드에 맵핑을 한다는 점입니다.
[3주차 3차시 14:31] 서비스나 컨트롤러에서 게시글을 조회하게 되면 그 결과를 그대로 보내지 않고 이 DTO에 옮겨 담은 후 반환하고 있는 것입니다.
[3주차 3차시 14:42] 이렇게 하면 데이터베이스 구조가 그대로 드러나는 엔티티 객체 그대로 외부에 노출되는 것을 [불명확: 방지할] 수가 있고
[3주차 3차시 14:50] 필요한 정보만 선택적으로 전달할 수 있으므로 보안과 유지 보수 측면에서 매우 유리합니다. 그럼 다음으로 [불명확: 이] 요청과 응답용 DTO들을 실제로 활용하는 서비스 클래스를 만들어 보도록 하겠습니다.
[3주차 3차시 15:10] 서비스 클래스는 컨트롤러에서 전달된 요청을 처리하고 데이터베이스와 연결된 레포지토리와 직접 상호작용을 합니다.
[3주차 3차시 15:20] 먼저 클래스 선언부를 보면 서비스를 붙여서
[3주차 3차시 15:24] 서비스 빈으로 자동 등록하도록 지정하였습니다. 그리고 포스트 레포지토리 변수를 파이널로 선언해놓고 생성자 주입을 통해 주입하고 있습니다.
[3주차 3차시 15:37] 메소드들을 간단하게 둘러보자면 getAllPost 메소드는 전체 게시글을 조회하는 기능이 구현이 되어 있고
[3주차 3차시 15:46] 레포지토리의 findAll을 통해 모든 게시글을 가져온 뒤 자바 스트림을 이용해서 각 게시글을 PostResponse DTO로 변환한 후 리스트로 [불명확: 반환하고] 있습니다.
[3주차 3차시 16:00] DTO 변환 작업을 맵과 컬렉트를 활용하여 간결하게 만들었습니다. 그 다음으로 GetPostByIdMethod는 ID값으로 특정 게시글을 조회하는 기능입니다.
[3주차 3차시 16:14] find by 아이디를 호출한 다음, 해당 아이디에 해당하는 게시글이 없으면 or else throw로 예외를 발생시키지만, 정상적으로 게시글이 존재한다면 이를 post-response DTO로 감싼 다음에 반환합니다.
[3주차 3차시 16:31] 이어서 create post는 이 게시글을 생성하는 기능입니다. 입력받은 post-request DTO를 기반으로 새로운 post 객체를 만들고,
[3주차 3차시 16:45] 제목과 내용을 설정하여 데이터베이스에 자동으로 저장합니다. 그리고 저장된 게시글을 DTO 형태로 다시 변환한 다음 돌려주게 됩니다.
[3주차 3차시 16:57] 업데이트 포스트는 기존 게시글을 수정하는 기능인데요. 먼저 아이디로 기존 게시글을 조회한 후 요청으로 전달된 제목과 내용을 반영해 DB Entity를 수정합니다.
[3주차 3차시 17:10] JPA에서는 이처럼 Entity의 값을 바꾸기만 해도
[3주차 3차시 17:14] 자동으로 변경한 내용이 반영이 되기 때문에 별도로 세이브를 호출하지 않아도 됩니다. 그리고 [불명확: 이] 골뱅이 [불명확: 트랜잭셔너를] 붙였는데요.
[3주차 3차시 17:28] 이렇게 하면 트랜잭션 처리가 [불명확: 부당이] 되어서 데이터 동시 접근에 따른 무결성이 깨지는 것을 막을 수 있습니다. 마지막으로 딜리트 포스트는 게시글 삭제 기능입니다.
[3주차 3차시 17:41] DeleteByID를 호출하여 해당 아이디에 대응되는 게시글을 삭제를 합니다. 지금까지 본 것처럼 서비스 클래스는 컨트롤러보다 더 중요한 로직을 담당하는 계층으로 DTO와 엔티티 간 변환, 예외 처리, 트랜잭션 처리 등을 종합적으로 관리합니다.
[3주차 3차시 18:05] 이제 마지막 단계로 컨트롤러 클래스 살펴보도록
[3주차 3차시 18:09] 하겠습니다.
[3주차 3차시 18:11] 이미 알고 있듯이 포스트 컨트롤러는 사용자 요청을 직접 받는 역할을 합니다. [불명확: 클래스] 상단에 REST 컨트롤러를 지정해서 이 클래스에서 REST API 요청을 처리한다는 것을 Spring Framework에 알려주고 Request Mapping slash Post를 통해
[3주차 3차시 18:33] Post로 시작하는 모든 경로를 처리하겠다는 것을 인식을 시킵니다.
[3주차 3차시 18:39] 컨트롤러에서는 서비스 객체를 주입받은 다음 각 요청에 맞는 작업을 알맞은 서비스로 넘기고 그 응답을 받아서 클라이언트에 전달하는 역할을 하게 됩니다.
[3주차 3차시 18:53] 첫번째 메소드인 getAllPost는 그냥 getMapping으로 지정되어 있어서 포스트 뒤에 아무것도 없이 HTTP GET 요청을 받으면 전체 게시글을 반환을 합니다.
[3주차 3차시 19:06] 두번째는 getPost인데요.
[3주차 3차시 19:08] 요청하는 URL에서 게시글 아이디를 [불명확: 추출해서] 그 아이디에 해당하는 게시글을 조회하고 응답으로 돌려줍니다.
[3주차 3차시 19:17] Create Post는 새로운 게시글을 등록하는 메소드입니다. HTTP Post 요청과 함께 들어온 JSON 데이터를 골뱅이 Request Body를 통해 받은 다음
[3주차 3차시 19:34] 서비스를 통해 저장하고 결과를 반환합니다.
[3주차 3차시 19:39] 그 다음 업데이트 포스트는 http put 요청을 받아 게시글을 수정하는데요. 아이디와 수정 내용을 함께 받아서 해당 게시글을 수정하고 결과를 응답합니다.
[3주차 3차시 19:53] 마지막 딜리트 포스트는 http 딜리트 요청으로 게시글을 삭제하는 기능인데요. 아이디만 전달받아서 삭제 처리하게 되며 따로 응답 데이터는 없습니다.
[3주차 3차시 20:06] 이렇게 컨트롤러는 요청을 받고 필요한 처리를 서비스에 넘기고 클라이언트 입장에서는 이 계층과 직접 통신을 하게 됩니다.
[3주차 3차시 20:20] 이런 식으로 만든 게시판 코드는 메인 어플리케이션 클래스에서 실행시키면 되는데요. 실행이 잘 되고 나면 내 [불명확: 컴퓨터에] 8080 포트로 접속을 해서 [불명확: 만들어놓은] REST API를 사용해 볼 수 있습니다.
[3주차 3차시 20:36] 따로 프로그램을 개발하지 않고 편리하게 API 테스트를 할 수 있는 포스트맨을 활용하면 좋습니다. 포스트맨을 통해 CRUD 각 기능별로 원하는 동작을 수행하는지 확인해 보면 되는데 구체적인 내용은 다음 시연 영상으로 보여드리도록 하겠습니다.
[3주차 3차시 20:59] 앞에서 설명한 대로 한번 프로젝트 만들어 보도록 하겠습니다.
[3주차 3차시 21:07] 그래서 이 코드 소스 코드 대부분은 앞에 있는 거 그대로니까요 제가
[3주차 3차시 21:17] 작성하는 과정은 좀 배속으로 넘어 가는데 [불명확: 여러분] 한번 직접 타이핑을 해 보시면 도움이 많이 될 것 같습니다
[3주차 3차시 21:33] 스프링 스타터 프로젝트 이용해서 프로젝트를
[3주차 3차시 21:38] 만들어 주시고요 다른 내용들은 디폴트 그대로 두고
[3주차 3차시 21:45] 패키지 이름만 com.example.board라고 지정을 해주도록 하겠습니다.
[3주차 3차시 21:51] 그래서 넘어가서 Dependency에서 Spring Web, H2, Lombok, Spring Data JPA를 차례대로 선택을 해줍니다.
[3주차 3차시 22:10] 그리고
[3주차 3차시 22:11] Finish 눌러주시고 이제 만들어진 프로젝트가 정상적으로 빌드 되는지 보도록
[3주차 3차시 22:17] 하겠습니다.
[3주차 3차시 22:23] 정상적으로 빌드되어 서버가 올라오는 것을 확인을 했고요. 이제 소스 코드를 하나씩 넣어보도록 하겠습니다. 패키지 폴더 하단으로
[3주차 3차시 22:33] NTD
[3주차 3차시 22:35] 패키지부터 만들고 그리고
[3주차 3차시 22:41] 이 안에서 클래스를
[3주차 3차시 22:43] 생성을 합니다. 소스 코드는 슬라이드에 있는 내용 그대로 입력을
[3주차 3차시 22:48] 하겠습니다.
[3주차 3차시 23:08] 그 다음은 레포지토리 똑같이 패키지 만들어 주시고요.
[3주차 3차시 23:15] 그 다음에 클래스
[3주차 3차시 23:21] 이름은 포스트 레포지토리 그리고
[3주차 3차시 23:25] 여기선 인터페이스만 정의를 해주면 됩니다.
[3주차 3차시 23:29] 다음으로는 DTO 만들겠습니다. 첫
[3주차 3차시 23:33] 번째 클래스명은 포스트 리퀘스트 DTO였죠.
[3주차 3차시 23:45] 그리고 소스 코드 똑같이
[3주차 3차시 23:47] 넣습니다. 다음으로는 응답 내용을 만드는 포스트 리스폰스 DTO 만들겠습니다.
[3주차 3차시 23:58] 여기에도 소스 코드 넣어주시고요.
[3주차 3차시 24:04] 교재 내용 그대로 넣으면 되긴 하는데요. 실제 개발할 때는 이 컨스트럭터 각 필드 내용을 주입하는 경우가 많기 때문에 자동화 기능을 쓰면 편리합니다.
[3주차 3차시 24:16] 그래서 generate constructor using field에서 필드 선택해주시면
[3주차 3차시 24:23] 이렇게 자동으로 만들어주기도 합니다.
[3주차 3차시 24:27] 하지만 우리는 이제 엔티티 클래스로 받아야 하니까
[3주차 3차시 24:32] 조금 맞춰
[3주차 3차시 24:33] 주도록 하겠습니다 각 필드마다 적절한 엔티티 내용이 주입되도록 이렇게 수정을 해 주도록 하겠습니다 그런
[3주차 3차시 24:53] 다음으로는 서비스 패키지 만들겠습니다 이건 역시 포스트
[3주차 3차시 24:58] 서비스 라는 클래스 만들어서 슬라이드에 있는 소스 코드 입력해 주시면
[3주차 3차시 25:05] 되겠습니다
[3주차 3차시 25:21] 소스 입력 하다보면
[3주차 3차시 25:24] [불명확: SDS가] 지속적으로 추천하는 내용들이 나타나는데
[3주차 3차시 25:27] 이를 잘 활용하면 입력 시간을 줄이실 수 있습니다.
[3주차 3차시 26:16] 이렇게 Delete Post까지 하고
[3주차 3차시 26:18] 컨트롤러 패키지도 만들어 주도록 하겠습니다.
[3주차 3차시 26:27] PostController라는 [불명확: 이름으로] 클래스 만들고 소스코드 입력하겠습니다.
[3주차 3차시 27:07] 꼭 한번 직접 입력해 보시길 바랍니다.
[3주차 3차시 27:27] 이제
[3주차 3차시 27:27] 입력한 내용들이 잘 동작하는지 한번 실행해 보겠습니다.
[3주차 3차시 27:32] 저장 안됐다면 먼저
[3주차 3차시 27:34] 저장해주시고 패키지에서
[3주차 3차시 27:36] 스프링 부트
[3주차 3차시 27:37] 앱을 [불명확: 실행을] 합니다 8080 포트에 정상적으로 실행되는거 확인 됐구요
[3주차 3차시 27:44] 미리 준비해둔 포스트맨으로 한번 테스트 해보겠습니다 설치가 어렵지 않으니까요 포스트맨 공식 사이트에서 다운로드 받아서 설치 한번 해주세요 우선 게시글 내용들을 한번 받아보려고 하는데요
[3주차 3차시 27:59] Get
[3주차 3차시 28:00] 방식 선택하고 로컬 [불명확: 포스트] 8080 포트로 포스트를 주면 전송해보면
[3주차 3차시 28:07] 하단 결과에 내용이 비어있는 [불명확: 대괄으로만] 보이는데 현재 등록되어 있는 글이 없다는 뜻입니다. 그럼 글을 하나 등록해보겠습니다.
[3주차 3차시 28:18] 그래서 포스트 방식으로 바꾼 다음에 보이는
[3주차 3차시 28:21] 것처럼 로 타입의 제이슨 형태로 글 제목이랑
[3주차 3차시 28:25] 내용 한번 넣어보겠습니다. 그렇게
[3주차 3차시 28:28] 전송을
[3주차 3차시 28:29] 해보면 처리 결과를 아래처럼 받아볼 수 있습니다. [불명확: 그래서] 글 번호는 1이고 생성일자가 함께 수신된 것이 확인이 됩니다.
[3주차 3차시 28:40] 그럼 이제 다시 한번 모든 글 조회를 이제
[3주차 3차시 28:42] 해보겠습니다.
[3주차 3차시 28:47] 그러면 아까와 마찬가지로 등록된 한 개의 글 내용이 수신이 되었죠. 이번에는 글을 하나 더 등록해 보겠습니다.
[3주차 3차시 29:03] 잘 등록이 되었고 2번으로 생성이 되었습니다.
[3주차 3차시 29:07] 다시
[3주차 3차시 29:08] 조회를
[3주차 3차시 29:09] 해보면 두
[3주차 3차시 29:11] 개의 글 내용 모두 다 받아볼 수가 있고 한번
[3주차 3차시 29:15] 1번
[3주차 3차시 29:15] 삭제해볼까요?
[3주차 3차시 29:17] 딜리트 URL에
[3주차 3차시 29:20] 글번호를 추가하여 전송을 하면
[3주차 3차시 29:22] 정상적으로 삭제되고 특별히 응답은 없습니다.
[3주차 3차시 29:28] 다시
[3주차 3차시 29:29] 모든 글을 받아보면 2번
[3주차 3차시 29:32] 글만 남아있는 것을 보실 수가 있고
[3주차 3차시 29:35] 글 하나만 번호를 지정해서
[3주차 3차시 29:43] 수정도
[3주차 3차시 29:45] 한번
[3주차 3차시 29:45] 해보겠습니다. [불명확: put] 방식으로
[3주차 3차시 29:49] 번호를
[3주차 3차시 29:50] 1번으로
[3주차 3차시 29:50] 바꿔놓고
[3주차 3차시 29:54] 여기까지
[3주차 3차시 29:56] 이제 네
[3주차 3차시 29:59] 이렇게 뭐 간단하게 게시판 백엔드 서버 개발 실습 해봤는데요.
[3주차 3차시 30:11] 이번 차시 내용을 한번 요약해 보도록 하겠습니다. 우리 이번 차시에서 간단한 게시판 백엔드 api 서버를 만들어 봤고요.
[3주차 3차시 30:20] 만들고 읽고 기록하고 삭제하는 CRUD 기능 중심으로 아주 간단하게 구성을 해봤죠. 그리고 DB와 맵핑하고자 하는 엔티티에 JPA 어노테이션을 지정하여 바인딩을 시켰습니다.
[3주차 3차시 30:35] 레포지토리의 경우 JPA 레포지토리를 상속을 시켜서 기본 기능이 자동으로 만들어지도록 하였고 서비스 계층에서는 DTO를 정의하고 비즈니스 로직을 처리를 하였습니다.
[3주차 3차시 30:49] 그리고 마지막으로는 테스트를 간편하게 하기 위해 포스트맨을 활용을 해서 해봤습니다.
[3주차 3차시 31:01] [불명확: 참고문안이고요.]
[3주차 3차시 31:03] 3차시 수업 여기까지 하도록 하겠습니다. 감사합니다.

