# -*- coding: utf-8 -*-
"""8차-M: 네이버 예약 엑셀 가져오기 — 엑셀에서 줄을 복사해 붙여 넣으면(탭 구분) 머리글을 찾아 예약번호 기준으로 새로 넣거나 고칩니다.
   전화번호는 네이버가 뒷자리 4개만 주므로 메모에 남기고, 이름은 가려진 그대로. 룸/테이블 상품 → room-any / table-any."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

JS = r'''
/* ---------- 네이버 예약 가져오기 (8차-M) ----------
   네이버 파트너센터 '예약자 관리' 엑셀을 열어 표 전체를 복사(Ctrl+A, Ctrl+C)해 붙여 넣습니다. 탭으로 나뉜 줄이 들어옵니다.
   머리글 줄(예약번호 · 상태 · 예약자 · 이용일시 · 상품 · 인원 · 옵션 · 요청사항 …)을 찾아 열 이름으로 읽으므로 열 순서가 바뀌어도 됩니다.
   · 예약번호(naverNo)로 같은 예약을 찾아 있으면 고치고(상태·시각·인원·요청) 없으면 새로 넣습니다
   · 전화번호는 뒷자리 4개만 오므로 phone 은 비우고 메모에 '네이버 ****1234' 를 남깁니다 — 노쇼 이력은 못 잇습니다
   · 상품에 '룸' 이 있으면 룸 미정(room-any), '테이블' 이면 테이블(층 미정, table-any). 자리는 잠정 배정이 잡습니다
   · 옵션 열(주말 A 세트·주말 B 세트·한코스 …)은 수량이 있으면 코스 구성으로. 이름이 코스 항목과 안 맞으면 요청사항에 적어 둡니다 */
function openNaver(){ view.form = {type:"naver"}; view.naver = view.naver || {text:"", result:null}; render(); }
function sheetNaver(){
  const n = view.naver || {text:"", result:null};
  const res = n.result ? `<div class="bulk-res">${n.result.map(x=>`<div class="bulk-row ${x.ok?(x.kind==="skip"?"":"ok"):"bad"}"><span class="bulk-ln">${x.n}</span><span class="grow">${esc(x.text)}</span><span class="bulk-msg">${x.ok?`${x.kind==="new"?"＋ 새로":x.kind==="update"?"↻ 고침":"＝ 같음"} · ${esc(x.msg)}`:`✗ ${esc(x.msg)}`}</span></div>`).join("")}</div>` : "";
  const cnt = k => n.result ? n.result.filter(x=>x.ok && x.kind===k).length : 0;
  return `
    ${sheetHead("네이버 예약 가져오기")}
    <p class="f-note" style="margin:-6px 0 10px">네이버 파트너센터 → 예약자 관리 → 엑셀 다운로드 → 파일을 열어 <b>표 전체 복사(Ctrl+A, Ctrl+C)</b> → 아래에 붙여 넣기(Ctrl+V).
      예약번호로 같은 예약을 찾아 고치고, 없으면 새로 넣습니다. 전화번호는 네이버가 뒷자리만 주어 메모에만 남습니다.</p>
    <textarea id="naver-paste" rows="7" placeholder="여기에 붙여 넣으세요 (머리글 줄 포함, 안내 문장이 섞여 있어도 됩니다)" oninput="view.naver={text:this.value, result:null}">${esc(n.text)}</textarea>
    <div class="btn-row" style="margin-top:8px">
      <button class="btn" onclick="naverPreview()">미리보기</button>
      ${n.result ? `<button class="btn primary" onclick="naverApply()" ${cnt("new")+cnt("update")?"":"disabled"}>새로 ${cnt("new")} · 고침 ${cnt("update")} 적용</button>` : ""}
    </div>
    ${res}
    <div class="sheet-actions"><button class="btn ghost" onclick="closeSheet()">닫기</button></div>`;
}
/* '26. 8. 17.(월) 오후 12:00' → {date:"2026-08-17", time:"12:00"} */
function naverWhen(s){
  const m = String(s||"").match(/(\d{2,4})\.\s*(\d{1,2})\.\s*(\d{1,2})\.?[^0-9]*?(오전|오후)?\s*(\d{1,2}):(\d{2})/);
  if(!m) return null;
  let y = Number(m[1]); if(y < 100) y += 2000;
  let h = Number(m[5]); const ap = m[4];
  if(ap === "오후" && h < 12) h += 12; if(ap === "오전" && h === 12) h = 0;
  return { date: `${y}-${pad(Number(m[2]))}-${pad(Number(m[3]))}`, time: `${pad(h)}:${m[6]}` };
}
/* '4명/성인(3),어린이(1)' → {people:4, infants:1} */
function naverPeople(s){
  const t = String(s||""); const tot = t.match(/(\d+)\s*명/); const kid = t.match(/(?:어린이|유아|아동)\((\d+)\)/);
  return { people: tot ? Number(tot[1]) : 0, infants: kid ? Number(kid[1]) : 0 };
}
function naverParse(text){
  const lines = text.split(/\r?\n/).map(l=>l.replace(/\r/g,"")).filter(l=>l.trim());
  const hi = lines.findIndex(l=>/예약번호/.test(l) && /\t/.test(l));
  if(hi < 0) return {err:"머리글 줄(예약번호 … 이용일시 … 인원)을 못 찾았습니다. 엑셀에서 표 전체를 복사해 붙여 넣으세요."};
  const head = lines[hi].split("\t").map(x=>x.trim());
  const col = name => head.findIndex(h=>h === name);
  const idx = { no:col("예약번호"), status:col("상태"), name:col("예약자"), phone:col("전화번호"), when:col("이용일시"), prod:col("상품"), ppl:col("인원"), req:col("요청사항"), memo:col("직원메모"), cancelWhy:col("취소사유"), route:col("유입경로") };
  if(idx.no < 0 || idx.when < 0) return {err:"예약번호·이용일시 열이 필요합니다"};
  /* 옵션 열: '옵션1-주말 A 세트' 처럼 이름이 붙은 것 중 '결제금액' 이 아닌 것 */
  const opts = head.map((h,i)=>({h,i})).filter(x=>/^옵션\d+-/.test(x.h) && !/결제금액$/.test(x.h)).map(x=>({i:x.i, name:x.h.replace(/^옵션\d+-/,"").replace(/^한옥반점\s*/,"").trim()}));
  const st = store().settings, groups = st.courseGroups || DEFAULT_COURSE_GROUPS;
  const rows = [];
  for(let k = hi + 1; k < lines.length; k++){
    const c = lines[k].split("\t"); if(c.length < head.length - 5) continue;
    const g = i => i >= 0 && i < c.length ? String(c[i]||"").trim() : "";
    const no = g(idx.no); if(!/^\d{5,}$/.test(no)) continue;
    const when = naverWhen(g(idx.when)); const pp = naverPeople(g(idx.ppl));
    const stRaw = g(idx.status), prod = g(idx.prod);
    const status = /취소|거절/.test(stRaw) ? "취소" : /이용완료|완료/.test(stRaw) ? "방문" : /노쇼|미방문/.test(stRaw) ? "노쇼" : "확정";
    const isRoomProd = /룸/.test(prod);
    /* 옵션 수량 → 코스. 이름이 코스 항목(A·B·한 등)과 맞는 것만 */
    const courses = {}; const unmatched = [];
    opts.forEach(o=>{ const q = Number(g(o.i)) || 0; if(!q) return;
      if(/테이블 예약|룸 예약/.test(o.name)) return;   /* 자리 옵션은 코스가 아님 */
      const gid = when && when.time >= "17:00" ? "cg_dinner" : (when && isWeekendDay(when.date) ? "cg_welunch" : "cg_wdlunch");
      const grp = groups.find(x=>x.id===gid) || groups[0];
      const item = (grp.items||[]).find(it=>o.name.replace(/\s|세트|코스/g,"").indexOf(it) >= 0 || it.indexOf(o.name.replace(/\s|세트|코스/g,"")) >= 0);
      if(item) courses[grp.id + "|" + item] = (courses[grp.id + "|" + item] || 0) + q; else unmatched.push(`${o.name} ${q}`);
    });
    rows.push({ n: rows.length + 1, text: `${no} · ${g(idx.name)} · ${g(idx.when)} · ${g(idx.ppl)} · ${prod} · ${stRaw}`,
      no, when, name: g(idx.name) || "네이버 손님", phoneTail: (g(idx.phone).match(/(\d{4})\s*$/) || [,""])[1],
      status, isRoomProd, people: pp.people, infants: pp.infants, courses, unmatched, request: g(idx.req), cancelWhy: g(idx.cancelWhy) });
  }
  return { rows, headFound: true };
}
function naverPreview(){
  const ta = document.getElementById("naver-paste"); const text = ta ? ta.value : (view.naver ? view.naver.text : "");
  const p = naverParse(text);
  if(p.err){ view.naver = {text, result:[{n:1, text:"", ok:false, msg:p.err}]}; render(); return; }
  const s = store();
  const result = p.rows.map(r=>{
    if(!r.when) return {n:r.n, text:r.text, ok:false, msg:"이용일시를 못 읽었습니다"};
    if(!r.people) return {n:r.n, text:r.text, ok:false, msg:"인원을 못 읽었습니다"};
    const ex = s.reservations.concat(s.trash||[]).find(x=>x.naverNo === r.no);
    if(!ex) return Object.assign({ok:true, kind:"new", msg:`${r.when.date} ${r.when.time} ${r.people}명 ${r.isRoomProd?"룸":"테이블"}${r.status!=="확정"?" · "+r.status:""}`}, r);
    const diff = [];
    if(ex.date !== r.when.date || ex.time !== r.when.time) diff.push("시각");
    if(pplOf(ex) !== r.people) diff.push("인원");
    if(ex.status !== r.status) diff.push("상태 " + ex.status + "→" + r.status);
    if((ex.request||"") !== (r.request||"") && r.request) diff.push("요청");
    if(!diff.length) return Object.assign({ok:true, kind:"skip", msg:"바뀐 것 없음"}, r);
    return Object.assign({ok:true, kind:"update", msg:diff.join(" · "), exId:ex.id}, r);
  });
  view.naver = {text, result}; render();
}
async function naverApply(){
  const n = view.naver; if(!n || !n.result) return;
  if(readonlyBlock()) return;
  const s = store(); let added = 0, updated = 0;
  n.result.filter(x=>x.ok && x.kind !== "skip").forEach(r=>{
    const memoTail = `네이버 예약번호 ${r.no}${r.phoneTail?` · 전화 ****${r.phoneTail}`:""}${r.unmatched.length?` · 옵션 ${r.unmatched.join(", ")}`:""}${r.cancelWhy?` · 취소사유: ${r.cancelWhy}`:""}`;
    if(r.kind === "new"){
      const rec = { id:newId("res"), naverNo:r.no, date:r.when.date, time:r.when.time, name:r.name, phone:"", people:r.people, infants:r.infants, chairs:0,
        roomId:null, extraIds:[], seatPref: r.isRoomProd ? "room-any" : "table-any", tentativeRoomId:null, tentativeExtra:[], tentativeSplit:false,
        source:"네이버 예약", sourceDetail:"", createdAt:new Date().toISOString(),
        menuType: Object.keys(r.courses).length ? "코스" : (r.isRoomProd ? "확인 필요" : "해당 없음"), courses:r.courses, courseUndecided:false,
        allergy:"", allergyChecked:false, request:r.request||"", memo:memoTail, status:r.status, changes:[], sms:[] };
      createReservation(rec); added++;
    }else{
      const ex = s.reservations.find(x=>x.id===r.exId) || (s.trash||[]).find(x=>x.id===r.exId); if(!ex) return;
      const d = [];
      if(ex.date !== r.when.date || ex.time !== r.when.time){ d.push({n:"시각", a:ex.date+" "+ex.time, b:r.when.date+" "+r.when.time}); ex.date = r.when.date; ex.time = r.when.time; }
      if(pplOf(ex) !== r.people){ d.push({n:"인원", a:pplOf(ex), b:r.people}); ex.people = r.people; ex.infants = r.infants; }
      if(r.request && ex.request !== r.request){ d.push({n:"요청"}); ex.request = r.request; }
      if(ex.status !== r.status){ if(r.status==="취소"||r.status==="노쇼") addChange(ex, r.status, []); else d.push({n:"상태", a:ex.status, b:r.status}); ex.status = r.status; }
      if(d.length) addChange(ex, "변경", d); else touch(ex);
      reflowTentatives(ex.date); updated++;
    }
  });
  logEvent("네이버 가져오기", `새로 ${added} · 고침 ${updated}`);
  view.naver = null; view.form = null; saveData(); render();
  uiAlert("네이버 예약 가져오기 완료", `새로 ${added}건, 고침 ${updated}건. 룸 예약은 '룸 미정' 으로 들어와 잠정 배정이 잡습니다 — 좌석 미정 목록에서 확정하세요.`, "ok");
}
'''

s = R(s, """function openNoshow(){""", JS + "\nfunction openNoshow(){")
s = R(s, """              <button onclick="closeMore(); openHours()">${ICON.clock}<span>영업시간</span></button>""",
         """              <button onclick="closeMore(); openHours()">${ICON.clock}<span>영업시간</span></button>
              <button onclick="closeMore(); openNaver()">${ICON.res}<span>네이버 예약 가져오기</span></button>""")
s = R(s, """tedit:sheetTableEdit, logs:sheetLogs,""", """tedit:sheetTableEdit, naver:sheetNaver, logs:sheetLogs,""")
s = R(s, """#ovr-bulk{width:100%;""", """#naver-paste{width:100%; font:inherit; font-size:var(--fs-sub); padding:var(--s8) var(--s12); border:1px solid var(--border-strong); border-radius:var(--r-sm); resize:vertical; white-space:pre}
#ovr-bulk{width:100%;""")
L.js_check(s)
L.save(s)
print("naver ok")
