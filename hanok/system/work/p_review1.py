# -*- coding: utf-8 -*-
"""전수 검토(2026-09-16) 1차 수정:
   B1 폰 목록(renderAgenda)이 기본 필터 '예정' 을 몰라서 '해당 조건의 예약이 없습니다' 만 보이던 것 —
      PC 목록과 같은 묶음(전체/예정/지난·방문/취소·노쇼)과 '지금' 선을 쓰게 합침 """
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep

s = load("js/07-dash.js")
# 묶음 정의를 함수로 빼서 둘이 같이 씀
s = rep(s, '''function renderResList(date){
  const s = store();
  let day = s.reservations.filter(r=>r.date===date).sort((a,b)=>a.time.localeCompare(b.time));
  /* 8차-W(재아): 전체 / 예정(아직 안 온 확정) / 지난·방문(1시간 지난 확정 + 방문) / 취소·노쇼 */
  const nowM0 = toMin(nowHM()), isToday0 = date === todayStr();
  const isPastRes = r => r.date < todayStr() || (isToday0 && toMin(r.time) + 60 < nowM0);
  /* '예정' 에는 아직 시각이 안 지난 '방문' 도 흐리게 넣습니다 — 잘못 누른 방문 처리를 눈치채게(8차-Z 재아) */
  const GROUPS = { "전체": r=>true, "예정": r=>(r.status==="확정" || r.status==="방문") && !isPastRes(r), "지난·방문": r=>r.status==="방문" || (r.status==="확정" && isPastRes(r)), "취소·노쇼": r=>r.status==="취소" || r.status==="노쇼" };
  if(!GROUPS[view.filter]) view.filter = "예정";
  /* 기본은 '예정'. 지난 날짜에서는 예정이 늘 비므로 그때만 '전체' 로 보여 줍니다(버튼도 전체가 켜짐) */
  const eff = (view.filter === "예정" && date < todayStr()) ? "전체" : view.filter;
  const filters = Object.keys(GROUPS).map(f=>{''',
'''/* 목록 묶음 — PC 목록과 폰 목록이 같이 씁니다.
   8차-W(재아): 전체 / 예정(아직 안 온 확정) / 지난·방문(1시간 지난 확정 + 방문) / 취소·노쇼
   '예정' 에는 아직 시각이 안 지난 '방문' 도 흐리게 넣습니다 — 잘못 누른 방문 처리를 눈치채게(8차-Z 재아) */
function listGroups(date){
  const nowM0 = toMin(nowHM()), isToday0 = date === todayStr();
  const isPastRes = r => r.date < todayStr() || (isToday0 && toMin(r.time) + 60 < nowM0);
  const GROUPS = { "전체": r=>true, "예정": r=>(r.status==="확정" || r.status==="방문") && !isPastRes(r), "지난·방문": r=>r.status==="방문" || (r.status==="확정" && isPastRes(r)), "취소·노쇼": r=>r.status==="취소" || r.status==="노쇼" };
  if(!GROUPS[view.filter]) view.filter = "예정";
  /* 기본은 '예정'. 지난 날짜에서는 예정이 늘 비므로 그때만 '전체' 로 보여 줍니다(버튼도 전체가 켜짐) */
  const eff = (view.filter === "예정" && date < todayStr()) ? "전체" : view.filter;
  return { GROUPS, eff };
}
function renderResList(date){
  const s = store();
  let day = s.reservations.filter(r=>r.date===date).sort((a,b)=>a.time.localeCompare(b.time));
  const { GROUPS, eff } = listGroups(date);
  const filters = Object.keys(GROUPS).map(f=>{''', 1)
# 폰 목록: 상태별 필터(전체/확정/방문/취소/노쇼)가 view.filter 기본값 '예정' 을 몰라 늘 비어 보였음(검토 B1)
s = rep(s, '''function renderAgenda(date){
  const s = store();
  let day = s.reservations.filter(r=>r.date===date).sort((a,b)=>a.time.localeCompare(b.time));
  const filters = ["전체",...STATUS].map(f=>{
    const n = f==="전체" ? day.length : day.filter(r=>r.status===f).length;
    return `<button class="${view.filter===f?'on':''}" onclick="setFilter('${f}')">${f} ${n}</button>`;
  }).join("");
  if(view.filter!=="전체") day = day.filter(r=>r.status===view.filter);
  const rows = day.length ? day.map(resRowMobile).join("") : `<div class="empty">해당 조건의 예약이 없습니다.</div>`;
  return `<div class="filters">${filters}</div><div class="mlist">${rows}</div>`;
}''',
'''function renderAgenda(date){
  const s = store();
  let day = s.reservations.filter(r=>r.date===date).sort((a,b)=>a.time.localeCompare(b.time));
  const { GROUPS, eff } = listGroups(date);
  const filters = Object.keys(GROUPS).map(f=>{
    const n = day.filter(GROUPS[f]).length;
    return `<button class="${eff===f?'on':''}" onclick="setFilter('${f}')">${f} ${n}</button>`;
  }).join("");
  if(eff!=="전체") day = day.filter(GROUPS[eff]);
  const nowM = toMin(nowHM()), isToday = date === todayStr();
  let marked = false;
  const rows = day.length ? day.map(r=>{
    let m = "";
    if(isToday && !marked && toMin(r.time) > nowM){ marked = true; m = `<div class="now-sep"><span>지금 | ${hm(nowHM())}</span></div>`; }
    return m + resRowMobile(r);
  }).join("") + (isToday && !marked ? `<div class="now-sep"><span>지금 | ${hm(nowHM())} · 오늘 남은 예약 없음</span></div>` : "")
    : `<div class="empty">${eff === "예정" ? "앞으로 남은 예약이 없습니다. 지난 것은 '지난·방문' 또는 '전체'." : "해당 조건의 예약이 없습니다."}</div>`;
  return `<div class="filters">${filters}</div><div class="mlist">${rows}</div>`;
}''', 1)
# PC 목록의 빈 문구도 같은 안내
s = rep(s, '''    : `<div class="empty">해당 조건의 예약이 없습니다.</div>`;
  return `<div class="filters">${filters}</div><div class="rlist">${rows}</div>`;''',
'''    : `<div class="empty">${eff === "예정" ? "앞으로 남은 예약이 없습니다. 지난 것은 '지난·방문' 또는 '전체'." : "해당 조건의 예약이 없습니다."}</div>`;
  return `<div class="filters">${filters}</div><div class="rlist">${rows}</div>`;''', 1)
save("js/07-dash.js", s)
print("ok")
