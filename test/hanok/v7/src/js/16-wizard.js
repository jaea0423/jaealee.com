/* ============================================================
   예약 등록 마법사 (5단계) — 전화 응대 순서대로 진행
   직원 누구나 화면에 뜬 질문을 그대로 읽으면 되도록 구성
   ============================================================ */
let WZ = null;   /* 진행 중인 예약 입력 상태. null이면 닫힘 */

/* 손님께 그대로 읽어 드리는 말은 큰따옴표로 묶습니다 —
   직원이 화면을 보고 읽을 때 어디까지가 손님께 할 말인지 바로 보이게 */
const WZ_STEPS = [
  "어떤 경로로 온 예약인가요?",
  "\u201C날짜와 시간은 언제로 해 드릴까요?\u201D",
  "\u201C몇 분이서 오세요?\u201D",
  "\u201C룸과 테이블 중 어디로 해 드릴까요?\u201D",
  "\u201C식사는 코스로 준비해 드릴까요?\u201D",
  "\u201C예약자 성함과 연락처 부탁드립니다.\u201D",
  "\u201C알러지나 따로 요청하실 사항 있으세요?\u201D"
];
const WZ_LABELS = ["경로","날짜·시간","인원","좌석","메뉴","예약자","요청사항"];
const LAST_STEP = 6;

/* 코스 구성 기본값 — 실제 값은 설정(settings.courseGroups)에서 관리합니다 */
const DEFAULT_COURSE_GROUPS = [
  { id:"cg_dinner",  label:"저녁 (종일)", items:["오","촉","한","위"],     when:["종일"] },
  { id:"cg_wdlunch", label:"평일 점심",   items:["요리사","동한","서한"],  when:["평일점심"] },
  { id:"cg_welunch", label:"주말 점심",   items:["요리사","B","A"],        when:["주말점심"] }
];
const WHEN_OPTS = ["종일","평일점심","평일저녁","주말점심","주말저녁"];
function courseGroups(){ return store().settings.courseGroups || DEFAULT_COURSE_GROUPS; }
/* 코스 키의 앞부분(cg_xxx)으로 묶음을 찾습니다.
   ※ 예전 키는 앞부분이 '순서 번호'(0, 1, 2) 였습니다. 설정에서 순서만 바꿔도
      저장된 예약이 전부 다른 묶음을 가리키게 되는 구조라 고정 id 로 바꿨습니다.
      옛 키는 migrate() 가 옮겨 주지만, 혹시 남아 있으면 번호로도 찾아 줍니다. */
function courseGroupById(gs, id){
  var i;
  for(i = 0; i < gs.length; i++) if(gs[i].id === id) return gs[i];
  if(/^\d+$/.test(id)) return gs[+id] || null;
  return null;
}

/* ---------- 뒤로가기 보호 ----------
   앱은 주소를 history.replaceState 로만 바꾸므로 브라우저 뒤로가기가 눌리면 사이트 밖으로 나가 입력이 날아갔습니다.
   마법사·수정 시트를 열 때 history 에 한 칸(pushState) 넣어 두면 뒤로가기는 '닫기' 가 됩니다 —
   닫을지 한 번 묻고, 취소하면 그 칸을 다시 넣습니다. 정상으로 닫을 때는 그 칸을 도로 빼서(histPop) 뒤로가기가 헛돌지 않게 합니다.
   새로고침·탭 닫기는 beforeunload 로 브라우저 기본 확인창 — 문구는 브라우저가 정하고 우리 문구는 못 넣습니다.
   디스플레이(view.display)에서는 둘 다 걸지 않습니다 (TV 는 방치용) */
function isEditingRes(){ return !view.display && (!!WZ || !!(view.form && view.form.type === "res")); }
/* history.back() 은 비동기라, 처리되기 전에 다시 열고 닫으면 back() 이 두 번 나가 사이트 밖으로 나갑니다.
   되돌리는 중(HIST_PENDING)에는 push/pop 을 하지 않고, 그 back() 의 popstate 가 왔을 때 상황에 맞게 정리합니다 */
var HIST_PENDING = false;
function histPush(){
  if(view.display || HIST_PENDING) return;   /* 되돌리는 중이면 popstate 가 칸을 다시 넣어 줍니다 */
  try{ if(!(history.state && history.state.wz)) history.pushState({wz:1}, ""); }catch(e){}
}
function histPop(){
  if(HIST_PENDING) return;
  try{ if(history.state && history.state.wz){ HIST_PENDING = true; history.back(); } }catch(e){}
}
window.addEventListener("popstate", async function(){
  if(HIST_PENDING){
    HIST_PENDING = false;
    /* 닫는 사이에 다른 입력이 열렸으면(마법사 완료 → 새 예약 등) 칸을 도로 넣어 보호를 이어 갑니다 */
    if(isEditingRes()){ try{ history.pushState({wz:1}, ""); }catch(e){} }
    return;
  }
  if(!isEditingRes()) return;
  if(!await uiConfirm2("입력 중인 예약이 있습니다. 나갈까요?")){
    try{ history.pushState({wz:1}, ""); }catch(e){}
    return;
  }
  WZ = null; view.form = null; tmpRes = null; render();
});
window.addEventListener("beforeunload", function(e){
  if(!isEditingRes()) return;
  e.preventDefault(); e.returnValue = "";
});
function openWizard(date){
  if(readonlyBlock()) return;
  Object.keys(view.open).forEach(function(x){ view.open[x] = false; });   /* 마법사 다녀오면 목록 폴드는 접힘 */
  histPush();
  WZ = {
    step:0, source:null, sourceDetail:"",
    /* 8차-Y(재아): 등록 버튼으로 열면 날짜가 안 골라진 채 시작합니다 — 보고 있던 날짜가 슬쩍 들어가면 헷갈립니다. 달력은 보던 달로 */
    calMonth:(date||view.date).slice(0,7),
    date:date||null, time:null,
    people:null, infants:0, chairs:0, customPeople:false, phoneNone:false,
    menuType:null, courses:{}, courseOpen:false,
    seat:null, seatExtra:[], seatKind:null,   /* 좌석 id | 'room-any' | 'table-any'. seatExtra = 합친 나머지 좌석 */
    name:"", phone:"", allergy:"", request:"", memo:"",
    done:null               /* 등록 완료 후 확인 메시지용 */
  };
  render();
}
async function closeWizard(){
  if(WZ && !WZ.done && (WZ.name || WZ.time)){
    if(!await uiConfirm2("입력 중인 예약이 있습니다. 닫을까요?")) return;
  }
  WZ = null; render(); histPop();
}
async function wzGo(n){
  wzSyncInputs();                       /* 먼저 입력값을 상태로 옮긴 뒤 */
  /* 두 단계 이상 앞으로 뛰면(단계 점) 한 단계씩 검사하며 갑니다 — 좌석·메뉴·알러지 확인을 건너뛰고 등록되던 것(점검 R2) */
  if(n > WZ.step + 1){
    while(WZ.step < n){ const was = WZ.step; await wzGo(was + 1); if(WZ.step !== was + 1) return; }
    return;
  }
  if(n > WZ.step && !wzCanNext()) return; /* 통과 여부를 검사 */
  /* 좌석 단계에서 종류만 고르고 넘어가면 '미정' 으로(재아) — 자리 없으면 확인창은 wzSeat 가 띄웁니다 */
  if(n === 4 && WZ.step === 3 && !WZ.seat && WZ.seatKind){ await wzSeat(WZ.seatKind === "room" ? "room-any" : "table-any"); if(!WZ.seat) return; if(WZ.step === 4) return; }
  /* 마지막 예약 가능 시각을 넘겼는지 확인 */
  if(n===2 && WZ.time){
    const reason = timeBlock(WZ.date, WZ.time);
    if(reason){
      const dh = hoursFor(WZ.date);
      const ok = await uiConfirm(reason,
        `${dateLabel(WZ.date)} ${hm(WZ.time)}\n` +
        (dh.closed ? "" : `영업 ${dh.open} ~ ${dh.close}${dh.bs?` · 브레이크 ${dh.bs} ~ ${dh.be}`:""}${dh.lo?` · 라스트오더 ${dh.lo}`:""}\n`) +
        `\n손님께 안내하신 뒤 진행하세요.`,
        {ok:"안내했습니다", cancel:"시간 다시 고르기"});
      if(!ok) return;
    }
  }
  /* 전화번호 없이 넘어가려 할 때 — 막지는 않되 한 번 되묻습니다.
     번호가 없으면 예약 확인 전화도, 늦으실 때 연락도 못 합니다.
     '해당 없음'을 손이 미끄러져 누른 경우를 여기서 잡아 줍니다. */
  if(n > 5 && WZ.step === 5 && WZ.phoneNone){
    const ok = await uiConfirm("전화번호 없이 접수합니다",
      `${WZ.name || "이 손님"}은 연락처가 없습니다.\n` +
      `예약 확인이나 변경 안내를 드릴 수 없고, 노쇼 이력도 남지 않습니다.\n\n` +
      `현장에서 직접 받으신 예약이라면 그대로 진행하세요.`,
      {ok:"이대로 접수", cancel:"번호 입력하기"});
    if(!ok) return;
  }
  WZ.step = Math.max(0, Math.min(LAST_STEP, n));
  WZ.maxStep = Math.max(WZ.maxStep || 0, WZ.step);
  render();
  /* 단계를 옮길 때만 맨 위로 */
  const mid = document.querySelector(".wz-mid");
  if(mid) mid.scrollTop = 0;
}
/* 고르는 순간 다음 단계로 — 단, 경고가 걸리면 이 화면에 멈춰서 빨갛게 보여 줍니다.
   (넘어가 버리면 경고를 아무도 못 봅니다. 확인 팝업이 이미 뜬 것도 여기서 한 번 더 걸립니다) */
function wzAutoNext(){
  if(WZ.step < LAST_STEP && wzCanNext() && !wzWarnReason()) wzGo(WZ.step + 1);
  else render();
}
/* 다음으로 넘어갈 수 있는지 검사 */
function wzCanNext(){
  if(WZ.step===0) return !!WZ.source;
  if(WZ.step===1) return !!(WZ.date && WZ.time);
  if(WZ.step===2) return WZ.people>0;
  if(WZ.step===3) return !!(WZ.seat || WZ.seatKind);
  if(WZ.step===4){
    if(!WZ.menuType) return false;
    /* 코스를 골라 놓고 구성을 비운 채 넘어가면 나중에 아무도 안 채웁니다.
       '코스 미정' 을 누르면 통과됩니다. */
    if(WZ.menuType==="코스" && !WZ.courseUndecided && courseCount()===0) return false;
    return true;
  }
  /* 한 글자라도 들어가면 됩니다 — 가명·이니셜·외국 이름도 받습니다 */
  if(WZ.step===5) return WZ.name.trim().length>0 &&
    (WZ.phoneNone || WZ.phone.trim().length>0);
  /* 알러지는 확인했다는 표시가 있어야 넘어갑니다 */
  if(WZ.step===6) return WZ.allergyNone || (WZ.allergy||"").trim().length>0;
  return true;
}
/* 화면을 다시 그리기 전에 입력창 값을 상태로 옮김.
   ※ 예전에는 입력창이 없을 때 g() 가 빈 문자열을 돌려주고, 그 빈 값을 그대로 WZ 에 넣었습니다.
      6단계(요청사항)에는 wz-name 이 없으므로 거기서 이 함수가 불릴 때마다 성함이 지워졌고,
      등록 버튼(wzSubmit)이 맨 먼저 이 함수를 부르는 탓에 매번 "성함을 입력하세요"가 떴습니다.
      이제 화면에 있는 입력창만 옮겨 담습니다. */
function wzSyncInputs(){
  const g=function(id){ const el=document.getElementById(id); return el?el.value:null; };
  const set=function(key,id){ const v=g(id); if(v!==null) WZ[key]=v; };
  set("name","wz-name");
  set("phone","wz-phone");
  set("allergy","wz-allergy");
  set("request","wz-request");
  set("memo","wz-memo");
  set("sourceDetail","wz-src-detail");
}

function renderWizard(){
  if(WZ.done) return wzDone();
  const bodies = [wzStepSource, wzStepDate, wzStepPeople, wzStepSeat, wzStepMenu, wzStepGuest, wzStepExtra];
  const dots = WZ_LABELS.map((l,i)=>
    `<button class="wz-dot ${i===WZ.step?'on':''} ${i<WZ.step?'past':''}" onclick="wzGo(${i})" ${i > (WZ.maxStep||0) + 1 ? "disabled" : ""}>
       <span class="n">${i+1}</span><span class="l">${l}</span></button>`).join("");
  const canNext = wzCanNext();
  const warn = wzWarnReason();
  const last = WZ.step===LAST_STEP;

  return `
  <div class="wz">
    <header class="wz-top">
      <button class="wz-back" onclick="closeWizard()">✕ 닫기</button>   <!-- '이전' 은 단계 점으로(재아). 입력이 있으면 닫을 때 확인창 -->
      <div class="wz-steps">${dots}</div>
      <div class="wz-sum">${wzSummary()}</div>
    </header>
    <div class="wz-mid">
      <div class="wz-q">
        <button class="wz-side prev ${WZ.step===0?'off':''}" onclick="wzGo(${WZ.step-1})" ${WZ.step===0?"disabled":""} aria-label="이전">‹ 이전</button>
        <h2>${WZ_STEPS[WZ.step]}</h2>
        <button class="wz-side next ${canNext?'':'off'}" onclick="${last?'wzSubmit()':`wzGo(${WZ.step+1})`}" ${canNext?"":"disabled"} aria-label="다음">${last?"등록":"다음"} ›</button>
        <div class="wz-warn" id="wz-warn">${
        String(warn||"").split("\n").map(l=>`<div>${esc(l)}</div>`).join("")}</div></div>
      <div class="wz-body">${bodies[WZ.step]()}</div>
    </div>
    <footer class="wz-foot">
      ${last?`<button class="btn ghost lg" onclick="wzSubmit()">바로 등록</button>`:""}
      <button id="wz-next" class="btn primary lg grow ${canNext?'':'off'} ${warn?'warned':''}"
        onclick="${last?'wzSubmit()':`wzGo(${WZ.step+1})`}" ${canNext?"":"disabled"}>
        ${last?"예약 등록":"다음"}
      </button>
    </footer>
  </div>`;
}
/* 이 날짜·시각에 예약을 잡으면 생기는 문제 (없으면 빈 문자열) */
/* 그 시각에 예약하면 생기는 문제를 **전부** 돌려줍니다.
   예전에는 첫 번째 하나만 돌려줘서, 라스트오더와 마감이 같이 걸려도 하나만 보였습니다.
   또 라스트오더는 '이미 넘김'만 알렸는데, 그보다 필요한 건
   "식사 중에 라스트오더가 다가온다"는 사전 안내입니다. */
function timeWarns(date, time){
  const dh = hoursFor(date), out = [];
  if(dh.closed) return [`휴무일${dh.note?` - ${dh.note}`:""}`];
  if(inBreak(date, time)) return ["브레이크입니다"];
  if(toMin(time) < toMin(dh.open) || toMin(time) >= toMin(dh.close)) return ["영업시간 아님"];

  const stx = store().settings;
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
  }
  if(dh.bs && t < toMin(dh.bs)){
    if((stx.breakMode||"leave")==="leave"){
      if(end > toMin(dh.bs)) out.push(`식사 중 브레이크가 시작됩니다 - 식사시간 ${hmDur(toMin(dh.bs) - t)}`);
    }else{
      const buf = stx.breakEntryBuffer != null ? stx.breakEntryBuffer : 60;
      if(t > toMin(dh.bs) - buf) out.push(`브레이크 임박 - ${buf}분 전 이후 입장`);
    }
  }
  if(end > toMin(dh.close)) out.push(`마감 임박 - 식사시간 ${hmDur(toMin(dh.close) - t)}`);
  return out;
}
/* 분 → "1시간 05분" 꼴. 한 시간이 안 돼도 "0시간 40분" 으로 자리를 맞춥니다 (문구 길이가 흔들리지 않게) */
function hmDur(m){
  m = Math.max(0, m);
  return `${Math.floor(m/60)}시간 ${pad(m%60)}분`;
}
function timeWarn(date, time){ return timeWarns(date, time).join("\n"); }
/* 확인 팝업을 띄울 만큼 심각한 것만.
   '라스트오더 임박' 은 저녁 예약이면 거의 매번 걸리므로 화면 표시로만 두고
   여기서는 뺍니다 — 팝업이 자주 뜨면 안 읽고 누르게 됩니다 (설계 5.2 주의). */
function timeBlock(date, time){
  return timeWarns(date, time).filter(function(x){ return x.indexOf("라스트오더 임박") < 0; }).join("\n");   /* 임박은 알림만, 확인창은 안 띄움 */
}
/* 시간 칸에 붙는 짧은 말. 여러 개가 걸리면 가장 중한 것 하나만 */
function shortWarn(msg){
  if(msg.indexOf("휴무") >= 0) return "휴무";
  if(msg.indexOf("영업시간") >= 0) return "영업 외";
  if(msg.indexOf("지난 날짜") >= 0) return "확인";
  if(msg.indexOf("브레이크입니다") >= 0) return "브레이크";
  if(msg.indexOf("접수 마감") >= 0) return "접수 마감";
  if(msg.indexOf("라스트오더 이후") >= 0) return "라스트오더 지남";
  if(msg.indexOf("마감") >= 0) return "마감 넘김";
  if(msg.indexOf("라스트오더") >= 0) return "라스트오더 임박";
  if(msg.indexOf("브레이크") >= 0) return "브레이크 임박";
  return "확인";
}

/* 지금 단계에서 걸리는 문제 — 있으면 '다음' 버튼이 빨갛게 바뀝니다 */
/* 걸리는 것을 **전부** 돌려줍니다. 여러 개면 줄바꿈으로 이어 붙습니다 —
   예전에는 첫 번째 하나만 보여서, 겹침과 최소 인원이 같이 걸려도 하나만 알려줬습니다. */
function wzWarnReason(){
  const st = store().settings;
  const out = [];
  if(WZ.step===1 && WZ.date){
    const dh = hoursFor(WZ.date);
    if(WZ.date < todayStr()) out.push("지난 날짜");
    if(WZ.time) out.push.apply(out, timeWarns(WZ.date, WZ.time));
    else if(dh.closed) out.push(`휴무일${dh.note?` - ${dh.note}`:""}`);
  }
  if(WZ.step===3 && WZ.seat){
    const room = st.rooms.find(x=>x.id===WZ.seat);
    if(room && room.type==="room"){
      const rs = roomStatus(WZ.date, WZ.time, WZ.seat);
      const who = rs.hits.map(x=>`${hm(x.time)} ${x.name} ${pplText(x)}`).join(", ");
      if(rs.state==="blocked") out.push(`${hmDur(store().settings.closeGapMin != null ? store().settings.closeGapMin : 60)} 안에 다른 예약${who?` - ${who}`:""}`);
      else if(rs.state==="warn") out.push(`식사 시간이 겹침${who?` - ${who}`:""}`);
      const cnt = seatCountsInfants() ? WZ.people : adultCount(WZ.people, WZ.infants);
      if(cnt > room.capacity) out.push(`정원 초과 - ${seatLabel(room.id)} 최대 ${room.capacity}명`);
      if(cnt < roomMin(room, WZ.date)) out.push(`최소 인원 미달 - ${seatLabel(room.id)} ${roomMin(room, WZ.date)}명부터`);
      const bk = blockedAt(room, WZ.date, WZ.time);
      if(bk) out.push(`사용 중지 - ${seatLabel(room.id)}${bk.note?` · ${bk.note}`:""}`);
    }
    /* 테이블(층): 같은 시간대 손님 수가 자리 수를 넘으면 — 막지 않고 이 화면에 빨갛게 */
    const fl = prefFloor(WZ.seat);
    if(fl != null && WZ.time){
      const fit = floorFit(fl, WZ.date, WZ.time, WZ.people||0);
      if(fit.state === "none") out.push(`테이블 자리 없음 - ${floorLabel(fl)} 한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명 (지금 ${WZ.people}명)`);
      else if(fit.state === "split") out.push(`나눠 앉음 - ${floorLabel(fl)}에 붙일 테이블이 없어 옆 테이블에 나눠 앉습니다`);
    }
  }
  if(WZ.step===2 && WZ.people && (WZ.infants||0) >= WZ.people) out.push(`성인이 없음 - 유아만 ${WZ.infants}명`);
  if(WZ.step===5){
    if(WZ.phoneNone) out.push("전화번호 없음");
    else if(WZ.phone && WZ.phone.replace(/\D/g,"").length < 9)
      out.push("전화번호가 짧음");
    const ns = WZ.phone ? noshowOf(WZ.phone) : null;
    if(ns) out.push(`노쇼 이력 - ${ns.count}회`);
  }
  if(WZ.step===4){
    const seat = st.rooms.find(x=>x.id===WZ.seat);
    if(seat && seat.type==="room"){
      const adults = adultCount(WZ.people, WZ.infants);
      const n = courseCount();
      if(WZ.menuType==="해당 없음") out.push("룸인데 코스가 아님");
      if(WZ.menuType==="확인 필요") out.push("룸인데 코스 여부 미확인");
      if(WZ.menuType==="코스" && !WZ.courseUndecided && n>0 && n<adults)
        out.push(`코스 부족 - ${n}인분 / 성인 ${adults}명`);
      if(WZ.menuType==="코스" && !WZ.courseUndecided && n>adults)
        out.push(`코스 초과 - ${n}인분 / 성인 ${adults}명`);
    }
    out.push.apply(out, courseWarns());
  }
  if(WZ.step===6){
    if((WZ.chairs||0) > (WZ.infants||0)) out.push(`의자가 유아보다 많음 - 의자 ${WZ.chairs||0} / 유아 ${WZ.infants||0}`);
    if((WZ.chairs||0) < (WZ.infants||0)) out.push(`의자가 유아보다 적음 - 의자 ${WZ.chairs||0} / 유아 ${WZ.infants||0}`);
  }
  return out.join("\n");
}

/* 상단에 지금까지 고른 값 요약 */
function wzSummary(){
  const p=[];
  if(WZ.source) p.push(WZ.source==="기타" && WZ.sourceDetail ? WZ.sourceDetail : WZ.source);
  if(WZ.date && WZ.time) p.push(`${(+WZ.date.slice(5,7))}/${(+WZ.date.slice(8))} ${hm(WZ.time)}`);
  if(WZ.people) p.push(`${WZ.people}명${WZ.infants?`(유아${WZ.infants})`:""}`);
  if(WZ.seat) p.push(WZ.seatExtra && WZ.seatExtra.length ? seatLabelIds([WZ.seat].concat(WZ.seatExtra)) : seatLabel(WZ.seat));
  return p.map(x=>`<span>${esc(x)}</span>`).join("");
}
function hm(t){
  /* 8차-Y(재아): 시각 칸과 같은 모양 '오후 5:30'. '5시 30분' 은 길고 칸마다 폭이 달랐습니다 */
  const [h,m]=t.split(":").map(Number);
  const ap = h<12?"오전":"오후";
  const h12 = h%12===0?12:h%12;
  return `${ap} ${h12}:${pad(m||0)}`;
}
function seatLabel(seat){
  const st = store().settings;
  if(seat==="any") return "좌석 상관없음";
  if(seat==="hall-any" || seat==="table-any") return "테이블 (층 상관없음)";
  if(/^table:/.test(seat||"")) return floorLabel(seat.slice(6));
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
function resSeatLabel(r){
  if(r.roomId) return seatLabelIds([r.roomId].concat(r.extraIds||[]));
  if(isTablePref(r.seatPref)) return seatLabel(r.seatPref) + tableHint(r);   /* 테이블 예약은 층까지만 — 미배정이 아닙니다 */
  return "미배정";
}
/* 4명을 넘는 테이블 예약만 숨은 배정(붙일 테이블)을 작게 덧붙입니다(재아) — 큰 팀은 어느 테이블을 붙일지 미리 알아야 준비가 됩니다.
   4명 이하는 그날 남는 자리에 앉히므로 안 보여 줍니다 */
function tableHint(r){
  if(!isTablePref(r.seatPref) || pplOf(r) <= 4 || !r.tentativeRoomId) return "";
  const names = seatsOf(r).map(id=>{ const x = seatById(id); return x ? x.name : ""; }).filter(Boolean);
  return names.length ? ` (${names.join("+")}${r.tentativeSplit ? " 나눠" : ""})` : "";
}
/* 확인 시트·검색·상세에 쓰는 좌석 꼬리표(8차-AB 재아) — 잠정도 '배정된 것' 이라 붉게 쓰지 않습니다. 붉은색은 자리가 정말 없을 때만.
   확정 룸/테이블 → 'pine', 잠정 → 색 없음 '장비 룸(잠정)' / '1층 테이블 · 21(잠정)', 자리 없음 → 'rust' */
function seatTag(r){
  var t = seatTagText(r);
  return '<span class="tag ' + (r.roomId ? "pine" : (t.ok ? "" : "rust")) + '">' + esc(t.text) + '</span>';
}
function seatTagText(r){
  if(r.roomId) return { ok:true, text:resSeatLabel(r) };
  var live = holdsSeat(r);   /* 취소·노쇼는 자리를 안 잡으니 '자리 없음' 이라고 붉게 쓰지 않습니다 */
  var names = r.tentativeRoomId ? seatsOf(r).map(function(id){ var x = seatById(id); return x ? x.name : ""; }).filter(Boolean) : [];
  if(isTablePref(r.seatPref)){
    var fl = prefFloor(r.seatPref), head = fl ? floorLabel(fl) : "테이블 (층 상관없음)";
    return names.length ? { ok:true, text: head + " · " + names.join("+") + (r.tentativeSplit ? " 나눠" : "") + "(잠정)" } : { ok:!live, text: live ? head + " · 자리 없음" : head };
  }
  return names.length ? { ok:true, text: seatLabelIds([r.tentativeRoomId].concat(r.tentativeExtra||[])) + "(잠정)" } : { ok:!live, text:"미배정" };
}
/* 룸 미배정(잠정 포함) 여부 — 테이블 예약은 층이 자리이므로 미배정으로 세지 않습니다 */
function isUnassigned(r){ return !r.roomId && !isTablePref(r.seatPref); }
/* 목록·시트에 쓰는 좌석 표시 한 줄 — 확정 좌석 / 테이블(층) / 룸 미정이면 '잠정 룸(잠정)' / 없으면 미배정 */
function seatText(r){
  if(r.roomId) return resSeatLabel(r);
  if(isTablePref(r.seatPref)) return resSeatLabel(r);
  return r.tentativeRoomId ? resTentLabel(r) + "(잠정)" : "미배정";
}
function resTentLabel(r){
  if(isTablePref(r.seatPref)) return "";   /* 테이블 예약의 숨은 배정은 이름을 보여 주지 않습니다 — 층까지만 */
  return r.tentativeRoomId ? seatLabelIds([r.tentativeRoomId].concat(r.tentativeExtra||[])) : "";
}

/* ---------- 0단계: 예약 경로 ---------- */
function wzStepSource(){
  /* 경로는 설정(sources)에서 — 예전엔 셋만 박혀 있어 '방문' 이 빠져 있었습니다(누락 수정). '기타' 는 항상 마지막 */
  const srcs = (store().settings.sources || ["전화 예약","네이버 예약","방문","기타"]).slice();
  if(srcs.indexOf("기타") < 0) srcs.push("기타");
  const isNaver = /네이버/.test(WZ.source || "");
  /* 두 열이 기본. 다섯 개부터는 두 줄에 3/2, 3/3, 4/3, 4/4 … (열 수 = 올림(개수/2)) */
  const cols = srcs.length <= 4 ? 2 : Math.ceil(srcs.length / 2);
  return `
    <div class="srcgrid" style="grid-template-columns:repeat(${cols},1fr)">
      ${srcs.map(v=>`
        <button class="srccell ${WZ.source===v?'on':''}" onclick="wzSource('${jsq(v)}')">
          <span class="s-l">${esc(v)}</span>
        </button>`).join("")}
    </div>
    <!-- 네이버를 고르면 나타나는 갈래 — 자리를 미리 잡아 두고 보이기만 바꿉니다(버튼 위치가 튀지 않게) -->
    <div class="naver-how" style="visibility:${isNaver?'visible':'hidden'}">
      <div class="lbl" style="margin-top:14px">네이버 예약은 어떻게 넣을까요?</div>
      <div class="sgrid any two">
        <button class="scell" onclick="wzAutoNext()"><span class="sn">직접 등록</span></button>
        <button class="scell" onclick="WZ=null; openNaver()"><span class="sn">Excel 등록</span></button>
      </div>
    </div>
    <label class="f big src-detail ${WZ.source==="기타"?"":"hold"}"><div class="lb">경로</div>
        <input id="wz-src-detail" value="${esc(WZ.sourceDetail)}" placeholder="예: 지인 소개, 대면 예약" ${WZ.source==="기타"?"autofocus":"tabindex=\"-1\""}>
        <div class="f-note">예약 내역에 참고로만 남습니다</div>
      </label>
    <button class="linkbtn wz-quick" onclick="openQuick()">한 화면으로 입력</button>`;
}
/* 빠른 입력 — 새 화면을 만들지 않고 이미 있는 수정 시트(sheetRes)를 빈 예약으로 엽니다 (새 코드가 적어야 오류도 적습니다).
   마법사 1단계 아래 '한 화면으로 입력' 에서만 들어옵니다. 날짜는 마법사가 열려 있던 날짜(= 보고 있던 날짜) */
function openQuick(){
  const d = (WZ && WZ.date) || view.date;
  WZ = null; tmpRes = null;
  view.form = {type:"res", date:d, page:true};   /* 화면형(재아) */
  render(); window.scrollTo(0,0);
}
function wzSource(v){
  const el = document.getElementById("wz-src-detail");
  if(el) WZ.sourceDetail = el.value;
  WZ.source = v;
  if(/네이버/.test(v) && !(WZ.memo||"").trim()) WZ.memo = "네이버 예약번호: ";   /* 직접 등록 때 메모 양식(재아) — 번호를 적어 두면 나중에 엑셀 가져오기가 같은 건으로 잇습니다 */
  /* 전화·방문은 더 물을 것이 없으니 바로 넘어갑니다. 기타는 경로를 적어야 하고, 네이버는 직접/Excel 을 고르므로 이 화면에 머뭅니다 */
  if(v !== "기타" && !/네이버/.test(v)){ wzAutoNext(); return; }
  render();
}

/* ---------- 1단계: 날짜 + 시간 ---------- */
/* 8차-U(재아): 시각 선택 — 그날 세션(점심/저녁)마다 '접수 가능한 시각' 만 큼직하게. 칸에는 이 인원이 앉을 빈 룸 수·테이블 가능 여부.
   영업 밖·브레이크·접수 마감 뒤 시각은 아래 '접수 시간 밖' 에 접어 둡니다(경고 붙여서 받을 수는 있음) */
function sessionGrid(){ return timeGrid({date:WZ.date, people:WZ.people||0, time:WZ.time, pick:"wzPickSlot"}); }
function timeGrid(ctx){
  const s = store(), st = s.settings, dh = hoursFor(ctx.date);
  if(dh.closed) return `<div class="empty">휴무일입니다. 아래 '접수 시간 밖' 에서 그래도 받을 수 있습니다.</div>`;
  const ss = sessionsFor(ctx.date); if(!ss.length) return "";
  const isToday = ctx.date===todayStr(), isPastDate = ctx.date < todayStr(), nowM = toMin(nowHM());
  const curT = ctx.time ? toMin(ctx.time) : null, curSlot = curT===null ? null : Math.floor(curT/30)*30;
  const people = ctx.people || 0;
  const rooms = st.rooms.filter(isRoom);
  return ss.map(se=>{
    const from = toMin(se.from), last = toMin(se.lastBook);
    const cells = [];
    /* 다음 세션이 있으면 그 시작(경계) 시각은 다음 세션 칸에만 — 15:30 이 점심·저녁에 둘 다 나와 같이 켜지던 것(재아) */
    const cut = ss.indexOf(se) + 1 < ss.length ? toMin(se.until) : null;
    for(let t = from; t <= last; t += 30){
      if(cut != null && t >= cut) break;
      if(dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be)) continue;
      const hmS = minToHM(t);
      const gone = isPastDate || (isToday && t+30 <= nowM);
      const freeRooms = rooms.filter(x=>!blockedAt(x, ctx.date, hmS) && (!people || (people >= roomMin(x, ctx.date) && people <= seatMax(x))) && roomStatus(ctx.date, hmS, x.id).state === "free").length;
      const tf = people ? floorFit(null, ctx.date, hmS, people) : null;
      const tTxt = !people ? "" : tf.state==="ok" ? "테이블 가능" : tf.state==="split" ? "테이블 나눠" : "테이블 없음";
      const cnt = s.reservations.filter(r=>r.date===ctx.date && holdsSeat(r) && Math.floor(toMin(r.time)/30)*30===t).length;
      const bad = (people && freeRooms===0 && (!tf || tf.state==="none"));
      cells.push(`<button class="hcell big ${curSlot===t?'on':''} ${gone?'gone':''} ${bad?'busy':''}" onclick="${ctx.pick}(${t})">
        <span class="hh">${hm(hmS).replace(/^(오전|오후) /,"")}</span><span class="ap">${t<720?"오전":"오후"}</span>
        <span class="hn">${people?`룸 ${freeRooms} · ${tTxt}`:"&nbsp;"}</span>
      </button>`);
    }
    /* 접수 마감이 30분 단위가 아니면(예 19:50) 그 마지막 시각 칸을 하나 더 — 전화로 "몇 시까지 되나요" 에 바로 답하게(재아) */
    if(last % 30 !== 0 && !(cut != null && last >= cut)){
      const hmL = minToHM(last), goneL = isPastDate || (isToday && last <= nowM);
      cells.push(`<button class="hcell big last ${curT===last?'on':''} ${goneL?'gone':''}" onclick="${ctx.pick}(${last})">
        <span class="hh">${hm(hmL).replace(/^(오전|오후) /,"")}</span><span class="ap">마지막</span><span class="hn">접수 마감 시각</span></button>`);
    }
    return `<div class="sess-h2"><b>${esc(se.name)}</b><span class="lbl-note">${se.from}부터 · 접수 ${se.lastBook}까지 · ${stayLabel(se)}</span></div><div class="hgrid sess">${cells.join("")}</div>`;
  }).join("");
}
function wzStepDate(){
  const s = store(), st = s.settings;
  const [y,m] = WZ.calMonth.split("-").map(Number);
  const first = new Date(y, m-1, 1), lastDay = new Date(y, m, 0).getDate();
  const lead = first.getDay();
  const today = todayStr();

  let cells = "";
  /* 달력은 항상 6줄(42칸)로 그립니다.
     5주짜리 달과 6주짜리 달이 번갈아 나오면 아래 시각 칸이 한 줄씩 오르내립니다.
     빈 칸이 한 줄 생기는 것이 화면이 들썩이는 것보다 낫습니다. */
  for(let i=0;i<lead;i++) cells += `<span class="bday"></span>`;
  for(let d=1; d<=lastDay; d++){
    const ds = `${y}-${pad(m)}-${pad(d)}`;
    const list = s.reservations.filter(r=>r.date===ds && r.status==="확정");
    const dow = new Date(ds+"T00:00:00").getDay();
    const cls = ["bday","btn-day", WZ.date===ds?"sel":"", ds===today?"today":"",
                 ds<today?"past":"", dow===0?"sun":dow===6?"sat":"", hoursFor(ds).closed?"closed":""].join(" ");
    const rt = list.length ? dayStat(ds).rate : 0;
    cells += `<button class="${cls}" onclick="wzPickDate('${ds}')">
        <span class="d">${d}</span>
        ${list.length?`<span class="b">${list.length}건</span><span class="obar"><i style="width:${rt}%" class="${rt>=70?'hi':rt>=40?'mid':''}"></i></span>`:""}
      </button>`;
  }
  for(let i=lead+lastDay; i<42; i++) cells += `<span class="bday"></span>`;

  /* 영업시간 안에서 30분 단위 시각 후보 생성 (11:00, 11:30, … 마감 전까지).
     1시간 칸이면 7:00 과 7:30 의 사정(라스트오더·브레이크)이 한 칸에 섞여 어느 쪽이 안 되는지 안 보였습니다 */
  const dh = WZ.date ? hoursFor(WZ.date) : {closed:false, open:"", close:"", bs:"", be:"", lo:""};
  /* 칸 수는 '이번 주 중 가장 이른 개점 ~ 가장 늦은 마감' 으로 고정합니다.
     일요일(20:30 마감)을 누르면 칸이 세 개 줄어 아래가 올라오던 것이 원인이었습니다.
     오늘 영업시간 밖인 칸은 그대로 두고 '영업 전 / 영업 종료' 로 흐리게만 표시합니다. */
  const range = weekHourRange(WZ.date || todayStr());
  const slots = [];
  for(let t = range.open; t < range.close; t += 30) slots.push(t);
  const todayOpen = dh.closed ? null : toMin(dh.open), todayClose = dh.closed ? null : toMin(dh.close);
  const curT = WZ.time ? toMin(WZ.time) : null;
  const curSlot = curT===null ? null : Math.floor(curT/30)*30;   /* 고른 시각이 속한 30분 칸 */
  const base = curSlot===null ? 0 : curSlot%60;                  /* 분 레일의 시작(0 또는 30) */
  const off = curT===null ? 0 : curT - curSlot;                  /* 칸 안에서의 분 (0~25) */

  const isToday = WZ.date===todayStr();
  const isPastDate = WZ.date < todayStr();
  const nowM = toMin(nowHM());
  /* 세션 칸에 이미 있는 시각은 여기서 뺍니다 — '접수 시간 밖' 은 나머지만 */
  const inSess = {}; (WZ.date ? sessionsFor(WZ.date) : []).forEach(se=>{ for(let t = toMin(se.from); t <= toMin(se.lastBook); t += 30) inSess[t] = 1; });
  const slotCells = !WZ.date ? "" : slots.filter(t=>!inSess[t] || (dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be))).map(t=>{
    const h = Math.floor(t/60), m = t%60;
    const n = 0;
    /* 이 칸을 고르면 경고가 생기는지 미리 확인합니다 */
    const probe = timeWarn(WZ.date, minToHM(t));
    /* 지난 시각도 누를 수는 있게 — 예약 누락을 나중에 입력하는 경우가 있습니다 */
    const gone = isPastDate || (isToday && t+30 <= nowM);
    /* 오늘(고른 날) 영업시간 밖 — 칸은 자리를 지키되 누를 수 없게 */
    const outside = dh.closed || t < todayOpen || t >= todayClose;
    /* 브레이크타임에 걸리는 칸은 따로 표시 */
    const brk = dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be);
    const bad = !!probe;
    /* 경고가 걸리는 시각은 작은 표시만이 아니라 시각 글자까지 벽돌색 — 눈이 먼저 가야 하는 칸입니다 */
    const red = (bad || brk) ? " rust" : "";
    return `<button class="hcell ${curSlot===t?'on':''} ${bad?'late warned':''} ${gone?'gone':''} ${brk?'brk':''} ${outside?'outside':''}" ${outside?'disabled':`onclick="wzPickSlot(${t})"`}>
      <span class="ap${red}">${h<12?"오전":"오후"}</span>
      <span class="hh${red}">${h%12===0?12:h%12}:${pad(m)}</span>
      ${outside?`<span class="hn muted2">${dh.closed?"휴무":(t<todayOpen?"영업 전":"영업 종료")}</span>`
           :brk?`<span class="hn rust">브레이크</span>`
           :bad?`<span class="hn rust">${esc(shortWarn(probe))}</span>`
           :`<span class="hn">&nbsp;</span>`}
    </button>`;
  }).join("");
  /* (날짜가 없으면 slotCells 는 빈 문자열) */

  /* 분 조절은 고른 30분 칸 안에서만 움직입니다 — 정각 칸이면 00~25, 30분 칸이면 30~55.
     시각을 고르기 전에도 자리를 지킵니다(.idle) — 누르는 순간 레일이 생기며 화면이 내려앉지 않게 */
  const pct = v => (v/25)*100;
  const minuteRail = store().settings.minuteSteps === false ? "" : `
    <div class="mwrap ${curSlot===null?'idle':''}">
      <div class="mhead"><span class="lbl">분</span><span class="mnow">${curSlot===null?"시각을 먼저 고르세요":hm(WZ.time)}</span></div>
      <div class="mrail" id="mrail">
        <div class="mtrack"></div>
        <div class="mfill" style="width:${pct(off)}%"></div>
        ${[0,5,10,15,20,25].map(v=>
          `<span class="mnotch ${v%10===0?'big':''}" style="left:${pct(v)}%"></span>`).join("")}
        <div class="mknob" style="left:${pct(off)}%">${pad(base+off)}</div>
        ${[0,5,10,15,20,25].map(v=>
          `<button class="mtick ${off===v?'on':''}" style="left:${pct(v)}%" onclick="wzPickMin(${v})">${pad(base+v)}</button>`).join("")}
      </div>
      <div class="mfine">
        <button ${off<=0?"disabled":""} onclick="wzNudge(-5)">− 5분</button>
        <button ${off>=25?"disabled":""} onclick="wzNudge(5)">＋ 5분</button>
      </div>
    </div>`;

  return `
    <div class="wz-step1">
    <div class="wz-cal">
      <div class="mo-h">
        <button class="nav" onclick="wzMonth(-1)" aria-label="이전 달">◀</button>
        <div class="mo">${y}년 ${m}월</div>
        <button class="nav" onclick="wzMonth(1)" aria-label="다음 달">▶</button>
      </div>
      <div class="bgrid bhead">${["일","월","화","수","목","금","토"].map((x,i)=>`<span class="${i===0?'sun':i===6?'sat':''}">${x}</span>`).join("")}</div>
      <div class="bgrid">${cells}</div>
    </div>
    <div class="wz-time">
      ${WZ.date ? hoursLineHtml(dh) : `<div class="hours-line"><span class="hl-c"><i>영업시간</i>—</span><span class="hl-c"><i>브레이크</i>—</span><span class="hl-c"><i>라스트오더</i>—</span></div>`}
      <div class="lbl" style="margin-bottom:8px">${WZ.date?dateLabel(WZ.date):"날짜를 먼저 고르세요"} · 시각</div>
      ${WZ.date ? sessionGrid() : `<div class="empty">왼쪽 달력에서 날짜를 고르면 시각이 나옵니다.</div>`}
      <details class="hmore" ${WZ.showAllSlots?"open":""} ontoggle="WZ.showAllSlots=this.open"><summary>접수 시간 밖 시각 보기 <span class="lbl-note">영업 전·브레이크·접수 마감 뒤 — 경고가 붙습니다</span></summary>
      <div class="hgrid">${slotCells}</div></details>
      ${minuteRail}
    </div>
    </div>`;
}
/* 그 날짜가 속한 주(일~토) 7일의 영업시간을 모아 가장 이른 개점·가장 늦은 마감을 돌려줍니다.
   시각 칸 수를 요일에 따라 바뀌지 않게 고정하는 데 씁니다. 휴무일은 건너뜁니다. */
function weekHourRange(dateStr){
  var d0 = new Date(dateStr + "T00:00:00");
  d0.setDate(d0.getDate() - d0.getDay());
  var open = 24*60, close = 0, i;
  for(i=0;i<7;i++){
    var d = new Date(d0); d.setDate(d0.getDate()+i);
    var h = hoursFor(todayStr(d));
    if(h.closed) continue;
    open = Math.min(open, Math.floor(toMin(h.open)/30)*30);
    close = Math.max(close, Math.ceil(toMin(h.close)/30)*30);
  }
  if(open >= close){ open = 11*60; close = 22*60; }   /* 전부 휴무인 주 — 기본 범위 */
  return { open:open, close:close };
}
function wzPickDate(d){ WZ.date=d; render(); }
function wzMonth(n){
  const [y,m]=WZ.calMonth.split("-").map(Number);
  const d=new Date(y,m-1+n,1);
  WZ.calMonth = d.getFullYear()+"-"+pad(d.getMonth()+1);
  render();
}
/* 30분 칸을 고르면 그 칸의 시작 시각(정각 또는 30분)이 됩니다. 세부 분은 아래 레일에서 */
function wzPickSlot(t){ WZ.time = minToHM(t); render(); }   /* 마지막 접수 칸(19:50)처럼 30분 단위가 아닌 값도 그대로 — 분 레일이 자동으로 +20 위치 */
/* 레일의 분(0~25)을 칸 시작에 더한 시각 */
function wzSlotBase(){ return WZ.time ? Math.floor(toMin(WZ.time)/30)*30 : 18*60; }
function wzPickMin(v){
  WZ.time = minToHM(wzSlotBase() + Math.min(25, Math.max(0, v))); render();
}
function wzNudge(d){
  if(!WZ.time) return;
  const base = wzSlotBase(), off = toMin(WZ.time) - base;
  /* 칸 안(0~25분)에서만 — 칸을 바꾸는 것은 위 타일에서 */
  const next = Math.min(25, Math.max(0, off + d));
  if(next===off) return;
  WZ.time = minToHM(base + next); render();
}
/* 분 레일을 손가락으로 끌어서 조절 */
function wzRefreshNext(){
  const b = document.getElementById("wz-next");
  if(!b) return;
  const ok = wzCanNext();
  b.disabled = !ok;
  b.classList.toggle("off", !ok);
  /* 경고 문구도 함께 갱신 */
  const warn = wzWarnReason();
  b.classList.toggle("warned", !!warn);
  const bar = document.getElementById("wz-warn");
  if(bar){ bar.innerHTML = String(warn||"").split("\n").map(l=>`<div>${esc(l)}</div>`).join(""); }
}
/* 창 크기나 브라우저 배율이 바뀌면 칸 높이도 바뀝니다.
   글자 크기는 CSS 가 알아서 따라가지만, '몇 줄까지 보일지'는 자바스크립트가 정하므로
   여기서 다시 계산해 줍니다. 연달아 들어오는 resize 는 마지막 것만 처리합니다. */
var fitTimer = null;
window.onresize = function(){
  if(fitTimer) clearTimeout(fitTimer);
  fitTimer = setTimeout(function(){ fitTimer = null; if(view.display) fitDisplay(); }, 180);
};
/* 폰 압축 그래프는 11시간을 가로로 늘려 스크롤합니다 — 그린 직후 현재 시각 1시간 전이 왼쪽에 오게 */
function scrollTlToNow(){
  var sc = document.querySelector(".tl-scroll.compact"); if(!sc) return;
  var track = sc.querySelector(".tl-track"); if(!track) return;
  var line = sc.querySelector(".nowline"); if(!line || /edge/.test(line.className)) return;
  var x = line.offsetLeft - track.clientWidth / 11;   /* 한 시간 폭만큼 앞에 */
  sc.scrollLeft = Math.max(0, track.offsetLeft + x - 88);
}
/* 현재 시각 선을 표 전체 높이로 늘립니다 — 축 줄 안에 있으므로 표 높이에서 축 줄 위치를 뺀 만큼 */
function fitNowLine(){
  var tl = document.querySelector(".tl"), ln = tl && tl.querySelector(".tl-row.axis .nowline");
  if(!ln) return;
  var track = ln.parentNode, sc = tl.parentNode;   /* .tl-scroll 이 position:relative 라 offsetTop 은 그 기준 */
  ln.style.height = Math.max(0, sc.scrollHeight - track.offsetTop) + "px"; ln.style.bottom = "auto";
}
function afterRender(){
  view.foldJust = null;   /* 다음 render 부터는 애니메이션 없이 */
  fitNowLine();
  scrollTlToNow();
  restoreScroll();   /* 다시 그리기 전 스크롤 위치로 되돌립니다 */
  fitDisplay();   /* 디스플레이 모드 글자 크기를 화면에 맞게 키움 */
  /* 타임라인은 좁은 화면에서 가로로 스크롤됩니다 — 현재 시각이 보이도록 맞춰 둡니다 */
  const tls = document.getElementById("tl-scroll");
  if(tls && tls.scrollWidth > tls.clientWidth){
    const line = tls.querySelector(".nowline");
    if(line){
      const x = line.offsetLeft - tls.clientWidth*0.35;
      tls.scrollLeft = Math.max(0, x);
    }
  }
  /* 예약자 이름·전화는 글자를 칠 때마다 상태에 반영해서 '다음' 버튼을 바로 켬 */
  /* 성함·전화 어느 쪽을 먼저 쳐도 '다음' 상태가 바로 갱신되게 합니다.
     자동 포커스는 아직 아무것도 입력하지 않았을 때만 겁니다. */
  const nameEl = document.getElementById("wz-name");
  const phoneEl = document.getElementById("wz-phone");
  if(nameEl){
    nameEl.oninput = ()=>{ WZ.name = nameEl.value; wzRefreshNext(); };
    if(!nameEl.value && !(WZ && WZ.phone)) setTimeout(()=>{
      if(document.activeElement === document.body) nameEl.focus();
    }, 60);
  }
  if(phoneEl){
    phoneEl.oninput = (ev)=>{ fmtPhone(phoneEl, ev); wzRefreshNext(); };
  }

  const rail = document.getElementById("mrail");
  if(!rail) return;
  const set = (e)=>{
    const r = rail.getBoundingClientRect();
    const x = Math.min(Math.max(e.clientX - r.left, 0), r.width);
    const v = Math.min(25, Math.max(0, Math.round((x/r.width)*25/5)*5));   /* 5분 단위, 칸 안 0~25분 */
    const nt = minToHM(wzSlotBase() + v);
    if(nt!==WZ.time){ WZ.time = nt; render(); }
  };
  rail.addEventListener("pointerdown", e=>{
    if(e.target.tagName==="BUTTON") return;   /* 눈금 버튼은 따로 처리 */
    rail.setPointerCapture(e.pointerId); set(e);
    const mv = ev=>set(ev);
    const up = ()=>{ rail.removeEventListener("pointermove",mv); rail.removeEventListener("pointerup",up); };
    rail.addEventListener("pointermove",mv); rail.addEventListener("pointerup",up);
  });
}

/* ---------- 2단계: 인원 (유아 포함 총원) ---------- */
function wzStepPeople(){
  const tiles = [1,2,3,4,5,6].map(n=>
    `<button class="ptile ${WZ.people===n&&!WZ.customPeople?'on':''} ${n===1?'off':''}" onclick="wzPeople(${n})">
      <span class="pn">${n}</span><span class="pu">명</span></button>`).join("");
  const cur = WZ.people||0;
  return `
    <div class="pgrid">${tiles}</div>
    <button class="pmore ${WZ.customPeople?'on':''}" onclick="wzCustom()">7명 이상</button>
      <div class="bigstep ${WZ.customPeople?'':'hold'}">
        <button onclick="wzAdj('people',-1)" ${WZ.customPeople?'':'tabindex="-1"'}>−</button>
        <div class="v"><span>${WZ.people||7}</span><small>명</small></div>
        <button onclick="wzAdj('people',1)" ${WZ.customPeople?'':'tabindex="-1"'}>＋</button>
      </div>
    <div class="infant ${WZ.infants>=(WZ.people||99)&&WZ.people?'bad':''}">
      <div><div class="t">유아</div>
        <div class="s">${WZ.infants>=(WZ.people||99)&&WZ.people
          ? "성인이 없습니다"
          : "총 인원에 포함"}</div></div>
      <div class="bigstep sm">
        <button onclick="wzAdj('infants',-1)">−</button>
        <div class="v"><span>${WZ.infants}</span><small>명</small></div>
        <button onclick="wzAdj('infants',1)">＋</button>
      </div>
    </div>
    <div class="ptotal">${cur ? `총 <b>${cur}명</b>${WZ.infants?` (유아 ${WZ.infants}명 포함)`:""}` : ""}</div>`;
}
function wzPeople(n){
  /* 1명 예약은 받지 않습니다(재아: 타일은 보이되 누르면 안내). 1인 규칙은 누님 질문 2번 대기 */
  if(n === 1) return uiAlert("1명 예약은 받지 않습니다", "2명부터 예약할 수 있습니다.", "warn");
  WZ.people=n; WZ.customPeople=false;
  WZ.chairs = chairDefaultInfants() ? WZ.infants : 0;   /* 기본값은 설정에서 (유아 수 / 0개) */
  render();
}
function wzCustom(){ WZ.customPeople=true; if(!WZ.people || WZ.people < 7) WZ.people=7; render(); }   /* 6명을 눌러 뒀어도 7부터(재아) */
function wzAdj(k,d){
  /* 막지 않습니다 — 이상한 값은 빨갛게 보여 주고 사장이 판단합니다 */
  if(k==="infants"){
    WZ.infants = Math.max(0,(WZ.infants||0)+d);
    WZ.chairs = chairDefaultInfants() ? WZ.infants : 0;
  }else{
    WZ.people = Math.max(1,(WZ.people||0)+d);
    /* 직접 입력 상태는 유지합니다 — 1명까지 내려도 됩니다 */
  }
  render();
}

/* ---------- 3단계: 좌석 ---------- */
/* ---------- 3단계: 좌석 (8차) ----------
   룸 | 테이블 두 갈래(가게에서 '룸 예약 / 테이블 예약' 이라 부름). 고른 갈래의 좌석 + '미정'.
   룸 쪽에는 인원이 맞는 합침 그룹(중문 탈거)도 나옵니다 — 자동 배정은 안 하고 사람이 고를 때만, 원탁은 확인창 */
function wzStepSeat(){
  const s=store(), st=s.settings;
  const total = WZ.people||0;
  const adults = adultCount(total, WZ.infants);
  if(!WZ.seatKind && WZ.seat){
    const cur = seatById(WZ.seat) || (st.joins||[]).find(j=>j.id===WZ.seat);
    WZ.seatKind = cur ? (isTable(cur) ? "table" : "room") : (isTablePref(WZ.seat) ? "table" : "room");
  }
  const kind = WZ.seatKind;   /* 8차-W(재아): 기본값 없음 — 룸/테이블을 먼저 고르면 그때 좌석이 보입니다 */

  const cell = (ids, x, extraCls) => {
    const label = ids.length > 1 ? seatLabelIds(ids).replace(/ (룸|테이블)$/,"") : esc(x.name);
    let statuses = ids.map(id=>roomStatus(WZ.date, WZ.time, id));
    const state = statuses.some(r=>r.state==="blocked") ? "blocked" : statuses.some(r=>r.state==="warn") ? "warn" : "free";
    const blocked = ids.some(id=>blockedAt(seatById(id), WZ.date, WZ.time));
    const over = total > seatsMax(ids), under = adults < seatsMin(ids, WZ.date);
    /* 2명이 2인석에 — 좁아서 손님이 싫어합니다. 고르는 단계부터 알립니다(8차-Y 재아). 규칙은 누님 질문 1번 대기 */
    const two = ids.length === 1 && isTable(x) && total > 0 && total <= 2 && (x.seats||4) <= 2;
    const txt = blocked ? "사용 중지" : state==="free" ? (over?"인원 초과":under?"인원 부족":two?"2인석 (좁음)":"이용 가능") : "이용 불가";
    const cls = blocked ? "blocked" : state!=="free" ? state : (over||under||two ? "warn" : "free");
    const bad = blocked || state!=="free" || over || under || two;
    const mv = statuses.reduce((a,r)=>a+(r.movable?r.movable.length:0),0);
    const key = ids.length > 1 ? x.id : ids[0];
    const sub = isTable(x) ? `${roomMin(x)?roomMin(x)+"~":""}${seatMax(x)}인${x.note?` · ${esc(x.note)}`:""}` : `${seatsMin(ids, WZ.date)}~${seatsMax(ids)}인${ids.length===1 && roomOpt(x) ? ` · 최적 ${roomOpt(x)}` : ""}`;
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
    const joins = (st.joins||[]);   /* 인원이 안 맞아도 다 보여 주고 '인원 부족/초과' 로 표시(재아: 합침이 안 보였음) */
    body = `<div class="sgrid">${rooms.map(r=>cell([r.id], r)).join("")}</div>` +
      (joins.length ? `<div class="lbl" style="margin-top:16px">룸 합침 <span class="lbl-note">중문 탈거 · 자동 배정 안 됨</span></div>
        <div class="sgrid">${joins.map(j=>cell(j.ids, {id:j.id, name:"", note:j.note}, "join")).join("")}</div>` : "");
  }else{
    /* 테이블은 층만 고릅니다 — 어느 테이블에 앉을지는 그날 현장에서. 남은 자리는 같은 시간대 겹치는 손님 수로 */
    const floors = tableFloors();
    const anyFit = WZ.time ? floorFit(null, WZ.date, WZ.time, total) : null;
    const anyBad = anyFit && anyFit.state !== "ok";
    body = `<div class="sgrid floors">
      ${floors.map(fl=>{
      const key = "table:" + fl, tb = floorTables(fl);
      const fit = WZ.time ? floorFit(fl, WZ.date, WZ.time, total) : null;
      /* 2명인데 이 층에 남은 게 2인석뿐이면 미리 알립니다 */
      const twoOnly = fit && fit.state === "ok" && total <= 2 && fit.f && !(fit.f.extra||[]).length && ((seatById(fit.f.id)||{}).seats||4) <= 2;
      const bad = fit && (fit.state !== "ok" || twoOnly);
      const txt = !fit ? "시간을 먼저" : fit.state === "ok" ? (twoOnly ? "2인석만 남음 (좁음)" : "자리 있음")
                : fit.state === "split" ? `붙일 테이블 없음 · 나눠 앉기 (한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명)`
                : `자리 없음 (한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명)`;
      return `<button class="scell ${WZ.seat===key?'on':''} ${bad?'warned busy':''}" onclick="wzSeat('${key}')">
        <span class="sn">${esc(floorLabel(fl))}</span>
        <span class="sc">테이블 ${tb.length} · ${tb.reduce((a,t)=>a+(t.seats||4),0)}석</span>
        <span class="avail ${bad?'warn':'free'}">${txt}</span>
      </button>`; }).join("")}</div>
      <button class="wz-adv ${WZ.tableAdv?'on':''}" onclick="WZ.tableAdv=!WZ.tableAdv; render()">${WZ.tableAdv?"▲":"▼"} 특정 테이블 지정 <span class="lbl-note">창가석·여포 같은 요청이 있을 때만. 보통은 층만 고르면 됩니다</span></button>
      ${WZ.tableAdv ? floors.map(fl=>`<div class="lbl" style="margin-top:10px">${esc(floorLabel(fl))}</div>
        <div class="sgrid tables">${floorTables(fl).map(t=>cell([t.id], t)).join("")}</div>`).join("") : ""}`;
  }
  const sess = WZ.time ? sessionAt(WZ.date, WZ.time) : null;
  const stv = sess ? (kind === "table" && sess.stayTable != null ? sess.stayTable : sess.stay) : null;
  const stayTxt = WZ.time ? (sess && stv==="end" ? `${sess.name} 세션 끝(${hm(minToHM(sessionEnd(WZ.date, sess)))})까지 한 팀` : `${hmDur(stayMinAt(WZ.date, WZ.time, kind === "table" ? "table-any" : null))} 머무는 기준`) : "";
  return `
    <div class="seat-note">${WZ.time?`<b>${hm(WZ.time)}</b> 입장 · ${stayTxt}`:"시간을 먼저 선택하세요"}</div>
    ${(()=>{ if(!WZ.time) return `<div class="seg seatkind"><button class="${kind==='room'?'on':''}" onclick="wzSeatKind('room')">룸 예약</button><button class="${kind==='table'?'on':''}" onclick="wzSeatKind('table')">테이블 예약</button></div>`;
      /* 고르는 순간부터 자리 여부를 — 종류 버튼에 '자리 없음' 을 붙입니다(재아). 룸: 이 인원이 앉을 빈 룸 하나라도, 테이블: 층 무관 */
      const roomOk = !!findSeat({date:WZ.date, time:WZ.time, people:total, kind:"room-any"});
      const tf = floorFit(null, WZ.date, WZ.time, total);
      return `<div class="seg seatkind">
        <button class="${kind==='room'?'on':''} ${roomOk?'':'warned'}" onclick="wzSeatKind('room')">룸 예약${roomOk?"":" · 빈 방 없음"}</button>
        <button class="${kind==='table'?'on':''} ${tf.state==='none'?'warned':''}" onclick="wzSeatKind('table')">테이블 예약${tf.state==='none'?" · 자리 없음":tf.state==='split'?" · 나눠 앉기":""}</button>
      </div>`; })()}
    <div class="lbl-note" style="margin:6px 0 10px">${kind==='room' ? `정원은 ${seatCountsInfants()?"유아 포함":"유아 제외 성인"} 기준 · 순서는 사장님이 정한 배정 우선순위` : "그 시간에 비는 테이블(붙임 포함)로 앉힐 수 있는지 봅니다. 어느 테이블인지는 당일 현장에서"}</div>
    ${body}
    ${!kind ? `<div class="empty">룸 예약인지 테이블 예약인지 먼저 고르세요.</div>` : kind==='room' ? `<p class="f-note" style="margin-top:12px">방을 안 고르고 <b>다음</b>을 누르면 '룸 미정' 으로 접수돼 빈 방에 잠정 배정됩니다.</p>` : `<p class="f-note" style="margin-top:12px">층을 안 고르고 <b>다음</b>을 누르면 층 상관없이 사장님 순서로 잡습니다. 어느 테이블인지는 당일 현장에서.</p>`}`;
}
function wzSeatKind(k){ WZ.seatKind = k; if(WZ.seat){ const cur = seatById(WZ.seat) || (store().settings.joins||[]).find(j=>j.id===WZ.seat); const isT = cur ? isTable(cur) : isTablePref(WZ.seat); if((k==="room") === !!isT) WZ.seat = null; } render(); }   /* 갈래를 바꾸면 다른 갈래의 선택은 지움 */
function wzChair(d){ WZ.chairs = Math.max(0,(WZ.chairs||0)+d); render(); }

/* 좌석 선택 — 막을 것은 막고, 판단이 필요한 것은 물어봅니다 */
/* 좌석 선택 — 막을 것은 막고, 판단이 필요한 것은 물어봅니다. v = 좌석 id / 합침 그룹 id / room-any / table-any */
async function wzSeat(v){
  const st = store().settings;
  const people = WZ.people||0;
  WZ.seatExtra = []; WZ.tentative = null; WZ.tentativeExtra = [];
  /* 테이블(층) — 테이블 단위로 앉힐 수 있는지 계산하되 이름은 안 보여 줍니다. 없거나 나눠 앉아도 알리기만 */
  if(/^table:/.test(v) || v === "table-any"){
    const fl = v === "table-any" ? null : v.slice(6), fit = floorFit(fl, WZ.date, WZ.time, people);
    if(fit.state === "none" && !await uiConfirm(`${floorLabel(fl)}에 ${people}명 자리가 없습니다`,
      `${hm(WZ.time)} 기준으로 비는 테이블을 붙여도 한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명입니다.\n\n회전·합석으로 감당 가능하면 접수하세요. '테이블 자리 없음' 경고로 남습니다.`,
      {ok:"그래도 접수", cancel:"다시 고르기"})) return;
    if(fit.state === "split" && !await uiConfirm(`${floorLabel(fl)}에서는 나눠 앉게 됩니다`,
      `붙일 수 있는 테이블이 없습니다 (한 자리 최대 ${floorMaxParty(fl, WZ.date, WZ.time)}명). 옆 테이블에 나눠 앉는 것으로 접수합니다.\n손님께 안내하셨나요?`,
      {ok:"안내했음 · 접수", cancel:"다시 고르기"})) return;
    WZ.tentative = fit.f ? fit.f.id : null; WZ.tentativeExtra = fit.f ? fit.f.extra : []; WZ.tentativeSplit = fit.state === "split";
    WZ.seat = v; wzAutoNext();
    return;
  }
  if(!["any","hall-any","table-any","room-any"].includes(v)){
    const j = (st.joins||[]).find(g=>g.id===v);
    const ids = j ? j.ids.slice() : [v];
    if(!seatById(ids[0])) return;
    const label = seatLabelIds(ids);
    for(let k=0;k<ids.length;k++){
      const room = seatById(ids[k]);
      const bk = blockedAt(room, WZ.date, WZ.time);
      if(bk && !await uiConfirm(`${room.name}은 이 시각에 사용 중지입니다`,
        `${dateLabel(WZ.date)} ${spanLabel(bk)}${bk.note?`\n사유: ${bk.note}`:""}\n\n그래도 이 자리로 배정할까요?`,
        {ok:"그래도 배정", cancel:"다시 고르기"})) return;
      const rs = roomStatus(WZ.date, WZ.time, ids[k]);
      if(rs.state==="blocked"){
        const lines = rs.hits.map(r=>`· ${hm(r.time)} ${r.name} 손님 ${pplText(r)}`).join("\n");
        if(!await uiConfirm(`${room.name}에 ${hmDur(store().settings.closeGapMin != null ? store().settings.closeGapMin : 60)} 안에 확정 예약이 있습니다`, lines, {ok:"그래도 배정", cancel:"다시 고르기"})) return;
      }
      if(rs.state==="warn"){
        const a = rs.hits.map(r=>`· ${hm(r.time)} ${r.name} 손님 ${pplText(r)}`);
        const b = rs.tentative.map(r=>`· ${hm(r.time)} ${r.name} 손님 ${pplText(r)} (좌석 미정 · 잠정 배정)`);
        if(!await uiConfirm2(`${room.name}에 겹치는 예약이 있습니다.\n\n${[...a,...b].join("\n")}\n\n그래도 배정할까요?`)) return;
      }
    }
    if(people > seatsMax(ids)){
      if(!await uiConfirm2(`${label}은 최대 ${seatsMax(ids)}명입니다. 지금 ${people}명입니다.\n간이 의자 등으로 감당 가능한 경우에만 배정하세요.`)) return;
    }else{
      const adults = adultCount(people, WZ.infants);
      if(adults < seatsMin(ids, WZ.date)){
        const basis = store().settings.minCountAdultsOnly===false ? "총 인원" : "성인";
        if(!await uiConfirm(`${label} 최소 인원 미달`, `최소 ${seatsMin(ids, WZ.date)}명부터 받습니다.\n지금 ${basis} ${adults}명입니다${WZ.infants?` (유아 ${WZ.infants}명 제외)`:""}.`, {ok:"그래도 배정", cancel:"다시 고르기"})) return;
      }
    }
    /* 한 테이블에 안 들어가는 인원이 테이블 하나를 고르면 붙일 테이블을 함께 제안 */
    const one = seatById(v);
    if(!j && isTable(one) && people > seatMax(one)){
      const f = findSeat({date:WZ.date, time:WZ.time, people:people, kind:"table-any"});
      if(f && f.id === v && f.extra.length){
        if(!await uiConfirm2(`${one.name} 하나로는 ${people}명이 안 됩니다.\n${seatLabelIds([f.id].concat(f.extra))}로 붙여서 받을까요?`)) return;
        WZ.seatExtra = f.extra;
      }
    }
    if(j && (j.split || j.note) && !await uiConfirm(`${label} — ${j.note || "공간이 나뉩니다"}`, j.split ? "테이블이 나뉘어 앉게 됩니다. 손님께 확인하셨나요?" : "손님께 확인하셨나요?", {ok:"확인했음", cancel:"다시 고르기"})) return;
    if(j) WZ.seatExtra = ids.slice(1);
    WZ.seat = j ? ids[0] : v; WZ.seatJoin = j ? j.id : null; wzAutoNext();
    return;
  }
  /* 좌석 미정 — 잠정 배정 가능 여부를 먼저 확인 */
  const f = suggestSeatFull(WZ.date, WZ.time, people, v);
  if(!f){
    if(!await uiConfirm2(`지금 ${hm(WZ.time)} 기준으로 ${people}명이 들어갈 빈 자리가 없습니다.\n먼저 접수한 좌석 미정 예약까지 계산한 결과입니다.\n\n자리 없이 접수할까요?`)) return;
  }
  WZ.tentative = f ? f.id : null; WZ.tentativeExtra = f ? f.extra : [];
  WZ.seat = v; WZ.step = 4; WZ.maxStep = Math.max(WZ.maxStep||0, 4); render();
}
/* 전화번호가 노쇼 이력이 있는 번호인지 — 입력하는 즉시 보여줍니다 */
function noshowHint(){
  const ph = (WZ.phone||"").replace(/\D/g,"");
  if(ph.length < 9) return "";
  const ns = noshowOf(WZ.phone);
  if(!ns) return "";
  return `<div class="ns-hint">노쇼 이력 ${ns.count}회</div>`;
}
/* ---------- 4단계: 예약자 ---------- */
function wzStepGuest(){
  return `
    <label class="f big"><div class="lb">예약자 성함</div>
      <input id="wz-name" value="${esc(WZ.name)}" placeholder="예: 김영수" autocomplete="off" autofocus>
    </label>
    <div class="f big"><div class="lb">전화번호</div>
      <div class="inrow">
        <input id="wz-phone" type="tel" inputmode="numeric" pattern="[0-9-]*"
               value="${esc(WZ.phone)}" placeholder="010-0000-0000"
               onfocus="wzPhoneNone(false)">
        <button class="nonebtn sm warn ${WZ.phoneNone?'on':''}" onclick="wzPhoneNone()">번호 없음</button>
      </div>
      <div class="ns-slot">${noshowHint()}</div>
    </div>
    `;
}
function wzAllergyNone(v){
  wzSyncInputs();
  const next = (v === false) ? false : !WZ.allergyNone;
  if(next === WZ.allergyNone) return;
  WZ.allergyNone = next;
  if(next) WZ.allergy = "";
  render();
}
/* 인자 없이 부르면 토글, false 를 주면 해제만 (입력칸을 누르면 자동 해제) */
function wzPhoneNone(v){
  const next = (v === false) ? false : !WZ.phoneNone;
  if(next === WZ.phoneNone) return;
  WZ.phoneNone = next;
  if(next) WZ.phone = "";
  render();
}
/* 숫자만 남기고 010-0000-0000 형태로 자동 정리 */
/* 010 으로 시작할 때만 자동으로 - 를 넣습니다.
   직접 - 를 치는 분도 있어서, 사용자가 넣은 자리를 시스템이 다시 옮기면 오히려 방해가 됩니다.
   그래서 이미 - 가 들어 있으면 손대지 않습니다. */
/* ※ 예전에는 "값에 - 가 하나라도 있으면 손대지 않음" 이었는데, 시스템이 넣은 - 도 그 조건에 걸려
      010-1234 까지 만든 뒤로는 다시 정리하지 않아 010-12345678 이 됐습니다.
      이제 '사용자가 - 를 직접 쳤는지'(phoneManual)만 보고, 아니면 숫자만으로 매번 다시 만듭니다 */
function fmtPhone(el, ev){
  const raw = el.value;
  if(ev && ev.inputType==="insertText" && ev.data==="-") WZ.phoneManual = true;
  if(!raw.replace(/\D/g,"")) WZ.phoneManual = false;        /* 다 지우면 다시 자동으로 */
  if(WZ.phoneManual){ WZ.phone = raw; return; }
  const out = phoneFmt(raw.replace(/\D/g,"").slice(0,11));
  if(el.value !== out) el.value = out;
  WZ.phone = out;
}
/* 숫자열 → 하이픈 넣은 번호. 휴대폰(01x) 3-4-4, 서울(02) 2-3-4 / 2-4-4, 지역번호(033 등) 3-3-4 / 3-4-4, 1588 류 4-4.
   입력 중(자릿수가 다 안 찼을 때)에도 앞부분 하이픈은 미리 넣어 줍니다 */
/* 입력한 번호를 저장용 모양으로 — 숫자만 남기고 phoneFmt. 서버 왕복 뒤 모양이 달라져 충돌로 오인하던 것을 막습니다(점검 D10) */
function phoneNorm(v){ const d = String(v || "").replace(/\D/g, ""); return d ? phoneFmt(d) : ""; }
function phoneFmt(d){
  if(!d) return "";
  let a = 3;                                   /* 앞자리(지역·통신사) 길이 */
  if(d.indexOf("02") === 0) a = 2;
  else if(/^1[5-9]/.test(d)) a = 4;            /* 1588-0000 같은 대표번호 */
  if(d.length <= a) return d;
  const rest = d.slice(a);
  if(a === 4) return d.slice(0,4) + "-" + rest;
  /* 가운데 자리: 휴대폰은 4, 그 외는 전체 길이가 (a+8) 이면 4, 아니면 3 */
  const mobile = d.indexOf("01") === 0;
  const mid = mobile ? 4 : (d.length >= a+8 ? 4 : 3);
  if(rest.length <= mid) return d.slice(0,a) + "-" + rest;
  return d.slice(0,a) + "-" + rest.slice(0,mid) + "-" + rest.slice(mid);
}

/* ---------- 5단계: 메뉴 ---------- */
/* 코스 선택 팝업은 마법사(WZ)와 예약 수정 시트(tmpRes) 두 곳에서 씁니다.
   어느 쪽 값을 고치는지 여기서 한 번만 정해 둡니다 — 함수를 두 벌 만들지 않으려고. */
function cTgt(){ return WZ ? WZ : tmpRes; }
/* 시트에서 쓸 때는 화면을 다시 그리기 전에 입력창 값을 옮겨 담아야 타이핑이 날아가지 않습니다 */
function cSync(){ if(!WZ && tmpRes) syncRes(); }
function courseCount(){
  const t = cTgt();
  return t ? Object.values(t.courses||{}).reduce((a,b)=>a+b,0) : 0;
}
function courseSummary(courses){
  const items = Object.entries(courses||{}).filter(([k,v])=>v>0)
    .map(([k,v])=>`${k.split("|")[1]}${v>1?`×${v}`:""}`);
  return items.join(", ");
}
function wzStepMenu(){
  const st = store().settings;
  const seat = st.rooms.find(x=>x.id===WZ.seat);
  const isHall = seat ? isTable(seat) : isTablePref(WZ.seat);
  /* 테이블은 보통 메뉴를 정하지 않고 받습니다 — 선택지를 줄입니다 */
  const opts = isHall
    ? [["코스","코스",""],
       ["해당 없음","해당 없음",""]]
    : [["코스","코스",""],
       ["코스 상당","코스 상당",""],
       ["확인 필요","확인 필요",""],
       ["해당 없음","해당 없음",""]];
  const n = courseCount();
  const adults = adultCount(WZ.people, WZ.infants);
  const seatIsRoom = seat && seat.type==="room";
  /* 룸은 코스 주문을 전제로 받는 자리입니다 */
  const roomWarn = seatIsRoom && (
    WZ.menuType==="해당 없음" ? "룸 예약에 코스 이용 예정 손님이 아닙니다" :
    WZ.menuType==="확인 필요" ? "" :
    (WZ.menuType==="코스" && !WZ.courseUndecided && n>0 && n<adults)
      ? `코스 ${n}인분 · 성인 ${adults}명보다 적습니다` : "");
  /* 룸 경고 문구는 위 질문 아래 경고 자리(wz-warn)에 이미 뜨므로 여기서는 타일 색만 바꿉니다 */
  return `
    <div class="srcgrid menu4 ${opts.length===2?'menu2':''}">
      ${opts.map(([v,label,desc])=>`
        <button class="srccell ${WZ.menuType===v?'on':''} ${WZ.menuType===v&&roomWarn?'warned':''}" onclick="wzMenu('${v}')">
          <span class="s-l">${label}</span>
          ${desc?`<span class="s-d">${desc}</span>`:""}
          ${v==="코스"&&n?`<span class="s-n">${n}</span>`:""}
        </button>`).join("")}
    </div>
      <div class="course-sum ${WZ.menuType==="코스"?'':'hold'}">
        ${WZ.courseUndecided ? "코스 미정 · 방문 전 확정" : (n?`${esc(courseSummary(WZ.courses))}`:"구성을 고르세요")}
        <button class="btn sm" style="margin-left:auto" onclick="openCourse()" ${WZ.menuType==="코스"?'':'tabindex="-1"'}>${n||WZ.courseUndecided?"수정":"선택"}</button>
      </div>
    ${WZ.courseOpen?renderCourse():""}`;
}
function wzMenu(v){
  WZ.menuType = v;
  if(v==="코스"){ WZ.courseOpen = true; render(); return; }
  WZ.courses = {}; WZ.courseOpen = false;
  wzAutoNext();
}
/* 코스 팝업의 '완료' — 마법사에서는 코스 인원이 맞으면 바로 예약자 단계로 */
function doneCourse(){
  cSync(); const t=cTgt(); if(t) t.courseOpen = false;
  if(WZ) wzAutoNext(); else render();
}
function openCourse(){ cSync(); const t=cTgt(); if(t) t.courseOpen = true; render(); }
function closeCourse(){ cSync(); const t=cTgt(); if(t) t.courseOpen = false; render(); }
/* 한 테이블은 코스를 통일하는 것이 규칙이라, 처음 누르면 '아직 코스가 없는 성인 수'만큼 한 번에 채웁니다.
   (4명 테이블이면 탭 한 번에 4). 그 뒤로는 누를 때마다 1씩, 줄일 때는 모서리 − 로 */
function bumpCourse(key){
  cSync(); const t=cTgt(); if(!t) return;
  const cur = (t.courses||{})[key]||0;
  let add = 1;
  if(!cur){
    const adults = adultCount(t.people||0, t.infants||0);
    add = Math.max(1, adults - courseCount());
  }
  t.courses = {...t.courses, [key]:cur+add};
  t.courseUndecided = false;
  render();
}
function dropCourse(key){
  cSync(); const t=cTgt(); if(!t) return;
  const cur = (t.courses||{})[key]||0;
  const next = {...t.courses}; if(cur<=1) delete next[key]; else next[key] = cur-1;
  t.courses = next; render();
}
function resetCourse(){ cSync(); const t=cTgt(); if(!t) return; t.courses = {}; t.courseUndecided = false; render(); }
function toggleUndecided(){
  cSync(); const t=cTgt(); if(!t) return;
  t.courseUndecided = !t.courseUndecided;
  if(t.courseUndecided) t.courses = {};
  render();
}
/* 이 예약의 날짜·시각에 그 코스 그룹을 파는지 */
function courseGroupFits(g){
  const stx = store().settings, W = cTgt();
  /* 점심/저녁은 그 날 세션으로 판단 — 주말은 15:30 까지가 점심입니다(8차 세션) */
  const sess = W.date && W.time ? sessionAt(W.date, W.time) : null;
  const lunch = sess ? /점심/.test(sess.name||"") : (W.time && toMin(W.time) < toMin(stx.lunchUntil||"16:00"));
  const dow = W.date ? new Date(W.date+"T00:00:00").getDay() : 0;
  /* 공휴일을 주말로 볼지는 설정에서 정합니다 */
  const weekend = dow===0 || dow===6 || (stx.holidayAsWeekend!==false && isHoliday(W.date));
  const w = g.when||[];
  if(!w.length || w.includes("종일")) return true;
  const key = (weekend?"주말":"평일") + (lunch?"점심":"저녁");
  return w.includes(key);
}
/* 코스 구성에서 걸리는 것 — 코스 팝업 안과 '다음' 버튼 위 경고 자리 두 곳에 같이 씁니다.
   1) 그 시간대에 팔지 않는 코스가 들어감 (예: 저녁에 평일 점심 코스)
   2) 코스가 두 종류 이상 섞임 — 한 테이블은 코스를 통일하는 것이 가게 규칙입니다
   둘 다 막지 않습니다. 사장님이 예외를 둘 수 있으므로 빨갛게 알리기만 합니다 */
function courseWarns(){
  const W = cTgt(); if(!W || W.menuType!=="코스" || W.courseUndecided) return [];
  const gs = courseGroups(), out = [];
  const picked = Object.entries(W.courses||{}).filter(([k,v])=>v>0);
  const offNames = picked.filter(([k])=>{ const g = courseGroupById(gs, k.split("|")[0]); return g && !courseGroupFits(g); })
    .map(([k])=>k.split("|")[1]);
  if(offNames.length) out.push(`이 시간엔 없는 코스 - ${offNames.join(", ")}`);
  if(picked.length >= 2) out.push(`코스 ${picked.length}종류 - 한 테이블은 하나로`);
  return out;
}
function renderCourse(){
  const gs = courseGroups();
  const W = cTgt();
  const fits = courseGroupFits;
  const rows = gs.map((g,gi)=>`
    <div class="cgroup ${fits(g)?'':'off'}">
      <div class="cg-label">${esc(g.label)}${fits(g)?'':''}</div>
      <div class="cg-items">
        ${g.items.map(name=>{
          const key = `${g.id}|${name}`;
          const c = (W.courses||{})[key]||0;
          const off = !fits(g);
          return `<span class="citem-w"><button class="citem ${c?'on':''} ${off&&c?'warned':''}" onclick="bumpCourse('${jsq(key)}')">
            ${esc(name)}${c?`<i class="cnum">${c}</i>`:""}</button>${c?`<button class="cminus" onclick="dropCourse('${jsq(key)}')" aria-label="하나 줄이기">−</button>`:""}</span>`;
        }).join("")}
      </div>
    </div>`).join("");
  return `
    <div class="overlay" onclick="closeCourse()">
      <div class="sheet" onclick="event.stopPropagation()">
        <div class="sheet-h"><h2>코스 선택</h2>
          <button class="x" onclick="closeCourse()" aria-label="닫기">×</button></div>
                ${rows}
        <button class="undecided ${W.courseUndecided?'on':''}" onclick="toggleUndecided()">
          코스 미정
        </button>
        ${(()=>{
          const n = courseCount(), ad = adultCount(W.people, W.infants);
          const short = n>0 && n<ad, over = n>ad;
          return `<div class="course-total ${short||over||courseWarns().length?'bad':''}">선택 합계 <b>${n}</b>명
            ${W.people?` / 성인 ${ad}명${W.infants?` (유아 ${W.infants}명)`:""}`:""}
            ${short?`<div class="ct-warn">코스 부족 - 성인보다 ${ad-n}명 적음</div>`:""}
            ${over?`<div class="ct-warn">코스 초과 - 성인보다 ${n-ad}명 많음</div>`:""}
            ${courseWarns().map(w=>`<div class="ct-warn">${esc(w)}</div>`).join("")}</div>`;
        })()}
        <div class="sheet-actions">
          <button class="btn danger" onclick="resetCourse()">초기화</button>
          <button class="btn primary" onclick="doneCourse()">완료</button>
        </div>
      </div>
    </div>`;
}

/* ---------- 6단계: 추가사항 ---------- */
function wzStepExtra(){
  return `
    <div class="f big"><div class="lb">알러지</div>
      <div class="inrow">
        <input id="wz-allergy" value="${esc(WZ.allergy)}"
               placeholder="예: 갑각류 알러지 1명" onfocus="wzAllergyNone(false)">
        <button class="nonebtn sm ${WZ.allergyNone?'on':''}" onclick="wzAllergyNone()">없음</button>
      </div>
    </div>
    <div class="f big"><div class="lb">유아용 의자
      ${(WZ.chairs||0)>(WZ.infants||0)?`<span class="req">유아 ${WZ.infants||0}명보다 많음</span>`:""}</div>
      <div class="bigstep sm ${(WZ.chairs||0)>(WZ.infants||0)?'bad':''}" style="justify-content:flex-start; margin-top:0">
        <button onclick="wzChair(-1)">−</button>
        <div class="v"><span>${WZ.chairs||0}</span><small>개</small></div>
        <button onclick="wzChair(1)">＋</button>
      </div>
      <div class="f-note">${chairDefaultInfants()?`유아 ${WZ.infants||0}명 기준 자동 입력`:"&nbsp;"}</div>
    </div>
    <label class="f big"><div class="lb">요청사항 <span class="lbl-note">선택</span></div>
      <input id="wz-request" value="${esc(WZ.request)}" placeholder="예: 송별회, 상견례">
    </label>
    <label class="f big"><div class="lb">메모 <span class="lbl-note">선택</span></div>
      <input id="wz-memo" value="${esc(WZ.memo||"")}" placeholder="예: 사장님 지인, 상석 준비">
    </label>
    <div class="wz-review">
      <div class="rv"><span>일시</span><b>${WZ.date?dateLabel(WZ.date):"-"} ${WZ.time?hm(WZ.time):""}</b></div>
      <div class="rv"><span>인원</span><b>총 ${WZ.people||0}명${WZ.infants?` (유아 ${WZ.infants}명 포함)`:""}</b></div>
      ${WZ.chairs?`<div class="rv"><span>유아의자</span><b>${WZ.chairs}개</b></div>`:""}
      <div class="rv"><span>좌석</span><b>${WZ.seat?(WZ.seatExtra&&WZ.seatExtra.length?seatLabelIds([WZ.seat].concat(WZ.seatExtra)):seatLabel(WZ.seat)):"-"}</b></div>
      <div class="rv"><span>예약자</span><b>${esc(WZ.name)||"-"} ${esc(WZ.phone)}</b></div>
      <div class="rv"><span>식사</span><b>${esc(WZ.menuType||"-")}${WZ.menuType==="코스"&&courseCount()?` · ${esc(courseSummary(WZ.courses))}`:""}</b></div>
    </div>`;
}

/* ---------- 새 예약 등록 — 마법사(wzSubmit)와 빠른 입력(saveRes)이 같은 길을 갑니다 ----------
   같은 번호 확인 → 노쇼 이력 확인(confirmNewRes) → 등록 기록·문자 흉내·목록에 넣기·로그·잠정 배정(createReservation).
   둘이 따로 있으면 데이터 모양(changes·updatedAt·source…)이 조금씩 달라집니다 */
async function confirmNewRes(date, phone){
  const s = store();
  /* 같은 번호로 같은 날 이미 예약이 있으면 확인 */
  if(phone){
    const dup = s.reservations.filter(r=>r.date===date && r.status==="확정" &&
      (r.phone||"").replace(/\D/g,"") === phone.replace(/\D/g,""));
    if(dup.length){
      const ok = await uiConfirm("같은 번호로 이미 예약이 있습니다",
        dup.map(r=>`${hm(r.time)} ${r.name} 손님 ${pplText(r)}`).join("\n") +
        "\n\n같은 팀이라면 기존 예약을 수정하는 편이 좋습니다.",
        {ok:"새로 등록", cancel:"취소"});
      if(!ok) return false;
    }
  }
  /* 노쇼 이력이 있으면 확정 전에 확인 */
  const ns = noshowOf(phone);
  if(ns && !await uiConfirm2(
      `이 번호로 노쇼 기록이 ${ns.count}건 있습니다.\n` +
      `(${ns.dates.slice(0,3).map(d=>d.slice(5).replace("-","월 ")+"일").join(", ")}${ns.dates.length>3?" 외":""})\n\n` +
      `예약을 확정할까요?`)) return false;
  return true;
}
function createReservation(rec){
  const s = store();
  addChange(rec, "등록", []);
  /* 접수 문자 — 등록 즉시 1회 (지금은 흉내) */
  if(smsCfg().on && rec.phone) smsSend(rec, "접수");
  s.reservations.push(rec);
  logEvent("예약 등록", `${rec.date} ${rec.time} ${rec.name} ${pplOf(rec)}명 ${rec.roomId?seatLabel(rec.roomId):(rec.tentativeRoomId?"잠정 "+seatLabel(rec.tentativeRoomId):"미배정")} 경로:${rec.source}${rec.sourceDetail?"/"+rec.sourceDetail:""}`);
  reflowTentatives(rec.date);
  return rec;
}
/* ---------- 등록 ---------- */
async function wzSubmit(){
  wzSyncInputs();
  if(!WZ.date || !WZ.time) return await uiAlert2("날짜와 시간을 선택하세요.");
  if(!WZ.people) return await uiAlert2("인원을 선택하세요.");
  if(!WZ.name.trim()) return await uiAlert2("예약자 성함을 입력하세요.");
  if(!await confirmNewRes(WZ.date, WZ.phone)) return;
  const fixed = WZ.seat && !["any","hall-any","table-any","room-any"].includes(WZ.seat) && !/^table:/.test(WZ.seat);   /* 좌석을 특정했는지 (층 희망은 미정 취급) */
  const rec = {
    id:newId("res"), date:WZ.date, time:WZ.time,
    name:WZ.name.trim(), phone:phoneNorm(WZ.phone),
    people:WZ.people, infants:WZ.infants, chairs:WZ.chairs||0,
    roomId: fixed ? WZ.seat : null,
    extraIds: fixed ? (WZ.seatExtra || []) : [],
    seatPref: fixed ? null : WZ.seat,     /* 미배정일 때 희망 좌석 종류를 기억 */
    tentativeRoomId: fixed ? null : (WZ.tentative || null),  /* 나중에 확정할 때 1순위로 뜨는 자리 */
    tentativeSplit: fixed ? false : !!WZ.tentativeSplit,
    tentativeExtra: fixed ? [] : (WZ.tentativeExtra || []),
    source:WZ.source||"전화 예약",
    sourceDetail:WZ.source==="기타" ? (WZ.sourceDetail||"").trim() : "",
    createdAt:new Date().toISOString(),
    menuType:WZ.menuType||"해당 없음", courses:{...(WZ.courses||{})},
    courseUndecided: !!WZ.courseUndecided,
    allergy:WZ.allergyNone?"":WZ.allergy.trim(), allergyChecked:true, request:WZ.request.trim(),
    memo:(WZ.memo||"").trim(),
    status:"확정"
  };
  createReservation(rec);
  /* 6차 전에는 view.date = rec.date 로 그 날짜로 점프했습니다. 이제 화면 날짜는 그대로 — 완료 화면에 날짜가 있고,
     닫은 뒤 토스트의 '보기' 로 갈 수 있습니다(closeWizardDone) */
  WZ.done = rec;
  saveData(); render();
}
/* 등록 완료 화면 — 손님에게 그대로 읽어주면 되는 문장 */
function wzDone(){
  const r = WZ.done;
  const d = new Date(r.date+"T00:00:00");
  const dow = ["일","월","화","수","목","금","토"][d.getDay()];
  const [h,m] = r.time.split(":").map(Number);
  const ap = h<12?"오전":"오후", h12 = h%12===0?12:h%12;
  const seat = r.roomId ? resSeatLabel(r)
             : seatText(r);
  return `
    <div class="wz done">
      <div class="done-box">
        <div class="check">✓</div>
        <p class="done-msg">
          <b>${d.getMonth()+1}월 ${d.getDate()}일 ${dow}요일, ${hm(WZ.done.time)}</b>,
          <b>${esc(seat)}</b> 좌석,
          <b>${esc(r.name)}</b> 손님<br>예약이 접수됐습니다
        </p>
        <div class="done-sub">${pplText(r)}${r.phone?` · ${esc(r.phone)}`:""}
          ${r.menuType?`<br>식사: ${esc(r.menuType)}${r.courses&&Object.keys(r.courses).length?` (${esc(courseSummary(r.courses))})`:""}`:""}
          ${r.chairs?`<br>유아용 의자 ${r.chairs}개`:""}
          ${r.allergy?`<br>알러지: ${esc(r.allergy)}`:""}${r.request?`<br>요청: ${esc(r.request)}`:""}</div>
        <div class="done-btns">
          <button class="btn lg" onclick="openWizard('${r.date}')">새 예약</button>
          <button class="btn primary lg" onclick="closeWizardDone()">확인</button>
        </div>
      </div>
    </div>`;
}
function closeWizardDone(){ var r = WZ && WZ.done; WZ=null; render(); histPop(); toastSaved(r); }
