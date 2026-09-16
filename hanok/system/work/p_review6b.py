# -*- coding: utf-8 -*-
"""재아 요청(2026-09-17) 시스템 쪽 — 홈페이지 예약:
   ① 대기 중인 요청을 타임라인에 연회색 블록으로(확정 전 자리 확보). 남은 자리 계산(availOfDay)에도 찬 것으로
   ② 켤 때 대기 건이 있으면 팝업. 문구 "새 홈페이지 예약 N건 / N건의 예약이 접수되었습니다."
   ③ 목록: 접수 순(오래된 것 위), '17시간 전 접수' 삭제, "6시간 38분 후 만료" / 12시간 안이면 빨간 "N시간 M분 남음"
   ④ 줄 순서: 날짜·시간 → 인원 → 룸/테이블 → 메뉴. 경고 '테이블 없음'/'룸 없음'. 알약 작게
   ⑤ 거절: 사유 고르기·직접 입력·생략 되는 시트
   ⑥ 승인 = '예약 확정' 바로 등록. 경고 있으면 팝업 → 그래도 확정 / 예약 창에서 자리 고르기(그 단계로)
   ⑦ 알러지 칸(requests.allergy) 연동
   ⑧ 마법사 '한 화면으로 입력'(빠른 입력) 진입 삭제
   ⑨ 확인 목록에 '사용 중지 좌석에 잡힌 예약' — 날짜 상관없이 오늘 이후 전부 """
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep

s = load("css/05-dash.css")
s = rep(s, '''.blk.tent{background-image:repeating-linear-gradient(-45deg, rgba(255,255,255,.34) 0 4px, transparent 4px 10px); border:1px dashed rgba(255,255,255,.75)}''',
'''.blk.tent{background-image:repeating-linear-gradient(-45deg, rgba(255,255,255,.34) 0 4px, transparent 4px 10px); border:1px dashed rgba(255,255,255,.75)}
/* 확정 전 홈페이지 예약 — 연회색, 누르면 그 요청 창. 자리를 미리 잡아 둔 것이라 다른 블록과 같은 자리에 그려집니다 */
.blk.req, .blk.req.tent{background:#E3E0D8; background-image:none; color:#3A3833; border:1px dashed #8C8578}
.blk.req .rq{font-style:normal; font-weight:700; color:var(--rust); font-size:10px}''', 2)
save("css/05-dash.css", s)

s = load("css/03-parts.css")
s = rep(s, '''.tag.blue{background:var(--blue-soft); color:var(--blue); border-color:var(--blue-line)}''',
'''.tag.blue{background:var(--blue-soft); color:var(--blue); border-color:var(--blue-line)}
.tag.sm{padding:1px 6px; font-size:11px; font-weight:600}   /* 목록 줄 안의 작은 꼬리표(홈페이지 예약 경고 등) */
.rj-list{display:flex; flex-direction:column; gap:var(--s8); margin-bottom:var(--s8)}
.rj-list .chk{margin:0}
.rj-list textarea{width:100%}''', 1)
save("css/03-parts.css", s)

# ---------- 마법사: '한 화면으로 입력' 삭제 ----------
s = load("js/16-wizard.js")
s = rep(s, '''    <button class="linkbtn wz-quick" onclick="openQuick()">한 화면으로 입력</button>`;''', '''`;   /* '한 화면으로 입력'(빠른 입력)은 2026-09-17 뺐습니다 — 경고가 안 보여 오히려 불편(재아). openQuick 은 남겨 둠 */''', 1)
save("js/16-wizard.js", s)

# ---------- 확인 목록: 사용 중지 좌석에 잡힌 예약(오늘 이후 전부) ----------
s = load("js/09-sms.js")
s = rep(s, '''  const un = list.filter(isUnassigned);   /* 테이블 예약은 층이 자리 — 미배정 아님 */''',
'''  /* 사용 중지 좌석에 잡힌 예약 — 날짜 상관없이 오늘 이후 전부. 미리 연락하거나 자리를 옮겨야 하니(재아) */
  const blk = s.reservations.filter(r=>r.date>=today && holdsSeat(r) && resBlocked(r)).sort((a,b)=>a.date.localeCompare(b.date)||a.time.localeCompare(b.time));
  if(blk.length) items.push(["rust", `사용 중지 좌석에 잡힌 예약 ${blk.length}건`,
    blk.slice(0,3).map(r=>`${dateLabel(r.date)} ${r.time} ${r.name} · ${resSeatLabel(r)}`).join(", "), `openPick('blocked')`]);

  const un = list.filter(isUnassigned);   /* 테이블 예약은 층이 자리 — 미배정 아님 */''', 1)
s = rep(s, '''    auto:{title:"어제 자동 방문 처리", pick:null, note:""}
  }[kind];
  const list = kind==="auto"
    ? autoClosedList(shiftDate(today,-1))
    : s.reservations.filter(r=>r.date===d && (kind==="changed" || r.status==="확정") && conf.pick(r))
        .sort((a,b)=>a.time.localeCompare(b.time));''',
'''    auto:{title:"어제 자동 방문 처리", pick:null, note:""},
    blocked:{title:"사용 중지 좌석에 잡힌 예약", pick:null, note:"그 좌석은 그 기간 쓸 수 없습니다. 미리 연락해 다른 자리로 옮기거나 사용 중지를 풀어 주세요. 오늘 이후 전부입니다."}
  }[kind];
  const list = kind==="auto"
    ? autoClosedList(shiftDate(today,-1))
    : kind==="blocked"
    ? s.reservations.filter(r=>r.date>=today && holdsSeat(r) && resBlocked(r)).sort((a,b)=>a.date.localeCompare(b.date)||a.time.localeCompare(b.time))
    : s.reservations.filter(r=>r.date===d && (kind==="changed" || r.status==="확정") && conf.pick(r))
        .sort((a,b)=>a.time.localeCompare(b.time));''', 1)
s = rep(s, '''      <span class="time-col">${esc(r.time)}</span>
      <span class="grow"><span class="t">${esc(r.name)}</span>
        <span class="s">${pplText(r)}${r.phone?` · ${esc(r.phone)}`:""}${''',
'''      <span class="time-col">${esc(r.time)}</span>
      <span class="grow"><span class="t">${esc(r.name)}</span>
        <span class="s">${kind==="blocked"?`${dateLabel(r.date)} · `:""}${pplText(r)}${r.phone?` · ${esc(r.phone)}`:""}${
          kind==="blocked"&&resBlocked(r)?` · ${esc(blockLabelText(resBlocked(r).blk))}`:""}${''', 1)
save("js/09-sms.js", s)
print("ok")
