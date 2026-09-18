/* ---------- 워크시프트 (staff · attendance · hr_settings, 15·17차) ----------
   사장님이 직접 찍는 주간 근무표 + 월 급여 계산. 화면형(view.form={type:"staff", page:true}) — 관리자 비밀번호 뒤.
   · 표는 한 주(월~일). 줄 = 직원(별칭 우선), 칸 = 날. 칸을 누르면 ○ 정규 / △ 다른 시간 / × 결근 / – 휴무 + 배율(휴일 등) + 메모
   · 정규 = 그 직원의 정규 근무(요일·시작·종료·휴게). 시간은 거기서 자동, 다른 시간(△)은 적은 시각으로
   · 급여(월): 기본급 + 연장(하루 8h·주 40h 넘김 ×0.5) + 야간(22~06시 ×0.5) + 주휴수당(주 15h 이상 개근) + 배율 가산
     − 공제(4대보험 4종 또는 3.3% 사업소득, 또는 없음) = 실지급. 연장·야간 가산은 '5인 이상 사업장' 일 때만(설정).
     월급제는 월급 그대로 + 연장·야간(통상시급 = 월급/209) − 공제. 퇴직금은 1년 이상 근속자에게 추정치(최근 3개월 평균).
   · 요율·5인 이상·야간 시간대는 hr_settings(설정 창). 세금·보험은 '참고용' — 최종 신고는 세무사/노무사와.
   서버 표: staff / attendance / hr_settings. 직원은 지우지 않고 '퇴사'. 근태 칸은 지울 수 있음. */
var HR = null;
var HR_STATUS = { "정규":"○", "변형":"△", "결근":"×", "휴무":"–" };
var HR_DAYS = ["일","월","화","수","목","금","토"];
var HR_DEF = { over5:true, rates:{ pension:4.5, health:3.545, care:12.95, employ:0.9 }, night:["22:00","06:00"], taxRate:3.3, weeklyPay:true, ownerNote:"" };

async function openStaffPage(){
  if(!supaOn()){ await uiAlert("서버 설정이 없는 빌드입니다", "워크시프트는 서버가 있어야 합니다.", "warn"); return; }
  if(!view.adminOk){ if(!await adminGate("워크시프트 열기")) return; view.adminOk = true; }
  view.form = {type:"staff", page:true};
  if(!HR) HR = { week: hrWeekStart(todayStr()), month: monthStr(), staff:[], att:{}, loaded:{}, cfg:null, loading:true, pop:null, edit:null, view:"week", slip:null, setup:false };
  render(); await hrLoad(); render();
}
/* 주의 시작(월요일) */
function hrWeekStart(d){ var x = new Date(d + "T00:00:00"), dow = (x.getDay() + 6) % 7; return shiftDate(d, -dow); }
function hrWeekDays(w){ var out = []; for(var i = 0; i < 7; i++) out.push(shiftDate(w, i)); return out; }
function hrMonthEnd(m){ var d = new Date(m + "-01T00:00:00"); d.setMonth(d.getMonth() + 1); d.setDate(0); return m + "-" + pad(d.getDate()); }
function hrMonthDays(m){ var n = Number(hrMonthEnd(m).slice(8)), out = []; for(var i = 1; i <= n; i++) out.push(m + "-" + pad(i)); return out; }
function hrCfg(){ var c = (HR && HR.cfg) || {}; return { over5: c.over5 !== false, rates: Object.assign({}, HR_DEF.rates, c.rates || {}), night: c.night || HR_DEF.night, taxRate: c.taxRate != null ? c.taxRate : HR_DEF.taxRate, weeklyPay: c.weeklyPay !== false }; }
/* 직원 + 설정 + 필요한 기간의 근태(월 단위로 받아 두고 loaded 에 표시) */
async function hrLoad(){
  var key = view.storeKey || "hanok";
  try{
    HR.staff = await sb("/rest/v1/staff?store=eq." + key + "&select=*&order=sort,name");
    var cs = await sb("/rest/v1/hr_settings?store=eq." + key + "&select=data"); HR.cfg = cs[0] ? cs[0].data : {};
    HR.err = null;
  }catch(e){ HR.err = e.message || String(e); }
  await hrLoadRange();
  HR.loading = false;
}
async function hrLoadMonth(m){
  if(HR.loaded[m]) return;
  var key = view.storeKey || "hanok", from = m + "-01", to = shiftDate(hrMonthEnd(m), 1);
  var rows = await sb("/rest/v1/attendance?store=eq." + key + "&date=gte." + from + "&date=lt." + to + "&select=*");
  rows.forEach(function(a){ HR.att[a.staff_id + "|" + a.date] = a; });
  HR.loaded[m] = true;
}
async function hrLoadRange(){
  try{
    var ms = {}; hrWeekDays(HR.week).forEach(function(d){ ms[d.slice(0, 7)] = 1; }); ms[HR.month] = 1;
    /* 주휴·주 40h 계산은 그 달의 앞뒤 주까지 걸치므로 앞뒤 달도 */
    var mx = new Date(HR.month + "-01T00:00:00"); mx.setMonth(mx.getMonth() - 1); ms[monthStr(mx)] = 1; mx.setMonth(mx.getMonth() + 2); ms[monthStr(mx)] = 1;
    for(var m in ms) await hrLoadMonth(m);
  }catch(e){ HR.err = e.message || String(e); }
}
async function hrMoveWeek(d){ HR.week = shiftDate(HR.week, 7 * d); HR.loading = true; render(); await hrLoadRange(); HR.loading = false; render(); }
async function hrMoveMonth(d){ var x = new Date(HR.month + "-01T00:00:00"); x.setMonth(x.getMonth() + d); HR.month = monthStr(x); HR.loading = true; render(); await hrLoadRange(); HR.loading = false; render(); }
function hrLabel(s){ return s.nick || s.name; }
/* 정규 근무 시간표 읽기 — 없으면 요일 전부 쉼 */
function hrSched(s){ var x = s.sched || {}; return { days: x.days && x.days.length === 7 ? x.days : [false,false,false,false,false,false,false], start: x.start || "10:00", end: x.end || "22:00", brk: Number(x.break || 0) }; }
function hrSchedText(s){ var c = hrSched(s), ds = HR_DAYS.filter(function(_, i){ return c.days[i]; }); return ds.length ? ds.join("·") + " " + hm(c.start) + "~" + hm(c.end) + (c.brk ? " (휴게 " + c.brk + "분)" : "") : "정규 근무 없음"; }
function hrOnDuty(s, date){ var c = hrSched(s), dow = new Date(date + "T00:00:00").getDay(); if(!c.days[dow]) return false; if(s.start_date && date < s.start_date) return false; if(s.end_date && date > s.end_date) return false; return true; }
/* 한 칸의 근무 구간(분) — [start,end,break]. 정규는 시간표, 변형은 적힌 시각. 자정 넘김은 end += 24h */
function hrSpan(s, a){
  if(!a || (a.status !== "정규" && a.status !== "변형")) return null;
  var c = hrSched(s), st = a.status === "정규" ? c.start : a.start, en = a.status === "정규" ? c.end : a.end, brk = a.status === "정규" ? c.brk : Number(a.break_min || 0);
  if(!st || !en) return null;
  var s0 = toMin(st), e0 = toMin(en); if(e0 <= s0) e0 += 24 * 60;
  return { s0:s0, e0:e0, brk:brk, hours:Math.max(0, (e0 - s0 - brk) / 60) };
}
function hrHours(s, a){ var sp = hrSpan(s, a); return sp ? sp.hours : 0; }
/* 야간(22~06) 시간 — 휴게는 야간 밖에서 뺀 것으로 봄(단순화) */
function hrNight(sp){
  if(!sp) return 0; var n = hrCfg().night, ns = toMin(n[0]), ne = toMin(n[1]) + 24 * 60, h = 0;
  [[ns, ne], [ns - 24 * 60, ne - 24 * 60], [ns + 24 * 60, ne + 24 * 60]].forEach(function(w){ var a = Math.max(sp.s0, w[0]), b = Math.min(sp.e0, w[1]); if(b > a) h += (b - a) / 60; });
  return Math.min(h, sp.hours);
}
function hrRound(h){ return Math.round(h * 10) / 10; }
function hrWon(n){ return Math.round(Number(n || 0)).toLocaleString("ko-KR") + "원"; }
/* 한 주(월~일) 요약 — 시간·연장·야간·주휴 */
function hrWeekCalc(s, w){
  var cfg = hrCfg(), t = { hours:0, ot:0, night:0, days:0, absent:0, dutyDays:0, sched:0, weeklyPay:0 };
  var c = hrSched(s), dayH = Math.max(0, (toMin(c.end) - toMin(c.start) - c.brk) / 60); if(toMin(c.end) <= toMin(c.start)) dayH += 24;
  hrWeekDays(w).forEach(function(d){
    var duty = hrOnDuty(s, d); if(duty){ t.dutyDays++; t.sched += dayH; }
    var a = HR.att[s.id + "|" + d]; if(!a) return;
    if(a.status === "결근"){ t.absent++; return; }
    var sp = hrSpan(s, a); if(!sp) return;
    t.days++; t.hours += sp.hours; t.night += hrNight(sp);
    if(sp.hours > 8) t.ot += sp.hours - 8;   /* 하루 8시간 넘김 */
  });
  var weekOt = Math.max(0, t.hours - 40 - t.ot); t.ot += weekOt;   /* 주 40시간 넘김(하루 연장과 겹치지 않게) */
  if(!cfg.over5){ t.ot = 0; t.night = 0; }   /* 5인 미만은 가산 의무 없음 */
  /* 주휴: 주 소정근로 15h 이상 + 그 주 정규 근무일 개근(결근 없음, 정규일 전부 찍힘). 시급제만. 주휴시간 = min(주 시간, 40)/40 × 8 */
  if(s.pay_type !== "monthly" && s.weekly_pay !== false && cfg.weeklyPay && t.sched >= 15 && t.dutyDays > 0 && !t.absent && t.days >= t.dutyDays){
    t.weeklyPay = Math.min(t.hours, 40) / 40 * 8;
  }
  return t;
}
/* 한 달 급여 — 그 달에 속한 날만 셈. 주 단위 값(연장·주휴)은 '주의 마지막 날(일요일)이 속한 달' 에 넣습니다 */
function hrCalc(s, month){
  var cfg = hrCfg(), days = hrMonthDays(month), t = { reg:0, alt:0, abs:0, off:0, days:0, hours:0, night:0, ot:0, weekly:0, bonusH:0, base:0, otPay:0, nightPay:0, weeklyPay:0, bonusPay:0, gross:0, ded:{}, dedTotal:0, net:0, employer:0, wage:0 };
  days.forEach(function(d){
    var a = HR.att[s.id + "|" + d]; if(!a) return;
    if(a.status === "정규") t.reg++; else if(a.status === "변형") t.alt++; else if(a.status === "결근") t.abs++; else if(a.status === "휴무") t.off++;
    var sp = hrSpan(s, a); if(!sp) return;
    t.hours += sp.hours; t.night += hrNight(sp);
    var r = Number(a.rate || 1); if(r > 1) t.bonusH += sp.hours * (r - 1);
  });
  t.days = t.reg + t.alt;
  /* 주 단위: 이 달에 일요일이 있는 주들 */
  var w = hrWeekStart(days[0]); if(hrWeekDays(w)[6] < days[0]) w = shiftDate(w, 7);
  for(; hrWeekDays(w)[6] <= days[days.length - 1]; w = shiftDate(w, 7)){ var wk = hrWeekCalc(s, w); t.ot += wk.ot; t.weekly += wk.weeklyPay; }
  if(!cfg.over5) t.night = 0;
  var hourly = s.pay_type !== "monthly";
  t.wage = hourly ? Number(s.pay || 0) : Math.round(Number(s.pay || 0) / 209);   /* 월급제 통상시급 = 월급 / 209 */
  t.base = hourly ? t.hours * t.wage : Number(s.pay || 0);
  t.otPay = t.ot * t.wage * 0.5; t.nightPay = t.night * t.wage * 0.5; t.weeklyPay = hourly ? t.weekly * t.wage : 0; t.bonusPay = t.bonusH * t.wage;
  t.gross = Math.round(t.base + t.otPay + t.nightPay + t.weeklyPay + t.bonusPay);
  /* 공제 */
  var tax = s.tax || "4대보험", r = cfg.rates;
  if(tax === "4대보험"){
    var health = Math.round(t.gross * r.health / 100);
    t.ded = { "국민연금": Math.round(t.gross * r.pension / 100), "건강보험": health, "장기요양": Math.round(health * r.care / 100), "고용보험": Math.round(t.gross * r.employ / 100) };
    t.employer = Math.round(t.gross * (r.pension + r.health + r.employ + 0.25) / 100) + Math.round(health * r.care / 100);   /* 사업주 부담(참고, 산재 제외) */
  }else if(tax === "3.3%"){
    var inc = Math.round(t.gross * (cfg.taxRate / 1.1) / 100); t.ded = { "소득세(3%)": inc, "지방소득세(0.3%)": Math.round(inc / 10) };
  }
  t.dedTotal = Object.keys(t.ded).reduce(function(a, k){ return a + t.ded[k]; }, 0);
  t.net = t.gross - t.dedTotal;
  ["hours","night","ot","weekly","bonusH"].forEach(function(k){ t[k] = hrRound(t[k]); });
  return t;
}
/* 퇴직금 추정: 1년 이상 근속 — 최근 3개월 총지급 / 91일 × 30일 × 근속년수 */
async function hrSeverance(s){
  if(!s.start_date) return null;
  var days = Math.round((new Date(todayStr() + "T00:00:00") - new Date(s.start_date + "T00:00:00")) / 864e5);
  if(days < 365) return { days:days, ok:false };
  var ms = [], x = new Date(todayStr().slice(0, 7) + "-01T00:00:00");
  for(var i = 1; i <= 3; i++){ x.setMonth(x.getMonth() - 1); ms.push(monthStr(x)); }
  for(var j = 0; j < ms.length; j++) await hrLoadMonth(ms[j]);
  var sum = ms.reduce(function(a, m){ return a + hrCalc(s, m).gross; }, 0);
  return { days:days, ok:true, months:ms, avgDay:sum / 91, amount:Math.round(sum / 91 * 30 * (days / 365)) };
}

/* ---------- 칸 편집 ---------- */
function hrCell(staffId, date){
  var s = HR.staff.find(function(x){ return x.id === staffId; }); if(!s) return;
  var a = HR.att[staffId + "|" + date], c = hrSched(s);
  HR.pop = a ? deepClone(a) : { id:"att_" + staffId + "_" + date, staff_id:staffId, date:date, status: hrOnDuty(s, date) ? "정규" : "휴무", start:c.start, end:c.end, break_min:c.brk, rate:1, memo:"", _new:true };
  if(!HR.pop.start) HR.pop.start = c.start; if(!HR.pop.end) HR.pop.end = c.end;
  render();
}
function hrPopSet(k, v){ if(HR.pop){ HR.pop[k] = v; if(k === "status" || k === "rate") render(); } }
async function hrPopSave(){
  var p = HR.pop; if(!p) return;
  if(p.status === "변형" && (!p.start || !p.end)){ await uiAlert("시작·종료 시각을 넣어 주세요", "", "warn"); return; }
  var row = { id:p.id, store:view.storeKey || "hanok", staff_id:p.staff_id, date:p.date, status:p.status,
              start:p.status === "변형" ? p.start : "", end:p.status === "변형" ? p.end : "", break_min:p.status === "변형" ? Number(p.break_min || 0) : 0,
              rate:Number(p.rate || 1), memo:(p.memo || "").trim(), by:(SESSION && SESSION.who) || "" };
  try{
    await sb("/rest/v1/attendance?on_conflict=id", { method:"POST", body:row, prefer:"resolution=merge-duplicates,return=minimal" });
    HR.att[row.staff_id + "|" + row.date] = row; HR.pop = null; render();
  }catch(e){ await uiAlert("저장 실패", e.message || String(e), "warn"); }
}
async function hrPopDel(){
  var p = HR.pop; if(!p) return;
  if(p._new){ HR.pop = null; render(); return; }
  try{
    await sb("/rest/v1/attendance?id=eq." + encodeURIComponent(p.id), { method:"DELETE", prefer:"return=minimal" });
    delete HR.att[p.staff_id + "|" + p.date]; HR.pop = null; render();
  }catch(e){ await uiAlert("지우지 못했습니다", e.message || String(e), "warn"); }
}
/* 한 주를 정규 근무대로 한 번에 ○ (안 찍힌 정규 근무일만) */
async function hrFillWeek(staffId){
  var s = HR.staff.find(function(x){ return x.id === staffId; }); if(!s) return;
  var rows = hrWeekDays(HR.week).filter(function(d){ return d <= todayStr() && hrOnDuty(s, d) && !HR.att[staffId + "|" + d]; })
    .map(function(d){ return { id:"att_" + staffId + "_" + d, store:view.storeKey || "hanok", staff_id:staffId, date:d, status:"정규", start:"", end:"", break_min:0, rate:1, memo:"", by:(SESSION && SESSION.who) || "" }; });
  if(!rows.length){ showToast("찍을 칸이 없습니다"); return; }
  try{
    await sb("/rest/v1/attendance?on_conflict=id", { method:"POST", body:rows, prefer:"resolution=merge-duplicates,return=minimal" });
    rows.forEach(function(r){ HR.att[r.staff_id + "|" + r.date] = r; }); showToast(hrLabel(s) + " · " + rows.length + "일 ○"); render();
  }catch(e){ await uiAlert("저장 실패", e.message || String(e), "warn"); }
}

/* ---------- 직원 편집 ---------- */
function hrStaffNew(){ HR.edit = { id:newId("stf"), name:"", nick:"", role:"", phone:"", pay_type:"hourly", pay:0, tax:"4대보험", weekly_pay:true, sched:{days:[false,true,true,true,true,true,true], start:"10:00", end:"22:00", break:60}, start_date:todayStr(), end_date:null, memo:"", active:true, sort:HR.staff.length, _new:true }; render(); }
function hrStaffEdit(id){ var s = HR.staff.find(function(x){ return x.id === id; }); if(!s) return; HR.edit = deepClone(s); HR.edit.sched = hrSchedRaw(HR.edit); HR.edit.sev = null; render(); }
function hrSchedRaw(s){ var c = hrSched(s); return { days:c.days.slice(), start:c.start, end:c.end, break:c.brk }; }
function hrEditSet(k, v){ if(HR.edit) HR.edit[k] = v; }
function hrEditDay(i){ HR.edit.sched.days[i] = !HR.edit.sched.days[i]; render(); }
async function hrStaffSave(){
  var e = HR.edit; if(!e) return;
  if(!(e.name || "").trim() && !(e.nick || "").trim()){ await uiAlert("이름이나 별칭을 적어 주세요", "", "warn"); return; }
  var row = { id:e.id, store:view.storeKey || "hanok", name:(e.name || "").trim() || (e.nick || "").trim(), nick:(e.nick || "").trim(), role:(e.role || "").trim(), phone:phoneNorm(e.phone || ""),
              pay_type:e.pay_type || "hourly", pay:Number(e.pay || 0), tax:e.tax || "4대보험", weekly_pay:e.weekly_pay !== false,
              sched:{ days:e.sched.days, start:e.sched.start || "10:00", end:e.sched.end || "22:00", break:Number(e.sched.break || 0) },
              start_date:e.start_date || null, end_date:e.end_date || null, memo:(e.memo || "").trim(), active:e.active !== false, sort:Number(e.sort || 0) };
  try{
    await sb("/rest/v1/staff?on_conflict=id", { method:"POST", body:row, prefer:"resolution=merge-duplicates,return=minimal" });
    logEvent(e._new ? "직원 추가" : "직원 수정", row.nick || row.name);
    HR.edit = null; HR.loading = true; render(); await hrLoad(); render();
  }catch(err){ await uiAlert("저장 실패", err.message || String(err), "warn"); }
}
async function hrStaffRetire(){
  var e = HR.edit; if(!e || e._new) return;
  var goOn = e.active === false;
  if(!goOn && !await uiConfirm("퇴사 처리할까요?", hrLabel(e) + " 님이 표에서 빠집니다. 근태 기록은 남고, 다시 '재직' 으로 되돌릴 수 있습니다.", {ok:"퇴사 처리", cancel:"취소"})) return;
  e.active = goOn; if(!goOn && !e.end_date) e.end_date = todayStr(); if(goOn) e.end_date = null;
  await hrStaffSave();
}
async function hrShowSeverance(){ var e = HR.edit; if(!e) return; e.sev = { loading:true }; render(); e.sev = await hrSeverance(e) || { none:true }; render(); }
/* ---------- 설정(사업장) ---------- */
function hrSetupOpen(){ HR.setup = deepClone(Object.assign({}, HR_DEF, HR.cfg || {})); HR.setup.rates = Object.assign({}, HR_DEF.rates, (HR.cfg || {}).rates || {}); render(); }
async function hrSetupSave(){
  var d = HR.setup; if(!d) return;
  try{
    await sb("/rest/v1/hr_settings?on_conflict=store", { method:"POST", body:{ store:view.storeKey || "hanok", data:d }, prefer:"resolution=merge-duplicates,return=minimal" });
    HR.cfg = d; HR.setup = null; logEvent("워크시프트 설정", (d.over5 ? "5인 이상" : "5인 미만")); render();
  }catch(e){ await uiAlert("저장 실패", e.message || String(e), "warn"); }
}

/* ---------- 화면 ---------- */
function sheetStaff(){
  if(!HR || HR.loading) return '<p class="muted" style="padding:20px 0">불러오는 중…</p>';
  if(HR.err) return '<div class="alert rust"><span class="ic">!</span><div><div class="a-t">불러오지 못했습니다</div><div class="a-s">' + esc(HR.err) + '</div></div></div><div class="btn-row" style="margin-top:12px"><button class="btn" onclick="HR.loading=true; render(); hrLoad().then(render)">다시 시도</button></div>';
  var list = HR.staff.filter(function(s){ return s.active !== false || HR.showRetired; });
  var top = '<div class="hr-top"><div class="seg"><button class="' + (HR.view === "week" ? "on" : "") + '" onclick="HR.view=\'week\'; render()">주간표</button><button class="' + (HR.view === "pay" ? "on" : "") + '" onclick="HR.view=\'pay\'; render()">급여</button></div>' +
      '<div class="btn-row"><button class="btn sm ghost" onclick="HR.showRetired=!HR.showRetired; render()">' + (HR.showRetired ? "퇴사자 숨기기" : "퇴사자 보기") + '</button>' +
      '<button class="btn sm ghost" onclick="hrSetupOpen()">설정</button><button class="btn sm primary" onclick="hrStaffNew()">＋ 직원</button></div></div>';
  var body = !list.length ? '<div class="empty">직원이 없습니다. "＋ 직원" 으로 첫 사람을 넣고 정규 근무(요일·시간)를 정해 두면, 칸을 눌러 ○ 만 찍으면 됩니다.</div>'
           : HR.view === "pay" ? hrPayView(list) : hrWeekView(list);
  return top + body + (HR.pop ? hrPopHtml() : "") + (HR.edit ? hrEditHtml() : "") + (HR.slip ? hrSlipHtml() : "") + (HR.setup ? hrSetupHtml() : "");
}
function hrWeekView(list){
  var days = hrWeekDays(HR.week), today = todayStr(), cfg = hrCfg();
  var w0 = new Date(days[0] + "T00:00:00"), w6 = new Date(days[6] + "T00:00:00");
  var nav = '<div class="hr-mon"><button class="bnav" onclick="hrMoveWeek(-1)">&lsaquo;</button><b>' + (w0.getMonth() + 1) + '/' + w0.getDate() + ' – ' + (w6.getMonth() + 1) + '/' + w6.getDate() + '</b><button class="bnav" onclick="hrMoveWeek(1)">&rsaquo;</button>' +
      (HR.week !== hrWeekStart(today) ? '<button class="btn sm ghost" onclick="HR.week=hrWeekStart(todayStr()); HR.loading=true; render(); hrLoadRange().then(function(){ HR.loading=false; render(); })">이번 주</button>' : '') + '</div>';
  var ths = days.map(function(d){ var dt = new Date(d + "T00:00:00"), dow = dt.getDay(), hol = isHoliday(d);
    return '<th class="' + (d === today ? "today " : "") + (dow === 0 || hol ? "sun" : dow === 6 ? "sat" : "") + '"><b>' + HR_DAYS[dow] + '</b><small>' + (dt.getMonth() + 1) + '/' + dt.getDate() + (hol ? ' 공휴' : '') + '</small></th>'; }).join("");
  var trs = list.map(function(s){
    var wk = hrWeekCalc(s, HR.week);
    var tds = days.map(function(d){
      var a = HR.att[s.id + "|" + d], duty = hrOnDuty(s, d), past = d <= today, sp = hrSpan(s, a);
      var cls = "hc" + (a ? " " + ({"정규":"reg","변형":"alt","결근":"abs","휴무":"off"}[a.status]) : (duty && past ? " due" : "")) + (d === today ? " today" : "");
      var sub = sp ? (a.status === "변형" ? hm(a.start).replace(/^오[전후] /, "") + "–" + hm(a.end).replace(/^오[전후] /, "") : hrRound(sp.hours) + "h") : (a ? "" : (duty ? "정규" : ""));
      return '<td class="' + cls + '" onclick="hrCell(\'' + s.id + '\',\'' + d + '\')"><span class="m">' + (a ? HR_STATUS[a.status] : "") + '</span><small>' + esc(sub) + '</small>' +
        (a && Number(a.rate) > 1 ? '<i class="r">' + a.rate + '</i>' : '') + (a && a.memo ? '<i class="dot" title="' + esc(a.memo) + '"></i>' : '') + '</td>';
    }).join("");
    return '<tr' + (s.active === false ? ' class="gone"' : '') + '><th class="hr-name"><button class="hr-nm" onclick="hrStaffEdit(\'' + s.id + '\')"><b>' + esc(hrLabel(s)) + '</b><small>' + esc(s.nick && s.name !== s.nick ? s.name + " · " : "") + esc(s.role || "") + (s.active === false ? " · 퇴사" : "") + '</small></button>' +
      (s.active !== false ? '<button class="hr-fill" onclick="hrFillWeek(\'' + s.id + '\')" title="이번 주 정규 근무일을 한 번에 ○">○ 채우기</button>' : '') + '</th>' + tds +
      '<td class="hr-sum"><b>' + hrRound(wk.hours) + 'h</b><small>' + wk.days + '일' + (wk.ot ? ' · 연장 ' + hrRound(wk.ot) : '') + (wk.night ? ' · 야간 ' + hrRound(wk.night) : '') + (wk.weeklyPay ? ' · 주휴 ' + hrRound(wk.weeklyPay) + 'h' : '') + (wk.absent ? ' · <span class="rust">결근 ' + wk.absent + '</span>' : '') + '</small></td></tr>';
  }).join("");
  return nav + '<div class="hr-scroll"><table class="hr-grid week"><thead><tr><th class="hr-name"></th>' + ths + '<th class="hr-sum">이번 주</th></tr></thead><tbody>' + trs + '</tbody></table></div>' +
    '<div class="hr-legend"><span><i class="hc reg">○</i>정규</span><span><i class="hc alt">△</i>다른 시간</span><span><i class="hc abs">×</i>결근</span><span><i class="hc off">–</i>휴무</span><span><i class="hc due"></i>안 찍은 근무일</span><span><i class="r-ex">1.5</i>배율(휴일 등)</span><span><i class="dot-ex"></i>메모</span></div>' +
    '<p class="f-note">칸을 누르면 찍습니다. 이름을 누르면 정규 근무·급여를 고치고, "○ 채우기" 는 이번 주 정규 근무일을 한 번에 찍습니다. 시간은 정규 근무에서 자동, 다른 시간(△)은 적은 시각으로. ' +
      (cfg.over5 ? '5인 이상 사업장: 하루 8h·주 40h 넘김 연장 ×1.5, 22~06시 야간 ×1.5(설정에서 바꿈).' : '5인 미만 사업장으로 설정됨: 연장·야간 가산 없음.') + '</p>';
}
function hrPayView(list){
  var m = HR.month, mx = new Date(m + "-01T00:00:00"), title = mx.getFullYear() + "년 " + (mx.getMonth() + 1) + "월";
  var nav = '<div class="hr-mon"><button class="bnav" onclick="hrMoveMonth(-1)">&lsaquo;</button><b>' + title + '</b><button class="bnav" onclick="hrMoveMonth(1)">&rsaquo;</button>' + (m !== monthStr() ? '<button class="btn sm ghost" onclick="HR.month=monthStr(); hrMoveMonth(0)">이번 달</button>' : '') + '</div>';
  var tot = { gross:0, ded:0, net:0, employer:0 };
  var rows = list.map(function(s){
    var t = hrCalc(s, m); tot.gross += t.gross; tot.ded += t.dedTotal; tot.net += t.net; tot.employer += t.employer;
    var extra = [];
    if(t.ot) extra.push("연장 " + t.ot + "h"); if(t.night) extra.push("야간 " + t.night + "h"); if(t.weekly) extra.push("주휴 " + t.weekly + "h"); if(t.bonusH) extra.push("가산 " + t.bonusH + "h");
    return '<tr><td><b>' + esc(hrLabel(s)) + '</b><small>' + esc(s.role || "") + ' · ' + (s.pay_type === "monthly" ? "월급" : "시급 " + hrWon(s.pay)) + '</small></td><td>' + t.days + '일' + (t.abs ? '<small class="rust">결근 ' + t.abs + '</small>' : '') + '</td><td>' + t.hours + 'h' + (extra.length ? '<small>' + extra.join(" · ") + '</small>' : '') + '</td>' +
      '<td class="won">' + hrWon(t.gross) + '</td><td class="won">' + (t.dedTotal ? '−' + hrWon(t.dedTotal) + '<small>' + esc(s.tax || "4대보험") + '</small>' : '<small class="muted">공제 없음</small>') + '</td><td class="won"><b>' + hrWon(t.net) + '</b></td>' +
      '<td><button class="btn sm" onclick="HR.slip={id:\'' + s.id + '\', month:\'' + m + '\'}; render()">계산서</button></td></tr>';
  }).join("");
  return nav + '<div class="card" style="padding:0; overflow:auto"><table class="hr-pay"><thead><tr><th>직원</th><th>근무</th><th>시간</th><th>총지급</th><th>공제</th><th>실지급</th><th></th></tr></thead><tbody>' + rows +
    '<tr class="tot"><td>합계</td><td></td><td></td><td class="won">' + hrWon(tot.gross) + '</td><td class="won">−' + hrWon(tot.ded) + '</td><td class="won"><b>' + hrWon(tot.net) + '</b></td><td></td></tr></tbody></table></div>' +
    '<p class="f-note">총지급 = 기본급 + 연장·야간 가산(5인 이상) + 주휴수당(시급제, 주 15h 이상 개근) + 배율 가산. 공제 = 4대보험(근로자 부담분) 또는 3.3%(사업소득). 사업주 부담 4대보험(산재 제외) 합계 약 ' + hrWon(tot.employer) + '. <b>참고용 계산</b>입니다 — 신고·정산은 세무사/노무사 확인 후.</p>';
}
function hrSlipHtml(){
  var s = HR.staff.find(function(x){ return x.id === HR.slip.id; }); if(!s) return "";
  var m = HR.slip.month, mx = new Date(m + "-01T00:00:00"), title = mx.getFullYear() + "년 " + (mx.getMonth() + 1) + "월", t = hrCalc(s, m), cfg = hrCfg();
  var line = function(k, v, note){ return '<div class="slip-l"><span>' + k + (note ? '<small>' + note + '</small>' : '') + '</span><b>' + v + '</b></div>'; };
  var html = '<div class="slip-h"><b>' + esc(hrLabel(s)) + '</b>' + (s.nick && s.name !== s.nick ? ' <span class="muted">' + esc(s.name) + '</span>' : '') + ' · ' + esc(s.role || "") + '<br><small>' + title + ' 급여 · 근무 ' + t.days + '일 ' + t.hours + 'h · ' + (s.pay_type === "monthly" ? "월급제(통상시급 " + hrWon(t.wage) + ")" : "시급 " + hrWon(t.wage)) + '</small></div>' +
    '<div class="slip-sec">지급</div>' +
    line(s.pay_type === "monthly" ? "월급" : "기본급", hrWon(t.base), s.pay_type === "monthly" ? "" : t.hours + "h × " + hrWon(t.wage)) +
    (t.otPay ? line("연장수당", hrWon(t.otPay), t.ot + "h × 0.5") : "") + (t.nightPay ? line("야간수당", hrWon(t.nightPay), t.night + "h × 0.5") : "") +
    (t.weeklyPay ? line("주휴수당", hrWon(t.weeklyPay), t.weekly + "h") : "") + (t.bonusPay ? line("휴일·배율 가산", hrWon(t.bonusPay), t.bonusH + "h") : "") +
    line("<b>총지급</b>", "<b>" + hrWon(t.gross) + "</b>") +
    '<div class="slip-sec">공제 · ' + esc(s.tax || "4대보험") + '</div>' +
    (Object.keys(t.ded).length ? Object.keys(t.ded).map(function(k){ return line(k, "−" + hrWon(t.ded[k])); }).join("") : line("공제 없음", "0원")) +
    line("<b>실지급</b>", "<b class='pine'>" + hrWon(t.net) + "</b>") +
    (t.employer ? '<p class="f-note">사업주 부담 4대보험(참고, 산재 제외): 약 ' + hrWon(t.employer) + ' — 요율 국민연금 ' + cfg.rates.pension + '% · 건강 ' + cfg.rates.health + '% · 장기요양 ' + cfg.rates.care + '%(건강보험료의) · 고용 ' + cfg.rates.employ + '%</p>' : '') +
    '<p class="f-note">참고용 계산서입니다. 소득세(4대보험 가입자의 간이세액)·비과세 식대·수습 감액 등은 넣지 않았습니다.</p>';
  var text = title + " 급여계산서 · " + hrLabel(s) + (s.nick && s.name !== s.nick ? "(" + s.name + ")" : "") + "\n근무 " + t.days + "일 " + t.hours + "h · " + (s.pay_type === "monthly" ? "월급제" : "시급 " + hrWon(t.wage)) + "\n" +
    (s.pay_type === "monthly" ? "월급 " : "기본급 ") + hrWon(t.base) + (t.otPay ? "\n연장수당 " + hrWon(t.otPay) + " (" + t.ot + "h)" : "") + (t.nightPay ? "\n야간수당 " + hrWon(t.nightPay) + " (" + t.night + "h)" : "") + (t.weeklyPay ? "\n주휴수당 " + hrWon(t.weeklyPay) : "") + (t.bonusPay ? "\n휴일·배율 가산 " + hrWon(t.bonusPay) : "") +
    "\n총지급 " + hrWon(t.gross) + "\n공제(" + (s.tax || "4대보험") + ") " + Object.keys(t.ded).map(function(k){ return k + " " + hrWon(t.ded[k]); }).join(", ") + "\n실지급 " + hrWon(t.net);
  return '<div class="overlay" onclick="HR.slip=null; render()"><div class="sheet" onclick="event.stopPropagation()">' + sheetHead("급여계산서") + '<div class="slip">' + html + '</div>' +
    '<div class="sheet-actions"><button class="btn ghost" onclick="navigator.clipboard&&navigator.clipboard.writeText(' + JSON.stringify(text).replace(/"/g, "&quot;") + ').then(function(){ showToast(\'복사했습니다\'); })">글로 복사</button><button class="btn ghost" onclick="hrPrintSlip()">인쇄</button><button class="btn primary" onclick="HR.slip=null; render()">닫기</button></div></div></div>';
}
function hrPrintSlip(){
  var el = document.querySelector(".slip"); if(!el) return;
  var w = window.open("", "_blank"); if(!w){ uiAlert("팝업이 막혀 있습니다", "브라우저에서 팝업을 허용해 주세요.", "warn"); return; }
  w.document.write('<!doctype html><meta charset="utf-8"><title>급여계산서</title><style>body{font:14px/1.6 sans-serif; padding:24px; max-width:520px} .slip-h{font-size:16px; margin-bottom:12px} .slip-h small{font-size:12px; color:#666} .slip-sec{font-weight:700; margin:14px 0 6px; border-bottom:1px solid #ccc} .slip-l{display:flex; justify-content:space-between; padding:3px 0} .slip-l small{display:block; color:#666; font-size:11px} .f-note{color:#666; font-size:11px}</style>' + el.innerHTML);
  w.document.close(); w.focus(); setTimeout(function(){ w.print(); }, 300);
}
function hrPopHtml(){
  var p = HR.pop, s = HR.staff.find(function(x){ return x.id === p.staff_id; }) || {}, c = hrSched(s);
  var seg = function(k, v, label){ return '<button class="' + (p[k] == v ? "on" : "") + '" onclick="hrPopSet(\'' + k + '\',' + JSON.stringify(v) + ')">' + label + '</button>'; };
  return '<div class="overlay" onclick="HR.pop=null; render()"><div class="sheet" onclick="event.stopPropagation()">' +
    sheetHead(esc(hrLabel(s)) + ' · ' + dateLabel(p.date)) +
    '<p class="f-note" style="margin:-6px 0 12px">정규 근무: ' + esc(hrSchedText(s)) + '</p>' +
    '<div class="seg hr-seg">' + seg("status", "정규", "○ 정규") + seg("status", "변형", "△ 다른 시간") + seg("status", "결근", "× 결근") + seg("status", "휴무", "– 휴무") + '</div>' +
    (p.status === "변형" ? '<div class="grid3" style="margin-top:12px"><label class="f"><div class="lb">시작</div><input type="time" value="' + esc(p.start || c.start) + '" onchange="hrPopSet(\'start\', this.value)"></label>' +
      '<label class="f"><div class="lb">종료</div><input type="time" value="' + esc(p.end || c.end) + '" onchange="hrPopSet(\'end\', this.value)"></label>' +
      '<label class="f"><div class="lb">휴게(분)</div><input type="number" min="0" step="10" value="' + Number(p.break_min || 0) + '" oninput="hrPopSet(\'break_min\', this.value)"></label></div>' : '') +
    (p.status === "정규" || p.status === "변형" ? '<div class="f" style="margin-top:12px"><div class="lb">배율 <span class="lbl-note">휴일 근무 같은 때(연장·야간은 자동)</span></div><div class="seg">' + seg("rate", 1, "1배") + seg("rate", 1.5, "1.5배") + seg("rate", 2, "2배") + '</div></div>' : '') +
    '<label class="f" style="margin-top:12px"><div class="lb">메모 <span class="lbl-note">선택</span></div><input type="text" value="' + esc(p.memo || "") + '" placeholder="예: 늦게 옴, 행사 지원" oninput="hrPopSet(\'memo\', this.value)"></label>' +
    '<div class="sheet-actions">' + (p._new ? '' : '<button class="btn ghost danger" onclick="hrPopDel()">지우기</button>') + '<button class="btn ghost" onclick="HR.pop=null; render()">취소</button><button class="btn primary" data-enter onclick="hrPopSave()">저장</button></div></div></div>';
}
function hrEditHtml(){
  var e = HR.edit, sc = e.sched;
  var daysBtns = HR_DAYS.map(function(d, i){ return '<button class="' + (sc.days[i] ? "on" : "") + '" onclick="hrEditDay(' + i + ')">' + d + '</button>'; }).join("");
  var segv = function(k, v, label){ return '<button class="' + (e[k] === v ? "on" : "") + '" onclick="hrEditSet(\'' + k + '\',' + JSON.stringify(v) + '); render()">' + label + '</button>'; };
  var sev = e.sev ? (e.sev.loading ? '<p class="f-note">계산 중…</p>' : e.sev.none ? '<p class="f-note">입사일이 없어 계산할 수 없습니다.</p>' : !e.sev.ok ? '<p class="f-note">근속 ' + e.sev.days + '일 — 1년(365일)이 되면 퇴직금이 생깁니다.</p>' : '<p class="f-note">근속 ' + e.sev.days + '일 · 최근 3개월(' + e.sev.months.slice().reverse().join(", ") + ') 평균임금 하루 ' + hrWon(e.sev.avgDay) + ' → <b>퇴직금 추정 ' + hrWon(e.sev.amount) + '</b> (30일분 × 근속년수). 참고용.</p>') : '';
  return '<div class="overlay" onclick="HR.edit=null; render()"><div class="sheet sheet-tall" onclick="event.stopPropagation()">' +
    sheetHead(e._new ? "직원 추가" : "직원") +
    '<div class="grid2"><label class="f"><div class="lb">별칭 <span class="lbl-note">화면에 먼저 보임</span></div><input type="text" value="' + esc(e.nick || "") + '" placeholder="예: 만두언니" oninput="hrEditSet(\'nick\', this.value)"></label>' +
    '<label class="f"><div class="lb">이름</div><input type="text" value="' + esc(e.name || "") + '" oninput="hrEditSet(\'name\', this.value)"></label></div>' +
    '<div class="grid2"><label class="f"><div class="lb">역할 <span class="lbl-note">홀·주방 등</span></div><input type="text" value="' + esc(e.role || "") + '" oninput="hrEditSet(\'role\', this.value)"></label>' +
    '<label class="f"><div class="lb">전화</div><input type="tel" value="' + esc(e.phone || "") + '" oninput="hrEditSet(\'phone\', this.value)"></label></div>' +
    '<div class="grid2"><div class="f"><div class="lb">급여</div><div class="seg">' + segv("pay_type", "hourly", "시급") + segv("pay_type", "monthly", "월급") + '</div></div>' +
    '<label class="f"><div class="lb">' + (e.pay_type === "monthly" ? "월급(원)" : "시급(원)") + '</div><input type="number" min="0" step="100" value="' + Number(e.pay || 0) + '" oninput="hrEditSet(\'pay\', this.value)"></label></div>' +
    '<div class="f"><div class="lb">공제 <span class="lbl-note">4대보험 가입자 / 3.3% 사업소득자 / 없음</span></div><div class="seg">' + segv("tax", "4대보험", "4대보험") + segv("tax", "3.3%", "3.3%") + segv("tax", "없음", "없음") + '</div></div>' +
    (e.pay_type !== "monthly" ? '<div class="f"><div class="lb">주휴수당 <span class="lbl-note">주 15h 이상 개근이면 자동</span></div><div class="seg">' + segv("weekly_pay", true, "계산") + segv("weekly_pay", false, "안 함") + '</div></div>' : '') +
    '<div class="f"><div class="lb">정규 근무 요일</div><div class="seg hr-days">' + daysBtns + '</div></div>' +
    '<div class="grid3"><label class="f"><div class="lb">시작</div><input type="time" value="' + esc(sc.start) + '" onchange="HR.edit.sched.start=this.value"></label><label class="f"><div class="lb">종료</div><input type="time" value="' + esc(sc.end) + '" onchange="HR.edit.sched.end=this.value"></label><label class="f"><div class="lb">휴게(분)</div><input type="number" min="0" step="10" value="' + Number(sc.break || 0) + '" oninput="HR.edit.sched.break=this.value"></label></div>' +
    '<div class="grid2"><label class="f"><div class="lb">입사일</div><input type="date" value="' + esc(e.start_date || "") + '" onchange="hrEditSet(\'start_date\', this.value)"></label><label class="f"><div class="lb">퇴사일 <span class="lbl-note">비우면 재직</span></div><input type="date" value="' + esc(e.end_date || "") + '" onchange="hrEditSet(\'end_date\', this.value || null)"></label></div>' +
    '<label class="f"><div class="lb">메모</div><input type="text" value="' + esc(e.memo || "") + '" oninput="hrEditSet(\'memo\', this.value)"></label>' +
    (e._new ? '' : '<div class="btn-row" style="margin-top:4px"><button class="btn sm ghost" onclick="hrShowSeverance()">퇴직금 계산</button></div>' + sev) +
    '<div class="sheet-actions">' + (e._new ? '' : '<button class="btn ghost ' + (e.active === false ? "" : "danger") + '" onclick="hrStaffRetire()">' + (e.active === false ? "재직으로" : "퇴사") + '</button>') +
    '<button class="btn ghost" onclick="HR.edit=null; render()">취소</button><button class="btn primary" data-enter onclick="hrStaffSave()">저장</button></div></div></div>';
}
function hrSetupHtml(){
  var d = HR.setup, r = d.rates;
  var num = function(path, label, note){ var ks = path.split("."), v = ks.length === 2 ? d[ks[0]][ks[1]] : d[ks[0]]; return '<label class="f"><div class="lb">' + label + (note ? ' <span class="lbl-note">' + note + '</span>' : '') + '</div><input type="number" step="0.001" value="' + v + '" oninput="' + (ks.length === 2 ? 'HR.setup.' + ks[0] + '.' + ks[1] : 'HR.setup.' + ks[0]) + '=Number(this.value)"></label>'; };
  return '<div class="overlay" onclick="HR.setup=null; render()"><div class="sheet" onclick="event.stopPropagation()">' + sheetHead("워크시프트 설정") +
    '<div class="f"><div class="lb">사업장 규모 <span class="lbl-note">사장님 제외 동시 근무 5인 이상이면 연장·야간·휴일 가산 의무</span></div><div class="seg"><button class="' + (d.over5 ? "on" : "") + '" onclick="HR.setup.over5=true; render()">5인 이상</button><button class="' + (!d.over5 ? "on" : "") + '" onclick="HR.setup.over5=false; render()">5인 미만</button></div></div>' +
    '<div class="f"><div class="lb">주휴수당 자동 계산</div><div class="seg"><button class="' + (d.weeklyPay !== false ? "on" : "") + '" onclick="HR.setup.weeklyPay=true; render()">켬</button><button class="' + (d.weeklyPay === false ? "on" : "") + '" onclick="HR.setup.weeklyPay=false; render()">끔</button></div></div>' +
    '<div class="subhead">4대보험 근로자 부담 요율(%) <span>매년 1월 바뀝니다 — 확인 후 고치세요</span></div>' +
    '<div class="grid2">' + num("rates.pension", "국민연금") + num("rates.health", "건강보험") + num("rates.care", "장기요양", "건강보험료의 %") + num("rates.employ", "고용보험") + '</div>' +
    '<div class="grid2">' + num("taxRate", "사업소득 원천징수(%)", "3.3 = 소득세 3 + 지방 0.3") + '<div class="f"><div class="lb">야간 시간대</div><div class="grid2"><input type="time" value="' + esc(d.night[0]) + '" onchange="HR.setup.night[0]=this.value"><input type="time" value="' + esc(d.night[1]) + '" onchange="HR.setup.night[1]=this.value"></div></div></div>' +
    '<div class="sheet-actions"><button class="btn ghost" onclick="HR.setup=null; render()">취소</button><button class="btn primary" onclick="hrSetupSave()">저장</button></div></div></div>';
}
/* Esc: 작은 창이 떠 있으면 그것부터 닫음(18-router 의 키 처리에서 부름) */
function hrEsc(){ if(!HR || !(view.form && view.form.type === "staff")) return false; var k = ["pop","edit","slip","setup"].find(function(x){ return HR[x]; }); if(k){ HR[k] = null; render(); return true; } return false; }
