/* 손님용 계산대 화면 시안 — 포인트 적립.
   쉬는 화면 → (직원이 매장 화면에서 결제 금액을 보냄) → 번호 입력 → 적립 완료 → 잠시 뒤 쉬는 화면.
   쉬는 화면에서 '내 포인트 보기' 로 번호만 넣어 조회할 수도 있습니다.
   ★ 금액은 손님이 아니라 직원이 넣습니다 — 손님이 금액을 바꿀 수 없어야 하니까(POS 대신 직원 손).
   자료는 ../manage/store.js 의 ZB. 매장 화면과는 같은 브라우저의 다른 탭끼리 storage 이벤트로 이어집니다(시안이라 서버 없음). */
(function(){
  const app = document.querySelector("#app");
  const S = { mode: "idle", digits: "", agree: false, done: null, back: 0 };   /* mode: idle 쉬는 화면 · earn 적립 번호 입력 · look 조회 번호 입력 · done 끝 */
  let timer = null;
  const pt = n => n.toLocaleString("ko-KR") + "P", won = n => n.toLocaleString("ko-KR") + "원";
  const phoneText = d => "010-" + d.slice(0, 4).padEnd(4, "_") + "-" + d.slice(4).padEnd(4, "_");
  const head = `<header class="hd"><img src="../img/logo.png" alt="짚불태백"><span>인계점</span></header>`;

  function render(){
    ZB.reload();
    const pend = ZB.pending;
    if(pend && (S.mode === "idle" || S.mode === "look")){ S.mode = "earn"; S.digits = ""; S.agree = false; }   /* 금액이 오면 바로 번호 입력으로 */
    if(!pend && S.mode === "earn"){ S.mode = "idle"; }                                                        /* 직원이 거두면 쉬는 화면으로 */
    app.innerHTML = head + (S.mode === "done" ? done() : S.mode === "earn" ? keypad(pend) : S.mode === "look" ? keypad(null) : idle());
  }

  function idle(){
    const c = ZB.cfg;
    return `<section class="card center pidle">
        <p class="sub">짚불태백 인계점 포인트</p>
        <h1>결제 금액의 <em>${c.pointRate}%</em>를 쌓아 드립니다</h1>
        <p class="sub">휴대폰 번호만 누르면 끝 — 앱 설치도 가입도 없습니다.<br>${pt(c.pointMin)}부터 다음 계산에서 1P = 1원으로 할인됩니다.</p>
        <div class="wait-dot"><i></i>계산할 때 직원이 금액을 넣으면 이 화면이 바뀝니다</div>
        <button class="quiet" data-a="look">내 포인트 보기</button>
      </section>`;
  }

  /* 번호 입력 — pend 가 있으면 적립, 없으면 조회 */
  function keypad(pend){
    const full = S.digits.length === 8, phone = "010" + S.digits;
    const isNew = pend && full && !ZB.memberByPhone(phone);
    const ok = full && (!isNew || S.agree);
    const keys = ["1","2","3","4","5","6","7","8","9","","0","del"].map(k => k === "" ? `<span></span>` : `<button data-a="key" data-v="${k}"${k === "del" ? ' aria-label="한 글자 지우기"' : ""}>${k === "del" ? "←" : k}</button>`).join("");
    const get = pend ? Math.floor(pend.amount * ZB.cfg.pointRate / 100) : 0;
    return (pend ? `<section class="now"><div><span>결제 금액</span><b>${won(pend.amount)}</b></div><div><span>쌓이는 포인트</span><b>+${pt(get)}</b></div></section>` : "") + `
      <section class="card grid">
        <div class="left">
          <h2>${pend ? "휴대폰 번호를 눌러 주세요" : "내 포인트 보기"}</h2>
          <div class="phone${full ? " full" : ""}" aria-live="polite">${phoneText(S.digits)}</div>
          <p class="sub">${pend ? "처음이시면 이 번호로 바로 회원이 됩니다." : "번호를 누르면 쌓인 포인트를 보여 드립니다."}</p>
          ${isNew ? `<button class="agree${S.agree ? " on" : ""}" data-a="agree" role="checkbox" aria-checked="${S.agree}"><i></i><span>포인트 적립을 위한 전화번호 수집에 동의합니다<small>적립·사용 내역 안내에만 씁니다 (예시 문구)</small></span></button>` : ""}
          ${pend ? `<button class="quiet" data-a="skip">적립 안 할게요</button>` : `<button class="quiet" data-a="idle">돌아가기</button>`}
        </div>
        <div class="right">
          <div class="pad">${keys}</div>
          <button class="go" data-a="${pend ? "earn" : "show"}"${ok ? "" : " disabled"}>${pend ? "적립하기" : "조회"}</button>
        </div>
      </section>`;
  }

  function done(){
    const d = S.done, c = ZB.cfg, can = d.total >= c.pointMin;
    if(d.kind === "skip") return `<section class="card center"><h1>감사합니다</h1><p class="sub">다음에 또 오세요.</p>${backBtn()}</section>`;
    if(d.kind === "none") return `<section class="card center"><h1>아직 쌓인 포인트가 없습니다</h1><p class="sub">계산할 때 번호를 누르시면 결제 금액의 ${c.pointRate}%가 쌓입니다.</p>${backBtn()}</section>`;
    return `<section class="card center">
        <p class="sub">${d.kind === "earn" ? (d.isNew ? "회원이 되셨습니다 · " : "") + "적립되었습니다" : "내 포인트"}</p>
        ${d.kind === "earn" ? `<div class="big"><span>이번에 쌓인 포인트</span><b>+${d.pts.toLocaleString("ko-KR")}</b></div>` : ""}
        <div class="pair one"><div><span>모두</span><b>${pt(d.total)}</b></div></div>
        <p class="sub">${can ? `다음 계산 때 직원에게 말씀하시면 <b>${won(d.total)}</b>까지 할인해 드립니다.` : `${pt(c.pointMin - d.total)} 더 모으시면 할인으로 쓰실 수 있습니다.`}</p>
        ${d.kind === "earn" ? `<p class="sub">적립 내역을 카카오 알림톡으로 보내 드렸습니다. (시안: 실제 발송 없음)</p>` : ""}
        ${backBtn()}
      </section>`;
  }
  const backBtn = () => `<button class="go" data-a="idle">처음으로 <small>${S.back}초 뒤 자동</small></button>`;

  /* 끝 화면은 잠시 보여 주고 스스로 쉬는 화면으로 — 다음 손님에게 앞 손님 포인트가 보이지 않게 */
  function finish(d){
    S.done = d; S.mode = "done"; S.back = 8; S.digits = ""; S.agree = false;
    clearInterval(timer); timer = setInterval(() => { if(--S.back <= 0) goIdle(); else render(); }, 1000);
    render();
  }
  function goIdle(){ clearInterval(timer); timer = null; S.mode = "idle"; S.digits = ""; S.agree = false; S.done = null; render(); }

  document.addEventListener("click", e => {
    const el = e.target.closest("[data-a]"); if(!el) return;
    const a = el.dataset.a, v = el.dataset.v;
    if(a === "key"){ if(v === "del") S.digits = S.digits.slice(0, -1); else if(S.digits.length < 8) S.digits += v; }
    else if(a === "agree") S.agree = !S.agree;
    else if(a === "look"){ S.mode = "look"; S.digits = ""; }
    else if(a === "idle") return goIdle();
    else if(a === "skip"){ ZB.setPending(null); return finish({ kind: "skip" }); }
    else if(a === "earn"){
      ZB.reload(); const pend = ZB.pending; if(!pend || S.digits.length !== 8) return render();
      const phone = "010" + S.digits; if(!ZB.memberByPhone(phone) && !S.agree) return;
      const r = ZB.earn(phone, pend.amount); ZB.setPending(null);
      return finish({ kind: "earn", pts: r.t.pts, total: ZB.pbal(r.m.id), isNew: r.isNew });
    }
    else if(a === "show"){
      const m = ZB.memberByPhone("010" + S.digits);
      return finish(m ? { kind: "look", total: ZB.pbal(m.id) } : { kind: "none" });
    }
    render();
  });
  /* 매장 화면(다른 탭)에서 금액을 보내거나 거두면 바로 바뀜. 끝 화면을 보는 중에는 그대로 둠 */
  window.addEventListener("storage", e => { if(e.key === ZB.KEY && S.mode !== "done") render(); });

  render();
})();
