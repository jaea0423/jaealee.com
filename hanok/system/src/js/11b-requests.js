/* ---------- 홈페이지 예약 — 흉내 ----------
   가게 사이트(../site) 예약 창에서 손님이 접수한 것이 여기로 들어옵니다. 접수는 바로 확정이 아니고,
   직원이 보고 ① 승인 → 마법사가 그 내용으로 채워져 열리고 좌석까지 골라 등록 → 확정 문자
          ② 거절 → 사유 골라 문자(흉내)
   지금은 서버가 없어 브라우저 안(메모리)에서만 돕니다. REQ_API 세 개만 Supabase 로 바꾸면 됩니다.
     list()          → 대기 목록        submit 은 사이트 쪽(site/js/reserve.js RES_API.submit) 이 넣습니다
     accept(id, res) → 확정 처리 + 예약 id 기록
     reject(id, why) → 거절 처리
   요청 모양 = 사이트가 보내는 payload 그대로:
     {id, createdAt, date, time, adults, kids, people, seat:"room"|"table", course:"course:촉 코스"|"set:B 세트"|"later"|"none",
      courseLabel, name, phone, request, status:"대기"|"확정"|"거절", resId, reason}
   온라인 접수 기준(재아, 사이트와 같은 값): 성인 2명부터 · 룸은 성인 5명부터 · 13명 이상은 전화. 사이트에서 이미 걸러서 오지만
   여기서도 한 번 더 표시합니다(경고는 막지 않고 알리기만). */
const REQ_RULE = { minAdults:2, roomMinAdults:5, onlineMax:12, expireH:24 };   /* expireH: 이 시간 안에 확정·거절이 없으면 자동 취소 */
let REQUESTS = [];
const REQ_API = {
  list: async () => REQUESTS.filter(q => q.status === "대기"),
  accept: async (id, resId) => { const q = REQUESTS.find(x => x.id === id); if(q){ q.status = "확정"; q.resId = resId; } return {ok:true}; },
  reject: async (id, why) => { const q = REQUESTS.find(x => x.id === id); if(q){ q.status = "거절"; q.reason = why; } return {ok:true}; }
};
/* 24시간 지나면 자동 만료 — 목록을 볼 때마다 정리합니다. 실제 서버에서는 cron 이 하고, 여기서는 흉내 */
function reqExpireAt(q){ return q.expiresAt ? new Date(q.expiresAt).getTime() : new Date(q.createdAt).getTime() + REQ_RULE.expireH * 3600e3; }   /* 서버 값이 있으면 그것 */
function reqSweep(){
  const now = Date.now();
  REQUESTS.forEach(q => { if(q.status === "대기" && reqExpireAt(q) <= now){ q.status = "만료"; q.reason = "24시간 안에 처리되지 않음"; reqExpireSms(q); } });
}
function reqPending(){ reqSweep(); return REQUESTS.filter(q => q.status === "대기"); }
/* 만료 안내 문자(흉내) — 홈페이지 예약 시트·사이트 안내문에 "자동 취소되고 안내 문자가 갑니다" 라고 적혀 있어 실제로도 보냅니다 */
function reqExpireSms(q){
  if(!q || !q.phone || typeof smsMockSend !== "function") return;
  smsMockSend(q.phone, q.name, `[한옥반점] ${q.name}님, ${dateLabel(q.date)} ${hm(q.time)} 예약 요청을 24시간 안에 확인해 드리지 못해 접수가 취소되었습니다. 죄송합니다. 전화 주시면 자리를 찾아드리겠습니다. ${store().settings.tel || "031-724-1004"}`);
}
/* "23시간 10분 남음" — 1시간 아래면 분만, 다 되면 '만료 임박' */
function reqLeft(q){
  const ms = reqExpireAt(q) - Date.now(); if(ms <= 0) return "만료";
  const h = Math.floor(ms / 3600e3), m = Math.floor((ms % 3600e3) / 60000);
  return h ? `${h}시간 ${m}분 남음` : `${m}분 남음`;
}
function reqById(id){ return REQUESTS.find(q => q.id === id); }
function reqPeopleText(q){ return q.kids ? `${q.people}명(어린이${q.kids})` : `${q.people}명`; }
function reqMenuText(q){
  if(q.course === "later") return "코스·세트 미정";
  if(q.course === "none") return "단품 주문";
  return `${q.courseLabel} ${q.people}인분`;
}
/* 사이트에서 접수할 때는 되던 것이 그 사이에 안 되게 된 것 — '충돌' 만 봅니다(규칙은 사이트가 이미 걸렀음).
   · 그 날 같은 번호로 다른 예약이 들어옴  · 그 사이 자리가 참  · 날짜가 지남 */
function reqWarns(q){
  const out = [];
  if(q.date < todayStr()) out.push("지난 날짜");
  try{
    const seats = store().settings.rooms;
    const free = seats.filter(x => (q.seat === "room" ? isRoom(x) : isTable(x)) && !blockedAt(x, q.date, q.time)
                   && q.people <= seatMax(x) && (q.seat !== "room" || q.people >= roomMin(x, q.date))
                   && roomStatus(q.date, q.time, x.id).state === "free").length;
    if(!free) out.push(q.seat === "room" ? "그 시간에 빈 룸이 없음" : "그 시간에 빈 테이블이 없음");
  }catch(e){}
  const dup = store().reservations.find(r => r.date === q.date && r.status !== "취소" && (r.phone||"").replace(/\D/g,"") === (q.phone||"").replace(/\D/g,""));
  if(dup) out.push(`같은 날 같은 번호 예약 있음 (${dup.time} ${dup.name})`);
  return out;
}

/* ---------- 목록 시트 ---------- */
function openRequests(){ view.form = {type:"reqs"}; render(); }
function sheetRequests(){
  const list = reqPending().sort((a,b) => a.date.localeCompare(b.date) || a.time.localeCompare(b.time));
  const rows = list.length ? list.map(q => {
    const w = reqWarns(q);
    return `<button class="rowitem tap" onclick="openRequest('${q.id}')">
      <span class="grow"><span class="t">${esc(q.name)} <span class="tag">${q.seat==="room"?"룸":"테이블"}</span>${w.length?`<span class="tag rust">${esc(w[0])}</span>`:""}</span>
        <span class="s">${dateLabel(q.date)} ${hm(q.time)} · ${reqPeopleText(q)} · ${esc(reqMenuText(q))}</span></span>
      <span class="s left ${reqExpireAt(q)-Date.now() < 3600e3 ? "soon" : ""}" style="white-space:nowrap; text-align:right">${reqLeft(q)}<br><span class="muted">${reqAgo(q.createdAt)} 접수</span></span>
    </button>`; }).join("")
    : `<div class="empty">처리할 홈페이지 예약이 없습니다.<br><span class="s">손님이 홈페이지에서 접수하면 여기로 들어옵니다. 24시간 안에 확정·거절하지 않으면 자동 취소됩니다.</span></div>`;
  return `
    ${sheetHead(`홈페이지 예약 · ${list.length}건`)}
    <div class="card searchbox">${rows}</div>
    <div class="sheet-actions">
      ${supaOn() ? "" : `<button class="btn ghost" onclick="reqSeedDemo()">흉내 예약 넣기</button>`}
      <button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
function reqAgo(iso){
  const m = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));
  return m < 1 ? "방금" : m < 60 ? `${m}분 전` : m < 1440 ? `${Math.floor(m/60)}시간 전` : `${Math.floor(m/1440)}일 전`;
}

/* ---------- 요청 하나 ---------- */
function openRequest(id){ view.form = {type:"req", id}; render(); }
function sheetRequest(){
  const q = reqById(view.form.id); if(!q) return sheetRequests();
  const w = reqWarns(q);
  const row = (k, v) => `<div class="rv"><span>${k}</span><b>${v}</b></div>`;
  return `
    ${sheetHead("홈페이지 예약")}
    <div class="card" style="padding:12px 14px">
      ${row("날짜", `${dateLabel(q.date)} ${hm(q.time)}`)}
      ${row("인원", q.kids ? `성인 ${q.adults} · 어린이 ${q.kids}` : `성인 ${q.adults}`)}
      ${row("자리", q.seat === "room" ? "룸" : "테이블")}
      ${row("메뉴", esc(reqMenuText(q)))}
      ${row("예약자", `${esc(q.name)} · ${esc(q.phone)}`)}
      ${q.request ? row("요청사항", esc(q.request)) : ""}
      ${row("접수", `${reqAgo(q.createdAt)} · <b class="${reqExpireAt(q)-Date.now() < 3600e3 ? "rust" : ""}">${reqLeft(q)}</b>`)}
    </div>
    ${w.length ? `<div class="menu-warn" style="margin-top:10px">${w.map(esc).join(" · ")}</div>` : ""}
    <p class="f-note" style="margin-top:10px">승인하면 이 내용으로 예약 등록이 열립니다. 좌석을 고르고 등록하면 손님께 확정 문자가 나갑니다. 24시간 안에 처리하지 않으면 자동 취소되고 손님께 안내 문자가 갑니다.</p>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="reqReject('${q.id}')">거절</button>
      <button class="btn ghost" onclick="openRequests()">목록</button>
      <button class="btn primary" data-enter onclick="reqAccept('${q.id}')">승인 → 예약 등록</button></div>`;
}

/* 승인: 마법사를 요청 내용으로 채워 엽니다. 좌석·알러지 확인은 직원이 마저 합니다 */
function reqAccept(id){
  const q = reqById(id); if(!q) return;
  view.form = null;
  openWizard(q.date);
  if(!WZ){ render(); return; }   /* 읽기 전용(연결 끊김)이면 마법사가 안 열립니다 — 그 안내는 openWizard 가 띄움 */
  const gs = courseGroups();
  const courses = {};
  const m = /^(course|set):(.+)$/.exec(q.course || "");
  if(m){
    /* 사이트 이름('촉 코스' '요리사 추천세트') → 설정의 짧은 이름('촉' '요리사') 로 맞춥니다 */
    const short = m[2].replace(/\s*(코스|세트)$/,"").replace(/추천세트$/,"").trim();
    for(const g of gs){ const it = (g.items||[]).find(x => short.indexOf(x) === 0 || x.indexOf(short) === 0); if(it){ courses[g.id + "|" + it] = q.people; break; } }
  }
  Object.assign(WZ, {
    step:1, source:"기타", sourceDetail:"홈페이지 예약",
    date:q.date, time:q.time, calMonth:q.date.slice(0,7),
    people:q.people, infants:q.kids||0, chairs:0,
    menuType: q.course === "none" ? "해당 없음" : "코스",
    courses, courseUndecided: q.course === "later" || (m && !Object.keys(courses).length),
    seatKind: q.seat === "room" ? "room" : "table",
    name:q.name, phone:q.phone, request:q.request||"",
    memo:`홈페이지 접수 ${q.createdAt.slice(0,16).replace("T"," ")}`,
    reqId:q.id
  });
  /* 방금 그려진 0단계의 경로 입력칸이 비어 있어서 render() 의 wzSyncInputs 가 sourceDetail 을 지웁니다 — 칸에도 넣어 둠 */
  const el = document.getElementById("wz-src-detail"); if(el) el.value = WZ.sourceDetail;
  render();
}
/* 마법사가 등록을 마치면 요청을 확정으로 돌립니다(wzRegister 끝에서 부름) */
function reqAfterRegister(rec){
  if(!WZ || !WZ.reqId) return;
  REQ_API.accept(WZ.reqId, rec.id);
  const q = reqById(WZ.reqId);
  if(q) smsMockSend(q.phone, q.name, `[한옥반점] ${q.name}님, ${dateLabel(q.date)} ${hm(q.time)} ${reqPeopleText(q)} 예약이 확정되었습니다. 문의 ${store().settings.tel || "031-724-1004"}`);
}
async function reqReject(id){
  const q = reqById(id); if(!q) return;
  const reasons = ["그 시간에 자리가 없습니다", "룸은 성인 5명부터 받고 있습니다", "당일·연휴는 전화로 부탁드립니다", "직접 입력"];
  const pick = await uiPick("거절 사유", reasons); if(pick == null) return;
  let why = reasons[pick];
  if(why === "직접 입력"){ why = (prompt("거절 사유") || "").trim(); if(!why) return; }
  await REQ_API.reject(id, why);
  smsMockSend(q.phone, q.name, `[한옥반점] ${q.name}님, 요청하신 ${dateLabel(q.date)} ${hm(q.time)} 예약을 받지 못했습니다. ${why}. 전화 주시면 자리를 찾아드리겠습니다. ${store().settings.tel || "031-724-1004"}`);
  showToast("거절했습니다 · 문자 흉내");
  openRequests();
}
/* 목록 시트에서 고르는 작은 상자 — 없으면 confirm 으로 대신 */
async function uiPick(title, opts){
  if(typeof uiChoose === "function") return uiChoose(title, opts);
  const s = prompt(title + "\n" + opts.map((o,i)=>`${i+1}. ${o}`).join("\n"), "1");
  const n = parseInt(s, 10); return n >= 1 && n <= opts.length ? n - 1 : null;
}

/* 새 홈페이지 예약이 들어오면 화면 위에 알림 — 확인하면 그 창으로, 닫으면 그냥 닫힘.
   실제 연동에서는 갱신(refresh) 때 못 보던 id 가 있으면 reqNotify(newOnes) 를 부르면 됩니다 */
let REQ_SEEN = {};
function reqNotify(list){
  const fresh = list.filter(q => !REQ_SEEN[q.id]); list.forEach(q => REQ_SEEN[q.id] = true);
  if(!fresh.length || view.display) return;
  const q = fresh[0];
  const body = fresh.length === 1
    ? `${dateLabel(q.date)} ${hm(q.time)} · ${reqPeopleText(q)} · ${q.seat==="room"?"룸":"테이블"}\n${q.name} ${q.phone}`
    : `${fresh.length}건이 들어왔습니다. 가장 빠른 것: ${dateLabel(q.date)} ${hm(q.time)} ${q.name}`;
  uiConfirm(fresh.length === 1 ? "새 홈페이지 예약이 들어왔습니다" : `새 홈페이지 예약 ${fresh.length}건`, body, {ok:"확인하기", cancel:"닫기", tone:"ok"})
    .then(ok => { if(ok){ if(WZ) return; view.form = null; fresh.length === 1 ? openRequest(q.id) : openRequests(); } });
}
function reqPush(q){ REQUESTS.push(q); render(); reqNotify([q]); }

/* 흉내 데이터 — 사이트에서 접수한 것처럼 몇 건 넣습니다 */
function reqSeedDemo(){
  const t = todayStr(), d1 = shiftDate(t, 2), d2 = shiftDate(t, 5), d3 = shiftDate(t, 9);
  const now = Date.now();
  const mk = (o) => Object.assign({ id:"q" + Math.random().toString(36).slice(2,8), status:"대기", createdAt:new Date(now - Math.random()*3*3600e3).toISOString() }, o);
  const items = [
    mk({ date:d1, time:"12:30", adults:5, kids:1, people:6, seat:"room", course:"set:요리사 추천세트", courseLabel:"요리사 추천세트", name:"김서연", phone:"010-2233-4455", request:"어린이 의자 하나 부탁드립니다." }),
    mk({ date:d2, time:"18:00", adults:2, kids:0, people:2, seat:"table", course:"none", courseLabel:"단품 주문", name:"박도현", phone:"010-9876-1234", request:"" }),
    mk({ date:d3, time:"19:00", adults:8, kids:0, people:8, seat:"room", course:"later", courseLabel:"메뉴 미정", name:"이준호", phone:"010-5555-0001", request:"회사 회식입니다. 창가 쪽 룸이면 좋겠습니다." }),
    mk({ date:d1, time:"11:30", adults:3, kids:0, people:3, seat:"room", course:"course:위 코스", courseLabel:"위 코스", name:"최민아", phone:"010-4444-7777", request:"" })
  ];
  /* 하나는 곧 만료되는 것으로 — 카운트다운 확인용 */
  items[1].createdAt = new Date(now - (REQ_RULE.expireH*3600e3 - 40*60000)).toISOString();
  REQUESTS.push.apply(REQUESTS, items);
  view.form = null; render(); reqNotify(items);
}

/* 문자 흉내 기록 — '보낸 문자' 목록(smsFreeLog)에 남깁니다. 실제 발송은 업체 연동 뒤 */
function smsMockSend(to, name, text){
  const st = store().settings;
  st.smsFreeLog = [{ at:new Date().toISOString(), to, name, text }].concat(st.smsFreeLog || []).slice(0, 50);
  if(typeof mirrorDraft === "function") mirrorDraft("smsFreeLog");
  logEvent("문자 보내기(흉내)", `${to} ${name} ${text.slice(0, 40)}`);
  saveData();
}
