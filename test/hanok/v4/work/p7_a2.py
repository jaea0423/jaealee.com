# -*- coding: utf-8 -*-
"""6차 묶음 A 조정 — 영업시간 세 칸이 좁은 곳에서 잘리던 것
   · 마법사 오른쪽 열(1280 에서 약 530px)에서 '브레이크 15:30 ~ 17:00' 이 잘림 → 칸 안쪽 여백을 줄이고 마법사에서는 12px
   · 폰(767px 이하)에서 한 줄로 이어도 넘침 → 12px + '영업시간' 라벨 생략(시각 범위만으로 뜻이 통함)"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

rep(""".hours-line .hl-c{min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; padding:0 var(--s12); font-weight:600}
.hours-line .hl-c:first-child{padding-left:0}
.hours-line .hl-c + .hl-c{border-left:1px solid var(--border-strong)}
.hours-line .hl-c i{font-style:normal; color:var(--text-3); font-weight:600; margin-right:var(--s8)}
.hours-line.closed{grid-template-columns:1fr}
""",
""".hours-line .hl-c{min-width:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; padding:0 var(--s8); font-weight:600}
.hours-line .hl-c:first-child{padding-left:0}
.hours-line .hl-c + .hl-c{border-left:1px solid var(--border-strong)}
.hours-line .hl-c i{font-style:normal; color:var(--text-3); font-weight:600; margin-right:6px}
.hours-line.closed{grid-template-columns:1fr}
/* 마법사 날짜 화면의 오른쪽 열은 1280 에서도 530px 정도라 세 칸이 빠듯합니다 — 한 단계 작게 */
.wz-time .hours-line{font-size:12px}
""")

rep("""  /* 영업시간 줄 — 폰에서는 세 칸이 좁아 값이 잘리므로 한 줄에 '|' 구분선으로 이어 씁니다 */
  .hours-line{display:flex}
  .hours-line .hl-c{flex:none; padding:0 var(--s8)}
  .hours-line .hl-c i{margin-right:var(--s4)}
""",
"""  /* 영업시간 줄 — 폰에서는 세 칸이 좁아 값이 잘리므로 한 줄에 '|' 구분선으로 이어 씁니다.
     그래도 340px 안에 다 안 들어가서 12px + '영업시간' 라벨 생략(시각 범위만으로 뜻이 통합니다. '휴무' 는 남김) */
  .hours-line{display:flex; font-size:12px}
  .hours-line .hl-c{flex:none; padding:0 6px}
  .wz-time .hours-line{padding-left:var(--s8); padding-right:var(--s8)}   /* 마법사 카드는 여백이 한 겹 더 있어 10px 가 모자랐습니다 */
  .hours-line:not(.closed) .hl-c:first-child i{display:none}
  .hours-line .hl-c i{margin-right:var(--s4)}
""")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_a2 ok")
