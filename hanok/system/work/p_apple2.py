# -*- coding: utf-8 -*-
"""apple-design 2차 손보기 (2026-09-20) — 09-07 v3 개편 뒤에 늘어난 화면(사장님·설정 목록·워크시프트·감사 문자…)이
   토큰·계단에서 벗어난 곳을 되돌리고, apple-design 규칙 중 아직 없던 것(끌어서 닫기·스크롤 가장자리·손잡이)을 더합니다.

   1) 색 — 경고·주의·강조의 '옅은 테두리' 색을 토큰(--rust-line --amber-line --pine-line)으로. 따뜻한 팔레트 시절의 #EFD3CC 같은 값이
      중성 회색 팔레트 위에 그대로 남아 있었습니다. 이제 테마가 바뀌면 같이 바뀝니다
   2) 굵기 — 800/900 → 700 (두 단만: 600·700). 잠금 화면 명조 로고 글자(.pdot)는 글꼴 자체가 900 이라 그대로
   3) 글자 크기 — 계단 밖(9·10·12·12.5px) → 11·13. 영수증(.rc-*, 인쇄물)·타임라인 칸 안의 작은 칩(높이가 정해진 곳)은 그대로
   4) 새 조각 12c-apple.css — 스크롤 가장자리·시트 손잡이·스위치형 토글·사장님 타일·누름 반응·움직임 줄이기
   5) 새 조각 15b-sheetdrag.js — 손가락 기기에서 시트를 끌어서 닫기(1:1 · 속도 이어받기 · 고무줄 · 스프링) + 스크롤 가장자리 표시
   python work/p_apple2.py
"""
import os, sys, io, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L

# ---------- 1) 옅은 테두리 색 토큰 ----------
L.rep_in("css/01-tokens.css",
  "  --rust:#9C3B27;        /* 경고 */\n  --rust-soft:#FAE9E5;\n",
  "  --rust:#9C3B27;        /* 경고 */\n  --rust-soft:#FAE9E5;\n"
  "  /* 옅은 바탕 위에 두르는 실선 — soft 보다 한 단 진한 같은 색. 예전엔 #EFD3CC 같은 값이 곳곳에 박혀 있어 테마를 바꿔도 안 따라왔습니다 */\n"
  "  --rust-line:#EFD3CC;  --amber-line:#EDDFBC;  --pine-line:#CDDFD8;\n")
L.rep_in("css/09-theme.css",
  "  --rust-soft:#FAE9E4;\n  --shadow:none;",
  "  --rust-soft:#FAE9E4;\n  --rust-line:#EBC9C1;  --amber-line:#E9DAB6;  --pine-line:#D8D8DD;   /* 중성 팔레트에 맞춘 옅은 실선 */\n  --shadow:none;")
LINE_MAP = {"#EFD3CC":"var(--rust-line)", "#EDDFBC":"var(--amber-line)", "#EBDCB6":"var(--amber-line)",
            "#CDDFD8":"var(--pine-line)", "#C9DED5":"var(--pine-line)"}
n_line = 0
for name in L.parts("css"):
    if name.endswith(("00-fonts.css","01-tokens.css","10-tv.css")): continue
    s = L.load(name); t = s
    for k, v in LINE_MAP.items(): t = t.replace(k, v)
    if t != s: n_line += sum(s.count(k) for k in LINE_MAP); L.save(name, t)
print("옅은 실선 토큰화:", n_line, "곳")

# ---------- 2) 굵기 두 단 ----------
n_w = 0
for name in L.parts("css") + L.parts("js"):
    if name.endswith(("00-fonts.css","10-tv.css","08-lock.css")): continue   # 글꼴 선언·TV·잠금 로고 글자는 예외
    s = L.load(name)
    t = re.sub(r"font-weight:\s*(800|900)\b", "font-weight:700", s)
    t = t.replace(".rc-h1{text-align:center; font-size:20px; font-weight:700", ".rc-h1{text-align:center; font-size:20px; font-weight:800")   # 영수증 제목은 인쇄물 — 원래대로
    t = t.replace(".rc-tot b{font-weight:700}", ".rc-tot b{font-weight:800}")
    if t != s: n_w += len(re.findall(r"font-weight:\s*(800|900)\b", s)); L.save(name, t)
print("굵기 800/900 → 700:", n_w, "곳")

# ---------- 3) 글자 크기 계단 ----------
SIZE_FIX = [
  ("css/03-parts.css", "font-size:10px; font-weight:700; letter-spacing:.04em; line-height:1.5; border:1px solid #B8860B", "font-size:var(--fs-label); font-weight:700; letter-spacing:.04em; line-height:1.5; border:1px solid #B8860B"),
  ("css/04-layout.css", "background:rgba(255,255,255,.14); font-size:12px; line-height:18px; text-align:center}", "background:rgba(255,255,255,.14); font-size:var(--fs-label); line-height:18px; text-align:center}"),
  ("css/07-settings.css", "border-radius:var(--r-sm); font-size:12px; color:var(--pine); cursor:pointer}", "border-radius:var(--r-sm); font-size:var(--fs-sub); color:var(--pine); cursor:pointer}"),
  ("css/07b-site.css", "font-size:12px; color:#8B8377; letter-spacing:.02em}", "font-size:var(--fs-sub); color:var(--text-3); letter-spacing:.02em}"),
  ("css/07c-staff.css", ".hr-grid thead th small{font-size:10px}", ".hr-grid thead th small{font-size:var(--fs-label)}"),
  ("css/07c-staff.css", ".hr-grid.week td.hc small{display:block; font-size:10px;", ".hr-grid.week td.hc small{display:block; font-size:var(--fs-label);"),
  ("css/07c-staff.css", "padding:1px 7px; font-size:10px; font-weight:700; color:var(--pine); cursor:pointer}", "padding:1px 7px; font-size:var(--fs-label); font-weight:700; color:var(--pine); cursor:pointer}"),
  ("css/11-media.css", ".ts-s{color:#8A857C; font-size:12.5px;", ".ts-s{color:#8A857C; font-size:var(--fs-sub);"),
]
for name, old, new in SIZE_FIX:
    cnt = L.load(name).count(old)
    if cnt: L.rep_in(name, old, new, cnt)
    else: print("!! 못 찾음:", name, old[:50])
print("글자 크기 계단 맞춤:", len(SIZE_FIX), "곳")

# ---------- 4) 새 CSS 조각 ----------
L.save("css/12c-apple.css", r'''/* ============================================================
   12c. apple-design 2차 (2026-09-20) — 12b 뒤·13 앞. 새 화면(사장님·설정 목록·워크시프트·감사 문자)이 생긴 뒤 다시 맞춘 것.
   규칙 출처는 .claude/skills/apple-design (WWDC '반응·직접 조작·중단 가능·재질·타이포').
   ============================================================ */

/* ---- 스크롤 가장자리 (§12 "1px 구분선 대신 내용이 떠 있는 틀과 만나는 곳만") ----
   맨 위에서는 상단바 밑선이 없고, 내용이 밑으로 흘러 들어가야 옅은 선 + 그림자가 생깁니다. body.scrolled 는 15b 가 켭니다 */
.topbar{transition:box-shadow .15s ease}
body.theme-hanok .topbar{border-bottom-color:transparent}
body.scrolled .topbar{box-shadow:0 1px 0 var(--topbar-line), 0 6px 20px rgba(0,0,0,.06)}
.wz-top{transition:box-shadow .15s ease; border-bottom-color:transparent}
.wz-top.scrolled{box-shadow:0 1px 0 var(--border), 0 6px 20px rgba(0,0,0,.06)}

/* ---- 시트 손잡이 (§2·§7 "어디를 잡는지 보이게") — 손가락 기기에서만. 15b 가 이 머리를 잡고 끌게 합니다 ---- */
@media (pointer:coarse){
  .overlay > .sheet{position:relative}
  .overlay > .sheet::before{content:""; position:absolute; top:6px; left:50%; width:36px; height:5px; margin-left:-18px; border-radius:3px; background:var(--border-strong)}
  .overlay > .sheet .sheet-h{touch-action:none; cursor:grab}   /* 머리에서는 세로 스크롤 대신 끌기 */
}
.sheet.dragging{overflow:hidden}   /* 끄는 동안 안쪽 스크롤이 같이 움직이지 않게 */

/* ---- 스위치형 토글 — 옛 '넓은 회색 상자'(설정 → 공휴일 운영시간 사용 등)를 알약 + 앞 점으로. 켜지면 점이 찹니다 ---- */
.togglebtn{display:inline-flex; align-items:center; gap:var(--s8); width:auto; padding:var(--s8) var(--s16) var(--s8) var(--s12); border-radius:980px; border-color:var(--border-strong); background:var(--surface); color:var(--text-2); font-weight:600}
.togglebtn::before{content:""; width:12px; height:12px; border-radius:50%; border:2px solid var(--border-strong); box-sizing:border-box; flex:none; transition:background .12s, border-color .12s}
.togglebtn.on{background:var(--surface); border-color:var(--text); color:var(--text)}
.togglebtn.on::before{background:var(--text); border-color:var(--text)}
.togglebtn.sa-off{border-color:var(--rust); color:var(--rust)}
.togglebtn.sa-off::before{background:var(--rust); border-color:var(--rust)}

/* ---- 사장님·설정 타일: 아이콘은 위, 이름은 아래 모서리에 (빈 자리가 '남은 공간'이 아니라 '여백'으로 읽히게) ---- */
.own-it{justify-content:space-between; min-height:104px; padding:var(--s16) var(--s16) var(--s12)}
.own-it svg{margin-bottom:0}
.own-it:active{filter:brightness(.94)}

/* ---- 누르는 순간 반응 (§1) — 03-parts 목록에 없던 새 부품 ---- */
.mk:not(.flat), .cd-v, .cd-n, .hr-grid td.hc, .hr-fill, .kwtag .x, .dq-img .x, .more-menu button, .own-it, .tl-name.foldable{-webkit-tap-highlight-color:transparent; transition:filter .08s}
.mk:not(.flat):active, .cd-v:active, .cd-n:active, .hr-grid td.hc:active, .hr-fill:active, .kwtag .x:active, .dq-img .x:active, .tl-name.foldable:active{filter:brightness(.9)}
@media (max-width:640px){ .mk{height:36px} }   /* 폰 지표 칩 34 → 36 (44 는 칩 줄이 두꺼워져 대신 위아래 여백으로 손가락 자리를 확보) */

/* ---- 움직임 줄이기 (§14) — 12-overrides 가 더한 더보기 메뉴·토스트·끌기 스프링까지 ---- */
@media (prefers-reduced-motion:reduce){
  .more-menu, .fold-b{animation:none}
  .toast{transition:none}
  .topbar, .wz-top, .togglebtn::before{transition:none}
}
''')

# ---------- 5) 새 JS 조각 ----------
L.save("js/15b-sheetdrag.js", r'''/* ============================================================
   시트 끌어서 닫기 + 스크롤 가장자리 표시 (apple-design 2차, 2026-09-20)
   ------------------------------------------------------------
   손가락 기기에서 시트 머리(.sheet-h)를 잡고 아래로 끌면 손가락에 1:1 로 붙어 따라오고(§2), 놓으면 손가락 속도를 그대로 이어받아(§5)
   '어디까지 갈지'를 속도로 미리 계산해(§6) 닫히거나 제자리로 돌아옵니다. 위로 끌면 고무줄처럼 버팁니다(§9).
   돌아오는 움직임은 임계 감쇠 스프링(튀지 않음, response .35s)이고 끄는 도중 다시 잡으면 그 자리에서 이어집니다(§3).
   왜 CSS transition 이 아닌가: transition 은 중간에 잡아 되돌릴 수 없고 속도를 이어받지 못합니다.
   닫기는 시트 바깥(.overlay)의 onclick 을 그대로 부릅니다 — 시트마다 닫는 함수가 달라도(closeSheet·closeCourse…) 그게 맞는 함수입니다.
   ============================================================ */
(function(){
  var D = null;                                   /* 진행 중인 끌기 */
  var REDUCE = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function sheetOf(t){
    if(!t || !t.closest) return null;
    if(t.closest("button, input, select, textarea, a, label")) return null;   /* 닫기 ×·입력칸은 제 일을 해야 함 */
    var h = t.closest(".sheet-h"); if(!h) return null;
    var s = h.closest(".sheet"); if(!s) return null;
    var ov = s.parentElement;
    if(!ov || !ov.classList.contains("overlay") || s.classList.contains("page-sheet")) return null;
    return s;
  }
  /* 화면 밖까지 거리. 폰(아래 붙음)이면 시트 높이, 태블릿(가운데)이면 시트 아래쪽 여백까지 더함 */
  function travel(s){ var r = s.getBoundingClientRect(); return Math.max(80, window.innerHeight - r.top); }
  /* 고무줄 — 경계를 넘을수록 덜 따라옵니다 (apple-design §9 의 식 그대로) */
  function rubber(over, dim, c){ c = c || 0.55; return (over * dim * c) / (dim + c * Math.abs(over)); }
  /* 놓았을 때 이 속도로 미끄러지면 어디서 멈추는지 (감속 .998 — 스크롤과 같은 느낌) */
  function project(v){ var d = 0.998; return (v / 1000) * d / (1 - d); }

  function velocity(hist){
    var now = performance.now(), i = hist.length - 1, j = i;
    while(j > 0 && now - hist[j-1][1] < 100) j--;   /* 마지막 100ms 만 */
    if(i === j) return 0;
    var dt = hist[i][1] - hist[j][1]; return dt > 0 ? (hist[i][0] - hist[j][0]) / dt * 1000 : 0;   /* px/s */
  }
  function apply(s, y){ s.style.transform = y ? "translateY(" + y.toFixed(1) + "px)" : ""; }

  /* 임계 감쇠 스프링 — from(현재값·현재속도)에서 target 으로. 매 프레임 적분, 다 오면 done() */
  function spring(s, state, target, done){
    var w = 2 * Math.PI / 0.35;                    /* response .35s */
    var last = performance.now();
    function tick(now){
      if(state.stop) return;
      var dt = Math.min(0.032, (now - last) / 1000); last = now;
      var a = -w * w * (state.y - target) - 2 * w * state.v;
      state.v += a * dt; state.y += state.v * dt;
      apply(s, state.y);
      if(Math.abs(state.y - target) < 0.5 && Math.abs(state.v) < 20){ state.y = target; apply(s, target); done && done(); return; }
      state.raf = requestAnimationFrame(tick);
    }
    state.raf = requestAnimationFrame(tick);
  }

  document.addEventListener("pointerdown", function(e){
    if(e.pointerType === "mouse") return;          /* 마우스는 × 로 — 끌기는 손가락·펜만 */
    var s = sheetOf(e.target); if(!s) return;
    /* 되돌아가는 중이면 그 자리에서 이어받습니다 (§3 중단 가능) */
    var y0 = 0, v0 = 0;
    if(s.__drag){ s.__drag.stop = true; cancelAnimationFrame(s.__drag.raf); y0 = s.__drag.y; v0 = s.__drag.v; }
    D = { s:s, id:e.pointerId, startY:e.clientY, base:y0, y:y0, v:v0, hist:[[e.clientY, performance.now()]], h:travel(s) };
    s.__drag = D;
    s.style.animation = "none"; s.style.willChange = "transform"; s.classList.add("dragging");
    try{ s.setPointerCapture(e.pointerId); }catch(_){}
  }, true);

  document.addEventListener("pointermove", function(e){
    if(!D || e.pointerId !== D.id) return;
    var dy = D.base + (e.clientY - D.startY);
    D.y = dy < 0 ? rubber(dy, D.h) : dy;           /* 위로는 고무줄, 아래로는 1:1 */
    D.hist.push([e.clientY, performance.now()]); if(D.hist.length > 12) D.hist.shift();
    apply(D.s, D.y);
    if(e.cancelable) e.preventDefault();
  }, {passive:false, capture:true});

  function release(e){
    if(!D || e.pointerId !== D.id) return;
    var d = D; D = null;
    var s = d.s; s.classList.remove("dragging");
    if(!s.isConnected) return;                     /* 끄는 사이 화면이 다시 그려졌으면 그만 */
    d.v = velocity(d.hist);
    var landing = d.y + project(d.v);              /* 속도로 본 도착점 (§6) */
    var close = e.type !== "pointercancel" && (landing > d.h * 0.5 || d.v > 900);
    var target = close ? d.h + 24 : 0;
    var ov = s.parentElement;
    var finish = function(){
      s.style.willChange = "";
      if(close){ if(ov && ov.isConnected) ov.click(); }   /* 시트 바깥 클릭 = 그 시트의 닫기 */
      else { apply(s, 0); s.__drag = null; }
    };
    if(REDUCE){ d.y = target; apply(s, target); finish(); return; }
    /* 스프링은 현재 속도를 이어받습니다 (§5). 닫힐 때는 조금 더 빠르게(response 는 같고 거리만 김) */
    spring(s, d, target, finish);
  }
  document.addEventListener("pointerup", release, true);
  document.addEventListener("pointercancel", release, true);

  /* ---- 스크롤 가장자리: 맨 위에서는 밑선 없음, 내려가면 12c 가 그림자를 그립니다 ---- */
  var scrolledTimer = null;
  function onScroll(e){
    if(e.target === document || e.target === document.documentElement || e.target === document.body){
      var on = (window.scrollY || document.documentElement.scrollTop) > 2;
      if(document.body.classList.contains("scrolled") !== on) document.body.classList.toggle("scrolled", on);
      return;
    }
    var el = e.target;
    if(el.classList && el.classList.contains("wz-mid")){
      var top = el.previousElementSibling;
      if(top && top.classList.contains("wz-top")) top.classList.toggle("scrolled", el.scrollTop > 2);
    }
  }
  document.addEventListener("scroll", onScroll, {passive:true, capture:true});
})();
''')
print("새 조각: css/12c-apple.css, js/15b-sheetdrag.js")
