# -*- coding: utf-8 -*-
"""6차 묶음 C(인트로) 확인 — 가상 시간 예산으로 특정 시점을 찍습니다. 왼쪽 위 검은 배지 = startIntro 뒤 경과 ms"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import run
INTRO = ("window.__t0=performance.now(); startIntro();"
         "var b=document.createElement('div'); b.style.cssText='position:fixed;left:8px;top:8px;z-index:999;background:#000;color:#fff;font:14px monospace;padding:2px 6px';"
         "document.body.appendChild(b); setInterval(function(){ b.textContent=Math.round(performance.now()-window.__t0)+'ms'; }, 16);")
jobs = [("intro_04", 1280, 800, INTRO, 600), ("intro_09", 1280, 800, INTRO, 1100),
        ("intro_14", 1280, 800, INTRO, 1600), ("intro_19", 1280, 800, INTRO, 2100),
        ("intro_14", 430, 932, INTRO, 1600)]
if __name__ == "__main__":
    run("6c", jobs)
