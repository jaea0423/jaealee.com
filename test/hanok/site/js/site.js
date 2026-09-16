/* 한옥반점 사이트 — 여섯 장이 같이 쓰는 스크립트.
   상단·폰 하단 바·바닥·알림 팝업을 여기서 넣고, <body data-page="..."> 값으로 그 장의 내용을 그립니다.
   가격은 화면에 안 씁니다(메뉴판 PDF 에서만) — data/menu.js 의 price 는 그대로 두고 여기서 안 읽을 뿐입니다.
   예약 창은 js/reserve.js 가 맡습니다(어느 장에서든 [data-reserve] 를 누르면 뜹니다). */
(function(){
  const $ = s => document.querySelector(s);
  const esc = s => String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  const page = document.body.dataset.page || "home";
  if(/[?&]shot/.test(location.search)) document.documentElement.classList.add("shot");   /* 전체 페이지 스크린샷용 */

  /* ---------- 상단 ---------- */
  const L = [["about.html","about","이야기"],["space.html","space","공간"],["menu.html","menu","차림"],["visit.html","visit","오시는 길"]];
  const header = document.createElement("header");
  header.className = "nav";
  header.innerHTML = `<div class="wrap">
      <a class="brand" href="index.html"><span class="brand-ko">한옥반점</span><span class="brand-en">BUNDANG</span></a>
      <nav class="links">${L.map(([h,k,l])=>`<a href="${h}" class="${page===k?'cur':''}">${l}</a>`).join("")}</nav>
      <div class="nav-r"><button type="button" class="btn fill cta" data-reserve>예약하기</button><button class="burger" aria-label="메뉴 열기"><i></i><i></i></button></div>
    </div>`;
  document.body.prepend(header);
  /* 첫 화면 위에서는 사진이 비치게, 내려가면 검정 */
  if(page === "home"){
    const onScroll = () => header.classList.toggle("solid", window.scrollY > 40);
    window.addEventListener("scroll", onScroll, {passive:true}); onScroll();
  }
  const mnav = document.createElement("nav"); mnav.className = "mnav";
  mnav.innerHTML = `<a href="index.html">홈</a>` + L.map(([h,k,l])=>`<a href="${h}">${l}</a>`).join("") + `<a href="#" data-reserve>예약</a><a href="tel:${INFO.tel}">전화 ${esc(INFO.tel)}</a>`;
  header.after(mnav);
  header.querySelector(".burger").addEventListener("click", () => mnav.classList.toggle("open"));
  /* 폰 하단 고정 바 — 차림 · 위치 · 예약이 어디서든 한 번에 */
  const mbar = document.createElement("nav"); mbar.className = "mbar";
  mbar.innerHTML = `<a href="menu.html">차림</a><a href="visit.html">오시는 길</a><a href="#" data-reserve>예약</a>`;
  document.body.append(mbar);

  /* ---------- 바닥 ---------- */
  const foot = document.createElement("footer");
  foot.className = "foot";
  foot.innerHTML = `<div class="wrap">
      <div class="fb"><img class="foot-logo" src="img/logo.png" alt="한옥반점 BUNDANG"><div><p>${esc(INFO.addr)}</p><a href="tel:${INFO.tel}">${esc(INFO.tel)}</a></div></div>
      <div><h5>영업시간</h5>${HOURS.map(h=>`<p>${esc(h.day)} ${esc(h.open)}</p>`).join("")}${HOURS_NOTE.map(n=>`<p class="mute">${esc(n)}</p>`).join("")}</div>
      <div><h5>주차</h5><p>주차비 1,000원 · 발렛 무료</p></div>
      <div><h5>소식</h5><a href="${INFO.instagram}" target="_blank" rel="noopener">인스타그램</a><a href="${INFO.blog}" target="_blank" rel="noopener">블로그</a></div>
    </div>
    <div class="foot-copy"><span>© ${new Date().getFullYear()} 한옥반점</span><span>대표 ${esc(INFO.owner)} · 사업자등록번호 ${esc(INFO.bizno)}</span></div>`;
  document.body.append(foot);

  /* ---------- 팝업창: 여러 개가 왼쪽 위에 겹쳐 뜸. '오늘 하루 보지 않기' 는 그 팝업만 하루 숨김. ?notice=1 이면 무조건 ---------- */
  (function popups(){
    const list = (window.NOTICES || []).filter(n => n && n.title);
    if(!list.length) return;
    const force = /[?&]notice=1/.test(location.search);
    if(!force && /[?&]shot(?!=notice)/.test(location.search)) return;
    const t = new Date(); const ymd = t.getFullYear()+"-"+String(t.getMonth()+1).padStart(2,"0")+"-"+String(t.getDate()).padStart(2,"0");
    /* '오늘 하루' 는 localStorage(날짜), 그냥 닫기는 sessionStorage(이 방문 동안) */
    const hidden = id => { try{ return localStorage.getItem("hanok-pop-"+id) === ymd || sessionStorage.getItem("hanok-pop-"+id) === "1"; }catch(e){ return false; } };
    const show = list.filter(n => (!n.until || ymd <= n.until) && (force || !hidden(n.id)));
    if(!show.length) return;
    const wrap = document.createElement("div"); wrap.className = "pops";
    wrap.innerHTML = show.map((n, i) => `<div class="pop" style="left:${n.x||40}px; top:${n.y||110}px; width:${n.w||360}px; z-index:${10+i}" role="dialog" aria-label="${esc(n.title)}">
        <div class="pop-b">
          ${n.img ? `<img src="img/${esc(n.img)}" alt="${esc(n.title)}">` : `<h3>${esc(n.title)}</h3>${(n.lines||[]).map(l=>`<p>${esc(l)}</p>`).join("")}`}
          ${n.button ? `<button type="button" class="btn fill sm" data-reserve>${esc(n.button)}</button>` : ""}
        </div>
        <div class="pop-f"><label><input type="checkbox" data-day="${esc(n.id)}"> 오늘 하루 보지 않기</label><button type="button" class="x" data-close>닫기</button></div>
      </div>`).join("");
    document.body.append(wrap);
    /* 나중에 연 창이 위로 오게 */
    let z = 10 + show.length;
    wrap.querySelectorAll(".pop").forEach(p => {
      p.addEventListener("mousedown", () => { p.style.zIndex = ++z; });
      p.querySelector("[data-close]").addEventListener("click", () => {
        const chk = p.querySelector("[data-day]");
        try{ if(chk.checked) localStorage.setItem("hanok-pop-"+chk.dataset.day, ymd); sessionStorage.setItem("hanok-pop-"+chk.dataset.day, "1"); }catch(e){}
        p.remove(); if(!wrap.querySelector(".pop")) wrap.remove();
      });
      const rv = p.querySelector("[data-reserve]"); if(rv) rv.addEventListener("click", () => p.querySelector("[data-close]").click());
    });
  })();

  /* ---------- 공통 조각 ---------- */
  const two = arr => { /* 메뉴판처럼 두 단 */
    const h = Math.ceil(arr.length/2); return `<ul>${arr.slice(0,h).map(d=>`<li>${esc(d)}</li>`).join("")}</ul><ul>${arr.slice(h).map(d=>`<li>${esc(d)}</li>`).join("")}</ul>`; };
  const hoursList = () => HOURS.map(h=>`<div><b>${esc(h.day)}</b><span>${esc(h.open)}</span></div>`).join("") + HOURS_NOTE.map(n=>`<div class="note"><b></b><span>${esc(n)}</span></div>`).join("");
  const roomCard = r => `<figure class="room"><img src="img/${r.img}" alt="${esc(r.name)} 룸" loading="lazy"><figcaption>${esc(r.name)}</figcaption></figure>`;
  const hallCard = h => `<figure class="hall"><img src="img/${h.img}" alt="${esc(h.name)}" loading="lazy"><figcaption>${esc(h.name)}</figcaption></figure>`;

  /* ---------- 장별 ---------- */
  if(page === "home"){
    /* 첫 화면 사진 넘김: 7초마다, 화살표·점으로도. 줄이기 설정이면 안 움직임 */
    (function slider(){
      const slides = Array.from(document.querySelectorAll(".hero .slide")); if(slides.length < 2) return;
      const dots = $(".hero .dots"); let cur = 0, timer = null;
      dots.innerHTML = slides.map(() => "<i></i>").join("");
      const dotEls = Array.from(dots.children);
      const go = n => { cur = (n + slides.length) % slides.length; slides.forEach((s,i)=>s.classList.toggle("on", i===cur)); dotEls.forEach((d,i)=>d.classList.toggle("on", i===cur)); };
      const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches || /[?&]shot/.test(location.search);
      const arm = () => { clearInterval(timer); if(!still) timer = setInterval(() => go(cur+1), 7000); };
      $(".hero .prev").addEventListener("click", () => { go(cur-1); arm(); });
      $(".hero .next").addEventListener("click", () => { go(cur+1); arm(); });
      dotEls.forEach((d,i) => d.addEventListener("click", () => { go(i); arm(); }));
      go(0); arm();
    })();
    $("#home-courses").innerHTML = MENU.courses.items.map(c => `<a href="menu.html#courses"><b>${esc(c.name)}<small>${esc(c.cn)}</small></b><i>보기</i></a>`).join("");
    $("#home-hours").innerHTML = HOURS.map(h=>`<div class="row"><span>${esc(h.day)}</span><span>${esc(h.open)}</span></div>`).join("") + HOURS_NOTE.map(n=>`<div class="row mute"><span></span><span>${esc(n)}</span></div>`).join("");
    document.querySelectorAll("a.insta").forEach(a => a.href = INFO.instagram);
    document.querySelectorAll("a.blog").forEach(a => a.href = INFO.blog);
  }
  if(page === "about"){
    document.querySelectorAll("a.insta").forEach(a => a.href = INFO.instagram);
    document.querySelectorAll("a.blog").forEach(a => a.href = INFO.blog);
  }
  if(page === "space"){
    $("#rooms").innerHTML = ROOMS.map(roomCard).join("");
    $("#halls").innerHTML = HALLS.map(hallCard).join("");
  }
  if(page === "menu"){
    $("#courses-body").innerHTML = MENU.courses.items.map(c => `<div class="course">
        <div class="ch"><h3>${esc(c.name)}<small>${esc(c.cn||"")}</small></h3></div>
        <div class="dishes">${two(c.dishes)}</div>
      </div>`).join("");
    $("#lunch-body").innerHTML = MENU.lunch.map(s => `<div class="lunch"><h3>${esc(s.title)}${s.sub?`<small>${esc(s.sub)}</small>`:""}</h3>
        ${s.items.map(x=>`<div class="set"><b>${esc(x.name)}</b><span>${x.dishes.map(esc).join(" · ")}</span></div>`).join("")}</div>`).join("");
    const CN = {"고기류":"肉","해산물류":"海鮮","닭고기류":"鷄","잡품류":"雜","냉채류":"冷菜","탕류":"湯"};
    $("#dishes-body").innerHTML = MENU.dishes.map(g => `<div class="dgroup"><h3>${esc(g.group)}<small>${esc(CN[g.group]||"")}</small></h3>
        ${g.items.map(x=>`<div class="dish"><span class="n">${esc(x.name)}</span></div>`).join("")}</div>`).join("");
    $("#dumplings-body").innerHTML = `<div class="dgroup">
        ${MENU.dumplings.items.map(x=>`<div class="dish"><span class="n">${esc(x.name)}</span></div>`).join("")}</div>`;
    $("#drinks-body").innerHTML = MENU.drinks.map(g => `<div class="dgroup"><h3>${esc(g.group)}</h3>
        ${g.items.map(x=>`<div class="drink"><span class="n">${esc(x.name)}</span>${x.tag?`<span class="opt">${esc(x.tag)}</span>`:""}${x.sizes?`<span class="opt">${x.sizes.map(s=>esc(String(s[0]).replace(/^[대중소]\s*/,""))).filter(Boolean).join(" · ")}</span>`:""}</div>`).join("")}</div>`).join("");
    document.querySelectorAll("a.pdf").forEach(a => a.href = INFO.menuPdf);
  }
  if(page === "visit"){
    $("#hours").innerHTML = hoursList();
    $("#lnk-naver").href = INFO.naverMap; $("#lnk-kakao").href = INFO.kakaoMap;
  }
})();
