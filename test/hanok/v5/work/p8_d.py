# -*- coding: utf-8 -*-
"""v5 7차 묶음 D — 손님용 TV
   · 공개 뷰(public_screen / public_today) 읽기는 B 에서. 여기서는 화면 캐시(hanok.screen.v1)로 시작 시 실패해도 마지막 데이터를 보여 주고,
     갱신 실패는 지금처럼 마지막 데이터 유지 + 3회 연속이면 '연결 확인 중'"""
import io
P = "src/index.html"
s = io.open(P, encoding="utf-8").read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

rep("""  try{ localStorage.setItem("hanok.screen.v1", JSON.stringify({ at:new Date().toISOString(), data:d })); }catch(e){}
}""",
"""  try{ localStorage.setItem(SCREEN_KEY, JSON.stringify({ at:new Date().toISOString(), data:d })); }catch(e){}
}
var SCREEN_KEY = "hanok.screen.v1";
/* 켤 때 서버를 못 읽으면 마지막으로 성공한 화면(캐시)으로 시작합니다 — TV 는 방치용이라 빈 화면보다 어제 목록이 낫습니다.
   1분 갱신이 이어서 시도하고, 성공하면 자연히 새 데이터로 바뀝니다. 캐시도 없으면 그대로 던집니다(빈 화면 + 띠) */
async function loadPublicOrCache(){
  try{ await loadPublic(); }
  catch(e){
    var c = null; try{ c = JSON.parse(localStorage.getItem(SCREEN_KEY) || "null"); }catch(e2){}
    if(!c || !c.data) throw e;
    var ui = DATA && DATA._ui;
    DATA = migrate(deepClone(c.data)); DATA._ui = ui || uiLoad(); DATA._readonly = true; READONLY_WHY = "public";
    DISP_FAIL = Math.max(DISP_FAIL, 1);
    console.warn("공개 뷰 실패 — 캐시(" + c.at + ")로 시작", e.message);
  }
}""")
rep("""    if(!AUTHED) loadPublic().then(function(){ render(); }).catch(function(e){ console.warn("공개 뷰 실패", e.message); });""",
    """    if(!AUTHED) loadPublicOrCache().then(function(){ render(); }).catch(function(e){ console.warn("공개 뷰 실패", e.message); });""")
rep("""  if(supaOn()) loadPublic().then(function(){ render(); }).catch(function(){});   /* 매장 선택의 '오늘 예약 N건' */""",
    """  if(supaOn()) loadPublicOrCache().then(function(){ render(); }).catch(function(){});   /* 매장 선택의 '오늘 예약 N건' */""")
# 캐시 시각이 오늘이 아니면(어제 캐시로 켠 TV) 예약 목록은 비웁니다 — 어제 예약을 오늘 것처럼 보이면 안 됩니다
rep("""    if(!c || !c.data) throw e;
    var ui = DATA && DATA._ui;
    DATA = migrate(deepClone(c.data));""",
"""    if(!c || !c.data) throw e;
    if(!c.at || todayStr(new Date(c.at)) !== todayStr()){ Object.keys(c.data).forEach(function(k){ c.data[k].reservations = []; }); }   /* 날짜가 지난 캐시 — 좌석 설정만 쓰고 예약은 비움 */
    var ui = DATA && DATA._ui;
    DATA = migrate(deepClone(c.data));""")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("p8_d ok")
