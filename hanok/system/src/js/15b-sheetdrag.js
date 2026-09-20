/* ============================================================
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
    /* 화면 주사(rAF)에 맞춰 돌리되, 탭이 가려져 rAF 가 멈추면 80ms 뒤 타이머가 대신 이어 갑니다 — 멈춘 채 남지 않게 */
    function next(){ state.raf = requestAnimationFrame(tick); state.tmo = setTimeout(function(){ tick(performance.now()); }, 80); }
    function tick(now){
      cancelAnimationFrame(state.raf); clearTimeout(state.tmo);
      if(state.stop) return;
      var dt = Math.min(0.25, Math.max(0.001, (now - last) / 1000)); last = now;
      /* 프레임이 늦게 와도(탭이 가려짐·느린 기기) 8ms 씩 잘게 나눠 적분 — 한 걸음이 크면 감쇠항(2w·dt > 1)이 뒤집혀 튀어 나갑니다 */
      var n = Math.ceil(dt / 0.008), h = dt / n;
      for(var i = 0; i < n; i++){
        var a = -w * w * (state.y - target) - 2 * w * state.v;
        state.v += a * h; state.y += state.v * h;
      }
      apply(s, state.y);
      if(Math.abs(state.y - target) < 0.5 && Math.abs(state.v) < 20){ state.y = target; apply(s, target); done && done(); return; }
      next();
    }
    next();
  }

  document.addEventListener("pointerdown", function(e){
    if(e.pointerType === "mouse") return;          /* 마우스는 × 로 — 끌기는 손가락·펜만 */
    var s = sheetOf(e.target); if(!s) return;
    /* 되돌아가는 중이면 그 자리에서 이어받습니다 (§3 중단 가능) */
    var y0 = 0, v0 = 0;
    if(s.__drag){ s.__drag.stop = true; cancelAnimationFrame(s.__drag.raf); clearTimeout(s.__drag.tmo); y0 = s.__drag.y; v0 = s.__drag.v; }
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
