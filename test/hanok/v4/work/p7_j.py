# -*- coding: utf-8 -*-
"""6차-J — 예약률 시트 제목의 기간이 14일(d−13~d)인데 그래프는 21일치(rateChart(d,21))였음 → 21일로 맞춤"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
old = """      <span class="muted" style="flex:1; text-align:center; font-size:13px">${dateLabel(shiftDate(d,-13))} – ${dateLabel(d)}</span>"""
new = """      <span class="muted" style="flex:1; text-align:center; font-size:13px">${dateLabel(shiftDate(d,-20))} – ${dateLabel(d)}</span>   <!-- 그래프가 21일치(rateChart(d,21))라 첫날은 d−20 -->"""
assert s.count(old) == 1
io.open(P, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))
print("p7_j ok")
