# hanok/system/ — 작업 지침 (Codex·GPT 용)

**규칙 전문은 같은 폴더 `CLAUDE.md` 입니다. 손대기 전에 반드시 읽으세요.** 아래는 어기면 바로 사고가 나는 것만 추린 요약입니다.

## 1. 고치는 곳

- 고치는 것은 **`src/css/NN-*.css` · `src/js/NN-*.js` 조각뿐**입니다.
- `dist/hanok-admin.html` · `index.html` · `dev/` · `screen/` 은 **자동 생성**입니다. 직접 편집 금지(3MB 한 덩어리).
- 조각 사이 **순서를 바꾸지 마세요** — CSS 는 뒤가 이기고, JS 는 선언 순서에 걸립니다. 새 조각은 번호를 사이에 끼웁니다(`07b-…`).
- 어느 조각인지 모르면: `python -c "import work.patchlib as L; print(L.where('함수이름('))"`

## 2. 구형 스마트TV 문법 금지 (쓰면 손님 화면이 통째로 죽습니다)

| 금지 | 대신 |
|---|---|
| `?.` | `a && a.b` |
| `??` | `a != null ? a : b` |
| `.flat()` `.replaceAll()` | `.reduce(concat)` / `.split().join()` |
| `structuredClone` | `deepClone()` |
| CSS `inset:` `backdrop-filter` `color-mix()` `oklch()` `:has()` `:is()` `@container` | 풀어 쓰기 / 클래스 직접 붙이기 |

배율은 `zoom` 입니다. **`transform:scale` 금지**(원래 자리를 차지해 화면이 잘립니다).

## 3. 설계 원칙 (디자인을 바꿔도 흐려지면 안 됨)

- **경고는 막지 않고 알리기만.** 자리 겹침·정원 초과·라스트오더 이후 — 빨갛게 알리되 진행은 됩니다. 쓰는 사람은 사장님이고, 판단은 사장님이 합니다.
- 주석은 **한국어로 '왜'** 를 씁니다. (`/* 여백 조정 */` ✗ → `/* TV는 3~5m 떨어져 봅니다 */` ○)
- **예약 객체 모양을 바꾸지 않습니다.** 행 ↔ 객체 변환은 `rowToRes` / `resToRow` 두 함수에서만.
- 날짜가 정해진 계산은 `store().settings` 말고 **`settingsAt(date)`**(좌석 `roomsAt`·`joinsAt`, 코스 `courseGroups(date)`, id 조회 `seatById`).
- supabase-js·Realtime·Edge Function 안 씁니다. `fetch` + `sb()` 헬퍼 하나로 REST·Auth 직접 호출.
- 나타났다 사라지는 요소는 자리를 미리 잡아 두고 **보이기만** 바꿉니다.
- 시트는 `.overlay` 의 `onclick` 이 닫기입니다(`15b-sheetdrag.js` 가 그 클릭을 대신 부름) — 닫는 길을 다른 곳으로 옮기지 마세요.
- **알러지 칸은 없습니다**(2026-09-20, 요청사항에 통합). `allergy` 필드는 옛 예약 표시용으로만 남아 있습니다. 새 입력 칸을 만들지 마세요.

## 4. 손대면 안 되는 것 / 지금 일부러 이런 것

- `PIN_ANY`·문자 흉내(`smsSend`)·저장 안 됨은 **일부러 남겨 둔 미완성**입니다. 순서는 재아가 정합니다.
- 흉내 표시(`.mockbar` `.sb-mock` `.lk-open`)를 지우지 마세요.
- service_role 키·PIN·API 키는 어떤 파일에도 쓰지 않습니다(`build.py` 가 일부를 막습니다). 서버 비밀번호 = PIN + `"00"`.
- `supabase.dev.json` 은 그대로 둡니다.
- 더미 데이터 이름은 **만화·영화·애니메이션 인물**(실존 인물 ✗). 넣는 스크립트는 `work/seed_dev.py`, 환경변수 `HANOK_PIN` 필요.

## 5. 한 단계 끝날 때마다

1. `python build.py` 그리고 `python build.py dev` — **`구형 브라우저 문법 검사 통과`** 가 떠야 정상입니다.
2. 화면을 **직접 보고** 확인합니다(추측 금지). 폭 430 / 820 / 1280 / 1920 + 손님용 TV.
   dev 주소: `http://127.0.0.1:8767/system/dev/` (8767 은 `hanok/` 를 루트로 띄운 서버)
3. `work/PROGRESS.md` 에 한 줄(날짜 · 무엇을 · 왜).
4. 멈추고 보고합니다.
