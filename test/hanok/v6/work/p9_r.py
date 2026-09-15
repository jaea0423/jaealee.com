# -*- coding: utf-8 -*-
"""8차-R — 재아 목록 3차: 더보기 전체화면 전환, 상세 '바뀐 내용'(전체 이력, 오늘 것 있을 때만 파랑), 노쇼 관리 문구(노쇼 취소·경고 제외 해제·로그),
   PIN 목록(공용) 표시, 목록 취소 삭선 굵게·알약 납작·행 낮게, 22 눈금 오른쪽, 대시보드 폴드 이동 시 접힘, 매장 나가기 삭제·로그아웃 문구,
   TV 버튼 호버 유지, 경고 건수 기준 통일(확정+방문)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 더보기: 전체화면 전환, 매장 나가기 삭제, 로그아웃 ----------
s = R(s, """              <button onclick="closeMore(); goHome()">${ICON.exit}<span>매장 나가기</span></button>
              <button onclick="closeMore(); lockNow()">${ICON.exit}<span>로그아웃 (잠금)</span></button>""",
"""              ${document.fullscreenEnabled ? `<button onclick="closeMore(); toggleFullscreen()">${ICON.tv}<span>${document.fullscreenElement?"전체화면 해제":"전체화면"}</span></button>` : ""}
              <button onclick="closeMore(); lockNow()">${ICON.exit}<span>로그아웃</span></button>""")
s = R(s, """function setFullscreenAuto(on){""", """function toggleFullscreen(){
  try{
    if(document.fullscreenElement){ if(document.exitFullscreen) document.exitFullscreen().catch(function(){}); }
    else if(document.documentElement.requestFullscreen) document.documentElement.requestFullscreen().catch(function(){});
  }catch(e){}
  setTimeout(render, 300);
}
function setFullscreenAuto(on){""")

# ---------- 상세: 바뀐 내용 전체, 오늘 것 있으면 파랑 ----------
s = R(s, """    ${(()=>{
      const lines = changeLines(r);
      if(!lines.length) return "";
      return `<div class="chg-box">
        <div class="cb-t">오늘 바뀐 내용</div>
        ${lines.map(l=>`<div class="cb-l"><span class="cb-tm">${esc(l.t)}</span>${esc(l.s)}</div>`).join("")}
        <div class="cb-s">주방에 이미 전달한 내용이 있다면 다시 알려주세요.</div>
      </div>`;
    })()}""", """    ${(()=>{
      /* 8차-R(재아): 오늘 것만이 아니라 처음부터의 이력 전부. 오늘 바뀐 게 있을 때만 파란 상자, 아니면 회색 */
      const lines = changeLinesAll(r), todayN = todayChanges(r).length;
      if(!lines.length) return "";
      return `<div class="chg-box ${todayN?"":"quiet"}">
        <div class="cb-t">바뀐 내용${todayN?` <span class="tag blue">오늘 ${todayN}건</span>`:""}</div>
        ${lines.map(l=>`<div class="cb-l"><span class="cb-tm">${esc(l.t)}</span>${esc(l.s)}</div>`).join("")}
        ${todayN?`<div class="cb-s">주방에 이미 전달한 내용이 있다면 다시 알려주세요.</div>`:""}
      </div>`;
    })()}""")
s = R(s, """function changeLines(r){
  var cs = todayChanges(r).slice().reverse(), out = [], i, j;""", """/* 처음부터의 이력 — 날짜까지 붙여서 */
function changeLinesAll(r){
  var cs = (r.changes || []).slice().reverse(), out = [], i, j;
  for(i=0;i<cs.length;i++){
    var c = cs[i], d = c.at ? new Date(c.at) : null;
    var t = d && !isNaN(d) ? (d.getMonth()+1)+"/"+d.getDate()+" "+pad(d.getHours())+":"+pad(d.getMinutes()) : (c.on || "");
    if(c.kind === "등록"){ out.push({t:t, s:"예약 접수"}); continue; }
    if(c.kind === "취소"){ out.push({t:t, s:"예약 취소"}); continue; }
    if(c.kind === "노쇼"){ out.push({t:t, s:"노쇼 처리"}); continue; }
    if(!(c.items||[]).length){ out.push({t:t, s:"수정"}); continue; }
    for(j=0;j<c.items.length;j++) out.push({t:t, s:c.items[j].n + (c.items[j].a != null ? " " + c.items[j].a + " → " + c.items[j].b : "")});
  }
  return out;
}
function changeLines(r){
  var cs = todayChanges(r).slice().reverse(), out = [], i, j;""")
s = R(s, """.chg-box{border:1px solid var(--blue-line); background:var(--blue-soft);""", """.chg-box.quiet{border-color:var(--border); background:var(--surface-2)}
.chg-box.quiet .cb-t, .chg-box.quiet .cb-tm{color:var(--text-2)}
.chg-box{border:1px solid var(--blue-line); background:var(--blue-soft);""")

# ---------- 노쇼 관리 문구·해제·로그 ----------
s = R(s, """      <button class="btn sm" onclick="undoNoshow('${r.id}')">되돌리기</button>
      ${k && !ex ? `<button class="btn sm ghost" onclick="clearNoshow('${k}')" title="이 번호는 다음 예약 때 노쇼 경고를 띄우지 않음">경고 제외</button>` : ""}""",
"""      <button class="btn sm" onclick="undoNoshow('${r.id}')">노쇼 취소</button>
      ${k ? (ex ? `<button class="btn sm ghost" onclick="unclearNoshow('${k}')" title="다시 노쇼 경고를 띄움">경고 제외 해제</button>` : `<button class="btn sm ghost" onclick="clearNoshow('${k}')" title="이 번호는 다음 예약 때 노쇼 경고를 띄우지 않음">경고 제외</button>`) : ""}""")
s = R(s, """function restoreNoshow(){ store().settings.noshowExcluded = []; mirrorDraft("noshowExcluded"); saveData(); render(); }""",
"""function restoreNoshow(){ store().settings.noshowExcluded = []; mirrorDraft("noshowExcluded"); logEvent("노쇼 경고 제외 전부 해제", ""); saveData(); render(); }
async function unclearNoshow(key){
  if(readonlyBlock()) return;
  const st = store().settings; st.noshowExcluded = (st.noshowExcluded||[]).filter(k=>k!==key); mirrorDraft("noshowExcluded");
  logEvent("노쇼 경고 제외 해제", key); saveData(); render();
}""")
s = R(s, """  if(!await uiConfirm("노쇼를 되돌릴까요?", `${dateLabel(r.date)} ${r.time} ${r.name} 손님 → ${to}`, {ok:"되돌리기"})) return;
  if(readonlyBlock()) return;
  logEvent("상태 변경", `${r.date} ${r.time} ${r.name} 노쇼 → ${to}`);""",
"""  if(!await uiConfirm("노쇼를 취소할까요?", `${dateLabel(r.date)} ${r.time} ${r.name} 손님 → ${to}(으)로 돌아갑니다`, {ok:"노쇼 취소"})) return;
  if(readonlyBlock()) return;
  logEvent("노쇼 취소", `${r.date} ${r.time} ${r.name} ${pplOf(r)}명 ${r.phone||""} 노쇼 → ${to}`);""")
s = R(s, """      ${excluded.length?`<br>제외된 번호 ${excluded.length}건 · <button class="linkbtn" onclick="restoreNoshow()">되돌리기</button>`:""}""",
         """      ${excluded.length?`<br>경고 제외 번호 ${excluded.length}건 · <button class="linkbtn" onclick="restoreNoshow()">전부 해제</button>`:""}""")
# 로그 더: 방문/확정 되돌림도 남김(markRes 는 이미 상태 변경 로그), 예약 등록 상세에 경로·좌석 이미 있음. 좌석 배정·수정 ok.

# ---------- PIN 목록 (지금은 공용 하나) ----------
s = R(s, """      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>
    </div>""", """      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>
    </div>
    <div class="subhead" style="margin-top:14px">PIN 목록</div>
    <div class="rowitem"><span class="grow"><span class="t">공용 <span class="tag pine">사용 중</span></span><span class="s">직원 모두가 쓰는 PIN. 접속 기록에는 '공용' 으로 남습니다.</span></span></div>
    <p class="f-note">직원마다 다른 PIN(이름별)은 나중에 여기서 추가·삭제하게 만들 수 있습니다. 그러면 기록에 직원 이름이 남습니다(누님 질문 15).</p>""")

# ---------- 목록: 취소 삭선 굵게·흐리게, 알약 납작, 행 낮게 ----------
s = R(s, """.rrow.s-방문, .rrow.s-취소, .rrow.s-노쇼{background:var(--surface-2); color:var(--text-3)}
.rrow.s-방문 .rr-t:before{content:"✓ "; color:var(--pine); font-weight:700}
.rrow.s-방문 .rr-n{color:var(--text-2)}
.rrow.s-취소 .rr-n, .rrow.s-취소 .rr-t{text-decoration:line-through}
.rrow.s-노쇼 .rr-n{text-decoration:line-through} .rrow.s-노쇼 .rr-t{color:var(--rust)}""",
""".rrow.s-방문, .rrow.s-취소, .rrow.s-노쇼{background:var(--surface-2); color:var(--text-3)}
.rrow.s-방문 .rr-t:before{content:"✓ "; color:var(--pine); font-weight:700}
.rrow.s-방문 .rr-n{color:var(--text-2)}
/* 취소는 줄 전체에 굵은 삭선 + 흐리게(방문과 구분) */
.rrow.s-취소{opacity:.55; position:relative}
.rrow.s-취소:after{content:""; position:absolute; left:var(--s8); right:var(--s8); top:50%; height:2px; background:var(--text-3); pointer-events:none}
.rrow.s-노쇼 .rr-n{text-decoration:line-through} .rrow.s-노쇼 .rr-t{color:var(--rust)}
.rrow{padding-top:var(--s8); padding-bottom:var(--s8)}
.rrow .pill{padding:1px 6px; font-size:var(--fs-label); line-height:1.4}""")
s = R(s, """.mrow.s-취소 .mr-n, .mrow.s-노쇼 .mr-n{text-decoration:line-through}""", """.mrow.s-취소{opacity:.55; position:relative} .mrow.s-취소:after{content:""; position:absolute; left:var(--s12); right:var(--s12); top:50%; height:2px; background:var(--text-3); pointer-events:none}
.mrow.s-노쇼 .mr-n{text-decoration:line-through}""")

# ---------- 22 눈금: 다른 눈금처럼 선 오른쪽 ----------
s = R(s, """.tk.end b{transform:translateX(-100%); margin-left:-2px}""", """.tk.end b{}   /* 예약률 글자를 빼서 오른쪽에 자리가 생겼으니 다른 눈금과 같게 */""")
s = R(s, """.tl-row.axis .tl-track{overflow:visible}""", """.tl-row.axis .tl-track{overflow:visible} .tl-row.axis .tl-rate{background:transparent}""")

# ---------- 대시보드 폴드: 탭 이동·시트/마법사 열기에 접힘 ----------
s = R(s, """  if(view.tab==="settings" && t!=="settings") Object.keys(view.open).forEach(function(x){ if(x.indexOf("s_") === 0) view.open[x] = false; });   /* 나갔다 오면 접힌 상태로(재아) */""",
"""  Object.keys(view.open).forEach(function(x){ view.open[x] = false; });   /* 어디든 갔다 오면 폴드는 접힌 상태로(재아) — 설정·대시보드 모두 */""")
s = R(s, """function openWizard(date){
  if(readonlyBlock()) return;
  histPush();""", """function openWizard(date){
  if(readonlyBlock()) return;
  Object.keys(view.open).forEach(function(x){ view.open[x] = false; });   /* 마법사 다녀오면 목록 폴드는 접힘 */
  histPush();""")

# ---------- TV 버튼 호버: 버튼 위로 옮겨도 사라지지 않게 ----------
s = R(s, """  .tv-hot:hover ~ .tv-exit,
  .tv-hot:hover ~ .tv-swap{opacity:1; pointer-events:auto}
  .tv-exit:hover{opacity:1; pointer-events:auto}""", """  .tv-hot:hover ~ .tv-exit,
  .tv-hot:hover ~ .tv-swap{opacity:1; pointer-events:auto}
  .tv-exit:hover, .tv-swap:hover{opacity:1; pointer-events:auto}""")
s = R(s, """    <div class="tv-hot" aria-hidden="true"></div>""", """    <div class="tv-hot" aria-hidden="true" onmouseenter="pokeExit(6000)"></div>   <!-- 마우스가 버튼으로 옮겨가는 사이 사라지지 않게 6초 유지 -->""")

# ---------- 경고 건수 기준 통일: 확정+방문 ----------
s = R(s, """  const warnCnt = active.filter(r=>resWarn(r).length).length;""", """  const warnCnt = dayRes.filter(r=>holdsSeat(r) && resWarn(r).length).length;   /* 타임라인 위 '경고 N건' 과 같은 기준(확정+방문) */""")
L.js_check(s)
L.save(s)
print("p9_r ok")
