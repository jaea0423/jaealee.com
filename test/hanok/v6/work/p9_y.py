# -*- coding: utf-8 -*-
"""8차-Y — 재아 목록 8차(뒷부분): 인트로 더 끊기게(글자 즉시), '⊕ 공간 나뉨', 잠정+변동 블록 빗금은 파란 뒤에만,
   마법사 달력 휴무 흐림(선택은 됨), 시각 글자 '오후 5:00', 1명 타일은 보이되 경고, 예약 등록은 날짜 미선택으로 시작,
   2인석 경고를 좌석 단계에서, 4명 이하 테이블도 상세에 '추천 좌석'(참고)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- 인트로: 글자는 한 번에, 창호·먹선은 단계 수를 줄여 더 뚝뚝 ----------
s = R(s, """.intro .ic{display:inline-block; transition:clip-path .36s steps(4,end), color .01s steps(1,end)}""",
         """.intro .ic{display:inline-block; transition:none}   /* 8차-Y(재아): 글자는 한 번에 바뀝니다 — 왼쪽부터 드러나는 것도 '부드러움' */""")
s = R(s, """  transition:opacity .01s steps(1,end), transform .9s steps(5,end)}""",
         """  transition:opacity .01s steps(1,end), transform .6s steps(3,end)}""")
s = R(s, """.intro-w:after{content:""; display:block; width:0; height:3px; margin:.3em auto 0; background:#241E1A; transition:width .8s steps(5,end) .2s}""",
         """.intro-w:after{content:""; display:block; width:0; height:3px; margin:.3em auto 0; background:#241E1A; transition:width .6s steps(3,end) .2s}""")
s = R(s, """  transform:translateX(-100%); animation:intro-scan 1.6s steps(8,end) .2s 1 forwards}""",
         """  transform:translateX(-100%); animation:intro-scan 1.2s steps(6,end) .2s 1 forwards}""")

# ---------- 범례 ----------
s = R(s, """<span class="tl-legend sym" title="룸 합침인데 공간이 나뉨(원탁) — 손님 확인">⊕ 나뉨</span>""",
         """<span class="tl-legend sym" title="룸 합침인데 공간이 나뉨(원탁) — 손님 확인. '나눠 앉음'(테이블을 못 붙여 따로 앉음)과는 다릅니다">⊕ 공간 나뉨</span>""")

# ---------- 잠정+변동 블록: 파란 앞부분 위에는 빗금이 없게(파랑을 위에, 빗금은 뒤) ----------
s = R(s, """button.blk.tent.changed{background-image:repeating-linear-gradient(-45deg, rgba(255,255,255,.34) 0 4px, transparent 4px 10px), linear-gradient(90deg, #3D8BD9 0, #3D8BD9 48%, rgba(61,139,217,0) 56%)}
button.blk.tent.warned.changed{background-image:repeating-linear-gradient(-45deg, rgba(255,255,255,.34) 0 4px, transparent 4px 10px), linear-gradient(90deg, #3D8BD9 0, #3D8BD9 48%, rgba(61,139,217,0) 56%)}""",
"""/* 8차-Y(재아): 파란 변동 띠를 위에 — 앞부분엔 빗금이 안 보이고, 파랑이 빠지는 뒤쪽에만 빗금 */
button.blk.tent.changed{background-image:linear-gradient(90deg, #3D8BD9 0, #3D8BD9 48%, rgba(61,139,217,0) 56%), repeating-linear-gradient(-45deg, rgba(255,255,255,.34) 0 4px, transparent 4px 10px)}
button.blk.tent.warned.changed{background-image:linear-gradient(90deg, #3D8BD9 0, #3D8BD9 48%, rgba(61,139,217,0) 56%), repeating-linear-gradient(-45deg, rgba(255,255,255,.34) 0 4px, transparent 4px 10px)}""")

# ---------- 마법사 달력: 휴무일 흐리게 + 빗금 (누를 수는 있음 — 사장이 판단) ----------
s = R(s, """    const cls = ["bday","btn-day", WZ.date===ds?"sel":"", ds===today?"today":"",
                 ds<today?"past":"", dow===0?"sun":dow===6?"sat":""].join(" ");""",
"""    const cls = ["bday","btn-day", WZ.date===ds?"sel":"", ds===today?"today":"",
                 ds<today?"past":"", dow===0?"sun":dow===6?"sat":"", hoursFor(ds).closed?"closed":""].join(" ");""")
s = R(s, """.cday.closed{background-image:repeating-linear-gradient(-45deg, rgba(58,56,51,.08) 0 4px, transparent 4px 10px)}""",
""".cday.closed{background-image:repeating-linear-gradient(-45deg, rgba(58,56,51,.08) 0 4px, transparent 4px 10px)}
/* 마법사·수정 달력의 휴무일 — 흐리고 빗금. 누를 수는 있습니다(휴무에도 받을 사정이 있을 수 있어 사장에게 맡김, 8차-Y 재아) */
.btn-day.closed{background-image:repeating-linear-gradient(-45deg, rgba(58,56,51,.10) 0 4px, transparent 4px 10px)}
.btn-day.closed .d{opacity:.4; text-decoration:line-through}
.btn-day.closed.sel .d{opacity:1}""")

# ---------- 시각 글자: '오후 5시 30분' → '오후 5:30' ----------
s = L.replace_fn(s, "hm", """function hm(t){
  /* 8차-Y(재아): 시각 칸과 같은 모양 '오후 5:30'. '5시 30분' 은 길고 칸마다 폭이 달랐습니다 */
  const [h,m]=t.split(":").map(Number);
  const ap = h<12?"오전":"오후";
  const h12 = h%12===0?12:h%12;
  return `${ap} ${h12}:${pad(m||0)}`;
}""")

# ---------- 인원 1명: 타일은 보이되 누르면 경고(2인부터) ----------
s = R(s, """  const tiles = [1,2,3,4,5,6].map(n=>
    `<button class="ptile ${WZ.people===n&&!WZ.customPeople?'on':''}" onclick="wzPeople(${n})">""",
"""  const tiles = [1,2,3,4,5,6].map(n=>
    `<button class="ptile ${WZ.people===n&&!WZ.customPeople?'on':''} ${n===1?'off':''}" onclick="wzPeople(${n})">""")
s = R(s, """function wzPeople(n){
  WZ.people=n; WZ.customPeople=false;""",
"""function wzPeople(n){
  /* 1명 예약은 받지 않습니다(재아: 타일은 보이되 누르면 안내). 1인 규칙은 누님 질문 2번 대기 */
  if(n === 1) return uiAlert("1명 예약은 받지 않습니다", "2명부터 예약할 수 있습니다.", "warn");
  WZ.people=n; WZ.customPeople=false;""")
s = R(s, """.ptile{border:1px solid var(--border-strong); background:var(--surface); padding:var(--s24) 0 var(--s16); display:flex; flex-direction:column; align-items:center; gap:1px; border-radius:var(--r-md)}""",
""".ptile{border:1px solid var(--border-strong); background:var(--surface); padding:var(--s24) 0 var(--s16); display:flex; flex-direction:column; align-items:center; gap:1px; border-radius:var(--r-md)}
.ptile.off{opacity:.4}""")

# ---------- 예약 등록은 날짜를 고르지 않은 상태로 시작 ----------
s = R(s, """<button class="tvbtn accent b-add" onclick="openWizard('${view.date}')">＋ 예약 등록</button>""",
         """<button class="tvbtn accent b-add" onclick="openWizard()">＋ 예약 등록</button>""")
s = R(s, """<button class="fab" onclick="openWizard('${d}')" aria-label="예약 등록">""",
         """<button class="fab" onclick="openWizard()" aria-label="예약 등록">""")
s = R(s, """<button class="btn primary add" onclick="openWizard('${view.date}')">＋ 예약 등록</button>""",
         """<button class="btn primary add" onclick="openWizard()">＋ 예약 등록</button>""")
s = R(s, """    calMonth:(date||view.date).slice(0,7),
    date:date||view.date, time:null,""",
"""    /* 8차-Y(재아): 등록 버튼으로 열면 날짜가 안 골라진 채 시작합니다 — 보고 있던 날짜가 슬쩍 들어가면 헷갈립니다. 달력은 보던 달로 */
    calMonth:(date||view.date).slice(0,7),
    date:date||null, time:null,""")
# 날짜가 없을 때의 1단계 — 시각 칸은 비우고 자리만
s = R(s, """  const dh = hoursFor(WZ.date);
  /* 칸 수는 '이번 주 중 가장 이른 개점 ~ 가장 늦은 마감' 으로 고정합니다.""",
"""  const dh = WZ.date ? hoursFor(WZ.date) : {closed:false, open:"", close:"", bs:"", be:"", lo:""};
  /* 칸 수는 '이번 주 중 가장 이른 개점 ~ 가장 늦은 마감' 으로 고정합니다.""")
s = R(s, """  const range = weekHourRange(WZ.date);""", """  const range = weekHourRange(WZ.date || todayStr());""")
s = R(s, """  const slotCells = slots.filter(t=>!inSess[t] || (dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be))).map(t=>{""",
         """  const slotCells = !WZ.date ? "" : slots.filter(t=>!inSess[t] || (dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be))).map(t=>{""")
s = R(s, """      ${hoursLineHtml(dh)}
      <div class="lbl" style="margin-bottom:8px">${WZ.date?dateLabel(WZ.date):"날짜를 먼저 고르세요"} · 시각</div>
      ${sessionGrid()}""",
"""      ${WZ.date ? hoursLineHtml(dh) : `<div class="hours-line"><span class="hl-c"><i>영업시간</i>—</span><span class="hl-c"><i>브레이크</i>—</span><span class="hl-c"><i>라스트오더</i>—</span></div>`}
      <div class="lbl" style="margin-bottom:8px">${WZ.date?dateLabel(WZ.date):"날짜를 먼저 고르세요"} · 시각</div>
      ${WZ.date ? sessionGrid() : `<div class="empty">왼쪽 달력에서 날짜를 고르면 시각이 나옵니다.</div>`}""")
# slotCells 가 문자열일 때 .join 이 없으므로 — map(...).join("") 뒤를 확인
s = R(s, """      <span class="ap${red}">${h<12?"오전":"오후"}</span>
      <span class="hh${red}">${h%12===0?12:h%12}:${pad(m)}</span>
      ${outside?`<span class="hn muted2">${dh.closed?"휴무":(t<todayOpen?"영업 전":"영업 종료")}</span>`
           :brk?`<span class="hn rust">브레이크</span>`
           :bad?`<span class="hn rust">${esc(shortWarn(probe))}</span>`
           :`<span class="hn">&nbsp;</span>`}
    </button>`;
  }).join("");""",
"""      <span class="ap${red}">${h<12?"오전":"오후"}</span>
      <span class="hh${red}">${h%12===0?12:h%12}:${pad(m)}</span>
      ${outside?`<span class="hn muted2">${dh.closed?"휴무":(t<todayOpen?"영업 전":"영업 종료")}</span>`
           :brk?`<span class="hn rust">브레이크</span>`
           :bad?`<span class="hn rust">${esc(shortWarn(probe))}</span>`
           :`<span class="hn">&nbsp;</span>`}
    </button>`;
  }).join("");
  /* (날짜가 없으면 slotCells 는 빈 문자열) */""")
# wzWarnReason: 날짜 없을 때
s = R(s, """  if(WZ.step===1){
    const dh = hoursFor(WZ.date);
    if(WZ.date < todayStr()) out.push("지난 날짜");""",
"""  if(WZ.step===1 && WZ.date){
    const dh = hoursFor(WZ.date);
    if(WZ.date < todayStr()) out.push("지난 날짜");""")

# ---------- 2인석 경고를 좌석 단계에서 ----------
# 특정 테이블 카드
s = R(s, """    const over = total > seatsMax(ids), under = adults < seatsMin(ids, WZ.date);
    const txt = blocked ? "사용 중지" : state==="free" ? (over?"인원 초과":under?"인원 부족":"이용 가능") : "이용 불가";
    const cls = blocked ? "blocked" : state!=="free" ? state : (over||under ? "warn" : "free");
    const bad = blocked || state!=="free" || over || under;""",
"""    const over = total > seatsMax(ids), under = adults < seatsMin(ids, WZ.date);
    /* 2명이 2인석에 — 좁아서 손님이 싫어합니다. 고르는 단계부터 알립니다(8차-Y 재아). 규칙은 누님 질문 1번 대기 */
    const two = ids.length === 1 && isTable(x) && total > 0 && total <= 2 && (x.seats||4) <= 2;
    const txt = blocked ? "사용 중지" : state==="free" ? (over?"인원 초과":under?"인원 부족":two?"2인석 (좁음)":"이용 가능") : "이용 불가";
    const cls = blocked ? "blocked" : state!=="free" ? state : (over||under||two ? "warn" : "free");
    const bad = blocked || state!=="free" || over || under || two;""")
# 층 카드
s = R(s, """      const fit = WZ.time ? floorFit(fl, WZ.date, WZ.time, total) : null;
      const bad = fit && fit.state !== "ok";
      const txt = !fit ? "시간을 먼저" : fit.state === "ok" ? "자리 있음\"""",
"""      const fit = WZ.time ? floorFit(fl, WZ.date, WZ.time, total) : null;
      /* 2명인데 이 층에 남은 게 2인석뿐이면 미리 알립니다 */
      const twoOnly = fit && fit.state === "ok" && total <= 2 && fit.f && !(fit.f.extra||[]).length && ((seatById(fit.f.id)||{}).seats||4) <= 2;
      const bad = fit && (fit.state !== "ok" || twoOnly);
      const txt = !fit ? "시간을 먼저" : fit.state === "ok" ? (twoOnly ? "2인석만 남음 (좁음)" : "자리 있음")""")

# ---------- 4명 이하 테이블도 상세에서 '추천 좌석'(참고) ----------
s = R(s, """    const st8 = !r.tentativeRoomId ? `<b style="color:var(--rust)">자리 없음</b> — 한 자리 최대 ${floorMaxParty(fl, r.date, r.time, r.id)}명`
              : r.tentativeSplit ? `<b style="color:var(--rust)">나눠 앉음</b> — 테이블 ${seatsOf(r).length}개, 붙일 수 없음`
              : `자리 있음 — 테이블 ${seatsOf(r).length}개`;
    seatPick = `<div class="lbl" style="margin:16px 0 8px">테이블 자리</div>
      <p class="f-note">${esc(floorLabel(fl))} · ${st8}. 어느 테이블에 앉을지는 당일 현장에서 정합니다. 특정 테이블(파셜룸 등)을 잡으려면 '수정' 에서 고르세요.</p>`;""",
"""    const st8 = !r.tentativeRoomId ? `<b style="color:var(--rust)">자리 없음</b> — 한 자리 최대 ${floorMaxParty(fl, r.date, r.time, r.id)}명`
              : r.tentativeSplit ? `<b style="color:var(--rust)">나눠 앉음</b> — 테이블 ${seatsOf(r).length}개, 붙일 수 없음`
              : `자리 있음 — 테이블 ${seatsOf(r).length}개`;
    /* 숨은 잠정 배정을 '추천 좌석' 으로 — 4명 이하도(8차-Y 재아). 어디 앉힐지는 사장 자유, 참고용 */
    const recNames = r.tentativeRoomId ? seatsOf(r).map(id=>{ const x = seatById(id); return x ? x.name : ""; }).filter(Boolean) : [];
    const rec = recNames.length ? `<div class="lbl" style="margin:12px 0 4px">추천 좌석 <span class="lbl-note">참고용 · 당일 사장님이 정합니다</span></div><div class="f-note" style="margin:0">${esc(recNames.join(" + "))}${r.tentativeSplit ? " (나눠 앉음)" : ""}</div>` : "";
    seatPick = `<div class="lbl" style="margin:16px 0 8px">테이블 자리</div>
      <p class="f-note">${esc(floorLabel(fl))} · ${st8}. 어느 테이블에 앉을지는 당일 현장에서 정합니다. 특정 테이블(파셜룸 등)을 잡으려면 '수정' 에서 고르세요.</p>${rec}`;""")

L.js_check(s)
L.save(s)
print("p9_y 적용")
# (추가) 날짜 없을 때 sessionsFor(null) 이 isHoliday 에서 죽던 것
# s = R(s, "  const inSess = {}; sessionsFor(WZ.date).forEach(se=>{", "  const inSess = {}; (WZ.date ? sessionsFor(WZ.date) : []).forEach(se=>{")
