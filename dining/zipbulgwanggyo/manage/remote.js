/* DineONE — 매장 화면 시안을 실제 DB(Supabase dineone-dev)에 연결 (11-12).
   주소에 ?db=dev 가 있을 때만 움직입니다. 없으면 아무것도 하지 않고 시안은 지금처럼 브라우저 저장으로 돕니다.

   하는 일
   · 맨 위 노란 DEV 띠(개발 DB 라는 표시, 구조 정리 14장) + 직원 로그인(이메일·비밀번호)
   · 로그인한 직원의 가게 자료를 DB 에서 읽어 store.js 의 자료 모양(ZB)으로 바꿔 끼움 → 화면(app.js)은 그대로
   · 화면에서 바꾼 것(예약·웨이팅·장부·포인트·설정·마감)을 DB 에 씀 — store.js 의 함수를 감싸 '화면 먼저 바꾸고 → DB 에 쓰고 → 다시 읽음'
   · 10초마다 다시 읽음(다른 기기에서 들어온 웨이팅·적립도 보이게). 새로 들어온 게 있으면 화면이 알림을 띄움
   ★ 여기 들어가는 키는 공개용(publishable)입니다. 지켜 주는 건 DB 의 로그인과 권한(RLS)입니다. 비밀 키(service_role·secret)는 절대 넣지 않음 */
(function(){
  if(!window.ZB || !ZB.REMOTE) return;
  const SB_URL = "https://fkvwexlixmukbxgtxmio.supabase.co";      /* dineone-dev (서울) */
  const SB_KEY = "sb_publishable_7Z5ZmOHNMFYFVunKQm3j5w_R4lDEjJ5"; /* 공개용 키 */
  const LIB = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.57.4/dist/umd/supabase.min.js";

  let sb = null, sid = null, me = { name: "", role: "" }, busy = 0, chain = Promise.resolve(), timer = null, lastSig = "";
  const digits = s => String(s || "").replace(/\D/g, "");
  const fmt = s => { const d = digits(s); return d.length === 11 ? d.slice(0, 3) + "-" + d.slice(3, 7) + "-" + d.slice(7) : d; };
  const ms = t => t ? Date.parse(t) : undefined;
  const iso = n => new Date(n).toISOString();
  const won = n => Number(n || 0).toLocaleString("ko-KR") + "원";

  /* ---------- 이름 바꾸기 (DB 값 ↔ 화면 값) ---------- */
  const RES_SRC = { web: "홈페이지", phone: "전화", walkin: "방문", staff: "직원", other: "기타" };
  const RES_SRC_DB = { "홈페이지": "web", "전화": "phone", "방문": "walkin" };
  const WAIT_SRC = { entrance: "입구 접수", staff: "직접 등록", reservation: "예약 손님", remote: "원격 접수" };
  const P_SRC = { counter: "계산대", staff: "직원 입력", receipt: "영수증", pos: "포스", system: "시스템" };
  const P_SRC_DB = { "계산대": "counter", "직원 입력": "staff" };
  const HOW = { name: "이름+번호", code: "인증번호", manual: "직원이 직접 확인" };
  const HOW_DB = { "이름+번호": "name", "인증번호": "code", "직원이 직접 확인": "manual" };
  const resStatus = s => s === "seated" || s === "done" ? "in" : s;
  const resStatusDb = s => s === "in" ? "seated" : s;

  /* ---------- 맨 위 DEV 띠 · 로그인 ---------- */
  const css = document.createElement("style");
  css.textContent = `.devbar{display:flex; gap:12px; align-items:center; justify-content:space-between; padding:6px 14px; background:#FFD60A; color:#000; font:600 13px/1.4 -apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}
    .devbar button{border:0; background:rgba(0,0,0,.12); border-radius:8px; padding:4px 10px; font:inherit; cursor:pointer}
    .devbar .err{color:#B00020}
    .devlogin{position:fixed; inset:0; z-index:200; display:grid; place-items:center; background:rgba(242,242,247,.96); padding:16px}
    .devlogin form{width:min(360px,100%); background:#fff; border-radius:18px; padding:24px; box-shadow:0 10px 40px rgba(0,0,0,.12); font:15px/1.5 -apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}
    .devlogin h2{margin:0 0 4px; font-size:20px} .devlogin p{margin:0 0 16px; color:#6E6E73; font-size:13.5px}
    .devlogin input{display:block; width:100%; box-sizing:border-box; margin:0 0 10px; padding:12px; border:1px solid #D1D1D6; border-radius:10px; font:inherit}
    .devlogin button{width:100%; padding:12px; border:0; border-radius:10px; background:#1D1D1F; color:#fff; font:inherit; font-weight:600; cursor:pointer}
    .devlogin .msg{min-height:20px; margin-top:10px; color:#B00020; font-size:13.5px}`;
  document.head.appendChild(css);
  document.title = "[DEV] " + document.title;
  const bar = document.createElement("div"); bar.className = "devbar"; bar.setAttribute("role", "status");
  bar.innerHTML = `<span>DEV · 실제 개발 DB(dineone-dev)에 연결 중 — 손님 정보는 모두 더미</span><span id="dev-who"></span>`;
  document.body.insertBefore(bar, document.body.firstChild);
  const say = (html, isErr) => { const w = document.getElementById("dev-who"); if(w) w.innerHTML = isErr ? `<span class="err">${html}</span>` : html; };

  function loginForm(msg){
    let box = document.querySelector(".devlogin");
    if(!box){ box = document.createElement("div"); box.className = "devlogin"; document.body.appendChild(box); }
    box.innerHTML = `<form><h2>매장 화면 로그인</h2><p>개발 DB(dineone-dev) · Supabase Authentication 에서 만든 계정</p>
      <input type="email" name="e" placeholder="이메일" autocomplete="username" required>
      <input type="password" name="p" placeholder="비밀번호" autocomplete="current-password" required>
      <button type="submit">로그인</button><div class="msg">${msg || ""}</div></form>`;
    box.querySelector("form").addEventListener("submit", async ev => {
      ev.preventDefault();
      const f = ev.target, btn = f.querySelector("button"); btn.disabled = true; btn.textContent = "확인 중…";
      const { error } = await sb.auth.signInWithPassword({ email: f.e.value.trim(), password: f.p.value });
      if(error){ btn.disabled = false; btn.textContent = "로그인"; f.querySelector(".msg").textContent = "이메일이나 비밀번호가 맞지 않습니다"; return; }
      box.remove(); start();
    });
  }

  /* ---------- 읽기: DB → 화면 자료 ---------- */
  async function q(p){ const r = await p; if(r.error) throw r.error; return r.data; }
  async function fetchAll(){
    const today = await q(sb.rpc("biz_date", { p_store: sid }));
    const [cfgRow, feats, custs, res, waits, wc, accts, ltx, ptx, pend, clos, logs] = await Promise.all([
      q(sb.from("store_settings").select("cfg").eq("store_id", sid).maybeSingle()),
      q(sb.from("store_features").select("feature,enabled").eq("store_id", sid)),
      q(sb.from("customers").select("id,phone,name,marketing,created_at").eq("store_id", sid).range(0, 9999)),
      q(sb.from("reservations").select("*").eq("store_id", sid).range(0, 9999)),
      q(sb.from("waitlist").select("*").eq("store_id", sid).eq("biz_date", today)),
      q(sb.from("wait_counters").select("last_no").eq("store_id", sid).eq("biz_date", today).maybeSingle()),
      q(sb.from("ledger_accounts").select("*").eq("store_id", sid)),
      q(sb.from("ledger_tx").select("*").eq("store_id", sid).range(0, 9999)),
      q(sb.from("point_tx").select("*").eq("store_id", sid).range(0, 9999)),
      q(sb.from("counter_pending").select("amount,at").eq("store_id", sid).maybeSingle()),
      q(sb.from("day_closings").select("*").eq("store_id", sid).eq("biz_date", today).maybeSingle()),
      q(sb.from("activity_log").select("*").eq("store_id", sid).order("id", { ascending: false }).limit(500))
    ]);
    const C = {}; custs.forEach(c => C[c.id] = c);
    const waitByRes = {}; waits.forEach(w => { if(w.reservation_id) waitByRes[w.reservation_id] = w.no; });
    const d = ZB.blank();
    d.cfg = Object.assign({}, ZB.DEFAULT_CFG, (cfgRow && cfgRow.cfg) || {});
    d.res = res.map(r => { const c = C[r.customer_id] || {}; const o = { id: r.id, date: r.visit_date, time: String(r.visit_time).slice(0, 5), people: r.people,
      name: c.name || "", phone: fmt(c.phone), memo: r.memo || "", pre: r.pre_order || "", status: resStatus(r.status), src: RES_SRC[r.src] || r.src, at: ms(r.created_at) };
      if(waitByRes[r.id]) o.waitNo = waitByRes[r.id]; return o; });
    const fOn = {}; feats.forEach(f => fOn[f.feature] = f.enabled);
    d.wait = { on: fOn.wait !== false, seq: Math.max((wc && wc.last_no) || 0, ...waits.map(w => w.no), 0),
      list: waits.map(w => { const o = { id: w.id, no: w.no, people: w.people, phone: fmt(w.phone), src: WAIT_SRC[w.src] || w.src, status: w.status, at: ms(w.created_at) };
        if(w.called_at) o.callAt = ms(w.called_at); if(w.seated_at || w.ended_at) o.doneAt = ms(w.seated_at || w.ended_at); if(w.priority) o.first = true; return o; }) };
    d.ledger = { seq: ltx.length,
      accts: accts.map(a => ({ id: a.id, name: a.name, kind: a.kind === "person" ? "개인" : "회사", contact: a.contact || "", phone: fmt(a.phone), memo: a.memo || "" })),
      tx: ltx.map(t => { const o = { id: t.id, acct: t.account_id, type: t.type, amount: t.amount, memo: t.memo || "", by: t.by_name || "", at: ms(t.created_at) }; if(t.voided_at) o.void = true; return o; }) };
    const memIds = new Set(ptx.map(t => t.customer_id));
    d.points = { seq: ptx.length,
      members: custs.filter(c => memIds.has(c.id)).map(c => ({ id: c.id, phone: fmt(c.phone), name: c.name || "", mkt: !!c.marketing, agreeAt: ms(c.created_at) })),
      tx: ptx.map(t => { const o = { id: t.id, mem: t.customer_id, type: t.type === "use" || t.type === "adjust_sub" ? "use" : "earn", pts: t.pts, amount: t.pay_amount || 0,
        at: ms(t.created_at), src: P_SRC[t.src] || "" }; if(t.verify) o.how = HOW[t.verify]; if(t.voided_at) o.void = true; return o; }) };
    if(pend) d.points.pending = { amount: pend.amount, at: ms(pend.at) };
    if(clos) d.closing = { date: ZB.today(), pos: clos.pos_total || 0, done: clos.closed_at ? ms(clos.closed_at) : undefined };
    d.log = logs.map(logLine).filter(Boolean).reverse();
    return d;
  }

  /* 업무 기록(activity_log) 한 줄 → 화면 '마감·기록' 탭의 글 한 줄 */
  const KIND = { reservations: "res", waitlist: "wait", ledger_accounts: "ledger", ledger_tx: "ledger", point_tx: "point", customers: "point", store_settings: "cfg", store_features: "wait", day_closings: "point" };
  const WST = { call: "호출", in: "입장", gone: "미방문", cancel: "취소", wait: "대기로 되돌림" };
  const RST = { req: "새 신청", ok: "확정", seated: "방문", done: "방문", noshow: "노쇼", cancel: "취소" };
  function logLine(g){
    const a = g.after || {}, b = g.before || {}, kind = KIND[g.entity]; if(!kind) return null;
    let text = "";
    if(g.entity === "reservations") text = g.action === "insert" ? `${String(a.visit_date).slice(5)} ${String(a.visit_time).slice(0, 5)} ${a.people}명 예약 ${a.status === "req" ? "신청" : "등록"} (${RES_SRC[a.src] || a.src})`
      : a.status !== b.status ? `${String(a.visit_date).slice(5)} ${String(a.visit_time).slice(0, 5)} ${a.people}명 → ${RST[a.status] || a.status}` : `${String(a.visit_date).slice(5)} ${String(a.visit_time).slice(0, 5)} 예약 수정`;
    else if(g.entity === "waitlist") text = g.action === "insert" ? `웨이팅 ${a.no}번 ${a.people}명 접수${a.priority ? " (예약 손님 · 맨 앞)" : ""}`
      : a.status !== b.status ? `웨이팅 ${a.no}번 ${WST[a.status] || a.status}` : "";
    else if(g.entity === "ledger_accounts") text = g.action === "insert" ? `새 장부 ${a.name}` : `장부 ${a.name} 수정`;
    else if(g.entity === "ledger_tx") text = g.action === "insert" ? `${a.type === "charge" ? "충전" : "사용"} ${won(a.amount)}${a.memo ? " · " + a.memo : ""}`
      : `${a.type === "charge" ? "충전" : "사용"} ${won(a.amount)} ${a.voided_at ? "취소" : "되살림"}`;
    else if(g.entity === "point_tx") text = g.action === "insert" ? (a.type === "use" ? `사용 −${Number(a.pts).toLocaleString("ko-KR")}${a.verify ? " · 확인: " + HOW[a.verify] : ""}` : `적립 +${Number(a.pts).toLocaleString("ko-KR")} (결제 ${won(a.pay_amount)})`)
      : `${a.type === "use" ? "사용" : "적립"} ${Number(a.pts).toLocaleString("ko-KR")} ${a.voided_at ? "취소" : "되살림"}`;
    else if(g.entity === "customers") text = g.action === "insert" ? `새 회원 ${a.phone ? fmt(a.phone) : ""}` : "";
    else if(g.entity === "store_settings") { const ca = a.cfg || {}, cb = b.cfg || {}; text = "설정 " + Object.keys(ca).filter(k => JSON.stringify(ca[k]) !== JSON.stringify(cb[k])).map(k => `${k} ${cb[k]} → ${ca[k]}`).join(", "); }
    else if(g.entity === "store_features") text = a.feature === "wait" ? (a.enabled ? "웨이팅 접수 다시 받음" : "웨이팅 접수 멈춤") : `기능 ${a.feature} ${a.enabled ? "켬" : "끔"}`;
    else if(g.entity === "day_closings") text = a.closed_at && !b.closed_at ? "마감 확인 완료" : `마감: 포스 매출 ${won(a.pos_total)} 입력`;
    if(!text) return null;
    return { id: "g" + g.id, at: ms(g.at), kind: kind, text: text, by: g.actor_label || (g.actor_kind === "system" ? "시스템" : "") };
  }

  /* 새로 읽어 와서 화면에 알림 — app.js 는 storage 사건을 받으면 ZB.reload() 로 바꿔 끼우고 '전→후' 를 비교해 알림을 띄움 */
  async function refresh(){
    try{
      const d = await fetchAll(), sig = JSON.stringify(d);
      if(sig !== lastSig){   /* 바뀐 게 있을 때만 다시 그림 — 검색 칸에 글을 치는 중에 10초마다 지워지지 않게 */
        lastSig = sig; ZB._next(d);
        window.dispatchEvent(new StorageEvent("storage", { key: ZB.KEY }));
      }
      say(`${me.name || ""} · ${{ owner: "사장", manager: "매니저", staff: "직원" }[me.role] || ""} <button type="button" id="dev-out">로그아웃</button>`);
    }catch(e){ say("DB 읽기 실패: " + (e.message || e), true); }
  }

  /* ---------- 쓰기: 화면에서 바꾼 것 → DB ---------- */
  function push(label, fn){
    busy++;
    chain = chain.then(fn).then(() => refresh(), e => { say(`${label} 저장 실패: ${e.message || e} — 화면을 DB 기준으로 되돌립니다`, true); return refresh(); })
      .finally(() => { busy--; });
    return chain;
  }
  async function ensureCustomer(phone, name){
    const ph = digits(phone) || null;
    if(ph){ const f = await q(sb.from("customers").select("id").eq("store_id", sid).eq("phone", ph).maybeSingle()); if(f) return f.id; }
    const row = await q(sb.from("customers").insert({ store_id: sid, phone: ph, name: (name || "").trim() || null }).select("id").single());
    return row.id;
  }
  const wrap = (name, after) => { const orig = ZB[name]; ZB[name] = function(){ const out = orig.apply(ZB, arguments); after(out, arguments); return out; }; };
  const L = () => me.name || "매장 화면";

  wrap("add", (r) => push("예약", async () => {
    const cid = await ensureCustomer(r.phone, r.name);
    await q(sb.from("reservations").insert({ id: r.id, store_id: sid, customer_id: cid, visit_date: r.date, visit_time: r.time, people: r.people,
      status: resStatusDb(r.status), src: RES_SRC_DB[r.src] || "staff", memo: r.memo || null, pre_order: r.pre || null, created_by: L() }));
  }));
  wrap("update", (r, args) => { if(!r) return; const p = args[1] || {}, row = { updated_at: new Date().toISOString() };
    if(p.status) row.status = resStatusDb(p.status); if(p.date) row.visit_date = p.date; if(p.time) row.visit_time = p.time;
    if(p.people) row.people = p.people; if(p.memo != null) row.memo = p.memo || null; if(p.pre != null) row.pre_order = p.pre || null;
    if(p.waitNo){ const w = ZB.wait.list.filter(x => x.no === p.waitNo)[0];
      if(w) push("웨이팅 연결", async () => q(sb.from("waitlist").update({ reservation_id: r.id }).eq("id", w.id))); }
    if(Object.keys(row).length > 1) push("예약 변경", async () => q(sb.from("reservations").update(row).eq("id", r.id)));
  });
  wrap("waitAdd", (w, args) => push("웨이팅 등록", async () => {
    await q(sb.rpc("staff_wait_add", { p_store: sid, p_id: w.id, p_people: w.people, p_phone: digits(w.phone) || null, p_priority: !!args[3], p_reservation: null }));
  }));
  wrap("waitSet", (w, args) => { if(!w) return; const st = args[1], now = new Date().toISOString(), row = { status: st };
    if(st === "call"){ row.called_at = now; row.seated_at = null; row.ended_at = null; }
    else if(st === "wait"){ row.called_at = null; row.seated_at = null; row.ended_at = null; }
    else if(st === "in"){ row.seated_at = now; row.ended_at = now; }
    else { row.ended_at = now; }
    push("웨이팅 상태", async () => q(sb.from("waitlist").update(row).eq("id", w.id)));
  });
  wrap("waitOn", (o, args) => push("웨이팅 접수", async () => q(sb.from("store_features").upsert({ store_id: sid, feature: "wait", enabled: !!args[0] }))));
  wrap("addAcct", (a) => push("장부", async () => q(sb.from("ledger_accounts").insert({ id: a.id, store_id: sid, name: a.name, kind: a.kind === "개인" ? "person" : "company",
    contact: a.contact || null, phone: digits(a.phone) || null, memo: a.memo || null }))));
  wrap("addTx", (t) => push("장부 기록", async () => q(sb.from("ledger_tx").insert({ id: t.id, store_id: sid, account_id: t.acct, type: t.type, amount: t.amount,
    memo: t.memo || null, by_name: t.by || null, created_by: L() }))));
  wrap("voidTx", (t) => { if(t) push("장부 취소", async () => q(sb.from("ledger_tx").update({ voided_at: t.void ? new Date().toISOString() : null, voided_by: t.void ? L() : null }).eq("id", t.id))); });
  wrap("earn", (r, args) => push("적립", async () => {
    const agree = args[4] || {}, ph = digits(r.m.phone);
    let cid = null; const f = await q(sb.from("customers").select("id").eq("store_id", sid).eq("phone", ph).maybeSingle());
    if(f) cid = f.id;
    else { cid = (await q(sb.from("customers").insert({ id: r.m.id, store_id: sid, phone: ph, name: r.m.name || null, marketing: !!agree.mkt }).select("id").single())).id; }
    if(r.isNew) await q(sb.from("consents").insert([
      { store_id: sid, customer_id: cid, kind: "privacy", version: "2026-11-v1", agreed: true, via: agree.via || L() },
      { store_id: sid, customer_id: cid, kind: "marketing", version: "2026-11-v1", agreed: !!agree.mkt, via: agree.via || L() }]));
    await q(sb.from("point_tx").insert({ id: r.t.id, store_id: sid, customer_id: cid, type: "earn", pts: r.t.pts, pay_amount: r.t.amount,
      src: P_SRC_DB[r.t.src] || "staff", created_by: L() }));
    await q(sb.from("customers").update({ last_seen_at: new Date().toISOString() }).eq("id", cid));
  }));
  wrap("usePts", (t) => push("포인트 사용", async () => {
    await q(sb.from("point_tx").insert({ id: t.id, store_id: sid, customer_id: t.mem, type: "use", pts: t.pts, verify: HOW_DB[t.how] || null, created_by: L() }));
    await q(sb.from("customers").update({ last_seen_at: new Date().toISOString() }).eq("id", t.mem));
  }));
  wrap("voidPTx", (t) => { if(t) push("포인트 취소", async () => q(sb.from("point_tx").update({ voided_at: t.void ? new Date().toISOString() : null, voided_by: t.void ? L() : null }).eq("id", t.id))); });
  wrap("setCfg", () => push("설정", async () => q(sb.from("store_settings").update({ cfg: ZB.cfg, updated_at: new Date().toISOString() }).eq("store_id", sid))));
  wrap("setPending", (o, args) => push("계산대 금액", async () => args[0]
    ? q(sb.from("counter_pending").upsert({ store_id: sid, amount: args[0], created_by: L(), at: new Date().toISOString() }))
    : q(sb.from("counter_pending").delete().eq("store_id", sid))));
  wrap("setClosing", () => push("마감", async () => { const c = ZB.closing, today = await q(sb.rpc("biz_date", { p_store: sid }));
    return q(sb.from("day_closings").upsert({ store_id: sid, biz_date: today, pos_total: c.pos || 0, closed_at: c.done ? iso(c.done) : null, closed_by: c.done ? L() : null })); }));
  ZB.reset = function(){ alert("개발 DB 는 여기서 되돌리지 않습니다.\nSupabase SQL Editor 에서  select dev_reseed();  를 실행해 주세요."); return null; };

  /* ---------- 시작 ---------- */
  async function start(){
    const { data: { session } } = await sb.auth.getSession();
    if(!session) return loginForm();
    const uid = session.user.id;
    const staff = await q(sb.from("store_staff").select("store_id,role").eq("user_id", uid)).catch(() => []);
    if(!staff.length){ say("이 계정에 연결된 가게가 없습니다 — SQL Editor 에서 select dev_reseed(); 를 다시 실행하면 사장으로 연결됩니다", true); return; }
    sid = staff[0].store_id; me.role = staff[0].role;
    let prof = await q(sb.from("profiles").select("name").eq("user_id", uid).maybeSingle()).catch(() => null);
    if(!prof){ const nm = (session.user.email || "").split("@")[0]; await q(sb.from("profiles").insert({ user_id: uid, name: nm })).catch(() => {}); prof = { name: nm }; }
    me.name = prof.name || "";
    ZB.setDevice(me.name || "매장 화면");
    await refresh();
    clearInterval(timer);
    timer = setInterval(() => { if(!busy && !document.hidden) refresh(); }, 10000);
  }
  document.addEventListener("click", async e => {
    if(e.target && e.target.id === "dev-out"){ clearInterval(timer); await sb.auth.signOut(); location.reload(); }
  });

  const s = document.createElement("script"); s.src = LIB; s.crossOrigin = "anonymous";
  s.onload = () => { sb = window.supabase.createClient(SB_URL, SB_KEY, { auth: { persistSession: true, storageKey: "dineone-dev-auth" } }); start(); };
  s.onerror = () => say("Supabase 연결 파일을 불러오지 못했습니다(인터넷 확인)", true);
  document.head.appendChild(s);
})();
