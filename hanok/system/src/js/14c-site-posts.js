/* ---------- 홈페이지 관리 → 소식 (site_posts, 14차) ----------
   사장님이 글을 쌓는 게시판. 초안·적용 판(site_draft/site_versions)과는 별개 — **저장하면 바로 홈페이지 소식 장에 나옵니다**.
   글 하나 = 제목·날짜·본문·사진 여러 장·첨부 파일. 사진·파일은 Storage 'site' 버킷(saPickFile). 지우기는 status '삭제' 로 숨김(S4).
   상태는 SA.posts(목록) · SA.post(고치는 중인 글 하나). 14b 의 sheetSite 가 SA.tab === "posts" 면 saTabPosts() 를 부릅니다. */
async function saPostsLoad(){
  SA.postsLoading = true; render();
  try{
    var key = view.storeKey || "hanok";
    SA.posts = await sb("/rest/v1/site_posts?store=eq." + key + "&status=neq.%EC%82%AD%EC%A0%9C&select=id,title,body,date,images,files,pinned,status,updated_at,by&order=pinned.desc,date.desc,created_at.desc&limit=300");
    SA.postsErr = null;
  }catch(e){ SA.posts = SA.posts || []; SA.postsErr = e.message || String(e); }
  SA.postsLoading = false; render();
}
function saPostNew(){
  SA.post = { id:"post_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), title:"", body:"", date:todayStr(), images:[], files:[], pinned:false, status:"게시", _new:true };
  SA.postSaved = JSON.stringify(SA.post); render();
}
function saPostEdit(id){
  var p = (SA.posts || []).find(function(x){ return x.id === id; }); if(!p) return;
  SA.post = deepClone(p); SA.post.images = SA.post.images || []; SA.post.files = SA.post.files || [];
  SA.postSaved = JSON.stringify(SA.post); render();
}
function saPostDirty(){ return !!(SA && SA.post && JSON.stringify(SA.post) !== SA.postSaved); }
async function saPostBack(){
  if(saPostDirty() && !await uiConfirm("고친 내용을 버릴까요?", "저장하지 않은 내용은 사라집니다.", {ok:"버리기", cancel:"계속 쓰기"})) return;
  SA.post = null; render();
}
function saPostSet(k, v){ if(SA.post) SA.post[k] = v; saPostHeader(); }
/* 제목 줄 같은 작은 표시만 갈아 끼움 — 글자마다 render() 하면 입력 초점이 날아감 */
function saPostHeader(){ var el = document.getElementById("sa-post-state"); if(el) el.textContent = saPostDirty() ? "고친 내용이 있습니다" : ""; }
function saPostImgAdd(){ saPickFile("image", function(u){ SA.post.images.push(u); render(); }); }
function saPostImgDel(i){ SA.post.images.splice(i, 1); render(); }
function saPostImgMove(i, d){ var a = SA.post.images, j = i + d; if(j < 0 || j >= a.length) return; var t = a[i]; a[i] = a[j]; a[j] = t; render(); }
function saPostFileAdd(){ saPickFile("file", function(u, name){ SA.post.files.push({name:name || u.split("/").pop(), url:u}); render(); }); }
function saPostFileDel(i){ SA.post.files.splice(i, 1); render(); }
function saPostFileName(i, v){ SA.post.files[i].name = v; saPostHeader(); }
/* 저장 = 바로 게시(또는 초안). 새 글은 POST, 있던 글은 같은 id 로 upsert */
async function saPostSave(status){
  var p = SA.post; if(!p) return;
  if(!(p.title || "").trim()){ await uiAlert("제목을 적어 주세요", "", "warn"); return; }
  if(!/^\d{4}-\d{2}-\d{2}$/.test(p.date || "")){ await uiAlert("날짜를 골라 주세요", "", "warn"); return; }
  var row = { id:p.id, store:view.storeKey || "hanok", title:p.title.trim(), body:(p.body || "").replace(/\r/g, ""), date:p.date,
              images:p.images || [], files:p.files || [], pinned:!!p.pinned, status:status || p.status || "게시", by:(SESSION && SESSION.who) || "" };
  try{
    await sb("/rest/v1/site_posts?on_conflict=id", { method:"POST", body:row, prefer:"resolution=merge-duplicates,return=minimal" });
    logEvent("소식 " + (row.status === "게시" ? "게시" : "초안 저장"), row.title);
    showToast(row.status === "게시" ? "게시했습니다 — 홈페이지 소식에 바로 나옵니다" : "초안으로 저장했습니다");
    SA.post = null; await saPostsLoad();
  }catch(e){ await uiAlert("저장 실패", e.message || String(e), "warn"); }
}
async function saPostDelete(){
  var p = SA.post; if(!p || p._new){ SA.post = null; render(); return; }
  if(!await uiConfirm("이 글을 지울까요?", "홈페이지에서 사라집니다. 지운 글은 되살릴 수 없습니다(사진·파일은 남음).", {ok:"지우기", cancel:"취소"})) return;
  try{
    await sb("/rest/v1/site_posts?id=eq." + encodeURIComponent(p.id), { method:"PATCH", body:{status:"삭제"}, prefer:"return=minimal" });
    logEvent("소식 삭제", p.title);
    SA.post = null; await saPostsLoad();
  }catch(e){ await uiAlert("지우지 못했습니다", e.message || String(e), "warn"); }
}
function saPostWhen(iso){ var d = new Date(iso); return isNaN(d) ? "" : (d.getMonth()+1) + "/" + d.getDate() + " " + String(d.getHours()).padStart(2,"0") + ":" + String(d.getMinutes()).padStart(2,"0"); }

/* ---------- 화면 ---------- */
function saTabPosts(){
  if(!SA.posts && !SA.postsLoading && !SA.postsErr) saPostsLoad();
  if(SA.post) return saPostEditor();
  var list = SA.posts || [];
  var rows = SA.postsLoading && !SA.posts ? '<p class="muted" style="padding:12px 0">불러오는 중…</p>'
    : SA.postsErr ? '<div class="alert rust"><span class="ic">!</span><div><div class="a-t">불러오지 못했습니다</div><div class="a-s">' + esc(SA.postsErr) + '</div></div></div>'
    : !list.length ? '<div class="empty">아직 글이 없습니다. "새 글" 로 첫 소식을 올려 보세요.</div>'
    : list.map(function(p){
        var imgs = (p.images || []).length, files = (p.files || []).length;
        return '<button class="rowitem tap" onclick="saPostEdit(\'' + p.id + '\')">' +
          '<span class="grow"><span class="t">' + esc(p.title) + (p.pinned ? ' <span class="tag pine sm">고정</span>' : '') + (p.status === "초안" ? ' <span class="tag amber sm">초안</span>' : '') + '</span>' +
          '<span class="s">' + esc(dateLabel(p.date)) + (imgs ? ' · 사진 ' + imgs : '') + (files ? ' · 파일 ' + files : '') + (p.updated_at ? ' · 고침 ' + saPostWhen(p.updated_at) : '') + '</span></span></button>';
      }).join("");
  return saBox("소식 글", '<div class="card searchbox" style="margin-bottom:12px">' + rows + '</div>' +
      '<div class="btn-row"><button class="btn sm primary" onclick="saPostNew()">＋ 새 글</button><a class="btn sm" href="' + saRoot() + 'news.html?v=' + Date.now() + '" target="_blank" rel="noopener">홈페이지 소식 보기</a></div>',
      '<span class="muted" style="margin-left:auto; font-size:var(--fs-label)">저장하면 바로 홈페이지에 나옵니다 — 위의 초안·적용과 무관</span>') +
    '<p class="f-note">글은 최신 날짜가 위, "고정" 한 글은 맨 위. 본문은 줄바꿈 그대로, 빈 줄로 문단이 나뉘고 **굵게** 를 쓸 수 있습니다. 사진은 긴 변 1600px 로 줄여서 올라갑니다.</p>';
}
function saPostEditor(){
  var p = SA.post;
  var imgs = (p.images || []).map(function(u, i){
    return '<div class="sa-pimg"><img src="' + esc(u) + '" alt="" onclick="saPostZoom(' + i + ')" title="크게 보기"><div class="sa-pimg-x">' +
      '<button class="btn sm ghost" onclick="saPostImgMove(' + i + ',-1)" ' + (i === 0 ? "disabled" : "") + '>←</button>' +
      '<button class="btn sm ghost" onclick="saPostImgMove(' + i + ',1)" ' + (i === p.images.length - 1 ? "disabled" : "") + '>→</button>' +
      '<button class="btn sm ghost" onclick="saPostImgDel(' + i + ')">×</button></div></div>';
  }).join("");
  var files = (p.files || []).map(function(f, i){
    return '<div class="sa-row"><input type="text" class="in-sm" value="' + esc(f.name || "") + '" placeholder="보이는 이름" oninput="saPostFileName(' + i + ', this.value)">' +
      '<a class="btn sm ghost" href="' + esc(f.url) + '" target="_blank" rel="noopener">열기</a><button class="btn sm ghost" onclick="saPostFileDel(' + i + ')">×</button></div>';
  }).join("");
  return saBox(p._new ? "새 글" : "글 고치기",
      '<label class="f sa-f"><div class="lb">제목</div><input type="text" class="in-sm" value="' + esc(p.title) + '" placeholder="예: 추석 연휴 정상 영업" oninput="saPostSet(\'title\', this.value)"></label>' +
      '<div class="grid2">' +
        '<label class="f sa-f"><div class="lb">날짜 <span class="lbl-note">글에 보이는 날짜 · 정렬 기준</span></div><input type="date" class="in-sm" value="' + esc(p.date) + '" onchange="saPostSet(\'date\', this.value)"></label>' +
        '<div class="f">' + saSwHtml(!!p.pinned, "saPostSet('pinned', " + (p.pinned ? "false" : "true") + "); render()", "맨 위 고정", "소식 목록 맨 위에 둡니다") + '</div>' +
      '</div>' +
      '<label class="f sa-f"><div class="lb">본문 <span class="lbl-note">빈 줄로 문단 · **굵게**</span></div><textarea class="in-sm" rows="10" placeholder="내용을 적어 주세요" oninput="saPostSet(\'body\', this.value)">' + esc(p.body || "") + '</textarea></label>' +
      '<div class="f"><div class="lb">사진 <span class="lbl-note">여러 장 · 순서는 화살표</span></div><div class="sa-pimgs">' + imgs + '<button class="sa-pimg add" onclick="saPostImgAdd()">＋ 사진 올리기</button></div></div>' +
      '<div class="f"><div class="lb">첨부 파일 <span class="lbl-note">PDF·한글·워드·엑셀·zip 등, 50MB 까지</span></div>' + files + '<div class="btn-row"><button class="btn sm" onclick="saPostFileAdd()">＋ 파일 올리기</button></div></div>' +
      '<div class="btn-row" style="margin-top:16px; align-items:center">' +
        '<button class="btn sm ghost" onclick="saPostBack()">← 목록</button>' +
        (p._new ? '' : '<button class="btn sm ghost danger" onclick="saPostDelete()">지우기</button>') +
        '<button class="btn sm" onclick="SA.postPreview=true; render()">미리보기</button>' +
        '<span id="sa-post-state" class="muted" style="margin-left:auto; font-size:var(--fs-label)">' + (saPostDirty() ? "고친 내용이 있습니다" : "") + '</span>' +
        '<button class="btn sm" onclick="saPostSave(\'초안\')">초안으로 저장</button>' +
        '<button class="btn sm primary" onclick="saPostSave(\'게시\')">' + (p.status === "게시" && !p._new ? "고친 것 게시" : "게시") + '</button>' +
      '</div>',
      p.status === "초안" ? '<span class="tag amber sm" style="margin-left:auto">초안 — 홈페이지에 안 보임</span>' : '') +
    (SA.postPreview ? saPostPreviewHtml() : '') + (SA.postZoom != null ? saPostZoomHtml() : '');
}
/* 사진 크게 보기(관리 화면) */
function saPostZoom(i){ SA.postZoom = i; render(); }
function saPostZoomHtml(){
  var imgs = SA.post.images || [], i = SA.postZoom, u = imgs[i]; if(!u){ SA.postZoom = null; return ""; }
  return '<div class="overlay sa-zoom" onclick="SA.postZoom=null; render()"><img src="' + esc(u) + '" alt="" onclick="event.stopPropagation()">' +
    (imgs.length > 1 ? '<button class="sa-zoom-nav prev" onclick="event.stopPropagation(); SA.postZoom=(' + i + '+' + imgs.length + '-1)%' + imgs.length + '; render()">‹</button><button class="sa-zoom-nav next" onclick="event.stopPropagation(); SA.postZoom=(' + i + '+1)%' + imgs.length + '; render()">›</button>' : '') +
    '<span class="sa-zoom-n">' + (i + 1) + ' / ' + imgs.length + '</span></div>';
}
/* 미리보기 — 홈페이지 소식 장에 나오는 모양 그대로(js/news.js 와 같은 규칙: 빈 줄 문단, **굵게**) */
function saPostPreviewHtml(){
  var p = SA.post, rich = function(s){ return esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>"); };
  var paras = String(p.body || "").split(/\n{2,}/).map(function(x){ return x.trim(); }).filter(Boolean);
  var WD = ["일","월","화","수","목","금","토"], dt = new Date(p.date + "T00:00:00");
  var date = isNaN(dt) ? p.date : dt.getFullYear() + ". " + (dt.getMonth() + 1) + ". " + dt.getDate() + " (" + WD[dt.getDay()] + ")";
  var imgs = (p.images || []).filter(Boolean), files = (p.files || []).filter(function(f){ return f && f.url; });
  return '<div class="overlay" onclick="SA.postPreview=null; render()"><div class="sheet sheet-tall sa-pv-post" onclick="event.stopPropagation()">' + sheetHead("미리보기 — 홈페이지 소식") +
    '<div class="np"><div class="np-meta">' + (p.pinned ? '<em>고정</em>' : '') + '<time>' + esc(date) + '</time></div><h2>' + esc(p.title || "(제목 없음)") + '</h2>' +
    '<div class="np-text">' + paras.map(function(x){ return '<p>' + rich(x).replace(/\n/g, "<br>") + '</p>'; }).join("") + '</div>' +
    (imgs.length ? '<div class="np-imgs ' + (imgs.length === 1 ? "one" : "") + '">' + imgs.map(function(u, i){ return '<img src="' + esc(u) + '" alt="" onclick="saPostZoom(' + i + ')">'; }).join("") + '</div>' : '') +
    (files.length ? '<ul class="np-files">' + files.map(function(f){ return '<li><a href="' + esc(f.url) + '" target="_blank" rel="noopener">↓ ' + esc(f.name || f.url.split("/").pop()) + '</a></li>'; }).join("") + '</ul>' : '') + '</div>' +
    '<div class="sheet-actions"><button class="btn primary" onclick="SA.postPreview=null; render()">닫기</button></div></div></div>';
}
