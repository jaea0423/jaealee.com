'use strict';
// Ten permanent slots. Daily equity closes and pre-cutoff intraday bars are distinct.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const ASSETS = [
  ['kospi','코스피','KOSPI','^KS11','1d','Asia/Seoul','15:30','지수(포인트)'],
  ['kosdaq','코스닥','KOSDAQ','^KQ11','1d','Asia/Seoul','15:30','지수(포인트)'],
  ['sp500','S&P 500','S&P 500','^GSPC','1d','America/New_York','16:00','지수(포인트)'],
  ['nasdaq','나스닥','NASDAQ Composite','^IXIC','1d','America/New_York','16:00','지수(포인트)'],
  ['qqq','QQQ','Invesco QQQ','QQQ','1d','America/New_York','16:00','USD/주'],
  ['usdkrw','원/달러','USD/KRW','KRW=X','5m',null,null,'KRW/USD · 글로벌 호가, 서울 주간 종가와 다름'],
  ['dxy','달러인덱스','DXY','DX-Y.NYB','5m',null,null,'지수(포인트)'],
  ['gold','금','Gold Futures','GC=F','5m',null,null,'금 선물 · USD/트로이온스 · 현물과 다름'],
  ['wti','WTI 유가','WTI Futures','CL=F','5m',null,null,'WTI 선물 · USD/배럴'],
  ['bitcoin','비트코인','BTC/USD','BTC-USD','1m',null,null,'USD/BTC'],
].map(([id,name,en,symbol,interval,timezone,closeTime,unit])=>({id,name,en,symbol,interval,timezone,closeTime,unit}));
function dateInZone(seconds,timezone) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('en-CA',{timeZone:timezone,year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date(seconds*1000)).map(x=>[x.type,x.value]));
  return `${p.year}-${p.month}-${p.day}`;
}
function localSeconds(date,time,timezone) {
  const base=Date.parse(`${date}T${time}:00Z`); let guess=base;
  for(let i=0;i<4;i++) {
    const p=Object.fromEntries(new Intl.DateTimeFormat('en-GB',{timeZone:timezone,year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}).formatToParts(new Date(guess)).map(x=>[x.type,x.value]));
    const represented=Date.parse(`${p.year}-${p.month}-${p.day}T${p.hour}:${p.minute}:${p.second}Z`);
    guess += base-represented;
  }
  return guess/1000;
}
function kst(seconds) {return new Date(seconds*1000+9*3600000).toISOString().replace('Z','+09:00');}
function rowsFor(result,asset,cutoff) {
  const q=result.indicators?.quote?.[0]?.close || [];
  const span=asset.interval==='1m'?60:300;
  return (result.timestamp||[]).map((bar,i)=>{
    const priceTime=asset.interval==='1d'?localSeconds(dateInZone(bar,asset.timezone),asset.closeTime,asset.timezone):bar+span-1;
    return {bar,priceTime,value:q[i]};
  }).filter(r=>Number.isFinite(r.value)&&r.value>0&&r.priceTime<cutoff).sort((a,b)=>a.priceTime-b.priceTime);
}
function missing(asset,cutoff,attempts,reason) {
  return {id:asset.id,name:asset.name,en:asset.en,value:'확인 못함',change:'등락률 미산출',dir:'flat',status:'unavailable',asof:`${kst(cutoff)} 기준 · 조회 실패`,fx:`${asset.unit} · 조회 실패 사유: ${reason}`,missingReason:reason,sourceUrl:null,attempts};
}
function makeTile(result,asset,cutoff,url) {
  const rows=rowsFor(result,asset,cutoff);if(!rows.length)throw new Error('기준 시각 이전 유효 가격 없음');
  const latest=rows.at(-1);
  if(cutoff-latest.priceTime>7*86400)throw new Error('가격이 7일 이상 오래됨');
  const prev=asset.interval==='1d'?rows.at(-2):rows.findLast(r=>r.priceTime===latest.priceTime-86400);
  const delta=prev?(latest.value/prev.value-1)*100:null;
  const label=asset.interval==='1d'?'정규장 종가(보수적으로 정상 마감시각 적용) · 전 거래일 대비':`${asset.interval==='1m'?'1분':'5분'}봉 마지막 가격 · 같은 시각 24시간 전 대비`;
  const suffix=asset.id==='usdkrw'?'원':(['qqq','gold','wti','bitcoin'].includes(asset.id)?' USD':'');
  return {id:asset.id,name:asset.name,en:asset.en,value:latest.value.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})+suffix,change:delta===null?'비교값 미확인':`${delta>0?'▲':delta<0?'▼':''}${Math.abs(delta).toFixed(2)}%`,dir:delta>0?'up':delta<0?'down':'flat',status:'verified',asof:`${kst(latest.priceTime)} · ${label}`,fx:asset.unit+(cutoff-latest.priceTime>3600?' · 최근 확인값(휴장·거래시간 확인)':''),price:latest.value,priceAt:kst(latest.priceTime),barAt:kst(latest.bar),comparisonAt:prev?kst(prev.priceTime):null,comparisonPrice:prev?.value??null,changePercent:delta,sourceUrl:url,provider:'Yahoo Finance',interval:asset.interval};
}
function validateMarket(market,cutoff) {
  assert.equal(market.tiles.length,ASSETS.length,'시장 10개 항목 유지 필수');
  assert.deepEqual(market.tiles.map(t=>t.id),ASSETS.map(a=>a.id),'시장 항목 ID·순서 고정');
  for(const tile of market.tiles) {
    assert(['verified','unavailable'].includes(tile.status),'확인 상태 필수');
    if(tile.status==='verified') {
      assert(Number.isFinite(tile.price)&&tile.price>0,'유효 가격 필수');
      assert(Number.isFinite(Date.parse(tile.priceAt))&&Date.parse(tile.priceAt)<Date.parse(cutoff),'기준 시각 이후 가격 금지');
      assert(tile.sourceUrl?.startsWith('https://'),'확인 출처 필수');
      if(tile.changePercent!==null)assert(Math.abs(tile.changePercent-(tile.price/tile.comparisonPrice-1)*100)<1e-8,'동일 기준 비교값 필요');
    } else {assert(tile.missingReason?.trim(),'누락 사유 필수');assert(tile.attempts?.length,'실제 조회 시도 기록 필수');}
  }
}
async function collect(date,auditDir) {
  assert(/^\d{4}-\d{2}-\d{2}$/.test(date));const cutoff=Date.parse(`${date}T06:00:00+09:00`)/1000;assert(Number.isFinite(cutoff));
  assert(cutoff*1000<=Date.now(),'미래 기준 시각 조회 금지');if(auditDir)fs.mkdirSync(auditDir,{recursive:true});
  const tiles=await Promise.all(ASSETS.map(async asset=>{
    const attempts=[];for(const host of ['query1.finance.yahoo.com','query2.finance.yahoo.com']) {
      const start=cutoff-(asset.interval==='1d'?14*86400:2*86400+300);
      const url=`https://${host}/v8/finance/chart/${encodeURIComponent(asset.symbol)}?interval=${asset.interval}&period1=${start}&period2=${cutoff}`;
      try {
        const response=await fetch(url,{signal:AbortSignal.timeout(15000)});if(!response.ok)throw new Error(`HTTP ${response.status}`);
        const raw=await response.text();const body=JSON.parse(raw);const result=body.chart?.result?.[0];if(!result)throw new Error(body.chart?.error?.description||'가격 데이터 없음');
        if(auditDir)fs.writeFileSync(path.join(auditDir,`${asset.id}-${attempts.length+1}.json`),raw);
        const tile=makeTile(result,asset,cutoff,url);tile.attempts=[...attempts,{url,result:'success'}];return tile;
      }catch(error){attempts.push({url,result:error.message});}
    }
    return missing(asset,cutoff,attempts,attempts.map(a=>a.result).join(' / '));
  }));
  const market={tiles,oneliner:'시장 10개 항목을 유지합니다. 정규장 종가와 기준 직전 시세의 관측 시각을 구분해 확인하세요.',note:'주가지수·QQQ는 마감한 정규장 종가와 전 거래일 대비입니다. 나머지는 기준 시각 직전 5분봉(비트코인 1분봉)의 마지막 가격이며 같은 시각 24시간 전 값이 없으면 등락률을 산출하지 않습니다. 금은 선물, 환율은 글로벌 호가로 현물 금·서울 주간 종가와 다릅니다. 조회 실패도 항목을 제거하지 않습니다.',collectedAt:new Date().toISOString(),cutoff:kst(cutoff)};
  validateMarket(market,market.cutoff);return market;
}
module.exports={ASSETS,rowsFor,makeTile,missing,validateMarket,collect};
if(require.main===module) {
  const args=process.argv.slice(2);const value=flag=>args[args.indexOf(flag)+1];
  if(!args.includes('--date')||!args.includes('--output')){console.error('Usage: node automation/market.cjs --date YYYY-MM-DD --output /private/drafts/market.json [--audit-dir /private/work/market]');process.exitCode=1;}
  else collect(value('--date'),args.includes('--audit-dir')?value('--audit-dir'):null).then(m=>{fs.writeFileSync(value('--output'),JSON.stringify(m,null,2)+'\n');console.log(`시장 ${m.tiles.length}개 · 확인 ${m.tiles.filter(t=>t.status==='verified').length}개 · 실패 ${m.tiles.filter(t=>t.status==='unavailable').length}개`);}).catch(e=>{console.error(e.message);process.exitCode=1;});
}
