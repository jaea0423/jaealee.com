# -*- coding: utf-8 -*-
"""코스 → '코스·세트' 표기 (재아, 사이트 작업에서 나온 숙제).
   저녁 코스는 종일 팔고 점심에만 세트가 있으므로 둘을 같은 것으로 다루되, 화면 이름만 '코스·세트'로.
   내부 값(menuType === "코스", courses 키)은 그대로 — 예약 객체 모양 불변."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep, js_check

L = "코스·세트"

# ---- 대시보드 목록 pill ----
s = load("js/07-dash.js")
s = rep(s, 'r.menuType==="코스" ? (r.courseUndecided ? "코스 미정" : "코스") : r.menuType==="코스 상당" ? "코스상당"',
           'r.menuType==="코스" ? (r.courseUndecided ? "%s 미정" : "%s") : r.menuType==="코스 상당" ? "코스상당"' % (L, L))
s = rep(s, '''      ? `<span class="pill amber">코스 미정</span>`
      : `<span class="pill pine" title="${esc(courseSummary(r.courses))}">코스</span>`) :''',
           '''      ? `<span class="pill amber">%s 미정</span>`
      : `<span class="pill pine" title="${esc(courseSummary(r.courses))}">%s</span>`) :''' % (L, L))
save("js/07-dash.js", s)

# ---- 변경 비교 ----
s = load("js/08-changes.js")
s = rep(s, 'if(ca !== cb) out.push({n:"코스", a:ca||"없음", b:cb||"없음"});', 'if(ca !== cb) out.push({n:"%s", a:ca||"없음", b:cb||"없음"});' % L)
save("js/08-changes.js", s)

# ---- 확인 필요 꼬리표 (키와 설명을 같이 바꿈) ----
s = load("js/09-sms.js")
s = rep(s, 'if(r.menuType==="해당 없음") out.push("룸·코스 아님");', 'if(r.menuType==="해당 없음") out.push("룸·%s 아님");' % L)
s = rep(s, 'else if(r.menuType==="확인 필요") out.push("코스 미확정");', 'else if(r.menuType==="확인 필요") out.push("%s 미확정");' % L)
s = rep(s, 'out.push("코스 인원 부족");', 'out.push("%s 인원 부족");' % L)
s = rep(s, 'note:"방문 전 연락해 코스를 확정하세요."', 'note:"방문 전 연락해 %s를 확정하세요."' % L)
s = rep(s, 'kind==="group"&&r.menuType==="코스"?` · 코스`:""', 'kind==="group"&&r.menuType==="코스"?` · %s`:""' % L)
save("js/09-sms.js", s)

s = load("js/15-sheets.js")
s = rep(s, '''    "룸·코스 아님": `룸 예약인데 식사가 '해당 없음' 입니다`,
    "코스 미확정": `코스가 '확인 필요' 상태입니다`,
    "코스 인원 부족": `코스 인원이 성인 수보다 적습니다`,''',
           '''    "룸·%s 아님": `룸 예약인데 식사가 '해당 없음' 입니다`,
    "%s 미확정": `%s가 '확인 필요' 상태입니다`,
    "%s 인원 부족": `%s 인원이 성인 수보다 적습니다`,''' % (L, L, L, L, L))
# 수정 시트 식사 단추: 값은 그대로, 보이는 글자만
s = rep(s, '''    `<button class="${f.menuType===x?'on':''}" onclick="pickMenuType('${x}')">${x}</button>`).join("");''',
           '''    `<button class="${f.menuType===x?'on':''}" onclick="pickMenuType('${x}')">${x==="코스"?"%s":x}</button>`).join("");''' % L)
s = rep(s, '"룸 예약에 코스 이용 예정 손님이 아닙니다" :', '"룸 예약에 %s 이용 예정 손님이 아닙니다" :' % L)
s = rep(s, '? `코스 ${cN}인분 · 성인 ${cAd}명보다 적습니다` : "");', '? `%s ${cN}인분 · 성인 ${cAd}명보다 적습니다` : "");' % L)
s = rep(s, '<span>${f.courseUndecided ? "코스 미정 — 방문 전 확정"', '<span>${f.courseUndecided ? "%s 미정 — 방문 전 확정"' % L)
s = rep(s, '''out.push("코스인데 구성이 비어 있습니다 — '코스 미정' 으로 두거나 구성을 넣으세요");''',
           '''out.push("%s인데 구성이 비어 있습니다 — '%s 미정' 으로 두거나 구성을 넣으세요");''' % (L, L))
save("js/15-sheets.js", s)

# ---- 설정 ----
s = load("js/14-settings.js")
s = rep(s, '${sec("course","코스 구성",', '${sec("course","%s 구성",' % L)
s = rep(s, '예약 시각에 맞는 행이 코스 선택 팝업에서 강조됩니다.', '예약 시각에 맞는 행이 %s 선택 팝업에서 강조됩니다. 저녁 코스는 종일, 점심 세트는 점심 시간에만 팝니다.' % L)
save("js/14-settings.js", s)

# ---- 마법사 ----
s = load("js/16-wizard.js")
s = rep(s, '"\\u201C식사는 코스로 준비해 드릴까요?\\u201D",', '"\\u201C식사는 코스나 세트로 준비해 드릴까요?\\u201D",')
s = rep(s, 'if(WZ.menuType==="해당 없음") out.push("룸인데 코스가 아님");', 'if(WZ.menuType==="해당 없음") out.push("룸인데 %s가 아님");' % L)
s = rep(s, 'if(WZ.menuType==="확인 필요") out.push("룸인데 코스 여부 미확인");', 'if(WZ.menuType==="확인 필요") out.push("룸인데 %s 여부 미확인");' % L)
s = rep(s, 'out.push(`코스 부족 - ${n}인분 / 성인 ${adults}명`);', 'out.push(`%s 부족 - ${n}인분 / 성인 ${adults}명`);' % L)
s = rep(s, 'out.push(`코스 초과 - ${n}인분 / 성인 ${adults}명`);', 'out.push(`%s 초과 - ${n}인분 / 성인 ${adults}명`);' % L)
s = rep(s, '''    ? [["코스","코스",""],
       ["해당 없음","해당 없음",""]]
    : [["코스","코스",""],''',
           '''    ? [["코스","%s",""],
       ["해당 없음","해당 없음",""]]
    : [["코스","%s",""],''' % (L, L))
s = rep(s, 'WZ.menuType==="해당 없음" ? "룸 예약에 코스 이용 예정 손님이 아닙니다" :', 'WZ.menuType==="해당 없음" ? "룸 예약에 %s 이용 예정 손님이 아닙니다" :' % L)
s = rep(s, '? `코스 ${n}인분 · 성인 ${adults}명보다 적습니다` : "");', '? `%s ${n}인분 · 성인 ${adults}명보다 적습니다` : "");' % L)
s = rep(s, '${WZ.courseUndecided ? "코스 미정 · 방문 전 확정" :', '${WZ.courseUndecided ? "%s 미정 · 방문 전 확정" :' % L)
s = rep(s, '<div class="sheet-h"><h2>코스 선택</h2>', '<div class="sheet-h"><h2>%s 선택</h2>' % L)
s = rep(s, '''          코스 미정
        </button>''', '''          %s 미정
        </button>''' % L)
s = rep(s, '${short?`<div class="ct-warn">코스 부족 - 성인보다 ${ad-n}명 적음</div>`:""}', '${short?`<div class="ct-warn">%s 부족 - 성인보다 ${ad-n}명 적음</div>`:""}' % L)
s = rep(s, 'if(offNames.length) out.push(`이 시간엔 없는 코스 - ${offNames.join(", ")}`);', 'if(offNames.length) out.push(`이 시간엔 없는 %s - ${offNames.join(", ")}`);' % L)
s = rep(s, 'if(picked.length >= 2) out.push(`코스 ${picked.length}종류 - 한 테이블은 하나로`);', 'if(picked.length >= 2) out.push(`%s ${picked.length}종류 - 한 테이블은 하나로`);' % L)
save("js/16-wizard.js", s)
js_check()
print("코스·세트 표기 끝")
