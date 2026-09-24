/* 같은 줄 높이 검사 — 브라우저 콘솔(또는 자동화)에서 돌립니다. 09-24 재아 "높이 안 맞는 게 계속 나온다, 말하기 전에 잡아라".
   화면에 보이는 입력칸·단추(input·select·button·.btn·.sa-pick)를 부모(가로 flex/grid)별로 묶고, 세로로 겹치는 것끼리
   높이 차이가 2px 넘으면 적어 냅니다. 사진(.sa-thumb)·여러 줄 칸(textarea)·체크박스는 뺌.
   사용: auditRows(document.getElementById("app")) → [{where, heights, texts}] */
function auditRows(root){
  var sel = 'input:not([type=checkbox]):not([type=radio]):not([type=hidden]), select, button:not(.ibtn), a.btn, .sa-pick';
  var els = Array.prototype.slice.call(root.querySelectorAll(sel)).filter(function(el){
    if(!el.offsetParent) return false;
    var r = el.getBoundingClientRect(); if(r.width < 4 || r.height < 4) return false;
    if(el.closest(".pkeys, .pk-grid, .tl, .tl-scroll, .sa-tabs, .seg, .rrow, .srow, .own-grid, .hr-grid, .cgrid, .modal .md-b, .tap-plain, .rowitem > .grow")) return false;   /* 격자·표·탭은 제외(칸 모양이 원래 다름) */
    return true;
  });
  var groups = new Map();
  els.forEach(function(el){
    /* 5단계 위까지 올라가며 '가로 줄' 상자 중 가장 바깥 것을 씀 — 줄 안에 작은 줄이 또 있으면(사진 칸 + 화살표 묶음) 따로 재서 놓쳤음 */
    var p = el.parentElement, depth = 0, best = null;
    while(p && depth < 5 && p !== root){ var cs = getComputedStyle(p); if((cs.display.indexOf("flex") >= 0 && cs.flexDirection.indexOf("row") === 0) || cs.display.indexOf("grid") >= 0) best = p; p = p.parentElement; depth++; }
    p = best; if(!p) return;
    if(!groups.has(p)) groups.set(p, []);
    groups.get(p).push(el);
  });
  var out = [];
  groups.forEach(function(list, p){
    if(list.length < 2) return;
    /* 세로로 겹치는 것끼리(같은 줄) */
    var rows = [];
    list.forEach(function(el){ var r = el.getBoundingClientRect(), row = rows.find(function(x){ return r.top < x.bottom && r.bottom > x.top; }); if(row){ row.els.push(el); row.top = Math.min(row.top, r.top); row.bottom = Math.max(row.bottom, r.bottom); } else rows.push({top:r.top, bottom:r.bottom, els:[el]}); });
    rows.forEach(function(row){
      if(row.els.length < 2) return;
      var hs = row.els.map(function(el){ return Math.round(el.getBoundingClientRect().height); });
      var tops = row.els.map(function(el){ return Math.round(el.getBoundingClientRect().top); });
      if(Math.max.apply(null, hs) - Math.min.apply(null, hs) > 2 || Math.max.apply(null, tops) - Math.min.apply(null, tops) > 2){
        out.push({ where:(p.className || p.tagName).toString().slice(0, 60), heights:hs.join("/"), tops:tops.join("/"), texts:row.els.map(function(el){ return (el.value || el.textContent || el.placeholder || el.tagName).trim().slice(0, 10); }).join(" | ") });
      }
    });
  });
  return out;
}
