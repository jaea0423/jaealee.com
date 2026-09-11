/* 개인 시작 페이지: 프레임워크 없이 동작하도록 화면과 외부 데이터 처리를 분리합니다. */
async function fetchWithTimeout(url, options = {}) {
  // 응답이 없는 제공처 때문에 전체 시세 표시가 끝없이 대기하지 않도록 제한합니다.
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  try {
    const response = await fetch(url, {...options, signal:controller.signal});
    if (!response.ok) throw new Error('Provider response: ' + response.status);
    return response;
  } finally { clearTimeout(timeout); }
}
function readTheme() { try { return localStorage.getItem('dark'); } catch { return null; } }
function applyTheme(dark) {
  document.body.classList.toggle('light', !dark);
  document.getElementById('darkBtn').setAttribute('aria-pressed', String(dark));
  document.getElementById('darkBtn').setAttribute('aria-label', dark ? '밝은 테마로 변경' : '어두운 테마로 변경');
}
function toggleDark() {
  const dark = document.body.classList.contains('light');
  applyTheme(dark);
  // 다른 개인 페이지와 사용하던 테마 키를 유지합니다.
  try { localStorage.setItem('dark', String(dark)); } catch {}
}
applyTheme(readTheme() !== 'false');
function tickClock() {
  const now = new Date();
  document.getElementById('clock').textContent = new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Seoul',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).format(now);
  document.getElementById('todayLabel').textContent = new Intl.DateTimeFormat('ko-KR',{timeZone:'Asia/Seoul',year:'numeric',month:'long',day:'numeric',weekday:'long'}).format(now);
}
tickClock(); setInterval(tickClock, 30000);
const engines = {g:['Google','https://www.google.com/search?q='],n:['Naver','https://search.naver.com/search.naver?query='],y:['YouTube','https://www.youtube.com/results?search_query=']};
let selectedEngine = 'g';
const engineButtons = [...document.querySelectorAll('[data-engine]')];
function selectEngine(button) {
  selectedEngine = button.dataset.engine;
  engineButtons.forEach(el => { const active = el === button; el.classList.toggle('selected',active); el.setAttribute('aria-selected',String(active)); el.tabIndex = active ? 0 : -1; });
  document.getElementById('searchForm').setAttribute('aria-labelledby', button.id);
  document.querySelector('label[for="searchInput"]').textContent = engines[selectedEngine][0] + ' 검색어';
}
engineButtons.forEach((button,index) => {
  button.addEventListener('click',() => selectEngine(button));
  button.addEventListener('keydown',event => {
    if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
    event.preventDefault();
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? 2 : (index + (event.key === 'ArrowRight' ? 1 : 2)) % 3;
    selectEngine(engineButtons[next]); engineButtons[next].focus();
  });
});
document.getElementById('searchForm').addEventListener('submit',event => {
  event.preventDefault();
  const input = document.getElementById('searchInput'); const query = input.value.trim();
  if (!query) return;
  input.value = ''; input.blur();
  window.location.href = engines[selectedEngine][1] + encodeURIComponent(query);
});
window.addEventListener('pageshow',() => { document.getElementById('searchInput').value = ''; });
function toggleQuick() {
  const grid = document.getElementById('quickGrid'); grid.hidden = !grid.hidden;
  const button = document.getElementById('quickBtn'); button.setAttribute('aria-expanded',String(!grid.hidden));
  button.innerHTML = grid.hidden ? '펼치기 <span aria-hidden="true">+</span>' : '접기 <span aria-hidden="true">−</span>';
}

/* ── 날씨 (Open-Meteo, 춘천) ── */
const WX = [
  {max:0,  icon:'☀️',  desc:'맑음',     cls:'wx-sunny'},
  {max:2,  icon:'⛅',  desc:'구름 조금', cls:'wx-cloudy'},
  {max:3,  icon:'☁️',  desc:'흐림',      cls:'wx-overcast'},
  {max:49, icon:'🌫️', desc:'안개',       cls:'wx-fog'},
  {max:67, icon:'🌧️', desc:'비',         cls:'wx-rain'},
  {max:77, icon:'❄️',  desc:'눈',        cls:'wx-snow'},
  {max:82, icon:'🌦️', desc:'소나기',     cls:'wx-rain'},
  {max:99, icon:'⛈️',  desc:'뇌우',      cls:'wx-thunder'},
];
function wxInfo(code){
  for(const w of WX) if(code<=w.max) return w;
  return WX[WX.length-1];
}

async function fetchWeather(){
  try{
    const res = await fetchWithTimeout(
      'https://api.open-meteo.com/v1/forecast' +
      '?latitude=37.8813&longitude=127.7298' +
      '&current=temperature_2m,weathercode' +
      '&hourly=temperature_2m,weathercode' +
      '&daily=temperature_2m_max,temperature_2m_min' +
      '&timezone=Asia%2FSeoul&forecast_days=2'
    );
    const d = await res.json();

    /* 현재 날씨 */
    const temp = Math.round(d.current.temperature_2m);
    const code = d.current.weathercode;
    const w    = wxInfo(code);

    /* 최저/최고 */
    const tmax = Math.round(d.daily.temperature_2m_max[0]);
    const tmin = Math.round(d.daily.temperature_2m_min[0]);

    /* 배너 */
    const banner = document.getElementById('wxBanner');
    banner.className = 'wx-banner ' + w.cls;
    document.getElementById('wxIcon').textContent  = w.icon;
    document.getElementById('wxTemp').textContent  = temp + '°';
    document.getElementById('wxDesc').textContent  = w.desc;
    document.getElementById('wxMinMax').textContent = `최저 ${tmin}° / 최고 ${tmax}°　춘천`;

    /* 시간대별 (현재 시각부터 8시간) */
    const now    = new Date();
    const nowH = Number(new Intl.DateTimeFormat('en-GB', {timeZone:'Asia/Seoul', hour:'2-digit', hourCycle:'h23'}).format(now));
    const times  = d.hourly.time;       /* "2026-04-15T00:00" 형식 */
    const hTemps = d.hourly.temperature_2m;
    const hCodes = d.hourly.weathercode;

    /* 현재 시간 인덱스 찾기 */
    const seoulDate = new Intl.DateTimeFormat('en-CA', {timeZone:'Asia/Seoul', year:'numeric', month:'2-digit', day:'2-digit'}).format(now);
    let startIdx = times.findIndex(t => t >= seoulDate + 'T' + String(nowH).padStart(2,'0') + ':00');
    if(startIdx < 0) startIdx = 0;

    const hourlyEl = document.getElementById('wxHourly');
    hourlyEl.innerHTML = '';

    /* 2시간 간격으로 8칸 표시 */
    for(let i = 0; i < 8; i++){
      const idx = startIdx + i * 2;
      if(idx >= times.length) break;
      const hh   = parseInt(times[idx].split('T')[1]);
      const ampm = hh < 12 ? '오전' : '오후';
      const h12  = hh % 12 === 0 ? 12 : hh % 12;
      const hw   = wxInfo(hCodes[idx]);
      const ht   = Math.round(hTemps[idx]);

      const el = document.createElement('div');
      el.className = 'wx-hour';
      el.innerHTML = `
        <div class="wx-hour-time">${ampm}<br>${h12}시</div>
        <div class="wx-hour-icon">${hw.icon}</div>
        <div class="wx-hour-temp">${ht}°</div>
      `;
      hourlyEl.appendChild(el);
    }

  } catch(e){
    /* 네트워크/API 실패 시 배너에 안내만 표시 (없는 요소 참조 금지) */
    document.getElementById('wxDesc').textContent = '날씨 정보를 불러오지 못했습니다';
  }
}
fetchWeather();
setInterval(() => { if (!document.hidden) fetchWeather(); }, 600000);


/* 기존 시세 제공처 및 관심 종목 */

(function(){
  /* ▼▼▼ 여기에 Finnhub 무료 API 키를 붙여넣으세요 ▼▼▼
     (비워두면 미국 주식은 '키 필요'로만 표시됩니다. BTC·환율은 키 없이 동작)
     발급: finnhub.io 무료 가입 → Dashboard의 API key 복사 */
  const FINNHUB_KEY = "d9h30ohr01qhv00ki5dgd9h30ohr01qhv00ki5e0";
  /* ▲▲▲ 키 교체 시 이 따옴표 안 값만 바꾸면 됩니다 ▲▲▲ */

  // 표시 항목 (왼→오 순서). type: fx=환율 / btc=비트코인 / stock=미국주식
  const ITEMS = [
    {type:'fx',    id:'USDKRW', label:'USD/KRW'},
    {type:'btc',   id:'KRW-BTC',label:'BTC'},
    {type:'stock', id:'SOXL',   label:'SOXL'},
    {type:'stock', id:'QQQ',    label:'QQQ'},
    {type:'stock', id:'TQQQ',   label:'TQQQ'},
    {type:'stock', id:'SPY',    label:'SPY'},
    {type:'stock', id:'TSLA',   label:'TSLA'},
    {type:'stock', id:'NVDA',   label:'NVDA'},
    {type:'stock', id:'PLTR',   label:'PLTR'},
    {type:'stock', id:'AAPL',   label:'AAPL'},
    {type:'stock', id:'SPCX',   label:'SPCX'},
  ];

  const store = {};        // id -> 시세 데이터 저장소
  let marketLive = false;  // 미국장 실시간 여부
  let frozenRounds = 0;    // (보조) 전 종목 가격 고정 연속 횟수
  let lastStockSig = null; // 직전 주가 스냅샷 비교용

  /* ── 미국 정규장(9:30~16:00 ET) 개장 여부. 서머타임 자동 반영 ── */
  function marketClockOpen(){
    const now = new Date();
    const wd = new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',weekday:'short'}).format(now);
    if(wd==='Sat'||wd==='Sun') return false;                 // 주말 휴장
    const hm = new Intl.DateTimeFormat('en-US',
      {timeZone:'America/New_York',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).format(now);
    const [h,m] = hm.split(':').map(Number);
    const mins = h*60 + m;
    return mins >= 570 && mins < 960;                         // 570=09:30, 960=16:00
  }

  /* ── 숫자 포맷 ── */
  const fmtKRW = n => '₩' + Math.round(n).toLocaleString('ko-KR');
  const fmtUSD = n => '$' + n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
  const fmtFX  = n => n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
  const fmtPct = p => (p>0?'+':'') + p.toFixed(2) + '%';
  const arrow  = d => d==='up' ? '▲' : d==='down' ? '▼' : '·';   // 방향 화살표
  const dirOf  = v => v>0 ? 'up' : v<0 ? 'down' : 'flat';        // 등락 방향

  /* ── 환율 USD→KRW (키 없는 무료 API, 실패 시 대체 API) ── */
  async function updateFX(){
    let rate = null;
    try{                                   // 1순위: open.er-api.com
      const d = await (await fetchWithTimeout('https://open.er-api.com/v6/latest/USD')).json();
      if(d && d.rates && d.rates.KRW) rate = d.rates.KRW;
    }catch(e){}
    if(rate === null){                     // 2순위: frankfurter.app
      try{
        const d = await (await fetchWithTimeout('https://api.frankfurter.app/latest?from=USD&to=KRW')).json();
        if(d && d.rates && d.rates.KRW) rate = d.rates.KRW;
      }catch(e){}
    }
    if(rate !== null){
      const prev = store['USDKRW'] ? store['USDKRW'].price : rate;   // 직전 값과 비교해 등락 방향
      store['USDKRW'] = {price:rate, chg:rate-prev, ok:true};
    }else if(!store['USDKRW']){
      store['USDKRW'] = {ok:false};
    }
  }

  /* ── 비트코인 KRW (업비트, 24시간) ── */
  async function updateBTC(){
    try{
      const d = await (await fetchWithTimeout('https://api.upbit.com/v1/ticker?markets=KRW-BTC')).json();
      const t = d[0];
      // signed_change_rate: 전일 대비 등락률(소수). ×100 해서 % 로
      store['KRW-BTC'] = {price:t.trade_price, pct:t.signed_change_rate*100, ok:true};
    }catch(e){
      if(!store['KRW-BTC']) store['KRW-BTC'] = {ok:false};
    }
  }

  /* ── 미국 주식 (Finnhub) ── */
  async function updateStocks(){
    const syms = ITEMS.filter(i=>i.type==='stock').map(i=>i.id);
    if(!FINNHUB_KEY){                       // 키 없으면 '키 필요' 상태만 세팅
      syms.forEach(s => store[s] = {nokey:true});
      return;
    }
    await Promise.all(syms.map(async sym => {
      try{
        const d = await (await fetchWithTimeout(`https://finnhub.io/api/v1/quote?symbol=${sym}&token=${FINNHUB_KEY}`)).json();
        // c=현재가, dp=등락률(%), t=마지막 체결 시각(unix 초)
        if(d && typeof d.c === 'number' && d.c > 0){
          store[sym] = {price:d.c, pct:(typeof d.dp==='number'?d.dp:0), t:d.t||0, ok:true};
        }else if(!store[sym]){
          store[sym] = {ok:false};
        }
      }catch(e){
        if(!store[sym]) store[sym] = {ok:false};
      }
    }));
    computeMarketLive();
  }

  /* ── 장중 / 휴장 판정 ──
     주 방법: 마지막 체결 시각(t)이 최근인지 → 최근 체결이 있으면 살아있음
     보조 방법: t가 없을 때, 전 종목 가격이 3번 연속 완전히 고정이면 휴장 간주 */
  function computeMarketLive(){
    if(!marketClockOpen()){ marketLive = false; frozenRounds = 0; return; }  // 시계상 장 밖
    const stocks = ITEMS.filter(i=>i.type==='stock').map(i=>store[i.id]).filter(s=>s && s.ok);
    if(stocks.length === 0){ marketLive = false; return; }
    const haveT = stocks.every(s => s.t && s.t > 0);
    if(haveT){
      const nowSec = Date.now()/1000;
      marketLive = stocks.some(s => (nowSec - s.t) < 600);   // 10분 내 체결 있으면 장중
      frozenRounds = 0;
    }else{
      const sig = stocks.map(s => s.price).join(',');        // 가격 스냅샷
      if(sig === lastStockSig) frozenRounds++; else frozenRounds = 0;
      lastStockSig = sig;
      marketLive = frozenRounds < 3;                         // 3번 연속 고정이면 휴장
    }
  }

  /* ── 화면 그리기 ── */
  function render(){
    const inner = document.getElementById('tkInner');
    if(!inner) return;
    inner.innerHTML = '';
    ITEMS.forEach(it => {
      const s  = store[it.id];
      const el = document.createElement('a');       // 클릭 시 토스증권으로 이동
      el.href = 'https://www.tossinvest.com';
      el.className = 'tk';
      let priceHtml = '<span class="tk-price">—</span>', chgHtml = '', extra = '';

      if(it.type === 'fx'){
        if(s && s.ok){
          const d = dirOf(s.chg);
          priceHtml = `<span class="tk-price">${fmtFX(s.price)}</span>`;
          chgHtml   = `<span class="tk-chg ${d}">${arrow(d)}</span>`;   // 환율은 화살표만
        }
      }else if(it.type === 'btc'){
        if(s && s.ok){
          const d = dirOf(s.pct);
          priceHtml = `<span class="tk-price">${fmtKRW(s.price)}</span>`;
          chgHtml   = `<span class="tk-chg ${d}">${arrow(d)} ${fmtPct(s.pct)}</span>`;
        }
      }else{ // stock
        if(s && s.nokey){
          priceHtml = `<span class="tk-price" style="color:var(--txt-l)">—</span>`;
          extra = `<span class="tk-tag">키 필요</span>`;
        }else if(s && s.ok){
          const d = dirOf(s.pct);
          priceHtml = `<span class="tk-price">${fmtUSD(s.price)}</span>`;
          chgHtml   = `<span class="tk-chg ${d}">${arrow(d)} ${fmtPct(s.pct)}</span>`;
          if(marketLive){ extra = `<span class="tk-dot" title="최근 체결 정보"></span>`; }  // 장중: 빨간 점
          else{ el.className = 'tk closed'; extra = `<span class="tk-tag">최근값</span>`; } // 마감: 흐림+종가
        }
      }
      el.innerHTML = `<span class="tk-name">${it.label}</span>${priceHtml}${chgHtml}${extra}`;
      if (!s || (!s.ok && !s.nokey)) { const state = document.createElement('span'); state.className = 'tk-tag'; state.textContent = s ? '연결 확인' : '불러오는 중'; el.appendChild(state); }
      inner.appendChild(el);
    });
  }

  /* ── 갱신 루프 (1분 주기) ── */
  let tick = 0;
  async function refresh(){
    tick++;
    const clockOpen = marketClockOpen();
    const jobs = [updateFX(), updateBTC()];
    // 주식: 장중이면 매분 / 장 밖이면 5분마다 심박(재개·휴장복구 감지용)
    const doStocks = (tick === 1) || clockOpen || (tick % 5 === 0);
    if(doStocks) jobs.push(updateStocks());
    await Promise.all(jobs);
    if(!doStocks) computeMarketLive();   // 미갱신 틱에도 상태는 최신화
    render();
  }
  refresh();
  setInterval(() => { if (!document.hidden) refresh(); }, 60000);
})();
