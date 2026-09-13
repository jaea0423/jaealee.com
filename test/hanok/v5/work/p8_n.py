# -*- coding: utf-8 -*-
"""설정 화면 나가기 버튼이 가운데로 — 상단바 3열 grid(날짜 가운데용)가 설정에도 적용돼 bar-right 가 가운데 열에 놓임. 설정은 flex 로."""
import io
P = "src/index.html"; s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80]); s = s.replace(old, new)
rep("""      <header class="topbar ${notodayView()?'notoday':''} ${isMobile()?'mobile':''}"><div class="topbar-in">""",
    """      <header class="topbar ${notodayView()?'notoday':''} ${isMobile()?'mobile':''} ${view.tab==="settings"?'settings':''}"><div class="topbar-in">""")
rep("""  .topbar-in .more-veil{grid-column:1 / -1}
}""",
"""  .topbar-in .more-veil{grid-column:1 / -1}
  /* 설정 화면은 가운데 칸(날짜)이 없어 grid 면 나가기 버튼이 가운데로 옵니다 → flex 로 되돌리고 오른쪽 끝에 */
  .topbar.settings .topbar-in{display:flex}
  .topbar.settings .bar-right{margin-left:auto}
}""")
io.open(P, "w", encoding="utf-8", newline="\n").write(s); print("p8_n ok")
