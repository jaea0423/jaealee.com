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

s = load("js/16-wizard.js")
s = rep(s, 'function courseGroups(){ return store().settings.courseGroups || DEFAULT_COURSE_GROUPS; }',
           'function courseGroups(date){ return (date ? settingsAt(date) : store().settings).courseGroups || DEFAULT_COURSE_GROUPS; }')
s = rep(s, "  const gs = courseGroups(), out = [];", "  const gs = courseGroups(cTgt() && cTgt().date), out = [];")
s = rep(s, "  const gs = courseGroups();" + chr(10), "  const gs = courseGroups(cTgt() && cTgt().date);" + chr(10))
s = rep(s, "  const people = ctx.people || 0;" + chr(10) + "  const rooms = st.rooms.filter(isRoom);", "  const people = ctx.people || 0;" + chr(10) + "  const rooms = roomsAt(ctx.date).filter(isRoom);")
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
