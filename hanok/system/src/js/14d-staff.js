/* ---------- 직원 근태 (staff · attendance, 15차) ----------
   사장님이 직접 체크하는 달력표. 화면형(view.form={type:"staff", page:true}) — 관리자 비밀번호 뒤.
   줄 = 직원, 칸 = 그 달의 날. 칸을 누르면 작은 창: 정규(○) / 다른 시간(△, 단축·연장·다른 타임) / 결근(×) / 휴무(–) + 배율(1.5배) + 메모.
   정규 = 그 직원의 '정규 근무'(요일·시작·종료·휴게)대로 나온 날. 시간은 정규 근무에서 자동으로 셉니다.
   급여: 시급제 = 시급 × (시간 × 배율 합) · 월급제 = 월급 그대로 + 참고 숫자(결근·변형). 복잡하게 안 갑니다(재아).
   서버 표: staff / attendance. 직원은 지우지 않고 '퇴사'(active=false). 근태 칸은 지울 수 있음. */
var HR = null;
var HR_STATUS = { "정규":"○", "변형":"△", "결근":"×", "휴무":"–" };
var HR_DAYS = ["일","월","화","수","목","금","토"];

async function openStaffPage(){
  if(!supaOn()){ await uiAlert("서버 설정이 없는 빌드입니다", "근태는 서버가 있어야 합니다.", "warn"); return; }
  if(!view.adminOk){ if(!await adminGate("직원 근태 열기")) return; view.adminOk = true; }
  view.form = {type:"staff", page:true};
  if(!HR) HR = { month: monthStr(), staff:[], att:{}, loading:true, pop:null, edit:null, pay:false };
  render(); await hrLoad(); render();
}
async function hrLoad(){
  var key = view.storeKey || "hanok", m = HR.month;
  var from = m + "-01", to = shiftDate(hrMonthEnd(m), 1);
  try{
    HR.staff = await sb("/rest/v1/staff?store=eq." + key + "&select=*&order=sort,name");
    var rows = await sb("/rest/v1/attendance?store=eq." + key + "&date=gte." + from + "&date=lt." + to + "&select=*");
    HR.att = {}; rows.forEach(function(a){ HR.att[a.staff_id + "|" + a.date] = a; });
    HR.err = null;
  }catch(e){ HR.err = e.message || String(e); }
  HR.loading = false;
}
function hrMonthEnd(m){ var d = new Date(m + "-01T00:00:00"); d.setMonth(d.getMonth() + 1); d.setDate(0); return m + "-" + pad(d.getDate()); }
function hrMonthDays(m){ var n = Number(hrMonthEnd(m).slice(8)), out = []; for(var i = 1; i <= n; i++) out.push(m + "-" + pad(i)); return out; }
async function hrMove(d){
  var x = new Date(HR.month + "-01T00:00:00"); x.setMonth(x.getMonth() + d);
  HR.month = monthStr(x); HR.loading = true; HR.scrolled = false; render(); await hrLoad(); render();
}
/* 정규 근무 시간표 읽기 — 없으면 요일 전부 쉼 */
function hrSched(s){ var x = s.sched || {}; return { days: x.days && x.days.length === 7 ? x.days : [false,false,false,false,false,false,false], start: x.start || "10:00", end: x.end || "22:00", brk: Number(x.break || 0) }; }
function hrSchedText(s){ var c = hrSched(s), ds = HR_DAYS.filter(function(_, i){ return c.days[i]; }); return ds.length ? ds.join("·") + " " + hm(c.start) + "~" + hm(c.end) + (c.brk ? " (휴게 " + c.brk + "분)" : "") : "정규 근무 없음"; }
function hrOnDuty(s, date){ var c = hrSched(s), dow = new Date(date + "T00:00:00").getDay(); if(!c.days[dow]) return false; if(s.start_date && date < s.start_date) return false; if(s.end_date && date > s.end_date) return false; return true; }
/* 한 칸의 근무 시간(시간 단위). 정규는 시간표, 변형은 적힌 시각 */
function hrHours(s, a){
  if(!a) return 0;
  if(a.status === "정규"){ var c = hrSched(s); return Math.max(0, (toMin(c.end) - toMin(c.start) - c.brk) / 60); }
  if(a.status === "변형" && a.start && a.end){ var mins = toMin(a.end) - toMin(a.start); if(mins < 0) mins += 24 * 60; return Math.max(0, (mins - (a.break_min || 0)) / 60); }
  return 0;
}
function hrRound(h){ return Math.round(h * 10) / 10; }
/* 한 달 합계 — 정규·변형 일수, 시간, 배율 적용 시간, 급여 */
function hrCalc(s, month){
  var t = { reg:0, alt:0, abs:0, off:0, hours:0, weighted:0, extra:0, pay:0, days:0 };
  hrMonthDays(month).forEach(function(d){
    var a = HR.att[s.id + "|" + d]; if(!a) return;
    if(a.status === "정규") t.reg++; else if(a.status === "변형") t.alt++; else if(a.status === "결근") t.abs++; else if(a.status === "휴무") t.off++;
    var h = hrHours(s, a), r = Number(a.rate || 1);
    t.hours += h; t.weighted += h * r; if(r > 1) t.extra += h;
  });
  t.days = t.reg + t.alt;
  t.pay = s.pay_type === "monthly" ? Number(s.pay || 0) : Math.round(Number(s.pay || 0) * t.weighted);
  t.hours = hrRound(t.hours); t.weighted = hrRound(t.weighted); t.extra = hrRound(t.extra);
  return t;
}
function hrWon(n){ return Number(n || 0).toLocaleString("ko-KR") + "원"; }

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

/* ---------- 직원 편집 ---------- */
function hrStaffNew(){ HR.edit = { id:newId("stf"), name:"", role:"", phone:"", pay_type:"hourly", pay:0, sched:{days:[false,true,true,true,true,true,true], start:"10:00", end:"22:00", break:60}, start_date:todayStr(), end_date:null, memo:"", active:true, sort:HR.staff.length, _new:true }; render(); }
function hrStaffEdit(id){ var s = HR.staff.find(function(x){ return x.id === id; }); if(!s) return; HR.edit = deepClone(s); HR.edit.sched = hrSchedRaw(HR.edit); render(); }
function hrSchedRaw(s){ var c = hrSched(s); return { days:c.days.slice(), start:c.start, end:c.end, break:c.brk }; }
function hrEditSet(k, v){ if(HR.edit) HR.edit[k] = v; }
function hrEditDay(i){ HR.edit.sched.days[i] = !HR.edit.sched.days[i]; render(); }
async function hrStaffSave(){
  var e = HR.edit; if(!e) return;
  if(!(e.name || "").trim()){ await uiAlert("이름을 적어 주세요", "", "warn"); return; }
  var row = { id:e.id, store:view.storeKey || "hanok", name:e.name.trim(), role:(e.role || "").trim(), phone:phoneNorm(e.phone || ""), pay_type:e.pay_type || "hourly", pay:Number(e.pay || 0),
              sched:{ days:e.sched.days, start:e.sched.start || "10:00", end:e.sched.end || "22:00", break:Number(e.sched.break || 0) },
              start_date:e.start_date || null, end_date:e.end_date || null, memo:(e.memo || "").trim(), active:e.active !== false, sort:Number(e.sort || 0) };
  try{
    await sb("/rest/v1/staff?on_conflict=id", { method:"POST", body:row, prefer:"resolution=merge-duplicates,return=minimal" });
    logEvent(e._new ? "직원 추가" : "직원 수정", row.name);
    HR.edit = null; HR.loading = true; render(); await hrLoad(); render();
  }catch(err){ await uiAlert("저장 실패", err.message || String(err), "warn"); }
}
async function hrStaffRetire(){
  var e = HR.edit; if(!e || e._new) return;
  var goOn = e.active === false;
  if(!goOn && !await uiConfirm("퇴사 처리할까요?", e.name + " 님이 표에서 빠집니다. 근태 기록은 남고, 다시 '재직' 으로 되돌릴 수 있습니다.", {ok:"퇴사 처리", cancel:"취소"})) return;
  e.active = goOn; if(!goOn && !e.end_date) e.end_date = todayStr(); if(goOn) e.end_date = null;
  await hrStaffSave();
}

/* ---------- 화면 ---------- */
function sheetStaff(){
  if(!HR || HR.loading) return '<p class="muted" style="padding:20px 0">불러오는 중…</p>';
  if(HR.err) return '<div class="alert rust"><span class="ic">!</span><div><div class="a-t">불러오지 못했습니다</div><div class="a-s">' + esc(HR.err) + '</div></div></div><div class="btn-row" style="margin-top:12px"><button class="btn" onclick="HR.loading=true; render(); hrLoad().then(render)">다시 시도</button></div>';
  var m = HR.month, days = hrMonthDays(m), today = todayStr();
  var list = HR.staff.filter(function(s){ return s.active !== false || HR.showRetired; });
  var mx = new Date(m + "-01T00:00:00");
  var head = '<div class="hr-top"><div class="hr-mon"><button class="bnav" onclick="hrMove(-1)">&lsaquo;</button><b>' + mx.getFullYear() + '년 ' + (mx.getMonth() + 1) + '월</b><button class="bnav" onclick="hrMove(1)">&rsaquo;</button>' +
      (m !== monthStr() ? '<button class="btn sm ghost" onclick="HR.month=monthStr(); HR.loading=true; render(); hrLoad().then(render)">이번 달</button>' : '') + '</div>' +
      '<div class="btn-row"><button class="btn sm ' + (HR.pay ? "" : "ghost") + '" onclick="HR.pay=!HR.pay; render()">' + (HR.pay ? "표로" : "정산") + '</button>' +
      '<button class="btn sm ghost" onclick="HR.showRetired=!HR.showRetired; render()">' + (HR.showRetired ? "퇴사자 숨기기" : "퇴사자 보기") + '</button>' +
      '<button class="btn sm primary" onclick="hrStaffNew()">＋ 직원</button></div></div>';
  var body;
  if(!list.length) body = '<div class="empty">직원이 없습니다. "＋ 직원" 으로 첫 사람을 넣고, 정규 근무(요일·시간)를 정해 두면 칸을 눌러 ○ 만 찍으면 됩니다.</div>';
  else if(HR.pay) body = hrPayTable(list, m);
  else{
    var ths = days.map(function(d){ var dt = new Date(d + "T00:00:00"), dow = dt.getDay(), hol = isHoliday(d);
      return '<th class="' + (d === today ? "today " : "") + (dow === 0 || hol ? "sun" : dow === 6 ? "sat" : "") + '"><b>' + Number(d.slice(8)) + '</b><small>' + HR_DAYS[dow] + '</small></th>'; }).join("");
    var trs = list.map(function(s){
      var t = hrCalc(s, m);
      var tds = days.map(function(d){
        var a = HR.att[s.id + "|" + d], duty = hrOnDuty(s, d), past = d <= today;
        var cls = "hc" + (a ? " " + ({"정규":"reg","변형":"alt","결근":"abs","휴무":"off"}[a.status]) : (duty && past ? " due" : "")) + (d === today ? " today" : "") + (s.active === false ? " gone" : "");
        var mark = a ? HR_STATUS[a.status] : "";
        var tip = a ? (a.status + (a.status === "변형" ? " " + hm(a.start) + "~" + hm(a.end) : "") + (Number(a.rate) > 1 ? " · " + a.rate + "배" : "") + (a.memo ? " · " + a.memo : "")) : (duty ? "정규 근무일 · 아직 안 찍음" : "");
        return '<td class="' + cls + '" title="' + esc(tip) + '" onclick="hrCell(\'' + s.id + '\',\'' + d + '\')"><span class="m">' + mark + '</span>' +
          (a && Number(a.rate) > 1 ? '<i class="r">' + a.rate + '</i>' : '') + (a && a.memo ? '<i class="dot"></i>' : '') + '</td>';
      }).join("");
      return '<tr' + (s.active === false ? ' class="gone"' : '') + '><th class="hr-name" onclick="hrStaffEdit(\'' + s.id + '\')"><b>' + esc(s.name) + '</b><small>' + esc(s.role || "") + (s.active === false ? " · 퇴사" : "") + '</small></th>' + tds +
        '<td class="hr-sum"><b>' + t.days + '일</b><small>' + t.hours + 'h' + (t.extra ? ' · 가산 ' + t.extra + 'h' : '') + '</small><small>' + hrWon(t.pay) + '</small></td></tr>';
    }).join("");
    body = '<div class="hr-scroll"><table class="hr-grid"><thead><tr><th class="hr-name"></th>' + ths + '<th class="hr-sum">이달</th></tr></thead><tbody>' + trs + '</tbody></table></div>' +
      '<div class="hr-legend"><span><i class="hc reg">○</i>정규</span><span><i class="hc alt">△</i>다른 시간</span><span><i class="hc abs">×</i>결근</span><span><i class="hc off">–</i>휴무</span><span><i class="hc due"></i>안 찍은 근무일</span><span><i class="r-ex">1.5</i>배율</span><span><i class="dot-ex"></i>메모</span></div>' +
      '<p class="f-note">칸을 누르면 찍습니다. 이름을 누르면 정규 근무·급여를 고칩니다. 시간은 정규 근무 시간표에서 자동으로 세고, 다른 시간(△)은 적은 시각으로 셉니다.</p>';
  }
  /* 폰에서는 날짜 열이 6개쯤만 보여 오늘이 안 보임 → 그린 뒤 오늘 열이 보이게 스크롤(처음 한 번) */
  if(!HR.pay && !HR.scrolled) setTimeout(function(){ var sc = document.querySelector(".hr-scroll"), td = sc && sc.querySelector("thead th.today"); if(sc && td && td.offsetLeft > sc.clientWidth - 160){ sc.scrollLeft = td.offsetLeft - 120; } HR.scrolled = true; }, 30);
  return head + body + (HR.pop ? hrPopHtml() : "") + (HR.edit ? hrEditHtml() : "");
}
function hrPayTable(list, m){
  var mx = new Date(m + "-01T00:00:00"), title = mx.getFullYear() + "년 " + (mx.getMonth() + 1) + "월";
  var rows = list.map(function(s){
    var t = hrCalc(s, m), hourly = s.pay_type !== "monthly";
    var how = hourly ? hrWon(s.pay) + " × " + t.weighted + "h" : "월급";
    return '<tr><td><b>' + esc(s.name) + '</b><small>' + esc(s.role || "") + '</small></td><td>' + t.reg + '일</td><td>' + t.alt + '일</td><td>' + t.abs + '일</td><td>' + t.hours + 'h' + (t.extra ? '<small>가산 ' + t.extra + 'h → ' + t.weighted + 'h</small>' : '') + '</td><td><small>' + how + '</small></td><td class="won"><b>' + hrWon(t.pay) + '</b></td></tr>';
  }).join("");
  var total = list.reduce(function(a, s){ return a + hrCalc(s, m).pay; }, 0);
  var text = title + " 급여\n" + list.map(function(s){ var t = hrCalc(s, m); return s.name + " · 출근 " + t.days + "일 " + t.hours + "h" + (t.extra ? " (가산 " + t.extra + "h)" : "") + (t.abs ? " · 결근 " + t.abs : "") + " → " + hrWon(t.pay); }).join("\n") + "\n합계 " + hrWon(total);
  return '<div class="card" style="padding:0; overflow:auto"><table class="hr-pay"><thead><tr><th>직원</th><th>정규</th><th>다른 시간</th><th>결근</th><th>시간</th><th>계산</th><th>급여</th></tr></thead><tbody>' + rows +
    '<tr class="tot"><td colspan="6">합계</td><td class="won"><b>' + hrWon(total) + '</b></td></tr></tbody></table></div>' +
    '<div class="btn-row" style="margin-top:12px"><button class="btn sm" onclick="navigator.clipboard&&navigator.clipboard.writeText(' + JSON.stringify(text).replace(/"/g, "&quot;") + ').then(function(){ showToast(\'복사했습니다\'); })">글로 복사</button></div>' +
    '<p class="f-note">시급제 = 시급 × (근무 시간 × 배율)의 합. 월급제 = 월급 그대로(결근·다른 시간은 참고 숫자). 세금·4대보험은 넣지 않습니다 — 급여 대장은 세무사와.</p>';
}
function hrPopHtml(){
  var p = HR.pop, s = HR.staff.find(function(x){ return x.id === p.staff_id; }) || {}, c = hrSched(s);
  var seg = function(k, v, label){ return '<button class="' + (p[k] == v ? "on" : "") + '" onclick="hrPopSet(\'' + k + '\',' + JSON.stringify(v) + ')">' + label + '</button>'; };
  return '<div class="overlay" onclick="HR.pop=null; render()"><div class="sheet" onclick="event.stopPropagation()">' +
    sheetHead(esc(s.name) + ' · ' + dateLabel(p.date)) +
    '<p class="f-note" style="margin:-6px 0 12px">정규 근무: ' + esc(hrSchedText(s)) + '</p>' +
    '<div class="seg hr-seg">' + seg("status", "정규", "○ 정규") + seg("status", "변형", "△ 다른 시간") + seg("status", "결근", "× 결근") + seg("status", "휴무", "– 휴무") + '</div>' +
    (p.status === "변형" ? '<div class="grid3" style="margin-top:12px"><label class="f"><div class="lb">시작</div><input type="time" value="' + esc(p.start || c.start) + '" onchange="hrPopSet(\'start\', this.value)"></label>' +
      '<label class="f"><div class="lb">종료</div><input type="time" value="' + esc(p.end || c.end) + '" onchange="hrPopSet(\'end\', this.value)"></label>' +
      '<label class="f"><div class="lb">휴게(분)</div><input type="number" min="0" step="10" value="' + Number(p.break_min || 0) + '" oninput="hrPopSet(\'break_min\', this.value)"></label></div>' : '') +
    (p.status === "정규" || p.status === "변형" ? '<div class="f" style="margin-top:12px"><div class="lb">배율 <span class="lbl-note">휴일·연장 같은 때</span></div><div class="seg">' + seg("rate", 1, "1배") + seg("rate", 1.5, "1.5배") + seg("rate", 2, "2배") + '</div></div>' : '') +
    '<label class="f" style="margin-top:12px"><div class="lb">메모 <span class="lbl-note">선택</span></div><input type="text" value="' + esc(p.memo || "") + '" placeholder="예: 늦게 옴, 행사 지원" oninput="hrPopSet(\'memo\', this.value)"></label>' +
    '<div class="sheet-actions">' + (p._new ? '' : '<button class="btn ghost danger" onclick="hrPopDel()">지우기</button>') + '<button class="btn ghost" onclick="HR.pop=null; render()">취소</button><button class="btn primary" data-enter onclick="hrPopSave()">저장</button></div></div></div>';
}
function hrEditHtml(){
  var e = HR.edit, sc = e.sched;
  var daysBtns = HR_DAYS.map(function(d, i){ return '<button class="' + (sc.days[i] ? "on" : "") + '" onclick="hrEditDay(' + i + ')">' + d + '</button>'; }).join("");
  return '<div class="overlay" onclick="HR.edit=null; render()"><div class="sheet" onclick="event.stopPropagation()">' +
    sheetHead(e._new ? "직원 추가" : "직원") +
    '<div class="grid2"><label class="f"><div class="lb">이름</div><input type="text" value="' + esc(e.name) + '" oninput="hrEditSet(\'name\', this.value)"></label>' +
    '<label class="f"><div class="lb">역할 <span class="lbl-note">홀·주방 등</span></div><input type="text" value="' + esc(e.role || "") + '" oninput="hrEditSet(\'role\', this.value)"></label></div>' +
    '<label class="f"><div class="lb">전화</div><input type="tel" value="' + esc(e.phone || "") + '" oninput="hrEditSet(\'phone\', this.value)"></label>' +
    '<div class="f"><div class="lb">급여</div><div class="seg"><button class="' + (e.pay_type !== "monthly" ? "on" : "") + '" onclick="hrEditSet(\'pay_type\',\'hourly\'); render()">시급</button><button class="' + (e.pay_type === "monthly" ? "on" : "") + '" onclick="hrEditSet(\'pay_type\',\'monthly\'); render()">월급</button></div></div>' +
    '<label class="f"><div class="lb">' + (e.pay_type === "monthly" ? "월급(원)" : "시급(원)") + '</div><input type="number" min="0" step="100" value="' + Number(e.pay || 0) + '" oninput="hrEditSet(\'pay\', this.value)"></label>' +
    '<div class="f"><div class="lb">정규 근무 요일</div><div class="seg hr-days">' + daysBtns + '</div></div>' +
    '<div class="grid3"><label class="f"><div class="lb">시작</div><input type="time" value="' + esc(sc.start) + '" onchange="HR.edit.sched.start=this.value"></label><label class="f"><div class="lb">종료</div><input type="time" value="' + esc(sc.end) + '" onchange="HR.edit.sched.end=this.value"></label><label class="f"><div class="lb">휴게(분)</div><input type="number" min="0" step="10" value="' + Number(sc.break || 0) + '" oninput="HR.edit.sched.break=this.value"></label></div>' +
    '<div class="grid2"><label class="f"><div class="lb">입사일</div><input type="date" value="' + esc(e.start_date || "") + '" onchange="hrEditSet(\'start_date\', this.value)"></label><label class="f"><div class="lb">퇴사일 <span class="lbl-note">비우면 재직</span></div><input type="date" value="' + esc(e.end_date || "") + '" onchange="hrEditSet(\'end_date\', this.value || null)"></label></div>' +
    '<label class="f"><div class="lb">메모</div><input type="text" value="' + esc(e.memo || "") + '" oninput="hrEditSet(\'memo\', this.value)"></label>' +
    '<div class="sheet-actions">' + (e._new ? '' : '<button class="btn ghost ' + (e.active === false ? "" : "danger") + '" onclick="hrStaffRetire()">' + (e.active === false ? "재직으로" : "퇴사") + '</button>') +
    '<button class="btn ghost" onclick="HR.edit=null; render()">취소</button><button class="btn primary" data-enter onclick="hrStaffSave()">저장</button></div></div></div>';
}
/* Esc: 작은 창이 떠 있으면 그것부터 닫음(18-router 의 키 처리에서 부름) */
function hrEsc(){ if(!HR || !(view.form && view.form.type === "staff")) return false; if(HR.pop){ HR.pop = null; render(); return true; } if(HR.edit){ HR.edit = null; render(); return true; } return false; }
