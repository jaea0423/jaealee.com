# 대경빌 주차 관리 시스템

정적 HTML + Supabase 로 만든 아주 작은 주차 등록 관리 도구입니다.

```
index.html   방문자용 - 등록 차량 번호 목록
admin.html   관리자용 - PIN 로그인 / 등록 / 관리 / PIN 변경
config.js    Supabase 주소와 키를 적는 곳  ← 여기만 채우면 됩니다
style.css    공용 디자인
setup.sql    Supabase 최초 설정 SQL (한 번만 실행)
```

---

## 설정 순서 (한 번만)

### 1. Supabase 프로젝트 만들기
1. https://supabase.com 로그인 → **New project**
2. 이름은 아무거나 (예: `daegyeong-parking`)
3. Region 은 **Northeast Asia (Seoul)** 을 고르면 조금 더 빠릅니다
4. Database Password 는 아무거나 정하고 따로 적어 두세요

> jaealee.com 에서 쓰는 기존 프로젝트와 **섞지 말고 새로 만드는 것**이 맞습니다.
> 무료 플랜에서도 프로젝트를 여러 개 만들 수 있습니다.

### 2. 표(table) 만들기
왼쪽 메뉴 **SQL Editor** → `setup.sql` 내용을 통째로 붙여넣고 **Run**.

### 3. 관리자 계정 만들기
왼쪽 메뉴 **Authentication → Users → Add user → Create new user**

- Email: `jaea0423@gmail.com` (config.js 의 `ADMIN_EMAIL` 과 같아야 합니다)
- Password: **처음 쓸 PIN 6자리** (예: `482913`)
- **Auto Confirm User 를 반드시 켜세요** (안 켜면 로그인이 안 됩니다)

### 4. 키 복사해서 config.js 에 넣기
왼쪽 메뉴 **Project Settings → API**

- `Project URL` → `config.js` 의 `SUPABASE_URL`
- `anon public` 키 → `config.js` 의 `SUPABASE_ANON_KEY`

### 5. 커밋 & 푸시
끝입니다. `https://jaealee.com/yb/parking/` 로 들어가면 동작합니다.

---

## 왜 PIN 을 Supabase 비밀번호로 쓰나요?

이 사이트는 **정적 사이트(static site)** 입니다.
브라우저가 받아 가는 것은 HTML/CSS/JS 파일 그 자체라서,
`if (pin === "123456")` 같은 검사를 JS 안에 적어 두면
F12(개발자 도구)로 소스를 열어 보는 순간 PIN 이 그대로 보입니다.
즉 **문에 자물쇠가 아니라 "들어오지 마세요" 팻말을 붙인 것**과 같습니다.

그래서 이 프로젝트는 PIN 을 **Supabase 계정의 비밀번호 자체**로 씁니다.

- PIN 검사는 브라우저가 아니라 **Supabase 서버**가 합니다 → 소스를 봐도 알 수 없습니다
- 데이터베이스에는 **RLS(Row Level Security)** 가 켜져 있어서,
  로그인하지 않은 사람은 `vehicles` 표를 읽지도 쓰지도 못합니다
- 방문자에게는 `vehicles_public` 이라는 **뷰(view)** 만 열어 둡니다.
  이 뷰에는 **차량번호만** 들어 있어서 호실·메모 같은 개인정보는 새어 나가지 않습니다

`anon key` 가 소스에 보이는 것은 정상이며, 원래 공개용 키입니다.
실제 권한은 위의 RLS 정책이 결정합니다.

---

## 사용법

**방문자** — `index.html`
등록 기간 중인 차량 번호만 보입니다. (등록 예정·만료·삭제된 차량은 안 보임)

**관리자** — 제목 "대경빌 등록 차량" 을 **1.5초 안에 5번 연속** 클릭 → `admin.html`

- **등록**: 1단계(호실·기간·차량번호) → 2단계(차량 종류·메모) → 등록하기 → 첫 화면으로
- **관리**: 등록 중 / 등록 예정 / 만료 / 삭제됨 탭.
  차량을 누르면 수정 화면. 기간은 날짜를 직접 고치거나 `+n개월` 버튼으로 연장.
  `삭제` → 삭제됨 탭으로 이동, 거기서 `복구` 또는 `영구 삭제`.
- **PIN 변경**: 숫자 6자리 PIN, 또는 8자 이상(대문자·숫자·특수문자 포함) 비밀번호.

로그인 상태는 브라우저에 유지되므로 매번 PIN 을 넣지 않아도 됩니다.
공용 PC 에서 썼다면 메뉴 아래 **로그아웃** 을 눌러 주세요.
