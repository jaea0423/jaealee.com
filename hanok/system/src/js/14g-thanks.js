/* ---------- 감사 문자 (thanks_sms, 18차 재아) ----------
   다녀간 손님께 다음 날 보내는 짧은 감사 문자. **'방문' 으로 확인된 예약만** 대상(안 온 손님께는 안 감).
   글은 Gemini 가 예약 정보(이름·인원·룸/테이블·시간·요청·어린이·손님 메모)와 사장님 키워드(팔순·생일·회식·날씨…)로 만듭니다 —
   과하지 않고 광고 같지 않게. 마음에 안 들면 다시 만들기 / 직접 고치기 / 기본 양식. AI 가 막히면(키 없음·한도·오류) 기본 양식으로.
   보내기는 '예약 발송' — thanks_sms 표에 넣고 보낼 시각이 되면 1분 갱신(thanksTick)이 보냅니다(문자 업체 연결 전엔 흉내).
   Gemini 키는 빌드 설정(supabase.*.json 의 geminiKey → SUPA_CFG)에 박음(재아 09-19). 화면에서 못 바꿈. 유료 키라 구글 콘솔에서
   'HTTP 리퍼러 제한(jaealee.com/*)' 과 하루 한도를 걸어 두는 것이 안전장치. 모델은 3.6-flash → 안 되면 flash-latest → flash-lite 순으로 시도. */
var TH = null;
var TH_MODELS = ["gemini-3.6-flash", "gemini-flash-latest", "gemini-flash-lite-latest"];   /* gemini-2.5-flash 는 새 키에서 404 (2026-09 확인) */
var TH_DEF_MODEL = TH_MODELS[0];
function thCfg(){ var a = store().settings.ai || {}; return { key: (typeof SUPA_CFG !== "undefined" && SUPA_CFG && SUPA_CFG.geminiKey) || "", model: a.model || TH_DEF_MODEL, hour: a.thanksHour || "11:00", common: a.thanksCommon || "" }; }
/* 모델마다 '생각(thinking)' 을 끄는 설정이 다름: 3.x 는 thinkingLevel, 2.5 계열(flash-latest)은 thinkingBudget 0. 안 끄면 토큰을 생각에 다 써 본문이 잘림 */
function thGenCfg(model){
  var g = { temperature:0.9, maxOutputTokens:2048 };
  if(/gemini-3/.test(model)) g.thinkingConfig = { thinkingLevel:"minimal" };
  else if(/flash-latest|2\.5/.test(model) && !/lite/.test(model)) g.thinkingConfig = { thinkingBudget:0 };
  return g;
}
function thSaveCfg(patch){ var st = store().settings; st.ai = Object.assign({}, st.ai || {}, patch); if(typeof mirrorDraft === "function") mirrorDraft("ai"); saveData(); }

async function openThanksPage(){
  if(!supaOn()){ await uiAlert("서버 설정이 없는 빌드입니다", "감사 문자는 서버가 있어야 합니다.", "warn"); return; }
  if(!view.adminOk){ if(!await adminGate("감사 문자 열기")) return; view.adminOk = true; }
  view.form = {type:"thanks", page:true};
  if(!TH) TH = { date: shiftDate(todayStr(), -1), items:{}, queue:[], tab:"make", busy:{}, setup:false, sendAt:"" };
  TH.sendAt = TH.sendAt || (todayStr() + "T" + thCfg().hour);
  render(); await thLoadQueue(); render();
}
async function thLoadQueue(){
  try{ TH.queue = await sb("/rest/v1/thanks_sms?store=eq." + (view.storeKey || "hanok") + "&select=*&order=send_at.desc&limit=200"); }catch(e){ TH.queue = TH.queue || []; }
}
function thQueued(resId){ return (TH.queue || []).find(function(q){ return q.res_id === resId && q.status !== "취소"; }); }
/* 대상: 그 날짜에 '방문' 인 예약(전화번호 있는 것). 같은 번호가 여러 건이면 한 건만 */
function thTargets(){
  var seen = {};
  return store().reservations.filter(function(r){ return r.date === TH.date && r.status === "방문" && (r.phone || "").replace(/\D/g, "").length >= 9; })
    .sort(function(a, b){ return a.time.localeCompare(b.time); })
    .filter(function(r){ var d = r.phone.replace(/\D/g, ""); if(seen[d]) return false; seen[d] = 1; return true; });
}
function thItem(r){ return TH.items[r.id] || (TH.items[r.id] = { kw:"", text:"", made:"", pick:true }); }
/* 기본 양식 — AI 가 막혔을 때, 또는 사장님이 원할 때 */
function thTemplate(r, kw){
  var c = custStat(r), again = c.visit >= 3 ? " 늘 찾아 주셔서 더욱 감사합니다." : "";
  var extra = kw ? " " + kw.replace(/[,.]?\s*$/, "") + " 함께한 자리가 좋은 기억으로 남으셨기를 바랍니다." : "";
  return "[한옥반점] " + r.name + "님, 어제 저희 한옥반점을 찾아 주셔서 감사합니다." + again + extra + " 식사는 즐거우셨는지요. 다음에도 편안한 자리로 모시겠습니다. — 한옥반점 드림";
}
function thPrompt(r, kw){
  var c = custStat(r), cfg = thCfg(), seat = r.roomId ? (isRoom(seatById(r.roomId) || {}) ? "룸(방 이름은 쓰지 말 것)" : "홀 테이블") : "홀 테이블";
  var lines = [
    "당신은 경기 성남 분당의 한옥 중식당 '한옥반점' 사장입니다. 어제 다녀간 손님께 보내는 감사 문자를 한국어로 한 통만 쓰세요.",
    "규칙: 80~170자. 존댓말. 첫 줄은 '[한옥반점]' 로 시작하고 손님 이름을 '○○님' 으로 한 번 부를 것. 이모지는 최대 1개(없어도 됨). 광고·할인·링크·해시태그·과장 금지. 스팸처럼 보이면 안 됨. 받으면 기분 좋은, 담백하고 따뜻한 한 통. 마지막은 '한옥반점 드림'. 본문 외에 아무것도 출력하지 말 것.",
    "손님 정보: 이름 " + r.name + " · " + pplText(r) + (r.infants ? "(어린이 " + r.infants + "명)" : "") + " · " + dateLabel(r.date) + " " + hm(r.time) + " · " + seat + (r.menuType === "코스" ? " · 코스 식사" : "") +
      (c.visit >= 2 ? " · 방문 " + c.visit + "회째(단골)" : " · 첫 방문") + (r.request ? " · 요청사항: " + r.request : "") + (r.allergy ? " · 알러지: " + r.allergy : "") + (c.memo ? " · 손님 메모: " + c.memo : ""),
    kw ? "사장님이 준 키워드(꼭 자연스럽게 녹일 것): " + kw : "사장님 키워드 없음",
    cfg.common ? "공통 참고(계절·날씨 등): " + cfg.common : "",
    "오늘 날짜: " + todayStr()
  ];
  return lines.filter(Boolean).join("\n");
}
async function thGemini(prompt){
  var cfg = thCfg(); if(!cfg.key) throw new Error("NOKEY");
  var models = [cfg.model].concat(TH_MODELS.filter(function(m){ return m !== cfg.model; })), lastErr = null;
  for(var i = 0; i < models.length; i++){
    var model = models[i], ctl = new AbortController(), t = setTimeout(function(){ ctl.abort(); }, 25000), res;
    try{
      res = await fetch("https://generativelanguage.googleapis.com/v1beta/models/" + encodeURIComponent(model) + ":generateContent?key=" + encodeURIComponent(cfg.key), {
        method:"POST", headers:{ "Content-Type":"application/json" }, signal:ctl.signal,
        body: JSON.stringify({ contents:[{ role:"user", parts:[{ text:prompt }] }], generationConfig:thGenCfg(model) }) });
    }catch(e){ clearTimeout(t); throw e; }
    clearTimeout(t);
    if(res.status === 404 || res.status === 400){ var m0 = ""; try{ m0 = (await res.json()).error.message || ""; }catch(e){} lastErr = new Error("HTTP " + res.status + " · " + model + (m0 ? " · " + m0.slice(0, 80) : "")); continue; }   /* 그 모델이 없으면 다음 모델 */
    if(!res.ok){ var m = ""; try{ m = (await res.json()).error.message || ""; }catch(e){} throw new Error("HTTP " + res.status + (m ? " · " + m.slice(0, 120) : "")); }
    var j = await res.json(), text = "";
    try{ text = j.candidates[0].content.parts.filter(function(p){ return p.text && !p.thought; }).map(function(p){ return p.text; }).join("").trim(); }catch(e){}   /* 생각(thought) 조각은 뺌 */
    if(!text){ lastErr = new Error("빈 응답 · " + model); continue; }
    if(cfg.model !== model) thSaveCfg({model:model});   /* 되는 모델을 기억 */
    return text.replace(/^```[\s\S]*?\n|```$/g, "").trim();
  }
  throw lastErr || new Error("쓸 수 있는 모델이 없음");
}
async function thMake(resId, force){
  var r = store().reservations.find(function(x){ return x.id === resId; }); if(!r) return;
  var it = thItem(r); if(TH.busy[resId]) return;
  TH.busy[resId] = true; render();
  try{
    it.text = await thGemini(thPrompt(r, it.kw)); it.made = "ai"; it.err = "";
  }catch(e){
    var why = e.name === "AbortError" ? "응답이 25초 안에 안 옴" : e.message === "NOKEY" ? "Gemini 키가 빌드에 없음(supabase.*.json 의 geminiKey)" : e.message;
    it.err = why; if(!it.text || force){ it.text = thTemplate(r, it.kw); it.made = "template"; }
  }
  TH.busy[resId] = false; render();
}
async function thMakeAll(){
  var list = thTargets().filter(function(r){ return thItem(r).pick && !thQueued(r.id) && !thItem(r).text; });
  for(var i = 0; i < list.length; i++) await thMake(list[i].id);
}
function thUseTemplate(resId){ var r = store().reservations.find(function(x){ return x.id === resId; }); if(!r) return; var it = thItem(r); it.text = thTemplate(r, it.kw); it.made = "template"; it.err = ""; render(); }
function thSetText(resId, v){ var it = TH.items[resId]; if(it){ it.text = v; it.made = "manual"; } }
function thSetKw(resId, v){ var it = TH.items[resId]; if(it) it.kw = v; }
/* 예약 발송: 고른 건들을 thanks_sms 에 넣음(같은 예약은 한 번만 — unique) */
async function thSchedule(){
  var list = thTargets().filter(function(r){ var it = thItem(r); return it.pick && it.text && !thQueued(r.id); });
  if(!list.length){ await uiAlert("보낼 문자가 없습니다", "글이 만들어진 건을 체크하세요.", "warn"); return; }
  var at = new Date(TH.sendAt); if(isNaN(at)){ await uiAlert("보낼 시각을 정해 주세요", "", "warn"); return; }
  if(!await uiConfirm(list.length + "건 예약 발송", dateLabel(TH.sendAt.slice(0, 10)) + " " + hm(TH.sendAt.slice(11, 16)) + " 에 나갑니다. 그 전에는 '대기' 목록에서 취소할 수 있습니다.", {ok:"예약 발송", cancel:"취소", tone:"ok"})) return;
  var rows = list.map(function(r){ var it = thItem(r); return { id:"th_" + r.id, store:view.storeKey || "hanok", res_id:r.id, phone:r.phone.replace(/\D/g, ""), name:r.name, text:it.text, send_at:at.toISOString(), status:"대기", made_by:it.made || "manual", by:(SESSION && SESSION.who) || "" }; });
  try{
    await sb("/rest/v1/thanks_sms?on_conflict=store,res_id", { method:"POST", body:rows, prefer:"resolution=merge-duplicates,return=minimal" });
    logEvent("감사 문자 예약", rows.length + "건 · " + TH.sendAt);
    showToast(rows.length + "건 예약했습니다 — " + hm(TH.sendAt.slice(11, 16)) + " 발송"); await thLoadQueue(); render();
  }catch(e){ await uiAlert("예약 발송 실패", e.message || String(e), "warn"); }
}
async function thCancel(id){
  try{ await sb("/rest/v1/thanks_sms?id=eq." + encodeURIComponent(id) + "&status=eq.%EB%8C%80%EA%B8%B0", { method:"PATCH", body:{status:"취소"}, prefer:"return=minimal" }); await thLoadQueue(); render(); }
  catch(e){ await uiAlert("취소 실패", e.message || String(e), "warn"); }
}
async function thSendNow(id){
  var q = (TH.queue || []).find(function(x){ return x.id === id; }); if(!q) return;
  if(!await uiConfirm("지금 보낼까요?", q.name + " · " + phoneNorm(q.phone), {ok:"지금 보내기", cancel:"취소", tone:"ok"})) return;
  await thDeliver(q); await thLoadQueue(); render();
}
/* 실제 보내기(지금은 흉내). 먼저 '보냄' 으로 잡아 두 기기가 겹쳐 보내지 않게 */
async function thDeliver(q){
  try{
    var got = await sb("/rest/v1/thanks_sms?id=eq." + encodeURIComponent(q.id) + "&status=eq.%EB%8C%80%EA%B8%B0", { method:"PATCH", body:{status:"보냄"}, prefer:"return=representation" });
    if(!got || !got.length) return false;   /* 다른 기기가 먼저 보냄 */
    smsMockSend(phoneNorm(q.phone), q.name, q.text);
    return true;
  }catch(e){ console.error("감사 문자 보내기 실패", e.message); return false; }
}
/* 1분마다(06-modal 살림 틱에서) — 보낼 시각이 된 '대기' 건 */
async function thanksTick(){
  if(!supaOn() || !SESSION || !AUTHED || OFFLINE || view.display) return;
  try{
    var due = await sb("/rest/v1/thanks_sms?store=eq." + (view.storeKey || "hanok") + "&status=eq.%EB%8C%80%EA%B8%B0&send_at=lte." + encodeURIComponent(new Date().toISOString()) + "&select=*&limit=50");
    for(var i = 0; i < due.length; i++) await thDeliver(due[i]);
    if(due.length && TH){ await thLoadQueue(); if(view.form && view.form.type === "thanks") render(); }
  }catch(e){}
}

/* ---------- 화면 ---------- */
function sheetThanks(){
  if(!TH) return "";
  var cfg = thCfg();
  var tabs = '<div class="seg" style="margin-bottom:12px"><button class="' + (TH.tab === "make" ? "on" : "") + '" onclick="TH.tab=\'make\'; render()">만들기</button><button class="' + (TH.tab === "queue" ? "on" : "") + '" onclick="TH.tab=\'queue\'; render()">대기·보낸 문자' + ((TH.queue || []).filter(function(q){ return q.status === "대기"; }).length ? ' <i class="cnt">' + (TH.queue || []).filter(function(q){ return q.status === "대기"; }).length + '</i>' : '') + '</button></div>';
  var body = TH.tab === "queue" ? thQueueHtml() : thMakeHtml();
  return '<div class="th-top">' + tabs + '<div class="btn-row"><button class="btn sm ghost" onclick="TH.setup=true; render()">' + (cfg.key ? "AI 설정" : "AI 설정 · 키 없음!") + '</button></div></div>' + body + (TH.setup ? thSetupHtml() : "");
}
function thMakeHtml(){
  var list = thTargets(), anyBusy = Object.keys(TH.busy).some(function(k){ return TH.busy[k]; });
  var head = '<div class="th-ctl"><label class="f"><div class="lb">다녀간 날</div><input type="date" value="' + esc(TH.date) + '" onchange="TH.date=this.value; TH.items={}; render()"></label>' +
    '<label class="f"><div class="lb">공통 키워드 <span class="lbl-note">계절·날씨·행사 등, 모든 문자에 참고</span></div><input type="text" value="' + esc(thCfg().common) + '" placeholder="예: 갑자기 추워진 날씨, 추석 연휴" onchange="thSaveCfg({thanksCommon:this.value})"></label>' +
    '<label class="f"><div class="lb">보낼 시각</div><input type="datetime-local" value="' + esc(TH.sendAt) + '" onchange="TH.sendAt=this.value"></label></div>' +
    '<div class="btn-row" style="margin-bottom:12px"><button class="btn primary" onclick="thMakeAll()" ' + (anyBusy ? "disabled" : "") + '>' + ICON.spark + ' 체크한 것 전부 AI 로 만들기</button><button class="btn" onclick="thSchedule()">예약 발송</button></div>' +
    (anyBusy ? '<div class="ai-wave-wrap"><canvas class="ai-wave"></canvas><span>글을 짓고 있습니다…</span></div>' : '');
  if(!list.length) return head + '<div class="empty">' + dateLabel(TH.date) + ' 에 \'방문\' 으로 확인된 예약이 없습니다. 예약 상태를 방문으로 바꾼 손님만 대상입니다.</div>';
  var rows = list.map(function(r){
    var it = thItem(r), q = thQueued(r.id), c = custStat(r), busy = !!TH.busy[r.id];
    var info = hm(r.time) + ' · ' + pplText(r) + ' · ' + (r.roomId ? (isRoom(seatById(r.roomId) || {}) ? "룸" : "테이블") : "테이블") + (r.menuType === "코스" ? ' · 코스' : '') + (c.visit >= 2 ? ' · 방문 ' + c.visit + '회' : ' · 첫 방문') + (r.request ? ' · 요청: ' + esc(r.request) : '') + (c.memo ? ' · 메모: ' + esc(c.memo) : '');
    return '<div class="th-card ' + (q ? "queued" : "") + '"><div class="th-h"><label class="chk" style="margin:0"><input type="checkbox" ' + (it.pick && !q ? "checked" : "") + ' ' + (q ? "disabled" : "") + ' onchange="thItem(store().reservations.find(function(x){return x.id===\'' + r.id + '\';})).pick=this.checked"><span><b>' + esc(r.name) + '</b>' + tierTag(r) + ' <small class="muted">' + esc(phoneNorm(r.phone)) + '</small></span></label>' +
      (q ? '<span class="tag ' + (q.status === "보냄" ? "pine" : q.status === "취소" ? "" : "amber") + ' sm">' + q.status + (q.status === "대기" ? ' · ' + hm(new Date(q.send_at).toTimeString().slice(0, 5)) : '') + '</span>' : '') + '</div>' +
      '<div class="th-info">' + info + '</div>' +
      (q ? '<div class="th-text ro">' + esc(q.text) + '</div>' :
        '<div class="grid2 th-kw"><input type="text" value="' + esc(it.kw) + '" placeholder="사장님 키워드 — 예: 아버님 팔순, 팀 회식, 아이 생일" oninput="thSetKw(\'' + r.id + '\', this.value)">' +
        '<div class="btn-row"><button class="btn sm primary" onclick="thMake(\'' + r.id + '\')" ' + (busy ? "disabled" : "") + '>' + (busy ? "짓는 중…" : (it.text && it.made === "ai" ? "다시 만들기" : "AI 로 만들기")) + '</button><button class="btn sm ghost" onclick="thUseTemplate(\'' + r.id + '\')">기본 양식</button></div></div>' +
        (busy ? '<div class="ai-wave-wrap sm"><canvas class="ai-wave"></canvas></div>' : '') +
        '<textarea class="th-text" rows="4" placeholder="여기에 문자가 만들어집니다. 직접 써도 됩니다." oninput="thSetText(\'' + r.id + '\', this.value)">' + esc(it.text) + '</textarea>' +
        '<div class="th-meta">' + (it.text ? it.text.length + '자 · ' + (it.made === "ai" ? "AI" : it.made === "template" ? "기본 양식" : "직접 씀") : '') + (it.err ? ' <span class="rust">· AI 실패: ' + esc(it.err) + '</span>' : '') + '</div>') +
      '</div>';
  }).join("");
  return head + rows + '<p class="f-note">체크한 건만 보냅니다. 같은 손님이 하루 두 번 다녀갔으면 한 번만. 글은 80~170자, 광고·링크 없이 담백하게 — AI 가 만든 뒤에도 직접 고칠 수 있습니다. 문자 업체 연결 전까지는 흉내(문자 기록에만 남음).</p>';
}
function thQueueHtml(){
  var q = TH.queue || [];
  if(!q.length) return '<div class="empty">아직 예약하거나 보낸 감사 문자가 없습니다.</div>';
  return '<div class="card searchbox">' + q.map(function(x){ var at = new Date(x.send_at); return '<div class="rowitem"><span class="grow"><span class="t">' + esc(x.name) + ' <small class="muted">' + esc(phoneNorm(x.phone)) + '</small> <span class="tag ' + (x.status === "보냄" ? "pine" : x.status === "대기" ? "amber" : x.status === "실패" ? "rust" : "") + ' sm">' + x.status + '</span></span><span class="s" style="white-space:normal">' + esc(x.text) + '</span><span class="s">' + (isNaN(at) ? '' : (at.getMonth() + 1) + '/' + at.getDate() + ' ' + at.toTimeString().slice(0, 5)) + ' · ' + (x.made_by === "ai" ? "AI" : x.made_by === "template" ? "기본 양식" : "직접") + '</span></span>' +
    (x.status === "대기" ? '<span class="btn-row"><button class="btn sm ghost" onclick="thSendNow(\'' + x.id + '\')">지금</button><button class="btn sm ghost danger" onclick="thCancel(\'' + x.id + '\')">취소</button></span>' : '') + '</div>'; }).join("") + '</div>';
}
function thSetupHtml(){
  var cfg = thCfg();
  return '<div class="overlay" onclick="TH.setup=false; render()"><div class="sheet" onclick="event.stopPropagation()">' + sheetHead("AI 설정 (Gemini)") +
    '<div class="f"><div class="lb">API 키</div><div class="' + (cfg.key ? "" : "rust") + '">' + (cfg.key ? "빌드에 들어 있음 (" + esc(cfg.key.slice(0, 6)) + "…" + esc(cfg.key.slice(-4)) + ")" : "없음 — supabase.*.json 의 geminiKey 에 넣고 다시 빌드") + '</div></div>' +
    '<p class="f-note">키는 화면에서 바꾸지 않습니다(재아). 바꾸려면 supabase.dev.json / supabase.prod.json 의 geminiKey 를 고치고 빌드. 유료 키이니 구글 클라우드 콘솔에서 이 키에 "HTTP 리퍼러 제한: jaealee.com/*" 과 하루 사용 한도를 걸어 두세요.</p>' +
    '<div class="grid2"><label class="f"><div class="lb">모델 <span class="lbl-note">안 되면 자동으로 다음 모델</span></div><input id="th-model" type="text" value="' + esc(cfg.model) + '" placeholder="' + TH_DEF_MODEL + '"></label><label class="f"><div class="lb">보내는 시각 기본값</div><input id="th-hour" type="time" value="' + esc(cfg.hour) + '"></label></div>' +
    '<div class="sheet-actions"><button class="btn ghost" onclick="TH.setup=false; render()">취소</button><button class="btn primary" onclick="thSaveCfg({model:document.getElementById(\'th-model\').value.trim()||TH_DEF_MODEL, thanksHour:document.getElementById(\'th-hour\').value||\'11:00\'}); TH.setup=false; render()">저장</button></div></div></div>';
}
function thEsc(){ if(TH && view.form && view.form.type === "thanks" && TH.setup){ TH.setup = false; render(); return true; } return false; }

/* ---------- AI 물결 (시리 느낌) — 글 짓는 동안만. 여러 색 선이 파동치는 캔버스. 움직임 줄이기 설정이면 정적 띠 ---------- */
var AI_WAVE_RAF = null;
function aiWaveTick(){
  var cs = document.querySelectorAll("canvas.ai-wave"); AI_WAVE_RAF = null;
  if(!cs.length) return;
  var t = performance.now() / 1000, reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  cs.forEach(function(c){
    var w = c.clientWidth || 300, h = c.clientHeight || 56; if(c.width !== w * 2 || c.height !== h * 2){ c.width = w * 2; c.height = h * 2; }
    var g = c.getContext("2d"); g.setTransform(2, 0, 0, 2, 0, 0); g.clearRect(0, 0, w, h);
    var lines = [["#7C5CFF", 1.0, 0.0], ["#2BC6FF", 0.8, 1.3], ["#FF6FB1", 0.65, 2.4], ["#41E2A6", 0.55, 3.6], ["#FFB454", 0.45, 4.9]];
    lines.forEach(function(L, i){
      g.beginPath(); g.lineWidth = 2 - i * 0.25; g.strokeStyle = L[0]; g.shadowColor = L[0]; g.shadowBlur = 8; g.globalAlpha = 0.85;
      for(var x = 0; x <= w; x += 2){
        var p = x / w, env = Math.sin(p * Math.PI), amp = (h / 2 - 4) * L[1] * env * (reduce ? 0.5 : (0.7 + 0.3 * Math.sin(t * 1.7 + i)));
        var y = h / 2 + Math.sin(p * 9 + (reduce ? 0 : t * 2.6) + L[2]) * amp * 0.6 + Math.sin(p * 4.2 - (reduce ? 0 : t * 1.9) + L[2] * 2) * amp * 0.4;
        if(x === 0) g.moveTo(x, y); else g.lineTo(x, y);
      }
      g.stroke();
    });
    g.globalAlpha = 1; g.shadowBlur = 0;
  });
  if(!reduce) AI_WAVE_RAF = requestAnimationFrame(aiWaveTick);
}
function aiWaveStart(){ if(!AI_WAVE_RAF && document.querySelector("canvas.ai-wave")) AI_WAVE_RAF = requestAnimationFrame(aiWaveTick); }
