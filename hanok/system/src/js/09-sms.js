/* ============================================================
   문자 안내 — ※ 지금은 흉내만 냅니다 (실제로 발송되지 않습니다)

   [왜 흉내로 두는가]
   문자를 실제로 보내려면 문자 발송 업체(알리고·솔라피 등)에 가입해서
   발신번호를 등록하고(통신사 사전등록 필요), 건당 요금을 내고, 그 업체 서버를
   호출해야 합니다. 브라우저에서 직접 못 보냅니다 — 열쇠(API 키)가 노출되니까요.
   그래서 **화면과 문안, 언제 나갈지를 먼저 확정**하고 발송만 나중에 붙입니다.
   실제로 붙일 때 고칠 곳은 smsSend() 한 곳뿐입니다.

   [언제 나가나]
   1. 접수 문자 — 예약을 등록한 즉시 1회
   2. 재안내 문자 — 설정한 시점에 1회 (기본: 전날 오후 5시)
      · 2일 전 / 1일 전 : 오전 9시 ~ 오후 7시, 1시간 단위
      · 당일          : 오전 9시 ~ 오전 11시, 1시간 단위
      · 재안내 시각이 **이미 지난 뒤에 접수된 예약은 재안내가 나가지 않습니다.**
        (전날 5시가 기준인데 당일 저녁 예약을 오후 6시에 받으면 보낼 시점이 없습니다)
      · 며칠 전이냐에 따라 문구가 달라집니다 — 모레 / 내일 / 오늘
   ============================================================ */
/* SMS_DEFAULT 는 DEFAULT_DATA 보다 위에 있습니다 (아래 주석 참고) */
/* st 를 넘기면 그 매장 기준으로 봅니다.
   생략하면 지금 보고 있는 매장 — 화면에서 부를 때는 이쪽입니다.
   ※ 매장을 고르기 전(앱 켜자마자)에는 store() 가 없으므로,
      smsTick() 처럼 매장 밖에서 도는 코드는 반드시 st 를 넘겨야 합니다. */
function smsCfg(st){
  var s = st || store();
  return { ...SMS_DEFAULT, ...((s && s.settings && s.settings.sms) || {}) };
}
/* 재안내 시점으로 고를 수 있는 시각. 당일은 오전만 — 저녁 예약 손님이
   오후에 "오늘 예약이십니다" 를 받아도 이미 늦습니다. */
function remindHours(offset){
  var out = [], h, last = (offset === 0) ? 11 : 19;
  for(h = 9; h <= last; h++) out.push(h);
  return out;
}
function offsetLabel(o){ return o === 2 ? "2일 전" : o === 1 ? "1일 전" : "당일 아침"; }
/* 재안내 시각 알약 — 30분 선택지가 없으니 "오전 9시" 로 짧게 */
function hourLabel(h){ return (h < 12 ? "오전 " : "오후 ") + (h % 12 === 0 ? 12 : h % 12) + "시"; }
/* 문자 안에 들어갈 말 — '설정값'이 아니라 '보내는 날과 예약일의 실제 차이'로 정합니다.
   앱이 꺼져 있어 뒤늦게 나가는 경우(전날 5시에 못 보내고 당일 아침에 나감)에
   설정값만 보면 "내일 예약입니다"라고 잘못 나갑니다. 손님이 날짜를 착각하게 됩니다. */
function smsGapWord(r){
  var d1 = new Date(r.date + "T00:00:00"), d0 = new Date(todayStr() + "T00:00:00");
  if(isNaN(d1)) return null;
  var g = Math.round((d1 - d0) / 86400000);
  return g < 0 ? null : g === 0 ? "오늘" : g === 1 ? "내일" : g === 2 ? "모레" : g + "일 뒤";
}

/* 재안내가 나갈 시각 (Date). 설정이 꺼져 있어도 계산은 합니다 — 미리보기에 씁니다 */
function remindAt(r, st){
  var c = smsCfg(st);
  if(!r || !r.date) return null;
  var d = new Date(shiftDate(r.date, -c.remindOffset) + "T00:00:00");
  if(isNaN(d)) return null;
  d.setHours(c.remindHour, 0, 0, 0);
  return d;
}
function smsFind(r, kind){
  var log = (r && r.sms) || [], i;
  for(i = log.length - 1; i >= 0; i--) if(log[i].kind === kind) return log[i];
  return null;
}
/* 재안내 문자의 현재 상태. state 하나로 화면·발송이 같은 판단을 쓰게 합니다 */
function remindState(r, st){
  var c = smsCfg(st), at = remindAt(r, st), sent = smsFind(r, "재안내");
  if(sent) return { state:"보냄", at:at, rec:sent };
  if(!c.on) return { state:"꺼짐", at:at };
  if(!(r.phone || "").trim()) return { state:"번호없음", at:at };
  if(r.status === "취소" || r.status === "노쇼") return { state:"제외", at:at };
  if(!at) return { state:"제외", at:null };
  /* 이미 오신 손님(방문)·시작 시각이 지난 예약에는 보내지 않습니다 — 지금은 흉내지만 실발송을 붙이면 그대로 나갑니다(점검 R6) */
  if(r.status === "방문") return { state:"제외", at:at };
  if(r.date < todayStr() || (r.date === todayStr() && toMin(r.time) < new Date().getHours()*60 + new Date().getMinutes())) return { state:"제외", at:at };
  /* 접수 시각이 재안내 시각보다 늦으면 보낼 시점이 이미 지났습니다 */
  var made = r.createdAt ? new Date(r.createdAt) : null;
  if(made && !isNaN(made) && made.getTime() > at.getTime())
    return { state:"늦은접수", at:at };
  return { state: at.getTime() <= Date.now() ? "발송대기" : "예정", at:at };
}
/* 상태를 사람이 읽는 한 줄로 */
function remindWhy(st){
  return st.state === "꺼짐"     ? "문자 안내가 꺼져 있습니다"
       : st.state === "번호없음" ? "전화번호가 없어 보낼 수 없습니다"
       : st.state === "제외"     ? "취소·노쇼·이미 오신 손님이거나 시각이 지나 보내지 않습니다"
       : st.state === "늦은접수" ? "재안내 시각이 지난 뒤에 접수돼 나가지 않습니다"
       : "";
}

/* ---------- 문안 ---------- */
function smsWhen(r){
  var d = new Date(r.date + "T00:00:00");
  var dow = ["일","월","화","수","목","금","토"][d.getDay()];
  return (d.getMonth() + 1) + "월 " + d.getDate() + "일(" + dow + ") " + hm(r.time);
}
/* seatLabel() 은 '지금 보고 있는 매장'(store())을 씁니다.
   문자는 매장을 고르기 전에도 만들어질 수 있어서(smsTick) 여기서는 직접 찾습니다. */
/* '4명' / 어린이가 있으면 '4명(어린이 1명 포함)'. 어린이가 없으면 괄호를 아예 안 씁니다 */
function smsPpl(r){
  var inf = r.infants || 0;
  return pplOf(r) + "명" + (inf > 0 ? "(어린이 " + inf + "명 포함)" : "");
}
/* kind: "접수" | "재안내". 재안내는 offset 을 넘겨 문구를 바꿉니다 */
function smsText(r, kind, offset, st){
  var c = smsCfg(st), s = st || store();
  var map = { "매장": s.name || "", "이름": r.name || "", "일시": smsWhen(r), "인원": smsPpl(r),
              "주차": (c.parkingNote || "").trim(),
              /* '오늘 / 내일 / 모레' 는 설정값이 아니라 보내는 날과 예약일의 실제 차이로 정합니다 */
              "오늘내일": kind === "접수" ? "" : (smsGapWord(r) || "") };
  var tpl = kind === "접수" ? (c.tplNew || SMS_DEFAULT.tplNew) : (c.tplRemind || SMS_DEFAULT.tplRemind);
  return smsFill(tpl, map);
}
/* 문안의 {자리} 를 채우고, 빈 값 때문에 생긴 앞 공백·겹친 빈 줄을 정리합니다 */
function smsFill(tpl, map){
  var out = String(tpl || "").replace(/\{(매장|이름|일시|인원|주차|오늘내일)\}/g, function(_, k){ return map[k] != null ? map[k] : ""; });
  out = out.replace(/^[ \t]+/mg, "").replace(/\n{3,}/g, "\n\n");
  return out.trim();
}

/* ---------- 발송 (흉내) ----------
   실제로 붙일 때는 이 함수 안에서 발송 업체 API 를 부르면 됩니다.
   나머지 코드는 손댈 필요가 없습니다. */
function smsSend(r, kind, offset, resent, st){
  var c = smsCfg(st);
  if(!r) return null;
  var rec = {
    kind: kind,
    at: new Date().toISOString(),
    to: (r.phone || "").trim(),
    offset: kind === "재안내" ? (offset != null ? offset : c.remindOffset) : null,
    text: smsText(r, kind, offset, st),
    resent: !!resent,
    mock: true                    /* 진짜로 나간 게 아니라는 표시 */
  };
  r.sms = (r.sms || []).concat([rec]);
  if(r.sms.length > 30) r.sms = r.sms.slice(-30);
  touch(r);
  return rec;
}

/* 재안내 시각이 지난 예약을 훑어 '보냄'으로 바꿉니다.
   실제 서비스라면 서버가 할 일입니다. 여기서는 화면이 열려 있을 때만 돕니다.
   지난 날짜는 건드리지 않습니다 — 예시 데이터 수백 건에 기록이 쌓이면 지저분해집니다. */
function smsTick(){
  var today = todayStr(), n = 0, keys = DATA ? Object.keys(DATA) : [], k, i;
  for(k = 0; k < keys.length; k++){
    var s = DATA[keys[k]];
    /* _auth·_logs 같은 내부 항목은 매장이 아닙니다 */
    if(!s || !s.settings || !s.reservations) continue;
    var c = smsCfg(s);
    if(!c.on) continue;
    for(i = 0; i < s.reservations.length; i++){
      var r = s.reservations[i];
      if(r.date < today) continue;
      if(remindState(r, s).state !== "발송대기") continue;
      smsSend(r, "재안내", c.remindOffset, false, s);
      n++;
    }
  }
  if(n) saveData();
  return n;
}
/* 매장 전체의 보낸 문자 — 최근 것부터 */
function smsLog(){
  var s = store(), out = [], i, j;
  for(i = 0; i < s.reservations.length; i++){
    var r = s.reservations[i], log = r.sms || [];
    for(j = 0; j < log.length; j++) out.push({ r:r, m:log[j] });
  }
  /* 관리자가 직접 보낸 문자(예약 없음) */
  var free = (s.settings && s.settings.smsFreeLog) || [];
  for(i = 0; i < free.length; i++) out.push({ r:{ id:null, name:free[i].name || "직접 입력" }, m:{ at:free[i].at, kind:"직접", to:free[i].to, text:free[i].text } });
  out.sort(function(a, b){ return a.m.at < b.m.at ? 1 : a.m.at > b.m.at ? -1 : 0; });
  return out;
}

/* 예약 한 건의 경고 사유 — 지표와 목록에서 함께 씁니다 */
function resWarn(r){
  const st = store().settings;
  const out = [];
  const h = hoursFor(r.date);
  if(h.closed) out.push("휴무일 예약");
  else{
    if(inBreak(r.date, r.time)) out.push("브레이크타임");
    if(toMin(r.time) < toMin(h.open) || toMin(r.time) >= toMin(h.close)) out.push("영업시간 밖");
    else if(toMin(r.time) > lastBookMin(r.date, r.time)) out.push("접수 마감 이후");
    else if(h.lo && toMin(r.time) > toMin(h.lo)) out.push("라스트오더 이후");
    if(toMin(r.time) + stayOf(r) > toMin(h.close)) out.push("마감 넘김");
  }
  const seat = st.rooms.find(x=>x.id===r.roomId);
  const ids = r.roomId ? [r.roomId].concat(r.extraIds||[]) : [];
  if(seat && resBlocked(r)) out.push("사용 중지 좌석");
  /* 2명이 2인석에 앉게 되면 알립니다(2인석은 좁아 손님이 싫어함 — 규칙은 누님 답 대기, 그때까지 경고만) */
  const tSeats = seat ? [seat] : (isTablePref(r.seatPref) && r.tentativeRoomId ? seatsOf(r).map(seatById).filter(Boolean) : []);
  if(pplOf(r) <= 2 && tSeats.length === 1 && isTable(tSeats[0]) && (tSeats[0].seats||4) <= 2 && r.status !== "취소") out.push("2인석 배정");
  if(seat){
    /* 룸·테이블 모두: 묶음(합침 포함)의 최대·최소로 판단. 테이블은 최소가 없고(여포만 4), 정원 초과만 봅니다 */
    if(pplOf(r) > seatsMax(ids)) out.push("정원 초과");
    else if(adultCount(pplOf(r), r.infants) < seatsMin(ids, r.date)) out.push("최소 인원 미달");
    if(ids.length > 1 && joinOf(ids) && (joinOf(ids).split || /원탁/.test(joinOf(ids).note||""))) out.push("원탁 합침 · 손님 확인");
  }
  if((r.infants||0) >= pplOf(r) && pplOf(r)>0) out.push("성인 없음");
  /* 테이블 예약(층): 숨은 배정 결과로 — 자리가 아예 없으면, 붙일 수 없어 나눠 앉으면 */
  if(!seat && isTablePref(r.seatPref) && r.status!=="취소"){
    /* 지난 날짜는 잠정 배정을 다시 계산하지 않으므로(reflowFuture 는 오늘 이후만) '자리 없음' 을 말할 수 없습니다 — 이미 다녀간 손님 */
    if(!r.tentativeRoomId){ if(r.date >= todayStr()) out.push("테이블 자리 없음"); }
    else if(r.tentativeSplit) out.push("나눠 앉음");
  }
  {
    const cn = Object.values(r.courses||{}).reduce((a,b)=>a+b,0);
    const ad = adultCount(pplOf(r), r.infants);
    if(seat && seat.type==="room"){
      if(r.menuType==="해당 없음") out.push("룸·코스·세트 아님");
      else if(r.menuType==="확인 필요") out.push("코스·세트 미확정");
    }
    /* 코스·세트 인원은 룸이든 테이블이든 어른 수에 맞춰야 합니다(누님 09-20: 인원에 맞춰 음식이 나가므로) */
    if(r.menuType==="코스" && !r.courseUndecided && cn>0 && cn<ad) out.push("코스·세트 인원 부족");
  }
  /* 테이블 하나에 기본 좌석보다 많이 앉힘(여포 4인석에 5명 — 되긴 하지만 좁음, 누님 09-20) */
  if(tSeats.length === 1 && isTable(tSeats[0]) && pplOf(r) > (tSeats[0].seats||4) && pplOf(r) <= seatMax(tSeats[0]) && r.status !== "취소") out.push(`${tSeats[0].seats||4}인석에 ${pplOf(r)}명`);
  /* 겹쳐 받은 룸은 접수 뒤에도 계속 보여야 합니다.
     막지 않고 받는 대신(설계 5.2), 취소를 깜빡한 예약이 남아 있는 경우를
     '확인 필요'에서 나중에라도 잡아낼 수 있게 합니다. */
  if(seat && r.roomId && r.status!=="취소"){
    if(ids.some(id=>roomStatus(r.date, r.time, id, r.id).hits.length)) out.push("좌석 겹침");
  }
  return out;
}

/* 손이 가야 할 것만 모읍니다. 각 줄은 눌러서 바로 처리할 수 있습니다. */
function checkItems(date){
  const s = store(), today = todayStr();
  const d = date || today;
  const list = s.reservations.filter(r=>r.date===d && r.status==="확정");
  const items = [];

  /* 어제 다녀간 손님 감사 문자 미발송 — 누락 방지(09-20). 수는 thanksTick 이 1분마다 셈 */
  if(typeof TH_MISSING === "number" && TH_MISSING > 0 && d === today) items.push(["amber", `감사 문자 안 보낸 손님 ${TH_MISSING}명`, "어제 방문 손님 중 예약 발송이 없는 건", `openThanksPage()`]);
  /* 홈페이지에서 들어온 손님 요청 — 날짜와 상관없이 대기 중이면 맨 위에 */
  const pend = reqPending();
  if(pend.length) items.push(["blue", `홈페이지 예약 ${pend.length}건`,
    pend.slice(0,3).map(q=>`${dateLabel(q.date)} ${hm(q.time)} ${q.name}`).join(", "), `openRequests()`]);

  /* 사용 중지 좌석에 잡힌 예약 — 날짜 상관없이 오늘 이후 전부. 미리 연락하거나 자리를 옮겨야 하니(재아) */
  const blk = s.reservations.filter(r=>r.date>=today && holdsSeat(r) && resBlocked(r)).sort((a,b)=>a.date.localeCompare(b.date)||a.time.localeCompare(b.time));
  if(blk.length) items.push(["rust", `사용 중지 좌석에 잡힌 예약 ${blk.length}건`,
    blk.slice(0,3).map(r=>`${dateLabel(r.date)} ${r.time} ${r.name} · ${resSeatLabel(r)}`).join(", "), `openPick('blocked')`]);

  const un = list.filter(isUnassigned);   /* 테이블 예약은 층이 자리 — 미배정 아님 */
  if(un.length) items.push(["amber", `좌석 미배정 ${un.length}건`,
    un.slice(0,3).map(r=>`${r.time} ${r.name}`).join(", "), `openUnassigned()`]);

  const allergy = list.filter(r=>r.allergy);
  if(allergy.length) items.push(["rust", `알러지 확인 ${allergy.length}건`,
    allergy.slice(0,2).map(r=>`${r.time} ${r.name} · ${r.allergy}`).join(" / "), `openPick('allergy')`]);

  const gsize = settingsAt(d).groupSize || 8;
  const group = list.filter(r=>pplOf(r) >= gsize);
  if(group.length) items.push(["pine", `단체 손님 ${group.length}건`,
    group.slice(0,3).map(r=>`${r.time} ${r.name} ${pplOf(r)}명`).join(", "), `openPick('group')`]);

  const menuChk = list.filter(r=>r.menuType==="확인 필요");
  if(menuChk.length) items.push(["amber", `메뉴 확인 ${menuChk.length}건`,
    menuChk.slice(0,3).map(r=>`${r.time} ${r.name}`).join(", "), `openPick('menu')`]);

  /* 취소·노쇼도 '자리를 비워야 하는 변동'이라 확정 목록이 아닌 그날 전체에서 셉니다 */
  const chg = s.reservations.filter(r=>r.date===d && changeTag(r));
  if(chg.length) items.push(["blue", `오늘 변동 ${chg.length}건`,
    chg.slice(0,3).map(r=>`${hm(r.time)} ${r.name} ${changeTag(r).kind}`).join(", "), `openPick('changed')`]);

  const ns = list.filter(r=>noshowOf(r.phone));
  /* 8차-U(재아): 취소 등으로 자리가 나서, 나눠 앉거나 자리 없던 예약을 한 자리로 옮길 수 있게 된 것 */
  const better = list.filter(r=>{
    if(!isTablePref(r.seatPref)) return false;
    if(!(r.tentativeSplit || !r.tentativeRoomId)) return false;
    const f = floorFit(prefFloor(r.seatPref), r.date, r.time, pplOf(r), r.id);
    return f.state === "ok";
  });
  if(better.length) items.push(["pine", `자리 개선 가능 ${better.length}건`, "나눠 앉거나 자리 없던 테이블 예약에 한 자리가 났습니다. 새로고침하면 다시 배정됩니다.", "openPick('better')"]);
  if(ns.length) items.push(["rust", `노쇼 이력 손님 ${ns.length}건`,
    ns.slice(0,3).map(r=>`${r.time} ${r.name}`).join(", "), `openPick('noshow')`]);

  if(d===today){
    const y = shiftDate(today,-1);
    const yAll = s.reservations.filter(r=>r.date===y && r.status!=="취소").length;
    const auto = autoClosedList(y);
    if(auto.length) items.push(["", `어제 예약 ${yAll}건 중 ${auto.length}건 자동 방문 처리`,
      "노쇼·취소가 있었다면 눌러서 수정하세요", `openPick('auto')`]);
  }

  return items;
}
function openCheck(){ view.form={type:"check"}; render(); }
function sheetCheck(){
  const items = checkItems(view.date);   /* 세부(sub)는 안 보임 — 제목만, 누르면 목록(재아 09-17) */
  const body = items.length
    ? `<div class="alerts">${items.map(([c,t,sub,act])=>`
        <button class="alert ${c}" onclick="${act}">
          <span class="a-t">${esc(t)}</span>
          <span class="a-go">&rsaquo;</span>
        </button>`).join("")}</div>`
    : `<div class="empty">지금 확인할 항목이 없습니다.</div>`;
  return `
    ${sheetHead(`확인 · ${dateLabel(view.date)}`)}
    <div class="checkbox-scroll">${body}</div>
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}

/* 확인 필요 항목을 눌렀을 때 뜨는 목록 */
function openPick(kind){ view.form={type:"pick", kind}; render(); }
function sheetPick(){
  const s = store(), d = view.date, today = todayStr();
  const kind = view.form.kind;
  const conf = {
    allergy:{title:"알러지 확인", pick:r=>r.allergy, note:"주방에 전달됐는지 확인하세요."},
    menu:{title:"메뉴 확인", pick:r=>r.menuType==="확인 필요", note:"방문 전 연락해 코스·세트를 확정하세요."},
    noshow:{title:"노쇼 이력 손님", pick:r=>!!noshowOf(r.phone), note:"확인 전화를 돌리면 노쇼가 줄어듭니다."},
    warn:{title:"경고 예약", pick:r=>resWarn(r).length>0, note:""},
    confirmed:{title:"확정 예약", pick:r=>true, note:""},
    better:{title:"자리 개선 가능", pick:r=>isTablePref(r.seatPref) && (r.tentativeSplit || !r.tentativeRoomId) && floorFit(prefFloor(r.seatPref), r.date, r.time, pplOf(r), r.id).state==="ok", note:"취소 등으로 자리가 났습니다. 다시 계산되면 한 자리로 배정됩니다."},
    request:{title:"요청사항 있는 예약", pick:r=>!!(r.request||"").trim(), note:""},
    memo:{title:"메모 있는 예약", pick:r=>!!(r.memo||"").trim(), note:""},
    changed:{title:"오늘 변동", pick:r=>!!changeTag(r), note:""},
    group:{title:"단체 손님", pick:r=>pplOf(r) >= (store().settings.groupSize||8),
           note:"상차림과 인력 배치를 미리 준비하세요. 기준 인원은 설정에서 바꿀 수 있습니다."},
    auto:{title:"어제 자동 방문 처리", pick:null, note:""},
    blocked:{title:"사용 중지 좌석에 잡힌 예약", pick:null, note:"그 좌석은 그 기간 쓸 수 없습니다. 미리 연락해 다른 자리로 옮기거나 사용 중지를 풀어 주세요. 오늘 이후 전부입니다."}
  }[kind];
  const list = kind==="auto"
    ? autoClosedList(shiftDate(today,-1))
    : kind==="blocked"
    ? s.reservations.filter(r=>r.date>=today && holdsSeat(r) && resBlocked(r)).sort((a,b)=>a.date.localeCompare(b.date)||a.time.localeCompare(b.time))
    : s.reservations.filter(r=>r.date===d && (kind==="changed" || r.status==="확정") && conf.pick(r))
        .sort((a,b)=>a.time.localeCompare(b.time));
  const rows = list.length ? list.map(r=>`
    <button class="rowitem tap" onclick="openMark('${r.id}')">
      <span class="time-col">${esc(r.time)}</span>
      <span class="grow"><span class="t">${esc(r.name)}${tierTag(r)}</span>
        <span class="s">${kind==="warn"?`<span class="rust">${esc(resWarn(r).join(", "))}</span> · `:""}${kind==="blocked"?`${dateLabel(r.date)} · `:""}${pplText(r)}${r.phone?` · ${esc(r.phone)}`:""}${
          kind==="blocked"&&resBlocked(r)?` · ${esc(blockLabelText(resBlocked(r).blk))}`:""}${
          kind==="allergy"&&r.allergy?` · ${esc(r.allergy)}`:""}${
          kind==="noshow"&&noshowOf(r.phone)?` · 노쇼 ${noshowOf(r.phone).count}회`:""}${

          kind==="group"&&r.menuType==="코스"?` · 코스·세트`:""}</span></span>
    </button>`).join("") : `<div class="empty">해당 예약이 없습니다.</div>`;   /* 좌석 알약은 뺐음 — 목록에서는 이름·시각이면 충분(재아 09-17) */
  return `
    ${sheetHead(kind==="blocked" ? conf.title : `${conf.title} · ${kind==="auto"?dateLabel(shiftDate(today,-1)):dateLabel(d)}`)   /* 사용 중지 예약은 날짜와 무관하게 전부 모음 */}
    <div class="card" style="margin-bottom:12px">${rows}</div>
    ${conf.note ? `<p class="f-note">${conf.note}</p>` : ""}
    <div class="sheet-actions"><button class="btn primary" onclick="closeSheet()">닫기</button></div>`;
}
