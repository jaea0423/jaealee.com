# -*- coding: utf-8 -*-
"""8차-Z — 재아: 예약 목록 '예정' 에 방문 처리된 앞 예약도(흐리게), 지난 날짜가 아니면 '예정' 이 기본, 접힌 목록 아래 여백(PC 60~80px) 정리,
   마법사 제목 양옆 이전/다음(못 가면 연하게)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 목록 필터 ----------
s = R(s, """  const GROUPS = { "전체": r=>true, "예정": r=>r.status==="확정" && !isPastRes(r), "지난·방문": r=>r.status==="방문" || (r.status==="확정" && isPastRes(r)), "취소·노쇼": r=>r.status==="취소" || r.status==="노쇼" };
  if(!GROUPS[view.filter]) view.filter = "전체";
  const filters = Object.keys(GROUPS).map(f=>{
    const n = s.reservations.filter(r=>r.date===date && GROUPS[f](r)).length;
    return `<button class="${view.filter===f?'on':''}" onclick="setFilter('${f}')">${f} ${n}</button>`;
  }).join("");
  if(view.filter!=="전체") day = day.filter(GROUPS[view.filter]);""",
"""  /* '예정' 에는 아직 시각이 안 지난 '방문' 도 흐리게 넣습니다 — 잘못 누른 방문 처리를 눈치채게(8차-Z 재아) */
  const GROUPS = { "전체": r=>true, "예정": r=>(r.status==="확정" || r.status==="방문") && !isPastRes(r), "지난·방문": r=>r.status==="방문" || (r.status==="확정" && isPastRes(r)), "취소·노쇼": r=>r.status==="취소" || r.status==="노쇼" };
  if(!GROUPS[view.filter]) view.filter = "예정";
  /* 기본은 '예정'. 지난 날짜에서는 예정이 늘 비므로 그때만 '전체' 로 보여 줍니다(버튼도 전체가 켜짐) */
  const eff = (view.filter === "예정" && date < todayStr()) ? "전체" : view.filter;
  const filters = Object.keys(GROUPS).map(f=>{
    const n = s.reservations.filter(r=>r.date===date && GROUPS[f](r)).length;
    return `<button class="${eff===f?'on':''}" onclick="setFilter('${f}')">${f} ${n}</button>`;
  }).join("");
  if(eff!=="전체") day = day.filter(GROUPS[eff]);""")
s = R(s, """let view = { storeKey:null, tab:"dash", date:todayStr(), filter:"전체",""",
         """let view = { storeKey:null, tab:"dash", date:todayStr(), filter:"예정",""")

# ---------- 접힌 목록 아래 여백: PC 에는 둥근 등록 버튼(FAB)이 없으니 큰 아래 여백이 필요 없습니다 ----------
s = R(s, """@media (min-width:768px){
  .content{padding:var(--s24) var(--s24) 80px}""",
"""@media (min-width:768px){
  .content{padding:var(--s24) var(--s24) var(--s24)}   /* 아래 80px 은 폰의 FAB 자리였습니다 — 태블릿·PC 에서는 접힌 목록 밑에 빈 띠만 남겼습니다(재아) */""")
s = R(s, """  .content{padding:var(--s24) var(--s24) 60px; max-width:1720px; margin:0 auto}""",
         """  .content{padding:var(--s24) var(--s24) var(--s24); max-width:1720px; margin:0 auto}""")

# ---------- 마법사 제목 양옆 이전/다음 ----------
s = R(s, """      <div class="wz-q">
        <h2>${WZ_STEPS[WZ.step]}</h2>""",
"""      <div class="wz-q">
        <button class="wz-side prev ${WZ.step===0?'off':''}" onclick="wzGo(${WZ.step-1})" ${WZ.step===0?"disabled":""} aria-label="이전">‹ 이전</button>
        <h2>${WZ_STEPS[WZ.step]}</h2>
        <button class="wz-side next ${canNext?'':'off'}" onclick="${last?'wzSubmit()':`wzGo(${WZ.step+1})`}" ${canNext?"":"disabled"} aria-label="다음">${last?"등록":"다음"} ›</button>""")
s = R(s, """.wz-q{text-align:center; padding:var(--s8) var(--s16) var(--s4)}""",
""".wz-q{text-align:center; padding:var(--s8) var(--s16) var(--s4); display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:var(--s12)}
.wz-q h2{grid-column:2}
.wz-q .wz-warn{grid-column:1 / -1}
/* 제목 양옆 이전/다음(8차-Z 재아) — 못 가는 쪽은 연하게. 아래 큰 '다음' 은 그대로 */
.wz-side{background:var(--surface); border:1px solid var(--border-strong); border-radius:999px; padding:var(--s8) var(--s16); font-size:var(--fs-body); font-weight:700; color:var(--text); cursor:pointer; white-space:nowrap}
.wz-side.prev{justify-self:start} .wz-side.next{justify-self:end}
.wz-side.off{opacity:.3; cursor:default}
@media (max-width:767px){ .wz-side{display:none} }""")

L.js_check(s)
L.save(s)
print("p9_z 적용")
