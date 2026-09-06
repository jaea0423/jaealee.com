"""Phase 3-1 버튼 통일 — 구역 파일을 고칩니다 (한 번만 실행).
 1) 3구역 맨 앞에 '누르는 것 공통' 블록: 최소 높이 44px, 누르는 순간 반응(:active), 탭 하이라이트 끄기
 2) 버튼류 반경을 --r-sm 으로 통일 (타일·달력 칸은 --r-md 유지)
"""
import os, re
Z = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zones")

def patch(fn, old, new, count=1):
    p = os.path.join(Z, fn); s = open(p, encoding="utf-8").read()
    assert old in s, (fn, old[:60])
    s = s.replace(old, new, count); open(p, "w", encoding="utf-8").write(s); print("ok", fn, old[:40])

SHARED = """/* ---------- 누르는 것 공통 (Phase 3-1) ----------
   카운터에서 손가락으로 쓰는 화면이라, 누를 수 있는 것은 전부 높이 44px 이상으로 둡니다 (애플 HIG 최소 터치 크기).
   누르는 순간 살짝 어두워져 '눌렸다'가 바로 보이게 합니다 — 지금까지는 :active 가 한 군데뿐이라 두 번 누르는 일이 생겼습니다.
   transform:scale 은 배율(zoom)과 부딪혀 화면이 잘리므로 쓰지 않고 filter 로만 합니다.
   ※ 타임라인 블록(button.blk)은 그래프 행 높이를 따르므로 44px 규칙에서 뺍니다. 작은 ± 버튼(.dcell button)은 36px. */
.btn, .topbar .tvbtn, .topbar .home, .storename, .bnav, .bdate,
.seg button, .filters button, .hourpick button, .wbtn, .numbtn, .numgrid button, .mfine button,
.markbtn, .sbtn, .spick, .nonebtn, .togglebtn, .pkey, .wz-back, .wz-dot,
.mo-h .nav, .datenav .nav, .res-head .nav, .cal-nav .nav, .sheet-h .x, .linkbtn, .lk-back{
  min-height:44px;
}
.bnav{min-width:36px}
.sheet-h .x{min-width:44px; display:inline-flex; align-items:center; justify-content:center}
.linkbtn, .lk-back{display:inline-flex; align-items:center}
.btn, .topbar .tvbtn, .topbar .home, .storename, .bnav, .bdate,
.seg button, .filters button, .hourpick button, .wbtn, .numbtn, .numgrid button, .numbig button, .bigstep button, .mfine button,
.markbtn, .sbtn, .spick, .nonebtn, .togglebtn, .pkey, .wz-back, .wz-dot,
.mo-h .nav, .datenav .nav, .res-head .nav, .cal-nav .nav, .sheet-h .x, .linkbtn, .lk-back, .dcell button,
.undecided, .pmore, .ptile, .scell, .hcell, .srccell, .citem, button.bday,
.rrow, .alert, button.metric, .fold-h, .tapzone, .bh-row, .smsrow, button.blk{
  -webkit-tap-highlight-color:transparent;
  transition:filter .08s ease-out;
}
.btn:active, .topbar .tvbtn:active, .topbar .home:active, .storename:active, .bnav:active, .bdate:active,
.seg button:active, .filters button:active, .hourpick button:active, .wbtn:active, .numbtn:active, .numgrid button:active, .numbig button:active, .bigstep button:active, .mfine button:active,
.markbtn:active, .sbtn:active, .spick:active, .nonebtn:active, .togglebtn:active, .pkey:active, .wz-back:active, .wz-dot:active,
.mo-h .nav:active, .datenav .nav:active, .res-head .nav:active, .cal-nav .nav:active, .sheet-h .x:active, .linkbtn:active, .lk-back:active, .dcell button:active,
.undecided:active, .pmore:active, .ptile:active, .scell:active, .hcell:active, .srccell:active, .citem:active, button.bday:active,
.rrow:active, .alert:active, button.metric:active, .fold-h:active, .tapzone:active, .bh-row:active, .smsrow:active, button.blk:active{
  filter:brightness(.9);
}

"""
patch("3.css", "/* ---------- 버튼 ----------", SHARED + "/* ---------- 버튼 ----------")
# 반경 통일: 버튼은 --r-sm. (달력 칸 button.bday, 인원 타일 등 '타일'은 --r-md 그대로)
patch("3.css", ".btn.lg{padding:var(--s16) var(--s24); font-size:var(--fs-title); border-radius:var(--r-md)}",
               ".btn.lg{padding:var(--s16) var(--s24); font-size:var(--fs-title); border-radius:var(--r-sm)}")
for fn, sel in (("4.css", ".topbar .tvbtn{"), ("4.css", ".datenav .nav{"), ("6.css", ".mo-h .nav{")):
    p = os.path.join(Z, fn); s = open(p, encoding="utf-8").read()
    i = s.index(sel); j = s.index("}", i)
    block = s[i:j]
    assert "var(--r-md)" in block, (fn, sel)
    s = s[:i] + block.replace("var(--r-md)", "var(--r-sm)") + s[j:]
    open(p, "w", encoding="utf-8").write(s); print("ok", fn, sel, "→ --r-sm")
# .dcell button 은 22px → 36px (칩 안의 ± 버튼. 44 는 칩을 깨뜨림)
patch("7.css", ".dcell button{width:22px; height:22px;", ".dcell button{width:36px; height:36px;")
