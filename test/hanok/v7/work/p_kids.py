# -*- coding: utf-8 -*-
"""'유아' → '어린이' (재아). 어린이가 유아를 포함하는 개념. 의자만 '유아용 의자' 그대로.
   유아용 의자 기본값은 0개(설정 기본을 zero 로).
   내부 필드 infants/chairs 와 설정 키는 그대로 — 예약 객체 모양 불변."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep, js_check, parts

def sub_all(s):
    # 의자 관련은 지킴: '유아용 의자' '유아의자' 를 잠시 다른 글자로 바꿔 두고 나머지 '유아' 만 바꿈
    s = s.replace("유아용 의자", "\x00CHAIR1\x00").replace("유아의자", "\x00CHAIR2\x00")
    s = s.replace("유아", "어린이")
    return s.replace("\x00CHAIR1\x00", "유아용 의자").replace("\x00CHAIR2\x00", "유아의자")

for name in parts("js"):
    s = load(name); t = sub_all(s)
    if t != s: save(name, t); print("바꿈", name)

# 의자 기본값: 0개
s = load("js/03-util.js")
s = rep(s, 'function chairDefaultInfants(){ return store().settings.chairDefault !== "zero"; }',
           'function chairDefaultInfants(){ return store().settings.chairDefault === "infants"; }   /* 기본 0개(재아). 설정에서 \'어린이 수와 같게\' 를 고르면 따라감 */')
save("js/03-util.js", s)
s = load("js/14-settings.js")
s = rep(s, '''<button class="${st.chairDefault!=="zero"?'on':''}" onclick="setPolicy('chairDefault','infants')">어린이 수와 같게</button>
      <button class="${st.chairDefault==="zero"?'on':''}" onclick="setPolicy('chairDefault','zero')">0개</button>''',
           '''<button class="${st.chairDefault==="infants"?'on':''}" onclick="setPolicy('chairDefault','infants')">어린이 수와 같게</button>
      <button class="${st.chairDefault!=="infants"?'on':''}" onclick="setPolicy('chairDefault','zero')">0개</button>''')
s = rep(s, '`의자 ${st.chairDefault==="zero"?"0개":"어린이 수"}', '`의자 ${st.chairDefault==="infants"?"어린이 수":"0개"}')
save("js/14-settings.js", s)
# 네이버 엑셀 붙여넣기의 '어린이/유아/아동' 인식은 유지 (원문에 유아라고 올 수 있음)
s = load("js/15-sheets.js")
s = rep(s, 'const kid = t.match(/(?:어린이|어린이|아동)\\((\\d+)\\)/);', 'const kid = t.match(/(?:어린이|유아|아동)\\((\\d+)\\)/);')
save("js/15-sheets.js", s)
js_check()
print("어린이 표기 끝")
