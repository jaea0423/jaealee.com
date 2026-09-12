/* 공개용으로 선별한 관찰 요약만 읽습니다. 키·계좌·원문 로그·주문 기능 없음. */
(() => {
  const root=document.getElementById('panel-stock'); if(!root)return;
  const $=id=>document.getElementById('stock-'+id);
  const esc=v=>String(v??'—').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fmt=(v,d=0)=>typeof v==='number'&&Number.isFinite(v)?v.toLocaleString('ko-KR',{maximumFractionDigits:d,minimumFractionDigits:d}):'—';
  const sign=v=>v>0?'+':''; const cls=v=>v>0?'stock-up':v<0?'stock-down':'';
  // 공개 요약 파일만 조회하며 증권사 API를 직접 호출하지 않습니다.
  const STATE_URL='/home/stock-state.json';
  const designPreview=root.dataset.designPreview==='true';

  let period="1m",assetPeriod="1m";
  let selectedAsset=null,assetChart=null,assetCandle=false;
  let demo=designPreview,market='KR',chartKind='equity',candle=false,percent=false,logKind='decisions',chart=null,state=null,busy=false,manualMarket=false;
  const names=[['원 / 달러','KRW',1372.45,.24],['코스피','INDEX',2684.32,-.38],['비트코인','업비트 · KRW',92345000,1.42],['나스닥100','QQQ · ETF',482.36,.85],['S&P 500','SPY · ETF',563.12,.46],['다우존스','DIA · ETF',414.26,-.13],['반도체','SOXX · ETF',231.78,1.26],['금','GLD · ETF',237.15,.32],['원유','USO · ETF',72.64,-.78],['달러','UUP · ETF',28.45,.18]];
  const series=Array.from({length:49},(_,i)=>Math.round(10000+i*5+Math.sin(i*.64)*42+Math.cos(i*.23)*29));
  const demoData=()=>({label:market==='KR'?'한빛테크 · 가상 종목':'Example Tech · 가상 종목',price:market==='KR'?10280:128.5,change:2.8,cash:market==='KR'?1000000:1000,holdings:0,today:0,total:0,fees:0,verdict:'판단 보류',reason:'기업 발표는 확인했지만 가격 반영과 최신 공시를 더 확인해야 합니다.',series:series.map(v=>market==='KR'?v:v/80),trades:[],decisions:[['09:12','판단 보류','가격 반영과 최신 공시가 확인되지 않았습니다.'],['09:10','근거 확인','원문과 인용 문구를 대조했습니다.'],['08:35','자료 수집','예시 자료 묶음의 중복 기사를 제외했습니다.']],logs:[['09:12','OBSERVE','신규 진입 없음 · 예시'],['09:10','SOURCE','원문 대조 완료 · 예시'],['08:35','COLLECT','자료 수집 완료 · 예시']]});
  function data(){if(!demo)return state?.markets?.KR||{};return {...demoData(),net_profit:9800,equity:1509800,cash:597800,total:2800,today:-400,fees:120,initial_equity:1500000,verdict:'보유 유지 · 추가 매수 대기',reason:'예시 판단: 삼성전자 보유분은 유지하고, SK하이닉스는 추가 매수 없이 점검합니다. 달러는 배정 한도 안에서 보유합니다.',trades:Array.from({length:16},(_,i)=>({time:`09/${String(12-Math.floor(i/2)).padStart(2,'0')} ${i%2?'09:35':'14:20'}`,side:i%2?'BUY':'SELL',name:i%3?'삼성전자':'SK하이닉스',price:i%3?62000:160000,quantity:1,pnl:i%2?null:[-400,400,400,400,500,500,500,500][i/2]})),decisions:Array.from({length:12},(_,i)=>[`${String(14-Math.floor(i/3)).padStart(2,'0')}:${String(50-i*3).padStart(2,'0')}`,['보유 유지','추가 매수 대기','위험 한도 확인'][i%3],['기존 보유분의 조건 유지 · 더미','가격 조건 미충족으로 신규 매수하지 않음 · 더미','주식·달러 배정액과 현금 확인 · 더미'][i%3]]),logs:Array.from({length:80},(_,i)=>['09/12 '+String(14-Math.floor(i/6)).padStart(2,'0')+':00',['자료 확인','원문 대조','자산 평가','판단 기록'][i%4],'화면 검토용 더미 기록 '+(i+1)]),buckets:[{name:'주식',allocated:1000000,value:1007800},{name:'달러',allocated:500000,value:502000}],assets:[{id:'samsung',name:'삼성전자',value:250000,change:2.4,average_price:60000,price:62500,quantity:4,unit:'원 / 주'},{id:'hynix',name:'SK하이닉스',value:160000,change:-1.8,average_price:165000,price:160000,quantity:1,unit:'원 / 주'},{id:'usd',name:'미국 달러',value:502000,change:.4,average_price:1372.45/1.004,price:1372.45,quantity:502000/1372.45,unit:'원 / 1 USD'},{id:'cash',name:'원화 대기자금',value:597800,change:0,price:null,quantity:null,unit:'원'}],equity_series:[0,1200,800,2400,1800,3100,4600,3900,5200,4900,6300,6100,7200,6800,8100,7800,9300,9000,10200,9800]};}
  function render(){
    const d=data(),unit=market==='KR'?'원':'USD';
    $('mode-note').textContent=demo?'화면 미리보기 · 아래 숫자와 기록은 모두 가상 예시입니다.':'공개 관찰 기록 · 자동 매매 미가동 · 실제 주문 없음';
    $('demo-toggle').textContent=demo?'예시 끄기':'예시 보기';
    $('market-time').textContent=demo?'예시 · 실시간 시세 아님':state?.market_updated_at?new Date(state.market_updated_at).toLocaleString('ko-KR'):'시세 연결 대기';
    $('markets').innerHTML=names.map(([name,ticker,value,change],i)=>{const m=demo?{value,change}:state?.overview?.[i]||{};return `<div class="stock-market-item"><p>${esc(name)}<small>${esc(ticker)}</small></p><strong>${fmt(m.value,i===2?0:2)}</strong><em class="${cls(m.change)}">${typeof m.change==='number'?(m.change>=0?'▲ ':'▼ ')+fmt(Math.abs(m.change),2)+'%':'확인 대기'}</em></div>`;}).join('');
    const stats=[['누적 총손익',d.net_profit,'원','실현 + 평가손익 · 비용 차감'],['총 평가금액',d.equity,'원','현금 + 보유 자산'],['투자 가능 현금',d.cash,'원','예수금 · 계좌 연결 시 표시'],['금일 실현손익',d.today,'원','매도 완료분 기준'],['누적 비용',d.fees,'원','확인된 체결 비용']];
    $('stats').innerHTML=stats.map(([label,value,suffix,note],i)=>`<div class="stock-stat"><p>${esc(label)}</p><strong class="${i===0||i===3?cls(value):''}">${i===0||i===3?sign(value):''}${fmt(value)} <span style="font-size:11px">${suffix}</span></strong><small>${esc(note)}</small></div>`).join('');
    $('evidence-text').textContent=demo?'가상 예시 · 기업 발표 원문 대조':d.evidence||'근거 자료 연결 대기';$('unknown-text').textContent=demo?'가상 예시 · 최신 공시와 가격 반영 확인 필요':(d.unknowns||[]).join(' · ')||'미확인 항목 연결 대기';
    $('verdict').textContent=d.verdict||'아직 판단 기록이 없습니다';$('reason').textContent=d.reason||'연결되지 않은 자료를 정상 상태로 표시하지 않습니다.';
    $('judgment-summary').textContent=d.verdict||'기록 없음';
    $('risk').textContent='● '+(demo?'보유 관리 · 신규 진입 대기':'위험 판정 확인 대기');
    $('session').textContent=demo?'예시 화면 · 장중 여부를 추정하지 않습니다':d.session_label?`${d.session_label} · ${d.session_hours||'거래 시간 확인 대기'}`:'거래 시간은 서버 캘린더 연결 후 표시';
    $('chart-label').textContent=chartKind==='price'?(d.label?d.label+(demo?' | 5분봉 · 09:00–13:00 KST · KRW':' | 가격 자료 미연결'):'종목·기간·통화 확인 대기'):'누적 총손익 · '+(demo?'가상 계좌 · '+periodSpec().label+' 예시':'실현·평가손익 포함 · 입출금 제외');
    $('chart-price').textContent=chartKind==='price'?fmt(d.price,market==='US'?2:0)+' '+unit:demo?(percent?fmt(d.net_profit/d.initial_equity*100,2)+'%':sign(d.net_profit)+fmt(d.net_profit)+' 원'):fmt(d.net_profit)+' 원';
    $('chart-change').textContent=chartKind==='price'&&typeof d.change==='number'?`${sign(d.change)}${fmt(d.change,2)}%`:'';$('chart-change').className=cls(d.change);
    $('chart-caption').textContent=demo?'가상 데이터 · 투자 성과 아님':'원본 데이터 시각 기준';

    $('chart-explainer').textContent=chartKind==='price'?(demo?'보유 종목이 아닌 가상 관찰 종목의 가격입니다. 5분 간격 · 구간 상승 빨강 / 하락 파랑':'원본 OHLC·시각·봉 간격 연결 전입니다.'):'입출금으로 늘어난 금액을 수익으로 세지 않습니다. 계좌·비용·평가 이력이 연결되기 전에는 수익을 추정하지 않습니다.';
    const trades=d.trades||[];$('trade-count').textContent=trades.length?'· '+trades.length+'건':'';
    $('trades').innerHTML=trades.length?trades.slice(0,40).map(t=>`<tr><td>${esc(t.time)}</td><td class="${t.side==='BUY'?'stock-up':'stock-down'}">${t.side==='BUY'?'매수':'매도'}</td><td>${esc(t.name)}</td><td>${fmt(t.price,market==='US'?2:0)}</td><td>${fmt(t.quantity)}</td><td class="${cls(t.pnl)}">${sign(t.pnl)}${fmt(t.pnl)}</td></tr>`).join(''):'<tr><td class="empty" colspan="6">아직 매매 기록이 없습니다. 거래하지 않는 것도 정상적인 판단입니다.</td></tr>';
    const logs=(logKind==='decisions'?d.decisions:d.logs)||[];
    $('logs').innerHTML=logs.length?logs.slice(0,logKind==='decisions'?12:80).map(l=>`<div class="stock-log-line"><time>${esc(l[0])}</time><span><b>${esc(l[1])}</b> · ${esc(l[2])}</span></div>`).join(''):'<div class="stock-log-line">관찰 기록이 아직 연결되지 않았습니다.</div>';
    const at=state?.updated_at,age=at?Date.now()-Date.parse(at):NaN;
    $('updated').textContent=demo?'':at?`자료 시각 ${new Date(at).toLocaleString('ko-KR')}${!Number.isFinite(age)||age>86400000?' · 지난 관찰 기록':''}`:'연결 대기 · 마지막 관찰 시각 없음';
    draw();renderAssets();
  }

  // 선택 기간의 극값을 차트 안에 배치합니다. 캔들은 실제 표시한 고가·저가를 사용합니다.
  const extremaLabels={id:'stockExtrema',afterDatasetsDraw(c,args,opts){
    const values=c.data.datasets[0].data;
    const highs=opts.highs||values,lows=opts.lows||values;
    const finite=xs=>xs.map((v,i)=>({v,i})).filter(p=>Number.isFinite(p.v));
    const hi=finite(highs).reduce((a,b)=>!a||b.v>a.v?b:a,null);
    const lo=finite(lows).reduce((a,b)=>!a||b.v<a.v?b:a,null);
    if(!hi||!lo)return;
    const {ctx,chartArea:a,scales:{x,y}}=c;
    ctx.save();ctx.font='11px "Segoe UI", "Malgun Gothic", sans-serif';ctx.textBaseline='middle';
    for(const [p,color,above] of [[hi,'#d93b48',true],[lo,'#2866cf',false]]){
      const label=fmt(p.v,opts.decimals||0)+'원',width=ctx.measureText(label).width;
      const px=x.getPixelForValue(p.i),py=y.getPixelForValue(p.v);
      const tx=Math.max(a.left+width/2+4,Math.min(a.right-width/2-4,px));
      const ty=Math.max(a.top+9,Math.min(a.bottom-9,py+(above?-16:16)));
      ctx.fillStyle='rgba(255,255,255,.92)';ctx.fillRect(tx-width/2-3,ty-8,width+6,16);
      ctx.fillStyle=color;ctx.textAlign='center';ctx.fillText(label,tx,ty);
      ctx.beginPath();ctx.arc(px,py,2.5,0,Math.PI*2);ctx.fill();
    }
    ctx.restore();
  }};

  const candles={id:'stockCandles',afterDatasetsDraw(c){if(!candle||chartKind!=='price')return;const {ctx,scales:{x,y},chartArea:a}=c;const values=c.data.datasets[0].data;ctx.save();ctx.beginPath();ctx.rect(a.left,a.top,a.right-a.left,a.bottom-a.top);ctx.clip();values.forEach((close,i)=>{const open=values[Math.max(0,i-1)],xx=x.getPixelForValue(i),w=Math.max(2,(a.right-a.left)/values.length*.55);ctx.strokeStyle=ctx.fillStyle=close>=open?'#d93b48':'#2866cf';ctx.beginPath();ctx.moveTo(xx,y.getPixelForValue(Math.max(open,close)+8));ctx.lineTo(xx,y.getPixelForValue(Math.min(open,close)-8));ctx.stroke();ctx.fillRect(xx-w/2,y.getPixelForValue(Math.max(open,close)),w,Math.max(1,Math.abs(y.getPixelForValue(open)-y.getPixelForValue(close))));});ctx.restore();}};
  function draw(){if(root.hidden||$('dashboard').hidden)return;if(chart){chart.destroy();chart=null;}const d=data();let values=demo?(chartKind==='price'?d.series:d.equity_series):null; if(demo)values=demoHistory(9800).values; if(demo&&chartKind==='equity'&&percent)values=values.map(v=>v/d.initial_equity*100); if(!Array.isArray(values)||!values.length||!window.Chart){$('chart-empty').hidden=false;$('chart-empty').textContent=!window.Chart?'차트 모듈을 불러오는 중입니다.':'차트 자료가 아직 없습니다.';return;}$('chart-empty').hidden=true;const color=(d.change||0)>=0?'#d93b48':'#2866cf';chart=new Chart($('chart'),{type:'line',data:{labels:demoHistory(9800).labels,datasets:[{data:values,borderColor:color,backgroundColor:color+'09',segment:{borderColor:ctx=>ctx.p1.parsed.y>ctx.p0.parsed.y?'#d93b48':ctx.p1.parsed.y<ctx.p0.parsed.y?'#2866cf':'#8b94a3'},borderWidth:candle&&chartKind==='price'?0:1.7,pointRadius:0,fill:false,tension:0}]},plugins:[candles,extremaLabels],options:{responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:false},tooltip:{enabled:!(candle&&chartKind==='price')}},scales:{x:{grid:{display:false},ticks:{maxTicksLimit:7,color:'#9099a7',font:{size:10}},border:{display:false}},y:{position:'right',grid:{color:'#f0f2f6'},border:{display:false},ticks:{maxTicksLimit:5,color:'#9099a7',font:{size:10}}}}}});}

  // 이분할로 평가금액 면적 비율을 유지합니다. 표시 반올림은 원본 금액을 바꾸지 않습니다.
  function splitTiles(items,x=0,y=0,w=100,h=100){if(!items.length)return [];if(items.length===1)return [{...items[0],x,y,w,h}];const total=items.reduce((s,a)=>s+a.value,0);let sum=0,cut=1;for(let i=0;i<items.length-1;i++){sum+=items[i].value;cut=i+1;if(sum>=total/2)break;}const ratio=sum/total;return w>=h?[...splitTiles(items.slice(0,cut),x,y,w*ratio,h),...splitTiles(items.slice(cut),x+w*ratio,y,w*(1-ratio),h)]:[...splitTiles(items.slice(0,cut),x,y,w,h*ratio),...splitTiles(items.slice(cut),x,y+h*ratio,w,h*(1-ratio))];}
  function renderAssets(){const d=data(),assets=(d.assets||[]).map(a=>({...a,return_pct:a.id==='cash'?0:(Number.isFinite(a.price)&&Number.isFinite(a.average_price)&&a.average_price>0?(a.price/a.average_price-1)*100:null)})).filter(a=>typeof a.value==='number'&&Number.isFinite(a.value)&&a.value>0);const total=assets.reduce((s,a)=>s+a.value,0);$('assets-note').textContent=demo?'편집용 더미 · 실제 보유/배정이 아닙니다. 주식·달러를 눌러 아래 가격 차트를 확인하세요.':'실제 보유 자산 연결 대기 · 관찰 종목과 보유 종목은 다릅니다.';
    $('buckets').innerHTML=(d.buckets||[]).map(b=>`<div><span>${esc(b.name)} 자산</span><strong>${fmt(b.value)}원 <em class="${cls(b.value-b.allocated)}">${b.allocated>0?sign(b.value-b.allocated)+fmt((b.value/b.allocated-1)*100,2)+'%('+sign(b.value-b.allocated)+fmt(b.value-b.allocated)+'원)':'—'}</em></strong><small>배정 ${fmt(b.allocated)}원</small></div>`).join('');
    $('treemap').innerHTML=assets.length?splitTiles([...assets].sort((a,b)=>b.value-a.value)).map(a=>`<button class="stock-tile ${a.return_pct>0?'tile-up':a.return_pct<0?'tile-down':'tile-neutral'}" data-asset-id="${esc(a.id)}" aria-pressed="${a.id===selectedAsset}" ${a.id==='cash'?'disabled':''} style="left:${a.x}%;top:${a.y}%;width:${a.w}%;height:${a.h}%" aria-label="${esc(a.name)} 비중 ${fmt(a.value/total*100,1)}%, 평단 대비 ${sign(a.return_pct)}${fmt(a.return_pct,2)}%"><b>${esc(a.name)}</b><strong>${sign(a.return_pct)}${fmt(a.return_pct,2)}%</strong><small>${fmt(a.value)}원 · 비중 ${fmt(a.value/total*100,1)}%</small></button>`).join(''):'<p class="stock-assets-empty">보유 자산이 연결되면 비중별로 표시합니다.<br>예시 보기에서 여러 자산의 구성을 확인할 수 있습니다.</p>';
    $('treemap').querySelectorAll('[data-asset-id]').forEach(b=>b.onclick=()=>{selectedAsset=b.dataset.assetId;renderAssets();});
    const a=assets.find(a=>a.id===selectedAsset);$('asset-detail').hidden=!a;if(assetChart){assetChart.destroy();assetChart=null;}if(!a)return;
    $('asset-name').textContent=a.name+(demo?' · 더미 가격':'');$('asset-price').textContent=fmt(a.price,a.id==='usd'?2:0)+' '+a.unit;$('asset-return').textContent='평단 대비 '+sign(a.return_pct)+fmt(a.return_pct,2)+'%';$('asset-return').className=cls(a.return_pct);
    $('asset-meta').textContent=`평단 ${fmt(a.average_price,a.id==='usd'?2:0)}원 · 보유 ${fmt(a.quantity,a.id==='usd'?4:0)}${a.id==='usd'?' USD':'주'} · 평가 ${fmt(a.value)}원 · ${demo?periodSpec(assetPeriod).label+' / '+periodSpec(assetPeriod).interval+' 가상 자료':'원본 시각 확인 필요'}`;
    $('asset-line').setAttribute('aria-pressed',!assetCandle);$('asset-candle').setAttribute('aria-pressed',assetCandle);
    if(!demo||!window.Chart){$('asset-empty').hidden=false;return;}$('asset-empty').hidden=true;
    const prices=demoHistory(a.price,true,assetPeriod).values,bars=prices.map((close,i)=>{const open=prices[Math.max(0,i-1)],pad=a.price*.001;return {open,close,high:Math.max(open,close)+pad,low:Math.min(open,close)-pad};});
    const plugin={id:'holdingCandles',afterDatasetsDraw(c){if(!assetCandle)return;const {ctx,scales:{x,y}}=c;ctx.save();bars.forEach((b,i)=>{const px=x.getPixelForValue(i);ctx.fillStyle=ctx.strokeStyle=b.close>=b.open?'#d93b48':'#2866cf';ctx.beginPath();ctx.moveTo(px,y.getPixelForValue(b.high));ctx.lineTo(px,y.getPixelForValue(b.low));ctx.stroke();ctx.fillRect(px-2,y.getPixelForValue(Math.max(b.open,b.close)),4,Math.max(1,Math.abs(y.getPixelForValue(b.open)-y.getPixelForValue(b.close))));});ctx.restore();}};
    assetChart=new Chart($('asset-chart'),{type:'line',data:{labels:demoHistory(a.price,true,assetPeriod).labels,datasets:[{data:prices,pointRadius:0,borderWidth:assetCandle?0:1.7,tension:0,segment:{borderColor:c=>c.p1.parsed.y>=c.p0.parsed.y?'#d93b48':'#2866cf'}}]},plugins:[plugin,extremaLabels],options:{responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:false},stockExtrema:{decimals:a.id==='usd'?2:0,...(assetCandle?{highs:bars.map(b=>b.high),lows:bars.map(b=>b.low)}:{})}},scales:{x:{ticks:{maxTicksLimit:6}},y:{position:'right',suggestedMin:Math.min(...bars.map(b=>b.low)),suggestedMax:Math.max(...bars.map(b=>b.high))}}}});
  }
  $('asset-line').onclick=()=>{assetCandle=false;renderAssets();};$('asset-candle').onclick=()=>{assetCandle=true;renderAssets();};


  function periodSpec(selected=period){return {"1d":{label:'1일',n:49,days:0,interval:'5분 간격'},"1m":{label:'1개월',n:31,days:30,interval:'일별'},"3m":{label:'3개월',n:91,days:90,interval:'일별'},"1y":{label:'1년',n:53,days:365,interval:'주별'},"3y":{label:'3년',n:157,days:1095,interval:'주별'}}[selected];}
  function demoHistory(last,price=false,selected=period){const s=periodSpec(selected),end=Date.UTC(2026,8,12),values=[],labels=[];for(let i=0;i<s.n;i++){const t=i/(s.n-1);values.push(price?last*(.93+.07*t+.008*Math.sin(i*.8)*(1-t)):Math.round(last*t+Math.sin(i*.9)*1100*(1-t)));const date=new Date(end-(s.days*(1-t))*86400000);labels.push(selected==='1d'?`${String(9+Math.floor(i*5/60)).padStart(2,'0')}:${String(i*5%60).padStart(2,'0')}`:(s.days>90?date.getUTCFullYear()+'/'+(date.getUTCMonth()+1):date.getUTCMonth()+1+'/'+date.getUTCDate()));}values[values.length-1]=last;return {values,labels};}
  root.querySelectorAll('[data-stock-period]').forEach(b=>b.onclick=()=>{period=b.dataset.stockPeriod;root.querySelectorAll('[data-stock-period]').forEach(x=>x.setAttribute('aria-pressed',x===b));render();});

  root.querySelectorAll('[data-stock-asset-period]').forEach(b=>b.onclick=()=>{assetPeriod=b.dataset.stockAssetPeriod;root.querySelectorAll('[data-stock-asset-period]').forEach(x=>x.setAttribute('aria-pressed',x===b));renderAssets();});

  async function refresh(){if(demo||root.hidden||document.hidden||busy)return;busy=true;const c=new AbortController(),timer=setTimeout(()=>c.abort(),8000);try{const r=await fetch(STATE_URL,{cache:'no-store',credentials:'omit',signal:c.signal});if(!r.ok)throw new Error('공개 관찰 기록을 불러오지 못했습니다.');const next=await r.json();if(next.mode!=='observation_only'||!next.markets)throw new Error('관찰 자료 형식을 확인할 수 없습니다.');state=next;$('error').hidden=true;render();}catch(e){state=null;$('error').textContent=e.message+' 연결을 확인하세요.';$('error').hidden=false;render();}finally{clearTimeout(timer);busy=false;}}
  $('demo-toggle').onclick=()=>{selectedAsset=null;demo=!demo;render();refresh();};
  root.querySelectorAll('[data-stock-chart]').forEach(b=>b.onclick=()=>{chartKind=b.dataset.stockChart;root.querySelectorAll('[data-stock-chart]').forEach(x=>x.setAttribute('aria-pressed',x===b));render();});
  root.querySelectorAll('[data-stock-log]').forEach(b=>b.onclick=()=>{logKind=b.dataset.stockLog;root.querySelectorAll('[data-stock-log]').forEach(x=>x.setAttribute('aria-pressed',x===b));render();});
  new MutationObserver(()=>{if(!root.hidden){render();refresh();}}).observe(root,{attributes:true,attributeFilter:['hidden']});
  setInterval(refresh,5000);refresh();document.addEventListener('visibilitychange',refresh);
  const script=document.createElement('script');script.src='https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js';script.onload=()=>{draw();renderAssets();};script.onerror=()=>{$('chart-empty').textContent='차트를 불러오지 못했습니다. 네트워크 연결을 확인하세요.';};document.head.appendChild(script);render();
})();
