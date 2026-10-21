# 2025_강원대_시큐어코딩_3주차_2차시_vF (1)

<!-- p.1 -->

실습환경 구축-2
01 SpringBoot 프레임워크를 활용한 웹 프로젝트 구축(1)

---

<!-- p.2 -->

학습 목표
SpringBoot 프레임워크의 개념과 역할을 이해한다.
SpringBoot 프레임워크의 기본 사용법을 익힌다.

---

<!-- p.3 -->

학습 내용
1. 프레임워크와 플랫폼의 개념 및 차이
2. 기본 웹 애플리케이션 작성 및 실행

---

<!-- p.4 -->

실습환경 구축-2
01 SpringBoot 프레임워크를 활용한 웹프로젝트 구축(1)

---

<!-- p.5 -->

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

<!-- p.6 -->

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

<!-- p.7 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
프레임워크(Framework)와 플랫폼(Platform) 개념 및 차이 — 프레임워크 vs 플랫폼 비교

| 구분 | 프레임워크 | 플랫폼 |
| --- | --- | --- |
| 역할 | 개발을 위한 기본 구조 제공 | 애플리케이션이 실행되는 환경 제공 |
| 범위 | 제한적(특정 도구 및 기능 제공) | 넓음(하드웨어, 소프트웨어, 서비스 포함) |
| 예시 | Spring, Django, React, Flutter | Window, Linux, Android, iOS |
| 강제성 | 특정 패턴을 강제(ex: MVC) | 실행환경만 제공(개발방식을 강제하지 않음) |

---

<!-- p.8 -->

Spring Boot 프레임워크란?
Spring Boot는 자바기반의 웹 애플리케이션을 만들 수 있는 Spring 프레임워크를 기반으로 개발 프레임워크로,
설정(Configuration) 없이 빠르게 Spring 기반 애플리케이션을 개발 할 수 있도록 지원하는 프레임워크
SpringBoot은 내장 웹서버 제공, 자동설정(Auto Configuration), 의존성 관리 등의 기능을 통해
개발자의 생산성을 극대화 함.

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.9 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
Spring Boot vs. Spring Framework

| 비교항목 | Spring Framework | Spring Boot Framework |
| --- | --- | --- |
| 설정방식 | XML 또는 자바 설정 필요 | 자동 설정(Auto Configuration) 지원 |
| 의존성 관리 | 수동으로 라이브러리 추가 | spring-boot-starter로 간편하게 관리 |
| 내장 서버 | 별도 WAS 필요 | 내장 서버 제공(Tomcat 기본 포함) |
| 배포 방식 | WAR 패키징 필요 (WAS필요) | JAR 패키징(독립 실행 가능) |
| 학습난이도 | 상대적으로 복잡 | 쉬운 시작 가능 |

---

<!-- p.10 -->

Spring Boot 기본 사용법
Step1. STS (Spring Tool Suite) 다운로드 및 설치
공식 사이트(https://spring.io/tools)에 접속하여 IDE를 다운로드 받는다.

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[캡처: 'Spring Tools for Eclipse — Free. Open source.' 다운로드 버튼 5개 — 4.28.1 - LINUX X86_64 / LINUX ARM_64 / MACOS X86_64 / MACOS ARM_64 / **WINDOWS X86_64**, 옆에 STS 화면 캡처와 Eclipse 로고]

---

<!-- p.11 -->

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

<!-- p.12 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[Spring Initializr 화면 캡처]
- Project: ○ Gradle-Groovy ○ Gradle-Kotlin ◉ **Maven** / Language: ◉ **Java** ○ Kotlin ○ Groovy
- Spring Boot: ○ 3.5.0 (SNAPSHOT) ○ 3.5.0 (M2) ○ 3.4.4 (SNAPSHOT) ◉ **3.4.3** ○ 3.3.10 (SNAPSHOT) ○ 3.3.9
- Project Metadata: Group `com.example` / Artifact `hello-spring-boot` / Name `hello-spring-boot` / Description `Demo project for Spring Boot` / Package name `com.example.hello-spring-boot`
- Dependencies: **Spring Web** [WEB] — "Build web, including RESTful, applications using Spring MVC. Uses Apache Tomcat as the default embedded container."
- 아래 버튼 [GENERATE CTRL+⏎] [EXPLORE CTRL+SPACE] […]

---

<!-- p.13 -->

Spring Boot 기본 사용법
Step3. HelloSpringBootApplication.java 생성 및 코드 추가
- @SpringBootApplication: Spring Boot 애플리케이션의 기본 설정을 담당
- SpringApplication.run(HelloSpringBootApplication.class, args); : 애플리케이션 실행

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.14 -->

Spring Boot 기본 사용법
Step４. HelloController.java 생성 후 코드 추가
- @RestController: REST API를 위한 컨트롤러임을 선언
- @RequestMapping("/api"): 기본 URL 경로를 /api로 설정
- @GetMapping("/hello"): /api/hello 요청이 들어오면 "Hello, Spring Boot!"를 반환

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.15 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[명령어 상자]
- 방법2: `mvn spring-boot:run`
- 방법3: `mvn clean package` → `java -jar target/hello-spring-boot-0.0.1-SNAPSHOT.jar` (슬라이드에는 `Java`로 대문자 표기)

---

<!-- p.16 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[Postman 로고. 주소 상자: `http://localhost:8080/api/hello`]

---

<!-- p.17 -->

Spring Boot 기본 사용법
Step7. 애플리케이션 종료 또는 재시작
1. Spring Boot 애플리케이션 종료
- STS 콘솔에서 Ctrl + C 또는 Stop(붉은 사각) 버튼 클릭
2. Spring Boot 애플리케이션 재시작
- MainApplication.java 우클릭 → Run As → Spring Boot App

---

<!-- p.18 -->

시연 영상
Spring Boot 신규 프로젝트 작성

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[시연 영상 자리 — 'Spring Boot 신규 프로젝트 작성'. PDF에는 영상이 포함되지 않아 빈 화면]

---

<!-- p.19 -->

요약 정리
- 프레임워크는 소프트웨어 개발을 위한 구조와 규칙을 제공하는 코드 라이브러리
- 플랫폼은 애플리케이션이 실행될 수 있는 환경을 포괄적으로 칭함
- Spring Boot 프레임워크는 Spring 프레임워크 기반으로 빠르게 자바 기반의 웹 애플리케이션을
만들 수 있도록 지원함
- Spring Initializr를 사용하면 신규 프로젝트를 생성하고 개발 가능

---

<!-- p.20 -->

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

<!-- p.21 -->

감사합니다.

---

<!-- p.22 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
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

<!-- p.23 -->

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
