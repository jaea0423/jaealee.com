# 2025_강원대_시큐어코딩_7주차_3차시_vF

<!-- p.1 -->

CSRF 취약점 진단 및 대응
01 CSRF 취약점 이해
02 CSRF 취약점 진단
03 CSRF 취약점 방어

---

<!-- p.2 -->

학습 목표
CSRF(크로스 사이트 요청 위조)의 개념과 공격 원리를 이해한다.
실제 CSRF 공격 기법을 학습하고, 취약점을 진단하는 방법을 익힌다.
CSRF 방어 기법을 적용하여 웹 애플리케이션 보안을 강화할 수 있다.

---

<!-- p.3 -->

학습 내용
1. CSRF 취약점 이해
2. CSRF 취약점 진단
3. CSRF 취약점 방어

---

<!-- p.4 -->

CSRF 취약점 진단 및 대응
01 CSRF 취약점 이해
02 CSRF 취약점 진단
03 CSRF 취약점 방어

---

<!-- p.5 -->

CSRF(크로스 사이트 요청 위조)란?
정의
Cross-Site Request Forgery의 약자로, 사용자의 인증 정보를 이용해 의도치 않은 요청을 강제 실행하는 공격
→ 공격자가 악의적인 웹 페이지, 이메일, 또는 다른 매체를 통해 사용자의 브라우저에 요청을 보내도록 유도
취약점 배경
웹 애플리케이션이 인증 상태(쿠키 등)를 기반으로 요청을 처리하는 구조
브라우저는 같은 도메인에 대한 요청 시 자동으로 쿠키를 전송하므로, 사용자가 의도치 않은 요청에도 인증 정보를 포함하게 됨

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림: CSRF 공격 개념도 (왼쪽 → 오른쪽 흐름)]**

- 왼쪽: 후드를 쓴 가면(가이 포크스 가면) 해커가 노트북 앞에 있음 (공격자).
- → 주황색 라벨 **"CSRF"**가 붙은 화살표 → 가운데: 책상에서 노트북을 쓰는 정장 차림 사용자(로그인한 피해자).
- → 라벨 **"Cookies"**가 붙은 화살표 → 한 입 베어 문 쿠키 그림 → 화살표 → 오른쪽: 서버 본체 + 모니터. 모니터 속 브라우저 창 주소창에 `http://`, 창 안에 **"CSRF"** 글자.
- 의미: 공격자가 CSRF 요청을 사용자에게 심으면, 사용자의 브라우저가 쿠키(인증 정보)를 자동으로 붙여 서버에 요청을 보내게 됨.

---

<!-- p.6 -->

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

<!-- p.7 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## CSRF 취약점 공격 흐름

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

<!-- p.8 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 검증: Python `urllib.parse`로 두 URL을 분해 — `https://bank.com/transfer` 경로에 쿼리 `to=hacker`, `amount=1000000`(100만), `http://sns.com/like` 경로에 `postId=434`. `<img>`·`<iframe>`의 `src`는 페이지 로드 시 브라우저가 자동으로 GET 요청을 보내므로, 클릭 없이도 이 상태 변경 요청이 쿠키와 함께 전송됨 — 슬라이드 설명과 일치)

---

<!-- p.9 -->

CSRF와 XSS의 차이점
XSS(크로스 사이트 스크립팅)
공격자가 웹 사이트에 악성 스크립트를 삽입, 사용자의 웹 브라우저에서 실행
주로 브라우저 내 스크립트 조작 및 쿠키 탈취, UI 변조에 활용
CSRF(크로스 사이트 요청 위조)
공격자가 사용자 대신 다른 웹 사이트에 요청을 보내도록 유도
서버 입장에서 사용자 의도와 무관한 요청을 정상 요청으로 오인

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[그림: XSS vs CSRF 비교 일러스트 (오른쪽 아래)]**

- 하늘색 배경에 검은 캐릭터 두 명.
- 왼쪽 캐릭터: 몸에 **"XSS"**, 손에 **`<script>`** 팻말을 들고 브라우저 창(점 3개 탭, 입력창) 앞에 서 있음 → 웹 페이지에 스크립트를 삽입하는 공격.
- 오른쪽 캐릭터: 몸에 **"CSRF"**, 뒤에는 **Login** 버튼이 있는 로그인 화면 모니터. XSS 캐릭터가 오른쪽 캐릭터 쪽으로 **"FAKE FORM"** 종이를 내밀고 있음 → 위조된 폼(요청)으로 로그인된 사용자의 권한을 악용하는 공격.

---

<!-- p.10 -->

CSRF 공격 사고 사례

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.11 -->

CSRF 취약점 진단 및 대응
01 CSRF 취약점 이해
02 CSRF 취약점 진단
03 CSRF 취약점 방어

---

<!-- p.12 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 검증: Python으로 URL 분해 — `https://target.com/deleteAccount` 경로, 쿼리 `user=123`. `<img>` 태그는 렌더링 시 src로 GET 요청을 자동 전송하므로 계정 삭제 같은 상태 변경을 GET으로 처리하는 서버라면 쿠키와 함께 실행됨 — 일치)

---

<!-- p.13 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## CSRF 공격 기법

### 예시 1: GET 요청을 이용한 CSRF

공격자 페이지 코드

```html
<!-- 공격자가 피해자에게 보낼 악의적 링크 예시 -->
<img src="https://target.com/action?param=value" alt="image" />
```

피해자가 해당 페이지를 로드하면, 브라우저가 자동으로 GET 요청을 보내고, 서버는 피해자의 쿠키와 함께 요청을 처리

### 예시 2: POST 요청을 이용한 CSRF (숨겨진 폼 & 자동 제출)

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

<!-- p.14 -->

CSRF 공격 기법
예시 3: 링크 클릭을 유도하는 사회공학적 CSRF
공격자가 피해자에게 URL을 포함한 메시지(예: 이메일, SNS)를 보내어 클릭을 유도
(예) https://target.com/updateEmail?newEmail=attacker@example.com
피해자가 링크를 클릭하면, 피해자의 인증 정보와 함께 요청이 실행되어 이메일 변경 등의 작업이 이루어짐

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 검증: Python `urllib.parse`로 분해 — 경로 `/updateEmail`, 쿼리 `newEmail=attacker@example.com` 한 개. 쿼리 안의 `@`는 인코딩(`%40`) 없이도 정상 파싱됨 — 일치. 이메일이 공격자 주소로 바뀌면 '비밀번호 찾기'로 계정 탈취까지 이어질 수 있는 대표 시나리오)

---

<!-- p.15 -->

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

<!-- p.16 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 검증: Python으로 URL 분해 — `https://vulnerable.com/deleteAccount`, 쿼리 `userId=123` — 일치. 12쪽 예시는 파라미터명이 `user=123`, 이 쪽은 `userId=123`으로 서로 다른 가상 예시임)

---

<!-- p.17 -->

CSRF 취약점 진단 및 대응
01 CSRF 취약점 이해
02 CSRF 취약점 진단
03 CSRF 취약점 방어

---

<!-- p.18 -->

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

<!-- p.19 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## CSRF 토큰 적용 및 활용

### Spring Security Java Configuration 예시

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

### HTML FORM에 CSRF 토큰 적용 (Thymeleaf 예시)

Thymeleaf 환경에선 자동으로 히든 필드로 추가됨

```html
<form th:action="@{/update}" method="post">
    <input type="text" name="data" />
    <!-- Spring Security가 자동으로 CSRF 토큰 숨은 필드로 삽입 -->
    <button type="submit">제출</button>
</form>
```

### AJAX 요청에서 CSRF 토큰 사용

1) HTML 생성시 meta 태그에서 토큰 이름과 값을 넣어 보냄
2) 스크립트에서 meta 태그의 토큰 이름/내용을 가져와 포함시켜 전송

```html
<!-- CSRF 토큰 메타 태그 -->
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

<!-- p.20 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## SameSite Cookie 정책 설정

### SameSite Cookie란?
- 브라우저에서 웹 요청 시 어떤 조건 하에 쿠키가 함께 전송될지 제어하는 속성
- CSRF 공격 등 외부 사이트에서의 악의적 요청으로부터 보호

### 주요 속성 값
- **Strict**
  - 쿠키가 오직 동일 사이트 내 요청에만 전송됨
- **Lax**
  - 최초 타 사이트 접속하는 경우만 전송하고 그 외 크로스사이트 요청들엔 차단
- **None**
  - 모든 요청에서 쿠키 전송
  - 반드시 Secure 플래그와 함께 사용해야 함

### CSRF 대응 효과
다른 도메인으로부터의 요청에 쿠키가 자동으로 포함되지 않아, CSRF 공격 위험 감소

```http
HTTP/1.1 200 OK
Set-Cookie: JSESSIONID=ABC123DEF456; Path=/; HttpOnly; SameSite=Strict
```
(박스 안에서 `SameSite=Strict`가 굵게 강조됨)

(※ 검증: Python `http.cookies.SimpleCookie`로 Set-Cookie 값을 파싱 — 이름 `JSESSIONID`, 값 `ABC123DEF456`, `path=/`, `httponly=True`, `samesite=Strict` — 일치. 보충: Lax의 정확한 동작은 "다른 사이트에서 링크 클릭 등 최상위(top-level) 이동 + 안전한 메서드(GET)일 때만 쿠키 전송, `<img>`·`<iframe>`·POST 폼 등 크로스사이트 하위 요청에는 미전송". 그래서 Lax만으로도 8·13쪽의 img/POST 자동 제출 공격은 막히지만, 14쪽처럼 GET 링크 클릭으로 상태가 바뀌는 기능은 여전히 위험. 최신 Chrome 등은 SameSite 미지정 쿠키를 Lax로 취급)

---

<!-- p.21 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## SameSite Cookie 정책 설정

### Spring Boot 설정 예시

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

### Node.js (Express) 설정 예시

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

<!-- p.22 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Origin/Referer 검증 및 세션 관리 보안 강화

### Origin/Referer 검증의 개념
- HTTP 요청 헤더의 Origin/Referer 값을 확인하여, 요청이 올바른 출처(도메인)에서 발생했는지 검증
- 공격자가 외부 사이트에서 악의적 요청을 보내는 것을 사전에 차단하는 역할

### 필요성
- CSRF 공격 및 핫링크(Hotlinking)와 같은 외부 위협을 감소시킴
- 민감한 기능(예: 결제, 계정 변경 등)에 대한 요청이 예상된 출처에서 발생했음을 보장

### 구현 방법 예시
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

<!-- p.23 -->

요약 정리
- CSRF는 로그인된 세션 쿠키를 악용해 사용자가 의도치 않은 요청을 보내도록 유도하는 취약점이다.
- 피싱 링크나 악성 웹페이지로 사용자를 유도해, 브라우저 자동 전송 쿠키를 이용한 요청이 발생한다.
- 이미지·폼·링크 등을 통해 계정 변경, 자금 이체 등 민감 동작이 자동 실행될 수 있다.
- CSRF 토큰·SameSite 쿠키·Referer/Origin 검증을 병행 적용해 공격 표면을 최소화해야 한다.

---

<!-- p.24 -->

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

<!-- p.25 -->

감사합니다.

---

<!-- p.26 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 퀴즈

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

<!-- p.27 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(정답 표시: 1번 "1) 중요 웹사이트에 로그인되어 쿠키를 보유하고 있어야 한다.", 2번 "4) 암호화된 비밀번호로 로그인 처리", 3번 괄호 안 "SameSite"가 빨간 글씨로 표시됨. ※ 검증: 26쪽 보기와 대조 — 1번의 2)·3)·4)는 모두 방어 측 조치라 공격 성립 조건이 아니고, 2번의 1)~3)은 18~22쪽에서 다룬 방어 기법(토큰·SameSite·Origin/Referer)이므로 정답 1 / 4 / SameSite — 일치)
