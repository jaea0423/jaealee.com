# -*- coding: utf-8 -*-
"""v4 6차 묶음 C (지시서 10) — 인트로: 글자 작게, 단계 느낌, 도장 삭제, 바탕 3단계(빨강 → 나무색 → 한지)"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---------- CSS ----------
rep("""   歡迎光臨(붉은 칠·금박) → 어서오세요(한지·먹·창살·낙관).
   · 배경은 두 겹을 겹쳐 두고 위(한옥)의 불투명도만 올립니다.
   · 글자는 먹이 종이에 스미듯 흐림(blur)에서 선명하게 나타납니다.
   · 양옆 띠살 창호와 한지 결(SVG 잡음)은 전부 CSS/데이터 URI — 이미지 파일 0개.
   · 마지막에 붉은 낙관(韓屋)이 찍히고 끝납니다.
""",
"""   歡迎光臨(붉은 칠·금박) → 어서오세요(한지·먹·창살).
   · 배경은 세 겹(붉은 칠 / 어두운 나무색 .intro-mid / 한지 .intro-ko)을 겹쳐 두고 글자 진행에 따라 위 두 겹의 불투명도를 올립니다.
     6차 전에는 빨강 → 한지 두 단계였는데 글자 5개가 1.3초에 걸쳐 바뀌므로 바탕도 중간 단계가 있어야 '단계'가 느껴집니다.
   · 글자는 먹이 종이에 스미듯 흐림(blur)에서 선명하게 나타납니다.
   · 양옆 띠살 창호와 한지 결(SVG 잡음)은 전부 CSS/데이터 URI — 이미지 파일 0개.
   · 6차에서 마지막 낙관(韓屋)·소제(한옥반점)는 조잡해서 뺐습니다. 마지막 장면은 어서오세요 + 창호만.
""")
rep(""".intro-bg{position:absolute; top:0; right:0; bottom:0; left:0; transition:opacity 1.1s ease}
""",
"""/* 바탕 전환은 글자 간격(260ms)보다 조금 길게 — 1.1s 는 마지막 글자 뒤 700ms 에 끝나는 인트로보다 늦게 끝났습니다 */
.intro-bg{position:absolute; top:0; right:0; bottom:0; left:0; transition:opacity .7s ease}
""")
rep("""/* 한옥 — 한지. 미색 바탕에 종이 결(SVG feTurbulence 를 아주 옅게 겹침) + 가운데 은은한 빛 */
.intro-ko{
""",
"""/* 중간 — 어두운 나무색(대들보). 빨강에서 한지로 곧장 가면 두 장면이라, 사이에 한 장면을 더 둡니다.
   사라지는 한자를 나무색(#9A6A3A)으로 누르는 규칙과도 어울립니다 */
.intro-mid{opacity:0; background:
    radial-gradient(ellipse at 50% 46%, rgba(120,90,60,.22) 0%, rgba(0,0,0,0) 45%),
    linear-gradient(165deg, #46332A 0%, #3A2A1E 55%, #2C1F16 100%)}
/* 한옥 — 한지. 미색 바탕에 종이 결(SVG feTurbulence 를 아주 옅게 겹침) + 가운데 은은한 빛 */
.intro-ko{
""")
rep("""  font-size:clamp(44px,10vw,104px); letter-spacing:.16em; text-indent:.16em; width:100%; text-align:center}""",
    """  font-size:clamp(36px,6.4vw,72px); letter-spacing:.16em; text-indent:.16em; width:100%; text-align:center}   /* 6차: 104px 는 너무 컸음 */""")
rep(""".intro .ic{display:inline-block; transition:opacity .55s ease, filter .55s ease, transform .55s ease, color .8s ease}""",
    """.intro .ic{display:inline-block; transition:opacity .7s ease, filter .7s ease, transform .7s ease, color .8s ease}   /* 글자 간격 260ms 에 맞춰 .55 → .7 */""")
rep("""/* 낙관 — 붉은 사각 도장, 韓屋 두 줄. 글자 오른쪽 아래에 비스듬히 '찍힙니다' */
.intro-seal{position:absolute; right:calc(50% - 3.2em); bottom:-.62em; width:.78em; height:.78em;
  border:.045em solid #B5312A; border-radius:.03em .06em .03em .07em; color:#FBF3E6; background:#B5312A;
  box-shadow:inset 0 0 0 .025em #F4E6D4; font-size:inherit; line-height:1; font-weight:900;
  display:flex; align-items:center; justify-content:center; flex-direction:column; letter-spacing:0; text-indent:0;
  opacity:0; transform:rotate(-8deg) scale(1.6); transition:opacity .28s ease, transform .32s cubic-bezier(.2,.9,.2,1.15)}
.intro-seal span{display:block; font-size:.36em; line-height:1.02}
.intro-seal.on{opacity:.94; transform:rotate(-8deg) scale(1)}
/* 도장 아래 작은 상호 — 마지막에 낙관과 함께 떠오릅니다 */
.intro-sub{position:absolute; left:0; width:100%; top:5.9em; font-size:.22em;  /* top 은 자기 글자 크기(.22em) 기준 → 부모 기준 약 1.3em */ letter-spacing:.62em; text-indent:.62em;
  color:#6B5A48; font-weight:700; opacity:0; transform:translateY(.4em); transition:opacity .7s ease, transform .7s ease}
.intro-sub.on{opacity:1; transform:none}
/* 좁은 화면(폰): 창호는 접어 두고 낙관만 조금 안쪽으로 */
@media (max-width:640px){ .intro-sash{display:none} .intro-seal{right:calc(50% - 2.9em)} }
""",
"""/* 좁은 화면(폰): 창호는 접어 둡니다 */
@media (max-width:640px){ .intro-sash{display:none} }
""")

# ---------- JS ----------
rep("""   중식당이라 중국어(歡迎光臨)에서 한국어(어서오세요)로 글자가 하나씩 바뀌고,
   바탕은 붉은 칠기에서 한지·창살로, 마지막에 낙관이 찍힙니다.""",
"""   중식당이라 중국어(歡迎光臨)에서 한국어(어서오세요)로 글자가 하나씩 바뀌고,
   바탕은 붉은 칠기 → 어두운 나무색 → 한지·창살 세 단계로 따라갑니다.""")
rep("""  var steps = INTRO_TO.length, t0 = 320, gap = 135;
  for(var i=1;i<=steps;i++){
    introTimers.push(setTimeout((function(k){ return function(){ introStep(k); }; })(i), t0 + i*gap));
  }
  var tSeal = t0 + steps*gap + 260;
  introTimers.push(setTimeout(function(){ introSeal(); }, tSeal));
  introTimers.push(setTimeout(endIntro, tSeal + 1050));
}""",
"""  /* 글자 5개가 260ms 간격(1.3초) — 6차 전(135ms)에는 거의 동시에 바뀌어 단계가 안 느껴졌습니다.
     마지막 글자 뒤 700ms 에 끝. 총 약 2.4초, 아무 데나 누르면 건너뜀 */
  var steps = INTRO_TO.length, t0 = 380, gap = 260;
  for(var i=1;i<=steps;i++){
    introTimers.push(setTimeout((function(k){ return function(){ introStep(k); }; })(i), t0 + i*gap));
  }
  introTimers.push(setTimeout(endIntro, t0 + steps*gap + 700));
}
/* 글자 진행 p(0~1)에 따른 바탕 두 겹의 불투명도 — 나무색은 앞 절반에서, 한지(와 창호)는 뒤 절반에서 올라옵니다 */
function introBg(n){
  var p = Math.min(1, n / Math.max(1, INTRO_TO.length - 1));
  return { mid: Math.min(1, p*2).toFixed(2), ko: Math.max(0, (p-.5)*2).toFixed(2) };
}""")
rep("""  /* 첫 글자가 바뀌는 순간 바탕도 함께 움직이기 시작하도록 조금 앞서 갑니다 */
  var p = Math.min(1, k / Math.max(1, INTRO_TO.length - 1)).toFixed(2);
  var bgs = root.querySelectorAll(".intro-ko, .intro-sash");
  for(i=0;i<bgs.length;i++) bgs[i].style.opacity = p;
}
function introSeal(){
  var seal = document.querySelector(".intro-seal"), sub = document.querySelector(".intro-sub");
  if(seal) seal.className = "intro-seal on";
  if(sub)  sub.className  = "intro-sub on";
}""",
"""  /* 첫 글자가 바뀌는 순간 바탕도 함께 움직이기 시작하도록 조금 앞서 갑니다 (k=1 에 나무색 절반, k=2 에 나무색 완성, k=3~4 에 한지) */
  var bg = introBg(k), mid = root.querySelector(".intro-mid"), kos = root.querySelectorAll(".intro-ko, .intro-sash");
  if(mid) mid.style.opacity = bg.mid;
  for(i=0;i<kos.length;i++) kos[i].style.opacity = bg.ko;
}""")
rep("""  var p = n ? ' style="opacity:' + Math.min(1, n / Math.max(1, INTRO_TO.length - 1)).toFixed(2) + '"' : '';
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
         '</div>';""",
"""  var bg = introBg(n);
  var pm = n ? ' style="opacity:' + bg.mid + '"' : '', pk = n ? ' style="opacity:' + bg.ko + '"' : '';
  return '<div class="intro' + (n ? ' turning' : '') + '" onclick="endIntro()">' +
           '<div class="intro-bg intro-cn"></div>' +
           '<div class="intro-bg intro-mid"' + pm + '></div>' +
           '<div class="intro-bg intro-ko"' + pk + '></div>' +
           '<div class="intro-sash l"' + pk + '></div><div class="intro-sash r"' + pk + '></div>' +
           '<div class="intro-w">' +
             '<div class="intro-word cn">' + cn + '</div>' +
             '<div class="intro-word ko">' + ko + '</div>' +
           '</div>' +
         '</div>';""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_c 적용 완료")
