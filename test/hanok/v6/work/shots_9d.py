# -*- coding: utf-8 -*-
"""8차-D 스크린샷 — 대시보드(타임라인)·설정 좌석·운영시간 편집·마법사 좌석 단계·TV"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import run
SRC = "/v6/dev/index.html"
D = "view.date='2026-09-19'; view.tab='dash'; "
SEATS = "view.tab='settings'; view.open['s_seats']=true; render(); "
HOURS = "view.tab='settings'; view.open['s_hours']=true; render(); openSchedule('2000-01-01'); render(); "
WZ = "DATA._readonly=false; READONLY_WHY=''; openWizard('2026-09-19'); WZ.source='네이버 예약'; WZ.time='12:00'; WZ.people=6; WZ.step=3; render(); "
jobs = []
for w, h in [(1280, 900), (820, 1100), (430, 932)]:
    jobs += [("dash", w, h, D + "render(); if(typeof isMobile==='function'&&isMobile()){ view.mview='tl'; render(); }"),
             ("seats", w, h, D + SEATS),
             ("hours", w, h, D + HOURS),
             ("wz_seat", w, h, D + WZ)]
run("9d", jobs, src=SRC)
run("9d", [("tv", 1920, 1080, "render();")], src="/v6/dev/screen/index.html")
