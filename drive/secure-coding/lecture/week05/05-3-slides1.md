# 2025_강원대_시큐어코딩_5주차_3차시_vF

<!-- p.1 -->

JWT 인증 및 인가
01 JWT 이해
02 JWT 구현
03 JWT 보안 및 취약점 대응

---

<!-- p.2 -->

학습 목표
JWT 개념과 필요성을 이해하고 설명할 수 있다.
JWT 기반 인증 흐름을 이해하고, 구현할 수 있다.
JWT 보안 위협을 이해하고 이에 대한 해결 방안을 설명할 수 있다.

---

<!-- p.3 -->

학습 내용
1. JWT 개념
2. JWT 구현
3. JWT 보안 위협 및 해결방법

---

<!-- p.4 -->

JWT 인증 및 인가
01 JWT 이해
02 JWT 구현
03 JWT 보안 및 취약점 대응

---

<!-- p.5 -->

JWT(JSON Web Token) 이란?
- JWT란?
JSON Web Token은 JSON 형식의 데이터를 안전하게 전송하기 위한 개방 표준(RFC 7519)입니다.
주로 인증(Authentication)과 인가(Authorization)에 사용되며, 클라이언트-서버 간 정보를 교환하는 용도로 활용됩니다.
- 주요 특징
- 자체 포함(Self-contained): 토큰 내에 사용자 정보, 만료 시간 등의 정보를 포함하여 별도 저장소 없이 인증 가능
- 경량(Compact): URL, 헤더, 쿠키 등 다양한 환경에서 전송하기 적합한 크기
- 서명(Signature): 토큰의 위변조 여부를 확인하기 위해 HMAC, RSA, ECDSA 등의 알고리즘으로 서명

---

<!-- p.6 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.7 -->

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

<!-- p.8 -->

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

<!-- p.9 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## JWT 기반 인증 흐름

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

<!-- p.10 -->

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

<!-- p.11 -->

JWT 기반 인증 흐름
- JWT를 활용한 사용자 인가 및 권한 관리 사용시 고려사항
- 동적 권한 관리의 한계 및 보완
사용자 권한 변경 시, 기존 JWT에 반영되지 않으므로 주기적 토큰 갱신 또는 별도 인가 체크 필요
중앙 인가 서버와의 연계를 통해 실시간 권한 업데이트 구현 고려
- 보안 강화
HTTPS를 통한 안전한 전송, HttpOnly/ Secure 쿠키 등 안전한 저장소 활용
최소한의 정보만 포함하고, 민감 정보는 별도 암호화 또는 안전한 관리

---

<!-- p.12 -->

JWT 인증 및 인가
01 JWT 이해
02 JWT 구현
03 JWT 보안 및 취약점 대응

---

<!-- p.13 -->

JWT 구현 실습
- hello-spring-boot 프로젝트에 기능 추가하여 실습
Spring Boot 기본 사용법 설명에서 실습하였던 프로젝트 활용
Java 17 / Maven 환경
- 실습 내용
- Access Token과 Refresh Token의 생성
- Access Token의 검증
- Refresh Token을 이용하여 새로운 Access Token과 Refresh Token 재발급

---

<!-- p.14 -->

프로젝트 환경 설정
- pom.xml 의 Dependency 목록에 JWT 라이브러리(JJWT)를 추가함
- jjwt-api : 관련 API 정의
- jjwt-impl : 실제 API 동작 구현
- jjwt-Jackson : Jackson 라이브러리 연동으로 JSON 처리

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.15 -->

JWT 컨트롤러 소스코드 (1/4)
- 상수값 설정
- secretKey : HS256 암호화 비밀 키
- ACCESS_TOKEN_EXPIRATION : 10분
- REFRESH_TOKEN_EXPIRATION : 30분
JwtController.java

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.16 -->

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

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.17 -->

JWT 컨트롤러 소스코드 (3/4)
- 엔드포인트 구현
/jwt/verify : Access Token 유효성 검증
JwtController.java

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.18 -->

JWT 컨트롤러 소스코드 (4/4)
- 엔드포인트 구현
/jwt/refresh : Refresh Token이 유효할 경우 새로운 Access Token과 Refresh Token을 발급
이전 Refresh Token 재사용을 방지하려면 서버 측에서 DB나 캐시를 활용해야 함
JwtController.java

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.19 -->

구현된 JWT 기능 테스트 (1/3)
- Access Token 발급 시험
실제 환경에서는 사용자 인증 성공한 사용자에 대해서만 처리되어야 함
웹 브라우저에서 http://localhost:8080/jwt/generate 입력
JSON 형식으로 accessToken, refreshToken 값이 반환됨
파이어폭스 브라우저의 경우 결과 화면에서 '원시값 보기' 선택

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.20 -->

구현된 JWT 기능 테스트 (2/3)
- Access Token 유효 확인 시험
Access Token의 유효성 및 클레임 내용 확인
웹 브라우저에서 http://localhost:8080/jwt/verify?token=액세스토큰값 입력
토큰이 유효할 경우 JSON 형식으로 토큰 안에 들어있는 클레임 정보 반환됨
잘못된 토큰일 경우 HTTP 400 응답으로 에러 메시지가 반환됨
< 토큰이 유효할 경우 >
< 잘못된 토큰일 경우 >

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.21 -->

구현된 JWT 기능 테스트 (3/3)
- Refresh Token 으로 Access Token 및 Refresh Token 회전 시험
Refresh Token의 유효성 확인 후 재발급 처리
웹 브라우저에서 http://localhost:8080/jwt/refresh?refreshToken=리프레시토큰값 입력
토큰이 유효할 경우 JSON 형식으로 새로운 Access Token과 Refresh Token이 반환됨
잘못된 토큰일 경우 HTTP 400 응답으로 에러 메시지가 반환됨
< 토큰이 유효할 경우 >
< 잘못된 토큰일 경우 >

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
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

<!-- p.22 -->

JWT 인증 및 인가
01 JWT 이해
02 JWT 구현
03 JWT 보안 및 취약점 대응

---

<!-- p.23 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## JWT 보안 및 취약점 대응 – 서명과 키 관리

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

<!-- p.24 -->

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

<!-- p.25 -->

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

<!-- p.26 -->

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

<!-- p.27 -->

요약 정리
- JWT는 인증과 인가를 위한 강력한 도구지만, 서명 검증, 유효기간 관리, 키 보호가 필수적.
- JWT는 암호화되지 않으므로 민감한 데이터를 직접 포함하면 안 됨.
- Refresh Token을 활용한 인증 유지 전략을 적용하고, 토큰 탈취 방지를 위한 XSS 방어 및 안전한 저
장소 사용이 중요.

---

<!-- p.28 -->

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

<!-- p.29 -->

감사합니다.

---

<!-- p.30 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 퀴즈

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

<!-- p.31 -->

퀴즈 정답
1. JWT의 주요 특징에 해당하지 않는 것은?
4) 헤더-페이로드-트레일러 로 구성
JWT는 헤더-페이로드-서명 으로 구성되어 있는 토큰 형식입니다.
2. JWT의 단점 중 틀린 것은?
1) 만료 시간 전 강제 무효화를 위한 관리자 페이지 필요
JWT는 기본적으로, 만료 기간 전에 강제로 만료할 수 있는 방법이 없습니다.
3. JWT 페이로드에 포함시키는 사용자 식별자, 역할, 권한 등의 정보를 일컫는 단어는?
( 클레임 또는 claim )
