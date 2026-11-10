/* 손님용 웨이팅 화면 시안.
   · 주소 그대로 열면: 매장 입구 태블릿의 접수 화면 (인원 → 전화번호 → 접수 → 대기번호)
   · ?no=12 로 열면: 손님 휴대폰의 '내 순서' 화면 (실제 서비스에서는 알림톡 속 링크가 여기로 옴)
   자료는 ../manage/store.js 의 ZB — 매장 화면 웨이팅 탭과 같은 것을 씁니다.
   입구 태블릿은 여러 손님이 이어서 쓰므로, 접수가 끝나면 잠시 뒤 스스로 처음 화면으로 돌아갑니다(앞 손님 번호가 남지 않게). */
(function(){
  const $ = s => document.querySelector(s);
  const app = $("#app");
  const myNo = Number(new URLSearchParams(location.search).get("no")) || 0;
  const S = { step: "form", people: 2, digits: "", agree: false, mine: null, back: 0 };
  let timer = null;
  const BACK_SEC = 12;

  const phoneText = d => "010-" + (d.slice(0, 4) || "").padEnd(4, "_") + "-" + (d.slice(4) || "").padEnd(4, "_");
  const etaText = n => n > 0 ? "약 " + ZB.waitEta(n) + "분" : "곧 입장";
  const head = `<header class="hd"><img src="../img/logo.png" alt="짚불태백"><span>인계점</span></header>`;

  function render(){
    ZB.reload();   /* 매장 화면에서 바꾼 것을 늘 새로 읽음 */
    app.innerHTML = myNo ? status() : S.step === "done" ? done() : form();
  }

  /* ---------- 접수 화면(입구 태블릿) ---------- */
  function form(){
    const live = ZB.waitLive(), n = live.length;
    if(!ZB.wait.on) return head + `<section class="card center"><h1>지금은 웨이팅을 받지 않습니다</h1><p class="sub">직원에게 말씀해 주세요.</p></section>`;
    const ok = S.digits.length === 8 && S.agree;
    const keys = ["1","2","3","4","5","6","7","8","9","","0","del"].map(k => k === "" ? `<span></span>` : `<button data-a="key" data-v="${k}"${k === "del" ? ' aria-label="한 글자 지우기"' : ""}>${k === "del" ? "←" : k}</button>`).join("");
    return head + `<section class="now"><div><span>지금 대기</span><b>${n}팀</b></div><div><span>예상 대기</span><b>${n ? "약 " + ZB.waitEta(n) + "분" : "바로 입장"}</b></div></section>
      <section class="card grid">
        <div class="left">
          <h2>인원</h2>
          <div class="step"><button data-a="ppl" data-v="-1" aria-label="한 명 줄이기">−</button><b>${S.people}<small>명</small></b><button data-a="ppl" data-v="1" aria-label="한 명 늘리기">+</button></div>
          <p class="sub">아이도 인원에 넣어 주세요.</p>
          <h2>휴대폰 번호</h2>
          <div class="phone${S.digits.length === 8 ? " full" : ""}" aria-live="polite">${phoneText(S.digits)}</div>
          <p class="sub">순서가 가까워지면 이 번호로 알려 드립니다.</p>
          <button class="agree${S.agree ? " on" : ""}" data-a="agree" role="checkbox" aria-checked="${S.agree}"><i></i><span>대기 안내를 위한 전화번호 수집에 동의합니다<small>오늘 영업이 끝나면 지웁니다 (예시 문구)</small></span></button>
        </div>
        <div class="right">
          <div class="pad">${keys}</div><p class="kbd">키보드 숫자로도 누를 수 있습니다 · Enter</p>
          <button class="go" data-a="go"${ok ? "" : " disabled"}>웨이팅 접수</button>
        </div>
      </section>`;
  }
  function done(){
    const x = S.mine, ahead = ZB.waitAhead(x.id);
    return head + `<section class="card center">
        <p class="sub">${S.dup ? "이미 접수된 번호입니다" : "접수되었습니다"}</p>
        <div class="big"><span>대기번호</span><b>${x.no}</b></div>
        <div class="pair"><div><span>내 앞</span><b>${Math.max(0, ahead)}팀</b></div><div><span>예상 대기</span><b>${etaText(ahead)}</b></div></div>
        <p class="sub">순서가 가까워지면 카카오 알림톡으로 알려 드립니다.</p>
        <a class="link" href="?no=${x.no}" target="_blank" rel="noopener">손님 휴대폰에서 보이는 화면 예시</a>
        <button class="go" data-a="home">처음으로 <small>${S.back}초 뒤 자동</small></button>
      </section>`;
  }

  /* ---------- 내 순서(손님 휴대폰) ---------- */
  function status(){
    const x = ZB.wait.list.filter(r => r.no === myNo)[0];
    if(!x) return head + `<section class="card center narrow"><h1>대기번호 ${myNo}번을 찾을 수 없습니다</h1><p class="sub">오늘 접수한 번호가 맞는지 확인해 주세요.</p></section>`;
    const ahead = ZB.waitAhead(x.id);
    const body = x.status === "call" ? `<div class="callbox"><b>지금 입장해 주세요</b><span>매장 입구에서 대기번호를 말씀해 주세요.</span></div>`
      : x.status === "wait" ? `<div class="pair"><div><span>내 앞</span><b>${ahead}팀</b></div><div><span>예상 대기</span><b>${etaText(ahead)}</b></div></div>
          <p class="sub">이 화면은 스스로 새로 고쳐집니다. 순서가 되면 알림톡으로도 알려 드립니다.</p>`
      : `<div class="endbox">${x.status === "in" ? "입장하셨습니다. 맛있게 드세요." : x.status === "gone" ? "호출 뒤 오지 않으셔서 순서가 넘어갔습니다. 매장에 말씀해 주세요." : "웨이팅이 취소되었습니다."}</div>`;
    return head + `<section class="card center narrow">
        <div class="big"><span>대기번호</span><b>${x.no}</b></div>
        <p class="sub">${x.people}명</p>
        ${body}
        ${x.status === "wait" || x.status === "call" ? `<button class="quiet" data-a="cancel">웨이팅 취소</button>` : ""}
      </section>`;
  }

  function goHome(){ clearInterval(timer); timer = null; S.step = "form"; S.people = 2; S.digits = ""; S.agree = false; S.mine = null; S.dup = false; render(); }

  document.addEventListener("click", e => {
    const el = e.target.closest("[data-a]"); if(!el) return;
    const a = el.dataset.a, v = el.dataset.v;
    if(a === "ppl") S.people = Math.max(1, Math.min(20, S.people + Number(v)));
    else if(a === "key"){ if(v === "del") S.digits = S.digits.slice(0, -1); else if(S.digits.length < 8) S.digits += v; }
    else if(a === "agree") S.agree = !S.agree;
    else if(a === "go"){
      if(S.digits.length !== 8 || !S.agree) return;
      ZB.reload();
      const phone = "010-" + S.digits.slice(0, 4) + "-" + S.digits.slice(4);
      const had = ZB.waitLive().filter(x => x.phone === phone)[0];   /* 같은 번호로 두 번 누르면 새 번호를 주지 않고 원래 번호를 보여 줌 */
      S.mine = had || ZB.waitAdd(S.people, phone, "매장 접수"); S.dup = !!had;
      S.step = "done"; S.back = BACK_SEC;
      clearInterval(timer); timer = setInterval(() => { if(--S.back <= 0) goHome(); else render(); }, 1000);
    }
    else if(a === "home") return goHome();
    else if(a === "cancel"){ const x = ZB.wait.list.filter(r => r.no === myNo)[0]; if(x && confirm("웨이팅을 취소할까요?")) ZB.waitSet(x.id, "cancel"); }
    render();
  });
  /* 매장 화면(다른 탭)에서 호출·입장을 누르면 바로 반영 */
  window.addEventListener("storage", e => { if(e.key === ZB.KEY && S.step !== "done") render(); });
  if(myNo) setInterval(render, 20000);   /* 예상 대기 숫자가 멈춰 보이지 않게 */

  /* 키보드로도 — 노트북에서 보여 줄 때·입구에 키보드를 둔 매장. 숫자, ← 지우기(Backspace), Enter = 주 단추 */
  document.addEventListener("keydown", e => {
    if(e.ctrlKey || e.metaKey || e.altKey) return;
    let sel = null;
    if(/^[0-9]$/.test(e.key)) sel = '[data-a=key][data-v="' + e.key + '"]';
    else if(e.key === "Backspace") sel = '[data-a=key][data-v="del"]';
    else if(e.key === "Enter") sel = ".go:not(:disabled)";
    const b = sel && document.querySelector(sel); if(!b) return;
    e.preventDefault(); b.click();
    const again = sel.indexOf("data-a=key") >= 0 && document.querySelector(sel);   /* 다시 그린 뒤의 같은 단추에 잠깐 눌림 표시 */
    if(again){ again.classList.add("hit"); setTimeout(() => again.classList.remove("hit"), 120); }
  });

  render();
})();
