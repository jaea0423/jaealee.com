# -*- coding: utf-8 -*-
"""6차 묶음 E 보강 — delRes 가 수정 시트에서 불렸을 때 history 칸 회수 (상세 시트에서 지운 경우는 state 가 없어 아무 일도 안 함)"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
old = """  if(rec) reflowTentatives(rec.date);
  view.form=null; tmpRes=null; saveData(); render();
}"""
new = """  if(rec) reflowTentatives(rec.date);
  view.form=null; tmpRes=null; saveData(); render(); histPop();
}"""
assert s.count(old) == 1, s.count(old)
s = s.replace(old, new)
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_e2 ok")
