/* 손님용 계산대 화면 — 포인트 적립.
   금액이 들어온 화면(결제 금액 · 쌓이는 포인트 · 번호판) → 적립 완료 → 잠시 뒤 다음 손님 금액.
   ★ 11-10 사용자 요청: '직원이 금액을 넣으면 이 화면이 바뀝니다' 같은 안내 대신 금액이 들어온 실제 화면을 바로 보여 줌.
     매장 화면에서 보낸 금액이 있으면 그것을, 없으면 그럴듯한 더미 금액(DUMMY)을 씀 — 더미는 저장하지 않아 매장 화면엔 안 뜸.
   번호판 화면의 '내 포인트만 보기' 로 조회만 할 수도 있습니다.
   ★ 금액은 손님이 아니라 직원이 넣습니다 — 손님이 금액을 바꿀 수 없어야 하니까(POS 대신 직원 손).
   자료는 ../manage/store.js 의 ZB. 매장 화면과는 같은 브라우저의 다른 탭끼리 storage 이벤트로 이어집니다(시안이라 서버 없음). */
(function(){
  const app = document.querySelector("#app");
  ZB.setDevice("계산대");   /* 기록에 '계산대' 로 남음 */
  const S = { mode: "idle", digits: "", agree: false, mkt: false, name: "", done: null, back: 0 };   /* mode: idle 쉬는 화면 · earn 적립 번호 입력 · look 조회 번호 입력 · done 끝 */
  let timer = null;
  const pt = n => n.toLocaleString("ko-KR") + "포인트", won = n => n.toLocaleString("ko-KR") + "원";
  const phoneText = d => "010-" + d.slice(0, 4).padEnd(4, "_") + "-" + d.slice(4).padEnd(4, "_");
  /* 더미 결제 금액 — 고깃집 2~6인 계산 금액쯤. 다음 손님마다 바뀜 */
  const DUMMY = [86000, 64000, 128000, 47000, 152000, 93000, 71000, 118000];
  let di = Math.floor(Math.random() * DUMMY.length);
  const nextDummy = () => { di = (di + 1) % DUMMY.length; S.dummy = { amount: DUMMY[di], dummy: true }; };
  S.dummy = { amount: DUMMY[di], dummy: true };
  const head = `<header class="hd"><img src="../img/logo.png" alt="짚불태백"><span>광교점</span></header>`;

  function render(){
    ZB.reload();
    const pend = ZB.pending || S.dummy;   /* 매장에서 보낸 금액이 먼저, 없으면 더미 */
    if(S.mode === "idle"){ S.mode = "earn"; S.digits = ""; S.agree = false; }
    app.innerHTML = head + (S.mode === "done" ? done() : S.mode === "look" ? keypad(null) : keypad(pend));
  }

  /* 번호 입력 — pend 가 있으면 적립, 없으면 조회 */
  function keypad(pend){
    const full = S.digits.length === 8, phone = "010" + S.digits;
    const isNew = pend && full && !ZB.memberByPhone(phone);
    const ok = full && (!isNew || (S.agree && S.name.trim()));
    const keys = ["1","2","3","4","5","6","7","8","9","","0","del"].map(k => k === "" ? `<span></span>` : `<button data-a="key" data-v="${k}"${k === "del" ? ' aria-label="한 글자 지우기"' : ""}>${k === "del" ? "←" : k}</button>`).join("");
    const get = pend ? Math.floor(pend.amount * ZB.cfg.pointRate / 100) : 0;
    return (pend ? `<section class="now"><div><span>결제 금액</span><b>${won(pend.amount)}</b></div><div><span>쌓이는 포인트</span><b>+${get.toLocaleString("ko-KR")}<small class="u">포인트</small></b></div></section>` : "") + `
      <section class="card grid">
        <div class="left">
          <h2>${pend ? "휴대폰 번호를 눌러 주세요" : "내 포인트 보기"}</h2>
          <div class="phone${full ? " full" : ""}" aria-live="polite">${phoneText(S.digits)}</div>
          ${isNew ? "" : `<p class="sub">${pend ? "처음이시면 이 번호로 바로 회원이 됩니다." : "번호를 누르면 쌓인 포인트를 보여 드립니다."}</p>`}
          ${isNew ? `<label class="nm"><span>성함 <small>성이나 별명도 됩니다 · 포인트를 쓰실 때 확인해요</small></span><input id="nm" value="${S.name.replace(/"/g, "&quot;")}" maxlength="10" autocomplete="off" placeholder="예) 김민수"></label>` : ""}
          ${isNew ? `<button class="agree${S.agree ? " on" : ""}" data-a="agree" role="checkbox" aria-checked="${S.agree}"><i></i><span><b>[필수]</b> 포인트 회원 개인정보 수집·이용 동의<small>번호·성함 · 적립·사용 안내 · 마지막 이용 후 3년 보관</small></span></button>
            <button class="agree opt${S.mkt ? " on" : ""}" data-a="mkt" role="checkbox" aria-checked="${S.mkt}"><i></i><span><b>[선택]</b> 할인·행사 소식 받기<small>안 받으셔도 적립은 똑같습니다</small></span></button>` : ""}
          ${pend ? `<div class="quiets"><button class="quiet" data-a="skip">적립 안 할게요</button><button class="quiet" data-a="look">내 포인트만 보기</button></div>` : `<button class="quiet" data-a="idle">돌아가기</button>`}
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
        <p class="sub">${d.kind === "earn" && c.pointNextDay ? `오늘 쌓인 포인트는 <b>내일부터</b> 쓰실 수 있습니다. ` : ""}${can ? `다음 계산 때 직원에게 성함과 번호를 말씀하시면 <b>${won(d.total)}</b>까지 할인해 드립니다.` : `${pt(c.pointMin - d.total)} 더 모으시면 할인으로 쓰실 수 있습니다.`}</p>
        ${d.soon ? `<p class="sub warn">${pt(d.soon)}가 30일 안에 사라집니다.</p>` : ""}
        ${d.kind === "earn" ? `<p class="sub">적립 내역을 카카오톡으로 보내 드렸습니다.</p>` : ""}
        ${backBtn()}
      </section>`;
  }
  const backBtn = () => `<button class="go" data-a="idle">처음으로 <small>${S.back}초 뒤 자동</small></button>`;

  /* 끝 화면은 잠시 보여 주고 스스로 쉬는 화면으로 — 다음 손님에게 앞 손님 포인트가 보이지 않게 */
  function finish(d){
    S.done = d; S.mode = "done"; S.back = 8; S.digits = ""; S.agree = false; S.mkt = false;
    clearInterval(timer); timer = setInterval(() => { if(--S.back <= 0) goIdle(); else render(); }, 1000);
    render();
  }
  function goIdle(){ clearInterval(timer); timer = null; S.mode = "idle"; S.digits = ""; S.agree = false; S.mkt = false; S.name = ""; S.done = null; render(); }

  document.addEventListener("click", e => {
    const el = e.target.closest("[data-a]"); if(!el) return;
    const a = el.dataset.a, v = el.dataset.v;
    if(a === "key"){ if(v === "del") S.digits = S.digits.slice(0, -1); else if(S.digits.length < 8) S.digits += v; }
    else if(a === "agree") S.agree = !S.agree;
    else if(a === "mkt") S.mkt = !S.mkt;
    else if(a === "look"){ S.mode = "look"; S.digits = ""; }
    else if(a === "idle") return goIdle();
    else if(a === "skip"){ if(ZB.pending) ZB.setPending(null); else nextDummy(); return finish({ kind: "skip" }); }
    else if(a === "earn"){
      ZB.reload(); const pend = ZB.pending || S.dummy; if(!pend || S.digits.length !== 8) return render();
      const phone = "010" + S.digits; if(!ZB.memberByPhone(phone) && !(S.agree && S.name.trim())) return;
      const r = ZB.earn(phone, pend.amount, S.name, "계산대", { mkt: S.mkt }); if(pend.dummy) nextDummy(); else ZB.setPending(null);
      const st = ZB.pstate(r.m.id);
      return finish({ kind: "earn", pts: r.t.pts, total: st.total, soon: st.soon, isNew: r.isNew });
    }
    else if(a === "show"){
      const m = ZB.memberByPhone("010" + S.digits);
      if(!m) return finish({ kind: "none" });
      const st = ZB.pstate(m.id); return finish({ kind: "look", total: st.total, soon: st.soon });
    }
    render();
  });
  document.addEventListener("input", e => {
    if(e.target.id !== "nm") return;
    S.name = e.target.value;
    const go = document.querySelector(".go"); if(go) go.disabled = !(S.digits.length === 8 && S.agree && S.name.trim());
  });
  /* 매장 화면(다른 탭)에서 금액을 보내거나 거두면 바로 바뀜. 끝 화면을 보는 중에는 그대로 둠 */
  window.addEventListener("storage", e => { if(e.key === ZB.KEY && S.mode !== "done" && !(document.activeElement && document.activeElement.id === "nm")) render(); });

  /* 키보드로도 — 노트북에서 보여 줄 때·입구에 키보드를 둔 매장. 숫자, ← 지우기(Backspace), Enter = 주 단추 */
  document.addEventListener("keydown", e => {
    if(e.ctrlKey || e.metaKey || e.altKey) return;
    if(e.target && e.target.id === "nm"){ if(e.key === "Enter"){ const g = document.querySelector(".go:not(:disabled)"); if(g){ e.preventDefault(); g.click(); } } return; }   /* 이름 칸에서는 글자 그대로 */
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
