# -*- coding: utf-8 -*-
"""재아 묶음(2026-09-16 오후): 인트로 속도 · 네이버 시트 · Enter/Esc · 문자 설정 정리 · '홈페이지 예약' 이름 ·
   24시간 만료 카운트다운 · 새 요청 팝업 · 사용 중지 알약 라벨 · 초과 칸 라벨 · '지금 | 시각' · TV 주소 · 입력 글씨 · 중지 겹침 검사"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patchlib import load, save, rep, js_check

# ---------- 인트로 1.7배 빠르게 ----------
s = load("js/04-render.js")
s = rep(s, "var steps = INTRO_TO.length, t0 = 120, gap = 150;   /* 8차-AA(재아): 조금 더 빠르게 — 글자 150ms 간격, 총 1.3초쯤 */",
           "var steps = INTRO_TO.length, t0 = 70, gap = 88;   /* 재아: 1.7배 빠르게 — 글자 88ms 간격, 총 0.8초쯤 */")
s = rep(s, "introTimers.push(setTimeout(endIntro, t0 + steps*gap + 450));", "introTimers.push(setTimeout(endIntro, t0 + steps*gap + 265));")
save("js/04-render.js", s)

# ---------- 네이버 가져오기: 확인 / 신규 N건 · 수정 N건 · 등록 / 닫기는 같은 줄 맨 오른쪽 ----------
s = load("js/15-sheets.js")
s = rep(s, '''    <div class="btn-row" style="margin-top:8px">
      <button class="btn" onclick="naverPreview()">미리보기</button>
      ${n.result ? `<button class="btn primary" onclick="naverApply()" ${cnt("new")+cnt("update")?"":"disabled"}>새로 ${cnt("new")} · 고침 ${cnt("update")} 적용</button>` : ""}
    </div>
    ${res}
    <div class="sheet-actions"><button class="btn ghost" onclick="closeSheet()">닫기</button></div>`;''',
'''    <div class="btn-row" style="margin-top:8px">
      <button class="btn" data-enter onclick="naverPreview()">확인</button>
      ${n.result ? `<button class="btn primary" data-enter onclick="naverApply()" ${cnt("new")+cnt("update")?"":"disabled"}>신규 ${cnt("new")}건 · 수정 ${cnt("update")}건 · 등록</button>` : ""}
      <button class="btn ghost" style="margin-left:auto" onclick="closeSheet()">닫기</button>
    </div>
    ${res}`;''')
s = rep(s, 'logEvent("네이버 가져오기", `새로 ${added} · 고침 ${updated}`);', 'logEvent("네이버 가져오기", `신규 ${added} · 수정 ${updated}`);')
s = rep(s, 'uiAlert("네이버 예약 가져오기 완료", `새로 ${added}건, 고침 ${updated}건.', 'uiAlert("네이버 예약 가져오기 완료", `신규 ${added}건, 수정 ${updated}건.')

# ---------- 예약 목록 '지금 | 오후 4:50' ----------
save("js/15-sheets.js", s)
s = load("js/07-dash.js")
s = rep(s, '`<div class="now-sep"><span>지금 ${hm(nowHM())}</span></div>`', '`<div class="now-sep"><span>지금 | ${hm(nowHM())}</span></div>`')
s = rep(s, '`<div class="now-sep"><span>지금 ${hm(nowHM())} · 오늘 남은 예약 없음</span></div>`', '`<div class="now-sep"><span>지금 | ${hm(nowHM())} · 오늘 남은 예약 없음</span></div>`')
save("js/07-dash.js", s)

# ---------- Enter → 확인/등록(data-enter 또는 .btn.primary), Esc → 닫기 ----------
s = load("js/18-router.js")
s += '''
/* 시트·마법사 어디서든: Enter = 그 창의 확인·등록 단추(data-enter 가 있으면 그것, 없으면 .btn.primary 하나뿐일 때만),
   Esc = 닫기. 여러 줄 입력(textarea) 안에서 Enter 는 줄바꿈이라 건드리지 않습니다. '이전' 은 일부러 안 묶습니다(재아) */
document.addEventListener("keydown", function(e){
  if(e.key === "Escape"){
    if(document.querySelector(".modal-ov")) return;   /* 확인창은 자기 Esc 처리가 있음 */
    if(view.form){ e.preventDefault(); closeSheet(); }
    else if(view.moreOpen){ closeMore(); }
    return;
  }
  if(e.key !== "Enter" || e.ctrlKey || e.altKey || e.isComposing) return;
  const t = e.target;
  if(t && (t.tagName === "TEXTAREA" || t.tagName === "BUTTON" || t.tagName === "A" || t.isContentEditable)) return;
  if(document.querySelector(".modal-ov")) return;
  const sheet = document.querySelector(".sheet");
  if(!sheet) return;
  let btn = sheet.querySelector("[data-enter]:not(:disabled)");
  if(!btn){ const ps = sheet.querySelectorAll(".sheet-actions .btn.primary:not(:disabled)"); if(ps.length === 1) btn = ps[0]; }
  if(btn){ e.preventDefault(); btn.click(); }
});
'''
save("js/18-router.js", s)

# ---------- 문자 설정 정리 ----------
s = load("js/09-sms.js")
s = rep(s, 'function offsetLabel(o){ return o === 2 ? "2일 전" : o === 1 ? "1일 전 (전날)" : "당일 아침"; }',
           'function offsetLabel(o){ return o === 2 ? "2일 전" : o === 1 ? "1일 전" : "당일 아침"; }\n/* 재안내 시각 알약 — 30분 선택지가 없으니 "오전 9시" 로 짧게 */\nfunction hourLabel(h){ return (h < 12 ? "오전 " : "오후 ") + (h % 12 === 0 ? 12 : h % 12) + "시"; }')
save("js/09-sms.js", s)
s = load("js/01-data.js")
s = rep(s, '  storePhone:"",          /* 발신번호 — 문자에 찍히는 번호. 실제 발송을 붙일 때 필요합니다 */',
           '  storePhone:"031-724-1004",   /* 발신번호 — 매장 번호. 실제 발송을 붙일 때 통신사에 등록 */')
save("js/01-data.js", s)
s = load("js/14-settings.js")
s = rep(s, '''    <div class="mockbar">지금은 <b>흉내만</b> 냅니다. 실제로 문자가 나가지 않습니다.
      화면과 문구를 먼저 정하고, 발송은 나중에 붙입니다.</div>

    <div class="subhead">문자 안내</div>''', '''    <div class="subhead">문자 안내</div>''')
s = rep(s, '''    <input id="sms-phone" type="tel" value="${esc(sm.storePhone||"")}"
      placeholder="031-000-0000" oninput="setSms('storePhone',this.value)">
    <p class="f-note">실제로 문자를 보내려면 이 번호를 통신사에 미리 등록해야 합니다.
      지금은 적어만 둡니다.</p>''', '''    <input id="sms-phone" type="tel" class="in-sm" value="${esc(sm.storePhone||"031-724-1004")}"
      placeholder="031-724-1004" oninput="setSms('storePhone',this.value)">
    <p class="f-note">실제로 문자를 보내려면 이 번호를 통신사에 미리 등록해야 합니다.</p>''')
s = rep(s, '''    <div class="hourpick">
      ${remindHours(sm.remindOffset).map(h=>`<button class="${sm.remindHour===h?'on':''}"
        onclick="setSms('remindHour',${h})">${hm(pad(h)+":00")}</button>`).join("")}
    </div>''', '''    <div class="seg" style="margin-top:8px">
      ${remindHours(sm.remindOffset).map(h=>`<button class="${sm.remindHour===h?'on':''}"
        onclick="setSms('remindHour',${h})">${hourLabel(h)}</button>`).join("")}
    </div>''')
s = rep(s, '''    <textarea id="sms-park" rows="3" placeholder="비워 두면 문자에 안 들어갑니다"
      onchange="setSms('parkingNote',this.value)">''', '''    <textarea id="sms-park" rows="3" class="in-sm" placeholder="비워 두면 문자에 안 들어갑니다"
      onchange="setSms('parkingNote',this.value)">''')
# 문안 옆에 미리보기 단추, 아래 '이렇게 나갑니다' 블록은 뺌
s = rep(s, '''    <div class="subhead">접수 문자 문안 <span>예약을 받은 즉시</span></div>
    <textarea id="sms-tpl-new" rows="9" onchange="setSms('tplNew',this.value)">${esc(sm.tplNew||SMS_DEFAULT.tplNew)}</textarea>
    <div class="btn-row" style="margin:6px 0 12px"><button class="btn sm" onclick="setSms('tplNew',SMS_DEFAULT.tplNew)">기본 문안으로</button></div>
    <div class="subhead">재안내 문자 문안 <span>방문 전 재안내</span></div>
    <textarea id="sms-tpl-rem" rows="12" onchange="setSms('tplRemind',this.value)">${esc(sm.tplRemind||SMS_DEFAULT.tplRemind)}</textarea>
    <div class="btn-row" style="margin:6px 0 0"><button class="btn sm" onclick="setSms('tplRemind',SMS_DEFAULT.tplRemind)">기본 문안으로</button></div>''',
'''    <div class="subhead">접수 문자 문안 <span>예약을 받은 즉시</span></div>
    <textarea id="sms-tpl-new" rows="9" class="in-sm" onchange="setSms('tplNew',this.value)">${esc(sm.tplNew||SMS_DEFAULT.tplNew)}</textarea>
    <div class="btn-row" style="margin:6px 0 12px"><button class="btn sm" onclick="setSms('tplNew',SMS_DEFAULT.tplNew)">기본 문안으로</button><button class="btn sm" onclick="previewSms('접수')">미리보기</button></div>
    <div class="subhead">재안내 문자 문안 <span>방문 전 재안내</span></div>
    <textarea id="sms-tpl-rem" rows="12" class="in-sm" onchange="setSms('tplRemind',this.value)">${esc(sm.tplRemind||SMS_DEFAULT.tplRemind)}</textarea>
    <div class="btn-row" style="margin:6px 0 0"><button class="btn sm" onclick="setSms('tplRemind',SMS_DEFAULT.tplRemind)">기본 문안으로</button><button class="btn sm" onclick="previewSms('재안내')">미리보기</button></div>''')
s = rep(s, '''    <div class="subhead">이렇게 나갑니다</div>
    <div class="smsprev">
      <div class="sp-h">접수 문자 <span>예약을 받은 즉시</span></div>
      <div class="smsmsg">${esc(smsText(smsSample,"접수"))}</div>
    </div>
    <div class="smsprev">
      <div class="sp-h">재안내 문자 <span>${esc(offsetLabel(sm.remindOffset))} ${esc(hm(pad(sm.remindHour)+":00"))}</span></div>
      <div class="smsmsg">${esc(smsText(smsSample,"재안내",sm.remindOffset))}</div>
    </div>
    <p class="f-note">점선 사이가 손님께 가는 내용입니다. 점선은 화면에만 그려집니다.<br>
      보내는 시점을 바꾸면 “모레 / 내일 / 오늘” 이 자동으로 바뀝니다.
      어린이가 있는 예약이면 인원이 “4명(어린이 1명 포함)” 처럼 나갑니다.</p>
''', '''    <p class="f-note">보내는 시점을 바꾸면 “모레 / 내일 / 오늘” 이 자동으로 바뀝니다. 어린이가 있는 예약이면 인원이 “4명(어린이 1명 포함)” 처럼 나갑니다.</p>
''')
s = rep(s, '''  const etcBody = `''', '''  /* 문안 옆 '미리보기' — 가짜 예약으로 채운 문자를 확인창에 */
  window.previewSms = function(kind){
    const smNow = { ...SMS_DEFAULT, ...(draft().sms||{}) };
    const sample = { ...smsSample, date: shiftDate(todayStr(), smNow.remindOffset) };
    const text = kind === "접수" ? smsText(sample, "접수") : smsText(sample, "재안내", smNow.remindOffset);
    uiAlert(kind === "접수" ? "접수 문자 — 이렇게 나갑니다" : `재안내 문자 — ${offsetLabel(smNow.remindOffset)} ${hourLabel(smNow.remindHour)}`, text, "ok");
  };
  const etcBody = `''')
# 광고 영상 이름 입력도 작은 글씨
s = rep(s, '<input id="tv-ad" value="${esc(st.tvAd||"")}" placeholder="ad.mp4"', '<input id="tv-ad" class="in-sm" value="${esc(st.tvAd||"")}" placeholder="ad.mp4"')
# TV 전용 주소: 실제 링크 + 오른쪽에 복사, 안내 문장 삭제
s = rep(s, '''    <div class="urlbox">
      <div class="ub-t">TV 전용 주소</div>
      <div class="ub-u" id="screen-url">${esc(screenUrl())}</div>
      <div class="ub-s">TV 브라우저 주소창에 이 주소를 넣으면 PIN 없이 바로 이 화면이 열립니다.</div>
      <button class="btn sm" onclick="copyScreenUrl()">주소 복사</button>
    </div>''', '''    <div class="urlbox">
      <div class="ub-t">TV 전용 주소</div>
      <div class="ub-row"><a class="ub-u" id="screen-url" href="${esc(screenUrl())}" target="_blank" rel="noopener">${esc(screenUrl())}</a><button class="btn sm" onclick="copyScreenUrl()">주소 복사</button></div>
    </div>''')
s = rep(s, '''    if(location.protocol === "file:") return location.href.split("#")[0] + `#/screen/${view.storeKey}`;
    return location.origin + appDir() + "/screen/";''', '''    /* 로컬(127.0.0.1·file:)에서 열어도 TV 에 넣을 주소는 실제 배포 주소여야 합니다(재아) */
    if(/^(127\\.|localhost|file:)/.test(location.host || location.protocol)) return "https://jaealee.com/test/hanok/v7/screen/";
    return location.origin + appDir() + "/screen/";''')
save("js/14-settings.js", s)

# ---------- 사용 중지: 겹치는 구간이 있으면 막기 ----------
s = load("js/15-sheets.js")
s = rep(s, '''  const hits = blockHits(room, d);
  if(hits.length){''', '''  /* 이미 사용 중지인 구간과 겹치면 넣지 않습니다 — 겹친 구간이 둘이면 나중에 하나만 지워도 남아서 헷갈립니다(재아) */
  const dup = (room.blocks||[]).find(function(b){
    if(b.id === d.id) return false;
    const aS = d.from, aE = d.openEnded ? "9999-12-31" : (d.to || d.from);
    const bS = b.from, bE = b.openEnded ? "9999-12-31" : (b.to || b.from);
    if(aE < bS || bE < aS) return false;              /* 날짜가 안 겹침 */
    if(d.allDay || b.allDay) return true;              /* 하루 종일이면 겹침 */
    if(aS !== aE || bS !== bE) return true;            /* 여러 날짜면 사이 날이 종일이라 겹침 */
    return !(d.toTime <= b.fromTime || b.toTime <= d.fromTime);   /* 같은 날 시각 비교 */
  });
  if(dup) return uiAlert("이미 사용 중지가 있습니다", `${dup.from}${dup.openEnded?" ~ (기한 없음)":dup.to&&dup.to!==dup.from?` ~ ${dup.to}`:""}${dup.allDay?" 하루 종일":` ${hm(dup.fromTime)} ~ ${hm(dup.toTime)}`}${dup.note?` · ${dup.note}`:""}\\n\\n겹치는 기간은 넣을 수 없습니다. 기존 것을 고치거나 지운 뒤 다시 넣으세요.`, "warn");
  const hits = blockHits(room, d);
  if(hits.length){''')
save("js/15-sheets.js", s)

# ---------- 타임라인: 사용 중지 라벨을 빗금 위에, 초과 칸 라벨 ----------
s = load("js/10-timeline.js")
s = rep(s, '''    return `<span class="blockband" style="left:${pos(s)}%; width:${((e-s)/span)*100}%"
      title="사용 중지 · ${esc(spanLabel(sp))}${sp.note?` · ${esc(sp.note)}`:""}"></span>`;''',
'''    return `<span class="blockband" style="left:${pos(s)}%; width:${((e-s)/span)*100}%"
      title="사용 중지 · ${esc(spanLabel(sp))}${sp.note?` · ${esc(sp.note)}`:""}"><i class="bb-l">사용 중지${sp.note?` (${esc(sp.note)}${sp.allDay?"":" · "+esc(spanLabel(sp))})`:` (${esc(spanLabel(sp))})`}</i></span>`;''')
s = rep(s, '''      + (over ? `<div class="offband overlane" style="left:0; right:0; top:0; height:${LANE}px" title="테이블 수를 넘은 팀이 놓이는 칸"></div>` : "");''',
'''      + (over ? `<div class="offband overlane" style="left:0; right:0; top:0; height:${LANE}px" title="테이블 수를 넘은 팀이 놓이는 칸"><i class="ol-l">자리 없음 ${over}팀 — 테이블 수를 넘은 예약</i></div>` : "");''')
save("js/10-timeline.js", s)

c = load("css/05-dash.css")
c += '''
/* 사용 중지 빗금 위 라벨 — 예약 블록과 겹치지 않게 맨 위 한 줄, 작은 글씨 */
.blockband{overflow:visible}
.blockband .bb-l{position:absolute; left:6px; top:2px; font-style:normal; font-size:11px; font-weight:700; color:var(--rust); background:rgba(255,255,255,.85); padding:0 6px; border-radius:3px; white-space:nowrap; pointer-events:none; z-index:2}
/* 테이블 초과 칸 라벨 */
.overlane .ol-l{position:absolute; left:6px; top:2px; font-style:normal; font-size:11px; font-weight:700; color:var(--rust); background:rgba(255,255,255,.85); padding:0 6px; border-radius:3px; white-space:nowrap; pointer-events:none}
'''
save("css/05-dash.css", c)

# ---------- 설정 입력 글씨: 미리보기(문자) 크기와 같게 ----------
c = load("css/07-settings.css")
c += '''
/* 설정의 긴 입력칸(발신번호·문안·주차 안내·광고 영상 이름)은 본문 크기로 — 제목 크기라 너무 컸습니다(재아) */
.in-sm{font-size:var(--fs-sub) !important; line-height:1.65}
/* TV 주소: 링크 + 오른쪽 복사 */
.ub-row{display:flex; align-items:center; gap:var(--s8)}
.ub-row .ub-u{flex:1; min-width:0; overflow-wrap:anywhere; text-decoration:underline; text-underline-offset:3px; margin:0}
'''
save("css/07-settings.css", c)
js_check()
print("batch2 ok")
