/* 매장 화면 시안 — 예약 탭 · 웨이팅 탭 · 선결제 장부 탭 · 포인트 탭.
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
  const TABS = [["res", "예약", ""], ["wait", "웨이팅", ""], ["ledger", "선결제 장부", ""], ["point", "포인트", ""], ["close", "마감·기록", ""]];

  /* 주소 끝 #wait · #ledger · #point 로 열면 그 탭부터 (안내 페이지 단추가 탭별로 바로 열리게) */
  const nowMin = () => { const d = new Date(); return d.getHours() * 60 + d.getMinutes(); };
  const view = { tab: TABS.some(t => t[0] === location.hash.slice(1)) ? location.hash.slice(1) : "res", date: ZB.today(), filter: "all", slot: "", sheet: null };
  let form = null, toastTimer = null;

  /* ---------- 그리기 ---------- */
  function render(){
    const app = $("#app");
    app.innerHTML = top() + (view.tab === "res" ? resTab() : view.tab === "wait" ? waitTab() : view.tab === "ledger" ? ledgerTab() : view.tab === "point" ? pointTab() : view.tab === "close" ? closeTab() : soon())
      + (view.sheet === "new" ? sheetNew() : view.sheet === "cfg" ? sheetCfg() : view.sheet === "wnew" ? sheetWait()
        : view.sheet === "lx" ? sheetTx() : view.sheet === "la" ? sheetAcct() : view.sheet === "pe" ? sheetEarn() : view.sheet === "pu" ? sheetUse() : "");
  }
  function top(){
    const reqAll = ZB.res.filter(r => r.status === "req" && r.date >= ZB.today()).length, waitN = ZB.waitLive().length;
    return `<div class="top">
        <h1>짚불태백 광교점<small>매장 화면</small></h1>
        <nav class="tabs">${TABS.map(([k, l, note]) => `<button data-a="tab" data-v="${k}" class="${view.tab === k ? "on" : ""}">${l}${k === "res" && reqAll ? `<em aria-label="새 신청 ${reqAll}건" title="확인할 새 신청">${reqAll}</em>` : k === "wait" && waitN ? `<em class="b" aria-label="대기 ${waitN}팀" title="지금 대기">${waitN}</em>` : note ? `<em>${note}</em>` : ""}</button>`).join("")}</nav>
        <div class="r"><a href="../home.html" target="_blank" rel="noopener">손님 홈페이지</a><button data-a="cfg">설정</button></div>
      </div>`;
  }
  function soon(){
    const t = TABS.filter(x => x[0] === view.tab)[0];
    return `<div class="soon"><h2>${t[1]}</h2><p>준비 중입니다.</p></div>`;
  }

  function resTab(){
    const list = ZB.byDate(view.date), act = list.filter(r => r.status === "req" || r.status === "ok" || r.status === "in");
    const sum = a => a.reduce((n, r) => n + r.people, 0);
    const cnt = s => list.filter(r => r.status === s).length;
    /* 날짜 줄: 오늘부터 7일 */
    const days = []; for(let i = 0; i < 7; i++) days.push(ZB.addDays(ZB.today(), i));
    const dayBtn = d => { const dt = new Date(d + "T00:00:00"), n = ZB.byDate(d).filter(r => r.status !== "cancel" && r.status !== "noshow").length;
      return `<button data-a="date" data-v="${d}" class="${d === view.date ? "on" : ""}${dt.getDay() === 0 ? " sun" : dt.getDay() === 6 ? " sat" : ""}"><b>${dt.getDate()} ${WD[dt.getDay()]}</b><span>${n}팀</span></button>`; };
    return `<div class="datebar">
        <div class="nav"><button data-a="shift" data-v="-1" aria-label="전날">‹</button><button data-a="shift" data-v="1" aria-label="다음날">›</button><button class="today" data-a="date" data-v="${ZB.today()}">오늘</button></div>
        <h2>${dateText(view.date)}</h2>
        <div class="days">${days.map(dayBtn).join("")}</div>
      </div>
      <div class="kpis">
        <div class="kpi"><span>예약</span><b class="num">${act.length}팀<small>${sum(act)}명</small></b></div>
        <div class="kpi${cnt("req") ? " req" : ""}"><span>확인할 새 신청</span><b class="num">${cnt("req")}건</b></div>
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
      const isNow = view.date === ZB.today() && m <= nowMin() && nowMin() < m + 30;   /* 지금 시각이 든 줄 */
      return gap + `<button class="slot${view.slot === t ? " on" : ""}${left <= 0 ? " full" : ""}${isNow ? " now" : ""}" data-a="slot" data-v="${t}"${isNow ? ' aria-current="time"' : ""}>
          <span class="t num">${t}</span>
          <span class="bar"><i class="${cls}" style="width:${pct}%"></i><u style="left:${c.onlineTables / c.tables * 100}%"></u></span>
          <span class="n num"><b>${Math.max(0, left)}</b> 남음</span>
        </button>`;
    }).join("");
    return `<section class="panel">
        <header><div><h3>시간대별 테이블</h3><p>전체 ${c.tables}개 · 홈페이지 예약 ${c.onlineTables}개까지</p></div></header>
        ${rows}
        <p class="legend">막대는 그 시각에 예약으로 차 있는 테이블입니다. 점선은 홈페이지로 받는 한도이고, 그 뒤는 워크인·전화용입니다. 한 팀은 평균 이용 시간(점심 ${c.dwellLunch}분 · 저녁 ${c.dwellDinner}분) 동안 자리를 차지하는 것으로 셉니다.</p>
      </section>`;
  }

  /* 오른쪽: 그 날 예약 목록 */
  function listPanel(all){
    let list = all;
    if(view.slot) list = list.filter(r => { const s = ZB.mins(r.time), m = ZB.mins(view.slot); return s <= m && m < s + ZB.dwellFor(r.time); });
    if(view.filter !== "all") list = list.filter(r => view.filter === "off" ? (r.status === "noshow" || r.status === "cancel") : r.status === view.filter);
    const F = [["all", "전체"], ["req", "새 신청"], ["ok", "확정"], ["in", "방문"], ["off", "노쇼·취소"]];
    const reqs = list.filter(r => r.status === "req"), rest = list.filter(r => r.status !== "req");
    const lunch = rest.filter(r => ZB.mins(r.time) < 15 * 60), dinner = rest.filter(r => ZB.mins(r.time) >= 15 * 60);
    /* 오늘 목록에는 '지금' 줄을 넣어 지난 팀과 올 팀을 한눈에 나눔(시간을 골라 본 때는 빼고) */
    let marked = view.date !== ZB.today() || !!view.slot;
    const nowLine = () => { const n = nowMin(); return `<div class="now-line" role="separator"><span>지금 ${ZB.hhmm(n)}</span></div>`; };
    const rows = arr => arr.map(r => { let h = ""; if(!marked && ZB.mins(r.time) >= nowMin()){ marked = true; h = nowLine(); } return h + card(r); }).join("");
    const sec = (title, arr) => arr.length ? `<div class="sec-h">${title} · ${arr.length}팀</div>` + (title === "확인할 새 신청" ? arr.map(card).join("") : rows(arr)) : "";
    return `<section class="panel">
        <header><div><h3>예약 목록${view.slot ? ` · ${view.slot} 에 있는 팀` : ""}</h3>${view.slot ? `<p><button class="btn sm ghost" data-a="slot" data-v="">시간 선택 풀기</button></p>` : ""}</div>
          <button class="btn pri" data-a="new">+ 예약 등록</button></header>
        <div class="filters">${F.map(([k, l]) => `<button data-a="filter" data-v="${k}" class="${view.filter === k ? "on" : ""}">${l}</button>`).join("")}</div>
        ${list.length ? sec("확인할 새 신청", reqs) + sec("점심", lunch) + sec("저녁", dinner) + (!marked && rest.length ? nowLine() : "") : `<div class="empty">해당하는 예약이 없습니다.</div>`}
      </section>`;
  }
  function card(r){
    const B = (a, label, cls) => `<button class="btn sm ${cls || ""}" data-a="st" data-id="${esc(r.id)}" data-v="${a}">${label}</button>`;
    /* 오늘 확정 예약이 시간이 지났는데 아직 안 왔으면 '늦음' — 자리를 잡아 두는 시간(lateMin)을 넘기면 더 눈에 띄게 */
    const late = r.status === "ok" && r.date === ZB.today() ? nowMin() - ZB.mins(r.time) : -1;
    const lateChip = late > 0 ? `<span class="chip ${late > ZB.cfg.lateMin ? "noshow" : "req"}">${late}분 늦음${late > ZB.cfg.lateMin ? " · 잡아 둔 " + ZB.cfg.lateMin + "분 지남" : ""}</span>` : "";
    const ns = ZB.noshowCount(r.phone), nsChip = ns ? `<span class="chip ${ns >= ZB.cfg.noshowLimit ? "noshow" : "src"}">노쇼 ${ns}회${ns >= ZB.cfg.noshowLimit ? " · 홈페이지 예약 제한" : ""}</span>` : "";
    const waited = r.waitNo ? `<span class="chip ok">웨이팅 ${r.waitNo}번 · 맨 앞</span>` : "";
    const acts = r.status === "req" ? B("ok", "확정", "ok") + B("cancel", "거절", "no")
               : r.status === "ok" ? B("in", "방문", "in") + B("noshow", "노쇼", "no") + B("cancel", "취소")
                   + (r.date === ZB.today() && !r.waitNo ? `<button class="btn sm ghost" data-a="r-wait" data-id="${esc(r.id)}" title="예약 손님이 왔는데 자리가 없을 때">자리 없음 → 웨이팅 맨 앞</button>` : "")
               : B("ok", "되돌리기", "ghost");   /* 끝난 예약 — 되돌리기는 드물게 쓰니 눈에 덜 띄게 */
    return `<article class="res ${r.status}">
        <div class="time"><b class="num">${esc(r.time)}</b><span>${hm(r.time).slice(0, 2)}</span></div>
        <div class="who">
          <div class="l1"><b>${esc(r.name)}</b><span class="ppl num">${r.people}명</span><span class="chip ${r.status}">${STATUS[r.status]}</span><span class="chip src">${esc(r.src || "")}</span>${lateChip}${waited}${nsChip}</div>
          <div class="l2 num">${esc(r.phone)} · 테이블 ${ZB.tablesFor(r.people)}개${r.status === "req" && r.people >= ZB.cfg.groupConfirm ? ` · ${ZB.cfg.groupConfirm}명 이상 단체라 확인 후 확정` : ""}</div>
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

  /* ---------- 웨이팅 탭 ----------
     왼쪽: 지금 기다리는 팀(번호 순). 오른쪽: 판단에 필요한 것 — 곧 오는 예약, 오늘 지나간 팀.
     흐름은 한 줄: 대기 → 호출(입장 안내를 보냄) → 입장 / 미방문. 어느 테이블인지는 여기서도 정하지 않습니다. */
  function waitTab(){
    const w = ZB.wait, now = Date.now(), live = ZB.waitLive(), c = ZB.cfg;
    const done = w.list.filter(x => x.status === "in" || x.status === "gone" || x.status === "cancel").sort((a, b) => (b.doneAt || 0) - (a.doneAt || 0));
    const ago = t => Math.max(0, Math.round((now - t) / 60000));
    const sum = a => a.reduce((n, r) => n + r.people, 0), cnt = s => done.filter(x => x.status === s).length;
    const rg = ZB.waitRange(live.length), pace = ZB.waitPace(), close = ZB.waitClose();
    const B = (x, a, label, cls) => `<button class="btn sm ${cls || ""}" data-a="w-st" data-id="${esc(x.id)}" data-v="${a}">${label}</button>`;
    /* 호출하고 callWaitMin 분이 지나도 안 오면 '넘기기' 를 권함(막지는 않음) */
    const row = (x, i) => { const over = x.status === "call" && ago(x.callAt) >= c.callWaitMin;
      return `<article class="wt ${x.status}${over ? " over" : ""}">
        <div class="no"><b class="num">${x.no}</b><span>번</span></div>
        <div class="who">
          <div class="l1"><b class="num">${x.people}명</b>${x.status === "call" ? `<span class="chip ${over ? "noshow" : "req"}">호출함 · ${ago(x.callAt)}분 전${over ? " · " + c.callWaitMin + "분 지남" : ""}</span>` : `<span class="chip ok">${i === 0 ? "다음 순서" : "앞에 " + i + "팀"}</span>`}${x.notifyFail ? `<span class="chip noshow" title="카카오톡을 안 쓰거나 알림을 차단한 손님">알림 못 감 · 직접 불러 주세요</span>` : ""}${x.first ? `<span class="chip in">예약 손님 · 맨 앞</span>` : ""}<span class="chip src">${esc(x.src)}</span></div>
          <div class="l2 num">${esc(x.phone || "전화번호 없음")} · 기다린 지 ${ago(x.at)}분${over ? " · 오지 않으면 미방문으로 넘기고 다음 팀을 부르세요" : ""}</div>
        </div>
        <div class="acts">${x.status === "call" ? B(x, "in", "입장", "in") + B(x, "call", "다시 호출") + B(x, "gone", over ? "넘기기 (미방문)" : "미방문", "no") : B(x, "call", "호출", "ok") + B(x, "in", "입장") + B(x, "cancel", "취소", "no")}</div>
      </article>`; };
    const DONE = { in: "입장", gone: "미방문", cancel: "취소" }, CH = { in: "in", gone: "noshow", cancel: "cancel" };
    const old = x => `<div class="wdone"><b class="num">${x.no}번</b><span class="num">${x.people}명</span><span class="chip ${CH[x.status]}">${DONE[x.status]}</span><button class="btn sm ghost" data-a="w-st" data-id="${esc(x.id)}" data-v="wait">되돌리기</button></div>`;
    /* 곧 오는 예약 — 빈자리가 나도 예약 손님 몫을 남겨야 하니, 호출하기 전에 같이 봅니다 */
    const d = new Date(), nowM = d.getHours() * 60 + d.getMinutes(), td = ZB.today();
    const soonRes = ZB.byDate(td).filter(r => (r.status === "ok" || r.status === "req") && ZB.mins(r.time) >= nowM - 15 && ZB.mins(r.time) <= nowM + 60);
    return `<div class="datebar wbar">
        <h2>오늘 웨이팅</h2>
        <button class="sw${w.on ? " on" : ""}" data-a="w-on" role="switch" aria-checked="${w.on}"><i></i>${w.on ? "접수 받는 중" : "접수 멈춤"}</button>
        <span class="chip ${close.closed ? "noshow" : "src"}">${close.closed ? "접수 마감 시간 지남 (" + close.at + ")" : close.at + " 접수 마감"}</span>
        <div class="r"><a class="btn" href="../waiting/" target="_blank" rel="noopener">입구 접수 화면</a><a class="btn" href="../tv/" target="_blank" rel="noopener">매장 TV 화면</a><button class="btn pri" data-a="w-new">+ 직접 등록</button></div>
      </div>
      <div class="kpis">
        <div class="kpi${live.length ? " req" : ""}"><span>지금 대기</span><b class="num">${live.length}팀<small>${sum(live)}명</small></b></div>
        <div class="kpi"><span>지금 오면 예상 대기<em>${esc(pace.basis)} · 한 팀 ${pace.per}분</em></span><b class="num">${rg ? rg.lo + "~" + rg.hi + "분" : "바로 입장"}</b></div>
        <div class="kpi"><span>오늘 입장</span><b class="num">${cnt("in")}팀<small>${sum(done.filter(x => x.status === "in"))}명</small></b></div>
        <div class="kpi"><span>미방문 · 취소</span><b class="num">${cnt("gone")} · ${cnt("cancel")}</b></div>
      </div>
      <div class="cols w">
        <section class="panel">
          <header><div><h3>기다리는 팀</h3><p>번호 순서입니다. 호출하면 손님 휴대폰으로 입장 안내가 갑니다.</p></div></header>
          ${live.length ? live.map(row).join("") : `<div class="empty">기다리는 팀이 없습니다.${w.on ? "" : "<br>접수가 멈춰 있어 손님용 화면에서 새로 받지 않습니다."}</div>`}
        </section>
        <div class="side">
          <section class="panel">
            <header><div><h3>곧 오는 예약</h3><p>1시간 안 · 지금 예약으로 잡힌 테이블 ${ZB.usedAt(td, nowM)} / ${c.tables}개</p></div></header>
            ${soonRes.length ? soonRes.map(r => `<div class="wdone"><b class="num">${esc(r.time)}</b><span>${esc(r.name)} · ${r.people}명</span><span class="chip src">테이블 ${ZB.tablesFor(r.people)}개</span></div>`).join("") : `<div class="empty sm">1시간 안에 오는 예약이 없습니다.</div>`}
          </section>
          <section class="panel">
            <header><div><h3>오늘 지나간 팀</h3><p>${done.length}팀</p></div></header>
            ${done.length ? done.map(old).join("") : `<div class="empty sm">아직 없습니다.</div>`}
          </section>
        </div>
      </div>`;
  }
  /* 직접 등록 — 화면을 못 쓰시는 손님, 전화번호 없이 기다리는 손님 */
  function sheetWait(){
    const f = form, n = ZB.waitLive().length;
    return `<div class="ov" data-a="close-ov"><div class="sheet" role="dialog" aria-modal="true" aria-label="웨이팅 직접 등록">
        <header><h3>웨이팅 직접 등록</h3><button class="btn sm ghost" data-a="close">닫기</button></header>
        <div class="body">
          <div class="fld"><span>인원</span>
            <div class="step"><button data-a="f-ppl" data-v="-1" aria-label="한 명 줄이기">−</button><b class="num">${f.people}</b><button data-a="f-ppl" data-v="1" aria-label="한 명 늘리기">+</button><span>명</span></div></div>
          <div class="fld"><label for="f-phone">전화번호<em>없어도 됩니다 — 없으면 번호를 직접 불러 주세요</em></label><input id="f-phone" data-f="phone" value="${esc(f.phone)}" inputmode="numeric" autocomplete="off" placeholder="010-0000-0000"></div>
          <p class="hint">지금 ${n}팀이 기다리고 있어 예상 대기는 ${n ? ZB.waitRange(n).lo + "~" + ZB.waitRange(n).hi + "분" : "없음(바로 입장)"}입니다.${f.people >= ZB.cfg.bigTeam ? ` ${ZB.cfg.bigTeam}명 이상은 입구 기기에서 받지 않는 인원입니다. 직원 판단으로 등록할 수 있습니다.` : ""}</p>
        </div>
        <footer><button class="btn" data-a="close">취소</button><button class="btn pri" data-a="w-save">등록</button></footer>
      </div></div>`;
  }

  /* ---------- 선결제 장부 탭 ----------
     왼쪽: 장부 목록(최근에 쓴 순). 오른쪽: 고른 장부의 잔액과 기록.
     직원이 하는 일은 둘뿐 — '사용'(먹은 만큼 빼기)과 '충전'. 잘못 넣으면 그 줄을 '취소'(지우지 않음). */
  const won = n => (n < 0 ? "−" : "") + Math.abs(n).toLocaleString("ko-KR") + "원";
  const md = t => { const d = new Date(t); return (d.getMonth() + 1) + "/" + d.getDate() + " " + String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0"); };
  function acctRows(){
    const L = ZB.ledger, low = ZB.cfg.lowBalance, q = (view.q || "").trim();
    const last = id => { const a = ZB.acctTx(id); return a.length ? a[a.length - 1].at : 0; };
    const list = L.accts.filter(a => !q || (a.name + a.contact + a.phone).indexOf(q) >= 0).sort((x, y) => last(y.id) - last(x.id));
    if(!list.length) return `<div class="empty sm">찾는 장부가 없습니다.</div>`;
    return list.map(a => { const b = ZB.bal(a.id), cls = b < 0 ? "neg" : b < low ? "low" : "";
      return `<button class="acct${view.acct === a.id ? " on" : ""}" data-a="acct" data-v="${esc(a.id)}">
          <span class="nm"><b>${esc(a.name)}</b><small>${esc(a.kind)}${a.contact ? " · " + esc(a.contact) : ""} · 최근 ${last(a.id) ? md(last(a.id)).split(" ")[0] : "-"}</small></span>
          <span class="bl num ${cls}">${won(b)}${cls ? `<small>${b < 0 ? "모자람" : "충전 안내"}</small>` : ""}</span>
        </button>`; }).join("");
  }
  function ledgerTab(){
    const L = ZB.ledger, low = ZB.cfg.lowBalance;
    if(!view.acct || !L.accts.some(a => a.id === view.acct)){ const t = L.tx.filter(x => !x.void).sort((a, b) => b.at - a.at)[0]; view.acct = t ? t.acct : (L.accts[0] || {}).id; }
    const d = new Date(), m0 = new Date(d.getFullYear(), d.getMonth(), 1).getTime();
    const live = L.tx.filter(t => !t.void), month = live.filter(t => t.at >= m0);
    const sumT = (arr, type) => arr.filter(t => t.type === type).reduce((s, t) => s + t.amount, 0);
    const bals = L.accts.map(a => ZB.bal(a.id)), owed = bals.reduce((s, b) => s + Math.max(0, b), 0), lowN = bals.filter(b => b < low).length;
    const a = L.accts.filter(x => x.id === view.acct)[0];
    return `<div class="kpis">
        <div class="kpi"><span>남은 선결제 합계<em>손님이 맡겨 둔 돈</em></span><b class="num">${won(owed)}</b></div>
        <div class="kpi"><span>이번 달 충전</span><b class="num">${won(sumT(month, "charge"))}</b></div>
        <div class="kpi"><span>이번 달 사용</span><b class="num">${won(sumT(month, "use"))}</b></div>
        <div class="kpi${lowN ? " req" : ""}"><span>잔액 부족</span><b class="num">${lowN}곳<small>${won(low)} 아래</small></b></div>
      </div>
      <div class="cols l">
        <section class="panel">
          <header><div><h3>장부 ${L.accts.length}권</h3></div><button class="btn pri sm" data-a="l-new">+ 새 장부</button></header>
          <div class="search"><input data-q="1" value="${esc(view.q || "")}" placeholder="이름 · 담당자 · 전화번호로 찾기" autocomplete="off" aria-label="장부 찾기"></div>
          <div id="acct-list">${acctRows()}</div>
        </section>
        ${a ? acctPanel(a) : `<section class="panel"><div class="empty">장부를 골라 주세요.</div></section>`}
      </div>`;
  }
  function acctPanel(a){
    const b = ZB.bal(a.id), low = ZB.cfg.lowBalance; let run = 0;
    const rows = ZB.acctTx(a.id).map(t => { if(!t.void) run += t.type === "charge" ? t.amount : -t.amount;
      return `<div class="tx ${t.type}${t.void ? " void" : ""}">
          <span class="dt num">${md(t.at)}</span>
          <span class="ty">${t.type === "charge" ? "충전" : "사용"}</span>
          <span class="mm">${esc(t.memo)}${t.by ? `<small>${esc(t.by)}</small>` : ""}${t.void ? `<small>취소한 줄 — 잔액에 넣지 않음</small>` : ""}</span>
          <span class="am num">${t.type === "charge" ? "+" : "−"}${Math.abs(t.amount).toLocaleString("ko-KR")}</span>
          <span class="rn num">${t.void ? "" : won(run)}</span>
          <button class="btn sm ghost" data-a="l-void" data-v="${esc(t.id)}">${t.void ? "되살리기" : "취소"}</button>
        </div>`; }).reverse().join("");
    return `<section class="panel">
        <div class="ahead">
          <div><h3>${esc(a.name)}</h3><p>${esc(a.kind)}${a.contact ? " · " + esc(a.contact) : ""}${a.phone ? " · " + esc(a.phone) : ""}</p>${a.memo ? `<p class="memo">${esc(a.memo)}</p>` : ""}</div>
          <div class="bal${b < 0 ? " neg" : b < low ? " low" : ""}"><span>잔액</span><b class="num">${won(b)}</b>${b < 0 ? `<small>다음 충전에서 정산</small>` : b < low ? `<small>충전을 권해 보세요</small>` : ""}</div>
        </div>
        <div class="abtn"><button class="btn pri" data-a="l-tx" data-v="use">사용 (차감)</button><button class="btn" data-a="l-tx" data-v="charge">충전</button></div>
        <div class="tx th"><span>날짜</span><span>구분</span><span>내용</span><span>금액</span><span>남은 돈</span><span></span></div>
        ${rows || `<div class="empty sm">기록이 없습니다.</div>`}
      </section>`;
  }
  const amt = () => Number(String(form.amount || "").replace(/\D/g, "")) || 0;
  function txPreview(){
    const a = form.acct, b = ZB.bal(a), n = amt(), after = form.type === "charge" ? b + n : b - n;
    const lim = ZB.cfg.ledgerCredit;
    return `지금 ${won(b)} → ${form.type === "charge" ? "충전" : "사용"} 후 <b>${won(after)}</b>` + (form.type === "use" && after < 0
      ? (after < -lim ? `<em>${lim ? "마이너스 한도(" + won(lim) + ")를 넘습니다" : "이 가게는 마이너스를 쓰지 않기로 했습니다"}. 그래도 뺄 수 있지만 담당자와 확인해 주세요.</em>`
                      : `<em>잔액보다 많습니다. 마이너스 한도 ${won(lim)} 안이라 모자란 만큼 다음 충전에서 정산합니다.</em>`) : "");
  }
  function sheetTx(){
    const f = form, a = ZB.ledger.accts.filter(x => x.id === f.acct)[0], use = f.type === "use";
    const presets = use ? [] : [300000, 500000, 1000000];
    return `<div class="ov" data-a="close-ov"><div class="sheet" role="dialog" aria-modal="true" aria-label="${use ? "사용" : "충전"}">
        <header><h3>${use ? "사용 (차감)" : "충전"} · ${esc(a.name)}</h3><button class="btn sm ghost" data-a="close">닫기</button></header>
        <div class="body">
          <div class="fld"><label for="f-amount">금액<em>${use ? "계산서 금액 그대로" : "받은 금액"}</em></label><input id="f-amount" data-f="amount" value="${esc(f.amount)}" inputmode="numeric" autocomplete="off" placeholder="0">
            ${presets.length ? `<div class="presets">${presets.map(p => `<button class="btn sm" data-a="l-preset" data-v="${p}">${p / 10000}만원</button>`).join("")}</div>` : ""}</div>
          <div class="two">
            <div class="fld"><label for="f-memo">내용<em>${use ? "인원 · 모임" : "현금 · 카드 · 이체"}</em></label><input id="f-memo" data-f="memo" value="${esc(f.memo)}" autocomplete="off"></div>
            <div class="fld"><label for="f-by">${use ? "드신 분" : "맡긴 분"}<em>선택</em></label><input id="f-by" data-f="by" value="${esc(f.by)}" autocomplete="off" placeholder="${esc(a.contact || "")}"></div>
          </div>
          <p class="pv" id="lx-pv">${txPreview()}</p>
        </div>
        <footer><button class="btn" data-a="close">취소</button><button class="btn pri" data-a="l-save"${amt() > 0 ? "" : " disabled"}>${use ? "빼기" : "충전하기"}</button></footer>
      </div></div>`;
  }
  function sheetAcct(){
    const f = form;
    return `<div class="ov" data-a="close-ov"><div class="sheet" role="dialog" aria-modal="true" aria-label="새 장부">
        <header><h3>새 장부</h3><button class="btn sm ghost" data-a="close">닫기</button></header>
        <div class="body">
          <div class="fld"><span>구분</span><div class="seg">${["회사", "개인"].map(k => `<button data-a="la-kind" data-v="${k}" class="${f.kind === k ? "on" : ""}">${k}</button>`).join("")}</div></div>
          <div class="fld"><label for="f-name">${f.kind === "회사" ? "회사·모임 이름" : "성함"}</label><input id="f-name" data-f="name" value="${esc(f.name)}" autocomplete="off"></div>
          <div class="two">
            <div class="fld"><label for="f-contact">담당자<em>선택</em></label><input id="f-contact" data-f="contact" value="${esc(f.contact)}" autocomplete="off"></div>
            <div class="fld"><label for="f-phone">전화번호<em>사용 내역 알림톡을 받을 번호</em></label><input id="f-phone" data-f="phone" value="${esc(f.phone)}" inputmode="numeric" autocomplete="off" placeholder="010-0000-0000"></div>
          </div>
          <div class="fld"><label for="f-amount">처음 맡기는 금액<em>나중에 충전해도 됩니다</em></label><input id="f-amount" data-f="amount" value="${esc(f.amount)}" inputmode="numeric" autocomplete="off" placeholder="0"></div>
          <div class="fld"><label for="f-memo">메모<em>선택</em></label><input id="f-memo" data-f="memo" value="${esc(f.memo)}" autocomplete="off"></div>
        </div>
        <footer><button class="btn" data-a="close">취소</button><button class="btn pri" data-a="la-save"${f.name.trim() ? "" : " disabled"}>만들기</button></footer>
      </div></div>`;
  }

  /* ---------- 포인트 탭 ----------
     계산대에서 하는 일은 '적립' 하나가 거의 전부 — 결제 금액과 손님 번호를 넣으면 끝.
     왼쪽: 회원(최근 방문 순, 뒷번호 4자리로 찾기). 오른쪽: 고른 회원의 포인트와 기록. 화면 구성은 선결제 장부와 같게 맞춤. */
  const pt = n => n.toLocaleString("ko-KR") + "P";
  const digits = s => String(s || "").replace(/\D/g, "");
  function memRows(){
    const P = ZB.points, q = digits(view.pq), nm = (view.pq || "").trim();
    const last = id => { const a = ZB.memTx(id); return a.length ? a[a.length - 1].at : 0; };
    const list = P.members.filter(m => !nm || (q && digits(m.phone).indexOf(q) >= 0) || (m.name && m.name.indexOf(nm) >= 0)).sort((x, y) => last(y.id) - last(x.id));
    if(!list.length) return `<div class="empty sm">찾는 회원이 없습니다.</div>`;
    return list.map(m => { const s = ZB.pstate(m.id), can = s.usable >= ZB.cfg.pointMin;
      return `<button class="acct${view.mem === m.id ? " on" : ""}" data-a="mem" data-v="${esc(m.id)}">
          <span class="nm"><b class="num">${esc(m.phone)}</b><small>${m.name ? esc(m.name) + " · " : ""}최근 ${last(m.id) ? md(last(m.id)).split(" ")[0] : "-"}</small></span>
          <span class="bl num">${pt(s.total)}${can ? `<small class="ok-t">사용 가능</small>` : s.today ? `<small class="sub-t">오늘 적립분 내일부터</small>` : ""}</span>
        </button>`; }).join("");
  }
  function pointTab(){
    const P = ZB.points, c = ZB.cfg;
    if(!view.mem || !P.members.some(m => m.id === view.mem)){ const t = P.tx.filter(x => !x.void).sort((a, b) => b.at - a.at)[0]; view.mem = t ? t.mem : (P.members[0] || {}).id; }
    const d = new Date(), m0 = new Date(d.getFullYear(), d.getMonth(), 1).getTime();
    const live = P.tx.filter(t => !t.void), month = live.filter(t => t.at >= m0);
    const sumT = (arr, type) => arr.filter(t => t.type === type).reduce((s, t) => s + t.pts, 0);
    const left = P.members.reduce((s, m) => s + ZB.pbal(m.id), 0);
    const newM = P.members.filter(m => { const a = ZB.memTx(m.id); return a.length && a[0].at >= m0; }).length;
    const m = P.members.filter(x => x.id === view.mem)[0], pend = ZB.pending;
    return `<div class="datebar wbar">
        <h2>포인트</h2><p class="rate">결제 금액의 <b>${c.pointRate}%</b> 적립 · ${pt(c.pointMin)}부터 사용 · 유효기간 ${Math.round(c.pointExpireDays / 30.4)}개월${c.pointNextDay ? " · 다음 날부터 사용" : ""}</p>
        <div class="r"><a class="btn" href="../points/" target="_blank" rel="noopener">계산대 화면 열기</a><button class="btn pri big" data-a="p-earn">+ 적립</button></div>
      </div>
      ${pend ? `<div class="pend"><span><b>계산대 화면</b> 결제 ${won(pend.amount)} · 손님이 번호를 누르기를 기다리는 중 (${Math.max(0, Math.round((Date.now() - pend.at) / 60000))}분 전)</span><button class="btn sm" data-a="p-pend-off">거두기</button></div>` : ""}
      <div class="kpis">
        <div class="kpi"><span>회원</span><b class="num">${P.members.length}명<small>이번 달 새로 ${newM}명</small></b></div>
        <div class="kpi"><span>이번 달 적립</span><b class="num">${pt(sumT(month, "earn"))}</b></div>
        <div class="kpi"><span>이번 달 사용</span><b class="num">${pt(sumT(month, "use"))}</b></div>
        <div class="kpi"><span>쌓여 있는 포인트<em>앞으로 할인해 줄 몫</em></span><b class="num">${pt(left)}</b></div>
      </div>
      <div class="cols l">
        <section class="panel">
          <header><div><h3>회원 ${P.members.length}명</h3><p>휴대폰 번호가 곧 회원 — 따로 가입하지 않습니다</p></div></header>
          <div class="search"><input data-q="p" value="${esc(view.pq || "")}" inputmode="numeric" placeholder="뒷번호 4자리 또는 이름" autocomplete="off" aria-label="회원 찾기"></div>
          <div id="mem-list">${memRows()}</div>
        </section>
        ${m ? memPanel(m) : `<section class="panel"><div class="empty">회원을 골라 주세요.</div></section>`}
      </div>`;
  }
  function memPanel(m){
    const s = ZB.pstate(m.id), all = ZB.memTx(m.id), live = all.filter(t => !t.void), c = ZB.cfg, min = c.pointMin; let run = 0;
    const visits = live.filter(t => t.type === "earn"), spent = visits.reduce((x, t) => x + t.amount, 0);
    const SRC = { "계산대": "계산대", "직원 입력": "직원 입력" };
    const rows = all.map(t => { if(!t.void) run += t.type === "earn" ? t.pts : -t.pts;
      return `<div class="tx ${t.type === "earn" ? "charge" : "use"}${t.void ? " void" : ""}">
          <span class="dt num">${md(t.at)}</span>
          <span class="ty">${t.type === "earn" ? "적립" : "사용"}</span>
          <span class="mm">${t.type === "earn" ? "결제 " + won(t.amount) + (t.src ? `<small>${esc(SRC[t.src] || t.src)}</small>` : "") : "계산에서 할인" + (t.how ? `<small>확인: ${esc(t.how)}</small>` : "")}${t.void ? `<small>취소한 줄 — 포인트에 넣지 않음</small>` : ""}</span>
          <span class="am num">${t.type === "earn" ? "+" : "−"}${t.pts.toLocaleString("ko-KR")}</span>
          <span class="rn num">${t.void ? "" : pt(run)}</span>
          <button class="btn sm ghost" data-a="p-void" data-v="${esc(t.id)}">${t.void ? "되살리기" : "취소"}</button>
        </div>`; }).reverse().join("");
    const notes = [];
    if(s.today) notes.push(`오늘 적립 ${pt(s.today)}는 내일부터 쓸 수 있습니다`);
    if(s.soon) notes.push(`${pt(s.soon)}가 30일 안에 사라집니다`);
    if(s.expired) notes.push(`유효기간(${Math.round(c.pointExpireDays / 30)}개월)이 지나 사라진 포인트 ${pt(s.expired)}`);
    return `<section class="panel">
        <div class="ahead">
          <div><h3 class="num">${esc(m.phone)}</h3><p>${m.name ? "<b>" + esc(m.name) + "</b> · " : "<b>이름 없음</b> · "}방문 ${visits.length}번 · 누적 결제 ${won(spent)}</p>${all.length ? `<p>처음 적립 ${md(all[0].at).split(" ")[0]}</p>` : ""}</div>
          <div class="bal"><span>포인트</span><b class="num">${pt(s.total)}</b>${s.usable >= min ? `<small class="ok-t">지금 ${won(s.usable)} 할인 가능</small>` : `<small class="sub-t">${s.usable > 0 ? "지금 쓸 수 있는 " + pt(s.usable) + " · " : ""}${pt(min)}부터 사용</small>`}</div>
        </div>
        ${notes.length ? `<p class="pnote">${notes.map(esc).join(" · ")}</p>` : ""}
        <div class="abtn"><button class="btn pri" data-a="p-earn" data-v="${esc(m.phone)}">적립</button><button class="btn" data-a="p-use"${s.usable > 0 ? "" : " disabled"}>포인트 사용</button></div>
        <div class="tx th"><span>날짜</span><span>구분</span><span>내용</span><span>포인트</span><span>남은 포인트</span><span></span></div>
        ${rows || `<div class="empty sm">기록이 없습니다.</div>`}
      </section>`;
  }
  /* 적립 창 — 번호를 치는 동안 '기존 회원 / 새 회원(이름 받기)' 과 '오늘 이미 적립' 이 바로 보임 */
  const earnMember = () => { const ph = digits(form.phone); return ph.length === 11 ? ZB.memberByPhone(ph) : null; };
  function earnPreview(){
    const f = form, ph = digits(f.phone), amount = Number(digits(f.amount)) || 0, get = Math.floor(amount * ZB.cfg.pointRate / 100);
    const m = earnMember();
    const who = ph.length < 11 ? `휴대폰 번호 11자리를 넣어 주세요` : m ? `기존 회원${m.name ? " " + esc(m.name) : ""} · 지금 ${pt(ZB.pbal(m.id))}` : `처음 오신 손님 — 이름(또는 성·별명)을 받아 두면 쓸 때 확인합니다`;
    const dup = m ? ZB.earnedToday(m.id) : [];
    return `<span>${who}</span>` + (amount ? `<b>${won(amount)} × ${ZB.cfg.pointRate}% = ${pt(get)} 적립</b>` : "")
      + (dup.length ? `<em>오늘 이미 ${dup.length}번 적립했습니다 (${dup.map(t => md(t.at).split(" ")[1] + " " + won(t.amount)).join(", ")}). 다른 계산이 맞는지 확인해 주세요 — 막지는 않습니다.</em>` : "");
  }
  /* 처음 오신 손님은 직원이 말로 동의를 받고 체크해야 적립됨(필수) · 홍보 소식은 선택 */
  const earnOk = () => digits(form.phone).length === 11 && /^010/.test(digits(form.phone)) && Number(digits(form.amount)) > 0 && (earnMember() || form.agree);
  const agreeBox = () => `<div class="fld"><button type="button" class="chk${form.agree ? " on" : ""}" data-a="pe-ag" role="checkbox" aria-checked="${!!form.agree}"><i></i><span><b>[필수]</b> 손님께 개인정보 수집·이용 동의를 받았습니다<em>휴대폰 번호·이름 · 포인트 적립·사용·내역 알림 · 마지막 이용 후 3년 보관</em></span></button>
      <button type="button" class="chk${form.mkt ? " on" : ""}" data-a="pe-mk" role="checkbox" aria-checked="${!!form.mkt}"><i></i><span><b>[선택]</b> 할인·행사 소식 받기에 동의하셨습니다<em>묻고 원하실 때만 체크</em></span></button></div>`;
  function sheetEarn(){
    const f = form, ph = digits(f.phone), isNew = ph.length === 11 && !earnMember();
    return `<div class="ov" data-a="close-ov"><div class="sheet" role="dialog" aria-modal="true" aria-label="포인트 적립">
        <header><h3>포인트 적립</h3><button class="btn sm ghost" data-a="close">닫기</button></header>
        <div class="body">
          <div class="fld"><label for="f-amount">결제 금액<em>포인트로 낸 금액은 빼고 · 계산서 금액 그대로</em></label><input id="f-amount" data-f="amount" value="${esc(f.amount)}" inputmode="numeric" autocomplete="off" placeholder="0"></div>
          <div class="fld"><label for="f-phone">손님 휴대폰 번호<em>또는 아래 '계산대 화면으로' — 손님이 직접 누름</em></label><input id="f-phone" data-f="phone" value="${esc(f.phone)}" inputmode="numeric" autocomplete="off" placeholder="010-0000-0000"></div>
          <div class="fld" id="pe-name"${isNew ? "" : " hidden"}><label for="f-name">이름<em>성이나 별명도 됩니다 · 포인트를 쓸 때 확인용</em></label><input id="f-name" data-f="name" value="${esc(f.name || "")}" autocomplete="off"></div>
          <div id="pe-agree"${isNew ? "" : " hidden"}>${agreeBox()}</div>
          <p class="pv" id="pe-pv">${earnPreview()}</p>
        </div>
        <footer><button class="btn" data-a="close">취소</button>
          <button class="btn" data-a="pe-send"${Number(digits(f.amount)) > 0 ? "" : " disabled"}>계산대 화면으로</button>
          <button class="btn pri" data-a="pe-save"${earnOk() ? "" : " disabled"}>적립</button></footer>
      </div></div>`;
  }
  /* 사용 창 — 본인 확인(설정: 이름+번호 / 인증번호)을 거쳐야 '사용' 이 켜짐. 확인 방법은 기록에 남음 */
  const norm = s => String(s || "").replace(/\s/g, "");
  function authState(){
    const m = ZB.points.members.filter(x => x.id === form.mem)[0], how = ZB.cfg.pointAuth;
    if(form.manual) return { ok: true, how: "직원이 직접 확인", msg: "직원이 직접 확인했습니다" };
    if(how === "code"){
      if(!form.code) return { ok: false, msg: "손님 휴대폰으로 인증번호를 보내 주세요" };
      return norm(form.codeIn) === form.code ? { ok: true, how: "인증번호", msg: "인증번호가 맞습니다" } : { ok: false, msg: form.codeIn ? "인증번호가 다릅니다" : "손님이 불러 주는 인증번호를 넣어 주세요" };
    }
    if(!m.name) return { ok: false, msg: "등록된 이름이 없습니다 — 손님께 여쭤 직접 확인해 주세요" };
    const said = norm(form.said), name = norm(m.name);
    if(!said) return { ok: false, msg: "손님께 이름을 여쭤 넣어 주세요 (전화번호는 이미 확인)" };
    return said === name || (name.length === 1 && said[0] === name) || (said.length >= 1 && said[0] === name[0] && said.length >= name.length && said.indexOf(name) === 0)
      ? { ok: true, how: "이름+번호", msg: "이름이 맞습니다" } : { ok: false, msg: "등록된 이름과 다릅니다" };
  }
  function sheetUse(){
    const m = ZB.points.members.filter(x => x.id === form.mem)[0], s = ZB.pstate(m.id), n = Number(digits(form.pts)) || 0, code = ZB.cfg.pointAuth === "code", au = authState();
    return `<div class="ov" data-a="close-ov"><div class="sheet" role="dialog" aria-modal="true" aria-label="포인트 사용">
        <header><h3>포인트 사용 · ${esc(m.phone)}</h3><button class="btn sm ghost" data-a="close">닫기</button></header>
        <div class="body">
          <div class="fld"><span>본인 확인<em>${code ? "휴대폰 인증번호" : "이름 + 전화번호"}</em></span>
            ${code ? `<div class="two"><button class="btn" data-a="pu-code">${form.code ? "인증번호 다시 보내기" : "인증번호 보내기"}</button><input data-f="codeIn" value="${esc(form.codeIn || "")}" inputmode="numeric" autocomplete="off" placeholder="손님이 불러 주는 4자리" aria-label="인증번호"></div>`
                   : `<input data-f="said" value="${esc(form.said || "")}" autocomplete="off" placeholder="손님이 말한 이름" aria-label="손님이 말한 이름">`}
            <p class="auth ${au.ok ? "ok" : ""}" id="pu-auth">${esc(au.msg)}</p>
            ${au.ok ? "" : `<button class="btn sm ghost" data-a="pu-manual">직원이 직접 확인함</button>`}</div>
          <div class="fld"><label for="f-pts">쓸 포인트<em>지금 쓸 수 있는 ${pt(s.usable)}${s.today ? " (오늘 적립 " + pt(s.today) + "은 내일부터)" : ""} · 1포인트 = 1원</em></label><input id="f-pts" data-f="pts" value="${esc(form.pts)}" inputmode="numeric" autocomplete="off">
            <div class="presets"><button class="btn sm" data-a="pu-all">모두 쓰기</button></div></div>
          <p class="pv" id="pu-pv">${puPreview()}</p>
        </div>
        <footer><button class="btn" data-a="close">취소</button><button class="btn pri" data-a="pu-save"${puOk() ? "" : " disabled"}>사용</button></footer>
      </div></div>`;
  }
  const puOk = () => { const n = Number(digits(form.pts)) || 0; return n > 0 && n <= ZB.pstate(form.mem).usable && authState().ok; };
  function puPreview(){
    const s = ZB.pstate(form.mem), min = ZB.cfg.pointMin, n = Number(digits(form.pts)) || 0;
    if(n > s.usable) return `<em>지금 쓸 수 있는 포인트(${pt(s.usable)})보다 많습니다.</em>`;
    return `계산에서 <b>${won(n)}</b> 할인 · 남는 포인트 ${pt(s.total - n)}` + (s.usable < min ? `<em>${pt(min)}부터 쓰는 규칙이지만 막지는 않습니다. 사장님 판단으로 쓰세요.</em>` : "");
  }

  /* ---------- 설정 — 확인표 답 = 설정값 ----------
     사장님 확인표 답이 오면 여기서 값만 바꿉니다. 숫자는 −/+, 고르는 것은 단추. 바꾼 것은 기록 탭에 남습니다. */
  const CFG_STEP = {   /* 키: [한 번에, 최소, 최대] */
    tables: [1, 1, 80], onlineTables: [1, 0, 80], seats: [1, 2, 8], dwellLunch: [10, 40, 180], dwellDinner: [10, 60, 240],
    groupConfirm: [1, 2, 30], lateMin: [5, 0, 60], noshowLimit: [1, 1, 10],
    waitMin: [1, 2, 30], callWaitMin: [1, 3, 30], bigTeam: [1, 3, 20], waitCloseBefore: [10, 0, 120],
    lowBalance: [10000, 0, 500000], ledgerCredit: [50000, 0, 2000000],
    pointRate: [1, 1, 10], pointMin: [1000, 0, 20000], pointExpireDays: [30, 30, 1095]
  };
  function sheetCfg(){
    const c = ZB.cfg;
    const row = (k, title, note, val, unit) => `<div class="row"><div class="lbl"><b>${title}</b><span>${note}</span></div>
        <div class="step"><button data-a="c" data-k="${k}" data-v="-1" aria-label="${title} 줄이기">−</button><b class="num">${val}</b><button data-a="c" data-k="${k}" data-v="1" aria-label="${title} 늘리기">+</button><span>${unit}</span></div></div>`;
    const pickRow = (k, title, note, opts) => `<div class="row"><div class="lbl"><b>${title}</b><span>${note}</span></div>
        <div class="seg">${opts.map(([v, l]) => `<button data-a="cs" data-k="${k}" data-v="${esc(String(v))}" class="${String(c[k]) === String(v) ? "on" : ""}">${l}</button>`).join("")}</div></div>`;
    const H = t => `<h4 class="cfg-h">${t}</h4>`;
    const man = n => n >= 10000 ? (n / 10000) + "만" : n.toLocaleString("ko-KR");
    return `<div class="ov" data-a="close-ov"><div class="sheet wide" role="dialog" aria-modal="true" aria-label="설정">
        <header><h3>설정</h3><button class="btn sm ghost" data-a="close">닫기</button></header>
        <div class="body">
          <p class="hint top">지금 값은 확인표에서 먼저 제안한 기본값입니다. 사장님 답이 오면 여기서 바꾸면 손님 홈페이지·입구·계산대·TV에 바로 반영됩니다.</p>
          ${H("예약")}
          ${row("tables", "전체 테이블", "매장에 있는 테이블 수", c.tables, "개")}
          ${row("onlineTables", "홈페이지 예약 한도", "이 개수까지만 홈페이지로 받고 나머지는 워크인·전화용", c.onlineTables, "개")}
          ${row("seats", "한 테이블 좌석", "인원을 이 수로 나눠 필요한 테이블을 셉니다", c.seats, "명")}
          ${row("dwellLunch", "평균 이용 시간 · 점심", "제한이 아니라 예약을 잡기 위한 평균 머무는 시간", c.dwellLunch, "분")}
          ${row("dwellDinner", "평균 이용 시간 · 저녁", "저녁은 술을 곁들여 보통 더 깁니다", c.dwellDinner, "분")}
          ${pickRow("maxDays", "홈페이지 예약 기간", "오늘부터 며칠 앞까지 받을지 (마감은 전날)", [[30, "30일"], [60, "60일"], [90, "90일"]])}
          ${row("groupConfirm", "단체 확인 기준", "이 인원 이상 홈페이지 예약은 사장님 확인 후 확정, 그 아래는 바로 확정", c.groupConfirm, "명 이상")}
          ${row("lateMin", "늦을 때 자리 잡아 두기", "예약 시각이 지나고 이 시간까지 기다립니다", c.lateMin, "분")}
          ${row("noshowLimit", "노쇼 제한", "노쇼가 이 횟수가 되면 홈페이지 예약을 막고 전화로 안내", c.noshowLimit, "회")}
          ${H("웨이팅")}
          ${row("callWaitMin", "호출 후 기다리는 시간", "이 시간이 지나도 안 오면 '넘기기' 를 권합니다", c.callWaitMin, "분")}
          ${row("bigTeam", "입구 접수 인원 한도", "이 인원 이상은 입구 기기에서 받지 않고 직원·예약으로 안내", c.bigTeam, "명 이상")}
          ${pickRow("lastOrder", "라스트오더", "웨이팅 접수 마감의 기준", [["20:30", "20:30"], ["21:00", "21:00"], ["21:30", "21:30"], ["22:00", "22:00"]])}
          ${row("waitCloseBefore", "웨이팅 접수 마감", "라스트오더 몇 분 전에 입구 접수를 닫을지", c.waitCloseBefore, "분 전")}
          ${row("waitMin", "한 팀당 시간 (기본값)", "입장 기록이 쌓이기 전에 예상 대기에 쓰는 값. 기록이 3팀 넘으면 실제 간격으로 계산", c.waitMin, "분")}
          ${H("선결제 장부")}
          ${row("lowBalance", "잔액 부족 기준", "잔액이 이 아래면 '충전 안내' 표시", man(c.lowBalance), "원")}
          ${row("ledgerCredit", "마이너스 한도", "잔액보다 더 쓸 수 있는 금액. 0이면 마이너스 안 씀 (막지는 않고 경고)", man(c.ledgerCredit), "원")}
          ${H("포인트")}
          ${row("pointRate", "적립률", "결제 금액(포인트로 낸 금액 제외)의 이만큼", c.pointRate, "%")}
          ${row("pointMin", "사용 시작", "이만큼 모이면 할인으로 쓸 수 있음", c.pointMin.toLocaleString("ko-KR"), "포인트")}
          ${row("pointExpireDays", "유효기간", "적립한 날부터. 기간이 없으면 쌓인 포인트가 가게의 부채로 남습니다", Math.round(c.pointExpireDays / 30.4) + "개월", "")}
          ${pickRow("pointNextDay", "적립한 포인트 사용", "다음 날부터면 그날 밤 마감에서 실수를 바로잡을 수 있습니다", [[true, "다음 날부터"], [false, "바로"]])}
          ${pickRow("pointAuth", "쓸 때 본인 확인", "이름+번호는 손님이 말한 이름을 직원이 확인", [["name", "이름 + 번호"], ["code", "인증번호"]])}
          <p class="hint">어느 테이블에 앉힐지는 정하지 않습니다. 개수만 세기 때문에 좌석 배치도를 그리거나 관리할 필요가 없습니다.</p>
        </div>
        <footer><button class="btn ghost" data-a="reset">자료 처음으로</button><button class="btn pri" data-a="close">확인</button></footer>
      </div></div>`;
  }

  /* ---------- 마감·기록 탭 ----------
     하루 끝에 사장님이 한 번 봅니다: 오늘 적립(같은 번호 여러 번 · 큰 금액 · 직원 입력 표시 — 막지 않고 표시만),
     포스 매출과 적립 대상 금액 비교, 오늘 예약·웨이팅·장부 요약, 그리고 모든 기록(언제·어느 기기·무엇). */
  const KIND = { res: "예약", wait: "웨이팅", ledger: "장부", point: "포인트", cfg: "설정" };
  function closeTab(){
    const t0 = ZB.dayStart(), P = ZB.points, cl = ZB.closing;
    const earns = P.tx.filter(t => t.type === "earn" && t.at >= t0).sort((a, b) => a.at - b.at);
    const uses = P.tx.filter(t => t.type === "use" && t.at >= t0 && !t.void);
    const live = earns.filter(t => !t.void), base = live.reduce((s, t) => s + t.amount, 0), pts = live.reduce((s, t) => s + t.pts, 0);
    const cnt = {}; live.forEach(t => { cnt[t.mem] = (cnt[t.mem] || 0) + 1; });
    const amounts = live.map(t => t.amount).sort((a, b) => a - b), med = amounts.length ? amounts[Math.floor(amounts.length / 2)] : 0;
    const flags = t => { const f = []; if(t.void) return f;
      if(cnt[t.mem] > 1) f.push(["같은 번호 " + cnt[t.mem] + "번", "req"]);
      if(t.amount >= Math.max(300000, med * 3)) f.push(["큰 금액", "noshow"]);
      if(t.src === "직원 입력") f.push(["직원 입력", "src"]);
      return f; };
    const flagged = live.filter(t => flags(t).some(f => f[1] !== "src")).length;
    const mem = id => P.members.filter(m => m.id === id)[0] || {};
    const prow = t => { const m = mem(t.mem);
      return `<div class="tx ${t.void ? "void" : "charge"}">
          <span class="dt num">${md(t.at).split(" ")[1]}</span>
          <span class="ty">${t.src === "직원 입력" ? "직원" : "계산대"}</span>
          <span class="mm"><b class="num">${esc(m.phone || "")}</b>${m.name ? " " + esc(m.name) : ""}<small>${flags(t).map(f => `<span class="chip ${f[1]}">${f[0]}</span>`).join("")}${t.void ? "취소한 줄" : ""}</small></span>
          <span class="am num">${won(t.amount)}</span>
          <span class="rn num">+${t.pts.toLocaleString("ko-KR")}</span>
          <button class="btn sm ghost" data-a="p-void" data-v="${esc(t.id)}">${t.void ? "되살리기" : "취소"}</button>
        </div>`; };
    const pos = cl.pos || 0, ratio = pos ? Math.round(base / pos * 100) : 0;
    /* 오늘 예약·웨이팅·장부 */
    const res = ZB.byDate(ZB.today()), rc = s => res.filter(r => r.status === s).length;
    const wl = ZB.wait.list, wc = s => wl.filter(x => x.status === s).length;
    const waited = wl.filter(x => x.status === "in" && x.doneAt).map(x => (x.doneAt - x.at) / 60000), avgW = waited.length ? Math.round(waited.reduce((a, b) => a + b, 0) / waited.length) : 0;
    const ltx = ZB.ledger.tx.filter(t => t.at >= t0 && !t.void), lsum = ty => ltx.filter(t => t.type === ty).reduce((s, t) => s + t.amount, 0);
    /* 기록 */
    const kf = view.logKind || "all";
    const logs = ZB.log.filter(l => (view.logDay === "all" || l.at >= t0) && (kf === "all" || l.kind === kf)).slice().reverse();
    return `<div class="datebar wbar">
        <h2>오늘 마감</h2><p class="rate">${dateText(ZB.today())} · 실수는 막지 않고 여기서 바로잡습니다</p>
        <div class="r">${cl.done ? `<span class="chip in">마감 확인 ${md(cl.done).split(" ")[1]}</span>` : `<button class="btn pri" data-a="cl-done">마감 확인</button>`}</div>
      </div>
      <div class="kpis">
        <div class="kpi"><span>오늘 적립</span><b class="num">${live.length}건<small>${pt(pts)}</small></b></div>
        <div class="kpi${flagged ? " req" : ""}"><span>살펴볼 적립<em>같은 번호 여러 번 · 큰 금액</em></span><b class="num">${flagged}건</b></div>
        <div class="kpi"><span>오늘 포인트 사용</span><b class="num">${uses.length}건<small>${pt(uses.reduce((s, t) => s + t.pts, 0))}</small></b></div>
        <div class="kpi"><span>적립 대상 / 포스 매출</span><b class="num">${pos ? ratio + "%" : "—"}<small>${won(base)}${pos ? " / " + won(pos) : ""}</small></b></div>
      </div>
      <div class="cols cl">
        <section class="panel">
          <header><div><h3>오늘 포인트 적립 ${earns.length}건</h3><p>표시만 하고 막지 않습니다. 잘못된 줄은 '취소' — 지우지 않고 남습니다.</p></div></header>
          <div class="pos"><label for="cl-pos">오늘 포스 매출</label><input id="cl-pos" data-cl="pos" value="${pos ? pos.toLocaleString("ko-KR") : ""}" inputmode="numeric" placeholder="포스 마감 금액" autocomplete="off"><button class="btn sm" data-a="cl-pos">넣기</button>
            <span>${pos ? (ratio > 100 ? `<b class="neg">적립 대상이 매출보다 많습니다 — 확인 필요</b>` : `매출의 ${ratio}%가 적립 대상`) : "넣으면 적립 대상 금액과 비교합니다"}</span></div>
          <div class="tx th"><span>시각</span><span>입력</span><span>회원</span><span>결제</span><span>적립</span><span></span></div>
          ${earns.length ? earns.slice().reverse().map(prow).join("") : `<div class="empty sm">오늘 적립이 없습니다.</div>`}
        </section>
        <div class="side">
          <section class="panel">
            <header><div><h3>오늘 한눈에</h3></div></header>
            <div class="wdone"><b>예약</b><span>방문 ${rc("in")} · 노쇼 ${rc("noshow")} · 취소 ${rc("cancel")} · 남은 확정 ${rc("ok")}</span></div>
            <div class="wdone"><b>웨이팅</b><span>입장 ${wc("in")} · 미방문 ${wc("gone")} · 취소 ${wc("cancel")}${avgW ? " · 평균 " + avgW + "분 기다림" : ""}</span></div>
            <div class="wdone"><b>장부</b><span>사용 ${won(lsum("use"))} · 충전 ${won(lsum("charge"))} (${ltx.length}건)</span></div>
          </section>
          <section class="panel">
            <header><div><h3>기록</h3><p>언제 · 어느 기기 · 무엇을. 지우거나 고칠 수 없습니다.</p></div></header>
            <div class="filters">${[["all", "전체"]].concat(Object.keys(KIND).map(k => [k, KIND[k]])).map(([k, l]) => `<button data-a="log-k" data-v="${k}" class="${kf === k ? "on" : ""}">${l}</button>`).join("")}
              <button data-a="log-d" class="${view.logDay === "all" ? "on" : ""}">${view.logDay === "all" ? "전체 날짜" : "오늘만"}</button></div>
            <div class="logs">${logs.length ? logs.slice(0, 200).map(l => `<div class="lg"><span class="num">${md(l.at)}</span><span class="chip src">${KIND[l.kind] || l.kind}</span><span class="tx2">${esc(l.text)}<small>${esc(l.by || "")}</small></span></div>`).join("") : `<div class="empty sm">기록이 없습니다.</div>`}</div>
          </section>
        </div>
      </div>`;
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
      view.sheet = null; toast(`${form.name.trim()} 님 ${form.time} ${form.people}명 예약을 등록했습니다`, form.phone.trim() ? "확정 알림톡을 보냈습니다" : "");
    }
    else if(a === "st"){
      const r = ZB.update(el.dataset.id, { status: v });
      if(r){ const M = { ok: "확정했습니다", in: "방문 처리했습니다", noshow: "노쇼로 표시했습니다", cancel: "취소했습니다" };
        toast(`${r.name} 님 ${r.time} 예약을 ${M[v]}`, (v === "ok" || v === "cancel") && r.phone ? "손님에게 안내 알림톡을 보냈습니다" : ""); }
    }
    else if(a === "c"){
      const k = el.dataset.k, c = ZB.cfg, st = CFG_STEP[k] || [1, 0, 999], max = k === "onlineTables" ? c.tables : st[2];
      const p = {}; p[k] = Math.max(st[1], Math.min(max, c[k] + Number(v) * st[0])); ZB.setCfg(p);
    }
    else if(a === "cs"){ const k = el.dataset.k, cur = ZB.cfg[k], p = {};
      p[k] = typeof cur === "boolean" ? v === "true" : typeof cur === "number" ? Number(v) : v; ZB.setCfg(p); }
    else if(a === "r-wait"){
      const r = ZB.res.filter(x => x.id === el.dataset.id)[0]; if(!r) return;
      const x = ZB.waitAdd(r.people, r.phone, "예약 손님", true); ZB.update(r.id, { waitNo: x.no });
      toast(`${r.name} 님을 웨이팅 ${x.no}번으로 맨 앞에 넣었습니다`, "자리가 나면 웨이팅 탭에서 가장 먼저 호출됩니다");
    }
    else if(a === "w-on"){ ZB.waitOn(!ZB.wait.on); toast(ZB.wait.on ? "웨이팅 접수를 다시 받습니다" : "웨이팅 접수를 멈췄습니다", ZB.wait.on ? "" : "기다리던 팀은 그대로 남습니다"); }
    else if(a === "w-new"){ form = { people: 2, phone: "" }; view.sheet = "wnew"; }
    else if(a === "w-save"){
      const x = ZB.waitAdd(form.people, form.phone.trim(), "직접 등록"), ahead = ZB.waitAhead(x.id);
      view.sheet = null; toast(`${x.no}번 · ${x.people}명을 등록했습니다 (앞에 ${ahead}팀)`, x.phone ? "대기 접수 안내를 보냈습니다" : "");
    }
    else if(a === "w-st"){
      const x = ZB.waitSet(el.dataset.id, v);
      if(x){ const M = { call: "손님을 호출했습니다", in: "입장 처리했습니다", gone: "미방문으로 넘겼습니다", cancel: "취소했습니다", wait: "다시 대기로 되돌렸습니다" };
        toast(`${x.no}번 ${M[v]}`, v === "call" ? (x.phone ? "입장 안내를 보냈습니다" : "전화번호가 없습니다 — 번호를 직접 불러 주세요") : ""); }
    }
    else if(a === "acct"){ view.acct = v; }
    else if(a === "l-tx"){ form = { type: v, acct: view.acct, amount: "", memo: "", by: "" }; view.sheet = "lx"; }
    else if(a === "l-preset"){ form.amount = v; }
    else if(a === "l-save"){
      const n = amt(); if(n <= 0) return;
      const ac = ZB.ledger.accts.filter(x => x.id === form.acct)[0];
      ZB.addTx(form.acct, form.type, n, form.memo.trim(), form.by.trim()); view.sheet = null;
      toast(`${ac.name} ${form.type === "charge" ? "충전" : "사용"} ${won(n)} · 잔액 ${won(ZB.bal(ac.id))}`, ac.phone ? "담당자에게 내역 알림톡을 보냈습니다" : "");
    }
    else if(a === "l-void"){
      const t = ZB.ledger.tx.filter(x => x.id === v)[0]; if(!t) return;
      if(!t.void && !confirm(`${md(t.at)} ${t.type === "charge" ? "충전" : "사용"} ${won(t.amount)} 을(를) 취소할까요?\n줄은 지우지 않고 '취소' 로 남습니다.`)) return;
      ZB.voidTx(v, !t.void); toast(t.void ? "취소했습니다 — 잔액을 그 전으로 되돌렸습니다" : "되살렸습니다 — 잔액에 다시 넣었습니다");
    }
    else if(a === "l-new"){ form = { kind: "회사", name: "", contact: "", phone: "", amount: "", memo: "" }; view.sheet = "la"; }
    else if(a === "la-kind"){ form.kind = v; }
    else if(a === "la-save"){
      if(!form.name.trim()) return;
      const ac = ZB.addAcct({ name: form.name.trim(), kind: form.kind, contact: form.contact.trim(), phone: form.phone.trim(), memo: form.memo.trim() }), n = amt();
      if(n > 0) ZB.addTx(ac.id, "charge", n, "처음 맡김", form.contact.trim());
      view.acct = ac.id; view.q = ""; view.sheet = null; toast(`${ac.name} 장부를 만들었습니다${n > 0 ? " · " + won(n) : ""}`);
    }
    else if(a === "mem"){ view.mem = v; }
    else if(a === "p-earn"){ form = { phone: v || "", amount: "", name: "" }; view.sheet = "pe"; }
    else if(a === "pe-save"){
      if(!earnOk()) return;
      const r = ZB.earn(digits(form.phone), Number(digits(form.amount)), form.name, "직원 입력", { mkt: !!form.mkt, via: "직원 확인(말로)" });
      view.mem = r.m.id; view.pq = ""; view.sheet = null;
      toast(`${r.m.phone} ${pt(r.t.pts)} 적립${r.isNew ? " · 새 회원" : ""} · 모두 ${pt(ZB.pbal(r.m.id))}`, "적립 알림톡을 보냈습니다");
    }
    else if(a === "pe-ag"){ form.agree = !form.agree; }
    else if(a === "pe-mk"){ form.mkt = !form.mkt; }
    else if(a === "pe-send"){
      const n = Number(digits(form.amount)) || 0; if(n <= 0) return;
      ZB.setPending(n); view.sheet = null;
      toast(`계산대 화면에 결제 ${won(n)}을 띄웠습니다`, "손님이 번호를 누르면 여기에 바로 적립됩니다");
    }
    else if(a === "p-pend-off"){ ZB.setPending(null); toast("계산대 화면에서 거뒀습니다"); }
    else if(a === "p-use"){ form = { mem: view.mem, pts: "", said: "", code: "", codeIn: "", manual: false }; view.sheet = "pu"; }
    else if(a === "pu-code"){ form.code = String(1000 + Math.floor(Math.random() * 9000)); form.codeIn = ""; const m = ZB.points.members.filter(x => x.id === form.mem)[0]; toast(`${m.phone} 으로 인증번호를 보냈습니다`, "시안이라 실제로 보내지 않습니다 · 번호 " + form.code); }
    else if(a === "pu-manual"){ form.manual = true; }
    else if(a === "pu-all"){ form.pts = String(ZB.pstate(form.mem).usable); }
    else if(a === "pu-save"){
      if(!puOk()) return;
      const n = Number(digits(form.pts)) || 0, au = authState();
      ZB.usePts(form.mem, n, au.how); view.sheet = null; toast(`${won(n)} 할인으로 썼습니다 · 남은 포인트 ${pt(ZB.pbal(form.mem))}`, "확인: " + au.how);
    }
    else if(a === "p-void"){
      const t = ZB.points.tx.filter(x => x.id === v)[0]; if(!t) return;
      if(!t.void && !confirm(`${md(t.at)} ${t.type === "earn" ? "적립" : "사용"} ${pt(t.pts)} 을(를) 취소할까요?\n줄은 지우지 않고 '취소' 로 남습니다.`)) return;
      ZB.voidPTx(v, !t.void); toast(t.void ? "취소했습니다 — 포인트를 그 전으로 되돌렸습니다" : "되살렸습니다");
    }
    else if(a === "cl-pos"){ const inp = $("#cl-pos"); ZB.setClosing({ pos: Number(digits(inp && inp.value)) || 0 }); }
    else if(a === "cl-done"){ ZB.setClosing({ done: Date.now() }); toast("오늘 마감을 확인했습니다", "기록에 남았습니다"); }
    else if(a === "log-k"){ view.logKind = v; }
    else if(a === "log-d"){ view.logDay = view.logDay === "all" ? "" : "all"; }
    else if(a === "reset"){ ZB.reset(); view.sheet = null; toast("자료를 처음 상태로 되돌렸습니다"); }
    render();
  });
  /* 글자 칸은 다시 그리지 않고 값만 받아 둠(그리면 입력 중에 초점이 날아감). 등록 단추만 켜고 끔 */
  document.addEventListener("input", e => {
    const ds = e.target.dataset || {};
    if(ds.cl === "pos"){ const d = digits(e.target.value); e.target.value = d ? Number(d).toLocaleString("ko-KR") : ""; return; }
    if(ds.q === "p"){ view.pq = e.target.value; const box = $("#mem-list"); if(box) box.innerHTML = memRows(); return; }   /* 회원 찾기 — 목록만 다시 그림 */
    if(ds.q){ view.q = e.target.value; const box = $("#acct-list"); if(box) box.innerHTML = acctRows(); return; }   /* 장부 찾기 — 목록만 다시 그림 */
    const k = ds.f; if(!k || !form) return;
    form[k] = e.target.value;
    const b = $("[data-a=f-save]"); if(b) b.disabled = !(form.time && form.name.trim());
    if(view.sheet === "lx"){ $("#lx-pv").innerHTML = txPreview(); $("[data-a=l-save]").disabled = amt() <= 0; }
    if(view.sheet === "la"){ $("[data-a=la-save]").disabled = !form.name.trim(); }
    if(view.sheet === "pe"){ $("#pe-pv").innerHTML = earnPreview(); $("[data-a=pe-save]").disabled = !earnOk(); $("[data-a=pe-send]").disabled = !(Number(digits(form.amount)) > 0);
      const nw = digits(form.phone).length === 11 && !earnMember(), nm = $("#pe-name"), ag = $("#pe-agree"); if(nm) nm.hidden = !nw; if(ag) ag.hidden = !nw; }
    if(view.sheet === "pu"){ const au = authState(), box = $("#pu-auth"); $("#pu-pv").innerHTML = puPreview(); $("[data-a=pu-save]").disabled = !puOk();
      if(box){ box.textContent = au.msg; box.classList.toggle("ok", au.ok); } }
  });
  document.addEventListener("keydown", e => {
    if(e.key === "Escape" && view.sheet){ view.sheet = null; render(); return; }
    /* 창 안 글자 칸에서 Enter = 그 창의 주 단추(등록·적립·빼기 등) — 켜져 있을 때만 */
    if(e.key === "Enter" && view.sheet && e.target.matches && e.target.matches(".sheet input") && !e.isComposing){
      const b = $(".sheet footer .btn.pri:not(:disabled)"); if(b){ e.preventDefault(); b.click(); }
    }
  });
  /* 손님 홈페이지(다른 탭)에서 예약이 들어오면 바로 반영 — 실제 서비스의 '새 신청 알림' 자리 */
  window.addEventListener("storage", e => {
    if(e.key !== ZB.KEY) return;
    const before = ZB.res.filter(r => r.status === "req").length, wBefore = ZB.wait.seq, pBefore = ZB.points.seq; ZB.reload();
    const after = ZB.res.filter(r => r.status === "req").length;
    if(ZB.points.seq > pBefore){ const t = ZB.points.tx[ZB.points.tx.length - 1], m = ZB.points.members.filter(x => x.id === t.mem)[0]; if(m) view.mem = m.id; }   /* 계산대에서 적립한 손님을 바로 펼쳐 둠 */
    if(!view.sheet) render();
    if(after > before) toast("홈페이지에서 새 예약 신청이 들어왔습니다");
    else if(ZB.wait.seq > wBefore){ const x = ZB.wait.list[ZB.wait.list.length - 1]; toast(`웨이팅 ${x.no}번 · ${x.people}명이 접수됐습니다`); }
    else if(ZB.points.seq > pBefore){ const t = ZB.points.tx[ZB.points.tx.length - 1], m = ZB.points.members.filter(x => x.id === t.mem)[0];
      toast(`계산대에서 ${m ? m.phone : ""} ${pt(t.pts)} 적립`, m ? "모두 " + pt(ZB.pbal(m.id)) : ""); }
  });
  /* '기다린 지 n분' 이 흐르게 — 웨이팅 탭을 보고 있을 때만 가끔 다시 그림 */
  /* 예약 탭의 '지금' 줄도 시간 따라 내려가게. 글자를 치는 중(초점이 입력 칸)이면 건너뜀 */
  setInterval(() => { if((view.tab === "wait" || view.tab === "res") && !view.sheet && !(document.activeElement && document.activeElement.matches("input"))) render(); }, 30000);

  render();
})();
