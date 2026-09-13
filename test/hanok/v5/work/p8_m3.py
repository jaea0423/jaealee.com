# -*- coding: utf-8 -*-
"""7차-M 보강 2 — PC 지표 카드 셋째 줄(부연) 삭제 · 폰 스위치 '리스트|그래프' → '목록|타임라인'"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

rep("""        <div class="metric"><div class="v">${active.length}<span class="u">건</span></div>
          <div class="k">확정 예약</div><div class="s">${people}명 · 좌석 ${seatUse}개</div></div>
        <div class="metric"><div class="v">${stat.rate}<span class="u">%</span></div>
          <div class="k">예약률</div><div class="s">좌석 ${seatUse}/${stat.seatAll} 사용</div></div>
        <button class="metric tapm ${unassigned?'warn':''}" onclick="openUnassigned()">
          <div class="v">${unassigned}<span class="u">건</span></div>
          <div class="k">룸 미배정</div><div class="s">${unassigned?"눌러서 열기":"모두 배정됨"}</div></button>
        <button class="metric tapm ${warnCnt?'warn':''}" onclick="openPick('warn')">
          <div class="v">${warnCnt}<span class="u">건</span></div>
          <div class="k">경고 예약</div><div class="s">${warnCnt?"눌러서 열기":"이상 없음"}</div></button>
        <button class="metric tapm ${checkCnt?'amber':''}" onclick="openCheck()">
          <div class="v">${checkCnt}<span class="u">건</span></div>
          <div class="k">확인 필요</div><div class="s">${checkCnt?"눌러서 열기":"모두 확인됨"}</div></button>""",
"""        <!-- 셋째 줄(부연·'눌러서 열기')은 7차-M 에서 뺐습니다 — 두 줄이면 충분하고 카드가 낮아집니다 -->
        <div class="metric"><div class="v">${active.length}<span class="u">건</span></div>
          <div class="k">확정 예약</div></div>
        <div class="metric"><div class="v">${stat.rate}<span class="u">%</span></div>
          <div class="k">예약률</div></div>
        <button class="metric tapm ${unassigned?'warn':''}" onclick="openUnassigned()">
          <div class="v">${unassigned}<span class="u">건</span></div>
          <div class="k">룸 미배정</div></button>
        <button class="metric tapm ${warnCnt?'warn':''}" onclick="openPick('warn')">
          <div class="v">${warnCnt}<span class="u">건</span></div>
          <div class="k">경고 예약</div></button>
        <button class="metric tapm ${checkCnt?'amber':''}" onclick="openCheck()">
          <div class="v">${checkCnt}<span class="u">건</span></div>
          <div class="k">확인 필요</div></button>""")
rep("""          <span class="${view.mView==='graph'?'':'on'}">리스트</span><span class="${view.mView==='graph'?'on':''}">그래프</span>""",
    """          <span class="${view.mView==='graph'?'':'on'}">목록</span><span class="${view.mView==='graph'?'on':''}">타임라인</span>""")
rep("""aria-label="리스트/그래프 전환">""", """aria-label="목록/타임라인 전환">""")
rep("""  /* 리스트 | 그래프 스위치 — 로고 옆, 알약 두 칸. 켜진 쪽이 먹색 */""",
    """  /* 목록 | 타임라인 스위치 — 로고 옆, 알약 두 칸. 켜진 쪽이 먹색 */""")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_m3 ok")
