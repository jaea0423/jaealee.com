# -*- coding: utf-8 -*-
"""재아 요청(2026-09-17): 타임라인 라벨은 그래프 안에만.
   · 사용 중지 — 좌석 이름 칸에 안 적고 빗금 위에만. 자리: 빗금 왼쪽 → 거기 예약이 있으면 오른쪽 → 그래도 있으면 그 줄 위에 층을 하나 더 만들어 거기
   · 자리 없음 — 같은 규칙. 초과 팀이 여럿이면 포개지 않고 팀마다 층을 하나씩 쌓음(3팀 = 3층)
   자리 판단은 그린 뒤 실제 픽셀로(tlPlaceLabels) — 글자 폭을 분 단위로 어림하면 폰·PC 가 달라 틀립니다 """
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep

s = load("js/10-timeline.js")
# 좌석 이름 칸의 사용 중지 표시 제거
s = rep(s, '''      <div class="tl-name"><b>${esc(room.name)}</b><small>${sub}</small>${blockTag(room)}</div>''',
           '''      <div class="tl-name"><b>${esc(room.name)}</b><small>${sub}</small></div>''', 1)
s = rep(s, '''  /* 좌석 이름 칸에 붙는 사용 중지 요약 — 빗금 위 글자가 예약에 가려도 여기서는 보입니다 */
  const blockTag = (seat)=>{''', '''  /* (안 씀 — 사용 중지는 빗금 위에만 적습니다. 자리는 tlPlaceLabels 가 그린 뒤 정함) */
  const blockTag = (seat)=>{''', 1)
# 초과 팀: 팀마다 층 하나씩(포개지 않게). extraLane 대신 lanes + k
s = rep(s, '''    const over = placed.filter(x=>x.lane===null).length;
    /* 자리를 못 받은 팀(테이블 수보다 팀이 많음)은 다른 블록 위에 겹쳐 그리지 않고 **맨 위에 칸을 하나 더** 만들어 넣습니다.
       그 칸은 블록 자리 말고는 영업 종료 빗금으로 채워 '정상 칸이 아니다' 가 보이게 (재아) */
    const extraLane = over ? lanes : -1;
    const totalLanes = lanes + (over ? 1 : 0);''',
'''    const over = placed.filter(x=>x.lane===null).length;
    /* 자리를 못 받은 팀(테이블 수보다 팀이 많음)은 다른 블록 위에 겹쳐 그리지 않고 **맨 위에 칸을 더** 만들어 넣습니다.
       팀마다 한 칸씩 — 둘이면 두 칸(포개면 뒤 팀이 안 보임, 재아). 그 칸은 영업 종료 빗금으로 채워 '정상 칸이 아니다' 가 보이게 */
    let overK = 0; placed.forEach(x=>{ if(x.lane===null){ x.overLane = lanes + overK; overK++; } });
    const totalLanes = lanes + over;''', 1)
s = rep(s, '''      const w = ((it.e0-it.s0)/span)*100, lane = it.lane===null?extraLane:it.lane;''',
           '''      const w = ((it.e0-it.s0)/span)*100, lane = it.lane===null?it.overLane:it.lane;''', 1)
s = rep(s, '''      + (over ? `<div class="offband overlane" style="left:0; right:0; top:0; height:${LANE}px" title="테이블 수를 넘은 팀이 놓이는 칸"><i class="ol-l">자리 없음 ${over}팀 — 테이블 수를 넘은 예약</i></div>` : "");''',
           '''      + (over ? `<div class="offband overlane" style="left:0; right:0; top:0; height:${over*LANE}px" title="테이블 수를 넘은 팀이 놓이는 칸"><i class="ol-l tl-lbl">자리 없음 ${over}팀 — 테이블 수를 넘은 예약</i></div>` : "");''', 1)
s = rep(s, '''<i class="bb-l">${esc(blockLabelText(sp.blk))}</i></span>`;''', '''<i class="bb-l tl-lbl">${esc(blockLabelText(sp.blk))}</i></span>`;''', 1)
# 그린 뒤 라벨 자리 정하기
s += '''
/* ---------- 라벨 자리 정하기 (그린 뒤, 실제 픽셀로) ----------
   사용 중지·자리 없음 글자는 그래프 안에만 둡니다(좌석 이름 칸·예약률 칸에는 안 적음 — 재아).
   자리: 띠의 왼쪽 → 거기에 예약 블록이 겹치면 오른쪽 → 그래도 겹치면 그 줄 위에 층(LANE)을 하나 더 만들어 거기에.
   블록은 bottom 기준으로 놓여 있어 트랙 높이를 늘리면 위에 빈 층이 생깁니다. */
function tlPlaceLabels(){
  var tracks = document.querySelectorAll(".tl-track");
  for(var t = 0; t < tracks.length; t++){
    var track = tracks[t], labels = track.querySelectorAll(".tl-lbl");
    if(!labels.length) continue;
    var blocks = Array.prototype.slice.call(track.querySelectorAll(".blk")).map(function(b){ return b.getBoundingClientRect(); });
    var raised = false;
    for(var i = 0; i < labels.length; i++){
      var el = labels[i];
      el.classList.remove("right", "above");
      if(!tlLabelHits(el, blocks)) continue;
      el.classList.add("right");
      if(!tlLabelHits(el, blocks)) continue;
      el.classList.remove("right"); el.classList.add("above");
      if(!raised){   /* 위에 층 하나 — 같은 줄의 라벨 여럿이면 한 층을 같이 씀 */
        raised = true;
        var lane = parseInt(track.getAttribute("data-lane") || "21", 10);
        track.style.height = (track.offsetHeight + lane) + "px";
        var rate = track.parentNode.querySelector(".tl-rate"); if(rate) rate.style.height = track.style.height;
        var ol = track.querySelector(".overlane"); if(ol) ol.style.height = (ol.offsetHeight + lane) + "px";   /* 초과 칸 빗금도 새 층까지 */
      }
    }
  }
}
function tlLabelHits(el, blocks){
  var r = el.getBoundingClientRect();
  for(var i = 0; i < blocks.length; i++){
    var b = blocks[i];
    if(r.left < b.right - 1 && r.right > b.left + 1 && r.top < b.bottom - 1 && r.bottom > b.top + 1) return true;
  }
  return false;
}
'''
# 트랙에 층 높이를 실어 둠(위에 층 더할 때 씀)
s = rep(s, '''      <div class="tl-track" style="height:${lanes*LANE}px">
        ${layers}${blockBands(room)}${blocks}
      </div>''', '''      <div class="tl-track" data-lane="${LANE}" style="height:${lanes*LANE}px">
        ${layers}${blockBands(room)}${blocks}
      </div>''', 1)
s = rep(s, '''      <div class="tl-track" style="height:${totalLanes*LANE}px; background-image:''', '''      <div class="tl-track" data-lane="${LANE}" style="height:${totalLanes*LANE}px; background-image:''', 1)
save("js/10-timeline.js", s)

s = load("js/04-render.js")
s = rep(s, '''  syncHash();      /* 주소를 지금 화면에 맞춥니다 — 새로고침해도 그 자리로 */
  afterRender();   /* 화면을 그린 뒤 필요한 이벤트 연결 (분 조절 레일 등) */
}''', '''  syncHash();      /* 주소를 지금 화면에 맞춥니다 — 새로고침해도 그 자리로 */
  afterRender();   /* 화면을 그린 뒤 필요한 이벤트 연결 (분 조절 레일 등) */
  if(typeof tlPlaceLabels === "function") tlPlaceLabels();   /* 타임라인 라벨(사용 중지·자리 없음) 자리 — 실제 픽셀로 겹침을 보고 정함 */
}''', 1)
save("js/04-render.js", s)

s = load("css/05-dash.css")
s = rep(s, '''.overlane .ol-l{position:absolute; left:6px; top:2px; font-style:normal; font-size:11px; font-weight:700; color:var(--rust); background:rgba(255,255,255,.92); padding:0 6px; border-radius:3px; white-space:nowrap; pointer-events:none; z-index:6}   /* 초과 블록이 그 칸 왼쪽에 놓여도 라벨은 위에 보이게(재아). 층 이름 칸에도 같은 글이 있음 */''',
'''.overlane .ol-l{position:absolute; left:6px; top:2px; font-style:normal; font-size:11px; font-weight:700; color:var(--rust); background:rgba(255,255,255,.92); padding:0 6px; border-radius:3px; white-space:nowrap; pointer-events:none; z-index:6}
/* 라벨 자리(tlPlaceLabels): 기본 왼쪽 → 예약과 겹치면 오른쪽 → 그래도 겹치면 줄 위에 새로 생긴 층(맨 위) */
.tl-lbl.right{left:auto; right:6px}
.tl-lbl.above{left:6px; right:auto; top:auto; bottom:calc(100% + 2px)}
.overlane .tl-lbl.above{top:2px; bottom:auto}   /* 초과 칸은 트랙 맨 위에 붙어 있어, 늘어난 층이 곧 그 칸의 윗부분 */''', 1)
# 빗금 띠는 top:0 bottom:0 이라 트랙이 늘어나면 위 층까지 덮음 → 라벨 above 는 띠 밖(위)이 아니라 띠의 맨 위 층. blockband 도 같은 규칙
s = rep(s, '''.tl-lbl.above{left:6px; right:auto; top:auto; bottom:calc(100% + 2px)}''', '''.tl-lbl.above{left:6px; right:auto; top:2px}''', 1)
save("css/05-dash.css", s)
print("ok")
