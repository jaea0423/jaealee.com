# -*- coding: utf-8 -*-
"""v6 8차-B — 규칙·저장·시트·마법사 좌석 단계 (테이블 개별 + 룸 합침)
   · saveIssues/resWarn: 좌석 묶음(대표+합침) 기준으로 겹침·정원·최소 검사, '접수 마감 이후' 경고
   · timeWarns: 세션의 접수 마감(lastBook) 기준. 라스트오더는 주방 마감 안내로만
   · 상세 시트 후보·좌석 확정(assignSeat): 룸/테이블/합침 그룹, extraIds
   · 마법사 3단계: 룸 | 테이블 두 단계 + 미정. 합침 그룹은 룸 쪽에 표시(자동 배정 안 함, 원탁 확인창)
   · 수정 시트 좌석 select: 룸 / 테이블 / 합침 묶음
   · 라벨: seatLabel(id|join id|table-any), resSeatLabel(r)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()

# ---------- 라벨 ----------
s = L.replace_fn(s, "seatLabel", """function seatLabel(seat){
  const st = store().settings;
  if(seat==="any") return "좌석 상관없음";
  if(seat==="hall-any" || seat==="table-any") return "테이블 중 아무곳";
  if(seat==="room-any") return "룸 중 아무곳";
  const j = (st.joins||[]).find(g=>g.id===seat);
  if(j) return j.ids.map(id=>{ const x = seatById(id); return x ? x.name : "?"; }).join("+") + " 룸";
  const r = seatById(seat);
  if(!r) return "미배정";
  /* 이름 뒤에 종류를 붙여 직원이 바로 알게 — '조조 룸', '21 테이블' */
  return r.type==="room" ? `${r.name} 룸` : `${r.name} 테이블`;
}
/* 여러 좌석(합침) 라벨 — '장비+관우 룸', '하후돈+하후상-1 테이블' */
function seatLabelIds(ids){
  if(!ids || !ids.length) return "미배정";
  if(ids.length===1) return seatLabel(ids[0]);
  const xs = ids.map(seatById).filter(Boolean);
  const kind = xs.length && xs[0].type==="room" ? " 룸" : " 테이블";
  return xs.map(x=>x.name).join("+") + kind;
}
/* 예약의 확정 좌석 라벨 / 잠정 좌석 라벨 */
function resSeatLabel(r){ return r.roomId ? seatLabelIds([r.roomId].concat(r.extraIds||[])) : "미배정"; }
function resTentLabel(r){ return r.tentativeRoomId ? seatLabelIds([r.tentativeRoomId].concat(r.tentativeExtra||[])) : ""; }""")
# 확정/잠정 라벨 호출부 교체
for old, new in [("seatLabel(r.roomId)", "resSeatLabel(r)"), ("seatLabel(r.tentativeRoomId)", "resTentLabel(r)"),
                 ("seatLabel(x.roomId)", "resSeatLabel(x)")]:
    s = s.replace(old, new)

# ---------- 접수 마감 (timeWarns) ----------
s = L.rep(s, """  const stx = store().settings;
  const lo = lastBookMin(date);
  const loTxt = hm(dh.lo || minToHM(lo));
  const t = toMin(time);
  const end = t + stayMinAt(date, time);

  /* 문구는 짧게, 대신 '남은 시간'을 함께 — 직원이 손님께 "주문 가능 시간이 40분입니다" 라고 바로 말할 수 있게.
     정확한 시각(라스트오더 몇 시)은 위 hours-line 에 이미 있으므로 여기서는 되풀이하지 않습니다 */
  if(t > lo) out.push("라스트오더 이후입니다.");
  else {
    /* 임박 기준 분은 설정에서 바꿉니다 (설정 → 운영 판단 기준) */
    const soon = stx.loSoon != null ? stx.loSoon : 120;
    if(lo - t <= soon) out.push(`라스트오더 임박 - 주문시간 ${hmDur(lo - t)}`);
  }""",
"""  const stx = store().settings;
  const t = toMin(time);
  const end = t + stayMinAt(date, time);
  /* 접수 마감(세션의 lastBook) — 식사 시간을 보장하려고 정한 마지막 입장 시각. 라스트오더(주방 마감)와 다릅니다 */
  const sess = sessionAt(date, time);
  const lb = lastBookMin(date, time);
  if(t > lb) out.push(`접수 마감 이후입니다 - ${sess?sess.name+" ":""}${hm(minToHM(lb))}까지`);
  /* 라스트오더까지 남은 주문 시간 — 직원이 손님께 "주문 가능 시간이 40분입니다" 라고 바로 말할 수 있게 */
  if(dh.lo){
    const lo = toMin(dh.lo);
    if(t > lo) out.push("라스트오더 이후입니다.");
    else { const soon = stx.loSoon != null ? stx.loSoon : 120; if(lo - t <= soon) out.push(`라스트오더 임박 - 주문시간 ${hmDur(lo - t)}`); }
  }""")
s = L.rep(s, """  if(msg.indexOf("브레이크입니다") >= 0) return "브레이크";
  if(msg.indexOf("라스트오더 이후") >= 0) return "라스트오더 지남";""",
"""  if(msg.indexOf("브레이크입니다") >= 0) return "브레이크";
  if(msg.indexOf("접수 마감") >= 0) return "접수 마감";
  if(msg.indexOf("라스트오더 이후") >= 0) return "라스트오더 지남";""")
s = L.rep(s, """  return timeWarns(date, time).filter(function(x){ return x.indexOf("라스트오더 임박") < 0; }).join("\\n");""",
    """  return timeWarns(date, time).filter(function(x){ return x.indexOf("라스트오더 임박") < 0; }).join("\\n");   /* 임박은 알림만, 확인창은 안 띄움 */""")

# ---------- resWarn ----------
s = L.rep(s, """    if(toMin(r.time) < toMin(h.open) || toMin(r.time) >= toMin(h.close)) out.push("영업시간 밖");
    else if(h.lo && toMin(r.time) > toMin(h.lo)) out.push("라스트오더 이후");
    if(toMin(r.time) + stayOf(r) > toMin(h.close)) out.push("마감 넘김");
  }
  const seat = st.rooms.find(x=>x.id===r.roomId);
  if(seat && resBlocked(r)) out.push("사용 중지 좌석");
  if(seat && seat.type==="room"){
    if(pplOf(r) > seat.capacity) out.push("정원 초과");
    else if(adultCount(pplOf(r), r.infants) < roomMin(seat)) out.push("최소 인원 미달");
  }""",
"""    if(toMin(r.time) < toMin(h.open) || toMin(r.time) >= toMin(h.close)) out.push("영업시간 밖");
    else if(toMin(r.time) > lastBookMin(r.date, r.time)) out.push("접수 마감 이후");
    else if(h.lo && toMin(r.time) > toMin(h.lo)) out.push("라스트오더 이후");
    if(toMin(r.time) + stayOf(r) > toMin(h.close)) out.push("마감 넘김");
  }
  const seat = st.rooms.find(x=>x.id===r.roomId);
  const ids = r.roomId ? [r.roomId].concat(r.extraIds||[]) : [];
  if(seat && resBlocked(r)) out.push("사용 중지 좌석");
  if(seat){
    /* 룸·테이블 모두: 묶음(합침 포함)의 최대·최소로 판단. 테이블은 최소가 없고(여포만 4), 정원 초과만 봅니다 */
    if(pplOf(r) > seatsMax(ids)) out.push("정원 초과");
    else if(adultCount(pplOf(r), r.infants) < seatsMin(ids)) out.push("최소 인원 미달");
    if(ids.length > 1 && joinOf(ids) && /원탁/.test(joinOf(ids).note||"")) out.push("원탁 합침 · 손님 확인");
  }""")
s = L.rep(s, """  if(seat && seat.type==="room" && r.roomId && r.status!=="취소"){
    const rs = roomStatus(r.date, r.time, r.roomId, r.id);
    if(rs.hits.length) out.push("좌석 겹침");
  }""",
"""  if(seat && r.roomId && r.status!=="취소"){
    if(ids.some(id=>roomStatus(r.date, r.time, id, r.id).hits.length)) out.push("좌석 겹침");
  }""")
s = L.rep(s, """function resBlocked(r){
  if(!r.roomId) return null;
  const room = store().settings.rooms.find(x=>x.id===r.roomId);
  if(!room) return null;
  const spans = blockSpans(room, r.date);
  const s = toMin(r.time), e = s + stayOf(r);
  for(let i=0;i<spans.length;i++) if(s < spans[i].e && spans[i].s < e) return spans[i];
  return null;
}""",
"""function resBlocked(r){
  if(!r.roomId) return null;
  const ids = [r.roomId].concat(r.extraIds||[]);
  const s = toMin(r.time), e = s + stayOf(r);
  for(let k=0;k<ids.length;k++){
    const room = seatById(ids[k]); if(!room) continue;
    const spans = blockSpans(room, r.date);
    for(let i=0;i<spans.length;i++) if(s < spans[i].e && spans[i].s < e) return spans[i];
  }
  return null;
}""")

# ---------- saveIssues ----------
s = L.rep(s, """  const seat = st.rooms.find(x=>x.id===rec.roomId);
  if(seat){
    const bk = blockedAt(seat, rec.date, rec.time);
    if(bk) out.push(`${seat.name}은 이 시각에 사용 중지입니다${bk.note?` — ${bk.note}`:""}`);
    const ppl = pplOf(rec), ad = adultCount(ppl, rec.infants||0);
    if(seat.type==="room"){
      const rs = roomStatus(rec.date, rec.time, seat.id, excludeId);
      if(rs.hits.length)
        out.push(`${seat.name}에 겹치는 예약이 있습니다 — ` +
          rs.hits.map(x=>`${hm(x.time)} ${x.name} 손님`).join(", "));
      if(ppl > seat.capacity) out.push(`${seat.name} 정원 ${seat.capacity}명을 넘습니다 (지금 ${ppl}명)`);
      else if(ad < roomMin(seat)) out.push(`${seat.name} 최소 인원 ${roomMin(seat)}명에 못 미칩니다 (지금 ${ad}명)`);
    }else{
      const h = hallStatus(rec.date, rec.time, seat.id, excludeId);
      if(!hallFits(h, ppl)) out.push(`${seat.name}에 ${ppl}명 앉힐 자리가 부족합니다`);
    }
  }""",
"""  const ids = rec.roomId ? [rec.roomId].concat(rec.extraIds||[]) : [];
  if(ids.length){
    const ppl = pplOf(rec), ad = adultCount(ppl, rec.infants||0), label = seatLabelIds(ids);
    ids.forEach(id=>{
      const seat = seatById(id); if(!seat) return;
      const bk = blockedAt(seat, rec.date, rec.time);
      if(bk) out.push(`${seat.name}은 이 시각에 사용 중지입니다${bk.note?` — ${bk.note}`:""}`);
      const rs = roomStatus(rec.date, rec.time, id, excludeId);
      if(rs.hits.length)
        out.push(`${seat.name}에 겹치는 예약이 있습니다 — ` + rs.hits.map(x=>`${hm(x.time)} ${x.name} 손님`).join(", "));
    });
    if(ppl > seatsMax(ids)) out.push(`${label} 정원 ${seatsMax(ids)}명을 넘습니다 (지금 ${ppl}명)`);
    else if(ad < seatsMin(ids)) out.push(`${label} 최소 인원 ${seatsMin(ids)}명에 못 미칩니다 (지금 ${ad}명)`);
    const j = ids.length > 1 ? joinOf(ids) : null;
    if(j && j.note) out.push(`${label}: ${j.note}`);
  }""")

# ---------- 수정 시트: 좌석 select + 저장 ----------
s = L.rep(s, """  const roomOpts = st.rooms.map(r=>`<option value="${r.id}" ${f.roomId===r.id?'selected':''}>${
    r.type==="hall"?"[홀] ":""}${esc(r.name)}${r.type==="room"?` · ${roomMin(r)}~${r.capacity}인`:""}</option>`).join("");""",
"""  /* 룸 / 테이블 / 합침 묶음. 합침은 대표+extraIds 로 저장되며 select 값은 그룹 id */
  const curJoin = (f.extraIds||[]).length ? joinOf([f.roomId].concat(f.extraIds)) : null;
  const opt = (v, label, sel) => `<option value="${v}" ${sel?'selected':''}>${label}</option>`;
  const roomOpts = `<optgroup label="룸">${st.rooms.filter(isRoom).map(r=>opt(r.id, `${esc(r.name)} · ${roomMin(r)}~${r.capacity}인`, !curJoin && f.roomId===r.id)).join("")}</optgroup>` +
    `<optgroup label="룸 합침">${(st.joins||[]).map(j=>opt(j.id, `${esc(seatLabel(j.id))} · ${j.min}~${j.max}인`, !!curJoin && curJoin.id===j.id)).join("")}</optgroup>` +
    `<optgroup label="테이블">${st.rooms.filter(isTable).map(r=>opt(r.id, `${esc(r.floor||"")} ${esc(r.name)} · ${roomMin(r)?roomMin(r)+"~":""}${seatMax(r)}인`, !curJoin && f.roomId===r.id)).join("")}</optgroup>` +
    ((f.extraIds||[]).length && !curJoin ? `<optgroup label="현재">${opt("__keep", esc(seatLabelIds([f.roomId].concat(f.extraIds))) + " (붙임 유지)", true)}</optgroup>` : "");""")
s = L.rep(s, """function pickRoom(v){ syncRes(); tmpRes = {...tmpRes, roomId:v}; render(); }""",
"""function pickRoom(v){
  syncRes();
  const j = (store().settings.joins||[]).find(g=>g.id===v);
  if(v === "__keep") return render();
  if(j) tmpRes = Object.assign({}, tmpRes, {roomId:j.ids[0], extraIds:j.ids.slice(1)});
  else  tmpRes = Object.assign({}, tmpRes, {roomId:v, extraIds:[]});
  render();
}""")
s = L.rep(s, """  const seatObj = st.rooms.find(x=>x.id===f.roomId);
  const isHall = seatObj ? seatObj.type==="hall" : false;""",
"""  const seatObj = st.rooms.find(x=>x.id===f.roomId);
  const isHall = seatObj ? isTable(seatObj) : false;""")
s = L.rep(s, """  [["date","f-date"],["time","f-time"],["name","f-name"],["phone","f-phone"],
   ["roomId","f-room"],["sourceDetail","f-src-detail"],["request","f-request"],["allergy","f-allergy"],""",
"""  [["date","f-date"],["time","f-time"],["name","f-name"],["phone","f-phone"],
   ["sourceDetail","f-src-detail"],["request","f-request"],["allergy","f-allergy"],""")
s = L.rep(s, """    roomId: f.roomId || null,
    seatPref: f.roomId ? null : (old ? old.seatPref : "any"),
    tentativeRoomId: f.roomId ? null : (old ? old.tentativeRoomId : null),""",
"""    roomId: f.roomId || null,
    extraIds: f.roomId ? (f.extraIds || []) : [],
    seatPref: f.roomId ? null : (old ? old.seatPref : "table-any"),
    tentativeRoomId: f.roomId ? null : (old ? old.tentativeRoomId : null),
    tentativeExtra: f.roomId ? [] : (old ? (old.tentativeExtra || []) : []),""")

# ---------- 상세 시트 후보 · 좌석 확정 ----------
s = L.rep(s, """  if(!r.roomId){
    const cand = st.rooms.filter(x=>{
      const kind = r.seatPref||"any";
      if(kind==="hall-any" && x.type!=="hall") return false;
      if(kind==="room-any" && x.type!=="room") return false;
      if(x.type==="room") return pplOf(r)<=x.capacity;
      return true;
    }).map(x=>{
      const ok = x.type==="room"
        ? roomStatus(r.date,r.time,x.id,r.id).state==="free"
        : hallFits(hallStatus(r.date,r.time,x.id,r.id), pplOf(r));
      const first = x.id===r.tentativeRoomId;
      /* 남는 자리가 적을수록 좋은 자리 — 4명을 6인 룸에 넣지 않기 위해 */
      const waste = x.type==="room" ? (x.capacity - pplOf(r)) : 99;
      return {x, ok, first, waste};
    }).sort((a,b)=> (b.first-a.first) || (b.ok-a.ok) || (a.waste-b.waste));""",
"""  if(!r.roomId){
    const kind = r.seatPref==="hall-any" ? "table-any" : (r.seatPref||"any");
    const ppl = pplOf(r);
    /* 후보: 룸 또는 테이블(희망 종류) + 인원에 맞는 룸 합침 그룹. 붙일 테이블은 잠정 배정이 이미 골라 둔 것(tentativeExtra)만 */
    let cand = st.rooms.filter(x=>{
      if(kind==="table-any" && !isTable(x)) return false;
      if(kind==="room-any" && !isRoom(x)) return false;
      return ppl <= seatMax(x);
    }).map(x=>{
      const ok = roomStatus(r.date,r.time,x.id,r.id).state==="free";
      const first = x.id===r.tentativeRoomId && !(r.tentativeExtra||[]).length;
      const waste = (ppl <= 2 && isTable(x) && (x.seats||4) >= 4) ? -1 : (seatMax(x) - ppl);
      return {x, ok, first, waste, ids:[x.id]};
    });
    if(kind!=="table-any") (st.joins||[]).filter(j=>ppl>=j.min && ppl<=j.max).forEach(j=>{
      const ok = j.ids.every(id=>roomStatus(r.date,r.time,id,r.id).state==="free");
      cand.push({x:{id:j.id, name:seatLabel(j.id).replace(/ 룸$/,""), type:"join", note:j.note}, ok, first:false, waste:j.max-ppl, ids:j.ids});
    });
    if((r.tentativeExtra||[]).length && r.tentativeRoomId){
      const ids = [r.tentativeRoomId].concat(r.tentativeExtra);
      cand.unshift({x:{id:"__tent", name:seatLabelIds(ids).replace(/ 테이블$/,""), type:"tables"}, ok:ids.every(id=>roomStatus(r.date,r.time,id,r.id).state==="free"), first:true, waste:seatsMax(ids)-ppl, ids});
    }
    cand = cand.sort((a,b)=> (b.first-a.first) || (b.ok-a.ok) || (a.waste-b.waste));""")
s = L.rep(s, """    seatPick = `
      <div class="lbl" style="margin:16px 0 8px">좌석 배정 ${r.tentativeRoomId?`<span class="tag amber">${esc(resTentLabel(r))} 잠정</span>`:""}</div>
      <div class="seatpick">${ranked.map(({x,ok,rank})=>`
        <button class="spick ${ok?'':'busy'} ${rank===1?'first':''} ${view.pickSeat===x.id?'picked':''}"
          onclick="pickSeatCand('${r.id}','${x.id}')">
          ${esc(x.name)}${x.type==="room"?` <small>${roomMin(x)}~${x.capacity}</small>`:""}
          ${rank?`<i>${rank}순위</i>`:""}
        </button>`).join("")}</div>
      ${view.pickSeat?`
        <div class="seatconfirm">
          <span><b>${esc(seatLabel(view.pickSeat))}</b> 으로 배정합니다</span>
          <button class="btn ghost sm" onclick="pickSeatCand('${r.id}','')">취소</button>
          <button class="btn primary" onclick="assignSeat('${r.id}','${esc(view.pickSeat)}')">좌석 확정하기</button>
        </div>`:`<p class="f-note" style="margin-top:8px">자리를 고른 뒤 '좌석 확정하기'를 눌러야 배정됩니다.</p>`}`;""",
"""    const pickedIds = view.pickSeat ? (view.pickSeat==="__tent" ? [r.tentativeRoomId].concat(r.tentativeExtra||[]) : ((st.joins||[]).find(j=>j.id===view.pickSeat)||{ids:[view.pickSeat]}).ids) : null;
    seatPick = `
      <div class="lbl" style="margin:16px 0 8px">좌석 배정 ${r.tentativeRoomId?`<span class="tag amber">${esc(resTentLabel(r))} 잠정</span>`:""}</div>
      <div class="seatpick">${ranked.map(({x,ok,rank,ids})=>`
        <button class="spick ${ok?'':'busy'} ${rank===1?'first':''} ${view.pickSeat===x.id?'picked':''} ${x.type==="join"?'join':''}"
          onclick="pickSeatCand('${r.id}','${x.id}')" ${x.note?`title="${esc(x.note)}"`:""}>
          ${esc(x.name)} <small>${seatsMin(ids)?seatsMin(ids)+"~":""}${seatsMax(ids)}</small>
          ${rank?`<i>${rank}순위</i>`:""}
        </button>`).join("")}</div>
      ${view.pickSeat?`
        <div class="seatconfirm">
          <span><b>${esc(seatLabelIds(pickedIds))}</b> 으로 배정합니다</span>
          <button class="btn ghost sm" onclick="pickSeatCand('${r.id}','')">취소</button>
          <button class="btn primary" onclick="assignSeat('${r.id}','${esc(view.pickSeat)}')">좌석 확정하기</button>
        </div>`:`<p class="f-note" style="margin-top:8px">자리를 고른 뒤 '좌석 확정하기'를 눌러야 배정됩니다.</p>`}`;""")
s = L.replace_fn(s, "assignSeat", """/* 좌석 확정 — seatId 는 좌석 id / 합침 그룹 id / "__tent"(잠정으로 골라 둔 테이블 묶음). 막지 않고 확인만 (설계 5.2) */
async function assignSeat(id, seatId){
  const s = store();
  const r = s.reservations.find(x=>x.id===id);
  if(!r) return;
  const j = (s.settings.joins||[]).find(g=>g.id===seatId);
  const ids = seatId==="__tent" ? [r.tentativeRoomId].concat(r.tentativeExtra||[]) : (j ? j.ids.slice() : [seatId]);
  if(!ids[0] || !seatById(ids[0])) return;
  const label = seatLabelIds(ids), ppl = pplOf(r);
  for(let k=0;k<ids.length;k++){
    const seat = seatById(ids[k]);
    const bk = blockedAt(seat, r.date, r.time);
    if(bk && !await uiConfirm(`${seat.name}은 이 시각에 사용 중지입니다`, `${spanLabel(bk)}${bk.note?`\\n사유: ${bk.note}`:""}\\n\\n그래도 배정할까요?`, {ok:"그래도 배정", cancel:"다시 고르기"})) return;
    const rs = roomStatus(r.date, r.time, ids[k], id);
    if(rs.state==="blocked"){
      const lines = rs.hits.map(x=>`· ${hm(x.time)} ${x.name} 손님 ${pplText(x)}`).join("\\n");
      if(!await uiConfirm(`${seat.name}에 1시간 안에 확정 예약이 있습니다`, lines, {ok:"그래도 배정", cancel:"다시 고르기"})) return;
    }else if(rs.state==="warn" && !await uiConfirm2(`${seat.name}에 겹치는 예약이 있습니다. 그래도 배정할까요?`)) return;
  }
  if(ppl > seatsMax(ids) && !await uiConfirm2(`${label} 정원(${seatsMax(ids)}명)을 넘습니다. 배정할까요?`)) return;
  if(adultCount(ppl, r.infants||0) < seatsMin(ids) && !await uiConfirm2(`${label}은 최소 ${seatsMin(ids)}명부터입니다. 지금 ${adultCount(ppl, r.infants||0)}명입니다. 배정할까요?`)) return;
  if(j && j.note && !await uiConfirm(`${label} — ${j.note}`, "손님께 확인하셨나요?", {ok:"확인했음 · 배정", cancel:"다시 고르기"})) return;
  logEvent("좌석 배정", `${r.date} ${r.time} ${r.name} → ${label}`);
  if(!r.roomId) r.assignedLater = {from:r.seatPref||"any", at:new Date().toISOString()};
  addChange(r, "변경", [{n:"좌석", a:resSeatLabel(r), b:label}]);
  r.roomId = ids[0]; r.extraIds = ids.slice(1); r.tentativeRoomId = null; r.tentativeExtra = []; r.seatPref = null;
  view.pickSeat = null;
  reflowTentatives(r.date);
  view.form = null; saveData(); render();
}""")

# ---------- 대시보드 좌석 사용 수 ----------
s = L.rep(s, """  const halls = st.rooms.filter(x=>x.type==="hall");
  const rooms = st.rooms.filter(x=>x.type==="room");
  /* 예약이 쓰는 좌석(룸 1개 = 1, 홀은 테이블 수) */
  const seatUse = active.reduce((a,r)=>{
    const seat = st.rooms.find(x=>x.id===effSeat(r));
    return a + (seat && seat.type==="hall" ? tablesFor(pplOf(r)) : 1);
  },0);""",
"""  /* 예약이 쓰는 좌석 수 — 룸 1개 = 1, 테이블 1개 = 1, 합치면 그만큼 */
  const seatUse = active.reduce((a,r)=>a + seatsOf(r).length, 0);""")

# ---------- 마법사 경고 · 메뉴 · 등록 ----------
s = L.rep(s, """    if(room && room.type==="hall"){
      const h = hallStatus(WZ.date, WZ.time, WZ.seat);
      if(!hallFits(h, WZ.people)) out.push(`자리 부족 - ${seatLabel(room.id)} 남은 테이블 ${h.left}`);
    }""", "")
s = L.rep(s, """  const isHall = seat ? seat.type==="hall" : (WZ.seat==="hall-any");
  /* 홀은 보통 메뉴를 정하지 않고 받습니다 — 선택지를 줄입니다 */""",
"""  const isHall = seat ? isTable(seat) : (WZ.seat==="table-any" || WZ.seat==="hall-any");
  /* 테이블은 보통 메뉴를 정하지 않고 받습니다 — 선택지를 줄입니다 */""")
s = L.rep(s, """  const isRoom = WZ.seat && !["any","hall-any","room-any"].includes(WZ.seat);
  const rec = {
    id:newId("res"), date:WZ.date, time:WZ.time,
    name:WZ.name.trim(), phone:WZ.phone.trim(),
    people:WZ.people, infants:WZ.infants, chairs:WZ.chairs||0,
    roomId: isRoom ? WZ.seat : null,
    seatPref: isRoom ? null : WZ.seat,     /* 미배정일 때 희망 좌석 종류를 기억 */
    tentativeRoomId: isRoom ? null : (WZ.tentative || null),  /* 나중에 확정할 때 1순위로 뜨는 자리 */""",
"""  const fixed = WZ.seat && !["any","hall-any","table-any","room-any"].includes(WZ.seat);   /* 좌석을 특정했는지 */
  const rec = {
    id:newId("res"), date:WZ.date, time:WZ.time,
    name:WZ.name.trim(), phone:WZ.phone.trim(),
    people:WZ.people, infants:WZ.infants, chairs:WZ.chairs||0,
    roomId: fixed ? WZ.seat : null,
    extraIds: fixed ? (WZ.seatExtra || []) : [],
    seatPref: fixed ? null : WZ.seat,     /* 미배정일 때 희망 좌석 종류를 기억 */
    tentativeRoomId: fixed ? null : (WZ.tentative || null),  /* 나중에 확정할 때 1순위로 뜨는 자리 */
    tentativeExtra: fixed ? [] : (WZ.tentativeExtra || []),""")

# ---------- 마법사 3단계: 룸 | 테이블 ----------
s = L.replace_fn(s, "wzStepSeat", """/* ---------- 3단계: 좌석 (8차) ----------
   룸 | 테이블 두 갈래(가게에서 '룸 예약 / 테이블 예약' 이라 부름). 고른 갈래의 좌석 + '미정'.
   룸 쪽에는 인원이 맞는 합침 그룹(중문 탈거)도 나옵니다 — 자동 배정은 안 하고 사람이 고를 때만, 원탁은 확인창 */
function wzStepSeat(){
  const s=store(), st=s.settings;
  const total = WZ.people||0;
  const adults = adultCount(total, WZ.infants);
  if(!WZ.seatKind){
    /* 이미 고른 좌석이 있으면 그 종류, 없으면 인원으로 추정(룸 최소 4 이상이면 룸) */
    const cur = seatById(WZ.seat) || (st.joins||[]).find(j=>j.id===WZ.seat);
    WZ.seatKind = cur ? (isTable(cur) ? "table" : "room") : (WZ.seat==="table-any" ? "table" : "room");
  }
  const kind = WZ.seatKind;

  const cell = (ids, x, extraCls) => {
    const label = ids.length > 1 ? seatLabelIds(ids).replace(/ (룸|테이블)$/,"") : esc(x.name);
    let statuses = ids.map(id=>roomStatus(WZ.date, WZ.time, id));
    const state = statuses.some(r=>r.state==="blocked") ? "blocked" : statuses.some(r=>r.state==="warn") ? "warn" : "free";
    const blocked = ids.some(id=>blockedAt(seatById(id), WZ.date, WZ.time));
    const over = total > seatsMax(ids), under = adults < seatsMin(ids);
    const txt = blocked ? "사용 중지" : state==="free" ? (over?"인원 초과":under?"인원 부족":"이용 가능") : "이용 불가";
    const cls = blocked ? "blocked" : state!=="free" ? state : (over||under ? "warn" : "free");
    const bad = blocked || state!=="free" || over || under;
    const mv = statuses.reduce((a,r)=>a+(r.movable?r.movable.length:0),0);
    const key = ids.length > 1 ? x.id : ids[0];
    const sub = isTable(x) ? `${roomMin(x)?roomMin(x)+"~":""}${seatMax(x)}인${x.note?` · ${esc(x.note)}`:""}` : `${seatsMin(ids)}~${seatsMax(ids)}인`;
    return `<button class="scell ${WZ.seat===key?'on':''} ${bad?'warned busy':''} ${extraCls||''}" onclick="wzSeat('${key}')" ${x.note&&ids.length>1?`title="${esc(x.note)}"`:""}>
      <span class="sn">${label}</span>
      <span class="sc">${sub}</span>
      <span class="avail ${cls}">${txt}</span>
      ${mv?`<span class="movable">미정 ${mv}건 이동 가능</span>`:""}
    </button>`;
  };

  let body = "";
  if(kind === "room"){
    const rooms = st.rooms.filter(isRoom);
    const joins = (st.joins||[]).filter(j=>total >= j.min && total <= j.max);
    body = `<div class="sgrid">${rooms.map(r=>cell([r.id], r)).join("")}</div>` +
      (joins.length ? `<div class="lbl" style="margin-top:16px">룸 합침 <span class="lbl-note">중문 탈거 · 자동 배정 안 됨</span></div>
        <div class="sgrid">${joins.map(j=>cell(j.ids, {id:j.id, name:"", note:j.note}, "join")).join("")}</div>` : "");
  }else{
    const floors = [];
    st.rooms.filter(isTable).forEach(t=>{ if(floors.indexOf(t.floor||"")<0) floors.push(t.floor||""); });
    body = floors.map(fl=>`<div class="lbl" style="margin-top:12px">${esc(fl||"테이블")}</div>
      <div class="sgrid tables">${st.rooms.filter(t=>isTable(t) && (t.floor||"")===fl).map(t=>cell([t.id], t)).join("")}</div>`).join("");
    if(WZ.seatExtra && WZ.seatExtra.length) body += `<p class="f-note">붙인 테이블: <b>${esc(seatLabelIds([WZ.seat].concat(WZ.seatExtra)))}</b></p>`;
  }
  const sess = WZ.time ? sessionAt(WZ.date, WZ.time) : null;
  const stayTxt = WZ.time ? (sess && sess.stay==="end" ? `${sess.name} 세션 끝(${hm(minToHM(sessionEnd(WZ.date, sess)))})까지 한 팀` : `${hmDur(stayMinAt(WZ.date, WZ.time))} 머무는 기준`) : "";
  return `
    <div class="seat-note">${WZ.time?`<b>${hm(WZ.time)}</b> 입장 · ${stayTxt}`:"시간을 먼저 선택하세요"}</div>
    <div class="seg seatkind">
      <button class="${kind==='room'?'on':''}" onclick="wzSeatKind('room')">룸 예약</button>
      <button class="${kind==='table'?'on':''}" onclick="wzSeatKind('table')">테이블 예약</button>
    </div>
    <div class="lbl-note" style="margin:6px 0 10px">정원은 ${seatCountsInfants()?"유아 포함":"유아 제외 성인"} 기준 · 순서는 사장님이 정한 배정 우선순위</div>
    ${body}
    <div class="lbl" style="margin-top:18px">좌석 미정으로 접수</div>
    <div class="sgrid any">
      <button class="scell any ${WZ.seat===(kind==='room'?'room-any':'table-any')?'on':''}" onclick="wzSeat('${kind==='room'?'room-any':'table-any'}')">
        <span class="sn">${kind==='room'?'룸 중 아무곳':'테이블 중 아무곳'}</span><span class="sc">비어 있는 자리에 잠정 배정</span></button>
    </div>`;
}
function wzSeatKind(k){ WZ.seatKind = k; if(WZ.seat && !seatById(WZ.seat)) { /* 다른 갈래의 '미정' 은 지움 */ if(/-any$/.test(WZ.seat)) WZ.seat = null; } render(); }""")
s = L.replace_fn(s, "wzSeat", """/* 좌석 선택 — 막을 것은 막고, 판단이 필요한 것은 물어봅니다. v = 좌석 id / 합침 그룹 id / room-any / table-any */
async function wzSeat(v){
  const st = store().settings;
  const people = WZ.people||0;
  WZ.seatExtra = []; WZ.tentative = null; WZ.tentativeExtra = [];
  if(!["any","hall-any","table-any","room-any"].includes(v)){
    const j = (st.joins||[]).find(g=>g.id===v);
    const ids = j ? j.ids.slice() : [v];
    if(!seatById(ids[0])) return;
    const label = seatLabelIds(ids);
    for(let k=0;k<ids.length;k++){
      const room = seatById(ids[k]);
      const bk = blockedAt(room, WZ.date, WZ.time);
      if(bk && !await uiConfirm(`${room.name}은 이 시각에 사용 중지입니다`,
        `${dateLabel(WZ.date)} ${spanLabel(bk)}${bk.note?`\\n사유: ${bk.note}`:""}\\n\\n그래도 이 자리로 배정할까요?`,
        {ok:"그래도 배정", cancel:"다시 고르기"})) return;
      const rs = roomStatus(WZ.date, WZ.time, ids[k]);
      if(rs.state==="blocked"){
        const lines = rs.hits.map(r=>`· ${hm(r.time)} ${r.name} 손님 ${pplText(r)}`).join("\\n");
        if(!await uiConfirm(`${room.name}에 1시간 안에 확정 예약이 있습니다`, lines, {ok:"그래도 배정", cancel:"다시 고르기"})) return;
      }
      if(rs.state==="warn"){
        const a = rs.hits.map(r=>`· ${hm(r.time)} ${r.name} 손님 ${pplText(r)}`);
        const b = rs.tentative.map(r=>`· ${hm(r.time)} ${r.name} 손님 ${pplText(r)} (좌석 미정 · 잠정 배정)`);
        if(!await uiConfirm2(`${room.name}에 겹치는 예약이 있습니다.\\n\\n${[...a,...b].join("\\n")}\\n\\n그래도 배정할까요?`)) return;
      }
    }
    if(people > seatsMax(ids)){
      if(!await uiConfirm2(`${label}은 최대 ${seatsMax(ids)}명입니다. 지금 ${people}명입니다.\\n간이 의자 등으로 감당 가능한 경우에만 배정하세요.`)) return;
    }else{
      const adults = adultCount(people, WZ.infants);
      if(adults < seatsMin(ids)){
        const basis = store().settings.minCountAdultsOnly===false ? "총 인원" : "성인";
        if(!await uiConfirm(`${label} 최소 인원 미달`, `최소 ${seatsMin(ids)}명부터 받습니다.\\n지금 ${basis} ${adults}명입니다${WZ.infants?` (유아 ${WZ.infants}명 제외)`:""}.`, {ok:"그래도 배정", cancel:"다시 고르기"})) return;
      }
    }
    /* 한 테이블에 안 들어가는 인원이 테이블 하나를 고르면 붙일 테이블을 함께 제안 */
    const one = seatById(v);
    if(!j && isTable(one) && people > seatMax(one)){
      const f = findSeat({date:WZ.date, time:WZ.time, people:people, kind:"table-any"});
      if(f && f.id === v && f.extra.length){
        if(!await uiConfirm2(`${one.name} 하나로는 ${people}명이 안 됩니다.\\n${seatLabelIds([f.id].concat(f.extra))}로 붙여서 받을까요?`)) return;
        WZ.seatExtra = f.extra;
      }
    }
    if(j && j.note && !await uiConfirm(`${label} — ${j.note}`, "손님께 확인하셨나요?", {ok:"확인했음", cancel:"다시 고르기"})) return;
    if(j) WZ.seatExtra = ids.slice(1);
    WZ.seat = j ? ids[0] : v; WZ.seatJoin = j ? j.id : null; wzAutoNext();
    return;
  }
  /* 좌석 미정 — 잠정 배정 가능 여부를 먼저 확인 */
  const f = suggestSeatFull(WZ.date, WZ.time, people, v);
  if(!f){
    if(!await uiConfirm2(`지금 ${hm(WZ.time)} 기준으로 ${people}명이 들어갈 빈 자리가 없습니다.\\n먼저 접수한 좌석 미정 예약까지 계산한 결과입니다.\\n\\n자리 없이 접수할까요?`)) return;
  }
  WZ.tentative = f ? f.id : null; WZ.tentativeExtra = f ? f.extra : [];
  WZ.seat = v; wzAutoNext();
}""")
# 마법사 요약·완료 라벨: 합침이면 묶음 라벨
s = L.rep(s, """  if(WZ.seat) p.push(seatLabel(WZ.seat));""",
    """  if(WZ.seat) p.push(WZ.seatExtra && WZ.seatExtra.length ? seatLabelIds([WZ.seat].concat(WZ.seatExtra)) : seatLabel(WZ.seat));""")
s = L.rep(s, """      <div class="rv"><span>좌석</span><b>${WZ.seat?seatLabel(WZ.seat):"-"}</b></div>""",
    """      <div class="rv"><span>좌석</span><b>${WZ.seat?(WZ.seatExtra&&WZ.seatExtra.length?seatLabelIds([WZ.seat].concat(WZ.seatExtra)):seatLabel(WZ.seat)):"-"}</b></div>""")
# 마법사 상태 초기값
s = L.rep(s, """    seat:null,              /* 룸 id | 'hall-any' | 'room-any' | 'any' */""",
    """    seat:null, seatExtra:[], seatKind:null,   /* 좌석 id | 'room-any' | 'table-any'. seatExtra = 합친 나머지 좌석 */""")

L.js_check(s)
L.save(s)
print("p9_b ok")
