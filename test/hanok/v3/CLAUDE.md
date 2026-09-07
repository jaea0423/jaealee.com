# v3 — 재아 요청 반영 작업 폴더

**여기가 작업 공간입니다. `v2/` 와 상위 폴더(v1)는 읽기 전용입니다.**

---

## 0. 무엇이 어디에 있나

| 경로 | 상태 |
|---|---|
| `../src/index.html` `../index.html` `../dist/` `../build.py` | **읽기만.** 사장님 댁에 나간 링크가 여는 파일 |
| `../v2/` | **읽기만.** 디자인 개편(Phase 0~6)이 끝난 상태. v3 는 여기서 복사해 시작했습니다 |
| `../assets/*.b64` | **읽기만.** 빌드가 여기서 이미지를 가져옵니다 |
| `v3/src/index.html` | ★ 여기만 고칩니다 |
| `v3/work/` | 패치 스크립트 · 스크린샷 · 진행 기록 |

빌드:

```bash
cd v3
python build.py
```

결과는 `v3/dist/hanok-admin.html` 과 `v3/index.html` 에만 생깁니다.
배포 주소: **`jaealee.com/test/hanok/v3`**

## 1. v2 와 다른 점

- v2 의 `work/zones/*.css` + `apply.py` (CSS 구역 재조립) 는 **쓰지 않습니다.** CSS 통합이 끝났으므로
  `src/index.html` 을 직접 고칩니다. 새 CSS 는 11구역 끝의 **"v3 1차" 블록**에 덧붙입니다 (뒤가 이기니까).
- 동작(자바스크립트) 수정이 많습니다. 각 수정은 `work/patch_v3_*.py` 로 남겨 두었고, 정확히 한 번만 맞는 치환만 합니다.
- 서버·스크린샷 도구는 v2 것을 그대로 가져와 경로만 `/v3/` 로 바꿨습니다:
  `python work/serve.py 8766` (프로젝트 루트 기준이라 v2 서버가 떠 있으면 그것으로도 됩니다),
  `python work/shots.py shoot <라벨> v3/index.html` (`SHOT_STATES=dash,wizard` 로 일부만).

## 2. 이번 작업의 설계 원칙 — "누르는 선택에 따라 화면 높이가 바뀌지 않게"

나타났다 사라지는 요소는 **자리를 미리 잡아 두고 보이기만 바꿉니다.**
`.ghost` (visibility:hidden) 와 슬롯(`.ns-slot`, `.wz-warn` min-height) 이 그 도구입니다.
새 요소를 조건부로 그릴 때 `display:none` 이나 `${cond ? html : ""}` 를 쓰기 전에, 그 요소가 생길 때 아래가 밀리는지 먼저 생각하세요.

## 3. 코드 규칙 (v1·v2 와 동일)

상위 `../CLAUDE.md` 2장을 그대로 따릅니다. 특히 구형 스마트TV 문법 금지(`?.` `??` `.flat()` `inset:` 등),
배율은 `zoom`, **경고는 막지 않고 알리기만**, 주석은 한국어로 '왜'를, 흉내 표시(`.mockbar` `.sb-mock` `.lk-open`) 유지.

## 4. 한 단계 끝날 때마다

1. `python build.py` — `구형 브라우저 문법 검사 통과`
2. 네 폭(430/820/1280/1920) 스크린샷 + 동작은 브라우저에서 직접 눌러 확인
3. `work/PROGRESS.md` 에 한 줄
4. 멈추고 보고
