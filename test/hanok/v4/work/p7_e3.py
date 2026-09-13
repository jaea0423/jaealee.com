# -*- coding: utf-8 -*-
"""6차 묶음 E 보강 2 — histPop 의 history.back() 이 처리되기 전에 다시 열고 닫으면 back() 이 두 번 나가
   사이트 밖(이전 주소)으로 나가던 것. 되돌리는 중(HIST_PENDING)에는 push/pop 을 막고 popstate 에서 정리합니다"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

rep("""function isEditingRes(){ return !view.display && (!!WZ || !!(view.form && view.form.type === "res")); }
function histPush(){
  if(view.display) return;
  try{ if(!(history.state && history.state.wz)) history.pushState({wz:1}, ""); }catch(e){}
}
function histPop(){
  try{ if(history.state && history.state.wz) history.back(); }catch(e){}
}
window.addEventListener("popstate", async function(){
  if(!isEditingRes()) return;""",
"""function isEditingRes(){ return !view.display && (!!WZ || !!(view.form && view.form.type === "res")); }
/* history.back() 은 비동기라, 처리되기 전에 다시 열고 닫으면 back() 이 두 번 나가 사이트 밖으로 나갑니다.
   되돌리는 중(HIST_PENDING)에는 push/pop 을 하지 않고, 그 back() 의 popstate 가 왔을 때 상황에 맞게 정리합니다 */
var HIST_PENDING = false;
function histPush(){
  if(view.display || HIST_PENDING) return;   /* 되돌리는 중이면 popstate 가 칸을 다시 넣어 줍니다 */
  try{ if(!(history.state && history.state.wz)) history.pushState({wz:1}, ""); }catch(e){}
}
function histPop(){
  if(HIST_PENDING) return;
  try{ if(history.state && history.state.wz){ HIST_PENDING = true; history.back(); } }catch(e){}
}
window.addEventListener("popstate", async function(){
  if(HIST_PENDING){
    HIST_PENDING = false;
    /* 닫는 사이에 다른 입력이 열렸으면(마법사 완료 → 새 예약 등) 칸을 도로 넣어 보호를 이어 갑니다 */
    if(isEditingRes()){ try{ history.pushState({wz:1}, ""); }catch(e){} }
    return;
  }
  if(!isEditingRes()) return;""")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p7_e3 ok")
