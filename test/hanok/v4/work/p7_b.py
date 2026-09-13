# -*- coding: utf-8 -*-
"""v4 6차 묶음 B (지시서 2, 7, 9, 15)
   2  예약 목록 한 줄을 CSS grid 로 — 시각|이름|인원|룸|전화 고정 폭, 전화 열이 세로로 맞음. 폰은 전화를 둘째 줄로
   7  날짜가 멋대로 바뀌는 문제 — (a) 예약률 시트는 전용 커서 view.rateEnd (b) 등록·수정 뒤 날짜 점프 삭제 + 토스트 '보기'
   9  PIN 동그라미 — 빈 원 테두리 안에 한·옥·반·점 글자(내장 글꼴 f1~f4)
   15 삭제 확인창에 예약 정보 한 줄"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ============================================================
# 2. 예약 목록 grid
# ============================================================
rep(""".rrow{display:flex; align-items:center; gap:var(--s12); width:100%; text-align:left; background:none; border:none; border-top:1px solid var(--border); font:inherit; color:inherit; white-space:nowrap; overflow:hidden; padding:var(--s12) var(--s8)}
""",
"""/* 한 줄 = grid. 느낌표 | 시각 | 이름 | 인원 | 룸 | 전화 | 나머지(꼬리표).
   6차 전에는 flex 로 흘러서 룸 이름 길이('동탁 룸' vs '지하 홀')에 따라 전화번호 자리가 밀렸습니다.
   앞 여섯 칸을 고정 폭으로 두면 전화 열이 세로로 맞습니다. 인원은 '4명(유아1)' 까지 들어가게 72px */
.rrow{display:grid; grid-template-columns:12px 52px 92px 72px 88px 118px minmax(0,1fr); column-gap:var(--s8); align-items:center; width:100%; text-align:left; background:none; border:none; border-top:1px solid var(--border); font:inherit; color:inherit; white-space:nowrap; overflow:hidden; padding:var(--s12) var(--s8)}
""")
rep(""".rr-t{font-size:var(--fs-body); font-weight:700; width:52px; flex:none; color:var(--text)}
.rr-n{font-size:var(--fs-body); font-weight:600; width:84px; flex:none; overflow:hidden; text-overflow:ellipsis}
.rr-p{font-size:var(--fs-sub); color:var(--text-2); width:100px; flex:none}
.rr-ph{font-size:var(--fs-sub); color:var(--text-3); width:126px; flex:none; overflow:hidden; text-overflow:ellipsis}
.rr-pills{display:flex; gap:var(--s4); flex:1; min-width:0; overflow:hidden}
.rr-seat{flex:none; max-width:150px; overflow:hidden; text-overflow:ellipsis}
.rr-st{flex:none}
""",
""".rr-t{font-size:var(--fs-body); font-weight:700; color:var(--text)}
.rr-n{font-size:var(--fs-body); font-weight:600; min-width:0; overflow:hidden; text-overflow:ellipsis}
/* 인원·룸·전화는 같은 무게(--text-2, 500). 룸만 색 있는 tag 였던 것을 내렸습니다 — 셋 다 '읽는 값'이지 강조가 아닙니다 */
.rr-p, .rr-seat, .rr-ph{font-size:var(--fs-sub); color:var(--text-2); font-weight:500; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
.rr-seat.none{color:var(--rust)}   /* 미배정만 벽돌색 글자 — 자리를 잡아 줘야 하는 건이라 눈에 띄어야 합니다 */
/* 꼬리표 묶음(코스·메모·상태·변동) — 전화 뒤에서 지금처럼 흐릅니다 */
.rr-rest{display:flex; gap:var(--s4); min-width:0; overflow:hidden; align-items:center}
""")
rep("""/* 예약 목록 한 줄이 안 들어가면 두 줄로 접음 */
@media (max-width:780px){
  .rrow{flex-wrap:wrap; gap:var(--s8) var(--s8); white-space:normal}
  .rr-n{width:auto}
  .rr-p{width:auto}
  .rr-ph{width:auto}
  .rr-pills{flex-basis:100%; flex:none}
}
""",
"""/* 폰에서는 다섯 열이 안 들어갑니다 — 전화번호를 둘째 줄로, 꼬리표는 셋째 줄로 (rr-rest 는 있을 때만 그려짐) */
@media (max-width:640px){
  .rrow{grid-template-columns:12px 52px minmax(0,1fr) 72px 88px; row-gap:var(--s4)}
  .rr-ph{grid-column:2 / -1; grid-row:2}
  .rr-rest{grid-column:2 / -1; grid-row:3; flex-wrap:wrap; overflow:visible; white-space:normal}
}
""")
rep("""      <span class="rr-seat tag ${room?'pine':(r.tentativeRoomId?'amber':'rust')}">${esc(seat)}</span>
      <span class="rr-ph">${esc(r.phone||"-")}</span>
      <span class="rr-pills">${pills}</span>
      ${r.status!=="확정"?`<span class="rr-st tag ${r.status==="노쇼"?"rust":""}">${r.status}</span>`:""}
      ${(()=>{ const c=changeTag(r); return c?`<span class="chg-tag ${c.kind==="취소"||c.kind==="노쇼"?"off":""}">${esc(c.label)}</span>`:""; })()}
    </button>`;""",
"""      <span class="rr-seat ${room||r.tentativeRoomId?'':'none'}">${esc(seat)}</span>
      <span class="rr-ph">${esc(r.phone||"-")}</span>
      ${rest?`<span class="rr-rest">${rest}</span>`:""}
    </button>`;""")
rep("""    r.memo ? `<span class="pill blue" title="${esc(r.memo)}">메모</span>` : ""
  ].join("");
  return `
    <button class="rrow s-${r.status} ${late?'late':''}" onclick="openMark('${r.id}')">""",
"""    r.memo ? `<span class="pill blue" title="${esc(r.memo)}">메모</span>` : ""
  ].join("");
  /* 꼬리표 묶음 — 상태(취소/방문/노쇼)와 오늘 변동 표시까지 한 칸에. 비어 있으면 칸 자체를 안 그립니다(폰에서 빈 줄 방지) */
  const rest = pills
    + (r.status!=="확정"?`<span class="rr-st tag ${r.status==="노쇼"?"rust":""}">${r.status}</span>`:"")
    + (()=>{ const c=changeTag(r); return c?`<span class="chg-tag ${c.kind==="취소"||c.kind==="노쇼"?"off":""}">${esc(c.label)}</span>`:""; })();
  return `
    <button class="rrow s-${r.status} ${late?'late':''}" onclick="openMark('${r.id}')">""")

# ============================================================
# 7a. 예약률 시트 — 전용 커서 view.rateEnd
# ============================================================
rep("""function openRate(){ view.form={type:"rate"}; render(); }""",
"""/* 예약률 시트는 자기 커서(view.rateEnd)로 주를 옮깁니다. 6차 전에는 moveDate(±7) 로 메인 날짜를 밀어서
   시트를 닫으면 대시보드가 엉뚱한 주에 가 있었습니다. 열 때 view.date 로 시작하고 닫으면 view.date 는 그대로 */
function openRate(){ view.rateEnd = view.date; view.form={type:"rate"}; render(); }
function rateMove(n){ view.rateEnd = shiftDate(view.rateEnd || view.date, n); render(); }""")
rep("""function sheetRate(){
  const d = view.date;
  return `
    <div class="wide-sheet">
    ${sheetHead("예약률 추이")}
    <div class="chart-nav">
      <button class="btn sm" onclick="moveDate(-7)">&lsaquo; 이전 주</button>
      <span class="muted" style="flex:1; text-align:center; font-size:13px">${dateLabel(shiftDate(d,-13))} – ${dateLabel(d)}</span>
      <button class="btn sm" onclick="moveDate(7)">다음 주 &rsaquo;</button>""",
"""function sheetRate(){
  const d = view.rateEnd || view.date;
  return `
    <div class="wide-sheet">
    ${sheetHead("예약률 추이")}
    <div class="chart-nav">
      <button class="btn sm" onclick="rateMove(-7)">&lsaquo; 이전 주</button>
      <span class="muted" style="flex:1; text-align:center; font-size:13px">${dateLabel(shiftDate(d,-13))} – ${dateLabel(d)}</span>
      <button class="btn sm" onclick="rateMove(7)">다음 주 &rsaquo;</button>""")

# ============================================================
# 7b. 등록·수정 뒤 날짜 점프 삭제 + 토스트
# ============================================================
# 토스트 CSS — 6구역(팝업) .modal-ov 뒤
rep(""".modal-ov{align-items:center; z-index:70; zoom:var(--ui-zoom, 1.1)}
""",
""".modal-ov{align-items:center; z-index:70; zoom:var(--ui-zoom, 1.1)}
/* 토스트 — 화면 아래 한 줄, 3초. 예약을 저장한 뒤 '그 날짜로 점프' 하던 것을 없애고 대신 '보기' 로 갈 수 있게.
   #app 밖(body 바로 아래)에 두어 render() 가 지우지 않습니다. 자리를 항상 같은 곳에 두고 겹치면 글자만 바꿉니다.
   translateX 는 가운데 맞춤용(배율은 zoom — transform:scale 금지와 무관) */
.toast{position:fixed; left:50%; bottom:28px; transform:translateX(-50%); z-index:80; zoom:var(--ui-zoom, 1.1);
  display:flex; align-items:center; gap:var(--s12); max-width:calc(100vw - 32px); white-space:nowrap;
  background:var(--text); color:#fff; border-radius:var(--r-md); padding:var(--s12) var(--s16);
  font-size:var(--fs-body); font-weight:600; box-shadow:0 8px 24px rgba(0,0,0,.28);
  visibility:hidden; opacity:0; transition:opacity .2s ease, visibility .2s}
.toast.on{visibility:visible; opacity:1}
.toast-a{background:none; border:none; color:#9FD8FF; font:inherit; font-weight:700; padding:0 var(--s4); cursor:pointer}
.toast-a:hover{text-decoration:underline}
""")

# 토스트 JS — closeSheet 앞
rep("""function closeSheet(){ view.form=null; tmpRes=null; render(); }""",
"""function closeSheet(){ view.form=null; tmpRes=null; render(); }
/* ---------- 토스트 ----------
   showToast(text, actionLabel, fn) — 같은 자리 하나뿐. 새로 부르면 앞 것을 교체합니다.
   구형 TV 브라우저에서도 죽지 않게 setTimeout 만 씁니다 */
var TOAST_T = null, TOAST_FN = null;
function showToast(text, actionLabel, fn){
  var el = document.getElementById("toast");
  if(!el){ el = document.createElement("div"); el.id = "toast"; el.className = "toast"; document.body.appendChild(el); }
  TOAST_FN = fn || null;
  el.innerHTML = '<span class="toast-t"></span>' + (actionLabel ? '<button class="toast-a" onclick="toastAction()"></button>' : '');
  el.querySelector(".toast-t").textContent = text;
  if(actionLabel) el.querySelector(".toast-a").textContent = actionLabel;
  el.className = "toast on";
  if(TOAST_T) clearTimeout(TOAST_T);
  TOAST_T = setTimeout(hideToast, 3000);
}
function hideToast(){ var el = document.getElementById("toast"); if(el) el.className = "toast"; TOAST_T = null; }
function toastAction(){ var fn = TOAST_FN; hideToast(); if(fn) fn(); }
/* 예약을 저장한 뒤 — 보고 있는 날짜의 예약이면 이미 보이니 '저장됨' 만, 다른 날짜면 '9/20(금) 예약 저장됨 · 보기' */
function toastSaved(rec){
  if(!rec) return;
  if(rec.date === view.date && view.tab !== "settings"){ showToast("저장됨"); return; }
  var d = new Date(rec.date + "T00:00:00");
  var label = (d.getMonth()+1) + "/" + d.getDate() + "(" + ["일","월","화","수","목","금","토"][d.getDay()] + ") 예약 저장됨";
  showToast(label, "보기", function(){ view.date = rec.date; view.tab = "dash"; render(); });
}""")

# (b) 수정 시트 저장 — 점프 삭제
rep("""  if(old && old.date !== rec.date) reflowTentatives(old.date);
  reflowTentatives(rec.date);
  view.date = rec.date; view.form=null; tmpRes=null;
  saveData(); render();
}""",
"""  if(old && old.date !== rec.date) reflowTentatives(old.date);
  reflowTentatives(rec.date);
  /* 6차 전에는 여기서 view.date = rec.date 로 그 날짜로 점프했습니다 — 다음 주 예약을 받다가 화면이 다음 주로 가 버려서
     '오늘' 을 놓치는 일이 있었습니다. 화면은 그대로 두고 토스트의 '보기' 로만 갑니다 */
  view.form=null; tmpRes=null;
  saveData(); render();
  toastSaved(rec);
}""")

# 마법사 완료 — 점프 삭제, 토스트는 완료 화면을 닫은 뒤
rep("""  reflowTentatives(rec.date);
  view.date = rec.date; view.tab = "res"; view.calMonth = rec.date.slice(0,7);
  WZ.done = rec;
  saveData(); render();
}""",
"""  reflowTentatives(rec.date);
  /* 6차 전에는 view.date = rec.date 로 그 날짜로 점프했습니다. 이제 화면 날짜는 그대로 — 완료 화면에 날짜가 있고,
     닫은 뒤 토스트의 '보기' 로 갈 수 있습니다(closeWizardDone) */
  view.tab = "res";
  WZ.done = rec;
  saveData(); render();
}""")
rep("""function closeWizardDone(){ WZ=null; render(); }""",
"""function closeWizardDone(){ var r = WZ && WZ.done; WZ=null; render(); toastSaved(r); }""")

# ============================================================
# 9. PIN 동그라미 — 빈 원 + 글자
# ============================================================
rep(""".pdot{width:38px; height:38px; border:1.5px solid var(--border-strong); background:transparent; display:grid; place-items:center; font-size:var(--fs-head); font-weight:700; color:transparent; transition:all .2s ease; box-shadow:none; border-radius:var(--r-sm)}
.pdot.on{background:transparent; border-color:transparent; transform:none; box-shadow:none; color:var(--text)}
/* 네모 대신 동그라미. 채워지면 먹색 원 안에 글자 — 원래 정의 바로 뒤에 둬야 이깁니다 */
.pdot{border-radius:50%; width:34px; height:34px}
.pdot.on{border-color:transparent; background:var(--text); color:#fff}
.pdot.f1{font-family:'Nanum Myeongjo',serif}
.pdot.f2{font-family:'Noto Serif KR',serif; font-weight:700}
.pdot.f3{font-family:'Pretendard','Noto Sans KR',sans-serif; font-weight:700}
.pdot.f4{font-family:'Nanum Myeongjo',serif; font-weight:700; font-style:italic}
""",
""".pdot{width:34px; height:34px; border:1.5px solid var(--border-strong); background:transparent; display:grid; place-items:center; font-size:var(--fs-head); font-weight:700; color:transparent; transition:color .2s ease; box-shadow:none; border-radius:50%}
/* 채워지면 원은 그대로(빈 테두리) 두고 글자만 나타납니다. 6차 1차 때 '먹색 원 + 흰 글자' 로 바꿨다가 되돌림 —
   원래 규칙은 테두리도 지웠는데, 글자만 떠 있으면 자리 수가 안 보여 테두리는 남깁니다 */
.pdot.on{color:var(--text)}
/* 글자마다 다른 글꼴 — 내장 글꼴만 씁니다(Nanum Myeongjo 는 외부 글꼴이라 지움).
   f3 은 명조 합성 이탤릭(기울임 파일이 없어 브라우저가 기울입니다) */
.pdot.f1{font-family:'Noto Serif KR',serif; font-weight:900}
.pdot.f2{font-family:'Pretendard',sans-serif; font-weight:700}
.pdot.f3{font-family:'Noto Serif KR',serif; font-weight:900; font-style:italic}
.pdot.f4{font-family:'Pretendard',sans-serif; font-weight:400}
""")

# ============================================================
# 15. 삭제 확인창에 예약 정보
# ============================================================
rep("""async function delRes(id){
  if(!await uiConfirm2("이 예약을 삭제할까요? 기록이 완전히 사라집니다.\\n손님이 취소한 경우라면 '예약 취소'를 쓰는 편이 좋습니다.")) return;
  const s=store();
  const rec = s.reservations.find(r=>r.id===id);
""",
"""async function delRes(id){
  const s=store();
  const rec = s.reservations.find(r=>r.id===id);
  /* 무엇을 지우는지 한 줄 — 목록에서 옆 줄을 잘못 누른 경우를 여기서 잡습니다 */
  const who = rec ? `${resLine(rec)}\\n` : "";
  if(!await uiConfirm2(`이 예약을 삭제할까요? 기록이 완전히 사라집니다.\\n${who}손님이 취소한 경우라면 '예약 취소'를 쓰는 편이 좋습니다.`)) return;
""")
# 예약 한 줄 요약 — dateLabel 뒤
rep("""function nowHM(){ const d=new Date(); return pad(d.getHours())+":"+pad(d.getMinutes()); }
""",
"""function nowHM(){ const d=new Date(); return pad(d.getHours())+":"+pad(d.getMinutes()); }
/* 예약 한 줄 요약 — '9/20(금) 18:00 · 홍길동 · 4명 · 관우 룸'. 확인창·토스트처럼 좁은 곳에 씁니다 */
function resLine(r){
  const d = new Date(r.date + "T00:00:00");
  const seat = r.roomId ? seatLabel(r.roomId) : (r.tentativeRoomId ? seatLabel(r.tentativeRoomId) + "(잠정)" : "미배정");
  return (d.getMonth()+1) + "/" + d.getDate() + "(" + ["일","월","화","수","목","금","토"][d.getDay()] + ") "
       + r.time + " · " + r.name + " · " + pplOf(r) + "명 · " + seat;
}
""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_b 적용 완료")
