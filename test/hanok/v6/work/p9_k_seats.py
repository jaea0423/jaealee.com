# -*- coding: utf-8 -*-
"""8차-K: 설정 좌석 폴드를 룸 / 테이블 / 합침 세 탭으로. 룸 합침에 '공간 나뉨(손님 확인)' 체크, 테이블 붙임 짝 편집기"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patchlib as L
s = L.load()
R = L.rep

s = R(s, """  const joinRowHtml = j => `
      <div class="rowitem seat">
        <span class="grow"><span class="t">${esc(jLabel(j))}</span>
          <span class="s">${j.min}~${j.max}명${j.note?` · ${esc(j.note)}`:""}</span></span>""",
"""  const joinRowHtml = j => `
      <div class="rowitem seat">
        <span class="grow"><span class="t">${esc(jLabel(j))}</span>
          <span class="s">${j.min}~${j.max}명${j.note?` · ${esc(j.note)}`:""}</span>
          <label class="chk" style="margin:4px 0 0"><input type="checkbox" ${j.split?"checked":""} onchange="setJoinFlag('${j.id}','split',this.checked)"><span>공간이 나뉨(원탁 등) — 배정할 때 손님 확인 창</span></label></span>""")

# 세 탭 구조로 재구성
a = s.index("  const seatBody = `\n    <p class=\"f-note\" style=\"margin:0 0 12px\">")
b = s.index("  /* ---------- 코스 ---------- */")
seat_old = s[a:b]
# 룸 부분·테이블 부분·합침 부분을 잘라 씁니다
i_room = seat_old.index('    <div class="subhead">룸 ')
i_tbl = seat_old.index('    <div class="subhead" style="margin-top:20px">테이블 ')
i_join = seat_old.index('    <div class="subhead" style="margin-top:20px">룸 합침 ')
intro = seat_old[len("  const seatBody = `\n"):i_room]
room_part = seat_old[i_room:i_tbl].replace('<div class="subhead">룸 ', '<div class="subhead">룸 ')
tbl_part = seat_old[i_tbl:i_join].replace('<div class="subhead" style="margin-top:20px">테이블 ', '<div class="subhead">테이블 ')
join_part = seat_old[i_join:].rstrip()
assert join_part.endswith("</div>`;"), join_part[-40:]
join_part = join_part[:-len("`;")].replace('<div class="subhead" style="margin-top:20px">룸 합침 ', '<div class="subhead">룸 합침 ')

new_seat = """  /* 8차-K: 세 탭(룸 / 테이블 / 합침) — 한 폴드에 다 펼치면 너무 길었습니다 */
  const seatTab = view.seatTab || "room";
  const tabBtn = (k, label) => `<button class="${seatTab===k?'on':''}" onclick="view.seatTab='${k}'; render()">${label}</button>`;
  /* 테이블 붙임 짝 — 같은 층 안에서 서로 붙일 수 있는 테이블을 표로. 칸을 누르면 양쪽 다 바뀝니다 */
  const pairTable = fl => { const list = tables.filter(t=>(t.floor||"")===fl); if(list.length < 2) return "";
    return `<div class="lbl" style="margin:10px 0 4px">${esc(fl||"층 없음")} — 서로 붙일 수 있는 테이블</div>
    <div class="pairwrap"><table class="pairs"><tr><th></th>${list.map(t=>`<th>${esc(t.name)}</th>`).join("")}</tr>
      ${list.map(a=>`<tr><th>${esc(a.name)}</th>${list.map(b=>a.id===b.id?`<td class="self"></td>`:`<td><button class="pair ${(a.joinWith||[]).indexOf(b.id)>=0?'on':''}" onclick="toggleJoinWith('${a.id}','${b.id}')" title="${esc(a.name)} + ${esc(b.name)}">${(a.joinWith||[]).indexOf(b.id)>=0?"●":""}</button></td>`).join("")}</tr>`).join("")}
    </table></div>`; };
  const seatBody = `
""" + intro + """    <div class="seg seattabs">${tabBtn("room","룸")}${tabBtn("table","테이블")}${tabBtn("join","합침")}</div>
    ${seatTab==="room" ? `
""" + room_part + """` : ""}
    ${seatTab==="table" ? `
""" + tbl_part + """` : ""}
    ${seatTab==="join" ? `
""" + join_part + """
    <div class="subhead" style="margin-top:20px">테이블 붙임 <span>같은 층에서 붙여 앉힐 수 있는 짝. 큰 팀이 오면 이 짝으로만 붙입니다(아니면 나눠 앉음)</span></div>
    ${floorsT.map(pairTable).join("")}` : ""}`;

"""
s = s[:a] + new_seat + s[b:]

# 합침 플래그 + 경고 판정을 note 정규식 대신 플래그로(옛 메모 '원탁' 도 인정)
s = R(s, """async function delJoin(id){""", """function setJoinFlag(id, k, v){ const st = draft(); st.joins = (st.joins||[]).map(j=>j.id===id?Object.assign({}, j, {[k]:v}):j); render(); }
async function delJoin(id){""")
s = R(s, """    if(ids.length > 1 && joinOf(ids) && /원탁/.test(joinOf(ids).note||"")) out.push("원탁 합침 · 손님 확인");""",
         """    if(ids.length > 1 && joinOf(ids) && (joinOf(ids).split || /원탁/.test(joinOf(ids).note||""))) out.push("원탁 합침 · 손님 확인");""")
# 마법사·배정 확인창도 플래그 기준
s = R(s, """    if(j && j.note && !await uiConfirm(`${label} — ${j.note}`, "손님께 확인하셨나요?", {ok:"확인했음", cancel:"다시 고르기"})) return;""",
         """    if(j && (j.split || j.note) && !await uiConfirm(`${label} — ${j.note || "공간이 나뉩니다"}`, j.split ? "테이블이 나뉘어 앉게 됩니다. 손님께 확인하셨나요?" : "손님께 확인하셨나요?", {ok:"확인했음", cancel:"다시 고르기"})) return;""")
s = R(s, """  if(j && j.note && !await uiConfirm(`${label} — ${j.note}`, "손님께 확인하셨나요?", {ok:"확인했음 · 배정", cancel:"다시 고르기"})) return;""",
         """  if(j && (j.split || j.note) && !await uiConfirm(`${label} — ${j.note || "공간이 나뉩니다"}`, j.split ? "테이블이 나뉘어 앉게 됩니다. 손님께 확인하셨나요?" : "손님께 확인하셨나요?", {ok:"확인했음 · 배정", cancel:"다시 고르기"})) return;""")
# 기본 데이터: 원탁 합침에 split:true
s = R(s, """        {id:"j2",ids:["r5","r6"],     min:12,max:14,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"},""",
         """        {id:"j2",ids:["r5","r6"],     min:12,max:14,split:true,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"},""")
s = R(s, """        {id:"j3",ids:["r6","r7"],     min:12,max:14,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"},""",
         """        {id:"j3",ids:["r6","r7"],     min:12,max:14,split:true,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"},""")
s = R(s, """        {id:"j4",ids:["r5","r6","r7"],min:18,max:21,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"}""",
         """        {id:"j4",ids:["r5","r6","r7"],min:18,max:21,split:true,note:"중문 탈거 · 원탁이라 테이블은 나뉨 — 손님 확인"}""")
# 옛 저장본: note 에 원탁이 있으면 split 채움
s = R(s, """    if(!st.joins) st.joins = deepClone(def.joins || []);""", """    if(!st.joins) st.joins = deepClone(def.joins || []);
    st.joins.forEach(function(j){ if(j.split == null && /원탁|나뉨/.test(j.note || "")) j.split = true; });""")

s = R(s, """.offline-card{padding:var(--s24); text-align:center}""", """/* 좌석 폴드 탭·테이블 붙임 표 */
.seg.seattabs{margin:0 0 var(--s12)}
.pairwrap{overflow-x:auto}
.pairs{border-collapse:collapse; font-size:var(--fs-sub)}
.pairs th{font-weight:600; color:var(--text-2); padding:var(--s4) var(--s8); text-align:center; white-space:nowrap}
.pairs td{text-align:center; padding:2px}
.pairs td.self{background:var(--surface-2)}
.pairs .pair{width:36px; height:36px; border:1px solid var(--border-strong); background:var(--surface); border-radius:var(--r-sm); font-size:12px; color:var(--pine); cursor:pointer}
.pairs .pair.on{background:var(--pine); color:#fff; border-color:var(--pine)}
.offline-card{padding:var(--s24); text-align:center}""")
L.js_check(s)
L.save(s)
print("seats ok")
