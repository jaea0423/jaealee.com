# 2025_강원대_시큐어코딩_6주차_2차시_vF

<!-- p.1 -->

SQL 인젝션 진단 및 대응
01 SQL 인젝션 개념과 발생 원리
02 SQL 인젝션 취약점 진단 및 대응

---

<!-- p.2 -->

학습 목표
SQL 인젝션 공격의 개념과 원리를 이해한다.
SQL 인젝션 공격의 다양한 기법을 학습하고 실습한다.
SQL 인젝션을 방어하기 위한 보안 기법을 적용할 수 있다.

---

<!-- p.3 -->

학습 내용
1. SQL 인젝션 개념 및 발생 원리
2. SQL 인젝션 공격 기법 이해
3. SQL 인젝션 대응 기법

---

<!-- p.4 -->

SQL 인젝션 취약점 진단 및 대응
01 SQL 인젝션 개념과 발생 원리
02 SQL 인젝션 취약점 진단 및 대응

---

<!-- p.5 -->

SQL 인젝션 개요
개요
- 웹 애플리케이션에서 입력 받아 데이터베이스로 전달하는 정상적인 쿼리(CRUD)를 변조, 삽입하여
데이터베이스에 불법적인 데이터 열람, 시스템 명령 수행 등 비정상적인 데이터 베이스에 접근하는 기법.
- 모든 종류의 DBMS에 적용 가능한 공격 기법이며, 지속적으로 발전되고 있는 공격기법.
피해 내용
- 악성 스크립트 실행, 외부 프로그램 사용가능, DB 정보 열람,추가,수정,삭제 가능
- 프로시저를 통한 운영체제 명령어 수행, 불법 로그인 등의 침해 사고가 발생 가능

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[이미지] 오른쪽 하단 일러스트: 데이터베이스(원통형 디스크) 아이콘을 향해 주사기 바늘이 꽂히려는 그림, 아래에 파란 굵은 글씨 **SQL Injection** — SQL 인젝션을 DB에 '주입(injection)'하는 공격으로 형상화.

---

<!-- p.6 -->

SQL 인젝션 개요

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[도식: SQL 인젝션 공격 흐름 — 슬라이드 전체가 이미지]

- 좌측 상단: 웹 로그인 폼 화면 캡처
  - 상단 링크: `회원가입` | `아이디/비밀번호 찾기`
  - 아이디 입력란: `WIRESHARK`
  - 비밀번호 입력란: `'a'or'1=1'`
  - [로그인] 버튼, □ 로그인 상태 유지 (체크박스)
  - 오른쪽: `IP보안 ON`(ON은 초록색 밑줄), [일회용 로그인] 버튼
- 공격자(선글라스 쓴 인물 + 노트북) 아래 검은 상자 — 공격 패턴 문자열:
  ```
  'or 1=1--
  Admin' --
  'or 1=1#
  ```
  캡션: "공격 패턴 문자열로 쿼리문 조작" (상자에서 공격자 쪽으로 위쪽 화살표)
  (※ 원문 표기 그대로 — 캡처 속 따옴표가 둥근 따옴표 ‘ ’로 표시됨. 실제 페이로드는 ASCII 작은따옴표 `'`)
- 흐름:
  - 공격자 → **① 조작된 Request** → 웹 서버
  - 웹 서버 → **② DB 쿼리 실행** → 데이터베이스
  - 웹 서버 → **③ 공격 결과** → 공격자
- 웹 서버 위 말풍선(빨간 점선 구름): "인가되지 않은 사용자가 DB 데이터를 무단 조작 하거나 삭제."
- 데이터베이스 옆 말풍선(파란 구름): "조작된 SQL 쿼리 실행"

(※ 검증: Python(sqlite3)으로 확인 — 일치) `select * from m where id='' or 1=1--' and pw='x'` → `--` 뒤가 주석 처리되어 전체 행 반환. `Admin' --` → `id='Admin' --' and pw=...` → 비밀번호 검사 생략. `'or 1=1#`는 MySQL에서 `#`이 주석이라 동일 효과(SQLite 등에서는 `#` 미지원으로 오류).
비밀번호란 값이 `a'or'1=1`(바깥 따옴표는 쿼리의 따옴표)이면 `pw='a'or'1=1'` → 문자열 `'1=1'`이 숫자 1(참)로 평가되어 전체 행 반환(SQLite로 확인, MySQL도 같은 형 변환 규칙). 입력값 자체에 바깥 따옴표까지 넣은 `'a'or'1=1'`을 그대로 결합하면 `pw=''a'or'1=1''` 구문 오류.

---

<!-- p.7 -->

SQL 인젝션 취약점 발생 원인
1. 동적 쿼리에서 사용자 입력 검증 부족
- 폼, URL 파라미터, API 요청 등 모든 외부 입력에 대해 검증 로직이 없는 경우 발생
- 입력 값 내 특수문자(' , ", ; 등)를 처리하지 않아 SQL 구문이 의도치 않게 변경됨
아래 SQL 문에서 userInput에 admin' OR '1'='1 을 삽입하면 항상 참이 되어 인증 우회됨
"SELECT * FROM users WHERE username = '" + userInput + “’;”

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
슬라이드 표시: 삽입 값 `admin' OR '1'='1`은 굵은 고정폭 글꼴, SQL 문은 테두리 상자 안 고정폭 글꼴.

(※ 검증: Python(sqlite3)으로 확인 — 일치) 최종 쿼리:
```sql
SELECT * FROM users WHERE username = 'admin' OR '1'='1';
```
→ `OR '1'='1'`이 항상 참이므로 users 전체 행 반환(테스트 DB 2행 모두 반환) → 인증 우회.
(※ 원문 표기 그대로 — 상자 끝 `“’;”`가 둥근 따옴표로 되어 있음. Java 문자열로는 `"';"`(작은따옴표+세미콜론)여야 컴파일됨.)

---

<!-- p.8 -->

SQL 인젝션 취약점 발생 원인
2. 에러 메시지 및 정보 노출
- 애플리케이션에서 내부 에러 메시지 및 데이터베이스 정보를 노출할 경우, 공격자가 이를 분석하여 추가 공격을 설계할 수 있음.
- 에러 메시지에 포함된 내용으로 다양한 정보 획득 가능
→ SQL 구문 오류, 테이블명, 컬럼 명, DB 버전 등
아래 SQL 문에서 userInput에 1' AND db_name() = 0-- 삽입하면 에러 메시지에 데이터베이스 이름이 드러남.
"SELECT * FROM users WHERE username = '" + userInput + “’;”

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
슬라이드 표시: 삽입 값 `1' AND db_name() = 0--`은 굵은 고정폭 글꼴, SQL 문은 테두리 상자 안.

최종 쿼리 (※ 검증: Python으로 문자열 생성 확인 — 일치):
```sql
SELECT * FROM users WHERE username = '1' AND db_name() = 0--';
```
→ `--` 뒤의 `';`는 주석 처리. MS-SQL에서 `db_name()`은 nvarchar(문자열)를 반환하므로 정수 0과 비교할 때 형 변환 오류(“Conversion failed when converting the nvarchar value '<DB이름>' to data type int”)가 나며, 이 오류 메시지에 현재 DB 이름이 노출됨. (MS-SQL 전용 동작이라 Python에서 실행 검증은 불가 — 원리상 내용 일치)
(※ 원문 표기 그대로 — 상자 끝 `“’;”` 둥근 따옴표, p.7과 동일)

---

<!-- p.9 -->

SQL 인젝션 취약점 발생 원인
3. 권한 및 보안 설정 미흡
- 애플리케이션에서 사용하는 DB 계정이 불필요한 권한(예: DROP, ALTER, EXECUTE 등)을 가지고 있을 경우,
공격자가 이를 악용할 수 있음.
- 취약한 저장 프로시저를 통해 시스템 명령어 실행이나 추가 권한 상승 공격이 가능.

---

<!-- p.10 -->

SQL 인젝션 취약점 공격 방식
HTML
Java
입력 예
정상 요청 : login.jsp?id=gildong&password=gdhong
공격 코드 : login.jsp?id=a' or 'a'='a&password=a' or 'a'='a
login.jsp?id=admin' -- &password=x
login.jsp?id=admin' # &password=x

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[코드 이미지 — 추출 텍스트에 없음] 파란 상자 2개를 아래 화살표로 연결(HTML 폼 → Java 처리 코드).

HTML (상자 오른쪽 위 'HTML' 표시):
```html
<form action="login.jsp">
   ID : <input type="text" name="id" />
   Password : <input type="password" name="password" />
</form>
```
↓

Java (상자 오른쪽 위 'Java' 표시):
```java
String sql = "select * from member where id = '" + request.getParameter("id") + "' "
             + "and password = '" + request.getParameter("password") + "' ";
statement.executeQuery(sql);
```
(판독 확신 낮음 — 이미지 글꼴 특성상 `getParameter[...]`, `executeQuery[sql]`처럼 대괄호로 보이나 Java 문법상 소괄호로 판독)

입력 예의 요청 URL은 굵은 고정폭 글꼴.

최종 쿼리 (※ 검증: Python(sqlite3)으로 정상·공격1·공격2 실행 — 일치):
- 정상: `select * from member where id = 'gildong' and password = 'gdhong' ` → gildong 1행
- 공격1: `select * from member where id = 'a' or 'a'='a' and password = 'a' or 'a'='a' ` → AND가 OR보다 우선 → `id='a' OR ('a'='a' AND password='a') OR 'a'='a'` → 항상 참 → 전체 행
- 공격2: `select * from member where id = 'admin' -- ' and password = 'x' ` → `--` 이후 주석, 비밀번호 검사 없이 admin 행 반환
- 공격3: `select * from member where id = 'admin' # ' and password = 'x' ` → MySQL에서 `#`은 한 줄 주석 → 공격2와 같은 효과
(참고: 실제 브라우저 URL에서 `#`은 프래그먼트 시작 문자라 서버로 전송되지 않으므로 `%23`으로, 공백은 `%20`/`+`로 인코딩해야 함. MySQL의 `-- ` 주석은 뒤에 공백이 필요.)

---

<!-- p.11 -->

Error-based SQL 인젝션 (오류 기반 SQL 인젝션)
추가 공격에 필요한 정보가 오류 메시지에 포함되어 노출될 수 있도록 입력 값을 조작
공격 방식 예시
- ' ➔ 1개의 따옴표. 인젝션 가능 여부 및 에러 메시지 내용 확인이 가능
- ' having 1 = 1 -- ➔ 오류에서 테이블명, 컬럼 명 확인이 가능
- ' and db_name() = 1 -- ➔ 현재 데이터베이스의 이름 확인이 가능
- ' and 1 = (select @@version) -- ➔ 현재 설치된 SQL Server의 시스템 및 빌드 정보 확인이 가능

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
슬라이드 표시: 공격 문자열은 굵은 고정폭 글꼴, ➔ 화살표로 오른쪽 설명과 연결. 첫 항목은 작은따옴표 하나(`'`).

(※ 검증: MS-SQL 전용 동작이라 Python 실행 검증 불가 — 원리상 내용 일치)
- `' having 1 = 1 --` : GROUP BY 없이 HAVING 사용 → “Column 'users.id' is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause.” 형태 오류에 `테이블명.컬럼명` 노출
- `' and db_name() = 1 --` : nvarchar → int 형 변환 오류 메시지에 DB 이름 노출 (p.8과 같은 원리, 비교값만 0/1 차이)
- `' and 1 = (select @@version) --` : `@@version` 문자열을 int로 변환하다 오류 → 메시지에 SQL Server 버전·빌드·OS 정보 노출

---

<!-- p.12 -->

Union-based SQL 인젝션 (유니온 기반 SQL 인젝션)
조회 결과를 출력하는 사용자 화면에, 원래 화면 출력을 위한 쿼리와 공격자가 알고자 하는 정보를 조회하는 쿼리를
조인한 결과가 출력되도록 입력 값을 조작
공격 방식 예시
- admin' union select 1,2,3,4,5,6 #
- admin' union select version(),2,3,4,5,6 #
- admin' union select schema_name,2,3,4,5,6 from information_schema.schemata #
- admin' union select group_concat(table_name),2,3,4,5,6 from information_schema.tables where
table_schema=database() #
- admin' union select group_concat(column_name),2,3,4,5,6 from information_schema.columns where
table_name='board_member' #
- admin' union select idx,userid,userpw,username,5,6 from board_member #

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
슬라이드 표시: 페이로드 전체가 굵은 고정폭 글꼴.

(※ 검증: Python으로 확인 — 일치) 각 페이로드를 `select * from board_member where userid='` + 입력 + `'`에 넣으면 `#` 앞까지 작은따옴표 짝이 맞고, 원래 쿼리 끝의 `'`는 MySQL `#` 주석으로 무시됨. 6개 예시 모두 UNION SELECT 컬럼 수가 6개로 일치(원 쿼리 컬럼 수가 6이라는 전제 — 첫 예시 `1,2,3,4,5,6`으로 컬럼 수와 화면 출력 위치 확인).
예: `select * from board_member where userid='admin' union select idx,userid,userpw,username,5,6 from board_member #'`
`version()`, `database()`, `group_concat()`, `information_schema` → MySQL 문법. 순서: 컬럼 수 확인 → DB 버전 → 스키마 목록 → 현재 DB 테이블 목록 → board_member 컬럼 목록 → 계정 데이터 추출.

---

<!-- p.13 -->

Union-based SQL 인젝션 (유니온 기반 SQL 인젝션)
주요 DBMS별 시스템 테이블

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[표 이미지 — 추출 텍스트에 없음] 주요 DBMS별 시스템 테이블 (머리글 파란 배경)

| DBMS | 테이블 | 비고 |
|---|---|---|
| MS-SQL | sysdatabases (sys.databases)<br>sysobjects (sys.objects)<br>syscolumns (sys.columns)<br>systypes (sys.types)<br>sysusers (sys.database_pricipals) | http://technet.microsoft.com/ko-kr/library/ms187997.aspx |
| Oracle | SYS.ALL_OBJECTS<br>SYS.DBA_OBJECTS<br>SYS.USER_OBJECTS<br>SYS.TABLES<br>SYS.ALL_TABLES<br>SYS.DBA_TABLES<br>SYS.USER_TABLES<br>SYS.COLUMNS | http://docs.oracle.com/cd/E21901_01/doc/timesten.1122/e21644/systemtables.htm |
| MySQL | INFORMATION_SCHEMA.SCHEMATA<br>INFORMATION_SCHEMA.TABLES<br>INFORMATION_SCHEMA.COLUMNS | https://dev.mysql.com/doc/refman/5.7/en/information-schema.html |

(※ 원문 표기 그대로 — `sys.database_pricipals`는 `sys.database_principals`의 오타)
(참고: Oracle URL은 TimesTen 11.2.2 문서의 시스템 테이블 목록이라 `SYS.TABLES`, `SYS.COLUMNS` 등은 TimesTen 기준 이름임. 일반 Oracle DB에서는 `ALL_TABLES`, `ALL_TAB_COLUMNS`, `USER_TABLES` 등을 주로 사용)

---

<!-- p.14 -->

Blind SQL 인젝션 (블라인드 SQL 인젝션)
쿼리 실행 결과에 따라 서버의 반응이 다른 것을 이용한 공격
공격자가 알고자 하는 정보의 존재 여부를 확인하기 위해
참인 조건(쿼리 실행 결과가 존재)과 거짓인 조건(쿼리 실행 결과가 없음)을 번갈아 가면서 입력되도록 입력 값을 조작
Content-based 방식과 Time-based 방식이 있음
공격방식 예시
Data' and substring(user_name(1),1,1)='a' -- // a~z까지 첫번째 글자를 비교
Data' and substring(user_name(1),2,1)='a' -- // 응답 내용의 길이를 가지고 판단
또는
Data' and substring(user_name(1),1,1)='a' waitfor delay '0:0:5' // 시간 지연을 가지고 판단.
. . . . 지속적으로 반복. 공격시간이 많이 걸리므로 툴에 의해 자동화 공격을 시도한다.

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
슬라이드 표시: 공격 예시 3줄과 마지막 줄은 고정폭 글꼴, 오른쪽에 `//` 주석.

(※ 검증: Python으로 따옴표 짝 확인 — 1·2번째 예시 일치, 3번째 예시는 불일치)
- `select * from t where c='Data' and substring(user_name(1),1,1)='a' --'` → 따옴표 짝 맞음, `--` 뒤 주석
- 3번째(Time-based) 예시는 끝에 `--`가 없어 원래 쿼리의 닫는 `'`가 남음 → `... waitfor delay '0:0:5''` 따옴표 짝 불일치(구문 오류 가능).
- 또한 MS-SQL에서 `WAITFOR DELAY`는 조건식이 아닌 별도 문장이므로 위 형태로는 조건부 지연이 되지 않음. 조건부 지연은 보통 `Data'; IF (substring(user_name(1),1,1)='a') WAITFOR DELAY '0:0:5'--` 형태로 작성.
- `user_name(1)`, `substring`, `waitfor delay` → MS-SQL 문법(`user_name(1)`은 사용자 ID 1, 보통 `dbo`).

---

<!-- p.15 -->

SQL 인젝션 공격 보안 사고 사례

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[화면 캡처 2개 — 언론 기사, 추출 텍스트에 없음]

① 왼쪽: 데일리시큐 기사 캡처
- 상단 메뉴: 이슈 | 산업 | 정책 | 해외 | IT&생활 | 자료실 | 전체기사 / 최종편집 : 2025-02-16 19:45 (일)
- 제목: **여기어때, SQL 인젝션 공격 통해 회원정보 탈취 당해**
- 길민권 기자 | 승인 2017.04.26 18:13
- 부제: 민관합동조사단, “홈페이지 취약점 공격으로 개인정보 유출 발생”
- 도식(캡션 '▲ 여기어때 해킹 과정 개요'): 공격자 ↔ [위드이노베이션: (마케팅 센터 웹서버), (서비스 관리 웹서버)] ↔ DB서버
  - ① SQL-인젝션(취약점 수집) → 마케팅 센터 웹서버 ↔ DB서버: 취약점 조회
  - ② SQL-인젝션(세션값 탈취) → 마케팅 센터 웹서버 ↔ DB서버: 세션값 조회
  - ③ 세션변조(관리자우회접속) → 서비스 관리 웹서버
  - ③ 세션변조(정보조회·유출) ← 서비스 관리 웹서버 ↔ DB서버: 개인정보 조회
  - (※ 원문 표기 그대로 — 도식에 ③이 두 번 나옴. 네 번째 단계는 ④로 보임)
- 본문 요지(저작권상 요약): 방통위·미래부가 3월 7일~17일 발생한 위드이노베이션 '여기어때' 개인정보 유출 침해사고에 대한 민관합동조사단 조사 결과를 발표. 이용고객에게 총 4,817건의 협박성 음란문자(SMS)가 발송된 사고의 원인 분석과 재발 방지를 위한 조사.

② 오른쪽: 보안뉴스(시큐리티월드) 기사 캡처
- 상단: 로그인 | 회원가입 | 기사제보 | 스크랩, 통합검색 / 메뉴: #전체기사 #시큐리티월드 #사건사고 #보안리포트 #사이버안보 #AI 보안, 뉴스레터 신청, 시큐리티 콘텐츠
- Home > 전체기사
- 제목: **한국직업능력교육원, 해킹으로 개인정보 유출... 이름, 전화번호 등 4개 항목**
- 입력 : 2024-09-10 11:39
- 본문 요지(저작권상 요약): K테크에듀는 1999년 열린직업전문학교로 설립, 시흥·안산·군포(안양)·인천 4개 지점, 교직원 80여 명. 익스플로잇랩스 대표는 해킹에 의한 유출에 완벽한 대응책이 없는 것이 근본 문제이며 이번 사고는 SQL 인젝션으로 발생한 것으로 보인다고 언급, 텔레그램 유출 데이터의 진위 파악에 관한 의견도 덧붙임.
- **빨간 박스 강조**: "SQL 인젝션을 통해 사고가 발생"

---

<!-- p.16 -->

SQL 인젝션 취약점 진단 및 대응
01 SQL 인젝션 개념과 발생 원리
02 SQL 인젝션 취약점 진단 및 대응

---

<!-- p.17 -->

SQL인젝션 취약점 진단 방법 – 코드리뷰
코드 리뷰란?
- 개발자가 작성한 소스 코드를 체계적으로 검토하여 버그 및 보안 취약점을 찾아내는 프로세스
- SQL 인젝션과 같은 취약점은 코드 리뷰를 통해 조기에 발견할 수 있음
SQL 인젝션 취약점의 주요 원인
- 동적 SQL 사용: 사용자 입력 값을 문자열로 직접 쿼리에 삽입
- 입력 값 검증 미흡: 사용자 입력에 대한 필터링 또는 이스케이핑이 부족
- 잘못된 권한 설정: 데이터베이스 접근 권한이 과도하게 부여됨
코드 리뷰의 중요성
- 보안 취약점이 제품 출시 전 단계에서 사전에 제거됨
- 팀 내 보안 인식 제고 및 모범 사례 공유
- 자동화 도구와 수동 리뷰를 병행하여 취약점 탐지율 향상

---

<!-- p.18 -->

SQL인젝션 취약점 진단 방법 – 코드리뷰
1. 동적 SQL 구문 사용 여부 점검
사용자 입력 값을 직접 쿼리 문자열에 결합하는 경우
public User findUserByUsername(String username) {
String sql = "SELECT * FROM users WHERE username = '" + username + "'";
try {
return jdbcTemplate.queryForObject(sql, new BeanPropertyRowMapper<>(User.class));
} catch (EmptyResultDataAccessException e) {
return null;
}
}
2. 입력 값 검증 및 이스케이핑 점검
- 사용자 입력 값에 대해 화이트리스트 기반의 유효성 검증 수행
- 특수문자나 위험 문자에 대한 이스케이핑 적용 여부 확인

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
슬라이드 표시: 코드가 테두리 상자 안 고정폭 글꼴, `String sql = "SELECT * FROM users WHERE username = '" + username + "'";` 줄은 굵게 강조(Spring `JdbcTemplate` 사용 코드).

(※ 검증: Python(sqlite3)으로 확인 — 일치) username에 `' OR '1'='1` 입력 시 `SELECT * FROM users WHERE username = '' OR '1'='1'` → 전체 행 반환. (참고: `queryForObject`는 결과가 2행 이상이면 `IncorrectResultSizeDataAccessException`을 던지지만, 쿼리 자체는 조작됨. 안전한 형태는 `jdbcTemplate.queryForObject("SELECT * FROM users WHERE username = ?", new BeanPropertyRowMapper<>(User.class), username)`처럼 `?` 바인딩)

---

<!-- p.19 -->

SQL인젝션 취약점 진단 방법 – 자동화된 진단 도구 활용
정적 분석 도구
소스 코드를 분석하여 보안 취약점(예: 동적 SQL, 입력값 처리 미흡 등)을 자동으로 탐지
예) SonarQube, Checkmarx, Fortify
동적 분석 도구
실행 중인 애플리케이션에 대해 실제 공격 시나리오(예: OWASP ZAP)를 적용해 취약점 검증
예) OWASP ZAP
자동화 도구의 필요성
- 광범위한 코드 검증: 수동 리뷰만으로는 놓치기 쉬운 취약점을 체계적으로 탐지
- 반복적 검사: CI/CD 파이프라인에 통합하여 코드 변경 시마다 자동 점검
SQL 인젝션 취약점 탐지 역할
- 사용자 입력과 동적 SQL 구문 조합을 자동으로 스캔하여 위험 패턴을 식별
- 취약한 코드 패턴(예: 문자열 결합으로 SQL 생성)을 보고서로 제공

---

<!-- p.20 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용

### 취약성을 가지는 쿼리구조 - 동적 쿼리

[흐름도 — 위에서 아래로 화살표]

1. `String id=request.getParameter(“id”);`
2. ↓ `String sql=“select * from tbl where id=“+id;` (주황색 강조 상자)
3. ↓ JDBC API Statement 명령어 생성
4. ↓ 쿼리 실행

(2번 상자를 가리키는 말풍선)
외부 입력 값이 삽입된 뒤,
쿼리 명령문이 만들어지는 구조이므로,
외부 입력 값에 따라 쿼리명령문이 수정될 수 있음.

(※ 원문 표기 그대로 — 둥근 따옴표 “ ” 사용. 실제 Java 코드라면 `String sql = "select * from tbl where id=" + id;`)
(※ 검증: Python(sqlite3)으로 확인 — 일치) id가 따옴표 없이 결합되므로(숫자형 컬럼 가정) id에 `1 or 1=1` 입력 시 `select * from tbl where id=1 or 1=1` → 전체 행 반환.

---

<!-- p.21 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용

### 취약성을 가지지 않는 쿼리구조 - 동적 쿼리

(※ 원문 표기 그대로 — 안전한 구조인데도 소제목이 '동적 쿼리'로 되어 있음. 내용상 파라미터화(정적 구조) 쿼리에 해당)

[흐름도 — 위에서 아래로 화살표]

1. `String id=request.getParameter(“id”);`
2. ↓ JDBC API PreparedStatement 명령어 생성
   `prepareStatement(“select * from tbl where id=?”);`
3. ↓ `setString(1,id)` (회색 강조 상자)
4. ↓ 쿼리 실행

(2~3번 사이를 가리키는 말풍선)
쿼리명령문이 만들어지고 난 다음, 외부입력
값이 자료형에 맞게 삽입되어
외부입력값에 의해 명령어 구조가 변경되지
않음

(※ 원문 표기 그대로 — 둥근 따옴표 “ ” 사용)
(※ 검증: Python(sqlite3)으로 확인 — 일치) 같은 입력 `1 or 1=1`을 `?`에 바인딩하면 하나의 값으로만 취급되어 0행 반환(쿼리 구조 불변).

---

<!-- p.22 -->

SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
Statement 방식 DB Query
안전하지 않은 코드
String query = "SELECT * FROM users WHERE userid ='"+ userid + "'" +
“AND password='" + password + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
안전한 코드
String query = "SELECT * FROM users WHERE userid=? AND password=?”;
PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, userid);
stmt.setString(2, password);
ResultSet rs = stmt.executeQuery();
PreparedStatement 의 setXXX()메소드로 외부 입력 데이터를 쿼리문에 설정하여 쿼리 구조가 변조되는 것을 방지한다.

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
슬라이드 구성: 자물쇠 아이콘 + 'Statement 방식 DB Query' 제목, 빨간 리본 라벨 '안전하지 않은 코드' 아래 회색 코드 상자(변수 `userid`, `password`가 **빨간색** 강조), 파란 리본 라벨 '안전한 코드' 아래 회색 코드 상자, 맨 아래 설명 문장. (이 페이지의 삽입 이미지는 자물쇠 아이콘·리본 라벨 배경·제목/상자 그림자뿐이며 별도 글자 없음)

(※ 검증: Python(sqlite3)으로 확인 — 일치)
- 정상: `SELECT * FROM users WHERE userid ='kim'AND password='pw2'` → 1행 (`'`와 `AND` 사이 공백이 없어도 SQL 파싱은 정상)
- userid=`admin' --` → `SELECT * FROM users WHERE userid ='admin' --'AND password='x'` → 비밀번호 검사 없이 admin 행 반환
- 같은 값을 PreparedStatement `?`에 바인딩 → 0행
(※ 원문 표기 그대로 — `“AND password='"`, `password=?”;`에 둥근 따옴표 “ ”가 섞여 있어 그대로는 컴파일되지 않음. 또 `"'"` 다음 `"AND`에 공백이 없음)

---

<!-- p.23 -->

SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용
Hibernate Query Language 방식
안전하지 않은 코드
List results = session.createQuery(
"from Orders as orders where orders.id = " + currentOrder.getId()).list();
안전한 코드
Query hqlQuery = session.createQuery("from Orders as orders where orders.id = ?0");
List results = hqlQuery.setString(0, "123-456-7890").list();

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
슬라이드 구성: 자물쇠 아이콘 + 'Hibernate Query Language 방식', 빨간 리본 '안전하지 않은 코드' / 파란 리본 '안전한 코드' 아래 회색 코드 상자. 안전하지 않은 코드에서 `orders.id = " + currentOrder.getId()).list();` 부분이 **빨간색** 강조. (삽입 이미지는 아이콘·리본·그림자뿐, 별도 글자 없음)

참고: `?0`은 JPA 스타일 위치(ordinal) 파라미터로 `setString(0, ...)`이 0번 자리에 값을 바인딩함(Hibernate 5.3+는 기존 `?` 레거시 파라미터 대신 `?0`, `?1` 형태 사용). `setString`은 Hibernate 5.2부터 deprecated, 6에서 제거되어 현재는 `setParameter(0, ...)` 사용. "123-456-7890"은 예시 값. (도구/라이브러리 지식 기반 — Python 검증 대상 아님)

---

<!-- p.24 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용

### 🔒 MyBatis 방식

**[안전하지 않은 코드]** (빨간 리본 라벨)
```xml
<select id="getPerson" parameterType=“String" resultType="org.application.vo.Person">
        SELECT * FROM PERSON WHERE NAME LIKE '${name}'
</select>
```

**[안전한 코드]** (파란 리본 라벨)
```xml
<select id="getPerson" parameterType=“String" resultType="org.application.vo.Person">
        SELECT * FROM PERSON WHERE NAME = #{name}
</select>
```

(※ 숨은 텍스트 — PDF 추출 텍스트에는 "Hibernate Query Language에 외부 입력값을 바인드 방식으로 처리하여 쿼리문이 변조 되지 않도록 한다." 문장이 안전한 코드 상자 위치에 들어 있으나, 회색 코드 상자에 가려 슬라이드 화면에는 보이지 않음. MyBatis 페이지인데 'Hibernate Query Language'로 적혀 있어 앞 슬라이드에서 복사된 잔재로 보임)
(※ 원문 표기 그대로 — `parameterType=“String"`의 여는 따옴표가 둥근 따옴표)

설명: `${name}`은 값을 SQL 문자열에 그대로 치환(문자열 결합)하고, `#{name}`은 PreparedStatement의 `?` 바인딩으로 처리됨.
(※ 검증: Python(sqlite3)으로 확인 — 일치) name에 `' OR '1'='1` 입력 시 `${}` 치환 결과 `SELECT * FROM PERSON WHERE NAME LIKE '' OR '1'='1'` → 전체 행 반환, `#{}`(바인딩) 방식은 0행.
(참고: 안전한 코드는 `LIKE`를 `=`로 바꿨으므로 부분 검색이 필요하면 MySQL 기준 `NAME LIKE CONCAT('%', #{name}, '%')`처럼 바인딩을 유지해야 함)

---

<!-- p.25 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용

### 🔒 Java Persistence API 방식

**[안전하지 않은 코드]** (빨간 리본 라벨)
```java
List results = entityManager.createQuery
   ("Select order from Orders order where order.id = " + orderId).getResultList();
```

**[안전한 코드]** (파란 리본 라벨)
```java
Query jpqlQuery =
    entityManager.createQuery("Select order from Orders order where order.id= ?1");
List results = jpqlQuery.setParameter(1, "123-456-7890").getResultList();
```

(※ 숨은 텍스트 — PDF 추출 텍스트에는 "Hibernate Query Language에 외부 입력값을 바인드 방식으로 처리하여 쿼리문이 변조 되지 않도록 한다." 문장이 안전한 코드 상자 안(두 코드 줄 사이 위치)에 들어 있으나, 회색 코드 상자에 가려 슬라이드 화면에는 보이지 않음. JPA 페이지인데 'Hibernate Query Language'로 적혀 있어 p.23에서 복사된 잔재로 보임)

설명: `?1`은 JPQL 위치 파라미터, `setParameter(1, ...)`로 1번 자리에 값을 바인딩 → orderId 문자열 결합 대신 바인딩으로 쿼리 구조 변조 방지. (JPA 문법 지식 기반 — Python 검증 대상 아님)

---

<!-- p.26 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## SQL인젝션 취약점 대응 방법 – 시큐어코딩 적용

### 🔒 입력 값 필터링으로 안전한 값을 쿼리문에 사용

동적 쿼리 구조를 사용하여야 하는 경우, 외부 입력 값에 대해 철저한 필터링을 수행한 뒤 쿼리문에 사용하도록 한다.

**전달되는 파라미터에 필터링 되어야 하는 특수 문자들** (좌우 2개 표)

| 일반 | URL Encoding | HTML Encoding |
|---|---|---|
| `'` | `%27` | `&#x27;` `&apos;` |
| `"` | `%22` | `&#x22;` `&quot;` |
| `:` | `%3a` | `&#x3a;` |
| `;` | `%3b` | `&#x3b;` |
| `(` | `%28` | `&#x28;` |
| `)` | `%29` | `&#x29;` |
| `<` | `%3c` | `&#x3c;` `&lt;` |
| `>` | `%3e` | `&#x3e;` `&gt;` |
| `[` | `%5b` | `&#x5b;` |
| `]` | `%5d` | `&#x5d;` |
| `{` | `%7b` | `&#x7b;` |
| `}` | `%7d` | `&#x7d;` |

| 일반 | URL Encoding | HTML Encoding |
|---|---|---|
| `` ` `` | `%60` | `&#x60;` |
| `=` | `%3d` | `&#x3d;` |
| `#` | `%23` | `&#x23;` |
| `$` | `%24` | `&#x24;` |
| `%` | `%25` | `&#x25;` |
| `&` | `%26` | `&#x26;` `&amp;` |
| `?` | `%3f` | `&#x3f;` |
| `!` | `%21` | `&#x21;` |
| `@` | `%40` | `&#x40;` |
| `*` | `%2a` | `&#x2a;` |
| 탭문자 | `%09` | `&#x09;` |
| `\|` | `%7c` | `&#x7c;` |

(※ 검증: Python으로 확인 — 일치) 24개 문자 모두 URL 인코딩 `%XX` = 문자 코드(16진수), HTML 16진 엔티티 `&#xXX;`와 명명 엔티티(`&apos;`, `&quot;`, `&lt;`, `&gt;`, `&amp;`)가 `html.unescape`로 원래 문자로 복원됨.

---

<!-- p.27 -->

SQL인젝션 취약점 대응 방법 – 입력 값 검증
SQLMap을 활용한 검증 테스트
자동화된 SQL인젝션 테스트 도구 SQLMap을 활용하여, 구현된 입력값 검증이 제대로 작동하는지 테스트
검증 테스트 예시
sqlmap -u "http://example.com/search?keyword=test" --risk=3 --level=5 --batch
- u: 타겟 URL 지정 (GET 파라미터 포함)
- -batch: 모든 질문에 자동으로 기본값 사용
- -risk [1-3]: 위험 수준 설정 (높을수록 다양한 페이로드 시도)
- -level [1-5]: 테스트 강도 조정 (높을수록 검사하는 파라미터와 페이로드가 많아짐)
- -dump: 데이터베이스 내용을 덤프 (테스트 목적 시에만 사용, 운영 환경에서는 주의해야 함)
테스트 결과 판단
- "Parameter: keyword (GET) appears to be 'safe’” 출력 시 성공적으로 방어되었음
- SQL인젝션 관련 취약점 경고가 출력되면, 입력 값 검증 로직을 보완해야 함

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[이미지] 오른쪽 하단: sqlmap 로고 — 검은 배경에 노란색 ASCII 아트 'sqlmap' 글자, 가운데 빨간 세로 막대(주사기 모양)와 `H`, `[,]`, `[']`, `[)]`, `V...` 기호. 명령 예시는 테두리 상자 안 고정폭 글꼴.

참고(도구 지식 기반, Python 검증 대상 아님): 명령의 `--risk=3 --level=5`는 설명의 `--risk [1-3]`, `--level [1-5]`와 같은 옵션(`=`/공백 모두 허용)이며 최댓값 조합이라 가장 많은 페이로드를 시도(시간이 오래 걸리고, risk 3은 OR 기반 페이로드로 데이터 변경 위험이 있음). `--dump`는 예시 명령에는 포함되지 않음.
(※ 원문 표기 그대로 — 결과 문구 끝 따옴표가 `'safe’”`로 혼용)
(참고: sqlmap은 주입 불가 시 보통 "all tested parameters do not appear to be injectable" 형태로 출력하고, "Parameter: keyword (GET)" 머리글은 주입 가능 지점을 찾았을 때 표시됨 — 슬라이드 문구는 실제 출력 문구와 다를 수 있음)

---

<!-- p.28 -->

SQL인젝션 취약점 대응 방법 – 보안 로그 기록 및 모니터링
로그 기록 및 모니터링의 필요성
조기 탐지
- SQL 인젝션 공격은 종종 비정상적인 쿼리 패턴이나 오류 로그를 남김
- 실시간 모니터링을 통해 공격 징후를 빠르게 파악 가능
사후 분석
- 공격 발생 시 로그를 통해 원인 분석 및 대응 전략 수립
- 법적 대응 및 보안 감사 자료로 활용 쿼리 파라미터: 숫자, 날짜, 식별자 등 쿼리에서 사용되는 모든 값
로그 기록 대상
- 웹 애플리케이션 요청 로그 (입력 값, URL, IP 등)
- 데이터베이스 에러 로그 (SQL 문법 오류, 타입 변환 오류 등)
- 인증/인가 관련 이벤트 (로그인 실패, 권한 상승 시도 등)

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
(※ 원문 표기 그대로 — '사후 분석'의 두 번째 항목 "법적 대응 및 보안 감사 자료로 활용" 뒤에 "쿼리 파라미터: 숫자, 날짜, 식별자 등 쿼리에서 사용되는 모든 값"이 같은 줄에 붙어 있음. 문맥상 다른 슬라이드에서 남은 문구로 보임)

---

<!-- p.29 -->

SQL인젝션 취약점 대응 방법 – 보안 로그 기록 및 모니터링
로그 기록시 고려사항
- 쿼리 파라미터 및 입력값
사용자 입력값, 특히 특수문자나 SQL 예약어 포함 여부 기록
- 에러 및 예외 처리 로그
SQL 실행 오류, 구문 오류, 타입 변환 오류 등 상세 에러 메시지 기록
- 사용자 및 요청 정보
요청한 IP, timestamp, User Agent 등 공격 추적에 유용한 정보 기록
민감 정보(예: 비밀번호, 개인정보)는 로그에 기록하지 않도록 주의
모니터링 도구 및 기술
- SIEM(보안정보 및 이벤트 관리) 시스템
Splunk, ELK Stack (Elasticsearch, Logstash, Kibana), Graylog 등을 활용하여 로그 집계 및 실시간 분석
- 알림 및 자동 대응
- 특정 패턴(예: SQL 구문 오류, 이상한 파라미터 값) 감지 시 관리자에게 알림 발송
- 일정 기준 초과 시 자동으로 방어 조치(예: IP 차단) 수행

---

<!-- p.30 -->

요약 정리
- SQL 인젝션은 입력 값을 제대로 검증하지 않아 DB 쿼리가 조작될 수 있는 취약점입니다.
- 공격 방식에는 에러 메시지를 활용하는 Error-based, 여러 쿼리를 결합하는 Union-based, 응답을
통해 간접적으로 추론하는 Blind 방식 등이 있습니다.
- 이 취약점은 대규모 개인정보 유출이나 시스템 명령어 실행 등 심각한 보안 사고로 이어질 수 있습니다.
- PreparedStatement 같은 안전한 쿼리 작성, 입력 값 검증, 자동화 진단 도구 활용, 로깅·모니터링을
통해 대응하여야 합니다.
- 코드 리뷰와 사고 사례 학습을 통해 지속적으로 취약점을 점검하고, CI/CD 파이프라인에서 보안 검증
을 강화해야 합니다.

---

<!-- p.31 -->

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

<!-- p.32 -->

감사합니다.

---

<!-- p.33 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 퀴즈

(좌상단 'Quiz' 돋보기 아이콘)

**1. 다음 중 SQL 인젝션을 예방하기 위한 방법으로 옳지 않은 것은 무엇일까요?**
- 1) PreparedStatement(또는 파라미터 바인딩)를 사용한다.
- 2) 사용자 입력값을 길이·형식·특수문자 등에 대해 검증한다.
- 3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.
- 4) 데이터베이스 에러 메시지를 사용자에게 그대로 노출하지 않는다.

**2. 다음 중 SQL 인젝션 공격으로 인해 발생할 수 있는 피해가 아닌 것은 무엇일까요?**
- 1) 데이터베이스에서 민감 정보가 유출된다.
- 2) 관리자 계정으로 인증을 우회할 수 있다.
- 3) 서버의 파일이 삭제되거나 변경될 수 있다.
- 4) 네트워크 장비가 물리적으로 파손된다.

**3. SQL 인젝션 방어를 위해 Java에서 동적 SQL 대신 권장되는 JDBC API 클래스 이름은?**

(                    )

---

<!-- p.34 -->

퀴즈 정답
1. 다음 중 SQL 인젝션을 예방하기 위한 방법으로 옳지 않은 것은 무엇일까요?
3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.
문자열 결합을 통해 쿼리를 직접 작성하면 인젝션 위험이 커집니다.
2. 다음 중 SQL 인젝션 공격으로 인해 발생할 수 있는 피해가 아닌 것은 무엇일까요?
4) 네트워크 장비가 물리적으로 파손된다.
SQL 인젝션은 주로 DB 및 서버 내부 데이터 조작에 영향을 미치며, 물리적 장비 파손은 직접적인 영향 범위가 아닙니다.
3. SQL 인젝션 방어를 위해 Java에서 동적 SQL 대신 권장되는 JDBC API 클래스 이름은?
( PreparedStatement )

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
슬라이드 표시: 정답 줄('3) 개발자가 만든 쿼리를 문자열 결합으로 직접 작성한다.', '4) 네트워크 장비가 물리적으로 파손된다.', 'PreparedStatement')은 **빨간색**, 해설은 검은색. 좌상단 'Quiz' 돋보기 아이콘.
