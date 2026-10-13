'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {ASSETS,rowsFor,makeTile,missing,validateMarket}=require('./market.cjs');
const end=Date.parse('2026-10-13T06:00:00+09:00')/1000;
const result=rows=>({timestamp:rows.map(r=>r[0]),indicators:{quote:[{close:rows.map(r=>r[1])}]}});
test('rejects future and partial bars while ignoring null prices',()=>{
 const a=ASSETS.find(a=>a.id==='bitcoin');const rows=rowsFor(result([[end-120,null],[end-60,100],[end-30,200],[end,300]]),a,end);
 assert.deepEqual(rows.map(r=>r.value),[100]);
});
test('uses New York daylight saving close, not daily bar open',()=>{
 const a=ASSETS.find(a=>a.id==='sp500');const r=result([[Date.parse('2026-10-12T13:30:00Z')/1000,100]]);
 assert.equal(rowsFor(r,a,Date.parse('2026-10-12T19:00:00Z')/1000).length,0);
 assert.equal(rowsFor(r,a,end)[0].priceTime,Date.parse('2026-10-12T20:00:00Z')/1000);
 const winter=result([[Date.parse('2026-11-12T14:30:00Z')/1000,100]]);
 assert.equal(rowsFor(winter,a,Date.parse('2026-11-13T06:00:00+09:00')/1000).length,0); // close is exactly cutoff
});
test('intraday comparison requires identical 24-hour clock, not adjacent minute',()=>{
 const a=ASSETS.find(a=>a.id==='bitcoin');const t=makeTile(result([[end-86400-120,90],[end-60,100]]),a,end,'https://example.com/quote');
 assert.equal(t.changePercent,null);
 const u=makeTile(result([[end-86400-60,80],[end-60,100]]),a,end,'https://example.com/quote');assert.equal(u.changePercent,25);
});
test('failed prices retain all slots and reasons; dropping a slot fails publication',()=>{
 const tiles=ASSETS.map(a=>missing(a,end,[{url:'https://example.com',result:'HTTP 429'}],'HTTP 429'));
 validateMarket({tiles},'2026-10-13T06:00:00+09:00');
 assert.throws(()=>validateMarket({tiles:tiles.slice(0,9)},'2026-10-13T06:00:00+09:00'));
 tiles[0].missingReason='';assert.throws(()=>validateMarket({tiles},'2026-10-13T06:00:00+09:00'));
});
