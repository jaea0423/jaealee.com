# -*- coding: utf-8 -*-
"""v4 6차-H — 재아 검토 3
   · 잠정 = 색이 아니라 **빗금 무늬 + 점선 테두리**. 바탕색은 상태 그대로(확정 먹색 / 경고 벽돌) →
     확정·잠정·경고·변동(파란 칩)이 전부 다른 방식이라 셋이 겹쳐도 다 읽힙니다
   · 영업시간 줄을 그래프 카드에서 빼서 그 아래 별도 카드(.hours-card)로"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

H  = "repeating-linear-gradient(-45deg, rgba(255,255,255,.34) 0 4px, transparent 4px 10px)"   # 어두운 바탕용 흰 빗금
HP = "repeating-linear-gradient(-45deg, rgba(0,0,0,.13) 0 4px, transparent 4px 10px)"          # 지난(밝은 회색) 바탕용 검은 빗금

# ---- 5구역 ----
rep("""/* 예약 블록 — 확정은 먹색(#3A3833), 지난 것은 회색, 잠정은 빗금 테두리, 경고는 벽돌색 */""",
    """/* 예약 블록 — 확정은 먹색(#3A3833), 지난 것은 회색, 경고는 벽돌색.
   잠정은 색이 아니라 **빗금 무늬 + 점선 테두리** (6차-H). 바탕색은 상태 그대로라 '먹색+빗금 = 잠정 확정', '벽돌+빗금 = 잠정 경고'.
   그래서 background 는 반드시 background-color 로 씁니다 — 단축 속성은 빗금(background-image)을 지웁니다 */""")
rep(""".blk.tent{background:#8C8067; border:1px dashed #EFE7D5}
.blk.past{background:#B9B5AC}
.blk.past.tent{background:#BDB6A6}""",
""".blk.tent{background-image:%s; border:1px dashed rgba(255,255,255,.75)}
.blk.past{background-color:#B9B5AC}
.blk.past.tent{background-color:#B9B5AC; background-image:%s}""" % (H, HP))
rep("""/* 확정 / 잠정 / 경고를 구분해서 보여줍니다
   잠정 = 빗금 테두리, 경고 = 붉은색, 둘 다면 붉은색 + 빗금 테두리 */
button.blk.warned{border-color:rgba(255,255,255,.45); background:var(--rust)}
button.blk.warned.past{background:#C08476}
button.blk.tent.warned{background:var(--rust); border:1px dashed #FFE2DA}
button.blk.tent{background:#8E8A80; border:1px dashed #E7E3DA}""",
"""/* 확정 / 잠정 / 경고를 구분해서 보여줍니다
   잠정 = 빗금 무늬 + 점선 테두리, 경고 = 붉은색, 둘 다면 붉은색 위에 빗금 */
button.blk.warned{border-color:rgba(255,255,255,.45); background-color:var(--rust)}
button.blk.warned.past{background-color:#C08476}
button.blk.tent.warned{background-color:var(--rust); background-image:%s; border:1px dashed #FFE2DA}
button.blk.tent{background-image:%s; border:1px dashed rgba(255,255,255,.75)}""" % (H, H))
rep(""".lgsw.tent{background:#8E8A80; border:1px dashed #E7E3DA}""",
    """.lgsw.tent{background-color:#2C2C2E; background-image:%s; border:1px dashed rgba(255,255,255,.75)}   /* 먹색 + 빗금 = 잠정 */""" % H)
# ---- 9구역(한옥 테마) ----
rep(""".blk, .lgsw.ok{background:#2C2C2E}
.blk.past{background:#C7C7CC}
.blk.past.tent{background:#D1D1D6}""",
""".blk, .lgsw.ok{background-color:#2C2C2E}
.blk.past{background-color:#C7C7CC}
.blk.past.tent{background-color:#C7C7CC; background-image:%s}""" % HP)

# ---- 영업시간 카드 ----
rep("""      ${hoursLineHtml(dh)}
      <div class="tl-legends">""",
"""      <div class="tl-legends">""")
rep("""    <div class="card"><div class="card-b">${renderTimeline(d)}</div></div>
    ${metrics}""",
"""    <div class="card"><div class="card-b">${renderTimeline(d)}</div></div>
    <section class="card hours-card">${hoursLineHtml(hoursFor(d))}</section>
    ${metrics}""")
rep(""".tl-top .hours-line{margin-bottom:0}   /* .tl-top 은 gap 으로 간격을 잡으므로 여기서는 아래 여백 없이 */""",
    """/* 대시보드에서는 그래프 카드 아래 별도 카드(6차-H). 카드가 곧 상자라 안쪽 회색 바탕은 뺍니다 */
.hours-card{padding:var(--s4) var(--s8)}
.hours-card .hours-line{margin:0; background:transparent}""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_h ok")
