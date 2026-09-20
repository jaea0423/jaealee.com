/* ---------- 워크시프트 (staff · attendance · hr_settings, 15·17·18차) ----------
   사장님이 직접 찍는 주간 근무표 + 월 급여 계산. 화면형(view.form={type:"staff", page:true}) — 사장님 메뉴, 관리자 비밀번호 뒤.
   · 표는 한 주(월~일), 역할(주방·홀)별로 묶음. 줄 = 직원(별칭 우선), 칸 = 날. 안 찍힌 칸을 누르면 상태는 비어 있고(기본 안 찍힘) 배율만 1배.
     ○ 정규 / △ 다른 시간(한 타임 또는 두 타임) / × 결근 / – 휴무 + 배율(휴일 등) + 메모
   · 정규 근무·시급은 **기간별**(sched_hist / pay_hist: from 날짜부터). 그 날짜에 맞는 것을 씁니다 — 바뀐 뒤에도 옛 달 계산이 안 틀림.
     하루 두 타임(점심·저녁)은 spans 로. 다른 시간(△)도 두 타임 가능(attendance.spans)
   · 급여(월): 기본급 + 연장(하루 8h·주 40h 넘김 ×0.5) + 야간(22~06 ×0.5) + 주휴수당(시급제, 주 15h 이상 개근) + 배율 가산
     − 공제(4대보험 / 3.3% / 없음) = 실지급. 연장·야간 가산은 '5인 이상' 일 때만(설정).
     월급제 = 월급 고정(통상시급 = 월급/209) + 연장·야간·배율 가산 [+ 결근 일할 공제(직원마다 켬/끔)] − 공제. 퇴직금은 1년 이상 근속자 추정.
   · 세금·보험은 참고용 — 최종 신고는 세무사/노무사와. */
var HR = null;
var HR_STATUS = { "정규":"○", "변형":"△", "결근":"×", "휴무":"–" };
var HR_DAYS = ["일","월","화","수","목","금","토"];
var HR_DEF = { over5:true, rates:{ pension:4.5, health:3.545, care:12.95, employ:0.9 }, night:["22:00","06:00"], taxRate:3.3, weeklyPay:true };
var HR_ROLES = ["주방", "홀"];   /* 묶는 순서. 다른 역할은 뒤에 '기타' */

async function openStaffPage(){
  if(!supaOn()){ await uiAlert("서버 설정이 없는 빌드입니다", "워크시프트는 서버가 있어야 합니다.", "warn"); return; }
  if(!view.adminOk){ if(!await adminGate("워크시프트 열기")) return; view.adminOk = true; }
  view.form = {type:"staff", page:true};
  if(!HR) HR = { week: hrWeekStart(todayStr()), month: monthStr(), staff:[], att:{}, loaded:{}, cfg:null, loading:true, pop:null, edit:null, view:"week", slip:null, setup:false, retired:false };
  render(); await hrLoad(); render();
}
function hrWeekStart(d){ var x = new Date(d + "T00:00:00"), dow = (x.getDay() + 6) % 7; return shiftDate(d, -dow); }
function hrWeekDays(w){ var out = []; for(var i = 0; i < 7; i++) out.push(shiftDate(w, i)); return out; }
/* "9월 3주차" — 그 주의 목요일이 속한 달·주(ISO 식). 월요일이 전달이면 앞 달의 5주차 같은 식으로 자연스럽게 */
function hrWeekLabel(w){ var th = new Date(shiftDate(w, 3) + "T00:00:00"); return (th.getMonth() + 1) + "월 " + (Math.floor((th.getDate() - 1) / 7) + 1) + "주차"; }
function hrMonthEnd(m){ var d = new Date(m + "-01T00:00:00"); d.setMonth(d.getMonth() + 1); d.setDate(0); return m + "-" + pad(d.getDate()); }
function hrMonthDays(m){ var n = Number(hrMonthEnd(m).slice(8)), out = []; for(var i = 1; i <= n; i++) out.push(m + "-" + pad(i)); return out; }
function hrCfg(){ var c = (HR && HR.cfg) || {}; return { over5: c.over5 !== false, over5Mode: c.over5Mode || "auto", inclusive: !!c.inclusive, rates: Object.assign({}, HR_DEF.rates, c.rates || {}), night: c.night || HR_DEF.night, taxRate: c.taxRate != null ? c.taxRate : HR_DEF.taxRate, weeklyPay: c.weeklyPay !== false }; }
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
    var mx = new Date(HR.month + "-01T00:00:00"); mx.setMonth(mx.getMonth() - 1); ms[monthStr(mx)] = 1; mx.setMonth(mx.getMonth() + 2); ms[monthStr(mx)] = 1;
    for(var m in ms) await hrLoadMonth(m);
  }catch(e){ HR.err = e.message || String(e); }
}
async function hrMoveWeek(d){ HR.week = d === 0 ? hrWeekStart(todayStr()) : shiftDate(HR.week, 7 * d); HR.loading = true; render(); await hrLoadRange(); HR.loading = false; render(); }
async function hrMoveMonth(d){ if(d === 0) HR.month = monthStr(); else { var x = new Date(HR.month + "-01T00:00:00"); x.setMonth(x.getMonth() + d); HR.month = monthStr(x); } HR.loading = true; render(); await hrLoadRange(); HR.loading = false; render(); }
function hrLabel(s){ return s.nick || s.name; }
function hrRole(s){ var r = (s.role || "").trim(); return HR_ROLES.find(function(x){ return r.indexOf(x) >= 0; }) || (r || "기타"); }

/* ---------- 기간별 정규 근무·시급 ----------
   sched_hist: [{from, days:[7], spans:[{start,end,break}]}] · pay_hist: [{from, pay}]. 비어 있으면 옛 칸(sched/pay)을 from 없음으로 씀 */
function hrSchedHist(s){
  var h = Array.isArray(s.sched_hist) && s.sched_hist.length ? s.sched_hist : [ Object.assign({from:""}, hrSchedFromOld(s.sched)) ];
  return h.slice().sort(function(a, b){ return (a.from || "").localeCompare(b.from || ""); });
}
function hrSchedFromOld(x){ x = x || {}; return { days: x.days && x.days.length === 7 ? x.days.slice() : [false,false,false,false,false,false,false], spans: x.spans && x.spans.length ? x.spans : [{ start: x.start || "10:00", end: x.end || "22:00", break: Number(x.break || 0) }] }; }
function hrSchedAt(s, date){ var h = hrSchedHist(s), cur = h[0]; h.forEach(function(e){ if(!e.from || e.from <= date) cur = e; }); return { days: cur.days || [false,false,false,false,false,false,false], spans: (cur.spans && cur.spans.length ? cur.spans : [{start:"10:00", end:"22:00", break:0}]) }; }
function hrPayHist(s){ var h = Array.isArray(s.pay_hist) && s.pay_hist.length ? s.pay_hist : [{ from:"", pay:Number(s.pay || 0) }]; return h.slice().sort(function(a, b){ return (a.from || "").localeCompare(b.from || ""); }); }
function hrPayAt(s, date){ var h = hrPayHist(s), cur = h[0]; h.forEach(function(e){ if(!e.from || e.from <= date) cur = e; }); return Number(cur.pay || 0); }
function hrSpanText(sp){ return sp.start + "–" + sp.end + (Number(sp.break) ? "(휴게 " + sp.break + ")" : ""); }   /* 24시간 표기 — 오전/오후를 떼면 10:00–3:00 처럼 헷갈림 */
function hrSchedText(s, date){ var c = hrSchedAt(s, date || todayStr()), ds = HR_DAYS.filter(function(_, i){ return c.days[i]; }); return ds.length ? ds.join("·") + " " + c.spans.map(hrSpanText).join(" + ") : "정규 근무 없음"; }
function hrOnDuty(s, date){ var c = hrSchedAt(s, date), dow = new Date(date + "T00:00:00").getDay(); if(!c.days[dow]) return false; if(s.start_date && date < s.start_date) return false; if(s.end_date && date > s.end_date) return false; return true; }
/* 한 칸의 근무 구간들 — [{s0,e0,brk,hours}]. 정규는 그 날짜의 시간표, 변형은 적힌 시각(spans 우선, 없으면 start/end) */
function hrSpans(s, a){
  if(!a || (a.status !== "정규" && a.status !== "변형")) return [];
  var raw = a.status === "정규" ? hrSchedAt(s, a.date).spans : (Array.isArray(a.spans) && a.spans.length ? a.spans : [{start:a.start, end:a.end, break:a.break_min}]);
  var out = [];
  raw.forEach(function(sp){ if(!sp || !sp.start || !sp.end) return; var s0 = toMin(sp.start), e0 = toMin(sp.end); if(e0 <= s0) e0 += 24 * 60; var brk = Number(sp.break || 0); out.push({ s0:s0, e0:e0, brk:brk, hours:Math.max(0, (e0 - s0 - brk) / 60) }); });
  return out;
}
function hrHours(s, a){ return hrSpans(s, a).reduce(function(t, sp){ return t + sp.hours; }, 0); }
function hrNight(sps){
  var n = hrCfg().night, ns = toMin(n[0]), ne = toMin(n[1]) + 24 * 60, h = 0;
  sps.forEach(function(sp){ var hh = 0; [[ns, ne], [ns - 1440, ne - 1440], [ns + 1440, ne + 1440]].forEach(function(w){ var a = Math.max(sp.s0, w[0]), b = Math.min(sp.e0, w[1]); if(b > a) hh += (b - a) / 60; }); h += Math.min(hh, sp.hours); });
  return h;
}
function hrRound(h){ return Math.round(h * 10) / 10; }
function hrWon(n){ return Math.round(Number(n || 0)).toLocaleString("ko-KR") + "원"; }
/* 상시 근로자 5인 이상인지 — 근로기준법 시행령 7조의2 방식(재아 09-20: "그날 몇 명 나왔느냐가 아니라 어떻게 세느냐").
   한 달(여기서는 그 급여 달) 동안 날마다 나온 사람 수를 전부 더해 영업일 수로 나눈 평균이 5 이상이면 5인 이상.
   단, 평균이 5 이상이라도 5인 미만인 날이 영업일의 절반 이상이면 미만으로, 평균이 5 미만이라도 5인 이상인 날이 절반 이상이면 이상으로 봅니다.
   영업일 = 한 명이라도 근무를 찍은 날. 사장님은 직원 표에 없으니 자연히 빠집니다. 설정이 '자동' 이 아니면 설정값 그대로 */
function hrOver5Note(month){
  var c = hrCfg(), r = hrOver5Calc(month), m = month.split("-");
  var what = c.over5Mode === "auto" ? (m[1].replace(/^0/, "") + "월 근태 기준 하루 평균 " + r.avg + "명(영업일 " + r.biz + "일 · 5인 미만인 날 " + r.under + "일) → ") : "설정: ";
  return what + (hrOver5(month) ? "5인 이상 사업장 — 하루 8h·주 40h 넘김 연장 ×1.5, 22~06시 야간 ×1.5." : "5인 미만 사업장 — 연장·야간 가산 없음(정규 외 시간은 ×1.0).");
}
function hrOver5(month){
  var c = hrCfg();
  if(c.over5Mode !== "auto") return c.over5;
  var r = hrOver5Calc(month); return r.over5;
}
function hrOver5Calc(month){
  var days = hrMonthDays(month), cnt = {}, total = 0, biz = 0, under = 0, over = 0;
  HR.staff.forEach(function(st){
    days.forEach(function(d){ var a = HR.att[st.id + "|" + d]; if(!a || a.status === "결근" || a.status === "휴무") return; if(!hrSpans(st, a).length) return; cnt[d] = (cnt[d] || 0) + 1; });
  });
  days.forEach(function(d){ var n = cnt[d] || 0; if(!n) return; biz++; total += n; if(n < 5) under++; else over++; });
  var avg = biz ? total / biz : 0, over5 = avg >= 5;
  if(over5 && under * 2 >= biz) over5 = false;          /* 평균은 5 넘는데 5인 미만인 날이 절반 이상 */
  if(!over5 && biz && over * 2 >= biz) over5 = true;   /* 평균은 5 아래인데 5인 이상인 날이 절반 이상 */
  return { over5: over5, avg: Math.round(avg * 10) / 10, biz: biz, under: under, over: over };
}
function hrWeekCalc(s, w){
  var cfg = hrCfg(), _m = w.slice(0, 7); cfg.over5 = hrOver5(_m); t = { hours:0, ot:0, night:0, days:0, absent:0, dutyDays:0, sched:0, weeklyPay:0 };
  hrWeekDays(w).forEach(function(d){
    var duty = hrOnDuty(s, d);
    if(duty){ t.dutyDays++; t.sched += hrSchedAt(s, d).spans.reduce(function(a, sp){ var s0 = toMin(sp.start), e0 = toMin(sp.end); if(e0 <= s0) e0 += 1440; return a + Math.max(0, (e0 - s0 - Number(sp.break || 0)) / 60); }, 0); }
    var a = HR.att[s.id + "|" + d]; if(!a) return;
    if(a.status === "결근"){ t.absent++; return; }
    var sps = hrSpans(s, a); if(!sps.length) return;
    var h = sps.reduce(function(x, sp){ return x + sp.hours; }, 0);
    t.days++; t.hours += h; t.night += hrNight(sps); if(h > 8) t.ot += h - 8;
  });
  t.ot += Math.max(0, t.hours - 40 - t.ot);
  if(!cfg.over5){ t.ot = 0; t.night = 0; }
  if(s.pay_type !== "monthly" && s.weekly_pay !== false && cfg.weeklyPay && t.sched >= 15 && t.dutyDays > 0 && !t.absent && t.days >= t.dutyDays) t.weeklyPay = Math.min(t.hours, 40) / 40 * 8;
  return t;
}
/* 한 달 급여. 시급이 달 중간에 바뀌면 날마다 그날 시급으로 셉니다(basePay). 연장·야간·주휴·배율은 달의 마지막 날 시급 기준 */
function hrCalc(s, month){
  var cfg = hrCfg(); cfg.over5 = hrOver5(month); var days = hrMonthDays(month), t = { reg:0, alt:0, abs:0, off:0, days:0, hours:0, night:0, ot:0, weekly:0, bonusH:0, base:0, otPay:0, nightPay:0, weeklyPay:0, bonusPay:0, absentPay:0, extraH:0, extraPay:0, gross:0, ded:{}, dedTotal:0, net:0, employer:0, wage:0, log:[] };
  var hourly = s.pay_type !== "monthly", last = days[days.length - 1];
  var monthPay = hrPayAt(s, last);
  t.wage = hourly ? monthPay : Math.round(monthPay / 209);
  days.forEach(function(d){
    var a = HR.att[s.id + "|" + d]; if(!a) return;
    if(a.status === "정규") t.reg++; else if(a.status === "변형") t.alt++; else if(a.status === "결근") t.abs++; else if(a.status === "휴무") t.off++;
    var sps = hrSpans(s, a), h = sps.reduce(function(x, sp){ return x + sp.hours; }, 0), r = Number(a.rate || 1), w = hourly ? hrPayAt(s, d) : t.wage;
    t.log.push({ date:d, status:a.status, spans:sps, hours:h, rate:r, memo:a.memo || "", wage:w });
    if(!sps.length) return;
    t.hours += h; t.night += hrNight(sps); if(hourly) t.base += h * w;
    /* 월급제: 월급은 '정규 근무 시간' 값입니다. 그날 정규 시간을 넘긴 만큼(휴무일 출근은 전부)은 통상시급 × 1.0 을 따로 줍니다(초과 기본분, 재아 09-20).
       그 위에 연장 0.5 가산(5인 이상)은 아래 otPay 에서. 포괄임금(월급에 연장 포함)이면 설정에서 끔 */
    if(!hourly && !cfg.inclusive){ var sh = hrOnDuty(s, d) ? hrSchedAt(s, d).spans.reduce(function(a2, sp){ var s0 = toMin(sp.start), e0 = toMin(sp.end); if(e0 <= s0) e0 += 1440; return a2 + Math.max(0, (e0 - s0 - Number(sp.break || 0)) / 60); }, 0) : 0; if(h > sh) t.extraH += h - sh; }
    if(r > 1) t.bonusH += h * (r - 1);
  });
  t.days = t.reg + t.alt;
  var w0 = hrWeekStart(days[0]); if(hrWeekDays(w0)[6] < days[0]) w0 = shiftDate(w0, 7);
  for(; hrWeekDays(w0)[6] <= last; w0 = shiftDate(w0, 7)){ var wk = hrWeekCalc(s, w0); t.ot += wk.ot; t.weekly += wk.weeklyPay; }
  if(!cfg.over5) t.night = 0;
  if(!hourly){ t.base = monthPay; if(s.absent_deduct && t.abs) t.absentPay = -Math.round(t.abs * t.wage * 8); }
  t.otPay = t.ot * t.wage * 0.5; t.nightPay = t.night * t.wage * 0.5; t.weeklyPay = hourly ? t.weekly * t.wage : 0; t.bonusPay = t.bonusH * t.wage; t.extraPay = t.extraH * t.wage;
  t.gross = Math.round(t.base + t.extraPay + t.otPay + t.nightPay + t.weeklyPay + t.bonusPay + t.absentPay);
  var tax = s.tax || "4대보험", r = cfg.rates;
  if(tax === "4대보험"){
    var health = Math.round(t.gross * r.health / 100);
    t.ded = { "국민연금": Math.round(t.gross * r.pension / 100), "건강보험": health, "장기요양": Math.round(health * r.care / 100), "고용보험": Math.round(t.gross * r.employ / 100) };
    t.employer = Math.round(t.gross * (r.pension + r.health + r.employ + 0.25) / 100) + Math.round(health * r.care / 100);
  }else if(tax === "3.3%"){ var inc = Math.round(t.gross * (cfg.taxRate / 1.1) / 100); t.ded = { "소득세(3%)": inc, "지방소득세(0.3%)": Math.round(inc / 10) }; }
  t.dedTotal = Object.keys(t.ded).reduce(function(a, k){ return a + t.ded[k]; }, 0);
  t.net = t.gross - t.dedTotal;
  ["hours","night","ot","weekly","bonusH","extraH"].forEach(function(k){ t[k] = hrRound(t[k]); });
  return t;
}
async function hrSeverance(s){
  if(!s.start_date) return null;
  var end = s.end_date && s.end_date < todayStr() ? s.end_date : todayStr();
  var days = Math.round((new Date(end + "T00:00:00") - new Date(s.start_date + "T00:00:00")) / 864e5) + 1;
  if(days < 365) return { days:days, ok:false };
  var ms = [], x = new Date(end.slice(0, 7) + "-01T00:00:00");
  for(var i = 1; i <= 3; i++){ x.setMonth(x.getMonth() - 1); ms.push(monthStr(x)); }
  for(var j = 0; j < ms.length; j++) await hrLoadMonth(ms[j]);
  var sum = ms.reduce(function(a, m){ return a + hrCalc(s, m).gross; }, 0);
  return { days:days, ok:true, months:ms.slice().reverse(), sum:sum, avgDay:sum / 91, amount:Math.round(sum / 91 * 30 * (days / 365)) };
}

/* ---------- 칸 편집 ---------- */
async function hrCell(staffId, date){
  var s = HR.staff.find(function(x){ return x.id === staffId; }); if(!s) return;
  /* 아직 오지 않은 날은 막지 않고 한 번 되묻습니다(재아 09-20: 미래 근무는 미리 알 수 없으니) */
  if(date > todayStr() && !HR.att[staffId + "|" + date]){
    if(!await uiConfirm("아직 오지 않은 날입니다", dateLabel(date) + " 근무를 미리 찍을까요? 그날 실제와 다르면 다시 고쳐야 합니다.", {ok:"미리 찍기", cancel:"그만"})) return;
  }
  var a = HR.att[staffId + "|" + date], c = hrSchedAt(s, date);
  /* 안 찍힌 칸은 상태 비움(기본 안 찍힘, 재아). 다른 시간 칸은 그 날짜 정규 시간표를 미리 넣어 둠 */
  HR.pop = a ? deepClone(a) : { id:"att_" + staffId + "_" + date, staff_id:staffId, date:date, status:"", spans:c.spans.map(function(sp){ return {start:sp.start, end:sp.end, break:Number(sp.break || 0)}; }), rate:1, memo:"", _new:true };
  if(!Array.isArray(HR.pop.spans) || !HR.pop.spans.length) HR.pop.spans = HR.pop.start ? [{start:HR.pop.start, end:HR.pop.end, break:Number(HR.pop.break_min || 0)}] : c.spans.map(function(sp){ return {start:sp.start, end:sp.end, break:Number(sp.break || 0)}; });
  render();
}
function hrPopSet(k, v){ if(HR.pop){ HR.pop[k] = v; if(k === "status" || k === "rate") render(); } }
function hrPopSpan(i, k, v){ HR.pop.spans[i][k] = k === "break" ? Number(v || 0) : v; }
function hrPopSpanAdd(){ HR.pop.spans.push({start:"17:00", end:"22:00", break:0}); render(); }
function hrPopSpanDel(i){ if(HR.pop.spans.length > 1){ HR.pop.spans.splice(i, 1); render(); } }
async function hrPopSave(){
  var p = HR.pop; if(!p) return;
  if(!p.status){ await uiAlert("무엇으로 찍을지 고르세요", "정규 · 다른 시간 · 결근 · 휴무", "warn"); return; }
  var spans = p.status === "변형" ? p.spans.filter(function(x){ return x.start && x.end; }) : [];
  if(p.status === "변형" && !spans.length){ await uiAlert("시작·종료 시각을 넣어 주세요", "", "warn"); return; }
  var row = { id:p.id, store:view.storeKey || "hanok", staff_id:p.staff_id, date:p.date, status:p.status,
              start:spans[0] ? spans[0].start : "", end:spans[0] ? spans[0].end : "", break_min:spans[0] ? Number(spans[0].break || 0) : 0, spans:spans,
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
/* 날짜 머리 누르기 → 공휴일 지정/해제(토·일은 고정) */
async function hrDayClick(date){
  var dow = new Date(date + "T00:00:00").getDay();
  if(dow === 0 || dow === 6){ await uiAlert(dateLabel(date), dow === 0 ? "일요일은 늘 빨간날입니다." : "토요일은 늘 파란날입니다.", "ok"); return; }
  var hol = isHoliday(date);
  var ok = await uiConfirm(dateLabel(date), hol ? "지금 공휴일(빨간날)입니다. 평일로 되돌릴까요?\n워크시프트 휴일 표시·달력 색이 바뀝니다." : "이 날을 공휴일(빨간날)로 지정할까요?\n워크시프트 휴일 표시·달력 색이 바뀝니다.", {ok: hol ? "평일로" : "공휴일로", cancel:"취소", tone:"ok"});
  if(!ok) return;
  setHolidayFlag(date, !hol); render();
}

/* ---------- 직원 편집 ---------- */
function hrStaffNew(){ HR.edit = { id:newId("stf"), name:"", nick:"", role:"홀", phone:"", pay_type:"hourly", pay:0, tax:"4대보험", weekly_pay:true, absent_deduct:false, sched_hist:[{from:"", days:[false,true,true,true,true,true,true], spans:[{start:"10:00", end:"22:00", break:60}]}], pay_hist:[{from:"", pay:0}], start_date:todayStr(), end_date:null, memo:"", active:true, sort:HR.staff.length, _new:true, tab:"sched" }; render(); }
function hrStaffEdit(id){ var s = HR.staff.find(function(x){ return x.id === id; }); if(!s) return; HR.edit = deepClone(s); HR.edit.sched_hist = hrSchedHist(s).map(function(e){ return { from:e.from || "", days:(e.days || []).slice(), spans:(e.spans || []).map(function(x){ return Object.assign({}, x); }) }; }); HR.edit.pay_hist = hrPayHist(s).map(function(e){ return Object.assign({}, e); }); HR.edit.sev = null; HR.edit.tab = "sched"; render(); }
function hrEditSet(k, v){ if(HR.edit) HR.edit[k] = v; }
function hrEditDay(i, j){ HR.edit.sched_hist[i].days[j] = !HR.edit.sched_hist[i].days[j]; render(); }
function hrEditSpan(i, j, k, v){ HR.edit.sched_hist[i].spans[j][k] = k === "break" ? Number(v || 0) : v; }
function hrEditSpanAdd(i){ HR.edit.sched_hist[i].spans.push({start:"17:00", end:"22:00", break:0}); render(); }
function hrEditSpanDel(i, j){ var sp = HR.edit.sched_hist[i].spans; if(sp.length > 1){ sp.splice(j, 1); render(); } }
function hrEditSchedAdd(){ var h = HR.edit.sched_hist, last = h[h.length - 1]; h.push({ from: monthStr(new Date(Date.now() + 32 * 864e5)) + "-01", days:last.days.slice(), spans:last.spans.map(function(x){ return Object.assign({}, x); }) }); render(); }
function hrEditSchedDel(i){ if(HR.edit.sched_hist.length > 1){ HR.edit.sched_hist.splice(i, 1); render(); } }
function hrEditPayAdd(){ var h = HR.edit.pay_hist, last = h[h.length - 1]; h.push({ from: monthStr(new Date(Date.now() + 32 * 864e5)) + "-01", pay:last.pay }); render(); }
function hrEditPayDel(i){ if(HR.edit.pay_hist.length > 1){ HR.edit.pay_hist.splice(i, 1); render(); } }
async function hrStaffSave(){
  var e = HR.edit; if(!e) return;
  if(!(e.name || "").trim() && !(e.nick || "").trim()){ await uiAlert("이름이나 별칭을 적어 주세요", "", "warn"); return; }
  var sh = e.sched_hist.map(function(x){ return { from:x.from || "", days:x.days, spans:x.spans.filter(function(sp){ return sp.start && sp.end; }).map(function(sp){ return {start:sp.start, end:sp.end, break:Number(sp.break || 0)}; }) }; }).sort(function(a, b){ return a.from.localeCompare(b.from); });
  var ph = e.pay_hist.map(function(x){ return { from:x.from || "", pay:Number(x.pay || 0) }; }).sort(function(a, b){ return a.from.localeCompare(b.from); });
  var cur = sh[sh.length - 1], sp0 = cur.spans[0] || {start:"10:00", end:"22:00", break:0};
  var row = { id:e.id, store:view.storeKey || "hanok", name:(e.name || "").trim() || (e.nick || "").trim(), nick:(e.nick || "").trim(), role:(e.role || "").trim(), phone:phoneNorm(e.phone || ""),
              pay_type:e.pay_type || "hourly", pay:ph[ph.length - 1].pay, pay_hist:ph, tax:e.tax || "4대보험", weekly_pay:e.weekly_pay !== false, absent_deduct:!!e.absent_deduct,
              sched:{ days:cur.days, start:sp0.start, end:sp0.end, break:sp0.break, spans:cur.spans }, sched_hist:sh,
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
  if(!goOn && !await uiConfirm("퇴사 처리할까요?", hrLabel(e) + " 님이 주간표에서 빠집니다(급여에는 퇴사한 달까지 남음). 다시 '재직' 으로 되돌릴 수 있습니다.", {ok:"퇴사 처리", cancel:"취소"})) return;
  e.active = goOn; if(!goOn && !e.end_date) e.end_date = todayStr(); if(goOn) e.end_date = null;
  await hrStaffSave();
}
async function hrShowSeverance(){ var e = HR.edit; if(!e) return; e.sev = { loading:true }; render(); e.sev = await hrSeverance(e) || { none:true }; render(); }
function hrSetupOpen(){ HR.setup = deepClone(Object.assign({}, HR_DEF, HR.cfg || {})); HR.setup.rates = Object.assign({}, HR_DEF.rates, (HR.cfg || {}).rates || {}); render(); }
async function hrSetupSave(){
  var d = HR.setup; if(!d) return;
  try{
    await sb("/rest/v1/hr_settings?on_conflict=store", { method:"POST", body:{ store:view.storeKey || "hanok", data:d }, prefer:"resolution=merge-duplicates,return=minimal" });
    HR.cfg = d; HR.setup = null; logEvent("워크시프트 설정", (d.over5 ? "5인 이상" : "5인 미만")); render();
  }catch(e){ await uiAlert("저장 실패", e.message || String(e), "warn"); }
}

/* ---------- 화면 ---------- */
function hrGroups(list){
  var g = {}; list.forEach(function(s){ var r = hrRole(s); (g[r] = g[r] || []).push(s); });
  var keys = HR_ROLES.filter(function(r){ return g[r]; }).concat(Object.keys(g).filter(function(r){ return HR_ROLES.indexOf(r) < 0; }).sort());
  return keys.map(function(r){ return { role:r, list:g[r] }; });
}
function sheetStaff(){
  if(!HR || HR.loading) return '<p class="muted" style="padding:20px 0">불러오는 중…</p>';
  if(HR.err) return '<div class="alert rust"><span class="ic">!</span><div><div class="a-t">불러오지 못했습니다</div><div class="a-s">' + esc(HR.err) + '</div></div></div><div class="btn-row" style="margin-top:12px"><button class="btn" onclick="HR.loading=true; render(); hrLoad().then(render)">다시 시도</button></div>';
  var top = '<div class="hr-top"><div class="seg"><button class="' + (HR.view === "week" ? "on" : "") + '" onclick="HR.view=\'week\'; render()">주간표</button><button class="' + (HR.view === "pay" ? "on" : "") + '" onclick="HR.view=\'pay\'; render()">급여</button></div>' +
      '<div class="btn-row">' + (HR.view === "week" ? '<button class="btn sm ' + (HR.retired ? "" : "ghost") + '" onclick="HR.retired=!HR.retired; render()">' + (HR.retired ? "재직자 보기" : "퇴사자 보기") + '</button>' : '') +
      '<button class="btn sm ghost" onclick="hrSetupOpen()">설정</button><button class="btn sm primary" onclick="hrStaffNew()">＋ 직원</button></div></div>';
  var body = !HR.staff.length ? '<div class="empty">직원이 없습니다. "＋ 직원" 으로 첫 사람을 넣고 정규 근무(요일·시간)를 정해 두면, 칸을 눌러 ○ 만 찍으면 됩니다.</div>'
           : HR.view === "pay" ? hrPayView() : hrWeekView();
  return top + body + (HR.pop ? hrPopHtml() : "") + (HR.edit ? hrEditHtml() : "") + (HR.slip ? hrSlipHtml() : "") + (HR.setup ? hrSetupHtml() : "");
}
/* 기간 옮기기(재아 09-20): 화살표 말고도 날짜를 바로 골라 뛸 수 있게 — 제목 옆 달력 입력 */
async function hrJumpWeek(v){ if(!v) return; HR.week = hrWeekStart(v); HR.loading = true; render(); await hrLoadRange(); HR.loading = false; render(); }
async function hrJumpMonth(v){ if(!/^\d{4}-\d{2}$/.test(v || "")) return; HR.month = v; HR.loading = true; render(); await hrLoadRange(); HR.loading = false; render(); }
function hrPeriodHead(title, sub, onPrev, onToday, onNext, isNow){
  var pick = HR.view === "pay"
    ? '<input type="month" class="hr-jump" value="' + esc(HR.month) + '" onchange="hrJumpMonth(this.value)" title="달 바로 가기">'
    : '<input type="date" class="hr-jump" value="' + esc(HR.week) + '" onchange="hrJumpWeek(this.value)" title="그 날짜가 든 주로 가기">';
  return '<div class="hr-period"><div class="hr-period-t"><b>' + title + '</b>' + (sub ? '<small>' + sub + '</small>' : '') + '</div>' + pick +
    '<div class="hr-period-nav">' + (isNow ? '' : '<button class="btn sm ghost" onclick="' + onToday + '">' + (HR.view === "pay" ? "이번 달" : "이번 주") + '</button>') + '<button class="bnav" onclick="' + onPrev + '" aria-label="이전">&lsaquo;</button><button class="bnav" onclick="' + onNext + '" aria-label="다음">&rsaquo;</button></div></div>';
}
function hrWeekView(){
  var days = hrWeekDays(HR.week), today = todayStr(), cfg = hrCfg();
  var list = HR.staff.filter(function(s){ return HR.retired ? s.active === false : s.active !== false; });
  if(HR.retired) list.sort(function(a, b){ return (b.end_date || "").localeCompare(a.end_date || ""); });
  var w0 = new Date(days[0] + "T00:00:00"), w6 = new Date(days[6] + "T00:00:00");
  var head = hrPeriodHead(hrWeekLabel(HR.week), (w0.getMonth() + 1) + "월 " + w0.getDate() + "일 – " + (w6.getMonth() + 1) + "월 " + w6.getDate() + "일", "hrMoveWeek(-1)", "hrMoveWeek(0)", "hrMoveWeek(1)", HR.week === hrWeekStart(today));
  var ths = days.map(function(d){ var dt = new Date(d + "T00:00:00"), dow = dt.getDay(), hol = isHoliday(d);
    return '<th class="hd ' + (d === today ? "today " : "") + (dow === 0 || hol ? "sun" : dow === 6 ? "sat" : "") + '" onclick="hrDayClick(\'' + d + '\')" title="누르면 공휴일 지정/해제"><b>' + dt.getDate() + '</b><small>' + HR_DAYS[dow] + (hol && dow !== 0 ? ' · 공휴' : '') + '</small></th>'; }).join("");
  var rowHtml = function(s){
    var wk = hrWeekCalc(s, HR.week);
    var tds = days.map(function(d){
      var a = HR.att[s.id + "|" + d], duty = hrOnDuty(s, d), past = d <= today, sps = hrSpans(s, a), h = sps.reduce(function(x, sp){ return x + sp.hours; }, 0);
      /* 안 찍은 정규 근무일: 지난 날은 빨간 '정규', 오늘 이후는 검정 '정규' — 빗금은 화려하다는 평(재아 09-20)이라 글자만 */
      var cls = "hc" + (a ? " " + ({"정규":"reg","변형":"alt","결근":"abs","휴무":"off"}[a.status]) : (duty ? (past ? " due" : " due-future") : "")) + (d === today ? " today" : "");
      var sub = sps.length ? hrRound(h) + "h" : (a ? "" : (duty ? "정규" : ""));
      return '<td class="' + cls + '" onclick="hrCell(\'' + s.id + '\',\'' + d + '\')"><span class="m">' + (a ? HR_STATUS[a.status] : "") + '</span><small>' + esc(sub) + '</small>' +
        (a && Number(a.rate) > 1 ? '<i class="r">' + a.rate + 'x</i>' : '') + (a && a.memo ? '<i class="dot" title="' + esc(a.memo) + '"></i>' : '') + '</td>';
    }).join("");
    return '<tr' + (s.active === false ? ' class="gone"' : '') + '><th class="hr-name"><button class="hr-nm" onclick="hrStaffEdit(\'' + s.id + '\')"><b>' + esc(hrLabel(s)) + '</b><small>' + esc(s.nick && s.name !== s.nick ? s.name + " · " : "") + esc(s.role || "") + (s.active === false && s.end_date ? " · " + s.end_date.slice(5).replace("-", "/") + " 퇴사" : "") + '</small></button></th>' + tds +
      /* 줄마다 하나씩(연장·야간·주휴·결근) — 한 줄에 '·' 로 이으면 좁은 칸에서 낱말 중간이 잘려 깨져 보였음(재아 09-20) */
      '<td class="hr-sum"><b>' + hrRound(wk.hours) + 'h</b><small>' + wk.days + '일 근무</small>' + (wk.ot ? '<small>연장 ' + hrRound(wk.ot) + 'h</small>' : '') + (wk.night ? '<small>야간 ' + hrRound(wk.night) + 'h</small>' : '') + (wk.weeklyPay ? '<small>주휴 ' + hrRound(wk.weeklyPay) + 'h</small>' : '') + (wk.absent ? '<small class="rust">결근 ' + wk.absent + '</small>' : '') + '</td></tr>';
  };
  var trs = hrGroups(list).map(function(g){ return '<tr class="hr-grp"><th class="hr-name">' + esc(g.role) + '</th><td colspan="8"></td></tr>' + g.list.map(rowHtml).join(""); }).join("");
  if(!list.length) trs = '<tr><td colspan="9" class="empty">' + (HR.retired ? "퇴사한 직원이 없습니다." : "재직 중인 직원이 없습니다.") + '</td></tr>';
  return head + '<div class="hr-scroll"><table class="hr-grid week"><thead><tr><th class="hr-name"></th>' + ths + '<th class="hr-sum">이번 주</th></tr></thead><tbody>' + trs + '</tbody></table></div>' +
    '<div class="hr-legend"><span><i class="hc reg">○</i>정규</span><span><i class="hc alt">△</i>다른 시간</span><span><i class="hc abs">×</i>결근</span><span><i class="hc off">–</i>휴무</span><span><i class="hc due">정규</i>안 찍은 근무일(지난 날은 빨강)</span><span><i class="r-ex">1.5x</i>배율(휴일 등)</span><span><i class="dot-ex"></i>메모</span></div>' +
    '<p class="f-note">칸을 누르면 찍습니다(안 찍힌 칸은 상태를 골라야 저장). 이름을 누르면 정규 근무·시급을 기간별로 고칩니다. 날짜를 누르면 공휴일 지정/해제. ' +
      hrOver5Note(HR.week.slice(0, 7)) + '</p>';
}
function hrPayView(){
  var m = HR.month, mx = new Date(m + "-01T00:00:00"), title = mx.getFullYear() + "년 " + (mx.getMonth() + 1) + "월";
  var last = hrMonthEnd(m), list = HR.staff.filter(function(s){ return s.active !== false || !s.end_date || s.end_date >= m + "-01"; });   /* 퇴사자도 퇴사한 달까지 */
  var head = hrPeriodHead(title, "급여", "hrMoveMonth(-1)", "hrMoveMonth(0)", "hrMoveMonth(1)", m === monthStr());
  var tot = { gross:0, ded:0, net:0, employer:0 };
  var rowHtml = function(s){
    var t = hrCalc(s, m); tot.gross += t.gross; tot.ded += t.dedTotal; tot.net += t.net; tot.employer += t.employer;
    var extra = [];
    if(t.ot) extra.push("연장 " + t.ot + "h"); if(t.night) extra.push("야간 " + t.night + "h"); if(t.weekly) extra.push("주휴 " + t.weekly + "h"); if(t.bonusH) extra.push("가산 " + t.bonusH + "h");
    return '<tr' + (s.active === false ? ' class="gone"' : '') + '><td class="nm"><button class="hr-nm" onclick="hrStaffEdit(\'' + s.id + '\')"><b>' + esc(hrLabel(s)) + '</b><small>' + esc(s.nick && s.name !== s.nick ? s.name + " · " : "") + esc(s.role || "") + (s.active === false ? " · 퇴사" : "") + '</small></button></td>' +
      '<td class="won"><small>' + (s.pay_type === "monthly" ? "월급" : "시급") + '</small>' + hrWon(hrPayAt(s, last)) + '</td><td>' + t.days + '일' + (t.abs ? '<small class="rust">결근 ' + t.abs + '</small>' : '') + '</td><td>' + t.hours + 'h' + (extra.length ? '<small>' + extra.join(" · ") + '</small>' : '') + '</td>' +
      '<td class="won">' + hrWon(t.gross) + '</td><td class="won">' + (t.dedTotal ? '−' + hrWon(t.dedTotal) + '<small>' + esc(s.tax || "4대보험") + '</small>' : '<small class="muted">공제 없음</small>') + '</td><td class="won"><b>' + hrWon(t.net) + '</b></td>' +
      '<td><button class="btn sm" onclick="HR.slip={id:\'' + s.id + '\', month:\'' + m + '\'}; render()">계산서</button></td></tr>';
  };
  var trs = hrGroups(list).map(function(g){ return '<tr class="hr-grp"><td colspan="8">' + esc(g.role) + '</td></tr>' + g.list.map(rowHtml).join(""); }).join("");
  return head + '<div class="card" style="padding:0; overflow:auto"><table class="hr-pay"><thead><tr><th>직원</th><th>시급·월급</th><th>근무</th><th>시간</th><th>총지급</th><th>공제</th><th>실지급</th><th></th></tr></thead><tbody>' + trs +
    '<tr class="tot"><td colspan="4">합계</td><td class="won">' + hrWon(tot.gross) + '</td><td class="won">−' + hrWon(tot.ded) + '</td><td class="won"><b>' + hrWon(tot.net) + '</b></td><td></td></tr></tbody></table></div>' +
    '<p class="f-note">총지급 = 기본급 + 연장·야간 가산(5인 이상) + 주휴수당(시급제, 주 15h 이상 개근) + 배율 가산. 월급제는 월급 고정 + 가산(통상시급 = 월급 ÷ 209), 결근 공제는 직원마다 켬. 공제 = 4대보험(근로자분) 또는 3.3%. 사업주 부담 4대보험(산재 제외) 약 ' + hrWon(tot.employer) + '. 퇴사자는 퇴사한 달까지 회색으로. <b>참고용 계산</b> — 신고·정산은 세무사/노무사 확인 후.</p>';
}
/* ---------- 급여계산서: 영수증 모양 (재아 09-19 "직원한테 보내기 안 민망하게") ----------
   hrSlipData 가 줄 목록을 만들고, 화면(HTML)·인쇄·사진 저장(캔버스)이 같은 줄을 씁니다 — 셋이 늘 같게 */
function hrSlipData(s, m){
  var mx = new Date(m + "-01T00:00:00"), title = mx.getFullYear() + "년 " + (mx.getMonth() + 1) + "월", t = hrCalc(s, m), cfg = hrCfg();
  var st = store(), shop = (st && st.name) || "한옥반점";
  var L = [];   /* {k:"h1|sub|sec|row|tot|note|log|dash", a, b, n} */
  L.push({k:"h1", a:shop}); L.push({k:"sub", a:title + " 급여계산서"});
  L.push({k:"dash"});
  L.push({k:"row", a:"직원", b:hrLabel(s) + (s.nick && s.name !== s.nick ? " (" + s.name + ")" : "") + (s.role ? " · " + s.role : "")});
  L.push({k:"row", a:"기준", b:(s.pay_type === "monthly" ? "월급제 · 통상시급 " + hrWon(t.wage) : "시급 " + hrWon(t.wage)) + " · " + (s.tax || "4대보험")});
  L.push({k:"row", a:"근무", b:t.days + "일 · " + t.hours + "시간" + (t.abs ? " · 결근 " + t.abs + "일" : "")});
  L.push({k:"dash"}); L.push({k:"sec", a:"지급"});
  L.push({k:"row", a:s.pay_type === "monthly" ? "월급" : "기본급", b:hrWon(t.base), n:s.pay_type === "monthly" ? "" : t.hours + "h × " + hrWon(t.wage)});
  if(t.extraPay) L.push({k:"row", a:"정규 외 근무", b:hrWon(t.extraPay), n:t.extraH + "h × " + hrWon(t.wage)});
  if(t.otPay) L.push({k:"row", a:"연장수당", b:hrWon(t.otPay), n:t.ot + "h × 0.5"});
  if(t.nightPay) L.push({k:"row", a:"야간수당", b:hrWon(t.nightPay), n:t.night + "h × 0.5"});
  if(t.weeklyPay) L.push({k:"row", a:"주휴수당", b:hrWon(t.weeklyPay), n:t.weekly + "h"});
  if(t.bonusPay) L.push({k:"row", a:"휴일·배율 가산", b:hrWon(t.bonusPay), n:t.bonusH + "h"});
  if(t.absentPay) L.push({k:"row", a:"결근 공제", b:hrWon(t.absentPay), n:t.abs + "일 × 8h"});
  L.push({k:"tot", a:"총지급", b:hrWon(t.gross)});
  L.push({k:"sec", a:"공제 · " + (s.tax || "4대보험")});
  if(Object.keys(t.ded).length) Object.keys(t.ded).forEach(function(k){ L.push({k:"row", a:k, b:"−" + hrWon(t.ded[k])}); }); else L.push({k:"row", a:"공제 없음", b:"0원"});
  L.push({k:"tot", a:"실지급액", b:hrWon(t.net), big:true});
  L.push({k:"dash"}); L.push({k:"sec", a:"근무 기록 " + t.log.length + "일"});
  t.log.forEach(function(l){ var dt = new Date(l.date + "T00:00:00"); L.push({k:"log", a:(dt.getMonth() + 1) + "/" + dt.getDate() + "(" + HR_DAYS[dt.getDay()] + ")", b:HR_STATUS[l.status] + " " + (l.spans.length ? l.spans.map(function(sp){ return minToHM(sp.s0) + "-" + minToHM(sp.e0 % 1440); }).join("+") + " " + hrRound(l.hours) + "h" : l.status) + (l.rate > 1 ? " " + l.rate + "x" : ""), n:l.memo || ""}); });
  L.push({k:"dash"});
  L.push({k:"note", a:"발행 " + todayStr() + " · " + shop});
  L.push({k:"note", a:"참고용 계산서 — 소득세(간이세액)·비과세·수습 감액은 넣지 않았습니다"});
  return { lines:L, title:title, t:t, cfg:cfg, shop:shop };
}
function hrSlipHtml(){
  var s = HR.staff.find(function(x){ return x.id === HR.slip.id; }); if(!s) return "";
  var d = hrSlipData(s, HR.slip.month);
  var html = d.lines.map(function(l){
    if(l.k === "h1") return '<div class="rc-h1">' + esc(l.a) + '</div>';
    if(l.k === "sub") return '<div class="rc-sub">' + esc(l.a) + '</div>';
    if(l.k === "dash") return '<div class="rc-dash"></div>';
    if(l.k === "sec") return '<div class="rc-sec">' + esc(l.a) + '</div>';
    if(l.k === "note") return '<div class="rc-note">' + esc(l.a) + '</div>';
    if(l.k === "tot") return '<div class="rc-row rc-tot' + (l.big ? ' big' : '') + '"><span>' + esc(l.a) + '</span><b>' + esc(l.b) + '</b></div>';
    if(l.k === "log") return '<div class="rc-row rc-log"><span>' + esc(l.a) + '</span><span class="g">' + esc(l.b) + '</span>' + (l.n ? '<small>' + esc(l.n) + '</small>' : '') + '</div>';
    return '<div class="rc-row"><span>' + esc(l.a) + (l.n ? '<small>' + esc(l.n) + '</small>' : '') + '</span><b>' + esc(l.b) + '</b></div>';
  }).join("");
  var text = d.lines.map(function(l){ return l.k === "dash" ? "-----------------------------" : l.k === "log" ? l.a + " " + l.b + (l.n ? " · " + l.n : "") : (l.a || "") + (l.b ? "  " + l.b : "") + (l.n ? " (" + l.n + ")" : ""); }).join("\n");
  return '<div class="overlay" onclick="HR.slip=null; render()"><div class="sheet sheet-tall" onclick="event.stopPropagation()">' + sheetHead("급여계산서") +
    '<div class="searchbox rc-wrap"><div class="receipt">' + html + '</div></div>' +
    '<div class="sheet-actions"><button class="btn ghost" onclick="hrSlipImage()">사진으로 저장</button><button class="btn ghost" onclick="navigator.clipboard&&navigator.clipboard.writeText(' + JSON.stringify(text).replace(/"/g, "&quot;") + ').then(function(){ showToast(\'복사했습니다\'); })">글로 복사</button><button class="btn ghost" onclick="hrPrintSlip()">인쇄</button><button class="btn primary" onclick="HR.slip=null; render()">닫기</button></div></div></div>';
}
function hrPrintSlip(){
  var el = document.querySelector(".receipt"); if(!el) return;
  var w = window.open("", "_blank"); if(!w){ uiAlert("팝업이 막혀 있습니다", "브라우저에서 팝업을 허용해 주세요.", "warn"); return; }
  var css = ""; try{ css = Array.prototype.slice.call(document.styleSheets).map(function(ss){ try{ return Array.prototype.slice.call(ss.cssRules).filter(function(r){ return /\.rc-|\.receipt/.test(r.cssText); }).map(function(r){ return r.cssText; }).join("\n"); }catch(e){ return ""; } }).join("\n"); }catch(e){}
  w.document.write('<!doctype html><meta charset="utf-8"><title>급여계산서</title><style>' + css + ' body{background:#fff; margin:0; padding:20px; display:flex; justify-content:center; font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",sans-serif} .receipt{box-shadow:none}</style><div class="receipt">' + el.innerHTML + '</div>');
  w.document.close(); w.focus(); setTimeout(function(){ w.print(); }, 300);
}
/* 사진으로 저장: 캔버스에 같은 줄을 그려 PNG 로. 폰·태블릿이면 공유 시트(카톡으로 바로), 아니면 내려받기 */
async function hrSlipImage(){
  var s = HR.staff.find(function(x){ return x.id === HR.slip.id; }); if(!s) return;
  var d = hrSlipData(s, HR.slip.month), W = 720, P = 44, y = 0, scale = 2;
  var c = document.createElement("canvas"), g = c.getContext("2d");
  var F = '"Pretendard","Apple SD Gothic Neo","Malgun Gothic",sans-serif';
  var hOf = function(l){ return l.k === "h1" ? 48 : l.k === "sub" ? 30 : l.k === "dash" ? 22 : l.k === "sec" ? 30 : l.k === "note" ? 22 : (l.k === "tot" && l.big) ? 56 : l.k === "tot" ? 36 : l.k === "log" ? (l.n ? 44 : 26) : (l.n ? 42 : 28); };
  var heights = d.lines.reduce(function(a, l){ return a + hOf(l); }, 0);
  c.width = W * scale; c.height = (heights + P * 2 + 20) * scale; g.scale(scale, scale);
  g.fillStyle = "#fff"; g.fillRect(0, 0, W, heights + P * 2 + 20); g.fillStyle = "#1B1A18"; g.textBaseline = "top";
  y = P;
  var right = function(txt, yy, font){ g.font = font; g.textAlign = "right"; g.fillText(txt, W - P, yy); g.textAlign = "left"; };
  var dash = function(yy){ g.save(); g.strokeStyle = "#999"; g.setLineDash([4, 4]); g.beginPath(); g.moveTo(P, yy); g.lineTo(W - P, yy); g.stroke(); g.restore(); };
  d.lines.forEach(function(l){
    if(l.k === "h1"){ g.font = "800 30px " + F; g.textAlign = "center"; g.fillText(l.a.split("").join(" "), W / 2, y); g.textAlign = "left"; }
    else if(l.k === "sub"){ g.font = "16px " + F; g.fillStyle = "#555"; g.textAlign = "center"; g.fillText(l.a, W / 2, y); g.textAlign = "left"; g.fillStyle = "#1B1A18"; }
    else if(l.k === "dash"){ dash(y + 10); }
    else if(l.k === "sec"){ g.font = "700 16px " + F; g.fillStyle = "#555"; g.fillText(l.a, P, y + 8); g.fillStyle = "#1B1A18"; }
    else if(l.k === "note"){ g.font = "13px " + F; g.fillStyle = "#888"; g.textAlign = "center"; g.fillText(l.a, W / 2, y + 4); g.textAlign = "left"; g.fillStyle = "#1B1A18"; }
    else if(l.k === "tot"){ g.save(); g.strokeStyle = "#333"; g.beginPath(); g.moveTo(P, y + 2); g.lineTo(W - P, y + 2); g.stroke(); g.restore(); var big = !!l.big;
      g.font = (big ? "800 22px " : "700 17px ") + F; g.fillText(l.a, P, y + (big ? 14 : 10)); right(l.b, y + (big ? 12 : 10), (big ? "800 28px " : "800 18px ") + F); }
    else if(l.k === "log"){ g.font = "14px " + F; g.fillStyle = "#555"; g.fillText(l.a, P, y + 4); g.fillStyle = "#1B1A18"; g.fillText(l.b, P + 84, y + 4); if(l.n){ g.font = "12px " + F; g.fillStyle = "#888"; g.fillText("· " + l.n, P + 84, y + 24); g.fillStyle = "#1B1A18"; } }
    else { g.font = "16px " + F; g.fillText(l.a, P, y + 4); right(l.b, y + 4, "600 16px " + F); if(l.n){ g.font = "12px " + F; g.fillStyle = "#888"; g.fillText(l.n, P, y + 25); g.fillStyle = "#1B1A18"; } }
    y += hOf(l);
  });
  var name = d.title.replace(/\s/g, "") + "_급여계산서_" + hrLabel(s) + ".png";
  c.toBlob(async function(blob){
    if(!blob){ uiAlert("사진을 만들지 못했습니다", "", "warn"); return; }
    try{
      var file = new File([blob], name, {type:"image/png"});
      if(navigator.canShare && navigator.canShare({files:[file]})){ await navigator.share({files:[file], title:name}); return; }   /* 폰·태블릿: 카톡 등으로 바로 */
    }catch(e){ if(e && e.name === "AbortError") return; }
    var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 2000);
    showToast("사진으로 저장했습니다 · " + name);
  }, "image/png");
}
function hrPopHtml(){
  var p = HR.pop, s = HR.staff.find(function(x){ return x.id === p.staff_id; }) || {};
  var seg = function(k, v, label){ return '<button class="' + (p[k] == v ? "on" : "") + '" onclick="hrPopSet(\'' + k + '\',' + JSON.stringify(v) + ')">' + label + '</button>'; };
  var spans = (p.spans || []).map(function(sp, i){ return '<div class="grid3 hr-spanrow"><label class="f"><div class="lb">시작</div><input type="time" value="' + esc(sp.start || "") + '" onchange="hrPopSpan(' + i + ',\'start\', this.value)"></label>' +
      '<label class="f"><div class="lb">종료</div><input type="time" value="' + esc(sp.end || "") + '" onchange="hrPopSpan(' + i + ',\'end\', this.value)"></label>' +
      '<label class="f"><div class="lb">휴게(분)' + (p.spans.length > 1 ? ' <button class="btn sm ghost" style="float:right; padding:0 6px; min-height:0" onclick="hrPopSpanDel(' + i + ')">×</button>' : '') + '</div><input type="number" min="0" step="10" value="' + Number(sp.break || 0) + '" oninput="hrPopSpan(' + i + ',\'break\', this.value)"></label></div>'; }).join("");
  return '<div class="overlay" onclick="HR.pop=null; render()"><div class="sheet" onclick="event.stopPropagation()">' +
    sheetHead(esc(hrLabel(s)) + ' · ' + dateLabel(p.date)) +
    '<p class="f-note" style="margin:-6px 0 12px">정규 근무: ' + esc(hrSchedText(s, p.date)) + '</p>' +
    '<div class="seg hr-seg">' + seg("status", "정규", "○ 정규") + seg("status", "변형", "△ 다른 시간") + seg("status", "결근", "× 결근") + seg("status", "휴무", "– 휴무") + '</div>' +
    (p.status === "변형" ? '<div style="margin-top:12px">' + spans + (p.spans.length < 2 ? '<button class="btn sm ghost" onclick="hrPopSpanAdd()">＋ 타임 추가 (점심·저녁 따로)</button>' : '') + '</div>' : '') +
    (p.status === "정규" || p.status === "변형" ? '<div class="f" style="margin-top:12px"><div class="lb">배율 <span class="lbl-note">휴일 근무 같은 때(연장·야간은 자동)</span></div><div class="seg">' + seg("rate", 1, "1x") + seg("rate", 1.5, "1.5x") + seg("rate", 2, "2x") + '</div></div>' : '') +
    '<label class="f" style="margin-top:12px"><div class="lb">메모 <span class="lbl-note">선택</span></div><input type="text" value="' + esc(p.memo || "") + '" placeholder="예: 늦게 옴, 행사 지원" oninput="hrPopSet(\'memo\', this.value)"></label>' +
    '<div class="sheet-actions">' + (p._new ? '' : '<button class="btn ghost danger" onclick="hrPopDel()">지우기</button>') + '<button class="btn ghost" onclick="HR.pop=null; render()">취소</button><button class="btn primary" data-enter onclick="hrPopSave()">저장</button></div></div></div>';
}
function hrEditHtml(){
  var e = HR.edit;
  var segv = function(k, v, label){ return '<button class="' + (e[k] === v ? "on" : "") + '" onclick="hrEditSet(\'' + k + '\',' + JSON.stringify(v) + '); render()">' + label + '</button>'; };
  var tab = function(k, label){ return '<button class="' + (e.tab === k ? "on" : "") + '" onclick="HR.edit.tab=\'' + k + '\'; render()">' + label + '</button>'; };
  var body = "";
  if(e.tab === "sched"){
    body = e.sched_hist.map(function(h, i){
      var days = HR_DAYS.map(function(d, j){ return '<button class="' + (h.days[j] ? "on" : "") + '" onclick="hrEditDay(' + i + ',' + j + ')">' + d + '</button>'; }).join("");
      var spans = h.spans.map(function(sp, j){ return '<div class="grid3 hr-spanrow"><label class="f"><div class="lb">시작</div><input type="time" value="' + esc(sp.start) + '" onchange="hrEditSpan(' + i + ',' + j + ',\'start\',this.value)"></label><label class="f"><div class="lb">종료</div><input type="time" value="' + esc(sp.end) + '" onchange="hrEditSpan(' + i + ',' + j + ',\'end\',this.value)"></label><label class="f"><div class="lb">휴게(분)' + (h.spans.length > 1 ? ' <button class="btn sm ghost" style="float:right; padding:0 6px; min-height:0" onclick="hrEditSpanDel(' + i + ',' + j + ')">×</button>' : '') + '</div><input type="number" min="0" step="10" value="' + Number(sp.break || 0) + '" oninput="hrEditSpan(' + i + ',' + j + ',\'break\',this.value)"></label></div>'; }).join("");
      return '<div class="hr-hist"><div class="hr-hist-h"><label class="f" style="margin:0"><div class="lb">' + (i === 0 && !h.from ? "처음부터" : "적용 시작일") + '</div>' + (i === 0 && !h.from ? '<span class="muted">입사 때부터</span>' : '<input type="date" value="' + esc(h.from) + '" onchange="HR.edit.sched_hist[' + i + '].from=this.value">') + '</label>' + (e.sched_hist.length > 1 ? '<button class="btn sm ghost" onclick="hrEditSchedDel(' + i + ')">이 기간 삭제</button>' : '') + '</div>' +
        '<div class="f"><div class="lb">근무 요일</div><div class="seg hr-days">' + days + '</div></div>' + spans + (h.spans.length < 2 ? '<button class="btn sm ghost" onclick="hrEditSpanAdd(' + i + ')">＋ 타임 추가 (하루 두 타임)</button>' : '') + '</div>';
    }).join("") + '<div class="btn-row"><button class="btn sm" onclick="hrEditSchedAdd()">＋ 다른 기간의 근무 시간</button></div><p class="f-note">근무 시간이 바뀌면 "다른 기간" 으로 추가하고 시작일을 적으세요 — 그 전 날짜는 옛 시간표로 계산됩니다.</p>';
  }else if(e.tab === "pay"){
    body = '<div class="grid2"><div class="f"><div class="lb">급여 방식</div><div class="seg">' + segv("pay_type", "hourly", "시급") + segv("pay_type", "monthly", "월급") + '</div></div>' +
      '<div class="f"><div class="lb">공제</div><div class="seg">' + segv("tax", "4대보험", "4대보험") + segv("tax", "3.3%", "3.3%") + segv("tax", "없음", "없음") + '</div></div></div>' +
      e.pay_hist.map(function(h, i){ return '<div class="grid2 hr-spanrow"><label class="f"><div class="lb">' + (i === 0 && !h.from ? "처음부터" : "적용 시작일") + '</div>' + (i === 0 && !h.from ? '<span class="muted" style="display:block; padding:10px 0">입사 때부터</span>' : '<input type="date" value="' + esc(h.from) + '" onchange="HR.edit.pay_hist[' + i + '].from=this.value">') + '</label><label class="f"><div class="lb">' + (e.pay_type === "monthly" ? "월급(원)" : "시급(원)") + (e.pay_hist.length > 1 ? ' <button class="btn sm ghost" style="float:right; padding:0 6px; min-height:0" onclick="hrEditPayDel(' + i + ')">×</button>' : '') + '</div><input type="number" min="0" step="100" value="' + Number(h.pay || 0) + '" oninput="HR.edit.pay_hist[' + i + '].pay=Number(this.value)"></label></div>'; }).join("") +
      '<div class="btn-row"><button class="btn sm" onclick="hrEditPayAdd()">＋ 시급 변경 (다음 달 1일부터)</button></div>' +
      (e.pay_type !== "monthly" ? '<div class="f"><div class="lb">주휴수당 <span class="lbl-note">주 15h 이상 개근이면 자동</span></div><div class="seg">' + segv("weekly_pay", true, "계산") + segv("weekly_pay", false, "안 함") + '</div></div>'
        : '<div class="f"><div class="lb">결근 공제 <span class="lbl-note">월급제 — 결근일 × 8h 일할 공제</span></div><div class="seg">' + segv("absent_deduct", true, "공제") + segv("absent_deduct", false, "안 함") + '</div></div>') +
      (e._new ? '' : '<div class="hr-sev"><div class="hr-sev-h"><b>퇴직금</b><button class="btn sm" onclick="hrShowSeverance()">계산</button></div>' +
        (e.sev ? (e.sev.loading ? '<p class="muted">계산 중…</p>' : e.sev.none ? '<p class="muted">입사일이 없어 계산할 수 없습니다.</p>' : !e.sev.ok ? '<p class="muted">근속 ' + e.sev.days + '일 — 1년(365일)이 되면 생깁니다.</p>' :
          '<div class="hr-sev-n">' + hrWon(e.sev.amount) + '</div><div class="hr-sev-s">근속 ' + e.sev.days + '일 (' + hrRound(e.sev.days / 365) + '년) · 최근 3개월(' + e.sev.months.join(", ") + ') 총지급 ' + hrWon(e.sev.sum) + ' → 하루 평균 ' + hrWon(e.sev.avgDay) + ' × 30일 × 근속년수 · 참고용</div>') : '<p class="muted">1년 이상 근속하면 최근 3개월 평균임금으로 추정합니다.</p>') + '</div>');
  }else{
    body = '<div class="grid2"><label class="f"><div class="lb">전화</div><input type="tel" value="' + esc(e.phone || "") + '" oninput="hrEditSet(\'phone\', this.value)"></label><label class="f"><div class="lb">역할 <span class="lbl-note">주방 · 홀 (표에서 묶임)</span></div><input type="text" value="' + esc(e.role || "") + '" oninput="hrEditSet(\'role\', this.value)"></label></div>' +
      '<div class="grid2"><label class="f"><div class="lb">입사일</div><input type="date" value="' + esc(e.start_date || "") + '" onchange="hrEditSet(\'start_date\', this.value)"></label><label class="f"><div class="lb">퇴사일 <span class="lbl-note">비우면 재직</span></div><input type="date" value="' + esc(e.end_date || "") + '" onchange="hrEditSet(\'end_date\', this.value || null)"></label></div>' +
      '<label class="f"><div class="lb">메모</div><input type="text" value="' + esc(e.memo || "") + '" oninput="hrEditSet(\'memo\', this.value)"></label>';
  }
  return '<div class="overlay" onclick="HR.edit=null; render()"><div class="sheet sheet-tall" onclick="event.stopPropagation()">' +
    sheetHead(e._new ? "직원 추가" : "직원") +
    '<div class="grid2"><label class="f"><div class="lb">별칭 <span class="lbl-note">화면에 먼저 보임</span></div><input type="text" value="' + esc(e.nick || "") + '" placeholder="예: 만두언니" oninput="hrEditSet(\'nick\', this.value)"></label>' +
    '<label class="f"><div class="lb">이름</div><input type="text" value="' + esc(e.name || "") + '" oninput="hrEditSet(\'name\', this.value)"></label></div>' +
    '<div class="seg" style="margin-bottom:12px">' + tab("sched", "정규 근무") + tab("pay", "급여·퇴직금") + tab("etc", "기타") + '</div>' +
    '<div class="searchbox" style="flex:1; min-height:0; overflow:auto">' + body + '</div>' +
    '<div class="sheet-actions">' + (e._new ? '' : '<button class="btn ghost ' + (e.active === false ? "" : "danger") + '" onclick="hrStaffRetire()">' + (e.active === false ? "재직으로" : "퇴사") + '</button>') +
    '<button class="btn ghost" onclick="HR.edit=null; render()">취소</button><button class="btn primary" data-enter onclick="hrStaffSave()">저장</button></div></div></div>';
}
function hrSetupHtml(){
  var d = HR.setup;
  var num = function(path, label, note){ var ks = path.split("."), v = ks.length === 2 ? d[ks[0]][ks[1]] : d[ks[0]]; return '<label class="f"><div class="lb">' + label + (note ? ' <span class="lbl-note">' + note + '</span>' : '') + '</div><input type="number" step="0.001" value="' + v + '" oninput="' + (ks.length === 2 ? 'HR.setup.' + ks[0] + '.' + ks[1] : 'HR.setup.' + ks[0]) + '=Number(this.value)"></label>'; };
  return '<div class="overlay" onclick="HR.setup=null; render()"><div class="sheet" onclick="event.stopPropagation()">' + sheetHead("워크시프트 설정") +
    '<div class="f"><div class="lb">사업장 규모 <span class="lbl-note">5인 이상이면 연장·야간·휴일 가산 의무</span></div><div class="seg"><button class="' + ((d.over5Mode || "auto") === "auto" ? "on" : "") + '" onclick="HR.setup.over5Mode=\'auto\'; render()">근태로 자동</button><button class="' + (d.over5Mode === "yes" ? "on" : "") + '" onclick="HR.setup.over5Mode=\'yes\'; HR.setup.over5=true; render()">5인 이상</button><button class="' + (d.over5Mode === "no" ? "on" : "") + '" onclick="HR.setup.over5Mode=\'no\'; HR.setup.over5=false; render()">5인 미만</button></div>' +
      '<div class="f-note">"그날 몇 명" 이 아니라 <b>한 달 평균</b>으로 봅니다(근로기준법 시행령 7조의2): 날마다 나온 사람 수를 더해 영업일로 나눈 값이 5 이상이면 5인 이상. 5인 미만인 날이 절반을 넘으면 미만, 반대면 이상. 자동이면 달마다 근태에서 계산합니다. ' + hrOver5Note(HR.month) + '</div></div>' +
    '<div class="f"><div class="lb">월급제 정규 외 근무 <span class="lbl-note">정규 시간을 넘긴 만큼 통상시급으로 따로 줌</span></div><div class="seg"><button class="' + (!d.inclusive ? "on" : "") + '" onclick="HR.setup.inclusive=false; render()">따로 계산</button><button class="' + (d.inclusive ? "on" : "") + '" onclick="HR.setup.inclusive=true; render()">월급에 포함(포괄)</button></div><div class="f-note">근로계약서에 "월급에 연장근로 ○시간 포함" 이라고 써 뒀으면(포괄임금) 포함으로. 아니면 따로 계산이 법대로입니다.</div></div>' +
    '<div class="f"><div class="lb">주휴수당 자동 계산</div><div class="seg"><button class="' + (d.weeklyPay !== false ? "on" : "") + '" onclick="HR.setup.weeklyPay=true; render()">켬</button><button class="' + (d.weeklyPay === false ? "on" : "") + '" onclick="HR.setup.weeklyPay=false; render()">끔</button></div></div>' +
    '<div class="subhead">4대보험 근로자 부담 요율(%) <span>매년 1월 바뀝니다 — 확인 후 고치세요</span></div>' +
    '<div class="grid2">' + num("rates.pension", "국민연금") + num("rates.health", "건강보험") + num("rates.care", "장기요양", "건강보험료의 %") + num("rates.employ", "고용보험") + '</div>' +
    '<div class="grid2">' + num("taxRate", "사업소득 원천징수(%)", "3.3 = 소득세 3 + 지방 0.3") + '<div class="f"><div class="lb">야간 시간대</div><div class="grid2"><input type="time" value="' + esc(d.night[0]) + '" onchange="HR.setup.night[0]=this.value"><input type="time" value="' + esc(d.night[1]) + '" onchange="HR.setup.night[1]=this.value"></div></div></div>' +
    '<div class="sheet-actions"><button class="btn ghost" onclick="HR.setup=null; render()">취소</button><button class="btn primary" onclick="hrSetupSave()">저장</button></div></div></div>';
}
function hrEsc(){ if(!HR || !(view.form && view.form.type === "staff")) return false; var k = ["pop","edit","slip","setup"].find(function(x){ return HR[x]; }); if(k){ HR[k] = null; render(); return true; } return false; }
