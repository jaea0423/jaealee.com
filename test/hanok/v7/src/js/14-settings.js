/* ============================================================
   설정
   ============================================================ */
/* 설정 설명문 → ⓘ 버튼(8차-X, 재아): 항목마다 붙던 설명(.f-note)을 떼어 오른쪽 ⓘ 로 옮기고, 누르면 팝업으로 보여 줍니다.
   · <label class="f"> 안의 설명 → 그 항목 제목(.lb) 오른쪽
   · 홀로 있는 <p class="f-note"> → 바로 앞의 소제목(.subhead)·버튼 줄(.btn-row)·라벨(.lbl) 끝, 없으면 작은 ⓘ 줄
   설명 안의 버튼(linkbtn)·굵은 글씨는 그대로 팝업에 들어갑니다 */
var INFO_NOTES = [];
function infoBtn(html){ INFO_NOTES.push(html); return `<button class="ibtn" type="button" onclick="event.stopPropagation(); showInfo(${INFO_NOTES.length-1})" aria-label="설명">i</button>`; }
function showInfo(i){ const h = INFO_NOTES[i]; if(h == null) return; modalReplace({mode:"alert", title:"설명", html:h, tone:"ok", res:function(){}}); }
function infoize(html){
  html = html.replace(/<label class="f"([^>]*)>([\s\S]*?)<\/label>/g, function(m, attrs, body){
    var notes = [];
    body = body.replace(/<div class="f-note"[^>]*>([\s\S]*?)<\/div>/g, function(_, n){ notes.push(n); return ""; });
    if(!notes.length) return m;
    body = body.replace(/(<div class="lb">)([\s\S]*?)(<\/div>)/, function(_, a, t, b){ return a + t + infoBtn(notes.join("<br><br>")) + b; });
    return '<label class="f"' + attrs + '>' + body + '</label>';
  });
  html = html.replace(/<\/p>\s*<p class="f-note"[^>]*>/g, "<br><br>");   /* 붙어 있는 설명 둘은 한 팝업으로 */
  var out = "", re = /<p class="f-note"[^>]*>([\s\S]*?)<\/p>/g, last = 0, m;
  while((m = re.exec(html))){
    var seg = html.slice(last, m.index), btn = infoBtn(m[1]);
    var a = Math.max(seg.lastIndexOf('<div class="subhead"'), seg.lastIndexOf('<div class="btn-row"'), seg.lastIndexOf('<div class="lbl"'));
    var e = a >= 0 ? seg.indexOf("</div>", a) : -1;
    seg = e >= 0 ? seg.slice(0, e) + btn + seg.slice(e) : seg + '<div class="f-info">' + btn + '</div>';
    out += seg; last = re.lastIndex;
  }
  return out + html.slice(last);
}
/* 설정 화면의 접이식 구역 */
function sec(key, title, extra, inner){
  const open = !!view.open["s_"+key];
  return `
    <section class="card fold ${open?'on':''}" style="margin-top:12px">
      <button class="fold-h" onclick="toggleFold('s_${key}')">
        <span class="fh-t">${title}</span>
        <span class="fh-x">${extra||""}</span>
      </button>
      ${open?`<div class="fold-b ${view.foldJust==="s_"+key?'just':''}">${infoize(inner)}</div>`:""}
    </section>`;
}
function renderSettings(){
  INFO_NOTES = [];                  /* ⓘ 설명은 그릴 때마다 새로 모읍니다 */
  const st = draft();               /* 임시본 — '적용하기'를 눌러야 반영됩니다 */
  const dirty = settingsDirty();
  const DOWN = ["일","월","화","수","목","금","토"];

  /* ---------- 운영시간 ---------- */
  const schedBody = `
    ${(st.schedules||[]).slice().sort((a,b)=>b.from.localeCompare(a.from)).map(sc=>{
      const cur = sc === scheduleFor(todayStr());
      return `<div class="schrow ${cur?'cur':''}">
        <div class="sch-h">
          <b>${sc.from==="2000-01-01"?"기본":`${sc.from.slice(0,4)}. ${+sc.from.slice(5,7)}. ${+sc.from.slice(8)}. 부터`}</b>
          ${cur?`<span class="tag pine">현재 적용</span>`:""}
          <button class="btn sm" style="margin-left:auto" onclick="openSchedule('${sc.from}')">수정</button>
        </div>
        <div class="sch-days">
          ${[1,2,3,4,5,6,0].map(i=>({d:(sc.days||[])[i], i})).filter(x=>x.d).map(({d,i})=>`<span class="sch-d"><b>${DOWN[i]}</b>
            ${esc(d.open)} ~ ${esc(d.close)}${d.bs?` · 브레이크 ${esc(d.bs)} ~ ${esc(d.be)}`:""}${d.lo?` · 라스트오더 ${esc(d.lo)}`:""}${sessSummary(d)}</span>`).join("")}
          ${sc.holiday?`<span class="sch-d"><b>공휴</b>
            ${esc(sc.holiday.open)} ~ ${esc(sc.holiday.close)}${sc.holiday.bs?` · 브레이크 ${esc(sc.holiday.bs)} ~ ${esc(sc.holiday.be)}`:""}${sc.holiday.lo?` · 라스트오더 ${esc(sc.holiday.lo)}`:""}${sessSummary(sc.holiday)}</span>`:""}
        </div>
      </div>`;
    }).join("")}
    <div class="btn-row" style="margin-top:12px">
      <button class="btn" onclick="openSchedule(null)">운영시간 수정</button>
      <button class="btn" onclick="openOverride()">임시 영업·휴무</button>
    </div>
    <p class="f-note">운영시간을 바꿀 때는 적용 시작일을 정합니다.
      과거 기록은 그때의 시간으로 계산되므로 지난 예약률이 틀어지지 않습니다.</p>

    <div class="subhead">공휴일</div>
    <button class="togglebtn ${st.holidayMode!==false?'on':''}" onclick="toggleHoliday()">
      ${st.holidayMode!==false?"공휴일 운영시간 사용":"공휴일 구분 안 함"}
    </button>
    ${st.holidayMode!==false?`
      <label class="chk" style="margin-top:10px">
        <input type="checkbox" ${st.holidayAsWeekend!==false?"checked":""} onchange="toggleHolidayWeekend()">
        <span>코스 시간대에서 공휴일을 주말로 봅니다</span></label>
      ${(()=>{ const y = view.holYear || new Date().getFullYear(); const gap = holidayTableGap(); return `
      <div class="btn-row" style="margin-top:8px; align-items:center">
        <button class="btn sm" onclick="view.holYear=${y-1}; render()">◀</button><b>${y}년</b><button class="btn sm" onclick="view.holYear=${y+1}; render()">▶</button>
        <span class="muted" style="font-size:12px">${KR_HOLIDAYS[y]?"내장표 있음":"내장표 없음 — 직접 등록"}</span>
      </div>
      ${gap?`<div class="alert amber" style="margin:8px 0"><span class="ic">!</span><div><div class="a-t">${gap}년 공휴일이 등록되지 않았습니다</div><div class="a-s">내장표는 2026~2027년까지입니다. 아래에서 ${gap}년 공휴일을 직접 추가하세요(대체공휴일 포함). 안 하면 그날 평일 운영시간으로 계산됩니다.</div></div></div>`:""}
      <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px">
        ${holidaysOfYear(y, st).map(h=>`
          <span class="tag ${h.src==="추가"?"blue":""}" style="padding:6px 10px" title="${h.src}">${h.date.slice(5).replace("-","/")}
            <button onclick="delHoliday('${h.date}')" style="background:none;border:none;color:var(--rust);padding:0 0 0 5px" title="${h.src==="내장"?"이 날은 공휴일 아님으로":"삭제"}">×</button>
          </span>`).join("") || `<span class="muted" style="font-size:13px">${y}년 공휴일이 없습니다.</span>`}
        ${(st.holidaysOff||[]).filter(d=>d.slice(0,4)===String(y)).map(d=>`<span class="tag" style="padding:6px 10px; opacity:.55; text-decoration:line-through" title="제외됨">${d.slice(5).replace("-","/")}
            <button onclick="restoreHoliday('${d}')" style="background:none;border:none;color:var(--pine);padding:0 0 0 5px" title="다시 공휴일로">↺</button></span>`).join("")}
      </div>
      <div class="btn-row" style="margin-top:10px">
        <input id="hol-date" type="date" style="flex:1 1 160px">
        <button class="btn" onclick="addHoliday()">공휴일 추가</button>
      </div>
      <p class="f-note">2026~2027년 공휴일(대체공휴일 포함)은 들어 있습니다. 임시공휴일·선거일은 미리 알 수 없으니 정해지면 추가하세요. × 는 그날을 공휴일에서 뺍니다.</p>`; })()}`:""}`;

  /* ---------- 예약 규칙 ---------- */
  const ruleBody = `
    <p class="f-note" style="margin:0 0 12px"><b>점유 시간·접수 마감</b>은 운영시간의 <b>세션</b>(점심/저녁)에서 요일마다 정합니다 (운영시간 → 수정).</p>

    <div class="subhead">인원</div>
    <label class="f"><div class="lb">룸 최소 인원 기준</div>
      <button class="togglebtn ${st.minCountAdultsOnly!==false?'on':''}" onclick="toggleAdultOnly()">
        ${st.minCountAdultsOnly!==false?"성인 기준 (어린이 제외)":"총 인원 기준 (어린이 포함)"}</button>
      <div class="f-note">성인 기준이면 성인 1명·어린이 3명은 4인 룸 최소 인원에 못 미치는 것으로 봅니다.</div></label>
    <label class="f"><div class="lb">단체 기준 인원</div>
      <button class="numbtn" onclick="openNum('groupSize','단체 기준 인원',2,40)">${st.groupSize||8}<small>명</small></button>
      <div class="f-note">이 인원부터 확인에 ‘단체 손님’으로 뜹니다.</div></label>

    <div class="subhead">경고 기준</div>
    <label class="f"><div class="lb">겹침 강한 경고</div>
      <button class="numbtn" onclick="openNum('closeGapMin','같은 좌석에 몇 분 안에 겹치면 강한 경고',10,240,{step:10})">${st.closeGapMin != null ? st.closeGapMin : 60}<small>분 안</small></button>
      <div class="f-note">같은 좌석에 이 시간 안으로 다른 예약이 있으면 '1시간 안에 확정 예약' 식의 강한 확인창이 뜹니다. 그보다 멀면 약한 경고.</div></label>
    <label class="f"><div class="lb">분 단위 예약</div>
      <button class="togglebtn ${st.minuteSteps!==false?'on':''}" onclick="setSetting('minuteSteps', ${st.minuteSteps===false?'true':'false'})">${st.minuteSteps!==false?"5분 단위 조절 켬":"30분 단위만"}</button>
      <div class="f-note">끄면 시각 선택에서 분 눈금이 사라지고 30분 단위로만 받습니다(누님 답 대기).</div></label>
    <label class="f"><div class="lb">취소를 노쇼로 볼 기준</div>
      <div class="seg">${[["none","안 함"],["sameday","당일"],["day1","전날부터"],["day2","이틀 전부터"],["hours","N시간 전"],["after","시각 지난 뒤"]].map(([v,l])=>`<button class="${(st.noshowCancelRule||"none")===v?'on':''}" onclick="setSetting('noshowCancelRule','${v}')">${l}</button>`).join("")}</div>
      <div class="f-note">기준 안에서 취소하면 '노쇼에 해당합니다 — 노쇼 / 취소' 를 되묻습니다. 취소는 언제나 남겨 둡니다(어제 취소를 오늘 입력할 수도 있으니).${st.noshowCancelRule==="hours"?` 지금 기준 <button class="numbtn sm" onclick="openNum('noshowCancelHours','몇 시간 전부터',1,48)">${st.noshowCancelHours||3}시간</button>`:""}</div></label>
    <label class="f"><div class="lb">노쇼 경고 기준</div>
      <button class="numbtn" onclick="openNum('noshowWarnCount','노쇼 몇 회부터 경고',1,10)">${st.noshowWarnCount != null ? st.noshowWarnCount : 1}<small>회부터</small></button>
      <div class="f-note">같은 번호의 노쇼가 이 횟수 이상이면 새 예약 때 '노쇼 이력' 안내가 뜹니다.</div></label>

    <div class="subhead">브레이크</div>
    <label class="f"><div class="lb">브레이크타임 방식</div>
      <div class="seg">
        <button class="${(st.breakMode||"leave")==="leave"?"on":""}" onclick="setSetting('breakMode','leave')">매장을 비움</button>
        <button class="${st.breakMode==="order"?"on":""}" onclick="setSetting('breakMode','order')">음식 주문만 중단</button>
      </div>
      <div class="f-note">‘매장을 비움’이면 브레이크 시작 전에 식사가 끝나야 합니다.</div></label>
    ${st.breakMode==="order"?`
      <label class="f"><div class="lb">브레이크 전 마지막 입장</div>
        <button class="numbtn" onclick="openNum('breakEntryBuffer','브레이크 몇 분 전까지 받나요?',0,180,{step:10})">${st.breakEntryBuffer != null ? st.breakEntryBuffer : 60}<small>분 전</small></button>
      </label>`:""}`;

  /* ---------- 좌석 (8차) ---------- */
  const rooms = st.rooms.filter(isRoom), tables = st.rooms.filter(isTable);
  const floorsT = []; tables.forEach(t=>{ if(floorsT.indexOf(t.floor||"")<0) floorsT.push(t.floor||""); });
  const ord = (list, r) => { const i = list.indexOf(r); return `<span class="ordbtns">
        <button ${i===0?"disabled":""} onclick="moveSeat('${r.id}',-1)" title="위로">▲</button>
        <button ${i===list.length-1?"disabled":""} onclick="moveSeat('${r.id}',1)" title="아래로">▼</button></span><span class="ordnum">${i+1}</span>`; };
  const roomRowHtml = r => `
      <div class="rowitem seat">
        ${ord(rooms, r)}
        <span class="grow"><span class="t">${esc(r.name)}</span>
          <span class="s">평일 ${roomMin(r)}명부터 · 주말 ${r.minWeekend != null ? r.minWeekend : roomMin(r)}명부터 · 최적 ${roomOpt(r)} · 최대 ${r.capacity}${r.floor?` · ${esc(r.floor)}`:""}${blockSummary(r)}</span></span>
        <button class="numbtn sm" onclick="openNum('minCapacity','${esc(r.name)} 평일 최소 인원',1,30,{room:'${r.id}'})">평일 ${roomMin(r)}</button>
        <button class="numbtn sm" onclick="openNum('minWeekend','${esc(r.name)} 주말·공휴일 최소 인원',1,30,{room:'${r.id}'})">주말 ${r.minWeekend != null ? r.minWeekend : roomMin(r)}</button>
        <button class="numbtn sm" onclick="openNum('optCapacity','${esc(r.name)} 최적 인원 (안내용)',1,30,{room:'${r.id}'})">최적 ${roomOpt(r)}</button>
        <button class="numbtn sm" onclick="openNum('capacity','${esc(r.name)} 최대 인원',1,40,{room:'${r.id}'})">최대 ${r.capacity}</button>
        <label class="tbl-in">층
          <input value="${esc(r.floor||"")}" placeholder="1층" style="width:60px" onchange="setRoomText('${r.id}','floor',this.value)"></label>
        <button class="btn sm ${roomBlocks(r).length?'danger':''}" onclick="openBlocks('${r.id}')">${roomBlocks(r).length?`사용 중지 ${roomBlocks(r).length}건`:"사용 중지"}</button>
        <button class="btn sm danger" onclick="delRoom('${r.id}')">삭제</button>
      </div>`;
  const tableRowHtml = (list, t) => `
      <div class="rowitem seat tblrow">
        ${ord(list, t)}
        <span class="grow"><span class="t">${esc(t.name)}${t.note?` <small class="muted">${esc(t.note)}</small>`:""}</span>
          <span class="s">${esc(t.floor||"층 없음")} · ${t.seats||4}인석${t.capacity&&t.capacity!==t.seats?` · 최대 ${t.capacity}`:""}${roomMin(t)?` · 최소 ${roomMin(t)}`:""}${blockSummary(t)}</span>
          <span class="s">붙이기: ${(t.joinWith||[]).length ? (t.joinWith||[]).map(id=>{ const x = st.rooms.find(r=>r.id===id); return x ? esc(x.name) : ""; }).filter(Boolean).join(", ") : "없음"}</span></span>
        <button class="numbtn sm" onclick="openNum('seats','${esc(t.name)} 기본 인원',1,20,{room:'${t.id}'})">${t.seats||4}인석</button>
        <button class="btn sm" onclick="openTableEdit('${t.id}')">상세</button>
        <button class="btn sm ${roomBlocks(t).length?'danger':''}" onclick="openBlocks('${t.id}')">${roomBlocks(t).length?`중지 ${roomBlocks(t).length}`:"사용 중지"}</button>
        <button class="btn sm danger" onclick="delRoom('${t.id}')">삭제</button>
      </div>`;
  /* 설정은 임시본을 보므로 seatLabel(실제 설정 기준) 대신 임시본으로 이름을 만듭니다 — 방금 추가한 합침도 바로 보이게 */
  const dName = id => { const x = st.rooms.find(r=>r.id===id); return x ? x.name : "?"; };
  const jLabel = j => j.ids.map(dName).join("+") + " 룸";
  const joinRowHtml = j => `
      <div class="rowitem seat">
        <span class="grow"><span class="t">${esc(jLabel(j))}</span>
          <span class="s">${j.min}~${j.max}명${j.note?` · ${esc(j.note)}`:""}</span>
          <label class="chk" style="margin:4px 0 0"><input type="checkbox" ${j.split?"checked":""} onchange="setJoinFlag('${j.id}','split',this.checked)"><span>공간이 나뉨(원탁 등) — 배정할 때 손님 확인 창</span></label></span>
        <button class="numbtn sm" onclick="openNum('min','${esc(jLabel(j))} 최소',1,60,{join:'${j.id}'})">최소 ${j.min}</button>
        <button class="numbtn sm" onclick="openNum('max','${esc(jLabel(j))} 최대',1,80,{join:'${j.id}'})">최대 ${j.max}</button>
        <button class="btn sm danger" onclick="delJoin('${j.id}')">삭제</button>
      </div>`;
  /* 8차-K: 세 탭(룸 / 테이블 / 합침) — 한 폴드에 다 펼치면 너무 길었습니다 */
  const seatTab = view.seatTab || "room";
  const tabBtn = (k, label) => `<button class="${seatTab===k?'on':''}" onclick="view.seatTab='${k}'; render()">${label}</button>`;
  /* 테이블 붙임 짝 — 같은 층 안에서 서로 붙일 수 있는 테이블을 표로. 칸을 누르면 양쪽 다 바뀝니다 */
  const pairTable = fl => { const list = tables.filter(t=>(t.floor||"")===fl); if(list.length < 2) return "";
    return `<div class="lbl" style="margin:10px 0 4px">${esc(fl||"층 없음")} — 서로 붙일 수 있는 테이블</div>
    <div class="pairwrap"><table class="pairs"><tr><th></th>${list.map(t=>`<th>${esc(t.name)}</th>`).join("")}</tr>
      ${list.map(a=>`<tr><th>${esc(a.name)}</th>${list.map(b=>a.id===b.id?`<td class="self"></td>`:`<td><button class="pair ${(a.joinWith||[]).indexOf(b.id)>=0?'on':''}" onclick="toggleJoinWith('${a.id}','${b.id}')" title="${esc(a.name)} + ${esc(b.name)}">${(a.joinWith||[]).indexOf(b.id)>=0?"●":""}</button></td>`).join("")}</tr>`).join("")}
    </table></div>`; };
  const seatBody = `
    <p class="f-note" style="margin:0 0 12px">
      <b>배정 순서</b>는 좌석을 정하지 않은 손님에게 자리를 미리 잡아 둘 때 씁니다.
      인원이 맞는 좌석 중 <b>위에서부터</b> 고릅니다(▲▼로 순서를 바꾸세요). 룸과 테이블은 손님이 고른 쪽만 봅니다.</p>
    <div class="seg seattabs">${tabBtn("room","룸")}${tabBtn("table","테이블")}${tabBtn("join","합침")}</div>
    ${seatTab==="room" ? `
    <div class="subhead">룸 <span>최소(평일 / 주말·공휴일)보다 적으면 경고. 최적은 안내용(마법사에 표시)</span></div>
    ${rooms.map(roomRowHtml).join("")}
    <div class="btn-row" style="margin-top:8px">
      <input id="nr-name" placeholder="룸 이름" style="flex:2 1 120px">
      <input id="nr-min" type="number" min="1" value="6" title="최적(최소) 인원" style="flex:1 1 62px">
      <input id="nr-cap" type="number" min="1" value="7" title="최대 인원" style="flex:1 1 62px">
      <input id="nr-floor" placeholder="층" style="flex:1 1 60px">
      <button class="btn" onclick="addRoom('room')">룸 추가</button>
    </div>

` : ""}
    ${seatTab==="table" ? `
    <div class="subhead">테이블 <span>예약은 층까지만 받습니다. 여기 목록은 층의 '자리 수' 를 세는 근거 — 테이블 인원을 더한 값이 그 층 자리 수</span></div>
    <p class="f-note" style="margin:0 0 8px">층 구분 없이 <b>위에서부터 좋은 자리</b> 순서입니다(▲▼). 층은 표시·안내용. 1층 창가 다음이 지하 여포일 수도 있으니 섞어서 정하세요.</p>
    ${tables.map(t=>tableRowHtml(tables, t)).join("")}
    <div class="btn-row" style="margin-top:8px">
      <input id="nt-name" placeholder="테이블 이름 (예: 26)" style="flex:2 1 120px">
      <input id="nt-seats" type="number" min="1" value="4" title="기본 인원" style="flex:1 1 62px">
      <input id="nt-floor" placeholder="층" value="${esc(floorsT[0]||"1층")}" style="flex:1 1 60px">
      <button class="btn" onclick="addRoom('table')">테이블 추가</button>
    </div>

` : ""}
    ${seatTab==="join" ? `
    <div class="subhead">룸 합침 <span>중문을 떼어 두세 방을 한 팀이 쓰는 경우. 자동 배정에는 안 쓰고, 예약 받을 때 사람이 고릅니다</span></div>
    ${(st.joins||[]).map(joinRowHtml).join("") || `<div class="empty">합침 그룹이 없습니다.</div>`}
    <div class="btn-row" style="margin-top:8px; flex-wrap:wrap">
      ${rooms.map(r=>`<label class="chk" style="margin:0"><input type="checkbox" class="nj-room" value="${r.id}"><span>${esc(r.name)}</span></label>`).join("")}
    </div>
    <div class="btn-row" style="margin-top:6px">
      <input id="nj-min" type="number" min="1" value="12" title="최소" style="flex:1 1 62px">
      <input id="nj-max" type="number" min="1" value="14" title="최대" style="flex:1 1 62px">
      <input id="nj-note" placeholder="메모 (예: 원탁 — 손님 확인)" style="flex:3 1 160px">
      <button class="btn" onclick="addJoin()">합침 추가</button>
    </div>
    <div class="subhead" style="margin-top:20px">테이블 붙임 <span>같은 층에서 붙여 앉힐 수 있는 짝. 큰 팀이 오면 이 짝으로만 붙입니다(아니면 나눠 앉음)</span></div>
    ${floorsT.map(pairTable).join("")}` : ""}`;

  /* ---------- 코스 ---------- */
  const courseBody = `
    ${(st.courseGroups||DEFAULT_COURSE_GROUPS).map((g,i)=>`
      <div class="cgedit">
        <div class="row">
          <label class="f" style="flex:1 1 150px"><div class="lb">${i+1}행 이름</div>
            <input value="${esc(g.label)}" onchange="setCourseField(${i},'label',this.value)"></label>
          <label class="f" style="flex:2 1 220px"><div class="lb">항목 (쉼표로 구분)</div>
            <input value="${esc((g.items||[]).join(", "))}" onchange="setCourseItems(${i},this.value)"></label>
        </div>
        <div class="whenrow">
          <span class="lbl">적용 시간대</span>
          ${WHEN_OPTS.map(w=>`<button class="wbtn ${(g.when||[]).includes(w)?'on':''}" onclick="toggleWhen(${i},'${w}')">${w}</button>`).join("")}
          <button class="btn sm danger" style="margin-left:auto" onclick="delCourseRow(${i})">행 삭제</button>
        </div>
      </div>`).join("")}
    <div class="btn-row" style="margin-top:10px">
      <button class="btn" onclick="addCourseRow()">＋ 행 추가</button>
    </div>
    <p class="f-note">메뉴판 구성에 맞춰 행을 나누세요. 예약 시각에 맞는 행이 코스·세트 선택 팝업에서 강조됩니다. 저녁 코스는 종일, 점심 세트는 점심 시간에만 팝니다.</p>`;

  /* ---------- 예약경로 ---------- */
  const srcBody = `
    <div style="display:flex; flex-wrap:wrap; gap:6px">
      ${(st.sources||[]).map(x=>`<span class="tag" style="padding:6px 10px">${esc(x)}
        ${["전화 예약","네이버 예약","방문","기타"].indexOf(x)<0?`<button onclick="delSource('${jsq(x)}')" style="background:none;border:none;color:var(--rust);padding:0 0 0 5px">×</button>`:""}
      </span>`).join(" ")}
    </div>
    <div class="btn-row" style="margin-top:12px">
      <input id="ns" placeholder="예: 캐치테이블" style="flex:1 1 140px">
      <button class="btn" onclick="addSource()">추가</button>
    </div>`;

  /* ---------- 디스플레이 ---------- */
  const rows = displayRows();
  const dispBody = `
    <div class="subhead">평소 띄울 화면</div>
    <div class="seg">
      <button class="${tvType()!=="grid"?'on':''}" onclick="setTvType('list')">목록 (영상+예약)</button>
      <button class="${tvType()==="grid"?'on':''}" onclick="setTvType('grid')">좌석표</button>
    </div>
    <p class="f-note">입구에 걸어 두는 TV라면 <b>목록</b>이 낫습니다.
      손님은 지나가면서 3~5초 보기 때문에, 좌석표보다 시각 순으로 늘어놓는 편이 자기 예약을 빨리 찾습니다.<br>
      TV 화면에서도 우측 상단에 마우스를 올리거나 화면을 한 번 누르면 바꿀 수 있습니다.
      여기서 고른 값이 새로 켤 때의 기본입니다.</p>

    <div class="subhead">예약이 없을 때</div>
    <div class="seg">
      <button class="${st.tvIdleFull!==false?'on':''}" onclick="setPolicy('tvIdleFull', true)">광고만 전체 화면</button>
      <button class="${st.tvIdleFull===false?'on':''}" onclick="setPolicy('tvIdleFull', false)">빈 목록 그대로</button>
    </div>
    <p class="f-note">오늘 남은 예약이 하나도 없으면(30분 넘게 지난 것은 빼고) 목록·좌석표 대신 광고 영상만 화면 가득 틉니다. 예약이 생기면 다음 갱신(1분) 때 목록으로 돌아옵니다.</p>

    <div class="subhead">광고 영상 <span>목록 화면 왼쪽에 나옵니다</span></div>
    <input id="tv-ad" class="in-sm" value="${esc(st.tvAd||"")}" placeholder="ad.mp4"
      onchange="setPolicy('tvAd', this.value)">
    <p class="f-note">
      영상 파일을 <b>이 폴더에 같이 올려두고</b> 파일 이름만 적으면 됩니다 (예: <code>ad.mp4</code>).<br>
      · <b>H.264 (MP4)</b> 로 만드세요. 다른 형식은 구형 TV에서 안 나옵니다.<br>
      · 소리는 빼세요. 자동 재생이 막히고, 입구에서 소리가 나면 민폐입니다.<br>
      · 20~40초, 10MB 이하. 좌우가 잘리므로 <b>중요한 것은 가운데</b>에 두세요.<br>
      비워 두면 매장 사진이 천천히 넘어갑니다.</p>

    <div class="subhead">좌석표 화면 배치</div>
    <p class="f-note" style="margin:0 0 12px">
      좌석표를 띄울 때의 배치입니다. 3줄로 고정되며 한 줄에 최대 ${DISP_MAX}칸까지 놓을 수 있습니다.</p>
    <div class="urlbox">
      <div class="ub-t">TV 전용 주소</div>
      <div class="ub-row"><a class="ub-u" id="screen-url" href="${esc(screenUrl())}" target="_blank" rel="noopener">${esc(screenUrl())}</a><button class="btn sm" onclick="copyScreenUrl()">주소 복사</button></div>
    </div>
    ${rows.map((ids,ri)=>`
      <div class="disprow ${ids.length>DISP_MAX?'over':''}">
        <div class="dr-title">${ri+1}번째 줄 <span>${ids.length}칸${ids.length>DISP_MAX?" · 너무 많습니다":""}</span></div>
        <div class="dr-cells">
          ${ids.map(id=>{
            const r = st.rooms.find(x=>x.id===id);
            if(!r) return "";
            return `<span class="dcell">${esc(r.name)}
              <button ${ri===0?"disabled":""} onclick="moveDisp('${id}',-1)" title="윗줄로">▲</button>
              <button ${ri===2?"disabled":""} onclick="moveDisp('${id}',1)" title="아랫줄로">▼</button>
            </span>`;
          }).join("")}
          ${ids.length?"":`<span class="muted" style="font-size:13px">비어 있음</span>`}
        </div>
      </div>`).join("")}`;

  /* ---------- 보안 / 기타 ---------- */
  const adminBody = `
    <div class="btn-row">
      <button class="btn" onclick="openPinManage()">PIN 번호 관리</button>
      ${supaOn() ? `<button class="btn" onclick="openAdminPw()">관리자 비밀번호 변경</button>` : ""}
      <button class="btn" onclick="openLogs()">로그</button>
      <button class="btn" onclick="openRate()">예약률 추이</button>
      <button class="btn" onclick="openSmsFree()">문자 보내기</button>
      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>
      <button class="btn" onclick="openSlip()">비상 예약지 인쇄</button>
    </div>
    <p class="f-note">비상 예약지: 시스템이 안 될 때 손으로 받는 종이(A4 한 장에 6장). 열리면 Ctrl+P 로 인쇄해 카운터에 두세요.</p>
    <p class="f-note">설정은 관리자 비밀번호로 들어옵니다. PIN 관리·관리자 비밀번호 변경·로그·초기화는 한 번 더 묻습니다. PIN 은 직원과 공유하는 번호, 관리자 비밀번호는 사장님만 아는 것입니다.</p>`;

  /* 화면 크기 — 기기마다 적당한 값이 달라 사장님이 직접 고르게 둡니다.
     저장 위치가 settings 가 아니라 DATA._ui 인 이유: 이건 매장 운영 값이 아니라
     '이 기기에서 어떻게 보이는지'라 '적용하기' 없이 즉시 반영되는 편이 낫습니다. */
  /* 사장님이 정할 값들 — 코드에 박아 두면 나중에 못 바꿉니다 (작업 규칙) */
  const policyBody = `
    <div class="subhead">유아용 의자 기본값</div>
    <div class="seg">
      <button class="${st.chairDefault==="infants"?'on':''}" onclick="setPolicy('chairDefault','infants')">어린이 수와 같게</button>
      <button class="${st.chairDefault!=="infants"?'on':''}" onclick="setPolicy('chairDefault','zero')">0개</button>
    </div>
    <p class="f-note">어린이 인원을 입력할 때 의자 수가 자동으로 따라올지 정합니다.
      0개로 두면 어린이 수와 다를 때 경고가 뜹니다.</p>

    <div class="subhead">룸 정원 기준</div>
    <div class="seg">
      <button class="${st.minCountAdultsOnly!==false?'on':''}" onclick="setPolicy('minCountAdultsOnly',true)">성인만</button>
      <button class="${st.minCountAdultsOnly===false?'on':''}" onclick="setPolicy('minCountAdultsOnly',false)">어린이 포함 총원</button>
    </div>
    <p class="f-note">룸 최소·최대 인원을 따질 때 어린이를 셀지 정합니다.</p>

    <div class="subhead">라스트오더 임박 기준</div>
    <div class="seg">
      ${[30,60,90,120,180].map(v=>`<button class="${(st.loSoon!=null?st.loSoon:120)===v?'on':''}"
        onclick="setPolicy('loSoon',${v})">${v}분</button>`).join("")}
    </div>
    <p class="f-note">라스트오더까지 이만큼 남은 시각부터 '임박'으로 알립니다.
      손님께 라스트오더를 미리 안내하기 위한 것입니다.</p>`;

  const zBase = ZOOM_STEPS.indexOf(st.uiZoom) >= 0 ? st.uiZoom : 100, zAdj = (DATA._ui && DATA._ui.zoomAdj) || 0;
  const zoomBody = `
    <div class="lbl">모든 기기 공통 <span class="lbl-note">적용하기를 눌러야 반영</span></div>
    <div class="seg zoomseg">${ZOOM_STEPS.map(function(z){
      return `<button class="${zBase===z?'on':''}" onclick="setZoom(${z})">${z}%</button>`;
    }).join("")}</div>
    <p class="f-note">기기마다 다르게 보이면 더보기 → <b>화면 보정</b>(이 기기만, 바로 반영). 지금 이 기기: <b>${uiZoom()}%</b> (공통 ${zBase}% ${zAdj>=0?"+":""}${zAdj}).</p>
    <p class="f-note">글자와 버튼이 한 번에 커집니다. 태블릿·모니터에 맞춰 고르세요.
      손님용 디스플레이 모드에는 영향을 주지 않습니다.<br>
      <b>브라우저 확대(Ctrl +)를 함께 쓰면 두 배로 곱해집니다.</b>
      여기서 맞출 거라면 브라우저는 100%로 두세요.</p>
    <div class="subhead" style="margin-top:16px">전체화면</div>
    <label class="f"><div class="lb">로그인하면 전체화면으로</div>
      <button class="togglebtn ${(DATA._ui&&DATA._ui.fullscreen===false)?'':'on'}" onclick="setFullscreenAuto(${(DATA._ui&&DATA._ui.fullscreen===false)?'true':'false'})">${(DATA._ui&&DATA._ui.fullscreen===false)?"안 함":"전체화면 켬"}</button>
      <div class="f-note">이 기기에만 적용됩니다. 안드로이드·PC 크롬에서 주소창·탭이 사라집니다. 아이폰·아이패드는 브라우저가 막고 있어, 사파리 공유 → <b>홈 화면에 추가</b> 로 열면 같은 효과가 납니다. 전체화면에서 나오려면 ESC 또는 아래로 쓸어내리기.</div></label>`;

  /* ---------- 문자 안내 ---------- */
  const sm = { ...SMS_DEFAULT, ...(st.sms||{}) };
  /* 미리보기에 쓸 가짜 예약 — 실제 예약을 건드리지 않습니다 */
  const smsSample = {
    name:"김영수", phone:"010-1234-5678", people:4, infants:0,
    date: shiftDate(todayStr(), sm.remindOffset), time:"18:30",
    roomId:(st.rooms[0]||{}).id || null
  };
  const smsBodyUI = `
    <div class="subhead">문자 안내</div>
    <div class="seg">
      <button class="${sm.on?'on':''}" onclick="setSms('on',true)">보냄</button>
      <button class="${sm.on?'':'on'}" onclick="setSms('on',false)">안 보냄</button>
    </div>

    <div class="subhead">발신번호 <span>손님 폰에 찍히는 번호</span></div>
    <input id="sms-phone" type="tel" class="in-sm" value="${esc(sm.storePhone||"031-724-1004")}"
      placeholder="031-724-1004" oninput="setSms('storePhone',this.value)">
    <p class="f-note">실제로 문자를 보내려면 이 번호를 통신사에 미리 등록해야 합니다.</p>

    <div class="subhead">재안내 문자를 언제 보낼까요</div>
    <div class="seg">
      ${[2,1,0].map(o=>`<button class="${sm.remindOffset===o?'on':''}"
        onclick="setSms('remindOffset',${o})">${offsetLabel(o)}</button>`).join("")}
    </div>
    <div class="seg" style="margin-top:8px">
      ${remindHours(sm.remindOffset).map(h=>`<button class="${sm.remindHour===h?'on':''}"
        onclick="setSms('remindHour',${h})">${hourLabel(h)}</button>`).join("")}
    </div>
    <p class="f-note">
      ${sm.remindOffset===0
        ? "당일은 오전만 고를 수 있습니다. 저녁 예약 손님이 오후에 “오늘 예약이십니다”를 받으면 이미 늦습니다."
        : "오전 9시부터 오후 7시까지 고를 수 있습니다."}<br>
      <b>재안내 시각이 지난 뒤에 접수된 예약은 재안내가 나가지 않습니다.</b>
      지금 설정이면 ${offsetLabel(sm.remindOffset)} ${hm(pad(sm.remindHour)+":00")} 이후에 받은 예약이 그렇습니다.
      그런 건은 예약 상세에 이유가 뜨고, 거기서 직접 보내실 수 있습니다.</p>

    <div class="subhead">주차 안내 <span>재안내 문자에만 들어갑니다</span></div>
    <textarea id="sms-park" rows="3" class="in-sm" placeholder="비워 두면 문자에 안 들어갑니다"
      onchange="setSms('parkingNote',this.value)">${esc(sm.parkingNote||"")}</textarea>
    <p class="f-note">주차비나 발렛이 바뀌면 여기만 고치면 됩니다.</p>

    <div class="subhead">문안 <span>{매장} {이름} {일시} {인원} {주차} {오늘내일} 자리에 값이 들어갑니다</span></div>
    <div class="subhead">접수 문자 문안 <span>예약을 받은 즉시</span></div>
    <textarea id="sms-tpl-new" rows="9" class="in-sm" onchange="setSms('tplNew',this.value)">${esc(sm.tplNew||SMS_DEFAULT.tplNew)}</textarea>
    <div class="btn-row" style="margin:6px 0 12px"><button class="btn sm" onclick="setSms('tplNew',SMS_DEFAULT.tplNew)">기본 문안으로</button><button class="btn sm" onclick="previewSms('접수')">미리보기</button></div>
    <div class="subhead">재안내 문자 문안 <span>방문 전 재안내</span></div>
    <textarea id="sms-tpl-rem" rows="12" class="in-sm" onchange="setSms('tplRemind',this.value)">${esc(sm.tplRemind||SMS_DEFAULT.tplRemind)}</textarea>
    <div class="btn-row" style="margin:6px 0 0"><button class="btn sm" onclick="setSms('tplRemind',SMS_DEFAULT.tplRemind)">기본 문안으로</button><button class="btn sm" onclick="previewSms('재안내')">미리보기</button></div>
    <p class="f-note">{주차}는 위 주차 안내가 비어 있으면 그 줄이 통째로 빠집니다. {오늘내일}은 보내는 날 기준으로 “오늘 / 내일 / 모레” 가 들어갑니다.</p>

    <p class="f-note">보내는 시점을 바꾸면 “모레 / 내일 / 오늘” 이 자동으로 바뀝니다. 어린이가 있는 예약이면 인원이 “4명(어린이 1명 포함)” 처럼 나갑니다.</p>

    <div class="btn-row" style="margin-top:12px">
      <button class="btn" onclick="openSmsLog()">보낸 문자 보기</button>
    </div>`;

  /* 문안 옆 '미리보기' — 가짜 예약으로 채운 문자를 확인창에 */
  window.previewSms = function(kind){
    const smNow = { ...SMS_DEFAULT, ...(draft().sms||{}) };
    const sample = { ...smsSample, date: shiftDate(todayStr(), smNow.remindOffset) };
    const text = kind === "접수" ? smsText(sample, "접수") : smsText(sample, "재안내", smNow.remindOffset);
    uiAlert(kind === "접수" ? "접수 문자 — 이렇게 나갑니다" : `재안내 문자 — ${offsetLabel(smNow.remindOffset)} ${hourLabel(smNow.remindHour)}`, text, "ok");
  };
  const etcBody = `
    <div class="btn-row">
      <button class="btn" onclick="openNoshow()">노쇼 관리</button>
    </div>`;

  return `
    ${sec("hours","운영시간",`${hoursFor(todayStr()).open} ~ ${hoursFor(todayStr()).close}`, schedBody)}
    ${sec("rules","예약 규칙",`단체 ${st.groupSize||8}명${schedChip("rules")}`, ruleBody)}
    ${sec("seats","좌석",`룸 ${st.rooms.filter(isRoom).length} · 테이블 ${st.rooms.filter(isTable).length}${schedChip("seats")}`, seatBody)}
    ${sec("course","코스·세트 구성",`${(st.courseGroups||[]).length}행${schedChip("course")}`, courseBody)}
    ${sec("source","예약경로",`${(st.sources||[]).length}개`, srcBody)}
    ${sec("sms","문자 안내",
      sm.on===false ? "안 보냄"
        : `${offsetLabel(sm.remindOffset)} ${hm(pad(sm.remindHour)+":00")}`,
      smsBodyUI)}
    ${sec("disp","디스플레이 배치",`${rows.map(r=>r.length).join(" · ")}`, dispBody)}
    ${sec("policy","운영 판단 기준",
      `의자 ${st.chairDefault==="infants"?"어린이 수":"0개"} · 정원 ${st.minCountAdultsOnly===false?"총원":"성인"} · 임박 ${st.loSoon!=null?st.loSoon:120}분`,
      policyBody)}
    ${sec("zoom","화면 크기",`${uiZoom()}%`, zoomBody)}
    <div class="set-divider"></div>
    ${sec("admin","관리자",`PIN · 로그 · 초기화`, adminBody)}
    ${sec("etc","기타",`노쇼 관리`, etcBody)}

    ${dirty ? `<div class="applybar on"><span class="ab-t">저장하지 않은 변경이 있습니다</span></div>` : ""}`;
}
/* 디스플레이 배치에서 좌석을 다른 줄로 옮깁니다 */
/* 광고 영상 주소.
   TV 는 .../v3/screen/hanok 주소로 엽니다. 그 상태에서 <video src="ad.mp4"> 를 쓰면
   브라우저가 .../v3/screen/ad.mp4 를 찾습니다 — 폴더가 한 칸 깊어져 영상이 안 나옵니다.
   (history.replaceState 로 주소를 바꾸면 상대 주소의 기준도 같이 바뀝니다)
   그래서 파일 이름만 적었을 때는 앱이 있는 폴더를 직접 붙여 줍니다. */
/* 앱이 놓인 폴더 경로(끝 슬래시 없음). /v4/, /v4/index.html, /v4/screen/, /v4/screen/index.html, /v4/screen/hanok 전부 → /v4 */
function appDir(){
  try{
    return location.pathname
      .replace(/\/[^\/]*\.html?$/i, "")            /* index.html 떼기 */
      .replace(/\/screen(\/[a-z]*)?\/?$/i, "")       /* screen 폴더(와 매장 이름) 떼기 */
      .replace(/\/+$/, "");
  }catch(e){ return ""; }
}
/* 광고 영상은 screen/ 폴더에 둡니다 (손님용 화면과 한 묶음). 파일 이름만 적으면 그 폴더를 붙입니다 */
function adUrl(name){
  var v = (name || "").trim();
  if(!v) return "";
  /* 전체 주소나 경로를 직접 적었으면 그대로 씁니다 */
  if(v.indexOf("://") >= 0 || v.charAt(0) === "/") return v;
  return appDir() + "/screen/" + v;
}
function screenUrl(){
  try{
    /* 로컬(127.0.0.1·file:)에서 열어도 TV 에 넣을 주소는 실제 배포 주소여야 합니다(재아) */
    if(/^(127\.|localhost|file:)/.test(location.host || location.protocol)) return "https://jaealee.com/test/hanok/v7/screen/";
    return location.origin + appDir() + "/screen/";
  }catch(e){ return "/screen/"; }
}
function copyScreenUrl(){
  if(!navigator.clipboard) return uiAlert("복사 실패","주소를 직접 입력해 주세요.","warn");
  navigator.clipboard.writeText(screenUrl()).then(
    ()=>uiAlert("복사 완료","TV 브라우저 주소창에 붙여넣으세요.","ok"),
    ()=>uiAlert("복사 실패","주소를 직접 입력해 주세요.","warn"));
}
function moveDisp(id, dir){
  const st = draft();
  const rows = (st.displayRows && st.displayRows.length===3)
    ? st.displayRows.map(r=>[...r]) : displayRows().map(r=>[...r]);
  const from = rows.findIndex(r=>r.includes(id));
  const to = from + dir;
  if(from<0 || to<0 || to>2) return;
  rows[from] = rows[from].filter(x=>x!==id);
  rows[to].push(id);
  st.displayRows = rows;
  render();
}
function setSetting(k,v){ draft()[k]=v; render(); }
function toggleAdultOnly(){
  const st = draft();
  st.minCountAdultsOnly = st.minCountAdultsOnly===false;
  render();
}
function toggleHoliday(){
  const st = draft();
  st.holidayMode = st.holidayMode===false;
  render();
}
function addHoliday(){
  const v = document.getElementById("hol-date").value;
  if(!v) return;
  const st = draft();
  st.holidaysOff = (st.holidaysOff||[]).filter(x=>x!==v);
  st.holidays = [...new Set([...(st.holidays||[]), v])];
  view.holYear = Number(v.slice(0,4));
  render();
}
function delHoliday(d){
  const st = draft();
  if((st.holidays||[]).indexOf(d) >= 0) st.holidays = st.holidays.filter(x=>x!==d);
  else st.holidaysOff = (st.holidaysOff||[]).concat([d]);   /* 내장표의 날짜는 지울 수 없으니 '제외' 목록에 */
  render();
}
function restoreHoliday(d){ const st = draft(); st.holidaysOff = (st.holidaysOff||[]).filter(x=>x!==d); render(); }
/* 숫자 값을 팝업으로 고칩니다 (키패드 대신 큰 버튼) */
function openNum(key, title, min, max, ctx){
  view.form = {type:"num", key, title, min, max, ctx, val:null};
  render();
}
function toggleHolidayWeekend(){
  const st = draft();
  st.holidayAsWeekend = st.holidayAsWeekend===false;
  render();
}
function courseSet(){ const st=draft(); if(!st.courseGroups) st.courseGroups=deepClone(DEFAULT_COURSE_GROUPS); return st.courseGroups; }
function setCourseField(i,f,v){ courseSet()[i][f]=v; render(); }
function setCourseItems(i,v){
  courseSet()[i].items = v.split(",").map(x=>x.trim()).filter(Boolean); render();
}
function toggleWhen(i,w){
  const g=courseSet(); const cur = g[i].when||[];
  g[i].when = cur.includes(w) ? cur.filter(x=>x!==w) : [...cur, w];
  render();
}
function addCourseRow(){ courseSet().push({id:newId("cg"), label:"새 행", items:[], when:[]}); render(); }
async function delCourseRow(i){
  const g=courseSet();
  if(!await uiConfirm("행을 삭제할까요?", `${g[i].label} — 항목 ${(g[i].items||[]).length}개`, {ok:"삭제"})) return;
  g.splice(i,1); render();
}
/* 설정 목록 한 줄에 붙는 사용 중지 요약 — 지금 걸린 것만 짧게 */
function blockSummary(r){
  const list = roomBlocks(r);
  if(!list.length) return "";
  const now = blockedAt(r, todayStr());
  const txt = now
    ? `사용 중지 중${now.note?` (${esc(now.note)})`:""}`
    : `사용 중지 예정 ${list.length}건`;
  return ` · <b style="color:var(--rust)">${txt}</b>`;
}
function openBlocks(id){ view.form={type:"blocks", id}; view.blkDraft=null; render(); }
/* 같은 종류(룸끼리·같은 층 테이블끼리) 안에서만 순서를 바꿉니다 — 배열은 룸·테이블이 섞여 있어 절대 index 로 바꾸면 종류를 넘어감 */
function moveSeat(id, d){
  const st = draft(), arr = st.rooms;
  const r = arr.find(x=>x.id===id); if(!r) return;
  const same = arr.filter(x=>x.type===r.type);   /* 테이블은 층 구분 없이 전체 순서(재아) */
  const k = same.indexOf(r), j = k + d;
  if(j < 0 || j >= same.length) return;
  const other = same[j];
  const i1 = arr.indexOf(r), i2 = arr.indexOf(other);
  arr[i1] = other; arr[i2] = r;
  render();
}
function setRoomText(id,field,v){
  const st=draft();
  st.rooms = st.rooms.map(r=>r.id===id?{...r,[field]:v}:r);
  render();
}
async function addRoom(type){
  const st = draft();
  if(type === "table"){
    const name = (document.getElementById("nt-name").value||"").trim();
    if(!name) return uiAlert("테이블 이름을 입력하세요","","warn");
    const seats = Math.max(1, parseInt(document.getElementById("nt-seats").value)||4);
    st.rooms.push({id:"t_"+newId("t").slice(2,10), name, type:"table", floor:(document.getElementById("nt-floor").value||"").trim(), seats, joinWith:[]});
  }else{
    const name = (document.getElementById("nr-name").value||"").trim();
    if(!name) return uiAlert("룸 이름을 입력하세요","","warn");
    const cap = Math.max(1, parseInt(document.getElementById("nr-cap").value)||6);
    const min = Math.max(1, parseInt(document.getElementById("nr-min").value)||cap);
    st.rooms.push({id:"r_"+newId("r").slice(2,10), name, type:"room", floor:(document.getElementById("nr-floor").value||"").trim(), capacity:cap, minCapacity:Math.min(min,cap), tuned:true});
  }
  render();
}
/* 테이블 상세 — 최대 인원·최소·붙일 수 있는 테이블·메모 */
function openTableEdit(id){ view.form={type:"tedit", id}; render(); }
function sheetTableEdit(){
  const st = draft(), t = st.rooms.find(x=>x.id===view.form.id);
  if(!t) return `${sheetHead("테이블")}<div class="empty">없음</div>`;
  const others = st.rooms.filter(x=>isTable(x) && x.id!==t.id && (x.floor||"")===(t.floor||""));
  return `
    ${sheetHead(`${esc(t.name)} 테이블`)}
    <div class="grid2">
      <label class="f"><div class="lb">기본 인원</div><button class="numbtn" onclick="openNum('seats','기본 인원',1,20,{room:'${t.id}'})">${t.seats||4}<small>명</small></button></label>
      <label class="f"><div class="lb">최대 인원 <span class="lbl-note">비우면 기본과 같음</span></div><button class="numbtn" onclick="openNum('capacity','최대 인원',1,20,{room:'${t.id}'})">${t.capacity||t.seats||4}<small>명</small></button></label>
      <label class="f"><div class="lb">최소 인원 <span class="lbl-note">0 = 제한 없음</span></div><button class="numbtn" onclick="openNum('minCapacity','최소 인원',0,20,{room:'${t.id}'})">${t.minCapacity||0}<small>명</small></button></label>
      <label class="f"><div class="lb">층</div><input value="${esc(t.floor||"")}" onchange="setRoomText('${t.id}','floor',this.value)"></label>
    </div>
    <label class="f"><div class="lb">메모 <span class="lbl-note">예: 파셜룸</span></div><input value="${esc(t.note||"")}" onchange="setRoomText('${t.id}','note',this.value)"></label>
    <div class="lbl" style="margin-top:12px">붙일 수 있는 테이블 <span class="lbl-note">같은 층만. 서로 체크해야 붙습니다</span></div>
    <div class="btn-row" style="flex-wrap:wrap">
      ${others.map(o=>`<button class="wbtn ${(t.joinWith||[]).indexOf(o.id)>=0?'on':''}" onclick="toggleJoinWith('${t.id}','${o.id}')">${esc(o.name)}</button>`).join("") || `<span class="muted">같은 층에 다른 테이블이 없습니다</span>`}
    </div>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
function toggleJoinWith(id, other){
  const st = draft(), t = st.rooms.find(x=>x.id===id), o = st.rooms.find(x=>x.id===other);
  if(!t || !o) return;
  const on = (t.joinWith||[]).indexOf(other) >= 0;
  t.joinWith = on ? (t.joinWith||[]).filter(x=>x!==other) : (t.joinWith||[]).concat([other]);
  o.joinWith = on ? (o.joinWith||[]).filter(x=>x!==id) : ((o.joinWith||[]).indexOf(id)>=0 ? o.joinWith : (o.joinWith||[]).concat([id]));   /* 양쪽 다 */
  render();
}
async function addJoin(){
  const st = draft();
  const ids = Array.prototype.map.call(document.querySelectorAll(".nj-room:checked"), el=>el.value);
  if(ids.length < 2) return uiAlert("합칠 룸을 두 개 이상 고르세요","","warn");
  if((st.joins||[]).some(j=>sameIds(j.ids, ids))) return uiAlert("이미 있는 합침입니다","","warn");
  const min = Math.max(1, parseInt(document.getElementById("nj-min").value)||1), max = Math.max(min, parseInt(document.getElementById("nj-max").value)||min);
  st.joins = (st.joins||[]).concat([{id:"j_"+newId("j").slice(2,10), ids, min, max, note:(document.getElementById("nj-note").value||"").trim()}]);
  render();
}
function setJoinFlag(id, k, v){ const st = draft(); st.joins = (st.joins||[]).map(j=>j.id===id?Object.assign({}, j, {[k]:v}):j); render(); }
async function delJoin(id){
  const st = draft(); const j = (st.joins||[]).find(x=>x.id===id);
  if(!await uiConfirm("합침을 삭제할까요?", j ? j.ids.map(id=>{ const x = st.rooms.find(r=>r.id===id); return x ? x.name : "?"; }).join("+")+" 룸" : "", {ok:"삭제"})) return;
  st.joins = (st.joins||[]).filter(x=>x.id!==id); render();
}
async function delRoom(id){
  const st = draft();
  const r = st.rooms.find(x=>x.id===id);
  if(!await uiConfirm("이 좌석을 삭제할까요?", `${r?r.name:""} — 기존 예약은 ‘미배정’으로 표시됩니다.`, {ok:"삭제"})) return;
  st.rooms = st.rooms.filter(x=>x.id!==id);
  st.rooms.forEach(x=>{ if(x.joinWith) x.joinWith = x.joinWith.filter(y=>y!==id); });
  st.joins = (st.joins||[]).filter(j=>j.ids.indexOf(id) < 0);
  render();
}
async function addSource(){
  const el = document.getElementById("ns");
  const v = (el?el.value:"").trim();
  const st = draft();
  if(!v || (st.sources||[]).includes(v)) return;
  st.sources = [...(st.sources||[]), v];
  render();
}
function delSource(x){ const st=draft(); st.sources=(st.sources||[]).filter(s=>s!==x); render(); }

/* 묶음 제목 옆 "9월 22일부터 바뀜" — 예정이 걸려 있으면 */
function schedChip(group){
  const l = schedFor(group, store().settings);
  return l.length ? ` <span class="pill amber" onclick="event.stopPropagation(); openScheduled()">${esc(dateLabel(l[0].from))}${l[0].to?" ~":""}부터 바뀜${l.length>1?` 외 ${l.length-1}`:""}</span>` : "";
}
