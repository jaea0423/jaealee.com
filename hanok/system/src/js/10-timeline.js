/* ============================================================
   좌석 가동 타임라인
   룸: 한 줄에 예약 블록
   홀: 테이블 수만큼 층을 만들고, 먼저 온 팀부터 아래층에 배치
       (한 팀이 테이블 2개를 쓰면 두 층을 차지)
   ============================================================ */
function laneLayout(items, laneCount){
  /* 시간 순으로 훑으며 비어 있는 가장 아래 층에 배치 */
  const laneEnd = new Array(laneCount).fill(-1);
  const placed = [];
  for(const it of items){
    let start = -1;
    for(let i=0; i+it.need<=laneCount; i++){
      let ok = true;
      for(let k=i;k<i+it.need;k++) if(laneEnd[k] > it.s0){ ok=false; break; }
      if(ok){ start=i; break; }
    }
    if(start<0){ placed.push({...it, lane:null, over:true}); continue; }
    for(let k=start;k<start+it.need;k++) laneEnd[k] = it.e0;
    placed.push({...it, lane:start});
  }
  return placed;
}
/* 층(lane)에 놓는 순서 = 먼저 들어온 예약이 아래, 늦게 들어온 예약이 위로 쌓임(재아 09-17) — 겹쳐 받았을 때 누가 원래 자리인지 한눈에.
   예전에는 시각 순이라 나중에 받은 예약이 먼저 시작하면 아래로 갔음. 홈페이지 대기 건은 접수 시각이 createdAt */
function byCreated(a, b){ return String(a.createdAt||"").localeCompare(String(b.createdAt||"")) || a.time.localeCompare(b.time); }
/* 폰 압축판에서 층 테이블 줄 접기/펼치기 — 층별로 기억(새로 고침하면 다시 접힘) */
function tlToggleFloor(key){ view.tlOpen = view.tlOpen || {}; view.tlOpen[key] = !view.tlOpen[key]; render(); }
/* ---------- 점심 / 저녁 / 하루 판 (재아 09-20) ----------
   그래프 글씨가 작다는 평 → 하루를 반으로 잘라 폭을 두 배로. 경계는 브레이크가 있는 날은 브레이크(점심 = 개점~브레이크 시작,
   저녁 = 브레이크 끝~마감), 없는 날(주말·공휴일)은 세션 경계(sess.edge, 보통 15:30).
   브레이크가 없는 날은 경계 너머 1시간을 흐리게 덧붙여 이어지는 예약이 보이게(EXT 분).
   기본값: 오늘은 지금 시각이 속한 판, 다른 날짜는 하루 전체. 버튼으로 바꾼 값은 그 날짜에만(view.tlPart / tlPartDate) */
const TL_EXT = 60;
function tlParts(date){
  const dh = hoursFor(date), edge = sessFromDay(dh).edge || "15:30";
  const o = toMin(dh.open), c = toMin(dh.close), brk = !!(dh.bs && dh.be);
  const lEnd = brk ? toMin(dh.bs) : toMin(edge), dStart = brk ? toMin(dh.be) : toMin(edge);
  return { open:o, close:c, brk:brk,
    lunch:  { o:o, c:lEnd, extEnd: brk ? lEnd : Math.min(c, lEnd + TL_EXT) },
    dinner: { o:dStart, c:c, extStart: brk ? dStart : Math.max(o, dStart - TL_EXT) } };
}
function tlPartOf(date){
  if(view.tlPart && view.tlPartDate === date) return view.tlPart;
  if(date !== todayStr()) return "day";
  const p = tlParts(date), now = toMin(nowHM());
  return now < p.dinner.o ? "lunch" : "dinner";
}
function tlSetPart(part){ view.tlPart = part; view.tlPartDate = view.date; render(); }
function renderTimeline(date, compact){
  const s = store(), st = s.settings;
  const dh = hoursFor(date);                    /* 그날 실제 운영시간 */
  const dOpen = toMin(dh.open), dClose = toMin(dh.close);
  /* 가로축 = 그날 영업시간(예전엔 가장 넓은 영업시간이라 일찍 닫는 날은 끝이 빗금이었음 — 재아 09-20). 휴무면 기본 시간대 */
  const parts = tlParts(date), part = dh.closed ? "day" : tlPartOf(date);
  const ax = dh.closed ? axisRange() : parts;
  const o = part === "dinner" ? parts.dinner.extStart : (dh.closed ? ax.o : parts.open);
  const c = part === "lunch" ? parts.lunch.extEnd : (dh.closed ? ax.c : parts.close);
  const span = Math.max(30, c - o);
  /* 흐리게 덧붙인 구간(경계 너머) */
  const ext = part === "lunch" && parts.lunch.extEnd > parts.lunch.c ? [parts.lunch.c, parts.lunch.extEnd]
            : part === "dinner" && parts.dinner.extStart < parts.dinner.o ? [parts.dinner.extStart, parts.dinner.o] : null;
  const list = s.reservations.filter(r=>r.date===date && holdsSeat(r))
    .concat(typeof reqPendingOn === "function" ? reqPendingOn(date).map(reqAsRes) : []);   /* 대기 중인 홈페이지 요청 — 연회색(확정 전 자리 확보, 재아) */
  const pos = m => ((m-o)/span)*100;
  /* 영업 전·후, 브레이크타임을 덮는 층 */
  const shade = `
    ${dh.closed?`<span class="closed-band"></span>`:`
      ${dOpen>o?`<span class="offband" style="left:0; width:${pos(dOpen)}%"></span>`:""}
      ${dClose<c?`<span class="offband" style="left:${pos(dClose)}%; right:0"></span>`:""}
      ${dh.bs&&dh.be&&part==="day"?`<span class="breakband" style="left:${pos(toMin(dh.bs))}%; width:${((toMin(dh.be)-toMin(dh.bs))/span)*100}%"></span>`:""}
      ${ext?`<span class="extband ${part==="dinner"?"l":""}" style="left:${pos(ext[0])}%; width:${((ext[1]-ext[0])/span)*100}%" title="${part==="lunch"?"저녁 시간대 — 이어지는 예약만 흐리게":"점심 시간대 — 이어지는 예약만 흐리게"}"></span>`:""}
    `}`;
  const LANE = compact ? 30 : 34;   /* 층 하나의 높이(px). 09-20 재아: 21 → 32 — 카운터에서 보기에 너무 작았음(눈이 침침). 폰 압축판은 30 */


  const ticks = [];
  const step = part === "day" ? 60 : 30;   /* 반쪽 판은 30분 눈금까지 */
  for(let m=Math.ceil(o/step)*step; m<=c; m+=step)
    ticks.push(`<span class="tk ${m>=c?'end':''} ${m%60?'half':''}" style="left:${pos(m)}%"><i></i><b>${m%60?"":Math.floor(m/60)}</b></span>`);   /* 맨 끝 눈금은 글자를 왼쪽으로 붙여 잘리지 않게 */
  const layers = ticks.join("") + shade;
  /* 현재 시각 선.
     예전에는 그래프 범위(o~c)를 벗어나면 선을 아예 안 그렸습니다.
     그러면 개점 전이나 마감 후에 선이 사라져서 "지금이 어디쯤인지" 감이 끊깁니다.
     범위를 벗어나면 가까운 쪽 끝에 붙여 두고, 붙어 있다는 걸 알 수 있게
     점선으로 바꿉니다(.edge). 선이 있는 편이 없는 것보다 읽기 쉽습니다. */
  const nowM = toMin(nowHM());
  const isToday = date===todayStr();
  const nowClamped = Math.min(c, Math.max(o, nowM));
  const nowLine = isToday
    ? `<span class="nowline ${nowM<o?'edge before':nowM>c?'edge after':''}"
             style="left:${pos(nowClamped)}%"
             title="${nowM<o?`아직 그래프 시작(${hm(minToHM(o))}) 전입니다`
                    :nowM>c?`그래프 끝(${hm(minToHM(c))})을 지났습니다`
                    :`지금 ${hm(nowHM())}`}"></span>` : "";

  /* 이름 뒤 VIP·VVIP 알약(tierTag) — 그래프에서도 단골이 보이게(재아 09-20). 칸이 좁으면 잘려도 시각·이름이 먼저 */
  const blockLabel = r =>
    `${r._req?`<i class="rq">홈페이지</i> `:""}<b>${esc(r.time)}</b> ${esc(r.name)}${tierTag(r)} ${pplOf(r)}명${r.infants?`(어린이${r.infants})`:""}${r._req?" · 확정 전":""}`;

  /* (안 씀 — 사용 중지는 빗금 위에만 적습니다. 자리는 tlPlaceLabels 가 그린 뒤 정함) */
  const blockTag = (seat)=>{
    const sp = blockSpans(seat, date);
    if(!sp.length) return "";
    /* '사용 중지 (사유 / 기간)' — 기간은 날짜(하루면 날짜 하나). 시각은 빗금이 이미 보여 주니 적지 않음(재아) */
    const txt = sp.map(x=>blockLabelText(x.blk)).join(" · ");
    const tip = sp.map(x=>blockLabelText(x.blk)+(x.allDay?"":" · "+spanLabel(x))).join(" / ");
    return `<span class="bk" title="${esc(tip)}">${esc(txt)}</span>`;
  };

  /* 좌석 사용 중지 구간을 그 줄에만 덮습니다.
     영업시간 밖(.offband)과 같은 빗금 계열이되, 사람이 일부러 잠근 것이므로 더 진하게. */
  /* 빗금만 그리고 글자는 넣지 않습니다 — 예약 블록과 겹쳐 서로 안 읽힙니다.
     무슨 사유인지는 좌석 이름 칸의 표시와 마우스를 올렸을 때 나옵니다. */
  const blockBands = (seat)=>blockSpans(seat, date).map(sp=>{
    const s = Math.max(o, sp.s), e = Math.min(c, sp.e);
    if(e <= s) return "";
    return `<span class="blockband" style="left:${pos(s)}%; width:${((e-s)/span)*100}%"
      title="${esc(blockLabelText(sp.blk))}${sp.allDay?"":" · "+esc(spanLabel(sp))}"><i class="bb-l tl-lbl">${esc(blockLabelText(sp.blk))}</i></span>`;
  }).join("");

  /* ---------- 룸 ---------- */
  /* 좌석 하나 = 한 줄. 합쳐 쓰는(중문 탈거) 예약은 **이어진 줄들을 가로질러 한 덩어리**로 — 맨 위 방 줄에 그리고 높이는 그린 뒤(tlSpanJoined) 맞춥니다(재아 09-19).
     방들이 표에서 이어져 있지 않으면 예전처럼 줄마다 따로 */
  const rooms = roomsAt(date).filter(isRoom);   /* 그 날짜의 좌석(예정 반영) */
  const roomIdx = {}; rooms.forEach((r, i) => { roomIdx[r.id] = i; });
  const spanInfo = r => {   /* 합침 예약이 이어진 방 줄을 쓰면 {first, ids} */
    const ids = seatsOf(r).filter(id => roomIdx[id] != null); if(ids.length < 2) return null;
    const idx = ids.map(id => roomIdx[id]).sort((a, b) => a - b);
    for(let i = 1; i < idx.length; i++) if(idx[i] !== idx[i-1] + 1) return null;
    return { first: rooms[idx[0]].id, last: rooms[idx[idx.length-1]].id, ids };
  };
  const roomRow = (room)=>{
    const items = list.filter(r=>usesSeat(r, room.id))
      .sort(byCreated)
      .map(r=>({ r, need:1, s0:Math.max(o, toMin(r.time)), e0:Math.min(c, toMin(r.time)+stayOf(r)), joined:seatsOf(r).length>1 }))
      .filter(it=>it.e0 > it.s0);   /* 판(점심/저녁) 밖의 예약은 안 그림 */
    /* 룸은 방 하나 = 칸 하나. 겹쳐 받은(사장 판단) 예약은 홀처럼 **위에 빗금 칸을 쌓아** 넣습니다 — 먼저 들어온 예약이 아래 정상 칸,
       늦게 들어온 것이 위 '겹침' 칸(재아 09-17). 예전에는 겹치는 수만큼 칸을 늘려 전부 정상 칸처럼 보였음 */
    const placed = laneLayout(items, 1);
    let overK = 0; placed.forEach(x=>{ if(x.lane===null){ x.overLane = 1 + overK; overK++; } });
    const over = overK, lanes = 1 + over;
    const blocks = placed.map(it=>{
      const w = ((it.e0-it.s0)/span)*100;
      const tent = !it.r.roomId;
      const past = isBlockPast(it.r, it.s0, date, nowM);
      const lane = it.lane===null?it.overLane:it.lane;
      const bad = resWarn(it.r).length>0;
      const chg = changeTag(it.r);
      /* 09-20(재아): 합침 예약을 이어진 줄을 가로지르는 한 덩어리로 그렸더니 붕 떠 보였음 → 다시 방마다 한 칸씩, ⊞ 표시로 묶임을 알림.
         spanInfo/tlSpanJoined 는 남겨 두되 안 씀 */
      const sp = null;
      const spanAttr = sp ? ` data-span-to="${esc(sp.last)}"` : "";
      return `<button class="blk ${tent?'tent':''} ${it.r._req?'req':''} ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''} ${it.joined?'joined':''} ${sp?'spanned':''} ${it.lane===null?'overlap':''}"${spanAttr} onclick="${it.r._req?`openRequest('${it.r._req.id}')`:`openMark('${it.r.id}')`}"
        style="left:${pos(it.s0)}%; width:${w}%; ${sp ? `top:${(lanes - 1 - lane)*LANE+1}px` : `bottom:${lane*LANE+1}px`}; height:${LANE-2}px; line-height:${LANE-2}px"
        title="${esc(it.r.time)} ${esc(it.r.name)} ${pplText(it.r)}${it.joined?` · ${esc(it.r.roomId?resSeatLabel(it.r):resTentLabel(it.r))} 합침`:""}${tent?' · 잠정':''}${chg?` · 오늘 ${esc(chg.label)}`:""}${bad?` · 경고: ${esc(resWarn(it.r).join(", "))}`:""}">
        ${it.joined?`<i class="jn">${(joinOf(seatsOf(it.r))||{}).split?"⊕":"⊞"}</i>`:''}${chg?`<span class="chg-chip">${blockLabel(it.r)}</span>`:blockLabel(it.r)}</button>`;
    }).join("");
    const sub = isTable(room) ? `${roomMin(room)?roomMin(room)+"~":""}${seatMax(room)}인` : `${roomMin(room, date)}~${room.capacity}인`;   /* 그 날짜 기준(주말 최소) */
    const overBand = over ? `<div class="offband overlane" style="left:0; right:0; top:0; height:${over*LANE}px" title="같은 룸에 겹쳐 받은 예약이 놓이는 칸"></div>` : "";   /* '겹침 N팀' 글자는 뺌(재아 09-20) — 회색 칸이 곧 그 뜻 */
    return `<div class="tl-row ${isTable(room)?'tbl':''} ${blockedAllDay(room,date)?'off-seat':''}" data-room="${esc(room.id)}">
      <div class="tl-name" title="${esc(sub)}"><b>${esc(room.name)}</b></div>
      <div class="tl-track" data-lane="${LANE}" style="height:${lanes*LANE}px${over?`; background-image:repeating-linear-gradient(to top, transparent 0, transparent ${LANE-1}px, var(--border) ${LANE-1}px, var(--border) ${LANE}px)`:""}">
        ${layers}${blockBands(room)}${overBand}${blocks}
      </div>
    </div>`;
  };

  const groupRow = (label) => `<div class="tl-row group"><div class="tl-name"><b>${esc(label)}</b></div><div class="tl-track"></div></div>`;
  /* 테이블은 층 한 줄 — 겹치는 예약을 층(lane)으로 쌓고, 예약률은 손님 수 / 자리 수 (8차-H) */
  const floorRow = (fl)=>{
    /* 층 한 줄의 높이는 그 층 테이블 수만큼(테이블 하나 = 한 칸). 여러 테이블이 필요한 팀은 그만큼 칸을 병합해 그립니다 —
       재아 요청: 테이블이 다 보여야 직관적. 어느 테이블인지는 안 정하므로 칸의 순서에 뜻은 없고, 몇 자리 차지하는지만 보입니다 */
    const tbls = fl==null ? [] : floorTables(fl);
    /* 칸 수 = 숨은 배정(붙임·나눠 앉기 포함)이 쓰는 테이블 개수. 자리를 못 찾은 예약은 1칸 + 경고 */
    const needOf = r => Math.max(1, seatsOf(r).length);
    const items = list.filter(r=>resFloor(r) !== undefined && (resFloor(r)||"") === (fl||""))
      .sort(byCreated)
      .map(r=>({ r, need:needOf(r), s0:Math.max(o, toMin(r.time)), e0:Math.min(c, toMin(r.time)+stayOf(r)) }))
      .filter(it=>it.e0 > it.s0);
    /* 폰(압축판)은 테이블 6칸이 너무 높아 3칸으로 접고, 층 이름을 누르면 펼칩니다(모바일 2026-09-17).
       접힌 동안 못 들어간 팀은 그리지 않고 "숨은 N팀" 으로만 — 겹쳐 그리면 뒤 팀이 안 보입니다 */
    const FOLD = 3, key = fl == null ? "_" : fl;
    const foldable = compact && tbls.length > FOLD;
    const folded = foldable && !(view.tlOpen && view.tlOpen[key]);
    const lanes = Math.max(1, folded ? FOLD : tbls.length);
    let placed = laneLayout(items.map(it=>Object.assign({}, it, {need:Math.min(it.need, lanes)})), lanes);
    /* 여러 칸이 필요한 팀이 '이어진 빈 칸' 이 없어 못 들어가면(칸이 띄엄띄엄 비어 있을 때) 한 칸짜리 조각으로 나눠 다시 놓습니다 —
       실제로도 나눠 앉는 것이니 그림도 그렇게. 그래도 못 들어가면 '초과' */
    if(placed.some(x=>x.lane===null && x.need>1)){
      const again = [];
      placed.forEach(x=>{ if(x.lane===null && x.need>1){ for(let k=0;k<x.need;k++) again.push(Object.assign({}, x, {need:1, part:k+1, parts:x.need, lane:undefined})); } else again.push(Object.assign({}, x, {lane:undefined})); });
      again.sort((a,b)=>byCreated(a.r, b.r));
      placed = laneLayout(again, lanes);
    }
    const hidden = folded ? placed.filter(x=>x.lane===null).length : 0;
    if(folded) placed = placed.filter(x=>x.lane!==null);
    const over = placed.filter(x=>x.lane===null).length;
    /* 줄 높이는 실제로 쓰인 칸까지만(최소 1칸) — 테이블 6개라고 늘 6칸이면 빈 공간이 아까움(재아 09-19). 자리 없음 칸은 그 위에 */
    const usedLanes = Math.max(1, placed.filter(x=>x.lane!==null).reduce((a,x)=>Math.max(a, x.lane + x.need), 0));
    /* 자리를 못 받은 팀(테이블 수보다 팀이 많음)은 다른 블록 위에 겹쳐 그리지 않고 **맨 위에 칸을 더** 만들어 넣습니다.
       팀마다 한 칸씩 — 둘이면 두 칸(포개면 뒤 팀이 안 보임, 재아). 그 칸은 영업 종료 빗금으로 채워 '정상 칸이 아니다' 가 보이게 */
    let overK = 0; placed.forEach(x=>{ if(x.lane===null){ x.overLane = usedLanes + overK; overK++; } });
    const totalLanes = usedLanes + over;
    const seats = fl==null ? 0 : floorSeats(fl);
    const blocks = placed.map(it=>{
      const w = ((it.e0-it.s0)/span)*100, lane = it.lane===null?it.overLane:it.lane;
      const past = isBlockPast(it.r, it.s0, date, nowM);
      const bad = resWarn(it.r).length>0, chg = changeTag(it.r);
      const tn = it.r.roomId ? seatLabelIds(seatsOf(it.r)).replace(/ 테이블$/,"") : tableHint(it.r).replace(/^ \(|\)$/g,"").replace(/ 나눠$/,"");
      const h = (it.lane===null ? 1 : it.need) * LANE - 2;   /* 테이블 n개 → n칸 높이로 병합 */
      const split = !it.r.roomId && it.r.tentativeSplit, none = !it.r.roomId && !it.r.tentativeRoomId;
      return `<button class="blk ${it.r._req?'req':''} ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''} ${it.need>1?'multi':''} ${split?'split':''}" onclick="${it.r._req?`openRequest('${it.r._req.id}')`:`openMark('${it.r.id}')`}"
        style="left:${pos(it.s0)}%; width:${w}%; bottom:${lane*LANE+1}px; height:${h}px; line-height:${h}px"
        title="${esc(it.r.time)} ${esc(it.r.name)} ${pplText(it.r)}${tn?` · ${esc(tn)} 테이블 지정`:""}${split?" · 나눠 앉음":""}${none?" · 자리 없음":""}${chg?` · 오늘 ${esc(chg.label)}`:""}">
        ${split?'<i class="jn">↔</i>':''}${chg?`<span class="chg-chip">${blockLabel(it.r)}</span>`:blockLabel(it.r)}${tn?` <small class="tn">${esc(tn)}</small>`:""}${it.part?` <small class="tn">${it.part}/${it.parts}</small>`:""}</button>`;
    }).join("");
    const bands = (fl==null ? "" : floorTables(fl).map(blockBands).join(""))
      + (over ? `<div class="offband overlane" style="left:0; right:0; top:0; height:${over*LANE}px" title="테이블 수를 넘은 팀이 놓이는 칸"></div>` : "");
    return `<div class="tl-row tbl floor">
      <div class="tl-name ${foldable?'foldable':''}" ${foldable?`onclick="tlToggleFloor('${esc(key)}')" role="button"`:`title="${fl==null?"":`테이블 ${tbls.length} · ${seats}석`}"`}><b>${fl==null?"층 미정":esc(floorLabel(fl))}</b>${
        foldable ? `<small class="fold-hint">${folded ? `${FOLD}칸만 ▾${hidden?`<i>숨은 ${hidden}팀</i>`:""}` : "접기 ▴"}</small>` : ""}</div>
      <div class="tl-track" data-lane="${LANE}" style="height:${totalLanes*LANE}px; background-image:repeating-linear-gradient(to top, transparent 0, transparent ${LANE-1}px, var(--border) ${LANE-1}px, var(--border) ${LANE}px)">${layers}${bands}${blocks}</div>
    </div>`;
  };
  const unknownFloor = list.some(r=>resFloor(r) === null);
  const tableRows = groupRow("테이블") + tableFloors().map(floorRow).join("") + (unknownFloor ? floorRow(null) : "");

  /* 전체 가동률 */
  const st2 = dayStat(date);
  const roomRate = st2.roomRate, hallRate = st2.hallRate;
  const tentCount = list.filter(isUnassigned).length;

  return `
    <div class="tl-top">
      <div class="tl-kpis">
        <span class="tl-kpi"><b>${st2.rate}%</b></span>
        <span class="tl-kpi sub">룸 <b>${roomRate}%</b></span>
        <span class="tl-kpi sub">테이블 <b>${hallRate}%</b></span>
        ${(()=>{
          /* 그날 상황을 한 줄로 — 각자 뜻에 맞는 색으로 */
          const day = s.reservations.filter(x=>x.date===date);
          const live = day.filter(holdsSeat);
          /* 8차-U(재아): 확정·경고·오늘 변경·요청·메모만, 누르면 목록. 확인 필요는 맨 오른쪽. 아래 지표 카드는 없앴습니다 */
          const cnt = {
            확정: live.filter(x=>x.status==="확정").length,
            경고: live.filter(x=>resWarn(x).length).length,
            변경: day.filter(x=>changeTag(x)).length,
            요청: live.filter(x=>(x.request||"").trim()).length,
            메모: live.filter(x=>(x.memo||"").trim()).length
          };
          const cls = {확정:"", 경고:"rust", 변경:"blue", 요청:"", 메모:"blue"};
          const nm  = {변경:"오늘 변동", 요청:"요청사항"};   /* 목록 제목·범례와 같은 말로(재아 09-17) */
          const act = {확정:"openPick('confirmed')", 경고:"openPick('warn')", 변경:"openPick('changed')", 요청:"openPick('request')", 메모:"openPick('memo')"};
          const chk = checkItems(date).length;
          return Object.keys(cnt).filter(k=>cnt[k])
            .map(k=>`<button class="tag tapchip ${cls[k]}" onclick="${act[k]}">${nm[k]||k} ${cnt[k]}건</button>`).join("")
            + `<button class="tag tapchip ${chk?'amber':''} right" onclick="openCheck()">확인 ${chk}건</button>`;
        })()}
      </div>
      <div class="tl-legends">
        <span class="tl-legend"><i class="lgsw ok"></i>확정</span>
        <span class="tl-legend"><i class="lgsw tent"></i>잠정</span>
        <span class="tl-legend"><i class="lgsw warn"></i>경고</span>
        <span class="tl-legend"><i class="lgsw chg"></i>변동</span>
        <span class="tl-legend sym" title="룸 합침(중문 탈거) — 한 방처럼">⊞ 합침</span>
        <span class="tl-legend sym" title="룸 합침인데 공간이 나뉨(원탁) — 손님 확인. '나눠 앉음'(테이블을 못 붙여 따로 앉음)과는 다릅니다">⊕ 공간 나뉨</span>
        <span class="tl-legend sym" title="붙일 테이블이 없어 옆 테이블에 나눠 앉음">↔ 나눠 앉음</span>
        ${dh.closed ? "" : `<span class="seg tl-part" role="group" aria-label="시간대">
          <button class="${part==="lunch"?"on":""}" onclick="tlSetPart('lunch')">점심</button><button class="${part==="dinner"?"on":""}" onclick="tlSetPart('dinner')">저녁</button><button class="${part==="day"?"on":""}" onclick="tlSetPart('day')">하루</button>
        </span>`}
      </div>
    </div>
    <div class="tl-scroll ${compact?'compact':''}" id="tl-scroll">
      <div class="tl">
        <div class="tl-row axis">
          <div class="tl-name"></div>
          <div class="tl-track">${ticks.join("")}${nowLine}</div>
        </div>
        ${groupRow("룸")}
        ${rooms.map(roomRow).join("")}
        ${tableRows}
      </div>
    </div>`;
}

/* ---------- 라벨 자리 정하기 (그린 뒤, 실제 픽셀로) ----------
   사용 중지·자리 없음 글자는 그래프 안에만 둡니다(좌석 이름 칸·예약률 칸에는 안 적음 — 재아).
   자리: 띠의 왼쪽 → 거기에 예약 블록이 겹치면 오른쪽 → 그래도 겹치면 그 줄 위에 층(LANE)을 하나 더 만들어 거기에.
   블록은 bottom 기준으로 놓여 있어 트랙 높이를 늘리면 위에 빈 층이 생깁니다. */
/* 합침 블록(data-span-to)을 마지막 방 줄 바닥까지 늘림 — 줄마다 높이가 달라(겹침 칸) 그린 뒤 픽셀로 */
function tlSpanJoined(){
  document.querySelectorAll(".blk.spanned[data-span-to]").forEach(function(b){
    var track = b.parentNode, row = track.closest(".tl-row"), last = row && row.parentNode.querySelector('.tl-row[data-room="' + b.getAttribute("data-span-to") + '"] .tl-track');
    if(!last) return;
    var top = track.getBoundingClientRect().top + parseFloat(b.style.top || 0), bottom = last.getBoundingClientRect().bottom;
    b.style.height = Math.max(20, bottom - top - 2) + "px"; track.classList.add("has-span");
  });
}
function tlPlaceLabels(){
  tlSpanJoined();
  var tracks = document.querySelectorAll(".tl-track");
  for(var t = 0; t < tracks.length; t++){
    var track = tracks[t], labels = track.querySelectorAll(".tl-lbl");
    if(!labels.length) continue;
    var blocks = Array.prototype.slice.call(track.querySelectorAll(".blk")).map(function(b){ return b.getBoundingClientRect(); });
    var raised = false;
    for(var i = 0; i < labels.length; i++){
      var el = labels[i];
      el.classList.remove("right", "above");
      if(!tlLabelHits(el, blocks)) continue;
      el.classList.add("right");
      if(!tlLabelHits(el, blocks)) continue;
      el.classList.remove("right"); el.classList.add("above");
      if(!raised){   /* 위에 층 하나 — 같은 줄의 라벨 여럿이면 한 층을 같이 씀 */
        raised = true;
        var lane = parseInt(track.getAttribute("data-lane") || "21", 10);
        track.style.height = (track.offsetHeight + lane) + "px";
        var ol = track.querySelector(".overlane"); if(ol) ol.style.height = (ol.offsetHeight + lane) + "px";   /* 초과 칸 빗금도 새 층까지 */
      }
    }
  }
}
function tlLabelHits(el, blocks){
  var r = el.getBoundingClientRect();
  for(var i = 0; i < blocks.length; i++){
    var b = blocks[i];
    if(r.left < b.right - 1 && r.right > b.left + 1 && r.top < b.bottom - 1 && r.bottom > b.top + 1) return true;
  }
  return false;
}
