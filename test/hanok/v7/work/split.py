# -*- coding: utf-8 -*-
"""v7 1단계 — src/index.html(한 파일)을 src/page.html + src/css/*.css + src/js/*.js 로 나눕니다.
   build.py 가 다시 한 파일로 합치므로 배포 형태(HTML 하나)는 그대로입니다.
   나누는 기준은 파일 안의 배너(/* ===== 제목 ===== */) 줄 번호입니다. 한 번만 돌립니다."""
import io, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "src", "index.html")
lines = io.open(SRC, encoding="utf-8").read().split("\n")

def find(prefix_line_idx_from, text):
    """text 가 들어 있는 배너 제목 줄의 '배너 시작(/* ====)' 줄 번호(0-based) — 제목은 배너 다음 줄"""
    for i in range(prefix_line_idx_from, len(lines)):
        if lines[i].startswith("/* ====") and i + 1 < len(lines) and text in lines[i + 1]:
            return i
    raise SystemExit("배너 없음: " + text)

style_open = lines.index("<style>"); style_close = lines.index("</style>")
script_open = lines.index("<script>"); script_close = lines.index("</script>")

# ---------- CSS 조각 ----------
css_marks = [
    ("00-fonts",     "글꼴 — 파일 안에 내장"),
    ("01-tokens",    "1. 토큰"),
    ("02-reset",     "2. 리셋"),
    ("03-parts",     "3. 공통 부품"),
    ("04-layout",    "4. 레이아웃"),
    ("05-dash",      "5. 대시보드"),
    ("06-res",       "6. 예약"),
    ("07-settings",  "7. 설정"),
    ("08-lock",      "8. 잠금"),
    ("09-theme",     "9. 테마"),
    ("10-tv",        "10. 손님용 화면"),
    ("11-media",     "11. 반응형"),
    ("12-overrides", "v3 1차"),
    ("13-fallback",  "12. 구형 브라우저 폴백"),
]
css_starts = []
cur = style_open
for name, text in css_marks:
    i = find(cur, text); css_starts.append((name, i)); cur = i + 1
css_parts = []
for k, (name, start) in enumerate(css_starts):
    end = css_starts[k + 1][1] if k + 1 < len(css_starts) else style_close
    css_parts.append((name, lines[start:end]))

# ---------- JS 조각 ----------
js_marks = [
    ("01-data",      "데이터 정의"),
    ("02-supabase",  "Supabase (7차)"),
    ("03-util",      "유틸"),
    ("04-render",    "렌더링"),
    ("05-lock",      "PIN 잠금"),
    ("06-modal",     "공통 팝업"),
    ("07-dash",      "대시보드"),
    ("08-changes",   "변동 이력"),
    ("09-sms",       "문자 안내"),
    ("10-timeline",  "좌석 가동 타임라인"),
    ("11-res",       "예약"),
    ("12-staff-off", "직원 · 근태"),
    ("13-sales-off", "매출 (비활성화)"),
    ("14-settings",  "설정"),
    ("15-sheets",    "입력 시트"),
    ("16-wizard",    "예약 등록 마법사"),
    ("17-display",   "디스플레이 모드"),
    ("18-router",    "주소로 화면 구분"),
    ("19-demo",      "예시 데이터"),
]
js_starts = [("00-boot", script_open + 1)]
cur = script_open
for name, text in js_marks:
    i = find(cur, text); js_starts.append((name, i)); cur = i + 1
js_parts = []
for k, (name, start) in enumerate(js_starts):
    end = js_starts[k + 1][1] if k + 1 < len(js_starts) else script_close
    js_parts.append((name, lines[start:end]))

# ---------- 쓰기 ----------
os.makedirs(os.path.join(BASE, "src", "css"), exist_ok=True)
os.makedirs(os.path.join(BASE, "src", "js"), exist_ok=True)
def w(path, body):
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(body).rstrip("\n") + "\n")
for name, body in css_parts: w(os.path.join(BASE, "src", "css", name + ".css"), body)
for name, body in js_parts:  w(os.path.join(BASE, "src", "js", name + ".js"), body)

page = lines[:style_open] + ["<style>", "__CSS__", "</style>"] + lines[style_close + 1:script_open] + ["<script>", "__JS__", "</script>"] + lines[script_close + 1:]
w(os.path.join(BASE, "src", "page.html"), page)
print("css", [(n, len(b)) for n, b in css_parts])
print("js", [(n, len(b)) for n, b in js_parts])
