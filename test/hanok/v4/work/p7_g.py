# -*- coding: utf-8 -*-
"""v4 6차-G — 재아 검토 2
   · 변동 표시: 블록 전체 파랑 → 글자 영역만 파란 칩(.chg-chip). 블록 바탕·테두리는 원래 상태(확정/잠정/경고/잠정+경고) 그대로 →
     상태와 변동이 서로 덮지 않아 '잠정+경고+변동' 도 한 블록에서 다 읽힙니다
   · PIN 글자 40px → 30px (너무 컸다는 평)"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---- 변동 블록 CSS 통째로 교체 (주석 시작 ~ past 규칙까지) ----
a = "/* 오늘 등록·변경·취소·노쇼가 일어난 예약(changeTag 가 있는 것) — 바탕을 통째로 파랑으로."
b = "button.blk.changed.past, button.blk.changed.warned.past{background:var(--blue); opacity:.5}\n"
assert s.count(a) == 1 and s.count(b) == 1
i, j = s.index(a), s.index(b) + len(b)
s = s[:i] + """/* 오늘 등록·변경·취소·노쇼가 일어난 예약(changeTag 가 있는 것) — 글자 부분만 파란 칩(.chg-chip)으로.
   6차 전의 '왼쪽 4px 띠 + 하늘색 글자'는 회색 잠정 블록 위에서 거의 안 보였고,
   6차 A 의 '블록 전체 파랑 + 상태색 테두리' 는 상태(잠정 점선·경고 벽돌)와 변동이 서로 덮어 조합이 어지러웠습니다(재아 검토).
   블록 바탕·테두리는 원래 상태 그대로 두고 그 위에 파란 칩만 얹으므로, 잠정+경고+변동이 한 블록에서 다 읽힙니다.
   내일이 되면 changeTag 가 비어 저절로 풀립니다. '잠정' 꼬리표(.tt)는 지웠습니다(툴팁의 ' · 잠정'은 남김) */
.blk .chg-chip{display:inline-block; line-height:12px; height:12px; padding:0 4px; margin-left:-2px; border-radius:3px; font-size:10px;   /* inline-flex 는 시각·이름 사이 공백을 버립니다. 15px 는 블록(19px)을 거의 채워 어색 → 12px·글자 10px */
  background:var(--blue); color:#fff; box-shadow:0 0 0 1px rgba(255,255,255,.4)}   /* 먹색·벽돌 바탕 위에서 칩 가장자리가 보이게 흰 선 */
.blk .chg-chip b{color:#fff; font-size:10px}
/* 지난 것은 블록처럼 흐리게 */
.blk.past .chg-chip{opacity:.55}
""" + s[j:]

rep("""${blockLabel(it.r)}</button>`;""",
    """${chg?`<span class="chg-chip">${blockLabel(it.r)}</span>`:blockLabel(it.r)}</button>`;""", 2)

# 범례 견본도 칩과 같은 파랑만
rep("""/* 오늘 변동 — 블록과 같은 파랑 + 검정 테두리 (타임라인 .blk.changed 참고) */
.lgsw.chg{background:var(--blue); border:3px solid #2C2C2E; width:18px; height:14px}""",
"""/* 오늘 변동 — 블록 글자 위의 파란 칩과 같은 색 (타임라인 .chg-chip 참고) */
.lgsw.chg{background:var(--blue)}""")

# ---- PIN 글자 줄이기 ----
rep(""".pdots{display:flex; justify-content:center; align-items:center; margin:var(--s24) 0 var(--s8); gap:var(--s12); height:56px}
.pdot{width:48px; height:48px; border:1.5px solid var(--border-strong); background:transparent; display:grid; place-items:center; font-size:40px; line-height:1; color:transparent; transition:color .2s ease; box-shadow:none; border-radius:50%}""",
""".pdots{display:flex; justify-content:center; align-items:center; margin:var(--s24) 0 var(--s8); gap:var(--s16); height:48px}
.pdot{width:40px; height:40px; border:1.5px solid var(--border-strong); background:transparent; display:grid; place-items:center; font-size:30px; line-height:1; color:transparent; transition:color .2s ease; box-shadow:none; border-radius:50%}   /* 40px 은 너무 컸음 → 30px */""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_g ok")
