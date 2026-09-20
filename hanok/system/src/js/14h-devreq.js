/* ---------- 개발자에게 (19차, 재아 09-20) ----------
   사장님·직원이 개선 요청이나 급한 조치를 글로 남기는 곳. 매번 전화·카톡으로 연락하는 게 서로 불편해서.
   · 급함 / 보통 — 급함만 재아에게 알림(서버 웹훅, patch_19차 주석). 보통은 재아가 모아서 봄.
   · 재아가 답변(reply)·상태(접수 → 확인 → 처리 중 → 끝)를 적음. 화면에서는 '끝' 표시만 할 수 있음(해결된 걸 치우려고).
   · 화면 사진을 붙일 수 있음(홈페이지 관리의 saPickFile 재사용 — Storage site 버킷).
   더보기(⋮)에서 바로 열림(관리자 비밀번호 없음 — 직원도 씀). 화면형(view.form={type:"devreq", page:true}). */
var DQ = null;

async function openDevPage(){
  if(!supaOn()){ await uiAlert("서버 설정이 없는 빌드입니다", "개발자에게는 서버가 있어야 합니다.", "warn"); return; }
  view.form = {type:"devreq", page:true};
  if(!DQ) DQ = { list:[], loading:true, err:null, open:null, draft:null };
  DQ.loading = true; render();
  await dqLoad(); render();
}
async function dqLoad(){
  try{
    DQ.list = await sb("/rest/v1/dev_requests?store=eq." + (view.storeKey || "hanok") + "&select=*&order=created_at.desc&limit=200");
    DQ.err = null;
  }catch(e){ DQ.err = e.message || String(e); DQ.list = DQ.list || []; }
  DQ.loading = false;
}
function dqWhen(iso){ var d = new Date(iso); return (d.getMonth()+1) + "/" + d.getDate() + " " + pad(d.getHours()) + ":" + pad(d.getMinutes()); }
function dqStatusTag(s){ var c = s === "끝" ? "" : s === "처리 중" ? "blue" : s === "확인" ? "pine" : "amber"; return '<span class="tag sm ' + c + '">' + esc(s) + '</span>'; }

function sheetDevReq(){
  if(!DQ || DQ.loading) return '<p class="muted" style="padding:20px 0">불러오는 중…</p>';
  var open = DQ.list.filter(function(r){ return r.status !== "끝"; }), done = DQ.list.filter(function(r){ return r.status === "끝"; });
  var row = function(r){
    return '<button class="rowitem tap dq-row' + (r.urgent ? ' urgent' : '') + '" onclick="DQ.open=\'' + esc(r.id) + '\'; render()">' +
      '<span class="time-col">' + esc(dqWhen(r.created_at)) + '</span>' +
      '<span class="grow"><span class="t">' + (r.urgent ? '<span class="tag rust sm">급함</span> ' : '') + esc(r.title) + '</span>' +
      '<span class="s">' + (r.reply ? '답변: ' + esc(r.reply).slice(0, 80) : esc(r.body || "").split("\n")[0].slice(0, 80)) + '</span></span>' +
      dqStatusTag(r.status) + '</button>';
  };
  return '<div class="dq-top"><button class="btn primary" onclick="dqNew()">글 쓰기</button>' +
    '<p class="f-note" style="margin:0">고쳤으면 하는 것, 이상한 것, 급하게 바꿔야 하는 것을 여기 적어 주세요. <b>급함</b>이면 재아에게 바로 알림이 가고, <b>보통</b>은 모아서 봅니다. 정말 급하면 전화.</p></div>' +
    (DQ.err ? '<p class="f-note rust">불러오지 못했습니다: ' + esc(DQ.err) + ' (서버에 patch_19차가 아직 없을 수 있습니다)</p>' : '') +
    '<div class="subhead">진행 중 ' + open.length + '건</div>' +
    '<div class="card searchbox">' + (open.length ? open.map(row).join("") : '<p class="muted" style="padding:16px">남긴 글이 없습니다.</p>') + '</div>' +
    (done.length ? '<div class="subhead">끝난 것 ' + done.length + '건</div><div class="card searchbox dq-done">' + done.slice(0, 30).map(row).join("") + '</div>' : '') +
    (DQ.draft ? dqFormHtml() : DQ.open ? dqDetailHtml() : "");
}
function dqNew(){ DQ.draft = { title:"", body:"", urgent:false, images:[] }; render(); setTimeout(function(){ var el = document.getElementById("dq-title"); if(el) el.focus(); }, 50); }
function dqSet(k, v){ if(DQ.draft) DQ.draft[k] = v; }
function dqFormHtml(){
  var d = DQ.draft;
  return '<div class="overlay" onclick="DQ.draft=null; render()"><div class="sheet" onclick="event.stopPropagation()">' +
    sheetHead("개발자에게 글 쓰기") +
    '<div class="f"><div class="lb">얼마나 급한가요</div><div class="seg">' +
      '<button class="' + (!d.urgent ? "on" : "") + '" onclick="dqSet(\'urgent\', false); render()">보통</button>' +
      '<button class="' + (d.urgent ? "on rust" : "") + '" onclick="dqSet(\'urgent\', true); render()">급함</button></div>' +
      '<div class="f-note">' + (d.urgent ? '지금 영업에 지장이 있는 것 — 재아에게 바로 알림이 갑니다.' : '개선 요청·건의 — 재아가 모아서 봅니다.') + '</div></div>' +
    '<label class="f"><div class="lb">제목</div><input id="dq-title" type="text" value="' + esc(d.title) + '" placeholder="예: 예약 목록에서 전화번호가 안 보여요" oninput="dqSet(\'title\', this.value)"></label>' +
    '<label class="f big"><div class="lb">내용 <span class="lbl-note">언제, 어느 화면에서, 무엇이</span></div><textarea rows="6" placeholder="예: 오늘 12시쯤 태블릿에서 예약 등록 마지막 단계에서 버튼이 안 눌렸어요" oninput="dqSet(\'body\', this.value)">' + esc(d.body) + '</textarea></label>' +
    '<div class="f"><div class="lb">화면 사진 <span class="lbl-note">선택</span></div><div class="dq-imgs">' +
      d.images.map(function(u, i){ return '<span class="dq-img"><img src="' + esc(u) + '" alt=""><button class="x" onclick="DQ.draft.images.splice(' + i + ',1); render()" aria-label="빼기">×</button></span>'; }).join("") +
      '<button class="btn sm" onclick="saPickFile(\'image\', function(u){ DQ.draft.images.push(u); render(); })">사진 올리기</button></div></div>' +
    '<div class="sheet-actions"><button class="btn" onclick="DQ.draft=null; render()">취소</button><button class="btn primary" onclick="dqSend()">보내기</button></div></div></div>';
}
async function dqSend(){
  var d = DQ.draft; if(!d) return;
  if(!d.title.trim()){ await uiAlert("제목을 적어 주세요", "", "warn"); return; }
  try{
    var row = { id:newId("dq"), store:view.storeKey || "hanok", title:d.title.trim(), body:d.body.trim(), urgent:!!d.urgent, images:d.images, by:(SESSION && SESSION.who) || "" };
    await sb("/rest/v1/dev_requests", { method:"POST", body:row, prefer:"return=minimal" });
    logEvent("개발자에게", (d.urgent ? "급함 " : "") + row.title);
    DQ.draft = null; showToast(d.urgent ? "보냈습니다 · 재아에게 알림이 갑니다" : "보냈습니다");
    await dqLoad(); render();
  }catch(e){ await uiAlert("보내지 못했습니다", e.message || String(e), "warn"); }
}
function dqDetailHtml(){
  var r = DQ.list.filter(function(x){ return x.id === DQ.open; })[0]; if(!r) return "";
  var imgs = Array.isArray(r.images) ? r.images : [];
  return '<div class="overlay" onclick="DQ.open=null; render()"><div class="sheet" onclick="event.stopPropagation()">' +
    sheetHead((r.urgent ? '<span class="tag rust sm">급함</span> ' : '') + esc(r.title) + ' ' + dqStatusTag(r.status)) +
    '<p class="f-note" style="margin-top:-6px">' + esc(dqWhen(r.created_at)) + (r.by ? ' · ' + esc(r.by === "admin" ? "사장님" : "직원") : '') + '</p>' +
    (r.body ? '<div class="dq-body">' + esc(r.body).replace(/\n/g, "<br>") + '</div>' : '') +
    (imgs.length ? '<div class="dq-imgs">' + imgs.map(function(u){ return '<a class="dq-img" href="' + esc(u) + '" target="_blank" rel="noopener"><img src="' + esc(u) + '" alt=""></a>'; }).join("") + '</div>' : '') +
    '<div class="subhead">재아 답변</div>' +
    (r.reply ? '<div class="dq-reply">' + esc(r.reply).replace(/\n/g, "<br>") + (r.replied_at ? '<small>' + esc(dqWhen(r.replied_at)) + '</small>' : '') + '</div>' : '<p class="muted">아직 답변이 없습니다.</p>') +
    '<div class="sheet-actions">' + (r.status !== "끝" ? '<button class="btn" onclick="dqDone(\'' + esc(r.id) + '\')">해결됨 · 끝으로</button>' : '') + '<button class="btn primary" onclick="DQ.open=null; render()">닫기</button></div></div></div>';
}
async function dqDone(id){
  try{ await sb("/rest/v1/dev_requests?id=eq." + id, { method:"PATCH", body:{ status:"끝" }, prefer:"return=minimal" }); DQ.open = null; await dqLoad(); render(); }
  catch(e){ await uiAlert("바꾸지 못했습니다", e.message || String(e), "warn"); }
}
