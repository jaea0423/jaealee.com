"""v3 3차 — 문구·디자인 개편.
   문구 원칙: 손님께 읽어 주는 말은 큰따옴표 + 전화로 실제 하는 말투. 직원에게 알리는 말은 짧게.
   경고는 전부 "제목 - 세부" 꼴 (재아가 정한 시간 경고 5종과 같은 꼴)."""
import os, sys, io
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "index.html")
s = io.open(SRC, encoding="utf-8").read()
n_ok = 0
def rep(old, new, count=1):
    global s, n_ok
    c = s.count(old)
    if c != count:
        print("!! 치환 실패 (%d번 발견, %d번 기대):\n%s" % (c, count, old[:200])); sys.exit(1)
    s = s.replace(old, new); n_ok += 1

# ---------- 질문 (손님께 읽어 주는 말은 전화 말투로) ----------
rep('''  "어떤 경로로 들어온 예약인가요?",
  "\\u201C예약 원하시는 날짜와 시간 말씀해 주시겠습니까?\\u201D",
  "\\u201C총 방문 인원수 말씀해 주시겠습니까?\\u201D",
  "\\u201C원하시는 좌석 있으신가요?\\u201D",
  "\\u201C식사는 어떻게 준비할까요?\\u201D",
  "\\u201C예약자 성함과 전화번호 말씀해 주시겠습니까?\\u201D",
  "\\u201C추가로 요청하실 사항 있으신가요?\\u201D"''',
'''  "어떤 경로로 온 예약인가요?",
  "\\u201C날짜와 시간은 언제로 해 드릴까요?\\u201D",
  "\\u201C몇 분이서 오세요?\\u201D",
  "\\u201C홀과 룸 중 어디로 해 드릴까요?\\u201D",
  "\\u201C식사는 코스로 준비해 드릴까요?\\u201D",
  "\\u201C예약자 성함과 연락처 부탁드립니다.\\u201D",
  "\\u201C알러지나 따로 요청하실 사항 있으세요?\\u201D"''')
# 질문 위에 '누구에게 하는 말인지' 작은 표시 — 큰따옴표 질문은 손님께, 아니면 직원 확인
rep('''      <div class="wz-q"><h2>${WZ_STEPS[WZ.step]}</h2>''',
'''      <div class="wz-q"><div class="wz-eyebrow">${WZ_STEPS[WZ.step].charAt(0)==="\\u201C"?"손님께 여쭤 보세요":"직원 확인"}</div>
        <h2>${WZ_STEPS[WZ.step]}</h2>''')
# 아래 버튼
rep('''      ${last?`<button class="btn ghost lg" onclick="wzSubmit()">건너뛰기 · 바로 등록</button>`:""}''',
    '''      ${last?`<button class="btn ghost lg" onclick="wzSubmit()">바로 등록</button>`:""}''')
rep('''        ${last?"예약 등록하기":"다음"}''', '''        ${last?"예약 등록":"다음"}''')

# ---------- 0단계 ----------
rep('''    ["전화 예약","전화 예약",""],
    ["네이버 예약","네이버 예약",""],
    ["기타","기타",""]''',
'''    ["전화 예약","전화 예약","가게로 걸려 온 전화"],
    ["네이버 예약","네이버 예약","네이버에서 들어온 예약"],
    ["기타","기타","지인 소개 · 대면 · 그 밖"]''')
rep('''<div class="lb">어떤 경로인가요?</div>''', '''<div class="lb">경로</div>''')
rep('''        <div class="f-note">예약 내역에만 참고용으로 표시됩니다.</div>''',
    '''        <div class="f-note">예약 내역에 참고로만 남습니다</div>''')

# ---------- 1단계 ----------
rep('''      <div class="lbl" style="margin-bottom:8px">${WZ.date?dateLabel(WZ.date):"날짜를 먼저 선택하세요"} · 시간 선택</div>''',
    '''      <div class="lbl" style="margin-bottom:8px">${WZ.date?dateLabel(WZ.date):"날짜를 먼저 고르세요"} · 시</div>''')
rep('''<span class="lbl">분 단위 조절</span><span class="mnow">${curH===null?"시각을 먼저 선택하세요":hm(WZ.time)}</span>''',
    '''<span class="lbl">분</span><span class="mnow">${curH===null?"시를 먼저 고르세요":hm(WZ.time)}</span>''')
rep('''  if(dh.closed) return [`휴무일입니다 (${dh.note||""})`];
  if(inBreak(date, time)) return ["브레이크입니다"];
  if(toMin(time) < toMin(dh.open) || toMin(time) >= toMin(dh.close)) return ["영업시간이 아닙니다"];''',
'''  if(dh.closed) return [`휴무일${dh.note?` - ${dh.note}`:""}`];
  if(inBreak(date, time)) return ["브레이크입니다"];
  if(toMin(time) < toMin(dh.open) || toMin(time) >= toMin(dh.close)) return ["영업시간 아님"];''')
rep('''      if(t > toMin(dh.bs) - buf) out.push(`브레이크 ${buf}분 전 이후 입장입니다`);''',
    '''      if(t > toMin(dh.bs) - buf) out.push(`브레이크 임박 - ${buf}분 전 이후 입장`);''')
rep('''    if(WZ.date < todayStr()) out.push("이미 지난 날짜입니다");
    if(WZ.time) out.push.apply(out, timeWarns(WZ.date, WZ.time));
    else if(dh.closed) out.push(`휴무일입니다${dh.note?` (${dh.note})`:""}`);''',
'''    if(WZ.date < todayStr()) out.push("지난 날짜");
    if(WZ.time) out.push.apply(out, timeWarns(WZ.date, WZ.time));
    else if(dh.closed) out.push(`휴무일${dh.note?` - ${dh.note}`:""}`);''')
rep('''  if(msg.indexOf("휴무") >= 0) return "휴무";
  if(msg.indexOf("영업시간") >= 0) return "영업 외";''',
'''  if(msg.indexOf("휴무") >= 0) return "휴무";
  if(msg.indexOf("영업시간") >= 0) return "영업 외";
  if(msg.indexOf("지난 날짜") >= 0) return "확인";''')

# ---------- 2단계 ----------
rep('''<button class="pmore ${WZ.customPeople?'on':''}" onclick="wzCustom()">직접 입력</button>''',
    '''<button class="pmore ${WZ.customPeople?'on':''}" onclick="wzCustom()">7명 이상</button>''')
rep('''      <div><div class="t">유아 인원수</div>
        <div class="s">${WZ.infants>=(WZ.people||99)&&WZ.people
          ? "성인이 없습니다. 확인해 주세요."
          : "총원에 포함된 인원입니다."}</div></div>''',
'''      <div><div class="t">유아</div>
        <div class="s">${WZ.infants>=(WZ.people||99)&&WZ.people
          ? "성인이 없습니다"
          : "위 인원에 포함됩니다"}</div></div>''')
rep('''  if(WZ.step===2 && WZ.people && (WZ.infants||0) >= WZ.people) out.push("성인 없이 유아만 있습니다");''',
    '''  if(WZ.step===2 && WZ.people && (WZ.infants||0) >= WZ.people) out.push(`성인이 없음 - 유아만 ${WZ.infants}명`);''')

# ---------- 3단계 ----------
rep('''      <span class="sc">${h.total}테이블 중 <b>${h.used+h.tentUsed}</b> 사용 · 남은 ${h.left}</span>
      <span class="sc2">${plan?`${total}명 → ${plan}`:`${total}명 앉힐 자리 없음`}</span>''',
'''      <span class="sc">남은 테이블 <b>${h.left}</b> / ${h.total}</span>
      <span class="sc2">${plan?`${total}명 → ${plan}`:`${total}명 자리 없음`}</span>''')
rep('''      <span class="lbl-note">정원 기준 : ${seatCountsInfants()?"유아 포함 총원":"유아 제외 성인 수"}</span></div>''',
    '''      <span class="lbl-note">정원은 ${seatCountsInfants()?"유아 포함":"유아 제외 성인"} 기준</span></div>''')
rep('''    <div class="lbl" style="margin-top:18px">정하지 않고 접수</div>''',
    '''    <div class="lbl" style="margin-top:18px">좌석 미정으로 접수</div>''')
rep('''      if(rs.state==="blocked") out.push(`다른 예약과 1시간 안에 겹칩니다${who?` (${who})`:""}`);
      else if(rs.state==="warn") out.push(`다른 예약과 체류 시간이 겹칩니다${who?` (${who})`:""}`);
      const cnt = seatCountsInfants() ? WZ.people : adultCount(WZ.people, WZ.infants);
      if(cnt > room.capacity) out.push(`${seatLabel(room.id)} 정원 ${room.capacity}명을 넘습니다`);
      if(cnt < roomMin(room)) out.push(`${seatLabel(room.id)} 최소 인원 ${roomMin(room)}명에 못 미칩니다`);
      const bk = blockedAt(room, WZ.date, WZ.time);
      if(bk) out.push(`${seatLabel(room.id)}은 이 시각에 사용 중지입니다${bk.note?` — ${bk.note}`:""}`);
    }
    if(room && room.type==="hall"){
      const h = hallStatus(WZ.date, WZ.time, WZ.seat);
      if(!hallFits(h, WZ.people)) out.push("홀에 남은 자리가 부족합니다");
    }''',
'''      if(rs.state==="blocked") out.push(`1시간 안에 다른 예약${who?` - ${who}`:""}`);
      else if(rs.state==="warn") out.push(`식사 시간이 겹침${who?` - ${who}`:""}`);
      const cnt = seatCountsInfants() ? WZ.people : adultCount(WZ.people, WZ.infants);
      if(cnt > room.capacity) out.push(`정원 초과 - ${seatLabel(room.id)} 최대 ${room.capacity}명`);
      if(cnt < roomMin(room)) out.push(`최소 인원 미달 - ${seatLabel(room.id)} ${roomMin(room)}명부터`);
      const bk = blockedAt(room, WZ.date, WZ.time);
      if(bk) out.push(`사용 중지 - ${seatLabel(room.id)}${bk.note?` · ${bk.note}`:""}`);
    }
    if(room && room.type==="hall"){
      const h = hallStatus(WZ.date, WZ.time, WZ.seat);
      if(!hallFits(h, WZ.people)) out.push(`자리 부족 - ${seatLabel(room.id)} 남은 테이블 ${h.left}`);
    }''')
rep('''      const who = rs.hits.map(x=>`${hm(x.time)} ${x.name} 손님 ${pplText(x)}`).join(", ");''',
    '''      const who = rs.hits.map(x=>`${hm(x.time)} ${x.name} ${pplText(x)}`).join(", ");''')

# ---------- 4단계 ----------
rep('''    ? [["코스","코스","코스 구성을 선택합니다"],
       ["해당 없음","해당 없음","일반 주문"]]
    : [["코스","코스","코스 구성을 선택합니다"],
       ["코스 상당","코스 상당 식사","코스에 준하는 주문"],
       ["확인 필요","확인 필요","코스 이용 여부 확인 필요"],
       ["해당 없음","해당 없음","일반 주문"]];''',
'''    ? [["코스","코스","구성을 고릅니다"],
       ["해당 없음","해당 없음","단품 주문"]]
    : [["코스","코스","구성을 고릅니다"],
       ["코스 상당","코스 상당 식사","코스에 준하는 주문"],
       ["확인 필요","확인 필요","방문 전에 확인"],
       ["해당 없음","해당 없음","단품 주문"]];''')
rep('''        ${WZ.courseUndecided ? "코스 미정 — 방문 전 확정" : (n?`선택: ${esc(courseSummary(WZ.courses))}`:"코스 구성을 선택하세요")}''',
    '''        ${WZ.courseUndecided ? "코스 미정 · 방문 전 확정" : (n?`${esc(courseSummary(WZ.courses))}`:"구성을 고르세요")}''')
rep('''          코스 미정 — 코스는 이용하지만 아직 정하지 못함''', '''          코스 미정 · 이용은 하지만 아직 못 정함''')
rep('''            ${short?`<div class="ct-warn">성인 ${ad}명보다 ${ad-n}명 적습니다</div>`:""}
            ${over?`<div class="ct-warn">성인 ${ad}명보다 ${n-ad}명 많습니다</div>`:""}''',
'''            ${short?`<div class="ct-warn">코스 부족 - 성인보다 ${ad-n}명 적음</div>`:""}
            ${over?`<div class="ct-warn">코스 초과 - 성인보다 ${n-ad}명 많음</div>`:""}''')
rep('''      if(WZ.menuType==="해당 없음") out.push("룸 예약에 코스 이용 예정 손님이 아닙니다");
      if(WZ.menuType==="확인 필요") out.push("룸 손님 코스 이용 여부가 아직 확인되지 않았습니다");
      if(WZ.menuType==="코스" && !WZ.courseUndecided && n>0 && n<adults)
        out.push(`코스 ${n}인분이 성인 ${adults}명보다 적습니다`);
      if(WZ.menuType==="코스" && !WZ.courseUndecided && n>adults)
        out.push(`코스 ${n}인분이 성인 ${adults}명보다 많습니다`);''',
'''      if(WZ.menuType==="해당 없음") out.push("룸인데 코스가 아님");
      if(WZ.menuType==="확인 필요") out.push("룸인데 코스 여부 미확인");
      if(WZ.menuType==="코스" && !WZ.courseUndecided && n>0 && n<adults)
        out.push(`코스 부족 - ${n}인분 / 성인 ${adults}명`);
      if(WZ.menuType==="코스" && !WZ.courseUndecided && n>adults)
        out.push(`코스 초과 - ${n}인분 / 성인 ${adults}명`);''')
rep('''  if(offNames.length) out.push(`이 시간에 팔지 않는 코스입니다 — ${offNames.join(", ")}`);
  if(picked.length >= 2) out.push(`코스가 ${picked.length}종류입니다 — 한 테이블은 코스를 통일합니다`);''',
'''  if(offNames.length) out.push(`이 시간엔 없는 코스 - ${offNames.join(", ")}`);
  if(picked.length >= 2) out.push(`코스 ${picked.length}종류 - 한 테이블은 하나로`);''')

# ---------- 5단계 ----------
rep('''        <button class="nonebtn sm warn ${WZ.phoneNone?'on':''}" onclick="wzPhoneNone()">해당 없음</button>''',
    '''        <button class="nonebtn sm warn ${WZ.phoneNone?'on':''}" onclick="wzPhoneNone()">번호 없음</button>''')
rep('''    if(WZ.phoneNone) out.push("전화번호가 입력되지 않았습니다");
    else if(WZ.phone && WZ.phone.replace(/\\D/g,"").length < 9)
      out.push("올바른 전화번호가 입력되지 않았습니다");
    const ns = WZ.phone ? noshowOf(WZ.phone) : null;
    if(ns) out.push(`이 번호로 노쇼 ${ns.count}회 기록이 있습니다`);''',
'''    if(WZ.phoneNone) out.push("전화번호 없음");
    else if(WZ.phone && WZ.phone.replace(/\\D/g,"").length < 9)
      out.push("전화번호가 짧음");
    const ns = WZ.phone ? noshowOf(WZ.phone) : null;
    if(ns) out.push(`노쇼 이력 - ${ns.count}회`);''')
rep('''  return `<div class="ns-hint">이 번호로 노쇼 ${ns.count}회 기록이 있습니다</div>`;''',
    '''  return `<div class="ns-hint">노쇼 이력 ${ns.count}회</div>`;''')

# ---------- 6단계 ----------
rep('''      ${chairDefaultInfants()?`<div class="f-note">유아 ${WZ.infants||0}명 기준으로 자동 입력되었습니다.</div>`:""}''',
    '''      <div class="f-note">${chairDefaultInfants()?`유아 ${WZ.infants||0}명 기준 자동 입력`:"&nbsp;"}</div>''')
rep('''    <label class="f big"><div class="lb">기타 요청사항</div>''', '''    <label class="f big"><div class="lb">요청사항</div>''')
rep('''    <label class="f big"><div class="lb">메모 <span class="lbl-note">우리끼리 보는 기록입니다</span></div>''',
    '''    <label class="f big"><div class="lb">메모 <span class="lbl-note">우리끼리만 봅니다</span></div>''')
rep('''      <div class="lbl" style="margin-bottom:8px">확인</div>''',
    '''      <div class="lbl" style="margin-bottom:8px">이대로 등록됩니다</div>''')
rep('''    if((WZ.chairs||0) > (WZ.infants||0)) out.push("유아용 의자가 유아 수보다 많습니다");
    if((WZ.chairs||0) < (WZ.infants||0)) out.push("유아용 의자가 유아 수보다 적습니다");''',
'''    if((WZ.chairs||0) > (WZ.infants||0)) out.push(`의자가 유아보다 많음 - 의자 ${WZ.chairs||0} / 유아 ${WZ.infants||0}`);
    if((WZ.chairs||0) < (WZ.infants||0)) out.push(`의자가 유아보다 적음 - 의자 ${WZ.chairs||0} / 유아 ${WZ.infants||0}`);''')

# ---------- 완료 화면 ----------
rep('''          <b>${esc(r.name)}</b> 손님<br>예약 접수되었습니다.''', '''          <b>${esc(r.name)}</b> 손님<br>예약이 접수됐습니다''')
rep('''          <button class="btn lg" onclick="openWizard('${r.date}')">추가 예약</button>''',
    '''          <button class="btn lg" onclick="openWizard('${r.date}')">예약 하나 더</button>''')

# ---------- 대시보드 지표 문구 ----------
rep('''<div class="k">룸 미배정</div><div class="s">${unassigned?"눌러서 배정":"모두 배정됨"}</div>''',
    '''<div class="k">룸 미배정</div><div class="s">${unassigned?"눌러서 열기":"모두 배정됨"}</div>''')
rep('''<div class="k">경고 예약</div><div class="s">${warnCnt?"눌러서 확인":"이상 없음"}</div>''',
    '''<div class="k">경고 예약</div><div class="s">${warnCnt?"눌러서 열기":"이상 없음"}</div>''')
rep('''<div class="k">확인 필요</div><div class="s">${checkCnt?"눌러서 확인":"모두 확인됨"}</div>''',
    '''<div class="k">확인 필요</div><div class="s">${checkCnt?"눌러서 열기":"모두 확인됨"}</div>''')

# ---------- CSS ----------
rep('''/* 코스 칸 + 모서리 − (처음 누르면 성인 수만큼 채워지므로 줄이는 길이 필요합니다) */''',
'''/* 질문 위 작은 표시 — 손님께 읽는 말인지, 직원이 확인할 것인지 */
.wz-eyebrow{font-size:var(--fs-label); font-weight:700; letter-spacing:.08em; color:var(--text-3); margin-bottom:var(--s8)}
/* 코스 칸 + 모서리 − (처음 누르면 성인 수만큼 채워지므로 줄이는 길이 필요합니다) */''')

io.open(SRC, "w", encoding="utf-8", newline="\n").write(s)
print("3차 패치 완료:", n_ok, "곳")
