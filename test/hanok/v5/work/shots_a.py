# -*- coding: utf-8 -*-
"""6차 묶음 A 확인 스크린샷. python work/shots_a.py → work/shots/6a/"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import run

# 오늘 예약을 손봐서 확인할 상태를 만듭니다 (예시 데이터는 저장되지 않으니 안전).
#  · 지금 시각을 19:00 으로 고정
#  · 확정+룸 예약 하나에 '변경' 기록 → 파랑 + 검정 테두리
#  · 잠정(룸 없음) 예약 하나에 '변경' 기록 → 파랑 + 회색 테두리
#  · 흐림 세 종류: 17:30 확정(+60 지남 → 흐림) / 18:30 방문(즉시 흐림) / 18:30 확정(아직 선명)
TODAY_SETUP = """
nowHM = function(){ return "19:00"; };
var s = store(), t = todayStr();
var L = s.reservations.filter(function(r){ return r.date===t && r.status==="확정"; }).sort(function(a,b){ return a.time.localeCompare(b.time); });
var withRoom = L.filter(function(r){ return !!r.roomId; });
var a = withRoom[0]; a.time = "18:00"; addChange(a, "변경", [{n:"인원"}]);
var b = withRoom[1]; b.tentativeRoomId = b.roomId; b.roomId = null; b.time = "18:30"; addChange(b, "변경", [{n:"시각"}]);
var c = withRoom[2]; c.time = "17:30";
var d = withRoom[3]; d.time = "18:30"; d.status = "방문";
var e = withRoom[4]; e.time = "18:30";
window.__ids = [a.id, b.id, c.id, d.id, e.id];
render();
"""

jobs = [
    ("dash_today",     1280, 800,  TODAY_SETUP),
    ("dash_today",     430,  932,  TODAY_SETUP),
    ("dash_today",     820,  1180, TODAY_SETUP),
    ("dash_yesterday", 1280, 800,  "view.date = shiftDate(todayStr(), -1); render();"),
    ("dash_yesterday", 430,  932,  "view.date = shiftDate(todayStr(), -1); render();"),
    ("dash_tomorrow",  1280, 800,  "view.date = shiftDate(todayStr(), 3); render();"),
    ("dash_tomorrow",  430,  932,  "view.date = shiftDate(todayStr(), 3); render();"),
    ("wizard_date",    1280, 800,  "openWizard(todayStr()); WZ.source='전화'; WZ.step=1; render();"),
    ("wizard_date",    430,  932,  "openWizard(todayStr()); WZ.source='전화'; WZ.step=1; render();"),
    ("display",        1920, 1080, "view.display = true; render();"),
]
if __name__ == "__main__":
    run("6a", jobs)
