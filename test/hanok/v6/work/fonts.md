# 내장 글꼴 만드는 법 (v4 3차)

왜: 시스템에 Pretendard·Noto Serif KR 이 없으면 맑은 고딕·바탕으로 떨어져 '파워포인트 느낌'이 납니다.
TV·태블릿은 글꼴을 깔 수 없으니 파일 안에 넣습니다. 전체를 넣으면 10MB 가 넘어 **부분집합(subset)** 만 넣습니다.

## 원본
- Pretendard 1.3.9 (`npm pack pretendard@1.3.9` → `dist/web/static/woff2/Pretendard-Regular.woff2`, `-Bold.woff2`)
- Noto Serif KR (`npm pack @fontsource/noto-serif-kr` → `files/noto-serif-kr-korean-700-normal.woff2`, `-900-`)

## 글자 목록 `subset.txt` (2,579자)
KS X 1001 한글 2,350자 + ASCII 전부 + 기호(· … – — ‘ ’ “ ” ₩ ℃ ○ ● ◇ ◆ □ ■ ★ ☆ → ← ↑ ↓ ✓ ✕ 등)
+ 한자 `歡迎光臨韓屋反店飯點`. **새 한자를 화면에 쓰면 여기에 추가해 다시 만들어야 합니다.**

## 명령
```bash
pip install fonttools brotli
pyftsubset Pretendard-Regular.woff2 --text-file=subset.txt --flavor=woff2 --layout-features='*' --output-file=out/Pretendard-Regular.woff2
# Bold, NotoSerifKR-700, -900 도 같은 식
base64 -w0 out/Pretendard-Regular.woff2 > assets/font-Pretendard-Regular.b64
```
크기: Pretendard 각 ~170KB, Noto Serif 700 ~330KB / 900 ~200KB (base64 후 ×1.33).

## 파일 안 자리표시자
`src/index.html` 맨 위 `@font-face` 의 `__FONT_PT_R__(400) __FONT_PT_S__(600) __FONT_PT_B__(700) __FONT_NS_9__(명조 900)`.
명조 700 은 `__FONT_NS_7__` 자리와 b64 만 준비, @font-face 는 안 넣었습니다(435KB — 파일이 2.8MB 를 넘어서). 필요하면 900 줄을 복사해 700 으로.
`build.py` 의 SUBS 목록이 `assets/` 또는 `../assets/` 에서 찾아 끼웁니다.
