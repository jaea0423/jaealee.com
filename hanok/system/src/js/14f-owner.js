/* ---------- 사장님 메뉴 (18차, 재아) ----------
   더보기(⋮) → 사장님. 관리자 비밀번호 한 번 통과하면 그 안의 것들은 다시 안 묻습니다(설정과 같은 view.adminOk).
   여기 모은 것: 디스플레이 모드 · 수기 예약지 · 워크시프트 · 손님 관리(노쇼 관리 포함) · 문자 · PIN·보안 관리 · 홈페이지 관리.
   화면형(view.form={type:"owner", page:true}) — 큰 단추 격자. 폰에서는 두 줄. */
async function openOwnerPage(){
  /* 09-20(재아): 메뉴 자체는 안 묻고, 안의 것을 누를 때마다 묻습니다(10분 유지 체크로 줄일 수 있음) */
  view.form = {type:"owner", page:true}; render();
}
/* 사장님 화면에서 고른 설정을 바로 엽니다. 별도 '설정' 목록을 한 번 더 거치지 않습니다. */
async function openOwnerSetting(key){
  if(!await adminGate("설정 열기")) return;
  if(view.draft && !settingsDirty()) view.draft = null;
  if(!view.draft) view.draft = deepClone(store().settings);
  view.form = null; view.tab = "settings"; view.setSec = key; render(); window.scrollTo(0,0);
}
async function closeSettingsToOwner(){
  await setTab("dash");
  if(view.tab === "dash"){ view.form = {type:"owner", page:true}; render(); window.scrollTo(0,0); }
}
function openMessagesPage(){ view.form = {type:"messages", page:true, back:"owner"}; render(); window.scrollTo(0,0); }
function sheetMessages(){
  var item = function(fn, icon, title, sub){ return '<button class="own-it" onclick="' + fn + '">' + icon + '<b>' + title + '</b><small>' + sub + '</small></button>'; };
  return '<div class="own-section"><h2>문자</h2><p class="own-lead">감사 문자 작성부터 직접 보내기와 기록 확인까지 한곳에서 관리합니다.</p><div class="own-grid">' +
    item("openThanksPage()", ICON.spark, "감사 문자", "방문 손님 문안 작성 · 예약 발송") +
    item("openSmsFree(true)", ICON.sms, "문자 보내기", "번호를 직접 입력해 보내기") +
    item("openSmsLog(true)", ICON.inbox, "문자 기록", "작성·발송 기록 확인") +
    '</div></div>';
}
/* ---------- 퇴근하기(09-20 재아) — 안내 겸 정리. 써도 되고 안 써도 되는 편의 기능 ----------
   1) 오늘 예약 중 아직 '확정' 인 것 → 방문/노쇼 한 번에   2) 근무 찍기(워크시프트)   3) 감사 문자 만들어 예약 발송   4) 끝 */
async function openCloseDay(date){
  var d = date || todayStr();
  if(d === todayStr()){   /* 영업 종료 2시간 전부터(재아 09-20). 그 전이면 막지 않고 되묻기만 */
    var h = hoursFor(d); if(!h.closed && toMin(nowHM()) < toMin(h.close) - 120){
      if(!await uiConfirm("아직 영업 중입니다", "퇴근 정리는 영업 종료 2시간 전(" + hm(minToHM(toMin(h.close) - 120)) + ")부터 여는 걸 권합니다. 그래도 열까요?", {ok:"열기", cancel:"나중에"})) return;
    }
  }
  view.form = {type:"closeday", page:true, date:d, back:(view.form && (view.form.type === "owner" || view.form.back)) ? "owner" : ""}; render();
}
function sheetCloseDay(){
  var today = (view.form && view.form.date) || todayStr();
  /* 그날 예약 전부(확정·방문·노쇼) — 누른 건 사라지지 않고 검게 표시된 채 남음. 한 번 더 누르면 풀림(09-24 재아) */
  var all = store().reservations.filter(function(r){ return r.date === today && (r.status === "확정" || r.status === "방문" || r.status === "노쇼"); }).sort(function(a,b){ return a.time.localeCompare(b.time); });
  var left = all.filter(function(r){ return r.status === "확정"; });
  var rows = all.map(function(r){ return '<div class="rowitem cd-row s-' + r.status + '"><span class="time-col">' + esc(hm(r.time)) + '</span><span class="grow"><span class="t">' + tierTag(r) + groupTag(r) + esc(r.name) + '</span><span class="s">' + esc(pplText(r)) + ' · ' + seatKindText(r) + '</span></span>' +   /* 자리는 룸/테이블만(09-24) */
    '<span class="btn-row"><button class="btn sm cd-v ' + (r.status === "방문" ? "on" : "ghost") + '" onclick="cdMark(\'' + r.id + '\', \'방문\')">방문</button><button class="btn sm cd-ns ' + (r.status === "노쇼" ? "on" : "ghost") + '" onclick="cdMark(\'' + r.id + '\', \'노쇼\')">노쇼</button></span></div>'; }).join("");
  var done = left.length === 0;
  var step = function(n, ok, title, right, body){ return '<div class="cd-step' + (ok ? ' done' : '') + '"><div class="cd-n">' + n + '</div><div class="cd-b"><div class="cd-bh"><b>' + title + '</b>' + (right || '') + '</div>' + (body || '') + '</div></div>'; };
  return '<div class="cd-wrap">' +
    '<div class="cd-hello"><b>' + (today === todayStr() ? "오늘도 고생 많으셨습니다." : dateLabel(today) + " 정리") + '</b><small>' + esc(dateLabel(today)) + '</small></div>' +
    step(1, done, "손님 방문 처리", done || !all.length ? '' : '<button class="btn sm primary" onclick="cdMarkAll()">남은 ' + left.length + '건 전부 방문</button>',
      all.length ? '<div class="card searchbox" style="margin-top:8px">' + rows + '</div>' : '<small>이날 예약이 없습니다.</small>') +
    step(2, false, "워크시프트", '<button class="btn sm" onclick="cdStaffOpen()">워크시프트 작성</button>') +
    step(3, false, "감사 문자", '<button class="btn sm" onclick="cdThanksOpen()">감사 문자 작성</button>') +
    step(4, false, "끝", '<button class="btn sm primary" onclick="cdLeave()">퇴근</button>') +
    '</div>' + (view.cdStaff ? cdStaffHtml() : '') + (HR && HR.pop && view.cdStaff ? hrPopHtml() : '') + (view.cdThanks ? cdThanksHtml() : '');
}
async function cdMark(id, st){
  var r = store().reservations.find(function(x){ return x.id === id; }); if(!r) return;
  var to = r.status === st ? "확정" : st;   /* 같은 걸 한 번 더 누르면 선택 해제 = 다시 '확정' */
  if(to === "노쇼" && !await uiConfirm("노쇼로 표시할까요?", r.name + " 손님 · " + hm(r.time), {ok:"노쇼", cancel:"취소", tone:"warn"})) return;
  var before = deepClone(r); r.status = to; addChange(r, "상태", diffRes(before, r)); saveData(); render();
}
async function cdMarkAll(){
  var today = (view.form && view.form.date) || todayStr();
  var left = store().reservations.filter(function(r){ return r.date === today && r.status === "확정"; });
  if(!left.length) return;
  if(!await uiConfirm("남은 " + left.length + "건을 전부 방문으로 표시할까요?", "안 온 손님이 있으면 그 줄만 노쇼로 바꾸면 됩니다.", {ok:"전부 방문", cancel:"취소"})) return;
  left.forEach(function(r){ var before = deepClone(r); r.status = "방문"; addChange(r, "상태", diffRes(before, r)); });
  saveData(); render();
}
/* ---------- 퇴근하기 안의 '오늘 워크시프트' 팝업(09-24 재아) ----------
   워크시프트 화면으로 넘어가지 않고 그 자리에서 오늘 줄만. 누르면 바로 저장(워크시프트 표와 같은 자료 attendance) */
async function cdStaffOpen(){
  if(!supaOn()){ await uiAlert("서버 설정이 없는 빌드입니다", "워크시프트는 서버가 있어야 합니다.", "warn"); return; }
  if(!await adminGate("워크시프트")) return;
  if(!HR) HR = { week: hrWeekStart(todayStr()), month: monthStr(), staff:[], att:{}, loaded:{}, cfg:null, loading:true, pop:null, edit:null, view:"week", slip:null, setup:false, retired:false };
  view.cdStaff = true; HR.loading = true; render();
  HR.week = hrWeekStart((view.form && view.form.date) || todayStr()); HR.month = ((view.form && view.form.date) || todayStr()).slice(0, 7);
  await hrLoad(); render();
}
function cdStaffClose(){ view.cdStaff = false; if(HR) HR.pop = null; render(); }
async function cdStaffQuick(id, status){
  var d = (view.form && view.form.date) || todayStr(), s = HR.staff.find(function(x){ return x.id === id; }); if(!s) return;
  var a = HR.att[id + "|" + d];
  if(a && a.status === status){   /* 같은 걸 또 누르면 지움 */
    try{ await sb("/rest/v1/attendance?id=eq." + encodeURIComponent(a.id), { method:"DELETE", prefer:"return=minimal" }); delete HR.att[id + "|" + d]; render(); }catch(e){ await uiAlert("지우지 못했습니다", e.message || String(e), "warn"); }
    return;
  }
  var row = { id:"att_" + id + "_" + d, store:view.storeKey || "hanok", staff_id:id, date:d, status:status, start:"", end:"", break_min:0, spans:[], rate:1, memo:"", by:(SESSION && SESSION.who) || "" };
  try{ await sb("/rest/v1/attendance?on_conflict=id", { method:"POST", body:row, prefer:"resolution=merge-duplicates,return=minimal" }); HR.att[id + "|" + d] = row; render(); }
  catch(e){ await uiAlert("저장 실패", e.message || String(e), "warn"); }
}
function cdStaffHtml(){
  var d = (view.form && view.form.date) || todayStr();
  var body;
  if(!HR || HR.loading) body = '<p class="muted" style="padding:16px 0">불러오는 중…</p>';
  else if(HR.err) body = '<p class="f-note rust">불러오지 못했습니다: ' + esc(HR.err) + '</p>';
  else {
    var list = HR.staff.filter(function(s){ return s.active !== false; });
    body = hrGroups(list).map(function(g){ return '<div class="cd-sgrp">' + esc(g.role) + '</div>' + g.list.map(function(s){
      var a = HR.att[s.id + "|" + d], duty = hrOnDuty(s, d), st = a ? a.status : "", h = a ? hrRound(hrHours(s, a)) : 0;
      var b = function(k, label){ return '<button class="btn sm cd-sb' + (st === k ? ' on' : '') + '" onclick="cdStaffQuick(\'' + s.id + '\', \'' + k + '\')">' + label + '</button>'; };
      return '<div class="rowitem cd-srow"><span class="grow"><span class="t">' + esc(hrLabel(s)) + '</span><span class="s">' + (duty ? '정규 ' + esc(hrSchedAt(s, d).spans.map(hrSpanText).join(" · ")) : '오늘 정규 근무 없음') + (st ? ' · ' + (h ? h + '시간' : st) : '') + '</span></span>' +
        '<span class="btn-row">' + b("정규", "○ 정규") + '<button class="btn sm cd-sb' + (st === "변형" ? ' on' : '') + '" onclick="hrCell(\'' + s.id + '\', \'' + d + '\')">△ 다른 시간</button>' + b("결근", "× 결근") + b("휴무", "– 휴무") + '</span></div>';
    }).join(""); }).join("") || '<p class="muted">직원이 없습니다.</p>';
  }
  return '<div class="overlay" onclick="cdStaffClose()"><div class="sheet sheet-tall" onclick="event.stopPropagation()">' + sheetHead("워크시프트 · " + dateLabel(d)) +
    '<div class="searchbox" style="flex:1; min-height:0; overflow:auto">' + body + '</div>' +
    '<div class="sheet-actions"><button class="btn primary" onclick="cdStaffClose()">완료</button></div></div></div>';
}
/* ---------- 퇴근하기 안의 감사 문자 팝업 — 화면이 바뀌면 퇴근 순서를 잃어서(09-24 재아). 감사 문자 화면(14g)을 그대로 덮개 안에 ---------- */
async function cdThanksOpen(){
  if(!supaOn()){ await uiAlert("서버 설정이 없는 빌드입니다", "감사 문자는 서버가 있어야 합니다.", "warn"); return; }
  if(!await adminGate("감사 문자")) return;
  if(!TH) TH = { date: todayStr(), items:{}, queue:[], tab:"make", busy:{}, sendAt:"", adv:false, run:null, stop:false, qf:"all" };
  TH.date = (view.form && view.form.date) || todayStr();
  TH.sendAt = TH.sendAt || (shiftDate(todayStr(), 1) + "T" + thCfg().hour);
  view.cdThanks = true; render(); await thLoadQueue(); render();
}
function cdThanksClose(){ if(thRunning()){ showToast("AI 가 글을 짓는 중입니다 — 끝나거나 중단한 뒤에 닫으세요"); return; } view.cdThanks = false; render(); }
function cdThanksHtml(){
  return '<div class="overlay" onclick="cdThanksClose()"><div class="sheet sheet-tall sheet-wide cd-th" onclick="event.stopPropagation()">' + sheetHead("감사 문자") +
    '<div class="searchbox" style="flex:1; min-height:0; overflow:auto">' + sheetThanks() + '</div>' +
    '<div class="sheet-actions"><button class="btn primary" onclick="cdThanksClose()">완료</button></div></div></div>';
}
/* ---------- 퇴근 — '수고하셨습니다' + 폭죽 뒤 잠금 화면으로(09-24 재아) ---------- */
function cdLeave(){
  view.cdStaff = false; view.cdThanks = false;
  var ov = document.createElement("div"); ov.className = "cd-bye";
  ov.innerHTML = '<canvas></canvas><div class="cd-bye-t"><b>수고하셨습니다</b><small>오늘도 고맙습니다. 푹 쉬세요.</small></div>';
  document.body.appendChild(ov);
  var c = ov.querySelector("canvas"), g = c.getContext("2d"), W = c.width = window.innerWidth, H = c.height = window.innerHeight, parts = [], t0 = Date.now();
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var cols = ["#E5C15C", "#F28C6B", "#8FC6E8", "#B5E39B", "#FFFFFF", "#F5A3C7"];
  function burst(x, y){ for(var i = 0; i < 90; i++){ var a = Math.random() * Math.PI * 2, v = 2 + Math.random() * 5; parts.push({x:x, y:y, vx:Math.cos(a) * v, vy:Math.sin(a) * v, life:60 + Math.random() * 30, c:cols[i % cols.length]}); } }
  if(!still){ burst(W * 0.3, H * 0.35); setTimeout(function(){ burst(W * 0.7, H * 0.3); }, 350); setTimeout(function(){ burst(W * 0.5, H * 0.2); }, 700); setTimeout(function(){ burst(W * 0.2, H * 0.25); }, 1050); setTimeout(function(){ burst(W * 0.8, H * 0.4); }, 1350); }
  (function tick(){
    if(!ov.parentNode) return;
    g.fillStyle = "rgba(20,19,17,.18)"; g.fillRect(0, 0, W, H);   /* 옅은 덮기로 꼬리를 남김 */
    parts.forEach(function(p){ p.x += p.vx; p.y += p.vy; p.vy += 0.06; p.vx *= 0.985; p.life--; g.globalAlpha = Math.min(1, Math.max(0, p.life / 45)); g.fillStyle = p.c; g.beginPath(); g.arc(p.x, p.y, 2.6, 0, Math.PI * 2); g.fill(); });   /* 3px 네모는 너무 옅었음 — 동그라미·끝까지 밝게 */
    g.globalAlpha = 1; parts = parts.filter(function(p){ return p.life > 0; });
    if(Date.now() - t0 < 3200) requestAnimationFrame(tick);
  })();
  logEvent("퇴근", (view.form && view.form.date) || todayStr());
  setTimeout(function(){ ov.classList.add("out"); setTimeout(function(){ ov.remove(); view.form = null; lockNow(); }, 450); }, 3000);
}
/* ---------- 예약 내보내기(CSV, 09-20 재아) — 엑셀에서 바로 열림(UTF-8 BOM). 기간은 물어봄 ---------- */
async function exportCsv(){
  var from = await uiPrompt("예약 내보내기", "시작일 (YYYY-MM-DD)", {value: shiftDate(todayStr(), -30), ok:"다음"}); if(from == null) return;
  var to = await uiPrompt("예약 내보내기", "마지막 날 (YYYY-MM-DD)", {value: todayStr(), ok:"내보내기"}); if(to == null) return;
  var list = store().reservations.filter(function(r){ return r.date >= from && r.date <= to; }).sort(function(a,b){ return (a.date + a.time).localeCompare(b.date + b.time); });
  var head = ["예약번호","날짜","시각","이름","전화","인원","어린이","좌석","상태","경로","코스·세트","요청사항","메모","등록일시"];
  var q = function(v){ v = String(v == null ? "" : v); return '"' + v.replace(/"/g, '""') + '"'; };
  var lines = [head.map(q).join(",")].concat(list.map(function(r){ return [resCode(r), r.date, r.time, r.name, r.phone || "", pplOf(r), r.infants || 0, resSeatLabel(r), r.status, r.source || "", (typeof courseSummary === "function" ? courseSummary(r.courses) : "") || (r.courseUndecided ? "미정" : ""), r.request || "", r.memo || "", r.createdAt || ""].map(q).join(","); }));
  var blob = new Blob(["\ufeff" + lines.join("\r\n")], {type:"text/csv;charset=utf-8"});
  var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "한옥반점_예약_" + from + "_" + to + ".csv"; document.body.appendChild(a); a.click(); setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  logEvent("예약 내보내기", from + "~" + to + " " + list.length + "건"); showToast(list.length + "건을 내보냈습니다");
}
function sheetOwner(){
  var item = function(fn, icon, title, sub){ return '<button class="own-it" onclick="' + fn + '">' + icon + '<b>' + title + '</b><small>' + sub + '</small></button>'; };
  var pend = typeof reqPending === "function" ? reqPending().length : 0;
  var st = store().settings;
  return '<div class="own-section"><h2>사장님</h2><div class="own-grid">' +
    item("openSiteAdmin()", ICON.site, "홈페이지 관리", "글·사진·팝업·소식·예약 접수" + (pend ? " · 대기 " + pend + "건" : "")) +
    item("openStaffPage()", ICON.staff, "워크시프트", "직원 근무표 · 급여") +
    item("openGuestsPage()", ICON.users, "손님 관리", "단골·메모 · 노쇼 관리") +
    item("openMessagesPage()", ICON.sms, "문자", "감사 문자 · 직접 보내기 · 기록") +
    item("openCloseDay()", ICON.clock, "퇴근하기", "방문 처리 · 근무 · 감사 문자 차례로") +
    '</div></div><div class="own-section"><h2>설정</h2><div class="own-grid">' +
    item("openOwnerSetting('hours')", ICON.clock, "운영시간", hoursFor(todayStr()).open + " ~ " + hoursFor(todayStr()).close) +
    item("openOwnerSetting('rules')", ICON.res, "예약 규칙", "단체 " + (st.groupSize||8) + "명") +
    item("openOwnerSetting('seats')", ICON.dash, "좌석", "룸·테이블·배정 순서") +
    item("openOwnerSetting('course')", ICON.chart, "코스·세트 구성", "코스와 적용 기간") +
    item("openOwnerSetting('source')", ICON.inbox, "예약경로", "전화·네이버·방문") +
    item("openOwnerSetting('sms')", ICON.sms, "문자 안내", "접수·재안내 문안") +
    item("openOwnerSetting('disp')", ICON.tv, "디스플레이 설정", "좌석표·광고 영상") +
    item("openOwnerSetting('thanks')", ICON.spark, "감사 문자 AI", "프롬프트·기본 양식") +
    item("openOwnerSetting('policy')", ICON.set, "운영 판단 기준", "정원·경고 기준") +
    item("openOwnerSetting('zoom')", ICON.search, "화면 크기", "모든 기기 공통") +
    '</div></div><div class="own-section"><h2>관리</h2><div class="own-grid">' +
    (isMobile() ? "" : item("openDisplay()", ICON.tv, "디스플레이 모드", "손님용 TV 화면")) +
    item("openSlip()", ICON.print, "수기 예약지", "전화 예약을 손으로 적는 종이") +
    item("openDevPage()", ICON.sms, "개발자에게", "고칠 것 · 급한 것 글로 남기기") +
    item("exportCsv()", ICON.print, "예약 내보내기", "엑셀로 여는 CSV") +
    item("openRate('owner')", ICON.chart, "예약률 추이", "최근 예약률과 흐름") +
    item("openOwnerSetting('admin')", ICON.key, "PIN·보안 관리", "직원 PIN · 사장님 비밀번호 · 로그") +
    '</div></div>';
}
/* Esc: 퇴근하기 안의 작은 창부터 닫음(바로 퇴근하기 화면 전체가 닫히지 않게) */
function cdEsc(){ if(HR && HR.pop && view.cdStaff){ HR.pop = null; render(); return true; } if(view.cdStaff){ cdStaffClose(); return true; } if(view.cdThanks){ cdThanksClose(); return true; } return false; }
