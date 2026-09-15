# -*- coding: utf-8 -*-
"""8차-N: 네이버 가져오기 보완(따옴표 안 줄바꿈 셀, 요청사항 표시, 열 때 초기화, 마법사 '네이버 예약 → 직접/Excel'),
   마법사 경로가 설정(sources)을 안 쓰던 누락(방문 빠짐) 수정, 일괄 등록도 열 때 초기화"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

# ---------- A. 엑셀 붙여넣기 파서: 따옴표로 감싼 셀 안의 줄바꿈·탭·"" 처리 ----------
s = R(s, """function naverParse(text){
  const lines = text.split(/\\r?\\n/).map(l=>l.replace(/\\r/g,"")).filter(l=>l.trim());
  const hi = lines.findIndex(l=>/예약번호/.test(l) && /\\t/.test(l));
  if(hi < 0) return {err:"머리글 줄(예약번호 … 이용일시 … 인원)을 못 찾았습니다. 엑셀에서 표 전체를 복사해 붙여 넣으세요."};
  const head = lines[hi].split("\\t").map(x=>x.trim());""",
"""/* 엑셀에서 복사한 표는 탭으로 나뉘고, 셀 안에 줄바꿈이 있으면 그 셀을 큰따옴표로 감쌉니다(안의 " 는 "").
   줄 단위로 자르면 요청사항에 엔터가 든 손님이 통째로 사라졌습니다 — 글자 단위로 따옴표 상태를 보며 자릅니다 */
function tsvRows(text){
  const rows = []; let row = [], cell = "", q = false;
  for(let i = 0; i < text.length; i++){
    const c = text[i];
    if(q){
      if(c === '"'){ if(text[i+1] === '"'){ cell += '"'; i++; } else q = false; }
      else cell += c;
    }else{
      if(c === '"' && cell === "") q = true;
      else if(c === "\\t"){ row.push(cell); cell = ""; }
      else if(c === "\\n" || c === "\\r"){ if(c === "\\r" && text[i+1] === "\\n") i++; row.push(cell); rows.push(row); row = []; cell = ""; }
      else cell += c;
    }
  }
  if(cell !== "" || row.length) { row.push(cell); rows.push(row); }
  return rows.filter(r=>r.some(x=>x.trim()));
}
function naverParse(text){
  const table = tsvRows(text);
  const hi = table.findIndex(r=>r.some(x=>x.trim()==="예약번호") && r.length > 3);
  if(hi < 0) return {err:"머리글 줄(예약번호 … 이용일시 … 인원)을 못 찾았습니다. 엑셀에서 표 전체를 복사해 붙여 넣으세요."};
  const head = table[hi].map(x=>x.trim());""")
s = R(s, """  for(let k = hi + 1; k < lines.length; k++){
    const c = lines[k].split("\\t"); if(c.length < head.length - 5) continue;""",
"""  for(let k = hi + 1; k < table.length; k++){
    const c = table[k]; if(c.length < head.length - 5) continue;""")
# 요청사항 있는 줄은 미리보기에 표시
s = R(s, """    if(!ex) return Object.assign({ok:true, kind:"new", msg:`${r.when.date} ${r.when.time} ${r.people}명 ${r.isRoomProd?"룸":"테이블"}${r.status!=="확정"?" · "+r.status:""}`}, r);""",
"""    if(!ex) return Object.assign({ok:true, kind:"new", msg:`${r.when.date} ${r.when.time} ${r.people}명 ${r.isRoomProd?"룸":"테이블"}${r.status!=="확정"?" · "+r.status:""}${r.request?" · ⚠ 요청사항 있음 — 확인":""}`}, r);""")
# 열 때 초기화(쓰다 만 내용이 남지 않게)
s = R(s, """function openNaver(){ view.form = {type:"naver"}; view.naver = view.naver || {text:"", result:null}; render(); }""",
         """function openNaver(){ view.form = {type:"naver"}; view.naver = {text:"", result:null}; render(); }   /* 열 때마다 비움(재아) */""")
s = R(s, """function openOverride(){ view.form={type:"ovr"}; render(); }""", """function openOverride(){ view.form={type:"ovr"}; view.ovrBulk = null; render(); }""")
# 더보기에서 빼고 마법사 경로 단계로
s = R(s, """
              <button onclick="closeMore(); openNaver()">${ICON.res}<span>네이버 예약 가져오기</span></button>""", "")

# ---------- B. 마법사 경로: 설정의 sources 사용(방문 누락), 네이버 → 직접 / Excel ----------
s = R(s, """function wzStepSource(){
  const opts = [
    ["전화 예약","전화 예약",""],
    ["네이버 예약","네이버 예약",""],
    ["기타","기타",""]
  ];
  return `
    <div class="srcgrid">
      ${opts.map(([v,label,desc])=>`
        <button class="srccell ${WZ.source===v?'on':''}" onclick="wzSource('${jsq(v)}')">
          <span class="s-l">${label}</span>
          ${desc?`<span class="s-d">${desc}</span>`:""}
        </button>`).join("")}
    </div>""",
"""function wzStepSource(){
  /* 경로는 설정(sources)에서 — 예전엔 셋만 박혀 있어 '방문' 이 빠져 있었습니다(누락 수정). '기타' 는 항상 마지막 */
  const srcs = (store().settings.sources || ["전화 예약","네이버 예약","방문","기타"]).slice();
  if(srcs.indexOf("기타") < 0) srcs.push("기타");
  const isNaver = /네이버/.test(WZ.source || "");
  return `
    <div class="srcgrid">
      ${srcs.map(v=>`
        <button class="srccell ${WZ.source===v?'on':''}" onclick="wzSource('${jsq(v)}')">
          <span class="s-l">${esc(v)}</span>
        </button>`).join("")}
    </div>
    ${isNaver ? `<div class="lbl" style="margin-top:14px">네이버 예약은 어떻게 넣을까요?</div>
    <div class="sgrid any">
      <button class="scell" onclick="wzAutoNext()"><span class="sn">직접 등록</span><span class="sc">전화 받듯 한 건씩 입력</span></button>
      <button class="scell" onclick="WZ=null; openNaver()"><span class="sn">Excel 등록</span><span class="sc">파트너센터 엑셀을 복사해 붙여 넣기 — 여러 건 한 번에, 고침도 됨</span></button>
    </div>` : ""}""")
s = R(s, """  WZ.source = v;
  /* 전화·네이버는 더 물을 것이 없으니 '다음'을 누르게 하지 않고 바로 넘어갑니다 (이전으로 돌아올 수 있습니다).
     기타는 경로를 적어야 하므로 이 화면에 머뭅니다 */
  if(v !== "기타"){ wzAutoNext(); return; }
  render();""",
"""  WZ.source = v;
  /* 전화·방문은 더 물을 것이 없으니 바로 넘어갑니다. 기타는 경로를 적어야 하고, 네이버는 직접/Excel 을 고르므로 이 화면에 머뭅니다 */
  if(v !== "기타" && !/네이버/.test(v)){ wzAutoNext(); return; }
  render();""")
L.js_check(s)
L.save(s)
print("fix ok")
