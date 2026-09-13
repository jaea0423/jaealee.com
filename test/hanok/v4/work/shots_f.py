# -*- coding: utf-8 -*-
"""6차-F 확인 스크린샷"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import run
from shots_a import TODAY_SETUP
from shots_c import INTRO
COURSE = ("openWizard(todayStr()); WZ.source='전화 예약'; WZ.date=todayStr(); WZ.time='18:00'; WZ.people=4; WZ.infants=0; WZ.seat='any'; WZ.step=4;"
          "WZ.menuType='코스'; WZ.courseOpen=true; var g=courseGroups()[0]; bumpCourse(g.id+'|'+g.items[0]); render();")
jobs = [
    ("dash_today_tall", 1280, 1700, TODAY_SETUP),
    ("lock", 430, 932, "AUTHED=false; PIN_BUF='1234'; render();"),
    ("lock", 1280, 800, "AUTHED=false; PIN_BUF='1234'; render();"),
    ("dash_yesterday", 1280, 800, "view.date = shiftDate(todayStr(), -1); render();"),
    ("dash_yesterday", 430, 932, "view.date = shiftDate(todayStr(), -1); render();"),
    ("course_popup", 1280, 900, COURSE),
    ("course_popup", 430, 932, COURSE),
    ("intro_05", 1280, 800, INTRO, 700),
    ("intro_12", 1280, 800, INTRO, 1400),
    ("intro_17", 1280, 800, INTRO, 1900),
    ("display", 1920, 1080, "view.display = true; render();", 12000),
]
if __name__ == "__main__":
    run("6f", jobs)
