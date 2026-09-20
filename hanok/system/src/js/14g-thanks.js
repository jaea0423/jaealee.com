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
/* 설정(store().settings.ai) — 09-20(재아): AI 설정을 감사 문자 화면에서 빼고 설정 → 감사 문자 AI 로. 프롬프트는 문장 단위로 고치고(promptLines),
   기본 양식(template)·글자 한도(maxLen)·키워드 프리셋(kwPresets)도 거기서. 바꾸면 그 뒤에 만드는 글부터 적용 */
var TH_DEF_PROMPT = [
  "당신은 경기 성남 분당의 한옥 중식당 '한옥반점' 사장입니다. 어제 다녀간 손님께 보내는 감사 문자를 한국어로 한 통만 쓰세요.",
  "존댓말로, 첫 줄은 '[한옥반점]' 로 시작하고 손님 이름을 '○○님' 으로 한 번 부르세요.",
  "이모지는 최대 1개(없어도 됨). 광고·할인·링크·해시태그·과장은 쓰지 마세요. 스팸처럼 보이면 안 됩니다.",
  "설명 없이 문자 본문만 답하세요."
];
var TH_DEF_TEMPLATE = "[한옥반점] {이름}님, 어제 저희 한옥반점을 찾아 주셔서 감사합니다.{단골}{키워드} 식사는 즐거우셨는지요. 다음에도 편안한 자리로 모시겠습니다. — 한옥반점 드림";
var TH_DEF_KW = ["가족 모임", "생신", "회식", "상견례", "아이 생일", "첫 방문", "단골"];
function thCfg(){
  var a = store().settings.ai || {};
  return { key: (typeof SUPA_CFG !== "undefined" && SUPA_CFG && SUPA_CFG.geminiKey) || "", model: a.model || TH_DEF_MODEL, hour: a.thanksHour || "11:00", common: a.thanksCommon || "",
    promptLines: Array.isArray(a.promptLines) && a.promptLines.length ? a.promptLines : TH_DEF_PROMPT.slice(),
    template: a.template || TH_DEF_TEMPLATE, maxLen: Number(a.maxLen) || 200,
    kwPresets: Array.isArray(a.kwPresets) ? a.kwPresets : TH_DEF_KW.slice() };
}
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
  if(!TH) TH = { date: shiftDate(todayStr(), -1), items:{}, queue:[], tab:"make", busy:{}, sendAt:"", adv:false, run:null, stop:false, qf:"all" };
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
function thItem(r){ return TH.items[r.id] || (TH.items[r.id] = { kws:[], text:"", made:"", pick:true, manual:false }); }
function thKw(it){ return (it.kws || []).join(", "); }
/* 기본 양식 — AI 가 막혔을 때, 또는 사장님이 원할 때. 설정에서 고칠 수 있음: {이름} {단골} {키워드} {매장} 자리에 값이 들어감 */
function thTemplate(r, kw){
  var c = custStat(r), again = c.visit >= 3 ? " 늘 찾아 주셔서 더욱 감사합니다." : "";
  var extra = kw ? " " + kw.replace(/[,.]?\s*$/, "") + " 함께한 자리가 좋은 기억으로 남으셨기를 바랍니다." : "";
  return thCfg().template.replace(/\{이름\}/g, r.name).replace(/\{단골\}/g, again).replace(/\{키워드\}/g, extra).replace(/\{매장\}/g, store().name || "한옥반점");
}
function thPrompt(r, kw){
  var c = custStat(r), cfg = thCfg(), seat = r.roomId ? (isRoom(seatById(r.roomId) || {}) ? "룸(방 이름은 쓰지 말 것)" : "홀 테이블") : "홀 테이블";
  var lines = cfg.promptLines.slice().concat([
    "길이: 80자 이상 " + cfg.maxLen + "자 이하.",
    "손님 정보: 이름 " + r.name + " · " + pplText(r) + (r.infants ? "(어린이 " + r.infants + "명)" : "") + " · " + dateLabel(r.date) + " " + hm(r.time) + " · " + seat + (r.menuType === "코스" ? " · 코스 식사" : "") +
      (c.visit >= 2 ? " · 방문 " + c.visit + "회째(단골)" : " · 첫 방문") + (r.request ? " · 요청사항: " + r.request : "") + (r.allergy ? " · 알러지: " + r.allergy : "") + (c.memo ? " · 손님 메모: " + c.memo : ""),
    kw ? "사장님이 준 키워드(꼭 자연스럽게 녹일 것): " + kw : "사장님 키워드 없음",
    cfg.common ? "공통 참고(계절·날씨 등): " + cfg.common : "",
    "오늘 날짜: " + todayStr()
  ]);
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
    var t = await thGemini(thPrompt(r, thKw(it)));
    if(TH.stop) throw new Error("STOP");
    it.text = t.slice(0, thCfg().maxLen); it.made = "ai"; it.err = ""; it.manual = false;
  }catch(e){
    if(e.message === "STOP"){ TH.busy[resId] = false; return; }
    var why = e.name === "AbortError" ? "응답이 25초 안에 안 옴" : e.message === "NOKEY" ? "Gemini 키가 빌드에 없음(supabase.*.json 의 geminiKey)" : e.message;
    it.err = why; if(!it.text || force){ it.text = thTemplate(r, thKw(it)); it.made = "template"; }
  }
  TH.busy[resId] = false; render();
}
/* 'AI 로 완성하기' — 직접 쓴 것(manual)과 이미 예약된 것만 빼고 전부(09-20 재아: 체크와 무관). 진행 중엔 위에 떠 있는 표시 + 중단 */
async function thMakeAll(){
  var list = thTargets().filter(function(r){ var it = thItem(r); return !thQueued(r.id) && !it.manual && !(it.text && it.made === "ai"); });
  if(!list.length){ showToast("AI 로 만들 것이 없습니다 — 직접 쓴 것과 이미 만든 것은 그대로 둡니다"); return; }
  TH.stop = false; TH.run = { total:list.length, done:0 }; render();
  for(var i = 0; i < list.length && !TH.stop; i++){ await thMake(list[i].id); TH.run.done = i + 1; }
  TH.run = null; TH.stop = false; render();
}
function thStop(){ TH.stop = true; TH.run = null; Object.keys(TH.busy).forEach(function(k){ TH.busy[k] = false; }); render(); showToast("중단했습니다"); }
function thRunning(){ return !!(TH && (TH.run || Object.keys(TH.busy).some(function(k){ return TH.busy[k]; }))); }
function thUseTemplate(resId){ var r = store().reservations.find(function(x){ return x.id === resId; }); if(!r) return; var it = thItem(r); it.text = thTemplate(r, thKw(it)); it.made = "template"; it.err = ""; it.manual = false; render(); }
function thManual(resId){ var it = TH.items[resId]; if(it){ it.manual = true; if(!it.made) it.made = "manual"; render(); setTimeout(function(){ var el = document.getElementById("th-ta-" + resId); if(el) el.focus(); }, 30); } }
function thSetText(resId, v, el){ var it = TH.items[resId]; if(!it) return; var max = thCfg().maxLen; if(v.length > max){ v = v.slice(0, max); if(el) el.value = v; } it.text = v; it.made = "manual"; it.manual = true; if(el){ el.style.height = "auto"; el.style.height = el.scrollHeight + "px"; var m = el.parentNode.querySelector(".th-meta"); if(m) m.innerHTML = v.length + "자 / " + max + "자 · 직접 씀"; } }
/* 키워드 알약 — Enter 나 '등록' 으로 쌓이고 × 로 뺌. 프리셋(설정)은 누르면 바로 들어감 */
function thAddKw(resId, v){ var it = TH.items[resId]; if(!it) return; v = String(v || "").trim(); if(!v) return; if(it.kws.indexOf(v) < 0) it.kws.push(v); render(); setTimeout(function(){ var el = document.getElementById("th-kw-" + resId); if(el) el.focus(); }, 20); }
function thDelKw(resId, i){ var it = TH.items[resId]; if(!it) return; it.kws.splice(i, 1); render(); }
function thKwKey(ev, resId){ if(ev.key === "Enter" && !ev.isComposing){ ev.preventDefault(); thAddKw(resId, ev.target.value); ev.target.value = ""; } }
function thPickAll(on){ thTargets().forEach(function(r){ if(!thQueued(r.id)) thItem(r).pick = on; }); render(); }
/* 예약 발송: 고른 건들을 thanks_sms 에 넣음(같은 예약은 한 번만 — unique) */
async function thSchedule(){
  var list = thTargets().filter(function(r){ var it = thItem(r); return it.pick && it.text && !thQueued(r.id); });
  if(!list.length){ await uiAlert("보낼 문자가 없습니다", "글이 만들어진 건을 체크하세요.", "warn"); return; }
  var at = new Date(TH.sendAt); if(isNaN(at)){ await uiAlert("보낼 시각을 정해 주세요", "", "warn"); return; }
  if(!await uiConfirm(list.length + "건 예약 발송", dateLabel(TH.sendAt.slice(0, 10)) + " " + hm(TH.sendAt.slice(11, 16)) + " 에 나갑니다. 그 전에는 '대기' 목록에서 취소할 수 있습니다.", {ok:"예약 발송", cancel:"취소", tone:"ok"})) return;
  var rows = list.map(function(r){ var it = thItem(r); return { id:"th_" + r.id, store:view.storeKey || "hanok", res_id:r.id, phone:r.phone.replace(/\D/g, ""), name:r.name, text:it.text, send_at:at.toISOString(), status:"대기", made_by:it.made || "manual", by:(SESSION && SESSION.who) || "", kw:thKw(it) }; });
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
    try{ smsMockSend(phoneNorm(q.phone), q.name, q.text); }
    catch(e2){ await sb("/rest/v1/thanks_sms?id=eq." + encodeURIComponent(q.id), { method:"PATCH", body:{status:"오류"}, prefer:"return=minimal" }); return false; }   /* 09-20: 못 보낸 건은 '오류' 로 남겨 목록에서 보이게 */
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
function thStatusLabel(st){ return st === "보냄" ? "전송 완료" : st === "대기" ? "대기" : st === "오류" ? "오류" : st; }
function sheetThanks(){
  if(!TH) return "";
  var cfg = thCfg(), wait = (TH.queue || []).filter(function(q){ return q.status === "대기"; }).length;
  var tabs = '<div class="seg" style="margin-bottom:12px"><button class="' + (TH.tab === "make" ? "on" : "") + '" onclick="TH.tab=\'make\'; render()">만들기</button><button class="' + (TH.tab === "queue" ? "on" : "") + '" onclick="TH.tab=\'queue\'; render()">보낸 문자' + (wait ? '<i class="cnt">' + wait + '</i>' : '') + '</button></div>';
  var body = TH.tab === "queue" ? thQueueHtml() : thMakeHtml();
  /* AI 가 도는 동안: 탭 위에 떠 있는 작은 표시 + 중단. 그동안 화면을 나가지 못하게 닫기 단추도 막음(thGuard) */
  var run = thRunning() ? '<div class="th-run"><canvas class="ai-wave"></canvas><span>AI 가 글을 짓고 있습니다' + (TH.run ? ' · ' + TH.run.done + '/' + TH.run.total : '') + '</span><button class="btn sm" onclick="thStop()">중단</button></div>' : '';
  return run + '<div class="th-top">' + tabs + (cfg.key ? '' : '<span class="tag rust sm">Gemini 키 없음 — 기본 양식만</span>') + '</div>' + body;
}
function thMakeHtml(){
  var list = thTargets(), cfg = thCfg(), running = thRunning();
  var head = '<div class="th-ctl"><label class="f"><div class="lb">다녀간 날</div><input type="date" value="' + esc(TH.date) + '" onchange="TH.date=this.value; TH.items={}; render()"></label>' +
    '<label class="f"><div class="lb">공통 키워드 <span class="lbl-note">계절·날씨·행사 등, 모든 문자에 참고</span></div><input type="text" value="' + esc(cfg.common) + '" placeholder="예: 갑자기 추워진 날씨, 추석 연휴" onchange="thSaveCfg({thanksCommon:this.value})"></label>' +
    '<div class="f"><div class="lb">&nbsp;</div><button class="btn sm ghost" onclick="TH.adv=!TH.adv; render()">' + (TH.adv ? "고급 닫기" : "고급") + '</button></div></div>' +
    (TH.adv ? '<div class="th-ctl adv"><label class="f"><div class="lb">보낼 시각 <span class="lbl-note">기본은 오늘 ' + esc(cfg.hour) + ' (설정에서)</span></div><input type="datetime-local" value="' + esc(TH.sendAt) + '" onchange="TH.sendAt=this.value"></label></div>' : '') +
    '<div class="th-actions"><div class="btn-row"><button class="btn primary" onclick="thMakeAll()" ' + (running ? "disabled" : "") + '>' + ICON.spark + ' AI 로 완성하기</button>' +
      '<button class="btn sm ghost" onclick="thPickAll(true)">전체 선택</button><button class="btn sm ghost" onclick="thPickAll(false)">전체 해제</button></div>' +
      '<button class="btn" onclick="thSchedule()" ' + (running ? "disabled" : "") + '>예약발송하기</button></div>';
  if(!list.length) return head + '<div class="empty">' + dateLabel(TH.date) + ' 에 \'방문\' 으로 확인된 예약이 없습니다. 예약 상태를 방문으로 바꾼 손님만 대상입니다.</div>';
  var rows = list.map(function(r){
    var it = thItem(r), q = thQueued(r.id), c = custStat(r), busy = !!TH.busy[r.id];
    var info = hm(r.time) + ' · ' + pplText(r) + ' · ' + (r.roomId ? (isRoom(seatById(r.roomId) || {}) ? "룸" : "테이블") : "테이블") + (r.menuType === "코스" ? ' · 코스' : '') + (c.visit >= 2 ? ' · 방문 ' + c.visit + '회' : ' · 첫 방문') + (r.request ? ' · 요청: ' + esc(r.request) : '') + (c.memo ? ' · 메모: ' + esc(c.memo) : '');
    var showText = !!(it.text || it.manual);
    var presets = cfg.kwPresets.filter(function(k){ return it.kws.indexOf(k) < 0; }).map(function(k, pi){ return '<button class="chip preset" onclick="thAddKw(\'' + r.id + '\', thCfg().kwPresets[' + cfg.kwPresets.indexOf(k) + '])">+ ' + esc(k) + '</button>'; }).join("");
    var chips = it.kws.map(function(k, i){ return '<span class="chip">' + esc(k) + '<button class="x" onclick="thDelKw(\'' + r.id + '\', ' + i + ')" aria-label="빼기">×</button></span>'; }).join("");
    return '<div class="th-card ' + (q ? "queued" : "") + '"><div class="th-h"><label class="chk" style="margin:0"><input type="checkbox" ' + (it.pick && !q ? "checked" : "") + ' ' + (q ? "disabled" : "") + ' onchange="thItem(store().reservations.find(function(x){return x.id===\'' + r.id + '\';})).pick=this.checked"> <b>' + esc(r.name) + '</b>' + tierTag(r) + ' <small class="muted">' + esc(phoneNorm(r.phone)) + '</small></label>' +
      (q ? '<span class="tag ' + (q.status === "보냄" ? "pine" : q.status === "오류" ? "rust" : q.status === "취소" ? "" : "amber") + ' sm">' + thStatusLabel(q.status) + (q.status === "대기" ? ' · ' + hm(new Date(q.send_at).toTimeString().slice(0, 5)) : '') + '</span>' : '') + '</div>' +
      '<div class="th-info">' + info + '</div>' +
      (q ? '<div class="th-text ro">' + esc(q.text) + '</div>' :
        '<div class="th-kwrow"><div class="chips">' + chips + '<input id="th-kw-' + r.id + '" type="text" class="chip-in" placeholder="키워드 — 예: 아버님 팔순" onkeydown="thKwKey(event, \'' + r.id + '\')"><button class="btn sm ghost" onclick="var el=document.getElementById(\'th-kw-' + r.id + '\'); thAddKw(\'' + r.id + '\', el.value); el.value=\'\'">등록</button></div>' +
          (presets ? '<div class="chips presets">' + presets + '</div>' : '') + '</div>' +
        (busy ? '<div class="ai-wave-wrap sm"><canvas class="ai-wave"></canvas></div>' : '') +
        (showText ? '<textarea id="th-ta-' + r.id + '" class="th-text grow" rows="2" placeholder="문자 내용" oninput="thSetText(\'' + r.id + '\', this.value, this)" maxlength="' + cfg.maxLen + '">' + esc(it.text) + '</textarea>' +
          '<div class="th-meta">' + (it.text ? it.text.length + '자 / ' + cfg.maxLen + '자 · ' + (it.made === "ai" ? "AI" : it.made === "template" ? "기본 양식" : "직접 씀") : '0자 / ' + cfg.maxLen + '자') + (it.err ? ' <span class="rust">· AI 실패: ' + esc(it.err) + '</span>' : '') + '</div>'
          : '<div class="th-meta">' + (it.err ? '<span class="rust">AI 실패: ' + esc(it.err) + '</span> · ' : '') + '아직 글이 없습니다 — \'AI 로 완성하기\' 로 한 번에, 또는 아래에서 직접</div>') +
        '<div class="btn-row th-cardbtns">' + (showText ? '' : '<button class="btn sm ghost" onclick="thManual(\'' + r.id + '\')">직접 입력하기</button>') + '<button class="btn sm ghost" onclick="thUseTemplate(\'' + r.id + '\')">기본 양식</button></div>') +
      '</div>';
  }).join("");
  return head + rows + '<p class="f-note">체크한 건만 보냅니다. 같은 손님이 하루 두 번 다녀갔으면 한 번만. 글은 ' + cfg.maxLen + '자까지 — 넘으면 문자가 나뉘어 요금이 늘거나 실패합니다. 프롬프트·기본 양식·한도·키워드 프리셋은 설정 → 감사 문자 AI 에서.</p>';
}
function thQueueHtml(){
  var q = TH.queue || [];
  if(!q.length) return '<div class="empty">아직 예약하거나 보낸 감사 문자가 없습니다.</div>';
  var f = TH.qf || "all", list = f === "all" ? q : q.filter(function(x){ return x.status === f; });
  var seg = function(k, l){ var n = k === "all" ? q.length : q.filter(function(x){ return x.status === k; }).length; return '<button class="' + (f === k ? "on" : "") + '" onclick="TH.qf=\'' + k + '\'; render()">' + l + (n ? ' ' + n : '') + '</button>'; };
  return '<div class="seg" style="margin-bottom:12px">' + seg("all", "전체") + seg("대기", "대기 문자") + seg("보냄", "전송 완료") + seg("오류", "오류") + seg("취소", "취소") + '</div>' +
    '<div class="card searchbox">' + (list.length ? list.map(function(x){ var at = new Date(x.send_at); return '<div class="rowitem"><span class="grow"><span class="t">' + esc(x.name) + ' <small class="muted">' + esc(phoneNorm(x.phone)) + '</small> <span class="tag ' + (x.status === "보냄" ? "pine" : x.status === "오류" ? "rust" : x.status === "취소" ? "" : "amber") + ' sm">' + thStatusLabel(x.status) + '</span></span><span class="s">' + esc(dateLabel(x.send_at.slice(0, 10))) + ' ' + pad(at.getHours()) + ':' + pad(at.getMinutes()) + ' · ' + esc(x.text) + '</span></span>' +
    (x.status === "대기" ? '<span class="btn-row"><button class="btn sm ghost" onclick="thSendNow(\'' + x.id + '\')">지금</button><button class="btn sm ghost danger" onclick="thCancel(\'' + x.id + '\')">취소</button></span>' : '') + '</div>'; }).join("") : '<p class="muted" style="padding:16px">없습니다.</p>') + '</div>';
}
/* 설정 → 감사 문자 AI (14-settings 가 부름). draft 의 settings.ai 를 고칩니다 — '적용하기' 로 저장 */
function thSettingsBody(st){
  var a = st.ai = st.ai || {}, cfg = { promptLines: Array.isArray(a.promptLines) && a.promptLines.length ? a.promptLines : TH_DEF_PROMPT.slice(), template: a.template || TH_DEF_TEMPLATE, maxLen: Number(a.maxLen) || 200, kwPresets: Array.isArray(a.kwPresets) ? a.kwPresets : TH_DEF_KW.slice(), hour: a.thanksHour || "11:00", model: a.model || TH_DEF_MODEL };
  var key = (typeof SUPA_CFG !== "undefined" && SUPA_CFG && SUPA_CFG.geminiKey) || "";
  var lines = cfg.promptLines.map(function(l, i){ return '<div class="th-pl"><span class="n">' + (i + 1) + '</span><input type="text" value="' + esc(l) + '" onchange="thSetLine(' + i + ', this.value)"><button class="btn sm ghost danger" onclick="thDelLine(' + i + ')">삭제</button></div>'; }).join("");
  return '<div class="f"><div class="lb">API 키</div><div class="' + (key ? "" : "rust") + '">' + (key ? "빌드에 들어 있음 (" + esc(key.slice(0, 6)) + "…" + esc(key.slice(-4)) + ")" : "없음 — supabase.*.json 의 geminiKey 에 넣고 다시 빌드") + '</div></div>' +
    '<div class="subhead">프롬프트 <span>문장 하나가 한 줄. 고치거나 지우거나 더하면 그 뒤에 만드는 글부터 적용</span></div>' + lines +
    '<div class="btn-row" style="margin:4px 0 16px"><button class="btn sm" onclick="thAddLine()">＋ 문장 추가</button><button class="btn sm ghost" onclick="thResetLines()">기본으로</button></div>' +
    '<p class="f-note">예: "추석 연휴에 다녀간 손님이니 명절 인사를 한 줄 넣으세요" 같은 문장을 그때그때 더하고, 끝나면 지우면 됩니다. 손님 정보(이름·인원·자리·방문 횟수)와 키워드, 글자 한도는 자동으로 뒤에 붙습니다.</p>' +
    '<label class="f big"><div class="lb">기본 양식 <span class="lbl-note">AI 가 막혔을 때 · \'기본 양식\' 단추. {이름} {단골} {키워드} {매장} 자리에 값이 들어감</span></div><textarea class="in-sm" rows="3" onchange="draft().ai.template=this.value; render()">' + esc(cfg.template) + '</textarea></label>' +
    '<div class="grid2"><label class="f"><div class="lb">글자 한도</div><input type="number" min="80" max="400" value="' + cfg.maxLen + '" onchange="draft().ai.maxLen=Number(this.value)||200; render()"></label>' +
    '<label class="f"><div class="lb">보내는 시각 기본</div><input type="time" value="' + esc(cfg.hour) + '" onchange="draft().ai.thanksHour=this.value; render()"></label></div>' +
    '<label class="f big"><div class="lb">키워드 프리셋 <span class="lbl-note">쉼표로 — 감사 문자 카드에 단추로 뜸</span></div><input type="text" value="' + esc(cfg.kwPresets.join(", ")) + '" onchange="draft().ai.kwPresets=this.value.split(\',\').map(function(x){return x.trim();}).filter(Boolean); render()"></label>' +
    '<label class="f"><div class="lb">모델 <span class="lbl-note">안 되면 자동으로 다음 모델</span></div><input type="text" value="' + esc(cfg.model) + '" placeholder="' + TH_DEF_MODEL + '" onchange="draft().ai.model=this.value.trim()||TH_DEF_MODEL; render()"></label>';
}
function thLines(){ var a = draft().ai = draft().ai || {}; if(!Array.isArray(a.promptLines) || !a.promptLines.length) a.promptLines = TH_DEF_PROMPT.slice(); return a.promptLines; }
function thSetLine(i, v){ thLines()[i] = v; render(); }
function thDelLine(i){ thLines().splice(i, 1); render(); }
function thAddLine(){ thLines().push(""); render(); }
function thResetLines(){ draft().ai.promptLines = TH_DEF_PROMPT.slice(); render(); }
function thEsc(){ return false; }
/* AI 가 도는 동안은 감사 문자 화면을 못 나감(15-sheets closeSheet 가 부름) */
function thGuard(){ if(view.form && view.form.type === "thanks" && thRunning()){ showToast("AI 가 글을 짓는 중입니다 — 끝나거나 중단한 뒤에 나가세요"); return true; } return false; }

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
