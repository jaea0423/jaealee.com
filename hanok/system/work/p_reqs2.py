# -*- coding: utf-8 -*-
"""홈페이지 예약(구 '예약 대기') 손질: 이름 · 24시간 만료 카운트다운 · 경고는 충돌만 · 새 요청 팝업"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep, js_check

s = load("js/11b-requests.js")
# 이름
s = s.replace("예약 대기(손님 요청) — 흉내", "홈페이지 예약 — 흉내")
s = rep(s, "const REQ_RULE = { minAdults:2, roomMinAdults:5, onlineMax:12 };",
           "const REQ_RULE = { minAdults:2, roomMinAdults:5, onlineMax:12, expireH:24 };   /* expireH: 이 시간 안에 확정·거절이 없으면 자동 취소 */")
s = rep(s, '''function reqPending(){ return REQUESTS.filter(q => q.status === "대기"); }''',
'''/* 24시간 지나면 자동 만료 — 목록을 볼 때마다 정리합니다. 실제 서버에서는 cron 이 하고, 여기서는 흉내 */
function reqExpireAt(q){ return new Date(q.createdAt).getTime() + REQ_RULE.expireH * 3600e3; }
function reqSweep(){
  const now = Date.now();
  REQUESTS.forEach(q => { if(q.status === "대기" && reqExpireAt(q) <= now){ q.status = "만료"; q.reason = "24시간 안에 처리되지 않음"; } });
}
function reqPending(){ reqSweep(); return REQUESTS.filter(q => q.status === "대기"); }
/* "23시간 10분 남음" — 1시간 아래면 분만, 다 되면 '만료 임박' */
function reqLeft(q){
  const ms = reqExpireAt(q) - Date.now(); if(ms <= 0) return "만료";
  const h = Math.floor(ms / 3600e3), m = Math.floor((ms % 3600e3) / 60000);
  return h ? `${h}시간 ${m}분 남음` : `${m}분 남음`;
}''')
# 경고: 사이트가 이미 규칙대로 걸러서 오므로 여기서는 '충돌'만 — 같은 번호 중복, 지난 날짜, 그 사이 자리가 찼는지
s = rep(s, '''/* 사이트 규칙에 걸리는 것 — 거절 사유 후보이기도 합니다 */
function reqWarns(q){
  const out = [];
  if(q.adults < REQ_RULE.minAdults) out.push(`성인 ${REQ_RULE.minAdults}명 미만`);
  if(q.seat === "room" && q.adults < REQ_RULE.roomMinAdults) out.push(`룸은 성인 ${REQ_RULE.roomMinAdults}명부터`);
  if(q.people > REQ_RULE.onlineMax) out.push(`${REQ_RULE.onlineMax}명 초과`);
  if(q.date < todayStr()) out.push("지난 날짜");''',
'''/* 사이트에서 접수할 때는 되던 것이 그 사이에 안 되게 된 것 — '충돌' 만 봅니다(규칙은 사이트가 이미 걸렀음).
   · 그 날 같은 번호로 다른 예약이 들어옴  · 그 사이 자리가 참  · 날짜가 지남 */
function reqWarns(q){
  const out = [];
  if(q.date < todayStr()) out.push("지난 날짜");
  try{
    const seats = store().settings.rooms;
    const free = seats.filter(x => (q.seat === "room" ? isRoom(x) : isTable(x)) && !blockedAt(x, q.date, q.time)
                   && q.people <= seatMax(x) && (q.seat !== "room" || q.people >= roomMin(x, q.date))
                   && roomStatus(q.date, q.time, x.id).state === "free").length;
    if(!free) out.push(q.seat === "room" ? "그 시간에 빈 룸이 없음" : "그 시간에 빈 테이블이 없음");
  }catch(e){}''')
# 목록: 남은 시간 표시, 제목
s = rep(s, '''      <span class="s" style="white-space:nowrap">${reqAgo(q.createdAt)}</span>
    </button>`; }).join("")
    : `<div class="empty">대기 중인 손님 요청이 없습니다.<br><span class="s">홈페이지 예약 창에서 접수하면 여기로 들어옵니다.</span></div>`;
  return `
    ${sheetHead(`예약 대기 · ${list.length}건`)}''',
'''      <span class="s left ${reqExpireAt(q)-Date.now() < 3600e3 ? "soon" : ""}" style="white-space:nowrap; text-align:right">${reqLeft(q)}<br><span class="muted">${reqAgo(q.createdAt)} 접수</span></span>
    </button>`; }).join("")
    : `<div class="empty">처리할 홈페이지 예약이 없습니다.<br><span class="s">손님이 홈페이지에서 접수하면 여기로 들어옵니다. 24시간 안에 확정·거절하지 않으면 자동 취소됩니다.</span></div>`;
  return `
    ${sheetHead(`홈페이지 예약 · ${list.length}건`)}''')
s = rep(s, '''    ${sheetHead("손님 요청")}''', '''    ${sheetHead("홈페이지 예약")}''')
s = rep(s, '''      ${row("접수", `${reqAgo(q.createdAt)} · 홈페이지`)}
    </div>''', '''      ${row("접수", `${reqAgo(q.createdAt)} · <b class="${reqExpireAt(q)-Date.now() < 3600e3 ? "rust" : ""}">${reqLeft(q)}</b>`)}
    </div>''')
s = rep(s, '<p class="f-note" style="margin-top:10px">승인하면 이 내용으로 예약 등록이 열립니다. 좌석을 고르고 등록하면 손님께 확정 문자가 나갑니다.</p>',
           '<p class="f-note" style="margin-top:10px">승인하면 이 내용으로 예약 등록이 열립니다. 좌석을 고르고 등록하면 손님께 확정 문자가 나갑니다. 24시간 안에 처리하지 않으면 자동 취소되고 손님께 안내 문자가 갑니다.</p>')
s = rep(s, '''      <button class="btn primary" onclick="reqAccept('${q.id}')">승인 → 예약 등록</button></div>`;''',
           '''      <button class="btn primary" data-enter onclick="reqAccept('${q.id}')">승인 → 예약 등록</button></div>`;''')
# 새 요청 들어오면 팝업 — 흉내에서는 reqPush 로 넣을 때, 실제로는 서버 갱신에서 새 id 를 보면 부르면 됨
s = rep(s, '''/* 흉내 데이터 — 사이트에서 접수한 것처럼 몇 건 넣습니다 */''',
'''/* 새 홈페이지 예약이 들어오면 화면 위에 알림 — 확인하면 그 창으로, 닫으면 그냥 닫힘.
   실제 연동에서는 갱신(refresh) 때 못 보던 id 가 있으면 reqNotify(newOnes) 를 부르면 됩니다 */
let REQ_SEEN = {};
function reqNotify(list){
  const fresh = list.filter(q => !REQ_SEEN[q.id]); list.forEach(q => REQ_SEEN[q.id] = true);
  if(!fresh.length || view.display) return;
  const q = fresh[0];
  const body = fresh.length === 1
    ? `${dateLabel(q.date)} ${hm(q.time)} · ${reqPeopleText(q)} · ${q.seat==="room"?"룸":"테이블"}\\n${q.name} ${q.phone}`
    : `${fresh.length}건이 들어왔습니다. 가장 빠른 것: ${dateLabel(q.date)} ${hm(q.time)} ${q.name}`;
  uiConfirm(fresh.length === 1 ? "새 홈페이지 예약이 들어왔습니다" : `새 홈페이지 예약 ${fresh.length}건`, body, {ok:"확인하기", cancel:"닫기"})
    .then(ok => { if(ok){ if(WZ) return; view.form = null; fresh.length === 1 ? openRequest(q.id) : openRequests(); } });
}
function reqPush(q){ REQUESTS.push(q); render(); reqNotify([q]); }

/* 흉내 데이터 — 사이트에서 접수한 것처럼 몇 건 넣습니다 */''')
s = rep(s, '''  REQUESTS.push(
    mk({''', '''  const items = [
    mk({''')
s = rep(s, '''    mk({ date:d1, time:"11:30", adults:3, kids:0, people:3, seat:"room", course:"course:위 코스", courseLabel:"위 코스", name:"최민아", phone:"010-4444-7777", request:"" })
  );
  showToast("흉내 요청 4건 넣음"); render();''', '''    mk({ date:d1, time:"11:30", adults:3, kids:0, people:3, seat:"room", course:"course:위 코스", courseLabel:"위 코스", name:"최민아", phone:"010-4444-7777", request:"" })
  ];
  /* 하나는 곧 만료되는 것으로 — 카운트다운 확인용 */
  items[1].createdAt = new Date(now - (REQ_RULE.expireH*3600e3 - 40*60000)).toISOString();
  REQUESTS.push.apply(REQUESTS, items);
  view.form = null; render(); reqNotify(items);''')
s = rep(s, '<button class="btn ghost" onclick="reqSeedDemo()">흉내 요청 넣기</button>', '<button class="btn ghost" onclick="reqSeedDemo()">흉내 예약 넣기</button>')
save("js/11b-requests.js", s)

# 상단·확인 목록·시트 등록 이름
s = load("js/06-modal.js")
s = rep(s, '<button class="tvbtn icon b-reqs ${reqPending().length?\'has\':\'\'}" onclick="openRequests()" title="예약 대기" aria-label="예약 대기">',
           '<button class="tvbtn icon b-reqs ${reqPending().length?\'has\':\'\'}" onclick="openRequests()" title="홈페이지 예약" aria-label="홈페이지 예약">')
s = rep(s, '<button class="tvbtn b-reqs ${reqPending().length?\'has\':\'\'}" onclick="openRequests()">예약 대기<i class="cnt">',
           '<button class="tvbtn b-reqs ${reqPending().length?\'has\':\'\'}" onclick="openRequests()">홈페이지 예약<i class="cnt">')
save("js/06-modal.js", s)
s = load("js/09-sms.js")
s = rep(s, '''  if(pend.length) items.push(["blue", `예약 대기 ${pend.length}건`,''', '''  if(pend.length) items.push(["blue", `홈페이지 예약 ${pend.length}건`,''')
save("js/09-sms.js", s)
c = load("css/04-layout.css")
c = rep(c, "/* 예약 대기 단추의 건수 — 0이면 흐리게, 있으면 파란 배지 */", "/* 홈페이지 예약 단추의 건수 — 0이면 흐리게, 있으면 파란 배지 */")
c += ".rowitem .left.soon, .rust{color:var(--rust)}\n"
save("css/04-layout.css", c)
js_check()
print("reqs2 ok")
