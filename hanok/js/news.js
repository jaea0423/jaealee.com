/* 소식 장 — 서버 site_posts 표에서 '게시' 글을 읽어 최신순으로 늘어놓습니다(고정 글이 맨 위).
   글은 예약 시스템 → 설정 → 홈페이지 관리 → 소식 에서 쓰고, 저장하면 바로 여기 나옵니다(초안·적용 단계 없음).
   목록은 제목·날짜·첫 줄만 보이고, 누르면 그 자리에서 펼쳐집니다. #post_… 주소로 들어오면 그 글을 펼친 채로.
   서버가 없거나(js/config.js 없음) 실패하면 "아직 소식이 없습니다" 만 — 손님에게 오류 문장을 보이지 않습니다. */
(function(){
  const box = document.getElementById("news"); if(!box) return;
  const esc = s => String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  const rich = s => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
  const WD = ["일","월","화","수","목","금","토"];
  const dateText = d => { const t = new Date(d + "T00:00:00"); return isNaN(t) ? d : `${t.getFullYear()}. ${t.getMonth()+1}. ${t.getDate()} (${WD[t.getDay()]})`; };
  const empty = () => { box.innerHTML = `<p class="news-empty">아직 올린 소식이 없습니다.</p>`; };
  const C = window.SUPA;
  if(!C || !C.url || !C.anonKey){ empty(); return; }
  const H = { "apikey": C.anonKey, "Authorization": "Bearer " + C.anonKey };
  fetch(`${C.url}/rest/v1/site_posts?store=eq.${C.store}&status=eq.%EA%B2%8C%EC%8B%9C&select=id,title,body,date,images,files,pinned&order=pinned.desc,date.desc,created_at.desc&limit=200`, {headers:H})
    .then(r => r.ok ? r.json() : [])
    .then(rows => {
      if(!rows.length){ empty(); return; }
      const want = (location.hash || "").slice(1);
      box.innerHTML = rows.map(p => {
        const paras = String(p.body || "").split(/\n{2,}/).map(x => x.trim()).filter(Boolean);
        const first = (paras[0] || "").split("\n")[0];
        const imgs = Array.isArray(p.images) ? p.images.filter(Boolean) : [];
        const files = Array.isArray(p.files) ? p.files.filter(f => f && f.url) : [];
        return `<article class="post${p.id === want ? " open" : ""}" id="${esc(p.id)}">
          <button type="button" class="post-h" aria-expanded="${p.id === want}">
            <span class="post-meta">${p.pinned ? `<em>공지</em>` : ""}<time datetime="${esc(p.date)}">${esc(dateText(p.date))}</time></span>
            <h2>${esc(p.title)}</h2>
            ${first ? `<p class="post-first">${rich(first)}</p>` : ""}
            <i class="post-arrow"></i>
          </button>
          <div class="post-b">
            <div class="post-text">${paras.map(x => `<p>${rich(x).replace(/\n/g, "<br>")}</p>`).join("")}</div>
            ${imgs.length ? `<div class="post-imgs ${imgs.length === 1 ? "one" : ""}">${imgs.map(u => `<a href="${esc(u)}" target="_blank" rel="noopener"><img src="${esc(u)}" alt="" loading="lazy" onerror="this.parentNode.parentNode.removeChild(this.parentNode)"></a>`).join("")}</div>` : ""}
            ${files.length ? `<ul class="post-files">${files.map(f => `<li><a href="${esc(f.url)}" target="_blank" rel="noopener" download>${esc(f.name || f.url.split("/").pop())}</a></li>`).join("")}</ul>` : ""}
          </div>
        </article>`;
      }).join("");
      box.querySelectorAll(".post-h").forEach(h => h.addEventListener("click", () => {
        const a = h.closest(".post"), open = !a.classList.contains("open");
        a.classList.toggle("open", open); h.setAttribute("aria-expanded", open);
        if(open) history.replaceState(null, "", "#" + a.id);
      }));
      const cur = want && document.getElementById(want);
      if(cur) setTimeout(() => cur.scrollIntoView({block:"start", behavior:"smooth"}), 50);
    })
    .catch(empty);
})();
