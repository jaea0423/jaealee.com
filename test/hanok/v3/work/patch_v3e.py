"""v3 5차 — 시각 선택을 30분 단위로.
   1시간 칸이면 '오후 7시' 칸 하나에 7:00 과 7:30 의 사정이 섞여 어느 쪽이 안 되는지 안 보였습니다.
   30분 칸마다 경고를 따로 계산해 보여 주고, 분 조절은 그 칸 안(정각 칸 00~25, 30분 칸 30~55)에서만 움직입니다."""
import os, sys, io
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "index.html")
s = io.open(SRC, encoding="utf-8").read()
n_ok = 0
def rep(old, new, count=1):
    global s, n_ok
    c = s.count(old)
    if c != count:
        print("!! 치환 실패 (%d번 발견, %d번 기대):\n%s" % (c, count, old[:200])); sys.exit(1)
    s = s.replace(old, new); n_ok += 1

rep('''  /* 영업시간 안에서 시각 후보 생성 */
  const dh = hoursFor(WZ.date);
  const oh = parseInt(dh.open.split(":")[0]), ch = Math.ceil(toMin(dh.close)/60);
  const hours = [];
  for(let h=oh; h<ch; h++) hours.push(h);
  const curH = WZ.time ? parseInt(WZ.time.split(":")[0]) : null;
  const curM = WZ.time ? parseInt(WZ.time.split(":")[1]) : 0;

  const lastBook = lastBookMin(WZ.date);
  const isToday = WZ.date===todayStr();
  const isPastDate = WZ.date < todayStr();
  const nowM = toMin(nowHM());
  const hourCells = hours.map(h=>{
    const n = s.reservations.filter(r=>r.date===WZ.date && r.status==="확정" && parseInt(r.time)===h).length;
    const late = h*60 > lastBook;
    /* 이 시각을 고르면 경고가 생기는지 미리 확인합니다 */
    const probe = timeWarn(WZ.date, pad(h)+":00");
    /* 지난 시각도 누를 수는 있게 — 예약 누락을 나중에 입력하는 경우가 있습니다 */
    const gone = isPastDate || (isToday && (h+1)*60 <= nowM);
    /* 브레이크타임에 걸리는 시각은 따로 표시 */
    const brk = dh.bs && dh.be && h*60 >= toMin(dh.bs) && h*60 < toMin(dh.be);
    const bad = !!probe;
    /* 경고가 걸리는 시각은 작은 표시만이 아니라 시각 글자까지 벽돌색 — 눈이 먼저 가야 하는 칸입니다 */
    const red = (bad || brk) ? " rust" : "";
    return `<button class="hcell ${curH===h?'on':''} ${bad?'late warned':''} ${gone?'gone':''}" onclick="wzPickHour(${h})">
      <span class="ap${red}">${h<12?"오전":"오후"}</span>
      <span class="hh${red}">${h%12===0?12:h%12}시</span>
      ${brk?`<span class="hn rust">브레이크</span>`
           :bad?`<span class="hn rust">${esc(shortWarn(probe))}</span>`
           :gone?`<span class="hn muted2">지난 시간</span>`
           :(n?`<span class="hn">${n}건</span>`:"")}
    </button>`;
  }).join("");

  /* 분 조절은 시각을 고르기 전에도 자리를 지킵니다(.idle) — 시각을 누르는 순간 레일이 생기며 화면이 내려앉지 않게 */
  const minuteRail = `
    <div class="mwrap ${curH===null?'idle':''}">
      <div class="mhead"><span class="lbl">분</span><span class="mnow">${curH===null?"시를 먼저 고르세요":hm(WZ.time)}</span></div>
      <div class="mrail" id="mrail">
        <div class="mtrack"></div>
        <div class="mfill" style="width:${(curM/55)*100}%"></div>
        ${[0,5,10,15,20,25,30,35,40,45,50,55].map(v=>
          `<span class="mnotch ${v%10===0?'big':''}" style="left:${(v/55)*100}%"></span>`).join("")}
        <div class="mknob" style="left:${(curM/55)*100}%">${pad(curM)}</div>
        ${[0,10,20,30,40,50].map(v=>
          `<button class="mtick ${curM===v?'on':''}" style="left:${(v/55)*100}%" onclick="wzPickMin(${v})">${pad(v)}</button>`).join("")}
      </div>
      <div class="mfine">
        <button ${curM<=0?"disabled":""} onclick="wzNudge(-5)">− 5분</button>
        <button ${curM>=55?"disabled":""} onclick="wzNudge(5)">＋ 5분</button>
      </div>
    </div>`;''',
'''  /* 영업시간 안에서 30분 단위 시각 후보 생성 (11:00, 11:30, … 마감 전까지).
     1시간 칸이면 7:00 과 7:30 의 사정(라스트오더·브레이크)이 한 칸에 섞여 어느 쪽이 안 되는지 안 보였습니다 */
  const dh = hoursFor(WZ.date);
  const slots = [];
  for(let t = Math.floor(toMin(dh.open)/30)*30; t < toMin(dh.close); t += 30) slots.push(t);
  const curT = WZ.time ? toMin(WZ.time) : null;
  const curSlot = curT===null ? null : Math.floor(curT/30)*30;   /* 고른 시각이 속한 30분 칸 */
  const base = curSlot===null ? 0 : curSlot%60;                  /* 분 레일의 시작(0 또는 30) */
  const off = curT===null ? 0 : curT - curSlot;                  /* 칸 안에서의 분 (0~25) */

  const isToday = WZ.date===todayStr();
  const isPastDate = WZ.date < todayStr();
  const nowM = toMin(nowHM());
  const slotCells = slots.map(t=>{
    const h = Math.floor(t/60), m = t%60;
    const n = s.reservations.filter(r=>r.date===WZ.date && r.status==="확정" && Math.floor(toMin(r.time)/30)*30===t).length;
    /* 이 칸을 고르면 경고가 생기는지 미리 확인합니다 */
    const probe = timeWarn(WZ.date, minToHM(t));
    /* 지난 시각도 누를 수는 있게 — 예약 누락을 나중에 입력하는 경우가 있습니다 */
    const gone = isPastDate || (isToday && t+30 <= nowM);
    /* 브레이크타임에 걸리는 칸은 따로 표시 */
    const brk = dh.bs && dh.be && t >= toMin(dh.bs) && t < toMin(dh.be);
    const bad = !!probe;
    /* 경고가 걸리는 시각은 작은 표시만이 아니라 시각 글자까지 벽돌색 — 눈이 먼저 가야 하는 칸입니다 */
    const red = (bad || brk) ? " rust" : "";
    return `<button class="hcell ${curSlot===t?'on':''} ${bad?'late warned':''} ${gone?'gone':''} ${brk?'brk':''}" onclick="wzPickSlot(${t})">
      <span class="ap${red}">${h<12?"오전":"오후"}</span>
      <span class="hh${red}">${h%12===0?12:h%12}:${pad(m)}</span>
      ${brk?`<span class="hn rust">브레이크</span>`
           :bad?`<span class="hn rust">${esc(shortWarn(probe))}</span>`
           :gone?`<span class="hn muted2">지난 시간</span>`
           :(n?`<span class="hn">${n}건</span>`:`<span class="hn">&nbsp;</span>`)}
    </button>`;
  }).join("");

  /* 분 조절은 고른 30분 칸 안에서만 움직입니다 — 정각 칸이면 00~25, 30분 칸이면 30~55.
     시각을 고르기 전에도 자리를 지킵니다(.idle) — 누르는 순간 레일이 생기며 화면이 내려앉지 않게 */
  const pct = v => (v/25)*100;
  const minuteRail = `
    <div class="mwrap ${curSlot===null?'idle':''}">
      <div class="mhead"><span class="lbl">분</span><span class="mnow">${curSlot===null?"시각을 먼저 고르세요":hm(WZ.time)}</span></div>
      <div class="mrail" id="mrail">
        <div class="mtrack"></div>
        <div class="mfill" style="width:${pct(off)}%"></div>
        ${[0,5,10,15,20,25].map(v=>
          `<span class="mnotch ${v%10===0?'big':''}" style="left:${pct(v)}%"></span>`).join("")}
        <div class="mknob" style="left:${pct(off)}%">${pad(base+off)}</div>
        ${[0,5,10,15,20,25].map(v=>
          `<button class="mtick ${off===v?'on':''}" style="left:${pct(v)}%" onclick="wzPickMin(${v})">${pad(base+v)}</button>`).join("")}
      </div>
      <div class="mfine">
        <button ${off<=0?"disabled":""} onclick="wzNudge(-5)">− 5분</button>
        <button ${off>=25?"disabled":""} onclick="wzNudge(5)">＋ 5분</button>
      </div>
    </div>`;''')

rep('''      <div class="lbl" style="margin-bottom:8px">${WZ.date?dateLabel(WZ.date):"날짜를 먼저 고르세요"} · 시</div>
      <div class="hgrid">${hourCells}</div>''',
'''      <div class="lbl" style="margin-bottom:8px">${WZ.date?dateLabel(WZ.date):"날짜를 먼저 고르세요"} · 시각</div>
      <div class="hgrid">${slotCells}</div>''')

rep('''function wzPickHour(h){
  const cur = WZ.time ? parseInt(WZ.time.split(":")[1]) : 0;
  WZ.time = pad(h)+":"+pad(cur); render();
}
function wzPickMin(m){
  const h = WZ.time ? parseInt(WZ.time.split(":")[0]) : 18;
  WZ.time = pad(h)+":"+pad(m); render();
}
function wzNudge(d){
  if(!WZ.time) return;
  const [h,m]=WZ.time.split(":").map(Number);
  /* 분만 조절 — 시(時)는 위 타일에서 바꾸도록 0~55분으로 묶습니다 */
  const next = Math.min(55, Math.max(0, m + d));
  if(next===m) return;
  WZ.time = pad(h)+":"+pad(next); render();
}''',
'''/* 30분 칸을 고르면 그 칸의 시작 시각(정각 또는 30분)이 됩니다. 세부 분은 아래 레일에서 */
function wzPickSlot(t){ WZ.time = minToHM(t); render(); }
/* 레일의 분(0~25)을 칸 시작에 더한 시각 */
function wzSlotBase(){ return WZ.time ? Math.floor(toMin(WZ.time)/30)*30 : 18*60; }
function wzPickMin(v){
  WZ.time = minToHM(wzSlotBase() + Math.min(25, Math.max(0, v))); render();
}
function wzNudge(d){
  if(!WZ.time) return;
  const base = wzSlotBase(), off = toMin(WZ.time) - base;
  /* 칸 안(0~25분)에서만 — 칸을 바꾸는 것은 위 타일에서 */
  const next = Math.min(25, Math.max(0, off + d));
  if(next===off) return;
  WZ.time = minToHM(base + next); render();
}''')

rep('''    const v = Math.min(55, Math.max(0, Math.round((x/r.width)*55/5)*5));   /* 5분 단위, 0~55분 */
    const h = WZ.time ? parseInt(WZ.time.split(":")[0]) : 18;
    const nt = pad(h)+":"+pad(v);
    if(nt!==WZ.time){ WZ.time = nt; render(); }''',
'''    const v = Math.min(25, Math.max(0, Math.round((x/r.width)*25/5)*5));   /* 5분 단위, 칸 안 0~25분 */
    const nt = minToHM(wzSlotBase() + v);
    if(nt!==WZ.time){ WZ.time = nt; render(); }''')

# ---------- CSS: 칸이 두 배가 됐으니 칸을 낮고 촘촘하게, 브레이크 칸은 흐리게 ----------
rep('''/* ---- 타임라인: 블록은 애플 진회색, 지난 것은 밝은 회색 ---- */''',
'''/* ---- 30분 단위 시각 칸: 칸이 두 배라 낮고 촘촘하게. 브레이크 칸은 지난 시간처럼 흐리게 (누를 수는 있음) ---- */
.hgrid{grid-template-columns:repeat(auto-fill,minmax(88px,1fr)); gap:var(--s8)}
.hcell{padding:var(--s8) var(--s4) var(--s8); gap:0; min-height:64px}
.hcell .ap{line-height:16px}
.hcell .hh{font-size:var(--fs-title); line-height:24px; font-variant-numeric:tabular-nums}
.hcell .hn{line-height:16px; min-height:16px}
.hcell.brk{opacity:.45; background:var(--surface-2)}
.hcell.brk.on{opacity:1}
@media (min-width:900px){ .hgrid{grid-template-columns:repeat(4,1fr)} .hcell{padding:var(--s8) var(--s4)} .hcell .hh{font-size:var(--fs-title)} }
@media (min-width:1280px){ .hgrid{grid-template-columns:repeat(4,1fr)} }
@media (max-height:820px) and (min-width:900px){ .hcell{min-height:56px} }
/* ---- 타임라인: 블록은 애플 진회색, 지난 것은 밝은 회색 ---- */''')

io.open(SRC, "w", encoding="utf-8", newline="\n").write(s)
print("5차 패치 완료:", n_ok, "곳")
