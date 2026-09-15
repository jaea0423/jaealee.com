# -*- coding: utf-8 -*-
"""오래 띄워 두면 '작성 도중 수정된 내용입니다' 가 저절로 뜨고 확인해도 안 사라지던 것.
   원인 ① 1분 갱신 뒤 reflowFuture 가 잠정 배정을 다시 계산해 서버에 저장 → 두 기기가 서로를 '먼저 수정한 기기' 로 봄
   원인 ② 알림이 겹치면 새 것이 이전 것을 덮고 이전 Promise 는 영원히 대기 → 확인을 눌러도 다음 알림이 또
   수정 ① 잠정 배정 재계산은 저장하지 않음(화면 계산). 잠정은 어차피 각 기기가 같은 규칙으로 계산해 같은 답이 나옴
   수정 ② 새 알림이 오면 이전 알림을 false 로 닫고 교체"""
import io
P = "src/index.html"; s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80]); s = s.replace(old, new)
rep("""  view.storeKey = prev;
  if(changed) saveData();
}""",
"""  view.storeKey = prev;
  /* 저장하지 않습니다. 잠정 배정은 겹침으로 정해지는 '계산값' 이라 각 기기가 같은 규칙으로 같은 답을 내고,
     저장하면 두 기기가 서로를 '먼저 수정한 기기' 로 보아 아무것도 안 했는데 충돌 알림이 떴습니다(7차 점검).
     이 기기에서 실제로 예약을 고칠 때(saveRes/wzSubmit 의 reflowTentatives) 함께 올라갑니다 */
  if(changed) syncMarkTentatives();
}
/* 재계산으로 바뀐 잠정 배정을 '이미 동기화된 것' 으로 표시해 flush 가 보내지 않게 합니다 */
function syncMarkTentatives(){
  Object.keys(DEFAULT_DATA).forEach(function(k){
    var st = DATA[k]; if(!st) return;
    (st.reservations || []).forEach(function(r){
      if(r.roomId || !SYNC.res[r.id]) return;
      try{ var was = JSON.parse(SYNC.res[r.id]); if(was.tentativeRoomId !== r.tentativeRoomId){ was.tentativeRoomId = r.tentativeRoomId; SYNC.res[r.id] = JSON.stringify(Object.assign({}, r, {updatedAt: was.updatedAt})); r.updatedAt = was.updatedAt; } }catch(e){}
    });
  });
}""")
rep("""function uiAlert(title, msg, tone){
  return new Promise(res => { MODAL = {mode:"alert", title, msg, tone:tone||"warn", res}; render(); });
}
function uiConfirm(title, msg, opt){
  opt = opt || {};
  return new Promise(res => {
    MODAL = {mode:"confirm", title, msg, tone:opt.tone||"warn",
             ok:opt.ok||"계속", cancel:opt.cancel||"취소", res};
    render();
  });
}""",
"""/* 알림이 떠 있는데 새 알림이 오면 이전 것은 '취소' 로 닫습니다 — 안 그러면 이전 Promise 가 영원히 대기해
   그것을 기다리던 저장·단계 이동이 조용히 멈추고, 확인을 눌러도 다음 알림이 계속 뜹니다(7차 점검 U2) */
function modalReplace(next){
  var prev = MODAL; MODAL = next; render();
  if(prev && prev.res) prev.res(false);
}
function uiAlert(title, msg, tone){
  return new Promise(res => { modalReplace({mode:"alert", title, msg, tone:tone||"warn", res}); });
}
function uiConfirm(title, msg, opt){
  opt = opt || {};
  return new Promise(res => {
    modalReplace({mode:"confirm", title, msg, tone:opt.tone||"warn",
                  ok:opt.ok||"계속", cancel:opt.cancel||"취소", res});
  });
}""")
io.open(P, "w", encoding="utf-8", newline="\n").write(s); print("p8_o ok")
