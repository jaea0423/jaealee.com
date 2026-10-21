# 2025_강원대_시큐어코딩_5주차_1차시_vF

<!-- p.1 -->

인증과 인가 기초
01 인증과 인가 개요
02 인증 및 인가의 동작 과정
03 보안 위협 및 해결 방법

---

<!-- p.2 -->

학습 목표
인증과 인가의 개념을 이해하고 차이점을 설명할 수 있다.
현대 애플리케이션 보안과제를 해결하기 위한 방안을 이해한다.
사고 사례를 통한 시큐어코딩을 이해한다.

---

<!-- p.3 -->

학습 내용
1. 인증과 인가 개요
2. 인증 및 인가의 동작 과정
3. 보안위협 및 해결 방법

---

<!-- p.4 -->

인증과 인가 기초
01 인증과 인가 개요
02 인증 및 인가의 동작 과정
03 보안 위협 및 해결방법

---

<!-- p.5 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 인증과 인가의 차이

| 인증(Authentication) | 인가(Authorization) |
|---|---|
| (그림: openmaru 로고(판독 확신 낮음)가 있는 사원증 'JOHN DOE / ID CARD' — 신원 확인을 상징) | (그림: 태블릿 화면의 항목 목록 — 첫 항목은 녹색 체크(허용), 나머지 두 항목은 빨간 X(거부) — 권한 허용/제한을 상징) |
| 인증은 시스템 접근 시, 등록된 사용자인지 여부를 확인하는 것.<br>ex) 로그인 | 인증 후 사용자에게 리소스에 접근 가능한 권한을 부여하는 것과 제한하는 것<br>ex) 사용자 등급(일반사용자/관리자/개인정보취급자) |

그림출처: openmaru.com

---

<!-- p.6 -->

인증 방식 이해
인증은 내가 “나”임을 증명하는 것으로, 인증방법에 따라 지식기반, 소유기반, 생체기반의 방식으로 구분할 수 있다.
가장 널리 사용되는 인증방식이 아이디(ID)와 패스워드(password)를 사용하는 방식이다.
지식기반 인증(ID/PWD) 소유기반 인증 생체기반 인증
그림출처: openmaru.com

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.7 -->

인증 방식 이해 – 지식기반 인증
정의
사용자가 알고 있는 정보를 기반으로 본인 여부를 확인하는 인증 방식(예: 비밀번호, PIN, 보안 질문)
장점
구현 및 사용이 비교적 간편하고 사용자에게 익숙 (비밀번호)
단점
사회공학적 공격, 정보 유출 시 위험 증가, 예측 가능한 질문의 경우 보안 취약
보완 방안
다단계 인증(MFA)과 결합하여 보안 강화, 주기적인 질문 및 답변 업데이트 권장

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[이미지 보충]** 오른쪽에 지식기반 인증 예시 캡처(6쪽과 동일): Chrome 'T world' 'T아이디 로그인' 화면(`https://auth.skt-id.co.kr/auth/authorize.do?client_id=2590d318-0816-...`, 아이디·비밀번호 입력칸)과 그 위에 겹친 '아이핀' 로그인 창('아이핀ID'·'비밀번호' 입력 + [확 인], 신규발급 / ID/비밀번호찾기 / 아이핀관리 / 고객센터, "타 웹사이트와 동일한 ID, 비밀번호를 사용하면 도용위험이 있으니 비밀번호 변경을 권장합니다.").

---

<!-- p.8 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[이미지 보충]** 오른쪽에 소유기반 인증 예시(6쪽과 동일): KB국민은행 OTP 토큰 사진('www.kbstar.com ☎1588-9999')과 공동인증서 선택 창(인증서 저장 위치: 하드디스크 / 이동식 / 보안토큰 / 휴대폰 / 안전디스크 / 간편인증, '사용할 인증서를 선택해 주세요' 목록 — 구분·사용자·만료일·발급자, '인증서 암호를 입력해 주세요' 입력칸, [확인] [취소]).
(※ 원문 표기 그대로 — 단점 둘째 줄이 '관리 체계 구축 필요,'처럼 쉼표로 끝남)

---

<!-- p.9 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[이미지 보충]** 오른쪽에 생체기반 인증을 상징하는 홍채(눈) 흑백 근접 사진과 지문 이미지가 겹쳐 있음.

---

<!-- p.10 -->

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

<!-- p.11 -->

인증과 인가 기초
01 인증과 인가 개요
02 인증 및 인가의 동작 과정
03 보안 위협 및 해결방법

---

<!-- p.12 -->

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

<!-- p.13 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 세션 기반 인증

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

<!-- p.14 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## LAB 세션 처리 확인

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

<!-- p.15 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## LAB 세션 처리 확인

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

<!-- p.16 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 토큰 기반 인증

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

<!-- p.17 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## JWT 로그인 세션 처리 확인

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

<!-- p.18 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## JWT 로그인 세션 처리 확인

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

<!-- p.19 -->

인증과 인가 기초
01 인증과 인가 개요
02 인증 및 인가의 동작 과정
03 보안 위협 및 해결방법

---

<!-- p.20 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 주요 인증 보안 위협

| 위협 | 설명 | 예제 |
|---|---|---|
| 비밀번호 기반 공격<br>(Credential Stuffing, Dictionary Attack) | 공격자가 유출된 사용자 계정을 활용하여 로그인 시도 | -자동화된 스크립트로 유출된 계정/비밀번호 조합을 입력<br>- 쉬운 비밀번호(123456, password 등)를 대입 |
| 피싱(Phishing) & 소셜 엔지니어링 | 사용자에게 속여 로그인 정보를 탈취 | - 가짜 로그인 페이지를 만들어 사용자 입력을 유도 |
| 중간자 공격<br>(MITM, Man-In-The-Middle Attack) | 네트워크 트래픽을 가로채 인증 정보를 탈취 | - 공용 Wi-Fi에서 패킷을 가로채 로그인 정보 수집 |
| 세션 탈취<br>(Session Hijacking) | 공격자가 유효한 세션 ID를 도용하여 로그인 상태를 유지 | - 쿠키 탈취(document.cookie), 세션 ID 도용 |
| 무차별 대입 공격<br>(Brute Force Attack) | 여러 비밀번호를 반복 시도하여 로그인 시도 | - 봇을 사용하여 다양한 비밀번호 조합을 입력 |
| 취약한 OTP / MFA<br>(Multi-Factor Authentication) 우회 | 2FA(이중 인증) 우회 공격 | - 2FA 코드 스니핑, SIM 스와핑(SIM Swapping) |

---

<!-- p.21 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 주요 인증 보안 위협 대응 방안

| 대응방법 | 설명 |
|---|---|
| 강력한 비밀번호 정책 | - 최소 8~12자 이상, 대문자/소문자/숫자/특수문자 조합 사용<br>- 비밀번호 재사용 방지 (이전 비밀번호 사용 불가) |
| 계정 잠금 (Account Lockout) | - 일정 횟수 이상 로그인 실패 시 계정 잠금 |
| 다중 매체 인증 (MFA, Multi-Factor Authentication) | - OTP, 인증 앱(Google Authenticator), FIDO2 등 추가 인증 적용 |
| HTTPS 사용 및<br>HSTS (HTTP strict-transport-security) 적용 | - 네트워크 암호화(SSL/TLS) 적용 |
| 세션 보안 강화 | - Secure, HttpOnly, SameSite 쿠키 적용<br>- 세션 타임아웃 설정 |
| 로그인 알림 및 로그 모니터링 | - 로그인 시 이메일/SMS 알림<br>- 비정상적인 로그인 감지 |
| CAPTCHA 적용 | - 봇(Bot) 기반 로그인 시도를 방지 |

---

<!-- p.22 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 주요 인가 보안 위협

| 위협 | 설명 | 예제 |
|---|---|---|
| 권한 상승 공격<br>(Privilege Escalation) | 낮은 권한의 사용자가 관리자 권한을 얻음 | - 일반 사용자가 관리자 계정으로 변경 |
| 수평적 권한 상승<br>(Horizontal Privilege Escalation) | 동일 권한 내에서 다른 사용자의 데이터에 접근 | - user_id=123을 user_id=124로 변경하여 다른 사용자 정보 접근 |
| 수직적 권한 상승<br>(Vertical Privilege Escalation) | 일반 사용자가 관리 권한을 얻음 | - 웹 요청을 수정하여 admin=true 설정 |
| 취약한 객체 직접 참조<br>(IDOR, Insecure Direct Object References) | 다른 사용자의 데이터에 직접 접근 | - /user/1001/profile → /user/1002/profile 변경하여 다른 사용자의 정보 조회 |
| CSRF (Cross-Site Request Forgery) | 사용자의 세션을 이용하여 공격자가 악의적인 요청 수행 | - 사용자가 로그인된 상태에서 공격자가 강제 요청 실행 |
| 불충분한 API 권한 검증 | API 요청에서 적절한 권한 검사가 없음 | - GET /admin/users API가 일반 사용자에게도 노출됨 |
| URL 기반 접근 통제 부족 | URL만 알면 누구나 접근 가능 | - /admin/dashboard에 접근할 수 있는 사용자 제한이 없음 |

---

<!-- p.23 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 주요 인가 보안 위협 대응 방안

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

<!-- p.24 -->

요약 정리
- 인증은 사용자의 신원을 확인하는 과정이며, 인가는 인증된 사용자의 접근 권한을 결정하는 과정이다.
- 세션 기반 인증은 서버에서 세션을 관리하며, 토큰 기반 인증은 클라이언트가 토큰을 저장하고 요청 시 전송한다.
- 보안 강화를 위해 다중 인증(MFA), 비밀번호 없는 인증, 생체 인증 등의 방식이 활용된다.
- XSS, CSRF, 세션 하이재킹, 리플레이 공격 등의 위협을 방어하기 위해 입력값 검증, 보안 쿠키 설정, 토큰 서명 검
증 등의 대책이 필요하다.
- 안전한 인증 시스템을 구축하려면 HTTPS/TLS를 통한 암호화, 최소 권한 원칙 적용, 이상 징후 모니터링이 필수
적이다.

---

<!-- p.25 -->

참고 문헌
- [KISA] 소프트웨어 개발 보안 가이드(2021.12.29)
- [KISA] 소프트웨어 보안약점 진단가이드(2021)
- [오픈이지북스] 실무에 바로 적용하는 해킹 방어를 위한 JAVA 시큐어코딩
- [홍릉과학출판사] 소프트웨어 개발 보안 실무 - 시큐어 코딩 원리와 실제
- [책만] 모두를 위한 소프트웨어 보안 설계와 구현 - 취약점 분석부터 위협 모델링과 완화 전략, 보안 패턴, 암호화까지
안전한 소프트웨어의 모든 것
- [한빛미디어] 웹 해킹 & 보안 완벽 가이드 - 웹 애플리케이션 보안 취약점을 겨냥한 공격과 방어

---

<!-- p.26 -->

감사합니다.

---

<!-- p.27 -->

퀴즈
1. 다음 중 인증과 인가에 대한 설명 중 잘못된 것은?
1) 인증은 사용자에게 리소스 접근 가능한 권한을 부여하는 것 2) 인가는 권한을 제한하는 것도 포함함
3) 인증은 이 사람이 누구인가를 확인하는 과정 4) 인가를 통해 사용자를 등급별로 구분할 수 있게 됨
2. 사용자의 역할에 따라 접근 권한을 부여하는 방식을 나타내는 용어는? (영문 4글자)
( )
3. 다음중 인가 보안 위협에 대한 대응 방안은?
1) 최소권한의 원칙 2) 강력한 비밀번호 정책
3) CAPCHA 적용 4) 다중인증

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 원문 표기 그대로 — 3번 보기 3) 'CAPCHA'는 'CAPTCHA'의 오타. 2번은 빈칸 '(          )'에 답을 쓰는 주관식)

---

<!-- p.28 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
**[이미지 보충]** 정답 '1) 인증은 사용자에게 리소스 접근 가능한 권한을 부여하는 것', 'RBAC', '1) 최소권한원칙'은 빨간 글씨로 강조됨.
(※ 원문 표기 그대로 — 추출 텍스트의 '허용둰 권한'은 '허용된 권한'의 오타로 보이며, 렌더링 이미지에서는 해당 글자가 보이지 않고 '허용    권한'처럼 빈칸으로 표시됨)
