# 2025_강원대_시큐어코딩_6주차_3차시_vF

<!-- p.1 -->

Command 인젝션 취약점 진단 및 대응
01 Command 인젝션 개념과 발생 원리
02 Command 인젝션 취약점 진단 및 대응

---

<!-- p.2 -->

학습 목표
Command 인젝션 취약점의 개념과 발생 원리를 이해한다.
실제 공격 기법을 학습하고, 취약점을 진단하는 방법을 익힌다.
시큐어코딩 및 시스템 보호 기법으로 Command 인젝션을 방어할 수 있다.

---

<!-- p.3 -->

학습 내용
1. Command 인젝션 개념 및 발생원리
2. Command 인젝션 취약점 진단 및 대응

---

<!-- p.4 -->

Command 인젝션 취약점 진단 및 대응
01 Command 인젝션 개념 및 발생 원리
02 Command 인젝션 취약점 진단 및 대응

---

<!-- p.5 -->

Command 인젝션이란?
개요
적절한 검증 절차를 거치지 않은 사용자 입력 값이 명령어의
일부 또는 전부로 구성되어 실행되는 경우 의도하지 않은
시스템 명령어가 실행되어 부적절하게 권한이 변경되거나
시스템 동작에 악영향을 미친다.
발생원인
운영체제 명령을 실행하는 함수를 사용하는 경우, 검증되지
않은 사용자 입력 값이 명령이나 명령의 파라미터로
사용되는 경우에 발생한다.

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[이미지] 오른쪽 흑백 일러스트: 복면(눈가리개 마스크)과 후드를 쓴 해커가 웃으며 주사기를 들고 컴퓨터 본체 쪽으로 손을 뻗고 있음. 옆 모니터 화면에 큰 글씨로 "COMMAND INJECTION"이라고 표시됨 → '명령어를 주입(injection)한다'는 개념을 주사기로 비유한 그림.

---

<!-- p.6 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## Command 인젝션이란?

[도식] 공격자 → 웹 서버 → 명령어 창(cmd.exe)으로 이어지는 Command 인젝션 공격 흐름. 각 단계에 말풍선(생각 구름) 설명이 붙어 있음.

**등장 요소 (왼쪽 → 오른쪽)**
- **공격자** (선글라스 낀 사람 + 노트북 아이콘)
- **웹 서버** (서버 아이콘)
- **명령어 창** (검은 콘솔 박스, 안의 내용):
  ```
  cmd.exe
  type "filename"
  & ping 127.0.0.1
  ```

**화살표 흐름**
1. ① 조작된 Request — 공격자 → 웹 서버 (오른쪽 방향 화살표)
2. ② 조작된 명령문 실행 — 웹 서버 → 명령어 창 (오른쪽 방향 화살표)
3. ③ 공격 결과 — 웹 서버 → 공격자 (왼쪽 방향 되돌아오는 화살표)

**말풍선(생각 구름) 내용**
- (공격자 아래, 파란 점선 구름 — 사전 정찰 단계) "입력 값을 서버 내부에서 쉘(cmd.exe)을 실행할 때 argument 로 사용하는 기능을 찾는다."
- (① 화살표 위, 빨간 점선 구름 — 공격자의 조작) "filename & ping 127.0.0.1 로 파일명을 조작한다."
- (웹 서버 위, 빨간 점선 구름 — 서버의 원래 동작) "파일명(filename)을 입력하면, cmd.exe 명령을 실행하여 type 명령을 이용하여 파일 내용을 화면에 출력한다."
- (명령어 창 위, 빨간 점선 구름) "조작된 명령문 실행"

**정리**: 서버는 원래 `cmd.exe` 로 `type "파일명"` 을 실행해 파일 내용을 보여주는 기능이다. 공격자가 파일명 자리에 `filename & ping 127.0.0.1` 을 넣으면 cmd.exe 가 `&` 를 명령 구분자로 해석하여 `type "filename"` 다음에 `ping 127.0.0.1` 을 추가로 실행하고, 그 결과가 응답으로 공격자에게 돌아온다.

(※ 검증: 이 PC의 cmd.exe에서 `type "nofile.txt" & echo SECOND_CMD_RAN` 실행 — 첫 명령이 '파일을 찾을 수 없음' 오류로 실패해도 `&` 뒤 명령이 실행됨을 확인 — 일치. `&` 는 앞 명령의 성공 여부와 무관하게 다음 명령을 실행하는 연결자임.)

---

<!-- p.7 -->

운영체제별 명령어 실행 방식 이해 - Windows
기본 명령어 인터프리터
주로 cmd.exe와 최근에는 PowerShell 사용
내부 명령어와 외부 프로그램 호출 방식 구분
명령어 파싱 및 실행 과정
특수문자(예: &, |, >)를 이용한 명령어 연결 및 리다이렉션
보안 고려사항
명령어 인젝션 시, cmd.exe의 특수문자 해석을 악용 가능
PowerShell의 스크립트 실행 정책 및 명령어 확장 취약점 존재

---

<!-- p.8 -->

운영체제별 명령어 실행 방식 이해 - Linux
기본 명령어 인터프리터
기본적으로 /bin/sh(대부분 Bash 기반) 사용
쉘의 확장 기능(파이프, 리다이렉션, 와일드카드 등) 활용
명령어 파싱 및 실행 과정
공백, 따옴표, 이스케이프 문자() 처리 방식
환경 변수, 명령어 치환(`, $() 등)의 해석 과정 포함
보안 고려사항
쉘 메타문자 및 파이프, 명령어 치환의 잘못된 처리로 인젝션 위험 증가
환경 변수 조작 및 경로 변조 공격 가능성

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[이미지] 오른쪽에 Linux 마스코트 펭귄(Tux) 그림.
(※ 원문 표기 그대로 — "이스케이프 문자()" 의 괄호 안이 비어 있음. 슬라이드 이미지에서도 빈 괄호로 렌더링됨. 문맥상 이스케이프 문자인 백슬래시 `\` 가 누락된 것으로 보임: "이스케이프 문자(\)")

---

<!-- p.9 -->

Command 인젝션 취약점 진단 및 대응
01 Command 인젝션 개념 및 발생 원리
02 Command 인젝션 취약점 진단 및 대응

---

<!-- p.10 -->

Command 인젝션 취약점 진단 - 수동진단
수동 진단의 목표
사용자 입력이 시스템 명령어와 결합되어 실행되는 경우, 악의적인 조작이 가능한지 확인
의도치 않은 명령 실행이나 출력 조작을 통해 취약점을 탐지
기본 접근 방법
테스트 입력 값에 특수문자 및 제어 문자를 삽입하여 명령어의 실행 흐름 변화를 관찰
다양한 OS(Windows, Linux)와 쉘의 파싱 규칙을 고려하여 테스트 케이스 설계

---

<!-- p.11 -->

Command 인젝션 취약점 진단 - 수동진단
명령어 연결자 테스트
&, &&, ||, ; 등으로 추가 명령어 실행 테스트
예) "test && cat /etc/passwd" 또는 "test; ls"
파이프 및 리다이렉션 테스트
|, >, < 등을 활용해 명령어 조작 테스트
예) "test | ls", "test > output.txt"

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
예시 페이로드 정리:
```bash
test && cat /etc/passwd   # 앞 명령 성공 시 /etc/passwd 출력
test; ls                  # 앞 명령 결과와 무관하게 ls 실행
test | ls                 # 파이프: 앞 출력이 ls 입력으로 전달, ls 결과 출력
test > output.txt         # 리다이렉션: 출력을 파일로 저장
```
(※ 검증: bash 에서 `echo test && echo CAT_RAN`, `echo test; ls`, `echo test | ls`, `echo test > output.txt` 를 실행해 각각 추가 명령 실행·파이프·파일 생성이 일어남을 확인 — 일치)

---

<!-- p.12 -->

Command 인젝션 취약점 진단 - 수동진단
환경 변수 활용 테스트
환경 변수 활용
$PATH, $IFS 등을 이용하여 명령어 실행 환경 변경하거나, 검증 우회 시도
예) "test $PATH" 또는 "test$IFSls" 처럼 환경변수 활용 가능한지 테스트
서브 명령 실행 테스트
백틱 및 $() 사용
백틱 (`) 또는 $()`를 사용해 서브 명령어 실행되는지 테스트
예) "test `ls`" 또는 "test $(ls)"

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
예시 페이로드 정리:
```bash
test $PATH       # 환경변수 확장 여부 확인
test$IFSls       # $IFS(공백·탭·개행)로 공백 필터 우회 시도
test `ls`        # 백틱 명령 치환
test $(ls)       # $() 명령 치환
```
(※ 검증: bash 에서 `echo test$IFSls` 를 실행하면 `test` 만 출력됨 — 쉘이 `$IFSls` 를 하나의 변수명 `IFSls`(정의되지 않음 → 빈 문자열)로 해석하기 때문. `$IFS` 뒤에 바로 영문자가 오면 구분이 안 되므로, 의도대로 동작하려면 `test${IFS}ls` 처럼 중괄호로 변수명을 구분해야 함(이 경우 `test<공백/탭/개행>ls` 로 확장됨을 확인). `$IFS` 바로 뒤가 `/` 같은 비식별자 문자일 때(예: `cat$IFS/etc/passwd`)는 중괄호 없이도 동작.)
(※ 검증: `` echo test `ls` `` 와 `echo test $(ls)` 는 둘 다 `test a.txt b.txt` 처럼 ls 결과가 치환되어 출력됨 — 일치)
(※ 원문 표기 그대로 — "백틱 (`) 또는 $()`를 사용해" 에서 `$()` 뒤에 불필요한 백틱(`)이 하나 더 붙어 있음)

---

<!-- p.13 -->

Command 인젝션 취약점 진단 – 자동화도구 활용
ZAP (Zed Attack Proxy) 설치 및 기본 설정
ZAP 공식 사이트(https://www.zaproxy.org/)에서 최신 버전 다운로드 및 설치
ZAP 실행 후, 프록시 포트(기본 8080) 확인
진단 환경 구성
진단 대상 웹 서비스 준비
브라우저 프록시 설정
브라우저의 프록시 설정을 ZAP의 프록시(예: localhost:8080)로 변경하여 모든 트래픽이 ZAP을 통해 흐르도록 설정

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[이미지] 오른쪽 위: ZAP 마스코트(방패 체크 표시 위에 번개 로고가 있는 로봇) 일러스트.
[도식] 하단 트래픽 흐름: [Browser] → (ZAP 번개 로고) → [Network Proxy] → [Web Application]
→ 브라우저의 모든 요청이 ZAP(프록시, 기본 localhost:8080)을 거쳐 네트워크/대상 웹 애플리케이션으로 전달되는 구조.

---

<!-- p.14 -->

Command 인젝션 취약점 진단 – 자동화도구 활용
ZAP의 자동 검사 Active Scan 수행 방법
ZAP 좌측 트리에서 테스트 대상 URL 선택 후, 우 클릭
→ "Attack" → "Active Scan" 실행
스캔 결과 확인
스캔 결과 창에서 "Command Injection" 관련 알림
(예: 에러 메시지, 비정상 응답 코드 등) 확인
알림 상세 정보를 통해 의심되는 입력 필드 및 실행 결과
분석

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
[화면 캡처 1] ZAP 메인 창 — 타이틀 "Untitled Session - ZAP 2.16.1", 모드 "Standard Mode". 메뉴바: 파일 / Edit / View / Analyse / 보고서 / Tools / Import / Export / Online / Help (한글·영문 혼합 UI).
- 좌측 Sites 트리: Contexts > Default Context, Sites > **http://localhost:…** (선택·강조) 하위에 `GET:/`, `board`, `css`, `img`, `GET:login`, `POST:login()(us…`, 그리고 `http://o.pki.goog…`.
- 대상 URL 우클릭 컨텍스트 메뉴: **공격**(=Attack, 강조) / Break... / Delete / Exclude from / Run application / 새 경고 / 이 노드에 대한 경고 / Include in Context / Include Site in Context / Exclude from Context / Flag as Context / Include Channel URL in Context / Exclude Channel URL from Context / Open/Resend with Request Editor... / Open in Requester Tab... (Ctrl+W) / Open URL in Browser / 시스템 브라우저에서 URL 열기 / Show in History Tab
- "공격" 하위 메뉴: **Active Scan...** / AJAX Spider... / Client Spider... / Spider... / Fuzz... / Forced Browse Site / Forced Browse Directory / Forced Browse Directory (and Children)
- 오른쪽 Welcome 탭: "Welcome to ZAP", "…ed penetration testing tool for finding vulnerabilities in web applications.", "…best to start with one of the options below.", 버튼 [Automated Scan] [Manual Explore], News 박스 "ZAP 2.16.1 is available now" [Learn More]. 상단 탭: …uest / Response / Requester.

[화면 캡처 2] "Active Scan" 대화상자 — 탭: Scope / 필터 / Input Vectors / Custom Vectors / Technology / **Policy**(선택).
- 왼쪽 Policy 트리: Client Browser / Information Gathering / **Injection**(선택) / Miscellaneous / Server Security
- 오른쪽 Injection 정책 목록 (Test Name / Threshold / Strength / Status — 모든 행 Default / Default / Release):
  Buffer Overflow, Cloud Metadata Potentially Exposed, CRLF Injection, Cross Site Scripting (Persistent), Cross Site Scripting (Persistent) - Prime, Cross Site Scripting (Persistent) - Spider, Cross Site Scripting (Reflected), Format String Error, Parameter Tampering, **Remote OS Command Injection**(선택·파란 강조), Server Side Code Injection, Server Side Include, Server Side Template Injection, Server Side Template Injection (Blind), Spring4Shell, SQL Injection, SQL Injection - Hypersonic SQL, SQL Injection - MsSQL, SQL Injection - MySQL
- 하단 버튼: [Start Scan] [초기화] [취소]
→ Command 인젝션 진단은 Active Scan 정책 중 Injection 카테고리의 "Remote OS Command Injection" 스캔 규칙이 담당함.
(※ 원문 표기 그대로 — 본문은 "Attack" → "Active Scan" 이라고 했지만, 캡처 속 ZAP은 한글 UI라 메뉴명이 "공격" 으로 표시됨)

---

<!-- p.15 -->

Command 인젝션 대응 – 시큐어코딩 적용
명령어 삽입 취약점이 발생하는 경우
안전하지 않은 코드
...
String version = request.getParameter("version");
String cmd = new String("cmd.exe /K \"run.bat \"");
Runtime.getRuntime().exec(cmd + " c:\\prog_cmd\\" + version);
...
안전한 코드
...
String version = request.getParameter("version");
if(version.matches("[0-9.]+")) {
Runtime.getRuntime().exec(new String[]{"cmd.exe","/c", "run.bat", version});
} else {
부적합한 값으로 처리
}
…

<!-- 아래는 슬라이드 이미지·도표에서 판독한 내용 -->
코드(들여쓰기 포함 원문):

안전하지 않은 코드 (빨간 라벨)
```java
...
 String version = request.getParameter("version");
 String cmd = new String("cmd.exe /K \"run.bat \"");
 Runtime.getRuntime().exec(cmd + " c:\\prog_cmd\\" + version);
...
```

안전한 코드 (파란 라벨)
```java
...
 String version = request.getParameter("version");
 if(version.matches("[0-9.]+")) {
   Runtime.getRuntime().exec(new String[]{"cmd.exe","/c", "run.bat", version});
 } else {
    부적합한 값으로 처리
 }
…
```
[이미지] 제목 옆 자물쇠 아이콘, 코드 상자 위 라벨 리본("안전하지 않은 코드"=빨강, "안전한 코드"=파랑) — 장식용 이미지이며 코드 자체는 텍스트임.

(※ 검증: Python으로 Java 문자열 결합 결과 재현 — `cmd` 값은 `cmd.exe /K "run.bat "`, 최종 문자열은 version=`1.0 & dir` 일 때 `cmd.exe /K "run.bat " c:\prog_cmd\1.0 & dir`. cmd.exe /K 가 나머지 문자열을 해석하므로 `&` 뒤 `dir` 이 추가 실행됨 → 취약 — 일치)
(※ 검증: Java `String.matches()` 는 전체 일치이므로 Python `re.fullmatch(r"[0-9.]+")` 로 확인 — `1.0`, `1.2.3` 통과 / `1.0 & dir`, `1;ls`, `1.0&type …` 거부 — 일치. 단, `..` 같은 점만으로 된 값도 통과함(이 예제에서는 version 이 경로가 아닌 run.bat 인자로만 쓰여 영향은 제한적).)
(※ 참고: 안전한 코드도 여전히 cmd.exe /c 를 거쳐 run.bat 을 실행하므로, 인자 배열 방식만으로는 cmd.exe 의 메타문자 해석을 완전히 막지 못함 — 화이트리스트 정규식 검증이 실질적 방어선 역할을 함. 또 안전하지 않은 코드는 `/K`, 안전한 코드는 `/c` 로 옵션이 다름.)

---

<!-- p.16 -->

Command 인젝션 대응 – 시큐어코딩 적용
안전한 API 사용
직접 OS 명령어를 실행하지 않고, 안전하게 프로세스를 실행하는 API (예: 인자 배열 방식의 ProcessBuilder, execvp() 등) 사용
→ Command 인젝션 위험을 줄이기 위해 파라미터와 명령어를 명확하게 분리
사용자 입력 값 검증
화이트리스트 기반 검증: 허용된 값만 받아들이고, 예상치 못한 입력은 모두 거부
→ 정규 표현식, 타입 체크 등을 활용하여 올바른 포맷만 통과
메타 문자 필터링
사용자 입력에서 특수문자 (&, ;, |, >, <, $(), `` 등)를 제거하거나 이스케이프 처리
→ 입력 값에 포함된 메타문자를 명시적으로 치환하거나 제거하여, 명령어 결합 우회 방지

---

<!-- p.17 -->

Command 인젝션 대응 – 시큐어코딩 적용
에러 핸들링 및 로깅
입력 값 검증 실패 및 명령어 실행 오류 시, 민감 정보가 노출되지 않도록 안전하게 처리
→ 오류 발생 시 내부 로그에만 기록하고, 사용자에게는 최소한의 정보만 제공
코드 리뷰 및 정적 분석
정기적인 코드 리뷰와 정적 분석 도구를 활용하여 Command 인젝션 취약점 사전 탐지
보안 관련 라이브러리 및 프레임워크의 최신 업데이트 적용
테스트 케이스 마련
다양한 악의적 입력(우회 페이로드, 인코딩 변형 등)을 포함한 단위 테스트, 통합 테스트를 수행

---

<!-- p.18 -->

Command 인젝션 대응 – 시스템 보호 전략
1. 최소 권한 원칙 적용
애플리케이션 또는 명령어 실행 시 비 권한 사용자 계정을 활용
시스템 서비스나 웹 서버의 실행 권한 제한을 통해 공격 성공 시 피해 범위 최소화
2. 애플리케이션 샌드박싱 및 컨테이너화
샌드박스 환경 또는 컨테이너(예: Docker)를 이용해 애플리케이션 격리
외부 명령 실행 시 격리된 환경 내에서 실행하여 시스템 전체에 영향을 주지 않도록 구성
3. 로깅 및 모니터링 활성화
명령어 실행 로그, 에러 로그, 접근 로그를 체계적으로 기록
이상 행동 감지 시 즉각 알림 및 대응할 수 있는 모니터링 시스템 구축

---

<!-- p.19 -->

요약 정리
- Command 인젝션은 검증되지 않은 입력이 OS 명령어를 조작해 시스템을 장악하는 취약점입니다.
- 공격 원리는 메타문자(;, &, |)를 사용해 OS 명령어 파싱 방식을 악용하는 방식입니다.
- 취약점 진단은 수동 진단과 OWASP ZAP 같은 자동화 도구를 병행해 수행합니다.
- 대응 방안으로 입력 값 검증과 안전한 API 사용, 그리고 최소 권한·샌드박싱·모니터링을 사용합니다.
- 지속적으로 코드 리뷰와 CI/CD 보안 검증을 적용해 사전에 차단하고 재발을 방지해야 합니다.

---

<!-- p.20 -->

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

<!-- p.21 -->

감사합니다.

---

<!-- p.22 -->

<!-- 아래는 슬라이드 원본(도식·표·이미지 포함)을 보고 다시 옮긴 내용 -->
## 퀴즈

**1. 다음 중 Windows 환경에서 Command 인젝션 위험을 줄이기 위한 방법으로 가장 옳은 것은 ?**
- 1) 문자열 결합으로 명령어를 만들고, 관리자 권한으로 실행한다.
- 2) 사용자 입력을 전혀 검증하지 않고 바로 cmd.exe /c에 전달한다.
- 3) 명령 인자를 배열로 분리하고, 권한이 제한된 계정으로 실행한다.
- 4) PowerShell 스크립트를 항상 시스템 권한으로만 실행한다.

**2. 다음 중 Command 인젝션 공격 예시로 볼 수 있는 것은 ?**
- 1) `ls –al`
- 2) `dir C:\Users`
- 3) `ls; rm -rf /`
- 4) `ping 127.0.0.1`

(※ 원문 표기 그대로 — 1)번 `ls –al` 의 하이픈이 일반 하이픈(-)이 아닌 en dash(–)로 입력되어 있음)

**3. Linux 환경에서 명령어를 연속 실행하기 위해 자주 사용되는 쉘 연산자 기호를 정확히 쓰세요.**

(            )

---

<!-- p.23 -->

퀴즈 정답
1. 다음 중 Windows 환경에서 Command 인젝션 위험을 줄이기 위한 방법으로 가장 옳은 것은 ?
3) 명령 인자를 배열로 분리하고, 권한이 제한된 계정으로 실행한다.
인자를 배열로 분리하고, 최소 권한 계정을 사용해야 인젝션 위험이 낮아집니다.
2. 다음 중 Command 인젝션 공격 예시로 볼 수 있는 것은 ?
3) ls; rm -rf /
세미콜론 ;을 사용해 기존 명령 뒤에 rm -rf /를 추가로 실행하므로, 전형적인 인젝션 공격 시도입니다.
3. Linux 환경에서 명령어를 연속 실행하기 위해 자주 사용되는 쉘 연산자 기호를 정확히 쓰세요.
( ; )
