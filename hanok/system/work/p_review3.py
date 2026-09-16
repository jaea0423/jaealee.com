# -*- coding: utf-8 -*-
"""재아 요청(2026-09-16 저녁):
   ① 설정에서 나가면 관리자 확인이 풀림 — 다시 들어갈 때 비밀번호를 또 묻게
   ② 타임라인 '자리 없음 N팀' 라벨이 초과 블록에 가려지지 않게(맨 위) + 층 이름 칸에도 표시
   ③ 사용 중지 표시를 '사용 중지 (사유 / 기간)' 으로 — 기간은 날짜(하루면 날짜 하나, 여러 날이면 시작 ~ 끝). '중지 2구간' 같은 말 없앰
   ④ 홈페이지 영업시간 글은 시스템과 연결하지 않고 직접 고치는 것으로 — 안내 문구 정리 """
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep

# ① 설정 나가면 관리자 확인 해제
s = load("js/06-modal.js")
s = rep(s, '''  if(t==="settings" && !view.adminOk){ if(!await adminGate("설정 열기")) return; view.adminOk = true; }''',
'''  if(t==="settings" && !view.adminOk){ if(!await adminGate("설정 열기")) return; view.adminOk = true; }
  /* 설정에서 나가면 관리자 확인도 풀립니다 — 다시 들어올 때 비밀번호를 또 묻게(재아). 홈페이지 관리도 설정 안에 있으니 같이 */
  if(view.tab==="settings" && t!=="settings") view.adminOk = false;''', 1)
save("js/06-modal.js", s)

# ③ 사용 중지 라벨 — 03-util 에 기간 표기 도우미
s = load("js/03-util.js")
s = rep(s, '''/* 그 날짜(·시각)에 사용 중지인지. time 을 주면 그 시각만, 안 주면 그 날 하루 중 일부라도 */''',
'''/* 그 날짜에 걸리는 사용 중지 항목(원본 block)들 — 라벨에 '기간' 을 적으려고. blockSpans 는 그 날의 분 구간만 주기 때문 */
function blocksOn(room, date){
  return roomBlocks(room).filter(function(b){ if(!b.from || date < b.from) return false; if(!b.openEnded && b.to && date > b.to) return false; return true; });
}
/* "9/17" · "9/17 ~ 9/19" · "9/17 부터" — 하루면 날짜 하나, 여러 날이면 시작 ~ 끝(재아) */
function blockPeriod(b){
  const md = function(d){ return d ? (+d.slice(5,7)) + "/" + (+d.slice(8,10)) : ""; };
  if(!b || !b.from) return "";
  if(b.openEnded) return md(b.from) + " 부터";
  if(!b.to || b.to === b.from) return md(b.from);
  return md(b.from) + " ~ " + md(b.to);
}
/* "사용 중지 (사유 / 기간)" — 사유가 없으면 기간만 */
function blockLabelText(b){
  const p = blockPeriod(b);
  return "사용 중지 (" + (b.note ? b.note + " / " : "") + p + ")";
}
/* 그 날짜(·시각)에 사용 중지인지. time 을 주면 그 시각만, 안 주면 그 날 하루 중 일부라도 */''', 1)
# blockSpans 에 원본 블록도 실어 둠(라벨용)
s = rep(s, '''    out.push({s, e, note:b.note||"", id:b.id, allDay:(s===0 && e===24*60)});''',
           '''    out.push({s, e, note:b.note||"", id:b.id, allDay:(s===0 && e===24*60), blk:b});''', 1)
save("js/03-util.js", s)

s = load("js/10-timeline.js")
s = rep(s, '''    /* 자세한 시각·사유는 그래프 위 빗금에 적혀 있으므로 여기는 짧게만 */
    const txt = sp.length>1 ? `중지 ${sp.length}구간`
              : (sp[0].allDay ? "하루 중지" : "일부 중지");
    const tip = sp.map(x=>spanLabel(x)+(x.note?` · ${x.note}`:"")).join(" / ");
    return `<span class="bk" title="사용 중지 · ${esc(tip)}">${esc(txt)}</span>`;''',
'''    /* '사용 중지 (사유 / 기간)' — 기간은 날짜(하루면 날짜 하나). 시각은 빗금이 이미 보여 주니 적지 않음(재아) */
    const txt = sp.map(x=>blockLabelText(x.blk)).join(" · ");
    const tip = sp.map(x=>blockLabelText(x.blk)+(x.allDay?"":" · "+spanLabel(x))).join(" / ");
    return `<span class="bk" title="${esc(tip)}">${esc(txt)}</span>`;''', 1)
s = rep(s, '''      title="사용 중지 · ${esc(spanLabel(sp))}${sp.note?` · ${esc(sp.note)}`:""}"><i class="bb-l">사용 중지${sp.note?` (${esc(sp.note)}${sp.allDay?"":" · "+esc(spanLabel(sp))})`:` (${esc(spanLabel(sp))})`}</i></span>`;''',
           '''      title="${esc(blockLabelText(sp.blk))}${sp.allDay?"":" · "+esc(spanLabel(sp))}"><i class="bb-l">${esc(blockLabelText(sp.blk))}</i></span>`;''', 1)
# ② 자리 없음 라벨: 층 이름 칸에도
s = rep(s, '''      <div class="tl-name"><b>${fl==null?"층 미정":esc(floorLabel(fl))}</b><small>${fl==null?"":`테이블 ${tbls.length} · ${seats}석`}</small></div>''',
           '''      <div class="tl-name"><b>${fl==null?"층 미정":esc(floorLabel(fl))}</b><small>${fl==null?"":`테이블 ${tbls.length} · ${seats}석`}</small>${over?`<span class="bk" title="같은 시간에 테이블 수보다 팀이 많습니다 — 맨 위 빗금 칸에 놓인 예약">자리 없음 ${over}팀</span>`:""}</div>''', 1)
save("js/10-timeline.js", s)

s = load("css/05-dash.css")
s = rep(s, '''.overlane .ol-l{position:absolute; left:6px; top:2px; font-style:normal; font-size:11px; font-weight:700; color:var(--rust); background:rgba(255,255,255,.85); padding:0 6px; border-radius:3px; white-space:nowrap; pointer-events:none}''',
           '''.overlane .ol-l{position:absolute; left:6px; top:2px; font-style:normal; font-size:11px; font-weight:700; color:var(--rust); background:rgba(255,255,255,.92); padding:0 6px; border-radius:3px; white-space:nowrap; pointer-events:none; z-index:6}   /* 초과 블록이 그 칸 왼쪽에 놓여도 라벨은 위에 보이게(재아). 층 이름 칸에도 같은 글이 있음 */''', 1)
save("css/05-dash.css", s)

# 사용 중지 편집 시트 목록 표기도 같은 형식
s = load("js/15-sheets.js")
print("blocks sheet label sites:", s.count("spanLabel("))
save("js/15-sheets.js", s)

# ④ 홈페이지 영업시간 글 — 연결 안 함 안내
s = load("js/14b-site-admin.js")
s = rep(s, '''      '<p class="f-note">여기 글은 홈페이지에 보이는 것만 바꿉니다. 예약 시각 계산은 예약 시스템 설정의 운영시간을 따릅니다 — 둘을 같이 맞춰 주세요.</p>') +''',
           '''      '<p class="f-note"><b>홈페이지에 보이는 글자</b>일 뿐, 예약 시스템 운영시간과 연결돼 있지 않습니다. 운영시간을 바꾸면(설정 → 운영시간) 여기 글도 직접 고쳐 주세요. 예약 창의 시각 칸은 시스템 운영시간을 따릅니다.</p>') +''', 1)
save("js/14b-site-admin.js", s)
print("ok")
