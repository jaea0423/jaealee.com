# -*- coding: utf-8 -*-
"""6차 묶음 B 확인 스크린샷. python work/shots_b.py → work/shots/6b/"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import run

LIST = "view.open.list=true; render(); var el=document.getElementById('tl-scroll'); window.scrollTo(0, document.querySelector('.fold.on').offsetTop-8);"
LOCK = "AUTHED=false; PIN_BUF='12'; render();"
TOAST = "render(); toastSaved({date:shiftDate(todayStr(),6)}); clearTimeout(TOAST_T);"
TOAST2 = "render(); toastSaved({date:todayStr()}); clearTimeout(TOAST_T);"
DEL = "var r=store().reservations.filter(function(x){return x.date===todayStr()&&x.roomId;})[0]; delRes(r.id);"
RATE = "openRate(); rateMove(-7);"
jobs = [
    ("list", 1280, 1400, LIST), ("list", 820, 1400, LIST), ("list", 430, 1600, LIST),
    ("lock", 1280, 800, LOCK), ("lock", 430, 932, LOCK),
    ("toast_other", 1280, 800, TOAST), ("toast_same", 430, 932, TOAST2),
    ("del_confirm", 1280, 800, DEL), ("del_confirm", 430, 932, DEL),
    ("rate_sheet", 1280, 900, RATE),
]
if __name__ == "__main__":
    run("6b", jobs)
