/* 한옥반점 예약 창 — 어느 장에서든 [data-reserve] 를 누르면 뜹니다.

   흐름(한 화면에 하나씩) ① 인원 → ② 날짜 → ③ 시간 → ④ 자리 → ⑤ 메뉴 → ⑥ 예약자 정보 → ⑦ 예약 확인 → 접수
   접수는 바로 확정이 아닙니다. 가게에서 확인한 뒤 문자로 확정합니다(예약 시스템 '손님 요청' 칸으로 들어갈 예정).
   제한 시간 5분은 시간을 고른 다음(④)부터 흐릅니다.
   당일 예약은 온라인으로 받지 않습니다(내일부터). 어린이는 유아를 포함합니다.

   입력은 브라우저 기본 위젯을 쓰지 않습니다. 달력·인원·시간 모두 직접 그립니다(기기마다 같은 모습이어야 해서).

   ★ 예약 시스템과 이어붙일 곳은 RES_API 셋뿐입니다. 지금은 영업시간 규칙으로 흉내냅니다.
     month(ym, people, seat)   → {"2026-09-18": 11, …}  그 달 각 날짜에 남은 시각 수(0이면 달력에서 잠김)
     slots(date, people, seat) → ["11:00","11:30", …]    그 날 고를 수 있는 시각
     submit(payload)           → {ok:true}               '손님 요청' 으로 저장 */
(function(){
  const $ = (s, r) => (r||document).querySelector(s);
  const esc = s => String(s == null ? "" : s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  const pad = n => String(n).padStart(2,"0");
  const ymd = d => d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate());
  const mins = t => Number(t.slice(0,2))*60 + Number(t.slice(3));
  const hm = t => { const h = Math.floor(mins(t)/60), m = mins(t)%60; return (h<12?"오전":"오후")+" "+(h%12===0?12:h%12)+":"+pad(m); };
  const WD = ["일","월","화","수","목","금","토"];
  const dateText = s => { const d = new Date(s+"T00:00:00"); return (d.getMonth()+1)+"월 "+d.getDate()+"일 ("+WD[d.getDay()]+")"; };
  const MAX_DAYS = 30, ONLINE_MAX = 12, MAX_SEAT = 40, MIN_ADULTS = 2, ROOM_MIN_ADULTS = 5, LUNCH_END = 15*60+30, LIMIT_SEC = 5*60, CODE_SEC = 60;

  /* ---------- 흉내 API ---------- */
  const isHoliday = s => { const d = new Date(s+"T00:00:00"); return d.getDay() === 0 || (window.HOLIDAYS||[]).indexOf(s) >= 0; };
  const isWeekend = s => { const d = new Date(s+"T00:00:00"); return d.getDay() === 6 || isHoliday(s); };
  /* 가짜 만석: 금·토 저녁 18:00·18:30 룸은 찼다고 칩니다. 실제로는 예약 현황에서 옵니다 */
  const stubFull = (date, time, seat) => { const wd = new Date(date+"T00:00:00").getDay(); return seat === "room" && (wd === 5 || wd === 6) && (time === "18:00" || time === "18:30"); };
  window.RES_API = window.RES_API || {
    slots: async (date, people, seat) => {
      if((window.CLOSED||[]).indexOf(date) >= 0) return [];
      const out = []; const add = (a, b) => { for(let x = a; x <= b; x += 30) out.push(pad(Math.floor(x/60))+":"+pad(x%60)); };
      /* 접수 시각 = 예약 시스템 세션과 같은 값: 평일 점심 11:00–14:00 · 저녁 17:00–19:30, 토 11:00–19:30, 일·공휴일 11:00–18:00 */
      if(isHoliday(date)) add(11*60, 18*60);
      else if(isWeekend(date)) add(11*60, 19*60+30);
      else { add(11*60, 14*60); add(17*60, 19*60+30); }
      return out.filter(t => seat === "any" || !stubFull(date, t, seat));
    },
    /* 기본 구현은 slots 를 날마다 불러 셉니다. 실제로는 한 번에 받아오게 바꾸세요 */
    month: async function(ym, people, seat){
      const out = {}, first = new Date(ym+"-01T00:00:00");
      const last = new Date(first.getFullYear(), first.getMonth()+1, 0).getDate();
      for(let d = 1; d <= last; d++){ const key = ym+"-"+pad(d); out[key] = (await this.slots(key, people, seat)).length; }
      return out;
    },
    submit: async payload => { await new Promise(r => setTimeout(r, 600)); return {ok:true}; }
  };

  /* ---------- 진짜 API: js/config.js 에 window.SUPA 가 있으면 예약 시스템(Supabase)과 붙습니다 ----------
     · 남은 자리는 public_avail 표(예약 시스템 태블릿이 30일치를 올려 둠)를 읽습니다 —
       {"11:00":{"rooms":[[최소,최대],…],"tableMax":n}, …}. 룸은 인원이 어느 룸의 범위에 들면, 테이블은 tableMax 이하면 가능.
     · 접수는 requests 표에 한 줄. 서버가 규칙(내일부터·성인 2·룸 성인 5·12명 이하·번호당 하루 3건)을 한 번 더 확인합니다. */
  if(window.SUPA && SUPA.url && SUPA.anonKey){
    const H = { "apikey": SUPA.anonKey, "Authorization": "Bearer " + SUPA.anonKey, "Content-Type": "application/json" };
    const get = async path => { const r = await fetch(SUPA.url + path, {headers:H}); if(!r.ok) throw new Error("HTTP " + r.status); return r.json(); };
    const okAt = (e, people, seat) => {
      if(!e) return false;
      const room = (e.rooms||[]).some(([mn, mx]) => people >= mn && people <= mx), table = people <= (e.tableMax||0);
      return seat === "room" ? room : seat === "table" ? table : (room || table);
    };
    const availCache = {};
    const dayData = async date => { if(!(date in availCache)){ const rows = await get(`/rest/v1/public_avail?store=eq.${SUPA.store}&date=eq.${date}&select=data`); availCache[date] = rows[0] ? rows[0].data : null; } return availCache[date]; };
    RES_API.slots = async (date, people, seat) => {
      const d = await dayData(date); if(!d) return [];
      return Object.keys(d).sort().filter(t => okAt(d[t], people, seat));
    };
    RES_API.month = async (ym, people, seat) => {
      const rows = await get(`/rest/v1/public_avail?store=eq.${SUPA.store}&date=like.${ym}%25&select=date,data`);
      const out = {}; rows.forEach(r => { availCache[r.date] = r.data; out[r.date] = Object.keys(r.data||{}).filter(t => okAt(r.data[t], people, seat)).length; });
      /* 표에 없는 날(태블릿이 아직 안 올린 날)은 0 = 고를 수 없음 */
      const first = new Date(ym + "-01T00:00:00"), last = new Date(first.getFullYear(), first.getMonth()+1, 0).getDate();
      for(let i = 1; i <= last; i++){ const k = ym + "-" + pad(i); if(!(k in out)) out[k] = 0; }
      return out;
    };
    RES_API.submit = async p => {
      const body = { id:"rq_" + Math.random().toString(36).slice(2, 10) + Date.now().toString(36), store:SUPA.store,
        date:p.date, time:p.time, adults:p.adults, kids:p.kids, people:p.people, seat:p.seat, course:p.course, course_label:p.courseLabel,
        name:p.name, phone:String(p.phone).replace(/\D/g,""), request:p.request||"", status:"대기" };
      const r = await fetch(SUPA.url + "/rest/v1/requests", { method:"POST", headers:Object.assign({"Prefer":"return=minimal"}, H), body:JSON.stringify(body) });
      if(r.ok) return {ok:true};
      let msg = ""; try{ msg = (await r.json()).message || ""; }catch(e){}
      if(/RATE_PHONE/.test(msg)) return {ok:false, msg:"이 번호로 오늘 접수한 예약이 이미 3건입니다. 전화로 문의해 주세요."};
      if(/RATE_ALL/.test(msg)) return {ok:false, msg:"지금 접수가 몰려 있습니다. 잠시 뒤 다시 시도해 주세요."};
      return {ok:false, msg:"접수가 되지 않았습니다. 잠시 뒤 다시 시도하시거나 전화로 문의해 주세요."};
    };
  }

  /* ---------- 상태 ---------- */
  let S, step, timer, left, ov, monthCache, extended;   /* extended: 5분 연장을 한 번 썼는지 */
  const total = () => S.adults + S.kids;
  const tooMany = () => total() > ONLINE_MAX;
  function reset(){
    S = {date:"", adults:0, kids:0, time:"", seat:"", course:"", courseLabel:"", name:"", phone:"",
         sent:false, verified:false, req:"", agree:{rule:false, priv:false, age:false}};
    step = 1; monthCache = {};
    clearInterval(timer); timer = null; left = LIMIT_SEC; extended = false;
  }

  /* ---------- 창 ---------- */
  function open(){
    if(ov) return;
    reset();
    ov = document.createElement("div"); ov.className = "rv-ov";
    ov.innerHTML = `<div class="rv" role="dialog" aria-modal="true" aria-label="예약">
        <div class="rv-h">
          <div class="rv-ttl"><span>한옥반점</span><h2>예약</h2></div>
          <div class="rv-timer" hidden><span>시간 내 예약을 완료해 주세요</span><b id="rv-clock">5:00</b><button type="button" class="rv-ext" id="rv-ext" hidden>+5분</button></div>
          <button class="rv-x" aria-label="닫기"><svg viewBox="0 0 20 20"><path d="M4 4l12 12M16 4L4 16"/></svg></button>
        </div>
        <ol class="rv-steps"></ol>
        <div class="rv-b"></div>
        <div class="rv-f"></div>
      </div>`;
    document.body.append(ov); document.body.classList.add("rv-open");
    ov.addEventListener("click", e => { if(e.target === ov) confirmClose(); });
    $(".rv-x", ov).addEventListener("click", confirmClose);
    document.addEventListener("keydown", onKey);
    render();
  }
  function close(){
    if(!ov) return;
    clearInterval(timer); timer = null;
    ov.remove(); ov = null;
    document.body.classList.remove("rv-open");
    document.removeEventListener("keydown", onKey);
  }
  function confirmClose(){
    if(step > 1 && step < 8){ ask("예약을 그만두시겠습니까?", "입력하신 내용은 저장되지 않습니다.", "그만두기", close); return; }
    close();
  }
  function onKey(e){ if(e.key === "Escape"){ if($(".rv-ask", ov)) $(".rv-ask .no", ov).click(); else confirmClose(); } }

  /* 창 안에서 묻는 작은 확인 상자 */
  function ask(title, body, okLabel, onOk){
    const box = document.createElement("div"); box.className = "rv-ask";
    box.innerHTML = `<div class="rv-ask-in" role="alertdialog" aria-modal="true">
        <h4>${esc(title)}</h4><p>${body}</p>
        <div class="rv-ask-f"><button type="button" class="btn ghost no">취소</button><button type="button" class="btn fill yes">${esc(okLabel)}</button></div>
      </div>`;
    $(".rv", ov).append(box);
    $(".no", box).addEventListener("click", () => box.remove());
    $(".yes", box).addEventListener("click", () => { box.remove(); onOk(); });
    $(".yes", box).focus();
  }

  function startTimer(){
    if(timer) return;
    $(".rv-timer", ov).hidden = false;
    /* 1분 남으면 '+5분' 이 나타나고, 한 번만 쓸 수 있습니다 */
    $("#rv-ext", ov).addEventListener("click", () => { if(extended) return; extended = true; left += LIMIT_SEC; $("#rv-ext", ov).hidden = true; tick(); });
    tick(); timer = setInterval(tick, 1000);
  }
  function tick(){
    if(!ov) return;
    const c = $("#rv-clock", ov); if(!c) return;
    c.textContent = Math.floor(left/60)+":"+pad(left%60);
    c.classList.toggle("warn", left <= 60);
    const ext = $("#rv-ext", ov); if(ext) ext.hidden = !(left <= 60 && !extended);
    if(left <= 0){
      clearInterval(timer); timer = null;
      const keep = {adults:S.adults, kids:S.kids, date:S.date};
      reset(); Object.assign(S, keep);
      $(".rv-timer", ov).hidden = true;
      render("시간이 만료되었습니다.");
      return;
    }
    left--;
  }

  /* ---------- 온라인으로 못 받는 조합은 전화로 ---------- */
  function phoneOnly(){
    if(S.seat === "room" && S.adults < ROOM_MIN_ADULTS) return `룸 예약은 성인 기준 ${ROOM_MIN_ADULTS}명부터 받고 있습니다.`;
    if(S.seat === "table" && total() > 8) return "테이블은 8명까지 온라인으로 받고 있습니다.";
    return "";
  }
  const telBox = msg => `<div class="rv-note">${esc(msg)}<a class="rv-tel-lnk" href="tel:${INFO.tel}">${esc(INFO.tel)}</a></div>`;

  /* ---------- 틀 ---------- */
  const STEPS = ["인원", "날짜", "시간", "자리", "메뉴", "예약자 정보", "예약 확인"];
  function render(msg){
    const steps = $(".rv-steps", ov);
    steps.hidden = step > STEPS.length;
    steps.innerHTML = STEPS.map((t,i) => `<li class="${i+1===step?'on':(i+1<step?'done':'')}"><i>${i+1}</i>${t}</li>`).join("");
    const b = $(".rv-b", ov), f = $(".rv-f", ov);
    b.scrollTop = 0;
    b.innerHTML = msg ? `<div class="rv-msg">${esc(msg)}</div>` : "";
    [null, sPeople, sDate, sTime, sSeat, sMenu, sGuest, sConfirm, done][step](b, f);
    const on = steps.querySelector(".on"); if(on && on.scrollIntoView) on.scrollIntoView({block:"nearest", inline:"center"});
  }
  /* warn 을 주면 다음 버튼 왼쪽에 경고 문구가 뜹니다(이전 버튼·전화 안내 자리) */
  function foot(f, prev, next, label, off, warn){
    const leftEl = warn ? `<div class="rv-warn">${warn}</div>`
                 : prev ? `<button type="button" class="btn ghost" data-prev>이전</button>`
                        : `<a class="rv-call" href="tel:${INFO.tel}"><b>전화로 예약</b><span>${esc(INFO.tel)}</span></a>`;
    f.innerHTML = leftEl + `<button type="button" class="btn fill" data-next${off?" disabled":""}>${label||"다음"}</button>`;
    if(prev) $("[data-prev]", f).addEventListener("click", () => { step--; render(); });
    $("[data-next]", f).addEventListener("click", next);
  }
  const peopleText = () => S.kids ? `성인 ${S.adults} · 어린이 ${S.kids}` : `성인 ${S.adults}`;
  const sumLine = () => {
    const bits = [peopleText()];
    if(S.date) bits.push(dateText(S.date));
    if(S.time) bits.push(hm(S.time));
    if(S.seat) bits.push(S.seat === "room" ? "룸" : "테이블");
    if(S.courseLabel) bits.push(S.courseLabel);
    return `<div class="rv-sum">${bits.map(x=>`<span>${esc(x)}</span>`).join("")}</div>`;
  };
  const dayRange = () => { const t = new Date(); return { min: ymd(new Date(t.getTime() + 864e5)), max: ymd(new Date(t.getTime() + MAX_DAYS*864e5)) }; };   /* 내일부터 */

  /* ---------- ① 인원 ---------- */
  function sPeople(b, f){
    const stepper = (key, label, note) => `<div class="rv-cnt" data-k="${key}">
        <div class="rv-cnt-l"><b>${label}</b>${note?`<span>${note}</span>`:""}</div>
        <div class="rv-cnt-r">
          <button type="button" data-d="-1" aria-label="${label} 한 명 줄이기"><svg viewBox="0 0 24 24"><path d="M5 12h14"/></svg></button>
          <b class="rv-cnt-n">${S[key]}</b>
          <button type="button" data-d="1" aria-label="${label} 한 명 늘리기"><svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg></button>
        </div>
      </div>`;
    b.insertAdjacentHTML("beforeend", `<section class="rv-sec">
        <h3>몇 분이 오시나요</h3>
        ${stepper("adults", "성인")}
        ${stepper("kids", "어린이", "유아 포함")}
      </section>`);
    const ok = () => !tooMany() && S.adults >= MIN_ADULTS;
    function sync(){
      b.querySelectorAll(".rv-cnt").forEach(r => r.querySelectorAll("button").forEach(y =>
        y.disabled = (y.dataset.d === "-1" ? S[r.dataset.k] <= 0 : total() >= MAX_SEAT)));
      const warn = tooMany()
        ? `${total()}명은 온라인으로 접수하기 어렵습니다.<br>전화로 문의해 주세요. <a href="tel:${INFO.tel}">${esc(INFO.tel)}</a>`
        : (S.adults < MIN_ADULTS ? `성인 ${MIN_ADULTS}명부터 접수할 수 있습니다.` : "");
      foot(f, false, next, "다음", !ok(), warn);
    }
    b.querySelectorAll(".rv-cnt").forEach(row => {
      const key = row.dataset.k, num = $(".rv-cnt-n", row);
      row.querySelectorAll("button").forEach(x => x.addEventListener("click", () => {
        const n = Math.max(0, S[key] + Number(x.dataset.d));
        if(n === S[key] || total() - S[key] + n > MAX_SEAT) return;
        S[key] = n; num.textContent = n; monthCache = {}; S.time = ""; sync();
      }));
    });
    function next(){ if(ok()){ step = 2; render(); } }
    sync();
  }

  /* ---------- ② 날짜 ---------- */
  function sDate(b, f){
    const {min, max} = dayRange();
    let view = new Date((S.date || min) + "T00:00:00"); view.setDate(1);
    b.insertAdjacentHTML("beforeend", sumLine() + `<section class="rv-sec">
        <h3>날짜</h3>
        <div class="rv-cal">
          <div class="rv-cal-h">
            <button type="button" class="rv-mo" data-m="-1" aria-label="지난달"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
            <b id="rv-cal-t"></b>
            <button type="button" class="rv-mo" data-m="1" aria-label="다음달"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
          </div>
          <div class="rv-wd">${WD.map((w,i)=>`<span class="${i===0?'sun':(i===6?'sat':'')}">${w}</span>`).join("")}</div>
          <div class="rv-days" id="rv-days"></div>
        </div>
      </section>`);
    const days = $("#rv-days", b), title = $("#rv-cal-t", b);
    b.querySelectorAll(".rv-mo").forEach(x => x.addEventListener("click", () => { view.setMonth(view.getMonth() + Number(x.dataset.m)); draw(); }));
    async function draw(){
      const ym = view.getFullYear()+"-"+pad(view.getMonth()+1);
      title.textContent = view.getFullYear()+"년 "+(view.getMonth()+1)+"월";
      const first = new Date(view.getFullYear(), view.getMonth(), 1);
      const lastDay = new Date(view.getFullYear(), view.getMonth()+1, 0).getDate();
      b.querySelector('[data-m="-1"]').disabled = ym <= min.slice(0,7);
      b.querySelector('[data-m="1"]').disabled = ym >= max.slice(0,7);
      const cells = [];
      for(let i = 0; i < first.getDay(); i++) cells.push(`<span class="pad"></span>`);
      for(let d = 1; d <= lastDay; d++){
        const key = ym+"-"+pad(d), wd = new Date(key+"T00:00:00").getDay();
        const out = key < min || key > max;
        cells.push(`<button type="button" data-day="${key}" class="${wd===0||isHoliday(key)?'sun':(wd===6?'sat':'')}${key===S.date?' on':''}"${out?" disabled":""}>${d}</button>`);
      }
      days.innerHTML = cells.join("");
      days.querySelectorAll("[data-day]").forEach(el => el.addEventListener("click", () => {
        S.date = el.dataset.day; S.time = "";
        days.querySelectorAll("[data-day]").forEach(x => x.classList.toggle("on", x === el));
        foot(f, true, next, "다음", false);
      }));
      if(!monthCache[ym]){
        days.classList.add("loading");
        monthCache[ym] = await RES_API.month(ym, total(), S.seat || "any");
        days.classList.remove("loading");
      }
      const m = monthCache[ym];
      days.querySelectorAll("[data-day]").forEach(el => { if(!el.disabled && m[el.dataset.day] === 0) el.disabled = true; });
      if(S.date && m[S.date] === 0){ S.date = ""; foot(f, true, next, "다음", true); }
    }
    function next(){ if(S.date){ step = 3; render(); } }
    foot(f, true, next, "다음", !S.date);
    draw();
  }

  /* ---------- ③ 시간 ---------- */
  function sTime(b, f){
    b.insertAdjacentHTML("beforeend", sumLine() + `<section class="rv-sec"><h3>시간</h3><div id="rv-times"><p class="rv-quiet">불러오는 중…</p></div></section>`);
    const times = $("#rv-times", b);
    foot(f, true, next, "다음", true);
    (async () => {
      const want = S.date;
      const list = await RES_API.slots(S.date, total(), S.seat || "any");
      if(!ov || want !== S.date) return;
      if(!list.length){ times.innerHTML = `<p class="rv-quiet">이 날은 예약 가능한 시간이 없습니다. 다른 날짜를 골라 주세요.</p>`; return; }
      const lunch = list.filter(t => mins(t) < LUNCH_END), dinner = list.filter(t => mins(t) >= LUNCH_END);
      const grid = (label, arr) => arr.length ? `<div class="rv-tgroup"><span>${label}</span><div class="rv-times">${
        arr.map(t => `<button type="button" data-t="${t}" class="${t===S.time?'on':''}">${hm(t)}</button>`).join("")}</div></div>` : "";
      times.innerHTML = grid("점심", lunch) + grid("저녁", dinner);
      times.querySelectorAll("[data-t]").forEach(el => el.addEventListener("click", () => {
        if(S.time !== el.dataset.t){ S.course = ""; S.courseLabel = ""; }
        S.time = el.dataset.t;
        times.querySelectorAll("[data-t]").forEach(x => x.classList.toggle("on", x === el));
        foot(f, true, next, "다음", false);
      }));
      foot(f, true, next, "다음", !S.time);
    })();
    function next(){ if(S.time){ startTimer(); step = 4; render(); } }
  }

  /* ---------- ④ 자리 ---------- */
  function sSeat(b, f){
    b.insertAdjacentHTML("beforeend", sumLine() + `<section class="rv-sec">
        <h3>자리</h3>
        <div class="rv-pick two" id="rv-seat">
          <button type="button" data-s="table" class="${S.seat==='table'?'on':''}"><b>테이블</b></button>
          <button type="button" data-s="room" class="${S.seat==='room'?'on':''}"><b>룸</b></button>
        </div>
        <div id="rv-seat-hint"></div>
      </section>`);
    const seg = $("#rv-seat", b), hint = $("#rv-seat-hint", b);
    function draw(){
      seg.querySelectorAll("[data-s]").forEach(x => x.classList.toggle("on", x.dataset.s === S.seat));
      const po = S.seat ? phoneOnly() : "";
      hint.innerHTML = "";
      foot(f, true, next, "다음", !S.seat || !!po, po ? `${esc(po)} <a href="tel:${INFO.tel}">${esc(INFO.tel)}</a>` : "");
    }
    seg.querySelectorAll("[data-s]").forEach(x => x.addEventListener("click", () => {
      if(S.seat !== x.dataset.s){ S.seat = x.dataset.s; S.course = ""; S.courseLabel = ""; }
      draw();
    }));
    function next(){ if(S.seat && !phoneOnly()){ step = 5; render(); } }
    draw();
  }

  /* ---------- ⑤ 메뉴 — 점심 시각이면 그 날(평일·주말)의 점심 세트도 함께 ---------- */
  function menuGroups(){
    const out = [];
    if(mins(S.time) < LUNCH_END){
      const want = isWeekend(S.date) ? "주말" : "평일";
      const set = MENU.lunch.filter(g => g.title.indexOf(want) === 0)[0] || MENU.lunch[0];
      out.push({ title: set.title, items: set.items.map(x => ({key:"set:"+x.name, name:x.name, cn:""})) });
    }
    out.push({ title: MENU.courses.title, items: MENU.courses.items.map(c => ({key:"course:"+c.name, name:c.name, cn:c.cn})) });
    return out;
  }
  function sMenu(b, f){
    const room = S.seat === "room";
    b.insertAdjacentHTML("beforeend", sumLine() + `<section class="rv-sec">
        <h3>메뉴</h3>
        ${room ? `<p class="rv-quiet">룸은 코스, 또는 그에 상응하는 금액의 단품 주문이 가능합니다.</p>` : ""}
        <div class="rv-pick" id="rv-cs">
          ${menuGroups().map(g => `<div class="rv-pick-h">${esc(g.title)}</div>` + g.items.map(it =>
              `<button type="button" data-c="${esc(it.key)}" data-l="${esc(it.name)}" class="${S.course===it.key?'on':''}"><b>${esc(it.name)}${it.cn?`<small>${esc(it.cn)}</small>`:""}</b><span class="qty">${total()}인분</span></button>`).join("")).join("")}
          <div class="rv-pick-h">그 밖에</div>
          ${room ? `<button type="button" data-c="later" data-l="메뉴 미정" class="${S.course==='later'?'on':''}"><b>미정</b></button>`
                 : `<button type="button" data-c="none" data-l="단품 주문" class="${S.course==='none'?'on':''}"><b>단품 주문</b></button>`}
        </div>
        <p class="rv-quiet"><a href="${INFO.menuPdf}" target="_blank" rel="noopener">메뉴판(PDF) 보기</a></p>
      </section>`);
    b.querySelectorAll("[data-c]").forEach(el => el.addEventListener("click", () => {
      S.course = el.dataset.c; S.courseLabel = el.dataset.l;
      b.querySelectorAll("[data-c]").forEach(x => x.classList.toggle("on", x === el));
      foot(f, true, next, "다음", false);
    }));
    function go(){ step = 6; render(); }
    function next(){
      if(!S.course) return;
      if(room) ask("룸 이용 안내", "룸에서는 <b>코스</b>, 또는 그에 상응하는 금액의 단품 주문만 가능합니다.", "확인", go);
      else go();
    }
    foot(f, true, next, "다음", !S.course);
  }

  /* ---------- ⑥ 예약자 정보 ---------- */
  function sGuest(b, f){
    b.insertAdjacentHTML("beforeend", sumLine() + `<section class="rv-sec">
        <h3>예약자 정보</h3>
        <div class="rv-fld"><label for="rv-name">성함</label><input id="rv-name" value="${esc(S.name)}" placeholder="성함을 입력해 주세요" autocomplete="name"></div>
        <div class="rv-fld">
          <label for="rv-phone">전화번호</label>
          <div class="rv-inline">
            <input id="rv-phone" type="tel" value="${esc(S.phone)}" placeholder="010-0000-0000" autocomplete="tel" inputmode="numeric"${S.verified?" disabled":""}>
            <button type="button" class="btn" id="rv-send"${S.verified?" disabled":""}>${S.verified ? "인증 완료" : "인증번호 요청"}</button>
          </div>
          <div class="rv-inline" id="rv-codebox"${S.sent && !S.verified ? "" : " hidden"}>
            <input id="rv-code" inputmode="numeric" maxlength="6" placeholder="인증번호 6자리">
            <button type="button" class="btn" id="rv-verify">확인</button>
          </div>
          <p class="rv-fld-hint" id="rv-tel-hint">${S.verified ? "인증되었습니다." : ""}</p>
        </div>
        <div class="rv-fld"><label for="rv-req">요청사항 <em>선택</em></label>
          <textarea id="rv-req" rows="3" placeholder="알레르기가 있으시거나 어린이 의자·식기가 필요하시면 적어 주세요. 예약하시는 분과 방문하시는 분이 다르면 함께 적어 주세요.">${esc(S.req)}</textarea></div>
      </section>`);
    const name = $("#rv-name", b), phone = $("#rv-phone", b), send = $("#rv-send", b),
          codebox = $("#rv-codebox", b), code = $("#rv-code", b), verify = $("#rv-verify", b), hint = $("#rv-tel-hint", b), req = $("#rv-req", b);
    let codeTimer = null, codeLeft = 0;
    const codeTick = () => {
      if(codeLeft <= 0){ clearInterval(codeTimer); codeTimer = null; verify.disabled = true; hint.textContent = "인증번호가 만료되었습니다. 다시 요청해 주세요."; hint.classList.add("bad"); return; }
      hint.textContent = `문자로 보낸 인증번호를 입력해 주세요. (${pad(Math.floor(codeLeft/60))}:${pad(codeLeft%60)})`; codeLeft--;
    };
    const ok = () => S.name.trim().length >= 2 && S.verified;
    const refoot = () => foot(f, true, next, "다음", !ok());
    name.addEventListener("input", () => { S.name = name.value; refoot(); });
    req.addEventListener("input", () => { S.req = req.value; });
    phone.addEventListener("input", () => {
      const d = phone.value.replace(/\D/g, "").slice(0, 11);
      phone.value = d.length > 7 ? d.replace(/(\d{3})(\d{3,4})(\d{0,4})/, "$1-$2-$3") : d.length > 3 ? d.replace(/(\d{3})(\d{0,4})/, "$1-$2") : d;
      S.phone = phone.value;
    });
    send.addEventListener("click", () => {
      const d = S.phone.replace(/\D/g, "");
      if(!/^01\d{8,9}$/.test(d)){ hint.textContent = "휴대폰 번호를 확인해 주세요."; hint.classList.add("bad"); return; }
      /* 실제로는 여기서 문자를 보냅니다 */
      S.sent = true; codebox.hidden = false; send.textContent = "다시 요청"; verify.disabled = false; code.value = "";
      hint.classList.remove("bad"); clearInterval(codeTimer); codeLeft = CODE_SEC; codeTick(); codeTimer = setInterval(codeTick, 1000);
      code.focus();
    });
    verify.addEventListener("click", () => {
      if(!/^\d{6}$/.test(code.value)){ hint.textContent = "6자리 숫자를 입력해 주세요."; hint.classList.add("bad"); return; }
      clearInterval(codeTimer); codeTimer = null;
      S.verified = true; codebox.hidden = true; phone.disabled = true; send.disabled = true; send.textContent = "인증 완료";
      hint.classList.remove("bad"); hint.textContent = "인증되었습니다."; refoot();
    });
    function next(){ if(ok()){ step = 7; render(); } }
    refoot();
  }

  /* ---------- ⑦ 예약 확인 ---------- */
  function sConfirm(b, f){
    const rows = [
      ["날짜", dateText(S.date)], ["시간", hm(S.time)],
      ["인원", S.kids ? `성인 ${S.adults}명 · 어린이 ${S.kids}명` : `성인 ${S.adults}명`],
      ["자리", S.seat === "room" ? "룸" : "테이블"],
      ["메뉴", S.course === "later" ? "미정" : (S.course === "none" ? "단품 주문" : `${S.courseLabel} · ${total()}인분`)],
      ["예약자", S.name.trim()+" · "+S.phone]
    ];
    if(S.req.trim()) rows.push(["요청사항", S.req.trim()]);
    const box = (key, title, body) => `<div class="rv-agree${S.agree[key]?" on":""}">
        <div class="rv-agree-h">
          <label class="rv-chk"><input type="checkbox" data-a="${key}"${S.agree[key]?" checked":""}><i></i></label>
          <button type="button" class="rv-agree-t"><b>[필수] ${title}</b><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></button>
        </div>
        <div class="body">${body}</div></div>`;
    b.insertAdjacentHTML("beforeend", `<section class="rv-sec">
        <h3>예약 확인</h3>
        <dl class="rv-check">${rows.map(([k,v])=>`<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join("")}</dl>
      </section>
      <section class="rv-sec">
        ${box("rule", "매장 이용규정에 동의합니다", `<ul>
            <li>접수 후 가게에서 확인하고 문자로 확정을 알려드립니다.</li>
            <li>룸에서는 코스, 또는 그에 상응하는 금액의 단품 주문만 가능합니다.</li>
            <li>룸은 인원에 맞춰 배정합니다. 원하시는 룸이 있으면 요청사항에 적어 주세요.</li>
            <li>인원이 바뀌면 미리 알려 주세요. 자리와 준비가 달라집니다.</li>
            <li>예약 시각에서 20분이 지나도록 연락이 없으면 자리를 다른 손님께 드릴 수 있습니다.</li>
            <li>취소는 전화로 부탁드립니다. 예약금과 결제는 없습니다.</li></ul>`)}
        ${box("priv", "개인정보 수집 · 이용에 동의합니다", `<table>
            <tr><th>항목</th><th>목적</th><th>보유 기간</th></tr>
            <tr><td>성함, 휴대폰 번호</td><td>예약 확인과 안내 문자 발송</td><td>방문일로부터 90일</td></tr>
            <tr><td>요청사항</td><td>자리와 식사 준비</td><td>방문일로부터 90일</td></tr></table>
          <p>동의하지 않으셔도 전화로 예약하실 수 있습니다.</p>`)}
        ${box("age", "만 14세 이상입니다", `<p>만 14세 미만은 보호자가 대신 예약해 주세요.</p>`)}
      </section>`);
    b.querySelectorAll("[data-a]").forEach(c => c.addEventListener("change", () => {
      S.agree[c.dataset.a] = c.checked; c.closest(".rv-agree").classList.toggle("on", c.checked); refoot();
    }));
    b.querySelectorAll(".rv-agree-t").forEach(t => t.addEventListener("click", () => t.closest(".rv-agree").classList.toggle("open")));
    const all = () => S.agree.rule && S.agree.priv && S.agree.age;
    const refoot = () => foot(f, true, submit, "접수하기", !all());
    async function submit(){
      if(!all()) return;
      const btn = $("[data-next]", f); btn.disabled = true; btn.textContent = "접수 중…";
      const r = await RES_API.submit({date:S.date, time:S.time, adults:S.adults, kids:S.kids, people:total(),
                                      seat:S.seat, course:S.course, courseLabel:S.courseLabel,
                                      name:S.name.trim(), phone:S.phone, request:S.req.trim()});
      if(r && r.ok){ clearInterval(timer); timer = null; step = 8; render(); }
      else { btn.disabled = false; btn.textContent = "접수하기"; render((r && r.msg) || "접수가 되지 않았습니다. 잠시 뒤 다시 시도하시거나 전화로 문의해 주세요."); }
    }
    refoot();
  }

  /* ---------- 접수 완료 ---------- */
  function done(b, f){
    $(".rv-timer", ov).hidden = true;
    b.innerHTML = `<div class="rv-done">
        <div class="rv-tick"><svg viewBox="0 0 48 48"><path d="M14 25l7 7 14-15"/></svg></div>
        <h3>접수되었습니다</h3>
        <p class="big">${esc(dateText(S.date))} ${esc(hm(S.time))} · ${esc(peopleText())} · ${S.seat==="room"?"룸":"테이블"}</p>
        <p>확인 후 <b>${esc(S.phone)}</b> 로 예약 확정 문자를 보내드립니다.</p>
        <p class="rv-quiet">예약 변경 혹은 다른 문의사항은 <a href="tel:${INFO.tel}">${esc(INFO.tel)}</a> 로 전화 주세요.</p>
      </div>`;
    f.innerHTML = `<span></span><button type="button" class="btn fill" data-close>닫기</button>`;
    $("[data-close]", f).addEventListener("click", close);
  }

  document.addEventListener("click", e => {
    const t = e.target.closest("[data-reserve]"); if(!t) return;
    e.preventDefault(); open();
  });
  window.openReserve = open;

  /* 미리보기: ?rv=5 처럼 붙이면 그 단계가 보기 데이터로 열립니다(스크린샷·검토용) */
  const m = location.search.match(/[?&]rv=(\d)/);
  if(m){
    open();
    const d = new Date(Date.now() + 3*864e5);
    Object.assign(S, {date:ymd(d), time:"12:30", adults:5, kids:1, seat:"room", course:"course:촉 코스", courseLabel:"촉 코스",
                      name:"홍길동", phone:"010-1234-5678", sent:true, verified:true});
    step = Number(m[1]);
    if(step === 1){ S.adults = 1; S.kids = 0; }
    if(step > 3) startTimer();
    render();
  }
})();
