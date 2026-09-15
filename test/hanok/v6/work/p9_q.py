# -*- coding: utf-8 -*-
"""8차-Q — 재아 목록 2차: 문자 안내 칸(문구·색·흉내 삭제·보내기 삭제·접힘 유지·네이버 안 보냄 설정), 취소→노쇼 되묻기(설정 기준),
   노쇼 관리(검색·행 눌러 상세), 관리자 폴드(PIN·관리자 비번·접속 기록·설정 변경 내역·설정 초기화), 설정 변경 내역 기록,
   테이블 층 상관없음(마법사 카드·네이버 기본)·설정 테이블 한 목록(층 구분 없이 우선순위), 붙임은 이어진 짝(chain)도 허용,
   네이버 미리보기 행 편집(건너뛰기·좌석)·등록 전 경고, 유아의자 확인 필요 메모, 인트로 클릭에도 전체화면"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 문자 안내 칸 ----------
s = R(s, """  return `
    <div class="sms-box">
      <div class="sb-t">문자 안내 <span class="sb-mock">흉내 · 실제로 나가지 않습니다</span></div>
      ${row("접수 문자",
        sent ? `<b>보냄</b> ${esc(stamp(sent))}${sent.resent?" · 재발송":""}`
             : (r.phone ? `<i>기록 없음</i>` : `<i>번호 없음</i>`))}
      ${row("재안내 문자",
        rs.state==="보냄"     ? `<b>보냄</b> ${esc(stamp(rs.rec))}${rs.rec.resent?" · 재발송":""}`
      : rs.state==="예정"     ? `${esc(planTxt)} 예정`
      : rs.state==="발송대기" ? `${esc(planTxt)} · 곧 나감`
      : `<i>안 나감</i>`,
        (rs.state!=="보냄" && rs.state!=="예정" && rs.state!=="발송대기") ? "bad" : "")}
      ${why ? `<div class="sb-why">${esc(why)}</div>` : ""}
      <div class="sb-btns">
        <button class="btn sm" onclick="smsPreview('${r.id}','접수')">접수 문자 보기</button>
        <button class="btn sm" onclick="smsPreview('${r.id}','재안내')">재안내 문자 보기</button>
      </div>
      <p class="sb-note">문안을 열면 그 자리에서 다시 보낼 수 있습니다.</p>
    </div>`;""",
"""  /* 8차-Q(재아): 상태 문구를 전송 완료(초록·시각) / 전송 예정(검정·시각) / 전송 건너뜀(노랑·사유) / 전송 실패(빨강·사유) 넷으로 통일.
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
    </div>`;""")
# 미리보기: 보내기 없이 닫기만(우상단 X 는 모달에 없으므로 '닫기' 버튼 하나)
s = R(s, """  if(!(r.phone||"").trim())
    return await uiAlert(kind + " 문자", body + "\\n\\n전화번호가 없어 보낼 수 없습니다.", "warn");
  const ok = await uiConfirm(kind + " 문자", r.phone + "\\n\\n" + body,
    { ok:"이 문자 보내기", cancel:"닫기" });
  if(!ok) return;
  smsSend(r, kind, smsCfg().remindOffset, true);
  logEvent("문자 재발송", r.date + " " + r.time + " " + r.name + " " + kind);
  saveData(); render();
}""", """  /* 8차-Q: '이 문자 보내기' 는 없앴습니다 — 문안 확인만. 재발송이 필요해지면 실발송 붙일 때 같이 */
  await uiAlert(kind + " 문안", (r.phone || "전화번호 없음") + "\\n\\n" + body, "ok");
}""")
s = R(s, """    "\\n---\\n지금은 흉내만 냅니다. 실제로 나가지 않습니다.";""", """    "\\n---";""")
# 접힘 상태 유지 + 설정: 네이버 예약은 문자 안 보냄
s = R(s, """    <details class="sms-fold"><summary>문자 안내 <span class="sb-mock">흉내</span></summary>${smsBox(r)}</details>""",
         """    <details class="sms-fold" ${view.smsOpen?"open":""} ontoggle="view.smsOpen=this.open"><summary>문자 안내</summary>${smsBox(r)}</details>""")
s = R(s, """var SMS_DEFAULT = {
  on:true,""", """var SMS_DEFAULT = {
  on:true,
  skipNaver:true,         /* 네이버 예약은 네이버가 문자를 보내므로 우리는 안 보냄(재아) */""")
s = R(s, """.tk.end b{transform:translateX(-100%); margin-left:-2px}""", """.tk.end b{transform:translateX(-100%); margin-left:-2px}
.sm-done{color:var(--pine); font-weight:600} .sm-plan{color:var(--text); font-weight:600} .sm-skip{color:#8A6D1F; font-weight:600} .sm-fail{color:var(--rust); font-weight:600}""")

# ---------- 취소 → 노쇼 되묻기 (설정 기준) ----------
s = R(s, """async function setStatus(id,status){
  const s=store();
  const rec = s.reservations.find(r=>r.id===id);
  if(status==="취소" && rec && rec.status!=="취소"){""", """/* 취소하려는 시점이 설정한 기준 안이면(당일 등) '노쇼에 해당' 되묻기. 답: "노쇼" | "취소" | null(그만) */
async function askNoshowOnCancel(rec){
  const rule = store().settings.noshowCancelRule || "none";
  if(rule === "none" || !rec || rec.status === "취소") return "취소";
  const now = new Date(), t = new Date(rec.date + "T" + rec.time + ":00");
  const hoursLeft = (t - now) / 3600000;
  const hit = rule === "after" ? hoursLeft <= 0
            : rule === "sameday" ? rec.date === todayStr() || hoursLeft <= 0
            : rule === "day1" ? rec.date <= shiftDate(todayStr(), 1)
            : rule === "day2" ? rec.date <= shiftDate(todayStr(), 2)
            : rule === "hours" ? hoursLeft <= (store().settings.noshowCancelHours || 3)
            : false;
  if(!hit) return "취소";
  const label = {after:"예약 시각이 지난 뒤의 취소", sameday:"당일 취소", day1:"전날부터의 취소", day2:"이틀 전부터의 취소", hours:`${store().settings.noshowCancelHours||3}시간 안의 취소`}[rule];
  const r = await uiChoice(`${label}는 노쇼에 해당합니다`, `${rec.time} ${rec.name} 손님 · ${pplText(rec)}\\n어떻게 처리할까요?`, [["노쇼로 처리","노쇼"],["취소로 처리","취소"]]);
  return r;
}
async function setStatus(id,status){
  const s=store();
  const rec = s.reservations.find(r=>r.id===id);
  if(status==="취소" && rec && rec.status!=="취소"){
    const ans = await askNoshowOnCancel(rec); if(ans == null) return; status = ans;
  }
  if(status==="취소" && rec && rec.status!=="취소"){""")
# 세 갈래 확인창(uiChoice)
s = R(s, """/* 한 줄 입력 팝업 — 관리자 비밀번호 등. 취소면 null */""", """/* 선택지 팝업 — [[라벨, 값], …]. 취소면 null */
function uiChoice(title, msg, choices){
  return new Promise(res => { modalReplace({mode:"choice", title, msg, tone:"warn", choices, cancel:"그만두기", res}); });
}
/* 한 줄 입력 팝업 — 관리자 비밀번호 등. 취소면 null */""")
s = R(s, """          ${m.mode==="confirm"||m.mode==="prompt"?`<button class="btn" onclick="modalAnswer(${m.mode==="prompt"?"null":"false"})">${esc(m.cancel)}</button>`:""}
          <button class="btn ${m.tone==="warn"?"danger-fill":"primary"}" onclick="${m.mode==="prompt"?"modalPromptAnswer()":"modalAnswer(true)"}">
            ${m.mode==="confirm"||m.mode==="prompt"?esc(m.ok):"확인"}</button>""",
"""          ${m.mode==="confirm"||m.mode==="prompt"||m.mode==="choice"?`<button class="btn" onclick="modalAnswer(${m.mode==="confirm"?"false":"null"})">${esc(m.cancel)}</button>`:""}
          ${m.mode==="choice" ? (m.choices||[]).map(([lb,v],i)=>`<button class="btn ${i===0?"danger-fill":"primary"}" onclick="modalAnswer(${JSON.stringify(v)})">${esc(lb)}</button>`).join("") :
          `<button class="btn ${m.tone==="warn"?"danger-fill":"primary"}" onclick="${m.mode==="prompt"?"modalPromptAnswer()":"modalAnswer(true)"}">
            ${m.mode==="confirm"||m.mode==="prompt"?esc(m.ok):"확인"}</button>`}""")
# 수정 시트 저장에서 상태를 취소로 바꾼 경우도 같은 되묻기
s = R(s, """  if(old){
    /* 무엇이 바뀌었는지 남깁니다 (사장님의 '파란 글씨' — 변동 이력 참고) */
    const d = diffRes(old, rec);""", """  if(old && old.status !== "취소" && rec.status === "취소"){ const ans = await askNoshowOnCancel(old); if(ans == null) return; rec.status = ans; }
  if(old){
    /* 무엇이 바뀌었는지 남깁니다 (사장님의 '파란 글씨' — 변동 이력 참고) */
    const d = diffRes(old, rec);""")
s = R(s, """    <label class="f"><div class="lb">노쇼 경고 기준</div>""", """    <label class="f"><div class="lb">취소를 노쇼로 볼 기준</div>
      <div class="seg">${[["none","안 함"],["sameday","당일"],["day1","전날부터"],["day2","이틀 전부터"],["hours","N시간 전"],["after","시각 지난 뒤"]].map(([v,l])=>`<button class="${(st.noshowCancelRule||"none")===v?'on':''}" onclick="setSetting('noshowCancelRule','${v}')">${l}</button>`).join("")}</div>
      <div class="f-note">기준 안에서 취소하면 '노쇼에 해당합니다 — 노쇼 / 취소' 를 되묻습니다. 취소는 언제나 남겨 둡니다(어제 취소를 오늘 입력할 수도 있으니).${st.noshowCancelRule==="hours"?` 지금 기준 <button class="numbtn sm" onclick="openNum('noshowCancelHours','몇 시간 전부터',1,48)">${st.noshowCancelHours||3}시간</button>`:""}</div></label>
    <label class="f"><div class="lb">노쇼 경고 기준</div>""")

# ---------- 노쇼 관리: 검색 버튼, 행 눌러 상세 ----------
s = R(s, """  return `
    ${sheetHead("노쇼 관리")}
    ${stat}""", """  return `
    ${sheetHead("노쇼 관리")}
    <div class="btn-row" style="margin:-4px 0 10px"><button class="btn sm" onclick="openSearch()">🔍 예약 검색</button></div>
    ${stat}""")
s = R(s, """    <div class="rowitem">
      <span class="grow"><span class="t">${dateLabel(r.date)} ${esc(r.time)} · ${esc(r.name)}${k && cnt[k]>1?` <span class="tag rust">노쇼 ${cnt[k]}회</span>`:""}${ex?` <span class="tag">경고 제외</span>`:""}</span>
        <span class="s">${pplText(r)} · ${esc(r.phone||"연락처 없음")} · ${esc(resSeatLabel(r))}</span></span>""",
"""    <div class="rowitem">
      <button class="grow tap-plain" onclick="openMark('${r.id}')" title="예약 상세"><span class="t">${dateLabel(r.date)} ${esc(r.time)} · ${esc(r.name)}${k && cnt[k]>1?` <span class="tag rust">노쇼 ${cnt[k]}회</span>`:""}${ex?` <span class="tag">경고 제외</span>`:""}</span>
        <span class="s">${pplText(r)} · ${esc(r.phone||(r.phoneTail?`***-****-${r.phoneTail} (네이버)`:"연락처 없음"))} · ${esc(resSeatLabel(r))}</span></button>""")
s = R(s, """.tk.end b{transform:translateX(-100%); margin-left:-2px}""", """.tk.end b{transform:translateX(-100%); margin-left:-2px}
.tap-plain{background:none; border:none; padding:0; text-align:left; font:inherit; color:inherit; cursor:pointer; display:flex; flex-direction:column; min-width:0}""")

# ---------- 관리자 폴드 ----------
s = R(s, """    ${sec("security","보안","PIN", secBody)}""", """    ${sec("admin","관리자",`PIN · 비밀번호 · 기록`, adminBody)}""")
s = R(s, """  const secBody = `
    <div class="btn-row">
      <button class="btn" onclick="openPin()">PIN 번호 변경</button>
      ${supaOn() ? `<button class="btn" onclick="openAdminPw()">관리자 비밀번호 변경</button>` : ""}

    </div>""", """  const adminBody = `
    <div class="btn-row">
      <button class="btn" onclick="openPin()">PIN 번호 변경</button>
      ${supaOn() ? `<button class="btn" onclick="openAdminPw()">관리자 비밀번호 변경</button>` : ""}
      <button class="btn" onclick="openLogs()">접속 기록</button>
      <button class="btn" onclick="openSetLog()">설정 변경 내역</button>
      <button class="btn danger" onclick="resetSettingsAll()">설정 초기화</button>
    </div>""")
s = R(s, """  const etcBody = `
    <div class="btn-row">
      <button class="btn" onclick="openNoshow()">노쇼 관리</button>
      <button class="btn" onclick="openLogs()">접속 기록</button>
    </div>
    <p class="f-note">
      <b>접속 기록</b> — 누가 언제 무엇을 고쳤는지가 남습니다.
      예약이 왜 바뀌었는지 되짚을 때 보세요. 최근 ${LOG_MAX}건까지 보관합니다.</p>`;""", """  const etcBody = `
    <div class="btn-row">
      <button class="btn" onclick="openNoshow()">노쇼 관리</button>
    </div>`;""")
# 설정 변경 내역: applySettings 때 이전/이후 차이를 기록(_setlog, 서버 settings 안에 최근 60건)
s = R(s, """function applySettings(){
  if(!view.draft) return;
  if(readonlyBlock()) return;
  store().settings = deepClone(view.draft);
  logEvent("설정 변경", "적용");""", """/* 설정 두 개의 차이를 '키: 이전 → 이후' 로 — 관리자 → 설정 변경 내역 */
function settingsDiff(a, b){
  const out = [], keys = {}; Object.keys(a||{}).concat(Object.keys(b||{})).forEach(k=>{ keys[k]=1; });
  const NAME = {rooms:"좌석", joins:"룸 합침", schedules:"운영시간", overrides:"임시 일정", holidays:"공휴일 추가", holidaysOff:"공휴일 제외", courseGroups:"코스 구성", sources:"예약경로", sms:"문자 안내", displayRows:"디스플레이 배치", tvType:"디스플레이 형식", groupSize:"단체 기준", noshowExcluded:"노쇼 경고 제외", uiZoom:"화면 크기", closeGapMin:"겹침 경고", noshowWarnCount:"노쇼 경고 기준", noshowCancelRule:"취소→노쇼 기준", tvAd:"광고 영상", holidayAsWeekend:"공휴일=주말", minCountAdultsOnly:"정원 기준", chairDefault:"유아의자 기본", loSoon:"임박 기준", breakMode:"브레이크 방식", _setlog:null};
  Object.keys(keys).forEach(k=>{
    if(NAME[k] === null) return;
    const x = JSON.stringify(a ? a[k] : undefined), y = JSON.stringify(b ? b[k] : undefined);
    if(x === y) return;
    const short = v => { if(v === undefined) return "없음"; const t = typeof v === "string" ? v : JSON.stringify(v); return t.length > 60 ? t.slice(0,57) + "…" : t; };
    out.push(`${NAME[k] || k}: ${short(a ? a[k] : undefined)} → ${short(b ? b[k] : undefined)}`);
  });
  return out;
}
function applySettings(){
  if(!view.draft) return;
  if(readonlyBlock()) return;
  const before = store().settings, after = deepClone(view.draft);
  const diff = settingsDiff(before, after);
  after._setlog = (before._setlog || []).concat(diff.length ? [{at:new Date().toISOString(), who:SESSION ? SESSION.who : "-", items:diff}] : []).slice(-60);
  store().settings = after;
  logEvent("설정 변경", diff.length ? diff.join(" / ").slice(0, 300) : "적용(변경 없음)");""")
s = R(s, """function sheetLogs(){""", """function openSetLog(){ view.form = {type:"setlog"}; render(); }
function sheetSetLog(){
  const log = (store().settings._setlog || []).slice().reverse();
  const rows = log.length ? log.map(e=>{ const d = new Date(e.at); const t = isNaN(d) ? e.at : `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
    return `<div class="logrow"><span class="lg-t">${esc(t)}</span><span class="lg-ip">${esc(e.who||"")}</span><span class="lg-d">${e.items.map(esc).join("<br>")}</span></div>`; }).join("") : `<div class="empty">아직 기록이 없습니다. '적용하기' 를 누를 때부터 쌓입니다.</div>`;
  return `${sheetHead("설정 변경 내역")}<div class="logbox">${rows}</div><p class="f-note">최근 60번의 '적용하기' 까지. 운영시간·임시 일정처럼 바로 저장되는 것은 접속 기록에 남습니다.</p>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
/* 설정 초기화 — 기본표(DEFAULT_DATA)로. 누님과 정한 값이 기본표에 들어간 뒤에 쓸모가 있습니다. 관리자 비밀번호 */
async function resetSettingsAll(){
  if(!await uiConfirm("설정을 처음 값으로 되돌릴까요?", "좌석·운영시간·코스·경로·문자 등 설정 전부가 기본표로 돌아갑니다. 예약은 그대로 둡니다.\\n관리자 비밀번호를 물어봅니다.", {ok:"초기화"})) return;
  if(!await adminGate("설정 초기화")) return;
  const keep = store().settings._setlog || [];
  const def = migrate(deepClone(DEFAULT_DATA))[view.storeKey].settings;
  def._setlog = keep.concat([{at:new Date().toISOString(), who:SESSION ? SESSION.who : "-", items:["설정 초기화(기본표)"]}]).slice(-60);
  store().settings = def; view.draft = null;
  logEvent("설정 변경", "초기화"); takeSnapshot(); saveData(); render();
}
function sheetLogs(){""")
s = R(s, """tedit:sheetTableEdit, naver:sheetNaver, logs:sheetLogs,""", """tedit:sheetTableEdit, naver:sheetNaver, setlog:sheetSetLog, logs:sheetLogs,""")

# ---------- 테이블: 층 상관없음 + 설정 한 목록 ----------
s = R(s, """    const floors = tableFloors();
    body = `<div class="sgrid floors">${floors.map(fl=>{""", """    const floors = tableFloors();
    const anyFit = WZ.time ? floorFit(null, WZ.date, WZ.time, total) : null;
    const anyBad = anyFit && anyFit.state !== "ok";
    body = `<div class="sgrid floors">
      <button class="scell ${WZ.seat==='table-any'?'on':''} ${anyBad?'warned busy':''}" onclick="wzSeat('table-any')">
        <span class="sn">층 상관없음</span><span class="sc">사장님 순서대로 자동</span>
        <span class="avail ${anyBad?'warn':'free'}">${!anyFit ? "시간을 먼저" : anyFit.state==="ok" ? "자리 있음" : anyFit.state==="split" ? "나눠 앉기" : "자리 없음"}</span></button>
      ${floors.map(fl=>{""")
s = R(s, """function floorTables(fl){ return (store().settings.rooms || []).filter(t => isTable(t) && (t.floor || "") === (fl || "")); }""",
         """function floorTables(fl){ return (store().settings.rooms || []).filter(t => isTable(t) && (fl == null || (t.floor || "") === (fl || ""))); }   /* fl == null → 전체 */""")
s = R(s, """function floorMaxParty(fl, date, time, excludeId){""", """/* fl == null 은 '층 상관없음' — findSeat 에 floor 를 안 넘겨 전체 테이블(사장님 순서)로 */""" + "\nfunction floorMaxParty(fl, date, time, excludeId){")
# table-any 미리보기·wzSeat 처리: /^table:/ 만 잡던 곳에 table-any 도
s = R(s, """  if(/^table:/.test(v)){
    const fl = v.slice(6), fit = floorFit(fl, WZ.date, WZ.time, people);""", """  if(/^table:/.test(v) || v === "table-any"){
    const fl = v === "table-any" ? null : v.slice(6), fit = floorFit(fl, WZ.date, WZ.time, people);""")
s = R(s, """  if(isTablePref(r.seatPref)) return prefFloor(r.seatPref);
  return undefined;""", """  if(isTablePref(r.seatPref)) return prefFloor(r.seatPref);   /* table-any → null(층 미정) */
  return undefined;""")
s = R(s, """  if(seat==="hall-any" || seat==="table-any") return "테이블";""", """  if(seat==="hall-any" || seat==="table-any") return "테이블 (층 상관없음)";""")
# 설정 테이블 탭: 층 구분 없이 한 목록, 순서는 전체 우선순위
s = R(s, """    ${floorsT.map(fl=>{ const list = tables.filter(t=>(t.floor||"")===fl); return `<div class="lbl" style="margin:10px 0 4px">${esc(fl||"층 없음")}</div>${list.map(t=>tableRowHtml(list, t)).join("")}`; }).join("")}""",
"""    <p class="f-note" style="margin:0 0 8px">층 구분 없이 <b>위에서부터 좋은 자리</b> 순서입니다(▲▼). 층은 표시·안내용. 1층 창가 다음이 지하 여포일 수도 있으니 섞어서 정하세요.</p>
    ${tables.map(t=>tableRowHtml(tables, t)).join("")}""")
s = R(s, """  const same = arr.filter(x=>x.type===r.type && (isRoom(r) || (x.floor||"")===(r.floor||"")));""",
         """  const same = arr.filter(x=>x.type===r.type);   /* 테이블은 층 구분 없이 전체 순서(재아) */""")
s = R(s, """        <label class="tbl-in">층
          <input value="${esc(r.floor||"")}" placeholder="1층" style="width:60px" onchange="setRoomText('${r.id}','floor',this.value)"></label>
        <button class="btn sm ${roomBlocks(r).length?'danger':''}" onclick="openBlocks('${r.id}')">${roomBlocks(r).length?`사용 중지 ${roomBlocks(r).length}건`:"사용 중지"}</button>""",
"""        <label class="tbl-in">층
          <input value="${esc(r.floor||"")}" placeholder="1층" style="width:60px" onchange="setRoomText('${r.id}','floor',this.value)"></label>
        <button class="btn sm ${roomBlocks(r).length?'danger':''}" onclick="openBlocks('${r.id}')">${roomBlocks(r).length?`사용 중지 ${roomBlocks(r).length}건`:"사용 중지"}</button>""")
s = R(s, """          <span class="s">${t.seats||4}인석${t.capacity&&t.capacity!==t.seats?` · 최대 ${t.capacity}`:""}${roomMin(t)?` · 최소 ${roomMin(t)}`:""}${blockSummary(t)}</span>""",
         """          <span class="s">${esc(t.floor||"층 없음")} · ${t.seats||4}인석${t.capacity&&t.capacity!==t.seats?` · 최대 ${t.capacity}`:""}${roomMin(t)?` · 최소 ${roomMin(t)}`:""}${blockSummary(t)}</span>""")

# ---------- 붙임: 이어진 짝(chain)도 허용 — A-B, B-C 면 A+B+C 를 한 줄로 ----------
s = R(s, """        if(!combo.every(c=>canJoinTables(c.id, x.id))) return;""", """        if(!combo.some(c=>canJoinTables(c.id, x.id))) return;   /* 하나라도 이어져 있으면(한 줄로 붙는 자리) — 전부 서로 붙을 필요는 없음 */""")

# ---------- 네이버: 기본 table-any, 유아의자 확인, 미리보기 행 편집 ----------
s = R(s, """    if(!ex) return Object.assign({ok:true, kind:"new", msg:`${r.when.date} ${r.when.time} ${r.people}명 ${r.isRoomProd?"룸":"테이블"}${r.status!=="확정"?" · "+r.status:""}${r.request?" · ⚠ 요청사항 있음 — 확인":""}`}, r);""",
"""    if(!ex){
      /* 등록 전 자리 경고 — 룸 미정이면 빈 룸이 있는지, 테이블이면 앉힐 수 있는지 */
      let seatWarn = "";
      if(r.status === "확정"){
        if(r.isRoomProd){ if(!findSeat({date:r.when.date, time:r.when.time, people:r.people, kind:"room-any"})) seatWarn = "빈 룸 없음"; }
        else { const ff = floorFit(null, r.when.date, r.when.time, r.people); if(ff.state === "none") seatWarn = "테이블 자리 없음"; else if(ff.state === "split") seatWarn = "나눠 앉음"; }
      }
      return Object.assign({ok:true, kind:"new", seatWarn, seat: r.isRoomProd ? "room-any" : "table-any", skip:false,
        msg:`${r.when.date} ${r.when.time} ${r.people}명${r.status!=="확정"?" · "+r.status:""}${r.request?" · ⚠ 요청사항 있음":""}${seatWarn?" · ⚠ "+seatWarn:""}`}, r);
    }""")
s = R(s, """  const res = n.result ? `<div class="bulk-res">${n.result.map(x=>`<div class="bulk-row ${x.ok?(x.kind==="skip"?"":"ok"):"bad"}"><span class="bulk-ln">${x.n}</span><span class="grow">${esc(x.text)}</span><span class="bulk-msg">${x.ok?`${x.kind==="new"?"＋ 새로":x.kind==="update"?"↻ 고침":"＝ 같음"} · ${esc(x.msg)}`:`✗ ${esc(x.msg)}`}</span></div>`).join("")}</div>` : "";""",
"""  /* 행마다: 건너뛰기 · 좌석 고르기(룸 미정/특정 룸/테이블). 자리 경고가 있으면 붉은 줄 — 등록 전에 손볼 수 있게(재아) */
  const st = store().settings;
  const seatOpts = (x) => `<select class="nv-seat" onchange="view.naver.result[${x.n-1}].seat=this.value">
      <option value="room-any" ${x.seat==="room-any"?"selected":""}>룸 미정(자동)</option>
      ${st.rooms.filter(isRoom).map(rm=>`<option value="${rm.id}" ${x.seat===rm.id?"selected":""}>${esc(rm.name)} 룸</option>`).join("")}
      <option value="table-any" ${x.seat==="table-any"?"selected":""}>테이블(층 상관없음)</option>
      ${tableFloors().map(fl=>`<option value="table:${fl}" ${x.seat==="table:"+fl?"selected":""}>${esc(floorLabel(fl))}</option>`).join("")}
    </select>`;
  const res = n.result ? `<div class="bulk-res">${n.result.map(x=>`<div class="bulk-row ${x.ok?(x.kind==="skip"?"":(x.seatWarn||x.request?"warn":"ok")):"bad"} ${x.skip?"skipped":""}"><span class="bulk-ln">${x.n}</span><span class="grow">${esc(x.text)}${x.request?`<div class="nv-req">요청: ${esc(x.request)}</div>`:""}${x.ok&&x.kind==="new"?`<div class="nv-ctl"><label class="chk" style="margin:0"><input type="checkbox" ${x.skip?"checked":""} onchange="view.naver.result[${x.n-1}].skip=this.checked"><span>건너뛰기</span></label>${seatOpts(x)}</div>`:""}</span><span class="bulk-msg">${x.ok?`${x.kind==="new"?"＋ 새로":x.kind==="update"?"↻ 고침":"＝ 같음"} · ${esc(x.msg)}`:`✗ ${esc(x.msg)}`}</span></div>`).join("")}</div>` : "";""")
s = R(s, """  n.result.filter(x=>x.ok && x.kind !== "skip").forEach(r=>{""", """  n.result.filter(x=>x.ok && x.kind !== "skip" && !x.skip).forEach(r=>{""")
s = R(s, """      const rec = { id:newId("res"), naverNo:r.no, date:r.when.date, time:r.when.time, name:r.name, phone:r.phone||"", people:r.people, infants:r.infants, chairs:0,
        roomId:null, extraIds:[], seatPref: r.isRoomProd ? "room-any" : "table-any", tentativeRoomId:null, tentativeExtra:[], tentativeSplit:false,""",
"""      const pick = r.seat || (r.isRoomProd ? "room-any" : "table-any"), pickedRoom = seatById(pick) ? pick : null;
      const rec = { id:newId("res"), naverNo:r.no, date:r.when.date, time:r.when.time, name:r.name, phone:r.phone||"", phoneTail:r.phoneTail||"", people:r.people, infants:r.infants, chairs:0,
        roomId:pickedRoom, extraIds:[], seatPref: pickedRoom ? null : pick, tentativeRoomId:null, tentativeExtra:[], tentativeSplit:false,""")
s = R(s, """    const memoTail = `네이버 예약번호 ${r.no}${r.phoneTail?` · 전화 ****${r.phoneTail}`:""}""", """    const memoTail = `네이버 예약번호 ${r.no}${r.phoneTail?` · 전화 ****${r.phoneTail}`:""}${r.infants?" · 유아의자 확인 필요":""}""")
s = R(s, """.tk.end b{transform:translateX(-100%); margin-left:-2px}""", """.tk.end b{transform:translateX(-100%); margin-left:-2px}
.bulk-row.warn{background:#FBEFEC} .bulk-row.skipped{opacity:.45}
.nv-req{font-size:var(--fs-label); color:var(--text-2); margin-top:2px; white-space:pre-wrap}
.nv-ctl{display:flex; gap:var(--s8); align-items:center; margin-top:4px} .nv-ctl select{padding:2px 6px; font-size:var(--fs-label); min-height:0}""")
# 상세 화면 전화 표시: 네이버 뒷자리
s = R(s, """      ${r.phone?`<div class="mi-s">${esc(r.phone)}</div>`:""}""", """      ${r.phone?`<div class="mi-s">${esc(r.phone)}</div>`:(r.phoneTail?`<div class="mi-s">***-****-${esc(r.phoneTail)} <small class="muted">(네이버 예약 — 번호는 네이버에서)</small></div>`:"")}""")

# ---------- 인트로 클릭에도 전체화면 ----------
s = R(s, """function endIntro(){ clearIntro(); INTRO = null; render(); }""", """function endIntro(){ tryFullscreen(); clearIntro(); INTRO = null; render(); }   /* 인트로를 눌러 건너뛸 때도 전체화면 시도(손짓이 있으니) */""")
L.js_check(s)
L.save(s)
print("p9_q ok")
