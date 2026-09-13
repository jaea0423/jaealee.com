# -*- coding: utf-8 -*-
"""v4 6차 묶음 E (지시서 14 → 13)
   14 마법사·수정 시트 뒤로가기 보호 — pushState 한 칸 + popstate 확인창, beforeunload 브라우저 기본 확인창. 디스플레이 제외
   13 빠른 입력 — 새 화면 없이 수정 시트(sheetRes)를 빈 예약으로. 마법사 1단계 아래 '한 화면으로 입력'.
      등록 경로는 마법사와 같은 함수(confirmNewRes → createReservation)"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()

def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ============================================================
# 14. 뒤로가기 보호
# ============================================================
rep("""function openWizard(date){
  WZ = {""",
"""/* ---------- 뒤로가기 보호 ----------
   앱은 주소를 history.replaceState 로만 바꾸므로 브라우저 뒤로가기가 눌리면 사이트 밖으로 나가 입력이 날아갔습니다.
   마법사·수정 시트를 열 때 history 에 한 칸(pushState) 넣어 두면 뒤로가기는 '닫기' 가 됩니다 —
   닫을지 한 번 묻고, 취소하면 그 칸을 다시 넣습니다. 정상으로 닫을 때는 그 칸을 도로 빼서(histPop) 뒤로가기가 헛돌지 않게 합니다.
   새로고침·탭 닫기는 beforeunload 로 브라우저 기본 확인창 — 문구는 브라우저가 정하고 우리 문구는 못 넣습니다.
   디스플레이(view.display)에서는 둘 다 걸지 않습니다 (TV 는 방치용) */
function isEditingRes(){ return !view.display && (!!WZ || !!(view.form && view.form.type === "res")); }
function histPush(){
  if(view.display) return;
  try{ if(!(history.state && history.state.wz)) history.pushState({wz:1}, ""); }catch(e){}
}
function histPop(){
  try{ if(history.state && history.state.wz) history.back(); }catch(e){}
}
window.addEventListener("popstate", async function(){
  if(!isEditingRes()) return;
  if(!await uiConfirm2("입력 중인 예약이 있습니다. 나갈까요?")){
    try{ history.pushState({wz:1}, ""); }catch(e){}
    return;
  }
  WZ = null; view.form = null; tmpRes = null; render();
});
window.addEventListener("beforeunload", function(e){
  if(!isEditingRes()) return;
  e.preventDefault(); e.returnValue = "";
});
function openWizard(date){
  histPush();
  WZ = {""")
rep("""    if(!await uiConfirm2("입력 중인 예약이 있습니다. 닫을까요?")) return;
  }
  WZ = null; render();
}""",
"""    if(!await uiConfirm2("입력 중인 예약이 있습니다. 닫을까요?")) return;
  }
  WZ = null; render(); histPop();
}""")
rep("""function closeWizardDone(){ var r = WZ && WZ.done; WZ=null; render(); toastSaved(r); }""",
    """function closeWizardDone(){ var r = WZ && WZ.done; WZ=null; render(); histPop(); toastSaved(r); }""")
rep("""function openRes(id){ view.form={type:"res", id}; render(); }""",
    """function openRes(id){ histPush(); view.form={type:"res", id}; render(); }""")
rep("""function closeSheet(){ view.form=null; tmpRes=null; render(); }""",
    """function closeSheet(){ var was = view.form && view.form.type === "res"; view.form=null; tmpRes=null; render(); if(was) histPop(); }""")

# ============================================================
# 13. 빠른 입력
# ============================================================
# (a) 마법사 1단계 아래 텍스트 버튼
rep("""        <input id="wz-src-detail" value="${esc(WZ.sourceDetail)}" placeholder="예: 지인 소개, 대면 예약" ${WZ.source==="기타"?"autofocus":"tabindex=\\"-1\\""}>
        <div class="f-note">예약 내역에 참고로만 남습니다</div>
      </label>`;
}""",
"""        <input id="wz-src-detail" value="${esc(WZ.sourceDetail)}" placeholder="예: 지인 소개, 대면 예약" ${WZ.source==="기타"?"autofocus":"tabindex=\\"-1\\""}>
        <div class="f-note">예약 내역에 참고로만 남습니다</div>
      </label>
    <button class="linkbtn wz-quick" onclick="openQuick()">한 화면으로 입력</button>`;
}
/* 빠른 입력 — 새 화면을 만들지 않고 이미 있는 수정 시트(sheetRes)를 빈 예약으로 엽니다 (새 코드가 적어야 오류도 적습니다).
   마법사 1단계 아래 '한 화면으로 입력' 에서만 들어옵니다. 날짜는 마법사가 열려 있던 날짜(= 보고 있던 날짜) */
function openQuick(){
  const d = (WZ && WZ.date) || view.date;
  WZ = null; tmpRes = null;
  view.form = {type:"res", date:d};
  render();
}""")
rep(""".srcgrid{display:grid; grid-template-columns:1fr; gap:var(--s12)}
""",
""".srcgrid{display:grid; grid-template-columns:1fr; gap:var(--s12)}
/* 1단계 타일 아래 '한 화면으로 입력' — 타일과 경쟁하지 않게 작은 회색 글자 링크 */
.wz-quick{display:block; margin:var(--s24) auto 0; color:var(--text-3); font-size:var(--fs-sub); font-weight:600}
.wz-quick:hover{color:var(--text)}
""")

# (b) sheetRes 새 예약 모드 — 빈 값, 제목 '빠른 입력', 버튼 '등록'
rep("""      : {__id:"new", date:view.date, time:"18:00", name:"", phone:"", people:2, infants:0,
         chairs:0, roomId:"", source:"전화", sourceDetail:"", request:"", allergy:"", status:"확정",
         menuType:"해당 없음", courses:{}, courseUndecided:false};""",
"""      /* 빠른 입력(openQuick) — 시각·인원·경로를 비워 두어 마법사처럼 직접 고르게 합니다. 필수는 시각·인원·이름 */
      : {__id:"new", date:(view.form.date||view.date), time:"", name:"", phone:"", people:0, infants:0,
         chairs:0, roomId:"", source:"", sourceDetail:"", request:"", allergy:"", status:"확정",
         menuType:"해당 없음", courses:{}, courseUndecided:false};""")
rep("""    ${sheetHead(editing?"예약 내용 수정":"새 예약")}""",
    """    ${sheetHead(editing?"예약 내용 수정":"빠른 입력")}""")
rep("""      <button class="btn primary" onclick="saveRes()">저장</button>
    </div>`;
}""",
"""      <button class="btn primary" onclick="saveRes()">${editing?"저장":"등록"}</button>
    </div>`;
}""")

# (c) 등록 경로 공유 — wzSubmit 의 확인·등록 부분을 confirmNewRes / createReservation 으로
rep("""  const s = store();
  /* 같은 번호로 같은 날 이미 예약이 있으면 확인 */
  if(WZ.phone){
    const dup = s.reservations.filter(r=>r.date===WZ.date && r.status==="확정" &&
      (r.phone||"").replace(/\\D/g,"") === WZ.phone.replace(/\\D/g,""));
    if(dup.length){
      const ok = await uiConfirm("같은 번호로 이미 예약이 있습니다",
        dup.map(r=>`${hm(r.time)} ${r.name} 손님 ${pplText(r)}`).join("\\n") +
        "\\n\\n같은 팀이라면 기존 예약을 수정하는 편이 좋습니다.",
        {ok:"새로 등록", cancel:"취소"});
      if(!ok) return;
    }
  }
  /* 노쇼 이력이 있으면 확정 전에 확인 */
  const ns = noshowOf(WZ.phone);
  if(ns && !await uiConfirm2(
      `이 번호로 노쇼 기록이 ${ns.count}건 있습니다.\\n` +
      `(${ns.dates.slice(0,3).map(d=>d.slice(5).replace("-","월 ")+"일").join(", ")}${ns.dates.length>3?" 외":""})\\n\\n` +
      `예약을 확정할까요?`)) return;
  const isRoom""",
"""  if(!await confirmNewRes(WZ.date, WZ.phone)) return;
  const isRoom""")
rep("""  addChange(rec, "등록", []);
  /* 접수 문자 — 등록 즉시 1회 (지금은 흉내) */
  if(smsCfg().on && rec.phone) smsSend(rec, "접수");
  s.reservations.push(rec);
  logEvent("예약 등록", `${rec.date} ${rec.time} ${rec.name} ${pplOf(rec)}명 ${rec.roomId?seatLabel(rec.roomId):(rec.tentativeRoomId?"잠정 "+seatLabel(rec.tentativeRoomId):"미배정")} 경로:${rec.source}${rec.sourceDetail?"/"+rec.sourceDetail:""}`);
  reflowTentatives(rec.date);
  /* 6차 전에는 view.date = rec.date 로 그 날짜로 점프했습니다.""",
"""  createReservation(rec);
  /* 6차 전에는 view.date = rec.date 로 그 날짜로 점프했습니다.""")
rep("""/* ---------- 등록 ---------- */
async function wzSubmit(){""",
"""/* ---------- 새 예약 등록 — 마법사(wzSubmit)와 빠른 입력(saveRes)이 같은 길을 갑니다 ----------
   같은 번호 확인 → 노쇼 이력 확인(confirmNewRes) → 등록 기록·문자 흉내·목록에 넣기·로그·잠정 배정(createReservation).
   둘이 따로 있으면 데이터 모양(changes·updatedAt·source…)이 조금씩 달라집니다 */
async function confirmNewRes(date, phone){
  const s = store();
  /* 같은 번호로 같은 날 이미 예약이 있으면 확인 */
  if(phone){
    const dup = s.reservations.filter(r=>r.date===date && r.status==="확정" &&
      (r.phone||"").replace(/\\D/g,"") === phone.replace(/\\D/g,""));
    if(dup.length){
      const ok = await uiConfirm("같은 번호로 이미 예약이 있습니다",
        dup.map(r=>`${hm(r.time)} ${r.name} 손님 ${pplText(r)}`).join("\\n") +
        "\\n\\n같은 팀이라면 기존 예약을 수정하는 편이 좋습니다.",
        {ok:"새로 등록", cancel:"취소"});
      if(!ok) return false;
    }
  }
  /* 노쇼 이력이 있으면 확정 전에 확인 */
  const ns = noshowOf(phone);
  if(ns && !await uiConfirm2(
      `이 번호로 노쇼 기록이 ${ns.count}건 있습니다.\\n` +
      `(${ns.dates.slice(0,3).map(d=>d.slice(5).replace("-","월 ")+"일").join(", ")}${ns.dates.length>3?" 외":""})\\n\\n` +
      `예약을 확정할까요?`)) return false;
  return true;
}
function createReservation(rec){
  const s = store();
  addChange(rec, "등록", []);
  /* 접수 문자 — 등록 즉시 1회 (지금은 흉내) */
  if(smsCfg().on && rec.phone) smsSend(rec, "접수");
  s.reservations.push(rec);
  logEvent("예약 등록", `${rec.date} ${rec.time} ${rec.name} ${pplOf(rec)}명 ${rec.roomId?seatLabel(rec.roomId):(rec.tentativeRoomId?"잠정 "+seatLabel(rec.tentativeRoomId):"미배정")} 경로:${rec.source}${rec.sourceDetail?"/"+rec.sourceDetail:""}`);
  reflowTentatives(rec.date);
  return rec;
}
/* ---------- 등록 ---------- */
async function wzSubmit(){""")

# saveRes — 새 예약이면 공유 함수로
rep("""    source:f.source, sourceDetail:f.source==="기타"?(f.sourceDetail||"").trim():"",
    request:(f.request||"").trim(), allergy:(f.allergy||"").trim(), memo:(f.memo||"").trim(),""",
"""    source:f.source || "전화 예약", sourceDetail:f.source==="기타"?(f.sourceDetail||"").trim():"",
    request:(f.request||"").trim(), allergy:(f.allergy||"").trim(), memo:(f.memo||"").trim(),
    allergyChecked: old ? old.allergyChecked : true,   /* 마법사와 같은 모양 */""")
rep("""  /* 무엇이 바뀌었는지 남깁니다 (사장님의 '파란 글씨' — 변동 이력 참고) */
  if(old){
    const d = diffRes(old, rec);
    if(d.length) addChange(rec, "변경", d);
    if(old.status !== rec.status && (rec.status==="취소" || rec.status==="노쇼"))
      addChange(rec, rec.status, []);
  }else{
    addChange(rec, "등록", []);
    /* 접수 문자 — 새 예약일 때만 1회 (수정으로는 다시 나가지 않습니다) */
    if(smsCfg().on && rec.phone) smsSend(rec, "접수");
  }

  s.reservations = view.form.id ? s.reservations.map(r=>r.id===rec.id?rec:r) : [...s.reservations, rec];
  logEvent(view.form.id?"예약 수정":"예약 등록", `${rec.date} ${rec.time} ${rec.name} ${pplOf(rec)}명`);
  /* 날짜를 옮겼으면 원래 날짜의 잠정 배정도 다시 계산해야 합니다 —
     안 그러면 비어 버린 자리를 계속 피한 채로 남습니다 */
  if(old && old.date !== rec.date) reflowTentatives(old.date);
  reflowTentatives(rec.date);""",
"""  if(old){
    /* 무엇이 바뀌었는지 남깁니다 (사장님의 '파란 글씨' — 변동 이력 참고) */
    const d = diffRes(old, rec);
    if(d.length) addChange(rec, "변경", d);
    if(old.status !== rec.status && (rec.status==="취소" || rec.status==="노쇼"))
      addChange(rec, rec.status, []);
    s.reservations = s.reservations.map(r=>r.id===rec.id?rec:r);
    logEvent("예약 수정", `${rec.date} ${rec.time} ${rec.name} ${pplOf(rec)}명`);
    /* 날짜를 옮겼으면 원래 날짜의 잠정 배정도 다시 계산해야 합니다 —
       안 그러면 비어 버린 자리를 계속 피한 채로 남습니다 */
    if(old.date !== rec.date) reflowTentatives(old.date);
    reflowTentatives(rec.date);
  }else{
    /* 빠른 입력 — 마법사와 같은 등록 경로 (같은 번호·노쇼 확인 포함) */
    if(!await confirmNewRes(rec.date, rec.phone)) return;
    createReservation(rec);
  }""")
rep("""  view.form=null; tmpRes=null;
  saveData(); render();
  toastSaved(rec);
}""",
"""  view.form=null; tmpRes=null;
  saveData(); render(); histPop();
  toastSaved(rec);
}""")

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_e 적용 완료")
