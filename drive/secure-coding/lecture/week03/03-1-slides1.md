# 2025_강원대_시큐어코딩_3주차_1차시_vF (1)

<!-- p.1 -->

실습환경 구축-1
01 실습환경 구축
02 웹과 HTTP 구조 이해
03 데이터 인코딩

---

<!-- p.2 -->

학습 목표
보안 실습 환경의 구조를 이해하고, 로컬에 구축한다.
웹의 구조와 HTTP 통신 방식을 이해한다.
BASE64와 URL 인코딩 및 디코딩 개념을 이해한다.

---

<!-- p.3 -->

학습 내용
1. LAB 프로젝트 웹 서비스 구동 방법
2. 웹 서버와 애플리케이션 서버, 데이터베이스 간의 구조 및 요청 흐름 이해
3. HTTP 메시지 구조와 요청 메서드, 응답 코드의 역할
4. BASE64, URL 인코딩 및 디코딩 개념 이해

---

<!-- p.4 -->

실습환경 구축-1
01 실습환경 구축
02 웹과 HTTP 구조 이해
03 데이터 인코딩

---

<!-- p.5 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
실습환경 아키텍처 이해

[도식: 실습 PC (MS Windows, 192.168.0.10) 안에서의 구성]

```
 ┌─────────────────────┐  ◄── HTTP Request ───  ┌─────────────────┐  ◄── HTTP Request ───  ┌──────────────┐
 │   시큐어코딩랩       │                          │ Local Proxy     │                          │    사용자     │
 │   SpringBoot        │  ─── HTTP Response ──►  │ Server          │  ─── HTTP Response ──►  │ Web Browser  │
 │   + DB (MariaDB)    │                          │ BurpSuite       │                          │              │
 └─────────────────────┘                          └─────────────────┘                          └──────────────┘
   웹 서비스 포트                                    프록시 서비스 포트
   192.168.0.10:8000                                127.0.0.1:8081
        ▲
        └┄┄┄┄┄┄┄┄┄┄┄ (점선) HTTP Request / HTTP Response — 프록시를 거치지 않는 직접 연결 ┄┄┄┄┄┄┄┄┄┄┄┘
```

| 연결 방식 | 설정 | 설명 |
| --- | --- | --- |
| **1. 웹 서비스 직접 연결** (점선) | 브라우저에 `192.168.0.10:8000` 또는 `127.0.0.1:8000` 입력 | 사용자는 웹 브라우저에서 직접 웹 서비스 포트에 접속하여 웹 서비스 사용 가능 |
| **2. Local Proxy 설정** (주황 실선) | 브라우저 Proxy 서버 설정에 `127.0.0.1:8081` 설정 후 `192.168.0.10:8000` 접속 | BurpSuite로 동작시킨 후, 웹 브라우저에 해당 프록시 서버를 등록하면, 모든 HTTP 요청과 응답을 프록시를 통해 주고받을 수 있음 |

---

<!-- p.6 -->

실습환경 구축 – 웹 서비스 서버 설정 (1/8)
Step1. 배포된 LAB 파일 압축 해제
SecureCoding2025.zip 파일을 C:\에 압축 해제
정상적으로 압축을 해제하면 아래 화면과 같이 폴더와 LAB 파일들이 생성됨

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[탐색기 캡처: 내 PC > 로컬 디스크 (C:) > SecureCoding2025]

| 이름 | 유형 |
| --- | --- |
| download | 파일 폴더 |
| JNDI-Exploit-Kit | 파일 폴더 |
| logs | 파일 폴더 |
| sts4 | 파일 폴더 |
| webgoat | 파일 폴더 |
| workspace | 파일 폴더 |
| README.md | MD 파일 (0KB) |
| set_env.txt | TXT 파일 (1KB) |
| start_lab.bat | Windows 배치 파일 (1KB) |

---

<!-- p.7 -->

실습환경 구축 – 웹 서비스 서버 설정 (2/8)
Step2. 환경변수 설정
〮 시스템 변수 3가지 추가
내PC > 오른쪽 버튼 클릭 > 속성 > 고급 시스템 설정 > 환경변수 로 들어가서 하단 ‘시스템 변수’ 창에서 ‘새로 만들기’ 선택
JAVA_HOME C:\SecureCoding2025\download\jdk-15.0.2\
MAVEN_HOME C:\SecureCoding2025\download\apache-maven-3.8.1\
MYSQL_HOME C:\SecureCoding2025\download\mariadb-10.5.10-winx64\
〮 시스템 변수 Path에 3가지 경로를 제일 앞에 추가
‘시스템 변수’에서 Path 환경변수 선택 > 편집 > 새로 만들기 선택 후 제일 위에 추가
%JAVA_HOME%\bin\
%MAVEN_HOME%\bin\
%MYSQL_HOME%\bin\
〮 환경변수가 정상적으로 반영되었는지 확인
찾기 > cmd 실행하여 커맨드 창에서 정상적으로 버전이 출력되는지 확인
> java –version
> mvn –version
> mysql --version

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[명령 프롬프트 캡처: 세 명령의 정상 출력 예]

```
C:\Users\...>java -version
java version "15.0.2" 2021-01-19
Java(TM) SE Runtime Environment (build 15.0.2+7-27)
Java HotSpot(TM) 64-Bit Server VM (build 15.0.2+7-27, mixed mode, sharing)

C:\Users\...>mvn -version
Apache Maven 3.8.1 (05c21c65bdfed0f71a2f2ada8b84da59348c4c5d)
Maven home: C:\SecureCoding2025\download\apache-maven-3.8.1\bin\..
Java version: 15.0.2, vendor: Oracle Corporation, runtime: C:\SecureCoding2025\download\jdk-15.0.2
Default locale: ko_KR, platform encoding: MS949
OS name: "windows 10", version: "10.0", arch: "amd64", family: "windows"

C:\Users\...>mysql --version
mysql  Ver 15.1 Distrib 10.5.10-MariaDB, for Win64 (AMD64), source revision 3f55c569...
```

---

<!-- p.8 -->

실습환경 구축 – 웹 서비스 서버 설정 (3/8)
Step3. 사용하고 있는 포트 확인
〮 시스템에 이미 사용하고 있는 포트가 있는지 확인
cmd 창에서 아래 명령어를 입력하여, 실습에 사용할 포트를 이미 점유한 프로세스가 있는지 확인
3306, 8000, 8100, 8200, 8080, 8081
> netstat –ano | more
〮 만약 LISTENING으로 보이는 포트가 있다면, 해당하는 프로세스를 찾아 종료
표시된 PID값으로 ‘작업 관리자’ 에서 어떤 프로세스인지 확인 가능

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[명령 프롬프트 캡처: `netstat -ano | more` 결과 — 프로토콜 / 로컬 주소 / 외부 주소 / 상태 / PID 열로 TCP 0.0.0.0:80, :135, :445, :843 … :7680 등이 LISTENING 상태로 나열됨]

※ 실습 포트 **3306, 8000, 8100, 8200, 8080, 8081**(빨간 글씨)이 목록에 LISTENING으로 있으면 그 PID의 프로세스를 종료

---

<!-- p.9 -->

실습환경 구축 – 웹 서비스 서버 설정 (4/8)
Step4. start_lab.bat 실행
〮 LAB 실습에 사용할 데이터베이스(MariaDB)와 웹 서비스 개발환경(Spring Tool Suite 4) 실행
cmd 창에서 C:\SecureCoding2025로 이동하여 준비되어 있는 시작 배치 파일 실행
C:\SecureCoding2025> start_lab
〮 DB 정상 구동 확인
cmd 창에 나타난 로그 내용으로 정상 여부 확인됨
정상: [Note] mysqld.exe: ready for connections.
cmd 창은 최소화시켜놓기만 하고, 종료시키지 말 것
〮 Spring Tool Suite 4 정상 구동 확인
좌측 Project Explorer 영역에 SecureCoding 폴더가 보이면 정상

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[캡처 2장]
- **start_lab 명령 프롬프트**: MariaDB InnoDB 초기화 로그가 이어지다가 `[Note] mysqld.exe: ready for connections.` 가 출력됨 (정상 구동)
- **Spring Tool Suite 4 창**: 왼쪽 Package Explorer에 `SecureCoding` 프로젝트가 보임 (정상 구동)

※ 빨간 글씨 강조: **cmd 창은 최소화시켜놓기만 하고, 종료시키지 말 것**

---

<!-- p.10 -->

실습환경 구축 – 웹 서비스 서버 설정 (5/8)
Step5. Update Project 실행
〮 SecureCoding 프로젝트의 의존성과 설정을 최신 상태로 동기화
프로젝트명에서 마우스 오른쪽 클릭 > Maven > Update Project 선택
Update Maven 창에서 OK 선택
〮 IDE의 우측 하단 진행 상황 확인
모든 업데이트가 완료되면 진행 상황이 사라짐

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[캡처 3장 — 빨간 상자로 클릭 위치 표시]
1. STS4에서 프로젝트 우클릭 메뉴 > **Maven** > **Update Project…** (단축키 Alt+F5)
2. 'Update Maven Project' 창: Available Maven Codebases에 `SecureCoding` 체크 → **OK**
3. 오른쪽 아래 진행 표시줄 `Updating Maven Project: (48%)` — 사라지면 완료

---

<!-- p.11 -->

실습환경 구축 – 웹 서비스 서버 설정 (6/8)
Step6. Run As > Spring Boot App 실행
〮 프로젝트의 업데이트가 모두 완료되면 서버 실행
프로젝트명에서 마우스 오른쪽 클릭 > Run As > Spring boot App 선택
Select Java Application에서 SecureCodingLabTestApplication 확인 후 OK 선택
〮 IDE의 우측 하단 진행 상황 확인
아래와 같이 콘솔창에 Tomcat started on port(s): 8000 이 보이면 정상

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[캡처 3장 — 빨간 상자로 클릭 위치 표시]
1. 프로젝트 우클릭 메뉴 > **Run As** > **Spring Boot App** (Alt+Shift+X, B)
2. 'Select Java Application' 창: Matching items 중 **SecureCodingLabTestApplication - kr.co.openeg.lab** 선택 → **OK** (다른 후보: BuildExploit, EncodingMaker)
3. Console 로그 중 검은 상자로 강조된 줄: `TomcatWebServer:220 - Tomcat started on port(s): 8000 (http) with context path ''` → 정상 실행

---

<!-- p.12 -->

실습환경 구축 – 웹 서비스 서버 설정 (7/8)
Step7. 다음과 같은 경고가 발생하였을 때 대처 방법
〮 콘솔 윈도우의 버퍼 크기를 늘려줘야 함
Window > Preferences > Run/Debug > Console을 선택하여
Console buffer size(characters)를 1,000,000으로 수정한 후,
‘Apply and Close’ 버튼 클릭

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[경고창 캡처: Ansi Console — **CONSOLE PERFORMANCE WARNING** (from Ansi Console)!]

> Console buffer size too low (80,000). About 2 times slower.
> Main menu → Window → Preferences → Run/Debug → Console
> • Check "Limit console output"
> • Set "Console buffer size (characters)" to a bigger value. The sweet spot seems to be about 1,000,000
> or
> • Uncheck "Limit console output" — No visible performance difference compared to 1,000,000
> [Remind me later] [Never remind me again]

[Preferences 창 캡처: 왼쪽 트리에서 **Run/Debug > Console** 선택(빨간 상자), 오른쪽 'Limit console output' 체크 상태에서 **Console buffer size (characters): 1000000** 입력(빨간 상자) → Apply and Close]

---

<!-- p.13 -->

실습환경 구축 – 웹 서비스 서버 설정 (8/8)
Step8. 웹 브라우저를 띄워 정상 동작 확인
크롬이나 파이어폭스를 실행시켜 LAB 웹 서비스에 접속
주소창에 localhost:8000 를 입력하면 아래와 같은 화면이 나타나고, 로그인 가능함
ID: test
PW: qqq111
입력하여 로그인

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[브라우저 캡처 2장 — 화살표로 이어짐]
1. **로그인 화면** (`localhost:8000/login`, 탭 제목 '시큐어코딩랩 - 홈'): 상단 '(주)오픈이지 — 안전한 소프트웨어를 만들기 위한 노력', 메뉴 [메인 / 게시판 / 시큐어코딩 테스트 / DB 초기화], 가운데 일러스트, 아래 아이디·비밀번호 입력칸과 [로그인] 버튼, '아직 회원이 아니신가요? 회원가입'. 빨간 글씨: **ID: test / PW: qqq111 입력하여 로그인**
2. **로그인 후 메인 화면** (`localhost:8000/board/main`): 오른쪽 위 '[test 님] 로그아웃 정보수정', 소프트웨어 보안 소개 문단과 『해킹 방어를 위한 JAVA 시큐어코딩』 책 표지, 하단 'Copyright © (주)오픈이지 2021-2025'

---

<!-- p.14 -->

실습환경 구축 – 프록시 설정(1/4)
Step1. BurpSuite 패키지 실행
〮 BurpSuiteCommunity.exe 를 실행하면 별도 설치 없이 바로 구동됨
C:\SecureCoding2025\download\BurpSuiteCommunity 폴더에 있음
〮 Terms and Conditions 에서 ‘I Accept’ 버튼 선택

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[캡처 2장]
1. 탐색기 `C:\SecureCoding2025\download\BurpSuiteCommunity` 폴더: .install4j, burpbrowser, jre, burpsuite_community.jar, **BurpSuiteCommunity.exe**(빨간 상자), BurpSuiteCommunity.vmoptions, uninstall.exe
2. 'Burp Suite Community Edition — Terms and Conditions' 창: 약관 본문 아래 [I Decline] [**I Accept**](빨간 상자)

---

<!-- p.15 -->

실습환경 구축 – 프록시 설정(2/4)
Step2. BurpSuite 패키지 실행 옵션 선택
Temporary project 선택 후 ‘Next’ 버튼 선택
Use Burp defaults 선택 후 ‘Start Burp’ 버튼 선택

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[Burp Suite Community Edition v2021.10 시작 창 2단계]
1. 프로젝트 선택: **Temporary project**(빨간 상자) / New project on disk / Open existing project (※ Disk-based projects are only supported on Burp Suite Professional) → [Next]
2. 설정 선택: **Use Burp defaults**(빨간 상자) / Use options saved with project / Load from configuration file → [**Start Burp**](빨간 상자)

---

<!-- p.16 -->

실습환경 구축 – 프록시 설정(3/4)
Step3. 프록시 서버의 인터페이스 설정 수정
〮 상단 메뉴에서 Proxy > Options 선택
Proxy Listener 목록에서 127.0.0.1:8080 인터페이스 체크 및 선택
해당 인터페이스가 주황색으로 표시됨
〮 좌측 Edit 버튼 클릭

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite 화면 캡처 — 빨간 상자·화살표로 순서 표시]

상단 탭 **Proxy** → 하위 탭 **Options** → 'Proxy Listeners' 표:

| Running | Interface | Invisible | Redirect | Certificate |
| --- | --- | --- | --- | --- |
| ☑ | **127.0.0.1:8080** (주황색으로 선택됨) | | | Per-host |

→ 왼쪽 [Add] [**Edit**] [Remove] 중 Edit 클릭

---

<!-- p.17 -->

실습환경 구축 – 프록시 설정(4/4)
Step4. 프록시 서버의 Bind Port 수정
Edit proxy listener 창에서 ‘Bind to port’ 항목을 8081로 변경
OK 버튼 선택

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
['Edit proxy listener' 창 캡처 — Binding 탭]
- **Bind to port: 8081**(빨간 상자, 기존 8080에서 변경)
- Bind to address: ◉ Loopback only / ○ All interfaces / ○ Specific address: 127.0.0.1
- → [**OK**](빨간 상자)

---

<!-- p.18 -->

실습환경 구축 – 파이어폭스 브라우저 설정(1/3)
Step1. 우측 상단 세줄 메뉴 버튼 클릭
아래 항목에서 ‘설정’ 항목 선택
나타난 ‘일반’ 화면 맨 아래로 내려가서
‘네트워크 설정’의 ‘설정’ 버튼 선택

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[파이어폭스 캡처 2장]
1. 오른쪽 위 **≡ 메뉴**(빨간 상자) → 메뉴 목록(새 탭, 새 창, 새 사생활 보호 창, 북마크, 기록, 다운로드, 비밀번호, 부가 기능 및 테마, 인쇄, … 확대/축소) 중 **설정**(빨간 상자)
2. 설정 '일반' 화면 맨 아래 **네트워크 설정** — "Firefox가 인터넷에 접근하는 방법을 설정하세요." 옆 [**설정…(E)**](빨간 상자)

---

<!-- p.19 -->

실습환경 구축 – 파이어폭스 브라우저 설정(2/3)
Step2. 연결 설정에서 수동 프록시 서버 정보 입력
수동 프록시 설정 선택
HTTP 프록시에 127.0.0.1, 포트에 8081 입력
확인 버튼 선택

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[파이어폭스 '연결 설정' 창 캡처]
- 인터넷 프록시 접근 설정: ○ 프록시 사용 안 함 / ○ 프록시 설정 자동 감지 / ○ 시스템 프록시 설정 사용 / ◉ **수동 프록시 설정**(빨간 상자)
- **HTTP 프록시: 127.0.0.1**(빨간 상자) / **포트: 8081**(빨간 상자)
- □ HTTPS에도 이 프록시를 사용 (체크 안 함), HTTPS 프록시·SOCKS 호스트는 비움
- 안내 문구: "localhost, 127.0.0.1/8 및 ::1에 대한 연결은 프록시가 사용되지 않습니다." ← 다음 단계(3/3)에서 이 제한을 푸는 이유
- → [**확인**](빨간 상자)

---

<!-- p.20 -->

실습환경 구축 – 파이어폭스 브라우저 설정(3/3)
Step3. localhost 에서 프록시 설정 가능하도록 옵션 변경
〮 주소창에 ‘about:config’ 입력
〮 경고 메시지에서 ‘위험을 감수하고 계속’ 버튼 선택
〮 ‘설정 이름 검색’ 창에 ‘network.proxy.allow_hijacking_localhost’를 입력
〮 해당 설정 우측 좌우 화살표 버튼을 눌러 값을 ‘true’로 변경

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[파이어폭스 캡처 2장]
1. `about:config` 경고 화면: '주의해서 사용하세요 — 고급 설정을 변경하면 Firefox의 성능 또는 보안에 영향을 줄 수 있습니다.' → [**위험을 감수하고 계속**](빨간 상자)
2. 설정 검색창에 `network.proxy.allow_hijacking_localhost` 입력(빨간 상자) → 결과 행 값이 **true**, 오른쪽 ⇄(토글) 버튼을 빨간 화살표로 가리킴

---

<!-- p.21 -->

실습환경 구축 – BurpSuite 프록시 서버 동작
이후 해당 웹 브라우저 사용시 발생하는 모든 HTTP 요청은 BurpSuite가 가로 챔
웹 브라우저에서 LAB 웹 서비스 주소를 입력해도 일단 BurpSuite가 붙잡고 있어서 화면이 나오지 않음
Intercept 메뉴에서 ‘Intercept is on’ 버튼을 눌러 off 시키면, 대기하던 모든 내용이 전달되어 화면이 나타남
붙잡혀있는
HTTP 요청

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite 캡처: Proxy > **Intercept** 탭(빨간 상자), 'Request to http://localhost:8000 [127.0.0.1]', 버튼 [Forward] [Drop] [**Intercept is on**](빨간 상자) [Action] [Open Browser]]

빨간 글씨 '붙잡혀있는 HTTP 요청'이 가리키는 Raw 내용:

```http
GET /login HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Fi…
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Cookie: JSESSIONID=EC82962C430C2679DF183C7AC123763A
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

---

<!-- p.22 -->

실습환경 구축-1
01 실습환경 구축
02 웹과 HTTP 구조 이해
03 데이터 인코딩

---

<!-- p.23 -->

웹 구조
단순화된 구조 확장 표현된 구조
출처: 위키피디아 출처: https://medium.com/@iyuroch/application-architecture-plan-layers-68defde66ade

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[도식 2개 — 화살표로 이어짐]

**단순화된 구조** (출처: 위키피디아)
```
 Users                     Calling Services
   ↕                              ┆ (점선)
 Presentation Layer               ┆
 Business Layer  ◄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘
 Data Layer
   ↕            ↕
 Data Sources   Services
```

**확장 표현된 구조** (출처: https://medium.com/@iyuroch/application-architecture-plan-layers-68defde66ade)

| 계층 | 구성 요소 |
| --- | --- |
| (외부) | Users, Clients |
| **Presentation Layer** | UI Components, UI Process Components (← Users) / Service Interface (← Clients) |
| **Business Layer** | Application Facade, Business Components, Business Workflows, Business Entities(세로로 여러 계층에 걸침) |
| **Data Layer** | Data Access Logic Components, Data Helper / Utilities, Service Agents |
| (외부) | Data Sources, Services |
| **Cross-Cutting** (전 계층 공통, 오른쪽 세로 막대) | Security, Operational Management, Communication |

(퀴즈 1번의 '웹 애플리케이션 서버 로직 3대 계층' = Presentation / Business / Data)

---

<!-- p.24 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
웹 서비스 흐름

[도식: Web Browser → DNS Server → Web Server → WAS → Database, 번호 순서대로]

| 순서 | 구간 | 동작 |
| --- | --- | --- |
| ① | Web Browser → DNS Server | `http://www.웹서버URL.com` 요청 |
| ② | DNS Server → Web Browser | 123.123.123.123을 응답 (IP 주소) |
| ③ | Web Browser → Web Server | 123.123.123.123으로 index.html 요청 |
| ④ | Web Server → WAS | 요청 중계 |
| ⑤ | WAS ↔ Database | DB 조회 (Connector: JDBC, ODBC) |
| ⑥ | WAS → Web Server | 응답 중계 |
| ⑦ | Web Server → Web Browser | index.html 응답 (html, css, javascript, …) |

| 구성 요소 | 예시 제품 |
| --- | --- |
| Web Browser | Chrome, FireFox, Internet Explorer |
| Web Server | Apache, nginx, webtob |
| Web Application Server (WAS) — 안에 Business Logic 여러 개 | tomcat, WebLogic, JBoss, jeus |
| Database | Oracle, MySQL, MSSQL |

---

<!-- p.25 -->

HTTP 구조
HTTP (HyperText Transfer Protocol)
〮 WWW 상에서 HTML 문서와 같은 리소스들을 가져올 수 있도록 해주는 프로토콜
〮 요청(Request), 응답(Response) 구조, 무상태 방식(Stateless)

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[도식 2개]

**왼쪽 — 웹 문서 하나를 여러 요청으로 가져오는 모습**: Web document 안의 요소마다 별도 GET 요청이 The Internet을 거쳐 각 서버로 감
- `GET layout.css`, `GET image.png`, `GET page.html` → **Web server**
- `GET video.mp4` → **Video server**
- `GET ads.jpg` → **Ads server**

**오른쪽 — 웹 기술 계층도 ('The Web' 범위)**

```
┌──────┬──────┬──────────┐
│      │      │ Web APIs │
│ HTML │ CSS  ├──────────┤
│      │      │JavaScript│
├──────┴──────┴──────────┤
│         HTTP           │  ← 빨간 글씨
├──────┬─────────┬───────┤
│ DNS  │         │  TLS  │
├──────┤   TCP   ├───────┤
│ UDP  │                 │
├──────┴─────────────────┤
│          IP            │
└────────────────────────┘
```

---

<!-- p.26 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
HTTP 구조 — HTTP 흐름 이해

[도식: 웹 브라우저(왼쪽)와 웹 서버(오른쪽)의 HTTP·TCP·IP 계층 사이에 번호 순서대로 주고받는 흐름]

| 번호 | 위치 | 내용 |
| --- | --- | --- |
| 1 | 서버 HTTP 부모 프로세스 → TCP | 연결대기 |
| 2 | 브라우저 HTTP → TCP | 연결요청 |
| 3 | 브라우저 → 서버 | **SYN** |
| 4 | 서버 → 브라우저 | **SYN/ACK** |
| 5 | 브라우저 → 서버 | **ACK** (여기까지 3-way handshake = TCP 연결설정) |
| 6 | 브라우저 TCP → HTTP | 연결확인 |
| 7 | 서버 TCP → HTTP 부모 프로세스 | 연결승락 |
| 8 | 서버 | HTTP 부모 프로세스가 **HTTP 자식 프로세스 생성** |
| 9 | 브라우저 HTTP → TCP | HTTP요청 |
| 10 | 브라우저 → 서버 | **DATA (Request)** |
| 11 | 서버 → 브라우저 | ACK |
| 12 | 서버 TCP → 자식 프로세스 | HTTP요청 |
| 13 | 자식 프로세스 ↔ 저장소 | 웹 페이지 |
| 14 | 자식 프로세스 → TCP | HTTP응답 |
| 15 | 서버 → 브라우저 | **DATA (Response)** |
| 16 | 브라우저 → 서버 | ACK |
| 17 | 브라우저 TCP → HTTP | HTTP응답 |
| 18 | 브라우저 → 서버 | **FIN** |
| 19 | 서버 → 브라우저 | ACK |
| 20 | 서버 → 브라우저 | **FIN** |
| 21 | 브라우저 → 서버 | ACK (여기까지 4-way handshake = TCP 연결해제) |

(TCP 박스 안 구간 표시: 연결설정 → 데이터 전송 → 연결해제)

---

<!-- p.27 -->

BurpSuite을 활용한 HTTP 구조 보기
〮 수동 웹 프록시로 BurpSuite를 경유하도록 설정한 경우
Proxy > HTTP history 에서 HTTP
Request/Response 내용 조회 가능
Request
Response
내용
내용

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite 캡처: Proxy > **HTTP history**(빨간 상자)]

| # | Host | Method | URL | Status | Length | MIME type |
| --- | --- | --- | --- | --- | --- | --- |
| 197 | http://localhost:8000 | GET | /board/main | 200 | 3589 | HTML (주황색 선택) |
| 202 | http://detectportal.firefox.com | GET | /canonical.html | 200 | 317 | XML |
| 203 | http://detectportal.firefox.com | GET | /success.txt?ipv4 | 200 | 235 | text |
| 204 | http://detectportal.firefox.com | GET | /success.txt?ipv6 | 200 | 235 | text |

아래 왼쪽 빨간 상자 = **Request 내용**, 가운데 빨간 상자 = **Response 내용** (각각 다음 두 슬라이드에 확대), 오른쪽 INSPECTOR 패널(Request Attributes, Request Cookies (1), Request Headers (10), Response Headers (13))

---

<!-- p.28 -->

HTTP Request 메시지 구조

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite Request 탭 Raw 캡처]

```http
GET /board/main HTTP/1.1
Host: localhost:8000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://localhost:8000/login
Connection: close
Cookie: JSESSIONID=C84105A85AC5C292FEE00982DB9EA846
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

(1행 = 요청 라인: 메서드·경로·버전 / 2~11행 = 헤더 / 빈 줄 뒤 = 바디(GET이라 비어 있음))

---

<!-- p.29 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
HTTP Request Method

| Method | 설명 |
| --- | --- |
| **GET** | 자원 요청(default값), 요청 파라메터를 URL에 붙여서 전송<br>보안이 요구되지 않은 짧은 데이터를 전송하는 경우, 북마크가 필요한 경우에 사용<br>예: `test.jsp?id=kim&pass=1234` |
| **POST** | 자원 요청, 요청 파라메터를 Body에 붙여서 전송<br>전송할 데이터가 양이 많은 경우, 비밀 정보를 전송해야 하는 경우에 사용<br>예: `<form method="post"></form>` |
| **HEAD** | HTTP Header 정보만 요청<br>Meta 정보 획득이나 Hyper Text의 링크 유효성을 검사하는 용도로 사용 |
| **PUT** | URL 자원을 생성하도록 요청. 파일을 업로드 할 수 있다. |
| **DELETE** | URL 자원을 삭제하도록 요청. 파일을 삭제할 수 있다. |
| **TRACE** | 진단을 위한 목적으로 사용되는 메서드로, 서버는 응답 바디에 요청 받은 자료와 똑같은 내용을 보냄 |
| **OPTIONS** | 응답 가능한 HTTP Method를 요청 |

---

<!-- p.30 -->

HTTP Response 메시지 구조

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite Response 탭 Raw 캡처]

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
Date: Sun, 16 Feb 2025 05:15:10 GMT
Connection: close
Content-Length: 3182

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>□□□□□□ - □□</title>
  <!-- universal -->
```

(1행 = 상태 라인: 버전·상태코드 / 2~14행 = 헤더 / 빈 줄 뒤 = HTML 바디. title의 한글은 캡처에서 깨져 □로 보임)

---

<!-- p.31 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
HTTP Response Status Code

| 상태코드 | 설명 |
| --- | --- |
| 1xx | 정보를 제공함 |
| 2xx | 요청이 성공적으로 이루어짐 |
| 3xx | 요청한 해당 자원이 다른 곳에 있음 |
| 4xx | 요청에 문제가 있음 |
| 5xx | 서버에 에러가 있음 |

| 코드 | 설명 |
| --- | --- |
| 100(계속) | 요청자는 요청을 계속해야 한다. 서버는 이 코드를 제공하여 요청의 첫 번째 부분을 받았으며 나머지를 기다리고 있음 |
| 101(프로토콜 전환) | 요청자가 서버에 프로토콜 전환을 요청했으며 서버는 이를 승인하는 중. |
| 200(성공) | 서버가 요청을 정상적으로 처리함. |
| 201(작성됨) | 성공적으로 요청되었으며 서버가 새 리소스를 작성 |
| 202(허용됨) | 서버가 요청을 접수했지만 아직 처리하지 않음 |
| 203(신뢰할 수 없는 정보) | 서버가 요청을 성공적으로 처리했지만 다른 소스에서 수신된 정보를 제공 |
| 204(콘텐츠 없음) | 서버가 요청을 성공적으로 처리했지만 콘텐츠를 제공하지 않음 |
| 205(콘텐츠 재설정) | 서버가 요청을 성공적으로 처리했지만 콘텐츠를 표시하지 않음. 204 응답과 달리 이 응답은 요청자가 문서 보기를 재설정할 것을 요구(예: 새 입력을 위한 양식 비우기). |
| 206(일부 콘텐츠) | 서버가 GET 요청의 일부만 성공적으로 처리함 |

---

<!-- p.32 -->

HTTP Response Status Code
300(복수 응답) 서버가 요청에 따라 여러 조치를 선택. 수행할 작업을 선택하거나, 요청자가 선택할 수 있는 작업 목록을 제공.
301(영구 이동) 요청한 페이지가 새 위치로 영구적으로 이동했음.
302(임시 이동) 현재 서버가 다른 위치의 페이지로 요청에 응답하고 있지만, 요청자는 향후 요청 시 원래 위치를 계속 사용해야 함.
303(기타 위치 보기) HEAD 요청 이외의 모든 요청을 다른 위치로 자동으로 전달
304(수정되지 않음) 마지막 요청 이후 요청한 페이지는 수정되지 않았음.
305(프록시 사용) 요청자는 프록시를 사용하여 요청한 페이지만 접근할 수 있음.
307(임시 리다이렉션) 현재 서버가 다른 위치의 페이지로 요청에 응답하고 있지만, 요청자는 향후 요청시 원래 위치를 계속 사용해야 함.
308(영구 리다이렉션) RFC에서 실험적으로 승인됨
400(잘못된 요청) 서버가 요청의 구문을 인식하지 못함
401(권한 없음) 이 요청은 인증이 필요함. 서버는 로그인이 필요한 페이지에 대해 이 요청을 제공할 수 있음.
402(결제 필요) 이 요청은 결제가 필요함
403(Forbidden, 금지됨) 서버가 요청을 거부함. 예를 들어, 사용자가 리소스에 대한 필요 권한을 갖고 있지 않다.
(401은 인증 실패, 403은 인가 실패라고 볼 수 있음)
404(Not Found, 찾을 수 없음) 서버가 요청한 페이지(Resource)를 찾을 수 없음
405(허용되지 않는 방법) 요청에 지정된 방법을 사용할 수 없음 ex)POST 방식으로 요청을 받는 서버에 GET 요청을 보내는 경우,
또는 읽기 전용 리소스에 PUT 요청을 보내는 경우
406(허용되지 않음) 요청한 페이지가 요청한 콘텐츠 특성으로 응답할 수 없음
407(프록시 인증 필요) 이 상태 코드는 401(권한 없음)과 비슷하지만 요청자가 프록시를 사용하여 인증해야 함.
408(요청 시간초과) 서버의 요청 대기가 시간을 초과함
409(충돌) 서버가 요청을 수행하는 중에 충돌이 발생함.
서버는 PUT 요청과 충돌하는 PUT 요청에 대한 응답으로 이 코드를 요청 간 차이점 목록과 함께 표시

---

<!-- p.33 -->

HTTP Response Status Code
410(사라짐) 요청한 리소스가 영구적으로 삭제되었을 때 이 응답을 표시
411(길이 필요) 서버는 유효한 콘텐츠 길이 헤더 입력란 없이는 요청을 수락하지 않음
412(사전조건 실패) 서버가 요청자가 요청 시 부과한 사전조건을 만족하지 않음
413(요청 속성이 너무 큼) 요청이 너무 커서 서버가 처리할 수 없음
414(요청 URI가 너무 김) 요청 URI(일반적으로 URL)가 너무 길어 서버가 처리할 수 없음
415(지원되지 않는 미디어 유형) 요청이 요청한 페이지에서 지원하지 않는 형식으로 되어 있음
416(처리할 수 없는 요청범위) 요청이 페이지에서 처리할 수 없는 범위에 해당되는 경우 서버는 이 상태 코드를 표시
417(예상 실패) 서버는 Expect 요청 헤더 입력란의 요구사항을 만족할 수 없음
500(내부 서버 오류) 서버에 오류가 발생하여 요청을 수행할 수 없음
501(구현되지 않음) 서버에 요청을 수행할 수 있는 기능이 없음. ex)서버가 요청 메소드를 인식하지 못할 때 이 코드를 표시
502 (Bad Gateway, 불량 게이트웨이) 서버가 게이트웨이나 프록시 역할을 하고 있거나 또는 업스트림 서버에서 잘못된 응답을 받음
503(서비스를 사용할 수 없음) 서버가 오버로드되었거나 유지관리를 위해 다운되었기 때문에 현재 서버를 사용할 수 없음
504(게이트웨이 시간초과) 서버가 게이트웨이나 프록시 역할을 하고 있거나 또는 업스트림 서버에서 제때 요청을 받지 못함
505(HTTP 버전이 지원되지 않음) 서버가 요청에 사용된 HTTP 프로토콜 버전을 지원하지 않음
506(Variant Also Negotiates, RFC 2295)
507(용량 부족, WebDAV; RFC 4918)
508(루프 감지됨, WebDAV; RFC 5842)
509(대역폭 제한 초과, Apache bw/limited extension)
510(확장되지 않음, RFC 2774)
511(네트워크 인증 필요, RFC 6585)

---

<!-- p.34 -->

실습환경 구축-1
01 실습환경 구축
02 웹과 HTTP 구조 이해
03 데이터 인코딩

---

<!-- p.35 -->

데이터 인코딩 개요
데이터를 특정 규칙에 따라 다른 형식으로 변환하는 과정
인코딩이 필요한 이유
〮 데이터 전송: 다양한 환경에서 데이터가 올바르게 해석되도록 보장
〮 보안 강화: 입력 값을 안전하게 처리하여 XSS, HTML 인젝션 등 보안 취약점 예방
〮 호환성: 서로 다른 시스템 간에 데이터 포맷의 차이로 인한 오류 방지
인코딩 vs 암호화
〮 인코딩은 데이터를 다른 형태로 변환해도, 누구나 역 변환(디코딩) 가능
〮 암호화는 보안 목적으로 데이터를 변환하며, 복호화를 위해 키가 필요
주요 인코딩 유형
〮 BASE64 인코딩
〮 URL 인코딩

---

<!-- p.36 -->

03 데이터 인코딩
BASE64 인코딩
이진 데이터를 텍스트 형식으로 변환하는 인코딩 방식
특징
〮 데이터를 6비트 단위로 분할하여, 총 64개의 문자 집합(A-Z, a-z, 0-9, +, /)으로 표현
〮 6비트씩 처리하므로 부족한 비트는 0으로 패딩 처리되며, =로 표현
BASE64를 사용하는 이유
〮 이메일, JSON, XML 등 텍스트 전송 환경에서 안전하게 사용 가능
〮 네트워크나 시스템간 전송 시 발생할 수 있는 데이터 손상 및 인코딩 문제를 방지
인코딩 사례
Hello, World! SGVsbG8sIFdvcmxkIQ==

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[인코딩 사례 도식] `Hello, World!` → (BASE64) → `SGVsbG8sIFdvcmxkIQ==`  (끝의 `==`가 패딩)

---

<!-- p.37 -->

URL 인코딩
URL에서 사용이 불가능한 문자를 안전하게 표현하기 위해, 특정 문자를 % 기호와 ASCII 16진수 코드로 변환하는 방식
- URL 에서 사용할 수 없는 문자 처리
URL에서는 공백, ?, &, #, /, : 등의 문자들이 특별한 의미를 가짐
ex) https://example.com/search?query=hello world ➔ https://example.com/search?query=hello%20world
- 비 ASCII 문자(한글, 일본어 등) 처리
URL은 ASCII 문자 집합(영어, 숫자, 일부특수문자)만 허용
ex) 한글 ➔ %ED%95%9C%EA%B8%80
- 보안 및 일관성 유지
웹서버와 클라이언트 간 통신에서 일부 문자(<, >, “ 등)는 보안 문제를 유발할 수 있어 인코딩을 통해 안전하게 전송
ex) <script>alert(1);<script> ➔ %3Cscript%3Ealert%281%29%3B%3Cscript%3E

---

<!-- p.38 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
URL 인코딩이 필요한 문자 목록

**인코딩이 필요한 문자**

| 문자유형 | 예 | 인코딩된 값 |
| --- | --- | --- |
| 공백 | (공백) | `%20` |
| 예약문자(URL구조에서 사용) | `?` `&` `#` `/` `:` | `%3F` `%26` `%23` `%2F` `%3A` |
| 특수문자 | `!` `@` `$` `+` `=` | `%21` `%40` `%24` `%2B` `%3D` |
| 비ASCII 문자(한글, 특수기호..) | `한` `日` | `%ED%95%9C` `%E6%97%A5` |

**안전한 문자(인코딩 불필요)**
- 영문 대/소문자
- 숫자
- 일부 특수문자 (`-` `_` `.` `~`)

---

<!-- p.39 -->

BurpSuite를 통해 BASE64 디코딩
1. 파이어폭스 주소창에 주소 입력
파이어폭스 주소창에 아래 주소 입력
http://httpbin.org/basic-auth/user/passwd
화면상에 로그인 창이 나타남
BurpSuite Proxy에서 [Intercept is off] 버튼을 눌러
[Intercept is on] 으로 전환
사용자 이름 및 암호에 아무 값이나 입력한 후 [확인] 버튼

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[캡처: 파이어폭스(위)와 BurpSuite(아래)]
- 파이어폭스 주소창 `httpbin.org/basic-auth/user/passwd` → 'http://httpbin.org — 이 사이트에서 로그인을 요청합니다.' 팝업: 사용자 이름 `usertest`, 비밀번호 `••••••••` 입력 후 [로그인] (빨간 화살표)
- BurpSuite Proxy > Intercept 탭에서 **Intercept is on** 버튼(빨간 화살표) — 'Requests sent by Burp's browser will be held here so that you can analyze and modify them before forwarding them to the target server.'

---

<!-- p.40 -->

BurpSuite를 통해 BASE64 디코딩
2. BurpSuite Intercept 화면에 Request 내용이 보임
HTTP Request의 Header 내용 중 Authorization 내용에
BASE64 인코딩된 내용이 들어있음

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite Intercept 캡처 — Request to http://httpbin.org:80 [44.217.196.51]]

```http
GET /basic-auth/user/passwd HTTP/1.1
Host: httpbin.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Priority: u=0, i
Authorization: Basic dXNlcnRlc3Q6cGFzc3Rlc3Q=      ← 빨간 상자·화살표
```

---

<!-- p.41 -->

BurpSuite를 통해 BASE64 디코딩
3. 해당 BASE64 인코딩 내용 선택하여 디코딩
BASE64 인코딩된 문자열을 더블클릭하면 우측에 Base64
디코딩된 내용을 볼 수 있음
해당 문자열을 CTRL-C (Copy) 함

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite 캡처: 10행 `Authorization: Basic dXNlcnRlc3Q6cGFzc3Rlc3Q=` 의 값을 더블클릭해 주황색으로 선택(빨간 화살표)]

오른쪽 **Inspector** 패널:
- Selection: 23 (0x17)
- Selected text: `dXNlcnRlc3Q6cGFzc3Rlc3Q`
- **Decoded from: Base64** → `usertest:passtest` (빨간 상자)

→ Basic 인증 헤더는 암호화가 아니라 **인코딩**이라 `아이디:비밀번호`가 그대로 드러남

---

<!-- p.42 -->

BurpSuite를 통해 BASE64 디코딩
4. Decode 메뉴에서 디코딩
복사한 BASE64문자열을 입력창에 붙여 넣고 우측 'Decode as …' 에서 Base64 선택
하단에 디코딩된 문자열이 출력됨

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite **Decoder** 탭 캡처 2장]
1. 입력창에 `dXNlcnRlc3Q6cGFzc3Rlc3Q` 붙여넣기 → 오른쪽 'Decode as …' 목록(Plain, URL, HTML, **Base64**(빨간 상자), ASCII hex, Hex, Octal, Binary, Gzip)에서 Base64 선택
2. 아래 결과창에 디코딩된 문자열 출력 (캡처에는 `usertest:passtec3Q`로 보임)

※ 캡처 결과가 앞 쪽 Inspector의 `usertest:passtest`와 다르게 보이는데, 복사할 때 끝의 패딩 `=`가 빠지는 등 입력 문자열 차이로 보입니다. 올바른 디코딩 결과는 `usertest:passtest`입니다.

---

<!-- p.43 -->

BurpSuite를 통해 URL인코딩/디코딩
1. 입력창에 사이트 주소 붙여 넣고 인코딩
앞서 접속했던 사이트 주소를 입력창에 넣고 'Encode as …' 선택
종류 중 'URL' 선택
하단에 인코딩된 문자열이 출력됨

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite **Decoder** 캡처]
- 입력창: `http://httpbin.org/basic-auth/user/passwd`
- 'Encode as …' 목록(Plain, **URL**(빨간 화살표), HTML, Base64, ASCII hex, Hex, Octal, Binary, Gzip)에서 URL 선택
- 결과(빨간 상자): `%68%74%74%70%3a%2f%2f%68%74%74%70%62%69%6e%2e…` — 영문자까지 **모든 글자를 %16진수로** 바꾼 형태 (BurpSuite의 URL 인코딩은 전체 문자를 인코딩함)

---

<!-- p.44 -->

BurpSuite를 통해 URL인코딩/디코딩
2. 인코딩 된 문자열로 다시 URL 디코딩
앞서 접속했던 사이트 주소를 입력창에 넣고 'Encode as …' 선택
종류 중 'URL' 선택
하단에 디코딩된 원본 문자열이 출력됨

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[BurpSuite Decoder 캡처]
- 가운데 칸: 인코딩된 문자열 `…%75%74%68%2f%75%73%65%72%2f%70%61%73%73%77%64` (빨간 배경)
- 'Decode as …' 목록에서 **URL**(빨간 화살표) 선택
- 결과(빨간 상자): `http://httpbin.org/basic-auth/user/passwd` — 원본으로 복원됨

---

<!-- p.45 -->

요약 정리
- 실습환경은 Spring Boot 기반 웹 애플리케이션과 BurpSuite 프록시로 구성되어 있다.
- 웹 서비스는 브라우저, 웹 서버, WAS, DB 간의 통신 흐름으로 운영된다.
- HTTP는 요청과 응답 메시지로 통신하며, 상태 정보를 유지하지 않는다.
- HTTP 요청 안에는 바디 외에 메서드, 경로, 쿠키, 파라미터 같은 헤더 등이 들어있다.
- HTTP 응답 안에는 바디 외에 상태 코드가 들어있어, 서버의 처리 상태를 알 수 있다..
- BASE64와 URL 인코딩은 특수 문자나 바이너리 데이터를 안전하게 전달하기 위해 사용된다.

---

<!-- p.46 -->

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

<!-- p.47 -->

감사합니다.

---

<!-- p.48 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
퀴즈

1. 다음 중 웹 애플리케이션 서버 로직의 3대 계층에 속하지 않는 것은?
   1) 데이터 계층　2) 네트워크 계층　3) 비즈니스 계층　4) 프레젠테이션 계층
2. 다음 중 HTTP에 대한 설명으로 옳은 것은?
   1) 무상태 방식
   2) UDP를 기본적으로 사용
   3) Request Method로 GET, POST, PUT, REMOVE 등이 있음
   4) Response Status Code로 2xx는 서버에 에러가 있다는 의미
3. 다음 중 BASE64 인코딩에 대한 내용으로 틀린 것은?
   1) 이메일, JSON, XML 등 텍스트 전송 환경에서 안전하게 사용
   2) 부족한 비트는 0으로 패딩 처리되며, =로 표현
   3) 데이터 손상 및 인코딩 문제를 방지함
   4) 데이터를 8비트 단위로 분할하며, 총 64개의 문자 집합으로 표현

---

<!-- p.49 -->

<!-- 아래는 다단·표 배치로 추출 순서가 뒤섞여 슬라이드 원본을 보고 다시 옮긴 내용 -->
퀴즈 정답

1. **2) 네트워크 계층** — 웹 애플리케이션 서버 로직은 프레젠테이션 계층, 비즈니스 계층, 데이터 계층으로 구성되어 있습니다.
2. **1) 무상태 방식** — HTTP는 주로 TCP기반 무상태 방식으로 통신하며, GET, POST, PUT, DELETE 등의 Request Method를 사용합니다. Response Status Code가 2xx인 경우는 요청이 성공적으로 이루어졌다는 의미입니다.
3. **4) 데이터를 8비트 단위로 분할하며, 총 64개의 문자 집합으로 표현** — BASE64는 데이터를 6비트 단위로 분할합니다.
