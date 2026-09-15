# -*- coding: utf-8 -*-
"""v6 8차-I — H 의 모순 정리: 계산은 테이블 단위(숨김), 화면은 층
   · 테이블 예약(seatPref "table:<층>")도 잠정 배정을 다시 계산합니다 — 단 이름은 어디에도 안 보여 줍니다(층까지만)
   · findSeat 에 floor 제한 + 붙일 조합이 없으면 '나눠 앉기'(빈 테이블 여러 개, 붙임 무관) 로 잡고 split 표시 → 경고만
   · 여포는 지하 테이블 후보 그대로(최소 4·붙임 불가·순서 맨 앞 = 우선)
   · 마법사 층 카드: 자리 있음 / 나눠 앉기 / 자리 없음(한 자리 최대 N명). 남은 자리 '석' 계산(floorLoad) 은 안 씀
   · 타임라인 칸 병합은 숨은 배정(테이블 개수)대로. 나눠 앉기는 ↔ 표시
   · 예약률은 테이블 개수 기준으로 복귀
   · 경고: '테이블 자리 없음' / '나눠 앉음'"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- findSeat: floor 제한 + 나눠 앉기 ----------
s = R(s, """  if(wantTable){
    const tables = seats.filter(x=>isTable(x) && people >= roomMin(x) && people <= seatMax(x));""",
"""  if(wantTable){
    /* 층을 정한 테이블 예약("table:1층")은 그 층 안에서만. 층 미정(옛 table-any)은 전체 */
    const inFloor = x => o.floor == null || (x.floor||"") === (o.floor||"");
    const tables = seats.filter(x=>isTable(x) && inFloor(x) && people >= roomMin(x) && people <= seatMax(x));""")
s = R(s, """    const pool = seats.filter(x=>isTable(x) && (x.joinWith||[]).length && ((o.confirmedOnly || o.strict) ? free(x.id) : freeLoose(x.id)));""",
"""    const pool = seats.filter(x=>isTable(x) && inFloor(x) && (x.joinWith||[]).length && ((o.confirmedOnly || o.strict) ? free(x.id) : freeLoose(x.id)));""")
s = R(s, """    pool.forEach(x=>tryCombo([x], x.seats||4));
    if(best) return {id:best.combo[0].id, extra:best.combo.slice(1).map(x=>x.id)};""",
"""    pool.forEach(x=>tryCombo([x], x.seats||4));
    if(best) return {id:best.combo[0].id, extra:best.combo.slice(1).map(x=>x.id)};
    /* 나눠 앉기(재아 결정) — 붙일 조합이 없으면 빈 테이블 여러 개에 나눠 앉는 것으로 잡습니다. 붙임 여부는 안 봅니다.
       큰 테이블부터 채워 개수를 최소로. 결과에 split 을 붙여 화면에서는 경고로만 알립니다(막지 않음) */
    if(!o.noSplit){
      const freeT = seats.filter(x=>isTable(x) && inFloor(x) && !(roomMin(x) > people && false) && ((o.confirmedOnly || o.strict) ? free(x.id) : freeLoose(x.id)))
        .sort((x,y)=>(y.seats||4)-(x.seats||4));
      let sum = 0; const pick = [];
      for(const t of freeT){ if(sum >= people) break; pick.push(t); sum += (t.seats||4); }
      if(sum >= people && pick.length > 1) return {id:pick[0].id, extra:pick.slice(1).map(x=>x.id), split:true};
    }""")
# 그 층에서 한 자리로 앉힐 수 있는 최대 인원(붙임 포함, 나눠 앉기 제외) — 안내 문구용
s = R(s, """function floorLabel(fl){ return `${fl || ""} 테이블`.trim(); }""",
"""function floorLabel(fl){ return `${fl || ""} 테이블`.trim(); }
/* 그 시각에 그 층에서 한 자리(붙임 포함)로 앉힐 수 있는 최대 인원 — 마법사 안내용. 20명부터 내려가며 찾습니다 */
function floorMaxParty(fl, date, time, excludeId){
  for(let p = 21; p >= 1; p--) if(findSeat({date, time, people:p, kind:"table-any", floor:fl, excludeId, noSplit:true})) return p;
  return 0;
}
/* 테이블 예약(층)의 숨은 배정 결과 — {state:"ok"|"split"|"none", f} */
function floorFit(fl, date, time, people, excludeId){
  const f = findSeat({date, time, people, kind:"table-any", floor:fl, excludeId});
  return { state: !f ? "none" : (f.split ? "split" : "ok"), f };
}""")

# ---------- 잠정 배정: 테이블 예약도 계산(숨김) ----------
s = R(s, """  targets.forEach(r=>{ r.tentativeRoomId = null; r.tentativeExtra = []; });
  /* 테이블 예약은 층 단위라 잠정 배정이 없습니다 — 룸 희망만 */
  targets.splice(0, targets.length, ...targets.filter(r=>!isTablePref(r.seatPref)));
  targets.sort((a,b)=>a.time.localeCompare(b.time)).forEach(r=>{
    const f = findSeat({date:r.date, time:r.time, people:pplOf(r), kind:r.seatPref||"any", excludeId:r.id, strict:true});
    r.tentativeRoomId = f ? f.id : null; r.tentativeExtra = f && f.extra.length ? f.extra : [];
  });""",
"""  targets.forEach(r=>{ r.tentativeRoomId = null; r.tentativeExtra = []; r.tentativeSplit = false; });
  /* 테이블 예약(층)도 계산은 테이블 단위로 합니다 — 화면에는 층까지만 보이고, 겹침·붙임·나눠 앉기 판단에 씁니다 */
  targets.sort((a,b)=>a.time.localeCompare(b.time)).forEach(r=>{
    const fl = prefFloor(r.seatPref);
    const f = findSeat({date:r.date, time:r.time, people:pplOf(r), kind:isTablePref(r.seatPref) ? "table-any" : (r.seatPref||"any"), floor:fl, excludeId:r.id, strict:true});
    r.tentativeRoomId = f ? f.id : null; r.tentativeExtra = f && f.extra.length ? f.extra : []; r.tentativeSplit = !!(f && f.split);
  });""")
s = R(s, """    s.reservations.forEach(function(r){ if(r.date >= today && !r.roomId && !isTablePref(r.seatPref) && holdsSeat(r)) dates[r.date] = 1; });""",
"""    s.reservations.forEach(function(r){ if(r.date >= today && !r.roomId && holdsSeat(r)) dates[r.date] = 1; });""")
# 로드 때 테이블 잠정을 지우던 것 삭제
s = R(s, """      /* 테이블(층) 예약에는 잠정 배정이 없습니다(8차-H) — 옛 값이 남아 있으면 룸 줄에 겹쳐 보였습니다 */
      if(isTablePref(r.seatPref) && (r.tentativeRoomId || (r.tentativeExtra||[]).length)){ r.tentativeRoomId = null; r.tentativeExtra = []; }
""", "")
# syncMarkTentatives 가 tentativeExtra/Split 도 같이 봐야 — 확인
s = R(s, """      try{ var was = JSON.parse(SYNC.res[r.id]); if(was.tentativeRoomId !== r.tentativeRoomId){ was.tentativeRoomId = r.tentativeRoomId;""",
"""      try{ var was = JSON.parse(SYNC.res[r.id]); if(was.tentativeRoomId !== r.tentativeRoomId || JSON.stringify(was.tentativeExtra||[]) !== JSON.stringify(r.tentativeExtra||[]) || !!was.tentativeSplit !== !!r.tentativeSplit){ was.tentativeRoomId = r.tentativeRoomId; was.tentativeExtra = r.tentativeExtra || []; was.tentativeSplit = !!r.tentativeSplit;""")

# ---------- 라벨: 테이블 예약의 잠정 이름은 숨김 ----------
s = R(s, """function resTentLabel(r){ return r.tentativeRoomId ? seatLabelIds([r.tentativeRoomId].concat(r.tentativeExtra||[])) : ""; }""",
"""function resTentLabel(r){
  if(isTablePref(r.seatPref)) return "";   /* 테이블 예약의 숨은 배정은 이름을 보여 주지 않습니다 — 층까지만 */
  return r.tentativeRoomId ? seatLabelIds([r.tentativeRoomId].concat(r.tentativeExtra||[])) : "";
}""")

# ---------- 경고 ----------
s = R(s, """  /* 테이블 예약(층 단위): 같은 시간대 손님 수가 그 층 자리 수를 넘으면 */
  if(!seat && isTablePref(r.seatPref) && r.status!=="취소" && prefFloor(r.seatPref) != null){
    if(floorLoad(r.date, r.time, prefFloor(r.seatPref), r.id) + pplOf(r) > floorSeats(prefFloor(r.seatPref), r.date, r.time)) out.push("테이블 자리 부족");
  }""",
"""  /* 테이블 예약(층): 숨은 배정 결과로 — 자리가 아예 없으면, 붙일 수 없어 나눠 앉으면 */
  if(!seat && isTablePref(r.seatPref) && r.status!=="취소"){
    if(!r.tentativeRoomId) out.push("테이블 자리 없음");
    else if(r.tentativeSplit) out.push("나눠 앉음");
  }""")
s = R(s, """    "테이블 자리 부족": (function(){ const fl = prefFloor(rec.seatPref); return `${floorLabel(fl)} 자리가 부족합니다 — 그 시간에 ${floorLoad(rec.date, rec.time, fl, excludeId)}명 앉아 있고 자리는 ${floorSeats(fl, rec.date, rec.time)}석`; })()""",
"""    "테이블 자리 없음": `${seatLabel(rec.seatPref)}에 그 시간 ${pplOf(rec)}명이 앉을 자리가 없습니다 (한 자리 최대 ${floorMaxParty(prefFloor(rec.seatPref), rec.date, rec.time, excludeId)}명)`,
    "나눠 앉음": `${seatLabel(rec.seatPref)}에 붙일 수 있는 테이블이 없어 나눠 앉게 됩니다 (한 자리 최대 ${floorMaxParty(prefFloor(rec.seatPref), rec.date, rec.time, excludeId)}명)`""")
# saveIssues 는 resWarn(rec) 를 쓰는데 rec 은 아직 잠정 계산 전 — 층 예약이면 즉석 계산
s = R(s, """  resWarn(rec).forEach(k => { if(words[k]) out.push(words[k]); });""",
"""  if(!rec.roomId && isTablePref(rec.seatPref)){
    /* 저장 전 객체라 잠정 배정이 아직 없습니다 — 즉석에서 계산해 넣고 경고를 뽑습니다 */
    const ff = floorFit(prefFloor(rec.seatPref), rec.date, rec.time, pplOf(rec), excludeId);
    rec.tentativeRoomId = ff.f ? ff.f.id : null; rec.tentativeExtra = ff.f ? ff.f.extra : []; rec.tentativeSplit = ff.state === "split";
  }
  resWarn(rec).forEach(k => { if(words[k]) out.push(words[k]); });""")

# ---------- 마법사 층 카드 ----------
s = R(s, """    const floors = tableFloors();
    body = `<div class="sgrid floors">${floors.map(fl=>{
      const key = "table:" + fl, seats = floorSeats(fl, WZ.date, WZ.time), left = WZ.time ? floorLeft(WZ.date, WZ.time, fl) : seats;
      const short = WZ.time && left < total;
      return `<button class="scell ${WZ.seat===key?'on':''} ${short?'warned busy':''}" onclick="wzSeat('${key}')">
        <span class="sn">${esc(floorLabel(fl))}</span>
        <span class="sc">자리 ${seats}석</span>
        <span class="avail ${short?'warn':'free'}">${WZ.time ? (short ? `남은 자리 ${Math.max(0,left)}석 · 부족` : `남은 자리 ${left}석`) : "시간을 먼저"}</span>
      </button>`; }).join("")}</div>`;""",
"""    const floors = tableFloors();
    body = `<div class="sgrid floors">${floors.map(fl=>{
      const key = "table:" + fl, tb = floorTables(fl);
      const fit = WZ.time ? floorFit(fl, WZ.date, WZ.time, total) : null;
      const bad = fit && fit.state !== "ok";
      const txt = !fit ? "시간을 먼저" : fit.state === "ok" ? "자리 있음"
                : fit.state === "split" ? `붙일 테이블 없음 · 나눠 앉기 (한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명)`
                : `자리 없음 (한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명)`;
      return `<button class="scell ${WZ.seat===key?'on':''} ${bad?'warned busy':''}" onclick="wzSeat('${key}')">
        <span class="sn">${esc(floorLabel(fl))}</span>
        <span class="sc">테이블 ${tb.length} · ${tb.reduce((a,t)=>a+(t.seats||4),0)}석</span>
        <span class="avail ${bad?'warn':'free'}">${txt}</span>
      </button>`; }).join("")}</div>`;""")
s = R(s, """    <div class="lbl-note" style="margin:6px 0 10px">${kind==='room' ? `정원은 ${seatCountsInfants()?"유아 포함":"유아 제외 성인"} 기준 · 순서는 사장님이 정한 배정 우선순위` : "남은 자리 = 그 층 자리 수 − 같은 시간대에 앉아 있는 손님 수"}</div>""",
"""    <div class="lbl-note" style="margin:6px 0 10px">${kind==='room' ? `정원은 ${seatCountsInfants()?"유아 포함":"유아 제외 성인"} 기준 · 순서는 사장님이 정한 배정 우선순위` : "그 시간에 비는 테이블(붙임 포함)로 앉힐 수 있는지 봅니다. 어느 테이블인지는 당일 현장에서"}</div>""")
s = R(s, """  /* 테이블(층) — 자리 수만 보고, 부족해도 알리기만 */
  if(/^table:/.test(v)){
    const fl = v.slice(6), left = floorLeft(WZ.date, WZ.time, fl);
    if(left < people && !await uiConfirm(`${floorLabel(fl)} 자리가 부족합니다`,
      `그 시간대에 ${floorLoad(WZ.date, WZ.time, fl)}명이 앉아 있고 자리는 ${floorSeats(fl, WZ.date, WZ.time)}석입니다.\\n지금 ${people}명 — 남은 자리 ${Math.max(0,left)}석.\\n\\n회전이나 합석으로 감당 가능하면 접수하세요.`,
      {ok:"그래도 접수", cancel:"다시 고르기"})) return;
    WZ.seat = v; wzAutoNext();
    return;
  }""",
"""  /* 테이블(층) — 테이블 단위로 앉힐 수 있는지 계산하되 이름은 안 보여 줍니다. 없거나 나눠 앉아도 알리기만 */
  if(/^table:/.test(v)){
    const fl = v.slice(6), fit = floorFit(fl, WZ.date, WZ.time, people);
    if(fit.state === "none" && !await uiConfirm(`${floorLabel(fl)}에 ${people}명 자리가 없습니다`,
      `${hm(WZ.time)} 기준으로 비는 테이블을 붙여도 한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명입니다.\\n\\n회전·합석으로 감당 가능하면 접수하세요. '테이블 자리 없음' 경고로 남습니다.`,
      {ok:"그래도 접수", cancel:"다시 고르기"})) return;
    if(fit.state === "split" && !await uiConfirm(`${floorLabel(fl)}에서는 나눠 앉게 됩니다`,
      `붙일 수 있는 테이블이 없습니다 (한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명). 옆 테이블에 나눠 앉는 것으로 접수합니다.\\n손님께 안내하셨나요?`,
      {ok:"안내했음 · 접수", cancel:"다시 고르기"})) return;
    WZ.tentative = fit.f ? fit.f.id : null; WZ.tentativeExtra = fit.f ? fit.f.extra : []; WZ.tentativeSplit = fit.state === "split";
    WZ.seat = v; wzAutoNext();
    return;
  }""")
s = R(s, """    tentativeRoomId: fixed ? null : (WZ.tentative || null),  /* 나중에 확정할 때 1순위로 뜨는 자리 */""",
"""    tentativeRoomId: fixed ? null : (WZ.tentative || null),  /* 나중에 확정할 때 1순위로 뜨는 자리 */
    tentativeSplit: fixed ? false : !!WZ.tentativeSplit,""")
# 마법사 경고(wzWarnReason)
s = R(s, """    const fl = prefFloor(WZ.seat);
    if(fl != null && WZ.time){
      const left = floorLeft(WZ.date, WZ.time, fl);
      if(left < (WZ.people||0)) out.push(`테이블 자리 부족 - ${floorLabel(fl)} 남은 자리 ${Math.max(0,left)}석 (지금 ${WZ.people}명)`);
    }""",
"""    const fl = prefFloor(WZ.seat);
    if(fl != null && WZ.time){
      const fit = floorFit(fl, WZ.date, WZ.time, WZ.people||0);
      if(fit.state === "none") out.push(`테이블 자리 없음 - ${floorLabel(fl)} 한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명 (지금 ${WZ.people}명)`);
      else if(fit.state === "split") out.push(`나눠 앉음 - ${floorLabel(fl)}에 붙일 테이블이 없어 옆 테이블에 나눠 앉습니다`);
    }""")

# ---------- 좌석 배정 시트 문구 ----------
s = R(s, """    seatPick = fl != null ? `<div class="lbl" style="margin:16px 0 8px">테이블 자리</div>
      <p class="f-note">${esc(floorLabel(fl))} · 그 시간대 ${floorLoad(r.date, r.time, fl, r.id) + pplOf(r)}명 / 자리 ${floorSeats(fl, r.date, r.time)}석. 어느 테이블에 앉을지는 당일 현장에서 정합니다. 특정 테이블(파셜룸 등)을 잡으려면 '수정' 에서 고르세요.</p>` : "";""",
"""    const st8 = !r.tentativeRoomId ? `<b style="color:var(--rust)">자리 없음</b> — 한 자리 최대 ${floorMaxParty(fl, r.date, r.time, r.id)}명`
              : r.tentativeSplit ? `<b style="color:var(--rust)">나눠 앉음</b> — 테이블 ${seatsOf(r).length}개, 붙일 수 없음`
              : `자리 있음 — 테이블 ${seatsOf(r).length}개`;
    seatPick = `<div class="lbl" style="margin:16px 0 8px">테이블 자리</div>
      <p class="f-note">${esc(floorLabel(fl))} · ${st8}. 어느 테이블에 앉을지는 당일 현장에서 정합니다. 특정 테이블(파셜룸 등)을 잡으려면 '수정' 에서 고르세요.</p>`;""")

# ---------- 타임라인: 칸 병합은 숨은 배정대로 ----------
s = R(s, """    const needOf = r => {
      if(r.roomId) return Math.max(1, seatsOf(r).length);            /* 특정 테이블을 잡았으면 그 개수 */
      let sum = 0, n = 0; for(const sz of sizes){ if(sum >= pplOf(r)) break; sum += sz; n++; }   /* 큰 테이블부터 채워 몇 개 필요한지 */
      return Math.max(1, n);
    };""",
"""    /* 칸 수 = 숨은 배정(붙임·나눠 앉기 포함)이 쓰는 테이블 개수. 자리를 못 찾은 예약은 1칸 + 경고 */
    const needOf = r => Math.max(1, seatsOf(r).length);""")
s = R(s, """      const h = (it.lane===null ? 1 : it.need) * LANE - 2;   /* 테이블 n개 필요 → n칸 높이로 병합 */
      return `<button class="blk ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''} ${it.need>1?'multi':''}" onclick="openMark('${it.r.id}')"
        style="left:${pos(it.s0)}%; width:${w}%; bottom:${lane*LANE+1}px; height:${h}px"
        title="${esc(it.r.time)} ${esc(it.r.name)} ${pplText(it.r)}${tn?` · ${esc(tn)} 테이블 지정`:""}${chg?` · 오늘 ${esc(chg.label)}`:""}">
        ${chg?`<span class="chg-chip">${blockLabel(it.r)}</span>`:blockLabel(it.r)}${tn?` <small class="tn">${esc(tn)}</small>`:""}</button>`;""",
"""      const h = (it.lane===null ? 1 : it.need) * LANE - 2;   /* 테이블 n개 → n칸 높이로 병합 */
      const split = !it.r.roomId && it.r.tentativeSplit, none = !it.r.roomId && !it.r.tentativeRoomId;
      return `<button class="blk ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''} ${it.need>1?'multi':''} ${split?'split':''}" onclick="openMark('${it.r.id}')"
        style="left:${pos(it.s0)}%; width:${w}%; bottom:${lane*LANE+1}px; height:${h}px"
        title="${esc(it.r.time)} ${esc(it.r.name)} ${pplText(it.r)}${tn?` · ${esc(tn)} 테이블 지정`:""}${split?" · 나눠 앉음":""}${none?" · 자리 없음":""}${chg?` · 오늘 ${esc(chg.label)}`:""}">
        ${split?'<i class="jn">↔</i>':''}${chg?`<span class="chg-chip">${blockLabel(it.r)}</span>`:blockLabel(it.r)}${tn?` <small class="tn">${esc(tn)}</small>`:""}</button>`;""")
# 예약률 계산: 테이블 개수 기준으로 복귀
s = R(s, """  /* 테이블은 층 단위라 '좌석 수' 가 아니라 '손님 수 / 자리 수' 로 — 테이블 예약(층 희망·특정 테이블 모두) 인원 × 시간 */
  const hallUsed = list.reduce((a,r)=>a + (resFloor(r) !== undefined ? pplOf(r) * spanOf(r) : 0), 0);""",
"""  const hallUsed = list.reduce((a,r)=>a + (noSeat(r) ? (r.seatPref==="room-any" ? 0 : 1) : seatsOf(r).filter(id=>halls.some(x=>x.id===id)).length) * spanOf(r), 0);""")
s = R(s, """  const hallT = halls.reduce((a,t)=>a+(t.seats||4), 0);   /* 테이블 자리 수 합 (8차-H: 테이블 개수가 아니라 인원) */""",
"""  const hallT = halls.length;""")
s = R(s, """  const hallDen = Math.max(0, hallN*span - halls.reduce((a,h)=>a+blockedOf(h)*(h.seats||4),0));""",
"""  const hallDen = Math.max(0, hallN*span - halls.reduce((a,h)=>a+blockedOf(h),0));""")
s = R(s, """  const seatAll = roomN + hallN;        /* 룸 1개 = 좌석 1, 테이블은 자리 수(인원) */""",
"""  const seatAll = roomN + hallN;        /* 룸 1개 = 좌석 1, 테이블 1개 = 좌석 1 */""")
# 층 줄 예약률 — 테이블 개수 기준
s = R(s, """    const used = items.reduce((a,x)=>a+pplOf(x.r)*(x.e0-x.s0),0);
    const rate = seats ? Math.min(100, Math.round(used/(seats*span)*100)) : 0;""",
"""    const used = items.reduce((a,x)=>a+x.need*(x.e0-x.s0),0);
    const rate = tbls.length ? Math.min(100, Math.round(used/(tbls.length*span)*100)) : 0;""")
s = R(s, """    const sizes = tbls.map(t=>t.seats||4).sort((a,b)=>b-a);
""", "")

L.js_check(s)
L.save(s)
print("p9_i ok")
