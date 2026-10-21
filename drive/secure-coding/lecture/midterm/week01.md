# WEEK01 — 1주차 보안약점과 시큐어코딩 개요 (시큐어코딩 중간고사 주차 묶음)

> 이 파일 하나에 1주차의 교안 퀴즈(1-QUESTIONS, 신뢰도 A) · 정리(4-NOTES, C~D) · 교안 원문(2-SLIDES, A) · 강의 발화(3-TRANSCRIPT, B)가 모두 있다.
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

---

# [4-NOTES] 1주차 관련 정리 (신뢰도 C~D) — 교안·발화가 다른 지점. 시험 답은 교안 우선.

## [4-NOTES] 1주차 · 교안/발화 세부 불일치 모음 (C)
키워드: 보안약점, CVE, CSAP, SolarWinds, SP800-64
- 1주차 발화 곳곳에 세부 수치·연도·사례의 오인식·착오가 있음(예: 표준 연도, CVE 번호 표현, 공급망 공격 사례 용어). 세부 수치는 교안 원문([2-SLIDES] 1주차)을 기준으로 확인.
- [1주차 1차시 25:45] "승환구조" 구간은 자동 전사 불명확 — 원음 재확인 필요(미해결).

## [4-NOTES] 공통 · 자동 전사 한계 (C)
키워드: 녹취, 자동 전사, 불명확, 음성 인식
- 3-TRANSCRIPT는 자동 전사라 영문 용어·숫자·포트·메서드명에 오인식이 있을 수 있음([불명확]·[표현 차이] 표시). 숫자·코드·정확한 용어는 2-SLIDES(교안)를 우선.
- 6·7주차 녹취는 화면 기록이 없어 교수님 펜 강조 위치를 알 수 없음. 7주차는 1차시 앞부분(시험 안내)과 3차시 중간에 무음 구간이 있어 누락 가능.

## [4-NOTES] 시험 안내 (B, 발화 근거)
키워드: 중간고사, 시험, LMS, 온라인, 범위
- [7주차 1차시 00:00] 발화: 8주차에 중간고사, LMS 온라인 실시간, 공지사항 확인 요망. 범위는 "오늘까지 수업 내용"(1~7주차).
- 시험 규정(사용자 확인): 2026-10-22(목) 19:00~20:00, 온라인 LMS 퀴즈, AI·오픈북 가능, 범위 1~7주차. 날짜·시간은 LMS 공지로 최종 확인.

---

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

---

# [3-TRANSCRIPT] 1주차 1차시 — 보안약점과 시큐어코딩 개요
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · HTML Encoding/HTML 인코딩/이스케이프/Escape/엔티티/Entity/escapeHtml/textContent · ORM/Object-Relational Mapping/객체 관계 매핑/JPA/Hibernate/하이버네이트 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · IDOR/Insecure Direct Object References/직접 객체 참조/수평 권한/수직 권한/권한 상승 · Threat Modeling/위협 모델링/STRIDE/스트라이드/DREAD/드레드/MS-SDL/MTMT · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

[1주차 1차시 00:01] 안녕하세요. 저는 이번 학기 시큐어 코딩 강의를 담당하게 된 강원대학교
[1주차 1차시 00:06] 이동재입니다. 비대면 온라인 동영상 강의로 진행되긴 하지만, 한 학기 동안 잘 부탁드립니다. 본 교과목은 안전하게 소프트웨어를 개발하는 방법에 대해서 다루는데요.
[1주차 1차시 00:20] 설계 단계에서부터 구현 단계까지 어떻게 시큐어 코딩을 할 수 있을지를 다룰 예정입니다.
[1주차 1차시 00:26] 본 수업은 총 15주차로 진행되며 8주차와 15주차에는 각각 중간고사와 기말고사가 있으니 참고하시길 바랍니다.
[1주차 1차시 00:35] 그럼 1주차 1차시 시작하도록 하겠습니다.
[1주차 1차시 00:41] 이번 차시에서 학습할 내용은 소프트웨어 개발 보안의 이해로 첫번째 현대 애플리케이션 보안과제 그리고 두번째 사고사례를 통한 시큐어 코딩의 이해 이렇게 두가지 주제로 나눠서
[1주차 1차시 00:57] 강의를 진행하도록 하겠습니다. 학습
[1주차 1차시 01:01] 목표는 다음과 같습니다. 먼저 현대 애플리케이션의 보안과제를 이해하고 현대 애플리케이션 보안과제를 해결하기 위한 방안을 이해하고 마지막으로 사고 사례를 통한 시큐어 코딩을 이해하도록 하겠습니다.
[1주차 1차시 01:17] 첫 번째 주제 현대 애플리케이션 보안과제에 대해서 설명하도록 하겠습니다.
[1주차 1차시 01:24] 먼저
[1주차 1차시 01:27] 개인정보위원회에서 제공하는 자료를 한번 살펴보면 최근 3년간 개인정보 유출사고가 지속적으로 늘어나고 있는 것을 볼 수가 있습니다.
[1주차 1차시 01:38] 이 중에서 특히 2024년 개인정보 유출사고의 원인 분석 결과를 한번 보면 해킹이 171건으로 유출사고의 약 55%의 원인으로 나타나고 있는데요.
[1주차 1차시 01:52] 해킹의 세부 유형으로는
[1주차 1차시 01:56] 관리자 페이지의 비정상 접속이 가장 많은 원인이 되고 있으며 SQL 인젝션, 크로스 사이트 스크립트, 웹쉘, 파라미터 변조와 같은 보안 취약점들이 사고의 원인임을 알 수가 있습니다.
[1주차 1차시 02:14] 앞서
[1주차 1차시 02:14] 봤듯이 크로스 사이트 스크립트나 SQL 인젝션 등 비교적 익숙한 유형들이 여전히 보안 사고의 원인이 되고 있음을
[1주차 1차시 02:26] 볼 수 있었는데요. 이는 아직도 소프트웨어 개발 보안 인식이 부족하다는 것을 증명하고 있는데 국내 소프트웨어들이 잘 알려진 보안 취약점에 대해서도 잘 대응하지 못하고 있다고 볼 수 있겠습니다.
[1주차 1차시 02:44] 이에 대해서 OECD에서도 취약점은 디지털 생활의 일부로 보고 있으며 모든 취약점을 제거하는 것은 불가능하다고 하기도 합니다.
[1주차 1차시 02:56] 그래서 취약점이 드러나는 것을 사업 리스크나 잘못으로 받아들이기보다는 일상적인 현상으로 이해하고 관련 제보 체계 및 지속적인 보안 업데이트를 정착시켜야 한다는 보고서가 나와서 눈길을 끌기도 했습니다.
[1주차 1차시 03:14] 소프트웨어를 개발하는 단계에서 보안 취약점이 최대한 발생하지 않도록 소프트웨어를 개발해야 하겠지만 그럼에도 불구하고 발견되는 취약점은
[1주차 1차시 03:26] 빠르게 대응하여 제거할 수 있는 체계를 구축을 해서 소프트웨어 보안성을 강화할 수 있다고 설명할 수 있습니다.
[1주차 1차시 03:37] 이제 그럼 본격적으로 현대 애플리케이션들은 어떤 보안 과제를 가지고 있는지를 한번 살펴보도록 하겠습니다.
[1주차 1차시 03:47] 지금 보시는 화면은 라드웨어에서
[1주차 1차시 03:51] 제시한 애플리케이션 보호를 위한 4가지 도전과제 기술 백서에서 설명하고 있는 현대 애플리케이션 보안 과제입니다.
[1주차 1차시 04:01] 현대 애플리케이션 보안 과제를 BOT 관리, API 보안, 서비스 거부, 지속적인 보안으로 분류를 하고 있는데요.
[1주차 1차시 04:12] 하나씩 한번 살펴보도록 하겠습니다. 첫 번째 과제는 BOT 관리입니다.
[1주차 1차시 04:19] 인터넷 트래픽의 52%는 봇에 의한 통신이다 라는 통계가 있는데요. 여기서 봇이 뭘까요?
[1주차 1차시 04:28] 봇은 로봇의 줄임말인데 특정한 작업을 자동으로 수행하는 소프트웨어 프로그램을 말하고 있습니다.
[1주차 1차시 04:37] 트래픽의 52%가 봇에 의해 발생이 되는데 또 그 중에서 절반은 악성 봇에 의한 트래픽이다 라고 설명을 하고 있습니다.
[1주차 1차시 04:48] 거기에 더 문제인 점은 악성봇이 트래픽을 많이 차지하고 있더라도 기업이 악성봇과 정상봇을 잘 구분한다면 또 문제가 크게 안 될 수가 있는데 기업의 79%는 악성봇과 정상봇을 구분하지 못한다고 합니다.
[1주차 1차시 05:08] 정상적인 봇은 말 그대로 정상적인 업무를 수행하는 프로그램이라고 보면 되는데 그러면 악성봇은 뭘까요?
[1주차 1차시 05:16] 악성봇은 네트워크 트래픽을 낭비하게 만들거나 DDoS 공격을 수행하는 쓰레기 트래픽이거나 중요정보 또는 개인정보를 수집하기 위한 트래픽을 발생시키는 봇을 말합니다.
[1주차 1차시 05:32] 그래서 이런 봇에 의한 통신들을 어떻게 기업들이 잘 통제할 수 있을까 하는 것이 첫번째 보안과제라고 설명하고 있습니다.
[1주차 1차시 05:43] 두 번째는 API 보안인데요. 현대 애플리케이션은 IoT, 클라우드, 웹, 모바일 등 다양한 환경에서 동작을 하고 있으며 API라는 것을 통해서 서로의 리소스와 정보를 공유를 하고 있습니다.
[1주차 1차시 05:59] API는 프로그램들끼리 소통할 수 있도록 도와주는 규칙이나 약속인데 API를 호출을 할 때 일반적으로 요청하거나 처리해야 하는 데이터를 첨부를 해서 전송을 하게 됩니다.
[1주차 1차시 06:16] 그래서 이러한 API에서 다양한 취약점들이 발생을 하게 되는데 이 취약점들을 이용을 해서 각종 인젝션, 파라미터 조작
[1주차 1차시 06:26] 공격 사이트로 리디렉트 되는 등의 보안 사고가 빈번하게 발생되고 있어서 이를 막는 것이 두 번째 보안 과제가 되겠습니다.
[1주차 1차시 06:36] 세 번째는 서비스 거부인데요.
[1주차 1차시 06:40] 서비스 거부, 도스 공격은 매우 오래된 공격 방식이지만 여전히 서비스 장애를 일으키게 만드는 효과적인 방식입니다.
[1주차 1차시 06:50] HTTP, HTTPS, 플러드, 소량의 네트워크 트래픽으로도 웹서버의 자원을 점유하여 정상적인 요청을 처리 못하게 하는 슬로우 리스.
[1주차 1차시 07:03] 웹사이트나 서버에 대량의 트래픽을 보내 과부하를 일으키는 공격 방식 등으로 서비스 장애를 일으키게 하고 있습니다.
[1주차 1차시 07:15] 네 번째는 지속적인 보안입니다. DevOps 환경이라는 것은 개발과 운영팀 간의 협업을 강화해서 소프트웨어 개발과 배포 속도를 높이고 안정성과 품질을 향상시키는 것을 목표로 하는 굉장히 좋은
[1주차 1차시 07:34] 환경인데 이 두 가지만 좀 신경을 쓰다 보면 신속한 개발과 롤아웃 방법론은 민첩성을 보장하긴 하지만 보안이 희생되는 경우가 종종 발생하곤 합니다.
[1주차 1차시 07:49] 개발이 완료된 서비스의 취약점을 개선하고 보안을 주입하는 것은 더 어려운 일이기 때문에 개발 환경단에서 보안을 고려를 해서
[1주차 1차시 08:01] 민첩성과 보안의 적절한 트레이드 오프를 결정하는 것이 네 번째 과제라고 볼 수 있겠습니다. 그렇다면
[1주차 1차시 08:09] 이런 애플리케이션 보안 과제를 어떻게 해결할 수 있을까요? 소프트웨어 개발 보안 프로세스, DevSecOps, 보안 내재화, Security by Design, Zero Trust와 같은 소프트웨어 개발 방법론 또는 [불명확: 소프트...]
[1주차 1차시 08:27] 소프트웨어 개발 프로세스들을 활용을 해서 우리는 애플리케이션 보안 과제를 해결할 수 있는데요.
[1주차 1차시 08:35] 그 중 첫 번째로 소프트웨어 개발 보안 프로세스와 DevSecOps에 대해서 먼저 알아보겠습니다. 소프트웨어 개발 보안 프로세스나 DevSecOps는 애플리케이션의 수명 주기에 따른 반복적이고 지속적인 보안 제어를 필수로 하는 보안 활동입니다.
[1주차 1차시 08:57] 소프트웨어
[1주차 1차시 08:58] 개발
[1주차 1차시 08:58] 보안 프로세스는 소프트웨어 개발 과정에서 개발자의 실수, 논리적인 오류 등으로 인해 발생할 수 있는 보안 취약점을 최소화하고 안전한 소프트웨어를 개발하기 위해 소프트웨어 개발 각 단계별로 적절한 보안 활동을 수행하는 프로세스를 정의하고 있습니다.
[1주차 1차시 09:22] 요구사항을 분석하는 단계에서 요구사항 중에 보완요구사항을 식별하게 되는데요. 보완요구사항 식별은 예를 들어서 중요정보를 식별하고 해당 중요정보를 어떻게 처리하는지 법적인 기준을 확인하는 등의 활동을 의미합니다.
[1주차 1차시 09:45] 그 다음 설계 단계에서는 보안 요구사항과 위협에 대한 보안 통제를 고려한 위험을 도출하는 작업을 수행하는데 이러한 활동을 위험 모델링이라는 단어로 설명을 하게 됩니다.
[1주차 1차시 10:01] 개발하고자 하는 시스템이 어떤 사용자가 있고 어떤 데이터를 다루고 있고 또 어떤 데이터의 흐름을 가지고 있는지를 식별을 하게 됩니다.
[1주차 1차시 10:15] 이 흐름에서 어떤 위협들이 발생할 수 있는지를 도출하는 보안 활동이 위험 모델링입니다. 이런 위험 모델링은, 이런 위험 모델링이라는 보안 활동을 통해서 우리는 선제적으로 우리가 개발하는 시스템에 대해서 발생할 수 있는 보안 위협들을 식별을 하고 이것을
[1주차 1차시 10:37] 제거하기 위한 보안 조치를 결정하고 이를 소프트웨어 설계에 반영하여
[1주차 1차시 10:44] 소프트웨어의 안전성을 확보하게 됩니다. 즉, 설계 단계에서는 외부 인터페이스를 식별하고 발생 가능한 보안 위협을 식별해서 그에 대한 보안 통제를 수립하는 단계라고 볼 수 있겠습니다.
[1주차 1차시 11:05] 세 번째 구현 단계에서는 표준 코딩 정의서나 소프트웨어 개발 보안 가이드를 준수를 하여 소프트웨어를 개발하게 됩니다.
[1주차 1차시 11:16] 개발 프로젝트에서는 소프트웨어를 한 명이 개발하는 게 아니고 여러 명이 팀으로 개발을 하게 되는데요. 유지보수를 위해 모든 개발자가 비슷한 방식으로 코딩하자 라고 한 약속이 표준 코딩 정의서입니다.
[1주차 1차시 11:34] 개발자가 일관되고 효율적인 방식으로 코드를 작성할 수 있도록 정해놓은 규칙 스타일을 가이드를 하게 되고
[1주차 1차시 11:43] 예를 들어 자바 프로그램 개발할 때 클래스명은 대문자로 시작을 해야 하고 전역변수도 이름을 대문자로 작성하는 등 대문자로 작성하는 등 그리고 또 인스턴스 변수나 로컬 변수는 소문자로 시작하고 단어 구분은 대문자로 해야 하는 등의 규칙이
[1주차 1차시 12:05] 표준
[1주차 1차시 12:07] 코딩 정의서에서 다루고 있는 내용이 되겠습니다.
[1주차 1차시 12:11] 개발 보안 가이드는 이미 알려진 보안 약점들에 대해서 어떻게 코드를 작성해야 보안 약점이 제거되는지에 대한 내용을 담고 있습니다.
[1주차 1차시 12:25] 구현 단계에서 표준 코딩 정의서나 개발 보안 가이드를 준수를 해서 소프트웨어가 개발되었는지는 소스 코드 보안 약점 진단 도구를 활용해서 점검을 하도록 하고 있습니다.
[1주차 1차시 12:42] 소스코드 보안 약점 진단 도구는 CC 인증이라는 것을 받은 도구를 활용하기도 하고, 오픈소스 진단 도구를 활용하기도 합니다.
[1주차 1차시 12:53] 행정 공공 시스템을 개발하는 경우에, 행안부의 소프트웨어 개발 보안 가이드에서는 소스코드 보안 약점 진단은 반드시 CC 인증을 받은 진단 도구를 사용해야 한다고 정의를 하고 있습니다.
[1주차 1차시 13:07] 소스코드 진단의 경우에는 실행되지 않은 [불명확: 소스코드에] 대해 보안약점 진단
[1주차 1차시 13:15] 진단의 경우에는 실행되지 않은 채로 코드를 분석하기 때문에 정적 분석이라고 부릅니다. 그 다음에 테스트 단계에서는 실행 코드에 대한 보안 취약점을 진단하도록 합니다.
[1주차 1차시 13:31] 테스트 단계에서 프로그램을 실행해서 보안 취약점을 진단하는 방식은 동적 분석이라고 부릅니다. 실행되고 있는 프로그램에 대해서 데이터 입출력을 통해서 진단하는 방식을 사용하기 때문에
[1주차 1차시 13:46] 동적분석이라고 부릅니다. 일반적으로 동적분석은 도구를 사용한 스캐닝을 의미하지만 모의해킹, 모의침투테스트를 통해서 소프트웨어의 보안성을 점검하는 보안활동을 통틀어서 동적분석이라고 부를 수 있습니다.
[1주차 1차시 14:07] [불명확: 이렇게] [불명확: 소프트웨어의]
[1주차 1차시 14:09] 개발의 전 단계에 걸쳐서 각각의 단계에서 적절한 보안 활동을 수행하도록 하는 이러한 개발 방법론을 소프트웨어 개발 방법론을 소프트웨어 개발 보안 프로세스라고 부릅니다.
[1주차 1차시 14:27] 다음은 DevOps 환경의 보안을 고려한 DevOps를 살펴보도록 하겠습니다.
[1주차 1차시 14:35] 전페이지에서 설명했던 소프트웨어 개발 보안 프로세스와 거의 유사한 보안 활동을 수행하는 것을 볼 수 있는데요. 왼쪽에 보이는 타원이
[1주차 1차시 14:46] 개발 프로세스이고 왼쪽이 개발 프로세스,
[1주차 1차시 14:54] 오른쪽 타원이 운영 프로세스입니다.
[1주차 1차시 14:58] 개발 환경에서는 Plan, Create, Verify, Pre-Product 단계로 진행이 되는데요.
[1주차 1차시 15:09] 프리프로덕트 단계로 진행하게 되는데 플랜 단계에서는 프로젝트를 실행하기 위한 인력
[1주차 1차시 15:16] 구성, 보안 활동 범위, 위험 모델링 수립, 교육 등을 통해 프로젝트 수행을 준비를 하게 됩니다. 그 다음 두 번째 크리에이트 단계에서는 실제 설계 산출물을 만들고 코드를 작성하게 되겠죠.
[1주차 1차시 15:32] 이렇게 작성된 코드는 빌드와 테스트 단계를 거치게 될 건데
[1주차 1차시 15:38] Verify 단계에서 여러가지 보안점검을 수행하는 것을 볼 수 있습니다. [불명확: 세] 번째 단계죠.
[1주차 1차시 15:49] 정적분석, SAST, DAST, IST, SCA와 같은 다양한 검증작업을 수행하고 소스코드의 보안약점을 진단하는 정적분석, SAST, 실행되는 프로그램에 대한 취약점을 동적으로 분석하는 DAST.
[1주차 1차시 16:09] 여러 개의 애플리케이션 간 상호 연동시 발생될 수 있는 문제점들을 진단하는 게 IAST 소프트웨어의 구성을 점검하는 SCA와 같은 보안활동이 이 Verify 단계에서 수행이 됩니다.
[1주차 1차시 16:26] 특히 이제 2021년 로그4j 보안 사고 이후에는 오픈소스에 대한 보안 취약점이 아주 민감한 상황으로 대두가 되고 있는데요.
[1주차 1차시 16:35] 소프트웨어의 80% 이상이 오픈소스로 구성이 되어
[1주차 1차시 16:40] 내가 만드는 시스템에 포함되어 있는 오픈소스 중 취약한 버전의 라이브러리나 프레임워크가 포함되어 있는지 점검하는 것이 이 단계의 필수 요소가 되었습니다.
[1주차 1차시 16:55] 검증 단계를 거치고 나면 배포를 위한
[1주차 1차시 16:58] 배포 전 단계 보안 활동이 필요한데 이때는 일반적으로 모의 침투 테스트와 같이 전문가가 실체의 것처럼 시스템의 침투를 테스트해보고 이상이 없는 경우 이제 제품으로 릴리즈를 하게 됩니다.
[1주차 1차시 17:17] 소프트웨어 개발보안 프로세스랑 DevSecOps의 설명을 들어보니 다른 이름 같은 보안 활동임을 이해하셨을까요?
[1주차 1차시 17:27] 두 가지 다 소프트웨어를 개발하는 전 단계에 걸쳐서 적절한 보안 활동을 수행해서 소프트웨어의 보안성을 강화하도록 하는 방법 또는 아키텍처인 것을 확인할 수 있겠습니다.
[1주차 1차시 17:41] 보기 그림은 AWS에서 제시하고
[1주차 1차시 17:45] 있는 DevSecOps 아키텍처 예시인데요. 개발자들은 코드 커밋을
[1주차 1차시 17:53] 통해서 코드를 통합하게 되고
[1주차 1차시 17:59] 코드가 통합되면 코드 빌드 단계로 넘어가게
[1주차 1차시 18:03] 되는데요. 여기서 시크릿
[1주차 1차시 18:07] 스캔, SAST,
[1주차 1차시 18:10] SCA 체크,
[1주차 1차시 18:11] 클라우드 포메이션 스캔과
[1주차 1차시 18:14] 같은 보안 활동이 수행됩니다. 이 시크릿 스캔은 Git 저장소의 소스 코드에
[1주차 1차시 18:22] 중요 정보가 포함되어 있는지를 스캔을 합니다. 그래서 API 키라든지 시크릿 키와 같은 정보가 소스코드에 하드코딩되어 있지는 않은지 이런 것들을 확인을 합니다.
[1주차 1차시 18:36] SAST는 소스코드의 보안약점 점검, SCA 체크는 소프트웨어 구성 점검 등을 수행을 하게 됩니다.
[1주차 1차시 18:46] 클라우드 포메이션 스캔에서는
[1주차 1차시 18:50] AWS에서 프로비저닝을 자동화하는
[1주차 1차시 18:53] 코드인 클라우드 포메이션 코드에 대한 취약점을 점검하게 됩니다. 자동화된 도우를 활용하여 정적 분석들을 수행하는 과정에서 문제점이 발견되는 경우에는 AWS Security Hub
[1주차 1차시 19:09] 서비스를 통해 메시지들을 통합 관리하게 됩니다. 로그는 S3 스토리지에
[1주차 1차시 19:17] 저장이 되고 AWS SNS
[1주차 1차시 19:20] 같은 서비스를 활용하여 경고 메시지를 실시간으로 알림 처리할 수도 있습니다. 코드 빌드 단계에서 정적 분석들을 통과를 하게 되면 DevSecOps
[1주차 1차시 19:36] 프로세스에서는 코드 디플로이 프리 프로덕트 단계로 넘어가게 됩니다. 코드 디플로이 단계에서는 빌드된 서비스를 배포 가능한 상태로 만들고
[1주차 1차시 19:51] 배포 직전인 서비스에 대한 동적 분석 DAST를
[1주차 1차시 19:56] 수행하게 됩니다. 동적 진단을 통해서 서비스가 가질 수 있는 보안 취약점을 찾아내고 수정할 수 있도록 하고 동적 진단까지 끝나게 되면 최종적으로 Code Deploy Product 단계로 넘어가서 제품이 배포가 되게 됩니다.
[1주차 1차시 20:19] 보여지는 화면은 DevSecOps 아키텍처를 실제로 AWS 코드 파이플라인으로 구축해서 실행되는 화면을 캡쳐해 보았는데요.
[1주차 1차시 20:34] 소스코드가 Git에 통합을
[1주차 1차시 20:37] 성공하게 되면 SCA와 SAST
[1주차 1차시 20:44] 분석이 실시가 됩니다.
[1주차 1차시 20:47] 여기서 SCA나 SAST 점검 결과에서 취약점이 발견되면 다음 단계로 넘어가지 않고 정지하게 됩니다.
[1주차 1차시 20:58] 발견된 취약점을 제거하고 점검 재시도를 수행해서 문제점이 발견되지 않으면 다음 단계로 넘어가게 됩니다.
[1주차 1차시 21:11] 소스 코드에 대한 정적 분석이 성공을 해서 통과를 하게 되면
[1주차 1차시 21:19] 스테이징 서버에 배포가 되고 이어서
[1주차 1차시 21:22] DAST 동적 분석이 실시됩니다. Deploy Staging
[1주차 1차시 21:29] Action으로 스테이징 서버로 배포가 성공적으로 수행을
[1주차 1차시 21:35] 하고 나면 실행되는 프로그램에 대해서 DAST
[1주차 1차시 21:43] Analysis가 동적 분석이 실시가 됩니다.
[1주차 1차시 21:48] 동적 분석 결과에서 취약점이 발견되지 않다고 하더라도 자동으로 서비스 배포 단계로 넘어가지는 않습니다.
[1주차 1차시 22:00] 그래서 스테이징 서버에서 동적 분석까지 끝나게 되면 서비스를 배포를 시키기 위해서는 수동으로 승인을
[1주차 1차시 22:11] 반드시 눌러줘야 하고 그렇게 되면 최종적으로 서비스가 운영 환경에
[1주차 1차시 22:18] 프로덕트가
[1주차 1차시 22:19] 디플로이 배포가 되어서 전체 코드 파이플라인이 마무리가 되겠습니다.
[1주차 1차시 22:30] 그 다음에 애플리케이션 보안 과제를 해결하기 위한 두 번째 솔루션으로 보안 내재와
[1주차 1차시 22:37] 시큐리티 바이
[1주차 1차시 22:39] 디자인을 알아보도록 하겠습니다. 이는 안전하게 동작되는 제품을 만들기 위해 제품의 설계 단계에서부터 보안을 고려함으로써
[1주차 1차시 22:51] 알려진 취약점을 조기에 효과적으로 제거하는 개념인데요. 이 두 가지 용어에는 차이가 있습니다.
[1주차 1차시 23:00] 보안 내재화라는 것은 소프트웨어나 시스템 개발 과정에서 보안을 기능처럼 자연스럽게 포함시키는 접근 또는 실천 방법이고 이에 반해서 Security by Design은
[1주차 1차시 23:14] 시스템을 설계할 때부터 보안을 핵심 요소로 고려하는 철학 또는 전략이라고 볼 수가 있습니다. 이 두 개념은 함께 가야지 강력한 보안을 이룰 수가 있고 설계할 때 보안을 고려하는 시큐리티 바이 디자인, 개발 배포 과정에 그걸 실제로 녹여내는 것을 보안 내재화라고
[1주차 1차시 23:37] 정리할 수 있겠습니다.
[1주차 1차시 23:42] 설계 단계에서 보안을 고려하기 위한 보안 활동 중 하나가 위험 모델링, Threat 모델링인데요.
[1주차 1차시 23:51] 위험 모델링 활동은 몇 개의 단계로 구분해서 정의를 할 수가 있는데 첫 번째가 일단 위험 모델링을 수행하기
[1주차 1차시 24:00] 위해 각각의 직무 전문가로 구성된 팀을
[1주차 1차시 24:04] 구성하는 것입니다. 이 때 팀의 리더는 보안 전문가가 하는 것이 가장 효과적입니다.
[1주차 1차시 24:12] 두 번째 단계는 다루어질 위협 환경의 범위를 설정하는데 일반적으로는 데이터 플로우 다이어그램, DFD를 사용합니다.
[1주차 1차시 24:24] DFD는 사용자, 프로세스, 데이터 저장소, 데이터의 흐름을 표시할 수 있는데 이를 통해서 개발하고자 하는 시스템을 파악할 수 있습니다.
[1주차 1차시 24:37] 세 번째 단계에서는 특정 애플리케이션 또는 시스템에 대한 위협을 식별합니다. 예를 들어서 로그인 기능을 구현을 하는데 발생 가능한 위협들을 식별하는 거죠.
[1주차 1차시 24:51] 그래서 누군가 로그인이 성공될 때까지 무작위로 아이디 패스워드를 입력을 하거나
[1주차 1차시 24:57] 훔쳐온 아이디 패스워드를 사용해서 로그인을 시도하는 것과 같은 위협들이 발생할 수가 있는데 이런 가능한 모든 위협을 식별하는 단계가 되겠습니다.
[1주차 1차시 25:08] 네 번째는 세 번째 단계에서 식별한 모든 위협을 위험 수준에 따라서 순위를 정하고 위험도를 계산하는 거죠.
[1주차 1차시 25:19] 위험도 계산을 통해서 가장 위험한 위협들을 식별할 수가 있습니다. 다섯 번째 단계에서는
[1주차 1차시 25:27] 위협들을 어떻게 완화할 건지를 결정하고 위협에 대응 가능한 시스템을 설계를 하게 됩니다. 이 단계에서는 위협을 완화하거나 수영하거나 기능을 제거하거나 위임하거나 같은 조치를 결정할 수 있습니다.
[1주차 1차시 25:45] 위협 모델링 마지막 단계에서는 모든 조사 결과와 조치를 문서화하여 승환구조를 만들 수 있도록 합니다.
[1주차 1차시 25:58] 보시는 그림은 마이크로소프트사의 위험 모델링 도구를 활용한 데이터 플로우 다이어그램 DFD 입니다. MTM 이라고 부르는 도구이고 Azure 환경에서 무상으로 사용 가능합니다.
[1주차 1차시 26:15] 사용자와 프로세스 데이터 흐름 등을 볼 수가 있고 아래쪽에 [불명확: 잘] 안보이네요.
[1주차 1차시 26:26] 데이터 저장소가 있는데
[1주차 1차시 26:28] 이렇게 dfd 를 그려놓고 나면 이제 각각의 프로세스에서 발생할 수 있는 위협을 도출하게 되는데 보통 위협 도출을 stride, stride 각각 약자인 6개를 기준으로 도출합니다.
[1주차 1차시 26:47] s는 spoofing identity [불명확: 신혼] 위조이고 누가 매니저가 아닌데 매니저라고
[1주차 1차시 26:54] 신분을 속일 수 있는 그런 종류의 위협인 거죠. T는 템퍼링으로 중간에 누군가가 데이터를 가로채기를 할 수 있는 그런 종류의 위협입니다.
[1주차 1차시 27:08] R은 repudiation에서 부인이다. 부인인데 해놓고 안했다고 발뺌할 수 있는 그런 위협이죠.
[1주차 1차시 27:18] [불명확: 그리고] I는 Information Disclosure [불명확: 그래서] 정보 유출에 위협이 있는가
[1주차 1차시 27:26] D는 Daniel of Service, 서비스 거부 위협이 발생할 수 있는 부분이 포함되어 있는가? E는 Elevation of Privilege, 권한 상승입니다.
[1주차 1차시 27:38] 일반 사용자인데 슈퍼바이저의 권한을 얻는다든지 시스템에 피해를 입힐 수 있는 위협이 존재하는지를 각 데이터 흐름마다, 사용자마다, 프로세스마다 식별을 하게 됩니다.
[1주차 1차시 27:57] 마지막으로 서비스의 보안 과제를 해결하기 위한 보안모델이 제로트러스트.
[1주차 1차시 28:07] 제로트러스트는 말 그대로 트러스트가 0이다. 아무것도 신뢰하지 않는다. 입니다 베스천 모델과 비교되면서 설명되기도 하는데 베스천은 성벽 요새라는 뜻입니다.
[1주차 1차시 28:22] 그래서 보안에서 [불명확: 외부로부터의]
[1주차 1차시 28:25] 외부로부터 내부의 시스템을 보호하는 보안 아키텍처를 의미하는 게 베스천 모델인데요. 베스천 보안모델은 외부에서 들어오는 위협은 방어가 가능하지만 내부자에 의한 내부에서 발생하는 위협에 대해서는 취약한 모델이에요.
[1주차 1차시 28:47] 그래서 이에 반해서 제로트러스트 보안모델
[1주차 1차시 28:54] 제안이 되었고 내외부로 구분하지 않고 보호해야 하는 리소스를 식별하고 해당 리소스에 대한 최소한의 권한과 세밀한 통제를 지속적으로 수행하는 보안 활동을 통해 해당 리소스를 보호한다는 개념이 제로트러스트가 되겠습니다.
[1주차 1차시 29:15] 절대로 믿지 말고 항상 검증하라가 제로스트 보안 모델의 핵심이라고 할 수 있습니다.
[1주차 1차시 29:25] [불명확: 네,] 제로트러스트 보안모델의 사례를 하나 살펴보겠습니다. 비욘트코프
[1주차 1차시 29:32] 라는 모델은 구글이 만든 제로트러스트 기반의 기업 보안모델로 기존의 경계기반 보안모델, 그러니까 그 앞서 말했던 베스천 보안모델입니다.
[1주차 1차시 29:46] 그래서 그 경계기반 보안모델을 탈피해서 사용자와 기기 중심에 접근 제어를 하는 것이 핵심입니다.
[1주차 1차시 29:53] 기존에는 회사 안에 들어오거나 VPN으로 연결이 되면 그 이후에는 자유롭게 움직일 수 있는 구조였다면 비욘드커프는 회사 안팎을 구분하지 않고 누군지 정확히 확인을 해서 허용된
[1주차 1차시 30:07] 리소스만
[1주차 1차시 30:08] 쓸 수 있게 만드는 구조입니다. 이를 위해서 [불명확: 이제]
[1주차 1차시 30:13] 첫 번째,
[1주차 1차시 30:14] 기기 인증을 위한 데이터베이스, 사용자 인증을
[1주차 1차시 30:20] 위한 데이터베이스를 구축하고 모든 요청은 접근 제어 엔진을
[1주차 1차시 30:27] 통해 통제될 수 있도록 아키텍처링이 되어 있습니다. 비욘드코프의 핵심 요소는 첫 번째, 사용자의 신원이나 역할, 보안 상태 등을 기반으로 접근을 판단하는 사용자 중심 접근 제어.
[1주차 1차시 30:44] 또 사용 중인 디바이스가 기업 정책에 부합하는지를 검사하는 등의 기기 중심 보안 상태 확인, 세 번째 위치, 시간, 기기 상태, 사용자 행동 등 다양한 조건을 고려해서 접근을 허용하거나 차단을 결정하는 컨텍스트 기반 접근 제어, 그리고 네트워크
[1주차 1차시 31:07] 단위가 아닌 서비스 애플리케이션 단위로 접근을 통제하는 리소스 단위 접근 제어가 가능합니다.
[1주차 1차시 31:15] 핵심 요소가 되겠습니다. 그럼
[1주차 1차시 31:19] 이제 다음 주제인 사고 사례를 통한 시큐어 코딩 이해로 넘어가 보도록 하겠습니다.
[1주차 1차시 31:28] 시큐어한 소프트웨어는 설계나 구현 단계에서 발생할 수 있는 실수나 오류를 가지고 있지
[1주차 1차시 31:37] 않은 소프트웨어입니다. 논리적인 오류나
[1주차 1차시 31:41] 개발자의 사소한 실수로 인해 정상적으로 동작되지 않는 기능들을 우리는 버그라고 하기도
[1주차 1차시 31:49] 하고 결점 또는 결함이라고 하기도 합니다. 이렇게 버그나 결점 또는 결함을 가지고 있는 소프트웨어를 사용해서 서비스를 하다보면 해당 버그가 공격자에게 식별되고 공격을 당하게 되면 시스템은
[1주차 1차시 32:06] 중요정보가 유출된다거나 서비스가 중지되는 장애가 발생할 수 있는데요. 시큐한 소프트웨어라고 하면 이런 장애나 문제가 발생하지 않는 소프트웨어, 즉 결함이나 결점, 버그를 가지고 있지 않은 소프트웨어라고 정의할 수 있습니다.
[1주차 1차시 32:30] 본 주제에 맞게 개발자의 사소한 실수로
[1주차 1차시 32:33] 발생된 보안사고 사례를 하나 살펴보겠습니다.
[1주차 1차시 32:37] 블록체인의 스마트 컨트랙트 코드 중 시켜코딩이 적용되지 않아 보안 사고가 발생한 사례입니다. SMT라고 하는 토큰이 1경계 이상이 복사되어 후오비에서 거래가 발생되는 사건이 발생했는데 후오비에서는 이상거래를 포착하고 거래를
[1주차 1차시 32:59] 중지시키기는 했지만 일부 피해가 발생되었던 사고입니다.
[1주차 1차시 33:05] 이더리움 기반의 토큰이 자동적으로 복사되어서 사고가 발생된 건 아니었고요. SMT 스마트 컨트랙트에서 잔고를 체크하는 코드를 잘못 작성함으로써 발생된 사고였다고 판단되었습니다.
[1주차 1차시 33:27] 먼저 정수 오버플로우라는 취약점에 대해서 설명을 하도록 하겠습니다. 오버플로우라는 숫자가 최대치 이상으로 증가하는 것을 말하는데요.
[1주차 1차시 33:38] 보통 4바이트 정수를
[1주차 1차시 33:40] 표현하는 경우
[1주차 1차시 33:41] 첫번째 비트는 [불명확: 사인] 비트입니다. 그래서 0이면 양수, 1이면 음수를 나타내죠. 근데 이 unsigned int의 경우 첫번째 비트는 항상 0이면서 이 값은 변경되지가 않습니다.
[1주차 1차시 33:58] 프로그램에서처럼 첫 그림에서처럼 첫줄의 값은 가장 큰 양수를 표현하고 있습니다.
[1주차 1차시 34:08] 그래서 가장 큰 양수에
[1주차 1차시 34:10] 1을 더하면 어떻게 될까요?
[1주차 1차시 34:12] 1과 2를 더하게 되면 0이고
[1주차 1차시 34:14] 1이 올라가죠.
[1주차 1차시 34:19] 그래서 계속해서 1이 올라가서
[1주차 1차시 34:21] 사인
[1주차 1차시 34:22] 비트까지
[1주차 1차시 34:23] 1이 넘어가게
[1주차 1차시 34:24] 되면 이 unsigned int의 경우는 이 비트값이 0으로 고정되어 있어 오버플로우가 발생해서 연산 결과가 0이 되게 됩니다.
[1주차 1차시 34:38] 네 그럼 이 secure coding이 적용되지 않아서
[1주차 1차시 34:42] 오버플로우 앞서 살펴봤던 정수 오버플로우 취약점이 발생하는 스마트 컨트랙트를 한번 살펴보도록 하겠습니다 화면에 보이는 문제가 되는 함수
[1주차 1차시 34:56] 이름은 transfer proxy 라는 함수인데요 이제 송금자의
[1주차 1차시 35:02] 주소 [불명확: in] from 그리고
[1주차 1차시 35:07] 송금을
[1주차 1차시 35:08] 받는 사용자의 주소 to, 그리고 value라는
[1주차 1차시 35:12] 만큼 송금을 할 거고 또 이때
[1주차 1차시 35:15] fsmt라는 송금 수수료가 발생을 해서 이런 패러미터를 받아가지고 송금을 처리하는 기능을 수행하고 있는 함수입니다.
[1주차 1차시 35:27] 그래서 여기 첫 번째
[1주차 1차시 35:29] 조건문 if문에서 [불명확: balances]
[1주차 1차시 35:32] underbar from 여기에는 from이 송금, 돈을 보내는 사람이라고 했잖아요 돈을 보내는 사람의 잔고에 해당되는 금액이에요 그리고 잔고가 만약에 송금 수수료랑 보내고자 하는 돈이 합보다 만약에 작으면 리버트
[1주차 1차시 35:54] 함수가 실행이 돼서 송금이 일어나지 않고
[1주차 1차시 36:00] 이제 함수가 종료가 되는데 여기서 뭐 어떤 부분에서 오버플로우가 발생했는지 예측이 되시나요?
[1주차 1차시 36:09] 얘네
[1주차 1차시 36:10] 둘을 더하는 과정에서 [불명확: fee] smt 랑 value 두 값이 정수 오버플로우를 일으키면 이 값이 0으로 처리되서 실제로 잔고가 얼마가 있든 무조건 송금이 수행이 되겠죠.
[1주차 1차시 36:31] 그래서 공격자는 입력 값인 value 랑 fsmt 값을 조작을 해서 오버플로우를 발생하도록 해서 값을 0으로 만들고 그런 식으로 공격을 원하는 value만큼이
[1주차 1차시 36:54] 보내지게 만들 수 있게 됐습니다.
[1주차 1차시 36:58] Value라는 변수가 unsigned int 256bit이기 때문에 1경계 이상의 토큰이 있는 것처럼 처리될 수가 있었습니다.
[1주차 1차시 37:09] 왜
[1주차 1차시 37:10] 이 사고를 개발자의 사소한 실수라고 정의를 했냐면 [불명확: 이] 이더리움의 스마트 컨트랙트 개발에 사용된 언어는 Solidity라는 언어인데 Solidity 가이드에서 오버플로우랑 언더플로우
[1주차 1차시 37:31] 처리를 위해서 SafeMath라는
[1주차 1차시 37:34] 라이브러리를 제공해서 사용을 권고하고 있습니다. 개발자는 평상시 자신의 습관에 따라서 오버플로우 발생 가능성을 염두에 두지 않고 4층 연산, 플러스 연산을 그냥 4층 연산으로 처리를 함으로써 사고가 발생되는 원인이 제공이 되었던 것인데요.
[1주차 1차시 37:56] 새로운 언어가 나오고 개발 기간이 짧은 경우에
[1주차 1차시 38:01] 기능 개발을 서두르게 되면 이런 의도치 않은 보안 취약점을 만들 수 있습니다. 이런 취약점이 구현하고 테스트하는 단계에서 걸러내지지 않으면 그대로 보안 사고의 원인이 될 수 있다는 것을 명심해야 할 것입니다.
[1주차 1차시 38:21] 또 개발 보안을 다룰 때 유의 깊게 다루어야 하는 내용이 오픈소스의 취약점 공격인데요.
[1주차 1차시 38:29] 요즘 프로그램 개발할 때 다 오픈소스 기반으로 하잖아요. 그래서 국내외 웹 애플리케이션에서 오픈소스 사용 현황은 시놉시스 OSS RA 2023 보고서에 따르면 상용 소프트웨어의 코드베이스 중 76%는 오픈소스고 그
[1주차 1차시 38:52] 중 48%가 고위험군의 보안 취약점을 포함하고 있다고 합니다.
[1주차 1차시 38:58] 2021년 발생된 로그4J 취약점 공격 이후에도 2년 이상 방치된 오픈소스를 88%의 조직에서 사용 중이라는 기사도 찾아볼 수가 있는데요.
[1주차 1차시 39:13] 로그4J 취약점이라는 것은 2021년 11월 24일 알리바바 클라우드 보안팀에 의해서 처음 발견되었던 로그4J 취약점과 로그4쉘의
[1주차 1차시 39:29] Log4Shell의 경우 Java 기반 로깅 도구인 Apache Log4j 라이브러리 원격 코드 실행 취약점이었는데요.
[1주차 1차시 39:39] Log4j의 로그 메시지 처리 중 이렇게 생긴
[1주차 1차시 39:45] 구문이 Java 데이터베이스의 인터페이스 룩업 기능을 통해 외부 서버로 연결되는 과정에서 악성 Java 클래스가 로드될 수가 있었습니다.
[1주차 1차시 39:57] 공격자가 로그에다가
[1주차 1차시 40:00] 이런 식으로
[1주차 1차시 40:07] 다음과 같은 문자를 삽입을 하면 로그4j가 이를 처리하면서 원격에서 악성 클래스를 다운로드하여 실행하게 되는 공격 기법입니다.
[1주차 1차시 40:18] 이게 HTTP 요청만 가능하면 되고 되기 때문에 공격 난이도가 매우 낮았고 거의 모든 자바 기반의 웹 서비스 자바
[1주차 1차시 40:31] 기반의 앱들이
[1주차 1차시 40:32] 로그4J를 사용하고 있었기 때문에 영향
[1주차 1차시 40:35] 범위가
[1주차 1차시 40:36] 아주 넓었는데 그래서 이렇게까지 떠들썩했던 로그4J 취약점도 2년이 지나서도 여전히 패치되지 않고 있을 정도로 보안 취약점이 아주 심각한 최신의 그런 것들로만 발생하는 것이 아니라
[1주차 1차시 40:58] 개발자의 실수라고 볼 수 있을 정도의 잘 알려진 취약점에 대해서도 여전히 문제가 발생하고 있다는 점입니다.
[1주차 1차시 41:10] 오픈소스 취약점과 맞물려서 설명되는 것이 공급망 해킹입니다. 공급망 해킹은 해커가 직접 목표 시스템을 공격하기는 어려우니까
[1주차 1차시 41:23] 시스템에 소프트웨어나 서비스를 공급하는 외부 파트너를 먼저 해킹을 해서 악성 코드를 정식 업데이트나 배포 경로를 통해 유입시키는 공격입니다.
[1주차 1차시 41:38] 그래서 먼저 그런
[1주차 1차시 41:40] 사례 중에 위즈베라 해킹
[1주차 1차시 41:43] 사고가 있었는데요. 위즈베라는 보안 프로그램 통합 설치 관리 솔루션인 위즈베라 베라포트를 개발한 국내 업체로 해당 솔루션이 해킹되어 공공기관, 은행 등 사용자 PC의 악성 코드가 유포된 사건이 있었습니다.
[1주차 1차시 42:03] 해커가 위즈베라 서버를 침입을 해서 베라포트 정식 설치 파일에 악성 코드를 삽입을 하면
[1주차 1차시 42:14] 공공기관, 금융기관 웹사이트 접속시 베라포트를 통해서 악성 파일이 자동 설치가 되고 사용자의 PC가 원격 제어, 정보 탈취 등의 피해 가능성에 노출된 그런 사건입니다.
[1주차 1차시 42:29] 또 솔라윈즈 보안
[1주차 1차시 42:33] 사고도 공급망 해킹의 대표 사례 중 하나인데요. 미국의 IT 관리 소프트웨어 기업인 솔라윈즈의 제품 업데이트 서버가 해킹이 돼서
[1주차 1차시 42:44] 수많은 정부기관과 글로벌 기업이 정식 업데이트를 통해 악성 코드를 설치당한 사건입니다. 해커가 솔라윈즈의 소프트웨어 빌드 시스템인 오리온에 침투를 하여 정상적인 소프트웨어 업데이트 파일에 악성 코드를 삽입을 합니다.
[1주차 1차시 43:02] 오리온을 사용하는 전세계 18,000여 개 이상의 기관이 정상 업데이트를 통해 악성 코드가 설치가 되었고
[1주차 1차시 43:10] 공격자는 이후 피해 조직의 내부망에 침투하여 정보 탈취, 권한 상승 등 지속적인 공격을 수행한 사고 사례입니다.
[1주차 1차시 43:21] 공격망 공격은 공격자는 한 번의 침투로 수천 개 조직의 확산 가능한 공격을 성공시킬 수 있으므로 공격자 입장에서는 가성비가 아주 좋은 공격 방법이기 때문에 많은 공격자들이 공급망 해킹을 시도하고 있습니다.
[1주차 1차시 43:39] 이런 공급망 해킹에 대응하기 위해서는 여러가지 방법들을 사용할 수 있습니다. 소프트웨어 구성요소 목록화 및 추적을 위해 S범, 소프트웨어 명세서를 활용하거나 빌드 서버, 배포 자동화 과정에 대한 접근 제어 및 무결성 검증을 수행하는 CICD,
[1주차 1차시 44:00] 그리고 모든 배포 파일의 서명, 해시, 검증 프로세스를 구축하고 소프트웨어 공급자에 대한 보안 수준 사전평가 및 계약 조항 강화 등과 같은 방법으로 공급망 잉킹을 대응할 수 있습니다.
[1주차 1차시 44:17] 특히 최근 국내외 S-BOM을 사용한 소프트웨어 보안을 강화하고 있는 추세입니다. [불명확: SBOM은] [불명확: 소프트웨어의]
[1주차 1차시 44:29] [불명확: 자재명세사인데요.] 하나의 소프트웨어 제품이 어떤 오픈소스, 어떤 라이브러리, 어떤 컴포넌트로 구성되어 있는지를 문서화한 목록입니다.
[1주차 1차시 44:41] 그래서 스폰의 활용 목적은 사용 중인 오픈소스의 CV가 있는지 신속하게 파악을 해서 보안 취약점을 대응할 수 있도록 하기 위함인데요.
[1주차 1차시 44:52] 사업적 사용이 제한된 라이센스를 식별하거나 관리할 수 있도록 하고 정부기관 대기업 납품 시 보안 요구사항에 대한 대응이 가능하게도 합니다.
[1주차 1차시 45:06] 제3자 컴포넌트에 의한 위협을 사전에 파악할 수 있게 함으로써 공급망 리스크를 관리할 수 있도록 합니다.
[1주차 1차시 45:14] 이 화면에 보이시는 그림은 소프트웨어 개발 생애 주기 전반에 걸쳐 SBOM 정보가 어떻게 생성되는지 보여주는데요.
[1주차 1차시 45:24] 설계 단계에서는 기술 설계서, 요구사항 명세서, 그리고 아키텍처 설계 문서를 통해 외부 패키지 목록, 사전 정의된 의존성, 라이브러리 사양과 같은 정보를 SBOM에 포함시킬 수 있습니다.
[1주차 1차시 45:41] 개발 단계에서는 Git, Code [불명확: Reparative,]
[1주차 1차시 45:46] 레포지토리 개발단계에서는 [불명확: Git라는] 코드 레포지토리 그리고 빌드 도구 등을 통해 소스코드에서 사용하는 오픈소스 패키지 매니저 의존성 정보를 SBOM에 포함시킬 수 있습니다.
[1주차 1차시 46:02] 그 다음에 테스트 단계에서는 테스트 자동화 도구, 인증서, 인증서 저장소 등을 통해서 사용하는 테스트 툴의 라이브러리, 인증 관련 구성 요소,
[1주차 1차시 46:15] 테스트 스크립트에 포함된 외부 모듈 정보를 포함시킬 수 있고 배포 단계에서는 빌드, 빌드 아티팩트, 배포 이미지, 컨테이너 레지스트리 등을 통해 최종 패키지에 포함된 모든 컴포넌트, 버전, 해시값 등의 메타 데이터를 포함시킬 수가 있습니다.
[1주차 1차시 46:37] 마지막 유지 보수 단계에서는 취약점 스캐닝 결과
[1주차 1차시 46:42] 패치로그, 스폰 버전 관리 시스템을 통해 변경된 컴포넌트, CV 취약점 정보, 업데이트 이력과 같은 정보를 포함시킬 수 있습니다.
[1주차 1차시 46:53] 스폰은 정적 문서가 아니라 지속적으로 지나는 문서이면서 각 단계에서 생산되는 실질적인 데이터를 기반으로 구성되며 자동화 도구를 활용하여 수집을 합니다.
[1주차 1차시 47:10] 스봄은 소프트웨어 내부를 투명하게 공개하고 보안, 라이선스, 품질, 신뢰성 관리에 기반 역할을 하는 핵심 문서가 되겠습니다.
[1주차 1차시 47:22] 그래서 이번 차시의 내용을 요약을 해보면 현대 애플리케이션 보안 과제에서 API 보안과 지속적인 보안에 대해서 학습을 했고
[1주차 1차시 47:36] 현대 애플리케이션 보안 과제를 해결하기 위한 방안으로 소프트웨어 개발 보안, 보안 내제와 제로트러스트 보안 모델을 배웠고 개발자의 사소한 실수로 발생할 수 있는 보안 사고를 예방하기 위해 시켜코딩이 필수 보안 활동임을 알 수 있었습니다.
[1주차 1차시 47:59] 참고 문원이고요.
[1주차 1차시 48:02] 감사합니다.

# [3-TRANSCRIPT] 1주차 2차시 — 보안약점과 시큐어코딩 개요
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure

[1주차 2차시 00:01] 네,
[1주차 2차시 00:04] 1주차 2차시 시작하도록 하겠습니다.
[1주차 2차시 00:09] 이번 차시에서 학습할 내용은 소프트웨어 개발 보안 가이드 그리고
[1주차 2차시 00:15] 클라우드 서비스 보안 인증 가이드 이렇게 두 개의 주제를
[1주차 2차시 00:20] 다루도록 하겠습니다.
[1주차 2차시 00:23] 학습 목표는 다음과 같습니다. 소프트웨어 개발 보안 가이드를 설명하면서
[1주차 2차시 00:29] 설계 단계, 구현 단계 보안 활동에 대해서 알아본 다음에 SaaS 애플리케이션을 대상으로 하는 클라우드 보안 인증 통제 항목의 기술적 보호 조치 등에 대해 설명하는 개발 보안을 알아보도록 하겠습니다.
[1주차 2차시 00:48] 학습 내용이고요.
[1주차 2차시 00:51] 첫 번째 주제에 들어가겠습니다.
[1주차 2차시 00:55] 국내 소프트웨어 개발 보안 적용을 위한 가이드 중 행정안전부에서 배포하고 있는 소프트웨어 개발 보안 가이드를 살펴보겠습니다.
[1주차 2차시 01:08] 행안부의 소프트웨어 개발 보안 가이드는 행정, 공공기관의 정보 시스템, 개발 및 유지 보수 시 각종 사이버 위협으로부터 안전한 소프트웨어를 개발하기 위해 소프트웨어 개발 단계에서부터 소프트웨어 개발 보안을 적용하기 위한 기준으로 제공되고 있습니다.
[1주차 2차시 01:29] 해당 가이드는 행정, 공공기관, 정보 시스템 개발자 및 유지 보수자 담당 공무원들이 소프트웨어를 개발할 때
[1주차 2차시 01:38] 진단원 및 감리원 또는 사업자 자체의 소프트웨어 보안 약점 잔존 여부를 진단할 때 활용하도록 권고를 하고 있습니다.
[1주차 2차시 01:50] 조금 더 자세히 알아보겠습니다. 행안부 소프트웨어 개발 보안 가이드는 행정기관 등이 정보화 사업을 추진할 때 소프트웨어 보안 약점이 없도록 소프트웨어를 개발 또는 변경할 때 활용할 수 있는 지침인데요.
[1주차 2차시 02:09] 이 지침은 법적 구속력은 없지만 기관들이 참고하거나 따르도록 제시한 운영 가이드라인 또는 실행 안내서입니다.
[1주차 2차시 02:19] 고시는 행정안전부 장관이 법령이나 시행령에서 위임받은 사항을 구체적으로 정해 공고하는 공식 규정입니다.
[1주차 2차시 02:33] 2021년 행정안전부 고시가 일부 개정이 되면서 소프트웨어 개발 보안이 공공기관의 경우
[1주차 2차시 02:42] 지켜야 할 의무 사항이 되었습니다. 소프트웨어 개발 보안 가이드 적용 대상은 정보시스템 감리 대상 정보화 사업인데요.
[1주차 2차시 02:53] 일반적으로 감리 대상 사업이라고 하면 기관 유형에 따라서 5억 또는 10억 이상인 사업이 대상이 됩니다.
[1주차 2차시 03:02] 하지만 이 감리 대상이 아닌 정보화 사업도 소프트웨어 개발 보안을 적용하기를 권고는 하고 있습니다.
[1주차 2차시 03:12] 소프트웨어 개발 보안 가이드 적용 범위는 설계 단계 산출물 및 소스 코드 전체인데요. 유지 보수의 경우에는 유지 보수로 인해 변경되는 설계 단계 산출물과 소스 코드 전체가 대상이 되겠습니다.
[1주차 2차시 03:28] 이때 상용 소프트웨어는 진단 대상에서 제외됩니다.
[1주차 2차시 03:36] 소프트웨어 개발 보안 가이드의 필수 진단 항목은 설계 기준 20개 항목,
[1주차 2차시 03:45] 구현단계 보안약점제거기준 49개 항목입니다. 각각의 내용은 뒤에서 조금 더 자세히 설명하도록 하겠습니다.
[1주차 2차시 03:56] 그럼 진단은 어떻게 할까요? 설계산출물은 진단원이 수동으로 산출물에 대해 진단을 수행합니다.
[1주차 2차시 04:06] 소스코드의 경우 방대한 양을 수동으로 진단하지는 않고요.
[1주차 2차시 04:11] 어렵기 때문에 소프트웨어 보안약점 진단 도구를 활용해서 진단하도록 하고 있습니다. 감리법인이 진단 도구를 사용할 경우에는 과학기술정보통신부 장관이 고시한 정보보호시스템평가인증지침에 따라 국가보안기술연구소장이
[1주차 2차시 04:34] 인증한 진단 도구를 사용합니다. 혹시 CC인증이라는 단어 들어보셨을까요?
[1주차 2차시 04:42] CC 인증은 정보보안 제품이 국제적으로 통용되는 보안 기준에 따라 평가받고 신뢰성과 안전성을 인정받는 제도입니다.
[1주차 2차시 04:53] 소프트웨어 보안 약점 진단 도구는 CC 인증 등급 중에서 2등급을 받아야 하고 구조적 테스트 및 설계 검토 수준의 등급을 받은 상용 도구를 주로 사용하게 됩니다.
[1주차 2차시 05:09] 소프트웨어 보안 약점 진단원은 설계 산출물이나 소스코드에서 보안 미적용 소프트웨어 보안 약점이 남아 있는지 진단하여 조치 방안을 수립하고 조치 결과를 확인하는 등의 보안 활동을 수행하는 전문 인력입니다.
[1주차 2차시 05:32] [불명확: 현재는]
[1주차 2차시 05:33] 국내에서 40시간 이상의 진단원 교육과정을 이수한 훈련생을 대상으로 이수시험을 실시하고 이수시험에서 합격하는 인력에 대해서 소프트웨어 약점 진단원 자격이 주어집니다.
[1주차 2차시 05:52] 진단원 교육과정은 6년 이상의 개발 경력 또는 3년 이상의 진단 경력을 가진 전문인력이 교육신청을 할 수 있습니다.
[1주차 2차시 06:06] 별표 3에서 제공하고 있는 소프트웨어 보안 약점 기준 설계 단계 보안 요구 항목입니다.
[1주차 2차시 06:16] 크게 4개의 파트로 분류하고 있는데요. 입력 데이터 검증 및 표현으로
[1주차 2차시 06:24] 분류되는 10개의 설계
[1주차 2차시 06:30] 단계 보안 요구 항목, 그리고 보안 기능으로
[1주차 2차시 06:35] 분류되는 8개의 항목,
[1주차 2차시 06:37] 에러처리로
[1주차 2차시 06:38] 분류되는 1개 항목, 세션통제로
[1주차 2차시 06:42] 분류되는 1개의 보안요구 항목으로 구성이 되어 있습니다. 이러한 설계단계의 보안요구 항목을 다시 정리를 하면 이렇게 8개의
[1주차 2차시 06:58] 항목으로 정리를 할 수 있는데요. 입력값 검증 및 표현의 10개의 보안요구 항목은 외부 입력값에 대한 통제를 강화하기 위해
[1주차 2차시 07:10] 강화하기 위한 보안 설계를 다루고 있으며 입력값 검증이라는 보안 요구 항목으로 함축을 할 수가 있을 겁니다.
[1주차 2차시 07:20] 보안 기능의 8개 항목에
[1주차 2차시 07:24] 대해서는 중요 정보를 식별하고 처리하기 위한
[1주차 2차시 07:31] 중요 정보 처리 그리고 중요 정보의 가장 보편화된 처리 방식인 암호화로
[1주차 2차시 07:48] 분류를 할 수 있습니다. 그리고 무엇보다도 설계 단계에서 중요하게 다뤄야 하는 부분이 인증과
[1주차 2차시 07:56] 인가입니다. 인증 대상 및 방식, 인증 수행 제한, 비밀번호 관리와 중요자원 접근 통제와 같은 설계 단계의 보안 요구 항목은 인증과 인가로 분류를 할 수가 있습니다.
[1주차 2차시 08:13] 시스템 설계 시 핵심적으로 고려해야 할 사항이 에러 처리인데요.
[1주차 2차시 08:19] 오류 메시지를 통해 중요 정보가 유출되지 않도록 안전하게 처리될 수 있도록 해야 합니다.
[1주차 2차시 08:26] 공격자들은 시스템 오류를 통해 시스템 취약점을 식별하는 경우가 많기 때문입니다. 세션 통제도 설계
[1주차 2차시 08:35] 단계에서 중점적으로 고려하는 상황인데요. 로그인에서 로그아웃까지 유지되는 세션을 안전하게 관리하기 위한 다양한 방식들이 설계 단계에서 고려되어야 합니다.
[1주차 2차시 08:50] 행안부의 개발 보안 가이드에는 분류되어 있지 않지만 설계 단계에서 고려하는 핵심 사항 [불명확: 중에] 하나가 바로 로깅인데요.
[1주차 2차시 09:02] 로깅은 보안 사고가 발생했을 때 사고의 피해를 확인하고 수습할 때 반드시 필요한 정보들을 확보하기 위한 활동이기 때문에 로깅이 행안부의 가이드에는 분류되어 있지 않지만 핵심 사항 중에 하나다.
[1주차 2차시 09:20] 보시면 되겠습니다.
[1주차 2차시 09:30] 과기정통부에서도 행안부랑 마찬가지로 2020년에 소프트웨어 산업진흥법을 개정하면서 민간기업이 소프트웨어를 개발할 때 소프트웨어 개발 보안을 적용하도록 권고하고 있습니다.
[1주차 2차시 09:47] 소프트웨어 산업진흥법 제29조에 소프트웨어 개발 보안이라는 항목을 통해 소프트웨어를 개발하거나 변경할 때
[1주차 2차시 09:58] 소프트웨어의 보안 취약점을 최소화하기 위한 [불명확: 1년의] 보안 활동을 수행하도록 명시를 하고 있습니다. 제30조, 제31조를 통해 소프트웨어 안전을 정의하고 있는데요.
[1주차 2차시 10:13] 소프트웨어 안전은 외부로부터 침해 행위가 없는 상태에서
[1주차 2차시 10:18] 소프트웨어의 내부적인 오작동으로 안전기능이 미비하여 발생할 수 있는 사고로부터 사람의 생명이나 신체에 대한 위협에 충분한 대비가 되어 있어야 한다는 규정입니다.
[1주차 2차시 10:32] 자율주행 드론과 같은 기기들에 들어가는 소프트웨어의 안전성을 확보하기 위한 규정이라고 볼 수 있겠습니다.
[1주차 2차시 10:41] 그래서 좀 더 구체적인
[1주차 2차시 10:43] 조문
[1주차 2차시 10:45] 강의 자료에 첨부해놨으니까요. 한번 확인해 보시면 좋겠습니다.
[1주차 2차시 10:52] 다음으로 이제 두 번째 주제인 클라우드 서비스 SaaS 보안 인증 가이드에 대해서 설명하도록 하겠습니다.
[1주차 2차시 11:04] SaaS 표준 등급 클라우드 보안 인증은 중요 데이터를 처리하는 서비스를 대상으로 하면서
[1주차 2차시 11:15] 13개 분야에서 총 79개의 통제 항목을 준수해야 하는데요. 이 인증기준은 클라우드 서비스의 보안성과 신뢰성을 확보하기 위한 관리적 기술적 보호 조치를 포함합니다.
[1주차 2차시 11:30] 특히 소프트웨어 보안과 관련된 통제 항목은 다음과 같습니다. 첫 번째, 정보보호 정책 수립 및 운영.
[1주차 2차시 11:40] 조직의 정보보호를 위한 정책을 수립하고 지속적으로 운영해야 합니다.
[1주차 2차시 11:46] 두번째, 서비스 연속성 관리, 서비스의 가용성을 유지하기 위해 장애 대응 및 복구 계획을 마련해야 합니다.
[1주차 2차시 11:56] 세번째, 접근 제어, 시스템 및 데이터에 대한 접근 권한을 적절하게 관리하고 통제해야 합니다. 네번째, 암호화 적용, 중요 데이터의 저장 및 전송 시 암호화를 통해 기밀성을 보호해야 합니다.
[1주차 2차시 12:15] 다섯 번째 시스템 개발 및 운영 보안, 안전한 소프트웨어 개발 생명 주기를 적용하고 개발 단계에서부터 보안을 고려해야 한다는 내용이 담겨 있고 여섯 번째 취약점 관리 부분에서는 잠시만요.
[1주차 2차시 12:37] 여섯 번째 취약점 관리에서는 정기적인 보안 취약점 점검 및 패치를 통해 시스템의 보안 상태를 유지해야 합니다.
[1주차 2차시 12:50] 이러한 통제 항목들은 클라우드
[1주차 2차시 12:53] 서비스 제공자가 소프트웨어 개발 및 운영 과정에서 보안
[1주차 2차시 12:57] 요구 사항을 충족하도록 설계되어 있습니다. 이를 통해 공공기관 및 민간 기업이 안전하게 클라우드 서비스를 도입하고 활용할 수 있도록 지원을 하는 그런 보안 인증이라고 생각하시면 되겠습니다.
[1주차 2차시 13:14] 이 SaaS 표준 등급의 클라우드 보안 인증 통제 항목의 13번째 항목이
[1주차 2차시 13:20] 시스템 개발 및 도입 보안인데요. 이 항목에 보면 시스템 분석 및 설계,
[1주차 2차시 13:30] 구현 및 시험,
[1주차 2차시 13:32] 그리고 외주 개발 보안 등으로 분류된 총 10개, 5개,
[1주차 2차시 13:38] 4개, 1개 해서 이렇게 10개의 통제 항목을 정의를 하고 있습니다.
[1주차 2차시 13:46] [불명확: 그래서] 이 SaaS Cloud 보안 인증의 13번 [불명확: 짝목인] 시스템 개발 및 도입
[1주차 2차시 13:52] 보안의 세부 통제 항목에 대해서 살펴보도록 하겠습니다. 첫 번째 통제 항목은 시스템 분석 및
[1주차 2차시 14:04] 설계인데요. 그 중에서 신규 시스템 개발 및 기존 시스템 변경 시 보안 요구사항을 명확히 정의하고 이를 적용해야 한다고 규정을 하고 있습니다.
[1주차 2차시 14:26] 그리고 이제
[1주차 2차시 14:27] 인증 및
[1주차 2차시 14:29] 암호화 기능 통제 항목에서는 중요정보의 입출력 및 송수신과정에서 무결성, 기밀성이 요구될 경우 법적 요구사항을 고려해야 한다.
[1주차 2차시 14:41] 세부통제항목을 설명하고 있습니다.
[1주차 2차시 14:45] 이외에도 사용자의 인증, 권한 변경, 중요정보 이용 및 유출 등에 대해 [불명확: 감사 증적을] 확보할 수 있도록 해야 하며,
[1주차 2차시 14:58] 시스템 설계 시 업무의 목적 및 중요도에 따라 접근 권한을 부여할 수 있도록 해야 합니다. 로그 기록의 정확성을 보장하고 법적인 자료로서 효력을 가질 수 있도록 시스템 시각을 공식 표준 시각으로 동기해야 하는 부분도 있고 기술적 보호 조치의 내용을 살펴보면
[1주차 2차시 15:21] 앞에서
[1주차 2차시 15:23] 설계한 소프트웨어 개발 보안 가이드의 설계 시 보안 요구 항목과 유사하게 정의되어 있다는 것을 알 수가 있습니다.
[1주차 2차시 15:34] 두 번째 통제 항목 보면 구현 및
[1주차 2차시 15:38] 시험, 여기 네 가지 항목이 있는데 안전한 코딩 방법에 따라 서비스를 구현하고 분석 설계 과정에서 도출한 보안 요구 사항이 시스템에 적용되었는지 확인하기 위한 시험을 수행하도록 하고 있습니다.
[1주차 2차시 15:58] 개발과 운영 환경을 분리해서
[1주차 2차시 16:06] 비인가 접근 변경의 위험을 감소시키도록 하고 있고 시험 테스트 과정에서 운영 데이터 유출을 예방하기 위해 테스트 데이터를 생성, 이용, 관리 파기 등 기술적 보호 조치에 관한 절차를 수립하고
[1주차 2차시 16:29] 이행하도록 하고 있습니다.
[1주차 2차시 16:33] 마지막으로 소스
[1주차 2차시 16:35] 프로그램 보안, 여기서는 소스 코드에 대해 변경 관리를 수행하고 인가된 사용자만이 소스 코드에 접근할 수 있도록 통제 절차를 수립하고 [불명확: 이해해야] 한다고 나와 있습니다.
[1주차 2차시 16:51] 세 번째, 제 화면에서는 잘렸는데
[1주차 2차시 16:57] 나눠드린 자료에는 제대로 되어 있을 거예요.
[1주차 2차시 17:08] 말로만 설명하고 하도록 하겠습니다. 세 번째 통제 항목은 외주 개발 보안인데요.
[1주차 2차시 17:20] 시스템 개발을 외주 위탁하는 경우 분석, 설계 단계에서 구현 및 이관까지 준수해야 할 보안 요구사항을 계약서에 명시하고 이행 여부를 관리 감독을 해야 합니다.
[1주차 2차시 17:34] 우리가 개발한 소프트웨어를 공공기관에
[1주차 2차시 17:38] SaaS 형태의 클라우드 서비스를 제공하기 위해서는 반드시 살펴본 클라우드 서비스 보안 인증을 받아야 하는데요.
[1주차 2차시 17:48] 이러한 보안 인증을 받기 위해서 소프트웨어를 설계하고 구현하는 단계에서부터 소프트웨어 개발 보안이 적용돼야 하며 적용 여부는 구체적으로 살펴본 이런 통제
[1주차 2차시 18:05] 항목 그리고 세부 통제 항목을 통해서
[1주차 2차시 18:11] 점검되도록 제도화가 되어 있습니다.
[1주차 2차시 18:18] 이번 차시 배운 내용에 대해서 요약을 해보면 소프트웨어 개발 보안을 위한 국내 기준으로 활용되는 소프트웨어 개발 보안 가이드에서 설명하고 있는 20개의
[1주차 2차시 18:34] 보안 요구사항, 49개의
[1주차 2차시 18:37] 보안 약점 제거 기준이 뭔지
[1주차 2차시 18:42] 나름 간단하면서도 어떤 부분들은 자세하게 살펴봤고요. 두 번째로 SaaS 애플리케이션을 대상으로 실시되는 클라우드 보안 인증 통제 항목의 기술적 보호 조치 등에서 설명하는 시스템 개발 및 도입 보안의 점검 항목을 배워봤습니다.
[1주차 2차시 19:05] 참고 문헌은 다음과 같고요. 이번 차시 수업 여기까지 하도록 하겠습니다.
[1주차 2차시 19:11] 감사합니다.

# [3-TRANSCRIPT] 1주차 3차시 — 보안약점과 시큐어코딩 개요
키워드: 보안약점/Weakness/CWE/취약점/Vulnerability · SQL Injection/SQL 인젝션/SQL 삽입/에스큐엘 인젝션/에스큐엘/SQLi/CWE-89 · Command Injection/커맨드 인젝션/명령어 삽입/명령 삽입/OS Command/CWE-78 · CSP/Content Security Policy/콘텐츠 보안 정책/컨텐츠 시큐리티 폴리시 · 화이트리스트/Whitelist/최소 허용/허용 목록 · Authentication/인증/로그인 · Authorization/인가/권한/RBAC/ABAC/PBAC/최소 권한 · Session/세션/JSESSIONID/세션 쿠키/쿠키/HttpOnly/Secure · Token/토큰/Bearer/베어러 · Filter/필터/Interceptor/인터셉터/Servlet/DispatcherServlet · SSR/CSR/Server-Side Rendering/Client-Side Rendering/서버 사이드 렌더링/클라이언트 사이드 렌더링 · 코드 리뷰/Code Review/SAST/DAST/정적 분석/동적 분석/SonarQube/Fortify

[1주차 3차시 00:01] 네, 1주차 마지막 3차시 강의 시작하도록 하겠습니다.
[1주차 3차시 00:10] 이번에 학습할 내용은 소프트웨어 개발 보안 국외의 기준입니다. 총 4가지 주제로 나눠서 강의를 하도록 하겠습니다.
[1주차 3차시 00:24] 학습 목표는 다음과 같습니다. 우선 국외 소프트웨어 개발 보안 기준을 알아보고
[1주차 3차시 00:32] OWASP TOP10과 CVE, CWE의 용도에 대해 알아보면서 각각을 어떻게 개발 단계에 적용할 수 있는지 알아보도록 하겠습니다.
[1주차 3차시 00:46] 이에 따른 학습 내용은 국외 개발 보안 현황, OWASP TOP10, CVE, CWE TOP25입니다.
[1주차 3차시 00:58] 그럼 국외 개발 보안 현황부터 한번 알아보도록 하겠습니다.
[1주차 3차시 01:07] 국외 개발 보안 현황을 연대별로 한번 살펴보면 그 역사가 오래되었음을 알 수가 있습니다. 2000년도 로스 앤더슨의 시큐리티 엔지니어링은 보안 설계의 기본 원칙과 다양한 시스템에서 보안을 구현하는 방법을 다룬 보안 엔지니어링의 고전적인 참고서인데요.
[1주차 3차시 01:30] 이 책은 암호학, 네트워크 보안, 운영체제 보안, 이런 것뿐만 아니라 경제학, 심리학, 사회공학적 공격 등 보안의 다각적인 측면을 탐구하는 특징을 가지고 있습니다.
[1주차 3차시 01:45] 2002년에는 FISMA, 즉 미연방정보보안관리법이 의회를 통과했는데요. 이 법률은 미국 연방정부의 정보시스템과 데이터를 보호하기 위한 법률로
[1주차 3차시 01:58] 안전한 소프트웨어 개발, 소프트웨어 보안 결함 제거, 소프트웨어 공급망 보안과 S-BOM과 같은 내용들을 담고 있습니다.
[1주차 3차시 02:09] 2014년에 개정되어 FISMA 2014로 불리며 업데이트 되었습니다. 해당 법률에서 정의하고 있는 안전한 소프트웨어 개발에서는 소프트웨어 개발 생명주기의 전반에서 보안 검토를 수행하고 보안 요구사항을 설계 단계에서 정의하도록 하고 있으며
[1주차 3차시 02:28] 코드 분석과 동적 및 정적 보안 테스트 적용을 정의하고 있습니다. NIST의 SP는 미국 국립표준기술연구소에서 발행한 정보시스템 보안 통제 가이드라인들입니다.
[1주차 3차시 02:45] 미국 연방기관이랑 민간에서도 광범위하게 사용되고 있고 정보보호 프레임워크 중 가장 대표적인 문서라고 보시면 되겠습니다.
[1주차 3차시 02:58] 2013년에 NIST SSDLC [불명확: SP80]-64는 보안이 통합된 시스템 개발 생명주기에 대한 가이드라인인데요.
[1주차 3차시 03:11] 시스템이나 애플리케이션을 개발할 때 처음부터 보안을 고려하라는 취지로 만들어졌습니다. 2006년 OWASP 클라스프는 보안을 고려한 소프트웨어 개발 보안 프로세스를 만들기 위한 프레임워크로
[1주차 3차시 03:28] 특히 기본 개발 프로세스에 쉽게 통과될 수 있도록 고안되었습니다. 2016년에 발표한 NIST [불명확: SP80]-160은 보안이 잘 설계된 시스템을 만드는 방법에 초점을 둔 문서입니다.
[1주차 3차시 03:46] 즉, 보안이 내재된 시스템 아키텍처 설계를 강조하고 있습니다. 오랜 시간 동안 지속적으로 소프트웨어 개발 보안을 위한 방법론,
[1주차 3차시 03:58] 프로세스, 프레임워크 등이 제한되고 개선되어 오면서 소프트웨어 개발 보안의 체계를 만들어 오고 있는 것을 볼 수 있습니다.
[1주차 3차시 04:10] 미국에서는 니스트로 불리는 국립표준기술연구소에서 안전한 소프트웨어 개발 프레임워크 SSDF를 문서를 통해 제시를 하고 있습니다.
[1주차 3차시 04:26] 이 프레임워크는 소프트웨어 개발 생명주기의 전반에 걸친
[1주차 3차시 04:31] 보안 관행을 통합하기 위한 지침을 제공하고 있으며 주요 내용은 다음과 같습니다. 소프트웨어 개발 보안에 대한 정의를 소프트웨어 개발 초기 단계에서 보안 요구사항을 명확히 정의하여 보안을 설계에 반영하는 활동으로 정의를 하고 있습니다.
[1주차 3차시 04:52] 다음은 소프트웨어 개발 보안을 적용하기 위해서 위험을 식별하고 관리하도록 하고 있습니다.
[1주차 3차시 05:05] 빌드 시스템을 포함한 개별 환경의 보안 위험을 식별하고 적절한 보안 통제를 구현하도록 하고 있습니다. 또한 코드의 무결성을 확보하기 위해 자동화된 진단 [불명확: 노고를] 도입하여 정적 및 동적 분석을 수행하고 사용되는 라이브러리나 패키지 등의 구성 요소에 알려진
[1주차 3차시 05:28] 취약점이 없는지를 검사합니다.
[1주차 3차시 05:38] 그렇다면 국외 개발 보안 현황에서 유럽은 어떤지 한번 살펴볼까요?
[1주차 3차시 05:43] 유럽연합의 사이버보안법제도 중 핵심 법령인 NIS2는 지침은 유럽 전역에 걸쳐 공통되고 높은 수준의 사이버보안 체계를 확립하며, 중요 인프라와 민간기업에 대한 보안 의무를 강화하고 있습니다.
[1주차 3차시 06:04] NIS2에서 요구하는 소프트웨어 개발보안 관련 활동들을 요약해보면,
[1주차 3차시 06:10] 조직은 정기적인 위험분석을 수행하고 이를 기반으로 정보시스템 보안정책을 수립하도록 하고
[1주차 3차시 06:18] 있습니다.
[1주차 3차시 06:20] 사이버사고 발생시 신속하게 대응하고 비즈니스 연속성을 유지하기 위하여 위기관리계획을 마련하도록 하고 있고요.
[1주차 3차시 06:38] 공급업체 및 서비스 제공자와의 관계에서 보안요구사항을 명확히 하고
[1주차 3차시 06:44] 관리하는 공급망 보안 강화 대책을 마련하도록 하여 시스템 개발 및 유지 보수 과정에서 보안을 고려하고 취약점을 관리하도록 하고 있습니다.
[1주차 3차시 06:57] 소프트웨어 개발 생명주기 전반에 걸쳐 보안 관행을 통합하고 취약점 처리 및 공개 절차를 수립하는 것을 포함합니다.
[1주차 3차시 07:08] 이를 통해 개발 단계에서부터 보안을 고려하여 안전한 소프트웨어를 구축하고 잠재적인 보안 위협을 사전에 방지할 수 있습니다.
[1주차 3차시 07:19] 또한 NIS2 지침은 조직의 규모와 관계없이 필수 및 중요 서비스 제공자를 대상으로 하며 소프트웨어 개발 기업도 이에 해당될 수 있습니다.
[1주차 3차시 07:32] 따라서 해당 지침의 요구사항을 준수하기 위해서는 보안 코딩 표준의 수립, 정기적인 보안 검토, 취약점 관리 체계 구축 등 포괄적인 보안 관리 체계를 도입해야 합니다.
[1주차 3차시 07:48] NIS2 지침의 시행으로 인해
[1주차 3차시 07:51] 소프트웨어 개발 보안에 대한 요구사항이 강화되었고 조직이 사이버 보안 위험을 효과적으로 관리하고 안전한 소프트웨어를 제공하기 위한 필수적인 조치로 간주됩니다.
[1주차 3차시 08:08] OWASP TOP10에 대해 알아보도록 하겠습니다.
[1주차 3차시 08:13] 앞에서 미국과 유럽의 소프트웨어 개발 보안 적용에 관련된 지침들을 알아보았는데요.
[1주차 3차시 08:21] 많은 기업들이 웹을 기반으로 애플리케이션을 활용한 서비스를 제공하고 있는데 OWASP는 웹 애플리케이션의 보안 강화를 목적으로 가장 치명적인 보안 취약점 10가지를 정리를 해서 OWASP TOP10이라는
[1주차 3차시 08:44] 문서를 주기적으로 발표를 하고 있습니다. 해당 문서는 웹 애플리케이션 보안 필수지침으로 개발자, 보안 전문가 및 조직이
[1주차 3차시 08:54] 보안 취약점을 사전에 방지할 수 있도록 도와줍니다. 이를 바탕으로 코드 보안성 강화, 시스템 구성 보안 점검, 최신 보안 업데이트 유지 등을 통해 완전한 웹 애플리케이션을 구축하는 것이 중요합니다.
[1주차 3차시 09:14] 최근에 발표된 OWASP TOP10의 3가지 버전, 2013년, 2017년, 21년 버전을 비교해 보도록 하겠습니다.
[1주차 3차시 09:24] 2017년 TOP10하고 비교를 해서 2021년 TOP10의 내용에서 눈여겨볼 내용은 인시큐어 디자인이 네 번째 보안 이슈로 선정된 것입니다.
[1주차 3차시 09:38] 보안을 고려하지 않은 설계로 인해 발생된 보안 사고가 많았다고 볼 수 있습니다. 그리고 새롭게 추가된 서버사이드 요청 위조도
[1주차 3차시 09:51] API 간의 호출이 많아지면서 열 번째 보안 이슈로 선정이 되었습니다.
[1주차 3차시 09:58] 2017년에 안전하지 않은 역직렬화 보안 이슈을
[1주차 3차시 10:11] 다른 보안 이슈들과 통합을 하여 소프트웨어와 데이터 무결성 실패로 리스트를 작성하고
[1주차 3차시 10:19] 있습니다.
[1주차 3차시 10:24] [불명확: 이렇게요.]
[1주차 3차시 10:25] 나머지는 2017년에 선정되었던 10개 보안 이슈에 순위가 바뀌거나 통합되어 리스트가 작성되어 있는 것을 볼 수 있습니다.
[1주차 3차시 10:36] 2021년 OWASP TOP10의 각각의 항목을 좀 더 자세히 살펴보도록 하겠습니다.
[1주차 3차시 10:45] 첫 번째 이슈는 이 취약한 접근 통제입니다.
[1주차 3차시 10:49] 인증과 [불명확: 인간은] 좀 다른 개념인데요. 일반적으로 인증을 통해 사용자를 식별을 하고 이렇게 식별된 정보를 활용하여 인가 정책을 수립을 하게 되는데요.
[1주차 3차시 11:03] 인증된 사용자에 대해 모든 리소스에 대해 허용함으로
[1주차 3차시 11:08] 인증된 사용자에 대해 모든 리소스에 접근하도록 허용함으로써 다른 계정의 데이터를 조회하거나 더 많은 권한을 가져야 하는 관리자 기능을 수행한다거나 하는 보안 사고를 일으킬 수 있습니다.
[1주차 3차시 11:24] 인증된 사용자라도 접근이 제한된 데이터나 기능에 접근할 수 있는 취약점을 취약한 접근 통제로 분류를 하고 있습니다.
[1주차 3차시 11:34] 취약한 접근 통제와 같은 보안 사고를 예방하려면
[1주차 3차시 11:38] 모든 요청에 대한 접근 권한을 확인하는 절차를 만듭니다. 이때는 최소 권한의 원칙을 적용해야 합니다.
[1주차 3차시 11:48] 그리고 가장 일반적인 접근 통제 정책 중에 하나가 역할 기반 접근 제어입니다. 관리자, 일반 사용자 등과 같이 역할을 정의하고 각각의 역할에 따라 접근 권한을 할당하여 통제하는 방식입니다.
[1주차 3차시 12:06] 두 번째는
[1주차 3차시 12:07] 암호화 실패, Cryptographic Failure [불명확: 쓰임인데요.]
[1주차 3차시 12:12] 중요 데이터가 제대로 보호되지 않아 기밀 정보가 유출되는 취약점입니다. 예를 들어 주민등록번호와 같은 민감정보를 평문으로 저장하거나 전송하는 경우입니다.
[1주차 3차시 12:26] 암호화 실패 보안사고를 예방하려면 먼저 암호화에서 처리해야 하는 중요정보를 먼저 식별해야 할텐데요.
[1주차 3차시 12:35] 이렇게 식별된 중요 정보를 전송하는 경우 TLS 기반의 HTTPS 프로토콜을 사용해서 데이터를 암호화해서 전송하도록 시스템을 구축해야 합니다.
[1주차 3차시 12:47] 예를 들어 주민등록번호, 여권번호와 같은 개인정보를 데이터베이스에 저장하는 경우 안전한 AES나 RSA와 같은 알고리즘을 사용해서 데이터를 [불명확: 안복화하면서] 사용을 반드시 해야겠습니다.
[1주차 3차시 13:05] 이 중요 정보 중 [불명확: 복화를] 하지 않아도 되는 패스워드 같은 정보는 단방향 해시 알고리즘을 사용해서 저장을 합니다.
[1주차 3차시 13:14] 특히 패스워드가 짧은 입력인 경우를 받아서 해시를 처리해야 되는 경우에는
[1주차 3차시 13:26] 보안을 강화하기 위해서 긴 솔트라는 그런 기법이 있거든요. 그런 걸 사용을 해서 무작위 대입 공격을 방어할 수 있도록 해야 합니다.
[1주차 3차시 13:38] 세 번째는 인젝션 공격인데요. 공격자가 악성 데이터 또는 코드를 삽입해서 데이터베이스나 원하는 기능을 조작하거나 시스템을 장악하는 그런 취약점입니다.
[1주차 3차시 13:56] SQL 쿼리문에 악성 코드를 삽입해서 쿼리를 조작하는 SQL 인젝션, [불명확: 그리고] 명령어를 삽입해서 공격자가 의도하는 명령이 실행되도록 하는 커맨드 인젝션, 스크립트를 삽입해서 사용자의 브라우저에 공격자가 의도하는 동작이 수행되도록 하는 [불명확: 크로스드] 사이트
[1주차 3차시 14:18] 스크립트 등을 통합을 해서 인젝션이라고 분류를 하고 있습니다.
[1주차 3차시 14:23] 이러한 인젝션 공격을 예방하기 위해서는 사용자의 입력값을 검증하고 악의적인 값들을 철저히 필터링을 해서 공격이 차단될 수 있도록 해야 합니다.
[1주차 3차시 14:37] 그때 필터링을 수행할 때는 값을 차단해서 원천적으로 시스템에 들어오지 못하게 하거나 안전한 값으로 치환해서 사용하게 하는 등의 처리를 할 수 있습니다.
[1주차 3차시 14:49] 이때 필터링 정책은 반드시 시스템에서 안전하게 처리 가능한 값만 걸러서 사용을 하고 나머지 입력은 모두 차단하도록 하는 화이트리스트 정책을 적용하는 것이 바람직하다고 권고되고 있습니다.
[1주차 3차시 15:06] 네 번째는 보안 설계 미흡인데요. 보안 요소를 고려하지 않는 시스템 설계로 인해 발생되는 어떤 점.
[1주차 3차시 15:19] 취약점들을 분류를 하였습니다. 예를 들어서 관리자 페이지가 있는데 URL을 직접 입력해서 인증 절차 없이 해당 페이지에 접근이 가능한 것이 보안 설계 미흡에 해당되는 경우입니다.
[1주차 3차시 15:34] 그래서 이러한 보안 설계상의 미흡 취약점을 방지하기 위해서 설계 단계의 위험 모델링을 수행을 해서
[1주차 3차시 15:42] 발생 가능한 위협을 미리서부터 식별을 하고 이에 대응하기 위한 시스템 구조를 설계하도록 해야 합니다. 보안 설계를 코드에 반영을 하고 주기적으로 소스 코드 보안 약점 진단, 동적 진단 등을 통해 시스템의 보안성을 확보할 수 있도록 노력해야 하겠습니다.
[1주차 3차시 16:05] 다섯 번째는 보안 설정 오류인데요. 소프트웨어를 설치하는 경우에 기본적으로 설정되는 값들이 있습니다.
[1주차 3차시 16:13] 이런 설정된 기본값들이 보안 사고의 원인이 되기도 하고 디버깅 모드로 동작되는 소프트웨어로 인해 보안 취약점이 유출되기도 하는데요.
[1주차 3차시 16:26] 이런 보안 사고를 예방하기 위해서는 불필요한 기능이나 서비스는 비활성화를 해야 하며 이미 알려진 취약점들을 예방하기 위해서는 보안 패치나 업데이트를 주기적으로 적용할 수 있도록 해야 합니다.
[1주차 3차시 16:40] 특히 환경설정 파일과 같은 시스템에 중요한 영향을 미칠 수 있는 파일들은 철저한 접근통제 정책이 적용돼야 합니다.
[1주차 3차시 16:53] 다음은 취약하고 오래된 구성요소인데요. 오래된 라이브러리, 프레임워크, 플러그인을 사용하는 경우 쉽게 공격에 노출될 수 있습니다.
[1주차 3차시 17:05] 특히 많은 기업들이 오픈소스 소프트웨어를 많이 사용하고 있는데
[1주차 3차시 17:11] 이때 오픈소스 취약점을 이용한 공격이 점점 더 들어가는 추세입니다. 패치가 되지 않은 오픈소스 소프트웨어의 사용은 공격자에게는 너무나 쉬운 먹잇감이 될 수가 있는데요.
[1주차 3차시 17:26] 취약하고 오래된 구성요소 취약점을 예방하기 위해서 최신 버전의 라이브러리 프레임워크가 유지될 수 있도록 주기적으로 패치를 수행해야 합니다.
[1주차 3차시 17:37] 또한 사용 중인 오픈소스 및 서드파티 모듈의 보안 이슈가
[1주차 3차시 17:41] 관리될 수 있도록 당연히 해야겠죠. 그래서 최근에는 그런 것들은 스봄 소프트웨어 명세서를 작성을 해서 이런 보안 이슈들을 해결할 수 있도록 노력을 하고 있습니다.
[1주차 3차시 17:56] 다음은 인증 및 세션 관리 취약점입니다. 보안 강도가 약한 비밀번호나 세션 하이제킹 등의 문제로 인증이 우회되거나 접근이 통제되지 않는
[1주차 3차시 18:10] 보안 사고들이 발생을 하고 있는데요. 예를 들어 무작위 비밀번호 대입 공격으로 인증이 뚫린다거나 세션 인가 정책에 사용되고 있는 제이슨 웹 토큰이 유출된다거나 하는 유출이 빈번하게 발생하고 있습니다.
[1주차 3차시 18:28] 그래서 이러한 보안 사고를 예방하기 위해 멀티 팩터 인증, 다중 요소 인증을 적용하기를 권고를 하고 있고요.
[1주차 3차시 18:38] 이미 많은 기업들이 휴대폰 기기와 아이디, 패스워드 입력과 같이 두 가지 종류의 정보를 사용해서 인증을 수행하도록 설계를 하고 있습니다.
[1주차 3차시 18:49] 또 안전한 세션 관리를 위해서 토큰 유효기간을 두 개의 레이어로 관리하는 방법 등이 있고 실제 사용되는 액세스 토큰과 세션 토큰을 안전하게 관리하는 리프레쉬 토큰으로 이중 관리하여 토큰이 유출되었을 때도 대응할 수 있도록 하고 있습니다.
[1주차 3차시 19:08] 또한 사용자들에게 강력한 비밀번호를 설정할 수 있도록 시스템에서 정책을 수립하고 구현함으로써 비밀번호를 안전하게 관리할 수 있도록 합니다.
[1주차 3차시 19:24] 다음은 소프트웨어 및 데이터 무결성 실패인데요. 무결성을 검증하지 않은 코드 및 데이터로 인해 악성 코드가 실행될 가능성이 있는 취약점입니다.
[1주차 3차시 19:41] 예를 들어서 서명이 없는 업데이트 파일로 시스템을 업데이트를 한다거나 외부에서 수신된 객체에 대해 검증 작업 없이 역직렬화를 수행한다거나 신뢰할 수 없는 CICD 파이프라인 상의 코드, 실행
[1주차 3차시 20:05] 파일을 검증 없이 사용한다거나 하는 취약점들이 되겠습니다. 이 문제를 예방하기 위해서 코드에 대해서는 코드 서명을 항상 첨부를 하고
[1주차 3차시 20:16] 사용 전에 무결성을 검증하는 프로세스를 만들어야 합니다. CICD 파이프라인에 대한 보안 강화를 위해서는 개발에서 빌드하는 단계에서 코드 검토, 취약점 스캔, 권한 관리와 같은 보안 활동을 자동화 도구를 활용해서 수행을 하고 빌드에서 배포하는 단계에서는
[1주차 3차시 20:39] 아티팩트 무결성 검증, 자동화된 동적 보안 테스트를 수행을 할 수가 있습니다.
[1주차 3차시 20:47] 아홉 번째는 보안 로깅 및 모니터링 실패입니다. 보안 이벤트를 로깅하지 않거나 적절한 모니터링이 없어서 공격을 탐지하지 못하는 그런 취약한 점이 되겠습니다.
[1주차 3차시 21:08] 보안 로깅 상당히 중요한 이슈인데요. 이전 차시에서도 얘기했지만 보안 사고를 예방하거나 보안 사고가 발생한 경우
[1주차 3차시 21:19] 피해 범위를 확인하고 복구하는 데 상당히 중요한 역할을 수행하겠죠. 이러한 취약점을 예방하기 위해 보안 이벤트 로깅과 중앙화된 로그 관리와 같은 보안 정책을 수립해야 합니다.
[1주차 3차시 21:41] SIEM이라든지 [불명확: 도입을] 여러 보안 장비를 도입을 해서 시스템에서 발생하는 로그와 이벤트를 모아서 이를 분석하고 이상징후를 실시간으로 탐지하고 대응할 수 있는 체계를 구축을 해야겠습니다.
[1주차 3차시 21:57] 보안사고가 발생한 경우 대응체계가 구축되어 있지 않으면 우왕좌왕하게 만들텐데요. 보안사고 대응체계를 미리 구축을 해서 사고 발생시 빠르게 대처할 수 있도록 해야겠습니다.
[1주차 3차시 22:13] 마지막
[1주차 3차시 22:14] 열 번째는 SSRF 서버 사이드 요청 위조입니다. 공격자가 서버를 이용해 내부 네트워크를 스캔하거나 외부 사이트를 공격하는 취약점입니다.
[1주차 3차시 22:32] 쉽게 말해 서버를 속여서 공격자가 원하는 곳으로 요청을 보내게 하는 공격이라고 볼 수 있습니다. 서버 사이드 요청 위조 취약점으로 인해서 내부 관리자 페이지 접근이 가능하거나 내부망을 스캔하거나
[1주차 3차시 22:48] 클라우드의 메타 데이터에 접근하는 것과 같은 피해 사례가 발생을 할 수가 있습니다. SSRF 공격은 사용자가 입력한 URL 등 외부 입력을 서버가 그대로 요청할 때 주로 발생되기 때문에 공격자가 내부망 주소, 민감한 리소스 주소를 넣지 못하도록 입력값 검증을 해야 합니다.
[1주차 3차시 23:13] 그래서 CSP는 Content Security Policy로
[1주차 3차시 23:17] 웹 브라우저에서 악성 컨텐츠가 로드되지 않도록 제어하는 HTTP 응답 헤더인데요. 원래 크로스 사이트 스크립트 방어 목적이 크지만 SSRF와 연계된 클라이언트 측 공격을 제한하는 데도 도움이 됩니다.
[1주차 3차시 23:38] 애플리케이션에서 웹으로 나가는 요청을 네트워크 장비나 보안 정책을 통해 통제해서 서버 사이드 위조 같은 공격이
[1주차 3차시 23:47] 내부 시스템으로 전파되지 않도록 막을 수가 있습니다. 이렇게 OWASP TOP10의 보안 취약점을 살펴보았는데요.
[1주차 3차시 23:57] 2021년 발표된 TOP10은 소프트웨어 개발 보안의 중요성을 좀 더 강조하고 있는 느낌입니다.
[1주차 3차시 24:07] OWASP API Security Risk TOP10은
[1주차 3차시 24:12] API 보안 위협 중 가장 자주 발생하고 위험도가 높은 10가지 유형의 보안 취약점과 이에 대한 대응 방안을 정리한 리스트입니다.
[1주차 3차시 24:24] 해당 리스트를 요약을 해보면 1번, 2번, 5번이 1번,
[1주차 3차시 24:33] 2번,
[1주차 3차시 24:34] 2, 3, 4 이렇게
[1주차 3차시 24:36] 5번 이렇게 세 가지가 접근 제어 실패인데요. 1번은 인증된 사용자라도 다른 사용자의 자원에 접근할 수 있는 취약점.
[1주차 3차시 24:46] 3번은 요청에서 전달된 속성 필드에 대한 권한 검사가 없어서 중요한 속성을 변경할 수 있는 취약점.
[1주차 3차시 25:03] 5번은 특정 기능에 대한 권한 검사를 하지 않아서 비인가 기능 수행이 가능한 취약점이 되겠습니다.
[1주차 3차시 25:13] 2번은 인증 세션 문제고 API 인증 메커니즘이 약해서 불법 접근이나 세션 탈취가 가능한 경우입니다.
[1주차 3차시 25:28] 4번과 6번은 과도한 요청 처리 [불명확: 비비] 4번은 API 요청을 무제한으로 보내면 서버 자원이 고갈되는 취약점 그리고 6번은
[1주차 3차시 25:42] 결제, 예약, 주문 등 핵심 비즈니스 로직에 속도 제한이나 검증이 없어 악용 가능한 취약점입니다.
[1주차 3차시 25:54] 그럼
[1주차 3차시 25:54] 이번에는 그렇게 10가지
[1주차 3차시 26:01] 간략하게 알아봤고 구체적인
[1주차 3차시 26:05] 내용들은
[1주차 3차시 26:05] 한번 직접
[1주차 3차시 26:07] 읽어보는
[1주차 3차시 26:09] 걸로 하겠습니다.
[1주차 3차시 26:16] 모바일 리스크 탑10도 모바일 애플리케이션 보안 취약점을 식별하고 대응하기 위한
[1주차 3차시 26:27] 제시하고 있는 부분인데요. 10가지도 강의 자료에 제시된 내용만 강의 자료로 제공하는 걸로 끝내도록 하겠습니다.
[1주차 3차시 26:44] 이번에는 CVE에 대해서 알아보도록 하겠습니다.
[1주차 3차시 26:51] CVE는 공통 취약점 및 노출 즉 Common Vulnerability Exposure의 약어인데요.
[1주차 3차시 27:04] 공개적으로 알려진 보안 취약점 목록을 관리를 하는 국제표준식별체계입니다. 쉽게 말해 전세계 보안 취약점에 고유한 아이디를 부여를 해서 누구나 동일하게 참조할 수 있도록 만들어 놓은 체계입니다.
[1주차 3차시 27:21] 즉 CVE는 보안 취약점을 표준화하고 추적하는 중요한 시스템이며 기업과 개발자는 이를 활용하여 보안성을 강화할 수 있습니다.
[1주차 3차시 27:34] 특히 소프트웨어 개발자는 CVE 데이터를 활용해서 보안 취약점을 사전에 예방하고 신속하게 패치를 적용할 수 있습니다.
[1주차 3차시 27:45] CVE는 MITRE라는 미국의 비영리 연구기관이 관리를 하고 있는데요. 연구기관 보안회사 등으로 구성된 파트너가 취약점을 등록하면 검토 후 CVE 번호가 부여가 됩니다.
[1주차 3차시 28:00] CVE 시스템의 동작 방식을 한번 보면
[1주차 3차시 28:04] 보안연구원, 기업, 기관 등이 새로운 보안 취약점을 먼저 일단 발견을 하고 그러면 CVE 넘버링 기관인 CNA라는 CVE 넘버링 어서리티의 취약점을 보고를 합니다.
[1주차 3차시 28:21] 그러면 이후에 마이터가 검토를 한 뒤에 CVE 아이디를 부여를 하게 되고 취약점 세부정보가 미국 국가 취약점 데이터베이스
[1주차 3차시 28:32] NVD에 등록되고 보안 패치와 대응책이 공개가 됩니다.
[1주차 3차시 28:39] CVE ID는 발생 연도와 시퀀스 번호로 구성이 되는데요.
[1주차 3차시 28:46] 예를 들어 CVE-2022-24086은 2022년도에 24806번째로 등록된 취약점이라는 의미입니다.
[1주차 3차시 29:01] 발견된 날짜, 영향을 받는 시스템, 취약점 설명, 해결 방법을 정리를 해서 CVE 사이트를 통해 배포가 됩니다.
[1주차 3차시 29:15] CVE는 보안사고가 발생된 취약점 사례인데요. 조직은 CVE를 기반으로 보안리스크를 분석하고 [불명확: 우리가]
[1주차 3차시 29:29] 분석을 하고 대응 계획을 수립을 할 수가 있습니다. 우리가 이제 학습한 위험 모델링을 수행을 할 때 참고할 수 있는 좋은 자료입니다.
[1주차 3차시 29:38] 개발 단계에서 이 CVE 데이터베이스를 활용을 해서 취약점 스캐너 및 도구 운영을
[1주차 3차시 29:46] 통해 서비스 배포 전에 주요 취약점들을 또 제거할 수 있도록 합니다.
[1주차 3차시 29:55] 이제 마지막으로 CWE TOP25에 대해 살펴보도록 하겠습니다.
[1주차 3차시 30:04] CWE는 Common Weakness Enumeration의 약자로 미 국토안보부에서 관리하는 소프트웨어와 하드웨어의 보안 약점을 체계적으로 정리해서 공개하는 목록입니다.
[1주차 3차시 30:23] CWE의 주요 목적은 소프트웨어 및 하드웨어 취약점을 분류하고 표준화하며 보안 취약점의 예방 및 완화를 위한 지침을 제공하는 건데요.
[1주차 3차시 30:35] 더불어 보안평가나 코드 분석 도구와 연계를 하여 소프트웨어의 보안성을 강화하도록 합니다. CWE는 개발자의 보안 코딩 가이드라인이나 정적 또는 동적 보안 점검 도구에서 CWE 목록 기반 취약점을 탐지하는 항목 그리고 OWASP,
[1주차 3차시 30:58] NIST, CVE 등과 연계하여 보안 개선 등에
[1주차 3차시 31:03] 다양한 곳에서 활용하고 있습니다.
[1주차 3차시 31:09] 그럼 이제 앞에서 설명했던 CVE와는 어떤 차이점이 있는지 한번 볼까요? CWE는 보안약점의 개념적인 분류라고 본다면 개념적인
[1주차 3차시 31:23] 정의고 CVE는
[1주차 3차시 31:26] 실제 특정 제품에서 발생한
[1주차 3차시 31:33] 보안 취약점이 되겠습니다. 그래서 A사의 B제품에서 보안사고가 발생했다면 보안사고를 통해 CVE가 NVD에 등록되어 있는 경우 해당 [불명확: 분서의] 상세 내용에서는 이 사고의 원인이 된 보안약점은 CWE-89가 원인이었다.
[1주차 3차시 31:56] 이런 식으로 작성이 된다고 보시면 되겠습니다.
[1주차 3차시 32:01] CWE의
[1주차 3차시 32:03] 경우에는 해마다 CWE TOP 25라는 목록을 발표를 하는데요. 소프트웨어에서 가장 위험한 보안 약점 25가지를 선정한 목록입니다.
[1주차 3차시 32:14] 개발자와 보안 전문가들이 우선적으로 대응해야 될 취약점을 제시를 하는 거고 이 목록 역시 마이터에서 관리를 하며 내셔널 NVD의 데이터를 기반으로 작성을 합니다.
[1주차 3차시 32:31] 선정 방법은 소프트웨어 보안 약점의 발생 빈도와 심각도를 기반으로 선정합니다. 더 구체적인 선정 방식은 넘어가도록 하겠습니다.
[1주차 3차시 32:47] CWE TOP25의 선정 목적은 가장 빈번하고 심각한 소프트웨어 약점을 강조해서 보안 사고를 예방하기 위함입니다.
[1주차 3차시 32:57] 개발 및 보안팀이 우선적으로 해결될 취약점을 파악하고 대응하도록 하여 소프트웨어의 보안을 강화하도록 하겠습니다.
[1주차 3차시 33:07] 또한 보안 교육과 훈련에 활용되어 안전한 코딩과 설계를 촉진하도록 하기 위한 목적도 있습니다.
[1주차 3차시 33:18] 취약점의 우선순위를 정하고 제한된 자원을 효과적으로 활용할 수 있도록 하는 것이 가장 큰 목적이 되겠습니다.
[1주차 3차시 33:33] 그래서 이 TOP25에 대해서는
[1주차 3차시 33:36] 이런 식으로 나와 있고요.
[1주차 3차시 33:40] 오늘 수업에서 강의에서 국외 소프트웨어 개발 보안 활동에 대해 알아봤는데요.
[1주차 3차시 33:48] OWASP TOP10 내용을 보면서 반드시 고려해야 될 보안 이슈들을 살펴보고 CWE 리스트의 내용은 어떤 용도를 가지고 있는지 CWE와의 차이점을 살펴보면서 이를 활용하여 소프트웨어 보안을 강화하는 활용법 등을 살펴보았습니다.
[1주차 3차시 34:10] 참고문은
[1주차 3차시 34:11] 다음과 같고요.
[1주차 3차시 34:13] 오늘
[1주차 3차시 34:14] 1주차 3차시까지 마무리를 해서 1주차 강의는 여기서 마무리하도록 하겠습니다.
[1주차 3차시 34:21] 감사합니다.

