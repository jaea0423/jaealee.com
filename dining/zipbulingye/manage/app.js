/* 매장 화면 시안 — 예약 탭.
   화면은 상태(view) 하나로 통째로 다시 그립니다(render). 자료는 store.js 의 ZB.
   설계 원칙(한옥반점에서 가져온 것 하나): 경고는 막지 않고 알리기만 — 자리가 모자라도 직원이 판단해 받을 수 있게.
   단추는 data-a="동작" 으로 표시하고 맨 아래 한 곳에서 처리합니다(문자열 onclick 을 안 써서 따옴표 문제가 없음). */
(function(){
  const $ = (s, r) => (r || document).querySelector(s);
  const esc = s => String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const WD = ["일","월","화","수","목","금","토"];
  const dateText = s => { const d = new Date(s + "T00:00:00"); return (d.getMonth() + 1) + "월 " + d.getDate() + "일 " + WD[d.getDay()] + "요일"; };
  const hm = t => { const m = ZB.mins(t), h = Math.floor(m / 60); return (h < 12 ? "오전 " : "오후 ") + (h % 12 === 0 ? 12 : h % 12) + ":" + String(m % 60).padStart(2, "0"); };
  const STATUS = { req: "새 신청", ok: "확정", in: "방문", noshow: "노쇼", cancel: "취소" };
  const TABS = [["res", "예약", ""], ["wait", "웨이팅", "준비 중"], ["ledger", "선결제 장부", "준비 중"], ["point", "포인트", "준비 중"]];

  const view = { tab: "res", date: ZB.today(), filter: "all", slot: "", sheet: null };
  let form = null, toastTimer = null;

  /* ---------- 그리기 ---------- */
  function render(){
    const app = $("#app");
    app.innerHTML = top() + (view.tab === "res" ? resTab() : soon()) + (view.sheet === "new" ? sheetNew() : view.sheet === "cfg" ? sheetCfg() : "");
  }
  function top(){
    const reqAll = ZB.res.filter(r => r.status === "req" && r.date >= ZB.today()).length;
    return `<div class="top">
        <h1>짚불태백 인계점<small>매장 화면</small></h1>
        <nav class="tabs">${TABS.map(([k, l, note]) => `<button data-a="tab" data-v="${k}" class="${view.tab === k ? "on" : ""}">${l}${k === "res" && reqAll ? `<em>새 신청 ${reqAll}</em>` : note ? `<em>${note}</em>` : ""}</button>`).join("")}</nav>
        <div class="r"><a href="../index.html" target="_blank" rel="noopener">손님 홈페이지</a><button data-a="cfg">설정</button></div>
      </div>
      <div class="demo">제안용 시안 — 예시 자료입니다. 바꾼 내용은 이 브라우저에만 남고, 문자는 실제로 나가지 않습니다.</div>`;
  }
  function soon(){
    const t = TABS.filter(x => x[0] === view.tab)[0];
    return `<div class="soon"><h2>${t[1]}</h2><p>다음 시안에서 만듭니다.</p></div>`;
  }

  function resTab(){
    const list = ZB.byDate(view.date), act = list.filter(r => r.status === "req" || r.status === "ok" || r.status === "in");
    const sum = a => a.reduce((n, r) => n + r.people, 0);
    const cnt = s => list.filter(r => r.status === s).length;
    /* 날짜 줄: 오늘부터 7일 */
    const days = []; for(let i = 0; i < 7; i++) days.push(ZB.addDays(ZB.today(), i));
    const dayBtn = d => { const dt = new Date(d + "T00:00:00"), n = ZB.byDate(d).filter(r => r.status !== "cancel" && r.status !== "noshow").length;
      return `<button data-a="date" data-v="${d}" class="${d === view.date ? "on" : ""}${dt.getDay() === 0 ? " sun" : ""}"><b>${dt.getDate()} ${WD[dt.getDay()]}</b><span>${n}팀</span></button>`; };
    return `<div class="datebar">
        <div class="nav"><button data-a="shift" data-v="-1" aria-label="전날">‹</button><button data-a="shift" data-v="1" aria-label="다음날">›</button><button class="today" data-a="date" data-v="${ZB.today()}">오늘</button></div>
        <h2>${dateText(view.date)}</h2>
        <div class="days">${days.map(dayBtn).join("")}</div>
      </div>
      <div class="kpis">
        <div class="kpi"><span>예약</span><b class="num">${act.length}팀<small>${sum(act)}명</small></b></div>
        <div class="kpi req"><span>확인할 새 신청</span><b class="num">${cnt("req")}건</b></div>
        <div class="kpi"><span>방문</span><b class="num">${cnt("in")}팀<small>${sum(list.filter(r => r.status === "in"))}명</small></b></div>
        <div class="kpi"><span>노쇼 · 취소</span><b class="num">${cnt("noshow")} · ${cnt("cancel")}</b></div>
      </div>
      <div class="cols">${slotPanel()}${listPanel(list)}</div>`;
  }

  /* 왼쪽: 시간대별 테이블 — 그 시각에 차 있는 개수 / 전체. 누르면 그 시각 예약만 */
  function slotPanel(){
    const c = ZB.cfg; let prev = 0;
    const rows = c.slots.map(t => {
      const m = ZB.mins(t), used = ZB.usedAt(view.date, m), left = c.tables - used, pct = Math.min(100, used / c.tables * 100);
      const cls = left <= 0 ? "full" : used >= c.onlineTables ? "hot" : "";
      const gap = prev && m - prev > 30 ? `<div class="gap">브레이크</div>` : ""; prev = m;
      return gap + `<button class="slot${view.slot === t ? " on" : ""}${left <= 0 ? " full" : ""}" data-a="slot" data-v="${t}">
          <span class="t num">${t}</span>
          <span class="bar"><i class="${cls}" style="width:${pct}%"></i><u style="left:${c.onlineTables / c.tables * 100}%"></u></span>
          <span class="n num"><b>${Math.max(0, left)}</b> 남음</span>
        </button>`;
    }).join("");
    return `<section class="panel">
        <header><div><h3>시간대별 테이블</h3><p>전체 ${c.tables}개 · 홈페이지 예약 ${c.onlineTables}개까지</p></div></header>
        ${rows}
        <p class="legend">막대는 그 시각에 예약으로 차 있는 테이블입니다. 점선은 홈페이지로 받는 한도이고, 그 뒤는 워크인·전화용입니다. 한 팀은 ${c.dwellMin / 60}시간 동안 자리를 차지하는 것으로 셉니다.</p>
      </section>`;
  }

  /* 오른쪽: 그 날 예약 목록 */
  function listPanel(all){
    let list = all;
    if(view.slot) list = list.filter(r => { const s = ZB.mins(r.time), m = ZB.mins(view.slot); return s <= m && m < s + ZB.cfg.dwellMin; });
    if(view.filter !== "all") list = list.filter(r => view.filter === "off" ? (r.status === "noshow" || r.status === "cancel") : r.status === view.filter);
    const F = [["all", "전체"], ["req", "새 신청"], ["ok", "확정"], ["in", "방문"], ["off", "노쇼·취소"]];
    const reqs = list.filter(r => r.status === "req"), rest = list.filter(r => r.status !== "req");
    const lunch = rest.filter(r => ZB.mins(r.time) < 15 * 60), dinner = rest.filter(r => ZB.mins(r.time) >= 15 * 60);
    const sec = (title, arr) => arr.length ? `<div class="sec-h">${title} · ${arr.length}팀</div>` + arr.map(card).join("") : "";
    return `<section class="panel">
        <header><div><h3>예약 목록${view.slot ? ` · ${view.slot} 에 있는 팀` : ""}</h3>${view.slot ? `<p><button class="btn sm ghost" data-a="slot" data-v="">시간 선택 풀기</button></p>` : ""}</div>
          <button class="btn pri" data-a="new">+ 예약 등록</button></header>
        <div class="filters">${F.map(([k, l]) => `<button data-a="filter" data-v="${k}" class="${view.filter === k ? "on" : ""}">${l}</button>`).join("")}</div>
        ${list.length ? sec("확인할 새 신청", reqs) + sec("점심", lunch) + sec("저녁", dinner) : `<div class="empty">해당하는 예약이 없습니다.</div>`}
      </section>`;
  }
  function card(r){
    const B = (a, label, cls) => `<button class="btn sm ${cls || ""}" data-a="st" data-id="${esc(r.id)}" data-v="${a}">${label}</button>`;
    const acts = r.status === "req" ? B("ok", "확정", "ok") + B("cancel", "거절", "no")
               : r.status === "ok" ? B("in", "방문", "in") + B("noshow", "노쇼", "no") + B("cancel", "취소")
               : B("ok", "되돌리기");
    return `<article class="res ${r.status}">
        <div class="time"><b class="num">${esc(r.time)}</b><span>${hm(r.time).slice(0, 2)}</span></div>
        <div class="who">
          <div class="l1"><b>${esc(r.name)}</b><span class="ppl num">${r.people}명</span><span class="chip ${r.status}">${STATUS[r.status]}</span><span class="chip src">${esc(r.src || "")}</span></div>
          <div class="l2 num">${esc(r.phone)} · 테이블 ${ZB.tablesFor(r.people)}개</div>
          ${r.pre || r.memo ? `<div class="l3">${r.pre ? `<mark>미리 주문 ${esc(r.pre)}</mark>` : ""}${esc(r.memo || "")}</div>` : ""}
        </div>
        <div class="acts">${acts}</div>
      </article>`;
  }

  /* ---------- 예약 등록(전화·방문 접수) ---------- */
  function sheetNew(){
    const c = ZB.cfg, f = form, need = ZB.tablesFor(f.people);
    const tb = c.slots.map(t => { const left = ZB.leftAt(f.date, t, false), cls = left < need ? "over" : left - need < 3 ? "tight" : "";
      return `<button data-a="f-time" data-v="${t}" class="${f.time === t ? "on " : ""}${cls}"><b class="num">${t}</b><span>${left <= 0 ? "자리 없음" : "남음 " + left}</span></button>`; }).join("");
    const over = f.time && !ZB.fits(f.date, f.time, f.people, false);
    const ok = f.time && f.name.trim().length >= 1;
    return `<div class="ov" data-a="close-ov"><div class="sheet" role="dialog" aria-modal="true" aria-label="예약 등록">
        <header><h3>예약 등록 · ${dateText(f.date)}</h3><button class="btn sm ghost" data-a="close">닫기</button></header>
        <div class="body">
          <div class="fld"><span>인원<em>테이블 ${need}개</em></span>
            <div class="step"><button data-a="f-ppl" data-v="-1" aria-label="한 명 줄이기">−</button><b class="num">${f.people}</b><button data-a="f-ppl" data-v="1" aria-label="한 명 늘리기">+</button><span>명</span></div></div>
          <div class="fld"><span>시간<em>숫자는 그 시각에 남는 테이블</em></span><div class="tgrid">${tb}</div></div>
          <div class="two">
            <div class="fld"><label for="f-name">성함</label><input id="f-name" data-f="name" value="${esc(f.name)}" autocomplete="off"></div>
            <div class="fld"><label for="f-phone">전화번호</label><input id="f-phone" data-f="phone" value="${esc(f.phone)}" inputmode="numeric" autocomplete="off" placeholder="010-0000-0000"></div>
          </div>
          <div class="fld"><label for="f-memo">메모<em>미리 주문 · 요청사항</em></label><input id="f-memo" data-f="memo" value="${esc(f.memo)}" autocomplete="off"></div>
        </div>
        <footer>${over ? `<span class="warn">이 시각은 테이블이 모자랍니다. 그래도 받을 수 있습니다.</span>` : ""}
          <button class="btn" data-a="close">취소</button><button class="btn pri" data-a="f-save"${ok ? "" : " disabled"}>등록</button></footer>
      </div></div>`;
  }

  /* ---------- 설정: 테이블 개수 ---------- */
  function sheetCfg(){
    const c = ZB.cfg;
    const row = (k, title, note, val, unit) => `<div class="row"><div class="lbl"><b>${title}</b><span>${note}</span></div>
        <div class="step"><button data-a="c" data-k="${k}" data-v="-1">−</button><b class="num">${val}</b><button data-a="c" data-k="${k}" data-v="1">+</button><span>${unit}</span></div></div>`;
    return `<div class="ov" data-a="close-ov"><div class="sheet" role="dialog" aria-modal="true" aria-label="설정">
        <header><h3>설정 · 테이블</h3><button class="btn sm ghost" data-a="close">닫기</button></header>
        <div class="body">
          ${row("tables", "전체 테이블", "매장에 있는 테이블 수", c.tables, "개")}
          ${row("onlineTables", "홈페이지 예약 한도", "이 개수까지만 홈페이지로 받고 나머지는 워크인·전화용", c.onlineTables, "개")}
          ${row("seats", "한 테이블 좌석", "인원을 이 수로 나눠 필요한 테이블을 셉니다", c.seats, "명")}
          ${row("dwellMin", "한 팀 식사 시간", "이 시간 동안 자리를 차지하는 것으로 셉니다", c.dwellMin, "분")}
          <p class="hint">어느 테이블에 앉힐지는 정하지 않습니다. 개수만 세기 때문에 좌석 배치도를 그리거나 관리할 필요가 없습니다. 바꾸면 손님 홈페이지의 예약 가능 시간에도 바로 반영됩니다.</p>
        </div>
        <footer><button class="btn ghost" data-a="reset">예시 자료 처음으로</button><button class="btn pri" data-a="close">확인</button></footer>
      </div></div>`;
  }

  function toast(msg, sub){
    const old = $(".toast"); if(old) old.remove();
    const t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status");
    t.innerHTML = esc(msg) + (sub ? `<small>${esc(sub)}</small>` : "");
    document.body.append(t); clearTimeout(toastTimer); toastTimer = setTimeout(() => t.remove(), 3200);
  }

  /* ---------- 누름 처리 (한 곳) ---------- */
  document.addEventListener("click", e => {
    const el = e.target.closest("[data-a]"); if(!el) return;
    const a = el.dataset.a, v = el.dataset.v;
    if(a === "close-ov"){ if(e.target !== el) return; view.sheet = null; return render(); }   /* 바깥 어두운 곳을 눌렀을 때만 닫음 */
    if(a === "tab"){ view.tab = v; }
    else if(a === "date"){ view.date = v; view.slot = ""; }
    else if(a === "shift"){ view.date = ZB.addDays(view.date, Number(v)); view.slot = ""; }
    else if(a === "slot"){ view.slot = view.slot === v ? "" : v; }
    else if(a === "filter"){ view.filter = v; }
    else if(a === "cfg"){ view.sheet = "cfg"; }
    else if(a === "close"){ view.sheet = null; }
    else if(a === "new"){ form = { date: view.date, time: view.slot || "", people: 4, name: "", phone: "", memo: "" }; view.sheet = "new"; }
    else if(a === "f-ppl"){ form.people = Math.max(1, Math.min(40, form.people + Number(v))); }
    else if(a === "f-time"){ form.time = v; }
    else if(a === "f-save"){
      if(!form.time || !form.name.trim()) return;
      ZB.add({ date: form.date, time: form.time, people: form.people, name: form.name.trim(), phone: form.phone.trim(), memo: form.memo.trim(), pre: "", status: "ok", src: "전화" });
      view.sheet = null; toast(`${form.name.trim()} 님 ${form.time} ${form.people}명 예약을 등록했습니다`, form.phone.trim() ? "확정 문자를 보냈습니다 (시안: 실제 발송 없음)" : "");
    }
    else if(a === "st"){
      const r = ZB.update(el.dataset.id, { status: v });
      if(r){ const M = { ok: "확정했습니다", in: "방문 처리했습니다", noshow: "노쇼로 표시했습니다", cancel: "취소했습니다" };
        toast(`${r.name} 님 ${r.time} 예약을 ${M[v]}`, (v === "ok" || v === "cancel") && r.phone ? "손님에게 안내 문자를 보냈습니다 (시안: 실제 발송 없음)" : ""); }
    }
    else if(a === "c"){
      const k = el.dataset.k, c = ZB.cfg, step = k === "dwellMin" ? 30 : 1, min = k === "dwellMin" ? 60 : k === "seats" ? 2 : 1, max = k === "dwellMin" ? 240 : k === "seats" ? 8 : k === "onlineTables" ? c.tables : 80;
      const p = {}; p[k] = Math.max(min, Math.min(max, c[k] + Number(v) * step)); ZB.setCfg(p);
    }
    else if(a === "reset"){ ZB.reset(); view.sheet = null; toast("예시 자료를 처음 상태로 되돌렸습니다"); }
    render();
  });
  /* 글자 칸은 다시 그리지 않고 값만 받아 둠(그리면 입력 중에 초점이 날아감). 등록 단추만 켜고 끔 */
  document.addEventListener("input", e => {
    const k = e.target.dataset && e.target.dataset.f; if(!k || !form) return;
    form[k] = e.target.value;
    const b = $("[data-a=f-save]"); if(b) b.disabled = !(form.time && form.name.trim());
  });
  document.addEventListener("keydown", e => { if(e.key === "Escape" && view.sheet){ view.sheet = null; render(); } });
  /* 손님 홈페이지(다른 탭)에서 예약이 들어오면 바로 반영 — 실제 서비스의 '새 신청 알림' 자리 */
  window.addEventListener("storage", e => {
    if(e.key !== ZB.KEY) return;
    const before = ZB.res.filter(r => r.status === "req").length; ZB.reload();
    const after = ZB.res.filter(r => r.status === "req").length;
    if(!view.sheet) render();
    if(after > before) toast("홈페이지에서 새 예약 신청이 들어왔습니다");
  });

  render();
})();
