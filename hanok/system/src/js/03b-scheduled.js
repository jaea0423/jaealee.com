/* ---------- 예정 설정 ----------
   "다음 주 월요일부터 좌석이 하나 는다", "연말까지만 코스가 바뀐다" 처럼 날짜가 정해진 설정 변경.
   지금 설정(settings) 은 그대로 두고, settings.scheduled[] 에 "언제부터(·언제까지) 어느 묶음이 이 값" 을 쌓아 둡니다.
   날짜가 필요한 계산은 store().settings 대신 settingsAt(date) 를 씁니다 — 그 날짜에 유효한 예정을 덮어 씌운 설정.
   운영시간은 예전부터 schedules[] 로 같은 일을 했으니 여기서는 다루지 않습니다.

   항목 모양: { id, from:"2026-09-22", to:null|"2026-12-31", group:"seats"|"rules"|"course",
               values:{ rooms:[…], joins:[…] }, note, createdAt, by }
   · to 가 없으면 그 날부터 계속 — 날짜가 되면 absorbScheduled() 가 settings 로 흡수하고 목록에서 뺍니다(기록 남김)
   · to 가 있으면 그 기간에만 유효, 지나면 목록에서 빠집니다 */
const SCHED_GROUPS = {
  seats:  { label:"좌석",        keys:["rooms","joins"] },
  rules:  { label:"예약 규칙",   keys:["groupSize","closeGapMin","minuteSteps","noshowWarnCount","noshowCancelRule","noshowCancelHours","breakMode","minCountAdultsOnly"] },
  course: { label:"코스·세트 구성", keys:["courseGroups"] }
};
function schedList(st){ return ((st || store().settings).scheduled || []).slice().sort((a,b)=>a.from.localeCompare(b.from)); }
/* 그 날짜에 유효한 설정. 예정이 없으면 settings 그대로(같은 객체) */
function settingsAt(date, st){
  st = st || store().settings;
  const list = st.scheduled || [];
  if(!list.length || !date) return st;
  let out = null;
  schedList(st).forEach(e => {
    if(e.from > date || (e.to && date > e.to)) return;
    if(!out) out = Object.assign({}, st);
    Object.keys(e.values || {}).forEach(k => { out[k] = e.values[k]; });
  });
  return out || st;
}
function roomsAt(date){ return settingsAt(date).rooms || []; }
function joinsAt(date){ return settingsAt(date).joins || []; }
/* 어느 날짜에도 나올 수 있는 좌석 전부(지금 + 예정) — id 로 찾을 때 씁니다 */
function allSeatsEver(){
  const st = store().settings, seen = {}, out = [];
  const add = list => (list||[]).forEach(x => { if(!seen[x.id]){ seen[x.id] = 1; out.push(x); } });
  add(st.rooms); (st.scheduled||[]).forEach(e => add(e.values && e.values.rooms));
  return out;
}
function allJoinsEver(){
  const st = store().settings, seen = {}, out = [];
  const add = list => (list||[]).forEach(x => { if(!seen[x.id]){ seen[x.id] = 1; out.push(x); } });
  add(st.joins); (st.scheduled||[]).forEach(e => add(e.values && e.values.joins));
  return out;
}
/* 그 묶음에 걸린 예정 (설정 화면 표시용) */
function schedFor(group, st){ return schedList(st).filter(e => e.group === group && (!e.to || e.to >= todayStr())); }
function schedLabel(e){
  const g = SCHED_GROUPS[e.group] || {label:e.group};
  return `${dateLabel(e.from)}${e.to ? ` ~ ${dateLabel(e.to)}` : "부터"} · ${g.label}${e.note ? ` · ${e.note}` : ""}`;
}

/* 날짜가 된 예정을 설정으로 흡수, 기간이 끝난 예정을 정리. 불러올 때·자정 넘길 때·적용하기 때 부릅니다 */
function absorbScheduled(){
  const st = store().settings, today = todayStr();
  const list = st.scheduled || []; if(!list.length) return false;
  let changed = false;
  const keep = [];
  list.slice().sort((a,b)=>a.from.localeCompare(b.from)).forEach(e => {
    if(e.to && e.to < today){ changed = true; logEvent("예정 설정 종료", schedLabel(e)); return; }      /* 기간 끝 */
    if(!e.to && e.from <= today){                                                                       /* 날짜 됨 → 지금 설정으로 */
      Object.keys(e.values||{}).forEach(k => { st[k] = e.values[k]; });
      st._setlog = (st._setlog || []).concat([{at:new Date().toISOString(), who:"예정 적용", items:[schedLabel(e)]}]).slice(-60);
      logEvent("예정 설정 적용", schedLabel(e)); changed = true; return;
    }
    keep.push(e);
  });
  if(changed){ st.scheduled = keep; if(view.draft) view.draft = deepClone(st); takeSnapshot(); saveData(); }
  return changed;
}

/* ---------- 예정으로 넣기: 적용하기 때 바뀐 묶음이 있으면 묻습니다 ---------- */
/* 임시본과 지금 설정을 묶음별로 비교해 바뀐 묶음 이름을 돌려줍니다 */
function changedGroups(before, after){
  return Object.keys(SCHED_GROUPS).filter(g => SCHED_GROUPS[g].keys.some(k => JSON.stringify(before[k]) !== JSON.stringify(after[k])));
}
/* 예정 항목이 걸리는 예약 — 좌석이 없어지거나 정원이 줄거나 코스가 사라지는 경우. 막지 않고 목록으로 보여 줍니다 */
function schedConflicts(e){
  const s = store(), st = s.settings, v = e.values || {}, out = [];
  const inRange = r => r.date >= e.from && (!e.to || r.date <= e.to) && r.status !== "취소" && r.status !== "노쇼";
  const list = s.reservations.filter(inRange);
  if(v.rooms){
    const ids = {}; v.rooms.forEach(x => { ids[x.id] = x; });
    list.forEach(r => {
      const used = (typeof seatsOf === "function" ? seatsOf(r) : [r.roomId]).filter(Boolean);
      const gone = used.filter(id => !ids[id]);
      if(gone.length) out.push(`${dateLabel(r.date)} ${hm(r.time)} ${r.name} — 좌석 ${gone.map(id => (seatById(id)||{}).name || id).join("+")} 이 없어짐`);
      else if(r.roomId && ids[r.roomId]){
        /* 합친 좌석은 묶음 정원으로 봅니다(예정 joins 가 있으면 그것, 없으면 지금 것). 지금도 이미 넘는 예약은 예정 때문이 아니니 빼고,
           예정으로 정원이 '줄어서' 넘게 되는 것만 셉니다(검토: 합침 12명이 "주유 정원 7명 넘음" 으로 22건 잡혔음) */
        const joins = v.joins || st.joins || [];
        const j = joins.find(g => sameIds(g.ids, used));
        const after = j ? j.max : used.reduce((a, id) => a + seatMax(ids[id]), 0);
        if(pplOf(r) > after && after < seatsMax(used)) out.push(`${dateLabel(r.date)} ${hm(r.time)} ${r.name} ${pplOf(r)}명 — ${used.map(id => ids[id].name).join("+")} 정원 ${after}명 넘음`);
      }
    });
  }
  if(v.courseGroups){
    const ok = {}; v.courseGroups.forEach(g => (g.items||[]).forEach(it => { ok[g.id + "|" + it] = 1; }));
    list.forEach(r => {
      const bad = Object.keys(r.courses||{}).filter(k => (r.courses[k] > 0) && !ok[k]);
      if(bad.length) out.push(`${dateLabel(r.date)} ${hm(r.time)} ${r.name} — 코스 ${bad.map(k => k.split("|")[1]).join(", ")} 이 구성에서 빠짐`);
    });
  }
  return out;
}
/* 적용하기에서 부름. 바뀐 묶음이 있으면 "지금 바로 / 날짜부터" 를 묻고, 날짜면 예정으로 넣고 그 묶음은 임시본에서 되돌립니다.
   돌려주는 값: true = 계속 적용하기 진행, false = 취소 */
async function askScheduleOnApply(before, after){
  const groups = changedGroups(before, after);
  if(!groups.length) return true;
  const names = groups.map(g => SCHED_GROUPS[g].label).join(" · ");
  const when = await uiChoose ? await uiChoose(`${names} 변경 — 언제부터 적용할까요?`, ["지금 바로", "날짜를 정해서 (예정)"]) : 0;
  if(when == null) return false;
  if(when === 0) return true;
  const from = await uiPrompt("적용 시작일", "YYYY-MM-DD", {value:shiftDate(todayStr(), 1), ok:"다음"});
  if(!from || !/^\d{4}-\d{2}-\d{2}$/.test(from)) return false;
  if(from <= todayStr()){ await uiAlert("내일부터 정할 수 있습니다", "오늘 바로면 '지금 바로' 를 고르세요.", "warn"); return false; }
  let to = await uiPrompt("적용 종료일 (비우면 계속)", "YYYY-MM-DD · 이 날까지만 쓰고 원래대로", {value:"", ok:"다음"});
  if(to == null) return false;
  to = to.trim() || null;
  if(to && (!/^\d{4}-\d{2}-\d{2}$/.test(to) || to < from)){ await uiAlert("종료일이 시작일보다 빠릅니다", "", "warn"); return false; }
  const note = ((await uiPrompt("메모 (선택)", "예: 여포 파셜룸 추가", {value:"", ok:"확인"})) || "").trim();
  const st = store().settings;
  st.scheduled = st.scheduled || [];
  /* 예정은 '그 묶음 전체의 모습' 을 날짜순으로 덮어씁니다. 같은 묶음에 더 이른 예정이 있으면 이번 것이 그 뒤에 덮으므로
     그 예정의 내용은 이번 값에 들어 있어야 합니다 — 지금 설정을 고쳐 만든 값이라 빠져 있을 수 있어 한 번 알립니다 */
  for(const g of groups){
    const earlier = (st.scheduled||[]).filter(e => e.group === g && e.from < from && !e.to);
    if(earlier.length){
      const ok = await uiConfirm(`${SCHED_GROUPS[g].label}에 더 이른 예정이 있습니다`,
        earlier.map(schedLabel).join("\n") + `\n\n이번 예정(${dateLabel(from)}부터)은 그 뒤에 적용되어 위 내용을 덮어씁니다.\n위 예정에서 바꾼 것도 이번 값에 들어 있어야 합니다. 확실하지 않으면 취소하고 예정 목록을 먼저 보세요.`,
        {ok:"알고 있습니다, 계속", cancel:"취소"});
      if(!ok) return false;
    }
  }
  for(const g of groups){
    const values = {}; SCHED_GROUPS[g].keys.forEach(k => { if(after[k] !== undefined) values[k] = deepClone(after[k]); });
    const e = { id:"sc_" + Date.now() + "_" + g, from, to, group:g, values, note, createdAt:new Date().toISOString(), by:SESSION ? SESSION.who : "-" };
    const conf = schedConflicts(e);
    if(conf.length){
      const ok = await uiConfirm(`${SCHED_GROUPS[g].label} 예정에 걸리는 예약 ${conf.length}건`, conf.slice(0,8).join("\n") + (conf.length > 8 ? `\n외 ${conf.length-8}건` : "") + "\n\n예약은 지워지지 않고 '경고 예약' 으로 남습니다.", {ok:"그래도 예정", cancel:"취소"});
      if(!ok) return false;
    }
    st.scheduled.push(e);
    /* 그 묶음은 지금 설정으로 되돌립니다 — 예정에만 들어가야 하니까 */
    SCHED_GROUPS[g].keys.forEach(k => { if(before[k] === undefined) delete after[k]; else after[k] = deepClone(before[k]); });
    logEvent("예정 설정 등록", schedLabel(e));
  }
  return true;
}

/* ---------- 예정 목록 시트 (되돌리기 왼쪽 단추) ---------- */
function openScheduled(){ view.form = {type:"sched2"}; render(); }
function sheetScheduled(){
  const list = schedList().filter(e => !e.to || e.to >= todayStr());
  const rows = list.length ? list.map(e => {
    const conf = schedConflicts(e);
    return `<div class="rowitem" style="display:block">
      <div class="t"><b>${esc(dateLabel(e.from))}${e.to ? ` ~ ${esc(dateLabel(e.to))}` : " 부터"}</b> <span class="tag">${esc(SCHED_GROUPS[e.group].label)}</span>${conf.length ? `<span class="tag rust">걸리는 예약 ${conf.length}</span>` : ""}</div>
      <div class="s">${esc(schedSummary(e))}${e.note ? ` · ${esc(e.note)}` : ""} · ${esc(e.by||"")} ${esc((e.createdAt||"").slice(0,10))}</div>
      <div class="btn-row" style="margin-top:8px">
        <button class="btn sm" onclick="schedApplyNow('${e.id}')">지금 적용</button>
        <button class="btn sm danger" onclick="schedDelete('${e.id}')">삭제</button></div>
    </div>`; }).join("")
    : `<div class="empty">예정된 설정 변경이 없습니다.<br><span class="s">설정을 고치고 '적용하기' 에서 '날짜를 정해서' 를 고르면 여기에 쌓입니다.</span></div>`;
  return `${sheetHead(`예정된 설정 · ${list.length}건`)}
    <div class="card searchbox">${rows}</div>
    <p class="f-note">날짜가 되면 아무도 안 눌러도 그 날부터 적용됩니다. 기간이 있는 것은 끝나면 원래대로 돌아옵니다.</p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
function schedSummary(e){
  const v = e.values || {};
  if(v.rooms) return `룸 ${v.rooms.filter(isRoom).length} · 테이블 ${v.rooms.filter(isTable).length} · 합침 ${(v.joins||[]).length}`;
  if(v.courseGroups) return `${v.courseGroups.length}행 · ${v.courseGroups.map(g => g.label).join(", ")}`;
  return Object.keys(v).map(k => `${k} ${JSON.stringify(v[k])}`).join(" · ").slice(0, 80);
}
async function schedDelete(id){
  const st = store().settings, e = (st.scheduled||[]).find(x => x.id === id); if(!e) return;
  if(!await uiConfirm("이 예정을 지울까요?", schedLabel(e), {ok:"지우기"})) return;
  st.scheduled = st.scheduled.filter(x => x.id !== id); if(view.draft) view.draft.scheduled = deepClone(st.scheduled);
  logEvent("예정 설정 삭제", schedLabel(e)); saveData(); render();
}
async function schedApplyNow(id){
  const st = store().settings, e = (st.scheduled||[]).find(x => x.id === id); if(!e) return;
  if(!await uiConfirm("지금 바로 적용할까요?", schedLabel(e) + "\n\n예정 날짜를 기다리지 않고 오늘부터 씁니다.", {ok:"지금 적용"})) return;
  Object.keys(e.values||{}).forEach(k => { st[k] = e.values[k]; });
  st.scheduled = st.scheduled.filter(x => x.id !== id); if(view.draft) view.draft = deepClone(st);
  logEvent("예정 설정 앞당겨 적용", schedLabel(e)); takeSnapshot(); saveData(); render();
}
