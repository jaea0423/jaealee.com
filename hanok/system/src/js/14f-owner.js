/* ---------- 사장님 메뉴 (18차, 재아) ----------
   더보기(⋮) → 사장님. 관리자 비밀번호 한 번 통과하면 그 안의 것들은 다시 안 묻습니다(설정과 같은 view.adminOk).
   여기 모은 것: 디스플레이 모드 · 수기 예약지 · 워크시프트 · 손님 관리(노쇼 관리 포함) · 문자(기록·직접 보내기·감사 문자) · PIN 관리 · 홈페이지 관리.
   화면형(view.form={type:"owner", page:true}) — 큰 단추 격자. 폰에서는 두 줄. */
async function openOwnerPage(){
  /* 09-20(재아): 메뉴 자체는 안 묻고, 안의 것을 누를 때마다 묻습니다(10분 유지 체크로 줄일 수 있음) */
  view.form = {type:"owner", page:true}; render();
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
  /* 그날 예약 전부(확정·방문·노쇼) — 누른 건 사라지지 않고 검게 표시된 채 남음(재아 09-20) */
  var all = store().reservations.filter(function(r){ return r.date === today && (r.status === "확정" || r.status === "방문" || r.status === "노쇼"); }).sort(function(a,b){ return a.time.localeCompare(b.time); });
  var left = all.filter(function(r){ return r.status === "확정"; });
  var rows = all.map(function(r){ return '<div class="rowitem cd-row s-' + r.status + '"><span class="time-col">' + esc(hm(r.time)) + '</span><span class="grow"><span class="t">' + esc(r.name) + tierTag(r) + groupTag(r) + '</span><span class="s">' + esc(pplText(r)) + ' · ' + esc(resSeatLabel(r)) + '</span></span>' +
    '<span class="btn-row"><button class="btn sm cd-v ' + (r.status === "방문" ? "on" : "ghost") + '" onclick="cdMark(\'' + r.id + '\', \'방문\')">방문</button><button class="btn sm cd-n ' + (r.status === "노쇼" ? "on" : "ghost") + '" onclick="cdMark(\'' + r.id + '\', \'노쇼\')">노쇼</button></span></div>'; }).join("");
  var done = left.length === 0;
  return '<div class="cd-wrap">' +
    '<div class="cd-hello"><b>' + (today === todayStr() ? "오늘도 고생 많으셨습니다." : dateLabel(today) + " 정리") + '</b><small>' + esc(dateLabel(today)) + ' · 문 닫기 전에 세 가지만 정리하면 내일 아침이 편합니다.</small></div>' +
    '<div class="cd-step ' + (done ? "done" : "") + '"><div class="cd-n">1</div><div class="cd-b"><b>손님 방문 처리</b>' +
      (all.length ? '<small>' + (done ? '예약이 모두 정리됐습니다.' : '아직 \'확정\' 으로 남은 ' + left.length + '건 — 온 손님은 방문, 안 온 손님은 노쇼. 감사 문자는 방문으로 표시한 손님께만 갑니다.') + '</small>' +
        (done ? '' : '<div class="btn-row" style="margin-top:8px"><button class="btn sm primary" onclick="cdMarkAll()">남은 ' + left.length + '건 전부 방문</button></div>') +
        '<div class="card searchbox" style="margin-top:8px">' + rows + '</div>' : '<small>이날 예약이 없습니다.</small>') + '</div></div>' +
    '<div class="cd-step"><div class="cd-n">2</div><div class="cd-b"><b>근무 찍기</b><small>오늘 나온 직원의 근무를 워크시프트에 표시합니다. 정규대로면 ○ 한 번.</small><div class="btn-row" style="margin-top:8px"><button class="btn sm" onclick="openStaffPage()">워크시프트 열기</button></div></div></div>' +
    '<div class="cd-step"><div class="cd-n">3</div><div class="cd-b"><b>감사 문자</b><small>방문 처리한 손님께 키워드를 넣고 \'AI 로 완성하기\' → \'예약발송하기\'. 내일 오전 11시에 나갑니다. 지금 안 해도 내일 아침 확인 목록에 남습니다.</small><div class="btn-row" style="margin-top:8px"><button class="btn sm" onclick="openThanksPage()">감사 문자 열기</button></div></div></div>' +
    '<div class="cd-step"><div class="cd-n">4</div><div class="cd-b"><b>끝</b><small>다 했으면 닫고 퇴근하세요. 시스템은 켜 둬도 됩니다(TV 는 따로).</small><div class="btn-row" style="margin-top:8px"><button class="btn sm primary" onclick="closeSheet()">퇴근</button></div></div></div>' +
    '</div>';
}
async function cdMark(id, st){
  var r = store().reservations.find(function(x){ return x.id === id; }); if(!r || r.status === st) return;
  if(st === "노쇼" && !await uiConfirm("노쇼로 표시할까요?", r.name + " 손님 · " + hm(r.time), {ok:"노쇼", cancel:"취소", tone:"warn"})) return;
  var before = deepClone(r); r.status = st; addChange(r, "상태", diffRes(before, r)); saveData(); render();
}
async function cdMarkAll(){
  var today = (view.form && view.form.date) || todayStr();
  var left = store().reservations.filter(function(r){ return r.date === today && r.status === "확정"; });
  if(!left.length) return;
  if(!await uiConfirm("남은 " + left.length + "건을 전부 방문으로 표시할까요?", "안 온 손님이 있으면 그 줄만 노쇼로 바꾸면 됩니다.", {ok:"전부 방문", cancel:"취소"})) return;
  left.forEach(function(r){ var before = deepClone(r); r.status = "방문"; addChange(r, "상태", diffRes(before, r)); });
  saveData(); render();
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
  return '<div class="own-grid">' +
    item("openSiteAdmin()", ICON.site, "홈페이지 관리", "글·사진·팝업·소식·예약 접수" + (pend ? " · 대기 " + pend + "건" : "")) +
    item("openStaffPage()", ICON.staff, "워크시프트", "직원 근무표 · 급여") +
    item("openGuestsPage()", ICON.users, "손님 관리", "단골·메모 · 노쇼 관리") +
    item("openThanksPage()", ICON.spark, "감사 문자", "다녀간 손님께 AI 문자 · 예약 발송") +
    item("openSmsLog()", ICON.inbox, "문자 기록", "나간 문자 전부") +
    item("openSmsFree()", ICON.sms, "문자 직접 보내기", "번호 넣고 바로") +
    (isMobile() ? "" : item("openDisplay()", ICON.tv, "디스플레이 모드", "손님용 TV 화면")) +
    item("openSlip()", ICON.print, "수기 예약지", "전화 예약을 손으로 적는 종이") +
    item("openDevPage()", ICON.sms, "개발자에게", "고칠 것 · 급한 것 글로 남기기") +
    item("openCloseDay()", ICON.clock, "퇴근하기", "방문 처리 · 근무 · 감사 문자 차례로") +
    item("exportCsv()", ICON.print, "예약 내보내기", "엑셀로 여는 CSV") +
    item("openPinManage()", ICON.key, "PIN 관리", "직원 PIN · 사장님 2차 비밀번호") +
    item("setTab('settings')", ICON.set, "설정", "운영시간 · 좌석 · 코스 · 문자 안내") +
    '</div><p class="f-note">사장님만 쓰는 것들을 모았습니다. 직원 화면에서는 안 보이게 하는 작업(권한)은 나중에.</p>';
}
