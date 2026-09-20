# -*- coding: utf-8 -*-
"""apple-design 손보기용 스크린샷 (2026-09-20). 로그인 없이 예시 데이터(seedDemo)로 주요 화면을 찍습니다.
   서버가 필요한 페이지(워크시프트·손님 관리·감사 문자·홈페이지 관리)는 여기서 못 찍습니다 — review_shots.py(HANOK_PIN) 로.

   python work/ad_shots.py <라벨> [폭들]     예: python work/ad_shots.py ad1 820,1280
"""
import sys
from shot import run

DEMO = ("DATA=seedDemo(deepClone(DEFAULT_DATA)); DATA._ui={theme:'hanok'}; DATA._readonly=false; AUTHED=true; "
        "view.storeKey='hanok'; view.date=todayStr(); view.adminOk=true; MODAL=null; INTRO=null; ")
TM = "shiftDate(todayStr(),1)"
first_res = "store().reservations.filter(function(r){return r.date===todayStr()&&r.status==='확정'})[0]"
JOBS = [
  ("dash_graph",   "view.tab='dash'; view.mView='graph'; view.mode='graph';"),
  ("dash_list",    "view.tab='dash'; view.mView='list'; view.mode='list'; view.open.list=true;"),
  ("more",         "view.tab='dash'; view.moreOpen=true;"),
  ("cal",          "openCal();"),
  ("search",       "openSearch();"),
  ("check",        "openCheck();"),
  ("res_detail",   "openRes(%s.id);" % first_res),
  ("res_mark",     "openMark(%s.id);" % first_res),
  ("wz0",          "openWizard();"),
  ("wz1",          "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='18:00'; WZ.step=1;" % TM),
  ("wz2",          "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='12:00'; WZ.step=2; WZ.people=4;" % TM),
  ("wz3",          "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='12:00'; WZ.people=4; WZ.step=3; WZ.seatKind='room';" % TM),
  ("wz4",          "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='18:00'; WZ.people=4; WZ.step=4; WZ.seatKind='room'; WZ.seat=roomsAt(WZ.date).filter(isRoom)[0].id; WZ.menuType='코스';" % TM),
  ("wz5",          "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='18:00'; WZ.people=4; WZ.step=5; WZ.seatKind='room'; WZ.seat=roomsAt(WZ.date).filter(isRoom)[0].id; WZ.name='홍길동';" % TM),
  ("wz6",          "openWizard(); wzSource('전화 예약'); WZ.date=%s; WZ.time='18:00'; WZ.people=4; WZ.step=6; WZ.seatKind='room'; WZ.seat=roomsAt(WZ.date).filter(isRoom)[0].id; WZ.name='홍길동'; WZ.phone='010-1234-5678';" % TM),
  ("settings",     "view.tab='settings';"),
  ("set_hours",    "view.tab='settings'; view.setSec='hours';"),
  ("set_seats",    "view.tab='settings'; view.setSec='seats';"),
  ("set_rules",    "view.tab='settings'; view.setSec='rules';"),
  ("owner",        "openOwnerPage();"),
  ("lock",         "AUTHED=false; view.storeKey='hanok'; PIN_BUF='10';"),
  ("modal",        "MODAL={mode:'confirm', title:'관우 룸에 1시간 안에 확정 예약이 있습니다', msg:'· 오후 6시 김하람 4명\\n\\n그래도 이 자리로 배정할까요?', tone:'warn', ok:'그래도 배정', cancel:'다시 고르기', res:function(){}};"),
]

if __name__ == "__main__":
    label = sys.argv[1] if len(sys.argv) > 1 else "ad"
    widths = [int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else "820,1280").split(",")]
    only = sys.argv[3].split(",") if len(sys.argv) > 3 else None
    jobs = []
    for name, js in JOBS:
        if only and name not in only: continue
        for w in widths:
            h = {390: 844, 430: 932, 820: 1180, 1280: 800, 1920: 1080}.get(w, 900)
            jobs.append((name, w, h, DEMO + js + " render();"))
    run(label, jobs, src="/system/dev/index.html")
