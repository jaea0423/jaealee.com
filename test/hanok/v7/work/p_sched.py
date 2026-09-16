# -*- coding: utf-8 -*-
"""예정 설정(03b-scheduled.js) 연결:
   · uiPrompt 에 기본값(opt.value), uiChoose(title, 목록) 추가
   · 날짜를 아는 계산은 settingsAt(date) — 좌석 목록·합침·코스·단체 기준
   · seatById / joinOf 는 지금+예정 전부에서 찾음(예정 좌석 id 도 풀림)
   · applySettings 에서 예정 여부 묻기, 불러올 때·자정에 absorbScheduled
   · 설정 화면: 되돌리기 왼쪽 '예정 N', 묶음 제목 옆 '9/22부터 바뀜' 표시"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep, js_check

# ---- 모달: prompt 기본값, uiChoose ----
s = load("js/06-modal.js")
s = rep(s, '''  return new Promise(res => { modalReplace({mode:"prompt", title, msg, tone:"ok", ok:opt.ok||"확인", cancel:"취소", password:!!opt.password, res}); });
}''', '''  return new Promise(res => { modalReplace({mode:"prompt", title, msg, tone:"ok", ok:opt.ok||"확인", cancel:"취소", password:!!opt.password, value:opt.value||"", res}); });
}
/* 여러 개 중 하나 고르기 — 고른 번호(0부터), 취소면 null */
function uiChoose(title, options, msg){
  return new Promise(res => { modalReplace({mode:"choice", title, msg:msg||"", tone:"ok", choices:options.map((o,i)=>[o,i]), cancel:"취소", res}); });
}''')
s = rep(s, '''<input id="md-input" type="${m.password?"password":"text"}" autofocus style="margin-top:8px; width:100%"''',
           '''<input id="md-input" type="${m.password?"password":"text"}" value="${esc(m.value||"")}" autofocus style="margin-top:8px; width:100%"''')
s = rep(s, '''          ${m.mode==="choice" ? (m.choices||[]).map(([lb,v],i)=>`<button class="btn ${i===0?"danger-fill":"primary"}" onclick="modalAnswer(${JSON.stringify(v)})">${esc(lb)}</button>`).join("") :''',
           '''          ${m.mode==="choice" ? (m.choices||[]).map(([lb,v],i)=>`<button class="btn ${m.tone==="warn"&&i===0?"danger-fill":"primary"}" onclick="modalAnswer(${JSON.stringify(v)})">${esc(lb)}</button>`).join("") :''')
# applySettings: 예정 묻기 → 흡수
s = rep(s, '''function applySettings(){
  if(!view.draft) return;
  if(readonlyBlock()) return;
  const before = store().settings, after = deepClone(view.draft);
  const diff = settingsDiff(before, after);''', '''async function applySettings(){
  if(!view.draft) return;
  if(readonlyBlock()) return;
  const before = store().settings, after = deepClone(view.draft);
  /* 좌석·규칙·코스가 바뀌었으면 "지금 바로 / 날짜부터" — 날짜면 예정으로 들어가고 그 묶음은 되돌아옵니다(03b) */
  if(!await askScheduleOnApply(before, after)) return;
  after.scheduled = before.scheduled;   /* 예정 목록은 임시본이 아니라 설정에서 직접 관리 */
  const diff = settingsDiff(before, after);''')
s = rep(s, '''  logEvent("설정 변경", diff.length ? diff.join(" / ").slice(0, 300) : "적용(변경 없음)");
  takeSnapshot();''', '''  logEvent("설정 변경", diff.length ? diff.join(" / ").slice(0, 300) : "적용(변경 없음)");
  absorbScheduled();
  takeSnapshot();''')
# 상단바: 되돌리기 왼쪽에 '예정 N'
s = rep(s, '''          <button class="tvbtn b-revert" onclick="revertSettings()" ${settingsDirty()?"":"disabled"}>되돌리기</button>''',
           '''          <button class="tvbtn b-sched ${schedList().length?'has':''}" onclick="openScheduled()" title="예정된 설정">예정<i class="cnt">${schedList().length}</i></button>
          <button class="tvbtn b-revert" onclick="revertSettings()" ${settingsDirty()?"":"disabled"}>되돌리기</button>''')
s = rep(s, 'const NAME = {rooms:"좌석", joins:"룸 합침", schedules:"운영시간",', 'const NAME = {scheduled:null, rooms:"좌석", joins:"룸 합침", schedules:"운영시간",')
# 자정: 예정 흡수
s = rep(s, '''  if(SNAP_DAY && todayStr() !== SNAP_DAY){ takeSnapshot(); if(AUTHED && autoCloseDays()) saveData(); }''',
           '''  if(SNAP_DAY && todayStr() !== SNAP_DAY){ if(AUTHED) absorbScheduled(); takeSnapshot(); if(AUTHED && autoCloseDays()) saveData(); }''')
save("js/06-modal.js", s)
c = load("css/04-layout.css")
c = rep(c, ".tvbtn.icon.b-reqs{position:relative; overflow:visible}", ".tvbtn.icon.b-reqs{position:relative; overflow:visible}\n.tvbtn.b-sched .cnt{font-style:normal; margin-left:6px; min-width:18px; height:18px; padding:0 5px; border-radius:9px; background:rgba(255,255,255,.14); font-size:12px; line-height:18px; text-align:center}\n.tvbtn.b-sched.has .cnt{background:#C9A66B; color:#1a1714}")
save("css/04-layout.css", c)

# ---- 불러온 뒤 흡수 ----
s = load("js/02-supabase.js")
s = rep(s, "function migrate(d){", "function migrate(d){\n  /* 예정 설정 중 날짜가 된 것은 불러오자마자 흡수(03b). migrate 안이라 매장별로 도는 아래 코드보다 먼저, 전역 store() 가 준비된 뒤에 한 번 더 부릅니다 */")
save("js/02-supabase.js", s)
s = load("js/18-router.js")
s = rep(s, "/* 시트·마법사 어디서든: Enter = 그 창의 확인·등록 단추", "/* 화면이 처음 그려질 때 예정 설정을 흡수합니다(불러온 직후) */\nsetTimeout(function(){ try{ if(AUTHED && DATA && view.storeKey) absorbScheduled(); }catch(e){} }, 1500);\n\n/* 시트·마법사 어디서든: Enter = 그 창의 확인·등록 단추")
save("js/18-router.js", s)

# ---- 날짜를 아는 계산은 settingsAt ----
s = load("js/03-util.js")
s = rep(s, 'function seatById(id){ const st = store().settings; return (st.rooms||[]).find(x=>x.id===id) || null; }',
           '/* id 로 좌석 찾기 — 지금 좌석에 없으면 예정 좌석에서도 찾습니다(예정 날짜의 예약이 그 좌석을 가리킬 수 있음) */\nfunction seatById(id){ const st = store().settings; return (st.rooms||[]).find(x=>x.id===id) || allSeatsEver().find(x=>x.id===id) || null; }')
s = rep(s, 'function joinOf(ids){ return (store().settings.joins||[]).find(g=>sameIds(g.ids, ids)) || null; }',
           'function joinOf(ids){ return allJoinsEver().find(g=>sameIds(g.ids, ids)) || null; }')
s = rep(s, 'function floorTables(fl){ return (store().settings.rooms || []).filter(t => isTable(t) && (fl == null || (t.floor || "") === (fl || ""))); }   /* fl == null → 전체 */',
           'function floorTables(fl, date){ return (date ? roomsAt(date) : (store().settings.rooms || [])).filter(t => isTable(t) && (fl == null || (t.floor || "") === (fl || ""))); }   /* fl == null → 전체. date 를 주면 그 날짜의 좌석 */')
s = rep(s, '  const seats = (st.rooms||[]).filter(x=>!blockedAt(x, date, time));', '  const seats = roomsAt(date).filter(x=>!blockedAt(x, date, time));')
s = rep(s, '    const order = x => (st.rooms||[]).indexOf(x);', '    const order = x => roomsAt(date).indexOf(x);')
save("js/03-util.js", s)

s = load("js/10-timeline.js")
s = rep(s, "  const rooms = st.rooms.filter(isRoom);", "  const rooms = roomsAt(date).filter(isRoom);   /* 그 날짜의 좌석(예정 반영) */")
save("js/10-timeline.js", s)
s = load("js/11-res.js")
s = rep(s, '''  const rooms = st.rooms.filter(isRoom);
  const halls = st.rooms.filter(isTable);''', '''  const rooms = roomsAt(date).filter(isRoom);            /* 앞날은 예정 좌석 수로 (예약률 분모) */
  const halls = roomsAt(date).filter(isTable);''')
save("js/11-res.js", s)
s = load("js/09-sms.js")
s = rep(s, "  const gsize = s.settings.groupSize || 8;", "  const gsize = settingsAt(d).groupSize || 8;")
save("js/09-sms.js", s)
s = load("js/16-wizard.js")
s = rep(s, 'function courseGroups(){ return store().settings.courseGroups || DEFAULT_COURSE_GROUPS; }',
           'function courseGroups(date){ return (date ? settingsAt(date) : store().settings).courseGroups || DEFAULT_COURSE_GROUPS; }')
s = rep(s, "  const gs = courseGroups(), out = [];", "  const gs = courseGroups(cTgt() && cTgt().date), out = [];")
s = rep(s, "  const gs = courseGroups();\n", "  const gs = courseGroups(cTgt() && cTgt().date);\n")
s = rep(s, "  const rooms = st.rooms.filter(isRoom);\n", "  const rooms = roomsAt(ctx.date).filter(isRoom);\n")
s = rep(s, '''    const rooms = st.rooms.filter(isRoom);
    const joins = (st.joins||[]);''', '''    const rooms = roomsAt(WZ.date).filter(isRoom);   /* 예정 좌석 반영 */
    const joins = joinsAt(WZ.date);''')
save("js/16-wizard.js", s)
s = load("js/15-sheets.js")
s = rep(s, '''  const roomOpts = `<optgroup label="룸">${st.rooms.filter(isRoom).map(''', '''  const roomOpts = `<optgroup label="룸">${roomsAt(f.date).filter(isRoom).map(''')
s = rep(s, '''    `<optgroup label="룸 합침">${(st.joins||[]).map(''', '''    `<optgroup label="룸 합침">${joinsAt(f.date).map(''')
s = rep(s, '''<optgroup label="특정 테이블 (파셜룸 등 꼭 잡아야 할 때)">${st.rooms.filter(isTable).map(''', '''<optgroup label="특정 테이블 (파셜룸 등 꼭 잡아야 할 때)">${roomsAt(f.date).filter(isTable).map(''')
s = rep(s, "    let cand = st.rooms.filter(x=>{", "    let cand = roomsAt(r.date).filter(x=>{")
s = rep(s, '    if(kind!=="table-any") (st.joins||[]).filter(j=>ppl>=j.min && ppl<=j.max).forEach(j=>{', '    if(kind!=="table-any") joinsAt(r.date).filter(j=>ppl>=j.min && ppl<=j.max).forEach(j=>{')
s = rep(s, 'sched:sheetSchedule, ovr:sheetOverride, blocks:sheetBlocks, reqs:sheetRequests, req:sheetRequest', 'sched:sheetSchedule, ovr:sheetOverride, blocks:sheetBlocks, reqs:sheetRequests, req:sheetRequest, sched2:sheetScheduled')
save("js/15-sheets.js", s)

# ---- 설정 화면: 묶음 제목 옆 예정 표시 ----
s = load("js/14-settings.js")
s = rep(s, '''    ${sec("rules","예약 규칙",`단체 ${st.groupSize||8}명`, ruleBody)}''', '''    ${sec("rules","예약 규칙",`단체 ${st.groupSize||8}명${schedChip("rules")}`, ruleBody)}''')
s = rep(s, '''    ${sec("seats","좌석",`룸 ${st.rooms.filter(isRoom).length} · 테이블 ${st.rooms.filter(isTable).length}''', '''    ${sec("seats","좌석",`룸 ${st.rooms.filter(isRoom).length} · 테이블 ${st.rooms.filter(isTable).length}${schedChip("seats")}''')
s = rep(s, '''    ${sec("course","코스·세트 구성",`${(st.courseGroups||[]).length}행`, courseBody)}''', '''    ${sec("course","코스·세트 구성",`${(st.courseGroups||[]).length}행${schedChip("course")}`, courseBody)}''')
s += '''
/* 묶음 제목 옆 "9월 22일부터 바뀜" — 예정이 걸려 있으면 */
function schedChip(group){
  const l = schedFor(group, store().settings);
  return l.length ? ` <span class="pill amber" onclick="event.stopPropagation(); openScheduled()">${esc(dateLabel(l[0].from))}${l[0].to?" ~":""}부터 바뀜${l.length>1?` 외 ${l.length-1}`:""}</span>` : "";
}
'''
save("js/14-settings.js", s)
js_check()
print("sched wiring ok")
