# 2025_강원대_시큐어코딩_4주차_3차시_vF (1)

<!-- p.1 -->

정규식을 활용한 입력값 필터링
01 입력값 필터 만들기

---

<!-- p.2 -->

학습 목표
정규식을 활용하여 입력값을 필터링 하는 필터를 구현한다
Spring Boot 프레임워크에 필터를 적용한다.
XSS 대응을 위한 필터를 적용하여 취약점을 제거한다.

---

<!-- p.3 -->

학습 내용
1. 정규식으로 입력값을 필터링 할 수 있는 필터 제작
2. SpringBoot 프레임워크에서 필터를 적용하여 입력값 필터링
3. XSS 취약점의 기본적인 이해 및 필터링 적용

---

<!-- p.4 -->

정규식을 활용한 입력값 필터링
01 입력값 필터 만들기

---

<!-- p.5 -->

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

<!-- p.6 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
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

<!-- p.7 -->

Spring Boot 에서 필터 구현 방법
STEP1. 기본 필터 구현

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.8 -->

Spring Boot 에서 필터 구현 방법
STEP2. 필터를 Spring Boot 에 등록
(방법1) @Component를 사용하여 자동 등록

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.9 -->

Spring Boot 에서 필터 구현 방법
STEP2. 필터를 Spring Boot 에 등록
(방법2) FilterRegistrationBean을 사용하여 수동 등록(우선순위 지정이 필요한 경우)
FilterConfig

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.10 -->

Spring Security 와 기본 필터
Spring Security 사용 시 자동으로 보안 필터 적용
Spring Security에는 로그인, 인증, 권한체크 등을 처리하는 필터가 포함되어 있음.
DefaultSecurityConfig

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.11 -->

입력값 필터 만들기
XSS (Cross-Site Scripting) 공격이란
게시판처럼 입력 내용 그대로 표출되는 곳에 악성 스크립트를 넣어, 서비스 이용자의 브라우저에서 실행되도록 하는 공격
XSS 공격 방어 전략
〮 사용자 입력값에서 위험한 패턴의 문자열을 필터링
〮 SpringBoot의 ServletFilter와 HttpServletRequestWrapper를 이용하여 모든 요청의 입력값을 가로챔
〮 입력값의 내용을 정규식으로 패턴을 확인하여 필터링 처리
웹 브라우저 XSSFilter XSSRequestWrapper Controller 웹 브라우저

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[흐름도] 웹 브라우저 → **XSSFilter** → **XSSRequestWrapper** → Controller → 웹 브라우저

---

<!-- p.12 -->

입력값 필터 만들기
XSS 필터 구현
모든 HTTP Request를 XSSRequestWrapper로 감싸서 모든 요청 내용의 입력 값 필터링하도록 함
p043_XSSFilter.java

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.13 -->

입력값 필터 만들기
XSSRequestWrapper 구현
p043_XSSRequestWrapper.java
1) <script> 태그와 그 사이의 내용을 제거
2) onclick, onerror 등의 이벤트 핸들러 제거
3) javascript: 문자열 제거

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.14 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
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

<!-- p.15 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[브라우저 캡처: `localhost:8000/board/write` 게시글 작성 화면, 제목 칸(빨간 상자)에 `asfdasfds<script>alert('XSS!!');</script>`, 내용 칸에 `testtest`]

---

<!-- p.16 -->

LAB1 - 소스코드의 XSS 취약점 확인
6. 게시판 목록 화면에서 해당 게시글 제목에 스크립트
내용이 보여짐
7. 해당 게시글을 클릭하면 스크립트가 동작하여 화면에
경고창이 나타남
XSS 취약점 있는 것이 확인됨

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[브라우저 캡처 2장]
1. 게시판 목록(`/board/list`): 제목 칸에 `asfdasfds<script>alert('XSS!!');</script>`가 글자 그대로 보임(빨간 상자), 작성자 테스트, 작성일 2025-02-25
2. 게시글 조회(`/board/view?idx=3`): 'localhost:8000 — XSS!!' 경고창이 뜸 → 스크립트가 실행됨

---

<!-- p.17 -->

LAB2 - 소스코드에 XSS 필터 반영
1. 서비스 실행 중이라면, 상단 ■ 버튼을 눌러 중지
2. STS의 좌측 Package Explorer에서
kr.co.openeg.lab을 찾아 마우스 오른쪽 버튼 클릭
3. New > Package 선택

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[STS 캡처: 상단 툴바의 ■(빨간 정지) 버튼(빨간 화살표) / Package Explorer의 `kr.co.openeg.lab` 우클릭(빨간 화살표) → **New** → **Package** (파란 상자)]

---

<!-- p.18 -->

LAB2 - 소스코드에 XSS 필터 반영
3. Java Package 창에서 Name 항목에
kr.co.openeg.lab.filter.xss 입력
4. Finish 버튼

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
['New Java Package' 창: Source folder `SecureCoding/src/main/java`, **Name: `kr.co.openeg.lab.filter.xss`**(빨간 상자) → [Finish](빨간 화살표)]

---

<!-- p.19 -->

LAB2 - 소스코드에 XSS 필터 반영
5. 폴더에서 XSS 필터 소스코드 2개를 선택한 후, 새롭게
생성하여 비어있는 패키지로 Drag & Drop
6. 파일 Import 방법으로 'Copy files' 선택한 후 OK버튼

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[캡처: 탐색기 '4주차' 폴더의 파일 목록(p031_RegexExample, p032_RegexValidation, p033_RegexReplace, p034_PasswordRegex…, **p043_XSSFilter.java**, **p043_XSSRequestWrapper.java** 선택) → STS의 `kr.co.openeg.lab.filter.xss` 패키지로 드래그(빨간 화살표) → 'File Operation' 창에서 ◉ **Copy files** → [OK]]

---

<!-- p.20 -->

LAB2 - 소스코드에 XSS 필터 반영
7. 프로젝트 명에서 마우스 우측 클릭한 후
Maven > Update Project 실행
8. 빌드 완료 확인
9. 프로젝트 명에서 마우스 우측 클릭한 후
Run As > Spring Boot App 실행
10.OK 버튼을 눌러 서비스 다시 실행

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[STS 캡처: 프로젝트 우클릭 → Maven → **Update Project…** → 'Update Maven Project' 창 [OK] / 프로젝트 우클릭 → Run As → **Spring Boot App** → 'Select Java Application'에서 `SecureCodingLabTestApplication - kr.co.openeg.lab` 선택 → [OK]]

---

<!-- p.21 -->

LAB3 - 소스코드에서 XSS 필터 동작 확인
1. 파이어폭스에서 서비스 재 접속 및 로그인
2. 게시판에 들어가서 마찬가지로 새 글 작성 및 제목에
스크립트 구문 입력
3. 확인 버튼 눌러 글 등록 후 목록에서 제목 확인
제목에 스크립트 부분이 제외된 것이 확인됨
해당 글을 눌러 들어가도 경고창이 나타나지 않고 글 내용이 나타남.
XSS 필터가 글 등록 직전 정상적으로 동작하여
스크립트 구문을 삭제한 것이 확인됨

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[브라우저 캡처 3장]
1. 글쓰기: 제목 `adfsafa<script>alert('XSS!!');</script>` 입력(빨간 상자)
2. 목록: 제목이 **`adfsafa`**만 남음(빨간 상자) — 스크립트 부분이 삭제됨
3. 조회: 제목 `adfsafa`, 경고창 없이 내용 `testtest` 표시

---

<!-- p.22 -->

시연 영상
- XSS 필터 만들기

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[시연 영상 자리 — 'XSS 필터 만들기'. PDF에는 영상이 포함되지 않음]

---

<!-- p.23 -->

요약 정리
- 필터는 클라이언트의 HTTP 요청과 응답을 가로채어 특정 작업을 수행하는 서블릿 기반 컴포넌트로
웹 애플리케이션에서 보안, 로깅, 데이터변환등의 작업을 수행할 때 사용
- Spring Security 를 설치하면 로그인, 인증, 권한체크 등을 처리하는 필터가 기본적으로 적용
- 웹애플리케이션의 XSS 취약점을 방어하기 위해 XSS Filter를 생성해서 프레임워크에 적용

---

<!-- p.24 -->

참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [secu BOOK] 웹 해킹과 시큐어코딩 탐지/수정 실습가이드
- [에이콘출판사] 보안 위협 모델링 Threat Modeling - 위협 식별과 대응을 위한 소프트웨어 설계
- [위키북스] 웹 애플리케이션 보안 완벽 가이드 - 체계적으로 배우는 안전한 웹 애플리케이션 제작 기법

---

<!-- p.25 -->

감사합니다.

---

<!-- p.26 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
퀴즈

1. 클라이언트의 HTTP 요청과 응답을 가로채어 특정 작업을 수행하는 서블릿 기반 컴포넌트는 무엇인가?
   1) Dispatcher　2) Handler　3) Filter　4) ViewResolver
2. String 클래스에서 정규식으로 지정한 문자열을 다른 문자열로 바꾸기 위해 사용하는 메서드 이름은? (영문 10글자, . 제외)　(　　)
3. 다음 중 XSS 입력값 필터에서 처리해야 하는 내용이 아닌 것은?
   1) <script> 태그와 그 사이 내용을 제거　2) javascript: 문자열 제거
   3) onclick, onerror 등의 이벤트 핸들러 제거　4) 압축파일 안에 들어있는 스크립트 파일 제거

---

<!-- p.27 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
퀴즈 정답

1. **3) Filter** — ※ 원본 정답 쪽에는 "2) Filter"로 인쇄되어 있지만, 문제의 보기에서 Filter는 **3번**입니다(2번은 Handler).
2. **( replaceAll )**
3. **4) 압축파일 안에 들어있는 스크립트 파일 제거** — 압축파일을 다루는 작업은 필터에서 처리하기에 매우 많은 리소스를 사용하며, XSS 공격 방어와도 관련이 없습니다.
