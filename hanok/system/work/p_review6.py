# -*- coding: utf-8 -*-
"""재아 요청(2026-09-17) 시스템 쪽 — 홈페이지 예약:
   ① 대기 중인 요청을 타임라인에 연회색 블록으로(확정 전 자리 확보). 남은 자리 계산(availOfDay)에도 찬 것으로
   ② 켤 때 대기 건이 있으면 팝업. 문구 "새 홈페이지 예약 N건 / N건의 예약이 접수되었습니다."
   ③ 목록: 접수 순(오래된 것 위), '17시간 전 접수' 삭제, "6시간 38분 후 만료" / 12시간 안이면 빨간 "N시간 M분 남음"
   ④ 줄 순서: 날짜·시간 → 인원 → 룸/테이블 → 메뉴. 경고 '테이블 없음'/'룸 없음'. 알약 작게
   ⑤ 거절: 사유 고르기·직접 입력·생략 되는 시트
   ⑥ 승인 = '예약 확정' 바로 등록. 경고 있으면 팝업 → 그래도 확정 / 예약 창에서 자리 고르기(그 단계로)
   ⑦ 알러지 칸(requests.allergy) 연동
   ⑧ 마법사 '한 화면으로 입력'(빠른 입력) 진입 삭제
   ⑨ 확인 목록에 '사용 중지 좌석에 잡힌 예약' — 날짜 상관없이 오늘 이후 전부 """
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep

# ---------- 11b ----------
s = load("js/11b-requests.js")
s = rep(s, '''function reqPending(){ reqSweep(); return REQUESTS.filter(q => q.status === "대기"); }''',
'''function reqPending(){ reqSweep(); return REQUESTS.filter(q => q.status === "대기").sort((a, b) => (a.createdAt || "").localeCompare(b.createdAt || "")); }   /* 접수 순(오래된 것부터) — 시간 제한이 있으니(재아) */
/* 대기 중인 요청을 예약처럼 — 타임라인에 연회색으로 그리고, 남은 자리 계산에서 찬 것으로 칩니다(확정 전이라도 자리를 잡아 두려고 — 재아).
   좌석은 그때그때 빈 곳을 골라 잠정으로. 실제 예약 표에는 없고 화면·계산에만 잠깐 끼워 넣습니다 */
function reqAsRes(q){
  const f = suggestSeatFull(q.date, q.time, q.people, q.seat === "room" ? "room-any" : "table-any");
  let pref = q.seat === "room" ? "room-any" : "table-any";
  if(q.seat !== "room" && f){ const t = seatById(f.id); if(t && isTable(t)) pref = "table:" + (t.floor || ""); }
  if(q.seat !== "room" && !f){ const fl = tableFloors()[0]; if(fl != null) pref = "table:" + fl; }
  return { id:"req:" + q.id, _req:q, date:q.date, time:q.time, name:q.name, phone:q.phone, people:q.people, infants:q.kids || 0, chairs:0,
           roomId:null, extraIds:[], seatPref:pref, tentativeRoomId:f ? f.id : null, tentativeExtra:f ? (f.extra || []) : [], tentativeSplit:!!(f && f.split),
           source:"기타", sourceDetail:"홈페이지 예약", createdAt:q.createdAt, menuType:"해당 없음", courses:{}, courseUndecided:false,
           allergy:q.allergy || "", allergyChecked:true, request:q.request || "", memo:"", status:"확정", changes:[], sms:[] };
}
function reqPendingOn(date){ return reqPending().filter(q => q.date === date); }
/* fn 을 돌리는 동안만 대기 요청을 예약 표에 끼워 넣습니다 — 남은 자리 계산용 */
function withPendingReqs(date, fn){
  const s = store(), add = reqPendingOn(date).map(reqAsRes);
  if(!add.length) return fn();
  s.reservations.push.apply(s.reservations, add);
  try{ return fn(); }
  finally{ for(let i = s.reservations.length - 1; i >= 0; i--) if(s.reservations[i]._req) s.reservations.splice(i, 1); }
}''', 1)
s = rep(s, '''/* "23시간 10분 남음" — 1시간 아래면 분만, 다 되면 '만료 임박' */
function reqLeft(q){
  const ms = reqExpireAt(q) - Date.now(); if(ms <= 0) return "만료";
  const h = Math.floor(ms / 3600e3), m = Math.floor((ms % 3600e3) / 60000);
  return h ? `${h}시간 ${m}분 남음` : `${m}분 남음`;
}''',
'''/* "6시간 38분 후 만료" — 12시간 안으로 들어오면 빨간 "11시간 59분 남음" (reqLeftClass) */
function reqLeft(q){
  const ms = reqExpireAt(q) - Date.now(); if(ms <= 0) return "만료";
  const h = Math.floor(ms / 3600e3), m = Math.floor((ms % 3600e3) / 60000);
  if(ms < 12 * 3600e3) return h ? `${h}시간 ${m}분 남음` : `${m}분 남음`;
  return `${h}시간 ${m}분 후 만료`;
}
function reqLeftClass(q){ return reqExpireAt(q) - Date.now() < 12 * 3600e3 ? "rust" : ""; }''', 1)
# 경고 문구 + 자리 없음 판단은 '그 요청 빼고 다른 대기 요청까지 찬 것으로'
s = rep(s, '''    if(!free) out.push(q.seat === "room" ? "그 시간에 빈 룸이 없음" : "그 시간에 빈 테이블이 없음");''',
           '''    if(!free) out.push(q.seat === "room" ? "룸 없음" : "테이블 없음");''', 1)
# 목록 줄
s = rep(s, '''  const list = reqPending().sort((a,b) => a.date.localeCompare(b.date) || a.time.localeCompare(b.time));
  const rows = list.length ? list.map(q => {
    const w = reqWarns(q);
    return `<button class="rowitem tap" onclick="openRequest('${q.id}')">
      <span class="grow"><span class="t">${esc(q.name)} <span class="tag">${q.seat==="room"?"룸":"테이블"}</span>${w.length?`<span class="tag rust">${esc(w[0])}</span>`:""}</span>
        <span class="s">${dateLabel(q.date)} ${hm(q.time)} · ${reqPeopleText(q)} · ${esc(reqMenuText(q))}</span></span>
      <span class="s left ${reqExpireAt(q)-Date.now() < 3600e3 ? "soon" : ""}" style="white-space:nowrap; text-align:right">${reqLeft(q)}<br><span class="muted">${reqAgo(q.createdAt)} 접수</span></span>
    </button>`; }).join("")''',
'''  const list = reqPending();   /* 접수 순 */
  const rows = list.length ? list.map(q => {
    const w = reqWarns(q);
    return `<button class="rowitem tap" onclick="openRequest('${q.id}')">
      <span class="grow"><span class="t">${esc(q.name)}${w.length?` <span class="tag rust sm">${esc(w[0])}</span>`:""}</span>
        <span class="s">${dateLabel(q.date)} ${hm(q.time)} · ${reqPeopleText(q)} · ${q.seat==="room"?"룸":"테이블"} · ${esc(reqMenuText(q))}</span></span>
      <span class="s left ${reqLeftClass(q)}" style="white-space:nowrap; text-align:right">${reqLeft(q)}</span>
    </button>`; }).join("")''', 1)
# 상세
s = rep(s, '''      ${row("날짜", `${dateLabel(q.date)} ${hm(q.time)}`)}
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
      <button class="btn primary" data-enter onclick="reqAccept('${q.id}')">승인 → 예약 등록</button></div>`;''',
'''      ${row("날짜", `${dateLabel(q.date)} ${hm(q.time)}`)}
      ${row("인원", q.kids ? `성인 ${q.adults} · 어린이 ${q.kids}` : `성인 ${q.adults}`)}
      ${row("자리", q.seat === "room" ? "룸" : "테이블")}
      ${row("메뉴", esc(reqMenuText(q)))}
      ${row("예약자", `${esc(q.name)} · ${esc(q.phone)}`)}
      ${q.allergy ? row("알레르기", `<span class="rust">${esc(q.allergy)}</span>`) : ""}
      ${q.request ? row("요청사항", esc(q.request)) : ""}
      ${row("만료", `<b class="${reqLeftClass(q)}">${reqLeft(q)}</b>`)}
    </div>
    ${w.length ? `<div class="menu-warn" style="margin-top:10px">${w.map(esc).join(" · ")}</div>` : ""}
    <p class="f-note" style="margin-top:10px">'예약 확정' 을 누르면 이 내용 그대로 예약이 등록되고(자리는 빈 곳으로 잠정 배정) 손님께 확정 문자가 나갑니다. 경고가 있으면 먼저 알려 드립니다. 24시간 안에 처리하지 않으면 자동 취소됩니다.</p>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="openReqReject('${q.id}')">거절</button>
      <button class="btn ghost" onclick="openRequests()">목록</button>
      <button class="btn primary" data-enter onclick="reqAccept('${q.id}')">예약 확정</button></div>`;''', 1)
# 승인: 바로 확정. 경고 있으면 팝업 → 그래도 확정 / 예약 창(마법사)
s = rep(s, '''/* 승인: 마법사를 요청 내용으로 채워 엽니다. 좌석·알러지 확인은 직원이 마저 합니다 */
function reqAccept(id){
  const q = reqById(id); if(!q) return;
  view.form = null;
  openWizard(q.date);
  if(!WZ){ render(); return; }   /* 읽기 전용(연결 끊김)이면 마법사가 안 열립니다 — 그 안내는 openWizard 가 띄움 */
  const gs = courseGroups();''',
'''/* 요청의 코스 이름('촉 코스' '요리사 추천세트') → 설정 항목('cg_dinner|촉') */
function reqCourses(q){
  const gs = courseGroups(q.date), courses = {};
  const m = /^(course|set):(.+)$/.exec(q.course || "");
  if(m){
    const short = m[2].replace(/\\s*(코스|세트)$/,"").replace(/추천세트$/,"").trim();
    for(const g of gs){ const it = (g.items||[]).find(x => short.indexOf(x) === 0 || x.indexOf(short) === 0); if(it){ courses[g.id + "|" + it] = q.people; break; } }
  }
  return { courses, matched: !!(m && Object.keys(courses).length), isCourse: q.course !== "none" };
}
/* 예약 확정: 요청 내용 그대로 바로 등록(자리는 빈 곳으로 잠정). 경고가 있으면 먼저 팝업 —
   그래도 확정 / 예약 창에서 자리 고르기(마법사 좌석 단계로) / 취소 (재아) */
async function reqAccept(id){
  const q = reqById(id); if(!q) return;
  if(readonlyBlock && readonlyBlock()) return;
  const warns = reqWarns(q);
  const pr = reqAsRes(q);   /* 잠정 좌석 계산 */
  if(!pr.tentativeRoomId) warns.push(q.seat === "room" ? "빈 룸이 없어 미배정으로 들어갑니다" : "빈 테이블이 없어 자리 없음으로 들어갑니다");
  const cr = reqCourses(q);
  if(cr.isCourse && !cr.matched && q.course !== "later") warns.push(`코스 이름을 설정에서 못 찾음 (${q.courseLabel}) — 미정으로 넣습니다`);
  if(warns.length){
    const pick = await uiChoose("확인이 필요합니다", ["그래도 예약 확정", "예약 창에서 직접 고르기"], warns.join("\\n"));
    if(pick == null) return;
    if(pick === 1){ reqAcceptWizard(id, 3); return; }
  }
  const st = store().settings;
  const rec = {
    id:newId("res"), date:q.date, time:q.time, name:q.name, phone:phoneNorm(q.phone),
    people:q.people, infants:q.kids || 0, chairs:(typeof chairDefaultInfants === "function" && chairDefaultInfants()) ? (q.kids || 0) : 0,
    roomId:null, extraIds:[], seatPref:pr.seatPref, tentativeRoomId:pr.tentativeRoomId, tentativeSplit:pr.tentativeSplit, tentativeExtra:pr.tentativeExtra,
    source:"기타", sourceDetail:"홈페이지 예약", createdAt:new Date().toISOString(),
    menuType: q.course === "none" ? "해당 없음" : "코스", courses:cr.courses, courseUndecided: q.course === "later" || (cr.isCourse && !cr.matched),
    allergy:(q.allergy || "").trim(), allergyChecked:true, request:(q.request || "").trim(),
    memo:`홈페이지 접수 ${(q.createdAt || "").slice(0,16).replace("T"," ")}`, status:"확정"
  };
  createReservation(rec);
  await REQ_API.accept(q.id, rec.id);
  smsMockSend(q.phone, q.name, `[한옥반점] ${q.name}님, ${dateLabel(q.date)} ${hm(q.time)} ${reqPeopleText(q)} 예약이 확정되었습니다. 문의 ${st.tel || "031-724-1004"}`);
  saveData();
  showToast(`${q.name} 예약 확정 · 문자 흉내`, "보기", () => goRes(rec.id, rec.date));
  view.form = null; render();
  if(reqPending().length) openRequests();
}
/* 예약 창(마법사)으로 — 요청 내용을 채워 열고, 원하는 단계로 */
function reqAcceptWizard(id, step){
  const q = reqById(id); if(!q) return;
  view.form = null;
  openWizard(q.date);
  if(!WZ){ render(); return; }   /* 읽기 전용(연결 끊김)이면 마법사가 안 열립니다 — 그 안내는 openWizard 가 띄움 */
  const gs = courseGroups();''', 1)
s = rep(s, '''  Object.assign(WZ, {
    step:1, source:"기타", sourceDetail:"홈페이지 예약",''',
           '''  Object.assign(WZ, {
    step:step || 1, maxStep:step || 1, source:"기타", sourceDetail:"홈페이지 예약",''', 1)
s = rep(s, '''    name:q.name, phone:q.phone, request:q.request||"",
    memo:`홈페이지 접수 ${q.createdAt.slice(0,16).replace("T"," ")}`,''',
           '''    name:q.name, phone:q.phone, request:q.request||"", allergy:q.allergy||"", allergyNone:!(q.allergy||"").trim(),
    memo:`홈페이지 접수 ${q.createdAt.slice(0,16).replace("T"," ")}`,''', 1)
# 거절 시트
s = rep(s, '''async function reqReject(id){
  const q = reqById(id); if(!q) return;
  const reasons = ["그 시간에 자리가 없습니다", "룸은 성인 5명부터 받고 있습니다", "당일·연휴는 전화로 부탁드립니다", "직접 입력"];
  const pick = await uiPick("거절 사유", reasons); if(pick == null) return;
  let why = reasons[pick];
  if(why === "직접 입력"){ why = (prompt("거절 사유") || "").trim(); if(!why) return; }
  await REQ_API.reject(id, why);
  smsMockSend(q.phone, q.name, `[한옥반점] ${q.name}님, 요청하신 ${dateLabel(q.date)} ${hm(q.time)} 예약을 받지 못했습니다. ${why}. 전화 주시면 자리를 찾아드리겠습니다. ${store().settings.tel || "031-724-1004"}`);
  showToast("거절했습니다 · 문자 흉내");
  openRequests();
}''',
'''/* 거절 — 사유를 고르거나 직접 적거나 생략. 문자에 사유가 들어갑니다 */
const REQ_REASONS = ["그 시간에 자리가 없습니다", "룸은 성인 5명부터 받고 있습니다", "당일·연휴는 전화로 부탁드립니다", "단체는 전화로 부탁드립니다"];
function openReqReject(id){ view.form = {type:"reqrej", id}; view.reqRej = {pick:0, text:""}; render(); }
function sheetReqReject(){
  const q = reqById(view.form.id); if(!q) return sheetRequests();
  const d = view.reqRej || {pick:0, text:""};
  return `
    ${sheetHead("거절")}
    <p class="f-note" style="margin:-6px 0 12px">${esc(q.name)} · ${dateLabel(q.date)} ${hm(q.time)} · ${reqPeopleText(q)}. 손님께 거절 문자가 나갑니다(사유는 넣어도, 안 넣어도 됩니다).</p>
    <div class="rj-list">
      ${REQ_REASONS.map((r, i) => `<label class="chk"><input type="radio" name="rj" ${d.pick === i ? "checked" : ""} onchange="view.reqRej.pick=${i}; render()"><span>${esc(r)}</span></label>`).join("")}
      <label class="chk"><input type="radio" name="rj" ${d.pick === -1 ? "checked" : ""} onchange="view.reqRej.pick=-1; render()"><span>직접 입력</span></label>
      ${d.pick === -1 ? `<textarea class="in-sm" rows="2" placeholder="사유" oninput="view.reqRej.text=this.value">${esc(d.text)}</textarea>` : ""}
    </div>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="openRequest('${q.id}')">돌아가기</button>
      <button class="btn ghost" onclick="reqReject('${q.id}', '')">사유 없이 거절</button>
      <button class="btn primary" data-enter onclick="reqReject('${q.id}')">거절하기</button></div>`;
}
async function reqReject(id, whyGiven){
  const q = reqById(id); if(!q) return;
  let why = whyGiven;
  if(why === undefined){ const d = view.reqRej || {pick:0, text:""}; why = d.pick === -1 ? (d.text || "").trim() : REQ_REASONS[d.pick]; if(d.pick === -1 && !why){ await uiAlert("사유를 적어 주세요", "사유 없이 거절하려면 '사유 없이 거절' 을 누르세요.", "warn"); return; } }
  await REQ_API.reject(id, why || "");
  smsMockSend(q.phone, q.name, `[한옥반점] ${q.name}님, 요청하신 ${dateLabel(q.date)} ${hm(q.time)} 예약을 받지 못했습니다.${why ? " " + why + "." : ""} 전화 주시면 자리를 찾아드리겠습니다. ${store().settings.tel || "031-724-1004"}`);
  showToast("거절했습니다 · 문자 흉내");
  view.reqRej = null; openRequests();
}''', 1)
# 팝업 문구
s = rep(s, '''  const q = fresh[0];
  const body = fresh.length === 1
    ? `${dateLabel(q.date)} ${hm(q.time)} · ${reqPeopleText(q)} · ${q.seat==="room"?"룸":"테이블"}\\n${q.name} ${q.phone}`
    : `${fresh.length}건이 들어왔습니다. 가장 빠른 것: ${dateLabel(q.date)} ${hm(q.time)} ${q.name}`;
  uiConfirm(fresh.length === 1 ? "새 홈페이지 예약이 들어왔습니다" : `새 홈페이지 예약 ${fresh.length}건`, body, {ok:"확인하기", cancel:"닫기", tone:"ok"})
    .then(ok => { if(ok){ if(WZ) return; view.form = null; fresh.length === 1 ? openRequest(q.id) : openRequests(); } });
}''',
'''  const q = fresh[0];
  uiConfirm(`새 홈페이지 예약 ${fresh.length}건`, `${fresh.length}건의 예약이 접수되었습니다.`, {ok:"확인하기", cancel:"닫기", tone:"ok"})
    .then(ok => { if(ok){ if(WZ) return; view.form = null; fresh.length === 1 ? openRequest(q.id) : openRequests(); } });
}
/* 켤 때 이미 대기 중인 건이 있으면 — 새로 들어온 것은 아니지만 처리해야 하니 한 번 알림(재아) */
function reqNotifyPending(){
  const pend = reqPending(); if(!pend.length || view.display) return;
  pend.forEach(q => { REQ_SEEN[q.id] = true; });
  uiConfirm(`홈페이지 예약 대기 ${pend.length}건`, `${pend.length}건의 예약이 확정을 기다리고 있습니다.`, {ok:"확인하기", cancel:"닫기", tone:"ok"})
    .then(ok => { if(ok){ if(WZ) return; view.form = null; openRequests(); } });
}''', 1)
# 홈페이지 요청 흉내 시드에 allergy 없음 → 그대로. rowToReq 는 11c
save("js/11b-requests.js", s)

# ---------- 11c: allergy, 켤 때 팝업, 남은 자리에 대기 요청 반영 ----------
s = load("js/11c-site-link.js")
s = rep(s, '''           course:x.course, courseLabel:x.course_label, name:x.name, phone:phoneFmtReq(x.phone), request:x.request||"",''',
           '''           course:x.course, courseLabel:x.course_label, name:x.name, phone:phoneFmtReq(x.phone), request:x.request||"", allergy:x.allergy||"",''', 1)
s = rep(s, '''  if(fresh.length && REQ_SEEN_INIT) reqNotify(fresh); else fresh.forEach(q => { REQ_SEEN[q.id] = true; });
  REQ_SEEN_INIT = true;''',
'''  if(REQ_SEEN_INIT){ if(fresh.length) reqNotify(fresh); }
  else { reqNotifyPending(); }   /* 처음 불러온 것: 새 건은 아니지만 대기 중이면 알림 */
  REQ_SEEN_INIT = true;''', 1)
s = rep(s, '''function availOfDay(date){
  const out = {}, ss = sessionsFor(date); if(!ss.length) return out;''',
'''function availOfDay(date){
  /* 대기 중인 홈페이지 요청도 찬 것으로 — 확정 전이라도 그 자리를 다른 손님에게 안 내주려고(재아) */
  if(typeof withPendingReqs === "function") return withPendingReqs(date, function(){ return availOfDayRaw(date); });
  return availOfDayRaw(date);
}
function availOfDayRaw(date){
  const out = {}, ss = sessionsFor(date); if(!ss.length) return out;''', 1)
save("js/11c-site-link.js", s)

# ---------- 시트 등록 ----------
s = load("js/15-sheets.js")
s = rep(s, "reqs:sheetRequests, req:sheetRequest, sched2:sheetScheduled, site:sheetSite /*", "reqs:sheetRequests, req:sheetRequest, reqrej:sheetReqReject, sched2:sheetScheduled, site:sheetSite /*", 1)
save("js/15-sheets.js", s)

# ---------- 타임라인: 대기 요청을 연회색 블록으로 ----------
s = load("js/10-timeline.js")
s = rep(s, '''  const list = s.reservations.filter(r=>r.date===date && holdsSeat(r));''',
           '''  const list = s.reservations.filter(r=>r.date===date && holdsSeat(r))
    .concat(typeof reqPendingOn === "function" ? reqPendingOn(date).map(reqAsRes) : []);   /* 대기 중인 홈페이지 요청 — 연회색(확정 전 자리 확보, 재아) */''', 1)
# 룸 블록
s = rep(s, '''      return `<button class="blk ${tent?'tent':''} ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''} ${it.joined?'joined':''}" onclick="openMark('${it.r.id}')"''',
           '''      return `<button class="blk ${tent?'tent':''} ${it.r._req?'req':''} ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''} ${it.joined?'joined':''}" onclick="${it.r._req?`openRequest('${it.r._req.id}')`:`openMark('${it.r.id}')`}"''', 1)
# 테이블 블록
s = rep(s, '''      return `<button class="blk ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''} ${it.need>1?'multi':''} ${split?'split':''}" onclick="openMark('${it.r.id}')"''',
           '''      return `<button class="blk ${it.r._req?'req':''} ${bad?'warned':''} ${past?'past':''} ${chg?'changed':''} ${it.need>1?'multi':''} ${split?'split':''}" onclick="${it.r._req?`openRequest('${it.r._req.id}')`:`openMark('${it.r.id}')`}"''', 1)
s = rep(s, '''  const blockLabel = r =>
    `<b>${esc(r.time)}</b> ${esc(r.name)} ${pplOf(r)}명${r.infants?`(어린이${r.infants})`:""}`;''',
'''  const blockLabel = r =>
    `${r._req?`<i class="rq">홈페이지</i> `:""}<b>${esc(r.time)}</b> ${esc(r.name)} ${pplOf(r)}명${r.infants?`(어린이${r.infants})`:""}${r._req?" · 확정 전":""}`;''', 1)
save("js/10-timeline.js", s)

s = load("css/05-dash.css")
s = rep(s, '''.blk.tent{background-image:repeating-linear-gradient(-45deg, rgba(255,255,255,.34) 0 4px, transparent 4px 10px); border:1px dashed rgba(255,255,255,.75)}''',
'''.blk.tent{background-image:repeating-linear-gradient(-45deg, rgba(255,255,255,.34) 0 4px, transparent 4px 10px); border:1px dashed rgba(255,255,255,.75)}
/* 확정 전 홈페이지 예약 — 연회색, 누르면 그 요청 창. 자리를 미리 잡아 둔 것이라 다른 블록과 같은 자리에 그려집니다 */
.blk.req, .blk.req.tent{background:#E3E0D8; background-image:none; color:#3A3833; border:1px dashed #8C8578}
.blk.req .rq{font-style:normal; font-weight:700; color:var(--rust); font-size:10px}''', 1)
save("css/05-dash.css", s)

s = load("css/03-parts.css")
s = rep(s, '''.tag.blue{background:var(--blue-soft); color:var(--blue); border-color:var(--blue-line)}''',
'''.tag.blue{background:var(--blue-soft); color:var(--blue); border-color:var(--blue-line)}
.tag.sm{padding:1px 6px; font-size:11px; font-weight:600}   /* 목록 줄 안의 작은 꼬리표(홈페이지 예약 경고 등) */
.rj-list{display:flex; flex-direction:column; gap:var(--s8); margin-bottom:var(--s8)}
.rj-list .chk{margin:0}
.rj-list textarea{width:100%}''', 1)
save("css/03-parts.css", s)

# ---------- 마법사: '한 화면으로 입력' 삭제 ----------
s = load("js/16-wizard.js")
s = rep(s, '''    <button class="linkbtn wz-quick" onclick="openQuick()">한 화면으로 입력</button>`;''', '''`;   /* '한 화면으로 입력'(빠른 입력)은 2026-09-17 뺐습니다 — 경고가 안 보여 오히려 불편(재아). openQuick 은 남겨 둠 */''', 1)
save("js/16-wizard.js", s)

# ---------- 확인 목록: 사용 중지 좌석에 잡힌 예약(오늘 이후 전부) ----------
s = load("js/09-sms.js")
s = rep(s, '''  const un = list.filter(isUnassigned);   /* 테이블 예약은 층이 자리 — 미배정 아님 */''',
'''  /* 사용 중지 좌석에 잡힌 예약 — 날짜 상관없이 오늘 이후 전부. 미리 연락하거나 자리를 옮겨야 하니(재아) */
  const blk = s.reservations.filter(r=>r.date>=today && holdsSeat(r) && resBlocked(r)).sort((a,b)=>a.date.localeCompare(b.date)||a.time.localeCompare(b.time));
  if(blk.length) items.push(["rust", `사용 중지 좌석에 잡힌 예약 ${blk.length}건`,
    blk.slice(0,3).map(r=>`${dateLabel(r.date)} ${r.time} ${r.name} · ${resSeatLabel(r)}`).join(", "), `openPick('blocked')`]);

  const un = list.filter(isUnassigned);   /* 테이블 예약은 층이 자리 — 미배정 아님 */''', 1)
s = rep(s, '''    auto:{title:"어제 자동 방문 처리", pick:null, note:""}
  }[kind];
  const list = kind==="auto"
    ? autoClosedList(shiftDate(today,-1))
    : s.reservations.filter(r=>r.date===d && (kind==="changed" || r.status==="확정") && conf.pick(r))
        .sort((a,b)=>a.time.localeCompare(b.time));''',
'''    auto:{title:"어제 자동 방문 처리", pick:null, note:""},
    blocked:{title:"사용 중지 좌석에 잡힌 예약", pick:null, note:"그 좌석은 그 기간 쓸 수 없습니다. 미리 연락해 다른 자리로 옮기거나 사용 중지를 풀어 주세요. 오늘 이후 전부입니다."}
  }[kind];
  const list = kind==="auto"
    ? autoClosedList(shiftDate(today,-1))
    : kind==="blocked"
    ? s.reservations.filter(r=>r.date>=today && holdsSeat(r) && resBlocked(r)).sort((a,b)=>a.date.localeCompare(b.date)||a.time.localeCompare(b.time))
    : s.reservations.filter(r=>r.date===d && (kind==="changed" || r.status==="확정") && conf.pick(r))
        .sort((a,b)=>a.time.localeCompare(b.time));''', 1)
s = rep(s, '''      <span class="time-col">${esc(r.time)}</span>
      <span class="grow"><span class="t">${esc(r.name)}</span>
        <span class="s">${pplText(r)}${r.phone?` · ${esc(r.phone)}`:""}${''',
'''      <span class="time-col">${esc(r.time)}</span>
      <span class="grow"><span class="t">${esc(r.name)}</span>
        <span class="s">${kind==="blocked"?`${dateLabel(r.date)} · `:""}${pplText(r)}${r.phone?` · ${esc(r.phone)}`:""}${
          kind==="blocked"&&resBlocked(r)?` · ${esc(blockLabelText(resBlocked(r).blk))}`:""}${''', 1)
save("js/09-sms.js", s)
print("ok")
