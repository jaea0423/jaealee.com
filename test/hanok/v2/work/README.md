# work/ — Phase 0 (CSS 통합) 작업 도구

전부 `v2` 폴더에서 실행합니다. 서버가 먼저 떠 있어야 합니다: `python work/serve.py 8766`

| 파일 | 하는 일 |
|---|---|
| `src_before.html` `before.html` | 통합 **전** 원본(src)과 그 빌드 사본. 모든 비교의 기준. 건드리지 마세요 |
| `sections.json` | 셀렉터 → 구역 배정표(대표 클래스 목록, 순서가 곧 구역 안 배치 순서) + 죽은 클래스 목록 + @media 정렬 순서 |
| `header.css` | 새 CSS 맨 위에 붙는 구조 안내 주석 |
| `apply.py N` | 구역 1..N 을 정리한 CSS 를 `src/index.html` 에 써넣음. 항상 `src_before.html` 에서 다시 계산 |
| `zones/N.gen.css` `zones/N.css` | 구역 N 의 생성본 / 손으로 다듬은 판. `N.css` 가 있으면 그것을 씀 (11 = 반응형 @media 구역) |
| `zones/11.extra.css` | 반응형 구역 뒤에 덧붙이는 규칙. 기본 규칙을 앞 구역으로 올리면서 뒤의 @media 에 지게 된 것을 되살릴 때 |
| `cssparse.py` `csscheck.py` | CSS 파서 / 통합 전후 정적 비교(최종값 보존 + 순서 뒤집힘) |
| `shots.py` | 헤드리스 크롬 스크린샷(4폭 × 대시보드·마법사·설정·예약상세·매장선택·잠금·디스플레이 + 긴 화면 2종)과 픽셀 비교 |
| `compare.py` | 두 스크린샷 묶음을 나란히 붙여 한 장으로 (전후 눈 비교) |
| `tokens.py` | Phase 1 토큰 도구. `inventory`(px 분포) / `exact`(계단에 맞는 값만 토큰으로) / `snap space|font|radius`(계단으로 옮김). 구역 파일을 직접 고침 |
| `src_phase0.html` `phase0.html` `zones_phase0/` | Phase 0 끝난 시점 사본(소스·빌드·구역 파일). 스크린샷 `shots/phase0/` |
| `shot.html` `states.js` | 스크린샷용 감싸개와 화면 상태 스크립트 |
| `snaps/before.json` | 실제 DOM 에 나온 (태그, 클래스) 조합 — csscheck 가 '같은 요소에 같이 걸리는 규칙'을 가릴 때 씀 |

한 구역 진행 순서
```
python work/apply.py N
python build.py
python work/shots.py shoot zoneN v2/dist/hanok-admin.html
python work/shots.py diff before zoneN            # 합계 0 (긴 대시보드 430 은 수십 px 노이즈 있음)
cd work && python cssparse.py ../src/index.html rules_after.json && python csscheck.py rules_before.json rules_after.json snaps/before.json
```
주의: Git Bash 는 `/v2/...` 인자를 `C:/Program Files/Git/v2/...` 로 바꿉니다. 경로는 앞 `/` 없이 넘기세요.
