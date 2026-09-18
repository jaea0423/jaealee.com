# 한옥반점 — 가게 사이트 + 예약 관리 시스템

이 파일은 Claude Code 가 자동으로 읽습니다. **먼저 이것부터 읽고 시작하세요.**

경기 성남시 분당구 중식당 **한옥반점**(사장님 = 재아의 누님 김지아)의 홈페이지와 예약 관리 시스템입니다.
재아(컴공 2학년)가 혼자, 무상으로 만듭니다. 쓰는 사람은 사장님·홀 직원·손님 — 개발자가 아닙니다.

---

## 0. 무엇이 어디에 있나

| 주소 | 폴더 | 무엇 |
|---|---|---|
| `jaealee.com/hanok/` | `hanok/` (이 폴더) | **가게 사이트** — 손님이 보는 홈페이지 7장(소식 포함) + 예약 창. 정적 파일, 빌드 없음. 자세한 건 `README.md` |
| `jaealee.com/hanok/system/` | `system/` | **예약 관리 시스템** — 카운터 태블릿·사장님 폰. HTML 파일 하나로 빌드. **규칙은 `system/CLAUDE.md`** |
| `jaealee.com/hanok/system/dev/` | `system/dev/` | 시스템 개발용 빌드 (`python build.py dev`) |
| `jaealee.com/hanok/system/screen/` | `system/screen/` | 손님용 TV 화면 (+ 광고 영상 `ad.mp4`) |
| `jaealee.com/test/hanok/` | `../test/hanok/` | **옛 버전 보관(v1~v6)·옛 문서. 읽기만.** 누님께 보낸 링크가 살아 있어 옮기지 않습니다 |

2026-09-16 에 `test/hanok/site` → `hanok/`, `test/hanok/v7` → `hanok/system/` 으로 옮겼습니다. 옛 문서에 `v7/` `test/hanok/` 이 보이면 이 폴더 이야기입니다.

## 1. 두 물건은 규칙이 다릅니다

| | 사이트 `hanok/` | 시스템 `system/` |
|---|---|---|
| 보는 기기 | 손님 폰 우선 | 태블릿 > 폰 > 구형 TV(2018~2020 크롬) > PC |
| 문법 제약 | 없음(현대 CSS·JS) | **구형 TV 금지 문법** — `system/CLAUDE.md` 2장 |
| 데이터 | `data/site.js` 기본값 + 서버 `site_versions` + Supabase `public_avail`(읽기)·`requests`(접수) | Supabase `stores`·`reservations`·`logs` + 위 둘 |
| 확인 | `python work/shot.py` (8767 서버 필요) | `python build.py` + 브라우저 |

## 2. 사이트 ↔ 시스템 연동

- 시스템이 내일부터 30일치 남은 자리를 `public_avail` 에 올리고(`system/src/js/11c-site-link.js`), 사이트 예약 창은 그것만 읽습니다.
- 사이트 접수는 `requests` 표에 한 줄(anon 은 넣기만). 시스템이 1분마다 읽어 팝업 → 승인/거절.
- 사이트 내용은 `data/site.js`(기본값) 위에 서버 `site_versions` 최신 판을 덮음(`js/content.js`). 시스템 설정 → 홈페이지 → **홈페이지 관리**(`system/src/js/14b-site-admin.js`)에서 초안 → 미리보기(`?preview=1`) → 적용(지금/정한 시각). 사진·PDF·TV 광고 영상은 Storage `site` 버킷에 올림(`saPickFile`).
- **소식**(`news.html`, `js/news.js`)은 서버 `site_posts` 표를 바로 읽습니다 — 초안·적용 판과 무관하게 시스템 홈페이지 관리 → 소식 에서 저장하면 즉시 반영. 표·정책은 `system/supabase/patch_14차_소식.sql`.
- 접속 정보는 `js/config.js`(anon 키·URL — 공개해도 되는 키). **service_role 키는 어떤 파일에도 쓰지 않습니다.**
- 서버 표·정책은 `system/supabase/patch_9차_홈페이지.sql`. 실서비스 순서는 `system/supabase/checklist.md` 8장.

## 3. 로컬 확인

```bash
# 이 폴더(hanok/)를 루트로 8767 — .claude/launch.json 의 "hanok"
python -m http.server 8767 --bind 127.0.0.1
#  사이트   http://127.0.0.1:8767/
#  시스템   http://127.0.0.1:8767/system/dev/   (개발용, PIN 은 재아만)
```

## 4. 공통 규칙

- 주석은 한국어로, **'왜'** 를 씁니다. 나중에 재아 혼자 읽습니다.
- 경고는 막지 않고 알리기만(시스템 설계 원칙). 사이트 예약 창도 서버가 최종 확인하니 화면은 안내만.
- 커밋·푸시는 재아가 직접 합니다. 묶음 하나 끝나면 빌드·확인·`system/work/PROGRESS.md` 한 줄·보고.
- 누님께 여쭐 것은 `system/work/누님_질문.md` 에 번호 붙여 모읍니다.
- 이 저장소(jaealee.com) 전체 규칙은 루트 `AGENTS.md`·`README.md`.
