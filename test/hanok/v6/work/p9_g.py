# -*- coding: utf-8 -*-
"""v6 8차-G — 점검 결함 수정 묶음 3(낮음 항목 일괄)
   R6 재안내 문자: 방문 처리·지난 예약 제외 · R8 수정 시트 유아>총원 차단 → 경고 · R9 시트 코스 구성 0 경고
   R10 날짜 옮기면 auto 플래그 제거, 미정+잠정없음 예약도 예약률 분자에 1좌석, view.tab="res" 제거
   C5 삭제된 좌석의 예약을 미배정으로 셈, 지난 임시일정·공휴일 1년 넘으면 정리
   D10 전화번호 저장 전 정규화 · D11 캐시 키에 프로젝트 · D12 SYNC 초기값 storeUpd, 휴지통 자르기 전 미전송 보존, reloadFromStore 매장 키
   T4 '외 N건' 자리 미리 확보 · 6장 로그 detail 전화 뒷자리만"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- R6 ----------
s = R(s, """  if(r.status === "취소" || r.status === "노쇼") return { state:"제외", at:at };
  if(!at) return { state:"제외", at:null };""",
"""  if(r.status === "취소" || r.status === "노쇼") return { state:"제외", at:at };
  if(!at) return { state:"제외", at:null };
  /* 이미 오신 손님(방문)·시작 시각이 지난 예약에는 보내지 않습니다 — 지금은 흉내지만 실발송을 붙이면 그대로 나갑니다(점검 R6) */
  if(r.status === "방문") return { state:"제외", at:at };
  if(r.date < todayStr() || (r.date === todayStr() && toMin(r.time) < new Date().getHours()*60 + new Date().getMinutes())) return { state:"제외", at:at };""")
s = R(s, """       : st.state === "제외"     ? "취소·노쇼 예약이라 보내지 않습니다\"""",
"""       : st.state === "제외"     ? "취소·노쇼·이미 오신 손님이거나 시각이 지나 보내지 않습니다\"""")

# ---------- R8 / R9 / D10 / R10(auto) ----------
s = R(s, """  if((f.infants||0) > f.people)
    return uiAlert("유아 수가 총 인원보다 많습니다", `총 ${f.people}명 중 유아 ${f.infants}명`, "warn");
  const old = view.form.id ? s.reservations.find(r=>r.id===view.form.id) : null;""",
"""  /* 유아 > 총원은 마법사처럼 막지 않고 아래 saveIssues 에서 경고만 합니다(점검 R8 — 2-4 원칙) */
  const old = view.form.id ? s.reservations.find(r=>r.id===view.form.id) : null;""")
s = R(s, """    date:f.date, time:f.time, name:(f.name||"").trim(), phone:(f.phone||"").trim(),
    people: Math.max(1, f.people||1), infants: f.infants||0, chairs: f.chairs||0,""",
"""    date:f.date, time:f.time, name:(f.name||"").trim(), phone:phoneNorm(f.phone),
    people: Math.max(1, f.people||1), infants: f.infants||0, chairs: f.chairs||0,""")
s = R(s, """  delete rec.__id; delete rec.adults; delete rec.courseOpen;

  /* 막지 않고 알리기만 합니다 (설계 5.2). 그대로 저장하면 경고 예약으로 남습니다. */""",
"""  delete rec.__id; delete rec.adults; delete rec.courseOpen;
  if(old && old.date !== rec.date) delete rec.auto;   /* 자동 방문 표시는 그 날짜의 것 — 옮기면 지웁니다(점검 R10) */

  /* 막지 않고 알리기만 합니다 (설계 5.2). 그대로 저장하면 경고 예약으로 남습니다. */""")
s = R(s, """  resWarn(rec).forEach(k => { if(words[k]) out.push(words[k]); });""",
"""  resWarn(rec).forEach(k => { if(words[k]) out.push(words[k]); });
  if((rec.infants||0) > pplOf(rec)) out.push(`유아 ${rec.infants}명이 총 인원 ${pplOf(rec)}명보다 많습니다`);
  if(rec.menuType === "코스" && !rec.courseUndecided && !Object.keys(rec.courses||{}).some(k=>rec.courses[k] > 0))
    out.push("코스인데 구성이 비어 있습니다 — '코스 미정' 으로 두거나 구성을 넣으세요");""")
# 전화번호 정규화 헬퍼 — 서버는 숫자만 저장하고 rowToRes 가 phoneFmt 로 되돌리므로, 저장 전에 같은 모양으로 맞춰야 두 기기가 같은 변경을 충돌로 안 봅니다(점검 D10)
s = R(s, """function phoneFmt(d){
  if(!d) return "";""", """/* 입력한 번호를 저장용 모양으로 — 숫자만 남기고 phoneFmt. 서버 왕복 뒤 모양이 달라져 충돌로 오인하던 것을 막습니다(점검 D10) */
function phoneNorm(v){ const d = String(v || "").replace(/\\D/g, ""); return d ? phoneFmt(d) : ""; }
function phoneFmt(d){
  if(!d) return "";""")
# 마법사 등록도 같은 정규화
s = R(s, """    name:WZ.name.trim(), phone:WZ.phone.trim(),""", """    name:WZ.name.trim(), phone:phoneNorm(WZ.phone),""")

# ---------- R10: view.tab="res" (없는 값) ----------
s = R(s, """  view.tab = "res";
  WZ.done = rec;""", """  WZ.done = rec;""")

# ---------- R10: 미정+잠정 없음 예약도 예약률 분자에 1좌석 ----------
s = R(s, """  const roomUsed = list.reduce((a,r)=>a + seatsOf(r).filter(isRoomSeat).length * spanOf(r), 0);
  const hallUsed = list.reduce((a,r)=>a + seatsOf(r).filter(id=>halls.some(x=>x.id===id)).length * spanOf(r), 0);""",
"""  /* 자리를 아직 못 잡은 미정 예약(잠정도 없음)도 손님은 오므로 희망 쪽 좌석 1개로 셉니다 — 빠지면 예약률이 실제보다 낮게 보입니다(점검 R10) */
  const noSeat = r => !seatsOf(r).length && !r.roomId;
  const roomUsed = list.reduce((a,r)=>a + (noSeat(r) ? (r.seatPref==="room-any" ? 1 : 0) : seatsOf(r).filter(isRoomSeat).length) * spanOf(r), 0);
  const hallUsed = list.reduce((a,r)=>a + (noSeat(r) ? (r.seatPref==="room-any" ? 0 : 1) : seatsOf(r).filter(id=>halls.some(x=>x.id===id)).length) * spanOf(r), 0);""")

# ---------- C5: 삭제된 좌석의 예약은 미배정으로 ----------
s = R(s, """  const unassigned = active.filter(r=>!r.roomId).length;
  const usedSeats""", """  const unassigned = active.filter(r=>!r.roomId || !seatById(r.roomId)).length;   /* 좌석이 삭제된 예약도(점검 C5) */
  const usedSeats""")
s = R(s, """  const list = s.reservations.filter(r=>r.date===d && r.status==="확정" && !r.roomId)
    .sort((a,b)=>a.time.localeCompare(b.time));
  const rows = list.length ? list.map(r=>`
    <button class="rowitem tap" onclick="openMark('${r.id}')">""",
"""  const list = s.reservations.filter(r=>r.date===d && r.status==="확정" && (!r.roomId || !seatById(r.roomId)))
    .sort((a,b)=>a.time.localeCompare(b.time));
  const rows = list.length ? list.map(r=>`
    <button class="rowitem tap" onclick="openMark('${r.id}')">""")
# 지난 임시일정·추가 공휴일·사용중지 1년 넘은 것 정리 (migrate 에서)
s = R(s, """    if(!st.joins) st.joins = deepClone(def.joins || []);
    if(!st.holidaysOff) st.holidaysOff = [];""",
"""    if(!st.joins) st.joins = deepClone(def.joins || []);
    if(!st.holidaysOff) st.holidaysOff = [];
    /* 1년 넘게 지난 임시 일정·추가/제외 공휴일·사용 중지는 정리 — 무한히 쌓여 설정 JSON 이 커지는 것을 막습니다(점검 C5) */
    var cut = shiftDate(todayStr(), -366);
    if(st.overrides) st.overrides = st.overrides.filter(function(o){ return !o.date || o.date >= cut; });
    st.holidays = (st.holidays || []).filter(function(d){ return d >= cut; });
    st.holidaysOff = st.holidaysOff.filter(function(d){ return d >= cut; });
    (st.rooms || []).forEach(function(r){ if(r.blocks) r.blocks = r.blocks.filter(function(b){ return !b.to || b.to >= cut; }); });""")

# ---------- D11: 캐시 키에 프로젝트 — dev/prod 가 같은 origin 이면 오프라인 때 서로 섞였습니다 ----------
s = R(s, """var CACHE_KEY = "hanok.cache.v1", UI_KEY = "hanok.ui.v1", SESSION_KEY = "hanok.session.v1", PINH_KEY = "hanok.pinh.v1";""",
"""/* 캐시·세션 키에 프로젝트 주소를 붙입니다 — dev 와 실서비스가 같은 origin(jaealee.com)이라 안 붙이면 prod 오프라인 때 dev 더미가 보였습니다(점검 D11) */
var PROJ_TAG = (function(){ try{ return supaOn() ? "." + SUPA_CFG.url.replace(/^https?:\\/\\//, "").split(".")[0] : ""; }catch(e){ return ""; } })();
var CACHE_KEY = "hanok.cache.v1" + PROJ_TAG, UI_KEY = "hanok.ui.v1", SESSION_KEY = "hanok.session.v1" + PROJ_TAG, PINH_KEY = "hanok.pinh.v1" + PROJ_TAG;""")

# ---------- D12 ----------
s = R(s, """    s.trash = (s.trash || []).concat([rec]);
    if(s.trash.length > 500) s.trash = s.trash.slice(-500);""",
"""    s.trash = (s.trash || []).concat([rec]);
    /* 휴지통은 500건까지만 들고 있되, 아직 서버에 못 보낸 삭제는 버리지 않습니다 — 버리면 서버에서 되살아납니다(점검 D12) */
    if(s.trash.length > 500){
      const keep = s.trash.filter(x=>SYNC && SYNC.res && SYNC.res[x.id] && JSON.stringify(x) !== SYNC.res[x.id]);
      s.trash = keep.concat(s.trash.filter(x=>keep.indexOf(x) < 0).slice(-(500 - keep.length)));
    }""")
s = R(s, """      if(JSON.stringify(st.settings) === SYNC.settings[k]){ st.settings = migrate({ hanok:{settings:srow.settings||{}} }).hanok.settings;""",
"""      if(JSON.stringify(st.settings) === SYNC.settings[k]){ var mg = {}; mg[k] = { settings: srow.settings || {} }; st.settings = migrate(mg)[k].settings;""")

# ---------- T4: '외 N건' 줄 자리를 미리 확보 ----------
s = R(s, """.tvl-more:empty{display:none}""", """/* 비어 있어도 자리는 둡니다 — 접은 뒤에 이 줄이 나타나면 마지막 줄이 잘렸습니다(점검 T4) */
.tvl-more:empty{visibility:hidden}""")

# ---------- 6장: 로그에 전화번호 전체 남기지 않기 ----------
s = R(s, """  if(rec) logEvent("예약 삭제", `${rec.date} ${rec.time} ${rec.name} ${rec.phone||""}`);""",
"""  if(rec) logEvent("예약 삭제", `${rec.date} ${rec.time} ${rec.name} ${rec.phone ? "…" + rec.phone.replace(/\\D/g,"").slice(-4) : ""}`);""")

L.js_check(s)
L.save(s)
print("p9_g ok")
