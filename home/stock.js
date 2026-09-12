/* 공개용으로 선별한 관찰 요약만 읽습니다. 키·계좌·원문 로그·주문 기능 없음. */
(() => {
  const root=document.getElementById('panel-stock'); if(!root)return;
  const $=id=>document.getElementById('stock-'+id);
  const esc=v=>String(v??'—').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fmt=(v,d=0)=>typeof v==='number'&&Number.isFinite(v)?v.toLocaleString('ko-KR',{maximumFractionDigits:d,minimumFractionDigits:d}):'—';
  const sign=v=>v>0?'+':''; const cls=v=>v>0?'stock-up':v<0?'stock-down':'';
  // 설정 전에는 네트워크 요청이 없습니다. 실제 HTTPS 서버 연결은 별도 작업입니다.
  const STATE_URL='/home/stock-state.json';
  const designPreview=root.dataset.designPreview==='true';

  let demo=designPreview,market='KR',chartKind='price',candle=true,percent=false,logKind='decisions',chart=null,state=null,busy=false,manualMarket=false;
  const names=[['원 / 달러','KRW',1372.45,.24],['코스피','INDEX',2684.32,-.38],['비트코인','업비트 · KRW',92345000,1.42],['나스닥100','QQQ · ETF',482.36,.85],['S&P 500','SPY · ETF',563.12,.46],['다우존스','DIA · ETF',414.26,-.13],['반도체','SOXX · ETF',231.78,1.26],['금','GLD · ETF',237.15,.32],['원유','USO · ETF',72.64,-.78],['달러','UUP · ETF',28.45,.18]];
  const series=Array.from({length:49},(_,i)=>Math.round(10000+i*5+Math.sin(i*.64)*42+Math.cos(i*.23)*29));
  const demoData=()=>({label:market==='KR'?'한빛테크 · 가상 종목':'Example Tech · 가상 종목',price:market==='KR'?10280:128.5,change:2.8,cash:market==='KR'?1000000:1000,holdings:0,today:0,total:0,fees:0,verdict:'판단 보류',reason:'기업 발표는 확인했지만 가격 반영과 최신 공시를 더 확인해야 합니다.',series:series.map(v=>market==='KR'?v:v/80),trades:[],decisions:[['09:12','판단 보류','가격 반영과 최신 공시가 확인되지 않았습니다.'],['09:10','근거 확인','원문과 인용 문구를 대조했습니다.'],['08:35','자료 수집','예시 자료 묶음의 중복 기사를 제외했습니다.']],logs:[['09:12','OBSERVE','신규 진입 없음 · 예시'],['09:10','SOURCE','원문 대조 완료 · 예시'],['08:35','COLLECT','자료 수집 완료 · 예시']]});
  function data(){return demo?demoData():(state?.markets?.[market]||{});}
  function render(){
    const d=data(),unit=market==='KR'?'원':'USD';
    $('mode-note').textContent=demo?'화면 미리보기 · 아래 숫자와 기록은 모두 가상 예시입니다.':'공개 관찰 기록 · 자동 매매 미가동 · 실제 주문 없음';
    $('demo-toggle').textContent=demo?'예시 끄기':'예시 보기';
    $('market-time').textContent=demo?'예시 · 실시간 시세 아님':state?.market_updated_at?new Date(state.market_updated_at).toLocaleString('ko-KR'):'시세 연결 대기';
    $('markets').innerHTML=names.map(([name,ticker,value,change],i)=>{const m=demo?{value,change}:state?.overview?.[i]||{};return `<div class="stock-market-item"><p>${esc(name)}<small>${esc(ticker)}</small></p><strong>${fmt(m.value,i===2?0:2)}</strong><em class="${cls(m.change)}">${typeof m.change==='number'?(m.change>=0?'▲ ':'▼ ')+fmt(Math.abs(m.change),2)+'%':'확인 대기'}</em></div>`;}).join('');
    const stats=[['예수금',d.cash,unit,'가상 계좌'],['보유 종목',d.holdings,'개','추가 매수 강제 없음'],['금일 실현손익',d.today,unit,'매도 완료분 기준'],['누적 실현손익',d.total,unit,'미실현 손익 별도'],['누적 수수료',d.fees,unit,'체결 자료 기준']];
    $('stats').innerHTML=stats.map(([label,value,suffix,note],i)=>`<div class="stock-stat"><p>${esc(label)}</p><strong class="${i===2||i===3?cls(value):''}">${i===2||i===3?sign(value):''}${fmt(value,market==='US'&&i!==1?2:0)} <span style="font-size:11px">${esc(suffix)}</span></strong><small>${esc(note)}</small></div>`).join('');
    $('evidence-text').textContent=demo?'가상 예시 · 기업 발표 원문 대조':d.evidence||'근거 자료 연결 대기';$('unknown-text').textContent=demo?'가상 예시 · 최신 공시와 가격 반영 확인 필요':(d.unknowns||[]).join(' · ')||'미확인 항목 연결 대기';
    $('verdict').textContent=d.verdict||'아직 판단 기록이 없습니다';$('reason').textContent=d.reason||'연결되지 않은 자료를 정상 상태로 표시하지 않습니다.';
    $('risk').textContent='● '+(demo?'신규 진입 보류':'위험 판정 확인 대기');
    root.querySelectorAll('[data-stock-market]').forEach(b=>{const selected=b.dataset.stockMarket===market;b.setAttribute('aria-selected',selected);b.tabIndex=selected?0:-1;b.querySelector('span').textContent=b.dataset.stockMarket==='US'?'준비 중':demo?'예시':state?.markets?.KR?.session_label||'확인 대기';});
    $('market-panel').setAttribute('aria-labelledby','stock-tab-'+market);
    $('session').textContent=demo?'예시 화면 · 장중 여부를 추정하지 않습니다':d.session_label?`${d.session_label} · ${d.session_hours||'거래 시간 확인 대기'}`:'거래 시간은 서버 캘린더 연결 후 표시';
    $('chart-label').textContent=chartKind==='price'?(d.label?d.label+(demo?' | 5분봉 · 09:00–13:00 KST · KRW':' | 가격 자료 미연결'):'종목·기간·통화 확인 대기'):'누적 수익 · '+(demo?'가상 계좌':'관찰 계좌');
    $('chart-price').textContent=chartKind==='price'?fmt(d.price,market==='US'?2:0)+' '+unit:demo?(percent?'0.00%':'0 '+unit):'—';
    $('chart-change').textContent=chartKind==='price'&&typeof d.change==='number'?`${sign(d.change)}${fmt(d.change,2)}%`:'';$('chart-change').className=cls(d.change);
    $('chart-caption').textContent=demo?'가상 데이터 · 투자 성과 아님':'원본 데이터 시각 기준';
    $('chart-unit').textContent=chartKind==='price'?(candle?'직선 라인으로 전환':'캔들로 전환'):(percent?'금액으로 전환':'%로 전환');
    $('chart-explainer').textContent=chartKind==='price'?(demo?'관찰 종목의 가격 · 5분마다 시가·고가·저가·종가 표시 · 빨강 상승 / 파랑 하락 · 전부 가상 예시':'원본 OHLC·시각·봉 간격 연결 전입니다.'):'계좌의 누적 손익입니다. 종목 가격 차트와 다릅니다. 거래가 없으면 수익은 0입니다.';
    const trades=d.trades||[];$('trade-count').textContent=trades.length?'· '+trades.length+'건':'';
    $('trades').innerHTML=trades.length?trades.slice(0,40).map(t=>`<tr><td>${esc(t.time)}</td><td class="${t.side==='BUY'?'stock-up':'stock-down'}">${t.side==='BUY'?'매수':'매도'}</td><td>${esc(t.name)}</td><td>${fmt(t.price,market==='US'?2:0)}</td><td>${fmt(t.quantity)}</td><td class="${cls(t.pnl)}">${sign(t.pnl)}${fmt(t.pnl)}</td></tr>`).join(''):'<tr><td class="empty" colspan="6">아직 매매 기록이 없습니다. 거래하지 않는 것도 정상적인 판단입니다.</td></tr>';
    const logs=(logKind==='decisions'?d.decisions:d.logs)||[];
    $('logs').innerHTML=logs.length?logs.slice(0,logKind==='decisions'?12:80).map(l=>`<div class="stock-log-line"><time>${esc(l[0])}</time><span><b>${esc(l[1])}</b> · ${esc(l[2])}</span></div>`).join(''):'<div class="stock-log-line">관찰 기록이 아직 연결되지 않았습니다.</div>';
    const at=state?.updated_at,age=at?Date.now()-Date.parse(at):NaN;
    $('updated').textContent=demo?'미리보기 · 자동 데이터 연결 전':at?`자료 시각 ${new Date(at).toLocaleString('ko-KR')}${!Number.isFinite(age)||age>86400000?' · 지난 관찰 기록':''}`:'연결 대기 · 마지막 관찰 시각 없음';
    draw();
  }
  const candles={id:'stockCandles',afterDatasetsDraw(c){if(!candle||chartKind!=='price')return;const {ctx,scales:{x,y},chartArea:a}=c;const values=c.data.datasets[0].data;ctx.save();ctx.beginPath();ctx.rect(a.left,a.top,a.right-a.left,a.bottom-a.top);ctx.clip();values.forEach((close,i)=>{const open=values[Math.max(0,i-1)],xx=x.getPixelForValue(i),w=Math.max(2,(a.right-a.left)/values.length*.55);ctx.strokeStyle=ctx.fillStyle=close>=open?'#d93b48':'#2866cf';ctx.beginPath();ctx.moveTo(xx,y.getPixelForValue(Math.max(open,close)+8));ctx.lineTo(xx,y.getPixelForValue(Math.min(open,close)-8));ctx.stroke();ctx.fillRect(xx-w/2,y.getPixelForValue(Math.max(open,close)),w,Math.max(1,Math.abs(y.getPixelForValue(open)-y.getPixelForValue(close))));});ctx.restore();}};
  function draw(){if(root.hidden||$('dashboard').hidden)return;if(chart){chart.destroy();chart=null;}const d=data();let values=demo?(chartKind==='price'?d.series:d.equity_series):null; if(demo&&chartKind==='equity')values=Array(20).fill(0); if(!Array.isArray(values)||!values.length||!window.Chart){$('chart-empty').hidden=false;$('chart-empty').textContent=!window.Chart?'차트 모듈을 불러오는 중입니다.':'차트 자료가 아직 없습니다.';return;}$('chart-empty').hidden=true;const color=(d.change||0)>=0?'#d93b48':'#2866cf';chart=new Chart($('chart'),{type:'line',data:{labels:values.map((_,i)=>chartKind==='price'?`${String(9+Math.floor(i*5/60)).padStart(2,'0')}:${String(i*5%60).padStart(2,'0')}`:`${i+1}`),datasets:[{data:values,borderColor:color,backgroundColor:color+'09',borderWidth:candle&&chartKind==='price'?0:1.7,pointRadius:0,fill:!candle,tension:0}]},plugins:[candles],options:{responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:false},tooltip:{enabled:!candle}},scales:{x:{grid:{display:false},ticks:{maxTicksLimit:7,color:'#9099a7',font:{size:10}},border:{display:false}},y:{position:'right',grid:{color:'#f0f2f6'},border:{display:false},ticks:{maxTicksLimit:5,color:'#9099a7',font:{size:10}}}}}});}
  async function refresh(){if(demo||root.hidden||document.hidden||busy)return;busy=true;const c=new AbortController(),timer=setTimeout(()=>c.abort(),8000);try{const r=await fetch(STATE_URL,{cache:'no-store',credentials:'omit',signal:c.signal});if(!r.ok)throw new Error('공개 관찰 기록을 불러오지 못했습니다.');const next=await r.json();if(next.mode!=='observation_only'||!next.markets)throw new Error('관찰 자료 형식을 확인할 수 없습니다.');state=next;$('error').hidden=true;render();}catch(e){state=null;$('error').textContent=e.message+' 연결을 확인하세요.';$('error').hidden=false;render();}finally{clearTimeout(timer);busy=false;}}
  $('demo-toggle').onclick=()=>{demo=!demo;render();refresh();};
  root.querySelectorAll('[data-stock-market]').forEach(b=>{b.onclick=()=>{market=b.dataset.stockMarket;manualMarket=true;render();};b.onkeydown=e=>{if(['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();const other=root.querySelector('[data-stock-market="KR"]');other.focus();}};});
  root.querySelectorAll('[data-stock-chart]').forEach(b=>b.onclick=()=>{chartKind=b.dataset.stockChart;root.querySelectorAll('[data-stock-chart]').forEach(x=>x.setAttribute('aria-pressed',x===b));render();});
  $('chart-unit').onclick=()=>{if(chartKind==='price'){if(!demo){$('error').textContent='실제 캔들 원본 데이터 연결 전입니다.';$('error').hidden=false;return;}candle=!candle;}else percent=!percent;render();};
  root.querySelectorAll('[data-stock-log]').forEach(b=>b.onclick=()=>{logKind=b.dataset.stockLog;root.querySelectorAll('[data-stock-log]').forEach(x=>x.setAttribute('aria-pressed',x===b));render();});
  new MutationObserver(()=>{if(!root.hidden){render();refresh();}}).observe(root,{attributes:true,attributeFilter:['hidden']});
  setInterval(refresh,5000);refresh();document.addEventListener('visibilitychange',refresh);
  const script=document.createElement('script');script.src='https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js';script.onload=draw;script.onerror=()=>{$('chart-empty').textContent='차트를 불러오지 못했습니다. 네트워크 연결을 확인하세요.';};document.head.appendChild(script);render();
})();
