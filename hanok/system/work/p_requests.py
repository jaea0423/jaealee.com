# -*- coding: utf-8 -*-
"""예약 대기(손님 요청) 흉내 — 11b-requests.js 를 화면에 잇습니다.
   상단바 '예약 대기 N' · 확인 목록 첫 줄 · 시트 등록 · 마법사 등록 뒤 확정 처리 · 문자 흉내 기록 헬퍼."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep, js_check

# 11b 안의 헬퍼 이름을 실제 것에 맞춤: smsFreeLog(to, text) 를 새로 만들어 기록만 남김. toast → showToast
s = load("js/11b-requests.js")
s = s.replace('if(q) smsFreeLog && smsFreeLog(q.phone,', 'if(q) smsMockSend(q.phone, q.name,')
s = s.replace('if(typeof smsFreeLog === "function") smsFreeLog(q.phone,', 'smsMockSend(q.phone, q.name,')
s = s.replace('toast(`거절했습니다 · 문자 흉내`);', 'showToast("거절했습니다 · 문자 흉내");')
s = s.replace('toast("흉내 요청 4건 넣음"); render();', 'showToast("흉내 요청 4건 넣음"); render();')
s += '''
/* 문자 흉내 기록 — '보낸 문자' 목록(smsFreeLog)에 남깁니다. 실제 발송은 업체 연동 뒤 */
function smsMockSend(to, name, text){
  const st = store().settings;
  st.smsFreeLog = [{ at:new Date().toISOString(), to, name, text }].concat(st.smsFreeLog || []).slice(0, 50);
  if(typeof mirrorDraft === "function") mirrorDraft("smsFreeLog");
  logEvent("문자 보내기(흉내)", `${to} ${name} ${text.slice(0, 40)}`);
  saveData();
}
'''
save("js/11b-requests.js", s)

# 시트 등록
s = load("js/15-sheets.js")
s = rep(s, 'sched:sheetSchedule, ovr:sheetOverride, blocks:sheetBlocks', 'sched:sheetSchedule, ovr:sheetOverride, blocks:sheetBlocks, reqs:sheetRequests, req:sheetRequest')
s = rep(s, '(view.form.type==="search" ? " sheet-tall" : "")', '((view.form.type==="search" || view.form.type==="reqs") ? " sheet-tall" : "")')
save("js/15-sheets.js", s)

# 마법사 등록 뒤 → 요청 확정
s = load("js/16-wizard.js")
s = rep(s, '''  createReservation(rec);
  /* 6차 전에는 view.date = rec.date 로 그 날짜로 점프했습니다.''', '''  createReservation(rec);
  reqAfterRegister(rec);   /* 홈페이지 요청을 승인해 온 것이면 요청을 '확정' 으로 (11b) */
  /* 6차 전에는 view.date = rec.date 로 그 날짜로 점프했습니다.''')
save("js/16-wizard.js", s)

# 상단바: 예약 검색 옆 '예약 대기 N' (폰은 아이콘+숫자)
s = load("js/06-modal.js")
s = rep(s, '''          <button class="tvbtn icon b-search" onclick="openSearch()" title="예약 검색" aria-label="예약 검색">${ICON.search}</button>` : `''',
           '''          <button class="tvbtn icon b-search" onclick="openSearch()" title="예약 검색" aria-label="예약 검색">${ICON.search}</button>
          <button class="tvbtn icon b-reqs ${reqPending().length?'has':''}" onclick="openRequests()" title="예약 대기" aria-label="예약 대기">${ICON.inbox}<i class="cnt">${reqPending().length}</i></button>` : `''')
s = rep(s, '''          <button class="tvbtn b-search" onclick="openSearch()">예약 검색</button>
          <button class="tvbtn accent b-add" onclick="openWizard()">＋ 예약 등록</button>`}''',
           '''          <button class="tvbtn b-search" onclick="openSearch()">예약 검색</button>
          <button class="tvbtn b-reqs ${reqPending().length?'has':''}" onclick="openRequests()">예약 대기<i class="cnt">${reqPending().length}</i></button>
          <button class="tvbtn accent b-add" onclick="openWizard()">＋ 예약 등록</button>`}''')
save("js/06-modal.js", s)

# 아이콘
s = load("js/03-util.js")
s = rep(s, "  search:'<svg viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"6.5\"/><path d=\"M20 20l-4.2-4.2\"/></svg>',",
           "  search:'<svg viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"6.5\"/><path d=\"M20 20l-4.2-4.2\"/></svg>',\n  inbox:'<svg viewBox=\"0 0 24 24\"><path d=\"M4 13l2-8h12l2 8v6H4z\"/><path d=\"M4 13h5l1.5 2h3L15 13h5\"/></svg>',")
save("js/03-util.js", s)

# 확인 목록 첫 줄
s = load("js/09-sms.js")
s = rep(s, '''  const items = [];

  const un = list.filter(isUnassigned);''', '''  const items = [];

  /* 홈페이지에서 들어온 손님 요청 — 날짜와 상관없이 대기 중이면 맨 위에 */
  const pend = reqPending();
  if(pend.length) items.push(["blue", `예약 대기 ${pend.length}건`,
    pend.slice(0,3).map(q=>`${dateLabel(q.date)} ${hm(q.time)} ${q.name}`).join(", "), `openRequests()`]);

  const un = list.filter(isUnassigned);''')
save("js/09-sms.js", s)

# CSS: 상단바 숫자 배지
c = load("css/04-layout.css")
c = rep(c, '.tvbtn{border-radius:var(--r-sm)}', '''.tvbtn{border-radius:var(--r-sm)}
/* 예약 대기 단추의 건수 — 0이면 흐리게, 있으면 파란 배지 */
.tvbtn.b-reqs .cnt{font-style:normal; margin-left:6px; min-width:18px; height:18px; padding:0 5px; border-radius:9px; background:rgba(255,255,255,.14); font-size:12px; line-height:18px; text-align:center}
.tvbtn.b-reqs.has .cnt{background:#3F6C9E; color:#fff}
.tvbtn.icon.b-reqs .cnt{position:absolute; top:-4px; right:-4px; margin:0; min-width:16px; height:16px; line-height:16px; font-size:11px}
.tvbtn.icon.b-reqs{position:relative; overflow:visible}''')
save("css/04-layout.css", c)
js_check()
print("예약 대기 흉내 연결 끝")
