# -*- coding: utf-8 -*-
"""6차 묶음 E 확인 스크린샷 — 마법사 1단계(한 화면으로 입력 링크) / 빠른 입력 시트"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import run
WZ0 = "openWizard(todayStr()); render();"
QUICK = "openWizard(todayStr()); openQuick();"
jobs = [("wizard_step0", 1280, 800, WZ0), ("wizard_step0", 430, 932, WZ0),
        ("quick_sheet", 1280, 900, QUICK), ("quick_sheet", 430, 932, QUICK), ("quick_sheet_tall", 430, 1500, QUICK)]
if __name__ == "__main__":
    run("6e", jobs)
