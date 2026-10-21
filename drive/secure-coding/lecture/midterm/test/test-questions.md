# 테스트 문제 10개 (정답·난이도 표시 없음 — AI에 보내는 용도)

1. 3주차 실습 환경에서 Burp Suite 프록시 리스너(Bind to port)와 Firefox의 HTTP 프록시에 설정한 포트 번호는?
1) 8000
2) 8080
3) 8081
4) 8082

2. 정규식에서 \b 가 의미하는 것은?
1) 공백 문자
2) 단어 경계(Word Boundary)
3) 줄의 시작
4) 백스페이스 문자

3. 5주차 JWT 실습에서 검증 요청(/jwt/verify)에 잘못된 토큰을 보내면 서버가 반환하는 HTTP 상태 코드는?
1) 200
2) 400
3) 401
4) 403

4. DREAD로 평가한 어떤 위협의 항목 점수가 Damage 5, Reproducibility 10, Exploitability 10, Affected Users 8, Discoverability 10이다. (가) 2주차 2차시 교안의 총점 기준표로 판정한 위협 수준과 (나) 2주차 3차시 실습의 평균 기준으로 판정한 등급을 각각 쓰시오.
(　　　　)

5. MyBatis 동적 SQL에서 <where> 태그 안에 <if> 두 개가 있고 각각 "AND name = #{name}", "AND email = #{email}" 조건을 가진다. name만 전달되고 email이 null일 때 실제로 만들어지는 WHERE 절은?
1) WHERE AND name = ?
2) WHERE name = ?
3) WHERE name = ? AND email = NULL
4) WHERE 절이 만들어지지 않는다

6. 어떤 페이지의 자바스크립트가 URL의 # 뒤(fragment) 값을 읽어 그대로 innerHTML에 넣는다. 서버가 보낸 HTML에는 공격 스크립트가 포함되지 않는다. 이 취약점은 XSS의 어느 유형인가?
1) Reflected XSS
2) Stored XSS
3) DOM 기반 XSS
4) Blind XSS

7. JWT 헤더의 alg 값을 none으로 바꿔 서명 검증을 건너뛰게 하는 공격을 막기 위한 서버 측 조치로 가장 적절한 것은?
1) 토큰 만료 시간을 짧게 둔다
2) 서버가 허용할 서명 알고리즘을 고정하고 none을 거부한다
3) 토큰을 localStorage 대신 쿠키에 저장한다
4) 페이로드를 Base64 대신 Hex로 인코딩한다

8. 다른 사이트가 내 페이지를 투명한 iframe으로 띄워 사용자의 클릭을 가로채는 공격(클릭재킹)을 막는 HTTP 응답 헤더는?
1) X-Content-Type-Options
2) X-Frame-Options
3) Strict-Transport-Security
4) Set-Cookie

9. 비밀번호를 저장할 때 SHA-256을 한 번 적용하는 것보다 bcrypt·Argon2 같은 비밀번호 전용 해시 함수가 권장되는 이유를 두 가지 쓰시오.
(　　　　)

10. 비밀번호 재설정 링크에 넣는 일회용 토큰을 만들 때 피해야 할 방식은?
1) SecureRandom 같은 암호학적 난수 사용
2) 시간·순번처럼 예측 가능한 값 사용
3) 충분히 긴 길이로 생성
4) 1회 사용 후 폐기

