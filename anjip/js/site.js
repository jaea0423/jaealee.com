/* 안집 사이트 — 네 장(홈·이야기·차림·오시는 길)이 같이 쓰는 스크립트. 한옥반점 js/site.js 를 안집에 맞게 줄인 것.
   상단·폰 하단 바·바닥을 넣고, <body data-page="..."> 값으로 그 장의 내용을 그립니다.
   예약 창은 없습니다(재아 09-20: 안집 온라인 예약은 한옥반점을 끝낸 뒤) — '예약' 단추는 전부 전화(tel:)로.
   내용은 window.SITE(data/site.js 기본값 + 서버 값, js/content.js)에서 읽습니다. HTML 의 글은 JS 가 꺼져 있을 때의 대비용. */
window.SITE_READY.then(function(){
  const $ = s => document.querySelector(s);
  const esc = s => String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  const rich = s => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/\n/g, "<br>");
  const imgUrl = x => !x ? "" : /^(https?:)?\/\//.test(x) || /^data:/.test(x) ? x : "img/" + x;
  const won = n => n == null ? "" : Number(n).toLocaleString("ko-KR");
  const get = path => path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), SITE);
  const S = SITE;
  const page = document.body.dataset.page || "home";
  const telHref = "tel:" + String(INFO.tel).replace(/[^\d+]/g, "");

  /* ---------- 상단 ---------- */
  const L = [["about.html","about","이야기"],["menu.html","menu","차림"],["visit.html","visit","오시는 길"]];
  const header = document.createElement("header");
  header.className = "nav";
  header.innerHTML = `<div class="wrap">
      <a class="brand" href="index.html"><span class="brand-ko">안집</span><span class="brand-en">${esc(INFO.tagline || "BUNDANG")}</span></a>
      <nav class="links">${L.map(([h,k,l])=>`<a href="${h}" class="${page===k?'cur':''}">${l}</a>`).join("")}</nav>
      <div class="nav-r"><a class="btn fill cta" href="${telHref}">전화 예약</a><button class="burger" aria-label="메뉴 열기"><i></i><i></i></button></div>
    </div>`;
  document.body.prepend(header);
  if(page === "home"){
    const onScroll = () => header.classList.toggle("solid", window.scrollY > 40);
    window.addEventListener("scroll", onScroll, {passive:true}); onScroll();
  }
  const mnav = document.createElement("nav"); mnav.className = "mnav";
  mnav.innerHTML = `<a href="index.html">홈</a>` + L.map(([h,k,l])=>`<a href="${h}">${l}</a>`).join("") + `<a href="${telHref}">전화 ${esc(INFO.tel)}</a>`;
  header.after(mnav);
  header.querySelector(".burger").addEventListener("click", () => mnav.classList.toggle("open"));
  /* 폰: 오른쪽 아래 동그란 '전화' 단추 */
  const fab = document.createElement("a"); fab.className = "fab"; fab.href = telHref; fab.textContent = "전화";
  document.body.append(fab);

  /* ---------- 바닥 ---------- */
  const foot = document.createElement("footer");
  foot.className = "foot";
  foot.innerHTML = `<div class="wrap">
      <div class="fb"><div class="foot-brand"><b>안집</b><small>${esc(INFO.tagline || "")}</small></div><div><p>${esc(INFO.addr)}</p><a href="${telHref}">${esc(INFO.tel)}</a></div></div>
      <div><h5>영업시간</h5>${HOURS.map(h=>`<p>${esc(h.day)} ${esc(h.open)}</p>`).join("")}${HOURS_NOTE.map(n=>`<p class="mute">${esc(n)}</p>`).join("")}</div>
      <div><h5>주차</h5><p>${esc(INFO.parking)}</p></div>
      <div><h5>이웃</h5><a href="../hanok/">한옥반점</a></div>
    </div>
    <div class="foot-copy"><span>© ${new Date().getFullYear()} 안집</span><span>${INFO.owner ? `대표 ${esc(INFO.owner)}` : ""}${INFO.bizno ? ` · 사업자등록번호 ${esc(INFO.bizno)}` : ""}</span></div>`;
  document.body.append(foot);

  /* ---------- 표시된 자리 채우기 ---------- */
  document.querySelectorAll("[data-t]").forEach(el => { const v = get(el.dataset.t); if(v != null) el.innerHTML = rich(v); });
  document.querySelectorAll("[data-paras]").forEach(el => { const v = get(el.dataset.paras); if(Array.isArray(v)) el.innerHTML = v.map(x => `<p>${rich(x)}</p>`).join(""); });
  document.querySelectorAll("[data-list]").forEach(el => { const v = get(el.dataset.list); if(Array.isArray(v)) el.innerHTML = v.map(x => `<li>${rich(x)}</li>`).join(""); });
  document.querySelectorAll("[data-img]").forEach(el => { const v = get(el.dataset.img); if(v) el.src = imgUrl(v); const a = el.dataset.alt ? get(el.dataset.alt) : null; if(a != null) el.alt = a; });
  document.querySelectorAll("a[data-tel]").forEach(el => { el.href = telHref; el.textContent = INFO.tel; });
  document.querySelectorAll("[data-tel-btn]").forEach(el => { el.href = telHref; });

  const hoursList = () => HOURS.map(h=>`<div><b>${esc(h.day)}</b><span>${esc(h.open)}</span></div>`).join("") + HOURS_NOTE.map(n=>`<div class="note"><b></b><span>${esc(n)}</span></div>`).join("");
  const tvList = () => (S.tv || []).map(t => `<li><b>${esc(t.show)}</b><span>${esc(t.ep)} · ${esc(t.date)} · ${esc(t.what)}</span></li>`).join("");

  /* ---------- 장별 ---------- */
  if(page === "home"){
    $(".hero .slides").innerHTML = S.home.heroSlides.map((x, i) => `<div class="slide${i===0?" on":""}" style="background-image:url(${esc(imgUrl(x))})"></div>`).join("");
    $("#home-sig").innerHTML = SIGNATURE.map(c => `<a href="menu.html"><img src="${esc(imgUrl(c.img))}" alt="${esc(c.name)}" loading="lazy"><b>${esc(c.name)}</b><small>${esc(c.sub||"")}</small></a>`).join("");
    $("#home-tv").innerHTML = tvList();
    $("#home-tiles").innerHTML = S.home.spaceSec.tiles.map(t => `<figure${t.wide?' class="wide"':""}><img src="${esc(imgUrl(t.img))}" alt="${esc(t.alt||"")}"></figure>`).join("");
    $("#home-hours").innerHTML = HOURS.map(h=>`<div class="row"><span>${esc(h.day)}</span><span>${esc(h.open)}</span></div>`).join("") + HOURS_NOTE.map(n=>`<div class="row mute"><span></span><span>${esc(n)}</span></div>`).join("");
    $(".band .in p").innerHTML = S.home.band.lines.map(esc).join("<br>");
    (function slider(){
      const slides = Array.from(document.querySelectorAll(".hero .slide")); if(slides.length < 2) return;
      const dots = $(".hero .dots"); let cur = 0, timer = null;
      dots.innerHTML = slides.map((_, i) => `<button type="button" aria-label="사진 ${i+1}"></button>`).join("");
      const dotEls = Array.from(dots.children);
      const go = n => { cur = (n + slides.length) % slides.length; slides.forEach((s,i)=>s.classList.toggle("on", i===cur)); dotEls.forEach((d,i)=>d.classList.toggle("on", i===cur)); };
      const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches || /[?&]shot/.test(location.search);
      const arm = () => { clearInterval(timer); if(!still) timer = setInterval(() => go(cur+1), 7000); };
      $(".hero .prev").addEventListener("click", () => { go(cur-1); arm(); });
      $(".hero .next").addEventListener("click", () => { go(cur+1); arm(); });
      dotEls.forEach((d,i) => d.addEventListener("click", () => { go(i); arm(); }));
      go(0); arm();
    })();
  }
  if(page === "about"){
    $("#story-pics").innerHTML = S.about.story.pics.map(p => `<figure><img src="${esc(imgUrl(p.img))}" alt="${esc(p.alt||"")}"></figure>`).join("");
    $("#about-tv").innerHTML = tvList();
  }
  if(page === "menu"){
    /* 차림: 묶음마다 이름·설명·가격 한 줄. 가격은 메뉴판 사진 그대로(2026-09) — 바뀔 수 있다는 안내가 아래에 있음 */
    const item = x => `<div class="mi${x.badge?' has-badge':''}">
        <div class="mi-n"><b>${esc(x.name)}</b>${x.size?`<small>${esc(x.size)}</small>`:""}${x.badge?`<em>${esc(x.badge)}</em>`:""}</div>
        ${x.desc?`<div class="mi-d">${esc(x.desc)}</div>`:""}
        <div class="mi-p num">${x.sizes ? x.sizes.map(s=>`<span>${esc(s[0])} <b>${won(s[1])}</b></span>`).join("") : `<b>${won(x.price)}</b>`}</div>
      </div>`;
    $("#menu-body").innerHTML = MENU.map(sec => `<section class="sec" id="${esc(sec.id)}"><div class="wrap ed">
        <div class="eh"><h2>${esc(sec.title)}</h2>${sec.sub?`<p>${esc(sec.sub)}</p>`:""}</div>
        <div><div class="mlist">${sec.items.map(item).join("")}</div>${sec.note?`<p class="cap mnote">${esc(sec.note)}</p>`:""}</div>
      </div></section>`).join("");   /* .wrap.ed 는 두 칸(왼쪽 제목 · 오른쪽 본문) — 본문은 한 덩어리여야 해서 목록과 메모를 같이 감쌈 */
    $("#menu-notes").innerHTML = (S.menuPage.notes||[]).map(n => `<li>${rich(n)}</li>`).join("");
    $("#menu-origin").textContent = S.menuPage.origin || "";
  }
  if(page === "visit"){
    $("#hours").innerHTML = hoursList();
    const nv = $("#lnk-naver"), kk = $("#lnk-kakao");
    if(INFO.naverMap && INFO.naverMap !== "#") nv.href = INFO.naverMap; else nv.remove();
    if(INFO.kakaoMap && INFO.kakaoMap !== "#") kk.href = INFO.kakaoMap; else kk.remove();
  }
});
