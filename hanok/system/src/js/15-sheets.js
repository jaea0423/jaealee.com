/* ============================================================
   입력 시트 (예약 / 직원 / 근태)
   ============================================================ */
function openRes(id){ if(readonlyBlock()) return; histPush(); view.form={type:"res", id}; render(); }
function openMark(id){ view.form={type:"mark", id}; view.pickSeat=null; render(); }
/* 누르면 바로 배정되던 것을 '고르기 → 확정하기' 두 단계로 나눴습니다.
   태블릿에서 손이 스쳐 엉뚱한 방에 배정되는 사고를 막습니다. */
function pickSeatCand(resId, seatId){ view.pickSeat = seatId || null; render(); }
function openUnassigned(){ view.form={type:"unassigned"}; render(); }

/* ---------- 네이버 예약 가져오기 (8차-M) ----------
   네이버 파트너센터 '예약자 관리' 엑셀을 열어 표 전체를 복사(Ctrl+A, Ctrl+C)해 붙여 넣습니다. 탭으로 나뉜 줄이 들어옵니다.
   머리글 줄(예약번호 · 상태 · 예약자 · 이용일시 · 상품 · 인원 · 옵션 · 요청사항 …)을 찾아 열 이름으로 읽으므로 열 순서가 바뀌어도 됩니다.
   · 예약번호(naverNo)로 같은 예약을 찾아 있으면 고치고(상태·시각·인원·요청) 없으면 새로 넣습니다
   · 전화번호는 뒷자리 4개만 오므로 phone 은 비우고 메모에 '네이버 ****1234' 를 남깁니다 — 노쇼 이력은 못 잇습니다
   · 상품에 '룸' 이 있으면 룸 미정(room-any), '테이블' 이면 테이블(층 미정, table-any). 자리는 잠정 배정이 잡습니다
   · 옵션 열(주말 A 세트·주말 B 세트·한코스 …)은 수량이 있으면 코스 구성으로. 이름이 코스 항목과 안 맞으면 요청사항에 적어 둡니다 */
function openNaver(){
  /* 엑셀을 다녀와야 하므로 전체화면이면 잠시 풀고, 닫을 때 되돌립니다(재아) */
  view.fsWas = !!document.fullscreenElement;
  if(view.fsWas && document.exitFullscreen) document.exitFullscreen().catch(function(){});
  view.form = {type:"naver", page:true}; view.naver = {text:"", result:null}; render(); window.scrollTo(0,0);
}
function sheetNaver(){
  const n = view.naver || {text:"", result:null};
  /* 행마다: 건너뛰기 · 좌석 고르기(룸 미정/특정 룸/테이블). 자리 경고가 있으면 붉은 줄 — 등록 전에 손볼 수 있게(재아) */
  const st = store().settings;
  const seatOpts = (x) => `<select class="nv-seat" onchange="view.naver.result[${x.n-1}].seat=this.value">
      <option value="room-any" ${x.seat==="room-any"?"selected":""}>룸 미정(자동)</option>
      ${st.rooms.filter(isRoom).map(rm=>`<option value="${rm.id}" ${x.seat===rm.id?"selected":""}>${esc(rm.name)} 룸</option>`).join("")}
      <option value="table-any" ${x.seat==="table-any"?"selected":""}>테이블(층 상관없음)</option>
      ${tableFloors().map(fl=>`<option value="table:${fl}" ${x.seat==="table:"+fl?"selected":""}>${esc(floorLabel(fl))}</option>`).join("")}
    </select>`;
  const res = n.result ? `<div class="bulk-res">${n.result.map(x=>`<div class="bulk-row ${x.ok?(x.kind==="skip"?"":(x.seatWarn||x.request?"warn":"ok")):"bad"} ${x.skip?"skipped":""}"><span class="bulk-ln">${x.n}</span><span class="grow">${esc(x.text)}${x.request?`<div class="nv-req">요청: ${esc(x.request)}</div>`:""}${x.ok&&x.kind==="new"?`<div class="nv-ctl"><label class="chk" style="margin:0"><input type="checkbox" ${x.skip?"checked":""} onchange="view.naver.result[${x.n-1}].skip=this.checked"><span>건너뛰기</span></label>${seatOpts(x)}</div>`:""}</span><span class="bulk-msg">${x.ok?`${x.kind==="new"?"＋ 새로":x.kind==="update"?"↻ 고침":"＝ 같음"} · ${esc(x.msg)}`:`✗ ${esc(x.msg)}`}</span></div>`).join("")}</div>` : "";
  const cnt = k => n.result ? n.result.filter(x=>x.ok && x.kind===k).length : 0;
  return `
    ${sheetHead("네이버 예약 가져오기")}
    <p class="f-note" style="margin:-6px 0 10px">네이버 파트너센터 → 예약자 관리 → 엑셀 다운로드 → 파일을 열어 <b>표 전체 복사(Ctrl+A, Ctrl+C)</b> → 아래에 붙여 넣기(Ctrl+V).</p>
    <textarea id="naver-paste" rows="7" placeholder="여기에 붙여 넣으세요 (머리글 줄 포함, 안내 문장이 섞여 있어도 됩니다)" oninput="view.naver={text:this.value, result:null}">${esc(n.text)}</textarea>
    <div class="btn-row" style="margin-top:8px">
      <button class="btn" data-enter onclick="naverPreview()">확인</button>
      ${n.result ? `<button class="btn primary" data-enter onclick="naverApply()" ${cnt("new")+cnt("update")?"":"disabled"}>신규 ${cnt("new")}건 · 수정 ${cnt("update")}건 · 등록</button>` : ""}
      <button class="btn ghost" style="margin-left:auto" onclick="closeSheet()">닫기</button>
    </div>
    ${res}`;
}
/* '26. 8. 17.(월) 오후 12:00' → {date:"2026-08-17", time:"12:00"} */
function naverWhen(s){
  const m = String(s||"").match(/(\d{2,4})\.\s*(\d{1,2})\.\s*(\d{1,2})\.?[^0-9]*?(오전|오후)?\s*(\d{1,2}):(\d{2})/);
  if(!m) return null;
  let y = Number(m[1]); if(y < 100) y += 2000;
  let h = Number(m[5]); const ap = m[4];
  if(ap === "오후" && h < 12) h += 12; if(ap === "오전" && h === 12) h = 0;
  return { date: `${y}-${pad(Number(m[2]))}-${pad(Number(m[3]))}`, time: `${pad(h)}:${m[6]}` };
}
/* '4명/성인(3),어린이(1)' → {people:4, infants:1} */
function naverPeople(s){
  const t = String(s||""); const tot = t.match(/(\d+)\s*명/); const kid = t.match(/(?:어린이|유아|아동)\((\d+)\)/);
  return { people: tot ? Number(tot[1]) : 0, infants: kid ? Number(kid[1]) : 0 };
}
/* 엑셀에서 복사한 표는 탭으로 나뉘고, 셀 안에 줄바꿈이 있으면 그 셀을 큰따옴표로 감쌉니다(안의 " 는 "").
   줄 단위로 자르면 요청사항에 엔터가 든 손님이 통째로 사라졌습니다 — 글자 단위로 따옴표 상태를 보며 자릅니다 */
function tsvRows(text){
  const rows = []; let row = [], cell = "", q = false;
  for(let i = 0; i < text.length; i++){
    const c = text[i];
    if(q){
      if(c === '"'){ if(text[i+1] === '"'){ cell += '"'; i++; } else q = false; }
      else cell += c;
    }else{
      if(c === '"' && cell === "") q = true;
      else if(c === "\t"){ row.push(cell); cell = ""; }
      else if(c === "\n" || c === "\r"){ if(c === "\r" && text[i+1] === "\n") i++; row.push(cell); rows.push(row); row = []; cell = ""; }
      else cell += c;
    }
  }
  if(cell !== "" || row.length) { row.push(cell); rows.push(row); }
  return rows.filter(r=>r.some(x=>x.trim()));
}
function naverParse(text){
  const table = tsvRows(text);
  const hi = table.findIndex(r=>r.some(x=>x.trim()==="예약번호") && r.length > 3);
  if(hi < 0) return {err:"머리글 줄(예약번호 … 이용일시 … 인원)을 못 찾았습니다. 엑셀에서 표 전체를 복사해 붙여 넣으세요."};
  const head = table[hi].map(x=>x.trim());
  const col = name => head.findIndex(h=>h === name);
  const idx = { no:col("예약번호"), status:col("상태"), name:col("예약자"), phone:col("전화번호"), when:col("이용일시"), prod:col("상품"), ppl:col("인원"), req:col("요청사항"), memo:col("직원메모"), cancelWhy:col("취소사유"), route:col("유입경로"),
                visitor:col("방문자"), visitorPhone:col("방문자전화번호"), made:col("예약신청일시"), black:col("블랙리스트등록여부") };
  if(idx.no < 0 || idx.when < 0) return {err:"예약번호·이용일시 열이 필요합니다"};
  /* 옵션 열: '옵션1-주말 A 세트' 처럼 이름이 붙은 것 중 '결제금액' 이 아닌 것 */
  const opts = head.map((h,i)=>({h,i})).filter(x=>/^옵션\d+-/.test(x.h) && !/결제금액$/.test(x.h)).map(x=>({i:x.i, name:x.h.replace(/^옵션\d+-/,"").replace(/^한옥반점\s*/,"").trim()}));
  const st = store().settings, groups = st.courseGroups || DEFAULT_COURSE_GROUPS;
  const rows = [];
  for(let k = hi + 1; k < table.length; k++){
    const c = table[k]; if(c.length < head.length - 5) continue;
    const g = i => i >= 0 && i < c.length ? String(c[i]||"").trim() : "";
    const no = g(idx.no); if(!/^\d{5,}$/.test(no)) continue;
    const when = naverWhen(g(idx.when)); const pp = naverPeople(g(idx.ppl));
    const stRaw = g(idx.status), prod = g(idx.prod);
    const status = /취소|거절/.test(stRaw) ? "취소" : /이용완료|완료/.test(stRaw) ? "방문" : /노쇼|미방문/.test(stRaw) ? "노쇼" : "확정";
    const isRoomProd = /룸/.test(prod);
    /* 옵션 수량 → 코스. 이름이 코스 항목(A·B·한 등)과 맞는 것만 */
    const courses = {}; const unmatched = [];
    opts.forEach(o=>{ const q = Number(g(o.i)) || 0; if(!q) return;
      if(/테이블 예약|룸 예약/.test(o.name)) return;   /* 자리 옵션은 코스가 아님 */
      const gid = when && when.time >= "17:00" ? "cg_dinner" : (when && isWeekendDay(when.date) ? "cg_welunch" : "cg_wdlunch");
      const grp = groups.find(x=>x.id===gid) || groups[0];
      const item = (grp.items||[]).find(it=>o.name.replace(/\s|세트|코스/g,"").indexOf(it) >= 0 || it.indexOf(o.name.replace(/\s|세트|코스/g,"")) >= 0);
      if(item) courses[grp.id + "|" + item] = (courses[grp.id + "|" + item] || 0) + q; else unmatched.push(`${o.name} ${q}`);
    });
    /* 방문자(대리 예약)가 있으면 그 이름·전화가 실제 손님. 전화가 가려지지 않고 온 경우(9자리 이상 숫자)만 phone 에 넣습니다 */
    const vName = g(idx.visitor), vPhone = g(idx.visitorPhone).replace(/\D/g,""), mPhone = g(idx.phone).replace(/\D/g,"");
    const fullPhone = vPhone.length >= 9 ? vPhone : (mPhone.length >= 9 ? mPhone : "");
    const madeRaw = g(idx.made), mm = madeRaw.match(/(\d{4})-(\d{2})-(\d{2})[^0-9]*(오전|오후)?\s*(\d{1,2}):(\d{2})/);
    let made = null; if(mm){ let h = Number(mm[5]); if(mm[4]==="오후" && h < 12) h += 12; if(mm[4]==="오전" && h === 12) h = 0; made = new Date(`${mm[1]}-${mm[2]}-${mm[3]}T${pad(h)}:${mm[6]}:00`).toISOString(); }
    rows.push({ n: rows.length + 1, text: `${no} · ${g(idx.name)} · ${g(idx.when)} · ${g(idx.ppl)} · ${prod} · ${stRaw}`,
      no, when, name: vName || g(idx.name) || "네이버 손님", phone: fullPhone ? phoneFmt(fullPhone) : "", phoneTail: fullPhone ? "" : (g(idx.phone).match(/(\d{4})\s*$/) || [,""])[1],
      status, isRoomProd, people: pp.people, infants: pp.infants, courses, unmatched, request: g(idx.req), cancelWhy: g(idx.cancelWhy),
      route: g(idx.route), staffMemo: g(idx.memo), made, black: /^Y/i.test(g(idx.black)) });
  }
  return { rows, headFound: true };
}
function naverPreview(){
  const ta = document.getElementById("naver-paste"); const text = ta ? ta.value : (view.naver ? view.naver.text : "");
  const p = naverParse(text);
  if(p.err){ view.naver = {text, result:[{n:1, text:"", ok:false, msg:p.err}]}; render(); return; }
  const s = store();
  const result = p.rows.map(r=>{
    if(!r.when) return {n:r.n, text:r.text, ok:false, msg:"이용일시를 못 읽었습니다"};
    if(!r.people) return {n:r.n, text:r.text, ok:false, msg:"인원을 못 읽었습니다"};
    const all = s.reservations.concat(s.trash||[]);
    let ex = all.find(x=>x.naverNo === r.no) || all.find(x=>!x.naverNo && (x.memo||"").indexOf(r.no) >= 0);   /* 직접 넣으며 메모에 예약번호를 적어 둔 건 */
    let linked = false;
    if(!ex){
      /* 같은 날·같은 시각·같은 인원으로 직접 넣은 네이버 예약이 있으면 중복이 아니라 같은 건으로 봅니다(재아: 중복 잡기) */
      const cand = s.reservations.filter(x=>!x.naverNo && x.date===r.when.date && x.time===r.when.time && pplOf(x)===r.people && x.status!=="취소");
      const same = cand.find(x=>/네이버/.test(x.source||"")) || cand.find(x=>x.name && r.name && x.name.charAt(0)===r.name.charAt(0));
      if(same){ ex = same; linked = true; }
    }else if(!ex.naverNo) linked = true;
    if(!ex){
      /* 등록 전 자리 경고 — 룸 미정이면 빈 룸이 있는지, 테이블이면 앉힐 수 있는지 */
      let seatWarn = "";
      if(r.status === "확정"){
        if(r.isRoomProd){ if(!findSeat({date:r.when.date, time:r.when.time, people:r.people, kind:"room-any"})) seatWarn = "빈 룸 없음"; }
        else { const ff = floorFit(null, r.when.date, r.when.time, r.people); if(ff.state === "none") seatWarn = "테이블 자리 없음"; else if(ff.state === "split") seatWarn = "나눠 앉음"; }
      }
      return Object.assign({ok:true, kind:"new", seatWarn, seat: r.isRoomProd ? "room-any" : "table-any", skip:false,
        msg:`${r.when.date} ${r.when.time} ${r.people}명${r.status!=="확정"?" · "+r.status:""}${r.request?" · ⚠ 요청사항 있음":""}${seatWarn?" · ⚠ "+seatWarn:""}`}, r);
    }
    const diff = [];
    if(ex.date !== r.when.date || ex.time !== r.when.time) diff.push("시각");
    if(pplOf(ex) !== r.people) diff.push("인원");
    if(ex.status !== r.status) diff.push("상태 " + ex.status + "→" + r.status);
    if((ex.request||"") !== (r.request||"") && r.request) diff.push("요청");
    if(linked) diff.unshift(`직접 넣은 예약(${ex.name})과 같은 건으로 연결`);
    if(!diff.length) return Object.assign({ok:true, kind:"skip", msg:"바뀐 것 없음"}, r);
    return Object.assign({ok:true, kind:"update", msg:diff.join(" · "), exId:ex.id, link:linked}, r);
  });
  view.naver = {text, result}; render();
}
async function naverApply(){
  const n = view.naver; if(!n || !n.result) return;
  if(readonlyBlock()) return;
  const s = store(); let added = 0, updated = 0;
  n.result.filter(x=>x.ok && x.kind !== "skip" && !x.skip).forEach(r=>{
    const memoTail = `네이버 예약번호 ${r.no}${r.phoneTail?` · 전화 ****${r.phoneTail}`:""}${r.infants?" · 유아의자 확인 필요":""}${r.black?" · ⚠ 네이버 블랙리스트":""}${r.unmatched.length?` · 옵션 ${r.unmatched.join(", ")}`:""}${r.staffMemo?` · 직원메모: ${r.staffMemo}`:""}${r.cancelWhy?` · 취소사유: ${r.cancelWhy}`:""}`;
    if(r.kind === "new"){
      const pick = r.seat || (r.isRoomProd ? "room-any" : "table-any"), pickedRoom = seatById(pick) ? pick : null;
      const rec = { id:newId("res"), naverNo:r.no, date:r.when.date, time:r.when.time, name:r.name, phone:r.phone||"", phoneTail:r.phoneTail||"", people:r.people, infants:r.infants, chairs:0,
        roomId:pickedRoom, extraIds:[], seatPref: pickedRoom ? null : pick, tentativeRoomId:null, tentativeExtra:[], tentativeSplit:false,
        source:"네이버 예약", sourceDetail:r.route||"", createdAt:r.made||new Date().toISOString(),
        menuType: Object.keys(r.courses).length ? "코스" : (r.isRoomProd ? "확인 필요" : "해당 없음"), courses:r.courses, courseUndecided:false,
        allergy:"", allergyChecked:false, request:r.request||"", memo:memoTail, status:r.status, changes:[], sms:[] };
      createReservation(rec); added++;
    }else{
      const ex = s.reservations.find(x=>x.id===r.exId) || (s.trash||[]).find(x=>x.id===r.exId); if(!ex) return;
      const d = [];
      if(r.link){ ex.naverNo = r.no; if((ex.memo||"").indexOf(r.no) < 0) ex.memo = ((ex.memo||"").replace(/네이버 예약번호:\s*$/,"").trim() + " · " + memoTail).replace(/^ · /,""); if(r.phone && !ex.phone) ex.phone = r.phone; }
      if(ex.date !== r.when.date || ex.time !== r.when.time){ d.push({n:"시각", a:ex.date+" "+ex.time, b:r.when.date+" "+r.when.time}); ex.date = r.when.date; ex.time = r.when.time; }
      if(pplOf(ex) !== r.people){ d.push({n:"인원", a:pplOf(ex), b:r.people}); ex.people = r.people; ex.infants = r.infants; }
      if(r.request && ex.request !== r.request){ d.push({n:"요청"}); ex.request = r.request; }
      if(ex.status !== r.status){ if(r.status==="취소"||r.status==="노쇼") addChange(ex, r.status, []); else d.push({n:"상태", a:ex.status, b:r.status}); ex.status = r.status; }
      if(d.length) addChange(ex, "변경", d); else touch(ex);
      reflowTentatives(ex.date); updated++;
    }
  });
  logEvent("네이버 가져오기", `신규 ${added} · 수정 ${updated}`);
  view.naver = null; view.form = null; saveData(); render();
  uiAlert("네이버 예약 가져오기 완료", `신규 ${added}건, 수정 ${updated}건. 룸 예약은 '룸 미정' 으로 들어와 잠정 배정이 잡습니다 — 좌석 미정 목록에서 확정하세요.`, "ok");
}

function openNoshow(){ view.form={type:"noshow"}; render(); }
function openSearch(){ view.form={type:"search"}; render(); }
function openPin(){ view.form={type:"pin"}; render(); }
async function openPinManage(){ if(!await adminGate("PIN 번호 관리")) return; view.form={type:"pinlist"}; render(); }
function sheetPinList(){
  return `
    ${sheetHead("PIN 번호 관리")}
    <div class="rowitem"><span class="grow"><span class="t">공용 <span class="tag pine">사용 중</span></span><span class="s">직원 모두가 쓰는 PIN · 로그에는 '공용(staff)' 으로 남습니다</span></span>
      <button class="btn sm" onclick="openPin()">번호 바꾸기</button></div>
    <div class="btn-row" style="margin-top:12px"><button class="btn" disabled title="직원별 PIN 은 서버 계정을 하나씩 만들어야 해서 다음 단계에서">＋ 직원 PIN 추가 (준비 중)</button></div>
    <p class="f-note">직원마다 다른 PIN 을 만들면 로그에 이름이 남고, 그만두면 그 PIN 만 지우면 됩니다. 서버 쪽 준비가 필요해 지금은 공용 하나입니다. 추가·삭제할 때도 관리자 비밀번호를 한 번 더 묻게 만듭니다.</p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
function openAdminPw(){ view.form={type:"apw"}; render(); }
async function openLogs(){ if(!await adminGate("접속 기록")) return; view.form={type:"logs"}; render(); }
function openSmsLog(){ view.form={type:"smslog"}; view.smsOpen = {}; render(); }
/* 예약률 시트는 자기 커서(view.rateEnd)로 주를 옮깁니다. 6차 전에는 moveDate(±7) 로 메인 날짜를 밀어서
   시트를 닫으면 대시보드가 엉뚱한 주에 가 있었습니다. 열 때 view.date 로 시작하고 닫으면 view.date 는 그대로 */
function openRate(){ view.rateEnd = view.date; view.form={type:"rate"}; render(); }
function rateMove(n){ view.rateEnd = shiftDate(view.rateEnd || view.date, n); render(); }
function openSchedule(from){
  const st = store().settings;
  const base = from ? (st.schedules||[]).find(s=>s.from===from) : scheduleFor(todayStr());
  view.schedDraft = {
    from: from || todayStr(), origFrom: from || null,
    isNew: !from,
    days: deepClone(base ? base.days : DEFAULT_DATA.hanok.settings.schedules[0].days),
    holiday: deepClone(base && base.holiday ? base.holiday : DEFAULT_DATA.hanok.settings.schedules[0].holiday)
  };
  view.form={type:"sched"}; render();
}
function openOverride(){ view.form={type:"ovr"}; view.ovrBulk = null; render(); }
function closeSheet(){
  if(typeof thGuard === "function" && thGuard()) return;   /* 감사 문자 AI 진행 중엔 못 나감(09-20) */
  var was = view.form && view.form.type === "res", wasNaver = view.form && view.form.type === "naver";
  view.form=null; tmpRes=null; view.pickAll=false; view.pickSeat=null; render(); if(was) histPop();
  if(wasNaver && view.fsWas){ view.fsWas = false; tryFullscreenForce(); }   /* 닫기 버튼 클릭이 손짓이라 여기서는 됩니다 */
}
function tryFullscreenForce(){ try{ var el = document.documentElement; if(!document.fullscreenElement && el.requestFullscreen) el.requestFullscreen().catch(function(){}); }catch(e){} }
/* ---------- 토스트 ----------
   showToast(text, actionLabel, fn) — 같은 자리 하나뿐. 새로 부르면 앞 것을 교체합니다.
   구형 TV 브라우저에서도 죽지 않게 setTimeout 만 씁니다 */
var TOAST_T = null, TOAST_FN = null;
function showToast(text, actionLabel, fn){
  var el = document.getElementById("toast");
  if(!el){ el = document.createElement("div"); el.id = "toast"; el.className = "toast"; document.body.appendChild(el); }
  TOAST_FN = fn || null;
  el.innerHTML = '<span class="toast-t"></span>' + (actionLabel ? '<button class="toast-a" onclick="toastAction()"></button>' : '');
  el.querySelector(".toast-t").textContent = text;
  if(actionLabel) el.querySelector(".toast-a").textContent = actionLabel;
  el.className = "toast on";
  if(TOAST_T) clearTimeout(TOAST_T);
  TOAST_T = setTimeout(hideToast, actionLabel ? 6000 : 4000);   /* 3초는 너무 금방 사라짐(재아 09-17). '보기' 같은 버튼이 있으면 더 길게 */
}
function hideToast(){ var el = document.getElementById("toast"); if(el) el.className = "toast"; TOAST_T = null; }
function toastAction(){ var fn = TOAST_FN; hideToast(); if(fn) fn(); }
/* 예약을 저장한 뒤 — 보고 있는 날짜의 예약이면 이미 보이니 '저장됨' 만, 다른 날짜면 '9/20(금) 예약 저장됨 · 보기' */
function toastSaved(rec){
  if(!rec) return;
  if(rec.date === view.date && view.tab !== "settings"){ showToast("저장됨"); return; }
  var d = new Date(rec.date + "T00:00:00");
  var label = (d.getMonth()+1) + "/" + d.getDate() + "(" + ["일","월","화","수","목","금","토"][d.getDay()] + ") 예약 저장됨";
  showToast(label, "보기", function(){ view.date = rec.date; view.tab = "dash"; render(); });
}

function renderSheet(){
  const inner = { res:sheetRes, mark:sheetMark, unassigned:sheetUnassigned, pick:sheetPick, check:sheetCheck, search:sheetSearch, num:sheetNum, noshow:sheetNoshow, pin:sheetPin, apw:sheetAdminPw, hours:sheetHours, tedit:sheetTableEdit, naver:sheetNaver, setlog:sheetSetLog, pinlist:sheetPinList, zoomadj:sheetZoomAdj, logs:sheetLogs, smslog:sheetSmsLog, smsfree:sheetSmsFree, rate:sheetRate, sched:sheetSchedule, ovr:sheetOverride, blocks:sheetBlocks, reqs:sheetRequests, req:sheetRequest, reqrej:sheetReqReject, sched2:sheetScheduled, site:sheetSite, staff:sheetStaff, guests:sheetGuests, owner:sheetOwner, thanks:sheetThanks, devreq:sheetDevReq, closeday:sheetCloseDay }[view.form.type]();   /* staff·guests 는 14d·14e(15차) */
  /* 검색은 창 높이를 고정해 두고 결과만 안에서 스크롤 — 칠 때마다 창이 늘었다 줄었다 하지 않게(재아) */
  const wide = view.form.type==="rate" ? " sheet-wide" : ((view.form.type==="search" || (view.form.type==="reqs" && reqPending().length >= 3)) ? " sheet-tall" : "");   /* 홈페이지 예약은 3건부터 높이를 고정하고 목록만 스크롤(재아 09-17). 0~2건이면 빈 상자를 길게 안 보임(검토 D3) */
  if(view.form.page) return `<div class="sheet page-sheet">${inner}</div>`;   /* 화면형: 덮개 없이 본문 자리에 */
  return `<div class="overlay" onclick="closeSheet()"><div class="sheet${wide}" onclick="event.stopPropagation()">${inner}</div></div>`;
}
function sheetHead(title){
  if(view.form && view.form.page) return `<div class="sheet-h"><h2>${title}</h2></div>`;   /* 화면형은 상단바에 X 가 있음 */
  return `<div class="sheet-h"><h2>${title}</h2><button class="x" onclick="closeSheet()" aria-label="닫기">×</button></div>`;
}

/* ---------- 예약 ---------- */
let tmpRes = null;   // 시트가 열려 있는 동안의 임시 값 (경로·상태 버튼 선택용)
function sheetRes(){
  const s=store(), st=s.settings;
  const editing = view.form.id ? s.reservations.find(r=>r.id===view.form.id) : null;
  if(!tmpRes || tmpRes.__id !== (view.form.id||"new")){
    tmpRes = editing
      ? {...editing, __id:editing.id}
      /* 빠른 입력(openQuick) — 시각·인원·경로를 비워 두어 마법사처럼 직접 고르게 합니다. 필수는 시각·인원·이름 */
      : {__id:"new", date:(view.form.date||view.date), time:"", name:"", phone:"", people:0, infants:0,
         chairs:0, roomId:"", source:"", sourceDetail:"", request:"", allergy:"", status:"확정",
         menuType:"해당 없음", courses:{}, courseUndecided:false};
  }
  const f = tmpRes;
  /* 룸 / 테이블 / 합침 묶음. 합침은 대표+extraIds 로 저장되며 select 값은 그룹 id */
  const curJoin = (f.extraIds||[]).length ? joinOf([f.roomId].concat(f.extraIds)) : null;
  const opt = (v, label, sel) => `<option value="${v}" ${sel?'selected':''}>${label}</option>`;
  const roomOpts = `<optgroup label="룸">${roomsAt(f.date).filter(isRoom).map(r=>opt(r.id, `${esc(r.name)} · ${roomMin(r, f.date)}~${r.capacity}인`, !curJoin && f.roomId===r.id)).join("")}</optgroup>` +
    `<optgroup label="룸 합침">${joinsAt(f.date).map(j=>opt(j.id, `${esc(seatLabel(j.id))} · ${j.min}~${j.max}인`, !!curJoin && curJoin.id===j.id)).join("")}</optgroup>` +
    `<optgroup label="테이블 (층만)">${tableFloors().map(fl=>opt("table:"+fl, `${esc(floorLabel(fl))} · 자리 ${floorSeats(fl)}석`, !f.roomId && f.seatPref==="table:"+fl)).join("")}</optgroup>` +
    `<optgroup label="특정 테이블 (파셜룸 등 꼭 잡아야 할 때)">${roomsAt(f.date).filter(isTable).map(r=>opt(r.id, `${esc(r.floor||"")} ${esc(r.name)} · ${roomMin(r)?roomMin(r)+"~":""}${seatMax(r)}인`, !curJoin && f.roomId===r.id)).join("")}</optgroup>` +
    ((f.extraIds||[]).length && !curJoin ? `<optgroup label="현재">${opt("__keep", esc(seatLabelIds([f.roomId].concat(f.extraIds))) + " (붙임 유지)", true)}</optgroup>` : "");
  const srcs = [...new Set([...(st.sources||["전화 예약","네이버 예약","기타"]), f.source||"전화 예약"])];
  const srcSeg = srcs.map(x=>`<button class="${f.source===x?'on':''}" onclick="pickSource('${jsq(x)}')">${esc(x)}</button>`).join("");
  const stSeg = STATUS.map(x=>`<button class="${f.status===x?'on':''}" onclick="pickStatus('${x}')">${x}</button>`).join("");

  /* 식사 — 마법사 5단계와 같은 규칙을 씁니다.
     테이블은 보통 메뉴를 정하지 않고 받으므로 선택지를 줄입니다. */
  const seatObj = st.rooms.find(x=>x.id===f.roomId);
  const isHall = seatObj ? isTable(seatObj) : isTablePref(f.seatPref);
  const seatIsRoom = seatObj ? seatObj.type==="room" : false;   /* 전역 isRoom(x) 헬퍼와 이름이 겹쳐 시트가 통째로 죽었습니다 — 이름을 바꿈 */
  const baseMenuOpts = isHall ? ["코스","해당 없음"] : ["코스","코스 상당","확인 필요","해당 없음"];
  /* 테이블로 옮긴 예약에 '확인 필요' 같은 값이 남아 있으면 버튼이 사라져 보이지 않게 되므로 살려 둡니다 */
  const menuOpts = f.menuType && baseMenuOpts.indexOf(f.menuType)<0
    ? baseMenuOpts.concat([f.menuType]) : baseMenuOpts;
  const cN = courseCount();
  const cAd = adultCount(pplOf(f), f.infants||0);
  /* 룸은 코스 주문을 전제로 받는 자리입니다 — 막지 않고 알리기만 합니다 */
  const menuWarn = seatIsRoom && (
    f.menuType==="해당 없음" ? "룸 예약에 코스·세트 이용 예정 손님이 아닙니다" :
    f.menuType==="확인 필요" ? "" :
    (f.menuType==="코스" && !f.courseUndecided && cN>0 && cN<cAd)
      ? `코스·세트 ${cN}인분 · 성인 ${cAd}명보다 적습니다` : "");
  const menuSeg = menuOpts.map(x=>
    `<button class="${f.menuType===x?'on':''}" onclick="pickMenuType('${x}')">${x==="코스"?"코스·세트":x}</button>`).join("");

  return `
    ${sheetHead(editing?"예약 내용 수정":"빠른 입력")}
    <div class="grid2">
      <div class="f"><div class="lb">날짜</div><button class="numbtn ${f.pickDate?'on':''}" onclick="syncRes(); tmpRes.pickDate=!tmpRes.pickDate; tmpRes.pickTime=false; render()">${f.date?dateLabel(f.date):"날짜 고르기"}</button></div>
      <div class="f"><div class="lb">시간</div><button class="numbtn ${f.pickTime?'on':''}" onclick="syncRes(); tmpRes.pickTime=!tmpRes.pickTime; tmpRes.pickDate=false; render()">${f.time?hm(f.time):"시각 고르기"}</button></div>
    </div>
    <input id="f-date" type="hidden" value="${f.date||""}"><input id="f-time" type="hidden" value="${f.time||""}">
    ${f.pickDate ? `<div class="card" style="padding:8px; margin-bottom:12px">${miniCal(f.date, "resPickDate")}</div>` : ""}
    ${f.pickTime ? `<div class="card" style="padding:8px; margin-bottom:12px">${f.date ? timeGrid({date:f.date, people:f.people||0, time:f.time, pick:"resPickSlot"}) : `<div class="empty">날짜를 먼저 고르세요</div>`}
      ${store().settings.minuteSteps !== false && f.time ? `<div class="btn-row" style="margin-top:8px"><button class="btn sm" onclick="resNudge(-5)">− 5분</button><span class="lbl-note">${hm(f.time)}</span><button class="btn sm" onclick="resNudge(5)">＋ 5분</button></div>` : ""}</div>` : ""}
    <div class="grid2">
      <label class="f"><div class="lb">예약자</div><input id="f-name" value="${esc(f.name)}" placeholder="홍길동" autocomplete="off"></label>
      <label class="f"><div class="lb">전화번호</div><input id="f-phone" type="tel" inputmode="numeric" value="${esc(f.phone)}" placeholder="010-0000-0000"></label>
    </div>
    <div class="grid2">
      <label class="f"><div class="lb">총 인원 (어린이 포함)</div>
        <input id="f-people" type="number" min="1" value="${pplOf(f)}"></label>
      <label class="f"><div class="lb">어린이</div>
        <input id="f-infants" type="number" min="0" value="${f.infants||0}"></label>
    </div>
    <label class="f"><div class="lb">좌석</div>
      <select id="f-room" onchange="pickRoom(this.value)"><option value="">미배정</option>${roomOpts}</select></label>
    <div class="f"><div class="lb">경로</div><div class="seg">${srcSeg}</div>
      <div id="src-detail" style="margin-top:8px; display:${f.source==="기타"?"block":"none"}">
        <input id="f-src-detail" value="${esc(f.sourceDetail||"")}" placeholder="예: 지인 소개">
      </div>
    </div>
    <div class="f"><div class="lb">식사</div>
      ${menuWarn?`<div class="menu-warn" style="margin:0 0 8px">${esc(menuWarn)}</div>`:""}
      <div class="seg">${menuSeg}</div>
      ${f.menuType==="코스"?`
        <div class="course-sum" style="margin-top:10px">
          <span>${f.courseUndecided ? "코스·세트 미정 — 방문 전 확정"
            : (cN?`${esc(courseSummary(f.courses))}`:"구성을 고르세요")}</span>
          <button class="btn sm" style="margin-left:auto" onclick="openCourse()">${cN||f.courseUndecided?"수정":"선택"}</button>
        </div>`:""}
    </div>
    ${f.allergy?`<label class="f"><div class="lb">알러지 <span class="lbl-note">옛 예약</span></div><input id="f-allergy" value="${esc(f.allergy)}"></label>`:""}
    <label class="f"><div class="lb">요청사항</div><input id="f-request" value="${esc(f.request||'')}" placeholder="예: 갑각류 알러지 1명, 유아용 의자, 송별회"></label>
    <label class="f"><div class="lb">메모 <span class="lbl-note">선택</span></div>
      <input id="f-memo" value="${esc(f.memo||'')}" placeholder="예: 사장님 지인, 상석 준비"></label>
    <div class="f"><div class="lb">상태</div><div class="seg">${stSeg}</div></div>
    <div class="sheet-actions">
      ${editing?`<button class="btn danger" onclick="delRes('${editing.id}')">삭제</button>`:""}
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="saveRes()">${editing?"저장":"등록"}</button>
    </div>`;
}
function step(id,d){
  const el=document.getElementById(id);
  el.value = Math.max(0,(parseInt(el.value)||0)+d);
}
function pickSource(x){ syncRes(); tmpRes = {...tmpRes, source:x}; render(); }
/* render 직전에 renderApp 이 입력칸(hidden f-date/f-time)을 다시 읽어 상태를 덮으므로, 값을 칸에도 먼저 써 둡니다 */
function setHidden(id, v){ const el = document.getElementById(id); if(el) el.value = v; }
function resPickDate(d){ syncRes(); tmpRes = Object.assign({}, tmpRes, {date:d, pickDate:false, calMonth:d.slice(0,7)}); setHidden("f-date", d); render(); }
function resPickSlot(t){ syncRes(); const v = minToHM(t); tmpRes = Object.assign({}, tmpRes, {time:v, pickTime:false}); setHidden("f-time", v); render(); }
function resNudge(d){ syncRes(); if(!tmpRes.time) return; const m = Math.max(0, Math.min(23*60+55, toMin(tmpRes.time) + d)); const v = minToHM(m); tmpRes = Object.assign({}, tmpRes, {time:v}); setHidden("f-time", v); render(); }
function resCalMove(d){ syncRes(); const [y,m] = (tmpRes.calMonth || tmpRes.date || todayStr()).slice(0,7).split("-").map(Number); const nd = new Date(y, m-1+d, 1); tmpRes = Object.assign({}, tmpRes, {calMonth:`${nd.getFullYear()}-${pad(nd.getMonth()+1)}`}); render(); }
/* 작은 달력 — 빠른 입력·수정 시트용. 마법사 달력과 같은 칸(일자·막대·건수) */
function miniCal(sel, pickFn){
  const s = store(), today = todayStr();
  const ym = (tmpRes && tmpRes.calMonth) || (sel || today).slice(0,7);
  const [y,m] = ym.split("-").map(Number);
  const first = new Date(y, m-1, 1), lastDay = new Date(y, m, 0).getDate(), lead = first.getDay();
  let cells = "";
  for(let i=0;i<lead;i++) cells += `<span class="bday"></span>`;
  for(let d=1; d<=lastDay; d++){
    const ds = `${y}-${pad(m)}-${pad(d)}`;
    const n = s.reservations.filter(r=>r.date===ds && r.status==="확정").length;
    const dow = new Date(ds+"T00:00:00").getDay();
    const rt = n ? dayStat(ds).rate : 0;
    cells += `<button class="bday btn-day ${sel===ds?'sel':''} ${ds===today?'today':''} ${ds<today?'past':''} ${dow===0?'sun':dow===6?'sat':''} ${hoursFor(ds).closed?'closed':''}" onclick="${pickFn}('${ds}')">
      <span class="d">${d}</span>${n?`<span class="b">${n}건</span><span class="obar"><i style="width:${rt}%" class="${rt>=70?'hi':rt>=40?'mid':''}"></i></span>`:""}</button>`;
  }
  return `<div class="wz-cal mini">
      <div class="bnav-row"><button class="nav" onclick="resCalMove(-1)">‹</button><b>${y}년 ${m}월</b><button class="nav" onclick="resCalMove(1)">›</button></div>
      <div class="bgrid bhead">${["일","월","화","수","목","금","토"].map((x,i)=>`<span class="${i===0?'sun':i===6?'sat':''}">${x}</span>`).join("")}</div>
      <div class="bgrid">${cells}</div>
    </div>`;
}
/* 좌석을 바꾸면 식사 선택지(홀은 2개·룸은 4개)와 경고가 달라져 바로 다시 그립니다 */
function pickRoom(v){
  syncRes();
  const j = (store().settings.joins||[]).find(g=>g.id===v);
  if(v === "__keep") return render();
  if(j) tmpRes = Object.assign({}, tmpRes, {roomId:j.ids[0], extraIds:j.ids.slice(1)});
  else if(/^table:/.test(v)) tmpRes = Object.assign({}, tmpRes, {roomId:null, extraIds:[], seatPref:v});   /* 층만 */
  else if(v === "") tmpRes = Object.assign({}, tmpRes, {roomId:null, extraIds:[], seatPref:"room-any"});
  else  tmpRes = Object.assign({}, tmpRes, {roomId:v, extraIds:[]});
  render();
}
/* 식사 종류를 바꿈. 코스가 아니면 코스 구성을 비웁니다 — 남겨 두면 저장될 때 섞입니다 */
function pickMenuType(v){
  syncRes();
  tmpRes = {...tmpRes, menuType:v};
  if(v==="코스"){ tmpRes.courseOpen = true; }
  else { tmpRes.courses = {}; tmpRes.courseUndecided = false; tmpRes.courseOpen = false; }
  render();
}
function pickStatus(x){ syncRes(); tmpRes = {...tmpRes, status:x}; render(); }
/* 버튼을 눌러 화면을 다시 그리기 전에, 입력창에 친 값을 임시 객체에 옮겨 담음 */
function syncRes(){
  const g=id=>{const el=document.getElementById(id); return el?el.value:undefined;};
  const v = {};
  [["date","f-date"],["time","f-time"],["name","f-name"],["phone","f-phone"],
   ["sourceDetail","f-src-detail"],["request","f-request"],["allergy","f-allergy"],
   ["memo","f-memo"]]
    .forEach(([k,id])=>{ const x=g(id); if(x!==undefined) v[k]=x; });
  [["people","f-people"],["infants","f-infants"]]
    .forEach(([k,id])=>{ const x=g(id); if(x!==undefined) v[k]=Math.max(0,parseInt(x)||0); });
  tmpRes = {...tmpRes, ...v};
}
/* 저장하기 전에 걸리는 문제를 모아 돌려줍니다.
   마법사는 단계마다 물어보지만 수정 화면은 한 번에 물어야 하므로 목록으로 만듭니다.
   ※ 예전에는 수정 화면에만 이 검사가 통째로 없었습니다. 손님이 시간을 바꿔 달라고 할 때
      이미 찬 방이어도 조용히 저장되어, 통화를 끊은 뒤에야 발견했습니다. */
function saveIssues(rec, excludeId){
  const st = store().settings, out = [];
  const w = timeBlock(rec.date, rec.time);
  if(w) out.push.apply(out, w.split("\n"));
  const ids = rec.roomId ? [rec.roomId].concat(rec.extraIds||[]) : [];
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
    else if(ad < seatsMin(ids, rec.date)) out.push(`${label} 최소 인원 ${seatsMin(ids, rec.date)}명에 못 미칩니다 (지금 ${ad}명)`);
    const j = ids.length > 1 ? joinOf(ids) : null;
    if(j && j.note) out.push(`${label}: ${j.note}`);
  }
  /* 경고 판정(resWarn)과 같은 기준으로 — 여기서 안 물어본 것이 저장 뒤 '경고 예약'으로 뜨면 사장님이 놀랍니다.
     (재아 발견: 어린이를 총 인원까지 올려 저장하니 경고는 붙는데 확인창이 없었음 — '성인 없음' 이 빠져 있었습니다)
     시각·좌석 겹침·정원은 위에서 자세한 문장으로 이미 넣었으므로 나머지만 옮깁니다 */
  const words = {
    "성인 없음": `어린이 ${rec.infants||0}명이 총 인원 ${pplOf(rec)}명과 같습니다 — 성인이 없습니다`,
    "룸·코스·세트 아님": `룸 예약인데 식사가 '해당 없음' 입니다`,
    "코스·세트 미확정": `코스·세트가 '확인 필요' 상태입니다`,
    "코스·세트 인원 부족": `코스·세트 인원이 성인 수보다 적습니다`,
    "2인석 배정": `4인석이 없어 2인석에 앉게 됩니다 (2인석은 좁습니다)`,
    "테이블 자리 없음": `${seatLabel(rec.seatPref)}에 그 시간 ${pplOf(rec)}명이 앉을 자리가 없습니다 (한 자리 최대 ${floorMaxParty(prefFloor(rec.seatPref), rec.date, rec.time, excludeId)}명)`,
    "나눠 앉음": `${seatLabel(rec.seatPref)}에 붙일 수 있는 테이블이 없어 나눠 앉게 됩니다 (한 자리 최대 ${floorMaxParty(prefFloor(rec.seatPref), rec.date, rec.time, excludeId)}명)`
  };
  if(!rec.roomId && isTablePref(rec.seatPref)){
    /* 저장 전 객체라 잠정 배정이 아직 없습니다 — 즉석에서 계산해 넣고 경고를 뽑습니다 */
    const ff = floorFit(prefFloor(rec.seatPref), rec.date, rec.time, pplOf(rec), excludeId);
    rec.tentativeRoomId = ff.f ? ff.f.id : null; rec.tentativeExtra = ff.f ? ff.f.extra : []; rec.tentativeSplit = ff.state === "split";
  }
  resWarn(rec).forEach(k => { if(words[k]) out.push(words[k]); });
  if((rec.infants||0) > pplOf(rec)) out.push(`어린이 ${rec.infants}명이 총 인원 ${pplOf(rec)}명보다 많습니다`);
  if(rec.menuType === "코스" && !rec.courseUndecided && !Object.keys(rec.courses||{}).some(k=>rec.courses[k] > 0))
    out.push("코스·세트인데 구성이 비어 있습니다 — '코스·세트 미정' 으로 두거나 구성을 넣으세요");
  return out;
}
async function saveRes(){
  syncRes();
  const s=store(), f=tmpRes;
  if(!(f.name||"").trim()) return uiAlert("예약자 성함을 입력하세요","","warn");
  /* 날짜 검사가 없어서, 날짜 칸을 비우고 저장하면 date:"" 가 저장되고
     화면 날짜가 'NaN월 NaN일' 이 되어 달력으로도 복구가 안 됐습니다. */
  if(!/^\d{4}-\d{2}-\d{2}$/.test(f.date||"")) return uiAlert("날짜를 입력하세요","","warn");
  if(!f.time) return uiAlert("시간을 입력하세요","","warn");
  if(!(f.people > 0)) return uiAlert("인원을 입력하세요","1명 이상이어야 합니다","warn");
  /* 어린이 > 총원은 마법사처럼 막지 않고 아래 saveIssues 에서 경고만 합니다(점검 R8 — 2-4 원칙) */
  const old = view.form.id ? s.reservations.find(r=>r.id===view.form.id) : null;
  const rec = {
    ...(old||{}),
    id: view.form.id || newId("res"),
    date:f.date, time:f.time, name:(f.name||"").trim(), phone:phoneNorm(f.phone),
    people: Math.max(1, f.people||1), infants: f.infants||0, chairs: f.chairs||0,
    roomId: f.roomId || null,
    extraIds: f.roomId ? (f.extraIds || []) : [],
    seatPref: f.roomId ? null : (f.seatPref || (old ? old.seatPref : "room-any")),
    tentativeRoomId: f.roomId ? null : (old ? old.tentativeRoomId : null),
    tentativeExtra: f.roomId ? [] : (old ? (old.tentativeExtra || []) : []),
    tentativeSplit: f.roomId ? false : (old ? !!old.tentativeSplit : false),
    source:f.source || "전화 예약", sourceDetail:f.source==="기타"?(f.sourceDetail||"").trim():"",
    request:(f.request||"").trim(), allergy:(f.allergy||"").trim(), memo:(f.memo||"").trim(),
    allergyChecked: old ? old.allergyChecked : true,   /* 마법사와 같은 모양 */
    menuType: f.menuType || "해당 없음",
    /* 코스가 아니면 구성은 비워 둡니다 — '해당 없음'인데 코스 인원이 남는 일을 막습니다 */
    courses: f.menuType==="코스" ? {...(f.courses||{})} : {},
    courseUndecided: f.menuType==="코스" ? !!f.courseUndecided : false,
    status:f.status,
    createdAt: old ? old.createdAt : new Date().toISOString()
  };
  delete rec.__id; delete rec.adults; delete rec.courseOpen; delete rec.pickDate; delete rec.pickTime; delete rec.calMonth;
  if(old && old.date !== rec.date) delete rec.auto;   /* 자동 방문 표시는 그 날짜의 것 — 옮기면 지웁니다(점검 R10) */

  /* 막지 않고 알리기만 합니다 (설계 5.2). 그대로 저장하면 경고 예약으로 남습니다. */
  const issues = saveIssues(rec, view.form.id);
  if(issues.length){
    const ok = await uiConfirm("이대로 저장할까요?",
      issues.map(x=>`· ${x}`).join("\n") +
      "\n\n저장해도 됩니다. 대신 '경고 예약'으로 남아 확인에 뜹니다.",
      {ok:"그래도 저장", cancel:"다시 고치기"});
    if(!ok) return;
  }

  if(old && old.status !== "취소" && rec.status === "취소"){ const ans = await askNoshowOnCancel(old); if(ans == null) return; rec.status = ans; }
  if(old){
    /* 무엇이 바뀌었는지 남깁니다 (사장님의 '파란 글씨' — 변동 이력 참고) */
    const d = diffRes(old, rec);
    if(d.length) addChange(rec, "변경", d);
    if(old.status !== rec.status && (rec.status==="취소" || rec.status==="노쇼"))
      addChange(rec, rec.status, []);
    s.reservations = s.reservations.map(r=>r.id===rec.id?rec:r);
    logEvent("예약 수정", `${rec.date} ${rec.time} ${rec.name} ${pplOf(rec)}명`);
    /* 날짜를 옮겼으면 원래 날짜의 잠정 배정도 다시 계산해야 합니다 —
       안 그러면 비어 버린 자리를 계속 피한 채로 남습니다 */
    if(old.date !== rec.date) reflowTentatives(old.date);
    reflowTentatives(rec.date);
  }else{
    /* 빠른 입력 — 마법사와 같은 등록 경로 (같은 번호·노쇼 확인 포함) */
    if(!await confirmNewRes(rec.date, rec.phone)) return;
    createReservation(rec);
  }
  /* 6차 전에는 여기서 view.date = rec.date 로 그 날짜로 점프했습니다 — 다음 주 예약을 받다가 화면이 다음 주로 가 버려서
     '오늘' 을 놓치는 일이 있었습니다. 화면은 그대로 두고 토스트의 '보기' 로만 갑니다 */
  view.form=null; tmpRes=null;
  saveData(); render(); histPop();
  toastSaved(rec);
}
async function delRes(id){
  if(readonlyBlock()) return;
  const s=store();
  const rec = s.reservations.find(r=>r.id===id);
  /* 무엇을 지우는지 한 줄 — 목록에서 옆 줄을 잘못 누른 경우를 여기서 잡습니다 */
  const who = rec ? `${resLine(rec)}\n` : "";
  if(!await uiConfirm2(`이 예약을 삭제할까요? 기록이 완전히 사라집니다.\n${who}손님이 취소한 경우라면 '예약 취소'를 쓰는 편이 좋습니다.`)) return;
  if(rec) logEvent("예약 삭제", `${rec.date} ${rec.time} ${rec.name} ${rec.phone ? "…" + rec.phone.replace(/\D/g,"").slice(-4) : ""}`);
  /* 진짜로 지우지 않습니다. 삭제 표시를 붙여 trash 로 옮깁니다.
     여러 기기가 같은 DB 를 쓸 때, 지웠다는 사실 자체가 전달돼야 다른 기기에서 되살아나지 않습니다.
     화면 코드는 s.reservations 만 보므로 동작은 전과 같습니다. */
  if(rec){
    rec.deletedAt = new Date().toISOString(); touch(rec);
    s.trash = (s.trash || []).concat([rec]);
    /* 휴지통은 500건까지만 들고 있되, 아직 서버에 못 보낸 삭제는 버리지 않습니다 — 버리면 서버에서 되살아납니다(점검 D12) */
    if(s.trash.length > 500){
      const keep = s.trash.filter(x=>SYNC && SYNC.res && SYNC.res[x.id] && JSON.stringify(x) !== SYNC.res[x.id]);
      s.trash = keep.concat(s.trash.filter(x=>keep.indexOf(x) < 0).slice(-(500 - keep.length)));
    }
  }
  s.reservations=s.reservations.filter(r=>r.id!==id);
  if(rec) reflowTentatives(rec.date);
  view.form=null; tmpRes=null; saveData(); render(); histPop();
}

/* 예약 상세에 붙는 문자 칸 — 나갔는지, 언제 나가는지, 왜 안 나가는지 */
function smsBox(r){
  const c = smsCfg();
  const sent = smsFind(r, "접수");
  const rs = remindState(r);
  const stamp = m => {
    const d = new Date(m.at);
    return isNaN(d) ? "" : `${d.getMonth()+1}/${d.getDate()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
  };
  const planTxt = rs.at
    ? `${rs.at.getMonth()+1}/${rs.at.getDate()} ${pad(rs.at.getHours())}:00`
    : "-";
  /* 안 나가는 이유가 있으면 그것부터 보여줍니다 — 사장님이 직접 전화하실 수 있게 */
  const why = remindWhy(rs);
  const row = (label, right, cls) =>
    `<div class="sms-row ${cls||""}"><span class="sm-l">${label}</span><span class="sm-r">${right}</span></div>`;
  /* 8차-Q(재아): 상태 문구를 전송 완료(초록·시각) / 전송 예정(검정·시각) / 전송 건너뜀(노랑·사유) / 전송 실패(빨강·사유) 넷으로 통일.
     네이버 예약은 네이버가 따로 보내므로 설정(smsSkipNaver)이 켜져 있으면 '건너뜀 (네이버 예약)'. 번호가 없는데 네이버가 아니면 '실패 — 번호 없음'(장난 접수·입력 오류 신호) */
  const naver = /네이버/.test(r.source||"");
  const skipNaver = naver && c.skipNaver !== false;
  const noPhone = !(r.phone||"").trim();
  const st4 = (kind, m, when) => {
    if(m) return {cls:"done", txt:`전송 완료 · ${stamp(m)}${m.resent?" (다시 보냄)":""}`};
    if(skipNaver) return {cls:"skip", txt:"전송 건너뜀 · 네이버 예약(네이버가 보냄)"};
    if(noPhone) return {cls:"fail", txt:`전송 실패 · 전화번호 없음${naver?" (네이버 예약)":""}`};
    if(kind==="재안내"){
      if(rs.state==="예정" || rs.state==="발송대기") return {cls:"plan", txt:`전송 예정 · ${planTxt}`};
      if(rs.state==="꺼짐") return {cls:"skip", txt:"전송 건너뜀 · 문자 안내 꺼짐"};
      if(rs.state==="늦은접수") return {cls:"skip", txt:"전송 건너뜀 · 임박 접수(재안내 시각 지남)"};
      if(rs.state==="제외") return {cls:"skip", txt:"전송 건너뜀 · 취소·노쇼·방문 또는 지난 예약"};
      return {cls:"skip", txt:"전송 건너뜀"};
    }
    return {cls:"skip", txt:"전송 건너뜀 · 등록 때 문자 안내가 꺼져 있었음"};
  };
  const a = st4("접수", sent), b = st4("재안내", rs.rec);
  return `
    <div class="sms-box">
      ${row("접수 문자", `<span class="sm-${a.cls}">${esc(a.txt)}</span>`)}
      ${row("재안내 문자", `<span class="sm-${b.cls}">${esc(b.txt)}</span>`)}
      <div class="sb-btns">
        <button class="btn sm" onclick="smsPreview('${r.id}','접수')">접수 문안 보기</button>
        <button class="btn sm" onclick="smsPreview('${r.id}','재안내')">재안내 문안 보기</button>
      </div>
    </div>`;
}
/* 문안을 보여주고, 그 자리에서 다시 보낼 수 있게 합니다.
   미리보기와 재발송을 한 창에 둔 이유: 사장님이 보내기 전에 내용을 반드시 보게 하려고요.
   내용을 안 보고 보내는 버튼은 실수를 부릅니다. */
async function smsPreview(id, kind){
  const r = store().reservations.find(x=>x.id===id);
  if(!r) return;
  /* '---' 줄은 화면에서 가로선으로 그려집니다 — 어디부터 어디까지가 문자인지 끊어 줍니다 */
  const body = "---\n" + smsText(r, kind, smsCfg().remindOffset) +
    "\n---";
  /* 8차-Q: '이 문자 보내기' 는 없앴습니다 — 문안 확인만. 재발송이 필요해지면 실발송 붙일 때 같이 */
  await uiAlert(kind + " 문안", (r.phone || "전화번호 없음") + "\n\n" + body, "ok");
}

/* ---------- 예약 상세 · 처리 ---------- */
function sheetMark(){
  const s = store(), st = s.settings;
  const r = s.reservations.find(x=>x.id===view.form.id);
  if(!r) return `${sheetHead("예약")}<div class="empty">예약을 찾을 수 없습니다.</div>`;

  const seat = seatTagText(r).text;   /* '장비 룸(잠정)' · '1층 테이블 · 21(잠정)' (재아) */
  const srcTxt = r.source==="기타" && r.sourceDetail ? `기타 · ${r.sourceDetail}` : (r.source||"전화");
  const made = r.createdAt ? new Date(r.createdAt) : null;
  const madeTxt = made
    ? `${made.getFullYear()}. ${made.getMonth()+1}. ${made.getDate()}. ${pad(made.getHours())}:${pad(made.getMinutes())}`
    : "기록 없음";

  const btn = (v,label,cls) =>
    `<button class="markbtn ${cls} ${r.status===v?'on':''}" onclick="markRes('${r.id}','${v}')">${label}</button>`;

  /* 좌석 미정이면 배정 후보를 바로 고를 수 있게 */
  let seatPick = "";
  if(!r.roomId && isTablePref(r.seatPref)){
    /* 테이블 예약은 층이 곧 자리입니다. 특정 테이블을 꼭 잡아야 하면 '수정' 에서 */
    const fl = prefFloor(r.seatPref);
    const st8 = !r.tentativeRoomId ? `<b style="color:var(--rust)">자리 없음</b> — 한 자리 최대 ${floorMaxParty(fl, r.date, r.time, r.id)}명`
              : r.tentativeSplit ? `<b style="color:var(--rust)">나눠 앉음</b> — 테이블 ${seatsOf(r).length}개, 붙일 수 없음`
              : `자리 있음 — 테이블 ${seatsOf(r).length}개`;
    /* 숨은 잠정 배정을 '추천 좌석' 으로 — 4명 이하도(8차-Y 재아). 어디 앉힐지는 사장 자유, 참고용 */
    const recNames = r.tentativeRoomId ? seatsOf(r).map(id=>{ const x = seatById(id); return x ? x.name : ""; }).filter(Boolean) : [];
    const rec = recNames.length ? `<div class="lbl" style="margin:12px 0 4px">추천 좌석 <span class="lbl-note">참고용 · 당일 사장님이 정합니다</span></div><div class="f-note" style="margin:0">${esc(recNames.join(" + "))}${r.tentativeSplit ? " (나눠 앉음)" : ""}</div>` : "";
    seatPick = `<div class="lbl" style="margin:16px 0 8px">테이블 자리</div>
      <p class="f-note">${esc(floorLabel(fl))} · ${st8}. 어느 테이블에 앉을지는 당일 현장에서 정합니다. 특정 테이블(파셜룸 등)을 잡으려면 '수정' 에서 고르세요.</p>${rec}`;
  }else if(!r.roomId){
    const kind = r.seatPref==="hall-any" ? "table-any" : (r.seatPref||"any");
    const ppl = pplOf(r);
    /* 후보: 룸 또는 테이블(희망 종류) + 인원에 맞는 룸 합침 그룹. 붙일 테이블은 잠정 배정이 이미 골라 둔 것(tentativeExtra)만 */
    let cand = roomsAt(r.date).filter(x=>{
      if(kind==="table-any" && !isTable(x)) return false;
      if(kind==="room-any" && !isRoom(x)) return false;
      return ppl <= seatMax(x);
    }).map(x=>{
      const ok = roomStatus(r.date,r.time,x.id,r.id).state==="free";
      const first = x.id===r.tentativeRoomId && !(r.tentativeExtra||[]).length;
      const waste = (ppl <= 2 && isTable(x) && (x.seats||4) >= 4) ? -1 : (seatMax(x) - ppl);
      return {x, ok, first, waste, ids:[x.id]};
    });
    if(kind!=="table-any") joinsAt(r.date).filter(j=>ppl>=j.min && ppl<=j.max).forEach(j=>{
      const ok = j.ids.every(id=>roomStatus(r.date,r.time,id,r.id).state==="free");
      cand.push({x:{id:j.id, name:seatLabel(j.id).replace(/ 룸$/,""), type:"join", note:j.note}, ok, first:false, waste:j.max-ppl, ids:j.ids});
    });
    if((r.tentativeExtra||[]).length && r.tentativeRoomId){
      const ids = [r.tentativeRoomId].concat(r.tentativeExtra);
      cand.unshift({x:{id:"__tent", name:seatLabelIds(ids).replace(/ 테이블$/,""), type:"tables"}, ok:ids.every(id=>roomStatus(r.date,r.time,id,r.id).state==="free"), first:true, waste:seatsMax(ids)-ppl, ids});
    }
    cand = cand.sort((a,b)=> (b.first-a.first) || (b.ok-a.ok) || (a.waste-b.waste));
    /* 쓸 수 있는 자리 중 앞에서 세 개까지 순위를 붙입니다.
       예전에는 잠정 배정된 1순위만 표시돼, 그다음으로 좋은 자리가 뭔지 알 수 없었습니다. */
    let rank = 0;
    const ranked = cand.map(c=>{
      if(c.ok && rank < 3) return {...c, rank: ++rank};
      return {...c, rank: 0};
    });
    const pickedIds = view.pickSeat ? (view.pickSeat==="__tent" ? [r.tentativeRoomId].concat(r.tentativeExtra||[]) : ((st.joins||[]).find(j=>j.id===view.pickSeat)||{ids:[view.pickSeat]}).ids) : null;
    /* 8차-K: 순위 붙은 세 개(와 이미 고른 것)만 먼저, 나머지는 '다른 자리 보기' 로 접습니다 — 후보가 스무 개면 시트가 너무 길었습니다 */
    const showAll = !!view.pickAll;
    const shown = ranked.filter(c=>showAll || c.rank || c.x.id===view.pickSeat), hiddenN = ranked.length - shown.length;
    seatPick = `
      <div class="lbl" style="margin:16px 0 8px">좌석 배정 ${r.tentativeRoomId?`<span class="tag amber">${esc(resTentLabel(r))} 잠정</span>`:""}</div>
      <div class="seatpick">${shown.map(({x,ok,rank,ids})=>`
        <button class="spick ${ok?'':'busy'} ${rank===1?'first':''} ${view.pickSeat===x.id?'picked':''} ${x.type==="join"?'join':''}"
          onclick="pickSeatCand('${r.id}','${x.id}')" ${x.note?`title="${esc(x.note)}"`:""}>
          ${esc(x.name)} <small>${seatsMin(ids, r.date)?seatsMin(ids, r.date)+"~":""}${seatsMax(ids)}</small>
          ${rank?`<i>${rank}순위</i>`:""}
        </button>`).join("")}</div>
      ${hiddenN > 0 ? `<button class="linkbtn" style="margin-top:6px" onclick="view.pickAll=true; render()">다른 자리 ${hiddenN}개 보기</button>` : (showAll && ranked.length > 3 ? `<button class="linkbtn" style="margin-top:6px" onclick="view.pickAll=false; render()">접기</button>` : "")}
      ${view.pickSeat?`
        <div class="seatconfirm">
          <span><b>${esc(seatLabelIds(pickedIds))}</b> 으로 배정합니다</span>
          <button class="btn ghost sm" onclick="pickSeatCand('${r.id}','')">취소</button>
          <button class="btn primary" onclick="assignSeat('${r.id}','${esc(view.pickSeat)}')">좌석 확정하기</button>
        </div>`:`<p class="f-note" style="margin-top:8px">자리를 고른 뒤 '좌석 확정하기'를 눌러야 배정됩니다.</p>`}`;
  }

  return `
    ${sheetHead("예약 상세")}
    <div class="mark-info">
      <div class="mi-t">${esc(r.time)} · ${esc(r.name)} 손님${tierTag(r)}${groupTag(r)} <small class="muted num" title="예약 번호">#${resCode(r)}</small></div>
      ${custStat(r).total > 1 ? `<div class="mi-s">방문 ${custStat(r).visit}회${custStat(r).noshow ? ` · <span class="rust">노쇼 ${custStat(r).noshow}회</span>` : ""}</div>` : ""}
      <div class="mi-s">${pplText(r)} · ${esc(seat)}</div>
      ${r.phone?`<div class="mi-s">${esc(r.phone)}</div>`:(r.phoneTail?`<div class="mi-s">***-****-${esc(r.phoneTail)} <small class="muted">(네이버 예약 — 번호는 네이버에서)</small></div>`:"")}
      ${custOf(r.phone)&&custOf(r.phone).memo?`<div class="mi-s"><b>손님 메모</b> · ${esc(custOf(r.phone).memo)}</div>`:""}
      <div class="mi-s">식사 · <b>${esc(r.menuType||"해당 없음")}</b>${
        r.courseUndecided?" (구성 미정)":(r.courses&&Object.keys(r.courses).length?` (${esc(courseSummary(r.courses))})`:"")}</div>
      ${r.assignedLater?`<div class="mi-s">좌석 미정으로 접수 → ${esc(resSeatLabel(r))} 배정 완료</div>`:""}
      ${resWarn(r).length?`<div class="mi-s warn-txt">경고 · ${esc(resWarn(r).join(", "))}</div>`:""}
      ${r.allergy?`<div class="mi-s warn-txt">알러지: ${esc(r.allergy)}</div>`:""}
      ${r.request?`<div class="mi-s">요청: ${esc(r.request)}</div>`:""}
      ${r.memo?`<div class="mi-s memo-line">메모: ${esc(r.memo)}</div>`:""}
      <div class="mi-meta">
        <span>경로 ${esc(srcTxt)}</span><span>등록 ${madeTxt}</span>
      </div>
    </div>
    ${(()=>{
      /* 8차-R(재아): 오늘 것만이 아니라 처음부터의 이력 전부. 오늘 바뀐 게 있을 때만 파란 상자, 아니면 회색 */
      const lines = changeLinesAll(r), todayN = r.date === todayStr() ? todayChanges(r).length : 0;   /* 파란 상자도 오늘 예약만 */
      if(!lines.length) return "";
      return `<div class="chg-box ${todayN?"":"quiet"}">
        <div class="cb-t">바뀐 내용${todayN?` <span class="tag blue">오늘 ${todayN}건</span>`:""}</div>
        ${lines.map(l=>`<div class="cb-l"><span class="cb-tm">${esc(l.t)}</span>${esc(l.s)}</div>`).join("")}
        ${todayN?`<div class="cb-s">주방에 이미 전달한 내용이 있다면 다시 알려주세요.</div>`:""}
      </div>`;
    })()}
    ${seatPick}
    ${(()=>{
      /* 8차-O(재아): 확정·취소 버튼은 빼고 방문/노쇼만. 방문을 다시 누르면 확정으로 되돌림. 오늘 이후 날짜는 눌 수 없음(아직 안 온 손님).
         취소는 '예약 내용 수정' 의 상태에서. 방문을 눌러도 시트는 그대로 둡니다(직접 닫기) */
      const future = r.date > todayStr();
      const mb = (v,label,cls) => `<button class="markbtn ${cls} ${r.status===v?'on':''}" ${future?'disabled':''} onclick="markRes('${r.id}','${r.status===v?'확정':v}')">${label}${r.status===v?' ✓':''}</button>`;
      return `<div class="lbl" style="margin:16px 0 8px">상태${r.status!=="확정"?` <span class="tag ${r.status==="방문"?"pine":r.status==="노쇼"?"rust":""}">${esc(r.status)}</span>`:""}</div>
    <div class="markgrid two">
      ${mb("방문","방문","ok")}
      ${mb("노쇼","노쇼","no")}
    </div>
    ${future?`<p class="f-note" style="margin:6px 0 0">아직 오지 않은 날의 예약은 방문·노쇼를 누를 수 없습니다. 취소는 '예약 내용 수정' 에서.</p>`:`<p class="f-note" style="margin:6px 0 0">다시 누르면 확정으로 되돌아갑니다. 취소는 '예약 내용 수정' 에서.</p>`}`;
    })()}
    <details class="sms-fold" ${view.smsOpen?"open":""} ontoggle="view.smsOpen=this.open"><summary>문자 안내</summary>${smsBox(r)}</details>
    <div class="sheet-actions">
      <button class="btn danger" onclick="delRes('${r.id}')">삭제</button>
      <button class="btn primary" onclick="openRes('${r.id}')">예약 내용 수정</button>
    </div>`;
}
async function markRes(id, status){
  if(readonlyBlock()) return;
  const s = store();
  const rec = s.reservations.find(r=>r.id===id);
  /* 취소→노쇼 기준(설정)은 setStatus·saveRes 만 물었습니다 — 이 길로 와도 같게(11월 점검) */
  if(status==="취소" && rec && rec.status!=="취소"){ const ans = await askNoshowOnCancel(rec); if(ans == null) return; status = ans; }
  if(status==="취소" && rec && rec.status!=="취소"){
    const ok = await uiConfirm("예약을 취소할까요?",
      `${rec.time} ${rec.name} 손님 · ${pplText(rec)}\n좌석이 비고, 기록에는 ‘취소’로 남습니다.`,
      {ok:"예약 취소", cancel:"그대로 두기"});
    if(!ok) return;
  }
  if(status==="노쇼" && rec && rec.status!=="노쇼"){
    const ok = await uiConfirm("노쇼로 처리할까요?",
      `${rec.time} ${rec.name} 손님 · ${pplText(rec)}\n` +
      `이 번호는 노쇼 관리 목록에 쌓이고, 다음 예약 때 안내가 뜹니다.`,
      {ok:"노쇼 처리", cancel:"그대로 두기"});
    if(!ok) return;
  }
  /* 예약 시각까지 1시간 넘게 남았는데 방문을 누르면 되묻습니다(손이 미끄러진 경우가 많음). 그래도 누르면 그대로 방문 */
  if(status==="방문" && rec && rec.status!=="방문"){
    const left = (new Date(rec.date + "T" + rec.time + ":00") - new Date()) / 60000;
    if(left > 60 && !await uiConfirm("예약 시각이 아직 멀었습니다", `${rec.time} ${rec.name} 손님 · 예약까지 ${hmDur(Math.round(left))} 남음\n지금 방문 처리할까요?`, {ok:"방문 처리", cancel:"아니요"})) return;
  }
  if(rec) logEvent("상태 변경", `${rec.date} ${rec.time} ${rec.name} ${rec.status} → ${status}`);
  /* 취소·노쇼는 화이트보드에서 지워야 하는 건이라 반드시 남깁니다.
     '방문'은 자동 처리라 변동으로 세지 않습니다 (매일 전부 표시되면 의미가 없어집니다) */
  s.reservations = s.reservations.map(function(r){
    if(r.id!==id) return r;
    const n = touch({...r, status});
    if(status==="취소" || status==="노쇼") addChange(n, status, []);
    else if(status==="확정" && (r.status==="취소" || r.status==="노쇼")) addChange(n, "변경", [{n:"상태", a:r.status, b:"확정"}]);   /* 되돌림도 남겨야 '오늘 취소' 태그가 풀립니다(점검 R3) */
    return n;
  });
  if(rec) reflowTentatives(rec.date);
  if(status === "취소") view.form = null;   /* 방문·노쇼·되돌림은 시트를 그대로 둡니다(재아) */
  saveData(); render();
}
/* 좌석 확정 — seatId 는 좌석 id / 합침 그룹 id / "__tent"(잠정으로 골라 둔 테이블 묶음). 막지 않고 확인만 (설계 5.2) */
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
    if(bk && !await uiConfirm(`${seat.name}은 이 시각에 사용 중지입니다`, `${spanLabel(bk)}${bk.note?`\n사유: ${bk.note}`:""}\n\n그래도 배정할까요?`, {ok:"그래도 배정", cancel:"다시 고르기"})) return;
    const rs = roomStatus(r.date, r.time, ids[k], id);
    if(rs.state==="blocked"){
      const lines = rs.hits.map(x=>`· ${hm(x.time)} ${x.name} 손님 ${pplText(x)}`).join("\n");
      if(!await uiConfirm(`${seat.name}에 ${hmDur(store().settings.closeGapMin != null ? store().settings.closeGapMin : 60)} 안에 확정 예약이 있습니다`, lines, {ok:"그래도 배정", cancel:"다시 고르기"})) return;
    }else if(rs.state==="warn" && !await uiConfirm2(`${seat.name}에 겹치는 예약이 있습니다. 그래도 배정할까요?`)) return;
  }
  if(ppl > seatsMax(ids) && !await uiConfirm2(`${label} 정원(${seatsMax(ids)}명)을 넘습니다. 배정할까요?`)) return;
  if(adultCount(ppl, r.infants||0) < seatsMin(ids, r.date) && !await uiConfirm2(`${label}은 최소 ${seatsMin(ids, r.date)}명부터입니다. 지금 ${adultCount(ppl, r.infants||0)}명입니다. 배정할까요?`)) return;
  if(j && (j.split || j.note) && !await uiConfirm(`${label} — ${j.note || "공간이 나뉩니다"}`, j.split ? "테이블이 나뉘어 앉게 됩니다. 손님께 확인하셨나요?" : "손님께 확인하셨나요?", {ok:"확인했음 · 배정", cancel:"다시 고르기"})) return;
  logEvent("좌석 배정", `${r.date} ${r.time} ${r.name} → ${label}`);
  if(!r.roomId) r.assignedLater = {from:r.seatPref||"any", at:new Date().toISOString()};
  addChange(r, "변경", [{n:"좌석", a:resSeatLabel(r), b:label}]);
  r.roomId = ids[0]; r.extraIds = ids.slice(1); r.tentativeRoomId = null; r.tentativeExtra = []; r.tentativeSplit = false; r.seatPref = null;
  view.pickSeat = null;
  reflowTentatives(r.date);
  view.form = null; saveData(); render();
}


/* ---------- 룸 미배정 목록 ---------- */
function sheetUnassigned(){
  const s = store(), d = view.date;
  const list = s.reservations.filter(r=>r.date===d && r.status==="확정" && (isUnassigned(r) || (r.roomId && !seatById(r.roomId))))
    .sort((a,b)=>a.time.localeCompare(b.time));
  const rows = list.length ? list.map(r=>`
    <button class="rowitem tap" onclick="openMark('${r.id}')">
      <span class="time-col">${esc(r.time)}</span>
      <span class="grow"><span class="t">${esc(r.name)}</span>
        <span class="s">${pplText(r)} · 희망 ${esc(seatLabel(r.seatPref||"any"))}${r.phone?` · ${esc(r.phone)}`:""}</span></span>
      <span class="tag ${r.tentativeRoomId?'amber':'rust'}">${r.tentativeRoomId?`잠정 ${esc(resTentLabel(r))}`:"자리 없음"}</span>
    </button>`).join("") : `<div class="empty">배정할 예약이 없습니다.</div>`;
  return `
    ${sheetHead(`룸 미배정 · ${dateLabel(d)}`)}
    <div class="card" style="margin-bottom:12px">${rows}</div>
    <p class="f-note">예약을 누르면 좌석을 배정할 수 있습니다. ‘잠정’은 시스템이 잡아둔 1순위 자리입니다.</p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}

/* ---------- 숫자 입력 팝업 ---------- */
function numValue(){
  const f = view.form;
  if(f.val != null) return f.val;
  const st = draft();
  if(f.ctx && f.ctx.room){
    const r = st.rooms.find(x=>x.id===f.ctx.room);
    return r ? (f.key==="minCapacity" ? roomMin(r) : f.key==="minWeekend" ? (r.minWeekend != null ? r.minWeekend : roomMin(r)) : f.key==="optCapacity" ? roomOpt(r) : (r[f.key] != null ? r[f.key] : (f.key==="capacity" ? seatMax(r) : f.min))) : f.min;
  }
  if(f.ctx && f.ctx.join){
    const j = (st.joins||[]).find(x=>x.id===f.ctx.join);
    return j ? j[f.key] : f.min;
  }
  return st[f.key] != null ? st[f.key] : f.min;
}
function sheetNum(){
  const f = view.form;
  const v = numValue();
  const step = (f.ctx && f.ctx.step) || 1;
  const quick = [];
  for(let i=f.min; i<=f.max && quick.length<12; i+=step) quick.push(+i.toFixed(1));
  return `
    ${sheetHead(f.title)}
    <div class="numbig">
      <button onclick="numAdj(-1)" ${v<=f.min?"disabled":""}>−</button>
      <div class="nv">${v}</div>
      <button onclick="numAdj(1)" ${v>=f.max?"disabled":""}>＋</button>
    </div>
    <div class="numgrid">
      ${quick.map(n=>`<button class="${v===n?'on':''}" onclick="numSet(${n})">${n}</button>`).join("")}
    </div>
    <p class="f-note">${f.min} ~ ${f.max} 사이로 정할 수 있습니다.${step!==1?` (${step} 단위)`:""}</p>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">취소</button>
      <button class="btn primary" onclick="numSave()">확인</button>
    </div>`;
}
function numAdj(d){
  const f = view.form;
  const step = (f.ctx && f.ctx.step) || 1;
  f.val = +Math.max(f.min, Math.min(f.max, numValue()+d*step)).toFixed(1);
  render();
}
function numSet(n){ view.form.val = n; render(); }
function numSave(){
  const f = view.form, v = numValue();
  const st = draft();
  if(f.ctx && f.ctx.room){
    st.rooms = st.rooms.map(r=>{
      if(r.id!==f.ctx.room) return r;
      const n = Object.assign({}, r, {[f.key]:v, tuned:true});
      /* 최소가 최대보다 크면 그 좌석은 어떤 인원에도 안 맞아 배정 후보에서 영영 빠집니다(점검 C4) — 맞춰 줍니다 */
      if((f.key==="minCapacity" || f.key==="minWeekend" || f.key==="optCapacity") && n.capacity != null && v > seatMax(n)) n.capacity = v;
      if(f.key==="capacity"){ if(n.minCapacity != null && n.minCapacity > v) n.minCapacity = v; if(n.minWeekend != null && n.minWeekend > v) n.minWeekend = v; if(n.optCapacity != null && n.optCapacity > v) n.optCapacity = v; }
      return n;
    });
  }else if(f.ctx && f.ctx.join){
    st.joins = (st.joins||[]).map(j=>j.id===f.ctx.join?Object.assign({}, j, {[f.key]:v}):j);
  }else{
    st[f.key] = v;
  }
  view.form = null; render();
}

/* ---------- 홀 테이블 구성 ---------- */
/* 이 구역에서 실제로 만들 수 있는 자리 크기를 모두 구합니다.
   (같은 구역 안이면 어떤 테이블이든 붙임 한도까지 붙일 수 있습니다) */

/* 구역 배치를 그림으로 — 테이블 구성과 만들 수 있는 자리 크기를 함께 보여줍니다 */

/* ---------- 예약 검색 ----------
   전화 응대 중 "지난주에 예약한 OOO인데요"를 찾기 위한 화면입니다. */
function sheetSearch(){
  const q = (view.searchQ||"").trim();
  const s = store();
  /* 8차-K(재아): 구분 없이 한 글자부터 전부 찾습니다 — 이름·전화·메모·요청·알러지·경로·좌석. 많이 뜨면 더 치면 줄어듭니다 */
  const digits = q.replace(/\D/g,"");
  const lower = q.toLowerCase();
  const okNum = digits.length >= 1 && /^[\d\-\s]+$/.test(q);
  const okTxt = q.length >= 1 && !okNum;
  let rows = "";   /* 안내 문구는 입력칸 placeholder 하나로(재아 09-17) */
  if(okNum || okTxt){
    const hits = s.reservations.filter(r=>{
      if(okNum) return (r.phone||"").replace(/\D/g,"").includes(digits);
      const bag = `${r.name} ${r.request||""} ${r.memo||""} ${r.allergy||""} ${r.sourceDetail||""} ${r.source||""} ${resSeatLabel(r)} ${r.phone||""}`.toLowerCase();
      return bag.includes(lower);
    }).sort((a,b)=> b.date.localeCompare(a.date) || b.time.localeCompare(a.time)).slice(0,80);
    rows = hits.length ? hits.map(r=>`
      <button class="rowitem tap" onclick="goRes('${r.id}','${r.date}')">
        <span class="grow"><span class="t">${esc(r.name)}${tierTag(r)}
          ${r.status!=="확정"?`<span class="tag ${r.status==="노쇼"?"rust":""}">${r.status}</span>`:""}</span>
          <span class="s">${dateLabel(r.date)} ${esc(r.time)} · ${pplText(r)} · ${esc(r.phone||"연락처 없음")}${
          r.request?` · ${esc(r.request)}`:""}${r.allergy?` · 알러지 ${esc(r.allergy)}`:""}</span></span>
        ${seatTag(r)}
      </button>`).join("")
      : `<div class="empty">찾은 예약이 없습니다.</div>`;
  }
  const hintTxt = "";
  return `
    ${sheetHead("예약 검색")}
    <input id="search-q" value="${esc(q)}" placeholder="이름, 전화, 메모, 요청사항에서 검색합니다."
           oninput="setSearchQ(this.value)" autocomplete="off" style="margin-bottom:10px">
    ${hintTxt}
    <div class="card searchbox">${rows}</div>`;
}
function setSearchQ(v){
  view.searchQ = v;
  const box = document.querySelector(".searchbox");
  if(box) box.innerHTML = sheetSearch().split('<div class="card searchbox">')[1].split('</div>\n    <div class="sheet-actions"')[0];
}
function goRes(id, date){
  view.date = date; view.calMonth = date.slice(0,7);
  view.form = {type:"mark", id};
  render();
}

/* ---------- 노쇼 관리 ----------
   따로 저장하지 않고 예약 기록에서 전화번호 기준으로 모읍니다. */
function noshowList(){
  const s = store();
  const excluded = s.settings.noshowExcluded || [];
  const map = new Map();
  s.reservations.filter(r=>r.status==="노쇼" && r.phone).forEach(r=>{
    const key = r.phone.replace(/\D/g,"");
    if(!key || excluded.includes(key)) return;
    if(!map.has(key)) map.set(key, {phone:r.phone, key, name:r.name, count:0, dates:[]});
    const v = map.get(key);
    v.count++; v.dates.push(r.date); v.name = r.name;
  });
  return [...map.values()].sort((a,b)=>b.count-a.count);
}
function noshowOf(phone){
  if(!phone) return null;
  const key = String(phone).replace(/\D/g,"");
  if(!key) return null;
  const hit = noshowList().find(x=>x.key===key) || null;
  const need = store().settings.noshowWarnCount != null ? store().settings.noshowWarnCount : 1;   /* 설정: 몇 회부터 경고 */
  return hit && hit.count >= need ? hit : null;
}
function sheetNoshow(){
  /* 8차-O(재아): 예약자 단위가 아니라 식사 날짜 단위 — 한 건씩 '되돌리기' 가 됩니다(잘못 누른 노쇼). 같은 번호의 횟수는 옆에 */
  const excluded = store().settings.noshowExcluded || [];
  const cnt = {}; store().reservations.forEach(r=>{ if(r.status==="노쇼" && r.phone){ const k=r.phone.replace(/\D/g,""); cnt[k]=(cnt[k]||0)+1; } });
  const list = store().reservations.filter(r=>r.status==="노쇼").sort((a,b)=>(b.date+b.time).localeCompare(a.date+a.time)).slice(0,120);
  const rows = list.length ? list.map(r=>{ const k=(r.phone||"").replace(/\D/g,""); const ex = k && excluded.includes(k); return `
    <div class="rowitem">
      <button class="grow tap-plain" onclick="openMark('${r.id}')" title="예약 상세"><span class="t">${dateLabel(r.date)} ${esc(r.time)} · ${esc(r.name)}${k && cnt[k]>1?` <span class="tag rust">노쇼 ${cnt[k]}회</span>`:""}${ex?` <span class="tag">경고 제외</span>`:""}</span>
        <span class="s">${pplText(r)} · ${esc(r.phone||(r.phoneTail?`***-****-${r.phoneTail} (네이버)`:"연락처 없음"))} · ${esc(resSeatLabel(r))}</span></button>
      <button class="btn sm" onclick="undoNoshow('${r.id}')">노쇼 취소</button>
      ${k ? (ex ? `<button class="btn sm ghost" onclick="unclearNoshow('${k}')" title="다시 노쇼 경고를 띄움">경고 제외 해제</button>` : `<button class="btn sm ghost" onclick="clearNoshow('${k}')" title="이 번호는 다음 예약 때 노쇼 경고를 띄우지 않음">경고 제외</button>`) : ""}
    </div>`; }).join("") : `<div class="empty">노쇼 기록이 없습니다.</div>`;
  /* 노쇼율 — 이번 달·지난 달·최근 90일. 분모는 '올 손님'(방문+노쇼), 취소는 뺍니다 */
  const rate = (from, to) => { const all = store().reservations.filter(r=>r.date >= from && r.date <= to && r.date < todayStr() && (r.status==="방문"||r.status==="노쇼")); const ns = all.filter(r=>r.status==="노쇼").length; return {n:all.length, ns, pct: all.length ? Math.round(ns/all.length*1000)/10 : 0}; };
  const t = todayStr(), ym = t.slice(0,7), pm = shiftDate(ym + "-01", -1).slice(0,7);
  const rThis = rate(ym + "-01", t), rPrev = rate(pm + "-01", pm + "-31"), r90 = rate(shiftDate(t, -90), t);
  const stat = `<div class="ns-stats">
      <div class="ns-stat"><div class="v">${rThis.pct}<span class="u">%</span></div><div class="k">이번 달 노쇼율</div><div class="s">${rThis.ns}건 / ${rThis.n}팀</div></div>
      <div class="ns-stat"><div class="v">${rPrev.pct}<span class="u">%</span></div><div class="k">지난 달</div><div class="s">${rPrev.ns}건 / ${rPrev.n}팀</div></div>
      <div class="ns-stat"><div class="v">${r90.pct}<span class="u">%</span></div><div class="k">최근 90일</div><div class="s">${r90.ns}건 / ${r90.n}팀</div></div>
    </div>`;
  return `
    ${sheetHead("노쇼 관리")}
    <div class="btn-row" style="margin:-4px 0 10px"><button class="btn sm" onclick="openSearch()">🔍 예약 검색</button></div>
    ${stat}
    <div class="card" style="margin-bottom:12px">${rows}</div>
    <p class="f-note">예약 상태를 ‘노쇼’로 바꾸면 자동으로 여기에 쌓입니다.
      새 예약을 등록할 때 같은 번호가 있으면 확정 전에 알려드립니다.
      ${excluded.length?`<br>경고 제외 번호 ${excluded.length}건 · <button class="linkbtn" onclick="restoreNoshow()">전부 해제</button>`:""}
    </p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
/* 노쇼 되돌리기 — 지난 날짜면 '방문'(실제로 온 것), 오늘·앞날이면 '확정' */
async function undoNoshow(id){
  const r = store().reservations.find(x=>x.id===id); if(!r) return;
  const to = r.date < todayStr() ? "방문" : "확정";
  if(!await uiConfirm("노쇼를 취소할까요?", `${dateLabel(r.date)} ${r.time} ${r.name} 손님 → ${to}(으)로 돌아갑니다`, {ok:"노쇼 취소"})) return;
  if(readonlyBlock()) return;
  logEvent("노쇼 취소", `${r.date} ${r.time} ${r.name} ${pplOf(r)}명 ${r.phone||""} 노쇼 → ${to}`);
  addChange(r, "변경", [{n:"상태", a:"노쇼", b:to}]); r.status = to; touch(r);
  reflowTentatives(r.date); saveData(); render();
}
async function clearNoshow(key){
  if(!await uiConfirm2("이 고객의 노쇼 기록을 목록에서 제외할까요?\n예약 기록 자체는 남습니다.")) return;
  const st = store().settings;
  logEvent("노쇼 기록 제외", key);
  st.noshowExcluded = [...(st.noshowExcluded||[]), key];
  mirrorDraft("noshowExcluded");
  saveData(); render();
}
function restoreNoshow(){ store().settings.noshowExcluded = []; mirrorDraft("noshowExcluded"); logEvent("노쇼 경고 제외 전부 해제", ""); saveData(); render(); }
async function unclearNoshow(key){
  if(readonlyBlock()) return;
  const st = store().settings; st.noshowExcluded = (st.noshowExcluded||[]).filter(k=>k!==key); mirrorDraft("noshowExcluded");
  logEvent("노쇼 경고 제외 해제", key); saveData(); render();
}

/* ---------- 운영시간 수정 ---------- */
const DOW = ["일","월","화","수","목","금","토"];
/* 운영시간 요약 한 줄에 붙는 세션 요약 — "점심 접수 ~14:00 · 저녁 접수 ~19:30" */
function sessSummary(d){
  const ss = sessionsOfDay(d); if(!ss.length) return "";
  const f = v => v === "end" ? "끝까지" : `${v||110}분`;
  return `<span class="sch-s">${ss.map(se=>`${esc(se.name)} 접수 ~${esc(se.lastBook)} (룸 ${f(se.stay)} · 테이블 ${f(se.stayTable)})`).join(" · ")}</span>`;
}
/* 운영시간 편집(8차-X, 재아) — 월요일부터, 요일 카드는 접혀 있고 눌러서 폅니다.
   세션은 '점심 경계' 하나 + 점심/저녁 접수 마감·점유(룸/테이블 따로). 브레이크가 있으면 경계는 브레이크 시작으로 잠깁니다.
   라스트오더는 직접 입력하고 옆에 '마감 N분 전' 을 참고로만 보여 줍니다(자동 버튼 삭제) */
function stayBox(i, seg, k, label){
  const v = dayOf(i).sess[seg][k];
  return `<div class="sf"><span>${label}</span><span class="sess-stay"><label class="chk"><input type="checkbox" ${v==="end"?"checked":""} onchange="setSessV(${i},'${seg}','${k}',this.checked?'end':110)"><span>끝까지</span></label>
    <input type="number" min="30" step="10" value="${v==="end"?"":(v||110)}" ${v==="end"?"disabled":""} onchange="setSessV(${i},'${seg}','${k}',parseInt(this.value)||110)"><small>분</small></span></div>`;
}
function segBox(i, seg, title, note){
  return `<div class="sess-r two">
    <div class="sf full"><b>${title}</b><span class="lbl-note">${esc(note)}</span></div>
    <div class="sf"><span>접수 마감</span><input type="time" value="${dayOf(i).sess[seg].lastBook||""}" onchange="setSessV(${i},'${seg}','lastBook',this.value)"></div>
    ${stayBox(i, seg, "room", "점유 · 룸")}
    ${stayBox(i, seg, "table", "점유 · 테이블")}
  </div>`;
}
function setSessV(i, seg, k, v){ dayOf(i).sess[seg][k] = v; render(); }
function setEdge(i, v){ dayOf(i).sess.edge = v; render(); }
function toggleEdge(i){ const x = dayOf(i).sess; x.edge = x.edge === "" ? "15:30" : ""; render(); }
function toggleSchedDay(key){ const d = view.schedDraft; d.open = d.open || {}; d.open[key] = !d.open[key]; render(); }
function sheetSchedule(){
  const d = view.schedDraft;
  d.open = d.open || {};
  const dayBlock = (x, i, label, cls) => {
    ensureSess(x);
    const key = String(i), isOpen = !!d.open[key];
    const edge = x.bs ? x.bs : (x.sess.edge || "");
    const loRef = x.lo ? `마감 ${hmDur(Math.max(0, toMin(x.close) - toMin(x.lo)))} 전` : "";
    const sum = `${esc(x.open)} ~ ${esc(x.close)}${x.bs?` · 브레이크 ${esc(x.bs)} ~ ${esc(x.be)}`:""}${x.lo?` · 라스트오더 ${esc(x.lo)}`:""}`;
    return `<div class="dayrow ${cls||''} ${isOpen?'on':''}">
      <button class="dr-h" onclick="toggleSchedDay('${key}')"><b>${label}</b><span class="dr-sum">${sum}</span><span class="fh-i">${isOpen?"▲":"▼"}</span></button>
      ${isOpen ? `<div class="dr-in">
        <label><span>영업</span>
          <input type="time" value="${x.open}" onchange="setDay(${i},'open',this.value)">
          <em>~</em>
          <input type="time" value="${x.close}" onchange="setDay(${i},'close',this.value)"></label>
        <label><span>브레이크</span>
          <input type="time" value="${x.bs||""}" ${x.bs?"":"disabled"} onchange="setDay(${i},'bs',this.value)">
          <em>~</em>
          <input type="time" value="${x.be||""}" ${x.bs?"":"disabled"} onchange="setDay(${i},'be',this.value)"></label>
        <label class="chk"><input type="checkbox" ${x.bs?"":"checked"} onchange="toggleBreakDay(${i})">
          <span>브레이크타임 없음</span></label>
        <label><span>라스트오더</span>
          <input type="time" value="${x.lo||""}" ${x.lo?"":"disabled"} onchange="setDay(${i},'lo',this.value)">
          <em class="lo-ref">${loRef}</em></label>
        <label class="chk"><input type="checkbox" ${x.lo?"":"checked"} onchange="toggleLoDay(${i})">
          <span>라스트오더 없음</span></label>
        <label><span>점심 경계</span>
          <input type="time" value="${edge}" ${(x.bs || x.sess.edge === "")?"disabled":""} onchange="setEdge(${i},this.value)">
          <em class="lo-ref">${x.bs ? "브레이크 시작과 같음 (자동)" : edge ? "이 시각부터 저녁" : "하루가 한 세션"}</em></label>
        ${x.bs ? "" : `<label class="chk"><input type="checkbox" ${x.sess.edge===""?"checked":""} onchange="toggleEdge(${i})">
          <span>점심 경계 없음 (하루 한 세션)</span></label>`}
        <div class="sess">
          ${edge ? segBox(i,"lunch","점심", `${x.open} ~ ${edge}`) + segBox(i,"dinner","저녁", `${x.be||edge} ~ ${x.close}`) : segBox(i,"dinner","종일", `${x.open} ~ ${x.close}`)}
        </div>
      </div>` : ""}
    </div>`;
  };
  const rows = [1,2,3,4,5,6,0].map(i=>dayBlock(d.days[i], i, DOW[i], i===0?'sun':i===6?'sat':'')).join("")
             + dayBlock(d.holiday, 7, "공휴일", "sun");
  return `
    ${sheetHead(d.isNew?"운영시간 수정":"운영시간 편집")}
    <p class="f-note" style="margin:-6px 0 12px"><b>점심 경계</b>부터 저녁입니다(브레이크가 있으면 브레이크 시작). <b>접수 마감</b>은 마지막으로 입장을 받는 시각,
      <b>점유 '끝까지'</b>는 그 세션 끝까지 한 자리에 한 팀. 라스트오더는 주방 마감이라 별개입니다.</p>
    <label class="f"><div class="lb">적용 시작일</div>
      <input type="date" value="${d.from}" onchange="setSchedFrom(this.value)">
      <div class="f-note">이 날짜부터 새 시간이 적용됩니다. 그 전 날짜는 이전 설정을 그대로 씁니다.</div>
    </label>
    ${rows}
    <div class="sheet-actions">
      ${!d.isNew && d.from!=="2000-01-01" ? `<button class="btn danger" onclick="delSchedule('${d.from}')">삭제</button>`:""}
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="saveSchedule()">저장</button>
    </div>`;
}
function dayOf(i){ return i===7 ? view.schedDraft.holiday : view.schedDraft.days[i]; }
function setDay(i,k,v){ dayOf(i)[k]=v; render(); }
function toggleBreakDay(i){
  const d = dayOf(i);
  if(d.bs){ d.bs=""; d.be=""; } else { d.bs="15:30"; d.be="17:00"; }
  render();
}
function toggleLoDay(i){
  const d = dayOf(i);
  d.lo = d.lo ? "" : minToHM(Math.max(0, toMin(d.close)-80));
  render();
}
function setSchedFrom(v){ view.schedDraft.from = v; render(); }
async function saveSchedule(){
  const st = store().settings, d = view.schedDraft;
  if(!d.from) return uiAlert("적용 시작일을 정해주세요","","warn");
  st.schedules = (st.schedules||[]).filter(s=>s.from!==d.from && s.from!==d.origFrom);   /* 시작일을 바꿨으면 옛 항목도 정리 */
  d.days.forEach(ensureSess); ensureSess(d.holiday);
  st.schedules.push({from:d.from, days:deepClone(d.days), holiday:deepClone(d.holiday)});
  st.schedules.sort((a,b)=>a.from.localeCompare(b.from));
  mirrorDraft("schedules");   /* 안 그러면 '적용하기'가 방금 저장한 것을 되돌립니다(점검 D1) */
  logEvent("설정 변경", `운영시간 ${d.from}부터`);
  view.form=null; view.schedDraft=null; saveData(); render();
}
async function delSchedule(from){
  if(!await uiConfirm("이 운영시간을 삭제할까요?", `${from}부터 적용되던 설정이 사라지고 이전 설정이 이어집니다.`, {ok:"삭제"})) return;
  const st = store().settings;
  st.schedules = st.schedules.filter(s=>s.from!==from);
  mirrorDraft("schedules");
  logEvent("설정 변경", `운영시간 삭제 ${from}`);
  view.form=null; saveData(); render();
}

/* ---------- 임시 영업시간 · 휴무 ---------- */
function sheetOverride(){
  const st = store().settings;
  const list = (st.overrides||[]).slice().sort((a,b)=>a.date.localeCompare(b.date));
  const rows = list.length ? list.map(o=>`
    <div class="rowitem">
      <span class="grow"><span class="t">${dateLabel(o.date)}
        <span class="tag ${o.closed?'rust':'amber'}">${o.closed?"휴무":"임시 시간"}</span></span>
        <span class="s">${o.closed?esc(o.note||"휴무")
          :`${esc(o.open||"-")} ~ ${esc(o.close||"-")}${o.bs?` · 브레이크 ${esc(o.bs)} ~ ${esc(o.be)}`:""}${o.note?` · ${esc(o.note)}`:""}`}</span></span>
      <button class="btn sm danger" onclick="delOverride('${o.date}')">삭제</button>
    </div>`).join("") : `<div class="empty">등록된 임시 일정이 없습니다.</div>`;
  const d = view.ovrDraft || {date:todayStr(), closed:true, open:"", close:"", bs:"", be:"", lo:"", note:""};
  const base = hoursFor(d.date);
  return `
    ${sheetHead("임시 영업시간 · 휴무")}
    <div class="card" style="margin-bottom:14px">${rows}</div>
    <div class="sect-title" style="margin-top:0">새로 추가</div>
    <label class="f"><div class="lb">날짜</div>
      <input type="date" value="${d.date}" onchange="setOvr('date',this.value)"></label>
    <div class="seg" style="margin-bottom:12px">
      <button class="${d.closed?'on':''}" onclick="setOvr('closed',true)">휴무</button>
      <button class="${d.closed?'':'on'}" onclick="setOvr('closed',false)">시간 변경</button>
    </div>
    ${d.closed?"":`
      <div class="grid2">
        <label class="f"><div class="lb">영업 시작</div>
          <input type="time" value="${d.open||base.open}" onchange="setOvr('open',this.value)"></label>
        <label class="f"><div class="lb">영업 종료</div>
          <input type="time" value="${d.close||base.close}" onchange="setOvr('close',this.value)"></label>
        <label class="f"><div class="lb">브레이크 시작</div>
          <input type="time" value="${d.noBreak?"":(d.bs!==undefined&&d.bs!==""?d.bs:base.bs)}" ${d.noBreak?"disabled":""} onchange="setOvr('bs',this.value)"></label>
        <label class="f"><div class="lb">브레이크 종료</div>
          <input type="time" value="${d.noBreak?"":(d.be!==undefined&&d.be!==""?d.be:base.be)}" ${d.noBreak?"disabled":""} onchange="setOvr('be',this.value)"></label>
      </div>
      <label class="chk"><input type="checkbox" ${d.noBreak?"checked":""} onchange="setOvr('noBreak',this.checked)">
        <span>브레이크타임 없음</span></label>
      <label class="f"><div class="lb">라스트오더</div>
        <input type="time" value="${d.noLo?"":(d.lo||base.lo)}" ${d.noLo?"disabled":""} onchange="setOvr('lo',this.value)"></label>
      <label class="chk"><input type="checkbox" ${d.noLo?"checked":""} onchange="setOvr('noLo',this.checked)">
        <span>라스트오더 없음</span></label>`}
    <label class="f"><div class="lb">메모</div>
      <input value="${esc(d.note||"")}" placeholder="예: 창립기념일 단축 영업" onchange="setOvr('note',this.value)"></label>
    <label class="chk"><input type="checkbox" ${d.holiday || (d.holiday == null && isHoliday(d.date||todayStr())) ? "checked" : ""} onchange="setOvr('holiday',this.checked)">
      <span>공휴일(빨간날)로도 표시 — 워크시프트 휴일 가산·달력 색에 반영</span></label>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="saveOverride()">추가</button>
    </div>
    ${bulkOvrHtml()}`;
}
/* ---------- 임시 일정 일괄 등록 (8차-J, 재아 요청) ----------
   한 줄에 하나. `날짜 | 메모 | 내용`. 메모는 비워도 됩니다. 날짜는 2026-12-31 또는 2026-12-24~2026-12-26.
   내용은 `휴무` 또는 `영업 11:00-23:00` 에 `라스트오더 22:00`(또는 `라스트오더 없음`)·`브레이크 15:00-17:00`(또는 `브레이크 없음`) 을 덧붙임.
   영업 시간이 없는데 휴무도 아니면 오류. 미리보기에서 줄마다 결과를 보고 '적용' 하면 맞는 줄만 들어갑니다(같은 날짜는 덮어씀). */
const BULK_OVR_GUIDE = "날짜 | 메모 | 내용   (한 줄에 하나, 메모는 비워도 됨)\n2026-09-16 | 임시공휴일 | 휴무\n2026-12-31 | 연말 | 영업 11:00-23:00 라스트오더 22:00 브레이크 없음\n2026-12-24~2026-12-26 | 크리스마스 | 영업 11:00-22:00 브레이크 15:00-17:00";
function bulkOvrHtml(){
  const b = view.ovrBulk || {text:"", result:null};
  const res = b.result ? `<div class="bulk-res">${b.result.map(x=>`<div class="bulk-row ${x.ok?'ok':'bad'}"><span class="bulk-ln">${x.n}</span><span class="grow">${esc(x.text)}</span><span class="bulk-msg">${x.ok?`✓ ${esc(x.msg)}`:`✗ ${esc(x.msg)}`}</span></div>`).join("")}</div>` : "";
  const okN = b.result ? b.result.filter(x=>x.ok).length : 0, badN = b.result ? b.result.length - okN : 0;
  return `
    <div class="sect-title" style="margin-top:20px">일괄 등록 <span class="lbl-note">여러 날을 한 번에</span></div>
    <pre class="bulk-guide">${esc(BULK_OVR_GUIDE)}</pre>
    <textarea id="ovr-bulk" rows="6" placeholder="여기에 붙여 넣으세요" oninput="setOvrBulk(this.value)">${esc(b.text)}</textarea>
    <div class="btn-row" style="margin-top:8px">
      <button class="btn" onclick="copyBulkPrompt()">AI 에게 시킬 프롬프트 복사</button>
      <button class="btn" onclick="bulkPreview()">미리보기</button>
      ${b.result ? `<button class="btn primary" onclick="bulkApply()" ${okN?"":"disabled"}>맞는 ${okN}줄 적용${badN?` (오류 ${badN}줄 제외)`:""}</button>` : ""}
    </div>
    ${res}`;
}
function setOvrBulk(v){ view.ovrBulk = {text:v, result:null}; }   /* 글자마다 render 하지 않습니다(입력 유실) */
function parseOvrLine(line){
  const parts = line.split("|").map(x=>x.trim());
  if(parts.length < 2) return {ok:false, msg:"‘|’ 로 나눈 칸이 두 개 이상이어야 합니다 (날짜 | 메모 | 내용)"};
  const dateRaw = parts[0].replace(/\./g,"-").replace(/\s/g,""), note = parts.length >= 3 ? parts[1] : "", spec = (parts.length >= 3 ? parts.slice(2).join(" ") : parts[1]).trim();
  const dm = dateRaw.match(/^(\d{4}-\d{2}-\d{2})(?:~(\d{4}-\d{2}-\d{2}))?$/);
  if(!dm) return {ok:false, msg:"날짜는 2026-12-31 또는 2026-12-24~2026-12-26 형식"};
  const from = dm[1], to = dm[2] || dm[1];
  if(isNaN(new Date(from+"T00:00:00")) || isNaN(new Date(to+"T00:00:00")) || to < from) return {ok:false, msg:"날짜가 이상합니다"};
  const dates = []; for(let d = from; d <= to && dates.length < 62; d = shiftDate(d, 1)) dates.push(d);
  if(/^(휴무|휴업|쉼|닫음)$/.test(spec.replace(/\s/g,""))) return {ok:true, dates, rec:{closed:true, note:note||"휴무"}, msg:`${dates.length}일 휴무`};
  const t = spec.replace(/\s+/g," ");
  const open = t.match(/영업\s*(\d{1,2}:\d{2})\s*[-~]\s*(\d{1,2}:\d{2})/);
  if(!open) return {ok:false, msg:"‘휴무’ 이거나 ‘영업 11:00-22:00’ 처럼 영업 시간이 있어야 합니다"};
  const pad2 = x => x.length === 4 ? "0" + x : x;
  const base = hoursFor(from);
  const rec = {closed:false, open:pad2(open[1]), close:pad2(open[2]), bs:"", be:"", lo:"", note:note||"임시 운영시간"};
  const lo = t.match(/(?:라스트오더|LO|lo)\s*(\d{1,2}:\d{2})/);
  const loNone = /(?:라스트오더|LO|lo)\s*(?:없음|없|x|X)/.test(t);
  if(lo) rec.lo = pad2(lo[1]); else if(!loNone) rec.lo = base.lo || "";
  const br = t.match(/브레이크\s*(\d{1,2}:\d{2})\s*[-~]\s*(\d{1,2}:\d{2})/);
  const brNone = /브레이크\s*(?:없음|없|x|X)/.test(t);
  if(br){ rec.bs = pad2(br[1]); rec.be = pad2(br[2]); } else if(!brNone){ rec.bs = base.bs || ""; rec.be = base.be || ""; }
  if(toMin(rec.close) <= toMin(rec.open)) return {ok:false, msg:"종료가 시작보다 빠릅니다"};
  return {ok:true, dates, rec, msg:`${dates.length}일 · ${rec.open}~${rec.close}${rec.bs?` 브레이크 ${rec.bs}~${rec.be}`:" 브레이크 없음"}${rec.lo?` 라스트오더 ${rec.lo}`:" 라스트오더 없음"}`};
}
function bulkPreview(){
  const ta = document.getElementById("ovr-bulk"); const text = ta ? ta.value : (view.ovrBulk ? view.ovrBulk.text : "");
  const lines = text.split(/\r?\n/).map(x=>x.trim()).filter(x=>x && !/^날짜\s*\|/.test(x));
  const result = lines.map((ln, i)=>Object.assign({n:i+1, text:ln}, parseOvrLine(ln)));
  view.ovrBulk = {text, result}; render();
}
async function bulkApply(){
  const b = view.ovrBulk; if(!b || !b.result) return;
  if(readonlyBlock()) return;
  const st = store().settings; let n = 0;
  b.result.filter(x=>x.ok).forEach(x=>{ x.dates.forEach(d=>{
    st.overrides = (st.overrides||[]).filter(o=>o.date!==d).concat([Object.assign({date:d}, x.rec)]); n++;
  }); });
  mirrorDraft("overrides");
  logEvent("설정 변경", `임시 일정 일괄 ${n}일`);
  view.ovrBulk = null; saveData(); render();
  uiAlert("일괄 등록 완료", `${n}일이 들어갔습니다. 위 목록에서 확인하세요.`, "ok");
}
async function copyBulkPrompt(){
  const txt = "우리 식당(한옥반점) 예약 시스템에 넣을 임시 휴무·영업시간 목록을 만들어 줘.\n먼저 나에게 물어봐: ① 몇 년도 공휴일이 필요한지(대체공휴일 포함 여부) ② 휴무로 할 날과 임시 영업시간으로 할 날 ③ 임시 영업시간이면 영업·라스트오더·브레이크 시간. 답을 받은 뒤에 아래 형식으로 한 줄에 하루씩만 출력해(다른 말 없이).\n형식: 날짜 | 메모 | 내용\n- 날짜: 2026-12-31 처럼. 연속이면 2026-12-24~2026-12-26\n- 내용: \"휴무\" 또는 \"영업 11:00-22:00\" 뒤에 \"라스트오더 21:00\"(없으면 \"라스트오더 없음\"), \"브레이크 15:00-17:00\"(없으면 \"브레이크 없음\")\n예)\n2026-09-16 | 임시공휴일 | 휴무\n2026-12-31 | 연말 | 영업 11:00-23:00 라스트오더 22:00 브레이크 없음\n\n내가 원하는 것: ";
  try{ await navigator.clipboard.writeText(txt); uiAlert("복사했습니다", "AI 채팅에 붙여 넣고 뒤에 원하는 날짜·조건을 말하면 됩니다.", "ok"); }
  catch(e){ uiAlert("복사가 막혔습니다 — 아래를 직접 복사하세요", txt, "warn"); }
}

/* ---------- 좌석 사용 중지 기간 ---------- */
function blkDraft(){
  if(!view.blkDraft) view.blkDraft = {
    from:todayStr(), to:todayStr(), fromTime:"", toTime:"", allDay:true, openEnded:false, note:""
  };
  return view.blkDraft;
}
function setBlk(k,v){ view.blkDraft = {...blkDraft(), [k]:v}; render(); }
function sheetBlocks(){
  const st = draft();
  const room = st.rooms.find(x=>x.id===view.form.id);
  if(!room) return `${sheetHead("좌석 사용 중지")}<div class="empty">좌석을 찾을 수 없습니다.</div>`;
  const list = roomBlocks(room).slice().sort((a,b)=>(a.from||"").localeCompare(b.from||""));
  const rows = list.length ? list.map(b=>{
    const period = b.openEnded
      ? `${dateLabel(b.from)}부터 · 해제할 때까지`
      : ((b.from===b.to || !b.to) ? dateLabel(b.from) : `${dateLabel(b.from)} ~ ${dateLabel(b.to)}`);
    const time = (b.fromTime||b.toTime) ? `${esc(b.fromTime||"영업 시작")} ~ ${esc(b.toTime||"영업 종료")}` : "하루 종일";
    return `<div class="rowitem">
      <span class="grow"><span class="t">${esc(period)}
        <span class="tag ${b.openEnded?'rust':'amber'}">${b.openEnded?"무기한":"기간"}</span></span>
        <span class="s">${time}${b.note?` · ${esc(b.note)}`:""}</span></span>
      <button class="btn sm danger" onclick="delBlock('${b.id}')">해제</button>
    </div>`;
  }).join("") : `<div class="empty">사용 중지 기간이 없습니다.</div>`;

  const d = blkDraft();
  /* 등록하기 전에, 이 기간에 걸리는 예약을 미리 보여줍니다 */
  const hits = blockHits(room, d);
  return `
    ${sheetHead(`${esc(room.name)} 사용 중지`)}
    <p class="f-note" style="margin:-6px 0 14px">공사·대관 등으로 그 기간만 자리를 잠급니다.
      예약을 막지는 않고, 그래프에 빗금과 사유가 표시됩니다.</p>
    <div class="card" style="margin-bottom:14px">${rows}</div>
    <div class="sect-title" style="margin-top:0">기간 추가</div>
    <div class="grid2">
      <label class="f"><div class="lb">시작 날짜</div>
        <input type="date" value="${d.from}" onchange="setBlk('from',this.value)"></label>
      <label class="f"><div class="lb">종료 날짜</div>
        <input type="date" value="${d.to}" ${d.openEnded?"disabled":""}
          onchange="setBlk('to',this.value)"></label>
    </div>
    <label class="chk"><input type="checkbox" ${d.openEnded?"checked":""}
      onchange="setBlk('openEnded',this.checked)">
      <span>해제할 때까지 (끝나는 날을 모를 때)</span></label>
    <label class="chk"><input type="checkbox" ${d.allDay?"checked":""}
      onchange="setBlk('allDay',this.checked)">
      <span>하루 종일</span></label>
    ${d.allDay?"":`
      <div class="grid2">
        <label class="f"><div class="lb">시작 시각</div>
          <input type="time" value="${esc(d.fromTime||"")}" onchange="setBlk('fromTime',this.value)"></label>
        <label class="f"><div class="lb">종료 시각</div>
          <input type="time" value="${esc(d.toTime||"")}" onchange="setBlk('toTime',this.value)"></label>
      </div>
      <p class="f-note" style="margin:-4px 0 12px">여러 날이면 첫날은 시작 시각부터,
        마지막 날은 종료 시각까지 잠급니다. 사이에 낀 날은 하루 종일입니다.</p>`}
    <label class="f"><div class="lb">사유</div>
      <input value="${esc(d.note||"")}" placeholder="예: 에어컨 공사, 단체 대관"
        onchange="setBlk('note',this.value)"></label>
    ${hits.length?`
      <div class="blk-hits">
        <div class="bh-t">이 기간에 예약 ${hits.length}건이 있습니다</div>
        ${hits.slice(0,8).map(r=>`<button class="bh-row" onclick="gotoRes('${r.id}')">
          <b>${dateLabel(r.date)} ${esc(hm(r.time))}</b> ${esc(r.name)} 손님 ${pplOf(r)}명
          <i>보기 ›</i></button>`).join("")}
        ${hits.length>8?`<div class="bh-more">외 ${hits.length-8}건</div>`:""}
        <div class="bh-s">그대로 등록해도 예약은 지워지지 않습니다.
          <b>경고 예약</b>으로 남아 확인에 뜹니다. 자리를 옮기려면 위에서 눌러 이동하세요.</div>
      </div>`:""}
    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="saveBlock()">사용 중지 추가</button>
    </div>`;
}
/* 입력 중인 기간에 걸리는 확정 예약 (체류 시간까지 봅니다) */
function blockHits(room, d){
  if(!d.from) return [];
  const s = store();
  const to = d.openEnded ? "9999-12-31" : (d.to || d.from);
  return s.reservations.filter(function(r){
    if(r.roomId !== room.id || r.status !== "확정") return false;
    if(r.date < d.from || r.date > to) return false;
    if(d.allDay) return true;
    const rs0 = toMin(r.time), re0 = rs0 + stayOf(r);
    const bs = (r.date === d.from && d.fromTime) ? toMin(d.fromTime) : 0;
    const be = (!d.openEnded && r.date === to && d.toTime) ? toMin(d.toTime) : 24*60;
    return rs0 < be && bs < re0;
  }).sort(function(a,b){ return (a.date+a.time).localeCompare(b.date+b.time); });
}
/* 걸리는 예약으로 바로 이동 — 그 날짜로 옮기고 예약 상세를 엽니다.
   설정에 임시본이 있으면 먼저 반영해야 대시보드가 같은 상태를 보여줍니다. */
async function gotoRes(id){
  const r = store().reservations.find(x=>x.id===id);
  if(!r) return;
  if(view.draft && !await uiConfirm("설정을 저장하고 예약으로 이동할까요?",
      "아직 '적용하기'를 누르지 않은 설정 변경이 있습니다.", {ok:"저장하고 이동"})) return;
  if(view.draft) applySettings(true);
  view.date = r.date;
  view.tab = "dash";
  openMark(id);
}
async function saveBlock(){
  const st = draft();
  const room = st.rooms.find(x=>x.id===view.form.id);
  const d = blkDraft();
  if(!room) return;
  if(!d.from) return uiAlert("시작 날짜를 정해주세요","","warn");
  if(!d.openEnded && d.to && d.to < d.from)
    return uiAlert("종료 날짜가 시작 날짜보다 빠릅니다","","warn");
  if(!d.allDay && d.fromTime && d.toTime && (d.openEnded || (d.to||d.from) === d.from) && d.toTime <= d.fromTime)
    return uiAlert("종료 시각이 시작 시각보다 빠릅니다","","warn");

  /* 이미 사용 중지인 구간과 겹치면 넣지 않습니다 — 겹친 구간이 둘이면 나중에 하나만 지워도 남아서 헷갈립니다(재아) */
  const dup = (room.blocks||[]).find(function(b){
    if(b.id === d.id) return false;
    const aS = d.from, aE = d.openEnded ? "9999-12-31" : (d.to || d.from);
    const bS = b.from, bE = b.openEnded ? "9999-12-31" : (b.to || b.from);
    if(aE < bS || bE < aS) return false;              /* 날짜가 안 겹침 */
    if(d.allDay || b.allDay) return true;              /* 하루 종일이면 겹침 */
    if(aS !== aE || bS !== bE) return true;            /* 여러 날짜면 사이 날이 종일이라 겹침 */
    return !(d.toTime <= b.fromTime || b.toTime <= d.fromTime);   /* 같은 날 시각 비교 */
  });
  if(dup) return uiAlert("이미 사용 중지가 있습니다", `${dup.from}${dup.openEnded?" ~ (기한 없음)":dup.to&&dup.to!==dup.from?` ~ ${dup.to}`:""}${dup.allDay?" 하루 종일":` ${hm(dup.fromTime)} ~ ${hm(dup.toTime)}`}${dup.note?` · ${dup.note}`:""}\n\n겹치는 기간은 넣을 수 없습니다. 기존 것을 고치거나 지운 뒤 다시 넣으세요.`, "warn");
  const hits = blockHits(room, d);
  if(hits.length){
    const lines = hits.slice(0,6).map(function(r){
      return `· ${dateLabel(r.date)} ${hm(r.time)} ${r.name} 손님 ${pplOf(r)}명`; }).join("\n");
    const ok = await uiConfirm(`${room.name}에 이 기간 예약 ${hits.length}건이 있습니다`,
      `${lines}${hits.length>6?`\n외 ${hits.length-6}건`:""}\n\n` +
      "사용 중지해도 예약은 지워지지 않습니다.\n대신 '경고 예약'으로 남아 확인에 뜹니다.",
      {ok:"그래도 중지", cancel:"취소"});
    if(!ok) return;
  }
  const rec = {
    id:"blk_"+Date.now(),
    from:d.from,
    to:d.openEnded ? "" : (d.to || d.from),
    fromTime:d.allDay ? "" : (d.fromTime||""),
    toTime:d.allDay ? "" : (d.toTime||""),
    openEnded:!!d.openEnded,
    note:(d.note||"").trim()
  };
  st.rooms = st.rooms.map(function(x){
    return x.id===room.id ? {...x, blocks:(x.blocks||[]).concat([rec])} : x; });
  logEvent("좌석 사용 중지", `${room.name} ${rec.from}${rec.to?`~${rec.to}`:"~"}${rec.note?` (${rec.note})`:""}`);
  view.blkDraft = null;
  render();
}
async function delBlock(bid){
  const st = draft();
  const room = st.rooms.find(x=>x.id===view.form.id);
  if(!room) return;
  if(!await uiConfirm2("이 사용 중지 기간을 해제할까요?")) return;
  st.rooms = st.rooms.map(function(x){
    return x.id===room.id ? {...x, blocks:(x.blocks||[]).filter(b=>b.id!==bid)} : x; });
  logEvent("좌석 사용 중지 해제", room.name);
  render();
}
function setOvr(k,v){
  view.ovrDraft = {...(view.ovrDraft||{date:todayStr(),closed:true}), [k]:v};
  render();
}
async function saveOverride(){
  const st = store().settings;
  const d = view.ovrDraft || {date:todayStr(), closed:true};
  if(!d.date) return uiAlert("날짜를 정해주세요","","warn");
  const base = hoursFor(d.date);
  const rec = d.closed
    ? {date:d.date, closed:true, note:d.note||"임시 휴무"}
    : {date:d.date, closed:false, open:d.open||base.open, close:d.close||base.close,
       bs:d.noBreak?"":(d.bs!==undefined?d.bs:base.bs), be:d.noBreak?"":(d.be!==undefined?d.be:base.be),
       lo:d.noLo?"":(d.lo||base.lo), note:d.note||"임시 운영시간"};
  st.overrides = [...(st.overrides||[]).filter(o=>o.date!==d.date), rec];
  mirrorDraft("overrides");
  if(d.holiday != null) setHolidayFlag(d.date, !!d.holiday);   /* 휴무 등록 때 공휴일 여부도 함께(재아 09-19) */
  logEvent("설정 변경", `임시 일정 ${rec.date} ${rec.closed?"휴무":"시간변경"}`);
  view.ovrDraft = null; saveData(); render();
}
async function delOverride(date){
  if(!await uiConfirm("임시 일정을 삭제할까요?", dateLabel(date), {ok:"삭제"})) return;
  const st = store().settings;
  st.overrides = st.overrides.filter(o=>o.date!==date);
  mirrorDraft("overrides");
  logEvent("설정 변경", `임시 일정 삭제 ${date}`);
  saveData(); render();
}

/* ---------- PIN 변경 ---------- */
function sheetPin(){
  if(!supaOn()) return `${sheetHead("PIN 번호 변경")}<p class="f-note">서버 미연결 빌드에서는 PIN 이 없습니다(아무 번호나 통과). 실서비스 빌드에서 바꿉니다.</p>
    <div class="sheet-actions"><button class="btn ghost" onclick="closeSheet()">닫기</button></div>`;
  return `
    ${sheetHead("PIN 번호 변경")}
    <label class="f big"><div class="lb">사장님 2차 비밀번호</div>
      <input id="pin-admin" type="password" placeholder="숫자 6자리" autocomplete="off" inputmode="numeric">
    </label>
    <label class="f big"><div class="lb">현재 PIN</div>
      <input id="pin-cur" type="password" inputmode="numeric" maxlength="4" placeholder="••••" autocomplete="off">
    </label>
    <label class="f big"><div class="lb">새 PIN (숫자 4자리)</div>
      <input id="pin-new" type="password" inputmode="numeric" maxlength="4" placeholder="••••" autocomplete="off">
    </label>
    <label class="f big"><div class="lb">새 PIN 확인</div>
      <input id="pin-new2" type="password" inputmode="numeric" maxlength="4" placeholder="••••" autocomplete="off">
    </label>
    <p class="f-note">PIN을 잊으면 관리자 비밀번호로만 되돌릴 수 있습니다. 직원들에게 공유하는 번호입니다.</p>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="savePin()">변경</button>
    </div>`;
}
/* PIN = staff 계정 비밀번호. admin 토큰으로는 남(staff)의 비밀번호를 못 바꾸므로:
   관리자 비밀번호로 admin 로그인(권한 확인) → 현재 PIN 으로 staff 로그인 → 그 토큰으로 PUT /auth/v1/user.
   지금 세션(SESSION)은 건드리지 않습니다 — 임시 토큰만 씁니다 */
async function authToken(email, password){
  var j = await sb("/auth/v1/token?grant_type=password", { method:"POST", anon:true, body:{ email:email, password:password } });
  return j.access_token;
}
async function setPassword(token, password){
  var res = await fetch(SUPA_CFG.url + "/auth/v1/user", { method:"PUT",
    headers:{ "apikey":SUPA_CFG.anonKey, "Authorization":"Bearer " + token, "Content-Type":"application/json" },
    body: JSON.stringify({ password:password }) });
  if(!res.ok){ var j = null; try{ j = await res.json(); }catch(e){} var err = new Error((j && (j.msg || j.message || j.error_description)) || ("HTTP " + res.status)); err.status = res.status; throw err; }
}
async function savePin(){
  const g = id => document.getElementById(id).value;
  const adminPw = g("pin-admin"), cur = g("pin-cur"), a = g("pin-new"), b = g("pin-new2");
  if(!/^\d{4}$/.test(a)){ await uiAlert2("PIN은 숫자 4자리여야 합니다."); return; }
  if(a !== b){ await uiAlert2("새 PIN이 서로 다릅니다."); return; }
  if(!/^\d{4}$/.test(cur)){ await uiAlert2("현재 PIN을 입력하세요."); return; }
  try{
    try{ await authToken(SUPA_CFG.adminEmail, /^\d{6}$/.test(adminPw) ? adminToPassword(adminPw) : adminPw); }
    catch(e){ if(e.status === 400){ logEvent("PIN 변경 실패", "2차 비밀번호 불일치"); await uiAlert2("사장님 2차 비밀번호가 맞지 않습니다."); return; } throw e; }
    var staffTok;
    try{ staffTok = await authToken(SUPA_CFG.staffEmail, pinToPassword(cur)); }
    catch(e){ if(e.status === 400){ logEvent("PIN 변경 실패", "현재 PIN 불일치"); await uiAlert2("현재 PIN이 맞지 않습니다."); return; } throw e; }
    await setPassword(staffTok, pinToPassword(a));
  }catch(e){
    await uiAlert("PIN을 바꾸지 못했습니다", e.network ? "서버에 연결할 수 없습니다." : e.message, "warn"); return;
  }
  pinHashSave(a);
  logEvent("PIN 변경", "성공");
  view.form = null; render();
  await uiAlert2("PIN이 변경되었습니다.\n다른 기기는 다음 로그인부터 새 PIN 을 씁니다.");
}
/* 관리자 비밀번호 변경 — admin 본인 토큰으로 */
function sheetAdminPw(){
  return `
    ${sheetHead("사장님 2차 비밀번호 변경")}
    <label class="f big"><div class="lb">현재 2차 비밀번호</div>
      <input id="apw-cur" type="password" autocomplete="off" inputmode="numeric">
    </label>
    <label class="f big"><div class="lb">새 2차 비밀번호 (숫자 6자리)</div>
      <input id="apw-new" type="password" autocomplete="off" inputmode="numeric" maxlength="6" pattern="[0-9]*">
    </label>
    <label class="f big"><div class="lb">새 2차 비밀번호 확인</div>
      <input id="apw-new2" type="password" autocomplete="off" inputmode="numeric" maxlength="6" pattern="[0-9]*">
    </label>
    <p class="f-note">2차 비밀번호는 사장님 메뉴·설정·PIN 변경처럼 사장님만 하는 일에 씁니다. 직원 PIN(4자리)과 다르게 정하세요. 잊으면 Supabase 대시보드에서만 되돌릴 수 있습니다.</p>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="saveAdminPw()">변경</button>
    </div>`;
}
async function saveAdminPw(){
  const g = id => document.getElementById(id).value;
  const cur = g("apw-cur"), a = g("apw-new"), b = g("apw-new2");
  if(!/^\d{6}$/.test(a)){ await uiAlert2("새 2차 비밀번호는 숫자 6자리여야 합니다."); return; }
  if(a !== b){ await uiAlert2("새 2차 비밀번호가 서로 다릅니다."); return; }
  try{
    var tok;
    try{ tok = await authToken(SUPA_CFG.adminEmail, /^\d{6}$/.test(cur) ? adminToPassword(cur) : cur); }
    catch(e){
      var ok2 = false;
      if(/^\d{6}$/.test(cur)){ try{ tok = await authToken(SUPA_CFG.adminEmail, cur); ok2 = true; }catch(e2){} }   /* 옛 비밀번호가 우연히 6자리였던 경우 */
      if(!ok2){ if(e.status === 400){ logEvent("2차 비밀번호 변경 실패", "현재 비밀번호 불일치"); await uiAlert2("현재 2차 비밀번호가 맞지 않습니다."); return; } throw e; }
    }
    await setPassword(tok, adminToPassword(a));
  }catch(e){
    await uiAlert("비밀번호를 바꾸지 못했습니다", e.network ? "서버에 연결할 수 없습니다." : e.message, "warn"); return;
  }
  logEvent("관리자 비밀번호 변경", "성공");
  view.form = null; render();
  await uiAlert2("사장님 2차 비밀번호가 변경되었습니다.");
}

/* ---------- 접속 기록 ---------- */
/* 관리자 비밀번호 한 번 묻기 — 서버가 없는 빌드는 그냥 통과 */
/* 09-20(재아): '사장님 아이디' 대신 사장님 2차 비밀번호(숫자 6자리). 서버 admin 계정 비밀번호 = 6자리+"00".
   아직 옛 비밀번호(자유 문자열)를 쓰는 서버면 그것도 받아 줍니다 — 6자리 → 안 되면 친 그대로 한 번 더 */
var ADMIN_UNTIL = 0;   /* '10분간 다시 묻지 않기' 를 켜고 맞힌 시각 + 10분 */
async function adminGate(what){
  if(!supaOn()) return true;
  if(ADMIN_UNTIL > Date.now()) return true;
  const r = await uiPin(what, "사장님 2차 비밀번호 6자리", 6, {keep:"10분간 다시 묻지 않기"});   /* PIN 화면과 같은 키패드(09-20) */
  if(r == null) return false;
  const pw = r.code;
  try{ await authToken(SUPA_CFG.adminEmail, /^\d{6}$/.test(pw) ? adminToPassword(pw) : pw); logEvent("관리자 확인", what + (r.keep ? " · 10분 유지" : "")); if(r.keep) ADMIN_UNTIL = Date.now() + 10 * 60000; return true; }
  catch(e){
    if(/^\d{6}$/.test(pw)){ try{ await authToken(SUPA_CFG.adminEmail, pw); logEvent("관리자 확인", what + " (옛 비밀번호)"); return true; }catch(e2){} }
    await uiAlert("2차 비밀번호가 다릅니다", "", "warn"); return false;
  }
}
function sheetSetLog(){
  const log = (store().settings._setlog || []).slice().reverse();
  const rows = log.length ? log.map(e=>{ const d = new Date(e.at); const t = isNaN(d) ? e.at : `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
    return `<div class="logrow"><span class="lg-t">${esc(t)}</span><span class="lg-ip">${esc(e.who||"")}</span><span class="lg-d">${e.items.map(esc).join("<br>")}</span></div>`; }).join("") : `<div class="empty">아직 기록이 없습니다. '적용하기' 를 누를 때부터 쌓입니다.</div>`;
  return `${sheetHead("설정 변경 내역")}<div class="logbox">${rows}</div><p class="f-note">최근 60번의 '적용하기' 까지. 운영시간·임시 일정처럼 바로 저장되는 것은 접속 기록에 남습니다.</p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
/* 설정 초기화 — 기본표(DEFAULT_DATA)로. 누님과 정한 값이 기본표에 들어간 뒤에 쓸모가 있습니다. 관리자 비밀번호 */
async function resetSettingsAll(){
  if(!await uiConfirm("설정을 처음 값으로 되돌릴까요?", "좌석·운영시간·코스·경로·문자 등 설정 전부가 기본표로 돌아갑니다. 예약은 그대로 둡니다.\n관리자 비밀번호를 물어봅니다.", {ok:"초기화"})) return;
  if(!await adminGate("설정 초기화")) return;
  const keep = store().settings._setlog || [];
  const def = migrate(deepClone(DEFAULT_DATA))[view.storeKey].settings;
  def._setlog = keep.concat([{at:new Date().toISOString(), who:SESSION ? SESSION.who : "-", items:["설정 초기화(기본표)"]}]).slice(-60);
  store().settings = def; view.draft = null;
  logEvent("설정 변경", "초기화"); takeSnapshot(); saveData(); render();
}
function sheetLogs(){
  const logs = (DATA._logs||[]).slice().reverse();
  const q = (view.logQuery||"").trim();
  const filtered = q ? logs.filter(l =>
    (l.action+" "+l.detail+" "+l.ip+" "+l.ts).toLowerCase().includes(q.toLowerCase())) : logs;
  const rows = filtered.slice(0,400).map(l=>{
    const dd = new Date(l.ts), t = isNaN(dd) ? String(l.ts).slice(0,19) : `${dd.getFullYear()}-${pad(dd.getMonth()+1)}-${pad(dd.getDate())} ${pad(dd.getHours())}:${pad(dd.getMinutes())}:${pad(dd.getSeconds())}`;   /* 저장은 UTC, 표시는 이 기기(한국) 시각 */
    return `<div class="logrow">
      <span class="lg-t">${esc(t)}</span>
      <span class="lg-ip">${esc(l.ip)}</span>
      <span class="lg-a">${esc(l.action)}</span>
      <span class="lg-d">${esc(l.detail)}</span>
    </div>`;
  }).join("");
  const tab = view.logTab || "use";
  const setlog = (store().settings._setlog || []).slice().reverse();
  const setRows = setlog.length ? setlog.map(e=>{ const d = new Date(e.at); const t = isNaN(d) ? e.at : `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
    return `<div class="logrow"><span class="lg-t">${esc(t)}</span><span class="lg-ip">${esc(e.who||"")}</span><span class="lg-d">${e.items.map(esc).join("<br>")}</span></div>`; }).join("") : `<div class="empty">아직 없습니다. '적용하기' 를 누를 때부터 쌓입니다.</div>`;
  return `
    ${sheetHead("로그")}
    <div class="seg" style="margin-bottom:10px"><button class="${tab==="use"?'on':''}" onclick="view.logTab='use'; render()">이용 로그</button><button class="${tab==="set"?'on':''}" onclick="view.logTab='set'; render()">설정 로그</button></div>
    ${tab==="use" ? `
    <div class="row" style="margin-bottom:10px">
      <input id="log-q" value="${esc(q)}" placeholder="검색 (동작·계정·날짜)" oninput="setLogQuery(this.value)" style="flex:1">
      <button class="btn" onclick="copyLogs()">전체 복사</button>
    </div>
    <div class="logbox">${rows || `<div class="empty">기록이 없습니다.</div>`}</div>
    <p class="f-note">전체 ${logs.length}건 중 ${Math.min(filtered.length,400)}건 표시. 로그인·예약 등록·상태 변경·좌석 배정·노쇼·설정 적용이 계정과 함께 쌓입니다.</p>` : `
    <div class="logbox">${setRows}</div>
    <p class="f-note">'적용하기' 마다 무엇이 어떻게 바뀌었는지. 최근 60번까지.</p>`}
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
/* ---------- 보낸 문자 ---------- */
function sheetSmsLog(){
  const all = smsLog();
  view.smsOpen = view.smsOpen || {};
  /* 8차-X(재아): 전부 접어 두고 누르면 그 문자만 폅니다. 예약은 편 안에서 엽니다 */
  const rows = all.slice(0,200).map(({r,m})=>{
    const d = new Date(m.at);
    const t = isNaN(d) ? "" : `${d.getMonth()+1}/${d.getDate()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
    const key = (r.id || "free") + "|" + m.at, on = !!view.smsOpen[key];
    return `<div class="smsrow ${on?'on':''}">
      <button class="sr-top" onclick="toggleSmsRow('${key}')">
        <span class="sr-t">${esc(t)}</span>
        <span class="sr-k ${m.kind==="접수"?'new':m.kind==="직접"?'free':'rem'}">${esc(m.kind)}${m.resent?" · 재발송":""}</span>
        <span class="sr-n">${esc(r.name)} 님</span>
        <span class="sr-p">${esc(m.to||"번호 없음")}</span>
        <span class="fh-i">${on?"▲":"▼"}</span>
      </button>
      ${on ? `<div class="smsmsg">${esc(m.text)}</div>${r.id ? `<div class="btn-row" style="margin:0 0 8px"><button class="btn sm" onclick="openMark('${r.id}')">예약 열기</button></div>` : ""}` : ""}
    </div>`;
  }).join("");
  return `
    ${sheetHead("보낸 문자")}
    <div class="mockbar">실제로 나간 문자가 아닙니다. 화면 확인용 기록입니다.</div>
    <div class="smsbox">${rows || `<div class="empty">아직 보낸 문자가 없습니다.</div>`}</div>
    <p class="f-note">전체 ${all.length}건 중 ${Math.min(all.length,200)}건 표시. 누르면 내용이 펼쳐집니다.</p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
function toggleSmsRow(key){ view.smsOpen = view.smsOpen || {}; view.smsOpen[key] = !view.smsOpen[key]; render(); }
/* ---------- 관리자 → 문자 보내기(흉내) — 예약과 무관한 임의 문자(재아) ----------
   기록은 매장 설정(smsFreeLog, 최근 50건)에 남겨 다른 기기에서도 '보낸 문자' 에 보입니다 */
function openSmsFree(){ view.form = {type:"smsfree"}; view.smsFree = {to:"", name:"", text:""}; render(); }
function sheetSmsFree(){
  const f = view.smsFree || {to:"", name:"", text:""};
  return `
    ${sheetHead("문자 보내기")}
    <div class="mockbar">지금은 <b>흉내만</b> 냅니다. 실제로 문자가 나가지 않습니다.</div>
    <label class="f"><div class="lb">받는 번호</div><input id="sf-to" type="tel" value="${esc(f.to)}" placeholder="010-0000-0000"></label>
    <label class="f"><div class="lb">받는 분 (선택)</div><input id="sf-name" value="${esc(f.name)}" placeholder="홍길동"></label>
    <label class="f"><div class="lb">내용</div><textarea id="sf-text" rows="7" placeholder="보낼 내용">${esc(f.text)}</textarea></label>
    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="sendSmsFree()">보내기 (흉내)</button>
    </div>`;
}
async function sendSmsFree(){
  const g = id => { const el = document.getElementById(id); return el ? el.value.trim() : ""; };
  const to = g("sf-to"), name = g("sf-name"), text = g("sf-text");
  view.smsFree = {to, name, text};
  if(!to) return uiAlert("받는 번호를 입력하세요", "", "warn");
  if(!text) return uiAlert("내용을 입력하세요", "", "warn");
  if(!await uiConfirm(`${name ? name + " 님 " : ""}${to} 으로 보낼까요?`, text, {ok:"보내기", tone:"ok"})) return;
  if(readonlyBlock()) return;
  const st = store().settings;
  st.smsFreeLog = [{ at:new Date().toISOString(), to, name, text }].concat(st.smsFreeLog || []).slice(0, 50);
  mirrorDraft("smsFreeLog");
  logEvent("문자 보내기(흉내)", `${to} ${name} ${text.slice(0, 40)}`);
  view.form = null; view.smsFree = null; saveData(); render();
  uiAlert("문자를 보낸 것으로 기록했습니다", "실제 발송은 업체 연동 뒤에 붙습니다.", "ok");
}
function setLogQuery(v){
  view.logQuery = v;
  const box = document.querySelector(".logbox");
  if(box) box.innerHTML = sheetLogs().split('<div class="logbox">')[1].split("</div>\n    <p")[0];
}
async function copyLogs(){
  if(!await adminGate("접속 기록 전체 복사")) return;   /* 전화번호·이름이 들어 있어 관리자 비밀번호(재아) */
  const txt = (DATA._logs||[]).map(l=>{ const d = new Date(l.ts); const t = isNaN(d) ? l.ts : `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`; return `${t}\t${l.ip}\t${l.store}\t${l.action}\t${l.detail}\t${l.ua}`; }).join("\n");
  if(!navigator.clipboard) return uiAlert("복사 실패","클립보드를 쓸 수 없습니다.","warn");
  navigator.clipboard.writeText(txt).then(
    ()=>uiAlert("복사 완료","접속 기록을 클립보드에 복사했습니다.","ok"),
    ()=>uiAlert("복사 실패","클립보드에 접근할 수 없습니다.","warn"));
}

/* ---------- 예약률 추이 (팝업) ---------- */
function sheetRate(){
  const d = view.rateEnd || view.date;
  return `
    <div class="wide-sheet">
    ${sheetHead("예약률 추이")}
    <div class="chart-nav">
      <button class="btn sm" onclick="rateMove(-7)">&lsaquo; 이전 주</button>
      <span class="muted" style="flex:1; text-align:center; font-size:13px">${dateLabel(shiftDate(d,-20))} – ${dateLabel(d)}</span>   <!-- 그래프가 21일치(rateChart(d,21))라 첫날은 d−20 -->
      <button class="btn sm" onclick="rateMove(7)">다음 주 &rsaquo;</button>
    </div>
    ${rateChart(d, 21)}
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>
    </div>`;
}

