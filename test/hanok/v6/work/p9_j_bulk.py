# -*- coding: utf-8 -*-
"""8차-J: 임시 일정 일괄 등록 도구 (sheetOverride 아래)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()

JS = r'''
/* ---------- 임시 일정 일괄 등록 (8차-J, 재아 요청) ----------
   한 줄에 하나. `날짜 | 메모 | 내용`. 메모는 비워도 됩니다. 날짜는 2026-12-31 또는 2026-12-24~2026-12-26.
   내용은 `휴무` 또는 `영업 11:00-23:00` 에 `라스트오더 22:00`(또는 `라스트오더 없음`)·`브레이크 15:00-17:00`(또는 `브레이크 없음`) 을 덧붙임.
   영업 시간이 없는데 휴무도 아니면 오류. 미리보기에서 줄마다 결과를 보고 '적용' 하면 맞는 줄만 들어갑니다(같은 날짜는 덮어씀). */
const BULK_OVR_GUIDE = "날짜 | 메모 | 내용   (한 줄에 하나, 메모는 비워도 됨)\n2026-09-16 | 임시공휴일 | 휴무\n2026-12-31 | 연말 | 영업 11:00-23:00 라스트오더 22:00 브레이크 없음\n2026-12-24~2026-12-26 | 크리스마스 | 영업 11:00-22:00 브레이크 15:00-17:00";
function bulkOvrHtml(){
  const b = view.ovrBulk || {text:"", result:null};
  const res = b.result ? `<div class="bulk-res">${b.result.map(x=>`<div class="bulk-row ${x.ok?'ok':'bad'}"><span class="bulk-ln">${x.n}</span><span class="grow">${esc(x.text)}</span><span class="bulk-msg">${x.ok?`✓ ${esc(x.msg)}`:`✗ ${esc(x.msg)}`}</span></div>`).join("")}</div>` : "";
  const okN = b.result ? b.result.filter(x=>x.ok).length : 0, badN = b.result ? b.result.length - okN : 0;
  return `
    <div class="sect-title" style="margin-top:20px">일괄 등록 <span class="lbl-note">여러 날을 한 번에</span></div>
    <pre class="bulk-guide">${esc(BULK_OVR_GUIDE)}</pre>
    <textarea id="ovr-bulk" rows="6" placeholder="여기에 붙여 넣으세요" oninput="setOvrBulk(this.value)">${esc(b.text)}</textarea>
    <div class="btn-row" style="margin-top:8px">
      <button class="btn" onclick="copyBulkPrompt()">AI 에게 시킬 프롬프트 복사</button>
      <button class="btn" onclick="bulkPreview()">미리보기</button>
      ${b.result ? `<button class="btn primary" onclick="bulkApply()" ${okN?"":"disabled"}>맞는 ${okN}줄 적용${badN?` (오류 ${badN}줄 제외)`:""}</button>` : ""}
    </div>
    ${res}`;
}
function setOvrBulk(v){ view.ovrBulk = {text:v, result:null}; }   /* 글자마다 render 하지 않습니다(입력 유실) */
function parseOvrLine(line){
  const parts = line.split("|").map(x=>x.trim());
  if(parts.length < 2) return {ok:false, msg:"‘|’ 로 나눈 칸이 두 개 이상이어야 합니다 (날짜 | 메모 | 내용)"};
  const dateRaw = parts[0].replace(/\./g,"-").replace(/\s/g,""), note = parts.length >= 3 ? parts[1] : "", spec = (parts.length >= 3 ? parts.slice(2).join(" ") : parts[1]).trim();
  const dm = dateRaw.match(/^(\d{4}-\d{2}-\d{2})(?:~(\d{4}-\d{2}-\d{2}))?$/);
  if(!dm) return {ok:false, msg:"날짜는 2026-12-31 또는 2026-12-24~2026-12-26 형식"};
  const from = dm[1], to = dm[2] || dm[1];
  if(isNaN(new Date(from+"T00:00:00")) || isNaN(new Date(to+"T00:00:00")) || to < from) return {ok:false, msg:"날짜가 이상합니다"};
  const dates = []; for(let d = from; d <= to && dates.length < 62; d = shiftDate(d, 1)) dates.push(d);
  if(/^(휴무|휴업|쉼|닫음)$/.test(spec.replace(/\s/g,""))) return {ok:true, dates, rec:{closed:true, note:note||"휴무"}, msg:`${dates.length}일 휴무`};
  const t = spec.replace(/\s+/g," ");
  const open = t.match(/영업\s*(\d{1,2}:\d{2})\s*[-~]\s*(\d{1,2}:\d{2})/);
  if(!open) return {ok:false, msg:"‘휴무’ 이거나 ‘영업 11:00-22:00’ 처럼 영업 시간이 있어야 합니다"};
  const pad2 = x => x.length === 4 ? "0" + x : x;
  const base = hoursFor(from);
  const rec = {closed:false, open:pad2(open[1]), close:pad2(open[2]), bs:"", be:"", lo:"", note:note||"임시 운영시간"};
  const lo = t.match(/(?:라스트오더|LO|lo)\s*(\d{1,2}:\d{2})/);
  const loNone = /(?:라스트오더|LO|lo)\s*(?:없음|없|x|X)/.test(t);
  if(lo) rec.lo = pad2(lo[1]); else if(!loNone) rec.lo = base.lo || "";
  const br = t.match(/브레이크\s*(\d{1,2}:\d{2})\s*[-~]\s*(\d{1,2}:\d{2})/);
  const brNone = /브레이크\s*(?:없음|없|x|X)/.test(t);
  if(br){ rec.bs = pad2(br[1]); rec.be = pad2(br[2]); } else if(!brNone){ rec.bs = base.bs || ""; rec.be = base.be || ""; }
  if(toMin(rec.close) <= toMin(rec.open)) return {ok:false, msg:"종료가 시작보다 빠릅니다"};
  return {ok:true, dates, rec, msg:`${dates.length}일 · ${rec.open}~${rec.close}${rec.bs?` 브레이크 ${rec.bs}~${rec.be}`:" 브레이크 없음"}${rec.lo?` 라스트오더 ${rec.lo}`:" 라스트오더 없음"}`};
}
function bulkPreview(){
  const ta = document.getElementById("ovr-bulk"); const text = ta ? ta.value : (view.ovrBulk ? view.ovrBulk.text : "");
  const lines = text.split(/\r?\n/).map(x=>x.trim()).filter(x=>x && !/^날짜\s*\|/.test(x));
  const result = lines.map((ln, i)=>Object.assign({n:i+1, text:ln}, parseOvrLine(ln)));
  view.ovrBulk = {text, result}; render();
}
async function bulkApply(){
  const b = view.ovrBulk; if(!b || !b.result) return;
  if(readonlyBlock()) return;
  const st = store().settings; let n = 0;
  b.result.filter(x=>x.ok).forEach(x=>{ x.dates.forEach(d=>{
    st.overrides = (st.overrides||[]).filter(o=>o.date!==d).concat([Object.assign({date:d}, x.rec)]); n++;
  }); });
  mirrorDraft("overrides");
  logEvent("설정 변경", `임시 일정 일괄 ${n}일`);
  view.ovrBulk = null; saveData(); render();
  uiAlert("일괄 등록 완료", `${n}일이 들어갔습니다. 위 목록에서 확인하세요.`, "ok");
}
async function copyBulkPrompt(){
  const txt = "아래 형식으로 한 줄에 하루씩 써 줘. 다른 말은 붙이지 말고 줄만.\n형식: 날짜 | 메모 | 내용\n- 날짜: 2026-12-31 처럼. 연속이면 2026-12-24~2026-12-26\n- 내용: \"휴무\" 또는 \"영업 11:00-22:00\" 뒤에 \"라스트오더 21:00\"(없으면 \"라스트오더 없음\"), \"브레이크 15:00-17:00\"(없으면 \"브레이크 없음\")\n예)\n2026-09-16 | 임시공휴일 | 휴무\n2026-12-31 | 연말 | 영업 11:00-23:00 라스트오더 22:00 브레이크 없음\n\n내가 원하는 것: ";
  try{ await navigator.clipboard.writeText(txt); uiAlert("복사했습니다", "AI 채팅에 붙여 넣고 뒤에 원하는 날짜·조건을 말하면 됩니다.", "ok"); }
  catch(e){ uiAlert("복사가 막혔습니다 — 아래를 직접 복사하세요", txt, "warn"); }
}
'''

s = L.rep(s, """    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="saveOverride()">추가</button>
    </div>`;
}""", """    <div class="sheet-actions">
      <button class="btn ghost" onclick="closeSheet()">닫기</button>
      <button class="btn primary" onclick="saveOverride()">추가</button>
    </div>
    ${bulkOvrHtml()}`;
}""" + JS)

s = L.rep(s, """.offline-card{padding:var(--s24); text-align:center}""", """/* 임시 일정 일괄 등록 */
.bulk-guide{margin:0 0 var(--s8); padding:var(--s8) var(--s12); background:var(--surface-2); border-radius:var(--r-sm); font-size:var(--fs-label); line-height:1.6; white-space:pre-wrap; color:var(--text-2); font-family:var(--sans)}
#ovr-bulk{width:100%; font:inherit; font-size:var(--fs-sub); padding:var(--s8) var(--s12); border:1px solid var(--border-strong); border-radius:var(--r-sm); resize:vertical}
.bulk-res{margin-top:var(--s12); border:1px solid var(--border); border-radius:var(--r-sm); overflow:hidden}
.bulk-row{display:flex; gap:var(--s8); align-items:flex-start; padding:var(--s8) var(--s12); font-size:var(--fs-sub); border-top:1px solid var(--border)}
.bulk-row:first-child{border-top:none}
.bulk-row.ok{background:#F1F7F2} .bulk-row.bad{background:#FBEFEC}
.bulk-ln{flex:none; width:20px; color:var(--text-3)} .bulk-row .grow{flex:1; min-width:0; word-break:break-all}
.bulk-msg{flex:none; max-width:46%; color:var(--text-2)} .bulk-row.bad .bulk-msg{color:var(--rust)}
.offline-card{padding:var(--s24); text-align:center}""")
L.js_check(s)
L.save(s)
print("bulk ok")
