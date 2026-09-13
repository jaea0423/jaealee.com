# -*- coding: utf-8 -*-
"""v4 5차 — 들어갈 때 인사(인트로) 재설계.
   붉은 중식당(歡迎光臨) → 한지·창살·낙관의 한옥(어서오세요).
   글자마다 화면을 통째로 다시 그리던 것을 멈추고(전환 효과가 전혀 안 돌았음),
   한 번 그린 뒤 클래스만 바꿔 CSS 전환이 실제로 재생되게 합니다."""
import re, io, sys
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()

def cut(s, start_marker, end_marker, new):
    a = s.index(start_marker); b = s.index(end_marker, a)
    assert s.count(start_marker) == 1, start_marker
    return s[:a] + new + s[b:]

# ---------- CSS ----------
CSS_NEW = r"""/* ------------------------------------------------------------
   들어갈 때 인사 — 중식당에서 한옥으로

   歡迎光臨(붉은 칠·금박) → 어서오세요(한지·먹·창살·낙관).
   · 배경은 두 겹을 겹쳐 두고 위(한옥)의 불투명도만 올립니다.
   · 글자는 먹이 종이에 스미듯 흐림(blur)에서 선명하게 나타납니다.
   · 양옆 띠살 창호와 한지 결(SVG 잡음)은 전부 CSS/데이터 URI — 이미지 파일 0개.
   · 마지막에 붉은 낙관(韓屋)이 찍히고 끝납니다.
   ※ 한 번 그린 뒤 클래스만 바꿉니다. innerHTML 을 다시 쓰면 전환이 전혀 재생되지 않습니다.
   ------------------------------------------------------------ */
.intro{position:fixed; top:0; right:0; bottom:0; left:0; z-index:200;
  display:flex; align-items:center; justify-content:center; overflow:hidden;
  background:#6E1A10; color:#F6E7C8; cursor:pointer}
.intro-bg{position:absolute; top:0; right:0; bottom:0; left:0; transition:opacity 1.1s ease}
/* 중식당 — 칠기 붉은색. 가운데는 살짝 밝고 가장자리는 어둡게(조명 아래 칠기) */
.intro-cn{
  background:
    radial-gradient(ellipse at 50% 46%, rgba(255,190,120,.10) 0%, rgba(0,0,0,0) 40%),
    radial-gradient(circle at 50% 50%, rgba(0,0,0,.02) 0%, rgba(0,0,0,.26) 56%, rgba(0,0,0,.62) 100%),
    repeating-linear-gradient(45deg,  rgba(255,213,150,.085) 0 2px, transparent 2px 30px),
    repeating-linear-gradient(-45deg, rgba(255,213,150,.085) 0 2px, transparent 2px 30px),
    linear-gradient(160deg, #8E2314 0%, #6E1A10 55%, #4E1109 100%);
}
/* 한옥 — 한지. 미색 바탕에 종이 결(SVG feTurbulence 를 아주 옅게 겹침) + 가운데 은은한 빛 */
.intro-ko{
  opacity:0;
  background:
    radial-gradient(ellipse at 50% 42%, rgba(255,255,255,.55) 0%, rgba(255,255,255,0) 58%),
    radial-gradient(circle at 50% 50%, rgba(80,56,30,0) 52%, rgba(80,56,30,.16) 100%),
    url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .45 0 0 0 0 .36 0 0 0 0 .24 0 0 0 .09 0'/%3E%3C/filter%3E%3Crect width='220' height='220' filter='url(%23n)'/%3E%3C/svg%3E"),
    linear-gradient(170deg, #F5EEE0 0%, #EFE5D2 60%, #E9DEC8 100%);
}
/* 띠살 창호 — 양옆에 한 짝씩. 세로살은 끝까지, 가로살은 위·가운데·아래 세 무리만(띠살의 특징).
   위→아래 순서: 세로살 / 가로살을 가리는 한지 띠 / 가로살 / 한지 바탕 */
.intro-sash{position:absolute; top:6vh; bottom:6vh; width:17vw; opacity:0; pointer-events:none;
  border:3px solid rgba(96,66,38,.78); box-shadow:0 0 0 1px rgba(96,66,38,.25), 0 18px 60px rgba(60,40,20,.18);
  background:
    repeating-linear-gradient(90deg, rgba(96,66,38,.72) 0 3px, transparent 3px 44px),
    linear-gradient(to bottom, transparent 0, transparent 21%, #F0E6D3 21%, #F0E6D3 44%, transparent 44%, transparent 56%, #F0E6D3 56%, #F0E6D3 79%, transparent 79%),
    repeating-linear-gradient(0deg, rgba(96,66,38,.72) 0 3px, transparent 3px 44px),
    #F0E6D3;
  transition:opacity 1.1s ease, transform 1.3s cubic-bezier(.2,.7,.2,1)}
.intro-sash.l{left:3vw;  transform:translateX(-6vw)}
.intro-sash.r{right:3vw; transform:translateX(6vw)}
.intro.turning .intro-sash{transform:translateX(0)}
/* 글자 — 두 낱말을 한 자리에 겹쳐 놓고 글자 단위로 바꿉니다 */
.intro-w{position:relative; font-family:var(--serif-tv); font-weight:900; line-height:1.1;
  font-size:clamp(40px,9vw,104px); letter-spacing:.16em; text-indent:.16em; width:100%; text-align:center}
.intro-word{display:block}
.intro-word.ko{position:absolute; top:0; left:0; width:100%}
.intro .ic{display:inline-block; transition:opacity .55s ease, filter .55s ease, transform .55s ease, color .8s ease}
/* 한자: 금박. 바탕이 한지로 바뀌면 남은 한자는 나무색으로 눌러 두었다가 흐려지며 사라집니다 */
.intro-word.cn .ic{color:#F1C77C; text-shadow:0 2px 18px rgba(0,0,0,.5), 0 0 2px rgba(255,236,190,.35)}
.intro.turning .intro-word.cn .ic{color:#9A6A3A; text-shadow:none}
.intro-word.cn .ic.off{opacity:0; filter:blur(8px); transform:scale(1.08)}
/* 한글: 먹. 흐림에서 선명하게 — 먹이 종이에 스미는 느낌 */
.intro-word.ko .ic{color:#241E1A; opacity:0; filter:blur(10px); transform:translateY(.06em) scale(1.06);
  text-shadow:0 0 1px rgba(36,30,26,.5)}
.intro-word.ko .ic.on{opacity:1; filter:blur(0); transform:none}
/* 낙관 — 붉은 사각 도장, 韓屋 두 줄. 글자 오른쪽 아래에 비스듬히 '찍힙니다' */
.intro-seal{position:absolute; right:calc(50% - 3.2em); bottom:-.62em; width:.78em; height:.78em;
  border:.045em solid #B5312A; border-radius:.03em .06em .03em .07em; color:#FBF3E6; background:#B5312A;
  box-shadow:inset 0 0 0 .025em #F4E6D4; font-size:inherit; line-height:1; font-weight:900;
  display:flex; align-items:center; justify-content:center; flex-direction:column; letter-spacing:0; text-indent:0;
  opacity:0; transform:rotate(-8deg) scale(1.6); transition:opacity .28s ease, transform .32s cubic-bezier(.2,.9,.2,1.15)}
.intro-seal span{display:block; font-size:.36em; line-height:1.02}
.intro-seal.on{opacity:.94; transform:rotate(-8deg) scale(1)}
/* 도장 아래 작은 상호 — 마지막에 낙관과 함께 떠오릅니다 */
.intro-sub{position:absolute; left:0; width:100%; top:1.32em; font-size:.22em; letter-spacing:.62em; text-indent:.62em;
  color:#6B5A48; font-weight:700; opacity:0; transform:translateY(.4em); transition:opacity .7s ease, transform .7s ease}
.intro-sub.on{opacity:1; transform:none}
/* 좁은 화면(폰): 창호는 접어 두고 낙관만 조금 안쪽으로 */
@media (max-width:640px){ .intro-sash{display:none} .intro-seal{right:calc(50% - 2.9em)} }
"""
s = cut(s, "/* ------------------------------------------------------------\n   들어갈 때 인사 — 중식당에서 한옥으로",
        "\n\n/* ============================================================\n   11. 반응형", CSS_NEW)

# ---------- JS ----------
JS_NEW = r"""/* ---------- 들어갈 때 인사 ----------
   PIN 을 맞히고 바로 화면이 튀어나오면 눌린 건지 아닌지 알기 어렵습니다.
   짧게(2초 안쪽) 인사를 띄워 '들어가는 중'이라는 감각을 줍니다.
   중식당이라 중국어(歡迎光臨)에서 한국어(어서오세요)로 글자가 하나씩 바뀌고,
   바탕은 붉은 칠기에서 한지·창살로, 마지막에 낙관이 찍힙니다.
   아무 데나 누르면 바로 건너뜁니다 — 바쁠 때 1초도 아깝습니다.
   ※ 글자가 바뀔 때마다 render() 로 화면을 다시 그리면 CSS 전환이 전혀 재생되지 않습니다
     (요소가 새로 만들어지니까). 처음 한 번만 그리고 그 뒤로는 클래스만 바꿉니다. */
var INTRO = null, introTimers = [];
var INTRO_FROM = "歡迎光臨";       /* 歡迎光臨 */
var INTRO_TO   = "어서오세요";  /* 어서오세요 */
function startIntro(){
  INTRO = { n:0 };
  clearIntro(true);
  render();                                   /* 한 번만 그립니다 */
  var steps = INTRO_TO.length, t0 = 320, gap = 135;
  for(var i=1;i<=steps;i++){
    introTimers.push(setTimeout((function(k){ return function(){ introStep(k); }; })(i), t0 + i*gap));
  }
  var tSeal = t0 + steps*gap + 260;
  introTimers.push(setTimeout(function(){ introSeal(); }, tSeal));
  introTimers.push(setTimeout(endIntro, tSeal + 1050));
}
function clearIntro(keepState){
  for(var i=0;i<introTimers.length;i++) clearTimeout(introTimers[i]);
  introTimers = [];
  if(!keepState) INTRO = null;
}
function endIntro(){ clearIntro(); INTRO = null; render(); }
/* k 번째 글자까지 바꿉니다. 화면을 다시 그리지 않고 클래스만 붙입니다 */
function introStep(k){
  if(!INTRO) return;
  INTRO.n = k;
  var root = document.querySelector(".intro");
  if(!root) return;
  root.className = "intro turning";
  var cn = root.querySelectorAll(".intro-word.cn .ic"), ko = root.querySelectorAll(".intro-word.ko .ic"), i;
  for(i=0;i<cn.length;i++) cn[i].className = "ic" + (i < k ? " off" : "");
  for(i=0;i<ko.length;i++) ko[i].className = "ic" + (i < k ? " on"  : "");
  /* 첫 글자가 바뀌는 순간 바탕도 함께 움직이기 시작하도록 조금 앞서 갑니다 */
  var p = Math.min(1, k / Math.max(1, INTRO_TO.length - 1)).toFixed(2);
  var bgs = root.querySelectorAll(".intro-ko, .intro-sash");
  for(i=0;i<bgs.length;i++) bgs[i].style.opacity = p;
}
function introSeal(){
  var seal = document.querySelector(".intro-seal"), sub = document.querySelector(".intro-sub");
  if(seal) seal.className = "intro-seal on";
  if(sub)  sub.className  = "intro-sub on";
}
/* 다른 이유로 render() 가 도중에 불려도 진행 중인 단계(INTRO.n)를 그대로 그립니다 */
function renderIntro(){
  var i, cn = "", ko = "", n = INTRO.n || 0;
  for(i=0;i<INTRO_FROM.length;i++) cn += '<span class="ic' + (i < n ? ' off' : '') + '">' + INTRO_FROM.charAt(i) + '</span>';
  for(i=0;i<INTRO_TO.length;i++)   ko += '<span class="ic' + (i < n ? ' on'  : '') + '">' + INTRO_TO.charAt(i) + '</span>';
  var p = n ? ' style="opacity:' + Math.min(1, n / Math.max(1, INTRO_TO.length - 1)).toFixed(2) + '"' : '';
  return '<div class="intro' + (n ? ' turning' : '') + '" onclick="endIntro()">' +
           '<div class="intro-bg intro-cn"></div>' +
           '<div class="intro-bg intro-ko"' + p + '></div>' +
           '<div class="intro-sash l"' + p + '></div><div class="intro-sash r"' + p + '></div>' +
           '<div class="intro-w">' +
             '<div class="intro-word cn">' + cn + '</div>' +
             '<div class="intro-word ko">' + ko + '</div>' +
             '<div class="intro-seal"><span>韓</span><span>屋</span></div>' +   /* 韓屋 */
             '<div class="intro-sub">한옥반점</div>' +                  /* 한옥반점 */
           '</div>' +
         '</div>';
}
"""
s = cut(s, "/* ---------- 들어갈 때 인사 ----------",
        "\n/* ============================================================\n   PIN 잠금", JS_NEW + "\n")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("ok", len(s))
